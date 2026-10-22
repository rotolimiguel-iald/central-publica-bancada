"""Exercise the actual installed Bilby WaveformGenerator with this source."""
from pathlib import Path
import hashlib
import json
import bilby
import numpy as np
from tgl_ringdown_template import ringdown
from fetch_public import atomic_json
ROOT=Path(__file__).resolve().parent

def main():
    params=dict(mass_detector_solar=68.1,spin=.68,reading='R-B',strain_amplitude=1e-21,
                t_start=.002,phase=.3,inclination=.5,deformation=1.,redshift=.086)
    gen=bilby.gw.WaveformGenerator(duration=.125,sampling_frequency=4096,
            time_domain_source_model=ringdown,parameter_conversion=lambda p:(dict(p),[]),
            waveform_arguments={})
    report=dict(bilby_version=bilby.__version__,source_parameters=sorted(gen.source_parameter_keys),
                template_sha256=hashlib.sha256((ROOT/'tgl_ringdown_template.py').read_bytes()).hexdigest())
    try:
        got=gen.time_domain_strain(params)
        expected=ringdown(gen.time_array,**params)
        errors={key:float(np.max(np.abs(got[key]-expected[key]))/np.max(np.abs(expected[key]))) for key in expected}
        assert max(errors.values())<1e-12
        changed=dict(params,deformation=0.)
        gr=gen.time_domain_strain(changed)
        difference=float(np.linalg.norm(gr['plus']-got['plus'])/np.linalg.norm(gr['plus']))
        assert difference>1e-4
        report.update(status='PASS_ACTUAL_BILBY_CONSUMER',relative_errors=errors,deformation_effect=difference)
    except Exception as error:
        report.update(status='FAIL_ACTUAL_BILBY_CONSUMER',error=str(error))
        atomic_json(ROOT/'C3_BILBY_CONSUMER.json',report)
        print(json.dumps(report),flush=True);raise
    atomic_json(ROOT/'C3_BILBY_CONSUMER.json',report);print(json.dumps(report),flush=True)

if __name__=='__main__':main()
