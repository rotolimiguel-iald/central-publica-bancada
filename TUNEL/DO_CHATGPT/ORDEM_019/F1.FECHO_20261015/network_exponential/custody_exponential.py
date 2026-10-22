"""Custody accepted local exponential-vector modules without modifying earlier files."""
from pathlib import Path
import json,hashlib,re,datetime,sys,os
b=Path(__file__).resolve().parent
names=sys.argv[1:]
assert names
def pin(p):return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size)
def save(p,data):
    data=data.encode() if isinstance(data,str) else data
    with p.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
    assert p.read_bytes()==data
modules=[]
for name in names:
    src=b/(name+'.lean'); match=[]
    for p in sorted((b/'attempts').glob('*/RECEIPT.json')):
        d=json.loads(p.read_bytes());snap=p.parent/src.name
        if d['exit_code']==0 and snap.exists() and snap.read_bytes()==src.read_bytes():match.append((p,d))
    assert match,name
    p,d=match[-1]; raw=(p.parent/'AXIOMS.txt').read_text(encoding='utf8')
    assert 'sorryAx' not in raw and 'error:' not in raw
    code=src.read_text(encoding='utf8')
    assert not re.search(r'\bsorry\b|^axiom\b',code,re.M)
    modules.append(dict(module=name,source=pin(src),receipt=pin(p),olean=pin(p.parent/(name+'.olean')),
      build=pin(p.parent/'BUILD.log'),axioms=pin(p.parent/'AXIOMS.txt'),seconds=d['seconds'],exit_code=d['exit_code'],
      readonly_dependencies_unchanged=d['readonly_dependencies_unchanged'],printed_axiom_names=re.findall(r"^'(.+)' depends on axioms:",raw,re.M),
      explicit_theorems=re.findall(r'^(?:@\[simp\]\s+)?theorem\s+([^\s]+)',code,re.M)))
failed=[]
for p in sorted((b/'attempts').glob('*/RECEIPT.json')):
    d=json.loads(p.read_bytes())
    if d['exit_code']!=0:failed.append(dict(receipt=pin(p),build=pin(p.parent/'BUILD.log'),source=d['source'],exit_code=d['exit_code']))
totality=any('exponential_total' in x['explicit_theorems'] for x in modules)
d=dict(unit='F1.FECHO_20261015',claim=845,status='REAL_COMPILED_SANDBOX_INDEPENDENT_REVIEW_PENDING',
  created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),modules=modules,failed_attempts=failed,
  source_plan=pin(b/'EXPONENTIAL_REUSE_PLAN_R1.json'),gamma_j=pin(b.parent/'network_antiunitary/FINAL_GAMMA_J_RECEIPT_R1.json'),
  construction='e(f)_n = (sqrt(n!))^(-1) pureTensor(n,f) on the exact same Sector n and F.',
  actual_results=['Mem lp 2 from exponential series', 'inner kernel exp(inner f g)', 'squared norm exp(norm f squared)']+(['Totality by analytic uniqueness and closed symmetric spans'] if totality else []),
  totality_proved=totality,
  not_claimed=['No Weyl operator yet','No algebra-vacuum Tomita or KMS merely from exponential totality','No global net or physical H3 constructed'],
  provider_jobs='Existing MiMo exponential-vector request preserved; local Codex construction only, no dispatch/cancel/substitution.',
  production_modified=False,gate_modified=False,external_calls=False,sorry=0,allowed_axioms=['propext','Classical.choice','Quot.sound'])
save(b/'FINAL_EXPONENTIAL_RECEIPT_R1.json',json.dumps(d,ensure_ascii=False,indent=2)+'\n')
save(b/'RELATORIO_EXPONENTIAL_R1.md','# Vetores exponenciais no Fock canônico\n\n[REAL — compilado em sandbox]. A construção usa exatamente os setores e F da F1.REDE; não escolhe outro espaço nem supõe a existência dos vetores. O peso é 1/√(n!). A soma dos quadrados das normas é exp(‖f‖²), e o produto interno é exp(⟨f,g⟩).\n\n'+('A totalidade foi demonstrada: a ortogonalidade a todos os exponenciais faz uma série analítica escalar ser zero; cada coeficiente zera por unicidade. Como cada setor é o fecho do span dos tensores puros, cada componente do vetor ortogonal zera. Nenhuma hipótese de densidade foi acrescentada.\n\n' if totality else 'A totalidade ainda não está demonstrada nesta entrega.\n\n')+'As fontes, logs, axiomas, objetos e falhas estão pinados no recibo. Weyl/CCR, identificação modular do par, rede global, Takesaki e H3 permanecem suas obrigações próprias. Nenhuma mudança de produção, de gate ou nos pedidos externos existentes.\n')
print(json.dumps(pin(b/'FINAL_EXPONENTIAL_RECEIPT_R1.json'),ensure_ascii=False))
print('modules',len(modules),'totality',totality,'theorems',sum(len(x['explicit_theorems']) for x in modules))
