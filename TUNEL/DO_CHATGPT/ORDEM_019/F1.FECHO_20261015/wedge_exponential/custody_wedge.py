"""Freeze new wedge-exponential totality evidence; preserve failed attempts."""
from pathlib import Path
import hashlib,json,datetime,re,sys,os
b=Path(__file__).resolve().parent
names=sys.argv[1:]
assert names
def pin(p):return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size)
def save(p,s):
    data=s.encode('utf8')
    with p.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
    assert p.read_bytes()==data
modules=[]
for name in names:
    src=b/(name+'.lean'); matches=[]
    for p in sorted((b/'attempts').glob('*/RECEIPT.json')):
        d=json.loads(p.read_bytes());snap=p.parent/src.name
        if d['exit_code']==0 and snap.exists() and snap.read_bytes()==src.read_bytes(): matches.append((p,d))
    assert matches,name
    p,d=matches[-1];raw=(p.parent/'AXIOMS.txt').read_text(encoding='utf8');code=src.read_text(encoding='utf8')
    assert 'sorryAx' not in raw and 'error:' not in raw and not re.search(r'\bsorry\b|^axiom\b',code,re.M)
    modules.append(dict(module=name,source=pin(src),receipt=pin(p),build=pin(p.parent/'BUILD.log'),axioms=pin(p.parent/'AXIOMS.txt'),olean=pin(p.parent/(name+'.olean')),seconds=d['seconds'],exit_code=d['exit_code'],dependencies_unchanged=d['readonly_dependencies_unchanged'],theorems=re.findall(r'^(?:@\[simp\]\s+)?theorem\s+([^\s]+)',code,re.M),printed_axioms=re.findall(r"^'(.+)' depends on axioms:",raw,re.M)))
failed=[]
for p in sorted((b/'attempts').glob('*/RECEIPT.json')):
    d=json.loads(p.read_bytes())
    if d['exit_code']!=0:failed.append(dict(receipt=pin(p),source=d['source'],build=pin(p.parent/'BUILD.log')))
sector=b.parent.parent/'F1.REDE/fock_construction/BosonicSectorContinuity.lean'
d=dict(unit='F1.FECHO_20261015',claim=845,status='REAL_COMPILED_SANDBOX_REVIEW_PENDING',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),modules=modules,failed_attempts=failed,survey=pin(b/'WEDGE_EXPONENTIAL_SURVEY_R1.json'),reused_tensor_bilinear=pin(sector),exponential_base=pin(b.parent/'network_exponential/FINAL_EXPONENTIAL_RECEIPT_R1.json'),scope=['Real K with dense complex span implies totality of exponential(K).','StandardSubspace cyclicity gives the density assumption; applied to existing canonical KWR.','Proof uses real power-series coefficient uniqueness, analytic continuation x+t*y to x+i*y and sector closed spans.','No exponential totality assumed as a field.','Not yet the algebra-vacuum Tomita identification or KMS theorem.'],convention='For physical W_field(f)=D(i*f), apply the same result to K.mulI; no convention silently interchanged.',production_modified=False,gate_modified=False,provider_calls=False,sorry=0,allowed_axioms=['propext','Classical.choice','Quot.sound'])
save(b/'FINAL_WEDGE_EXPONENTIAL_RECEIPT_R1.json',json.dumps(d,ensure_ascii=False,indent=2)+'\n')
save(b/'RELATORIO_WEDGE_EXPONENTIAL_R1.md','# Totalidade exponencial na cunha\n\n[REAL — compilado em sandbox]. Para um subespaço real K de H1 cujo span complexo é denso, o span complexo de e(K) é denso no mesmo Fock canônico. A totalidade é conclusão, não campo de entrada.\n\nA prova extrai os coeficientes pela série real e estende os tensores diagonais de K para K+iK por identidade analítica. A complexificação é identificada com o span complexo; continuidade e os spans fechados dos setores completam o argumento. O IsCyclic de StandardSubspace fornece a hipótese de densidade, com aplicação por termo ao KWR existente.\n\nO produto tensorial bilinear contínuo é reaproveitado de BosonicSectorContinuity, além da construção anterior dos exponenciais. Para a convenção W_field(f)=D(i f), usa-se a mesma prova em K.mulI. Identificação de Tomita do par álgebra-vácuo e KMS permanecem etapas próprias. Recibo, fontes, logs e falhas são novos; nada modifica produção, gate ou pedidos externos.\n')
print(json.dumps(pin(b/'FINAL_WEDGE_EXPONENTIAL_RECEIPT_R1.json'),ensure_ascii=False))
print('modules',len(modules),'theorems',sum(len(x['theorems']) for x in modules))
