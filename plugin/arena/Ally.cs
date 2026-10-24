using System.Globalization;
using DeadworksManaged.Api;

namespace SandboxTester;

// Scripted ally / real-damage / self-cast tools (plugin only, no OS input).
//  ally <Hero>                 spawn (or reuse) a fake client "Ally" on the player's team as <Hero>, parked beside the player, kept alive. Verified by `allycheck`.
//  allycheck                   readback: ally exists, is a bot, same team as the player, wanted hero, pawn alive -> else SC VERIFY FAIL
//  aexec <ally|enemy|me> <slot> [alt]   that pawn executes the ability in the slot (1-4 = signatures, i1-i4 = active items) through the game's own execute path; ability events counted
//  castself <slot>             player executes the slot with no target; verifies an AbilityExecuted event and logs new modifiers on the player
//  eshoot <gun|spirit|melee> <dmg> [n] [gapSec]   REAL damage from the enemy pawn to the player via ApplyDamage (the game's damage pipeline, OnTakeDamage called); logs hp change and new modifiers
//  moddump [me|enemy|ally]     lists modifiers with schema fields (stack count, duration, creation time) when readable
//  modadd <me|enemy|ally> <modifier> [candidates...]   adds a modifier and verifies it registered (used for stun/cc experiments)
public partial class SandboxTester
{
	private static string _allyWant = ""; private static long _allyNext; private static bool _allyPlaced;
	private static CCitadelPlayerPawn? AllyPawn() { try { RefreshCache(); return _allyC?.GetHeroPawn(); } catch { return null; } }
	private static CCitadelPlayerPawn? PawnOf(string who) => who.ToLowerInvariant() switch { "ally" => AllyPawn(), "enemy" => EnemyPawn(), _ => MyPawn() };
	private static EAbilitySlot SlotOf(string s) => s.ToLowerInvariant() switch
	{
		"1" => EAbilitySlot.Signature1, "2" => EAbilitySlot.Signature2, "3" => EAbilitySlot.Signature3, "4" => EAbilitySlot.Signature4,
		"i1" => EAbilitySlot.ActiveItem1, "i2" => EAbilitySlot.ActiveItem2, "i3" => EAbilitySlot.ActiveItem3, "i4" => EAbilitySlot.ActiveItem4,
		_ => EAbilitySlot.Invalid,
	};
	private static int AbEv() => _evCount.Where(k => k.Key.StartsWith("AbilityExecuted")).Sum(k => k.Value);
	private static readonly List<(long at, string what, int ev0, HashSet<string> mods0)> _chk = new();

	private static bool AllyOp(Step st, CCitadelPlayerPawn? me, CCitadelPlayerPawn? en, long now)
	{
		switch (st.Op)
		{
			case "ally":
				{
					if (st.A.Length == 0) { ScLog("ally: need a hero"); return true; }
					_allyWant = st.A[0]; _allyPlaced = false; _allyNext = 0;
					RefreshCache();
					if (_allyC == null) { try { int sl = Server.CreateFakeClient("Ally"); ScLog($"ALLY created fake client slot={sl}"); InvalidateCache(); } catch (Exception e) { ScLog("ALLY create failed " + e.Message); } }
					_stepEnd = now + (long)(Num(st.A, 1, 6.0) * 1000);
					return true;
				}
			case "allycheck":
				{
					var ap = AllyPawn(); var c = _allyC;
					bool ok = c != null && ap != null && me != null && c.IsBot && c.TeamNum == (me?.TeamNum ?? -1) && ap.Health > 0 && ap.HeroID.ToString().Equals(_allyWant, StringComparison.OrdinalIgnoreCase);
					ScLog($"ALLY readback: ctl={(c != null)} bot={c?.IsBot} team={c?.TeamNum} myTeam={me?.TeamNum} hero={ap?.HeroID} want={_allyWant} hp={ap?.Health} pos={ap?.Position} => {(ok ? "OK" : "NOT READY")}");
					if (!ok) ScLog($"SC VERIFY {_label} FAIL setup/activation: allied bot {_allyWant} is not present on the player's team");
					return true;
				}
			case "aexec":
				{
					var p = PawnOf(st.A.Length > 0 ? st.A[0] : "ally"); var slot = SlotOf(st.A.Length > 1 ? st.A[1] : "1");
					if (p == null || slot == EAbilitySlot.Invalid) { ScLog($"SC VERIFY {_label} FAIL setup/activation: aexec {string.Join(' ', st.A)}: pawn or slot missing"); return true; }
					int e0 = AbEv(); var m0 = new HashSet<string>(ModNames(me ?? p));
					try { int r = p.ExecuteAbilityBySlot(slot, st.A.Length > 2 && st.A[2] == "alt", 0); ScLog($"AEXEC {st.A[0]} {slot} -> {r}"); } catch (Exception ex) { ScLog("AEXEC fail " + ex.Message); }
					_chk.Add((now + 600, $"AEXEC {st.A[0]} {slot}", e0, m0)); _stepEnd = now + 700;
					return true;
				}
			case "castself":
				{
					if (me == null) return true; var slot = SlotOf(st.A.Length > 0 ? st.A[0] : "1");
					int e0 = AbEv(); var m0 = new HashSet<string>(ModNames(me));
					try { int r = me.ExecuteAbilityBySlot(slot, false, 0); ScLog($"CASTSELF {slot} -> {r}"); } catch (Exception ex) { ScLog("CASTSELF fail " + ex.Message); }
					_chk.Add((now + 600, $"CASTSELF {slot}", e0, m0)); _stepEnd = now + 700;
					return true;
				}
			case "eshoot":
				{
					if (me == null || en == null) { ScLog("eshoot: no pawns"); return true; }
					var kind = (st.A.Length > 0 ? st.A[0] : "gun").ToLowerInvariant(); float dmg = (float)Num(st.A, 1, 50); int n = (int)Num(st.A, 2, 1); double gap = Num(st.A, 3, 0.3);
					var t = kind == "spirit" ? ECitadelDamageType.Ability : kind == "melee" ? ECitadelDamageType.Melee : ECitadelDamageType.Bullet;
					int hp0 = me.Health; var m0 = new HashSet<string>(ModNames(me));
					for (int i = 0; i < n; i++)
						_shootQ.Add((now + (long)(i * gap * 1000), dmg, t));
					_shootNote = (now + (long)(n * gap * 1000) + 600, hp0, m0, $"ESHOOT {kind} {dmg} x{n}");
					_stepEnd = now + (long)(n * gap * 1000) + 700;
					return true;
				}
			case "moddump":
				{
					var p = PawnOf(st.A.Length > 0 ? st.A[0] : "me"); if (p == null) { ScLog("moddump: no pawn"); return true; }
					foreach (var m in p.ModifierProp.Modifiers)
					{
						var sb = new System.Text.StringBuilder();
						foreach (var f in new[] { "m_nStackCount", "m_flDuration", "m_flCreationTime", "m_flLastAppliedTime", "m_flRemainingTime", "m_iStackCount" })
							foreach (var tp in new[] { "int", "float" })
								try { var acc = new SchemaAccessor<float>(System.Text.Encoding.UTF8.GetBytes("CBaseModifier"), System.Text.Encoding.UTF8.GetBytes(f), 0); if (tp == "float") { sb.Append($" {f}={acc.Get(m.Handle):0.###}"); break; } } catch { }
						ScLog($"MODDUMP {st.A.FirstOrDefault() ?? "me"}: {m.SubclassVData?.Name}{sb}");
					}
					return true;
				}
			case "modadd":
				{
					var p = PawnOf(st.A.Length > 0 ? st.A[0] : "me"); if (p == null || st.A.Length < 2) { ScLog("modadd: need <who> <modifier>"); return true; }
					var before = new HashSet<string>(ModNames(p)); string got = "";
					foreach (var name in st.A.Skip(1))
					{
						try { p.AddModifier(name, null, me, null, 0); } catch (Exception ex) { ScLog($"MODADD {name} threw {ex.Message}"); }
						var now2 = ModNames(p); var added = now2.Where(x => !before.Contains(x)).ToList();
						ScLog($"MODADD {name} on {st.A[0]}: new modifiers [{string.Join(",", added)}]");
						if (added.Count > 0) { got = name; break; }
					}
					if (got.Length == 0) ScLog($"SC VERIFY {_label} FAIL setup/activation: none of the modifiers [{string.Join(",", st.A.Skip(1))}] registered on {st.A[0]}");
					return true;
				}
		}
		return false;
	}

	private static readonly List<(long at, float dmg, ECitadelDamageType t)> _shootQ = new();
	private static (long at, int hp0, HashSet<string> m0, string what) _shootNote;
	private static void AllyTick(long now, CCitadelPlayerPawn? me)
	{
		// ally upkeep
		if (_allyWant.Length > 0 && me != null && now >= _allyNext)
		{
			_allyNext = now + 500; RefreshCache();
			var c = _allyC;
			if (c != null && Enum.TryParse<Heroes>(_allyWant, true, out var h))
			{
				var ap = c.GetHeroPawn();
				if (ap == null || ap.HeroID != h || c.TeamNum != me.TeamNum) { if (!(ap != null && ap.HeroID == h && c.TeamNum == me.TeamNum)) { try { c.ChangeTeam(me.TeamNum, keepHero: false); c.SelectHero(h); } catch (Exception e) { ScLog("ALLY team/hero failed " + e.Message); } } }
				else
				{
					if (ap.Health <= 0) { try { ap.ForceRespawn(false); } catch { } }
					else
					{
						ap.Health = ap.GetMaxHealth();
						if (!_allyPlaced) { try { ap.Teleport(me.Position + new System.Numerics.Vector3(0, 150f, 0), velocity: System.Numerics.Vector3.Zero); _allyPlaced = true; ScLog($"ALLY placed {h} at {ap.Position} team={c.TeamNum}"); } catch (Exception e) { ScLog("ALLY teleport failed " + e.Message); } }
					}
				}
			}
		}
		// real damage queue
		for (int i = _shootQ.Count - 1; i >= 0; i--)
		{
			var q = _shootQ[i]; if (now < q.at) continue; _shootQ.RemoveAt(i);
			var en = EnemyPawn(); if (me == null || en == null) continue;
			try { using var info = new CTakeDamageInfo(q.dmg, en, en, null!, 0); info.CitadelDamageType = q.t; _realDmg = true; me.ApplyDamage(info); }
			catch (Exception e) { ScLog("ESHOOT apply failed " + e.Message); }
			finally { _realDmg = false; }
		}
		if (_shootNote.at != 0 && now >= _shootNote.at && me != null)
		{
			var added = ModNames(me).Where(x => !_shootNote.m0.Contains(x)).ToList();
			ScLog($"{_shootNote.what}: hp {_shootNote.hp0}->{me.Health} newModifiers=[{string.Join(",", added)}] (real damage through ApplyDamage)");
			_shootNote = default;
		}
		// verify exec checks
		for (int i = _chk.Count - 1; i >= 0; i--)
		{
			var c = _chk[i]; if (now < c.at) continue; _chk.RemoveAt(i);
			int d = AbEv() - c.ev0; var pm = MyPawn(); var added = pm == null ? new List<string>() : ModNames(pm).Where(x => !c.mods0.Contains(x)).ToList();
			ScLog($"{c.what}: AbilityExecuted events +{d}, new modifiers on player [{string.Join(",", added)}]");
			if (d <= 0) ScLog($"SC VERIFY {_label} FAIL setup/activation: {c.what} produced no ability event");
		}
	}
	private static bool _realDmg;
	private static void AllyReset() { _allyWant = ""; _allyPlaced = false; _shootQ.Clear(); _shootNote = default; _chk.Clear(); }
}
