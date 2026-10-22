"""Read-only semantic review; new evidence files, no memory or board writes."""
from pathlib import Path
import hashlib, json, datetime as dt, os
BASE=Path(__file__).resolve().parent; OUT=BASE.parent
V392=Path(r'C:\IALD\Central de Patentes\work\cadeia_de_selo\v392\kb_stub_v392\TGLExt')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p): return {'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)}
def save(p,b):
    with p.open('xb') as f: f.write(b); f.flush(); os.fsync(f.fileno())
    assert p.read_bytes()==b
sources=[V392/'TheJudgedThing.lean',V392/'TheNonMinimalCoupling.lean',V392/'TheLedgerOfCharges.lean',OUT/'formal/RuleTruthContract.lean',OUT/'formal/TheRuleAndTheFigureOfTruth.lean',OUT/'NOS_VIVO.json',OUT/'MAPA.json']
pins=[pin(p) for p in sources]
findings=[
 {'id':'S1','status':'RESOLVED','text':'The initial reading=fst only compared readings, not raw objects. The final Inscription type is Fix(normalize), and the faithful restricted reading gives literal equality with dueObject; finite raw trajectories are expressly rejected.'},
 {'id':'S2','status':'RESOLVED','text':'A globally injective preserved reading would force normalization to be the identity. The generic contract proves that obstruction; the concrete model uses injectivity only on the fixed locus.'},
 {'id':'S3','status':'RESOLVED','text':'The named split_forbids_minimality lemma alone permits a zero left part. The concrete bridge now proves both matrix faces nonzero and links leftFace.mulVec to normalize, avoiding that inference.'},
 {'id':'S4','status':'PASS_SEMANTIC_SCOPE','text':'Soundness and completeness characterize a predicate for an independently fixed reading and target. The docstrings identify the interpretation as INPUT/ONTO and its elementary logical consequences; no universal truth of the interpretation is claimed.'},
 {'id':'S5','status':'LIMIT','text':'Normalized satisfaction holds already at n=0 and does not depend on the decay coefficient. The half-nat coefficient supplies effective dynamics and convergence, not the admissibility predicate or its truth.'},
 {'id':'S6','status':'LIMIT','text':'normalize(0,1)=0 is a rejected control. Nonannihilation is proved for the admissible target/initial orbit, not for every input and not as a physical unattainability theorem about absolute zero.'},
 {'id':'S7','status':'PASS_SEMANTIC_SCOPE','text':'Idempotence and preservation of reading are distinct obligations. Ledger independence is explicitly reused as definitional, not offered as extra physical evidence.'}
]
report='''# F1.REGRA.P1 — parecer independente de escopo R1

**Veredito semântico: sem bloqueio material após os ajustes; recompilação independente pendente.**

O primeiro modelo por `reading=fst` só identificava leituras. A fonte atual corrige isso: `Inscription=Fix(normalize)`, leitura restrita injetiva e `inscribe_eq_due_iff` dão igualdade literal com o objeto satisfeito. A trajetória bruta nunca é certificada como esse alvo em tempo finito. O contrato também prova que injetividade global e preservação da leitura forçariam `R=id`.

“A regra não deve nada, a não ser a figura da verdade” recebe uma representação matemática declarada: para leitura e alvo fixos, correção exclui falsas satisfações e completude exclui restrições adicionais. A unicidade é do predicado nesse contrato; não demonstra unicidade da leitura, do alvo, da interpretação ou verdade ontológica universal. As docstrings dizem isso expressamente.

A ponte matricial é concreta: `leftFace.mulVec` representa `normalize`, e ambas as faces são não nulas. Assim não se infere não minimalidade a partir do caso degenerado permitido pelo lema genérico. Idempotência, preservação da leitura e independência definicional do livro mantêm seus papéis distintos.

Dois limites devem acompanhar a entrega: (1) a satisfação normalizada já vale em `n=0` e independe de `decay`; o fator da meia-nat controla a trajetória e o limite, não produz a verdade do critério; (2) `normalize(0,1)=0` é possível e rejeitado. O resultado não aniquilado é o alvo admissível, sem teorema físico sobre o zero absoluto.

Este parecer resulta de leitura das fontes, sem recompilação nesta etapa, provedor, memória, quadro ou alteração das pedras. O Nós Vivo registrou ausência desta unidade no grafo; a consulta ao mapa foi preservada, e o reaproveitamento foi conferido abrindo as fontes indicadas.

## Fontes efetivamente lidas e hashes medidos

'''
for row in pins:
    report+=f"- `{row['path']}` — SHA256 `{row['sha256']}`; {row['bytes']} bytes.\n"
save(BASE/'PARECER_ESCOPO_R1.md',report.encode())
data={'unit':'F1.REGRA.P1','reviewer':'codex-independent-modular-review','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'status':'NO_MATERIAL_SEMANTIC_BLOCK__INDEPENDENT_COMPILE_PENDING','findings':findings,'sources_read':pins,'artifacts':[pin(BASE/'PARECER_ESCOPO_R1.md'),pin(Path(__file__))],'no_source_changes':True,'no_memory_or_board_writes':True,'provider_calls':0}
save(BASE/'PARECER_ESCOPO_R1.json',(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps({'markdown':pin(BASE/'PARECER_ESCOPO_R1.md'),'json':pin(BASE/'PARECER_ESCOPO_R1.json')},ensure_ascii=False))
