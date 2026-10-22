"""Register the cross-fit winner for prospective independent source draws."""
import argparse
from datetime import datetime, timezone
import json
import numpy as np
import source_evidence as se
import transport_phase_source as tp
from audit_phase_source import load_run
from diagnose_proposal_efficiency import posterior_weights
from diagnose_continuation_proposal import candidate, training_weights, PILOT, OLD_STAGE, FOLDER as DIAGNOSTIC
from run_real_phase_importance import STAGE


def fit():
    diagnostic = json.loads((DIAGNOSTIC/'RESULT.json').read_bytes())
    if not diagnostic['prospective_refinement_allowed']:
        raise ValueError('Prospective refinement criterion failed')
    dreg = json.loads((DIAGNOSTIC/'REGISTRATION.json').read_bytes())
    if diagnostic['registration_sha256'] != se.sha(DIAGNOSTIC/'REGISTRATION.json'):
        raise ValueError('Diagnostic registration changed')
    for name, expected in dreg['hashes'].items():
        if se.sha(se.ROOT/name) != expected:
            raise ValueError('Diagnostic input changed')
    selected = diagnostic['ranking'][0]
    decision = selected['rows'][0]
    result, u, logq, inside, values, stats = load_run(PILOT)
    p = posterior_weights(values, logq)
    weights = training_weights(p, decision['method'])
    with np.load(PILOT/'PROPOSALS.npz') as archive:
        y = archive['transport_y'].copy()
    old = json.loads((OLD_STAGE/'PROPOSAL.json').read_bytes())
    proposal = candidate(y[inside], weights[inside], old, decision['count'], 130970, decision['inflation'])
    proposal.update(selected=selected, training_result_sha256=se.sha(PILOT/'RESULT.json'),
        training_weight_ESS=float(1/(weights*weights).sum()), fitting_seed=130970)
    STAGE.mkdir(exist_ok=False)
    se.write(STAGE/'PROPOSAL.json', proposal)
    inherited = json.loads((OLD_STAGE/'REGISTRATION.json').read_bytes())
    names = list(inherited['hashes'])+[
        'fit_real_source_refinement.py','run_real_phase_importance.py','REAL_IMPORTANCE_RUNNER_PROVENANCE.json',
        'phase_real_refined/PROPOSAL.json','diagnose_continuation_proposal.py',
        'continuation_proposal_crossfit/REGISTRATION.json','continuation_proposal_crossfit/RESULT.json',
        'phase_ringdown_real_continuation/IMRPhenomXPHM_seed130892_N16384/RESULT.json',
        'phase_ringdown_real_continuation/IMRPhenomXPHM_seed130892_N16384/DENSITY_AUDIT.json',
        'phase_marginal_real_source.py','real_fourier_phase.py','real_phase_adapter_validation_corrected/RESULT.json']
    reg = dict(status='REGISTERED_FRESH_REAL_PHASE_PROPOSAL_REFINEMENT', date_utc=datetime.now(timezone.utc).isoformat(),
        family='IMRPhenomXPHM',seed=130972,draws=32768,selected=selected,
        physical_prior_changed=False,waveform_changed=False,likelihood_changed=False,
        solver='Same exact-source phase integral with validated real Nyquist convention',
        acceptance='Unchanged component ESS>=100,maxweight<=.05,paired MCsdlnB<=.2, repeat stability, source rate and continuous-strength calibration.',
        caution='The minimum-fold lower-tail predicted gain is small and uncertain. It is not achieved precision. Fresh samples must confirm improvement.',
        scientific_acceptance=False,C6_changed=False,
        hashes={name:se.sha(se.ROOT/name) for name in dict.fromkeys(names)})
    se.write(STAGE/'REGISTRATION.json',reg)
    print(json.dumps(dict(status=reg['status'],selected=selected['id'],seed=reg['seed'],draws=reg['draws'],
        predicted_lower_tail_gain=selected['min_fold_gain10'],training_weight_ESS=proposal['training_weight_ESS'])),flush=True)


if __name__ == '__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('command',choices=['fit','oracle']); args=parser.parse_args()
    if args.command == 'fit':
        fit()
    else:
        tp.STAGE=STAGE
        tp.oracle()
