# Rede: inventário de reaproveitamento R1

[REAL — leitura de fontes; não é nova auditoria Lean]. Unidade F1.FECHO_20261015, reivindicação845. Nenhum original alterado.
O nome da classe sempre se refere ao consumidor descrito; importação transitiva não prova identificação entre realizações.

## PoincareGroup.lean
- Classe: EXISTE_LIGADO
- Fonte: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\PoincareGroup.lean`; SHA256 `c73c927631381aa78136222d30783aa393735a146607e799371db22b4a4466db`.
- Âncoras: structure PoincareGroup — linhas [242]; theorem poincare_faithful — linhas [319]
- Consumo: Grupo e ação afim usados em PoincareWitness; no fecho de imports QGSolutionComplete.
- Resíduo: Não identifica essa ação com a representação fotônica canônica em H1.

## PoincareWitness.lean
- Classe: EXISTE_LIGADO
- Fonte: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\PoincareWitness.lean`; SHA256 `848f2937f35ec50b2ab483336cc3ba17c46135eb52c17418bc1fbc1530f568ad`.
- Âncoras: def thePoincareWitness — linhas [144]; theorem proper_sector_fibers_blind — linhas [260]
- Consumo: Habitante FullWitnessData; covariância e sensibilidade à paridade.
- Resíduo: O setor próprio age trivialmente nas fibras deste habitante, como teorema.

## WedgeNet.lean
- Classe: EXISTE_LIGADO
- Fonte: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\WedgeNet.lean`; SHA256 `be5a629740df809a2c2157dc6e99bef116704f1373276d0a979785ba37dce463`.
- Âncoras: def wedgeNet — linhas [317]; def theSpecificAQFTWitness — linhas [357]; Hilbert (U ≡ 1) — linhas [32]
- Consumo: Rede concreta não abeliana, vácuo cíclico/separante; fecho QG.
- Resíduo: Translações triviais nesta realização; não identificar com lightNet.

## WedgeNetFiniteDiamond.lean
- Classe: EXISTE_NAO_LIGADO_A_REDE_FOTONICA
- Fonte: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\WedgeNetFiniteDiamond.lean`; SHA256 `1772831452bab2ef5626004819e07202f7d39f956b5c2455e895ff7159cbc91c`.
- Âncoras: theorem finite_diamond_has_scalar_algebra — linhas [77]
- Consumo: Controle de alcance da rede WedgeNet.
- Resíduo: Diamantes limitados têm álgebra escalar nesta rede específica.

## V350L2CharacterMultiplier.lean
- Classe: EXISTE_LIGADO
- Fonte: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\V350L2CharacterMultiplier.lean`; SHA256 `2f7c413ee9ebd5ba93d1222bb596da11972a0b6b4efa1a71a04becb6ff856ca3`.
- Âncoras: theorem characterMultiplier_weyl — linhas [160]
- Consumo: Weyl entre multiplicador de caracteres e translação no Hilbert regular.
- Resíduo: Não é por identidade de nome a família W(f) do Fock canônico.

## TheImportedSecondQuantization.lean
- Classe: EXISTE_LIGADO_CONDICIONAL_KNOWN
- Fonte: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\TheImportedSecondQuantization.lean`; SHA256 `ef35478400ef07f20476f2bb937d8fbe2df7b9e506139f54dc5a37401e7d5242`.
- Âncoras: structure FockCertificate — linhas [168]; def lightNet — linhas [308]; theorem light_kms — linhas [440]; def lightH3 — linhas [547, 558]; theorem qg_formalized_by_citation — linhas [589]
- Consumo: Weyl/localidade, Tomita/KMS e core estão tipados como campos citados; consumidores existentes.
- Resíduo: Realização simultânea dos campos ainda importados sobre o mesmo Fock; não alegar teoremas ausentes.

## MaxwellLiteratureBridge.lean
- Classe: EXISTE_LIGADO
- Fonte: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\MaxwellLiteratureBridge.lean`; SHA256 `c07d135fac53737465c50636204da7ee79d27ced9df3867382d1e190781febe4`.
- Âncoras: structure MaxwellQuadraticForm — linhas [37]; def toStress — linhas [73]; def toCertificate — linhas [120]
- Consumo: Extensão por zero paga a passagem de forma no domínio a tensor total; consumida pela v375/v376.
- Resíduo: Forma Q e hipóteses charge_link/nontrivial da realização específica continuam explícitas.

## TheWholeIsOne.lean
- Classe: EXISTE_LIGADO
- Fonte: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\TheWholeIsOne.lean`; SHA256 `097236427302ae42857b1cfc3e89711b45f7bc34fe02e5374bc0903a34d1a608`.
- Âncoras: (Q : TGLExt.MaxwellBridge.MaxwellQuadraticForm C) — linhas [111]
- Consumo: Consumo formal da ponte Maxwell no teorema da v376.
- Resíduo: As hipóteses do mesmo par físico não desaparecem pelo consumo.

## MaxwellPolynomial_v2.lean
- Classe: EXISTE_NAO_LIGADO_A_EXPECTATIVA_WICK
- Fonte: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\O16\MaxwellPolynomial_v2.lean`; SHA256 `5e5460abca91081c2c62a1454e3660273e93952b51f739cb34825941ae3c2782`.
- Âncoras: theorem maxwell_symmetric — linhas [26]; theorem maxwell_null_flux_nonnegative — linhas [43]
- Consumo: Tensor clássico polinomial, cinco identidades já construídas na ORDEM016.
- Resíduo: Não identifica expectativa de Wick no domínio do Fock.

## ConcreteLightRayNet.lean
- Classe: EXISTE_NAO_LIGADO_A_CERTIFICADO_GLOBAL
- Fonte: `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.REDE\light_ray\ConcreteLightRayNet.lean`; SHA256 `512812b32d09f26e9b5ee5a94f6e4afc08e717602ae2d96bb3498980a9ff02bc`.
- Âncoras: def halfline — linhas [74]; theorem halfline_antitone — linhas [103]; theorem no_four_dimensional_promotion — linhas [133]
- Consumo: Rede de semirretas concretas padrão e não nulas, usando O16.
- Resíduo: Hilbert escalar da reta não é automaticamente H1 orbital nem rede4D.

## CanonicalOutput.lean
- Classe: EXISTE_NAO_LIGADO_A_CERTIFICADO_GLOBAL
- Fonte: `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.REDE\modular_wedge\CanonicalOutput.lean`; SHA256 `2ff7e40f04f95c693b0def903f6e0d622cdd1a53c38dce1b43c55e36199398ca`.
- Âncoras: def spectralOutput — linhas [66]; theorem spectralOutput_nonzero — linhas [85]; theorem delta_is_SdagS — linhas [35]
- Consumo: Habitante concreto do contrato D1a3 no H1 canônico.
- Resíduo: Glue da rede global ao KWR concreto deve ser fornecido explicitamente.

## BosonicFock.lean
- Classe: EXISTE_NAO_LIGADO_A_CERTIFICADO_COMPLETO
- Fonte: `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.REDE\fock_construction\BosonicFock.lean`; SHA256 `c7d24c14f9bb1c2a31c3b207a9f86e839577b6705c4b55b2aa6eab187450d3ec`.
- Âncoras: abbrev F := — linhas [18]; def gamma — linhas [20]; def oneParticle — linhas [22]; theorem infinite_dimensional — linhas [57]
- Consumo: Fock concreto, vácuo, Γ funtorial, inclusão H1; campos cinemáticos pagos.
- Resíduo: Fiação desses campos ao FockCertificate é o alvo desta candidata.

## BosonicFockContinuity.lean
- Classe: EXISTE_NAO_LIGADO_A_CERTIFICADO_COMPLETO
- Fonte: `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.REDE\fock_construction\BosonicFockContinuity.lean`; SHA256 `03ebc19982aec9d470fdb18d64efc67dff649320ce704305d6d70d9a863080b9`.
- Âncoras: theorem gamma_strong — linhas [16, 24, 28]; theorem boosts_strong — linhas [36]
- Consumo: Continuidade forte para parâmetros gerais, inclusive ℝ e ℝ4.
- Resíduo: Não reintroduzir continuidade como campo importado.

## CONSTRUCAO_CONTINUA_R1.md
- Classe: KNOWN_DERIVED_DOCUMENTAL
- Fonte: `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.REDE\CONSTRUCAO_CONTINUA_R1.md`; SHA256 `fea72d71ac891255b08428999810940e3508f11f0059e0d56e93bb64980c1a19`.
- Âncoras: Defina K(gW_R)=U(g)K(W_R). — linhas [125]; defina A(O)={W(f):f∈K(O)} — linhas [130]
- Consumo: Construção analítica por Wigner/BGL, com referências e revisão.
- Resíduo: Formalização integral e identificação de dispositivo constituem alvos diferentes.

## MATRIZ_CONTRATO_FOCK_R2.json
- Classe: OPEN_CONSTRUCAO_ESPECIFICA_KNOWN_LITERATURA
- Fonte: `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.REDE\MATRIZ_CONTRATO_FOCK_R2.json`; SHA256 `39a3c34f5d64a7f737ca128bf415290c4703fba02bf410c008c44ac01d75a932`.
- Âncoras: OPEN_CONSTRUCTION_KNOWN_LITERATURE — linhas [144, 149, 154, 159, 164, 169]; Correspondentes concretos de campos — linhas [8]
- Consumo: Matriz dos campos pagos versus importados.
- Resíduo: Residuo apenas no mesmo Fock; não é ausência da teoria conhecida.

## HANDOFF_SUBMITTED_R3_20261014.json
- Classe: MISSOES_EXISTENTES_NAO_DUPLICAR
- Fonte: `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.REDE\orchestration_r3\HANDOFF_SUBMITTED_R3_20261014.json`; SHA256 `b3beb7d511ad8162c4055c6613870dfa0e7b17d9000bc4adf388753ac1f3d0f4`.
- Âncoras: fock_exponential_vectors_totality_r3 — linhas [29, 53]; fock_antiunitary_second_quantization_r3 — linhas [70, 94]
- Consumo: MiMo: exponenciais/totalidade; DeepSeek: Γ(J). IDs preservados.
- Resíduo: Este trabalho não constrói esses alvos nem despacha novamente.
