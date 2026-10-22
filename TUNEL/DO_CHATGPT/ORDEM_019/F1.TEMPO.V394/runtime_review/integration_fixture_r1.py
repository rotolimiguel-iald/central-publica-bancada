"""Execute integrator only against a miniature fixture under runtime_review."""
from pathlib import Path
import ast, hashlib, json, os, sys
from datetime import datetime, timezone
BASE=Path(__file__).resolve().parent
UNIT=BASE.parent
ROOT=UNIT.parents[4]
SCRIPT=ROOT/'work/rede_quantica_20261013/integrate_time_v394.py'
FIX=BASE/'integration_fixture'
OUT=FIX/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.TEMPO.V394'
def pin(p):
    p=Path(p);b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def new(p,value):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    data=(value if isinstance(value,str) else json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode()
    with p.open('xb') as f:f.write(data)
    return pin(p)
baseline='''UM_VERSION = 'v393'
_EMBEDDED_KERNEL_FILES = {
    'TGLExt.lean': '-- preserved aggregator\\n',
    'TGL/Audit.lean': '-- preserved audit\\n',
}
_LEAN_THEOREM_FLAGS = {
    'old_flag': 'Old.theorem',
}
LINEAGE = [
    ('v393', 'RuleTruthContract', 'TGLExt/Old.lean', None, None),
]
def old_check(n_cl_, n_ex_):
    esc_ok_ = isinstance(n_cl_, int) and n_cl_ == n_ex_ == _V393_ESCADA["esperada"]
    return esc_ok_
def emit_article(core):
    pt = build_pt(core)
    en = build_en(core)
    return pt,en
def seal(core):
    return {
            "registros_v393": {},
    }
def main():
    core = {}
    _figs = emit_figures(core)
'''
new(OUT/'baseline/um.py',baseline)
new(OUT/'candidate/um.py',baseline)
module=OUT/'fixture_source.lean';new(module,'theorem fixture : True := True.intro\n')
new(OUT/'formal_verified/FORMAL_MANIFEST.json',{'passed':True,'modules':[{
    'relative':'TimeFixture.lean','path':str(module),'sha256':pin(module)['sha256'],'theorems':['fixture']}]})
for rel in ('physical_contract/physical_parameters.py','runtime/time_runtime_v394.py'):
    p=OUT/rel;p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write((UNIT/rel).read_bytes())
rels=['IGUALDADE_RECONHECIMENTO_R8/OPERADOR_IGUALDADE_VERBATIM.txt',
      'FREQUENCIA_E_GRAVITON_R9/OPERADOR_FREQUENCIA_VERBATIM.txt',
      'FREQUENCIA_E_GRAVITON_R9/OPERADOR_PONTE_EXISTENTE_VERBATIM.txt',
      'ENCAMINHAMENTO_V394_20261015/OPERADOR_ENVIO_V394_VERBATIM.txt']
source_verbatims=[]
for rel in rels:
    original=UNIT.parent/'F1.TEMPO.LEITURA_20261015'/rel
    raw=original.read_bytes();txt=original.read_text(encoding='utf-8')
    source_verbatims.append({'source':pin(original),'text_roundtrip_bytes_equal':raw==txt.encode('utf-8')})
    p=OUT.parent/'F1.TEMPO.LEITURA_20261015'/rel;p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(raw)

tree=ast.parse(SCRIPT.read_text(encoding='utf-8'))
nodes=[n for n in tree.body if not (isinstance(n,ast.ImportFrom) and n.module=='diary_r1') and not isinstance(n,ast.If)]
ns={'ROOT':FIX,'new':new,'pin':pin,'__file__':str(SCRIPT),'__name__':'isolated_integrator_fixture'}
def audit(event,args):
    if event in {'subprocess.Popen','os.system','socket.connect','socket.bind'}:raise RuntimeError('Forbidden '+event)
    if event=='open':
        p,mode,flags=args
        writing=isinstance(mode,str) and any(c in mode for c in 'wax+')
        writing=writing or isinstance(flags,int) and bool(flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC))
        if writing and isinstance(p,(str,bytes)) and not Path(os.fsdecode(p)).resolve().is_relative_to(BASE):raise RuntimeError('External write')
sys.addaudithook(audit)
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(SCRIPT)+' [fixture]','exec'),ns)
ns['main']()
candidate=OUT/'candidate/um.py'
first=pin(candidate);first_mtime=candidate.stat().st_mtime_ns
first_backup_count=len(list(candidate.parent.glob('um.py.bak_*')))
first_receipt=pin(OUT/'INTEGRATION_R1.json')
try:ns['main']()
except Exception as exc:repeat={'exception':type(exc).__name__,'message':str(exc)}
else:repeat={'exception':None}
repeat.update({'candidate_bytes_equal':pin(candidate)==first,'candidate_mtime_changed':candidate.stat().st_mtime_ns!=first_mtime,
    'new_backups_before_existing_receipt_refusal':len(list(candidate.parent.glob('um.py.bak_*')))-first_backup_count,
    'first_receipt_unchanged':pin(OUT/'INTEGRATION_R1.json')==first_receipt})
ct=ast.parse(candidate.read_text(encoding='utf-8'))
assigns={n.targets[0].id:ast.literal_eval(n.value) for n in ct.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in {'_V394_FORMAL_CONTRACT','_V394_INSCRIPTIONS','_EMBEDDED_KERNEL_FILES','UM_VERSION'}}
new(BASE/'INTEGRATION_FIXTURE_REVIEW_R1.json',{'source':pin(SCRIPT),'fixture_only':True,'first_success':first,
    'repeat_attempt':repeat,'inscriptions_byte_roundtrip':source_verbatims,
    'candidate_version':assigns['UM_VERSION'],'expected_ladder':assigns['_V394_FORMAL_CONTRACT']['expected_ladder'],
    'article_calls_wrapped':candidate.read_text(encoding='utf-8').count('_v394_article_tex(build_')==2,
    'baseline_unchanged':(OUT/'baseline/um.py').read_text()==baseline,
    'scope':'Mock Lean manifest is for integrator mechanics only; no claim of formal verification.'})
print(json.dumps({'repeat_attempt':repeat,'verbatims':source_verbatims},ensure_ascii=False))
