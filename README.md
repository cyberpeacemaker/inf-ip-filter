# **Project Name:** **Automated DNS-Correlation Dynamic Allowlist Defense System**

### **Background & Challenges**

* **The Power of Allowlists:** According to the *Windows 11 Security Book (2025)* and industry benchmarks, bidirectional allowlisting (Inbound/Outbound) is the gold standard for neutralizing Command & Control (C2) communication and preventing data exfiltration.
* **The Flexibility Gap:** Static IP filtering is too rigid for modern cloud environments. Meanwhile, standard **Dynamic Keywords** or FQDN allowlists often permit entire wildcard domains (e.g., `*.example.com`), leaving the network vulnerable to **Subdomain Takeover** or the exploitation of abandoned domains.

### **Core Solution**

This project develops an automated engine that monitors and validates **DNS Query** traffic in real-time to bridge the gap between security and usability:

* **Automated Dynamic Provisioning:** Analyzes DNS requests on the fly to update firewall rules dynamically, ensuring strict security without manual administrative overhead.
* **Behavioral Attribution (DNS-to-IP Mapping):** By logging the correlation between the "Target IP" and the "Initial DNS Request," the system eliminates the blind spots of **Reverse DNS Lookups**, which frequently fail or provide ambiguous results.
* **Integrity Verification:** By cross-referencing DNS resolution results with actual connection attempts, the system effectively detects and blocks **DNS Cache Poisoning** and malicious redirection attacks.

# Data Usage
- **dns-master**: all dns cache ([key,value] pair, including **A** and **CNAME** record)
- **white-master**: all white-list ip (    
    Build ip-white-master.csv from:
      dns-master (A records only)
      + ip-white-manual   (manual IP overrides; white manual wins over DNS, but loses to black)
      - ip-black-domain   (domain blacklist; black wins)
      - ip-black-manual   (IP blacklist; black wins)
      )
- white-manual: manual ip
- black-manual: black ip

# Script Process
- dns catch (get-dns) + (ipconfig) > dns-master + dns-latest
- dns-master + white-manual - black-manual > white-master
- white > profile

# Monitor Connection
- connection > white-master

# Simplewall Configure
- profile-baseline-02-13
    - Services: apps without internet access (269/269)
    - UWP apps: apps without internet access (106/106)
    - Blocklist
        - Enabled (166/1496)
        - Disabled (1330/1496)
    - System rule
        - Enabled: DHCP
    - User rule
        - doh:svchost.exe
        - tcp443:git, line
        - white:edge
        - http:winget

# Concept

## 專案名稱：基於 DNS 關聯分析之自動化動態白名單防禦系統

**Project: Automated Dynamic Allowlist & DNS Correlation Defense System**

### ### 專案背景與挑戰

* **白名單重要性：** 參考 *Windows 11 Security Book (2025)* 與各大指標資安報告，雙向白名單（Outbound/Inbound）是防禦 C2 溝通與資安外洩的核心。
* **現有機制缺陷：** 傳統靜態 IP 靈活性不足，而 Windows Firewall **Dynamic Keywords** 或 FQDN 白名單若放行所有子網域（Subdomains），則面臨子網域劫持（Subdomain Takeover）或棄用網域被濫用的風險。

### ### 核心解決方案

本專案試圖開發一套自動化系統，透過監控並批審 **DNS Query** 流量：

* **自動化動態批審：** 即時分析 DNS 請求，動態更新防火牆規則，兼顧安全性與管理便利性。
* **通訊行為溯源：** 透過日誌留存技術，精確紀錄「連線 IP」與「初始 DNS 請求」的關聯，解決 **Reverse DNS Lookup** 常因解析失敗而無法回溯行為原因的問題。
* **安全性強化：** 藉由對比 DNS 解析結果與實際通訊目標，有效偵測並防止 **DNS Poisoning（DNS 汙染）** 與惡意導向攻擊。

# Demo

## Part.1 Data
- dns-master.csv
    - EX1: reported C2: 34.104.35.123 > edgedl.me.gvt1.com
    - EX2: virustotal 185.199.111.153 > ydnaandy123.github.io
- [ip-white-manual.csv, ip-black-manual.csv, ip-black-domain.csv]
    - `python .\sort-manual-file.py --col 2` sort for visual
- ip-white-master
    - [dns-master.csv + ip-white-manual.csv] - [ip-black-manual.csv + ip-black-domain.csv + ignored]
- profile.xml for simplewall [Simple tool to configure Windows Filtering Platform (WFP) which can configure network activity on your computer.]
- pcap + sslkey, sysmonhunt

## Part.2 Networking
- create ip filter
- show connected ip

## Part.3 Packet Capture
- sslkey
- ipconfig
- wireshakr > zeek > rita
- sysmon

## 解說
### Part.1
- 0:45 dns-master介紹，儲存從本機端點撈出的dns cache資料，兩個好處，1.ip容易浮動的，單純紀錄ip連線，日後容易出現不確定當時是哪台裝置 2. ip是基於什麼名稱解析連線的，是直接連向惡意C2、compromised botnet，還是遭到毒化
- 0:56 **EX1**，我連到被標為惡意C2的IP，是什麼名稱解析過去的，從記錄看，也許不需要？
- 1:09 **EX2**，我連到被標為惡意C2的IP，是什麼名稱解析過去的，從記錄看，也許可以？
- 1:17 顯示3個手動maintain資料，手動白名單放了3個dns-server，手動黑名單放了幾個可能惡意C2、botnet，或是不需要的IP、Domain
- 1:51 可以根據欄位排序(單純為了方便檢視)
- 2:20 切回IP排序
- 2:42 此外，還有做sysmon紀錄，可以查，這個dns request，是誰、在什麼時候發出的 (還在整合施工中)
- 3:18 過往紀錄，可以使用flush衝到rotation中
- 3:49 flush後，dns-master/white-master清空，手動maintain的名單保留
### Part.2
- 4:00~4:29 還沒連線使用，dns-cache什麼都沒撈到，過濾清單只根據其他手動maintain的清單產生
- 5:14 只有dns-server被允許通過，其他都被擋下
- 5:36 使用，dns cache開始有資料，全部記錄下來，再來管理員可以批審是否允許
- 6:25 **EX1** 使用chrome連網chatgpt.com，dns cache資料全部紀錄，批審，可以覺得安全的允許，不安全的封鎖，不知道的跳過
- 7:12 **EX2** 使用chrome連網virustotal.com，dns cache資料全部紀錄，批審，可以覺得安全的允許，不安全的封鎖，不知道的跳過
- 8:18 **EX3** 檢視當前的連線，是什麼原因連過去的
- 8:40 剛剛批審中，選擇block的，會被加進black-domain清單中