"""Analytic review; does not compile Lean or modify any candidate or canonical file."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os

BASE = Path(__file__).resolve().parent
REDE = BASE.parent
KERNEL = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')

def pin(p):
    b = p.read_bytes()
    return {'path': str(p), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

sources = [
    REDE / 'sources/BGL_2002_v2.pdf',
    REDE / 'sources/PUBLIC_PRIMARY_CUSTODY_R1.json',
    KERNEL / 'TGLExt/TheImportedSecondQuantization.lean',
    KERNEL / 'TGLExt/O16/OrbitalMeasureSupport_v2.lean',
    KERNEL / 'TGLExt/O16/OrbitTranslationFaithfulness_v2.lean',
    KERNEL / 'TGLExt/O16/OrbitalTranslationOperators_v2.lean',
    KERNEL / 'TGLExt/O16/OrbitalRapidityMeasure_v4.lean',
    REDE / 'fiber_conjugation/GeometricFiberConjugation.lean',
    REDE / 'fubini/FubiniL2.lean',
]
custody = json.loads(sources[1].read_bytes())
assert pin(sources[0])['sha256'] == next(x['sha256'] for x in custody if x['path'] == str(sources[0]))
review = {
    'unit': 'F1.REDE',
    'created_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
    'reviewer': 'codex-takesaki-local-lemmas',
    'verdict': 'PASSA_ANALITICO_COM_CONVENCOES_EXPLICITADAS',
    'status': 'DERIVED_ANALYTIC_REVIEW; BGL_CONSEQUENCES_KNOWN; NOT_A_LEAN_CERTIFICATE',
    'scope': 'Massless helicity +1/-1 induced representation and wedge modular localization on the same canonical H1',
    'sources': [pin(p) for p in sources],
    'bibliography': {'authors': 'Brunetti, Guido, Longo', 'title': 'Modular localization and Wigner particles', 'version': 'arXiv:math-ph/0203021v2, 18 June 2002', 'url': 'https://arxiv.org/pdf/math-ph/0203021v2'},
    'conventions': [
        'Metric eta=diag(1,-1,-1,-1); translation phase exp(i eta(a,p)); Bx(t) uses positive sinh off diagonal.',
        'Proper orthochronous Lorentz group SO+(1,3), extended to the proper group by antiunitary spacetime inversion. Integer helicities +1/-1 descend to this group.',
        'rho=sqrt(q2^2+q3^2)>0; p=(rho cosh r,rho sinh r,q2,q3); k*=(1,0,0,1).',
        'Rx(phi)e3=(0,-sin(phi),cos(phi)) with cos(phi)=q3/rho, sin(phi)=-q2/rho. Define the rotation matrix directly from these coordinates, avoiding a branch-dependent angle.',
        'zeta is the unit-complex character of the SO(2) rotational quotient of ISO(2); its two translations act trivially. It is not a character of a full O(2) stabilizer.',
    ],
    'checks': [
        {'id': 'SECTION', 'result': 'PASSA', 'status': 'DERIVED', 'calculation': 'Bz(log rho)k*=rho k*. Rx(phi) sends rho e3 to (0,q2,q3). Bx(r) yields exactly p. Therefore s(p)k*=p.', 'null_set_clarification': 'At q=0, rho/r are unavailable. Either define operators a.e. with an explicit null-set convention, or complete s on p=(E,+/-E,0,0) by Ry(+/-pi/2)Bz(log E). The cone vertex has zero measure and is excluded from the positive mass shell.'},
        {'id': 'COCYCLE', 'result': 'PASSA', 'status': 'DERIVED', 'calculation': 'c(L,p) fixes k*, because s(L^-1 p)k*=L^-1 p. Inserting s(L1^-1 p)s(L1^-1 p)^-1 proves c(L1 L2,p)=c(L1,p)c(L2,L1^-1 p). D=diag(zeta,conj zeta) is a unitary representation of that stabilizer; D(c) therefore obeys the same law.'},
        {'id': 'MEASURE', 'result': 'PASSA', 'status': 'DERIVED', 'calculation': 'Canonical shell coordinates have measure dq2 dq3 dp1/E. The change p1=rho sinh r has dp1=E dr, hence the rapidity measure is dq2 dq3 dr. Under an axial boost the spatial Jacobian is Eprime/E; rotations have Jacobian 1. Rotations and boosts generate SO+(1,3), establishing invariance of dp/E. The factor 2 relative to dp/(2E) is an invariant constant.', 'source_anchor': 'OrbitalRapidityMeasure_v4.lean:21-28; OrbitalMeasureSupport_v2.lean:47-49'},
        {'id': 'REPRESENTATION', 'result': 'PASSA', 'status': 'DERIVED', 'calculation': 'Unitarity follows from D(c) unitary and invariant measure. The cocycle plus eta(b,L^-1p)=eta(Lb,p) gives U(a,L)U(b,M)=U(a+Lb,LM). Positive-energy spectrum is the future null shell. Strong continuity follows first on continuous compactly supported vectors away from q=0 using the continuous rotation matrix and dominated convergence, then on all H1 by density and unitarity; no globally smooth angular branch is needed.', 'canonical_match': 'Fib=EuclideanSpace complex (Fin 2), H1=Lp Fib 2 orbitalMeasure(0), and orbitPairing is precisely (+---). Thus the translation subgroup is the existing U1, not a new scalar product or measure.'},
        {'id': 'BOOST', 'result': 'PASSA', 'status': 'DERIVED', 'calculation': 's(Bx(t)p)=Bx(t)s(p) because q and rho stay fixed and r changes to r+t. Hence c(Bx(t),p)=I and U(0,Bx(t))f(q,r)=f(q,r-t), exactly the convention of B0 and productRapidityShift.'},
        {'id': 'ROTATION', 'result': 'PASSA', 'status': 'DERIVED', 'calculation': 'Rx(pi) commutes with Bx(r) and sends q to -q, preserving rho. Rx(phi(-q))=Rx(phi(q)-pi) as an SO(2) matrix. Thus c(Rx(pi),p)=I a.e. and U(Rx(pi)) pulls back q to -q. If working on the double cover, central 2pi factors may occur in a lifted section but act trivially for helicities +/-1.'},
        {'id': 'THETA', 'result': 'PASSA', 'status': 'DERIVED', 'calculation': 'Let P swap the two components. Theta=P complex_conjugation. P conj(D(c)) P=D(c); hence Theta commutes with the Lorentz subgroup. It conjugates exp(i eta(a,p)) to exp(-i eta(a,p)), so Theta U(a) Theta=U(-a), and Theta^2=I. The helicity pair is essential: a single nonzero-helicity summand cannot use this same involution.'},
        {'id': 'WEDGE_REFLECTION', 'result': 'PASSA', 'status': 'DERIVED', 'calculation': 'Write R=Rx(pi)=diag(1,1,-1,-1). J=U(R)Theta acts as swap(conj f(p0,p1,-q)), is antiunitary, and J^2=U(R^2)=I. J U(a,L) J=U(-Ra,RLR)=U(jW a,jW L jW), with jW=-R=diag(-1,-1,1,1). In particular, edge translations are preserved rather than inverted, explaining why omitting q reflection is geometrically wrong.'},
        {'id': 'MODULAR_AND_LOCALIZATION', 'result': 'PASSA_ANALYTIC_KNOWN_APPLICATION', 'status': 'DERIVED + KNOWN', 'calculation': 'Delta^(it)=B0(-2pi t) matches BGL right-wedge convention. J commutes with this unitary group but is antiunitary, so J(log Delta)J=-log Delta and J Delta J=Delta^-1. The spectral calculus defines positive nonsingular Delta with dense-domain Delta^(1/2), and S=J Delta^(1/2) is a closed dense antilinear involution. K=Fix(S) is standard. Covariance fixes K(gW) independently of the representative g; positive energy then gives isotony and wedge duality gives locality.', 'bgl_anchors': ['PDF p.4 convention and Proposition 2.1', 'PDF p.5 Propositions 2.2-2.4', 'PDF p.6 Theorem 2.5 and Remark 2.6', 'PDF p.8 Theorem 3.4 and Corollary 3.5'], 'formalization_boundary': 'These BGL applications are cited mathematical results and this review is a written derivation. They are not newly compiled Lean terms for the 4D representation or net.'},
        {'id': 'PHASE', 'result': 'PASSA_WITH_EXPLICIT_CHOICE', 'status': 'DERIVED', 'calculation': 'The chosen real swap fixes a convention. Replacing J by exp(i chi)J preserves involutivity and covariance but replaces K by exp(i chi/2)K. It is a unitarily equivalent net, not equality of the original subspace. For this single +/-1 pair an involutive swapping antiunitary requires the same off-diagonal phase on both components. BGL irreducible uniqueness wording must not be applied verbatim to the reducible doublet.', 'bgl_anchor': 'PDF pp.6-7, Remark 2.6'},
    ],
    'critical_warning': 'Do not infer geometrical localization merely from J^2=I and J Delta J=Delta^-1. The full relation J U(a,L) J=U(jW a,jW L jW), the positive-energy representation, and its match to the canonical B0 are the indispensable bridges.',
    'open_formal_work': ['Implement the full Lorentz little-group cocycle and its representation on canonical H1 in Lean.', 'Prove its equality with the chosen local candidate J and the existing translation and boost operators.', 'Import or formalize the localization theorem under its exact hypotheses.'],
    'not_claimed': ['New Lean proof of the 4D net', 'Interacting quantum gravity', 'Curved-spacetime net', 'Hardware or finite-device refinement', 'Experimental confirmation or gate change'],
    'production_changed': False,
    'script': pin(Path(__file__)),
}
p = BASE / 'REVIEW_R1.json'
b = (json.dumps(review, ensure_ascii=False, indent=2) + '\n').encode()
with p.open('xb') as f:
    f.write(b)
    f.flush()
    os.fsync(f.fileno())
assert p.read_bytes() == b
print(json.dumps(pin(p), ensure_ascii=False))
