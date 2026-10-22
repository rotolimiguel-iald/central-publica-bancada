"""Independent higher-count repeat, retaining the validated SEOB proposal.

Own-pilot full6D and spectral-product adaptations both failed their prospective
criteria. Do not launch those proposals or relabel their diagnostics as gains.
"""
from datetime import datetime, timezone
import argparse
import copy
import json
import source_evidence as se
import run_native_seob_source as runner

STAGE = se.ROOT/'phase_native_repeat'


def register():
    proposal = runner.check()
    original_stage = runner.STAGE
    original_registration = json.loads((original_stage/'REGISTRATION.json').read_bytes())
    original_oracle = json.loads((original_stage/'PROPOSAL_ORACLE.json').read_bytes())
    for directory in ('native_proposal_crossfit', 'native_product_proposal_diagnostic'):
        result = json.loads((se.ROOT/directory/'RESULT.json').read_bytes())
        if result['prospective_refinement_allowed']:
            raise ValueError('Repeat rationale changed: an adaptive candidate passed')
    if (original_oracle['status'] != 'PASS_TRANSPORT_PROPOSAL_MOMENTS' or
            original_oracle['registration_sha256'] != se.sha(original_stage/'REGISTRATION.json')):
        raise ValueError('Original proposal oracle does not match registration')
    STAGE.mkdir(exist_ok=False)
    # Byte-identical proposal: existing normalization test remains applicable.
    raw = (original_stage/'PROPOSAL.json').read_bytes()
    temporary = STAGE/'PROPOSAL.json.part'; temporary.write_bytes(raw)
    if temporary.read_bytes() != raw:
        raise ValueError('Proposal copy changed')
    temporary.replace(STAGE/'PROPOSAL.json')
    names = list(original_registration['hashes'])
    names += ['repeat_native_source.py', 'phase_native_repeat/PROPOSAL.json',
        'phase_native_seob/REGISTRATION.json', 'phase_native_seob/PROPOSAL_ORACLE.json',
        'phase_native_seob/SEOBNRv4HM_seed130901_N2048/RESULT.json',
        'native_proposal_crossfit/RESULT.json', 'native_product_proposal_diagnostic/RESULT.json']
    reg = dict(status='REGISTERED_INDEPENDENT_NATIVE_SOURCE_REPEAT',
        date_utc=datetime.now(timezone.utc).isoformat(), family='SEOBNRv4HM',
        seed=130942, draws=16384, old_seed=130901, old_draws=2048,
        rationale='Both own-pilot proposal fits failed held-out lower-tail efficiency checks. Retain exact previous proposal and measure fresh-sample precision; no favorable adaptation selected.',
        likelihood_changed=False, physical_prior_changed=False, proposal_changed=False,
        source_parameters_integrated=7, source_parameters_sampled=6, shared_amplitudes_integrated=2,
        C6_changed=False, acceptance='Unchanged ESS>=100,maxweight<=.05,pairedMCsd<=.2, independent repeat agreement, rate control and continuous-strength bias/coverage.',
        caveat='Increasing sample count is not a guarantee of convergence; original pilot remains unaccepted.',
        hashes={n: se.sha(se.ROOT/n) for n in dict.fromkeys(names)})
    se.write(STAGE/'REGISTRATION.json', reg)
    oracle = copy.deepcopy(original_oracle)
    oracle.update(registration_sha256=se.sha(STAGE/'REGISTRATION.json'),
        reused_original_oracle='phase_native_seob/PROPOSAL_ORACLE.json',
        original_oracle_sha256=se.sha(original_stage/'PROPOSAL_ORACLE.json'),
        proposal_sha256=se.sha(STAGE/'PROPOSAL.json'), fresh_oracle_run=False,
        reuse_justification='Proposal and family transport are byte-identical to the already validated distribution')
    se.write(STAGE/'PROPOSAL_ORACLE.json', oracle)
    print(json.dumps({k: reg[k] for k in ('status', 'family', 'seed', 'draws', 'proposal_changed')}), flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('command', choices=['register', 'run'])
    p.add_argument('--processes', type=int, default=4)
    args = p.parse_args()
    if args.command == 'register':
        register()
    else:
        runner.STAGE = STAGE
        reg = json.loads((STAGE/'REGISTRATION.json').read_bytes())
        args.draws, args.seed = reg['draws'], reg['seed']
        runner.run(args)
