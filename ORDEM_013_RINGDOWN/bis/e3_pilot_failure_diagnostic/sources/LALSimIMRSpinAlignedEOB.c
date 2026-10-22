    1/*
    2*  Copyright (C) 2018 Roberto Cotesta, Andrea Taracchini
    3*  Copyright (C) 2011 Craig Robinson, Enrico Barausse, Yi Pan, Prayush Kumar
    4*  (minor changes), Andrea Taracchini
    5*
    6*  This program is free software; you can redistribute it and/or modify
    7*  it under the terms of the GNU General Public License as published by
    8*  the Free Software Foundation; either version 2 of the License, or
    9*  (at your option) any later version.
   10*
   11*  This program is distributed in the hope that it will be useful,
   12*  but WITHOUT ANY WARRANTY; without even the implied warranty of
   13*  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   14*  GNU General Public License for more details.
   15*
   16*  You should have received a copy of the GNU General Public License
   17*  along with with program; see the file COPYING. If not, write to the
   18*  Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
   19*  MA  02110-1301  USA
   20*/
   21 
   22 
   23#include <math.h>
   24#include <complex.h>
   25#include <lal/LALSimInspiral.h>
   26#include <lal/LALSimIMR.h>
   27#include <lal/Date.h>
   28#include <lal/TimeSeries.h>
   29#include <lal/Units.h>
   30#include <lal/LALAdaptiveRungeKuttaIntegrator.h>
   31#include <lal/SphericalHarmonics.h>
   32#include <lal/LALSimSphHarmMode.h>
   33#include <LALSimInspiralWaveformFlags.h>
   34#include <lal/VectorOps.h>
   35 
   36#include <gsl/gsl_sf_gamma.h>
   37#include <gsl/gsl_matrix.h>
   38 
   39#include "LALSimIMREOBNRv2.h"
   40#include "LALSimIMRSpinEOB.h"
   41#include "LALSimInspiralPrecess.h"
   42#include "LALSimInspiralEOBPostAdiabatic.h"
   43 
   44/* Include all the static function files we need */
   45#include "LALSimIMREOBHybridRingdown.c"
   46#include "LALSimIMREOBFactorizedWaveform.c"
   47#include "LALSimIMREOBNewtonianMultipole.c"
   48#include "LALSimIMREOBNQCCorrection.c"
   49#include "LALSimIMRSpinEOBInitialConditions.c"
   50#include "LALSimIMRSpinEOBAuxFuncs.c"
   51#include "LALSimIMRSpinAlignedEOBHcapDerivative.c"
   52#include "LALSimIMRSpinEOBHamiltonian.c"
   53#include "LALSimIMRSpinEOBFactorizedWaveform.c"
   54#include "LALSimIMRSpinEOBFactorizedFlux.c"
   55#include "LALSimIMRSpinEOBFactorizedWaveform_PA.c"
   56/* OPTIMIZED */
   57#include "LALSimIMRSpinEOBHamiltonianOptimized.c"
   58#include "LALSimIMRSpinEOBComputeAmpPhasefromEOMSoln.c"
   59#include "LALSimIMRSpinAlignedEOBGSLOptimizedInterpolation.c"
   60#include "LALSimIMRSpinAlignedEOBHcapDerivativeOptimized.c"
   61#include "LALSimIMRSpinAlignedEOBOptimizedInterpolatorGeneral.c"
   62/* END OPTIMIZED */
   63 
   64 
   65#define debugOutput 0
   66#define SEOBNRv4HM 41
   67#define SEOBNRv4HM_PA 4111
   68#define pSEOBNRv4HM_PA 4112
   69 
   70 
   71//static int debugPK = 0;
   72 
   73#ifdef __GNUC__
   74#define UNUSED __attribute__ ((unused))
   75#else
   76#define UNUSED
   77#endif
   78 
   79 
   80static INT4 IntrpolateDynamics(REAL8Vector* tVec,REAL8Vector* rVec,REAL8Vector* phiVec,REAL8Vector* prVec,REAL8Vector* pphiVec,REAL8Vector* values,REAL8 closestTime){
   81  UNUSED gsl_interp_accel *acc1 = gsl_interp_accel_alloc();
   82  gsl_spline *spline1 = gsl_spline_alloc(gsl_interp_cspline, tVec->length);
   83  gsl_spline_init(spline1, tVec->data, rVec->data, tVec->length);
   84 
   85  UNUSED gsl_interp_accel *acc2 = gsl_interp_accel_alloc();
   86  gsl_spline *spline2 = gsl_spline_alloc(gsl_interp_cspline, tVec->length);
   87  gsl_spline_init(spline2, tVec->data, phiVec->data, tVec->length);
   88 
   89  UNUSED gsl_interp_accel *acc3 = gsl_interp_accel_alloc();
   90  gsl_spline *spline3 = gsl_spline_alloc(gsl_interp_cspline, tVec->length);
   91  gsl_spline_init(spline3, tVec->data, prVec->data, tVec->length);
   92 
   93  UNUSED gsl_interp_accel *acc4 = gsl_interp_accel_alloc();
   94  gsl_spline *spline4 = gsl_spline_alloc(gsl_interp_cspline, tVec->length);
   95  gsl_spline_init(spline4, tVec->data, pphiVec->data, tVec->length);
   96  values->data[0] = gsl_spline_eval(spline1, closestTime, acc1);
   97  values->data[1] = gsl_spline_eval(spline2, closestTime, acc2);
   98  values->data[2] = gsl_spline_eval(spline3, closestTime, acc3);
   99  values->data[3] = gsl_spline_eval(spline4, closestTime, acc4);
  100  //printf("Interpolated values: r=%.17f, phi = %.17f, pr=%.17f, pphi = %.17f\n",values->data[0],values->data[1],values->data[2],values->data[3]);
  101  gsl_spline_free (spline1);
  102  gsl_interp_accel_free (acc1);
  103 
  104  gsl_spline_free (spline2);
  105  gsl_interp_accel_free (acc2);
  106 
  107  gsl_spline_free (spline3);
  108  gsl_interp_accel_free (acc3);
  109 
  110  gsl_spline_free (spline4);
  111  gsl_interp_accel_free (acc4);
  112 
  113  return XLAL_SUCCESS;
  114 
  115}
  116 
  117/**
  118 * ModeArray is a structure which allows to select the modes to include
  119 * in the waveform.
  120 * This function will create a structure with the default modes for every model
  121 */
  122static INT4 XLALSetup_EOB__std_mode_array_structure(
  123    LALValue *ModeArray, UINT4 SpinAlignedEOBversion)
  124{
  125 
  126  /* setup ModeArray */
  127 
  128      if (SpinAlignedEOBversion == SEOBNRv4HM) {
  129        /* Adding all the modes of SEOBNRv4HM
  130        * i.e. [(2,2),(2,1),(3,3),(4,4),(5,5)]
  131        the relative -m modes are added automatically*/
  132        XLALSimInspiralModeArrayActivateMode(ModeArray, 2, 2);
  133        XLALSimInspiralModeArrayActivateMode(ModeArray, 2, 1);
  134        XLALSimInspiralModeArrayActivateMode(ModeArray, 3, 3);
  135        XLALSimInspiralModeArrayActivateMode(ModeArray, 4, 4);
  136        XLALSimInspiralModeArrayActivateMode(ModeArray, 5, 5);
  137      }
  138      else if (SpinAlignedEOBversion == SEOBNRv4HM_PA || SpinAlignedEOBversion == pSEOBNRv4HM_PA) {
  139        /* Adding all the modes of SEOBNRv4HM_PA or pSEOBNRv4HM_PA
  140        * i.e. [(2,2),(2,1),(3,3),(4,4),(5,5)]
  141        the relative -m modes are added automatically*/
  142        XLALSimInspiralModeArrayActivateMode(ModeArray, 2, 2);
  143        XLALSimInspiralModeArrayActivateMode(ModeArray, 2, 1);
  144        XLALSimInspiralModeArrayActivateMode(ModeArray, 3, 3);
  145        XLALSimInspiralModeArrayActivateMode(ModeArray, 4, 4);
  146        XLALSimInspiralModeArrayActivateMode(ModeArray, 5, 5);
  147      }
  148      else{
  149        /*All the other spin aligned model so far only have the 22 mode
  150        */
  151        XLALSimInspiralModeArrayActivateMode(ModeArray, 2, 2);
  152      }
  153 
  154 
  155    return XLAL_SUCCESS;
  156}
  157 
  158/**
  159 * ModeArray is a structure which allows to select the modes to include
  160 * in the waveform.
  161 * This function check if the selected modes are available for a given model
  162 */
  163static INT4 XLALCheck_EOB_mode_array_structure(
  164    LALValue *ModeArray, UINT4 SpinAlignedEOBversion)
  165{
  166  INT4 flagTrue = 0;
  167  UINT4 modeL;
  168  UINT4 modeM;
  169  UINT4 nModes;
  170  const UINT4 lmModes[5][2] = {{2, 2}, {3, 3}, {2, 1}, {4, 4}, {5, 5}};
  171 
  172  if (SpinAlignedEOBversion == SEOBNRv4HM) {
  173    /*If one select SEOBNRv4HM all the modes above are selected to check
  174    */
  175    nModes = 5;
  176  }
  177  else if (SpinAlignedEOBversion == SEOBNRv4HM_PA || SpinAlignedEOBversion == pSEOBNRv4HM_PA) {
  178    /*If one select SEOBNRv4HM_PA all the modes above are selected to check
  179    */
  180    nModes = 5;
  181  }
  182  else{
  183    /*If not only the 22 mode is selected to check
  184    */
  185    nModes = 1;
  186  }
  187  /*Loop over all the possible modes
  188  *we only check +m modes, when one select (l,m) mode is actually
  189  *selecting (l,|m|) mode
  190  */
  191  for (UINT4 ELL = 2; ELL <= LAL_SIM_L_MAX_MODE_ARRAY; ELL++) {
  192    for (UINT4 EMM = 0; EMM <= ELL; EMM++) {
  193      if (XLALSimInspiralModeArrayIsModeActive(ModeArray, ELL, EMM) == 1) {
  194            for (UINT4 k = 0; k < nModes; k++) {
  195              modeL  = lmModes[k][0];
  196              modeM = lmModes[k][1];
  197              if ((modeL == ELL)&&(modeM == EMM)) {
  198                flagTrue=1;
  199              }
  200            }
  201            /*For each active mode check if is available for the selected model
  202            */
  203            if (flagTrue != 1) {
  204              XLALPrintError ("Mode (%d,%d) is not available by the model %d.\n", ELL,
  205                 EMM, SpinAlignedEOBversion);
  206              return XLAL_FAILURE;
  207            }
  208            flagTrue = 0;
  209          }
  210      }
  211    }
  212 
  213    return XLAL_SUCCESS;
  214}
  215 
  216 
  217 
  218 
  219/**
  220 * NR fit to the geometric GW frequency M_{total}omega_{22} of a BNS merger,
  221 * defined by the time when the (2,2) amplitude peaks
  222 * See Eq.(2) in https://arxiv.org/pdf/1504.01764.pdf with coefficients
  223 * given by the 3rd row of Table II therein. Compared to NR for 0 <= kappa2T <= 500
  224 */
  225UNUSED REAL8 XLALSimNSNSMergerFreq(
  226                                       TidalEOBParams *tidal1, /**< Tidal parameters of body 1 */
  227                                       TidalEOBParams *tidal2  /**< Tidal parameters of body 2 */
  228)
  229{
  230    REAL8 X1 = tidal1->mByM;
  231    REAL8 X2 = tidal2->mByM;
  232    REAL8 lambda1 = tidal1->lambda2Tidal; // Dimensionless quadrupolar tidal deformability normalized to M^5
  233    REAL8 lambda2 = tidal2->lambda2Tidal; // Dimensionless quadrupolar tidal deformability normalized to M^5
  234 
  235    REAL8 X1v, X2v, lambda1v, lambda2v;
  236    if ( X1 >= X2 ) {
  237        X1v = X1;
  238        X2v = X2;
  239        lambda1v = lambda1;
  240        lambda2v = lambda2;
  241    }
  242    else {
  243        X1v = X2;
  244        X2v = X1;
  245        lambda1v = lambda2;
  246        lambda2v = lambda1;
  247    }
  248    REAL8 kappa2T = 3*(X2v/X1v*lambda1v + X1v/X2v*lambda2v);
  249    if ( kappa2T < 0. ) {
  250        XLAL_ERROR (XLAL_EFUNC);
  251    }
  252    else {
  253        if ( kappa2T > 500. ) {
  254            kappa2T = 500.;
  255        }
  256       return 0.3596*(1. + 0.024384*kappa2T - 0.000017167*kappa2T*kappa2T)/(1. + 0.068865*kappa2T);
  257    }
  258}
  259 
  260static int UNUSED
  261XLALEOBSpinStopCondition (double UNUSED t,/**<< UNUSED */
  262                          const double values[],  /**<< Dynamical variables */
  263                          double dvalues[],   /**<<1st time-derivatives of dynamical variables */
  264                          void *funcParams  /**<< physical parameters*/
  265  )
  266{
  267 
  268  SpinEOBParams *params = (SpinEOBParams *) funcParams;
  269  double omega_x, omega_y, omega_z, omega;
  270  double r2;
  271 
  272  omega_x = values[1] * dvalues[2] - values[2] * dvalues[1];
  273  omega_y = values[2] * dvalues[0] - values[0] * dvalues[2];
  274  omega_z = values[0] * dvalues[1] - values[1] * dvalues[0];
  275 
  276  r2 = values[0] * values[0] + values[1] * values[1] + values[2] * values[2];
  277  omega =
  278    sqrt (omega_x * omega_x + omega_y * omega_y + omega_z * omega_z) / r2;
  279 
  280  /* Terminate when omega reaches peak, and separation is < 6M */
  281  //if ( omega < params->eobParams->omega )
  282  if (r2 < 36. && omega < params->eobParams->omega)
  283    {
  284      return 1;
  285    }
  286 
  287  params->eobParams->omega = omega;
  288  return GSL_SUCCESS;
  289}
  290 
  291 
  292/**
  293 * Stopping condition for the regular resolution EOB orbital evolution
  294 * -- stop when reaching max orbital frequency in strong field.
  295 * At each test,
  296 * if omega starts to decrease, return 1 to stop evolution;
  297 * if not, update omega with current value and return GSL_SUCCESS to continue evolution.
  298 */
  299static int
  300XLALEOBSpinAlignedStopCondition (double UNUSED t, /**< UNUSED */
  301                                 const double values[],
  302                                                  /**< dynamical variable values */
  303                                 double dvalues[],/**< dynamical variable time derivative values */
  304                                 void *funcParams /**< physical parameters */
  305  )
  306{
  307 
  308  REAL8 omega, r;
  309  SpinEOBParams *params = (SpinEOBParams *) funcParams;
  310 
  311  r = values[0];
  312  omega = dvalues[1];
  313 
  314//  printf("function 1: r = %.16e, omega = %.16e, pr = %.16e, dpr = %.16e, t = %.16e \n",values[0],dvalues[1],values[2],dvalues[2],t);
  315  //if ( omega < params->eobParams->omega )
  316  if (r < 6 && (omega < params->eobParams->omega || dvalues[2] >= 0))
  317    {
  318      params->eobParams->omegaPeaked = 0;
  319      return 1;
  320    }
  321 
  322  params->eobParams->omega = omega;
  323  return GSL_SUCCESS;
  324}
  325 
  326/*
  327 * Stopping condition for the high resolution EOB orbital evolution
  328 * -- stop when reaching a minimum radius 0.3M out of the EOB horizon (Eqs. 9b, 37)
  329 * or when getting nan in any of the four ODE equations
  330 * At each test,
  331 * if conditions met, return 1 to stop evolution;
  332 * if not, return GSL_SUCCESS to continue evolution.
  333 */
  334static int
  335XLALSpinAlignedHiSRStopCondition (double UNUSED t, /**< UNUSED */
  336                                  const double UNUSED values[],/**< dynamical variable values */
  337                                  double dvalues[],     /**< dynamical variable time derivative values */
  338                                  void UNUSED * funcParams     /**< physical parameters */
  339  )
  340{
  341  if (dvalues[0] >= 0. || dvalues[2] >= 0. || isnan (dvalues[3]) || isnan (dvalues[2])
  342      || isnan (dvalues[1]) || isnan (dvalues[0]))
  343    {
  344      return 1;
  345    }
  346  return GSL_SUCCESS;
  347}
  348 
  349/**
  350 * This function defines the stopping criteria for the tidal EOB model
  351 * Note that here
  352 * values[0] = r
  353 * values[1] = phi
  354 * values[2] = pr
  355 * values[3] = pphi
  356 * dvalues[0] = dr/dt
  357 * dvalues[1] = dphi/dt
  358 * dvalues[2] = dpr/dt
  359 * dvalues[3] = dpphi/dt = omega
  360 */
  361static int
  362XLALSpinAlignedNSNSStopCondition (double UNUSED t, /**< UNUSED */
  363                                    const double UNUSED values[],
  364                                                               /**< dynamical variable values */
  365                                    double dvalues[],   /**< dynamical variable time derivative values */
  366                                    void UNUSED * funcParams   /**< physical parameters */
  367  )
  368{
  369  REAL8 omega, r;
  370  UINT4 counter;
  371  SpinEOBParams *params = (SpinEOBParams *) funcParams;
  372  REAL8 rMerger = pow ( params->eobParams->omegaMerger/2., -2./3. );
  373//  printf("rMerger %.16e\n", rMerger);
  374  r = values[0];
  375  omega = dvalues[1];
  376  counter = params->eobParams->omegaPeaked;
  377    REAL8 eta = params->eobParams->eta;
  378  if (debugOutput)   printf("function NSNS: r = %.16e, omega = %.16e, pr = %.16e, dpr = %.16e, count = %.16u\n",values[0],dvalues[1],values[2],dvalues[2],counter);
  379//  printf("%.16e %.16e %.16e %.16e\n",values[0],dvalues[1],values[2],dvalues[2]);
  380  REAL8 rCheck = 1.5*rMerger;
  381  if (r < rCheck && omega < params->eobParams->omega)
  382    {
  383      if (debugOutput) printf("Peak detection %.16e %.16e\n", omega, params->eobParams->omega);
  384      params->eobParams->omegaPeaked = counter + 1;
  385    }
  386  if ( omega >= params->eobParams->omegaMerger/2. ) {
  387      if (debugOutput) printf("Stop at Tim's freq at r=%.16e\n", r);
  388      return 1;
  389  }
  390   if ( r < rCheck && values[2] >= 0 ) {
  391        if (debugOutput) printf("Stop at pr >= 0 at r=%.16e\n", r);
  392        return 1;
  393   }
  394    if ( r < rCheck && dvalues[0] >= 0 ) {
  395        if (debugOutput) printf("Stop at dr/dt >= 0 at r=%.16e\n", r);
  396        return 1;
  397    }
  398   if ( r < rCheck && dvalues[2] >= 0 ) {
  399       params->eobParams->omegaPeaked = counter + 1;
  400       if (debugOutput) printf("Stop at dpr/dt >= 0 at r=%.16e\n", r);
  401       // return 1;
  402  }
  403  if (r < rCheck && params->eobParams->omegaPeaked == 3 )
  404    {
  405     params->eobParams->omegaPeaked = 0;
  406     if (debugOutput) printf("params->eobParams->omegaPeaked == 3 at r=%.16e\n", r);
  407     return 1;
  408  }
  409    if ( isnan (dvalues[3]) || isnan (dvalues[2]) || isnan (dvalues[1]) || isnan (dvalues[0]) ) {
  410        if (debugOutput) printf("Stop at nan's at r=%.16e\n", r);
  411        return 1;
  412    }
  413    if ( fabs(r/params->eobParams->rad - 1.) < 1.e-3*64./5.*eta/(r*r*r*r)*0.02 && fabs(r/params->eobParams->rad - 1.) > 0.) {
  414        if (debugOutput) printf("Radius is stalling at r=%.16e and rad=%.16e\n", r, params->eobParams->rad);
  415        return 1;
  416    }
  417  params->eobParams->omega = omega;
  418  params->eobParams->rad = r;
  419    if( LAL_PI/params->deltaT <= 2.*omega ) {
  420        params->eobParams->NyquistStop = 1;
  421        if (debugOutput) printf("Stop at Nyquist at r=%.16e\n", r);
  422        XLAL_PRINT_WARNING ("Waveform will be generated only up to half the sampling frequency, thus discarding any physical higher-frequency contect above that!\n");
  423        return 1;
  424    }
  425  return GSL_SUCCESS;
  426}
  427 
  428static int
  429XLALSpinAlignedHiSRStopConditionV4 (double UNUSED t, /**< UNUSED */
  430                                    const double UNUSED values[],
  431                                    /**< dynamical variable values */
  432                                    double dvalues[],   /**< dynamical variable time derivative values */
  433                                    void UNUSED * funcParams   /**< physical parameters */
  434)
  435{
  436    REAL8 omega, r;
  437    UINT4 counter;
  438    SpinEOBParams *params = (SpinEOBParams *) funcParams;
  439    r = values[0];
  440    omega = dvalues[1];
  441    counter = params->eobParams->omegaPeaked;
  442    //printf("function 2: r = %.16e, omega = %.16e, pr = %.16e, dpr = %.16e, count = %.16u \n",values[0],dvalues[1],values[2],dvalues[2],counter);
  443    if (r < 6. && omega < params->eobParams->omega)
  444    {
  445        //        printf("Peak detection %.16e %.16e\n", omega, params->eobParams->omega);
  446        params->eobParams->omegaPeaked = counter + 1;
  447    }
  448    if (dvalues[2] >= 0. || params->eobParams->omegaPeaked == 5
  449        || isnan (dvalues[3]) || isnan (dvalues[2]) || isnan (dvalues[1])
  450        || isnan (dvalues[0]))
  451    {
  452        //        if ( dvalues[2] >= 0 ) printf("dvalues[2] >= 0\n");
  453        //        if ( params->eobParams->omegaPeaked == 5 ) printf("params->eobParams->omegaPeaked == 5\n");
  454        //        if ( isnan( dvalues[3] ) || isnan (dvalues[2]) || isnan (dvalues[1]) || isnan (dvalues[0]) ) printf("%.16e %.16e %.16e %.16e\n", dvalues[0], dvalues[1], dvalues[2], dvalues[3]);
  455        return 1;
  456    }
  457    params->eobParams->omega = omega;
  458    return GSL_SUCCESS;
  459}
  460 
  461/**
  462 * @addtogroup LALSimIMRSpinAlignedEOB_c
  463 *
  464 * @author Craig Robinson, Yi Pan
  465 *
  466 * @brief Functions for producing SEOBNRv1 and v2 waveforms.
  467 *
  468 * Functions for producing SEOBNRv1 waveforms for
  469 * spinning binaries, as described in
  470 * Taracchini et al. ( PRD 86, 024011 (2012), arXiv 1202.0790 ).
  471 * All equation numbers in this file refer to equations of this paper,
  472 * unless otherwise specified.
  473 *
  474 * @review SEOBNRv1 has been reviewd by Riccardo Sturani, B. Sathyaprakash and Prayush Kumar.
  475 * The review concluded in fall 2012.
  476 *
  477 * Functions for producing SEOBNRv2 waveforms for
  478 * spinning binaries, as described in
  479 * Taracchini et al. ( arXiv 1311.2544 ).
  480 *
  481 * @review SEOBNRv2 has been reviewed by Riccardo Sturani, Prayush Kumar and Stas Babak.
  482 * The review concluded with git hash 5bc6bb861de2eb72ca403b9e0f529d83080490fe (August 2014).
  483 *
  484 * @{
  485 */
  486 
  487/**
  488 * This function returns the frequency at which the peak amplitude occurs
  489 * in SEOBNRv(x)
  490 *
  491 */
  492double
  493XLALSimIMRSpinAlignedEOBPeakFrequency (REAL8 m1SI,
  494                                /**< mass of companion 1 (kg) */
  495                                       REAL8 m2SI,
  496                                /**< mass of companion 2 (kg) */
  497                                       const REAL8 spin1z,
  498                                /**< z-component of the dimensionless spin of object 1 */
  499                                       const REAL8 spin2z,
  500                                /**< z-component of the dimensionless spin of object 2 */
  501                                       UINT4 SpinAlignedEOBversion
  502                                /**< 1 for SEOBNRv1, 2 for SEOBNRv2, 4 for SEOBNRv4 */
  503  )
  504{
  505 
  506  /* The return variable, frequency in Hz */
  507  double retFreq;
  508 
  509  REAL8 nrOmega;
  510 
  511  /* The mode to use; currently, only l=2, m=2 is supported */
  512  INT4 ll = 2;
  513  INT4 mm = 2;
  514 
  515  /* Mass parameters (we'll work in units of solar mass) */
  516  REAL8 m1 = m1SI / LAL_MSUN_SI;
  517  REAL8 m2 = m2SI / LAL_MSUN_SI;
  518  REAL8 Mtotal = m1 + m2;
  519  REAL8 eta = m1 * m2 / (Mtotal * Mtotal);
  520 
  521  /* We need spin vectors for the SigmaKerr function */
  522  REAL8Vector *sigmaKerr = XLALCreateREAL8Vector (3);
  523  int ii;
  524  REAL8 aa;
  525 
  526  REAL8Vector s1Vec, s2Vec;
  527  s1Vec.length = s2Vec.length = 3;
  528  REAL8 spin1[3] = { 0., 0., spin1z };
  529  REAL8 spin2[3] = { 0., 0., spin2z };
  530  s1Vec.data = spin1;
  531  s2Vec.data = spin2;
  532  /* the SigmaKerr function uses spins, not chis */
  533  for (ii = 0; ii < 3; ii++)
  534    {
  535      s1Vec.data[ii] *= m1 * m1;
  536      s2Vec.data[ii] *= m2 * m2;
  537    }
  538 
  539  /* Calculate the normalized spin of the deformed-Kerr background */
  540  if (XLALSimIMRSpinEOBCalculateSigmaKerr (sigmaKerr, m1, m2, &s1Vec, &s2Vec)
  541      == XLAL_FAILURE)
  542    {
  543      XLALDestroyREAL8Vector (sigmaKerr);
  544      XLAL_ERROR (XLAL_EFUNC);
  545    }
  546 
  547  aa = sigmaKerr->data[2];
  548 
  549  /* Now get the frequency at the peak amplitude */
  550  switch (SpinAlignedEOBversion)
  551    {
  552    case 1:
  553      nrOmega = XLALSimIMREOBGetNRSpinPeakOmega (ll, mm, eta, aa);
  554      break;
  555    case 2:
  556      nrOmega = XLALSimIMREOBGetNRSpinPeakOmegav2 (ll, mm, eta, aa);
  557      break;
  558    case 4:
  559      nrOmega = XLALSimIMREOBGetNRSpinPeakOmegaV4 (ll, mm, eta, aa/(1. - 2.*eta));
  560      break;
  561    case 5:
  562      nrOmega = XLALSimIMREOBGetNRSpinPeakOmegaV5 (ll, mm, eta, aa/(1. - 2.*eta));
  563      break;
  564    default:
  565      XLALPrintError
  566        ("XLAL Error - %s: Unknown SEOBNR version!\nAt present only v1, v2 and v4 are available.\n",
  567         __func__);
  568      XLAL_ERROR (XLAL_EINVAL);
  569      break;
  570    }
  571 
  572  retFreq = nrOmega / (2 * LAL_PI * Mtotal * LAL_MTSUN_SI);
  573 
  574  /* Free memory */
  575  XLALDestroyREAL8Vector (sigmaKerr);
  576 
  577  return retFreq;
  578}
  579 
  580 
  581 
  582int
  583XLALSimIMRSpinAlignedEOBWaveform (
  584    REAL8TimeSeries ** hplus,
  585    /**<< OUTPUT, +-polarization waveform */
  586    REAL8TimeSeries ** hcross,
  587    /**<< OUTPUT, x-polarization waveform */
  588    const REAL8 phiC,
  589    /**<< coalescence orbital phase (rad) */
  590    REAL8 deltaT,
  591    /**<< sampling time step */
  592    const REAL8 m1SI,
  593    /**<< mass-1 in SI unit */
  594    const REAL8 m2SI,
  595    /**<< mass-2 in SI unit */
  596    const REAL8 fMin,
  597    /**<< starting frequency of the 22 mode (Hz) */
  598    const REAL8 r,
  599    /**<< distance in SI unit */
  600    const REAL8 inc,
  601    /**<< inclination angle */
  602    const REAL8 spin1z,
  603    /**<< z-component of spin-1, dimensionless */
  604    const REAL8 spin2z,
  605    /**<< z-component of spin-2, dimensionless */
  606    UINT4 SpinAlignedEOBversion,
  607    /**<< 1 for SEOBNRv1, 2 for SEOBNRv2, 4 for SEOBNRv4,
  608    201 for SEOBNRv2T,401 for SEOBNRv4T, 41 for SEOBNRv4HM,
  609    4111 for SEOBNRv4HM_PA, 4112 for pSEOBNRv4HM_PA */
  610    LALDict *LALParams
  611    /**<< Dictionary of additional wf parameters, including tidal and nonGR */
  612)
  613{
  614  int ret;
  615 
  616  REAL8 lambda2Tidal1 = 0;
  617  REAL8 omega02Tidal1 = 0;
  618  REAL8 lambda3Tidal1 = 0;
  619  REAL8 omega03Tidal1 = 0;
  620  REAL8 lambda2Tidal2 = 0;
  621  REAL8 omega02Tidal2 = 0;
  622  REAL8 lambda3Tidal2 = 0;
  623  REAL8 omega03Tidal2 = 0;
  624  REAL8 quadparam1 = 0;
  625  REAL8 quadparam2 = 0;
  626  REAL8 domega220 = 0;
  627  REAL8 dtau220 = 0;
  628  REAL8 domega210 = 0;
  629  REAL8 dtau210 = 0;
  630  REAL8 domega330 = 0;
  631  REAL8 dtau330 = 0;
  632  REAL8 domega440 = 0;
  633  REAL8 dtau440 = 0;
  634  REAL8 domega550 = 0;
  635  REAL8 dtau550 = 0;
  636  UINT2 TGRflag = 0;
  637 
  638  domega220 = XLALSimInspiralWaveformParamsLookupDOmega220(LALParams);
  639  dtau220 = XLALSimInspiralWaveformParamsLookupDTau220(LALParams);
  640  domega210 = XLALSimInspiralWaveformParamsLookupDOmega210(LALParams);
  641  dtau210 = XLALSimInspiralWaveformParamsLookupDTau210(LALParams);
  642  domega330 = XLALSimInspiralWaveformParamsLookupDOmega330(LALParams);
  643  dtau330 = XLALSimInspiralWaveformParamsLookupDTau330(LALParams);
  644  domega440 = XLALSimInspiralWaveformParamsLookupDOmega440(LALParams);
  645  dtau440 = XLALSimInspiralWaveformParamsLookupDTau440(LALParams);
  646  domega550 = XLALSimInspiralWaveformParamsLookupDOmega550(LALParams);
  647  dtau550 = XLALSimInspiralWaveformParamsLookupDTau550(LALParams);
  648 
  649  if (SpinAlignedEOBversion == 4112) TGRflag = 1;
  650 
  651  LALDict *TGRParams = XLALCreateDict();
  652 
  653  XLALSimInspiralWaveformParamsInsertDOmega220(TGRParams, domega220);
  654  XLALSimInspiralWaveformParamsInsertDTau220(TGRParams, dtau220);
  655  XLALSimInspiralWaveformParamsInsertDOmega210(TGRParams, domega210);
  656  XLALSimInspiralWaveformParamsInsertDTau210(TGRParams, dtau210);
  657  XLALSimInspiralWaveformParamsInsertDOmega330(TGRParams, domega330);
  658  XLALSimInspiralWaveformParamsInsertDTau330(TGRParams, dtau330);
  659  XLALSimInspiralWaveformParamsInsertDOmega440(TGRParams, domega440);
  660  XLALSimInspiralWaveformParamsInsertDTau440(TGRParams, dtau440);
  661  XLALSimInspiralWaveformParamsInsertDOmega550(TGRParams, domega550);
  662  XLALSimInspiralWaveformParamsInsertDTau550(TGRParams, dtau550);
  663 
  664  XLALDictInsertUINT2Value(TGRParams, "TGRflag", TGRflag);
  665 
  666  lambda2Tidal1 = XLALSimInspiralWaveformParamsLookupTidalLambda1(LALParams);
  667  lambda2Tidal2 = XLALSimInspiralWaveformParamsLookupTidalLambda2(LALParams);
  668  if ( (SpinAlignedEOBversion == 201 || SpinAlignedEOBversion == 401) && lambda2Tidal1 != 0. ) {
  669      omega02Tidal1 = XLALSimInspiralWaveformParamsLookupTidalQuadrupolarFMode1(LALParams);
  670      if ( omega02Tidal1 == 0. ) {
  671          XLALPrintError ("XLAL Error - %s: Tidal parameters are not set correctly! Always provide non-zero f-mode frequency when lambda2 is non-zero!\n", __func__);
  672          XLAL_ERROR (XLAL_EDOM);
  673      }
  674      lambda3Tidal1 = XLALSimInspiralWaveformParamsLookupTidalOctupolarLambda1(LALParams);
  675      omega03Tidal1 = XLALSimInspiralWaveformParamsLookupTidalOctupolarFMode1(LALParams);
  676      if ( lambda3Tidal1 != 0. && omega03Tidal1 == 0. ) {
  677          XLALPrintError ("XLAL Error - %s: Tidal parameters are not set correctly! Always provide non-zero octupolar f-mode frequency when lambda3 is non-zero!\n", __func__);
  678          XLAL_ERROR (XLAL_EDOM);
  679      }
  680  }
  681  if ( (SpinAlignedEOBversion == 201 || SpinAlignedEOBversion == 401) && lambda2Tidal2 != 0. ) {
  682      omega02Tidal2 = XLALSimInspiralWaveformParamsLookupTidalQuadrupolarFMode2(LALParams);
  683      if ( omega02Tidal2 == 0. ) {
  684          XLALPrintError ("XLAL Error - %s: Tidal parameters are not set correctly! Always provide non-zero  f-mode frequency when lambda2 is non-zero!\n", __func__);
  685          XLAL_ERROR (XLAL_EDOM);
  686      }
  687      lambda3Tidal2 = XLALSimInspiralWaveformParamsLookupTidalOctupolarLambda2(LALParams);
  688      omega03Tidal2 = XLALSimInspiralWaveformParamsLookupTidalOctupolarFMode2(LALParams);
  689      if ( lambda3Tidal2 != 0. && omega03Tidal2 == 0. ) {
  690          XLALPrintError ("XLAL Error - %s: Tidal parameters are not set correctly! Always provide non-zero octupolar f-mode frequency when lambda3 is non-zero!\n", __func__);
  691          XLAL_ERROR (XLAL_EDOM);
  692      }
  693    }
  694  quadparam1 = 1. + XLALSimInspiralWaveformParamsLookupdQuadMon1(LALParams);
  695  quadparam2 = 1. + XLALSimInspiralWaveformParamsLookupdQuadMon2(LALParams);
  696 
  697  LALValue *ModeArray = XLALSimInspiralWaveformParamsLookupModeArray(LALParams);
  698  /*ModeArray includes the modes chosen by the user
  699  */
  700  if (ModeArray == NULL) {
  701    /*If the user doesn't choose the modes, use the standard modes
  702    */
  703    ModeArray = XLALSimInspiralCreateModeArray();
  704    XLALSetup_EOB__std_mode_array_structure(ModeArray, SpinAlignedEOBversion);
  705  }
  706  /*Check that the modes chosen are available for the given model
  707  */
  708  if(XLALCheck_EOB_mode_array_structure(ModeArray, SpinAlignedEOBversion) == XLAL_FAILURE){
  709    XLALPrintError ("Not available mode chosen.\n");
  710    XLAL_ERROR(XLAL_EFUNC);
  711  }
  712 
  713 
  714 
  715  REAL8Vector *nqcCoeffsInput = XLALCreateREAL8Vector(10);
  716  INT4 nqcFlag = 0;
  717 
  718 
  719  if ( SpinAlignedEOBversion == 401 ) {
  720      nqcFlag = 1;
  721      REAL8 m1BH, m2BH;
  722      m1BH = m1SI / (m1SI + m2SI) * 50. * LAL_MSUN_SI;
  723      m2BH = m2SI / (m1SI + m2SI) * 50. * LAL_MSUN_SI;
  724#if debugOutput
  725      printf("First run SEOBNRv4 to compute NQCs\n");
  726#endif
  727      ret = XLALSimIMRSpinAlignedEOBWaveformAll (
  728        hplus, hcross,
  729        phiC,
  730        1./32768,
  731        m1BH, m2BH,
  732        2*pow(10.,-1.5)/(2.*LAL_PI)/((m1BH + m2BH)*LAL_MTSUN_SI/LAL_MSUN_SI),
  733        r,
  734        inc,
  735        spin1z, spin2z,
  736        400,
  737        0, 0,
  738        0, 0,
  739        0, 0,
  740        0, 0,
  741        0, 0,
  742        nqcCoeffsInput, nqcFlag,
  743        ModeArray,
  744        TGRParams
  745    );
  746      if (ret == XLAL_FAILURE){
  747        if ( nqcCoeffsInput ) XLALDestroyREAL8Vector( nqcCoeffsInput );
  748        if(ModeArray) XLALDestroyValue(ModeArray);
  749        XLALDestroyDict(TGRParams);
  750        XLAL_ERROR(XLAL_EFUNC);
  751      }
  752      nqcFlag = 2;
  753  }
  754#if debugOutput
  755    printf("Generate EOB wf\n");
  756#endif
  757    {
  758      //REAL8Vector *nqcCoeffsInput = XLALCreateREAL8Vector(10);
  759      //INT4 nqcFlag = 0;
  760      ret = XLALSimIMRSpinAlignedEOBWaveformAll (
  761        hplus, hcross,
  762        phiC,
  763        deltaT,
  764        m1SI, m2SI,
  765        fMin,
  766        r,
  767        inc,
  768        spin1z, spin2z,
  769        SpinAlignedEOBversion,
  770        lambda2Tidal1, lambda2Tidal2,
  771        omega02Tidal1, omega02Tidal2,
  772        lambda3Tidal1, lambda3Tidal2,
  773        omega03Tidal1, omega03Tidal2,
  774        quadparam1, quadparam2,
  775        nqcCoeffsInput, nqcFlag,
  776        ModeArray,
  777        TGRParams
  778    );
  779     if (ret == XLAL_FAILURE){
  780       if ( nqcCoeffsInput ) XLALDestroyREAL8Vector( nqcCoeffsInput );
  781       if (ModeArray) XLALDestroyValue(ModeArray);
  782       XLALDestroyDict(TGRParams);
  783       XLAL_ERROR(XLAL_EFUNC);
  784     }
  785      if(ModeArray) XLALDestroyValue(ModeArray);
  786 
  787      if ( nqcCoeffsInput )
  788        XLALDestroyREAL8Vector( nqcCoeffsInput );
  789 
  790        XLALDestroyDict(TGRParams);
  791    }
  792  return ret;
  793}
  794 
  795/**
  796 * This function generates spin-aligned SEOBNRv1,2,2opt,4,4opt,2T,4T,4HM complex modes hlm.
  797 * Currently, only the h22 harmonic is available for all the models with the exception of SEOBNRv4HM
  798 * which contains also the modes hlm =  ((2,1),(3,3),(4,4),(5,5)) besides the (2,2). For this model
  799 * all available harmonics are generated, one cannot choose which harmonic to generate.
  800 * STEP 0) Prepare parameters, including pre-computed coefficients
  801 * for EOB Hamiltonian, flux and waveform
  802 * STEP 1) Solve for initial conditions
  803 * STEP 2) Evolve EOB trajectory until reaching the peak of orbital frequency
  804 * STEP 3) Step back in time by tStepBack and volve EOB trajectory again
  805 * using high sampling rate, stop at 0.3M out of the "EOB horizon".
  806 * STEP 4) Locate the peak of orbital frequency for NQC and QNM calculations
  807 * STEP 5) Calculate NQC correction using hi-sampling data
  808 * STEP 6) Calculate QNM excitation coefficients using hi-sampling data
  809 * STEP 7) Generate full inspiral mode using desired sampling frequency
  810 * STEP 8) Generate full IMR modes -- attaching ringdown to inspiral
  811 * STEP 9) Generate full IMR modes
  812 * Note that sanity checks on merger for SEOBNRv4 have revealed that for
  813 * eta<=0.15 and chi1>0.95 about 0.04% of the waveforms display either
  814 * very shallow double amplitude peak or slightly negave time-derivative of
  815 * the GW freq at merger.
  816 * Note that SEOBNRv2T and SEOBNRv4T can display similar features. The model was
  817 * validated on the range q=[1,3], Sz=[-0.5,0.5], Lambda2=[0,5000]. Waveforms
  818 * will not fail on Sz=[-0.7,0.7], but with possibly stronger unwanted features.
  819 * The initial conditions solver can also fail for low starting frequencies,
  820 * with a failure rate of ~0.3% at fmin=10Hz for M=3Msol.
  821 */
  822int
  823XLALSimIMRSpinAlignedEOBModes (
  824  SphHarmTimeSeries ** hlmmode,
  825  /**<< OUTPUT, mode hlm */
  826  //SM
  827  REAL8Vector ** dynamics_out, /**<< OUTPUT, low-sampling dynamics */
  828  REAL8Vector ** dynamicsHi_out, /**<< OUTPUT, high-sampling dynamics */
  829  //SM
  830  REAL8 deltaT,
  831  /**<< sampling time step */
  832  const REAL8 m1SI,
  833  /**<< mass-1 in SI unit */
  834  const REAL8 m2SI,
  835  /**<< mass-2 in SI unit */
  836  const REAL8 fMin,
  837  /**<< starting frequency of the 22 mode (Hz) */
  838  const REAL8 r,
  839  /**<< distance in SI unit */
  840  const REAL8 spin1z,
  841  /**<< z-component of spin-1, dimensionless */
  842  const REAL8 spin2z,
  843  /**<< z-component of spin-2, dimensionless */
  844  UINT4 SpinAlignedEOBversion,
  845  /**<< 1 for SEOBNRv1, 2 for SEOBNRv2, 4 for SEOBNRv4,
  846  201 for SEOBNRv2T, 401 for SEOBNRv4T, 41 for SEOBNRv4HM,
  847  4111 for SEOBNRv4HM_PA, 4112 for pSEOBNRv4HM_PA */
  848  const REAL8 lambda2Tidal1,
  849  /**<< dimensionless adiabatic quadrupole tidal deformability for body 1 (2/3 k2/C^5) */
  850  const REAL8 lambda2Tidal2,
  851  /**<< dimensionless adiabatic quadrupole tidal deformability for body 2 (2/3 k2/C^5) */
  852  const REAL8 omega02Tidal1,
  853  /**<< quadrupole f-mode angular freq for body 1 m_1*omega_{02,1}*/
  854  const REAL8 omega02Tidal2,
  855  /**<< quadrupole f-mode angular freq for body 2 m_2*omega_{02,2}*/
  856  const REAL8 lambda3Tidal1,
  857  /**<< dimensionless adiabatic octupole tidal deformability for body 1 (2/15 k3/C^7) */
  858  const REAL8 lambda3Tidal2,
  859  /**<< dimensionless adiabatic octupole tidal deformability for body 2 (2/15 k3/C^7) */
  860  const REAL8 omega03Tidal1,
  861  /**<< octupole f-mode angular freq for body 1 m_1*omega_{03,1}*/
  862  const REAL8 omega03Tidal2,
  863  /**<< octupole f-mode angular freq for body 2 m_2*omega_{03,2}*/
  864  const REAL8 quadparam1,
  865  /**<< parameter kappa_1 of the spin-induced quadrupole for body 1, quadrupole is Q_A = -kappa_A m_A^3 chi_A^2 */
  866  const REAL8 quadparam2,
  867  /**<< parameter kappa_2 of the spin-induced quadrupole for body 2, quadrupole is Q_A = -kappa_A m_A^3 chi_A^2 */
  868  REAL8Vector *nqcCoeffsInput,
  869  /**<< Input NQC coeffs */
  870  const INT4 nqcFlag,
  871  /**<< Flag to tell the code to use the NQC coeffs input thorugh nqcCoeffsInput */
  872  LALDict *PAParams,
  873  /**<< Dictionary containing parameters for the post-adiabatic routine */
  874  LALDict *TGRParams
  875  /**<< Dictionary containing parameters for tests of General Relativity */
  876)
  877{
  878  UNUSED REAL8 STEP_SIZE = STEP_SIZE_CALCOMEGA;
  879  INT4 use_tidal = 0;
  880  if ( (lambda3Tidal1 != 0. && lambda2Tidal1 == 0.) || (lambda3Tidal2 != 0. && lambda2Tidal2 == 0.) ) {
  881      XLALPrintError ("XLAL Error - %s: Tidal parameters are not set correctly! You must have a non-zero lambda2 if you provide a non-zero lambda3!\n",
  882                      __func__);
  883      XLAL_ERROR (XLAL_EDOM);
  884  }
  885  if ( SpinAlignedEOBversion==201 || SpinAlignedEOBversion==401 )
  886    {
  887        if ( (lambda2Tidal1 != 0. && omega02Tidal1 == 0.)
  888            || (lambda2Tidal2 != 0. && omega02Tidal2 == 0.) ) {
  889            XLALPrintError ("XLAL Error - %s: Tidal parameters are not set correctly! Always provide non-zero compactness and f-mode frequency when lambda2 is non-zero!\n",
  890                 __func__);
  891            XLAL_ERROR (XLAL_EDOM);
  892        }
  893        if ( (lambda3Tidal1 != 0. && omega03Tidal1 == 0.)
  894            || (lambda3Tidal2 != 0. && omega03Tidal2 == 0.) ) {
  895            XLALPrintError ("XLAL Error - %s: Tidal parameters are not set correctly! Always provide non-zero compactness and f-mode frequency when lambda3 is non-zero!\n",
  896                            __func__);
  897            XLAL_ERROR (XLAL_EDOM);
  898        }
  899        if (fmax(m1SI/m2SI, m2SI/m1SI)>3.) {
  900            XLALPrintWarning("XLAL Warning - %s: Generating waveform with mass ratio outside the recommended range q=[1,3].\n", __func__);
  901        }
  902        if (fabs(spin1z)>0.5 || fabs(spin2z)>0.5) {
  903            XLALPrintWarning("XLAL Warning - %s: Generating waveform with at least one aligned spin component outside the recommended range chi=[-0.5,0.5].\n", __func__);
  904        }
  905        if (lambda2Tidal1>5000. || lambda2Tidal2>5000.) {
  906            XLALPrintWarning("XLAL Warning - %s: Generating waveform with at least one quadrupole tidal deformability outside the recommended range Lambda2=[0,5000].\n", __func__);
  907        }
  908        if ((m1SI+m2SI)/LAL_MSUN_SI*LAL_MTSUN_SI*fMin<1.477e-4) {
  909            XLALPrintWarning("XLAL Warning - %s: Generating waveform with a low starting frequency. Initial conditions solver can fail when pushing the model to lower frequencies, with a rate of failure ~0.3%% at Mf~1.5e-4 (10Hz for M=3Msol).\n", __func__);
  910        }
  911      use_tidal = 1;
  912      if ( SpinAlignedEOBversion==201 )
  913          SpinAlignedEOBversion=2;
  914      if ( SpinAlignedEOBversion==401 )
  915          SpinAlignedEOBversion=4;
  916    }
  917  INT4 use_optimized_v2_or_v4 = 0;
  918  /* If we want SEOBNRv2_opt, then reset SpinAlignedEOBversion=2 and set use_optimized_v2_or_v4=1 */
  919  if (SpinAlignedEOBversion == 200)
  920    {
  921      SpinAlignedEOBversion = 2;
  922      use_optimized_v2_or_v4 = 1;
  923    }
  924  /* If we want SEOBNRv4_opt, then reset SpinAlignedEOBversion=4 and set use_optimized_v4=1 */
  925  if (SpinAlignedEOBversion == 400)
  926    {
  927      SpinAlignedEOBversion = 4;
  928      use_optimized_v2_or_v4 = 1;
  929    }
  930 
  931   INT4 use_hm = 0;
  932    /* The list of available modes */
  933//    const UINT4 lmModes[5][2] = {{2, 2}, {2, 1}, {3, 3}, {4, 4}, {5, 5}};
  934    const UINT4 lmModes[5][2] = {{2, 2}, {3, 3}, {2, 1}, {4, 4},{5, 5}};
  935    REAL8Vector *hLMAllHi = NULL;
  936    REAL8Vector *hLMAll = NULL;
  937    UINT4 nModes = 1;
  938    UINT4 postAdiabaticFlag = 0;
  939    UINT2 TGRflag = 0;
  940 
  941    if (SpinAlignedEOBversion == 4111 || SpinAlignedEOBversion == 4112) {
  942        postAdiabaticFlag = 1;
  943        XLALDictInsertUINT4Value(PAParams, "PAFlag", postAdiabaticFlag);
  944        XLALDictInsertUINT4Value(PAParams, "PAOrder", 8);
  945 
  946        XLALDictInsertREAL8Value(PAParams, "rFinal", 1.8);
  947        XLALDictInsertREAL8Value(PAParams, "rSwitch", 1.8);
  948        XLALDictInsertUINT2Value(PAParams, "analyticFlag", 1);
  949    }
  950 
  951    if (SpinAlignedEOBversion == 4112) {
  952        TGRflag = 1;
  953    }
  954 
  955    /* If we want SEOBNRv4HM, then reset SpinAlignedEOBversion=4 and set use_hm=1 */
  956    if (SpinAlignedEOBversion == 41 || SpinAlignedEOBversion == 4111 || SpinAlignedEOBversion == 4112) {
  957        SpinAlignedEOBversion = 4;
  958        use_hm = 1;
  959        nModes = 5;
  960    }
  961 
  962  /* If the EOB version flag is neither 1, 2, nor 4, exit */
  963  if (SpinAlignedEOBversion != 1 && SpinAlignedEOBversion != 2
  964      && SpinAlignedEOBversion != 4)
  965    {
  966      XLALPrintError
  967        ("XLAL Error - %s: SEOBNR version flag incorrectly set to %u\n",
  968         __func__, SpinAlignedEOBversion);
  969      XLAL_ERROR (XLAL_EERR);
  970    }
  971 
  972  Approximant SpinAlignedEOBapproximant;
  973  switch (SpinAlignedEOBversion)
  974    {
  975    case 1:
  976      SpinAlignedEOBapproximant = SEOBNRv1;
  977      break;
  978    case 2:
  979      SpinAlignedEOBapproximant = SEOBNRv2;
  980      break;
  981    case 4:
  982      SpinAlignedEOBapproximant = SEOBNRv4;
  983      break;
  984    default:
  985      XLALPrintError
  986        ("XLAL Error - %s: SEOBNR version flag incorrectly set to %u\n",
  987         __func__, SpinAlignedEOBversion);
  988      XLAL_ERROR (XLAL_EERR);
  989      break;
  990    }
  991 
  992  /*
  993   * Check spins
  994   */
  995  if (spin1z < -1.0 || spin2z < -1.0)
  996    {
  997      XLALPrintError ("XLAL Error - %s: Component spin less than -1!\n",
  998                      __func__);
  999      XLAL_ERROR (XLAL_EINVAL);
 1000    }
 1001  if (spin1z > 1.0 || spin2z > 1.0)
 1002    {
 1003      XLALPrintError ("XLAL Error - %s: Component spin bigger than 1!\n",
 1004          __func__);
 1005      XLAL_ERROR (XLAL_EINVAL);
 1006    }
 1007  /* If either spin > 0.6, model not available, exit */
 1008  if (SpinAlignedEOBversion == 1 && (spin1z > 0.6 || spin2z > 0.6))
 1009    {
 1010      XLALPrintError
 1011        ("XLAL Error - %s: Component spin larger than 0.6!\nSEOBNRv1 is only available for spins in the range -1 < a/M < 0.6.\n",
 1012         __func__);
 1013      XLAL_ERROR (XLAL_EINVAL);
 1014    }
 1015  /* For v2 the upper bound is 0.99 */
 1016  if ((SpinAlignedEOBversion == 2) && (spin1z > 0.99 || spin2z > 0.99))
 1017    {
 1018      XLALPrintError
 1019        ("XLAL Error - %s: Component spin larger than 0.99!\nSEOBNRv2 and SEOBNRv2_opt are only available for spins in the range -1 < a/M < 0.99.\n",
 1020         __func__);
 1021      XLAL_ERROR (XLAL_EINVAL);
 1022    }
 1023  //R.C: region where SEOBNRv4HM can be generated, see the test on the review page
 1024  //here  https://git.ligo.org/waveforms/reviews/SEOBNRv4HM/wikis/visual-inspection#check-if-there-are-cases-for-which-the-maximum-amplitude-of-the-22-mode-is-smaller-than-the-one-of-any-of-the-higher-order-modes
 1025  if(use_hm){
 1026    if(m1SI>m2SI){
 1027      if((m1SI/m2SI > 57.) && (spin1z> 0.96)){
 1028        XLALPrintError
 1029              ("XLAL Error - %s: Component spin of the more massive BH larger than 0.96 for mass ratio bigger than 57.!\nSEOBNRv4HM \
 1030        for mass ratio bigger than 57 is only available when the spin on the more massive BH in the range -1 < a/M < 0.96.\n",__func__);
 1031        XLAL_ERROR (XLAL_EINVAL);
 1032      }
 1033    }
 1034    if(m2SI>m1SI){
 1035      if((m2SI/m1SI > 57.) && (spin2z> 0.96)){
 1036        XLALPrintError
 1037              ("XLAL Error - %s: Component spin of the more massive BH larger than 0.96 for mass ratio bigger than 57.!\nSEOBNRv4HM \
 1038        for mass ratio bigger than 57 is only available when the spin on the more massive BH in the range -1 < a/M < 0.96.\n",__func__);
 1039        XLAL_ERROR (XLAL_EINVAL);
 1040      }
 1041    }
 1042  }
 1043 
 1044  INT4 i;
 1045 
 1046  REAL8Vector *values = NULL;
 1047 
 1048  /* EOB spin vectors used in the Hamiltonian */
 1049  REAL8Vector *sigmaStar = NULL;
 1050  REAL8Vector *sigmaKerr = NULL;
 1051  REAL8 a, tplspin;
 1052  REAL8 chiS, chiA;
 1053 
 1054  /* Wrapper spin vectors used to calculate sigmas */
 1055  REAL8Vector s1Vec, s1VecOverMtMt;
 1056  REAL8Vector s2Vec, s2VecOverMtMt;
 1057  REAL8 spin1[3] = { 0, 0, spin1z };
 1058  REAL8 spin2[3] = { 0, 0, spin2z };
 1059  REAL8 s1Data[3], s2Data[3], s1DataNorm[3], s2DataNorm[3];
 1060 
 1061  /* Parameters of the system */
 1062  REAL8 m1, m2, mTotal, eta, mTScaled;
 1063  REAL8 amp0;
 1064  LIGOTimeGPS tc = LIGOTIMEGPSZERO;
 1065  /* Dynamics of the system */
 1066  REAL8Vector rVec, phiVec, prVec, pPhiVec,tVec;
 1067  /* OPTIMIZED */
 1068  REAL8Vector ampVec, phaseVec;
 1069  ampVec.data = NULL;
 1070  phaseVec.data = NULL;
 1071  /* END OPTIMIZED */
 1072 
 1073  REAL8 omega, v;
 1074  REAL8Vector *hamVHi;
 1075  REAL8Vector *hamV = NULL;
 1076  REAL8Vector *omegaVec = NULL;
 1077  REAL8Vector *vPhiVec = NULL; //PA
 1078  /* SEOBNRv4HM modes */
 1079  INT4 modeL, modeM;
 1080 
 1081  /* Cartesian vectors needed to calculate Hamiltonian */
 1082  REAL8Vector cartPosVec, cartMomVec;
 1083  REAL8 cartPosData[3], cartMomData[3];
 1084 
 1085  /* Signal mode */
 1086  COMPLEX16 hLM, hT;
 1087  REAL8Vector *sigReVec = NULL, *sigImVec = NULL;
 1088 
 1089  /* Non-quasicircular correction */
 1090  EOBNonQCCoeffs nqcCoeffs;
 1091  COMPLEX16 hNQC;
 1092  REAL8Vector *ampNQC = NULL, *phaseNQC = NULL;
 1093 
 1094  /* Ringdown freq used to check the sample rate */
 1095  COMPLEX16Vector modefreqVec;
 1096  COMPLEX16 modeFreq;
 1097 
 1098  /* We will have to switch to a high sample rate for ringdown attachment */
 1099  REAL8 deltaTHigh;
 1100  UINT4 resampFac;
 1101  UINT4 resampPwr;
 1102  REAL8 resampEstimate;
 1103 
 1104  /* How far will we have to step back to attach the ringdown? */
 1105  REAL8 tStepBack;
 1106  INT4 nStepBack;
 1107 
 1108  /* Dynamics and details of the high sample rate part used to attach the ringdown */
 1109  UINT4 hiSRndx;
 1110  REAL8Vector timeHi, rHi, phiHi, prHi, pPhiHi;
 1111  REAL8Vector *sigReHi = NULL, *sigImHi = NULL;
 1112  REAL8Vector *omegaHi = NULL;
 1113  REAL8Vector *vPhiVecHi = NULL;
 1114  /* Indices of peak frequency and final point */
 1115  /* Needed to attach ringdown at the appropriate point */
 1116  UINT4 peakIdx = 0, finalIdx = 0;
 1117 
 1118  /* Variables for the integrator */
 1119  LALAdaptiveRungeKuttaIntegrator *integrator = NULL;
 1120  REAL8Array *dynamics = NULL;
 1121  REAL8Array *dynamicsHi = NULL;
 1122 
 1123  REAL8Array *dynamicstmp = NULL;       // DAVIDS: MOVING THIS OUTSIDE IF-BLOCK FOR NOW
 1124  REAL8Array *dynamicsHitmp = NULL;     // DAVIDS: MOVING THE VARIABLE DECLARATION OUTSIDE THE IF-BLOCK FOR NOW
 1125  INT4 retLen_fromOptStep2 = 0; // DAVIDS: ONLY SETTING TO ZERO TO SUPRESS COMPILER WARNING
 1126  INT4 retLen_fromOptStep3 = 0; // DAVIDS: ^ DITTO
 1127 
 1128  INT4 retLen;
 1129  REAL8 UNUSED tMax;
 1130 
 1131  /* Accuracies of adaptive Runge-Kutta integrator */
 1132  const REAL8 EPS_ABS = 1.0e-10;
 1133  const REAL8 EPS_REL = 1.0e-9; // Davids: changed exponent from -9 to -10
 1134 
 1135  /*
 1136   * STEP 0) Prepare parameters, including pre-computed coefficients
 1137   *         for EOB Hamiltonian, flux and waveform
 1138   */
 1139 
 1140  /* Parameter structures containing important parameters for the model */
 1141  SpinEOBParams seobParams;
 1142  SpinEOBHCoeffs seobCoeffs;
 1143  EOBParams eobParams;
 1144  FacWaveformCoeffs hCoeffs;
 1145  NewtonMultipolePrefixes prefixes;
 1146  TidalEOBParams tidal1, tidal2;
 1147 
 1148  /* fStart is the start frequency of the 22 mode generation */
 1149  REAL8 fStart;
 1150 
 1151  /* Initialize parameters */
 1152  m1 = m1SI / LAL_MSUN_SI;
 1153  m2 = m2SI / LAL_MSUN_SI;
 1154  mTotal = m1 + m2;
 1155  mTScaled = mTotal * LAL_MTSUN_SI;
 1156  eta = m1 * m2 / (mTotal * mTotal);
 1157 
 1158  /* For v2 the upper bound is mass ratio 100 */
 1159  if ((SpinAlignedEOBversion == 2 || SpinAlignedEOBversion == 4)
 1160      && eta < 100. / 101. / 101.)
 1161    {
 1162      XLALPrintError
 1163        ("XLAL Error - %s: Mass ratio larger than 100!\nSEOBNRv2, SEOBNRv2_opt, SEOBNRv4, and SEOBNRv4_opt are only available for mass ratios up to 100.\n",
 1164         __func__);
 1165      XLAL_ERROR (XLAL_EINVAL);
 1166    }
 1167 
 1168  amp0 = mTotal * LAL_MRSUN_SI / r;
 1169 
 1170  #if debugOutput
 1171  printf("Amp = %.16e\n", amp0);
 1172  #endif
 1173 
 1174  fStart = fMin;
 1175 
 1176   /* If fMin is too high, then for safety in the initial conditions we integrate nonetheless from r=10M */
 1177  if (pow (10., -3. / 2.)/(LAL_PI * mTScaled) < fMin) {
 1178    fStart = pow (10., -3. / 2.)/(LAL_PI * mTScaled);
 1179    //FP    XLAL_PRINT_WARNING ("Waveform will be generated from %f and stored from %f.",fStart,fMin);
 1180  }
 1181 
 1182  /*
 1183  if (pow (LAL_PI * fMin * mTScaled, -2. / 3.) < 10.0)
 1184    {
 1185      XLAL_PRINT_WARNING
 1186        ("Waveform generation may fail due to high starting frequency. The starting frequency corresponds to a small initial radius of %.2fM. We recommend a lower starting frequency that corresponds to an estimated starting radius > 10M.",
 1187         pow (LAL_PI * fMin * mTScaled, -2.0 / 3.0));
 1188    }
 1189  */
 1190 
 1191  /* TODO: Insert potentially necessary checks on the arguments */
 1192 
 1193  /* Calculate the time we will need to step back for ringdown */
 1194  tStepBack = 100. * mTScaled;
 1195  if (SpinAlignedEOBversion == 4)
 1196    {
 1197      tStepBack = 150. * mTScaled;
 1198    }
 1199  //nStepBack = ceil (tStepBack / deltaT);
 1200 
 1201  // printf("odeStep = %e, 5*deltaT/mTscaled=%e, nStepBack = %d\n",odeStep,5*deltaT/mTScaled,nStepBack);
 1202 
 1203  /* Calculate the resample factor for attaching the ringdown */
 1204  /* We want it to be a power of 2 */
 1205  /* If deltaT > Mtot/50, reduce deltaT by the smallest power of two for which deltaT < Mtot/50 */
 1206  resampEstimate = 50. * deltaT / mTScaled;
 1207  resampFac = 1;
 1208  //resampFac = 1 << (UINT4)ceil(log2(resampEstimate));
 1209 
 1210  if (resampEstimate > 1.)
 1211    {
 1212      resampPwr = (UINT4) ceil (log2 (resampEstimate));
 1213      while (resampPwr--)
 1214        {
 1215          resampFac *= 2u;
 1216        }
 1217    }
 1218 
 1219 
 1220  /* Allocate the values vector to contain the initial conditions */
 1221  /* Since we have aligned spins, we can use the 4-d vector as in the non-spin case */
 1222  UINT4 num_elements_in_values_vector = 4;
 1223  if (use_optimized_v2_or_v4)
 1224    /* In v2opt/v4opt, we add an additional two elements to this vector, to store amplitude & phase.
 1225       After ODE solves EOMs (which involves 4 coupled ODEs & thus 4 solution vectors),
 1226       amp & phase are computed explicitly from sparse EOM solution, then interpolated in v2opt/v4opt. */
 1227    num_elements_in_values_vector = 6;
 1228  if (!(values = XLALCreateREAL8Vector (num_elements_in_values_vector)))
 1229    {
 1230      XLAL_ERROR (XLAL_ENOMEM);
 1231    }
 1232  memset (values->data, 0, values->length * sizeof (REAL8));
 1233 
 1234  /* Set up structures and calculate necessary PN parameters */
 1235  /* Unlike the general case, we only need to calculate these once */
 1236  memset (&seobParams, 0, sizeof (seobParams));
 1237  memset (&seobCoeffs, 0, sizeof (seobCoeffs));
 1238  memset (&eobParams, 0, sizeof (eobParams));
 1239  memset (&hCoeffs, 0, sizeof (hCoeffs));
 1240  memset (&prefixes, 0, sizeof (prefixes));
 1241 
 1242  /* Before calculating everything else, check sample freq is high enough */
 1243  modefreqVec.length = 1;
 1244  modefreqVec.data = &modeFreq;
 1245 
 1246  UINT4 mode_highest_freqL = 2;
 1247  UINT4 mode_highest_freqM = 2;
 1248 
 1249  if (use_hm) {
 1250    //RC: if we are using SEOBNRv4HM, the check for the Nyquist frequency
 1251    //should be done for the 55 mode, the frequency of the RD scales with l
 1252    mode_highest_freqL = 5;
 1253    mode_highest_freqM = 5;
 1254  }
 1255 
 1256  if (XLALSimIMREOBGenerateQNMFreqV2
 1257      (&modefreqVec, m1, m2, spin1, spin2, mode_highest_freqL, mode_highest_freqM, 1,
 1258       SpinAlignedEOBapproximant) == XLAL_FAILURE)
 1259    {
 1260      XLALDestroyREAL8Vector (values);
 1261      XLAL_ERROR (XLAL_EFUNC);
 1262    }
 1263 
 1264    /* Check if fMin exceeds 95% the ringdown frequency; if so, don't generate a wf */
 1265    REAL8 fRD = 0.95*creal (modeFreq)/(2.*LAL_PI);
 1266//    UNUSED REAL8 fMerger = GetNRSpinPeakOmegaV4 (2, 2, eta, 0.5*(spin1z + spin2z) + 0.5*(spin1z - spin2z)*(m1 - m2)/(m1 + m2)/(1. - 2.*eta))/(2.*LAL_PI*mTScaled);
 1267//    printf("fMin %.16e\n", fMin);
 1268//    printf("fStart %.16e\n", fStart);
 1269//    printf("fMerger %.16e\n", fMerger);
 1270//    printf("fRD %.16e\n", fRD);
 1271    if ( fMin > fRD ) {
 1272        XLALPrintError
 1273        ("XLAL Error - Starting frequency is above ringdown frequency!\n");
 1274        XLALDestroyREAL8Vector (values);
 1275        XLAL_ERROR (XLAL_EINVAL);
 1276    }
 1277 
 1278  /* If Nyquist freq < 220 QNM freq for SEOBNRv1/2/4 and freq < 550 QNM for SEOBNRv4HM, exit */
 1279  if (use_tidal == 0 && deltaT > LAL_PI / creal (modeFreq))
 1280    {
 1281      XLALPrintError
 1282        ("XLAL Error - %s: Ringdown frequency > Nyquist frequency!\nAt present this situation is not supported.\n",
 1283         __func__);
 1284      XLALDestroyREAL8Vector (values);
 1285     XLAL_ERROR (XLAL_EDOM);
 1286    }
 1287 
 1288  if (!(sigmaStar = XLALCreateREAL8Vector (3)))
 1289    {
 1290      XLALDestroyREAL8Vector (values);
 1291      XLAL_ERROR (XLAL_ENOMEM);
 1292    }
 1293 
 1294  if (!(sigmaKerr = XLALCreateREAL8Vector (3)))
 1295    {
 1296      XLALDestroyREAL8Vector (sigmaStar);
 1297      XLALDestroyREAL8Vector (values);
 1298      XLAL_ERROR (XLAL_ENOMEM);
 1299    }
 1300 
 1301// Rescale tidal polarizabilites by powers of mNS/M
 1302// Rescale f-mode freqs by M/mNS
 1303// No rescaling needed for spin-induced quadrupole parameters
 1304  tidal1.mByM = m1SI / (m1SI + m2SI);
 1305  tidal1.lambda2Tidal = lambda2Tidal1 * pow(tidal1.mByM,5);
 1306  tidal1.omega02Tidal = omega02Tidal1 / tidal1.mByM;
 1307  tidal1.lambda3Tidal = lambda3Tidal1 * pow(tidal1.mByM,7);
 1308  tidal1.omega03Tidal = omega03Tidal1 / tidal1.mByM;
 1309  tidal1.quadparam = quadparam1;
 1310 
 1311  tidal2.mByM = m2SI / (m1SI + m2SI);
 1312  tidal2.lambda2Tidal = lambda2Tidal2 * pow(tidal2.mByM,5);
 1313  tidal2.omega02Tidal = omega02Tidal2 / tidal2.mByM;
 1314  tidal2.lambda3Tidal = lambda3Tidal2 * pow(tidal2.mByM,7);
 1315  tidal2.omega03Tidal = omega03Tidal2 / tidal2.mByM;
 1316  tidal2.quadparam = quadparam2;
 1317 
 1318  seobCoeffs.tidal1 = &tidal1;
 1319  seobCoeffs.tidal2 = &tidal2;
 1320 
 1321  hCoeffs.tidal1 = &tidal1;
 1322  hCoeffs.tidal2 = &tidal2;
 1323 
 1324  seobParams.deltaT = deltaT /( (m1 + m2) * LAL_MTSUN_SI );
 1325  seobParams.alignedSpins = 1;
 1326  seobParams.tortoise = 1;
 1327  seobParams.sigmaStar = sigmaStar;
 1328  seobParams.sigmaKerr = sigmaKerr;
 1329  seobParams.seobCoeffs = &seobCoeffs;
 1330  seobParams.eobParams = &eobParams;
 1331  seobParams.nqcCoeffs = &nqcCoeffs;
 1332  seobParams.use_hm = use_hm;
 1333  eobParams.hCoeffs = &hCoeffs;
 1334  eobParams.prefixes = &prefixes;
 1335  seobParams.postAdiabaticFlag = postAdiabaticFlag;
 1336  eobParams.m1 = m1;
 1337  eobParams.m2 = m2;
 1338  eobParams.eta = eta;
 1339 
 1340  s1Vec.length = s2Vec.length = 3;
 1341  s1VecOverMtMt.length = s2VecOverMtMt.length = 3;
 1342  s1Vec.data = s1Data;
 1343  s2Vec.data = s2Data;
 1344  s1VecOverMtMt.data = s1DataNorm;
 1345  s2VecOverMtMt.data = s2DataNorm;
 1346 
 1347    if ( use_tidal == 1 ) {
 1348        REAL8 omegaMerger = XLALSimNSNSMergerFreq( &tidal1, &tidal2 );
 1349        REAL8 rMerger = pow ( omegaMerger/2., -2./3. );
 1350        if ( pow( fStart*LAL_PI*mTScaled, -2./3. ) <= 2.*rMerger ) {
 1351            XLALPrintError
 1352            ("XLAL Error - %s: fmin is too high for a tidal run, it should be at most %.16e Hz\n", __func__, pow (2.*rMerger, -3. / 2.)/(LAL_PI * mTScaled));
 1353            XLAL_ERROR (XLAL_EINVAL);
 1354        }
 1355    }
 1356 
 1357  /* copy the spins into the appropriate vectors, and scale them by the mass */
 1358  memcpy (s1Data, spin1, sizeof (s1Data));
 1359  memcpy (s2Data, spin2, sizeof (s2Data));
 1360  memcpy (s1DataNorm, spin1, sizeof (s1DataNorm));
 1361  memcpy (s2DataNorm, spin2, sizeof (s2DataNorm));
 1362 
 1363  /* Calculate chiS and chiA */
 1364 
 1365  chiS = 0.5 * (spin1[2] + spin2[2]);
 1366  chiA = 0.5 * (spin1[2] - spin2[2]);
 1367 
 1368  for (i = 0; i < 3; i++)
 1369    {
 1370      s1Data[i] *= m1 * m1;
 1371      s2Data[i] *= m2 * m2;
 1372    }
 1373  for (i = 0; i < 3; i++)
 1374    {
 1375      s1DataNorm[i] = s1Data[i] / mTotal / mTotal;
 1376      s2DataNorm[i] = s2Data[i] / mTotal / mTotal;
 1377    }
 1378  seobParams.s1Vec = &s1VecOverMtMt;
 1379  seobParams.s2Vec = &s2VecOverMtMt;
 1380 
 1381  cartPosVec.length = cartMomVec.length = 3;
 1382  cartPosVec.data = cartPosData;
 1383  cartMomVec.data = cartMomData;
 1384  memset (cartPosData, 0, sizeof (cartPosData));
 1385  memset (cartMomData, 0, sizeof (cartMomData));
 1386 
 1387  /* Populate the initial structures */
 1388  if (XLALSimIMRSpinEOBCalculateSigmaStar (sigmaStar, m1, m2, &s1Vec, &s2Vec)
 1389      == XLAL_FAILURE)
 1390    {
 1391      XLALDestroyREAL8Vector (sigmaKerr);
 1392      XLALDestroyREAL8Vector (sigmaStar);
 1393      XLALDestroyREAL8Vector (values);
 1394      XLAL_ERROR (XLAL_EFUNC);
 1395    }
 1396 
 1397  if (XLALSimIMRSpinEOBCalculateSigmaKerr (sigmaKerr, m1, m2, &s1Vec, &s2Vec)
 1398      == XLAL_FAILURE)
 1399    {
 1400      XLALDestroyREAL8Vector (sigmaKerr);
 1401      XLALDestroyREAL8Vector (sigmaStar);
 1402      XLALDestroyREAL8Vector (values);
 1403      XLAL_ERROR (XLAL_EFUNC);
 1404    }
 1405 
 1406  /* Calculate the value of a */
 1407  /* XXX I am assuming that, since spins are aligned, it is okay to just use the z component XXX */
 1408  /* TODO: Check this is actually the way it works in LAL */
 1409  switch (SpinAlignedEOBversion)
 1410    {
 1411    case 1:
 1412      tplspin = 0.0;
 1413      break;
 1414    case 2:
 1415      tplspin = (1. - 2. * eta) * chiS + (m1 - m2) / (m1 + m2) * chiA;
 1416      break;
 1417    case 4:
 1418      tplspin = (1. - 2. * eta) * chiS + (m1 - m2) / (m1 + m2) * chiA;
 1419      break;
 1420    default:
 1421      XLALPrintError
 1422        ("XLAL Error - %s: Unknown SEOBNR version!\nAt present only v1, v2, and v4 are available.\n",
 1423         __func__);
 1424      if(sigmaKerr){
 1425        XLALDestroyREAL8Vector (sigmaKerr);
 1426      }
 1427      if(sigmaStar){
 1428        XLALDestroyREAL8Vector (sigmaStar);
 1429      }
 1430      if(values){
 1431        XLALDestroyREAL8Vector (values);
 1432      }
 1433      XLAL_ERROR (XLAL_EINVAL);
 1434      break;
 1435    }
 1436  /*for ( i = 0; i < 3; i++ )
 1437     {
 1438     a += sigmaKerr->data[i]*sigmaKerr->data[i];
 1439     }
 1440     a = sqrt( a ); */
 1441  seobParams.a = a = sigmaKerr->data[2];
 1442  seobParams.chi1 = spin1[2];
 1443  seobParams.chi2 = spin2[2];
 1444 
 1445  /* Now compute the spinning H coefficients and store them in seobCoeffs */
 1446    if (XLALSimIMRCalculateSpinEOBHCoeffs
 1447      (&seobCoeffs, eta, a, SpinAlignedEOBversion) == XLAL_FAILURE)
 1448    {
 1449      XLALDestroyREAL8Vector (sigmaKerr);
 1450      XLALDestroyREAL8Vector (sigmaStar);
 1451      XLALDestroyREAL8Vector (values);
 1452      XLAL_ERROR (XLAL_EFUNC);
 1453    }
 1454  //RC: SEOBNRv4HM uses the same dynamics of SEOBNRv4, we momentarily put use_hm = 0 such that it uses the SEOBNRv4 coefficients to compute the flux LALSimIMRSpinEOBFactorizedFlux
 1455  if(use_hm == 1){
 1456    seobParams.use_hm = 0;
 1457  }
 1458  if (XLALSimIMREOBCalcSpinFacWaveformCoefficients
 1459      (&hCoeffs, &seobParams, m1, m2, eta, tplspin, chiS, chiA,
 1460       SpinAlignedEOBversion) == XLAL_FAILURE)
 1461    {
 1462      XLALDestroyREAL8Vector (sigmaKerr);
 1463      XLALDestroyREAL8Vector (sigmaStar);
 1464      XLALDestroyREAL8Vector (values);
 1465      XLAL_ERROR (XLAL_EFUNC);
 1466    }
 1467  if(use_hm == 1){
 1468    seobParams.use_hm = 1;
 1469  }
 1470 
 1471  if (XLALSimIMREOBComputeNewtonMultipolePrefixes
 1472      (&prefixes, eobParams.m1, eobParams.m2) == XLAL_FAILURE)
 1473    {
 1474      XLALDestroyREAL8Vector (sigmaKerr);
 1475      XLALDestroyREAL8Vector (sigmaStar);
 1476      XLALDestroyREAL8Vector (values);
 1477      XLAL_ERROR (XLAL_EFUNC);
 1478    }
 1479 
 1480  switch (SpinAlignedEOBversion)
 1481    {
 1482    case 1:
 1483      if (XLALSimIMRGetEOBCalibratedSpinNQC (&nqcCoeffs, 2, 2, eta, a) ==
 1484          XLAL_FAILURE)
 1485        {
 1486    if(sigmaKerr){
 1487      XLALDestroyREAL8Vector (sigmaKerr);
 1488    }
 1489    if(sigmaStar){
 1490      XLALDestroyREAL8Vector (sigmaStar);
 1491    }
 1492    if(values){
 1493      XLALDestroyREAL8Vector (values);
 1494    }
 1495          XLAL_ERROR (XLAL_EFUNC);
 1496        }
 1497      break;
 1498    case 2:
 1499      if (XLALSimIMRGetEOBCalibratedSpinNQC3D
 1500          (&nqcCoeffs, 2, 2, m1, m2, a, chiA) == XLAL_FAILURE)
 1501        {
 1502    if(sigmaKerr){
 1503      XLALDestroyREAL8Vector (sigmaKerr);
 1504    }
 1505    if(sigmaStar){
 1506      XLALDestroyREAL8Vector (sigmaStar);
 1507    }
 1508    if(values){
 1509      XLALDestroyREAL8Vector (values);
 1510    }
 1511          XLAL_ERROR (XLAL_EFUNC);
 1512        }
 1513      break;
 1514    case 4:
 1515      nqcCoeffs.a1 = 0.;
 1516      nqcCoeffs.a2 = 0.;
 1517      nqcCoeffs.a3 = 0.;
 1518      nqcCoeffs.a3S = 0.;
 1519      nqcCoeffs.a4 = 0.;
 1520      nqcCoeffs.a5 = 0.;
 1521      nqcCoeffs.b1 = 0.;
 1522      nqcCoeffs.b2 = 0.;
 1523      nqcCoeffs.b3 = 0.;
 1524      nqcCoeffs.b4 = 0.;
 1525      break;
 1526    default:
 1527      XLALPrintError
 1528        ("XLAL Error - %s: Unknown SEOBNR version!\nAt present only v1, v2, and v4 are available.\n",
 1529         __func__);
 1530      if(sigmaKerr){
 1531        XLALDestroyREAL8Vector (sigmaKerr);
 1532      }
 1533      if(sigmaStar){
 1534        XLALDestroyREAL8Vector (sigmaStar);
 1535      }
 1536      if(values){
 1537        XLALDestroyREAL8Vector (values);
 1538      }
 1539      XLAL_ERROR (XLAL_EINVAL);
 1540      break;
 1541    }
 1542 
 1543  /*
 1544   * STEP 1) Solve for initial conditions
 1545   */
 1546 
 1547  /* Set the initial conditions. For now we use the generic case */
 1548  /* Can be simplified if spin-aligned initial conditions solver available. The cost of generic code is negligible though. */
 1549  REAL8Vector *tmpValues = XLALCreateREAL8Vector (14);
 1550  if (!tmpValues)
 1551    {
 1552      XLALDestroyREAL8Vector (sigmaKerr);
 1553      XLALDestroyREAL8Vector (sigmaStar);
 1554      XLALDestroyREAL8Vector (values);
 1555      XLAL_ERROR (XLAL_ENOMEM);
 1556    }
 1557 
 1558  memset (tmpValues->data, 0, tmpValues->length * sizeof (REAL8));
 1559 
 1560  /* We set inc zero here to make it easier to go from Cartesian to spherical coords */
 1561  /* No problem setting inc to zero in solving spin-aligned initial conditions. */
 1562  /* inc is not zero in generating the final h+ and hx */
 1563  if (XLALSimIMRSpinEOBInitialConditions
 1564      (tmpValues, m1, m2, fStart, 0, s1Data, s2Data, &seobParams,
 1565       use_optimized_v2_or_v4) == XLAL_FAILURE)
 1566    {
 1567      XLALDestroyREAL8Vector (tmpValues);
 1568      XLALDestroyREAL8Vector (sigmaKerr);
 1569      XLALDestroyREAL8Vector (sigmaStar);
 1570      XLALDestroyREAL8Vector (values);
 1571      XLAL_ERROR (XLAL_EFUNC);
 1572    }
 1573 
 1574//  printf( "ICs = %.16e %.16e %.16e %.16e %.16e %.16e %.16e %.16e %.16e %.16e %.16e %.16e\n", tmpValues->data[0], tmpValues->data[1], tmpValues->data[2],
 1575//     tmpValues->data[3], tmpValues->data[4], tmpValues->data[5], tmpValues->data[6], tmpValues->data[7], tmpValues->data[8],
 1576//     tmpValues->data[9], tmpValues->data[10], tmpValues->data[11] );
 1577 
 1578  /* Taken from Andrea's code */
 1579/*  memset( tmpValues->data, 0, tmpValues->length*sizeof(tmpValues->data[0]));*/
 1580#if 0
 1581  tmpValues->data[0] = 20;
 1582  tmpValues->data[3] = -0.0001008684225106323/eta;
 1583  tmpValues->data[4] = 1.16263606988612/eta / tmpValues->data[0];       // q=8 chi1=0.5
 1584#endif
 1585 
 1586  /* Now convert to Spherical */
 1587  /* The initial conditions code returns Cartesian components of four vectors x, p, S1 and S2,
 1588   * in the special case that the binary starts on the x-axis and the two spins are aligned
 1589   * with the orbital angular momentum along the z-axis.
 1590   * Therefore, in spherical coordinates the initial conditions are
 1591   * r = x; phi = 0.; pr = px; pphi = r * py.
 1592   */
 1593  values->data[0] = tmpValues->data[0];
 1594  values->data[1] = 0.;
 1595  values->data[2] = tmpValues->data[3];
 1596  values->data[3] = tmpValues->data[0] * tmpValues->data[4];
 1597 
 1598  eobParams.rad = values->data[0];
 1599  eobParams.omegaPeaked = 0;
 1600  eobParams.omegaMerger = XLALSimNSNSMergerFreq( &tidal1, &tidal2 );
 1601  eobParams.NyquistStop = 0;
 1602 
 1603  //fprintf( stderr, "Spherical initial conditions: %e %e %e %e\n", values->data[0], values->data[1], values->data[2], values->data[3] );
 1604 
 1605  REAL8Array *dynamicsPA = NULL;
 1606 
 1607  INT4 postAdiabaticOutcome = 0;
 1608 
 1609  if (postAdiabaticFlag)
 1610  {
 1611    XLAL_TRY(XLALSimInspiralEOBPostAdiabatic(
 1612      &dynamicsPA,
 1613      m1,
 1614      m2,
 1615      spin1z,
 1616      spin2z,
 1617      *values,
 1618      SpinAlignedEOBversion,
 1619      &seobParams,
 1620      &nqcCoeffs,
 1621      PAParams
 1622    ), postAdiabaticOutcome);
 1623 
 1624    if (postAdiabaticOutcome == XLAL_ERANGE)
 1625    {
 1626      postAdiabaticFlag=0;
 1627    }
 1628    else if (postAdiabaticOutcome != XLAL_SUCCESS)
 1629    {
 1630      XLAL_ERROR(XLAL_EFUNC, "XLALSimInspiralEOBPostAdiabatic failed!");
 1631    }
 1632    else
 1633    {
 1634      UINT4 rSize;
 1635      rSize = dynamicsPA->dimLength->data[1];
 1636 
 1637      values->data[0] = dynamicsPA->data[2*rSize-1];
 1638      values->data[1] = 0.;
 1639      values->data[2] = dynamicsPA->data[4*rSize-1];
 1640      values->data[3] = dynamicsPA->data[5*rSize-1];
 1641 
 1642      eobParams.rad = values->data[0];
 1643    }
 1644  }
 1645 
 1646  /*
 1647   * STEP 2) Evolve EOB trajectory until reaching the peak of orbital frequency
 1648   */
 1649  REAL8 odeStep = 1.0;
 1650 
 1651  if(postAdiabaticFlag)
 1652    {
 1653      //odeStep = deltaT/mTScaled;
 1654      odeStep = fmax(5*deltaT/mTScaled,1);
 1655    }
 1656  else
 1657    {
 1658      odeStep = deltaT/mTScaled;
 1659    }
 1660 
 1661  nStepBack = ceil (tStepBack / odeStep/ mTScaled);
 1662  /* Now we have the initial conditions, we can initialize the adaptive integrator */
 1663#if debugOutput
 1664    printf("Begin integration\n");
 1665#endif
 1666    if ( use_tidal == 1 ) {
 1667        if (!
 1668            (integrator =
 1669             XLALAdaptiveRungeKutta4Init (4, XLALSpinAlignedHcapDerivative,
 1670                                          XLALSpinAlignedNSNSStopCondition,
 1671                                          EPS_ABS, EPS_REL)))
 1672        {
 1673            XLALDestroyREAL8Vector (values);
 1674            XLAL_ERROR (XLAL_EFUNC);
 1675        }
 1676    }
 1677    else {
 1678        if (use_optimized_v2_or_v4)
 1679        {
 1680            if (!
 1681                (integrator =
 1682                 XLALAdaptiveRungeKutta4InitEighthOrderInstead (4,
 1683                                                          XLALSpinAlignedHcapDerivativeOptimized,
 1684                                                          XLALEOBSpinAlignedStopCondition,
 1685                                                          EPS_ABS, EPS_REL)))
 1686            {
 1687                XLALDestroyREAL8Vector (values);
 1688                XLAL_ERROR (XLAL_EFUNC);
 1689            }
 1690        }
 1691        else
 1692        {
 1693 
 1694          if(postAdiabaticFlag){
 1695              if (!
 1696                  (integrator =
 1697                  XLALAdaptiveRungeKutta4Init (4, XLALSpinAlignedHcapDerivativeOptimized,
 1698            XLALEOBSpinAlignedStopCondition,
 1699            EPS_ABS, EPS_REL)))
 1700              {
 1701                  XLALDestroyREAL8Vector (values);
 1702                  XLAL_ERROR (XLAL_EFUNC);
 1703              }
 1704          }
 1705          else{
 1706            if (!
 1707                  (integrator =
 1708                  XLALAdaptiveRungeKutta4Init (4, XLALSpinAlignedHcapDerivative,
 1709            XLALEOBSpinAlignedStopCondition,
 1710            EPS_ABS, EPS_REL)))
 1711              {
 1712                  XLALDestroyREAL8Vector (values);
 1713                  XLAL_ERROR (XLAL_EFUNC);
 1714              }
 1715          }
 1716        }
 1717    }
 1718 
 1719  integrator->stopontestonly = 1;
 1720  integrator->retries = 1;
 1721 
 1722 
 1723  if (use_optimized_v2_or_v4)
 1724    {
 1725      /* BEGIN OPTIMIZED */
 1726      retLen_fromOptStep2 =
 1727        XLALAdaptiveRungeKutta4NoInterpolate (integrator, &seobParams,
 1728                                              values->data, 0.,
 1729                                              20. / mTScaled,
 1730                                              deltaT / mTScaled, 0., /* ignore deltaT_min, set it to 0 */
 1731                                              &dynamicstmp,2);/* Last parameter added when funcions were combined in LALAdaptiveRungeKuttaIntegrator.c*/
 1732      if (retLen_fromOptStep2 == XLAL_FAILURE || !dynamicstmp)
 1733        {
 1734          XLAL_ERROR (XLAL_EFUNC);
 1735        }
 1736      retLen =
 1737        SEOBNRv2OptimizedInterpolatorNoAmpPhase (dynamicstmp, 0.,
 1738                                                 deltaT / mTScaled,
 1739                                                 retLen_fromOptStep2,
 1740                                                 &dynamics);
 1741      /* END OPTIMIZED */
 1742    }
 1743  else
 1744    {
 1745      //retLen =
 1746        //XLALAdaptiveRungeKutta4NoInterpolate (integrator, &seobParams, values->data, 0.,
 1747                                 //20. / mTScaled, deltaT / mTScaled,0,
 1748                                 //&dynamics,2);
 1749       retLen =
 1750        XLALAdaptiveRungeKutta4 (integrator, &seobParams, values->data, 0.,
 1751                                 20. / mTScaled, odeStep,
 1752                                 &dynamics);
 1753    }
 1754 
 1755  if (retLen == XLAL_FAILURE || dynamics == NULL)
 1756    {
 1757      XLAL_ERROR (XLAL_EFUNC);
 1758    }
 1759 
 1760  REAL8Vector *tVecInterp = NULL;
 1761  REAL8Vector *rVecInterp = NULL;
 1762  REAL8Vector *phiVecInterp = NULL;
 1763  REAL8Vector *prVecInterp = NULL;
 1764  REAL8Vector *pphiVecInterp = NULL;
 1765  INT4 combinedLenForInterp = 0;
 1766 
 1767  if (postAdiabaticFlag && postAdiabaticOutcome == XLAL_SUCCESS)
 1768  {
 1769    const INT4 PALen = dynamicsPA->dimLength->data[1];
 1770 
 1771    REAL8 tStepInterp = deltaT/mTScaled;
 1772    //const INT4 nInterp = ceil((dynamicsPA->data[PALen-1]-dynamicsPA->data[0]) / tStepInterp);
 1773 
 1774    tVecInterp = XLALCreateREAL8Vector(PALen);
 1775    rVecInterp = XLALCreateREAL8Vector(PALen);
 1776    phiVecInterp = XLALCreateREAL8Vector(PALen);
 1777    prVecInterp = XLALCreateREAL8Vector(PALen);
 1778    pphiVecInterp = XLALCreateREAL8Vector(PALen);
 1779 
 1780    for (i = 0; i < PALen; i++)
 1781    {
 1782        tVecInterp->data[i] = dynamicsPA->data[i];
 1783        rVecInterp->data[i] = dynamicsPA->data[PALen + i];
 1784        phiVecInterp->data[i] = dynamicsPA->data[2*PALen + i];
 1785        prVecInterp->data[i] = dynamicsPA->data[3*PALen + i];
 1786        pphiVecInterp->data[i] = dynamicsPA->data[4*PALen + i];
 1787    }
 1788 
 1789    REAL8Array *interpDynamicsPA = NULL;
 1790    interpDynamicsPA = XLALCreateREAL8ArrayL(2, 5, PALen);
 1791 
 1792    for (i = 0; i < PALen; i++)
 1793    {
 1794        interpDynamicsPA->data[i] = tVecInterp->data[i];
 1795        interpDynamicsPA->data[PALen + i] = rVecInterp->data[i];
 1796        interpDynamicsPA->data[2*PALen + i] =   phiVecInterp->data[i];
 1797        interpDynamicsPA->data[3*PALen + i] = prVecInterp->data[i];
 1798        interpDynamicsPA->data[4*PALen + i] = pphiVecInterp->data[i] = dynamicsPA->data[4*PALen + i];
 1799    }
 1800 
 1801    REAL8 tOffset = interpDynamicsPA->data[PALen - 1];
 1802    REAL8 phiOffset = interpDynamicsPA->data[3*PALen - 1];
 1803 
 1804    const INT4 combinedLen = PALen + retLen - 1;
 1805 
 1806    combinedLenForInterp = ceil((dynamics->data[retLen-1]+tOffset-dynamicsPA->data[0]) / tStepInterp) - 1;
 1807    // printf("Last point of integration: %e\n",dynamics->data[retLen-1]+tOffset);
 1808    // printf("First point of PA is %e\n",dynamicsPA->data[0]);
 1809    // printf("The spacing to interpolate to is %e\n",tStepInterp);
 1810    // printf("The length of the array is %d\n",combinedLenForInterp);
 1811    //REAL8 nODE = ceil((dynamics->data[retLen-1]-dynamics->data[0])/tStepInterp);
 1812    //combinedLenForInterp = ceil((dynamicsPA->data[PALen-1]-dynamicsPA->data[0]) / tStepInterp) + nODE - 1;
 1813    REAL8Array *combinedDynamics = NULL;
 1814    combinedDynamics = XLALCreateREAL8ArrayL(2, 5, combinedLen);
 1815 
 1816    for (i = 0; i < PALen; i++)
 1817      {
 1818        combinedDynamics->data[i] = interpDynamicsPA->data[i];
 1819        combinedDynamics->data[combinedLen + i] = interpDynamicsPA->data[PALen + i];
 1820        combinedDynamics->data[2*combinedLen + i] = interpDynamicsPA->data[2*PALen + i];
 1821        combinedDynamics->data[3*combinedLen + i] = interpDynamicsPA->data[3*PALen + i];
 1822        combinedDynamics->data[4*combinedLen + i] = interpDynamicsPA->data[4*PALen + i];
 1823      }
 1824 
 1825    for (i = 1; i < retLen; i++)
 1826      {
 1827        combinedDynamics->data[PALen + i - 1] = dynamics->data[i] + tOffset;
 1828        combinedDynamics->data[combinedLen + PALen + i - 1] = dynamics->data[retLen + i];
 1829        combinedDynamics->data[2*combinedLen + PALen + i - 1] = dynamics->data[2*retLen + i] + phiOffset;
 1830        combinedDynamics->data[3*combinedLen + PALen + i - 1] = dynamics->data[3*retLen + i];
 1831        combinedDynamics->data[4*combinedLen + PALen + i - 1] = dynamics->data[4*retLen + i];
 1832      }
 1833 
 1834    XLALDestroyREAL8Array(dynamics);
 1835    dynamics = combinedDynamics;
 1836 
 1837    retLen = combinedLen;
 1838 
 1839    values->data[0] = dynamics->data[retLen];
 1840    values->data[1] = dynamics->data[2*retLen];
 1841    values->data[2] = dynamics->data[3*retLen];
 1842    values->data[3] = dynamics->data[4*retLen];
 1843 
 1844    eobParams.rad = values->data[0];
 1845 
 1846    XLALDestroyREAL8Array(interpDynamicsPA);
 1847 
 1848    XLALDestroyREAL8Array(dynamicsPA);
 1849    /*
 1850    for (i = 0; i < PALen; i++)
 1851      {
 1852        combinedDynamics->data[i] = dynamicsPA->data[i];
 1853        combinedDynamics->data[combinedLen + i] = dynamicsPA->data[PALen + i];
 1854        combinedDynamics->data[2*combinedLen + i] = dynamicsPA->data[2*PALen + i];
 1855        combinedDynamics->data[3*combinedLen + i] = dynamicsPA->data[3*PALen + i];
 1856        combinedDynamics->data[4*combinedLen + i] = dynamicsPA->data[4*PALen + i];
 1857      }
 1858 
 1859    for (i = 1; i < retLen; i++)
 1860    {
 1861      combinedDynamics->data[PALen + i - 1] = dynamics->data[i] + tOffset;
 1862      combinedDynamics->data[combinedLen + PALen + i - 1] = dynamics->data[retLen + i];
 1863      combinedDynamics->data[2*combinedLen + PALen + i - 1] = dynamics->data[2*retLen + i] + phiOffset;
 1864      combinedDynamics->data[3*combinedLen + PALen + i - 1] = dynamics->data[3*retLen + i];
 1865      combinedDynamics->data[4*combinedLen + PALen + i - 1] = dynamics->data[4*retLen + i];
 1866    }
 1867    */
 1868 
 1869  }
 1870 
 1871  /* Set up pointers to the dynamics */
 1872  // REAL8Vector tVec;
 1873  // tVec.data = dynamics->data;
 1874  // tVec.length = rVec.length = phiVec.length = prVec.length = pPhiVec.length = retLen;
 1875  rVec.length = phiVec.length = prVec.length = pPhiVec.length = retLen;
 1876  rVec.data = dynamics->data + retLen;
 1877  tVec.data = dynamics->data;
 1878  tVec.length = rVec.length;
 1879  phiVec.data = dynamics->data + 2 * retLen;
 1880  prVec.data = dynamics->data + 3 * retLen;
 1881  pPhiVec.data = dynamics->data + 4 * retLen;
 1882 
 1883  // printf( "We think we hit the peak at time %e\n", dynamics->data[retLen-1] );
 1884 
 1885  /* TODO : Insert high sampling rate / ringdown here */
 1886 
 1887  if (tStepBack > retLen * odeStep*mTScaled)
 1888    {
 1889      tStepBack = 0.5 * retLen * odeStep*mTScaled;      //YPnote: if 100M of step back > actual time of evolution, step back 50% of the later
 1890      nStepBack = ceil (tStepBack / odeStep/mTScaled);
 1891    }
 1892 
 1893  //SM
 1894  // retLen is going to be reused for the length of the high-sampling dynamics
 1895  INT4 retLen_out = retLen;
 1896  //SM
 1897 
 1898  /*
 1899   * STEP 3) Step back in time by tStepBack and volve EOB trajectory again
 1900   *         using high sampling rate, stop at 0.3M out of the "EOB horizon".
 1901   */
 1902 
 1903  /* Set up the high sample rate integration */
 1904  hiSRndx = retLen - nStepBack;
 1905  deltaTHigh = deltaT / (REAL8) resampFac;
 1906  //printf("deltaT = %.17f, deltaTHigh = %.17f\n",deltaT,deltaTHigh);
 1907// #if 1
 1908  // printf (
 1909         //   "Stepping back %d points - we expect %d points at high SR\n",
 1910         //   nStepBack, nStepBack * resampFac);
 1911  // printf (
 1912         //   "Commencing high SR integration... from %.16e %.16e %.16e %.16e %.16e\n",
 1913         //   (dynamics->data)[hiSRndx], rVec.data[hiSRndx],
 1914         //   phiVec.data[hiSRndx], prVec.data[hiSRndx], pPhiVec.data[hiSRndx]);
 1915// #endif
 1916 
 1917  values->data[0] = rVec.data[hiSRndx];
 1918  values->data[1] = phiVec.data[hiSRndx];
 1919  values->data[2] = prVec.data[hiSRndx];
 1920  values->data[3] = pPhiVec.data[hiSRndx];
 1921  //printf("Before it begins\n");
 1922  //printf("t=%.17f values: r=%.17f, phi = %.17f, pr=%.17f, pphi = %.17f\n",tVec.data[hiSRndx],values->data[0],values->data[1],values->data[2],values->data[3]);
 1923 
 1924  eobParams.rad = values->data[0];
 1925  eobParams.omegaPeaked = 0;
 1926  eobParams.NyquistStop = 0;
 1927 
 1928  /* If we are doing a post-adibatic run, we need to be more careful.
 1929     In particular because the grid is *not* uniform and has a different
 1930     step than what we want the final waveform on, we need to actually step
 1931     back into a point that *will* be on the final grid. This is needed to
 1932     ensure that when we insert the high-SR waveform after the low-SR, the times
 1933     are consistent.
 1934     To do this, we proceed as follows: determine the point on the final grid that
 1935     is closest to the desired tStepBack. Then interpolate the dynamics to this point
 1936     and begin the high-SR evolution from there. We can also set the highSRndx correctly
 1937     here
 1938  */
 1939  REAL8 tstartHi = 0.0;
 1940  if (postAdiabaticFlag && postAdiabaticOutcome == XLAL_SUCCESS)
 1941    {
 1942      /* The time to which want to step back to */
 1943 
 1944      REAL8 tTarget =  tVec.data[retLen-1]-tStepBack/mTScaled;
 1945      UINT4 ndx = floor(tTarget*mTScaled/deltaT);
 1946      REAL8 closestTime = ndx*deltaT/mTScaled;
 1947      tstartHi = closestTime;
 1948      //printf("tStepBack = %.17f, tend=%.17f, tTarget=%.17f,ndx=%d,closestTime=%.17f\n",tStepBack,tVec.data[retLen-1],tTarget,ndx,closestTime);
 1949      IntrpolateDynamics(&tVec,&rVec,&phiVec,&prVec,&pPhiVec,values,closestTime);
 1950      eobParams.rad = values->data[0];
 1951    }
 1952  /* For HiSR evolution, we stop at a radius 0.3M from the deformed Kerr singularity,
 1953   * or when any derivative of Hamiltonian becomes nan */
 1954  integrator->stop = XLALSpinAlignedHiSRStopCondition;
 1955  if (SpinAlignedEOBversion == 4)
 1956    {
 1957      integrator->stop = XLALSpinAlignedHiSRStopConditionV4;
 1958    }
 1959  if ( use_tidal == 1 ) {
 1960      integrator->stop = XLALSpinAlignedNSNSStopCondition;
 1961    }
 1962 
 1963  if (use_optimized_v2_or_v4)
 1964    {
 1965      /* BEGIN OPTIMIZED: */
 1966      retLen_fromOptStep3 =
 1967        XLALAdaptiveRungeKutta4NoInterpolate (integrator, &seobParams,
 1968                                              values->data, 0.,
 1969                                              20. / mTScaled,
 1970                                              deltaTHigh / mTScaled, 0., /* ignore deltaT_min, set it to 0 */
 1971                                              &dynamicsHitmp,2);/* Last parameter added when funcions were combined in LALAdaptiveRungeKuttaIntegrator.c*/
 1972      if (retLen_fromOptStep3 == XLAL_FAILURE || !dynamicsHitmp)
 1973        {
 1974          XLAL_ERROR (XLAL_EFUNC);
 1975        }
 1976      retLen =
 1977        SEOBNRv2OptimizedInterpolatorNoAmpPhase (dynamicsHitmp, 0.,
 1978                                                 deltaTHigh / mTScaled,
 1979                                                 retLen_fromOptStep3,
 1980                                                 &dynamicsHi);
 1981      /* END OPTIMIZED */
 1982    }
 1983  else
 1984    {
 1985      retLen =
 1986        XLALAdaptiveRungeKutta4 (integrator, &seobParams, values->data, 0.,
 1987                                 20. / mTScaled, deltaTHigh / mTScaled,
 1988                                 &dynamicsHi);
 1989    }
 1990 
 1991  if (retLen == XLAL_FAILURE || dynamicsHi == NULL)
 1992    {
 1993      if(tmpValues){
 1994        XLALDestroyREAL8Vector (tmpValues);
 1995      }
 1996      if(sigmaKerr){
 1997        XLALDestroyREAL8Vector (sigmaKerr);
 1998      }
 1999      if(sigmaStar){
 2000        XLALDestroyREAL8Vector (sigmaStar);
 2001      }
 2002      if(values){
 2003        XLALDestroyREAL8Vector (values);
 2004      }
 2005      XLAL_ERROR (XLAL_EFUNC);
 2006    }
 2007 
 2008  //SM
 2009  // retLen now means the length of the high-sampling dynamics
 2010  // We also keep track of the starting time of the high-sampling dynamics
 2011  INT4 retLenHi_out = retLen;
 2012 
 2013 
 2014 
 2015  if(!postAdiabaticFlag)
 2016  {
 2017    tstartHi = hiSRndx * odeStep;
 2018  }
 2019  // printf("tstartHi = %e\n",tstartHi);
 2020  //SM
 2021 
 2022//  fprintf( stderr, "We got %d points at high SR\n", retLen );
 2023 
 2024  /* Set up pointers to the dynamics */
 2025  rHi.length = phiHi.length = prHi.length = pPhiHi.length = timeHi.length =
 2026    retLen;
 2027  timeHi.data = dynamicsHi->data;
 2028  rHi.data = dynamicsHi->data + retLen;
 2029  phiHi.data = dynamicsHi->data + 2 * retLen;
 2030  prHi.data = dynamicsHi->data + 3 * retLen;
 2031  pPhiHi.data = dynamicsHi->data + 4 * retLen;
 2032 
 2033  REAL8 domega220 = 0;
 2034  REAL8 dtau220 = 0;
 2035  REAL8 domega210 = 0;
 2036  REAL8 dtau210 = 0;
 2037  REAL8 domega330 = 0;
 2038  REAL8 dtau330 = 0;
 2039  REAL8 domega440 = 0;
 2040  REAL8 dtau440 = 0;
 2041  REAL8 domega550 = 0;
 2042  REAL8 dtau550 = 0;
 2043 
 2044  domega220 = XLALSimInspiralWaveformParamsLookupDOmega220(TGRParams);
 2045  dtau220 = XLALSimInspiralWaveformParamsLookupDTau220(TGRParams);
 2046  domega210 = XLALSimInspiralWaveformParamsLookupDOmega210(TGRParams);
 2047  dtau210 = XLALSimInspiralWaveformParamsLookupDTau210(TGRParams);
 2048  domega330 = XLALSimInspiralWaveformParamsLookupDOmega330(TGRParams);
 2049  dtau330 = XLALSimInspiralWaveformParamsLookupDTau330(TGRParams);
 2050  domega440 = XLALSimInspiralWaveformParamsLookupDOmega440(TGRParams);
 2051  dtau440 = XLALSimInspiralWaveformParamsLookupDTau440(TGRParams);
 2052  domega550 = XLALSimInspiralWaveformParamsLookupDOmega550(TGRParams);
 2053  dtau550 = XLALSimInspiralWaveformParamsLookupDTau550(TGRParams);
 2054 
 2055  if (TGRParams && XLALDictContains(TGRParams, "TGRflag")) {
 2056    TGRflag = XLALDictLookupUINT2Value(TGRParams, "TGRflag");
 2057  }
 2058 
 2059  /* Allocate the high sample rate vectors */
 2060  if(dtau220 > 0)
 2061    {
 2062      /*If dtau220>0 we need a larger array than in GR case to accomodate the whole ringdown*/
 2063      sigReHi =
 2064                XLALCreateREAL8Vector (retLen +
 2065                                   (UINT4) ceil (20 * (1. + dtau220) /
 2066                                                 (cimag (modeFreq) * deltaTHigh)));
 2067      sigImHi =
 2068                XLALCreateREAL8Vector (retLen +
 2069                                   (UINT4) ceil (20 * (1. + dtau220) /
 2070                                                 (cimag (modeFreq) * deltaTHigh)));
 2071      omegaHi =
 2072                XLALCreateREAL8Vector (retLen +
 2073                                   (UINT4) ceil (20 * (1. + dtau220) /
 2074                                                 (cimag (modeFreq) * deltaTHigh)));
 2075      vPhiVecHi =
 2076                XLALCreateREAL8Vector (retLen +
 2077                                   (UINT4) ceil (20 * (1. + dtau220) /
 2078                                                 (cimag (modeFreq) * deltaTHigh)));
 2079    }
 2080  else {
 2081    /* Allocate the high sample rate vectors */
 2082      sigReHi =
 2083        XLALCreateREAL8Vector (retLen +
 2084                               (UINT4) ceil (20 /
 2085                                             (cimag (modeFreq) * deltaTHigh)));
 2086      sigImHi =
 2087        XLALCreateREAL8Vector (retLen +
 2088                               (UINT4) ceil (20 /
 2089                                             (cimag (modeFreq) * deltaTHigh)));
 2090      omegaHi =
 2091        XLALCreateREAL8Vector (retLen +
 2092                               (UINT4) ceil (20 /
 2093                                             (cimag (modeFreq) * deltaTHigh)));
 2094      vPhiVecHi =
 2095        XLALCreateREAL8Vector (retLen +
 2096                               (UINT4) ceil (20 /
 2097                                             (cimag (modeFreq) * deltaTHigh)));
 2098 
 2099  }
 2100 
 2101  ampNQC = XLALCreateREAL8Vector (retLen);
 2102  phaseNQC = XLALCreateREAL8Vector (retLen);
 2103  hamVHi = XLALCreateREAL8Vector (retLen);
 2104  //RC: we save the Hamiltonian in a vector such that we can compute it only once
 2105  //and use it for calculate all the modes
 2106 
 2107  if (!sigReHi || !sigImHi || !omegaHi || !ampNQC || !phaseNQC|| !hamVHi)
 2108    {
 2109      if(tmpValues){
 2110        XLALDestroyREAL8Vector (tmpValues);
 2111      }
 2112      if(sigmaKerr){
 2113        XLALDestroyREAL8Vector (sigmaKerr);
 2114      }
 2115      if(sigmaStar){
 2116        XLALDestroyREAL8Vector (sigmaStar);
 2117      }
 2118      if(values){
 2119        XLALDestroyREAL8Vector (values);
 2120      }
 2121      XLAL_ERROR (XLAL_ENOMEM);
 2122    }
 2123 
 2124  memset (sigReHi->data, 0, sigReHi->length * sizeof (sigReHi->data[0]));
 2125  memset (sigImHi->data, 0, sigImHi->length * sizeof (sigImHi->data[0]));
 2126 
 2127  /* Populate the high SR waveform */
 2128  REAL8 omegaOld = 0.0;
 2129  INT4 phaseCounter = 0;
 2130  for (i = 0; i < retLen; i++)
 2131    {
 2132      values->data[0] = rHi.data[i];
 2133      values->data[1] = phiHi.data[i];
 2134      values->data[2] = prHi.data[i];
 2135      values->data[3] = pPhiHi.data[i];
 2136 
 2137      if (use_optimized_v2_or_v4)
 2138        {
 2139          /* OPTIMIZED: */
 2140          omega =
 2141            XLALSimIMRSpinAlignedEOBCalcOmegaOptimized (values->data,
 2142                                                        &seobParams);
 2143          /* END OPTIMIZED: */
 2144        }
 2145      else
 2146        {
 2147 
 2148    if(postAdiabaticFlag){
 2149      omega =
 2150              XLALSimIMRSpinAlignedEOBCalcOmegaOptimized (values->data, &seobParams);
 2151    }
 2152    else{
 2153          omega =
 2154            XLALSimIMRSpinAlignedEOBCalcOmega (values->data, &seobParams, STEP_SIZE);
 2155    }
 2156        }
 2157 
 2158      if (omega < 1.0e-15)
 2159        omega = 1.0e-9;         //YPnote: make sure omega>0 during very-late evolution when numerical errors are huge.
 2160      omegaHi->data[i] = omega; //YPnote: omega<0 is extremely rare and had only happenned after relevant time interval.
 2161      v = cbrt (omega);
 2162 
 2163      if (postAdiabaticFlag){
 2164         vPhiVecHi->data[i] =  XLALSimIMRSpinAlignedEOBNonKeplerCoeffOptimized (values->data, &seobParams);
 2165      }
 2166      /* Calculate the value of the Hamiltonian */
 2167      cartPosVec.data[0] = values->data[0];
 2168      cartMomVec.data[0] = values->data[2];
 2169      cartMomVec.data[1] = values->data[3] / values->data[0];
 2170 
 2171      if (use_optimized_v2_or_v4)
 2172        {
 2173          /* OPTIMIZED: */
 2174          hamVHi->data[i] =
 2175            XLALSimIMRSpinEOBHamiltonianOptimized (eta, &cartPosVec,
 2176                                                   &cartMomVec,
 2177                                                   &s1VecOverMtMt,
 2178                                                   &s2VecOverMtMt, sigmaKerr,
 2179                                                   sigmaStar,
 2180                                                   seobParams.tortoise,
 2181                                                   &seobCoeffs);
 2182          /* END OPTIMIZED: */
 2183        }
 2184      else
 2185        {
 2186          hamVHi->data[i] =
 2187            XLALSimIMRSpinEOBHamiltonian (eta, &cartPosVec, &cartMomVec,
 2188                                          &s1VecOverMtMt, &s2VecOverMtMt,
 2189                                          sigmaKerr, sigmaStar,
 2190                                          seobParams.tortoise, &seobCoeffs);
 2191        }
 2192 
 2193      if (omega <= omegaOld && !peakIdx)
 2194        {
 2195//      printf( "Have we got the peak? omegaOld = %.16e, omega = %.16e\n", omegaOld, omega );
 2196          peakIdx = i;
 2197        }
 2198      omegaOld = omega;
 2199    }
 2200 
 2201  finalIdx = retLen - 1;
 2202  if (!peakIdx)
 2203    peakIdx = finalIdx;
 2204 
 2205//  printf( "We now think the peak is at %d\n", peakIdx );
 2206#if debugOutput
 2207    FILE *out = fopen ("saDynamicsHi.dat", "w");
 2208    for (i = 0; i < retLen; i++)
 2209    {
 2210        fprintf (out, "%.16e %.16e %.16e %.16e %.16e %.16e\n", timeHi.data[i],
 2211                 rHi.data[i], phiHi.data[i], prHi.data[i], pPhiHi.data[i], omegaHi->data[i]);
 2212    }
 2213    fclose (out);
 2214#endif
 2215 
 2216  /*
 2217   * STEP 4) Locate the peak of orbital frequency for NQC and QNM calculations
 2218   */
 2219 
 2220  /* Stuff to find the actual peak time */
 2221  gsl_spline *spline = NULL;
 2222  gsl_interp_accel *acc = NULL;
 2223  REAL8 omegaDeriv1;            //, omegaDeriv2;
 2224  REAL8 time1, time2;
 2225  REAL8 timePeak, timewavePeak = 0., omegaDerivMid;
 2226  REAL8 sigAmpSqHi = 0., oldsigAmpSqHi = 0.;
 2227  INT4 peakCount = 0;
 2228 
 2229  spline = gsl_spline_alloc (gsl_interp_cspline, retLen);
 2230  acc = gsl_interp_accel_alloc ();
 2231 
 2232  time1 = dynamicsHi->data[peakIdx];
 2233 
 2234  gsl_spline_init (spline, dynamicsHi->data, omegaHi->data, retLen);
 2235  omegaDeriv1 = gsl_spline_eval_deriv (spline, time1, acc);
 2236  if (omegaDeriv1 > 0.)
 2237    {
 2238      time2 = dynamicsHi->data[peakIdx + 1];
 2239      //omegaDeriv2 = gsl_spline_eval_deriv( spline, time2, acc );
 2240    }
 2241  else
 2242    {
 2243      //omegaDeriv2 = omegaDeriv1;
 2244      time2 = time1;
 2245      time1 = dynamicsHi->data[peakIdx - 1];
 2246      peakIdx--;
 2247      omegaDeriv1 = gsl_spline_eval_deriv (spline, time1, acc);
 2248    }
 2249 
 2250  do
 2251    {
 2252      timePeak = (time1 + time2) / 2.;
 2253      omegaDerivMid = gsl_spline_eval_deriv (spline, timePeak, acc);
 2254 
 2255      if (omegaDerivMid * omegaDeriv1 < 0.0)
 2256        {
 2257          //omegaDeriv2 = omegaDerivMid;
 2258          time2 = timePeak;
 2259        }
 2260      else
 2261        {
 2262          omegaDeriv1 = omegaDerivMid;
 2263          time1 = timePeak;
 2264        }
 2265    }
 2266  while (time2 - time1 > 1.0e-5);
 2267 
 2268//    if (use_tidal == 1)
 2269//        timePeak = dynamicsHi->data[retLen-1];
 2270 
 2271 
 2272gsl_spline_free( spline );
 2273gsl_interp_accel_free( acc );
 2274 
 2275 
 2276  //XLALPrintInfo( "Estimation of the peak is now at time %.16e\n", timePeak );
 2277 
 2278 
 2279  /*
 2280   * STEP 5) Calculate NQC correction using hi-sampling data
 2281   */
 2282 
 2283  /* Calculate nonspin and amplitude NQC coefficients from fits and interpolation table */
 2284  /*switch ( SpinAlignedEOBversion )
 2285     {
 2286     case 1:
 2287     if ( XLALSimIMRGetEOBCalibratedSpinNQC( &nqcCoeffs, 2, 2, eta, a ) == XLAL_FAILURE )
 2288     {
 2289     XLAL_ERROR( XLAL_EFUNC );
 2290     }
 2291     break;
 2292     case 2:
 2293     if ( XLALSimIMRGetEOBCalibratedSpinNQC3D( &nqcCoeffs, 2, 2, eta, a, chiA ) == XLAL_FAILURE )
 2294     {
 2295     XLAL_ERROR( XLAL_EFUNC );
 2296     }
 2297     break;
 2298     default:
 2299     XLALPrintError( "XLAL Error - %s: Unknown SEOBNR version!\nAt present only v1 and v2 are available.\n", __func__);
 2300     XLAL_ERROR( XLAL_EINVAL );
 2301     break;
 2302     } */
 2303 
 2304    /* Calculate the time of amplitude peak. Despite the name, this is in fact the shift in peak time from peak orb freq time */
 2305    switch (SpinAlignedEOBversion)
 2306    {
 2307        case 1:
 2308            timewavePeak = XLALSimIMREOBGetNRSpinPeakDeltaT (2, 2, eta, a);
 2309            break;
 2310        case 2:
 2311            timewavePeak = XLALSimIMREOBGetNRSpinPeakDeltaTv2 (2, 2, m1, m2, spin1z, spin2z);   // David debug: we need to be using v2 for SpinAlignedEOBversion 2, right?
 2312            break;
 2313        case 4:
 2314            timewavePeak =
 2315            XLALSimIMREOBGetNRSpinPeakDeltaTv4 (2, 2, m1, m2, spin1z, spin2z);
 2316            break;
 2317        default:
 2318            XLALPrintError
 2319            ("XLAL Error - %s: Unknown SEOBNR version!\nAt present only v1 and v2 are available.\n",
 2320             __func__);
 2321             if(tmpValues){
 2322               XLALDestroyREAL8Vector (tmpValues);
 2323             }
 2324             if(sigmaKerr){
 2325               XLALDestroyREAL8Vector (sigmaKerr);
 2326             }
 2327             if(sigmaStar){
 2328               XLALDestroyREAL8Vector (sigmaStar);
 2329             }
 2330             if(values){
 2331               XLALDestroyREAL8Vector (values);
 2332             }
 2333             if(sigReHi){
 2334               XLALDestroyREAL8Vector(sigReHi);
 2335             }
 2336             if(sigImHi){
 2337               XLALDestroyREAL8Vector(sigImHi);
 2338             }
 2339             if(omegaHi){
 2340               XLALDestroyREAL8Vector(omegaHi);
 2341             }
 2342             if(vPhiVecHi){
 2343               XLALDestroyREAL8Vector(vPhiVecHi);
 2344             }
 2345             if(ampNQC){
 2346               XLALDestroyREAL8Vector(ampNQC);
 2347             }
 2348             if(phaseNQC){
 2349               XLALDestroyREAL8Vector(phaseNQC);
 2350             }
 2351             if(hamVHi){
 2352               XLALDestroyREAL8Vector(hamVHi);
 2353             }
 2354            XLAL_ERROR (XLAL_EINVAL);
 2355            break;
 2356    }
 2357    if (use_tidal == 1) {
 2358        timewavePeak = 0.;
 2359    }    /*                      */
 2360 
 2361    /* Evaluating the modes */
 2362 
 2363    /*The for over the modes should start here */
 2364    // REAL8 nqcCoeffsMatrix[nModes][10];    //RC: Andrea coded the 2d array in this way. It works in C99 and indeed I don't get any errors when compiling, but I think this should be deprecated, it's better the gsl matrix
 2365    gsl_matrix * nqcCoeffsMatrix = gsl_matrix_alloc (nModes, 10);
 2366 
 2367 
 2368  if(use_hm == 1)
 2369    {
 2370    //RC for the SEOBNRv4HM model we need to compute again the coefficients for the modes because they are different from those using for computing the flux LALSimIMRSpinEOBFactorizedFlux.
 2371    if (XLALSimIMREOBCalcSpinFacWaveformCoefficients
 2372        (&hCoeffs, &seobParams, m1, m2, eta, tplspin, chiS, chiA,
 2373         SpinAlignedEOBversion) == XLAL_FAILURE)
 2374      {
 2375        if(tmpValues){
 2376          XLALDestroyREAL8Vector (tmpValues);
 2377        }
 2378        if(sigmaKerr){
 2379          XLALDestroyREAL8Vector (sigmaKerr);
 2380        }
 2381        if(sigmaStar){
 2382          XLALDestroyREAL8Vector (sigmaStar);
 2383        }
 2384        if(values){
 2385          XLALDestroyREAL8Vector (values);
 2386        }
 2387        if(sigReHi){
 2388          XLALDestroyREAL8Vector(sigReHi);
 2389        }
 2390        if(sigImHi){
 2391          XLALDestroyREAL8Vector(sigImHi);
 2392        }
 2393        if(omegaHi){
 2394          XLALDestroyREAL8Vector(omegaHi);
 2395        }
 2396        if(vPhiVecHi){
 2397               XLALDestroyREAL8Vector(vPhiVecHi);
 2398             }
 2399        if(ampNQC){
 2400          XLALDestroyREAL8Vector(ampNQC);
 2401        }
 2402        if(phaseNQC){
 2403          XLALDestroyREAL8Vector(phaseNQC);
 2404        }
 2405        if(hamVHi){
 2406          XLALDestroyREAL8Vector(hamVHi);
 2407        }
 2408        XLAL_ERROR (XLAL_EFUNC);
 2409      }
 2410      if((fabs(m1-m2) == 0) && (chiA == 0)){
 2411        //RC: in the case of equal mass equal spins (where odd m modes are 0), the calibration parameter is 0
 2412      }
 2413      else{
 2414      //RC: in addition to the PN coefficient, here we also need to evaluate a spinning pseudo-PN coefficient for the 21 and the 55 mode. These coefficients do not break
 2415      //the odd mode's symmetry and for this reason they are 0 if chiS == chiA == 0. This of course hold also for non-spinning configurations.
 2416        XLALSimIMREOBCalcCalibCoefficientHigherModes(&hCoeffs, &seobParams,2,1,&phiHi,&rHi,&prHi,
 2417              omegaHi,hamVHi,&pPhiHi,timePeak -timewavePeak,m1,m2,chiS,chiA,deltaTHigh / mTScaled);
 2418        XLALSimIMREOBCalcCalibCoefficientHigherModes(&hCoeffs, &seobParams,5,5,&phiHi,&rHi,&prHi,
 2419                    omegaHi,hamVHi,&pPhiHi,timePeak -timewavePeak- 10,m1,m2,chiS,chiA,deltaTHigh / mTScaled);
 2420        //RC: The - 10 here is because for the 55 mode the attachment is done at timePeak -timewavePeak- 10. timewavePeak is computed here outside
 2421        //the for loop for the modes, for this reason I'm putting the -10 by hand, if it was inside the loop I could have used XLALSimIMREOBGetNRSpinPeakDeltaTv4 (5, 5, m1, m2, spin1z, spin2z)
 2422      }
 2423    }
 2424 
 2425 
 2426 
 2427 
 2428    hLMAllHi = XLALCreateREAL8Vector((UINT4)2*sigReHi->length*nModes);
 2429    INT4 status = XLAL_SUCCESS;
 2430    memset(hLMAllHi->data, 0, hLMAllHi->length*sizeof (REAL8));
 2431for ( UINT4 k = 0; k<nModes; k++) {
 2432    modeL  = lmModes[k][0];
 2433    modeM = lmModes[k][1];
 2434#if debugOutput
 2435    char filename2[sizeof "saModesXXHi.dat"];
 2436    sprintf(filename2,"saModes%01d%01dHi.dat",modeL,modeM);
 2437    out = fopen (filename2, "w");
 2438#endif
 2439    for(i=0; i<retLen; i++){
 2440        values->data[0] = rHi.data[i];
 2441        values->data[1] = phiHi.data[i];
 2442        values->data[2] = prHi.data[i];
 2443        values->data[3] = pPhiHi.data[i];
 2444        v = cbrt (omegaHi->data[i]);
 2445        if (postAdiabaticFlag)
 2446        {
 2447          status = XLALSimIMRSpinEOBGetSpinFactorizedWaveform_PA(&hLM, values, v, hamVHi->data[i], modeL, modeM, &seobParams,
 2448                                                                 vPhiVecHi->data[i]);
 2449        }
 2450        else
 2451        {
 2452           status = XLALSimIMRSpinEOBGetSpinFactorizedWaveform(&hLM, values, v, hamVHi->data[i], modeL, modeM, &seobParams,
 2453                                                              use_optimized_v2_or_v4);
 2454        }
 2455 
 2456          if (status == XLAL_FAILURE)
 2457        {
 2458            if(tmpValues){
 2459              XLALDestroyREAL8Vector (tmpValues);
 2460            }
 2461            if(sigmaKerr){
 2462              XLALDestroyREAL8Vector (sigmaKerr);
 2463            }
 2464            if(sigmaStar){
 2465              XLALDestroyREAL8Vector (sigmaStar);
 2466            }
 2467            if(values){
 2468              XLALDestroyREAL8Vector (values);
 2469            }
 2470            if(sigReHi){
 2471              XLALDestroyREAL8Vector(sigReHi);
 2472            }
 2473            if(sigImHi){
 2474              XLALDestroyREAL8Vector(sigImHi);
 2475            }
 2476            if(omegaHi){
 2477              XLALDestroyREAL8Vector(omegaHi);
 2478            }
 2479            if(vPhiVecHi){
 2480               XLALDestroyREAL8Vector(vPhiVecHi);
 2481             }
 2482            if(ampNQC){
 2483              XLALDestroyREAL8Vector(ampNQC);
 2484            }
 2485            if(phaseNQC){
 2486              XLALDestroyREAL8Vector(phaseNQC);
 2487            }
 2488            if(hamVHi){
 2489              XLALDestroyREAL8Vector(hamVHi);
 2490            }
 2491            if(hLMAllHi){
 2492              XLALDestroyREAL8Vector(hLMAllHi);
 2493            }
 2494            XLAL_ERROR (XLAL_EFUNC);
 2495        }
 2496#if debugOutput
 2497        fprintf (out, "%.16e %.16e %.16e\n", timeHi.data[i],
 2498                 creal (hLM) , cimag (hLM ) );
 2499#endif
 2500        ampNQC->data[i] = cabs (hLM);
 2501        sigReHi->data[i] = (REAL8) (amp0 * creal (hLM));
 2502        sigImHi->data[i] = (REAL8) (amp0 * cimag (hLM));
 2503        phaseNQC->data[i] = carg (hLM) + phaseCounter * LAL_TWOPI;
 2504 
 2505        if (i && phaseNQC->data[i] > phaseNQC->data[i - 1])
 2506        {
 2507            phaseCounter--;
 2508            phaseNQC->data[i] -= LAL_TWOPI;
 2509        }
 2510 
 2511    }
 2512#if debugOutput
 2513    fclose (out);
 2514#endif
 2515 
 2516 
 2517 
 2518 
 2519  if (SpinAlignedEOBversion == 4)
 2520    {
 2521        if ( use_tidal == 1 && nqcFlag == 2 ) {
 2522            nqcCoeffs.a1 = nqcCoeffsInput->data[0];
 2523            nqcCoeffs.a2 = nqcCoeffsInput->data[1];
 2524            nqcCoeffs.a3 = nqcCoeffsInput->data[2];
 2525            nqcCoeffs.a3S = nqcCoeffsInput->data[3];
 2526            nqcCoeffs.a4 = nqcCoeffsInput->data[4];
 2527            nqcCoeffs.a5 = nqcCoeffsInput->data[5];
 2528            nqcCoeffs.b1 = nqcCoeffsInput->data[6];
 2529            nqcCoeffs.b2 = nqcCoeffsInput->data[7];
 2530            nqcCoeffs.b3 = nqcCoeffsInput->data[8];
 2531            nqcCoeffs.b4 = nqcCoeffsInput->data[9];
 2532        }
 2533        else {
 2534          if(eta == 0.25 && chiA == 0 && ( (modeL == 2 && modeM == 1) || (modeL == 3 && modeM == 3)|| (modeL == 5 && modeM == 5) ) ) { //RC:Since the mode is 0 by symmetry, we don't need to compute the NQCs
 2535            nqcCoeffs.a1 = 0.;
 2536            nqcCoeffs.a2 = 0.;
 2537            nqcCoeffs.a3 = 0.;
 2538            nqcCoeffs.a3S = 0.;
 2539            nqcCoeffs.a4 = 0.;
 2540            nqcCoeffs.a5 = 0.;
 2541            nqcCoeffs.b1 = 0.;
 2542            nqcCoeffs.b2 = 0.;
 2543            nqcCoeffs.b3 = 0.;
 2544            nqcCoeffs.b4 = 0.;
 2545          }
 2546          else{
 2547            if (XLALSimIMRSpinEOBCalculateNQCCoefficientsV4
 2548                (ampNQC, phaseNQC, &rHi, &prHi, omegaHi, modeL, modeM, timePeak,
 2549                 deltaTHigh / mTScaled, m1, m2, chiA, chiS, &nqcCoeffs) == XLAL_FAILURE)
 2550 
 2551            {
 2552              if(tmpValues){
 2553                XLALDestroyREAL8Vector (tmpValues);
 2554              }
 2555              if(sigmaKerr){
 2556                XLALDestroyREAL8Vector (sigmaKerr);
 2557              }
 2558              if(sigmaStar){
 2559                XLALDestroyREAL8Vector (sigmaStar);
 2560              }
 2561              if(values){
 2562                XLALDestroyREAL8Vector (values);
 2563              }
 2564              if(sigReHi){
 2565                XLALDestroyREAL8Vector(sigReHi);
 2566              }
 2567              if(sigImHi){
 2568                XLALDestroyREAL8Vector(sigImHi);
 2569              }
 2570              if(omegaHi){
 2571                XLALDestroyREAL8Vector(omegaHi);
 2572              }
 2573              if(vPhiVecHi){
 2574               XLALDestroyREAL8Vector(vPhiVecHi);
 2575             }
 2576              if(ampNQC){
 2577                XLALDestroyREAL8Vector(ampNQC);
 2578              }
 2579              if(phaseNQC){
 2580                XLALDestroyREAL8Vector(phaseNQC);
 2581              }
 2582              if(hamVHi){
 2583                XLALDestroyREAL8Vector(hamVHi);
 2584              }
 2585              if(hLMAllHi){
 2586                XLALDestroyREAL8Vector(hLMAllHi);
 2587              }
 2588              XLAL_ERROR (XLAL_EFUNC);
 2589            }
 2590          }
 2591        }
 2592    }
 2593    if ( SpinAlignedEOBversion == 4 && nqcFlag == 1 ) {
 2594        nqcCoeffsInput->data[0] = nqcCoeffs.a1;
 2595        nqcCoeffsInput->data[1] = nqcCoeffs.a2;
 2596        nqcCoeffsInput->data[2] = nqcCoeffs.a3;
 2597        nqcCoeffsInput->data[3] = nqcCoeffs.a3S;
 2598        nqcCoeffsInput->data[4] = nqcCoeffs.a4;
 2599        nqcCoeffsInput->data[5] = nqcCoeffs.a5;
 2600        nqcCoeffsInput->data[6] = nqcCoeffs.b1;
 2601        nqcCoeffsInput->data[7] = nqcCoeffs.b2;
 2602        nqcCoeffsInput->data[8] = nqcCoeffs.b3;
 2603        nqcCoeffsInput->data[9] = nqcCoeffs.b4;
 2604 
 2605 
 2606        // FINISHED COMPUTING NQC. NOW MUST FREE ALLOCATED MEMORY!
 2607 
 2608        XLALDestroyREAL8Vector (tmpValues);
 2609        XLALDestroyREAL8Vector (sigmaKerr);
 2610        XLALDestroyREAL8Vector (sigmaStar);
 2611        XLALDestroyREAL8Vector (values);
 2612        XLALDestroyREAL8Vector (ampNQC);
 2613        XLALDestroyREAL8Vector (phaseNQC);
 2614        XLALDestroyREAL8Vector (sigReVec);
 2615        XLALDestroyREAL8Vector (sigImVec);
 2616        XLALAdaptiveRungeKuttaFree (integrator);
 2617        XLALDestroyREAL8Array (dynamics);
 2618        XLALDestroyREAL8Array (dynamicsHi);
 2619 
 2620        if (dynamicstmp)
 2621          {
 2622            XLALDestroyREAL8Array (dynamicstmp);
 2623          }
 2624        if (dynamicsHitmp)
 2625          {
 2626            XLALDestroyREAL8Array (dynamicsHitmp);
 2627          }
 2628 
 2629        XLALDestroyREAL8Vector (sigReHi);
 2630        XLALDestroyREAL8Vector (sigImHi);
 2631        XLALDestroyREAL8Vector (omegaHi);
 2632 
 2633#if debugOutput
 2634        printf
 2635        ("Tidal point-mass NQC should not be 0 here: %.16e %.16e %.16e %.16e %.16e %.16e %.16e %.16e %.16e %.16e\n",
 2636         nqcCoeffs.a1, nqcCoeffs.a2, nqcCoeffs.a3, nqcCoeffs.a3S, nqcCoeffs.a4,
 2637         nqcCoeffs.a5, nqcCoeffs.b1, nqcCoeffs.b2, nqcCoeffs.b3, nqcCoeffs.b4);
 2638#endif
 2639        return XLAL_SUCCESS;
 2640    }
 2641    /* Here we store the NQC coefficients for the different modes in some matrices */
 2642    gsl_matrix_set(nqcCoeffsMatrix,k,0, nqcCoeffs.a1);
 2643    gsl_matrix_set(nqcCoeffsMatrix,k,1, nqcCoeffs.a2);
 2644    gsl_matrix_set(nqcCoeffsMatrix,k,2, nqcCoeffs.a3);
 2645    gsl_matrix_set(nqcCoeffsMatrix,k,3, nqcCoeffs.a3S);
 2646    gsl_matrix_set(nqcCoeffsMatrix,k,4, nqcCoeffs.a4);
 2647    gsl_matrix_set(nqcCoeffsMatrix,k,5, nqcCoeffs.a5);
 2648    gsl_matrix_set(nqcCoeffsMatrix,k,6, nqcCoeffs.b1);
 2649    gsl_matrix_set(nqcCoeffsMatrix,k,7, nqcCoeffs.b2);
 2650    gsl_matrix_set(nqcCoeffsMatrix,k,8, nqcCoeffs.b3);
 2651    gsl_matrix_set(nqcCoeffsMatrix,k,9, nqcCoeffs.b4);
 2652#if debugOutput
 2653  printf
 2654    ("(%d,%d)-mode NQC should not be 0 here: %.16e %.16e %.16e %.16e %.16e %.16e %.16e %.16e %.16e %.16e\n",
 2655     modeL, modeM, nqcCoeffs.a1, nqcCoeffs.a2, nqcCoeffs.a3, nqcCoeffs.a3S, nqcCoeffs.a4,
 2656     nqcCoeffs.a5, nqcCoeffs.b1, nqcCoeffs.b2, nqcCoeffs.b3, nqcCoeffs.b4);
 2657     FILE *NQC = NULL;
 2658     sprintf(filename2,"NQC%01d%01dHi.dat",modeL,modeM);
 2659     NQC = fopen (filename2, "w");
 2660     fprintf(NQC, "%.16e \n%.16e \n%.16e \n%.16e \n%.16e\n", nqcCoeffs.a1, nqcCoeffs.a2, nqcCoeffs.a3,nqcCoeffs.b1, nqcCoeffs.b2);
 2661     fclose(NQC);
 2662#endif
 2663 
 2664 
 2665/* Apply to the high sampled part */
 2666#if debugOutput
 2667    char filename[sizeof "saModesXXHiNQC.dat"];
 2668    sprintf(filename,"saModes%01d%01dHiNQC.dat",modeL,modeM);
 2669    out = fopen (filename, "w");
 2670#endif
 2671  for (i = 0; i < retLen; i++)
 2672    {
 2673      values->data[0] = rHi.data[i];
 2674      values->data[1] = phiHi.data[i];
 2675      values->data[2] = prHi.data[i];
 2676      values->data[3] = pPhiHi.data[i];
 2677 
 2678      if (XLALSimIMREOBNonQCCorrection
 2679          (&hNQC, values, omegaHi->data[i], &nqcCoeffs) == XLAL_FAILURE)
 2680        {
 2681    if(tmpValues){
 2682      XLALDestroyREAL8Vector (tmpValues);
 2683    }
 2684    if(sigmaKerr){
 2685      XLALDestroyREAL8Vector (sigmaKerr);
 2686    }
 2687    if(sigmaStar){
 2688      XLALDestroyREAL8Vector (sigmaStar);
 2689    }
 2690    if(values){
 2691      XLALDestroyREAL8Vector (values);
 2692    }
 2693    if(sigReHi){
 2694      XLALDestroyREAL8Vector(sigReHi);
 2695    }
 2696    if(sigImHi){
 2697      XLALDestroyREAL8Vector(sigImHi);
 2698    }
 2699    if(omegaHi){
 2700      XLALDestroyREAL8Vector(omegaHi);
 2701    }
 2702    if(vPhiVecHi){
 2703      XLALDestroyREAL8Vector(vPhiVecHi);
 2704    }
 2705    if(ampNQC){
 2706      XLALDestroyREAL8Vector(ampNQC);
 2707    }
 2708    if(phaseNQC){
 2709      XLALDestroyREAL8Vector(phaseNQC);
 2710    }
 2711    if(hamVHi){
 2712      XLALDestroyREAL8Vector(hamVHi);
 2713    }
 2714    if(hLMAllHi){
 2715      XLALDestroyREAL8Vector(hLMAllHi);
 2716    }
 2717          XLAL_ERROR (XLAL_EFUNC);
 2718        }
 2719      hLM = sigReHi->data[i];
 2720      hLM += I * sigImHi->data[i];
 2721      hLM *= hNQC;
 2722        if ( (lambda2Tidal1 != 0. && omega02Tidal1 != 0.) || (lambda2Tidal2 != 0. && omega02Tidal2 != 0.) ) {
 2723            if (XLALSimIMRSpinEOBWaveformTidal
 2724                (&hT, values, cbrt(omegaHi->data[i]), 2, 2, &seobParams) )
 2725            {
 2726                XLAL_ERROR (XLAL_EFUNC);
 2727            }
 2728            hLM += amp0*hT;
 2729        }
 2730 
 2731      sigReHi->data[i] = (REAL8) creal (hLM);
 2732      sigImHi->data[i] = (REAL8) cimag (hLM);
 2733 
 2734 
 2735 
 2736        hLMAllHi->data[2*k*sigReHi->length + i] = sigReHi->data[i];
 2737        hLMAllHi->data[(1+2*k)*sigReHi->length + i] = sigImHi->data[i];
 2738#if debugOutput
 2739        fprintf (out, "%.16e %.16e %.16e %.16e %.16e\n", timeHi.data[i],
 2740                 creal (hLM) / amp0, cimag (hLM) / amp0,
 2741                 hLMAllHi->data[2*k*sigReHi->length + i]/ amp0 ,hLMAllHi->data[(1+2*k)*sigReHi->length + i]/ amp0
 2742                 );
 2743#endif
 2744 
 2745      if (SpinAlignedEOBversion==1 || SpinAlignedEOBversion==2) {
 2746          sigAmpSqHi = creal (hLM) * creal (hLM) + cimag (hLM) * cimag (hLM);
 2747          if (sigAmpSqHi < oldsigAmpSqHi && peakCount == 0 && (i - 1) * deltaTHigh / mTScaled < timePeak-timewavePeak)
 2748          {
 2749              timewavePeak = (i - 1) * deltaTHigh / mTScaled;
 2750              peakCount += 1;
 2751          }
 2752          oldsigAmpSqHi = sigAmpSqHi;
 2753      }
 2754    }
 2755#if debugOutput
 2756  fclose (out);
 2757  printf ("NQCs entering hNQC: %f, %f, %f, %f, %f, %f\n", nqcCoeffs.a1,
 2758          nqcCoeffs.a2, nqcCoeffs.a3, nqcCoeffs.a3S, nqcCoeffs.a4,
 2759          nqcCoeffs.a5);
 2760  printf ("NQCs entering hNQC: %f, %f, %f, %f\n", nqcCoeffs.b1, nqcCoeffs.b2,
 2761          nqcCoeffs.b3, nqcCoeffs.b4);
 2762  printf ("Stas, again: timePeak = %.16f, timewavePeak = %.16f \n", timePeak,
 2763          timewavePeak);
 2764#endif
 2765 
 2766}
 2767 
 2768 
 2769 
 2770 
 2771/* REMOVE THIS */
 2772 
 2773 
 2774    if (timewavePeak < 1.0e-16 || peakCount == 0)
 2775    {
 2776      //printf("YP::warning: could not locate mode peak, use calibrated time shift of amplitude peak instead.\n");
 2777      /* NOTE: instead of looking for the actual peak, use the calibrated value,    */
 2778      /*       ignoring the error in using interpolated NQC instead of iterated NQC */
 2779      timewavePeak = timePeak - timewavePeak;
 2780    }
 2781 
 2782  /*
 2783   * STEP 6) Calculate QNM excitation coefficients using hi-sampling data
 2784   */
 2785 
 2786  /*out = fopen( "saInspWaveHi.dat", "w" );
 2787     for ( i = 0; i < retLen; i++ )
 2788     {
 2789     fprintf( out, "%.16e %.16e %.16e\n", timeHi.data[i], sigReHi->data[i], sigImHi->data[i] );
 2790     }
 2791     fclose( out ); */
 2792 
 2793  /* Attach the ringdown at the time of amplitude peak */
 2794  REAL8 combSize = 7.5;         /* Eq. 34 */
 2795  REAL8 chi =
 2796    (spin1[2] + spin2[2]) / 2. +
 2797    ((spin1[2] - spin2[2]) / 2.) * ((m1 - m2) / (m1 + m2)) / (1. - 2. * eta);
 2798 
 2799  /* Modify the combsize for SEOBNRv2 */
 2800  /* If chi1=chi2=0, comb = 11. if chi < 0.8, comb = 12. if chi >= 0.8, comb =
 2801   * 13.5 */
 2802   //RC: the combsize is not used for the RD attachment for v4, I don't understand why the code enters inside this loop even for v4...
 2803  if (SpinAlignedEOBversion == 2 || SpinAlignedEOBversion == 4)
 2804    {
 2805      combSize = (spin1[2] == 0.
 2806                  && spin2[2] == 0.) ? 11. : ((eta > 10. / 121.
 2807                                               && chi >= 0.8) ? 8.5 : 12.);
 2808      if ((eta > 30. / 31. / 31. && eta <= 10. / 121. && chi >= 0.8)
 2809          || (eta <= 30. / 31. / 31. && chi >= 0.8 && chi < 0.9))
 2810        combSize = 13.5;
 2811    }
 2812 
 2813  REAL8 timeshiftPeak;
 2814  timeshiftPeak = timePeak - timewavePeak;
 2815  if (SpinAlignedEOBversion == 2 || SpinAlignedEOBversion == 4)
 2816    {
 2817      timeshiftPeak =
 2818        (timePeak - timewavePeak) > 0. ? (timePeak - timewavePeak) : 0.;
 2819    }
 2820 
 2821  /*printf("YP::timePeak and timewavePeak: %.16e and %.16e\n",timePeak,timewavePeak);
 2822     printf("YP::timeshiftPeak and combSize: %.16e and %.16e\n",timeshiftPeak,combSize);
 2823     printf("PK::chi and SpinAlignedEOBversion: %.16e and %u\n\n", chi,SpinAlignedEOBversion); */
 2824 
 2825  REAL8Vector *rdMatchPoint = XLALCreateREAL8Vector (4);
 2826  if (!rdMatchPoint)
 2827    {
 2828      if(tmpValues){
 2829        XLALDestroyREAL8Vector (tmpValues);
 2830      }
 2831      if(sigmaKerr){
 2832        XLALDestroyREAL8Vector (sigmaKerr);
 2833      }
 2834      if(sigmaStar){
 2835        XLALDestroyREAL8Vector (sigmaStar);
 2836      }
 2837      if(values){
 2838        XLALDestroyREAL8Vector (values);
 2839      }
 2840      if(sigReHi){
 2841        XLALDestroyREAL8Vector(sigReHi);
 2842      }
 2843      if(sigImHi){
 2844        XLALDestroyREAL8Vector(sigImHi);
 2845      }
 2846      if(omegaHi){
 2847        XLALDestroyREAL8Vector(omegaHi);
 2848      }
 2849      if(vPhiVecHi){
 2850        XLALDestroyREAL8Vector(vPhiVecHi);
 2851      }
 2852      if(ampNQC){
 2853        XLALDestroyREAL8Vector(ampNQC);
 2854      }
 2855      if(phaseNQC){
 2856        XLALDestroyREAL8Vector(phaseNQC);
 2857      }
 2858      if(hamVHi){
 2859        XLALDestroyREAL8Vector(hamVHi);
 2860      }
 2861      if(hLMAllHi){
 2862        XLALDestroyREAL8Vector(hLMAllHi);
 2863      }
 2864      XLAL_ERROR (XLAL_ENOMEM);
 2865    }
 2866 
 2867  if (combSize > timePeak - timeshiftPeak)
 2868    {
 2869      XLALPrintError ("The comb size looks to be too big!!!\n");
 2870    }
 2871 
 2872    REAL8Vector *OmVec = NULL;
 2873    if (use_tidal == 1) {
 2874        timeshiftPeak = 0.;
 2875        UINT4 indAmax = 0;
 2876        REAL8 Anew, Aval = sqrt( sigReHi->data[0]*sigReHi->data[0] +sigImHi->data[0]*sigImHi->data[0] );
 2877        for (i =  1; i < (INT4) timeHi.length; i++) {
 2878            Anew = sqrt( sigReHi->data[i]*sigReHi->data[i] +sigImHi->data[i]*sigImHi->data[i]);
 2879            if ( Aval > Anew ) {
 2880                indAmax = i-1;
 2881                break;
 2882            } else {
 2883                indAmax = i;
 2884                Aval = Anew;
 2885            }
 2886        }
 2887#if debugOutput
 2888        printf("indAmax %d\n",indAmax);
 2889#endif
 2890 
 2891        if ( (INT4)indAmax== (INT4) timeHi.length-1 ) {
 2892            INT4 peakDet = 0;
 2893            REAL8 dAnew, dAval;
 2894            REAL8 Avalp = sqrt( sigReHi->data[1]*sigReHi->data[1] +sigImHi->data[1]*sigImHi->data[1] );
 2895            REAL8 Avalm = sqrt( sigReHi->data[0]*sigReHi->data[0] +sigImHi->data[0]*sigImHi->data[0] );
 2896            dAval= Avalp - Avalm;
 2897            INT4 iSkip = (INT4) 1./(deltaTHigh / mTScaled);
 2898            for (i=(INT4) timeHi.length/2; i<(INT4) timeHi.length; i=i+iSkip) {
 2899                Avalm = sqrt( sigReHi->data[i-1]*sigReHi->data[i-1] +sigImHi->data[i-1]*sigImHi->data[i-1]);
 2900                Avalp = sqrt( sigReHi->data[i]*sigReHi->data[i] +sigImHi->data[i]*sigImHi->data[i]);
 2901                dAnew = Avalp - Avalm;
 2902#if debugOutput
 2903                printf("%.16e %.16e %.16e\n", i*deltaTHigh / mTScaled, dAnew, dAval);
 2904#endif
 2905                if ( peakDet==0) {
 2906                    if ( dAnew<dAval) peakDet++;
 2907                    dAval = dAnew;
 2908                }
 2909                else {
 2910                    if ( dAnew>dAval ) {
 2911                        indAmax = i-1;
 2912                        break;
 2913                    }
 2914                    else {
 2915                        dAval = dAnew;
 2916                    }
 2917                }
 2918            }
 2919        }
 2920#if debugOutput
 2921        printf("indAmax %d\n",indAmax);
 2922#endif
 2923        UINT4 indOmax = 0;
 2924        REAL8 dt = timeHi.data[1] - timeHi.data[0];
 2925        REAL8 re = sigReHi->data[0], im = sigImHi->data[0];
 2926        REAL8 red = ( sigReHi->data[1] - sigReHi->data[0] ) / dt, imd = ( sigImHi->data[1] - sigImHi->data[0] ) / dt;
 2927        REAL8 Onew, Oval = - (imd*re - red*im) / (re*re + im*im);
 2928 
 2929        OmVec = XLALCreateREAL8Vector (sigReHi->length);
 2930        memset (OmVec->data, 0, OmVec->length * sizeof (REAL8));
 2931 
 2932        for (i = 1; i < (INT4) timeHi.length-1; i++) {
 2933            re = sigReHi->data[i];
 2934            im = sigImHi->data[i];
 2935            red = ( sigReHi->data[i+1] - sigReHi->data[i] ) / dt;
 2936            imd = ( sigImHi->data[i+1] - sigImHi->data[i] ) / dt;
 2937            Onew = - (imd*re - red*im) / (re*re + im*im);
 2938            OmVec->data[i] = Onew;
 2939            if ( Onew >= Oval ) {
 2940                indOmax = i;
 2941                Oval = Onew;
 2942            }
 2943        }
 2944 
 2945        if ( indAmax>timeHi.length/2 && timeHi.data[indAmax] <= timeHi.data[indOmax] ) {
 2946            timePeak = timeHi.data[indAmax] ;
 2947        }
 2948        else {
 2949            timePeak = timeHi.data[indOmax];
 2950        }
 2951        if ( eobParams.NyquistStop ==1 ) timePeak = timeHi.data[timeHi.length - 1];
 2952    }
 2953 
 2954    /* Having located the peak of orbital frequency, we set time and phase of coalescence */
 2955    if(!postAdiabaticFlag){
 2956      XLALGPSAdd (&tc, -mTScaled * (dynamics->data[hiSRndx] + timePeak));
 2957    }
 2958 
 2959 
 2960  rdMatchPoint->data[0] =
 2961    combSize <
 2962    timePeak - timeshiftPeak ? timePeak - timeshiftPeak - combSize : 0;
 2963  //rdMatchPoint->data[0] = timePeak + 2.0*deltaTHigh;
 2964  rdMatchPoint->data[1] = timePeak - timeshiftPeak;
 2965  rdMatchPoint->data[2] = dynamicsHi->data[finalIdx];
 2966#if debugOutput
 2967  printf ("YP::comb range: %f, %f\n", rdMatchPoint->data[0],
 2968          rdMatchPoint->data[1]);
 2969#endif
 2970  rdMatchPoint->data[0] -=
 2971    fmod (rdMatchPoint->data[0], deltaTHigh / mTScaled);
 2972  rdMatchPoint->data[1] -=
 2973    fmod (rdMatchPoint->data[1], deltaTHigh / mTScaled);
 2974#if debugOutput
 2975    printf("tattach = %.16f\n", rdMatchPoint->data[1]);
 2976#endif
 2977UINT4 indAmpMax = 0; //RC this variable is only used for SEOBNRv4HM. It stores the index of the attaching point of the 22 mode
 2978 
 2979for ( UINT4 k = 0; k<nModes; k++) {
 2980 
 2981    modeL  = lmModes[k][0];
 2982    modeM = lmModes[k][1];
 2983 
 2984    //RC: Here I modify the attachment point for the 55 mode, which is tpeak22 -10M and is passed with the variable rdMatchPoint->data[3]
 2985    if((modeL == 5)&&(modeM==5)){
 2986      rdMatchPoint->data[3] = timePeak - timeshiftPeak-10;
 2987      rdMatchPoint->data[3] -= fmod (rdMatchPoint->data[3], deltaTHigh / mTScaled);
 2988    }
 2989 
 2990    for ( i=0; i<retLen; i++ ) {
 2991        sigReHi->data[i] = hLMAllHi->data[i + 2*k*sigReHi->length];
 2992        sigImHi->data[i] = hLMAllHi->data[i + (2*k+1)*sigReHi->length];
 2993    }
 2994    for ( i=retLen; i<(INT4)sigReHi->length; i++ ) {
 2995        sigReHi->data[i] = 0.;
 2996        sigImHi->data[i] = 0.;
 2997    }
 2998 
 2999    if ( use_tidal == 1 ) {
 3000        INT4 kount;
 3001        REAL8 dtGeom = deltaTHigh / mTScaled;
 3002        REAL8Vector *ampl, *phtmp;
 3003        ampl = XLALCreateREAL8Vector (sigReHi->length);
 3004        memset (ampl->data, 0, ampl->length * sizeof (REAL8));
 3005        phtmp = XLALCreateREAL8Vector (sigReHi->length);
 3006        memset (phtmp->data, 0,phtmp->length * sizeof (REAL8));
 3007        INT4 iEnd= (INT4)rdMatchPoint->data[1]/dtGeom;
 3008        UINT4 iM = iEnd - 1000;
 3009        REAL8 omega0 = OmVec->data[iEnd];
 3010        REAL8 omegaM = OmVec->data[iM];
 3011        REAL8 omegaMdot = (OmVec->data[iM]-OmVec->data[iM-10])/(10*dtGeom);
 3012        REAL8 tau = 0.5*LAL_PI/omega0;
 3013 
 3014        for (kount=0; kount<iEnd; kount++){
 3015            ampl->data[kount] = sqrt(sigReHi->data[kount]/amp0*sigReHi->data[kount]/amp0 + sigImHi->data[kount]/amp0*sigImHi->data[kount]/amp0)/(1. + exp((kount*dtGeom-rdMatchPoint->data[1]-15)/tau));
 3016            phtmp->data[kount] = carg(sigReHi->data[kount] + I * sigImHi->data[kount]);
 3017        }
 3018        REAL8 amplEnd = sqrt(sigReHi->data[iEnd]/amp0*sigReHi->data[iEnd]/amp0 + sigImHi->data[iEnd]/amp0*sigImHi->data[iEnd]/amp0);
 3019        REAL8 amplEndM1 = sqrt(sigReHi->data[iEnd-1]/amp0*sigReHi->data[iEnd-1]/amp0 + sigImHi->data[iEnd-1]/amp0*sigImHi->data[iEnd-1]/amp0);
 3020        REAL8 ampldotEnd = (amplEnd-amplEndM1)/dtGeom;
 3021        if ( ampldotEnd < 0. ) ampldotEnd = 0.;
 3022        for (kount=iEnd;kount<(INT4)(sigReHi->length);kount++){
 3023            ampl->data[kount] = (amplEnd + ampldotEnd*(kount - iEnd)*dtGeom)/(1. + exp((kount*dtGeom-rdMatchPoint->data[1]-15)/tau));
 3024        }
 3025        for (kount=(INT4)iM;kount<(INT4)(sigReHi->length);kount++){
 3026            phtmp->data[kount] = phtmp->data[iM] - ( omega0*(kount-(INT4)iM)*dtGeom + (omega0-omegaM)*(omega0-omegaM)/omegaMdot*(exp(-(kount-(INT4)iM)*dtGeom/(omega0-omegaM)*omegaMdot) - 1.) );
 3027        }
 3028#if debugOutput
 3029        FILE *testout = fopen ("test.dat", "w");
 3030        for (kount=0;kount<(INT4)(sigReHi->length);kount++){
 3031            fprintf(testout, "%.16e %.16e %.16e %.16e %.16e %.16e %.16e\n", kount*dtGeom,ampl->data[kount],phtmp->data[kount],sigReHi->data[kount],sigImHi->data[kount],sqrt(sigReHi->data[kount]/amp0*sigReHi->data[kount]/amp0 + sigImHi->data[kount]/amp0*sigImHi->data[kount]/amp0),carg(sigReHi->data[kount] + I * sigImHi->data[kount]));
 3032        }
 3033        fclose(testout);
 3034#endif
 3035        for (kount=0;kount<(INT4)(sigReHi->length);kount++){
 3036            sigReHi->data[kount] = amp0*ampl->data[kount]*cos(phtmp->data[kount]);
 3037            sigImHi->data[kount] = amp0*ampl->data[kount]*sin(phtmp->data[kount]);
 3038        }
 3039        XLALDestroyREAL8Vector(ampl);
 3040        XLALDestroyREAL8Vector(phtmp);
 3041                            /*
 3042        if (XLALSimIMREOBTaper (sigReHi, sigImHi, 2, 2,
 3043                                            deltaTHigh, m1, m2, spin1[0],
 3044                                            spin1[1], spin1[2], spin2[0],
 3045                                            spin2[1], spin2[2], &timeHi,
 3046                                            rdMatchPoint,
 3047                                            SpinAlignedEOBapproximant) ==
 3048            XLAL_FAILURE)
 3049        {
 3050            XLAL_ERROR (XLAL_EFUNC);
 3051        }
 3052                             */
 3053    }
 3054    else {
 3055        if (SpinAlignedEOBversion == 1 || SpinAlignedEOBversion == 2)
 3056        {
 3057            if (XLALSimIMREOBHybridAttachRingdown (sigReHi, sigImHi, 2, 2,
 3058                                             deltaTHigh, m1, m2, spin1[0],
 3059                                             spin1[1], spin1[2], spin2[0],
 3060                                             spin2[1], spin2[2], &timeHi,
 3061                                             rdMatchPoint,
 3062                                             SpinAlignedEOBapproximant) ==
 3063                XLAL_FAILURE)
 3064            {
 3065                XLAL_ERROR (XLAL_EFUNC);
 3066            }
 3067        }
 3068        else if (SpinAlignedEOBversion == 4)
 3069        {
 3070            if (XLALSimIMREOBAttachFitRingdown (
 3071                sigReHi, sigImHi, modeL, modeM,
 3072                deltaTHigh, m1, m2,
 3073                spin1[0], spin1[1], spin1[2],
 3074                spin2[0], spin2[1], spin2[2],
 3075                domega220, dtau220,
 3076                domega210, dtau210,
 3077                domega330, dtau330,
 3078                domega440, dtau440,
 3079                domega550, dtau550,
 3080                TGRflag,
 3081                &timeHi,
 3082                rdMatchPoint,
 3083                SpinAlignedEOBapproximant, &indAmpMax) ==
 3084                XLAL_FAILURE)
 3085            {
 3086              if(tmpValues){
 3087                XLALDestroyREAL8Vector (tmpValues);
 3088              }
 3089              if(sigmaKerr){
 3090                XLALDestroyREAL8Vector (sigmaKerr);
 3091              }
 3092              if(sigmaStar){
 3093                XLALDestroyREAL8Vector (sigmaStar);
 3094              }
 3095              if(values){
 3096                XLALDestroyREAL8Vector (values);
 3097              }
 3098              if(sigReHi){
 3099                XLALDestroyREAL8Vector(sigReHi);
 3100              }
 3101              if(sigImHi){
 3102                XLALDestroyREAL8Vector(sigImHi);
 3103              }
 3104              if(omegaHi){
 3105                XLALDestroyREAL8Vector(omegaHi);
 3106              }
 3107              if(vPhiVecHi){
 3108                XLALDestroyREAL8Vector(vPhiVecHi);
 3109              }
 3110              if(ampNQC){
 3111                XLALDestroyREAL8Vector(ampNQC);
 3112              }
 3113              if(phaseNQC){
 3114                XLALDestroyREAL8Vector(phaseNQC);
 3115              }
 3116              if(hamVHi){
 3117                XLALDestroyREAL8Vector(hamVHi);
 3118              }
 3119              if(hLMAllHi){
 3120                XLALDestroyREAL8Vector(hLMAllHi);
 3121              }
 3122              XLAL_ERROR (XLAL_EFUNC);
 3123            }
 3124 
 3125        }
 3126 
 3127    }
 3128    for ( i=0; i<(INT4)sigReHi->length; i++) {
 3129        hLMAllHi->data[2*k*sigReHi->length + i] = sigReHi->data[i];
 3130        hLMAllHi->data[(1+2*k)*sigReHi->length + i] = sigImHi->data[i];
 3131    }
 3132#if debugOutput
 3133    char filename[sizeof "saModesXXHiIMR.dat"];
 3134    sprintf(filename,"saModes%01d%01dHiIMR.dat",modeL,modeM);
 3135    out = fopen (filename, "w");
 3136    for ( i=0; i<(INT4)sigReHi->length; i++) {
 3137        fprintf (out, "%.16e %.16e %.16e\n", i*deltaTHigh / mTScaled,hLMAllHi->data[2*k*sigReHi->length + i]/amp0,hLMAllHi->data[(1+2*k)*sigReHi->length + i]/amp0);
 3138    }
 3139    fclose(out);
 3140#endif
 3141 
 3142 
 3143}
 3144 
 3145 
 3146  /*
 3147   * STEP 7) Generate full inspiral waveform using desired sampling frequency
 3148   */
 3149 
 3150  if (use_optimized_v2_or_v4)
 3151    {
 3152      // maybe dynamicstmp and dynamicsHitmp should be called "intermediateDynamics(Hi)" now since they aren't so temporary anymore?
 3153      GenerateAmpPhaseFromEOMSoln (retLen_fromOptStep2, dynamicstmp->data,
 3154                                   &seobParams);
 3155      /*
 3156       * We used dynamics and dynamicsHi to store solution to equations of motion.
 3157       *   The solution was needed to find, e.g., the time at peak freq (STEP 4).
 3158       *   At this point, the solution to the EOMs is no longer needed, so we
 3159       *   now repurpose dynamics and dynamicsHi to store amplitude and phase
 3160       *   information only.
 3161`      * This is the most efficient solution, as it frees up unused memory.
 3162       */
 3163      XLALDestroyREAL8Array (dynamics);
 3164      XLALDestroyREAL8Array (dynamicsHi);
 3165      dynamics = NULL;
 3166      dynamicsHi = NULL;
 3167      retLen =
 3168        SEOBNRv2OptimizedInterpolatorOnlyAmpPhase (dynamicstmp, 0.,
 3169                                                   deltaT / mTScaled,
 3170                                                   retLen_fromOptStep2,
 3171                                                   &dynamics);
 3172 
 3173      ampVec.length = phaseVec.length = retLen;
 3174      ampVec.data = dynamics->data + 5 * retLen;
 3175      phaseVec.data = dynamics->data + 6 * retLen;
 3176 
 3177      GenerateAmpPhaseFromEOMSoln (retLen_fromOptStep3, dynamicsHitmp->data,
 3178                                   &seobParams);
 3179      retLen =
 3180        SEOBNRv2OptimizedInterpolatorOnlyAmpPhase (dynamicsHitmp, 0.,
 3181                                                   deltaTHigh / mTScaled,
 3182                                                   retLen_fromOptStep3,
 3183                                                   &dynamicsHi);
 3184    }
 3185 
 3186 
 3187 
 3188 
 3189  /* Now create vectors at the correct sample rate, and compile the complete waveform */
 3190  if(postAdiabaticFlag && postAdiabaticOutcome == XLAL_SUCCESS){
 3191    sigReVec =
 3192      XLALCreateREAL8Vector (combinedLenForInterp + ceil (sigReHi->length / resampFac));
 3193    sigImVec = XLALCreateREAL8Vector (sigReVec->length);
 3194  }
 3195  else{
 3196    sigReVec =
 3197      XLALCreateREAL8Vector (rVec.length + ceil (sigReHi->length / resampFac));
 3198    sigImVec = XLALCreateREAL8Vector (sigReVec->length);
 3199  }
 3200  memset (sigReVec->data, 0, sigReVec->length * sizeof (REAL8));
 3201  memset (sigImVec->data, 0, sigImVec->length * sizeof (REAL8));
 3202 
 3203  REAL8Vector *sigReCoorbVec =
 3204    XLALCreateREAL8Vector (combinedLenForInterp + ceil (sigReHi->length / resampFac));
 3205  REAL8Vector *sigImCoorbVec = XLALCreateREAL8Vector (sigReCoorbVec ->length);
 3206 
 3207  memset (sigReCoorbVec->data, 0, sigReCoorbVec->length * sizeof (REAL8));
 3208  memset (sigImCoorbVec->data, 0, sigImCoorbVec->length * sizeof (REAL8));
 3209  // PA: the spacing is not regular on the dynamics grid, so must be careful
 3210  // to set the correct length with the desired spacing
 3211 
 3212  hLMAll = XLALCreateREAL8Vector((UINT4)2*sigReVec->length*nModes);
 3213  memset(hLMAll->data, 0, hLMAll->length*sizeof (REAL8));
 3214 
 3215   UINT4 idx = 0;
 3216  /* Generate full inspiral waveform using desired sampling frequency */
 3217  if (use_optimized_v2_or_v4)
 3218    {
 3219      for (i = 0; i < (INT4) rVec.length; i++)
 3220        {
 3221 
 3222          hLM = ampVec.data[i] * cexp (I * phaseVec.data[i]);
 3223 
 3224          sigReVec->data[i] = amp0 * creal (hLM);
 3225          sigImVec->data[i] = amp0 * cimag (hLM);
 3226    hLMAll->data[i] = sigReVec->data[i];
 3227    hLMAll->data[sigReVec->length + i] = sigImVec->data[i];
 3228        }
 3229    }
 3230  else
 3231    {
 3232#if debugOutput
 3233        out = fopen ("saDynamics.dat", "w");
 3234#endif
 3235        hamV = XLALCreateREAL8Vector(rVec.length);
 3236        memset(hamV->data, 0., hamV->length*sizeof(REAL8));
 3237 
 3238        omegaVec = XLALCreateREAL8Vector(rVec.length);
 3239        memset(omegaVec->data, 0., omegaVec->length*sizeof(REAL8));
 3240 
 3241              vPhiVec = XLALCreateREAL8Vector(rVec.length);
 3242        memset(vPhiVec->data, 0., vPhiVec->length*sizeof(REAL8));
 3243 
 3244        if (!omegaVec|| !hamV)
 3245        {
 3246          if(tmpValues){
 3247            XLALDestroyREAL8Vector (tmpValues);
 3248          }
 3249          if(sigmaKerr){
 3250            XLALDestroyREAL8Vector (sigmaKerr);
 3251          }
 3252          if(sigmaStar){
 3253            XLALDestroyREAL8Vector (sigmaStar);
 3254          }
 3255          if(values){
 3256            XLALDestroyREAL8Vector (values);
 3257          }
 3258          if(sigReHi){
 3259            XLALDestroyREAL8Vector(sigReHi);
 3260          }
 3261          if(sigImHi){
 3262            XLALDestroyREAL8Vector(sigImHi);
 3263          }
 3264          if(omegaHi){
 3265            XLALDestroyREAL8Vector(omegaHi);
 3266          }
 3267          if(vPhiVecHi){
 3268            XLALDestroyREAL8Vector(vPhiVecHi);
 3269          }
 3270          if(ampNQC){
 3271            XLALDestroyREAL8Vector(ampNQC);
 3272          }
 3273          if(phaseNQC){
 3274            XLALDestroyREAL8Vector(phaseNQC);
 3275          }
 3276          if(hamVHi){
 3277            XLALDestroyREAL8Vector(hamVHi);
 3278          }
 3279          if(hLMAllHi){
 3280            XLALDestroyREAL8Vector(hLMAllHi);
 3281          }
 3282          if(sigReVec){
 3283            XLALDestroyREAL8Vector(sigReVec);
 3284          }
 3285          if(sigImVec){
 3286            XLALDestroyREAL8Vector(sigImVec);
 3287          }
 3288          if(hLMAll){
 3289            XLALDestroyREAL8Vector(hLMAll);
 3290          }
 3291          if(vPhiVec)
 3292            XLALDestroyREAL8Vector(vPhiVec);
 3293 
 3294          XLAL_ERROR (XLAL_ENOMEM);
 3295        }
 3296      for (i = 0; i < (INT4) rVec.length; i++)
 3297        {
 3298          values->data[0] = rVec.data[i];
 3299          values->data[1] = phiVec.data[i];
 3300          values->data[2] = prVec.data[i];
 3301          values->data[3] = pPhiVec.data[i];
 3302          /* Do not need to add an if(use_optimized_v2_or_v4), since this is strictly unoptimized code (see if(use_optimized_v2_or_v4) above) */
 3303          if (postAdiabaticFlag){
 3304      omegaVec->data[i] = XLALSimIMRSpinAlignedEOBCalcOmegaOptimized (values->data, &seobParams);
 3305      vPhiVec->data[i] =  XLALSimIMRSpinAlignedEOBNonKeplerCoeffOptimized (values->data, &seobParams);
 3306 
 3307    }
 3308    else{
 3309      omegaVec->data[i] = XLALSimIMRSpinAlignedEOBCalcOmega (values->data, &seobParams, STEP_SIZE);
 3310    }
 3311 
 3312            //
 3313 
 3314#if debugOutput
 3315        fprintf (out, "%.16e %.16e %.16e %.16e %.16e %.16e\n", dynamics->data[i],
 3316                 rVec.data[i], phiVec.data[i], prVec.data[i], pPhiVec.data[i],omegaVec->data[i]);
 3317#endif
 3318          /* Calculate the value of the Hamiltonian */
 3319          cartPosVec.data[0] = values->data[0];
 3320          cartMomVec.data[0] = values->data[2];
 3321          cartMomVec.data[1] = values->data[3] / values->data[0];
 3322 
 3323    if(postAdiabaticFlag){
 3324          hamV->data[i] =
 3325            XLALSimIMRSpinEOBHamiltonianOptimized (eta, &cartPosVec, &cartMomVec,
 3326                                          &s1VecOverMtMt, &s2VecOverMtMt,
 3327                                          sigmaKerr, sigmaStar,
 3328                                          seobParams.tortoise, &seobCoeffs);
 3329    }
 3330    else{
 3331      hamV->data[i] =
 3332            XLALSimIMRSpinEOBHamiltonian (eta, &cartPosVec, &cartMomVec,
 3333                                          &s1VecOverMtMt, &s2VecOverMtMt,
 3334                                          sigmaKerr, sigmaStar,
 3335                                          seobParams.tortoise, &seobCoeffs);
 3336    }
 3337  }
 3338 
 3339 
 3340    // Interpolants for Re/Im parts of coorb modes
 3341    UNUSED gsl_interp_accel *acc_re = gsl_interp_accel_alloc();
 3342          gsl_spline *spline_re = gsl_spline_alloc(gsl_interp_cspline, rVec.length);
 3343    UNUSED gsl_interp_accel *acc_im = gsl_interp_accel_alloc();
 3344          gsl_spline *spline_im = gsl_spline_alloc(gsl_interp_cspline, rVec.length);
 3345    // Interpolant for orbital phase
 3346    UNUSED gsl_interp_accel *acc_orbphase = gsl_interp_accel_alloc();
 3347          gsl_spline *spline_orbphase = gsl_spline_alloc(gsl_interp_cspline, rVec.length);
 3348    gsl_spline_init(spline_orbphase, tVec.data, phiVec.data, rVec.length);
 3349 
 3350 
 3351    for ( UINT4 k = 0; k<nModes; k++) {
 3352        modeL  = lmModes[k][0];
 3353        modeM = lmModes[k][1];
 3354 
 3355        nqcCoeffs.a1 = gsl_matrix_get(nqcCoeffsMatrix,k,0);
 3356        nqcCoeffs.a2 = gsl_matrix_get(nqcCoeffsMatrix,k,1);
 3357        nqcCoeffs.a3 = gsl_matrix_get(nqcCoeffsMatrix,k,2);
 3358        nqcCoeffs.a3S = gsl_matrix_get(nqcCoeffsMatrix,k,3);
 3359        nqcCoeffs.a4 = gsl_matrix_get(nqcCoeffsMatrix,k,4);
 3360        nqcCoeffs.a5 = gsl_matrix_get(nqcCoeffsMatrix,k,5);
 3361        nqcCoeffs.b1 = gsl_matrix_get(nqcCoeffsMatrix,k,6);
 3362        nqcCoeffs.b2 = gsl_matrix_get(nqcCoeffsMatrix,k,7);
 3363        nqcCoeffs.b3 = gsl_matrix_get(nqcCoeffsMatrix,k,8);
 3364        nqcCoeffs.b4 = gsl_matrix_get(nqcCoeffsMatrix,k,9);
 3365#if debugOutput
 3366        printf
 3367        ("(%d,%d)-mode NQC should not be 0 here: %.16e %.16e %.16e %.16e %.16e %.16e %.16e %.16e %.16e %.16e\n",
 3368         modeL, modeM, nqcCoeffs.a1, nqcCoeffs.a2, nqcCoeffs.a3, nqcCoeffs.a3S, nqcCoeffs.a4,
 3369         nqcCoeffs.a5, nqcCoeffs.b1, nqcCoeffs.b2, nqcCoeffs.b3, nqcCoeffs.b4);
 3370#endif
 3371        for (i = 0; i < (INT4) rVec.length; i++)
 3372        {
 3373            values->data[0] = rVec.data[i];
 3374            values->data[1] = phiVec.data[i];
 3375            values->data[2] = prVec.data[i];
 3376            values->data[3] = pPhiVec.data[i];
 3377            if(postAdiabaticFlag){
 3378              status = XLALSimIMRSpinEOBGetSpinFactorizedWaveform_PA(
 3379                &hLM,
 3380                values,
 3381                cbrt (omegaVec->data[i]),
 3382                hamV->data[i],
 3383                modeL,
 3384                modeM,
 3385                &seobParams,
 3386                vPhiVec->data[i]
 3387              );
 3388            }
 3389            else{
 3390               status = XLALSimIMRSpinEOBGetSpinFactorizedWaveform(&hLM, values,  cbrt (omegaVec->data[i]), hamV->data[i], modeL, modeM, &seobParams, 0 /*use_optimized_v2_or_v4 */ );
 3391            }
 3392 
 3393        if ( status == XLAL_FAILURE)
 3394            {
 3395              if(tmpValues){
 3396                XLALDestroyREAL8Vector (tmpValues);
 3397              }
 3398              if(sigmaKerr){
 3399                XLALDestroyREAL8Vector (sigmaKerr);
 3400              }
 3401              if(sigmaStar){
 3402                XLALDestroyREAL8Vector (sigmaStar);
 3403              }
 3404              if(values){
 3405                XLALDestroyREAL8Vector (values);
 3406              }
 3407              if(sigReHi){
 3408                XLALDestroyREAL8Vector(sigReHi);
 3409              }
 3410              if(sigImHi){
 3411                XLALDestroyREAL8Vector(sigImHi);
 3412              }
 3413              if(omegaHi){
 3414                XLALDestroyREAL8Vector(omegaHi);
 3415              }
 3416              if(vPhiVecHi){
 3417                XLALDestroyREAL8Vector(vPhiVecHi);
 3418              }
 3419              if(ampNQC){
 3420                XLALDestroyREAL8Vector(ampNQC);
 3421              }
 3422              if(phaseNQC){
 3423                XLALDestroyREAL8Vector(phaseNQC);
 3424              }
 3425              if(hamVHi){
 3426                XLALDestroyREAL8Vector(hamVHi);
 3427              }
 3428              if(hLMAllHi){
 3429                XLALDestroyREAL8Vector(hLMAllHi);
 3430              }
 3431              if(sigReVec){
 3432                XLALDestroyREAL8Vector(sigReVec);
 3433              }
 3434              if(sigImVec){
 3435                XLALDestroyREAL8Vector(sigImVec);
 3436              }
 3437              if(hLMAll){
 3438                XLALDestroyREAL8Vector(hLMAll);
 3439              }
 3440              if(vPhiVec)
 3441                XLALDestroyREAL8Vector(vPhiVec);
 3442 
 3443              XLAL_ERROR (XLAL_EFUNC);
 3444            }
 3445            hT = 0.;
 3446            if ( (lambda2Tidal1 != 0. && omega02Tidal1 != 0.) || (lambda2Tidal2 != 0. && omega02Tidal2 != 0.) ) {
 3447            if (XLALSimIMRSpinEOBWaveformTidal
 3448                (&hT, values, cbrt (omegaVec->data[i]), 2, 2, &seobParams)
 3449                == XLAL_FAILURE)
 3450                {
 3451                    XLAL_ERROR (XLAL_EFUNC);
 3452                }
 3453            }
 3454 
 3455            if (XLALSimIMREOBNonQCCorrection (&hNQC, values, omegaVec->data[i], &nqcCoeffs)
 3456                == XLAL_FAILURE)
 3457            {
 3458              if(tmpValues){
 3459                XLALDestroyREAL8Vector (tmpValues);
 3460              }
 3461              if(sigmaKerr){
 3462                XLALDestroyREAL8Vector (sigmaKerr);
 3463              }
 3464              if(sigmaStar){
 3465                XLALDestroyREAL8Vector (sigmaStar);
 3466              }
 3467              if(values){
 3468                XLALDestroyREAL8Vector (values);
 3469              }
 3470              if(sigReHi){
 3471                XLALDestroyREAL8Vector(sigReHi);
 3472              }
 3473              if(sigImHi){
 3474                XLALDestroyREAL8Vector(sigImHi);
 3475              }
 3476              if(omegaHi){
 3477                XLALDestroyREAL8Vector(omegaHi);
 3478              }
 3479              if(vPhiVecHi){
 3480                XLALDestroyREAL8Vector(vPhiVecHi);
 3481              }
 3482              if(ampNQC){
 3483                XLALDestroyREAL8Vector(ampNQC);
 3484              }
 3485              if(phaseNQC){
 3486                XLALDestroyREAL8Vector(phaseNQC);
 3487              }
 3488              if(hamVHi){
 3489                XLALDestroyREAL8Vector(hamVHi);
 3490              }
 3491              if(hLMAllHi){
 3492                XLALDestroyREAL8Vector(hLMAllHi);
 3493              }
 3494              if(sigReVec){
 3495                XLALDestroyREAL8Vector(sigReVec);
 3496              }
 3497              if(sigImVec){
 3498                XLALDestroyREAL8Vector(sigImVec);
 3499              }
 3500              if(hLMAll){
 3501                XLALDestroyREAL8Vector(hLMAll);
 3502              }
 3503              XLAL_ERROR (XLAL_EFUNC);
 3504            }
 3505 
 3506            hLM *= hNQC;
 3507            hLM += hT;
 3508 
 3509            if (use_tidal==1) {
 3510                REAL8 dtGeom = deltaTHigh / mTScaled;
 3511                INT4 iEnd= (INT4)rdMatchPoint->data[1]/dtGeom;
 3512                REAL8 omega0 = OmVec->data[iEnd];
 3513                REAL8 tau = 0.5*LAL_PI/omega0;
 3514                REAL8 dtGeomLow = deltaT / mTScaled;
 3515                sigReVec->data[i] = amp0 * creal (hLM)/(1.  + exp(( i*dtGeomLow - (rdMatchPoint->data[1]+15 + (dynamics->data)[hiSRndx]) )/tau));
 3516                sigImVec->data[i] = amp0 * cimag (hLM)/(1. + exp(( i*dtGeomLow - (rdMatchPoint->data[1] +15 + (dynamics->data)[hiSRndx]))/tau));
 3517            }
 3518            else {
 3519                sigReVec->data[i] = amp0 * creal (hLM);
 3520                sigImVec->data[i] = amp0 * cimag (hLM);
 3521                if(postAdiabaticFlag && postAdiabaticOutcome == XLAL_SUCCESS){
 3522                  // We need to prepare for interpolation
 3523                  // We cannot interpolate amplitude and phase directly, because:
 3524                  // 1. The grid is too sparse and we don't have the unwrapped GW phase
 3525                  // 2. (2,1) and (5,5) modes can have zeros in the amplitude which
 3526                  // cause jumps in the phase.
 3527                  // Thus, we follow the SEOBNRv4HM_ROM paper (https://arxiv.org/pdf/2003.12079.pdf)
 3528                  //  and take out the leading order PN inspiral phasing, interpolate the rest and then transform back.
 3529                  sigReCoorbVec->data[i] = sigReVec->data[i]*cos(modeM*phiVec.data[i])-sigImVec->data[i]*sin(modeM*phiVec.data[i]);
 3530                  sigImCoorbVec->data[i] = sigReVec->data[i]*sin(modeM*phiVec.data[i])+sigImVec->data[i]*cos(modeM*phiVec.data[i]);
 3531                  //printf("i: %d time = %e amp = %e phase = %e\n",i,tVec.data[i],ampVecIn->data[i],phaseVecIn->data[i]);
 3532                }
 3533            }
 3534            if(!postAdiabaticFlag){
 3535              hLMAll->data[2*k*sigReVec->length + i] = sigReVec->data[i];
 3536              hLMAll->data[(1+2*k)*sigReVec->length + i] = sigImVec->data[i];
 3537            }
 3538        }
 3539        if(postAdiabaticFlag && postAdiabaticOutcome == XLAL_SUCCESS){
 3540 
 3541 
 3542          gsl_spline_init(spline_re, tVec.data, sigReCoorbVec->data, rVec.length);
 3543 
 3544 
 3545          gsl_spline_init(spline_im, tVec.data, sigImCoorbVec->data, rVec.length);
 3546 
 3547 
 3548 
 3549          REAL8 t_i = 0.0;
 3550          REAL8 re_temp = 0.0;
 3551    REAL8 im_temp = 0.0;
 3552 
 3553          REAL8 phase_temp = 0.0;
 3554    REAL8 re_In = 0.0;
 3555    REAL8 im_In = 0.0;
 3556    REAL8 cm = 0.0;
 3557    REAL8 sm = 0.0;
 3558    double x_lo_old = 0, y_lo_old = 0, b_i_old = 0, c_i_old = 0, d_i_old = 0;
 3559    double x_lo_old2 = 0, y_lo_old2 = 0, b_i_old2 = 0, c_i_old2 = 0, d_i_old2 = 0;
 3560    double x_lo_old3 = 0, y_lo_old3 = 0, b_i_old3 = 0, c_i_old3 = 0, d_i_old3 = 0;
 3561    unsigned int index_old = 0, index_old2 = 0, index_old3 = 0;
 3562          // printf("Length of rVec is %d\n",rVec.length);
 3563          //printf("combinedLenForInterp : %d\n",combinedLenForInterp);
 3564    for (i = 0; i < combinedLenForInterp; i++)
 3565    {
 3566 
 3567      t_i = i * deltaT / mTScaled;
 3568      //printf("%e,%e\n",t_i,tstartHi);
 3569      //re_temp = gsl_spline_eval(spline_re, t_i, acc_re);
 3570      //im_temp = gsl_spline_eval(spline_im, t_i, acc_im);
 3571      //phase_temp = gsl_spline_eval(spline_orbphase, t_i, acc_orbphase);
 3572 
 3573      optimized_gsl_spline_eval_e (spline_re, t_i, acc_re, &re_temp,
 3574                                       &index_old, &x_lo_old, &y_lo_old,
 3575                                       &b_i_old, &c_i_old, &d_i_old);
 3576      optimized_gsl_spline_eval_e (spline_im, t_i, acc_im, &im_temp,
 3577                                       &index_old2, &x_lo_old2, &y_lo_old2,
 3578                                       &b_i_old2, &c_i_old2, &d_i_old2);
 3579 
 3580      optimized_gsl_spline_eval_e (spline_orbphase, t_i, acc_orbphase, &phase_temp,
 3581                                       &index_old3, &x_lo_old3, &y_lo_old3,
 3582                                       &b_i_old3, &c_i_old3, &d_i_old3);
 3583      cm = cos(modeM * phase_temp);
 3584      sm = sin(modeM * phase_temp);
 3585 
 3586      // Reconstruct the intertial frame mode
 3587      re_In = re_temp * cm + im_temp * sm;
 3588      im_In = -re_temp * sm + im_temp * cm;
 3589      hLMAll->data[2 * k * sigReVec->length + i] = re_In;
 3590      hLMAll->data[(1 + 2 * k) * sigReVec->length + i] = im_In;
 3591      if (t_i > tstartHi && idx == 0)
 3592      {
 3593        idx = i-1;
 3594      }
 3595    }
 3596    hiSRndx = idx;
 3597 
 3598  }
 3599 
 3600#if outputDebug
 3601         fclose (out);
 3602        fclose(out2);
 3603#endif
 3604  }
 3605  gsl_spline_free( spline_orbphase);
 3606  gsl_interp_accel_free( acc_orbphase );
 3607  gsl_spline_free( spline_re);
 3608  gsl_interp_accel_free( acc_re );
 3609  gsl_spline_free( spline_im);
 3610  gsl_interp_accel_free( acc_im );
 3611}
 3612 
 3613    if ( OmVec )
 3614        XLALDestroyREAL8Vector(OmVec);
 3615    if ( omegaVec )
 3616         XLALDestroyREAL8Vector(omegaVec);
 3617 
 3618 
 3619 
 3620 
 3621 
 3622  /*
 3623   * STEP 8) Generate full IMR modes -- attaching ringdown to inspiral
 3624   */
 3625 
 3626  /* Attach the ringdown part to the inspiral */
 3627if(postAdiabaticFlag){
 3628    XLALGPSAdd (&tc, -(deltaT*hiSRndx + timePeak*mTScaled));
 3629  }
 3630for ( UINT4 k = 0; k<nModes; k++) {
 3631  for (i = 0; i < (INT4) (sigReHi->length / resampFac); i++)
 3632    {
 3633      hLMAll->data[2*k*sigReVec->length + i + hiSRndx] = hLMAllHi->data[2*k*sigReHi->length + i*resampFac];
 3634      hLMAll->data[(2*k+1)*sigReVec->length + i + hiSRndx] = hLMAllHi->data[(2*k+1)*sigReHi->length + i*resampFac];
 3635    }
 3636}
 3637  // printf("The legnth of sigReVec is %d\n",sigReVec->length);
 3638  // printf("The hiSRndx is %d\n",hiSRndx);
 3639  // printf("The legnth of sigReHi is %d\n",sigReHi->length);
 3640  // printf("The length of hLMAll is %d\n",hLMAll->length);
 3641 
 3642 
 3643    /* Cut wf if fMin requested by user was high */
 3644    INT4 kMin = 0;
 3645    if ( fStart != fMin ) {
 3646        REAL8 finst;
 3647        gsl_spline *splineRe = NULL;
 3648        gsl_interp_accel *accRe = NULL;
 3649        gsl_spline *splineIm = NULL;
 3650        gsl_interp_accel *accIm = NULL;
 3651        //RC: since the cut of the waveform is done on the 22 mode, we assign here the 22 mode to sigReVec and sigImVec
 3652        for ( i=0; i<(INT4)sigReVec->length; i++) {
 3653          sigReVec->data[i] = hLMAll->data[i];
 3654          sigImVec->data[i] = hLMAll->data[sigReVec->length + i];
 3655        }
 3656        REAL8Vector *tmpRe = XLALCreateREAL8Vector(sigReVec->length), *tmpIm = XLALCreateREAL8Vector(sigReVec->length);
 3657        for ( i=0; i < (INT4) sigReVec->length; i++) {
 3658            tmpRe->data[i] = sigReVec->data[i] / amp0;
 3659            tmpIm->data[i] = sigImVec->data[i] / amp0;
 3660        }
 3661        splineRe = gsl_spline_alloc (gsl_interp_cspline, sigReVec->length);
 3662        splineIm = gsl_spline_alloc (gsl_interp_cspline, sigImVec->length);
 3663        accRe = gsl_interp_accel_alloc ();
 3664        accIm = gsl_interp_accel_alloc ();
 3665        REAL8 dRe, dIm;
 3666        REAL8Vector *timeList;
 3667        timeList = XLALCreateREAL8Vector (sigReVec->length);
 3668        for ( i=0; i < (INT4) sigReVec->length; i++) {
 3669            timeList->data[i] = i*deltaT/mTScaled;
 3670        }
 3671        gsl_spline_init (splineRe, timeList->data, tmpRe->data, tmpRe->length);
 3672        gsl_spline_init (splineIm, timeList->data, tmpIm->data, tmpIm->length);
 3673        REAL8 norm;
 3674        for ( i=1; i < (INT4) tmpRe->length - 1; i++) {
 3675            norm = tmpRe->data[i]*tmpRe->data[i] + tmpIm->data[i]*tmpIm->data[i];
 3676            if ( norm > 0. ) {
 3677                dRe = gsl_spline_eval_deriv (splineRe, timeList->data[i], accRe);
 3678                dIm = gsl_spline_eval_deriv (splineIm, timeList->data[i], accIm);
 3679                finst = (dRe*tmpIm->data[i] - dIm*tmpRe->data[i])/norm;
 3680//                printf("%.16e %.16e\n", timeList->data[i], finst);
 3681                finst = finst/(2.*LAL_PI*mTScaled);
 3682//                printf("%.16e %.16e %.16e\n", timeList->data[i], finst, fMin);
 3683                if ( finst > fMin ) {
 3684                    kMin = i;
 3685                    break;
 3686                }
 3687            }
 3688            else {
 3689                continue;
 3690            }
 3691        }
 3692        gsl_spline_free( splineRe );
 3693        gsl_interp_accel_free( accRe );
 3694        gsl_spline_free( splineIm );
 3695        gsl_interp_accel_free( accIm );
 3696        XLALDestroyREAL8Vector( tmpRe );
 3697        XLALDestroyREAL8Vector( tmpIm );
 3698        XLALDestroyREAL8Vector(timeList);
 3699    }
 3700 
 3701#if debugOutput
 3702    for ( UINT4 k = 0; k<nModes; k++) {
 3703        modeL  = lmModes[k][0];
 3704        modeM = lmModes[k][1];
 3705        char filename[sizeof "saModesXXIMR.dat"];
 3706        sprintf(filename,"saModes%01d%01dIMR.dat",modeL,modeM);
 3707        out = fopen (filename, "w");
 3708        for ( i=0; i<(INT4)sigReVec->length; i++) {
 3709            fprintf (out, "%.16e %.16e %.16e\n", i*deltaT / mTScaled,hLMAll->data[2*k*sigReVec->length + i]/amp0,hLMAll->data[(1+2*k)*sigReVec->length + i]/amp0);
 3710        }
 3711        fclose(out);
 3712    }
 3713#endif
 3714XLALGPSAdd (&tc, deltaT * (REAL8) kMin);
 3715/*
 3716 * STEP 9) Generate full IMR hp and hx waveforms
 3717 */
 3718//RC: this function stops now here and return the array with the modes
 3719 
 3720/*
 3721 * STEP 9) Return real and imaginary part of the modes
 3722 */
 3723  SphHarmTimeSeries *hlms = NULL;
 3724  char mode_name[32];
 3725 
 3726for ( UINT4 k = 0; k<nModes; k++) {
 3727  modeL  = lmModes[k][0];
 3728  modeM = lmModes[k][1];
 3729  snprintf(mode_name, sizeof(mode_name), "(%d, %d) mode", modeL, modeM);
 3730  COMPLEX16TimeSeries *tmp_mode = XLALCreateCOMPLEX16TimeSeries(mode_name, &tc, 0.0,
 3731    deltaT, &lalStrainUnit, sigReVec->length - kMin);
 3732  for (UINT4 t = kMin; t< (UINT4) sigReVec->length; t++)
 3733      {
 3734            tmp_mode->data->data[t - kMin]  = hLMAll->data[2*k*sigReVec->length + t];
 3735            tmp_mode->data->data[t - kMin]  += I * hLMAll->data[(2*k+1)*sigReVec->length + t];
 3736        }
 3737        hlms = XLALSphHarmTimeSeriesAddMode(hlms, tmp_mode, modeL, modeM);
 3738        XLALDestroyCOMPLEX16TimeSeries(tmp_mode);
 3739      }
 3740      /* Point the output pointers to the relevant time series and return */
 3741      (*hlmmode) = hlms;
 3742 
 3743      /* Free memory */
 3744      XLALDestroyREAL8Vector (tmpValues);
 3745      XLALDestroyREAL8Vector (sigmaKerr);
 3746      XLALDestroyREAL8Vector (sigmaStar);
 3747      XLALDestroyREAL8Vector (values);
 3748      XLALDestroyREAL8Vector (rdMatchPoint);
 3749      XLALDestroyREAL8Vector (ampNQC);
 3750      XLALDestroyREAL8Vector (phaseNQC);
 3751      XLALDestroyREAL8Vector (sigReVec);
 3752      XLALDestroyREAL8Vector (sigImVec);
 3753      XLALDestroyREAL8Vector (sigReCoorbVec);
 3754      XLALDestroyREAL8Vector (sigImCoorbVec);
 3755      XLALAdaptiveRungeKuttaFree (integrator);
 3756      //SM
 3757      //XLALDestroyREAL8Array (dynamics);
 3758      //XLALDestroyREAL8Array (dynamicsHi);
 3759      //SM
 3760      gsl_matrix_free (nqcCoeffsMatrix);
 3761 
 3762      if (dynamicstmp)
 3763        {
 3764          XLALDestroyREAL8Array (dynamicstmp);  // DAVIDS: We are done with these now
 3765        }
 3766      if (dynamicsHitmp)
 3767        {
 3768          XLALDestroyREAL8Array (dynamicsHitmp);        // DAVIDS: Done with these now
 3769        }
 3770 
 3771      XLALDestroyREAL8Vector (sigReHi);
 3772      XLALDestroyREAL8Vector (sigImHi);
 3773      XLALDestroyREAL8Vector (omegaHi);
 3774      if ( hLMAllHi )
 3775          XLALDestroyREAL8Vector (hLMAllHi);
 3776      if ( hLMAll )
 3777          XLALDestroyREAL8Vector (hLMAll);
 3778      if ( hamV )
 3779          XLALDestroyREAL8Vector (hamV);
 3780      if ( hamVHi )
 3781          XLALDestroyREAL8Vector (hamVHi);
 3782 
 3783      if (vPhiVec)
 3784        XLALDestroyREAL8Vector (vPhiVec);
 3785 
 3786      if (vPhiVecHi)
 3787        XLALDestroyREAL8Vector (vPhiVecHi);
 3788 
 3789      if (tVecInterp)
 3790        XLALDestroyREAL8Vector(tVecInterp);
 3791 
 3792      if (phiVecInterp)
 3793        XLALDestroyREAL8Vector(phiVecInterp);
 3794 
 3795      if (rVecInterp)
 3796        XLALDestroyREAL8Vector(rVecInterp);
 3797 
 3798      if (prVecInterp)
 3799        XLALDestroyREAL8Vector(prVecInterp);
 3800 
 3801      if (pphiVecInterp)
 3802        XLALDestroyREAL8Vector(pphiVecInterp);
 3803 
 3804      //SM
 3805      // Copy dynamics to output in the form of a REAL8Vector (required for SWIG wrapping, REAL8Array does not work)
 3806      *dynamics_out = XLALCreateREAL8Vector(5 * retLen_out);
 3807      *dynamicsHi_out = XLALCreateREAL8Vector(5 * retLenHi_out);
 3808      for (i = 0; i < 5*retLen_out; i++) (*dynamics_out)->data[i] = dynamics->data[i];
 3809      // We have to add the starting time of the high-sampling dynamics, as the output of the integrator starts with 0
 3810      for (i = 0; i < retLenHi_out; i++) (*dynamicsHi_out)->data[i] = tstartHi + dynamicsHi->data[i];
 3811      for (i = retLenHi_out; i < 5*retLenHi_out; i++) (*dynamicsHi_out)->data[i] = dynamicsHi->data[i];
 3812      XLALDestroyREAL8Array (dynamics);
 3813      XLALDestroyREAL8Array (dynamicsHi);
 3814      //SM
 3815 
 3816      return XLAL_SUCCESS;
 3817    }
 3818 
 3819/**
 3820 * This function takes the modes from the function XLALSimIMRSpinAlignedEOBModes and combine them into h+ and hx
 3821 */
 3822 
 3823int
 3824XLALSimIMRSpinAlignedEOBWaveformAll (
 3825    REAL8TimeSeries ** hplus,
 3826    /**<< OUTPUT, real part of the modes */
 3827    REAL8TimeSeries ** hcross,
 3828    /**<< OUTPUT, complex part of the modes */
 3829    const REAL8 phiC,
 3830    /**<< coalescence orbital phase (rad) */
 3831    REAL8 deltaT,
 3832    /**<< sampling time step */
 3833    const REAL8 m1SI,
 3834    /**<< mass-1 in SI unit */
 3835    const REAL8 m2SI,
 3836    /**<< mass-2 in SI unit */
 3837    const REAL8 fMin,
 3838    /**<< starting frequency of the 22 mode (Hz) */
 3839    const REAL8 r,
 3840    /**<< distance in SI unit */
 3841    const REAL8 inc,
 3842    /**<< inclination angle */
 3843    const REAL8 spin1z,
 3844    /**<< z-component of spin-1, dimensionless */
 3845    const REAL8 spin2z,
 3846    /**<< z-component of spin-2, dimensionless */
 3847    UINT4 SpinAlignedEOBversion,
 3848    /**<< 1 for SEOBNRv1, 2 for SEOBNRv2, 4 for SEOBNRv4, 201 for SEOBNRv2T, 401 for SEOBNRv4T, 41 for SEOBNRv4HM */
 3849    const REAL8 lambda2Tidal1,
 3850    /**<< dimensionless adiabatic quadrupole tidal deformability for body 1 (2/3 k2/C^5) */
 3851    const REAL8 lambda2Tidal2,
 3852    /**<< dimensionless adiabatic quadrupole tidal deformability for body 2 (2/3 k2/C^5) */
 3853    const REAL8 omega02Tidal1,
 3854    /**<< quadrupole f-mode angular freq for body 1 m_1*omega_{02,1}*/
 3855    const REAL8 omega02Tidal2,
 3856    /**<< quadrupole f-mode angular freq for body 2 m_2*omega_{02,2}*/
 3857    const REAL8 lambda3Tidal1,
 3858    /**<< dimensionless adiabatic octupole tidal deformability for body 1 (2/15 k3/C^7) */
 3859    const REAL8 lambda3Tidal2,
 3860    /**<< dimensionless adiabatic octupole tidal deformability for body 2 (2/15 k3/C^7) */
 3861    const REAL8 omega03Tidal1,
 3862    /**<< octupole f-mode angular freq for body 1 m_1*omega_{03,1}*/
 3863    const REAL8 omega03Tidal2,
 3864    /**<< octupole f-mode angular freq for body 2 m_2*omega_{03,2}*/
 3865    const REAL8 quadparam1,
 3866    /**<< parameter kappa_1 of the spin-induced quadrupole for body 1, quadrupole is Q_A = -kappa_A m_A^3 chi_A^2 */
 3867    const REAL8 quadparam2,
 3868    /**<< parameter kappa_2 of the spin-induced quadrupole for body 2, quadrupole is Q_A = -kappa_A m_A^3 chi_A^2 */
 3869    REAL8Vector *nqcCoeffsInput,
 3870    /**<< Input NQC coeffs */
 3871    const INT4 nqcFlag,
 3872    /**<< Flag to tell the code to use the NQC coeffs input thorugh nqcCoeffsInput */
 3873    LALValue *ModeArray,
 3874    /**<< Structure containing the modes to use in the waveform */
 3875    LALDict *TGRParams
 3876    /**<< dictionary containing parameters for tests of General Relativity */
 3877)
 3878  {
 3879 
 3880    REAL8 coa_phase = phiC;
 3881 
 3882    SphHarmTimeSeries *hlms = NULL;
 3883    //SM
 3884    REAL8Vector *dynamics = NULL;
 3885    REAL8Vector *dynamicsHi = NULL;
 3886    //SM
 3887 
 3888    LALDict *PAParams = XLALCreateDict();
 3889 
 3890    //RC: XLALSimIMRSpinAlignedEOBModes computes the modes and put them into hlm
 3891 
 3892    if(XLALSimIMRSpinAlignedEOBModes (
 3893        &hlms, //SM
 3894        &dynamics, &dynamicsHi, //SM
 3895        deltaT,
 3896        m1SI, m2SI,
 3897        fMin,
 3898        r,
 3899        spin1z, spin2z,
 3900        SpinAlignedEOBversion,
 3901        lambda2Tidal1, lambda2Tidal2,
 3902        omega02Tidal1, omega02Tidal2,
 3903        lambda3Tidal1, lambda3Tidal2,
 3904        omega03Tidal1, omega03Tidal2,
 3905        quadparam1, quadparam2,
 3906        nqcCoeffsInput, nqcFlag,
 3907        PAParams,
 3908        TGRParams) == XLAL_FAILURE
 3909    ){
 3910        if(dynamics) XLALDestroyREAL8Vector(dynamics);
 3911        if(dynamicsHi) XLALDestroyREAL8Vector(dynamicsHi);
 3912        XLAL_ERROR (XLAL_EFUNC);
 3913    };
 3914 
 3915    //RC: For SEOBNRv4T we also need to exit from this function when  nqcFlag == 1 because when this flag is 1, it is only computing the NQCs and not the wf
 3916    if (nqcFlag == 1){
 3917      if(hlms)
 3918        XLALDestroySphHarmTimeSeries(hlms);
 3919      return XLAL_SUCCESS;
 3920    }
 3921 
 3922    //RC: Here we read lenght and epoch of the modes. They are all the same by definition.
 3923    INT4 len = hlms->mode->data->length;
 3924    LIGOTimeGPS tc = hlms->mode->epoch;
 3925 
 3926    //RC: defining and initializing to 0 the hp and hc vectors
 3927    REAL8TimeSeries *hPlusTS =
 3928      XLALCreateREAL8TimeSeries ("H_PLUS", &tc, 0.0, deltaT, &lalStrainUnit,
 3929               len);
 3930    REAL8TimeSeries *hCrossTS =
 3931      XLALCreateREAL8TimeSeries ("H_CROSS", &tc, 0.0, deltaT, &lalStrainUnit,
 3932              len);
 3933    memset( hPlusTS->data->data, 0, hPlusTS->data->length * sizeof(REAL8) );
 3934    memset( hCrossTS->data->data, 0, hCrossTS->data->length * sizeof(REAL8) );
 3935 
 3936    //RC: adding all the modes in the SphHarmTimeSeries hlms to hp and hc
 3937    SphHarmTimeSeries *hlms_temp = hlms;
 3938    while ( hlms_temp ) {
 3939      if (XLALSimInspiralModeArrayIsModeActive(ModeArray, hlms_temp->l, hlms_temp->m) == 1){
 3940        /*Here we check if the mode generated is in the ModeArray structure
 3941        */
 3942          //R.C. the angles in the spin-weighted spherical harmonics are set accordingly to the document https://dcc.ligo.org/DocDB/0152/T1800226/003/LAL_GW_Frames.pdf
 3943          //for the conventions in master
 3944          XLALSimAddMode(hPlusTS, hCrossTS, hlms_temp->mode, inc, LAL_PI/2. - coa_phase, hlms_temp->l, hlms_temp->m, 1);
 3945          /*When the function XLALSimAddMode is called with the last argument == 1
 3946          *is using both +m and -m modes
 3947          */
 3948          //printf("Mode (%d,%d) active\n", hlms_temp->l,hlms_temp->m);
 3949        }
 3950        hlms_temp = hlms_temp->next;
 3951    }
 3952 
 3953 
 3954 
 3955    /* Point the output pointers to the relevant time series and return */
 3956    (*hplus) = hPlusTS;
 3957    (*hcross) = hCrossTS;
 3958 
 3959    if(hlms)
 3960      XLALDestroySphHarmTimeSeries(hlms);
 3961 
 3962    XLALDestroyDict(PAParams);
 3963 
 3964    //SM
 3965    if(dynamics) XLALDestroyREAL8Vector(dynamics);
 3966    if(dynamicsHi) XLALDestroyREAL8Vector(dynamicsHi);
 3967    //SM
 3968 
 3969    return XLAL_SUCCESS;
 3970  }
 3971 
 3972/** @} */
