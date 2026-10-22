"""Documentary candidate only. --verify and --inspect are strictly read-only.

Standard library only; never imports production, evaluates source, loads arrays,
starts subprocesses, contacts the network or resumes historical jobs.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, re, sys

HERE=Path(__file__).resolve().parent
B=HERE.parents[1]
R=B.parent
D=R/'TUNEL/DO_CHATGPT'
AUD=R/'TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/auditoria_da_gerencia/aud_5_protocolo.txt'
ORDER=R/'TUNEL/PARA_CHATGPT/ORDEM_013BIS_fechamento_e_ampliacao_dos_eventos_ate_5sigma.md'
PREFIX='ENTREGA_013_'
SPECS=[
 dict(id='C6a',name='C6a_REGISTRO_TOEPLITZ',receipt='REGISTRO_C6.json',marco='M5',
      paid='PAGO documental: registro NÃO-CEGO identificado; parâmetros/prior/janelas fixados e hash conferido. Declaração de registro não é resultado físico.',
      unpaid='NÃO PAGO naquela nota: análise do strain, calibração e equivalência pyRing. Hoje M5 reclassifica a execução posterior como C6-pre, pré-portão e não calibrada; a guarda original não cobre todos os runners/fetches.',
      anchors=[(3,18)], failures='Calibração IMR já declarada reprovada em :12. Ausência de posterior pyRing em 10,5 tM em :16 é lacuna, não teste passado.'),
 dict(id='C4c',name='C4c_C5_C6_strain_registrado',receipt='C6_RESULTS.json',marco='M2/M4/M5',
      paid='PAGO documental: rodada registrada e razões condicionais históricas localizadas. Os valores e o erro de quadratura são transportados dos JSON existentes, sem reler strain ou refazer inferência.',
      unpaid='NÃO PAGO científico: calibração das duas famílias, significância física, reprodução de posterior pyRing/rede coerente. Listas de próximas ações de :29–37 são históricas, não ordens vigentes.',
      anchors=[(3,27),(29,37),(39,68)],failures='Três tentativas de ruído numericamente instáveis declaradas em :21; backups RAW_COVARIANCE, DIFFERENCING e FULL_RATE_SPECTRAL localizados e hashados. Reprovação de calibração em :19,23,35 preservada.'),
 dict(id='C5_auditoria',name='C5_auditoria_integracao_fonte',receipt='C5_SOURCE_EVIDENCE_AUDIT_SUMMARY.json',marco='M4',
      paid='PAGO documental: piloto sem convergência, ESS insuficiente, auditoria aritmética/taxa e dois controles de integração localizados. Consta 0/1200 com precisão na rodada adaptada e discrepância 0,3987631086 entre sementes do oráculo balanceado.',
      unpaid='NÃO PAGO científico: convergência/precisão integral, repetição e calibração contínua. A aceitação de somas ou taxa não paga os critérios estatísticos nem a identificação astrofísica.',
      anchors=[(7,44),(46,71),(73,104)],failures='Falhas import_order_failed_bytes e numpy_bool_failed_bytes preservadas; resultado estatístico reprovado permanece, sem rerun.'),
 dict(id='C5_mistura',name='C5_mistura_das_familias_preparada',receipt='C5_FAMILY_MIXTURE_PREPARATION.json',marco='M4',
      paid='PAGO documental: método e registro de mistura com pesos 1/2 por família; controle analítico de 4.000 repetições e recusa de rodada incompleta. Mistura de evidências não é média dos ln B.',
      unpaid='NÃO PAGO naquela etapa: integrações concluídas e aceitas, precisão de componentes e calibração astrofísica. Implementar/registrar mistura não apaga reprovações nem autoriza executar os comandos históricos.',
      anchors=[(5,40),(42,54)],failures='Quatro entradas inválidas e recusa de consumidor incompleto declaradas em :22–24; resultado do validador e registro preservados. Código de saída histórico não foi reproduzido agora.'),
 dict(id='C5_SEOB',name='C5_piloto_SEOB_e_repeticao_registrada',receipt='C5_SEOB_PILOT_AND_REPEAT_REGISTRATION.json',marco='M4',
      paid='PAGO documental: piloto 2.048/1.024, auditoria de densidade e somas, 52 alternativas de proposta recusadas; repetição 16.384/seed130942 registrada, ainda não iniciada no instante da nota.',
      unpaid='NÃO PAGO científico: precisão 0/1200, calibração e repetição aceita. Controle de taxa ainda pendente naquela nota; resultados posteriores não se retrodatam. Texto Milburn complementar não é leitura do artigo original de 1991.',
      anchors=[(5,49),(51,72)],failures='Piloto sem precisão e 52 adaptações recusadas preservados nos resultados. Falhas bibliográficas originais declaradas em :39–42 não são apagadas pelo HTML complementar.'),
 dict(id='C5_interpolacao',name='C5_recuperacao_da_interpolacao_real',receipt='C5_REAL_PHASE_RECOVERY.json',marco='M4',
      paid='PAGO documental: falha original no índice15627, diagnóstico Nyquist, correção real validada e continuação registrada em diretório distinto. Recibo registra 8.128 preservados +32 recuperados +394 restantes =8.554 válidos, denominador16.384.',
      unpaid='NÃO PAGO: máximos exatos dos controles de 8.128 pontos antigos (só RAM), precisão integral e calibração. Continuação em execução às 09:18 não equivale a resultado final às 09:18.',
      anchors=[(5,47),(49,62)],failures='Rodada Phenom original falhou; primeiro oráculo corrigido falhou por broadcasting. Diagnóstico, validador original e registro permanecem; ausência de RESULT.json original é conferida sem criar saída.'),
 dict(id='C5_piloto_real',name='C5_piloto_real_concluido_e_refinamento',receipt='C5_COMPLETED_REAL_PHASE_PILOT.json',marco='M4',
      paid='PAGO documental: 16.384 propostas contabilizadas, 8.554 vetores e 7.830 zeros; auditorias aritméticas e 512/1200 na precisão local. Adendo de 09:35 registra controle SEOB de 196 pontos, não resultado anterior.',
      unpaid='NÃO PAGO: 688 conjuntos sem precisão; 120 diferenças de ln B >0,2 e máximo≈0,911183; controle global do posterior e calibração. Proposta32.768 estava só registrada na nota base, não executada.',
      anchors=[(5,55),(59,61)],failures='Original62818 preservado como falho. Limitação dos 8.128 controles não recuperados persiste. Backup anterior ao adendo de 09:35 é hashado e preservado.'),
 dict(id='C5_refinamento',name='C5_refinamento_iniciado_e_api_continua',receipt='C5_REAL_REFINEMENT_START.json',marco='M4',
      paid='PAGO documental: controle Phenom347 pontos, API60 verificações e igualdade dos extremos nos pontos testados; início32.768/seed130972 e instantâneo576 vetores documentados. API validada não é integral concluída.',
      unpaid='NÃO PAGO: precisão integral, Z(a) marginalizado completo, posterior/calibração de intensidade contínua. Sessões citadas são handles históricos, não PIDs nem prova de processos vivos hoje.',
      anchors=[(5,27),(29,44)],failures='Limites de precisão e falhas anteriores continuam ditos em :29–44. Não se herda para novos pontos o controle de resolução dos pontos antigos; intensidade negativa é extensão diagnóstica, não GKLS físico.'),
 dict(id='C4a_ADITIVA',name='C4a_REGISTRO_POSTERIORES',receipt='REGISTRO_C4.json',marco='M2',additive=True,
      paid='PAGO documental: registro de limiar100/95%, priors e identidade de integrais com nuisance comum; cronologia própria e hash conferidos. Acrescenta-se axiomas N/A e teoremas0, ausentes na nota.',
      unpaid='NÃO PAGO naquela nota: inferência em posterior, controles de PSD/injeções/strain. A emissão M2 posterior não converte C4a em fechamento M1 nem torna cega a seleção posterior.',
      anchors=[(1,20)],failures='Nenhuma tentativa computacional falha específica é documentada nesta nota de registro; isso não certifica ausência de falhas em toda a C4.')]
MFILES={
 'M1':'ENTREGA_013_M1_fechamento.md','M2':'ENTREGA_013_M2_C4_fechamento.md',
 'M3':'ENTREGA_013_M3_C3_2_C2_RMOD.md','M4':'ENTREGA_013_M4_C5_parede_e_portao.md','M5':'ENTREGA_013_M5_C6pre.md'}
MSTATE={
 'M1':('9–25','Fechamento documental/controles condicionais. C0, C1 e C2 com lacunas; calibração IMR, estado físico e cronologia primária não se presumem pagos.'),
 'M2':('7–21','C4 NÃO-CEGA, catálogo INCONCLUSIVE_SYSTEMATICS; RD sem 220 livre; GWTC4 localizado sem joint utilizável demonstrado; relógio livre sem corte sustentado. Não reafirma inexistência de release.'),
 'M3':('7–20','Template/oráculo e paredes R-MOD/R-PROP; gerador quadrático postulado, H(z) como entrada, sem ponte física fechada.'),
 'M4':('9–18,30–36','C5 fecha como PAREDE MEDIDA; calibração FULL_IMR reprovada, rigor assimétrico dito; não reabrir campanha. Registros de início antigos não revogam essa parada.'),
 'M5':('5–17,32','C6-pre NÃO-CEGA e não calibrada; sigma/z null, rede coerente/atraso/pyRing não pagos. Registro antes do strain não é aprovação prévia do portão.')}
PRIMARY={
 'C5_auditoria':[
  ('cache/source_evidence/importance_runs/IMRPhenomXPHM_adapted_130701_seed130707_N16384/RESULT.json',
   ['status','draws','evaluations','all_precision_pass','draws_passing_precision','scientific_acceptance']),
  ('cache/source_evidence/importance_runs/IMRPhenomXPHM_adapted_130701_seed130707_N16384/AUDIT.json',['status','scientific_acceptance'])],
 'C5_mistura':[
  ('cache/source_evidence/source_family_mixture_validation/RESULT.json',
   ['status','empirical_over_predicted_variance','constant_likelihood_correct_MC_sd','invalid_inputs_refused','low_ESS_refused','scientific_acceptance'])],
 'C5_SEOB':[
  ('cache/source_evidence/phase_native_seob/SEOBNRv4HM_seed130901_N2048/RESULT.json',
   ['status','draws','evaluations','all_precision_pass','draws_passing_precision','scientific_acceptance'])],
 'C5_interpolacao':[
  ('cache/source_evidence/real_phase_adapter_validation/ORACLE_FAILURE_DIAGNOSIS.json',
   ['status','original_error','corrected_error','corrected_vs_squeezed_error']),
  ('cache/source_evidence/real_phase_adapter_validation_corrected/RESULT.json',
   ['status','failed_point_recovered','full_wave_or_quadrature_tolerance_relaxed','scientific_acceptance'])],
 'C5_piloto_real':[
  ('cache/source_evidence/phase_ringdown_real_continuation/IMRPhenomXPHM_seed130892_N16384/RESULT.json',
   ['status','draws','evaluations','all_precision_pass','draws_passing_precision','scientific_acceptance']),
  ('cache/source_evidence/phase_ringdown_real_continuation/IMRPhenomXPHM_seed130892_N16384/PROPOSAL_COMPARISON.json',
   ['status','old_draws','new_draws','old_passing','new_passing','max_abs_lnB_change','changes_over_point2']),
  ('C5_SEOB_RATE_COMPLETION.json',['date_utc','status','points','maximum','limit','scientific_acceptance'])],
 'C5_refinamento':[
  ('cache/source_evidence/continuous_real_phase_validation/RESULT.json',
   ['status','direct_full_wave_controls','max_relative_wave_error','max_direct_logL_error','coverage_completed','scientific_acceptance']),
  ('cache/source_evidence/phase_ringdown_real_continuation/IMRPhenomXPHM_seed130892_N16384/real_rate_control/RESULT.json',
   ['status','max_active_logL_change','scientific_acceptance'])]}

def safe_path(p):
    p=Path(p).resolve()
    if not p.is_relative_to(R.resolve()):raise ValueError('Outside authorized root: '+str(p))
    low=p.name.lower()
    if low in {'.env','iald_stack_v7.py','iald_psion_state.json','um.py'} or any(x in low for x in ('token','password','credential')):
        raise ValueError('Sensitive or excluded file: '+str(p))
    if p.suffix.lower() in {'.h5','.hdf5','.gwf','.pkl','.pickle'}:raise ValueError('Raw data out of documentary scope: '+str(p))
    return p
def sha(p):
    p=safe_path(p);h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1048576),b''):h.update(block)
    return h.hexdigest()
def rel(p):return safe_path(p).relative_to(R.resolve()).as_posix()
def txt(p):return safe_path(p).read_text(encoding='utf-8-sig')
def js(p):return json.loads(txt(p))
def norm(name):
    name=name.strip('` <>').replace('\\','/')
    for prefix in ['/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/',str(B).replace('\\','/')+'/']:
        if name.startswith(prefix):name=name[len(prefix):]
    return safe_path(B/name)
def read_span(p,first,last):
    return '\n'.join(txt(p).split('\n')[first-1:last])
def key_line(p,key):
    needle=json.dumps(key,ensure_ascii=False)+':'
    return next((i for i,s in enumerate(txt(p).split('\n'),1) if needle in s),None)
def explicit_refs(p):
    refs=[]
    for ln,line in enumerate(txt(p).split('\n'),1):
        pins=re.findall(r'\b[a-fA-F0-9]{64}\b',line)
        if not pins:continue
        names=re.findall(r'`([^`]+)`',line)
        candidates=[n for n in names if not re.fullmatch(r'[a-fA-F0-9]{64}',n)]
        if not candidates and line.startswith('|'):
            cells=line.split('|');candidates=[cells[1].strip()] if len(cells)>2 else []
        if candidates and re.search(r'\.(?:json|py|md|npz|html|txt|failed_bytes)',candidates[0]):
            refs.append((norm(candidates[0]),pins[-1].lower(),ln))
    return refs
def snapshot(p):
    p=safe_path(p)
    if not p.exists():return {'path':rel(p),'exists':False,'sha256':None,'bytes':None}
    stat=p.stat();return {'path':rel(p),'exists':True,'sha256':sha(p),'bytes':stat.st_size}
def collect():
    files={};checks=[];notes=[];texts={};primary={}
    def add(p):
        p=safe_path(p);k=rel(p)
        if k not in files:files[k]=snapshot(p)
        return files[k]
    def check(p,expected,origin,locator):
        item=add(p);matches=[]
        if item['sha256']!=expected:
            # Only sibling backups of this exact filename, no broad filesystem search.
            for q in sorted(p.parent.glob(p.name+'.bak*')):
                if q.is_file() and sha(q)==expected:add(q);matches.append(rel(q))
        checks.append({'path':rel(p),'expected_sha256':expected,'actual_sha256':item['sha256'],
                       'match':item['sha256']==expected,'origin':rel(origin),'locator':locator,
                       'matching_sibling_backups':matches})
    for p in [AUD,ORDER,R/'TUNEL/TUNEL_PROTOCOLO.md',D/'ENTREGA_013BIS_ABERTURA_operador.md',Path(__file__),
              B/'REAPROVEITAMENTO_C5.md',B/'REAPROVEITAMENTO_C6_v2.md',B/'C5_SEOB_RATE_COMPLETION.json']:
        add(p)
    for spec in SPECS:
        note=D/(PREFIX+spec['name']+'.md');row=add(note)
        if not row['exists']:raise FileNotFoundError(note)
        content=txt(note);dates=re.findall(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?[+-]\d\d:\d\d',content)
        rec=B/spec['receipt'];add(rec);obj=js(rec)
        notes.append({**spec,'path':rel(note),'sha256':row['sha256'],'dates_as_written':dates,
                      'receipt':rel(rec),'receipt_sha256':sha(rec),'receipt_date_as_written':obj.get('date_utc',obj.get('created_utc',obj.get('date'))),
                      'receipt_status':obj.get('status'),'axioms':'N/A — sem Lean','new_theorems':0})
        if spec['id'] in ('C6a','C4a_ADITIVA'):
            pin=re.search(r'SHA256:\s*`([a-f0-9]{64})`',content)[1];check(rec,pin,note,'SHA256')
        for p,pin,ln in explicit_refs(note):check(p,pin,note,'line '+str(ln))
        if spec['receipt'].startswith('C5_'):
            for name,pin in obj.get('hashes',{}).items():
                if re.fullmatch(r'[a-f0-9]{64}',str(pin)):check(norm(name),pin,rec,'hashes/'+name)
        keys=['status','date_utc','scientific_acceptance','passing_datasets','draws','evaluations','local_precision_pass',
              'required_datasets','old_local_precision_pass','changes_over_point2','max_abs_lnB_change','arithmetic_error_max',
              'balanced_toy_seed_lnB_difference','independent_toy_lnB_max_error','pilot_draws','pilot_valid',
              'rejected_adaptive_proposals','original_saved','replay_recovered','remaining_at_start','total_proposals',
              'valid_proposals','failed_source_index','phenom_rate_points','phenom_rate_max_logL_change',
              'fresh_run_draws','fresh_run_seed','checkpoint_points_verified','coverage_completed','metadata_limitation']
        texts[rel(rec)]={k:{'value':obj[k],'line':key_line(rec,k)} for k in keys if k in obj}
        primary[spec['id']]=[]
        for name,keys in PRIMARY.get(spec['id'],[]):
            p=B/name;add(p);data=js(p)
            primary[spec['id']].append({'path':rel(p),'sha256':sha(p),
                'fields':{k:{'value':data[k],'line':key_line(p,k)} for k in keys if k in data}})
    for path in sorted(B.glob('prepare_empirical_noise.py.bak*')):add(path)
    for path in D.glob('ENTREGA_013_C5_piloto_real_concluido_e_refinamento.md.bak*'):add(path)
    extra=[B/'C6_DOWNLOADS.json',B/'cache/source_evidence/real_phase_adapter_validation/ORACLE_FAILURE_DIAGNOSIS.json',
           B/'cache/source_evidence/phase_ringdown_balanced/IMRPhenomXPHM_seed130892_N16384/RESULT.json']
    for p in extra:add(p)
    markers={}
    for k,name in MFILES.items():
        p=D/name;add(p);markers[k]={'path':rel(p),'sha256':sha(p),'lines':MSTATE[k][0],
                                   'current_documented_scope':MSTATE[k][1],'first_line':txt(p).split('\n')[0]}
    # JSON summaries were read, source code/binaries were hashed only unless
    # quoted above; no claim of independent numerical rerun.
    return {'schema':1,'status':'CANDIDATE_DOCUMENTARY_ERRATA__NOT_FORMAL_DELIVERY',
      'generated_utc':datetime.now(timezone.utc).isoformat(),'root_windows':str(R),'notes':notes,
      'eight_targets':8,'ninth_additive':1,'files':list(files.values()),'historical_hash_checks':checks,
      'read_json_fields':texts,'primary_evidence':primary,'current_M1_M5':markers,
      'scope':'Hashes and documentary source locators only; no C5/PE/strain/code execution or liveness polling',
      'not_claimed':'No retroactive receipt, no physical acceptance, no completion of all F7',
      'files_written':['ORDEM_013_RINGDOWN/bis/contract_errata/contract_errata.py',
                       'ORDEM_013_RINGDOWN/bis/contract_errata/CANDIDATE.md',
                       'ORDEM_013_RINGDOWN/bis/contract_errata/MANIFEST.json']}

def render(m):
    lines=['[REAL — errata documental candidata; NÃO-CEGA; OPEN nos itens científicos não pagos]',
     '', '# F7 — candidata de errata contratual: oito alvos e nona aditiva', '',
     'Data desta verificação: '+m['generated_utc']+'. Raiz dos localizadores: `C:\\IALD\\Central de Patentes\\Chatgpt`. Nenhuma nota original, fonte, memória ou pacote foi alterado. Este arquivo **não é** `ENTREGA_013_ERRATA_contrato.md`; sua emissão formal cabe ao construtor após leitura.', '',
     'Base: `TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/auditoria_da_gerencia/aud_5_protocolo.txt:40,65–68`; `ORDEM_013BIS_fechamento_e_ampliacao_dos_eventos_ate_5sigma.md:113–121,247` na mesma via. Contrato: `TUNEL/TUNEL_PROTOCOLO.md:47–63`. As lacunas de PAGO/NÃO PAGO das oito notas são supridas abaixo; C4a é **nona aditiva**, apenas por não declarar axiomas explicitamente.', '',
     '**PAGO nesta candidata:** estatuto, disposição por nota, fontes e hashes lidos, comando somente leitura, axiomas N/A, teoremas novos 0, falhas/limitações e estado posterior M1–M5. **NÃO PAGO por esta candidata:** emissão formal no túnel, recibo da gerência, auditoria física dos resultados, integralidade de F7 (limpeza/licenças/fichas/emendas são outras frentes), calibração ou retomada de C5.', '',
     '“PAGO documental” significa que o campo faltante é preenchido com evidência e alcance. Não significa que uma falha científica passou. Números históricos são lidos/transcritos de recibos; não reobtidos por PE. SHA confirma bytes, não a interpretação física. Os `--verify` dos builders antigos e os comandos de jobs citados nas notas **não foram executados**.', '',
     '## As oito notas e a aditiva', '']
    for n in m['notes']:
        lines += ['### '+n['id']+(' — nona aditiva, fora dos oito alvos' if n.get('additive') else ' — alvo'),'',
         f'Nota integral lida: `{n["path"]}`; SHA256 `{n["sha256"]}`.',
         f'Localizadores da nota: '+', '.join(f':{a}–{z}' for a,z in n['anchors'])+'.',
         f'Cronologia citada na nota, sem inferência de mtime: `{n["dates_as_written"]}`. Recibo: `{n["receipt"]}`; SHA256 `{n["receipt_sha256"]}`; data literal `{n["receipt_date_as_written"]}`; status `{n["receipt_status"]}`.', '',
         '- **[REAL documental] '+n['paid']+'**',
         '- **[OPEN] '+n['unpaid']+'**',
         '- **Falhas preservadas / alcance de leitura:** '+n['failures'],
         '- **Estado documental posterior:** '+n['marco']+'; consultar a matriz M1–M5 abaixo. Nenhum handle histórico é consultado ou reativado.',
         '- **Axiomas:** N/A — sem Lean. **Teoremas novos nesta errata:** 0. Sem fonte Lean ou compilação declarada; isso não apaga teoremas eventualmente citados em outras frentes.',
         '- **Reprodução documental:** o comando único `--verify` abaixo confere esta nota, suas fontes selecionadas e a candidata. Não refaz a ciência nem executa o script histórico.', '']
        fields=m['read_json_fields'].get(n['receipt'],{})
        if fields:
            lines += ['Campos reconsultados do recibo (linha e chave):','', '| Localizador | Valor lido |','|---|---|']
            for key,v in fields.items():
                val=json.dumps(v['value'],ensure_ascii=False).replace('|','\\|')
                lines.append(f'| `{n["receipt"]}:{v["line"]}` — `{key}` | {val} |')
            lines.append('')
        for evidence in m['primary_evidence'][n['id']]:
            lines += [f'Fonte de resultado/diagnóstico relida: `{evidence["path"]}`; SHA256 `{evidence["sha256"]}`.', '',
                      '| Localizador | Valor lido |','|---|---|']
            for key,v in evidence['fields'].items():
                val=json.dumps(v['value'],ensure_ascii=False).replace('|','\\|')
                lines.append(f'| `{evidence["path"]}:{v["line"]}` — `{key}` | {val} |')
            lines.append('')
    lines += ['## Cronologia preservada e estado documental de hoje','',
     'Os horários são os escritos nas notas/recibos. Quando um JSON usa `-03:00` e a nota usa `+00:00`, preservam-se ambas as representações; não se altera o instante nem se usa mtime como data de evento. C4a traz 23:05:47Z na nota; a referência do auditor a 20:02 local diz respeito ao registro anterior, não autoriza trocar o horário da nota.', '',
     'C6a/REGISTRO_C6 declara 00:56:31.808127Z; `C6_DOWNLOADS.json` registra H1 00:57:32.538104Z e L1 00:57:39.575154Z. São carimbos de registro/download arquivados, não nova observação do instante da primeira leitura. O auditor registra sua checagem histórica; esta errata não a reexecuta. M5 corrige o alcance: antes do strain não significa depois de um portão aprovado. O item 36 do auditor não substitui essa correção posterior.', '',
     'A sequência C5 de 09:18 →09:33 →adendo09:35 →09:47 é preservada: continuação ainda em execução → piloto concluído com precisão parcial → controle SEOB → refinamento iniciado/API. Não converter um registro de início em término, nem o estado posterior em verdade do instante anterior. Os handles citados são identificadores de sessão históricos; nenhum processo vivo foi afirmado, consultado ou retomado nesta tarefa.', '',
     '| Marco existente na data da candidata | Alcance atual lido | SHA256 calculado |','|---|---|---|']
    for key,v in m['current_M1_M5'].items():
        lines.append(f'| `{v["path"]}:{v["lines"]}` | {v["current_documented_scope"]} | `{v["sha256"]}` |')
    lines += ['',
     'A existência atual desses cinco marcos é [REAL documental]; sua aceitação científica/gerencial não é inferida só pelo nome. O auditor, no instante de sua leitura, registrava ausência de marcos. Não há contradição a apagar: são retratos em instantes distintos. Não se produz recibo retroativo. Fichas C5 e C6_v2 foram consultadas; criação/revisão das oito fichas não integra esta tarefa.', '',
     '## Custódia, divergências históricas e falhas','',
     'O manifesto enumera todos os arquivos lidos/hashados, com existência, tamanho, SHA atual e confronto com hashes antigos quando disponíveis. Os oito alvos e a aditiva têm os hashes completos acima. Para os três alvos C5 sem hashes na nota, os vínculos vêm dos recibos C5_REAL_PHASE_RECOVERY, C5_COMPLETED_REAL_PHASE_PILOT e C5_REAL_REFINEMENT_START e seus campos `hashes`; os builders foram lidos somente como texto para localizar esses recibos.', '']
    checks=m['historical_hash_checks'];bad=[c for c in checks if not c['match']]
    lines += [f'Confrontos históricos: {len(checks)} referências, {len(checks)-len(bad)} coincidem diretamente com o caminho atual, {len(bad)} divergem/estão ausentes. Referências repetidas são contadas por citação, não por arquivo único.','']
    if bad:
        lines += ['| Origem/localizador | Caminho citado | SHA esperado histórico | SHA atual | Backup irmão correspondente |','|---|---|---|---|---|']
        for c in bad:
            lines.append(f'| `{c["origin"]}` / `{c["locator"]}` | `{c["path"]}` | `{c["expected_sha256"]}` | `{c["actual_sha256"]}` | '+(', '.join('`'+p+'`' for p in c['matching_sibling_backups']) or 'não localizado nesta busca delimitada')+' |')
    lines += ['',
     'Divergência histórica documentada não é apagada por fixar um novo hash. “Não localizado” limita-se ao caminho e backups irmãos inspecionados; não afirma inexistência em todo o acervo. Um backup correspondente preserva bytes, mas não prova sua ordem temporal. Binários NPZ citados foram apenas hashados; não desserializados nem recalculados. Bibliografia citada nas notas foi identificada/hashada, não revalidada integralmente nesta errata.', '',
     'A ausência preservada de `cache/source_evidence/phase_ringdown_balanced/IMRPhenomXPHM_seed130892_N16384/RESULT.json` é uma condição do snapshot, não uma autorização para produzir esse arquivo. Falhas de importação/serialização, backups de ruído e oráculo de broadcasting constam nominalmente no manifesto. Nenhuma falha foi removida ou transformada em aprovação.', '',
     '## Comando exato somente leitura','',
     '```powershell',
     '& C:\\Python314\\python.exe -B "C:\\IALD\\Central de Patentes\\Chatgpt\\ORDEM_013_RINGDOWN\\bis\\contract_errata\\contract_errata.py" --verify',
     '```','',
     '`--verify` abre somente o manifesto, a candidata, o próprio script e os caminhos explícitos do snapshot; compara presença/ausência, tamanho e SHA256 e escreve apenas stdout. Não cria log, cache, backup ou pyc (`-B`), não importa produção, não aciona subprocesso ou rede e não reexecuta C5. Retorna código1 em divergência do snapshot. Código0 significa identidade documental conferida, **não** quitação de lacunas históricas/físicas. O manifesto é um recibo local editável, não assinatura independente.', '',
     '**Arquivos escritos, somente estes:** `ORDEM_013_RINGDOWN/bis/contract_errata/CANDIDATE.md`, `MANIFEST.json` e `contract_errata.py` na mesma pasta. A emissão formal no túnel e a revisão por outro agente permanecem pendentes.','']
    return '\n'.join(lines)

def new(p,raw):
    if p.parent.resolve()!=HERE or p.exists():raise FileExistsError('Create-once, authorized outputs only: '+str(p))
    t=p.with_suffix(p.suffix+'.tmp')
    with t.open('xb') as f:f.write(raw)
    if t.read_bytes()!=raw:raise ValueError('Byte verification failed')
    t.replace(p)
def verify():
    # No writes on this branch, including verification failures.
    m=js(HERE/'MANIFEST.json');bad=[]
    if m['eight_targets']!=8 or m['ninth_additive']!=1 or len(m['notes'])!=9:raise ValueError('Wrong target coverage')
    if len({n['id'] for n in m['notes']})!=9:raise ValueError('Duplicate target')
    for old in m['files']+[m['candidate']]:
        now=snapshot(R/old['path'])
        if any(now[k]!=old[k] for k in ['exists','sha256','bytes']):bad.append({'expected':old,'observed':now})
    print(json.dumps({'status':'FAIL_SNAPSHOT' if bad else 'PASS_DOCUMENTARY_SNAPSHOT_ONLY',
       'checked':len(m['files'])+1,'historical_nonmatches_recorded':sum(not c['match'] for c in m['historical_hash_checks']),
       'scientific_acceptance':False,'formal_delivery_written':False,'writes':0,'mismatches':bad},ensure_ascii=False,indent=2))
    return 1 if bad else 0
def main():
    parser=argparse.ArgumentParser();mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--verify',action='store_true');mode.add_argument('--inspect',action='store_true');mode.add_argument('--build',action='store_true')
    args=parser.parse_args()
    if args.verify:return verify()
    m=collect()
    if args.inspect:
        print(json.dumps({'files':len(m['files']),'bytes':sum(f['bytes'] or 0 for f in m['files']),
           'notes':[{k:n[k] for k in ('id','receipt','receipt_status')} for n in m['notes']],
           'nonmatches':[c for c in m['historical_hash_checks'] if not c['match']],
           'missing':[f for f in m['files'] if not f['exists']]},ensure_ascii=False,indent=2));return 0
    new(HERE/'CANDIDATE.md',render(m).encode('utf-8'))
    m['candidate']=snapshot(HERE/'CANDIDATE.md')
    new(HERE/'MANIFEST.json',(json.dumps(m,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
    return verify()
if __name__=='__main__':sys.exit(main())
