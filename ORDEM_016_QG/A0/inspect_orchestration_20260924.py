"""Authorized local fallback: status and preview only; no provider execution."""
from pathlib import Path
import sys
import json
import datetime
import hashlib

base=Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
sys.path.insert(0,str(base))
from iald_orchestrator.runtime import Runtime

prompt=('ORDEM 016, A-1.b2: rascunho matemático, não execução. '
        'Se n=(1,1,0,0), A23=1, A32=-1 e demais Aij=0, '
        'T é simétrico e covariante por translações, f=T_nn e Ttilde=T+f A, '
        'com propagador Ftilde(S)=F(sym S), quais hipóteses exatas permitem '
        'transportar um contrato que só lê T_nn e F(T), mantendo carga modular '
        'e Raychaudhuri, mas violando simetria onde f não é zero? '
        'Uma resposta textual com prova condicional; não invente habitante físico nem declare gate pago. '
        'Rota permitida: MiMo para rascunho; Física somente sentido INPUT/ONTO; '
        'nenhum Claude, Codex-executor, Antigravity ou Jev. Não executar código nem alterar arquivos.')
r=Runtime(recover=False)
status=r.status()
try:preview=r.preview(prompt)
except Exception as e:preview={'error':type(e).__name__+': '+str(e)}
out=Path(__file__).resolve().parent/'orchestration_fallback_inspection.json'
assert not out.exists()
data={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'mechanism':'Runtime(recover=False).status()/preview(); authorized global CLI fallback',
      'prompt':prompt,'prompt_sha256':hashlib.sha256(prompt.encode()).hexdigest(),
      'status':status,'preview':preview,'external_model_calls':0}
raw=(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode()
tmp=out.with_suffix('.json.tmp')
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw
tmp.rename(out)
print(json.dumps({'receipt':str(out),'sha256':hashlib.sha256(raw).hexdigest(),
 'providers':status.get('providers'),'sources':status.get('sources'),
 'preview':preview},ensure_ascii=False))
