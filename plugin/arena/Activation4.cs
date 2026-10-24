using System.Globalization;
using DeadworksManaged.Api;

namespace SandboxTester;

// Generic activation / setup verification (no per-item code).
//  meta required_activation <label>|<kind>|<match>|<min> ; <label>|...      kind = modifier (count absent->present transitions of a modifier whose name contains <match>)
//                                                                            | ability (AbilityExecuted events whose ability name contains <match>) | event (any counted event key containing <match>)
//  meta activation_range <units>   meta range_expect in|out|mixed   -> distance me<->target is logged at every measurement block and compared with the item's activation range.
// Not met => the run is INVALID with a plain reason (reasons are added by the queue runner via _selfInvalid).
// For modifiers the uptime, mean buff duration and the shortest gap between activations (internal-cooldown estimate) are logged: "ACT ...".
public partial class SandboxTester
{
	private sealed class ActReq { public string Label = "", Kind = "", Match = ""; public int Min; public int Count; public bool Present; public long Since, LastStart; public double UpSec, DurSum; public long MinGapMs = long.MaxValue; public int Durs; public double FireSec, FireUp; }
	private static readonly List<ActReq> _act = new();
	private static readonly List<string> _selfInvalid = new();
	private static readonly HashSet<string> _seenMods = new();
	private static long _actLast, _actT0; private static double _actRunSec;
	private static readonly List<(string label, float dist, bool inRange)> _distLog = new();

	private static void ActReset()
	{
		RbReset(); _act.Clear(); _selfInvalid.Clear(); _seenMods.Clear(); _distLog.Clear(); _actLast = 0; _actT0 = Environment.TickCount64;
		var spec = M("required_activation");
		foreach (var part in spec.Split(';', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries))
		{
			var p = part.Split('|'); if (p.Length < 3) continue;
			int.TryParse(p.Length > 3 ? p[3].Trim() : "1", out var mn);
			_act.Add(new ActReq { Label = p[0].Trim(), Kind = p[1].Trim().ToLowerInvariant(), Match = p[2].Trim().ToLowerInvariant(), Min = Math.Max(1, mn) });
		}
		if (_act.Count > 0) Log("ACT required: " + string.Join(" ; ", _act.Select(a => $"{a.Label} [{a.Kind} ~{a.Match} >= {a.Min}]")));
	}

	private static void ActSample(long now, CCitadelPlayerPawn? me)
	{
		if (me == null || now - _actLast < 100) return;
		double dt = _actLast == 0 ? 0 : Math.Min(1.0, (now - _actLast) / 1000.0);
		_actLast = now;
		RbSample(now, me); StackSample(now, me); CondTick(now, me);
		try
		{
			var names = ModNames(me);
			foreach (var n in names) if (_seenMods.Add(n) && _baseMods != null && !_baseMods.Contains(n)) Log("ACT modifier seen: " + n);
			foreach (var a in _act)
			{
				if (a.Kind != "modifier") continue;
				bool pres = names.Any(n => n.ToLowerInvariant().Contains(a.Match));
				if (pres && !a.Present)
				{
					a.Count++; a.Since = now;
					if (a.LastStart != 0) a.MinGapMs = Math.Min(a.MinGapMs, now - a.LastStart);
					a.LastStart = now; Log($"ACT {a.Label}: activation #{a.Count} (modifier ~{a.Match})");
				}
				if (!pres && a.Present) { double d = (now - a.Since) / 1000.0; a.UpSec += d; a.DurSum += d; a.Durs++; }
				if (_fire) { a.FireSec += dt; if (pres) a.FireUp += dt; }
				a.Present = pres;
			}
		}
		catch { }
	}

	private static void ActMark(string label)
	{
		try
		{
			var me = MyPawn(); var en = EnemyPawn(); if (me == null || en == null) return;
			LevelsCheck(label);
			float d = System.Numerics.Vector3.Distance(me.Position, en.Position);
			double rng = 0; double.TryParse(M("activation_range"), NumberStyles.Float, CultureInfo.InvariantCulture, out rng);
			bool inR = rng <= 0 || d <= rng;
			_distLog.Add((label, d, inR));
			Log($"DIST {label}: target {d:0} units away" + (rng > 0 ? $", activation range {rng:0} => {(inR ? "IN RANGE (item should be active)" : "OUT OF RANGE (item should be inactive - not a malfunction)")}" : ""));
		}
		catch { }
	}

	// returns plain-English reasons for INVALID; logs ACT summary
	private static void ActFinish()
	{
		try
		{
			long now = Environment.TickCount64;
			double run = Math.Max(1, (now - _actT0) / 1000.0);
			foreach (var a in _act)
			{
				if (a.Kind == "modifier" && a.Present) { double d = (now - a.Since) / 1000.0; a.UpSec += d; a.DurSum += d; a.Durs++; a.Present = false; }
				if (a.Kind == "ability") a.Count = _evCount.Where(k => k.Key.StartsWith("AbilityExecuted:") && k.Key.ToLowerInvariant().Contains(a.Match)).Sum(k => k.Value);
				if (a.Kind == "event") a.Count = _evCount.Where(k => k.Key.ToLowerInvariant().Contains(a.Match)).Sum(k => k.Value);
				Log($"ACT SUMMARY {a.Label}: count={a.Count} (needed {a.Min}) uptime={a.UpSec:0.0}s of {run:0}s ({100 * a.UpSec / run:0}%) avgDuration={(a.Durs > 0 ? a.DurSum / a.Durs : 0):0.0}s shortestGap={(a.MinGapMs == long.MaxValue ? "n/a" : (a.MinGapMs / 1000.0).ToString("0.0") + "s")} (a continuous-bonus assumption would be 100% uptime) activeWhileFiring={(a.FireSec > 0 ? (100 * a.FireUp / a.FireSec).ToString("0") + "%" : "n/a")} of {a.FireSec:0.0}s");
				if (a.Count < a.Min) _selfInvalid.Add($"{a.Label} never triggered ({a.Count} of {a.Min} needed)");
			}
			var exp = M("range_expect").ToLowerInvariant();
			if (_distLog.Count > 0)
			{
				int inN = _distLog.Count(x => x.inRange);
				Log($"DIST SUMMARY blocks={_distLog.Count} inRange={inN} outOfRange={_distLog.Count - inN} expected={(exp.Length > 0 ? exp : "mixed")}");
				if (exp == "in" && inN < _distLog.Count) _selfInvalid.Add($"target was out of the item's range in {_distLog.Count - inN} block(s) but the test needs it in range");
				if (exp == "out" && inN > 0) _selfInvalid.Add($"target was inside the item's range in {inN} block(s) but the test needs it out of range");
			}
			StackFinish(); RbFinish();
			foreach (var r in _selfInvalid) Log("SC VERIFY FAIL setup/activation: " + r);
		}
		catch (Exception e) { Log("ACT finish failed: " + e.Message); }
	}
}
