# Operational v2 only. Existing audited results remain in bis/f2_injection.
"""Render this diagnostic and byte-hash receipts without changing upstream files."""

def publish_exclusive(temp, destination):
    """Atomic no-replace publication; fail closed if hard links unsupported."""
    import os
    try:
        os.link(temp, destination)
    finally:
        temp.unlink()
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json
OUT = Path(__file__).resolve().parent
B = OUT.parents[1]

def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda: f.read(1048576), b''):
            h.update(chunk)
    return h.hexdigest()

def new(name, text):
    p = OUT / name
    if p.exists():
        raise FileExistsError(p)
    raw = text.encode('utf-8')
    t = p.with_suffix(p.suffix + '.tmp')
    with t.open('xb') as f:
        f.write(raw)
    if not t.read_bytes() == raw:
        raise ValueError('Guard rejected: t.read_bytes() == raw')
    publish_exclusive(t, p)

def dump(obj):
    return json.dumps(obj, indent=2, ensure_ascii=False, allow_nan=False) + '\n'

def pair(x):
    return '[' + ', '.join((f'{v:+.6f}' for v in x)) + ']'

def ref(file, needle):
    lines = (B / file).read_text(encoding='utf-8-sig').split('\n')
    hits = [i for i, s in enumerate(lines, 1) if needle in s]
    if not hits:
        raise ValueError((file, needle))
    return f'{file}:{hits[0]}'
d = json.loads((OUT / 'DESCRIPTIVE_RESULT.json').read_bytes())
m = json.loads((OUT / 'METADATA.json').read_bytes())
c = json.loads((OUT / 'PRIOR_CONTRACT.json').read_bytes())
source = B / d['source']
if not sha(source) == d['source_sha256']:
    raise ValueError("Guard rejected: sha(source) == d['source_sha256']")
if not len(d['extraction_path_matches']) == 1:
    raise ValueError("Guard rejected: len(d['extraction_path_matches']) == 1")
if not d['extraction_path_matches'][0]['sha256'] == d['source_sha256']:
    raise ValueError("Guard rejected: d['extraction_path_matches'][0]['sha256'] == d['source_sha256']")
if not d['analytic_prior_dictionaries_identical']:
    raise ValueError("Guard rejected: d['analytic_prior_dictionaries_identical']")
for group in d['groups'].values():
    if not abs(sum(group['posterior_quadrants_220'].values()) - 1) < 1e-12:
        raise ValueError("Guard rejected: abs(sum(group['posterior_quadrants_220'].values()) - 1) < 1e-12")
    if not not group['truth_finite_fields']:
        raise ValueError("Guard rejected: not group['truth_finite_fields']")
    for s in group['summaries'].values():
        if not (s['n'] == 20000 and abs(s['p_positive'] - s['n_positive'] / s['n']) < 1e-14):
            raise ValueError("Guard rejected: s['n'] == 20000 and abs(s['p_positive'] - s['n_positive'] / s['n']) < 1e-14")
        if not s['min'] <= s['median'] <= s['max']:
            raise ValueError("Guard rejected: s['min'] <= s['median'] <= s['max']")
        if not all((s['quantiles'][i] <= s['quantiles'][i + 1] for i in range(len(s['quantiles']) - 1))):
            raise ValueError("Guard rejected: all((s['quantiles'][i] <= s['quantiles'][i + 1] for i in range(len(s['quantiles']) - 1)))")
order = '../TUNEL/PARA_CHATGPT/ORDEM_013BIS_fechamento_e_ampliacao_dos_eventos_ate_5sigma.md'
lines = ['# F2 lateral — diagnóstico das injeções públicas LVK de GW250114', '', '**[REAL — cálculo descritivo NÃO-CEGO; OPEN — contrato integral de lnB e calibração de cobertura; AGUARDA REVISÃO POR OUTRO AGENTE]**', '', 'Este agente construiu o cálculo independente; não o aprova adversarialmente. Raiz B: `C:\\IALD\\Central de Patentes\\Chatgpt\\ORDEM_013_RINGDOWN`. Somente `bis/f2_injection_v2/` recebeu escritas. Não houve PE, leitura de strain, campanha C5, import de produção/um.py, unpickle ou execução de notebook.', '', '**Resultado:** as duas configurações têm mediana positiva de δf220. A mediana de δτ220 é positiva com 44 e negativa sem 44. O ponto GR está dentro da região conjunta de 90% estimada com 44; sem 44, está na fronteira aproximada de 95%, sem classificação robusta de exclusão. Isso não demonstra tendência positiva universal, causalidade exclusiva do 44 nem cobertura frequentista calibrada. lnB permanece `null`, não zero.', '', '## Ordem, unidade de comparação e fonte', '', f'F2 exata lida em `{order}:79–87`, especialmente `:85`: pede extrair e descrever `pseobnr_injection/` em E1.3 e diz **uma injeção, com e sem 44, não curva em SNR**. Não multiplicamos os dois resultados como eventos independentes e não somamos ao catálogo. Este é o recorte lateral solicitado, não aceitação integral de F2 nem entrega M2.', '', f"Fonte: `{d['source']}`; {source.stat().st_size:,} bytes; SHA256 `{d['source_sha256']}`. Identidade conferida com `bis/F2_CONTROL_EXTRACTION.json` e `bis/F2_CONTROL_SCHEMAS.json`, e antes/depois da leitura. Dois grupos `NR_with_44`/`NR_without_44`, cada qual com `posterior_samples` de 20.000 linhas. Foram lidos apenas campos selecionados de posteriores/priors e metadados físicos; nenhum dataset de strain. O recibo atribui licença MIT ao membro; não foi refeito download do tar.", '', '[KNOWN — seção primária consultada online, não artigo integral] O [artigo LVK, apêndice .7, parágrafos da Fig. 11](https://arxiv.org/html/2509.08099v1#A1.SS7) descreve uma simulação SXS:BBH:3617, massas iguais e spins nulos, em ruído gaussiano. A comparação remove os multipolos (4,±4) da injeção, preservando a simulação e os parâmetros. O objetivo original é validar a informação de frequência do 440. Isso não é um ensaio de população nem de cobertura do 220. A coincidência dos nomes e o caminho de configuração SXS_3617 são consistentes com essa identificação; não reconstruí o sinal ou a semente de ruído. A página foi lida via web, não arquivada em bytes nesta tarefa: nenhum SHA web é inventado.', '', 'No HDF5, `config_file/config/zero_noise=False` e `gaussian_noise=False` não provam ausência de ruído em dados já preparados externamente. O artigo fornece o contexto gaussiano; não transportei para estas duas configurações a seleção de ruído descrita em outra subseção do artigo.', '', '## Localização e massa posterior positiva do setor 220', '', 'As colunas são frações adimensionais arquivadas `domega220` e `dtau220`; não desvios logarítmicos do RD. P(>0) é massa posterior empírica, não p-valor, poder ou probabilidade de física nova. IC abaixo significa intervalo **credível** central, com quantis lineares.', '', '| Configuração | Campo | Mediana | Média | DP amostral | IC 90% | IC 95% | P(>0) |', '|---|---|---:|---:|---:|---|---|---:|']
for label, g in d['groups'].items():
    for field in ['domega220', 'dtau220']:
        s = g['summaries'][field]
        lines.append(f"| {label} | {field} | {s['median']:+.6f} | {s['mean']:+.6f} | {s['sd_ddof1']:.6f} | {pair(s['central_intervals']['0.9']['interval'])} | {pair(s['central_intervals']['0.95']['interval'])} | {100 * s['p_positive']:.3f}% |")
lines += ['', '[REAL] Ambos os ICs marginais de 90% de δf220 excluem zero, mas ambos os de 95% o incluem. δτ220 com 44 inclui zero a 90% e 95%; sem 44, seu IC de 95% é inteiramente negativo. O intervalo contíguo mais curto de 95% dá as mesmas conclusões de inclusão para esses quatro casos; ele não foi chamado de HPD multimodal.', '', f"A diferença **com menos sem 44** entre medianas de δτ220 é {d['differences_with_minus_without']['dtau220']['median_difference']:+.6f}, e entre medianas de δf220 é {d['differences_with_minus_without']['domega220']['median_difference']:+.6f}. Não são diferenças pareadas linha a linha; não há distribuição de repetições/ruídos que permita convertê-las em significância de viés. A covariância entre os dois ensaios não foi recuperada.", '', '| Configuração | P(df>0, dtau>0) | Correlação posterior df/dtau | Pares 220 distintos / 20.000 |', '|---|---:|---:|---:|']
for label, g in d['groups'].items():
    lines.append(f"| {label} | {g['posterior_quadrants_220']['df_positive_dtau_positive']:.6f} | {g['posterior_correlation_220']:+.6f} | {g['posterior_joint_unique_rows_220']} |")
lines += ['', 'Duplicatas são mantidas como parte da medida empírica publicada; contagem de linhas não é ESS. Não há coluna de pesos nesses posteriores; a análise usa pesos iguais. Não revalidei a reamostragem/diagnósticos de convergência do produtor.', '', '## Referência GR e limite de cobertura', '', 'Estimamos c₀=P[p̂(df,dtau)≥p̂(0,0)] com KDE gaussiano: 16.000 linhas de treino, 4.000 de consulta fora do treino, uma divisão determinada pela semente 1302212026. GR pertence à região estimada de nível α se c₀≤α. Os multiplicadores de Scott são 0,7/1/1,4, como no registro C4. Não são três dados independentes.', '', '| Configuração | c₀, banda 0,7 | c₀, Scott | c₀, banda 1,4 | Escala binomial Scott, se iid | Suporte local Scott* |', '|---|---:|---:|---:|---:|---:|']
for label, g in d['groups'].items():
    v = g['hpd_GR_220']
    lines.append(f"| {label} | {v[0]['content_at_GR']:.5f} | {v[1]['content_at_GR']:.5f} | {v[2]['content_at_GR']:.5f} | {v[1]['query_binomial_scale_if_iid_only']:.5f} | {v[1]['kernel_weight_effective_count_not_chain_ESS']:.2f} |")
lines += ['', '*Suporte local = (Σw)²/Σw² dos kernels no ponto GR, não ESS da cadeia. A escala binomial é apenas uma referência condicional iid; não inclui incerteza de treino, dependência das amostras ou viés de KDE.', '', 'Sem 44, os booleanos mecânicos no JSON dão `inside_joint_95=false`, pois c₀ ficou ligeiramente acima de 0,95. **Não interpretar como exclusão robusta:** Scott dá 0,95075, distante do corte por só 0,00075, versus escala de consulta ≈0,00342. O suporte local Scott é ≈60; na banda 0,7, ≈28. A borda de 95% não está resolvida. Com 44, o conteúdo 0,85925–0,875 é compatível com inclusão conjunta a 90%/95%. Marginais e região conjunta respondem perguntas diferentes; não há contradição entre suas inclusões.', '', 'Os campos `injection_data` têm somente valores não finitos e `meta_data/other/injection_parameters` é a string `None` em ambos os grupos. `METADATA.json` preserva esses NaN como JSON null. [KNOWN/DERIVED] GR fornece a referência df=dtau=0 para o setor 220 de uma simulação GR; [OPEN] os parâmetros numéricos completos da injeção e a realização de ruído não foram recuperados desses campos. Remover o 44 cria um controle de conteúdo modal, não uma segunda população de fontes. Inclusão/exclusão de zero nestes posteriores não estima cobertura frequentista, taxa de falsos positivos ou viés médio do estimador.', '', '## Priors, setor 440 e aplicabilidade do mesmo lnB', '', '[REAL — declarações arquivadas] Em cada grupo, `priors/analytic/domega220` e `dtau220` declaram `Uniform(minimum=-0.8, maximum=2.0, ...)`; `domega440` e `dtau440` declaram `Uniform(minimum=-0.8, maximum=0.8, ...)`. As declarações de todos os priors analíticos são idênticas entre os grupos. Os quatro campos variam nos posteriores. **O 440 é livre na recuperação de ambos os casos**: “without_44” não significa fixar seu desvio a GR durante a recuperação. Priors de outros desvios modais arquivados são DeltaFunction em zero.', '', 'O prior 220 assimétrico já atribui P(δ>0)=2/2,8=0,714286. A massa positiva posterior de dtau com 44 (0,7776) excede essa base por apenas 0,063314; sem 44 cai a 0,01415. Essa comparação descritiva impede usar apenas o sinal da mediana como evidência de deslocamento físico. Amostras de prior (5.000 por campo), limites e correlações estão no JSON; correlação amostral próxima de zero não é prova de fatoração global.', '', '| Configuração | Campo 440 | Mediana | DP | IC 90% |', '|---|---|---:|---:|---|']
for label, g in d['groups'].items():
    for field in ['domega440', 'dtau440']:
        s = g['summaries'][field]
        lines.append(f"| {label} | {field} | {s['median']:+.6f} | {s['sd_ddof1']:.6f} | {pair(s['central_intervals']['0.9']['interval'])} |")
lines += ['', 'A frequência 440 fica mais informativa com o multipolo presente; sem ele, seu posterior é amplo e aproximadamente centrado em zero. Isso descreve estes produtos; não decide sozinho a origem dos deslocamentos do 220.', '', '**lnB não calculado neste diagnóstico (`PRIOR_CONTRACT.json`, `lnB:null`).** Os priors de deformação não são desconhecidos. A aplicação como evidência do mesmo modelo restrito requer também justificar o prior normalizado comum dos parâmetros auxiliares e que a curva de cada leitura esteja no suporte pertinente em todo esse prior. A identidade usada na C4 está em `posterior_220_readout.py:3–7` e `REGISTRO_C4.json` (chaves `priors`/`spin_dependent_model_identity`); não é uma média de razões condicionais.', '', 'O HDF5 referencia um `prior_file` externo `QNM_prior_44_narrow.prior`, traz `prior_dict=None` e `default_prior=BBHPriorDict`. Há priors analíticos e amostras de remanescente úteis, mas não reconstruí o arquivo externo, a conversão integral de remanescente ou uma garantia global de suporte das leituras. Os 5.000 spins de prior observados vão até 0,974891/0,964738; uma amostra finita não prova um limite de suporte. Não apliquei um novo corte de spin/prior para tornar a fórmula utilizável, pois isso mudaria o contrato. Trata-se de contrato **parcialmente verificado**, não de prova de impossibilidade futura nem de falta absoluta de priors. A ausência das verdades de injeção, por si só, não bloqueia um Bayes factor.', '', 'Reuso futuro tem caminhos exatos: `{NR_with_44,NR_without_44}/posterior_samples` campos `domega220`, `dtau220`, `final_spin_non_evolved`, `final_mass_non_evolved`, `redshift`; priors nos caminhos acima e `priors/samples/`. Qualquer comparação permanece no setor 220, mantendo o 440 como nuisance livre nos dois modelos. Não equivale a um teste de GR em todos os modos e não é diretamente o setor com 440 fixo usado em grande parte do catálogo.', '', '## Reprodução, custo e pendências', '', f"Execução numérica: **{d['elapsed_s']:.3f} s**, uma thread, Python {d['runtime']['python']}, NumPy {d['runtime']['numpy']}, SciPy {d['runtime']['scipy']}, h5py {d['runtime']['h5py']}. Sem geração de posterior ou campanha de injeções. Verificações internas: integridade antes/depois, 20.000 linhas finitas por grupo nos campos selecionados, quantis ordenados, contagens de sinais, soma dos quadrantes e limites dos priors. Isso é controle do construtor, não auditoria independente de aprovação.", '', 'Os scripts recusam sobrescrever resultados. Para revisão, ler os scripts e recalcular em cópia isolada autorizada, mantendo a relação B/bis/f2_injection e os arquivos de entrada; não executar contra saídas já presentes. Comando original, repetido para `inspect_injection.py`, `diagnose_injection.py`, `check_contract.py` e `write_report.py` nessa ordem:', '', '```powershell', 'wsl -e /opt/lal_env/bin/python -B "/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/f2_injection_v2/diagnose_injection.py"', '```', '', 'Não pagos por este recorte: cobertura frequentista, viés contra parâmetros completos de verdade, generalização a SNR/catálogos, isolamento causal do efeito do 44, lnB com contrato integral, validação da pipeline LVK e aprovação adversarial deste cálculo. Sem comunicação externa ou alteração de gate. Axiomas N/A.', '', '## Localizadores e arquivos escritos', '', f"- Quantis, sinais e intervalos: `{ref('bis/f2_injection_v2/diagnose_injection.py', 'def summary')}`; HPD: `{ref('bis/f2_injection_v2/diagnose_injection.py', 'def hpd_content')}`.", f"""- Priors arquivados: `{ref('bis/f2_injection_v2/METADATA.json', '"priors_analytic"')}`; checagem de contrato: `bis/f2_injection_v2/PRIOR_CONTRACT.json`.""", f'- Fonte normativa F2: `{order}:85`; contrato anterior: `posterior_220_readout.py:3–7,25–53` e `REGISTRO_C4.json`.', '', 'Todos os arquivos escritos nesta tarefa, relativos a B:', '']
written = ['bis/f2_injection_v2/inspect_injection.py', 'bis/f2_injection_v2/METADATA.json', 'bis/f2_injection_v2/diagnose_injection.py', 'bis/f2_injection_v2/DESCRIPTIVE_RESULT.json', 'bis/f2_injection_v2/check_contract.py', 'bis/f2_injection_v2/PRIOR_CONTRACT.json', 'bis/f2_injection_v2/write_report.py', 'bis/f2_injection_v2/REPORT.md', 'bis/f2_injection_v2/RECEIPT.json']
lines += [f'{i}. `{name}`' for i, name in enumerate(written, 1)]
lines += ['', 'Os hashes completos dos arquivos, código, insumos e fontes locais estão em `RECEIPT.json`; o recibo não inclui seu próprio hash para evitar autorreferência. Fontes online não arquivadas são identificadas por URL e alcance de leitura, sem hash fictício.', '']
new('REPORT.md', '\n'.join(lines))
inputs = [source, B / 'bis/F2_CONTROL_EXTRACTION.json', B / 'bis/F2_CONTROL_SCHEMAS.json', B / order, B / 'REGISTRO_C4.json', B / 'posterior_220_readout.py', B / 'catalog_220_readout.py']
receipt = {'status': 'BUILDER_RECEIPT__AWAITING_INDEPENDENT_REVIEW', 'utc': datetime.now(timezone.utc).isoformat(), 'root_windows': 'C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN', 'inputs': [{'path': str(p.relative_to(B)), 'bytes': p.stat().st_size, 'sha256': sha(p)} for p in inputs], 'files_written': [{'path': p, 'bytes': (B / p).stat().st_size, 'sha256': sha(B / p)} for p in written if not p.endswith('RECEIPT.json')], 'receipt_self': 'bis/f2_injection_v2/RECEIPT.json; own hash computed separately', 'online_primary': {'url': 'https://arxiv.org/html/2509.08099v1', 'read_scope': 'appendix .7 and search context; not full article', 'archived_bytes': False, 'sha256': None}, 'unchanged_source_sha256_after_reporting': sha(source), 'lnB': None, 'adversarial_approval': 'NOT_PERFORMED_BY_BUILDER'}
new('RECEIPT.json', dump(receipt))
print(dump({'written': ['REPORT.md', 'RECEIPT.json'], 'receipt_sha256': sha(OUT / 'RECEIPT.json')}))
