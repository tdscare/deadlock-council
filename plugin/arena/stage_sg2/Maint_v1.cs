using System.Text.Json.Nodes;
using DeadworksManaged.Api;

namespace SandboxTester;

// Controlled maintenance (rebuild / hot-reload) protocol. Rebuilding the plugin mid-task is what interrupted runs before; now:
//   sbx_q maint begin <reason>  -> PAUSE written, active task aborted as MAINTENANCE (attempt refunded, NOT a test failure), queue.json + active-task snapshot saved
//                                  to sbx_queue\snapshots\, maint.flag written, event logged as MAINT (distinct from test failures)
//   sbx_build                   -> refused unless the runner is idle (no queue task, no scenario step in flight, no setup pending) AND maint.flag exists (when the runner is active)
//   sbx_q maint end             -> maint.flag removed (PAUSE stays; resume is a separate explicit step after the session is verified)
public partial class SandboxTester
{
	private static string MaintFlag() => QPath("maint.flag");
	private static bool RunnerIdle() => _qr == null && !_running && !_pending;
	private static void MaintLog(string m)
	{
		Log("MAINT " + m);
		try { File.AppendAllText(QPath("maintenance.log"), NowIso() + " " + m + "\n"); } catch { }
	}
	// null = build allowed, otherwise the refusal reason
	internal static string? MaintBuildRefusal()
	{
		if (!RunnerIdle()) return $"a task/scenario is in flight ({(_qr != null ? "queue task " + _qr.Id : _running ? "scenario running" : "setup pending")}); run 'sbx_q maint begin <reason>' first";
		if (QActive() && !File.Exists(MaintFlag())) return "queue runner is active and no maintenance window is open; run 'sbx_q maint begin <reason>' first";
		return null;
	}
	private static string MaintBegin(string reason, string who)
	{
		try
		{
			Directory.CreateDirectory(Path.Combine(QDir(), "snapshots"));
			string stamp = DateTime.UtcNow.ToString("yyyyMMdd_HHmmss");
			string active = _qr != null ? _qr.Id : "none";
			var snap = new JsonObject { ["at"] = NowIso(), ["reason"] = reason, ["by"] = who, ["activeTask"] = active };
			if (_qr != null) { snap["attempt"] = _qr.Attempt; snap["scenario"] = _qr.Scenario; snap["step"] = _si; snap["steps"] = _steps.Count; var t0 = QFind(_qr.Id); if (t0 != null) snap["taskState"] = JsonNode.Parse(t0.ToJsonString()); }
			File.WriteAllText(Path.Combine(QDir(), "snapshots", $"active_{stamp}.json"), snap.ToJsonString());
			if (File.Exists(QPath("queue.json"))) File.Copy(QPath("queue.json"), Path.Combine(QDir(), "snapshots", $"queue_{stamp}_pre_maint.json"), true);
			File.WriteAllText(QPath("PAUSE"), $"MAINT-PAUSE {NowIso()} by {who}: {reason}. Maintenance window open; 'sbx_q maint end' then 'sbx_q resume' after the session is verified.\n");
			_qrPauseAt = 0;
			if (_qr != null) QAbort("MAINTENANCE (not a test failure): " + reason, true, "pending", null, true, true);
			File.WriteAllText(MaintFlag(), $"{NowIso()} {who} {reason}\n");
			MaintLog($"BEGIN by {who}: {reason}; active task was {active}; snapshots saved; runner idle={RunnerIdle()}");
			return RunnerIdle() ? $"maintenance window open, runner idle, snapshots saved (active task was {active}). sbx_build is now allowed." : "maintenance begun but the runner is not idle yet; wait and re-check with 'sbx_q maint status'";
		}
		catch (Exception e) { LogException("maint begin", e); return "maint begin failed: " + e.Message; }
	}
	private static string MaintEnd(string who)
	{
		try { File.Delete(MaintFlag()); } catch { }
		MaintLog($"END by {who}; PAUSE still in place until an explicit sbx_q resume");
		return "maintenance window closed; PAUSE stays until 'sbx_q resume'";
	}
}
