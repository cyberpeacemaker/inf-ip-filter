$Events = Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-Sysmon/Operational'; Id=3}
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
$Results | Export-Csv -Path "$env:USERPROFILE\Desktop\sysmon_hunt.csv" -NoTypeInformation