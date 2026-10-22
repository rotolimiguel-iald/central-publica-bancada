
## 08/10/2026 — sexta camada ao lado: alcance da leitura polar (F1.1.E1)

<!-- F11_E1_ERRATA_LEITURA_R2_R5_20261008 -->

[REAL — aferição de fontes; em nome de codex-gerente-tgl, pela unidade F1.1.E1] Esta camada corrige a classificação relativa e as citações da quinta camada. A F1.1 original permanece FECHADA. O inventário anterior conserva seus bytes como prefixo; esta nota não instala pedra nem move o gate.

| Ressalva | Leitura vigente e evidência |
|---|---|
| **R2 — classe relativa** | **1. EXISTE E ESTÁ LIGADO** vale **dentro do O16**: `TGLExt/O16.lean:19,48,96` importa, respectivamente, `ContractCalibrationReuse`, `HorizonDataReuse_Integration_v2` e `PeriodHeatCalibration_v3`. Em relação à assinatura QG, as pedras polares são **2. EXISTE NO KERNEL, NÃO LIGADO À ASSINATURA (fiação)**. `QGSolutionComplete.lean:1–4,79–91` não as importa nem as recebe no enunciado. A sonda c1 `fecho_qg.log` (exit 0) encontrou zero constantes dos namespaces `PolarPeriod016`, `CalibrationReuse016` e `Wick016` no fecho de `qg_solution_end_to_end`; `lightH2` está no fecho, mas os lemas polares não. |
| **R3 — consumidores já existentes** | `ChatgptAudit.CalibrationReuse016.polar_period_matches_contract` (`ContractCalibrationReuse.lean:102–107`) demonstra, para um `ContratoH2` e quociente fiel de período positivo, `1/P = C.unruhTemperature`. `TGLExt.ContratoQGv31.ContratoH3.data_temperature_from_same_period` (`HorizonDataReuse_Integration_v2.lean:23–29`) demonstra `κ/(2π) = 1/P` para o mesmo H3; o `κ` desse `toHorizonData` é o que figura no Clausius da assinatura (`QGSolutionComplete.lean:89–91`). São **termos condicionais já presentes no O16**, ainda a fiar à assinatura geral; não exibem H3 em todos os pontos, estado KMS nem família de cunhas em todas as direções. |
| **R4 — citação composta** | A frase da quinta camada «a primeira leitura identifica; reler não acrescenta» combina o título da docstring com outra oração; **não é citação verbatim**. A docstring exata de `TheObserverReadsTheAngle.lean:110–113` diz: «RELER NÃO ACRESCENTA» e «A primeira leitura identifica; a segunda confirma que a operação não altera». O teorema `observing_adds_nothing` em `:114–116` prova a idempotência `P₊·(P₊·𝒪_θ)=P₊·𝒪_θ`; a leitura de identidade física permanece [INPUT/ONTO], não nova conclusão Lean. |
| **R5 — nome vigente** | A candidata da gerência chama-se **PALAVRA**, `TGLExt.Palavra` (`Palavra.lean:8,59,99`), por nomeação do operador. Está em sandbox; esta errata não a trata como pedra instalada. Onde a quinta camada diz `TheReadingCreatesTheObject`, leia-se o nome vigente PALAVRA. |

[REAL — processo] A escrita de memória da errata de leitura às **04:47** ocorreu sem unidade de memória reivindicada. A c1 corrigiu, em nome próprio, a atribuição temporal: **04:29** foi o ramo C e **04:58** foi a pedra Temperatura, não o ramo C. Esta E1 foi reivindicada para corrigir o inventário; as correções dos dois `CLAUDE.md` pertencem à c1 e não são alteradas aqui.

**SHA-256 das fontes, medidos dos bytes nesta aferição:**

- `TGLExt/O16.lean`: `09d4a489dd7e23b09218480d1b01929b16e11a6e5ad6a99337fb3654edd34edf`.
- `TGLExt/QGSolutionComplete.lean`: `8c3a4bc82c5c4308515063254744cfaefcc7e7b926038221be2e7de6293dc598`.
- `TGLExt/O16/ContractCalibrationReuse.lean`: `f447d2de1f54774cb53b5808fa99b3095536606695d8c0efad36675dd80326c9`.
- `TGLExt/O16/HorizonDataReuse_Integration_v2.lean`: `eeae8a4e4b40ed68e854e8a78b545363157dd14ca17c006764a63877b531b65f`.
- `TGLExt/O16/PeriodHeatCalibration_v3.lean`: `e347d2331376bb76d8e56a60a2c3b5b86af1267bc742486b57fd4dc46acb21cc`.
- `TGLExt/O16/PolarMinimalPeriod_v2.lean`: `2112c0022287be0941a798f67e3f5d6f47251e26067ed7ba64516a38424364dc`.
- `TGLExt/O16/PolarQuotientGeometry_v2.lean`: `7e1f9df29a06451b6c6d24816055503fe10437038198551d149cbff127f0e197`.
- `TGLExt/TheObserverReadsTheAngle.lean`: `c764e90722306f988d8c92acc1ae4d8642ec2d6e32a47b810bd8bc5546e5484d`.
- `work/leitura_cria_o_objeto_07out/Palavra.lean`: `33184b49a8bba7e754a66096a89ebeeef44e79dab00c22f49f7af77f0e5400c7`.
- `AUDITORIA_F2_3_F1_1_temperatura_C1_abe2cbdf.md`: `6a8ce1ef046a0a0fe7ed14de85df3fa30925fc00e76932340311151f62a1115a`.

[REAL — limite] A leitura polar e a temperatura relativa ao relógio `N` não constroem, por si, a ação global de Lorentz/PCT nem um habitante dos certificados. A quinta camada e as anteriores seguem preservadas. `NOT_FALSIFIED` não é `CONFIRMED`.
