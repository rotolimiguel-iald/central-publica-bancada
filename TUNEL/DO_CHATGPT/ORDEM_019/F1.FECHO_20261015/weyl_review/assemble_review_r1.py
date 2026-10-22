from pathlib import Path
import datetime, hashlib, json, re

B=Path(__file__).resolve().parent
P=B.parent
def pin(p):
    p=Path(p);r=p.read_bytes()
    return {'path':str(p),'sha256':hashlib.sha256(r).hexdigest(),'bytes':len(r)}
def put(p,s):
    r=s.encode('utf-8')
    with p.open('xb') as f:f.write(r)
    assert p.read_bytes()==r
def axioms(text):
    out={}
    for line in text.splitlines():
        if line.startswith('LOCAL_DECL\t'):
            _,n,a=line.split('\t');out[n]=[s for s in a.split(',') if s]
    for n,a in re.findall(r"'(.+?)' depends on axioms: \[([^]]*)\]",text):
        out[n]=[s.strip() for s in a.split(',') if s.strip()]
    for n in re.findall(r"'(.+?)' does not depend on any axioms",text):out[n]=[]
    return {k:sorted(v) for k,v in out.items()}

builds={};binary=[];anchors=[]
for name,count in [('coefficients',19),('operators',18),('covariance',2),('concrete',27)]:
    rp=B/name/'RECEIPT_R1.json';r=json.loads(rp.read_text(encoding='utf-8'))
    assert r['passed'] and r['exit_code']==0 and r['axiom_count']==count
    assert all(set(a)<={'propext','Classical.choice','Quot.sound'} for a in r['axioms'].values())
    for item in r['dependencies_before_after']:assert pin(item['path'])['sha256']==item['sha256']
    assert pin(r['source']['path'])==r['source']
    original=json.loads(Path(r['original_receipt']['path']).read_text(encoding='utf-8'))
    origax=next(x for x in original['artifacts'] if x['path'].endswith('AXIOMS.txt'))
    assert pin(origax['path'])==origax
    original_axioms=axioms(Path(origax['path']).read_text(encoding='utf-8'))
    assert original_axioms=={k:sorted(v) for k,v in r['axioms'].items()}
    builds[name]={'receipt':pin(rp),**{k:r[k] for k in ['start_utc','end_utc','seconds','exit_code','source','axiom_count','olean','olean_identical_to_accepted','log']},'same_declarations_and_axiom_sets_as_builder':True}
    origbin=next(x for x in original['artifacts'] if x['path'].endswith('.olean'))
    strings={}
    for label,record in [('original',origbin),('independent',r['olean'])]:
        assert pin(record['path'])==record
        raw=Path(record['path']).read_bytes()
        strings[label]=[s.decode('utf-8','replace') for s in re.findall(rb'[ -~]{16,}',raw) if b'C:' in s and b'.lean' in s]
    binary.append({'module':name,'original':origbin,'independent':r['olean'],'identical':r['olean_identical_to_accepted'],'serialized_source_paths':strings})
    for n,line in enumerate(Path(r['source']['path']).read_text(encoding='utf-8').splitlines(),1):
        if re.match(r'(?:def|theorem) ',line):anchors.append({'source':r['source']['path'],'line':n,'declaration':line})

checks=[
    {'id':'cocycle','verdict':'PASSA','statute':'REAL','finding':'A convenção D(f)e(g)=exp(-<f,f>/2-<f,g>)e(g+f) preserva Gram com o produto interno antilinear à esquerda. A composição deriva D(f)D(g)=exp(-i Im<f,g>)D(f+g). Não há um fator 1/2 omitido: o parâmetro simplético desta convenção é 2 Im<f,g>.'},
    {'id':'extension','verdict':'PASSA','statute':'REAL','finding':'O módulo genérico assume apenas a família exponencial, seu kernel e totalidade. A imagem deslocada é total por translação sobrejetiva e amplitude não nula. GramTotalExtension constrói a isometria/equivalência; nenhum Weyl, CCR, inverso ou covariância é um campo assumido. A revisão independente do Gram é do root, pinada abaixo.'},
    {'id':'star_locality','verdict':'PASSA','statute':'REAL','finding':'W(-f)W(f)=1 deriva do cociclo; a equivalência unitária identifica o inverso com adjunto, produzindo W(f)*=W(-f). Localidade usa Im<f,g>=0 nas duas ordens, com conjugação explícita.'},
    {'id':'covariance','verdict':'PASSA','statute':'REAL','finding':'A covariância genérica deriva da ação V e(g)=e(ug) e da invariância da amplitude. Na instanciação concreta essa hipótese é descarregada por gamma_exponential. As hipóteses de operador Weyl/kernel/totalidade desaparecem do enunciado concreto.'},
    {'id':'same_fock','verdict':'PASSA','statute':'REAL','finding':'ConcreteWeylR1 usa F1Rede.BosonicFock.F, o vacuum e exponential já construídos. W_vacuum e a característica gaussiana são derivados. Não há novo Hilbert, vácuo substituto ou densidade postulada.'},
    {'id':'net_and_cyclicity','verdict':'PASSA','statute':'REAL','finding':'R é a álgebra bicomutante dos W(K); monotonia/localidade/covariância consomem leis agora concretas. vacuum_orbit_total e global_vacuum_cyclic usam todos f:H1 e K=top. Não estabelecem ciclicidade ou separação de uma cunha.'},
    {'id':'flow_scope','verdict':'PASSA_COM_HIPOTESE_EXPLICITA','statute':'REAL','finding':'wedgeFlow continua recebendo LightNetData como dado de localização. As leis zero/add são algébricas; não são identificação modular, KMS ou construção de um habitante físico desse registro.'},
]
integration={
    'severity':'MATERIAL_PARA_INTEGRACAO_MODULAR_FUTURA',
    'current_theorems_invalidated':False,
    'status':'ACHADO_DERIVADO__TRATAMENTO_PLANEJADO_EM_MODULO_SEPARADO',
    'finding':'O W atual é D(f), cuja órbita do vácuo é proporcional a e(f). Para f em K, a regra de Tomita na órbita é S e(f)=e(-f). Se S_K fixa K, identificar diretamente esse S com Gamma(S_K) tem sinal incompatível para f não nulo. Não se deve promover R_D(K) e Gamma(J_K) à identificação modular sem uma ponte de fase.',
    'parent_decision_declared':'Root aceitou a ressalva e planejou FieldWeylR1 com W_field(f)=D(i*f), sem 1/sqrt(2) nesta convenção, e R_field(K)=R_D(iK). A rotação i preserva inner e o cociclo; a conjugação antilinear envia i*f a -i*f quando S_K fixa f.',
    'verification_limit':'Esta revisão só verifica as quatro fontes listadas. O módulo futuro e sua integração não são considerados compilados ou aprovados por este recibo.'
}
scope=[
    'Recompilação independente uma vez de cada fonte aceita, Lean 4.31.0, fonte copiada byte a byte, dependências pinadas antes/depois, LEAN_PATH literal nos recibos.',
    'Os três módulos seguintes importaram os módulos precedentes recompilados pelo revisor; Concrete importou também ExponentialVectors/Totality recompilados independentemente.',
    '66 declarações/impressões, incluindo auxiliares gerados, somente no trio propext/Classical.choice/Quot.sound; zero sorry.',
    'Os .olean podem diferir: caminhos absolutos distintos estão serializados e as dependências foram recompiladas. Não se alega identidade binária nem que o caminho seja a única causa de cada diferença.',
    'Não houve revisão própria do Gram: consume-se o parecer independente do root. Não se afirma continuidade forte de W, ciclicidade/separação de cunha, KMS/BW, certificado Fock completo ou confirmação física.',
    'Nenhum original, memória, produção, Nós ou gate foi modificado. AUDITADA/FECHADA é ato da gerência.'
]
report={'unit':'F1.FECHO_20261015','claim_event':845,'reviewer':'/root/atrator_skeptic','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'verdict':'PASSA_NO_ESCOPO_COM_RESSALVA_DE_INTEGRACAO_MODULAR','checks':checks,'integration_finding':integration,'builds':builds,'binary_comparison':binary,'source_anchors':anchors,'scope':scope,'gram_independent_review':pin(P/'weyl_extension/REVIEW_ROOT_R1.json'),'exponential_independent_review':pin(P/'exponential_review/REVISAO_EXPONENCIAIS_R1.json'),'previous_net_flow_review':pin(P/'network_wiring_review/REVISAO_REDE_MATERIA_R1.json'),'generator':pin(__file__)}
put(B/'REVISAO_WEYL_R1.json',json.dumps(report,ensure_ascii=False,indent=2)+'\n')
lines=['# Revisão independente dos operadores de Weyl','','[REAL] PASSA nos teoremas enunciados, com ressalva material para a integração modular futura.','',
    '## Ressalva de integração','',integration['finding'],'',
    '[DECLARADO — decisão do root] '+integration['parent_decision_declared'], '',integration['verification_limit'],'',
    '## Recompilação independente','','| Fonte | EXIT | Segundos | Declarações/impressões | .olean idêntico |','|---|---:|---:|---:|---|']
for b in builds.values():lines.append(f"| {Path(b['source']['path']).name} | {b['exit_code']} | {b['seconds']:.6f} | {b['axiom_count']} | {b['olean_identical_to_accepted']} |")
lines+=['','## Conferência matemática','']+[f"- **{c['id']} — {c['verdict']}:** {c['finding']}" for c in checks]
lines+=['','## Alcance','']+['- '+s for s in scope]
lines+=['','Recibos, hashes, linhas e evidência de comparação: REVISAO_WEYL_R1.json.']
put(B/'REVISAO_WEYL_R1.md','\n'.join(lines)+'\n')
print(json.dumps({'verdict':report['verdict'],'json':pin(B/'REVISAO_WEYL_R1.json'),'md':pin(B/'REVISAO_WEYL_R1.md')},ensure_ascii=False))
