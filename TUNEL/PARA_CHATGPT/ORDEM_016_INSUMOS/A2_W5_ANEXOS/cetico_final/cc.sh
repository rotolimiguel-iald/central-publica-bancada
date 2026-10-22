#!/usr/bin/env bash
set -u
KERNEL="/c/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel"
D="/c/Users/rotol/AppData/Local/Temp/claude/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d/scratchpad/qg_ataque/W5_final/cetico_final"
DW='C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\qg_ataque\W5_final\cetico_final'
SRC="$1"; LOG="$2"
cd "$KERNEL" || exit 99
LP="$(lake env printenv LEAN_PATH)"
STAMP="$D/.stamp_$$"; touch "$STAMP"
base="${SRC%.lean}"
export LEAN_PATH="$DW;$LP"
start=$(date +%s)
B="\\"
lean -R "$DW" -o "${DW}${B}${base}.olean" -i "${DW}${B}${base}.ilean" "${DW}${B}${SRC}" > "$D/$LOG" 2>&1
rc=$?
end=$(date +%s)
echo "rc=$rc secs=$((end-start))" >> "$D/$LOG"
newer=$(find "$KERNEL" -newer "$STAMP" -type f 2>/dev/null | wc -l)
echo "kernel_files_newer_than_stamp=$newer" >> "$D/$LOG"
rm -f "$STAMP"
echo "$SRC rc=$rc kernel_touched=$newer errors=$(grep -c ': error' "$D/$LOG") axioms_lines=$(grep -c 'depends on axioms' "$D/$LOG") nontrio=$(grep 'depends on axioms' "$D/$LOG" | grep -v 'depends on axioms: \[propext, Classical.choice, Quot.sound\]' | wc -l) sorry=$(grep -c sorryAx "$D/$LOG")"
