"""Freeze the prespecified C4 decision rule in the authorized return tunnel."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib

ROOT=Path(__file__).resolve().parent
target=ROOT.parent/'TUNEL'/'DO_CHATGPT'/'ENTREGA_013_C4a_REGISTRO_POSTERIORES.md'
registration=ROOT/'REGISTRO_C4.json'
raw=registration.read_bytes()
digest=hashlib.sha256(raw).hexdigest()
body=f'''[REAL — registro de procedimento; análise NÃO-CEGA; entrega parcial, não fechamento do M1]

# ORDEM 013 — Registro antes da inspeção local dos posteriores

UTC: {datetime.now(timezone.utc).isoformat()}

Registro: `{registration}`
SHA256: `{digest}`

PAGO: regra relativa de exclusão fixada em B(leitura/RG) <= 1/100 e RG dentro da região credível de 95%; instabilidade das caudas KDE impede exclusão forte. Valores centrais publicados já eram conhecidos. Nenhuma confirmação física ou mudança de gate.

PAGO: priors de relógio livre (uniforme e log-uniforme) fixados no JSON; prioridade de releases e não contagem dupla por evento; comparação conjunta, controle de largura KDE e bootstrap previstos.

CORREÇÃO ESTATÍSTICA AO LADO: para uma curva delta=g(eta), o Bayes factor é razão de integrais de densidade corrigida pelo prior, não a média de razões condicionais. O JSON registra a identidade, derivada de Bayes com prior de nuisance comum. Antes de usar o release, serão conferidos seus priors efetivos.

NÃO PAGO: inferência nos posteriores, controles completos de PSD, injeções e leitura de strain. O download público pode estar em andamento; baixar o arquivo não constitui analisar suas amostras. O registro C6, anterior à leitura da janela de strain, ainda será separado.

Reprodução da identidade do registro: calcular SHA256 do arquivo acima e comparar com este recibo. Este recibo é criado uma vez; emenda exige arquivo novo.

O alcance original permanece: taxas por leitura, forma de onda, distribuição de ln B, confronto com posteriores e strain, pacote reprodutível. Este registro não redefine a missão como encerrada.
'''
if target.exists():raise FileExistsError(target)
temp=target.with_suffix('.tmp')
temp.write_bytes(body.encode('utf-8'))
assert temp.stat().st_size==len(body.encode('utf-8'))
temp.replace(target)
print(str(target));print(digest)
