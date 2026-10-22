"""Exclusive pre-registration; this script does not run the synthetic tests."""
from pathlib import Path
import datetime, hashlib, json
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent.parent
def pin(p):
    p=Path(p); return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def new(p,obj):
    with Path(p).open('xb') as f: f.write((json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode())
decoder=BASE/'mission_audit_r62'/'run_prepared_readout_r62_r2.py'
sources=[decoder,BASE/'calibration_r65'/'calibration'/'CONTRATO_CALIBRACAO_R65.md',BASE/'calibration_r65'/'IDENTIFIABILITY_COMPLETION_R65.txt',BASE/'output_field_r64'/'output'/'CONTRATO_OUTPUT_R64.md',BASE/'anchored_contour_r68'/'ADENDO_R68_CORRESPONDENCIA_INTEGRAL.md']
plan={'status':'PREREGISTERED_SYNTHETIC_ONLY','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'tolerance':1e-12,'source_pins':[pin(p) for p in sources],'decoder_source':pin(decoder),
 'calibration':{'kind':'SYNTHETIC_INPUT','J0':'a_o_dag*sigma_minus + sigma_plus*a_i; ordered=(i,o,OH); unit_coefficients','time_unit':'s','rate_unit':'s^-1','quadrature_unit':'dimensionless','t0_seconds':.2,'gain_i':2.,'gain_o':3.,'lo_i_radians':.31,'lo_o_radians':-.22,'filter_l2_norm':1.,'port_model':'H_MARKOV_VACUUM_PORTS','same_preparation_four_runs':True},
 'falsifiers':['Known gain/LO inversion changes selected moments','Time and filter transport do not preserve the same normalized signal','Four cross-correlations uniquely determine the two-mode density in counterexample','Isometric/pullback-metric transport changes full vector residual','Wrong coefficient incorrectly satisfies exact target','Missing or dependent Gamma produces beta','NaN/bool/unit mismatch passes admission','Selected moments accepted as full-state tomography'],
 'scope':'Finite algebra and synthetic schema only, no ODE, no observed data, no physical Gamma, no betaTGL estimation, no 5sigma, no Fock/temporal extrapolation',
 'pass_rule':'All frozen controls pass; any failure leaves a visible failure result; no automatic rerun.'}
new(ROOT/'PRE_REGISTRO_R69.json',plan)
new(ROOT/'FREEZE_R69.json',{'status':'FROZEN_BEFORE_SYNTHETIC_EXECUTION','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':[pin(ROOT/n) for n in ('PRE_REGISTRO_R69.json','bridge_r69.py','test_r69.py','freeze_r69.py','CALIBRATION_BRIDGE_R69.md')]})
print(json.dumps(pin(ROOT/'FREEZE_R69.json')))
