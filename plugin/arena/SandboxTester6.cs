using System.Globalization;
using System.Diagnostics;
using System.Numerics;
using DeadworksManaged.Api;

namespace SandboxTester;

// Logs every hit to a CSV and gives commands to set up test scenarios.
// Every command exists as /name and !name (chat) and dw_name (player console and server console).
// From the server console, pawn commands act on the first connected human player.
public partial class SandboxTester : DeadworksPluginBase
{
	public override string Name => "Sandbox Tester";

	private static readonly object _lock = new();
	private static readonly object _logLock = new();
	private static string _dir = "";
	private static string _file = "";
	private static string _pluginLog = "";
	private static bool _logging = true;
	private static string _label = "none";
	private static long _t0;

	public override void OnLoad(bool isReload)
	{
		try
		{
			_dir = Environment.GetEnvironmentVariable("SBX_LOG_DIR") ?? Path.Combine(Directory.GetCurrentDirectory(), "sbx_logs");
			Directory.CreateDirectory(_dir);
			_file = Path.Combine(_dir, $"damage_{DateTime.Now:yyyyMMdd_HHmmss}.csv");
			_pluginLog = Path.Combine(_dir, "plugin.log");
			_t0 = Environment.TickCount64;
			_logLines = CountLines(_pluginLog);
			StartWriter();
			Write("t_ms,label,victim,victim_team,victim_hp_before,attacker,attacker_team,ability,dmg_type,damage,flags");
			Log($"OnLoad isReload={isReload} csv={_file}");
			
			DumpHeroes(); try { ApplyRules(); } catch (Exception e2) { Log("ApplyRules at load: " + e2.Message); }
			QrLoad(isReload);
		}
		catch (Exception e)
		{
			Console.WriteLine("[SandboxTester] OnLoad failed: " + e);
			LogException("OnLoad", e);
		}
	}

	public override void OnUnload() { Log("OnUnload"); FgStop(); try { QrUnload(); } catch { } _wStop = true; try { _wThread?.Join(1500); } catch { } }

	// ---- async buffered file writer: nothing on the game thread touches the disk or the console ----
	private static readonly System.Collections.Concurrent.ConcurrentQueue<(string path, string text)> _wq = new();
	private static volatile bool _wStop; private static Thread? _wThread;
	private static void StartWriter()
	{
		if (_wThread != null) return;
		_wStop = false;
		_wThread = new Thread(() =>
		{
			var sb = new Dictionary<string, System.Text.StringBuilder>();
			while (true)
			{
				bool any = false;
				while (_wq.TryDequeue(out var it))
				{
					any = true;
					if (!sb.TryGetValue(it.path, out var b)) sb[it.path] = b = new System.Text.StringBuilder();
					b.Append(it.text);
					if (b.Length > 1 << 20) break;
				}
				foreach (var kv in sb) { if (kv.Value.Length == 0) continue; try { File.AppendAllText(kv.Key, kv.Value.ToString()); } catch { } kv.Value.Clear(); }
				if (_wStop && !any && _wq.IsEmpty) break;
				Thread.Sleep(any ? 20 : 120);
			}
		}) { IsBackground = true, Name = "sbx-writer" };
		_wThread.Start();
	}
	internal static void AppendAsync(string path, string text) { if (path.Length == 0) return; _wq.Enqueue((path, text)); }

	private static void Write(string line) => AppendAsync(_file, line + Environment.NewLine);

	// plugin.log: OnLoad, every command call, every exception. Never throws.
	private static void Log(string line)
	{
		if (_pluginLog.Length == 0) return;
		AppendAsync(_pluginLog, $"{DateTime.Now:yyyy-MM-dd HH:mm:ss.fff} {line}{Environment.NewLine}");
		try { QrObserve(line); } catch { }
	}

	private static void LogException(string where, Exception e) => Log($"EXCEPTION in {where}: {e}");

	private static void LogCall(Caller caller, string cmd, string args = "")
	{
		Log($"CMD {cmd} by {(caller.IsConsole ? "Console" : caller.Name)} origin={Origin(caller)}{(args.Length > 0 ? " " + args : "")}");
		var r = _qr; if (r != null && r.Cmds.Count < 300) lock (r) r.Cmds.Add($"{cmd} {args} from {Origin(caller)}");
	}

	private static string Q(string? s) => "\"" + (s ?? "").Replace("\"", "'") + "\"";

	private static int _dbgN;
	public override HookResult OnTakeDamage(TakeDamageEvent ev)
	{
		try
		{
			var v0 = ev.Entity;
			var a0 = ev.Info.Attacker;
			if (v0 != null && a0 != null && v0.DesignerName == "player" && a0.DesignerName.StartsWith("npc_", StringComparison.Ordinal))
				return HookResult.Stop;
		}
		catch { }
if (_running) { TagIncoming(ev); ApplyEnemyResist(ev); CountDamageOnEnemy(ev); HazeStackNote(ev); RangeDmg(ev); }
if (!_logging) return HookResult.Continue;
try
{
var v = ev.Entity;
			var a = ev.Info.Attacker;
			if (_dbgN++ < 12) Log($"DMG victim idx={v.EntityIndex} type={v.GetType().Name} designer={v.DesignerName} team={v.TeamNum} hp={v.Health} infl={ev.Info.Inflictor?.DesignerName} dmg={ev.Info.Damage} flags={ev.Info.DamageFlags}");
			string ability = ev.Info.Ability?.SubclassVData?.Name ?? ev.Info.Ability?.DesignerName ?? "";
			Write(string.Join(",",
				(Environment.TickCount64 - _t0).ToString(CultureInfo.InvariantCulture),
				Q(_label),
				Q(v.DesignerName),
				v.TeamNum.ToString(CultureInfo.InvariantCulture),
				v.Health.ToString(CultureInfo.InvariantCulture),
				Q(a?.DesignerName),
				a != null ? a.TeamNum.ToString(CultureInfo.InvariantCulture) : "",
				Q(ability),
				ev.Info.CitadelDamageType.ToString(),
				ev.Info.Damage.ToString("0.###", CultureInfo.InvariantCulture),
				((ulong)ev.Info.DamageFlags).ToString(CultureInfo.InvariantCulture)));
		}
		catch (Exception e)
		{
			Console.WriteLine("[SandboxTester] hook error: " + e.Message);
			LogException("OnTakeDamage", e);
		}
		return HookResult.Continue;
	}

	// Server console: one line there. Player: their game console (as before) and chat.
	private static void Reply(Caller to, string m, bool chat = true)
	{
		Console.WriteLine("[SandboxTester] " + m);
		if (to.IsConsole) return;
		to.PrintToConsole(m);
		if (chat && !File.Exists(Path.Combine(RootDir(), "ctl", "loud"))) { Log("REPLY (chat suppressed) " + m); return; }
		if (chat) to.Reply(m);
	}

	// The caller's hero pawn; from the server console, the first connected human player's.
	private static CCitadelPlayerPawn? PawnOf(Caller caller)
	{
		var controller = caller.IsConsole
			? Players.GetAll().FirstOrDefault(p => !p.IsBot)
			: caller.Player;
		return controller?.GetHeroPawn();
	}

	// Runs a command body, logging the call and any exception, so a failure is recorded and reported.
	private static void Run(Caller caller, string cmd, string args, Action body)
	{
		OriginBegin(caller, cmd);
		LogCall(caller, cmd, args);
		if (QrGate(caller, cmd, args)) { OriginEnd(); return; }
		try { body(); }
		catch (Exception e)
		{
			LogException(cmd, e);
			Reply(caller, $"{cmd} failed: {e.Message}");
		}
		finally { OriginEnd(); }
	}

	[Command("sbx_mark", Description = "Start a labelled test run: sbx_mark <label>")]
	public void CmdMark(Caller caller, params string[] label) => Run(caller, "sbx_mark", string.Join(' ', label), () =>
	{
		if (label.Length == 0) { Reply(caller, "Usage: sbx_mark <label>"); return; }
		_label = string.Join(' ', label);
		Write($"{Environment.TickCount64 - _t0},{Q("MARK")},{Q(_label)},,,,,,,,");
		Reply(caller, $"label = {_label}");
	});

	[Command("sbx_log", Description = "Turn damage logging on or off: sbx_log true|false")]
	public void CmdLog(Caller caller, bool on) => Run(caller, "sbx_log", on.ToString(), () =>
	{
		_logging = on;
		Reply(caller, $"logging = {on}");
	});

	[Command("sbx_cheats", Description = "Enable sv_cheats on this server")]
	public void CmdCheats(Caller caller) => Run(caller, "sbx_cheats", "", () =>
	{
		Server.ExecuteCommand("sv_cheats 1");
		Reply(caller, "sv_cheats 1");
	});

	[Command("sbx_run", Description = "Run one console command on the server: sbx_run <command> [args...] (a single word may use dashes for spaces)")]
	public void CmdRun(Caller caller, params string[] command) => Run(caller, "sbx_run", string.Join(' ', command), () =>
	{
		if (command.Length == 0) { Reply(caller, "Usage: sbx_run <command> [args...]"); return; }
		// One token keeps the old dash-for-space form; several tokens are joined with spaces as typed.
		string c = command.Length == 1 ? command[0].Replace('-', ' ') : string.Join(' ', command);
		Server.ExecuteCommand(c);
		Reply(caller, $"ran: {c}");
	});

	[Command("sbx_item", Description = "Give an item for free: sbx_item <upgrade_name> [enhanced]")]
	public void CmdItem(Caller caller, string itemName, bool enhanced = false) => Run(caller, "sbx_item", $"{itemName} {enhanced}", () =>
	{
		var pawn = PawnOf(caller);
		if (pawn == null) { Reply(caller, "no hero pawn"); return; }
		var item = pawn.AddItem(itemName, enhanced);
		Reply(caller, item != null ? $"added {itemName}" : $"failed to add {itemName}");
	});

	[Command("sbx_imbue", Description = "Give an item imbued into an ability slot 0-3: sbx_imbue <item> <slot>")]
	public void CmdImbue(Caller caller, string itemName, EAbilitySlot slot) => Run(caller, "sbx_imbue", $"{itemName} {slot}", () =>
	{
		var pawn = PawnOf(caller);
		if (pawn == null) { Reply(caller, "no hero pawn"); return; }
		var r = pawn.TryAddItem(itemName, slot, out _, false);
		Reply(caller, $"{itemName} -> {slot}: {r}");
	});

	[Command("sbx_remove", Description = "Remove an item: sbx_remove <upgrade_name>")]
	public void CmdRemove(Caller caller, string itemName) => Run(caller, "sbx_remove", itemName, () =>
	{
		var pawn = PawnOf(caller);
		if (pawn == null) { Reply(caller, "no hero pawn"); return; }
		Reply(caller, pawn.RemoveItem(itemName) ? $"removed {itemName}" : $"could not remove {itemName}");
	});

	[Command("sbx_souls", Description = "Give souls: sbx_souls [amount]")]
	public void CmdSouls(Caller caller, int amount = 50000) => Run(caller, "sbx_souls", amount.ToString(CultureInfo.InvariantCulture), () =>
	{
		var pawn = PawnOf(caller);
		if (pawn == null) { Reply(caller, "no hero pawn"); return; }
		pawn.ModifyCurrency(ECurrencyType.EGold, amount, ECurrencySource.ECheats, silent: true, forceGain: true);
		Reply(caller, $"gave {amount} souls");
	});

	[Command("sbx_items", Description = "List what the hero currently has")]
	public void CmdItems(Caller caller) => Run(caller, "sbx_items", "", () =>
	{
		var pawn = PawnOf(caller);
		if (pawn == null) { Reply(caller, "no hero pawn"); return; }
		var all = pawn.AbilityComponent.Abilities;
		foreach (var e in all)
			Reply(caller, $"{e.DesignerName}", chat: false);
		if (!caller.IsConsole) caller.Reply($"{all.Count} entries listed in your console");
	});

	[Command("sbx_status", Description = "Show hero, health, item count, logging state and log path")]
	public void CmdStatus(Caller caller) => Run(caller, "sbx_status", "", () =>
	{
		var pawn = PawnOf(caller);
		if (pawn == null)
		{
			Reply(caller, "hero: none (no hero pawn)");
		}
		else
		{
			int items = pawn.AbilityComponent.Abilities.Count(a => a.IsItem);
			Reply(caller, $"hero: {pawn.HeroID}");
			Reply(caller, $"health: {pawn.Health}/{pawn.GetMaxHealth()}");
			Reply(caller, $"items: {items}");
		}
		Reply(caller, $"logging: {_logging} (label {_label})");
		Reply(caller, $"csv: {_file}");
		Reply(caller, $"plugin log: {_pluginLog}");
	});

	[Command("sbx_reset", Description = "Reset hero abilities and items")]
	public void CmdReset(Caller caller) => Run(caller, "sbx_reset", "", () =>
	{
		var pawn = PawnOf(caller);
		if (pawn == null) { Reply(caller, "no hero pawn"); return; }
		pawn.ResetHero(true);
		Reply(caller, "reset");
	});

	[Command("sbx_hurt", Description = "Hit yourself for a set amount, to check the log: sbx_hurt [amount]")]
	public void CmdHurt(Caller caller, int amount = 50) => Run(caller, "sbx_hurt", amount.ToString(CultureInfo.InvariantCulture), () =>
	{
		var pawn = PawnOf(caller);
		if (pawn == null) { Reply(caller, "no hero pawn"); return; }
		pawn.Hurt(amount);
		Reply(caller, $"hurt {amount}");
	});

	[Command("sbx_fake", Description = "Try to add a fake-client dummy and report the slot")]
	public void CmdFake(Caller caller) => Run(caller, "sbx_fake", "", () =>
	{
		int slot = Server.CreateFakeClient("Dummy");
		Reply(caller, $"CreateFakeClient -> slot {slot}");
	});

	// ---- File-queue driver: any *.txt dropped in <log dir>\..\sbx_cmd is run line by line as a server-console
	// command (dw_<line>), then renamed to .done. Lets scripts drive the sandbox without anyone typing in game.
	private static string _cmdDir = "";
	private static int _frames;

	private static string CmdDir()
	{
		if (_cmdDir.Length == 0)
		{
			_cmdDir = Path.Combine(Path.GetDirectoryName(_dir.TrimEnd('\\', '/')) ?? _dir, "sbx_cmd");
			Directory.CreateDirectory(_cmdDir);
		}
		return _cmdDir;
	}

	public override void OnGameFrame(bool simulating, bool firstTick, bool lastTick)
	{
		long _p0 = System.Diagnostics.Stopwatch.GetTimestamp();
		try { FrStatNote(simulating); } catch { }
		try { ScenarioTick(); } catch (Exception ex) { LogException("ScenarioTick", ex); _finishWhy = "EXCEPTION in ScenarioTick: " + ex.Message; _running = false; _aim = false; _fire = false; }
		PerfNote(0, System.Diagnostics.Stopwatch.GetTimestamp() - _p0);
		try { QrTick(); } catch (Exception ex) { LogException("QrTick", ex); }
		if (++_frames % 64 != 0) return;
		if (_pending) { try { SetupStep(); } catch (Exception ex) { LogException("SetupStep", ex); _pending = false; } }
		try
		{
			foreach (var f in Directory.GetFiles(CmdDir(), "*.txt").OrderBy(x => x))
			{
				string[] lines;
				try { lines = File.ReadAllLines(f); } catch { continue; }
				try { File.Move(f, f + ".done", true); } catch { continue; }
				string fname = Path.GetFileName(f); bool anyRefused = false;
				foreach (var raw in lines)
				{
					var line = raw.Trim();
					if (line.Length == 0 || line.StartsWith('#')) continue;
					bool force = false;
					if (line.StartsWith("force ", StringComparison.OrdinalIgnoreCase)) { force = true; line = line[6..].Trim(); }
					string word = line.Split(' ', StringSplitOptions.RemoveEmptyEntries)[0];
					if (_qrLoaded && QActive() && !_qrAllowed.Contains(word) && !force)
					{
						anyRefused = true;
						Log($"QR REFUSED queue-file line '{line}' origin=file:{fname} reason=runner active ({_qrState}); prefix the line with 'force' or run 'sbx_q pause' first");
						var rr = _qr; if (rr != null) lock (rr) rr.Cmds.Add($"REFUSED file {fname}: {line}");
						continue;
					}
					try
					{
						Log("QUEUE " + line);
						if (line.StartsWith("raw ", StringComparison.OrdinalIgnoreCase))
						{
							if (_qrLoaded && QActive()) { Log($"QR FORCED raw '{line}' origin=file:{fname}"); var r2 = _qr; if (r2 != null) lock (r2) r2.Ext.Add("forced raw " + line); }
							Server.ExecuteCommand(line[4..]);
						}
						else { _originFifo.Enqueue((word.ToLowerInvariant(), "file:" + fname, force)); Server.ExecuteCommand("dw_" + line); }
					}
					catch (Exception ex) { LogException("queue-file", ex); }
				}
				if (anyRefused) { try { File.Move(f + ".done", f + ".refused", true); } catch { } }
			}
		}
		catch (Exception e) { LogException("OnGameFrame", e); }
	}

	// Diagnostic: record what the client console / chat sends, so missing chat commands can be explained.
	public override HookResult OnClientConCommand(ClientConCommandEvent args)
	{
		try { Log($"CLIENTCMD {args.Command} {string.Join(' ', args.Args)}"); string who = ""; try { who = args.Controller?.PlayerName ?? ""; } catch { } QrClientCmd(args.Command, string.Join(' ', args.Args), who); } catch { }
		return HookResult.Continue;
	}

	[Command("sbx_ent", Description = "Spawn an entity ahead of you: sbx_ent <designer_name> [team]")]
	public void CmdEnt(Caller caller, string designer, int team = 3) => Run(caller, "sbx_ent", $"{designer} {team}", () =>
	{
		var pawn = PawnOf(caller);
		if (pawn == null) { Reply(caller, "no hero pawn"); return; }
		var e = CBaseEntity.CreateByDesignerName(designer);
		if (e == null) { Reply(caller, $"could not create {designer}"); return; }
		e.TeamNum = team;
		e.Spawn();
		var p = pawn.Position;
		e.Teleport(position: new Vector3(p.X + 350f, p.Y, p.Z + 10f));
		Reply(caller, $"spawned {designer} team {team} idx {e.EntityIndex}");
	});

	public override void OnClientFullConnect(ClientFullConnectEvent args)
	{
		try
		{
			Log($"CONNECT slot {args.Slot}"); _qrConnectAt = Environment.TickCount64;
			Log("CONNECT chat suppressed (quiet)");
			var auto = Path.Combine(Path.GetDirectoryName(_dir.TrimEnd('\\', '/')) ?? _dir, "auto.txt");
			if (File.Exists(auto) && (File.Exists(QPath("PAUSE")) || QActive())) Log("CONNECT auto-setup SKIPPED (queue runner active or PAUSE present: no game-affecting command is issued on connect)");
			else if (File.Exists(auto) && args.Controller is { IsBot: false } hc && hc.PlayerName != "Dummy")
			{
				var w = File.ReadAllText(auto).Split(new[] { ' ', '\r', '\n', ',' }, StringSplitOptions.RemoveEmptyEntries);
				if (w.Length >= 1) StartSetup(w[0], w.Length > 1 ? w[1] : "Haze", args.Controller);
			}
		}
		catch (Exception e) { LogException("OnClientFullConnect", e); }
	}

	[Command("sbx_players", Description = "List every player controller: slot, name, team, bot, hero pawn")]
	public void CmdPlayers(Caller caller) => Run(caller, "sbx_players", "", () =>
	{
		foreach (var c in Players.GetAll())
		{
			var pw = c.GetHeroPawn();
			Reply(caller, $"slot {c.EntityIndex - 1} {c.PlayerName} team {c.TeamNum} bot {c.IsBot} pawn {(pw == null ? "none" : pw.HeroID.ToString() + " hp " + pw.Health)}", chat: false);
		}
	});

	[Command("sbx_dummy", Description = "Make every non-human player an enemy hero: sbx_dummy <Hero> [team]")]
	public void CmdDummy(Caller caller, string hero, int team = 3) => Run(caller, "sbx_dummy", $"{hero} {team}", () =>
	{
		if (!Enum.TryParse<Heroes>(hero, true, out var h)) { Reply(caller, $"unknown hero {hero}"); return; }
		int n = 0;
		foreach (var c in Players.GetAll().Where(x => x.IsBot || x.PlayerName == "Dummy"))
		{
			c.ChangeTeam(team, keepHero: false);
			c.SelectHero(h);
			n++;
			var pw = c.GetHeroPawn();
			Reply(caller, $"{c.PlayerName}: team {c.TeamNum} pawn {(pw == null ? "none" : "ok hp " + pw.Health)}", chat: false);
		}
		Reply(caller, $"dummies set: {n}");
	});

	// ---- one-shot setup: put the human on Amber with a hero, spawn a dummy enemy hero near them in the middle ----
	private static bool _pending;
	private static Heroes _myHero = Heroes.Haze, _enemyHero = Heroes.Haze;
	private static bool _dummyMade, _dummyTeamed;
private static int _setupTries;
private static bool _setupErr;
private static int _verifyOk; private static bool _setupFail;
private static void DumpHeroes()
{
try { File.WriteAllText(Path.Combine(_dir, "hero_enum.txt"), string.Join("\n", Enum.GetValues<Heroes>().Select(h => $"{h} = {(int)h}")) + "\n"); } catch { }
}

	private static long _cacheAt = -1000; private static CCitadelPlayerController? _humanC, _dummyC; private static List<CCitadelPlayerController> _botsC = new();
	private static CCitadelPlayerController? _allyC;
	private static void RefreshCache()
	{
		_allyC = null;
		long now = Environment.TickCount64;
		if (now - _cacheAt < 200) return;
		_cacheAt = now;
		CCitadelPlayerController? h = null, d = null; var bots = new List<CCitadelPlayerController>();
		try
		{
			foreach (var p in Players.GetAll())
			{
				if (p == null) continue;
				if (!p.IsBot && p.PlayerName != "Dummy") { h ??= p; }
				else if (p.PlayerName == "Ally") { _allyC = p; }
				else { bots.Add(p); d ??= p; }
			}
		}
		catch { }
		_humanC = h; _dummyC = d; _botsC = bots;
	}
	internal static void InvalidateCache() { _cacheAt = -1000; }
	private static CCitadelPlayerController? Human() { RefreshCache(); return _humanC; }
	private static CCitadelPlayerController? DummyCtl() { RefreshCache(); return _dummyC; }
	private static List<CCitadelPlayerController> BotList() { RefreshCache(); return _botsC; }

	// ---- perf counters (game-thread time per hook) ----
	private static readonly double[] _perfMax = new double[3]; private static readonly long[] _perfN = new long[3], _perfSlow = new long[3]; private static double _perfSum0;
	private static void PerfNote(int k, long ticks)
	{
		double ms = ticks * 1000.0 / System.Diagnostics.Stopwatch.Frequency;
		_perfN[k]++; if (k == 0) _perfSum0 += ms;
		if (ms > _perfMax[k]) _perfMax[k] = ms;
		if (ms > 20) { _perfSlow[k]++; if (_perfSlow[k] <= 20) Log($"PERF slow hook {k} {ms:0.0} ms"); }
	}
	private static void PerfReport() { Log($"PERF tick n={_perfN[0]} avg={(_perfN[0] > 0 ? _perfSum0 / _perfN[0] : 0):0.00}ms max={_perfMax[0]:0.0}ms slow>20ms={_perfSlow[0]} | usercmd n={_perfN[1]} max={_perfMax[1]:0.0}ms slow={_perfSlow[1]} | abilityAttempt n={_perfN[2]} max={_perfMax[2]:0.0}ms"); Array.Clear(_perfMax); Array.Clear(_perfN); Array.Clear(_perfSlow); _perfSum0 = 0; }

	private static void StartSetup(string hero, string enemy, CCitadelPlayerController? human)
	{
DumpHeroes();
if (!Enum.TryParse(hero, true, out Heroes mh) || !Enum.IsDefined(mh)) { Log($"SETUP ERROR unknown hero '{hero}' (see hero_enum.txt)"); Console.WriteLine($"[SandboxTester] SETUP ERROR unknown hero '{hero}'"); _setupErr = true; return; }
if (!Enum.TryParse(enemy, true, out Heroes eh) || !Enum.IsDefined(eh)) { Log($"SETUP ERROR unknown enemy hero '{enemy}' (see hero_enum.txt)"); Console.WriteLine($"[SandboxTester] SETUP ERROR unknown enemy hero '{enemy}'"); _setupErr = true; return; }
_setupErr = false; _myHero = mh; _enemyHero = eh;
		_pending = true; _dummyMade = false; _dummyTeamed = false; _setupTries = 0; _verifyOk = 0; _setupFail = false;
		if (human != null)
		{
			var hp0 = human.GetHeroPawn();
			if (hp0 != null && hp0.HeroID == _myHero && human.TeamNum == 2) Log("SETUP me already " + _myHero);
			else { human.ChangeTeam(2, keepHero: false); human.SelectHero(_myHero); }
		}
		Log($"SETUP start me={_myHero} enemy={_enemyHero}");
	}

	[Command("sbx_setup", Description = "Auto-setup: sbx_setup <myHero> [enemyHero]")]
	public void CmdSetup(Caller caller, string myHero, string enemyHero = "Haze") => Run(caller, "sbx_setup", $"{myHero} {enemyHero}", () =>
	{
		var h = caller.IsConsole ? Human() : caller.Player;
		StartSetup(myHero, enemyHero, h);
		Reply(caller, $"setup started: you={myHero} enemy={enemyHero}");
	});

	// middle lane, ground height known from the lane trooper spawns
	private static readonly Vector3 MidLane = new Vector3(124f, 1668f, 430f);

	private static Vector3? _arena; private static bool _arenaLoaded;
	private static bool Home(out Vector3 pos)
	{
		if (!_arenaLoaded)
		{
			_arenaLoaded = true;
			try
			{
				var f = Path.Combine(_dir, "arena.txt");
				if (File.Exists(f)) { var t = File.ReadAllText(f).Trim().Split(' '); if (t.Length == 3) { var ci = System.Globalization.CultureInfo.InvariantCulture; _arena = new Vector3(float.Parse(t[0], ci), float.Parse(t[1], ci), float.Parse(t[2], ci)); } }
			}
			catch { }
		}
		if (_arena.HasValue) { pos = _arena.Value; return true; }
		if (OnLaneMap()) { pos = MidLane; return true; }
		pos = default; return false;
	}
	internal static void SetArena(Vector3? v)
	{
		_arena = v; _arenaLoaded = true;
		try
		{
			var f = Path.Combine(_dir, "arena.txt"); var ci = System.Globalization.CultureInfo.InvariantCulture;
			if (v.HasValue) File.WriteAllText(f, v.Value.X.ToString(ci) + " " + v.Value.Y.ToString(ci) + " " + v.Value.Z.ToString(ci)); else File.Delete(f);
		}
		catch { }
	}

	private static bool OnLaneMap()
	{
		try
		{
			var f = Path.Combine(Path.GetDirectoryName(_dir.TrimEnd('\\', '/')) ?? _dir, "map.txt");
			return !File.Exists(f) || File.ReadAllText(f).Trim().Equals("dl_midtown", StringComparison.OrdinalIgnoreCase);
		}
		catch { return true; }
	}

	private static void SetupStep()
	{
		var me = Human();
		var pawn = me?.GetHeroPawn();
		if (me == null || pawn == null) return;
		if (++_setupTries > 2000) { _setupFail = true; _pending = false; Log("SETUP gave up (not verified)"); return; }
		if (pawn.HeroID != _myHero) { if (_setupTries % 50 == 0) Log($"SETUP waiting for my hero pawn ({pawn.HeroID} -> {_myHero})"); return; }
		if (!_dummyMade)
		{
			pawn.ModifyCurrency(ECurrencyType.EGold, 50000, ECurrencySource.ECheats, silent: true, forceGain: true);
			if (Home(out var hp0)) pawn.Teleport(position: hp0);
			if (DummyCtl() == null) Server.CreateFakeClient("Dummy");
			_dummyMade = true;
			return;
		}
		var d = DummyCtl();
		if (d == null) return;
		if (!_dummyTeamed)
		{
			var d0 = d.GetHeroPawn();
			if (!(d0 != null && d0.HeroID == _enemyHero && d.TeamNum == 3)) { d.ChangeTeam(3, keepHero: false); d.SelectHero(_enemyHero); }
			_dummyTeamed = true; return;
		}
		var dp = d.GetHeroPawn();
		if (dp == null || (int)dp.HeroID == 0)
		{
			if (_setupTries % 5 == 0) { Log($"SETUP dummy not ready (pawn {(dp == null ? "null" : "hero0")}), retry select"); d.SelectHero(_enemyHero); try { dp?.ForceRespawn(); } catch { } }
			return;
		}
		// verify BOTH sides are in the arena (a hero swap respawns the pawn at spawn, so the first teleport is not enough)
		bool hasHome = Home(out var hp1);
		var basePos = hasHome ? hp1 : pawn.Position;
		var wantE = new Vector3(basePos.X + _dist, basePos.Y, basePos.Z);
		if (hasHome && (new Vector3(pawn.Position.X - basePos.X, pawn.Position.Y - basePos.Y, 0f).Length() > 25f || Math.Abs(pawn.Position.Z - basePos.Z) > 40f))
		{
			_verifyOk = 0; pawn.Teleport(position: basePos, velocity: Vector3.Zero);
			if (_setupTries % 20 == 0) Log($"SETUP VERIFY moving me to arena (was {pawn.Position})");
			return;
		}
		if ((new Vector3(dp.Position.X - wantE.X, dp.Position.Y - wantE.Y, 0f).Length() > 25f || Math.Abs(dp.Position.Z - wantE.Z) > 40f) && !(dp.Health <= 0))
		{
			var pre = dp.Position; _verifyOk = 0; dp.Teleport(position: wantE, velocity: Vector3.Zero);
			if (_setupTries % 20 == 0) Log($"SETUP VERIFY moving enemy to arena (was {pre}, want {wantE}, dist={_dist}, hp={dp.Health}, idx={dp.EntityIndex}, me={pawn.Position})");
			return;
		}
		if (dp.Health <= 0 || pawn.Health <= 0) { _verifyOk = 0; return; }
		if (++_verifyOk < 5) return;
		_pending = false;
		Log($"SETUP VERIFY ok: me {pawn.HeroID} at {pawn.Position}, enemy {dp.HeroID} at {dp.Position}, arena={(hasHome ? basePos.ToString() : "none")}");
		Log($"SETUP done: dummy team {d.TeamNum} hero {dp.HeroID} hp {dp.Health}");
		Log("enemy dummy placed (chat suppressed: quiet display)");
	}

	[Command("sbx_tp", Description = "Teleport yourself: sbx_tp <x> <y> <z>")]
	public void CmdTp(Caller caller, float x, float y, float z) => Run(caller, "sbx_tp", $"{x} {y} {z}", () =>
	{
		var pawn = PawnOf(caller);
		if (pawn == null) { Reply(caller, "no hero pawn"); return; }
		pawn.Teleport(position: new Vector3(x, y, z));
		Reply(caller, "teleported");
	});

	[Command("sbx_pos", Description = "Log where you and every named entity are: sbx_pos [designer_name]")]
	public void CmdPos(Caller caller, string designer = "") => Run(caller, "sbx_pos", designer, () =>
	{
		var pawn = PawnOf(caller);
		if (pawn != null) Reply(caller, $"you at {pawn.Position}", chat: false);
		if (designer.Length > 0)
		{
			int n = 0;
			foreach (var e in Entities.ByDesignerName(designer)) { Reply(caller, $"{designer} #{e.EntityIndex} at {e.Position} team {e.TeamNum}", chat: false); if (++n >= 8) break; }
			Reply(caller, $"{designer}: {n} found", chat: false);
		}
	});

	[Command("sbx_build", Description = "Rebuild this plugin from source and hot-reload it")]
	public void CmdBuild(Caller caller) => Run(caller, "sbx_build", "", () =>
	{
		var refuse = MaintBuildRefusal();
		if (refuse != null) { MaintLog("sbx_build REFUSED: " + refuse); Reply(caller, "REFUSED sbx_build: " + refuse); return; }
		MaintLog("sbx_build started (runner idle, window ok)");
		var root = Environment.GetEnvironmentVariable("SBX_ROOT") ?? @"E:\deadworks-server";
		var man = Environment.GetEnvironmentVariable("SBX_MAN") ?? @"F:\steamlibrary\steamapps\common\deadlock\game\bin\win64\managed";
		Task.Run(() =>
		{
			try
			{
				var outDir = Path.Combine(root, "SandboxTester", "out2");
				if (Directory.Exists(outDir)) Directory.Delete(outDir, true);
				var psi = new ProcessStartInfo("dotnet", $"build \"{Path.Combine(root, "SandboxTester", "SandboxTester.csproj")}\" -c Release -nologo -p:ManagedDir=\"{man}\" -o \"{outDir}\"")
				{ RedirectStandardOutput = true, RedirectStandardError = true, UseShellExecute = false, CreateNoWindow = true };
				using var pr = Process.Start(psi)!;
				var o = pr.StandardOutput.ReadToEnd() + pr.StandardError.ReadToEnd();
				pr.WaitForExit();
				File.WriteAllText(Path.Combine(_dir, "build_plugin.txt"), o);
				var dll = Path.Combine(outDir, "SandboxTester.dll");
				if (pr.ExitCode == 0 && File.Exists(dll))
				{
					File.Copy(dll, Path.Combine(man, "plugins", "SandboxTester.dll"), true);
					Log("BUILD ok, copied (hot reload expected)");
				}
				else Log("BUILD FAILED, see build_plugin.txt");
			}
			catch (Exception e) { LogException("sbx_build", e); }
		});
		Reply(caller, "build started, see plugin.log");
	});

	// Sandbox rules, set on every map load (cfg-set values reset on load): no lane troopers, no neutrals.
	private static void ApplyRules()
	{
		foreach (var (n, v) in new (string, int)[] {
			("citadel_trooper_spawn_enabled", 0), ("citadel_npc_spawn_enabled", 0), ("citadel_allow_purchasing_anywhere", 1),
			("citadel_allow_duplicate_heroes", 1), ("citadel_start_players_on_zipline", 0), ("citadel_player_spawn_time_max_respawn_time", 3) })
		{
			try { ConVar.Find(n)?.SetInt(v); } catch (Exception e) { Log($"convar {n}: {e.Message}"); }
		}
		Server.ExecuteCommand("sv_cheats 1");
		foreach (var c in new[] { "citadel_bot_practice_opponent hero_haze", "citadel_spawn_practice_bots 1", "citadel_spawn_practice_bots_count 1",
			"citadel_bot_brain_disable_attacks true", "citadel_bot_brain_disable_movement true" })
			Server.ExecuteCommand(c);
		Log("RULES applied");
	}

	public override void OnStartupServer()
	{
		try { ApplyRules(); } catch (Exception e) { LogException("OnStartupServer", e); }
	}

	public override void OnEntitySpawned(EntitySpawnedEvent e)
	{
		try { if (e.Entity.DesignerName is "npc_trooper" or "npc_trooper_boss") e.Entity.Remove(); } catch { }
	}
}
