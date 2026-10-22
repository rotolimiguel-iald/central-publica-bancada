# Primeiros resultados na Bancada Um atualizada

10/10/2026 — codex-gerente-tgl — F8.2.NU4, reivindicação 642.

## Resultado

**[REAL — execução] 16 chamadas concluídas na instalação atual da Bancada Um; todos os controles previstos passaram. [DERIVED — condicional] O canal de desfasamento produz uma alteração espectral extremamente pequena na instância tau_star=t_P, Kfac=1. Nenhum sigma observado foi calculado.**

Reaproveitamento: os contratos do autor recuperados em F8.2.NU3 (20 fontes; 10 contratos), o protocolo de referência da F8.2.NU2 e a implantação F0.3.B2. A consulta ao Nós Vivo foi registrada antes de produzir; a unidade nova ainda não está indexada. O grafo não substitui as fontes pinadas no PREREGISTRO_R1.json.

## O cálculo executado

Lei utilizada: dρ/dt = −i[H,ρ]/ℏ − beta0·tau_star·Kfac·[H,[H,ρ]]/(2ℏ²), H=M²/(2E).

Logo, Γij = beta0·tau_star·Kfac·(Δm²ij/(2Eℏ))²/2. O canal preserva as populações na base de massa e atenua as coerências por exp(−Γij·t). [DERIVED — modelo de propagação, H fixo].

- beta0 = alpha_CODATA_2018 × sqrt(e), obtido em runtime: 0.012031300400803142.
- `mu_do_rito: q→0 (Thomson; Teorema da Escala)`.
- [INPUT] tau_star = t_P = 5.391246448313605e-44 s. Esta escolha é uma instância condicional; não determina a amplitude física da TGL.
- [INPUT] Kfac=1, percurso 52.5 km, Δm²21=7,5e−5 eV², Δm²31=2,5e−3 eV², sin²θ12=0,307, sin²θ13=0,022. São referências herdadas, não parâmetros ajustados à amostra.
- ℏ da implementação = 6.582119569000e-16 eV·s. Seu arredondamento explica pequenas diferenças frente ao cálculo NU2 que deriva ℏ de h/eV.

Pee é a probabilidade de sobrevivência do estado eletrônico coerente. A diferença é TGL menos a evolução unitária com os mesmos inputs.

| E (MeV) | Γ21 (s⁻¹) | Γ31 (s⁻¹) | 1−exp(−Γ31 t) | ΔPee |
|---:|---:|---:|---:|---:|
| 2 | 2.631738715e-37 | 2.924154128e-34 | 5.120812337e-38 | +1.788067158e-39 |
| 4 | 6.579346789e-38 | 7.310385321e-35 | 1.280203084e-38 | -1.195567842e-40 |
| 8 | 1.644836697e-38 | 1.827596330e-35 | 3.200507710e-39 | +1.053061949e-40 |

Foi usada a perda de coerência calculada por −expm1(−Γt). Subtrair diretamente as duas probabilidades em ponto flutuante retorna zero nestes três casos; esse zero numérico não é um resultado físico. A taxa obedeceu E⁻², com redução por fator 4 ao dobrar E. O sinal de ΔPee muda com a fase oscilatória.

## Controles

- Traço: 1 dentro da tolerância 2e−12; positividade dentro da mesma tolerância.
- Energia: deriva numérica zero para Tr(ρH), com H diagonal fixo. Isso não prova por si conservação local de T_mu_nu num modelo estelar acoplado.
- Estado diagonal diag(0,2;0,3;0,5): permaneceu exatamente igual, para tau=0, tau=t_P e controle positivo. Este desfasamento sozinho não redistribui essas populações.
- Controle positivo [INPUT instrumental]: tau_ctrl escolhido antes por Γ31·t=0,1 a 4 MeV, resultando 4.211243134073e-07 s. Perda de coerência = 0.095162581964; ΔPee = -0.000889064398731. Confirma detecção pelo código de um efeito finito; não é estimativa de tau_star nem evidência física.
- Paridade: s=0, 0,5, 1; canal modular: autovalores 0, 1, 4, s=1. São controles separados, sem traduzir probabilidade adimensional em rendimento estelar.
- Escala v388: avaliados chi=0 e chi_fr=2acosh(1/alpha). A segunda recupera beta0. beta_bulk não foi inserido no dissipador físico sem um mapa para a situação experimental.

## O que estes resultados permitem dizer

Os contratos existentes já têm realizações computacionais verificadas na bancada. **Esta instância não entregou um sinal de 5sigma.** Um cálculo de significância exigiria dados e resposta instrumental, covariância e hipóteses físicas especificadas. O limite publicado do JUNO não é uma likelihood e usa uma textura Γ21=Γ31, Γ32=0, diferente da textura gap² deste ensaio.

O teste não calcula luminosidade bolométrica nem Massa de Chandrasekhar. Para esse objetivo, o passo seguinte é compor o contrato de produção/transporte dos artigos com as taxas fracas, Ye e estrutura estelar, e fixar tau_star/Kfac/chi quando pertinentes. Não se deduz essa composição de uma alteração de fase isolada. O resultado condicional aqui não exclui todos os canais de neutrinos da TGL.

Nenhum parâmetro foi escolhido para obter 5sigma. Não houve ajuste a dados observados, abertura de rito selado, comunicação ao Claude ou chamada de provedor. Gate intacto. A conferência independente desta execução fica em review/ e será pinada na entrega.

## Reprodução e custódia

Protocolo: PREREGISTRO_R1.json, sha256 `6d22605043111032f410eb7c6cb223b7a75d60f5abdbcfd15980d7c154d8d3ce`.
Resultado completo: RESULTADOS_R1.json, sha256 `ec18cfbd5a245d9a10e1bb446f7db86769cadfeca462a0172680047d8cd46482`.
Runner: run_pilot_r1.py, sha256 `50fba3ae2f7188f5a9ff697f4139598cc1000009ea8e81e056027daa014d3502`.
Manifesto instalado: `54fc9e27e4599c49990adb9587a45a8858393f2d8f5d66ec3e022b8140757c1b`; programa v391, `8e7b9927ceae64b8b6812019f77cca24c08296222ae7968af41baf2fe7a67dc6`.
Os 16 arquivos CALL_*.json guardam pedido, resposta e identidade na entrada/saída. A duração registrada foi 11.663 s. Não reexecutar o runner R1 sobre esses arquivos: uma repetição legítima deve usar outra pasta/nome e declarar seu motivo.
