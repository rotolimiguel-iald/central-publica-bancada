"""Append the measured-degree resolution without changing the cited review."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,uuid
H=Path(__file__).resolve().parent;O=H.parents[1]/'TUNEL/DO_CHATGPT'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):
    b=v if isinstance(v,bytes) else (v if isinstance(v,str) else json.dumps(v,ensure_ascii=False,indent=2)).encode()
    if p.exists():
        old=p.read_bytes()
        if old==b:return
        bk=p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
        bk.write_bytes(old);assert bk.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
now=datetime.now(timezone.utc).isoformat();opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
r=json.loads((H/'marked_actual_degree/results.json').read_bytes())
report=f'''[REAL — grau polinomial medido; DERIVED — cobertura da auditoria anterior]
# A7.b — adendo: grau efetivo dos numeradores marcados
Abertura SHA256 `{opening}`. UTC {now}.

Responde à ressalva precisa da coordenação sobre a auditoria do Kimi:
um extrator radial que aceita grau6 não prova que o domínio auditado até
grau5 cobre todos os numeradores. Por isso o grau foi medido diretamente
nos polinômios, antes de qualquer integração UV, nas160 polarizações
da base completa, para cada uma das5 famílias.

Máximos encontrados: left_ghost5, right_ghost5, triangle5,
left_metric4 e right_metric4. Portanto a comparação independente
dos378 monômios por simplex cobre o domínio efetivamente usado.
A mutação q0^6 é rejeitada pelo critério explícito de cobertura.

{r['checks']} verificações exatas, rc0, CPU{r['cpu_seconds']}s.
Nenhuma integral de laço foi refeita. O parecer e seu cotejo anterior
permanecem intactos; este adendo elimina a dependência de uma cota
meramente inferida para o grau. A redução O(4) continua sustentada pelas
contrações covariantes e pela multilinearidade, não só pela ausência de
epsilon. Controles negativos não demonstram unicidade de toda prescrição.
Q2 curva/finita continua aberta; nenhum gate ou original alterado.
'''
rp=O/'ENTREGA_016_A7b_grau_efetivo_numeradores_marcados.md';save(rp,report)
files=[Path(__file__),rp]+[H/p for p in ['marked_actual_degree_check.py','marked_actual_degree_run.log',
    'marked_actual_degree/PRE_REGISTER.json','marked_actual_degree/results.json','marked_actual_degree/manifest.json']]
manifest=H/'marked_actual_degree/delivery_manifest.json'
save(manifest,dict(at=now,opening_sha256=opening,artifacts=[dict(path=str(p),sha256=sha(p)) for p in files]))
ledger=O/'LEDGER_016.jsonl';raw=ledger.read_bytes();marker='A7_MARKED_ACTUAL_NUMERATOR_DEGREES'
if marker.encode() not in raw:
    save(ledger,raw+(json.dumps(dict(event=marker,at=now,provider='local',target='A-7.b',checks=r['checks'],
        cpu_seconds=r['cpu_seconds'],report_sha256=sha(rp),new_external_execution=False,full_Q2=False))+'\n').encode())
cont=H/'CONTINUIDADE.json';d=json.loads(cont.read_bytes())
d.update(at=now,marked_actual_degree_manifest=str(manifest),
    pending_orchestration='5 registered/7staging per latest official coordinator message; MiMo marked_wick_audit started once',
    latest_orchestration=dict(at=now,source='Official coordinator message',registered=5,staging=7,
        currently_executing='MiMo marked_wick_audit',execution_job='ab543117-b279-407c-8d0a-6d036b234b1b',
        newly_registered_completion_mimo='9a0fd610-896a-4c31-ba92-e14c9d876330'),
    previous_goal_turn='PROGRESS')
d['completed_this_turn'].append('Actual numerator degree checked in800cases:ghost/triangle5,metric4')
save(cont,d)
progress=O/'ENTREGA_016_PROGRESSO.md'
save(progress,progress.read_bytes()+f'\n- {now} — A7.b PROGRESSO: grau real dos800numeradores cobre auditoria simplex;maxghost5,metric4,triangle5;CPU{r["cpu_seconds"]}s. Semnova chamada/integração. Abertura{opening};ledger{sha(ledger)}.\n'.encode())
for item in json.loads(manifest.read_bytes())['artifacts']:assert sha(Path(item['path']))==item['sha256']
print(json.dumps(dict(report=str(rp),artifacts=len(files))))
