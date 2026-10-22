#!/usr/bin/env bash
# compile.sh <arquivo.lean relativo a ROOT> <log> [ROOT_windows_extra]
# Compila SO no scratchpad contrato_v3: -R ROOT (default v3), -o/-i dentro de ROOT;
# LEAN_PATH = [ROOT;] v3 + o LEAN_PATH do `lake env` do kernel canonico v370.
# NUNCA lake build; NUNCA escreve no kernel (conferido por find -newer no fim).
set -u
KERNEL="/c/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel"
V3="/c/Users/rotol/AppData/Local/Temp/claude/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d/scratchpad/contrato_v3/v3"
V3WIN='C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\contrato_v3\v3'
SRC="$1"; LOG="$2"; EXTRA="${3:-}"
cd "$KERNEL" || exit 99
LP="$(lake env printenv LEAN_PATH)"
STAMP="$V3/logs/.stamp_$$_$RANDOM"; touch "$STAMP"
base="${SRC%.lean}"
BS='\'
basew=$(printf '%s' "$base" | sed 's#/#\\#g')
if [ -n "$EXTRA" ]; then
  export LEAN_PATH="$EXTRA;$V3WIN;$LP"; ROOT="$EXTRA"
else
  export LEAN_PATH="$V3WIN;$LP"; ROOT="$V3WIN"
fi
t0=$(date +%s)
lean -R "$ROOT" -o "$ROOT$BS$basew.olean" -i "$ROOT$BS$basew.ilean" "$ROOT$BS$basew.lean" > "$LOG" 2>&1
rc=$?
echo "rc=$rc elapsed=$(( $(date +%s)-t0 ))s" >> "$LOG"
newer=$(find "$KERNEL" -newer "$STAMP" -type f 2>/dev/null | wc -l)
echo "kernel_files_newer_than_stamp=$newer" >> "$LOG"
rm -f "$STAMP"
echo "$SRC rc=$rc kernel_touched=$newer"
