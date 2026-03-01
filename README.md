# Data Usage
- dns-master: all dns cache
- white-master: all white-list ip
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
