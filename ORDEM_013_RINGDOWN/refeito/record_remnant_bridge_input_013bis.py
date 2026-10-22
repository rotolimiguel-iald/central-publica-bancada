"""Read installed input metadata only; no remnant evaluation or waveforms."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
from astropy.cosmology import Planck18
B=Path(__file__).resolve().parents[1]
source=Path('/opt/lal_env/lib/python3.12/site-packages/astropy/cosmology/data/Planck18.ecsv')
cfg={'remnant_fit':'LAL_SEOBNRv4_aligned_NR_fit','cosmology_name':'Planck18_external_INPUT',
  'cosmology_source_path':str(source),'cosmology_source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
  'cosmology_parameters':{'H0_km_s_Mpc':float(Planck18.H0.value),'Om0':float(Planck18.Om0),
    'Tcmb0_K':float(Planck18.Tcmb0.value),'Neff':float(Planck18.Neff),
    'm_nu_eV':Planck18.m_nu.value.tolist(),'Ob0':float(Planck18.Ob0)},
  'scope':'External Planck18 INPUT, not fitted by this program and not a TGL derived H0. GR aligned remnant fit, not independently measured inspiral-only parameters',
  'primary_return_contract_source':'https://lscsoft.docs.ligo.org/pesummary/latest/_modules/pesummary/gw/conversions/remnant.html',
  'contract_read':'SEOBNRv4 uses LAL SimIMREOBFinalMassSpin return indices1fraction/2spin; mass fraction multiplies total input mass',
  'created_utc':datetime.now(timezone.utc).isoformat(),'producer_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
p=B/'bis/E2_REMNANT_BRIDGE_INPUT.json'
with p.open('x') as f:json.dump(cfg,f,indent=2,allow_nan=False)
print(json.dumps({'status':'METADATA_ONLY_NO_REMNANT_OR_WAVEFORM_RUN','sha256':hashlib.sha256(p.read_bytes()).hexdigest()}))
