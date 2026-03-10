# Encrypted Threat Hunting Stack

This project outlines a workflow for detecting and analyzing Command and Control (C2) 
communication hidden within encrypted HTTPS tunnels.

## 🛠 The Stack

### 1. SSL/TLS Decryption (`SSLKEYLOGFILE`)
* **Purpose:** Captures symmetric session keys from browsers (Chrome/Edge) to decrypt TLS traffic.
* **Setup:** Set the `%SSLKEYLOGFILE%` environment variable to log keys for Wireshark/Zeek consumption.

### 2. Network Capture (`Wireshark` / `Tshark`)
* **Purpose:** Raw packet acquisition.
* **Focus:** Capturing the "Full Duplex" conversation. Tshark is used for long-term "all-day" 
logging with ring buffers to prevent disk exhaustion.

### 3. Network Analysis (`Zeek` & `RITA`)
* **Purpose:** Protocol metadata and behavioral threat hunting.
* **Zeek:** Converts raw PCAPs into structured logs (Conn, DNS, HTTP, SSL).
* **RITA:** Analyzes Zeek logs to find Beacons, Long Connections, and DNS Tunneling.

### 4. Endpoint Attribution (`Sysmon`)
* **Purpose:** Linking network activity to specific processes.
* **Key Events:** * **ID 3:** Network Connections (Process -> Destination IP).
    * **ID 22:** DNS Queries (Process -> Domain Name).
    * **ID 8:** CreateRemoteThread (Detecting Process Injection).

---

## 🔍 Investigation Workflow

1. **Capture:** Run `Tshark` and `Sysmon` simultaneously while performing activities.
2. **Decrypt:** Open PCAP in Wireshark using the generated `sslkeys.log`.
3. **Analyze:** Import Zeek logs into RITA to identify periodic "Beaconing" patterns.
4. **Attribute:** Cross-reference suspicious network timestamps with Sysmon Event ID 3/22 
to find the exact malicious binary on the disk.

---

Adding a "Quick Commands" section is a great way to make the README functional for anyone (including "future you") who needs to restart the hunt in a few seconds.

Here is the updated **Quick Commands** section to append to your `README.md`.

---

## ⚡️ Quick Commands

### 1. Start Chrome with Key Logging

Ensure all Chrome processes are closed before running.

```powershell
$env:SSLKEYLOGFILE = "$env:USERPROFILE\Desktop\sslkeys.log"
Stop-Process -Name chrome -ErrorAction SilentlyContinue
& "C:\Program Files\Google\Chrome\Application\chrome.exe"

```

### 2. Record metedata

```powershell
$Timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
"--- IPCONFIG RECORDED AT $Timestamp ---" | Out-File -FilePath "C:\logs\host_config.txt" -Append
ipconfig /all | Out-File -FilePath "C:\logs\host_config.txt" -Append
```

### 3. Start Tshark Ring Buffer Capture

Captures traffic only for your MAC address, rotating ten 100MB files.

```powershell
# index, MAC, dst path
& "C:\Program Files\Wireshark\tshark.exe" -i 4 -f "ether host 34:6F:24:C9:FA:01" -b filesize:102400 -b files:10 -w "C:\Users\sinceremony\Documents\2026-03-09-wireshark\mycapture.pcapng"
# Change -i index to match your 'tshark -D' output
& "C:\Program Files\Wireshark\tshark.exe" -i 1 -f "ether host 34:6f:24:c9:fa:01" -b filesize:102400 -b files:10 -w "C:\logs\mycapture.pcapng"

```

### 4. Export Sysmon Hunt Log (CSV)

Extracts Network (ID 3) and DNS (ID 22) events into a readable spreadsheet.

```powershell
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
$Results | Export-Csv -Path "C:\logs\sysmon_hunt.csv" -NoTypeInformation

```

---

## 🛠 Maintenance & Cleanup

### Sysmon
* **Do not terminate:** Sysmon runs as a persistent service. 
* **Log Rotation:** Windows automatically manages the size of the Event Log, so it won't fill your hard drive.
* **Update Config:** If you need to change your filters: `.\Sysmon64.exe -c newconfig.xml`

### Tshark Cleanup
* **Flush Buffers:** Always use `Ctrl+C` to stop Tshark so the PCAP file closes correctly.
* **Storage:** Periodically clear the `C:\logs` folder if you aren't using the ring buffer (`-b`) settings.

---

##
Process Hacker 2 or Process Explorer: Sysmon tells you what happened in the past, but these tools let you see what is happening right now. If you see an Event ID 8 (Injection), you can use Process Hacker to inspect the memory of that PowerShell process in real-time.

JA3 Fingerprinting (via Zeek): Since you are using Zeek, ensure you enable JA3. It allows you to identify malware based on the "fingerprint" of its TLS handshake, even if you haven't decrypted the traffic yet.
