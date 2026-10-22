"""Read-only GWOSC metadata inventory; exclusive new outputs, no data-link access."""
from pathlib import Path
from datetime import datetime, timezone
import csv, hashlib, io, json, math, time

B = Path(__file__).resolve().parents[2]
C = B / 'cache/e0_metadata'
OUT = Path(__file__).resolve().parent
THRESHOLDS = [12, 30, 53, 78, 95]

def require(ok, message):
    if not ok:
        raise ValueError(message)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def read(name):
    p = C / name
    receipt = json.loads(p.with_name(p.name + '.receipt.json').read_bytes())
    require(receipt['status'] == 200 and sha(p) == receipt['sha256'], name)
    return json.loads(p.read_bytes())

def emit(name, data):
    raw = (json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode()
    with (OUT / name).open('xb') as f:
        f.write(raw)

def main():
    tick = time.perf_counter()
    current = read('gwosc_cumulative_GWTC.json')['events']
    all_versions = read('gwosc_all_event_versions.json')['events']
    latest = read('gwosc_latest_v2_page1.json')
    require(latest['next'] is None and len(latest['results']) == latest['results_count'], 'Incomplete v2 pagination')
    runs = read('gwosc_runs.json')
    require(runs['next'] is None, 'Incomplete run pagination')
    selected = {}
    for key, event in current.items():
        require(event['commonName'] not in selected, 'Cumulative duplicate')
        selected[event['commonName']] = (key, event, 'GWTC cumulative confident')
    for key, event in sorted(all_versions.items(), key=lambda kv: kv[1]['version']):
        if event['catalog.shortName'] != 'O4_Discovery_Papers':
            continue
        name = event['commonName']
        if name not in selected or selected[name][2] == 'O4 discovery supplement':
            selected[name] = (key, event, 'O4 discovery supplement')
    v2 = {e['shortName']: e for e in latest['results']}
    fields = ['mass_1_source', 'mass_2_source', 'total_mass_source', 'final_mass_source', 'redshift', 'chi_eff', 'p_astro', 'far']
    rows = []
    for name, (key, e, membership) in sorted(selected.items(), key=lambda kv: kv[1][1]['GPS']):
        rho = e.get('network_matched_filter_snr')
        require(rho is None or (type(rho) in (float, int) and math.isfinite(rho) and rho > 0), 'Bad SNR')
        matches = [r for r in runs['results'] if r['gps_start'] <= e['GPS'] < r['gps_end']]
        require(len(matches) == 1, f'Run assignment {key}: {matches}')
        run = matches[0]['name']
        if run.startswith('O4c'):
            run = 'O4c_discovery_only'
        cross = None
        if key in v2:
            params = {p['name']: p['best'] for p in v2[key]['default_parameters']}
            cross = params.get('network_matched_filter_snr') == rho
            require(cross, f'API SNR disagreement: {key}')
        row = dict(event=name, version=e['version'], version_key=key, catalog=e['catalog.shortName'],
                   membership=membership, gps=e['GPS'], run=run, network_matched_filter_snr=rho,
                   snr_convention='GWOSC preferred/default network_matched_filter_snr',
                   snr_v2_same_version_crosscheck=cross,
                   event_metadata_url=e['jsonurl'],
                   strain_links_advertised=bool(e.get('strain')), strain_downloaded_here=False,
                   final_spin=None, final_spin_available_in_default_summary=False,
                   mass_spin_inspiral_only_certified=False,
                   mass_spin_cut_applied=False, posterior_downloaded_here=False,
                   preanalysis_status='Public GR metadata before this prospective selection; not certified inspiral-only; no dtau-width selection',
                   source_status='REAL_METADATA_RETRIEVAL__PARAMETER_ESTIMATES_DECLARED_BY_GWOSC')
        for f in fields:
            row[f] = e.get(f)
            row[f + '_lower_error'] = e.get(f + '_lower')
            row[f + '_upper_error'] = e.get(f + '_upper')
            row[f + '_unit'] = e.get(f + '_unit')
        row['mass_and_effective_spin_available'] = e.get('final_mass_source') is not None and e.get('chi_eff') is not None
        row['mass_and_final_spin_available'] = False
        rows.append(row)
    def group(rs):
        return dict(n_unique=len(rs), snr_available=sum(r['network_matched_filter_snr'] is not None for r in rs),
                    thresholds={str(t): dict(count=len(sel := [r for r in rs if r['network_matched_filter_snr'] is not None and r['network_matched_filter_snr'] >= t]),
                        events=[r['event'] for r in sel],
                        strain_links_advertised=sum(r['strain_links_advertised'] for r in sel),
                        final_mass_and_chi_eff_available=sum(r['mass_and_effective_spin_available'] for r in sel),
                        final_mass_and_final_spin_available=0) for t in THRESHOLDS})
    groups = {run: group([r for r in rows if r['run'] == run]) for run in dict.fromkeys(r['run'] for r in rows)}
    groups['O4_public_total'] = group([r for r in rows if r['run'].startswith('O4')])
    groups['all_public_selected'] = group(rows)
    catalog_groups = {cat: group([r for r in rows if r['catalog'] == cat]) for cat in sorted({r['catalog'] for r in rows})}
    receipts = [json.loads(p.read_bytes()) for p in C.glob('gwosc_*.receipt.json')]
    result = dict(status='REAL_METADATA_COUNTS__NO_NEW_SCIENTIFIC_INFERENCE',
        generated_utc=datetime.now(timezone.utc).isoformat(),
        observation_snapshot=dict(start_utc=min(r['started_utc'] for r in receipts), end_utc=max(r['finished_utc'] for r in receipts), atomic=False),
        convention=dict(field='network_matched_filter_snr', estimator='GWOSC preferred/default published summary; no recomputation',
            source_priority='Cumulative official GWTC confident entry; latest version of discovery events absent from cumulative',
            deduplication='commonName, one selected version per event; O4a GWTC4.0/4.1 never added together',
            thresholds=THRESHOLDS, comparison='inclusive >= on published rounded point estimates; uncertainty not propagated',
            population='Official cumulative confident GWTC CBC + additional O4 discovery events; not an all-BBH sample',
            excluded='Marginal and third-party catalogs; no alert-only list; no posterior-width or reading-based filter',
            limitation='Preferred pipeline differs between releases/events. IMR/network SNR is not windowed ringdown SNR.',
            selected_before_sigma_fit=True, sigma_fit_performed=False, scientific_reading_selected=False),
        coverage=dict(cumulative_unique=len(current), additional_discovery=len(rows)-len(current), selected_unique=len(rows),
            all_catalog_versions=len(all_versions), all_catalog_latest_unique=latest['results_count'],
            excluded_latest_events=[r['name'] for r in latest['results'] if r['name'] not in selected],
            o4c_scope='One discovery-event window exposed by runs API, not a complete O4c catalog or live-time measure',
            strain_availability='Only advertised links; no bytes fetched or integrity/playability verified',
            final_spin='Absent from default API summaries; chi_eff is a different parameter',
            preanalysis='Metadata independent of dtau width, but GR PE summaries are not certified inspiral-only fits'),
        by_run=groups, by_selected_catalog=catalog_groups, events=rows,
        input_sha256={str(p.relative_to(B)): sha(p) for p in [C/'gwosc_cumulative_GWTC.json',C/'gwosc_all_event_versions.json',C/'gwosc_latest_v2_page1.json',C/'gwosc_runs.json',Path(__file__)]},
        elapsed_s=time.perf_counter()-tick, threads=1)
    # Compare the earlier acquisition, never import its counts as new measurements.
    historical = B.parent/'TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/E_instrumento/gwosc_catalogs_raw.json'
    old = json.loads(historical.read_bytes())
    compare = dict(status='REAL_COMPARISON_OF_TWO_ARCHIVES_NOT_NEW_ASTROPHYSICAL_MEASUREMENT', old_path=str(historical), old_sha256=sha(historical), catalogs={})
    for cat, oldrows in old.items():
        oldmap = {r[0]: r[2] for r in oldrows}
        now = {e['commonName']: e.get('network_matched_filter_snr') for e in all_versions.values() if e['catalog.shortName'] == cat}
        compare['catalogs'][cat] = dict(old_rows=len(oldrows),current_rows=len(now),added=sorted(set(now)-set(oldmap)),removed=sorted(set(oldmap)-set(now)),
            snr_changes=[dict(event=n, old=oldmap[n], current=now[n]) for n in sorted(set(now)&set(oldmap)) if now[n]!=oldmap[n]])
    emit('GWOSC_INVENTORY.json', result)
    emit('HISTORICAL_COMPARISON.json', compare)
    sio=io.StringIO(newline=''); writer=csv.DictWriter(sio,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    with (OUT/'GWOSC_EVENTS.csv').open('xb') as f:f.write(sio.getvalue().encode('utf-8'))
    emit('SNR_JOIN_FOR_A.json', dict(status='METADATA_ONLY__AWAIT_A_STANDARD_DEVIATIONS',convention=result['convention'],
        inventory_sha256=sha(OUT/'GWOSC_INVENTORY.json'), events=[{k:r[k] for k in ['event','version_key','gps','run','network_matched_filter_snr','final_mass_source','redshift','chi_eff','final_spin']} for r in rows]))
    print(json.dumps(dict(by_run={k:{t:v['count'] for t,v in g['thresholds'].items()} for k,g in groups.items()},
        o4_availability=groups['O4_public_total'],crosschecks=sum(r['snr_v2_same_version_crosscheck'] is True for r in rows)),ensure_ascii=False))

if __name__ == '__main__':
    main()
