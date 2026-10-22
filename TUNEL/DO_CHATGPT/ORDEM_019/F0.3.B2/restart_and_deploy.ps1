$ErrorActionPreference = 'Stop'
$base = 'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F0.3.B2'
$oldServerId = 137088
$oldServer = Get-CimInstance Win32_Process -Filter "ProcessId=$oldServerId"
if ($oldServer.CommandLine -notmatch 'C:\\IALD\\Bancada_Um\\um_bancada.py') { throw 'Unexpected server identity' }
$oldCpu = (Get-Process -Id $oldServerId).CPU
Start-Sleep -Seconds 5
$cpuDelta = (Get-Process -Id $oldServerId).CPU - $oldCpu
if ($cpuDelta -gt 0.25) { throw 'Server CPU activity: defer restart' }
$children = @(Get-CimInstance Win32_Process | Where-Object { $_.ParentProcessId -eq $oldServerId })
if ($children.Count -gt 0) { throw 'Server has active child processes: defer restart' }
$oldAdapters = @(Get-CimInstance Win32_Process | Where-Object { $_.Name -match '^python(w)?\.exe$' -and $_.CommandLine -match 'C:\\IALD\\Bancada_Um\\mcp_um.py' })
$before = [ordered]@{ started_utc=[DateTime]::UtcNow.ToString('o'); server=$oldServerId; cpu_delta_5_seconds=$cpuDelta; child_count=$children.Count; legacy_idle_scope='No workload observed; legacy server has no task introspection. Not proof of idle.'; adapters=@($oldAdapters | Select-Object ProcessId,ParentProcessId,CreationDate,CommandLine) }
$before | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath ($base+'\RESTART_BEFORE_R1.json') -Encoding utf8
Stop-Process -Id $oldServerId
Wait-Process -Id $oldServerId -Timeout 15 -ErrorAction SilentlyContinue
if (Get-Process -Id $oldServerId -ErrorAction SilentlyContinue) { throw 'Old server still alive' }
& 'C:\Python314\python.exe' -B -X utf8 ($base+'\deploy_candidate.py') --apply
if ($LASTEXITCODE -ne 0) { throw 'Deploy failed; inspect rollback receipt before restarting' }
$retired = @()
foreach ($adapter in $oldAdapters) {
    $current = Get-CimInstance Win32_Process -Filter ('ProcessId='+$adapter.ProcessId)
    if ($current -and $current.CreationDate -eq $adapter.CreationDate -and $current.CommandLine -eq $adapter.CommandLine) {
        Stop-Process -Id $adapter.ProcessId
        $retired += $adapter.ProcessId
    }
}
$new = Start-Process -FilePath 'C:\Python314\pythonw.exe' -ArgumentList @('-B','-X','utf8','-X','pycache_prefix=C:\IALD\Bancada_Um\estado\pycache_B2_R2','C:\IALD\Bancada_Um\um_bancada.py') -WindowStyle Hidden -PassThru -RedirectStandardOutput ($base+'\RUNTIME_STDOUT_R1.log') -RedirectStandardError ($base+'\RUNTIME_STDERR_R1.log')
[ordered]@{ended_utc=[DateTime]::UtcNow.ToString('o');old_server=$oldServerId;new_server=$new.Id;retired_mcp=$retired;client_action='Reconnect existing MCP clients; fresh stdio verified separately';runtime_verified=$false} | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath ($base+'\RESTART_RECEIPT_R1.json') -Encoding utf8
Write-Output ('New server PID '+$new.Id+'; retired MCP '+$retired.Count)
