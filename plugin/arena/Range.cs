using System.Globalization;
using System.Numerics;
using DeadworksManaged.Api;

namespace SandboxTester;

// Range / multi-target / moving-target support (generic, no per-item code). Field names are documented in council/sandbox/RANGE_FIELDS.md.
//  ops:  layout <n> <dist> <spacing> [ring|line]      n enemies: enemy 0 at <dist> units straight ahead of the player; others at <spacing> units from enemy 0 (ring around it, or a line sideways). Auto-verifies (layoutcheck).
//        layoutcheck [tol] [try]                       VERIFY 3D distance of enemy 0 and spacing of the others; re-places up to 6x; else FAIL (invalid run). Writes RANGE/LAYOUT lines (measured block).
//        rng <dist> [tol]                              single-target distance block: place enemy 0 at <dist>, verify horizontal+3D distance within tol (default 20u), else FAIL.
//        strafe <amp> <periodSec> [all]                move enemy 0 (all=every active enemy) left-right sinusoid, +-amp units, teleport-driven (engine bots do not walk). strafe off stops.
//        rngreset                                      zero the per-target damage/hit tally and shot/hit counters
//        rngreport <label>                             per-target report since the last rngreset: primary vs secondary damage, hits, lethal hits, gun shots / bullet hits (hit rate), 3D distances. Lines start with "RANGE ".
public partial class SandboxTester
{
	private static bool _layOn; private static int _layN = 1; private static float _laySp = 250f; private static string _layShape = "ring";
	private static bool _strOn, _strAll; private static float _strAmp, _strPer = 3f; private static long _strT0, _strLast;
	private static int _rngShots0, _rngHits0; private static long _rngT0;
	private sealed class TgtTally { public double Dmg; public int Hits, Lethal; public Dictionary<string, double> ByAbility = new(); public long First; }
	private static readonly Dictionary<int, TgtTally> _tally = new();

	internal static Vector3 StrafeOff(long now, bool first)
	{
		if (!_strOn || (!first && !_strAll)) return Vector3.Zero;
		double t = (now - _strT0) / 1000.0;
		return new Vector3(0f, (float)(_strAmp * Math.Sin(2 * Math.PI * t / Math.Max(0.2, _strPer))), 0f);
	}
	internal static Vector3 LayoutOff(int i)
	{
		int k = i - 1, m = Math.Max(1, _layN - 1);
		if (_layShape == "line") { int step = k / 2 + 1; return new Vector3(0f, (k % 2 == 0 ? 1 : -1) * step * _laySp, 0f); }
		double ang = Math.PI / 2 + 2 * Math.PI * k / m;
		return new Vector3((float)(Math.Cos(ang) * _laySp), (float)(Math.Sin(ang) * _laySp), 0f);
	}
	// wanted position of active enemy i when a layout/strafe is active
	internal static Vector3 EnemyWantLay(int i, CCitadelPlayerPawn me, long now)
	{
		var b = me.Position + new Vector3(_dist, 0f, 0f);
		return i == 0 ? b + StrafeOff(now, true) : b + LayoutOff(i) + StrafeOff(now, false);
	}

	private static List<CCitadelPlayerPawn> ActiveEnemies()
	{
		var l = new List<CCitadelPlayerPawn>();
		int i = 0;
		foreach (var c in Group()) { if (i++ >= Math.Max(1, _nEn)) break; var p = c.GetHeroPawn(); if (p != null) l.Add(p); }
		return l;
	}

	private static bool RangeOp(Step st, CCitadelPlayerPawn? me, CCitadelPlayerPawn? en, long now)
	{
		switch (st.Op)
		{
			case "layout":
				{
					int n = Math.Max(1, (int)Num(st.A, 0, 1)); _dist = (float)Num(st.A, 1, 350); _laySp = (float)Num(st.A, 2, 250);
					_layShape = st.A.Length > 3 ? st.A[3].ToLowerInvariant() : "ring"; _layN = n; _layOn = n > 1 || _strOn; _nEn = n; _enR = _laySp;
					if (_nEn > _nCreate) { _nCreate = _nEn; _createTries = 0; }
					EnemiesMaintain(now, true); _stepEnd = now + 1200;
					ScLog($"LAYOUT request n={n} dist={_dist} spacing={_laySp} shape={_layShape}");
					_steps.Insert(_si + 1, new Step { Op = "layoutcheck", A = new[] { "30", "0" } });
					return true;
				}
			case "layoutcheck":
				{
					if (me == null) return true;
					double tol = Num(st.A, 0, 30); int tr = (int)Num(st.A, 1, 0);
					var ens = ActiveEnemies(); var bad = new List<string>(); var lines = new List<string>();
					if (ens.Count < _layN) bad.Add($"only {ens.Count} of {_layN} enemies exist");
					for (int i = 0; i < ens.Count; i++)
					{
						var d = ens[i].Position - me.Position; float dxy = new Vector3(d.X, d.Y, 0f).Length(), d3 = d.Length();
						string extra = "";
						if (i == 0)
						{
							if (!_strOn && Math.Abs(dxy - _dist) > tol) bad.Add($"enemy0 horizontal {dxy:0} != {_dist:0} (tol {tol:0})");
							if (Math.Abs(d.Z) > 60) bad.Add($"enemy0 height offset {d.Z:0}");
						}
						else
						{
							var dd = ens[i].Position - ens[0].Position; float sp = dd.Length(); extra = $" fromEnemy0={sp:0}";
							if (!_strOn && Math.Abs(sp - _laySp) > tol) bad.Add($"enemy{i} spacing {sp:0} != {_laySp:0} (tol {tol:0})");
						}
						lines.Add($"LAYOUT t{i} idx={ens[i].EntityIndex} dist3D={d3:0} horiz={dxy:0} dz={d.Z:0}{extra} hp={ens[i].Health}");
					}
					foreach (var l in lines) ScLog(l);
					if (bad.Count == 0) { ScLog($"RANGE layout OK n={ens.Count} want dist={_dist:0} spacing={_laySp:0} shape={_layShape} strafe={(_strOn ? "yes" : "no")}"); return true; }
					if (tr < 6)
					{
						ScLog($"LAYOUT not yet ({string.Join("; ", bad)}) - re-placing, try {tr + 1}");
						EnemiesMaintain(now, true); _stepEnd = now + 900;
						_steps.Insert(_si + 1, new Step { Op = "layoutcheck", A = new[] { st.A.Length > 0 ? st.A[0] : "30", (tr + 1).ToString() } });
						return true;
					}
					ScLog($"VERIFY {_label} FAIL setup/activation: layout not achieved: {string.Join("; ", bad)}");
					return true;
				}
			case "rng":
				{
					if (me == null) return true;
					_dist = (float)Num(st.A, 0, 350); double tol = Num(st.A, 1, 20);
					_layOn = _layOn || _strOn; if (_nEn < 1) _nEn = 1;
					EnemiesMaintain(now, true); if (en != null && !_layOn) en.Teleport(position: me.Position + new Vector3(_dist, 0f, 0f), velocity: Vector3.Zero);
					_stepEnd = now + 700;
					_steps.Insert(_si + 1, new Step { Op = "rngverify", A = new[] { _dist.ToString("0.#", CultureInfo.InvariantCulture), tol.ToString("0.#", CultureInfo.InvariantCulture), "0" } });
					return true;
				}
			case "rngverify":
				{
					if (me == null) return true;
					var ens = ActiveEnemies(); if (ens.Count == 0) { ScLog($"VERIFY {_label} FAIL setup/activation: no enemy to measure distance"); return true; }
					double want = Num(st.A, 0, _dist), tol = Num(st.A, 1, 20); int tr = (int)Num(st.A, 2, 0);
					var d = ens[0].Position - me.Position; float dxy = new Vector3(d.X, d.Y, 0f).Length(), d3 = d.Length();
					bool ok = (_strOn || Math.Abs(dxy - want) <= tol) && Math.Abs(d.Z) <= 60;
					if (ok) { ScLog($"RANGE verify {_label} want={want:0} horiz={dxy:0} dist3D={d3:0} dz={d.Z:0} tol={tol:0} => OK{(_strOn ? " (strafing: instantaneous)" : "")}"); return true; }
					if (tr < 4) { ens[0].Teleport(position: me.Position + new Vector3((float)want, 0f, 0f), velocity: Vector3.Zero); _stepEnd = now + 500; _steps.Insert(_si + 1, new Step { Op = "rngverify", A = new[] { st.A[0], st.A[1], (tr + 1).ToString() } }); return true; }
					ScLog($"RANGE verify {_label} want={want:0} horiz={dxy:0} dist3D={d3:0} dz={d.Z:0} => OUT");
					ScLog($"VERIFY {_label} FAIL setup/activation: target not at the intended distance (want {want:0}, got {dxy:0}, 3D {d3:0})");
					return true;
				}
			case "strafe":
				{
					if (st.A.Length > 0 && st.A[0] == "off") { _strOn = false; ScLog("STRAFE off"); EnemiesMaintain(now, true); return true; }
					_strAmp = (float)Num(st.A, 0, 150); _strPer = (float)Num(st.A, 1, 3); _strAll = st.A.Contains("all"); _strT0 = now; _strOn = true; _layOn = true;
					ScLog($"STRAFE on amp=+-{_strAmp:0}u period={_strPer:0.0}s targets={(_strAll ? "all" : "enemy0")} (teleport-driven)");
					return true;
				}
			case "rngreset":
				_tally.Clear(); _rngShots0 = Shots(); _rngHits0 = _evCount.Where(k => k.Key.StartsWith("BulletHit")).Sum(k => k.Value); _rngT0 = now;
				ScLog("RANGE tally reset");
				return true;
			case "rngreport":
				{
					string lab = st.A.Length > 0 ? string.Join(' ', st.A) : _label;
					var ens = ActiveEnemies(); int shots = Shots() - _rngShots0, bh = _evCount.Where(k => k.Key.StartsWith("BulletHit")).Sum(k => k.Value) - _rngHits0;
					double prim = 0, sec = 0; int ph = 0, sh = 0, lethal = 0, hitTargets = 0;
					for (int i = 0; i < ens.Count; i++)
					{
						_tally.TryGetValue(ens[i].EntityIndex, out var t); t ??= new TgtTally();
						double dist = me != null ? (ens[i].Position - me.Position).Length() : 0;
						if (i == 0) { prim += t.Dmg; ph += t.Hits; } else { sec += t.Dmg; sh += t.Hits; }
						if (t.Hits > 0) hitTargets++; lethal += t.Lethal;
						ScLog($"RANGE {lab} target{i}{(i == 0 ? "(primary)" : "(secondary)")} dist3D={dist:0} damage={t.Dmg:0.#} hits={t.Hits} lethalHits={t.Lethal} byAbility={string.Join(";", t.ByAbility.Select(k => k.Key + "=" + k.Value.ToString("0.#", CultureInfo.InvariantCulture)))}");
					}
					ScLog($"RANGE {lab} totals primaryDamage={prim:0.#} secondaryDamage={sec:0.#} primaryHits={ph} secondaryHits={sh} targetsHit={hitTargets}/{ens.Count} lethalHits={lethal} gunShots={shots} bulletHits={bh} hitRate={(shots > 0 ? (100.0 * bh / shots).ToString("0") + "%" : "n/a")} secs={(now - _rngT0) / 1000.0:0.0} (damage counted once per victim per event; misses are not damage; kills are masked by the target health floor, lethal hits = events whose damage >= victim health)");
					return true;
				}
		}
		return false;
	}

	// called from OnTakeDamage (running scenario only): per-victim tally of OUR damage
	private static void RangeDmg(TakeDamageEvent ev)
	{
		try
		{
			var me = MyPawn(); var a = ev.Info.Attacker; var v = ev.Entity;
			if (me == null || a == null || v == null || a.EntityIndex != me.EntityIndex || v.EntityIndex == me.EntityIndex) return;
			if (v.TeamNum == me.TeamNum) return;
			if (!_tally.TryGetValue(v.EntityIndex, out var t)) { t = new TgtTally { First = Environment.TickCount64 }; _tally[v.EntityIndex] = t; }
			t.Dmg += ev.Info.Damage; t.Hits++;
			if (ev.Info.Damage >= v.Health) t.Lethal++;
			string ab = ev.Info.Ability?.SubclassVData?.Name ?? "gun/other";
			t.ByAbility[ab] = t.ByAbility.GetValueOrDefault(ab) + ev.Info.Damage;
		}
		catch { }
	}

	// 25 Hz teleport-driven strafing for the active enemies
	private static void RangeTick(long now, CCitadelPlayerPawn? me)
	{
		if (!_strOn || me == null || now - _strLast < 40) return;
		_strLast = now;
		try
		{
			var ens = ActiveEnemies(); double t = (now - _strT0) / 1000.0;
			float vy = (float)(_strAmp * 2 * Math.PI / Math.Max(0.2, _strPer) * Math.Cos(2 * Math.PI * t / Math.Max(0.2, _strPer)));
			for (int i = 0; i < ens.Count; i++)
			{
				if (i > 0 && !_strAll) continue;
				ens[i].Teleport(position: EnemyWantLay(i, me, now), velocity: new Vector3(0f, vy, 0f));
			}
		}
		catch { }
	}
}
