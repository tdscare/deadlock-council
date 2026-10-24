using System.Globalization;
using System.Text;
using System.Text.Json;
using System.Text.Json.Nodes;
using System.Text.RegularExpressions;
using DeadworksManaged.Api;

namespace SandboxTester;

// Deterministic work-queue controller living in the plugin (survives Claude sessions, disconnects, reloads, restarts).
// State: <root>\sbx_queue\queue.json (atomic tmp+rename), controller.lock, progress.txt, results\<task>.json, PAUSE (flag file).
public partial class SandboxTester
{
	private sealed class QRun
	{
		public string Id = "", Scenario = "", DamageCsv = "", Samples = "", EndWhy = "";
		public int Attempt, Unknown, Exc, VFail, SetupOk, PosOk, ExpectPass, OpFailed;
		public long StartMs, StartTms, EndMs, EndTms, LogStart, LogEnd, FinAt, NoCtlSince, NoPawnSince, Hb;
		public DateTime StartUtc;
		public bool Ended;
		public List<string> Msgs = new(), Cmds = new(), Client = new(), Ext = new();
	}

	private static QRun? _qr;
	private static JsonObject? _q;
	private static bool _qBad, _qrLoaded, _qrYielded;
	private static readonly string _qrInst = Guid.NewGuid().ToString("N")[..8];
	private static string QrOwner => $"sbx-plugin:{Environment.ProcessId}:{_qrInst}";
	private static string _qrStartedIso = "";
	private static long _logLines, _qrLast, _qrLockAt, _qrPauseAt = -100000, _qrConnectAt = -10_000_000, _qrReadySince, _qrHbAt;
	private static string _qrState = "not loaded", _finishWhy = "";
	private static volatile string _origin = "";
	private static volatile bool _qrForce;
	private static string? _qrHumanCmd;
	private static bool _qrPausedNow;
	private static readonly JsonSerializerOptions _qJson = new() { WriteIndented = true };
	private static readonly HashSet<string> _qrInterf = new(StringComparer.OrdinalIgnoreCase)
		{ "selecthero", "changeteam", "buyitem", "sellitem", "buydependentitem", "buyabilityupgrade", "swapactiveability", "trainorupgradeability" };
	private static readonly HashSet<string> _qrAllowed = new(StringComparer.OrdinalIgnoreCase)
		{ "sbx_q", "sbx_build", "sbx_status", "sbx_players", "sbx_pos", "sbx_items" };

	private static string QDir() => Path.Combine(RootDir(), "sbx_queue");
	private static string QPath(string n) => Path.Combine(QDir(), n);
	private static string NowIso() => DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ss.fffZ", CultureInfo.InvariantCulture);
	private static string Safe(string id) => Regex.Replace(id, @"[^A-Za-z0-9_.\-]", "_");
	private static long FileLen(string p) { try { return p.Length > 0 && File.Exists(p) ? new FileInfo(p).Length : -1; } catch { return -1; } }

	// ---- latest-wins atomic writer thread (tmp + rename), nothing blocks the game thread ----
	private static readonly Dictionary<string, string> _qw = new();
	private static readonly object _qwL = new();
	private static Thread? _qwT; private static volatile bool _qwStop;
	private static void QWrite(string path, string text)
	{
		lock (_qwL)
		{
			_qw[path] = text;
			if (_qwT == null)
			{
				_qwStop = false;
				_qwT = new Thread(QwLoop) { IsBackground = true, Name = "sbx-qwriter" };
				_qwT.Start();
			}
			Monitor.Pulse(_qwL);
		}
	}
	private static void QwLoop()
	{
		while (true)
		{
			Dictionary<string, string> cp;
			lock (_qwL)
			{
				while (_qw.Count == 0 && !_qwStop) Monitor.Wait(_qwL, 500);
				if (_qw.Count == 0 && _qwStop) return;
				cp = new Dictionary<string, string>(_qw); _qw.Clear();
			}
			foreach (var kv in cp)
			{
				try
				{
					Directory.CreateDirectory(Path.GetDirectoryName(kv.Key)!);
					var tmp = kv.Key + ".tmp";
					File.WriteAllText(tmp, kv.Value);
					File.Move(tmp, kv.Key, true);
				}
				catch (Exception e) { Log("QR write failed " + kv.Key + ": " + e.Message); }
			}
		}
	}
	private static void QFlush()
	{
		try { _qwStop = true; lock (_qwL) Monitor.PulseAll(_qwL); _qwT?.Join(3000); } catch { }
	}

	// ---- json helpers ----
	private static JsonArray QTasks() => _q!["tasks"]!.AsArray();
	private static JsonObject? QFind(string id) { foreach (var n in QTasks()) if (n is JsonObject o && (string?)o["id"] == id) return o; return null; }
	private static string TS(JsonObject o, string k) => (string?)o[k] ?? "";
	private static int TI(JsonObject o, string k) => (int?)o[k] ?? 0;
	private static void QLog(JsonObject t, string kind, string why)
	{
		if (t["log"] is not JsonArray a) { a = new JsonArray(); t["log"] = a; }
		a.Add(new JsonObject { ["at"] = NowIso(), ["kind"] = kind, ["why"] = why });
		while (a.Count > 40) a.RemoveAt(0);
	}
	private static JsonObject QRunnerCfg() { if (_q!["runner"] is not JsonObject r) { r = new JsonObject { ["active"] = false }; _q["runner"] = r; } return r; }
	private static bool QActive() => _q != null && !_qBad && ((bool?)QRunnerCfg()["active"] ?? false);

	private static long CountLines(string path)
	{
		try
		{
			if (!File.Exists(path)) return 0;
			long n = 0; var buf = new byte[1 << 16];
			using var fs = new FileStream(path, FileMode.Open, FileAccess.Read, FileShare.ReadWrite);
			int r; while ((r = fs.Read(buf, 0, buf.Length)) > 0) for (int i = 0; i < r; i++) if (buf[i] == (byte)'\n') n++;
			return n;
		}
		catch { return 0; }
	}

	// every Log line passes here (any thread): counts lines and feeds the active run's validity checks
	private static void QrObserve(string line)
	{
		Interlocked.Add(ref _logLines, 1 + line.Count(c => c == '\n'));
		var r = _qr; if (r == null || r.Ended) return;
		lock (r)
		{
			void Note(string m) { if (r.Msgs.Count < 30) r.Msgs.Add(m.Length > 200 ? m[..200] : m); }
			if (line.StartsWith("SC unknown op")) { r.Unknown++; Note(line); }
			else if (line.StartsWith("EXCEPTION in")) { r.Exc++; Note(line.Split('\n')[0]); }
			else if (line.StartsWith("SC VERIFY ") && line.Contains(" FAIL")) { r.VFail++; Note(line); }
			else if (line.StartsWith("SC VERIFY ") && line.Contains(" PASS")) r.ExpectPass++;
			else if (line.StartsWith("SC POS VERIFY FAIL") || line.StartsWith("SETUP gave up") || line.StartsWith("SETUP ERROR")) { r.VFail++; Note(line); }
			else if (line.StartsWith("SETUP VERIFY ok")) r.SetupOk++;
			else if (line.StartsWith("SC POS VERIFY ok")) r.PosOk++;
			else if (line.StartsWith("SC ") && line.Contains("FAILED")) { r.OpFailed++; Note(line); }
		}
	}

	// ---- load / unload ----
	private static void QrLoad(bool isReload)
	{
		_qrStartedIso = NowIso();
		QLoad();
		if (_q == null) return;
		if (!_qBad)
		{
			bool foreign = QForeign(out var fdesc);
			// a live foreign controller owns the file: do not touch its running tasks and do not write anything
			int fixedN = foreign ? 0 : QOrphanReset("controller gone (plugin reload/restart/crash)");
			_qrYielded = foreign && QActive();
			Log($"QR LOAD isReload={isReload} active={QActive()} tasks={QTasks().Count} orphanedRunningReset={fixedN} foreignController={(foreign ? fdesc : "none")} {QReconcile(out _)}");
			if (!foreign) QSave();
		}
		_qrLoaded = true; _qrState = QActive() ? (_qrYielded ? "YIELDED (another controller is active)" : "resuming after load") : "stopped";
	}

	// Running tasks whose controller is gone go back to pending. An interruption is not a test failure, so the attempt is refunded
	// (max 5 interruptions per task, then it counts, so a scenario that crashes the game every time still ends blocked).
	private static int QOrphanReset(string cause)
	{
		int n = 0;
		foreach (var x in QTasks())
		{
			if (x is not JsonObject t || TS(t, "state") != "running") continue;
			int att = TI(t, "attempts"), pauses = TI(t, "pauses");
			bool refund = pauses < 5;
			if (refund) { t["attempts"] = Math.Max(0, att - 1); t["pauses"] = pauses + 1; att = Math.Max(0, att - 1); }
			QLog(t, "interrupted", $"{cause}, last hb {TS(t, "hb")}; {(refund ? "attempt refunded" : $"attempt {att} counted (5 interruptions used)")}");
			t["state"] = att >= 3 ? "blocked" : "pending";
			if (att >= 3) { QLog(t, "blocked", "3 attempts used (last one interrupted)"); t["blockedReason"] = "interrupted at attempt 3"; }
			n++;
		}
		return n;
	}

	// After yielding to another controller our in-memory queue is stale: re-read the file and adopt the dead owner's running tasks.
	private static void QTakeover(string why)
	{
		QLoad();
		if (_qBad || _q == null) return;
		int n = QOrphanReset("previous controller gone");
		Log($"QR TAKEOVER ({why}): queue.json re-read from disk, orphanedRunningReset={n} {QReconcile(out _)}");
		QSave();
	}

	// total must equal the sum of the known states (no lost, duplicated or unknown-state tasks)
	private static readonly string[] _qStates = { "pending", "running", "paused", "paused-needs-foreground", "done", "blocked" };
	private static string QReconcile(out bool ok)
	{
		var nodes = QTasks();
		var tasks = nodes.OfType<JsonObject>().ToList();
		int sum = _qStates.Sum(k => tasks.Count(t => TS(t, "state") == k));
		int dup = tasks.Count - tasks.Select(t => TS(t, "id")).Distinct().Count();
		int other = nodes.Count - sum;
		ok = other == 0 && dup == 0;
		return ok ? $"reconciled total={nodes.Count}=sum-of-states" : $"RECONCILE MISMATCH total={nodes.Count} sum-of-known-states={sum} unknown/malformed={other} duplicate-ids={dup}";
	}

	private static void QLoad()
	{
		try
		{
			Directory.CreateDirectory(QDir()); Directory.CreateDirectory(QPath("results"));
			var f = QPath("queue.json");
			if (File.Exists(f)) _q = JsonNode.Parse(File.ReadAllText(f))!.AsObject();
			else _q = new JsonObject { ["created"] = NowIso(), ["tasks"] = new JsonArray() };
			if (_q["tasks"] is not JsonArray) _q["tasks"] = new JsonArray();
			QRunnerCfg();
		}
		catch (Exception e) { _qBad = true; _q = new JsonObject(); Log("QR queue.json unreadable, runner disabled (file untouched): " + e.Message); }
	}

	private static void QrUnload()
	{
		try
		{
			if (_q != null && !_qBad && !QForeign(out _))
			{
				var r = _qr;
				if (r != null) { var t = QFind(r.Id); if (t != null) t["hb"] = NowIso(); }
				QSave();
				var o = new JsonObject { ["owner"] = QrOwner, ["pid"] = Environment.ProcessId, ["instance"] = _qrInst, ["hb"] = NowIso(), ["released"] = true };
				QWrite(QPath("controller.lock"), o.ToJsonString());
			}
		}
		catch { }
		QFlush();
	}

	private static void QSave()
	{
		if (_q == null || _qBad) return;
		QWrite(QPath("queue.json"), _q.ToJsonString(_qJson));
		QWrite(QPath("progress.txt"), QProgressText());
	}

	// ---- controller lock ----
	private static JsonObject? ReadLock()
	{
		try { var f = QPath("controller.lock"); return File.Exists(f) ? JsonNode.Parse(File.ReadAllText(f))?.AsObject() : null; } catch { return null; }
	}
	private static bool QForeign(out string desc)
	{
		desc = "";
		var o = ReadLock(); if (o == null) return false;
		var owner = (string?)o["owner"] ?? "";
		if (owner == QrOwner || ((bool?)o["released"] ?? false)) return false;
		int pid = (int?)o["pid"] ?? 0;
		if (pid == Environment.ProcessId) return false; // same process = our own previous plugin instance (reload)
		double age = 1e9;
		if (DateTime.TryParse((string?)o["hb"], CultureInfo.InvariantCulture, DateTimeStyles.RoundtripKind, out var hb)) age = (DateTime.UtcNow - hb.ToUniversalTime()).TotalSeconds;
		if (age > 15) return false;
		desc = $"owner={owner} pid={pid} hb={(string?)o["hb"]} age={age:0}s";
		return true;
	}
	private static void QLockWrite()
	{
		var o = new JsonObject { ["owner"] = QrOwner, ["pid"] = Environment.ProcessId, ["instance"] = _qrInst, ["hb"] = NowIso(), ["started"] = _qrStartedIso, ["released"] = false, ["state"] = _qrState, ["task"] = _qr?.Id };
		QWrite(QPath("controller.lock"), o.ToJsonString());
	}

	// ---- command gate: while the runner is active nobody else may drive the scenario engine ----
	// Server.ExecuteCommand runs the command later, so file origin/force travel in a FIFO matched on the command word.
	private static readonly System.Collections.Concurrent.ConcurrentQueue<(string cmd, string origin, bool force)> _originFifo = new();
	[ThreadStatic] private static string? _curOrigin;
	private static bool _curForce;
	private static string Origin(Caller caller) => _curOrigin ?? (caller.IsConsole ? "console" : "player:" + caller.Name);
	private static void OriginBegin(Caller caller, string cmd)
	{
		_curOrigin = null; _curForce = false;
		if (!caller.IsConsole) return;
		while (_originFifo.TryPeek(out var h))
		{
			_originFifo.TryDequeue(out h);
			if (h.cmd == cmd) { _curOrigin = h.origin; _curForce = h.force; break; }
			// stale entry (command never reached us): drop it and keep looking
		}
	}
	private static void OriginEnd() { _curOrigin = null; _curForce = false; }
	private static bool QrGate(Caller caller, string cmd, string args)
	{
		if (!_qrLoaded || !QActive() || _qrAllowedInternal) return false;
		if (_qrAllowed.Contains(cmd)) return false;
		string who = Origin(caller);
		bool force = _curForce || args.Split(' ', StringSplitOptions.RemoveEmptyEntries).Contains("force");
		var r = _qr;
		if (force)
		{
			Log($"QR FORCED {cmd} {args} origin={who} (operator override while runner active; current run becomes INVALID)");
			if (r != null) lock (r) r.Ext.Add($"forced {cmd} {args} from {who}");
			return false;
		}
		Log($"QR REFUSED {cmd} {args} origin={who} reason=runner active ({_qrState}); use 'sbx_q pause' first or add 'force'");
		if (r != null) lock (r) r.Cmds.Add($"REFUSED {cmd} {args} from {who}");
		Reply(caller, $"REFUSED {cmd}: the queue runner is active ({_qrState}). Pause it first: create E:\\deadworks-server\\sbx_queue\\PAUSE or run 'sbx_q pause'.");
		return true;
	}
	private static bool _qrAllowedInternal;

	private static void QrClientCmd(string cmd, string full, string who)
	{
		if (!_qrLoaded || !_qrInterf.Contains(cmd)) return;
		long now = Environment.TickCount64;
		bool grace = now - _qrConnectAt < 120000;
		string line = $"{cmd} [{full}] from client '{who}'";
		Log($"QR CLIENT-INPUT {line}{(grace ? " (within 120s of client connect: ignored)" : "")}");
		if (grace || !QActive() || _qrPausedNow) return;
		var r = _qr; if (r != null) lock (r) r.Client.Add(line);
		_qrHumanCmd = line;
	}

	// ---- main step, 1 Hz from OnGameFrame ----
	private static void QrTick()
	{
		if (!_qrLoaded || _qBad) return;
		long now = Environment.TickCount64;
		if (now - _qrLast < 1000) return;
		_qrLast = now;
		try { QrStep(now); } catch (Exception e) { LogException("QrStep", e); }
	}

	private static void QrStep(long now)
	{
		if (!QActive())
		{
			if (_qr != null) QAbort("runner stopped", true, operatorAction: true);
			_qrState = "stopped"; return;
		}
		// lock / foreign controller
		if (now - _qrLockAt >= 5000)
		{
			_qrLockAt = now;
			if (QForeign(out var fd))
			{
				if (!_qrYielded) { _qrYielded = true; Log($"QR CONFLICT another controller holds the lock ({fd}); this runner yields and does nothing"); if (_qr != null) QAbort("another controller took over", true, persist: false, operatorAction: true); }
			}
			else
			{
				if (_qrYielded) { Log("QR controller lock is free again; this runner resumes"); _qrYielded = false; QLockWrite(); QTakeover("lock free"); }
				else QLockWrite();
				QWrite(QPath("progress.txt"), QProgressText());   // proves liveness: written time advances every 5 s
			}
		}
		if (_qrYielded) { _qrState = "YIELDED (another controller is active)"; return; }

		// human input detected -> auto pause
		if (_qrHumanCmd != null)
		{
			var why = _qrHumanCmd; _qrHumanCmd = null;
			try { File.WriteAllText(QPath("PAUSE"), $"AUTO-PAUSE {NowIso()}: human client input detected: {why}. Delete this file or run 'sbx_q resume' to continue.\n"); } catch { }
			Log($"QR AUTO-PAUSE human input: {why}");
			if (_qr != null) QAbort("auto-pause: human client input " + why, true, operatorAction: true);
		}
		// PAUSE flag
		if (now - _qrPauseAt >= 1000)
		{
			_qrPauseAt = now;
			bool p = File.Exists(QPath("PAUSE"));
			if (p != _qrPausedNow)
			{
				_qrPausedNow = p; _qrHumanCmd = null;
				_qrState = p ? "PAUSED (PAUSE file present; delete it to resume)" : "resumed";
				Log(p ? "QR PAUSED (PAUSE file present): controller will not act" : "QR RESUMED (PAUSE file removed)"); QSave();
			}
		}
		if (_qrPausedNow)
		{
			if (_qr != null) QAbort("paused by user", true, operatorAction: true);
			string first = ""; try { first = File.ReadLines(QPath("PAUSE")).FirstOrDefault() ?? ""; } catch { }
			_qrState = "PAUSED " + (first.Length > 0 ? first : "(PAUSE file present; delete it to resume)"); return;
		}

		if (_qr != null) { QMonitor(now); return; }
		QIdle(now);
	}

	private static void QMonitor(long now)
	{
		var r = _qr!;
		var t = QFind(r.Id);
		if (r.Ended)
		{
			if (now - r.FinAt >= 2000) QFinalize(r);
			return;
		}
		if (!_running)
		{
			r.Ended = true; r.EndMs = now; r.EndTms = now - _t0; r.EndWhy = _finishWhy.Length > 0 ? _finishWhy : "scenario stopped without Finish";
			r.LogEnd = Interlocked.Read(ref _logLines) + 1; r.FinAt = now;
			Log($"QR TASK-END {r.Id}#{r.Attempt} why={r.EndWhy}");
			_qrState = $"finalizing {r.Id}"; return;
		}
		_qrState = $"RUNNING {r.Id} attempt {r.Attempt}/3 scenario {r.Scenario} step {_si}/{_steps.Count}";
		// client presence
		var h = Human(); var pw = h?.GetHeroPawn();
		if (h == null) { if (r.NoCtlSince == 0) r.NoCtlSince = now; } else r.NoCtlSince = 0;
		if (h != null && pw == null) { if (r.NoPawnSince == 0) r.NoPawnSince = now; } else r.NoPawnSince = 0;
		if (r.NoCtlSince != 0 && now - r.NoCtlSince > 10000) { QAbort("client disconnected", true, "paused", "client disconnected during run"); return; }
		if (r.NoPawnSince != 0 && now - r.NoPawnSince > 90000) { QAbort("client has no hero pawn for 90 s", true, "paused", "client has no hero pawn"); return; }
		// wall limit
		int maxSec = t != null && t["maxSec"] != null ? TI(t, "maxSec") : ((int?)QRunnerCfg()["maxSecDefault"] ?? 3600);
		if (now - r.StartMs > maxSec * 1000L) { QAbort($"wall-time limit {maxSec}s exceeded", false, "fail"); return; }
		// heartbeat
		if (now - _qrHbAt >= 5000 && t != null) { _qrHbAt = now; t["hb"] = NowIso(); QSave(); }
	}

	// ---- NO OS INPUT (Kieran, 12:49): the runner only drives the game through the server (usercmd/camera/convars). A task whose steps need
	// the real mouse/keyboard/window focus/client relaunch is never run unattended: state paused-needs-foreground, attempt NOT consumed.
	// Only an explicit 'sbx_q fgok <id>' by Kieran lets it run (the plugin still has no OS input code at all).
	private static readonly HashSet<string> _fgOps = new(StringComparer.OrdinalIgnoreCase)
	{
		"key", "keys", "keypress", "keydown", "keyup", "sendkeys", "sendinput", "type", "typetext", "click", "dblclick", "rightclick", "mouse", "mousemove", "mousedown", "mouseup",
		"scroll", "drag", "focus", "foreground", "activate", "alttab", "screenshot", "screen", "launch", "startgame", "openapp", "shell", "cmd", "powershell", "os", "osinput", "input",
		"reconnect", "connect", "disconnect", "restartclient", "restartgame", "clientrestart", "relaunch"
	};
	private static readonly HashSet<string> _fgRaw = new(StringComparer.OrdinalIgnoreCase)
		{ "connect", "reconnect", "disconnect", "retry", "quit", "exit", "kick", "kickid", "killserver", "restart", "startgame" };
	private static readonly HashSet<string> _fgKinds = new(StringComparer.OrdinalIgnoreCase)
		{ "foreground", "os-input", "osinput", "ui", "client-restart", "reconnect", "manual" };
	private static readonly Dictionary<string, (long at, string? why)> _fgCache = new(StringComparer.OrdinalIgnoreCase);

	private static string? QFgReason(JsonObject t)
	{
		if ((bool?)t["fgApproved"] == true) return null;
		if ((bool?)t["needsForeground"] == true) return "task is flagged needsForeground";
		var kind = TS(t, "kind"); if (_fgKinds.Contains(kind)) return $"task kind '{kind}' needs the foreground";
		var sc = TS(t, "scenario"); if (sc.Length == 0) return null;
		long now = Environment.TickCount64;
		if (_fgCache.TryGetValue(sc, out var c) && now - c.at < 20000) return c.why;
		string? why = null; try { why = QFgScan(sc, 0, new HashSet<string>(StringComparer.OrdinalIgnoreCase)); } catch { }
		_fgCache[sc] = (now, why); return why;
	}

	private static string? QFgScan(string name, int depth, HashSet<string> seen)
	{
		if (depth > 5 || !seen.Add(name)) return null;
		var f = Path.Combine(RootDir(), "scenarios", name + ".txt");
		if (!File.Exists(f)) return null;
		int ln = 0;
		foreach (var raw in File.ReadAllLines(f))
		{
			ln++;
			var line = raw; int h = line.IndexOf('#'); if (h >= 0) line = line[..h];
			line = line.Trim(); if (line.Length == 0) continue;
			var w = line.Split(' ', StringSplitOptions.RemoveEmptyEntries); var op = w[0];
			if (_fgOps.Contains(op)) return $"{name}.txt line {ln}: step '{op}' needs OS input / foreground";
			if (op.Equals("raw", StringComparison.OrdinalIgnoreCase) && w.Length > 1 && (_fgRaw.Contains(w[1]) || line.Contains("steam://", StringComparison.OrdinalIgnoreCase)))
				return $"{name}.txt line {ln}: raw '{w[1]}' drops/relaunches the client and needs the foreground";
			if (op.Equals("include", StringComparison.OrdinalIgnoreCase) && w.Length > 1) { var r = QFgScan(w[1], depth + 1, seen); if (r != null) return r; }
		}
		return null;
	}

	private static void QIdle(long now)
	{
		JsonObject? pick = null; bool anyPending = false, changed = false; int fgN = 0;
		long nowMs = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds(); long soonest = long.MaxValue;
		foreach (var n in QTasks())
		{
			if (n is not JsonObject t) continue;
			var st = TS(t, "state");
			if (st == "paused-needs-foreground") { fgN++; continue; }
			if (st != "paused" && st != "pending") continue;
			var fg = QFgReason(t);
			if (fg != null)
			{
				t["state"] = "paused-needs-foreground"; t["pauseReason"] = fg; QLog(t, "paused-needs-foreground", fg + " (attempt not consumed)");
				Log($"QR TASK-NEEDS-FOREGROUND {TS(t, "id")} reason={fg}"); fgN++; changed = true; continue;
			}
			anyPending = true;
			if (st == "pending")
			{
				long nb = (long?)t["notBefore"] ?? 0;
				if (nb > nowMs) { soonest = Math.Min(soonest, nb); continue; }
			}
			pick ??= t;
		}
		if (changed) QSave();
		if (pick == null)
		{
			_qrState = anyPending ? $"BACKOFF next retry in {Math.Max(0, (soonest - nowMs) / 1000)}s" : (fgN > 0 ? $"IDLE nothing runnable ({fgN} task(s) need the foreground, not run)" : "IDLE queue has no pending tasks");
			return;
		}
		// client ready?
		var h = Human(); var pw = h?.GetHeroPawn();
		string? missing = h == null ? "no client connected" : pw == null ? "client has no hero pawn" : null;
		if (missing != null)
		{
			_qrReadySince = 0;
			if (TS(pick, "state") != "paused" || TS(pick, "pauseReason") != missing)
			{
				pick["state"] = "paused"; pick["pauseReason"] = missing; QLog(pick, "paused", missing + " (attempt not consumed)");
				Log($"QR TASK-PAUSED {TS(pick, "id")} reason={missing}"); QSave();
			}
			_qrState = $"WAITING {missing} (task {TS(pick, "id")} paused)"; return;
		}
		if (_qrReadySince == 0) _qrReadySince = now;
		if (now - _qrReadySince < 5000 || now - _qrConnectAt < 10000 || _pending || _running) { _qrState = "WAITING client settling / setup pending"; return; }
		QStartTask(pick, now);
	}

	private static void QStartTask(JsonObject t, long now)
	{
		string id = TS(t, "id"), sc = TS(t, "scenario");
		int att = TI(t, "attempts");
		if (sc.Length == 0 || !File.Exists(Path.Combine(RootDir(), "scenarios", sc + ".txt")))
		{
			t["state"] = "blocked"; QLog(t, "blocked", $"scenario file missing: scenarios\\{sc}.txt (not runnable)"); t["blockedReason"] = $"scenario file missing: {sc}.txt";
			QWriteResult(id, att, false, new List<string> { $"scenario file missing: scenarios\\{sc}.txt" }, null, t); QSave(); return;
		}
		if (att >= 3) { t["state"] = "blocked"; QLog(t, "blocked", "attempts exhausted"); QSave(); return; }
		if (TS(t, "state") == "paused") QLog(t, "resumed", "client back");
		t["attempts"] = att + 1; t["state"] = "running"; t["started"] = NowIso(); t["hb"] = NowIso(); t.Remove("pauseReason"); t.Remove("notBefore");
		QLog(t, "start", $"attempt {att + 1}");
		var r = new QRun { Id = id, Attempt = att + 1, Scenario = sc, StartMs = now, StartTms = now - _t0, StartUtc = DateTime.UtcNow, LogStart = Interlocked.Read(ref _logLines) + 1 };
		_qr = r; _qrHbAt = now; _qrState = $"RUNNING {id}";
		Log($"QR TASK-START {id}#{r.Attempt} scenario={sc}");
		QSave();
		bool ok; string err;
		_qrAllowedInternal = true;
		try { ok = StartScenario(sc, out err, "runner:" + id); } finally { _qrAllowedInternal = false; }
		if (!ok) { r.Ended = true; r.EndMs = now; r.EndTms = now - _t0; r.EndWhy = "start failed: " + err; r.LogEnd = Interlocked.Read(ref _logLines) + 1; r.FinAt = now - 5000; return; }
		r.DamageCsv = _file; r.Samples = _samples;
	}

	private static void QAbort(string why, bool refund, string newState = "pending", string? pauseReason = null, bool persist = true, bool operatorAction = false)
	{
		var r = _qr; if (r == null) return;
		var t = QFind(r.Id);
		if (_running && !r.Ended) { try { Finish("aborted by runner: " + why); } catch { } }
		r.Ended = true; r.EndMs = Environment.TickCount64; r.EndTms = r.EndMs - _t0; r.EndWhy = "aborted: " + why; r.LogEnd = Interlocked.Read(ref _logLines) + 1;
		Log($"QR TASK-ABORT {r.Id}#{r.Attempt} {why} refund={refund}");
		_qr = null;
		if (t == null || !persist) return;   // persist=false: we lost the controller lock, the new owner's files are not ours to write
		int pauses = TI(t, "pauses") + 1; t["pauses"] = pauses;
		bool doRefund = refund && (operatorAction || pauses <= 5);   // operator pauses/stops are never charged; automatic aborts are capped at 5
		if (doRefund) t["attempts"] = Math.Max(0, TI(t, "attempts") - 1);
		QWriteResult(r.Id, r.Attempt, false, new List<string> { "aborted (not a test failure): " + why }, r, t);
		if (newState == "fail")
		{
			QFailTask(t, new List<string> { why });
		}
		else
		{
			t["state"] = newState;
			if (pauseReason != null) t["pauseReason"] = pauseReason;
			QLog(t, "aborted", $"{why}{(doRefund ? " (attempt refunded)" : " (attempt NOT refunded: too many pauses)")}");
		}
		QSave();
	}

	private static void QFailTask(JsonObject t, List<string> reasons)
	{
		int att = TI(t, "attempts");
		QLog(t, "invalid", string.Join("; ", reasons));
		t["lastReasons"] = new JsonArray(reasons.Select(x => (JsonNode?)JsonValue.Create(x)).ToArray());
		if (att >= 3)
		{
			t["state"] = "blocked"; t["blockedReason"] = string.Join("; ", reasons);
			QLog(t, "blocked", $"3 attempts failed; last: {string.Join("; ", reasons)}");
		}
		else
		{
			int backoff = ((int?)QRunnerCfg()["backoffSec"] ?? 30) * (1 << Math.Max(0, att - 1));
			t["state"] = "pending"; t["notBefore"] = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds() + backoff * 1000L;
			QLog(t, "retry", $"retry after {backoff}s (attempt {att}/3 failed)");
		}
	}

	private static void QFinalize(QRun r)
	{
		var t = QFind(r.Id);
		var reasons = new List<string>();
		bool completed = r.EndWhy == "end of script" || r.EndWhy == "end step";
		if (!completed) reasons.Add("scenario did not run to completion: " + r.EndWhy);
		lock (r)
		{
			if (r.Unknown > 0) reasons.Add($"{r.Unknown}x unknown op");
			if (r.Exc > 0) reasons.Add($"{r.Exc}x exception");
			if (r.VFail > 0) reasons.Add($"{r.VFail}x setup/position/expect VERIFY failed");
			if (r.OpFailed > 0) reasons.Add($"{r.OpFailed}x op FAILED (e.g. item not given)");
			if (r.Client.Count > 0) reasons.Add($"{r.Client.Count}x human client input during run");
			if (r.Ext.Count > 0) reasons.Add($"{r.Ext.Count}x forced external command during run");
			if (r.SetupOk < 1) reasons.Add("no SETUP VERIFY ok seen (setup not verified)");
		}
		if (FileLen(r.DamageCsv) <= 0) reasons.Add("damage csv missing");
		if (FileLen(r.Samples) < 60) reasons.Add("samples csv missing/empty");
		bool valid = reasons.Count == 0;
		_qr = null;
		if (t == null) return;
		QWriteResult(r.Id, r.Attempt, valid, reasons, r, t);
		if (valid)
		{
			t["state"] = "done"; t["result"] = "sbx_queue/results/" + Safe(r.Id) + ".json"; t["finished"] = NowIso(); t.Remove("notBefore"); t.Remove("lastReasons");
			QLog(t, "done", $"VALID: yes (attempt {r.Attempt})");
		}
		else QFailTask(t, reasons);
		QSave();
		Log($"QR TASK-RESULT {r.Id}#{r.Attempt} VALID={(valid ? "yes" : "no")} {string.Join("; ", reasons)}");
	}

	private static void QWriteResult(string id, int attempt, bool valid, List<string> reasons, QRun? r, JsonObject t)
	{
		var o = new JsonObject
		{
			["verdict"] = valid ? "VALID: yes" : "VALID: no",
			["task"] = id, ["build"] = TS(t, "build"), ["scenario"] = TS(t, "scenario"), ["attempt"] = attempt,
			["reasons"] = new JsonArray(reasons.Select(x => (JsonNode?)JsonValue.Create(x)).ToArray()),
		};
		if (r != null)
		{
			lock (r)
			{
				o["startedAt"] = r.StartUtc.ToString("o"); o["wallSec"] = Math.Round(((r.EndMs > 0 ? r.EndMs : Environment.TickCount64) - r.StartMs) / 1000.0, 1);
				o["endWhy"] = r.EndWhy;
				o["checks"] = new JsonObject { ["setupVerifyOk"] = r.SetupOk, ["posVerifyOk"] = r.PosOk, ["expectPass"] = r.ExpectPass, ["verifyFail"] = r.VFail, ["unknownOps"] = r.Unknown, ["exceptions"] = r.Exc, ["opFailed"] = r.OpFailed, ["humanClientInput"] = r.Client.Count, ["forcedExternal"] = r.Ext.Count };
				o["damageCsv"] = r.DamageCsv; o["damageCsvBytes"] = FileLen(r.DamageCsv); o["damageCsvTMs"] = new JsonArray(r.StartTms, r.EndTms);
				o["samplesCsv"] = r.Samples; o["samplesCsvBytes"] = FileLen(r.Samples);
				o["pluginLog"] = new JsonObject { ["file"] = _pluginLog, ["lineStart"] = r.LogStart, ["lineEnd"] = r.LogEnd, ["markerStart"] = $"QR TASK-START {id}#{attempt}", ["markerEnd"] = $"QR TASK-END {id}#{attempt}" };
				o["messages"] = new JsonArray(r.Msgs.Select(x => (JsonNode?)JsonValue.Create(x)).ToArray());
				o["clientInput"] = new JsonArray(r.Client.Select(x => (JsonNode?)JsonValue.Create(x)).ToArray());
				o["externalCommands"] = new JsonArray(r.Cmds.Concat(r.Ext).Select(x => (JsonNode?)JsonValue.Create(x)).ToArray());
			}
		}
		o["written"] = NowIso();
		var txt = o.ToJsonString(_qJson);
		QWrite(QPath("results\\" + Safe(id) + ".json"), txt);
		QWrite(QPath("results\\" + Safe(id) + ".a" + attempt + ".json"), txt);
	}

	// ---- progress ----
	private static string QProgressText()
	{
		var sb = new StringBuilder();
		sb.AppendLine($"SANDBOX QUEUE PROGRESS   written {NowIso()}");
		sb.AppendLine("PAUSE = create empty file E:\\deadworks-server\\sbx_queue\\PAUSE   |   RESUME = delete it   (console: sbx_q pause / sbx_q resume)");
		if (_q == null || _qBad) { sb.AppendLine("queue not loaded" + (_qBad ? " (queue.json unreadable, runner disabled)" : "")); return sb.ToString(); }
		var tasks = QTasks().OfType<JsonObject>().ToList();
		int Cn(string k) => tasks.Count(t => TS(t, "state") == k);
		var rec = QReconcile(out _);
		sb.AppendLine($"runner: {(QActive() ? "ACTIVE" : "STOPPED")} | {_qrState}");
		sb.AppendLine($"controller: {QrOwner}");
		sb.AppendLine($"counts: pending {Cn("pending")}  running {Cn("running")}  paused {Cn("paused")}  needs-foreground {Cn("paused-needs-foreground")}  done {Cn("done")}  blocked {Cn("blocked")}  | total {QTasks().Count} | {rec}");
		var cur = _qr;
		sb.AppendLine(cur != null ? $"current: {cur.Id} attempt {cur.Attempt}/3 scenario {cur.Scenario} step {_si}/{_steps.Count} elapsed {(Environment.TickCount64 - cur.StartMs) / 1000}s" : "current: none");
		sb.AppendLine("per build (done/total):");
		foreach (var g in tasks.GroupBy(t => TS(t, "build"))) sb.AppendLine($"  {g.Key}: {g.Count(t => TS(t, "state") == "done")}/{g.Count()}" + (g.Any(t => TS(t, "state") == "blocked") ? $" ({g.Count(t => TS(t, "state") == "blocked")} blocked)" : ""));
		foreach (var t in tasks.Where(t => TS(t, "state") == "blocked")) sb.AppendLine($"BLOCKED {TS(t, "id")} after {TI(t, "attempts")} attempts: {TS(t, "blockedReason")}");
		foreach (var t in tasks.Where(t => TS(t, "state") == "paused")) sb.AppendLine($"PAUSED {TS(t, "id")}: {TS(t, "pauseReason")}");
		foreach (var t in tasks.Where(t => TS(t, "state") == "paused-needs-foreground")) sb.AppendLine($"NEEDS-FOREGROUND {TS(t, "id")}: {TS(t, "pauseReason")} -> not run, no attempt used; run 'sbx_q fgok {TS(t, "id")}' only when you want it run");
		foreach (var t in tasks.Where(t => TS(t, "state") == "pending" && TI(t, "attempts") > 0)) sb.AppendLine($"RETRY-PENDING {TS(t, "id")} attempts {TI(t, "attempts")}: {(t["lastReasons"] as JsonArray)?.FirstOrDefault()}");
		sb.AppendLine();
		sb.AppendLine("STOP = 'sbx_q stop'  |  status = 'sbx_q status'. While active, other sbx_ commands and sbx_cmd files are REFUSED unless prefixed with 'force'. Game input (buy/sell/selecthero/changeteam) auto-pauses. The runner never sends mouse/keyboard/focus input.");
		return sb.ToString();
	}

	// ---- commands ----
	[Command("sbx_q", Description = "Queue runner: sbx_q start|stop|status|pause|resume|reload|add <id> <build> <scenario> [kind] [maxSec]|retry <id>|fgok <id>")]
	public void CmdQ(Caller caller, params string[] a)
	{
		string sub = a.Length > 0 ? a[0].ToLowerInvariant() : "status";
		OriginBegin(caller, "sbx_q");
		string who = Origin(caller);
		Log($"CMD sbx_q {string.Join(' ', a)} by {(caller.IsConsole ? "Console" : caller.Name)} origin={who}");
		try
		{
			if (_q == null) { Reply(caller, "queue not loaded"); return; }
			if (_qBad) { Reply(caller, "queue.json unreadable; runner disabled"); return; }
			// a yielding instance holds a stale in-memory queue: it must not write the live owner's files
			if (_qrYielded && (sub is "stop" or "add" or "retry" or "fgok" or "reload")) { Reply(caller, $"REFUSED: this plugin instance is yielding to another controller ({_qrState}); it does not write queue files"); return; }
			switch (sub)
			{
				case "start":
					{
						bool force = a.Contains("force") || _curForce;
						bool foreign = QForeign(out var fd);
						if (foreign && !force)
						{
							Log($"QR REFUSED sbx_q start origin={who}: another controller holds the lock ({fd})");
							Reply(caller, $"REFUSED: another controller is active ({fd}). Use 'sbx_q start force' only if it is dead.");
							return;
						}
						if (QActive() && !_qrYielded && !foreign) { Reply(caller, "already running (this instance owns the lock)"); break; }
						if (foreign) Log($"QR FORCED takeover of controller lock ({fd}) origin={who}");
						QRunnerCfg()["active"] = true; QRunnerCfg()["startedAt"] = NowIso(); _qrYielded = false; _qrLockAt = 0; QLockWrite();
						if (foreign) QTakeover("forced start"); else QSave();
						Log($"QR START by {who}"); Reply(caller, "queue runner started");
						break;
					}
				case "stop":
					QRunnerCfg()["active"] = false; if (_qr != null) QAbort("sbx_q stop", true, operatorAction: true); QSave();
					if (!QForeign(out _)) QWrite(QPath("controller.lock"), new JsonObject { ["owner"] = QrOwner, ["pid"] = Environment.ProcessId, ["instance"] = _qrInst, ["hb"] = NowIso(), ["released"] = true }.ToJsonString());
					Log($"QR STOP by {who}"); Reply(caller, "queue runner stopped (state kept)"); break;
				case "pause":
					File.WriteAllText(QPath("PAUSE"), $"USER-PAUSE {NowIso()} by {who}. Delete this file or run 'sbx_q resume' to continue.\n");
					_qrPauseAt = 0; if (_qr != null) QAbort("paused by user", true, operatorAction: true);
					Log($"QR PAUSE by {who}"); Reply(caller, "paused: current task aborted cleanly (attempt refunded), controller will not act. 'sbx_q resume' or delete sbx_queue\\PAUSE"); break;
				case "resume":
					try { File.Delete(QPath("PAUSE")); } catch { }
					_qrPauseAt = 0; _qrHumanCmd = null; Log($"QR RESUME by {who}"); Reply(caller, "resumed"); break;
				case "reload":
					{
						var keep = _qr; QLoad(); Log("QR reloaded queue.json from disk by " + who); Reply(caller, $"reloaded, {QTasks().Count} tasks"); break;
					}
				case "add":
					{
						if (a.Length < 4) { Reply(caller, "usage: sbx_q add <id> <build> <scenario> [kind] [maxSec]"); return; }
						var ex = QFind(a[1]);
						if (ex != null) { Reply(caller, $"exists {a[1]} (state {TS(ex, "state")}) - no change"); break; }
						var t = new JsonObject { ["id"] = a[1], ["build"] = a[2], ["exp"] = a[3], ["scenario"] = a[3], ["kind"] = a.Length > 4 ? a[4] : "scenario", ["state"] = "pending", ["attempts"] = 0, ["log"] = new JsonArray() };
						if (a.Length > 5 && int.TryParse(a[5], out var ms)) t["maxSec"] = ms;
						QTasks().Add(t); QSave(); Reply(caller, $"added {a[1]}"); break;
					}
				case "fgok":
					{
						var t = a.Length > 1 ? QFind(a[1]) : null; if (t == null) { Reply(caller, "usage: sbx_q fgok <id>"); return; }
						t["fgApproved"] = true; _fgCache.Clear();
						if (TS(t, "state") == "paused-needs-foreground") { t["state"] = "pending"; t.Remove("pauseReason"); }
						QLog(t, "fgok", "foreground use approved by " + who + " (explicit go-ahead)"); QSave(); Reply(caller, $"{a[1]} approved to run; it still needs you at the PC"); break;
					}
				case "retry":
					{
						var t = a.Length > 1 ? QFind(a[1]) : null; if (t == null) { Reply(caller, "no such task"); return; }
						if (TS(t, "state") == "running" || TS(t, "state") == "done") { Reply(caller, $"{a[1]} is {TS(t, "state")}, not retried"); return; }
						t["state"] = "pending"; t["attempts"] = 0; t.Remove("notBefore"); t.Remove("blockedReason"); t.Remove("pauseReason"); QLog(t, "retry", "manual retry by " + who); QSave(); Reply(caller, $"{a[1]} reset to pending"); break;
					}
				default:
					break;
			}
			foreach (var ln in QProgressText().Split('\n')) if (ln.Trim().Length > 0) Reply(caller, ln.TrimEnd(), chat: false);
		}
		catch (Exception e) { LogException("sbx_q", e); Reply(caller, "sbx_q failed: " + e.Message); }
		finally { OriginEnd(); }
	}
}
