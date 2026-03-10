```powershell
while($true) {
    $Timestamp = Get-Date -Format "HH:mm:ss"
    
    # Get only the ESTABLISHED connections
    $Connections = netstat -ano | Select-String "ESTABLISHED"
    
    foreach ($Line in $Connections) {
        # Split the line into parts and remove empty spaces
        $Parts = $Line.ToString().Split(' ', [System.StringSplitOptions]::RemoveEmptyEntries)
        
        # In netstat -ano, the PID is the 5th column (Index 4)
        $ProcessId = $Parts[4]
        
        try {
            # Find the name of the app using that ID
            $PName = (Get-Process -Id $ProcessId -ErrorAction Stop).Name
        } catch {
            $PName = "Unknown/Closed"
        }
        
        # Log it: Time | Local Address | Remote Address | PID | Name
        $LogEntry = "$Timestamp | $($Parts[1]) -> $($Parts[2]) | PID: $ProcessId | App: $PName"
        $LogEntry | Out-File -FilePath "C:\logs\netstat_history.txt" -Append
    }
    
    Start-Sleep -Seconds 5 
}
```