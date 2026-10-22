"""Create-once non-blind C6 protocol and verifiable return-tunnel receipt."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib
import json
import lal
import numpy as np
import scipy
import h5py
from tgl_ringdown_prediction import scales

ROOT=Path(__file__).resolve().parent

def main():
    target=ROOT/'REGISTRO_C6.json'
    receipt=ROOT.parent/'TUNEL/DO_CHATGPT/ENTREGA_013_C6a_REGISTRO_TOEPLITZ.md'
    if target.exists() or receipt.exists():raise FileExistsError('C6 is create-once; use a dated amendment')
    noise=json.loads((ROOT/'C5_EMPIRICAL_NOISE.json').read_bytes())
    h_peak=1420878141.2189023
    ra,dec=2.3332345218980706,.19024356075903648
    h=lal.CachedDetectors[lal.LALDetectorIndexLHODIFF].location
    l=lal.CachedDetectors[lal.LALDetectorIndexLLODIFF].location
    shift=lal.TimeDelayFromEarthCenter(l,ra,dec,lal.LIGOTimeGPS(h_peak))-lal.TimeDelayFromEarthCenter(h,ra,dec,lal.LIGOTimeGPS(h_peak))
    files=['c6_engine.py','tgl_ringdown_prediction.py','tgl_ringdown_likelihood.py',
           'QNM_GRID.json','C5_EMPIRICAL_NOISE.json','C5_EMPIRICAL_IMR_STARTS.json',
           'C5_LIKELIHOOD_VALIDATION.json','cache/gwosc/metadata_1.json']
    files += [f"cache/empirical_noise/{d['detector']}_noise.npz" for d in noise['detectors']]
    reg=dict(status='REGISTERED_NONBLIND_BEFORE_TARGET_STRAIN',created_utc=datetime.now(timezone.utc).isoformat(),
        on_source_strain_read_at_registration=False,
        nonblind_reason='Published GW250114 posteriors and summaries already analyzed; no target-window strain downloaded/read by this task',
        event='GW250114_082203',reference_peak_GPS={'H1':h_peak,'L1':h_peak+shift},
        reference_source='Released pyRing config TEOB 0M; H1 peak and fixed sky. L1 relative delay from LAL detector geometry.',
        reference_mass_for_start_solar=68.40897469707073,
        reference_tM_seconds=scales(68.40897469707073,'CODATA2018_IAU2015')[0],reference_redshift=.086,
        start_times_tM=[6.,8.,10.,10.5,12.],primary_start_tM=10.,
        interval_samples=410,analysis_sample_rate_hz=2048,sample_stride=2,
        time_selection='First original 4096 Hz sample at or after requested start, then every second sample; no pre-onset data used in filtering',
        noise='Wholly off-source first 2048 s of previous chunk: median Welch. Exact covariance at retained sample lags, degree-2 polynomial quotient formed through spectral factors; fixed before target data.',
        quality_required=['DATA','CBC_CAT1','CBC_CAT2','CBC_CAT3'],
        injection_flags_required=['NO_CBC_HW_INJ','NO_BURST_HW_INJ','NO_DETCHAR_HW_INJ','NO_STOCH_HW_INJ'],
        likelihood='Gaussian finite-interval Toeplitz quotient, 220+440 exact Kerr fundamentals, independent complex amplitudes per detector',
        scope='Conditional ensemble ringdown model. Both modes deformed together. Mass/spin integrated with shared broad priors; independently Gaussian detector quadratures, not full polarization-coherent IMR evidence. No product with earlier analyses of this event.',
        mass_detector_prior_solar=[40.,100.],spin_prior=[0.,.95],
        prior_origin='Declared broad uniform priors, not the same-event IMR posterior',
        amplitude_prior_sd_scaled=[1.,10.,30.],primary_amplitude_sd_scaled=10.,
        amplitude_unit_strain=1e-21,amplitude_prior='Zero-mean independent real Gaussians per quadrature; analytically marginalized, determinant retained',
        computed_readings=['R-GLOBAL','R-B','R-RAIZ-0','R-LIN','R-MOD'],
        subresolution_readings={'R-A':'Same as GR within double precision at this scale; Planck source clock redshift explicit',
            'R-RAIZ-EP4':'Same as GR within double precision','R-RAIZ-REST':'Same as GR within double precision'},
        omitted_nonexponential='Root-coherent field requires occupation and Poisson-sum template; not silently replaced by an exponential',
        quadrature_grids=[[61,81],[121,161],[241,321]],quadrature_convergence_abs_lnB=.05,
        convergence_rule='Compare levels 0 and 1; if abs lnB difference exceeds 0.05, use level 2 and report remaining discrepancy. No exclusion from unconverged integral.',
        physical_gate='C5 two-family injection calibration failed: every actual-data verdict is INCONCLUSIVE_SYSTEMATICS regardless of Bayes ratio. Do not tune start times or priors to obtain an exclusion.',
        comparison_release='pyRing TEOB existing posterior at 0M; Kerr220/221/222 posteriors at 6,8,10,12M exist. No 10.5M posterior in released archive index. Different mode/prior models are controls, not identical replicated likelihoods.',
        target_downloads=[r for r in json.loads((ROOT/'cache/gwosc/metadata_1.json').read_bytes())['results'] if r['sample_rate_kHz']==4],
        versions=dict(numpy=np.__version__,scipy=scipy.__version__,h5py=h5py.__version__,lal=lal.__version__),
        code_and_input_hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in files})
    raw=json.dumps(reg,ensure_ascii=False,indent=2).encode('utf-8')
    tmp=target.with_suffix('.tmp');tmp.write_bytes(raw);assert tmp.stat().st_size==len(raw);tmp.replace(target)
    digest=hashlib.sha256(raw).hexdigest()
    body=f'''# C6a — Registro não cego antes do strain do GW250114

[REAL — protocolo registrado; não é resultado físico]

UTC: {reg['created_utc']}

Arquivo: `{target}`
SHA256: `{digest}`

Fixados: janelas 6, 8, 10 (primária), 10,5 e 12 tM; 410 amostras a 2048 Hz por seleção exata de amostras; covariância obtida antes do evento; modos 220+440; priors uniformes de massa [40,100] massas solares e spin [0,0,95]; amplitudes gaussianas próprias integradas; três escalas de prior e até três grades de quadratura. O JSON contém todas as unidades, versões e hashes.

O controle algébrico da verossimilhança passou, inclusive integral independente das amplitudes. Os controles com duas famílias IMR não satisfizeram o critério completo de viés/cobertura. Por isso, esta rodada mede a sensibilidade condicionada e tem veredito obrigatório INCONCLUSIVE_SYSTEMATICS: nenhum fator de Bayes autoriza exclusão física nesta implementação. A escolha da partição permanece aberta.

Os resultados publicados do evento já eram conhecidos. Nenhuma amostra da janela do evento foi lida ou baixada por esta tarefa até este registro. O ruído utilizado termina 317,2 segundos antes. O programa recusa registro ou código alterados e embute este hash em cada resultado.

A grade de 10,5 tM será executada, mas não há posterior pyRing nesse início no índice do release inspecionado; a lacuna não será substituída por outro tempo sem indicação.

O objetivo integral continua ativo: completar confronto, controles e pacote independente. Este recibo não move o gate.
'''.encode('utf-8')
    tmp=receipt.with_suffix('.tmp');tmp.write_bytes(body);assert tmp.stat().st_size==len(body);tmp.replace(receipt)
    print(json.dumps(dict(registration=str(target),sha256=digest,receipt=str(receipt))))

if __name__=='__main__':main()
