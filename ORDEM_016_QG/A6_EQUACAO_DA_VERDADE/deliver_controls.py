from pathlib import Path
from datetime import datetime, timezone
import hashlib, importlib.util, json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
C=HERE/'C_controles'
OUT=ROOT.parent/'TUNEL/DO_CHATGPT'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):
    raw=v if isinstance(v,bytes) else (v.encode('utf-8') if isinstance(v,str) else json.dumps(v,ensure_ascii=False,indent=2).encode('utf-8'))
    stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    if p.exists():
        old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+stamp);bak.write_bytes(old)
        assert bak.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp_'+stamp);tmp.write_bytes(raw)
    assert tmp.read_bytes()==raw and raw
    tmp.replace(p)
spec=importlib.util.spec_from_file_location('audit',ROOT/'A0/auditar_axiomas.py')
audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
units=[]
for filename,label in [('TheEquationOfTruth_T20_controles_v3.lean','negative_controls_03'),
                       ('NegativeControlsCompleteness_v2.lean','negative_completeness_02')]:
    source=C/filename;log=C/(label+'.log');r=json.loads((C/(label+'.json')).read_bytes())
    assert r['rc']==0 and r['source_sha256']==sha(source) and r['log_sha256']==sha(log)
    assert not r['newer_kernel_files'] and not r['scan_errors']
    a=audit.audita(str(source),str(log));assert a['auditoria']=='PASSA',a
    save(C/(label+'_audit.json'),a)
    units.append(dict(source=str(source),source_sha256=sha(source),receipt=r,audit=a))
mutations=json.loads((C/'mutations/results.json').read_bytes())
assert mutations['detected']==8
for entry in mutations['results']:
    p=Path(entry['generated']['source']);r=entry['receipt'];log=p.parent/('mutation_'+entry['id']+'.log')
    assert sha(p)==r['source_sha256'] and sha(log)==r['log_sha256']
    assert not r['newer_kernel_files'] and not r['scan_errors']
    assert entry['detected'] and entry['audit']['auditoria']=='FALHA'
attempts=[json.loads((C/(label+'.json')).read_bytes()) for label in
    ['negative_controls_01','negative_controls_02','negative_controls_03','negative_completeness_01','negative_completeness_02']]
attempts += [e['receipt'] for e in mutations['results']]
groups=[
  ('C1.1','Projeção oblíqua','P²=P e HP=0, mas PH≠0 e P exp(−sH)≠P para s>0.'),
  ('C1.2','Gerador não autoadjunto','P ortogonal seleciona ker H; H nilpotente não simétrico e PH≠0.'),
  ('C1.3','Sem positividade','H=−I: sem limite zero; diag(3,−3): produto contínuo conservado sem fatoração.'),
  ('C1.4','Leitor descontínuo','Indicador da segunda coordenada é conservado, não fatora e não é contínuo.'),
  ('C1.5','Leitor constante','Conservação para qualquer fluxo e falha de distinção de identidades.'),
  ('C1.6','Fora dos bits','truthValue(2,0)=−3 não pertence a {0,1}.'),
  ('C1.7','Poda incompatível','Reuso do controle H=0, H′=I: a leitura anterior não é conservada.'),
  ('C1.8','Penalidade assinada','id†id−id†id=0 tem núcleo total; interseção dos núcleos é zero.'),
  ('C1.9','Qubit inválido','Traço 1, determinante −11/100 e testemunha quadrática negativa: não PosSemidef.')]
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
now=datetime.now(timezone.utc)
count=sum(e['audit']['n_theorem_lemma_na_fonte'] for e in units)
m=dict(status='REAL_C1_C2_SCOPED',at=now.isoformat(),opening_sha256=opening,
       groups=groups,group_count=len(groups),new_theorems=count,units=units,
       mutation_results=str(C/'mutations/results.json'),mutation_results_sha256=sha(C/'mutations/results.json'),
       detected=mutations['detected'],attempts=attempts,
       wall_seconds=sum(r['wall_seconds'] for r in attempts),
       cpu_seconds=sum(r['cpu_user_seconds']+r['cpu_kernel_seconds'] for r in attempts),gate_changed=False)
save(C/'controls_manifest.json',m)
lines=['[REAL — controles compilados e mutações detectadas; nenhum resultado físico inferido]',
       '', '# A6.C — controles das hipóteses e do auditor', '',f'Abertura SHA256: `{opening}`.', '',
       f'C1 PAGO: {len(groups)} grupos, {count} theorem/lemma locais compilados com rc0 e auditados no trio. '
       'C2 PAGO: oito mutações geradas por substituição exata, hashes conferidos com a referência, compiladas e recusadas pelo auditor.', '',
       '| Controle | Hipótese/objeto | Resultado |','|---|---|---|']
for row in groups: lines.append('| '+' | '.join(row)+' |')
lines += ['', '| Mutação | rc Lean | Auditor | Detectada |','|---|---:|---|---|']
for x in mutations['results']:
    lines.append(f"| {x['id']} | {x['receipt']['rc']} | {x['audit']['auditoria']} | {x['detected']} |")
lines += ['', 'M1–M5 falham na compilação. M6, M7a e M7b compilam, mas são recusados por sorry, axioma novo e cobertura ausente, respectivamente. '
          'Esses arquivos intencionalmente inválidos ficam apenas como controles, separados das fontes aprovadas.', '',
          'Cinco tentativas dos controles preservadas: três da base e duas do complemento. A última correção do complemento '
          'explicita a ordem parcial complexa para que a desigualdade 1/5≤0 produza a contradição. '
          'Todos os enunciados aprovados foram relidos; fluxos exponenciais estão vinculados às matrizes geradoras.', '',
          f'Máquina: {m["wall_seconds"]:.6f}s de parede somados por processo, {m["cpu_seconds"]:.6f}s CPU. '
          'Processos paralelos impedem interpretar a soma como duração cronológica. Nenhuma escrita detectada no kernel.', '',
          'Escopo: auditoria das fontes e dos logs locais; não substitui auditoria transitiva completa dos imports. '
          'Originais, um.py e gate não alterados. Próximo ramo: D1/D2. Integração monolítica continua pendente.', '',
          f'Manifesto: `{C/"controls_manifest.json"}`.']
save(OUT/'ENTREGA_016_A6_C_controles.md','\n'.join(lines)+'\n')
ledger=OUT/'LEDGER_016.jsonl';old=ledger.read_bytes();events=[]
marker='A6_C_CONTROLS_20260924'
if marker.encode() not in old:
    events.append(dict(event=marker,at=now.isoformat(),manifest=str(C/'controls_manifest.json'),manifest_sha256=sha(C/'controls_manifest.json'),
                       wall_seconds=m['wall_seconds'],cpu_seconds=m['cpu_seconds'],external_execution=False))
for u in json.loads((HERE/'orchestration_reviews/prepared_units.json').read_bytes()):
    if u['request_id'].encode() not in old:
        events.append(dict(event='unit_staged_by_coordinator',at=now.isoformat(),**u,
             confirmed_status='STAGED_CAPACITY_PENDING',external_execution=False,tokens=None,cost_estimate_usd=None,
             source_thread_id='01a0ce2b-8c2f-71b0-a9a8-91b17715a569'))
if events: save(ledger,old+b''.join((json.dumps(e,ensure_ascii=False)+'\n').encode('utf-8') for e in events))
rows=[json.loads(l) for l in ledger.read_text(encoding='utf-8-sig').splitlines() if l.strip()]
priced={}
for row in rows:
    cost=next((row.get(k) for k in ('cost_estimate_usd','cost_usd','custo_usd') if isinstance(row.get(k),(int,float))),None)
    if cost is not None:
        key=row.get('execution_id') or row.get('job_id') or row.get('request_id')
        if key: priced[key]=cost
cost=sum(priced.values())
progress=OUT/'ENTREGA_016_PROGRESSO.md';old=progress.read_bytes()
if marker.encode() not in old:
    line=f'\n- {now.isoformat()} — A6.C PAGO: {count} lemas auditados/9 grupos; 8/8 mutações detectadas. Máquina {m["wall_seconds"]/3600:.6f}h parede somada/{m["cpu_seconds"]/3600:.6f}h CPU; bancada não exclusiva. Custos explícitos US${cost:.10f}, incompletos. Mais 3 unidades em staging Kimi/MiMo/DeepSeek; sem nova execução local de provedor. Abertura {opening}. Não move gate; próximo D1/D2. [{marker}]\n'
    save(progress,old+line.encode())
print(json.dumps(dict(status=m['status'],new_theorems=count,mutations=8,wall_seconds=m['wall_seconds'],priced_cost_incomplete=cost)))
