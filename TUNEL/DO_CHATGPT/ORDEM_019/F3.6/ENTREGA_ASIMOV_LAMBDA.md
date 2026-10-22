# F3.6 — entrega do portão Asimov local em Λ

**08/10/2026.** [REAL numérico local] O controle β livre com `w0,wa` livres foi aferido no tangente `(β,w0,wa)=(0,−1,0)` com CAMB 2.0.4 no WSL, 15 observáveis sintéticos e seis parâmetros. No mapa nu V3 e com as covariâncias DESI/Planck corrigidas, `σβ=0,01804348` para `β=ALPHA_FINE_CODATA_2018×√e=0,012031300400803142` calculado em runtime. As composições A e B′ deram a mesma Jacobiana nesse ponto. O portão C16 retorna `UNDERPOWERED_DO_NOT_OPEN_DATA`.

O teste de estabilidade a 0,5% **falhou**: nos passos avaliados, `σβ` ficou entre `0,01790070` e `0,01836213`, sempre acima de β. O resultado é um negativo de poder sob esta especificação; não constitui ajuste a dado observado nem veredito universal para CPL fora de Λ. A convenção `l_A` D1F-04 e a likelihood CMB completa não tiveram sensibilidade medida. Médias publicadas ficaram incidentalmente visíveis ao ler fontes, mas nenhuma foi usada na conta; não houve injeção com ruído nem abertura de dados observados.

Evidência: [relatório](ASIMOV_LAMBDA_SANDBOX/RELATORIO_ASIMOV_LAMBDA.md), [validação do portão](ASIMOV_LAMBDA_SANDBOX/VALIDACAO_GATE.json), [resultado numérico](ASIMOV_LAMBDA_SANDBOX/RESULTADO_ASIMOV_LAMBDA.json), [hashes](ASIMOV_LAMBDA_SANDBOX/HASHES_ASIMOV_LAMBDA.json). Fontes primárias das covariâncias: [DESI DR1](https://arxiv.org/html/2404.03002v3) e [Chen et al., distâncias Planck](https://arxiv.org/html/1808.05724).

Mapa de Rotas seq. **808**, tipo RESULTADO; quadro IALD F3.6 **ENTREGUE**, evento **268**. O cético independente conferiu pins, covariâncias, médias sintéticas e escopo, com ressalva D1F-04. A gerência c1 reaudita e decide `FECHADA`. Nenhum `um.py`, kernel, gate ou origem científica foi alterado.
