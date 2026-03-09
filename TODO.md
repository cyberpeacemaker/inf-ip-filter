# top
- no to all
- switch csv colum [reason,ip]
- overrite > exam key value, if different, why?
- ip-black-mannual
- blacklist-merged
`script/_inf_create_ip_black_list.py``
蒐集黑名單

# script
- sort data (ip-white-exclude, ip-white-mannual)
- ip-black-mannual reason modify
- dns-cache-ipconfig parser (psutil cmd command)

# analysis
- extract distinguished domain name in dns-cache
- repo-analysis
  - ip/README
  - malicious ip
  - duplicated ip
  - white-exclude + black-mannual
- 02-13 dns cache
- Real Intelligence Threat Analytics, zeek, snort, yara
- simplewall spy 比對
- check
  - dns-master
  - ip-white-master (which are allowed)

# Ask AI
- ai: browser hijacking > mitb
- Windows telemetry, tracking/telemetry
- malwarebytes




- dns-latest
- exclude or exclusion
- exclude domain
- print colorful / optimize output 
- avoid accententally misconfused the `_inf_create_ip_white_list.py` and `_inf_create_ip_black_list.py` (output profile?)
- white_list_mannual or **Windows NCSI (Network Connectivity Status Indicator)** (ipconfig /displaydns)
- print connection with white list (domain, reason)
- user confirmation before block ip
- observe how white list dns resolve work (packet analysis)
- "199.232.214.172"? # TODO : keep WHITE_MASTER remmain (now will be subtracted by exclusion)
- launchdarkly
- 比對黑名單跟dns catch (in data/rotation-2026-02-13)
  - 存在 Mapping
  - 不存在
- 02/09
- IP:443 ?
- ('wpad', None) > some dns catch IP value is `None`


# white list

比對黑名單跟dns catch
- 存在 Mapping
- 不存在

# black list

#  worth futher investigation
104.26.12.38
142.250.204.35
Xiaozhiyun+L.L.C
172.67.70.74
23.248.249.10

20.99.186.246 Lucky Mouse APT27

#
23.100.109.78

# valid domain but suspecious?
142.250.196.195
>>> Added to Blacklist: 142.250.66.91
>>> Added to Blacklist: 142.250.66.67
203.69.138

- reason have to connect twice?
# domain
- go.trouter.skype.com
- chrome.cloudflare-dns.com,1,162.159.61.3,140
- edge.microsoft.com,1,150.171.27.11,29
- www.bing.com,210.71.227.218
- th.bing.com,,210.71.227.209,17
- config.edge.skype.com
- www.googletagmanager.com
- default.exp-tas.com
- g.live.com,13.107.213.73

#
- monitor **any** tcp attempt