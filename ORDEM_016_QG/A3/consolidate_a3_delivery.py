from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, sys

HERE=Path(__file__).resolve().parent
OUT=HERE.parents[1]/'TUNEL/DO_CHATGPT'
INCOMING=HERE.parents[1]/'TUNEL/PARA_CHATGPT'
sys.path.insert(0,str(HERE.parent/'A0'))
from auditar_axiomas import audita
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,raw):
    stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    if p.exists():
        old=p.read_bytes(); b=p.with_name(p.name+'.bak_'+stamp)
        with b.open('xb') as f:f.write(old)
        assert b.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+stamp)
    with t.open('xb') as f:f.write(raw)
    assert t.read_bytes()==raw and raw
    t.replace(p)
names=['geometric_reuse_manifest.json','orbit_faithfulness_manifest.json',
       'vector_rapidity_manifest.json','orbital_measure_and_distribution_manifest.json',
       'l2_boost_spectrum_manifest.json','translation_operator_faithfulness_manifest.json',
       'energy_covariance_manifest.json']
proofs={}; manifests=[]
def inspect(d):
    if isinstance(d,dict):
        a=d.get('audit')
        if isinstance(a,dict) and a.get('fonte') and a.get('log'):
            source=Path(a['fonte']);log=Path(a['log'])
            current=audita(str(source),str(log))
            assert current['auditoria']=='PASSA',current
            assert current['fonte_sha16']==a['fonte_sha16']
            assert current['log_sha16']==a['log_sha16']
            if 'source_sha256' in d:assert sha(source)==d['source_sha256']
            if 'log_sha256' in d:assert sha(log)==d['log_sha256']
            receipt=log.with_suffix('.json');r=json.loads(receipt.read_text(encoding='utf8'))
            assert r['rc']==0 and not r['newer_kernel_files'] and not r['scan_errors']
            assert r['source_sha256']==sha(source) and r['log_sha256']==sha(log)
            proofs[str(source)]=dict(source=str(source),source_sha256=sha(source),log=str(log),
                log_sha256=sha(log),receipt_sha256=sha(receipt),audit=current)
        for v in d.values():inspect(v)
    elif isinstance(d,list):
        for v in d:inspect(v)
for name in names:
    p=HERE/name;d=json.loads(p.read_text(encoding='utf8'));inspect(d)
    manifests.append(dict(path=str(p),sha256=sha(p)))
attempts=[]
for p in HERE.glob('*.json'):
    d=json.loads(p.read_text(encoding='utf8'))
    if isinstance(d,dict) and all(k in d for k in ['command','rc','wall_seconds','source_sha256','cpu_user_seconds']):
        attempts.append(dict(path=str(p),sha256=sha(p),rc=d['rc'],utc=d['utc'],wall=d['wall_seconds'],
                             cpu=(d['cpu_user_seconds'] or 0)+(d['cpu_kernel_seconds'] or 0)))
now=datetime.now(timezone.utc)
count=sum(p['audit']['n_declaracoes_auditadas'] for p in proofs.values())
wall=sum(a['wall'] for a in attempts);cpu=sum(a['cpu'] for a in attempts)
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
incoming=[dict(name=p.name,sha256=sha(p),mtime_ns=p.stat().st_mtime_ns) for p in INCOMING.iterdir() if p.is_file()]
result=dict(status='REAL_SCALAR_ACCEPTANCE_WITH_PHOTON_MEASURE',utc=now.isoformat(),opening_sha256=opening,
    manifests=manifests,proofs=list(proofs.values()),declarations=count,attempts=attempts,
    machine_wall_seconds=wall,machine_cpu_seconds=cpu,incoming_listing=incoming,
    independent_provider_review='PENDING_NOT_INFERRED_FROM_COMPILATION',
    photon='ISOMETRIC_COCYCLE_NORM_THEOREM_ONLY_PHYSICAL_CONSTRUCTION_PENDING',
    fock='OUTSIDE_ORDER_NOT_A_NEW_BRANCH',gate='UNCHANGED')
save(HERE/'a3_consolidated_manifest.json',json.dumps(result,ensure_ascii=False,indent=2).encode())
report=f'''[REAL — entrega consolidada A3; ramo escalar formalizado, helicidades em MEDIDA]

# ORDEM 016 — A3: representação e alcance de H2

UTC {now.isoformat()}; ABERTURA sha256 `{opening}`.

| Exigência | Resultado conferido |
|---|---|
| A3.0, tipo de massa | Namespace próprio; m=0 e m>0 tratados, sem retipar o kernel nem escolher partição |
| A3.d, frame | Frame suave/invertível na cunha, arrastado pelo boostMat existente; N fornecido |
| A3.1, fidelidade | U(a)=I no L² implica a=0; indicadores + suporte pleno + prova na órbita |
| A3.2, energia | Integral espectral positiva, holomorfa, limitada, contínua na borda; coeficiente do vetor L² efetivo |
| A3.3, boosts | Grupo unitário fortemente contínuo; covariância via boostMat; dilatação do raio nulo |
| A3.4, espectro | Sem autovetores nos setores escalares massivo/sem massa; fibras isométricas sob hipótese explícita |
| A3.5, vácuo | Não existe vetor normalizado fixo pelos boosts no setor de uma partícula; null_ergodic isolado não foi refutado |

**Aceitação do principal A3.b:** os subalvos 1–4 estão demonstrados no espaço orbital,
e o 5 foi medido com a precisão acima. O setor escalar massivo reutiliza os mesmos
lemas parametrizados. A fibra dupla dá fidelidade, mas duas cópias escalares NÃO
identificam helicidades físicas ±1. Essa identificação continua NÃO PAGA; o teorema
do cociclo isométrico é condicional e a construção explícita foi atribuída ao Kimi.
Não foi declarado que os três ramos têm o mesmo estatuto.

**H2 completo permanece aberto.** Não há nesta entrega rede regional, identificação
BW do grupo modular, vácuo de Fock ou identificação com o horizonte físico da TGL.
A ordem §5.9 coloca Fock fora desta missão. Correção ao lado da linha de progresso
anterior: Fock NÃO é o próximo ramo a executar; após esta MEDIDA segue A4,
enquanto se recebe a revisão/construção pendente de A3.c. Nenhum 2π modular foi
obtido simplesmente redefinindo a rapidez.

**Custódia reconferida:** {count} declarações em {len(proofs)} fontes finais distintas,
rc0 e auditoria de axiomas refeita a partir de fontes/logs atuais. Os {len(attempts)}
recibos de compilação A3, inclusive falhas, somam {wall/3600:.6f} h parede e
{cpu/3600:.6f} h CPU. Não houve recompilação nesta consolidação. Manifesto:
`A3/a3_consolidated_manifest.json`, com hashes completos e listagem de PARA_CHATGPT.

As críticas remotas ainda aguardam conclusão; compilação não equivale a revisão
independente do alcance. Despacho é conduzido pela tarefa coordenadora única.
Originais, um.py, kernel e gate intactos. Move a construção orbital, não fecha H2
nem altera o gate. Próximo: A4k.1–A4k.3.
'''
save(OUT/'ENTREGA_016_A3_H2_par_fisico.md',report.encode())
p=OUT/'ENTREGA_016_PROGRESSO.md'
line=f'\n{now.isoformat()} | A3 CONSOLIDADO: {count} declarações/{len(proofs)} fontes reconferidas; principal escalar subalvos 1–4 e vácuo MEDIDA, cociclo físico A3.c NÃO PAGO. Fock fora da ordem; próximo A4, correção ao lado da linha anterior. Custódia sem recompilar; máquina acumulada A3 {wall/3600:.6f}h parede/{cpu/3600:.6f}h CPU (não somar novamente às entregas). Críticas externas em curso/pendentes, custos novos ainda não recebidos.\n'
save(p,p.read_bytes()+line.encode())
print(json.dumps(dict(status='PASSA',declarations=count,sources=len(proofs),attempts=len(attempts),wall_seconds=wall,cpu_seconds=cpu)))
