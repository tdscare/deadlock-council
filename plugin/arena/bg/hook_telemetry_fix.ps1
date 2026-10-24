# one-shot hook (run through buildcheck.req -> v5b): process audit + replace the broken telemetry with telemetry_v2. Read-only except the telemetry swap.
$E = 'E:\deadworks-server'; $L = "$E\sbx_logs"; $o = "$L\proc_audit.txt"
"== audit $(Get-Date -Format s)" | Out-File -Append -Encoding ascii $o
foreach ($n in 'powershell','wscript','cscript','cmd','deadworks','dotnet') { foreach ($p in (Get-CimInstance Win32_Process -Filter "Name='$n.exe'" -ErrorAction SilentlyContinue)) { ("{0} pid={1} ppid={2} cmd={3}" -f $p.Name, $p.ProcessId, $p.ParentProcessId, ($p.CommandLine -replace '\s+',' ')) | Out-File -Append -Encoding ascii $o } }
$tpf = "$E\ctl\telemetry.pid"
try { $old = [int](Get-Content $tpf); Stop-Process -Id $old -Force -ErrorAction SilentlyContinue; "old telemetry $old stopped" | Out-File -Append -Encoding ascii $o } catch {}
Start-Sleep 1
if (Test-Path "$L\telemetry.csv") { Move-Item "$L\telemetry.csv" "$L\telemetry_v1_blank.csv" -Force }
$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe"
$psi.Arguments = "-NoProfile -NonInteractive -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$E\staged_v5\telemetry_v2.ps1`""
$psi.UseShellExecute = $false; $psi.CreateNoWindow = $true; $psi.WindowStyle = 'Hidden'
$p = [System.Diagnostics.Process]::Start($psi); try { $p.PriorityClass = 'Idle' } catch {}
$p.Id | Out-File -Encoding ascii $tpf
"telemetry_v2 started pid $($p.Id)" | Out-File -Append -Encoding ascii $o
