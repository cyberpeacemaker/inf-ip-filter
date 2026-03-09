# Create the log folder if it doesn't exist
New-Item -ItemType Directory -Path "C:\logs" -Force

# Record the configuration with a timestamp
$Timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
"--- IPCONFIG RECORDED AT $Timestamp ---" | Out-File -FilePath "C:\logs\host_config.txt" -Append
ipconfig /all | Out-File -FilePath "C:\logs\host_config.txt" -Append