"""Directed source inventory; no claimed new theorem or production mutation."""
from pathlib import Path
import datetime, hashlib, json, re

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
REDE = OUT.parent / 'F1.REDE'
KERNEL = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
EXT = KERNEL / 'TGLExt'
PAT = Path(r'C:\IALD\Central de Patentes\Patentes')

def pin(path, needles=()):
    raw = path.read_bytes()
    text = raw.decode('utf-8-sig')
    lines = text.splitlines()
    anchors = {}
    for needle in needles:
        matches = [i for i, line in enumerate(lines, 1) if needle in line]
        assert matches, (str(path), needle)
        anchors[needle] = matches
    return {'path': str(path), 'sha256': hashlib.sha256(raw).hexdigest(),
            'bytes': len(raw), 'anchors': anchors}

sources = [
    pin(OUT/'network_reuse'/'INVENTARIO_REAPROVEITAMENTO_R1.md'),
    pin(OUT/'network_reuse'/'CanonicalFockAssemblyR1.lean', ['structure CanonicalNetInput', 'wedge_glue']),
    pin(EXT/'QGSolutionComplete.lean', ['structure LightNetData', 'K_local', 'K_translate', 'K_boost']),
    pin(REDE/'CONSTRUCAO_CONTINUA_R1.md'),
    pin(REDE/'CONTRATO_REDE_R2.md'),
    pin(REDE/'modular_wedge'/'CanonicalWedge.lean', ['def KWR']),
    pin(REDE/'geometric_identification'/'GeometricIdentification.lean', ['Jcandidate_eq_geometricJ', 'Jcandidate_rapidity_coordinates']),
    pin(REDE/'geometric_identification'/'WedgeReflectionTranslations.lean'),
    pin(EXT/'PoincareGroup.lean', ['LorentzGrp', 'PoincareGroup']),
    pin(EXT/'PoincareWitness.lean', ['def thePoincareWitness', 'proper_sector_fibers_blind']),
    pin(EXT/'LightHelicityWigner.lean', ['def helicityChar', 'helicity_screen_cocycle', 'light_helicity_character_nontrivial']),
    pin(EXT/'O16'/'PhotonCharacterCocycle.lean', ['def ScreenOrientationMeasured', 'oriented_screen_phase_unit', 'screen_phase_cocycle']),
    pin(EXT/'O16'/'StrictCocycleGauge.lean', ['strict_cocycle_is_coboundary']),
    pin(EXT/'O16'/'IsometricCocycleSpectrum_v2.lean', ['isometric_fiber_shift_no_eigen']),
    pin(EXT/'O16'/'OrbitalRapidityMeasure_v4.lean', ['def orbitalMeasure', 'def orbitalWeight']),
    pin(EXT/'O16'/'OrbitalBoostUnitary_v2.lean', ['def orbitalBoostUnitary', 'orbitalBoostUnitary_conj_translations']),
    pin(KERNEL/'.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Haar/InnerProductSpace.lean', ['theorem measurePreserving (f : E']),
    pin(REDE/'sources'/'ARTICLE_SOURCE_PINS_R1.json'),
    pin(PAT/'PATENTE_SUPERCONDUTOR_HOLOGRAFICO_TGL_v2_BLINDAGEM.tex'),
    pin(PAT/'Psi_Net_Protocol_PI_INPI.tex'),
    pin(PAT/'TGL_Tensor_LLM_PI_INPI.tex'),
]

body = r'''# Rede global: inventário dirigido e próximo lema

[REAL — leitura de fontes; não nova compilação] Este inventário localiza o resíduo global após as construções na cunha canônica. Não repete como abertas as peças de Fock pagas depois do inventário histórico. Os hashes e as âncoras foram extraídos dos bytes no JSON ao lado. Ausência aqui significa não localizada no escopo pesquisado, não prova de ausência universal.

## Objeto que precisa ser construído

`CanonicalNetInput` (`CanonicalFockAssemblyR1.lean:25–27`) estende `LightNetData` e exige `wedge_glue`: a cunha direita da rede deve ser exatamente o `KWR` concreto. `LightNetData` (`QGSolutionComplete.lean:49–57`) exige isotonia, localidade simplética, covariância sob todas as translações e o boost B0. Seu rótulo ±1 de helicidade não contém uma representação de Poincaré. Preencher o rótulo ou transportar somente uma cunha não constrói uma rede física global.

## Reaproveitamento que já tem conteúdo

| Peça | Conteúdo conferido na fonte | Limite para esta tarefa |
|---|---|---|
| CanonicalWedge / Fourier parcial | TW positivo, conjugação, KWR standard e convenção modular no H1 original | Uma cunha fixa |
| GeometricIdentification / WedgeReflectionTranslations | Jcandidate coincide com a reflexão geométrica, troca/conjugação das fibras; conjuga as quatro translações pela reflexão da cunha | Não é ação de todo Lorentz |
| OrbitalRapidityMeasure / OrbitalBoostUnitary | Medida orbital d³p/E, carta de rapidez, boost unitário contínuo e conjugação das translações | Boost de um plano; falta a família espacial completa |
| PhotonCharacterCocycle | Fase de tela unitária e composição, consumindo orientação da tela e preservação de momento/métrica | Provar essas hipóteses para a ação física global, mensurabilidade e ação L² |
| LightHelicityWigner | Caractere de helicidade ±1, cociclo escalar e conjugação | O cabeçalho preserva H1/K/B0/U1/Fock; não fornece U(a,Λ) |
| StrictCocycleGauge | Cociclo de translação na reta é cobordo na forma dada | Não é trivialização de toda representação de Poincaré |
| IsometricCocycleSpectrum | Ausência de autovetor para deslocamentos de fibra que preservam norma | Consome a ação de fibra; não a constrói |
| PoincareGroup / PoincareWitness | Grupo e ação afim geométrica; testemunha própria existente | A testemunha não é a representação Wigner no H1; `proper_sector_fibers_blind` explicita sua limitação |

`LorentzGrp` do arquivo geométrico contém todo O(1,3), porque a condição é preservar η. A órbita futura exige recorte ortócrono; a representação de helicidade usa a componente própria e a extensão antiunitária apropriada. O uso do grupo inteiro como se preservasse o cone futuro seria erro de tipo físico.

## Rota construtiva concreta

1. [OPEN — formalização global] Construir a ação da componente própria ortócrona na órbita nula futura, na medida orbital e depois no H1 já fixado. Pagar preservação da medida, não a substituir por um campo com esse nome.
2. [DERIVED — projeto analítico existente] Reutilizar a seção Borel explícita de `CONSTRUCAO_CONTINUA_R1`: s(p)=Bx(r) Rx(q) Bz(log ρ), com tratamento do eixo nulo. Formar c(Λ,p)=s(p)⁻¹ Λ s(Λ⁻¹p). Aplicar o cociclo de tela já provado após obter orientação, fase unitária e mensurabilidade. Não reconstruir só a lei escalar de cociclo.
3. [OPEN — consumidor L²] Construir U(a,Λ)f(p)=exp(i a·p)D(c(Λ,p))f(Λ⁻¹p), com D=diag(ζ,conj ζ), provar leis de grupo, continuidade forte e coincidência exata com U1, B0 e Jcandidate já existentes. O H1 e as convenções ficam fixos.
4. [OPEN — localização] Definir K(gWR)=U(g)KWR. Primeiro provar independência do representante por invariância sob o estabilizador da cunha. Depois provar isotonia, complemento simplético e localidade da família; construir regiões por interseções/somas fechadas apropriadas e provar a igualdade de colagem. Um nome de cunha sem peso ou a rede nula não paga esta etapa.
5. [OPEN — ponte física separada] O contrato RC1 exige equivalência unitária e entrelaçamento de toda ação/localização do setor físico refinado com a construção contínua. Nem o nome do dispositivo nem uma discretização finita fornecem isso por si.

## Menor próximo lema genuíno

[DERIVED — proposta, não theorem compilado] **Preservação da medida orbital por uma rotação espacial que muda a direção da cunha**, seguida da isometria L² por composição. Uma forma genérica útil é: para Q∈SO(3), R_Q(q,p₁) a ação linear obtida pela identificação (q,p₁)↔p∈ℝ³, provar `MeasurePreserving R_Q (orbitalMeasure 0) (orbitalMeasure 0)`. Isso usa volume preservado e invariância de E=|p|, inclusive no conjunto nulo p=0; depois a ação L² atua no mesmo H1. O lema `LinearIsometryEquiv.measurePreserving` da mathlib (`MeasureTheory/Measure/Haar/InnerProductSpace.lean:151`) paga o volume no modelo euclidiano, não automaticamente a densidade orbital nem a mudança de coordenadas.

É um incremento efetivo: traz rotações espaciais que não são as matrizes angulares 2×2 do plano de boost. **Ainda não** resolve a fase Wigner/helicidade ou o transporte global de KWR; esses consumidores vêm em seguida. A busca `rg --no-ignore` em TGLExt e F1.REDE não localizou um `orbitalRotation`/preservação Lorentz global pronto, no escopo documentado. Nenhum lema novo foi anunciado como provado por esta leitura.

## Dispositivo: o que se reaproveita, sem confundir setores

[DECLARADO — projeto na fonte; REAL — leitura] O Supercondutor fornece a câmara de seis faces, entradas/saídas ópticas e o Hamiltoniano de cavidade/OH, com salto `a_out†σ₋+σ₊a_in` e taxa proporcional ao acoplamento holográfico (linhas 340–389 do TeX). A geometria MQC e a rede tensorial finita, já inventariadas e testadas em F1.REDE, orientam o refinamento. Ψ-NET descreve endereçamento angular/REFLECT/MANIFEST; TGL-Tensor descreve codificação e quantização. Esses contratos não são uma representação Wigner de espaço-tempo.

O modelo finito de regiões e álgebras locais pode ser reaproveitado como ramo mecânico, com dimensões explícitas. A limitação de cyclicidade local em um sistema finito grande, já registrada em CONTRATO_REDE_R2, permanece. A fórmula histórica do TeX contém β arredondado; qualquer cálculo novo deve usar α_CODATA2018√e em runtime. A evolução GKLS de um estado e o grupo modular unitário do par álgebra/estado têm papéis distintos; a ponte deve entrelaçá-los sob um contrato físico declarado.

## Alcance e decisão

Não houve provedor, execução de um.py, teste observado, mudança do Nós/Bancada ou gate. Este é levantamento e rota de construção, não nova prova de globalidade. Não é necessário reconstruir a infraestrutura Fock, os cociclos de tela, a carta orbital ou a antiunitária já existentes. O próximo esforço deve pagar uma ação orbital espacial e depois a fase/localização global, preservando a condição RC1 do contrato e os requisitos R1–R10 da raiz.
'''

result = {
    'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'author': 'codex-atrator-skeptic', 'unit': 'F1.FECHO_20261015', 'claim': 845,
    'statute': 'DERIVED_SOURCE_INVENTORY_NOT_NEW_THEOREM',
    'sources': sources,
    'search_scope': ['TGLExt/**/*.lean (including ignored O16)', 'F1.REDE/**/*.lean excluding attempt duplicates'],
    'search_terms': ['spatialRotation', 'OrbitalRotation', 'rotationUnitary', 'transverseRotation', 'Lorentz/rotation with MeasurePreserving'],
    'next_genuine_lemma': 'Orbital spatial-rotation measure invariance, on the existing orbitalMeasure and H1, before helicity-cocycle and global-localization consumers.',
    'no_global_net_inhabitant_asserted': True, 'new_lean_theorem': False,
    'scope': 'Source-level directed inventory and construction route. Historical source receipts are not silently promoted to current independent compilation.',
    'production_modified': False, 'gate_changed': False,
}

for name, value in [('INVENTARIO_REDE_GLOBAL_R1.md', body),
                    ('INVENTARIO_REDE_GLOBAL_R1.json', json.dumps(result, ensure_ascii=False, indent=2)+'\n')]:
    data = value.encode('utf-8')
    with (HERE/name).open('xb') as f:
        f.write(data)
    assert (HERE/name).read_bytes() == data
print(json.dumps(pin(HERE/'INVENTARIO_REDE_GLOBAL_R1.json')))
