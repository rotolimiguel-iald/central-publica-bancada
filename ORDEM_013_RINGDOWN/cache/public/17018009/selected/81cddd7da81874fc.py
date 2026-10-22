import numpy as np
from scipy.stats import gaussian_kde
from scipy.special import logsumexp

import numpy as np
from scipy import interpolate
from scipy.stats import gaussian_kde
from scipy.ndimage import gaussian_filter
from scipy.integrate import cumulative_trapezoid as cumtrapz
from scipy.interpolate import interp1d, RectBivariateSpline


#------------------------------ 
class confidence(object):
    def __init__(self, counts):

        # Sort in descending order in frequency
        self.counts_sorted             = np.sort(counts.flatten())[::-1]

        # Get a normalized cumulative distribution from the mode
        self.norm_cumsum_counts_sorted = np.cumsum(self.counts_sorted) / np.sum(counts)

        # Set interpolations between heights, bins and levels
        self._set_interp()

    def _set_interp(self):

        self._length          = len(self.counts_sorted)

        # height from index
        self._height_from_idx = interpolate.interp1d(np.arange(self._length), self.counts_sorted, bounds_error=False, fill_value=0.)

        # index from height
        self._idx_from_height = interpolate.interp1d(self.counts_sorted[::-1], np.arange(self._length)[::-1], bounds_error=False, fill_value=self._length)

        # level from index
        self._level_from_idx  = interpolate.interp1d(np.arange(self._length), self.norm_cumsum_counts_sorted, bounds_error=False, fill_value=1.)

        # index from level
        self._idx_from_level  = interpolate.interp1d(self.norm_cumsum_counts_sorted, np.arange(self._length), bounds_error=False, fill_value=self._length)

    def level_from_height(self, height):
        return self._level_from_idx(self._idx_from_height(height))

    def height_from_level(self, level):
        return self._height_from_idx(self._idx_from_level(level))


#------------------------------ 
def get_bounds_from_posteriors(posterior_samples, comb=None, folded=False):
    """
    Calculate upper bounds on posterior distributions using kernel density estimation.
    
    This function estimates the probability density of posterior samples using
    Gaussian KDE, then calculates the 90% confidence bound. The bound represents
    the upper limit of the highest posterior density (HPD) region containing 90%
    of the posterior mass.
    
    Args:
        posterior_samples (array-like): Array of samples from a posterior distribution.
        comb (optional): Currently unused parameter (kept for backward compatibility).
        folded (bool, optional): If True, treats the posterior as folded around zero
                               (useful for parameters that are constrained to be positive).
                               If False, uses the full range. Defaults to False.
    
    Returns:
        float: The 90% HPD upper bound. For folded distributions, this is the maximum
               parameter value within the 90% HPD region. For unfolded distributions, 
               this is the maximum absolute parameter value within the 90% HPD region.
    
    Example:
        >>> # Posterior samples for a parameter
        >>> posterior = np.random.gamma(2, 1, 1000)  # Positive-valued parameter
        >>> upper_bound = get_bounds_from_posteriors(posterior, folded=True)
        >>> print(f"Numerical 90% HPD upper bound:  {upper_bound:.3f}")
        >>> print(f"Analytical 90% HPD upper bound: 3.890")
    """
    # Create kernel density estimator from posterior samples
    pdf = gaussian_kde(posterior_samples)
    
    if folded:
        # For folded distributions, evaluate from 0 to positive maximum
        centers = np.linspace(0.0, 1.05 * max(np.abs(posterior_samples)), 1000)
        # Add contributions from positive and negative sides (folded around zero)
        counts  = pdf(centers) + pdf(-centers)
        # Note: counts[0] /= 2. might be needed for proper normalization at zero
    else:
        # For unfolded distributions, evaluate over symmetric range
        centers = np.linspace(-1.05 * max(np.abs(posterior_samples)), 1.05 * max(np.abs(posterior_samples)), 1000)
        counts  = pdf(centers)
        
    # Create confidence object to find levels and bounds
    param_conf_obj = confidence(counts)
    
    # Calculate density height corresponding to 90% confidence level
    height = param_conf_obj.height_from_level(0.9)
    
    if folded:
        # For folded case, find maximum parameter value above the density threshold
        bound = np.max(centers[np.where(counts > height)])
    else:
        # For unfolded case, find maximum absolute parameter value above the density threshold
        bound = np.max(np.abs(centers[np.where(counts > height)]))
        
    return bound


#------------------------------ 
def get_sym_interval_from_pdf(y, x, p=0.9, normalize=True):
    """ Compute symmetric credible interval from PDF evaluated over grid.

    Arguments
    ---------
    y: array
        array of PDF values
    x: array
        array of parameter values corresponding to `y`.
    p: float
        credible level (def. 0.9).
    normalize: bool
        normalize PDF before computing CI (def. True).

    Returns
    -------
    left: float
        parameter value corresponding to lower interval edge.
    right: float
        parameter value corresponding to upper interval edge.
    """
    cdf_left  = 0.5*(1 - p)
    cdf_right = 1 - cdf_left
    
    # get CDF from PDF
    cdf       = cumtrapz(y, x, initial=0.)
    if normalize:
        cdf /= cdf.max()
        
    # compute lower edge
    if cdf_left < min(cdf):
        print("WARNING: value below range.")
        left = min(x)
        cdf_interp = None
    else:
        cdf_interp = interpolate.interp1d(cdf, x)
        left = cdf_interp(cdf_left)
        
    # compute upper edge
    if cdf_right > max(cdf):
        print("WARNING: value above range.")
        right = max(x)
    else:
        cdf_interp = cdf_interp or interp1d(cdf, x)
        right      = cdf_interp(cdf_right)
    return left, right


#------------------------------ 
def get_ul_from_pdf(y, x, p=0.9, normalize=True):
    """ Compute symmetric upper limit from PDF evaluated over grid.

    Arguments
    ---------
    y: array
        array of PDF values
    x: array
        array of parameter values corresponding to `y`.
    p: float
        credible level (def. 0.9).
    normalize: bool
        normalize PDF before computing UL (def. True).

    Returns
    -------
    ul: float
        parameter value corresponding to UL.
    """
    # get CDF from PDF
    cdf = cumtrapz(y, x, initial=0.)
    if normalize:
        cdf /= cdf.max()
        
    # compute UL
    if p > max(cdf):
        print("WARNING: value above range.")
        ul = max(x)
    else:
        cdf_interp = interpolate.interp1d(cdf, x)
        ul         = cdf_interp(p)
    return ul


#------------------------------ 
def calculate_summary_stats(posterior_samples, confidence_level=0.9):
    """
    Calculate median and confidence intervals for posterior samples.
    
    Args:
        posterior_samples: Array of posterior samples
        confidence_level: Confidence level for intervals (default 0.9 for 90%)
    
    Returns:
        dict: Dictionary with 'med', 'lo', 'hi' values
    """
    if len(posterior_samples) == 0:
        raise ValueError(f"Posterior samples empty!")
    
    # Calculate median
    median           = np.median(posterior_samples)
    
    # Calculate confidence intervals
    alpha            = 1 - confidence_level
    lower_percentile = (alpha / 2) * 100
    upper_percentile = (1 - alpha / 2) * 100
    
    lo_val           = np.percentile(posterior_samples, lower_percentile)
    hi_val           = np.percentile(posterior_samples, upper_percentile)
    
    # Convert to symmetric errors around median
    lo_error         = median - lo_val
    hi_error         = hi_val - median
    
    return {
        'med' : median,
        'lo'  : lo_error,
        'hi'  : hi_error
    }


#------------------------------ 
def get_imrct_stats(data,verbose=True,return_dict=False):
    L_dMfbyMf_dchifbychif, L_dMfbyMf, L_dchifbychif, dMfbyMf_vec, dchifbychif_vec = data

    # ~~~~~~~~~~~~ Calculate the credible levels and intervals in the marginalized 1d posteriors (joint)
    M90left, M90right     = get_sym_interval_from_pdf(L_dMfbyMf, dMfbyMf_vec, p=0.9)
    M50                   = get_ul_from_pdf(L_dMfbyMf, dMfbyMf_vec, p=0.5)

    chi90left, chi90right = get_sym_interval_from_pdf(L_dchifbychif, dchifbychif_vec, p=0.9)
    chi50                 = get_ul_from_pdf(L_dchifbychif, dchifbychif_vec, p=0.5)

    # ~~~~~~~~~~~~ Calculate the 2D GR quantile from combined posterior
    conf_v1v2       = confidence(L_dMfbyMf_dchifbychif)
    gr_height       = L_dMfbyMf_dchifbychif[
        np.argmin(abs(dMfbyMf_vec)),
        np.argmin(abs(dchifbychif_vec))
    ]
    gr_credib_level = conf_v1v2.level_from_height(gr_height)

    if(verbose):
        print('    Credible level of the GR value (combined):\t %.1f%% ' % (100.*gr_credib_level))
        print('    Median +/- 90%% sym-CI on dMfbyMf:\t\t %2.3f +%2.3f -%2.3f ' % (M50, M90right-M50, M50-M90left))
        print('    Median +/- 90%% sym-CI on dchifbychif:\t %2.3f +%2.3f -%2.3f '% (chi50, chi90right-chi50, chi50-chi90left))
    
    if(return_dict):
        stats_dict = {
            'GR_credible_level' : 100.*gr_credib_level,
            'dMf'   : {'med' : float(M50),   'hi' : M90right-M50,     'lo' : M50-M90left},
            'dchif' : {'med' : float(chi50), 'hi' : chi90right-chi50, 'lo' : chi50-chi90left}
        }
        return stats_dict


#------------------------------ 
def gf(P,sigma=1.0):
    """Apply a Gaussian filter to an array.
    
    Arguments
    ---------
    P : array_like
       Input array to filter
    sigma : float, optional
       Standard deviation for Gaussian kernel (default=1.0).
       Higher values produce more smoothing.
    
    Returns
    -------
    ndarray
       Filtered array
    """
    return gaussian_filter(P, sigma=sigma)


#------------------------------ 
def get_marginalized_posteriors(L_dMfbyMf_dchifbychif,dMfbyMf_vec,dchifbychif_vec):
    """Calculate the marginalized 1D posteriors (likelihoods). 

    Arguments
    ---------
    L_dMfbyMf_dchifbychif : array
        The 2D likelihood for {dMf/Mf, dchif/chif} 
    dMfbyMf_vec : array
        The 1D grid over which the dMf/Mf is evaluated.
    dchifbychif_vec : array 
        The 1D grid over which the dchif/chif is evaluated.

    Returns
    -------
    L_dMfbyMf_dchifbychif : array
        The normalized 2D likelihood on {dMf/Mf, dchif/chif} 
    L_dMfbyMf : array
        The 1D marginalized likelihood on dMf/Mf
    L_dchifbychif : array
        The 1D marginalized likelihood on dchif/chif
    dx : float
        The average grid spacing for {dMf/Mf}
    dy : float
        The average grid spacing for {dchif/chif}
        
    """
    # Normalize the 2D posteriors
    dx = np.mean(np.diff(dMfbyMf_vec))
    dy = np.mean(np.diff(dchifbychif_vec))
    L_dMfbyMf_dchifbychif /= np.sum(L_dMfbyMf_dchifbychif) * dx * dy

    # Compute marginalized 1D posterior
    L_dMfbyMf      = np.sum(L_dMfbyMf_dchifbychif, axis=0) * dy
    L_dchifbychif  = np.sum(L_dMfbyMf_dchifbychif, axis=1) * dx
    L_dMfbyMf     /= np.sum(L_dMfbyMf) * dx
    L_dchifbychif /= np.sum(L_dchifbychif) * dy
    
    return L_dMfbyMf_dchifbychif, L_dMfbyMf, L_dchifbychif, dx, dy


#------------------------------ 
def load_imrct_data_event(path, event='', wf='PhenomPv2'):
    # Read the likelihood data for this event, and corresponding grid
    data = []
    for k in ['dMfbyMf_dchifbychif', 'dMfbyMf_vec', 'dchifbychif_vec']:
        p = path.format(param=k, event=event, wf=wf)
        data.append(np.loadtxt(p))
    return data

def load_imrct_data_hier(path):
    # Read the likelihood data for this event, and corresponding grid
    data = []
    for k in ['dMfbyMf_dchifbychif', 'dMfbyMf_vec', 'dchifbychif_vec']:
        p = path.format(param=k)
        data.append(np.load(p,allow_pickle=True))
    return data


#------------------------------ 
# Map catalog id to super-event id
catalog_id_to_superevent_id_dict = {
    # O4a
    'GW230606A':'S230606d',
    'GW230609A':'S230609u',
    'GW230628A':'S230628ax',
    'GW230811A':'S230811n',
    'GW230919A':'S230919bj',
    'GW230920A':'S230920al',
    'GW230922A':'S230922g',
    'GW230924A':'S230924an',
    'GW230927B':'S230927be',
    'GW231108A':'S231108u',
    'GW231206A':'S231206ca',
    'GW231206B':'S231206cc',
    'GW231226A':'S231226av',
    # Pre-O4a
    'GW200316A' : 'S200316bj', 
    'GW200311B' : 'S200311bg', 
    'GW200225A' : 'S200225q', 
    'GW200224B' : 'S200224ca', 
    'GW200219A' : 'S200219ac', 
    'GW200208A' : 'S200208q', 
    'GW200202A' : 'S200202ac', 
    'GW200129A' : 'S200129m', 
    'GW200115'  : 'S200115j', 
    'GW191222A' : 'S191222n', 
    'GW191216A' : 'S191216ap', 
    'GW191215A' : 'S191215w', 
    'GW191204B' : 'S191204r', 
    'GW191129A' : 'S191129u', 
    'GW191109A' : 'S191109d',
    "GW190408A" : "S190408an",
    "GW190412A" : "S190412m",
    "GW190413A" : "S190413i",
    "GW190413B" : "S190413ac",
    "GW190421A" : "S190421ar",
    "GW190424A" : "S190424ao",
    "GW190425A" : "S190425z",
    "GW190426A" : "S190426c",
    "GW190503A" : "S190503bf",
    "GW190512A" : "S190512at",
    "GW190513A" : "S190513bm",
    "GW190514A" : "S190514n",
    "GW190517A" : "S190517h",
    "GW190519A" : "S190519bj",
    "GW190521A" : "S190521g",
    "GW190521B" : "S190521r",
    "GW190527A" : "S190527w",
    "GW190602A" : "S190602aq",
    "GW190620A" : "S190620e",
    "GW190630A" : "S190630ag",
    "GW190701A" : "S190701ah",
    "GW190706A" : "S190706ai",
    "GW190707A" : "S190707q",
    "GW190708A" : "S190708ap",
    "GW190719A" : "S190719an",
    "GW190720A" : "S190720a",
    "GW190727A" : "S190727h",
    "GW190728A" : "S190728q",
    "GW190731A" : "S190731aa",
    "GW190803A" : "S190803e",
    "GW190814A" : "S190814bv",
    "GW190828A" : "S190828j",
    "GW190828B" : "S190828l",
    "GW190909A" : "S190909w",
    "GW190910A" : "S190910s",
    "GW190915A" : "S190915ak",
    "GW190924A" : "S190924h",
    "GW190929A" : "S190929d",
    "GW190930A" : "S190930s",
    "GW150914A" : "S150914",
    "GW151012A" : "S151012",
    "GW151226A" : "S151226",
    "GW170104A" : "S170104",
    "GW170608A" : "S170608",
    "GW170729A" : "S170729",
    "GW170809A" : "S170809",
    "GW170814A" : "S170814",
    "GW170817A" : "S170817",
    "GW170818A" : "S170818",
    "GW170823A" : "S170823",
}

catalog_ids    = sorted(catalog_id_to_superevent_id_dict.keys())
superevent_ids = [catalog_id_to_superevent_id_dict[v] for v in catalog_ids]

superevent_id_to_catalog_id_dict = dict(zip(superevent_ids, catalog_ids))

def cid_to_sid(catalog_id):
    """ Get GraceDB superevent ID from catalog ID.
    """
    return catalog_id_to_superevent_id_dict[catalog_id]

def sid_to_cid(superevent_id):
    """ Get catalog ID from GraceDB superevent ID.
    """
    return superevent_id_to_catalog_id_dict[superevent_id]

o1o2_events = [k for k in catalog_id_to_superevent_id_dict.keys() if 'GW15' in k or 'GW17' in k]

o3a_events = ['GW190408A', 'GW190412A',
    'GW190421A', 'GW190425A', 'GW190503A', 'GW190512A', 'GW190513A',
    'GW190517A', 'GW190519A', 'GW190521A', 'GW190521B', 'GW190602A',
    'GW190630A', 'GW190706A', 'GW190707A', 'GW190708A', 'GW190720A',
    'GW190727A', 'GW190728A', 'GW190814A', 'GW190828A', 'GW190828B',
    'GW190910A', 'GW190915A', 'GW190924A']

o4a_events = [
    'GW230606A','GW230609A','GW230628A','GW230811A','GW230814A', 'GW230919A',
    'GW230920A','GW230922A','GW230924A','GW230927B','GW231108A',
    'GW231206A','GW231206B','GW231226A'
] 

class Event(object):
    def __init__(self, key):
        match_o1o2 = [k.strip('GW').strip('A') in key for k in o1o2_events]
        self.run = 'O3'        
        if any(match_o1o2):
            # this is an event from O1O2
            self.cid = [k for k,m in zip(o1o2_events,match_o1o2) if m][0]
            self.sid = cid_to_sid(self.cid)
            self.run = 'O1O2'
        elif key in superevent_ids:
            self.sid = key
            self.cid = sid_to_cid(self.sid)
            if self.cid in o4a_events:
                self.run = 'O4a'
        elif key.upper() in catalog_ids:
            self.cid = key.upper()
            self.sid = cid_to_sid(self.cid)
        else:
            # try to guess whether the key is mixed up
            new_key = key.replace('GW', 'S')
            if new_key in superevent_ids:
                self.sid = new_key
                self.cid = sid_to_cid(self.sid)
            else:
                raise ValueError("unrecognized event %r" % key)
            
#------------------------------ 
def get_22_peak_ang_freq(eta, a):
    """
    Get the peak angular frequency for the (2,2) mode. 
    This implements Eq. A8 of Bohe et al (2017) (arxiv.org/abs/1611.03703) and is a python port of the function in LAL:

    https://git.ligo.org/lscsoft/lalsuite/-/blob/master/lalsimulation/lib/LALSimInspiralTestingGRCorrections.c
    
    """
    chi = a
    
    res = (0.5626787200433265 + 
           (-0.08706198756945482 + 0.0017434519312586804 * chi) *
           np.log(10.26207326082448 -
                  chi * (7.629921628648589 - 
                        72.75949266353584 * (-0.25 + eta)) -
                  62.353217004599784 * (-0.25 + eta)))
    
    return res


#------------------------------ 
def get_shifted_waveform(ifo, waveform_polarizations, parameters, frequencies=None):
        if frequencies is None:
            frequencies = ifo.frequency_array[ifo.frequency_mask]
            mask = ifo.frequency_mask
        else:
            mask = np.ones(len(frequencies), dtype=bool)

        time_shift = ifo.time_delay_from_geocenter(
            parameters['ra'], parameters['dec'], parameters['geocent_time'])

        # Be careful to first subtract the two GPS times which are ~1e9 sec.
        # And then add the time_shift which varies at ~1e-5 sec
        dt_geocent = parameters['geocent_time'] - ifo.strain_data.start_time
        dt = dt_geocent + time_shift

        signal = {}
        for mode in waveform_polarizations.keys():
            signal[mode] = waveform_polarizations[mode][mask] * np.exp(-1j * 2 * np.pi * dt * frequencies)

        return signal