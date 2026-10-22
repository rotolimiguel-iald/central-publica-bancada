from pathlib import Path
import hashlib,importlib.util,json,sys
from fractions import Fraction
from datetime import datetime,timezone
B=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015')
REV=B/'mission_review_20261016';RES=B/'mission_resume_20261016'
REF=Path(r'C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json')
ACTOR={'id':'codex-mission-memory-review','kind':'agent'}
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def pin(p):
    p=Path(p);d=p.read_bytes();return {'path':str(p),'sha256':hashlib.sha256(d).hexdigest(),'bytes':len(d)}
def save(p,o):
    assert not p.exists(),f'Preserve prior artifact: {p}'
    d=(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode('utf-8');t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(d)
    assert t.stat().st_size==len(d);t.replace(p);return pin(p)
measured={};checks=[]
def walk(o):
    if isinstance(o,dict):
        if isinstance(o.get('path'),str) and isinstance(o.get('sha256'),str):
            if o['path'] not in measured:measured[o['path']]=pin(o['path'])
            a=measured[o['path']];assert a['sha256']==o['sha256'],(a,o)
            if 'bytes' in o:assert a['bytes']==o['bytes']
            checks.append(a)
        for v in o.values():walk(v)
    elif isinstance(o,list):
        for v in o:walk(v)
r5p=B/'global_net_inventory/R53/DEVICE_CONTINUUM_SOURCE_AUDIT_R1.json'
r4p=B/'physical_clock_reuse/R53/R53_PHYSICAL_CLOCK_SOURCE_AUDIT_R1.json'
r5=read(r5p);r4=read(r4p);walk(r5);walk(r4)
inventory=read(Path(r4['sources']['inventory']['path']));assert len(inventory['sources'])==21;walk(inventory['sources'])
startp=B/'R53_SOURCE_REVIEW_START.json';start=read(startp);walk(start)
assert r5['actor']['id']!=ACTOR['id'] and r4['actor']!=ACTOR['id']
assert not r5['requirement_satisfied'] and not r4['requirement_satisfied']
assert pin(r5p)['sha256'] in r5p.with_suffix('.txt').read_text(encoding='utf-8')
fr=read(Path(r5['sources']['finite_result']['path']));fre=read(Path(r5['sources']['finite_receipt']['path']))
assert fre['exit_code']==0 and fr['checks_passed']==fr['checks_total']==142
assert fr['quantum_dimensions']=={'Hilbert':8,'Liouville':64,'Choi':64,'factors':[2,2,2]}
for f in ['result','log','freeze']:assert fre[f+'_sha256']==r5['sources']['finite_'+f]['sha256']
assert fr['runner_sha256']==r5['sources']['finite_source']['sha256']
ip=RES/'LIVE_R53_DIAGNOSTIC_REVIEW_INITIAL_20261016T213810_413675Z_2234bec4_RECEIPT.json'
iq=read(ip)['result']['projection'];rq=read(Path(r4['mission']['return_receipt']))['result']['projection']
assert iq['revision']==rq['revision']==419
sys.path.insert(0,str(RES));s=importlib.util.spec_from_file_location('r53_joint_final',RES/'live_mission_r53.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m);assert Path(m.REFERENCE)==REF
r,fp=m.call('mission_cli.py',{'operation':'project','reference':str(REF),'actor':ACTOR,'max_chars':125000},'R53_JOINT_SOURCE_REVIEW_FINAL')
fq=r['projection'];assert fq['revision']>=420
def tasks(q):return {t['id']:t for t in q['active']+q['settled']}
assert tasks(iq)==tasks(rq)==tasks(fq),'Reconcile requirement changes before finalizing'
assert tasks(fq)['R4']['criterion']==r4['mission']['criterion']
assert tasks(fq)['R5']['criterion']==r5['criterion_unchanged']
for name in ['M0_MEMORIA','M1_HANDOFF_CAPACITY','M2_TERMINAL_PROJECTION','M3_TERMINAL_RECORDS','R7','R8']:
    assert tasks(fq)[name]['status']=='satisfied'
frequency=Fraction(300_000_000)/(2*Fraction(9,100))
reported_mhz=Fraction(1667,1000)*1_000_000
report={'schema':'iald-r53-independent-joint-source-review/v1','created_utc':datetime.now(timezone.utc).isoformat(),
 'reviewer':ACTOR,'unit':'F1.FECHO_20261015','handle':'r53-joint-source-review',
 'verdict':'PASS_DIAGNOSTIC_ONLY_R4_R5_REMAIN_OPEN','requirement_satisfied':False,
 'requirements':{'R4':{'criterion':tasks(fq)['R4']['criterion'],'satisfied':False},
                 'R5':{'criterion':tasks(fq)['R5']['criterion'],'satisfied':False}},
 'mission_reference':pin(REF),'initial_project':pin(ip),'R4_return_project':pin(Path(r4['mission']['return_receipt'])),
 'flow_registration':pin(startp),'final_project':pin(fp),'final_revision':fq['revision'],'state_sha256':fq['state_sha256'],
 'reconciliation':{'source_reports_revision':419,'flow_registration_revision':420,
   'all_requirement_records_identical_before_after':True,'accepted_requirements_preserved':[t['id'] for t in fq['settled']],
   'projection_changed_fields':[k for k in set(iq)|set(fq) if iq.get(k)!=fq.get(k)],
   'meaning':'A revisão419 dos relatórios foi reconciliada com a420: critérios, leases e registros completos dos requisitos permaneceram idênticos. Registro do acompanhamento/fluxo pela raiz está pinado; nenhuma transição feita pelo revisor.'},
 'reviewed_artifacts':[pin(r5p),pin(r5p.with_suffix('.txt')),pin(r4p),pin(Path(r4['companion_text']['path']))],
 'integrity':{'R5_source_entries':len(r5['sources']),'R4_source_entries':len(r4['sources']),
   'R4_original_inventory_entries':len(inventory['sources']),'pin_checks':len(checks),'unique_paths':len(measured),
   'mismatches':[],'pins':list(measured.values()),'R5_text_quotes_current_JSON_hash':True,
   'historical_finite_evidence':{'exit_code':0,'checks_passed':142,'checks_total':142,'Hilbert':8,'factors':[2,2,2],
     'source_result_log_freeze_match':True,'rerun':False}},
 'R5_findings':[
   {'result':'PASS_DIAGNOSTIC','anchors':['CONTRATO_REDE_R1.md:125–134','CONTRATO_REDE_R2.md:168–175','CONTRATO_REDE_R1.json:334–349'],
    'detail':'Família dirigida, inclusões coerentes, estados/limite e V entrelaçando ação completa/reflexão/localização são obrigações já escritas. As inclusões A→A tensor I do teste finito estão em um único tensor; não entregam refinamento contínuo.'},
   {'result':'PASS_SCOPE','anchors':['MQC_DESCRITIVO_EXTRACT_R1.txt:152–156,216–224','run_finite_device.py:157–182','RELATORIO_DEVICE_R1.md:2–13'],
    'detail':'27 sítios geométricos e três estados documentais por sítio não são o Hilbert8=2×2×2 da execução reduzida. O relatório distingue os objetos, não promove142 verificações sintéticas a realização de hardware e não deduz dimensão física finita de um número finito de sítios.'},
   {'result':'PASS_DERIVED_ARGUMENT','anchors':['TheImportedSecondQuantization.lean:133–134','ProductOrbitalSpectrum_v3.lean:83–105'],
    'detail':'Se x é reta própria comum para todos s e V é linear entrelaçador, B0(s)Vx=Vb(s)x=c(s)Vx; B0_no_eigen dá Vx=0. A injetividade exclui x não nulo. O corolário finito exige representação unitária abeliana: operadores normais comutantes admitem base própria comum em dimensão finita. Não é novo teorema compilado nem lei derivada para um dispositivo ainda não especificado.'},
   {'result':'PASS_LIMITS','anchors':['Santo.lean:205–218','CanonicalFockAssemblyR1.lean:61–63','PhysicalCanonicalNetCompleteR1.lean:207–224'],
    'detail':'A obstrução de translação espectral aditiva tem premissa diferente; não é identificada ao boost. O vácuo Fock fixo não é vetor de H1 e a dimensão infinita de Fock é argumento separado. D/rede global existem; o resíduo é a ponte do aparelho. Ausência é limitada às fontes declaradas, não universal.'}
 ],
 'R4_findings':[
   {'result':'PASS_DERIVED_ARGUMENT','anchors':['one_mqc.py:150–195'],
    'detail':'O modelo é explicitamente girante, H_eff=0. Com rho_rot=R rho_lab R*, derivação unitária dá H_rot=R H_lab R*+i hbar Rdot R*. Logo H_rot=0 implica H_lab=-i hbar R*Rdot, sem implicar H_lab=0. Estado, saltos e observáveis precisam do mesmo transporte.'},
   {'result':'PASS_DERIVED_SUPPORT','anchors':['one_mqc.py:182–195'],
    'detail':'Se q=gh/(gh+gd), w±=(1±q)/2, rho=w+ rhoT+w- A rhoT A e A²=I, então Lrho=[gh(1-q)-gd q](rhoT-A rhoT A)/2=0. Para0<beta<1 e gh,gd>0, ambos pesos são positivos e T,AT independentes; range=span{a|0>+b|Psi>,|1>} tem dimensão2. v=b|0>-a|Psi> está no núcleo. Não há fidelidade em B(C³); restrição ao suporte deve ser explícita e não equivale a eliminar Psi. Esta revisão é algébrica textual, não simulação nova.'},
   {'result':'PASS_DOCUMENTED_UNIT_CONFLICT','anchors':['MQC_DESCRITIVO_EXTRACT_R1.txt:175–184','PATENTE_SUPERCONDUTOR_HOLOGRAFICO_TGL_v2_BLINDAGEM.tex:506–517'],
    'detail':'O texto extraído pinado conserva9cm e1,667MHz. A regra f=c/(2L) da própria fonte fornece aproximadamente1,666667GHz. O Supercondutor escreve separadamente1.667,359MHz. Há conflito documental, não dado experimental nem autorização para corrigir a fonte/selecionar aparelho.',
    'exact_arithmetic':{'frequency_Hz_rational':str(frequency),'frequency_GHz':float(frequency/10**9),
      'ratio_to_1_667_MHz':float(frequency/reported_mhz),'interpretation':'vírgula decimal PT; fator aproximadamente1000'}},
   {'result':'PASS_TYPED_CLOCK_LIMITS','anchors':['TimeGravitonFlow.lean:171–203','physical_parameters.py:30–39,58–79','ContractCalibrationReuse.lean:18–51,95–99'],
    'detail':'Há relógio de coerência já construído; frequência2Omega não é Omega=V0/hbar. Eref controla a raiz positiva, comutador/Gibbs não fixam seu zero. A normalização kappa=1/rho(N) é fixa dadoN e N continua INPUT. As taxas típicas do protótipo, o setor OH desacoplado, o gap dissipativo e o referencial girante não fornecem a identificação SI do aparelho completo.'},
   {'result':'PASS_RESTRICTED_OBSTRUCTION','anchors':['DeviceRootObstructionR4.lean:21–62','CONTRATO_DISPOSITIVO_E_LEI_RAIZ_R7.txt:44–79'],
    'detail':'A recusa de D[J]=D[sqrt(H)] vale para a conjugação unital dos geradores isolados declarados; não exclui toda dilatação ou redução controlada. O contrato finito bomba→detector nomeia fonte/receptor, mas mantém preparação/calibração/domínios e resposta não nula como obrigações.'}
 ],
 'blocking_findings_against_reports':[],
 'scope':'Aprovada a fidelidade documental e a lógica dos diagnósticos no recorte informado. Não aprovada construção de R4/R5, não escolhidos dispositivo/estado/parâmetros e não afirmada ausência em todo o acervo.',
 'remaining':['R4: identificação física de estado, energia/zero, referencial, relógio SI, N e domínios do mesmo sistema.',
  'R5: setor do aparelho e representação/limite controlado com V completo e localização; rede física e R7/R8 já aceitos são reutilizados.'],
 'actions':{'new_builds':0,'provider_calls':0,'production_changes':False,'global_memory_changes':False,
  'mission_changes':False,'requirement_accepts':0,'gate_changes':False,'device_selected':False},'script':pin(Path(__file__))}
rp=save(REV/'R53_JOINT_SOURCE_REVIEW_R1.json',report)
print(json.dumps({'ok':True,'report':rp,'revision':fq['revision'],'pin_checks':len(checks),'unique_paths':len(measured),
 'all_requirements_unchanged':True,'verdict':report['verdict']},ensure_ascii=False))
