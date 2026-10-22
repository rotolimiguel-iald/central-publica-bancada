"""Measured cross-reference summary, no canonical-memory or scientific-code edits."""
from pathlib import Path
from datetime import datetime,timezone
import json
from prepare_part_d import sha,save,write
R=Path(__file__).resolve().parent;ROOT=R.parent;OUT=ROOT/'TUNEL/DO_CHATGPT';B=ROOT/'ORDEM_013_RINGDOWN';D=B/'bis/015/t03'
now=datetime.now(timezone.utc).isoformat();opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
sources=[R/'D6/MODULAR_BRIDGE_DELIVERY.json',R/'D6/SCALAR_REALIZATION_DELIVERY.json']+[R/x/'RESULTS.json' for x in ['D1prime','D2prime','D3prime','D4','D5']]
records={str(p):dict(sha256=sha(p),result=json.loads(p.read_bytes())) for p in sources}
save(R/'PART_D_DELIVERY.json',dict(at=now,sources=records,opening_sha256=opening,gate_changed=False))
text=f'''[REAL — cadeia formal de bancada; hipóteses físicas OPEN identificadas]

Abertura016SHA256: {opening}

| Alvo | Resultado da bancada | Alcance restante |
|---|---|---|
| D6 | Transporte do grafo de Tomita, reconhecimento modular condicional e realização escalar concreta | Realização analítica do par físico do fóton |
| D1′ | Quociente transversal, caracteres e composição de fases | GlobalHelicityInducedRepresentationMeasured: colagem mensurável, orientação global, representação unitária contínua e restrição ao boost; PCT físico |
| D2′ | Tensor polinomial de Maxwell, simetria, traço, fluxo nulo; tensor forjado recusado | MaxwellWickExpectationLocalMeasured: expectativa Wick, domínio e localidade na rede |
| D3′ | Quadrado/conjugação e ponto fixo finito; contrato H2 liga vetor fixo à linha do vácuo | StationaryLightCenterModularIdentificationMeasured e realização física de H2 |
| D4 | PAGO: retipagem e 90 consumidores compilados, escalar sem massa recusado | A admissibilidade do tipo não constrói uma rede |
| D5 | Dilatação positiva da cunha e reconhecimento modular condicional | PhotonDilationCovarianceMeasured e realização do par |

Os D1–D3 antigos foram cancelados pelo ADENDO003c. A ParteD revista foi percorrida até D5; MEDIDA não significa que todas as dívidas globais foram pagas. O quadro distingue provas e contratos condicionais sem gerar nova camada no programa. Manifesto e resultados completos: ORDEM_016_QG/PART_D_DELIVERY.json; SHA256 {sha(R/'PART_D_DELIVERY.json')}.

Nenhum original, um.py ou gate alterado. Revisão independente dos novos resultados não é substituída pelo compilador; a crítica Kimi de D6 cobria o recorte registrado em seu recibo. Os três novos envios a provedores continuam aguardando autorização específica.

Continuação: ParteB pela ORDEM015, após registro V1.1 e controles, sem antecipar o relógio de trabalho pesado.
'''
write(OUT/'ENTREGA_016_PARTE_D_quadro_final.md',text.encode())
delivery=json.loads((D/'REGISTRATION_DELIVERY.json').read_bytes());assert delivery['status']=='REGISTERED_ACTIVATION_CHECKED_HEAVY_EXECUTION_BLOCKED_BY_MISSING_R7'
proof=json.loads((D/'C1_GUARD_MUTATION_TESTS_V1_1.json').read_bytes());n=len(proof['tests']);assert all(t['passed'] for t in proof['tests'])
reg=B/'RINGDOWN_5SIGMA_V1_1.json';assert delivery['receipt']['registration_sha256']==sha(reg)
text=f'''[REAL — T03 registro e controles pagos; nulos da fase P ainda não executados]

Abertura015SHA256: {sha(OUT/'ENTREGA_015_ABERTURA_operador.md')}
Abertura016SHA256: {opening}

V1.1 registrada com testemunha anterior a qualquer job pesado. RegistroSHA256 {sha(reg)}. Recibo de conferência {sha(D/'REGISTRATION_DELIVERY.json')}. {n} controles consolidados, hashes da árvore atual conferidos: candidato, entrada integrada, leitura específica e relógio. A repetição dos31 controles do relógio foi necessária porque a guarda mudou; os demais resultados foram reaproveitados após conferir os respectivos hashes. ResultadoSHA256 {sha(D/'C1_GUARD_MUTATION_TESTS_V1_1.json')}.

A entrada real checked_registration no /opt/lal_env conferiu cadeia, ativação, pinos e runtime e recusou executar pela ausência esperada de PART_015_BUDGET_START.json. Isso é bloqueio deliberado da fase P, não falha do registro. V1 e árvores antigas intactas. R5:1015 retornos finitos na configuração4096/8192; permanece cobertura finita.

PAGO: preparo, estatísticas auxiliares, emenda, testemunha, controles e qualificação source-only. NÃO PAGO nesta entrega:30 células sintéticas, posterior piloto, calibração física E3.3. Machine hours desta fase:0. Nenhuma semente lida e nenhum descegamento. Nulos não medem p físico antes da calibração. A emenda compra condição operacional, não significância experimental.

Reprodução/auditoria: consolidate_guard_probes.py verifica os recibos; register_v1_1.py registra uma única vez e recusa sobrescrita. Para consultar, usar os artefatos entregues, não repetir a publicação. Axiomas:N/A sem Lean. PróximoT05, depoisT06,T11,T12 e alocação; R7 somente antes do primeiro job pesado.
'''
write(OUT/'ENTREGA_015_T03_emenda.md',text.encode())
q=OUT/'ENTREGA_016_PROGRESSO.md';write(q,q.read_bytes()+f'\n{now} — ParteD entregue com hipóteses nomeadas; B/T03 registro V1.1 PAGO e150 controles, nulos pendentes. Horas pesadas0. PróximoT05. AberturaSHA256 {opening}.\n'.encode(),True)
q=R/'A7/CONTINUIDADE.json';v=json.loads(q.read_bytes());v.update(at=now,own_live_process=None,own_live_processes=[],part_D_summary=str(R/'PART_D_DELIVERY.json'),B_registration_delivery=str(D/'REGISTRATION_DELIVERY.json'),next='B T05 light 440 rescaling/QNM pairing diagnostic, then T06 T11 T12 allocation. V1.1 registered with150 controls; real entry refused only missing R7. Do not rerun registration or tests with existing output. No heavy clock. New D6 provider payloads still pending specific consent. Coordinator local identity verified and progress message delivered after first auto-review refusal.');save(q,v,True)
print(json.dumps(dict(status='PART_D_AND_T03_DELIVERED',tests=n,heavy_clock=False)))
