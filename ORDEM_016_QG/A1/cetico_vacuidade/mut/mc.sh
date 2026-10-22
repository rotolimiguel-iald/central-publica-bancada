#!/usr/bin/env bash
# mc.sh <RUNWIN> <arquivo.lean> <log> : compila no diretório de rodada; LEAN_PATH = RUN;SRC;kernel
set -u
KERNEL="/c/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel"
SRCWIN='C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\contrato_v3\cetico_vacuidade\src'
RUN="$1"; SRC="$2"; LOG="$3"
cd "$KERNEL" || exit 99
LP="$(lake env printenv LEAN_PATH)"
STAMP="$(dirname "$LOG")/.stamp_$$_$RANDOM"; touch "$STAMP"
base="${SRC%.lean}"; BS='\'
export LEAN_PATH="$RUN;$SRCWIN;$LP"
lean -R "$RUN" -o "$RUN$BS$base.olean" -i "$RUN$BS$base.ilean" "$RUN$BS$base.lean" > "$LOG" 2>&1
rc=$?
echo "rc=$rc" >> "$LOG"
newer=$(find "$KERNEL" -newer "$STAMP" -type f 2>/dev/null | wc -l)
echo "kernel_files_newer_than_stamp=$newer" >> "$LOG"
rm -f "$STAMP"
