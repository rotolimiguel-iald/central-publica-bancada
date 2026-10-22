"""Pin a source-level independent review of the concrete H1 strip and final KMS consumer."""
from pathlib import Path
import datetime, hashlib, json, re

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
OUT = BASE.parent
NAMES = ['StripPhaseBoundsR1', 'KMSStripIntegralR2', 'HalfModularStripR3',
         'CanonicalJBoostR3', 'CanonicalH1StripR3', 'WedgeOneParticleStripR2',
         'KMSBoundaryExchangeR1', 'CanonicalWedgeKMSR4']

def pin(p):
    b = p.read_bytes()
    return {'path': str(p), 'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}

def save(p, value):
    data = value.encode('utf-8') if isinstance(value, str) else value
    with p.open('xb') as f:
        f.write(data)
    assert p.read_bytes() == data

items = []
for name in NAMES:
    src = BASE / (name + '.lean')
    raw = src.read_bytes()
    assert not re.search(rb'\b(sorry|admit|axiom)\b', raw), name
    accepted = []
    for folder in (BASE / 'attempts', OUT / 'weyl_net_wiring' / 'attempts'):
        for receipt in folder.glob('*/RECEIPT.json'):
            snapshot = receipt.parent / src.name
            if not snapshot.is_file() or snapshot.read_bytes() != raw:
                continue
            meta = json.loads(receipt.read_bytes())
            if meta['exit_code'] == 0:
                accepted.append((receipt, meta))
    assert accepted, f'No accepted byte-identical build for {name}'
    receipt, meta = sorted(accepted, key=lambda pair: str(pair[0]))[-1]
    for artifact in meta['artifacts']:
        assert pin(Path(artifact['path'])) == artifact, artifact['path']
    for dep in meta.get('dependencies', []):
        assert pin(Path(dep['path'])) == dep, dep['path']
    ax = receipt.parent / 'AXIOMS.txt'
    text = ax.read_text(encoding='utf-8')
    assert 'sorryAx' not in text
    lines = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", text, re.S)
    assert lines
    assert all(set(x.strip() for x in axioms.split(',') if x.strip()) <=
               {'propext', 'Classical.choice', 'Quot.sound'} for _, axioms in lines)
    items.append({'source': pin(src), 'builder_receipt': pin(receipt),
                  'builder_exit': 0, 'builder_start': meta['start_utc'],
                  'builder_end': meta['end_utc'], 'builder_seconds': meta['seconds'],
                  'axiom_prints': len(lines), 'axioms': pin(ax),
                  'dependency_hashes_rechecked': len(meta.get('dependencies', []))})

prior = BASE / 'review_closure' / 'REVISAO_FECHO_KMS_R1.json'
finite = BASE / 'FINAL_WEYL_KMS_FINITE_RECEIPT_R1.json'
graph = OUT / 'star_graph_root_review_r1' / 'REVISAO_STAR_GRAPH_ROOT_R1.json'
review = {
    'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'author': 'codex-atrator-skeptic', 'unit': 'F1.FECHO_20261015', 'claim': 845,
    'verdict': 'PASS_WITH_STATED_SCOPE', 'material_findings': [],
    'method': 'Independent mathematical source review of parent-authored modules and byte verification of accepted builder receipts. No additional independent rebuild.',
    'independent_rebuild': False, 'sources': items,
    'axiom_prints_total': sum(x['axiom_prints'] for x in items),
    'reasoning': [
        'The signed frequency h is not assumed positive. The strip phase is exp(-i*z*h); its norm is exp(Im(z)*h), dominated on the closed strip by 1+exp(h). The interior derivative is dominated away from both edges.',
        'Bochner integration produces the strip from a measurable amplitude and an integrable exponential-moment bound. Analyticity is derived under the integral and continuity extends to both edges by the same dominator.',
        'For two vectors genuinely in the half-modular domain, Cauchy-Schwarz in L2 proves integrability of the exponential moment. No analytic-vector premise is introduced.',
        'On the unchanged canonical H1, TW_multiplier proves the half-domain identity after Phi, with canonicalSigma=4*pi^2*xi. The real edge is B0(+2*pi*t), derived from the existing Fourier convention.',
        'Jcandidate commutes with B0 because rapidity reflection and complex conjugation cancel the character signs. The proof acts on the actual L2 classes and uses AE measure-preserving reflection.',
        'KWR membership supplies TW f=Jcandidate f, so antiunitarity and boost inversion give the exchanged upper boundary. KMSBoundaryExchange is a Hilbert-space identity, not an assumed KMS certificate.',
        'The final consumer uses simultaneous closure of (A Omega,A* Omega) for each argument, and the previously reviewed strip maximum/uniform closure. It obtains the full KMSBody for the actual von Neumann wedge algebra, not just the Weyl generators.'
    ],
    'authorship_and_reuse': {
        'prior_generic_closure_review': pin(prior),
        'finite_weyl_branch': pin(finite),
        'star_graph_root_independent_review': pin(graph),
        'disclosure': 'The reviewer constructed the finite Weyl branch and part of star-graph density. This review is independent only for the parent-authored H1 strip, exchange and final composition. It does not represent self-review as independent review of those transitive components.'
    },
    'scope': 'A concrete bounded KMSBody at strip height 1 for Gamma(B0(+2*pi*t)) on the canonical standard wedge and the same Fock/vacuum. The distinct equality of the actual modular CFC flow with Gamma(B0(-2*pi*t)), the full global net and a joint certificate inhabitant are not conclusions of this consumer.',
    'production_modified': False, 'gate_changed': False
}
save(HERE / 'REVISAO_KMS_CONCRETO_R1.json', json.dumps(review, ensure_ascii=False, indent=2) + '\n')
save(HERE / 'REVISAO_KMS_CONCRETO_R1.md',
     '# Revisão da faixa concreta e da composição KMS\n\n'
     '[REAL — revisão matemática de fontes e conferência dos recibos] PASSA no alcance declarado.\n\n'
     f'Oito módulos lidos; {review["axiom_prints_total"]} impressões dos builds aceitos ficam somente no trio. '
     'Os hashes das fontes, snapshots, artefatos e dependências foram relidos. Esta rodada não recompilou independentemente.\n\n'
     'A dominância exponencial vem dos dois domínios reais de TW. Não se pressupõe vetor analítico. '
     'A transformada com frequência assinada produz analiticidade interior e continuidade no fecho; '
     'a convenção de Fourier identifica o bordo inferior com B0(+2πt). A condição fixa de KWR, '
     'a antiunitariedade de J e o inverso do boost dão o bordo superior trocado.\n\n'
     'A composição final usa densidade conjunta de (AΩ,A*Ω), em ambos os argumentos, e o fecho de faixas já revisado. '
     'Conclui o KMSBody da álgebra concreta da cunha, com Γ(B0(+2πt)) e altura 1. '
     'A igualdade com o fluxo CFC de sinal negativo é outra obrigação, não consequência declarada deste consumidor.\n\n'
     'Independência delimitada: a revisão cobre os módulos da raiz; o revisor construiu o ramo Weyl finito '
     'e parte da densidade de grafos. Esta última tem revisão independente da raiz citada no JSON. '
     'Nenhum achado material; nada canônico ou gate alterado.\n')
print(json.dumps(pin(HERE / 'REVISAO_KMS_CONCRETO_R1.json')))
