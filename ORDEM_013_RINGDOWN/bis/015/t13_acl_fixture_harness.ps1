# The cleanup belongs to the harness, never to production seed custody.
$ErrorActionPreference='Stop'
$bench='C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN'
$base=[IO.Path]::GetFullPath((Join-Path $bench 'bis\015\t13'))
$fixture=[IO.Path]::GetFullPath((Join-Path $base 'ACL_CLEANUP_TEST_001'))
$receipt=Join-Path $base 'ACL_FINALLY_TEST.json'
if (Test-Path -LiteralPath $receipt) {throw 'Prior receipt; no repetition'}
if (Test-Path -LiteralPath $fixture) {throw 'Preexisting fixture; refuse to adopt'}
$result=@{scope='Native ACL synthetic fixture; original helper and production seed untouched';expected_error='T13_INJECTED_FAILURE_AFTER_NATIVE_ACL_CREATION';finally_entered=$false}
try {
    & 'C:\Python314\python.exe' -X utf8 -B (Join-Path $bench 'bis\015\t13_acl_fixture_worker.py') $fixture 2>&1 | Out-File -LiteralPath (Join-Path $base 'ACL_FINALLY_TEST.log') -Encoding utf8
    $result.worker_rc=$LASTEXITCODE
} catch {$result.harness_error=$_.Exception.Message}
finally {
    $result.finally_entered=$true
    try {
        if (-not $fixture.StartsWith($base+'\',[StringComparison]::OrdinalIgnoreCase)) {throw 'Unsafe fixture root'}
        $parent=Get-Item -LiteralPath $base -Force
        if ($parent.Attributes -band [IO.FileAttributes]::ReparsePoint) {throw 'Redirected parent'}
        if (Test-Path -LiteralPath $fixture) {
            $item=Get-Item -LiteralPath $fixture -Force
            if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {throw 'Redirected fixture'}
            Remove-Item -LiteralPath $fixture -Recurse -Force
        }
        $result.removed= -not (Test-Path -LiteralPath $fixture)
    } catch {$result.cleanup_error=$_.Exception.Message;$result.removed=$false}
    $result.at=[DateTime]::UtcNow.ToString('o')
    $tmp=$receipt+'.pending'
    [IO.File]::WriteAllText($tmp,($result|ConvertTo-Json -Depth 5),[Text.UTF8Encoding]::new($false))
    if ((Get-Item -LiteralPath $tmp).Length -eq 0) {throw 'Empty receipt'}
    Move-Item -LiteralPath $tmp -Destination $receipt
}
$result|ConvertTo-Json -Depth 5
