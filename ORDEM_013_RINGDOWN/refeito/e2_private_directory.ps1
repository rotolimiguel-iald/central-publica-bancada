param([ValidateSet('Prepare','Verify','VerifySeed')][string]$Action = 'Verify')
$ErrorActionPreference = 'Stop'
$basePath = Split-Path -Parent $PSScriptRoot
$cachePath = Join-Path $basePath 'cache'
$privatePath = Join-Path $cachePath 'E2_PRIVATE'
$sid = [System.Security.Principal.WindowsIdentity]::GetCurrent().User
foreach ($path in @($basePath, $cachePath)) {
    $item = Get-Item -LiteralPath $path
    if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) { throw 'Redirected parent refused' }
}
if ($Action -eq 'Prepare') {
    if (Test-Path -LiteralPath $privatePath) { throw 'Private directory already exists; no silent retry' }
    New-Item -ItemType Directory -Path $privatePath | Out-Null
    $security = [System.Security.AccessControl.DirectorySecurity]::new()
    $security.SetOwner($sid)
    $security.SetAccessRuleProtection($true, $false)
    $rule = [System.Security.AccessControl.FileSystemAccessRule]::new($sid, 'FullControl', 'ContainerInherit,ObjectInherit', 'None', 'Allow')
    $security.AddAccessRule($rule)
    Set-Acl -LiteralPath $privatePath -AclObject $security
}
$item = Get-Item -LiteralPath $privatePath
if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) { throw 'Redirected private directory refused' }
$actual = Get-Acl -LiteralPath $privatePath
$rules = @($actual.GetAccessRules($true,$true,[System.Security.Principal.SecurityIdentifier]))
if (-not $actual.AreAccessRulesProtected -or $rules.Count -ne 1) { throw 'Private DACL not exclusive/protected' }
$entry = $rules[0]
if ($entry.IdentityReference.Value -ne $sid.Value -or $entry.AccessControlType -ne 'Allow' -or $entry.IsInherited -or $entry.FileSystemRights -ne 'FullControl' -or $entry.InheritanceFlags -ne 'ContainerInherit, ObjectInherit') { throw 'Private DACL differs' }
if ($Action -eq 'VerifySeed') {
    $seedPath = Join-Path $privatePath 'BLIND_SEED_V1.bin.pending'
    $seedItem = Get-Item -LiteralPath $seedPath
    if (($seedItem.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) { throw 'Redirected seed refused' }
    $seedAcl = Get-Acl -LiteralPath $seedPath
    $seedRules = @($seedAcl.GetAccessRules($true,$true,[System.Security.Principal.SecurityIdentifier]))
    if ($seedRules.Count -ne 1 -or $seedRules[0].IdentityReference.Value -ne $sid.Value -or $seedRules[0].AccessControlType -ne 'Allow' -or $seedRules[0].FileSystemRights -ne 'FullControl') { throw 'Seed DACL differs' }
}
@{status='CURRENT_WINDOWS_USER_ONLY_DACL_VERIFIED';protected=$true;allow_rules=$rules.Count;path=$privatePath;scope='Windows ACL, same-user processes including WSL remain able to read; not independent custody'} | ConvertTo-Json -Compress
