# 1. Define your file path
#$filePath = "$PSScriptRoot\..\block-ip-list-raw.txt"
$filePath = "C:\Users\sinceremony\Documents\analysis\ip\block-ip-list-raw.txt"

# 2. Get active TCP connections (Foreign Addresses only)
# We filter for 'Established' to avoid junk, then split the IP from the Port
$activeIps = Get-NetTCPConnection -State Established | 
             Select-Object -ExpandProperty RemoteAddress

# 3. Define IPs to exclude
$excludeList = @("1.1.1.1", "9.9.9.9", "0.0.0.0", "127.0.0.1")

# 4. Filter, get unique values, and append to file
$activeIps | Where-Object { $_ -notin $excludeList } | 
             Select-Object -Unique | 
             Out-File -FilePath $filePath -Append -Encoding ascii
             
