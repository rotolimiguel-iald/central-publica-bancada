    1/*
    2 * Copyright (C) 2008 J. Creighton, S. Fairhurst, B. Krishnan, L. Santamaria, D. Keppel, Evan Ochsner, C. Pankow, 2014 A. Klein
    3 *
    4 *  This program is free software; you can redistribute it and/or modify
    5 *  it under the terms of the GNU General Public License as published by
    6 *  the Free Software Foundation; either version 2 of the License, or
    7 *  (at your option) any later version.
    8 *
    9 *  This program is distributed in the hope that it will be useful,
   10 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
   11 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   12 *  GNU General Public License for more details.
   13 *
   14 *  You should have received a copy of the GNU General Public License
   15 *  along with with program; see the file COPYING. If not, write to the
   16 *  Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
   17 *  MA  02110-1301  USA
   18 */
   19 
   20#include <complex.h>
   21#include <math.h>
   22 
   23#include <gsl/gsl_const.h>
   24#include <gsl/gsl_errno.h>
   25#include <gsl/gsl_math.h>
   26#include <gsl/gsl_odeiv.h>
   27 
   28#include <lal/SphericalHarmonics.h>
   29#include <lal/LALSimInspiral.h>
   30#include <lal/LALSimInspiralEOS.h>
   31#include <lal/LALSimIMR.h>
   32#include <lal/LALSimSphHarmMode.h>
   33#include <lal/LALConstants.h>
   34#include <lal/LALStdlib.h>
   35#include <lal/LALString.h>
   36#include <lal/Sequence.h>
   37#include <lal/TimeSeries.h>
   38#include <lal/FrequencySeries.h>
   39#include <lal/TimeFreqFFT.h>
   40#include <lal/BandPassTimeSeries.h>
   41#include <lal/Units.h>
   42#include <lal/LALSimBlackHoleRingdown.h>
   43#include <lal/LALSimInspiralPrecess.h>
   44#include <lal/LALSimInspiralWaveformParams.h>
   45 
   46#include "LALSimInspiralPNCoefficients.c"
   47#include "check_series_macros.h"
   48#include "check_waveform_macros.h"
   49#include "LALSimUniversalRelations.h"
   50#include "rotation_macros.h"
   51#include "fix_reference_frequency_macro.h"
   52 
   53#include "LALSimInspiralGenerator_private.h"
   54 
   55#ifdef __GNUC__
   56#define UNUSED __attribute__ ((unused))
   57#else
   58#define UNUSED
   59#endif
   60 
   61/**
   62 * (Twice) the highest known PN order of amplitude correction for
   63 * non-precessing binaries.
   64 */
   65#define MAX_NONPRECESSING_AMP_PN_ORDER 6
   66 
   67/**
   68 * (Twice) the highest known PN order of amplitude correction for
   69 * precessing binaries.
   70 */
   71#define MAX_PRECESSING_AMP_PN_ORDER 3
   72 
   73 
   74 
   75 
   76#define INITIALIZE_NAME(a) [a] = #a
   77/* TODO: UPDATE ME WHENEVER A NEW APPROXIMANT IS ADDED */
   78static const char *lalSimulationApproximantNames[] = {
   79    INITIALIZE_NAME(TaylorT1),
   80    INITIALIZE_NAME(TaylorT2),
   81    INITIALIZE_NAME(TaylorT3),
   82    INITIALIZE_NAME(TaylorF1),
   83    INITIALIZE_NAME(TaylorF2),
   84    INITIALIZE_NAME(TaylorF2Ecc),
   85    INITIALIZE_NAME(TaylorF2NLTides),
   86    INITIALIZE_NAME(TaylorR2F4),
   87    INITIALIZE_NAME(TaylorF2RedSpin),
   88    INITIALIZE_NAME(TaylorF2RedSpinTidal),
   89    INITIALIZE_NAME(PadeT1),
   90    INITIALIZE_NAME(PadeF1),
   91    INITIALIZE_NAME(EOB),
   92    INITIALIZE_NAME(BCV),
   93    INITIALIZE_NAME(BCVSpin),
   94    INITIALIZE_NAME(SpinTaylorT1),
   95    INITIALIZE_NAME(SpinTaylorT5),
   96    INITIALIZE_NAME(SpinTaylorT3),
   97    INITIALIZE_NAME(SpinTaylorT4),
   98    INITIALIZE_NAME(SpinTaylorF2),
   99    INITIALIZE_NAME(SpinTaylorFrameless),
  100    INITIALIZE_NAME(SpinTaylor),
  101    INITIALIZE_NAME(PhenSpinTaylor),
  102    INITIALIZE_NAME(PhenSpinTaylorRD),
  103    INITIALIZE_NAME(SpinQuadTaylor),
  104    INITIALIZE_NAME(FindChirpSP),
  105    INITIALIZE_NAME(FindChirpPTF),
  106    INITIALIZE_NAME(GeneratePPN),
  107    INITIALIZE_NAME(BCVC),
  108    INITIALIZE_NAME(FrameFile),
  109    INITIALIZE_NAME(AmpCorPPN),
  110    INITIALIZE_NAME(NumRel),
  111    INITIALIZE_NAME(NumRelNinja2),
  112    INITIALIZE_NAME(EccentricFD),
  113    INITIALIZE_NAME(Eccentricity),
  114    INITIALIZE_NAME(EOBNR),
  115    INITIALIZE_NAME(EOBNRv2),
  116    INITIALIZE_NAME(EOBNRv2HM),
  117    INITIALIZE_NAME(EOBNRv2_ROM),
  118    INITIALIZE_NAME(EOBNRv2HM_ROM),
  119    INITIALIZE_NAME(TEOBResum_ROM),
  120    INITIALIZE_NAME(SEOBNRv1),
  121    INITIALIZE_NAME(SEOBNRv2),
  122    INITIALIZE_NAME(SEOBNRv2_opt),
  123    INITIALIZE_NAME(SEOBNRv3),
  124    INITIALIZE_NAME(SEOBNRv3_pert),
  125    INITIALIZE_NAME(SEOBNRv3_opt),
  126    INITIALIZE_NAME(SEOBNRv3_opt_rk4),
  127    INITIALIZE_NAME(SEOBNRv4),
  128    INITIALIZE_NAME(SEOBNRv4_opt),
  129    INITIALIZE_NAME(SEOBNRv4P),
  130    INITIALIZE_NAME(SEOBNRv4PHM),
  131    INITIALIZE_NAME(SEOBNRv2T),
  132    INITIALIZE_NAME(SEOBNRv4T),
  133    INITIALIZE_NAME(SEOBNRv4HM),
  134    INITIALIZE_NAME(SEOBNRv1_ROM_EffectiveSpin),
  135    INITIALIZE_NAME(SEOBNRv1_ROM_DoubleSpin),
  136    INITIALIZE_NAME(SEOBNRv2_ROM_EffectiveSpin),
  137    INITIALIZE_NAME(SEOBNRv2_ROM_DoubleSpin),
  138    INITIALIZE_NAME(SEOBNRv2_ROM_DoubleSpin_HI),
  139    INITIALIZE_NAME(Lackey_Tidal_2013_SEOBNRv2_ROM),
  140    INITIALIZE_NAME(SEOBNRv4_ROM),
  141    INITIALIZE_NAME(SEOBNRv4HM_ROM),
  142    INITIALIZE_NAME(SEOBNRv4_ROM_NRTidal),
  143    INITIALIZE_NAME(SEOBNRv4_ROM_NRTidalv2),
  144    INITIALIZE_NAME(SEOBNRv4_ROM_NRTidalv2_NSBH),
  145    INITIALIZE_NAME(SEOBNRv4T_surrogate),
  146    INITIALIZE_NAME(SEOBNRv5_ROM),
  147    INITIALIZE_NAME(SEOBNRv5HM_ROM),
  148    INITIALIZE_NAME(SEOBNRv5_ROM_NRTidalv3),
  149    INITIALIZE_NAME(HGimri),
  150    INITIALIZE_NAME(IMRPhenomA),
  151    INITIALIZE_NAME(IMRPhenomB),
  152    INITIALIZE_NAME(IMRPhenomFA),
  153    INITIALIZE_NAME(IMRPhenomFB),
  154    INITIALIZE_NAME(IMRPhenomC),
  155    INITIALIZE_NAME(IMRPhenomD),
  156    INITIALIZE_NAME(IMRPhenomD_NRTidal),
  157    INITIALIZE_NAME(IMRPhenomD_NRTidalv2),
  158    INITIALIZE_NAME(IMRPhenomNSBH),
  159    INITIALIZE_NAME(IMRPhenomHM),
  160    INITIALIZE_NAME(IMRPhenomP),
  161    INITIALIZE_NAME(IMRPhenomPv2),
  162    INITIALIZE_NAME(IMRPhenomPv2_NRTidal),
  163    INITIALIZE_NAME(IMRPhenomPv2_NRTidalv2),
  164    INITIALIZE_NAME(IMRPhenomPv3),
  165    INITIALIZE_NAME(IMRPhenomPv3HM),
  166    INITIALIZE_NAME(IMRPhenomFC),
  167    INITIALIZE_NAME(TaylorEt),
  168    INITIALIZE_NAME(TaylorT4),
  169    INITIALIZE_NAME(EccentricTD),
  170    INITIALIZE_NAME(TaylorN),
  171    INITIALIZE_NAME(SpinTaylorT4Fourier),
  172    INITIALIZE_NAME(SpinTaylorT5Fourier),
  173    INITIALIZE_NAME(SpinDominatedWf),
  174    INITIALIZE_NAME(NRSur4d2s),
  175    INITIALIZE_NAME(NRSur7dq2),
  176    INITIALIZE_NAME(NRSur7dq4),
  177    INITIALIZE_NAME(NR_hdf5),
  178    INITIALIZE_NAME(NRHybSur3dq8),
  179    INITIALIZE_NAME(IMRPhenomXAS),
  180    INITIALIZE_NAME(IMRPhenomXHM),
  181    INITIALIZE_NAME(IMRPhenomXP),
  182    INITIALIZE_NAME(IMRPhenomXPHM),
  183    INITIALIZE_NAME(TEOBResumS),
  184    INITIALIZE_NAME(IMRPhenomT),
  185    INITIALIZE_NAME(IMRPhenomTHM),
  186    INITIALIZE_NAME(IMRPhenomTP),
  187    INITIALIZE_NAME(IMRPhenomTPHM),
  188    INITIALIZE_NAME(IMRPhenomXO4a),
  189    INITIALIZE_NAME(IMRPhenomXPNR),
  190    INITIALIZE_NAME(IMRPhenomXAS_NRTidalv2),
  191    INITIALIZE_NAME(IMRPhenomXP_NRTidalv2),
  192    INITIALIZE_NAME(IMRPhenomXAS_NRTidalv3),
  193    INITIALIZE_NAME(IMRPhenomXP_NRTidalv3),
  194    INITIALIZE_NAME(SEOBNRv4HM_PA),
  195    INITIALIZE_NAME(pSEOBNRv4HM_PA),
  196    INITIALIZE_NAME(ExternalPython)
  197};
  198#undef INITIALIZE_NAME
  199 
  200/* TODO: UPDATE ME WHENEVER A NEW PN ORDER IS ADDED */
  201static const char *lalSimulationPNOrderNames[] = {
  202    [LAL_PNORDER_NEWTONIAN]         = "newtonian",
  203    [LAL_PNORDER_HALF]              = "oneHalfPN",
  204    [LAL_PNORDER_ONE]               = "onePN",
  205    [LAL_PNORDER_ONE_POINT_FIVE]    = "onePointFivePN",
  206    [LAL_PNORDER_TWO]               = "twoPN",
  207    [LAL_PNORDER_TWO_POINT_FIVE]    = "twoPointFivePN",
  208    [LAL_PNORDER_THREE]             = "threePN",
  209    [LAL_PNORDER_THREE_POINT_FIVE]  = "threePointFivePN",
  210    [LAL_PNORDER_PSEUDO_FOUR]       = "pseudoFourPN",
  211};
  212 
  213/* TODO: UPDATE ME WHENEVER A NEW TAPER IS ADDED */
  214static const char *lalSimulationTaperNames[] = {
  215    [LAL_SIM_INSPIRAL_TAPER_NONE]       = "TAPER_NONE",
  216    [LAL_SIM_INSPIRAL_TAPER_START]      = "TAPER_START",
  217    [LAL_SIM_INSPIRAL_TAPER_END]        = "TAPER_END",
  218    [LAL_SIM_INSPIRAL_TAPER_STARTEND]   = "TAPER_STARTEND",
  219};
  220 
  221/* TODO: UPDATE ME WHENEVER A NEW FRAME AXIS IS ADDED */
  222static const char *lalSimulationFrameAxisNames[] = {
  223    [LAL_SIM_INSPIRAL_FRAME_AXIS_TOTAL_J]   = "TotalJ",
  224    [LAL_SIM_INSPIRAL_FRAME_AXIS_ORBITAL_L] = "OrbitalL",
  225    [LAL_SIM_INSPIRAL_FRAME_AXIS_VIEW]      = "View",
  226};
  227 
  228/* TODO: UPDATE ME WHENEVER A NEW MODES CHOICE IS ADDED */
  229static const char *lalSimulationModesChoiceNames[] = {
  230    [LAL_SIM_INSPIRAL_MODES_CHOICE_2AND3AND4AND5L] = "L2345",
  231    [LAL_SIM_INSPIRAL_MODES_CHOICE_2AND3AND4L] = "L234",
  232    [LAL_SIM_INSPIRAL_MODES_CHOICE_2AND3AND5L] = "L235",
  233    [LAL_SIM_INSPIRAL_MODES_CHOICE_2AND4AND5L] = "L245",
  234    [LAL_SIM_INSPIRAL_MODES_CHOICE_3AND4AND5L] = "L345",
  235    [LAL_SIM_INSPIRAL_MODES_CHOICE_2AND3L] = "L23",
  236    [LAL_SIM_INSPIRAL_MODES_CHOICE_2AND4L] = "L24",
  237    [LAL_SIM_INSPIRAL_MODES_CHOICE_3AND4L] = "L34",
  238    [LAL_SIM_INSPIRAL_MODES_CHOICE_2AND5L] = "L25",
  239    [LAL_SIM_INSPIRAL_MODES_CHOICE_3AND5L] = "L35",
  240    [LAL_SIM_INSPIRAL_MODES_CHOICE_4AND5L] = "L45",
  241    [LAL_SIM_INSPIRAL_MODES_CHOICE_RESTRICTED] = "L2",
  242    [LAL_SIM_INSPIRAL_MODES_CHOICE_3L] = "L3",
  243    [LAL_SIM_INSPIRAL_MODES_CHOICE_4L] = "L4",
  244    [LAL_SIM_INSPIRAL_MODES_CHOICE_5L] = "L5",
  245    /* NOTE: cannot do the "ALL" case since its value is -1 */
  246    // [LAL_SIM_INSPIRAL_MODES_CHOICE_ALL] = "ALL",
  247};
  248 
  249/* locates and deletes a substring in a list of substrings from a string, ignoring case;
  250 * if multiple substrings in the string match, delete the longest one; here, deletion
  251 * means replacing the substring with BEL characters */
  252static int delete_substring_in_list_from_string(char *string, const char *list[], size_t size)
  253{
  254    int longest_position = -1;
  255    int longest_offset = -1;
  256    int longest_length = -1;
  257    size_t i;
  258 
  259    if (string == NULL || strlen(string) == 0) // no string to search
  260        return -1;
  261 
  262    for (i = 0; i < size; ++i) {
  263        char *match;
  264        if (list[i] == NULL) // no such element in list
  265            continue;
  266        if ((match = XLALStringCaseSubstring(string, list[i]))) {
  267            int length = strlen(list[i]);
  268            if (length > longest_length) {
  269                longest_position = i;
  270                longest_offset = match - string;
  271                longest_length = length;
  272            }
  273        }
  274    }
  275 
  276    if (longest_position < 0) // failed to find a word
  277        return -1;
  278 
  279    /* delete word from string by replacing with BEL */
  280    for (i = 0; i < (size_t)longest_length; ++i)
  281        string[longest_offset + i] = '\b';
  282 
  283    return longest_position;
  284}
  285 
  286const LALSimInspiralGenerator *lalSimInspiralGeneratorTemplates[NumApproximants] = {
  287    [EOBNRv2HM] = &lalEOBNRv2HMGeneratorTemplate,
  288    [EOBNRv2HM_ROM] = &lalEOBNRv2HM_ROMGeneratorTemplate,
  289    [EOBNRv2] = &lalEOBNRv2GeneratorTemplate,
  290    [EOBNRv2_ROM] = &lalEOBNRv2_ROMGeneratorTemplate,
  291    [EccentricFD] = &lalEccentricFDGeneratorTemplate,
  292    [EccentricTD] = &lalEccentricTDGeneratorTemplate,
  293    [HGimri] = &lalHGimriGeneratorTemplate,
  294    [IMRPhenomA] = &lalIMRPhenomAGeneratorTemplate,
  295    [IMRPhenomB] = &lalIMRPhenomBGeneratorTemplate,
  296    [IMRPhenomC] = &lalIMRPhenomCGeneratorTemplate,
  297    [IMRPhenomD] = &lalIMRPhenomDGeneratorTemplate,
  298    [IMRPhenomD_NRTidal] = &lalIMRPhenomD_NRTidalGeneratorTemplate,
  299    [IMRPhenomD_NRTidalv2] = &lalIMRPhenomD_NRTidalv2GeneratorTemplate,
  300    [IMRPhenomHM] = &lalIMRPhenomHMGeneratorTemplate,
  301    [IMRPhenomNSBH] = &lalIMRPhenomNSBHGeneratorTemplate,
  302    [IMRPhenomP] = &lalIMRPhenomPGeneratorTemplate,
  303    [IMRPhenomPv2] = &lalIMRPhenomPv2GeneratorTemplate,
  304    [IMRPhenomPv2_NRTidal] = &lalIMRPhenomPv2_NRTidalGeneratorTemplate,
  305    [IMRPhenomPv2_NRTidalv2] = &lalIMRPhenomPv2_NRTidalv2GeneratorTemplate,
  306    [IMRPhenomPv3HM] = &lalIMRPhenomPv3HMGeneratorTemplate,
  307    [IMRPhenomPv3] = &lalIMRPhenomPv3GeneratorTemplate,
  308    [IMRPhenomTHM] = &lalIMRPhenomTHMGeneratorTemplate,
  309    [IMRPhenomTPHM] = &lalIMRPhenomTPHMGeneratorTemplate,
  310    [IMRPhenomTP] = &lalIMRPhenomTPGeneratorTemplate,
  311    [IMRPhenomT] = &lalIMRPhenomTGeneratorTemplate,
  312    [IMRPhenomXAS] = &lalIMRPhenomXASGeneratorTemplate,
  313    [IMRPhenomXHM] = &lalIMRPhenomXHMGeneratorTemplate,
  314    [IMRPhenomXPHM] = &lalIMRPhenomXPHMGeneratorTemplate,
  315    [IMRPhenomXP] = &lalIMRPhenomXPGeneratorTemplate,
  316    [IMRPhenomXAS_NRTidalv2] = &lalIMRPhenomXAS_NRTidalv2GeneratorTemplate,
  317    [IMRPhenomXP_NRTidalv2] = &lalIMRPhenomXP_NRTidalv2GeneratorTemplate,
  318    [IMRPhenomXAS_NRTidalv3] = &lalIMRPhenomXAS_NRTidalv3GeneratorTemplate,
  319    [IMRPhenomXP_NRTidalv3] = &lalIMRPhenomXP_NRTidalv3GeneratorTemplate,
  320    [IMRPhenomXO4a] = &lalIMRPhenomXO4aGeneratorTemplate,
  321    [IMRPhenomXPNR] = &lalIMRPhenomXPNRGeneratorTemplate,
  322    [Lackey_Tidal_2013_SEOBNRv2_ROM] = &lalLackey_Tidal_2013_SEOBNRv2_ROMGeneratorTemplate,
  323    [NRHybSur3dq8] = &lalNRHybSur3dq8GeneratorTemplate,
  324    [NRSur4d2s] = &lalNRSur4d2sGeneratorTemplate,
  325    [NRSur7dq2] = &lalNRSur7dq2GeneratorTemplate,
  326    [NRSur7dq4] = &lalNRSur7dq4GeneratorTemplate,
  327    [NR_hdf5] = &lalNR_hdf5GeneratorTemplate,
  328    [PhenSpinTaylorRD] = &lalPhenSpinTaylorRDGeneratorTemplate,
  329    [PhenSpinTaylor] = &lalPhenSpinTaylorGeneratorTemplate,
  330    [SEOBNRv1] = &lalSEOBNRv1GeneratorTemplate,
  331    [SEOBNRv1_ROM_DoubleSpin] = &lalSEOBNRv1_ROM_DoubleSpinGeneratorTemplate,
  332    [SEOBNRv1_ROM_EffectiveSpin] = &lalSEOBNRv1_ROM_EffectiveSpinGeneratorTemplate,
  333    [SEOBNRv2T] = &lalSEOBNRv2TGeneratorTemplate,
  334    [SEOBNRv2] = &lalSEOBNRv2GeneratorTemplate,
  335    [SEOBNRv2_ROM_DoubleSpin] = &lalSEOBNRv2_ROM_DoubleSpinGeneratorTemplate,
  336    [SEOBNRv2_ROM_DoubleSpin_HI] = &lalSEOBNRv2_ROM_DoubleSpin_HIGeneratorTemplate,
  337    [SEOBNRv2_ROM_EffectiveSpin] = &lalSEOBNRv2_ROM_EffectiveSpinGeneratorTemplate,
  338    [SEOBNRv2_opt] = &lalSEOBNRv2_optGeneratorTemplate,
  339    [SEOBNRv3] = &lalSEOBNRv3GeneratorTemplate,
  340    [SEOBNRv3_opt] = &lalSEOBNRv3_optGeneratorTemplate,
  341    [SEOBNRv3_opt_rk4] = &lalSEOBNRv3_opt_rk4GeneratorTemplate,
  342    [SEOBNRv3_pert] = &lalSEOBNRv3_pertGeneratorTemplate,
  343    [SEOBNRv4HM] = &lalSEOBNRv4HMGeneratorTemplate,
  344    [SEOBNRv4HM_ROM] = &lalSEOBNRv4HM_ROMGeneratorTemplate,
  345    [SEOBNRv4PHM] = &lalSEOBNRv4PHMGeneratorTemplate,
  346    [SEOBNRv4P] = &lalSEOBNRv4PGeneratorTemplate,
  347    [SEOBNRv4T] = &lalSEOBNRv4TGeneratorTemplate,
  348    [SEOBNRv4T_surrogate] = &lalSEOBNRv4T_surrogateGeneratorTemplate,
  349    [SEOBNRv4] = &lalSEOBNRv4GeneratorTemplate,
  350    [SEOBNRv4_ROM] = &lalSEOBNRv4_ROMGeneratorTemplate,
  351    [SEOBNRv4_ROM_NRTidal] = &lalSEOBNRv4_ROM_NRTidalGeneratorTemplate,
  352    [SEOBNRv4_ROM_NRTidalv2] = &lalSEOBNRv4_ROM_NRTidalv2GeneratorTemplate,
  353    [SEOBNRv4_ROM_NRTidalv2_NSBH] = &lalSEOBNRv4_ROM_NRTidalv2_NSBHGeneratorTemplate,
  354    [SEOBNRv4_opt] = &lalSEOBNRv4_optGeneratorTemplate,
  355    [SEOBNRv5_ROM] = &lalSEOBNRv5_ROMGeneratorTemplate,
  356    [SEOBNRv5HM_ROM] = &lalSEOBNRv5HM_ROMGeneratorTemplate,
  357    [SEOBNRv5_ROM_NRTidalv3] = &lalSEOBNRv5_ROM_NRTidalv3GeneratorTemplate,
  358    [SEOBNRv4HM_PA] = &lalSEOBNRv4HM_PAGeneratorTemplate,
  359    [pSEOBNRv4HM_PA] = &lalpSEOBNRv4HM_PAGeneratorTemplate,
  360    [SpinDominatedWf] = &lalSpinDominatedWfGeneratorTemplate,
  361    [SpinTaylorF2] = &lalSpinTaylorF2GeneratorTemplate,
  362    [SpinTaylorT1] = &lalSpinTaylorT1GeneratorTemplate,
  363    [SpinTaylorT4Fourier] = &lalSpinTaylorT4FourierGeneratorTemplate,
  364    [SpinTaylorT4] = &lalSpinTaylorT4GeneratorTemplate,
  365    [SpinTaylorT5Fourier] = &lalSpinTaylorT5FourierGeneratorTemplate,
  366    [SpinTaylorT5] = &lalSpinTaylorT5GeneratorTemplate,
  367    [TEOBResumS] = &lalTEOBResumSGeneratorTemplate,
  368    [TEOBResum_ROM] = &lalTEOBResum_ROMGeneratorTemplate,
  369    [TaylorEt] = &lalTaylorEtGeneratorTemplate,
  370    [TaylorF2Ecc] = &lalTaylorF2EccGeneratorTemplate,
  371    [TaylorF2NLTides] = &lalTaylorF2NLTidesGeneratorTemplate,
  372    [TaylorF2RedSpinTidal] = &lalTaylorF2RedSpinTidalGeneratorTemplate,
  373    [TaylorF2RedSpin] = &lalTaylorF2RedSpinGeneratorTemplate,
  374    [TaylorF2] = &lalTaylorF2GeneratorTemplate,
  375    [TaylorR2F4] = &lalTaylorR2F4GeneratorTemplate,
  376    [TaylorT1] = &lalTaylorT1GeneratorTemplate,
  377    [TaylorT2] = &lalTaylorT2GeneratorTemplate,
  378    [TaylorT3] = &lalTaylorT3GeneratorTemplate,
  379    [TaylorT4] = &lalTaylorT4GeneratorTemplate,
  380    [ExternalPython] = &lalPythonGeneratorTemplate,
  381};
  382 
  383/**
  384 * @addtogroup LALSimInspiral_c
  385 * @brief General routines for generating binary inspiral waveforms.
  386 *
  387 * @{
  388 */
  389 
  390 /**
  391  * @name New Interface Generator Routines
  392  * @{
  393  */
  394 
  395  /**
  396   * Destroy LALSimInspiralGenerator object.
  397   */
  398void XLALDestroySimInspiralGenerator(LALSimInspiralGenerator *generator)
  399{
  400    if (generator) {
  401        if (generator->initialize == NULL && generator->finalize == NULL) {
  402            /* assume generator is immutable -- this is a no-op */
  403            return;
  404        }
  405        /* invoke finalizer if present */
  406        if (generator->finalize)
  407            if (generator->finalize(generator) < 0)
  408                XLAL_ERROR_VOID(XLAL_EFUNC);
  409        XLALFree(generator);
  410    }
  411    return;
  412}
  413 
  414/**
  415 * Create LALSimInspiralGenerator object.
  416 * The LALDict can be None for all the C approximants. For external python model, the LALDict must contain the file and class object where the `generate_waveform` methods are defined.
  417 * Activating the option `condition` in the LALDict will generate the waveform with adequate conditioning for (inverse)Fourier transform.
  418 */
  419LALSimInspiralGenerator *XLALCreateSimInspiralGenerator(const LALSimInspiralGenerator *generator, LALDict *params)
  420{
  421    LALSimInspiralGenerator *new;
  422    XLAL_CHECK_NULL(generator, XLAL_EFAULT);
  423    if (generator->initialize == NULL && generator->finalize == NULL) {
  424        /* assume generator is immutable -- return the template */
  425        /* danger! discard the const qualifier! */
  426        new = (LALSimInspiralGenerator *)(intptr_t)generator;
  427    } else {
  428        /* create a new instance of the generator */
  429        new = XLALMalloc(sizeof(*new));
  430        XLAL_CHECK_NULL(new, XLAL_ENOMEM, "could not allocate memory for new generator");
  431        memcpy(new, generator, sizeof(*new));
  432        /* invoke initializer if present */
  433        if (new->initialize)
  434            if (new->initialize(new, params) < 0) {
  435                XLALFree(new);
  436                XLAL_ERROR_NULL(XLAL_EFUNC);
  437            }
  438    }
  439    return new;
  440}
  441 
  442/**
  443 * Returns LALSimInspiralGenerator object from approximant.
  444 * The LALDict can be None for all the C approximants. For external python model, the LALDict must contain the file and class object where the `generate_waveform` methods are defined.
  445 * Activating the option `condition` in the LALDict will generate the waveform with adequate conditioning for (inverse)Fourier transform.
  446 */
  447LALSimInspiralGenerator *XLALSimInspiralChooseGenerator(Approximant approx, LALDict *params)
  448{
  449    const LALSimInspiralGenerator *template = lalSimInspiralGeneratorTemplates[approx];
  450    XLAL_CHECK_NULL(template, XLAL_EINVAL, "no generator defined for approximant %d", approx);
  451    return XLALCreateSimInspiralGenerator(template, params);
  452}
  453 
  454/**
  455 * Return approximant name from generator object
  456 *
  457 */
  458const char *XLALSimInspiralGeneratorName(LALSimInspiralGenerator *generator)
  459{
  460    XLAL_CHECK_NULL(generator, XLAL_EFAULT);
  461    return generator->name;
  462}
  463 
  464 /** @} */
  465 
  466/**
  467 * @name New Interface Waveform Routines
  468 * @{
  469 */
  470 
  471/**
  472 * Returns time-domain polarizations for a specific approximant.
  473 * Equivalent to XLALSimInspiralChooseTDWaveform(). Equivalent to XLALSimInspiralTD() if the option `condition` is activated in the LALDict.
  474 * The waveform arguments are inserted into the LALDict. The generator carries the info about the approximant and potentially extra data which could be recycled by the model to speed-up calculation.
  475 *
  476 * The parameters in the LALDict must be in SI units.
  477 */
  478int XLALSimInspiralGenerateTDWaveform(
  479    REAL8TimeSeries **hplus,
  480    REAL8TimeSeries **hcross,
  481    LALDict *params,
  482    LALSimInspiralGenerator *generator
  483)
  484{
  485    XLAL_CHECK(hplus && hcross && generator, XLAL_EFAULT);
  486    XLAL_CHECK(*hplus == NULL && *hcross == NULL, XLAL_EINVAL, "hplus and hcross must be pointers to NULL");
  487 
  488    if (generator->generate_td_waveform)
  489        return generator->generate_td_waveform(hplus, hcross, params, generator);
  490 
  491    XLAL_ERROR(XLAL_EINVAL, "generator does not provide a method to generate time-domain waveforms");
  492}
  493 
  494/**
  495 * Compute time-domain modes for a specific approximant.
  496 * Equivalent to XLALSimInspiralChooseTDModes(). The only difference is that the SphHarmSeries object needs to be passed as an argument to the function. The actual returned value is an integer which indicates success or error in the waveform evaluation (see https://lscsoft.docs.ligo.org/lalsuite/lal/group___x_l_a_l_error__h.html).
  497 * The waveform arguments are inserted into the LALDict. The generator carries the info about the approximant and potentially extra data which could be recycled by the model to speed-up calculation.
  498 *
  499 * The parameters in the LALDict must be in SI units.
  500 */
  501int XLALSimInspiralGenerateTDModes(
  502    SphHarmTimeSeries **hlm,
  503    LALDict *params,
  504    LALSimInspiralGenerator *generator
  505)
  506{
  507    XLAL_CHECK(hlm && generator, XLAL_EFAULT);
  508    XLAL_CHECK(*hlm == NULL, XLAL_EINVAL, "hlm must be a pointer to NULL");
  509 
  510    if (generator->generate_td_modes)
  511        return generator->generate_td_modes(hlm, params, generator);
  512 
  513    XLAL_ERROR(XLAL_EINVAL, "generator does not provide a method to generate time-domain modes");
  514}
  515 
  516/**
  517 * Returns frequency-domain polarizations for a specific approximant.
  518 * Equivalent to XLALSimInspiralChooseFDWaveform(). Equivalent to XLALSimInspiralFD() if the option `condition` is activated in the LALDict.
  519 * The waveform arguments are inserted into the LALDict. The generator carries the info about the approximant and potentially extra data which could be recycled by the model to speed-up calculation.
  520 *
  521 * The parameters in the LALDict must be in SI units.
  522 */
  523int XLALSimInspiralGenerateFDWaveform(
  524    COMPLEX16FrequencySeries **hplus,
  525    COMPLEX16FrequencySeries **hcross,
  526    LALDict *params,
  527    LALSimInspiralGenerator *generator
  528)
  529{
  530    XLAL_CHECK(hplus && hcross && generator, XLAL_EFAULT);
  531    XLAL_CHECK(*hplus == NULL && *hcross == NULL, XLAL_EINVAL, "hplus and hcross must be pointers to NULL");
  532    if (generator->generate_fd_waveform)
  533        return generator->generate_fd_waveform(hplus, hcross, params, generator);
  534 
  535    XLAL_ERROR(XLAL_EINVAL, "generator does not provide a method to generate frequency-domain waveforms");
  536}
  537 
  538/**
  539 * Compute frequency-domain modes for a specific approximant.
  540 * Equivalent to XLALSimInspiralChooseFDModes. The only difference is that the SphHarmSeries object needs to be passed as an argument to the function. The actual returned value is an integer which indicates success or error in the waveform evaluation (see https://lscsoft.docs.ligo.org/lalsuite/lal/group___x_l_a_l_error__h.html).
  541 * The waveform arguments are inserted into the LALDict. The generator carries the info about the approximant and potentially extra data which could be recycled by the model to speed-up calculation.
  542 *
  543 * The parameters in the LALDict must be in SI units.
  544 */
  545int XLALSimInspiralGenerateFDModes(
  546    SphHarmFrequencySeries **hlm,
  547    LALDict *params,
  548    LALSimInspiralGenerator *generator
  549)
  550{
  551    XLAL_CHECK(hlm && generator, XLAL_EFAULT);
  552    XLAL_CHECK(*hlm == NULL, XLAL_EINVAL, "hlm must be a pointer to NULL");
  553 
  554    if (generator->generate_fd_modes)
  555        return generator->generate_fd_modes(hlm, params, generator);
  556 
  557    XLAL_ERROR(XLAL_EINVAL, "generator does not provide a method to generate frequency-domain modes");
  558}
  559 
  560/** @} */
  561 
  562/**
  563* @name New Interface parse parameters Routines
  564* @{
  565*/
  566 
  567/**
  568 * Insert all the input arguments needed by XALSimInspiralChooseTDWaveform() into a laldictionary.
  569 */
  570void XLALSimInspiralParseDictionaryToChooseTDWaveform(
  571    REAL8 *m1,                             /**< [out] mass of companion 1 (kg) */
  572    REAL8 *m2,                             /**< [out] mass of companion 2 (kg) */
  573    REAL8 *S1x,                            /**< [out] x-component of the dimensionless spin of object 1 */
  574    REAL8 *S1y,                            /**< [out] y-component of the dimensionless spin of object 1 */
  575    REAL8 *S1z,                            /**< [out] z-component of the dimensionless spin of object 1 */
  576    REAL8 *S2x,                            /**< [out] x-component of the dimensionless spin of object 2 */
  577    REAL8 *S2y,                            /**< [out] y-component of the dimensionless spin of object 2 */
  578    REAL8 *S2z,                            /**< [out] z-component of the dimensionless spin of object 2 */
  579    REAL8 *distance,                       /**< [out] distance of source (m) */
  580    REAL8 *inclination,                    /**< [out] inclination of source (rad) */
  581    REAL8 *phiRef,                         /**< [out] reference orbital phase (rad) */
  582    REAL8 *longAscNodes,                   /**< [out] longitude of ascending nodes, degenerate with the polarization angle, Omega in documentation */
  583    REAL8 *eccentricity,                   /**< [out] eccentrocity at reference epoch */
  584    REAL8 *meanPerAno,                     /**< [out] mean anomaly of periastron */
  585    REAL8 *deltaT,                         /**< [out] sampling interval (s) */
  586    REAL8 *f_min,                          /**< [out] starting GW frequency (Hz) */
  587    REAL8 *f_ref,                          /**< [out] reference frequency (Hz) */
  588    LALDict *params                        /**< Input lal dictionary with waveform (and optional) parameters **/
  589)
  590{
  591    *m1 = XLALSimInspiralWaveformParamsLookupMass1(params);
  592    *m2 = XLALSimInspiralWaveformParamsLookupMass2(params);
  593    *S1x = XLALSimInspiralWaveformParamsLookupSpin1x(params);
  594    *S1y = XLALSimInspiralWaveformParamsLookupSpin1y(params);
  595    *S1z = XLALSimInspiralWaveformParamsLookupSpin1z(params);
  596    *S2x = XLALSimInspiralWaveformParamsLookupSpin2x(params);
  597    *S2y = XLALSimInspiralWaveformParamsLookupSpin2y(params);
  598    *S2z = XLALSimInspiralWaveformParamsLookupSpin2z(params);
  599    *distance = XLALSimInspiralWaveformParamsLookupDistance(params);
  600    *inclination = XLALSimInspiralWaveformParamsLookupInclination(params);
  601    *phiRef = XLALSimInspiralWaveformParamsLookupRefPhase(params);
  602    *longAscNodes = XLALSimInspiralWaveformParamsLookupLongAscNodes(params);
  603    *eccentricity = XLALSimInspiralWaveformParamsLookupEccentricity(params);
  604    *meanPerAno = XLALSimInspiralWaveformParamsLookupMeanPerAno(params);
  605    *deltaT = XLALSimInspiralWaveformParamsLookupDeltaT(params);
  606    *f_min = XLALSimInspiralWaveformParamsLookupF22Start(params);
  607    *f_ref = XLALSimInspiralWaveformParamsLookupF22Ref(params);
  608 
  609    return;
  610}
  611 
  612/**
  613 * Insert all the input arguments needed by XLALSimInspiralChooseTDModes() into a laldictionary.
  614 */
  615void XLALSimInspiralParseDictionaryToChooseTDModes(
  616    REAL8 *phiRef,                         /**< [out] reference orbital phase (rad) */
  617    REAL8 *deltaT,                         /**< [out] sampling interval (s) */
  618    REAL8 *m1,                             /**< [out] mass of companion 1 (kg) */
  619    REAL8 *m2,                             /**< [out] mass of companion 2 (kg) */
  620    REAL8 *S1x,                            /**< [out] x-component of the dimensionless spin of object 1 */
  621    REAL8 *S1y,                            /**< [out] y-component of the dimensionless spin of object 1 */
  622    REAL8 *S1z,                            /**< [out] z-component of the dimensionless spin of object 1 */
  623    REAL8 *S2x,                            /**< [out] x-component of the dimensionless spin of object 2 */
  624    REAL8 *S2y,                            /**< [out] y-component of the dimensionless spin of object 2 */
  625    REAL8 *S2z,                            /**< [out] z-component of the dimensionless spin of object 2 */
  626    REAL8 *f_min,                          /**< [out] starting GW frequency (Hz) */
  627    REAL8 *f_ref,                          /**< [out] reference frequency (Hz) */
  628    REAL8 *distance,                       /**< [out] distance of source (m) */
  629    INT4 *lmax,                            /**< [out] generate all modes with l <= lmax */
  630    LALDict *params                        /**< Input lal dictionary with waveform (and optional) parameters **/
  631)
  632{
  633    *phiRef = XLALSimInspiralWaveformParamsLookupRefPhase(params);
  634    *deltaT = XLALSimInspiralWaveformParamsLookupDeltaT(params);
  635    *m1 = XLALSimInspiralWaveformParamsLookupMass1(params);
  636    *m2 = XLALSimInspiralWaveformParamsLookupMass2(params);
  637    *S1x = XLALSimInspiralWaveformParamsLookupSpin1x(params);
  638    *S1y = XLALSimInspiralWaveformParamsLookupSpin1y(params);
  639    *S1z = XLALSimInspiralWaveformParamsLookupSpin1z(params);
  640    *S2x = XLALSimInspiralWaveformParamsLookupSpin2x(params);
  641    *S2y = XLALSimInspiralWaveformParamsLookupSpin2y(params);
  642    *S2z = XLALSimInspiralWaveformParamsLookupSpin2z(params);
  643    *f_min = XLALSimInspiralWaveformParamsLookupF22Start(params);
  644    *f_ref = XLALSimInspiralWaveformParamsLookupF22Ref(params);
  645    *distance = XLALSimInspiralWaveformParamsLookupDistance(params);
  646    *lmax = XLALSimInspiralWaveformParamsLookupLmax(params);
  647 
  648    return;
  649}
  650 
  651/**
  652 * Insert all the input arguments needed by XLALSimInspiralChooseFDWaveform() into a laldictionary.
  653 */
  654void XLALSimInspiralParseDictionaryToChooseFDWaveform(
  655    REAL8 *m1,                             /**< [out] mass of companion 1 (kg) */
  656    REAL8 *m2,                             /**< [out] mass of companion 2 (kg) */
  657    REAL8 *S1x,                            /**< [out] x-component of the dimensionless spin of object 1 */
  658    REAL8 *S1y,                            /**< [out] y-component of the dimensionless spin of object 1 */
  659    REAL8 *S1z,                            /**< [out] z-component of the dimensionless spin of object 1 */
  660    REAL8 *S2x,                            /**< [out] x-component of the dimensionless spin of object 2 */
  661    REAL8 *S2y,                            /**< [out] y-component of the dimensionless spin of object 2 */
  662    REAL8 *S2z,                            /**< [out] z-component of the dimensionless spin of object 2 */
  663    REAL8 *distance,                       /**< [out] distance of source (m) */
  664    REAL8 *inclination,                    /**< [out] inclination of source (rad) */
  665    REAL8 *phiRef,                         /**< [out] reference orbital phase (rad) */
  666    REAL8 *longAscNodes,                   /**< [out] longitude of ascending nodes, degenerate with the polarization angle, Omega in documentation */
  667    REAL8 *eccentricity,                   /**< [out] eccentrocity at reference epoch */
  668    REAL8 *meanPerAno,                     /**< [out] mean anomaly of periastron */
  669    REAL8 *deltaF,                         /**< [out] frequency interval (Hz) */
  670    REAL8 *f_min,                          /**< [out] starting GW frequency (Hz) */
  671    REAL8 *f_max,                          /**< [out] ending GW frequency (Hz) */
  672    REAL8 *f_ref,                          /**< [out] reference frequency (Hz) */
  673    LALDict *params                        /**< Input lal dictionary with waveform (and optional) parameters **/
  674)
  675{
  676 
  677    *m1 = XLALSimInspiralWaveformParamsLookupMass1(params);
  678    *m2 = XLALSimInspiralWaveformParamsLookupMass2(params);
  679    *S1x = XLALSimInspiralWaveformParamsLookupSpin1x(params);
  680    *S1y = XLALSimInspiralWaveformParamsLookupSpin1y(params);
  681    *S1z = XLALSimInspiralWaveformParamsLookupSpin1z(params);
  682    *S2x = XLALSimInspiralWaveformParamsLookupSpin2x(params);
  683    *S2y = XLALSimInspiralWaveformParamsLookupSpin2y(params);
  684    *S2z = XLALSimInspiralWaveformParamsLookupSpin2z(params);
  685    *distance = XLALSimInspiralWaveformParamsLookupDistance(params);
  686    *inclination = XLALSimInspiralWaveformParamsLookupInclination(params);
  687    *phiRef = XLALSimInspiralWaveformParamsLookupRefPhase(params);
  688    *longAscNodes = XLALSimInspiralWaveformParamsLookupLongAscNodes(params);
  689    *eccentricity = XLALSimInspiralWaveformParamsLookupEccentricity(params);
  690    *meanPerAno = XLALSimInspiralWaveformParamsLookupMeanPerAno(params);
  691    *deltaF = XLALSimInspiralWaveformParamsLookupDeltaF(params);
  692    *f_min = XLALSimInspiralWaveformParamsLookupF22Start(params);
  693    *f_max = XLALSimInspiralWaveformParamsLookupFMax(params);
  694    *f_ref = XLALSimInspiralWaveformParamsLookupF22Ref(params);
  695 
  696    return;
  697}
  698 
  699/**
  700 * Insert all the input arguments needed by XLALSimInspiralChooseFDModes() into a laldictionary.
  701 */
  702void XLALSimInspiralParseDictionaryToChooseFDModes(
  703    REAL8 *m1,                                   /**< [out] mass of companion 1 (kg) */
  704    REAL8 *m2,                                   /**< [out] mass of companion 2 (kg) */
  705    REAL8 *S1x,                                  /**< [out] x-component of the dimensionless spin of object 1 */
  706    REAL8 *S1y,                                  /**< [out] y-component of the dimensionless spin of object 1 */
  707    REAL8 *S1z,                                  /**< [out] z-component of the dimensionless spin of object 1 */
  708    REAL8 *S2x,                                  /**< [out] x-component of the dimensionless spin of object 2 */
  709    REAL8 *S2y,                                  /**< [out] y-component of the dimensionless spin of object 2 */
  710    REAL8 *S2z,                                  /**< [out] z-component of the dimensionless spin of object 2 */
  711    REAL8 *deltaF,                               /**< [out] sampling interval (s) */
  712    REAL8 *f_min,                                /**< [out] starting GW frequency (Hz) */
  713    REAL8 *f_max,                                /**< [out] ending GW frequency (Hz) */
  714    REAL8 *f_ref,                                /**< [out] reference GW frequency (Hz) */
  715    REAL8 *phiRef,                               /**< [out] reference phase (rad) */
  716    REAL8 *distance,                             /**< [out] distance of source (m) */
  717    REAL8 *inclination,                          /**< [out] inclination of source (rad) */
  718    LALDict *params                              /**< Input lal dictionary with waveform (and optional) parameters **/
  719)
  720{
  721    *m1 = XLALSimInspiralWaveformParamsLookupMass1(params);
  722    *m2 = XLALSimInspiralWaveformParamsLookupMass2(params);
  723    *S1x = XLALSimInspiralWaveformParamsLookupSpin1x(params);
  724    *S1y = XLALSimInspiralWaveformParamsLookupSpin1y(params);
  725    *S1z = XLALSimInspiralWaveformParamsLookupSpin1z(params);
  726    *S2x = XLALSimInspiralWaveformParamsLookupSpin2x(params);
  727    *S2y = XLALSimInspiralWaveformParamsLookupSpin2y(params);
  728    *S2z = XLALSimInspiralWaveformParamsLookupSpin2z(params);
  729    *deltaF = XLALSimInspiralWaveformParamsLookupDeltaF(params);
  730    *f_min = XLALSimInspiralWaveformParamsLookupF22Start(params);
  731    *f_max = XLALSimInspiralWaveformParamsLookupFMax(params);
  732    *f_ref = XLALSimInspiralWaveformParamsLookupF22Ref(params);
  733    *phiRef = XLALSimInspiralWaveformParamsLookupRefPhase(params);
  734    *distance = XLALSimInspiralWaveformParamsLookupDistance(params);
  735    *inclination = XLALSimInspiralWaveformParamsLookupInclination(params);
  736 
  737    return;
  738}
  739 
  740 
  741 
  742 
  743 
  744 /** @} */
  745 
  746/**
  747 * @name General Waveform Switching Generation Routines
  748 * @{
  749 */
  750 
  751/**
  752 * Chooses between different approximants when requesting a waveform to be generated
  753 * For spinning waveforms, all known spin effects up to given PN order are included
  754 * Returns the waveform in the time domain.
  755 *
  756 * The parameters passed must be in SI units.
  757 */
  758int XLALSimInspiralChooseTDWaveform(
  759    REAL8TimeSeries **hplus,                    /**< +-polarization waveform */
  760    REAL8TimeSeries **hcross,                   /**< x-polarization waveform */
  761    const REAL8 m1,                             /**< mass of companion 1 (kg) */
  762    const REAL8 m2,                             /**< mass of companion 2 (kg) */
  763    const REAL8 S1x,                            /**< x-component of the dimensionless spin of object 1 */
  764    const REAL8 S1y,                            /**< y-component of the dimensionless spin of object 1 */
  765    const REAL8 S1z,                            /**< z-component of the dimensionless spin of object 1 */
  766    const REAL8 S2x,                            /**< x-component of the dimensionless spin of object 2 */
  767    const REAL8 S2y,                            /**< y-component of the dimensionless spin of object 2 */
  768    const REAL8 S2z,                            /**< z-component of the dimensionless spin of object 2 */
  769    const REAL8 distance,                       /**< distance of source (m) */
  770    const REAL8 inclination,                    /**< inclination of source (rad) */
  771    const REAL8 phiRef,                         /**< reference orbital phase (rad) */
  772    const REAL8 longAscNodes,                   /**< longitude of ascending nodes, degenerate with the polarization angle, Omega in documentation */
  773    const REAL8 eccentricity,                   /**< eccentrocity at reference epoch */
  774    const REAL8 UNUSED meanPerAno,              /**< mean anomaly of periastron */
  775    const REAL8 deltaT,                         /**< sampling interval (s) */
  776    const REAL8 f_min,                          /**< starting GW frequency (Hz) */
  777    REAL8 f_ref,                                /**< reference GW frequency (Hz) */
  778    LALDict *params,                            /**< LAL dictionary containing accessory parameters */
  779    const Approximant approximant               /**< post-Newtonian approximant to use for waveform production */
  780    )
  781{
  782        LALSimInspiralGenerator *generator;
  783    int ret;
  784 
  785    generator = XLALSimInspiralChooseGenerator(approximant, params);
  786    XLAL_CHECK(generator, XLAL_EFUNC);
  787 
  788    if (params == NULL) {
  789        params = XLALCreateDict();
  790    }
  791    else {
  792        params = XLALDictDuplicate(params);
  793    }
  794    XLAL_CHECK(params, XLAL_EFUNC);
  795 
  796    XLALSimInspiralWaveformParamsInsertMass1(params, m1);
  797    XLALSimInspiralWaveformParamsInsertMass2(params, m2);
  798    XLALSimInspiralWaveformParamsInsertSpin1x(params, S1x);
  799    XLALSimInspiralWaveformParamsInsertSpin1y(params, S1y);
  800    XLALSimInspiralWaveformParamsInsertSpin1z(params, S1z);
  801    XLALSimInspiralWaveformParamsInsertSpin2x(params, S2x);
  802    XLALSimInspiralWaveformParamsInsertSpin2y(params, S2y);
  803    XLALSimInspiralWaveformParamsInsertSpin2z(params, S2z);
  804    XLALSimInspiralWaveformParamsInsertDistance(params, distance);
  805    XLALSimInspiralWaveformParamsInsertInclination(params, inclination);
  806    XLALSimInspiralWaveformParamsInsertRefPhase(params, phiRef);
  807    XLALSimInspiralWaveformParamsInsertLongAscNodes(params, longAscNodes);
  808    XLALSimInspiralWaveformParamsInsertEccentricity(params, eccentricity);
  809    XLALSimInspiralWaveformParamsInsertMeanPerAno(params, meanPerAno);
  810    XLALSimInspiralWaveformParamsInsertDeltaT(params, deltaT);
  811    XLALSimInspiralWaveformParamsInsertF22Start(params, f_min);
  812    XLALSimInspiralWaveformParamsInsertF22Ref(params, f_ref);
  813 
  814    ret = XLALSimInspiralGenerateTDWaveform(hplus, hcross, params, generator);
  815    XLALDestroyDict(params);
  816    XLALDestroySimInspiralGenerator(generator);
  817 
  818    return ret;
  819}
  820 
  821/**
  822 * Chooses between different approximants when requesting a waveform to be generated
  823 * For spinning waveforms, all known spin effects up to given PN order are included
  824 * Returns the waveform in the frequency domain.
  825 */
  826int XLALSimInspiralChooseFDWaveform(
  827    COMPLEX16FrequencySeries **hptilde,     /**< FD plus polarization */
  828    COMPLEX16FrequencySeries **hctilde,     /**< FD cross polarization */
  829    const REAL8 m1,                         /**< mass of companion 1 (kg) */
  830    const REAL8 m2,                         /**< mass of companion 2 (kg) */
  831    const REAL8 S1x,                        /**< x-component of the dimensionless spin of object 1 */
  832    const REAL8 S1y,                        /**< y-component of the dimensionless spin of object 1 */
  833    const REAL8 S1z,                        /**< z-component of the dimensionless spin of object 1 */
  834    const REAL8 S2x,                        /**< x-component of the dimensionless spin of object 2 */
  835    const REAL8 S2y,                        /**< y-component of the dimensionless spin of object 2 */
  836    const REAL8 S2z,                        /**< z-component of the dimensionless spin of object 2 */
  837    const REAL8 distance,                   /**< distance of source (m) */
  838    const REAL8 inclination,                /**< inclination of source (rad) */
  839    const REAL8 phiRef,                     /**< reference orbital phase (rad) */
  840    const REAL8 longAscNodes,               /**< longitude of ascending nodes, degenerate with the polarization angle, Omega in documentation */
  841    const REAL8 eccentricity,               /**< eccentricity at reference epoch */
  842    const REAL8 UNUSED meanPerAno,          /**< mean anomaly of periastron */
  843    // frequency sampling parameters, no default value
  844    const REAL8 deltaF,                     /**< sampling interval (Hz) */
  845    const REAL8 f_min,                      /**< starting GW frequency (Hz) */
  846    const REAL8 f_max,                      /**< ending GW frequency (Hz) */
  847    REAL8 f_ref,                            /**< Reference frequency (Hz) */
  848    LALDict *params,                     /**< LAL dictionary containing accessory parameters */
  849    const Approximant approximant           /**< post-Newtonian approximant to use for waveform production */
  850    )
  851{
  852        LALSimInspiralGenerator *generator;
  853    int ret;
  854 
  855    generator = XLALSimInspiralChooseGenerator(approximant, params);
  856    XLAL_CHECK(generator, XLAL_EFUNC);
  857 
  858    if (params == NULL) {
  859        params = XLALCreateDict();
  860    }
  861    else {
  862        params = XLALDictDuplicate(params);
  863    }
  864    XLAL_CHECK(params, XLAL_EFUNC);
  865 
  866    /* Avoid duplication of arguments when called from XLALSimInspiralChoose(Generate)TDWaveform  */
  867    const char *remove_keys[12] = {"total_mass", "chirp_mass", "mass_difference", "reduced_mass", "mass_ratio", "sym_mass_ratio", \
  868       "spin1_norm", "spin1_tilt", "spin1_phi", "spin2_norm", "spin2_tilt", "spin2_phi"};
  869    for(size_t j = 0; j < sizeof(remove_keys)/sizeof(*remove_keys); ++j){
  870      if (XLALDictContains(params, remove_keys[j]))
  871        XLALDictPop(params, remove_keys[j]);
  872    }
  873 
  874    XLALSimInspiralWaveformParamsInsertMass1(params, m1);
  875    XLALSimInspiralWaveformParamsInsertMass2(params, m2);
  876    XLALSimInspiralWaveformParamsInsertSpin1x(params, S1x);
  877    XLALSimInspiralWaveformParamsInsertSpin1y(params, S1y);
  878    XLALSimInspiralWaveformParamsInsertSpin1z(params, S1z);
  879    XLALSimInspiralWaveformParamsInsertSpin2x(params, S2x);
  880    XLALSimInspiralWaveformParamsInsertSpin2y(params, S2y);
  881    XLALSimInspiralWaveformParamsInsertSpin2z(params, S2z);
  882    XLALSimInspiralWaveformParamsInsertDistance(params, distance);
  883    XLALSimInspiralWaveformParamsInsertInclination(params, inclination);
  884    XLALSimInspiralWaveformParamsInsertRefPhase(params, phiRef);
  885    XLALSimInspiralWaveformParamsInsertLongAscNodes(params, longAscNodes);
  886    XLALSimInspiralWaveformParamsInsertEccentricity(params, eccentricity);
  887    XLALSimInspiralWaveformParamsInsertMeanPerAno(params, meanPerAno);
  888    XLALSimInspiralWaveformParamsInsertDeltaF(params, deltaF);
  889    XLALSimInspiralWaveformParamsInsertF22Start(params, f_min);
  890    XLALSimInspiralWaveformParamsInsertFMax(params, f_max);
  891    XLALSimInspiralWaveformParamsInsertF22Ref(params, f_ref);
  892 
  893    ret = XLALSimInspiralGenerateFDWaveform(hptilde, hctilde, params, generator);
  894    XLALDestroyDict(params);
  895    XLALDestroySimInspiralGenerator(generator);
  896 
  897    return ret;
  898}
  899 
  900/**
  901 * @brief Generates an time domain inspiral waveform using the specified approximant; the
  902 * resulting waveform is appropriately conditioned, suitable for injection into data,
  903 * and decomposed into the (2, \f$\pm\f$ 2), spin -2 weighted spherical harmonic modes.
  904 * NOTE: This is an algebraic decomposition, and will only be correct for approximants
  905 * which use only the dominant 2, \f$\pm\f$ 2 mode.
  906 *
  907 * For spinning waveforms, all known spin effects up to given PN order are included
  908 *
  909 * This routine can generate FD approximants and transform them into the time domain.
  910 * Waveforms are generated beginning at a slightly lower starting frequency and tapers
  911 * are put in this early region so that the waveform smoothly turns on.  Artifacts at
  912 * the very end of the waveform are also tapered.  The resulting waveform is high-pass
  913 * filtered at frequency f_min so that it should have little content at lower frequencies.
  914 *
  915 * This routine used to have one additional parameter relative to XLALSimInspiralChooseTDWaveform:
  916 * the redshift, z, of the waveform, which is now stuffed into the LALDict structure.
  917 * This should be set to zero (default value) for sources in the nearby universe (that are nearly at rest relative to the
  918 * earth).  For sources at cosmological distances, the mass parameters m1 and m2 should
  919 * be interpreted as the physical (source frame) masses of the bodies and the distance
  920 * parameter r is the comoving (transverse) distance.  If the calling routine has already
  921 * applied cosmological "corrections" to m1 and m2 and regards r as a luminosity distance
  922 * then the redshift factor should again be set to zero.
  923 *
  924 * @note The parameters passed must be in SI units.
  925 */
  926SphHarmTimeSeries* XLALSimInspiralTDModesFromPolarizations(
  927    REAL8 m1,                                   /**< mass of companion 1 (kg) */
  928    REAL8 m2,                                   /**< mass of companion 2 (kg) */
  929    REAL8 S1x,                                  /**< x-component of the dimensionless spin of object 1 */
  930    REAL8 S1y,                                  /**< y-component of the dimensionless spin of object 1 */
  931    REAL8 S1z,                                  /**< z-component of the dimensionless spin of object 1 */
  932    REAL8 S2x,                                  /**< x-component of the dimensionless spin of object 2 */
  933    REAL8 S2y,                                  /**< y-component of the dimensionless spin of object 2 */
  934    REAL8 S2z,                                  /**< z-component of the dimensionless spin of object 2 */
  935    REAL8 distance,                             /**< distance of source (m) */
  936    REAL8 phiRef,                               /**< reference orbital phase (rad) */
  937    REAL8 longAscNodes,                         /**< longitude of ascending nodes, degenerate with the polarization angle, Omega in documentation */
  938    REAL8 eccentricity,                         /**< eccentrocity at reference epoch */
  939    REAL8 meanPerAno,                           /**< mean anomaly of periastron */
  940    REAL8 deltaT,                               /**< sampling interval (s) */
  941    REAL8 f_min,                                /**< starting GW frequency (Hz) */
  942    REAL8 f_ref,                                /**< reference GW frequency (Hz) */
  943    LALDict *LALparams,                         /**< LAL dictionary containing accessory parameters */
  944    Approximant approximant                     /**< post-Newtonian approximant to use for waveform production */
  945    )
  946{
  947 
  948    if( !checkTransverseSpinsZero(S1x, S1y, S2x, S2y) ) {
  949      XLALPrintError("Non-zero transverse spins were given, but it is not possible to recover modes from H+ and Hx for precessing waveforms.\n");
  950      XLAL_ERROR_NULL(XLAL_EINVAL);
  951    }
  952 
  953    REAL8TimeSeries *hplus = NULL, *hcross = NULL;
  954    COMPLEX16TimeSeries *h22,*h2m2;
  955    SphHarmTimeSeries *hlm;
  956    UINT4 j;
  957    int retval;
  958    float fac = XLALSpinWeightedSphericalHarmonic(0., 0., -2, 2,2);
  959 
  960    /* Generate waveform via on-axis emission. Assumes only (2,2) and (2,-2) emission */
  961    retval = XLALSimInspiralTD(&hplus, &hcross, m1, m2, S1x, S1y, S1z, S2x, S2y, S2z, distance, 0., phiRef, longAscNodes, eccentricity, meanPerAno, deltaT, f_min, f_ref, LALparams, approximant);
  962    if (retval < 0)
  963        XLAL_ERROR_NULL(XLAL_EFUNC);
  964 
  965    /* Step 1: Create COMPLEX16 TimeSeries and populate them */
  966    h22 = XLALCreateCOMPLEX16TimeSeries("h22", &(hplus)->epoch, 0, deltaT, &lalStrainUnit, (hplus)->data->length);
  967    h2m2 = XLALCreateCOMPLEX16TimeSeries("h2m2", &(hplus)->epoch, 0, deltaT, &lalStrainUnit, (hplus)->data->length);
  968    for (j=0; j< (hplus)->data->length; j++) {
  969      h22->data->data[j] = ((hplus)->data->data[j] - I*((hcross)->data->data[j]))/fac;
  970      h2m2->data->data[j] = ((hplus)->data->data[j] + I*((hcross)->data->data[j]))/fac;
  971    }
  972 
  973    /* Step 2: Add them into the data */
  974    hlm = XLALSphHarmTimeSeriesAddMode(NULL, h22, 2, 2);
  975    hlm = XLALSphHarmTimeSeriesAddMode(hlm, h2m2, 2, -2);
  976 
  977    /* Step 3: Clean up */
  978    XLALDestroyREAL8TimeSeries(hplus);
  979    XLALDestroyREAL8TimeSeries(hcross);
  980    XLALDestroyCOMPLEX16TimeSeries(h22);
  981    XLALDestroyCOMPLEX16TimeSeries(h2m2);
  982 
  983    return hlm;
  984}
  985 
  986/** Helper routines for XLALSimInspiralTD(): performs conditioning of a TD waveform */
  987int XLALSimInspiralTDFromTD(
  988    REAL8TimeSeries **hplus,                    /**< +-polarization waveform */
  989    REAL8TimeSeries **hcross,                   /**< x-polarization waveform */
  990    REAL8 m1,                                   /**< mass of companion 1 (kg) */
  991    REAL8 m2,                                   /**< mass of companion 2 (kg) */
  992    REAL8 S1x,                                  /**< x-component of the dimensionless spin of object 1 */
  993    REAL8 S1y,                                  /**< y-component of the dimensionless spin of object 1 */
  994    REAL8 S1z,                                  /**< z-component of the dimensionless spin of object 1 */
  995    REAL8 S2x,                                  /**< x-component of the dimensionless spin of object 2 */
  996    REAL8 S2y,                                  /**< y-component of the dimensionless spin of object 2 */
  997    REAL8 S2z,                                  /**< z-component of the dimensionless spin of object 2 */
  998    REAL8 distance,                             /**< distance of source (m) */
  999    REAL8 inclination,                          /**< inclination of source (rad) */
 1000    REAL8 phiRef,                               /**< reference orbital phase (rad) */
 1001    REAL8 longAscNodes,                         /**< longitude of ascending nodes, degenerate with the polarization angle, Omega in documentation */
 1002    REAL8 eccentricity,                         /**< eccentrocity at reference epoch */
 1003    REAL8 meanPerAno,                           /**< mean anomaly of periastron */
 1004    REAL8 deltaT,                               /**< sampling interval (s) */
 1005    REAL8 f_min,                                /**< starting GW frequency (Hz) */
 1006    REAL8 f_ref,                                /**< reference GW frequency (Hz) */
 1007    LALDict *LALparams,                         /**< LAL dictionary containing accessory parameters */
 1008    Approximant approximant                     /**< post-Newtonian approximant to use for waveform production */
 1009)
 1010{
 1011    const double extra_time_fraction = 0.1; /* fraction of waveform duration to add as extra time for tapering */
 1012    const double extra_cycles = 3.0; /* more extra time measured in cycles at the starting frequency */
 1013    double original_f_min = f_min; /* f_min might be overwritten below, so keep original value */
 1014    double tchirp, tmerge, textra;
 1015    double fisco, fstart;
 1016    double s;
 1017    int retval;
 1018 
 1019    if (!XLALSimInspiralImplementedTDApproximants(approximant))
 1020        XLAL_ERROR(XLAL_EINVAL, "Invalid approximant: not a TD approximant");
 1021 
 1022    /* adjust the reference frequency for certain precessing approximants:
 1023     * if that approximate interprets f_ref==0 to be f_min, set f_ref=f_min;
 1024     * otherwise do nothing */
 1025    FIX_REFERENCE_FREQUENCY(f_ref, f_min, approximant);
 1026 
 1027    /* apply redshift correction to dimensionful source-frame quantities */
 1028    REAL8 z=XLALSimInspiralWaveformParamsLookupRedshift(LALparams);
 1029    if (z != 0.0) {
 1030        m1 *= (1.0 + z);
 1031        m2 *= (1.0 + z);
 1032        distance *= (1.0 + z);  /* change from comoving (transverse) distance to luminosity distance */
 1033    }
 1034    /* set redshift to zero so we don't accidentally apply it again later */
 1035    z=0.;
 1036    if (LALparams)
 1037      XLALSimInspiralWaveformParamsInsertRedshift(LALparams,z);
 1038 
 1039    /* if the requested low frequency is below the lowest Kerr ISCO
 1040     * frequency then change it to that frequency */
 1041    fisco = 1.0 / (pow(9.0, 1.5) * LAL_PI * (m1 + m2) * LAL_MTSUN_SI / LAL_MSUN_SI);
 1042    if (f_min > fisco)
 1043        f_min = fisco;
 1044 
 1045    /* upper bound on the chirp time starting at f_min */
 1046    tchirp = XLALSimInspiralChirpTimeBound(f_min, m1, m2, S1z, S2z);
 1047 
 1048    /* upper bound on the final black hole spin */
 1049    s = XLALSimInspiralFinalBlackHoleSpinBound(S1z, S2z);
 1050 
 1051    /* upper bound on the final plunge, merger, and ringdown time */
 1052    tmerge = XLALSimInspiralMergeTimeBound(m1, m2) + XLALSimInspiralRingdownTimeBound(m1 + m2, s);
 1053 
 1054    /* extra time to include for all waveforms to take care of situations
 1055     * where the frequency is close to merger (and is sweeping rapidly):
 1056     * this is a few cycles at the low frequency */
 1057    textra = extra_cycles / f_min;
 1058 
 1059    /* time domain approximant: condition by generating a waveform
 1060     * with a lower starting frequency and apply tapers in the
 1061     * region between that lower frequency and the requested
 1062     * frequency f_min; here compute a new lower frequency */
 1063    fstart = XLALSimInspiralChirpStartFrequencyBound((1.0 + extra_time_fraction) * tchirp + tmerge + textra, m1, m2);
 1064 
 1065    /* generate the waveform in the time domain starting at fstart */
 1066    retval = XLALSimInspiralChooseTDWaveform(hplus, hcross, m1, m2, S1x, S1y, S1z, S2x, S2y, S2z, distance, inclination, phiRef, longAscNodes, eccentricity, meanPerAno, deltaT, fstart, f_ref, LALparams, approximant);
 1067    if (retval < 0)
 1068        XLAL_ERROR(XLAL_EFUNC);
 1069 
 1070    /* condition the time domain waveform by tapering in the extra time
 1071        * at the beginning and high-pass filtering above original f_min */
 1072    XLALSimInspiralTDConditionStage1(*hplus, *hcross, extra_time_fraction * tchirp + textra, original_f_min);
 1073 
 1074    /* final tapering at the beginning and at the end to remove filter transients */
 1075 
 1076    /* waveform should terminate at a frequency >= Schwarzschild ISCO
 1077        * so taper one cycle at this frequency at the end; should not make
 1078        * any difference to IMR waveforms */
 1079    fisco = 1.0 / (pow(6.0, 1.5) * LAL_PI * (m1 + m2) * LAL_MTSUN_SI / LAL_MSUN_SI);
 1080    XLALSimInspiralTDConditionStage2(*hplus, *hcross, f_min, fisco);
 1081 
 1082    return 0;
 1083}
 1084 
 1085/** Helper routines for XLALSimInspiralTD(): performs conditioning of a FD waveform and transforms it to TD */
 1086int XLALSimInspiralTDFromFD(
 1087    REAL8TimeSeries **hplus,                    /**< +-polarization waveform */
 1088    REAL8TimeSeries **hcross,                   /**< x-polarization waveform */
 1089    REAL8 m1,                                   /**< mass of companion 1 (kg) */
 1090    REAL8 m2,                                   /**< mass of companion 2 (kg) */
 1091    REAL8 S1x,                                  /**< x-component of the dimensionless spin of object 1 */
 1092    REAL8 S1y,                                  /**< y-component of the dimensionless spin of object 1 */
 1093    REAL8 S1z,                                  /**< z-component of the dimensionless spin of object 1 */
 1094    REAL8 S2x,                                  /**< x-component of the dimensionless spin of object 2 */
 1095    REAL8 S2y,                                  /**< y-component of the dimensionless spin of object 2 */
 1096    REAL8 S2z,                                  /**< z-component of the dimensionless spin of object 2 */
 1097    REAL8 distance,                             /**< distance of source (m) */
 1098    REAL8 inclination,                          /**< inclination of source (rad) */
 1099    REAL8 phiRef,                               /**< reference orbital phase (rad) */
 1100    REAL8 longAscNodes,                         /**< longitude of ascending nodes, degenerate with the polarization angle, Omega in documentation */
 1101    REAL8 eccentricity,                         /**< eccentrocity at reference epoch */
 1102    REAL8 meanPerAno,                           /**< mean anomaly of periastron */
 1103    REAL8 deltaT,                               /**< sampling interval (s) */
 1104    REAL8 f_min,                                /**< starting GW frequency (Hz) */
 1105    REAL8 f_ref,                                /**< reference GW frequency (Hz) */
 1106    LALDict *LALparams,                         /**< LAL dictionary containing accessory parameters */
 1107    Approximant approximant                     /**< post-Newtonian approximant to use for waveform production */
 1108)
 1109{
 1110    COMPLEX16FrequencySeries *hptilde = NULL;
 1111    COMPLEX16FrequencySeries *hctilde = NULL;
 1112    REAL8FFTPlan *plan;
 1113    size_t chirplen, end, k;
 1114    double tshift;
 1115    const double extra_time_fraction = 0.1; /* fraction of waveform duration to add as extra time for tapering */
 1116    const double extra_cycles = 3.0; /* more extra time measured in cycles at the starting frequency */
 1117    double original_f_min = f_min; /* f_min might be overwritten below, so keep original value */
 1118    double f_max = 0.5 / deltaT;
 1119    double tchirp, tmerge, textra;
 1120    double fisco, fstart;
 1121    double s;
 1122    int retval;
 1123 
 1124    if (!XLALSimInspiralImplementedFDApproximants(approximant))
 1125        XLAL_ERROR(XLAL_EINVAL, "Invalid approximant: not a FD approximant");
 1126 
 1127    /* adjust the reference frequency for certain precessing approximants:
 1128     * if that approximate interprets f_ref==0 to be f_min, set f_ref=f_min;
 1129     * otherwise do nothing */
 1130    FIX_REFERENCE_FREQUENCY(f_ref, f_min, approximant);
 1131 
 1132    /* apply redshift correction to dimensionful source-frame quantities */
 1133    REAL8 z=XLALSimInspiralWaveformParamsLookupRedshift(LALparams);
 1134    if (z != 0.0) {
 1135        m1 *= (1.0 + z);
 1136        m2 *= (1.0 + z);
 1137        distance *= (1.0 + z);  /* change from comoving (transverse) distance to luminosity distance */
 1138    }
 1139    /* set redshift to zero so we don't accidentally apply it again later */
 1140    z=0.;
 1141    if (LALparams)
 1142      XLALSimInspiralWaveformParamsInsertRedshift(LALparams,z);
 1143 
 1144    /* if the requested low frequency is below the lowest Kerr ISCO
 1145     * frequency then change it to that frequency */
 1146    fisco = 1.0 / (pow(9.0, 1.5) * LAL_PI * (m1 + m2) * LAL_MTSUN_SI / LAL_MSUN_SI);
 1147    if (f_min > fisco)
 1148        f_min = fisco;
 1149 
 1150    /* upper bound on the chirp time starting at f_min */
 1151    tchirp = XLALSimInspiralChirpTimeBound(f_min, m1, m2, S1z, S2z);
 1152 
 1153    /* upper bound on the final black hole spin */
 1154    s = XLALSimInspiralFinalBlackHoleSpinBound(S1z, S2z);
 1155 
 1156    /* upper bound on the final plunge, merger, and ringdown time */
 1157    tmerge = XLALSimInspiralMergeTimeBound(m1, m2) + XLALSimInspiralRingdownTimeBound(m1 + m2, s);
 1158 
 1159    /* extra time to include for all waveforms to take care of situations
 1160     * where the frequency is close to merger (and is sweeping rapidly):
 1161     * this is a few cycles at the low frequency */
 1162    textra = extra_cycles / f_min;
 1163 
 1164    /* generate the conditioned waveform in the frequency domain */
 1165    /* note: redshift factor has already been applied above */
 1166    /* set deltaF = 0 to get a small enough resolution */
 1167    retval = XLALSimInspiralFD(&hptilde, &hctilde, m1, m2, S1x, S1y, S1z, S2x, S2y, S2z, distance, inclination, phiRef, longAscNodes, eccentricity, meanPerAno, 0.0, f_min, f_max, f_ref, LALparams, approximant);
 1168    if (retval < 0)
 1169        XLAL_ERROR(XLAL_EFUNC);
 1170 
 1171    /* we want to make sure that this waveform will give something
 1172     * sensible if it is later transformed into the time domain:
 1173     * to avoid the end of the waveform wrapping around to the beginning,
 1174     * we shift waveform backwards in time and compensate for this
 1175     * shift by adjusting the epoch -- note that XLALSimInspiralFD
 1176     * guarantees that there is extra padding to do this */
 1177    tshift = round(textra / deltaT) * deltaT; /* integer number of samples */
 1178    for (k = 0; k < hptilde->data->length; ++k) {
 1179        double complex phasefac = cexp(2.0 * M_PI * I * k * hptilde->deltaF * tshift);
 1180        hptilde->data->data[k] *= phasefac;
 1181        hctilde->data->data[k] *= phasefac;
 1182    }
 1183    XLALGPSAdd(&hptilde->epoch, tshift);
 1184    XLALGPSAdd(&hctilde->epoch, tshift);
 1185 
 1186    /* transform the waveform into the time domain */
 1187    chirplen = 2 * (hptilde->data->length - 1);
 1188    *hplus = XLALCreateREAL8TimeSeries("H_PLUS", &hptilde->epoch, 0.0, deltaT, &lalStrainUnit, chirplen);
 1189    *hcross = XLALCreateREAL8TimeSeries("H_CROSS", &hctilde->epoch, 0.0, deltaT, &lalStrainUnit, chirplen);
 1190    plan = XLALCreateReverseREAL8FFTPlan(chirplen, 0);
 1191    if (!(*hplus) || !(*hcross) || !plan) {
 1192        XLALDestroyCOMPLEX16FrequencySeries(hptilde);
 1193        XLALDestroyCOMPLEX16FrequencySeries(hctilde);
 1194        XLALDestroyREAL8TimeSeries(*hcross);
 1195        XLALDestroyREAL8TimeSeries(*hplus);
 1196        XLALDestroyREAL8FFTPlan(plan);
 1197        XLAL_ERROR(XLAL_EFUNC);
 1198    }
 1199    XLALREAL8FreqTimeFFT(*hplus, hptilde, plan);
 1200    XLALREAL8FreqTimeFFT(*hcross, hctilde, plan);
 1201 
 1202    /* apply time domain filter at original f_min */
 1203    XLALHighPassREAL8TimeSeries(*hplus, original_f_min, 0.99, 8);
 1204    XLALHighPassREAL8TimeSeries(*hcross, original_f_min, 0.99, 8);
 1205 
 1206    /* compute how long a chirp we should have */
 1207    /* revised estimate of chirp length from new start frequency */
 1208    fstart = XLALSimInspiralChirpStartFrequencyBound((1.0 + extra_time_fraction) * tchirp, m1, m2);
 1209    tchirp = XLALSimInspiralChirpTimeBound(fstart, m1, m2, S1z, S2z);
 1210 
 1211    /* total expected chirp length includes merger */
 1212    chirplen = round((tchirp + tmerge) / deltaT);
 1213 
 1214    /* amount to snip off at the end is tshift */
 1215    end = (*hplus)->data->length - round(tshift / deltaT);
 1216 
 1217    /* snip off extra time at beginning and at the end */
 1218    XLALResizeREAL8TimeSeries(*hplus, end - chirplen, chirplen);
 1219    XLALResizeREAL8TimeSeries(*hcross, end - chirplen, chirplen);
 1220 
 1221    /* clean up */
 1222    XLALDestroyREAL8FFTPlan(plan);
 1223    XLALDestroyCOMPLEX16FrequencySeries(hptilde);
 1224    XLALDestroyCOMPLEX16FrequencySeries(hctilde);
 1225 
 1226    /* final tapering at the beginning and at the end to remove filter transients */
 1227 
 1228    /* waveform should terminate at a frequency >= Schwarzschild ISCO
 1229     * so taper one cycle at this frequency at the end; should not make
 1230     * any difference to IMR waveforms */
 1231    fisco = 1.0 / (pow(6.0, 1.5) * LAL_PI * (m1 + m2) * LAL_MTSUN_SI / LAL_MSUN_SI);
 1232    XLALSimInspiralTDConditionStage2(*hplus, *hcross, f_min, fisco);
 1233 
 1234    return 0;
 1235}
 1236 
 1237/**
 1238 * @brief Generates an time domain inspiral waveform using the specified approximant; the
 1239 * resulting waveform is appropriately conditioned and suitable for injection into data.
 1240 *
 1241 * For spinning waveforms, all known spin effects up to given PN order are included
 1242 *
 1243 * This routine can generate FD approximants and transform them into the time domain.
 1244 * Waveforms are generated beginning at a slightly lower starting frequency and tapers
 1245 * are put in this early region so that the waveform smoothly turns on.  Artifacts at
 1246 * the very end of the waveform are also tapered.  The resulting waveform is high-pass
 1247 * filtered at frequency f_min so that it should have little content at lower frequencies.
 1248 
 1249 * If calling with precessing time-domain approximants for which the reference frequency
 1250 * is the starting frequency, or if calling with NR_hdf5 approximant, the starting
 1251 * frequency is not altered. Uses XLALSimInspiralGetSpinFreqFromApproximant to determine
 1252 * appropriate behaviour.
 1253 * Similarly, if calling time-domain models for which a starting frequency of
 1254 * zero is allowed (as set in
 1255 * XLALSimInspiralGetAllowZeroMinFreqFromApproximant), the starting frequency
 1256 * is never altered, independent of f_min.
 1257 *
 1258 * This routine used to have one additional parameter relative to XLALSimInspiralChooseTDWaveform:
 1259 * the redshift, z, of the waveform, which is now stuffed into the LALDict structure.
 1260 * This should be set to zero (default value) for sources in the nearby universe (that are nearly at rest relative to the
 1261 * earth).  For sources at cosmological distances, the mass parameters m1 and m2 should
 1262 * be interpreted as the physical (source frame) masses of the bodies and the distance
 1263 * parameter r is the comoving (transverse) distance.  If the calling routine has already
 1264 * applied cosmological "corrections" to m1 and m2 and regards r as a luminosity distance
 1265 * then the redshift factor should again be set to zero.
 1266 *
 1267 * @note The parameters passed must be in SI units.
 1268 */
 1269int XLALSimInspiralTD(
 1270    REAL8TimeSeries **hplus,                    /**< +-polarization waveform */
 1271    REAL8TimeSeries **hcross,                   /**< x-polarization waveform */
 1272    REAL8 m1,                                   /**< mass of companion 1 (kg) */
 1273    REAL8 m2,                                   /**< mass of companion 2 (kg) */
 1274    REAL8 S1x,                                  /**< x-component of the dimensionless spin of object 1 */
 1275    REAL8 S1y,                                  /**< y-component of the dimensionless spin of object 1 */
 1276    REAL8 S1z,                                  /**< z-component of the dimensionless spin of object 1 */
 1277    REAL8 S2x,                                  /**< x-component of the dimensionless spin of object 2 */
 1278    REAL8 S2y,                                  /**< y-component of the dimensionless spin of object 2 */
 1279    REAL8 S2z,                                  /**< z-component of the dimensionless spin of object 2 */
 1280    REAL8 distance,                             /**< distance of source (m) */
 1281    REAL8 inclination,                          /**< inclination of source (rad) */
 1282    REAL8 phiRef,                               /**< reference orbital phase (rad) */
 1283    REAL8 longAscNodes,                         /**< longitude of ascending nodes, degenerate with the polarization angle, Omega in documentation */
 1284    REAL8 eccentricity,                         /**< eccentrocity at reference epoch */
 1285    REAL8 meanPerAno,                           /**< mean anomaly of periastron */
 1286    REAL8 deltaT,                               /**< sampling interval (s) */
 1287    REAL8 f_min,                                /**< starting GW frequency (Hz) */
 1288    REAL8 f_ref,                                /**< reference GW frequency (Hz) */
 1289    LALDict *LALparams,                         /**< LAL dictionary containing accessory parameters */
 1290    Approximant approximant                     /**< post-Newtonian approximant to use for waveform production */
 1291    )
 1292{
 1293    int ret;
 1294 
 1295    /* set condition flag */
 1296    if (LALparams == NULL) {
 1297        LALparams = XLALCreateDict();
 1298    } else {
 1299        LALparams = XLALDictDuplicate(LALparams);
 1300        if (XLALDictContains(LALparams, "condition"))
 1301            XLALDictRemove(LALparams, "condition");
 1302    }
 1303    XLALDictInsertINT4Value(LALparams, "condition", 2);
 1304 
 1305    ret = XLALSimInspiralChooseTDWaveform(hplus, hcross, m1, m2, S1x, S1y, S1z, S2x, S2y, S2z, distance, inclination, phiRef, longAscNodes, eccentricity, meanPerAno, deltaT, f_min, f_ref, LALparams, approximant);
 1306    XLALDestroyDict(LALparams);
 1307 
 1308    return ret;
 1309}
 1310 
 1311/**
 1312 * @brief Generates a frequency domain inspiral waveform using the specified approximant; the
 1313 * resulting waveform is appropriately conditioned and suitable for injection into data.
 1314 *
 1315 * For spinning waveforms, all known spin effects up to given PN order are included.
 1316 *
 1317 * This routine can generate TD approximants and transform them into the frequency domain.
 1318 * Waveforms are generated beginning at a slightly lower starting frequency and tapers
 1319 * are put in this early region so that the waveform smoothly turns on.
 1320 *
 1321 * If an FD approximant is used, this routine applies tapers in the frequency domain
 1322 * between the slightly-lower frequency and the requested f_min.  Also, the phase of the
 1323 * waveform is adjusted to introduce a time shift.  This time shift should allow the
 1324 * resulting waveform to be Fourier transformed into the time domain without wrapping
 1325 * the end of the waveform to the beginning.
 1326 *
 1327 * This routine assumes that f_max is the Nyquist frequency of a corresponding time-domain
 1328 * waveform, so that deltaT = 0.5 / f_max.  If deltaF is set to 0 then this routine computes
 1329 * a deltaF that is small enough to represent the Fourier transform of a time-domain waveform
 1330 * while ensuring the length of the time-domain signal if a power of 2.
 1331 * If deltaF is specified but f_max / deltaF is not a power of 2, and the waveform approximant
 1332 * is a time-domain approximant, then f_max is increased so that f_max / deltaF is the next
 1333 * power of 2.  (If the user wishes to discard the extra high frequency content, this must
 1334 * be done separately.)
 1335 *
 1336 * The user should take care to ensure that deltaF is sufficiently small to contain the full
 1337 * signal (time series duration = 1 / deltaF). If the provided deltaF is too large the signal
 1338 * will be abruptly truncated for time-domain waveform generators. For frequency-domain
 1339 * generators the signal will be aliased in the frequency domain.
 1340 *
 1341 * Similarly, if the provided f_max is less than the ringdown frequency the underlying waveform
 1342 * generator may raise an error. If not, the frequency domain signal will be aliased in the
 1343 * frequency domain.
 1344 *
 1345 * Some waveform approximants have built in checks for the maximum frequency and signal length
 1346 *
 1347 * This routine used to have one additional parameter relative to XLALSimInspiralChooseTDWaveform:
 1348 * the redshift, z, of the waveform, which is now stuffed into the LALDict.
 1349 * This should be set to zero (default value) for sources in the nearby universe (that are nearly at rest relative to the
 1350 * earth).  For sources at cosmological distances, the mass parameters m1 and m2 should
 1351 * be interpreted as the physical (source frame) masses of the bodies and the distance
 1352 * parameter r is the comoving (transverse) distance.  If the calling routine has already
 1353 * applied cosmological "corrections" to m1 and m2 and regards r as a luminosity distance
 1354 * then the redshift factor should again be set to zero.
 1355 *
 1356 *
 1357 * @note The parameters passed must be in SI units.
 1358 */
 1359int XLALSimInspiralFD(
 1360    COMPLEX16FrequencySeries **hptilde,     /**< FD plus polarization */
 1361    COMPLEX16FrequencySeries **hctilde,     /**< FD cross polarization */
 1362    REAL8 m1,                               /**< mass of companion 1 (kg) */
 1363    REAL8 m2,                               /**< mass of companion 2 (kg) */
 1364    REAL8 S1x,                              /**< x-component of the dimensionless spin of object 1 */
 1365    REAL8 S1y,                              /**< y-component of the dimensionless spin of object 1 */
 1366    REAL8 S1z,                              /**< z-component of the dimensionless spin of object 1 */
 1367    REAL8 S2x,                              /**< x-component of the dimensionless spin of object 2 */
 1368    REAL8 S2y,                              /**< y-component of the dimensionless spin of object 2 */
 1369    REAL8 S2z,                              /**< z-component of the dimensionless spin of object 2 */
 1370    REAL8 distance,                         /**< distance of source (m) */
 1371    REAL8 inclination,                      /**< inclination of source (rad) */
 1372    REAL8 phiRef,                           /**< reference orbital phase (rad) */
 1373    REAL8 longAscNodes,                     /**< longitude of ascending nodes, degenerate with the polarization angle, Omega in documentation */
 1374    REAL8 eccentricity,                     /**< eccentricity at reference epoch */
 1375    REAL8 meanPerAno,                       /**< mean anomaly of periastron */
 1376    REAL8 deltaF,                           /**< sampling interval (Hz) */
 1377    REAL8 f_min,                            /**< starting GW frequency (Hz) */
 1378    REAL8 f_max,                            /**< ending GW frequency (Hz) */
 1379    REAL8 f_ref,                            /**< Reference frequency (Hz) */
 1380    LALDict *LALparams,                     /**< LAL dictionary containing accessory parameters */
 1381    Approximant approximant                 /**< post-Newtonian approximant to use for waveform production */
 1382    )
 1383{
 1384    int ret;
 1385 
 1386    /* set condition flag */
 1387    if (LALparams == NULL) {
 1388        LALparams = XLALCreateDict();
 1389    } else {
 1390        LALparams = XLALDictDuplicate(LALparams);
 1391        if (XLALDictContains(LALparams, "condition"))
 1392            XLALDictRemove(LALparams, "condition");
 1393    }
 1394    XLALDictInsertINT4Value(LALparams, "condition", 2);
 1395 
 1396    ret = XLALSimInspiralChooseFDWaveform(hptilde, hctilde, m1, m2, S1x, S1y, S1z, S2x, S2y, S2z, distance, inclination, phiRef, longAscNodes, eccentricity, meanPerAno, deltaF, f_min, f_max, f_ref, LALparams, approximant);
 1397    XLALDestroyDict(LALparams);
 1398 
 1399    return ret;
 1400}
 1401 
 1402/**
 1403 * @deprecated Use XLALSimInspiralChooseTDWaveform() instead
 1404 *
 1405 * Chooses between different approximants when requesting a waveform to be generated
 1406 * For spinning waveforms, all known spin effects up to given PN order are included
 1407 *
 1408 * The parameters passed must be in SI units.
 1409 */
 1410int XLALSimInspiralChooseWaveform(
 1411    REAL8TimeSeries **hplus,                    /**< +-polarization waveform */
 1412    REAL8TimeSeries **hcross,                   /**< x-polarization waveform */
 1413    const REAL8 m1,                                   /**< mass of companion 1 (kg) */
 1414    const REAL8 m2,                                   /**< mass of companion 2 (kg) */
 1415    const REAL8 S1x,                                  /**< x-component of the dimensionless spin of object 1 */
 1416    const REAL8 S1y,                                  /**< y-component of the dimensionless spin of object 1 */
 1417    const REAL8 S1z,                                  /**< z-component of the dimensionless spin of object 1 */
 1418    const REAL8 S2x,                                  /**< x-component of the dimensionless spin of object 2 */
 1419    const REAL8 S2y,                                  /**< y-component of the dimensionless spin of object 2 */
 1420    const REAL8 S2z,                                  /**< z-component of the dimensionless spin of object 2 */
 1421    const REAL8 distance,                             /**< distance of source (m) */
 1422    const REAL8 inclination,                          /**< inclination of source (rad) */
 1423    const REAL8 phiRef,                               /**< reference orbital phase (rad) */
 1424    const REAL8 longAscNodes,                         /**< longitude of ascending nodes, degenerate with the polarization angle, Omega in documentation */
 1425    const REAL8 eccentricity,                         /**< eccentrocity at reference epoch */
 1426    const REAL8 meanPerAno,                           /**< mean anomaly of periastron */
 1427    // frequency sampling parameters, no default value
 1428    const REAL8 deltaT,                               /**< sampling interval (s) */
 1429    const REAL8 f_min,                                /**< starting GW frequency (Hz) */
 1430    const REAL8 f_ref,                                /**< reference GW frequency (Hz) */
 1431    LALDict *LALpars,                                 /**< LAL dictionary containing accessory parameters */
 1432    const Approximant approximant                     /**< post-Newtonian approximant to use for waveform production */)
 1433{
 1434    XLAL_PRINT_DEPRECATION_WARNING("XLALSimInspiralChooseTDWaveform");
 1435 
 1436    return XLALSimInspiralChooseTDWaveform(hplus, hcross, m1, m2, S1x, S1y, S1z, S2x, S2y, S2z,
 1437                       distance, inclination, phiRef, longAscNodes,
 1438                       eccentricity, meanPerAno, deltaT, f_min, f_ref,
 1439                       LALpars, approximant);
 1440}
 1441 
 1442/** @} */
 1443 
 1444/**
 1445 * @name General Waveform Switching Mode Generation Routines
 1446 * @{
 1447 */
 1448 
 1449/**
 1450 * Interface to compute a set of -2 spin-weighted spherical harmonic modes
 1451 * for a binary inspiral for a given waveform approximant.
 1452 * PN Approximants (TaylorT1 - T4), EOBNRv2 (EOBNRv2HM), NRSur7dq2, NRSur7dq4
 1453 * NRHybSur3dq8 and spin-precessing SpintaylorT1, T5, T4 are implemented.
 1454 *
 1455 * The EOBNRv2 model returns the (2,2), (2,1), (3,3), (4,4), and (5,5) modes.
 1456 * Note that the inclination parameter is not passed to create hlm modes,
 1457 * hence to recover the correct h+,x one has to combine the hlm modes with
 1458 * Euler angles alpha=0, iota=inclination, psi=0,Pi/2 (according to the approximat) i.e.
 1459 * (h+ + I hx) (psi,iota,alpha)= e^(-2Ialpha) Sum_{l,m} Y_lm(-iota,-psi) h_lm,
 1460 * or equivalently rotate h_lm -> h'_lm=DWigner(psi,iota,alpha) h_lm
 1461 * and then obtain
 1462 * (h+ + I hx) = Sum_{l,m} Y_lm(0,0) h'_lm,
 1463 */
 1464SphHarmTimeSeries *XLALSimInspiralChooseTDModes(
 1465    UNUSED REAL8 phiRef,                        /**< reference orbital phase (rad). This variable is not used and only kept here for backwards compatibility */
 1466    REAL8 deltaT,                               /**< sampling interval (s) */
 1467    REAL8 m1,                                   /**< mass of companion 1 (kg) */
 1468    REAL8 m2,                                   /**< mass of companion 2 (kg) */
 1469    REAL8 S1x,                                  /**< x-component of the dimensionless spin of object 1 */
 1470    REAL8 S1y,                                  /**< y-component of the dimensionless spin of object 1 */
 1471    REAL8 S1z,                                  /**< z-component of the dimensionless spin of object 1 */
 1472    REAL8 S2x,                                  /**< x-component of the dimensionless spin of object 2 */
 1473    REAL8 S2y,                                  /**< y-component of the dimensionless spin of object 2 */
 1474    REAL8 S2z,                                  /**< z-component of the dimensionless spin of object 2 */
 1475    REAL8 f_min,                                /**< starting GW frequency (Hz) */
 1476    REAL8 f_ref,                                /**< reference GW frequency (Hz) */
 1477    REAL8 distance,                             /**< distance of source (m) */
 1478    LALDict *params,                            /**< LAL dictionary containing accessory parameters */
 1479    int lmax,                                   /**< generate all modes with l <= lmax */
 1480    Approximant approximant                     /**< post-Newtonian approximant to use for waveform production */
 1481    )
 1482{
 1483        LALSimInspiralGenerator *generator;
 1484    SphHarmTimeSeries *hlms = NULL;
 1485 
 1486    generator = XLALSimInspiralChooseGenerator(approximant, params);
 1487        if (!(generator))
 1488        XLAL_ERROR_NULL(XLAL_EFUNC);
 1489 
 1490    if (params == NULL) {
 1491        params = XLALCreateDict();
 1492    }
 1493    else {
 1494        params = XLALDictDuplicate(params);
 1495    }
 1496        if (!(params))
 1497        XLAL_ERROR_NULL(XLAL_EFUNC);
 1498 
 1499    XLALSimInspiralWaveformParamsInsertRefPhase(params, phiRef);
 1500    XLALSimInspiralWaveformParamsInsertDeltaT(params, deltaT);
 1501    XLALSimInspiralWaveformParamsInsertMass1(params, m1);
 1502    XLALSimInspiralWaveformParamsInsertMass2(params, m2);
 1503    XLALSimInspiralWaveformParamsInsertSpin1x(params, S1x);
 1504    XLALSimInspiralWaveformParamsInsertSpin1y(params, S1y);
 1505    XLALSimInspiralWaveformParamsInsertSpin1z(params, S1z);
 1506    XLALSimInspiralWaveformParamsInsertSpin2x(params, S2x);
 1507    XLALSimInspiralWaveformParamsInsertSpin2y(params, S2y);
 1508    XLALSimInspiralWaveformParamsInsertSpin2z(params, S2z);
 1509    XLALSimInspiralWaveformParamsInsertF22Start(params, f_min);
 1510    XLALSimInspiralWaveformParamsInsertF22Ref(params, f_ref);
 1511    XLALSimInspiralWaveformParamsInsertDistance(params, distance);
 1512    XLALSimInspiralWaveformParamsInsertLmax(params, lmax);
 1513 
 1514    XLALSimInspiralGenerateTDModes(&hlms, params, generator);
 1515    XLALDestroyDict(params);
 1516    XLALDestroySimInspiralGenerator(generator);
 1517 
 1518    return hlms;
 1519}
 1520 
 1521/**
 1522 * @brief Interface to compute a set of -2 spin-weighted spherical harmonic modes
 1523 * for a binary merger for a given waveform approximant in the Fourier domain.
 1524 * Non-precessing models IMRPhenomXHM, SEOBNRv4HM_ROM, SEOBNRv5(HM)_ROM and IMRPhenomHM and the
 1525 * precessing IMRPhenomXPHM are implemented.
 1526 * By default, all the modes available in the model are returned, although the list
 1527 * can be specified through the ModeArray option in the LAL dictionary.
 1528 * @details
 1529 * In the Fourier domain the modes span over the whole frequency regime (positive and negative frequencies).
 1530 * However, in the aligned spin case, the modes have support only in one half of the frequency regime.
 1531 * The LAL conventions establish that the negative modes (m<0) have support for positive frequencies while
 1532 * the positive modes (m>0) have support for negative frequencies (this is based in the right hand rule and
 1533 * Fourier transform definition in LAL).
 1534 * Due to the equatorial symmetry of non-precessng systems, there exist a relation between them: h_{lm}(f) = (-1)^l h*_{l-m}(-f).
 1535 * In the precessing case this symmetry is broken and all the modes have support for both positive and negative frequencies.
 1536 *
 1537 * For this reason, the ouput SphHarmFrequencySeries object will return the modes in the whole frequency range.
 1538 * The frequencies of this object will be sorted as: -f_max,...,-f_min,...0,...,f_min,...,f_max.
 1539 * The values of the waveform will be sorted correspondingly. Consequently, in the aligned spin case, half of the frequency spectrum consists of zeros.
 1540 *
 1541 * It is relevant to mention why the arguments inclination and phiRef are needed for computing the h_lm.
 1542 * For AS models the argument inclination is irrelevant and will not be use since it only enters in the Ylm. However, for the precessing model,
 1543 * since the modes are returned in the J-frame, we need the inclination argument to carry out the Euler transformation from the co-precessing L-frame
 1544 * to the inertial J-frame. Regarding the argument phiRef, this affects the output of the precessing model due to the same reason as before, while for the AS models
 1545 * it would not affect the output of SEOBNRv4HM_ROM, SEOBNRv5(HM)_ROM but will change the output of IMRPhenomHM and IMRPhenomXHM (this is due to the internals workings of the models).
 1546 * If one wants to built the polarizations from the individual modes of ChooseFDModes must be aware of this behaviour.
 1547 * Ideally, one would call ChooseFDModes with phiRef=0 to obtain the h_lms, then build the Fourier domain polarizations as
 1548 *
 1549 * h_+ (f) = 1/2 sum_{l=2} sum_{m=-l}^{m=l}  (  h_lm(f) * Y_lm(theta, vphi)  +  h*_lm(-f) * Y*_lm(theta, vphi)  )
 1550 * h_x (f) = i/2 sum_{l=2} sum_{m=-l}^{m=l}  (  h_lm(f) * Y_lm(theta, vphi)  -  h*_lm(-f) * Y*_lm(theta, vphi)  )
 1551 *
 1552 * where theta is the inclination and vphi is pi/2 - phiRef.
 1553 *
 1554 * If one does this, one will find generally a very close result to ChooseFDWaveform with very small mismatches (~10^-9 for IMRPhenomXHM),
 1555 * and this is what is found if one uses the XLALSimInspiralPolarizationsFromSphHarmFrequencySeries function, however this is not close to machine precision.
 1556 * The reason is that IMRPhenomHM and IMRPhenomXHM use internally the phiRef argument to compute the h_lms because at that time phiRef was considered to be also a reference
 1557 * phase for the h_lms and not just the argument for the azimuthal angle in the Y_lms.
 1558 * To take this into account we provide also the function XLALSimInspiralPolarizationsFromChooseFDModes which build the polarizations in the proper way for each
 1559 * model returning a result close to machine precision with ChooseFDWaveform.
 1560 *
 1561 * For the precessing model IMRPhenomXPHM, since the h_lms are returned in the J-frame one must build the polarizations using theta = theta_JN and vphi = 0.
 1562 * The parameter theta_JN is computed internally when using XLALSimInspiralPolarizationsFromChooseFDModes and again here the result is close to machine precision to ChooseFDWaveform.
 1563 * However, one would have to compute theta_JN personally when using XLALSimInspiralPolarizationsFromSphHarmFrequencySeries.
 1564 * For IMRPhenomXPHM this parameter can be computed using XLALSimIMRPhenomXPCalculateModelParametersFromSourceFrame. Eventhough one would still have to correct with the polarization angle.
 1565 *
 1566 * By default all the modes available in the model will be returned, both positive and negative modes.
 1567 * The mode content of AS models can be adjusted through the ModeArray option in the LAL dictionary argument, and it accepts any set of modes e.g. (2,2),(2,-1),(3,3),...
 1568 * For IMRPhenomXPHM, we can specify both the modes in the co-precessing L-frame, which are used to do the twisting-up, and
 1569 * the ouput modes in the inertial J-frame. The set of modes in the L-frame are specified with the standard ModeArray option
 1570 * while the set of modes in the J-frame are specified in a new option called ModeArrayJframe. Notice that in IMRPhenomXPHM, ModeArray does not distinguish
 1571 * between positive or negative modes and it always twists-up both positive and negative modes, i.e. the sets {(2,2)}, {(2,-2)} or {(2,2),(2,-2)} would return the same result.
 1572 * For the modes in ModeArrayJframe, we can specify both positive or negative modes for example {(2,2),(2,-2),(2,-1),(3,3),...}.
 1573 */
 1574SphHarmFrequencySeries *XLALSimInspiralChooseFDModes(
 1575    REAL8 m1,                                   /**< mass of companion 1 (kg) */
 1576    REAL8 m2,                                   /**< mass of companion 2 (kg) */
 1577    REAL8 S1x,                                  /**< x-component of the dimensionless spin of object 1 */
 1578    REAL8 S1y,                                  /**< y-component of the dimensionless spin of object 1 */
 1579    REAL8 S1z,                                  /**< z-component of the dimensionless spin of object 1 */
 1580    REAL8 S2x,                                  /**< x-component of the dimensionless spin of object 2 */
 1581    REAL8 S2y,                                  /**< y-component of the dimensionless spin of object 2 */
 1582    REAL8 S2z,                                  /**< z-component of the dimensionless spin of object 2 */
 1583    REAL8 deltaF,                               /**< sampling interval (s) */
 1584    REAL8 f_min,                                /**< starting GW frequency (Hz) */
 1585    REAL8 f_max,                                /**< ending GW frequency (Hz) */
 1586    REAL8 f_ref,                                /**< reference GW frequency (Hz) */
 1587    REAL8 phiRef,                                                               /**< reference phase (rad) */
 1588    REAL8 distance,                             /**< distance of source (m) */
 1589    REAL8 inclination,                          /**< inclination of source (rad) */
 1590        LALDict *params,                            /**< LAL dictionary containing accessory parameters (optional mode array) */
 1591    Approximant approximant                     /**< approximant to use for waveform production */
 1592    )
 1593{
 1594 
 1595        LALSimInspiralGenerator *generator;
 1596    SphHarmFrequencySeries *hlms = NULL;
 1597 
 1598    generator = XLALSimInspiralChooseGenerator(approximant, params);
 1599        if (!(generator))
 1600        XLAL_ERROR_NULL(XLAL_EFUNC);
 1601 
 1602    if (params == NULL) {
 1603        params = XLALCreateDict();
 1604    }
 1605    else {
 1606        params = XLALDictDuplicate(params);
 1607    }
 1608        if (!(params))
 1609        XLAL_ERROR_NULL(XLAL_EFUNC);
 1610 
 1611    XLALSimInspiralWaveformParamsInsertMass1(params, m1);
 1612    XLALSimInspiralWaveformParamsInsertMass2(params, m2);
 1613    XLALSimInspiralWaveformParamsInsertSpin1x(params, S1x);
 1614    XLALSimInspiralWaveformParamsInsertSpin1y(params, S1y);
 1615    XLALSimInspiralWaveformParamsInsertSpin1z(params, S1z);
 1616    XLALSimInspiralWaveformParamsInsertSpin2x(params, S2x);
 1617    XLALSimInspiralWaveformParamsInsertSpin2y(params, S2y);
 1618    XLALSimInspiralWaveformParamsInsertSpin2z(params, S2z);
 1619    XLALSimInspiralWaveformParamsInsertDeltaF(params, deltaF);
 1620    XLALSimInspiralWaveformParamsInsertF22Start(params, f_min);
 1621    XLALSimInspiralWaveformParamsInsertFMax(params, f_max);
 1622    XLALSimInspiralWaveformParamsInsertF22Ref(params, f_ref);
 1623    XLALSimInspiralWaveformParamsInsertRefPhase(params, phiRef);
 1624    XLALSimInspiralWaveformParamsInsertDistance(params, distance);
 1625    XLALSimInspiralWaveformParamsInsertInclination(params, inclination);
 1626 
 1627 
 1628    XLALSimInspiralGenerateFDModes(&hlms, params, generator);
 1629    XLALDestroyDict(params);
 1630    XLALDestroySimInspiralGenerator(generator);
 1631 
 1632        return hlms;
 1633}
 1634 
 1635/**
 1636 * @brief Interface to compute a conditioned set of -2 spin-weighted spherical
 1637 * harmonic modes for a binary inspiral
 1638 * @details
 1639 * This routine is a wrapper for XLALSimInspiralChooseTDModes which applies
 1640 * waveform conditioning to the modes generated by that routine.  The conditioning
 1641 * algorithm is analogous to that performed in XLALSimInspiralTD.  Note that
 1642 * the modes are high-pass filtered at frequency f_min, which is specified for
 1643 * the m=2 mode, which means that the low-frequency part of the m=1 mode is
 1644 * removed by the filtering.  The phasing is computed with any of the TaylorT1,
 1645 * T2, T3, T4 methods.  It can also return the (2,2), (2,1), (3,3), (4,4),
 1646 * (5,5) modes of the EOBNRv2 model. Note that EOBNRv2 will ignore ampO,
 1647 * phaseO, lmax and f_ref arguments.
 1648 * @param deltaT      Sampling interval (s)
 1649 * @param m1          Mass of companion 1 (kg)
 1650 * @param m2          Mass of companion 2 (kg)
 1651 * @param f_min       Starting GW frequency (Hz)
 1652 * @param f_ref       Reference GW frequency (Hz)
 1653 * @param r           Distance of source (m)
 1654 * @param LALpars     LAL dictionary containing accesory parameters
 1655 * @param lmax        Generate all modes with l <= lmax
 1656 * @param approximant Post-Newtonian approximant to use for waveform production
 1657 * @return Linked list of SphHarmTimeSeries modes.
 1658 */
 1659SphHarmTimeSeries *XLALSimInspiralModesTD(REAL8 deltaT, REAL8 m1, REAL8 m2, REAL8 f_min, REAL8 f_ref, REAL8 r, LALDict *LALpars, int lmax, Approximant approximant)
 1660{
 1661    const size_t min_taper_samples = 4;
 1662    const double extra_time_fraction = 0.1; /* fraction of waveform duration to add as extra time for tapering */
 1663    const double extra_cycles = 3.0; /* more extra time measured in cycles at the starting frequency */
 1664    double original_f_min = f_min; /* f_min might be overwritten below, so keep original value */
 1665    //double tchirp, tmerge, textra;
 1666    //double fisco, fstart;
 1667    double tchirp, textra;
 1668    double fisco;
 1669    //double s;
 1670    size_t length, nzeros, ntaper;
 1671    size_t j;
 1672    SphHarmTimeSeries *modes, *hlm;
 1673 
 1674    /* if the requested low frequency is below the lowest Kerr ISCO frequency
 1675     * then change it to that frequency */
 1676    fisco = 1.0 / (pow(9.0, 1.5) * LAL_PI * (m1 + m2) * LAL_MTSUN_SI / LAL_MSUN_SI);
 1677    if (f_min > fisco)
 1678        f_min = fisco;
 1679 
 1680    /* upper bound on the chirp time starting at f_min */
 1681    tchirp = XLALSimInspiralChirpTimeBound(f_min, m1, m2, 0.0, 0.0);
 1682 
 1683    /* upper bound on the final black hole spin */
 1684    //s = XLALSimInspiralFinalBlackHoleSpinBound(0.0, 0.0);
 1685 
 1686    /* upper bound on the final plunge, merger, and ringdown time */
 1687    //tmerge = XLALSimInspiralMergeTimeBound(m1, m2) + XLALSimInspiralRingdownTimeBound(m1 + m2, s);
 1688 
 1689    /* extra time to include for all waveforms to take care of situations
 1690     * where the frequency is close to merger (and is sweeping rapidly):
 1691     * this is a few cycles at the low frequency */
 1692    textra = extra_cycles / f_min;
 1693 
 1694    /* condition by generating a waveform with a lower starting frequency and
 1695     * apply tapers in the region between that lower frequency and the
 1696     * requested frequency f_min; here compute a new lower frequency */
 1697    // fstart = XLALSimInspiralChirpStartFrequencyBound((1.0 + extra_time_fraction) * tchirp + tmerge + textra, m1, m2);
 1698 
 1699    XLALPrintWarning("XLAL Warning - XLALSimInspiralModesTD does not yet implement spins - passing zeros\n");
 1700    modes = XLALSimInspiralChooseTDModes(0.,deltaT, m1, m2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, f_min, f_ref, r, LALpars, lmax, approximant);
 1701    if (!modes)
 1702        XLAL_ERROR_NULL(XLAL_EFUNC);
 1703 
 1704    /* Note: fstart and f_min are frequencies for a m=2 mode, while the
 1705     * frequencies of the mth mode are f_m = m * f / 2; this means that if we
 1706     * generate a waveform that starts at fstart in the m=2 mode then the m=1
 1707     * mode starts at fstart/2 while the m=3 mode starts at 3*fstart/2, and so
 1708     * on.  However, the time it takes the m=2 mode to go from fstart to f_min
 1709     * is the same as the time that a m=1 mode to go from fstart/2 to f_min/2,
 1710     * etc., so we apply tapers over this time.  The upshot is that the
 1711     * resulting modes will be valid for frequencies above m * f_min / 2.
 1712     * evolve from fstart to f_min is the same as the time to evolve from
 1713     * 2*f_start/m to 2*f_min/m for the mth mode, so taper all modes over
 1714     * taper this duration. */
 1715    length = nzeros = modes->mode->data->length;
 1716    for (hlm = modes; hlm; hlm = hlm->next) {
 1717        /* some waveform generators zero-pad the end of the waveform, and we
 1718         * want to remove this; however, we want all modes to have the same
 1719         * length timeseries, so find the minimum number of zeros to excise */
 1720        if (nzeros) {
 1721            j = 0;
 1722            while (hlm->mode->data->data[hlm->mode->data->length - j - 1] == 0.0)
 1723                ++j;
 1724            if (j < nzeros)
 1725                nzeros = j;
 1726        }
 1727 
 1728        /* here is where we taper the beginning of the waveform below f_min */
 1729        ntaper = round((extra_time_fraction * tchirp + textra) / deltaT);
 1730        for (j = 0; j < ntaper; ++j)
 1731             hlm->mode->data->data[j] *= 0.5 - 0.5 * cos(j * LAL_PI / ntaper);
 1732 
 1733        /* now high-pass filter the data at the original f_min value so that
 1734         * the modes have negligible frequency content below that frequency;
 1735         * note: this will cut off the low-frequency content of the m=1 mode */
 1736        XLALHighPassCOMPLEX16TimeSeries(hlm->mode, original_f_min, 0.99, 8);
 1737    }
 1738 
 1739    /* new length after clipping zeros from end */
 1740    length -= nzeros;
 1741    if (nzeros)
 1742        XLALResizeSphHarmTimeSeries(modes, 0, length);
 1743 
 1744    /* stage 2 conditioning: final tapering at beginning and end */
 1745    /* final tapering at the beginning and at the end */
 1746    /* if this waveform is shorter than 2*min_taper_samples, do nothing */
 1747    if (length < 2 * min_taper_samples) {
 1748        XLAL_PRINT_WARNING("waveform is too shorter than %zu samples: no final tapering applied", 2 * min_taper_samples);
 1749        return modes;
 1750    }
 1751 
 1752    /* waveform should terminate at a frequency >= Schwarzschild ISCO
 1753     * so taper one cycle at this frequency at the end; should not make
 1754     * any difference to IMR waveforms */
 1755    fisco = 1.0 / (pow(6.0, 1.5) * LAL_PI * (m1 + m2) * LAL_MTSUN_SI / LAL_MSUN_SI);
 1756    ntaper = round(1.0 / (fisco * deltaT));
 1757    if (ntaper < min_taper_samples)
 1758        ntaper = min_taper_samples;
 1759    for (hlm = modes; hlm; hlm = hlm->next)
 1760        for (j = 1; j < ntaper; ++j)
 1761             hlm->mode->data->data[length - j] *= 0.5 - 0.5 * cos(j * LAL_PI / ntaper);
 1762 
 1763    /* there could be a filter transient at the beginning too: we should have
 1764     * some safety there owing to the fact that we are starting at a lower
 1765     * frequency than is needed, so taper off one cycle at the low frequency */
 1766    ntaper = round(1.0 / (f_min * deltaT));
 1767    if (ntaper < min_taper_samples)
 1768        ntaper = min_taper_samples;
 1769    for (hlm = modes; hlm; hlm = hlm->next)
 1770        for (j = 1; j < ntaper; ++j)
 1771             hlm->mode->data->data[j] *= 0.5 - 0.5 * cos(j * LAL_PI / ntaper);
 1772 
 1773    return modes;
 1774}
 1775 
 1776/**
 1777 * Interface to compute a single -2 spin-weighted spherical harmonic mode
 1778 * for a binary inspiral of any available amplitude and phase PN order.
 1779 * The phasing is computed with any of the TaylorT1, T2, T3, T4 methods.
 1780 */
 1781COMPLEX16TimeSeries *XLALSimInspiralChooseTDMode(
 1782    REAL8 deltaT,                               /**< sampling interval (s) */
 1783    REAL8 m1,                                   /**< mass of companion 1 (kg) */
 1784    REAL8 m2,                                   /**< mass of companion 2 (kg) */
 1785    REAL8 f_min,                                /**< starting GW frequency (Hz) */
 1786    REAL8 f_ref,                                /**< reference GW frequency (Hz) */
 1787    REAL8 r,                                    /**< distance of source (m) */
 1788    REAL8 lambda1,                              /**< (tidal deformability of mass 1) / m1^5 (dimensionless) */
 1789    REAL8 lambda2,                              /**< (tidal deformability of mass 2) / m2^5 (dimensionless) */
 1790    LALSimInspiralWaveformFlags *waveFlags,     /**< Set of flags to control special behavior of some waveform families. Pass in NULL (or None in python) for default flags */
 1791    LALSimInspiralTestGRParam *nonGRparams,     /**< Linked list of non-GR parameters. Pass in NULL (or None in python) for standard GR waveforms */
 1792    int amplitudeO,                             /**< twice post-Newtonian amplitude order */
 1793    int phaseO,                                 /**< twice post-Newtonian order */
 1794    int l,                                      /**< l index of mode */
 1795    int m,                                      /**< m index of mode */
 1796    Approximant approximant                     /**< post-Newtonian approximant to use for waveform production */
 1797    )
 1798{
 1799    REAL8 v0 = 1.;
 1800    COMPLEX16TimeSeries *hlm;
 1801    SphHarmTimeSeries *ts;
 1802 
 1803    /* General sanity checks that will abort */
 1804    /*
 1805     * If non-GR approximants are added, change the below to
 1806     * if( nonGRparams && approximant != nonGR1 && approximant != nonGR2 )
 1807     */
 1808    if( nonGRparams )
 1809    {
 1810        XLALPrintError("XLAL Error - %s: Passed in non-NULL pointer to LALSimInspiralTestGRParam for an approximant that does not use LALSimInspiralTestGRParam\n", __func__);
 1811        XLAL_ERROR_NULL(XLAL_EINVAL);
 1812    }
 1813 
 1814    /* General sanity check the input parameters - only give warnings! */
 1815    if( deltaT > 1. )
 1816        XLALPrintWarning("XLAL Warning - %s: Large value of deltaT = %e requested.\nPerhaps sample rate and time step size were swapped?\n", __func__, deltaT);
 1817    if( deltaT < 1./16385. )
 1818        XLALPrintWarning("XLAL Warning - %s: Small value of deltaT = %e requested.\nCheck for errors, this could create very large time series.\n", __func__, deltaT);
 1819    if( m1 < 0.09 * LAL_MSUN_SI )
 1820        XLALPrintWarning("XLAL Warning - %s: Small value of m1 = %e (kg) = %e (Msun) requested.\nPerhaps you have a unit conversion error?\n", __func__, m1, m1/LAL_MSUN_SI);
 1821    if( m2 < 0.09 * LAL_MSUN_SI )
 1822        XLALPrintWarning("XLAL Warning - %s: Small value of m2 = %e (kg) = %e (Msun) requested.\nPerhaps you have a unit conversion error?\n", __func__, m2, m2/LAL_MSUN_SI);
 1823    if( m1 + m2 > 1000. * LAL_MSUN_SI )
 1824        XLALPrintWarning("XLAL Warning - %s: Large value of total mass m1+m2 = %e (kg) = %e (Msun) requested.\nSignal not likely to be in band of ground-based detectors.\n", __func__, m1+m2, (m1+m2)/LAL_MSUN_SI);
 1825    if( f_min < 1. )
 1826        XLALPrintWarning("XLAL Warning - %s: Small value of fmin = %e requested.\nCheck for errors, this could create a very long waveform.\n", __func__, f_min);
 1827    if( f_min > 40.000001 )
 1828        XLALPrintWarning("XLAL Warning - %s: Large value of fmin = %e requested.\nCheck for errors, the signal will start in band.\n", __func__, f_min);
 1829 
 1830    switch (approximant)
 1831    {
 1832        case TaylorT1:
 1833            /* Waveform-specific sanity checks */
 1834            if( !XLALSimInspiralFrameAxisIsDefault(
 1835                    XLALSimInspiralGetFrameAxis(waveFlags)) )
 1836                XLAL_ERROR_NULL(XLAL_EINVAL, "Non-default LALSimInspiralFrameAxis provided, but this approximant does not use that flag.");
 1837            if( !XLALSimInspiralModesChoiceIsDefault(
 1838                    XLALSimInspiralGetModesChoice(waveFlags)) )
 1839                XLAL_ERROR_NULL(XLAL_EINVAL, "Non-default LALSimInspiralModesChoice provided, but this approximant does not use that flag.");
 1840            /* Call the waveform driver routine */
 1841            hlm = XLALSimInspiralTaylorT1PNMode(v0,
 1842                    deltaT, m1, m2, f_min, f_ref, r, lambda1, lambda2,
 1843                    XLALSimInspiralGetTidalOrder(waveFlags), amplitudeO,
 1844                    phaseO, l, m);
 1845            break;
 1846        case TaylorT2:
 1847            /* Waveform-specific sanity checks */
 1848            if( !XLALSimInspiralFrameAxisIsDefault(
 1849                    XLALSimInspiralGetFrameAxis(waveFlags)) )
 1850                XLAL_ERROR_NULL(XLAL_EINVAL, "Non-default LALSimInspiralFrameAxis provided, but this approximant does not use that flag.");
 1851            if( !XLALSimInspiralModesChoiceIsDefault(
 1852                    XLALSimInspiralGetModesChoice(waveFlags)) )
 1853                XLAL_ERROR_NULL(XLAL_EINVAL, "Non-default LALSimInspiralModesChoice provided, but this approximant does not use that flag.");
 1854            /* Call the waveform driver routine */
 1855            hlm = XLALSimInspiralTaylorT2PNMode(v0,
 1856                    deltaT, m1, m2, f_min, f_ref, r, lambda1, lambda2,
 1857                    XLALSimInspiralGetTidalOrder(waveFlags), amplitudeO,
 1858                    phaseO, l, m);
 1859            break;
 1860        case TaylorT3:
 1861            /* Waveform-specific sanity checks */
 1862            if( !XLALSimInspiralFrameAxisIsDefault( XLALSimInspiralGetFrameAxis(waveFlags)) )
 1863                XLAL_ERROR_NULL(XLAL_EINVAL, "Non-default LALSimInspiralFrameAxis provided, but this approximant does not use that flag.");
 1864            if( !XLALSimInspiralModesChoiceIsDefault( XLALSimInspiralGetModesChoice(waveFlags)) )
 1865                XLAL_ERROR_NULL(XLAL_EINVAL, "Non-default LALSimInspiralModesChoice provided, but this approximant does not use that flag.");
 1866            /* Call the waveform driver routine */
 1867            hlm = XLALSimInspiralTaylorT3PNMode(v0,
 1868                    deltaT, m1, m2, f_min, f_ref, r, lambda1, lambda2,
 1869                    XLALSimInspiralGetTidalOrder(waveFlags), amplitudeO,
 1870                    phaseO, l, m);
 1871            break;
 1872        case TaylorT4:
 1873            /* Waveform-specific sanity checks */
 1874            if( !XLALSimInspiralFrameAxisIsDefault(
 1875                    XLALSimInspiralGetFrameAxis(waveFlags) ) )
 1876                XLAL_ERROR_NULL(XLAL_EINVAL, "Non-default LALSimInspiralFrameAxis provided, but this approximant does not use that flag.");
 1877            if( !XLALSimInspiralModesChoiceIsDefault(
 1878                    XLALSimInspiralGetModesChoice(waveFlags) ) )
 1879                XLAL_ERROR_NULL(XLAL_EINVAL, "Non-default LALSimInspiralModesChoice provided, but this approximant does not use that flag.");
 1880            /* Call the waveform driver routine */
 1881            hlm = XLALSimInspiralTaylorT4PNMode(v0,
 1882                    deltaT, m1, m2, f_min, f_ref, r, lambda1, lambda2,
 1883                    XLALSimInspiralGetTidalOrder(waveFlags), amplitudeO,
 1884                    phaseO, l, m);
 1885            break;
 1886        case EOBNRv2:
 1887        case EOBNRv2HM:
 1888            ts = XLALSimIMREOBNRv2Modes(deltaT, m1, m2, f_min, r);
 1889            hlm = XLALSphHarmTimeSeriesGetMode(ts, l, m);
 1890            break;
 1891 
 1892        default:
 1893            XLALPrintError("Cannot generate modes for this approximant\n");
 1894            XLAL_ERROR_NULL(XLAL_EINVAL);
 1895    }
 1896    if ( !hlm )
 1897        XLAL_ERROR_NULL(XLAL_EFUNC);
 1898 
 1899    return hlm;
 1900}
 1901 
 1902/** @} */
 1903 
 1904/**
 1905 * @name Routines for Generating Inspiral Waveforms from Orbital Data
 1906 * @{
 1907 */
 1908 
 1909/**
 1910 * Given time series for a binary's orbital dynamical variables,
 1911 * construct the waveform polarizations h+ and hx directly.
 1912 * NB: Valid only for non-precessing binaries!
 1913 *
 1914 * Implements Equations (8.8) - (8.10) of:
 1915 * Luc Blanchet, Guillaume Faye, Bala R. Iyer and Siddhartha Sinha,
 1916 * \"The third post-Newtonian gravitational wave polarisations
 1917 * and associated spherical harmonic modes for inspiralling compact binaries
 1918 * in quasi-circular orbits\", Class. Quant. Grav. 25 165003 (2008);
 1919 * arXiv:0802.1249.
 1920 * NB: Be sure to check arXiv:0802.1249v3, which corrects a typo!
 1921 *
 1922 * Note however, that we do not include the constant \"memory\" terms
 1923 */
 1924int XLALSimInspiralPNPolarizationWaveforms(
 1925    REAL8TimeSeries **hplus,  /**< +-polarization waveform [returned] */
 1926    REAL8TimeSeries **hcross, /**< x-polarization waveform [returned] */
 1927    REAL8TimeSeries *V,       /**< post-Newtonian (PN) parameter */
 1928    REAL8TimeSeries *Phi,     /**< orbital phase */
 1929    REAL8 v0,                 /**< tail-term gauge choice (default = 1) */
 1930    REAL8 m1,                 /**< mass of companion 1 (kg) */
 1931    REAL8 m2,                 /**< mass of companion 2 (kg) */
 1932    REAL8 r,                  /**< distance of source (m) */
 1933    REAL8 i,                  /**< inclination of source (rad) */
 1934    int ampO                  /**< twice PN order of the amplitude */
 1935    )
 1936{
 1937    REAL8 M, eta, eta2, eta3, dm, dist, ampfac, phi, phiShift, v, v2, v3;
 1938    REAL8 hp0, hp05, hp1, hp15, hp2, hp25, hp3;
 1939    REAL8 hc0, hc05, hc1, hc15, hc2, hc25, hc3;
 1940    REAL8 ci, si, ci2, ci4, ci6, ci8, si2, si3, si4, si5, si6;
 1941    INT4 idx, len;
 1942 
 1943    /* Sanity check input time series */
 1944    LAL_CHECK_VALID_SERIES(V, XLAL_FAILURE);
 1945    LAL_CHECK_VALID_SERIES(Phi, XLAL_FAILURE);
 1946    LAL_CHECK_CONSISTENT_TIME_SERIES(V, Phi, XLAL_FAILURE);
 1947 
 1948    /* Allocate polarization vectors and set to 0 */
 1949    *hplus = XLALCreateREAL8TimeSeries( "H_PLUS", &V->epoch, 0.0,
 1950            V->deltaT, &lalStrainUnit, V->data->length );
 1951    *hcross = XLALCreateREAL8TimeSeries( "H_CROSS", &V->epoch, 0.0,
 1952            V->deltaT, &lalStrainUnit, V->data->length );
 1953    if ( ! hplus || ! hcross )
 1954        XLAL_ERROR(XLAL_EFUNC);
 1955    memset((*hplus)->data->data, 0, (*hplus)->data->length
 1956            * sizeof(*(*hplus)->data->data));
 1957    memset((*hcross)->data->data, 0, (*hcross)->data->length
 1958            * sizeof(*(*hcross)->data->data));
 1959 
 1960    M = m1 + m2;
 1961    eta = m1 * m2 / M / M; // symmetric mass ratio - '\nu' in the paper
 1962    eta2 = eta*eta;     eta3 = eta2*eta;
 1963    dm = (m1 - m2) / M; // frac. mass difference - \delta m/m in the paper
 1964    dist = r / LAL_C_SI;   // r (m) / c (m/s) --> dist in units of seconds
 1965    /* convert mass from kg to s, so ampfac ~ M/dist is dimensionless */
 1966    ampfac = 2. * M * LAL_G_SI * pow(LAL_C_SI, -3) * eta / dist;
 1967 
 1968    /*
 1969     * cosines and sines of inclination between
 1970     * line of sight (N) and binary orbital angular momentum (L_N)
 1971     */
 1972    ci = cos(i);        si = sin(i);
 1973    ci2 = ci*ci;  ci4 = ci2*ci2;  ci6 = ci2*ci4;  ci8 = ci6*ci2;
 1974    si2 = si*si;  si3 = si2*si;  si4 = si2*si2;  si5 = si*si4; si6 = si4*si2;
 1975 
 1976    /* loop over time steps and compute polarizations h+ and hx */
 1977 
 1978    len = V->data->length;
 1979    for(idx = 0; idx < len; idx++)
 1980    {
 1981        /* Abbreviated names in lower case for time series at this sample */
 1982        phi = Phi->data->data[idx];     v = V->data->data[idx];
 1983        v2 = v * v;     v3 = v * v2;
 1984 
 1985        /*
 1986         * As explained in Blanchet et al, a phase shift can be applied
 1987         * to make log terms vanish which would appear in the amplitude
 1988         * at 1.5PN and 2.5PN orders. This shift is given in Eq. (8.8)
 1989         * We apply the shift only for the PN orders which need it.
 1990         */
 1991        if( (ampO == -1) || ampO >= 5 )
 1992            phiShift = 3.*v3*(1. - v2*eta/2.)*log( v2 / v0 / v0  );
 1993        else if( ampO >= 3 )
 1994            phiShift = 3.*v3*log( v2 / v0 / v0 );
 1995        else
 1996            phiShift = 0.;
 1997 
 1998        phi = phi - phiShift;
 1999 
 2000        /*
 2001         * First set all h+/x coefficients to 0. Then use a switch to
 2002         * set proper non-zero values up to order ampO. Note we
 2003         * fall through the PN orders and break only after Newt. order
 2004         */
 2005        hp0 = hp05 = hp1 = hp15 = hp2 = hp25 = hp3 = 0.;
 2006        hc0 = hc05 = hc1 = hc15 = hc2 = hc25 = hc3 = 0.;
 2007 
 2008        switch( ampO )
 2009        {
 2010            /* case LAL_PNORDER_THREE_POINT_FIVE: */
 2011            case 7:
 2012                XLALPrintError("XLAL Error - %s: Amp. corrections not known "
 2013                        "to PN order %d\n", __func__, ampO );
 2014                XLAL_ERROR(XLAL_EINVAL);
 2015                break;
 2016            case -1: // Highest known PN order - move if higher terms added!
 2017            /* case LAL_PNORDER_THREE: */
 2018            case 6:
 2019        /* The reference had a typo in the 3PN terms and needed an errata.
 2020         * These should match arXiv:0802.1249v3, which has the fix. */
 2021                hp3 = LAL_PI*dm*si*cos(phi)*(19./64. + ci2*5./16. - ci4/192.
 2022                        + eta*(-19./96. + ci2*3./16. + ci4/96.)) + cos(2.*phi)
 2023                        * (-465497./11025. + (LAL_GAMMA*856./105.
 2024                        - 2.*LAL_PI*LAL_PI/3. + log(16.*v2)*428./105.)
 2025                        * (1. + ci2) - ci2*3561541./88200. - ci4*943./720.
 2026                        + ci6*169./720. - ci8/360. + eta*(2209./360.
 2027                        - LAL_PI*LAL_PI*41./96.*(1. + ci2) + ci2*2039./180.
 2028                        + ci4*3311./720. - ci6*853./720. + ci8*7./360.)
 2029                        + eta2*(12871./540. - ci2*1583./60. - ci4*145./108.
 2030                        + ci6*56./45. - ci8*7./180.) + eta3*(-3277./810.
 2031                        + ci2*19661./3240. - ci4*281./144. - ci6*73./720.
 2032                        + ci8*7./360.)) + LAL_PI*dm*si*cos(3.*phi)*(-1971./128.
 2033                        - ci2*135./16. + ci4*243./128. + eta*(567./64.
 2034                        - ci2*81./16. - ci4*243./64.)) + si2*cos(4.*phi)
 2035                        * (-2189./210. + ci2*1123./210. + ci4*56./9.
 2036                        - ci6*16./45. + eta*(6271./90. - ci2*1969./90.
 2037                        - ci4*1432./45. + ci6*112./45.) + eta2*(-3007./27.
 2038                        + ci2*3493./135. + ci4*1568./45. - ci6*224./45.)
 2039                        + eta3*(161./6. - ci2*1921./90. - ci4*184./45.
 2040                        + ci6*112./45.)) + dm*cos(5.*phi)*(LAL_PI*3125./384.
 2041                        * si3*(1. + ci2)*(1. - 2.*eta)) + si4*cos(6.*phi)
 2042                        * (1377./80. + ci2*891./80. - ci4*729./280.
 2043                        + eta*(-7857./80. - ci2*891./16. + ci4*729./40.)
 2044                        + eta2*(567./4. + ci2*567./10. - ci4*729./20.)
 2045                        + eta3*(-729./16. - ci2*243./80. + ci4*729./40.))
 2046                        + cos(8.*phi)*(-1024./315.*si6*(1. + ci2)*(1. - 7.*eta
 2047                        + 14.*eta2 - 7.*eta3)) + dm*si*sin(phi)*(-2159./40320.
 2048                        - log(2.)*19./32. + (-95./224. - log(2.)*5./8.)*ci2
 2049                        + (181./13440. + log(2.)/96.)*ci4 + eta*(1369./160.
 2050                        + log(2.)*19./48. + (-41./48. - log(2.)*3./8.)*ci2
 2051                        + (-313./480. - log(2.)/48.)*ci4)) + sin(2.*phi)
 2052                        * (-428.*LAL_PI/105.*(1. + ci2)) + dm*si*sin(3.*phi)
 2053                        * (205119./8960. - log(3./2.)*1971./64.
 2054                        + (1917./224. - log(3./2.)*135./8.)*ci2
 2055                        + (-43983./8960. + log(3./2.)*243./64.)*ci4 + eta
 2056                        * (-54869./960. + log(3./2.)*567./32.
 2057                        + (-923./80. - log(3./2.)*81./8.)*ci2
 2058                        + (41851./2880. - log(3./2.)*243./32.)*ci4))
 2059                        + dm*si3*(1. + ci2)*sin(5.*phi)*(-113125./5376.
 2060                        + log(5./2.)*3125./192.
 2061                        + eta*(17639./320. - log(5./2.)*3125./96.));
 2062                hc3 = dm*si*ci*cos(phi)*(11617./20160. + log(2.)*21./16.
 2063                        + (-251./2240. - log(2.)*5./48.)*ci2
 2064                        + eta*(-2419./240. - log(2.)*5./24.
 2065                        + (727./240. + log(2.)*5./24.)*ci2)) + ci*cos(2.*phi)
 2066                        * (LAL_PI*856./105.) + dm*si*ci*cos(3.*phi)
 2067                        * (-36801./896. + log(3./2.)*1809./32.
 2068                        + (65097./4480. - log(3./2.)*405./32.)*ci2
 2069                        + eta*(28445./288. - log(3./2.)*405./16.
 2070                        + (-7137./160. + log(3./2.)*405./16.)*ci2))
 2071                        + dm*si3*ci*cos(5.*phi)*(113125./2688.
 2072                        - log(5./2.)*3125./96. + eta*(-17639./160.
 2073                        + log(5./2.)*3125./48.)) + LAL_PI*dm*si*ci*sin(phi)
 2074                        * (21./32. - ci2*5./96. + eta*(-5./48. + ci2*5./48.))
 2075                        + ci*sin(2.*phi)*(-3620761./44100.
 2076                        + LAL_GAMMA*1712./105. - 4.*LAL_PI*LAL_PI/3.
 2077                        + log(16.*v2)*856./105. - ci2*3413./1260.
 2078                        + ci4*2909./2520. - ci6/45. + eta*(743./90.
 2079                        - 41.*LAL_PI*LAL_PI/48. + ci2*3391./180.
 2080                        - ci4*2287./360. + ci6*7./45.) + eta2*(7919./270.
 2081                        - ci2*5426./135. + ci4*382./45. - ci6*14./45.)
 2082                        + eta3*(-6457./1620. + ci2*1109./180. - ci4*281./120.
 2083                        + ci6*7./45.)) + LAL_PI*dm*si*ci*sin(3.*phi)
 2084                        * (-1809./64. + ci2*405./64. + eta*(405./32.
 2085                        - ci2*405./32.)) + si2*ci*sin(4.*phi)*(-1781./105.
 2086                        + ci2*1208./63. - ci4*64./45. + eta*(5207./45.
 2087                        - ci2*536./5. + ci4*448./45.) + eta2*(-24838./135.
 2088                        + ci2*2224./15. - ci4*896./45.) + eta3*(1703./45.
 2089                        - ci2*1976./45. + ci4*448./45.)) + dm*sin(5.*phi)
 2090                        * (3125.*LAL_PI/192.*si3*ci*(1. - 2.*eta))
 2091                        + si4*ci*sin(6.*phi)*(9153./280. - ci2*243./35.
 2092                        + eta*(-7371./40. + ci2*243./5.) + eta2*(1296./5.
 2093                        - ci2*486./5.) + eta3*(-3159./40. + ci2*243./5.))
 2094                        + sin(8.*phi)*(-2048./315.*si6*ci*(1. - 7.*eta
 2095                        + 14.*eta2 - 7.*eta3));
 2096#if __GNUC__ >= 7 && !defined __INTEL_COMPILER
 2097                __attribute__ ((fallthrough));
 2098#endif
 2099            /* case LAL_PNORDER_TWO_POINT_FIVE: */
 2100            case 5:
 2101                hp25 = cos(phi)*si*dm*(1771./5120. - ci2*1667./5120.
 2102                        + ci4*217./9216. - ci6/9126. + eta*(681./256.
 2103                        + ci2*13./768. - ci4*35./768. + ci6/2304.)
 2104                        + eta2*(-3451./9216. + ci2*673./3072. - ci4*5./9216.
 2105                        - ci6/3072.)) + cos(2.*phi)*LAL_PI*(19./3. + 3.*ci2
 2106                        - ci4*2./3. + eta*(-16./3. + ci2*14./3. + 2.*ci4))
 2107                        + cos(3.*phi)*si*dm*(3537./1024. - ci2*22977./5120.
 2108                        - ci4*15309./5120. + ci6*729./5120.
 2109                        + eta*(-23829./1280. + ci2*5529./1280.
 2110                        + ci4*7749./1280. - ci6*729./1280.)
 2111                        + eta2*(29127./5120. - ci2*27267./5120.
 2112                        - ci4*1647./5120. + ci6*2187./5120.)) + cos(4.*phi)
 2113                        * (-16.*LAL_PI/3.*(1. + ci2)*si2*(1. - 3.*eta))
 2114                        + cos(5.*phi)*si*dm*(-108125./9216. + ci2*40625./9216.
 2115                        + ci4*83125./9216. - ci6*15625./9216.
 2116                        + eta*(8125./256. - ci2*40625./2304. - ci4*48125./2304.
 2117                        + ci6*15625./2304.) + eta2*(-119375./9216.
 2118                        + ci2*40625./3072. + ci4*44375./9216.
 2119                        - ci6*15625./3072.)) + cos(7.*phi)*dm
 2120                        * (117649./46080.*si5*(1. + ci2)*(1. - 4.*eta
 2121                        + 3.*eta2)) + sin(2.*phi)*(-9./5. + ci2*14./5.
 2122                        + ci4*7./5. + eta*(32. + ci2*56./5. - ci4*28./5.))
 2123                        + sin(4.*phi)*si2*(1. + ci2)*(56./5. - 32.*log(2.)/3.
 2124                        + eta*(-1193./30. + 32.*log(2.)));
 2125                /* below would have a constant memory term of si2*ci*eta*6./5. */
 2126                hc25 = cos(2.*phi)*ci*(2. - ci2*22./5. + eta*(-282./5.
 2127                        + ci2*94./5.)) + cos(4.*phi)*ci*si2*(-112./5.
 2128                        + 64.*log(2.)/3. + eta*(1193./15. - 64.*log(2.)))
 2129                        + sin(phi)*si*ci*dm*(-913./7680. + ci2*1891./11520.
 2130                        - ci4*7./4608. + eta*(1165./384. - ci2*235./576.
 2131                        + ci4*7./1152.) + eta2*(-1301./4608. + ci2*301./2304.
 2132                        - ci4*7./1536.)) + sin(2.*phi)*LAL_PI*ci*(34./3.
 2133                        - ci2*8./3. + eta*(-20./3. + 8.*ci2))
 2134                        + sin(3.*phi)*si*ci*dm*(12501./2560. - ci2*12069./1280.
 2135                        + ci4*1701./2560. + eta*(-19581./640. + ci2*7821./320.
 2136                        - ci4*1701./640.) + eta2*(18903./2560.
 2137                        - ci2*11403./1280. + ci4*5103./2560.))
 2138                        + sin(4.*phi)*si2*ci*(-32.*LAL_PI/3.*(1. - 3.*eta))
 2139                        + sin(5.*phi)*si*ci*dm*(-101875./4608. + ci2*6875./256.
 2140                        - ci4*21875./4608. + eta*(66875./1152.
 2141                        - ci2*44375./576. + ci4*21875./1152.)
 2142                        + eta2*(-100625./4608. + ci2*83125./2304.
 2143                        - ci4*21875./1536.)) + sin(7.*phi)*si5*ci*dm
 2144                        * (117649./23040.*(1. - 4.*eta + 3.*eta2));
 2145#if __GNUC__ >= 7 && !defined __INTEL_COMPILER
 2146                __attribute__ ((fallthrough));
 2147#endif
 2148            /* case LAL_PNORDER_TWO: */
 2149            case 4:
 2150                hp2 = cos(phi)*LAL_PI*si*dm*(-5./8. - ci2/8.)
 2151                        + cos(2.*phi)*(11./60. + ci2*33./10. + ci4*29./24.
 2152                        - ci6/24. + eta*(353./36. - 3.*ci2 - ci4*251./72.
 2153                        + ci6*5./24.) + eta2*(-49./12. + ci2*9./2.
 2154                        - ci4*7./24. - ci6*5./24.)) + cos(3.*phi)*LAL_PI*si*dm
 2155                        * (27./8.*(1 + ci2)) + cos(4.*phi)*si2*2./15.*(59.
 2156                        + ci2*35. - ci4*8.
 2157                        - eta*5./3.*(131. + 59.*ci2 + 24.*ci4)
 2158                        + eta2*5.*(21. - 3.*ci2 - 8.*ci4))
 2159                        + cos(6.*phi)*(-81./40.*si4*(1. + ci2)
 2160                        * (1. - 5.*eta + 5.*eta2)) + sin(phi)*si*dm
 2161                        * (11./40. + 5.*log(2)/4. + ci2*(7./40. + log(2)/4.))
 2162                        + sin(3.*phi)*si*dm*((-189./40. + 27./4.*log(3./2.))
 2163                        * (1. + ci2));
 2164                hc2 = cos(phi)*si*ci*dm*(-9./20. - 3./2.*log(2.))
 2165                        + cos(3.*phi)*si*ci*dm*(189./20. - 27./2.*log(3./2.))
 2166                        - sin(phi)*si*ci*dm*3.*LAL_PI/4.
 2167                        + sin(2.*phi)*ci*(17./15. + ci2*113./30. - ci4/4.
 2168                        + eta*(143./9. - ci2*245./18. + ci4*5./4.)
 2169                        + eta2*(-14./3. + ci2*35./6. - ci4*5./4.))
 2170                        + sin(3.*phi)*si*ci*dm*27.*LAL_PI/4.
 2171                        + sin(4.*phi)*ci*si2*4./15.*(55. - 12.*ci2
 2172                        - eta*5./3.*(119. - 36.*ci2)
 2173                        + eta2*5.*(17. - 12.*ci2))
 2174                        + sin(6.*phi)*ci*(-81./20.*si4
 2175                        * (1. - 5.*eta + 5.*eta2));
 2176#if __GNUC__ >= 7 && !defined __INTEL_COMPILER
 2177                __attribute__ ((fallthrough));
 2178#endif
 2179            /* case LAL_PNORDER_ONE_POINT_FIVE: */
 2180            case 3:
 2181                hp15 = cos(phi)*si*dm*(19./64. + ci2*5./16. - ci4/192.
 2182                        + eta*(-49./96. + ci2/8. + ci4/96.))
 2183                        + cos(2.*phi)*(-2.*LAL_PI*(1. + ci2))
 2184                        + cos(3.*phi)*si*dm*(-657./128. - ci2*45./16.
 2185                        + ci4*81./128. + eta*(225./64. - ci2*9./8.
 2186                        - ci4*81./64.)) + cos(5.*phi)*si*dm*(625./384.*si2
 2187                        * (1. + ci2)*(1. - 2.*eta));
 2188                hc15 = sin(phi)*si*ci*dm*(21./32. - ci2*5./96.
 2189                        + eta*(-23./48. + ci2*5./48.))
 2190                        - 4.*LAL_PI*ci*sin(2.*phi) + sin(3.*phi)*si*ci*dm
 2191                        * (-603./64. + ci2*135./64.
 2192                        + eta*(171./32. - ci2*135./32.))
 2193                        + sin(5.*phi)*si*ci*dm*(625./192.*si2*(1. - 2.*eta));
 2194#if __GNUC__ >= 7 && !defined __INTEL_COMPILER
 2195                __attribute__ ((fallthrough));
 2196#endif
 2197            /* case LAL_PNORDER_ONE: */
 2198            case 2:
 2199                hp1 = cos(2.*phi)*(19./6. + 3./2.*ci2 - ci4/3.
 2200                        + eta*(-19./6. + ci2*11./6. + ci4))
 2201                        - cos(4.*phi) * (4./3.*si2*(1. + ci2)*(1. - 3.*eta));
 2202                hc1 = sin(2.*phi)*ci*(17./3. - ci2*4./3.
 2203                        + eta*(-13./3. + 4.*ci2))
 2204                        + sin(4.*phi)*ci*si2*(-8./3.*(1. - 3.*eta));
 2205#if __GNUC__ >= 7 && !defined __INTEL_COMPILER
 2206                __attribute__ ((fallthrough));
 2207#endif
 2208            /*case LAL_PNORDER_HALF:*/
 2209            case 1:
 2210                hp05 = - si*dm*(cos(phi)*(5./8. + ci2/8.)
 2211                        - cos(3.*phi)*(9./8. + 9.*ci2/8.));
 2212                hc05 = si*ci*dm*(-sin(phi)*3./4. + sin(3.*phi)*9./4.);
 2213#if __GNUC__ >= 7 && !defined __INTEL_COMPILER
 2214                __attribute__ ((fallthrough));
 2215#endif
 2216            case 0:
 2217                /* below would have a constant memory term of -si2/96.*(17. + ci2) */
 2218                hp0 = -(1. + ci2)*cos(2.*phi);
 2219                hc0 = -2.*ci*sin(2.*phi);
 2220                break;
 2221            /*case LAL_PNORDER_NEWTONIAN:*/
 2222            default:
 2223                XLALPrintError("XLAL Error - %s: Invalid amp. PN order %d\n",
 2224                        __func__, ampO );
 2225                XLAL_ERROR(XLAL_EINVAL);
 2226                break;
 2227        } /* End switch on ampO */
 2228 
 2229        /* Fill the output polarization arrays */
 2230        (*hplus)->data->data[idx] = ampfac * v2 * ( hp0 + v * ( hp05
 2231                + v * ( hp1 + v * ( hp15 + v * ( hp2 + v * ( hp25 + v * hp3
 2232                ) ) ) ) ) );
 2233        (*hcross)->data->data[idx] = ampfac * v2 * ( hc0 + v * ( hc05
 2234                + v * ( hc1 + v * ( hc15 + v * ( hc2 + v * ( hc25 + v * hc3
 2235                ) ) ) ) ) );
 2236 
 2237    } /* end loop over time series samples idx */
 2238    return XLAL_SUCCESS;
 2239}
 2240/** @} */
 2241 
 2242/**
 2243 * Given time series for a binary's orbital dynamical variables,
 2244 * construct the waveform polarizations h+ and hx as a sum of
 2245 * -2 spin-weighted spherical harmonic modes, h_lm.
 2246 * NB: Valid only for non-precessing systems!
 2247 *
 2248 * Implements Equation (11) of:
 2249 * Lawrence E. Kidder, \"Using Full Information When Computing Modes of
 2250 * Post-Newtonian Waveforms From Inspiralling Compact Binaries in Circular
 2251 * Orbit\", Physical Review D 77, 044016 (2008), arXiv:0710.0614v1 [gr-qc].
 2252 */
 2253int XLALSimInspiralPNPolarizationWaveformsFromModes(
 2254        REAL8TimeSeries **hplus,  /**< +-polarization waveform [returned] */
 2255               REAL8TimeSeries **hcross, /**< x-polarization waveform [returned] */
 2256               REAL8TimeSeries *v,       /**< post-Newtonian parameter */
 2257               REAL8TimeSeries *phi,     /**< orbital phase */
 2258               REAL8 v0,                 /**< tail-term gauge choice (default = 1) */
 2259               REAL8 m1,                 /**< mass of companion 1 */
 2260               REAL8 m2,                 /**< mass of companion 2 */
 2261               REAL8 r,                  /**< distance of source */
 2262               REAL8 i,                  /**< inclination of source (rad) */
 2263               int O                     /**< twice post-Newtonian order */
 2264        )
 2265{
 2266    int l, m;
 2267    LAL_CHECK_VALID_SERIES(v, XLAL_FAILURE);
 2268    LAL_CHECK_VALID_SERIES(phi, XLAL_FAILURE);
 2269    LAL_CHECK_CONSISTENT_TIME_SERIES(v, phi, XLAL_FAILURE);
 2270    *hplus = XLALCreateREAL8TimeSeries( "H_PLUS", &v->epoch, 0.0, v->deltaT, &lalStrainUnit, v->data->length );
 2271    *hcross = XLALCreateREAL8TimeSeries( "H_CROSS", &v->epoch, 0.0, v->deltaT, &lalStrainUnit, v->data->length );
 2272    if ( ! hplus || ! hcross )
 2273        XLAL_ERROR(XLAL_EFUNC);
 2274    memset((*hplus)->data->data, 0, (*hplus)->data->length*sizeof(*(*hplus)->data->data));
 2275    memset((*hcross)->data->data, 0, (*hcross)->data->length*sizeof(*(*hcross)->data->data));
 2276    for ( l = 2; l <= LAL_PN_MODE_L_MAX; ++l ) {
 2277        for ( m = 1; m <= l; ++m ) {
 2278            COMPLEX16TimeSeries *hmode;
 2279            hmode = XLALCreateSimInspiralPNModeCOMPLEX16TimeSeries(v, phi, v0, m1, m2, r, O, l, m);
 2280            if ( ! hmode )
 2281                XLAL_ERROR(XLAL_EFUNC);
 2282            if ( XLALSimAddMode(*hplus, *hcross, hmode, i, 0.0, l, m, 1) < 0 )
 2283                XLAL_ERROR(XLAL_EFUNC);
 2284            XLALDestroyCOMPLEX16TimeSeries(hmode);
 2285        }
 2286    }
 2287    return 0;
 2288}
 2289 
 2290/**
 2291 * Compute the polarizations from all the -2 spin-weighted spherical harmonic
 2292 * modes stored in 'hlms'. Be sure that 'hlms' is the head of the linked list!
 2293 *
 2294 * The computation done is:
 2295 * \f$hp(t) - i hc(t) = \sum_l \sum_m h_lm(t) -2Y_lm(iota,psi)\f$
 2296 *
 2297 * iota and psi are the inclination and polarization angle of the observer
 2298 * relative to the source of GWs.
 2299 */
 2300int XLALSimInspiralPolarizationsFromSphHarmTimeSeries(
 2301    REAL8TimeSeries **hp, /**< Plus polarization time series [returned] */
 2302    REAL8TimeSeries **hc, /**< Cross polarization time series [returned] */
 2303    SphHarmTimeSeries *hlms, /**< Head of linked list of waveform modes */
 2304    REAL8 iota, /**< inclination of viewer to source frame (rad) */
 2305    REAL8 phiRef /**< reference phase (rad) */
 2306    )
 2307{
 2308    int ret;
 2309    SphHarmTimeSeries *ts = hlms;
 2310    size_t length = ts->mode->data->length;
 2311    // Destroy hp, hc TimeSeries if they already exist
 2312    if( (*hp) ) XLALDestroyREAL8TimeSeries( *hp );
 2313    if( (*hc) ) XLALDestroyREAL8TimeSeries( *hc );
 2314    *hp = XLALCreateREAL8TimeSeries("hplus", &(ts->mode->epoch), ts->mode->f0,
 2315                ts->mode->deltaT, &lalStrainUnit, length);
 2316    *hc = XLALCreateREAL8TimeSeries("hplus", &(ts->mode->epoch), ts->mode->f0,
 2317                ts->mode->deltaT, &lalStrainUnit, length);
 2318    memset( (*hp)->data->data, 0, (*hp)->data->length*sizeof(REAL8) );
 2319    memset( (*hc)->data->data, 0, (*hc)->data->length*sizeof(REAL8) );
 2320    while (ts) { // Add the contribution from the current mode to hp, hx...
 2321        // This function adds hlm(t) * Y_lm(incl,phiRef) to (h+ - i hx)(t)
 2322        ret = XLALSimAddMode(*hp, *hc, ts->mode, iota, phiRef, ts->l, ts->m, 0);
 2323        if( ret != XLAL_SUCCESS ) XLAL_ERROR(XLAL_EFUNC);
 2324        ts = ts->next;
 2325    }
 2326 
 2327    return XLAL_SUCCESS;
 2328}
 2329 
 2330 
 2331/**
 2332  Function returning the Fourier domain polarizations for positive frequencies built from the individual modes computed with ChooseFDModes.
 2333        The output should be equivalent to that from ChooseFDWaveform, close to machine precision.
 2334        Some of the AS models use the argument phiRef internally to build the hlms and build the polarizations with an azimuthal angle different from Pi/2 - phiRef.
 2335        In this function we take into account those differences among models.
 2336        For the precessing model IMRPhenomXPHM, since the modes are returned in the J-frame, the polarizations are built using theta_JN instead of the inclination and azimuthal angle = 0.
 2337*/
 2338int XLALSimInspiralPolarizationsFromChooseFDModes(
 2339    COMPLEX16FrequencySeries **hptilde,     /**< FD plus polarization */
 2340    COMPLEX16FrequencySeries **hctilde,     /**< FD cross polarization */
 2341    const REAL8 m1,                         /**< mass of companion 1 (kg) */
 2342    const REAL8 m2,                         /**< mass of companion 2 (kg) */
 2343    const REAL8 S1x,                        /**< x-component of the dimensionless spin of object 1 */
 2344    const REAL8 S1y,                        /**< y-component of the dimensionless spin of object 1 */
 2345    const REAL8 S1z,                        /**< z-component of the dimensionless spin of object 1 */
 2346    const REAL8 S2x,                        /**< x-component of the dimensionless spin of object 2 */
 2347    const REAL8 S2y,                        /**< y-component of the dimensionless spin of object 2 */
 2348    const REAL8 S2z,                        /**< z-component of the dimensionless spin of object 2 */
 2349    const REAL8 distance,                   /**< distance of source (m) */
 2350    const REAL8 inclination,                /**< inclination of source (rad) */
 2351    const REAL8 phiRef,                     /**< reference orbital phase (rad) */
 2352    const REAL8 UNUSED longAscNodes,        /**< longitude of ascending nodes, degenerate with the polarization angle, Omega in documentation */
 2353    const REAL8 UNUSED eccentricity,        /**< eccentricity at reference epoch */
 2354    const REAL8 UNUSED meanPerAno,          /**< mean anomaly of periastron */
 2355    // frequency sampling parameters, no default value
 2356    const REAL8 deltaF,                     /**< sampling interval (Hz) */
 2357    const REAL8 f_min,                      /**< starting GW frequency (Hz) */
 2358    const REAL8 f_max,                      /**< ending GW frequency (Hz) */
 2359    REAL8 f_ref,                            /**< Reference frequency (Hz) */
 2360    LALDict *LALparams,                     /**< LAL dictionary containing accessory parameters */
 2361    const Approximant approximant           /**< post-Newtonian approximant to use for waveform production */
 2362    )
 2363{
 2364 
 2365        /* Adjust the reference frequency for certain precessing approximants:
 2366         * if that approximate interprets f_ref==0 to be f_min, set f_ref=f_min;
 2367         * otherwise do nothing */
 2368        FIX_REFERENCE_FREQUENCY(f_ref, f_min, approximant);
 2369 
 2370    int ret = XLAL_SUCCESS;
 2371    REAL8 phiRef_modes = 0;
 2372    REAL8 theta = inclination;
 2373    REAL8 azimuthal = LAL_PI_2 - phiRef;
 2374    REAL8 zeta_polarization = 0;
 2375 
 2376    switch (approximant)
 2377    {
 2378        case IMRPhenomXHM:
 2379        phiRef_modes = phiRef;
 2380        azimuthal = LAL_PI_2;
 2381        break;
 2382 
 2383        case IMRPhenomXPHM:
 2384        phiRef_modes = phiRef;
 2385        REAL8 d1=0, d2=0, d3=0, d4=0, d5=0;
 2386        ret = XLALSimIMRPhenomXPCalculateModelParametersFromSourceFrame(&d1, &d2, &d3, &theta, &d4, &d5, &zeta_polarization, m1, m2, f_ref, phiRef, inclination, S1x,S1y,S1z, S2x,S2y,S2z, LALparams);
 2387        XLAL_CHECK(XLAL_SUCCESS == ret, XLAL_EFUNC, "Error: XLALSimIMRPhenomXPCalculateModelParametersFromSourceFrame failed.\n");
 2388        azimuthal = 0.;
 2389 
 2390        break;
 2391        case IMRPhenomXO4a:
 2392        phiRef_modes = phiRef;
 2393        d1=0, d2=0, d3=0, d4=0, d5=0;
 2394        ret = XLALSimIMRPhenomXPCalculateModelParametersFromSourceFrame(&d1, &d2, &d3, &theta, &d4, &d5, &zeta_polarization, m1, m2, f_ref, phiRef, inclination, S1x,S1y,S1z, S2x,S2y,S2z, LALparams);
 2395        XLAL_CHECK(XLAL_SUCCESS == ret, XLAL_EFUNC, "Error: XLALSimIMRPhenomXPCalculateModelParametersFromSourceFrame failed.\n");
 2396        azimuthal = 0.;
 2397        break;
 2398 
 2399        case IMRPhenomXPNR:
 2400        phiRef_modes = phiRef;
 2401        d1=0, d2=0, d3=0, d4=0, d5=0;
 2402        ret = XLALSimIMRPhenomXPCalculateModelParametersFromSourceFrame(&d1, &d2, &d3, &theta, &d4, &d5, &zeta_polarization, m1, m2, f_ref, phiRef, inclination, S1x,S1y,S1z, S2x,S2y,S2z, LALparams);
 2403        XLAL_CHECK(XLAL_SUCCESS == ret, XLAL_EFUNC, "Error: XLALSimIMRPhenomXPCalculateModelParametersFromSourceFrame failed.\n");
 2404        azimuthal = 0.;
 2405        break;
 2406 
 2407        case SEOBNRv4HM_ROM:
 2408 
 2409        break;
 2410        case SEOBNRv5_ROM:
 2411 
 2412        break;
 2413        case SEOBNRv5HM_ROM:
 2414 
 2415        break;
 2416        case IMRPhenomHM:
 2417        phiRef_modes = phiRef;
 2418        break;
 2419        default:
 2420                XLALPrintError("Approximant not implemented\n");
 2421                XLAL_ERROR(XLAL_EINVAL);
 2422    }
 2423 
 2424 
 2425    SphHarmFrequencySeries **hlms = XLALMalloc(sizeof(SphHarmFrequencySeries));
 2426    *hlms = XLALSimInspiralChooseFDModes(m1, m2, S1x, S1y, S1z, S2x, S2y, S2z, deltaF, f_min, f_max, f_ref, phiRef_modes, distance, inclination, LALparams, approximant);
 2427    if(!(*hlms)){
 2428        XLAL_ERROR(XLAL_EFUNC, "Error: XLALSimInspiralChooseFDModes failed\n");
 2429    }
 2430 
 2431    UINT4 len = (*hlms)->mode->data->length;
 2432    UINT4 offset = 0;
 2433 
 2434    /* This is to account that ChooseFDModes return the modes for both negative and positve frequencies,
 2435       but here we return the polarizations just for positive frequencies. */
 2436    len = (UINT4) ceil(len/2.);
 2437    offset = len-1;
 2438 
 2439    /* Create polarizations objects */
 2440    *hptilde = XLALCreateCOMPLEX16FrequencySeries("FD hplus",
 2441                    &((*hlms)->mode->epoch), (*hlms)->mode->f0, (*hlms)->mode->deltaF,
 2442                    &((*hlms)->mode->sampleUnits), len);
 2443    *hctilde = XLALCreateCOMPLEX16FrequencySeries("FD hcross",
 2444                    &((*hptilde)->epoch), (*hptilde)->f0, (*hptilde)->deltaF,
 2445                    &((*hptilde)->sampleUnits), (*hptilde)->data->length);
 2446    memset((*hptilde)->data->data, 0, (len) * sizeof(COMPLEX16));
 2447    memset((*hctilde)->data->data, 0, (len) * sizeof(COMPLEX16));
 2448 
 2449 
 2450    SphHarmFrequencySeries *hlms_tmp = *hlms;
 2451 
 2452    /* Build the polarizations by summing the modes*/
 2453    while ( hlms_tmp ){
 2454        COMPLEX16 Ylm = XLALSpinWeightedSphericalHarmonic(theta, azimuthal, -2, hlms_tmp->l, hlms_tmp->m);
 2455        COMPLEX16 Ylmstar = conj(Ylm);
 2456 
 2457        for(UINT4 idx = 0; idx<len; idx++){
 2458            COMPLEX16 hlm = hlms_tmp->mode->data->data[idx + offset];
 2459            COMPLEX16 hlm2 = conj(hlms_tmp->mode->data->data[len - 1 - idx]);
 2460            (*hptilde)->data->data[idx] += 0.5 * (hlm * Ylm + hlm2 * Ylmstar);
 2461            (*hctilde)->data->data[idx] += 0.5 * I * (hlm * Ylm - hlm2 * Ylmstar);
 2462        }
 2463        hlms_tmp = hlms_tmp->next;
 2464    }
 2465 
 2466    /* Free memory */
 2467    XLALDestroySphHarmFrequencySeries(*hlms);
 2468    XLALFree(hlms);
 2469    XLALDestroySphHarmFrequencySeries(hlms_tmp);
 2470 
 2471 
 2472    /* Add the correct polarization angle for IMRPhenomXPHM */
 2473    if(fabs(zeta_polarization) > 0)
 2474    {
 2475        COMPLEX16 PhPpolp, PhPpolc;
 2476        REAL8 cosPolFac, sinPolFac;
 2477 
 2478        cosPolFac = cos(2.0 * zeta_polarization);
 2479        sinPolFac = sin(2.0 * zeta_polarization);
 2480 
 2481        for (UINT4 i = 0; i < (*hptilde)->data->length; i++)
 2482        {
 2483            PhPpolp = (*hptilde)->data->data[i];
 2484            PhPpolc = (*hctilde)->data->data[i];
 2485 
 2486            (*hptilde)->data->data[i] = cosPolFac * PhPpolp + sinPolFac * PhPpolc;
 2487            (*hctilde)->data->data[i] = cosPolFac * PhPpolc - sinPolFac * PhPpolp;
 2488        }
 2489    }
 2490 
 2491 
 2492  /* This final rotation is taken from ChooseFDWaveform */
 2493    REAL8 polariz=longAscNodes;
 2494    if (polariz) {
 2495        COMPLEX16 tmpP,tmpC;
 2496        for (UINT4 idx=0;idx<(*hptilde)->data->length;idx++) {
 2497tmpP=(*hptilde)->data->data[idx];
 2498tmpC=(*hctilde)->data->data[idx];
 2499(*hptilde)->data->data[idx] =cos(2.*polariz)*tmpP+sin(2.*polariz)*tmpC;
 2500(*hctilde)->data->data[idx]=cos(2.*polariz)*tmpC-sin(2.*polariz)*tmpP;
 2501        }
 2502    }
 2503 
 2504    if (ret == XLAL_FAILURE) XLAL_ERROR(XLAL_EFUNC);
 2505    if (XLALSimInspiralWaveformParamsLookupEnableLIV(LALparams))
 2506        ret = XLALSimLorentzInvarianceViolationTerm(hptilde, hctilde, m1/LAL_MSUN_SI, m2/LAL_MSUN_SI, distance, LALparams);
 2507    if (ret == XLAL_FAILURE) XLAL_ERROR(XLAL_EFUNC);
 2508 
 2509    return ret;
 2510}
 2511 
 2512 
 2513 
 2514/**
 2515    Return polarizations for positive frequencies built by summing the individual modes present
 2516    in the input array SphHarmFrequencySeries *hlms     computed with ChooseFDModes.
 2517    Notice that in general the output may not be close to machine precision with ChooseFDWaveform due to differences in
 2518    computing the h_lms and in the use of the azimuthal angle.
 2519    For IMRPhenomXPHM, the argument theta should not be the inclination but theta_JN and phiRef should be 0.
 2520*/
 2521int XLALSimInspiralPolarizationsFromSphHarmFrequencySeries(
 2522    COMPLEX16FrequencySeries **hp, /**< Plus polarization frequency series [returned] */
 2523    COMPLEX16FrequencySeries **hc, /**< Cross polarization frequency series [returned] */
 2524    SphHarmFrequencySeries *hlms,  /**< Head of linked list of waveform modes */
 2525    REAL8 theta,                                                                         /**< Polar angle for the Ylms (rad): Inclination for h_lms in L0-frame and theta_JN for J-frame. */
 2526    REAL8 phi                                                                            /**< Azimuthal angle for the Ylms (rad): pi/2 - phiRef for AS models and 0 for precessing. */
 2527    )
 2528{
 2529    if (!(hlms)){ XLAL_ERROR(XLAL_EFUNC, "SphHarmFrequencySeires object empty.\n");}
 2530 
 2531    SphHarmFrequencySeries *fs = hlms;
 2532    UINT4 len = fs->mode->data->length;
 2533    INT4 offset = 0;
 2534    /* This is to account that ChooseFDModes return the modes for both negative and positve frequencies,
 2535        but here we return the polarizations just for positive frequencies. */
 2536    len = (UINT4) ceil(len/2.);
 2537    offset = len-1;
 2538    // Destroy hp, hc FrequencySeries if they already exist
 2539    if( (*hp) ) XLALDestroyCOMPLEX16FrequencySeries( *hp );
 2540    if( (*hc) ) XLALDestroyCOMPLEX16FrequencySeries( *hc );
 2541    *hp = XLALCreateCOMPLEX16FrequencySeries("hplus", &(fs->mode->epoch), fs->mode->f0,
 2542                fs->mode->deltaF, &(fs->mode->sampleUnits), len);
 2543    *hc = XLALCreateCOMPLEX16FrequencySeries("hcross", &(fs->mode->epoch), fs->mode->f0,
 2544                fs->mode->deltaF, &(fs->mode->sampleUnits), len);
 2545    memset( (*hp)->data->data, 0, (*hp)->data->length*sizeof(COMPLEX16) );
 2546    memset( (*hc)->data->data, 0, (*hc)->data->length*sizeof(COMPLEX16) );
 2547 
 2548 
 2549    /* Build the polarizations by summing the modes */
 2550    while ( fs ){
 2551        COMPLEX16 Ylm = XLALSpinWeightedSphericalHarmonic(theta, phi, -2, fs->l, fs->m);
 2552        COMPLEX16 Ylmstar = conj(Ylm);
 2553 
 2554        for(UINT4 idx = 0; idx<len; idx++){
 2555            COMPLEX16 hlm = fs->mode->data->data[idx + offset];
 2556            COMPLEX16 hlm2 = conj(fs->mode->data->data[len - 1 - idx]);
 2557            (*hp)->data->data[idx] += 0.5 * (hlm * Ylm + hlm2 * Ylmstar);
 2558            (*hc)->data->data[idx] += 0.5 * I * (hlm * Ylm - hlm2 * Ylmstar);
 2559        }
 2560        fs = fs->next;
 2561    }
 2562    XLALDestroySphHarmFrequencySeries(fs);
 2563 
 2564    return XLAL_SUCCESS;
 2565}
 2566 
 2567 
 2568/**
 2569 * Given time series for a binary's orbital dynamical variables,
 2570 * computes the radial and angular orbital motion; then constructs
 2571 * the waveform polarizations h+ and hx in terms of the relative
 2572 * separation r, the `true anomaly` phi and their time derivatives.
 2573 * NB: Valid only for non-spinning binaries in inspiralling!
 2574 * and precessing eccentric orbits!
 2575 *
 2576 * Implements Equations (3.7a) - (3.7c) and Equations (B2a) - (B2d), (B4a), (B4b) of:
 2577 * Sashwat Tanay, Maria Haney, and Achamveedu Gopakumar,
 2578 * \"Frequency and time domain inspiral waveforms from comparable
 2579 * mass compact binaries in eccentric orbits\", (2015);
 2580 * arXiv:TBD
 2581 * https://dcc.ligo.org/P1500148-v1
 2582 *
 2583 * (note that above equations use x = v^2 as the PN expansion parameter)
 2584 *
 2585 * as well as Equations (6a) and (6b) of:
 2586 * Thibault Damour, Achamveedu Gopakumar, and Bala R. Iyer,
 2587 * \"Phasing of gravitational waves from inspiralling eccentric
 2588 * binaries\", Phys. Rev. D 70 064028 (2004);
 2589 * arXiv:gr-qc/0404128.
 2590 */
 2591int XLALSimInspiralPNPolarizationWaveformsEccentric(
 2592    REAL8TimeSeries **hplus,  /**< +-polarization waveform [returned] */
 2593    REAL8TimeSeries **hcross, /**< x-polarization waveform [returned] */
 2594    REAL8TimeSeries *V,       /**< post-Newtonian (PN) parameter */
 2595    REAL8TimeSeries *Ecc,     /**< orbital eccentricity */
 2596    REAL8TimeSeries *U,       /**< eccentric anomaly of quasi-Keplerian orbit */
 2597    REAL8TimeSeries *Phi,     /**< orbital phase */
 2598    REAL8 m1,                 /**< mass of companion 1 (kg) */
 2599    REAL8 m2,                 /**< mass of companion 2 (kg) */
 2600    REAL8 r,                  /**< distance of source (m) */
 2601    REAL8 i,                  /**< inclination of source (rad) */
 2602    int ampO,                 /**< twice PN order of the amplitude */
 2603    int ph_O                  /**< twice PN order of the phase */
 2604    )
 2605{
 2606    REAL8 mt, eta, dist, ampfac, phi, v, et, u;
 2607    REAL8 dt, OTS;
 2608    REAL8 CF_rdot, CF_rphidot, CF_Z, r_sc, rdot_sc, phidot;
 2609    REAL8 rdot, rphidot, Z;
 2610    REAL8 hp0;
 2611    REAL8 hc0;
 2612    REAL8 ci, si, ci2, si2;
 2613    INT4 idx, len;
 2614 
 2615    /* Sanity check input time series */
 2616    LAL_CHECK_VALID_SERIES(V, XLAL_FAILURE);
 2617    LAL_CHECK_VALID_SERIES(Ecc, XLAL_FAILURE);
 2618    LAL_CHECK_VALID_SERIES(U, XLAL_FAILURE);
 2619    LAL_CHECK_VALID_SERIES(Phi, XLAL_FAILURE);
 2620    LAL_CHECK_CONSISTENT_TIME_SERIES(V, Ecc, XLAL_FAILURE);
 2621    LAL_CHECK_CONSISTENT_TIME_SERIES(V, U, XLAL_FAILURE);
 2622    LAL_CHECK_CONSISTENT_TIME_SERIES(V, Phi, XLAL_FAILURE);
 2623 
 2624    /* Allocate polarization vectors and set to 0 */
 2625    *hplus = XLALCreateREAL8TimeSeries( "H_PLUS", &V->epoch, 0.0,
 2626            V->deltaT, &lalStrainUnit, V->data->length );
 2627    *hcross = XLALCreateREAL8TimeSeries( "H_CROSS", &V->epoch, 0.0,
 2628            V->deltaT, &lalStrainUnit, V->data->length );
 2629    if ( ! hplus || ! hcross )
 2630        XLAL_ERROR(XLAL_EFUNC);
 2631    memset((*hplus)->data->data, 0, (*hplus)->data->length
 2632            * sizeof(*(*hplus)->data->data));
 2633    memset((*hcross)->data->data, 0, (*hcross)->data->length
 2634            * sizeof(*(*hcross)->data->data));
 2635 
 2636    mt = (m1 + m2)/LAL_MSUN_SI;
 2637    eta = m1 * m2 / pow(m1 + m2, 2.0); // symmetric mass ratio - '\nu' in the paper
 2638    dist = r / LAL_C_SI;   // r (m) / c (m/s) --> dist in units of seconds
 2639    /* convert mass from kg to s, so ampfac ~ M/dist is dimensionless */
 2640    ampfac = mt * LAL_MTSUN_SI * eta / dist;
 2641 
 2642    /*
 2643     * cosines and sines of inclination between
 2644     * line of sight (N) and binary orbital angular momentum (L_N)
 2645     */
 2646    ci = cos(i);        si = sin(i);
 2647    ci2 = ci*ci;
 2648    si2 = si*si;
 2649 
 2650    /* loop over time steps and compute first radial and angular orbital variables,
 2651     * then the waveform polarizations h+ and hx */
 2652    len = V->data->length;
 2653    for(idx = 0; idx < len; idx++)
 2654    {
 2655        /* Abbreviated names in lower case for time series at this sample */
 2656        phi = Phi->data->data[idx];     et = Ecc->data->data[idx];      u = U->data->data[idx]; v = V->data->data[idx];
 2657 
 2658    /* Some abbreviated functions in terms of u and et. */
 2659    dt  = 1. - et * cos(u);
 2660    OTS = sqrt(1. - et * et);
 2661 
 2662    /*
 2663         * First set the functions for the dimensionless orbital variables
 2664     * (1/c)*dr/dt, (r/c)*dphi/dt, Z = G*m/(r*c^2) to 0.
 2665     * Then use a switch to set proper non-zero values
 2666         * up to order ph_O for the contributions to the dimensionless variables. Note we
 2667         * fall through the PN orders and break only after Newt. order
 2668         */
 2669 
 2670    rdot = rphidot = Z = 0;
 2671 
 2672    /* Common factors in PN accurate expressions for orbital variables */
 2673    CF_rdot = et * v*sin(u)/dt;
 2674    CF_rphidot = OTS * v / dt;
 2675    CF_Z = pow(v, 2.0) / dt;
 2676 
 2677    switch( ph_O )
 2678        {
 2679        /* case LAL_PNORDER_FOUR: */
 2680            case 8:
 2681                XLALPrintError("XLAL Error - %s: dynamical variables not known "
 2682                        "to PN order %d\n", __func__, ph_O );
 2683                XLAL_ERROR(XLAL_EINVAL);
 2684                break;
 2685            /* case LAL_PNORDER_THREE_POINT_FIVE: */
 2686            case 7:
 2687                XLALPrintError("XLAL Error - %s: dynamical variables not known "
 2688                        "to PN order %d\n", __func__, ph_O );
 2689                XLAL_ERROR(XLAL_EINVAL);
 2690                break;
 2691            /* case LAL_PNORDER_THREE: */
 2692            case 6:
 2693        XLALPrintError("XLAL Error - %s: dynamical variables not yet implemented "
 2694                        "to PN order %d\n", __func__, ph_O );
 2695                XLAL_ERROR(XLAL_EINVAL);
 2696                break;
 2697            /* case LAL_PNORDER_TWO_POINT_FIVE: */
 2698            case 5:
 2699        XLALPrintError("XLAL Error - %s: dynamical variables not yet implemented "
 2700                        "to PN order %d\n", __func__, ph_O );
 2701                XLAL_ERROR(XLAL_EINVAL);
 2702                break;
 2703        case -1: // Highest known PN order - move if higher terms added!
 2704            /* case LAL_PNORDER_TWO: */
 2705            case 4:
 2706        r_sc    = 1.
 2707              //==============================================================================
 2708              + ((-24. + dt * (18. - 7. * eta) + 9. * eta + pow(et, 2.0) * (24. - 9. * eta
 2709              + dt * (-6. + 7. * eta))) * pow(v, 2.0)) / (6. * dt * pow(OTS, 2.0))
 2710              //==============================================================================
 2711              + ((-288. + 765. * eta - 27. * pow(eta,  2.0)
 2712              + pow(et, 4.0) * (261. * eta - 27 * pow(eta, 2.0))
 2713              + pow(et, 2.0) * (288. - 1026. * eta + 54. * pow(eta, 2.0))
 2714              + (-540. + pow(et, 2.0) * (540. - 216. * eta)
 2715              + 216. * eta) * OTS + dt * (648. - 567. * eta + 35. * pow(eta, 2.0)
 2716              + pow(et, 2.0) * (468. + 150. * eta - 70. * pow(eta, 2.0))
 2717              + pow(et, 4.0) * (72. - 231. * eta + 35. * pow(eta, 2.0))
 2718              + (180. - 72. * eta + pow(et, 2.0) * (-180. + 72. * eta)) * OTS)) * pow(v, 4.0))
 2719              / (72. * dt * pow(OTS, 4.0));
 2720              //==============================================================================
 2721        phidot = 1.
 2722              //===========================================================================================
 2723              + (-1. + dt + pow(et, 2.0)) * (-4. + eta) * pow(v, 2.0) / (dt * pow(OTS, 2.0))
 2724              //===========================================================================================
 2725              + (-6. * pow(1. - pow(et, 2.0), 3.0) * eta * (3. + 2. * eta)
 2726              + pow(dt, 3.0) * (42. + 22. * eta + 8.* pow(eta, 2.0)
 2727              + pow(et, 2.0) * (-147. + 8. * eta - 14. * pow(eta, 2.0)))
 2728              + dt * (108. + 63. * eta + 33. * pow(eta, 2.0)
 2729              + pow(et, 2.0) * (-216. - 126. * eta - 66. * pow(eta, 2.0))
 2730              + pow(et, 4.0) * (108. + 63. * eta + 33. * pow(eta, 2.0)))
 2731              + pow(dt, 2.0) * (-240. - 31. * eta - 29. * pow(eta, 2.0)
 2732              + pow(et, 4.0) * (-48. + 17. * eta - 17. * pow(eta, 2.0))
 2733              + pow(et, 2.0) * (288. + 14. * eta + 46. * pow(eta,2)))
 2734              + 18. * pow(dt, 2.0) * (-2. + dt + 2. * pow(et, 2.0)) * (-5. + 2. * eta) * OTS) * pow(v, 4.0)
 2735              / (12. * pow(dt, 3.0) * pow(OTS, 4.0));
 2736              //===========================================================================================
 2737        rdot_sc = 1.
 2738              //==========================================================================================
 2739              + (-7. * eta + pow(et, 2.0) * (-6. + 7. * eta)) * pow(v, 2.0) / (6. * pow(OTS, 2.0))
 2740              //==========================================================================================
 2741              + (-135. * eta + 9. * pow(eta, 2.0) + pow(et, 2.0) * (405. * eta - 27. * pow(eta, 2.0))
 2742              + pow(et, 6.0) * (135. * eta - 9. * pow(eta, 2.0))
 2743              + pow(et, 4.0) * (-405. * eta + 27 * pow(eta, 2.0))
 2744              + dt * (-540. + 351. * eta - 9. * pow(eta, 2.0)
 2745              + pow(et, 4.0) * (-540. + 351. * eta - 9. * pow(eta, 2.0))
 2746              + pow(et, 2.0) * (1080. - 702. * eta + 18. * pow(eta, 2.0)))
 2747              + pow(dt, 3.0) * (-324. + 189. * eta + 35. * pow(eta, 2.0)
 2748              + pow(et, 2.0) * (-234. + 366. * eta - 70. * pow(eta, 2.0))
 2749              + pow(et, 4.0) * (72. - 231. * eta + 35. * pow(eta, 2.0)))
 2750              - 36 * pow(dt, 2.0) * (3. + dt) * (1 - pow(et, 2.0)) * (-5. + 2. * eta) * OTS) * pow(v, 4.0)
 2751              / (72. * pow(dt, 3.0) * pow(OTS, 4.0));
 2752              //==========================================================================================
 2753                break;
 2754            /* case LAL_PNORDER_ONE_POINT_FIVE: */
 2755            case 3:
 2756        r_sc    = 1.
 2757              //===========================================================================
 2758              + ((-24. + dt * (18. - 7. * eta) + 9. * eta + pow(et, 2.0) * (24. - 9. * eta
 2759              + dt * (-6. + 7. * eta))) * pow(v, 2.0)) / (6. * dt * pow(OTS, 2.0));
 2760              //===========================================================================
 2761        phidot  = 1.
 2762              //==============================================================================
 2763              + (-1. + dt + pow(et, 2.0)) * (-4. + eta) * pow(v, 2.0) / (dt * pow(OTS, 2.0));
 2764              //==============================================================================
 2765        rdot_sc = 1.
 2766              //====================================================================================
 2767              + (-7. * eta + pow(et, 2.0) * (-6. + 7. * eta)) * pow(v, 2.0) / (6. * pow(OTS, 2.0));
 2768              //====================================================================================
 2769                break;
 2770            /* case LAL_PNORDER_ONE: */
 2771            case 2:
 2772        r_sc    = 1.
 2773              //===========================================================================
 2774              + ((-24. + dt * (18. - 7. * eta) + 9. * eta + pow(et, 2.0) * (24. - 9. * eta
 2775              + dt * (-6. + 7. * eta))) * pow(v, 2.0)) / (6. * dt * pow(OTS, 2.0));
 2776              //===========================================================================
 2777        phidot  = 1.
 2778              //==============================================================================
 2779              + (-1. + dt + pow(et, 2.0)) * (-4. + eta) * pow(v, 2.0) / (dt * pow(OTS, 2.0));
 2780              //==============================================================================
 2781        rdot_sc = 1.
 2782              //====================================================================================
 2783              + (-7. * eta + pow(et, 2.0) * (-6. + 7. * eta)) * pow(v, 2.0) / (6. * pow(OTS, 2.0));
 2784              //====================================================================================
 2785                break;
 2786            /*case LAL_PNORDER_HALF:*/
 2787            case 1:
 2788        r_sc    = 1.;
 2789        phidot  = 1.;
 2790        rdot_sc = 1.;
 2791                break;
 2792        /*case LAL_PNORDER_NEWTONIAN:*/
 2793            case 0:
 2794                r_sc    = 1.;
 2795        phidot  = 1.;
 2796        rdot_sc = 1.;
 2797                break;
 2798            default:
 2799                XLALPrintError("XLAL Error - %s: Invalid phase PN order %d\n",
 2800                        __func__, ph_O );
 2801                XLAL_ERROR(XLAL_EINVAL);
 2802                break;
 2803        }
 2804 
 2805        /* Dimensionless rdot/c, (r/c)*phidot, Z = G*m/(r*c^2) entering the h+/x coefficients*/
 2806        rdot = CF_rdot * rdot_sc;
 2807    rphidot = CF_rphidot * r_sc * phidot;
 2808        Z = CF_Z/r_sc;
 2809 
 2810        /*
 2811         * First set all h+/x coefficients to 0. Then use a switch to
 2812         * set proper non-zero values up to order ampO. Note we
 2813         * fall through the PN orders and break only after Newt. order
 2814         */
 2815        hp0 = 0.;
 2816        hc0 = 0.;
 2817 
 2818        switch( ampO )
 2819        {
 2820            /* case LAL_PNORDER_THREE_POINT_FIVE: */
 2821            case 7:
 2822                XLALPrintError("XLAL Error - %s: Amp. corrections not known "
 2823                        "to PN order %d\n", __func__, ampO );
 2824                XLAL_ERROR(XLAL_EINVAL);
 2825                break;
 2826            /* case LAL_PNORDER_THREE: */
 2827            case 6:
 2828        XLALPrintError("XLAL Error - %s: Amp. corrections not known "
 2829                        "to PN order %d\n", __func__, ampO );
 2830                XLAL_ERROR(XLAL_EINVAL);
 2831                break;
 2832            /* case LAL_PNORDER_TWO_POINT_FIVE: */
 2833            case 5:
 2834        XLALPrintError("XLAL Error - %s: Amp. corrections not known "
 2835                        "to PN order %d\n", __func__, ampO );
 2836                XLAL_ERROR(XLAL_EINVAL);
 2837                break;
 2838            /* case LAL_PNORDER_TWO: */
 2839            case 4:
 2840        XLALPrintError("XLAL Error - %s: Amp. corrections not known "
 2841                        "to PN order %d\n", __func__, ampO );
 2842                XLAL_ERROR(XLAL_EINVAL);
 2843                break;
 2844            /* case LAL_PNORDER_ONE_POINT_FIVE: */
 2845            case 3:
 2846        XLALPrintError("XLAL Error - %s: Amp. corrections not known "
 2847                        "to PN order %d\n", __func__, ampO );
 2848                XLAL_ERROR(XLAL_EINVAL);
 2849                break;
 2850            /* case LAL_PNORDER_ONE: */
 2851            case 2:
 2852        XLALPrintError("XLAL Error - %s: Amp. corrections not yet implemented "
 2853                        "to PN order %d\n", __func__, ampO );
 2854                XLAL_ERROR(XLAL_EINVAL);
 2855                break;
 2856            /*case LAL_PNORDER_HALF:*/
 2857            case 1:
 2858        XLALPrintError("XLAL Error - %s: Amp. corrections not yet implemented "
 2859                        "to PN order %d\n", __func__, ampO );
 2860                XLAL_ERROR(XLAL_EINVAL);
 2861                break;
 2862        case -1: // Highest known PN order - move if higher terms added!
 2863        /*case LAL_PNORDER_NEWTONIAN:*/
 2864            case 0:
 2865          hp0 = - (si2 * (-pow(rphidot, 2.0) - pow(rdot, 2.0) + Z))
 2866            - (1. + ci2) * ((pow(rphidot, 2.0) - pow(rdot, 2.0) + Z) * cos(2. * phi)
 2867            + (2. * rphidot * rdot) * sin(2. * phi));
 2868          hc0 = - 2. * ci * (-2. * rphidot * rdot * cos(2. * phi)
 2869              + (pow(rphidot, 2.0) - pow(rdot, 2.0) + Z) * sin(2. * phi));
 2870                break;
 2871            default:
 2872                XLALPrintError("XLAL Error - %s: Invalid amp. PN order %d\n",
 2873                        __func__, ampO );
 2874                XLAL_ERROR(XLAL_EINVAL);
 2875                break;
 2876        } /* End switch on ampO */
 2877 
 2878        /* Fill the output polarization arrays */
 2879      (*hplus)->data->data[idx] = ampfac*hp0;
 2880      (*hcross)->data->data[idx] = ampfac*hc0;
 2881 
 2882    } /* end loop over time series samples idx */
 2883    return XLAL_SUCCESS;
 2884}
 2885 
 2886/**
 2887 * Computes polarizations h+ and hx for a spinning, precessing binary
 2888 * when provided time series of all the dynamical quantities.
 2889 * Amplitude can be chosen between 1.5PN and Newtonian orders (inclusive).
 2890 *
 2891 * Based on K.G. Arun, Alesssandra Buonanno, Guillaume Faye and Evan Ochsner
 2892 * \"Higher-order spin effects in the amplitude and phase of gravitational
 2893 * waveforms emitted by inspiraling compact binaries: Ready-to-use
 2894 * gravitational waveforms\", Phys Rev. D 79, 104023 (2009), arXiv:0810.5336
 2895 *
 2896 * HOWEVER, the formulae have been adapted to use the output of the so-called
 2897 * \"Frameless\" convention for evolving precessing binary dynamics,
 2898 * which is not susceptible to hitting coordinate singularities.
 2899 *
 2900 * FIXME: Clean up and commit Mathematica NB Showing correctness. Cite here.
 2901 *
 2902 * NOTE: The vectors MUST be given in the so-called radiation frame where
 2903 * Z is the direction of propagation, X is the principal '+' axis and Y = Z x X
 2904 * For different convention (Z is the direction of initial total angular
 2905 * momentum, useful for GRB and comparison to NR, see XLALSimSpinInspiralGenerator())
 2906 */
 2907int XLALSimInspiralPrecessingPolarizationWaveforms(
 2908    REAL8TimeSeries **hplus,  /**< +-polarization waveform [returned] */
 2909    REAL8TimeSeries **hcross, /**< x-polarization waveform [returned] */
 2910    REAL8TimeSeries *V,       /**< post-Newtonian parameter */
 2911    REAL8TimeSeries *Phi,     /**< orbital phase */
 2912    REAL8TimeSeries *S1x,         /**< Spin1 vector x component */
 2913    REAL8TimeSeries *S1y,         /**< Spin1 vector y component */
 2914    REAL8TimeSeries *S1z,         /**< Spin1 vector z component */
 2915    REAL8TimeSeries *S2x,         /**< Spin2 vector x component */
 2916    REAL8TimeSeries *S2y,         /**< Spin2 vector y component */
 2917    REAL8TimeSeries *S2z,         /**< Spin2 vector z component */
 2918    REAL8TimeSeries *LNhatx,  /**< unit orbital ang. mom. x comp. */
 2919    REAL8TimeSeries *LNhaty,  /**< unit orbital ang. mom. y comp. */
 2920    REAL8TimeSeries *LNhatz,  /**< unit orbital ang. mom. z comp. */
 2921    REAL8TimeSeries *E1x,         /**< orbital plane basis vector x comp. */
 2922    REAL8TimeSeries *E1y,         /**< orbital plane basis vector y comp. */
 2923    REAL8TimeSeries *E1z,         /**< orbital plane basis vector z comp. */
 2924    REAL8 m1,                 /**< mass of companion 1 (kg) */
 2925    REAL8 m2,                 /**< mass of companion 2 (kg) */
 2926    REAL8 r,                  /**< distance of source (m) */
 2927    INT4 ampO             /**< twice amp. post-Newtonian order */
 2928    )
 2929{
 2930    REAL8 s1x, s1y, s1z, s2x, s2y, s2z, lnhx, lnhy, lnhz;
 2931    REAL8 e1x, e1y, e1z, e2x, e2y, e2z, nx, ny, nz, lx, ly, lz;
 2932    REAL8 nx2, ny2, nz2, nz3, lx2, ly2, lz2, lz3;
 2933    REAL8 hplus0, hcross0, hplus05, hcross05, hplus1, hcross1;
 2934    REAL8 hplus15, hcross15, hplusSpin1, hcrossSpin1;
 2935    REAL8 hplusSpin15, hcrossSpin15, hplusTail15, hcrossTail15;
 2936    REAL8 M, eta, dm, phi, v, v2, dist, ampfac;
 2937    INT4 idx, len;
 2938 
 2939    /* Macros to check time series vectors */
 2940    if ( !(hplus) || !(hcross) ) {
 2941      XLALPrintError("** XLALSimInspiralPrecessingPolarizationWaveform error: **h+ and **hx are expected to be non NULL!\n");
 2942      XLAL_ERROR( XLAL_FAILURE );
 2943    }
 2944    LAL_CHECK_VALID_SERIES(V,                   XLAL_FAILURE);
 2945    LAL_CHECK_VALID_SERIES(Phi,                 XLAL_FAILURE);
 2946    LAL_CHECK_VALID_SERIES(S1x,                 XLAL_FAILURE);
 2947    LAL_CHECK_VALID_SERIES(S1y,                 XLAL_FAILURE);
 2948    LAL_CHECK_VALID_SERIES(S1z,                 XLAL_FAILURE);
 2949    LAL_CHECK_VALID_SERIES(S2x,                 XLAL_FAILURE);
 2950    LAL_CHECK_VALID_SERIES(S2y,                 XLAL_FAILURE);
 2951    LAL_CHECK_VALID_SERIES(S2z,                 XLAL_FAILURE);
 2952    LAL_CHECK_VALID_SERIES(LNhatx,              XLAL_FAILURE);
 2953    LAL_CHECK_VALID_SERIES(LNhaty,              XLAL_FAILURE);
 2954    LAL_CHECK_VALID_SERIES(LNhatz,              XLAL_FAILURE);
 2955    LAL_CHECK_VALID_SERIES(E1x,                 XLAL_FAILURE);
 2956    LAL_CHECK_VALID_SERIES(E1y,                 XLAL_FAILURE);
 2957    LAL_CHECK_VALID_SERIES(E1z,                 XLAL_FAILURE);
 2958    LAL_CHECK_CONSISTENT_TIME_SERIES(V, Phi,    XLAL_FAILURE);
 2959    LAL_CHECK_CONSISTENT_TIME_SERIES(V, S1x,    XLAL_FAILURE);
 2960    LAL_CHECK_CONSISTENT_TIME_SERIES(V, S1y,    XLAL_FAILURE);
 2961    LAL_CHECK_CONSISTENT_TIME_SERIES(V, S1z,    XLAL_FAILURE);
 2962    LAL_CHECK_CONSISTENT_TIME_SERIES(V, S2x,    XLAL_FAILURE);
 2963    LAL_CHECK_CONSISTENT_TIME_SERIES(V, S2y,    XLAL_FAILURE);
 2964    LAL_CHECK_CONSISTENT_TIME_SERIES(V, S2z,    XLAL_FAILURE);
 2965    LAL_CHECK_CONSISTENT_TIME_SERIES(V, LNhatx, XLAL_FAILURE);
 2966    LAL_CHECK_CONSISTENT_TIME_SERIES(V, LNhaty, XLAL_FAILURE);
 2967    LAL_CHECK_CONSISTENT_TIME_SERIES(V, LNhatz, XLAL_FAILURE);
 2968    LAL_CHECK_CONSISTENT_TIME_SERIES(V, E1x,    XLAL_FAILURE);
 2969    LAL_CHECK_CONSISTENT_TIME_SERIES(V, E1y,    XLAL_FAILURE);
 2970    LAL_CHECK_CONSISTENT_TIME_SERIES(V, E1z,    XLAL_FAILURE);
 2971 
 2972    /* Allocate polarization vectors and set to 0 */
 2973    *hplus = XLALCreateREAL8TimeSeries( "H_PLUS", &V->epoch,
 2974            0.0, V->deltaT, &lalStrainUnit, V->data->length );
 2975    *hcross = XLALCreateREAL8TimeSeries( "H_CROSS", &V->epoch,
 2976            0.0, V->deltaT, &lalStrainUnit, V->data->length );
 2977    if ( ! hplus || ! hcross )
 2978        XLAL_ERROR(XLAL_EFUNC);
 2979    memset((*hplus)->data->data, 0,
 2980            (*hplus)->data->length*sizeof(*(*hplus)->data->data));
 2981    memset((*hcross)->data->data, 0,
 2982            (*hcross)->data->length*sizeof(*(*hcross)->data->data));
 2983 
 2984    M = m1 + m2;
 2985    eta = m1 * m2 / M / M; // symmetric mass ratio - '\nu' in the paper
 2986    dm = (m1 - m2) / M;    // frac. mass difference - \delta m/m in the paper
 2987    dist = r / LAL_C_SI;   // r (m) / c (m/s) --> dist in units of seconds
 2988    /* convert mass from kg to s, so ampfac ~ M/dist is dimensionless */
 2989    ampfac = 2. * M * LAL_G_SI * pow(LAL_C_SI, -3) * eta / dist;
 2990 
 2991    /* loop over time steps and compute polarizations h+ and hx */
 2992    len = V->data->length;
 2993    for(idx = 0; idx < len; idx++)
 2994    {
 2995        /* Abbreviated names in lower case for time series at this sample */
 2996        phi  = Phi->data->data[idx];    v = V->data->data[idx];     v2 = v * v;
 2997        lnhx = LNhatx->data->data[idx]; e1x = E1x->data->data[idx];
 2998        lnhy = LNhaty->data->data[idx]; e1y = E1y->data->data[idx];
 2999        lnhz = LNhatz->data->data[idx]; e1z = E1z->data->data[idx];
 3000        s1x  = S1x->data->data[idx];    s2x = S2x->data->data[idx];
 3001        s1y  = S1y->data->data[idx];    s2y = S2y->data->data[idx];
 3002        s1z  = S1z->data->data[idx];    s2z = S2z->data->data[idx];
 3003 
 3004        /* E2 = LNhat x E1 */
 3005        e2x = lnhy*e1z - lnhz*e1y;
 3006        e2y = lnhz*e1x - lnhx*e1z;
 3007        e2z = lnhx*e1y - lnhy*e1x;
 3008 
 3009        /* Unit orbital separation vector */
 3010        nx = e1x*cos(phi) + e2x*sin(phi);
 3011        ny = e1y*cos(phi) + e2y*sin(phi);
 3012        nz = e1z*cos(phi) + e2z*sin(phi);
 3013 
 3014        /* Unit inst. orbital velocity vector */
 3015        lx = e2x*cos(phi) - e1x*sin(phi);
 3016        ly = e2y*cos(phi) - e1y*sin(phi);
 3017        lz = e2z*cos(phi) - e1z*sin(phi);
 3018 
 3019        /* Powers of vector components */
 3020        nx2 = nx*nx;    ny2 = ny*ny;    nz2 = nz*nz;    nz3 = nz*nz2;
 3021        lx2 = lx*lx;    ly2 = ly*ly;    lz2 = lz*lz;    lz3 = lz*lz2;
 3022 
 3023        /*
 3024         * First set all h+/x coefficients to 0. Then use a switch to
 3025         * set proper non-zero values up to order ampO. Note we
 3026         * fall through the PN orders and break only after Newt. order
 3027         */
 3028        hplus0 = hplus05 = hplus1 = hplus15 = hplusTail15 = 0.;
 3029        hcross0 = hcross05 = hcross1 = hcross15 = hcrossTail15 = 0.;
 3030        hplusSpin1 = hplusSpin15 = hcrossSpin1 = hcrossSpin15 = 0.;
 3031 
 3032        switch( ampO )
 3033        {
 3034            /*
 3035             * case LAL_PNORDER_THREE_POINT_FIVE:
 3036             * case LAL_PNORDER_THREE:
 3037             * case LAL_PNORDER_TWO_POINT_FIVE:
 3038             * case LAL_PNORDER_TWO:
 3039             */
 3040            case 7:
 3041            case 6:
 3042            case 5:
 3043            case 4:
 3044                XLALPrintError("XLAL Error - %s: Amp. corrections not known "
 3045                        "to PN order %d, highest is %d\n", __func__, ampO,
 3046                        MAX_PRECESSING_AMP_PN_ORDER );
 3047                XLAL_ERROR(XLAL_EINVAL);
 3048                break;
 3049            case -1: /* Use highest known PN order - move if new orders added */
 3050            /*case LAL_PNORDER_ONE_POINT_FIVE:*/
 3051            case 3:
 3052                /* 1.5PN non-spinning amp. corrections */
 3053                hplus15 = (dm*(2*lx*nx*nz*(-95 + 90*lz2 - 65*nz2
 3054                        - 2*eta*(-9 + 90*lz2 - 65*nz2)) - 2*ly*ny*nz
 3055                        * (-95 + 90*lz2 - 65*nz2 - 2*eta*(-9 + 90*lz2 - 65*nz2))
 3056                        + 6*lx2*lz*(13 - 4*lz2 + 29*nz2 + eta*(-2 + 8*lz2
 3057                        - 58*nz2)) - 6*ly2*lz*(13 - 4*lz2 + 29*nz2 + eta
 3058                        * (-2 + 8*lz2 - 58*nz2)) - lz*(nx2 - ny2)*(83 - 6*lz2
 3059                        + 111*nz2 + 6*eta*(-1 + 2*lz2 - 37*nz2))))/24.;
 3060                hcross15 = (dm*(lz*(6*(19 - 4*eta)*lx*ly + (-101 + 12*eta)
 3061                        * nx*ny) + (-149 + 36*eta) * (ly*nx + lx*ny)*nz
 3062                        + 6*(-3 + eta) * (2*lx*ly*lz - lz*nx*ny - 3*ly*nx*nz
 3063                        - 3*lx*ny*nz) + (1 - 2*eta) * (6*lz3*(-4*lx*ly + nx*ny)
 3064                        + 90*lz2*(ly*nx + lx*ny)*nz + 3*lz*(58*lx*ly
 3065                        - 37*nx*ny)*nz2 - 65*(ly*nx + lx*ny)*nz3)))/12.;
 3066                /* 1.5PN spinning amp. corrections */
 3067                hplusSpin15 = (6*lz*ny*s1x + 6*dm*lz*ny*s1x - 3*eta*lz*ny*s1x
 3068                        + 2*ly2*lnhy*s1y + 2*dm*ly2*lnhy*s1y
 3069                        + 2*eta*ly2*lnhy*s1y + 6*lz*nx*s1y + 6*dm*lz*nx*s1y
 3070                        - 3*eta*lz*nx*s1y + 8*lnhy*nx2*s1y + 8*dm*lnhy*nx2*s1y
 3071                        - eta*lnhy*nx2*s1y - 8*lnhy*ny2*s1y - 8*dm*lnhy*ny2*s1y
 3072                        + eta*lnhy*ny2*s1y + 2*ly2*lnhz*s1z + 2*dm*ly2*lnhz*s1z
 3073                        + 2*eta*ly2*lnhz*s1z - 6*ly*nx*s1z - 6*dm*ly*nx*s1z
 3074                        - 9*eta*ly*nx*s1z + 8*lnhz*nx2*s1z + 8*dm*lnhz*nx2*s1z
 3075                        - eta*lnhz*nx2*s1z - 8*lnhz*ny2*s1z - 8*dm*lnhz*ny2*s1z
 3076                        + eta*lnhz*ny2*s1z + 6*lz*ny*s2x - 6*dm*lz*ny*s2x
 3077                        - 3*eta*lz*ny*s2x + lnhx*(2*ly2*((1 + dm + eta)*s1x
 3078                        + (1 - dm + eta)*s2x) + (nx2 - ny2)*((8 + 8*dm - eta)
 3079                        * s1x - (-8 + 8*dm + eta)*s2x)) + 2*ly2*lnhy*s2y
 3080                        - 2*dm*ly2*lnhy*s2y + 2*eta*ly2*lnhy*s2y + 6*lz*nx*s2y
 3081                        - 6*dm*lz*nx*s2y - 3*eta*lz*nx*s2y + 8*lnhy*nx2*s2y
 3082                        - 8*dm*lnhy*nx2*s2y - eta*lnhy*nx2*s2y - 8*lnhy*ny2*s2y
 3083                        + 8*dm*lnhy*ny2*s2y + eta*lnhy*ny2*s2y + 2*ly2*lnhz*s2z
 3084                        - 2*dm*ly2*lnhz*s2z + 2*eta*ly2*lnhz*s2z - 6*ly*nx*s2z
 3085                        + 6*dm*ly*nx*s2z - 9*eta*ly*nx*s2z + 8*lnhz*nx2*s2z
 3086                        - 8*dm*lnhz*nx2*s2z - eta*lnhz*nx2*s2z - 8*lnhz*ny2*s2z
 3087                        + 8*dm*lnhz*ny2*s2z + eta*lnhz*ny2*s2z - 3*lx*ny
 3088                        * ((2 + 2*dm + 3*eta)*s1z + (2 - 2*dm + 3*eta)*s2z)
 3089                        - 2*lx2*(lnhx*((1 + dm + eta)*s1x + (1 - dm + eta)*s2x)
 3090                        + lnhy*((1 + dm + eta)*s1y + (1 - dm + eta)*s2y)
 3091                        + lnhz*((1 + dm + eta)*s1z + (1 - dm + eta)*s2z)))/3.;
 3092                hcrossSpin15 = (-3*lz*(nx*((2 + 2*dm - eta)*s1x
 3093                        - (-2 + 2*dm + eta)*s2x) + ny*((-2 - 2*dm + eta)*s1y
 3094                        + (-2 + 2*dm + eta)*s2y)) + ny*(-6*ly*s1z - 6*dm*ly*s1z
 3095                        - 9*eta*ly*s1z + 16*lnhz*nx*s1z + 16*dm*lnhz*nx*s1z
 3096                        - 2*eta*lnhz*nx*s1z + 2*lnhx*nx*((8 + 8*dm - eta)*s1x
 3097                        - (-8 + 8*dm + eta)*s2x) + 2*lnhy*nx*((8 + 8*dm - eta)
 3098                        * s1y - (-8 + 8*dm + eta)*s2y) - 6*ly*s2z + 6*dm*ly*s2z
 3099                        - 9*eta*ly*s2z + 16*lnhz*nx*s2z - 16*dm*lnhz*nx*s2z
 3100                        - 2*eta*lnhz*nx*s2z) - lx*(4*lnhx*ly*((1 + dm + eta)*s1x
 3101                        + (1 - dm + eta)*s2x) - 3*nx*((2 + 2*dm + 3*eta)*s1z
 3102                        + (2 - 2*dm + 3*eta)*s2z) + 4*ly*(lnhy*((1 + dm + eta)
 3103                        * s1y + (1 - dm + eta)*s2y) + lnhz*((1 + dm + eta)*s1z
 3104                        + (1 - dm + eta)*s2z))))/3.;
 3105                /* 1.5PN tail amp. corrections */
 3106                hplusTail15 = 2*((lx2 - ly2 - nx2 + ny2)*LAL_PI);
 3107                hcrossTail15 = 4*((lx*ly - nx*ny)*LAL_PI);
 3108#if __GNUC__ >= 7 && !defined __INTEL_COMPILER
 3109                __attribute__ ((fallthrough));
 3110#endif
 3111 
 3112            /*case LAL_PNORDER_ONE:*/
 3113            case 2:
 3114                /* 1PN non-spinning amp. corrections */
 3115                hplus1 = (-13*lx2 + 13*ly2 + 6*lx2*lz2 - 6*ly2*lz2
 3116                        + 13*(nx2 - ny2) - 2*lz2*(nx2 - ny2) - 32*lx*lz*nx*nz
 3117                        + 32*ly*lz*ny*nz - 14*lx2*nz2 + 14*ly2*nz2
 3118                        + 10*(nx2 - ny2)*nz2)/6. + (eta*(lx2 - 18*lx2*lz2
 3119                        + 96*lx*lz*nx*nz - 96*ly*lz*ny*nz + 42*lx2*nz2
 3120                        + ly2*(-1 + 18*lz2 - 42*nz2) + (nx2 - ny2)
 3121                        * (-1 + 6*lz2 - 30*nz2)))/6.;
 3122                hcross1 = (eta*(lx*ly - nx*ny - 6*(lz2*(3*lx*ly - nx*ny)
 3123                        - 8*lz*(ly*nx + lx*ny)*nz + (-7*lx*ly
 3124                        + 5*nx*ny)*nz2)))/3. + (-13*(lx*ly - nx*ny)
 3125                        + 2*(lz2*(3*lx*ly - nx*ny) - 8*lz*(ly*nx + lx*ny)*nz
 3126                        + (-7*lx*ly + 5*nx*ny)*nz2))/3.;
 3127                /* 1PN spinning amp. corrections */
 3128                hplusSpin1 = (-(ny*((1 + dm)*s1x + (-1 + dm)*s2x))
 3129                        - nx*((1 + dm)*s1y + (-1 + dm)*s2y))/2.;
 3130                hcrossSpin1 = (nx*((1 + dm)*s1x + (-1 + dm)*s2x)
 3131                        - ny*((1 + dm)*s1y + (-1 + dm)*s2y))/2.;
 3132#if __GNUC__ >= 7 && !defined __INTEL_COMPILER
 3133                __attribute__ ((fallthrough));
 3134#endif
 3135 
 3136            /*case LAL_PNORDER_HALF:*/
 3137            case 1:
 3138                /* 0.5PN non-spinning amp. corrections */
 3139                hplus05 = (dm*(-2*lx2*lz + 2*ly2*lz + lz*(nx2 - ny2)
 3140                        + 6*lx*nx*nz - 6*ly*ny*nz))/2.;
 3141                hcross05 = dm*(-2*lx*ly*lz + lz*nx*ny
 3142                    + 3*ly*nx*nz + 3*lx*ny*nz);
 3143#if __GNUC__ >= 7 && !defined __INTEL_COMPILER
 3144                __attribute__ ((fallthrough));
 3145#endif
 3146            /*case LAL_PNORDER_NEWTONIAN:*/
 3147            case 0:
 3148                /* Newtonian order polarizations */
 3149                hplus0 = lx2 - ly2 - nx2 + ny2;
 3150                hcross0 = 2*lx*ly - 2*nx*ny;
 3151 
 3152                break;
 3153            default:
 3154                XLALPrintError("XLAL Error - %s: Invalid amp. PN order %d\n",
 3155                        __func__, ampO );
 3156                XLAL_ERROR(XLAL_EINVAL);
 3157                break;
 3158        } /* End switch on ampO */
 3159 
 3160        /* Fill the output polarization arrays */
 3161        (*hplus)->data->data[idx] = ampfac * v2 * ( hplus0
 3162                + v * ( hplus05 + v * ( hplus1 + hplusSpin1
 3163                + v * ( hplus15 + hplusSpin15 + hplusTail15 ) ) ) );
 3164        (*hcross)->data->data[idx] = ampfac * v2 * ( hcross0
 3165                + v * ( hcross05 + v * ( hcross1 + hcrossSpin1
 3166                + v * ( hcross15 + hcrossSpin15 + hcrossTail15 ) ) ) );
 3167    } /* end of loop over time samples, idx */
 3168    return XLAL_SUCCESS;
 3169}
 3170 
 3171/**
 3172 * Computes polarizations h+ and hx for a spinning, precessing binary
 3173 * when provided a single value of all the dynamical quantities.
 3174 * Amplitude can be chosen between 1.5PN and Newtonian orders (inclusive).
 3175 *
 3176 * Based on K.G. Arun, Alesssandra Buonanno, Guillaume Faye and Evan Ochsner
 3177 * \"Higher-order spin effects in the amplitude and phase of gravitational
 3178 * waveforms emitted by inspiraling compact binaries: Ready-to-use
 3179 * gravitational waveforms\", Phys Rev. D 79, 104023 (2009), arXiv:0810.5336
 3180 *
 3181 * HOWEVER, the formulae have been adapted to use the output of the so-called
 3182 * \"Frameless\" convention for evolving precessing binary dynamics,
 3183 * which is not susceptible to hitting coordinate singularities.
 3184 *
 3185 * This has been written to reproduce XLALSimInspiralPrecessingPolarizationWaveforms.
 3186 * If hplus and hcross are the output of XLALSimInspiralPrecessingPolarizationWaveforms,
 3187 * and hp(n) and hc(n) the output of this function for a given harmonic number, then
 3188 *
 3189 * hplus = sum_{n=0}^5 hp(n)*exp(-i*n*Phi) + c.c.
 3190 * hcross = sum_{n=0}^5 hc(n)*exp(-i*n*Phi) + c.c.
 3191 *
 3192 * NOTE: The vectors MUST be given in the so-called radiation frame where
 3193 * Z is the direction of propagation, X is the principal '+' axis and Y = Z x X
 3194 * For different convention (Z is the direction of initial total angular
 3195 * momentum, useful for GRB and comparison to NR, see XLALSimSpinInspiralGenerator())
 3196 * FIXME take out v0 as it can be absorbed in a 4PN additional phase term
 3197 * see discussion in sec. VIII of  Class.Quant.Grav. 25 (2008) 165003,
 3198 * arXiv 0802.1249.
 3199 */
 3200int XLALSimInspiralPrecessingPolarizationWaveformHarmonic(
 3201        COMPLEX16 *hplus,  /**< +-polarization waveform [returned] */
 3202        COMPLEX16 *hcross, /**< x-polarization waveform [returned] */
 3203        REAL8 v,       /**< post-Newtonian parameter */
 3204        REAL8 s1x,     /**< Spin1 vector x component */
 3205        REAL8 s1y,     /**< Spin1 vector y component */
 3206        REAL8 s1z,     /**< Spin1 vector z component */
 3207        REAL8 s2x,     /**< Spin2 vector x component */
 3208        REAL8 s2y,     /**< Spin2 vector y component */
 3209        REAL8 s2z,     /**< Spin2 vector z component */
 3210        REAL8 lnhx,  /**< unit orbital ang. mom. x comp. */
 3211        REAL8 lnhy,  /**< unit orbital ang. mom. y comp. */
 3212        REAL8 lnhz,  /**< unit orbital ang. mom. z comp. */
 3213        REAL8 e1x,     /**< orbital plane basis vector x comp. */
 3214        REAL8 e1y,     /**< orbital plane basis vector y comp. */
 3215        REAL8 e1z,     /**< orbital plane basis vector z comp. */
 3216        REAL8 dm,                 /**< dimensionless mass difference (m1 - m2)/(m1 + m2) > 0 */
 3217        REAL8 eta,                /**< symmetric mass ratio m1*m2/(m1 + m2)^2 */
 3218        REAL8 v0,                 /**< tail-term gauge choice (default = 1) */
 3219        INT4 n,                   /**< harmonic number */
 3220        INT4 ampO                 /**< twice amp. post-Newtonian order */
 3221        )
 3222{
 3223  /* E2 = LNhat x E1 */
 3224  REAL8 e2x = lnhy*e1z - lnhz*e1y;
 3225  REAL8 e2y = lnhz*e1x - lnhx*e1z;
 3226  REAL8 e2z = lnhx*e1y - lnhy*e1x;
 3227 
 3228  REAL8 v2 = v*v;
 3229  REAL8 v3 = v2*v;
 3230  REAL8 v4 = v3*v;
 3231  REAL8 v5 = v4*v;
 3232 
 3233  REAL8 twom1 = (1. + dm);
 3234  REAL8 twom2 = (1. - dm);
 3235 
 3236  REAL8 a1x = s1x*twom1;
 3237  REAL8 a1y = s1y*twom1;
 3238  REAL8 a1z = s1z*twom1;
 3239  REAL8 a2x = s2x*twom2;
 3240  REAL8 a2y = s2y*twom2;
 3241  REAL8 a2z = s2z*twom2;
 3242 
 3243  REAL8 logfac;
 3244 
 3245  /*
 3246   * First set all h+/x coefficients to 0. Then use a switch to
 3247   * set proper non-zero values up to order ampO. Note we
 3248   * fall through the PN orders and break only after Newt. order
 3249   */
 3250  *hplus = 0.;
 3251  *hcross = 0.;
 3252 
 3253  REAL8 fact1, fact2, fact3, fact4, fact5, fact6, fact7, fact8, fact9;
 3254 
 3255  REAL8 e1xe1x = e1x*e1x;
 3256  REAL8 e1xe1y = e1x*e1y;
 3257  REAL8 e1xe1z = e1x*e1z;
 3258  REAL8 e1ye1y = e1y*e1y;
 3259  REAL8 e1ye1z = e1y*e1z;
 3260  REAL8 e1ze1z = e1z*e1z;
 3261 
 3262  REAL8 e2xe2x = e2x*e2x;
 3263  REAL8 e2xe2y = e2x*e2y;
 3264  REAL8 e2xe2z = e2x*e2z;
 3265  REAL8 e2ye2y = e2y*e2y;
 3266  REAL8 e2ye2z = e2y*e2z;
 3267  REAL8 e2ze2z = e2z*e2z;
 3268 
 3269  REAL8 e1xe2x = e1x*e2x;
 3270  REAL8 e1xe2y = e1x*e2y;
 3271  REAL8 e1ye2x = e1y*e2x;
 3272  REAL8 e1xe2z = e1x*e2z;
 3273  REAL8 e1ze2x = e1z*e2x;
 3274  REAL8 e1ye2y = e1y*e2y;
 3275  REAL8 e1ye2z = e1y*e2z;
 3276  REAL8 e1ze2y = e1z*e2y;
 3277  REAL8 e1ze2z = e1z*e2z;
 3278 
 3279  switch(n) // harmonic number
 3280  {
 3281    case 0:
 3282      switch( ampO )
 3283      {
 3284        case -1: /* Use highest known PN order - move if new orders added */
 3285        case 3:
 3286        case 2:
 3287        case 1:
 3288          fact1 = v3*0.125;
 3289          fact2 = 7. + dm;
 3290          fact3 = 7. - dm;
 3291          fact4 = a1x*fact2 + a2x*fact3;
 3292          fact5 = a1y*fact2 + a2y*fact3;
 3293          fact6 = lnhx*fact4;
 3294          fact7 = lnhy*fact5;
 3295          fact8 = lnhz*(a1z*fact2 + a2z*fact3);
 3296          fact9 = fact6 + fact7 + fact8;
 3297 
 3298          *hplus += fact1*(fact4*lnhx - fact5*lnhy + fact9*(e1xe1x - e1ye1y
 3299          + e2xe2x - e2ye2y));
 3300          *hcross += fact1*(fact4*lnhy - fact5*lnhx + fact9*(e1xe1y + e2xe2y));
 3301        case 0:
 3302          break;
 3303        default:
 3304          XLALPrintError("XLAL Error - %s: Invalid amp. PN order %d, highest is %d\n", __func__, ampO, 3 );
 3305          break;
 3306      }
 3307      break;
 3308 
 3309    case 1: // harmonic number
 3310      switch( ampO )
 3311      {
 3312        case -1: /* Use highest known PN order - move if new orders added */
 3313        case 3:
 3314          fact1 = 1. - 2.*eta;
 3315          fact2 = 8. + fact1*(30. + 9.*e1ze1z + 19.*e2ze2z);
 3316          fact3 = 72. + fact1*(6. + e2ze2z - 9.*e1ze1z);
 3317          fact4 = 40. + fact1*(18. + 15.*e2ze2z + 5.*e1ze1z);
 3318          fact5 = 8. + fact1*(30. + 9.*e2ze2z + 19.*e1ze1z);
 3319          fact6 = 72. + fact1*(6. + e1ze1z - 9.*e2ze2z);
 3320          fact7 = 40. + fact1*(18. + 15.*e1ze1z + 5.*e2ze2z);
 3321          fact8 = v5*dm/384.;
 3322 
 3323          *hplus += fact8*(((e1xe1x - e1ye1y)*e2z*fact2 - (e2xe2x
 3324          - e2ye2y)*e2z*fact3 + 2.*e1z*(e1ye2y - e1xe2x)*fact4) + I*((-(e2xe2x
 3325          - e2ye2y)*fact5 + (e1xe1x - e1ye1y)*fact6)*e1z - 2.*e2z*(e1ye2y
 3326          - e1xe2x)*fact7));
 3327          *hcross += (2.*fact8)*((-e2xe2y*e2z*fact3 + e1xe2z*e1y*fact2
 3328          - e1z*(e1xe2y + e1ye2x)*fact4) + I*((e1xe2y + e1ye2x)*e2z*fact7
 3329          + (e1xe1y*fact6 - e2xe2y*fact5)*e1z));
 3330#if __GNUC__ >= 7 && !defined __INTEL_COMPILER
 3331          __attribute__ ((fallthrough));
 3332#endif
 3333        case 2:
 3334          fact1 = v4*0.25;
 3335 
 3336          *hplus += fact1*(((a2y - a1y)*e1x - (a1x - a2x)*e1y) + I*((a2y
 3337          - a1y)*e2x - (a1x - a2x)*e2y));
 3338          *hcross += fact1*(((a1x - a2x)*e1x - (a1y - a2y)*e1y) + I*((a1x
 3339          - a2x)*e2x - (a1y - a2y)*e2y));
 3340#if __GNUC__ >= 7 && !defined __INTEL_COMPILER
 3341          __attribute__ ((fallthrough));
 3342#endif
 3343        case 1:
 3344          fact1 = e1xe2x - e1ye2y;
 3345          fact2 = e1ye1y - e1xe1x;
 3346          fact3 = e2xe2x - e2ye2y;
 3347          fact4 = e1xe2y + e1ye2x;
 3348          fact5 = e1xe1y;
 3349          fact6 = e2xe2y;
 3350          fact7 = dm*v3*0.0625;
 3351 
 3352          *hplus += fact7*((6.*e1z*fact1 + e2z*(5.*fact2 + fact3))
 3353          + I*(e1z*(fact2 + 5.*fact3) - 6.*e2z*fact1));
 3354          *hcross += (2.*fact7)*((3.*e1z*fact4 + e2z*(-5.*fact5 + fact6))
 3355          + I*(e1z*(5.*fact6 - fact5) - 3.*e2z*fact4));
 3356#if __GNUC__ >= 7 && !defined __INTEL_COMPILER
 3357          __attribute__ ((fallthrough));
 3358#endif
 3359        case 0:
 3360          break;
 3361        default:
 3362          XLALPrintError("XLAL Error - %s: Invalid amp. PN order %d, highest is %d\n", __func__, ampO, 3 );
 3363          break;
 3364      }
 3365      break;
 3366 
 3367    case 2: // harmonic number
 3368      switch( ampO )
 3369      {
 3370        case -1: /* Use highest known PN order - move if new orders added */
 3371        case 3:
 3372          logfac = log(v/v0);
 3373          fact1 = e1xe2x - e1ye2y;
 3374          fact2 = -e1xe1x + e1ye1y + e2xe2x - e2ye2y;
 3375          fact3 = e1ye2x + e1xe2y;
 3376          fact4 = -e1xe1y + e2xe2y;
 3377 
 3378          *hplus += v5*((12.*fact1*logfac + fact2*LAL_PI) + I*(6.*fact2*logfac
 3379          - 2.*fact1*LAL_PI));
 3380          *hcross += v5*((2.*(6.*fact3*logfac + fact4*LAL_PI))
 3381          + I*(2.*(6.*fact4*logfac - fact3*LAL_PI)));
 3382 
 3383          fact1 = a1x*(7. + dm) + a2x*(7. - dm);
 3384          fact2 = a1y*(7. + dm) + a2y*(7. - dm);
 3385          fact3 = a1z*(11. - 3.*dm) + a2z*(11. + 3.*dm);
 3386          fact4 = a1x*(41. - dm) + a2x*(41. + dm);
 3387          fact5 = a1y*(41. - dm) + a2y*(41. + dm);
 3388          fact6 = a1z*(41. - dm) + a2z*(41. + dm);
 3389          fact7 = lnhx*fact4 + lnhy*fact5 + lnhz*fact6;
 3390          fact8 = e1xe1x - e1ye1y - (e2xe2x - e2ye2y);
 3391          fact9 = v5/48.;
 3392 
 3393          *hplus += fact9*((3.*(e1ye2z + e1ze2y)*fact1 + 3.*(e1xe2z
 3394          + e1ze2x)*fact2 - 6.*(e1ye2x + e1xe2y)*fact3 + fact8*fact7)
 3395          + I*(-3.*(e1ye1z - e2ye2z)*fact1 - 3.*(e1xe1z - e2xe2z)*fact2
 3396          + 6.*(e1xe1y - e2xe2y)*fact3 + 2.*(e1xe2x - e1ye2y)*fact7));
 3397          *hcross += fact9*((-3.*(e1ze2x + e1xe2z)*fact1 + 3.*(e1ze2y
 3398          + e1ye2z)*fact2 + 6.*(e1xe2x - e1ye2y)*fact3 + 2.*(e1xe1y
 3399          - e2xe2y)*fact7) + I*(3.*(e1xe1z - e2xe2z)*fact1 - 3.*(e1ye1z
 3400          - e2ye2z)*fact2 - 3.*fact8*fact3 + 2.*(e1ye2x + e1xe2y)*fact7));
 3401#if __GNUC__ >= 7 && !defined __INTEL_COMPILER
 3402          __attribute__ ((fallthrough));
 3403#endif
 3404 
 3405        case 2:
 3406          fact5 = -1. + 3.*eta;
 3407          fact1 = -13. + eta + (6.*e2ze2z + 2.*e1ze1z)*fact5;
 3408          fact2 = -13. + eta + (6.*e1ze1z + 2.*e2ze2z)*fact5;
 3409          fact3 = e1ze2z*fact5;
 3410          fact4 = -13. + eta + 4.*(e1ze1z + e2ze2z)*fact5;
 3411          fact6 = v4/6.;
 3412 
 3413          *hplus += fact6*((((e1ye1y - e1xe1x)*fact1 + (e2xe2x
 3414          - e2ye2y)*fact2)*0.5) + I*(2.*(e1xe1x - e1ye1y + e2xe2x
 3415          - e2ye2y)*fact3 + (e1ye2y - e1xe2x)*fact4));
 3416          *hcross += fact6*((-e1xe1y*fact1 + e2xe2y*fact2) + I*(4.*(e1xe1y
 3417          + e2xe2y)*fact3 - (e1ye2x + e1xe2y)*fact4));
 3418#if __GNUC__ >= 7 && !defined __INTEL_COMPILER
 3419          __attribute__ ((fallthrough));
 3420#endif
 3421        case 1:
 3422        case 0:
 3423          *hplus += v2*(0.5*(e1ye1y - e2ye2y + e2xe2x - e1xe1x) + I*(e1ye2y
 3424          - e1xe2x));
 3425          *hcross += v2*((e2xe2y - e1xe1y) - I*(e1ye2x + e1xe2y));
 3426          break;
 3427        default:
 3428          XLALPrintError("XLAL Error - %s: Invalid amp. PN order %d, highest is %d\n", __func__, ampO, 3 );
 3429          break;
 3430      }
 3431      break;
 3432 
 3433    case 3: // harmonic number
 3434      switch( ampO )
 3435      {
 3436        case -1: /* Use highest known PN order - move if new orders added */
 3437        case 3:
 3438          fact1 = v5*dm*9./256.;
 3439          fact2 = 1. - 2.*eta;
 3440          fact3 = 48. + fact2*(4. + 33.*e1ze1z + 9.*e2ze2z);
 3441          fact4 = 48. + fact2*(4. + 15.*e1ze1z + 15.*e2ze2z);
 3442          fact5 = 48. + fact2*(4. - 3.*e1ze1z + 21.*e2ze2z);
 3443          fact6 = 48. + fact2*(4. + 33.*e2ze2z + 9.*e1ze1z);
 3444          fact7 = 48. + fact2*(4. - 3.*e2ze2z + 21.*e1ze1z);
 3445 
 3446          *hplus += fact1*(((e2xe2x - e2ye2y)*e2z*fact3 + 2.*e1z*(e1ye2y
 3447          - e1xe2x)*fact4 - (e1xe1x - e1ye1y)*e2z*fact5) + I*(2.*(e1ye2y
 3448          - e1xe2x)*e2z*fact4 + (e1xe1x - e1ye1y)*e1z*fact6 - e1z*(e2xe2x
 3449          - e2ye2y)*fact7));
 3450          *hcross += fact1*((2.*(e2xe2y*e2z*fact3 - (e1xe2y + e1ye2x)*e1z*fact4
 3451          - e1xe1y*e2z*fact5)) + I*(2.*(-e1z*e2xe2y*fact7 + e1xe1y*e1z*fact6
 3452          - (e1xe2y + e1ye2x)*e2z*fact4)));
 3453#if __GNUC__ >= 7 && !defined __INTEL_COMPILER
 3454          __attribute__ ((fallthrough));
 3455#endif
 3456        case 2:
 3457        case 1:
 3458          fact1 = v3*dm*9./16.;
 3459          fact2 = 2.*(e1xe2x - e1ye2y);
 3460          fact3 = e1xe1x - e1ye1y - (e2xe2x - e2ye2y);
 3461          fact4 = 2.*(e1xe2y + e1ye2x);
 3462          fact5 = 2.*(e1xe1y - e2xe2y);
 3463 
 3464          *hplus += fact1*((e1z*fact2 + e2z*fact3) - I*(e1z*fact3 - e2z*fact2));
 3465          *hcross += fact1*((e1z*fact4 + e2z*fact5) + I*(-e1z*fact5
 3466          + e2z*fact4));
 3467#if __GNUC__ >= 7 && !defined __INTEL_COMPILER
 3468          __attribute__ ((fallthrough));
 3469#endif
 3470        case 0:
 3471          break;
 3472        default:
 3473          XLALPrintError("XLAL Error - %s: Invalid amp. PN order %d, highest is %d\n", __func__, ampO, 3 );
 3474          break;
 3475      }
 3476      break;
 3477 
 3478    case 4: // harmonic number
 3479      switch( ampO )
 3480      {
 3481        case -1: /* Use highest known PN order - move if new orders added */
 3482        case 3:
 3483        case 2:
 3484          fact1 = v4*4.*(1. - 3.*eta)/3.;
 3485          fact2 = e1xe2x - e1ye2y;
 3486          fact3 = e1xe1x - e1ye1y - (e2xe2x - e2ye2y);
 3487          fact4 = e1ze1z - e2ze2z;
 3488          fact5 = e1xe1y - e2xe2y;
 3489          fact6 = e1ye2x + e1xe2y;
 3490 
 3491          *hplus = fact1*((0.5*fact4*fact3 - 2.*e1ze2z*fact2) + I*(fact4*fact2
 3492          + e1ze2z*fact3));
 3493          *hcross = fact1*((fact4*fact5 - 2.*e1ze2z*fact6) + I*(fact4*fact6
 3494          + 2.*e1ze2z*fact5));
 3495#if __GNUC__ >= 7 && !defined __INTEL_COMPILER
 3496          __attribute__ ((fallthrough));
 3497#endif
 3498        case 1:
 3499        case 0:
 3500          break;
 3501        default:
 3502          XLALPrintError("XLAL Error - %s: Invalid amp. PN order %d, highest is %d\n", __func__, ampO, 3 );
 3503          break;
 3504      }
 3505      break;
 3506 
 3507    case 5: // harmonic number
 3508      switch( ampO )
 3509      {
 3510        case -1: /* Use highest known PN order - move if new orders added */
 3511        case 3:
 3512          fact1 = -v5*dm*(1. - 2.*eta)*625./384.;
 3513          fact2 = e1xe2x - e1ye2y;
 3514          fact3 = e1xe1x - e1ye1y - (e2xe2x - e2ye2y);
 3515          fact4 = e1z*(e1ze1z - 3.*e2ze2z);
 3516          fact5 = e2z*(e2ze2z - 3.*e1ze1z);
 3517          fact6 = e1ye2x + e1xe2y;
 3518          fact7 = e1xe1y - e2xe2y;
 3519 
 3520          *hplus += (fact1)*((fact4*fact2 - 0.5*fact5*fact3) - I*(fact5*fact2
 3521          + 0.5*fact4*fact3));
 3522          *hcross += (fact1)*((fact4*fact6 - fact5*fact7) - I*(fact4*fact7
 3523          + fact5*fact6));
 3524#if __GNUC__ >= 7 && !defined __INTEL_COMPILER
 3525          __attribute__ ((fallthrough));
 3526#endif
 3527        case 2:
 3528        case 1:
 3529        case 0:
 3530          break;
 3531        default:
 3532          XLALPrintError("XLAL Error - %s: Invalid amp. PN order %d, highest is %d\n", __func__, ampO, 3 );
 3533          break;
 3534      }
 3535      break;
 3536 
 3537    default: // harmonic number. zero at this order
 3538      break;
 3539  }
 3540  return XLAL_SUCCESS;
 3541}
 3542 
 3543/** @} */
 3544 
 3545/**
 3546 * @defgroup lalsimulation_inference LALSimulation-LALInference parameter transformations
 3547 * @author Riccardo Sturani
 3548 *
 3549 * @brief Functions to transform waveform parameters between LALSimulation and LALInference coordinate conventions
 3550 */
 3551 
 3552/**
 3553 * @ingroup lalsimulation_inference
 3554 * @brief Transform Precessing Parameters
 3555 *
 3556 * @details Routine for transforming LALInference geometric variables to ChooseWaveform input
 3557 *
 3558 * Function to specify the desired orientation of a precessing binary in terms
 3559 * of several angles and then compute the vector components with respect to
 3560 * orbital angular momentum as needed to specify binary configuration for
 3561 * ChooseTDWaveform.
 3562 *
 3563 * @image html lalsiminspiral_orbitelementsJ.svg Representation of input variables.
 3564 *
 3565 * ### Input:
 3566 * * thetaJN is the inclination between total angular momentum (J) and the
 3567 *   direction of propagation (N=(0,sin(thetaJN),cos(thetaJN)))
 3568 *   @note This choice has been made to made so that thetaJN -> inclination
 3569 *   for \f$ S_{1}+S_{2} \to 0\f$.
 3570 * * theta1 and theta2 are the inclinations of \f$S_{1,2}\f$
 3571 *   measured from the Newtonian orbital angular momentum (\f$L_{N}\f$).
 3572 * * phi12 is the difference in azimuthal angles of \f$S_{1,2}\f$.
 3573 * * chi1, chi2 are the dimensionless spin magnitudes ( chi1, chi2 \f$\le 1\f$)
 3574 * * phiJL is the azimuthal angle of \f$L_{N}\f$ on its cone about J.
 3575 * * m1, m2, f_ref, phiref are the component masses and reference GW frequency
 3576     and orbital phase, they are needed to compute the magnitude of
 3577     \f$L_{N}\f$, and thus J.
 3578 *
 3579 * ### Output:
 3580 * incl - inclination angle of N relative to L_N (N=(0,sin(incl),cos(incl)))
 3581 * in the p-q-Z frame.
 3582 * x, y, z components \f$S_{1,2}\f$ (unit spin vectors times their
 3583 * dimensionless spin magnitudes - i.e. they have unit magnitude for
 3584 * extremal BHs and smaller magnitude for slower spins).
 3585 * where x-y are rotated by phiRef with respect to p-q,
 3586 * i.e. is \f$S_{1}\f$ wrt to x-y is (a,b,0), wrt to p-q will be
 3587 * (a cos(phiRef) + b sin (phiRef), )
 3588 * @note Here the \"total\" angular momentum is computed as
 3589 * J = \f$L_{N}(1+l_{1PN}) + S_{1} + S_{2}\f$
 3590 * where \f$L_N\f$ is the Newtonian orbital angular momentum and \f$l_{1PN}\f$
 3591 * its relative 1PN corrections. In fact, there are
 3592 * PN corrections to L which contribute to J that are NOT ACCOUNTED FOR
 3593 * in this function. This is done so to avoid complications with spin-orbit
 3594 * contributions to L, which would require the full knowledge fo the orbital
 3595 * motion, not just the evolution of L (see e.g. eq.2.9c of
 3596 * arXiv:gr-qc/9506022). Also, it is believed that the difference in Jhat
 3597 * with or without these PN corrections to L is quite small.
 3598 *
 3599 * @attention fRef = 0 is not a valid choice. If you will pass fRef=0 into
 3600 * ChooseWaveform, then here pass in f_min, the starting GW frequency
 3601 *
 3602 * UNREVIEWED
 3603 */
 3604 
 3605int XLALSimInspiralTransformPrecessingNewInitialConditions(
 3606        REAL8 *incl,    /**< Inclination angle of L_N (returned) */
 3607        REAL8 *S1x,     /**< S1 x component (returned) */
 3608        REAL8 *S1y,     /**< S1 y component (returned) */
 3609        REAL8 *S1z,     /**< S1 z component (returned) */
 3610        REAL8 *S2x,     /**< S2 x component (returned) */
 3611        REAL8 *S2y,     /**< S2 y component (returned) */
 3612        REAL8 *S2z,     /**< S2 z component (returned) */
 3613        const REAL8 thetaJN,    /**< zenith angle between J and N (rad) */
 3614        const REAL8 phiJL,      /**< azimuthal angle of L_N on its cone about J (rad) */
 3615        const REAL8 theta1,     /**< zenith angle between S1 and LNhat (rad) */
 3616        const REAL8 theta2,     /**< zenith angle between S2 and LNhat (rad) */
 3617        const REAL8 phi12,      /**< difference in azimuthal angle btwn S1, S2 (rad) */
 3618        const REAL8 chi1,       /**< dimensionless spin of body 1 */
 3619        const REAL8 chi2,       /**< dimensionless spin of body 2 */
 3620        const REAL8 m1_SI,      /**< mass of body 1 (kg) */
 3621        const REAL8 m2_SI,      /**< mass of body 2 (kg) */
 3622        const REAL8 fRef,       /**< reference GW frequency (Hz) */
 3623        const REAL8 phiRef      /**< reference orbital phase */
 3624        )
 3625{
 3626    /* Check that fRef is sane */
 3627    if( fRef == 0. )
 3628    {
 3629        XLALPrintError("XLAL Error - %s: fRef=0 is invalid. Please pass in the starting GW frequency instead.\n", __func__);
 3630        XLAL_ERROR(XLAL_EINVAL);
 3631    }
 3632    if( (chi1<0.) || (chi1>1.) || (chi2<0.) || (chi2>1.) )
 3633    {
 3634      XLALPrintError("XLAL Error - %s: chi1,2=0  must be between 0 and 1, values %8.4f -- %8.4f passed.\n", __func__,chi1,chi2);
 3635        XLAL_ERROR(XLAL_EINVAL);
 3636    }
 3637 
 3638    REAL8 m1, m2, eta, v0, theta0, phi0, Jnorm, tmp1, tmp2;
 3639    REAL8 Jhatx, Jhaty, Jhatz, LNhx, LNhy, LNhz, Jx, Jy, Jz, Lmag;
 3640    REAL8 s1hatx,s1haty,s1hatz,s2hatx,s2haty,s2hatz;
 3641    REAL8 s1x, s1y, s1z, s2x, s2y, s2z;
 3642 
 3643    /* Starting frame: LNhat is along the z-axis and the unit
 3644     * spin vectors are defined from the angles relative to LNhat.
 3645     * Note that we put s1hat in the x-z plane, and phi12
 3646     * sets the azimuthal angle of s2hat measured from the x-axis.
 3647     */
 3648    LNhx = 0.;
 3649    LNhy = 0.;
 3650    LNhz = 1.;
 3651    /* Spins are given wrt to L,
 3652         * but still we cannot fill the spin as we do not know
 3653     * what will be the relative orientation of L and N.
 3654         * Note that these spin components are NOT wrt to binary
 3655     * separation vector, but wrt to binary separation vector
 3656     * at phiref=0.
 3657     */
 3658    s1hatx = sin(theta1)*cos(phiRef);
 3659    s1haty = sin(theta1)*sin(phiRef);
 3660    s1hatz = cos(theta1);
 3661    s2hatx = sin(theta2) * cos(phi12+phiRef);
 3662    s2haty = sin(theta2) * sin(phi12+phiRef);
 3663    s2hatz = cos(theta2);
 3664 
 3665    /* Define several internal variables needed for magnitudes */
 3666    m1 = m1_SI/LAL_MSUN_SI;
 3667    m2 = m2_SI/LAL_MSUN_SI;
 3668    eta=m1*m2/(m1+m2)/(m1+m2);
 3669    // v parameter at reference point
 3670    v0 = cbrt( (m1+m2) * LAL_MTSUN_SI *LAL_PI * fRef );
 3671 
 3672    /* Define S1, S2, J with proper magnitudes */
 3673    Lmag = XLALSimInspiralLN(m1+m2,eta,v0)*(1.+v0*v0*XLALSimInspiralL_2PN(eta));
 3674    s1x = m1 * m1 * chi1 * s1hatx;
 3675    s1y = m1 * m1 * chi1 * s1haty;
 3676    s1z = m1 * m1 * chi1 * s1hatz;
 3677    s2x = m2 * m2 * chi2 * s2hatx;
 3678    s2y = m2 * m2 * chi2 * s2haty;
 3679    s2z = m2 * m2 * chi2 * s2hatz;
 3680    Jx = s1x + s2x;
 3681    Jy = s1y + s2y;
 3682    Jz = Lmag + s1z + s2z;
 3683 
 3684    /* Normalize J to Jhat, find its angles in starting frame */
 3685    Jnorm = sqrt( Jx*Jx + Jy*Jy + Jz*Jz);
 3686    Jhatx = Jx / Jnorm;
 3687    Jhaty = Jy / Jnorm;
 3688    Jhatz = Jz / Jnorm;
 3689    theta0 = acos(Jhatz);
 3690    phi0 = atan2(Jhaty, Jhatx);
 3691 
 3692    /* Rotation 1: Rotate about z-axis by -phi0 to put Jhat in x-z plane */
 3693    ROTATEZ(-phi0, s1hatx, s1haty, s1hatz);
 3694    ROTATEZ(-phi0, s2hatx, s2haty, s2hatz);
 3695    //do not need to perform explicitly the rotation on L and J
 3696    //ROTATEZ(-phi0, Jhatx, Jhaty, Jhatz);
 3697    //ROTATEZ(-phi0, LNhx, LNhy, LNhz);
 3698 
 3699    /* Rotation 2: Rotate about new y-axis by -theta0
 3700     * to put Jhat along z-axis
 3701     */
 3702    ROTATEY(-theta0, LNhx, LNhy, LNhz);
 3703    ROTATEY(-theta0, s1hatx, s1haty, s1hatz);
 3704    ROTATEY(-theta0, s2hatx, s2haty, s2hatz);
 3705    //do not need to perform explicitly the rotation on J
 3706    //ROTATEY(-theta0, Jhatx, Jhaty, Jhatz);
 3707 
 3708    /* Rotation 3: Rotate about new z-axis by phiJL to put L at desired
 3709     * azimuth about J. Note that is currently in x-z plane towards -x
 3710     * (i.e. azimuth=pi). Hence we rotate about z by phiJL - LAL_PI
 3711     */
 3712    ROTATEZ(phiJL - LAL_PI, LNhx, LNhy, LNhz);
 3713    ROTATEZ(phiJL - LAL_PI, s1hatx, s1haty, s1hatz);
 3714    ROTATEZ(phiJL - LAL_PI, s2hatx, s2haty, s2hatz);
 3715    //do not need to perform explicitly the rotation on J
 3716    //ROTATEZ(phiJL - LAL_PI, Jhatx, Jhaty, Jhatz);
 3717 
 3718    /* The cosinus of the angle between L and N is the scalar
 3719         * product of the two vectors.
 3720         * We do not need to perform additional rotation to compute it.
 3721         */
 3722    REAL8 Nx=0.;
 3723    REAL8 Ny=sin(thetaJN);
 3724    REAL8 Nz=cos(thetaJN);
 3725    *incl=acos(Nx*LNhx+Ny*LNhy+Nz*LNhz); //output
 3726 
 3727    /* Rotation 4-5: Now J is along z and N in y-z plane, inclined from J
 3728         * by thetaJN and with >ve component along y.
 3729         * Now we bring L into the z axis to get spin components.
 3730     */
 3731    REAL8 thetaLJ = acos(LNhz);
 3732    REAL8 phiL    = atan2(LNhy, LNhx);
 3733 
 3734    ROTATEZ(-phiL, s1hatx, s1haty, s1hatz);
 3735    ROTATEZ(-phiL, s2hatx, s2haty, s2hatz);
 3736    ROTATEZ(-phiL, Nx, Ny, Nz);
 3737    // do not need to perform explicitly the rotations on L and J
 3738    //ROTATEZ(-phiL, LNhx, LNhy, LNhz);
 3739    //ROTATEZ(-phiL, Jhatx, Jhaty, Jhatz);
 3740 
 3741    ROTATEY(-thetaLJ, s1hatx, s1haty, s1hatz);
 3742    ROTATEY(-thetaLJ, s2hatx, s2haty, s2hatz);
 3743    ROTATEY(-thetaLJ, Nx, Ny, Nz);
 3744    // do not need to perform explicitly the rotations on L and J
 3745    //ROTATEY(-thetaLJ, LNhx, LNhy, LNhz);
 3746    //ROTATEY(-thetaLJ, Jhatx, Jhaty, Jhatz);
 3747 
 3748    /* Rotation 6: Now L is along z and we have to bring N
 3749     * in the y-z plane with >ve y components.
 3750     */
 3751    REAL8 phiN = atan2(Ny, Nx);
 3752    //Note the extra -phiRef here:
 3753        // output spins must be given wrt to two body separations
 3754        // which are rigidly rotated with spins
 3755    ROTATEZ(LAL_PI/2.-phiN-phiRef, s1hatx, s1haty, s1hatz);
 3756    ROTATEZ(LAL_PI/2.-phiN-phiRef, s2hatx, s2haty, s2hatz);
 3757    // do not need to perform explicitly the rotations on L, J and N
 3758    //ROTATEZ(LAL_PI/2.-phiN, LNhx, LNhy, LNhz);
 3759    //ROTATEZ(LAL_PI/2.-phiN, Nx, Ny, LNz);
 3760    //ROTATEZ(LAL_PI/2.-phiN, Jhatx, Jhaty, Jhatz);
 3761 
 3762    /* Set pointers to rotated spin vectors */
 3763    *S1x = s1hatx*chi1;
 3764    *S1y = s1haty*chi1;
 3765    *S1z = s1hatz*chi1;
 3766    *S2x = s2hatx*chi2;
 3767    *S2y = s2haty*chi2;
 3768    *S2z = s2hatz*chi2;
 3769 
 3770    //Uncomment the following lines for a check of the rotation
 3771    /*printf("*****************************************\n");
 3772    printf("** Check of TransformPrec...Conditions **\n");
 3773    printf("*****************************************\n");
 3774    //Rot 1:
 3775    ROTATEZ(-phi0, Jhatx, Jhaty, Jhatz);
 3776    //Rot 2:
 3777    ROTATEY(-theta0, Jhatx, Jhaty, Jhatz);
 3778    //Rot 3:
 3779    ROTATEZ(phiJL - LAL_PI, Jhatx, Jhaty, Jhatz);
 3780    //Rot 4:
 3781    ROTATEZ(-phiL, Nx, Ny, Nz);
 3782    ROTATEZ(-phiL, LNhx, LNhy, LNhz);
 3783    ROTATEZ(-phiL, Jhatx, Jhaty, Jhatz);
 3784    //Rot 5:
 3785    ROTATEY(-thetaLJ, Nx, Ny, Nz);
 3786    ROTATEY(-thetaLJ, LNhx, LNhy, LNhz);
 3787    ROTATEY(-thetaLJ, Jhatx, Jhaty, Jhatz);
 3788    //Rot 6:
 3789    ROTATEZ(LAL_PI/2.-phiN, Nx, Ny, Nz);
 3790    ROTATEZ(LAL_PI/2.-phiN, LNhx, LNhy, LNhz);
 3791    ROTATEZ(LAL_PI/2.-phiN, Jhatx, Jhaty, Jhatz);
 3792    printf("LNhat: %12.4e  %12.4e  %12.4e\n",LNhx,LNhy,LNhz);
 3793    printf("       %12.4e  %12.4e  %12.4e\n",0.,0.,1.);
 3794    printf("N:     %12.4e  %12.4e  %12.4e\n",Nx,Ny,Nz);
 3795    printf("       %12.4e  %12.4e  %12.4e\n",0.,sin(*incl),cos(*incl));
 3796    printf("J.Lhat  i: %12.4e f: %12.4e\n",Jz,Jnorm*Jhatz);
 3797    printf("S1.L    i: %12.4e f: %12.4e\n",chi1*cos(theta1),*S1z);
 3798    printf("S2.L    i: %12.4e f: %12.4e\n",chi2*cos(theta2),*S2z);
 3799    printf("S1.S2   i: %12.4e f: %12.4e\n",chi1*chi2*(sin(theta1)*sin(theta2)*cos(phi12)+cos(theta1)*cos(theta2)),(*S1x)*(*S2x)+(*S1y)*(*S2y)+(*S1z)*(*S2z));
 3800    printf("S1.J i: %12.4e f: %12.4e\n",chi1*(sin(theta1)*Jx+cos(theta1)*Jz),Jnorm*((*S1x)*Jhatx+(*S1y)*Jhaty+(*S1z)*Jhatz));
 3801    printf("S2.J i: %12.4e f: %12.4e\n",chi2*(sin(theta2)*(cos(phi12)*Jx+sin(phi12)*Jy)+cos(theta2)*Jz),Jnorm*((*S2x)*Jhatx+(*S2y)*Jhaty+(*S2z)*Jhatz));
 3802    printf("Jhat.Nhat i: %12.4e f: %12.4e\n",cos(thetaJN),Jhatx*Nx+Jhaty*Ny+Jhatz*Nz);
 3803    printf("Norm Jhat: %12.4e  norm N: %12.4e\n",Jhatx*Jhatx+Jhaty*Jhaty+Jhatz*Jhatz,Nx*Nx+Ny*Ny+Nz*Nz);
 3804    printf("*****************************************\n");*/
 3805    return XLAL_SUCCESS;
 3806}
 3807 
 3808/**
 3809 * @ingroup lalsimulation_inference
 3810 * @brief inverse to XLALSimInspiralTransformPrecessingNewInitialConditions()
 3811 *
 3812 * @details This function performs inverse transformation to
 3813 * XLALSimInspiralTransformPrecessingNewInitialConditions()
 3814 * it takes as input waveform parameters, assume to be defined in the
 3815 * L=z, n=x (L-robital momentum at fRef, n is orbital separation at fRef.
 3816 * Direction of propagation (direction to the observer) N is defined by spherical angles
 3817 * (pi/2-phiRef, inclination).
 3818 * The return parameters are what is used in PE for sampling (see description in ....)
 3819 * Note that the masses are in *solar mass* and |L| is computed to the same order as in the
 3820 * direct function above. Spins are dimensionless.
 3821 */
 3822 
 3823/** @{ */
 3824 
 3825int XLALSimInspiralTransformPrecessingWvf2PE(
 3826    REAL8 *thetaJN,     /**< zenith angle between J and N (rad) [return]*/
 3827        REAL8 *phiJL,   /**< azimuthal angle of L_N on its cone about J (rad) [return] */
 3828        REAL8 *theta1,          /**< zenith angle between S1 and LNhat (rad) [return] */
 3829        REAL8 *theta2,          /**< zenith angle between S2 and LNhat (rad) [return] */
 3830        REAL8 *phi12,   /**< difference in azimuthal angle btwn S1, S2 (rad) [return] */
 3831        REAL8 *chi1,    /**< dimensionless spin of body 1 */
 3832        REAL8 *chi2,    /**< dimensionless spin of body 2 */
 3833        const REAL8 incl,       /**< Inclination angle of L_N (returned) */
 3834        const REAL8 S1x,        /**< S1 x component (input) */
 3835        const REAL8 S1y,        /**< S1 y component (input) */
 3836        const REAL8 S1z,        /**< S1 z component (input) */
 3837        const REAL8 S2x,        /**< S2 x component (input) */
 3838        const REAL8 S2y,        /**< S2 y component (input) */
 3839        const REAL8 S2z,        /**< S2 z component (input) */
 3840        const REAL8 m1,         /**< mass of body 1 (solar mass) */
 3841        const REAL8 m2,         /**< mass of body 2 (solar mass) */
 3842        const REAL8 fRef,       /**< reference GW frequency (Hz) */
 3843        const REAL8 phiRef      /**< reference orbital phase */
 3844        )
 3845{
 3846   /* Check that fRef is sane */
 3847    if( fRef == 0. )
 3848    {
 3849        XLALPrintError("XLAL Error - %s: fRef=0 is invalid. Please pass in the starting GW frequency instead.\n", __func__);
 3850        XLAL_ERROR(XLAL_EINVAL);
 3851    }
 3852 
 3853    REAL8 eta, v0, Jnorm, tmp1, tmp2; // theta0, phi0, Jnorm, tmp1, tmp2;
 3854    REAL8 Jhatx, Jhaty, Jhatz, LNhx, LNhy, LNhz, Jx, Jy, Jz, Lmag;
 3855    REAL8 s1hatx,s1haty,s1hatz,s2hatx,s2haty,s2hatz;
 3856    REAL8 phi1, phi2, thetaJL, phiJ;
 3857    REAL8 s1x, s1y, s1z, s2x, s2y, s2z;
 3858    REAL8 Nx, Ny, Nz, phiO, phiN;
 3859 
 3860    /* Starting frame: LNhat is along the z-axis and the unit
 3861     * spin vectors are defined from the angles relative to LNhat.
 3862     */
 3863 
 3864    LNhx = 0.;
 3865    LNhy = 0.;
 3866    LNhz = 1.;
 3867    *chi1 = sqrt(S1x*S1x + S1y*S1y + S1z*S1z);
 3868    *chi2 = sqrt(S2x*S2x + S2y*S2y + S2z*S2z);
 3869    if ((*chi1) > 0.0){
 3870        s1hatx = S1x/(*chi1);
 3871        s1haty = S1y/(*chi1);
 3872        s1hatz = S1z/(*chi1);
 3873    }else{
 3874        s1hatx = 0.0;
 3875        s1haty = 0.0;
 3876        s1hatz = 0.0;
 3877    }
 3878 
 3879    if ((*chi2) > 0.0){
 3880        s2hatx = S2x/(*chi2);
 3881        s2haty = S2y/(*chi2);
 3882        s2hatz = S2z/(*chi2);
 3883    }else{
 3884        s2hatx = 0.0;
 3885        s2haty = 0.0;
 3886        s2hatz = 0.0;
 3887    }
 3888 
 3889    phi1 = atan2(s1haty, s1hatx);
 3890    phi2 = atan2(s2haty, s2hatx);
 3891 
 3892    *phi12 = phi2 - phi1;
 3893    if (*phi12 < 0.0){
 3894        *phi12 += 2.0*LAL_PI;
 3895    }
 3896    *theta1 = acos(s1hatz);
 3897    *theta2 = acos(s2hatz);
 3898 
 3899    eta=m1*m2/(m1+m2)/(m1+m2);
 3900    // v parameter at reference point
 3901    v0 = cbrt( (m1+m2) * LAL_MTSUN_SI *LAL_PI * fRef );
 3902 
 3903    /* Define S1, S2, J with proper magnitudes */
 3904    Lmag = XLALSimInspiralLN(m1+m2,eta,v0)*(1.0 + v0*v0*XLALSimInspiralL_2PN(eta));
 3905    s1x = m1 * m1 * S1x;
 3906    s1y = m1 * m1 * S1y;
 3907    s1z = m1 * m1 * S1z;
 3908    s2x = m2 * m2 * S2x;
 3909    s2y = m2 * m2 * S2y;
 3910    s2z = m2 * m2 * S2z;
 3911    Jx = s1x + s2x;
 3912    Jy = s1y + s2y;
 3913    Jz = Lmag * LNhz + s1z + s2z;
 3914 
 3915    /* Normalize J to Jhat, find its angles in starting frame */
 3916    Jnorm = sqrt( Jx*Jx + Jy*Jy + Jz*Jz);
 3917    Jhatx = Jx / Jnorm;
 3918    Jhaty = Jy / Jnorm;
 3919    Jhatz = Jz / Jnorm;
 3920 
 3921    thetaJL = acos(Jhatz);
 3922    phiJ = atan2(Jhaty, Jhatx);
 3923 
 3924    phiO = 0.5*LAL_PI - phiRef;
 3925    Nx = sin(incl)*cos(phiO);
 3926    Ny = sin(incl)*sin(phiO);
 3927    Nz = cos(incl);
 3928 
 3929    *thetaJN = acos(Jhatx*Nx + Jhaty*Ny + Jhatz*Nz);
 3930 
 3931    /* The easiest way to define the phiJL is to rotate to the frame
 3932     * where J is along z and N is in the y-z plane */
 3933    ROTATEZ(-phiJ, Nx, Ny, Nz);
 3934    ROTATEY(-thetaJL, Nx, Ny, Nz);
 3935 
 3936    ROTATEZ(-phiJ, LNhx, LNhy, LNhz);
 3937    ROTATEY(-thetaJL, LNhx, LNhy, LNhz);
 3938    /* You can check the rotation by uncommenting the lines below*/
 3939    /*ROTATEZ(-phiJ, Jhatx, Jhaty, Jhatz);
 3940    ROTATEY(-thetaJL, Jhatx, Jhaty, Jhatz);*/
 3941 
 3942    phiN = atan2(Ny, Nx);
 3943    /* N in J-frame should be in y-z plane
 3944     * After rotation defined below N should be in y-z plane inclined by thetaJN to J=z*/
 3945    /*ROTATEZ(0.5*LAL_PI - phiN, Nx, Ny, Nz);*/
 3946    ROTATEZ(0.5*LAL_PI - phiN, LNhx, LNhy, LNhz);
 3947 
 3948    *phiJL = atan2(LNhy, LNhx);
 3949 
 3950    if (*phiJL < 0.0){
 3951        *phiJL += 2.0*LAL_PI;
 3952    }
 3953 
 3954    /* That's all folks */
 3955    return XLAL_SUCCESS;
 3956 
 3957}
 3958 
 3959/** @} */
 3960 
 3961/**
 3962 * @name Routines for Handling Approximants, Order, Axis, Mode Information
 3963 * @{
 3964 */
 3965 
 3966/**
 3967 * Checks whether the given approximant is implemented in lalsimulation's XLALSimInspiralChooseTDWaveform().
 3968 *
 3969 * returns 1 if the approximant is implemented, 0 otherwise.
 3970 */
 3971int XLALSimInspiralImplementedTDApproximants(
 3972    Approximant approximant /**< post-Newtonian approximant for use in waveform production */
 3973    )
 3974{
 3975    switch (approximant)
 3976    {
 3977        case TaylorEt:
 3978        case TaylorT1:
 3979        case TaylorT2:
 3980        case TaylorT3:
 3981        case TaylorT4:
 3982            case EccentricTD:
 3983        case EOBNRv2:
 3984        case HGimri:
 3985        case IMRPhenomA:
 3986        case EOBNRv2HM:
 3987        case SpinTaylorT5:
 3988        case SpinTaylorT4:
 3989        case SpinTaylorT1:
 3990        case IMRPhenomB:
 3991        case PhenSpinTaylor:
 3992        case IMRPhenomC:
 3993        case IMRPhenomD:
 3994        case IMRPhenomHM:
 3995        case IMRPhenomPv2:
 3996        case IMRPhenomPv3:
 3997        case IMRPhenomPv3HM:
 3998        case IMRPhenomPv2_NRTidal:
 3999        case IMRPhenomPv2_NRTidalv2:
 4000        case IMRPhenomNSBH:
 4001        case IMRPhenomD_NRTidalv2:
 4002                case IMRPhenomXAS:
 4003        case IMRPhenomXAS_NRTidalv2:
 4004        case IMRPhenomXAS_NRTidalv3:
 4005                case IMRPhenomXHM:
 4006                case IMRPhenomXP:
 4007        case IMRPhenomXP_NRTidalv2:
 4008        case IMRPhenomXP_NRTidalv3:
 4009                case IMRPhenomXPHM:
 4010        case PhenSpinTaylorRD:
 4011        case SEOBNRv1:
 4012        case SpinDominatedWf:
 4013        case SEOBNRv2:
 4014        case SEOBNRv2_opt:
 4015        case SEOBNRv3:
 4016        case SEOBNRv3_pert:
 4017        case SEOBNRv3_opt:
 4018        case SEOBNRv3_opt_rk4:
 4019        case SEOBNRv4:
 4020        case SEOBNRv4_opt:
 4021        case SEOBNRv4P:
 4022        case SEOBNRv4PHM:
 4023        case SEOBNRv2T:
 4024        case SEOBNRv4T:
 4025        case SEOBNRv4_ROM_NRTidalv2_NSBH:
 4026        case SEOBNRv4_ROM_NRTidalv2:
 4027        case SEOBNRv5_ROM_NRTidalv3:
 4028        case NR_hdf5:
 4029        case NRSur7dq2:
 4030        case NRSur7dq4:
 4031        case TEOBResum_ROM:
 4032        case TEOBResumS:
 4033        case SEOBNRv4HM:
 4034        case NRHybSur3dq8:
 4035        case IMRPhenomT:
 4036        case IMRPhenomTHM:
 4037        case IMRPhenomTP:
 4038        case IMRPhenomTPHM:
 4039        case IMRPhenomXO4a:
 4040        case IMRPhenomXPNR:
 4041        case ExternalPython:
 4042        case SEOBNRv4HM_PA:
 4043        case pSEOBNRv4HM_PA:
 4044            return 1;
 4045 
 4046        default:
 4047            return 0;
 4048    }
 4049}
 4050 
 4051/**
 4052 * Checks whether the given approximant is implemented in lalsimulation's XLALSimInspiralChooseFDWaveform().
 4053 *
 4054 *
 4055 * returns 1 if the approximant is implemented, 0 otherwise.
 4056 */
 4057int XLALSimInspiralImplementedFDApproximants(
 4058    Approximant approximant /**< post-Newtonian approximant for use in waveform production */
 4059    )
 4060{
 4061    switch (approximant)
 4062    {
 4063        case IMRPhenomA:
 4064        case IMRPhenomB:
 4065        case IMRPhenomC:
 4066        case IMRPhenomD:
 4067        case IMRPhenomD_NRTidal:
 4068        case IMRPhenomD_NRTidalv2:
 4069        case IMRPhenomNSBH:
 4070        case IMRPhenomHM:
 4071        case IMRPhenomP:
 4072        case IMRPhenomPv2:
 4073        case IMRPhenomPv2_NRTidal:
 4074                case IMRPhenomPv2_NRTidalv2:
 4075                case IMRPhenomXAS:
 4076        case IMRPhenomXAS_NRTidalv2:
 4077        case IMRPhenomXAS_NRTidalv3:
 4078            case IMRPhenomXHM:
 4079                case IMRPhenomXP:
 4080        case IMRPhenomXP_NRTidalv2:
 4081        case IMRPhenomXP_NRTidalv3:
 4082                case IMRPhenomXPHM:
 4083        case EOBNRv2_ROM:
 4084        case EOBNRv2HM_ROM:
 4085        case SEOBNRv1_ROM_EffectiveSpin:
 4086        case SEOBNRv1_ROM_DoubleSpin:
 4087        case SEOBNRv2_ROM_EffectiveSpin:
 4088        case SEOBNRv2_ROM_DoubleSpin:
 4089        case SEOBNRv2_ROM_DoubleSpin_HI:
 4090        case Lackey_Tidal_2013_SEOBNRv2_ROM:
 4091        case SEOBNRv4_ROM:
 4092        case SEOBNRv4HM_ROM:
 4093        case SEOBNRv4_ROM_NRTidal:
 4094        case SEOBNRv4_ROM_NRTidalv2:
 4095        case SEOBNRv4_ROM_NRTidalv2_NSBH:
 4096        case SEOBNRv4T_surrogate:
 4097        case SEOBNRv5_ROM:
 4098        case SEOBNRv5HM_ROM:
 4099        case SEOBNRv5_ROM_NRTidalv3:
 4100        //case TaylorR2F4:
 4101        case TaylorF2:
 4102        case TaylorF2Ecc:
 4103        case TaylorF2NLTides:
 4104        case EccentricFD:
 4105        case SpinTaylorF2:
 4106        case TaylorF2RedSpin:
 4107        case TaylorF2RedSpinTidal:
 4108        case SpinTaylorT4Fourier:
 4109        case SpinTaylorT5Fourier:
 4110        case NRSur4d2s:
 4111        case IMRPhenomPv3:
 4112        case IMRPhenomPv3HM:
 4113        case ExternalPython:
 4114        case IMRPhenomXO4a:
 4115        case IMRPhenomXPNR:
 4116            return 1;
 4117 
 4118        default:
 4119            return 0;
 4120    }
 4121}
 4122 
 4123/**
 4124 * @brief Parses a waveform string to determine approximant, PN order, and axis choice.
 4125 * @details
 4126 * A waveform string can contain substrings specifying the approximant,
 4127 * the PN order, and the frame axis.  This routine decomposes the waveform
 4128 * string to extract this information.  Here we assume that there are no
 4129 * extraneous characters in the waveform string that do not encode this
 4130 * information.  If extra characters are detected then this routine returns
 4131 * a failure code.
 4132 *
 4133 * If one of the output parameters is set to NULL, this routine does not
 4134 * return the value for that parameter, and does not fail if that parameter
 4135 * cannot be determined from the waveform string; however, the full waveform
 4136 * string must be valid.  If the axis parameter is not NULL but information
 4137 * about the frame axis is not found in the string then the default value
 4138 * axis is set to the default value LAL_SIM_INSPIRAL_FRAME_AXIS_VIEW.
 4139 * However, if the approximant or order parameters are not NULL and
 4140 * the approximant and order cannot be determined from the waveform string,
 4141 * then this routine produces an error.
 4142 *
 4143 * Parsing is not case sensitive (using the "C" locale).
 4144 *
 4145 * @param[out] approximant The approximate value from Approximate enum.
 4146 * @param[out] order The PN order value from LALPNOrder enum.
 4147 * @param[out] axis The frame axis value from LALPNOrder enum.
 4148 * @param[in] waveform The waveform string.
 4149 * @retval 0 Success.
 4150 * @retval <0 Failure.
 4151 *
 4152 * @note
 4153 * Users of the SWIG-Python interface probably want to use the routines
 4154 * XLALSimInspiralGetApproximantFromString(),
 4155 * XLALSimInspiralGetPNOrderFromString(), and
 4156 * XLALSimInspiralGetFrameAxisFromString()
 4157 * since there is no way to disable required matching of the PN order
 4158 * with the SWIG-wrapped version of this routine.
 4159 */
 4160int XLALSimInspiralDecomposeWaveformString(int *approximant, int *order, int *axis, const char *waveform)
 4161{
 4162    char *string;
 4163    int found_approximant, found_order, found_axis;
 4164    int failed = 0;
 4165 
 4166    if (!waveform)
 4167        XLAL_ERROR(XLAL_EFAULT);
 4168 
 4169    string = XLALStringDuplicate(waveform);
 4170 
 4171#define DELETE_SUBSTRING_IN_LIST_FROM_STRING(string, list) delete_substring_in_list_from_string(string, list, sizeof(list)/sizeof(*list))
 4172    found_order       = DELETE_SUBSTRING_IN_LIST_FROM_STRING(string, lalSimulationPNOrderNames);
 4173    found_approximant = DELETE_SUBSTRING_IN_LIST_FROM_STRING(string, lalSimulationApproximantNames);
 4174    found_axis        = DELETE_SUBSTRING_IN_LIST_FROM_STRING(string, lalSimulationFrameAxisNames);
 4175#undef DELETE_SUBSTRING_IN_LIST_FROM_STRING
 4176 
 4177    /* assign values to output parameters */
 4178    if (approximant) {
 4179        *approximant = found_approximant;
 4180        /* fail if couldn't find approximant */
 4181        if (found_approximant < 0)
 4182            failed = 1;
 4183    }
 4184    if (order) {
 4185        *order = found_order;
 4186        /* fail if couldn't find order */
 4187        if (found_order < 0)
 4188            failed = 1;
 4189    }
 4190    if (axis) {
 4191        *axis = found_axis;
 4192        /* set frame axis to view if couldn't find, but don't fail */
 4193        if (found_axis < 0)
 4194            *axis = LAL_SIM_INSPIRAL_FRAME_AXIS_DEFAULT;
 4195    }
 4196 
 4197    /* check to see if there are extra characters */
 4198    if (strspn(string, "\b") != strlen(string))
 4199        failed = 1;
 4200 
 4201    XLALFree(string);
 4202 
 4203    if (failed)
 4204        XLAL_ERROR(XLAL_EINVAL, "Invalid waveform string `%s'.", waveform);
 4205    return 0;
 4206}
 4207 
 4208/**
 4209 * @brief Parses a waveform string to determine approximant.
 4210 * @details
 4211 * This routine uses XLALSimInspiralDecomposeWaveformString() to
 4212 * determine the approximant from the waveform string.
 4213 * @param[in] waveform The waveform string.
 4214 * @return The Approximant enum value, or -1 on error.
 4215 */
 4216int XLALSimInspiralGetApproximantFromString(const char *waveform)
 4217{
 4218    int approximant = -1;
 4219    if (XLALSimInspiralDecomposeWaveformString(&approximant, NULL, NULL, waveform)!=XLAL_SUCCESS)
 4220    {
 4221        approximant = -1;
 4222        XLAL_ERROR(XLAL_EFUNC);
 4223    }
 4224    return approximant;
 4225}
 4226 
 4227/**
 4228 * @deprecated
 4229 * Like XLALSimInspiralGetApproximantFromString() but doesn't demand that the
 4230 * remainder of the waveform string be valid.
 4231 */
 4232int XLALGetApproximantFromString(const char *waveform)
 4233{
 4234    int approximant = -1;
 4235    int errnum = 0;
 4236    XLAL_PRINT_DEPRECATION_WARNING("XLALSimInspiralGetApproximantFromString");
 4237    XLAL_TRY(XLALSimInspiralDecomposeWaveformString(&approximant, NULL, NULL, waveform), errnum);
 4238    if (errnum && errnum != XLAL_EINVAL) // pass any error other than XLAL_EINVAL
 4239        XLAL_ERROR(errnum);
 4240    /* fail if approximant wasn't found */
 4241    if (approximant < 0)
 4242        XLAL_ERROR(XLAL_EINVAL, "Cannot parse approximant from string `%s'.", waveform);
 4243    return approximant;
 4244}
 4245 
 4246/**
 4247 * @brief Parses a waveform string to determine PN order.
 4248 * @details
 4249 * This routine uses XLALSimInspiralDecomposeWaveformString() to
 4250 * determine the PN order from the waveform string.
 4251 * @param[in] waveform The waveform string.
 4252 * @return The LALPNOrder enum value, or -1 on error.
 4253 */
 4254int XLALSimInspiralGetPNOrderFromString(const char *waveform)
 4255{
 4256    int order = -1;
 4257    if (XLALSimInspiralDecomposeWaveformString(NULL, &order, NULL, waveform) < 0)
 4258        XLAL_ERROR(XLAL_EFUNC);
 4259    return order;
 4260}
 4261 
 4262/**
 4263 * @deprecated
 4264 * Like XLALSimInspiralGetPNOrderFromString() but doesn't demand that the
 4265 * remainder of the waveform string be valid.
 4266 */
 4267int XLALGetOrderFromString(const char *waveform)
 4268{
 4269    int order = -1;
 4270    int errnum = 0;
 4271    XLAL_PRINT_DEPRECATION_WARNING("XLALSimInspiralGetPNOrderFromString");
 4272    XLAL_TRY(XLALSimInspiralDecomposeWaveformString(NULL, &order, NULL, waveform), errnum);
 4273    if (errnum && errnum != XLAL_EINVAL) // pass any error other than XLAL_EINVAL
 4274        XLAL_ERROR(errnum);
 4275    /* fail if order wasn't found */
 4276    if (order < 0)
 4277        XLAL_ERROR(XLAL_EINVAL, "Cannot parse approximant from string `%s'.", waveform);
 4278    return order;
 4279}
 4280 
 4281/**
 4282 * @brief Parses a waveform string to determine frame axis.
 4283 * @details
 4284 * This routine uses XLALSimInspiralDecomposeWaveformString() to
 4285 * determine the frame axis from the waveform string.  If the
 4286 * frame axis cannot be determined, the value
 4287 * LAL_SIM_INSPIRAL_FRAME_AXIS_VIEW is returned.
 4288 * @param[in] waveform The waveform string.
 4289 * @return The LALPNOrder enum value, or -1 on error.
 4290 */
 4291int XLALSimInspiralGetFrameAxisFromString(const char *waveform)
 4292{
 4293    int axis = -1;
 4294    if (XLALSimInspiralDecomposeWaveformString(NULL, NULL, &axis, waveform) < 0)
 4295        XLAL_ERROR(XLAL_EFUNC);
 4296    return axis;
 4297}
 4298 
 4299/**
 4300 * @deprecated
 4301 * Like XLALSimInspiralGetFrameAxisFromString() but doesn't demand that the
 4302 * remainder of the waveform string be valid.
 4303 */
 4304int XLALGetFrameAxisFromString(const char *waveform)
 4305{
 4306    int axis = -1;
 4307    int errnum = 0;
 4308    XLAL_PRINT_DEPRECATION_WARNING("XLALSimInspiralGetFrameAxisFromString");
 4309    XLAL_TRY(XLALSimInspiralDecomposeWaveformString(NULL, NULL, &axis, waveform), errnum);
 4310    if (errnum && errnum != XLAL_EINVAL) // pass any error other than XLAL_EINVAL
 4311        XLAL_ERROR(errnum);
 4312    /* if axis wasn't found, use view */
 4313    if (axis < 0)
 4314        axis = LAL_SIM_INSPIRAL_FRAME_AXIS_DEFAULT;
 4315    return axis;
 4316}
 4317 
 4318/**
 4319 * @brief Parses a string to determine the LALSimInspiralApplyTaper enum value.
 4320 * @details
 4321 * Parses a string to determine the LALSimInspiralApplyTaper enum value.
 4322 * Parsing is not case sensitive (using the "C" locale).
 4323 * @param[in] string The string to be parsed.
 4324 * @return The LALSimInspiralApplyTaper enum value, or -1 on error.
 4325 */
 4326int XLALSimInspiralGetTaperFromString(const char *string)
 4327{
 4328    const char **list = lalSimulationTaperNames;
 4329    size_t size = sizeof(lalSimulationTaperNames)/sizeof(*lalSimulationTaperNames);
 4330    size_t i;
 4331 
 4332    if (!string)
 4333        XLAL_ERROR(XLAL_EFAULT);
 4334 
 4335    for (i = 0; i < size; ++i)
 4336        if (list[i])
 4337            if (XLALStringCaseCompare(string, list[i]) == 0) // found it
 4338                return i;
 4339 
 4340    XLAL_ERROR(XLAL_EINVAL, "Invalid injection tapering string `%s'.", string);
 4341}
 4342 
 4343/**
 4344 * @deprecated
 4345 * Use XLALSimInspiralGetTaperFromString() instead.
 4346 */
 4347int XLALGetTaperFromString(const char *string)
 4348{
 4349    XLAL_PRINT_DEPRECATION_WARNING("XLALSimInspiralGetTaperFromString");
 4350    return XLALSimInspiralGetTaperFromString(string);
 4351}
 4352 
 4353/**
 4354 * @brief Parses a string to determine the LALSimInspiralModesChoice enum value.
 4355 * @details
 4356 * Parses a string to determine the LALSimInspiralModesChoice enum value.
 4357 * Parsing is not case sensitive (using the "C" locale).
 4358 * @param[in] string The string to be parsed.
 4359 * @return The LALSimInspiralModesChoice enum value, or 0 on error.
 4360 * @note The normal error code -1 is actually a valid mode choice
 4361 * so this routine returns 0 (which is not a valid modes choice)
 4362 * on error rather than -1.
 4363 */
 4364int XLALSimInspiralGetHigherModesFromString(const char *string)
 4365{
 4366    const char **list = lalSimulationModesChoiceNames;
 4367    size_t size = sizeof(lalSimulationModesChoiceNames)/sizeof(*lalSimulationModesChoiceNames);
 4368    size_t i;
 4369 
 4370    if (!string)
 4371        XLAL_ERROR(XLAL_EFAULT);
 4372 
 4373    /* the "ALL" case is a special case */
 4374    if (XLALStringCaseCompare(string, "ALL") == 0)
 4375        return LAL_SIM_INSPIRAL_MODES_CHOICE_ALL;
 4376 
 4377    for (i = 0; i < size; ++i)
 4378        if (list[i])
 4379            if (XLALStringCaseCompare(string, list[i]) == 0) // found it
 4380                return i;
 4381 
 4382    XLAL_ERROR_VAL(0, XLAL_EINVAL, "Invalid injection modes choice string `%s'.", string);
 4383}
 4384 
 4385/**
 4386 * @deprecated
 4387 * Use XLALSimInspiralHigherModesFromString() instead.
 4388 */
 4389int XLALGetHigherModesFromString(const char *string)
 4390{
 4391    XLAL_PRINT_DEPRECATION_WARNING("XLALSimInspiralGetHigherModesFromString");
 4392    return XLALSimInspiralGetHigherModesFromString(string);
 4393}
 4394 
 4395/**
 4396 * @brief Returns a string associated with an Approximant enum value.
 4397 * @param[in] approximant The Approximant enum value.
 4398 * @returns A constant string or NULL if there is an error.
 4399 */
 4400const char * XLALSimInspiralGetStringFromApproximant(Approximant approximant)
 4401{
 4402    const char *s;
 4403    if ((int)(approximant) < 0 || (int)(approximant) >= NumApproximants)
 4404        XLAL_ERROR_NULL(XLAL_EINVAL);
 4405    s = lalSimulationApproximantNames[approximant];
 4406    if (!s)
 4407        XLAL_ERROR_NULL(XLAL_EINVAL);
 4408    return s;
 4409}
 4410 
 4411/**
 4412 * @deprecated
 4413 * Use XLALSimInspiralHigherModesFromString() instead.
 4414 */
 4415const char * XLALGetStringFromApproximant(Approximant approximant)
 4416{
 4417    XLAL_PRINT_DEPRECATION_WARNING("XLALSimInspiralGetStringFromApproximant");
 4418    return XLALSimInspiralGetStringFromApproximant(approximant);
 4419}
 4420 
 4421/**
 4422 * @brief Returns a string associated with a LALPNOrder enum value.
 4423 * @param[in] order The LALPNOrder enum value.
 4424 * @returns A constant string or NULL if there is an error.
 4425 */
 4426const char * XLALSimInspiralGetStringFromPNOrder(LALPNOrder order)
 4427{
 4428    const char *s;
 4429    if ((int)(order) < 0 || (int)(order) >= LAL_PNORDER_NUM_ORDER)
 4430        XLAL_ERROR_NULL(XLAL_EINVAL);
 4431    s = lalSimulationPNOrderNames[order];
 4432    if (!s)
 4433        XLAL_ERROR_NULL(XLAL_EINVAL);
 4434    return s;
 4435}
 4436 
 4437/**
 4438 * @brief Returns a string associated with a LALSimInspiralApplyTaper enum value.
 4439 * @param[in] taper The LALSimInspiralApplyTaper enum value.
 4440 * @returns A constant string or NULL if there is an error.
 4441 */
 4442const char * XLALSimInspiralGetStringFromTaper(LALSimInspiralApplyTaper taper)
 4443{
 4444    const char *s;
 4445    if ((int)(taper) < 0 || (int)(taper) >= LAL_SIM_INSPIRAL_TAPER_NUM_OPTS)
 4446        XLAL_ERROR_NULL(XLAL_EINVAL);
 4447    s = lalSimulationTaperNames[taper];
 4448    if (!s)
 4449        XLAL_ERROR_NULL(XLAL_EINVAL);
 4450    return s;
 4451}
 4452 
 4453/**
 4454 * @brief Returns a string associated with a LALSimInspiralFrameAxis enum value.
 4455 * @param[in] axis The LALSimInspiralFrameAxis enum value.
 4456 * @returns A constant string or NULL if there is an error.
 4457 */
 4458const char * XLALSimInspiralGetStringFromFrameAxis(LALSimInspiralFrameAxis axis)
 4459{
 4460    const char *s;
 4461    if ((int)(axis) < 0 || (size_t)(axis) >= sizeof(lalSimulationFrameAxisNames)/sizeof(*lalSimulationFrameAxisNames))
 4462        XLAL_ERROR_NULL(XLAL_EINVAL);
 4463    s = lalSimulationFrameAxisNames[axis];
 4464    if (!s)
 4465        XLAL_ERROR_NULL(XLAL_EINVAL);
 4466    return s;
 4467}
 4468 
 4469/**
 4470 * @brief Returns a string associated with a LALSimInspiralModesChoice enum value.
 4471 * @param[in] modes The LALSimInspiralModesChoice enum value.
 4472 * @returns A constant string or NULL if there is an error.
 4473 */
 4474const char * XLALSimInspiralGetStringFromModesChoice(LALSimInspiralModesChoice modes)
 4475{
 4476    const char *s;
 4477    if (modes == LAL_SIM_INSPIRAL_MODES_CHOICE_ALL) // handle this case separately
 4478        return "ALL";
 4479    if ((int)(modes) < 0 || (size_t)(modes) >= sizeof(lalSimulationModesChoiceNames)/sizeof(*lalSimulationModesChoiceNames))
 4480        XLAL_ERROR_NULL(XLAL_EINVAL);
 4481    s = lalSimulationModesChoiceNames[modes];
 4482    if (!s)
 4483        XLAL_ERROR_NULL(XLAL_EINVAL);
 4484    return s;
 4485}
 4486 
 4487int XLALSimInspiralGetSpinSupportFromApproximant(Approximant approx){
 4488 
 4489  SpinSupport spin_support=LAL_SIM_INSPIRAL_NUMSPINSUPPORT;
 4490  switch (approx)
 4491  {
 4492    case SpinTaylor:
 4493    case SpinTaylorFrameless:
 4494    case SpinTaylorT1:
 4495    case SpinTaylorT4:
 4496    case SpinTaylorT5:
 4497    case PhenSpinTaylor:
 4498    case PhenSpinTaylorRD:
 4499    case SpinTaylorT3:
 4500    case IMRPhenomP:
 4501    case IMRPhenomPv2:
 4502    case IMRPhenomPv2_NRTidal:
 4503    case IMRPhenomPv2_NRTidalv2:
 4504    case IMRPhenomPv3:
 4505    case IMRPhenomPv3HM:
 4506        case IMRPhenomXP:
 4507    case IMRPhenomXP_NRTidalv2:
 4508    case IMRPhenomXP_NRTidalv3:
 4509        case IMRPhenomXPHM:
 4510    case SpinTaylorT5Fourier:
 4511    case SpinTaylorT4Fourier:
 4512    case SpinDominatedWf:
 4513    case SEOBNRv3:
 4514    case SEOBNRv3_pert:
 4515    case SEOBNRv3_opt:
 4516    case SEOBNRv3_opt_rk4:
 4517    case SEOBNRv4P:
 4518    case SEOBNRv4PHM:
 4519    case NR_hdf5:
 4520    case NRSur4d2s:
 4521    case NRSur7dq2:
 4522    case NRSur7dq4:
 4523    case IMRPhenomTP:
 4524    case IMRPhenomTPHM:
 4525    case IMRPhenomXO4a:
 4526    case IMRPhenomXPNR:
 4527      spin_support=LAL_SIM_INSPIRAL_PRECESSINGSPIN;
 4528      break;
 4529    case SpinTaylorF2:
 4530    case FindChirpPTF:
 4531    case HGimri:
 4532      spin_support=LAL_SIM_INSPIRAL_SINGLESPIN;
 4533      break;
 4534    case TaylorF2:
 4535    case TaylorF2Ecc:
 4536    case TaylorF2NLTides:
 4537    case TaylorF2RedSpin:
 4538    case TaylorF2RedSpinTidal:
 4539    case IMRPhenomB:
 4540    case IMRPhenomC:
 4541    case IMRPhenomD:
 4542    case IMRPhenomD_NRTidal:
 4543    case IMRPhenomD_NRTidalv2:
 4544    case IMRPhenomNSBH:
 4545    case IMRPhenomHM:
 4546    case IMRPhenomXAS:
 4547    case IMRPhenomXAS_NRTidalv2:
 4548    case IMRPhenomXAS_NRTidalv3:
 4549    case IMRPhenomXHM:
 4550    case SEOBNRv1:
 4551    case SEOBNRv2:
 4552    case SEOBNRv4:
 4553    case SEOBNRv2_opt:
 4554    case SEOBNRv4_opt:
 4555    case SEOBNRv2T:
 4556    case SEOBNRv4T:
 4557    case SEOBNRv4HM:
 4558    case SEOBNRv1_ROM_EffectiveSpin:
 4559    case SEOBNRv1_ROM_DoubleSpin:
 4560    case SEOBNRv2_ROM_EffectiveSpin:
 4561    case SEOBNRv2_ROM_DoubleSpin:
 4562    case SEOBNRv2_ROM_DoubleSpin_HI:
 4563    case Lackey_Tidal_2013_SEOBNRv2_ROM:
 4564    case SEOBNRv4_ROM:
 4565    case SEOBNRv4HM_ROM:
 4566    case SEOBNRv4_ROM_NRTidal:
 4567    case SEOBNRv4_ROM_NRTidalv2:
 4568    case SEOBNRv4_ROM_NRTidalv2_NSBH:
 4569    case SEOBNRv4T_surrogate:
 4570    case SEOBNRv5_ROM:
 4571    case SEOBNRv5HM_ROM:
 4572    case SEOBNRv5_ROM_NRTidalv3:
 4573    case TEOBResumS:
 4574    case TaylorR2F4:
 4575    case IMRPhenomFB:
 4576    case FindChirpSP:
 4577    case NRHybSur3dq8:
 4578    case IMRPhenomT:
 4579    case IMRPhenomTHM:
 4580    case SEOBNRv4HM_PA:
 4581    case pSEOBNRv4HM_PA:
 4582      spin_support=LAL_SIM_INSPIRAL_ALIGNEDSPIN;
 4583      break;
 4584    case TaylorEt:
 4585    case TaylorT1:
 4586    case TaylorT2:
 4587    case TaylorT3:
 4588    case TaylorT4:
 4589    case EccentricTD:
 4590    case EccentricFD:
 4591    case IMRPhenomA:
 4592    case EOBNRv2HM:
 4593    case EOBNRv2HM_ROM:
 4594    case EOBNRv2:
 4595    case EOBNRv2_ROM:
 4596    case EOBNR:
 4597    case EOB:
 4598    case IMRPhenomFA:
 4599    case GeneratePPN:
 4600    case TEOBResum_ROM:
 4601      spin_support=LAL_SIM_INSPIRAL_SPINLESS;
 4602      break;
 4603    case ExternalPython:
 4604      spin_support=LAL_SIM_INSPIRAL_CASEBYCASE_SPINSUPPORT;
 4605      break;
 4606    default:
 4607      XLALPrintError("Approximant not supported by lalsimulation TD/FD routines \n");
 4608      XLAL_ERROR(XLAL_EINVAL);
 4609    }
 4610 
 4611    return spin_support;
 4612 
 4613}
 4614 
 4615int XLALSimInspiralGetSpinFreqFromApproximant(Approximant approx){
 4616 
 4617  SpinFreq spin_freq=LAL_SIM_INSPIRAL_NUMSPINFREQ;
 4618  switch (approx)
 4619  {
 4620    case SEOBNRv3:
 4621    case SEOBNRv3_pert:
 4622    case SEOBNRv3_opt:
 4623    case SEOBNRv3_opt_rk4:
 4624    case SEOBNRv4P:
 4625    case SEOBNRv4PHM:
 4626      spin_freq=LAL_SIM_INSPIRAL_SPINS_FLOW;
 4627      break;
 4628    case SpinTaylor:
 4629    case SpinTaylorFrameless:
 4630    case SpinTaylorT1:
 4631    case SpinTaylorT4:
 4632    case SpinTaylorT5:
 4633    case PhenSpinTaylor:
 4634    case PhenSpinTaylorRD:
 4635    case SpinTaylorT3:
 4636    case IMRPhenomP:
 4637    case IMRPhenomPv2:
 4638    case IMRPhenomPv3:
 4639    case IMRPhenomPv3HM:
 4640    case IMRPhenomPv2_NRTidal:
 4641    case IMRPhenomPv2_NRTidalv2:
 4642        case IMRPhenomXP:
 4643    case IMRPhenomXP_NRTidalv2:
 4644    case IMRPhenomXP_NRTidalv3:
 4645        case IMRPhenomXPHM:
 4646    case SpinTaylorT5Fourier:
 4647    case SpinTaylorT4Fourier:
 4648    case SpinDominatedWf:
 4649    case NRSur4d2s:
 4650    case NRSur7dq2:
 4651    case NRSur7dq4:
 4652    case SpinTaylorF2:
 4653    case IMRPhenomTP:
 4654    case IMRPhenomTPHM:
 4655    case IMRPhenomXO4a:
 4656    case IMRPhenomXPNR:
 4657      spin_freq=LAL_SIM_INSPIRAL_SPINS_F_REF;
 4658      break;
 4659    case FindChirpPTF:
 4660    case HGimri:
 4661    case TaylorF2:
 4662    case TaylorF2Ecc:
 4663    case TaylorF2NLTides:
 4664    case TaylorF2RedSpin:
 4665    case TaylorF2RedSpinTidal:
 4666    case IMRPhenomB:
 4667    case IMRPhenomC:
 4668    case IMRPhenomD:
 4669    case IMRPhenomD_NRTidal:
 4670    case IMRPhenomD_NRTidalv2:
 4671    case IMRPhenomNSBH:
 4672    case IMRPhenomHM:
 4673    case IMRPhenomXAS:
 4674    case IMRPhenomXAS_NRTidalv2:
 4675    case IMRPhenomXAS_NRTidalv3:
 4676    case IMRPhenomXHM:
 4677    case SEOBNRv1:
 4678    case SEOBNRv2:
 4679    case SEOBNRv4:
 4680    case SEOBNRv2_opt:
 4681    case SEOBNRv4_opt:
 4682    case SEOBNRv2T:
 4683    case SEOBNRv4T:
 4684    case SEOBNRv4HM:
 4685    case SEOBNRv1_ROM_EffectiveSpin:
 4686    case SEOBNRv1_ROM_DoubleSpin:
 4687    case SEOBNRv2_ROM_EffectiveSpin:
 4688    case SEOBNRv2_ROM_DoubleSpin:
 4689    case SEOBNRv2_ROM_DoubleSpin_HI:
 4690    case Lackey_Tidal_2013_SEOBNRv2_ROM:
 4691    case SEOBNRv4_ROM:
 4692    case SEOBNRv4_ROM_NRTidal:
 4693    case SEOBNRv4_ROM_NRTidalv2:
 4694    case SEOBNRv4_ROM_NRTidalv2_NSBH:
 4695    case SEOBNRv4T_surrogate:
 4696    case SEOBNRv4HM_ROM:
 4697    case SEOBNRv5_ROM:
 4698    case SEOBNRv5HM_ROM:
 4699    case SEOBNRv5_ROM_NRTidalv3:
 4700    case TaylorR2F4:
 4701    case IMRPhenomFB:
 4702    case FindChirpSP:
 4703    case NRHybSur3dq8:
 4704    case TaylorEt:
 4705    case TaylorT1:
 4706    case TaylorT2:
 4707    case TaylorT3:
 4708    case TaylorT4:
 4709    case EccentricTD:
 4710    case EccentricFD:
 4711    case IMRPhenomA:
 4712    case EOBNRv2HM:
 4713    case EOBNRv2HM_ROM:
 4714    case EOBNRv2:
 4715    case EOBNRv2_ROM:
 4716    case EOBNR:
 4717    case EOB:
 4718    case IMRPhenomFA:
 4719    case GeneratePPN:
 4720    case TEOBResum_ROM:
 4721    case IMRPhenomT:
 4722    case IMRPhenomTHM:
 4723        case TEOBResumS:
 4724    case SEOBNRv4HM_PA:
 4725    case pSEOBNRv4HM_PA:
 4726      spin_freq=LAL_SIM_INSPIRAL_SPINS_NONPRECESSING;
 4727      break;
 4728    case NR_hdf5:
 4729    case ExternalPython:
 4730      spin_freq=LAL_SIM_INSPIRAL_SPINS_CASEBYCASE;
 4731      break;
 4732    default:
 4733      XLALPrintError("Approximant not supported by lalsimulation TD/FD routines \n");
 4734      XLAL_ERROR(XLAL_EINVAL);
 4735    }
 4736 
 4737    return spin_freq;
 4738 
 4739}
 4740 
 4741int XLALSimInspiralGetAllowZeroMinFreqFromApproximant(Approximant approx){
 4742 
 4743  // Models for which LAL_SIM_INSPIRAL_ALLOW_ZERO_FMIN is set allow f_min=0,
 4744  // which means that the full length of the waveform is returned. This means
 4745  // that in XLALSimInspiralTD, XLALSimInspiralChooseTDWaveform is called
 4746  // instead of XLALSimInspiralTDFromTD for these models. This also means that
 4747  // the starting frequency is not altered (as done in XLALSimInspiralTDFromTD)
 4748  // for these models, independent of what f_min is passed.
 4749 
 4750  AllowZeroMinFreq allow_zero_fmin = LAL_SIM_INSPIRAL_NUMZEROFMIN;
 4751  switch (approx)
 4752  {
 4753    case NRSur7dq2:
 4754    case NRSur7dq4:
 4755      allow_zero_fmin=LAL_SIM_INSPIRAL_ALLOW_ZERO_FMIN;
 4756      break;
 4757    default:
 4758      allow_zero_fmin=LAL_SIM_INSPIRAL_DISALLOW_ZERO_FMIN;
 4759    }
 4760 
 4761    return allow_zero_fmin;
 4762 
 4763}
 4764 
 4765int XLALSimInspiralApproximantAcceptTestGRParams(Approximant approx){
 4766 
 4767  TestGRaccept testGR_accept=LAL_SIM_INSPIRAL_NUM_TESTGR_ACCEPT;
 4768  switch (approx)
 4769    {
 4770    case TaylorT1:
 4771    case TaylorT2:
 4772    case TaylorT3:
 4773    case TaylorF1:
 4774    case TaylorR2F4:
 4775    case TaylorF2RedSpin:
 4776    case TaylorF2RedSpinTidal:
 4777    case PadeT1:
 4778    case PadeF1:
 4779    case EOB:
 4780    case BCV:
 4781    case BCVSpin:
 4782    case SpinTaylorT1:
 4783    case SpinTaylorT5:
 4784    case SpinTaylorT3:
 4785    case SpinTaylorT4:
 4786    case SpinTaylorFrameless:
 4787    case SpinTaylor:
 4788    case SpinQuadTaylor:
 4789    case FindChirpSP:
 4790    case FindChirpPTF:
 4791    case HGimri:
 4792    case GeneratePPN:
 4793    case BCVC:
 4794    case FrameFile:
 4795    case AmpCorPPN:
 4796    case NumRel:
 4797    case NumRelNinja2:
 4798    case EOBNR:
 4799    case EOBNRv2:
 4800    case EOBNRv2_ROM:
 4801    case EOBNRv2HM:
 4802    case EOBNRv2HM_ROM:
 4803    case TEOBResum_ROM:
 4804    case SEOBNRv1:
 4805    case SEOBNRv2:
 4806    case SEOBNRv2_opt:
 4807    case SEOBNRv3:
 4808    case SEOBNRv3_pert:
 4809    case SEOBNRv3_opt:
 4810    case SEOBNRv3_opt_rk4:
 4811    case SEOBNRv4:
 4812    case SEOBNRv4_opt:
 4813    case SEOBNRv4P:
 4814    case SEOBNRv4PHM:
 4815    case SEOBNRv2T:
 4816    case SEOBNRv4T:
 4817    case SEOBNRv4HM:
 4818    case SEOBNRv1_ROM_EffectiveSpin:
 4819    case SEOBNRv1_ROM_DoubleSpin:
 4820    case SEOBNRv2_ROM_EffectiveSpin:
 4821    case SEOBNRv2_ROM_DoubleSpin:
 4822    case SEOBNRv2_ROM_DoubleSpin_HI:
 4823    case Lackey_Tidal_2013_SEOBNRv2_ROM:
 4824    case TEOBResumS:
 4825    case IMRPhenomA:
 4826    case IMRPhenomB:
 4827    case IMRPhenomFA:
 4828    case IMRPhenomFB:
 4829    case IMRPhenomFC:
 4830    case IMRPhenomNSBH:
 4831    case SpinTaylorT5Fourier:
 4832    case SpinTaylorT4Fourier:
 4833    case TaylorEt:
 4834    case TaylorT4:
 4835    case TaylorN:
 4836    case SpinDominatedWf:
 4837    case NR_hdf5:
 4838    case NRSur4d2s:
 4839    case NRSur7dq2:
 4840    case NRSur7dq4:
 4841    case NRHybSur3dq8:
 4842    case IMRPhenomT:
 4843    case IMRPhenomTHM:
 4844    case IMRPhenomTP:
 4845    case IMRPhenomTPHM:
 4846    case NumApproximants:
 4847    case SEOBNRv4HM_PA:
 4848    case IMRPhenomXO4a:
 4849    case IMRPhenomXPNR:
 4850      testGR_accept=LAL_SIM_INSPIRAL_NO_TESTGR_PARAMS;
 4851      break;
 4852    case TaylorF2:
 4853    case TaylorF2Ecc:
 4854    case TaylorF2NLTides:
 4855    case SpinTaylorF2:
 4856    case EccentricFD:
 4857    case Eccentricity:
 4858    case PhenSpinTaylor:
 4859    case PhenSpinTaylorRD:
 4860    case EccentricTD:
 4861    case SEOBNRv4_ROM:
 4862    case SEOBNRv4HM_ROM:
 4863    case SEOBNRv4_ROM_NRTidal:
 4864    case SEOBNRv4_ROM_NRTidalv2:
 4865    case SEOBNRv4_ROM_NRTidalv2_NSBH:
 4866    case SEOBNRv4T_surrogate:
 4867    case SEOBNRv5_ROM:
 4868    case SEOBNRv5HM_ROM:
 4869    case SEOBNRv5_ROM_NRTidalv3:
 4870    case IMRPhenomC:
 4871    case IMRPhenomD:
 4872    case IMRPhenomP:
 4873    case IMRPhenomPv2:
 4874    case IMRPhenomPv2_NRTidal:
 4875    case IMRPhenomPv2_NRTidalv2:
 4876    case IMRPhenomD_NRTidal:
 4877    case IMRPhenomD_NRTidalv2:
 4878    case IMRPhenomHM:
 4879    case IMRPhenomPv3:
 4880    case IMRPhenomPv3HM:
 4881    case pSEOBNRv4HM_PA:
 4882    case IMRPhenomXAS:
 4883    case IMRPhenomXHM:
 4884    case IMRPhenomXP:
 4885    case IMRPhenomXPHM:
 4886    case IMRPhenomXAS_NRTidalv2:
 4887    case IMRPhenomXAS_NRTidalv3:
 4888    case IMRPhenomXP_NRTidalv2:
 4889      testGR_accept=LAL_SIM_INSPIRAL_TESTGR_PARAMS;
 4890      break;
 4891    case IMRPhenomXP_NRTidalv3:
 4892      testGR_accept=LAL_SIM_INSPIRAL_TESTGR_PARAMS;
 4893      break;
 4894    case ExternalPython:
 4895                        testGR_accept=LAL_SIM_INSPIRAL_CASEBYCASE_TESTGR_PARAMS;
 4896      break;
 4897    default:
 4898      XLALPrintError("Approximant not supported by lalsimulation TD/FD routines \n");
 4899      XLAL_ERROR(XLAL_EINVAL);
 4900    }
 4901  return testGR_accept;
 4902};
 4903 
 4904/* Function for introducing Lorentz violating changes in FD phase; calculates eqns. 30 & 32 of arxiv 1110.2720 for the LV phase term in FD and multiplies to h+ and hx */
 4905int XLALSimLorentzInvarianceViolationTerm(
 4906                                          COMPLEX16FrequencySeries **hptilde, /**< Frequency-domain waveform h+ */
 4907                                          COMPLEX16FrequencySeries **hctilde, /**< Frequency-domain waveform hx */
 4908                                          REAL8 m1,                           /**< Mass 1 in solar masses */
 4909                                          REAL8 m2,                           /**< Mass 2 in solar masses */
 4910                                          REAL8 r,                            /**< distance in metres*/
 4911                                          LALDict *LALparams                     /**< LAL dictionary containing accessory parameters */
 4912                                          )
 4913{
 4914  REAL8 f0, f, df;
 4915  COMPLEX16 hplus, hcross, tmpExp;
 4916  REAL8 M, eta, zeta, dPhiPref, Mc, tmpVal;
 4917  UINT4 len, i;
 4918  M = m1+m2;
 4919  eta = m1*m2/(M*M);
 4920  Mc = M*pow(eta, 0.6);
 4921  len = (*hptilde)->data->length;
 4922 
 4923  REAL8 lambda_eff = pow(10,XLALSimInspiralWaveformParamsLookupNonGRLIVLogLambdaEff(LALparams)); /* Effective wavelength-like parameter in phase in metres */
 4924  REAL8 nonGR_alpha = XLALSimInspiralWaveformParamsLookupNonGRLIVAlpha(LALparams);   /* Exponent defined in terms of PN order characterising LIV*/
 4925  REAL8 LIV_A_sign = XLALSimInspiralWaveformParamsLookupNonGRLIVASign(LALparams);   /* Sign of A determining the sign of LV phase */
 4926 
 4927  if ((*hctilde)->data->length != len) {
 4928    XLALPrintError("Lengths of plus and cross polarization series do not agree \n");
 4929    XLAL_ERROR(XLAL_EBADLEN);
 4930  }
 4931 
 4932  f0 = (*hptilde)->f0;
 4933  if ((*hctilde)->f0 != f0) {
 4934    XLALPrintError("Starting frequencies of plus and cross polarization series do not agree \n");
 4935    XLAL_ERROR(XLAL_EINVAL);
 4936  }
 4937 
 4938  df = (*hptilde)->deltaF;
 4939  if ((*hctilde)->deltaF != df) {
 4940    XLALPrintError("Frequency steps of plus and cross polarization series do not agree \n");
 4941    XLAL_ERROR(XLAL_EINVAL);
 4942  }
 4943 
 4944  UINT4 k = 0;
 4945  if (f0 == 0.0)
 4946      k=1;
 4947 
 4948  if (nonGR_alpha == 1) {
 4949    zeta = LIV_A_sign*LAL_PI*r/lambda_eff; /*Eqn. (32) of arxiv:1110.2720*/
 4950    dPhiPref = zeta*log(LAL_PI*Mc*LAL_MTSUN_SI); /*Eqn. (31) of arxiv:1110.2720;the frequency dependence is treated below*/
 4951    for (i=k; i<len; i++) {
 4952      f = f0 + i*df;
 4953      tmpExp = cexp(I*(dPhiPref + zeta*log(f)));
 4954      hplus = (*hptilde)->data->data[i] * tmpExp;
 4955      (*hptilde)->data->data[i] = hplus;
 4956      hcross = (*hctilde)->data->data[i] * tmpExp;
 4957      (*hctilde)->data->data[i] = hcross;
 4958    }
 4959  }
 4960  else {
 4961    zeta = LIV_A_sign*pow(LAL_PI, (2. - nonGR_alpha))*r*pow(Mc*LAL_MRSUN_SI, (1. - nonGR_alpha))/((1. - nonGR_alpha)*pow(lambda_eff, (2. - nonGR_alpha))); /*Eqn. (30) of arxiv:1110.2720*/
 4962    dPhiPref = zeta*pow(LAL_PI*Mc*LAL_MTSUN_SI, (nonGR_alpha - 1.)); /*Eqn. (28) of arxiv:1110.2720;the frequency dependence is treated below*/
 4963    for (i=k; i<len; i++) {
 4964      f = f0 + i*df;
 4965      tmpVal = pow(f, (nonGR_alpha - 1.));
 4966      tmpExp=cexp(-I*dPhiPref*tmpVal);
 4967      hplus = (*hptilde)->data->data[i] * tmpExp;
 4968      (*hptilde)->data->data[i] = hplus;
 4969      hcross = (*hctilde)->data->data[i] * tmpExp;
 4970      (*hctilde)->data->data[i] = hcross;
 4971    }
 4972 
 4973  }
 4974  return XLAL_SUCCESS;
 4975}
 4976 
 4977/** @} */
 4978 
 4979/**
 4980 * @name Routines Determining Waveform Durations and Frequencies
 4981 * @{
 4982 */
 4983 
 4984/**
 4985 * @brief Routine to compute an overestimate of the inspiral time from a given frequency.
 4986 * @details
 4987 * This routine estimates the time it will take for point-particle inspiral from a
 4988 * specified frequency to infinite frequency.  The estimate is intended to be an
 4989 * over-estimate, so that the true inspiral time is always smaller than the time this
 4990 * routine returns.  To obtain this estimate, the 2pN chirp time is used where all
 4991 * negative contributions are discarded.
 4992 * @param fstart The starting frequency in Hz.
 4993 * @param m1 The mass of the first component in kg.
 4994 * @param m2 The mass of the second component in kg.
 4995 * @param s1 The dimensionless spin of the first component.
 4996 * @param s2 The dimensionless spin of the second component.
 4997 * @return Upper bound on chirp time of post-Newtonian inspiral in seconds.
 4998 */
 4999REAL8 XLALSimInspiralChirpTimeBound(REAL8 fstart, REAL8 m1, REAL8 m2, REAL8 s1, REAL8 s2)
 5000{
 5001    double M = m1 + m2; // total mass
 5002    double mu = m1 * m2 / M; // reduced mass
 5003    double eta = mu / M; // symmetric mass ratio
 5004    /* chi = (s1*m1 + s2*m2)/M <= max(|s1|,|s2|) */
 5005    double chi = fabs(fabs(s1) > fabs(s2) ? s1 : s2); // over-estimate of chi
 5006    /* note: for some reason these coefficients are named wrong...
 5007     * "2PN" should be "1PN", "4PN" should be "2PN", etc. */
 5008    double c0 = fabs(XLALSimInspiralTaylorT2Timing_0PNCoeff(M, eta));
 5009    double c2 = XLALSimInspiralTaylorT2Timing_2PNCoeff(eta);
 5010    /* the 1.5pN spin term is in TaylorT2 is 8*beta/5 [Citation ??]
 5011     * where beta = (113/12 + (25/4)(m2/m1))*(s1*m1^2/M^2) + 2 <-> 1
 5012     * [Cutler & Flanagan, Physical Review D 49, 2658 (1994), Eq. (3.21)]
 5013     * which can be written as (113/12)*chi - (19/6)(s1 + s2)
 5014     * and we drop the negative contribution */
 5015    double c3 = (226.0/15.0) * chi;
 5016    /* there is also a 1.5PN term with eta, but it is negative so do not include it */
 5017    double c4 = XLALSimInspiralTaylorT2Timing_4PNCoeff(eta);
 5018    double v = cbrt(LAL_PI * LAL_G_SI * M * fstart) / LAL_C_SI;
 5019    return c0 * pow(v, -8) * (1.0 + (c2 + (c3 + c4 * v) * v) * v * v);
 5020}
 5021 
 5022/**
 5023 * @brief Routine to compute an overestimate of the merger time.
 5024 * @details
 5025 * This routine provides an upper bound on the time it will take for compact
 5026 * binaries to plunge and merge at the end of the quasi-stationary inspiral.
 5027 * This is quite vague since the notion of a innermost stable circular orbit
 5028 * is ill-defined except in a test mass limit. Nevertheless, this routine
 5029 * assumes (i) that the innermost stable circular orbit occurs at v = c / 3,
 5030 * or r = 9 G M / c^3 (in Boyer-Lindquist coordinates), which is roughly right
 5031 * for an extreme Kerr black hole counter-rotating with a test particle,
 5032 * and (ii) the plunge lasts for a shorter period than one cycle at this
 5033 * innermost stable circular orbit.
 5034 * @param m1 The mass of the first component in kg.
 5035 * @param m2 The mass of the second component in kg.
 5036 * @return Upper bound on the merger time in seconds.
 5037 */
 5038REAL8 XLALSimInspiralMergeTimeBound(REAL8 m1, REAL8 m2)
 5039{
 5040    const double norbits = 1;
 5041    double M = m1 + m2; // total mass
 5042    double r = 9.0 * M * LAL_MRSUN_SI / LAL_MSUN_SI;
 5043    double v = LAL_C_SI / 3.0;
 5044    return norbits * (2.0 * LAL_PI * r / v);
 5045}
 5046 
 5047/**
 5048 * @brief Routine to compute an overestimate of the ringdown time.
 5049 * @details
 5050 * This routine provides an upper bound on the time it will take for a
 5051 * black hole produced by compact binary merger to ring down through
 5052 * quasinormal mode radiation.  An approximate formula for the frequency
 5053 * and quality of the longest-lived fundamental (n=0) dominant (l=m=2)
 5054 * quasinormal mode * is given by Eqs. (E1) and (E2) along with Table VIII
 5055 * of Berti, Cardoso, and Will, Physical Review D (2006) 064030.
 5056 * Waveform generators produce 10 e-folds of ringdown radiation, so
 5057 * this routine goes up to 11 to provide an over-estimate of the ringdown time.
 5058 * @param M The mass of the final black hole in kg.
 5059 * @param s The dimensionless spin of the final black hole.
 5060 * @return Upper bound on the merger time in seconds.
 5061 * @see Emanuele Berti, Vitor Cardoso, and Clifford M. Will, Physical Review D 73, 064030 (2006) DOI: 10.1103/PhysRevD.73.064030
 5062 */
 5063REAL8 XLALSimInspiralRingdownTimeBound(REAL8 M, REAL8 s)
 5064{
 5065    const double nefolds = 11; /* waveform generators only go up to 10 */
 5066 
 5067    /* these values come from Table VIII of Berti, Cardoso, and Will with n=0, m=2 */
 5068    const double f1 = +1.5251;
 5069    const double f2 = -1.1568;
 5070    const double f3 = +0.1292;
 5071    const double q1 = +0.7000;
 5072    const double q2 = +1.4187;
 5073    const double q3 = -0.4990;
 5074 
 5075    double omega = (f1 + f2 * pow(1.0 - s, f3)) / (M * LAL_MTSUN_SI / LAL_MSUN_SI);
 5076    double Q = q1 + q2 * pow(1.0 - s, q3);
 5077    double tau = 2.0 * Q / omega; /* see Eq. (2.1) of Berti, Cardoso, and Will */
 5078    return nefolds * tau;
 5079}
 5080 
 5081/**
 5082 * @brief Routine to compute an overestimate of a final black hole dimensionless spin.
 5083 * @details
 5084 * This routine provides an upper bound on the dimensionless spin of a black
 5085 * hole produced in a compact binary merger.  Uses the formula in Tichy and
 5086 * Marronetti, Physical Review D 78 081501 (2008), Eq. (1) and Table 1, for
 5087 * equal mass black holes, or the larger of the two spins (which covers the
 5088 * extreme mass case).  If the result is larger than a maximum realistic
 5089 * black hole spin, truncate at this maximum value.
 5090 * @param S1z The z-component of the dimensionless spin of body 1.
 5091 * @param S2z The z-component of the dimensionless spin of body 2.
 5092 * @return Upper bound on final black hole dimensionless spin.
 5093 * @see Tichy and Marronetti, Physical Review D 78 081501 (2008).
 5094 * @todo It has been suggested that Barausse, Rezzolla (arXiv: 0904.2577) is
 5095 * more accurate
 5096 */
 5097REAL8 XLALSimInspiralFinalBlackHoleSpinBound(REAL8 S1z, REAL8 S2z)
 5098{
 5099    const double maximum_black_hole_spin = 0.998;
 5100    double s;
 5101    /* lower bound on the final plunge, merger, and ringdown time here the
 5102     * final black hole spin is overestimated by using the formula in Tichy and
 5103     * Marronetti, Physical Review D 78 081501 (2008), Eq. (1) and Table 1, for
 5104     * equal mass black holes, or the larger of the two spins (which covers the
 5105     * extreme mass case) */
 5106    /* TODO: it has been suggested that Barausse, Rezzolla (arXiv: 0904.2577)
 5107     * is more accurate */
 5108    s = 0.686 + 0.15 * (S1z + S2z);
 5109    if (s < fabs(S1z))
 5110        s = fabs(S1z);
 5111    if (s < fabs(S2z))
 5112        s = fabs(S2z);
 5113    /* it is possible that |S1z| or |S2z| >= 1, but s must be less than 1
 5114     * (0th law of thermodynamics) so provide a maximum value for s */
 5115    if (s > maximum_black_hole_spin)
 5116        s = maximum_black_hole_spin;
 5117    return s;
 5118}
 5119 
 5120/**
 5121 * @brief Routine to compute an underestimate of the starting frequency for a given chirp time.
 5122 * @details
 5123 * This routine estimates a start frequency for a binary inspiral from which the
 5124 * actual inspiral chirp time will be shorter than the specified chirp time.
 5125 * To obtain this estimate, only the leading order Newtonian coefficient is used.
 5126 * The frequency returned by this routine is guaranteed to be less than the frequency
 5127 * passed to XLALSimInspiralChirpTimeBound() if the returned value of that routine
 5128 * is passed to this routine as tchirp.
 5129 * @param tchirp The chirp time of post-Newtonian inspiral s.
 5130 * @param m1 The mass of the first component in kg.
 5131 * @param m2 The mass of the second component in kg.
 5132 * @return Lower bound on the starting frequency of a post-Newtonian inspiral in Hz.
 5133 */
 5134REAL8 XLALSimInspiralChirpStartFrequencyBound(REAL8 tchirp, REAL8 m1, REAL8 m2)
 5135{
 5136    double M = m1 + m2; // total mass
 5137    double mu = m1 * m2 / M; // reduced mass
 5138    double eta = mu / M; // symmetric mass ratio
 5139    double c0 = XLALSimInspiralTaylorT3Frequency_0PNCoeff(M);
 5140    return c0 * pow(5.0 * M * (LAL_MTSUN_SI / LAL_MSUN_SI) / (eta * tchirp), 3.0 / 8.0);
 5141}
 5142 
 5143/**
 5144 * Function that gives the value of the desired frequency given some physical parameters
 5145 *
 5146 */
 5147double XLALSimInspiralGetFrequency(
 5148    REAL8 m1,                   /**< mass of companion 1 (kg) */
 5149    REAL8 m2,                   /**< mass of companion 2 (kg) */
 5150    const REAL8 S1x,            /**< x-component of the dimensionless spin of object 1 */
 5151    const REAL8 S1y,            /**< y-component of the dimensionless spin of object 1 */
 5152    const REAL8 S1z,            /**< z-component of the dimensionless spin of object 1 */
 5153    const REAL8 S2x,            /**< x-component of the dimensionless spin of object 2 */
 5154    const REAL8 S2y,            /**< y-component of the dimensionless spin of object 2 */
 5155    const REAL8 S2z,            /**< z-component of the dimensionless spin of object 2 */
 5156    FrequencyFunction freqFunc  /**< name of the function to use */
 5157    )
 5158{
 5159 
 5160    double freq; /* The return value */
 5161 
 5162    /* Variables needed for fIMRPhenom(x) */
 5163    double chi;
 5164    double m1Msun = m1 / LAL_MSUN_SI;
 5165    double m2Msun = m2 / LAL_MSUN_SI;
 5166 
 5167    /* Variables needed for f(S)EOBNRv(x) */
 5168    UINT4 SpinAlignedEOBVersion;
 5169    Approximant approximant;
 5170    REAL8 spin1[3];
 5171    REAL8 spin2[3];
 5172    int     modeL;
 5173    int     modeM;
 5174    COMPLEX16Vector modefreqVec;
 5175    COMPLEX16      modeFreq;
 5176 
 5177    switch (freqFunc)
 5178    {
 5179        case fSchwarzISCO:
 5180            /* Schwarzschild ISCO */
 5181            freq = pow(LAL_C_SI,3) / (pow(6.,3./2.)*LAL_PI*(m1+m2)*LAL_G_SI);
 5182            break;
 5183        case fIMRPhenomAFinal:
 5184            freq = XLALSimIMRPhenomAGetFinalFreq(m1Msun, m2Msun);
 5185            break;
 5186        case fIMRPhenomBFinal:
 5187            chi = XLALSimIMRPhenomBComputeChi(m1Msun, m2Msun, S1z, S2z);
 5188            freq = XLALSimIMRPhenomBGetFinalFreq(m1Msun, m2Msun, chi);
 5189            break;
 5190        case fIMRPhenomCFinal:
 5191            chi = XLALSimIMRPhenomBComputeChi(m1Msun, m2Msun, S1z, S2z);
 5192            freq = XLALSimIMRPhenomCGetFinalFreq(m1Msun, m2Msun, chi);
 5193            break;
 5194        case fIMRPhenomDPeak:
 5195            freq = XLALIMRPhenomDGetPeakFreq(m1Msun, m2Msun, S1z, S2z);
 5196            break;
 5197 
 5198        /* EOBNR ringdown frequencies all come from the same code,
 5199         * just with different inputs */
 5200        case fEOBNRv2HMRD:
 5201        case fEOBNRv2RD:
 5202        case fSEOBNRv1RD:
 5203        case fSEOBNRv2RD:
 5204        case fSEOBNRv4RD:
 5205            // FIXME: Probably shouldn't hard code the modes.
 5206            if ( freqFunc == fEOBNRv2HMRD )
 5207            {
 5208                modeL = 5;
 5209                modeM = 5;
 5210                approximant = EOBNRv2HM;
 5211            }
 5212            else
 5213            {
 5214                modeL = 2;
 5215                modeM = 2;
 5216                if (freqFunc == fEOBNRv2RD) approximant = EOBNRv2;
 5217                if (freqFunc == fSEOBNRv1RD) approximant = SEOBNRv1;
 5218                if (freqFunc == fSEOBNRv2RD) approximant = SEOBNRv2;
 5219                if (freqFunc == fSEOBNRv4RD) approximant = SEOBNRv4;
 5220            }
 5221            if ( freqFunc == fEOBNRv2RD || freqFunc == fEOBNRv2HMRD )
 5222            {
 5223                /* Check that spins are zero */
 5224                if( !checkSpinsZero(S1x, S1y, S1z, S2x, S2y, S2z) )
 5225                {
 5226                    XLALPrintError("Non-zero spins were given, but EOBNRv2 ringdown frequencies do not depend on spin.\n");
 5227                    XLAL_ERROR(XLAL_EINVAL);
 5228                spin1[0] = 0.; spin1[1] = 0.; spin1[2] = 0.;
 5229                spin2[0] = 0.; spin2[1] = 0.; spin2[2] = 0.;
 5230                }
 5231            }
 5232            else
 5233            {
 5234                spin1[0] = S1x; spin1[1] = S1y; spin1[2] = S1z;
 5235                spin2[0] = S2x; spin2[1] = S2y; spin2[2] = S2z;
 5236            }
 5237 
 5238            modefreqVec.length = 1;
 5239            modefreqVec.data   = &modeFreq;
 5240            if ( XLALSimIMREOBGenerateQNMFreqV2( &modefreqVec, m1Msun, m2Msun, spin1, spin2, modeL, modeM, 1, approximant) != XLAL_SUCCESS )
 5241            {
 5242                XLAL_ERROR( XLAL_EFUNC );
 5243            }
 5244 
 5245            freq = creal(modeFreq) / (2 * LAL_PI);
 5246            break;
 5247 
 5248        case fSEOBNRv5RD:
 5249            modeL = 2;
 5250            modeM = 2;
 5251            approximant = SEOBNRv5_ROM;
 5252            spin1[0] = S1x; spin1[1] = S1y; spin1[2] = S1z;
 5253            spin2[0] = S2x; spin2[1] = S2y; spin2[2] = S2z;
 5254            modefreqVec.length = 1;
 5255            modefreqVec.data   = &modeFreq;
 5256            if ( XLALSimIMREOBGenerateQNMFreqV5( &modefreqVec, m1Msun, m2Msun, spin1, spin2, modeL, modeM, 1, approximant) != XLAL_SUCCESS )
 5257            {
 5258                XLAL_ERROR( XLAL_EFUNC );
 5259            }
 5260 
 5261            freq = creal(modeFreq) / (2 * LAL_PI);
 5262            break;
 5263 
 5264        case fSEOBNRv1Peak:
 5265        case fSEOBNRv2Peak:
 5266        case fSEOBNRv4Peak:
 5267        case fSEOBNRv5Peak:
 5268            if ( freqFunc == fSEOBNRv1Peak ) SpinAlignedEOBVersion = 1;
 5269            if ( freqFunc == fSEOBNRv2Peak ) SpinAlignedEOBVersion = 2;
 5270            if ( freqFunc == fSEOBNRv4Peak ) SpinAlignedEOBVersion = 4;
 5271            if ( freqFunc == fSEOBNRv5Peak ) SpinAlignedEOBVersion = 5;
 5272            freq = XLALSimIMRSpinAlignedEOBPeakFrequency(m1, m2, S1z, S2z,
 5273                    SpinAlignedEOBVersion);
 5274            break;
 5275        case fTEOBResumSFinal: // MA: Replace with TEOB-related RD frequency!
 5276                               // CAUTION: different function for BNS/NSBH/BBH cases?
 5277            fprintf(stdout, "Final frequency for TEOBResumS not implemented yet.\n");
 5278            freq = XLALSimIMRSpinAlignedEOBPeakFrequency(m1, m2, S1z, S2z, 2);
 5279            break;
 5280        default:
 5281            XLALPrintError("Unsupported approximant\n");
 5282            XLAL_ERROR(XLAL_EINVAL);
 5283    }
 5284 
 5285    return freq;
 5286}
 5287 
 5288 
 5289/**
 5290 * Function that gives the default ending frequencies of the given approximant.
 5291 *
 5292 */
 5293double XLALSimInspiralGetFinalFreq(
 5294    REAL8 m1,                               /**< mass of companion 1 (kg) */
 5295    REAL8 m2,                               /**< mass of companion 2 (kg) */
 5296    const REAL8 S1x,                              /**< x-component of the dimensionless spin of object 1 */
 5297    const REAL8 S1y,                              /**< y-component of the dimensionless spin of object 1 */
 5298    const REAL8 S1z,                              /**< z-component of the dimensionless spin of object 1 */
 5299    const REAL8 S2x,                              /**< x-component of the dimensionless spin of object 2 */
 5300    const REAL8 S2y,                              /**< y-component of the dimensionless spin of object 2 */
 5301    const REAL8 S2z,                              /**< z-component of the dimensionless spin of object 2 */
 5302    Approximant approximant                 /**< post-Newtonian approximant to use for waveform production */
 5303    )
 5304{
 5305    FrequencyFunction freqFunc;
 5306 
 5307    /* input conditions */
 5308    switch (approximant)
 5309    {
 5310        case EccentricTD:
 5311        case EccentricFD:
 5312        case EOBNRv2HM:
 5313        case EOBNRv2:
 5314        case IMRPhenomA:
 5315            /* Check that spins are zero */
 5316            if( !checkSpinsZero(S1x, S1y, S1z, S2x, S2y, S2z) )
 5317            {
 5318                XLALPrintError("Non-zero spins were given, but this is a non-spinning approximant.\n");
 5319                XLAL_ERROR(XLAL_EINVAL);
 5320            }
 5321            break;
 5322 
 5323        case TaylorF2RedSpinTidal:
 5324        case SEOBNRv1:
 5325        case SEOBNRv2:
 5326        case SEOBNRv2_opt:
 5327        case SEOBNRv4:
 5328        case SEOBNRv4_opt:
 5329        case IMRPhenomB:
 5330        case IMRPhenomC:
 5331        case TEOBResumS:
 5332            /* Check that the transverse spins are zero */
 5333            if( !checkTransverseSpinsZero(S1x, S1y, S2x, S2y) )
 5334            {
 5335                XLALPrintError("Non-zero transverse spins were given, but this is a non-precessing approximant.\n");
 5336                XLAL_ERROR(XLAL_EINVAL);
 5337            }
 5338            break;
 5339 
 5340        default:
 5341            break;
 5342    }
 5343 
 5344    /* select the frequency function that is associated with each approximant */
 5345    switch (approximant)
 5346    {
 5347        /* non-spinning inspiral-only models */
 5348        // CHECKME: do they really all use Schwarzschild ISCO? */
 5349        case TaylorEt:
 5350        case TaylorT1:
 5351        case TaylorT2:
 5352        case TaylorT3:
 5353        case TaylorT4:
 5354        case EccentricTD:
 5355        case EccentricFD:
 5356        case TaylorF2:
 5357        case TaylorF2Ecc:
 5358        case TaylorF2NLTides:
 5359        case TaylorF2RedSpin:
 5360        case TaylorF2RedSpinTidal:
 5361            /* Schwarzschild ISCO */
 5362            freqFunc = fSchwarzISCO;
 5363            break;
 5364 
 5365        /* IMR models */
 5366        case EOBNRv2HM:
 5367            freqFunc = fEOBNRv2HMRD;
 5368            break;
 5369 
 5370        case EOBNRv2:
 5371            freqFunc = fEOBNRv2RD;
 5372            break;
 5373 
 5374        case SEOBNRv1:
 5375            freqFunc = fSEOBNRv1RD;
 5376            break;
 5377 
 5378        case SEOBNRv2:
 5379        case SEOBNRv2_opt:
 5380            freqFunc = fSEOBNRv2RD;
 5381            break;
 5382 
 5383        case SEOBNRv4:
 5384        case SEOBNRv4_opt:
 5385            freqFunc = fSEOBNRv4RD;
 5386            break;
 5387 
 5388        case SEOBNRv5_ROM:
 5389            freqFunc = fSEOBNRv5RD;
 5390            break;
 5391 
 5392        case IMRPhenomA:
 5393            freqFunc = fIMRPhenomAFinal;
 5394            break;
 5395 
 5396        case IMRPhenomB:
 5397            freqFunc = fIMRPhenomBFinal;
 5398            break;
 5399 
 5400        case IMRPhenomC:
 5401            freqFunc = fIMRPhenomCFinal;
 5402            break;
 5403 
 5404        case TEOBResumS:
 5405           freqFunc = fTEOBResumSFinal;
 5406       break;
 5407 
 5408        // FIXME: Following I don't know how to calculate */
 5409        /* Spinning inspiral-only time domain */
 5410        case SpinTaylorT5:
 5411        case SpinTaylorT4:
 5412        case SpinTaylorT1:
 5413        case PhenSpinTaylor:
 5414        /* Spinning with ringdown attachment */
 5415        case PhenSpinTaylorRD:
 5416        /* Spinning inspiral-only frequency domain */
 5417        case SpinTaylorF2:
 5418        /* NR waveforms */
 5419        case NR_hdf5:
 5420        case NRSur4d2s:
 5421            XLALPrintError("I don't know how to calculate final freq. for this approximant, sorry!\n");
 5422            XLAL_ERROR(XLAL_EINVAL);
 5423            break;
 5424 
 5425        default:
 5426            XLALPrintError("Unsupported approximant\n");
 5427            XLAL_ERROR(XLAL_EINVAL);
 5428    }
 5429 
 5430    return XLALSimInspiralGetFrequency(m1, m2, S1x, S1y, S1z, S2x, S2y, S2z, freqFunc);
 5431}
 5432 
 5433/** @} */
 5434 
 5435/**
 5436 * @name Waveform Conditioning Helper Routines
 5437 * @{
 5438 */
 5439 
 5440/**
 5441 * @brief First stage of conditioning of time-domain waveforms.
 5442 * @details
 5443 * The conditioning of time-domain waveforms is done in two stages:
 5444 *
 5445 * 1. Take a waveform that is generated so that begins a time at least textra
 5446 * before it reaches f_min and apply a taper over this duration textra; follow
 5447 * this up by high-pass filtering the data at frequency f_min; finally, if the
 5448 * original waveform was zero-padded, strip off this padding.
 5449 *
 5450 * 2. The high-pass filtered waveform might have transients remaining at the
 5451 * beginning and at the end; furthermore, the waveform might end at a non-zero
 5452 * value (especially for non-IMR waveforms).  The second stage tapers one
 5453 * cycle at f_min from the beginning of the waveform and one cycle at f_max
 5454 * from the end of the waveform.  There is a minimum number of samples that
 5455 * will be used in the tapering and if the waveform is shorter than twice
 5456 * this minimum number then no Stage 2 conditioning is done.
 5457 *
 5458 * This routine performs Stage 1 conditioning.  This stage is only performed
 5459 * for waveforms originally produced in the time domain.  (Frequency domain
 5460 * waveforms that have been transformed into the time domain have a different
 5461 * Stage 1 conditioning.)
 5462 *
 5463 * @param hplus  Pointer to the plus-polarization timeseries.
 5464 * @param hcross Pointer to the cross-polarization timeseries.
 5465 * @param textra Extra time at beginning of waveform to taper (s).
 5466 * @param f_min  Minimum frequency for high-pass filtering (Hz).
 5467 * @retval  0 Success.
 5468 * @retval <0 Failure.
 5469 */
 5470int XLALSimInspiralTDConditionStage1(REAL8TimeSeries *hplus, REAL8TimeSeries *hcross, REAL8 textra, REAL8 f_min)
 5471{
 5472    size_t nzeros;
 5473    size_t ntaper;
 5474    size_t j;
 5475 
 5476    /* some generators zero-pad the end of the waveform: will remove this */
 5477    nzeros = 0;
 5478    while (hplus->data->data[hplus->data->length - nzeros - 1] == 0.0 && hcross->data->data[hcross->data->length - nzeros - 1] == 0.0)
 5479        ++nzeros;
 5480 
 5481    /* apply tapers over the extra duration at the beginning */
 5482    ntaper = round(textra / hplus->deltaT);
 5483    for (j = 0; j < ntaper; ++j) {
 5484        double w = 0.5 - 0.5 * cos(j * LAL_PI / ntaper);
 5485        hplus->data->data[j] *= w;
 5486        hcross->data->data[j] *= w;
 5487    }
 5488 
 5489    /* apply time domain filter at f_min */
 5490    XLALHighPassREAL8TimeSeries(hplus, f_min, 0.99, 8);
 5491    XLALHighPassREAL8TimeSeries(hcross, f_min, 0.99, 8);
 5492 
 5493    /* now take off the zero padded end */
 5494    if (nzeros) {
 5495        XLALShrinkREAL8TimeSeries(hplus, 0, hplus->data->length - nzeros);
 5496        XLALShrinkREAL8TimeSeries(hcross, 0, hcross->data->length - nzeros);
 5497    }
 5498 
 5499    return 0;
 5500}
 5501 
 5502/**
 5503 * @brief Second stage of conditioning of time-domain waveforms.
 5504 * @details
 5505 * The conditioning of time-domain waveforms is done in two stages:
 5506 *
 5507 * 1. Take a waveform that is generated so that begins a time at least textra
 5508 * before it reaches f_min and apply a taper over this duration textra; follow
 5509 * this up by high-pass filtering the data at frequency f_min; finally, if the
 5510 * original waveform was zero-padded, strip off this padding.
 5511 *
 5512 * 2. The high-pass filtered waveform might have transients remaining at the
 5513 * beginning and at the end; furthermore, the waveform might end at a non-zero
 5514 * value (especially for non-IMR waveforms).  The second stage tapers one
 5515 * cycle at f_min from the beginning of the waveform and one cycle at f_max
 5516 * from the end of the waveform.  There is a minimum number of samples that
 5517 * will be used in the tapering and if the waveform is shorter than twice
 5518 * this minimum number then no Stage 2 conditioning is done.
 5519 *
 5520 * This routine performs Stage 2 conditioning.  This stage is performed both
 5521 * for waveforms originally produced in the time domain, and for waveforms that
 5522 * were originally produced in the frequency domain and then transformed to
 5523 * the time domain. This stage follows some form of Stage 1 conditioning,
 5524 * which is different depending on whether the original waveform was generated
 5525 * in the time domain or in the frequency domain.
 5526 *
 5527 * @param hplus  Pointer to the plus-polarization timeseries.
 5528 * @param hcross Pointer to the cross-polarization timeseries.
 5529 * @param f_min  Minimum frequency for tapering at the start (Hz).
 5530 * @param f_max  Minimum frequency for tapering at the end (Hz).
 5531 * @retval  0 Success.
 5532 * @retval <0 Failure.
 5533 */
 5534int XLALSimInspiralTDConditionStage2(REAL8TimeSeries *hplus, REAL8TimeSeries *hcross, REAL8 f_min, REAL8 f_max)
 5535{
 5536    const size_t min_taper_samples = 4;
 5537    size_t ntaper;
 5538    size_t j;
 5539 
 5540    /* final tapering at the beginning and at the end */
 5541    /* if this waveform is shorter than 2*min_taper_samples, do nothing */
 5542    if (hplus->data->length < 2 * min_taper_samples) {
 5543        XLAL_PRINT_WARNING("waveform is too shorter than %zu samples: no final tapering applied", 2 * min_taper_samples);
 5544        return 0;
 5545    }
 5546 
 5547    /* taper end of waveform: 1 cycle at f_max; at least min_taper_samples
 5548     * note: this tapering is done so the waveform goes to zero at the next
 5549     * point beyond the end of the data */
 5550    ntaper = round(1.0 / (f_max * hplus->deltaT));
 5551    if (ntaper < min_taper_samples)
 5552        ntaper = min_taper_samples;
 5553    for (j = 1; j < ntaper; ++j) {
 5554        double w = 0.5 - 0.5 * cos(j * LAL_PI / ntaper);
 5555        hplus->data->data[hplus->data->length - j] *= w;
 5556        hcross->data->data[hcross->data->length - j] *= w;
 5557    }
 5558 
 5559    /* there could be a filter transient at the beginning too: we should have
 5560     * some safety there owing to the fact that we are starting at a lower
 5561     * frequency than is needed, so taper off one cycle at the low frequency */
 5562    ntaper = round(1.0 / (f_min * hplus->deltaT));
 5563    if (ntaper < min_taper_samples)
 5564        ntaper = min_taper_samples;
 5565    for (j = 0; j < ntaper; ++j) {
 5566        double w = 0.5 - 0.5 * cos(j * LAL_PI / ntaper);
 5567        hplus->data->data[j] *= w;
 5568        hcross->data->data[j] *= w;
 5569    }
 5570 
 5571    return 0;
 5572}
 5573 
 5574 
 5575/**
 5576 * @brief Function for determining the starting frequency
 5577 * of the (2,2) mode when the highest order contribution starts at fLow.
 5578 * @details
 5579 * Compute the minimum frequency for waveform generation
 5580 *  using amplitude orders above Newtonian.  The waveform
 5581 *  generator turns on all orders at the orbital
 5582 *  associated with fMin, so information from higher
 5583 *  orders is not included at fLow unless fMin is
 5584 *  sufficiently low.
 5585 *
 5586 * @param fLow  Requested lower frequency.
 5587 * @param ampOrder Requested amplitude order.
 5588 * @param approximant LALApproximant
 5589 * @retval fStart The lower frequency to use to include corrections.
 5590 */
 5591REAL8 XLALSimInspiralfLow2fStart(REAL8 fLow, INT4 ampOrder, INT4 approximant)
 5592{
 5593  if (ampOrder == -1) {
 5594      if (approximant == SpinTaylorT5 || approximant == SpinTaylorT4)
 5595          ampOrder = MAX_PRECESSING_AMP_PN_ORDER;
 5596      else
 5597          ampOrder = MAX_NONPRECESSING_AMP_PN_ORDER;
 5598  }
 5599 
 5600    REAL8 fStart;
 5601    fStart = fLow * 2./(ampOrder+2);
 5602    return fStart;
 5603}
 5604 
 5605/**
 5606 * @deprecated Use XLALSimInspiralChooseTDWaveform() instead
 5607 * Chooses between different approximants when requesting a waveform to be generated
 5608 * For spinning waveforms, all known spin effects up to given PN order are included
 5609 * Returns the waveform in the time domain.
 5610 *
 5611 * The parameters passed must be in SI units.
 5612 */
 5613int XLALSimInspiralChooseTDWaveformOLD(
 5614    REAL8TimeSeries **hplus,                    /**< +-polarization waveform */
 5615    REAL8TimeSeries **hcross,                   /**< x-polarization waveform */
 5616    const REAL8 m1,                             /**< mass of companion 1 (kg) */
 5617    const REAL8 m2,                             /**< mass of companion 2 (kg) */
 5618    const REAL8 S1x,                            /**< x-component of the dimensionless spin of object 1 */
 5619    const REAL8 S1y,                            /**< y-component of the dimensionless spin of object 1 */
 5620    const REAL8 S1z,                            /**< z-component of the dimensionless spin of object 1 */
 5621    const REAL8 S2x,                            /**< x-component of the dimensionless spin of object 2 */
 5622    const REAL8 S2y,                            /**< y-component of the dimensionless spin of object 2 */
 5623    const REAL8 S2z,                            /**< z-component of the dimensionless spin of object 2 */
 5624    const REAL8 distance,                       /**< distance of source (m) */
 5625    const REAL8 inclination,                    /**< inclination of source (rad) */
 5626    const REAL8 phiRef,                         /**< reference orbital phase (rad) */
 5627    const REAL8 longAscNodes,                   /**< longitude of ascending nodes, degenerate with the polarization angle, Omega in documentation */
 5628    const REAL8 eccentricity,                   /**< eccentrocity at reference epoch */
 5629    const REAL8 UNUSED meanPerAno,              /**< mean anomaly of periastron */
 5630    // frequency sampling parameters, no default value
 5631    const REAL8 deltaT,                         /**< sampling interval (s) */
 5632    const REAL8 f_min,                          /**< starting GW frequency (Hz) */
 5633    REAL8 f_ref,                                /**< reference GW frequency (Hz) */
 5634    const REAL8 lambda1,                        /**< (tidal deformability of mass 1) / m1^5 (dimensionless) */
 5635    const REAL8 lambda2,                        /**< (tidal deformability of mass 2) / m2^5 (dimensionless) */
 5636    const REAL8 dQuadParam1,                    /**< (quad-monop parameter of mass 1) / m1^5 -1 (dimensionless), give 0 for BHs */
 5637    const REAL8 dQuadParam2,                    /**< (quad-monop parameter of mass 2) / m2^5 -1 (dimensionless), give 0 for BHs */
 5638    LALSimInspiralWaveformFlags *waveFlags,     /**< Set of flags to control special behavior of some waveform families. Pass in NULL (or None in python) for default flags */
 5639    LALSimInspiralTestGRParam *nonGRparams,     /**< Linked list of non-GR parameters. Pass in NULL (or None in python) for standard GR waveforms */
 5640    int amplitudeO,                             /**< twice post-Newtonian amplitude order */
 5641    const int phaseO,                           /**< twice post-Newtonian order */
 5642    const Approximant approximant               /**< post-Newtonian approximant to use for waveform production */
 5643    )
 5644{
 5645    LALDict *LALparams = NULL;
 5646    REAL8 LNhatx, LNhaty, LNhatz, E1x, E1y, E1z;
 5647    char *numrel_data_path;
 5648    //REAL8 tmp1, tmp2;
 5649    int ret;
 5650    /* N.B. the quadrupole of a spinning compact body labeled by A is
 5651     * Q_A = - quadparam_A chi_A^2 m_A^3 (see gr-qc/9709032)
 5652     * where quadparam = 1 for BH ~= 4-8 for NS.
 5653     * This affects the quadrupole-monopole interaction.
 5654     */
 5655    REAL8 v0 = 1., quadparam1 = 1.+dQuadParam1, quadparam2 = 1.+dQuadParam2;
 5656 
 5657    /* General sanity checks that will abort
 5658     *
 5659     * If non-GR approximants are added, include them in
 5660     * XLALSimInspiralApproximantAcceptTestGRParams()
 5661     */
 5662    if( nonGRparams && XLALSimInspiralApproximantAcceptTestGRParams(approximant) != LAL_SIM_INSPIRAL_TESTGR_PARAMS )
 5663    {
 5664        XLALPrintError("XLAL Error - %s: Passed in non-NULL pointer to LALSimInspiralTestGRParam for an approximant that does not use LALSimInspiralTestGRParam\n", __func__);
 5665        XLAL_ERROR(XLAL_EINVAL);
 5666    }
 5667 
 5668    /* Support variables for precessing wfs*/
 5669    REAL8 incl;
 5670 
 5671    UINT4 PrecEOBversion;
 5672 
 5673    /* SEOBNR flag for model version. 1 for SEOBNRv1, 2 for SEOBNRv2 */
 5674    UINT4 SpinAlignedEOBversion;
 5675    REAL8 spin1x,spin1y,spin1z;
 5676    REAL8 spin2x,spin2y,spin2z;
 5677    REAL8 polariz=longAscNodes;
 5678    //LIGOTimeGPS epoch = LIGOTIMEGPSZERO;
 5679 
 5680    /* General sanity check the input parameters - only give warnings! */
 5681    if( deltaT > 1. )
 5682        XLALPrintWarning("XLAL Warning - %s: Large value of deltaT = %e requested.\nPerhaps sample rate and time step size were swapped?\n", __func__, deltaT);
 5683    if( deltaT < 1./16385. )
 5684        XLALPrintWarning("XLAL Warning - %s: Small value of deltaT = %e requested.\nCheck for errors, this could create very large time series.\n", __func__, deltaT);
 5685    if( m1 < 0.09 * LAL_MSUN_SI )
 5686        XLALPrintWarning("XLAL Warning - %s: Small value of m1 = %e (kg) = %e (Msun) requested.\nPerhaps you have a unit conversion error?\n", __func__, m1, m1/LAL_MSUN_SI);
 5687    if( m2 < 0.09 * LAL_MSUN_SI )
 5688        XLALPrintWarning("XLAL Warning - %s: Small value of m2 = %e (kg) = %e (Msun) requested.\nPerhaps you have a unit conversion error?\n", __func__, m2, m2/LAL_MSUN_SI);
 5689    if( m1 + m2 > 1000. * LAL_MSUN_SI )
 5690        XLALPrintWarning("XLAL Warning - %s: Large value of total mass m1+m2 = %e (kg) = %e (Msun) requested.\nSignal not likely to be in band of ground-based detectors.\n", __func__, m1+m2, (m1+m2)/LAL_MSUN_SI);
 5691    if( S1x*S1x + S1y*S1y + S1z*S1z > 1.000001 )
 5692        XLALPrintWarning("XLAL Warning - %s: S1 = (%e,%e,%e) with norm > 1 requested.\nAre you sure you want to violate the Kerr bound?\n", __func__, S1x, S1y, S1z);
 5693    if( S2x*S2x + S2y*S2y + S2z*S2z > 1.000001 )
 5694        XLALPrintWarning("XLAL Warning - %s: S2 = (%e,%e,%e) with norm > 1 requested.\nAre you sure you want to violate the Kerr bound?\n", __func__, S2x, S2y, S2z);
 5695    if( f_min < 1. )
 5696        XLALPrintWarning("XLAL Warning - %s: Small value of fmin = %e requested.\nCheck for errors, this could create a very long waveform.\n", __func__, f_min);
 5697    if( f_min > 40.000001 )
 5698        XLALPrintWarning("XLAL Warning - %s: Large value of fmin = %e requested.\nCheck for errors, the signal will start in band.\n", __func__, f_min);
 5699 
 5700    /* adjust the reference frequency for certain precessing approximants:
 5701     * if that approximate interprets f_ref==0 to be f_min, set f_ref=f_min;
 5702     * otherwise do nothing */
 5703    FIX_REFERENCE_FREQUENCY(f_ref, f_min, approximant);
 5704 
 5705    switch (approximant)
 5706    {
 5707        /* non-spinning inspiral-only models */
 5708        case TaylorEt:
 5709            /* Waveform-specific sanity checks */
 5710            if( !XLALSimInspiralWaveformFlagsIsDefaultOLD(waveFlags) )
 5711                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralWaveformFlags given, but this approximant does not support this case.");
 5712            if( !checkSpinsZero(S1x, S1y, S1z, S2x, S2y, S2z) )
 5713                XLAL_ERROR(XLAL_EINVAL, "Non-zero spins were given, but this is a non-spinning approximant.");
 5714            if( !checkTidesZero(lambda1, lambda2) )
 5715                XLAL_ERROR(XLAL_EINVAL, "Non-zero tidal parameters were given, but this is approximant doe not have tidal corrections.");
 5716            if( f_ref != 0.)
 5717                XLALPrintWarning("XLAL Warning - %s: This approximant does use f_ref. The reference phase will be defined at coalescence.\n", __func__);
 5718            /* Call the waveform driver routine */
 5719            ret = XLALSimInspiralTaylorEtPNGenerator(hplus, hcross, phiRef, v0,
 5720                    deltaT, m1, m2, f_min, distance, inclination, amplitudeO, phaseO);
 5721            break;
 5722 
 5723        case TaylorT1:
 5724            /* Waveform-specific sanity checks */
 5725            if( !XLALSimInspiralFrameAxisIsDefault( XLALSimInspiralGetFrameAxis(waveFlags)) )
 5726                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralFrameAxis provided, but this approximant does not use that flag.");
 5727            if( !XLALSimInspiralModesChoiceIsDefault( XLALSimInspiralGetModesChoice(waveFlags)) )
 5728                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralModesChoice provided, but this approximant does not use that flag.");
 5729            if( !XLALSimInspiralSpinOrderIsDefault( XLALSimInspiralGetSpinOrder(waveFlags)) )
 5730                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralSpinOrder provided, but this approximant does not use that flag.");
 5731            if( !checkSpinsZero(S1x, S1y, S1z, S2x, S2y, S2z) )
 5732                XLAL_ERROR(XLAL_EINVAL, "Non-zero spins were given, but this is a non-spinning approximant.");
 5733            /* Call the waveform driver routine */
 5734            ret = XLALSimInspiralTaylorT1PNGenerator(hplus, hcross, phiRef, v0,
 5735                    deltaT, m1, m2, f_min, f_ref, distance, inclination, lambda1, lambda2,
 5736                    0, amplitudeO, phaseO);
 5737            break;
 5738 
 5739        case TaylorT2:
 5740            /* Waveform-specific sanity checks */
 5741            if( !XLALSimInspiralFrameAxisIsDefault( XLALSimInspiralGetFrameAxis(waveFlags)) )
 5742                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralFrameAxis provided, but this approximant does not use that flag.");
 5743            if( !XLALSimInspiralModesChoiceIsDefault( XLALSimInspiralGetModesChoice(waveFlags)) )
 5744                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralModesChoice provided, but this approximant does not use that flag.");
 5745            if( !XLALSimInspiralSpinOrderIsDefault( XLALSimInspiralGetSpinOrder(waveFlags)) )
 5746                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralSpinOrder provided, but this approximant does not use that flag.");
 5747            if( !checkSpinsZero(S1x, S1y, S1z, S2x, S2y, S2z) )
 5748                XLAL_ERROR(XLAL_EINVAL, "Non-zero spins were given, but this is a non-spinning approximant.");
 5749            /* Call the waveform driver routine */
 5750            ret = XLALSimInspiralTaylorT2PNGenerator(hplus, hcross, phiRef, v0,
 5751                    deltaT, m1, m2, f_min, f_ref, distance, inclination, lambda1, lambda2,
 5752                    0, amplitudeO, phaseO);
 5753            break;
 5754 
 5755        case TaylorT3:
 5756            /* Waveform-specific sanity checks */
 5757            if( !XLALSimInspiralFrameAxisIsDefault( XLALSimInspiralGetFrameAxis(waveFlags)) )
 5758                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralFrameAxis provided, but this approximant does not use that flag.");
 5759            if( !XLALSimInspiralModesChoiceIsDefault( XLALSimInspiralGetModesChoice(waveFlags)) )
 5760                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralModesChoice provided, but this approximant does not use that flag.");
 5761            if( !XLALSimInspiralSpinOrderIsDefault( XLALSimInspiralGetSpinOrder(waveFlags)) )
 5762                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralSpinOrder provided, but this approximant does not use that flag.");
 5763            if( !checkSpinsZero(S1x, S1y, S1z, S2x, S2y, S2z) )
 5764                XLAL_ERROR(XLAL_EINVAL, "Non-zero spins were given, but this is a non-spinning approximant.");
 5765            /* Call the waveform driver routine */
 5766            ret = XLALSimInspiralTaylorT3PNGenerator(hplus, hcross, phiRef, v0,
 5767                    deltaT, m1, m2, f_min, f_ref, distance, inclination, lambda1, lambda2,
 5768                    0, amplitudeO, phaseO);
 5769            break;
 5770 
 5771        case TaylorT4:
 5772            /* Waveform-specific sanity checks */
 5773            if( !XLALSimInspiralFrameAxisIsDefault( XLALSimInspiralGetFrameAxis(waveFlags)) )
 5774                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralFrameAxis provided, but this approximant does not use that flag.");
 5775            if( !XLALSimInspiralModesChoiceIsDefault( XLALSimInspiralGetModesChoice(waveFlags)) )
 5776                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralModesChoice provided, but this approximant does not use that flag.");
 5777            if( !XLALSimInspiralSpinOrderIsDefault( XLALSimInspiralGetSpinOrder(waveFlags)) )
 5778                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralSpinOrder provided, but this approximant does not use that flag.");
 5779            if( !checkSpinsZero(S1x, S1y, S1z, S2x, S2y, S2z) )
 5780                XLAL_ERROR(XLAL_EINVAL, "Non-zero spins were given, but this is a non-spinning approximant.");
 5781            /* Call the waveform driver routine */
 5782            ret = XLALSimInspiralTaylorT4PNGenerator(hplus, hcross, phiRef, v0,
 5783                    deltaT, m1, m2, f_min, f_ref, distance, inclination, lambda1, lambda2,
 5784                    0, amplitudeO, phaseO);
 5785            break;
 5786 
 5787    case EccentricTD:
 5788        /* Waveform-specific sanity checks */
 5789        if( !XLALSimInspiralFrameAxisIsDefault( XLALSimInspiralGetFrameAxis(waveFlags)) )
 5790                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralFrameAxis provided, but this approximant does not use that flag.");
 5791        if( !XLALSimInspiralModesChoiceIsDefault( XLALSimInspiralGetModesChoice(waveFlags)) )
 5792                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralModesChoice provided, but this approximant does not use that flag.");
 5793        if( !XLALSimInspiralSpinOrderIsDefault( XLALSimInspiralGetSpinOrder(waveFlags)) )
 5794                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralSpinOrder provided, but this approximant does not use that flag.");
 5795        if( !checkSpinsZero(S1x, S1y, S1z, S2x, S2y, S2z) )
 5796                XLAL_ERROR(XLAL_EINVAL, "Non-zero spins were given, but this is a non-spinning approximant.");
 5797            if( !checkTidesZero(lambda1, lambda2) )
 5798        XLAL_ERROR(XLAL_EINVAL, "Non-zero tidal parameters were given, but this is approximant doe not have tidal corrections.");
 5799        /* Call the waveform driver routine */
 5800        ret = XLALSimInspiralEccentricTDPNGenerator(hplus, hcross, phiRef,
 5801            deltaT, m1, m2, f_min, f_ref, distance, inclination, eccentricity,
 5802            amplitudeO, phaseO);
 5803        if (ret == XLAL_FAILURE) XLAL_ERROR(XLAL_EFUNC);
 5804        break;
 5805 
 5806        /* non-spinning inspiral-merger-ringdown models */
 5807        case IMRPhenomA:
 5808            /* Waveform-specific sanity checks */
 5809            if( !XLALSimInspiralWaveformFlagsIsDefaultOLD(waveFlags) )
 5810                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralWaveformFlags given, but this approximant does not support this case.");
 5811            if( !checkSpinsZero(S1x, S1y, S1z, S2x, S2y, S2z) )
 5812                XLAL_ERROR(XLAL_EINVAL, "Non-zero spins were given, but this is a non-spinning approximant.");
 5813            if( !checkTidesZero(lambda1, lambda2) )
 5814                XLAL_ERROR(XLAL_EINVAL, "Non-zero tidal parameters were given, but this is approximant doe not have tidal corrections.");
 5815            if( f_ref != 0.)
 5816                XLALPrintWarning("XLAL Warning - %s: This approximant does use f_ref. The reference phase will be defined at coalescence.\n", __func__);
 5817            /* Call the waveform driver routine */
 5818            // NB: f_max = 0 will generate up to the ringdown cut-off frequency
 5819            ret = XLALSimIMRPhenomAGenerateTD(hplus, hcross, phiRef, deltaT,
 5820                    m1, m2, f_min, 0., distance, inclination);
 5821            break;
 5822 
 5823        case EOBNRv2HM:
 5824            /* Waveform-specific sanity checks */
 5825            if( !XLALSimInspiralWaveformFlagsIsDefaultOLD(waveFlags) )
 5826                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralWaveformFlags given, but this approximant does not support this case.");
 5827            if( !checkSpinsZero(S1x, S1y, S1z, S2x, S2y, S2z) )
 5828                XLAL_ERROR(XLAL_EINVAL, "Non-zero spins were given, but this is a non-spinning approximant.");
 5829            if( !checkTidesZero(lambda1, lambda2) )
 5830                XLAL_ERROR(XLAL_EINVAL, "Non-zero tidal parameters were given, but this is approximant doe not have tidal corrections.");
 5831            if( f_ref != 0.)
 5832                XLALPrintWarning("XLAL Warning - %s: This approximant does use f_ref. The reference phase will be defined at coalescence.\n", __func__);
 5833            /* Call the waveform driver routine */
 5834            // FIXME: need to create a function to take in different modes or produce an error if all modes not given
 5835            ret = XLALSimIMREOBNRv2AllModes(hplus, hcross, phiRef, deltaT,
 5836                    m1, m2, f_min, distance, inclination);
 5837            break;
 5838 
 5839        case EOBNRv2:
 5840            /* Waveform-specific sanity checks */
 5841            if( !XLALSimInspiralWaveformFlagsIsDefaultOLD(waveFlags) )
 5842                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralWaveformFlags given, but this approximant does not support this case.");
 5843            if( !checkSpinsZero(S1x, S1y, S1z, S2x, S2y, S2z) )
 5844                XLAL_ERROR(XLAL_EINVAL, "Non-zero spins were given, but this is a non-spinning approximant.");
 5845            if( !checkTidesZero(lambda1, lambda2) )
 5846                XLAL_ERROR(XLAL_EINVAL, "Non-zero tidal parameters were given, but this is approximant doe not have tidal corrections.");
 5847            if( f_ref != 0.)
 5848                XLALPrintWarning("XLAL Warning - %s: This approximant does use f_ref. The reference phase will be defined at coalescence.\n", __func__);
 5849            /* Call the waveform driver routine */
 5850            ret = XLALSimIMREOBNRv2DominantMode(hplus, hcross, phiRef, deltaT,
 5851                    m1, m2, f_min, distance, inclination);
 5852            break;
 5853 
 5854        /* spinning inspiral-only models */
 5855        case SpinTaylorT5:
 5856            /* Waveform-specific sanity checks */
 5857            /* Sanity check unused fields of waveFlags */
 5858        XLALSimInspiralInitialConditionsPrecessingApproxs(&incl,&spin1x,&spin1y,&spin1z,&spin2x,&spin2y,&spin2z,inclination,S1x,S1y,S1z,S2x,S2y,S2z,m1,m2,f_ref,phiRef,XLALSimInspiralGetFrameAxis(waveFlags));
 5859            LNhatx = sin(incl);
 5860            LNhaty = 0.;
 5861            LNhatz = cos(incl);
 5862            E1x = 0.;
 5863            E1y = 1.;
 5864            E1z = 0.;
 5865        polariz+=LAL_PI/2.;
 5866            /* Maximum PN amplitude order for precessing waveforms is
 5867             * MAX_PRECESSING_AMP_PN_ORDER */
 5868            amplitudeO = amplitudeO <= MAX_PRECESSING_AMP_PN_ORDER ?
 5869                    amplitudeO : MAX_PRECESSING_AMP_PN_ORDER;
 5870            /* Call the waveform driver routine */
 5871            ret = XLALSimInspiralSpinTaylorT5(hplus, hcross, phiRef, deltaT,
 5872                          m1, m2, f_min, f_ref, distance, spin1x, spin1y, spin1z, spin2x, spin2y, spin2z,
 5873                          LNhatx, LNhaty, LNhatz, E1x, E1y, E1z, NULL);
 5874            break;
 5875 
 5876        // need to make a consistent choice for SpinTaylorT4 and PSpinInspiralRD waveform inputs
 5877        // proposal: TotalJ frame of PSpinInspiralRD
 5878        // inclination denotes the angle between the view direction
 5879        // and J (J is constant during the evolution, J//z, both N and initial
 5880        // L are in the x-z plane) and the spin coordinates are given wrt
 5881        // initial ** L **.
 5882        case SpinTaylorT4:
 5883            /* Waveform-specific sanity checks */
 5884            /* Sanity check unused fields of waveFlags */
 5885            XLALSimInspiralInitialConditionsPrecessingApproxs(&incl,&spin1x,&spin1y,&spin1z,&spin2x,&spin2y,&spin2z,inclination,S1x,S1y,S1z,S2x,S2y,S2z,m1,m2,f_ref,phiRef,XLALSimInspiralGetFrameAxis(waveFlags));
 5886            LNhatx = sin(incl);
 5887            LNhaty = 0.;
 5888            LNhatz = cos(incl);
 5889            E1x = 0.;
 5890            E1y = 1.;
 5891            E1z = 0.;
 5892        polariz+=LAL_PI/2.;
 5893            /* Maximum PN amplitude order for precessing waveforms is
 5894             * MAX_PRECESSING_AMP_PN_ORDER */
 5895            amplitudeO = amplitudeO <= MAX_PRECESSING_AMP_PN_ORDER ?
 5896                    amplitudeO : MAX_PRECESSING_AMP_PN_ORDER;
 5897            /* Call the waveform driver routine */
 5898            ret = XLALSimInspiralSpinTaylorT4OLD(hplus, hcross, phiRef, 1.,deltaT,
 5899                    m1, m2, f_min, f_ref, distance, spin1x, spin1y, spin1z, spin2x, spin2y, spin2z,
 5900                    LNhatx, LNhaty, LNhatz, E1x, E1y, E1z, lambda1, lambda2,
 5901            quadparam1, quadparam2, NULL,
 5902                    phaseO, amplitudeO);
 5903            break;
 5904 
 5905     case SpinTaylorT1:
 5906            /* Waveform-specific sanity checks */
 5907            /* Sanity check unused fields of waveFlags */
 5908        XLALSimInspiralInitialConditionsPrecessingApproxs(&incl,&spin1x,&spin1y,&spin1z,&spin2x,&spin2y,&spin2z,inclination,S1x,S1y,S1z,S2x,S2y,S2z,m1,m2,f_ref,phiRef,XLALSimInspiralGetFrameAxis(waveFlags));
 5909            LNhatx = sin(incl);
 5910            LNhaty = 0.;
 5911            LNhatz = cos(incl);
 5912            E1x = 0.;
 5913            E1y = 1.;
 5914            E1z = 0.;
 5915        polariz+=LAL_PI/2.;
 5916            /* Maximum PN amplitude order for precessing waveforms is
 5917             * MAX_PRECESSING_AMP_PN_ORDER */
 5918            amplitudeO = amplitudeO <= MAX_PRECESSING_AMP_PN_ORDER ?
 5919                    amplitudeO : MAX_PRECESSING_AMP_PN_ORDER;
 5920            /* Call the waveform driver routine */
 5921            ret = XLALSimInspiralSpinTaylorT1OLD(hplus, hcross, phiRef, 1., deltaT,
 5922                          m1, m2, f_min, f_ref, distance, spin1x, spin1y, spin1z, spin2x, spin2y, spin2z, LNhatx, LNhaty, LNhatz, E1x, E1y, E1z, lambda1, lambda2,
 5923                    quadparam1, quadparam2, NULL,
 5924                    phaseO, amplitudeO);
 5925            break;
 5926 
 5927        case SpinDominatedWf:
 5928                // waveform specific sanity checks
 5929                if (S2x != 0. || S2y != 0. || S2z != 0.){
 5930                XLALPrintError("XLAL Error : The spindominatedwf approximant is only for 1 spin case.\n");
 5931                XLAL_ERROR(XLAL_EDOM);
 5932                }
 5933                /*Maximal PN amplitude order is 1.5, maximal phase order is 2 PN*/
 5934                if (amplitudeO > 3) {
 5935                XLALPrintError("XLAL Error : Foe the spindominatedwf approximant maximal amplitude correction is 1.5 PN\n");
 5936                XLAL_ERROR(XLAL_EDOM);
 5937                }
 5938                if (phaseO > 4){
 5939                XLALPrintError("XLAL Error : For the spindominatedwf approximant maximal phase correction is 2 PN\n");
 5940                XLAL_ERROR(XLAL_EDOM);
 5941                }
 5942                incl=inclination;
 5943                LNhatx = 0.;
 5944                LNhaty = 0.;
 5945                LNhatz = 1.;
 5946                /* Call the waveform driver routine */
 5947                ret = XLALSimInspiralSpinDominatedWaveformInterfaceTD(hplus, hcross, deltaT, m1, m2, f_min, f_ref, distance, S1x, S1y, S1z, LNhatx, LNhaty, LNhatz, incl, phaseO, amplitudeO, phiRef);
 5948                break;
 5949 
 5950        /* spin aligned inspiral-merger-ringdown models */
 5951        case IMRPhenomB:
 5952            /* Waveform-specific sanity checks */
 5953            if( !XLALSimInspiralWaveformFlagsIsDefaultOLD(waveFlags) )
 5954                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralWaveformFlags given, but this approximant does not support this case.");
 5955            if( !checkTransverseSpinsZero(S1x, S1y, S2x, S2y) )
 5956                XLAL_ERROR(XLAL_EINVAL, "Non-zero transverse spins were given, but this is a non-precessing approximant.");
 5957            if( !checkTidesZero(lambda1, lambda2) )
 5958                XLAL_ERROR(XLAL_EINVAL, "Non-zero tidal parameters were given, but this is approximant doe not have tidal corrections.");
 5959            if( f_ref != 0.)
 5960                XLALPrintWarning("XLAL Warning - %s: This approximant does use f_ref. The reference phase will be defined at coalescence.\n", __func__);
 5961            /* Call the waveform driver routine */
 5962            // NB: f_max = 0 will generate up to the ringdown cut-off frequency
 5963            ret = XLALSimIMRPhenomBGenerateTD(hplus, hcross, phiRef, deltaT,
 5964                    m1, m2, XLALSimIMRPhenomBComputeChi(m1, m2, S1z, S2z),
 5965                    f_min, 0., distance, inclination);
 5966            break;
 5967 
 5968        case PhenSpinTaylor:
 5969            /* Waveform-specific sanity checks */
 5970            if( !checkTidesZero(lambda1, lambda2) )
 5971                XLAL_ERROR(XLAL_EINVAL, "Non-zero tidal parameters were given, but this is approximant doe not have tidal corrections.");
 5972            /* Call the waveform driver routine */
 5973        XLALSimInspiralInitialConditionsPrecessingApproxs(&incl,&spin1x,&spin1y,&spin1z,&spin2x,&spin2y,&spin2z,inclination,S1x,S1y,S1z,S2x,S2y,S2z,m1,m2,f_ref,phiRef,XLALSimInspiralGetFrameAxis(waveFlags));
 5974        polariz+=LAL_PI/2.;
 5975            ret = XLALSimSpinInspiralGenerator(hplus, hcross, phiRef,
 5976                           deltaT, m1, m2, f_min, f_ref, distance, incl, spin1x, spin1y, spin1z, spin2x, spin2y, spin2z,
 5977                           phaseO, amplitudeO, lambda1, lambda2, quadparam1, quadparam2, NULL);
 5978        break;
 5979 
 5980        case IMRPhenomC:
 5981            /* Waveform-specific sanity checks */
 5982            if( !XLALSimInspiralWaveformFlagsIsDefaultOLD(waveFlags) )
 5983                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralWaveformFlags given, but this approximant does not support this case.");
 5984            if( !checkTransverseSpinsZero(S1x, S1y, S2x, S2y) )
 5985                XLAL_ERROR(XLAL_EINVAL, "Non-zero transverse spins were given, but this is a non-precessing approximant.");
 5986            if( !checkTidesZero(lambda1, lambda2) )
 5987                XLAL_ERROR(XLAL_EINVAL, "Non-zero tidal parameters were given, but this is approximant doe not have tidal corrections.");
 5988            if( f_ref != 0.)
 5989                XLALPrintWarning("XLAL Warning - %s: This approximant does use f_ref. The reference phase will be defined at coalescence.\n", __func__);
 5990            /* Call the waveform driver routine */
 5991            // NB: f_max = 0 will generate up to the ringdown cut-off frequency
 5992            ret = XLALSimIMRPhenomCGenerateTD(hplus, hcross, phiRef, deltaT,
 5993                    m1, m2, XLALSimIMRPhenomBComputeChi(m1, m2, S1z, S2z),
 5994                    f_min, 0., distance, inclination, NULL);
 5995            break;
 5996 
 5997    case IMRPhenomD:
 5998            if( !XLALSimInspiralWaveformFlagsIsDefaultOLD(waveFlags) )
 5999            XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralWaveformFlags given, but this approximant does not support this case.");
 6000        if( !checkTransverseSpinsZero(S1x, S1y, S2x, S2y) )
 6001                XLAL_ERROR(XLAL_EINVAL, "Non-zero transverse spins were given, but this is a non-precessing approximant.");
 6002        if( !checkTidesZero(lambda1, lambda2) )
 6003            XLAL_ERROR(XLAL_EINVAL, "Non-zero tidal parameters were given, but this is approximant doe not have tidal corrections.");
 6004        // generate TD waveforms with zero inclincation so that amplitude can be
 6005        // calculated from hplus and hcross, apply inclination-dependent factors
 6006        // in loop below
 6007            /* FIXME: BUSTED -- EXTRA PARAMS NOT IMPLEMENTED */
 6008        ret = XLALSimInspiralTDFromFD(hplus, hcross, m1, m2, S1x, S1y, S1z, S2x, S2y, S2z, distance, 0.0, phiRef, 0.0, 0.0, 0.0, deltaT, f_min, f_ref, NULL, approximant);
 6009        REAL8 maxamp=0;
 6010        REAL8TimeSeries *hp = *hplus;
 6011        REAL8TimeSeries *hc = *hcross;
 6012        INT4 maxind=hp->data->length - 1;
 6013        INT4 loopi;
 6014        const REAL8 cfac=cos(inclination);
 6015        const REAL8 pfac = 0.5 * (1. + cfac*cfac);
 6016 
 6017        for (loopi=hp->data->length - 1; loopi > -1; loopi--)
 6018        {
 6019            REAL8 ampsqr = (hp->data->data[loopi])*(hp->data->data[loopi]) +
 6020               (hc->data->data[loopi])*(hc->data->data[loopi]);
 6021            if (ampsqr > maxamp)
 6022            {
 6023                maxind=loopi;
 6024                maxamp=ampsqr;
 6025            }
 6026            hp->data->data[loopi] *= pfac;
 6027            hc->data->data[loopi] *= cfac;
 6028        }
 6029        XLALGPSSetREAL8(&(hp->epoch), (-1.) * deltaT * maxind);
 6030        XLALGPSSetREAL8(&(hc->epoch), (-1.) * deltaT * maxind);
 6031        break;
 6032 
 6033    case IMRPhenomPv2:
 6034            /* FIXME: BUSTED -- EXTRA PARAMS NOT IMPLEMENTED */
 6035        ret = XLALSimInspiralTDFromFD(hplus, hcross, m1, m2, S1x, S1y, S1z, S2x, S2y, S2z, distance, inclination, phiRef, 0.0, 0.0, 0.0, deltaT, f_min, f_ref, NULL, approximant);
 6036        break;
 6037 
 6038        case PhenSpinTaylorRD:
 6039            /* Waveform-specific sanity checks */
 6040            if( !checkTidesZero(lambda1, lambda2) )
 6041                XLAL_ERROR(XLAL_EINVAL, "Non-zero tidal parameters were given, but this is approximant doe not have tidal corrections.");
 6042            if( f_ref != 0.)
 6043                XLALPrintWarning("XLAL Warning - %s: This approximant does use f_ref. The reference phase will be defined at the start.\n", __func__);
 6044            /* Call the waveform driver routine */
 6045        XLALSimInspiralInitialConditionsPrecessingApproxs(&incl,&spin1x,&spin1y,&spin1z,&spin2x,&spin2y,&spin2z,inclination,S1x,S1y,S1z,S2x,S2y,S2z,m1,m2,f_ref,phiRef,XLALSimInspiralGetFrameAxis(waveFlags));
 6046        polariz+=LAL_PI/2.;
 6047            ret = XLALSimIMRPhenSpinInspiralRDGenerator(hplus, hcross, phiRef,
 6048                            deltaT, m1, m2, f_min, f_ref, distance, incl, spin1x, spin1y, spin1z, spin2x, spin2y, spin2z,
 6049                            phaseO, amplitudeO, lambda1, lambda2, quadparam1, quadparam2, NULL);
 6050            break;
 6051 
 6052        case SEOBNRv1:
 6053            /* Waveform-specific sanity checks */
 6054            if( !XLALSimInspiralWaveformFlagsIsDefaultOLD(waveFlags) )
 6055                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralWaveformFlags given, but this approximant does not support this case.");
 6056            if( !checkTransverseSpinsZero(S1x, S1y, S2x, S2y) )
 6057                XLAL_ERROR(XLAL_EINVAL, "Non-zero transverse spins were given, but this is a non-precessing approximant.");
 6058            if( !checkTidesZero(lambda1, lambda2) )
 6059                XLAL_ERROR(XLAL_EINVAL, "Non-zero tidal parameters were given, but this is approximant doe not have tidal corrections.");
 6060            if( f_ref != 0.)
 6061                XLALPrintWarning("XLAL Warning - %s: This approximant does not use f_ref. The reference phase will be defined at coalescence.\n", __func__);
 6062            /* Call the waveform driver routine */
 6063            SpinAlignedEOBversion = 1;
 6064            ret = XLALSimIMRSpinAlignedEOBWaveform(hplus, hcross, phiRef,
 6065                    deltaT, m1, m2, f_min, distance, inclination, S1z, S2z, SpinAlignedEOBversion, LALparams);
 6066            break;
 6067 
 6068        case SEOBNRv2:
 6069            /* Waveform-specific sanity checks */
 6070            if( !XLALSimInspiralWaveformFlagsIsDefaultOLD(waveFlags) )
 6071                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralWaveformFlags given, but this approximant does not support this case.");
 6072            if( !checkTransverseSpinsZero(S1x, S1y, S2x, S2y) )
 6073                XLAL_ERROR(XLAL_EINVAL, "Non-zero transverse spins were given, but this is a non-precessing approximant.");
 6074            if( !checkTidesZero(lambda1, lambda2) )
 6075                XLAL_ERROR(XLAL_EINVAL, "Non-zero tidal parameters were given, but this is approximant doe not have tidal corrections.");
 6076            if( f_ref != 0.)
 6077                XLALPrintWarning("XLAL Warning - %s: This approximant does not use f_ref. The reference phase will be defined at coalescence.\n", __func__);
 6078            /* Call the waveform driver routine */
 6079            SpinAlignedEOBversion = 2;
 6080            ret = XLALSimIMRSpinAlignedEOBWaveform(hplus, hcross, phiRef,
 6081                    deltaT, m1, m2, f_min, distance, inclination, S1z, S2z, SpinAlignedEOBversion, LALparams);
 6082            break;
 6083 
 6084        case SEOBNRv4:
 6085            /* Waveform-specific sanity checks */
 6086            if( !XLALSimInspiralWaveformFlagsIsDefaultOLD(waveFlags) )
 6087                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralWaveformFlags given, but this approximant does not support this case.");
 6088            if( !checkTransverseSpinsZero(S1x, S1y, S2x, S2y) )
 6089                XLAL_ERROR(XLAL_EINVAL, "Non-zero transverse spins were given, but this is a non-precessing approximant.");
 6090            if( !checkTidesZero(lambda1, lambda2) )
 6091                XLAL_ERROR(XLAL_EINVAL, "Non-zero tidal parameters were given, but this is approximant doe not have tidal corrections.");
 6092            if( f_ref != 0.)
 6093                XLALPrintWarning("XLAL Warning - %s: This approximant does not use f_ref. The reference phase will be defined at coalescence.\n", __func__);
 6094            /* Call the waveform driver routine */
 6095            SpinAlignedEOBversion = 4;
 6096            ret = XLALSimIMRSpinAlignedEOBWaveform(hplus, hcross, phiRef,
 6097                                                   deltaT, m1, m2, f_min, distance, inclination, S1z, S2z, SpinAlignedEOBversion, LALparams);
 6098            break;
 6099 
 6100        case SEOBNRv2_opt:
 6101             /* Waveform-specific sanity checks */
 6102             if( !XLALSimInspiralWaveformFlagsIsDefaultOLD(waveFlags) )
 6103                 XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralWaveformFlags given, but this approximant does not support this case.");
 6104             if( !checkTransverseSpinsZero(S1x, S1y, S2x, S2y) )
 6105                 XLAL_ERROR(XLAL_EINVAL, "Non-zero transverse spins were given, but this is a non-precessing approximant.");
 6106             if( !checkTidesZero(lambda1, lambda2) )
 6107                 XLAL_ERROR(XLAL_EINVAL, "Non-zero tidal parameters were given, but this is approximant doe not have tidal corrections.");
 6108             if( f_ref != 0.)
 6109                 XLALPrintWarning("XLAL Warning - %s: This approximant does not use f_ref. The reference phase will be defined at coalescence.\n", __func__);
 6110             /* Call the waveform driver routine */
 6111             SpinAlignedEOBversion = 200;
 6112             ret = XLALSimIMRSpinAlignedEOBWaveform(hplus, hcross, phiRef,
 6113                     deltaT, m1, m2, f_min, distance, inclination, S1z, S2z, SpinAlignedEOBversion, LALparams);
 6114             break;
 6115 
 6116        case SEOBNRv3:
 6117            /* Waveform-specific sanity checks */
 6118            if( !XLALSimInspiralWaveformFlagsIsDefaultOLD(waveFlags) )
 6119                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralWaveformFlags given, but this approximant does not support this case.");
 6120            if( !checkTidesZero(lambda1, lambda2) )
 6121                XLAL_ERROR(XLAL_EINVAL, "Non-zero tidal parameters were given, but this is approximant doe not have tidal corrections.");
 6122            if( f_ref != 0.)
 6123                XLALPrintWarning("XLAL Warning - %s: This approximant does use f_ref. The reference phase will be defined at coalescence.\n", __func__);
 6124            /* Call the waveform driver routine */
 6125        REAL8 spin1[3], spin2[3];
 6126            spin1[0] = S1x; spin1[1] = S1y; spin1[2] = S1z;
 6127            spin2[0] = S2x; spin2[1] = S2y; spin2[2] = S2z;
 6128            PrecEOBversion = 3;
 6129            ret = XLALSimIMRSpinEOBWaveform(hplus, hcross, /*&epoch,*/ phiRef,
 6130                                            deltaT, m1, m2, f_min, distance, inclination, spin1, spin2, PrecEOBversion);
 6131            break;
 6132 
 6133        case SEOBNRv4_opt:
 6134            /* Waveform-specific sanity checks */
 6135            if( !XLALSimInspiralWaveformFlagsIsDefaultOLD(waveFlags) )
 6136                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralWaveformFlags given, but this approximant does not support this case.");
 6137            if( !checkTransverseSpinsZero(S1x, S1y, S2x, S2y) )
 6138                XLAL_ERROR(XLAL_EINVAL, "Non-zero transverse spins were given, but this is a non-precessing approximant.");
 6139            if( !checkTidesZero(lambda1, lambda2) )
 6140                XLAL_ERROR(XLAL_EINVAL, "Non-zero tidal parameters were given, but this is approximant doe not have tidal corrections.");
 6141            if( f_ref != 0.)
 6142                XLALPrintWarning("XLAL Warning - %s: This approximant does not use f_ref. The reference phase will be defined at coalescence.\n", __func__);
 6143            /* Call the waveform driver routine */
 6144            SpinAlignedEOBversion = 400;
 6145            ret = XLALSimIMRSpinAlignedEOBWaveform(hplus, hcross, phiRef,
 6146                                                   deltaT, m1, m2, f_min, distance, inclination, S1z, S2z, SpinAlignedEOBversion, LALparams);
 6147            break;
 6148 
 6149    case HGimri:
 6150         /* Waveform-specific sanity checks */
 6151         if( !checkTidesZero(lambda1, lambda2) )
 6152         XLAL_ERROR(XLAL_EINVAL, "Non-zero tidal parameters were given, but this is approximant doe not have tidal corrections.");
 6153         if( !checkCOSpinZero(S2x, S2y, S2z) )
 6154         XLAL_ERROR(XLAL_EINVAL, "Non-zero CO spin given, but this approximant does not support this case.");
 6155         /* Call the waveform driver */
 6156         ret = XLALHGimriGenerator(hplus, hcross, phiRef, deltaT, m1, m2, f_min, distance, inclination, S1z);
 6157         break;
 6158 
 6159        case NR_hdf5:
 6160            /* Waveform-specific sanity checks */
 6161            numrel_data_path = XLALSimInspiralGetNumrelDataOLD(waveFlags);
 6162            /* Call the waveform driver routine */
 6163            ret = XLALSimInspiralNRWaveformGetHplusHcross(hplus, hcross,
 6164                    phiRef, inclination, deltaT, m1, m2, distance, f_min, f_ref, S1x, S1y, S1z,
 6165                    S2x, S2y, S2z, numrel_data_path, NULL);
 6166            XLALFree(numrel_data_path);
 6167            break;
 6168 
 6169 
 6170        default:
 6171            XLALPrintError("TD version of approximant not implemented in lalsimulation\n");
 6172            XLAL_ERROR(XLAL_EINVAL);
 6173    }
 6174 
 6175    if (polariz) {
 6176      REAL8 tmpP,tmpC;
 6177      REAL8 cp=cos(2.*polariz);
 6178      REAL8 sp=sin(2.*polariz);
 6179      for (UINT4 idx=0;idx<(*hplus)->data->length;idx++) {
 6180    tmpP=(*hplus)->data->data[idx];
 6181    tmpC=(*hcross)->data->data[idx];
 6182    (*hplus)->data->data[idx] =cp*tmpP+sp*tmpC;
 6183    (*hcross)->data->data[idx]=cp*tmpC-sp*tmpP;
 6184      }
 6185    }
 6186 
 6187    if (ret == XLAL_FAILURE) XLAL_ERROR(XLAL_EFUNC);
 6188 
 6189    return ret;
 6190}
 6191 
 6192/**
 6193 * @deprecated Use XLALSimInspiralChooseFDWaveform() instead
 6194 * Chooses between different approximants when requesting a waveform to be generated
 6195 * For spinning waveforms, all known spin effects up to given PN order are included
 6196 * Returns the waveform in the frequency domain.
 6197 */
 6198int XLALSimInspiralChooseFDWaveformOLD(
 6199    COMPLEX16FrequencySeries **hptilde,     /**< FD plus polarization */
 6200    COMPLEX16FrequencySeries **hctilde,     /**< FD cross polarization */
 6201    const REAL8 m1,                         /**< mass of companion 1 (kg) */
 6202    const REAL8 m2,                         /**< mass of companion 2 (kg) */
 6203    const REAL8 S1x,                        /**< x-component of the dimensionless spin of object 1 */
 6204    const REAL8 S1y,                        /**< y-component of the dimensionless spin of object 1 */
 6205    const REAL8 S1z,                        /**< z-component of the dimensionless spin of object 1 */
 6206    const REAL8 S2x,                        /**< x-component of the dimensionless spin of object 2 */
 6207    const REAL8 S2y,                        /**< y-component of the dimensionless spin of object 2 */
 6208    const REAL8 S2z,                        /**< z-component of the dimensionless spin of object 2 */
 6209    const REAL8 distance,                   /**< distance of source (m) */
 6210    const REAL8 inclination,                /**< inclination of source (rad) */
 6211    const REAL8 phiRef,                     /**< reference orbital phase (rad) */
 6212    const REAL8 longAscNodes,               /**< longitude of ascending nodes, degenerate with the polarization angle, Omega in documentation */
 6213    const REAL8 eccentricity,               /**< eccentricity at reference epoch */
 6214    const REAL8 UNUSED meanPerAno,          /**< mean anomaly of periastron */
 6215    // frequency sampling parameters, no default value
 6216    const REAL8 deltaF,                     /**< sampling interval (Hz) */
 6217    const REAL8 f_min,                      /**< starting GW frequency (Hz) */
 6218    const REAL8 f_max,                      /**< ending GW frequency (Hz) */
 6219    REAL8 f_ref,                            /**< Reference frequency (Hz) */
 6220    const REAL8 lambda1,                    /**< (tidal deformability of mass 1) / m1^5 (dimensionless) */
 6221    const REAL8 lambda2,                    /**< (tidal deformability of mass 2) / m2^5 (dimensionless) */
 6222    const REAL8 dQuadParam1,                /**< (quad-monop parameter of mass 1) / m1^5 -1 (dimensionless), give 0 for BHs */
 6223    const REAL8 dQuadParam2,                /**< (quad-monop parameter of mass 2) / m2^5 -1 (dimensionless), give 0 for BHs */
 6224    LALSimInspiralWaveformFlags *waveFlags, /**< Set of flags to control special behavior of some waveform families. Pass in NULL (or None in python) for default flags */
 6225    LALSimInspiralTestGRParam *nonGRparams, /**< Linked list of non-GR parameters. Pass in NULL (or None in python) for standard GR waveforms */
 6226    int amplitudeO,                         /**< twice post-Newtonian amplitude order */
 6227    const int phaseO,                       /**< twice post-Newtonian order */
 6228    const Approximant approximant           /**< post-Newtonian approximant to use for waveform production */
 6229    )
 6230{
 6231    REAL8 LNhatx, LNhaty, LNhatz;
 6232    REAL8 tmp1, tmp2;
 6233    REAL8 E1x, E1y, E1z;
 6234    REAL8 kMax;
 6235    REAL8 v0, fStart;
 6236    int ret;
 6237    unsigned int j;
 6238    REAL8 pfac, cfac;
 6239    REAL8 quadparam1 = 1.+dQuadParam1, quadparam2 = 1.+dQuadParam2;
 6240    INT4 phiRefAtEnd;
 6241 
 6242    /* Support variables for precessing wfs*/
 6243    REAL8 incl;
 6244    REAL8 spin1x,spin1y,spin1z;
 6245    REAL8 spin2x,spin2y,spin2z;
 6246 
 6247    /* Variables for IMRPhenomP and IMRPhenomPv2 */
 6248    REAL8 chi1_l, chi2_l, chip, thetaJ, alpha0;
 6249 
 6250    /* General sanity checks that will abort
 6251     *
 6252     * If non-GR approximants are added, include them in
 6253     * XLALSimInspiralApproximantAcceptTestGRParams()
 6254     */
 6255    if( nonGRparams && XLALSimInspiralApproximantAcceptTestGRParams(approximant) != LAL_SIM_INSPIRAL_TESTGR_PARAMS ) {
 6256        XLALPrintError("XLAL Error - %s: Passed in non-NULL pointer to LALSimInspiralTestGRParam for an approximant that does not use LALSimInspiralTestGRParam\n", __func__);
 6257        XLAL_ERROR(XLAL_EINVAL);
 6258    }
 6259 
 6260    /* General sanity check the input parameters - only give warnings! */
 6261    if( deltaF > 1. )
 6262        XLALPrintWarning("XLAL Warning - %s: Large value of deltaF = %e requested...This corresponds to a very short TD signal (with padding). Consider a smaller value.\n", __func__, deltaF);
 6263    if( deltaF < 1./4096. )
 6264        XLALPrintWarning("XLAL Warning - %s: Small value of deltaF = %e requested...This corresponds to a very long TD signal. Consider a larger value.\n", __func__, deltaF);
 6265    if( m1 < 0.09 * LAL_MSUN_SI )
 6266        XLALPrintWarning("XLAL Warning - %s: Small value of m1 = %e (kg) = %e (Msun) requested...Perhaps you have a unit conversion error?\n", __func__, m1, m1/LAL_MSUN_SI);
 6267    if( m2 < 0.09 * LAL_MSUN_SI )
 6268        XLALPrintWarning("XLAL Warning - %s: Small value of m2 = %e (kg) = %e (Msun) requested...Perhaps you have a unit conversion error?\n", __func__, m2, m2/LAL_MSUN_SI);
 6269    if( m1 + m2 > 1000. * LAL_MSUN_SI )
 6270        XLALPrintWarning("XLAL Warning - %s: Large value of total mass m1+m2 = %e (kg) = %e (Msun) requested...Signal not likely to be in band of ground-based detectors.\n", __func__, m1+m2, (m1+m2)/LAL_MSUN_SI);
 6271    if( S1x*S1x + S1y*S1y + S1z*S1z > 1.000001 )
 6272        XLALPrintWarning("XLAL Warning - %s: S1 = (%e,%e,%e) with norm > 1 requested...Are you sure you want to violate the Kerr bound?\n", __func__, S1x, S1y, S1z);
 6273    if( S2x*S2x + S2y*S2y + S2z*S2z > 1.000001 )
 6274        XLALPrintWarning("XLAL Warning - %s: S2 = (%e,%e,%e) with norm > 1 requested...Are you sure you want to violate the Kerr bound?\n", __func__, S2x, S2y, S2z);
 6275    if( f_min < 1. )
 6276        XLALPrintWarning("XLAL Warning - %s: Small value of fmin = %e requested...Check for errors, this could create a very long waveform.\n", __func__, f_min);
 6277    if( f_min > 40.000001 )
 6278        XLALPrintWarning("XLAL Warning - %s: Large value of fmin = %e requested...Check for errors, the signal will start in band.\n", __func__, f_min);
 6279 
 6280    /* adjust the reference frequency for certain precessing approximants:
 6281     * if that approximate interprets f_ref==0 to be f_min, set f_ref=f_min;
 6282     * otherwise do nothing */
 6283    FIX_REFERENCE_FREQUENCY(f_ref, f_min, approximant);
 6284 
 6285    /* The non-precessing waveforms return h(f) for optimal orientation
 6286     * (i=0, Fp=1, Fc=0; Lhat pointed toward the observer)
 6287     * To get generic polarizations we multiply by inclination dependence
 6288     * and note hc(f) \propto -I * hp(f)
 6289     * Non-precessing waveforms multiply hp by pfac, hc by -I*cfac
 6290     */
 6291    cfac = cos(inclination);
 6292    pfac = 0.5 * (1. + cfac*cfac);
 6293 
 6294    switch (approximant)
 6295    {
 6296        /* inspiral-only models */
 6297    case EccentricFD:
 6298            /* Waveform-specific sanity checks */
 6299            if( !XLALSimInspiralFrameAxisIsDefault(
 6300                    XLALSimInspiralGetFrameAxis(waveFlags) ) )
 6301                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralFrameAxis provided, but this approximant does not use that flag.");
 6302            if( !XLALSimInspiralModesChoiceIsDefault(
 6303                    XLALSimInspiralGetModesChoice(waveFlags) ) )
 6304                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralModesChoice provided, but this approximant does not use that flag.");
 6305            if( !checkTransverseSpinsZero(S1x, S1y, S2x, S2y) )
 6306                XLAL_ERROR(XLAL_EINVAL, "Non-zero transverse spins were given, but this is a non-precessing approximant.");
 6307            /* Call the waveform driver routine */
 6308            /* Note that for generic inclined eccentric waveforms
 6309 *             * it is not possible to decompose hc(f) \propto I * hp(f)
 6310 *                         * we call both polarizations independently
 6311 *                                     */
 6312            /*ret = XLALSimInspiralEFD(hptilde, hctilde, phiRef, deltaF, m1, m2,
 6313 *             f_min, f_max, i, r, lambda1, lambda2, phaseO);*/
 6314            ret = XLALSimInspiralEFD(hptilde, hctilde, phiRef, deltaF, m1, m2,
 6315            f_min, f_max, inclination, distance,  (REAL8) XLALSimInspiralGetTestGRParam( nonGRparams, "inclination_azimuth"),
 6316             eccentricity, phaseO);
 6317            if (ret == XLAL_FAILURE) XLAL_ERROR(XLAL_EFUNC);
 6318            break;
 6319 
 6320        case TaylorF2:
 6321            /* Waveform-specific sanity checks */
 6322            if( !XLALSimInspiralFrameAxisIsDefault(
 6323                    XLALSimInspiralGetFrameAxis(waveFlags) ) )
 6324                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralFrameAxis provided, but this approximant does not use that flag.");
 6325            if( !XLALSimInspiralModesChoiceIsDefault(
 6326                    XLALSimInspiralGetModesChoice(waveFlags) ) )
 6327                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralModesChoice provided, but this approximant does not use that flag.");
 6328            if( !checkTransverseSpinsZero(S1x, S1y, S2x, S2y) )
 6329                XLAL_ERROR(XLAL_EINVAL, "Non-zero transverse spins were given, but this is a non-precessing approximant.");
 6330        XLAL_PRINT_DEPRECATION_WARNING("Calling TF2 via old interface, setting to default values tidal lambdas, quad-monopole pars, amplitude and phase order");
 6331            /* Call the waveform driver routine */
 6332            ret = XLALSimInspiralTaylorF2(hptilde, phiRef, deltaF, m1, m2,
 6333                    S1z, S2z, f_min, f_max, f_ref, distance,
 6334                    NULL);
 6335            if (ret == XLAL_FAILURE) XLAL_ERROR(XLAL_EFUNC);
 6336            /* Produce both polarizations */
 6337            *hctilde = XLALCreateCOMPLEX16FrequencySeries("FD hcross",
 6338                    &((*hptilde)->epoch), (*hptilde)->f0, (*hptilde)->deltaF,
 6339                    &((*hptilde)->sampleUnits), (*hptilde)->data->length);
 6340            for(j = 0; j < (*hptilde)->data->length; j++) {
 6341                (*hctilde)->data->data[j] = -I*cfac * (*hptilde)->data->data[j];
 6342                (*hptilde)->data->data[j] *= pfac;
 6343            }
 6344            break;
 6345 
 6346        case TaylorF2NLTides:
 6347            /* Waveform-specific sanity checks */
 6348            if( !XLALSimInspiralFrameAxisIsDefault(
 6349                    XLALSimInspiralGetFrameAxis(waveFlags) ) )
 6350                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralFrameAxis provided, but this approximant does not use that flag.");
 6351            if( !XLALSimInspiralModesChoiceIsDefault(
 6352                    XLALSimInspiralGetModesChoice(waveFlags) ) )
 6353                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralModesChoice provided, but this approximant does not use that flag.");
 6354            if( !checkTransverseSpinsZero(S1x, S1y, S2x, S2y) )
 6355                XLAL_ERROR(XLAL_EINVAL, "Non-zero transverse spins were given, but this is a non-precessing approximant.");
 6356            XLAL_PRINT_DEPRECATION_WARNING("Calling TF2 via old interface, setting to default values tidal lambdas, quad-monopole pars, amplitude and phase order");
 6357 
 6358            // FIXME : add checks for NL tidal parameters?
 6359 
 6360            /* Call the waveform driver routine */
 6361            ret = XLALSimInspiralTaylorF2NLTides(hptilde, phiRef, deltaF, m1, m2,
 6362                    S1z, S2z, f_min, f_max, f_ref, distance,
 6363                    NULL);
 6364            if (ret == XLAL_FAILURE) XLAL_ERROR(XLAL_EFUNC);
 6365            /* Produce both polarizations */
 6366            *hctilde = XLALCreateCOMPLEX16FrequencySeries("FD hcross",
 6367                    &((*hptilde)->epoch), (*hptilde)->f0, (*hptilde)->deltaF,
 6368                    &((*hptilde)->sampleUnits), (*hptilde)->data->length);
 6369            for(j = 0; j < (*hptilde)->data->length; j++) {
 6370                (*hctilde)->data->data[j] = -I*cfac * (*hptilde)->data->data[j];
 6371                (*hptilde)->data->data[j] *= pfac;
 6372            }
 6373            break;
 6374 
 6375        /* non-spinning inspiral-merger-ringdown models */
 6376        case IMRPhenomA:
 6377            /* Waveform-specific sanity checks */
 6378            if( !XLALSimInspiralWaveformFlagsIsDefaultOLD(waveFlags) )
 6379                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralWaveformFlags given, but this approximant does not support this case.");
 6380            if( !checkSpinsZero(S1x, S1y, S1z, S2x, S2y, S2z) )
 6381                XLAL_ERROR(XLAL_EINVAL, "Non-zero spins were given, but this is a non-spinning approximant.");
 6382            if( !checkTidesZero(lambda1, lambda2) )
 6383                XLAL_ERROR(XLAL_EINVAL, "Non-zero tidal parameters were given, but this is approximant doe not have tidal corrections.");
 6384            /* Call the waveform driver routine */
 6385            ret = XLALSimIMRPhenomAGenerateFD(hptilde, phiRef, deltaF, m1, m2,
 6386                    f_min, f_max, distance);
 6387            if (ret == XLAL_FAILURE) XLAL_ERROR(XLAL_EFUNC);
 6388            /* Produce both polarizations */
 6389            *hctilde = XLALCreateCOMPLEX16FrequencySeries("FD hcross",
 6390                    &((*hptilde)->epoch), (*hptilde)->f0, (*hptilde)->deltaF,
 6391                    &((*hptilde)->sampleUnits), (*hptilde)->data->length);
 6392            for(j = 0; j < (*hptilde)->data->length; j++) {
 6393                (*hctilde)->data->data[j] = -I*cfac * (*hptilde)->data->data[j];
 6394                (*hptilde)->data->data[j] *= pfac;
 6395            }
 6396            break;
 6397 
 6398        /* spinning inspiral-only models */
 6399        case SpinTaylorF2:
 6400            /* Waveform-specific sanity checks */
 6401            /* Sanity check unused fields of waveFlags */
 6402            if( !XLALSimInspiralFrameAxisIsDefault(
 6403                    XLALSimInspiralGetFrameAxis(waveFlags) ) )
 6404                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralFrameAxis provided, but this approximant does not use that flag.");
 6405            if( !XLALSimInspiralModesChoiceIsDefault(
 6406                    XLALSimInspiralGetModesChoice(waveFlags) ) )
 6407                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralModesChoice provided, but this approximant does not use that flag.");
 6408            if( !checkCOSpinZero(S2x, S2y, S2z) ) // This is a single-spin model
 6409                XLAL_ERROR(XLAL_EINVAL, "Non-zero CO spin given, but this approximant does not support this case.");
 6410        spin1x=S1x;
 6411        spin1y=S1y;
 6412        spin1z=S1z;
 6413            ROTATEY(inclination, spin1x, spin1y, spin1z);
 6414            LNhatx = sin(inclination);
 6415            LNhaty = 0.;
 6416            LNhatz = cos(inclination);
 6417            /* Maximum PN amplitude order for precessing waveforms is
 6418             * MAX_PRECESSING_AMP_PN_ORDER */
 6419            amplitudeO = 0; /* amplitudeO <= MAX_PRECESSING_AMP_PN_ORDER ?
 6420                    amplitudeO : MAX_PRECESSING_AMP_PN_ORDER */;
 6421            /* Call the waveform driver routine */
 6422            ret = XLALSimInspiralSpinTaylorF2(hptilde, hctilde, phiRef, deltaF,
 6423                    m1, m2, spin1x, spin1y, spin1z, LNhatx, LNhaty, LNhatz,
 6424                    f_min, f_max, f_ref, distance,
 6425                    NULL, phaseO, amplitudeO);
 6426            if (ret == XLAL_FAILURE) XLAL_ERROR(XLAL_EFUNC);
 6427            break;
 6428 
 6429        /* FIXME: Comment out this case, as I don't have its source code */
 6430        //case TaylorR2F4:
 6431        //    /* Waveform-specific sanity checks */
 6432        //    if( !XLALSimInspiralWaveformFlagsIsDefault(waveFlags) )
 6433        //        XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralWaveformFlags given, but this approximant does not support this case.");
 6434        //    if( !checkTransverseSpinsZero(S1x, S1y, S2x, S2y) )
 6435        //        XLAL_ERROR(XLAL_EINVAL, "Non-zero transverse spins were given, but this is a non-precessing approximant.");
 6436        //    /* Call the waveform driver routine */
 6437        //    ret = XLALSimInspiralTaylorR2F4(hptilde, phiRef, deltaF, m1, m2,
 6438        //            S1z, S2z, f_min, r, phaseO, amplitudeO);
 6439        //    break;
 6440 
 6441        case TaylorF2RedSpin:
 6442            /* Waveform-specific sanity checks */
 6443            if( !XLALSimInspiralWaveformFlagsIsDefaultOLD(waveFlags) )
 6444                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralWaveformFlags given, but this approximant does not support this case.");
 6445            if( !checkTransverseSpinsZero(S1x, S1y, S2x, S2y) )
 6446                XLAL_ERROR(XLAL_EINVAL, "Non-zero transverse spins were given, but this is a non-precessing approximant.");
 6447            if( !checkTidesZero(lambda1, lambda2) )
 6448                XLAL_ERROR(XLAL_EINVAL, "Non-zero tidal parameters were given, but this is approximant doe not have tidal corrections.");
 6449            /* Call the waveform driver routine */
 6450            ret = XLALSimInspiralTaylorF2ReducedSpin(hptilde, phiRef, deltaF,
 6451                    m1, m2, XLALSimInspiralTaylorF2ReducedSpinComputeChi(m1, m2, S1z, S2z),
 6452                    f_min, f_max, distance, phaseO, amplitudeO);
 6453            if (ret == XLAL_FAILURE) XLAL_ERROR(XLAL_EFUNC);
 6454            /* Produce both polarizations */
 6455            *hctilde = XLALCreateCOMPLEX16FrequencySeries("FD hcross",
 6456                    &((*hptilde)->epoch), (*hptilde)->f0, (*hptilde)->deltaF,
 6457                    &((*hptilde)->sampleUnits), (*hptilde)->data->length);
 6458            for(j = 0; j < (*hptilde)->data->length; j++) {
 6459                (*hctilde)->data->data[j] = -I*cfac * (*hptilde)->data->data[j];
 6460                (*hptilde)->data->data[j] *= pfac;
 6461            }
 6462            break;
 6463 
 6464        case TaylorF2RedSpinTidal:
 6465            /* Waveform-specific sanity checks */
 6466            if( !XLALSimInspiralWaveformFlagsIsDefaultOLD(waveFlags) )
 6467                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralWaveformFlags given, but this approximant does not support this case.");
 6468            if( !checkTransverseSpinsZero(S1x, S1y, S2x, S2y) )
 6469                XLAL_ERROR(XLAL_EINVAL, "Non-zero transverse spins were given, but this is a non-precessing approximant.");
 6470            /* Call the waveform driver routine */
 6471            ret = XLALSimInspiralTaylorF2ReducedSpinTidal(hptilde,phiRef,deltaF,
 6472                    m1, m2, XLALSimIMRPhenomBComputeChi(m1, m2, S1z, S2z),
 6473                    lambda1, lambda2, f_min, f_max, distance, phaseO, amplitudeO);
 6474            if (ret == XLAL_FAILURE) XLAL_ERROR(XLAL_EFUNC);
 6475            /* Produce both polarizations */
 6476            *hctilde = XLALCreateCOMPLEX16FrequencySeries("FD hcross",
 6477                    &((*hptilde)->epoch), (*hptilde)->f0, (*hptilde)->deltaF,
 6478                    &((*hptilde)->sampleUnits), (*hptilde)->data->length);
 6479            for(j = 0; j < (*hptilde)->data->length; j++) {
 6480                (*hctilde)->data->data[j] = -I*cfac * (*hptilde)->data->data[j];
 6481                (*hptilde)->data->data[j] *= pfac;
 6482            }
 6483            break;
 6484 
 6485        /* spinning inspiral-merger-ringdown models */
 6486        case IMRPhenomB:
 6487            /* Waveform-specific sanity checks */
 6488            if( !XLALSimInspiralWaveformFlagsIsDefaultOLD(waveFlags) )
 6489                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralWaveformFlags given, but this approximant does not support this case.");
 6490            if( !checkTransverseSpinsZero(S1x, S1y, S2x, S2y) )
 6491                XLAL_ERROR(XLAL_EINVAL, "Non-zero transverse spins were given, but this is a non-precessing approximant.");
 6492            if( !checkTidesZero(lambda1, lambda2) )
 6493                XLAL_ERROR(XLAL_EINVAL, "Non-zero tidal parameters were given, but this is approximant doe not have tidal corrections.");
 6494            /* Call the waveform driver routine */
 6495            ret = XLALSimIMRPhenomBGenerateFD(hptilde, phiRef, deltaF, m1, m2,
 6496                    XLALSimIMRPhenomBComputeChi(m1, m2, S1z, S2z),
 6497                    f_min, f_max, distance);
 6498            if (ret == XLAL_FAILURE) XLAL_ERROR(XLAL_EFUNC);
 6499            /* Produce both polarizations */
 6500            *hctilde = XLALCreateCOMPLEX16FrequencySeries("FD hcross",
 6501                    &((*hptilde)->epoch), (*hptilde)->f0, (*hptilde)->deltaF,
 6502                    &((*hptilde)->sampleUnits), (*hptilde)->data->length);
 6503            for(j = 0; j < (*hptilde)->data->length; j++) {
 6504                (*hctilde)->data->data[j] = -I*cfac * (*hptilde)->data->data[j];
 6505                (*hptilde)->data->data[j] *= pfac;
 6506            }
 6507            break;
 6508 
 6509        case IMRPhenomC:
 6510            /* Waveform-specific sanity checks */
 6511            if( !XLALSimInspiralWaveformFlagsIsDefaultOLD(waveFlags) )
 6512                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralWaveformFlags given, but this approximant does not support this case.");
 6513            if( !checkTransverseSpinsZero(S1x, S1y, S2x, S2y) )
 6514                XLAL_ERROR(XLAL_EINVAL, "Non-zero transverse spins were given, but this is a non-precessing approximant.");
 6515            if( !checkTidesZero(lambda1, lambda2) )
 6516                XLAL_ERROR(XLAL_EINVAL, "Non-zero tidal parameters were given, but this is approximant doe not have tidal corrections.");
 6517            /* Call the waveform driver routine */
 6518            ret = XLALSimIMRPhenomCGenerateFD(hptilde, phiRef, deltaF, m1, m2,
 6519                    XLALSimIMRPhenomBComputeChi(m1, m2, S1z, S2z),
 6520                    f_min, f_max, distance, NULL);
 6521            if (ret == XLAL_FAILURE) XLAL_ERROR(XLAL_EFUNC);
 6522            /* Produce both polarizations */
 6523            *hctilde = XLALCreateCOMPLEX16FrequencySeries("FD hcross",
 6524                    &((*hptilde)->epoch), (*hptilde)->f0, (*hptilde)->deltaF,
 6525                    &((*hptilde)->sampleUnits), (*hptilde)->data->length);
 6526            for(j = 0; j < (*hptilde)->data->length; j++) {
 6527                (*hctilde)->data->data[j] = -I*cfac * (*hptilde)->data->data[j];
 6528                (*hptilde)->data->data[j] *= pfac;
 6529            }
 6530            break;
 6531 
 6532        case IMRPhenomD:
 6533            /* Waveform-specific sanity checks */
 6534            if( !XLALSimInspiralWaveformFlagsIsDefaultOLD(waveFlags) )
 6535                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralWaveformFlags given, but this approximant does not support this case.");
 6536            if( !checkTransverseSpinsZero(S1x, S1y, S2x, S2y) )
 6537                XLAL_ERROR(XLAL_EINVAL, "Non-zero transverse spins were given, but this is a non-precessing approximant.");
 6538            if( !checkTidesZero(lambda1, lambda2) )
 6539                XLAL_ERROR(XLAL_EINVAL, "Non-zero tidal parameters were given, but this is approximant doe not have tidal corrections.");
 6540            /* Call the waveform driver routine */
 6541 
 6542            ret = XLALSimIMRPhenomDGenerateFD(hptilde, phiRef, f_ref, deltaF, m1, m2,
 6543                  S1z, S2z, f_min, f_max, distance, NULL, NoNRT_V);
 6544            if (ret == XLAL_FAILURE) XLAL_ERROR(XLAL_EFUNC);
 6545            /* Produce both polarizations */
 6546            *hctilde = XLALCreateCOMPLEX16FrequencySeries("FD hcross",
 6547                    &((*hptilde)->epoch), (*hptilde)->f0, (*hptilde)->deltaF,
 6548                    &((*hptilde)->sampleUnits), (*hptilde)->data->length);
 6549            for(j = 0; j < (*hptilde)->data->length; j++) {
 6550                (*hctilde)->data->data[j] = -I*cfac * (*hptilde)->data->data[j];
 6551                (*hptilde)->data->data[j] *= pfac;
 6552            }
 6553            break;
 6554 
 6555        case EOBNRv2_ROM:
 6556            /* Waveform-specific sanity checks */
 6557            if( !XLALSimInspiralWaveformFlagsIsDefaultOLD(waveFlags) )
 6558                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralWaveformFlags given, but this approximant does not support this case.");
 6559            if( !checkSpinsZero(S1x, S1y, S1z, S2x, S2y, S2z) )
 6560                XLAL_ERROR(XLAL_EINVAL, "Non-zero spins were given, but this is a non-spinning approximant.");
 6561            if( !checkTidesZero(lambda1, lambda2) )
 6562                XLAL_ERROR(XLAL_EINVAL, "Non-zero tidal parameters were given, but this is approximant doe not have tidal corrections.");
 6563 
 6564            ret = XLALSimIMREOBNRv2HMROM(hptilde, hctilde,
 6565        phiRef, deltaF, f_min, f_max, f_ref, distance, inclination, m1, m2, 0);
 6566            break;
 6567 
 6568        case EOBNRv2HM_ROM:
 6569            /* Waveform-specific sanity checks */
 6570            if( !XLALSimInspiralWaveformFlagsIsDefaultOLD(waveFlags) )
 6571                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralWaveformFlags given, but this approximant does not support this case.");
 6572            if( !checkSpinsZero(S1x, S1y, S1z, S2x, S2y, S2z) )
 6573                XLAL_ERROR(XLAL_EINVAL, "Non-zero spins were given, but this is a non-spinning approximant.");
 6574            if( !checkTidesZero(lambda1, lambda2) )
 6575                XLAL_ERROR(XLAL_EINVAL, "Non-zero tidal parameters were given, but this is approximant doe not have tidal corrections.");
 6576 
 6577            ret = XLALSimIMREOBNRv2HMROM(hptilde, hctilde,
 6578        phiRef, deltaF, f_min, f_max, f_ref, distance, inclination, m1, m2, 1);
 6579            break;
 6580 
 6581        case SEOBNRv1_ROM_EffectiveSpin:
 6582            /* Waveform-specific sanity checks */
 6583            if( !XLALSimInspiralWaveformFlagsIsDefaultOLD(waveFlags) )
 6584                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralWaveformFlags given, but this approximant does not support this case.");
 6585            if( !checkTransverseSpinsZero(S1x, S1y, S2x, S2y) )
 6586                XLAL_ERROR(XLAL_EINVAL, "Non-zero transverse spins were given, but this is a non-precessing approximant.");
 6587            if( !checkTidesZero(lambda1, lambda2) )
 6588                XLAL_ERROR(XLAL_EINVAL, "Non-zero tidal parameters were given, but this is approximant doe not have tidal corrections.");
 6589            if (!checkAlignedSpinsEqual(S1z, S2z)) {
 6590                    XLALPrintError("XLAL Error - %s: SEOBNRv1ROM Effective Spin model called with unequal aligned spins: %lf, %lf.\n", __func__,S1z,S2z);
 6591                    XLAL_ERROR(XLAL_EINVAL);
 6592            }
 6593 
 6594            ret = XLALSimIMRSEOBNRv1ROMEffectiveSpin(hptilde, hctilde,
 6595                    phiRef, deltaF, f_min, f_max, f_ref, distance, inclination, m1, m2, XLALSimIMRPhenomBComputeChi(m1, m2, S1z, S2z));
 6596            break;
 6597 
 6598        case SEOBNRv1_ROM_DoubleSpin:
 6599            /* Waveform-specific sanity checks */
 6600            if( !XLALSimInspiralWaveformFlagsIsDefaultOLD(waveFlags) )
 6601                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralWaveformFlags given, but this approximant does not support this case.");
 6602            if( !checkTransverseSpinsZero(S1x, S1y, S2x, S2y) )
 6603                XLAL_ERROR(XLAL_EINVAL, "Non-zero transverse spins were given, but this is a non-precessing approximant.");
 6604            if( !checkTidesZero(lambda1, lambda2) )
 6605                XLAL_ERROR(XLAL_EINVAL, "Non-zero tidal parameters were given, but this is approximant doe not have tidal corrections.");
 6606 
 6607            ret = XLALSimIMRSEOBNRv1ROMDoubleSpin(hptilde, hctilde,
 6608                    phiRef, deltaF, f_min, f_max, f_ref, distance, inclination, m1, m2, S1z, S2z);
 6609            break;
 6610 
 6611        case SEOBNRv2_ROM_EffectiveSpin:
 6612            /* Waveform-specific sanity checks */
 6613            if( !XLALSimInspiralWaveformFlagsIsDefaultOLD(waveFlags) )
 6614                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralWaveformFlags given, but this approximant does not support this case.");
 6615            if( !checkTransverseSpinsZero(S1x, S1y, S2x, S2y) )
 6616                XLAL_ERROR(XLAL_EINVAL, "Non-zero transverse spins were given, but this is a non-precessing approximant.");
 6617            if( !checkTidesZero(lambda1, lambda2) )
 6618                XLAL_ERROR(XLAL_EINVAL, "Non-zero tidal parameters were given, but this is approximant doe not have tidal corrections.");
 6619            if (!checkAlignedSpinsEqual(S1z, S2z)) {
 6620                    XLALPrintError("XLAL Error - %s: SEOBNRv2ROM Effective Spin model called with unequal aligned spins: %lf, %lf.\n", __func__,S1z,S2z);
 6621                    XLAL_ERROR(XLAL_EINVAL);
 6622            }
 6623 
 6624            ret = XLALSimIMRSEOBNRv2ROMEffectiveSpin(hptilde, hctilde,
 6625                    phiRef, deltaF, f_min, f_max, f_ref, distance, inclination, m1, m2, XLALSimIMRPhenomBComputeChi(m1, m2, S1z, S2z));
 6626            break;
 6627 
 6628        case SEOBNRv2_ROM_DoubleSpin:
 6629            /* Waveform-specific sanity checks */
 6630            if( !XLALSimInspiralWaveformFlagsIsDefaultOLD(waveFlags) )
 6631                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralWaveformFlags given, but this approximant does not support this case.");
 6632            if( !checkTransverseSpinsZero(S1x, S1y, S2x, S2y) )
 6633                XLAL_ERROR(XLAL_EINVAL, "Non-zero transverse spins were given, but this is a non-precessing approximant.");
 6634            if( !checkTidesZero(lambda1, lambda2) )
 6635                XLAL_ERROR(XLAL_EINVAL, "Non-zero tidal parameters were given, but this is approximant doe not have tidal corrections.");
 6636 
 6637            ret = XLALSimIMRSEOBNRv2ROMDoubleSpin(hptilde, hctilde,
 6638                    phiRef, deltaF, f_min, f_max, f_ref, distance, inclination, m1, m2, S1z, S2z);
 6639            break;
 6640 
 6641        case SEOBNRv2_ROM_DoubleSpin_HI:
 6642            /* Waveform-specific sanity checks */
 6643            if( !XLALSimInspiralWaveformFlagsIsDefaultOLD(waveFlags) )
 6644                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralWaveformFlags given, but this approximant does not support this case.");
 6645            if( !checkTransverseSpinsZero(S1x, S1y, S2x, S2y) )
 6646                XLAL_ERROR(XLAL_EINVAL, "Non-zero transverse spins were given, but this is a non-precessing approximant.");
 6647            if( !checkTidesZero(lambda1, lambda2) )
 6648                XLAL_ERROR(XLAL_EINVAL, "Non-zero tidal parameters were given, but this is approximant doe not have tidal corrections.");
 6649 
 6650            ret = XLALSimIMRSEOBNRv2ROMDoubleSpinHI(hptilde, hctilde,
 6651                    phiRef, deltaF, f_min, f_max, f_ref, distance, inclination, m1, m2, S1z, S2z, -1);
 6652            break;
 6653 
 6654 
 6655        case IMRPhenomP:
 6656            /* Waveform-specific sanity checks */
 6657            XLALSimInspiralInitialConditionsPrecessingApproxs(&incl,&spin1x,&spin1y,&spin1z,&spin2x,&spin2y,&spin2z,inclination,S1x,S1y,S1z,S2x,S2y,S2z,m1,m2,f_ref,phiRef,XLALSimInspiralGetFrameAxis(waveFlags));
 6658            if( !XLALSimInspiralModesChoiceIsDefault(          /* Default is (2,2) or l=2 modes. */
 6659                    XLALSimInspiralGetModesChoice(waveFlags) ) )
 6660                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralModesChoice provided, but this approximant does not use that flag.");
 6661            if( !checkTidesZero(lambda1, lambda2) )
 6662                XLAL_ERROR(XLAL_EINVAL, "Non-zero tidal parameters were given, but this is approximant doe not have tidal corrections.");
 6663            LNhatx = sin(incl);
 6664            LNhaty = 0.;
 6665            LNhatz = cos(incl);
 6666            /* Tranform to model parameters */
 6667            if(f_ref==0.0)
 6668                f_ref = f_min; /* Default reference frequency is minimum frequency */
 6669            XLALSimIMRPhenomPCalculateModelParametersOld(
 6670                &chi1_l, &chi2_l, &chip, &thetaJ, &alpha0,
 6671                m1, m2, f_ref,
 6672                LNhatx, LNhaty, LNhatz,
 6673        spin1x, spin1y, spin1z,
 6674        spin2x, spin2y, spin2z, IMRPhenomPv1_V);
 6675            /* Call the waveform driver routine */
 6676            ret = XLALSimIMRPhenomP(hptilde, hctilde,
 6677              chi1_l, chi2_l, chip, thetaJ,
 6678              m1, m2, distance, alpha0, phiRef, deltaF, f_min, f_max, f_ref, IMRPhenomPv1_V, NoNRT_V, NULL);
 6679            if (ret == XLAL_FAILURE) XLAL_ERROR(XLAL_EFUNC);
 6680            break;
 6681 
 6682        case IMRPhenomPv2:
 6683            /* Waveform-specific sanity checks */
 6684      XLALSimInspiralInitialConditionsPrecessingApproxs(&incl,&spin1x,&spin1y,&spin1z,&spin2x,&spin2y,&spin2z,inclination,S1x,S1y,S1z,S2x,S2y,S2z,m1,m2,f_ref,phiRef,XLALSimInspiralGetFrameAxis(waveFlags));
 6685            if( !XLALSimInspiralModesChoiceIsDefault(          /* Default is (2,2) or l=2 modes. */
 6686                    XLALSimInspiralGetModesChoice(waveFlags) ) )
 6687                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralModesChoice provided, but this approximant does not use that flag.");
 6688            if( !checkTidesZero(lambda1, lambda2) )
 6689                XLAL_ERROR(XLAL_EINVAL, "Non-zero tidal parameters were given, but this is approximant doe not have tidal corrections.");
 6690            LNhatx = sin(incl);
 6691            LNhaty = 0.;
 6692            LNhatz = cos(incl);
 6693            /* Tranform to model parameters */
 6694            if(f_ref==0.0)
 6695                f_ref = f_min; /* Default reference frequency is minimum frequency */
 6696            XLALSimIMRPhenomPCalculateModelParametersOld(
 6697                &chi1_l, &chi2_l, &chip, &thetaJ, &alpha0,
 6698                m1, m2, f_ref,
 6699                LNhatx, LNhaty, LNhatz,
 6700                spin1x, spin1y, spin1z,
 6701                spin2x, spin2y, spin2z, IMRPhenomPv2_V);
 6702            /* Call the waveform driver routine */
 6703            ret = XLALSimIMRPhenomP(hptilde, hctilde,
 6704              chi1_l, chi2_l, chip, thetaJ,
 6705              m1, m2, distance, alpha0, phiRef, deltaF, f_min, f_max, f_ref, IMRPhenomPv2_V, NoNRT_V, NULL);
 6706            if (ret == XLAL_FAILURE) XLAL_ERROR(XLAL_EFUNC);
 6707            break;
 6708 
 6709        case SpinTaylorT4Fourier:
 6710            /* Waveform-specific sanity checks */
 6711            if( !XLALSimInspiralFrameAxisIsDefault(
 6712                    XLALSimInspiralGetFrameAxis(waveFlags) ) )
 6713                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralFrameAxis provided, but this approximant does not use that flag.");
 6714            if( !XLALSimInspiralModesChoiceIsDefault(
 6715                    XLALSimInspiralGetModesChoice(waveFlags) ) )
 6716                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralModesChoice provided, but this approximant does not use that flag.");
 6717        spin1x=S1x;
 6718        spin1y=S1y;
 6719        spin1z=S1z;
 6720        spin2x=S2x;
 6721        spin2y=S2y;
 6722        spin2z=S2z;
 6723        ROTATEY(inclination,spin1x,spin1y,spin1z);
 6724        ROTATEY(inclination,spin2x,spin2y,spin2z);
 6725            LNhatx = sin(inclination);
 6726            LNhaty = 0.;
 6727            LNhatz = cos(inclination);
 6728            E1x = 0.;
 6729            E1y = 1.;
 6730            E1z = 0.;
 6731            // default kMax = 3
 6732            kMax = 3;
 6733            // default v0 = 1
 6734            v0 = 1.;
 6735            // default fStart = 0.9*fMin
 6736            fStart = 0.9*f_min;
 6737            phiRefAtEnd = 0;
 6738            // if f_ref = 0, set it to f_min, and tell the driver routine that we came from there
 6739            if(f_ref == 0)
 6740            {
 6741              f_ref = f_min;
 6742              phiRefAtEnd = 1;
 6743            }
 6744            // default quadparams are for black holes. Replace by ~2-12 for neutron stars
 6745            /* Call the waveform driver routine */
 6746            ret = XLALSimInspiralSpinTaylorT4Fourier(hptilde, hctilde,
 6747              f_min, f_max, deltaF, kMax, phiRef, v0, m1, m2, fStart, f_ref, distance, spin1x, spin1y, spin1z, spin2x, spin2y, spin2z, LNhatx, LNhaty, LNhatz, E1x, E1y, E1z, lambda1, lambda2, quadparam1, quadparam2, NULL, phaseO, amplitudeO, phiRefAtEnd);
 6748            if (ret == XLAL_FAILURE) XLAL_ERROR(XLAL_EFUNC);
 6749            break;
 6750 
 6751        case SpinTaylorT5Fourier:
 6752            /* Waveform-specific sanity checks */
 6753            if( !XLALSimInspiralFrameAxisIsDefault(
 6754                    XLALSimInspiralGetFrameAxis(waveFlags) ) )
 6755                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralFrameAxis provided, but this approximant does not use that flag.");
 6756            if( !XLALSimInspiralModesChoiceIsDefault(
 6757                    XLALSimInspiralGetModesChoice(waveFlags) ) )
 6758                XLAL_ERROR(XLAL_EINVAL, "Non-default LALSimInspiralModesChoice provided, but this approximant does not use that flag.");
 6759        spin1x=S1x;
 6760        spin1y=S1y;
 6761        spin1z=S1z;
 6762        spin2x=S2x;
 6763        spin2y=S2y;
 6764        spin2z=S2z;
 6765        ROTATEY(inclination,spin1x,spin1y,spin1z);
 6766        ROTATEY(inclination,spin2x,spin2y,spin2z);
 6767            LNhatx = sin(inclination);
 6768            LNhaty = 0.;
 6769            LNhatz = cos(inclination);
 6770            E1x = 0.;
 6771            E1y = 1.;
 6772            E1z = 0.;
 6773            // default kMax = 3
 6774            kMax = 3;
 6775            // default v0 = 1
 6776            v0 = 1.;
 6777            // default fStart = 0.9*fMin
 6778            fStart = 0.9*f_min;
 6779            phiRefAtEnd = 0;
 6780            // if f_ref = 0, set it to f_min, and tell the driver routine that we came from there
 6781            if(f_ref == 0)
 6782            {
 6783              f_ref = f_min;
 6784              phiRefAtEnd = 1;
 6785            }
 6786            // default quadparams are for black holes. Replace by ~2-12 for neutron stars
 6787            /* Call the waveform driver routine */
 6788            ret = XLALSimInspiralSpinTaylorT5Fourier(hptilde, hctilde,
 6789                             f_min, f_max, deltaF, kMax, phiRef, v0, m1, m2, fStart, f_ref, distance, spin1x, spin1y, spin1z, spin2x, spin2y, spin2z, LNhatx, LNhaty, LNhatz, E1x, E1y, E1z, lambda1, lambda2, quadparam1, quadparam2, NULL, phaseO, amplitudeO, phiRefAtEnd);
 6790            if (ret == XLAL_FAILURE) XLAL_ERROR(XLAL_EFUNC);
 6791            break;
 6792 
 6793 
 6794        default:
 6795            XLALPrintError("FD version of approximant not implemented in lalsimulation\n");
 6796            XLAL_ERROR(XLAL_EINVAL);
 6797    }
 6798 
 6799    REAL8 polariz=longAscNodes;
 6800    if (polariz) {
 6801      COMPLEX16 tmpP,tmpC;
 6802      for (UINT4 idx=0;idx<(*hptilde)->data->length;idx++) {
 6803    tmpP=(*hptilde)->data->data[idx];
 6804    tmpC=(*hctilde)->data->data[idx];
 6805    (*hptilde)->data->data[idx] =cos(2.*polariz)*tmpP+sin(2.*polariz)*tmpC;
 6806    (*hctilde)->data->data[idx]=cos(2.*polariz)*tmpC-sin(2.*polariz)*tmpP;
 6807      }
 6808    }
 6809 
 6810    if (ret == XLAL_FAILURE) XLAL_ERROR(XLAL_EFUNC);
 6811 
 6812    return ret;
 6813}
 6814 
 6815/**
 6816 * if you do NOT provide a quadparam[1,2] term and you DO provide
 6817 * lamdba[1,2] then we calculate quad-mono term using universal relations
 6818 * quadparam[1,2]_UR: Quadrupole-Monopole parameter computed using
 6819 * universal relations (UR)
 6820 */
 6821 
 6822int XLALSimInspiralSetQuadMonParamsFromLambdas(
 6823       LALDict *LALparams /**< LAL dictionary containing accessory parameters */
 6824       )
 6825{
 6826    REAL8 quadparam1 = XLALSimInspiralWaveformParamsLookupdQuadMon1(LALparams);
 6827    REAL8 quadparam2 = XLALSimInspiralWaveformParamsLookupdQuadMon2(LALparams);
 6828    REAL8 lambda1 = XLALSimInspiralWaveformParamsLookupTidalLambda1(LALparams);
 6829    REAL8 lambda2 = XLALSimInspiralWaveformParamsLookupTidalLambda2(LALparams);
 6830 
 6831    if ((lambda1 > 0) && (quadparam1 == 0)) {
 6832        REAL8 quadparam1_UR = XLALSimInspiralEOSQfromLambda(lambda1);
 6833        XLALSimInspiralWaveformParamsInsertdQuadMon1(LALparams, quadparam1_UR - 1.);
 6834    }
 6835 
 6836    if ((lambda2 > 0) && (quadparam2 == 0)) {
 6837        REAL8 quadparam2_UR = XLALSimInspiralEOSQfromLambda(lambda2);
 6838        XLALSimInspiralWaveformParamsInsertdQuadMon2(LALparams, quadparam2_UR - 1.);
 6839    }
 6840    return XLAL_SUCCESS;
 6841}
 6842/** @} */
