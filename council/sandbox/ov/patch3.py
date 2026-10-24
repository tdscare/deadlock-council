s=open('Realism.cs').read().replace('\r','')
old="""		return Players.GetAll().Where(p => p != null && (human == null || p.EntityIndex != human.EntityIndex) && (p.IsBot || p.PlayerName == "Dummy")).ToList();"""
new="""		var l = Players.GetAll().Where(p => p != null && (human == null || p.EntityIndex != human.EntityIndex) && (p.IsBot || p.PlayerName == "Dummy")).ToList();
		var main = DummyCtl();
		if (main != null) l = l.OrderBy(p => p.EntityIndex == main.EntityIndex ? 0 : 1).ToList();
		return l;"""
assert old in s; s=s.replace(old,new)
i0=s.index("	private static void EnemiesMaintain(long now, bool force)")
i1=s.index("	private static void EnemyKeepTick()")
newm=open('maintain.txt').read()
s=s[:i0]+newm+s[i1:]
a=s.index('case "enemies":'); b=s.index('case "ekeep":')
newop='''case "enemies":
					_nEn = Math.Max(1, (int)Num(st.A, 0, 1)); _enR = (float)Num(st.A, 1, 250);
					if (_nEn > _nCreate) { _nCreate = _nEn; _createTries = 0; }
					_stepEnd = now + (long)(Num(st.A, 2, 0) * 1000); EnemiesMaintain(now, true);
					ScLog($"enemies n={_nEn} r={_enR} (have {Group().Count}, extras are parked, never removed)");
					return true;
				'''
s=s[:a]+newop+s[b:]
s=s.replace('private static string _inKind = "";','private static double _inHitG, _inHitS, _accG, _accS; private static string _inKind = "";',1)
old='''			float amt = (float)(dps * dt);
			_inKind = kind; _inPending = true;'''
new='''			float amt = (float)(dps * dt);
				double hs = kind == "gun" ? _inHitG : _inHitS;
				if (hs > 0) { if (kind == "gun") { _accG += amt; if (_accG < hs) continue; amt = (float)_accG; _accG = 0; } else { _accS += amt; if (_accS < hs) continue; amt = (float)_accS; _accS = 0; } }
				_inKind = kind; _inPending = true;'''
assert old in s; s=s.replace(old,new)
old='case "incoming":\n'
assert old in s
s=s.replace(old,'case "inhit":\n_inHitG = Num(st.A, 0, 0); _inHitS = Num(st.A, 1, 0); _accG = _accS = 0; ScLog($"inhit gun={_inHitG} spirit={_inHitS}"); return true;\n\t\t\tcase "incoming":\n',1)
open('Realism.cs','w').write(s)
