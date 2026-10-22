[REAL — implementação verificada e processo iniciado; OPEN — evidência científica ainda não concluída]

# ORDEM 013 — Integração não linear da fonte

Registro: 2026-09-22T04:56:01.697307+00:00.

**PAGO:** a likelihood direta das formas de onda agora integra sete coordenadas físicas
(massa total, razão de massas, dois spins, inclinação, fase orbital e deslocamento do pico),
com distância/polarização comuns integradas analiticamente. O pico usa a correção intrínseca
22 previamente demonstrada. Priors uniformes declarados, sem reutilizar o posterior do
próprio evento. O prior de distância continua inverso-Rayleigh, não uniforme em volume.

**PAGO:** entradas congeladas: três fontes × duas famílias de injeção × a=0/1 × O4/O5 ×
50 intervalos = 1200 conjuntos simulados. São os mesmos 50 intervalos reutilizados e
pareados; não são 1200 eventos independentes. Cada conjunto recebe duas hipóteses:
2400 componentes de likelihood, reconstruídas SEPARADAMENTE. A média usada pelo
integrador é um recurso de cálculo, nunca o produto dessas simulações.

**PAGO:** equivalência da implementação com a API anterior: erro máximo
1.1368683772161603e-13; identidade de reconstrução de evidência conferida por
quadratura independente: 6.6613381477509392e-16.

**NÃO PAGO:** convergência astrofísica, distribuição final de ln B, posterior contínuo de a,
viés/cobertura, demais SNR e leituras. A primeira família de recuperação, IMRPhenomXPHM,
está em execução. SEOBNRv4HM continua na matriz, mas sua integração ainda não foi iniciada.
256 pontos vivos, orçamento piloto de 24000 avaliações, semente 130522 e checkpoints.
Não executar outra cópia enquanto a sessão 79591 continuar viva.

## O alerta que o controle produziu

O controle analítico usa gaussianas em sete dimensões. A componente com menor evidência
ficou com ESS de [19.1910390504424, 21.65496872447128] e erros em ln Z de
[-0.6151549186382663, -0.7644486530485732]. Portanto, a etiqueta PASS do teste de consistência
ampla **não satisfaz a precisão pretendida**. A auditoria astrofísica exigirá ESS≥100,
peso máximo≤0,05, estabilidade ao dobrar a amostragem temporal e repetição independente
com mais pontos vivos; a convergência global sozinha não basta. Se necessário, a rodada
piloto poderá orientar balanceamento computacional, preservando os priors e reconstruindo
as integrais por componente. O erro medido não será escondido por médias.

## Comandos

No WSL, diretório `cache/source_evidence`:

```text
/opt/pycbc_env/bin/python -B source_evidence.py run
/opt/pycbc_env/bin/python -B analyze_source_evidence.py IMRPhenomXPHM_seed130522_nlive256
```

O primeiro comando já está rodando: NÃO duplicar. A auditoria só pode rodar quando existir
RESULT.json. `--resume` é reservado a processo comprovadamente interrompido e checkpoint
existente; um timeout de observação não demonstra interrupção.

O pacote dynesty3.1.0 e sua licença foram COPIADOS de instalação existente para `vendor`;
nenhuma instalação de /opt foi alterada. A interface foi conferida na documentação primária
<https://dynesty.readthedocs.io/en/latest/quickstart.html> e no código local. A documentação
adverte que poucos pontos vivos podem perder modos; isso é uma limitação relevante aqui.

Não houve leitura nova da janela do evento, alteração de C6, seleção física de relógio,
partição ou desenrolamento, alteração do um.py, kernel, Atlas ou gate. C6 preserva
INCONCLUSIVE_SYSTEMATICS. Axiomas: N/A — sem Lean.

## Custódia dos insumos e scripts

| arquivo relativo à bancada | SHA256 medido |
|---|---|
| `prepare_source_evidence.py` | `acad4b6fcdda52b6a5c9ff3b6c5b091a9329ae4115871cbf4d1536099ce488c1` |
| `record_source_evidence_start.py` | `64461f6aa5996248d6fb2a24c46fba7625934be903fe63e3c5cc4d601d13b6e0` |
| `cache/source_evidence/source_evidence.py` | `0590f8e15bd508e525d2911fc570615671fdcdbc328399f4d7d8cb05d9816f7a` |
| `cache/source_evidence/validate_source_evidence.py` | `e2e81c1891c8d6c6253cd987f2aec25b4c1d787b5188d2a2f8587436928f2379` |
| `cache/source_evidence/validate_nested_mixture.py` | `22b441da13b79f8ec36fe0cedc9a329a10e983b2aeac55bc8b9a9c7a3f767fb2` |
| `cache/source_evidence/analyze_source_evidence.py` | `6723ed2ff58e409c7b47ed54e91929291f1f4d68879a842d658e4b8340aab12c` |
| `cache/source_evidence/REGISTRATION.json` | `cfde6683725ae3613cca2f3b46f55b7fd3ca9b0aac4443e297bb72cc7d2b7e6e` |
| `cache/source_evidence/PROVENANCE.json` | `ba6b1f184d7b789a9752a0941722bf378a8d6a4282ad0b76370fec70efef245e` |
| `cache/source_evidence/INJECTIONS.json` | `98a62aac521938955ac90c7a8a19e884ffd2bfc468d9a436164bf26d48299631` |
| `cache/source_evidence/INJECTIONS.npz` | `27dfc5fa47342efbaab30d32d915a7f0afd151f1cbae493bc44a813112472265` |
| `cache/source_evidence/VALIDATION.json` | `88119eee23a569f8d4781611b85659765fa31cd819b776cfe328fc4ba50fa4c0` |
| `cache/source_evidence/NESTED_ORACLE.json` | `7c817552578819589fa364211434abb34b5307f8d1a28efeda39c1637f6e2586` |
| `cache/source_evidence/vendor/MANIFEST.json` | `862341565cd495341e3bfef5912c6da9145e17d2af94ffa3c9caf0f920a25b3f` |
