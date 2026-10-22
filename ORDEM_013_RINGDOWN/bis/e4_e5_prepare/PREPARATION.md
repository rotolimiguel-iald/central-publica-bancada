# Preparação E4/E5 — somente documental, metadados e código

**[REAL] Preparação concluída; cálculos científicos novos não executados. [INPUT] Plano para o principal fixar antes do registro E2.**

A ordem foi relida nas seções E4/E5 e na sequência E0→E1→E2→E5/E4. O executável exige ativação expressa do principal, os hashes deste pacote dentro do registro E2 e a testemunha no túnel. Não foi criado registro nem autorização. A trava roda antes de scipy/h5py, leitura de valores HDF, previsão e mkdir. Execução anterior dos artefatos de referência é do agente principal autorizado, não atribuída ao humano.

## E4 preparado

Fisher analítico local do440, fonte INPUT fixa Mdet=68,1M☉, chi=0,68, z=0; quatro PSDs O4/O5/ET/CE, dez leituras, duas variantes físicas, dois perfis de frequência e duas rotas SNR. Derivada dH/d(delta_tau)=+.5*d*(1/zm²+1/zp²) em GR. Amplitude/fase marginalizadas. SNR é do **440 isolado**, sem conversão IMR/rede. A rota de rho igual por PSD compara formas; AMPLITUDE_FIXA_INPUT ancora A=rho440_O4_INPUT/||h||_O4 e transporta rho_PSD por ||h||_PSD/||h||_O4. A âncora é INPUT, não amplitude medida deGW250114.

N50=25/z² [INPUT E(Z)=5]; N90condicional=(5+1,2815515655446004)²/z², para Z gaussiano unilateral de variância conhecida1 e fontes idênticas independentes sem sistemáticas. Não são significância calibrada nem promessa de taxa física. Para efeito zero, ausente ou |delta|<1e−12, os alvos operacionais são null/OPEN; previsões sub-resolução não viram números astronômicos de eventos. Massa/spin livres permanecem degenerados no modo isolado.

O GW250114 já auditado fornece o produto livre com 40776 amostras pareadas. Preparados KDE residual 2D em três bandas e gaussiana 2D de momentos, para 220 e 440 separadamente. Faixa entre estimadores, ESS local, quantis, fração próxima da borda e massa KDE fora do prior serão reportadas; a faixa não é IC. Não há KDE4D novo, produto de marginais ou promoção a evidência. **lnB calibrado/global fica null:** razão unitária nos priors uniformes de deformação não fecha o contrato dos nuisances, seleção e suporte. O código entrega log-razões de densidade condicionais com seu nome exato.

As variantes só-220 e 220+440 aparecem nas previsões. Deformar440 é INPUT; nenhuma leitura é escolhida. O diagnóstico marginal220 conserva440 livre como nuisance: não equivale a recuperação com440 fixo. Não foi identificado no schema auditado um segundo produto da mesma fonte/configuração com440 fixo. Comparar outros32 eventos comGW250114 ou condicionar fatia do posterior livre não paga essa robustez. A comparação conjunta e o efeito fixo/livre permanecem OPEN.

R-PROP e R-RAIZ-COHERENT têm linhas OPEN sem um único amortecimento exponencial. R-GLOBAL tem efeito relativo zero por construção. R-MOD mantém o escopo KMS restrito, sem estado global Hartle–Hawking de Kerr.

## E4.4 metadados já executados

Snapshot GWOSC do E0, sem nova consulta de disponibilidade: {'start_utc': '2026-09-22T19:09:09.306847+00:00', 'end_utc': '2026-09-22T19:11:44.889815+00:00', 'atomic': False}. Tabela1 histórica TGR4 pp2–3 acrescenta GR O1–O3; PDF/texto conferidos campo a campo. Mescla declarada: propriedades GR antigas e versão GWOSC preferida do E0, não nova PE. Nenhum chi_eff usado como chi_f. Medianas/centrais seguem a convenção catalogal herdada; não são inspiral isolada nem dados independentes do strain.

| corrida | SNR≥12 | passa INPUT | falha conhecida | aguarda GR | prioridade elegível ≥30 |
|---|---:|---:|---:|---:|---:|
| O1 | 2 | 1 | 1 | 0 | 0 |
| O2 | 7 | 5 | 2 | 0 | 0 |
| O3a | 21 | 14 | 5 | 2 | 0 |
| O3b | 10 | 5 | 4 | 1 | 0 |
| O4a | 28 | 17 | 5 | 6 | 1 |
| O4b | 45 | 27 | 17 | 1 | 3 |
| O4c_discovery_only | 1 | 0 | 0 | 1 | 0 |
| O4_public_total | 74 | 44 | 22 | 8 | 4 |
| all_public_selected | 114 | 69 | 34 | 11 | 4 |

Listas nominais completas por corrida (JSON também inclui os cortes≥12/30/53/78/95):

- **O1, elegíveis:** GW150914.
- **O1, aguardando GR:** nenhum.
- **O2, elegíveis:** GW170104, GW170809, GW170814, GW170818, GW170823.
- **O2, aguardando GR:** nenhum.
- **O3a, elegíveis:** GW190408_181802, GW190412, GW190503_185404, GW190512_180714, GW190513_205428, GW190519_153544, GW190521, GW190521_074359, GW190602_175927, GW190630_185205, GW190706_222641, GW190828_063405, GW190910_112807, GW190915_235702.
- **O3a, aguardando GR:** GW190425, GW190620_030421.
- **O3b, elegíveis:** GW191109_010717, GW191222_033537, GW200129_065458, GW200224_222234, GW200311_115853.
- **O3b, aguardando GR:** GW200112_155838.
- **O4a, elegíveis:** GW230601_224134, GW230628_231200, GW230811_032116, GW230914_111401, GW230919_215712, GW230922_020344, GW230922_040658, GW230924_124453, GW230927_043729, GW230927_153832, GW231028_153006, GW231102_071736, GW231108_125142, GW231123_135430, GW231206_233134, GW231206_233901, GW231226_101520.
- **O4a, aguardando GR:** GW230606_065320, GW230728_083628, GW230814_230901, GW231231_154016, GW240104_164932, GW240105_151143.
- **O4b, elegíveis:** GW240511_031507, GW240513_183302, GW240514_121713, GW240515_005301, GW240615_113620, GW240615_160735, GW240621_195059, GW240705_053215, GW240716_034900, GW240919_061559, GW240920_073424, GW240920_124024, GW240923_204006, GW240930_035959, GW241006_015333, GW241102_144729, GW241111_111552, GW241127_061008, GW241129_021832, GW241130_034908, GW241210_060606, GW241225_082815, GW250104_015122, GW250109_010541, GW250114_082203, GW250118_170523, GW250119_025138.
- **O4b, aguardando GR:** GW241230_233618.
- **O4c_discovery_only, elegíveis:** nenhum com GR disponível.
- **O4c_discovery_only, aguardando GR:** GW250207_115645.
- **O4_public_total, elegíveis:** GW230601_224134, GW230628_231200, GW230811_032116, GW230914_111401, GW230919_215712, GW230922_020344, GW230922_040658, GW230924_124453, GW230927_043729, GW230927_153832, GW231028_153006, GW231102_071736, GW231108_125142, GW231123_135430, GW231206_233134, GW231206_233901, GW231226_101520, GW240511_031507, GW240513_183302, GW240514_121713, GW240515_005301, GW240615_113620, GW240615_160735, GW240621_195059, GW240705_053215, GW240716_034900, GW240919_061559, GW240920_073424, GW240920_124024, GW240923_204006, GW240930_035959, GW241006_015333, GW241102_144729, GW241111_111552, GW241127_061008, GW241129_021832, GW241130_034908, GW241210_060606, GW241225_082815, GW250104_015122, GW250109_010541, GW250114_082203, GW250118_170523, GW250119_025138.
- **O4_public_total, aguardando GR:** GW230606_065320, GW230728_083628, GW230814_230901, GW231231_154016, GW240104_164932, GW240105_151143, GW241230_233618, GW250207_115645.
- **all_public_selected, elegíveis:** GW150914, GW170104, GW170809, GW170814, GW170818, GW170823, GW190408_181802, GW190412, GW190503_185404, GW190512_180714, GW190513_205428, GW190519_153544, GW190521, GW190521_074359, GW190602_175927, GW190630_185205, GW190706_222641, GW190828_063405, GW190910_112807, GW190915_235702, GW191109_010717, GW191222_033537, GW200129_065458, GW200224_222234, GW200311_115853, GW230601_224134, GW230628_231200, GW230811_032116, GW230914_111401, GW230919_215712, GW230922_020344, GW230922_040658, GW230924_124453, GW230927_043729, GW230927_153832, GW231028_153006, GW231102_071736, GW231108_125142, GW231123_135430, GW231206_233134, GW231206_233901, GW231226_101520, GW240511_031507, GW240513_183302, GW240514_121713, GW240515_005301, GW240615_113620, GW240615_160735, GW240621_195059, GW240705_053215, GW240716_034900, GW240919_061559, GW240920_073424, GW240920_124024, GW240923_204006, GW240930_035959, GW241006_015333, GW241102_144729, GW241111_111552, GW241127_061008, GW241129_021832, GW241130_034908, GW241210_060606, GW241225_082815, GW250104_015122, GW250109_010541, GW250114_082203, GW250118_170523, GW250119_025138.
- **all_public_selected, aguardando GR:** GW190425, GW190620_030421, GW200112_155838, GW230606_065320, GW230728_083628, GW230814_230901, GW231231_154016, GW240104_164932, GW240105_151143, GW241230_233618, GW250207_115645.

GW250207_115645: candidato futuro de teste previsto pela ordem, SNR 68.91 no snapshot; GR ausente, elegibilidade null e cegueira não certificada. O4c é janela de um evento de descoberta, não censo completo. Não foi aberto posterior/strain de teste, e ausência no corpus39 não significa ausência universal de publicação.

## E5 preparado

O plano distingue fase browniana, fase Cauchy, soma coerente com ocupações Poisson, saltos temporais Poisson ainda não especificados e sinal determinístico. Cauchy não tem variância finita. Ocupações Poisson não são processo temporal de saltos. Ensemble delta_f=0 não fixa a dispersão do estimador numa realização.

Mantidos OPEN sigma_jit,rec (transferência por injeção na pipeline) e sigma_sys do canal delta_f (duas famílias GR). N físico continua cenário de limite inferior. C2/C5 e a única injeção LVK/RD são controles com seus próprios observáveis/janelas, não curva de transferência universal nem cobertura inferida de um ponto.

LRT sintético: v_i=sigma_i²+sigma_sys²+q, q≥0, mu livre nos dois modelos, nuloq=0. Limiar25 não vira5sigma sem calibração própria do nulo heterogêneo. A informação local em variância é 1/(2v_i²); 1/sigma_i⁴ vale no cenário sigma_sys=0, sem reponderar duas vezes o log likelihood. Todos os elegíveis entram, sem corte por largura;31/33/10/18 são somente cenários de calibração arquivados.

Preparada identidade de integração sobre todas as amostras, conservando as constantes W_i dos priors uniformes; não ajusta nuisance nem executa fit populacional. O limite pontual sigma_pop=0 não recebe largura arbitrária escondida. Seleção/normalização/suporte global permanecem OPEN: nunca chamar KDE ajustado de likelihood populacional hierárquica calibrada. Estatística secundária de outliers centrada, com a forma não centrada da ordem ao lado, foi proposta como INPUT para E2 fixar e calibrar separadamente.

## Custódia e próximos passos do principal

Fixar PLAN.json, INPUT_MANIFEST.json, SCHEMA.json e deterministic_e4_e5.py no campo e4_e5_preparation_pins do E2. Registrar nota testemunha no túnel; somente depois emitir ativação no formato descrito em PLAN.activation. O executor recusa pins divergentes e grava apenas runs/<id_novo> nesta pasta. Resultado e recibo registram wall e CPU de processo, com alcance do relógio explícito. Nenhum produtor, manifesto anterior, memória ou canônico foi alterado.

Verificação feita nesta etapa: parsing/compilação em memória sob optimize1, inspeção de imports/guardas, hashes reais dos arquivos, extração/junção documental. **Não há validação numérica do executável ainda**; pequenos controles determinísticos independentes das fórmulas e comparação com220 devem ser feitos pelo principal após ativação antes de interpretar saídas. As funções de inferência populacional são utilitários preparados, não tarefas acionadas pelo CLI deste pacote.

Hashes para registro:

- `PLAN.json`: `a54d1a9cc873e01e215f66a56a83d8d2f2a502d0bb8e101f3431fa19f76393ec`.
- `INPUT_MANIFEST.json`: `7eb692c2b1d488e94b4c6cb0c8d52661f79f1a891aefd7b1a64ac49f60b47e82`.
- `SCHEMA.json`: `5f638e82b0cd38192cfbd8e1f6de7119643f88bd545209aba33f01881f285521`.
- `deterministic_e4_e5.py`: `c5f8576c76a32f668580aac2386264e719ee8e1c425360d75c1551335063b694`.
