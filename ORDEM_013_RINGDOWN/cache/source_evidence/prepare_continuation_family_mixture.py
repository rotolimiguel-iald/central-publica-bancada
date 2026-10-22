"""Make an explicit second mixture registration, preserving the first one."""
import source_evidence as se

source = se.ROOT/'combine_source_families.py'
target = se.ROOT/'combine_continuation_families.py'
if target.exists():
    raise FileExistsError(target)
text = source.read_text()
changes = [
    ("FOLDER = se.ROOT/'source_family_combination'", "FOLDER = se.ROOT/'source_family_combination_real_repeat'"),
    ("'phase_ringdown_balanced/IMRPhenomXPHM_seed130892_N16384'", "'phase_ringdown_real_continuation/IMRPhenomXPHM_seed130892_N16384'"),
    ("'phase_native_seob/SEOBNRv4HM_seed130901_N2048'", "'phase_native_repeat/SEOBNRv4HM_seed130942_N16384'"),
    ("names = ['source_family_mixture.py', 'combine_source_families.py',", "names = ['source_family_mixture.py', 'combine_source_families.py',\n             'combine_continuation_families.py', 'CONTINUATION_FAMILY_MIXTURE_PROVENANCE.json',"),
]
for before, after in changes:
    if text.count(before) != 1:
        raise ValueError('Expected one mixture path/registration edit')
    text = text.replace(before, after)
raw = text.encode()
temporary = target.with_suffix('.py.part')
temporary.write_bytes(raw)
if temporary.read_bytes() != raw:
    raise ValueError('Incomplete mixture adapter copy')
temporary.replace(target)
se.write(se.ROOT/'CONTINUATION_FAMILY_MIXTURE_PROVENANCE.json', dict(
    original_source_sha256=se.sha(source), new_source_sha256=se.sha(target),
    edits=changes, mixture_arithmetic_changed=False, precision_criteria_changed=False,
    family_prior_changed=False, original_registration_preserved=True,
    rationale='Phenom original run terminated; use its separately validated continuation and the already registered independent SEOB repeat. Both runs remain pilots until all precision criteria pass.'))
print('New mixture paths explicit; original registration preserved.', flush=True)
