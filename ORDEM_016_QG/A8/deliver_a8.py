"""A proposal, not a gate mutation. Distinguish current controls from origin receipts."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json,sys,subprocess
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'A7'))
from deliver_nonminimal_wick_and_mimo_audit import H,OUT,sha,write,put,append
D=Path(__file__).resolve().parent; ROOT=D.parent; IN=OUT.parent/'PARA_CHATGPT'
now=datetime.now(timezone.utc);opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
statepath=IN/'ORDEM_016_INSUMOS/ESTADO_QG_v370.json';state=json.loads(statepath.read_bytes())
frontier=state['kernel_frontier']
original=ROOT/'A1/v31/ContratoQG_v31.lean';minimal=ROOT/'A1/minimal_imports/ContratoQG_v31_Minimal.lean'
def body(p): return '\n'.join(x for x in p.read_text('utf-8').splitlines() if not x.startswith('import '))
assert body(original)==body(minimal),'Contract body drift'
receipts=[]
for p in sorted(D.glob('*.json')):
    j=json.loads(p.read_bytes())
    if not isinstance(j,dict) or not {'command','rc','source_sha256','log_sha256'}<=j.keys(): continue
    assert sha(Path(j['command'][-1]))==j['source_sha256']
    assert sha(p.with_suffix('.log'))==j['log_sha256']
    receipts.append(dict(path=str(p),sha256=sha(p),**j))
byname={Path(x['path']).stem:x for x in receipts}
assert byname['contract_load_01']['rc']==0
assert byname['closed_indices_01']['rc']!=0 and 'out of memory' in (D/'closed_indices_01.log').read_text('utf-8')
assert byname['closed_indices_02']['rc']==0
assert byname['ReaderPositive_01']['rc']==0
for label in ['ReaderRejectEmpty_01','ReaderRejectToy_01','ReaderRejectIndex_01']:
    assert byname[label]['rc']==1 and 'EXACT_TYPE_MISMATCH' in (D/(label+'.log')).read_text('utf-8')
assert byname['reject_actual_contract_01']['rc']==1
assert 'Type mismatch' in (D/'reject_actual_contract_01.log').read_text('utf-8')
auditor=IN/'ORDEM_016_INSUMOS/A6_EQUACAO_DA_VERDADE/MEDIDAS_DO_REDATOR/auditar_axiomas.py'
cmd=[sys.executable,'-X','utf8','-B',str(auditor),str(D/'ReaderPositive_v2.lean'),str(D/'ReaderPositive_01.log'),str(D/'ClosedIndexChecks_v2.lean'),str(D/'closed_indices_02.log')]
run=subprocess.run(cmd,capture_output=True);assert run.returncode==0,run.stdout.decode('utf-8')
write(D/'axiom_audit.json',run.stdout);audits=json.loads(run.stdout)
assert all(x['auditoria']=='PASSA' for x in audits)
physical_manifest=ROOT/'A1/v31/MANIFESTO_V31.json';physical=json.loads(physical_manifest.read_bytes())
negative=[]
for name in ['ProbeVacuousImportV31.lean','ProbeToyV31.lean','ProbeLegacyV31.lean']:
    row=next(x for x in physical if x['arquivo']==name);p=physical_manifest.parent/name
    assert sha(p).startswith(row['sha16']) and row['rc']==1
    negative.append(dict(source=str(p),sha256=sha(p),origin_rc=row['rc'],origin_error_sites=row['sitios_de_erro'],
        origin_manifest_sha256=sha(physical_manifest),statute='DECLARADO_ORIGIN_COMPILATION_SOURCE_BYTES_VERIFIED_HERE',
        recompiled_in_A8=False,raw_origin_log_available_in_input_package=False))
put(D/'NEGATIVE_PROBES_PROVENANCE.json',negative)
bindings=[dict(item=k,status='OPEN',can_be_paid_by_name_or_clean_axioms=False) for k in frontier['remaining']]
bindings[0].update(expected_type='TGLExt.ContratoQGv31.ContratoH2 W0 R0 N0',closed_indices=['W0','R0','N0'])
bindings[1].update(expected_type='TGLExt.ContratoQGv31.ContratoH3 W0 R0 N0 T0',closed_indices=['W0','R0','N0','T0'],
    extra_alignment='h3.H2 = h2; direct equality evidence or produce(h2) with same_horizon, never an empty-domain arrow')
bindings[2].update(expected_type=None,reason='Physical interacting state, anomaly-free full QME and UV contract not supplied by UVScope016 logical routes; no boolean placeholder accepted')
spec=dict(statute='INPUT_PROPOSAL_ONLY',at=now.isoformat(),opening_sha256=opening,gate_changed=False,reader_deployed=False,
    reference_snapshot=dict(path=str(statepath),sha256=sha(statepath),version='v370 historical input, not a claim about current deployment'),
    contract=dict(source=str(original),sha256=sha(original),minimal_import_variant=str(minimal),minimal_sha256=sha(minimal),
        body_identical_after_import_lines_removed=True,ratification=None,closed_W_R_N_T=None),
    verification=dict(exact_type='Infer raw closed declaration type and compare definitionally with pinned target; never apply missing hypotheses to make it fit',
        wrapper='A no-autoImplicit closed definition/check at the exact ratified type; print axioms of final supplied terms and alignment',
        whitelist=['propext','Classical.choice','Quot.sound'],require_rc_zero=True,require_no_sorry=True,
        require_no_open_metas_or_locals=True,require_import_source_build_and_toolchain_custody=True,
        expected_type_from='Ratified contract, not from candidate or provider answer',
        fail_closed=['missing ratification','unreadable or changed artifact','missing evidence','type mismatch','new/unknown frontier item','failed negative control','unpaid named hypothesis']),
    remaining=bindings,physical_identifications=[dict(item=k,status='OPEN',expected_type=None,automatic_promotion=False) for k in frontier['physical_identifications_open']],
    import_H3=dict(expected_type='TGLExt.ContratoQGv31.ContratoImportH3 W0 R0 N0 T0 h2',requires_closed_h2=True),
    ringdown=dict(enabled=False,operator_authorization_required=True,role='Empirical report only, no mathematical frontier discharge',
        bilateral=True,reading_selection=None,registration_and_family_correction_required=True,clock_identification_automatic=False),
    negative_probes=negative,reader_controls=['ReaderPositive_01','ReaderRejectEmpty_01','ReaderRejectToy_01','ReaderRejectIndex_01','reject_actual_contract_01'],
    implementation_owner='gerencia',decision_owner='operador',transition_now='NONE')
put(D/'PROPOSTA_DEGRAU_GATE_016.json',spec)
cpu=sum(x['cpu_user_seconds']+x['cpu_kernel_seconds'] for x in receipts);wall=sum(x['wall_seconds'] for x in receipts)
elapsed=(now-datetime.fromisoformat(json.loads((D/'START.json').read_bytes())['at'])).total_seconds()/3600
put(D/'RESULTS.json',dict(at=now.isoformat(),status='PROPOSAL_DELIVERED_WITH_PROBE_PROVENANCE_MEASURE',
    exact_reader_controls='2 accepted types, 3 rejected raw declaration types',actual_H2_promotion_rejected=True,
    original_physical_negatives='Origin rc1 receipts reused and source hashes verified; not rerun in this target',
    conditional_contract_consumer_compiled=True,conditional_consumer_new_physics=False,axiom_audit='PASSA',
    compile_receipts=receipts,compile_wall_seconds=wall,compile_cpu_seconds=cpu,bench_elapsed_hours=elapsed,ceiling_hours=4,
    originals_modified=False,gate_changed=False,
    operational_incident='While ContractLoad was pending two tiny control compilations were dispatched together; possible overlap of three Lean processes exceeded max2. Subsequent compiles serialized. Results retain actual receipts; no scientific acceptance inferred from scheduling.',
    first_environment_setup_failure='Cli package has no built lib directory; existing package builds explicitly listed, absent entry retained in IMPORT_PATH_AVAILABILITY.json',
    source_and_import_custody_limit='Current contract body and artifact hashes checked. No full new rebuild or transitive source-to-olean certification is claimed.',next='PartC.C1'))
note=f'''[INPUT — proposta A8; verificações de engenharia REAL; ratificação pendente]

Abertura SHA256: {opening}

**Leitor por tipo.** O contrato v3.1 e seus índices W0/R0/N0/T0 devem ser
ratificados e fixados por manifesto. Conferir o tipo da declaração FECHADA,
sem aplicar hipóteses ausentes para fazê-la caber. Exigir compilação rc0,
axiomas no trio, zero sorry e custódia de fonte/imports/build. O tipo-alvo
vem do contrato ratificado, nunca da resposta do candidato. Nome, rótulo,
consenso de modelos ou axiomas limpos sozinhos não satisfazem o leitor.

**Ligação já existente.** ContratoImportH3 é indexado por h2 concreto;
produce(h2) fornece H3 e same_horizon prova que seu H2 é o mesmo. O
consumidor ClosedIndexChecks_v2 apenas reutiliza esses campos: rc0,
três declarações no trio, auditor PASSA. Não cria habitante físico.
RejectConditionalAsInhabitant recusou, no contrato real, retirar a
entrada H2 e anunciar a função condicional como fornecedora de H2.

**Estado lido.** JSON anexo contém literalmente os três remaining e as
duas physical_identifications do insumo histórico v370. H2/H3 leem os
tipos acima e a igualdade do mesmo horizonte. Estado interagente/QME/UV
e as duas identificações não ganham True substituto: sem contrato e
prova específicos continuam OPEN. UVScope016 não paga esses objetos.
Ratificar outro par não altera retroativamente o legado U=1.

**Controles.** Leitor protótipo aceitou dois tipos esperados e recusou
False→Nat como Nat, Unit como Nat e Fin2 como Fin3, todos sem axiomas
extras. São controles de engenharia, não substitutos dos probes físicos.
Os probes físicos import vazio/brinquedo/legado são os já entregues:
rc1 nos três no MANIFESTO_V31; hashes das fontes conferidos agora.
Seus rc são DECLARADOS da origem: logs integrais não constam no pacote,
e não alegamos nova compilação desses três nesta rodada. Essa MEDIDA
fica explícita; a gerência deve repeti-los no rito de incorporação.

**Ringdown.** Porta opcional desabilitada. Se autorizada, lê teste bilateral
pré-registrado, todas as leituras e correção de multiplicidade da 015;
nunca escolhe relógio ou parâmetro e nunca paga uma prova matemática.

**Recursos e falhas.** {len(receipts)} recibos Lean, {wall:.3f}s de parede somada,
{cpu:.3f}s de CPU, {elapsed:.4f}h de bancada/teto4h. O consumidor junto
ao metaprograma esgotou8GB; separá-los manteve o contrato e compilou.
Dependências de revisão idêntica são lidas da bancada; lake executado
apenas no ambiente isolado. Um manifesto nasceu nesse ambiente próprio.
Limitação: não houve novo rebuild/auditoria de toda a cadeia de oleans.
Incidente de agenda: houve possível sobreposição de3 processos na carga
do contrato com2 controles breves; o restante foi serializado.

Proposta JSON e manifest.json carregam hashes completos. Implementação
é da gerência; decisão é do operador. Sem edição do um.py, sem nomes
reservados novos, sem mudança de gate. Próximo: ParteC.C1.
'''
write(D/'PROPOSTA_DEGRAU_GATE_016.md',note.encode())
write(OUT/'ENTREGA_016_A8_degrau_do_gate.md',note.encode())
refs=[p for p in D.iterdir() if p.is_file() and p.suffix not in ['.marker']]
refs += [original,minimal,physical_manifest,statepath,auditor]+[Path(x['source']) for x in negative]
put(D/'manifest.json',dict(at=now.isoformat(),artifacts=[dict(path=str(p),sha256=sha(p)) for p in refs],gate_changed=False))
append(OUT/'LEDGER_016.jsonl',json.dumps(dict(at=now.isoformat(),event='A8_TYPED_READER_PROPOSAL',target='A8',remote_call=False,
    compile_wall_seconds=wall,compile_cpu_seconds=cpu,manifest_sha256=sha(D/'manifest.json')))+'\n')
append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A8 PROPOSTA ENTREGUE/MEDIDA: tipos e consumidor conferidos; probes físicos com rc da origem explicitamente não reexecutados. Bancada{elapsed:.4f}h/4h, máquina parede{wall:.3f}s CPU{cpu:.3f}s. Custódia {sha(D/"manifest.json")}. Gate intacto. PróximoParteC.C1. AberturaSHA256={opening}.\n')
p=H/'CONTINUIDADE.json';c=json.loads(p.read_bytes());c.update(at=now.isoformat(),previous_goal_turn='PROGRESS',next=['PartC.C1 contract integral reproduction in groups; thenC2-C6; ORDEM015PartB; finalaudit'],A8_manifest=str(D/'manifest.json'),own_live_processes=[])
c['remaining_full_goal']=['ADENDO002 critique final audits C2.3/C2.4/C2.5','PartC C1-C6','ORDEM015 PartB','Full final audit and reports']
put(p,c,True)
print(json.dumps(dict(status='A8_DELIVERED',bench_hours=elapsed,compile_cpu_seconds=cpu,next='PartC.C1')))
