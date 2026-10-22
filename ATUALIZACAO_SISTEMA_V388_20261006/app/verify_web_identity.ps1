param([Parameter(Mandatory=$true)][int]$WebPid)
$ErrorActionPreference='Stop'
$taskRoot='C:\IALD\projetos_pyhton\IALD'
$taskManifest=Get-Content -LiteralPath (Join-Path $taskRoot 'iald_nucleo_fixo.json') -Raw | ConvertFrom-Json
$taskExpected=$taskManifest.active_cluster.release_source_sha256
if ($taskManifest.active_cluster.release -ne 'v388' -or $taskExpected -notmatch '^[a-f0-9]{64}$') { throw 'Wrong installed identity' }
$taskSource=(Get-FileHash -LiteralPath $taskManifest.published_evidence.program.path -Algorithm SHA256).Hash.ToLowerInvariant()
if ($taskSource -ne $taskExpected) { throw 'Program differs from installed identity' }
$taskLines=@(Get-Content -LiteralPath (Join-Path $taskRoot 'logs\web-supervisor.log') -Tail 100)
$taskIndex=-1
for ($taskI=$taskLines.Count-1;$taskI -ge 0;$taskI--) { if ($taskLines[$taskI] -match "PID $WebPid iniciado\.") {$taskIndex=$taskI;break} }
if ($taskIndex -lt 1) { throw 'New PID has no supervisor log identity' }
$taskLine=$taskLines[$taskIndex-1]
if ($taskLine -notmatch ' -> (.+web-server_[0-9_]+_r[0-9]+\.log)$') { throw 'No log bound to PID' }
$taskLog=[IO.Path]::GetFullPath($Matches[1])
if ([IO.Path]::GetDirectoryName($taskLog) -ne (Join-Path $taskRoot 'logs')) { throw 'Log escaped expected root' }
$taskStartup=@(Get-Content -LiteralPath $taskLog -TotalCount 40 | Where-Object {$_ -match '^\[IALD-CANONICAL-CATALOG\]'})
if ($taskStartup.Count -ne 1 -or $taskStartup[0] -notmatch ('^\[IALD-CANONICAL-CATALOG\] release=v388 source_sha256='+$taskExpected.Substring(0,16)+' lean_files=1211$')) { throw 'Web catalog identity differs' }
[pscustomobject]@{status='PASS';web_pid=$WebPid;log_path=$taskLog;catalog_startup_line=$taskStartup[0];installed_source_sha256=$taskSource;runtime_sha_characters=16;scope='Existing loader log bound to actual supervisor child; no model inference'} | ConvertTo-Json -Compress
