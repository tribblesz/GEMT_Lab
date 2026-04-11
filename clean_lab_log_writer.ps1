$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path $PSScriptRoot).Path
$writerPort = 8765
$serverRelativeBack = "tools\lab-log-writer\server.py"
$serverRelativeForward = "tools/lab-log-writer/server.py"
$serverPathBack = Join-Path $repoRoot $serverRelativeBack
$serverPathForward = $serverPathBack -replace "\\", "/"

$listeningPids = @(
    Get-NetTCPConnection -LocalPort $writerPort -State Listen -ErrorAction SilentlyContinue |
        Select-Object -ExpandProperty OwningProcess -Unique
)

$pythonPortOwners = @()
if ($listeningPids.Count -gt 0) {
    $pythonPortOwners = @(
        Get-CimInstance Win32_Process | Where-Object {
            $_.ProcessId -in $listeningPids -and $_.Name -match '^pythonw?\.exe$'
        }
    )
}

$pythonMatches = @(
    Get-CimInstance Win32_Process | Where-Object {
        $_.Name -match '^pythonw?\.exe$' -and
        $_.CommandLine -and
        (
            $_.CommandLine -like ('*' + $serverPathBack + '*') -or
            $_.CommandLine -like ('*' + $serverPathForward + '*') -or
            $_.CommandLine -like ('*' + $serverRelativeBack + '*') -or
            $_.CommandLine -like ('*' + $serverRelativeForward + '*') -or
            $_.CommandLine -match '(^|\s|["''])server\.py($|\s|["''])'
        )
    }
)

$targets = @($pythonPortOwners + $pythonMatches | Sort-Object ProcessId -Unique)

if ($targets.Count -eq 0) {
    Write-Host "No running lab-log-writer server instances found."
    exit 0
}

foreach ($target in $targets) {
    Write-Host ("Stopping PID " + $target.ProcessId + ": " + $target.CommandLine)
    Stop-Process -Id $target.ProcessId -Force -ErrorAction Stop
}

Write-Host ("Stopped " + $targets.Count + " lab-log-writer server instance(s).")
