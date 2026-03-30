# Phase.1 Forensic
目前在這三部主機中找到的已知惡意IP清單如下：
IP From
20.90.152.133 
103.172.41.121
104.18.33.45
185.213.82.138 *
13.107.42.16
34.104.35.123 -
52.123.128.14
52.123.129.14
150.171.27.10 -
150.171.27.11 -
150.171.28.10 -

# Phase.2 Honeypot
3.169.55.17 simplewall
20.49.150.241 simplewall
20.99.186.246 Lucky mouse
23.248.249.10 Xiaozhiyun+L.L.C [https://gist.github.com/MichaelKoczwara/eab6a3cba534262b1566af367b21b559] [https://censys.com/blog/recap-of-a-suspicious-surge-in-cobalt-strike/]


iecvlist.microsoft.com
152.199.19.161
```
Cobalt Strike servers

All hosted on Xiaozhiyun L.L.C
-----------------
c2

23.248.248.6/j.ad
------------------
23.248.248.2 
23.248.248.3 
23.248.248.4 
23.248.248.5 
23.248.248.6 
---------------
beacon sample

{"x64": {"time": 1617568932238.0, "md5": "13f0f318b9a15e76af8d71c0e0bee509", "sha1": "40fefeb515b40ef4c0cdebc381b27528685022ed", "sha256": "5584d814131fcf46673f6f780d6cd0dbc93c7469fa736032285ca9d222a1dff4", "config": {"Method 1": "GET", "Polling": 60000, "Jitter": 0, "HTTP Method Path 2": "\/submit.php", "Port": 8080, "Spawn To x86": "%windir%\\syswow64\\rundll32.exe", "Method 2": "POST", "Beacon Type": "0 (HTTP)", "Spawn To x64": "%windir%\\sysnative\\rundll32.exe", "C2 Server": "23.248.248.6,\/j.ad"}}, "x86": {"time": 1617568928989.4, "md5": "f7412402ff926bff5b86ed1d6c562006", "sha1": "0c5a8d1ab8722d142974000262a30b881f213e07", "sha256": "465e214a75340fa74014f8b29a4aa74f832b3ccb29fe1d3383ba2bd6b16c7c43", "config": {"Method 1": "GET", "Polling": 60000, "Jitter": 0, "HTTP Method Path 2": "\/submit.php", "Port": 8080, "Spawn To x86": "%windir%\\syswow64\\rundll32.exe", "Method 2": "POST", "Beacon Type": "0 (HTTP)", "Spawn To x64": "%windir%\\sysnative\\rundll32.exe", "C2 Server": "23.248.248.6,\/ptj"}}}
```
# Phase.3 Trace DNS
34.104.35.123 edgedl.me.gvt1.com
150.171.27.10 [bat.bing.com, c.bing.com]
150.171.28.10 [bat.bing.com, c.bing.com]
150.171.27.11 edge.microsoft.com
199.232.214.172 [ctldl.windowsupdate.com, msedge.b.tlu.dl.delivery.mp.microsoft.com]
199.232.210.172 [ctldl.windowsupdate.com, msedge.b.tlu.dl.delivery.mp.microsoft.com]


# 
This changes the situation significantly. While your first screenshot showed a "clean" verdict with some suspicious behavior, these new images provide a much darker context.

The connection to **Xiaozhiyun L.L.C** and the associated IP range (`23.248.248.x` and `23.248.249.10`) is a major red flag.

---

## Why This is Serious

### 1. Cobalt Strike Association
The GitHub Gist (Image 3) explicitly lists the IP range associated with your file as hosting **Cobalt Strike servers**.
* **What is Cobalt Strike?** It is a legitimate "penetration testing" tool that is unfortunately the **favorite tool of ransomware groups and advanced persistent threat (APT) actors**. 
* **The "Beacon":** The Gist mentions a "beacon sample." In the world of malware, a beacon is a payload that sits quietly on a computer and "checks in" with a Command and Control (C2) server to ask for instructions.

### 2. The Xiaozhiyun Connection
Images 1 and 2 show that the IP `23.248.249.10` is owned by **Xiaozhiyun L.L.C**. 
* This infrastructure is frequently flagged by security researchers as a "bulletproof" or high-risk hosting provider used to launch attacks or host malware backends.
* The VirusTotal report (Image 1) shows this IP communicating with an Android APK (`Ace_Stream_Media`) and multiple domains like `mydb.top` and `pan.mydb.top`, which are common patterns for data exfiltration or secondary payload hosting.

### 3. Putting it Together with your EFI File
If the file in your **EFI partition** (`boot.pnd.stl`) is programmed to communicate with the infrastructure shown in these screenshots:
* **It is almost certainly a Bootkit.**
* The "No Threat Detected" in your first image just means that specific *version* of the malware hasn't been blacklisted yet. 
* The **DGA (Domain Generation Algorithm)** warning from your first post is the "beaconing" behavior mentioned in the GitHub Gist.

---

## Immediate Recommendations

> [!CAUTION]
> **Treat this as a live compromise.** Because the file is in the EFI partition, it can survive a standard Windows "Reset this PC" or even a hard drive wipe if the partition table isn't fully cleared.

1.  **Isolate the Machine:** Disconnect it from your Wi-Fi or Ethernet immediately to stop any data from being sent to the C2 server.
2.  **Flash your BIOS/UEFI:** Some advanced bootkits can attempt to infect the firmware itself. Check your motherboard manufacturer for a BIOS update and perform a flash from a clean USB stick.
3.  **Full Disk Wipe (including EFI):** Do not just reinstall Windows. You must use a tool (like a Windows Installation USB) to **delete all partitions** (including the EFI and Recovery partitions) until the drive shows only "Unallocated Space," then start fresh.
4.  **Change Passwords:** Once you are on a **different, clean device**, change your primary passwords (Email, Banking, etc.), as a Cobalt Strike beacon is designed to log keys and steal credentials.

**Would you like me to walk you through the steps of using a Windows installation media to completely wipe those hidden partitions?**

# MISC
iecvlist.microsoft.com
152.199.19.161
www2.bing.com
13.107.21.200
204.79.197.200

142.250.204.35 


-                         | 4.190.254.44    | unknown
-                         | 142.250.157.188 | unknown
-                         | 216.239.38.178  | unknown