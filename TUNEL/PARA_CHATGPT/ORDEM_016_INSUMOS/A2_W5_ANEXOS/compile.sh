#!/usr/bin/env bash
# compile.sh <arquivo.lean relativo a W5_final> <log>   -- frente W5_final, 23/09/2026
# Compila SO no scratchpad: -R W5_final (nome de modulo = caminho relativo, p.ex. TGLExt.ContratoQG),
# -o/-i dentro de W5_final; LEAN_PATH = W5_final + o LEAN_PATH do `lake env` do kernel canonico.
# NUNCA lake build; NUNCA escreve no kernel (conferido por find -newer no fim).
set -u
KERNEL="/c/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel"
W5="/c/Users/rotol/AppData/Local/Temp/claude/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d/scratchpad/qg_ataque/W5_final"
W5WIN='C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\qg_ataque\W5_final'
SRC="$1"; LOG="$2"
cd "$KERNEL" || exit 99
LP="$(lake env printenv LEAN_PATH)"
STAMP="$W5/.stamp_$$"; touch "$STAMP"
base="${SRC%.lean}"
export LEAN_PATH="$W5WIN;$LP"
lean -R "$W5WIN" -o "$W5WIN\\${base//\//\\}.olean" -i "$W5WIN\\${base//\//\\}.ilean" "$W5WIN\\${SRC//\//\\}" > "$W5/$LOG" 2>&1
rc=$?
echo "rc=$rc" >> "$W5/$LOG"
newer=$(find "$KERNEL" -newer "$STAMP" -type f 2>/dev/null | wc -l)
echo "kernel_files_newer_than_stamp=$newer" >> "$W5/$LOG"
rm -f "$STAMP"
echo "$SRC rc=$rc kernel_touched=$newer"
