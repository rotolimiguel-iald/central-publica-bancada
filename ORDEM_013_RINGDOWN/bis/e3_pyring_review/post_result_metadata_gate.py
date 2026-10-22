"""Pure metadata predicates; no output discovery, sampler, or posterior I/O."""
import copy
import json
import math

ACCEPTED = 'CONVERGENCE_CRITERIA_MET_REQUIRES_INDEPENDENT_REVIEW'


def finite(value, low=0):
    return type(value) in (int, float) and math.isfinite(value) and value >= low


def integer(value, low=0):
    return type(value) is int and value >= low


def evaluate(metadata, settings):
    """No science acceptance: true means metadata prerequisite passed only.

    Caller must independently verify custody, timings, raw terminal state and
    nested weights using the pinned protocol before inspecting accepted samples.
    Missing fields and malformed structures refuse, including under python -O.
    """
    issues = []
    def require(condition, label):
        if condition is not True:
            issues.append(label)
    try:
        launch = metadata['launch']
        controller = metadata['controller']
        convergence = metadata['convergence']
        cost = convergence['cost']
        require(launch['status'] == 'COMPLETED_REVIEW_PENDING', 'outer_status')
        require(type(launch['returncode']) is int and launch['returncode'] == 0, 'outer_returncode')
        require(launch['error'] is None, 'outer_error')
        require(controller['variant'] == 'public_psd', 'variant')
        require(controller['status'] == 'COMPLETED_REQUIRES_REVIEW', 'controller_status')
        require(type(controller['returncode']) is int and controller['returncode'] == 0, 'controller_returncode')
        require(controller['cutoff'] is False, 'cutoff')
        require(controller['cleanup']['group_absent'] is True, 'cleanup')
        require(metadata['failure_file_present'] is False, 'failure_file')
        require(metadata['partial_status_file_present'] is False, 'partial_status_file')
        require(convergence['status'] == ACCEPTED, 'convergence_status')
        require(convergence['accepted_for_analysis'] is True, 'accepted_flag')
        require(convergence['before_add_live'] is True, 'pre_live_evidence')
        require(finite(convergence['delta_logz']) and convergence['delta_logz'] < settings['dlogz'], 'delta_logz')
        require(type(convergence['threshold']) in (int, float) and convergence['threshold'] == settings['dlogz'], 'threshold')
        require(integer(convergence['ncall'], 1) and convergence['ncall'] < settings['maxcall'], 'maxcall')
        require(integer(convergence['ncall_reported'], 1) and convergence['ncall_reported'] == convergence['ncall'], 'ncall_reported')
        require(finite(convergence['ess'], settings['minimum_effective_samples']), 'ess')
        require(convergence['minimum_ess'] == settings['minimum_effective_samples'], 'minimum_ess')
        require(integer(convergence['posterior_samples'], settings['minimum_posterior_samples']), 'posterior_samples')
        require(type(convergence['log_evidence']) in (int, float) and math.isfinite(convergence['log_evidence']), 'finite_evidence')
        require(finite(convergence['log_evidence_err']), 'finite_evidence_error')
        require(integer(cost['likelihood_calls'], 1), 'likelihood_calls')
        require(integer(cost['likelihood_calls_after_sampler_constructor']), 'setup_calls')
        require(cost['likelihood_calls'] >= cost['likelihood_calls_after_sampler_constructor'], 'counter_order')
        require(integer(cost['sampler_ncall'], 1) and cost['sampler_ncall'] == convergence['ncall'], 'sampler_counter')
        require(cost['maxcall_nominal'] == settings['maxcall'], 'maxcall_pin')
        require(type(cost['workers']) is int and cost['workers'] == 1, 'workers')
        require(finite(cost['wall_seconds']) and finite(cost['parent_cpu_seconds']), 'cost_finite')
    except (KeyError, TypeError, ValueError, OverflowError) as error:
        issues.append('invalid_or_missing_metadata:' + type(error).__name__)
    return {'status': 'METADATA_PREREQUISITE_ONLY' if not issues else 'NO_ACCEPTED_POSTERIOR_ANALYSIS',
            'issues': issues, 'posterior_read': False, 'science_accepted': False}


def self_test():
    settings = dict(dlogz=.1, maxcall=3000000, minimum_effective_samples=100, minimum_posterior_samples=1000)
    base = dict(launch=dict(status='COMPLETED_REVIEW_PENDING', returncode=0, error=None),
                controller=dict(variant='public_psd', status='COMPLETED_REQUIRES_REVIEW', returncode=0,
                                cutoff=False, cleanup=dict(group_absent=True)),
                failure_file_present=False, partial_status_file_present=False,
                convergence=dict(status=ACCEPTED, accepted_for_analysis=True, before_add_live=True,
                                 delta_logz=.05, threshold=.1, ncall=2000000, ncall_reported=2000000,
                                 ess=200., minimum_ess=100, posterior_samples=1500,
                                 log_evidence=-100., log_evidence_err=.2,
                                 cost=dict(likelihood_calls=2000100, likelihood_calls_after_sampler_constructor=100,
                                           sampler_ncall=2000000, maxcall_nominal=3000000, workers=1,
                                           wall_seconds=800., parent_cpu_seconds=790.)))
    cases = [('synthetic_metadata_only', base, True)]
    mutations = [
        ('launch.status', 'FAILED_OR_PARTIAL'), ('launch.returncode', 1), ('launch.returncode', False),
        ('launch.error', {}), ('controller.variant', 'welch'), ('controller.cutoff', True),
        ('controller.cleanup.group_absent', False), ('controller.cleanup.group_absent', 1),
        ('failure_file_present', True), ('partial_status_file_present', True),
        ('convergence.status', 'PARTIAL_MAXCALL_NOT_ACCEPTED'), ('convergence.accepted_for_analysis', False),
        ('convergence.before_add_live', False), ('convergence.before_add_live', 1),
        ('convergence.delta_logz', .1), ('convergence.delta_logz', float('nan')),
        ('convergence.ncall', 3000000), ('convergence.ncall_reported', 1),
        ('convergence.ess', 99.9), ('convergence.posterior_samples', 999),
        ('convergence.posterior_samples', True), ('convergence.log_evidence', float('inf')),
        ('convergence.log_evidence_err', -1), ('convergence.cost.likelihood_calls', -1),
        ('convergence.cost.likelihood_calls_after_sampler_constructor', 3000000),
        ('convergence.cost.sampler_ncall', 1), ('convergence.cost.workers', 2),
        ('convergence.cost.wall_seconds', float('nan')),
    ]
    for key, value in mutations:
        item = copy.deepcopy(base)
        parts = key.split('.')
        target = item
        for part in parts[:-1]:
            target = target[part]
        target[parts[-1]] = value
        cases.append((key + ':' + repr(value), item, False))
    cases.append(('missing_fields', {}, False))
    results = []
    for name, metadata, expected in cases:
        result = evaluate(metadata, settings)
        passed = (not result['issues']) == expected and result['science_accepted'] is False
        if not passed:
            raise RuntimeError('Fixture failed: ' + name)
        results.append(dict(name=name, passed=passed, issues=result['issues']))
    return results


if __name__ == '__main__':
    # Deliberately no live-output argument or auto-discovery. Only synthetic tests.
    print(json.dumps(dict(status='PREPARED_INACTIVE_SYNTHETIC_ONLY', checks=self_test(),
                          posterior_read=False, scientific_execution=False), allow_nan=False))
