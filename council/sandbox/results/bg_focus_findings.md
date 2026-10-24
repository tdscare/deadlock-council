VALID: yes (passive telemetry from plugin.log UCSTAT lines; no experiment result)
SCOPE: instrument reliability only; no balance claim
ENV: mixed (natural foreground/background samples from 209 UCSTAT blocks, 2026-10-23..24)

# Background vs foreground: findings (14:10)
## Measured (209 UCSTAT blocks >=4 s, >=200 server frames, with foreground sampling)
| client state (fgPct) | blocks | server frames with NO human usercmd | usercmd gap p99 | calls/s |
|---|---|---|---|---|
| background 0% | 179 | mean 49.3% (29-88) | 91 ms | 58.9 |
| 1-50% foreground | 10 | 30.1% | 57 ms | 62.8 |
| 51-99% | 9 | 11.7% | 39 ms | 64.0 |
| foreground 100% | 11 | 0.8% (0-4) | 21 ms | 64.2 |
Dose-response with time in foreground => the burstiness is caused by the client being unfocused, not by server load (server tick avg 0.33 ms/s display cost, frames identical).
## Ruled out
- Windows EcoQoS/power throttling of deadlock.exe: GetProcessInformation(ProcessPowerThrottling) controlMask=1 stateMask=0 (explicitly NOT throttled); priority class Normal; process CPU 11-42% of one core (not CPU-bound). Log: PROCINFO 14:05:13.
## Cvar fix from the plugin (task A)
- API: Server.ClientCommand(slot, text) exists ("Sends a console command to the client in the given slot"). Plugin command sbx_cc added.
- Tested 14:02:31 `sbx_probe_unknown 1` and `say SBX_CC_PROBE` (commands that would show up in OnClientConCommand / chat if the client ran them): NOTHING came back (no CLIENTCMD log line, no chat). Sent `engine_no_focus_sleep 0` 14:03:01: empty-frame share after 46-62% (before 60-65%) = no effect.
- No API reads a client cvar back (fps_max, fps_max_ui, engine_no_focus_sleep cannot be printed into plugin.log). Conclusion: not possible from the plugin; the engine blocks or ignores server-sent commands here.
- Alternative needing Kieran's approval (NOT done): create/append `engine_no_focus_sleep 0` in <Deadlock install>\game\citadel\cfg\autoexec.cfg, effective at next Deadlock launch. Not yet proven to be the cause (cvar named in engine2.dll; Windows throttling excluded).
## Verdict
Background testing is NOT declared standard. Unreliable in background: anything whose timing depends on per-tick client input arrival (cooldown/proc/uptime effects, A/A on proc items, burst fire cycles during starved ticks). Earlier shots/per-hit damage equality still holds. Need: foreground-equivalent runs (autoexec cvar or Kieran foreground) before ENV: background can be baseline.
