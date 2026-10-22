# E1 — plano independente, NÃO-CEGO

[INPUT/OPEN] Código preparado para calibração condicional nos posteriores existentes; nenhum ajuste executado na emissão deste plano. E0 selado foi comunicado pelo **agente principal**, não pelo operador. A atribuição histórica incorreta fica corrigida aqui, sem alterar originais. Axiomas N/A; teoremas 0.

## Decisão de método

Para cada linha original do posterior conjunto, calcular δ_L(Mf_det, χf, z) e u = dtau220 − δ_L. Conservar todas as linhas, o pareamento e as correlações; nenhuma mediana entra no lugar de uma amostra. Registrar covariância entre df, dtau, Mf, χf e z, além de cov(dtau, δ_L). β vem do módulo runtime pinado, como α_CODATA2018 × √e. Convenção E0: BCW nas leituras locais, exceto R-MOD com spline do QNM complexo arquivado, sem extrapolar/clipping. A interpretação ensemble permanece condicional; não fecha a ponte para uma realização clássica.

Estimador principal: KDE gaussiana 1D de u com **todas** as amostras, Scott h=std(u,ddof=1)·n^(−1/5). Binning linear + convolução FFT; passo ≤h/16, refinamentos h/32 e h/64, limite 131072 pontos. Controle por soma gaussiana direta em 17 quantis e em cada ponto efetivamente usado no ótimo; erro |Δlog p|≤0,002 por evento. Massa integrada deve diferir de 1 por ≤10⁻⁶. Verificar estacionariedade e Hessiana com derivadas da soma **direta**, sem depender da derivada interpolada. Nenhum thinning. n não é ESS: ESS/correlação serial desconhecidas; controles h×0,7/1/1,4 nas populações completas. Os recortes usam h nominal. Momentos gaussianos de u e WLS são diagnósticos separados.

**df é integrado**, junto aos demais parâmetros, na distribuição empírica conjunta. Não há corte em df nem avaliação em df=0. Logo, a referência denominada GR neste ajuste significa δtau=0 com df livre/marginalizado: não é o modelo GR conjunto (df=dtau=0), nem o lnB anterior da curva 220. R-GLOBAL conserva seu nome, mesmo quando idêntico numericamente à referência; não conta como evidência independente.

## Prior e estatuto da densidade

Reler Uniform(dtau220) e Uniform(domega220) no HDF5, como texto; parse AST somente de literais, jamais eval/unpickle/import de prior. Usar `priors/analytic/<campo>` e, nos dois casos sem declaração analítica, `config_file/config/prior-dict` ou `prior_dict`. Divergência/ausência de declaração, amostras fora dos limites, pesos não tratados ou campos ausentes abortam, sem reduzir silenciosamente 31/33.

Os limites **não são universais**: há intervalos dtau [−0,8;4] e [−0,8;2]. Sob prior fatorizado πτ=1/W, prior auxiliar comum e suporte global compatível, o integral restrito de likelihood é proporcional a W·p_u(c). Registrar Σlog W como constante; **não dividir por um suposto prior uniforme de u**, pois a transformação depende de η. As declarações marginais e o suporte dos draws não comprovam fatorização global, normalização do modelo restrito nem suporte sobre todo o prior auxiliar. Essas três lacunas ficam OPEN. O código publica escore de densidade condicional, sem lnB calibrado/likelihood populacional normalizada.

Suporte finito: para cada evento exigir c dentro da interseção empírica [τ_min−minδ, τ_max−maxδ] e do domínio numérico da KDE. O ótimo deve estar ≥3h dessas bordas; caso contrário NÃO PAGO. A interseção é **mais restrita que a união induzida** e pode recusar regiões válidas da densidade marginal: é uma guarda conservadora fail-closed, **não o prior exato**, nem prova do suporte global ou correção de viés de borda.

## Ajustes e cobertura

- c(σ)=c0+kσ, σ=std(dtau220,ddof=1) reobtido dos draws e conferido contra E0; mesmo covariável em todas as leituras. σ é endógeno ao posterior: este ajuste condicional não resolve errors-in-variables nem estima uma lei causal de viés.
- Variante **[INPUT]** c(ρ)=c∞+kρ·(40/ρ), ρ=SNR network matched-filter GWOSC do join congelado. Intercepto é extrapolação para ρ→∞. A parametrização não é única nem derivada. SNR network não substitui os dois limiares de seleção inspiral/pós-inspiral.
- Populações 31 e 33 separadas; recortes σ<0,15/0,20/0,25 (sobrepostos, diagnósticos escolhidos agora, não testes cegos) e corridas O1–O3/O4a/O4b. n<5 ou desenho degenerado → NÃO PAGO. Sem imputar SNR ou corrida.
- Todas as dez leituras registradas. Oito possuem δtau local calculável; R-RAIZ-COHERENT e R-PROP recebem OPEN com motivo, sem inventar δ=0. GR adicional como referência marginal. Nenhuma leitura escolhida por desempenho.
- Otimização com cinco inicializações, intercepto e slope sempre livres, parâmetros reescalados para estabilidade. Guardas de borda/curvatura/controle direto; falhas preservadas como células NÃO PAGO. Covariância é inversa da Hessiana local, **não posterior calibrado**. Multistart não prova máximo global.
- Reportar c0,k,cov e intervalo Wald local; z local de c0/SE apenas descritivo. **z físico contra GR/predição fica null**: sem função de seleção e calibração não é lícito converter diferença de escore entre leituras não aninhadas em sigma. Efeito quase constante degenera com intercepto livre. Offsets fixos: **PROIBIDA_COMO_TESTE**; o script não os ajusta.

## Pendências E1 que este cálculo não paga sozinho

Ordem `TUNEL/PARA_CHATGPT/ORDEM_013BIS_fechamento_e_ampliacao_dos_eventos_ate_5sigma.md:168–174`, protocolo `TUNEL/TUNEL_PROTOCOLO.md:47–63` (raiz Chatgpt).

| Pedido | Entrega projetada / limite |
|---|---|
| E1.1 | Fullsample 31/33, leituras, dois covariáveis, covariância local e recortes; ainda não executado |
| E1.2 | NÃO PAGO por este script: releitura integral dos três textos e seções/citações exige nota separada. Função α(hiperparâmetros) desconhecida |
| E1.3 | Reutilizar resultados auditados das duas variantes da injeção LVK; ponto único, não curva por SNR. RD não se converte em posterior livre220 |
| E1.4 | NÃO PAGO por este script: C2 sintético e C5 IMR são estimadores diferentes; comparação com N/erro deve vir ao lado, sem fundi-los nem nova campanha |
| E1.5 | Distâncias locais descritivas; separação física/calibrada continua OPEN |
| Gerência −0,061±0,068; +0,79±0,37 | Controle independente das medianas dos draws: σ=(q95−q05)/(2×1,6449), W=diag(σ⁻²), cov=(XᵀWX)⁻¹ sem reescala χ². Fonte primária de cálculo lida como texto: `C_piso_sistematico/s02_measure.py:177–180` e `s03_sinais_e_catalogo.py:20–27` nos insumos. Comparação explícita dos quatro números com JSON arquivado; ao lado mediana/std, média/std e momentos/KDE, sem usar medianas como primário |

## Custo, autorização e revisão

Metadados existentes somam 608.681 linhas nos 33 eventos (contagem documental, nenhum HDF relido durante o desenho). Estimativa **não medida**: 5–15 min, um processo/uma thread, memória estimada <0,5 GB. Sem PE, strain, waveform, novos posteriores ou simulações. Depois de três eventos, extrapolar custo da fase de predição: abortar se >495 s. Limite total 900 s com guardas nos loops; também respeitar validade da autorização e deadline Part B. Não prolongar automaticamente campanha que falhar. Registrar tempos wall/CPU, versões, hashes e falhas. O limite é cooperativo, não watchdog do sistema.

O agente principal autorizou dependência após E0 selado. Hash do JSON do portão foi conferido em disco, igual ao comunicado; consta no manifesto calculado por script. **Plano/código são oferecidos para revisão antes de executar.** Um recibo de autorização, a criar somente após essa oportunidade de revisão, deverá conter:

```json
{
  "status": "E0_SEALED_E1_AUTHORIZED",
  "approved_by_role": "principal_agent",
  "design_manifest_sha256": "HASH_CALCULADO_DO_MANIFESTO",
  "sealed_E0_path": "ORDEM_013_RINGDOWN/PORTAO_DA_AMPLIACAO_V1.json",
  "sealed_E0_sha256": "HASH_CONFERIDO_EM_DISCO",
  "expires_utc": "VALIDADE_LIMITADA_DENTRO_DA_PARTE_B"
}
```

Comando futuro (não executado na emissão): `wsl -- /opt/lal_env/bin/python -B '/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e1_nuisance/prepare_e1.py' --execute --authorization 'ORDEM_013_RINGDOWN/bis/e1_nuisance/AUTHORIZATION.json' --tag authorized_001`.

Saídas futuras: `runs/<tag>/NUISANCE_DIAGNOSTIC.json` e `RECEIPT.json`, ou `FAILED.json`. Publicação exclusiva/no-overwrite por hard link do temporário completo. Manifesto, módulo, QNM, metadados e fontes HDF conferidos antes/depois. Nenhum cache novo >25 MB previsto; arrays permanecem em RAM. Guardas fail-closed não usam assert. Execução científica e revisão por agente distinto ainda pendentes; análise estática não é validação numérica.

Correções da revisão do agente principal antes do manifesto: a grade contém `spins` na raiz **e** no modo220, com arrays iguais neste arquivo; o código usa agora explicitamente `modes/220/spins`, conferindo comprimentos. Deadline derivado de `hard_deadline_utc` do orçamento pinado e conferido também dentro dos loops. Distâncias `c0_GR/SE` e `c0_residual_L/SE` e comparação das três bandas KDE são descritivas; **não LR/Bayes factor**, z calibrado continua null. O recibo de autorização será emitido pelo agente principal após o manifesto; não cabe pedir autorização ao operador.

Arquivos desta preparação: `PLAN.md`, `prepare_e1.py`, `DESIGN_MANIFEST.json`, `STATIC_REVIEW.json`. Nenhum original editado. O manifesto registra SHA das fontes e do plano/código; o recibo estático registra SHA do manifesto. Sem atualização de memória ou entrega formal.
