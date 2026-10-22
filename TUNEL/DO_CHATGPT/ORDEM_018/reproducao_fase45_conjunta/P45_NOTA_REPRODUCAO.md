# Reprodução histórica independente — P/F4 e P/F5

[REAL — reprodução computacional histórica, F1(b)] As três configurações reproduziram os alvos arquivados dentro das tolerâncias de engenharia congeladas antes da execução. Foram executados oito ajustes: três em P/F4, três em P/F5 sombra e dois em P/F5 acumulada. O LCDM de P/F5 é idêntico entre leituras quando beta=0 e foi reutilizado, com proveniência explícita. Não se emitiu novo veredito científico.

## Contrato e congelamento

Identidade: chatgpt-codex/ordem-018/derivacoes. Protocolo congelado em 2026-10-06T01:36:59.749288+00:00; registro MCP pré-execução seq413 confirmado com ok:true antes de chamar --run. Recibo preservado em P45_REGISTRO_PREEXEC.json. A execução iniciada em 2026-10-06T01:37:29Z verificou todos os pins.

- Protocolo: SHA-256 82735adee1484b72df5980224fb19d4d7284abb47dad84336374e266c3c7c4ca.
- Código P45: SHA-256 ac3d6b356909eaf881aabdbc65f7c31b3b32a6157894c166424902d88be3a6cd.
- Resultado: SHA-256 0dc829c19e6137dd5b417069e52ad3331937dca63b7bd23106bddf37ae59831e.

Os alvos já eram conhecidos; esta é reprodução histórica autorizada, não um teste cego nem uma nova escolha de lei. Beta fixo foi calculado em runtime como ALPHA_FINE_CODATA_2018 × sqrt(e). O ramo beta livre reproduz o diagnóstico histórico separado; não substitui a lei fixa.

| Configuração | Blocos | Tratamento da escada |
|---|---|---|
| P/F4 D1b | Planck comprimido + DESI DR2 + SH0ES gaussiano | H0 K* versus 73,04 ± 1,04, conforme entrada histórica |
| P/F5 sombra | Planck comprimido + DESI DR2 + Pantheon+SH0ES | 77 calibradores internos; DM/K*; um M perfilado |
| P/F5 acumulada | Mesmos blocos de P/F5 | 77 calibradores internos; integral 1/(E A); um M perfilado |

Não há SH0ES escalar adicional em P/F5. CC está fora das três configurações. Ambas as famílias P contêm escada; nenhuma delas é o ramo de fundo sem escada reproduzido na unidade T/F4.

## Fontes e covariâncias

Planck usa a matriz completa 3×3 de Chen2019 congelada nas entradas. DESI DR2 usa o arquivo médio e sua covariância completa 13×13, na ordem arquivada. Pantheon usa as mesmas cópias públicas previamente verificadas pela coordenação; 1701 linhas, seleção histórica (zHD>0,01) OU calibrador, 1657 selecionadas = 1580 cosmológicas + 77 calibradoras. A submatriz STAT+SYS completa 1657×1657 preserva correlações entre calibradores e demais SN.

A assimetria máxima antes de C←(C+Cᵀ)/2 foi 3e-08; essa simetrização pertence ao contrato histórico. Não foi introduzida aproximação diagonal. A covariância cruzada entre Planck, BAO e SN/escada não foi fornecida: a fatoração em blocos é [INPUT] do contrato histórico, não uma independência demonstrada nesta reprodução.

Com r=m_b−mu, Cholesky C=LLᵀ, y=L⁻¹r e u=L⁻¹1, usamos Mhat=(uᵀy)/(uᵀu) e chi2=||y−Mhat u||². Isso evita uma inversa explícita e a subtração de dois grandes quadráticos, preservando o mesmo perfil analítico. Nos calibradores mu=CEPH_DIST; nas demais SN mu=5log10[(1+zHEL)DM(zHD)]+25.

Arquivos de origem, hashes, seleção, matrizes e suporte constam em P45_PROTOCOLO.json, P45_ALVOS_HISTORICOS.json e ENTRADAS_HISTORICAS_E_COVARIANCIAS.json. Os JSONs históricos F4/F5 foram relidos para extrair os alvos sem digitação. O hash integral do motor realmente executado na ocasião não está nos resultados antigos; backups e contratos dão linhagem, não certificam a identidade completa daquele processo.

## Verificação antes dos ajustes e integradores

Oito pontos arquivados foram avaliados antes de qualquer ajuste P45: dois de P/F4 e seis de P/F5. Nos pontos SN fixos, a maior diferença em chi2 foi 5.40407654626e-07 e em M foi 4.79769113326e-10 mag. O ponto LCDM de F4 não traz theta integral no arquivo; a comparação desse modelo usa H0 e mínimos/decomposições arquivados.

Gauss–Legendre64 e128 concordaram nos resíduos branqueados até 1.42108547152e-13; nos mínimos, a maior diferença de chi2 foi 9.09494701773e-13. O integrador independente é uma alternativa explícita ao Simpson cumulativo20001 com interpolação do histórico. Não se atribui a diferença residual entre arquivos a uma única causa não medida. A máscara da tabela CAMB, E(z), as leituras de distância e os parâmetros físicos foram preservados.

O recibo T4 validou anteriormente a interpolação Lagrange de seis nós da tabela CAMB e seus400 pontos internos. Aqui se reutilizaram seu código independente, tabela e recibo por hash, sem repetir essa validação ou os ajustes T4. A reprodução SN-only da coordenação também foi lida como recibo, sem rerodá-la. Todos os redshifts cosmológicos SN ficaram abaixo de z*; portanto o ramo histórico A=1 acima de z* não é acionado.

## Ajustes e diferenças

| Configuração / modelo | chi2 reproduzido | diferença para arquivo | H0 | Mhat (mag) |
|---|---:|---:|---:|---:|
| P4_d1b / lcdm | 31.627025385145 | -6.48858e-09 | 68.8825681645 | — |
| P4_d1b / tgl | 15.575723761419 | +3.17723e-08 | 68.4297725960 | — |
| P4_d1b / livre | 14.293354384711 | +2.31352e-08 | 68.5310641039 | — |
| P5_sombra / lcdm | 1496.976730889112 | -3.3256e-07 | 68.8512179973 | -19.395652147593 |
| P5_sombra / tgl | 1469.307514877423 | -4.96068e-07 | 68.3930901692 | -19.236150833578 |
| P5_sombra / livre | 1469.166315988719 | -4.85119e-07 | 68.4231756723 | -19.246768597691 |
| P5_acumulada / lcdm | 1496.976730889112 | -3.3256e-07 | 68.8512179973 | -19.395652147593 |
| P5_acumulada / tgl | 1469.886746899237 | -5.00421e-07 | 68.3848982018 | -19.237282338211 |
| P5_acumulada / livre | 1469.725799770107 | -4.88516e-07 | 68.4178074968 | -19.248592478325 |

Máximos absolutos sobre os mínimos: Δchi2 total 5.00420583194e-07; por bloco 5.97905053468e-07; ΔH0 1.12739229507e-07; Δωb/Δωc 2.23936938437e-10; Δbeta 2.8023484748e-10; ΔM 1.98478034008e-09. As diferenças assinadas de cada theta, bloco, K e M estão no JSON, não arredondadas por esta tabela.

| Configuração | beta livre | sigma_beta (JᵀJ) | z_delta histórico reproduzido | raiz assinada de Δchi2 |
|---|---:|---:|---:|---:|
| P4_d1b | 0.009527630164 | 0.002226662168 | -1.124405073 | 4.006407571 |
| P5_sombra | 0.011231684740 | 0.002127775596 | -0.375798868 | 5.260153611 |
| P5_acumulada | 0.011173312466 | 0.002138724114 | -0.401168121 | 5.204803934 |

Esses diagnósticos são reproduções das definições arquivadas. A raiz assinada de Δchi2 no ajuste conjunto com a escada não é uma previsão de H0 sem escada; tampouco é uma evidência bayesiana. As famílias compartilham dados e não devem ser somadas como réplicas independentes.

O ajuste preservou escalas e Jacobiano central do histórico, TRF com xtol/ftol/gtol=1e−12 e máximo200 avaliações por modelo. Os otimizadores concluíram por seus critérios de parada, sem limites declarados ativos. Isso não é uma prova de mínimo global: foram reproduzidos os mesmos pontos de partida e a sequência LCDM→TGL/livre. O JSON preserva mensagem de parada, condição do Jacobiano, optimality, covariância JᵀJ e nfev. As incertezas não receberam reescala por chi2/gl.

## Custo e alcance

Execução local: 3.181673 s de parede; 3.031250 s de CPU; pico 173989888 bytes (165.930 MiB);540 avaliações de likelihood contando derivadas e controles; uma thread; sem GPU. O orçamento era600s/512MiB. Ambiente: Python 3.14.3, NumPy2.4.3, SciPy1.18.0; executável e plataforma completos no recibo.

As tolerâncias foram chi2 total/bloco0,01; residual de quadratura1e−7; H0 0,001; densidades1e−6; beta1e−5; sigma_beta1% relativo; diagnósticos z0,02; M1e−5mag. São tolerâncias de reprodução numérica, não critérios de confirmação física. Não houve instabilidade ou recusa nesta execução.

Nenhum original foi executado/importado ou alterado; nenhum novo catálogo, provedor remoto, evidência, MonteCarlo ou composto F9 foi utilizado. As bounds/priores históricos largos e a máscara menor da tabela estão explícitos; não se calculou nem renormalizou evidência. O próximo passo autorizado pela coordenação será dimensionar um piloto de custo de evidências antes de qualquer lote; esta entrega termina nos ajustes determinísticos.

[REAL] Artefatos locais e números medidos. [INPUT] Contratos históricos de leitura e fatoração. Não se move gate nem se transforma NOT_FALSIFIED em CONFIRMED.
