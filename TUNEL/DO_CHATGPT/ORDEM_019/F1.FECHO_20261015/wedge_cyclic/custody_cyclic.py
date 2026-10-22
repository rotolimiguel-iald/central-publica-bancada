"""Freeze the accepted cyclic/separating construction with all attempts retained."""
from pathlib import Path
import datetime,hashlib,json,re,sys,os
b=Path(__file__).resolve().parent
name=sys.argv[1]
def pin(p):return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size)
def save(p,data):
    if isinstance(data,str):data=data.encode('utf8')
    with p.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
    assert p.read_bytes()==data
src=b/(name+'.lean');matches=[];failed=[]
for p in sorted((b/'attempts').glob('*/RECEIPT.json')):
    r=json.loads(p.read_bytes())
    if r['exit_code']==0 and (p.parent/src.name).exists() and (p.parent/src.name).read_bytes()==src.read_bytes():matches.append((p,r))
    elif r['exit_code']!=0:failed.append(dict(receipt=pin(p),source=r['source'],build=pin(p.parent/'BUILD.log')))
assert matches
p,r=matches[-1];raw=(p.parent/'AXIOMS.txt').read_text(encoding='utf8');code=src.read_text(encoding='utf8')
assert 'sorryAx' not in raw and 'error:' not in raw and not re.search(r'\bsorry\b|^axiom\b',code,re.M)
d=dict(unit='F1.FECHO_20261015',claim=845,status='REAL_COMPILED_SANDBOX_REVIEW_PENDING',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source=pin(src),receipt=pin(p),build=pin(p.parent/'BUILD.log'),axioms=pin(p.parent/'AXIOMS.txt'),olean=pin(p.parent/(name+'.olean')),seconds=r['seconds'],exit_code=r['exit_code'],dependencies_unchanged=r['readonly_dependencies_unchanged'],theorems=re.findall(r'^(?:@\[simp\]\s+)?theorem\s+([^\s]+)',code,re.M),printed_axioms=re.findall(r"^'(.+)' depends on axioms:",raw,re.M),failed_attempts=failed,survey=pin(b/'WEDGE_CYCLIC_SURVEY_R1.json'),scope=['For every StandardSubspace K of the existing H1, the vacuum is cyclic and separating for the concrete Weyl algebra R(K).','The convention is W(f)=D(i f), on the same constructed sectors and Fock space.','Cyclicity uses density of exp(iK) and the nonzero vacuum displacement amplitude.','Separation uses locality with K.symplComp, its proved cyclicity, and continuity of bounded operators.','Applied by term to the already constructed canonical KWR; no algebra-cyclicity/separating input fields.','No algebra-vacuum Tomita identification, KMS, Maxwell, H3 or Takesaki identification asserted.'],production_modified=False,gate_modified=False,provider_calls=False,sorry=0,allowed_axioms=['propext','Classical.choice','Quot.sound'])
save(b/'FINAL_WEDGE_CYCLIC_RECEIPT_R1.json',json.dumps(d,ensure_ascii=False,indent=2)+'\n')
save(b/'RELATORIO_WEDGE_CYCLIC_R1.md','# Vácuo cíclico e separante na cunha\n\n[REAL — compilado em sandbox]. Para todo StandardSubspace K no H1 existente, o vácuo do mesmo Fock é cíclico e separante para R(K), a álgebra concretamente gerada pelos W(k)=D(ik). Há aplicação por termo ao KWR já construído.\n\nA ciclicidade decorre de e(iK) total e W(k)Ω ser um múltiplo não nulo de e(ik). A separação usa o complemento simplético padrão: aΩ=0 implica a bΩ=b aΩ=0 para todo b da álgebra do complemento; pela ciclicidade provada e continuidade, a=0. Nenhuma dessas duas propriedades é assumida como campo.\n\nOs teoremas não identificam ainda o Tomita do par álgebra-vácuo, não provam KMS, não constroem Maxwell/H3 nem a identificação Takesaki. Artefatos e tentativas são aditivos; originais, produção, memória e gate permanecem intactos.\n')
print(json.dumps(pin(b/'FINAL_WEDGE_CYCLIC_RECEIPT_R1.json'),ensure_ascii=False))
