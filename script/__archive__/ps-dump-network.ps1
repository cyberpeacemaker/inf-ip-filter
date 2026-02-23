function Get-UniqueFilePath {
    param (
        [Parameter(Mandatory)]
        [string]$Path
    )

    if (-not (Test-Path $Path)) {
        return $Path
    }

    $directory = Split-Path $Path
    $baseName  = [System.IO.Path]::GetFileNameWithoutExtension($Path)
    $extension = [System.IO.Path]::GetExtension($Path)

    $i = 1
    do {
        $newPath = Join-Path $directory "$baseName`_$i$extension"
        $i++
    } while (Test-Path $newPath)

    return $newPath
}


# DNS cache export
$dnsPath = Get-UniqueFilePath "$env:USERPROFILE\dns_cache.csv"

Get-DnsClientCache |
    Select-Object Entry, RecordType, Data, TimeToLive |
    Export-Csv -Path $dnsPath -NoTypeInformation


# TCP connections export
$tcpPath = Get-UniqueFilePath "$env:USERPROFILE\tcp_connections.csv"

Get-NetTCPConnection |
    Where-Object {
        $_.RemoteAddress -and
        $_.RemoteAddress -ne "0.0.0.0" -and
        $_.RemoteAddress -ne "::"
    } |
    Select-Object `
        @{Name="Process";Expression={(Get-Process -Id $_.OwningProcess -ErrorAction SilentlyContinue).ProcessName}},
        RemoteAddress
# Export-Csv -Path $tcpPath -NoTypeInformation
perfect. now i want to dump tcp to a log  and show tcp connection on screen as wll. like this "$tcpPath = Get-UniqueFilePath "$env:USERPROFILE\tcp_connections.csv"



Get-NetTCPConnection |

    Where-Object {

        $_.RemoteAddress -and

        $_.RemoteAddress -ne "0.0.0.0" -and

        $_.RemoteAddress -ne "::"

    } |

    Select-Object `

        @{Name="Process";Expression={(Get-Process -Id $_.OwningProcess -ErrorAction SilentlyContinue).ProcessName}},

        RemoteAddress"