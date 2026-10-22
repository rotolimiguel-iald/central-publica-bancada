"""Complete documentary omissions with typed diagnostics, not a calibrated test."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, math, time, uuid

B=Path(__file__).resolve().parents[2]
CHAT=B.parent;OUT=CHAT/'TUNEL/DO_CHATGPT';D=B/'bis/015/t01_core_adendo'
sources={}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):
    sources[str(p)]=sha(p)
    return json.loads(p.read_bytes())
def emit(p,value):
    assert not p.exists(),p
    raw=(value if isinstance(value,str) else json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
    temp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    with temp.open('xb') as f:f.write(raw)
    assert temp.read_bytes()==raw
    temp.rename(p)
def pin(p):
    sources[str(p)]=sha(p)
    return {'path':str(p),'sha256':sha(p)}
def main():
    start=time.perf_counter();cpu=time.process_time();D.mkdir(exist_ok=False)
    previous=B/'bis/015/t01_core/manifest.json';manifest=load(previous)
    checked=[]
    for name,digest in manifest['sources'].items():
        p=Path(name);assert sha(p)==digest,('source changed',name);checked.append(name)
    for item in manifest['outputs']:
        p=Path(item['path']);assert sha(p)==item['sha256'],('output changed',p);checked.append(str(p))
    assert sha(B/'C5_ANEXO_PROCESSOS.json')==manifest['F0_annex_sha256']
    op15=sha(OUT/'ENTREGA_015_ABERTURA_operador.md');op16=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    header=f'[REAL / DERIVED — NÃO-CEGO; diagnóstico documental, INCONCLUSIVE_SYSTEMATICS]\n\nAbertura015SHA256: {op15}\nAbertura016SHA256: {op16}\n\n'
    c2path=B/'bis/C2_TRAJECTORY_expanded_1000.json';c2=load(c2path)
    ri,row=next((i,r) for i,r in enumerate(c2['rows']) if r['reading']=='R-A')
    r=row['recolored'];keys=['N','mean_dtau','mean_dtau_standard_error','uncertainty_method','distinct_noise_windows','boundary_count','optimizer_failures']
    control={k:r[k] for k in keys}
    control['source_pointer']=f'/rows/{ri}/recolored'
    assert control['N']==1000 and control['distinct_noise_windows']==251
    npath=B/'NUISANCE_V1.json';n=load(npath)['conditional_diagnostics']
    info=load(B/'bis/015/t01_core/information_ledger.json')
    refs=info['reference_effects']
    fits=n['fits'];key=lambda r:(r['group'],r['covariate'],r['bandwidth_factor'])
    gr={key(r):r['result'] for r in fits if r['reading']=='GR'}
    rows=[]
    wanted=['R-B','R-MOD','R-RAIZ-0','R-LIN']
    for i,r in enumerate(fits):
        if r['group'] not in ('GWTC5_31','GWTC5_33') or r['reading'] not in wanted:continue
        v=r['result'];g=gr[key(r)];se=v['stderr'][0]
        assert se>0 and math.isclose(v['c0']/se,v['c0_local_wald_to_zero'],abs_tol=1e-12)
        rows.append({'reading':r['reading'],'group':r['group'],'covariate':r['covariate'],'bandwidth_factor':r['bandwidth_factor'],
          'c0':v['c0'],'SE_local':se,'own_prediction_distance_abs':abs(v['c0']/se),
          'reference_delta_GW250114':refs[r['reading']],
          'reference_over_local_SE':abs(refs[r['reading']])/se,
          'fitted_c0_difference_over_local_SE':abs(v['c0']-g['c0'])/se,
          'zero_in_local_95_interval':v['c0_local_interval_95'][0]<=0<=v['c0_local_interval_95'][1],
          'pointer':f'/conditional_diagnostics/fits/{i}/result','z_calibrated':None})
    nominal=[r for r in rows if key(r)==('GWTC5_31','sigma',1.0)]
    assert len(nominal)==4 and all(r['zero_in_local_95_interval'] for r in nominal)
    expected={'R-B':.40,'R-MOD':.76,'R-RAIZ-0':.75,'R-LIN':1.45}
    diagnostic={'status':'DESCRIPTIVE_NOT_CALIBRATED','C2_control':control,'rows':rows,
        'management_approximate_distance':expected,
        'reference_comparison':'abs(delta_GW250114)/SE_reading; explicit reference convention, not a uniform effect across all events',
        'fitted_comparison':'abs(c0_reading-c0_GR)/SE_reading; descriptive fitted-intercept change, not variance of their difference',
        'unresolved':'The exact delta reduction and SE convention for the management rounded distance is not uniquely identified in NUISANCE_V1. No calibrated separation field exists. In particular R-MOD .76 is not reproduced by the GW250114 reference (.718549).',
        'supersedes_scope_claim':pin(B/'bis/015/t01_core/RELATORIO_PARCIAL.md')}
    emit(D/'diagnostics.json',diagnostic)
    report=header+'Adendo ao relatório parcial: a afirmação anterior «T01(a-f) executados» não cobria todas as cláusulas documentais. Esta entrega acrescenta os campos omitidos; g/h continuam pendentes.\n\n'
    report+=f'Controle C2 R-A recolorido: {r if False else control["mean_dtau"]:.10f} ± {control["mean_dtau_standard_error"]:.10f}. N={control["N"]}; {control["distinct_noise_windows"]} janelas originais distintas. SE agrupado por janela off-source, não 1000 janelas independentes. Este controle não gera o centro +0,07 dos catálogos; não é prova geral de ausência de viés.\n\n'
    report+='Distâncias locais com c(σ)=c0+kσ livre, GWTC5_31, banda 1.0. Nenhuma coluna é um teste calibrado.\n\n| Leitura | própria predição: abs(c0)/SE | gerência: aproximação | referência GW250114/SE | diferença dos c0/SE |\n|---|---:|---:|---:|---:|\n'
    for r in nominal:report+=f'|{r["reading"]}|{r["own_prediction_distance_abs"]:.6f}|{expected[r["reading"]]:.2f}|{r["reference_over_local_SE"]:.6f}|{r["fitted_c0_difference_over_local_SE"]:.6f}|\n'
    report+='\n[OPEN] A redução exata de δ_X e o denominador empregados nas aproximações da gerência não estão identificados univocamente no JSON. A referência GW250114 reproduz a escala, mas dá R-MOD 0,718549, não 0,76. Não substituí o número para forçar concordância. A diferença de interceptos usa ajustes com k também livre e não é o mesmo diagnóstico; sua incerteza conjunta não foi calculada.\n'
    report+='\n[REAL] Todos os quatro intervalos locais nominais de c0 incluem zero. Os dados não fornecem uma separação calibrada entre leitura e RG com c0 livre; z_calibrated continua null. Bandas0,7/1,4, 1/SNR e grupo33 estão em diagnostics.json.\n'
    report+=f'\nPredecessor: {diagnostic["supersedes_scope_claim"]}.\n'
    emit(D/'RELATORIO_ADENDO.md',report)
    emit(OUT/'ENTREGA_015_T01_a_f_adendo.md',report)
    port=B/'PORTAO_DA_AMPLIACAO_V1.md';pr=pin(port);system=B/'bis/e0_core/SYSTEMATICS_ADENDO.json';sy=pin(system)
    emit(B/'PORTAO_DA_AMPLIACAO_V1_ERRATA_E06.md',header+f'Supersedes (somente escopo E0.6): {pr}\n\n[DECLARADO] A camada v1 de E0_CORE.json conserva magnitudes-proxy históricas do insumo da gerência, superadas pelo SYSTEMATICS_ADENDO.json ({sy["sha256"]}). Esta nota não transfere essas magnitudes à tabela do portão nem altera seus números. Não foi refeita a campanha C5.\n')
    census=B/'bis/e1_selection/CALIBRATION_AND_CANDIDATE_CENSUS.md';ce=pin(census)
    emit(OUT/'ENTREGA_015_ERRATA_CENTROS_E7.md',header+f'Correção ao lado de RELATORIO_FINAL (centros e linha E7): fonte detalhada e estatutos em {D/"RELATORIO_ADENDO.md"}.\n\n'+(B/'bis/015/t01_core/RELATORIO_PARCIAL.md').read_text('utf-8').split('T01(a-f) executados;',1)[1].split('E7:')[0].split('\n\n',1)[1]+f'\nControle recolorido C2: {control["mean_dtau"]:.10f} ± {control["mean_dtau_standard_error"]:.10f}; INCONCLUSIVE_SYSTEMATICS.\n\nCenso canônico: [{census.name}]({census.as_posix()}); SHA256={ce["sha256"]}. Os dois conjuntos de44 são distintos, como registrado no relatório parcial.\n')
    result={'at':datetime.now(timezone.utc).isoformat(),'status':'T01_A_F_DOCUMENTED_WITH_OPEN_DISTANCE_CONVENTION','checked_existing_entries':len(checked),
            'sources':sources,'outputs':[{'path':str(p),'sha256':sha(p)} for p in sorted(D.iterdir())],
            'wall_seconds':time.perf_counter()-start,'cpu_seconds':time.process_time()-cpu,'heavy_machine_hours':0,
            'gate_changed':False,'C6_reopened':False,'opening016_sha256':op16,'opening015_sha256':op15}
    emit(D/'manifest.json',result)
    print(json.dumps({'status':result['status'],'checked_existing_entries':len(checked),'C2_control':control,'nominal':nominal,'wall_seconds':result['wall_seconds']},ensure_ascii=False))
if __name__=='__main__':main()
