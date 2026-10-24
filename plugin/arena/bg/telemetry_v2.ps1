# telemetry_v2.ps1 - read-only sampler, Idle priority, hidden. Writes E:\deadworks-server\sbx_logs\telemetry.csv; errors go to telemetry_err.txt (v1 wrote only blank lines).
Add-Type -Namespace W -Name U -MemberDefinition '[DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow(); [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);'
try { (Get-Process -Id $PID).PriorityClass = 'Idle' } catch {}
$E = 'E:\deadworks-server'; $f = "$E\sbx_logs\telemetry.csv"; $ef = "$E\sbx_logs\telemetry_err.txt"
function ELog($m) { ("{0} {1}" -f (Get-Date -Format 'HH:mm:ss'), $m) | Out-File -Append -Encoding ascii $ef }
$iv = 10; try { $j = Get-Content "$E\ctl\bg_limits.json" -Raw | ConvertFrom-Json; if ($j.telemetry_interval_s) { $iv = [int]$j.telemetry_interval_s } } catch {}
$hdr = 'utc,cpu_total,mem_avail_mb,disk_busy_pct,proc_queue,gpu3d_pct,fg_pid,fg_name,dw_cpu,dw_ws_mb,dl_cpu,dl_ws_mb,ow_cpu,dotnet_cpu,ps_cpu,top1,top2,top3'
if (-not (Test-Path $f)) { $hdr | Out-File -Encoding ascii $f }
$prev = @{}; $ncpu = [Environment]::ProcessorCount; $t0 = Get-Date
ELog "telemetry_v2 start pid $PID interval $iv"
while ($true) {
  try {
    $now = Get-Date; $dt = ($now - $t0).TotalSeconds; if ($dt -lt 1) { $dt = 1 }; $t0 = $now
    $cpu = ''; $mem = ''; $disk = ''; $q = ''; $gpu = ''
    try { $c = (Get-Counter '\Processor(_Total)\% Processor Time','\Memory\Available MBytes','\PhysicalDisk(_Total)\% Disk Time','\System\Processor Queue Length' -ErrorAction Stop).CounterSamples
          foreach ($s in $c) { $p = $s.Path
            if ($p -like '*processor(_total)*') { $cpu = [math]::Round($s.CookedValue, 1) }
            elseif ($p -like '*available mbytes*') { $mem = [math]::Round($s.CookedValue) }
            elseif ($p -like '*disk time*') { $disk = [math]::Round($s.CookedValue, 1) }
            elseif ($p -like '*queue length*') { $q = $s.CookedValue } } } catch { ELog "counter: $($_.Exception.Message)" }
    try { $g = (Get-Counter '\GPU Engine(*engtype_3D)\Utilization Percentage' -ErrorAction Stop).CounterSamples | Measure-Object CookedValue -Sum; $gpu = [math]::Round($g.Sum, 1) } catch {}
    $fgpid = 0; $fgn = ''
    try { $h = [W.U]::GetForegroundWindow(); $tmp = [uint32]0; [void][W.U]::GetWindowThreadProcessId($h, [ref]$tmp); $fgpid = [int]$tmp; $fgn = (Get-Process -Id $fgpid -ErrorAction Stop).ProcessName } catch {}
    $cur = @{}; $names = @{}; $ws = @{}
    foreach ($p in (Get-Process)) { try { $cur[$p.Id] = $p.TotalProcessorTime.TotalSeconds; $names[$p.Id] = $p.ProcessName; $ws[$p.Id] = $p.WorkingSet64 } catch {} }
    $pc = @{}   # percent of whole machine per process id
    foreach ($id in $cur.Keys) { if ($prev.ContainsKey($id)) { $pc[$id] = ($cur[$id] - $prev[$id]) / $dt * 100 / $ncpu } }
    $prev = $cur
    $agg = @{ dw = @(0.0, 0.0); dl = @(0.0, 0.0); ow = @(0.0, 0.0); dn = @(0.0, 0.0); ps = @(0.0, 0.0) }
    foreach ($id in $names.Keys) {
      $n = $names[$id]; $k = $null
      if ($n -eq 'deadworks') { $k = 'dw' } elseif ($n -eq 'project8' -or $n -like 'deadlock*') { $k = 'dl' } elseif ($n -like 'Overwatch*') { $k = 'ow' } elseif ($n -eq 'dotnet') { $k = 'dn' } elseif ($n -eq 'powershell') { $k = 'ps' }
      if ($k) { if ($pc.ContainsKey($id)) { $agg[$k][0] += $pc[$id] }; $agg[$k][1] += $ws[$id] / 1MB }
    }
    $top = @(); foreach ($e in ($pc.GetEnumerator() | Sort-Object Value -Descending | Select-Object -First 3)) { $top += ('{0}:{1:N1}' -f $names[$e.Key], $e.Value) }
    while ($top.Count -lt 3) { $top += '' }
    $r = { param($x) [math]::Round($x, 1) }
    $row = @((Get-Date).ToUniversalTime().ToString('s'), $cpu, $mem, $disk, $q, $gpu, $fgpid, $fgn, (& $r $agg.dw[0]), [math]::Round($agg.dw[1]), (& $r $agg.dl[0]), [math]::Round($agg.dl[1]), (& $r $agg.ow[0]), (& $r $agg.dn[0]), (& $r $agg.ps[0]), $top[0], $top[1], $top[2])
    ($row -join ',') | Out-File -Append -Encoding ascii $f
  } catch { ELog "row: $($_.Exception.Message)" }
  Start-Sleep $iv
}
