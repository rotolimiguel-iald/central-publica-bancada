#!/usr/bin/env bash
# compila_tudo.sh — RODADA 2: recompila TUDO da v3.1 em ordem de dependência, logs em logs/final_*.txt.
# Só escreve em v31/. v3 entra SÓ como leitura (XPATH) para a Ponte. Nunca lake build.
set -u
V31="/c/Users/rotol/AppData/Local/Temp/claude/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d/scratchpad/contrato_v3/v31"
V3W='C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\contrato_v3\v3'
cd "$V31" || exit 9
rm -f ./*.olean ./*.ilean
c() { bash compile.sh "$1" "$V31/logs/final_${1%.lean}.txt"; }
# 0. referências byte-idênticas (v2, W5) — independentes do tipo
c ContratoQG.lean
c W5ParedeEspectral.lean & c ProbeToyContratoH2.lean & wait
# 1. o tipo
c ContratoQG_v31.lean
# 2. teoremas + probes que só importam o tipo
c ContratoQG_v31_Teoremas.lean &
for f in ProbeToyV31 ProbeLegacyV31 ProbeVacuousImportV31 ProbeTrivialH3v31 ProbeAjustadorV31 ProbeRekappaV31 ProbeResidualH3v31; do c $f.lean & done
wait
# 3. o que importa os teoremas
c ContratoQG_v31_Paredes.lean & c FlagNetV31.lean & (XPATH="$V3W" c PonteV3V31.lean) & wait
# 4. refolean (cópia dos oleans de referência para a mutação)
mkdir -p refolean; for m in ContratoQG W5ParedeEspectral ProbeToyContratoH2; do cp $m.olean $m.ilean refolean/; done
echo FIM
