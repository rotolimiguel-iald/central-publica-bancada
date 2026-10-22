"""Consolidate T01 evidence and preserve the pending external approval/review."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import json,hashlib,uuid
B=Path(__file__).resolve().parents[2];ROOT=B.parent;OUT=ROOT/'TUNEL/DO_CHATGPT'
D=B/'bis/015/t01_delivery';R=ROOT/'ORDEM_016_QG'
now=datetime.now(timezone.utc);stamp=now.strftime('%Y%m%d_%H%M%S_%f')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,raw,replace=False):
    if p.exists():
        assert replace
        old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+stamp)
        with bak.open('xb') as f:f.write(old)
        assert bak.read_bytes()==old
    temp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    with temp.open('xb') as f:f.write(raw)
    assert temp.read_bytes()==raw;temp.replace(p)
def put(p,obj,replace=False):write(p,(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode(),replace)
def append(p,text):write(p,p.read_bytes()+text.encode(),True)
def main():
    D.mkdir(exist_ok=False)
    evidence=[B/'bis/015/t01_core/manifest.json',B/'bis/015/t01_core_adendo/manifest.json',
              B/'bis/015/t01_e6_review_v2/RESULT.json',B/'bis/015/t01_statute_review/RESULT.json']
    verified=[];total_cpu=0
    for p in evidence:
        obj=json.loads(p.read_bytes());total_cpu+=obj['cpu_seconds']
        for entry in obj['outputs']:
            q=Path(entry['path']);assert sha(q)==entry['sha256'];verified.append(str(q))
    ledgerpath=OUT/'LEDGER_016.jsonl';rows=[json.loads(l) for l in ledgerpath.read_text('utf-8-sig').splitlines() if l.strip()]
    costs={}
    for row in rows:
        cost=next((row[k] for k in ('cost_estimate_usd','cost_usd','custo_usd') if row.get(k) is not None),None)
        key=next((row[k] for k in ('execution_task_id','execution_id','request_id','job_id') if row.get(k)),None)
        if cost is not None and key:costs[key]=Decimal(str(cost))
    total=sum(costs.values(),Decimal(0))
    first=json.loads(evidence[0].read_bytes())['at']
    elapsed=(now-datetime.fromisoformat(first)).total_seconds()/3600
    report=f'''[REAL / DERIVED — T01 executado localmente; NÃO-CEGO; comparação descritiva e custódia documental]

Abertura015SHA256: {sha(OUT/'ENTREGA_015_ABERTURA_operador.md')}
Abertura016SHA256: {sha(OUT/'ENTREGA_016_ABERTURA_operador.md')}

T01(a): anexo F0 com quatro grupos, dois incompletos e dois completos, hashes de START/PROGRESS/AUDIT_RATE/PRESTOP/CLOSED/snapshots; causa não observada. Nenhum desses produtos entra em veredito ou portão.
T01(b): centros e dominância separados por conjunto/estimador; C2 recolorido −0,002405633 ± 0,006326418, agrupado por251janelas originais. Errata de centros/E7 no túnel.
T01(c,d): dois conjuntos distintos de44, preservando 14elegíveis no registro. Ledger refeito, offset-zero PROIBIDA_COMO_TESTE: 14candidatos têm E[I]=134,967392; os44registrados, incluindo22reprovados,833,577641.
T01(e): PORTAO_DA_AMPLIACAO_V1_ERRATA_E06.md informa o estatuto herdado da camada v1; nenhuma campanha C5 refeita.
T01(f): NUISANCE relido por banda/covariável/população. c0 local não fornece separação calibrada. MEDIDA: a aproximação0,76 para R-MOD não se reproduz como abs(delta_GW250114)/SE(0,718549); diferença dos interceptos/SE=0,753559. A convenção exata do arredondamento da gerência permanece OPEN, sem substituir os dados.
T01(g): QUADRO_DE_ALCANCE_V1_v2.json/.md ao lado; taxas/IC das próprias fontes nas30células O4_HOJE;20ponteiros ausentes corrigidos;1576correções/σ disponíveis e964OPEN com motivo. Hashes e valores conferidos contra17fontes; três controles negativos passaram.
T01(h):13adendos de estatuto/proveniência; cinco revisões históricas sem hash agora vinculadas ao registro por errata datada; composição19reweighted/13pseob-rd/1v5PHM; ESS3093,851293>2128 rotulado nominal; comparação Kerr NÃO-CEGA. Parte A≈2,13h fora do ledger contínuo[DECLARADO na ordem]. Licença v3 não criada.

Revisão independente desta entrega continua pendente. A aprovação específica dos três payloads externos permanece pendente; não houve envio. Kimi C2.2 falhou terminalmente, sem resultado/uso informado, e não foi repetido. Nenhum gate, original científico ou registro congelado alterado.

Custo: {elapsed:.4f}h transcorridas desde o primeiro recibo T01 (inclui coordenação e intervalos; não CPU); CPU dos quatro recibos concluídos={total_cpu:.6f}s, sem somar a tentativa E6 falha cujo CPU não foi medido. Zero máquina pesada. Soma parcial de custos informados no ledger, deduplicada por execução/pedido: US${total}; assinaturas/falhas sem uso não equivalem a custo zero.

Próximo ramo: T02, runtime /opt/lal_env conferido(4621arquivos), probes leves iniciados em cópias; depois T13. C6 não reaberto.
'''
    path=OUT/'ENTREGA_015_T01_erratas.md';write(path,report.encode())
    result={'at':now.isoformat(),'status':'T01_LOCAL_DOCUMENTARY_DELIVERY_WITH_NAMED_OPEN_COMPARISON','evidence':[{'path':str(p),'sha256':sha(p)} for p in evidence],
            'verified_output_count':len(verified),'report_sha256':sha(path),'wall_elapsed_hours':elapsed,'completed_cpu_seconds':total_cpu,
            'heavy_machine_hours':0,'partial_metered_cost_usd':str(total),'metered_execution_or_request_count':len(costs),'independent_review_pending':True}
    put(D/'RESULT.json',result)
    append(OUT/'LEDGER_016.jsonl',json.dumps({'at':now.isoformat(),'event':'PARTB_T01_DOCUMENTARY_DELIVERY','receipt':str(D/'RESULT.json'),'new_external_calls':0,'partial_metered_cost_usd':str(total)},ensure_ascii=False)+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} — B/T01: EXECUTADO LOCAL; convenção R-MOD MEDIDA/OPEN; revisão independente pendente. Bancada transcorrida={elapsed:.4f}h; CPU concluída={total_cpu:.6f}s; máquina pesada=0h. Custos informados deduplicados=US${total}; desconhecidos preservados. PróximoT02.\n')
    p=R/'A7/CONTINUIDADE.json';state=json.loads(p.read_bytes())
    state.update(at=now.isoformat(),previous_goal_turn='PROGRESS',T01_delivery=str(D/'RESULT.json'),
       next='T02 DG14 live session12424, then DG02/frontD and T13; pending external approval remains',
       own_live_process={'session_id':12424,'scope':'T02 lightweight DG14 sequential','poll_only_no_restart':True},
       partial_metered_cost_usd=str(total))
    put(p,state,True)
    print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
