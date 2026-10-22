from pathlib import Path
import datetime, hashlib, json, re

B = Path(__file__).resolve().parent
P = B.parent

def pin(p):
    p = Path(p); b = p.read_bytes()
    return {'path': str(p), 'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}

def put(p, text):
    with p.open('x', encoding='utf-8', newline='\n') as f: f.write(text)

builds = []
for name in ['lift', 'positive', 'tomita']:
    rp = B / name / 'RECEIPT_R1.json'
    r = json.loads(rp.read_text(encoding='utf-8'))
    assert r['passed'] and r['exit_code'] == 0 and r['source_exact_copy']
    original = P / 'gamma_unbounded' / Path(r['source']['path']).name
    assert pin(original)['sha256'] == r['source']['sha256']
    builds.append({'name': name, 'receipt': pin(rp), 'source': pin(original),
                   'seconds': r['seconds'], 'print_axioms': r['axiom_count'],
                   'olean_identical': r['olean_identical_to_accepted'],
                   'source_theorem_count': len(re.findall(r'^\s*(?:private\s+)?theorem\s', original.read_text(encoding='utf-8'), re.M))})
ap = B / 'all_local/RECEIPT_R1.json'
audit = json.loads(ap.read_text(encoding='utf-8'))
assert audit['passed'] and audit['exit_code'] == 0
verified = {}
def verify(x):
    if isinstance(x, dict):
        if 'path' in x and 'sha256' in x:
            actual = pin(x['path']); assert actual['sha256'] == x['sha256']
            verified[x['path']] = actual
        else:
            for y in x.values(): verify(y)
    elif isinstance(x, list):
        for y in x: verify(y)
receipts = []
for name in ['FINAL_EXPONENTIAL_LIFT_RECEIPT_R1.json', 'FINAL_LIFT_POSITIVITY_RECEIPT_R1.json', 'FINAL_EXPONENTIAL_TOMITA_RECEIPT_R1.json']:
    f = P / 'gamma_unbounded' / name
    verify(json.loads(f.read_text(encoding='utf-8'))); receipts.append(pin(f))
analysis = [
    {'component': 'ExponentialLiftR2', 'result': 'PASSA',
     'text': 'O gerador do grafo é o conjunto efetivo (e(f),e(Tf)), f em D(T), seguido do span complexo e clausura no produto F×F. A hipótese geral é T auto-adjunto no H1 existente. Ela fornece densidade do domínio e emparelhamento; combinados com totalidade exponencial, provam funcionalidade da clausura. Essa funcionalidade não é campo assumido.'},
    {'component': 'Core e domínio', 'result': 'PASSA',
     'text': 'O domínio é a projeção da clausura do grafo; o valor é escolhido e provado único. O LinearPMap resultante tem grafo igual à clausura, domínio denso e simetria. core_graph_sequence aproxima simultaneamente x e o valor do operador em F×F, portanto fornece um core de grafo genuíno. A ação exponencial e cada setor são calculados por termo. Isso não prova auto-adjunção da elevação nem identidade com toda construção espectral de segunda quantização.'},
    {'component': 'ExponentialLiftPositiveR2', 'result': 'PASSA',
     'text': 'A positividade é do operador canônico, não um enunciado sobre todo T auto-adjunto. WT(rootParameter/2), já construído e auto-adjunto, fornece um fator h com (f,h) e (h,TWf) em seu grafo pelo lema WT_double_graph_iff. O emparelhamento transforma a matriz inner(e(f),e(TWg)) em Gram dos e(h). Somas finitas dão inner(x,Lx) real não negativo; o conjunto dessa desigualdade é fechado, estendendo-a à clausura do grafo.'},
    {'component': 'ExponentialTomitaR2', 'result': 'PASSA',
     'text': 'Sexp=JF composto com canonicalLift tem o domínio efetivo da elevação. A identidade TW(SWf)=Jcandidate f e a fórmula de JF nos exponenciais preservam o core por flipJ(x,y)=(JFy,JFx); conjugação dos coeficientes é tratada. Continuidade preserva a clausura. Funcionalidade dá Sexp(D) contido em D e Sexp²=I em D. A descrição do grafo como pré-imagem por (x,y)↦(x,JFy) prova fechamento; densidade é herdada. Não há hipótese de involução da elevação disfarçada de conclusão.'},
    {'component': 'Limite da identificação', 'result': 'ESCOPO_EXPLICITO',
     'text': 'Sexp é um operador construído, fechado, densamente definido e involutivo, com Sexp e(f)=e(SWf). Igualdade Sexp=S_par, auto-adjunção de canonicalLift, suas identificações polares/modulares e KMS permanecem sem prova nestes três arquivos.'}
]
base = P.parent / 'F1.REDE/modular_wedge'
support = [pin(base / 'CanonicalOutput.lean'), pin(base / 'CanonicalWedge.lean'),
           pin(P / 'wedge_review/REVISAO_CUNHA_R1.json'),
           pin(P / 'exponential_review/REVISAO_EXPONENCIAIS_R1.json')]
report = {'unit': 'F1.FECHO_20261015', 'claim': 845,
          'reviewer': 'codex-atrator-skeptic',
          'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'verdict': 'PASSA_COM_ESCOPO_OPERADORES_CONSTRUIDOS', 'material_findings': [],
          'low_findings': [], 'builds': builds, 'all_local_audit': pin(ap),
          'all_module_declarations': audit['all_decl_count'], 'counts': audit['counts'],
          'source_theorem_count': sum(b['source_theorem_count'] for b in builds),
          'print_axioms_count': sum(b['print_axioms'] for b in builds),
          'zero_sorry': True, 'trio_only': True,
          'mathematical_analysis': analysis,
          'nonvacuity': '[DERIVED] TW_selfadjoint é um termo previamente construído, não uma hipótese sem habitante. O domínio contém e(0)=Omega por exponential_mem_domain; Omega tem norma 1 na construção anterior. Não é um operador definido apenas no vetor zero.',
          'builder_receipts': receipts, 'verified_builder_pins': list(verified.values()),
          'support_sources': support, 'script': pin(__file__),
          'audit_method': 'Declarações pertencentes aos três módulos selecionadas por getModuleIdxFor? no ambiente completo, incluindo helpers privados; recusa de axioma local, sorryAx e qualquer dependência fora do trio.',
          'originals_memory_production_gate_modified': False,
          'provider_calls': False, 'management_status_changed': False}
put(B / 'REVISAO_GAMMA_R1.json', json.dumps(report, ensure_ascii=False, indent=2) + '\n')
md = ['# Revisão independente — elevação exponencial e Sexp', '',
      '[REAL] **PASSA COM ESCOPO DE OPERADORES CONSTRUÍDOS**, sem achado material. Claim 845.', '',
      '| Fonte | EXIT | Segundos | #print axioms | .olean idêntico |',
      '|---|---:|---:|---:|---|']
for b in builds:
    md.append(f"| {Path(b['source']['path']).name} | 0 | {b['seconds']:.3f} | {b['print_axioms']} | {b['olean_identical']} |")
md += ['', f"Checker independente: EXIT 0, {audit['all_decl_count']} declarações dos três módulos, incluindo auxiliares privados; apenas propext, Classical.choice e Quot.sound. Zero sorry. Logs guardam início/fim/segundos, comando, toolchain, LEAN_PATH e pinos antes/depois.", '', '## Conferência', '']
md += ['- **' + a['component'] + '** — ' + a['text'] for a in analysis]
md += ['', '## Não vacuidade e alcance', '', report['nonvacuity'], '',
       'Não se promove simetria/positividade/fechamento a auto-adjunção, nem se identifica Sexp com o Tomita do par. Os recibos anteriores e tentativas recusadas foram preservados e seus hashes conferidos. Originais, memória, produção e gate intactos; nenhuma chamada externa.', '']
put(B / 'REVISAO_GAMMA_R1.md', '\n'.join(md))
print(json.dumps({'verdict': report['verdict'], 'decls': audit['all_decl_count'],
                  'prints': report['print_axioms_count'], 'theorems': report['source_theorem_count'],
                  'json': pin(B / 'REVISAO_GAMMA_R1.json'),
                  'md': pin(B / 'REVISAO_GAMMA_R1.md')}, ensure_ascii=False))
