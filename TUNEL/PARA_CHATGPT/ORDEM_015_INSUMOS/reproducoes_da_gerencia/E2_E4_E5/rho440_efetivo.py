"""What isolated rho_440 does a real O4 event carry? Derived from the bancada's own archived GW250114 dtau440 width.

The Fisher table gives sigma(dtau440) = 0.2001 at rho_440 = 10 (sigma ~ 1/rho). The archived pSEOBNRv5PHM
posterior of GW250114 has dtau440 quantiles 5/50/95 = [-0.3489, 0.9519, 3.3968] (prior [-0.8, 4.0], edge mass 1.1%).
sigma_q90 = (q95 - q05)/3.29 -> effective rho_440 = 10 * 0.2001 / sigma. Then N90 via 440 for GW250114-like events
in O4, and with the bancada's fixed-amplitude rho gains for O5/ET/CE (1.8216, 8.7576, 14.2228).
"""
import json, math
q05, q50, q95 = -0.3489084548165656, 0.9518777311234092, 3.3968358269999683
sigma_q90 = (q95 - q05) / 3.2897
sigma_ref = 0.20011479377458105; rho_ref = 10.0
rho_eff = rho_ref * sigma_ref / sigma_q90
gain = {'O4': 1.0, 'O5': 1.821611425332796, 'ET': 8.757643952610179, 'CE': 14.22276470104178}
delta = {'R-B': -0.08216064025655216, 'R-MOD': -0.19599710827326722, 'R-RAIZ-0': -0.07367832435841462, 'R-LIN': -0.13724468993530575}
out = {'GW250114_dtau440_sigma_q90_archived': sigma_q90, 'rho440_effective_GW250114_O4': rho_eff,
       'caveat': 'posterior truncated by prior [-0.8,4.0] (1.1% KDE mass outside; 2.7% within one kernel sd of edge) -> true sigma larger, rho_eff smaller; the 440 posterior is also mass/spin-marginalised, not fixed-source Fisher',
       'N_per_reading': {}}
for r, d in delta.items():
    row = {}
    for det, g in gain.items():
        sig = sigma_ref * rho_ref / (rho_eff * g); z = abs(d) / sig
        n50 = (5 / z) ** 2; n90 = n50 * ((5 + 1.2816) / 5) ** 2
        row[det] = {'sigma_dtau440_GW250114_like': sig, 'z_per_event': z, 'N50': n50, 'N90': n90}
    out['N_per_reading'][r] = row
out['compare_220_route_N90_mixture_GWTC5_31'] = {'R-B': 3328, 'R-MOD': 1056, 'R-RAIZ-0': 976, 'R-LIN': 263}
print(json.dumps(out, indent=1))
