from pathlib import Path
from datetime import datetime,timezone
import json,sys
D=Path(__file__).resolve().parent;B=D.parents[2];ROOT=B.parent;R=ROOT/'ORDEM_016_QG';OUT=ROOT/'TUNEL/DO_CHATGPT'
sys.path.insert(0,str(R))
from prepare_part_d import sha,write,save
x=json.loads((D/'RESULT.json').read_bytes());assert x['status']=='T05_NONBLIND_DIAGNOSTICS_COMPLETE' and all(t['passed'] for t in x['checks'])
now=datetime.now(timezone.utc).isoformat();opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
table=['| Cenário | R-B | R-MOD | R-RAIZ-0 | R-LIN |','|---|---:|---:|---:|---:|']
for det in ['O4','O5','ET','CE']:
    rs={r['reading']:r for r in x['forecast_rows'] if r['mode']=='440' and r['detector_scenario']==det and r['profile']=='FREE_FREQUENCY_FIXED_TAU_GR' and r['variant']=='BOTH_220_440_DEFORMED'}
    table.append('| '+det+' | '+' | '.join(f'{rs[n]["N90"]:.2f}' for n in ['R-B','R-MOD','R-RAIZ-0','R-LIN'])+' |')
text=f'''[REAL — dados arquivados NÃO-CEGOS; DERIVED sobre INPUT — projeção gaussiana condicional]

Abertura015SHA256: {sha(OUT/'ENTREGA_015_ABERTURA_operador.md')}
Abertura016SHA256: {opening}

T05 PAGO como diagnóstico. Âncora efetiva 440={x['anchors']['440']['rho_effective_H1L1_INPUT']:.12f}, derivada da largura90/3,289707 e Fisher com frequência livre. É proxy H1L1 otimista: assimetria {x['anchors']['440']['asymmetry']:.4f}, posterior truncado em +4, massa KDE fora1,146% e borda2,730%. Não mede o SNR real do modo. N físico=null. O220 foi calculado na mesma convenção, com sua própria largura de posterior e âncora efetiva {x['anchors']['220']['rho_effective_H1L1_INPUT']:.9f}.

N90 de fontes idênticas, independentes e sem sistemática, ambas as deformações admitidas, perfil de frequência livre:

{chr(10).join(table)}

N50=25/z² e N90={x['power_numerator']:.12f}/z². As240 linhas incluem todas as dez leituras, dois perfis, as variantes do440 e a comparação220, sem seleção. Correção ao lado: O5/R-B calculado2289,94 versus2284 na ordem; os números integrais reprodutíveis prevalecem. Ganhos de PSD individual transportam uma âncora de rede como INPUT, não uma previsão física de rede ou população.

Pareamento QNM:608681 draws em33 eventos220 e40776 no440/GW250114, sem spin fora da grade.340 linhas de predição, conservando pares de amostras. R-MOD recebeu QNM numérico da grade qnm0.4.4; permanece CONJECTURE, com erro de interpolação/validação herdado da grade, não QNM analítico exato. Implementações escalar e vetorial concordaram nos controles. Extrapolação foi recusada. O produtor E7 registrado não foi alterado; seu status também não. Incorporação exige a sub-emenda doT12.

Controle conjunto arquivado: corr(dtau220,dtau440)={x['joint_control']['corr_dtau220_dtau440']:.9f}; diferença conjunta menos produto das marginais/R-B={x['joint_control']['R_B_joint_minus_marginals']:.9f}. Apenas diagnóstico: não existe comparação pareada de recuperação440-fixo versus440-livre.

ResultadoSHA256: {sha(D/'RESULT.json')}. CódigoSHA256: {sha(D/'measure.py')}. Cópias e fontes em COPIES.json e sources_sha256 do resultado. Reprodução: /opt/lal_env/bin/python -B t05/measure.py, saída única e recusa sobrescrita. CPU{x['cpu_seconds']:.6f}s, parede{x['wall_seconds']:.6f}s; fase leve, horas pesadas0; axiomasN/A. Condição operacional, nenhuma significância experimental ou movimento do gate. PróximoT06.
'''
write(OUT/'ENTREGA_015_T05_440.md',text.encode())
write(D/'REAPROVEITAMENTO_T05.md',('[REAL — reutilização]\n\nFisher440 arquivado reproduzido a erro relativo<1e-12; as fórmulas de prediction e prediction_draws foram copiadas byte a byte, com hashes em COPIES.json. QNM_GRID e posteriores públicos conferidos contra os recibos/registro. Nenhuma nova PE, novo dado ou ajuste para alcançar significância.\n').encode())
q=OUT/'ENTREGA_016_PROGRESSO.md';write(q,q.read_bytes()+f'\n{now} — B/T05 PAGO diagnóstico:240 linhas de projeção,340 de pareamento; N físico=null; CPU{x["cpu_seconds"]:.6f}s, horas pesadas0. AberturaSHA256 {opening}. PróximoT06.\n'.encode(),True)
q=R/'A7/CONTINUIDADE.json';c=json.loads(q.read_bytes());c.update(at=now,previous_goal_turn='PROGRESS',own_live_process=None,own_live_processes=[],T05_delivery=str(D/'RESULT.json'),next='T06 full-posterior nonblind population-width LRT and Gaussian comparison/jackknife; then T11 T12 allocation R7. T05 paid as diagnostic only, E7 producer unchanged; new D6 egress still pending.');save(q,c,True)
print(json.dumps(dict(status='T05_DELIVERED',result_sha256=sha(D/'RESULT.json'))))
