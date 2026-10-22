#!/usr/bin/env bash
# cc.sh <Arquivo.lean> : compila no diretorio cetico_brinquedo; LEAN_PATH = cb ; v3 ; lake env do kernel v370.
# Nunca lake build; olean/ilean so em cetico_brinquedo; find -newer no kernel E em v3 ao fim.
set -u
KERNEL="/c/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel"
CB="/c/Users/rotol/AppData/Local/Temp/claude/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d/scratchpad/contrato_v3/cetico_brinquedo"
V3="/c/Users/rotol/AppData/Local/Temp/claude/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d/scratchpad/contrato_v3/v3"
CBWIN='C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\contrato_v3\cetico_brinquedo'
V3WIN='C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\contrato_v3\v3'
SRC="$1"; base="${SRC%.lean}"; LOG="$CB/logs/$base.txt"
STAMP="$CB/logs/.stamp_$$_$RANDOM"; touch "$STAMP"
cd "$KERNEL" || exit 99
LP="$(lake env printenv LEAN_PATH)"
export LEAN_PATH="$CBWIN;$V3WIN;$LP"
t0=$(date +%s)
BS='\'
lean -R "$CBWIN" -o "$CBWIN$BS$base.olean" -i "$CBWIN$BS$base.ilean" "$CBWIN$BS$base.lean" > "$LOG" 2>&1
rc=$?
echo "rc=$rc elapsed=$(( $(date +%s)-t0 ))s" >> "$LOG"
nk=$(find "$KERNEL" -newer "$STAMP" -type f 2>/dev/null | wc -l)
nv=$(find "$V3" -newer "$STAMP" -type f 2>/dev/null | wc -l)
echo "kernel_files_newer_than_stamp=$nk v3_files_newer_than_stamp=$nv" >> "$LOG"
rm -f "$STAMP"
echo "$SRC rc=$rc kernel_touched=$nk v3_touched=$nv"
