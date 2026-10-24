# probe_windows.ps1 - STAGED, NOT ACTIVE, UNTESTED. READ-ONLY proof that our processes show no window and cause no focus change. Run only with permission, ideally started just BEFORE a permitted test.
# Usage: probe_windows.ps1 -Seconds 60 -Names deadworks,dotnet,cmd,conhost,powershell,wscript,VBCSCompiler,MSBuild
# Every 100 ms: foreground window handle/pid/name (changes are logged), plus every 2 s: for each process of interest, MainWindowHandle and ALL top-level windows it owns (visible flag). Writes sbx_logs\focus_probe.txt. It sends no input and changes nothing.
param([int]$Seconds = 60, [string[]]$Names = @('deadworks','dotnet','cmd','conhost','powershell','wscript','VBCSCompiler','MSBuild'))
Add-Type -Namespace W -Name P -MemberDefinition @'
[DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
[DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);
[DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
public delegate bool EnumProc(IntPtr h, IntPtr l);
[DllImport("user32.dll")] public static extern bool EnumWindows(EnumProc cb, IntPtr l);
'@
try { (Get-Process -Id $PID).PriorityClass = 'Idle' } catch {}
$out = 'E:\deadworks-server\sbx_logs\focus_probe.txt'
function L($m) { ("{0} {1}" -f (Get-Date).ToUniversalTime().ToString('HH:mm:ss.fff'), $m) | Out-File -Append -Encoding ascii $out }
function FgDesc { $h = [W.P]::GetForegroundWindow(); $p = 0; [void][W.P]::GetWindowThreadProcessId($h, [ref]$p); $n = ''; try { $n = (Get-Process -Id $p -ErrorAction Stop).ProcessName } catch {}; return "hwnd=$h pid=$p name=$n" }
L "PROBE start $Seconds s names=$($Names -join ',') foreground: $(FgDesc)"
$last = FgDesc; $end = (Get-Date).AddSeconds($Seconds); $next = Get-Date; $fgChanges = 0
while ((Get-Date) -lt $end) {
  $fg = FgDesc; if ($fg -ne $last) { $fgChanges++; L "FOREGROUND CHANGE: $last -> $fg"; $last = $fg }
  if ((Get-Date) -ge $next) {
    $next = (Get-Date).AddSeconds(2)
    $pids = @{}; foreach ($n in $Names) { foreach ($p in (Get-Process -Name $n -ErrorAction SilentlyContinue)) { $pids[[uint32]$p.Id] = $p } }
    $wins = New-Object System.Collections.ArrayList
    $cb = [W.P+EnumProc]{ param($h, $l) $pp = 0; [void][W.P]::GetWindowThreadProcessId($h, [ref]$pp); if ($pids.ContainsKey([uint32]$pp)) { [void]$wins.Add(@($pp, $h, [W.P]::IsWindowVisible($h))) }; return $true }
    [void][W.P]::EnumWindows($cb, [IntPtr]::Zero)
    foreach ($id in $pids.Keys) { $p = $pids[$id]; $mine = @($wins | Where-Object { $_[0] -eq $id }); $vis = @($mine | Where-Object { $_[2] }).Count; L ("PROC {0} pid={1} MainWindowHandle={2} topLevelWindows={3} visible={4}" -f $p.ProcessName, $id, $p.MainWindowHandle, $mine.Count, $vis) }
  }
  Start-Sleep -Milliseconds 100
}
L "PROBE end; foreground changes seen: $fgChanges"
