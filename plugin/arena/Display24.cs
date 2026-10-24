using System.Globalization;
using System.Text;
using System.Text.RegularExpressions;
using System.Text.Json.Nodes;
using DeadworksManaged.Api;

namespace SandboxTester;

// Experiment metadata + live in-game display + pre-state verify.
//  - Scenario files declare `meta <key> <text>` lines (question, kind, purpose, alternatives, mechanics, expectedstate, build, checkpoint, excluded,
//    accmode, accwhy, abilities, runs, reasonnext, assumed, conclusion). The runner refuses experiments without the mandatory ones.
//  - Display: CCitadelPlayerController.HudAnnounce (compact panel, refreshed only when it changed, >=3 s apart) + Chat lines on phase changes.
//    Every displayed line is also written to plugin.log as `DISPLAY ...`. ctl\display_off disables the in-game output (log lines remain).
//  - statecheck / expect-state: start-state record + comparison against expectedstate; waits (legitimate expiry) or hardresets, else FAIL.
public partial class SandboxTester
{
	private static readonly string[] MetaKinds = { "BASELINE", "ISOLATED ITEM", "PURCHASE CHECKPOINT", "COMPLETE BUILD", "INTERACTION" };
	private static Dictionary<string, string> _meta = new(StringComparer.OrdinalIgnoreCase);
	private static string _phase = "idle", _phaseWhy = "";
	private static int _runX, _runY;
	private static string _lastPanel = "", _taskLine = "";
	private static long _hudAt, _hudForce, _chatAt;
	private static readonly Queue<(string line, bool head)> _chatQ = new();
	private static string _hudOverT = "", _hudOverD = "", _lastHud = ""; private static long _hudOverUntil;
	private static double _dispPerfSum, _dispPerfMax; private static long _dispPerfN;
	private static readonly List<string> _startStates = new();
	private static int _hzStacks = -1, _hzStartStacks = -1; private static bool _hzAwaitFirst; private static string _hzNote = "";

	private static bool DispOn() { try { return !File.Exists(Path.Combine(RootDir(), "ctl", "display_off")); } catch { return true; } }

	// ---------------- metadata ----------------
	private static Dictionary<string, string> ReadMeta(string name)
	{
		var d = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);
		try
		{
			var f = Path.Combine(RootDir(), "scenarios", name + ".txt");
			if (!File.Exists(f)) return d;
			foreach (var raw in File.ReadAllLines(f))
			{
				var l = raw.Trim(); int h = l.IndexOf('#'); if (h >= 0) l = l[..h].Trim();
				if (!l.StartsWith("meta ", StringComparison.OrdinalIgnoreCase)) continue;
				var rest = l[5..].Trim(); int sp = rest.IndexOf(' ');
				if (sp < 0) { d[rest] = ""; continue; }
				var k = rest[..sp]; var v = rest[(sp + 1)..].Trim();
				d[k] = d.TryGetValue(k, out var o) ? o + " " + v : v;
			}
		}
		catch { }
		return d;
	}

	// null = OK, else why the experiment is anonymous/inconsistent
	private static string? MetaLint(Dictionary<string, string> d)
	{
		string G(string k) => d.TryGetValue(k, out var v) ? v.Trim() : "";
		var kind = G("kind").ToUpperInvariant();
		if (!MetaKinds.Contains(kind)) return "meta kind missing/invalid (BASELINE | ISOLATED ITEM | PURCHASE CHECKPOINT | COMPLETE BUILD | INTERACTION)";
		foreach (var k in new[] { "question", "purpose", "mechanics", "expectedstate" }) if (G(k).Length < 3) return $"meta {k} missing";
		if (kind == "ISOLATED ITEM" && G("excluded").Length < 10) return "ISOLATED ITEM must declare `meta excluded <what is excluded and why>`";
		if (kind == "INTERACTION" && (G("strategy_source").Length < 5 || G("feeds").Length < 10 || G("result_says").Length < 5)) return "INTERACTION must declare meta strategy_source, feeds and result_says";
		if ((kind == "COMPLETE BUILD" || kind == "PURCHASE CHECKPOINT" || kind == "INTERACTION") && (G("build").Length == 0 || G("checkpoint").Length == 0)) return $"{kind} must declare meta build and meta checkpoint";
		if (kind == "BASELINE" && !Regex.IsMatch(G("expectedstate"), @"items=(0|none)")) return "BASELINE expectedstate must contain items=none";
		if (G("required_activation").Length > 0) foreach (var part in G("required_activation").Split(';', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries)) { var pp = part.Split('|'); if (pp.Length < 3 || !new[] { "modifier", "ability", "event" }.Contains(pp[1].Trim().ToLowerInvariant())) return $"required_activation entry '{part}' must be <label>|modifier|ability|event|<match>[|min]"; }
		if (G("required_readback").Length > 0) foreach (var part in G("required_readback").Split(';', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries)) { var pp = part.Split('|'); if (pp.Length < 4 || !new[] { ">", ">=", "<", "<=", "==", "!=" }.Contains(pp[2].Trim())) return $"required_readback entry '{part}' must be <label>|<reading>|<op>|<reading or number>"; }
		if (G("condition").ToLowerInvariant().Contains("damage taken") || G("condition").ToLowerInvariant().Contains("damage_taken")) return "paused-needs-design: the condition needs real incoming damage; artificial damage commands do not trigger damage-taken effects and no real damage source is supported";
		if (G("required_levels").Length > 0) foreach (var part in G("required_levels").Split(';', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries)) { var pp = part.Split('='); if (pp.Length != 2 || !int.TryParse(pp[1].Trim(), out _)) return $"required_levels entry '{part}' must be <ability or slot>=<level>"; }
		var pc = PClass(d);
		foreach (var k in new[] { "player_title", "player_what", "player_why", "player_short", "player_expect" })
		{
			foreach (var part in G(k).Split('|')) if (part.Trim().Length > (k == "player_short" ? 26 : 32)) return $"meta {k} part '{part.Trim()}' is {part.Trim().Length} chars; max {(k == "player_short" ? 26 : 32)} so the HUD line is not clipped";
			if (pc == "BUILD" && G(k).Length < 5 && k != "player_expect") return $"paused-needs-design: build experiment needs plain-English meta {k} from the planner/theorycrafter";
		}
		if (pc == "BUILD" && G("strategy_source").Length < 5) return "paused-needs-design: build experiment needs meta strategy_source (planner/theorycrafter file the reasoning comes from)";
		if (kind == "ISOLATED ITEM" && pc == "BUILD" && G("feeds").Length < 10) return "isolated item inside a build investigation needs meta feeds <which build question it feeds>";
		return null;
	}

	private static string M(string k, string d = "") => _meta.TryGetValue(k, out var v) && v.Length > 0 ? v : d;

	private static void DispStartScenario(string name, string origin)
	{
		_meta = ReadMeta(name); ActReset(); _everMeasured = false; _phase = "setup"; _phaseWhy = ""; _runX = _runY = 0; _lastPanel = ""; _startStates.Clear(); _hzStacks = _hzStartStacks = -1; _hzAwaitFirst = false;
		var rs = M("runs"); if (rs.Contains('/')) { var p = rs.Split('/'); int.TryParse(p[0], out _runX); int.TryParse(p[1], out _runY); }
		_dispPerfSum = _dispPerfMax = 0; _dispPerfN = 0;
		ChatGroup(StatusTitle(), WhatLine(), WhyLine());
		if (PClass(_meta) == "BUILD" && M("question").Length > 0) foreach (var x in Wrap(M("question"), 32, 3)) ChatGroup2(x);
		Log("DISPLAY FULL " + $"{M("hero", _myHero.ToString())} | {M("checkpoint", "no checkpoint")} | {M("kind", "?")}: {M("question", "(no question declared)")} (build: {M("build", "none")}; items: {M("items", "none")}; why: {M("purpose", "?")})");
		DispStrategy();
	}
	private static string _nextNote = "", _nextNoteFor = "";
	private static string Cap(string x) => x.Length <= 200 ? x : x[..197] + "...";
	private static void DispStrategy()
	{
		try
		{
			string kind = M("kind").ToUpperInvariant();
			foreach (var k in new[] { "hypothesis", "alternatives", "tradeoffs", "missing_evidence" })
				if (M(k).Length > 0) Say(Cap(k.Replace('_', ' ') + ": " + M(k)), false);
			string sf = M("strategy_source").Length > 0 ? M("strategy_source") : M("strategy_file");
			if (sf.Length > 0)
			{
				var path = Path.IsPathRooted(sf) ? sf : Path.Combine(RootDir(), sf);
				if (File.Exists(path))
				{
					int n = 0;
					foreach (var raw in File.ReadLines(path).Take(2000))
					{
						var l = raw.Trim().TrimStart('#', '/', '*', ' ');
						if (l.StartsWith("GAME_SUMMARY:", StringComparison.OrdinalIgnoreCase) && n < 4) { Say(Cap(l["GAME_SUMMARY:".Length..].Trim()), false); n++; }
					}
					if (n == 0) Log("DISPLAY strategy source has no GAME_SUMMARY: lines (ok for interaction files): " + path);
				}
				else Log("DISPLAY strategy source missing on this PC: " + path);
			}
			if (kind == "ISOLATED ITEM") Say("ISOLATED: does not justify the overall build", false);
		}
		catch (Exception e) { Log("DISPLAY strategy failed: " + e.Message); }
	}

	private static void DispMarkNext(Step st)
	{
		try
		{
			var l = string.Join(' ', st.A);
			if (l == "none" || l.Length == 0) { DispPhase("idle-between-blocks"); return; }
			_everMeasured = true; ActMark(l); DispPhase("measure", l);
			var me = MyPawn(); string items = "?";
			try { if (me != null) { var its = me.AbilityComponent.Abilities.Where(a => a.IsItem).Select(a => ShortItem(a.AbilityName)).ToList(); items = its.Count == 0 ? "no items" : string.Join("+", its); } } catch { }
			Say($"{(me != null ? me.HeroID.ToString() : "?")} - now testing [{l}] - {M("purpose", M("question", "?"))} | items read back: {items} | aim: {AccText()} | run {(_runY > 0 ? _runX + "/" + _runY : "1/1")}", false);
		}
		catch { }
	}
	private static string RunEnv() { try { var f = Path.Combine(RootDir(), "ctl", "env.txt"); return File.Exists(f) ? File.ReadAllText(f).Trim() : "ENV: unlabelled"; } catch { return "ENV: unlabelled"; } }
	private static void DispNextLine(JsonObject? done)
	{
		try
		{
			var nx = QTasks().OfType<JsonObject>().FirstOrDefault(x => TS(x, "state") == "pending");
			if (nx == null) { _nextShort = "Next: queue empty"; Say("NEXT: queue empty", false); return; }
			var md = ReadMeta(TS(nx, "scenario"));
			_nextShort = Trunc("Next: " + md.GetValueOrDefault("player_short", "another test"), 32);
			ChatGroup2(_nextShort);
			Say($"NEXT: {md.GetValueOrDefault("kind", "?")} {TS(nx, "id")} - {md.GetValueOrDefault("question", "(no question)")} because {md.GetValueOrDefault("purpose", "it is the next pending task")}", false);
		}
		catch { }
	}



	// ---------------- compact presentation (HUD banner + short chat) ----------------
	private static string _nextShort = ""; private static bool _everMeasured;
	private static string Trunc(string x, int n)
	{
		x = (x ?? "").Replace("\r", " ").Replace("\n", " ").Trim();
		if (x.Length <= n) return x;
		int c = x.LastIndexOf(' ', n - 1); if (c < n / 2) c = n - 1;
		return x[..c].TrimEnd(' ', ',', ';', '-', ':') + "...";
	}
	private static string PClass(Dictionary<string, string> m)
	{
		string G(string k) => m.TryGetValue(k, out var v) ? v.Trim() : "";
		var kind = G("kind").ToUpperInvariant();
		if (kind == "PURCHASE CHECKPOINT" || kind == "COMPLETE BUILD" || kind == "INTERACTION" || G("feeds").Length > 0) return "BUILD";
		if (kind == "BASELINE" || kind == "ISOLATED ITEM") return "CALIBRATION";
		return "UNKNOWN";
	}
	private static string _stuckNote = ""; private static int _stuckSi = -2; private static long _stuckAt;
	private static string T32(string x) => Trunc(x, 32);
	private static string CpShort() { var c = M("checkpoint"); if (c.Length == 0) return ""; int i = c.IndexOfAny(new[] { ',', '(' }); if (i > 3) c = c[..i]; return Trunc(c.Trim(), 26); }
	private static string StatusTitle() => T32(M("player_title").Length > 0 ? M("player_title") : $"Testing {M("hero", _myHero.ToString())}");
	private static string WhatLine() => T32((M("player_what").Length > 0 ? M("player_what") : "Test running (no description)").Split('|')[0].Trim());
	private static string WhyLine() { var w = M("player_why"); if (PClass(_meta) == "BUILD" && M("feeds").Length > 0) w = "Feeds: " + M("feeds"); return T32(w); }
	private static string PhaseText() => _phase == "finished" ? "Finished" : _everMeasured ? "Measuring" : "Setting up";
	
	private static string PlainFail(string r)
	{
		r = (r ?? "").ToLowerInvariant();
		if (r.Contains("did not run to completion")) return "run did not finish";
		if (r.Contains("unknown op")) return "bad scenario step";
		if (r.Contains("never triggered")) return "item effect never triggered";
		if (r.Contains("readback") || r.Contains("needed >") || r.Contains("needed <") || r.Contains("needed =")) return "setup readback did not match";
		if (r.Contains("verify")) return "setup/activation check failed";
		if (r.Contains("exception")) return "plugin error";
		if (r.Contains("op failed")) return "item was not given";
		return "run was invalid";
	}
	// Why is the current attempt running? New test | Re-run after OUR interruption (not a failure) | Retry after a real failure. Never calls an interruption a retry.
	private static List<string> RunStatusFrames()
	{
		var l = new List<string>();
		try
		{
			var r = _qr; string planned = _runY > 1 ? $"Planned run {_runX} of {_runY}" : "";
			string kind = "new"; int fails = 0; string reason = "";
			var t = r != null ? QFind(r.Id) : null;
			if (t?["log"] is JsonArray la)
			{
				var items = la.OfType<JsonObject>().ToList();
				int ls = items.FindLastIndex(x => TS(x, "kind") == "start");
				fails = items.Count(x => TS(x, "kind") == "invalid");
				for (int i = ls - 1; i >= 0; i--) { var k = TS(items[i], "kind"); if (k == "interrupted" || k == "aborted") { kind = "rerun"; break; } if (k == "invalid" || k == "retry") { kind = "retry"; break; } if (k == "done") break; }
				if (t["lastReasons"] is JsonArray lr && lr.Count > 0) reason = PlainFail(lr[0]?.ToString() ?? "");
			}
			if (kind == "rerun") { l.Add("Re-run: run was interrupted"); l.Add("(not a failure)"); }
			else if (kind == "retry") l.Add(T32($"Retry {fails + 1} of 3: {reason}"));
			else l.Add(planned.Length > 0 ? planned : "New test");
			if (kind != "new" && planned.Length > 0) l.Add(planned);
		}
		catch { l.Add("Test running"); }
		return l;
	}
	private static List<string> StatusFrames()
	{
		var b = new List<string>();
		if (_stuckNote.Length > 0) { b.Add("STUCK - see progress.txt"); return b; }
		b.AddRange(RunStatusFrames()); b.Add(PhaseText());
		if (_nextShort.Length > 0) b.Add(T32(_nextShort));
		return b;
	}
	private static IEnumerable<string> WhatFrames() => (M("player_what").Length > 0 ? M("player_what") : "Test running (no description)").Split('|').Select(x => T32(x.Trim())).Where(x => x.Length > 0);
	// one short frame (title + 2 lines <= 32 chars); line A rotates what/why/expect, line B rotates status/next, every 5 s
	private static string ClassLabel() => M("kind").ToUpperInvariant() switch { "BASELINE" => "Calibration", "ISOLATED ITEM" => M("feeds").Length > 0 ? "Item test (for a build)" : "Calibration: item", "PURCHASE CHECKPOINT" => "Purchase checkpoint", "COMPLETE BUILD" => "Full build", "INTERACTION" => "Interaction test", _ => "" };
	private static string TierName(int b) => b switch { <= 0 => "-", 1 => "U", 3 => "T1", 7 => "T2", 15 => "T3", _ => "b" + b };
	private static List<string> LiveStateFrames()
	{
		var f = new List<string>();
		try
		{
			var me = MyPawn(); if (me == null) return f;
			var its = me.AbilityComponent.Abilities.Where(a => a.IsItem).Select(a => ShortItem(a.AbilityName).Replace('_', ' ')).ToList();
			if (its.Count == 0) f.Add("Items equipped: none");
			else { var cur = "Items: "; foreach (var n in its) { if (cur.Length + n.Length + 2 > 32 && cur != "Items: ") { f.Add(cur.TrimEnd(',', ' ')); cur = "+ "; } cur += n + ", "; } f.Add(cur.TrimEnd(',', ' ')); }
			var sig = new[] { EAbilitySlot.Signature1, EAbilitySlot.Signature2, EAbilitySlot.Signature3, EAbilitySlot.Signature4 };
			f.Add(T32("Ability tiers: " + string.Join(" ", sig.Select(sl => TierName(me.AbilityComponent.Abilities.FirstOrDefault(x => !x.IsItem && x.AbilitySlot == sl)?.UpgradeBits ?? -1)))));
		}
		catch { }
		return f;
	}
	private static (string t, string d) HudFrame(long now)
	{
		var a = new List<string>(WhatFrames()); if (WhyLine().Length > 0) a.Add(WhyLine()); if (M("player_expect").Length > 0) a.Add(T32(M("player_expect")));
		if (ClassLabel().Length > 0) a.Add(T32("Type: " + ClassLabel()));
		if (M("build").Length > 0) a.Add(M("build").StartsWith("none") ? "Build: none (item alone)" : T32("Build: " + M("build")));
		if (CpShort().Length > 0) a.Add(T32("At: " + CpShort()));
		a.AddRange(LiveStateFrames());
		a.Add(M("player_uses").Length > 0 ? T32(M("player_uses")) : T32("Uses: " + M("abilities", "gun only")));
		if (M("miss_on_purpose").Length > 0) a.Add(T32(M("miss_on_purpose")));
		if (M("effect_inactive_on_purpose").Length > 0) a.Add(T32("Effect inactive on purpose"));
		var b = StatusFrames();
		int k = (int)(now / 4000);
		return (StatusTitle(), a[k % a.Count] + "\n" + b[(k / 2) % b.Count]);
	}
	// chat group: short lines (<=32 chars), the group is shown >= 9 s after the previous group
	private static void ChatGroup(params string[] lines)
	{
		if (!DispOn()) return;
		bool head = true;
		foreach (var l in lines) { if (l.Length == 0) continue; if (_chatQ.Count < 16) _chatQ.Enqueue((l, head)); head = false; }
	}
	private static void DispBlocked(JsonObject t, string reason)
	{
		try
		{
			var md = ReadMeta(TS(t, "scenario")); string sh = md.GetValueOrDefault("player_short", TS(t, "id"));
			_hudOverT = T32("Blocked: " + sh); _hudOverD = T32(PlainFail(reason)) + "\nQueue moves to the next test"; _hudOverUntil = Environment.TickCount64 + 12000; _hudAt = 0;
			Log($"DISPLAY BLOCKED {TS(t, "id")}: {reason}");
			ChatGroup(_hudOverT, T32(PlainFail(reason)), "Queue moves to the next test");
		}
		catch { }
	}
	private static string _sig = ""; private static long _forceUntil;
	private static string _hudMode = "announce"; private static long _hudModeAt;
	private static string HudMode()
	{
		long n = Environment.TickCount64; if (n - _hudModeAt < 5000) return _hudMode; _hudModeAt = n;
		try { var f = Path.Combine(RootDir(), "ctl", "hudmode.txt"); _hudMode = File.Exists(f) ? File.ReadAllText(f).Trim().ToLowerInvariant() : "announce"; } catch { _hudMode = "announce"; }
		return _hudMode;
	}
	// Modes (ctl\hudmode.txt, comma list allowed): announce = HudGameAnnouncement re-sent ~2 s; hudmsg = CUserMessageHudMsg; center = CUserMessageTextMsg centre print; worldtext = point_worldtext entity above the enemy (not a HUD element, so boon/level-up/hero-change HUD resets cannot clear it); chat = chat only
	private static void HudShow(string title, string desc, int secs) => HudShowMode(HudMode(), title, desc, secs);
	private static CPointWorldText? _wt; private static string _wtMsg = "";
	private static void HudShowMode(string modes, string title, string desc, int secs)
	{
		var h = Human(); if (h == null || !DispOn()) return;
		foreach (var mode in modes.Split(',', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries))
		{
			try
			{
				if (mode == "chat") continue;
				if (mode == "hudmsg") { var m = new CUserMessageHudMsg { Channel = 3, X = 0.02f, Y = 0.25f, Effect = 0, Message = title + "\n" + desc }; NetMessages.Send(m, h.Recipients); }
				else if (mode == "center") { var m = new CUserMessageTextMsg { Dest = 4 }; m.Param.Add(title + "\n" + desc); NetMessages.Send(m, h.Recipients); }
				else if (mode == "worldtext") WorldText(title + "\n" + desc);
				else { var m = new CCitadelUserMsg_HudGameAnnouncement { TitleLocstring = title, DescriptionLocstring = desc, DurationOverride = secs }; NetMessages.Send(m, h.Recipients); }
				if (++_hudLogN % 15 == 1) Log($"DISPLAY HUD[{mode}] {title} | {desc.Replace("\n", " / ")}");
			}
			catch (Exception e) { Log($"DISPLAY HUD[{mode}] failed: {e.Message}"); }
		}
	}
	private static void WorldTextOff() { try { if (_wt != null && _wt.IsValid) _wt.Remove(); } catch { } _wt = null; _wtMsg = ""; }
	private static void WorldText(string msg)
	{
		var en = EnemyPawn() ?? MyPawn(); if (en == null) return;
		var pos = en.Position + new System.Numerics.Vector3(0, 0, 190f);
		if (_wt == null || !_wt.IsValid)
		{
			float fs = 36f, wu = 0.25f; try { var f = Path.Combine(RootDir(), "ctl", "wt.txt"); if (File.Exists(f)) { var p = File.ReadAllText(f).Split(' ', StringSplitOptions.RemoveEmptyEntries); fs = float.Parse(p[0], CultureInfo.InvariantCulture); wu = float.Parse(p[1], CultureInfo.InvariantCulture); } } catch { }
			_wt = CPointWorldText.Create(msg, pos, fs, wu, "", 255, 255, 80, 255, 1); _wtMsg = msg; Log($"DISPLAY worldtext created size={fs} units={wu} valid={_wt?.IsValid}");
		}
		else { _wt.Teleport(position: pos); if (msg != _wtMsg) { _wt.SetMessage(msg); _wtMsg = msg; } }
	}
	private static int _hudLogN;
	[Command("sbx_rbprobe", Description = "Discover weapon clip/reload schema fields (logs RBPROBE lines)")]
	public void CmdRbProbe(Caller caller) => Run(caller, "sbx_rbprobe", "", () => { var me = MyPawn(); if (me != null) RbProbe(me); else Log("RBPROBE no hero"); });
	[Command("sbx_why", Description = "Show the current experiment's reasoning in chat (short lines)")]
	public void CmdWhy(Caller caller) => Run(caller, "sbx_why", "", () =>
	{
		foreach (var k in new[] { "question", "hypothesis", "alternatives", "tradeoffs", "missing_evidence", "result_says" })
			if (M(k).Length > 0) foreach (var l in Wrap(k.Replace('_', ' ') + ": " + M(k), 32, 5)) ChatGroup2(l);
	});
	private static List<string> Wrap(string text, int w, int max)
	{
		var o = new List<string>(); var cur = "";
		foreach (var word in text.Split(' ', StringSplitOptions.RemoveEmptyEntries))
		{
			if (cur.Length > 0 && cur.Length + 1 + word.Length > w) { o.Add(cur); cur = word; if (o.Count >= max) return o; } else cur = cur.Length == 0 ? word : cur + " " + word;
		}
		if (cur.Length > 0 && o.Count < max) o.Add(cur);
		return o;
	}
	private static void ChatGroup2(string l) { if (_chatQ.Count < 24) _chatQ.Enqueue((l, false)); }

	// ---------------- output ----------------
	private static void Say(string line, bool chat)
	{
		Log("DISPLAY " + (chat ? "CHAT " : "") + line);
		
	}

	private static void DispPhase(string phase, string why = "")
	{
		if (phase == _phase && why == _phaseWhy) return;
		_phase = phase; _phaseWhy = why;
		Say($"PHASE {phase}{(why.Length > 0 ? " - " + why : "")}", false);
	}

	private static string ShortItem(string n) => n.StartsWith("upgrade_") ? n[8..] : n;

	private static string AccText()
	{
		if (M("accmode").Length > 0) return M("accmode") + (M("accwhy").Length > 0 ? " (" + M("accwhy") + ")" : "");
		string hit = _accActive ? $"{_accP * 100:0}% hit" : "100% hit";
		string hd = _accActive ? $"{_headFrac * 100:0}% of hits to head" : "body only";
		return $"{hit}, {hd} - measurement";
	}

	private static string Panel()
	{
		var me = MyPawn();
		string items = "-", bits = "-";
		try
		{
			if (me != null)
			{
				var its = me.AbilityComponent.Abilities.Where(a => a.IsItem).Select(a => ShortItem(a.AbilityName)).ToList();
				items = its.Count == 0 ? "none" : string.Join("+", its);
				var sig = new[] { EAbilitySlot.Signature1, EAbilitySlot.Signature2, EAbilitySlot.Signature3, EAbilitySlot.Signature4 };
				bits = string.Join("/", sig.Select(sl => me.AbilityComponent.Abilities.FirstOrDefault(x => !x.IsItem && x.AbilitySlot == sl)?.UpgradeBits ?? -1));
			}
		}
		catch { }
		string hero = me != null ? me.HeroID.ToString() : "-";
		var sb = new StringBuilder();
		sb.Append($"{hero} vs {_enemyHero} | {M("build", "no build")} | {M("kind", "?")}{(M("checkpoint").Length > 0 ? " @" + M("checkpoint") : "")}\n");
		sb.Append($"WHY: {M("purpose", "?")}\n");
		sb.Append($"ITEMS (read back): {items} | TIERS: {bits}\n");
		sb.Append($"AIM: {AccText()} | USES: {M("abilities", "gun only")}\n");
		string run = _runY > 0 ? $"run {_runX}/{_runY}" : "single run";
		sb.Append($"{run} | {_phase}{(_label != "none" ? " [" + _label + "]" : "")} | {_taskLine}\n");
		int fired = _evCount.Where(k => k.Key.StartsWith("GunFired")).Sum(k => k.Value), cast = _evCount.Where(k => k.Key.StartsWith("AbilityExecuted")).Sum(k => k.Value);
		sb.Append($"MECH: intended {M("mechanics", "none")} -> shots {fired}, hits {_dmgHitsOnEnemy}, abilities executed {cast}{(_hzNote.Length > 0 ? " | " + _hzNote : "")}");
		return sb.ToString();
	}

	// called 1 Hz from QrTick (game thread); cost is measured and logged at scenario end
	private static void DispTick()
	{
		long t0 = System.Diagnostics.Stopwatch.GetTimestamp();
		try
		{
			var h = Human();
			long now = Environment.TickCount64;
			if (_running)
			{
				string p = Panel();
				if (p != _lastPanel) { _lastPanel = p; Log("DISPLAY STATE " + p.Replace("\n", " || ")); }
			}
			// HUD: one short frame re-sent every 2 s so it looks continuous (a single banner only shows a few seconds)
			bool over = now < _hudOverUntil;
			if (_running)
			{
				if (_si != _stuckSi) { _stuckSi = _si; _stuckAt = now; if (_stuckNote.Length > 0) { Log("STUCK cleared: progress resumed"); _stuckNote = ""; } }
				else if (now - _stuckAt > 240000 && _stuckNote.Length == 0) { _stuckNote = $"STUCK: no step progress for 4 min at step {_si} ({_qr?.Id})"; Log("DISPLAY " + _stuckNote); Log("QR STUCK " + _stuckNote); }
			}
			{
				var me0 = MyPawn(); string sig = me0 == null ? "none" : $"{me0.EntityHandle}/{me0.Level}/{me0.HeroID}";
				if (_sig.Length > 0 && sig != _sig) { _forceUntil = now + 8000; _hudAt = 0; Log($"DISPLAY re-assert: pawn/level/hero changed {_sig} -> {sig}"); }
				_sig = sig;
			}
			if (_htStep >= 0) HudTestTick(now);
			else if (over || _running)
			{
				var fr = over ? (_hudOverT, _hudOverD) : HudFrame(now);
				if (now - _hudAt >= (now < _forceUntil ? 1000 : 2000)) { _hudAt = now; HudShow(fr.Item1, fr.Item2, 3); }
			}
			else if (_wt != null) WorldTextOff();
			if (_chatQ.Count > 0)
			{
				var nx = _chatQ.Peek();
				if (now - _chatAt >= (nx.head ? 9000 : 1000))
				{
					_chatAt = now; var l = _chatQ.Dequeue().line;
					if (DispOn() && h != null) { try { Chat.PrintToChat(h, "[Sandbox Tester] " + l); Log("DISPLAY SENT " + l); } catch (Exception e) { Log("DISPLAY chat failed: " + e.Message); } }
				}
			}
		}
		catch (Exception e) { Log("DISPLAY tick failed: " + e.Message); }
		double ms = (System.Diagnostics.Stopwatch.GetTimestamp() - t0) * 1000.0 / System.Diagnostics.Stopwatch.Frequency;
		_dispPerfSum += ms; _dispPerfN++; if (ms > _dispPerfMax) _dispPerfMax = ms;
	}

	private static string ResultLine()
	{
		int fired = _evCount.Where(k => k.Key.StartsWith("GunFired")).Sum(k => k.Value), bhit = _evCount.Where(k => k.Key.StartsWith("BulletHit")).Sum(k => k.Value);
		return $"shots {fired}, bullet hits {bhit}, damage events on target {_dmgHitsOnEnemy}{(_hzStartStacks >= 0 ? ", start stacks " + _hzStartStacks : "")}";
	}

	private static void DispFinish(string why)
	{
		try
		{
			string kind = M("kind", "?").ToUpperInvariant(); ActFinish();
			Log($"DISPLAYPERF ticks={_dispPerfN} avg={(_dispPerfN > 0 ? _dispPerfSum / _dispPerfN : 0):0.000}ms max={_dispPerfMax:0.000}ms");
			Say($"FINISHED: {kind} - {M("question", "?")} -> {ResultLine()} ({why})", false);
			var sum = new List<string>
			{
				"MEASURED: " + ResultLine() + "; verify-pass/fail are in the run log",
				"ASSUMED: " + M("assumed", "none declared"),
				"CALCULATED: " + M("calculated", "none"),
			};
			string concl = M("conclusion", "");
			if (concl.Length == 0 || kind == "ISOLATED ITEM" || kind == "BASELINE")
			{
				string c = concl.Length > 0 ? concl : "INSUFFICIENT EVIDENCE - no decision";
				if (kind == "ISOLATED ITEM") c += " | isolated result: NOT a build verdict (excluded: " + M("excluded", "?") + ")";
				if (kind == "BASELINE") c += " | baseline datum only";
				concl = c;
			}
			sum.Add("CONCLUSION: " + concl);
			if (_myHero == Heroes.Wraith && kind != "COMPLETE BUILD") sum.Add("NOTE: Wraith's real build also has Quicksilver Reload, Mercurial Magnum, Full Auto; magazine/ammo questions need the complete build");
			foreach (var s in sum) Say(s, false);
			{
				int fired = _evCount.Where(k => k.Key.StartsWith("GunFired")).Sum(k => k.Value);
				string cls = PClass(_meta);
				string sh = M("player_short").Length > 0 ? M("player_short") : M("hero", _myHero.ToString()) + " test";
				bool stopped = why.StartsWith("aborted"); _hudOverT = T32((stopped ? "Paused: " : "Done: ") + sh);
				string r1 = stopped ? "Stopped early - will re-run" : T32($"{fired} shots, {_dmgHitsOnEnemy} hits recorded");
				string r2 = stopped ? "(not a failure, not counted)" : M("player_expect").Length > 0 ? T32(M("player_expect")) : "";
				string r3 = cls == "BUILD" && M("kind").ToUpperInvariant() != "INTERACTION" ? (M("conclusion").Length > 0 ? T32(M("conclusion")) : "No build verdict yet") : "Verdict: from analysis";
				_hudOverD = r2.Length > 0 ? r1 + "\n" + r2 : r1 + "\n" + r3; _hudOverUntil = Environment.TickCount64 + 12000; _hudAt = 0;
				ChatGroup(_hudOverT, r1, r2, r3);
			}
			_phase = "finished"; _phaseWhy = why;
		}
		catch (Exception e) { Log("DISPLAY finish failed: " + e.Message); }
	}

	// ---------------- stack tracking (Haze ability_stacking_damage: damage row value = 0.2 per stack, readable only from damage events) ----------------
	private static void HazeStackNote(TakeDamageEvent ev)
	{
		try
		{
			string ab = ev.Info.Ability?.SubclassVData?.Name ?? "";
			if (ab != "ability_stacking_damage") return;
			var a = ev.Info.Attacker; var me = MyPawn(); if (a == null || me == null || a.TeamNum != me.TeamNum) return;
			int st = (int)Math.Round(ev.Info.Damage / 0.2f);
			if (_hzAwaitFirst)
			{
				_hzAwaitFirst = false; _hzStartStacks = st;
				bool wantZero = Regex.IsMatch(M("expectedstate"), @"stacks=0");
				_hzNote = $"Haze stacks at first hit: {st}";
				Log($"STATE {_label} first stacking_damage row => {st} stacks (fresh pawn gives 1)");
				if (wantZero && st > 2) Log($"SC VERIFY {_label} FAIL start-state: Haze stacking_damage already at {st} stacks at the first hit (expected fresh)");
			}
			_hzStacks = st;
		}
		catch { }
	}

	// ---------------- ops: meta / phase / statecheck / runinfo ----------------
	private static bool DisplayOp(Step st, CCitadelPlayerPawn? me, CCitadelPlayerPawn? en, long now)
	{
		switch (st.Op)
		{
			case "meta": return true;   // read up front by ReadMeta
			case "phase": DispPhase(st.A.Length > 0 ? st.A[0] : "?", string.Join(' ', st.A.Skip(1))); return true;
			case "runinfo": if (st.A.Length > 1) { int.TryParse(st.A[0], out _runX); int.TryParse(st.A[1], out _runY); } return true;
			case "statecheck": StateCheck(st, me, en, now); return true;
			case "rb": case "rbprobe": case "rl": case "rot": case "ally": case "allycheck": case "aexec": case "castself": case "eshoot": case "moddump": case "modadd": return ReadbackOp(st, me, now) || AllyOp(st, me, en, now);
		}
		return false;
	}

	// statecheck [wait=<s>] [hardreset=1] [items=none|a,b] [stacks=0] [modsmax=N] [cdready=1] [charges=1]
	// Tokens default to meta expectedstate. Records the start state; differing state => wait (legit expiry), optionally hardreset once, else FAIL (counted by the runner as VERIFY FAIL).
	private static void StateCheck(Step st, CCitadelPlayerPawn? me, CCitadelPlayerPawn? en, long now)
	{
		var kv = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);
		foreach (var t in (M("expectedstate") + " " + string.Join(' ', st.A)).Split(' ', StringSplitOptions.RemoveEmptyEntries)) { int q = t.IndexOf('='); if (q > 0) kv[t[..q]] = t[(q + 1)..]; }
		double wait = kv.TryGetValue("wait", out var ws) ? double.Parse(ws, CultureInfo.InvariantCulture) : 0;
		bool doHard = kv.TryGetValue("hardreset", out var hs) && hs == "1";
		var bad = new List<string>();
		string items = "?", mods = "?", cd = "?", bits = "?";
		try
		{
			if (me == null) bad.Add("no pawn");
			else
			{
				var its = me.AbilityComponent.Abilities.Where(a => a.IsItem).Select(a => a.AbilityName).OrderBy(x => x).ToList();
				items = its.Count == 0 ? "none" : string.Join(",", its);
				var extra = ModNames(me).Where(n => _baseMods == null || !_baseMods.Contains(n)).ToList();
				mods = extra.Count == 0 ? "none" : string.Join(",", extra);
				var sig = new[] { EAbilitySlot.Signature1, EAbilitySlot.Signature2, EAbilitySlot.Signature3, EAbilitySlot.Signature4 };
				var sa = me.AbilityComponent.Abilities.Where(x => !x.IsItem && sig.Contains(x.AbilitySlot)).ToList();
				bits = string.Join("/", sig.Select(sl => sa.FirstOrDefault(x => x.AbilitySlot == sl)?.UpgradeBits ?? -1));
				var busy = sa.Where(x => { try { return x.IsOnCooldown; } catch { return false; } }).Select(x => x.AbilityName).ToList();
				var lowCh = sa.Where(x => { try { return x.MaxCharges > 0 && x.RemainingCharges < x.MaxCharges; } catch { return false; } }).Select(x => x.AbilityName + ":" + x.RemainingCharges + "/" + x.MaxCharges).ToList();
				cd = $"onCooldown=[{string.Join(",", busy)}] chargesNotFull=[{string.Join(",", lowCh)}]";
				if (kv.TryGetValue("items", out var v)) { var want = v == "none" || v == "0" ? "none" : string.Join(",", v.Split(',').Select(x => x.StartsWith("upgrade_") ? x : "upgrade_" + x).OrderBy(x => x)); if (want != items) bad.Add($"items [{items}] != [{want}]"); }
				if (kv.TryGetValue("modsmax", out v) && extra.Count > int.Parse(v)) bad.Add($"extra modifiers {extra.Count} > {v}: {mods}");
				if (kv.TryGetValue("mods", out v) && v == "none" && extra.Count > 0) bad.Add($"unexpected modifiers: {mods}");
				if (kv.TryGetValue("cdready", out v) && v == "1" && busy.Count > 0) bad.Add($"on cooldown: {string.Join(",", busy)}");
				if (kv.TryGetValue("charges", out v) && v == "1" && lowCh.Count > 0) bad.Add($"charges not full: {string.Join(",", lowCh)}");
				if (kv.TryGetValue("bits", out v) && v.Replace(",", "/") != bits) bad.Add($"tiers {bits} != {v}");
				if (en != null && en.Health < en.GetMaxHealth() * 0.85) bad.Add($"target hp {en.Health}/{en.GetMaxHealth()}");
			}
		}
		catch (Exception e) { bad.Add("exception " + e.Message); }
		string rec = $"STATE {_label} items=[{items}] tiers={bits} extraMods=[{mods}] {cd} lastHazeStacks={_hzStacks} targetHp={en?.Health}/{en?.GetMaxHealth()}";
		if (bad.Count == 0)
		{
			Log(rec + " => MATCHES expected"); _startStates.Add(_label + ": " + rec);
			ScLog($"VERIFY {_label} PASS statecheck");
			_hzAwaitFirst = true; _hzStartStacks = -1;
			return;
		}
		if (wait > 0.25)
		{
			Log(rec + " => differs: " + string.Join("; ", bad) + $" - waiting (remaining {wait:0.0}s)");
			var a2 = st.A.Where(x => !x.StartsWith("wait=", StringComparison.OrdinalIgnoreCase)).Concat(new[] { "wait=" + (wait - 0.5).ToString("0.0", CultureInfo.InvariantCulture) }).ToArray();
			_steps.Insert(_si + 1, new Step { Op = "statecheck", A = a2 }); _stepEnd = now + 500; return;
		}
		if (doHard && !st.A.Contains("retried=1"))
		{
			Log(rec + " => differs: " + string.Join("; ", bad) + " - hardreset and re-verify once");
			var a2 = st.A.Where(x => !x.StartsWith("hardreset=")).Concat(new[] { "retried=1" }).ToArray();
			_steps.Insert(_si + 1, new Step { Op = "statecheck", A = a2 });
			_steps.Insert(_si + 1, new Step { Op = "hardreset", A = Array.Empty<string>() });
			return;
		}
		Log(rec); _startStates.Add(_label + ": " + rec + " => FAIL");
		ScLog($"VERIFY {_label} FAIL statecheck: {string.Join("; ", bad)}");
	}
}
