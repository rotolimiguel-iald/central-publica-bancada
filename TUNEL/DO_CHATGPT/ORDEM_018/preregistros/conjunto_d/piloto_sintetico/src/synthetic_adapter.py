"""Isolated source/injection adapter. No data paths, readers, sampler or likelihood."""
import math
import numpy as np
from pseob_source import pseob_frequency_domain, parameter_conversion

FIXED={"domega220":0.0,"dtau440":0.0,"domega440":0.0}
PHYSICAL={"mass_1","mass_2","luminosity_distance","chi_1","chi_2","theta_jn","phase","ra","dec","psi","geocent_time"}
TRUTH_KEYS=PHYSICAL|set(FIXED)|{"dtau220"}
GRID={"duration_s":32.0,"sample_rate_hz":4096,"generation_sample_rate_hz":8192,
      "generation_maximum_frequency_hz":4096,"minimum_frequency_hz":20.0,
      "maximum_frequency_hz":1024.0,"reference_frequency_hz":20.0,"roll_off_s":0.4,
      "geocenter_seconds_after_segment_start":16.0}
CONFIG_KEYS={"id","mode","fixture_ids","grid","detectors","psd_kind","target_SNR","noise_seed","geometry","priors","max_native_calls"}

def validate_config(cfg):
    if set(cfg)!=CONFIG_KEYS:raise ValueError("Unknown/missing synthetic config field; paths and real event ids prohibited")
    if cfg["id"]!="ORDEM018_F3_SYNTHETIC_P0_P2" or cfg["mode"]!="SYNTHETIC_ONLY":raise ValueError("Synthetic-only contract required")
    if cfg["fixture_ids"]!=["SYN_A","SYN_B"]:raise ValueError("Only frozen synthetic fixture ids allowed")
    if cfg["grid"]!=GRID or cfg["detectors"]!=["H1","L1"]:raise ValueError("Frozen grid/detectors required")
    if cfg["psd_kind"]!="LAL_ANALYTIC_aLIGOZeroDetHighPower":raise ValueError("Analytic PSD required; no path input")
    if cfg["target_SNR"]!=20.0 or cfg["noise_seed"]!=180601 or cfg["max_native_calls"]!=32:raise ValueError("Frozen limits/seeds required")
    geom=cfg["geometry"]
    if set(geom)!={"theta_jn","ra","dec","psi","phase","geocent_time"}:raise ValueError("Geometry schema")
    if geom["geocent_time"]!=1000000000.0 or not all(np.isfinite(list(geom.values()))):raise ValueError("Synthetic GPS/geometry")
    priors=cfg["priors"]
    if set(priors)!=TRUTH_KEYS|{"mass_ratio"}:raise ValueError("Exact prior coordinate set required")
    for k,p in priors.items():
        if k in FIXED:
            if isinstance(p,bool) or not isinstance(p,(float,int)) or p!=FIXED[k]:raise ValueError("Other deformations must be fixed zero")
        else:
            if not isinstance(p,dict) or not {"kind","minimum","maximum"}<=set(p) or set(p)-{"kind","minimum","maximum","boundary"}:raise ValueError("Free-prior schema")
            if not np.isfinite([p["minimum"],p["maximum"]]).all() or p["minimum"]>=p["maximum"]:raise ValueError("Prior bounds")
    return True

def validate_truth(cfg,truth):
    validate_config(cfg)
    if set(truth)!=TRUTH_KEYS:raise ValueError("Exact truth coordinates required; no event/path metadata")
    if any(isinstance(x,bool) or not isinstance(x,(float,int)) or not math.isfinite(x) for x in truth.values()):raise ValueError("Finite numeric truth required")
    if truth["mass_1"]<=0 or truth["mass_2"]<=0 or truth["mass_2"]>truth["mass_1"]:raise ValueError("Mass ordering")
    vals=dict(truth,mass_ratio=truth["mass_2"]/truth["mass_1"])
    for k,p in cfg["priors"].items():
        if k in FIXED:
            if vals[k]!=p:raise ValueError("Fixed truth differs: "+k)
        elif not p["minimum"]<=vals[k]<=p["maximum"]:raise ValueError("Truth outside support: "+k)
    return True

def synthetic_only220(frequency_array,mass_1,mass_2,luminosity_distance,chi_1,chi_2,
                      theta_jn,phase,dtau220,dtau440=0.0,domega220=0.0,domega440=0.0,
                      geocent_time=None,**kwargs):
    if any(isinstance(x,bool) or not isinstance(x,(float,int)) or x!=0.0 for x in (dtau440,domega220,domega440)):
        raise ValueError("DTau220 must be the only nonzero deformation")
    expected={"minimum_frequency","maximum_frequency","reference_frequency","catch_waveform_errors",
              "generation_sample_rate_hz","generation_maximum_frequency_hz","analysis_time_contract"}
    if set(kwargs)!=expected:raise ValueError("Exact source keyword contract required; no override/path extras")
    if kwargs["generation_sample_rate_hz"]!=8192 or kwargs["generation_maximum_frequency_hz"]!=4096:
        raise ValueError("Qualified generation grid required")
    if kwargs["catch_waveform_errors"] is not False:raise ValueError("No silent waveform errors")
    return pseob_frequency_domain(frequency_array,mass_1,mass_2,luminosity_distance,chi_1,chi_2,
                                  theta_jn,phase,dtau220,dtau440=0.0,domega220=0.0,domega440=0.0,
                                  geocent_time=geocent_time,**kwargs)

def generator(cfg):
    import bilby
    validate_config(cfg);g=cfg["grid"];start=cfg["geometry"]["geocent_time"]-g["geocenter_seconds_after_segment_start"]
    return bilby.gw.WaveformGenerator(
        duration=g["duration_s"],sampling_frequency=g["sample_rate_hz"],start_time=start,
        frequency_domain_source_model=synthetic_only220,parameter_conversion=parameter_conversion,
        waveform_arguments={"minimum_frequency":g["minimum_frequency_hz"],"maximum_frequency":g["maximum_frequency_hz"],
            "reference_frequency":g["reference_frequency_hz"],"catch_waveform_errors":False,
            "generation_sample_rate_hz":g["generation_sample_rate_hz"],"generation_maximum_frequency_hz":g["generation_maximum_frequency_hz"],
            "analysis_time_contract":{"start_GPS":start,"duration_s":g["duration_s"],"roll_off_s":g["roll_off_s"]}})

def generate(cfg,truth):
    validate_truth(cfg,truth)
    gen=generator(cfg)
    pol=gen.frequency_domain_strain(dict(truth))
    if pol is None:raise ValueError("Source generation returned None; preserve failure")
    if set(pol)!={"plus","cross"}:raise ValueError("Polarization keys")
    return gen.frequency_array,pol

def remnant_and_rb_truth(m1,m2,chi1,chi2):
    import lal,lalsimulation as ls
    ret=ls.SimIMREOBFinalMassSpin(m1*lal.MSUN_SI,m2*lal.MSUN_SI,[0.0,0.0,chi1],[0.0,0.0,chi2],ls.SEOBNRv4)
    if len(ret)!=3 or ret[0]!=0:raise ValueError("GR remnant fit failure")
    fraction,spin=float(ret[1]),float(ret[2])
    if not np.isfinite([fraction,spin]).all() or not 0<fraction<=1 or not 0<=spin<0.98:raise ValueError("Remnant outside registered domain")
    ALPHA_FINE_CODATA_2018=7.2973525693e-3
    beta=ALPHA_FINE_CODATA_2018*math.sqrt(math.e)
    root=math.sqrt(1-spin*spin);k=4*math.pi*(1+root)/root
    F=1.5251-1.1568*(1-spin)**0.1292;Q=0.7+1.4187*(1-spin)**(-0.4990)
    x=beta*k*F*Q
    return {"fit":"LAL_SEOBNRv4_aligned_NR_fit","Mf_detector_solar":fraction*(m1+m2),"chi_f":spin,
            "beta_runtime":beta,"k":k,"F":F,"Q":Q,"x":x,"dtau220":-x/(1+x),
            "scope":"Model-derived synthetic truth, not D metadata or observed posterior"}

def analytic_psd(f,cfg):
    import lalsimulation as ls
    validate_config(cfg);mask=(f>=cfg["grid"]["minimum_frequency_hz"])&(f<=cfg["grid"]["maximum_frequency_hz"])
    p=np.full_like(f,np.inf,dtype=float)
    p[mask]=[ls.SimNoisePSDaLIGOZeroDetHighPower(float(x)) for x in f[mask]]
    if not np.isfinite(p[mask]).all() or np.any(p[mask]<=0):raise ValueError("Invalid analytic PSD")
    return p,mask

def make_ifos(cfg,f,psd,noise_kind):
    import bilby
    validate_config(cfg)
    if noise_kind not in ("ZERO","SEEDED_GAUSSIAN"):raise ValueError("Only constructed synthetic noise allowed")
    g=cfg["grid"];duration=g["duration_s"];start=cfg["geometry"]["geocent_time"]-g["geocenter_seconds_after_segment_start"]
    mask=np.isfinite(psd);rng=np.random.default_rng(cfg["noise_seed"])
    ifos=bilby.gw.detector.InterferometerList(cfg["detectors"]);noise={}
    for ifo in ifos:
        n=np.zeros_like(f,dtype=complex)
        if noise_kind=="SEEDED_GAUSSIAN":
            n[mask]=np.sqrt(duration*psd[mask]/4)*(rng.normal(size=mask.sum())+1j*rng.normal(size=mask.sum()))
        ifo.minimum_frequency=g["minimum_frequency_hz"];ifo.maximum_frequency=g["maximum_frequency_hz"]
        ifo.power_spectral_density=bilby.gw.detector.PowerSpectralDensity(frequency_array=f,psd_array=psd)
        ifo.set_strain_data_from_frequency_domain_strain(n,sampling_frequency=g["sample_rate_hz"],duration=duration,start_time=start)
        noise[ifo.name]=n.copy()
    return ifos,noise

def inject(cfg,truth,pol,ifos):
    validate_truth(cfg,truth)
    responses={i.name:i.get_detector_response(pol,truth) for i in ifos}
    before=[float(np.real(i.optimal_snr_squared(responses[i.name]))) for i in ifos]
    if not np.isfinite(before).all() or min(before)<0 or sum(before)<=0:raise ValueError("Invalid source SNR")
    factor=cfg["target_SNR"]/math.sqrt(sum(before))
    scaled={k:np.asarray(a)*factor for k,a in pol.items()}
    actual=dict(truth);actual["luminosity_distance"]/=factor;validate_truth(cfg,actual)
    snr2=[float(np.real(i.optimal_snr_squared(i.get_detector_response(scaled,actual)))) for i in ifos]
    if not np.isclose(math.sqrt(sum(snr2)),cfg["target_SNR"],rtol=1e-8,atol=1e-10):raise ValueError("SNR scaling failed")
    before_data={i.name:i.strain_data.frequency_domain_strain.copy() for i in ifos}
    signal={i.name:i.get_detector_response(scaled,actual) for i in ifos}
    for i in ifos:
        i.inject_signal(parameters=actual,injection_polarizations=scaled,raise_error=True)
        if not np.allclose(i.strain_data.frequency_domain_strain,before_data[i.name]+signal[i.name],rtol=1e-12,atol=1e-30):
            raise ValueError("Injection is not exact additive response")
    return actual,scaled,signal,{"network_optimal_SNR":math.sqrt(sum(snr2)),"scale_factor":factor,
                                "noise":"constructed synthetic only","units":"one-sided PSD strain^2/Hz; Fourier strain seconds",
                                "SNR_kind":"full IMR network optimal, not ringdown"}
