#!/usr/bin/env bash
# compile.sh <arquivo.lean relativo a ROOT> <log> [ROOT_windows] — RODADA 2 (v3.1).
# Compila SO no scratchpad contrato_v3/v31: -R ROOT (default v31), -o/-i dentro de ROOT;
# LEAN_PATH = [ROOT;] v31 + o LEAN_PATH do `lake env` do kernel canonico v370.
# NUNCA lake build; NUNCA escreve no kernel (conferido por find -newer no fim, contra carimbo local E contra o
# carimbo global do inicio da rodada 2).
set -u
KERNEL="/c/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel"
V31="/c/Users/rotol/AppData/Local/Temp/claude/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d/scratchpad/contrato_v3/v31"
V31WIN='C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\contrato_v3\v31'
SRC="$1"; LOG="$2"; EXTRA="${3:-}"
case "$LOG" in /*) ;; *) LOG="$(pwd)/$LOG";; esac
cd "$KERNEL" || exit 99
LP="$(lake env printenv LEAN_PATH)"
STAMP="$V31/logs/.stamp_$$_$RANDOM"; touch "$STAMP"
base="${SRC%.lean}"
BS='\'
basew=$(printf '%s' "$base" | tr '/' '\\')
if [ -n "$EXTRA" ]; then
  export LEAN_PATH="$EXTRA;$V31WIN;$LP"; ROOT="$EXTRA"
else
  export LEAN_PATH="$V31WIN;$LP"; ROOT="$V31WIN"
fi
# XPATH (opcional): diretórios SÓ DE LEITURA de oleans (ex.: a v3), anexados DEPOIS de ROOT — nunca escritos.
if [ -n "${XPATH:-}" ]; then export LEAN_PATH="$ROOT;$XPATH;$LP"; fi
t0=$(date +%s)
lean -R "$ROOT" -o "$ROOT$BS$basew.olean" -i "$ROOT$BS$basew.ilean" "$ROOT$BS$basew.lean" > "$LOG" 2>&1
rc=$?
echo "rc=$rc elapsed=$(( $(date +%s)-t0 ))s" >> "$LOG"
newer=$(find "$KERNEL" -newer "$STAMP" -type f 2>/dev/null | wc -l)
gnewer=$(find "$KERNEL" -newer "$V31/logs/.STAMP_INICIO_R2" -type f 2>/dev/null | wc -l)
echo "kernel_files_newer_than_stamp=$newer kernel_files_newer_than_R2_start=$gnewer" >> "$LOG"
rm -f "$STAMP"
echo "$SRC rc=$rc kernel_touched=$newer kernel_touched_since_R2=$gnewer"
