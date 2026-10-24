using System.Diagnostics;
using System.Globalization;
using System.Runtime.InteropServices;
using DeadworksManaged.Api;

namespace SandboxTester;

// Passive instrumentation for the background-focus question. Sends NO input and changes NO window state:
//  - usercmd cadence of the human slot (call gaps, commands per call) and server-frame cadence, only while a scenario runs
//  - a read-only sample (4 Hz) of "is the foreground window the Deadlock client process?" (GetForegroundWindow + pid compare; no title logged)
// One UCSTAT line per labelled block (at each 'mark') and per scenario (at Finish).
public partial class SandboxTester
{
	[DllImport("user32.dll")] private static extern IntPtr GetForegroundWindow();
	[DllImport("user32.dll")] private static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);
	[DllImport("user32.dll")] private static extern bool IsIconic(IntPtr h);

	private static readonly List<float> _ucGaps = new(), _frGaps = new();
	private static readonly int[] _ucPerCall = new int[8];
	private static long _ucLastTs, _frLastTs, _ucCalls, _ucCmds, _frCount, _frEmpty, _ucThisFrame, _ucFirstTs, _ucLastSeenTs;
	private static int _fgN, _fgYes, _fgMin, _fgLast = -1;
	private static Thread? _fgThread; private static volatile bool _fgStop;

	private static void FgStart()
	{
		if (_fgThread != null) return;
		_fgStop = false;
		_fgThread = new Thread(() =>
		{
			while (!_fgStop)
			{
				try
				{
					if (_running)
					{
						uint fgPid = 0; var fg = GetForegroundWindow(); if (fg != IntPtr.Zero) GetWindowThreadProcessId(fg, out fgPid);
						bool yes = false, min = false;
						foreach (var p in Process.GetProcessesByName("deadlock"))
						{
							try { if ((uint)p.Id == fgPid) yes = true; var mh = p.MainWindowHandle; if (mh != IntPtr.Zero && IsIconic(mh)) min = true; } catch { }
							p.Dispose();
						}
						Interlocked.Increment(ref _fgN); if (yes) Interlocked.Increment(ref _fgYes); if (min) Interlocked.Increment(ref _fgMin);
						int st = yes ? 1 : min ? 2 : 0;
						if (st != _fgLast) { _fgLast = st; Log($"FG client {(st == 1 ? "FOREGROUND" : st == 2 ? "MINIMIZED" : "BACKGROUND")}"); }
					}
				}
				catch { }
				Thread.Sleep(250);
			}
		}) { IsBackground = true, Name = "sbx-fg" };
		_fgThread.Start();
	}
	private static void FgStop() { _fgStop = true; }

	private static readonly long[] _ucSlotCalls = new long[64];
	private static long _ucAllCalls;
	private static void UcStatNote(ProcessUsercmdsEvent args)
	{
		if (!_running) return;
		FgStart();
		_ucAllCalls++; { int sl = (int)args.PlayerSlot; if (sl >= 0 && sl < 64) _ucSlotCalls[sl]++; }
		var me = Human(); if (me == null || args.PlayerSlot != me.EntityIndex - 1) return;
		long ts = Stopwatch.GetTimestamp();
		int n = 0; foreach (var c in args.Usercmds) n++;
		_ucCalls++; _ucCmds += n; _ucThisFrame++; _ucPerCall[Math.Min(n, 7)]++;
		if (_ucFirstTs == 0) _ucFirstTs = ts;
		_ucLastSeenTs = ts;
		if (_ucLastTs != 0 && _ucGaps.Count < 400000) _ucGaps.Add((float)((ts - _ucLastTs) * 1000.0 / Stopwatch.Frequency));
		_ucLastTs = ts;
	}

	private static void FrStatNote(bool simulating)
	{
		if (!_running || !simulating) { _frLastTs = 0; return; }
		long ts = Stopwatch.GetTimestamp();
		_frCount++; if (_ucThisFrame == 0) _frEmpty++; _ucThisFrame = 0;
		if (_frLastTs != 0 && _frGaps.Count < 400000) _frGaps.Add((float)((ts - _frLastTs) * 1000.0 / Stopwatch.Frequency));
		_frLastTs = ts;
	}

	private static string Pct(List<float> g, double q)
	{
		if (g.Count == 0) return "-";
		var a = g.ToArray(); Array.Sort(a);
		return a[Math.Min(a.Length - 1, (int)(q * a.Length))].ToString("0.0", CultureInfo.InvariantCulture);
	}

	private static void UcStatReport(string label)
	{
		try
		{
			double secs = _ucFirstTs != 0 ? (_ucLastSeenTs - _ucFirstTs) / (double)Stopwatch.Frequency : 0;
			int late = _ucGaps.Count(x => x > 32f), vlate = _ucGaps.Count(x => x > 50f);
			double mean = _ucGaps.Count > 0 ? _ucGaps.Average() : 0;
			int fn = _fgN, fy = _fgYes, fm = _fgMin;
			Log("UCSTAT " + string.Join(" ",
				$"label={label}", $"secs={secs:0.0}", $"calls={_ucCalls}", $"cmds={_ucCmds}",
				$"calls/s={(secs > 0 ? _ucCalls / secs : 0):0.0}", $"cmds/call={(_ucCalls > 0 ? (double)_ucCmds / _ucCalls : 0):0.00}",
				$"perCall[0..7+]={string.Join("/", _ucPerCall)}",
				$"gapMs mean={mean:0.00} p50={Pct(_ucGaps, .5)} p95={Pct(_ucGaps, .95)} p99={Pct(_ucGaps, .99)} max={(_ucGaps.Count > 0 ? _ucGaps.Max() : 0):0.0}",
				$"gap>32ms={late} gap>50ms={vlate}",
				$"allSlotCalls={_ucAllCalls} allSlotCalls/frame={(_frCount > 0 ? (double)_ucAllCalls / _frCount : 0):0.00} slots={string.Join(",", Enumerable.Range(0, 64).Where(i => _ucSlotCalls[i] > 0).Select(i => i + ":" + _ucSlotCalls[i]))}",
				$"| frames={_frCount} emptyFrames(no human cmd)={_frEmpty} frameGapMs p50={Pct(_frGaps, .5)} p99={Pct(_frGaps, .99)} max={(_frGaps.Count > 0 ? _frGaps.Max() : 0):0.0}",
				$"| fgSamples={fn} fgPct={(fn > 0 ? 100.0 * fy / fn : -1):0} minimizedPct={(fn > 0 ? 100.0 * fm / fn : -1):0}"));
		}
		catch (Exception e) { Log("UCSTAT failed: " + e.Message); }
		_ucGaps.Clear(); _frGaps.Clear(); Array.Clear(_ucPerCall);
		_ucLastTs = _frLastTs = _ucCalls = _ucCmds = _frCount = _frEmpty = _ucThisFrame = _ucFirstTs = _ucLastSeenTs = 0;
		_fgN = _fgYes = _fgMin = 0; _ucAllCalls = 0; Array.Clear(_ucSlotCalls);
	}
}
