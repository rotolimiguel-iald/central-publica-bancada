# Entrega delimitada — R-A, covariância e cinco hipóteses

[DERIVED — condicional; REAL — controles sintéticos; nenhum novo veredito observacional]

Esta contribuição atende à solicitação da coordenação `48132f8d-c56d-4e3f-ae5e-1b31e173d418`, ORDEM018 do TÚNEL de 05/10/2026. Não substitui F0–F4, a auditoria de proveniência ou o V1 da gerência. O mapa foi consultado antes: `hubble.fase9_razao_discriminante`, seq 373. A fonte da crítica anterior foi conferida byte a byte contra o hash desse registro.

**Entrega principal:** [revisão matemática](covariance_identifiability/REVISAO_LOCAL.md), [controles sintéticos](covariance_identifiability/SYNTHETIC_CHECKS.json), [fontes por hash](covariance_identifiability/FONTES.json).

O que se torna operacional:

1. Deslocamento universal e β livre são reparametrizações no recorte de K comum; isso já estava na crítica da gerência e não foi apresentado como descoberta nova. A evidência deve transportar o Jacobiano do prior se a comparação pretende representar a mesma hipótese.
2. Deslocamento **só nas Cefeidas** é diferente: com outros leitores e respostas instrumentais definidas, o contraste entre métodos pode discriminá-lo de um fator universal. O controle de posto passou: universal local=1, com vínculo de fundo=2, seletivo com dois tipos de leitores=2.
3. Componentes de erro comum entram uma vez. A matriz C=D+ASAᵀ e o modelo com nuisance latente marginalizado são representações alternativas da mesma fonte de incerteza; não devem duplicá-la. Um erro comum pode limitar a média e cancelar no contraste. Os controles numéricos são exemplos sintéticos sem H₀ observado.
4. «Fundo livre» ainda precisa de definição única no V1: multiplicador do fundo e r_d livre não são o mesmo rival. O segundo exige as previsões e a likelihood BAO correspondentes, não só um número H₀ derivado com r_d fixado. Não equivale automaticamente a EDE.
5. A retrodição sem ajuste e a novidade de uso são preservadas. A cronologia existente deve ser conferida; não foi refeita. Nenhum dado novo foi aberto para compor veredito.

**Revisão cética preparada, não executada:** `covariance_identifiability/UNIT_MIMO.json`, request_id `a4534bcd-8058-48a7-b5fa-34bc046dc46e`. Uma chamada máxima na unidade, provedor obrigatório MiMo, memória científica comum, sem fallback. A prévia oficial recusou a validação da âncora do Supercondutor antes de selecionar um provedor, tanto no contexto restrito como no usuário normal IALD\rotol. Não houve envio, consumo remoto ou job novo. Não se alterou âncora, geração ou pedido antigo para contornar a recusa.

## MEDIDA técnica e alternativas executadas

- A: `prepare_unit.py preview` — CLI oficial `operation=preview_execution`, rc do subprocesso 1, 0,135128 s. Recibo `PREVIEW_REFUSAL.json`.
- B: mesmo payload e operação em processo normal Windows, identidade conferida no recibo — rc 1, 0,191411 s. Recibo `PREVIEW_NORMAL_REFUSAL.json`.
- Motivo observado em ambas: «Âncora do Supercondutor mudou ou não pôde ser lida; conferir antes de selecionar». A mensagem não distingue sozinha mudança de bytes e impossibilidade de leitura. Não atribuir à API/cota do MiMo nem ao pin antigo do Claude.
- Continuidade executada: revisão matemática local e controles sintéticos concluídos, artefatos entregues à coordenação para auditoria. A decisão de eventual reparo do transporte pertence à frente responsável. O trabalho científico desta unidade não depende de anunciar uma resposta remota inexistente.

Fontes/estatutos e limitações completas estão na nota. Os dados canônicos, o pré-registro congelado do ringdown, A/B/C/D, os serviços e o gate permaneceram intactos. Os artefatos desta entrega ficam sob `Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/`; não foi gravado nada no Nós.
