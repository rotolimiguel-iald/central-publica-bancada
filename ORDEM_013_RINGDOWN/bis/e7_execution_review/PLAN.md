# E7 — verificação independente pós-extração (PREPARADA, NÃO EXECUTADA)

Só iniciar depois do GO explícito do principal, E6 aprovado e produtos E7 reais disponíveis. Até lá não ler HDF5, JSON extraído, amostras ou resultados E7. Não importar produtor/guard, não instalar dependências, não executar extração, ajuste, PE, waveform, MC ou strain.

## Recorte e limite

Uma execução WSL `/opt/lal_env/bin/python -B`, um processo e caps BLAS1 antes dos imports. Teto600s, limitado também ao menor deadline global/reserva final, deixando10s para recibo. Alarme POSIX interrompe a revisão e produz recusa visível. Não reiniciar janela nem tentar novamente para obter aprovação. Estimativa preparatória:1–5min, dominada pela leitura/hash dos arquivos; custo real desconhecido até execução e será registrado. Esta estimativa não é custo de PE.

O plano congelado contém33 eventos de calibração e608681 linhas; expectativa de3043405 comparações campo/linha. São contagens **de metadados**, a conferir na execução. Cinco campos pareados: df220, dtau220, Mfdet, af, z. Comparar **todos** com os campos nomeados nos HDF5 originais, na ordem original, igualdade exata após conversão float64. Conferir N, ausência de thinning, pesos iguais declarados, massa/frame, IDs, dataset, hash H5/tar e priors textuais sem eval. Recusar links externos/soft, datasets virtuais/externos. Hash H5 antes/depois; cada tar uma vez, sem extração.

Reobter médias, std ddof1 e covariância5×5 por fsum/duas passagens, independentemente do np.cov do produtor. Conferir pesos sigma^-2/sigma^-4, média ponderada e33 leave-one-out. Tolerâncias prévias: rtol3e−10, atol2e−12; beta rtol2e−15, atol0. Igualdade de transporte das amostras é exata, sem tolerância.

Conferir as20 células/10 leituras, AWAITING_DATA, gate vermelho, zero eventos de teste, lnB/z físico/correção física null. Conferir todos os IDs de resumos por leitura e OPEN de R-MOD (falta QNM exato pareado), R-PROP e R-RAIZ-COHERENT. Não repetir a campanha algorítmica congelada: predições condicionais/geometria já revisadas não serão recalculadas integralmente; divisão seedada será conferida como partição, sem novos draws. Esse limite constará do recibo.

**Densidade:** este E7 não calcula KDE nem densidade marginal. Verificar que densidades de prior, likelihood física e evidência permanecem OPEN/null. Não inventar teste de densidade nem declarar esse produto pago. A aprovação é de extração/transporte, aritmética descritiva especificada e estatuto da saída, sem significado físico.

## GO posterior, sem fabricá-lo nesta preparação

O principal fornece um JSON novo com status `GO_E7_REVIEW_AFTER_E6`, created_utc explícito, registration_sha256 e verifier_sha256 calculados. Em `inputs`, seis objetos (`e6_result`, `e6_review`, `authorization`, `execution_receipt`, `posterior`, `e7_result`), cada qual com `relative_to_Chatgpt` e `sha256` calculados dos produtos reais. É uma autorização operacional documentada, não autenticação criptográfica da pessoa. Pode ser materializado nesta pasta após a mensagem GO do principal; nenhum GO foi criado agora.

O verificador exige review E6 approved:true com hash do E6; autorização E7 posterior a E2 ligada ao mesmo E6/review/orçamento; recibo da execução bem-sucedida e hashes dos dois produtos; árvore produtora e plano registrados intactos. Prazo/GO/custódia precedem qualquer leitura de arrays.

Comando futuro (placeholders não executáveis até receber GO/pins):

```text
wsl.exe --exec /opt/lal_env/bin/python -B "/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e7_execution_review/verify_e7_execution.py" --go <GO_PATH_WSL> --go-sha256 <SHA_REAL>
```

Saída exclusiva `E7_EXECUTION_INDEPENDENT_REVIEW.json`: somente após todas as verificações emitir `approved:true` e `e7_result_sha256` efetivamente conferido, com custos/pins/escopo. Falha produz `approved:false`, erro explícito e preserva recibo; requer sucessor explícito, sem sobrescrita. Nenhum recibo de aprovação existe na preparação.

Arquivos desta preparação: script, PLAN.md, PREPARATION.json e PREPARATION_MANIFEST.json. A execução futura só grava o recibo próprio, não modifica fontes, outputs do principal, canônico, memória ou registros.
