using DeadworksManaged.Api;

namespace SandboxTester;

// Sends a console command to the connected human's client (Server.ClientCommand). The client only runs it if the engine allows server-sent commands for that cvar.
// Logs what was sent; there is no API to read the client's answer back, so the effect is judged from UCSTAT cadence.
public partial class SandboxTester
{
	[Command("sbx_cc", Description = "Send a console command to the human client: sbx_cc <command text>")]
	public void CmdCc(Caller caller, params string[] words) => Run(caller, "sbx_cc", string.Join(' ', words), () =>
	{
		string cmd = string.Join(' ', words);
		var h = Human(); if (h == null) { Log("CC no human client"); return; }
		int slot = h.EntityIndex - 1;
		try { Server.ClientCommand(slot, cmd); Log($"CC sent to slot {slot}: {cmd}"); } catch (Exception e) { Log("CC failed: " + e.Message); }
	});
}
