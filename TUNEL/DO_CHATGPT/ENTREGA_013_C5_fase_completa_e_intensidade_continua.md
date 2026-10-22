[REAL — controles numéricos executados; OPEN — precisão da evidência e calibração da fonte]

# ORDEM 013 — fase inteira, auditoria e intensidade contínua

Registro: 2026-09-22T05:58:28.079650+00:00. N/A — sem Lean. Nenhuma edição no um.py/kernel/casas canônicas.

## Critérios desta etapa

- **PAGO:** o piloto de fase integral terminou (1024 propostas;843 dentro do prior). As181 externas têm integrando zero e contam no denominador. São1200 dados simulados, com50 intervalos de ruído por detector reutilizados entre células; não1200 observações independentes.
- **PAGO:** soma alternativa em precisão estendida, erro máximo 4.0856207306205761e-14; taxas8192→16384Hz nos35 pontos dominantes, mudança relevante máxima 0.016328971882330734, limite0,1. Esses testes verificam a implementação, não a suficiência das amostras.
- **NÃO PAGO:** precisão da evidência. ZERO/1200 comparações passou; ESS entre1.0012363 e14.35321, contra mínimo100. Não usar os lnB desse piloto como resultado físico aceito. Fase explícita não resolveu sozinha a exploração das demais coordenadas.
- **PAGO:** proposta computacional adaptada usando igualmente todos os2400 alvos.70% mistura ajustada,20% mistura anterior,10% prior inteiro. Priors físicos, likelihood e critérios inalterados. Nova integração com2048 propostas independentes: sessão38040, último registro1008/1656 avaliações internas. Conferir o handle; este documento não promete que continuará viva.
- **PAGO:** leitura contínua de a implementada e comparada à geração direta em480 controles (32 células; duas famílias, duas fontes, quatro leituras, O4/O5; a=-0,25;0;0,37;1;2). Erro relativo máximo da onda=2.1327560997955204e-07; logL=2.1337889847927727e-05. O controle negativo de a é extensão fenomenológica de diagnóstico, não gerador GKLS físico.
- **PAGO:** em a=0/1 a nova integral recupera a anterior, diferença máxima3.4106051316484809e-13.
- **NÃO PAGO:** repetição independente, precisão suficiente da fonte, recuperação SEOB integrada, demais SNR/leituras e viés/cobertura de a contínuo. Nenhum prior de a foi escolhido pelo simples teste da nova função.

## O que se integra

Na realização condicional inteira de harmônicos já usada, h_a = h_all + (exp(-a Γ_220 t)-1) h_22 + (exp(-a Γ_440 t)-1) h_44. Cada termo usa a mesma fonte, o pico intrínseco22 e distância/polarização comuns. O amortecimento ocorre ANTES do branqueamento pela covariância do detector. Demais harmônicos ficam como estavam; não é uma derivação da taxa de cada overtone.

A integral de fase é da **verossimilhança**, (1/2π)∫L(d|η,φ,a)dφ, não uma média da forma de onda. Marginalizar uma fase orbital desconhecida não é aplicar dephasing físico nem escolher um desenrolamento quântico. As duas ramificações orbitais e todos os harmônicos gerados continuam incluídos. A força contínua altera apenas a mesma lei de amortecimento explicitamente condicional.

## Reprodução e continuação

Scripts em `cache/source_evidence`, Python WSL `/opt/pycbc_env/bin/python -B`:

```text
audit_phase_source.py IMRPhenomXPHM_seed130801_N1024 --rate --processes 6
validate_continuous_phase.py
adapt_phase_source.py fit
adapt_phase_source.py run --draws 2048 --seed 130811 --processes 6
```

Comandos acima JÁ executados/iniciados. Arquivos create-once recusam sobrescrita; reproduzir numa cópia preservada ou usar nova semente/pasta quando aplicável. Não iniciar outra cópia da sessão38040. As sessões85465 (piloto),40076 (auditoria) e45570 (validação contínua) foram observadas terminais, código0. Após a nova rodada, conferir RESULT, somas, ESS, peso máximo e erro MC antes de interpretar lnB. C6 original permanece congelada. Nenhum número foi convertido em sigma, e nenhum gate foi movido.

## Custódia medida

| arquivo relativo à bancada | SHA256 |
|---|---|
| `cache/source_evidence/audit_phase_source.py` | `43f4c78aec69f141c7c2a1bd860ed728fcbfb32ece6a7d0327cb872a1d9418bb` |
| `cache/source_evidence/adapt_phase_source.py` | `8ffc29bd4fc48d4ba622db26f6f40822a7cc9ab0e1d7dda0c5daff56e0ae5cfb` |
| `cache/source_evidence/continuous_phase_source.py` | `fe6b60367fd66c7b4f11d84b6e5922f9c0e76f19777ff0bacb323ddd17d95bed` |
| `cache/source_evidence/validate_continuous_phase.py` | `8036ac3c0210621174a5526b6dc44dc28fa4801b00d9fc00d9977e047be8d762` |
| `cache/source_evidence/CONTINUOUS_PHASE_VALIDATION.json` | `d44a0a99b02b1bb152d9b99f6b5151b8de4084fc5a15cdb2ef1af3712057e3cc` |
| `cache/source_evidence/phase_runs/REGISTRATION.json` | `a47a203a5a794048d5d71f1e6b4db7f37b7187a5cea0cb8e1a8c51960275a3fc` |
| `cache/source_evidence/phase_runs/PROPOSAL.json` | `9e58d2b73d9f7c1c8f34dbd5367020fb2abf5f148bff0595732b366710557b7d` |
| `cache/source_evidence/phase_adapted_130801/ADAPTATION.json` | `4a8524918c38193580d51bee2629949d203da576f9fc3eddce0ea304c29d37f6` |
| `cache/source_evidence/phase_adapted_130801/PROPOSAL.json` | `1aea79fc4d34bd438a9372ad48cb7ec448ffb7f4d1304cfc38d90396414717b0` |
| `cache/source_evidence/phase_runs/IMRPhenomXPHM_seed130801_N1024/RESULT.json` | `5bb92343f7b8d44e9895515c47514d079a6291e3f18d5414c2e87dcfdf6780b5` |
| `cache/source_evidence/phase_runs/IMRPhenomXPHM_seed130801_N1024/RESULT_ARRAYS.npz` | `fde2b08494ac0bb663086d5b116581841786b67763719fae3f41fee94ffeb10d` |
| `cache/source_evidence/phase_runs/IMRPhenomXPHM_seed130801_N1024/PROPOSALS.npz` | `028029d0551a5b0a34eefd4fea6ab7fadaaf2f1dbb7b7ab26f077b8b20c925b7` |
| `cache/source_evidence/phase_runs/IMRPhenomXPHM_seed130801_N1024/AUDIT.json` | `70d0b45a5e271ac0bd77c2679d8ef0d117c7816a33aae6c6a2afcafdf9145f39` |
| `cache/source_evidence/phase_runs/IMRPhenomXPHM_seed130801_N1024/AUDIT_RATE.json` | `360c2e8ab157d0f01476719ec8216e519f15e6d0c8e36e81b602ad6cf331bf09` |
| `cache/source_evidence/phase_adapted_130801/IMRPhenomXPHM_seed130811_N2048/START.json` | `bd6f037680e1b3677c19b3c4f992f8fa069bb3cf0968cb390a61c766363c8d30` |
| `record_phase_source_progress.py` | `d9dfe36fd5a546d397dfe69bb276898c95353e3d57e5569b2012070f18c06846` |
