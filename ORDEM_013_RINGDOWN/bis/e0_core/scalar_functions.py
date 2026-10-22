"""Pure scalar E0 formulas; no I/O, dependencies, posterior access or simulation."""
import math
from statistics import NormalDist


def scalar_calibration(sigmas, predictions, centers):
    """Known-effect Gaussian calibration, NOT an E1 nuisance likelihood/test."""
    if not (len(sigmas)==len(predictions)==len(centers)) or not sigmas:
        raise ValueError('Mismatched or empty vectors')
    if any(not math.isfinite(x) for vector in (sigmas,predictions,centers) for x in vector):
        raise ValueError('Nonfinite input')
    if any(s<=0 for s in sigmas):
        raise ValueError('Nonpositive sigma')
    w=[1/(s*s) for s in sigmas]
    information=math.fsum(w)
    effect=math.fsum(a*b for a,b in zip(w,predictions))/information
    center=math.fsum(a*b for a,b in zip(w,centers))/information
    signal_information=math.fsum((p/s)**2 for p,s in zip(predictions,sigmas))
    lever=math.fsum(((p-effect)/s)**2 for p,s in zip(predictions,sigmas))
    factor=(5+NormalDist().inv_cdf(.9))**2/25
    n=len(w)
    n50=25*n/signal_information if signal_information else None
    n90=n50*factor if n50 is not None else None
    zobs=(center-effect)*math.sqrt(information)
    return {'I_tau_current':information,'delta_weighted':effect,'z_comb':math.sqrt(signal_information),
        'z_common':abs(effect)*math.sqrt(information),'z_slope':math.sqrt(lever),
        'N50':n50,'N90':n90,'I_tau_target90':n90*information/n if n90 is not None else None,
        'GW250114_equivalents_target90':n90*information/n*.058**2 if n90 is not None else None,
        'N50_slope':25*n/lever if lever else None,'N90_slope':factor*25*n/lever if lever else None,
        'N_spurious50_median':25*n/zobs**2 if zobs else None}
