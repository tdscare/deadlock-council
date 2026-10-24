' launcher_hidden_v2.vbs - starts the hidden supervisor (window style 0 = hidden, not activated). Double-click once.
Set sh = CreateObject("WScript.Shell")
sh.Run "powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -WindowStyle Hidden -File ""E:\deadworks-server\staged_v5\supervisor_v3.ps1""", 0, False
