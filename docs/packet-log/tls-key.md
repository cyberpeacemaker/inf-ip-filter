
# troubleshooting
```powershell
setx SSLKEYLOGFILE "$env:USERPROFILE\Desktop\sslkeys.log"
$env:SSLKEYLOGFILE = "$env:USERPROFILE\Desktop\sslkeys.log"
Get-ChildItem env:SSLKEYLOGFILE
Stop-Process -Name chrome -ErrorAction SilentlyContinue
& "C:\Program Files\Google\Chrome\Application\chrome.exe"
```
Likely CauseSolutionPermissionsMove path from C:\ to $env:USERPROFILE\Desktop\sslkeys.log.Active ProcessesUse Stop-Process -Name chrome to ensure a fresh start.ScopeRemember: $env:VAR = 'val' only lasts for that specific PowerShell window.

# tshark
```
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files\Wireshark", "Machine")
New-Item -ItemType Directory -Path "C:\logs" -Force
& "C:\Program Files\Wireshark\tshark.exe" -D
& "C:\Program Files\Wireshark\tshark.exe" -i 4 -f "ether host 34:6F:24:C9:FA:01" -b filesize:102400 -b files:10 -w "C:\Users\sinceremony\Documents\2026-03-09-wireshark\mycapture.pcapng"

```
---

# Variable

```powershell 
Get-ChildItem env: | Sort-Object -Property Name
setx SSLKEYLOGFILE "%USERPROFILE%\sslkeys.log"
Get-ChildItem env:SSLKEYLOGFILE
```

chrome://version
---

# Wireshark TLS decrypt
First, after right-clicking anywhere, choose “Protocol Preferences.” From the submenu, select “Transport Layer Security.” Thirdly, click on “Open Transport Layer Security preferences.”

1. per-session secrets && star
<!-- setx SSLKEYLOGFILE "%USERPROFILE%\sslkeys.log"
$env:SSLKEYLOGFILE = "%USERPROFILE%\sslkeys.log" -->
setx SSLKEYLOGFILE "C:\sslkeys.log"
$env:SSLKEYLOGFILE = "C:\sslkeys.log"

Start-Process "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
Start-Process "C:\Program Files\Google\Chrome\Application\chrome.exe"

2. Edit > Preferences > Protocols > TLS
Set “(Pre)-Master-Secret log filename” (older Wireshark call this “RSA keys list” separately) to the path of sslkeys.log.

# Example steps summary (Windows, Edge)

1. Close Edge.
2. In PowerShell: `setx SSLKEYLOGFILE "%USERPROFILE%\sslkeys.log"`
3. Start Edge, reproduce the interaction you want to capture.
4. In Wireshark: set TLS `(Pre)-Master-Secret log filename` to `%USERPROFILE%\sslkeys.log`.
5. Capture traffic (or open pcap). Decrypted TLS application data should appear.

---

# MISC

(Pre)-Master-Secret log filename: /path/to/ssl-key.log

```
chromium --ssl-key-log-file=~/ssl-key.log
"C:\Program Files\Google\Chrome\Application\chrome.exe" --ssl-key-log-file="C:\path\to\ssl-key.log"
"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --ssl-key-log-file="%USERPROFILE%\sslkeys.log"
```

& "C:\Program Files\Google\Chrome\Application\chrome.exe" --ssl-key-log-file="$env:USERPROFILE\desktop\sslkeys.log"