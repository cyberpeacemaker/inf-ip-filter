# Data Usage
- dns-master: all dns cache
- white-master: all white-list ip
- white-exclude: exclude ip
- white-mannual: mannual ip

# Script Process
- dns catch (get-dns) + (ipconfig) > dns-master + dns-latest
- dns-master + white-mannual - white-exclude > white-master
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
