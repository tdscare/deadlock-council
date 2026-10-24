# sandbox_run_v5_hidden.ps1 - STAGED, NOT ACTIVE, UNTESTED. Nonintrusive replacement for sandbox_run.ps1.
#  -BuildCheck : isolated low-priority compile to out_check only (no kill/start/deploy).
#  default     : (re)start the Sandbox server HIDDEN with the VERIFIED build; never launches/focuses Deadlock; never runs the compiler unless sources changed.
param([switch]$NoSupervisor, [switch]$BuildCheck)
. 'E:\deadworks-server\staged_v5\bg_common.ps1'
$ErrorActionPreference = 'Continue'; $ProgressPreference = 'SilentlyContinue'
$LOG = "$E\sbx_logs"; $GAME = 'F:\steamlibrary\steamapps\common\deadlock\game'; $WIN = "$GAME\bin\win64"; $MAN = "$WIN\managed"
New-Item -ItemType Directory -Force $LOG, "$E\sbx_cmd", "$E\academy_off", "$E\SandboxTester\registry" | Out-Null
$out = "$LOG\run.txt"
function Log($m) { ("{0} {1}" -f (Get-Date -Format 'HH:mm:ss'), $m) | Out-File -Append -Encoding ascii $out }
try { (Get-Process -Id $PID).PriorityClass = 'BelowNormal' } catch {}
Log 'v5 start'
$lim = Get-BgLimits
# A/B-test kill-switch file from the display experiment is the only display_off this script ever removes
$dof = "$CTL\display_off"
if ((Test-Path $dof) -and ((Get-Content $dof -Raw) -match 'A/B test')) { Remove-Item $dof -Force; Log 'A/B-test display_off removed' }

$srcHash = Get-SourceHash
$reg = "$E\SandboxTester\registry\verified_builds.csv"      # sourceHash,dllSha256,utc,how   (a row is written only after a build + metadata check passed)
$verified = $null
if (Test-Path $reg) { $verified = Import-Csv $reg -Header sourceHash,dllSha256,utc,how | Where-Object { $_.sourceHash -eq $srcHash } | Select-Object -Last 1 }

if ($BuildCheck) {
  $bc = "$E\SandboxTester\out_check"
  $ok = Invoke-IsolatedBuild $bc "$LOG\build_check.txt" $MAN
  if ($ok) {
    $h = (Get-FileHash "$bc\SandboxTester.dll" -Algorithm SHA256).Hash
    # metadata scan: the compiled DLL must not reference the crash-prone world-text API
    $bytes = [IO.File]::ReadAllBytes("$bc\SandboxTester.dll"); $txt = [Text.Encoding]::ASCII.GetString($bytes)
    $bad = ($txt.Contains('CPointWorldText') -or $txt.Contains('point_worldtext'))
    if ($bad) { Log "BUILDCHECK ok but REJECTED: DLL references CPointWorldText ($h)" }
    else { "$srcHash,$h,$(Get-Date -Format s),buildcheck" | Out-File -Append -Encoding ascii $reg; Log "BUILDCHECK ok (not deployed) sha256=$h source=$srcHash" }
  } else { Log 'BUILDCHECK FAILED (see build_check.txt)' }
  exit
}

# ---- normal start ----
Get-Process deadworks -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep 2
if (Test-Path "$MAN\plugins\DeadlockAcademy.dll") { Move-Item "$MAN\plugins\DeadlockAcademy.dll" "$E\academy_off\" -Force; Log 'academy disabled' }
Get-ChildItem "$E\sbx_cmd" -File -ErrorAction SilentlyContinue | Remove-Item -Force
if ($null -eq $verified) {
  Log "no verified build for source $srcHash - compiling (isolated, low priority)"
  $b = "$E\SandboxTester\out"
  if (-not (Invoke-IsolatedBuild $b "$LOG\build.txt" $MAN)) { Log 'ERROR plugin build failed - server NOT started (old DLL never used as fallback)'; exit }
  $bytes = [IO.File]::ReadAllBytes("$b\SandboxTester.dll"); $txt = [Text.Encoding]::ASCII.GetString($bytes)
  if ($txt.Contains('CPointWorldText') -or $txt.Contains('point_worldtext')) { Log 'ERROR built DLL references CPointWorldText - server NOT started'; exit }
  $h = (Get-FileHash "$b\SandboxTester.dll" -Algorithm SHA256).Hash
  "$srcHash,$h,$(Get-Date -Format s),restart" | Out-File -Append -Encoding ascii $reg
  Copy-Item "$b\SandboxTester.dll" "$MAN\plugins\" -Force
} else { Log "verified build reused (no compile): dll sha256=$($verified.dllSha256)" }
$dep = (Get-FileHash "$MAN\plugins\SandboxTester.dll" -Algorithm SHA256).Hash
$want = if ($verified) { $verified.dllSha256 } else { $h }
Log "plugin sha256 deployed=$dep expected=$want"
if ($dep -ne $want) {
  # deploy the verified DLL from out/ or out_check/ if it matches, otherwise refuse
  $cand = @("$E\SandboxTester\out\SandboxTester.dll", "$E\SandboxTester\out_check\SandboxTester.dll") | Where-Object { (Test-Path $_) -and ((Get-FileHash $_ -Algorithm SHA256).Hash -eq $want) } | Select-Object -First 1
  if ($cand) { Copy-Item $cand "$MAN\plugins\SandboxTester.dll" -Force; Log "deployed verified DLL from $cand" } else { Log 'ERROR no DLL matching the verified hash - server NOT started'; exit }
}
$env:SBX_LOG_DIR = $LOG
$map = 'dl_midtown'; if (Test-Path "$E\map.txt") { $m = (Get-Content "$E\map.txt" -TotalCount 1).Trim(); if ($m -match '^[a-z0-9_]+$' -and $m -ne 'restart' -and $m -ne 'buildcheck') { $map = $m } }
$srv = "-dedicated -console -insecure -allow_no_lobby_connect -maxplayers 12 -nomaster +hostport 27067 +tv_citadel_auto_record 0 +spec_replay_enable 0 +tv_enable 0 +citadel_upload_replay_enabled 0 +sv_cheats 1 +sv_hibernate_when_empty 0 +map $map"
Remove-Item "$LOG\server_stdout.log", "$LOG\server_stderr.log" -Force -ErrorAction SilentlyContinue
# HIDDEN start through cmd.exe redirection; the exact deadworks.exe window behaviour of -console is UNVERIFIED -> run probe_windows.ps1 on the first permitted test.
$cp = Start-HiddenRedirect "$WIN\deadworks.exe" $srv $WIN "$LOG\server_stdout.log" "$LOG\server_stderr.log" $lim.server_priority ([int64]$lim.server_affinity_mask)
Log "server launch requested hidden (cmd pid $($cp.Id), map $map, priority $($lim.server_priority))"
Start-Sleep 3
$dw = Get-Process deadworks -ErrorAction SilentlyContinue | Select-Object -First 1
if ($dw) { try { $dw.PriorityClass = $lim.server_priority; if ([int64]$lim.server_affinity_mask -gt 0) { $dw.ProcessorAffinity = [IntPtr][int64]$lim.server_affinity_mask } } catch {}; Log "deadworks pid $($dw.Id) priority $($dw.PriorityClass) MainWindowHandle $($dw.MainWindowHandle)" }
$up = $false
for ($i = 0; $i -lt 90; $i++) {
  Start-Sleep 1
  if ($cp.HasExited -and -not (Get-Process deadworks -ErrorAction SilentlyContinue)) { Log ("server exited, code " + $cp.ExitCode); break }
  if (Select-String -Path "$LOG\server_stdout.log" -Pattern 'player server started' -Quiet -ErrorAction SilentlyContinue) { $up = $true; break }
}
if ($up) { Log 'server up'; Log 'client NOT launched by this script (the plugin connect-assist handles hero/team after the player connects)' }
Log 'v5 end'
