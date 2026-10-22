from pathlib import Path
import datetime, hashlib, json, re

B=Path(__file__).resolve().parent
P=B.parent
def pin(p):
    p=Path(p);raw=p.read_bytes()
    return {'path':str(p),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
def put(p,s):
    raw=s.encode('utf-8')
    with p.open('xb') as f:f.write(raw)
    assert p.read_bytes()==raw
builds={};anchors=[]
for name in ['continuity','field']:
    path=B/name/'RECEIPT_R1.json';r=json.loads(path.read_text(encoding='utf-8'))
    assert r['passed'] and r['exit_code']==0
    assert all(set(v)<={'propext','Classical.choice','Quot.sound'} for v in r['axioms'].values())
    for item in r['dependencies_before_after']:assert pin(item['path'])['sha256']==item['sha256']
    assert pin(r['source']['path'])==r['source']
    assert pin(r['olean']['path'])==r['olean']
    builds[name]={'receipt':pin(path),**{k:r[k] for k in ['start_utc','end_utc','seconds','source','exit_code','axiom_count','olean','olean_identical_to_accepted','log']}}
    for no,line in enumerate(Path(r['source']['path']).read_text(encoding='utf-8').splitlines(),1):
        if re.match(r'(?:theorem|def) ',line):anchors.append({'source':r['source']['path'],'line':no,'declaration':line})
assert builds['continuity']['axiom_count']==5
support=P.parent/'F1.REDE/fock_construction/attempts/20261013T223630_675979Z/BosonicSectorContinuity.lean'
checks=[
    {'id':'exponential_continuity','verdict':'PASSA','statute':'REAL','finding':'A norma da diferença entre exponenciais deriva da expansão do produto interno e da identidade exp(inner). A continuidade resulta de funções escalares contínuas e limite zero; não é hipótese.'},
    {'id':'strong_continuity','verdict':'PASSA','statute':'REAL','finding':'A órbita W(f)e(g) é contínua pela amplitude e pelo mapa exponencial. O subespaço de órbitas contínuas é fechado por convergência uniforme decorrente de ||D(f)||=1; sua inclusão do span total dos exponenciais permite alcançar todo vetor. O argumento reutiliza continuousOrbitSpace_closed, sem assumir regularidade da família D.'},
    {'id':'continuity_topology','verdict':'PASSA_COM_ESCOPO','statute':'REAL','finding':'O enunciado prova continuidade forte, f↦W(f)ψ para cada ψ, e regularidade t↦W(tf)ψ. Não prova continuidade na norma de operador ou diferenciabilidade/geradores.'},
    {'id':'phase_rotation','verdict':'PASSA','statute':'REAL','finding':'rotate(f)=i*f preserva inner e a forma simplética. W_field(f)=D(i*f) conserva exatamente o cociclo exp(-i Im inner(f,g)), sem 1/sqrt(2) adicional. A lei de adjunto e a covariância unitária são transportadas com sinais consistentes.'},
    {'id':'field_net','verdict':'PASSA','statute':'REAL','finding':'A álgebra de campo é gerada por D(i*f) para f em K, no mesmo Fock e vácuo. R_mono/R_local/R_cov e o fluxo restrito são derivados dessas leis. A identidade wedgeFlow_is_Ad tem o sinal -(2*pi*t) previsto na assinatura.'},
    {'id':'previous_integration_finding','verdict':'CORRECAO_DE_FASE_ATENDIDA__IDENTIFICACAO_TOMITA_ABERTA','statute':'REAL/DERIVED','finding':'A ressalva de convenção do parecer R1 foi tratada por um módulo novo e separado. A órbita agora é proporcional a e(i*k), compatível com a antilinearidade de S_K quando S_K k=k. Esta compatibilidade de fase não demonstra que o Tomita da álgebra seja Gamma(S_K); nenhuma identificação Tomita, ciclicidade/separação de cunha ou KMS é afirmada por estas fontes.'},
]
scope=['Rodada material limitada às duas fontes novas; os quatro Weyl antigos aprovados não foram recompilados novamente.',
       'Recompilações em sandbox próprio com Lean 4.31.0, cópias exatas, dependências independentes quando disponíveis e hashes conferidos antes/depois. Logs registram comando, início/fim/segundos/exit e LEAN_PATH literal.',
       'As tentativas FieldWeyl R1/R2 recusadas não integram o aceite. Nenhuma fonte do construtor foi alterada pelo revisor.',
       'LightNetData continua hipótese de localização do fluxo. Nenhum FockCertificate completo ou habitante físico foi produzido por esta revisão.',
       'Originais, memória, produção e gate preservados; AUDITADA/FECHADA pertence à gerência.']
report={'unit':'F1.FECHO_20261015','claim_event':845,'reviewer':'/root/atrator_skeptic','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'verdict':'PASSA_NO_ESCOPO__FASE_CORRIGIDA_SEM_ALEGAR_TOMITA','checks':checks,'material_findings_current':[],'builds':builds,'anchors':anchors,'support_read':{**pin(support),'lines':'25-49: continuousOrbitSpace and closedness by uniform isometric bound'},'previous_review':pin(B/'REVISAO_WEYL_R1.json'),'oh_review_separate':pin(P/'physical_clock_reuse/review/REVISAO_OH_R1.json'),'scope':scope,'generator':pin(__file__)}
put(B/'REVISAO_WEYL_CONTINUIDADE_CAMPO_R1.json',json.dumps(report,ensure_ascii=False,indent=2)+'\n')
lines=['# Revisão independente: continuidade e convenção de campo','','[REAL] PASSA nos enunciados revisados. A correção de fase atende à ressalva anterior; a identificação Tomita continua fora do escopo.','','| Fonte | EXIT | Segundos | Declarações/impressões | .olean idêntico |','|---|---:|---:|---:|---|']
for b in builds.values():lines.append(f"| {Path(b['source']['path']).name} | {b['exit_code']} | {b['seconds']:.6f} | {b['axiom_count']} | {b['olean_identical_to_accepted']} |")
lines+=['','Somente o trio propext/Classical.choice/Quot.sound; zero sorry.','']+[f"- **{c['id']} — {c['verdict']}:** {c['finding']}" for c in checks]
lines+=['','## Alcance','']+['- '+s for s in scope]
lines+=['','Recibo, hashes e linhas: REVISAO_WEYL_CONTINUIDADE_CAMPO_R1.json.']
put(B/'REVISAO_WEYL_CONTINUIDADE_CAMPO_R1.md','\n'.join(lines)+'\n')
print(json.dumps({'verdict':report['verdict'],'json':pin(B/'REVISAO_WEYL_CONTINUIDADE_CAMPO_R1.json'),'md':pin(B/'REVISAO_WEYL_CONTINUIDADE_CAMPO_R1.md')},ensure_ascii=False))
