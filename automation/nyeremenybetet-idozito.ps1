# Checks if container runs
$dockerStatus = Get-Service -Name "com.docker.service" -ErrorAction SilentlyContinue

if ($dockerStatus -eq $null -or $dockerStatus.Status -ne "Running") {
    Write-Host "The docker container is not running. Starting it..."
    Start-Service com.docker.service
    Start-Sleep -Seconds 10 # Várunk egy kicsit az elindulásra
}

# Docker command
cd C:\docker\Gepkocsi-nyeremenybetet\v2.0
$dockerCommand = 'docker run --rm -v "C:\docker\Gepkocsi-nyeremenybetet\v2.0:/app" -v "C:\docker\Gepkocsi-nyeremenybetet\v2.0\series_numbers.txt:/app/series_numbers.txt" selenium-python'

# Scheduled task name
$taskName = "Car Lottery Deposit"

# Creating scheduled task
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -WindowStyle Hidden -Command $dockerCommand"

# Repeat task at
$trigger = New-ScheduledTaskTrigger -At 08:00AM -Daily -DaysInterval 30

# Additional parameters
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

# Create it
$task = New-ScheduledTask -Action $action -Trigger $trigger -Principal $principal -Settings $settings


# If it already exists, we delete it
if (Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue) {
    Write-Host "This task already exists, deleting it..."
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

# Registry of task
Register-ScheduledTask -TaskName $taskName -InputObject $task

Write-Host "Timer set!"
