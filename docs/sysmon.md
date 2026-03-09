#
Sysmon is the "gold standard" for this kind of work because it is a kernel-level driver. While your PowerShell script "asks" the OS for information every 5 seconds, Sysmon sits inside the operating system and **sees every single connection the millisecond it happens**.

If a C2 malware connects for only 0.5 seconds to send a heartbeat and then closes, your 5-second script might miss it. **Sysmon never misses it**.

---

### 1. Installation (The "Fast" Way)

To get started, you need the Sysmon executable (from Microsoft Sysinternals) and a configuration file. For threat hunting, the community favorite is **SwiftOnSecurity’s config**, which filters out the "noise" of normal Windows background tasks so you only see the interesting stuff.

**Commands (Run as Administrator):**

1. Download [Sysmon](https://www.google.com/search?q=https://download.sysinternals.com/files/Sysmon.zip) and extract it to `C:\Sysmon`.
2. Download the [config.xml](https://raw.githubusercontent.com/SwiftOnSecurity/sysmon-config/master/sysmonconfig-export.xml) to the same folder.
3. Install it:
```powershell
cd C:\Sysmon
.\Sysmon64.exe -i sysmonconfig-export.xml -accepteula

```



---

### 2. Why Event ID 3 is your best friend

Once installed, Sysmon logs everything to a special place in the **Event Viewer**:
`Applications and Services Logs > Microsoft > Windows > Sysmon > Operational`.

**Event ID 3 (Network Connection)** contains:

* **Image:** Exactly which `.exe` made the connection (e.g., `C:\Users\You\AppData\Local\Temp\invader.exe`).
* **ProcessGuid:** A unique ID that stays the same even if the PID changes.
* **Source/Destination IPs & Ports:** Perfect for matching with your `tshark` capture.

---

### 3. Coordinating Sysmon with Wireshark

This is where it gets powerful. If you find a suspicious IP in Wireshark, you don't have to guess. You can use PowerShell to query the Sysmon logs for that specific IP.

**Example: "Who talked to this IP at 2 PM?"**

```powershell
Get-WinEvent -LogName "Microsoft-Windows-Sysmon/Operational" | `
    Where-Object { $_.Id -eq 3 -and $_.Message -like "*9.9.9.9*" } | `
    Select-Object TimeCreated, Message | Format-List

```

*This will spit out the exact program name and user account that made that connection.*

---

### 4. Pro Tip: The "Process Creation" Link (Event ID 1)

If you find a C2 connection (ID 3), you can then look for **Event ID 1** for that same **ProcessGuid**. This will show you exactly *how* that malware started—for example, if it was launched by `Word.exe` (a macro) or `PowerShell.exe`.

### Summary Comparison

| Feature | PowerShell Script | Sysmon (Event ID 3) |
| --- | --- | --- |
| **Capture Type** | Polling (Snapshots) | Event-Driven (Real-time) |
| **Missing Data** | High (if connection is fast) | Zero |
| **System Impact** | Medium (CPU spikes) | Very Low (Kernel driver) |
| **Ease of Setup** | Instant | Requires Install |

**Would you like me to help you write a small script that exports all Sysmon ID 3 events to a CSV so you can easily compare them against your Wireshark traffic?**

#

To export your Sysmon network events to a CSV, you need a script that "translates" the complex XML data inside the event log into flat columns.

Standard Windows events store their most useful data (like the Program Name or Destination IP) in an internal list called `EventData`. If you just export the log normally, these fields will be squished into one messy column.

### 1. The Sysmon Export Script

This script specifically pulls out the **Process Name**, **Source IP**, **Destination IP**, and **Destination Port** from Sysmon Event ID 3.

```powershell
# 1. Get Sysmon Network Connection events
$Events = Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-Sysmon/Operational'; Id=3}

# 2. Extract the hidden data from the XML
$Results = foreach ($Event in $Events) {
    $xml = [xml]$Event.ToXml()
    $data = @{}
    foreach ($item in $xml.Event.EventData.Data) {
        $data[$item.Name] = $item.'#text'
    }

    # Create a clean object for the CSV
    [PSCustomObject]@{
        Time          = $Event.TimeCreated
        ProcessName   = $data.Image
        SourceIp      = $data.SourceIp
        SourcePort    = $data.SourcePort
        DestIp        = $data.DestinationIp
        DestPort      = $data.DestinationPort
        Protocol      = $data.Protocol
        User          = $data.User
    }
}

# 3. Save to CSV
$Results | Export-Csv -Path "C:\logs\sysmon_network.csv" -NoTypeInformation
Write-Host "Export complete: C:\logs\sysmon_network.csv" -ForegroundColor Cyan

```

---

### 2. How to Correlate with Wireshark

Now you have two CSVs (or one PCAP and one CSV). To find your C2 communication, follow this "Correlation Loop":

1. **In Wireshark:** Filter for a suspicious IP you found (e.g., `ip.addr == 1.2.3.4`). Note the **Timestamp** and the **Source Port**.
2. **In your Sysmon CSV:** Open it in Excel or use PowerShell to find that same port.
3. **The Result:** You will see the `ProcessName` (like `cmd.exe` or `updater.exe`).

**The "Magic" PowerShell Lookup:**
If you see a suspicious port (e.g., `54321`) in Wireshark, run this to identify the app:

```powershell
Import-Csv "C:\logs\sysmon_network.csv" | Where-Object { $_.SourcePort -eq "54321" } | Select-Object Time, ProcessName, DestIp

```

---

### 3. Why this is the "Ultimate" Combo

By combining **Tshark** (Raw packets), **SSL Keylogs** (Decrypted content), and **Sysmon** (Process attribution), you have created a professional-grade visibility stack:

* **Tshark** says: "Something happened on the wire."
* **SSL Keylog** says: "Here is exactly what they said (the HTTP command)."
* **Sysmon** says: "Here is the exact file on your hard drive that said it."

### Final Tip: The "Rare Process" Hunt

C2 malware often uses names that look like system files but are running from weird locations. In your Sysmon CSV, look for **`Image`** paths that are in `\AppData\Local\Temp\` or `\Public\`. Standard Windows services almost always run from `C:\Windows\System32\`.

Would you like me to show you how to use Sysmon **Event ID 22** to see every DNS query Chrome makes before it even starts the TLS connection?

#
The location where you installed the **Sysmon64.exe** binary (your `C:\Users\sinceremony\Documents\Sysmon` folder shown in the screenshot) does **not** affect where the logs are stored.

Sysmon is a service; once installed, it sends all its data to the **Windows Event Log** system, which is managed by the OS in a standardized location.

### 1. Where to find the Event File

You don't need to look for a physical file on your hard drive to view the logs. You access them through the **Event Viewer** interface:

1. Press `Win + R`, type **`eventvwr.msc`**, and hit Enter.
2. Navigate through this specific tree on the left:
* **Applications and Services Logs**
* **Microsoft**
* **Windows**
* **Sysmon**
* **Operational** (This is where the actual events live)



---

### 2. Is your Sysmon actually logging?

Looking at your screenshot `image_2fd020.png`, your commands to query the log for `9.9.9.9` and `1.1.1.1` returned **nothing** (no output). This usually happens for one of two reasons:

* **Timing:** Sysmon only logs connections that happened *after* it was started. If you ran those queries immediately after install, you might need to go browse the web for a minute to generate some traffic.
* **The Filter:** The `-like "*9.9.9.9*"` filter looks at the `Message` field. Sometimes, if the log is very new or the IP is stored differently in the XML, it might not catch it.

**Try this "Total Count" command to see if any events exist at all:**

```powershell
(Get-WinEvent -LogName "Microsoft-Windows-Sysmon/Operational").Count

```

*If this returns a number higher than 0, your Sysmon is working!*

---

### 3. Your CSV Export Script

Since you installed Sysmon in `Documents\Sysmon`, you are perfectly fine. The PowerShell script I gave you earlier will still work perfectly because it asks the **Windows OS** for the logs, not the folder where the `.exe` lives.

**Just make sure you run your PowerShell as Administrator.** If you aren't an Admin, `Get-WinEvent` will be denied access to the Sysmon logs for security reasons.

### 4. Why 1.1.1.1 and 9.9.9.9?

I see you are specifically hunting for those DNS IPs. In your Wireshark images (`image_3125da.png` and `image_311e91.png`), you have a lot of traffic to those addresses.

* **1.1.1.1** is Cloudflare DNS.
* **9.9.9.9** is Quad9 DNS.

If you find an Event ID 3 in your Sysmon log for these IPs, look at the `Image` field. If the image is `chrome.exe`, it's just your browser doing DNS-over-HTTPS. If the image is a **randomly named .exe in your Temp folder**, you've found your C2 beacon.

Would you like me to show you how to filter your Sysmon logs specifically for **"DNS Query" (Event ID 22)** so you can see exactly what domains your computer is looking up?

#
No reboot is required to see the "Operational" log! The reason you aren't seeing it is likely that the folder structure in **Event Viewer** is deeply nested, and your screenshot `image_2fcc7a.png` shows you are still at the top level.

Here is exactly how to find it and why your script returned an error.

### 1. Finding the "Missing" Operational Log

In your Event Viewer window, you need to "drill down" specifically to this path:

1. Click the arrow next to **Applications and Services Logs**.
2. Click the arrow next to **Microsoft**.
3. Click the arrow next to **Windows**.
4. Scroll way down to find **Sysmon**.
5. Click the arrow next to **Sysmon**, and you will see **Operational**.

**If the "Sysmon" folder itself is missing:** It means the installation didn't register the event provider correctly. Looking at `image_2fd020.png`, it says "Sysmon64 started," so it should be there. Try hitting **Action > Refresh** at the top of Event Viewer.

---

### 2. Why your PowerShell script failed

In `image_2fcc7a.png`, you see the red error: `No events were found that match the specified selection criteria`.

This is actually "normal" for a brand-new installation. Sysmon only records events that happen **after** it is installed.

* If you haven't browsed any websites or opened any apps since you ran the install command, there are no "Network Connection" (ID 3) events to find.
* The script crashed because it tried to process an empty list of events.

**To fix this and generate data:**

1. Open Chrome and visit a few sites (e.g., https://www.google.com/search?q=google.com, quad9.net).
2. Wait about 30 seconds.
3. Run the script again.

---

### 3. Verification Command

To see if Sysmon is actually awake and logging *anything* at all (not just network), run this simpler command. It looks for **Event ID 1** (Process Creation), which happens every time you open a terminal or app:

```powershell
Get-WinEvent -LogName "Microsoft-Windows-Sysmon/Operational" -MaxEvents 5

```

---

### 4. About your install location

Installing in `Documents\Sysmon` is perfectly fine. The only thing that would affect the logs is if the **Service** isn't running. You can verify the service status with:

```powershell
Get-Service Sysmon64

```

It should say **Running**.

**Once you generate some traffic and the `Operational` log appears, would you like me to show you how to filter for "Event ID 22" (DNS Queries)?** This will show you exactly what domains your computer is looking up, which is a key part of hunting for C2 "heartbeats."