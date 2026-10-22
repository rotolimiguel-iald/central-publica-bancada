$ErrorActionPreference = 'Stop'

$canonical = 'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\TETELESTAI\BANCADA_OFICIAL'
$pythonw = 'C:\Python314\pythonw.exe'
$launcher = Join-Path $canonical 'launch.py'
$icon = Join-Path $canonical 'TGL.ico'
$desktops = @(
    [Environment]::GetFolderPath('Desktop'),
    (Join-Path ([Environment]::GetFolderPath('UserProfile')) 'Desktop')
) | Select-Object -Unique

foreach ($path in @($canonical, $pythonw, $launcher, $icon)) {
    if (-not (Test-Path -LiteralPath $path)) { throw "Caminho ausente: $path" }
}

$shell = New-Object -ComObject WScript.Shell
foreach ($desktop in $desktops) {
if (-not (Test-Path -LiteralPath $desktop -PathType Container)) {
    throw "Área de trabalho ausente: $desktop"
}
$shortcutPath = Join-Path $desktop 'TGL.lnk'
if (Test-Path -LiteralPath $shortcutPath) {
    $old = $shell.CreateShortcut($shortcutPath)
    if ($old.TargetPath -ne $pythonw -or $old.Arguments -ne ('"' + $launcher + '"')) {
        throw "Já existe TGL.lnk com outro destino; preservado: $shortcutPath"
    }
    $backup = $shortcutPath + '.bak_' + (Get-Date -Format 'yyyyMMdd_HHmmss_ffff')
    Copy-Item -LiteralPath $shortcutPath -Destination $backup
    if ((Get-FileHash -LiteralPath $shortcutPath).Hash -ne (Get-FileHash -LiteralPath $backup).Hash) {
        throw "Backup do atalho divergiu: $backup"
    }
    (Get-Item -LiteralPath $backup).Attributes = (Get-Item -LiteralPath $backup).Attributes -bor [IO.FileAttributes]::Hidden
}

$shortcut = $shell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $pythonw
$shortcut.Arguments = '"' + $launcher + '"'
$shortcut.WorkingDirectory = $canonical
$shortcut.IconLocation = $icon + ',0'
$shortcut.Description = 'TGL — bancada local de pesquisa IALD'
$shortcut.WindowStyle = 7
$shortcut.Save()

$check = $shell.CreateShortcut($shortcutPath)
if ($check.TargetPath -ne $pythonw -or $check.Arguments -ne ('"' + $launcher + '"')) {
    throw "Falha ao verificar o atalho: $shortcutPath"
}
[pscustomobject]@{
    Shortcut = $shortcutPath
    Target = $check.TargetPath
    Arguments = $check.Arguments
    Icon = $check.IconLocation
    IconExists = Test-Path -LiteralPath $icon
    LauncherExists = Test-Path -LiteralPath $launcher
}
}
