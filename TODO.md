# top
- todo extension
- dns rotation for chrome

# analysis
- repo-analysis
  - ip/README
  - malicious ip
  - duplicated ip
  - white-exclude + black-mannual
- 02-13 dns cache

# Ask AI
- ai: browser hijacking > mitb
- Windows telemetry
- malwarebytes

# script
- check dns-cache before adding to whitelist
- extract distinguished domain name in dns-cache
- sort data (ip-white-exclude, ip-white-mannual)


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
`script/_inf_create_ip_white_list.py`
檢查白名單

比對黑名單跟dns catch
- 存在 Mapping
- 不存在

# black list
`script/_inf_create_ip_black_list.py``
蒐集黑名單

# simplewall spy
比對

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
- simplewall cml?
- debug : "PS C:\Users\sinceremony\Documents\GitHub\inf-create-ip-list\script> python .\_inf_create_ip_white_list.py
Traceback (most recent call last):
  File "C:\Users\sinceremony\Documents\GitHub\inf-create-ip-list\script\_inf_create_ip_white_list.py", line 201, in <module>
    dns_master = update_dns_master()
  File "C:\Users\sinceremony\Documents\GitHub\inf-create-ip-list\script\_inf_create_ip_white_list.py", line 95, in update_dns_master
    key = (record.Entry.lower(), record.Data.lower())
                                 ^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'lower'"
- monitor **any** tcp attempt
- folder path optimize?
- dns catch constrcuted to assist with white-list
- optimze dns catch
- Dir existed check
- change `MIN_IPS_FOR_CIDR` larger to observe more unique ips.