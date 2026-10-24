using System.Globalization;
using System.Text;
using DeadworksManaged.Api;

namespace SandboxTester;

// Generic conditional / active-trigger support (no per-item code).
//  ops:   rl <secondPressDelaySec|none> [waitSec]   press Reload now; optional 2nd press after the delay (timed active reload). Measures first press -> refill = reload_s (readback "reload_s").
//         rot <slot@sec ...> [fire]                 timed ability rotation (slot = 1-4, i1-i5, reload, melee...). Casts are verified against AbilityExecuted events.
//  meta:  required_levels <abil|slot>=<n>;...       actual ability level (bits popcount) must match before measuring, else INVALID. levels_mode isolated|progression is logged and kept in the result.
//         stack_track <modifier fragment>           logs stack count over time (schema read; falls back to presence), start stacks, time to first activation, active window, shots during window.
//         effect_inactive_on_purpose <why>          baseline with the effect off: shown on screen, flagged in result scope, never evidence that the item is weak.
//         condition <text>                          conditions containing "damage taken" are rejected by lint (artificial damage does not trigger them).
public partial class SandboxTester
{
	private sealed class PressItem { public long At, Hold; public InputButton B; }
	private static readonly List<PressItem> _pq = new();
	private static InputButton SchedNow()
	{
		long n = Environment.TickCount64; InputButton f = InputButton.None;
		for (int i = _pq.Count - 1; i >= 0; i--)
		{
			var p = _pq[i];
			if (n >= p.At + p.Hold) { _pq.RemoveAt(i); continue; }
			if (n >= p.At) f |= p.B;
		}
		return f;
	}

	private static long _rlPress; private static double _rlLast; private static int _rlN; private static string _rlSecond = "";
	private static int _rotWant, _rotEv0; private static long _rotEnd;

	private static bool CondOp(Step st, CCitadelPlayerPawn? me, long now)
	{
		if (st.Op == "rl")
		{
			if (me == null) return true;
			if (_clipField.Length == 0) RbProbe(me);
			double? second = null; if (st.A.Length > 0 && double.TryParse(st.A[0], NumberStyles.Float, CultureInfo.InvariantCulture, out var d)) second = d;
			double wait = Num(st.A, 1, 4.0);
			RbRead("clip", me, out var c0);
			_pq.Add(new PressItem { At = now, Hold = 120, B = InputButton.Reload });
			if (second.HasValue) _pq.Add(new PressItem { At = now + (long)(second.Value * 1000), Hold = 120, B = InputButton.Reload });
			_rlPress = now; _rlSecond = second.HasValue ? $"{second.Value:0.00}s" : "none";
			_aim = true; _stepEnd = now + (long)(wait * 1000);
			ScLog($"RELOAD press: clip={c0:0} secondPress={_rlSecond} (timed input via the plugin)");
			if (_clipField.Length == 0) ScLog($"SC VERIFY {_label} FAIL readback reload could not be measured (no clip field)");
			return true;
		}
		if (st.Op == "rot")
		{
			var spec = st.A.Where(a => a.Contains('@')).ToList(); bool fire = st.A.Contains("fire");
			long last = 0; _rotWant = 0; _rotEv0 = _evCount.Where(k => k.Key.StartsWith("AbilityExecuted")).Sum(k => k.Value);
			foreach (var s in spec)
			{
				var p = s.Split('@'); var b = CastButton(p[0]); if (b == InputButton.None || !double.TryParse(p[1], NumberStyles.Float, CultureInfo.InvariantCulture, out var t)) { ScLog($"SC VERIFY {_label} FAIL rotation bad token {s}"); continue; }
				long at = now + (long)(t * 1000); _pq.Add(new PressItem { At = at, Hold = 200, B = b }); last = Math.Max(last, at);
				if (b != InputButton.Reload && b != InputButton.Jump && b != InputButton.Duck && b != InputButton.Attack2) _rotWant++;
			}
			_aim = true; _fire = fire; _rotEnd = last + 900; _stepEnd = _rotEnd; _rotPending = true;
			ScLog($"ROT start: {_rotWant} ability casts planned [{string.Join(' ', spec)}] gun={(fire ? "firing" : "off")}");
			return true;
		}
		return false;
	}
	private static bool _rotPending;
	// imbue read-back: the item must report IsImbued with the target ability name in ImbuedAbilities
	private static void ImbueReadback(CCitadelPlayerPawn me, string item, string slot, object apiOk)
	{
		try
		{
			var it = me.AbilityComponent.Abilities.FirstOrDefault(a => a.IsItem && a.AbilityName == item);
			var tgt = me.AbilityComponent.Abilities.FirstOrDefault(a => !a.IsItem && a.AbilitySlot.ToString().Equals(slot, StringComparison.OrdinalIgnoreCase));
			bool imb = it != null && it.IsImbued; var names = it == null ? "(item missing)" : string.Join(",", it.ImbuedAbilities);
			bool match = tgt != null && names.Contains(tgt.AbilityName);
			ScLog($"IMBUE readback: item={item} present={it != null} isImbued={imb} imbuedInto=[{names}] target={tgt?.AbilityName} api={apiOk} => {(imb && match ? "OK" : "NOT IMBUED")}");
			if (!(imb && match)) ScLog($"SC VERIFY {_label} FAIL setup/activation: {item} is not imbued into {slot} (readback {(imb ? names : "not imbued")})");
		}
		catch (Exception e) { ScLog("IMBUE readback failed: " + e.Message); }
	}
	private static void CondTick(long now, CCitadelPlayerPawn? me)
	{
		if (_rotPending && now >= _rotEnd)
		{
			_rotPending = false;
			int got = _evCount.Where(k => k.Key.StartsWith("AbilityExecuted")).Sum(k => k.Value) - _rotEv0;
			ScLog($"ROT done: {got} AbilityExecuted events for {_rotWant} planned casts");
			if (got < _rotWant) ScLog($"SC VERIFY {_label} FAIL setup/activation: rotation cast {got} of {_rotWant} abilities (casts counted from ability events)");
		}
	}

	// reload duration hook (called by RbSample when the clip refills)
	private static void CondRefill(long now, double from, double to)
	{
		if (_rlPress == 0) return;
		_rlLast = (now - _rlPress) / 1000.0; _rlN++; _rlPress = 0;
		ScLog($"RELOAD done: first press -> refill {_rlLast:0.00}s (clip {from:0}->{to:0}, second press {_rlSecond})");
	}

	// ---- required_levels ----
	private static void LevelsCheck(string label)
	{
		var spec = M("required_levels"); var me = MyPawn(); if (me == null) return;
		var used = new List<string>();
		try
		{
			foreach (var a in me.AbilityComponent.Abilities.Where(x => !x.IsItem && !x.IsWeapon))
				used.Add($"{a.AbilityName}={System.Numerics.BitOperations.PopCount((uint)Math.Max(0, a.UpgradeBits))}");
		}
		catch { }
		Log($"LEVELS {label}: actual [{string.Join(", ", used)}] mode={(M("levels_mode").Length > 0 ? M("levels_mode") : "undeclared")}");
		foreach (var part in spec.Split(';', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries))
		{
			var p = part.Split('='); if (p.Length != 2 || !int.TryParse(p[1].Trim(), out var want)) continue;
			if (!RbRead("level:" + p[0].Trim(), me, out var have)) { _selfInvalid.Add($"ability '{p[0].Trim()}' not found for the level check"); continue; }
			if ((int)have != want && !_lvlBad.Contains(p[0])) { _lvlBad.Add(p[0]); _selfInvalid.Add($"ability {p[0].Trim()} is level {(int)have} but the scenario needs level {want}"); }
		}
	}
	private static readonly HashSet<string> _lvlBad = new();

	// ---- stack tracking (modifier schema read; presence fallback) ----
	private static int _stkPrev = -1; private static long _stkT0, _stkFirst, _stkWinStart; private static double _stkWin; private static int _stkMax, _stkStart = -1, _stkShots0, _stkShotsWin;
	private static bool _stkSchema = true; private static int _stkLogN;
	private static void StackReset() { _stkPrev = -1; _stkT0 = Environment.TickCount64; _stkFirst = 0; _stkWinStart = 0; _stkWin = 0; _stkMax = 0; _stkStart = -1; _stkShotsWin = 0; _stkSchema = true; _stkLogN = 0; _lvlBad.Clear(); _pq.Clear(); _rlPress = 0; _rlN = 0; _rlLast = 0; _rotPending = false; }
	private static int Shots() => _evCount.Where(k => k.Key.StartsWith("GunFired")).Sum(k => k.Value);
	private static void StackSample(long now, CCitadelPlayerPawn me)
	{
		var m = M("stack_track").ToLowerInvariant(); if (m.Length == 0) return;
		int n = 0; bool found = false;
		try
		{
			foreach (var mod in me.ModifierProp.Modifiers)
			{
				var nm = (mod.SubclassVData?.Name ?? "").ToLowerInvariant(); if (!nm.Contains(m)) continue;
				found = true; int c = 1;
				if (_stkSchema)
				{
					try { var acc = new SchemaAccessor<int>(Encoding.UTF8.GetBytes("CBaseModifier"), Encoding.UTF8.GetBytes("m_nStackCount"), 0); c = acc.Get(mod.Handle); if (c < 0 || c > 1000) { c = 1; _stkSchema = false; Log("STACK schema read gave junk; using presence only"); } }
					catch { _stkSchema = false; Log("STACK schema read unavailable; using presence only"); }
				}
				n = Math.Max(n, c);
			}
		}
		catch { }
		if (!found) n = 0;
		if (_stkStart < 0) { _stkStart = n; Log($"STACK start stacks={n} (~{m})"); }
		if (n != _stkPrev)
		{
			if (n > _stkMax) _stkMax = n;
			if (n > 0 && _stkFirst == 0) { _stkFirst = now; Log($"STACK first activation after {(now - _stkT0) / 1000.0:0.0}s"); }
			if (n > 0 && _stkWinStart == 0) { _stkWinStart = now; _stkShots0 = Shots(); }
			if (n == 0 && _stkWinStart != 0) { _stkWin += (now - _stkWinStart) / 1000.0; _stkShotsWin += Shots() - _stkShots0; _stkWinStart = 0; }
			if (_stkLogN++ < 60) Log($"STACK ~{m} {Math.Max(0, _stkPrev)}->{n} at {(now - _stkT0) / 1000.0:0.0}s");
			_stkPrev = n;
		}
	}
	private static void StackFinish()
	{
		var m = M("stack_track"); if (m.Length == 0) return;
		long now = Environment.TickCount64;
		if (_stkWinStart != 0) { _stkWin += (now - _stkWinStart) / 1000.0; _stkShotsWin += Shots() - _stkShots0; }
		Log($"STACK SUMMARY ~{m}: start={_stkStart} max={_stkMax} timeToFirst={(_stkFirst == 0 ? "never" : ((_stkFirst - _stkT0) / 1000.0).ToString("0.0") + "s")} activeWindow={_stkWin:0.0}s shotsInWindow={_stkShotsWin} schemaRead={_stkSchema}");
		if (_stkFirst == 0) _selfInvalid.Add($"stacking effect '{m}' never appeared");
	}
}
