# diagnostic_systeme.ps1

$cpuLoad = Get-CimInstance Win32_Processor | Measure-Object -Property LoadPercentage -Average | Select -ExpandProperty Average
$mem = Get-CimInstance Win32_OperatingSystem | Select-Object TotalVisibleMemorySize, FreePhysicalMemory
$memTotal = [math]::Round($mem.TotalVisibleMemorySize / 1MB, 2)
$memFree = [math]::Round($mem.FreePhysicalMemory / 1MB, 2)
$memUsedPct = [math]::Round((($mem.TotalVisibleMemorySize - $mem.FreePhysicalMemory) / $mem.TotalVisibleMemorySize) * 100, 2)

$criticalProcs = @("node", "python", "watchdog", "chrome")
$procStatus = @{}

foreach ($name in $criticalProcs) {
    if (Get-Process -Name $name -ErrorAction SilentlyContinue) {
        $procStatus[$name] = "Running"
    } else {
        $procStatus[$name] = "Stopped"
    }
}

$report = @{
    timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    cpu_load_pct = $cpuLoad
    ram_total_gb = $memTotal
    ram_free_gb = $memFree
    ram_used_pct = $memUsedPct
    services = $procStatus
}

$report | ConvertTo-Json
