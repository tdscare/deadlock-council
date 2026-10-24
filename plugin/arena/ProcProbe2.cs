using System.Diagnostics;
using System.Runtime.InteropServices;
using DeadworksManaged.Api;

namespace SandboxTester;

// Read-only: logs scheduling facts of the Deadlock client process (priority class, EcoQoS/power-throttling state, CPU use). Changes nothing.
public partial class SandboxTester
{
	[StructLayout(LayoutKind.Sequential)] private struct PROC_POWER_THROTTLING_STATE { public uint Version; public uint ControlMask; public uint StateMask; }
	[DllImport("kernel32.dll", SetLastError = true)] private static extern bool GetProcessInformation(IntPtr h, int cls, out PROC_POWER_THROTTLING_STATE info, int size);
	[DllImport("kernel32.dll")] private static extern IntPtr OpenProcess(uint access, bool inherit, int pid);
	[DllImport("kernel32.dll")] private static extern bool CloseHandle(IntPtr h);

	[Command("sbx_procinfo", Description = "Log scheduling facts of the Deadlock client process (read-only)")]
	public void CmdProcInfo(Caller caller) => Run(caller, "sbx_procinfo", "", () => { System.Threading.Tasks.Task.Run(() =>
	{
		foreach (var p in Process.GetProcessesByName("deadlock"))
		{
			try
			{
				var t0 = p.TotalProcessorTime; var w0 = Stopwatch.GetTimestamp();
				Thread.Sleep(1000);
				p.Refresh(); var t1 = p.TotalProcessorTime; double wall = (Stopwatch.GetTimestamp() - w0) / (double)Stopwatch.Frequency;
				string eco = "?";
				var h = OpenProcess(0x1000, false, p.Id);
				if (h != IntPtr.Zero)
				{
					if (GetProcessInformation(h, 4, out var st, Marshal.SizeOf<PROC_POWER_THROTTLING_STATE>()))
						eco = $"controlMask={st.ControlMask} stateMask={st.StateMask} (stateMask&1 = EXECUTION_SPEED throttled)";
					else eco = "query failed err=" + Marshal.GetLastWin32Error();
					CloseHandle(h);
				}
				Log($"PROCINFO pid={p.Id} priorityClass={p.PriorityClass} threads={p.Threads.Count} cpu={(t1 - t0).TotalSeconds / wall * 100:0}% of one core, powerThrottling: {eco}");
			}
			catch (Exception e) { Log("PROCINFO failed: " + e.Message); }
			p.Dispose();
		}
	}); });
}
