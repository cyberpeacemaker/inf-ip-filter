# TODO: Path Uniform
# 1. Start Chrome with Key Logging
setx SSLKEYLOGFILE "$env:USERPROFILE\Desktop\sslkeys.log"
$env:SSLKEYLOGFILE = "$env:USERPROFILE\Desktop\sslkeys.log"
Get-ChildItem env:SSLKEYLOGFILE
# Ensure all Chrome processes are closed before running.
Stop-Process -Name chrome -ErrorAction SilentlyContinue
# chromium --ssl-key-log-file=~/ssl-key.log
# "C:\Program Files\Google\Chrome\Application\chrome.exe" --ssl-key-log-file="C:\path\to\ssl-key.log"
& "C:\Program Files\Google\Chrome\Application\chrome.exe"

# 2. Record metadata
$Timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
"--- IPCONFIG RECORDED AT $Timestamp ---" | Out-File -FilePath "$env:USERPROFILE\Desktop\host_config.txt" -Append
ipconfig /all | Out-File -FilePath "$env:USERPROFILE\Desktop\host_config.txt" -Append

### 3. Start Tshark Ring Buffer Capture
# Captures traffic only for your MAC address, rotating ten 100MB files.
# TODO: index, MAC, dst path
& "C:\Program Files\Wireshark\tshark.exe" -D
& "C:\Program Files\Wireshark\tshark.exe" -i 4 -p -f "ether host 34:6F:24:C9:FA:01" -b filesize:102400 -b files:20 -w "C:\Users\sinceremony\Documents\Forensic\2026-03-11\mycapture.pcapng"
& "C:\Program Files\Wireshark\tshark.exe" -i 4 -f "ether host 34:6F:24:C9:FA:01" -b filesize:102400 -b files:10 -w "C:\Users\sinceremony\Documents\2026-03-09-wireshark\mycapture.pcapng"
# * **Storage:** Periodically clear the `C:\logs` folder if you aren't using the ring buffer (`-b`) settings.

### 4. Export Sysmon Hunt Log (CSV)
# TODO: seperate file?
# Extracts Network (ID 3) and DNS (ID 22) events into a readable spreadsheet.
# !administrator privilege required!
$Events = Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-Sysmon/Operational'; Id=3,22}
$Results = foreach ($Event in $Events) {
    $xml = [xml]$Event.ToXml()
    $data = @{}
    foreach ($item in $xml.Event.EventData.Data) { $data[$item.Name] = $item.'#text' }
    [PSCustomObject]@{
        Time     = $Event.TimeCreated
        ID       = $Event.Id
        Process  = $data.Image
        Query    = $data.QueryName
        DestIP   = $data.DestinationIp
        DestPort = $data.DestinationPort
    }
}
$Results | Export-Csv -Path "$env:USERPROFILE\Desktop\sysmon_hunt.csv" -NoTypeInformation
# * **Update Config:** If you need to change your filters: `.\Sysmon64.exe -c newconfig.xml`

### 5. RITA
### 1. Close the "Decryption Gap" for RITA

# RITA is a powerful tool, but it does not natively use your `sslkeys.log` file. It looks at the behavior of the connection (metadata) rather than the decrypted payload.

# To get the most out of your capture, you should:

# * **Convert to Zeek Logs with Keys:** Use Zeek to process your PCAP while providing the key log. This allows Zeek to generate a detailed `http.log` from your encrypted traffic, which RITA can then analyze for malicious URI patterns or missing headers.
# * **Command Example:**
# ```bash
# zeek -r mycapture.pcapng ssl.keylog_file=sslkeys.log

# ```

##
# TODO
# Process Hacker 2 or Process Explorer: Sysmon tells you what happened in the past, but these tools let you see what is happening right now. If you see an Event ID 8 (Injection), you can use Process Hacker to inspect the memory of that PowerShell process in real-time.

# JA3 Fingerprinting (via Zeek): Since you are using Zeek, ensure you enable JA3. It allows you to identify malware based on the "fingerprint" of its TLS handshake, even if you haven't decrypted the traffic yet.