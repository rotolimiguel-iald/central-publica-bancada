from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json,sys
HERE=Path(__file__).resolve().parent
OUT=HERE.parents[1]/'TUNEL/DO_CHATGPT'
sys.path.insert(0,str(HERE.parent/'A0'))
from auditar_axiomas import audita
now=datetime.now(timezone.utc);stamp=now.strftime('%Y%m%d_%H%M%S_%f')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,b):
    if p.exists():
        old=p.read_bytes();bk=p.with_name(p.name+'.bak_'+stamp)
        with bk.open('xb') as f:f.write(old)
        assert bk.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+stamp)
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b and b
    t.replace(p)
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
units=[('OrbitalRapidityTransport_v3.lean','orbital_transport_03'),('OrbitalL2Equivalence_v2.lean','orbital_l2_equivalence_02'),('OrbitalBoostTransport.lean','orbital_boost_transport_01'),('ProductOrbitalSpectrum_v3.lean','product_orbital_spectrum_03'),('IsometricCocycleSpectrum_v2.lean','isometric_cocycle_01')]
proofs=[]
for src,label in units:
    s=HERE/src;l=HERE/(label+'.log');r=json.loads((HERE/(label+'.json')).read_text(encoding='utf8'));a=audita(str(s),str(l))
    assert r['rc']==0 and not r['newer_kernel_files'] and not r['scan_errors']
    assert sha(s)==r['source_sha256'] and sha(l)==r['log_sha256'] and a['auditoria']=='PASSA'
    proofs.append(dict(source=str(s),source_sha256=sha(s),log_sha256=sha(l),receipt=r,audit=a))
attempts=[]
for prefix,count in [('orbital_transport',3),('orbital_l2_equivalence',2),('orbital_boost_transport',1),('product_orbital_spectrum',3),('isometric_cocycle',1)]:
    for i in range(1,count+1):
        label=f'{prefix}_{i:02}';p=HERE/(label+'.json');r=json.loads(p.read_text(encoding='utf8'))
        attempts.append(dict(label=label,rc=r['rc'],wall=r['wall_seconds'],cpu=r['cpu_user_seconds']+r['cpu_kernel_seconds'],sha256=sha(p)))
dependencies=[]
for name,label in [('RapidityJacobian_v2.lean','rapidity_jacobian_02'),('OrbitalRapidityMeasure_v4.lean','orbital_measure_04'),('VectorRapiditySpectrum.lean','vector_rapidity_01')]:
    p=HERE/name;r=json.loads((HERE/(label+'.json')).read_text(encoding='utf8'))
    assert r['rc']==0 and sha(p)==r['source_sha256']
    dependencies.append(dict(path=str(p),sha256=sha(p),receipt_sha256=sha(HERE/(label+'.json'))))
# Price estimates are deduplicated by job; an observed failed/unknown receipt supersedes an earlier zero.
prices={};unknown=set()
for line in (OUT/'LEDGER_016.jsonl').read_text(encoding='utf8').splitlines():
    e=json.loads(line);key=e.get('job_id') or e.get('request_id')
    if not key:continue
    price=e.get('cost_estimate_usd',e.get('custo_usd'))
    if price is not None:
        try:prices[key]=Decimal(str(price));unknown.discard(key)
        except Exception:pass
    elif e.get('desfecho')=='failed' or 'UNMETERED' in str(e):
        prices.pop(key,None);unknown.add(key)
# Current authoritative terminal failure already observed in the queue, cost not reported.
uncertain_job='bcacca23-9116-4043-8b69-ac7264009303'
prices.pop(uncertain_job,None);unknown.add(uncertain_job)
cost=dict(known_explicit_estimates_usd=str(sum(prices.values(),Decimal(0))),unknown_jobs=sorted(unknown),scope='NOT_INVOICE_NOT_COMPLETE_TOTAL',per_job={k:str(v) for k,v in prices.items()})
n=sum(p['audit']['n_declaracoes_auditadas'] for p in proofs)
wall=sum(p['wall'] for p in attempts);cpu=sum(p['cpu'] for p in attempts)
incoming=HERE.parents[1]/'TUNEL/PARA_CHATGPT'
listing=[dict(name=p.name,size=p.stat().st_size,mtime_ns=p.stat().st_mtime_ns) for p in incoming.iterdir() if p.is_file()]
manifest=dict(status='REAL',utc=now.isoformat(),opening_sha256=opening,proofs=proofs,dependencies=dependencies,attempts=attempts,declarations=n,cost=cost,incoming_listing=listing,pending=['Pointwise to operator translation faithfulness','Physical helicity representation/cocycle realization','Positive energy analytic form','Full Poincare/BW/Fock construction'])
save(HERE/'l2_boost_spectrum_manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2).encode())
report=f'''[REAL — equivalência L², entrelaçamento e ausência de autovetores escalares compilados]

# ORDEM 016 — do jacobiano ao operador de boost

UTC {now.isoformat()}; ABERTURA sha256 `{opening}`.

**Resultado:** {n} declarações auditadas, em cinco arquivos finais. Todas
compilaram com rc0, axiomas contidos no trio e nenhuma admissão. A inversa
foi construída; a equivalência L² não é uma hipótese.

1. `orbitalL2Equivalence m` leva L²(d³p/p₀;E) nas coordenadas orbitais
   construídas a L²(d²q dξ;E), linear e isometricamente, com inversa.
2. `coordinateBoost` age por p₁↦cosh(s)p₁+sinh(s)sqrt(m⊥²+p₁²).
   Ele preserva a medida ponderada. `orbitalScalarBoost` é a composição
   pelo boost inverso, um operador L² efetivamente definido.
3. `orbitalScalarBoost_intertwines` prova T B_s = D_s T. A composição
   B_(s+t)=B_s B_t foi provada. Não é uma igualdade imposta na definição
   de B: B é definido nas coordenadas de momento e comparado depois.
4. `orbitalScalarBoost_no_eigen`: se, para cada s real, B_s f=c_s f e
   |c_s|=1, então f=0. O mesmo resultado cobre m=0 e todo m>0. O argumento
   existente de intervalos inteiros foi reutilizado por Tonelli; não foi
   postulado espectro contínuo para obter ausência de autovetores.
5. Para ação com isometrias C_s(q,ξ) na fibra, a hipótese a.e.
   C_s(q,ξ)f(q,ξ−s)=c_s f(q,ξ) também implica f=0. Não supõe C_s=I;
   shifts inteiros já bastam. A construção física/mensurabilidade/cociclo
   das helicidades NÃO é conclusão desse lema.

**Três ramos, sem troca de tipo:** o resultado escalar é efetivo no cone
sem massa e no hiperboloide massivo em coordenadas. Para o fóton ±1,
o controle normativo está provado para toda ação isométrica com a forma
especificada; permanece fornecer a representação de helicidade concreta.
Um espaço de duas componentes com boost escalar não é automaticamente
essa representação. Os conjuntos excluídos de medida zero e as inversas
a.e. estão cobertos pelos lemas anteriores, incluídos por hash no manifesto.

**Ainda não pago:** fidelidade das translações como operadores L², energia
positiva na forma analítica, ligação integral com a representação de
Poincaré/BW e segunda quantização. H2 e A3 completos não são reivindicados;
nenhum gate/original foi alterado. O 2π não entrou por nova definição aqui.

**Verificação:** {len(attempts)} compilações neste bloco, {wall:.6f}s parede,
{cpu:.6f}s CPU, no máximo três versões por arquivo; tentativas falhas
preservadas. Logs, comandos, hashes e cobertura de declarações:
`A3/l2_boost_spectrum_manifest.json`. Oito lemas do boost passaram de primeira.

**Orquestração:** MiMo 6cdeb9a0-20f7-45af-8b96-4bf5bb35c8f2 e Kimi
f8ec22e7-21c2-4bf4-b3bc-29655e681481 continuam aguardando autorização
específica de envio pedida pela coordenadora após rejeição automática.
Não foram repetidos nem enviados por outra rota. A prova local do
controle normativo agora permite confrontar eventual rascunho MiMo.
DeepSeek cancelado permanece sem execução.

Estimativas explícitas conhecidas, deduplicadas: US$ {cost['known_explicit_estimates_usd']}.
Não é total faturado: {len(unknown)} jobs têm custo não informado. Correção
contábil ao lado: zero histórico do MiMo interrompido não é consumo zero.
Não houve chamada externa nova nesta rodada. Fine-tuning continua adiado.

**Próximo:** completar a ligação de fidelidade L² e a forma de representação
de helicidade; depois seguir energia positiva/boost no ramo principal,
conforme a árvore. Listagem do túnel conferida e guardada no manifesto.
'''
save(OUT/'ENTREGA_016_MEDIDA_A3_4_L2_boost_espectro.md',report.encode())
p=OUT/'ENTREGA_016_PROGRESSO.md'
save(p,p.read_bytes()+f'\n{now.isoformat()} | A3.4: +{n} declarações auditadas; equivalência L2 e boost escalar sem autovetores m=0/m>0, cociclo isométrico condicional. Helícidades físicas e H2 ainda não pagos. Máquina {wall/3600:.6f}h parede/{cpu/3600:.6f}h CPU. Sem novas chamadas; estimativas conhecidas {cost["known_explicit_estimates_usd"]} USD, custos desconhecidos preservados.\n'.encode())
print(json.dumps(dict(status='PASSA',declarations=n,wall_seconds=wall,cpu_seconds=cpu,cost=cost),ensure_ascii=False))
