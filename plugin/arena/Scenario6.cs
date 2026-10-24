using System.Globalization;
using System.Numerics;
using DeadworksManaged.Api;

namespace SandboxTester;

// Scenario engine: runs a text script (one step per line) that sets up a test and drives the human player's
// aim and buttons through the usercmd hook, so a test needs nobody at the keyboard.
public partial class SandboxTester
{
	private sealed class Step { public string Op = ""; public string[] A = Array.Empty<string>(); }

	private static readonly List<Step> _steps = new();
	private static int _si = -1;
	private static long _stepEnd;
	private static bool _running, _waitSetup;
	private static string _scName = "";
	private static bool _aim, _fire;
	private static InputButton _forced;
	private static long _forcedUntil;
	private static long _lastSample;
	private static string _samples = "";

	private static string RootDir() => Path.GetDirectoryName(_dir.TrimEnd('\\', '/')) ?? _dir;

	private static void ScLog(string m) { Log("SC " + m); }

	[Command("sbx_scenario", Description = "Run scenarios\\<name>.txt: sbx_scenario <name> [force]")]
	public void CmdScenario(Caller caller, string name, string opt = "") => Run(caller, "sbx_scenario", name + (opt.Length > 0 ? " " + opt : ""), () =>
	{
		if (!StartScenario(name, out var err, Origin(caller))) { Reply(caller, err); return; }
		Reply(caller, $"scenario {name} started");
	});

	private static bool StartScenario(string name, out string err, string origin)
	{
		err = "";
		var f = Path.Combine(RootDir(), "scenarios", name + ".txt");
		if (!File.Exists(f)) { err = $"no such scenario file {f}"; return false; }
		_steps.Clear();
		foreach (var raw in File.ReadAllLines(f))
		{
			var line = raw.Trim();
			int h = line.IndexOf('#');
			if (h >= 0) line = line[..h].Trim();
			if (line.Length == 0) continue;
			var w = line.Split(' ', StringSplitOptions.RemoveEmptyEntries);
			_steps.Add(new Step { Op = w[0].ToLowerInvariant(), A = w[1..] });
		}
		_scName = name;
		_samples = Path.Combine(_dir, $"samples_{name}_{DateTime.Now:HHmmss}.csv");
		File.WriteAllText(_samples, "t_ms,label,my_hp,my_max,enemy_hp,enemy_max\n");
		_si = -1; _stepEnd = 0; _waitSetup = false; _running = true; _aim = false; _fire = false; _finishWhy = "";
		RealismReset();
		DispStartScenario(name, origin);
		ScLog($"scenario {name} started, {_steps.Count} steps origin={origin}");
		return true;
	}

	[Command("sbx_stop", Description = "Stop the running scenario")]
	public void CmdStop(Caller caller) => Run(caller, "sbx_stop", "", () =>
	{
		_finishWhy = "stopped by operator"; _running = false; _aim = false; _fire = false; _forced = InputButton.None;
		ScLog("stopped");
		Reply(caller, "stopped");
	});

	private static double Num(string[] a, int i, double d) => a.Length > i && double.TryParse(a[i], NumberStyles.Float, CultureInfo.InvariantCulture, out var v) ? v : d;

	private static CCitadelPlayerPawn? MyPawn() => Human()?.GetHeroPawn();
	private static long _enAt; private static CCitadelPlayerPawn? _enP;
	private static CCitadelPlayerPawn? EnemyPawn()
	{
		long nowE = Environment.TickCount64;
		if (_enP != null && nowE - _enAt < 30) { try { if (_enP.Health > 0) return _enP; } catch { } }
		_enAt = nowE; _enP = EnemyPawn0(); return _enP;
	}
	private static CCitadelPlayerPawn? EnemyPawn0()
	{
		var me = MyPawn(); var main = DummyCtl()?.GetHeroPawn();
		if (me == null) return main;
		CCitadelPlayerPawn? best = null; float bd = float.MaxValue;
		try
		{
			if (_layOn) { var p0 = Group().FirstOrDefault()?.GetHeroPawn(); if (p0 != null && p0.Health > 0 && (int)p0.HeroID != 0) return p0; }   // layouts: always aim at enemy 0 (the primary target), not the nearest
			foreach (var c in Group().Take(Math.Max(1, _nEn)))
			{
				var p = c.GetHeroPawn(); if (p == null || p.Health <= 0 || (int)p.HeroID == 0) continue;
				float d = (p.Position - me.Position).Length();
				if (d < bd) { bd = d; best = p; }
			}
		}
		catch { }
		return best ?? main;
	}

	private static void Finish(string why)
	{
_finishWhy = why;
RealismSummary(); PerfReport(); UcStatReport("scenario-end"); DispFinish(why); _lowPct = 0; _inKind = ""; _accActive = false; _accP = 1; _headFrac = 1; _eFloor = 0.9; _eHp = 0;
_running = false; _aim = false; _fire = false; _forced = InputButton.None;
Write($"{Environment.TickCount64 - _t0},{Q("DONE")},{Q(_scName)},,,,,,,,");
		ScLog($"scenario {_scName} finished: {why}");
	}

	// aim point = enemy feet + (0,0,55+_aimU) + right*_aimR (units, distance independent); returns false if too close
	private static float _aimR, _aimU;
	private static bool AimAngles(CCitadelPlayerPawn me, CCitadelPlayerPawn en, out float pitch, out float yaw)
	{
		pitch = 0; yaw = 0;
		var f = me.Position + new Vector3(0, 0, 60);
		var t = en.Position + new Vector3(0, 0, 55 + _aimU);
		var h = new Vector3(t.X - f.X, t.Y - f.Y, 0); float hl = h.Length();
		if (hl > 1f) { h /= hl; t += new Vector3(h.Y, -h.X, 0) * _aimR; }
		var d = t - f; float l = d.Length();
		if (l <= 1f) return false;
		yaw = (float)(Math.Atan2(d.Y, d.X) * 180.0 / Math.PI);
		pitch = (float)(-Math.Asin(d.Z / l) * 180.0 / Math.PI);
		if (_accActive && _missDown) pitch = 89f - (_offPitch + _accPitch);
		return true;
	}

	private static long _lastCam; private static int _camN; private static float _offYaw = 0f, _offPitch = 0f;
	private static void ScenarioTick()
	{
		if (!_running) return;
		long now = Environment.TickCount64;
		var me = MyPawn();
		var en = EnemyPawn();

		// samples every 250 ms
		if (_samples.Length > 0 && now - _lastSample >= 250 && me != null)
		{
			_lastSample = now;
			try
			{
				AppendAsync(_samples, string.Join(",",
					(now - _t0).ToString(CultureInfo.InvariantCulture), Q(_label),
					me.Health.ToString(CultureInfo.InvariantCulture), me.GetMaxHealth().ToString(CultureInfo.InvariantCulture),
					en != null ? en.Health.ToString(CultureInfo.InvariantCulture) : "", en != null ? en.GetMaxHealth().ToString(CultureInfo.InvariantCulture) : "") + "\n");
			}
			catch { }
		}
		// keep the target alive; keep the player from dying mid-test
RealismTick(now, me, en);
ActSample(now, me);
if (me != null && me.Health > 0 && _lowPct <= 0 && _inKind.Length == 0 && me.Health < me.GetMaxHealth() * 0.15) me.Health = me.GetMaxHealth();

		// steer the real client camera at the target (usercmd edits alone are overridden by the client)
		if (_aim && me != null && en != null && now - _lastCam >= (_accActive ? 60 : 100))
		{
			_lastCam = now;
			try
			{
				if (AimAngles(me, en, out float pt, out float yw))
				{
Human()?.SetCameraAngles(pt + _offPitch + _accPitch, yw + _offYaw + _accYaw);
				}
			}
			catch (Exception e) { LogException("cam", e); }
		}
		if (_waitSetup)
		{
			if (!_pending) { _waitSetup = false; _stepEnd = now; if (_setupFail) { Finish("setup verify failed: characters not confirmed in the arena"); return; } }
			else if (now > _stepEnd) { Finish("setup timed out"); return; }
			return;
		}
		if (_si >= 0 && now < _stepEnd) return;

		_aim = false; _fire = false;
		_si++;
		if (_si >= _steps.Count) { Finish("end of script"); return; }
		var st = _steps[_si];
		ScLog($"step {_si}: {st.Op} {string.Join(' ', st.A)}");
		_stepEnd = now;
		switch (st.Op)
		{
			case "setup":
StartSetup(st.A.Length > 0 ? st.A[0] : "Haze", st.A.Length > 1 ? st.A[1] : "Haze", Human());
if (_setupErr) { Finish("setup: unknown hero name, nothing run (valid names in sbx_logs\\hero_enum.txt)"); break; }
_waitSetup = true; _stepEnd = now + 240000;
				break;
			case "clear":
				if (me != null)
					foreach (var a in me.AbilityComponent.Abilities.Where(x => x.IsItem).ToList())
						try { bool ok = me.RemoveItem(a.AbilityName); if (!ok) ScLog($"remove failed {a.AbilityName}"); } catch { }
				break;
			case "give":
				if (me != null && st.A.Length > 0)
				{
					var it = me.AddItem(st.A[0], st.A.Length > 1 && st.A[1] == "enhanced");
					ScLog(it != null ? $"gave {st.A[0]}" : $"FAILED to give {st.A[0]}");
				}
				break;
			case "imbue":
				if (me != null && st.A.Length > 1 && Enum.TryParse<EAbilitySlot>(st.A[1], true, out var sl))
					ScLog($"imbue {st.A[0]} -> {sl}: {me.TryAddItem(st.A[0], sl, out _, false)}");
				break;
			case "souls":
				me?.ModifyCurrency(ECurrencyType.EGold, (int)Num(st.A, 0, 50000), ECurrencySource.ECheats, silent: true, forceGain: true);
				break;
			case "mark":
				UcStatReport(_label);
				DispMarkNext(st);
				_label = string.Join(' ', st.A);
				try { if (me != null) ScLog($"ITEMS@{_label}: maxhp={me.GetMaxHealth()} " + string.Join(",", me.AbilityComponent.Abilities.Where(x => x.IsItem).Select(x => x.AbilityName))); } catch { }
				Write($"{now - _t0},{Q("MARK")},{Q(_label)},,,,,,,,");
				break;
			case "wait":
				_stepEnd = now + (long)(Num(st.A, 0, 1) * 1000);
				break;
			case "aimoff":
				_offYaw = (float)Num(st.A, 0, 0); _offPitch = (float)Num(st.A, 1, 0);
				break;
			case "aim":
				_aim = true; _stepEnd = now + (long)(Num(st.A, 0, 1) * 1000);
				break;
			case "fire":
				_aim = true; _fire = true; _stepEnd = now + (long)(Num(st.A, 0, 5) * 1000);
				break;
			case "cast":
				_aim = true;
				_forced = st.A.Length > 0 ? CastButton(st.A[0]) : InputButton.None;
				_forcedUntil = now + 350;
				_stepEnd = now + (long)(Num(st.A, 1, 1.0) * 1000);
				break;
case "hold":
_aim = true;
_forced = st.A.Length > 0 ? CastButton(st.A[0]) : InputButton.None;
_forcedUntil = now + (long)(Num(st.A, 1, 1.0) * 1000);
_stepEnd = _forcedUntil + 150;
break;
case "unlock":
				if (me != null)
					foreach (var a in me.AbilityComponent.Abilities.Where(x => !x.IsItem).ToList())
						try { int b0 = a.UpgradeBits; a.UpgradeBits = (int)Num(st.A, 0, 7); ScLog($"unlock {a.AbilityName} {b0} -> {a.UpgradeBits}"); } catch (Exception e) { ScLog("unlock fail " + e.Message); }
				break;
			case "fetch":
				// bring the enemy bot to me (350u ahead on +x), full health, and kick any other bots
				if (me != null && en != null)
				{
					if (st.A.Length > 0) _dist = (float)Num(st.A, 0, 350);
					en.Teleport(me.Position + new Vector3(_dist, 0f, 0f), velocity: Vector3.Zero);
en.Health = _eHp > 0 ? _eHp : en.GetMaxHealth();
EnemiesMaintain(now, true);
					ScLog($"fetched enemy to {en.Position} me {me.Position}"); if (_nEn <= 1) { _fvAt = now + 300; _fvTries = 0; }
				}
				break;
			case "flex":
				Server.ExecuteCommand("citadel_unlock_flex_slots");
				break;
			case "raw":
				Server.ExecuteCommand(string.Join(' ', st.A));
				break;
			case "heal":
				if (me != null) me.Health = me.GetMaxHealth();
				if (en != null) en.Health = en.GetMaxHealth();
				break;
			case "hurtme":
				me?.Hurt((int)Num(st.A, 0, 300));
				break;
			case "end":
				Finish("end step");
				break;
			default:
if (!RealismOp(st, me, en, now) && !DisplayOp(st, me, en, now)) ScLog($"unknown op {st.Op}");
				break;
		}
	}

	private static InputButton CastButton(string s) => s.ToLowerInvariant() switch
	{
		"1" or "a1" => InputButton.Ability1,
		"2" or "a2" => InputButton.Ability2,
		"3" or "a3" => InputButton.Ability3,
		"4" or "a4" => InputButton.Ability4,
		"i1" => InputButton.Item1,
		"i2" => InputButton.Item2,
		"i3" => InputButton.Item3,
		"i4" => InputButton.Item4,
		"i5" => InputButton.Item5,
		"reload" or "r" => InputButton.Reload,
		"jump" => InputButton.Jump,
		"duck" => InputButton.Duck,
		"alt" => InputButton.AltCast,
		"zip" => InputButton.Zipline,
		"melee" => InputButton.Attack2,
		_ => InputButton.None,
	};

	private static int _abSeen;

	public override void OnAbilityAttempt(AbilityAttemptEvent args)
	{
		if (!_running) return;
		var me = Human();
		if (me == null || args.PlayerSlot != me.EntityIndex - 1) return;
		InputButton f = InputButton.None;
		if (_fire) f |= InputButton.Attack;
		if (_forced != InputButton.None && Environment.TickCount64 < _forcedUntil) f |= _forced;
		f |= SchedNow();
		if (f != InputButton.None)
		{
			args.Force(f);
		}
	}

	private static int _ucSeen, _ucAimed;

	public override void OnProcessUsercmds(ProcessUsercmdsEvent args)
	{
		long _u0 = System.Diagnostics.Stopwatch.GetTimestamp();
		try { UcStatNote(args); } catch { }
		try { UcBody(args); } finally { PerfNote(1, System.Diagnostics.Stopwatch.GetTimestamp() - _u0); }
	}

	private static void UcBody(ProcessUsercmdsEvent args)
	{
		if (!_running || !_aim) return;
		try
		{
			var me = Human();
			if (me == null || args.PlayerSlot != me.EntityIndex - 1) return;
			var mp = me.GetHeroPawn();
			var ep = EnemyPawn();
			if (mp == null || ep == null) return;
			if (!AimAngles(mp, ep, out float pitch, out float yaw)) return;
			foreach (var cmd in args.Usercmds)
			{
				cmd.Base ??= new CBaseUserCmdPB();
cmd.Base.Viewangles = new CMsgQAngle { X = pitch + _offPitch + _accPitch, Y = yaw + _offYaw + _accYaw, Z = 0 };
if (_forced != InputButton.None && Environment.TickCount64 < _forcedUntil) { cmd.Base.ButtonsPb ??= new CInButtonStatePB(); cmd.Base.ButtonsPb.Buttonstate1 |= (ulong)_forced; }
{ var sq = SchedNow(); if (sq != InputButton.None) { cmd.Base.ButtonsPb ??= new CInButtonStatePB(); cmd.Base.ButtonsPb.Buttonstate1 |= (ulong)sq; } }
bool mv = Environment.TickCount64 < _moveUntil;
cmd.Base.Forwardmove = mv ? _moveF : 0;
				cmd.Base.Leftmove = mv ? _moveL : 0;
				if (_fire)
				{
					cmd.Base.ButtonsPb ??= new CInButtonStatePB();
					cmd.Base.ButtonsPb.Buttonstate1 |= (ulong)InputButton.Attack;
				}
			}
		}
		catch (Exception e) { LogException("OnProcessUsercmds", e); }
	}

	[Command("sbx_probe", Description = "Dump dummy state and test Hurt on it")]
	public void CmdProbe(Caller caller) => Run(caller, "sbx_probe", "", () =>
	{
		var en = EnemyPawn(); var me = MyPawn();
		if (en == null) { Log("PROBE no enemy"); return; }
		Log($"PROBE enemy idx={en.EntityIndex} designer={en.DesignerName} team={en.TeamNum} hp={en.Health} life={en.LifeState} flags={en.Flags} pos={en.Position}");
		if (me != null) Log($"PROBE me idx={me.EntityIndex} designer={me.DesignerName} team={me.TeamNum} flags={me.Flags}");
		foreach (var (n, p) in new[] { ("enemy", (CBaseEntity?)en), ("me", me) })
		{
			var c = p?.Collision;
			if (c == null) { Log($"PROBE {n} collision null"); continue; }
			Log($"PROBE {n} grp={c.CollisionGroup} solid={c.SolidType} sflags={c.SolidFlags} as={c.InteractsAs} with={c.InteractsWith} excl={c.InteractsExclude} mins={c.Mins} maxs={c.Maxs}");
		}
		double h0 = en.Health;
		en.Hurt(100, me);
		Log($"PROBE hurt100 hp {h0} -> {en.Health}");
	});
}
