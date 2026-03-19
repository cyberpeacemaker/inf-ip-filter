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

# MISC
142.250.204.35 

