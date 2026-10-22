# Intrinsic-peak phase alignment: measured numerical correction

Date: 2026-09-22T06:58:12.989179+00:00. This is a numerical diagnostic, not a physical detection.

For an aligned binary, the isolated face-on complex 22 mode has orbital-phase
dependence through a unit phase factor. Its amplitude and intrinsic peak are
therefore phase independent. The previous implementation minimized a spline
amplitude separately at each orbital phase. At source90 the measured peak
spread was of order 1e-10 seconds. That minimization noise contaminated the
otherwise finite Fourier dependence on orbital phase.

`stable_peak_imr_model.py` is a byte-preserving copy except for its explanatory
header and one replacement: the face-on peak uses `coa_phase=0.`. The actual
waveform still receives the requested orbital phase and inclination. No mode,
phase branch, source parameter, physical prior or conditional TGL clock was
removed. The source model used by the running registered integral is unchanged.

The common-peak diagnostic had 72 held-out controls (two families, three rates,
two PSDs, two strengths, three phases). Data were the same frozen8192Hz injections
scaled to SNR40/200/600. Recomputing the peak per phase failed44/72 controls;
using one common peak failed0/72. The copied implementation was then evaluated
independently against that common-peak Fourier bank: maximum relative waveform
error 2.4754042885334018e-15 and maximum log-likelihood error
4.9476511776447296e-10. These results concern source90, not the entire
source prior or posterior region. They do not validate high-SNR injection
resolution, evidence precision or posterior coverage.

The original SEOB rate discrepancy persists after the phase fix. A separate
noiseless SNR600 diagnostic projected the rate difference onto the existing
common amplitude/polarization, orbital phase and peak-time directions. Each
linear time/phase correction was also evaluated in the full waveform, with
amplitude/polarization refitted. For SEOB64kHz versus128kHz the largest directly
reevaluated residual norm is 0.10008450309423779.
This is a whitened waveform distance, not a detection significance. Time/phase
alignment reduces but does not eliminate the source90 SEOB shape difference.
It is not legitimate to substitute this profile diagnostic for prior
marginalization or the registered numerical evidence checks.

The corrected model is available for a separately registered follow-up.
Do not insert it into the live integral or overwrite frozen runs. Future use
requires controls over the relevant source region and waveform rates.
