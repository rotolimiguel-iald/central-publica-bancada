"""Prepared initialization alternatives. Never evaluates a waveform or likelihood."""
import hashlib
from pathlib import Path

def verify_file(row):
    path=Path(row["runtime_path"])
    raw=path.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=row["sha256"] or len(raw)!=row["bytes"]:
        raise ValueError("Exact initialization dependency changed: "+str(path))
    return path

def build_A(bilby,f,psd,geometry,expected):
    # No factory/eval/default noise curve. Geometry was extracted by restricted AST.
    if [r["name"] for r in geometry["detectors"]]!=["H1","L1"]:
        raise ValueError("Only pinned H1/L1 geometry")
    ifos=[]
    for row in geometry["detectors"]:
        kw=dict(row["parsed_parameters"])
        kw.update(minimum_frequency=20.,maximum_frequency=1024.)
        density=bilby.gw.detector.PowerSpectralDensity(frequency_array=f,psd_array=psd)
        ifos.append(bilby.gw.detector.Interferometer(power_spectral_density=density,**kw))
    return bilby.gw.detector.InterferometerList(ifos),[]

def build_B(bilby,f,psd,geometry,expected):
    # Exactly one pinned installed curve, demanded by both official configs.
    curve=verify_file(expected)
    if Path(curve.name).exists():
        raise ValueError("A local file could shadow the pinned installed default curve")
    ifos=bilby.gw.detector.InterferometerList(["H1","L1"])
    before=[]
    for ifo in ifos:
        density=ifo.power_spectral_density
        if Path(density.asd_file).resolve()!=curve.resolve():
            raise ValueError("Factory used another default curve")
        before.append({"detector":ifo.name,"asd_file":str(curve),"sha256":expected["sha256"]})
        ifo.minimum_frequency=20.;ifo.maximum_frequency=1024.
        replacement=bilby.gw.detector.PowerSpectralDensity(frequency_array=f,psd_array=psd)
        ifo.power_spectral_density=replacement
        if ifo.power_spectral_density is density or ifo.power_spectral_density is not replacement:
            raise ValueError("Analytic replacement did not take effect")
    return ifos,before

def verify_analytic_state(np,ifo,f,psd,geometry):
    density=ifo.power_spectral_density
    if density.asd_file is not None or density.psd_file is not None:
        raise ValueError("File-backed PSD survived replacement")
    if not np.array_equal(density.frequency_array,f) or not np.array_equal(density.psd_array,psd):
        raise ValueError("Analytic PSD arrays differ from qualified synthetic archive")
    if not np.array_equal(ifo.power_spectral_density_array,psd):
        raise ValueError("Effective likelihood PSD differs from analytic PSD")
    if not np.array_equal(ifo.frequency_array,f):raise ValueError("Detector frequency grid differs")
    if ifo.minimum_frequency!=20. or ifo.maximum_frequency!=1024.:raise ValueError("Analysis band differs")
    if ifo.duration!=32. or ifo.sampling_frequency!=4096. or ifo.start_time!=999999984.:
        raise ValueError("Synthetic timing differs")
    if ifo.strain_data.window_factor!=1 or len(ifo.strain_data.notch_list)!=0:
        raise ValueError("Unexpected strain window/notches")
    row=next(x for x in geometry["detectors"] if x["name"]==ifo.name)
    for key,value in row["parsed_parameters"].items():
        if key not in ("name","minimum_frequency","maximum_frequency") and not np.isclose(getattr(ifo.geometry,key),value,rtol=0,atol=1e-10):
            raise ValueError("Geometry changed: "+key)
    # Force lazily computed in-memory geometry now, never a detector response/waveform.
    for vector in (ifo.geometry.vertex,ifo.geometry.x,ifo.geometry.y,ifo.geometry.detector_tensor):
        if not np.isfinite(vector).all():raise ValueError("Geometry is not finite")
    return {"detector":ifo.name,"frequency_sha256":hashlib.sha256(f.tobytes()).hexdigest(),
            "PSD_raw_sha256":hashlib.sha256(psd.tobytes()).hexdigest(),
            "PSD_effective_sha256":hashlib.sha256(ifo.power_spectral_density_array.tobytes()).hexdigest(),
            "no_file_backed_PSD":True,"duration_s":ifo.duration,"sampling_frequency_Hz":ifo.sampling_frequency,
            "start_time":ifo.start_time,"strain_window_factor":ifo.strain_data.window_factor,
            "detector_roll_off_s_unchanged_from_Bilby":ifo.strain_data.roll_off}
