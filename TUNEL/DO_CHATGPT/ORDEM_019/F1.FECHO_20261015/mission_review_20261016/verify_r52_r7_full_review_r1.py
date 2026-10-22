from pathlib import Path
import hashlib, importlib.util, json, re
from datetime import datetime, timezone
B=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015')
REV=B/'mission_review_20261016'; TK=B/'takesaki_fock'
REF=Path(r'C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json')
ACTOR={'id':'codex-mission-memory-review','kind':'agent'}
def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def pin(p):
    p=Path(p); d=p.read_bytes()
    return {'path':str(p),'sha256':hashlib.sha256(d).hexdigest(),'bytes':len(d)}
def new(p,o):
    assert not p.exists(), f'Preserve existing report: {p}'
    data=(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode('utf-8');tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(data)
    assert tmp.stat().st_size==len(data);tmp.replace(p);return pin(p)
checked={}; measured={}
def walk(o):
    if isinstance(o,dict):
        if isinstance(o.get('path'),str) and isinstance(o.get('sha256'),str):
            k=(o['path'],o['sha256'])
            if k not in checked:
                if o['path'] not in measured:measured[o['path']]=pin(o['path'])
                a=measured[o['path']];assert a['sha256']==o['sha256'],(a,o)
                if 'bytes' in o:assert a['bytes']==o['bytes']
                checked[k]=a
        for v in o.values():walk(v)
    elif isinstance(o,list):
        for v in o:walk(v)
scope=read(REV/'R52_R7_SCOPE_REVIEW_R1.json');walk(scope)
components=[]
for name,attempt,manifest,count in [
    ('CanonicalFockNormalizedSplitR5','20261016T210351_533600Z','CANONICAL_FOCK_NORMALIZED_SPLIT_CANDIDATE_R5.json',3),
    ('CanonicalFockModularCoreInputR1','20261016T210640_174717Z','CANONICAL_FOCK_MODULAR_CORE_INPUT_CANDIDATE_R1.json',11),
]:
    source=TK/(name+'.lean');a=B/'orbital_rotation/attempts'/attempt
    receipt=read(a/'RECEIPT.json');meta=read(TK/manifest)
    assert receipt['exit_code']==0, (name,receipt['exit_code'])
    assert receipt['readonly_dependencies_unchanged'] and receipt['dependency_cache_unchanged']
    assert pin(source)['sha256']==receipt['source']['sha256']==meta['source']['sha256']
    assert meta['actor']!=ACTOR['id']
    walk(receipt);walk(meta);walk(read(a/'DEPENDENCY_CACHE.json'))
    text=source.read_text(encoding='utf-8-sig');axtext=(a/'AXIOMS.txt').read_text(encoding='utf-8-sig')
    ax=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",axtext)
    printed=re.findall(r'^#print axioms (.+)$',text,re.M)
    assert len(ax)==count==len(printed)
    for (n,v),p in zip(ax,printed):
        assert n==p or n.endswith('.'+p)
        assert {x.strip() for x in v.split(',')}=={'propext','Classical.choice','Quot.sound'}
    assert not re.search(r'\b(sorry|admit)\b',text)
    assert not re.search(r'^\s*(axiom|unsafe)\b',text,re.M)
    components.append({'name':name,'source':pin(source),'manifest':pin(TK/manifest),'receipt':pin(a/'RECEIPT.json'),
        'axioms':pin(a/'AXIOMS.txt'),'exit_code':0,'seconds':receipt['seconds'],'source_matches_attempt':True,
        'readonly_dependencies_unchanged_reported':True,'dependency_cache_unchanged_reported':True,
        'axiom_reports':[{'declaration':n,'axioms':[x.strip() for x in v.split(',')]} for n,v in ax]})
full_source=(TK/'CanonicalFockModularCoreInputR1.lean').read_text(encoding='utf-8-sig')
body=full_source.split('def modularCoreInput (D : CanonicalNetInput) : RemainingModularCoreInput D where',1)[1].split('#print axioms modularCoreInput',1)[0]
fields=re.findall(r'^  ([A-Za-z_]+) :=',body,re.M)
assert fields==read(TK/'CANONICAL_FOCK_MODULAR_CORE_INPUT_CANDIDATE_R1.json')['filled_fields']
assert len(fields)==21
vp=new(REV/'R52_R7_FULL_PIN_VERIFICATION_R1.json',{'schema':'iald-independent-pin-verification/v1','reviewer':ACTOR,
    'ok':True,'checked_unique_path_hash_pairs':len(checked),'pins':list(checked.values()),'components':components,
    'coverage':'Mapa de escopo pinado, dois recibos finais, manifestos e caches; bytes atuais. Sem recompilação.'})
spec=importlib.util.spec_from_file_location('r52_r7_final_project',B/'mission_resume_20261016/live_mission_r39.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);assert Path(m.REFERENCE)==REF
r,sp=m.call('mission_cli.py',{'operation':'project','reference':str(REF),'actor':ACTOR,'max_chars':100000},'R52_R7_FULL_REVIEW_FINAL')
q=r['projection'];task=next(t for t in q['active'] if t['id']=='R7')
assert task['criterion']==scope['criterion']
report={
    'schema':'iald-independent-requirement-review/v1','created_utc':datetime.now(timezone.utc).isoformat(),
    'reviewer':ACTOR,'requirement':'R7','verdict':'PASS_R7_CRITERION_WITH_EXPLICIT_SCOPE',
    'requirement_satisfied':True,'eligible_for_acceptance':True,'accept_performed':False,
    'mission_reference':pin(REF),'final_project':pin(sp),'revision':q['revision'],'state_sha256':q['state_sha256'],
    'criterion':task['criterion'],'lease_observed':task['lease'],'task_status_at_review':task['status'],
    'scope_review':pin(REV/'R52_R7_SCOPE_REVIEW_R1.json'),'pin_verification':vp,
    'components':components,'new_axiom_report_count':14,'filled_field_count':len(fields),'filled_fields':fields,
    'blocking_findings':[],
    'split_findings':[
        {'lines':[35,72],'finding':'Compressão a=vq no canto construído: a*a=q, r=aa* é projeção e qr=0. Prova genérica algébrica conserva o star e o carrier nativos.'},
        {'lines':[91,123],'finding':'Subprojeção finita é fornecida sob e existente; a lei quadrática W(a*a)=W(aa*) iguala os valores de q e r. As premissas genéricas são descarregadas por fornecedores concretos na linha209.'},
        {'lines':[125,185],'finding':'Aditividade positiva dá soma finita/positiva. A ação dual real em log(W(q+r).toReal) preserva projeções/ortogonalidade e normaliza W(q+r)=1; igualdade dos valores é preservada.'},
        {'lines':[203,232],'finding':'Três conclusões no mesmo PositiveInput/value, sem argumento final de canto, finitude, trace ou split. Todos os argumentos do helper são os termos já construídos.'}
    ],
    'assembly_findings':[
        {'lines':[51,73],'finding':'Escolha clássica extrai as duas projeções do único normalized_split_exists, conservando todas as propriedades conjuntas. PF não nulo segue de trace(PF)=1 e trace_zero.'},
        {'lines':[77,103],'finding':'Todos os 21 campos do contrato original preenchidos. Trace é cyclicTraceCandidate; PF/Pp/Pm vêm do mesmo par positivo. Aditividade do split usa value_add e compatibilidade positiva exata; nenhuma lei tracial, hreg, balance ou A é premissa final.'},
        {'lines':[107,118],'finding':'Igualdade do trace positivo com value e normalização PF=1 explicitadas; o value positivo é o inverseSupremum anterior, por mapa de escopo.'},
        {'lines':[121,146],'finding':'physicalModularCoreInput e physicalFockCertificate instanciam physicalCanonicalNet já construído; identidades de Core, trace, dualAction, embedding e rede demonstradas por rfl. A referência D da fábrica não permanece premissa na especialização física.'}
    ],
    'criterion_mapping':[
        {'clause':'Representação pretendida/produto cruzado','satisfied':True,'source':'CanonicalFockRegularCoreR2:22–99; PhysicalFockNetRealizationR2:18–89; fullA:121–146','explanation':'Core regular real do mesmo par Weyl/vácuo em L2(R; Fock), covariância modular, cunha KWR e embedding físico ligados por termos.'},
        {'clause':'Ação/peso/traço entrelaçados','satisfied':True,'source':'CanonicalFockDualWeightR3:27–108; CanonicalFockInverseSupremumR2:19–30; CanonicalFockActualPositiveTracePackageR2:89–125; fullA:107–114','explanation':'Peso dual, perturbação por cortes e traço positivo normal/semifinito/fiel são o mesmo encadeamento, com compatibilidade exata da extensão ENNReal no cone positivo.'},
        {'clause':'Escala V351 reutilizada','satisfied':True,'source':'GeneralRegularInverseCutoffR1:3–17,83; GeneralInverseCutoffWeightR3:82–104; GeneralInverseSupremumR3:71–79; CyclicTraceCompletionR3:105–132','explanation':'Escala exp(-s) do corte/peso/supremo/trace é derivada no fluxo Fock real; nenhuma equivalência SiteProfile↔Fock é inventada.'},
        {'clause':'Contrato modular concreto/PF','satisfied':True,'source':'SplitR5:203–232; fullA:77–146','explanation':'Split ortogonal finito de valores iguais e soma normalizada fornece o contrato completo de 21 campos e seu FockCertificate na rede física.'}
    ],
    'trace_scope':{
        'positive_value':'Traço positivo ENNReal, aditivo/homogêneo para escalares não negativos, fiel, normal e semifinito; lei quadrática e escala dual fornecidas.',
        'total_extension':'Função ENNReal cíclica/star-invariante/dual-escalada em todo RepresentedCore, exatamente value nos positivos.',
        'not_claimed':['Funcional complexo linear em todo o core','Aditividade total fora do cone positivo','Classificação do fator como tipo II∞','Equivalência do core Fock com SiteProfile']},
    'independence':{'new_sources_author':'codex-fock-r6-review','reviewer_is_distinct':True,
        'own_historical_dependencies':'Extensão R49 e cyclic R51 de autoria anterior do revisor são reutilizadas somente com pareceres independentes já pinados; esta rodada examina Split/fullA de autor distinto.'},
    'remaining_outside_R7':['R5 integral: grupo Poincaré pleno e identificação/realização do dispositivo conservam escopo próprio; D já existe.','R8: montagem Maxwell/carga/tensor na rede física exige sua evidência final própria; não é aceita por este parecer.','H3 universal/curvo e rito final da missão não decorrem deste aceite técnico de R7.'],
    'acceptance_instruction':'Recomendado aceite de R7 somente após submit da evidência pelo dono, nova projeção CAS e review_evidence deste artefato pelo revisor real. Este parecer não executa aceite nem fecha quadro/gate.',
    'new_builds':0,'provider_calls':0,'production_modified':False,'mission_mutations':False,
    'script':pin(Path(__file__))
}
rp=new(REV/'R52_R7_FULL_REVIEW_R1.json',report)
print(json.dumps({'ok':True,'revision':q['revision'],'report':rp,'verified_pin_pairs':len(checked),'axiom_reports':14,'fields':len(fields)},ensure_ascii=False))
