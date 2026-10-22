from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,importlib.util,json,re

HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
OUT=ROOT.parent/'TUNEL/DO_CHATGPT';E=HERE/'E_ficha';B=HERE/'B_fechamentos';C=HERE/'C_controles'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):
    raw=v if isinstance(v,bytes) else (v.encode() if isinstance(v,str) else json.dumps(v,ensure_ascii=False,indent=2).encode())
    stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    if p.exists():
        old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+stamp);bak.write_bytes(old);assert bak.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp_'+stamp);tmp.write_bytes(raw);assert tmp.read_bytes()==raw and raw;tmp.replace(p)
spec=importlib.util.spec_from_file_location('audit',ROOT/'A0/auditar_axiomas.py')
audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
units=[(B,'TheEquationOfTruth_T20_v3.lean','single_time_02'),
       (B,'InscriptionBridge.lean','inscription_bridge_01'),
       (B,'PenaltyThreeLocksBridge_v2.lean','penalty_bridge_02'),
       (B,'OperatorContourBridge_v2.lean','operator_contour_02'),
       (B,'QubitScalarEntropy.lean','qubit_scalar_01'),
       (B,'QubitEntropyDerivative_v3.lean','qubit_derivative_03'),
       (B,'IdempotentDephasing_v2.lean','idempotent_exp_02'),
       (B,'FiniteGapRate_v2.lean','finite_gap_02'),
       (B,'InfiniteLimitUniformControl_v2.lean','infinite_uniform_control_02'),
       (B,'ModularGeneratorControl.lean','modular_generator_01'),
       (C,'TheEquationOfTruth_T20_controles_v3.lean','negative_controls_03'),
       (C,'NegativeControlsCompleteness_v2.lean','negative_completeness_02')]
records=[];axioms={};theorems=[]
for folder,file,label in units:
    source=folder/file;log=folder/(label+'.log');receipt=json.loads((folder/(label+'.json')).read_bytes())
    assert receipt['rc']==0 and sha(source)==receipt['source_sha256'] and sha(log)==receipt['log_sha256']
    a=audit.audita(str(source),str(log));assert a['auditoria']=='PASSA'
    local,_=audit.decls_da_fonte(audit.sem_comentarios(source.read_text(encoding='utf-8')))
    assert not set(local)&set(theorems),'Duplicate declarations among selected sources'
    theorems.extend(local)
    for n,ax in a['axiomas'].items():
        if n in axioms:assert axioms[n]==ax
        axioms[n]=ax
    records.append(dict(source=str(source),sha256=sha(source),log=str(log),log_sha256=sha(log),
                         receipt_sha256=sha(folder/(label+'.json')),imports=re.findall(r'^import (\S+)',source.read_text(encoding='utf-8'),re.M),
                         theorem_names=local,audit=a))
prefix='TGLExt.EquationOfTruth.'
base_flags={
 'truth_bit':['truthValue_table','truthBit_eq_one_iff','truthBit_eq_zero_iff','truthBit_bivalent'],
 'joint_exclusion':['ker_penalty','ker_threeLocks','re_inner_penalty'],
 'selector_nonpos':['selector_nonpos'],
 'projection_annihilates':['H_mul_proj','proj_mul_H'],
 'reading_conserved':['proj_mul_T','reading_T','T_fix_of_mem_ker','T_decomp'],
 'verdict_one':['verdict_T','verdict_eq_one_iff'],
 'name_verifies_flow':['name_verifies_T','name_verifies_T_iterate'],
 'stable_memory':['mem_range_iff_fixed','starProjection_range_iff_fixed','pow_eq_self','apply_eq_apply_iff'],
 'converse_named':['conserved_iff_factors','conserved_iff_factors_T'],
 'spectral_limit_findim':['flowTendsToFamily_of_finiteDimensional'],
 'converse_findim':['conserved_iff_factors_penalty','conserved_iff_factors_of_nonneg'],
 'reading_derivative_zero':['hasDerivAt_reading_T','hasDerivAt_reading_flow','flow_derivative_ne_zero_at_zero'],
 'profile_derivatives':['profA_deriv_zero','profQ_deriv_zero','profA_second_deriv_zero'],
 'extremes':['reading_zero_of_kernel_bot','verdict_one_of_kernel_bot','operator_zero_of_kernel_top','flow_identity_of_kernel_top'],
 'distinguishing_reading':['distinguishing_reading_iff','distinguishing_verdict_eq'],
 'crossing_v368':['flow_preserves_inscription_form','inscription_form_survives','transported_name_eq_flow','positive_time_changes_nonfixed_content','same_form_changed_name'],
 'penalty_is_kernel_H3L':['penalty_eq_kernel_H3L','reading_eq_kernel_PF'],
 'single_time_converse':['T_add','iterate_T_eq_nat_time','single_time_conserved_iff_factors'],
 'not_static_operator_face':['equation_of_truth_is_not_static','equation_criterion_can_fail'],
 'qubit_entropy_scalar_monotone':['QubitScalar.entropy_monotoneOn','QubitScalar.entropy_strictMonoOn','QubitScalar.entropy_le_diagonal','QubitScalar.deficit_nonneg','QubitScalar.deficit_antitoneOn'],
 'norm_rate_findim':['finite_gap_norm_rate']}
flags={}
for key,names in base_flags.items():
    qualified=[prefix+n for n in names]
    assert all(n in axioms for n in qualified),qualified
    flags['ext_eot_'+key+'_kernel_proved']=dict(consumes=qualified,status='PROPOSAL_NOT_INSTALLED',gate_input=False)
flags['ext_eot_negative_controls_kernel_proved']=dict(consumes=[n for n in theorems if '.NegativeControls.' in n],status='PROPOSAL_NOT_INSTALLED',gate_input=False)
contour_source=HERE/'A_reproducao/AxiomasContorno.lean'
contour_names=re.findall(r'^#print axioms (\S+)',contour_source.read_text(encoding='utf-8'),re.M)
assert len(contour_names)==7
audit_lines=['-- PROPOSAL ONLY: integration module not accepted/installed.','import TGLExt.TheEquationOfTruth','import TGLExt.TheContourOfTruth']
audit_lines += ['#print axioms '+n for n in theorems+contour_names]
save(E/'PROPOSTA_AUDIT.lean','\n'.join(audit_lines)+'\n')
original=HERE/'A_reproducao/TheEquationOfTruth.lean';base=B/'TheEquationOfTruth_T20_v3.lean'
assert base.read_bytes().startswith(original.read_bytes())
failures=[json.loads((E/'candidate'/(l+'.json')).read_bytes()) for l in ['transposition_candidate_01','transposition_module_01']]
assert all(r['rc']!=0 and not r['newer_kernel_files'] and not r['scan_errors'] for r in failures)
original_log=HERE/'A_reproducao/equation_reproduction_01.log'
warnings=re.findall(r'^.*:\d+:\d+: warning:.*$',original_log.read_text(encoding='utf-8'),re.M)
save(E/'WARNINGS_V3.json',dict(source_sha256=sha(original),log_sha256=sha(original_log),warnings=warnings,
                              warning_count=len(warnings),deprecation_warning_count=sum('deprecated' in w for w in warnings)))
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md');now=datetime.now(timezone.utc)
incoming=ROOT.parent/'TUNEL/PARA_CHATGPT'
tunnel=[dict(name=p.name,bytes=p.stat().st_size,mtime_ns=p.stat().st_mtime_ns) for p in sorted(incoming.iterdir()) if p.is_file()]
save(E/'incoming_directory_snapshot.json',dict(at=now.isoformat(),files=tunnel,interpretation='No new physical ratification inferred from filenames; transport addendum reread, no mathematical change.'))
sheet=dict(status='INPUT_TRANSPOSITION_PROPOSAL_WITH_MEASURED_PACKAGING_GAP',at=now.isoformat(),opening_sha256=opening,
 target_module='TGLExt/TheEquationOfTruth.lean',namespace='TGLExt.EquationOfTruth',
 import_line='import TGLExt.TheEquationOfTruth',accepted_local_sources=records,
 local_theorem_count=len(theorems),axioms=axioms,proposed_flags=flags,contour_audit_additions=contour_names,
 reference_prefix=dict(bytes=len(original.read_bytes()),sha256=sha(original),preserved_in=str(base)),
 proposal_audit_sha256=sha(E/'PROPOSTA_AUDIT.lean'),warnings=str(E/'WARNINGS_V3.json'),
 strict_single_file_prefix_requirement='NOT_SATISFIED_FOR_ALL_CLOSURES; imports require header changes; MEDIDA',
 monolithic_attempts=failures,monolithic_candidate_approved=False,
 dependency_plan=['Choose exactly one final base; v1 and v3 cannot be imported together.',
                  'Relocate required imports only with management acceptance of prefix exception.',
                  'Alternative modular graph: regenerate companion imports against sole v3 base, then recompile all; not yet performed.',
                  'Separate all #print axioms into canonical Audit; rerun compilation and source/log/rc checks.',
                  'Install flags only after canonical audit, preserving named hypotheses and no gate input.'],
 open_mathematical_hypothesis='bounded_positive_strong_limit; infinite converse remains conditional on FlowTendsToFamily',
 excluded=['Matrix entropy is harness evidence, not a Lean theorem of von Neumann entropy.',
           '22/22+5 external package unavailable.',
           'No runtime floating-point H3L instantiation.',
           'No identification of dissipative semigroup with modular unitary flow.',
           'No identification of three distinct zero/annihilation statements.'],
 canonical_written=False,gate_changed=False)
save(E/'FICHA_TRANSPOSICAO_T20.json',sheet)
text=f'''[INPUT — ficha de transposição; REAL — fontes individuais auditadas; MEDIDA — integração monolítica]

# A6.E — ficha para a gerência

Abertura SHA256: `{opening}`.

Destino proposto: `TGLExt/TheEquationOfTruth.lean`, namespace `TGLExt.EquationOfTruth`; linha para TGLExt.lean: `import TGLExt.TheEquationOfTruth`. Incorporação é da gerência, com ratificação do operador. Nada foi instalado no kernel/um.py.

**Fontes aprovadas individualmente:** {len(records)} fontes, {len(theorems)} theorem/lemma locais distintos, todos compilados com rc0 e axiomas no trio. A lista integral, enunciados em suas fontes, imports, hashes de fontes/logs/recibos e axiomas estão na ficha JSON. A base selecionada é TheEquationOfTruth_T20_v3, com 57 lemas e os primeiros {len(original.read_bytes())} bytes da referência V3 preservados exatamente (SHA256 {sha(original)}). As pontes anteriores usam v1; não se pode importar v1 e v3 no mesmo ambiente. Os 127 lemas não são 127 novos: incluem os 46 reproduzidos.

**MEDIDA obrigatória de empacotamento:** a aceitação estrita de todos os fechamentos em arquivo único com prefixo V3 não está satisfeita. Lean recusa import acrescentado ao fim. A proposta separada de monólito realocou somente imports, sem alterar os corpos, e portanto não preserva aquele prefixo. Compilação com relatórios embutidos terminou rc={failures[0]['rc']}; a variante separando #print terminou rc={failures[1]['rc']}, com mensagem explícita `INTERNAL PANIC: out of memory`, sob o limite de 8 GiB. As duas tentativas, fontes e logs estão preservados. Nenhuma é fonte aprovada para instalar; não se aumentou o limite nem se substituiu falha por PASS. As provas individuais permanecem válidas no escopo auditado.

Ordem proposta: uma base única → pontes de inscrição/Three Locks/Contorno → entropia escalar/derivada/idempotente/taxa → controles modular e infinito → controles negativos. Os imports canônicos necessários incluem TheNameIsTheInstrument, NameIsTheContent, FiniteThreeLocks, TheContourOfTruth e ContinuousModularZero; a lista exata está no manifesto de construção. Uma transposição modular exige regenerar imports dos companheiros e recompilar; esse conjunto integrado ainda não foi certificado.

**Audit e flags:** `PROPOSTA_AUDIT.lean` contém uma linha por teorema local e as sete de TheContourOfTruth. É texto proposto, não auditoria executada do módulo canônico inexistente. A ficha propõe {len(flags)} bandeiras ext_eot_*, com consumidores exatos e gate_input=false. Todas são PROPOSAL_NOT_INSTALLED. O limite forte infinito permanece hipótese nomeada, sem bandeira de fechamento. WARNINGS_V3.json lista os {len(warnings)} avisos originais e distingue os de deprecação.

O que fica fora: entropia matricial do harness, pacote externo 22/22+5, identificação de operandos float do runtime e igualdades entre objetos de tipos distintos. As leituras “verdade”, “memória”, “seleção apofática” permanecem [INPUT/ONTO] em docstrings rotuladas; não são conclusões físicas.

**Frase da ficha:** Estas bandeiras não movem o gate. PROVADA (teorema em kernel) ≠ CONFIRMADA. A implicação está provada a partir das hipóteses nomeadas; a leitura é do operador; a natureza decide a teoria.

Ficha JSON: `{E/'FICHA_TRANSPOSICAO_T20.json'}`. Próximo alvo da árvore: A7. A6.B1d e empacotamento ficam MEDIDA; a ficha não apaga essas pendências.
'''
save(E/'FICHA_TRANSPOSICAO_T20.md',text)
save(OUT/'ENTREGA_016_A6_E_transposicao.md',text)
save(OUT/'ENTREGA_016_MEDIDA_A6_empacotamento.md',f'''[REAL — falhas de compilação da proposta monolítica; MEDIDA de integração]

Abertura SHA256: {opening}.

Prova individual não equivale a integração compilada. Os imports adicionais conflitam com prefixo V3 imutável. Uma proposta separada com imports no início preservou os corpos e removeu imports locais duplicados. Duas execuções isoladas: rc {failures[0]['rc']} e {failures[1]['rc']}; segunda com INTERNAL PANIC: out of memory. Total máquina {sum(r['wall_seconds'] for r in failures):.6f}s parede, {sum(r['cpu_user_seconds']+r['cpu_kernel_seconds'] for r in failures):.6f}s CPU. Recibos completos em E_ficha/candidate, hashes no JSON da ficha. Zero escrita detectada no kernel.

Não há terceiro retry sem novo diagnóstico. Fonte monolítica não aprovada; fontes individuais aprovadas continuam custodiadas. Opções para gerência: aceitar cabeçalho alterado e compilar com recursos autorizados, ou ratificar módulos companheiros com base única e auditoria transitiva. Nenhuma opção foi instalada. Próximo ramo A7, conforme protocolo de MEDIDA.
''')
ledger=OUT/'LEDGER_016.jsonl';old=ledger.read_bytes();marker='A6_E_TRANSPOSITION_MEASURE_20260924'
events=[json.loads(l) for l in old.decode('utf-8-sig').splitlines() if l.strip()];costs={}
for e in events:
    c=e.get('cost_estimate_usd',e.get('cost_usd',e.get('custo_usd')))
    key=e.get('execution_id') or e.get('job_id') or e.get('request_id') or e.get('execution_task_id')
    if c is not None and key:costs[key]=Decimal(str(c))
cost=sum(costs.values(),Decimal(0))
if marker.encode() not in old:
    entry=dict(event=marker,at=now.isoformat(),manifest=str(E/'FICHA_TRANSPOSICAO_T20.json'),manifest_sha256=sha(E/'FICHA_TRANSPOSICAO_T20.json'),external_execution=False)
    save(ledger,old+(json.dumps(entry,ensure_ascii=False)+'\n').encode())
p=OUT/'ENTREGA_016_PROGRESSO.md';old=p.read_bytes()
if marker.encode() not in old:
    save(p,old+f'\n- {now.isoformat()} — A6.E PAGO como proposta; integração MEDIDA (prefixo/imports e OOM). {len(theorems)} lemas locais auditados não equivalem a monólito aprovado. Duas tentativas de integração: {sum(r["wall_seconds"] for r in failures)/3600:.6f}h parede, {sum(r["cpu_user_seconds"]+r["cpu_kernel_seconds"] for r in failures)/3600:.6f}h CPU; bancada não exclusiva. Estimativas externas US${cost}, incompletas. Túnel listado; adendo transporte relido, nenhuma ratificação física inferida. Abertura {opening}. Não move gate; próximo A7. [{marker}]\n'.encode())
print(json.dumps(dict(status=sheet['status'],theorems=len(theorems),flags=len(flags),warnings=len(warnings))))
