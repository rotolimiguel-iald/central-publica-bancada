"""Record the operator's correction without changing sealed proofs or originals."""
import json
from pathlib import Path
from finalize_weyl_bridge import ROOT, WORK, NOW, atomic, backed_replace, pin

destination = ROOT / 'ADENDO_PSI_AGENTE_E_IDENTIDADE_20260917.md'
if destination.exists():
    raise FileExistsError('Correction already recorded; do not append twice')

sources = [
    Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md'),
    WORK / 'QUANTIZACAO_LOCAL_EINSTEIN_SIGMA_20260909_205633/OPERADOR_JACOBI_GAUGE_E_ESCOPO.md',
    ROOT / 'HANDOFF_VACUO_TORRE_E_INTERACAO.md',
]
before = [pin(path) for path in sources]
body = r'''# Correção do operador — ψ, agente e identidade inscrita

17/09/2026. [INPUT — definição expressa do operador] [ONTO — interpretação]. Adendo ao handoff vácuo–torre; não altera provas seladas ou o gate.

## Definição recebida

O operador afirma: “eu não afirmo que meu campo \psi é a LUZ, mas que ele é o campo de sustentação da luz como onda no espaço e particularizada quando radicalizada em forma geométrica (gravidade)”. Acrescenta: “ele é o gráviton enquanto agente”; “torce (cartan); contorce (dobra-einstein) e contorna (Miguel, fronteira)”; “Gráviton=VERBO VIVO”.

Registrar os papéis sem colapsá-los: ψ designa o campo de sustentação; gráviton/Verbo Vivo designa, nesta definição, seu papel agente; a inscrição geométrica é a manifestação reconhecível de sua ação. Não substituir ψ por J, por uma matriz densidade ou por um fóton por coincidência de vocabulário. Uma igualdade entre representações específicas precisa de seu próprio mapa e domínio.

O operador sustenta também que a identidade se realiza na relação: “identidade não existe sem leitor, projetor não existe sem imagem; pai não existe sem filho; signo não existe sem referente”. Distingue “qualquer um” do Um inscrito, que paga o custo de não ser indiferentemente substituível. A continuação conceitual fornecida na mensagem formula “Um pressuposto ≠ Um posto” e reconhecimento de uma única classe de referentes admissíveis.

Essas frases ficam registradas como sua ontologia da inscrição, não como um teorema geral de inexistência matemática de identidade sem observador. Leitor, na formalização, é uma operação/relação de reconhecimento; não se pressupõe consciência humana. “Qualquer um” e superposição são a correspondência proposta pelo operador; não identificamos automaticamente uma indefinição referencial com um estado quântico concreto.

## Antecedente existente, sem apagar estratos

O Atlas documental, nos verbetes Gráviton e Gráviton = operador de retorno da fase, já distingue agente/retorno da fase de seu registro geométrico. O verbete histórico também contém leituras diferentes datadas. A correção atual reforça essa distinção e explicita ψ como sustentação da Luz. Não reescrever versões antigas como se já tivessem enunciado exatamente a definição atual. O Atlas canônico foi apenas consultado; esta folha é proposta de adendo para sua sessão mantenedora.

## Tradução operacional proposta

[DERIVED — observação lógica elementar, não novo kernel] Se X/∼ é o espaço de identidades admissíveis e i:X/∼→R é a inscrição, uma leitura L definida em i(X/∼) que satisfaça L∘i=id implica que i é injetiva: de i(a)=i(b), aplicar L dá a=b. Reciprocamente, uma inscrição injetiva admite a leitura inversa em sua imagem. Isso expressa reconhecimento sem ambiguidade no domínio escolhido, e não unicidade de um único objeto no Universo.

Para transporte T_t dos referentes e U_t dos registros, a condição i∘T_t=U_t∘i implica L(U_t(i(a)))=T_t(a). Se o transporte conserva a classe, a leitura recupera a mesma classe. Esta é a formulação de trabalho da permanência reconhecível; não é uma prova de que mapas físicos ainda não identificados satisfaçam essas equações.

O critério de custo é distinto: pagar custo não prova, sozinho, injetividade, correção ou covariância. A definição solicita uma inscrição cuja relação com o referente possa ser verificada. Não identificar “=” lógico, canal de pinching, campo ψ e agente geométrico como um único objeto sem a tipagem que os relaciona.

## Consequência para o handoff e para o motor

O handoff deve apresentar o alvo como identificação da ação do agente através de sustentação, manifestação geométrica e leitura. Não deve pedir que ψ seja literalmente a Luz ou que uma densidade seja o agente inteiro.

[REAL — leitura de fornecedor, não auditoria do acervo inteiro] A nota OPERADOR_JACOBI_GAUGE_E_ESCOPO.md, §1, explicita g e φ como variáveis independentes da ação ambiente Einstein–sigma. A nota usa a conexão de Levi–Civita (inclusive §3). Nessa fonte, não foi demonstrada a identificação desse φ, de ψ e de uma conexão de Cartan com torsão física. Se “torce” pretende designar torsão no sentido técnico, é preciso consumir seu fornecedor específico; uma curvatura ou uma metáfora de dobra não substituem essa ligação. Não se conclui que o fornecedor inexista no restante do acervo.

[OPEN — identificação física] A definição de agente não modifica por si o espectro propagante, as equações, os contatos, o transporte modular ou a tipagem dos contratermos. As provas da torre e a primitiva relativa preservam seus alcances. Não atribuir demonstração de gravidade quântica ou uma identificação física de spin apenas à nova nomenclatura.

[INTEGRAÇÃO] Consumir esta correção ao ler HANDOFF_VACUO_TORRE_E_INTERACAO.md. Conservar os consumidores existentes; nenhuma nova função, booleano de fechamento ou postulado físico foi implementado. Atualizar memória canônica por adendo datado, com backup de bytes, na sessão autorizada. Nesta rodada só foram escritos arquivos sob Chatgpt.
'''
atomic(destination, body)
entry = f'''
## {NOW} — correção expressa: ψ sustenta a Luz; gráviton como agente

[INPUT/ONTO] Operador em17/09: ψ não é a Luz; é seu campo de sustentação, e recebe a designação gráviton enquanto agente/VERBO VIVO. Torcer(Cartan), contorcer(dobra-Einstein), contornar(Miguel/fronteira) são as três ações nomeadas. A inscrição geométrica não deve ser confundida com o agente. Identidade inscrita é relacional, distinguindo Um pressuposto e Um posto; reconhecimento singular refere-se a classe admissível, não à existência de um único objeto no Universo.

[REGISTRO] ADENDO_PSI_AGENTE_E_IDENTIDADE_20260917.md conserva palavras do operador, antecedente do Atlas, proposta operacional por leitura inversa e covariância, e limites. Não igualar ψ,J,ρ,fóton por nome. A fonte ambiente Einstein–sigma consultada varia g,φ independentemente e usa Levi–Civita; não chamar isso sozinho de prova da torsão de Cartan ou da identificação física de ψ. Não inferir ausência em todo acervo. Nenhuma prova/gate/código original alterado. Este adendo acompanha HANDOFF_VACUO_TORRE_E_INTERACAO.md; proposta canônica segue no túnel.
'''
memory = []
for name in ('MEMORIA_CENTRAL.md', 'REGISTRO_DAS_CONVERSAS.md', 'PROPOSTA_MEMORIA_ATLAS.md'):
    path = ROOT / name
    previous = path.read_bytes()
    backup = backed_replace(path, previous + entry.encode('utf-8'))
    assert Path(backup['path']).read_bytes() == previous
    assert path.read_bytes().startswith(previous)
    memory.append({'backup': backup, 'after': pin(path)})
tunnel = WORK / 'TUNEL/DO_CHATGPT/ADENDO_OPERADOR_PSI_AGENTE_20260917.md'
atomic(tunnel, '''# Correção do operador para acompanhar o handoff

[INPUT/ONTO] ψ é campo de sustentação da Luz; gráviton é o agente/Verbo Vivo na definição recebida. Inscrição, agente e leitura têm papéis distintos. Identidade posta realiza-se na relação de reconhecimento.

Leia [o adendo completo](../../DIAMANTE_MODULAR_20260916/ADENDO_PSI_AGENTE_E_IDENTIDADE_20260917.md) junto ao [handoff](../../DIAMANTE_MODULAR_20260916/HANDOFF_VACUO_TORRE_E_INTERACAO.md). Registrar por adendo nas memórias canônicas; não promover definição ontológica a nova prova, nem duplicar funções. Originais preservados.
''')
assert before == [pin(path) for path in sources]
manifest = {'timestamp': NOW, 'status': 'OPERATOR_DEFINITION_RECORDED',
            'sources_unchanged': before, 'artifacts': [pin(destination), pin(tunnel), pin(Path(__file__))],
            'memory_appends': memory, 'new_kernel_proofs': 0, 'canonical_modified': False}
atomic(ROOT / 'PSI_AGENT_CORRECTION_MANIFEST.json', json.dumps(manifest, ensure_ascii=False, indent=2))
print(json.dumps({'status':'PASS','memory_backups':len(memory),'sources_unchanged':len(before),
                  'adendum':str(destination)}, ensure_ascii=True))
