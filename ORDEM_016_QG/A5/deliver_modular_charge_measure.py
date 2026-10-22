from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
import hashlib, json, sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT.parent / 'TUNEL/DO_CHATGPT'
INCOMING = ROOT.parent / 'TUNEL/PARA_CHATGPT'
KERNEL = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
sys.path.insert(0, str(ROOT/'A0'))
from auditar_axiomas import audita

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def save(p, value):
    raw = value.encode('utf-8') if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2).encode('utf-8')
    stamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    if p.exists():
        before = p.read_bytes()
        backup = p.with_name(p.name+'.bak_'+stamp)
        backup.write_bytes(before)
        assert backup.read_bytes() == before
    tmp = p.with_name(p.name+'.tmp_'+stamp)
    tmp.write_bytes(raw)
    assert tmp.read_bytes() == raw and raw
    tmp.replace(p)

finals = [('TraceInfinityExtension_v3.lean','trace_infinity_03'),
          ('ModularBoostEnergyReuse_v2.lean','modular_boost_energy_02'),
          ('ModularChargeLink.lean','modular_charge_link_01'),
          ('ExistingTraceCompletionAudit_v2.lean','existing_trace_completion_02')]
proofs=[]
for name,label in finals:
    s=HERE/name; l=HERE/(label+'.log'); rp=HERE/(label+'.json')
    r=json.loads(rp.read_bytes()); a=audita(str(s),str(l))
    assert r['rc']==0 and a['auditoria']=='PASSA'
    assert r['source_sha256']==sha(s) and r['log_sha256']==sha(l)
    assert not r['newer_kernel_files'] and not r['scan_errors']
    proofs.append(dict(source=str(s),source_sha256=sha(s),log=str(l),log_sha256=sha(l),
                       receipt_sha256=sha(rp),receipt=r,audit=a))
attempts=[]
for pattern in ['trace_infinity_*.json','modular_boost_energy_*.json',
                'modular_charge_link_*.json','existing_trace_completion_*.json']:
    for p in HERE.glob(pattern):
        d=json.loads(p.read_bytes())
        if 'rc' in d: attempts.append(dict(path=str(p),sha256=sha(p),receipt=d))
reuse=json.loads((HERE/'modular_boost_energy_reuse.json').read_bytes())
origin=Path(reuse['source']); assert sha(origin)==reuse['source_sha256']
block='\n'.join(origin.read_text(encoding='utf-8-sig').splitlines()[reuse['start_line']-1:reuse['end_line']])
assert hashlib.sha256(block.encode()).hexdigest()==reuse['block_sha256']
assert block in (HERE/'ModularBoostEnergyReuse_v2.lean').read_text()
deps=[]
for p in [ROOT/'A1/minimal_imports/ContratoQG_v31_Minimal.lean',origin,
          KERNEL/'TGL/ModularRealization.lean',
          KERNEL/'TGLExt/V354TraceReaderWall.lean',
          KERNEL/'TGLExt/V354CyclicTraceCompletion.lean',
          KERNEL/'TGLExt/V354PositiveShiftCompatibility.lean',
          KERNEL/'TGLExt/V354RegularLegacyWitness.lean',
          KERNEL/'.lake/build/lib/lean/TGLExt/V354RegularLegacyWitness.olean']:
    deps.append(dict(path=str(p),sha256=sha(p)))
now=datetime.now(timezone.utc).isoformat()
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
paper=dict(url='https://arxiv.org/html/1703.10656v4',
           title='Modular Hamiltonians on the null plane and the Markov property of the vacuum state',
           authors='Casini, Testé, Torroba',version='v4, 14 Aug 2024; trabalho de 2017',
           inspected_at=now,read_scope='Introdução eqs.1.4–1.7; §§3.4, 5.4 e início de §6; não leitura integral.',
           locators=['1.5: carga unilateral, lambda do corte até infinito',
                     '1.6–1.7: diferença regional-complementar e integral bilateral',
                     '3.4/5.4: extensão por deformações conformes relevantes',
                     '6: hipóteses sobre rede; resultado algébrico não fornece fórmula explícita de T'],
           application='Aplicar ao tensor específico da bancada requer identificação adicional; esta consulta não a prova.')
save(HERE/'ctt_primary_source_audit.json',paper)
entries=sum(x['audit']['n_declaracoes_auditadas'] for x in proofs)
wall=sum(x['receipt']['wall_seconds'] for x in attempts)
cpu=sum(x['receipt']['cpu_user_seconds']+x['receipt']['cpu_kernel_seconds'] for x in attempts)
manifest=dict(at=now,status='REAL_SCOPED_A5C_MEASURE_AND_A5CP_CONDITIONAL',opening_sha256=opening,
              proofs=proofs,attempts=attempts,dependencies=deps,reuse=reuse,
              audited_entries=entries,new_local_theorems=9,reused_proof_bodies=2,
              existing_imported_declarations_audited=3,wall_seconds=wall,cpu_seconds=cpu,
              primary_source_audit_sha256=sha(HERE/'ctt_primary_source_audit.json'),
              full_kernel_rebuild=False,physical_stress_identification_discharged=False,gate_changed=False)
assert entries==14
save(HERE/'modular_charge_measure_manifest.json',manifest)
ledger=OUT/'LEDGER_016.jsonl'
rows=[json.loads(x) for x in ledger.read_text(encoding='utf-8-sig').splitlines() if x.strip()]
prices={}
for e in rows:
    key=e.get('execution_id') or e.get('job_id') or e.get('request_id')
    value=e.get('cost_estimate_usd',e.get('custo_usd'))
    # Preserve prior accounting: one known provider cost per coordination job.
    key=e.get('job_id') or e.get('request_id') or key
    if key and value is not None:
        try: prices[key]=Decimal(str(value))
        except Exception: pass
cost=sum(prices.values(),Decimal(0))
report=f'''[REAL — compilação e auditoria de módulos; DERIVED condicional; KNOWN com escopo]
# A5.c/c′ — Elo modular: reutilização e dívida delimitada
Abertura SHA256 `{opening}`.

**Parte já existente:** `modularEnergy_of_boostEnergy` e `modularEnergy_unique`
foram reutilizados literalmente da v3.1 e compilados. Sob BW do contrato,
a regra da cadeia dá k=2πb. Nenhuma segunda teoria de reconhecimento foi criada.

**Ponte condicional compilada:** se a expectativa do boost de cada estado
admissível é a carga do tensor T, então `ModularChargeLink C T A` vale.
O nome é exatamente o campo modular_charge do contrato. A hipótese suficiente
também exige existência da derivada para os estados da classe. Ela permanece
hipótese; não foi apresentada como tensor local construído.

**Controle negativo:** o tensor zero satisfaz o tipo fraco StressTensorData
(vácuo e covariância), mas viola ModularChargeLink em qualquer classe com
testemunha de energia modular não nula. Isso mede que o tipo de T, isolado,
não descarrega o elo. Não é refutação de um T₀ físico fornecido.

**Traço — parte já resolvida no kernel:** a extensão ingênua por infinito
fora do cone positivo falha: X=[[1,1],[0,1]], P=diag(1,0), τ(XP)=1,
τ(PX)=∞. Seis lemas compilados. Esse não é o leitor canônico existente.
`cyclicTraceCandidate` usa classes ShiftRelated; o kernel já prova ciclicidade
e acordo com o peso positivo, e `regularLegacyCore` habita ContinuousCoreData.
Os três símbolos foram carregados e tiveram axiomas auditados nesta rodada.
Não recompilamos suas fontes/dependências nem inferimos linearidade complexa
global de um leitor ENNReal. Não há nova dívida do leitor legado por causa
do contraexemplo específico. Correções por cima dos originais: nenhuma.

**Fonte primária:** CTT, eqs.1.5–1.7, confirma a distinção unilateral/bilateral.
O lado bilateral tem a forma do contrato no corte zero. A consulta não identifica
o tensor específico nem transforma a realização de uma partícula em rede local.
Fonte e recorte lidos: https://arxiv.org/html/1703.10656v4
(v4 de 2024 do trabalho de 2017; não alegamos leitura integral).

**Estado:** A5.c MEDIDA: falta identificar a carga de T₀ com a expectativa
do boost na realização física e no domínio adequado. A5.c′ PAGO no escopo
de hipótese nomeada e implicação suficiente. Não selecionamos os índices
(W,R,N,T), nem alteramos o gate. Segue A5.d e depois a composição A5.e.

Validação: {entries} entradas = 9 lemas locais novos + 2 corpos reutilizados
+ 3 declarações canônicas importadas; {len(attempts)} tentativas preservadas.
Finais rc0 e somente propext/Classical.choice/Quot.sound; kernel sem alterações.
Falhas preservadas: decidibilidade do predicado, simplificação excessiva,
notação de produto interno e import que não carregava os símbolos legados.
Máquina: {wall:.6f}s parede / {cpu:.6f}s CPU. Bancada não cronometrada
exclusivamente. Estimativas remotas conhecidas acumuladas: US${cost}, incompletas;
nenhuma nova execução de provedor nesta entrega. Preparo/fila não é consumo medido.

Manifesto: `{HERE/'modular_charge_measure_manifest.json'}`.
SHA256 do manifesto: `{sha(HERE/'modular_charge_measure_manifest.json')}`.
'''
save(OUT/'ENTREGA_016_MEDIDA_A5c_elo_modular_e_traco.md',report)
listing=[dict(name=p.name,mtime_ns=p.stat().st_mtime_ns,sha256=sha(p))
         for p in INCOMING.iterdir() if p.is_file() and p.suffix=='.md']
save(HERE/'incoming_at_modular_charge_delivery.json',listing)
progress=OUT/'ENTREGA_016_PROGRESSO.md'
tag='A5C_MEASURE_A5CP_CONDITIONAL_20260924'
if tag not in progress.read_text(encoding='utf-8-sig'):
    text=progress.read_text(encoding='utf-8-sig')
    text+=f'\n- {now} — A5.c MEDIDA / A5.c′ PAGO condicional: {entries} entradas, {len(attempts)} tentativas; traço cíclico legado reutilizado e auditado, extensão por infinito recusada. Máquina {wall/3600:.6f}h parede/{cpu/3600:.6f}h CPU; bancada não exclusiva. Estimativas US${cost}, incompletas. PARA_CHATGPT: sem novo adendo posterior a ADENDO_016_001; bloco de índices continua sem ratificação. Não move gate; próximo A5.d. [{tag}]\n'
    save(progress,text)
print(json.dumps({'entries':entries,'attempts':len(attempts),'wall_seconds':wall,
                  'cpu_seconds':cpu,'known_estimated_usd':str(cost),
                  'report':str(OUT/'ENTREGA_016_MEDIDA_A5c_elo_modular_e_traco.md')}))
