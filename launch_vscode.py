import subprocess, os
vscode = r"C:\Users\Mahboobian\AppData\Local\Programs\Microsoft VS Code\Code.exe"
ws = r"C:\Users\Mahboobian\Documents\VPP_Article6_Project\VPP_Article6.code-workspace"
subprocess.Popen([vscode, ws])
print("launched VS Code on", ws)
