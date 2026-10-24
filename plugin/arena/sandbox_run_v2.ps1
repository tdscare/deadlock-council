# Fast start: (no download) disable Academy plugin, rebuild Sandbox Tester, start server, launch Deadlock and auto-connect.
param([switch]$NoSupervisor)
$ErrorActionPreference = 'Continue'
$ProgressPreference = 'SilentlyContinue'
$E    = 'E:\deadworks-server'
$LOG  = "$E\sbx_logs"
$GAME = 'F:\steamlibrary\steamapps\common\deadlock\game'
$WIN  = "$GAME\bin\win64"
$MAN  = "$WIN\managed"
New-Item -ItemType Directory -Force $LOG, "$E\sbx_cmd", "$E\academy_off" | Out-Null
$out = "$LOG\run.txt"
function Log($m) { ("{0} {1}" -f (Get-Date -Format 'HH:mm:ss'), $m) | Out-File -Append -Encoding ascii $out }
Log 'start'
# BUILD-CHECK MODE: ctl\restart.req containing 'buildcheck' makes the supervisor write map.txt='buildcheck'. Then ONLY compile to out_check\ (never deployed), do not touch the running server/client/plugins, restore map.txt, exit.
$mapf = "$E\map.txt"
if ((Test-Path $mapf) -and ((Get-Content $mapf -TotalCount 1).Trim() -eq 'buildcheck')) {
  Set-Content -Encoding ascii $mapf 'dl_midtown'
  $bc = "$E\SandboxTester\out_check"
  try {
    if (Test-Path $bc) { Remove-Item $bc -Recurse -Force }
    & dotnet build "$E\SandboxTester\SandboxTester.csproj" -c Release -nologo "-p:ManagedDir=$MAN" -o $bc *> "$LOG\build_check.txt"
    if (Test-Path "$bc\SandboxTester.dll") { Log 'BUILDCHECK ok (not deployed)' } else { Log 'BUILDCHECK FAILED (see build_check.txt)' }
  } catch { Log ("BUILDCHECK error: " + $_) }
  exit
}
if (-not $NoSupervisor) {
  $alive = "$E\ctl\supervisor.alive"
  $fresh = (Test-Path $alive) -and (((Get-Date) - (Get-Item $alive).LastWriteTime).TotalSeconds -lt 15)
  if (-not $fresh) { Start-Process powershell -WindowStyle Hidden -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-File',"$E\supervisor.ps1"; Log 'supervisor started' }
}
Get-Process deadworks -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep 2
# Academy plugin off while testing (draws boxes, not wanted); SANDBOX_STOP.bat puts it back
if (Test-Path "$MAN\plugins\DeadlockAcademy.dll") { Move-Item "$MAN\plugins\DeadlockAcademy.dll" "$E\academy_off\" -Force; Log 'academy disabled' }
Get-ChildItem "$E\sbx_cmd" -File -ErrorAction SilentlyContinue | Remove-Item -Force
# build + deploy plugin
try {
  $b = "$E\SandboxTester\out"
  if (Test-Path $b) { Remove-Item $b -Recurse -Force }
  & dotnet build "$E\SandboxTester\SandboxTester.csproj" -c Release -nologo "-p:ManagedDir=$MAN" -o $b *> "$LOG\build.txt"
  if (Test-Path "$b\SandboxTester.dll") { Copy-Item "$b\SandboxTester.dll" "$MAN\plugins\" -Force; Log 'plugin built' } else { Log 'ERROR plugin build failed' }
} catch { Log ("ERROR build: " + $_) }
# server
$env:SBX_LOG_DIR = $LOG
$map = 'dl_midtown'
if (Test-Path "$E\map.txt") { $map = (Get-Content "$E\map.txt" -TotalCount 1).Trim() }
$srv = "-dedicated -console -insecure -allow_no_lobby_connect -maxplayers 12 -nomaster +hostport 27067 +tv_citadel_auto_record 0 +spec_replay_enable 0 +tv_enable 0 +citadel_upload_replay_enabled 0 +sv_cheats 1 +sv_hibernate_when_empty 0 +map $map"
Remove-Item "$LOG\server_stdout.log","$LOG\server_stderr.log" -Force -ErrorAction SilentlyContinue
$p = Start-Process -FilePath "$WIN\deadworks.exe" -ArgumentList $srv -WorkingDirectory $WIN -PassThru -RedirectStandardOutput "$LOG\server_stdout.log" -RedirectStandardError "$LOG\server_stderr.log"
Log "server started ($map)"
# wait for map up (max 90 s)
$up = $false
for ($i=0; $i -lt 90; $i++) {
  Start-Sleep 1
  if ($p.HasExited) { Log ("server exited, code " + $p.ExitCode); break }
  if (Select-String -Path "$LOG\server_stdout.log" -Pattern 'player server started' -Quiet -ErrorAction SilentlyContinue) { $up = $true; break }
}
if ($up) {
  Log 'server up'
  if (Get-Process deadlock -ErrorAction SilentlyContinue) { Log 'Deadlock already running: type  connect localhost:27067  in its console' }
  else { Start-Process 'steam://run/1422450//+connect localhost:27067 -console'; Log 'client launched with auto-connect' }
}
Log 'end'
