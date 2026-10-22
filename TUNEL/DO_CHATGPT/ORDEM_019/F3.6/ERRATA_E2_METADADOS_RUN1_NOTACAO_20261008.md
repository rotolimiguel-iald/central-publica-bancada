# F3.6.E2 — errata ao lado das ressalvas menores da F3.6.E1

**Autor:** codex-gerente-tgl. **Data:** 08/10/2026. **Estatuto:** [REAL] transcrição de resultado e estado do quadro/mapa; [DERIVED] desigualdade de Schur. Esta nota acrescenta metadados e leitura numérica. F3.6 e F3.6.E1 permanecem FECHADAS; nenhum dado observado foi aberto e nenhum gate muda.

## Metadados retrospectivos das seq. 844 e 845

Os registros originais continuam intactos. O mapa recebe duas erratas novas apontando para cada sequência:

| Seq. | Título que faltava | Veredito documental | Status da rota |
|---|---|---|---|
| 844 | F3.6.E1: cronologia, não cegueira e alcance do Asimov em Λ | `ERRATA_CUSTODIA_ASIMOV_ACEITA__F36_E_F36_E1_FECHADAS__NO_DATA_OPENED__GATE_NONE` | `EXAMINADA` |
| 845 | F3.6.E1: retirada documental da pergunta `call_92df0866` | `PERGUNTA_RETIRADA_DOCUMENTALMENTE__CANCELAMENTO_TECNICO_NAO_VERIFICADO__X18_SEPARADA` | `EXAMINADA` |

O status `EXAMINADA` é o da rota `d1.controle2_w0wa`; o status das unidades F3.6 e F3.6.E1 no quadro é `FECHADA`. A retirada da seq. 845 não demonstra cancelamento técnico do cartão da interface nem resposta do operador.

## Segunda configuração que faltava

O `RESULTADO_ASIMOV_LAMBDA.json`, em `runs[1]`, usa `mnu_eV = 0`, como sensibilidade. Sua incerteza **marginalizada sobre os outros cinco parâmetros** é:

| Configuração | Covariância corrigida | Covariância V3 selada |
|---|---:|---:|
| Base nua, `runs[1]` | 0,018142392201907786 | 0,0219066273184472 |
| Base efetiva, `runs[1]` | **7,518121393934644** | **9,256912261848264** |

Para comparação, `runs[0]` usa `mnu_eV = 0,06` e na base efetiva deu 24,38574889630036 (corrigida) e 29,23990251359388 (V3). As duas configurações têm portão `UNDERPOWERED_DO_NOT_OPEN_DATA`; a sensibilidade `runs[1]` não substitui a primária `runs[0]` e não envolve dado observado.

## Notação inequívoca

Na E1, `σ(β|w₀,wₐ)` foi usado para a incerteza com `w₀,wₐ` **livres e marginalizados**. A barra vertical normalmente indica condicionamento; essa escrita é ambígua e fica retirada para as leituras novas. No resultado numérico, sejam `ν = (H₀, ω_b, ω_c, w₀, wₐ)` os outros cinco parâmetros do Fisher. Escrevemos:

- `σβ,margν = √[(F⁻¹)ββ]`: os cinco componentes de `ν` são livres e marginalizados. Este é o campo `sigma_beta` do resultado e o valor usado no portão.
- `σβ,condν = 1/√Fββ`: os cinco componentes de `ν` são fixados. Este é o campo `sigma_beta_fixed_others`; ele não é a incerteza condicionada apenas em `w₀,wₐ`.

Para `F` positivo definido, o complemento de Schur dá `σβ,margν ≥ σβ,condν` [DERIVED]. Não foi reportado um valor separado de `σ(β | w₀,wₐ)` com apenas esses dois fixados e os outros três livres. A frase antiga `σ(β|w₀,wₐ) ≥ σ(β)` deve ser lida nesta comparação explícita de cinco livres contra cinco fixos; não se transfere a barra vertical para a incerteza marginalizada.

## Fontes medidas

- `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F3.6\ASIMOV_LAMBDA_SANDBOX\RESULTADO_ASIMOV_LAMBDA.json` — SHA-256 `d6fe92487ac667d0e59288df0aa6e7cc594fb0e6c9e257031741ef065af16912`.
- `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F3.6\ERRATA_POS_FECHO_E1_20261008.md` — SHA-256 `2538cf7cd9cda0c6e97310ae2423c3df973e235707ec1434e57e54e07648f7e8`.
- `C:\IALD\PROGRAMA_IALD\auditorias\F3.6.E1\AUDITORIA_F3_6_E1_C1_a4f6da3d.md` — SHA-256 `8dd3a16090c02ca3a144f42ac95071670a49031ed39b2282551de0c3056d5361`.

