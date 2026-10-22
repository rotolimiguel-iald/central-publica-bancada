"""Checkpoint Y jets, live review identity, and exact next contraction requirement."""
from pathlib import Path
from datetime import datetime,timezone
import json,sys
ROOT=Path(__file__).resolve().parents[1];H=ROOT/'A7';C=ROOT/'C6'
sys.path.insert(0,str(H))
from deliver_nonminimal_wick_and_mimo_audit import OUT,sha,write,put,append


def main():
    now=datetime.now(timezone.utc);D=C/'nonminimal_yjets_delivery';D.mkdir(exist_ok=False)
    result=json.loads((C/'nonminimal_yjets/results.json').read_bytes())
    opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    note=f'''[DERIVED+CAS — jatos Y do Euler métrico completo; montagem de vértices pendente]

AberturaSHA256={opening}.

Generalizada a ligação PH_hh do zerojet para derivadas Y ordenadas.
O termo HQ Kstar recebe a palavra Y externa ANTES da derivada do
Kstar: nabla_Yword nabla_Yc HQ, sem permutar derivadas covariantes.
A versão citada anterior fica preservada; a nova é
labelled_nonminimal_metric_euler_v2.py.

Conferência independente: diferenciou-se diretamente a expressão
rotulada inteira do zerojet, incluindo as conexões em seus dois índices
Y e nos índices das derivadas. O resultado coincide termo a termo
com derivar os blocos antes de montar Schur. São100 componentes,
21 palavras Y (comprimentos0,1,2), duas ordens de curvatura:
4200 identidades, mais100 regressões dos contatos prévios.
CPU{result['cpu_seconds']}s; rc0; sem mudança de prescrição.

PRÓXIMA CONTRAÇÃO: o bitensor armazenado tem os quatro índices
covariantes. Ao contrair com Lie_c h, que tem índices covariantes,
os índices Euler em X devem ser elevados com gX^{{ai}}gX^{{bj}}
ANTES de aplicar a extensão rotulada. No ponto normal a métrica
é identidade, mas suas derivadas não podem ser apagadas antes
de agir sobre derivadas de delta. O antighost já possui a dualização
separada verificada. Não somar as tabelas de zerojet como se fossem
o representante Q2 nem reaplicar pesos dos grafos planos já reduzidos.

Crítica Kimi: request b4af3263-e352-408a-a7fa-6c263a7d7d4a,
job b86007e9-8574-46dc-b950-0da6347191c9, execution
450d3e6e-27a6-4766-82fc-bb4bf17f644e; running reportado pela
coordenação, sem resultado recebido. Não repetir chamada.
C6 mantém prazo2026-09-26T06:07:12.868245Z. Gate e originais intactos.
'''
    write(D/'DERIVACAO.md',note.encode());write(OUT/'ENTREGA_016_MEDIDA_C6_jatos_Schur_Y.md',note.encode())
    paths=[Path(__file__),C/'nonminimal_yjets/manifest.json',C/'nonminimal_yjets/results.json',C/'nonminimal_yjets_check_run.log',C/'labelled_nonminimal_metric_euler_v2.py',C/'orchestration_dual_schur/COORDINATOR_REPORTED.json',D/'DERIVACAO.md']
    put(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in paths],opening_sha256=opening,full_Q2=False,gate_changed=False))
    append(OUT/'LEDGER_016.jsonl',json.dumps(dict(at=now.isoformat(),event='C6_NONMINIMAL_Y_JETS_CHECKPOINT',target='C6',remote_call=False,checks=result['checks'],cpu_seconds=result['cpu_seconds'],manifest_sha256=sha(D/'manifest.json')),ensure_ascii=False)+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} | C6ACTIVE: PH_hh com21palavrasY em100componentes ligado;{result["checks"]}checks CPU{result["cpu_seconds"]}s,rc0; montagem física dos índices/vértices pendente; Kimi b86007e9 emexecução, sem repetir.\n')
    p=H/'CONTINUIDADE.json';state=json.loads(p.read_bytes());state.update(at=now.isoformat(),C6_nonminimal_yjets_manifest=str(D/'manifest.json'),own_live_process=None,next='Auditar Kimi b86007e9; montar vertices com Euler X elevado por gInv duas vezes antes da extensao, ghost dual pronto. C6 deadline06:07:12Z sem reinicio. Depois PartB integral.')
    put(p,state,True)
    print(json.dumps(dict(manifest=str(D/'manifest.json'),checks=result['checks'],remote_call=False)))


if __name__=='__main__':main()
