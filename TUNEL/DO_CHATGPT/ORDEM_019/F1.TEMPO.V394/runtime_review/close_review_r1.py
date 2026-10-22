"""Collect immutable review evidence; does not approve integration or production."""
from pathlib import Path
import hashlib,json
from datetime import datetime,timezone
HERE=Path(__file__).resolve().parent
def pin(p):
    b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
original=json.loads((HERE/'RESULTADO_RUNTIME_REVIEW_R2.json').read_bytes())
correction=json.loads((HERE/'RUNTIME_R2_CORRECTION_REVIEW.json').read_bytes())
preflight=json.loads((HERE/'INTEGRATION_PREFLIGHT_R2_REVIEW.json').read_bytes())
findings=[
 {'id':'R1','severity':'MEDIUM','description':'Phase clock division overflow: (1e308,1e308) returned 0 instead of 0.5; (1,5e-324) returned infinity.', 'status':'RESOLVED_RUNTIME_R2'},
 {'id':'R2','severity':'MEDIUM','description':'expected_ladder was written but never consumed; absent/wrong counts accepted in admission mock.', 'status':'RESOLVED_RUNTIME_R2'},
 {'id':'R3','severity':'LOW','description':'Nested malformed axiom list raised TypeError outside controlled refusal.', 'status':'RESOLVED_RUNTIME_R2'},
 {'id':'R4','severity':'MEDIUM','description':'Repeated integration wrote candidate and backup before immutable-receipt refusal.', 'status':'RESOLVED_PREFLIGHT_R2'},
]
report='''# Revisão independente do runtime v394

[REAL] O runtime R1 passou 5.713 checks sintéticos; três defeitos de fronteira foram reproduzidos e comunicados antes da integração: overflow/underflow no relógio de fase, ausência de conferência da escada formal e exceção não encapsulada em axiomas malformados. O integrador repetido regravava a cópia antes de recusar o recibo existente. Não foi executado o um.py canônico nem a integração real.

[REAL] A fonte runtime R2 passou 5.716 checks e 19 controles adicionais, incluindo contagens ausentes, divergentes, booleanas, float e NaN; mutações da fonte/inscrição; axiomas malformados; relógio extremo representável e recusas de extremos não representáveis. Máximo resíduo contra a exponencial GKLS independente: 4,2987410278529964e-13. O preflight corrigido recusou recibo existente, candidata alterada e módulo parcial, sem alterar bytes ou mtimes das três fixtures.

[REAL] Os sinais dos modos, positividade/Choi, conservação de traço/energia, semigrupo, leitura, reconstrução de tempo, alias e não multiplicatividade foram conferidos pelo harness sintético. A taxa racionalizada e a tau efetiva reproduzem a mesma lei quadrática para o gap especificado. A referência direta pela diferença de raízes perde precisão em Eref/V0 muito grande; a fórmula estável evita essa subtração. Não é nova calibração física.

[REAL] ARTICLE foi extraído pela AST e executado como Python: há quebras de linha reais, comandos LaTeX e escapes corretos; uma inscrição contendo barra/end-document não quebra a fronteira. Os quatro verbatims atuais preservam bytes ao roundtrip UTF-8. A fixture confirma ambos os consumidores PT/EN envolvidos e baseline intacto. Isto não substitui renderização/compilação do artigo integrado.

[ESCOPO] Os testes de admissão usam relatórios formais simulados, identificados como mocks; não provam os teoremas nem substituem a auditoria Lean. As matrizes que este revisor construiu não foram reauditadas por ele. A aceitação aqui cobre runtime R2, contrato físico lido e preflight do integrador; o diff final, consumidor principal e artigos da candidata real aguardam a integração e a conferência separada. Nenhuma escrita de produção, abertura de dado ou gate.

[PROCESSO] O primeiro harness encontrou a infinity real do relógio, mas seu serializador JSON estrito recusou gravá-la. O arquivo incompleto RESULTADO_RUNTIME_REVIEW_R1.json foi preservado e não é evidência válida. O harness R2 apenas serializa retornos não finitos como descrição explícita; RESULTADO_RUNTIME_REVIEW_R2.json é a evidência completa da versão runtime R1. Nenhum fonte testado foi modificado pelo revisor.
'''
with (HERE/'RELATORIO_REVISAO_RUNTIME_R1.md').open('x',encoding='utf-8') as f:f.write(report)
files=['RESULTADO_RUNTIME_REVIEW_R2.json','RUNTIME_R2_CORRECTION_REVIEW.json','INTEGRATION_FIXTURE_REVIEW_R1.json',
       'INTEGRATION_PREFLIGHT_R2_REVIEW.json','RELATORIO_REVISAO_RUNTIME_R1.md','review_r1.py','review_r2.py',
       'verify_corrections_r2.py','integration_fixture_r1.py','integration_preflight_r2.py','close_review_r1.py']
receipt={'unit':'F1.TEMPO.V394','reviewer':'atrator_lean','created_utc':datetime.now(timezone.utc).isoformat(),
 'status':'PASS_RUNTIME_R2_AND_PREFLIGHT_WITH_SCOPE','findings':findings,
 'runtime_r1_sources':original['sources'],'runtime_r2_sources':correction['sources'],'integrator_corrected':preflight['source'],
 'evidence':[pin(HERE/f) for f in files],'incomplete_harness_failure_preserved':pin(HERE/'RESULTADO_RUNTIME_REVIEW_R1.json'),
 'integration_actual_review':'Pending actual integration; no approval of the complete program implied.',
 'production_changes':False,'gate_changed':False}
with (HERE/'REVIEW_RECEIPT_R1.json').open('x',encoding='utf-8') as f:json.dump(receipt,f,ensure_ascii=False,indent=2,allow_nan=False)
print(json.dumps(pin(HERE/'REVIEW_RECEIPT_R1.json'),ensure_ascii=False))
