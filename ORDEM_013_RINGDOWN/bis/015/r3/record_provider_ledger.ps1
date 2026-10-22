$ErrorActionPreference = 'Stop'
$bridge = 'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\bridge.py'
$python = 'C:\Python314\python.exe'
$ledger = 'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\LEDGER_016.jsonl'
$ids = @(
    '3cb7a84f-f6b3-4c19-a0e6-1e29d09b16fb',
    '241c61ad-3e31-452b-8950-e01db4fec4c7',
    '718e8849-b77f-4bb7-9bfa-4320eae1231b',
    '1e1bcffd-2488-470c-851d-8a730a6fa51d'
)
$utf8 = [System.Text.UTF8Encoding]::new($false)
$OutputEncoding = $utf8

function HashText([string]$value) {
    if ($null -eq $value) { return $null }
    $bytes = $utf8.GetBytes($value)
    return [Convert]::ToHexString([System.Security.Cryptography.SHA256]::HashData($bytes)).ToLowerInvariant()
}

$old = [System.IO.File]::ReadAllBytes($ledger)
$existing = @{}
foreach ($line in ($utf8.GetString($old) -split "`n")) {
    if ([string]::IsNullOrWhiteSpace($line)) { continue }
    $entry = $line | ConvertFrom-Json
    if ($entry.job_id -and $entry.status) {
        $existing["$($entry.job_id)/$($entry.status)"] = $true
    }
}
$new = [System.Collections.Generic.List[string]]::new()
foreach ($id in $ids) {
    $request = @{ operation = 'get'; job_id = $id } | ConvertTo-Json -Compress
    $job = $request | & $python -X utf8 $bridge | ConvertFrom-Json
    if ($LASTEXITCODE -ne 0 -or $job.id -ne $id) { throw "Bridge get failed for $id" }
    $status = if ($job.stage -eq 'completed') { 'completed' } elseif ($job.stage -eq 'execution_waiting') { 'execution_waiting' } else { $job.stage }
    if ($existing.ContainsKey("$id/$status")) { continue }
    $result = if ($job.execution) { $job.execution.result } else { $null }
    $entry = [ordered]@{
        at = [DateTime]::UtcNow.ToString('o')
        event = 'ORDEM016_PROVIDER_CALL_AUDIT'
        branch = $job.execution_constraints.branch_id
        lemma = $job.execution_constraints.lemma_id
        role = $job.execution_constraints.role
        provider = $job.execution_constraints.required_provider
        request_id = $job.request_id
        job_id = $id
        execution_id = $job.execution_task_id
        status = $status
        prompt_sha256 = HashText $job.prompt
        response_sha256 = if ($result -and $result.text) { HashText $result.text } else { $null }
        usage = if ($result) { $result.usage } else { $null }
        cost_estimate_usd = if ($result) { $result.cost_estimate_usd } else { $null }
        cost_status = if ($result) { $result.cost_status } else { $null }
        scientific_status = 'DECLARADO_NOT_PROOF'
    }
    $new.Add(($entry | ConvertTo-Json -Compress -Depth 8))
}
if ($new.Count -eq 0) { Write-Output 'NO_NEW_LEDGER_ENTRIES'; exit 0 }
$backup = $ledger + '.bak_' + [DateTime]::Now.ToString('yyyyMMdd_HHmmss')
[System.IO.File]::WriteAllBytes($backup, $old)
if (-not ([System.Linq.Enumerable]::SequenceEqual($old, [System.IO.File]::ReadAllBytes($backup)))) { throw 'Backup mismatch' }
$prefix = if ($old.Length -gt 0 -and $old[$old.Length - 1] -ne 10) { "`n" } else { '' }
$addition = $utf8.GetBytes($prefix + ($new -join "`n") + "`n")
$combined = [byte[]]::new($old.Length + $addition.Length)
[Array]::Copy($old, 0, $combined, 0, $old.Length)
[Array]::Copy($addition, 0, $combined, $old.Length, $addition.Length)
$temporary = $ledger + '.tmp'
[System.IO.File]::WriteAllBytes($temporary, $combined)
if ((Get-Item -LiteralPath $temporary).Length -ne $combined.Length) { throw 'Temporary ledger size mismatch' }
Move-Item -LiteralPath $temporary -Destination $ledger -Force
Write-Output ("APPENDED={0} LEDGER_SHA256={1}" -f $new.Count, (Get-FileHash -Algorithm SHA256 -LiteralPath $ledger).Hash.ToLowerInvariant())
