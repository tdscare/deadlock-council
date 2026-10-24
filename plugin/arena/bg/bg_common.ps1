# bg_common.ps1 - shared helpers for nonintrusive background operation. STAGED, NOT ACTIVE, UNTESTED (no PowerShell in the authoring environment).
# Rule: no child process may create a visible window or take focus. Every child is started with CreateNoWindow=true + UseShellExecute=false (CREATE_NO_WINDOW: no console window is created at all; console children inherit the hidden console).
$script:E   = 'E:\deadworks-server'
$script:CTL = "$E\ctl"
function Get-BgLimits {
  $d = @{ server_priority='BelowNormal'; server_affinity_mask=0; build_priority='Idle'; build_maxcpu=1; supervisor_priority='BelowNormal'; telemetry_priority='Idle'; telemetry_interval_s=10 }
  try { $j = Get-Content "$CTL\bg_limits.json" -Raw -ErrorAction Stop | ConvertFrom-Json; foreach ($k in @($d.Keys)) { if ($null -ne $j.$k) { $d[$k] = $j.$k } } } catch {}
  return $d
}
# Start exe hidden. $argline is the raw command line. Returns the Process (already set to $prio / $affinity when given).
function Start-Hidden([string]$exe, [string]$argline, [string]$workdir, [string]$prio = 'BelowNormal', [int64]$affinity = 0) {
  $psi = New-Object System.Diagnostics.ProcessStartInfo
  $psi.FileName = $exe; $psi.Arguments = $argline; $psi.WorkingDirectory = $workdir
  $psi.UseShellExecute = $false; $psi.CreateNoWindow = $true; $psi.WindowStyle = [System.Diagnostics.ProcessWindowStyle]::Hidden
  $p = [System.Diagnostics.Process]::Start($psi)
  try { $p.PriorityClass = $prio } catch {}
  if ($affinity -gt 0) { try { $p.ProcessorAffinity = [IntPtr]$affinity } catch {} }
  return $p
}
# Run a command line through cmd.exe so stdout/stderr go to files (no pipes to drain, no console window): "<exe>" args > out 2> err
function Start-HiddenRedirect([string]$exe, [string]$args, [string]$workdir, [string]$out, [string]$err, [string]$prio = 'BelowNormal', [int64]$affinity = 0) {
  $line = '/c ""' + $exe + '" ' + $args + ' > "' + $out + '" 2> "' + $err + '""'
  return Start-Hidden "$env:SystemRoot\System32\cmd.exe" $line $workdir $prio $affinity
}
function Get-SourceHash {
  $files = @(Get-ChildItem "$E\SandboxTester" -Filter *.cs -File) + @(Get-Item "$E\SandboxTester\SandboxTester.csproj")
  $sb = New-Object System.Text.StringBuilder
  foreach ($f in ($files | Sort-Object Name)) { [void]$sb.Append($f.Name + ':' + (Get-FileHash $f.FullName -Algorithm SHA256).Hash + ';') }
  $sha = [System.Security.Cryptography.SHA256]::Create()
  return ([BitConverter]::ToString($sha.ComputeHash([Text.Encoding]::UTF8.GetBytes($sb.ToString()))) -replace '-','')
}
# Isolated, low-priority, single-core build into $outDir. Never deploys. Returns $true if the DLL exists afterwards.
function Invoke-IsolatedBuild([string]$outDir, [string]$logFile, [string]$managedDir) {
  $lim = Get-BgLimits
  if (Test-Path $outDir) { Remove-Item $outDir -Recurse -Force }
  $env:DOTNET_CLI_TELEMETRY_OPTOUT = '1'; $env:DOTNET_NOLOGO = '1'; $env:MSBUILDDISABLENODEREUSE = '1'; $env:DOTNET_CLI_UI_LANGUAGE = 'en'
  $a = 'build "' + "$E\SandboxTester\SandboxTester.csproj" + '" -c Release -nologo -v:q -nodeReuse:false -maxcpucount:' + $lim.build_maxcpu + ' -p:UseSharedCompilation=false "-p:ManagedDir=' + $managedDir + '" -o "' + $outDir + '"'
  $p = Start-HiddenRedirect 'dotnet' $a $E $logFile ($logFile + '.err') $lim.build_priority 0
  [void]$p.WaitForExit(600000)
  return (Test-Path "$outDir\SandboxTester.dll")
}
