"""Assemble the independent review from measured numbers and source excerpts.
Only the two explicitly authorized report paths are replaced, atomically.
"""
import hashlib
import json
import math
import os
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
ROOT = BASE.parent
J = BASE/'bis/C0_ADVERSARIAL_SOURCE_REVIEW.json'
M = J.with_suffix('.md')
r = json.loads(J.read_bytes())
evidence = []

def add(rel, spans=(), role='primary', needles=()):
    p = (ROOT/rel).resolve()
    assert p.is_relative_to(ROOT)
    b = p.read_bytes()
    key = str(p)
    old = r['sources'].get(key)
    meta = {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
    if old:
        assert old['sha256']==meta['sha256'], ('source changed',key)
    r['sources'][key] = meta
    lines = b.decode('utf-8-sig').splitlines()
    ranges = list(spans)
    for needle in needles:
        hits = [i for i,s in enumerate(lines,1) if needle in s]
        assert hits, (rel,needle)
        ranges.append((hits[0],min(hits[0]+5,len(lines))))
    for a,z in ranges:
        assert 1<=a<=z<=len(lines),(rel,a,z,len(lines))
        evidence.append({'path':key,'line_start':a,'line_end':z,'role':role,
                         'excerpt':'\n'.join(lines[a-1:z])})
    return json.loads(b) if p.suffix=='.json' else None

P = 'ORDEM_013_RINGDOWN/'
add('TUNEL/TUNEL_PROTOCOLO.md',[(15,29),(64,79)],'instruction')
add('TUNEL/PARA_CHATGPT/ORDEM_013BIS_fechamento_e_ampliacao_dos_eventos_ate_5sigma.md',[(70,72)],'instruction')
add('TUNEL/PARA_CHATGPT/ORDEM_013_confrontacao_do_ringdown.md',[(36,41)],'instruction_not_primary_proof')
add('TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/auditoria_da_gerencia/aud_1_C0_C1_C2.txt',[(37,44)],'prior_audit_not_primary_proof')
add('TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/auditoria_da_gerencia/scripts/C0C1C2/gksl_oracle.py',[(1,10)],'prior_auditor_code_not_executed')
add(P+'cache/casa/um.py',[(95,95),(2311,2332),(2335,2342),(2831,2839),(7151,7156),(190563,190584),(190961,190968),(191005,191017)])
add(P+'cache/casa/ModularFirstLaw.lean',[(45,58)])
add(P+'cache/casa/ContinuousModularZero.lean',[(62,93)])
add(P+'cache/casa/davies_geometry.tex',[(60,78),(138,157),(214,231),(311,325)])
add(P+'cache/casa/tgl_paper_unified.py',[(1983,2025),(2892,2900),(9130,9134),(11049,11067),(11100,11119)])
add(P+'cache/casa/ringdown_dephasing_v2.py',[(139,141)])
add(P+'cache/casa/RINGDOWN_DEPHASING_V2_RESULT.json',needles=['"stacks":'])
add(P+'cache/casa/um_absoluto.json',needles=['"d1_camb_v3_real_v366":'])
add(P+'cache/casa/MEMORIA_DA_LINHAGEM.md',[(8198,8204)],'historical_cross_reference_only')
add(P+'C0_AUDITORIA.md',[(20,30),(116,138),(224,258)],'reviewed_claims')
c0 = add(P+'C0_AUDITORIA.json',role='reviewed_claims',needles=['"template":','"lvk":'])
add(P+'C0_C3_checks.json',role='existing_result',needles=['"signed_modular_extensions":'])
table = add(P+'C1_TABLES.json',role='existing_result')
initial = add(P+'C4_220_INITIAL.json',role='existing_result',needles=['"quantiles":','"correction_over_marginal_sigma":'])
combo = add(P+'C4_CATALOG_COMBINATION.json',role='existing_result',needles=['"selected_events":','"common_deformation_GR_diagnostics":'])
add(P+'C4_CATALOG_220.json',role='existing_result')
add(P+'posterior_220_readout.py',[(90,95)],'existing_code_read_only')
add(P+'LITERATURE_MANIFEST.json',role='existing_manifest',needles=['"gw250114_article.html"'])
add(P+'cache/literature/gw250114_article.html',[(493,493),(522,522)])
# Keep copyrighted excerpts short; the primary sections were read in full at these locations.
for rel,line in [('cache/literature/gwtc3_article_v3.html',11373)]:
    add(P+rel)
    evidence.append({'path':str(BASE/rel),'line_start':line,'line_end':line,'role':'primary',
                     'excerpt':'is biased towards positive values','excerpt_mode':'short exact excerpt from the line'})
rel='TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/B_catalogos/gwtc5_tgr.txt'
add(rel,[(4654,4656)])
receipt = add(P+'bis/INPUT_INTEGRITY_013BIS_retry.json',role='existing_integrity_receipt')
r['integrity_receipt'] = {'inputs':len(receipt['inputs']),'sources':len(receipt['sources']),
    'audited_state':len(receipt['audited_state']),'all_frozen_match_recorded':receipt['all_frozen_match'],
    'scope':'Receipt read, not entire 217/31 campaign rerun. Files used in this review independently hashed.'}
# Check the extracted D1 result against the literal pinned in the source, not memory.
u = (BASE/'cache/casa/um.py').read_text(encoding='utf-8').splitlines()
import ast
pin_line = next(s for s in u if s.startswith("    'saida/D1_CAMB_V3_REAL_RESULT.json': '") and len(s)<160)
r['d1']['embedded_pin_matches'] = r['d1']['embedded_utf8_sha256']==ast.literal_eval(pin_line.split(': ',1)[1].rstrip(','))
assert r['d1']['embedded_pin_matches']
e = r['GW250114']; b = r['beta_runtime']
sample_sd = e['sigma_dtau_population']*math.sqrt(e['N']/(e['N']-1))
e['sigma_dtau_sample_ddof1'] = sample_sd
e['correction_over_sample_sigma'] = abs(e['delta_RB_05_50_95'][1])/sample_sd
assert abs(e['correction_over_sample_sigma']-initial['rows'][0]['correction_over_marginal_sigma'])<1e-12
q = next(row['prediction'] for row in table['rows'] if row['event'].startswith('GW250114') and row['prediction']['reading']=='R-MOD')
x = b*q['tau_gr_s']/q['t_mass_s']; delta = -x/(1+x)
e['Gamma_beta_over_tM_exact_QNM_input'] = {'x':x,'delta':delta,'correction_over_sample_sigma':abs(delta)/sample_sd,
 'distance_to_observed_median_in_sigma':abs(delta-e['quantiles_05_50_95']['dtau220'][1])/sample_sd,
 'input_source':'C1_TABLES.json R-MOD row GW250114; only tau_gr_s/t_mass_s reused, not the R-MOD physical hypothesis',
 'scope':'Arithmetic reobtained from archived exact-QNM values; no independent Leaver/qnm solve in this review'}
add(P+'tgl_ringdown_template.py',role='current_artifact')
for p in BASE.glob('tgl_ringdown_template.py.bak*'):
    add(P+p.name,role='backup_candidate')
expected = c0['references']['template']['sha256']
r['template_reference']={'expected_from_C0':expected,'current_sha256':r['sources'][str(BASE/'tgl_ringdown_template.py')]['sha256'],
 'match':expected==r['sources'][str(BASE/'tgl_ringdown_template.py')]['sha256'],
 'search_scope':'Current template and immediate sibling backups only; no exhaustive claim about every disk or archive.',
 'historical_loss':'DECLARADO by prior management auditor; neither current nor immediate sibling backup matches.'}
r['evidence'] = evidence
r['findings'] = [
 {'id':'T02','severity':'CORRIGIR','status':'REAL_SOURCE_AND_DERIVED_COUNTEREXAMPLE','result':'Finite root dephasing and Davies transition family are distinct. Family absent from _verb_L, present in article code. README chronology remains DECLARADO.'},
 {'id':'T02-extra','severity':'CORRIGIR','status':'REAL_COUNTEREXAMPLE','result':'Universal coherent redundancy in davies_geometry.tex is false; article code already limits it to KMS/steady state.'},
 {'id':'T10','severity':'CORRIGIR','status':'REAL_PRIMARY_HDF5_READ','result':'24/31 positive dtau medians; V2 positive too; additive positive damping predicts nonpositive shift, not its physical interpretation.'},
 {'id':'T11','severity':'CORRIGIR','status':'REAL_ARITHMETIC_FROM_EMBEDDED_RESULT','result':'V2 effect/sigma 0.177851389; D1 symmetric-error tension 3.012497521; chain/autocorrelation limitation retained.'},
 {'id':'T19','severity':'CORRIGIR','status':'DERIVED_CONDITIONAL','result':'Gamma=beta/tM gives -0.128545147 from exact-QNM input, -0.127656099 from BCW; tau_star and physical partition not derived by cited formulas.'},
 {'id':'T20/T21','severity':'CORRIGIR','status':'REAL_PRIMARY_POSTERIOR_AND_DERIVED_RB','result':'R-B median -0.0198452854; sample sigma 0.05779438; correction/sigma 0.343377425; pSEOB damping limits not universal few-percent ringdown limits.'},
 {'id':'C0(d)-finite','severity':'CORRIGIR','status':'REAL_SOURCE_READ_NO_COMPILATION','result':'ModularFirstLaw is finite diagonal derivative without sum(p)=1. ContinuousModularZero is finite superoperator, not same K and not a new III1 proof.'},
 {'id':'C0(d)-III1','severity':'CORRIGIR','status':'KNOWN_PRIMARY_SECTIONS_READ','result':'No faithful normal semifinite trace on III1; no intrinsic tracial density representation. Modular Delta and log Delta still exist in standard representation.'},
 {'id':'C0(d)-rates','severity':'CORRIGIR','status':'REAL_MATRIX_ACTION','result':'abs(K) rate(+3,-3)=0; K_plus=3 beta/2. For (0,1), both yield beta/2. Rates require clock conversion for SI units.'}
]
r['unread_or_not_reobtained'] = [
 'README TGL_v2 25/05/2026 not located in cache/casa or supplied order inputs; chronological claim only read in ORDEM_013:36.',
 'Standalone davies_geometry_derivation.py cited by TeX not located in allowed source bundle; article implementation read instead.',
 'Dates 25/05 and 31/05 not independently established from version history. TeX uses date{today}.',
 'Original standalone D1 result/chains not opened; exact embedded JSON literal read and its bytes hashed, matching embedded pin. No rerun of MCMC.',
 'Connes entire 121-page PDF not read; printed pp.133-134 read. Sorce full proof not read; introduction equations 1-6 read.',
 'Milburn 1991, Davies 1974, Bisognano-Wichmann, Kay-Wald and Sewell original texts not read in this recorte and not used as proof.',
 'Full 217/31 integrity campaign, Lean compilation and all claims T01-T24 not redone.',
 'Joint catalog KDE/lnB/GR HPD not recomputed; only primary HDF5 medians, selected set membership, individual GW250114 quantiles and widths reobtained.',
 'No categorical global absence of a family throughout all embedded um.py payloads asserted; reviewed _verb_L and identified local references only.'
]

def ref(rel, line):
    path = str(ROOT/rel).replace('\\','/')
    return f'[{rel}:{line}](<{path}:{line}>)'

def c(rel,line):
    return ref(P+rel,line)

md = f'''# Revisão adversarial independente — C0/F1, ORDEM_013BIS

[REAL — leitura de fontes e contas leves independentes] **As erratas C0 examinadas são necessárias; T02 exige ainda corrigir a própria frase “família L_k inexistente” para delimitar seu escopo.** Esta revisão termina o recorte solicitado, com lacunas explicitadas. Não constitui aprovação de C0_v2, de F1 inteiro, do pacote final ou de gate.

Esta tarefa não construiu C0/C1/C2. O auditor anterior serviu como roteiro; as conclusões abaixo vêm das fontes e das contas desta tarefa. Fonte modificada: nenhuma. Leitura da skill `tgl-atlas` efetuada; consulta ao Atlas canônico e escrita em memória foram dispensadas pelo escopo expresso somente leitura sob Chatgpt. As instruções aplicadas estão no {ref('TUNEL/TUNEL_PROTOCOLO.md',15)} e na {ref('TUNEL/PARA_CHATGPT/ORDEM_013BIS_fechamento_e_ampliacao_dos_eventos_ate_5sigma.md',72)}. Os números históricos não foram tratados como atualizações automáticas.

## T02 — origem, família e proxy

[REAL] A cadeia documental acessível é a nota finita {c('cache/casa/davies_geometry.tex',60)}, a fig02 {c('cache/casa/tgl_paper_unified.py',9131)}, o enunciado GKSL {c('cache/casa/tgl_paper_unified.py',11049)} e as implementações. A nota diz “finite-dimensional matrix algebra” e limita o alcance a tipo I. As datas README TGL_v2 25/05 → nota 31/05 estão **[DECLARADO]** na {ref('TUNEL/PARA_CHATGPT/ORDEM_013_confrontacao_do_ringdown.md',36)}: o README primário não foi localizado no recorte; o TeX usa `\\date{{\\today}}`. Não confundir uma cadeia de remissões com cronologia primária verificada, nem afirmar que foi identificada a fonte efetiva do texto externo.

Em {c('cache/casa/um.py',2311)}, o trecho `K = (Araw @ Araw.T) / n` usa n=4, seed=11; `L = sqrt_beta * sqrtK` constrói **um** salto hermitiano. O estatuto está explícito em {c('cache/casa/um.py',2341)}: `[FINITE_DIM_SANITY_NOT_III1_PROOF]`. Reobtive o espectro de K: {r['proxy']['eigenvalues_K']}. Seus quatro projetores espectrais são estacionários, resíduo máximo {r['proxy']['four_independent_stationary_projectors_residual']:.3e}; o atrator dependente de rho0 é pinching, não um estado Gibbs único. Para o rho0 da fonte, ||rho_star − exp(−K)/Z||_F = {r['proxy']['rho_star_minus_exp_minus_K_normalized_frobenius']:.12f}.

[REAL + DERIVED] **Há família L_ij no código do Artigo A**: {c('cache/casa/tgl_paper_unified.py',1983)} percorre i≠j e adiciona `(gamma, A)`, com A=|i⟩⟨j|, taxas Bose e acoplamento comum β. Para espectro simples d=8 isso dá 56 saltos; não é a decomposição espectral de um único sqrt(K). A passagem para um único salto em {c('cache/casa/tgl_paper_unified.py',11103)} não decorre do balanceamento KMS.

Contraexemplo independente 2×2: K=diag(0,1), rho=|0⟩⟨0|. O salto sqrt(β)sqrt(K) dá d rho11/ds=0, enquanto os saltos Davies explicitados dão β/(e−1)={r['davies_counterexample']['davies_d_rho11']:.15g}>0. O primeiro conserva todas as populações na base de K; o segundo as transfere. **Não são representações equivalentes do mesmo dissipador.** A frase segura é: “família física indexada não construída por `_verb_L`; família de transições finita existe no Artigo A, sem ponte demonstrada para o salto-raiz ou para um horizonte III₁”. A analogia operacional em {c('cache/casa/um.py',7151)} declara expressamente que não é identidade física.

Achado conexo: {c('cache/casa/davies_geometry.tex',214)} afirma invariância de toda trajetória ao adicionar −i[K,rho]. Para rho=|+⟩⟨+|, positivo de autovalores 0 e 1, a diferença entre derivadas tem norma Frobenius {r['davies_counterexample']['hamiltonian_changes_derivative_norm']:.15g}, não zero. Comutação de dois fluxos não implica que um seja identidade. O próprio Artigo A já corrige a proposição em {c('cache/casa/tgl_paper_unified.py',2892)}: igualdade sobre KMS/estado estacionário, não rho arbitrário. A revisão deve transportar essa restrição. Nenhum desses contraexemplos falsifica globalmente a teoria; identifica exatamente a inferência documental inválida.

## T10 — sinal observado

[REAL] Reabri **31 HDF5 primários**, selecionados pelo conjunto já declarado em C4_CATALOG_COMBINATION: **24/31 medianas de dtau220 positivas**. Diferença máxima frente às medianas do C4_CATALOG_220.json: **0**. O JSON desta revisão guarda caminho, dataset, N, mediana e hash de cada HDF5; arquivos binários são citados por dataset, não por linhas fictícias. Não fiz seleção por sinal.

O V2 primário, {c('cache/casa/RINGDOWN_DEPHASING_V2_RESULT.json',1)}, registra em stacks/3.0 δτ={r['v2_stacks']['3.0']['delta_tau']:.12f} ± {r['v2_stacks']['3.0']['sigma']:.12f}; em stacks/6.0, {r['v2_stacks']['6.0']['delta_tau']:.12f} ± {r['v2_stacks']['6.0']['sigma']:.12f}. É outro instrumento/estrato; não somei ao catálogo. A lei de ensemble com Γ≥0, τ_GR>0 dá δτ=−x/(1+x)≤0, x=Γτ_GR. Logo o deslocamento comum positivo não tem o sinal desse amortecimento aditivo.

[KNOWN — seções primárias lidas] GWTC-3 discute o viés positivo em {c('cache/literature/gwtc3_article_v3.html',11373)}; GWTC-5 discute seleção favorecendo desvios positivos em {ref(rel,4654)}. Isso não identifica a causa do desvio: sistemática de forma de onda, estimador/prior, seleção e física nova não se tornam resultados exclusivos por essa observação. **Não repetir “RG passa em todos os testes”**: o JSON conjunto registra HPD da RG ≈0,983, mas não refiz a integração conjunta e não a uso como nova medição nesta revisão.

## T11 — β em GW e no D1

[REAL — aritmética sobre resultados] No V2, |δ_B|/σ={r['v2_stacks']['3.0']['power_B_recomputed']:.12f}≈0,18σ. `power_B` é separação efeito/erro, não uma probabilidade de poder estatístico. Não há medição GW independente de β no resultado conferido; na lei quadrática o produto βτ★ é degenerado sem relógio/partição identificados.

Fora de GW, li **sem importar/executar um.py** o literal JSON em {c('cache/casa/um.py',190499)}. Hash UTF-8 reobtido do literal: `{r['d1']['embedded_utf8_sha256']}`, igual ao pin lido no próprio fonte. β_med={r['d1']['posterior']['median']:.15g}, erro superior {r['d1']['posterior']['sigma_upper']:.15g}, inferior {r['d1']['posterior']['sigma_lower']:.15g}. Pela convenção simétrica efetivamente usada em {c('cache/casa/um.py',190565)}, σ={r['d1']['sigma_symmetric']:.15g} e |β_med−α√e|/σ={r['d1']['z_recomputed']:.12f}.

A frase pública deve incluir **D1_BETA_TENSION, 3,01σ**, e sua limitação: resultado no limiar; N/50=40 contra autocorrelação até 41,60, com 2/4 parâmetros abaixo de 50τ. Não refiz cadeia, likelihood cosmológica nem convergência. O número é diagnóstico pela convenção da fonte, não significância de cauda reavaliada. Tensão não é falsificação nem confirmação.

## T19 — supressão, relógio e −0,13

[DERIVED — condicional] Com Γ=β/t_M, x=βτ_GR/t_M e δτ=−x/(1+x). Usando tau_GR/t_M do QNM exato arquivado em C1_TABLES (sem escolher a hipótese R-MOD), x={x:.15g}, δτ={delta:.15g}; portanto o −0,1285 pedido foi reobtido. No controle BCW avaliado independentemente, δτ={e['Gamma_beta_over_tM']['delta']:.15g}. Essa diferença é de método QNM, não erro de arredondamento. O valor exato corresponde a {e['Gamma_beta_over_tM_exact_QNM_input']['correction_over_sample_sigma']:.4f}σ como tamanho da correção e {e['Gamma_beta_over_tM_exact_QNM_input']['distance_to_observed_median_in_sigma']:.4f}σ como distância à mediana observada; são comparações diferentes, nenhuma é Bayes factor ou teste calibrado.

Há supressão canônica já escrita: Γ=(β/2)τ★ω² com τ★=t_P `[PRINCIPLED IDENTIFICATION]` em {c('cache/casa/um.py',190966)}, e ramo A no {c('cache/casa/ringdown_dephasing_v2.py',139)}. Essa presença não deriva o relógio da geometria nem fixa a partição. A errata {c('cache/casa/um.py',2837)} distingue igualdade de expoente de igualdade de coeficiente: lei-raiz no IR fornece β(Δk)²/(8 kbar), coincidindo com o coeficiente declarado somente com kbar=1/4 [INPUT]. “Nada deriva τ★” deve significar **nenhuma derivação nas fontes/elos conferidos**, não uma prova de inexistência em todo o acervo. A identificação física continua aberta em {c('cache/casa/um.py',191013)}.

## T20/T21 — precisão e efeito comparável

[REAL — HDF5 primário] Para GW250114, N={e['N']}; dtau220 q05/50/95={e['quantiles_05_50_95']['dtau220']}; df220={e['quantiles_05_50_95']['domega220']}. Reobtive σ_amostral(dtau)={sample_sd:.15g} (ddof=1), a convenção da bancada em {c('posterior_220_readout.py',93)}. R-B, calculado amostra a amostra com BCW: mediana {e['delta_RB_05_50_95'][1]:.15g}, correção/σ={e['correction_over_sample_sigma']:.15g}, igual ao JSON anterior a <1e−12. O σ populacional foi guardado separadamente; explica a diferença de 4,2e−6 no quociente inicial.

[KNOWN] A fonte LVK local {c('cache/literature/gw250114_article.html',493)} dá frequência 220 em escala de 2% e amortecimento −0,01(+0,10/−0,09), com credibilidade de 90%, na análise pSEOBNR IMR. O ringdown isolado é menos restritivo, conforme {c('cache/literature/gw250114_article.html',522)}. Assim, “poucos por cento em todos os testes” não é sustentado. A frase corrigida deve carregar **R-B ≈−0,020 versus σ≈0,058: 0,34σ**, a hipótese de ensemble e a dependência de modelo. Consistência com Kerr não equivale a confirmação física da TGL.

## C0(d) — os dois K, traço e log Δ

[REAL — enunciados lidos, sem recompilar] {c('cache/casa/ModularFirstLaw.lean',45)} declara `[Fintype n]`; `first_law_diagonal`, linhas 55–58, assume p_i>0 e Σq_i=0 e prova a derivada de −Σ(p_i+εq_i)log(p_i+εq_i) igual a Σq_i(−log p_i). **Não assume Σp_i=1.** Consequentemente não prova K_i≥0: p_i>1 dá −log p_i<0. Com pesos de estado normalizados obtém-se K_unilateral=−log rho≥0, mas a normalização é uma hipótese adicional para essa leitura. Não há identificação com o gerador modular bilateral.

{c('cache/casa/ContinuousModularZero.lean',62)} também tem `[Fintype n]`; define `modularGen rho y = y * logRho rho - logRho rho * y`. Em E_ij, os autovalores são log p_j−log p_i; aparecem pares ±k. As linhas 80–93 estabelecem anulação de Omega (rho.PosDef) e J K J=−K na face matricial. Com h=−log rho, este K é L_h−R_h, não h. A igualdade entre objetos homônimos não está provada por essas duas pedras; “contínuo” no nome não elimina a hipótese finita.

[KNOWN — primária lida] Connes, *Une classification des facteurs de type III* (1973), p.133, recorda o critério **fator não-III ⇔ existência de traço normal fiel semifinito**; p.134 distingue pesos de traços e introduz a estrutura modular. Portanto III₁ não admite tal traço. Li pp.133–134, não o trabalho inteiro. [PDF primário Numdam](https://www.numdam.org/item/10.24033/asens.1247.pdf), SHA-256 `{r['external_primary'][0]['sha256']}` calculado dos {r['external_primary'][0]['bytes']} bytes recebidos em memória. O sinal ≠ saiu corrompido no OCR; foi cruzado com a renderização matemática indexada no site do autor.

[KNOWN] Sorce, *A short proof of Tomita’s theorem*, introdução, eqs.(1)–(6), fornece S=JΔ^1/2 e Δ positivo autoadjunto injetivo para vetor cíclico separante, com grupo modular preservando a álgebra. [Primária lida](https://arxiv.org/html/2309.16762v2). Não li a prova inteira; não inventei hash dos bytes que o navegador não entrega.

[DERIVED — distinção de tipos] O que falta em III₁ é a representação **intrínseca tracial** do estado como τ(rho·), com τ normal fiel semifinito na mesma álgebra. Isso não proíbe estados normais, representações vetoriais ou matrizes densidade ambientais em B(H). Δ tem logaritmo autoadjunto por cálculo espectral: log Δ pode ser ilimitado, em seu domínio denso; 0 pode estar no espectro contínuo sem ser autovalor. Logo **não concluir “log Δ não existe” nem “todo Hamiltoniano desaparece” da ausência de traço**. O passo de {c('cache/casa/davies_geometry.tex',317)} que atribui H_eff=0 à obstrução III₁ não é consequência desse critério. Usar sqrt(K) real positivo para K bilateral exige uma nova escolha f(K)≥0 e condições de domínio/geração; o oráculo finito não resolve a construção ilimitada.

## C0(d) — ±k e as escolhas positivas

[DERIVED + REAL em matriz finita] Para L=sqrt(β)sqrt(f(K)), Γ_ij=β/2(√f(k_i)−√f(k_j))². A avaliação independente da ação do dissipador em todos os E_ij do espectro [−3,−1,0,1,3] teve resíduo máximo {r['rates']['abs_K']['max_action_residual']:.3e}.

| Escolha | Γ(+3,−3) | Γ(0,1) | Consequência |
|---|---:|---:|---|
| f(K)=abs(K) | 0 | {b/2:.15g} | preserva coerência entre ±k para este canal |
| f(K)=K_+ | {3*b/2:.15g} | {b/2:.15g} | Γ(+k,−k)=βk/2, para k>0 |

As taxas são por unidade do parâmetro do dissipador usado no oráculo; **não s⁻¹ sem relógio de conversão**. “Não defasa ±k” vale para esse canal, não é imunidade a qualquer dinâmica adicional. Nenhuma das escolhas é fixada por Tomita; ambas permanecem [INPUT].

## Custódia, pendências honestas e reprodução

O recibo existente declara {len(receipt['inputs'])}/{len(receipt['inputs'])} insumos, {len(receipt['sources'])}/{len(receipt['sources'])} fontes e 34 artefatos de estado. Ele foi lido; não refiz a campanha inteira. Os arquivos usados aqui foram hashados por script. C0 ainda cita o template `{expected}`; o atual tem `{r['template_reference']['current_sha256']}`. O atual e o backup irmão conferidos não recuperam a referência. **Perda histórica é [DECLARADO] pelo auditor anterior; não fiz busca exaustiva de todos os discos.** A fonte LVK está arquivada com hash calculado no anexo: não deve continuar “ARCHIVING_PENDING” de modo indiferenciado. Arquivamento não implica leitura integral.

Não lidos/reexecutados: README histórico; davies_geometry_derivation.py independente; cadeias originais do D1; textos integrais de Connes/Sorce; primárias Milburn/Davies/BW/Kay–Wald/Sewell; compilação Lean; inferência cosmológica; KDE conjunto/lnB; outros itens de F1. O literal D1, as implementações indicadas, os dois enunciados Lean e os trechos LVK especificados foram efetivamente lidos. O JSON discrimina cada alcance e guarda os excertos locais.

Reprodução, sem importar fontes:

```powershell
wsl -e /opt/lal_env/bin/python -B '/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/c0_review/review_numbers.py'
& 'C:\\Users\\rotol\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\python\\python.exe' -B -X utf8 '{BASE}\\bis\\c0_review\\read_theory.py'
python -B -X utf8 '{BASE}\\bis\\c0_review\\complete_review.py'
```

O primeiro comando faz contas 2×2–5×5, hashes e leitura de 31 HDF5 de catálogo mais o posterior GW250114; sem PE/jobs pesados. O segundo usa rede apenas para a fonte pública Numdam, mantendo PDF em memória. Scripts escrevem somente relatórios autorizados, por temporário verificado → replace; não há atualização de memória. Axiomas: **N/A — leitura de Lean, sem compilação nem nova certificação de axiomas.** A tentativa inicial de impressão Python falhou por CP1252, corrigida com `-X utf8`; WSL/rede restritos falharam inicialmente, acesso de leitura foi autorizado pela revisão automática; 403 do site de Connes contornado pelo Numdam. Nenhuma falha virou sucesso presumido.
'''

r['files_written'] = [str(J),str(M)] + [str(p) for p in sorted((BASE/'bis/c0_review').glob('*.py'))]
r['temporary_files_created_and_replaced'] = [str(BASE/'bis/c0_review'/n) for n in ['report.tmp','theory.tmp','review.json.tmp','review.md.tmp']]
for p in (BASE/'bis/c0_review').glob('*.py'):
    data = p.read_bytes(); r['sources'][str(p)]={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'role':'review_script'}
md += '\n## Arquivos escritos\n\n' + '\n'.join('- `'+p+'`' for p in r['files_written'])
md += '\n\nTemporários transitórios, consumidos por substituição: '+', '.join('`'+Path(p).name+'`' for p in r['temporary_files_created_and_replaced'])+'. Nenhum outro arquivo escrito por esta tarefa.\n'
md += '\n## Hashes calculados — fontes locais e scripts\n\n| Caminho absoluto | Bytes | SHA-256 |\n|---|---:|---|\n'
for path,v in sorted(r['sources'].items()):
    md += f"| `{path}` | {v['bytes']} | `{v['sha256']}` |\n"
md += '\nOs hashes dos próprios relatórios não são embutidos neles para evitar autorreferência; podem ser reobtidos com Get-FileHash.\n'
for target,data,tmpname in [(J,(json.dumps(r,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode(),'review.json.tmp'),(M,md.encode(),'review.md.tmp')]:
    tmp = BASE/'bis/c0_review'/tmpname; tmp.write_bytes(data)
    assert tmp.stat().st_size==len(data) and len(data)>1000
    os.replace(tmp,target)
print(json.dumps({'findings':len(r['findings']),'sources':len(r['sources']),'files_written':r['files_written'],'report_bytes':M.stat().st_size},ensure_ascii=False,indent=2))
