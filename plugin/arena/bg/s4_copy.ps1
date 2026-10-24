# supervisor_v3.ps1 - hidden supervisor (started by launcher_hidden_v2.vbs). Requests are files in E:\deadworks-server\ctl\*.req (content = optional map name for restart; NEVER the word 'restart'):
#   restart.req -> sandbox_run_v5b.ps1 (verified build only, hidden server)   stop.req -> stop server   quit.req -> exit (also stops telemetry)
#   buildcheck.req -> isolated low-priority compile to out_check only        probe.req (content = seconds, default 120) -> hidden window/focus probe
. 'E:\deadworks-server\staged_v5\bg_common_v2.ps1'
# single-instance guard: a second copy exits immediately (named mutex, per user session)
$script:SbxMutex = New-Object System.Threading.Mutex($false, 'Local\SandboxSupervisor')
if (-not $script:SbxMutex.WaitOne(0)) { ("{0} second supervisor instance exited (mutex held)" -f (Get-Date -Format 'HH:mm:ss')) | Out-File -Append -Encoding ascii 'E:\deadworks-server\sbx_logs\supervisor_v3.txt'; exit }
$PS = "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe"
$SL = "$E\sbx_logs"; New-Item -ItemType Directory -Force $CTL, $SL | Out-Null
function SLog($m) { ("{0} {1}" -f (Get-Date -Format 'HH:mm:ss'), $m) | Out-File -Append -Encoding ascii "$SL\supervisor_v3.txt" }
try { (Get-Process -Id $PID).PriorityClass = (Get-BgLimits).supervisor_priority } catch {}
function RunChild([string]$file, [string]$argline) {
  $p = Start-Hidden $PS ("-NoProfile -NonInteractive -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$file`" $argline") $E 'BelowNormal' 0
  [void]$p.WaitForExit()
}
function StartBg([string]$file, [string]$argline, [string]$prio) {
  return Start-Hidden $PS ("-NoProfile -NonInteractive -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$file`" $argline") $E $prio 0
}
SLog "supervisor_v3 start pid $PID"
# telemetry (read-only, Idle), once
$tp = $null; $tpf = "$CTL\telemetry.pid"
try { if (Test-Path $tpf) { $old = Get-Process -Id ([int](Get-Content $tpf)) -ErrorAction SilentlyContinue; if ($old) { $tp = $old } } } catch {}
if (-not $tp) { $tp = StartBg "$E\staged_v5\telemetry.ps1" '' 'Idle'; $tp.Id | Out-File -Encoding ascii $tpf; SLog "telemetry started pid $($tp.Id)" }
while ($true) {
  (Get-Date -Format s) | Out-File -Encoding ascii "$CTL\supervisor.alive"
  foreach ($f in (Get-ChildItem "$CTL\*.req" -ErrorAction SilentlyContinue)) {
    $act = $f.BaseName; $arg = ''
    try { $arg = (Get-Content $f.FullName -Raw -ErrorAction SilentlyContinue).Trim() } catch {}
    Remove-Item $f.FullName -Force -ErrorAction SilentlyContinue
    SLog "request $act '$arg'"
    if ($act -eq 'restart') {
      if ($arg -match '^[a-z0-9_]+$' -and $arg -ne 'restart' -and $arg -ne 'buildcheck') { Set-Content -Encoding ascii "$E\map.txt" $arg }
      RunChild "$E\staged_v5\sandbox_run_v5b.ps1" '-NoSupervisor'
    }
    elseif ($act -eq 'buildcheck') { RunChild "$E\staged_v5\sandbox_run_v5b.ps1" '-BuildCheck' }
    elseif ($act -eq 'probe') { $sec = 120; if ($arg -match '^\d+$') { $sec = [int]$arg }; [void](StartBg "$E\staged_v5\probe_windows.ps1" "-Seconds $sec" 'Idle') }
    elseif ($act -eq 'stop') { Get-Process deadworks -ErrorAction SilentlyContinue | Stop-Process -Force }
    elseif ($act -eq 'quit') { try { Stop-Process -Id $tp.Id -Force -ErrorAction SilentlyContinue; Remove-Item $tpf -Force -ErrorAction SilentlyContinue } catch {}; SLog 'quit'; exit }
  }
  Start-Sleep 3
}
