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
def save(p,value):
    raw=value.encode('utf-8') if isinstance(value,str) else json.dumps(value,ensure_ascii=False,indent=2).encode('utf-8')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    if p.exists():
        old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+stamp);bak.write_bytes(old);assert bak.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp_'+stamp);tmp.write_bytes(raw);assert tmp.read_bytes()==raw and raw;tmp.replace(p)
proofs=[]
for name,label in [('BilateralFirstOrderReuse.lean','bilateral_first_order_01'),('NormalizedFirstOrder_v3.lean','normalized_first_order_03')]:
    src=HERE/name;log=HERE/(label+'.log');rp=HERE/(label+'.json');r=json.loads(rp.read_bytes());a=audita(str(src),str(log))
    assert r['rc']==0 and a['auditoria']=='PASSA' and not r['newer_kernel_files'] and not r['scan_errors']
    assert r['source_sha256']==sha(src) and r['log_sha256']==sha(log)
    proofs.append(dict(source=str(src),source_sha256=sha(src),log=str(log),log_sha256=sha(log),receipt_sha256=sha(rp),receipt=r,audit=a))
attempts=[]
for pattern in ['bilateral_first_order_*.json','normalized_first_order_*.json']:
    for p in HERE.glob(pattern):
        d=json.loads(p.read_bytes())
        if 'rc' in d:attempts.append(dict(path=str(p),sha256=sha(p),receipt=d))
reuse=json.loads((HERE/'bilateral_first_order_reuse.json').read_bytes());src=Path(reuse['source']);assert sha(src)==reuse['source_sha256']
lines=src.read_text(encoding='utf-8-sig').splitlines();target=Path(reuse['target']);assert sha(target)==reuse['target_sha256']
for b in reuse['blocks']:
    block='\n'.join(lines[b['start_line']-1:b['end_line']]);assert hashlib.sha256(block.encode()).hexdigest()==b['block_sha256'] and block in target.read_text()
harnesses=[]
for name in ['two_body_first_order_exact','two_body_first_order_exact_v2']:
    sp=HERE/(name+'.py');rp=HERE/(name+'.json');r=json.loads(rp.read_bytes());assert r['all_passed'] and r['source_sha256']==sha(sp)
    harnesses.append(dict(source=str(sp),source_sha256=sha(sp),result=str(rp),result_sha256=sha(rp),receipt=r))
wall=sum(x['receipt']['wall_seconds'] for x in attempts+harnesses)
cpu=sum(x['receipt']['cpu_user_seconds']+x['receipt']['cpu_kernel_seconds'] for x in attempts)+sum(x['receipt']['cpu_seconds'] for x in harnesses)
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md');now=datetime.now(timezone.utc).isoformat()
manifest=dict(at=now,status='REAL_A5D_SCOPED_FIRST_ORDER',opening_sha256=opening,proofs=proofs,attempts=attempts,reuse=reuse,
              harnesses=harnesses,lean_audit_entries=9,final_exact_checks=33,wall_seconds=wall,cpu_seconds=cpu,
              physical_tensor_identified=False,entropy_derivative_proved=False,gate_changed=False)
save(HERE/'first_order_manifest.json',manifest)
prices={}
for e in map(json.loads,(OUT/'LEDGER_016.jsonl').read_text(encoding='utf-8-sig').splitlines()):
    k=e.get('job_id') or e.get('request_id');v=e.get('cost_estimate_usd',e.get('custo_usd'))
    if k and v is not None:
        try:prices[k]=Decimal(str(v))
        except Exception:pass
cost=sum(prices.values(),Decimal(0))
report=f'''[REAL — cálculo exato e compilação; DERIVED no modelo de cargas especificado]
# A5.d — Primeira ordem unilateral versus bilateral
Abertura SHA256 `{opening}`.

Reutilizados literalmente três lemas da v3.1: Δit_vac, inner_vac_Δit e
bilateral_no_first_order. Eles demonstram, sob H2 e derivada de φ, energia
bilateral ε² kφ para Ω+εφ. O novo lema de normalização mantém derivada
zero em ε=0 para kφ ε²/(1+r ε²). Não foi substituído o contrato físico.

**Testemunho exato de dois corpos:** pacote f(k)=2√k exp(−k), k>0,
normalizado; Φ(k₁,k₂)=f(k₁)f(k₂) é simétrico e normalizado. Na compressão
aos setores |0>, |1_f>, |2_f>, N|2_f>=2|2_f>. O campo quadrático
normal ordenado foi definido explicitamente por
Q(u)=g(u)²a²+conj(g(u))²(a†)²+2|g(u)|²N,
g(u)=1/[√π(1+iu)²]. Essa convenção de carga é INPUT do harness.

As integrais convergentes dão ∫₀∞u g(u)²du=−1/(6π) e
∫₀∞u|g(u)|²du=1/(2π). Para H₊=2π∫₀∞uQ(u)du,
H₋=−2π∫₋∞⁰uQ(u)du, ψε=(|0>+ε|2_f>)/√(1+ε²),

    <H₊>ψε = (−2√2 ε/3 + 4ε²)/(1+ε²)
    d<H₊>/dε|₀ = −2√2/3 ≠ 0
    d<H₊−H₋>/dε|₀ = 0.

A segunda igualdade é geral no lema bilateral reutilizado; neste pacote
simétrico a compressão H₊−H₋ inteira zera. Isso NÃO diz que o boost
completo da teoria seja zero. O estado perturbado não é coerente para ε≠0:
o menor que testa proporcionalidade entre aψε e ψε é √2ε/(1+ε²).

**Controles:** fase relativa i ou retirada do termo de pares anulam a
derivada unilateral; trocar ε por −ε inverte seu sinal; normalizar não
muda o termo linear. Matriz hermitiana, vácuo subtraído e primeiro momento
absoluto das caudas conferidos. O abaixador é truncado e não foi anunciado
como representação completa de CCR. Não construímos Fock da rede, T₀ local
da TGL, covariância espacial completa nem derivada de entropia física.

**Estado A5.d:** PAGO como harness exato do mecanismo e reuso do teorema
bilateral; aplicação ao T₀ do mesmo par continua condicionada ao elo A5.c.
São 9 entradas Lean auditadas (3 reutilizadas, 6 locais), finais rc0/trio,
e 33 controles exatos no harness final. Tentativas anteriores preservadas;
as duas falhas do módulo novo decorreram de API de soma não importada e
conversão de instâncias, corrigidas sem hipóteses adicionais.
Máquina {wall:.6f}s parede/{cpu:.6f}s CPU; bancada não exclusiva.
Custos remotos explícitos acumulados US${cost}, incompletos; sem nova chamada.
Não move gate. Segue A5.e.

Manifesto: `{HERE/'first_order_manifest.json'}`
SHA256: `{sha(HERE/'first_order_manifest.json')}`.
'''
save(OUT/'ENTREGA_016_A5d_primeira_ordem_dois_corpos.md',report)
tag='A5D_FIRST_ORDER_EXACT_20260924';p=OUT/'ENTREGA_016_PROGRESSO.md';old=p.read_text(encoding='utf-8-sig')
if tag not in old:save(p,old+f'\n- {now} — A5.d PAGO no harness de cargas: 9 entradas Lean, 33 controles exatos; T0 físico não identificado. Máquina {wall/3600:.6f}h parede/{cpu/3600:.6f}h CPU, bancada não exclusiva. Estimativas US${cost}, incompletas. Não move gate; próximo A5.e. [{tag}]\n')
print(json.dumps({'lean_entries':9,'exact_checks':33,'attempts':len(attempts),'wall_seconds':wall,'report':str(OUT/'ENTREGA_016_A5d_primeira_ordem_dois_corpos.md')}))
