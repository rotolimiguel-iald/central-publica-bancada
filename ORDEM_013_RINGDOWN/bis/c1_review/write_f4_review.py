"""Finalize the independent review; read production, write review artifacts only."""
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    with path.open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()


def load(name):
    return json.loads((ROOT / name).read_bytes())


def write_new(path, raw):
    require(not path.exists(), 'Review output already exists')
    temp = path.with_name(path.name + '.tmp')
    with temp.open('xb') as handle:
        handle.write(raw)
    require(temp.read_bytes() == raw and len(raw) > 0, 'Review bytes differ')
    require(not path.exists(), 'Review output appeared')
    temp.rename(path)


def main():
    report = ROOT / 'bis/F4_POWER_GATE_REVIEW.md'
    supplement = ROOT / 'bis/c1_review/f4_final_integrity.json'
    require(not report.exists() and not supplement.exists(), 'Refuse overwrite')
    results = load('bis/c1_review/f4_independent_results.json')
    closing = load('bis/c1_review/closing_c1_results.json')
    gate = load('PORTAO_DO_PODER_013.json')
    empirical = load('C5_FISHER_EMPIRICAL.json')
    norm = load('bis/F4_GW250114_WINDOW_POWER_NORM.json')
    matches = {}
    for audit in (results, closing):
        for name, digest in audit['input_hashes'].items():
            path = ROOT / name
            matches[name] = sha(path) == digest
    require(all(matches.values()), 'Audited input changed before final review')
    opening = ROOT.parent / 'TUNEL/DO_CHATGPT/ENTREGA_013BIS_ABERTURA_operador.md'
    require(sha(opening) == gate['opening_sha256'], 'Opening provenance differs')
    controls = []
    for row in gate['measured_psd_control']:
        ref = next(p for p in empirical['records'] if p['psd'] == row['detector']
                   and p['reading'] == row['reading'] and p['snr_ringdown'] == 40
                   and p['scenario'] == 'MASS_SPIN_FIXED_OPTIMISTIC')
        expected = math.log1p(ref['x']) / ref['sigma_delta_local'] * norm['network_rho_estimate'] / 40
        require(math.isclose(expected, row['z_at_measured_rho'], rel_tol=1e-14, abs_tol=0), 'PSD transport differs')
        controls.append(dict(detector=row['detector'], reading=row['reading'], z=expected))
    require(load('C1_LEITURAS_v3.json')['rows'] == load('C1_LEITURAS_v4.json')['rows'], 'Frozen C1 rows changed')
    required = ['R-A', 'R-B', 'R-MOD', 'R-RAIZ-0', 'R-RAIZ-EP4', 'R-RAIZ-REST', 'R-LIN', 'R-GLOBAL', 'R-PROP', 'R-RAIZ-COHERENT']
    require({r['reading'] for r in gate['readings']} == set(required), 'Readings differ')
    require(all(r['power_gate'] == 'UNDERPOWERED' and r['physical_verdict'] == 'INCONCLUSIVE_SYSTEMATICS' for r in gate['readings']), 'Gate conclusion differs')
    meta = dict(utc=datetime.now(timezone.utc).isoformat(), input_hashes_match=matches,
                opening_hash_matches=True, frozen_C1_rows_match=True,
                measured_psd_arithmetic=controls, measured_psd_scope=empirical['PSD_scope'],
                closing_review_sha256=sha(ROOT/'bis/C1_CLOSING_REVIEW.md'),
                independent_results_sha256=sha(ROOT/'bis/c1_review/f4_independent_results.json'),
                script_sha256=sha(Path(__file__)))
    write_new(supplement, (json.dumps(meta, ensure_ascii=False, indent=2, allow_nan=False)+'\n').encode('utf-8'))
    stale_table = '\n'.join(f"| {r['psd']} | {r['stored_z']:.12g} | {r['corrected_log_z']:.12g} | {r['stored_mean']:.12g} | {r['corrected_mean']:.12g} |" for r in results['same_source_stale'])
    hash_files = ['PORTAO_DO_PODER_013.json', 'C5_FISHER_v2.json', 'refeito/measure_power_gate_013bis.py',
                  'refeito/measure_power_gate_013bis_v2.py', 'bis/F4_GW250114_WINDOW_POWER_NORM.json',
                  'bis/c1_review/f4_independent_checks.py', 'bis/c1_review/f4_independent_results.json',
                  'bis/c1_review/f4_final_integrity.json', 'bis/c1_review/write_f4_review.py']
    hashes = '\n'.join(f'| `{name}` | `{sha(ROOT/name)}` |' for name in hash_files)
    text = f'''[REAL — revisão independente dos cálculos arquivados; transporte e evidências condicionais; sem mudança de gate]

# Revisão adversarial leve de F4

Data UTC: {meta['utc']}. Raiz dos caminhos: `C:\\IALD\\Central de Patentes\\Chatgpt\\ORDEM_013_RINGDOWN`.

**Parecer: portão numérico corroborado no modelo declarado; C5_FISHER_v2 requer correção da tabela auxiliar antes de aprovação integral.** Há uma inconsistência concreta de convenção em `same_source_R_B` (P2, abaixo) e uma explicitação necessária no controle de PSD por detector. Nenhuma delas muda o resultado dos 50 registros do portão: todos ficam abaixo de 5; o maior z condicional é {results['max_fixed_z']:.12g}. Permanece `INCONCLUSIVE_SYSTEMATICS`, com `FAILED_TWO_FAMILY_CALIBRATION`. Não é aprovação de toda F4, da calibração física ou da ordem inteira.

C1 foi encerrado primeiro em `bis/C1_CLOSING_REVIEW.md`: controles positivos aceitos, dez mutações originais e quatro adicionais recusadas sob `-O`, divergência de bytes recusada antes de replace. Esta revisão F4 não reabre os achados C1 encerrados nem modifica produções.

## Controles independentes executados

Li os JSON, fontes dos dois builders e os insumos hasheados. Não executei builders, PE, injeções ou um.py. O script próprio `bis/c1_review/f4_independent_checks.py` reabriu apenas os segmentos necessários dos HDF5 e os whiteners; recalculou normas por einsum e soma compensada; refez Fisher com derivadas numéricas centrais de cinco pontos e projeção QR dos parâmetros nuisance; verificou transporte, momentos, limiar de N e todas as quadraturas livres.

[REAL] Conferem os 17 hashes de dependências do portão, a origem de Fisher e o hash da abertura no túnel. O vínculo com C1 v3 é uma dependência congelada legítima: suas dez linhas são iguais às de v4. O manifesto próprio inclui também o builder anterior e as quatro PSDs. Conferi novamente os insumos de C1 e F4 ao redigir este parecer: todos os hashes monitorados permanecem iguais.

| Controle | Resultado independente |
|---|---|
| Norma H1; índice inicial | 602,358607198691; 1299343; 407 graus de liberdade |
| Norma L1; índice inicial | 576,440162194493; 1299333; 407 graus de liberdade |
| Excesso de norma da rede | 364,798769393184 após subtrair 814 graus de liberdade |
| Estimativa rho da rede | {results['network_rho']:.15g}; erro-padrão aproximado {results['network_rho_se']:.12g} sob as hipóteses do recibo |
| Fisher | 384 registros; maior erro relativo de sigma {results['fisher_max_sigma_relative_error']:.6g} |
| Cobertura do portão | Cinco bases × dez leituras = 50; nenhuma omitida ou duplicada |
| Integral com amplitude livre | 48 registros; maior diferença absoluta de média {results['free_max_mean_error']:.6g}, de desvio-padrão {results['free_max_sd_error']:.6g} |

A janela é nominalmente 10 tM, com arredondamento documentado para a primeira amostra de 4096 Hz e retenção a 2048 Hz. rho vem de `sqrt(norm² − dof)`, com ruído gaussiano estacionário e covariância unitária após whitening. É estimativa de excesso de norma, não SNR medido por filtro casado nem significância de detecção. O erro aproximado não incorpora erro de PSD ou não estacionariedade. Essas restrições já aparecem no recibo e devem acompanhar seu uso.

## SNR, leituras e identificabilidade

[REAL] A versão v2 separa corretamente a referência GR (`a=0`) do SNR da injeção deformada (`a=1`) à mesma distância. As quatro referências GR, cruzadas com `C5_IMR_RECOVERY.json`, são:

| PSD / família | rho GR a 403 Mpc | fator rho/40 | z de R-B |
|---|---:|---:|---:|
| O4 / Phenom | 10,0659128940 | 0,251647822350 | 0,101718465559 |
| O4 / SEOB | 10,6535010891 | 0,266337527227 | 0,107656185288 |
| O5 / Phenom | 17,0551438969 | 0,426378597423 | 0,172218212596 |
| O5 / SEOB | 18,0652525512 | 0,451631313780 | 0,182418015542 |
| Norma GW250114 / referência O4 | 19,0997060028 | 0,477492650070 | 0,193007112985 |

Os SNR a=1 foram conferidos por leitura e família; os respectivos z à mesma distância também conferem. A tentativa anterior está preservada. Os trechos de cálculo da norma e de Fisher nos dois builders são idênticos; a nova rotina exige igualdade do JSON parseado antes de reutilizar os parciais. Isso verifica o mecanismo e os resultados atuais. A fonte, sozinha, não prova o log histórico da primeira execução nem identidade byte a byte entre serializações passadas.

[DERIVED, condicional] Fisher escala como rho² quando forma, PSD e parametrização são mantidas; sigma escala como 1/rho e z como rho. O código transporta uma **forma 220 de referência**, não recalcula a geometria de Fisher de cada IMR observado. `z_max_local` é separação otimista com massa/spin fixos nessa forma; não é cota superior rigorosa sobre toda família IMR ou sobre o sinal real. `UNDERPOWERED` tem precisamente esse alcance. O nome do campo não dispensa sua cláusula `scope`.

As dez leituras são R-A, R-B, R-MOD, R-RAIZ-0, R-RAIZ-EP4, R-RAIZ-REST, R-LIN, R-GLOBAL, R-PROP e R-RAIZ-COHERENT. Oito têm curvas Fisher; as duas últimas entram como equivalência numérica condicional, com `physical_exact_equality=false` no artefato Fisher. Seus zeros numéricos não viram identidade física universal nem nova taxa de decaimento. R-GLOBAL mantém a hipótese relacional distinta. A regra `abs(delta)<1e-6 → SUBRESOLUTION` foi respeitada: N não ganha precisão artificial nessas linhas.

[DERIVED, local] Para um único modo 220, o mapa `(log M, chi) → (log f, log tau)` tem determinante −Q'/Q. Em chi=0,68, medi −1,2188018444728255; a tangente de deformação do decaimento pertence ao espaço gerado por massa/spin, com resíduo numérico zero. Assim, o z identificável após liberar esses parâmetros é zero nesse modelo; `sigma=null` significa não identificável, nunca erro zero. Isto **não** demonstra degenerescência do IMR completo, de multimodos resolvidos ou de análise com informação externa sobre a fonte. O JSON faz essa distinção. O diagnóstico multimodo existente foi lido, não reexecutado; a limitação numérica SEOB continua aberta.

## Ponto fixo, amplitude livre e o valor aproximado 0,05

[DERIVED] No modelo escalar gaussiano, com x fixo e sigma local, `z=log1p(x)/sigma`; para a razão entre dois pontos fixos, as médias de lnB são ±z²/2 e o desvio-padrão é z. Isso não é uma evidência já marginalizada em amplitude ou fonte. Os 384 registros atualizados satisfazem essas identidades.

Para `a~Uniforme[0,1]`, reavaliei independentemente

`B(y) = integral_0^1 exp(y log(1+a*x)/sigma − log(1+a*x)^2/(2 sigma²)) da`.

Usei a primitiva analítica após `t=log(1+a*x)/sigma`, com diferenças estáveis de CDF normal, e integração adaptativa externa sobre o ruído em [−12,12]. É método diferente da quadratura Legendre/Hermite 64/128 do builder. As 48 linhas (quatro leituras apreciáveis, seis SNRs, duas amplitudes verdadeiras, O4 fixo) concordam nos erros da tabela. Não se estende essa cobertura a todas as PSDs ou a uma likelihood astrofísica.

| R-B, SNR 40, amplitude verdadeira a=1 | sigma | média lnB | desvio-padrão | lnB sem ruído |
|---|---:|---:|---:|---:|
| Fisher de referência atual | 0,0497391332454 | 0,0616331532411 | 0,205706742672 | 0,0548928707908 |
| Mesmo x, sigma aproximado da ordem | 0,058 | 0,0452830159450 | 0,175752237810 | 0,0403127433748 |

O “≈0,05” é compatível com a incerteza aproximada anteriormente citada; não é igualdade numérica com 0,06163. Tampouco se deve substituir média sobre ruído pelo valor sem ruído de 0,05489 apenas por estar mais próximo de 0,05. Para a=0, a integral atual dá média −0,0203296072199 e desvio-padrão 0,200283366308. O resultado pontual com a=1 é outro objeto: média 0,0816927002788 e desvio-padrão 0,404209599784.

Uniforme em tau_star produz a mesma integral apenas na lei quadrática com partição fixa, amplitude proporcional a tau_star e intervalo [0,tau_star_ref]. O JSON explicita isso. Não é prior independente, não estabelece limite observacional sem calibração e não autoriza a aproximação de Laplace fora de seu regime.

## Correções exatas pendentes

**F4-R1 — P2, bloqueante para declarar todo C5_FISHER_v2 consistente com a nova convenção.** Em `C5_FISHER_v2.json:9232`, `same_source_R_B` conserva z=x/sigma e momentos antigos, enquanto os registros usam log1p(x)/sigma. O builder atualiza `records` mas herda essa tabela sem marcador histórico. Correção em versão nova: preservar a tabela antiga explicitamente como histórica; acrescentar tabela logarítmica recalculada da linha R-B, SNR40, `FREQUENCY_FREE_TAU_GR_FIXED`, multiplicando pelo `snr_ratio_to_O4` da própria linha. Usar média z²/2 e desvio-padrão z. Valores:

| PSD | z antigo | z log correto | média antiga | média log correta |
|---|---:|---:|---:|---:|
{stale_table}

A mudança de z é −1,00188334284%. O desvio-padrão corrigido coincide com a coluna z log. Também é aceitável manter a tabela exclusivamente histórica, desde que seu nome/estatuto declare a convenção antiga e a interpretação global exclua explicitamente essa tabela da atualização. A inconsistência não contamina os 50 registros do portão, que leem `records` já corrigidos.

**F4-R2 — explicitação de escopo do controle empírico.** Em `refeito/measure_power_gate_013bis_v2.py:184`, os 16 `measured_psd_control` transportam cada curva de detector separadamente usando o rho total da rede. A aritmética confere, mas isso representa dois cenários alternativos normalizados ao mesmo rho; não mede o z de H1 e L1, nem combina a informação da rede. A origem `C5_FISHER_EMPIRICAL.json` já diz “each a separate single-detector forecast”; essa qualificação se perde na lista resumida.

Correção exata em versão nova: acrescentar à lista/cada entrada `rho_used`, `rho_kind=NETWORK_NORM_APPLIED_TO_EACH_PSD_SCENARIO` e `scope=Separate PSD-shape scenarios at common network rho; not detector-specific measured z or combined network Fisher`. Se a intenção for uma previsão de rede, ela exige Fisher de rede com normalizações por detector e nuisance comuns; não basta somar quadrados dos dois z aqui, pois ambos receberam todo o rho da rede. Esta ressalva não invalida a comparação de formas de PSD.

Não restou divergência nos cálculos centrais examinados. A aprovação integral dos artefatos deve aguardar a resolução de F4-R1 e a explicitação de F4-R2. Não há fundamento nesta auditoria para elevar o veredito físico; PE, cobertura/calibração IMR, realização estocástica e limites livres continuam com seus escopos abertos já declarados.

## Reprodução e integridade

Controle principal executado em WSL com `/opt/lal_env/bin/python -B`, apenas lendo insumos e gravando sua evidência em `bis/c1_review`. Revisão final escrita com o Python bundled, também sem importar código de produção. Axiomas: N/A — sem execução Lean. Scripts recusam sobrescrita; para repetir, usar cópia isolada com estrutura relativa e insumos preservados.

`f4_independent_results.json` contém erros por linha, quadraturas, hashes e limites. `f4_final_integrity.json` registra a conferência final dos insumos e os 16 controles empíricos. Nenhum PDF foi promovido a leitura integral nesta auditoria. Sem escrita em memória, canônico ou produções.

| Arquivo | SHA256 lido por script |
|---|---|
{hashes}
'''
    write_new(report, text.encode('utf-8'))
    print(json.dumps(dict(report=str(report), sha256=sha(report), bytes=report.stat().st_size,
                          integrity_inputs=len(matches), measured_psd_controls=len(controls)), ensure_ascii=False))


if __name__ == '__main__':
    main()
