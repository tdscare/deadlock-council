' launcher_hidden.vbs - STAGED, NOT ACTIVE. Starts the supervisor with window style 0 (hidden, no activation). Intended for a per-user logon scheduled task or Startup shortcut (both need Kieran's one-time approval).
Set sh = CreateObject("WScript.Shell")
sh.Run "powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -WindowStyle Hidden -File ""E:\deadworks-server\staged_v5\supervisor_v2.ps1""", 0, False
