from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
import hashlib,json,sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
OUT=ROOT.parent/'TUNEL/DO_CHATGPT'
sys.path.insert(0,str(ROOT/'A0'))
from auditar_axiomas import audita
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,raw):
    if isinstance(raw,str):raw=raw.encode('utf-8')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    if p.exists():
        old=p.read_bytes();bk=p.with_name(p.name+'.bak_'+stamp)
        with bk.open('xb') as f:f.write(old)
        assert bk.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp_'+stamp)
    with tmp.open('xb') as f:f.write(raw)
    assert tmp.read_bytes()==raw and raw
    tmp.replace(p)
def dump(p,obj):save(p,json.dumps(obj,ensure_ascii=False,indent=2))

now=datetime.now(timezone.utc).isoformat()
src=HERE/'HorizonDataReuse.lean';log=HERE/'horizon_data_02.log';rp=HERE/'horizon_data_02.json'
r=json.loads(rp.read_bytes());audit=audita(str(src),str(log))
assert r['rc']==0 and r['source_sha256']==sha(src) and r['log_sha256']==sha(log)
assert r['newer_kernel_files']==[] and r['scan_errors']==[] and audit['auditoria']=='PASSA'
reuse=json.loads((HERE/'horizon_reuse_source.json').read_bytes())
origin=Path(reuse['source']);assert sha(origin)==reuse['source_sha256']
origin_text=origin.read_text(encoding='utf-8-sig');target=src.read_text(encoding='utf-8-sig')
for block in reuse['reused']:
    text='\n'.join(origin_text.splitlines()[block['start_line']-1:block['end_line']])
    assert hashlib.sha256(text.encode()).hexdigest()==block['block_sha256']
    assert text in target
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
assert opening==r['opening_sha256']
incident=dict(status='SETUP_FAILURE_NOT_MATHEMATICAL_REFUTATION',
    detail='A geração falhou na extração de feeds_the_master antes de criar a fonte. '
           'O comando seguinte foi indevidamente iniciado; Lean registrou fonte inexistente. '
           'O runner terminou exit1 ao tentar ler a fonte ausente; sem recibo completo.',
    log=str(HERE/'horizon_data_01.log'),log_sha256=sha(HERE/'horizon_data_01.log'),
    wall_seconds=None,cpu_seconds=None,mathematical_proof_attempt=False)
dump(HERE/'horizon_setup_incident.json',incident)
manifest=dict(status='REAL_SCOPED_A5A_REUSE',at=now,opening_sha256=opening,
    source=str(src),source_sha256=sha(src),log=str(log),log_sha256=sha(log),
    receipt=r,receipt_sha256=sha(rp),audit=audit,reuse= reuse,
    incident=incident,scope='Conditional consumer of existing H3, not H2-to-H3 existence')
dump(HERE/'horizon_data_manifest.json',manifest)

units=json.loads((HERE/'orchestration_propagator_20260924/prepared_units.json').read_bytes())
ledger=OUT/'LEDGER_016.jsonl';before=ledger.read_bytes();entries=[json.loads(x) for x in before.decode('utf-8-sig').splitlines()]
added=[]
for u in units:
    if any(e.get('request_id')==u['request_id'] and e.get('event')=='unit_prepared' for e in entries):continue
    p=json.loads(Path(u['payload']).read_bytes())
    added.append(dict(ts=now,event='unit_prepared',provedor=u['provider'],alvo='A-5',ramo='A-5.b',
        request_id=u['request_id'],question_sha256=hashlib.sha256(p['prompt'].encode()).hexdigest(),
        answer_sha256=None,provider_calls_observed=0,custo_usd=None,
        desfecho='prepared_handed_to_coordinator_pending_queue_capacity'))
if added:save(ledger,before+''.join(json.dumps(e,ensure_ascii=False)+'\n' for e in added).encode())
prices={}
for e in entries:
    k=e.get('job_id') or e.get('request_id');v=e.get('cost_estimate_usd',e.get('custo_usd'))
    if k and v is not None:
        try:prices[k]=Decimal(str(v))
        except Exception:pass
cost=sum(prices.values(),Decimal(0))
wall=r['wall_seconds'];cpu=r['cpu_user_seconds']+r['cpu_kernel_seconds']
report=f'''[REAL — compilação isolada; DERIVED condicional]
# A5.a — Dados do MESMO horizonte, por reaproveitamento

Abertura SHA256 `{opening}`.

`HorizonDataReuse.lean` compilou rc0: {audit['n_declaracoes_auditadas']} declarações,
{audit['n_theorem_lemma_na_fonte']} theorem/lemma, somente propext/Classical.choice/Quot.sound.
Nove declarações do contrato v3.1 foram reutilizadas com corpo exato; duas composições
novas explicitam os campos e a temperatura no mesmo período. Não há tipo paralelo
de HorizonEquilibriumData nem novo habitante físico H3.

| Campo | Origem e estatuto |
|---|---|
| κ | `C.H2.kappa`, do mesmo W/R/N. Período P e fidelidade angular positivos ⇒ κ/(2π)=1/P; a faixa KMS regional/BW continua no contrato H2. |
| G | `C.G>0`, INPUT fixo antes de ψ; nenhum valor previsto. |
| dA | `windowArea (C.response ψ) x c d`, resposta do mesmo H3 e gerador nulo. |
| dS | `2π*windowCharge T ψ x c d`; leitura unilateral definida sobre o tensor T indexado. |
| dQ | `κ*windowCharge T ψ x c d`; Clausius segue das definições. |
| area_entropy | Derivada de `theta_is_expansion`, `raychaudhuri_einstein` e condição final θ(d)=0; T contínuo no gerador. Não deriva a lei de Einstein sem essa hipótese. |
| ligação mestre | `feeds_the_master` consome H1, o frame de C.H2 e estes dados, preservando suas hipóteses. |

**A5.a PAGO no escopo de discriminar e ligar os dados.** `toHorizonData` recebe
`ContratoH3`, não apenas H2. Construir a resposta/elo modular permanece em A5.b–e.
Não move gate nem altera kernel/originais.

Fonte SHA256 `{sha(src)}`; log `{sha(log)}`.
Manifesto `{HERE/'horizon_data_manifest.json'}` SHA256 `{sha(HERE/'horizon_data_manifest.json')}`.
Máquina: {wall:.6f}s parede, {cpu:.6f}s CPU na compilação válida.
Tentativa `_01`: falha de preparação por fonte inexistente; log preservado,
tempo não medido, não convertido em prova ou custo zero.
Custódia A4 independente recebida: conferência de hashes/recibos, sem nova execução ou revisão semântica.

**Orquestração:** 2 novas unidades Kimi (contorno/unicidade; matriz/covariância)
e 1 MiMo (rascunho Lean das integrais) preparadas e entregues ao coordenador.
Previews selecionaram os provedores exigidos com memória comum. Ainda aguardam
vaga na fila única; preparação não equivale a chamada nem resultado.
Estimativas explícitas acumuladas do ledger: US${cost}; não fatura, assinaturas
e consumos não informados excluídos. Próximo: A5.b, propagador teleológico.
'''
save(OUT/'ENTREGA_016_A5a_dados_mesmo_horizonte.md',report)
progress=OUT/'ENTREGA_016_PROGRESSO.md';tag='A5A_REUSE_20260924'
if tag.encode() not in progress.read_bytes():
    save(progress,progress.read_bytes()+f'\n- {now} — A5.a PAGO no escopo: 11 declarações auditadas (9 reutilizadas, 2 composições), H3 ainda condição. Máquina {wall/3600:.6f}h parede/{cpu/3600:.6f}h CPU; preparação anterior não medida. Estimativas explícitas US${cost}, incompletas. 2 Kimi+1 MiMo preparados para vagas; não move gate. [{tag}]\n'.encode())
print(json.dumps(dict(audit=audit['auditoria'],entries=audit['n_declaracoes_auditadas'],
    report=str(OUT/'ENTREGA_016_A5a_dados_mesmo_horizonte.md'),prepared=len(units),cost=str(cost))))
