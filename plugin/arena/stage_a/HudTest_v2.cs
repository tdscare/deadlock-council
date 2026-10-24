using System.Globalization;
using DeadworksManaged.Api;

namespace SandboxTester;

// sbx_hudtest: shows one labelled message per display mode, then sends a boon (ability point + souls) and a hero switch, logging every action with timestamps.
// Kieran answers per mode: could you still read it after the boon and after the hero switch (and was it clipped)?
// Refuses to run while a scenario/queue task is running (pause the queue first). No OS input.
public partial class SandboxTester
{
	private static int _htStep = -1, _htMode; private static long _htT0, _htSendAt; private static int _htStage;
	private static readonly string[] _htModes = { "announce", "hudmsg", "center", "worldtext" };
	private static Heroes _htOrig = Heroes.Haze; private static string _htEnemy = "Haze";
	

	[Command("sbx_hudtest", Description = "Test the 4 HUD display modes against a boon and a hero switch (queue must be paused/idle)")]
	public void CmdHudTest(Caller caller) => Run(caller, "sbx_hudtest", "", () =>
	{
		if (_running || _qr != null) { Reply(caller, "refused: a scenario/queue task is running. Pause the queue first (sbx_q pause)."); Log("HUDTEST refused: task running"); return; }
		if (_htStep >= 0) { Reply(caller, "hudtest already running"); return; }
		if (Human() == null || MyPawn() == null) { Log("HUDTEST refused: no client/pawn"); return; }
		_htOrig = _myHero; _htEnemy = _enemyHero.ToString(); _htMode = 0; _htStage = 0; _htT0 = Environment.TickCount64; _htStep = 0; _htSendAt = 0;
		Log($"HUDTEST START modes={string.Join(",", _htModes)} hero={_htOrig} enemy={_htEnemy}");
		ChatGroup("HUD test: 4 modes, 40 s each", "Watch the banner/text. Tell me per", "mode: A B C D readable? clipped?");
	});

	private static void HudTestTick(long now)
	{
		var mode = _htModes[_htMode]; long el = now - _htT0; char L = (char)('A' + _htMode);
		string title = T32($"TEST {L} of D: {mode}");
		string d1 = "Can you read this?";
		if (_htStage >= 1) d1 = "Boon sent. Still visible?";
		if (_htStage >= 2) d1 = "Hero switched. Still visible?";
		if (_htStage >= 3) d1 = "Switched back. Still visible?";
		string desc = d1 + "\nAnswer for " + L + ": seen / clipped?";
		if (now - _htSendAt >= (mode == "worldtext" ? 1000 : 2000)) { _htSendAt = now; HudShowMode(mode, title, desc, 3); }
		var me = MyPawn();
		if (_htStage == 0 && el >= 12000)
		{
			_htStage = 1;
			try
			{
				me?.ModifyCurrency(ECurrencyType.EAbilityPoints, 1, ECurrencySource.ELevelUp, false, true, false);
				me?.ModifyCurrency(ECurrencyType.EGold, 1000, ECurrencySource.EBossKill, false, true, false);
				Log($"HUDTEST {mode} t={el / 1000.0:0.0}s BOON sent (+1 ability point, +1000 souls, level {me?.Level})");
			}
			catch (Exception e) { Log("HUDTEST boon failed: " + e.Message); }
			ChatGroup($"{L} {mode}: boon sent now");
		}
		else if (_htStage == 1 && el >= 22000)
		{
			_htStage = 2; var other = _htOrig == Heroes.Haze ? "Wraith" : "Haze";
			Log($"HUDTEST {mode} t={el / 1000.0:0.0}s HERO SWITCH to {other}");
			try { StartSetup(other, _htEnemy, Human()); } catch (Exception e) { Log("HUDTEST switch failed: " + e.Message); }
			ChatGroup($"{L} {mode}: hero switch now");
		}
		else if (_htStage == 2 && el >= 31000)
		{
			_htStage = 3;
			Log($"HUDTEST {mode} t={el / 1000.0:0.0}s HERO SWITCH BACK to {_htOrig}");
			try { StartSetup(_htOrig.ToString(), _htEnemy, Human()); } catch (Exception e) { Log("HUDTEST switch back failed: " + e.Message); }
		}
		else if (el >= 40000)
		{
			Log($"HUDTEST {mode} END");
			ChatGroup($"End of test {L} ({mode})");
			_htMode++; _htStage = 0; _htT0 = now; _htSendAt = 0;
			if (_htMode >= _htModes.Length) { _htStep = -1; Log("HUDTEST DONE"); ChatGroup("HUD test done. Send me A B C D answers"); }
		}
	}
}
