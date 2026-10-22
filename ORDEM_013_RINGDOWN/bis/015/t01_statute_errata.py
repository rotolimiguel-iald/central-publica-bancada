"""Write T01(h) corrections alongside the cited documents, never into them."""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import json, hashlib, time, uuid

B=Path(__file__).resolve().parents[2];ROOT=B.parent;OUT=ROOT/'TUNEL/DO_CHATGPT'
D=B/'bis/015/t01_statute_review';sources={};outputs=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p):
    h=sha(p);sources[str(p)]=h
    return f'{p.as_posix()} — SHA256={h}'
def load(p):pin(p);return json.loads(p.read_bytes())
def emit(p,text):
    assert not p.exists(),p
    raw=text.encode() if isinstance(text,str) else (json.dumps(text,ensure_ascii=False,indent=2)+'\n').encode()
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    with t.open('xb') as f:f.write(raw)
    assert t.read_bytes()==raw;t.rename(p);outputs.append({'path':str(p),'sha256':sha(p)})
def main():
    start=time.perf_counter();cpu=time.process_time();D.mkdir(exist_ok=False)
    op15=sha(OUT/'ENTREGA_015_ABERTURA_operador.md');op16=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    header=f'[REAL — errata documental; NÃO-CEGO; não altera autorização, resultado ou gate]\n\nAbertura015SHA256: {op15}\nAbertura016SHA256: {op16}\n\n'
    entries=[]
    targets=[('ENTREGA_013BIS_B1_portao_e_nuisance.md','[REAL / DERIVED — NÃO-CEGO; portão e nuisance condicionais; calibração física e seleção não pagas]'),
      ('ENTREGA_013BIS_B2_registro_e_440.md','[REAL / DERIVED — NÃO-CEGO; registro, nulos sintéticos e diagnósticos condicionais; calibração e significância físicas não pagas]'),
      ('ENTREGA_013BIS_E2_REGISTRO_V1.md','[REAL — NÃO-CEGO; testemunho documental do registro V1; não constitui nova ativação]'),
      ('ENTREGA_013BIS_B3_piloto_e_orcamento.md','[REAL — NÃO-CEGO; comparação Kerr descritiva do mesmo evento; posterior IMR e calibração física não pagos]')]
    for name,line in targets:
        p=OUT/name;anchor=pin(p);old=p.read_text('utf-8-sig').splitlines()[0]
        dest=p.with_name(p.stem+'_ERRATA_1ALINHA.md')
        emit(dest,header+f'Predecessor: {anchor}\n\nPrimeira linha preservada na origem: {old}\n\nLeitura corrigida: **{line}**\n\nCorreção do estatuto e do escopo; nenhum byte do predecessor foi alterado.\n')
        entries.append(str(dest))
    predecessors={'C2_ADENDO_OBSERVAVEL_v2.md':'C2_ADENDO_OBSERVAVEL.md',
       'REAPROVEITAMENTO_C2_v2.md':'REAPROVEITAMENTO_C2.md',
       'REAPROVEITAMENTO_C1_v2.md':'REAPROVEITAMENTO_C1.md',
       'REAPROVEITAMENTO_C1_v3.md':'REAPROVEITAMENTO_C1_v2.md'}
    for name,prior in predecessors.items():
        p=B/name;anchor=pin(p);pr=pin(B/prior)
        dest=p.with_name(p.stem+'_ERRATA_1ALINHA.md')
        emit(dest,header+f'Documento corrigido ao lado: {anchor}\nPredecessor histórico da versão: {pr}\n\n[REAL / DERIVED — NÃO-CEGO; controles condicionais; realização física e escolha de leitura não demonstradas por esta ficha.]\n\nA primeira linha deve ser lida com este escopo e com o hash do predecessor histórico acima; a fonte original permanece íntegra.\n')
        entries.append(str(dest))
    reg=B/'RINGDOWN_5SIGMA_V1.json';regpin=pin(reg);digest=sha(reg)
    reviews=['bis/e6_review/FINAL_DRAFT_INDEPENDENT_REVIEW_V5.json','bis/e3_pyring_review/KERR_INDEPENDENT_REVIEW.md',
      'bis/e3_pyring_review/MANIFEST_V3_INDEPENDENT_REVIEW.md','bis/e2_publication_census/E7_INDEPENDENT_REVIEW_V4.md',
      'bis/e6_review/E3_WALL_HELPER_INDEPENDENT_REVIEW_V1.md']
    reviewchecks=[]
    for name in reviews:
        p=B/name;anchor=pin(p);had=digest in p.read_text('utf-8-sig')
        reviewchecks.append({'path':str(p),'had_registration_hash':had})
        dest=p.with_name(p.stem+'_ERRATA_REGISTRO_015.md')
        emit(dest,header+f'Revisão histórica: {anchor}\nRegistro de referência: {regpin}\nregistro_sha256: {digest}\n\nEste vínculo foi conferido na presente errata, não retroativamente pelo revisor histórico. Não equivale a revisão independente nova, ratificação, liberação de relógio ou autorização de dados cegos. Hash presente no predecessor: {had}.\n')
        entries.append(str(dest))
    planpath=B/'bis/e7_prepare/EXTRACTION_PLAN.json';plan=load(planpath)
    composition=Counter(e['dataset'].split('/')[0] for e in plan['events'])
    assert sum(composition.values())==33,composition
    comparisonpath=B/'cache/E3_KERR220_CALIBRATION_V2/public_psd/COMPARISON.json';comparison=load(comparisonpath)
    samples=comparison['samples'];ess=comparison['convergence']['ess']
    assert samples==2128 and ess>samples
    oldreport=OUT/'ENTREGA_013BIS_RELATORIO_FINAL.md';rp=pin(oldreport)
    extra=header+f'Predecessor: {rp}\n\nErrata de RELATORIO:57: o controle Kerr do evento conhecido é **NÃO-CEGO**; comparação descritiva do mesmo evento, sem z calibrado, Bayes factor ou evidência independente adicional.\n\n'
    extra+=f'Kerr V2: {samples} amostras; ESS={ess:.8f}. Descrição: **rejection sampling, ESS nominal**. O ESS nominal do sampler não é contagem de amostras posteriores independentes. Fonte: {pin(comparisonpath)}.\n\n'
    extra+=f'[REAL — plano em disco] Composição dos33produtos: {dict(composition)}. Fonte: {pin(planpath)}. Nenhum produto de teste foi acrescentado por esta nota.\n\n'
    extra+='[DECLARADO — ORDEM015/T01(h)] Parte A (≈2,13h) fora do ledger contínuo da Parte B. Nenhuma soma nova às35,017h remanescentes, nem alteração do relógio antigo ou abertura do R7.\n\nLicença v3 não criada; a correção exigida é documental, não uma campanha nova de licenças.\n'
    emit(OUT/'ENTREGA_015_ERRATA_ESTATUTOS.md',extra+'\nAdendos produzidos:\n'+''.join(f'- {p}\n' for p in entries))
    result={'at':datetime.now(timezone.utc).isoformat(),'status':'T01H_DOCUMENTED_LOCAL_ONLY_INDEPENDENT_AUDIT_PENDING','reviews':reviewchecks,
      'product_composition':dict(composition),'Kerr_samples':samples,'Kerr_ESS_nominal':ess,'sources':sources,'outputs':outputs,
      'wall_seconds':time.perf_counter()-start,'cpu_seconds':time.process_time()-cpu,'heavy_machine_hours':0,'opening015_sha256':op15,'opening016_sha256':op16,
      'originals_changed':False,'gate_changed':False,'blind_data_accessed':False}
    emit(D/'RESULT.json',result)
    print(json.dumps({'status':result['status'],'composition':dict(composition),'adendos':len(entries),'reviews':reviewchecks,'wall_seconds':result['wall_seconds']},ensure_ascii=False))
if __name__=='__main__':main()
