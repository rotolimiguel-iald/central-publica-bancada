#!/usr/bin/env bash
# cc.sh <Arquivo.lean> — compila ISOLADO em forma_inscrita_da_luz/habitante_v3/lean (-R/-o/-i aqui); NUNCA lake build;
# LEAN_PATH = esta pasta + o LEAN_PATH do `lake env` do kernel (so leitura); find -newer no fim.
set -u
KERNEL="/c/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel"
HERE="/c/Users/rotol/AppData/Local/Temp/claude/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d/scratchpad/forma_inscrita_da_luz/habitante_v3/lean"
HEREWIN='C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\forma_inscrita_da_luz\habitante_v3\lean'
SRC="$1"; base="${SRC%.lean}"; LOG="$HERE/logs/$base.txt"
cd "$KERNEL" || exit 99
LP="$(lake env printenv LEAN_PATH)"
STAMP="$HERE/logs/.stamp_$$"; touch "$STAMP"
export LEAN_PATH="$HEREWIN;$LP"
t0=$(date +%s)
BS="\\"
lean -R "$HEREWIN" -o "$HEREWIN$BS$base.olean" -i "$HEREWIN$BS$base.ilean" "$HEREWIN$BS$base.lean" > "$LOG" 2>&1
rc=$?
echo "rc=$rc elapsed=$(( $(date +%s)-t0 ))s" >> "$LOG"
newer=$(find "$KERNEL" -newer "$STAMP" -type f 2>/dev/null | wc -l)
gnewer=$(find "$KERNEL" -newer "$HERE/logs/.STAMP_INICIO" -type f 2>/dev/null | wc -l)
echo "kernel_files_newer_than_stamp=$newer kernel_files_newer_than_start=$gnewer" >> "$LOG"
rm -f "$STAMP"
echo "$SRC rc=$rc kernel_touched=$newer since_start=$gnewer"
