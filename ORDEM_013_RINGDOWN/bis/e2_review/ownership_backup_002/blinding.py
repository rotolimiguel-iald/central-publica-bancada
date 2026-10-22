"""Program-only offset access. The analyst receives shifted columns and hashes.

The local seed is committed by SHA256 in E2; its bytes and offsets must not be
printed, placed in the tunnel, or returned by analysis tools before unblinding.
This is procedural blinding on one host, not a separate human custodian.
"""
import hashlib,hmac
from pathlib import Path
import numpy as np
from registration_guard import contained,sha

FIELDS=('dtau220','dtau440','domega220','domega440')

def shifted_samples(columns,event,registration):
    seedpath=contained(registration['blinding']['seed_relative_to_Chatgpt'])
    if sha(seedpath)!=registration['blinding']['seed_commitment_sha256']:raise ValueError('Blinding commitment differs')
    seed=seedpath.read_bytes()
    if len(seed)!=32:raise ValueError('Invalid blinding seed length')
    scale=float(registration['blinding']['offset_half_range'])
    if not np.isfinite(scale) or scale<=0:raise ValueError('Invalid offset range')
    output={}
    for name in FIELDS:
        if name not in columns:continue
        a=np.asarray(columns[name],dtype=float)
        if a.ndim!=1 or not np.isfinite(a).all():raise ValueError('Invalid samples before blinding')
        digest=hmac.new(seed,('013BIS:'+event+':'+name).encode(),hashlib.sha256).digest()
        u=(int.from_bytes(digest[:8],'big')+.5)/(2**64)
        output['blinded_'+name]=(a+scale*(2*u-1)).tolist()
    if not output:raise ValueError('No deformation samples to blind')
    return {'status':'BLINDED_SAMPLES__NO_UNBLINDING_AUTHORIZATION',
      'event':event,'columns':output,'seed_commitment_sha256':registration['blinding']['seed_commitment_sha256'],
      'warning':'Offset-censored; means and signs have no physical interpretation. Parameter estimation private intermediates remain unread by analyst.'}

def unblinding_allowed(registration,information,systematic_gate,receipt):
    if systematic_gate is not True:return False
    if not np.isfinite(information) or information<registration['blinding']['minimum_information_to_unblind']:return False
    # This implementation never makes an implicit release decision.
    return bool(receipt and receipt.get('status')=='REGISTERED_UNBLINDING_GATE_MET' and
                receipt.get('independent_review_passed') is True)
