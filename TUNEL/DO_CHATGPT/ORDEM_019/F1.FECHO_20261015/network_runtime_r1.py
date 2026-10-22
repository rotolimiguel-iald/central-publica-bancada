"""Consume actual kernel evidence for the constructed Fock network components."""


def rede_fock_v394(core):
    """Check this run's proof reports and exact embedded sources.

    Success certifies the listed mathematical components. It does not supply
    an inhabitant of RemainingWeylInput, identify its polar factors, or assert
    a physical realization of the global net, stress tensor, or all-wedge H3.
    No nature gate or pre-existing verdict is changed.
    """
    import hashlib
    contract = _V394_NETWORK_CONTRACT
    report = core.get('kernel_formalization') or {}
    ladder = core.get('external_ladder') or {}
    axioms = report.get('axiom_report') or {}
    trio = {'propext', 'Classical.choice', 'Quot.sound'}
    declarations = {}
    for name in contract['declarations']:
        values = axioms.get(name)
        declarations[name] = (isinstance(values, list)
                              and all(isinstance(v, str) for v in values)
                              and set(values) <= trio)
    sources = {}
    for path, expected in contract['source_sha256'].items():
        body = _EMBEDDED_KERNEL_FILES.get(path)
        sources[path] = (isinstance(body, str)
                         and hashlib.sha256(body.encode('utf-8')).hexdigest() == expected)
    counts = [ladder.get('n_theorems_clean'), ladder.get('n_theorems_expected'),
              contract['expected_ladder']]
    exact = all(type(v) is int for v in counts) and len(set(counts)) == 1
    passed = (report.get('all_verified') is True and exact
              and bool(declarations) and all(declarations.values())
              and bool(sources) and all(sources.values())
              and (core.get('regra_quadratica_v394') or {}).get('all_verified') is True)
    result = dict(all_verified=passed, formal_declarations=declarations,
                  embedded_sources=sources, exact_ladder=exact,
                  constructed_components=contract['constructed_components'],
                  open_joint_contract=contract['open_joint_contract'],
                  whole_certificate_inhabited=False,
                  scope='Verified Fock and standard-wedge components with the remaining joint analytic contract explicit.',
                  does_not_gate_core=True)
    result['verdict'] = ('TGL_FOCK_NETWORK_V394__DERIVED_COMPONENTS__JOINT_CONTRACT_OPEN__GATE_UNMOVED'
                         if passed else 'TGL_FOCK_NETWORK_V394__REFUSED_FORMAL_OR_SOURCE_EVIDENCE__GATE_UNMOVED')
    core['rede_fock_v394'] = result
    return result
