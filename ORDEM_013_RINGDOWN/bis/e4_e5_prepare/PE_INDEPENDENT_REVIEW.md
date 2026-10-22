# Revisão independente PE — fotografia antes de E2

[REAL — inspeção e fixtures finitas; OPEN — PE física e calibração]

**Parecer: não liberar calibração de duas famílias com o desenho XPHM desta fotografia.** Há dois bloqueantes específicos, PE-R1/R2, e uma pendência de instrumentação de custo PE-R3. Não encontrei falha de aprovação indevida por maxcall no adaptador testado. Isto não aprova E2, PE física, janela de8s ou convergência do piloto real.

Ownership respeitado: somente este parecer e `pe_review_001/`. Nenhum módulo produtor, registro, manifesto de produção ou preparação E4/E5 foi modificado. Execução autorizada: toy analítico 2D e mocks; zero waveform física, PE física, leitura de strain, posterior real novo ou seed cega. Pickles produzidos automaticamente pelo Bilby no toy foram preservados e não abertos.

## Bloqueantes e correções exatas antes da calibração

### PE-R1 — P1, suporte temporal desigual na injeção XPHM

`injection_design.py:10–22,55–62` na fotografia abaixo: `aligned_gr_xphm` verifica finitude/shape/energia, mas não duração de inspiral, merger e cauda no intervalo não atenuado. O contrato `analysis_time_contract` só é fornecido à família pSEOB. Verificar que o instante de chegada está dentro da janela não comprova que a forma inteira está nela.

[REAL — mock] Com início100, duração8, rolloff0,2 e chegada100,3, a duração finita simulada de inspiral1+merger0,1 não cabe. O pSEOB recusa; XPHM aceita os mesmos dados finitos do adaptador. Não foi medida truncagem em waveform física: foi demonstrada ausência da guarda no caminho XPHM. A nova proteção contra o evento real, também testada, não fecha essa lacuna.

**Correção:** usar um contrato temporal comum a ambas as famílias, com limites adequados à família e reserva por atraso de detector; verificá-lo antes de gerar/injetar. Se o domínio registrado não couber, abortar e ampliar a configuração por alteração testemunhada; nunca recusar propostas como se isso fosse prior científico, nem normalizar SNR de sinal temporalmente cortado sem declarar. Acrescentar negativos XPHM para início/cauda fora do suporte e positivo dentro. Bloqueia a calibração XPHM e, portanto, o fechamento de duas famílias; não demonstra defeito no adaptador de convergência do piloto pSEOB.

### PE-R2 — P2, verdade injetada fora do prior de recuperação aceita

`injection_design.py:35–39,69–72`: desvios são checados apenas contra−1; só a distância reescalada é confrontada com o prior da recuperação. Massa, spins, tempo, ângulos, limites superiores/inferiores dos desvios e mass_ratio não recebem verificação de suporte registrada.

[REAL — mock] Uma injeção XPHM com `mass_1=1` foi aceita sob prior de recuperação `mass_1∈[15,100]`. O mock também evidencia que não se confere a ordenação/mass_ratio. Nenhuma injeção física fora de suporte foi executada.

**Correção:** validar o vetor físico/deformacional inteiro contra os priors e constraints de recuperação, inclusive depois do reescalonamento de distância, antes de gerar sinal. Para testes intencionais fora de suporte, exigir finalidade/célula distinta no registro e impedir seu uso como calibração de viés/cobertura da população-alvo. A injeção deve permanecer dentro do prior temporal realocado para seu segmento off-source, não herdar o prior GPS do piloto. Bloqueia o uso das células não verificadas para calibração ordinária.

### PE-R3 — P2, instrumentação pendente para custo e chamadas reais

`pe_runner.py:198–206` e `pseob_source.py:69–78`: há `sampler_ncall` e contador das chamadas efetivamente encaminhadas ao gerador Bilby/LAL; não há contador próprio de invocações reais da likelihood. A checagem `ncall_reported==ncall` compara dois valores internos do sampler, não uma contagem independente.

| toy independente, rwalk/2 workers | ncall sampler | invocações reais likelihood | após construir sampler | excesso real−reportado |
|---|---:|---:|---:|---:|
| converged | 1369 | 1535 | 101 | 166 |
| maxcall | 72 | 237 | 101 | 165 |

O caso maxcall70 parou com ncall72 e foi corretamente recusado. Portanto o achado **não** é convergência falsa. O limite nominal do Dynesty já é declarado como tal no código. A diferença real inclui inicialização e trabalho fora da contabilidade interna; não atribuo todos os excedentes a uma única causa. Outro mock confirma que erro na guarda temporal anterior ao gerador não incrementa `source_calls`.

**Correção:** acrescentar contador compartilhado para a fronteira real da likelihood (sem contar duas vezes wrappers aninhados), conservando sampler_ncall e chamadas do gerador como três grandezas diferentes. Registrar escopo por fase e recusas anteriores ao gerador. Rotular o custo hoje coletado antes da conversão de remanescente como custo até aquela fase; obter wall/CPU finais no recibo do runner/controlador. Não anunciar maxcall como teto global de likelihoods. Essa instrumentação bloqueia a afirmação de custo real por chamada/limite global e sua utilização na alocação; o teto de parede do controlador e a recusa por maxcall já têm escopos defensáveis.

## Controles que passaram e limites da conclusão

- **Convergência:** toy real do adaptador Bilby2.8.2/dynesty3.1.0, likelihood analítica2D, rwalk, walks5 e dois workers. Caso convergido: delta_logz≈0,393610<0,4, ESS≈106,146,79 amostras. Caso maxcall: delta≈13,5957, ESS≈5,977,4 amostras, recusado. Captura ocorre antes da adição dos live points. Não há repetição em lotes de checkpoint porque o caminho sem checkpoint é sobrescrito e `check_point=False`. Cadência de update de bounds não é critério de convergência física. O toy não certifica24 workers,15 dimensões, ESS100 em PE física nem ausência de modos perdidos.
- **Colunas e priors:** draft002 passa o validador; fixtures recusam fixação individual das11 colunas físicas e dos quatro desvios. `mass_ratio` é Constraint derivada. Pares e ordem são preservados; NaN físico recusa saída. Os spins são dois componentes alinhados livres, não um modelo precessante com seis componentes. Priors largos INPUT não reproduzem todos os priors do pSEOBNRv5PHM publicado.
- **Launcher/privacidade:** revisão de `run_controlled` e mocks independentes de `validate_launch` confirmam exigência de grupo/sessão, identidade do pai, config pinada e stdout/stderr com o mesmo inode regular de PRIVATE.log; TTY/inode errado/sessão errada recusados. Cleanup do grupo é procurado mesmo se o líder saiu; escopo de SIGTERM/grace/KILL declarado. O teste de cleanup existente é mock, não prova hard-real-time do SO. Privacidade é procedural no mesmo host, sem alegação de ACL NTFS ou custodiante humano distinto. Nenhum seed real lido.
- **Epoch/rolloff/PSD:** o runner preserva epoch do HDF e exige sample-rate/start exatos; rolloff é atribuído antes de consumo pelo likelihood. A seleção PSD impõe fim≤min(event_GPS−exclusão,segment_start). Fixtures de arrays/HDF/Welch inteiramente falsos confirmam bloco anterior e recusa quando não cabe. A injeção nova também confere o GPS real ancorado e exclusão do evento, com duas negativas independentes. Isso não certifica a DQ/cadência dos HDF reais, que não abri, nem suporte físico completo da janela de8s. O pSEOB posterior acrescentou reserva geocêntrica0,022s; XPHM continua com PE-R1.
- **Tempo no source e cache:** o WaveformGenerator real com source puramente finito passou `geocent_time` e o contrato temporal; duas chamadas com mesmos parâmetros reutilizaram cache, mudança do tempo produziu nova chamada. Logo custo de source não equivale automaticamente ao de likelihood, e incluir tempo no source pode aumentar recomputações; registrar desempenho real futuro sem inferi-lo deste toy.

## Remnant conversion e alterações durante a revisão

A fotografia inicial tinha `remnant_conversion.py` separado e runner sem integração. Na fotografia final, o runner chama `derive` somente depois da aceitação de convergência, verifica três arrays finitos com o mesmo N e publica18 colunas pareadas (15 originais+Mf_det/af/z). O caminho cego conserva as14 colunas físicas/derivadas e desloca os quatro desvios. É integração estática conferida, não PE end-to-end executada.

[KNOWN — fonte primária] O ramo SEOBNRv4 da [implementação PESummary](https://lscsoft.docs.ligo.org/pesummary/latest/_modules/pesummary/gw/conversions/remnant.html) usa índices1 e2 para fração de massa e spin; seu helper multiplica a fração pela soma das massas. A conversão detector-frame proposta é compatível com esse contrato. A leitura foi desses trechos, não de toda a documentação. [REAL — mocks] Sete controles confirmaram multiplicação sem redshift extra, conservação de spin final negativo/ordem, recusa de N desigual, retorno LAL nãozero, fração>1 e H0 divergente da Planck18 nomeada. Não executei LAL remnant fit nem inversão cosmológica reais.

**Escopo obrigatório:** Mf/af são fit GR alinhado aplicado à amostra física; z usa distância e cosmologia externa INPUT. Não são medidas independentes de inspiral nem resultados de TGL. Spin negativo não deve ser cortado, absolutizado ou extrapolado silenciosamente pela etapa QNM. A fonte ECSV tem pin próprio e os parâmetros agora são comparados com a Planck18 carregada. O manifesto existente inclui arquivos Astropy; ao congelar, incluir/verificar também a origem ativa Astropy na guarda de runtime, como já se faz para os oito módulos principais. Não conferi aqui todos os4621 arquivos do runtime.

## Congelamento antes de E2 e estatutos

O draft002 é rascunho, não registro: seu mapa não contém o módulo remnant novo e ainda usa `extra_code_trees`, enquanto a interface exige `extra_code_roots`; faltam os campos de emissão/identidade que serão próprios do registro. A nova injeção requer `event_reference_GPS`; o gate de jobs cegos agora exige `data_quality_hold` e recibos de revisão/resolução. **Regenerar o documento completo e mapa recursivo depois de fechar alterações; não apenas mudar status do draft002.** Preservar testemunha/hash/cronologia e extra roots efetivamente usados. Isso é condição de congelamento, não alegação de que um registro já existente falhou.

Atualizar INTERFACE_V2:15 colunas/“remanescente OPEN não derivado” descrevem a versão anterior; a versão integrada tem18 e o estatuto condicional acima. OWNED_V3 e toy_adaptor002 continuam evidências históricas. As cinco funções PE testadas (`sampler_class`, `terminal_state`, `convergence`, `validate_config`, `posterior_columns`) são AST-idênticas entre snapshot inicial e final; por isso o controle do adaptador conserva alcance nessas funções, sem estendê-lo ao main alterado. Novos gates de revisão documental receberam10 verificações leves adicionais. O fetch e os nulos apareceram no inventário de hashes mas não foram reauditados nesta tarefa.

**Declarações permitidas:** plumbing finito testado; maxcall/baixo ESS não aceitos; fonte alinhada livre; controles de descritores e pins; remanescente/cosmologia condicionais. **Continuam OPEN:** adequação física da janela em todo prior; convergência/cobertura da PE real; igualdade com posterior publicado; duas famílias calibradas; seleção normalizada; transferência browniana e sigma_sys. Convergência numérica nunca paga esses gates.

## Fotografias e evidência reproduzível

Fotografia final usada para este parecer: `2026-09-22T20:48:03.825965+00:00`. Draft002 lido: `23bef3e5d4e74e254fe21dfd865482e1b85b20d7ab1f638112eb34de29150932`. Hash é dos bytes existentes, não de estado posterior. Mudanças após esta fotografia não são automaticamente aprovadas.

| módulo | SHA256 da fotografia final |
|---|---|
| blinding.py | `7d4407fde07c66929651b017501873ecd4bd69ca80fd3e6cd03eaf8e653c6bc5` |
| injection_design.py | `b0eeac213c2f8cef66e7ce237d69707ac7f29f6a43bb214552eb6baef6e8931b` |
| pe_runner.py | `d5b5030dd365679a738a4cde57eeb7fea3acc319af449bf13add3841ea30fb3b` |
| pseob_source.py | `21f619e45ae01883a9ee1c23a29f21e8cce9881545d1d6c9b367d530f24d17ef` |
| registration_guard.py | `7fbb74837d8d56b33690c09b0a6f0ca186ee8d1b1c948f5dec28825316f20133` |
| remnant_conversion.py | `87604de5c8fa7139cd6aa4d0c4fde09476105769735e44d476f3b9a55aa11bc1` |
| run_controlled.py | `7b5dd6484014942ee5fdd9fc3e529eaf05f9dffe463f35cdd10a01bdcf86334d` |
| strain_io.py | `a52faf32e88088320c57d303987a31ec2b9b59c93e162923d603c2c96b21a5b6` |

Recibos relativos a esta pasta de preparação:

- `pe_review_001/SNAPSHOT.json` — `691b0e4f3efcf54ecddaf76c10b61ba4343ac375e5a16ce94395a92029f09457`.
- `pe_review_001/CLOSING_SNAPSHOT.json` — `4e95754b811d30f240fadfa30d0df901f0de105731ecca62b56d87cc48385035`.
- `pe_review_001/FINITE_FIXTURES.json` — `3e0dd43266690f4a11a796a37e4fcb01513b09a490a2ea7d209daa7bf0dfb34b`.
- `pe_review_001/FINITE_FIXTURES_INJECTION_V2.json` — `a67b8feabed2c0f4d9833eb6d682e43e5c6ff0b9e5c41ef1de7bc90354b503c4`.
- `pe_review_001/REMNANT_MOCKS.json` — `792e84651448551fad35f2126ea25a672a5ec4f8eba1b6e53650eeee61e7182d`.
- `pe_review_001/CLOSING_DELTA_CHECKS.json` — `01bd86725c970a49701644aabd441f4786e6449761ae0520b9e626d84d88dae0`.
- `pe_review_001/toy_parallel/INDEPENDENT_TOY_RECEIPT.json` — `33896b9869e97e9735b3855485e80586c88ce3e6ebb46c0eba43c90f078f1551`.

Toy independente: 4.517358s de parede, apenas plumbing analítico. São30 controles iniciais,32 na rechecagem da injeção (30 repetidos para a nova versão, não62 achados distintos),7 mocks de remanescente e10 verificações da integração/gates. Scripts e snapshots completos estão ao lado. As execuções anteriores citadas são do agente principal autorizado; este parecer e estes controles são do revisor independente.


## Adendo independente de fechamento das seis fontes A — 2026-09-22T20:54:26.750908+00:00

**[REAL — fechamento documental e aritmético, sem novo runtime científico]** Os oito pins de fonte/INPUT e seis pins de novos arquivos de `PE_CLOSING_RECEIPT.json` conferem com os bytes encontrados. Este adendo prevalece sobre a fotografia anterior nos pontos explicitamente atualizados; não apaga os achados de integração da calibração.

**Fechados no escopo de preparação das seis fontes:** integração pareada de remanescente, Planck18 explicitamente INPUT, guarda de hold/revisão documental, reserva temporal de detector e atualização do custo de wall/CPU após a conversão. O runner agora tem SHA256 `588806474519f4da44328b42e0ea468aa291d088fa5f8bb183a38b4e8b5e07d1`. As cinco funções PE exercidas pelo toy independente permanecem AST-idênticas; não se alegou repetição do toy para o main novo. A diferença posterior acrescenta cronômetro próprio da conversão e atualiza wall/CPU finais antes da saída ao analista. Essa parte temporal de PE-R3 está fechada; contador de invocações reais da likelihood ainda não foi acrescentado.

**Janela:** recomputei somente contas a partir dos limites escalares já registrados por A. Em8s/start1420878135, margens `0.333285809` e `-0.382623672`s: falha. Em16s/start1420878129, margens `6.333285809` e `1.617376328`s: passa os16 registros de extremos fornecidos. São dois pares de massa (15,10)/(100,100), quatro pares de spins e dois tempos. Isso cobre os cantos retangulares admissíveis examinados, **não** o interior nem todos os vértices que surgem ao recortar o domínio pela constraint de mass_ratio. Não certifica suporte de waveform. O aborto por violação durante execução permanece obrigatório. A configuração16s deve entrar no draft003/registro antes da execução; não alterei o draft002.

**Remanescente:** a razão2 de massa e diferença0 de spin conferem aritmeticamente nos arrays de duas linhas já produzidos por A. O erro de inversão Planck18≈5,1587e−9 é resultado do executor escalar A, conferido em código/recibo; não foi recalculado aqui. Os sete mocks independentes anteriores continuam aplicáveis ao mesmo hash de `remnant_conversion.py`. Não chamar isso de validação em todo posterior, fit independente de inspiral ou cosmologia derivada da TGL.

**Permanecem separados e abertos antes da calibração de duas famílias:** PE-R1 (suporte temporal XPHM) e PE-R2 (verdade injetada versus todos os priors/constraints), no módulo do principal `injection_design.py`, que não pertence às seis fontes A. Seu hash permanece `b0eeac213c2f8cef66e7ce237d69707ac7f29f6a43bb214552eb6baef6e8931b`, igual ao das fixtures independentes. O adendo A não modifica esse caminho e não fecha esses dois achados. PE-R3, na parte de chamadas reais de likelihood, continua requisito para afirmar custo/chamada e teto global; `sampler_ncall`/`source_calls` mantêm as distinções medidas pelo toy. Não transformar esse ponto em alegação de falsa convergência: a recusa por maxcall passou.

**Disposição:** preparação das seis fontes A e complemento remnant/hold aceitos no alcance documental/finito descrito, com janela16s como INPUT a registrar e suporte interior OPEN. Não equivale a autorização de PE, ciência executada, calibração de duas famílias pronta ou registro E2 aprovado. O principal pode preparar/fixar o draft003 mantendo os bloqueantes de injeção visíveis e resolvendo-os antes das respectivas células de calibração. E4/E5 segue sem execução.

Nova fotografia e verificações: `pe_review_001/a_closing_snapshot/` e `pe_review_001/A_CLOSING_INDEPENDENT_RECEIPT.json`. Os bytes anteriores deste parecer foram preservados ao lado nas fixtures.
