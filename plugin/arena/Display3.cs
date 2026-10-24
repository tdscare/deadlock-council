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
	private static readonly string[] MetaKinds = { "BASELINE", "ISOLATED ITEM", "PURCHASE CHECKPOINT", "COMPLETE BUILD" };
	private static Dictionary<string, string> _meta = new(StringComparer.OrdinalIgnoreCase);
	private static string _phase = "idle", _phaseWhy = "";
	private static int _runX, _runY;
	private static string _lastPanel = "", _taskLine = "";
	private static long _hudAt, _hudForce, _chatAt;
	private static readonly Queue<string> _chatQ = new();
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
		if (!MetaKinds.Contains(kind)) return "meta kind missing/invalid (BASELINE | ISOLATED ITEM | PURCHASE CHECKPOINT | COMPLETE BUILD)";
		foreach (var k in new[] { "question", "purpose", "mechanics", "expectedstate" }) if (G(k).Length < 3) return $"meta {k} missing";
		if (kind == "ISOLATED ITEM" && G("excluded").Length < 10) return "ISOLATED ITEM must declare `meta excluded <what is excluded and why>`";
		if ((kind == "COMPLETE BUILD" || kind == "PURCHASE CHECKPOINT") && (G("build").Length == 0 || G("checkpoint").Length == 0)) return $"{kind} must declare meta build and meta checkpoint";
		if (kind == "BASELINE" && !Regex.IsMatch(G("expectedstate"), @"items=(0|none)")) return "BASELINE expectedstate must contain items=none";
		return null;
	}

	private static string M(string k, string d = "") => _meta.TryGetValue(k, out var v) && v.Length > 0 ? v : d;

	private static void DispStartScenario(string name, string origin)
	{
		_meta = ReadMeta(name); _phase = "setup"; _phaseWhy = ""; _runX = _runY = 0; _lastPanel = ""; _startStates.Clear(); _hzStacks = _hzStartStacks = -1; _hzAwaitFirst = false;
		var rs = M("runs"); if (rs.Contains('/')) { var p = rs.Split('/'); int.TryParse(p[0], out _runX); int.TryParse(p[1], out _runY); }
		_dispPerfSum = _dispPerfMax = 0; _dispPerfN = 0;
		Say($"{M("hero", _myHero.ToString())} - {M("checkpoint", "no checkpoint")} - {M("kind", "?").ToLowerInvariant()}: {M("question", "(no question declared)")} (build: {M("build", "none")}; items: {M("items", "none")}; why: {M("purpose", "?")})", true);
	}
	private static string _nextNote = "", _nextNoteFor = "";
	private static void DispMarkNext(Step st)
	{
		try
		{
			var l = string.Join(' ', st.A);
			if (l == "none" || l.Length == 0) { DispPhase("idle-between-blocks"); return; }
			DispPhase("measure", l);
			var me = MyPawn(); string items = "?";
			try { if (me != null) { var its = me.AbilityComponent.Abilities.Where(a => a.IsItem).Select(a => ShortItem(a.AbilityName)).ToList(); items = its.Count == 0 ? "no items" : string.Join("+", its); } } catch { }
			Say($"{(me != null ? me.HeroID.ToString() : "?")} - now testing [{l}] - {M("purpose", M("question", "?"))} | items read back: {items} | aim: {AccText()} | run {(_runY > 0 ? _runX + "/" + _runY : "1/1")}", true);
		}
		catch { }
	}
	private static string RunEnv() { try { var f = Path.Combine(RootDir(), "ctl", "env.txt"); return File.Exists(f) ? File.ReadAllText(f).Trim() : "ENV: unlabelled"; } catch { return "ENV: unlabelled"; } }
	private static void DispNextLine(JsonObject? done)
	{
		try
		{
			var nx = QTasks().OfType<JsonObject>().FirstOrDefault(x => TS(x, "state") == "pending");
			if (nx == null) { Say("NEXT: queue empty", true); return; }
			var md = ReadMeta(TS(nx, "scenario"));
			Say($"NEXT: {md.GetValueOrDefault("kind", "?")} {TS(nx, "id")} - {md.GetValueOrDefault("question", "(no question)")} because {md.GetValueOrDefault("purpose", "it is the next pending task")}", true);
		}
		catch { }
	}


	// ---------------- output ----------------
	private static void Say(string line, bool chat)
	{
		Log("DISPLAY " + (chat ? "CHAT " : "") + line);
		if (chat && DispOn()) { if (_chatQ.Count < 12 && !_chatQ.Contains(line)) _chatQ.Enqueue(line); }
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
			if (_running || _chatQ.Count > 0)
			{
				string p = _running ? Panel() : _lastPanel;
				long now = Environment.TickCount64;
				if (_running && p != _lastPanel) { _lastPanel = p; Log("DISPLAY STATE " + p.Replace("\n", " || ")); }
				if (_chatQ.Count > 0 && now - _chatAt >= 1500)
				{
					_chatAt = now; var l = _chatQ.Dequeue();
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
			string kind = M("kind", "?").ToUpperInvariant();
			Log($"DISPLAYPERF ticks={_dispPerfN} avg={(_dispPerfN > 0 ? _dispPerfSum / _dispPerfN : 0):0.000}ms max={_dispPerfMax:0.000}ms");
			Say($"FINISHED: {kind} - {M("question", "?")} -> {ResultLine()} ({why})", true);
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
			foreach (var s in sum) Say(s, s.StartsWith("CONCLUSION"));
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
