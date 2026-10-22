#!/usr/bin/env bash
# compile_c.sh <arquivo.lean relativo a SRC> <log> — cético 2 (vacuidade). Só escreve em cetico_vacuidade/.
set -u
KERNEL="/c/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel"
CVWIN='C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\contrato_v3\cetico_vacuidade'
ROOT="${3:-$CVWIN\src}"
CV="/c/Users/rotol/AppData/Local/Temp/claude/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d/scratchpad/contrato_v3/cetico_vacuidade"
SRC="$1"; LOG="$2"
cd "$KERNEL" || exit 99
LP="$(lake env printenv LEAN_PATH)"
STAMP="$CV/logs/.stamp_$$_$RANDOM"; touch "$STAMP"
base="${SRC%.lean}"
BS='\'
export LEAN_PATH="$ROOT;$LP"
t0=$(date +%s)
lean -R "$ROOT" -o "$ROOT$BS$base.olean" -i "$ROOT$BS$base.ilean" "$ROOT$BS$base.lean" > "$LOG" 2>&1
rc=$?
echo "rc=$rc elapsed=$(( $(date +%s)-t0 ))s" >> "$LOG"
newer=$(find "$KERNEL" -newer "$STAMP" -type f 2>/dev/null | wc -l)
echo "kernel_files_newer_than_stamp=$newer" >> "$LOG"
rm -f "$STAMP"
echo "$SRC rc=$rc kernel_touched=$newer"
