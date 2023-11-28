<#
.SYNOPSIS
This module provides functions to reset Docker WSL integration.

.DESCRIPTION
The module includes functions to stop Docker Desktop, shut down WSL, and unregister Docker WSL data.

.NOTES
Version:        1.0
Author:         Daethyra
#>

function Stop-DockerDesktop {
    <#
    .SYNOPSIS
    Stops the Docker Desktop process.

    .DESCRIPTION
    Attempts to stop the Docker Desktop process. Writes an error if the process cannot be stopped.
    #>

    try {
        Get-Process -Name "Docker Desktop*" | Stop-Process -ErrorAction Stop
        Write-Verbose "Docker Desktop process stopped successfully."
    }
    catch {
        Write-Error "Error stopping Docker Desktop process: $_"
    }
}

function Shutdown-Wsl {
    <#
    .SYNOPSIS
    Shuts down the Windows Subsystem for Linux (WSL).

    .DESCRIPTION
    Tries to shut down WSL up to a maximum number of retries.
    #>

    param (
        [int]$maxRetries = 3
    )

    for ($i = 0; $i -lt $maxRetries; $i++) {
        wsl --shutdown
        if ($?) {
            Write-Verbose "WSL shut down successfully on attempt $($i + 1)."
            return
        }
        else {
            Write-Warning "WSL shutdown attempt $($i + 1) failed. Retrying..."
            Start-Sleep -Seconds 2
        }
    }

    Write-Error "Failed to shut down WSL after $maxRetries attempts."
}

function Unregister-DockerWsl {
    <#
    .SYNOPSIS
    Unregisters the docker-desktop-data from WSL.

    .DESCRIPTION
    Attempts to unregister the docker-desktop-data. Writes an error if the operation fails.
    #>

    try {
        wsl --unregister docker-desktop-data -ErrorAction Stop
        Write-Verbose "Unregistered docker-desktop-data successfully."
    }
    catch {
        Write-Error "Error unregistering docker-desktop-data: $_"
    }
}

# Main script
try {
    Write-Verbose "Starting Docker WSL integration reset process."

    Write-Verbose "Stopping Docker Desktop"
    Stop-DockerDesktop

    Write-Verbose "Shutting down WSL"
    Shutdown-Wsl

    Write-Verbose "Unregistering docker-desktop-data"
    Unregister-DockerWsl

    Write-Host "Docker WSL integration successfully reset"
}
catch {
    Write-Error "Reset failed: $_"
}
