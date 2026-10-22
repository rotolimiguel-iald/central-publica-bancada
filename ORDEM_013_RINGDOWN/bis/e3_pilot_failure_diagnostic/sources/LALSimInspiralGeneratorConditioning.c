    1#include <math.h>
    2#include <string.h>
    3#include <lal/LALStdlib.h>
    4#include <lal/LALConstants.h>
    5#include <lal/LALDict.h>
    6#include <lal/TimeSeries.h>
    7#include <lal/FrequencySeries.h>
    8#include <lal/TimeFreqFFT.h>
    9#include <lal/BandPassTimeSeries.h>
   10#include <lal/Date.h>
   11#include <lal/Units.h>
   12#include <lal/LALSimInspiral.h>
   13#include <lal/LALSimInspiralWaveformParams.h>
   14#include "fix_reference_frequency_macro.h"
   15#include "LALSimInspiralGenerator_private.h"
   16 
   17/* Helper struct storing generator and approximant */
   18struct internal_data {
   19    LALSimInspiralGenerator *generator;
   20    int approx; /* if this is a known named approximant */
   21};
   22 
   23/* Free memory */
   24static int finalize(LALSimInspiralGenerator * myself)
   25{
   26    struct internal_data *internal_data = myself->internal_data;
   27    if (internal_data->generator->finalize)
   28        internal_data->generator->finalize(internal_data->generator);
   29    LALFree(internal_data->generator);
   30    LALFree(internal_data);
   31    return 0;
   32}
   33 
   34/* this routine is used when reference frequency is the starting frequency */
   35static int generate_conditioned_td_waveform_from_td_fallback(REAL8TimeSeries **hplus, REAL8TimeSeries **hcross, LALDict *params, LALSimInspiralGenerator *myself)
   36{
   37    struct internal_data *internal_data = myself->internal_data;
   38    LALSimInspiralGenerator *internal_generator = internal_data->generator;
   39    LALSimInspiralApplyTaper taper = LAL_SIM_INSPIRAL_TAPER_START;
   40 
   41    if (internal_generator->generate_td_waveform(hplus, hcross, params, internal_generator) < 0)
   42        XLAL_ERROR(XLAL_EFUNC);
   43 
   44    /* taper the waveform */
   45    if (XLALSimInspiralREAL8WaveTaper((*hplus)->data, taper) == XLAL_FAILURE)
   46        XLAL_ERROR(XLAL_EFUNC);
   47    if (XLALSimInspiralREAL8WaveTaper((*hcross)->data, taper) == XLAL_FAILURE)
   48        XLAL_ERROR(XLAL_EFUNC);
   49 
   50    return 0;
   51}
   52 
   53/* Perform conditioning of TD waveform so that the Fourier transform afterwards is sane. Copy of code from XLALSimInspiralTDFromTD().
   54 * The redshift correction has been removed, now it is up to the user to apply the proper corrections depending on the meanining of the masses and distance they use.
   55 */
   56static int generate_conditioned_td_waveform_from_td(REAL8TimeSeries **hplus, REAL8TimeSeries **hcross, LALDict *params, LALSimInspiralGenerator *myself)
   57{
   58    struct internal_data *internal_data = myself->internal_data;
   59    LALSimInspiralGenerator *internal_generator = internal_data->generator;
   60    int approx = internal_data->approx;
   61    LALDict *new_params;
   62    const double extra_time_fraction = 0.1; /* fraction of waveform duration to add as extra time for tapering */
   63    const double extra_cycles = 3.0; /* more extra time measured in cycles at the starting frequency */
   64    double original_f_min; /* f_min might be overwritten below, so keep original value */
   65    double f_min;
   66    double f_ref;
   67    double tchirp, tmerge, textra;
   68    double fisco, fstart;
   69    double m1, m2, s1z, s2z, s;
   70    int retval;
   71 
   72    original_f_min = f_min = XLALSimInspiralWaveformParamsLookupF22Start(params);
   73    f_ref = XLALSimInspiralWaveformParamsLookupF22Ref(params);
   74    m1 = XLALSimInspiralWaveformParamsLookupMass1(params);
   75    m2 = XLALSimInspiralWaveformParamsLookupMass2(params);
   76    s1z = XLALSimInspiralWaveformParamsLookupSpin1z(params);
   77    s2z = XLALSimInspiralWaveformParamsLookupSpin2z(params);
   78 
   79    /* adjust the reference frequency for certain precessing approximants:
   80     * if that approximate interprets f_ref==0 to be f_min, set f_ref=f_min;
   81     * otherwise do nothing */
   82    FIX_REFERENCE_FREQUENCY(f_ref, f_min, approx);
   83 
   84    /* This option recovers the behaviour of SimInspiralTD in the old interface */
   85    if (XLALDictContains(params, "condition") && XLALDictLookupINT4Value(params, "condition") == 2)
   86    {
   87      /* apply redshift correction to dimensionful source-frame quantities */
   88      REAL8 z=XLALSimInspiralWaveformParamsLookupRedshift(params);
   89      if (z != 0.0) {
   90          m1 *= (1.0 + z);
   91          m2 *= (1.0 + z);
   92          REAL8 distance = XLALSimInspiralWaveformParamsLookupDistance(params) * (1.0 + z);  /* change from comoving (transverse) distance to luminosity distance */
   93          XLALSimInspiralWaveformParamsInsertMass1(params, m1);
   94          XLALSimInspiralWaveformParamsInsertMass2(params, m2);
   95          XLALSimInspiralWaveformParamsInsertDistance(params, distance);
   96      }
   97      /* set redshift to zero so we don't accidentally apply it again later */
   98      z = 0.0;
   99      if (params)
  100        XLALSimInspiralWaveformParamsInsertRedshift(params,z);
  101    }
  102 
  103    /* if the requested low frequency is below the lowest Kerr ISCO
  104     * frequency then change it to that frequency */
  105    fisco = 1.0 / (pow(9.0, 1.5) * LAL_PI * (m1 + m2) * LAL_MTSUN_SI / LAL_MSUN_SI);
  106    if (f_min > fisco)
  107        f_min = fisco;
  108 
  109    /* upper bound on the chirp time starting at f_min */
  110    tchirp = XLALSimInspiralChirpTimeBound(f_min, m1, m2, s1z, s2z);
  111 
  112    /* upper bound on the final black hole spin */
  113    s = XLALSimInspiralFinalBlackHoleSpinBound(s1z, s2z);
  114 
  115    /* upper bound on the final plunge, merger, and ringdown time */
  116    tmerge = XLALSimInspiralMergeTimeBound(m1, m2) + XLALSimInspiralRingdownTimeBound(m1 + m2, s);
  117 
  118    /* extra time to include for all waveforms to take care of situations
  119     * where the frequency is close to merger (and is sweeping rapidly):
  120     * this is a few cycles at the low frequency */
  121    textra = extra_cycles / f_min;
  122 
  123    /* time domain approximant: condition by generating a waveform
  124     * with a lower starting frequency and apply tapers in the
  125     * region between that lower frequency and the requested
  126     * frequency f_min; here compute a new lower frequency */
  127    fstart = XLALSimInspiralChirpStartFrequencyBound((1.0 + extra_time_fraction) * tchirp + tmerge + textra, m1, m2);
  128 
  129    /* generate the waveform in the time domain starting at fstart */
  130    new_params = XLALDictDuplicate(params);
  131    XLALSimInspiralWaveformParamsInsertF22Ref(new_params, f_ref);
  132    XLALSimInspiralWaveformParamsInsertF22Start(new_params, fstart);
  133    retval = internal_generator->generate_td_waveform(hplus, hcross, new_params, internal_generator);
  134    XLALDestroyDict(new_params);
  135    if (retval < 0)
  136        XLAL_ERROR(XLAL_EFUNC);
  137 
  138    /* condition the time domain waveform by tapering in the extra time
  139     * at the beginning and high-pass filtering above original f_min */
  140    XLALSimInspiralTDConditionStage1(*hplus, *hcross, extra_time_fraction * tchirp + textra, original_f_min);
  141 
  142    /* final tapering at the beginning and at the end to remove filter transients */
  143 
  144    /* waveform should terminate at a frequency >= Schwarzschild ISCO
  145     * so taper one cycle at this frequency at the end; should not make
  146     * any difference to IMR waveforms */
  147    fisco = 1.0 / (pow(6.0, 1.5) * LAL_PI * (m1 + m2) * LAL_MTSUN_SI / LAL_MSUN_SI);
  148    XLALSimInspiralTDConditionStage2(*hplus, *hcross, f_min, fisco);
  149 
  150    return 0;
  151}
  152 
  153/* Conditioning of a FD waveform and transform it ot TD. Copy of code from XLALSimInspiralTDFromFD().
  154 * The redshift correction has been removed, now it is up to the user to apply the proper corrections depending on the meanining of the masses and distance they use.
  155 */
  156static int generate_conditioned_td_waveform_from_fd(REAL8TimeSeries **hplus, REAL8TimeSeries **hcross, LALDict *params, LALSimInspiralGenerator *myself)
  157{
  158    struct internal_data *internal_data = myself->internal_data;
  159    int approx = internal_data->approx;
  160    COMPLEX16FrequencySeries *hptilde = NULL;
  161    COMPLEX16FrequencySeries *hctilde = NULL;
  162    LALDict *new_params;
  163    REAL8FFTPlan *plan;
  164    size_t chirplen, end, k;
  165    double tshift;
  166    const double extra_time_fraction = 0.1; /* fraction of waveform duration to add as extra time for tapering */
  167    const double extra_cycles = 3.0; /* more extra time measured in cycles at the starting frequency */
  168    double original_f_min; /* f_min might be overwritten below, so keep original value */
  169    double f_min, f_max, f_ref;
  170    double deltaT;
  171    double tchirp, tmerge, textra;
  172    double fisco, fstart;
  173    double m1, m2, s1z, s2z, s;
  174    int retval;
  175 
  176    deltaT = XLALSimInspiralWaveformParamsLookupDeltaT(params);
  177    original_f_min = f_min = XLALSimInspiralWaveformParamsLookupF22Start(params);
  178    f_ref = XLALSimInspiralWaveformParamsLookupF22Ref(params);
  179    f_max = 0.5 / deltaT;
  180    m1 = XLALSimInspiralWaveformParamsLookupMass1(params);
  181    m2 = XLALSimInspiralWaveformParamsLookupMass2(params);
  182    s1z = XLALSimInspiralWaveformParamsLookupSpin1z(params);
  183    s2z = XLALSimInspiralWaveformParamsLookupSpin2z(params);
  184 
  185    /* adjust the reference frequency for certain precessing approximants:
  186     * if that approximate interprets f_ref==0 to be f_min, set f_ref=f_min;
  187     * otherwise do nothing */
  188    FIX_REFERENCE_FREQUENCY(f_ref, f_min, approx);
  189 
  190    /* This option recovers the behaviour of SimInspiralTD in the old interface */
  191    if (XLALDictContains(params, "condition") && XLALDictLookupINT4Value(params, "condition") == 2)
  192    {
  193      /* apply redshift correction to dimensionful source-frame quantities */
  194      REAL8 z=XLALSimInspiralWaveformParamsLookupRedshift(params);
  195      if (z != 0.0) {
  196          m1 *= (1.0 + z);
  197          m2 *= (1.0 + z);
  198          REAL8 distance = XLALSimInspiralWaveformParamsLookupDistance(params) * (1.0 + z);  /* change from comoving (transverse) distance to luminosity distance */
  199          XLALSimInspiralWaveformParamsInsertMass1(params, m1);
  200          XLALSimInspiralWaveformParamsInsertMass2(params, m2);
  201          XLALSimInspiralWaveformParamsInsertDistance(params, distance);
  202      }
  203      /* set redshift to zero so we don't accidentally apply it again later */
  204      z = 0.0;
  205      if (params)
  206        XLALSimInspiralWaveformParamsInsertRedshift(params,z);
  207    }
  208 
  209    /* if the requested low frequency is below the lowest Kerr ISCO
  210     * frequency then change it to that frequency */
  211    fisco = 1.0 / (pow(9.0, 1.5) * LAL_PI * (m1 + m2) * LAL_MTSUN_SI / LAL_MSUN_SI);
  212    if (f_min > fisco)
  213        f_min = fisco;
  214 
  215    /* upper bound on the chirp time starting at f_min */
  216    tchirp = XLALSimInspiralChirpTimeBound(f_min, m1, m2, s1z, s2z);
  217 
  218    /* upper bound on the final black hole spin */
  219    s = XLALSimInspiralFinalBlackHoleSpinBound(s1z, s2z);
  220 
  221    /* upper bound on the final plunge, merger, and ringdown time */
  222    tmerge = XLALSimInspiralMergeTimeBound(m1, m2) + XLALSimInspiralRingdownTimeBound(m1 + m2, s);
  223 
  224    /* extra time to include for all waveforms to take care of situations
  225     * where the frequency is close to merger (and is sweeping rapidly):
  226     * this is a few cycles at the low frequency */
  227    textra = extra_cycles / f_min;
  228 
  229    /* generate the conditioned waveform in the frequency domain */
  230    /* set deltaF = 0 to get a small enough resolution */
  231    new_params = XLALDictDuplicate(params);
  232    XLALSimInspiralWaveformParamsInsertF22Ref(new_params, f_ref);
  233    XLALSimInspiralWaveformParamsInsertFMax(new_params, f_max);
  234    XLALSimInspiralWaveformParamsInsertDeltaF(new_params, 0.0);
  235    retval = myself->generate_fd_waveform(&hptilde, &hctilde, new_params, myself);
  236    XLALDestroyDict(new_params);
  237    if (retval < 0)
  238        XLAL_ERROR(XLAL_EFUNC);
  239 
  240    /* we want to make sure that this waveform will give something
  241     * sensible if it is later transformed into the time domain:
  242     * to avoid the end of the waveform wrapping around to the beginning,
  243     * we shift waveform backwards in time and compensate for this
  244     * shift by adjusting the epoch -- note that the conditioned
  245     * generate_fd_waveform method guarantees that there is the
  246     * extra padding to do this */
  247    tshift = round(textra / deltaT) * deltaT; /* integer number of samples */
  248    for (k = 0; k < hptilde->data->length; ++k) {
  249        double complex phasefac = cexp(2.0 * LAL_PI * I * k * hptilde->deltaF * tshift);
  250        hptilde->data->data[k] *= phasefac;
  251        hctilde->data->data[k] *= phasefac;
  252    }
  253    XLALGPSAdd(&hptilde->epoch, tshift);
  254    XLALGPSAdd(&hctilde->epoch, tshift);
  255 
  256    /* transform the waveform into the time domain */
  257    chirplen = 2 * (hptilde->data->length - 1);
  258    *hplus = XLALCreateREAL8TimeSeries("H_PLUS", &hptilde->epoch, 0.0, deltaT, &lalStrainUnit, chirplen);
  259    *hcross = XLALCreateREAL8TimeSeries("H_CROSS", &hctilde->epoch, 0.0, deltaT, &lalStrainUnit, chirplen);
  260    plan = XLALCreateReverseREAL8FFTPlan(chirplen, 0);
  261    if (!(*hplus) || !(*hcross) || !plan) {
  262        XLALDestroyCOMPLEX16FrequencySeries(hptilde);
  263        XLALDestroyCOMPLEX16FrequencySeries(hctilde);
  264        XLALDestroyREAL8TimeSeries(*hcross);
  265        XLALDestroyREAL8TimeSeries(*hplus);
  266        XLALDestroyREAL8FFTPlan(plan);
  267        XLAL_ERROR(XLAL_EFUNC);
  268    }
  269    XLALREAL8FreqTimeFFT(*hplus, hptilde, plan);
  270    XLALREAL8FreqTimeFFT(*hcross, hctilde, plan);
  271 
  272    /* apply time domain filter at original f_min */
  273    XLALHighPassREAL8TimeSeries(*hplus, original_f_min, 0.99, 8);
  274    XLALHighPassREAL8TimeSeries(*hcross, original_f_min, 0.99, 8);
  275 
  276    /* compute how long a chirp we should have */
  277    /* revised estimate of chirp length from new start frequency */
  278    fstart = XLALSimInspiralChirpStartFrequencyBound((1.0 + extra_time_fraction) * tchirp, m1, m2);
  279    tchirp = XLALSimInspiralChirpTimeBound(fstart, m1, m2, s1z, s2z);
  280 
  281    /* total expected chirp length includes merger */
  282    chirplen = round((tchirp + tmerge) / deltaT);
  283 
  284    /* amount to snip off at the end is tshift */
  285    end = (*hplus)->data->length - round(tshift / deltaT);
  286 
  287    /* snip off extra time at beginning and at the end */
  288    XLALResizeREAL8TimeSeries(*hplus, end - chirplen, chirplen);
  289    XLALResizeREAL8TimeSeries(*hcross, end - chirplen, chirplen);
  290 
  291    /* clean up */
  292    XLALDestroyREAL8FFTPlan(plan);
  293    XLALDestroyCOMPLEX16FrequencySeries(hptilde);
  294    XLALDestroyCOMPLEX16FrequencySeries(hctilde);
  295 
  296    /* final tapering at the beginning and at the end to remove filter transients */
  297 
  298    /* waveform should terminate at a frequency >= Schwarzschild ISCO
  299     * so taper one cycle at this frequency at the end; should not make
  300     * any difference to IMR waveforms */
  301    fisco = 1.0 / (pow(6.0, 1.5) * LAL_PI * (m1 + m2) * LAL_MTSUN_SI / LAL_MSUN_SI);
  302    XLALSimInspiralTDConditionStage2(*hplus, *hcross, f_min, fisco);
  303 
  304    return 0;
  305}
  306 
  307/* Conditioning a Fourier domain waveform to be properly transformed to the time domain. This code was taken from the original XLALSimInspiralFD() function, corresponding to the FD approximants part.
  308 * The redshift correction has been removed, now it is up to the user to apply the proper corrections depending on the meanining of the masses and distance they use.
  309 */
  310static int generate_conditioned_fd_waveform_from_fd(COMPLEX16FrequencySeries **hplus, COMPLEX16FrequencySeries **hcross, LALDict *params, LALSimInspiralGenerator *myself)
  311{
  312    struct internal_data *internal_data = myself->internal_data;
  313    LALSimInspiralGenerator *internal_generator = internal_data->generator;
  314    int approx = internal_data->approx;
  315    LALDict *new_params;
  316    const double extra_time_fraction = 0.1; /* fraction of waveform duration to add as extra time for tapering */
  317    const double extra_cycles = 3.0; /* more extra time measured in cycles at the starting frequency */
  318    double chirplen, deltaT, deltaF, f_nyquist;
  319    double f_min, f_max, f_ref;
  320    double tchirp, tmerge, textra, tshift;
  321    double fstart, fisco;
  322    double m1, m2, s1z, s2z, s;
  323    size_t k, k0, k1;
  324    int chirplen_exp;
  325    int retval;
  326    size_t n;
  327 
  328    deltaF = XLALSimInspiralWaveformParamsLookupDeltaF(params);
  329    f_min = XLALSimInspiralWaveformParamsLookupF22Start(params);
  330    f_max = XLALSimInspiralWaveformParamsLookupFMax(params);
  331    f_ref = XLALSimInspiralWaveformParamsLookupF22Ref(params);
  332    m1 = XLALSimInspiralWaveformParamsLookupMass1(params);
  333    m2 = XLALSimInspiralWaveformParamsLookupMass2(params);
  334    s1z = XLALSimInspiralWaveformParamsLookupSpin1z(params);
  335    s2z = XLALSimInspiralWaveformParamsLookupSpin2z(params);
  336 
  337    /* adjust the reference frequency for certain precessing approximants:
  338     * if that approximate interprets f_ref==0 to be f_min, set f_ref=f_min;
  339     * otherwise do nothing */
  340    FIX_REFERENCE_FREQUENCY(f_ref, f_min, approx);
  341 
  342    /* This option recovers the behaviour of SimInspiralFD in the old interface */
  343    if (XLALDictContains(params, "condition") && XLALDictLookupINT4Value(params, "condition") == 2)
  344    {
  345      /* apply redshift correction to dimensionful source-frame quantities */
  346      REAL8 z=XLALSimInspiralWaveformParamsLookupRedshift(params);
  347      if (z != 0.0) {
  348          m1 *= (1.0 + z);
  349          m2 *= (1.0 + z);
  350          REAL8 distance = XLALSimInspiralWaveformParamsLookupDistance(params) * (1.0 + z);  /* change from comoving (transverse) distance to luminosity distance */
  351          XLALSimInspiralWaveformParamsInsertMass1(params, m1);
  352          XLALSimInspiralWaveformParamsInsertMass2(params, m2);
  353          XLALSimInspiralWaveformParamsInsertDistance(params, distance);
  354      }
  355      /* set redshift to zero so we don't accidentally apply it again later */
  356      z = 0.0;
  357      if (params)
  358        XLALSimInspiralWaveformParamsInsertRedshift(params,z);
  359    }
  360 
  361    /* Apply condition that f_max rounds to the next power-of-two multiple
  362     * of deltaF.
  363     * Round f_max / deltaF to next power of two.
  364     * Set f_max to the new Nyquist frequency.
  365     * The length of the chirp signal is then 2 * f_nyquist / deltaF.
  366     * The time spacing is 1 / (2 * f_nyquist) */
  367    f_nyquist = f_max;
  368    if (deltaF != 0) {
  369        n = round(f_max / deltaF);
  370        if ((n & (n - 1))) { /* not a power of 2 */
  371            frexp(n, &chirplen_exp);
  372            f_nyquist = ldexp(1.0, chirplen_exp) * deltaF;
  373            XLAL_PRINT_WARNING("f_max/deltaF = %g/%g = %g is not a power of two: changing f_max to %g", f_max, deltaF, f_max/deltaF, f_nyquist);
  374        }
  375    }
  376    deltaT = 0.5 / f_nyquist;
  377 
  378    /* generate a FD waveform and condition it by applying tapers at
  379     * frequencies between a frequency below the requested f_min and
  380     * f_min; also wind the waveform in phase in case it would wrap-
  381     * around at the merger time */
  382 
  383    /* if the requested low frequency is below the lowest Kerr ISCO
  384     * frequency then change it to that frequency */
  385    fisco = 1.0 / (pow(9.0, 1.5) * LAL_PI * (m1 + m2) * LAL_MTSUN_SI / LAL_MSUN_SI);
  386    if (f_min > fisco)
  387        f_min = fisco;
  388 
  389    /* upper bound on the chirp time starting at f_min */
  390    tchirp = XLALSimInspiralChirpTimeBound(f_min, m1, m2, s1z, s2z);
  391 
  392    /* upper bound on the final plunge, merger, and ringdown time */
  393    switch (approx) {
  394    case TaylorF2:
  395    case TaylorF2Ecc:
  396    case TaylorF2NLTides:
  397    case SpinTaylorF2:
  398    case TaylorF2RedSpin:
  399    case TaylorF2RedSpinTidal:
  400    case SpinTaylorT4Fourier:
  401        /* inspiral-only models: no merger time */
  402        tmerge = 0.0;
  403        break;
  404    default:
  405        /* IMR model: estimate plunge and merger time */
  406        /* sometimes these waveforms have phases that
  407         * cause them to wrap-around an amount equal to
  408         * the merger-ringodwn time, so we will undo
  409         * that here */
  410        s = XLALSimInspiralFinalBlackHoleSpinBound(s1z, s2z);
  411        tmerge = XLALSimInspiralMergeTimeBound(m1, m2) + XLALSimInspiralRingdownTimeBound(m1 + m2, s);
  412        break;
  413    }
  414 
  415    /* new lower frequency to start the waveform: add some extra early
  416     * part over which tapers may be applied, the extra amount being
  417     * a fixed fraction of the chirp time; add some additional padding
  418     * equal to a few extra cycles at the low frequency as well for
  419     * safety and for other routines to use */
  420    textra = extra_cycles / f_min;
  421    fstart = XLALSimInspiralChirpStartFrequencyBound((1.0 + extra_time_fraction) * tchirp, m1, m2);
  422 
  423    /* revise (over-)estimate of chirp from new start frequency */
  424    tchirp = XLALSimInspiralChirpTimeBound(fstart, m1, m2, s1z, s2z);
  425 
  426    /* need a long enough segment to hold a whole chirp with some padding */
  427    /* length of the chirp in samples */
  428    chirplen = round((tchirp + tmerge + 2.0 * textra) / deltaT);
  429    /* make chirplen next power of two */
  430    frexp(chirplen, &chirplen_exp);
  431    chirplen = ldexp(1.0, chirplen_exp);
  432    /* frequency resolution */
  433    if (deltaF == 0.0)
  434        deltaF = 1.0 / (chirplen * deltaT);
  435    else if (deltaF > 1.0 / (chirplen * deltaT))
  436        XLAL_PRINT_WARNING("Specified frequency interval of %g Hz is too large for a chirp of duration %g s", deltaF, chirplen * deltaT);
  437 
  438    /* generate the waveform in the frequency domain starting at fstart */
  439    new_params = XLALDictDuplicate(params);
  440    XLALSimInspiralWaveformParamsInsertF22Ref(new_params, f_ref);
  441    XLALSimInspiralWaveformParamsInsertF22Start(new_params, fstart);
  442    XLALSimInspiralWaveformParamsInsertDeltaF(new_params, deltaF);
  443    retval = internal_generator->generate_fd_waveform(hplus, hcross, new_params, internal_generator);
  444    XLALDestroyDict(new_params);
  445    if (retval < 0)
  446        XLAL_ERROR(XLAL_EFUNC);
  447 
  448    /* taper frequencies between fstart and f_min */
  449    k0 = round(fstart / (*hplus)->deltaF);
  450    k1 = round(f_min / (*hplus)->deltaF);
  451    /* make sure it is zero below fstart */
  452    for (k = 0; k < k0; ++k) {
  453        (*hplus)->data->data[k] = 0.0;
  454        (*hcross)->data->data[k] = 0.0;
  455    }
  456    /* taper between fstart and f_min */
  457    for ( ; k < k1; ++k) {
  458        double w = 0.5 - 0.5 * cos(LAL_PI * (k - k0) / (double)(k1 - k0));
  459        (*hplus)->data->data[k] *= w;
  460        (*hcross)->data->data[k] *= w;
  461    }
  462    /* make sure Nyquist frequency is zero */
  463    (*hplus)->data->data[(*hplus)->data->length - 1] = 0.0;
  464    (*hcross)->data->data[(*hcross)->data->length - 1] = 0.0;
  465 
  466    /* we want to make sure that this waveform will give something
  467     * sensible if it is later transformed into the time domain:
  468     * to avoid the end of the waveform wrapping around to the beginning,
  469     * we shift waveform backwards in time and compensate for this
  470     * shift by adjusting the epoch */
  471    tshift = round(tmerge / deltaT) * deltaT; /* integer number of time samples */
  472    for (k = 0; k < (*hplus)->data->length; ++k) {
  473        double complex phasefac = cexp(2.0 * LAL_PI * I * k * deltaF * tshift);
  474        (*hplus)->data->data[k] *= phasefac;
  475        (*hcross)->data->data[k] *= phasefac;
  476    }
  477    XLALGPSAdd(&(*hplus)->epoch, tshift);
  478    XLALGPSAdd(&(*hcross)->epoch, tshift);
  479 
  480    return 0;
  481}
  482 
  483/* Transform a Fourier domain waveform to the time domain. This code was taken from the original XLALSimInspiralFD() function, corresponding to the TD approximants part.
  484 * The redshift correction has been removed, now it is up to the user to apply the proper corrections depending on the meanining of the masses and distance they use.
  485 */
  486static int generate_conditioned_fd_waveform_from_td(COMPLEX16FrequencySeries **hplus, COMPLEX16FrequencySeries **hcross, LALDict *params, LALSimInspiralGenerator *myself)
  487{
  488    struct internal_data *internal_data = myself->internal_data;
  489    int approx = internal_data->approx;
  490    REAL8TimeSeries *hp = NULL;
  491    REAL8TimeSeries *hc = NULL;
  492    LALDict *new_params;
  493    REAL8FFTPlan *plan;
  494    double chirplen, deltaT, deltaF, f_nyquist;
  495    double f_min, f_max, f_ref;
  496    int chirplen_exp;
  497    int retval;
  498    size_t n;
  499 
  500    deltaF = XLALSimInspiralWaveformParamsLookupDeltaF(params);
  501    f_min = XLALSimInspiralWaveformParamsLookupF22Start(params);
  502    f_max = XLALSimInspiralWaveformParamsLookupFMax(params);
  503    f_ref = XLALSimInspiralWaveformParamsLookupF22Ref(params);
  504 
  505    /* adjust the reference frequency for certain precessing approximants:
  506     * if that approximate interprets f_ref==0 to be f_min, set f_ref=f_min;
  507     * otherwise do nothing */
  508    FIX_REFERENCE_FREQUENCY(f_ref, f_min, approx);
  509 
  510    /* This option recovers the behaviour of SimInspiralFD in the old interface */
  511    if (XLALDictContains(params, "condition") && XLALDictLookupINT4Value(params, "condition") == 2)
  512    {
  513      /* apply redshift correction to dimensionful source-frame quantities */
  514      REAL8 z=XLALSimInspiralWaveformParamsLookupRedshift(params);
  515      if (z != 0.0) {
  516          REAL8 m1 = XLALSimInspiralWaveformParamsLookupMass1(params) * (1.0 + z);
  517          REAL8 m2 = XLALSimInspiralWaveformParamsLookupMass2(params) * (1.0 + z);
  518          REAL8 distance = XLALSimInspiralWaveformParamsLookupDistance(params) * (1.0 + z);  /* change from comoving (transverse) distance to luminosity distance */
  519          XLALSimInspiralWaveformParamsInsertMass1(params, m1);
  520          XLALSimInspiralWaveformParamsInsertMass2(params, m2);
  521          XLALSimInspiralWaveformParamsInsertDistance(params, distance);
  522      }
  523      /* set redshift to zero so we don't accidentally apply it again later */
  524      z = 0.0;
  525      if (params)
  526        XLALSimInspiralWaveformParamsInsertRedshift(params,z);
  527    }
  528 
  529 
  530    /* Apply condition that f_max rounds to the next power-of-two multiple
  531     * of deltaF.
  532     * Round f_max / deltaF to next power of two.
  533     * Set f_max to the new Nyquist frequency.
  534     * The length of the chirp signal is then 2 * f_nyquist / deltaF.
  535     * The time spacing is 1 / (2 * f_nyquist) */
  536    f_nyquist = f_max;
  537    if (deltaF != 0) {
  538        n = round(f_max / deltaF);
  539        if ((n & (n - 1))) { /* not a power of 2 */
  540            frexp(n, &chirplen_exp);
  541            f_nyquist = ldexp(1.0, chirplen_exp) * deltaF;
  542            XLAL_PRINT_WARNING("f_max/deltaF = %g/%g = %g is not a power of two: changing f_max to %g", f_max, deltaF, f_max/deltaF, f_nyquist);
  543        }
  544    }
  545    deltaT = 0.5 / f_nyquist;
  546 
  547    /* generate conditioned waveform in time domain */
  548    new_params = XLALDictDuplicate(params);
  549    XLALSimInspiralWaveformParamsInsertF22Ref(new_params, f_ref);
  550    XLALSimInspiralWaveformParamsInsertDeltaT(new_params, deltaT);
  551    retval = myself->generate_td_waveform(&hp, &hc, new_params, myself);
  552    XLALDestroyDict(new_params);
  553    if (retval < 0)
  554        XLAL_ERROR(XLAL_EFUNC);
  555 
  556    /* frequency resolution */
  557    if (deltaF == 0.0) {
  558        /* round length of time domain signal to next power of two */
  559        chirplen = hp->data->length;
  560        frexp(chirplen, &chirplen_exp);
  561        chirplen = ldexp(1.0, chirplen_exp);
  562        deltaF = 1.0 / (chirplen * hp->deltaT);
  563    } else {
  564        /* set chirp length using precomputed Nyquist */
  565        chirplen = 2 * f_nyquist / deltaF;
  566        if (chirplen < hp->data->length)
  567            XLAL_PRINT_WARNING("Specified frequency interval of %g Hz is too large for a chirp of duration %g s with Nyquist frequency %g Hz. The inspiral will be truncated.", deltaF, hp->data->length * deltaT, f_nyquist);
  568    }
  569 
  570    /* resize waveforms to the required length */
  571    XLALResizeREAL8TimeSeries(hp, hp->data->length - (size_t) chirplen, (size_t) chirplen);
  572    XLALResizeREAL8TimeSeries(hc, hc->data->length - (size_t) chirplen, (size_t) chirplen);
  573 
  574    /* put the waveform in the frequency domain */
  575    /* (the units will correct themselves) */
  576    *hplus = XLALCreateCOMPLEX16FrequencySeries("FD H_PLUS", &hp->epoch, 0.0, deltaF, &lalDimensionlessUnit, (size_t) chirplen / 2 + 1);
  577    *hcross = XLALCreateCOMPLEX16FrequencySeries("FD H_CROSS", &hc->epoch, 0.0, deltaF, &lalDimensionlessUnit, (size_t) chirplen / 2 + 1);
  578    plan = XLALCreateForwardREAL8FFTPlan((size_t) chirplen, 0);
  579    XLALREAL8TimeFreqFFT(*hcross, hc, plan);
  580    XLALREAL8TimeFreqFFT(*hplus, hp, plan);
  581 
  582    /* clean up */
  583    XLALDestroyREAL8FFTPlan(plan);
  584    XLALDestroyREAL8TimeSeries(hc);
  585    XLALDestroyREAL8TimeSeries(hp);
  586 
  587    return 0;
  588}
  589 
  590//static int generate_conditioned_td_modes(SphHarmTimeSeries **hlm, LALDict *params, LALSimInspiralGenerator *myself);
  591 
  592//static int generate_conditioned_fd_modes(SphHarmFrequencySeries **hlm, LALDict *params, LALSimInspiralGenerator *myself);
  593 
  594/* Function to assign the proper conditioning generator method for a given approximant. */
  595int XLALSimInspiralGeneratorAddConditioningForApproximant(LALSimInspiralGenerator *generator, int approximant)
  596{
  597    struct internal_data *internal_data;
  598 
  599    internal_data = LALMalloc(sizeof(*internal_data));
  600    internal_data->approx = approximant;
  601    internal_data->generator = LALMalloc(sizeof(*internal_data->generator));
  602    memcpy(internal_data->generator, generator, sizeof(*internal_data->generator));
  603 
  604    generator->internal_data = internal_data;
  605    generator->finalize = finalize;
  606 
  607    if (internal_data->generator->generate_td_waveform) {
  608        if (internal_data->approx == -1) {
  609            /* Not a recognized approximant:
  610             * assume we can use regular conditioning */
  611            generator->generate_td_waveform = generate_conditioned_td_waveform_from_td;
  612        } else {
  613          /* If using approximants for which reference frequency is the starting frequency
  614            * generate using XLALSimInspiralChooseTDWaveform and apply the
  615            * LAL Taper 'LAL_SIM_INSPIRAL_TAPER_START' instead of
  616            * XLALSimInspiralTDConditionStage1 and XLALSimInspiralTDConditionStage2
  617            * as is done in XLALSimInspiralTDFromTD.
  618            * This is because XLALSimInspiralTDFromTD modifies the start frequency
  619            * which is not always possible with NR_hdf5 waveforms.
  620            * Do the same (ChooseTDWaveform+LALTaper) if using approximants for
  621            * which a starting frequency of zero is allowed, as determined from
  622            * XLALSimInspiralGetAllowZeroMinFreqFromApproximant. This is because
  623            * XLALSimInspiralTDFromTD does not properly handle f_min=0. For models
  624            * that allow f_min=0, this (ChooseTDWaveform+LALTaper) is the behaviour
  625            * independent of what f_min is passed.
  626            */
  627 
  628            // Check whether for the given approximant reference frequency is the starting frequency
  629            SpinFreq spin_freq_flag = XLALSimInspiralGetSpinFreqFromApproximant(approximant);
  630            // Check whether for the given approximant, f_min=0 is allowed.
  631            AllowZeroMinFreq allow_zero_fmin_flag = XLALSimInspiralGetAllowZeroMinFreqFromApproximant(approximant);
  632 
  633            if (spin_freq_flag == LAL_SIM_INSPIRAL_SPINS_CASEBYCASE || spin_freq_flag == LAL_SIM_INSPIRAL_SPINS_FLOW || allow_zero_fmin_flag == LAL_SIM_INSPIRAL_ALLOW_ZERO_FMIN)
  634                generator->generate_td_waveform = generate_conditioned_td_waveform_from_td_fallback;
  635            else
  636                generator->generate_td_waveform = generate_conditioned_td_waveform_from_td;
  637       }
  638    } else if (internal_data->generator->generate_fd_waveform)
  639        generator->generate_td_waveform = generate_conditioned_td_waveform_from_fd;
  640 
  641    if (internal_data->generator->generate_fd_waveform)
  642        generator->generate_fd_waveform = generate_conditioned_fd_waveform_from_fd;
  643    else if (internal_data->generator->generate_td_waveform)
  644        generator->generate_fd_waveform = generate_conditioned_fd_waveform_from_td;
  645 
  646    /* FUTURE: implement routines for conditioning modes */
  647    // generator->generate_td_modes = generate_conditioned_td_modes;
  648    // generator->generate_fd_modes = generate_conditioned_fd_modes;
  649 
  650 
  651    return 0;
  652}
  653 
  654/* Function to assign standard conditioning. Currently this is `generate_conditioned_td_waveform_from_td`. */
  655int XLALSimInspiralGeneratorAddStandardConditioning(LALSimInspiralGenerator *generator)
  656{
  657    return XLALSimInspiralGeneratorAddConditioningForApproximant(generator, -1);
  658}
