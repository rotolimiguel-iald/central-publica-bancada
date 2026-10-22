"""Repeat the same review after serializing adversarial nonfinite returns explicitly.

R1's JSON encoder rejected the actual infinity returned by the tested clock.
The incomplete R1 result and its source are retained; no tested source is edited.
"""
from pathlib import Path
source=Path(__file__).with_name('review_r1.py').read_text(encoding='utf-8')
source=source.replace("if isinstance(value,np.generic):value=value.item()",
    "if isinstance(value,np.generic):value=value.item()\n        if isinstance(value,float) and not math.isfinite(value):value={'nonfinite_return':repr(value)}")
source=source.replace('RESULTADO_RUNTIME_REVIEW_R1.json','RESULTADO_RUNTIME_REVIEW_R2.json')
source=source.replace("with (HERE/'RESULTADO_RUNTIME_REVIEW_R2.json').open('x',encoding='utf-8') as f:\n    json.dump(result,f,ensure_ascii=False,indent=2,allow_nan=False,default=str)",
    "encoded=json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False,default=str)\nwith (HERE/'RESULTADO_RUNTIME_REVIEW_R2.json').open('x',encoding='utf-8') as f:\n    f.write(encoded)")
exec(compile(source,str(Path(__file__).with_name('review_r1.py'))+' [R2 serialization fix]','exec'))
