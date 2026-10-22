[REAL — leitor e avaliador contínuos verificados; OPEN — integral/calibração físicas]

# ORDEM 013 — Curvas contínuas iniciadas

Registro:2026-09-22T10:07:23.151865+00:00. N/A — sem Lean. Cânone, Atlas e C6 preservados.

## Critérios e evidências

- **PAGO, aritmética:** `continuous_source_calibration.py` reutiliza a função
  de importância pareada existente. O erro máximo contra quadratura de
  Gauss–Legendre foi 0.726097662 erros MC;
  a covariância foi conferida por somas independentes em long double, erro
  7.94203502e-17. Propostas de integrando
  zero continuam no denominador. Não se multiplicam mocks.
- **PAGO, geometria do leitor:** reutiliza `profile_intervals`. No oráculo
  gaussiano, erro MLE=2.77555756e-16 e erro de limites
  =0.00152112919. Os nove controles recusados
  incluem curva plana, borda, ilhas desconexas, fonte dominante, NaN e ruído
  duplicado. Mock com falha não é removido para melhorar a cobertura.
- **PAGO, avaliador de forma de onda:** 3 pontos reais,
  306 comparações diretas, 17 intensidades de −4 a4
  com passo0,5. Máximo erro relativo=1.05977555e-07,
  logL=1.17639993e-05, quadratura de fase
  =4.47066679e-06. Os extremos a=0/1 reproduzem os
  checkpoints anteriores com erro 0.
  Os dois critérios de seleção SEOB apontaram ao mesmo ponto1002: por isso
  são TRÊS pontos distintos, não quatro. Não extrapolar este controle pontual
  para todo o domínio; cada ponto novo enfrenta os controles completos.
- **INICIADO, ainda NÃO PAGO:** curvas SEOB para16384 propostas,8520 válidas,
  handle19681,dois trabalhadores. Primeiros48 pontos
  completos conferidos com seus controles embutidos. O conjunto inclui todos
  os1200 mocks congelados; reutiliza as mesmas coordenadas de fonte da rodada
  binária. São novas intensidades, não novas observações independentes.
- **REGISTRADO, NÃO INICIADO:** extensão Phenom32768/22384 válidas. A rodada
  binária Phenom34860 e a SEOB40860 continuam com quatro trabalhadores cada.
- **NÃO PAGO:** viés/cobertura físicos, repetição independente das curvas,
  controle de resolução nos pontos dominantes dessas novas curvas, mistura
  das famílias e demais leituras/SNR exigidos no objetivo completo.

## Tipagem estatística

Não foi escolhido prior para a, nem alterado β. O leitor calcula intervalos
de razão de verossimilhança sobre Z(a) marginalizado nos parâmetros da fonte.
Não os chama de intervalos bayesianos nem presume cobertura por Wilks: a
cobertura precisa ser medida nas injeções. Curva plana, ilha desconexa,
intervalo truncado, grade sem resolução ou fonte sem precisão deixam a
cobertura calibrada como nula/indisponível; diagnósticos brutos permanecem.
Intensidade negativa é controle numérico, não dinâmica GKLS física.
Uma comparação passo0,5/1,0 é necessária, mas não prova resolução final:
domínio/grade maiores podem ser exigidos. O máximo deslocamento aceito do
MLE e das duas bordas nessa comparação foi registrado em0,05unidades de a.

## Continuação e reprodução

Em `cache/source_evidence`, no Python WSL `/opt/pycbc_env/bin/python -B`:

1. Revalidar os handles34860,40860,19681. Não duplicar execução viva.
2. Quando19681 terminar, conferir `EVALUATIONS_COMPLETE.json` e rodar
   `run_continuous_source_curves.py analyze --family SEOBNRv4HM`.
3. Para Phenom, registro pronto; iniciar
   `run_continuous_source_curves.py run --family IMRPhenomXPHM --workers 2`
   quando houver capacidade, e depois seu `analyze`.
4. Comparar os extremos integrados das curvas às integrais binárias respectivas
   (mesmas propostas) e fazer auditoria independente; preservam-se as exigências
   de densidade, repetição e resolução. O runner emite diagnóstico, nunca
   aceitação científica automática.
5. A mistura binária já registrada continua Phenom16384+SEOB16384. Não trocar
   silenciosamente o primeiro pelo novo32768.

Nenhum teste de natureza moveu gate; nenhum resultado novo em sigma.
Tentativas anteriores e registros congelados mantidos. Ficha de aproveitamento:
reutilizados estimador de importância, leitor de intervalos, geradores completos,
adaptador SEOB nativo, leitor Fourier real, priors, propostas e ruídos existentes.
Acrescentadas apenas a ligação para curvas contínuas, controles e execução.

## Custódia

Hashes SHA256 lidos por script:

- `cache/source_evidence/continuous_source_calibration.py`: `f206fa9237654a1369eea9c3ddd966fa2f2f1d5bfa464e4ff10ec9d252cef0fb`
- `cache/source_evidence/validate_continuous_calibration.py`: `64ea0a49fdc80ec4cd56dbfdbef8a315b2fc5bbb87afcea942e5221390431ad7`
- `cache/source_evidence/controlled_continuous_source.py`: `3373a580390ca51a7953667ed2055e83c8d58a9220119e0deb9d3a32ed0aa3c8`
- `cache/source_evidence/validate_controlled_continuous_source.py`: `3aeb109b923cf7929a9f41f7254243fde6f9b78dfcea19494cdee409bfb9cf91`
- `cache/source_evidence/run_continuous_source_curves.py`: `7473bda8e5c5a306589159c80866ea469efae9b49a98f168b91d02303062497c`
- `cache/source_evidence/continuous_calibration_validation/REGISTRATION.json`: `1b2e60cc0d886b945e3ac30f323f60cf95b12924bf2a0dda0cd2a6c063d8fbe0`
- `cache/source_evidence/continuous_calibration_validation/RESULT.json`: `9d60fdee82bcdc85f5991489121210063f7371e78fa2e1add0486b689262b455`
- `cache/source_evidence/controlled_continuous_validation/REGISTRATION.json`: `b15519af4f3d5fb139135bd8cb093402c8e619f49808bbe55db71172bff0b941`
- `cache/source_evidence/controlled_continuous_validation/RESULT.json`: `00751b1f30161d224f7a27dd8c37cbdd9f2e9d0d2a4a4f83af01e06c8cb961f9`
- `cache/source_evidence/continuous_source_curves\SEOBNRv4HM_seed130942_N16384\REGISTRATION.json`: `93ba610c6889e804952190f9b6a6e000bf7cbf86f1906cede9f951798fe94064`
- `cache/source_evidence/continuous_source_curves\IMRPhenomXPHM_seed130972_N32768\REGISTRATION.json`: `fc82a1ba786a0e0d16175d0962f26b3757e1c725ac4a051c10eb57be1b9b96c2`
- `cache/source_evidence/continuous_source_curves\SEOBNRv4HM_seed130942_N16384\START.json`: `5751d1f460859af461390b7b6835fa7f1c176486609ccf193d1877532527be7e`
- `record_continuous_curve_start.py`: `f3c63aac91ab2718ad91c67acfb6897d8727a04eb8d4b11fe871118a3f7d70d1`
