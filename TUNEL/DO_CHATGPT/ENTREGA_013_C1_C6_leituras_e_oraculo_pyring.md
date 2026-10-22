[REAL — controle de implementação e custódia; DERIVED/INPUT/CONJECTURE nas leituras físicas; NÃO-CEGO]

# Ordem 013 — C1 completa e oráculo original do pyRing

UTC: 2026-09-22T03:28:09.205354+00:00. Axiomas: N/A — sem Lean novo.

## Critérios, um a um

- **PAGO — C1 documental:** dez leituras, nove âncoras, dezoito linhas numéricas e dez verificações de unidade. `C1_LEITURAS.json/.md` reúne operador, relógio/estatuto, FP-5, fonte/novidade, universalidade e dependência em distância. Conferidos hashes e textos das âncoras. A escolha e a relação com as falas do operador permanecem `null`.
- **PAGO — implementação gaussiana de C6:** executado pyRing 2.7.0 original, compilado somente em cache. Fonte likelihood.pyx instalada idêntica à distribuição pública. Nove casos Toeplitz, seis vetores de ruído fora do evento e 270 integrais. Erro máximo em log-evidência: 7.09974301571e-11; em log-densidade projetada: 1.830369456e-08. A omissão intencional do determinante produz diferença 2.46136609387, recusada.
- **PAGO — reprodução em pasta limpa:** todos os valores do novo oráculo coincidiram exatamente. Foi reutilizado o binário compilado e conferido; não chamar isso de nova compilação independente. O teste não leu novamente o strain do evento.
- **PAGO — pacote v2:** `cache/TGL_RINGDOWN_DELIVERY_v2.zip`, 10626560 bytes; 194 arquivos do manifesto verificados após extração nova. O v1 permanece intacto, inclusive seus resultados e reproduções.
- **NÃO PAGO — calibração científica C5:** continua reprovada conjuntamente nas duas famílias/duas amplitudes. O oráculo elimina uma suspeita aritmética específica; não elimina o viés do modelo de forma de onda.
- **PARCIAL — validação pelo posterior publicado:** a comparação pyRing continua com modos/priors/pré-processamento distintos; o release inspecionado não tem 10,5 tM. O oráculo verifica a implementação gaussiana, não a equivalência desses problemas inferenciais.
- **ABERTO — ponte física:** nenhuma partição, relógio ou desenrolamento foi escolhido. A realização KMS finita e as predições continuam condicionais; Kay-Wald/Milburn somente no escopo dos resumos efetivamente lidos.

## Aproveitamento

Foram reutilizados a matriz C1, os relógios da v369 congelada, a covariância e o ruído off-source de C5, o registro C6 e os quatro pacotes já reproduzidos. Não houve nova função em um.py, nova pedra Lean, nova PE de posterior ou repetição do catálogo. A instalação do pyRing usa o tarball público já existente e dependências somente sob cache/pyring_oracle.

Também foi conferida a suspeita de atribuição de remanescente: SEOBNRv4HM já usa a função SEOB correspondente; IMRPhenomXPHM já usa suas funções FinalMass2017/FinalSpin2017. Não há correção a fazer nessa atribuição, e ela não explica o viés.

## Próxima ação científica

C5: resolver o viés de recuperação da forma de onda. Os 4608 cálculos e sua reprodução já terminaram; nenhum grupo FULL_IMR passa as duas famílias e as duas amplitudes. Próxima ação científica: avaliar recuperação com formas IMR completas (rota b), em estudo não-cego separado, preservando o C6 e os critérios originais. Não repetir a grade QNM já reprovada nem ajustar critérios para obter aprovação.

Nenhum resultado de strain foi promovido: INCONCLUSIVE_SYSTEMATICS permanece. Não multiplicar os posteriores do mesmo evento nem tratar estes controles numéricos como observações. O objetivo continua ativo, sem reivindicação de precisão integral já alcançada.

## Reprodução

Descompactar o v2, executar `python verify_delivery.py`, entrar em `C1_C6_ADDENDUM` e executar `python -B reproduce.py --download` no ambiente científico da entrega. Para reutilizar a distribuição conferida: `--source-archive /path/to/pyRingGW-2.7.0.tar.gz`. A opção `--vendor-cache /path/to/vendor` registra explicitamente o reaproveitamento de binário.

O recibo separado `C7_C1_C6_REPLAY_VALIDATION.json` paga a pendência histórica `independent_directory_oracle_replay=PENDING` do recibo imutável do empacotamento. Não sobrescrever o histórico para esconder a sequência.

## Tentativas e memória

A primeira tentativa do gerador C1 falhou por pedir x à leitura coerente não exponencial; código anterior preservado e tipagem corrigida antes da entrega. Avisos do pyRing e a recusa inicial de acesso WSL estão no STATUS. STATUS, PROGRESSO e manifesto local recebem backup imediato dos bytes anteriores. Nenhuma memória canônica de outra casa foi tocada.

## Custódia

| Artefato | SHA-256 lido |
|---|---|
| `C1_LEITURAS.json` | `333a9d8b7d650affb21e63564a399fa3048e407de71f7b9d57ec4d2cd2e583b3` |
| `C1_LEITURAS.md` | `a640e0c9ab336dabf99b7f0bf6423abd4684f60942f3384395eac54028daf6be` |
| `complete_c1_contract.py` | `91d80e48f451fe92c7434f914582d066b3f9dd6440e9ee3dff6a97fcc78ed8aa` |
| `C6_PYRING_IMPLEMENTATION_ORACLE.json` | `bb75157f8f4edd4d3bda7e4607970d1ec77d04820c393c718b1ab9ede8a429aa` |
| `verify_pyring_likelihood.py` | `ca979eb8a0f20d69d679cedb9244d7ab7e0ff89a90ec32de2f014e02736a2a03` |
| `prepare_pyring_oracle.py` | `70986e5a16fcb3440db6879ce5c47ed62d4f9bd0b3810f8f11ad30a39345f8e0` |
| `package_reproduce_pyring_oracle.py` | `db315f1a4436f35573e4af2120f4b9bf1a39071d75882e73dda29f4ed1811acc` |
| `build_c1_c6_addendum.py` | `204be0777e17a46104de7ff5cb2522404c61583df9601ffb9d520d1d45287f26` |
| `C7_C1_C6_ADDENDUM.json` | `81045fa87271028d1e92af3a1cf64c6cd4590753a12da587fb2b96df19f62e3f` |
| `C7_C1_C6_ADDENDUM.md` | `5a9dd40b05480f784b3b325b5fb0d238f5ff067778f002d55702894950f1357e` |
| `C7_C1_C6_ADDENDUM_VALIDATION.json` | `c4488521944af97c8ebf9cef43d95b425c650f95f62cb900f1005013f6332c5b` |
| `C7_C1_C6_REPLAY_VALIDATION.json` | `dd4b6b113ab9df6a53888129eebe7d8756c9960314c7885000daf339c7d37613` |
| `cache/pyring_oracle/PREPARATION.json` | `c29a57a854957598ee748dab5ede93f910e546578a211065cd0e92a61f3c170c` |
| `cache/TGL_RINGDOWN_DELIVERY_v2.zip` | `3c1ae84211f81a46309c44f41035eeb926b31350336be22da4d16ca0953a0bbe` |
| `cache/MANIFESTO_DOWNLOADS.json` | `4320a6bd4ebfeb816a6a096d497650ad0ad3dc9d3df1d8a5121b31ea0a009a1f` |
