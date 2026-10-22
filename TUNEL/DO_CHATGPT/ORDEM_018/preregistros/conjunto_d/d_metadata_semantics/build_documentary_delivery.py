"""Offline documentary mapping. Reads only local textual snapshots in this unit."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re

BASE = Path(__file__).resolve().parent
LOCAL = BASE / 'sources_local'
CHECKS = []

def check(name, passed):
    CHECKS.append({'name': name, 'passed': bool(passed)})
    if not passed:
        raise AssertionError(name)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def read_json(name):
    return json.loads((LOCAL / name).read_bytes())

def write_new(name, obj):
    data = (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    path = BASE / name
    if path.exists():
        raise FileExistsError(path)
    tmp = path.with_name(path.name + '.tmp')
    with tmp.open('xb') as f:
        f.write(data)
    check('complete write ' + name, tmp.stat().st_size == len(data))
    os.replace(tmp, path)

def main():
    capture = json.loads((BASE / 'SOURCE_CAPTURE.json').read_bytes())
    request = read_json('D_METADATA_SEMANTICS_REQUEST.json')
    contract = read_json('CONTRATO_PSD_DQ_SELECAO_D_PROPOSTA.json')
    old_sources = read_json('FONTES_E_LACUNAS.json')
    gwosc = read_json('GWOSC_METADATA_EXCERPT.json')
    public = json.loads((BASE / 'PUBLIC_DOCUMENTARY_EXCERPTS.json').read_bytes())
    for row in capture['local']:
        data = Path(row['snapshot']).read_bytes()
        check('snapshot pin ' + Path(row['snapshot']).name,
              (len(data), sha(data)) == (row['bytes'], row['sha256']))
    for key in ('source_contract', 'source_note'):
        pin = request[key]
        data = (LOCAL / Path(pin['path']).name).read_bytes()
        check('request anchor ' + key, (len(data), sha(data)) == (pin['bytes'], pin['sha256']))
    check('no opening authorized', request['opening_authorized'] is False)
    check('no model calls authorized', request['new_remote_model_calls'] is False)
    check('A/B unselected', contract['selected_alternative'] is None)
    check('DQ choice remains pending', contract['DQ_configuration']['required_quality_flags'] is None)
    check('injection choice remains pending', contract['DQ_configuration']['required_no_injection_flags'] is None)

    for row in public['sources']:
        fragment = row.get('excerpt')
        if fragment is not None:
            row['excerpt_sha256_utf8'] = sha(fragment.encode('utf-8'))
        else:
            row['facts_sha256_canonical_json_utf8'] = sha(json.dumps(row['facts'], ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8'))
        row['source_body_sha256'] = None
    source_index = {'request_id': request['request_id'], 'public_representation': public,
                    'local_source_receipt': 'SOURCE_CAPTURE.json',
                    'hash_scope': 'Local metadata snapshot bytes and selected web-rendered excerpts/facts; NOT hashes of unread remote originals, archives or science containers.',
                    'raw_http_attempts': 'All ten attempts failed with WinError10013. No escalation, archive access or payload fallback performed.'}
    write_new('FONTES_QUALIFICADAS.json', source_index)

    facts = next(r['facts'] for r in public['sources'] if r['id'] == 'o4a_dictionary_json')
    dq = sorted([r for r in facts['bits'] if r['mask'] == 0], key=lambda r:r['bit'])
    inj = sorted([r for r in facts['bits'] if r['mask'] == 1], key=lambda r:r['bit'])
    check('documented nine DQ bits', len(dq) == facts['dqbits'] == 9)
    check('documented five injection bits', len(inj) == facts['injbits'] == 5)
    check('DQ bit order', [r['bit'] for r in dq] == list(range(9)))
    check('injection bit order', [r['bit'] for r in inj] == list(range(5)))
    check('mask cadence from documentary counts', facts['duration'] == facts['npointsQI'] == 4096)
    for row in dq + inj:
        row['bit_value'] = 1 << row['bit']
        row['local_presence_verified'] = None
        if row['mask'] == 0:
            row['meaning_when_set'] = 'Dados presentes segundo DATA' if row['shortName'] == 'DATA' else 'Passa a categoria de qualidade indicada para a análise nomeada'
        else:
            row['meaning_when_set'] = 'Ausência da classe de injeção de hardware indicada'
    mapping = {
        'schema': 'TGL_D_METADATA_SEMANTICS_V1', 'request_id': request['request_id'],
        'status': 'DOCUMENTARY_SEMANTICS_QUALIFIED_LOCAL_PRESENCE_NOT_VERIFIED',
        'statute': 'KNOWN_DOCUMENTATION + DERIVED_MAPPING; no science measurement',
        'DQ_bits': dq, 'injection_bits': inj,
        'dictionary_provenance': ['o4a_dictionary_json', 'o4a_dictionary', 'o4b_dictionary', 'o4_details'],
        'mask_field_meaning': 'mask=0 denotes DQ; mask=1 denotes INJ. This field is NOT 1<<bit.',
        'applies_documentarily_to': ['O4a_4KHZ_R1', 'O4b_4KHZ_R1'],
        'bridge': 'O4 technical documentation explicitly equates O4a/O4b and 4 kHz/16 kHz flag semantics. Direct 4 kHz schema fetches via web tool failed; no local schema was inspected.',
        'DATA_semantics': {'conditions': ['ANALYSIS_READY', 'CBC_CAT1', 'BURST_CAT1'], 'source_id': 'data_flag', 'implies_no_hardware_injection': False, 'implies_stationarity': False},
        'quality_groups': 'Category levels accumulate within each analysis group, not across CBC, BURST, CW and STOCH.',
        'time_contract': {
            'documented_mask_rate_hz': 1, 'documented_bulk_duration_s': 4096, 'documented_mask_samples': 4096,
            'strain_manifest_rate_hz': 4096,
            'future_required_checks': ['Read and verify mask time origin, rate, length and exact shortname/bit dictionary for each detector.', 'Read and verify strain origin and sampling; reject fractional alignment not covered by registration.', 'Verify all intersecting seconds in both onsource and offsource windows; do not interpolate bitfields or fill missing time.', 'Reject missing flags, differing time origins, inconsistent coverage or unsupported releases.'],
            'proposed_half_open_convention': 'DQ sample k covers [t_DQ0+k*Delta_DQ, t_DQ0+(k+1)*Delta_DQ). Map strain time t by floor((t-t_DQ0)/Delta_DQ). This interval convention is a proposed reader contract, not a claim of local verification.',
            'local_origin_cadence_verified': False,
            'existing_reader_static_finding': 'strain_io.py checks integer masks, equal shape and length equal to strain duration; assumes mask origin meta/GPSstart and 1 Hz. It does not independently read mask cadence/origin attributes or validate the full dictionary against the published bit positions.'},
        'GWF_channels_only': ['{ifo}:GWOSC-4KHZ_R1_STRAIN', '{ifo}:GWOSC-4KHZ_R1_DQMASK', '{ifo}:GWOSC-4KHZ_R1_INJMASK'],
        'HDF5_reader_expected_paths_not_observed': ['strain/Strain', 'meta/GPSstart', 'quality/simple/DQmask', 'quality/simple/DQShortnames', 'quality/injections/Injmask', 'quality/injections/InjShortnames'],
        'source_channel_by_release': {'O4a_4KHZ_R1': '{ifo}:GDS-CALIB_STRAIN_CLEAN_AR', 'O4b_4KHZ_R1': '{ifo}:DCS-CALIB_STRAIN_CLEAN_AR01'},
        'channel_scope': 'Public bulk-release source identity, not direct verification of local HDF5 attributes; GWF channel names are not HDF5 group paths.',
        'calibration_release': {
            'O4a': 'C00 online, documented final public bulk product',
            'O4b': 'AR01 is C01 where available and C00 otherwise; CLEAN includes noise subtraction.',
            'documented_C01_period_GPS': [1409425408, 1415647232],
            'R1_is_not_C01': True,
            'event_specific_C00_C01_assignment': None,
            'reason_not_assigned': 'No new 14-GPS reconciliation or payload inspection in this unit.',
            'source_ids': ['o4a', 'o4b', 'o4b_alternate']},
        'selection_unchanged': contract['selection_by_metadata'],
        'required_quality_flags': None, 'required_no_injection_flags': None,
        'ratified': False, 'hold_released': False, 'scientific_containers_opened': False,
        'science_executed': False, 'remote_model_calls': 0}
    write_new('MAPEAMENTO_DQ_CALIBRACAO_D.json', mapping)

    order = contract['selection_by_metadata']['original_order']
    check('fourteen unchanged events', len(order) == len(set(order)) == 14)
    events = []
    for event in order:
        selected = [r for r in gwosc['rows'] if r['event'] == event]
        check('detector pair ' + event, len(selected) == 2 and {r['det'] for r in selected} == {'H1', 'L1'})
        matches = [(release, row['descriptor']) for release in old_sources['release_descriptors'] for row in release['D_release_file_descriptors'] if row['event'] == event]
        check('unique external PE descriptor ' + event, len(matches) == 1)
        release, descriptor = matches[0]
        zenodo = read_json(f"ZENODO_{release['record_id']}_METADATA.json")
        original = [f for f in zenodo['files'] if f['key'] == descriptor['key']]
        check('descriptor exists in pinned metadata ' + event, len(original) == 1)
        f = original[0]
        check('exact file descriptor ' + event, (f['size'], f['checksum'], f['links']['self']) == (descriptor['size'], descriptor['checksum'], descriptor['self_url']))
        check('calibration declared in metadata ' + event, 'calibration uncertainty envelopes' in zenodo['metadata']['description'])
        strains = []
        for row in selected:
            tag = re.search(r'/data/(O4[ab]_4KHZ_R1)/', row['url'])
            check('documented strain release ' + event + row['det'], bool(tag) and row['fs'] == 4096)
            strains.append({'detector': row['det'], 'descriptor_url_not_fetched': row['url'],
                'release_from_manifest_url': tag.group(1), 'rate_hz_declared': row['fs'],
                'documented_source_channel': mapping['source_channel_by_release'][tag.group(1)].replace('{ifo}', row['det']),
                'local_content_verified_this_unit': False, 'DQ_flags_present': None, 'injection_flags_present': None,
                'calibration_internal_path': None, 'calibration_epoch_GPS': None, 'calibration_frequency_coverage': None})
        events.append({'event': event, 'prior_hold_preserved': event in contract['selection_by_metadata']['four_holds_preserved'],
            'record_id': release['record_id'], 'record_url': f"https://zenodo.org/records/{release['record_id']}",
            'doi': zenodo['doi'], 'record_revision_declared': zenodo.get('revision'), 'publication_date_declared': zenodo['metadata']['publication_date'],
            'metadata_snapshot_sha256': sha((LOCAL/f"ZENODO_{release['record_id']}_METADATA.json").read_bytes()),
            'outer_PE_file_descriptor': descriptor, 'checksum_scope': 'Provider-declared MD5 of unopened outer PE file; not independently verified here.',
            'calibration_envelopes': {'existence_scope': 'Declared generally by release description only', 'analysis_label': None, 'internal_path': None,
                'exact_envelope_filename': None, 'detector_coverage': None, 'payload_hash': None, 'status': 'OPEN_NOT_OBSERVED_IN_CONTAINER'},
            'strain_descriptors': strains})
    check('all original holds preserved', [r['event'] for r in events if r['prior_hold_preserved']] == contract['selection_by_metadata']['four_holds_preserved'])
    write_new('DESCRITORES_EXTERNOS_D.json', {'request_id': request['request_id'], 'events': events,
        'GPS_reconciliation_repeated': False, 'PE_containers_opened': False, 'posterior_arrays_or_centers_read': False,
        'limit': 'Exact outer file descriptors do not resolve inner calibration paths, actual detector coverage, epochs or per-analysis convention.'})

    calibration = {'source_id': 'calibration_readme', 'DCC_document': 'LIGO-T2500288-v5',
        'document_url': 'https://dcc.ligo-wa.caltech.edu/LIGO-T2500288/public',
        'readme_version_url': 'https://dcc.ligo-wa.caltech.edu/public/0202/T2500288/005/README.txt',
        'archive_names_documented': ['LIGO_O4a_cal_uncertainty.tgz', 'LIGO_O4b_cal_uncertainty.tgz'],
        'archives_fetched_or_opened': False, 'exact_archive_payload_hashes': None,
        'filename_pattern_only': 'calibration_uncertainty_[IFO]_[GPS].txt',
        'IFO': ['H1','L1'], 'documented_cadence': 'hourly', 'epoch_rule': 'nearest GPS to analyzed event',
        'event_exact_member_names': None, 'documented_valid_frequency_range_hz': [10,5000],
        'columns_zero_based': [
            {'i':0,'quantity':'frequency','unit':'Hz'},
            {'i':1,'quantity':'median magnitude R_true/R_model','unit':'dimensionless ratio'},
            {'i':2,'quantity':'median phase R_true/R_model','unit':'rad'},
            {'i':3,'quantity':'lower -1 sigma magnitude boundary','unit':'dimensionless ratio'},
            {'i':4,'quantity':'lower -1 sigma phase boundary','unit':'rad'},
            {'i':5,'quantity':'upper +1 sigma magnitude boundary','unit':'dimensionless ratio'},
            {'i':6,'quantity':'upper +1 sigma phase boundary','unit':'rad'}],
        'convention': 'Complex multiplicative response ratio R_true/R_model; median magnitude near 1, not fractional error near 0. The documented systematic estimate remains uncorrected in released strain.',
        'not_established': ['A complete covariance across frequency/detectors', 'Gaussianity or independence of envelope columns', 'Actual envelopes for each selected file/detector/label', 'Per-file GPS coverage/gaps and exact frequency grids'],
        'low_latency_warning': 'Preliminary low-latency PE envelopes are a distinct product; do not substitute automatically.',
        'historical_link_warning': 'README points to record16053484 as an example; it does not replace the pinned17602505 release.',
        'literal_date_warning': 'README O4b prose ends January28,2024 after April10,2024; chronological typo preserved as source defect. No GPS/event reconciliation attempted; use explicit release/epochs after separate verification.',
        'frequency_scope_note': '10–5000Hz describes calibration, not the admissible bandwidth of 4096Hz strain. O4 technical docs recommend16384Hz data around1700Hz and above. No band or sampling policy changed.'}
    write_new('CALIBRACAO_DOCUMENTAL.json', calibration)

    alternatives = {
      'status':'PROPOSALS_ONLY_NO_SELECTION_CHANGED',
      'calibration_gap':[
        {'id':'CAL_A','route':'PE-container header/schema-only inventory, under separately authorized segregated reader',
         'advantage':'Can link exact analysis label and calibration product to already pinned PE release.',
         'cost_or_risk':'HDF5 header access itself is excluded now; a generic PESummary read can load posterior arrays. Never execute it to discover paths.',
         'future_receipt':'Exact observed path, detector, label, units, epoch/range, declared convention, payload provenance; no assumed conventional path.'},
        {'id':'CAL_B','route':'Independent public DCC hourly-envelope inventory and later calibration-only qualification',
         'advantage':'No need to open PE posteriors; separates calibration product from science target.',
         'cost_or_risk':'Archive inspection and numerical envelopes are not authorized in this documentary unit. Need exact member names, provider/hash/epoch coverage and agreement with C00/C01 strain.',
         'future_receipt':'Archive identity/hash, member IFO/GPS, actual grid and valid epoch, documented ratio convention, reviewed nuisance model before data.'}],
      'recommendation':'Prefer CAL_B for segregating PE information; use CAL_A if exact released PE calibration provenance is needed. Neither is completed or selected here.',
      'injection_policy_gap':[
        {'id':'INJ_A','required_if_later_ratified':['NO_CBC_HW_INJ','NO_BURST_HW_INJ','NO_DETCHAR_HW_INJ','NO_STOCH_HW_INJ'],
         'meaning':'Absence of transient/other listed injection classes; CW is not covered.',
         'condition':'Separately preregister handling of known CW lines/contamination; do not presume negligible effect.'},
        {'id':'INJ_B','required_if_later_ratified':[r['shortName'] for r in inj],
         'meaning':'Absence of all five documented hardware-injection classes.',
         'cost_or_risk':'May remove substantial observing time since LIGO had CW injections; no survival fraction measured here.'}],
      'DQ_choice':'Nine defined bits do not imply requiring all nine. CBC/ringdown policy and category threshold remain pending ratification; do not silently replace it with a BURST/CW/STOCH intersection.',
      'calibration_statistics_gap':'An amplitude/phase envelope is not a complete stochastic nuisance model. Correlation, interpolation, marginalization/correction and band must be fixed with independent justification; no independent-Gaussian prior inferred from 1-sigma boundaries.'}
    write_new('ALTERNATIVAS_E_LACUNAS.json', alternatives)

    all_outputs = ['FONTES_QUALIFICADAS.json', 'MAPEAMENTO_DQ_CALIBRACAO_D.json', 'DESCRITORES_EXTERNOS_D.json', 'CALIBRACAO_DOCUMENTAL.json', 'ALTERNATIVAS_E_LACUNAS.json']
    for name in all_outputs:
        json.loads((BASE/name).read_bytes())
        check('parse output ' + name, True)
    write_new('VALIDACAO_DOCUMENTAL.json', {'status':'PASS_DOCUMENTARY_ONLY', 'checks':CHECKS.copy(),
        'checks_passed':len(CHECKS), 'not_a_scientific_test':True,
        'scientific_containers_opened':False,'science_executed':False,'remote_model_calls':0})
    manifest_files = []
    for path in sorted(BASE.rglob('*')):
        if path.is_file() and path.name != 'MANIFESTO_ENTREGA.json' and '__pycache__' not in path.parts:
            check('text-only artifact ' + str(path.relative_to(BASE)), path.suffix.lower() in {'.py','.json','.md','.txt','.html'})
            data = path.read_bytes()
            manifest_files.append({'path':str(path.relative_to(BASE)), 'bytes':len(data), 'sha256':sha(data)})
    write_new('MANIFESTO_ENTREGA.json', {'request_id':request['request_id'], 'created_at_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
        'status':'DOCUMENTARY_UNIT_COMPLETE_WITH_EXPLICIT_LOCAL_GAPS', 'files':manifest_files,
        'shared_memories_edited':False,'selection_changed':False,'holds_changed':False,
        'D_scientific_data_opened':False,'pilot_INIT003_retried':False,'remote_model_calls':0})
    print(json.dumps({'status':'DOCUMENTARY_UNIT_COMPLETE_WITH_EXPLICIT_LOCAL_GAPS', 'documentary_checks':json.loads((BASE/'VALIDACAO_DOCUMENTAL.json').read_bytes())['checks_passed'],
        'manifest_files':len(manifest_files), 'delivery_manifest_sha256':sha((BASE/'MANIFESTO_ENTREGA.json').read_bytes()),
        'report_sha256':sha((BASE/'NOTA_D_METADATA_SEMANTICS.md').read_bytes())},ensure_ascii=False))

if __name__ == '__main__':
    main()
