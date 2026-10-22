from pathlib import Path
import datetime, hashlib, json, re
B=Path(__file__).resolve().parent
P=B.parent
def pin(p):
 p=Path(p);b=p.read_bytes();return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def put(p,s):
 with p.open('x',encoding='utf-8',newline='\n') as f:f.write(s)
builds=[]
for name in ['analytic','span','totality','cyclic']:
 rp=B/name/'RECEIPT_R1.json';r=json.loads(rp.read_text(encoding='utf-8'))
 assert r['passed'] and r['exit_code']==0 and r['source_exact_copy']
 assert all(set(v)<={'propext','Classical.choice','Quot.sound'} for v in r['axioms'].values())
 builds.append({'name':name,'receipt':pin(rp),'source':r['source'],'seconds':r['seconds'],'axiom_count':r['axiom_count'],'olean_identical':r['olean_identical_to_accepted'],'source_sha256':r['source']['sha256']})
inputs=[]
for rel in ['wedge_exponential/FINAL_WEDGE_EXPONENTIAL_RECEIPT_R1.json','wedge_cyclic/FINAL_WEDGE_CYCLIC_RECEIPT_R1.json']:
 f=P/rel;x=json.loads(f.read_text(encoding='utf-8'));checked=[]
 def walk(x):
  if isinstance(x,dict):
   if 'path' in x and 'sha256' in x:
    actual=pin(x['path']);assert actual['sha256']==x['sha256'];checked.append(actual)
   else:
    for y in x.values():walk(y)
  elif isinstance(x,list):
   for y in x:walk(y)
 walk(x);inputs.append({'receipt':pin(f),'pins_verified':checked})
analysis=[
 {'source':'WedgeAnalyticR2.lean:27-49','finding':'PASSA','text':'Ortogonalidade aos exponenciais de K implica que cada coeficiente setorial é zero, restringindo a série inteira a t real com t*x em K. O peso 1/sqrt(n!) é estritamente positivo. Totalidade não é premissa.'},
 {'source':'WedgeAnalyticR2.lean:51-80','finding':'PASSA','text':'Analiticidade dos tensores puros vem do produto tensorial bilinear contínuo e da inclusão na completude. A sequência real 1/(n+1) dá zeros distintos acumulando em 0; aplica-se o teorema de identidade no domínio complexo conexo inteiro.'},
 {'source':'StandardComplexSpanR1.lean:12-33','finding':'PASSA','text':'K+iK é denso pelo campo IsCyclic de StandardSubspace; a clausura do span complexo contém K e iK. Só a metade cíclica da standardness é necessária para esta conclusão; não se assume densidade exponencial.'},
 {'source':'RealSubspaceTotalityR5.lean:16-68','finding':'PASSA','text':'A complexificação algébrica K+iK é provada igual ao span complexo. Para x,y em K, o polinômio P(c)=inner(v_n,(x+c*y)^tensor n) anula na reta real; continuação analítica dá P(i)=0. O inner é linear no segundo argumento.'},
 {'source':'RealSubspaceTotalityR5.lean:70-111','finding':'PASSA','text':'A densidade do span complexo e a continuidade estendem a anulação a todo H1; a totalidade dos tensores puros em cada setor e lp.ext dão v=0. O complemento ortogonal nulo entrega a totalidade exponencial. A aplicação a spectralOutput.KWR usa um habitante já construído.'},
 {'source':'WedgeCyclicR3.lean:23-49','finding':'PASSA','text':'Na convenção W(f)=D(i*f), W(k)Omega é amplitude não nula vezes e(i*k). A totalidade é aplicada a K.mulI. Isso prova a ciclicidade de R(K), não só ciclicidade global para K=top.'},
 {'source':'WedgeCyclicR3.lean:51-83','finding':'PASSA','text':'O complemento simplético K-prime é standard pela biblioteca. Localidade força a comutar com todo b de R(K-prime); a*Omega=0 implica a*b*Omega=0. Ciclicidade de K-prime e continuidade de a dão a=0. Não se assume separação da álgebra.'}
]
reuse=[pin(P/'exponential_review/REVISAO_EXPONENCIAIS_R1.json'),pin(P/'weyl_review/REVISAO_WEYL_CONTINUIDADE_CAMPO_R1.json'),pin(P.parent/'F1.REDE/fock_construction/BosonicFock.lean'),pin(Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\.lake\packages\mathlib\Mathlib\Analysis\InnerProductSpace\StandardSubspace.lean'))]
report={'unit':'F1.FECHO_20261015','claim':845,'reviewer':'codex-atrator-skeptic','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'verdict':'PASSA_COM_ESCOPO','status':'REAL_REVIEW_AND_INDEPENDENT_BUILDS','material_findings':[],'low_findings':[],'theorems_in_sources':21,'printed_axiom_reports':sum(r['axiom_count'] for r in builds),'zero_sorry':True,'trio_only':True,'builds':builds,'mathematical_analysis':analysis,'nonvacuity':'O consumidor usa spectralOutput.KWR concreto. F é o mesmo Fock já construído e Omega tem norma 1 (BosonicFock.lean:25), não espaço nulo. Não se exige como campo o resultado a provar.','scope':['Para K real de span complexo denso, exp(K) é total no Fock canônico.','Para K standard, Omega é cíclico e separante de R(K) na convenção W(f)=D(i*f); aplica-se à cunha canônica existente.','Não identifica o Tomita da álgebra-vácuo, nem estabelece KMS/BW, Maxwell, H3, Takesaki ou realização física.','Standardness é hipótese nos teoremas gerais, habitada pelo consumidor KWR; nenhuma rede completa com todos os certificados é reivindicada.','Não foi repetida a compilação dos exponenciais/Weyl já revisados: reutilizaram-se seus artefatos independentes.','A execução elevada segue a autorização desta unidade; tempo menor não prova a causa da latência anterior.'],'inputs':inputs,'reused_sources':reuse,'script':pin(__file__),'production_memory_originals_gate_modified':False,'provider_calls':False,'management_status_changed':False}
put(B/'REVISAO_CUNHA_R1.json',json.dumps(report,ensure_ascii=False,indent=2)+'\n')
lines=['# Revisão independente — totalidade na cunha e vácuo cíclico/separante','','[REAL] **PASSA COM ESCOPO**, sem achado material. Claim 845; decisão AUDITADA/FECHADA continua da gerência.','','## Recompilação independente','','| Módulo | EXIT | Segundos | Impressões de axiomas | .olean idêntico |','|---|---:|---:|---:|---|']
for b in builds:lines.append(f"| {b['source']['path'].split(chr(92))[-1]} | 0 | {b['seconds']:.3f} | {b['axiom_count']} | {b['olean_identical']} |")
lines+=['','21 teoremas nas fontes, 17 impressões de axiomas: somente propext, Classical.choice e Quot.sound; zero sorry. Logs/recibos guardam início, fim, duração, comando, toolchain e LEAN_PATH literal. Os quatro .olean são byte a byte os aceitos.','','## Conferência matemática','']
for a in analysis:lines.append(f"- **{a['source']}** — {a['text']}")
lines+=['','## Alcance e não vacuidade','',report['nonvacuity'],'']+[f'- {x}' for x in report['scope']]
lines+=['','Os hashes das duas entregas e de seus 37 pinos foram relidos. Fontes do construtor permaneceram intactas; a revisão copiou os bytes para subpastas próprias e recompilou com caches somente de leitura. O JSON guarda os pinos individuais, evidências e fontes reutilizadas. Nenhuma alteração de memória, produção ou gate.','']
put(B/'REVISAO_CUNHA_R1.md','\n'.join(lines))
print(json.dumps({'verdict':report['verdict'],'report':pin(B/'REVISAO_CUNHA_R1.json'),'markdown':pin(B/'REVISAO_CUNHA_R1.md'),'builds':[{k:b[k] for k in ['name','seconds','axiom_count','olean_identical']} for b in builds]},ensure_ascii=False))
