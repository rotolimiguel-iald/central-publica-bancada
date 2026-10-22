"""Append the verified ADENDO1 outcome to the surfaces named in claim 668."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import subprocess

B = Path(__file__).resolve().parent
M = Path(r'C:\IALD\Central de Patentes\memory')
def sha(data):
    return hashlib.sha256(data).hexdigest()
def exclusive(p, data):
    with p.open('xb') as f:
        f.write(data); f.flush(); os.fsync(f.fileno())
    assert p.read_bytes() == data

def main():
    receipt=B/'MEMORY_APPEND_ADENDO1_R1.json'
    journal=B/'MEMORY_APPEND_ADENDO1_JOURNAL_R1.jsonl'
    assert not receipt.exists() and not journal.exists(), 'Partial append must be recovered, not repeated'
    board=subprocess.run([r'C:\Python314\python.exe','-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','ver','F1.ATRATOR'],capture_output=True,check=True)
    state=json.loads(board.stdout)
    claim=state['reivindicacao']
    assert claim['quem']=='codex-gerente-tgl'
    assert datetime.fromisoformat(claim['vence_em'])>datetime.now(timezone.utc)
    result_path=B/'RESULTADO_ADENDO1_R1.json'
    raw=result_path.read_bytes(); r=json.loads(raw)
    assert r['claims']['A5']['verdict']=='PASSA_NO_MAPEAMENTO_DECLARADO'
    assert r['claims']['A6']['verdict']=='FALHA_MINIMALIDADE_OPERACIONAL'
    assert r['independent_review_passed'] is True
    marker='<!-- F1_ATRATOR_ADENDO1_20261010 -->'
    text=f'''\n\n## 10/10/2026 — F1.ATRATOR ADENDO1: autoleitura e controle da tríade
{marker}
Autor: codex-gerente-tgl, sob reivindicação F1.ATRATOR nº 668, que nomeia Atlas, Índice Vivo e TGL_CORE_MEMORY. Camada aditiva; cunhagens integrais no pré-registro, nas docstrings novas e no relatório, custodiadas por SHA256. O resumo abaixo é PARÁFRASE TÉCNICA; não substitui os quatro verbatims.

[REAL] A1–A4 mantêm o alcance da entrega R1. ADENDO1 pré-registrado antes dos novos ensaios (mapa seq 1002). A5 PASSA na leitura declarada sobre operadores: AdJ(F)=J∘F∘J e E_J=(F+AdJ(F))/2 no Pair real canônico; E_J²=E_J, E_J(J)=J e E_J(K)=0, reaproveitando J²=I e JKJ=−K. J²=J é FALSO na face não trivial. E_J fixa também I e tem dimensão de imagem 2 no M₂, logo não é o R de dimensão1 sobre estados. observing_adds_nothing permanece com seu tipo angular separado.

[REAL] A6 FALHA no mapeamento operacional pré-registrado: gerador zero (propagador identidade) e β=0/transmissão total conservam A1–A3, com a projeção do novo espaço fixo recalculada. A4 perde unicidade. Remover R da interface não apaga a projeção intrínseca. Espaço sem suporte é recusado por não vacuidade; o controle afim sem ponto fixo está fora da classe linear/CPTP. Esses casos não são convertidos em falso PASSA de minimalidade.

[ONTO] A singularidade como leitura universal, a tríade como célula da realidade e a nomenclatura Luz conservam seu estatuto. [DERIVED] O resultado negativo delimita esta tradução de T/G/L; não refuta a TGL inteira nem invalida A1–A5. Nenhuma significância física foi medida. β_TGL segue calculado em runtime; zero é intervenção do controle, não literal da constante.

Evidência nova: {result_path}; SHA256 {sha(raw)}. Relatório: RELATORIO_ADENDO1_R1.md. Compilações e revisão independente estão no pacote, com logs reais, trio e zero sorry. ENTREGUE é pedido à gerência; AUDITADA/FECHADA são atos da c1. Nada instalado no um.py, Nós ou Bancada; nenhum dado observado ou gate.
'''
    rows=[]; stamp=datetime.now().strftime('%Y%m%d_%H%M%S')
    with journal.open('xb') as j:
        for name in ('TGL_ATLAS.md','TGL_INDICE_VIVO.md','TGL_CORE_MEMORY.md'):
            p=M/name; before=p.read_bytes()
            assert marker.encode() not in before
            backup=p.with_name(p.name+'.bak_'+stamp)
            exclusive(backup,before)
            addition=text.replace('\n','\r\n') if b'\r\n' in before else text
            after=before+addition.encode('utf-8')
            tmp=p.with_name(p.name+'.tmp_F1_ATRATOR_ADENDO1_'+stamp)
            exclusive(tmp,after)
            assert p.read_bytes()==before, 'Concurrent edit; preserve temp and backup'
            os.replace(tmp,p)
            assert p.read_bytes()==after and len(after)>len(before)
            row={'path':str(p),'backup':str(backup),'before_sha256':sha(before),'after_sha256':sha(after),'before_bytes':len(before),'after_bytes':len(after),'pure_append':True}
            rows.append(row);j.write((json.dumps(row,ensure_ascii=False)+'\n').encode());j.flush();os.fsync(j.fileno())
    out={'claim':668,'unit':'F1.ATRATOR','author':'codex-gerente-tgl','created_utc':datetime.now(timezone.utc).isoformat(),'result_sha256':sha(raw),'surfaces':rows}
    exclusive(receipt,(json.dumps(out,ensure_ascii=False,indent=2)+'\n').encode())
    print(json.dumps(out,ensure_ascii=False))

if __name__=='__main__':
    main()
