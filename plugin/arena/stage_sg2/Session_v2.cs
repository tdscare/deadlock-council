using DeadworksManaged.Api;

namespace SandboxTester;

// Hard session-validity gate (Kieran 2026-10-24 17:00). The runner never issues commands or accepts a measurement unless the intended
// Sandbox session is live: client connected, hero pawn present (and alive + the scenario hero at a measurement start).
// On loss: active task is aborted as INTERRUPTED (attempt refunded, real reason in the queue log), a global PAUSE file is written so nothing
// resumes by itself, HUD repeats stop, and the single status 'Sandbox disconnected - testing paused' replaces every experiment text.
// Resume = a human/operator deletes PAUSE (sbx_q resume) AFTER the session was verified.
public partial class SandboxTester
{
	private static string _sessMsg = "";
	private static long _simLostUntil;   // sbx_q simlost <sec>: makes the gate see 'no client' for that long (real client untouched)
	internal static CCitadelPlayerController? SessHuman() => Environment.TickCount64 < _simLostUntil ? null : Human();
	internal static string SessKeyNow()
	{
		try { var h = SessHuman(); return h == null ? "" : $"{Environment.ProcessId}:{h.EntityIndex}:{h.PlayerSteamId}"; } catch { return ""; }
	}
	internal static string? SessionProblem(bool checkHero)
	{
		try
		{
			var h = SessHuman(); if (h == null) return Environment.TickCount64 < _simLostUntil ? "SIMULATED loss: no client connected to the Sandbox server" : "no client connected to the Sandbox server";
			var p = h.GetHeroPawn(); if (p == null) return "the client has no hero pawn";
			if (checkHero)
			{
				if (!p.IsAlive) return "the player pawn is dead";
				if (!_waitSetup && p.HeroID != _myHero) return $"hero is {p.HeroID}, expected {_myHero}";
			}
			return null;
		}
		catch (Exception e) { return "session check threw: " + e.Message; }
	}
	private static void SessionPause(string reason)
	{
		_sessMsg = "Sandbox disconnected - testing paused";
		try { File.WriteAllText(QPath("PAUSE"), $"AUTO-PAUSE {NowIso()}: session lost: {reason}. Resume only after the session is verified (sbx_q resume or delete this file).\n"); } catch { }
		Log($"QR SESSION-LOST {reason}; PAUSE file written, HUD repeats stopped, active task interrupted (attempt refunded)");
	}
}
