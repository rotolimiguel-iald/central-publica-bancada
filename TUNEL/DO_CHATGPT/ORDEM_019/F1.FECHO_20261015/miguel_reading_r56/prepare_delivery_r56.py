"""Prepare immutable R56 delivery from verified local artifacts."""
from support_r56 import *

b = json.loads((ROOT/'BUILD_SUCCESS_R56.json').read_text(encoding='utf-8'))
assert b['exit_code'] == 0 and b['trio_only'] and b['no_sorry']
assert b['axiom_declarations'] == 8
for key in ('source', 'build_log', 'olean'):
    assert pin(b[key]['path'])['sha256'] == b[key]['sha256']

text = '''R56 — REFERÊNCIA CONSERVADA E COMPOSIÇÃO VERIFICADA
Autor: codex-gerente-tgl. 17/10/2026. F1.FECHO_20261015, reivindicação 933.

1. INSCRIÇÃO
[INPUT/ONTO] As cinco falas integrais do operador estão em OPERADOR_VERBATIM_R56.json.
Elas fixam a referência: medida por paridade inversa; observador como forma matricial
da luz; ângulo de Miguel como leitura da abertura da fronteira. As correspondências
ontológicas são conservadas como tais; sua inscrição não prova igualdade de tipos.
[REAL] O mesmo apêndice de 2.854 bytes foi acrescentado a oito superfícies, com backup
imediato dos bytes. MEMORY_APPLIED_R56.json registra cada antes, backup e depois.
A memória ACOM usa a referência própria FECHO_MISSION_REFERENCE.json, sem nova missão.

2. REAPROVEITAMENTO
[REAL — fonte e composição compilada] SelectionAngleReconstruction.lean já contém
miguel_boundary_reconstructed_from_its_selected_face. O elo matriz/leitura não faltava.
Para 0 <= beta <= 1, theta_M = arcsin(sqrt(beta)); os pesos iniciais são beta e 1-beta.
O leitor phaseReading lê exp(i theta), e angularDecoder reconstrói S(theta).
Fora dessa família, a seleção por uma face não é injetiva: há controle negativo.
J antiunitário, P linear idempotente e theta real conservam seus tipos próprios.

3. CONTINUIDADE DEMONSTRADA, COM DOMÍNIO EXPLÍCITO
[REAL — Lean em sandbox] A candidata R2 define A(t)=S(theta_M+Omega*t).
Prova leitura exp(i(theta_M+Omega*t)), reconstrução de A(t), releitura idempotente
e fase relativa exp(i Omega*t). Todas as taxas têm a mesma forma inicial.
O build usa Lean 4.31.0: EXIT 0, oito declarações impressas com axiomas somente
propext, Classical.choice e Quot.sound; nenhum sorry; duração 51,422 s.
A fonte contém também initial_form, auxiliar sem impressão separada de axiomas.
O primeiro build foi interrompido por consumo de recursos; seus recibos estão
preservados. R2 reduziu os imports e concluiu com limite de memória explícito.

[OPEN — transporte físico] Esta é uma órbita angular escolhida. Seus pesos em t
são sin²(theta_M+Omega*t) e cos²(theta_M+Omega*t), não beta e 1-beta constantes.
Logo não prova que uma fronteira física de refletividade fixa beta evolui dessa
forma. Omega não é deduzido de beta. Reconstruir a matriz não recupera sozinho o
número de voltas da fase nem um tempo global. A fase escalar tem taxa Omega;
a coerência entre os dois setores da R9 tem taxa 2*Omega: objetos distintos.

4. RESÍDUO CONCRETO DO DISPOSITIVO
[REAL — conteúdo documental] A patente do Supercondutor escreve
G_OH(t)=a exp(i omega_OH*t), a=tanh(P_MW/P_th), e um Hamiltoniano que inclui
cavidade/OH, acoplamento Jaynes–Cummings e bombeamento de Rabi.
[DERIVED, família proposta A=a S(theta), a real e 0<a<1] Aplicar o decodificador
recíproco a z=a exp(i theta) troca a amplitude do segundo setor por 1/a.
Portanto ele não reconstrói A nessa extensão. z P+ + conj(z) P- é uma extensão
algébrica candidata para amplitude real; outra rota conserva amplitude e fase
separadamente. Com amplitude zero, a leitura da fase deve recusar.
O sinal escalar G_OH ainda precisa ser identificado com um observável do setor
matricial por uma redução/representação demonstrada; essa conta não o identifica.

5. CONTINUIDADE DA MISSÃO
Reutilizar Fock, Takesaki e Maxwell já aceitos; não reabri-los por perda de contexto.
A escolha exclusiva MQC/Supercondutor/Psi-NET foi prematura, conforme R55: célula,
dinâmica e protocolo têm papéis complementares, sem equivalência física presumida.
R4/R5 ainda exigem a realização do dispositivo, unidades, espectro/relógio,
refinamentos e entrelaçamentos. R3/R10 exigem rito integral e revisão final.
H3 universal conserva o alcance do inventário; R56 não fornece esse antecedente.

Revisão independente em REVIEW_R56.json e complemento. O aceite técnico desta
camada não é ratificação da gerência. Nenhum um.py, fonte Lean original, Bancada,
dado observado ou gate foi alterado. Oito memórias foram atualizadas, conforme
autorização e recibos; não se promete memória infalível nem instalação nos pesos.
'''
report = new('RELATORIO_R56.txt', text)

names = [
 'OPERADOR_VERBATIM_R56.json', 'SOURCES_R56.json', 'REAPROVEITAMENTO_R56.md',
 'MEMORY_APPEND_R56.txt', 'MEMORY_PLAN_R56.json', 'MEMORY_APPLIED_R56.json',
 'MiguelReadingTemporalCompositionR56R2.lean', 'BUILD_SUCCESS_R56.json',
 'ATTEMPT_R1_STOP_REASON.json', 'PONTE_DISPOSITIVO_PASSO_SEGUINTE_R56.md',
 'RELATORIO_R56.txt', 'REVIEW_R56.json', 'REVIEW_R56.md',
 'REVIEW_R56_SCOPE_ADDENDUM.json', 'REVIEW_R56_SCOPE_ADDENDUM.md',
]
names += [f'MEMORY_SURFACE_{i:02d}_R56.json' for i in range(8)]
artifacts = [pin(ROOT/n) for n in names]
artifacts += [pin(p) for p in sorted((ROOT/'builds').glob('*/*')) if p.is_file()]
artifacts += [pin(ROOT.parent/'CONFERENCIA_PONTE_DISPOSITIVO_R55.json'),
              pin(ROOT.parent/'CONFERENCIA_PONTE_DISPOSITIVO_R55.txt'),
              pin(Path(r'C:\IALD\Central de Patentes\Patentes\PATENTE_SUPERCONDUTOR_HOLOGRAFICO_TGL_v2_BLINDAGEM.tex'))]
new('DELIVERY_R56.json', {
 'unit':'F1.FECHO_20261015', 'board_claim':933, 'task_id':TASK,
 'reference':str(REFERENCE), 'status':'COMPONENT_VERIFIED_WITH_SCOPE',
 'memory_surfaces':8, 'memory_pure_append_bytes_each':2854,
 'compiled_declarations_printed':8, 'exit_code':b['exit_code'],
 'trio_only':True, 'zero_sorry':True, 'seconds':b['seconds'],
 'physical_device_realization':'OPEN',
 'bounded_claim':'Existing Miguel reader reused; parameterized angular composition compiled. No physical clock or fixed-reflectivity device dynamics inferred.',
 'artifacts':artifacts,
 'review':'Independent review of content, hashes and supplied build; no claim of independent recompilation.',
 'canonical_program_kernel_bench_data_gate_changed':False,
 'memory_changed':True,
})
print(json.dumps({'delivery':pin(ROOT/'DELIVERY_R56.json'), 'report':pin(report)},ensure_ascii=False))
