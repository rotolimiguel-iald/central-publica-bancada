"""Audit isolated D5 evidence and record its conditional scope."""
from pathlib import Path
from datetime import datetime, timezone
import json, re, sys
R=Path(__file__).resolve().parents[1]; D=R/'D5'; OUT=R.parent/'TUNEL/DO_CHATGPT'
sys.path.insert(0,str(R))
from prepare_part_d import sha,save,write
now=datetime.now(timezone.utc); proofs=[]
for fn,label,count in [('DilationGeometry_v2.lean','dilation_02',5),('DilationModularRecognition_v2.lean','recognition_01',2)]:
    p=D/fn; rp=D/(label+'.json'); log=D/(label+'.log'); x=json.loads(rp.read_bytes())
    assert x['rc']==0 and x['source_sha256']==sha(p) and x['log_sha256']==sha(log)
    assert not x['newer_kernel_files'] and not x['scan_errors']
    s=log.read_text('utf-8-sig'); assert 'sorryAx' not in s and ': error' not in s
    ax=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",s,re.S)
    assert len(ax)==count and all({a.strip() for a in v.split(',')}<={'propext','Classical.choice','Quot.sound'} for _,v in ax)
    proofs.append(dict(source=str(p),source_sha256=sha(p),receipt_sha256=sha(rp),log_sha256=sha(log),declarations=dict(ax)))
attempts=[json.loads((D/(v+'.json')).read_bytes()) for v in ['dilation_01','dilation_02','recognition_01']]
r=dict(at=now.isoformat(),status='D5_MEDIDA_GEOMETRY_AND_CONDITIONAL_MODULAR_RECOGNITION',proofs=proofs,declarations=7,
    open_obligations=['PhotonDilationCovarianceMeasured: construct implementing unitary, vacuum preservation and net covariance','PairTomitaAnalyticRealizationMeasured for the selected physical photon pair'],
    controls=['zero dilation rejected'],photon_network_constructed=False,gate_changed=False,
    cpu_seconds=sum(x['cpu_user_seconds']+x['cpu_kernel_seconds'] for x in attempts),wall_seconds=sum(x['wall_seconds'] for x in attempts),
    bench_hours=(now-datetime.fromisoformat(json.loads((D/'START.json').read_bytes())['at'])).total_seconds()/3600,
    opening_sha256=sha(OUT/'ENTREGA_016_ABERTURA_operador.md'))
save(D/'RESULTS.json',r)
text=f'''[REAL — sete declarações compiladas; DERIVED condicional; OPEN — realização física da rede]

Abertura016SHA256: {r['opening_sha256']}

D5: MEDIDA. Dilatação positiva comuta com o boost e leva a cunha sobre ela mesma; o raio normalizador escala por r e κ por 1/r. O controle r=0 é recusado. Geometria: cinco declarações. Reconhecimento modular: duas declarações, rc0 e axiomas apenas propext, Classical.choice, Quot.sound. Fontes, recibos e hashes em D5/RESULTS.json.

O teorema reutiliza D6: dado um unitário D que preserve o vácuo e implemente a covariância da rede sob dilatação, e uma realização analítica do par de Tomita, reconhece D J D*=J e D σ_t D*=σ_t na mesma cunha. Não põe essas duas conclusões como premissas. Não constrói D nem prova a covariância da rede selecionada: dívida PhotonDilationCovarianceMeasured, acompanhada da realização PairTomitaAnalyticRealizationMeasured física. Nenhuma dimensão fractal ou rede conforme foi deduzida de ausência de massa sozinha.

Reprodução: D5/start_and_compile.py <fonte> <rótulo novo>, compilador isolado com recibo. A geometria precisou de dois ciclos; a ponte de um. A primeira tentativa falhou na aplicação da desigualdade e normalização da divisão; preservada ao lado. CPU {r['cpu_seconds']:.6f}s; parede {r['wall_seconds']:.6f}s; bancada {r['bench_hours']:.6f}h, teto10h. Nenhum original, um.py ou gate alterado.

Próximo: Parte B, registro e controles da ORDEM015 antes de qualquer trabalho pesado.
'''
write(OUT/'ENTREGA_016_D5_dilatacao.md',text.encode())
q=OUT/'ENTREGA_016_PROGRESSO.md';write(q,q.read_bytes()+f'\n{now.isoformat()} — D5 MEDIDA:7 declarações, covariância física nomeada OPEN. Bancada {r["bench_hours"]:.6f}h CPU {r["cpu_seconds"]:.6f}s. PróximoB. AberturaSHA256 {r["opening_sha256"]}.\n'.encode(),True)
q=R/'A7/CONTINUIDADE.json';c=json.loads(q.read_bytes());c.update(at=now.isoformat(),own_live_process=None,own_live_processes=[],D5_delivery=str(D/'RESULTS.json'),next='Part B T03 master mutation controls and registration; no heavy clock before prerequisites. Three new remote payloads remain pending explicit specific approval.');save(q,c,True)
print(json.dumps({k:r[k] for k in ['status','declarations','cpu_seconds','bench_hours']}))
