using System.Globalization;
using System.Numerics;
using DeadworksManaged.Api;

namespace SandboxTester;

// Realism ops: reset, accuracy, enemies, ekeep/ehp/eitem, lowhp (+heal log by source), incoming damage.
public partial class SandboxTester
{
	private static readonly Random _rng = new();
	private static float _dist = 350f, _missDeg = 10f, _moveF, _moveL; private static long _moveUntil;

	// ---- accuracy ----
	private static double _accP = 1, _headFrac = 1;
	private static float _headPitch = -3f;
	private static long _accNext; private static bool _accActive;
	private static float _accPitch, _accYaw;
	private static int _accWin, _accMissWin, _accHeadWin;

	private static void AccTick(long now)
	{
		if (now < _accNext) return;
		_accNext = now + 170;
		if (!_accActive) { _accPitch = 0; _accYaw = 0; return; }
		_accWin++;
		if (_rng.NextDouble() >= _accP)
		{
			_accMissWin++;
			float s = _rng.Next(2) == 0 ? -1f : 1f;
			_accYaw = s * _missDeg * (0.6f + (float)_rng.NextDouble() * 0.8f);
			_accPitch = ((float)_rng.NextDouble() - 0.5f) * _missDeg;
		}
		else
		{
			_accYaw = 0;
			if (_rng.NextDouble() < _headFrac) { _accPitch = _headPitch; _accHeadWin++; }
			else _accPitch = 0;
		}
	}

	// ---- enemies group ----
	private static int _nEn = 1; private static float _enR = 250f;
	private static long _enNext;
	private static readonly HashSet<int> _enInit = new();
	private static bool _eGod; private static double _eFloor = 0.9; private static int _eHp;

	private static List<CCitadelPlayerController> Group()
	{
		var human = Human();
		return Players.GetAll().Where(p => p != null && (human == null || p.EntityIndex != human.EntityIndex) && (p.IsBot || p.PlayerName == "Dummy")).ToList();
	}

	private static void EnemiesMaintain(long now, bool force)
	{
		if (_nEn <= 1) return;
		if (!force && now < _enNext) return;
		_enNext = now + 500;
		var me = MyPawn(); if (me == null) return;
		var g = Group();
		if (g.Count < _nEn) { try { Server.CreateFakeClient("Dummy"); ScLog($"enemies: created fake client ({g.Count}/{_nEn})"); } catch (Exception e) { ScLog("enemies create fail " + e.Message); } return; }
		int i = 0;
		foreach (var c in g.Take(_nEn))
		{
			var p = c.GetHeroPawn();
			if (!_enInit.Contains(c.EntityIndex) || p == null || (int)p.HeroID == 0)
			{
				if (!(p != null && p.HeroID == _enemyHero && c.TeamNum == 3)) { c.ChangeTeam(3, keepHero: false); c.SelectHero(_enemyHero); }
				_enInit.Add(c.EntityIndex);
				i++; continue;
			}
			if (p.Health <= 0) { try { p.ForceRespawn(false); } catch { } i++; continue; }
			Vector3 want;
			if (i == 0) want = me.Position + new Vector3(_dist, 0, 0);
			else
			{
				double ang = (60.0 + 240.0 * (i - 1) / Math.Max(1, _nEn - 2)) * Math.PI / 180.0;
				want = me.Position + new Vector3((float)(Math.Cos(ang) * _enR), (float)(Math.Sin(ang) * _enR), 0);
			}
			if (force || (p.Position - want).Length() > 60f) p.Teleport(want, velocity: Vector3.Zero);
			p.Health = _eHp > 0 ? _eHp : p.GetMaxHealth();
			i++;
		}
	}

	private static void EnemyKeepTick()
	{
		foreach (var c in Group().Take(Math.Max(1, _nEn)))
		{
			var p = c.GetHeroPawn(); if (p == null || p.Health <= 0) continue;
			try { if ((p.Flags & EntityFlags.Godmode) != 0) p.Flags &= ~EntityFlags.Godmode; } catch { }
			int full = _eHp > 0 ? _eHp : p.GetMaxHealth();
			if (p.Health < full * _eFloor) p.Health = full;
		}
	}

	// ---- lowhp ----
	private static double _lowPct;
	private static int _lastH = -1; private static double _healDiff;

	private static void LowHpTick(CCitadelPlayerPawn me)
	{
		if (_lowPct <= 0 || me.Health <= 0) return;
		int max = me.GetMaxHealth();
		int tgt = Math.Max(1, (int)(max * _lowPct / 100.0));
		int h = me.Health;
		if (_lastH >= 0 && h > _lastH) _healDiff += h - _lastH;
		if (h > tgt) { me.Health = tgt; h = tgt; }
		else if (h < max * 0.03) { me.Health = tgt; h = tgt; }
		_lastH = h;
	}

	// ---- incoming damage ----
	private static bool _inPending; private static int _inDbg;
	private static void TagIncoming(TakeDamageEvent ev)
	{
		if (!_inPending) return;
		try { ev.Info.CitadelDamageType = _inKind == "gun" ? ECitadelDamageType.Bullet : ECitadelDamageType.Ability; } catch { }
	}
	private static string _inKind = ""; private static double _inDps; private static long _inLast; private static double _inTotal;

	private static void IncomingTick(long now, CCitadelPlayerPawn me, CCitadelPlayerPawn? en)
	{
		if (_inKind.Length == 0 || _inDps <= 0 || en == null || en.Health <= 0 || me.Health <= 0) { _inLast = now; if (_inKind.Length > 0 && _inDbg++ < 3) ScLog($"incoming skipped dps={_inDps} en={(en == null ? "null" : en.Health.ToString())} me={me.Health}"); return; }
		if (now - _inLast < 100) return;
		float amt = (float)(_inDps * (now - _inLast) / 1000.0);
		_inLast = now;
		_inPending = true;
		int hb = me.Health;
		try { me.Hurt(amt, en, en, null!, 0); } finally { _inPending = false; }
		_inTotal += amt;
		try { Write(string.Join(",", (Environment.TickCount64 - _t0).ToString(CultureInfo.InvariantCulture), Q(_label), Q("player"), me.TeamNum.ToString(CultureInfo.InvariantCulture), hb.ToString(CultureInfo.InvariantCulture), Q("player"), en.TeamNum.ToString(CultureInfo.InvariantCulture), Q("incoming"), _inKind == "gun" ? "Bullet" : "Ability", Math.Max(0, hb - me.Health).ToString(CultureInfo.InvariantCulture), "0")); } catch { }
		if (_inDbg++ < 5) ScLog($"incoming dbg amt={amt:0.0} hp {hb} -> {me.Health}");
	}

	// ---- heal / gun event logging ----
	private static string _healFile = "";
	private static readonly Dictionary<string, double[]> _healBySrc = new();
	private static readonly Dictionary<string, int> _evCount = new();
	private static int _dmgHitsOnEnemy, _dmgHeadsOnEnemy;

	private static void RealismReset()
	{
		_accActive = false; _accP = 1; _headFrac = 1; _accPitch = 0; _accYaw = 0; _accWin = _accMissWin = _accHeadWin = 0;
		_lowPct = 0; _lastH = -1; _healDiff = 0; _inKind = ""; _inDps = 0; _inTotal = 0;
		_healBySrc.Clear(); _evCount.Clear(); _dmgHitsOnEnemy = _dmgHeadsOnEnemy = 0;
		_eFloor = 0.9; _eHp = 0; _resGun = _resSpirit = 0; _dist = 350f; _moveUntil = 0;
		_healFile = Path.Combine(_dir, $"heals_{_scName}_{DateTime.Now:HHmmss}.csv");
		try { File.WriteAllText(_healFile, "t_ms,label,event,requested,applied,hp_now,caster,caster_ability,mods\n"); } catch { }
	}

	private static void RealismSummary()
	{
		try
		{
			ScLog($"ACC p={_accP} head={_headFrac}: windows={_accWin} missWindows={_accMissWin} headWindows={_accHeadWin} dmgHitsOnEnemy={_dmgHitsOnEnemy} weakpointHits={_dmgHeadsOnEnemy}");
			ScLog("EVENTS " + string.Join(" ", _evCount.OrderBy(k => k.Key).Select(k => k.Key + "=" + k.Value)));
			foreach (var kv in _healBySrc.OrderByDescending(k => k.Value[1]))
				ScLog($"HEALSRC {kv.Key}: n={kv.Value[2]} requested={kv.Value[0]:0.#} applied={kv.Value[1]:0.#}");
			ScLog($"HEAL totalAppliedByEvents={_healBySrc.Values.Sum(v => v[1]):0.#} healDiffObserved={_healDiff:0.#} incomingApplied={_inTotal:0.#}");
		}
		catch { }
	}

	public override void OnModifierEvent(ModifierEvent args)
	{
		if (!_running) return;
		try
		{
			var me = MyPawn(); if (me == null) return;
			var ev = args.Event;
			bool mine = args.Caster != null && args.Caster.EntityIndex == me.EntityIndex;
			bool onMe = args.Target != null && args.Target.EntityIndex == me.EntityIndex;
			switch (ev)
			{
				case EModifierEvent.GunFired: case EModifierEvent.BulletCreated: case EModifierEvent.BulletHit:
				case EModifierEvent.AbilityAsBulletHit: case EModifierEvent.ProjectileHit: case EModifierEvent.FiredFirstShotInBurst:
					{ var k = ev + (mine ? ":me" : ":other"); _evCount[k] = _evCount.GetValueOrDefault(k) + 1; }
					break;
case EModifierEvent.AbilityExecuted: case EModifierEvent.AbilityCastStarted:
{
if (!mine) break;
string an = ""; try { an = args.Ability?.Ability?.As<CCitadelBaseAbility>()?.AbilityName ?? ""; } catch { }
var k = ev + ":" + an; _evCount[k] = _evCount.GetValueOrDefault(k) + 1;
}
break;
case EModifierEvent.HealthTaken:
case EModifierEvent.UnitHealed:
				case EModifierEvent.ReplicatedHeal:
				case EModifierEvent.PreUnitHealed:
					{
						var d = args.Damage;
						var victim = d?.Victim ?? args.Target;
						if (victim == null || victim.EntityIndex != me.EntityIndex) break;
						float req = d?.HealthRequested ?? 0; int app = d?.HealthApplied ?? 0;
						string cname = "", cab = "";
						try { cname = args.Caster?.DesignerName ?? ""; } catch { }
						try { cab = args.Caster?.As<CCitadelBaseAbility>()?.AbilityName ?? ""; } catch { }
						string key = ev + "|" + cname + "|" + cab;
						if (!_healBySrc.TryGetValue(key, out var a)) _healBySrc[key] = a = new double[3];
						a[0] += req; a[1] += app; a[2]++;
						string mods = "";
						try { mods = string.Join("|", me.ModifierProp.Modifiers.Select(m => m.SubclassVData?.Name ?? "?")); } catch { }
						if (_healFile.Length > 0 && (app > 0 || req > 0))
							File.AppendAllText(_healFile, string.Join(",", (Environment.TickCount64 - _t0).ToString(CultureInfo.InvariantCulture), Q(_label), ev.ToString(),
								req.ToString("0.##", CultureInfo.InvariantCulture), app.ToString(CultureInfo.InvariantCulture), me.Health.ToString(CultureInfo.InvariantCulture), Q(cname), Q(cab), Q(mods)) + "\n");
					}
					break;
			}
		}
		catch (Exception e) { LogException("OnModifierEvent", e); }
	}

private static double _resGun, _resSpirit;
	private static void ApplyEnemyResist(TakeDamageEvent ev)
	{
		if (_resGun <= 0 && _resSpirit <= 0) return;
		try
		{
			var v = ev.Entity; var me = MyPawn();
			if (v == null || me == null || v.EntityIndex == me.EntityIndex || v.TeamNum != 3 || v.DesignerName != "player") return;
			var t = ev.Info.CitadelDamageType;
			double r = (t == ECitadelDamageType.Bullet || t == ECitadelDamageType.WeakpointBonus || t == ECitadelDamageType.Melee) ? _resGun : t == ECitadelDamageType.Ability ? _resSpirit : 0;
			if (r > 0) ev.Info.Damage = (float)(ev.Info.Damage * (1.0 - r / 100.0));
		}
		catch { }
	}

	private static void CountDamageOnEnemy(TakeDamageEvent ev)
	{
		try
		{
			var me = MyPawn(); var v = ev.Entity; var a = ev.Info.Attacker;
			if (me == null || v == null || a == null) return;
			if (a.EntityIndex == me.EntityIndex && v.EntityIndex != me.EntityIndex && v.TeamNum == 3)
			{
				_dmgHitsOnEnemy++;
				if (ev.Info.CitadelDamageType == ECitadelDamageType.WeakpointBonus) _dmgHeadsOnEnemy++;
			}
		}
		catch { }
	}

	// ---- reset ----
	private static HashSet<string>? _baseMods;
	private static long _tpAt;
	private static string _cdMode = "none";
	private static HashSet<string>? _baseModsEn;

	private static void ResetEnemies(bool respawn)
	{
		foreach (var c in Group().Take(Math.Max(1, _nEn)))
		{
			var p = c.GetHeroPawn(); if (p == null) continue;
			try
			{
				for (int pass = 0; pass < 2; pass++)
					foreach (var a in p.AbilityComponent.Abilities.Where(x => x.IsItem).ToList()) try { p.RemoveItem(a.AbilityName); } catch { }
				int rm = 0;
				if (_baseModsEn != null)
					foreach (var m in p.ModifierProp.Modifiers.ToList())
						if (!_baseModsEn.Contains(m.SubclassVData?.Name ?? "")) try { if (p.RemoveModifier(m)) rm++; } catch { }
				p.Health = _eHp > 0 ? _eHp : p.GetMaxHealth();
				if (respawn) p.ForceRespawn(false);
				ScLog($"RESET enemy {c.PlayerName}: items left={p.AbilityComponent.Abilities.Count(a => a.IsItem)} removedMods={rm} hp={p.Health}");
			}
			catch (Exception e) { ScLog("RESET enemy fail " + e.Message); }
		}
	}

	// DANGEROUS: ResetAllAbilityCooldowns / ResetAbilityCooldown(slot) / ResetCooldown on shocktarget (Pain Battery-type resource) abilities
	// write garbage (end=7e9, shown as -2e9 s in game). Only "each" mode exists now, with a sanity guard. Prefer hardreset (fresh pawn).
	private static void CdReset(CCitadelPlayerPawn p, string mode)
	{
		if (mode != "each") return;
		int n = 0, skipped = 0;
		foreach (var a in p.AbilityComponent.Abilities.ToList())
			try
			{
				string nm = a.AbilityName;
				float st = a.CooldownStart, en = a.CooldownEnd;
				bool sane = !a.IsItem && !nm.Contains("shocktarget") && !float.IsNaN(st) && !float.IsNaN(en) && st >= 0 && en >= 0 && st < 1e5f && en < 1e5f && en - st < 700f;
				if (!sane) { skipped++; continue; }
				a.ResetCooldown(); n++;
			}
			catch { }
		ScLog($"CDRESET each: reset={n} skipped(insane/shocktarget/item)={skipped}");
	}

	private static void LogCooldowns(CCitadelPlayerPawn me)
	{
		foreach (var a in me.AbilityComponent.Abilities)
			try
			{
				if (!a.AbilityName.StartsWith("citadel_ability_") && !a.AbilityName.StartsWith("cosmetic"))
					ScLog($"CD {a.AbilityName} onCd={a.IsOnCooldown} start={a.CooldownStart:0.0} end={a.CooldownEnd:0.0} bits={a.UpgradeBits}");
			}
			catch { }
		ScLog("CD listing done");
	}

	private static List<string> ModNames(CCitadelPlayerPawn me)
	{
		var l = new List<string>();
		try { foreach (var m in me.ModifierProp.Modifiers) l.Add(m.SubclassVData?.Name ?? "?"); } catch { }
		return l;
	}

	private static void DoReset(CCitadelPlayerPawn me, bool respawn, long now)
	{
		var before = ModNames(me);
		ScLog($"RESET mods before ({before.Count}): {string.Join(",", before)}");
		for (int pass = 0; pass < 2; pass++)
			foreach (var a in me.AbilityComponent.Abilities.Where(x => x.IsItem).ToList())
				try { me.RemoveItem(a.AbilityName); } catch { }
		int removed = 0;
		if (_baseMods != null)
			foreach (var m in me.ModifierProp.Modifiers.ToList())
			{
				var n = m.SubclassVData?.Name ?? "";
				if (_baseMods.Contains(n)) continue;
				try { if (me.RemoveModifier(m)) removed++; } catch { }
			}
CdReset(me, _cdMode);
me.Health = me.GetMaxHealth();
_lastH = -1;
ResetEnemies(respawn);
if (respawn)
		{
			try { me.ForceRespawn(false); } catch (Exception e) { ScLog("RESET respawn fail " + e.Message); }
			_tpAt = now + 3500;
		}
		var after = ModNames(me);
		int cd = 0; try { cd = me.AbilityComponent.Abilities.Count(a => a.IsOnCooldown); } catch { }
		ScLog($"RESET done: removedMods={removed} modsAfter({after.Count})={string.Join(",", after)} abilitiesOnCooldown={cd} items={me.AbilityComponent.Abilities.Count(a => a.IsItem)} hp={me.Health}/{me.GetMaxHealth()} respawn={respawn}");
	}

	// ---- op dispatcher ----
	private static bool RealismOp(Step st, CCitadelPlayerPawn? me, CCitadelPlayerPawn? en, long now)
	{
		switch (st.Op)
		{
case "hardreset":
{
// full clean state for BOTH sides: swap to another hero and back (fresh pawns: no items, mods, cooldown/charge residue, full hp), then restore mid lane
Heroes other = _myHero == Heroes.Haze ? Heroes.Wraith : Heroes.Haze;
var ins = new List<Step>
{
new Step { Op = "setup", A = new[] { other.ToString(), _enemyHero.ToString() } },
new Step { Op = "wait", A = new[] { "1.5" } },
new Step { Op = "setup", A = new[] { _myHero.ToString(), _enemyHero.ToString() } },
new Step { Op = "wait", A = new[] { "1" } },
new Step { Op = "raw", A = new[] { "citadel_unlock_flex_slots" } },
new Step { Op = "unlock", A = new[] { "7" } },
new Step { Op = "basemods", A = Array.Empty<string>() },
new Step { Op = "mark", A = new[] { "none" } },
};
_steps.InsertRange(_si + 1, ins);
_lastH = -1; _lowPct = 0; _inKind = ""; _nEn = 1; _enInit.Clear(); _resGun = _resSpirit = 0;
ScLog("hardreset: inserted fresh-pawn swap steps");
return true;
}
case "reset":
				if (me != null) DoReset(me, st.A.Length > 0 && st.A[0].Equals("respawn", StringComparison.OrdinalIgnoreCase), now);
				if (st.A.Length > 0 && st.A[0].Equals("respawn", StringComparison.OrdinalIgnoreCase)) _stepEnd = now + 4500;
				return true;
case "basemods":
if (me != null) { _baseMods = new HashSet<string>(ModNames(me)); ScLog($"BASEMODS {string.Join(",", _baseMods)}"); }
if (en != null) { _baseModsEn = new HashSet<string>(ModNames(en)); ScLog($"BASEMODS enemy {string.Join(",", _baseModsEn)}"); }
return true;
case "cdreset":
if (me != null) CdReset(me, st.A.Length > 0 ? st.A[0] : "all");
return true;
case "cdmode":
_cdMode = st.A.Length > 0 ? st.A[0] : "none"; ScLog("cdmode " + _cdMode);
return true;
case "cds":
if (me != null) LogCooldowns(me);
return true;
case "egod":
_eGod = !(st.A.Length > 0 && st.A[0] == "off"); _eFloor = _eGod ? 0.9999 : 0.3; _eHp = (int)Num(st.A, 1, 0);
ScLog($"egod floor={_eFloor} ehp={_eHp}");
return true;
case "mods":
if (en != null) ScLog($"MODS enemy@{_label}: {string.Join(",", ModNames(en))}");
if (me != null) ScLog($"MODS@{_label}: {string.Join(",", ModNames(me))}");
				return true;
			case "accuracy":
				_accActive = true; _accP = Num(st.A, 0, 1); _headFrac = Num(st.A, 1, 1); _headPitch = (float)Num(st.A, 2, _headPitch); _missDeg = (float)Num(st.A, 3, 10);
				_accWin = _accMissWin = _accHeadWin = 0; _dmgHitsOnEnemy = _dmgHeadsOnEnemy = 0; _accNext = 0; _evCount.Clear();
				ScLog($"accuracy p={_accP} head={_headFrac} headPitch={_headPitch}");
				return true;
			case "move":
_aim = true; _moveF = (float)Num(st.A, 0, 1); _moveL = (float)Num(st.A, 1, 0);
_moveUntil = Environment.TickCount64 + (long)(Num(st.A, 2, 1) * 1000); _stepEnd = _moveUntil;
ScLog($"move fwd={_moveF} left={_moveL} for {Num(st.A, 2, 1)}s");
return true;
case "acclog":
				RealismSummary();
				return true;
			case "enemies":
				_nEn = Math.Max(1, (int)Num(st.A, 0, 1)); _enR = (float)Num(st.A, 1, 250);
				if (_nEn == 1)
				{
					var main = DummyCtl();
					foreach (var c in Group().ToList())
						if (main == null || c.EntityIndex != main.EntityIndex)
							try { c.RemoveWithPawns(); ScLog("enemies: removed extra " + c.PlayerName); } catch (Exception e) { ScLog("enemies remove fail " + e.Message); }
					_enInit.Clear();
				}
				else { _stepEnd = now + (long)(Num(st.A, 2, 0) * 1000); EnemiesMaintain(now, true); }
				ScLog($"enemies n={_nEn} r={_enR}");
				return true;
			case "ekeep":
				_eFloor = Num(st.A, 0, 0.3); ScLog($"ekeep floor={_eFloor}");
				return true;
			case "ehp":
				_eHp = (int)Num(st.A, 0, 0); ScLog($"ehp {_eHp}");
				if (en != null && _eHp > 0) { en.Health = _eHp; ScLog($"ehp set -> enemy hp now {en.Health} (max {en.GetMaxHealth()})"); }
				return true;
			case "eitem":
				foreach (var c in Group().Take(Math.Max(1, _nEn)))
				{
					var p = c.GetHeroPawn(); if (p == null || st.A.Length == 0) continue;
var it = p.AddItem(st.A[0], false);
if (it == null) { try { p.ModifyCurrency(ECurrencyType.EGold, 50000, ECurrencySource.ECheats, silent: true, forceGain: true); } catch { } it = p.AddItem(st.A[0], false); }
ScLog(it != null ? $"eitem gave {st.A[0]} to {c.PlayerName}" : $"eitem FAILED {st.A[0]} for {c.PlayerName} (hero {p.HeroID} items={p.AbilityComponent.Abilities.Count(a => a.IsItem)})");
				}
				return true;
case "eresist":
{
string k = st.A.Length > 0 ? st.A[0].ToLowerInvariant() : "";
double pct = Num(st.A, 1, 0);
if (k == "gun") _resGun = pct; else if (k == "spirit") _resSpirit = pct; else { _resGun = _resSpirit = 0; }
ScLog($"eresist gun={_resGun}% spirit={_resSpirit}% (damage scaled in OnTakeDamage on enemy-team players)");
return true;
}
case "eclear":
				foreach (var c in Group().Take(Math.Max(1, _nEn)))
				{
					var p = c.GetHeroPawn(); if (p == null) continue;
					foreach (var a in p.AbilityComponent.Abilities.Where(x => x.IsItem).ToList()) try { p.RemoveItem(a.AbilityName); } catch { }
				}
				return true;
			case "lowhp":
				_lowPct = Num(st.A, 0, 0); _lastH = -1; _healDiff = 0;
				if (me != null && _lowPct > 0) me.Health = Math.Max(1, (int)(me.GetMaxHealth() * _lowPct / 100.0));
				ScLog($"lowhp {_lowPct}% -> hp {me?.Health}/{me?.GetMaxHealth()}");
				return true;
			case "healreset":
				_healBySrc.Clear(); _healDiff = 0; _lastH = -1;
				return true;
			case "healsum":
				RealismSummary();
				return true;
			case "incoming":
				_inKind = st.A.Length > 0 ? st.A[0].ToLowerInvariant() : ""; if (_inKind == "off") _inKind = "";
				_inDps = Num(st.A, 1, 0); _inLast = now; _inTotal = 0;
				ScLog($"incoming {_inKind} {_inDps} dps");
				return true;
		}
		return false;
	}

	private static void RealismTick(long now, CCitadelPlayerPawn? me, CCitadelPlayerPawn? en)
	{
		AccTick(now);
		if (_tpAt > 0 && now >= _tpAt)
		{
			_tpAt = 0;
			var m2 = MyPawn();
			if (m2 != null) { if (OnLaneMap()) m2.Teleport(position: MidLane); m2.Health = m2.GetMaxHealth(); ScLog("respawned, teleported to mid"); }
			return;
		}
		if (me == null) return;
		EnemiesMaintain(now, false);
		EnemyKeepTick();
		LowHpTick(me);
		IncomingTick(now, me, en);
	}
}
