"""Audit the concrete scalar realization; preserve its limited scope."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json,re
R=Path(__file__).resolve().parents[1];D=R/'D6';OUT=R.parent/'TUNEL/DO_CHATGPT'
sys.path.insert(0,str(R))
from prepare_part_d import sha,save,write
now=datetime.now(timezone.utc)
s=D/'ScalarGraphRealization_v3.lean';p=D/'scalar_04.json';log=D/'scalar_04.log'
r=json.loads(p.read_bytes())
assert r['rc']==0 and r['source_sha256']==sha(s) and r['log_sha256']==sha(log)
assert not r['newer_kernel_files'] and not r['scan_errors']
assert not re.search(r'\b(sorry|axiom)\b',s.read_text('utf-8'))
ax=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",log.read_text('utf-8-sig'))
assert len(ax)==9
assert all(set(v.split(', '))<={'propext','Classical.choice','Quot.sound'} for _,v in ax)
old=json.loads((D/'MODULAR_BRIDGE_DELIVERY.json').read_bytes())
cycles=[json.loads((D/f'scalar_{i:02}.json').read_bytes()) for i in range(1,5)]
receipt=dict(at=now.isoformat(),status='REAL_CONCRETE_SCALAR_ANALYTIC_REALIZATION',source_sha256=sha(s),log_sha256=sha(log),receipt_sha256=sha(p),declarations=dict(ax),previous_delivery_sha256=sha(D/'MODULAR_BRIDGE_DELIVERY.json'),cycles=4,cycle_limit=6,scalar_cpu_seconds=sum(x['cpu_user_seconds']+x['cpu_kernel_seconds'] for x in cycles),scalar_wall_seconds=sum(x['wall_seconds'] for x in cycles),physical_pair_identification='OPEN: chosen photon pair graph has not been identified with this scalar GNS graph',opening_sha256=sha(OUT/'ENTREGA_016_ABERTURA_operador.md'))
save(D/'SCALAR_REALIZATION_DELIVERY.json',receipt)
text=f'''[REAL — nove declarações Lean auditadas; OPEN — realização no par físico escolhido]

Abertura016SHA256: {receipt['opening_sha256']}

D6 agora fornece a ponte modular condicional e uma realização analítica concreta usando a torre GNS escalar existente. O grafo quadrático coincide com o quadrado de Tomita já construído; o resolvente, a raiz regularizada, J e as potências imaginárias são os objetos anteriores do kernel. Não foram definidos por conjugação pelo unitário a reconhecer.

ScalarGraphRealization_v3.lean: sha256 {sha(s)}. scalar_04.log: sha256 {sha(log)}. Compilação rc0; nove declarações, incluindo duas definições auxiliares, dependem somente de propext, Classical.choice e Quot.sound. Somadas às 24 declarações anteriores: 33 declarações auditadas. Os 31 controles finitos anteriores permanecem separados da prova geral.

Quatro ciclos foram usados (limite seis): um terminou por falta de memória no teto isolado de 8 GiB; dois diagnosticaram conversões de subtipos e busca de instâncias; o quarto passou após extrair o cálculo funcional para um lema genérico de Hilbert. Elevar o teto isolado a 12 GiB foi registrado em MEMORY_CEILING_CHANGE.json. Tentativas preservadas. CPU escalar total {receipt['scalar_cpu_seconds']:.6f}s; parede {receipt['scalar_wall_seconds']:.6f}s.

ALCANCE: as hipóteses analíticas do reconhecimento têm uma realização concreta; isso não identifica a torre escalar com a rede física de fótons selecionada. PairTomitaAnalyticRealizationMeasured permanece obrigação nomeada para aquele par. A cláusula same_horizon_by_content é proposta na cópia de bancada, sem alteração do contrato canônico ou gate. D6 atende à parte condicional demonstrada; a instanciação física continua indicada, sem aprovação por definição.

Crítica independente Kimi recebida anteriormente e adjudicada para o grafo e controles. Ela não revisou estes nove lemas novos. Três novas unidades remotas continuam sem envio, aguardando a autorização específica já perguntada após rejeição automática. Nenhuma repetição de chamadas terminais/incertas.

Próximo alvo autorizado: D1′, reutilizando C4 e suas quatro obrigações de GlobalHelicityInducedRepresentationMeasured. Ringdown segue preservado, sem registro ou relógio pesado.
'''
write(OUT/'ENTREGA_016_D6_realizacao_escalar.md',text.encode())
q=R/'A7/CONTINUIDADE.json';c=json.loads(q.read_bytes());c.update(at=now.isoformat(),own_live_process=None,own_live_processes=[],previous_goal_turn='PROGRESS',D6_scalar_delivery=str(D/'SCALAR_REALIZATION_DELIVERY.json'),next='D1prime: inherit C4 four obligations; D6 analytic bridge audited and instantiated in scalar GNS only, physical pair identification remains named. Three new remote payloads still require pending explicit approval. Do not dispatch/retry.');save(q,c,True)
q=OUT/'ENTREGA_016_PROGRESSO.md';write(q,q.read_bytes()+f'\n{now.isoformat()} — D6 REAL/MEDIDA: +9 declarações (33 totais), realização escalar; instanciação física nomeada. CPU adicional {receipt["scalar_cpu_seconds"]:.6f}s. Parede {receipt["scalar_wall_seconds"]:.6f}s. Próximo D1′. AberturaSHA256 {receipt["opening_sha256"]}.\n'.encode(),True)
print(json.dumps(receipt,ensure_ascii=False))
