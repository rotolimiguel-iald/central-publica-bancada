"""Pin successful local Gamma(J) construction and preserve all failed builds."""
from pathlib import Path
import json,hashlib,re,datetime,sys,os
b=Path(__file__).resolve().parent
names=sys.argv[1:] or ['AntilinearTensorR4','BosonicGammaJR4','CanonicalFockAntiAssemblyR2']
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
      local_declarations=[x.split('\t')[1] for x in raw.splitlines() if x.startswith('LOCAL_DECL\t')],
      explicit_theorems=re.findall(r'^(?:@\[simp\]\s+)?theorem\s+([^\s]+)',code,re.M)))
failed=[]
for p in sorted((b/'attempts').glob('*/RECEIPT.json')):
    d=json.loads(p.read_bytes())
    if d['exit_code']!=0:failed.append(dict(receipt=pin(p),build=pin(p.parent/'BUILD.log'),source=d['source'],exit_code=d['exit_code']))
d=dict(unit='F1.FECHO_20261015',claim=845,status='REAL_COMPILED_SANDBOX_INDEPENDENT_REVIEW_PENDING',
  created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),modules=modules,failed_attempts=failed,
  source_plan=pin(b/'GAMMA_J_REUSE_PLAN_R1.json'),kinematic_assembly=pin(b.parent/'network_reuse/FINAL_ASSEMBLY_RECEIPT_R1.json'),
  accounting=dict(original_certificate_fields_including_instances=63,paid_kinematic_scientific_fields=12,paid_kinematic_instances=3,
    additional_paid_fields=['J','J_invol','J_vac'],remaining_fields_including_core_instances=45),
  actual_inhabitant='antiunitary_fragment_inhabited: same F, same vacuum, same oneParticle, Jcandidate from concrete D1a3.',
  still_named=['Global net K with canonical wedge glue','Fock spectral properties','Weyl algebras/locality/cyclicity/separation','BW KMS and Tomita of the algebra-vacuum pair','Takesaki core/embedding/dual action/trace and finite projection on the same pair','Maxwell certificate and H3 named contracts'],
  not_claimed=['No inhabitant of RemainingAnalyticInput or full FockCertificate','No modular identification merely from Gamma(J)','No physical confirmation or global H3 derivation'],
  provider_jobs='Existing MiMo/DeepSeek requests preserved; local Codex construction only, no dispatch/cancel/substitution.',
  production_modified=False,gate_modified=False,external_calls=False,sorry=0,allowed_axioms=['propext','Classical.choice','Quot.sound'])
save(b/'FINAL_GAMMA_J_RECEIPT_R1.json',json.dumps(d,ensure_ascii=False,indent=2)+'\n')
text='''# Γ(J) no Fock canônico — R1

[REAL — compilado em sandbox; revisão independente pendente]. A J do D1a3 concreto foi transportada aos mesmos tensores, completações, setores bosônicos e soma de Hilbert já construídos na F1.REDE. Não há uma equivalência abstrata escolhendo outro Fock.

A construção fornece Γ(J), sua involução, preservação do vácuo e ação no setor de uma partícula. O novo consumidor fornece J/J_invol/J_vac por termo, eliminando esses três campos da entrada. A cinemática anterior fornece outros12 campos e3 instâncias. Dos63 campos do certificado original,45 permanecem explícitos, incluindo3 instâncias do Core.

O fragmento antiunitário tem habitante concreto, independente do registro restante. Não se reivindica habitante do registro analítico completo. Tomita/KMS do mesmo par, Weyl/CCR, propriedades espectrais no Fock, core de Takesaki, Maxwell e a rede global com sua colagem continuam os alvos precisos; não são inferidos da antiunitariedade.

As fontes, .olean, axiomas, logs reais e tentativas falhas estão pinados em FINAL_GAMMA_J_RECEIPT_R1.json. Axiomas permitidos somente propext, Classical.choice e Quot.sound; nenhum sorry na versão aceita. Os pedidos externos existentes permanecem intactos para conciliação pela coordenação. Nada foi gravado em produção e nada move o gate.
'''
save(b/'RELATORIO_GAMMA_J_R1.md',text)
print(json.dumps(pin(b/'FINAL_GAMMA_J_RECEIPT_R1.json'),ensure_ascii=False))
print('modules',len(modules),'failed_attempts',len(failed),'explicit_theorems',sum(len(x['explicit_theorems']) for x in modules))
