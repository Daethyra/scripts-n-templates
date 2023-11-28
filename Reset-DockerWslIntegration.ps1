Here is the complete script to purge Docker data by resetting the WSL integration:

```powershell
# Functions to reset Docker WSL integration

function Stop-DockerDesktop {

  Get-Process -Name DockerDesktop | Stop-Process

  if(!$?) {
    Write-Error "Error stopping Docker Desktop process"
  }

}

function Shutdown-Wsl {
  
  $maxRetries = 3

  for ($i = 0; $i -lt $maxRetries; $i++) {
    wsl --shutdown
    
    if($?) {
      Write-Host "WSL shut down successfully" 
      break
    }
    else {
      Write-Warning "Retrying WSL shutdown"
      Start-Sleep -Seconds 2 
    }

  }

}

function Unregister-DockerWsl {

  wsl --unregister docker-desktop-data

  if(!$?) {
    Write-Error "Error unregistering docker-desktop-data" 
  }
  else {
    Write-Host "Unregistered docker-desktop-data successfully"
  }

}


# Main script

try {

  Write-Host "Stopping Docker Desktop"
  Stop-DockerDesktop

  Write-Host "Shutting down WSL" 
  Shutdown-Wsl

  Write-Host "Unregistering docker-desktop-data"
  Unregister-DockerWsl

  Write-Host "Docker WSL integration successfully reset"

}
catch {
  Write-Error "Reset failed: $_"
}
```

Let me know if you would like any changes or have any other suggestions!
