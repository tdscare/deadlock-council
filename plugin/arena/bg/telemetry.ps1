# telemetry.ps1 - STAGED, NOT ACTIVE, UNTESTED. Read-only low-overhead sampler (Idle priority, hidden). Writes E:\deadworks-server\sbx_logs\telemetry.csv every N s (default 10).
# Columns: utc,cpu_total,mem_avail_mb,disk_busy_pct,proc_queue,gpu3d_pct,fg_pid,fg_name,dw_cpu,dw_ws_mb,dl_cpu,dl_ws_mb,ow_cpu,dotnet_cpu,ps_cpu,top1,top2,top3
Add-Type -Namespace W -Name U -MemberDefinition '[DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow(); [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);'
try { (Get-Process -Id $PID).PriorityClass = 'Idle' } catch {}
$E = 'E:\deadworks-server'; $f = "$E\sbx_logs\telemetry.csv"
$iv = 10; try { $j = Get-Content "$E\ctl\bg_limits.json" -Raw | ConvertFrom-Json; if ($j.telemetry_interval_s) { $iv = [int]$j.telemetry_interval_s } } catch {}
if (-not (Test-Path $f)) { 'utc,cpu_total,mem_avail_mb,disk_busy_pct,proc_queue,gpu3d_pct,fg_pid,fg_name,dw_cpu,dw_ws_mb,dl_cpu,dl_ws_mb,ow_cpu,dotnet_cpu,ps_cpu,top1,top2,top3' | Out-File -Encoding ascii $f }
$prev = @{}; $ncpu = [Environment]::ProcessorCount; $t0 = Get-Date
function Cpu($ps) { $s = 0.0; foreach ($p in $ps) { try { $s += $p.TotalProcessorTime.TotalSeconds } catch {} }; return $s }
while ($true) {
  $now = Get-Date; $dt = ($now - $t0).TotalSeconds; if ($dt -lt 1) { $dt = 1 }; $t0 = $now
  $c = $null; try { $c = (Get-Counter '\Processor(_Total)\% Processor Time','\Memory\Available MBytes','\PhysicalDisk(_Total)\% Disk Time','\System\Processor Queue Length' -ErrorAction Stop).CounterSamples } catch {}
  $gpu = ''; try { $g = (Get-Counter '\GPU Engine(*engtype_3D)\Utilization Percentage' -ErrorAction Stop).CounterSamples | Measure-Object CookedValue -Sum; $gpu = [math]::Round($g.Sum, 1) } catch {}
  $fgpid = 0; $fgn = ''; try { $h = [W.U]::GetForegroundWindow(); $tmp = 0; [void][W.U]::GetWindowThreadProcessId($h, [ref]$tmp); $fgpid = $tmp; $fgn = (Get-Process -Id $tmp -ErrorAction SilentlyContinue).ProcessName } catch {}
  $all = Get-Process; $cur = @{}; foreach ($p in $all) { try { $cur[$p.Id] = @($p.ProcessName, $p.TotalProcessorTime.TotalSeconds) } catch {} }
  $d = @{}; foreach ($id in $cur.Keys) { if ($prev.ContainsKey($id)) { $d[$id] = @($cur[$id][0], ($cur[$id][1] - $prev[$id][1]) / $dt * 100 / $ncpu) } }
  $prev = $cur
  function Sum($n) { $s = 0.0; foreach ($v in $d.Values) { if ($v[0] -like $n) { $s += $v[1] } }; return [math]::Round($s, 1) }
  function Ws($n) { $s = 0.0; foreach ($p in ($all | Where-Object { $_.ProcessName -like $n })) { $s += $p.WorkingSet64 / 1MB }; return [math]::Round($s) }
  $top = ($d.GetEnumerator() | Sort-Object { $_.Value[1] } -Descending | Select-Object -First 3 | ForEach-Object { '{0}:{1:N1}' -f $_.Value[0], $_.Value[1] })
  $row = @((Get-Date).ToUniversalTime().ToString('s'), $(if ($c) { [math]::Round($c[0].CookedValue, 1) }), $(if ($c) { [math]::Round($c[1].CookedValue) }), $(if ($c) { [math]::Round($c[2].CookedValue, 1) }), $(if ($c) { $c[3].CookedValue }), $gpu, $fgpid, $fgn, (Sum 'deadworks'), (Ws 'deadworks'), (Sum 'deadlock'), (Ws 'deadlock'), (Sum 'Overwatch*'), (Sum 'dotnet'), (Sum 'powershell'), $top[0], $top[1], $top[2])
  ($row -join ',') | Out-File -Append -Encoding ascii $f
  Start-Sleep $iv
}
