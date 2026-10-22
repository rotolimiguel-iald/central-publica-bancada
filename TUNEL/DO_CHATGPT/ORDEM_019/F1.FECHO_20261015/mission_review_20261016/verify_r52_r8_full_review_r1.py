from pathlib import Path
import hashlib, importlib.util, json, re
from datetime import datetime, timezone
B=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015')
REV=B/'mission_review_20261016'; MF=B/'maxwell_global'; RES=B/'mission_resume_20261016'
K=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt')
REF=Path(r'C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json')
ACTOR={'id':'codex-mission-memory-review','kind':'agent'}
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def pin(p):
    p=Path(p);d=p.read_bytes()
    return {'path':str(p),'sha256':hashlib.sha256(d).hexdigest(),'bytes':len(d)}
def new(p,o):
    assert not p.exists(),f'Preserve existing file: {p}'
    data=(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode('utf-8');tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(data)
    assert tmp.stat().st_size==len(data);tmp.replace(p);return pin(p)
checked={};measured={}
def walk(o):
    if isinstance(o,dict):
        if isinstance(o.get('path'),str) and isinstance(o.get('sha256'),str):
            key=(o['path'],o['sha256'])
            if o['path'] not in measured:measured[o['path']]=pin(o['path'])
            a=measured[o['path']];assert a['sha256']==o['sha256'],(a,o)
            if 'bytes' in o:assert a['bytes']==o['bytes'],(a,o)
            checked[key]=a
        for v in o.values():walk(v)
    elif isinstance(o,list):
        for v in o:walk(v)
manifest=MF/'PHYSICAL_MAXWELL_JOINT_CANDIDATES_R52_R2.json'
meta=read(manifest);walk(meta);assert meta['author']['id']!=ACTOR['id']
delivery=B/'R8_DELIVERY_R52.json';deliv=read(delivery);walk(deliv)
prior_names=['R48_NONZERO_CERTIFICATE_INDEPENDENT_REVIEW_R1.json','R50_FIELD_CORNER_REVIEW_R2.json',
 'R51_POINT_WICK_REVIEW_R2.json','R51_SMEARING_REVIEW_R1.json','R52_R7_FULL_REVIEW_R1.json','R52_R7_ACCEPT_RECEIPT_R1.json']
for name in prior_names:walk(read(REV/name))
components=[]
for name,stamp,count in [('CircularMaxwellCertificateR2','20261016T211151_421554Z',10),
                        ('PhysicalMaxwellJointRealizationR2','20261016T211651_298033Z',16)]:
    a=B/'orbital_rotation/attempts'/stamp;source=MF/(name+'.lean');r=read(a/'RECEIPT.json')
    assert r['exit_code']==0 and r['readonly_dependencies_unchanged'] and r['dependency_cache_unchanged']
    assert r['production_modified'] is False
    assert pin(source)['sha256']==r['source']['sha256']==pin(a/source.name)['sha256']
    walk(r);walk(read(a/'DEPENDENCY_CACHE.json'))
    src=source.read_text(encoding='utf-8-sig');axtext=(a/'AXIOMS.txt').read_text(encoding='utf-8-sig')
    ax=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",axtext)
    printed=re.findall(r'^#print axioms (.+)$',src,re.M)
    assert len(ax)==len(printed)==count
    for (n,v),p in zip(ax,printed):
        assert n==p or n.endswith('.'+p)
        assert {x.strip() for x in v.split(',')}=={'propext','Classical.choice','Quot.sound'}
    assert not re.search(r'\b(sorry|admit)\b',src)
    assert not re.search(r'^\s*(axiom|unsafe)\b',src,re.M)
    assert 'error:' not in axtext and 'sorryAx' not in axtext
    components.append({'module':name,'source':pin(source),'receipt':pin(a/'RECEIPT.json'),
      'axioms':pin(a/'AXIOMS.txt'),'attempt_source':pin(a/source.name),'exit_code':0,
      'seconds':r['seconds'],'source_matches_attempt':True,'readonly_dependencies_unchanged':True,
      'dependency_cache_unchanged':True,'axiom_reports':[{'declaration':n,'axioms':[x.strip() for x in v.split(',')]} for n,v in ax]})
vp=new(REV/'R52_R8_FULL_PIN_VERIFICATION_R1.json',{'schema':'iald-independent-pin-verification/v1',
 'reviewer':ACTOR,'ok':True,'checked_unique_path_hash_pairs':len(checked),'measured_unique_files':len(measured),
 'pins':list(checked.values()),'components':components,
 'coverage':'Entrega submetida, manifesto, dois recibos finais, caches e pareceres anteriores citados; bytes atuais. Sem recompilação.'})
spec=importlib.util.spec_from_file_location('r52_r8_final_review',RES/'live_mission_r39.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);assert Path(m.REFERENCE)==REF
r,sp=m.call('mission_cli.py',{'operation':'project','reference':str(REF),'actor':ACTOR,'max_chars':100000},'R52_R8_FULL_REVIEW_FINAL')
q=r['projection'];task=next(t for t in q['active'] if t['id']=='R8');walk(task['evidence'])
assert task['criterion']==deliv['criterion']==meta['criterion']
assert task['status']=='review_pending' and task['submitted_by']!=ACTOR['id']
assert any(t['id']=='R7' and t['status']=='satisfied' for t in q['settled'])
def anchor(p,lo,hi):return {'path':str(p),'lines':[lo,hi]}
c=MF/'CircularMaxwellCertificateR2.lean';j=MF/'PhysicalMaxwellJointRealizationR2.lean';f=MF/'CircularPhysicalFieldTransportR1.lean'
report={'schema':'iald-independent-requirement-review/v1','created_utc':datetime.now(timezone.utc).isoformat(),
 'reviewer':ACTOR,'requirement':'R8','verdict':'PASS_R8_CRITERION_WITH_EXPLICIT_SCOPE',
 'requirement_satisfied':True,'eligible_for_acceptance':True,'accept_performed':False,
 'statute':'REAL: leitura de fontes e verificação de bytes/recibos; validade formal no escopo dos enunciados. Nenhuma confirmação empírica.',
 'mission_reference':pin(REF),'final_project':pin(sp),'revision':q['revision'],'state_sha256':q['state_sha256'],
 'criterion':task['criterion'],'status_at_review':task['status'],'submitted_by':task['submitted_by'],
 'delivery':pin(delivery),'manifest':pin(manifest),'pin_verification':vp,'components':components,'new_axiom_report_count':26,
 'blocking_findings':[],
 'criterion_mapping':[
  {'clause':'Campos do certificado completo na representação/rede pretendida','satisfied':True,
   'anchors':[anchor(j,30,63),anchor(c,108,120)],
   'finding':'physicalMaxwellCertificate instancia o MaxwellCertificate original com physicalFockCertificate e physicalCanonicalNet concretos. Rede por igualdade, domínio AxisCompact denso, vácuo e translações; smearing circular normalizado permanece no subespaço local real e seu Weyl pertence à mesma rede. D/A não permanecem premissas na especialização física.'},
  {'clause':'Campos e estado não triviais','satisfied':True,
   'anchors':[anchor(f,166,180),anchor(c,92,105),anchor(j,108,120)],
   'finding':'O campo circular normalizado já possui teste real com ação não nula no vácuo. A testemunha do certificado é puxada pelo unitário inverso, preservando Regular e k não nulo. Um único ψ do domínio regular reúne norma1, AxisCompact, energia modular não nula, carga efetiva e identidade do tensor Wick; não se combinam testemunhas distintas.'},
  {'clause':'Ligação do campo da rede à forma Wick/tensor no mesmo estado','satisfied':True,
   'anchors':[anchor(f,145,164),anchor(c,123,149),anchor(j,66,74)],
   'finding':'Γ(circularH1) transporta explicitamente o estado e ambos os argumentos da forma. O Bochner por estado coincide com o aniquilador circular efetivo após esse mesmo transporte. A forma Wick local anterior, definida independentemente do certificado, coincide com T circular no vetor original ψ. Não se postula invariância do tensor antigo mantendo ψ fixo.'},
  {'clause':'Simetria/conservação e covariância do tensor','satisfied':True,
   'anchors':[anchor(c,25,46),anchor(j,76,104)],
   'finding':'Simetria, integrabilidade contra testes e conservação distribucional são transportadas do tensor global calibrado. Translações e boost usam comutação demonstrada de Γ(circularH1) com Γ(U1) e Γ(B0), sem trocar geradores ou acrescentar hipótese de conservação.'},
  {'clause':'Regular completo e carga no mesmo objeto','satisfied':True,
   'anchors':[anchor(c,48,89),anchor(K/'TheImportedSecondQuantization.lean',498,516)],
   'finding':'São preservadas as seis conjunções do Regular canônico, incluindo momento no plano, continuidade e ambas as caudas. A igualdade da função de correlação modular transporta HasModularEnergy com sinal -i k inalterado; charge_link é consumido do certificado previamente construído, não introduzido como premissa final.'},
  {'clause':'Fonte geométrica ligada','satisfied':True,
   'anchors':[anchor(j,123,147),anchor(K/'TheImportedSecondQuantization.lean',545,582),
              anchor(K/'O16/NullSolutionConsumerReuse.lean',18,58),anchor(K/'O16/TeleologicalNullSolution_v2.lean',23,48)],
   'finding':'physicalMaxwellH3/Import usa exatamente net, realização, boost, tensor e Regular da montagem. A equação de derivada theta ao longo de nullDir tem fonte -8πG vezes a contração nn do mesmo circularWickTensor no mesmo ψ. O construtor usa continuidade/caudas já fornecidas para a resposta de tela linearizada; não pressupõe a equação final como novo campo.'}
 ],
 'normalization':{'field_amplitude':'raiz positiva de ((2π)^3)^(-1), fixa pela convenção Fourier',
  'stress_scale':'((2π)^3)^(-1), já revisada, sem ajuste ao estado/carga e sem rescalar o gerador',
  'same_H1':'H1 orbital com medida d3p/E; circularH1 é isometria no mesmo H1 e Γ no mesmo Fock'},
 'explicit_inputs':['KillingNormalization N','G real e prova 0<G para H3'],
 'limits':['Maxwell livre no Fock/rede concretos de Minkowski; nenhuma interação nova ou dispositivo realizado.',
  'H3 é a resposta geométrica nula fixa/linearizada do contrato existente; não demonstra Einstein não linear para geometria arbitrária.',
  'Campo pontual é usado no domínio regular e em Bochner por estado; não é operador pontual global limitado nem integral em norma de operadores.',
  'N permanece explícito; seleção física do relógio/espectro e pendências R4/R5 não são satisfeitas por este parecer.',
  'O traço do core aceito em R7 é ENNReal com alcance declarado, sem nova afirmação de linearidade complexa total ou tipoII.',
  'Aceite de R8 na missão não fecha o quadro, rito integral, gate nem confirma física pela natureza.'],
 'prior_reviews_reused':[pin(REV/n) for n in prior_names],
 'independence':{'new_sources_author':meta['author'],'reviewer_is_distinct':True,
  'historical_authorship':'O revisor escreveu fornecedores históricos Regular/domínio/assembly. Eles são reutilizados com revisões independentes anteriores; as duas novas fontes da presente montagem são de autor distinto. Não se declara auditoria própria independente desses fornecedores.'},
 'acceptance_instruction':'A entrega já foi submetida por ator distinto. Aceite recomendado com nova projeção CAS e review_evidence deste parecer; ato separado e recibo próprio.',
 'new_builds':0,'provider_calls':0,'production_modified':False,'mission_mutations':False,'script':pin(Path(__file__))}
rp=new(REV/'R52_R8_FULL_REVIEW_R1.json',report)
print(json.dumps({'ok':True,'revision':q['revision'],'report':rp,'verified_pin_pairs':len(checked),'axiom_reports':26},ensure_ascii=False))
