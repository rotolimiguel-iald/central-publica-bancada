# F2.3 — adendo ao lado: ramo C com família de cunhas nomeada

[REAL — 08/10/2026] Consulta prévia ao Nós Vivo, unidade F2.3: a implicação curvada e a pedra anterior já estavam na bancada; o quadro a marcava AUDITADA. Este adendo preserva integralmente a entrega anterior. CR-08 classifica a implicação v317/v338 como existente, sem o antecedente físico ligado ao tipo da declaração. CR-09 corrige a falsa identificação das rotações angulares 2×2 de O16 com as rotações de espaço-tempo da rede da luz.

## Termo novo e alcance

ChatgptAudit.F23CurvedFieldBranchC.passage_with_light_lorentz_wedges_all_null_h3_to_einstein_atlas, em LiganteLeiCampoCurvoRamoC.lean, é uma implicação condicional no sandbox. Dadas as hipóteses nomeadas abaixo, conclui um único Λ no atlas suave fornecido e, em cada carta, recordEinstein + Λ g = (8πG) T_Maxwell(ψ), com η=(4G)⁻¹ e 2π/η=8πG. A identidade do coeficiente usa entropy_density_einstein_coefficient; a implicação e a unicidade vêm de connected_smooth_atlas_einstein. Não se constrói solução global de Einstein.

- [INPUT] LightLorentzWedgeFamilyEveryNullDirection: para cada carta, ponto e direção nula não nula, fornece uma região de cunha, fluxo Lorentz pontual, expansão nula e covariância da rede da luz. O tipo é um contrato pontual assumido. Não constrói a representação global coerente de Lorentz/Poincaré nem a família física BGL.
- [INPUT] hH3_from_passage_and_wedges: lei de área/Clausius em todas essas telas. A prova usa da cunha somente horizon_touch; os campos de boost, expansão e covariância tipam o contrato, mas não são usados para derivar H3. A tela screens do registro não é provada como tela construída da cunha. Essa identificação e toda a lei física estão contidas em hH3_from_passage_and_wedges.
- [INPUT] source_matches_maxwell: identifica a fonte recordSource de cada carta ao mesmo tensor M.T.T ψ nas coordenadas locais. É uma ponte forte de tipos, não transporte físico demonstrado. M.T é StressTensorDataLocalV32, com simetria e conservação distribucional planas; a premissa separada conserved_curved é a conservação covariante Levi-Civita exigida por AreaChart. Nenhuma implica automaticamente a outra.
- [INPUT] métricas, telas, cobertura, cartas e transições suaves. O estado ψ está irrestrito: o termo não exige Regular M.Dom ... ψ, não usa lightH3 nem charge_link, e não liga H3 ao estado Maxwell.

A passagem finita the_post_lives_in_the_passage é aplicada, mas a auditoria c1 já demonstrou a ociosidade lógica desse passo: sob suas premissas, o resultado da passagem está provado; logo hH3_from_passage_and_wedges carrega a lacuna de H3 inteira. Não há ganho de conteúdo físico sobre a implicação v338. A pedra apenas expõe, no nome e no tipo, as fiações que a conclusão em todas as direções exige.

A rotação angular SO(2) de RotationGeneratorBridges.lean e WickBoostRotation_v2.lean não entra neste termo; ela não é rotação de espaço-tempo da rede da luz. H3 derivado do estado e a família física global seguem abertos ou sabidos por citação no alcance de CR-08/CR-09.

## Verificação local

Lean 4.31.0 compilou diretamente kernel/TGLExt/LiganteLeiCampoCurvoRamoC.lean na cópia F2.3; exit code 0, .olean não vazio, nenhum erro ou aviso no BUILD_RAMOC_FINAL.log, nenhum sorry, admit ou novo axiom na fonte. #print axioms do teorema e das estruturas: somente propext, Classical.choice, Quot.sound. Os caches .olean do Nós original foram lidos; nenhum arquivo do Nós original foi escrito. Este build não move gate nem integra um.py.
