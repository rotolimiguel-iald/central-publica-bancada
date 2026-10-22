$ErrorActionPreference = 'Stop'
$bench = [IO.Path]::GetFullPath('C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN')
$receipt = Join-Path $bench 'bis\015\t13\WINDOWS_CLEANUP.json'
if (Test-Path -LiteralPath $receipt) { throw 'Receipt exists; inspect instead of repeating.' }
[IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($receipt)) | Out-Null
function Metadata([string]$path) {
    try {
        $item = Get-Item -Force -LiteralPath $path -ErrorAction Stop
        return @{path=$path;exists=$true;length=$item.Length;mtime_utc=$item.LastWriteTimeUtc.ToString('o');attributes=[string]$item.Attributes}
    } catch {
        return @{path=$path;exists=$null;error=$_.Exception.Message;error_id=$_.FullyQualifiedErrorId}
    }
}
function CheckedFixture([string]$path) {
    $full = [IO.Path]::GetFullPath($path)
    $allowed = Join-Path $bench 'bis\e2_publication_census'
    if (-not $full.StartsWith($allowed + '\',[StringComparison]::OrdinalIgnoreCase)) { throw 'Outside fixture namespace' }
    $parent = [IO.Directory]::GetParent($full)
    while ($null -ne $parent -and $parent.FullName.Length -ge $bench.Length) {
        $item = Get-Item -Force -LiteralPath $parent.FullName -ErrorAction Stop
        if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Redirected parent refused' }
        $parent = $parent.Parent
    }
    return $full
}
$seedPaths = @((Join-Path $bench 'cache\E2_PRIVATE\BLIND_SEED_V1.bin'),(Join-Path $bench 'bis\cache\E2_PRIVATE\BLIND_SEED_V1.bin'))
$before = @($seedPaths | ForEach-Object { Metadata $_ })
$targets = @(
 'bis\e2_publication_census\CUSTODY_TRANSFER_FIXTURE_20260922T214938\cache\E2_PRIVATE',
 'bis\e2_publication_census\NATIVE_ACL_FIXTURE_20260922T213829\cache\E2_PRIVATE',
 'bis\e2_publication_census\NATIVE_ACL_FIXTURE_20260922T213829\allocation_case\cache\E2_PRIVATE'
)
$rows = @()
foreach ($relative in $targets) {
    $path = Join-Path $bench $relative
    $row = @{path=$path;before=(Metadata $path);command='Remove-Item -LiteralPath <exact verified fixture> -Recurse -Force';status='NOT_ATTEMPTED'}
    try {
        $verified = CheckedFixture $path
        $item = Get-Item -Force -LiteralPath $verified -ErrorAction Stop
        if (-not $item.PSIsContainer -or ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw 'Non-directory or redirected target refused' }
        # Refuse to recurse through any link. Access denial is retained, never bypassed.
        $children = @(Get-ChildItem -LiteralPath $verified -Force -Recurse -ErrorAction Stop)
        if (@($children | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint }).Count) { throw 'Reparse child refused' }
        Remove-Item -LiteralPath $verified -Recurse -Force -ErrorAction Stop
        $row.status = 'REMOVED'
    } catch { $row.status='NOT_REMOVED';$row.error=$_.Exception.Message;$row.error_id=$_.FullyQualifiedErrorId }
    $row.after=Metadata $path;$rows += $row
}
$junction = Join-Path $bench 'bis\e2_publication_census\NATIVE_ACL_FIXTURE_20260922T213829\junction_alias'
$link = @{path=$junction;before=(Metadata $junction);command='System.IO.Directory.Delete(exact junction, false)';status='NOT_ATTEMPTED'}
try {
    $verified=CheckedFixture $junction
    $item=Get-Item -LiteralPath $verified -Force -ErrorAction Stop
    if ($item.LinkType -ne 'Junction') { throw 'Expected Junction; no deletion' }
    [IO.Directory]::Delete($verified,$false)
    $link.status='UNLINKED_WITHOUT_TARGET_RECURSION'
} catch {$link.status='NOT_REMOVED';$link.error=$_.Exception.Message}
$link.after=Metadata $junction
$after=@($seedPaths | ForEach-Object {Metadata $_})
$sid=[Security.Principal.WindowsIdentity]::GetCurrent().User.Value
$sidHash=[Convert]::ToHexString([Security.Cryptography.SHA256]::HashData([Text.Encoding]::UTF8.GetBytes($sid))).ToLowerInvariant()
$result=@{at=[DateTime]::UtcNow.ToString('o');seed_before=$before;seed_after=$after;seed_content_read=$false;rows=$rows;junction=$link;identity_sid_sha256=$sidHash;takeown_used=$false;scope='Only three literal fixture paths plus literal junction; no substitution for 214951'}
$raw=$result | ConvertTo-Json -Depth 10
$tmp=$receipt+'.pending'
[IO.File]::WriteAllText($tmp,$raw,[Text.UTF8Encoding]::new($false))
if ((Get-Item -LiteralPath $tmp).Length -le 0) {throw 'Empty receipt'}
Move-Item -LiteralPath $tmp -Destination $receipt
$result | ConvertTo-Json -Depth 10
