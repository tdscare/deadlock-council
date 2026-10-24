# supervisor_v2.ps1 - STAGED, NOT ACTIVE, UNTESTED. Hidden-capable supervisor. Requests are files in E:\deadworks-server\ctl\*.req (content = optional map name for restart; NEVER the word 'restart'):
#   restart.req  -> sandbox_run_v5_hidden.ps1 (verified build only, hidden server)       stop.req -> stop server      quit.req -> exit
#   buildcheck.req -> isolated low-priority compile to SandboxTester\out_check, nothing else
# It is itself started hidden by launcher_hidden.vbs (wscript Run style 0) and lowers its own priority. Poll 5 s (was 2 s).
. 'E:\deadworks-server\staged_v5\bg_common.ps1'
try { (Get-Process -Id $PID).PriorityClass = (Get-BgLimits).supervisor_priority } catch {}
New-Item -ItemType Directory -Force $CTL | Out-Null
function RunChild([string]$file, [string]$argline) {
  $p = Start-Hidden "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe" ("-NoProfile -NonInteractive -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$file`" $argline") $E 'BelowNormal' 0
  [void]$p.WaitForExit()
}
while ($true) {
  (Get-Date -Format s) | Out-File -Encoding ascii "$CTL\supervisor.alive"
  foreach ($f in (Get-ChildItem "$CTL\*.req" -ErrorAction SilentlyContinue)) {
    $act = $f.BaseName; $arg = ''
    try { $arg = (Get-Content $f.FullName -Raw -ErrorAction SilentlyContinue).Trim() } catch {}
    Remove-Item $f.FullName -Force -ErrorAction SilentlyContinue
    if ($act -eq 'restart') {
      if ($arg -match '^[a-z0-9_]+$' -and $arg -ne 'restart' -and $arg -ne 'buildcheck') { Set-Content -Encoding ascii "$E\map.txt" $arg }
      RunChild "$E\staged_v5\sandbox_run_v5_hidden.ps1" '-NoSupervisor'
    }
    elseif ($act -eq 'buildcheck') { RunChild "$E\staged_v5\sandbox_run_v5_hidden.ps1" '-BuildCheck' }
    elseif ($act -eq 'stop') { Get-Process deadworks -ErrorAction SilentlyContinue | Stop-Process -Force }
    elseif ($act -eq 'quit') { exit }
  }
  Start-Sleep 5
}
