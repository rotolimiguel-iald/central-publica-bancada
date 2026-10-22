$ErrorActionPreference = 'Stop'
$benchRoot = 'C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN'
$cacheRoot = (Resolve-Path -LiteralPath (Join-Path $benchRoot 'cache')).Path
$allowedNames = @('supplement_guard_c4m7d6mv', 'supplement_guard_oxfe5hli', 'gwtc3_guard_7zm1dt74', 'package_clean_79ggpm17')
$receipts = @()
foreach ($folderName in $allowedNames) {
    $targetPath = (Resolve-Path -LiteralPath (Join-Path $cacheRoot $folderName)).Path
    if ($targetPath -ne (Join-Path $cacheRoot $folderName)) { throw 'Resolved target differs from explicit authorized path' }
    if ((Split-Path -Parent $targetPath) -ne $cacheRoot) { throw 'Target escaped cache root' }
    $entry = Get-Item -LiteralPath $targetPath -Force
    if ($entry.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Target is a reparse point' }
    $children = @(Get-ChildItem -LiteralPath $targetPath -Recurse -Force)
    if (@($children | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint }).Count -gt 0) { throw 'Nested reparse point refused' }
    $files = @($children | Where-Object { -not $_.PSIsContainer } | ForEach-Object {
        @{ path = $_.FullName; bytes = $_.Length; sha256 = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant() }
    })
    $receipt = @{
        target = $targetPath; files = $files; file_count = $files.Count
        bytes = ($files | Measure-Object -Property bytes -Sum).Sum
        identity = [Security.Principal.WindowsIdentity]::GetCurrent().Name
        listed_utc = [DateTime]::UtcNow.ToString('o')
        authorization = 'ORDEM_013BIS F7: four explicitly named mkdtemp directories'
        source_canonical_untouched = $true
    }
    $receiptPath = Join-Path $benchRoot ('bis\F7_TEMP_' + $folderName + '_BEFORE.json')
    if (Test-Path -LiteralPath $receiptPath) { throw 'Receipt exists; do not overwrite custody' }
    $receiptTemp = $receiptPath + '.tmp'
    $json = $receipt | ConvertTo-Json -Depth 10
    [IO.File]::WriteAllText($receiptTemp, $json, [Text.UTF8Encoding]::new($false))
    if ((Get-Item -LiteralPath $receiptTemp).Length -lt 100) { throw 'Unexpected empty receipt' }
    Move-Item -LiteralPath $receiptTemp -Destination $receiptPath
    # All resolved paths and every child have been checked above; native PowerShell end-to-end.
    Remove-Item -LiteralPath $targetPath -Recurse -Force
    if (Test-Path -LiteralPath $targetPath) { throw 'Directory still exists after removal' }
    $receipts += @{
        target = $targetPath; removed_utc = [DateTime]::UtcNow.ToString('o')
        inventory = $receiptPath; inventory_sha256 = (Get-FileHash -LiteralPath $receiptPath -Algorithm SHA256).Hash.ToLowerInvariant()
        file_count = $files.Count; bytes = $receipt.bytes; absent_after = $true
    }
}
$resultPath = Join-Path $benchRoot 'bis\F7_NAMED_TEMPORARIES_REMOVED.json'
if (Test-Path -LiteralPath $resultPath) { throw 'Final receipt already exists' }
$finalText = @{ status = 'REMOVED_FOUR_AUTHORIZED_TEMPORARIES'; directories = $receipts } | ConvertTo-Json -Depth 10
[IO.File]::WriteAllText(($resultPath + '.tmp'), $finalText, [Text.UTF8Encoding]::new($false))
Move-Item -LiteralPath ($resultPath + '.tmp') -Destination $resultPath
$receipts | Select-Object target, file_count, bytes, absent_after | Format-Table
Get-FileHash -LiteralPath $resultPath -Algorithm SHA256
