$o = 'E:\deadworks-server\sbx_logs\proc_audit.txt'
$s = @(Get-CimInstance Win32_Process -Filter "Name='powershell.exe'" | Where-Object { $_.CommandLine -like '*supervisor_v3.ps1*' } | Sort-Object CreationDate)
"dedupe $(Get-Date -Format s): supervisors found: $(($s | ForEach-Object { $_.ProcessId }) -join ',')" | Out-File -Append -Encoding ascii $o
for ($i = 1; $i -lt $s.Count; $i++) { Stop-Process -Id $s[$i].ProcessId -Force -ErrorAction SilentlyContinue; "killed duplicate supervisor pid $($s[$i].ProcessId); kept $($s[0].ProcessId)" | Out-File -Append -Encoding ascii $o }
