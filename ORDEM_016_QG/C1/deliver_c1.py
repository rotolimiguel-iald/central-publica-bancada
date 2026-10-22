"""Report exact coverage, including the three legacy declarations not reproduced."""
from pathlib import Path
from datetime import datetime,timezone
import json,sys,subprocess
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'A7'))
from deliver_nonminimal_wick_and_mimo_audit import H,OUT,sha,write,put,append
D=Path(__file__).resolve().parent;ROOT=D.parent;now=datetime.now(timezone.utc)
plan=json.loads((D/'GROUP_AUDIT_PLAN_v3.json').read_bytes());original=set(plan['original_prints'])
auditor=OUT.parent/'PARA_CHATGPT/ORDEM_016_INSUMOS/A6_EQUACAO_DA_VERDADE/MEDIDAS_DO_REDATOR/auditar_axiomas.py'
args=[];sources=[];success=[]
for g in plan['groups']:
    k=g['group'];source=D/(f'ContractGroup{k}_v3.lean' if k!='J' else 'ContractGroupJ_v5.lean')
    label='group_'+k.lower()+('_02' if k=='A' else '_03' if k=='J' else '_01')
    p=D/(label+'.json');r=json.loads(p.read_bytes());assert r['rc']==0 and not r['scan_errors'] and not r['newer_kernel_files']
    assert sha(source)==r['source_sha256'] and sha(p.with_suffix('.log'))==r['log_sha256']
    args += [str(source),str(p.with_suffix('.log'))];sources.append(source);success.append(p)
audit=subprocess.run([sys.executable,'-X','utf8','-B',str(auditor),*args],capture_output=True)
assert audit.returncode==0,audit.stdout.decode('utf-8');write(D/'FINAL_AXIOM_AUDIT.json',audit.stdout)
audits=json.loads(audit.stdout);names=set()
for a in audits:
    assert a['auditoria']=='PASSA';names.update(a['axiomas'])
missing=sorted(original-names);covered=sorted(original&names)
expected_missing=['TGLExt.ContratoQGv31.'+n for n in ['contratoH2_empty_on_legacy','contratoH3_empty_on_legacy','no_import_on_legacy']]
assert missing==sorted(expected_missing) and len(covered)==87 and len(names)==92
all_receipts=[]
for p in sorted(D.glob('group_*.json')):
    r=json.loads(p.read_bytes())
    if not isinstance(r,dict) or 'command' not in r:continue
    assert sha(Path(r['command'][-1]))==r['source_sha256'] and sha(p.with_suffix('.log'))==r['log_sha256']
    all_receipts.append(dict(path=str(p),sha256=sha(p),**r))
bad=json.loads((D/'group_j_02.json').read_bytes());assert bad['rc']==3221226505 and bad['peak_process_committed_bytes']==8*1024**3
cpu=sum(r['cpu_user_seconds']+r['cpu_kernel_seconds'] for r in all_receipts);wall=sum(r['wall_seconds'] for r in all_receipts)
start=datetime.fromisoformat(json.loads((D/'SOURCE_GROUPS.json').read_bytes())['at']);elapsed=(now-start).total_seconds()/3600
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
result=dict(at=now.isoformat(),status='MEDIDA_PARTIAL_REPRODUCTION_87_OF_90',original_prints=len(original),covered=covered,missing=missing,
    all_current_audited_declarations=len(names),groups_compiled=10,all_axioms_in_trio=True,zero_sorry_success_sources=True,
    theorem_bodies_changed=False,body_equivalence='Copied source bodies with newline normalization and reopened identical scopes; only import/open wrappers differ',
    missing_reason='V354RegularLegacyWitness needed for regularModularRealization; adding actual import hit 8GiB WindowsJob cap',
    unchanged_named_obligation='ReproduceThreeLegacyDeclarationsWithRealImportWithin8GiB',obligation_kind='environment/integration, not a new physics axiom',
    original_90_claim_fully_reproduced=False,canonical_sources_modified=False,gate_changed=False,
    compile_wall_seconds=wall,compile_cpu_seconds=cpu,bench_elapsed_hours=elapsed,ceiling_hours=6,receipts=all_receipts,
    failed_attempts_retained=['group_a_01: absent namespace in reduced open header','group_j_01: missing regularModularRealization','group_j_02: bad_alloc at8GiB'],
    full_canonical_mtime_scan=False,scan_note='A8/CANONICAL_READONLY_SCAN.json reports no newer accessible files but access denied to canonical packages; read-only dependency builds supplied from bench',
    next='C2')
put(D/'RESULTS.json',result)
note=f'''[REAL — C1: reprodução parcial auditada; MEDIDA do import legado]

AberturaSHA256={opening}.

Reproduzidos **87 dos90 enunciados auditados na origem**. Dez grupos
coexistem pela cadeia de imports;92declarações no total foram auditadas,
incluindo auxiliares do texto original antes sem print. Compilação rc0,
somente propext/Classical.choice/Quot.sound, zero sorry nos arquivos aceitos.
Os corpos das provas foram copiados, com normalização de fim de linha;
somente imports, abertura de escopos e prints foram ajustados.

Os resultados incluem coerência espectral, sinais, KMS condicional,
κ dadoN, unicidade do implementador, campos geométricos, primeira lei
de janela, BH/Clausius, consumidoresH3 e o import não vazio indexado.
Nenhum desses teoremas perde as hipóteses do contrato.

**Três continuam sem reprodução nesta máquina sob o limite vigente:**
contratoH2_empty_on_legacy, contratoH3_empty_on_legacy e no_import_on_legacy.
São instâncias que precisam de regularModularRealization. Sem o import
real, o compilador recusa o nome; acrescentando V354RegularLegacyWitness,
o processo atingiu {bad['peak_process_committed_bytes']}bytes e saiu
rc{bad['rc']} com std::bad_alloc. O import não foi simulado nem trocado
por hipótese. Os cinco enunciados independentes desse import no grupoJ
foram separados e compilados. O teorema genérico de exclusão por
translações não fiéis permanece entre os pagos.

Obrigaçãodeintegração nomeada: ReproduceThreeLegacyDeclarationsWithRealImportWithin8GiB.
Não é uma nova hipótese física. Fontes e falhas preservadas, sem novo
teorema para mascarar a falta de reprodução. O recibo da origem para
os90 permanece distinto destes87 verificados aqui.

Recursos: {len(all_receipts)}compilações,parede{wall:.3f}s,CPU{cpu:.3f}s;
bancada{elapsed:.4f}h/teto6h. Comandos/logs/hashes emRESULTS/manifest.
Auditor da gerência: FINAL_AXIOM_AUDIT.json,10grupos PASSA.
Lake executado no ambiente isolado; pacotes em leitura na bancada,
revisões conferidas. Varredura canônica parcial: zero arquivos novos
acessíveis e recusa de acesso a.lake/packages, explicitada no reciboA8.

**Não move o gate.** Fecha parte da dívida de reprodução daA1, não
produz um par físico H2/H3. PróximoC2: largura/isotonia da reta de luz,
reutilizando LightRayTwistWidth_v3 antes de acrescentar qualquer lema.
'''
write(D/'RELATORIO.md',note.encode());write(OUT/'ENTREGA_016_C1_reproducao_contrato.md',note.encode())
write(OUT/'ENTREGA_016_MEDIDA_C1_import_legado_8GiB.md',note.encode())
refs=[p for p in D.iterdir() if p.is_file() and p.suffix!='.marker']+[auditor,Path(json.loads((D/'SOURCE_GROUPS.json').read_bytes())['source']),ROOT/'A8/CANONICAL_READONLY_SCAN.json']
put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in refs],original_covered=87,original_missing=3,gate_changed=False))
append(OUT/'LEDGER_016.jsonl',json.dumps(dict(at=now.isoformat(),event='C1_REPRODUCTION_87_OF_90',target='PartC.C1',remote_call=False,
    compile_wall_seconds=wall,compile_cpu_seconds=cpu,manifest_sha256=sha(D/'manifest.json')))+'\n')
append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} C1MEDIDA:87/90originais reproduzidos;92declarações no trio;3dependemimportqueexcede8GiB. Bancada{elapsed:.4f}h/6h;CPU{cpu:.3f}s;parede{wall:.3f}s. ManifestoSHA256={sha(D/"manifest.json")}. Gateintacto;segueC2. AberturaSHA256={opening}.\n')
p=H/'CONTINUIDADE.json';c=json.loads(p.read_bytes());c.update(at=now.isoformat(),previous_goal_turn='PROGRESS',next=['C2 existing LightRayTwistWidth_v3 then remove first-period assumption using full-strip contraction; retain physical/isotony scope','C3 integration; C4 cocycle; C5KMS; C6Q2; PartB; finalaudit'],C1_manifest=str(D/'manifest.json'),own_live_processes=[])
c['remaining_full_goal']=['C2-C6','C2.3/4/5 external critiques full source audits','ORDEM015 PartB','Full final audit and reports'];put(p,c,True)
print(json.dumps(dict(covered=len(covered),missing=len(missing),cpu=cpu,next='C2')))
