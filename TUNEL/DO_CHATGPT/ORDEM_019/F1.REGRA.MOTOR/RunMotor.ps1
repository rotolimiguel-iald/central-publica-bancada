# Replay only the pinned synthetic continuous motor. Each run creates a new receipt.
$ErrorActionPreference = 'Stop'
$motorPython = 'C:\Users\rotol\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$motorRunner = Join-Path $PSScriptRoot 'runtime\run_rule_motor.py'
$motorFreeze = Join-Path $PSScriptRoot 'runtime\freezes\20261014T142932_627224Z.json'
& $motorPython -B $motorRunner --replay $motorFreeze
exit $LASTEXITCODE
