"""Record source-audited C0 corrections beside, never over, the historical v1."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(2**20), b''):
            h.update(block)
    return h.hexdigest()

def new(path, text):
    if path.exists():
        raise FileExistsError(path)
    raw = text.encode('utf-8')
    tmp = path.with_name(path.name + '.tmp')
    with tmp.open('xb') as f:
        f.write(raw)
    assert tmp.read_bytes() == raw
    tmp.replace(path)

def main():
    old = ROOT / 'C0_AUDITORIA.json'
    before = old.read_bytes()
    data = json.loads(before)
    review_path = ROOT / 'bis/C0_ADVERSARIAL_SOURCE_REVIEW.json'
    review = json.loads(review_path.read_bytes())
    for path, receipt in review['sources'].items():
        p = Path(path)
        assert p.stat().st_size == receipt['bytes'], p
        assert sha(p) == receipt['sha256'], p
    gw = review['GW250114']
    exact = gw['Gamma_beta_over_tM_exact_QNM_input']
    corrections = {
        'T02': '[REAL] _verb_L constrói um salto hermitiano num proxy positivo 4×4, seed 11, FINITE_DIM_SANITY_NOT_III1_PROOF. Há uma família finita de transições Davies no Artigo A (56 saltos para espectro simples de dimensão 8); ela não é equivalente ao salto-raiz: um transfere populações, o outro as conserva. Família física de horizonte não construída; a expressão “família inexistente” só vale para _verb_L. README TGL_v2 25/05 → nota 31/05 é cronologia DECLARADA, README primário não localizado; nota finita → fig02 → teorema/implementações foram lidos. A identidade da fonte efetivamente usada pelo texto externo permanece OPEN.',
        'T10': '[REAL] O catálogo selecionado tem 24/31 medianas de δτ positivas; o V2 registra +0,176647±0,108894 e +0,031294±0,175529, estratos distintos, não somados. Amortecimento aditivo Γ≥0 prevê δτ=−Γτ/(1+Γτ)≤0. Viés de seleção, forma de onda, estimador e física nova permanecem hipóteses distintas; não se declara RG aprovada em todos os testes.',
        'T11': '[REAL, aritmética sobre resultados] Em GW, β não foi medido independentemente: a razão efeito/erro do V2 é 0,177851σ, não uma probabilidade de poder. Fora de GW, D1 V3 dá β livre em tensão com α√e: D1_BETA_TENSION, %.8gσ pela convenção simétrica da fonte. Cadeia não refeita; N/50=40 e autocorrelação até 41,60, com 2/4 parâmetros aquém de 50τ. O produto βτ★ permanece degenerado na lei quadrática sem relógio externo.' % review['d1']['z_recomputed'],
        'T19': '[DERIVED condicional] Γ=β/t_M dá δτ=%.12g com QNM exato arquivado; o controle BCW dá %.12g. A supressão canônica Γ=(β/2)τ★ω², τ★=t_P [PRINCIPLED IDENTIFICATION], já existe. A lei-raiz no IR recupera o coeficiente apenas para kbar=1/4 [INPUT]. Nas fontes e elos conferidos não há derivação da identificação física de τ★ ou da partição; não é prova de inexistência em todo o acervo. Nenhuma falsificação global decorre do 10^76 dimensionalmente errado.' % (exact['delta'], gw['Gamma_beta_over_tM']['delta']),
        'T20': '[KNOWN/REAL] No posterior pSEOBNR IMR de GW250114 a frequência 220 tem limite em escala de 2%% e δτ é −0,01(+0,10/−0,09), a 90%%. Ringdown isolado é menos restritivo. R-B de ensemble: mediana %.12g frente a σ amostral %.12g, correção/σ %.9g. Não é precisão de poucos por cento em todos os testes.' % (gw['delta_RB_05_50_95'][1], gw['sigma_dtau_sample_ddof1'], gw['correction_over_sample_sigma']),
        'T21': '[REAL/DERIVED condicional] Consistência do GW250114 com Kerr depende do modelo e não confirma a TGL. R-B de ensemble tem correção/σ %.9g; isso não é Bayes factor nem teste calibrado. Catálogos e GW250114 já consultados são calibração NÃO-CEGA.' % gw['correction_over_sample_sigma'],
    }
    for row in data['claims']:
        if row['id'] in corrections:
            row['previous_sentence_v1'] = row['corrected_public_sentence']
            row['corrected_public_sentence'] = corrections[row['id']]
            row['evidence'].append('independent_review_013bis')
    data.update(status='C0_CORRECTIONS_SOURCE_AUDITED__EXPLICIT_READING_AND_HISTORICAL_GAPS',
                supersedes=old.name, supersedes_sha256=sha(old),
                created_utc=datetime.now(timezone.utc).isoformat(),
                independent_review={'path': str(review_path), 'sha256': sha(review_path)},
                modular_distinctions=review['rates'],
                independent_findings=review['findings'],
                external_primary_reading_scope=review['external_primary'],
                remaining=review['unread_or_not_reobtained'])
    data['references']['independent_review_013bis'] = data['independent_review']
    lvk = ROOT/'cache/literature/gw250114_article.html'
    data['references']['lvk'].update(path=str(lvk), sha256=sha(lvk),
        locator='local HTML lines 493 and 522; primary sections read, not all supplementary proofs')
    data['references']['template']['historical_reference_mismatch'] = review['template_reference']
    data['references']['template']['scope'] = 'Historical hash retained; old C2 checks cannot be claimed byte-for-byte reproduced with current template.'
    data['references']['template_current'] = {'path': str(ROOT/'tgl_ringdown_template.py'),
        'sha256': sha(ROOT/'tgl_ringdown_template.py'), 'role': 'Current version, not historical C2 evidence'}
    opening = ROOT.parent/'TUNEL/DO_CHATGPT/ENTREGA_013BIS_ABERTURA_operador.md'
    data['opening_sha256'] = sha(opening)
    target = ROOT/'C0_AUDITORIA_v2.json'
    new(target, json.dumps(data, ensure_ascii=False, indent=2)+'\n')
    audit_md = ROOT/'bis/C0_ADVERSARIAL_SOURCE_REVIEW.md'
    text = ('[REAL/DERIVED condicional; lacunas de leitura explícitas] Adendo datado '+data['created_utc']+
        '\n\n# C0 — frases públicas corrigidas\n\nSupersedes: C0_AUDITORIA.json, SHA256 '+sha(old)+
        '. A v1 permanece intacta. Abertura do operador: '+sha(opening)+'.\n\n')
    for key, sentence in corrections.items():
        text += '## '+key+'\n\n'+sentence+'\n\n'
    text += ('## (d) — gerador unilateral, gerador bilateral e domínio\n\n'
        '[REAL — enunciados lidos, sem nova compilação] ModularFirstLaw.lean:45–58 é finito e diagonal; '
        'não assume Σp=1. Sua derivada usa −log p, mas não prova sua positividade. '
        'Com normalização de estado, −logρ≥0 é unilateral. ContinuousModularZero.lean:62–93 '
        'é outro objeto, L_h−R_h, com pares ±k; o nome contínuo não elimina Fintype. '
        'Não há ponte entre homônimos por mera nomenclatura.\n\n'
        '[KNOWN — Connes 1973, pp.133–134, fonte primária consultada pelo revisor] '
        'Um fator III₁ não admite traço normal fiel semifinito. Isso impede a representação tracial '
        'intrínseca τ(ρ·) nessa álgebra, não estados normais ou representações vetoriais. '
        'Δ positivo injetivo admite logΔ autoadjunto, possivelmente ilimitado, com domínio denso; '
        'não se deduz H_eff=0 da ausência de traço. Sorce, introdução eqs.(1)–(6), fornece '
        'o quadro modular; a prova integral não foi lida. URLs e alcance no relatório independente.\n\n'
        '[DERIVED/REAL em matriz] Γij=(β/2)(√f(ki)−√f(kj))²: f=|K| dá Γ(+3,−3)=0; '
        'f=K₊ dá Γ(+3,−3)=3β/2. Em (0,1), ambas dão β/2='+
        format(review['rates']['K_plus']['rate_0_1'],'.15g')+
        '. Unidades do parâmetro modular, não s⁻¹ sem relógio. A escolha f e os domínios '
        'ilimitados não são fixados por Tomita. A ausência de dephasing ±k vale só para esse canal.\n\n'
        'A alegada redundância universal de −i[K,ρ] tem contraexemplo; o Artigo A já a restringe '
        'a KMS/estado estacionário. Comutar fluxos não faz um deles identidade.\n\n'
        '## Evidência, custódia e limites\n\n'
        'As 64 fontes do recibo independente foram reconferidas pelo script desta correção. '
        'A cópia LVK está arquivada; o antigo ARCHIVING_PENDING foi removido do estado corrente. '
        'O template histórico citado por ef1b4d69 não coincide com o atual nem com o backup irmão; '
        'a busca exaustiva é DECLARADA pela auditoria da gerência. Os C2_TEMPLATE_CHECKS históricos '
        'não são reprodução byte a byte com a versão atual.\n\n'
        f'- C0_AUDITORIA_v2.json: {sha(target)}\n- Revisão independente JSON: {sha(review_path)}\n'
        f'- Revisão independente MD: {sha(audit_md)}\n- Fonte LVK local: {sha(lvk)}\n\n'
        'Comando: `python -B -X utf8 refeito/record_c0_013bis.py`; escrita única, recusa sobrescrever. '
        'Contas independentes: `bis/c0_review/review_numbers.py`. A revisão original discrimina '
        'fontes não lidas e falhas de acesso; não houve nova PE ou cadeia cosmológica. '
        'Axiomas: N/A — sem Lean executado. Nenhum gate alterado, nenhuma leitura física escolhida.\n')
    new(ROOT/'C0_ADENDO_FRASES_PUBLICAS.md', text)
    new(ROOT/'REAPROVEITAMENTO_C0.md',
        '[REAL — ficha de reaproveitamento; C0, 013BIS]\n\n'
        'Existia: C0_AUDITORIA.json (24 itens), verify_c0_c3.py (oráculos), cache/casa/um.py:2311 '
        '(_verb_L), :2837 (lei-raiz), :190499 (D1), :190966 (relógios), '
        'cache/casa/tgl_paper_unified.py:1983 (família Davies), :2892 (restrição KMS), '
        ':11049 (GKSL), cache/casa/ModularFirstLaw.lean:45 e ContinuousModularZero.lean:62.\n\n'
        'Reusado: verbatim e cobertura dos 24 itens, resultados e fontes congelados, 31 HDF5 '
        'reabertos pelo revisor. Novo: correções ao lado, prova matricial de não equivalência dos '
        'dissipadores, restrição de enunciados homônimos, taxas |K|/K₊ e nova aritmética D1/GW, '
        'para corrigir frases que a evidência anterior não sustentava. Fontes originais intactas.\n\n'
        'Evidência: C0_AUDITORIA_v2.json SHA256 '+sha(target)+'; revisão independente SHA256 '+
        sha(review_path)+'. Abertura SHA256 '+sha(opening)+'.\n\n'
        'Falta: derivação física de τ★/partição; README cronológico primário; prova integral das '
        'fontes III₁; recuperação da versão perdida. Isso não autoriza inferir fechamento. '
        'Falhas de acesso e de encoding preservadas no relatório. Axiomas: N/A — sem Lean.\n')
    assert old.read_bytes() == before
    for name in ('C0_AUDITORIA_v2.json','C0_ADENDO_FRASES_PUBLICAS.md','REAPROVEITAMENTO_C0.md'):
        print(name, sha(ROOT/name))

if __name__ == '__main__':
    main()
