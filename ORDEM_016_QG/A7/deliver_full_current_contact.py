"""Seal finite checks, contact matrices and independent reviews without promoting Q2."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json,uuid
H=Path(__file__).resolve().parent;OUT=H.parents[1]/'TUNEL/DO_CHATGPT'
D=H/'full_current_contact_delivery';D.mkdir(exist_ok=False)
now=datetime.now(timezone.utc);stamp=now.strftime('%Y%m%d_%H%M%S_%f')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b,existing=False):
 if p.exists():
  assert existing;old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+stamp);assert not bak.exists();bak.write_bytes(old);assert bak.read_bytes()==old
 t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert b and t.read_bytes()==b;t.replace(p)
def put(p,v,existing=False):write(p,json.dumps(v,ensure_ascii=False,indent=2).encode('utf-8'),existing)
def txt(p,t):write(p,t.encode('utf-8'))
folders=['full_current_assembly_checks','assembled_current_contact_v2','opposite_endpoint_contact_independent',
 'full_current_contact_matrix','full_current_contact_matrix_swapped','current_contact_consistency','polarized_current_contact',
 'kimi_smooth_twojet_review/local_audit','mimo_source_preibp_review/local_audit_v2']
results={f:json.loads((H/f/'results.json').read_bytes()) for f in folders}
cpu=sum(v['cpu_seconds'] for v in results.values());checks=sum(v.get('checks',0) for v in results.values())
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md');ledger=OUT/'LEDGER_016.jsonl'
cost=Decimal(0);seen=set()
for line in ledger.read_text('utf-8').splitlines():
 r=json.loads(line);v=r.get('cost_estimate_usd')
 if v is None:v=r.get('cost_usd')
 if v is None:continue
 key=r.get('execution_task_id') or r.get('job_id') or r.get('request_id')
 if key and key in seen:continue
 if key:seen.add(key)
 cost+=Decimal(str(v))
pol=results['polarized_current_contact'];review=results['mimo_source_preibp_review/local_audit_v2']
report=f'''[DERIVED — montagem plana e contatos medidos; Q2 completa OPEN]

Oito controles previamente registrados, com h diagonal/não diagonal, c0..c3,
pontos não axiais e jatos exponenciais de ambos os cutoffs, cancelam exatamente
após incluir correntes emX eY. Os pesos vêm da ação/Wick e não foram ajustados.
Isso amplia a evidência; oito controles não são prova de uma identidade universal.

Na prescrição radial já fixada, R=FP[(1-a)mu^(2a)z^a], foram calculados os
contatos da correnteX com os mesmos jatos externos atéh''. Quatro polinômios
(dois tensores, dois ghosts, dois diagramas) coincidem entre tabela de C_D e
diferenciação direta do regulador. Esta segunda rota conserva apenas a parcela
linear ema PORQUE aqui os kernels são racionais com polos simples; não se
exporta essa simplificação aos logaritmos.

No controle h11,c0,q=(1,2,-1,1), a montagem de todos esses contatos dá,
para(lambda,eta)=(0,0),(0,e0),(e0-e1,e0), respectivamente:
5341/1920,48317/7680,75977/3840, em unidades deC_E=-4pi².
Os números antigos avaliados emq=(2,1,0,0) não eram o mesmo controle.
Nenhum contato não nulo foi removido por ajuste ou chamado de anomalia irremovível.

Foram calculadas as40 componentes h_A c_r paralambda=e0-e1,eta=e0 e,
separadamente, as40 com os cutoffs trocados. No primeiro conjunto, a parte
homogênea de grau5 emq recupera EXATAMENTE os três coeficientes anteriores:
a=-139/1920,b=217/960,c=99/1280 na base
delta_ab q_r q4, q_a q_b q_r q2,(delta_ar q_b+delta_br q_a)q4.
Componentes externas não diagonais recebem o peso2 da contração tensorial.
A variação BRST dessa parte é zero por igualdade polinomial nas16 entradas.
Isso reencontra a primitiva plana já existente, sem criar novo teorema por nome.

O representante localizado completo tem defeito de adjunto graduado no setor
h/c isolado. Antes da polarização, a entrada01 emq0 é697/1920; a matriz do
defeito é antiautoadjunta com o peso exp((lambda+eta)X), conferido exatamente.
Testou-se então a polarização par FIXA (A(lambda,eta)+A(eta,lambda))/2;
resultado: fechado nesse setor={pol['h_c_alone_closed']},
entradas não nulas={pol['combined_defect_nonzero_entries']},
entrada01 emq0={pol['defect_01_at_q_zero']}.
Não se escolheu sinal conforme o resultado. A próxima análise deve identificar
os termos de descida/correntes/normalização ainda necessários ANTES de atribuir
classe de cohomologia à quebra. Não se promove esse setor a Q2 completa.
Curvatura do espaço-forma, partes suaves/tadpoles, outras aridades e realização
causal/lorentziana continuam com seus escopos registrados, não presumidos pagos.

Falha operacional preservada: metric_current_insertion_engine_v2 usava int0
na soma vazia e falhava em.subs quandoeta0. V3 muda somente paraInteger(0).
Nenhum coeficiente físico mudou; comando/log falho e sucessor estão no manifesto.
O primeiro testeMiMo parou no desacordo real de resíduo;v2 preserva o desacordo
em resultado estruturado e lista os coeficientes divergentes, sem corrigi-los
para concordar com o modelo.

{checks} verificações algébricas/auditorias, além dos8 controles e80 componentes
de contato calculadas;CPU medida dos scripts concluídos={cpu}s. As contagens
incluem verificações de contraexemplos: não significam que todo parecer passou.
Custo externo conhecido parcialUS${cost}, estimado/não fatura; assinatura Kimi
sem custo alocado. Originais,um.py,kernel e gate inalterados.
Abertura sha256:{opening}.
'''
txt(D/'DERIVACAO.md',report)
txt(OUT/'ENTREGA_016_A7b_montagem_completa_plana_e_contatos.md',report)
audit=f'''[REAL + DERIVED — auditoria local dos pareceres; correções ao lado]

Kimi218c: resposta integral lida e preservada.100 verificações locais aceitam
a fórmula de multiplicação de derivadas de delta e a cota de jatos finitos.
Corrige-se §5: paraW=v, derivarW|diag.delta dá0, não delta. Na prescrição
fixada,C00=-1/4,C000=-q0/2; logoC000-q0C00=-q0/4. Não se pode substituir
o contato da linha derivada pela derivada do contato anterior. A cota máxima
só é atingida se o coeficiente superior não se anula. R comuta com suaveW
por continuação meromorfa/parte finita; a diferenciação é a operação distinta.
Não foram apagados jatos ímpares nem inferida a Ward completa dessa álgebra.

MiMo934328:448898tokens,custo estimadoUS$0.24663804 registrado UMA vez.
960 comparações de coeficientes A/B com a soma direta do vértice e2 resíduos:
{review['coefficient_failure_count']} divergências, todas na fórmula B cometa!=0;
A coincide. DeltaH/pi² emq=(2,1,0,0) é7/4, contra11/4 escrito; em(1,2,0,0)
é5/2 e coincide. O motor anterior permaneceu inalterado. Resíduo deDeltaH
sozinho não é o contato inteiro E(H); omitir um somando não mede toda a mudança.
A contração Einstein nos índicesuv comr espectador já está explícita no código:
a lacuna de contexto do parecer não reabre essa decisão. A fórmula estrutural
P-Q=-C_E(H)+E C_divB já era conferida por duas rotas na bancada.

Nenhuma chamada repetida para corrigir esses pareceres. Os sucessores da fila
trabalham em perguntas novas e independentes, com seus IDs preservados.
Evidências:A7/kimi_smooth_twojet_review/local_audit e
A7/mimo_source_preibp_review/local_audit_v2; resultados/manifestos incluem hashes.
Custo total conhecido parcialUS${cost};abertura sha256:{opening}.
'''
txt(D/'AUDITORIAS.md',audit);txt(OUT/'ENTREGA_016_A7b_auditoria_jatos_e_fonte_preIBP.md',audit)
txt(OUT/'ENTREGA_016_MEDIDA_consistencia_contato_localizado.md',f'''[REAL — defeito localizado medido, sem declaração de obstrução cohomológica]

Após todos os diagramas calculados das correntesX/Y, a parte de maior ordem
fecha no teste BRST. A parte localizada não fecha no setor h/c isolado.
Polarização simétrica dos cutoffs:fechado={pol['h_c_alone_closed']};
entrada01 emq0={pol['defect_01_at_q_zero']},entradas não nulas={pol['combined_defect_nonzero_entries']}.
Comando:A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/polarized_current_contact_check.py.
rc0;logsha256={sha(H/'polarized_current_contact_run.log')}.
Próximo: rastrear a descida das correntes/normalização no mesmo representante,
sem inventar classe de anomalia nem ajustar a matriz. A7b termina20:32UTC.
Custo parcialUS${cost};abertura sha256:{opening}.
''')
scripts=['full_current_assembly_checks.py','opposite_endpoint_contact_engine.py','assembled_current_contact_check_v2.py',
 'opposite_endpoint_contact_independent_check.py','full_current_contact_matrix.py','full_current_contact_matrix_swapped.py',
 'current_contact_consistency_check.py','polarized_current_contact_check.py','audit_kimi_smooth_twojet.py',
 'audit_mimo_source_preibp.py','audit_mimo_source_preibp_v2.py','metric_current_insertion_engine_v3.py',
 'metric_current_zero_case_conversion.json','receive_mimo_source_preibp.py']
logs=['full_current_assembly_checks_run.log','assembled_current_contact_run.log','assembled_current_contact_run_v2.log',
 'opposite_endpoint_contact_independent_run.log','full_current_contact_matrix_run.log','full_current_contact_matrix_swapped_run.log',
 'current_contact_consistency_run.log','polarized_current_contact_run.log','audit_kimi_smooth_twojet_run.log',
 'audit_mimo_source_preibp_run.log','audit_mimo_source_preibp_run_v2.log']
files=[Path(__file__),D/'DERIVACAO.md',D/'AUDITORIAS.md']+[H/f for f in scripts+logs]
for f in folders:files.extend([H/f/'results.json',H/f/'manifest.json'])
put(D/'manifest.json',dict(at=now.isoformat(),opening_sha256=opening,checks=checks,off_diagonal_controls=8,
 contact_components=80,cpu_seconds=cpu,known_partial_usd=str(cost),full_Q2=False,gate_changed=False,
 artifacts=[dict(path=str(p),sha256=sha(p)) for p in files]))
event=dict(at=now.isoformat(),event='FULL_CURRENT_CONTACT_AND_MODEL_AUDITS',target='A7.b',checks=checks,
 off_diagonal_controls=8,contact_components=80,cpu_seconds=cpu,remote_call=False,manifest_sha256=sha(D/'manifest.json'))
write(ledger,ledger.read_bytes()+(json.dumps(event)+'\n').encode(),True)
cont=H/'CONTINUIDADE.json';v=json.loads(cont.read_bytes());elapsed=(now-datetime.fromisoformat(v['at'])).total_seconds()/3600
v.update(at=now.isoformat(),previous_goal_turn='PROGRESS',own_live_processes=[],
 full_current_contact_manifest=str(D/'manifest.json'),metric_current_active_engine=str(H/'metric_current_insertion_engine_v3.py'),
 pending_scientific_review=None,kimi_smooth_twojet_audit=str(H/'kimi_smooth_twojet_review/local_audit/manifest.json'),
 mimo_source_preibp_audit=str(H/'mimo_source_preibp_review/local_audit_v2/manifest.json'),
 scientific_partial_metered_cost_usd=str(cost),
 completed_this_turn=['8/8 expanded off-diagonal assembly controls zero',
 'CurrentX contact independently verified by regulator differentiation',
 '80 localized contact components; highest-order bulk WZ zero',
 'Localized h/c WZ and symmetric cutoff polarization measured without coefficient fitting',
 'Kimi/MiMo opinions audited and errors retained; no engine changes to conform with them'],
 next=['Trace classical-current descent and remaining normalization terms in localized Ward; preserve measured nonzero matrix',
 'Do not conflate partial h/c contact with fullQ2 or assign an obstruction class before consistency',
 'Retain other curved/smooth/tadpole/higher-arity work and branch deadline20:32UTC',
 'Audit newly completed FIFO reviews; no retries or blind context contamination',
 'A7c/d,A8,ORDEM015PartB and final requirement audit remain'])
put(cont,v,True)
progress=OUT/'ENTREGA_016_PROGRESSO.md'
write(progress,progress.read_bytes()+f'\r\n- {now.isoformat()} A7.b PROGRESS/MEDIDA:8/8zeros fora diagonal;80componentes locais;{checks}checks;CPU{cpu}s;bancada{elapsed:.6f}h;WZbulk fecha,localização medida;parcialUS${cost};Q2 OPEN.\r\n'.encode(),True)
for item in json.loads((D/'manifest.json').read_bytes())['artifacts']:assert sha(Path(item['path']))==item['sha256']
print(json.dumps(dict(manifest=str(D/'manifest.json'),checks=checks,cpu_seconds=cpu,known_partial_usd=str(cost),verified_artifacts=len(files))))
