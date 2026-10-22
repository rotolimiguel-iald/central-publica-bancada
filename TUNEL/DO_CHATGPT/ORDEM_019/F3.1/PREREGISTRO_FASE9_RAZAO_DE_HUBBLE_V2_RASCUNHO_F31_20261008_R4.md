# Fase 9 V2 R4 — rascunho aditivo, sem congelamento

Spec sha256: d6b6486b8a761028ec6f839ff6cd04fea49693eb5d0c2d39c62feb9ca345ea31. R3 sha256: 34ee2e2004e72a83cb52dd40b38dc5faa4d1940baa429d3278a2f72ce5f30e50. V1 sha256: 1893261e730994b3508d14dd2105f8aae3a764d3d217e28bd5939cb58f865273.

[REAL documental] As partes do V1 perdidas na substituição R3 estão incorporadas no JSON R4: estatísticas, função completa, base e 14 pins históricos, runner, novidade de uso e guarda n_local>1.
[REAL documental] Dos 14 pins históricos, 12 coincidem com os bytes atuais. um.py e selo têm hashes atuais diferentes por versões posteriores. A R4 preserva o V1 sem atribuir seus pins ao pacote ativo.

## SBF 0,031

[INPUT] Literal do gerador R2:126, usado para normalizar as amplitudes SBF. A origem bibliográfica é [OPEN]. [DERIVED] 2,3/73,8=0.031165311653, que arredonda a 0,031, mas essa coincidência não demonstra a origem.
[DERIVED] Na caixa só com sigma, sigma_max é 0.949355167 com 0,031 e 0.949392151 com 2,3/73,8. O efeito no teste desta sensibilidade é desprezível; nenhuma verossimilhança original foi recuperada.

## Pontas diagnósticas

- [DERIVED] R_r25: sigma_min=0.749377894; sigma_max=0.863450132; apenas sigma.
- [DERIVED] S_com_sirenes: sigma_min=0.801415560; sigma_max=0.945992846; apenas sigma.

## Regra e limite

Função proposta veredito_fase9_v2_r4_proposta, sha256 98ba17095fc8f84d053f8b7ab18f8c0125db323aba930e487bcb49bea924c14d; 12 ramos sintéticos passaram. O texto exato fica dentro do JSON.
n_local>1 antecede qualquer avaliação de dispersão. O caso de um leitor com p pequeno foi exercitado sinteticamente e não foi classificado por dispersão.
Se a regra recebesse hoje o inventário documental, o token seria TGL_FASE9_RAZAO_DE_HUBBLE_V2_R4_DRAFT__INCONCLUSIVE_SYSTEMATICS__D1B__FUNDO_BG1__NOT_BLIND_TO_DATA_STATED__NOT_A_CONFIRMATION__GATE_UNTOUCHED; isso é simulação, não abertura.
F3.4 e X13 antecedem congelamento; D-H antecede abertura; D-J nomeia o token final. NOT_FALSIFIED não credita e nenhum gate foi movido.
