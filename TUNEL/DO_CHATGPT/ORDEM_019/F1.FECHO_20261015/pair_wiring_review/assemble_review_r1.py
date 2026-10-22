from pathlib import Path
import datetime, hashlib, json

B = Path(__file__).resolve().parent
P = B.parent
NAMES = ['assembly_final', 'flow', 'closability', 'closed', 'symplectic', 'wedgepair', 'anti']

def pin(p):
    p = Path(p)
    b = p.read_bytes()
    return {'path': str(p), 'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}

def put(p, s):
    with p.open('x', encoding='utf-8', newline='\n') as f:
        f.write(s)

builds = []
for name in NAMES:
    f = B / name / 'RECEIPT_R1.json'
    r = json.loads(f.read_text(encoding='utf-8'))
    assert r['passed'] and r['exit_code'] == 0 and r['source_exact_copy']
    original = P / 'weyl_net_wiring' / Path(r['source']['path']).name
    assert pin(original)['sha256'] == r['source']['sha256']
    builds.append({'name': name, 'receipt': pin(f), 'source': pin(original),
                   'seconds': r['seconds'], 'print_axioms_count': r['axiom_count'],
                   'olean_identical_to_builder': r['olean_identical_to_accepted']})
audit_path = B / 'all_local/RECEIPT_R1.json'
audit = json.loads(audit_path.read_text(encoding='utf-8'))
assert audit['passed'] and audit['exit_code'] == 0
assert all(set(a) <= {'propext', 'Classical.choice', 'Quot.sound'} for a in audit['axioms'].values())
analysis = [
    {'component': 'CanonicalWeylAssembly', 'result': 'PASSA',
     'text': 'A versão final fornece dez campos por termos: R, monotonia, localidade, covariância, fluxo e suas três leis, ciclicidade e separação. Os últimos dois usam KWR concreto e D.wedge_glue. O tipo RemainingWeylInput continua premissa não habitada por este arquivo; não é construção de certificado completo.'},
    {'component': 'CanonicalWedgeFlowR2', 'result': 'PASSA',
     'text': 'A reflexão-conjugação comuta com o multiplicador de fase. O grafo do operador TW é preservado pelo boost, logo o espaço real fixo KWR é preservado. A volta usa B0(-s); a covariância concreta permite restringir Ad Gamma(B0(-2*pi*t)) à álgebra da cunha. Não se inventa a rede global nem se prova que esse fluxo é modular/KMS.'},
    {'component': 'PairTomitaClosabilityR2', 'result': 'PASSA',
     'text': 'O grafo usado é exatamente pairTomitaGraph(M,Omega). A identidade de emparelhamento segue do adjunto e da comutação M/N; estende-se à clausura por continuidade. A ciclicidade de N fornece funcionalidade da clausura, e a ciclicidade de M dá domínio denso. Essas são hipóteses explícitas no lema genérico, não conclusões assumidas no consumidor.'},
    {'component': 'PairClosedTomitaR2', 'result': 'PASSA',
     'text': 'O domínio é a projeção da clausura real do grafo, fechado por soma e multiplicação escalar com conjugação na segunda coordenada. Escolha de valor torna-se unívoca pela funcionalidade; constrói S semilinear, grafo fechado igual à clausura, domínio denso, invariância do domínio e involutividade. S(a*Omega)=a-star*Omega. Não se afirma S limitado em todo F.'},
    {'component': 'OneParticleSymplecticR2', 'result': 'PASSA',
     'text': 'TW f=Jcandidate f em KWR é deduzido da fixação de Jcandidate TW e Jcandidate^2=1. A simetria de TW no domínio efetivo, mais antiunitariedade, torna real inner(f,Jcandidate g), provando Jcandidate(KWR) contido no complemento simplético. Só inclusão é provada; não igualdade ou dualidade de Haag.'},
    {'component': 'WedgePairTomitaR2', 'result': 'PASSA',
     'text': 'Compõe as duas álgebras concretas R(K) e R(K-prime), cuja comutação e ciclicidade já foram provadas. Não há campos de ciclicidade, separação ou fechabilidade. Produz S fechado/densamente definido/involutivo do PAR concreto e sua ação nos vetores de Weyl. Standardness é a hipótese geral, com aplicação ao KWR construído.'},
    {'component': 'WeylAntiunitaryR4', 'result': 'PASSA',
     'text': 'Conjugação Gamma(j) D(f) Gamma(j)=D(jf) vem da fórmula nos exponenciais totais, conjugação da amplitude e j^2=1. Para o campo W(f)=D(if), antilinearidade muda o rótulo para -j f. A hipótese j involutiva é explícita. Trata-se de covariância antiunitária algébrica, sem identificar Gamma(j) com a polar do S do par.'}
]
reused = [pin(P / 'wedge_review/REVISAO_CUNHA_R1.json'),
          pin(P / 'weyl_review/REVISAO_WEYL_CONTINUIDADE_CAMPO_R1.json'),
          pin(P / 'exponential_review/REVISAO_EXPONENCIAIS_R1.json')]
historical = pin(B / 'assembly/RECEIPT_R1.json')
failed = pin(P / 'weyl_net_wiring/attempts/20261015T184238_432957Z/RECEIPT.json')
report = {'unit': 'F1.FECHO_20261015', 'claim': 845,
          'reviewer': 'codex-atrator-skeptic',
          'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'verdict': 'PASSA_COM_ESCOPO_COMPONENTES', 'material_findings': [],
          'builds': builds, 'all_local_audit': pin(audit_path),
          'all_local_count': audit['all_decl_count'], 'all_local_counts_by_namespace': audit['counts'],
          'source_print_axioms_count': sum(b['print_axioms_count'] for b in builds),
          'trio_only': True, 'zero_sorry_in_accepted': True,
          'mathematical_analysis': analysis, 'reused_reviews': reused,
          'historical_R3_review_build': historical, 'excluded_failed_R4': failed,
          'binary_scope': 'Identidade binária com o construtor é registrada por módulo; diferenças não são omitidas nem atribuídas a causa não medida. Fontes copiadas exatamente e declaração por declaração conferida pelo Lean.',
          'audit_method': 'Checker em arquivo separado importa só a montagem final, inspeciona env.constants.toList (inclui importados), recusa axioma local e axiomas fora do trio; não modifica fontes do construtor.',
          'scope': ['S é o Tomita fechado do par da álgebra concreta/vácuo no sentido da clausura do grafo; não há identificação das suas polares com Gamma(J) ou Gamma(Delta).',
                    'Invariância de uma cunha e restrição do fluxo não provam BW/KMS nem a rede física global.',
                    'RemainingWeylInput mantém condições analíticas/core importadas; não se reivindica habitante do FockCertificate completo, Maxwell ou H3.',
                    'As hipóteses do consumidor do par são habitadas pelo KWR e Fock concretos já construídos, com vácuo de norma um.',
                    'Integração no candidato um.py e rito integral são etapas distintas desta revisão.'],
          'management_status_changed': False, 'originals_memory_production_gate_modified': False,
          'provider_calls': False, 'script': pin(__file__)}
put(B / 'REVISAO_PAIR_WIRING_R1.json', json.dumps(report, ensure_ascii=False, indent=2) + '\n')
lines = ['# Revisão independente — fluxo da cunha e Tomita do par', '',
         '[REAL] **PASSA COM ESCOPO DE COMPONENTES**. Nenhum achado material; claim 845. O aceite da gerência permanece distinto.', '',
         '## Builds independentes', '',
         '| Fonte | EXIT | Segundos | #print axioms | .olean idêntico |',
         '|---|---:|---:|---:|---|']
for b in builds:
    lines.append(f"| {Path(b['source']['path']).name} | 0 | {b['seconds']:.3f} | {b['print_axioms_count']} | {b['olean_identical_to_builder']} |")
lines += ['', f"Checker separado: EXIT 0, {audit['all_decl_count']} declarações locais/geradas dos seis namespaces; todas no trio, nenhum axioma local, zero sorry nos aceites. Inclui importados via `env.constants.toList`. Cada recibo guarda início/fim/segundos, toolchain, comando, LEAN_PATH literal e pinos antes/depois.", '',
          'A R3 histórica foi recompilada antes da mudança de escopo. A R4 do construtor falhou e foi excluída; somente a montagem final é importada no checker. As diferenças de .olean indicadas na tabela não são ocultadas e sua causa não foi estabelecida.', '',
          '## Matemática', '']
for a in analysis:
    lines.append(f"- **{a['component']} — {a['result']}.** {a['text']}")
lines += ['', '## Alcance', ''] + ['- ' + x for x in report['scope']]
lines += ['', 'Fontes, recibos e compilações estão pinados no JSON. Originais, memória, produção e gate intactos; nenhuma chamada externa.', '']
put(B / 'REVISAO_PAIR_WIRING_R1.md', '\n'.join(lines))
print(json.dumps({'verdict': report['verdict'], 'decls': audit['all_decl_count'],
                  'prints': report['source_print_axioms_count'],
                  'json': pin(B / 'REVISAO_PAIR_WIRING_R1.json'),
                  'md': pin(B / 'REVISAO_PAIR_WIRING_R1.md')}, ensure_ascii=False))
