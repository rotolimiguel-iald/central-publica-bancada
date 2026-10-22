from pathlib import Path
import hashlib,json,datetime,re,os
b=Path(__file__).resolve().parent
src=b/'ExponentialLiftR2.lean'
def pin(p):return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size)
def save(p,s):
 raw=s.encode('utf8')
 with p.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 assert p.read_bytes()==raw
matches=[];failed=[]
for p in sorted((b/'attempts').glob('*/RECEIPT.json')):
 d=json.loads(p.read_bytes())
 if d['exit_code']==0 and (p.parent/src.name).exists() and (p.parent/src.name).read_bytes()==src.read_bytes():matches.append((p,d))
 elif d['exit_code']!=0:failed.append(dict(receipt=pin(p),source=d['source'],build=pin(p.parent/'BUILD.log')))
p,d=matches[-1];raw=(p.parent/'AXIOMS.txt').read_text(encoding='utf8');code=src.read_text(encoding='utf8')
assert 'sorryAx' not in raw and 'error:' not in raw and not re.search(r'\bsorry\b|^axiom\b',code,re.M)
r=dict(unit='F1.FECHO_20261015',claim=845,created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='REAL_COMPILED_SANDBOX_REVIEW_PENDING',source=pin(src),receipt=pin(p),build=pin(p.parent/'BUILD.log'),axioms=pin(p.parent/'AXIOMS.txt'),olean=pin(p.parent/'ExponentialLiftR2.olean'),seconds=d['seconds'],exit_code=0,dependencies_unchanged=d['readonly_dependencies_unchanged'],survey=pin(b/'GAMMA_UNBOUNDED_SURVEY_R1.json'),theorems=re.findall(r'^theorem\s+([^\s]+)',code,re.M),printed_axioms=re.findall(r"^'(.+)' depends on axioms:",raw,re.M),failed_attempts=failed,scope=['Actual closed densely-defined symmetric LinearPMap on the same constructed Fock.','Built from the closure of the span of (e(f),e(Tf)), for a self-adjoint operator T on the existing H1.','Functionality is proved from self-adjoint one-particle pairing and totality of e(D(T)).','Exact action on exponential vectors and every component of those vectors is proved.','The span of exponential pairs is a real graph core: sequences converge in both coordinates.','Applied concretely to TW; this is not yet self-adjointness or positivity of the lift, full spectral second quantization, or the algebra-vacuum Tomita polar identification.'],production_modified=False,gate_modified=False,provider_calls=False,sorry=0,allowed_axioms=['propext','Classical.choice','Quot.sound'])
save(b/'FINAL_EXPONENTIAL_LIFT_RECEIPT_R1.json',json.dumps(r,ensure_ascii=False,indent=2)+'\n')
save(b/'RELATORIO_EXPONENTIAL_LIFT_R1.md','# Levantamento exponencial fechado de TW\n\n[REAL — compilado em sandbox]. O novo operador é um LinearPMap fechado, densamente definido e simétrico no MESMO Fock já construído. Seu grafo é o fecho do span dos pares (e(f),e(Tf)), f no domínio de T; a funcionalidade é demonstrada pela simetria de T e pela totalidade de e(D(T)), sem hipótese de existência da extensão. Há aplicação concreta a TW.\n\nA ação e(f) → e(Tf) e suas componentes setoriais são termos. O span dos pares é core do operador construído em norma de grafo, com sequência convergindo simultaneamente na entrada e na saída; não se promove mera densidade em F a core.\n\n[OPEN] Auto-adjunção e positividade do operador fechado, identificação espectral com Γ(TW), e identidade com o fator positivo do Tomita do par álgebra-vácuo. O core demonstrado pertence ao operador recém-construído: não é por si uma identificação com o Tomita do par. Nenhuma alteração de produção, kernel, memória, gate ou fila externa.\n')
print(json.dumps(pin(b/'FINAL_EXPONENTIAL_LIFT_RECEIPT_R1.json'),ensure_ascii=False));print(len(r['theorems']),len(r['printed_axioms']))
