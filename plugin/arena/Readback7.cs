using System.Globalization;
using System.Text;
using DeadworksManaged.Api;

namespace SandboxTester;

// Generic read-back checks (no per-item code).
//  op  rb <name> <spec>      take a reading, log "RB <name> = <v>", keep it for required_readback
//        spec: clip | clipmax | level:<abil> | bits:<abil> | charges:<abil> | maxcharges:<abil> | oncd:<abil> | mod:<match> | ev:<match> | items | hp | maxhp
//              | field:<Class>.<field>:<int|float|bool>      (any schema field on the weapon ability)
//              <abil> = ability name fragment or slot number. clip/clipmax need a clip field: meta clip_field <Class>.<field> or auto-discovered by 'rbprobe'.
//  op  rbprobe               tries candidate class.field names on the weapon ability and logs which exist (discovery, no assumptions kept unless a clip field is found)
//  meta required_readback  <label>|<a>|<op>|<b> ; ...    a,b = reading names or numbers; op = > >= < <= == !=   (mismatch => INVALID with a plain reason)
//  Automatic when a clip field is known: reload/refill events (clip rises >= 2) counted as event key "Reload:refill" (usable by required_activation kind=event, match=refill), clipmax tracked.
public partial class SandboxTester
{
	private static readonly Dictionary<string, double> _rb = new();
	private static string _clipField = ""; private static double _clipPrev = -1, _clipMax; private static long _clipLast;
	private static readonly string[] _rbClasses = { "CCitadel_Ability_PrimaryWeapon", "CCitadelBaseWeapon", "CCitadelWeaponPrimary", "CBasePlayerWeapon", "CCitadelBaseAbility", "CBaseEntity" };
	private static readonly string[] _rbFields = { "m_iClip1", "m_iClip", "m_nClip", "m_iAmmo", "m_nAmmo", "m_iClip2", "m_iMaxClip", "m_nMaxClip", "m_iMaxClip1", "m_iPrimaryAmmoCount", "m_flReloadFinishTime", "m_bReloading", "m_bInReload", "m_flNextPrimaryAttack" };

	private static void RbReset()
	{
		StackReset(); _rb.Clear(); _clipPrev = -1; _clipMax = 0; _clipLast = 0;
		_clipField = M("clip_field"); if (_clipField == "auto") _clipField = "";
		_rbSeen = false;
	}
	private static bool _rbSeen;

	private static CCitadelBaseAbility? RbWeapon(CCitadelPlayerPawn me) { try { return me.AbilityComponent.Abilities.FirstOrDefault(a => a.IsWeapon); } catch { return null; } }
	private static CCitadelBaseAbility? RbAbil(CCitadelPlayerPawn me, string m)
	{
		try
		{
			m = m.ToLowerInvariant();
			if (int.TryParse(m, out var slot)) return me.AbilityComponent.Abilities.FirstOrDefault(a => !a.IsItem && (int)a.AbilitySlot == slot);
			return me.AbilityComponent.Abilities.FirstOrDefault(a => a.AbilityName.ToLowerInvariant().Contains(m));
		}
		catch { return null; }
	}

	private static bool RbField(CBaseEntity e, string cls, string fld, string type, out double v)
	{
		v = 0;
		try
		{
			var c = Encoding.UTF8.GetBytes(cls); var f = Encoding.UTF8.GetBytes(fld);
			switch (type)
			{
				case "float": v = e.GetField<float>(c, f); break;
				case "bool": v = e.GetField<bool>(c, f) ? 1 : 0; break;
				default: v = e.GetField<int>(c, f); break;
			}
			return true;
		}
		catch { return false; }
	}

	private static bool RbRead(string spec, CCitadelPlayerPawn me, out double v)
	{
		v = 0; var s = spec.Trim(); var lo = s.ToLowerInvariant();
		try
		{
			if (lo == "clip" || lo == "clipmax")
			{
				if (lo == "clipmax" && _clipMax > 0) { v = _clipMax; return true; }
				if (_clipField.Length == 0) return false;
				var w = RbWeapon(me); if (w == null) return false;
				var p = _clipField.Split('.'); if (p.Length != 2) return false;
				if (!RbField(w, p[0], p[1], "int", out v)) return false;
				if (lo == "clipmax") { _clipMax = Math.Max(_clipMax, v); v = _clipMax; }
				return true;
			}
			if (lo == "reload_s") { v = _rlLast; return _rlN > 0; }
			if (lo.StartsWith("minof:")) { var vs = lo[6..].Split(',').Select(x => x.Trim()).Where(x => _rb.ContainsKey(x)).Select(x => _rb[x]).ToList(); if (vs.Count == 0) return false; v = vs.Min(); return true; }
			if (lo == "reload_n") { v = _rlN; return true; }
			if (lo == "items") { v = me.AbilityComponent.Abilities.Count(a => a.IsItem); return true; }
			if (lo == "hp") { v = me.Health; return true; }
			if (lo == "maxhp") { v = me.GetMaxHealth(); return true; }
			if (lo.StartsWith("mod:")) { var m = lo[4..]; v = ModNames(me).Count(n => n.ToLowerInvariant().Contains(m)); return true; }
			if (lo.StartsWith("ev:")) { var m = lo[3..]; v = _evCount.Where(k => k.Key.ToLowerInvariant().Contains(m)).Sum(k => k.Value); return true; }
			if (lo.StartsWith("field:"))
			{
				var p = s[6..].Split(':'); var cf = p[0].Split('.'); if (cf.Length != 2) return false;
				var w = RbWeapon(me); if (w == null) return false;
				return RbField(w, cf[0], cf[1], p.Length > 1 ? p[1].ToLowerInvariant() : "int", out v);
			}
			foreach (var k in new[] { "level:", "bits:", "charges:", "maxcharges:", "oncd:" })
				if (lo.StartsWith(k))
				{
					var a = RbAbil(me, lo[k.Length..]); if (a == null) return false;
					switch (k)
					{
						case "level:": v = System.Numerics.BitOperations.PopCount((uint)Math.Max(0, a.UpgradeBits)); break;
						case "bits:": v = a.UpgradeBits; break;
						case "charges:": v = a.RemainingCharges; break;
						case "maxcharges:": v = a.MaxCharges; break;
						default: v = a.IsOnCooldown ? 1 : 0; break;
					}
					return true;
				}
		}
		catch { }
		return false;
	}

	private static bool ReadbackOp(Step st, CCitadelPlayerPawn? me, long now)
	{
		if (st.Op == "rl" || st.Op == "rot") return CondOp(st, me, now);
		if (st.Op == "rbprobe") { if (me != null) RbProbe(me); return true; }
		if (st.Op != "rb") return AllyOp(st, me, EnemyPawn(), now);
		if (me == null || st.A.Length < 2) { ScLog("rb: need <name> <spec>"); return true; }
		var spec = string.Join(' ', st.A.Skip(1));
		if (RbRead(spec, me, out var v)) { _rb[st.A[0]] = v; ScLog($"RB {st.A[0]} = {v.ToString("0.###", CultureInfo.InvariantCulture)}  ({spec})"); }
		else { ScLog($"RB {st.A[0]} UNREADABLE ({spec})"); ScLog($"SC VERIFY {_label} FAIL readback {st.A[0]} ({spec}) could not be read"); }
		return true;
	}

	internal static void RbProbe(CCitadelPlayerPawn me)
	{
		var w = RbWeapon(me); if (w == null) { Log("RBPROBE no weapon ability found"); return; }
		Log($"RBPROBE weapon ability = {w.AbilityName}");
		foreach (var c in _rbClasses) foreach (var f in _rbFields)
			foreach (var t in new[] { "int", "float" })
				if (RbField(w, c, f, t, out var v) && v > -1e6 && v < 1e6) { Log($"RBPROBE ok {c}.{f} ({t}) = {v}"); if (t == "int" && _clipField.Length == 0 && (f == "m_iClip1" || f == "m_iClip" || f == "m_nClip") && v >= 0 && v <= 500) { _clipField = c + "." + f; Log("RBPROBE clip field chosen: " + _clipField); } break; }
	}

	// called from ActSample (100 ms): clip tracking + refill = reload event
	private static void RbSample(long now, CCitadelPlayerPawn me)
	{
		if (_clipField.Length == 0 || now - _clipLast < 100) return; _clipLast = now;
		if (!RbRead("clip", me, out var c)) return;
		_clipMax = Math.Max(_clipMax, c);
		if (_clipPrev >= 0 && c - _clipPrev >= 2) { _evCount["Reload:refill"] = _evCount.GetValueOrDefault("Reload:refill") + 1; CondRefill(now, _clipPrev, c); Log($"ACT reload/refill event: clip {_clipPrev:0} -> {c:0} (max seen {_clipMax:0})"); }
		_clipPrev = c;
	}

	private static void RbFinish()
	{
		try
		{
			if (_clipField.Length > 0) Log($"RB SUMMARY clipField={_clipField} clipMax={_clipMax:0} refillEvents={_evCount.GetValueOrDefault("Reload:refill")}");
			var spec = M("required_readback");
			foreach (var part in spec.Split(';', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries))
			{
				var p = part.Split('|'); if (p.Length < 4) continue;
				string label = p[0].Trim(), an = p[1].Trim(), op = p[2].Trim(), bn = p[3].Trim();
				bool okA = Val(an, out var a), okB = Val(bn, out var b);
				if (!okA || !okB) { _selfInvalid.Add($"{label}: reading '{(okA ? bn : an)}' was never taken"); continue; }
				bool pass = op switch { ">" => a > b, ">=" => a >= b, "<" => a < b, "<=" => a <= b, "==" => Math.Abs(a - b) < 1e-6, "!=" => Math.Abs(a - b) >= 1e-6, _ => false };
				Log($"RB CHECK {label}: {an}={a:0.###} {op} {bn}={b:0.###} => {(pass ? "PASS" : "FAIL")}");
				if (!pass) _selfInvalid.Add($"{label}: {an} is {a:0.###}, needed {op} {b:0.###} ({bn})");
			}
		}
		catch (Exception e) { Log("RB finish failed: " + e.Message); }
	}
	private static bool Val(string n, out double v)
	{
		if (_rb.TryGetValue(n, out v) || double.TryParse(n, NumberStyles.Float, CultureInfo.InvariantCulture, out v)) return true;
		var me = MyPawn(); v = 0;
		if (n == "items_ok" && me != null) { v = me.AbilityComponent.Abilities.Any(a => a.IsItem) ? 1 : 0; return true; }
		if (n == "mods_present") { v = _newModsSeen; return true; }
		if (n == "hits") { v = _dmgHitsOnEnemy; return true; }
		if (n == "heads") { v = _dmgHeadsOnEnemy; return true; }
		return false;
	}
}
