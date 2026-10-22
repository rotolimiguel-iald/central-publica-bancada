    1/*
    2*  Copyright (C) 2008 Yi Pan, B.S. Sathyaprakash (minor modificaitons), Prayush
    3*  Kumar (some additions)
    4*
    5*  This program is free software; you can redistribute it and/or modify
    6*  it under the terms of the GNU General Public License as published by
    7*  the Free Software Foundation; either version 2 of the License, or
    8*  (at your option) any later version.
    9*
   10*  This program is distributed in the hope that it will be useful,
   11*  but WITHOUT ANY WARRANTY; without even the implied warranty of
   12*  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   13*  GNU General Public License for more details.
   14*
   15*  You should have received a copy of the GNU General Public License
   16*  along with with program; see the file COPYING. If not, write to the
   17*  Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
   18*  MA  02110-1301  USA
   19*/
   20 
   21/**
   22 * \author Yi Pan, Craig Robinson, Stas Babak, Andrea Taracchini
   23 * \file
   24 *
   25 * \brief Module to compute the ring-down waveform as linear combination
   26 * of quasi-normal-modes decaying waveforms, which can be attached to
   27 * the inspiral part of the compat binary coalescing waveform.
   28 * The method is describe in Sec. II C of Pan et al. PRD 84, 124052 (2011),
   29 * specifically Eqs. 30 - 32.
   30 * Eqs. 30 and 31 are written in explicity linear equation systems in
   31 * DCC document T1100433.
   32 * This method is currently used for EOBNRv2 and SEOBNRv1 models. The only difference
   33 * between the two models in ring-down waveform is the pseudo-QNM introduced
   34 * in the latter (see Taracchini et al. PRD 86, 024011 (2012) for more details).
   35 */
   36#ifndef _LALSIMIMREOBHYBRIDRINGDOWN_C
   37#define _LALSIMIMREOBHYBRIDRINGDOWN_C
   38#include <math.h>
   39#include <complex.h>
   40#include <stdlib.h>
   41#include <lal/LALStdlib.h>
   42#include <lal/AVFactories.h>
   43#include <lal/SeqFactories.h>
   44#include <gsl/gsl_linalg.h>
   45#include <gsl/gsl_interp.h>
   46#include <gsl/gsl_spline.h>
   47#include <gsl/gsl_matrix.h>
   48 
   49#include "LALSimIMREOBNRv2.h"
   50#include "LALSimBlackHoleRingdown.h"
   51#include "LALSimIMREOBNQCCorrection.c"
   52 
   53 
   54#ifdef __GNUC__
   55#define UNUSED __attribute__ ((unused))
   56#else
   57#define UNUSED
   58#endif
   59 
   60#define LMax 6
   61#define MMax 6
   62 
   63//////////////////////////////////////////////////////////////////////////////////////////////////////////
   64/* Defining matrices to store the coefficients that enter amplitude and phase of the RD signal of SEOBNRv4 and SEOBNRv4HM */
   65 
   66 
   67static REAL8 XLALCalculateRDAmplitudeCoefficient1( UINT4 modeL, UINT4 modeM, REAL8 eta, REAL8 chi){
   68  REAL8 A1coeff00[LMax][MMax]={{0}};
   69  REAL8 A1coeff01[LMax][MMax]={{0}};
   70  REAL8 A1coeff02[LMax][MMax]={{0}};
   71  REAL8 A1coeff10[LMax][MMax]={{0}};
   72  REAL8 A1coeff11[LMax][MMax]={{0}};
   73  REAL8 A1coeff20[LMax][MMax]={{0}};
   74  REAL8 A1coeff21[LMax][MMax]={{0}};
   75  REAL8 A1coeff31[LMax][MMax]={{0}};
   76 
   77  //////////////////////////////////////////////////////////////////////////////////////////////////////////
   78  /* Fit coefficients that enter amplitude of the RD signal for SEOBNRv4 and SEOBNRv4HM*/
   79  /* Eq. (54) of https://dcc.ligo.org/T1600383 for SEOBNRv4 and 22 mode SEOBNRv4HM*/
   80  /* Eqs. (C1, C3, C5, C7) of https://arxiv.org/pdf/1803.10701.pdf for SEOBNRv4HM*/
   81 
   82  A1coeff00[2][2] = 0.0830664;
   83  A1coeff01[2][2] = -0.0196758;
   84  A1coeff02[2][2] = -0.0136459;
   85  A1coeff10[2][2] = 0.0612892;
   86  A1coeff11[2][2] = 0.00146142;
   87  A1coeff20[2][2] = -0.0893454;
   88 
   89  A1coeff00[2][1] = 0.07780330893915006;
   90  A1coeff01[2][1] = -0.05070638166864379;
   91  A1coeff10[2][1] = 0.24091006920322164;
   92  A1coeff11[2][1] = 0.38582622780596576;
   93  A1coeff20[2][1] = -0.7456327888190485;
   94  A1coeff21[2][1] = -0.9695534075470388;
   95 
   96  A1coeff00[3][3] = 0.07638733045623343;
   97  A1coeff01[3][3] = -0.030993441267953236;
   98  A1coeff10[3][3] = 0.2543447497371546;
   99  A1coeff11[3][3] = 0.2516879591102584;
  100  A1coeff20[3][3] = -1.0892686061231245;
  101  A1coeff21[3][3] = -0.7980907313033606;
  102 
  103  A1coeff00[4][4] = -0.06392710223439678;
  104  A1coeff01[4][4] = -0.03646167590514318;
  105  A1coeff10[4][4] = 0.345195277237925;
  106  A1coeff11[4][4] = 1.2777441574118558;
  107  A1coeff20[4][4] = -1.764352185878576;
  108  A1coeff21[4][4] = -14.825262897834696;
  109  A1coeff31[4][4] = 40.67135475479875;
  110 
  111  A1coeff00[5][5] = -0.06704614393611373;
  112  A1coeff01[5][5] = 0.021905949257025503;
  113  A1coeff10[5][5] = -0.24754936787743445;
  114  A1coeff11[5][5] = -0.0943771022698497;
  115  A1coeff20[5][5] = 0.7588042862093705;
  116  A1coeff21[5][5] = 0.4357768883690394;
  117 
  118 
  119 
  120  return A1coeff00[modeL][modeM] + A1coeff01[modeL][modeM] * chi + A1coeff02[modeL][modeM] * chi * chi + A1coeff10[modeL][modeM] * eta +
  121  A1coeff11[modeL][modeM] * eta * chi + A1coeff20[modeL][modeM] * eta * eta + A1coeff21[modeL][modeM]*eta*eta*chi + A1coeff31[modeL][modeM]*eta*eta*eta*chi;
  122 
  123}
  124 
  125 
  126static REAL8 XLALCalculateRDAmplitudeCoefficient2( UINT4 modeL, UINT4 modeM, REAL8 eta, REAL8 chi){
  127 
  128  REAL8 A2coeff00[LMax][MMax]={{0}};
  129  REAL8 A2coeff01[LMax][MMax]={{0}};
  130  REAL8 A2coeff10[LMax][MMax]={{0}};
  131  REAL8 A2coeff11[LMax][MMax]={{0}};
  132  REAL8 A2coeff20[LMax][MMax]={{0}};
  133  REAL8 A2coeff21[LMax][MMax]={{0}};
  134  REAL8 A2coeff31[LMax][MMax]={{0}};
  135 
  136 
  137  //////////////////////////////////////////////////////////////////////////////////////////////////////////
  138  /* Fit coefficients that enter amplitude of the RD signal of SEOBNRv4 and SEOBNRv4HM*/
  139  /* Eq. (55) of https://dcc.ligo.org/T1600383 for SEOBNRv4 and 22 mode SEOBNRv4HM*/
  140  /* Eqs. (C1, C3, C5, C7) of https://arxiv.org/pdf/1803.10701.pdf for SEOBNRv4HM*/
  141  A2coeff00[2][2] = -0.623953;
  142  A2coeff01[2][2] = -0.371365;
  143  A2coeff10[2][2] = 1.39777;
  144  A2coeff11[2][2] = 2.40203;
  145  A2coeff20[2][2] = -1.82173;
  146  A2coeff21[2][2] = -5.25339;
  147 
  148  A2coeff00[2][1] = -1.2451852641667298;
  149  A2coeff01[2][1] = -1.195786238319961;
  150  A2coeff10[2][1] = 6.134202504312409;
  151  A2coeff11[2][1] = 15.66696619631313;
  152  A2coeff20[2][1] = -14.67251127485556;
  153  A2coeff21[2][1] = -44.41982201432511;
  154 
  155  A2coeff00[3][3] = -0.8325292359346013;
  156  A2coeff01[3][3] = -0.598880303198448;
  157  A2coeff10[3][3] = 2.767989795032018;
  158  A2coeff11[3][3] = 5.904371617277156;
  159  A2coeff20[3][3] = -7.028151926115957;
  160  A2coeff21[3][3] = -18.232606706124482;
  161 
  162  A2coeff00[4][4] = 0.7813275473485185;
  163  A2coeff01[4][4] = 0.8094706044462984;
  164  A2coeff10[4][4] = -5.18689829943586;
  165  A2coeff11[4][4] = -5.38343327318501;
  166  A2coeff20[4][4] = 14.026415859369477;
  167  A2coeff21[4][4] = 0.1051625997942299;
  168  A2coeff31[4][4] = 46.978434956814006;
  169 
  170  A2coeff00[5][5] = 1.6763424265367357;
  171  A2coeff01[5][5] = 0.4925695499534606;
  172  A2coeff10[5][5] = -5.604559311983177;
  173  A2coeff11[5][5] = -6.209095657439377;
  174  A2coeff20[5][5] = 16.751319143123386;
  175  A2coeff21[5][5] = 16.778452555342554;
  176 
  177  return A2coeff00[modeL][modeM] + A2coeff01[modeL][modeM] * chi + A2coeff10[modeL][modeM] * eta +
  178  A2coeff11[modeL][modeM] * eta * chi + A2coeff20[modeL][modeM] * eta * eta + A2coeff21[modeL][modeM] * eta * eta * chi + A2coeff31[modeL][modeM]*eta*eta*eta*chi;
  179}
  180 
  181static REAL8 XLALCalculateRDPhaseCoefficient1( UINT4 modeL, UINT4 modeM, REAL8 eta, REAL8 chi){
  182 
  183  REAL8 P1coeff00[LMax][MMax]={{0}};
  184  REAL8 P1coeff01[LMax][MMax]={{0}};
  185  REAL8 P1coeff02[LMax][MMax]={{0}};
  186  REAL8 P1coeff10[LMax][MMax]={{0}};
  187  REAL8 P1coeff11[LMax][MMax]={{0}};
  188  REAL8 P1coeff20[LMax][MMax]={{0}};
  189  REAL8 P1coeff21[LMax][MMax]={{0}};
  190  REAL8 P1coeff31[LMax][MMax]={{0}};
  191 
  192  //////////////////////////////////////////////////////////////////////////////////////////////////////////
  193  /* Fit coefficients that enter the phase of the RD signal of SEOBNRv4 and SEOBNRv4HM*/
  194  /* Eq. (62) of https://dcc.ligo.org/T1600383 for SEOBNRv4 and 22 mode SEOBNRv4HM*/
  195  /* Eqs. (C9, C11, C13, C15) of https://arxiv.org/pdf/1803.10701.pdf for SEOBNRv4HM*/
  196 
  197  P1coeff00[2][2] = 0.147584;
  198  P1coeff01[2][2] = 0.00779176;
  199  P1coeff02[2][2] = -0.0244358;
  200  P1coeff10[2][2] = 0.263456;
  201  P1coeff11[2][2] = -0.120853;
  202  P1coeff20[2][2] = -0.808987;
  203 
  204  P1coeff00[2][1] = 0.15601401627613815;
  205  P1coeff01[2][1] = 0.10219957917717622;
  206  P1coeff10[2][1] = 0.023346852452720928;
  207  P1coeff11[2][1] = -0.9435308286367039;
  208  P1coeff20[2][1] = 0.15326558178697175;
  209  P1coeff21[2][1] = 1.7979082057513565;
  210 
  211  P1coeff00[3][3] = 0.11085299117493969;
  212  P1coeff01[3][3] = 0.018959099261813613;
  213  P1coeff10[3][3] = 0.9999800463662053;
  214  P1coeff11[3][3] = -0.729149797691242;
  215  P1coeff20[3][3] = -3.3983315694441125;
  216  P1coeff21[3][3] = 2.5192011762934037;
  217 
  218  P1coeff00[4][4] = 0.11498976343440313;
  219  P1coeff01[4][4] = 0.008389519706605305;
  220  P1coeff10[4][4] = 1.6126522800609633;
  221  P1coeff11[4][4] = -0.8069979888526699;
  222  P1coeff20[4][4] = -6.255895564079467;
  223  P1coeff21[4][4] = 7.595651881827078;
  224  P1coeff31[4][4] = -19.32367406125053;
  225 
  226  P1coeff00[5][5] = 0.16465380962882128;
  227  P1coeff01[5][5] = -0.026574817803812007;
  228  P1coeff10[5][5] = -0.19184523794508765;
  229  P1coeff11[5][5] = -0.05519618962738479;
  230  P1coeff20[5][5] = 0.33328424135336965;
  231  P1coeff21[5][5] = 0.3194274548351241;
  232 
  233 
  234  return P1coeff00[modeL][modeM] + P1coeff01[modeL][modeM] * chi + P1coeff02[modeL][modeM] * chi * chi + P1coeff10[modeL][modeM] * eta +
  235  P1coeff11[modeL][modeM] * eta * chi + P1coeff20[modeL][modeM] * eta * eta + P1coeff21[modeL][modeM]*eta*eta*chi + P1coeff31[modeL][modeM]*eta*eta*eta*chi;
  236 
  237}
  238 
  239static REAL8 XLALCalculateRDPhaseCoefficient2( UINT4 modeL, UINT4 modeM, REAL8 eta, REAL8 chi){
  240 
  241  REAL8 P2coeff00[LMax][MMax]={{0}};
  242  REAL8 P2coeff01[LMax][MMax]={{0}};
  243  REAL8 P2coeff02[LMax][MMax]={{0}};
  244  REAL8 P2coeff12[LMax][MMax]={{0}};
  245  REAL8 P2coeff10[LMax][MMax]={{0}};
  246  REAL8 P2coeff11[LMax][MMax]={{0}};
  247  REAL8 P2coeff20[LMax][MMax]={{0}};
  248  REAL8 P2coeff21[LMax][MMax]={{0}};
  249  REAL8 P2coeff31[LMax][MMax]={{0}};
  250 
  251  //////////////////////////////////////////////////////////////////////////////////////////////////////////
  252  /* Fit coefficients that enter the phase of the RD signal of SEOBNRv4 and SEOBNRv4HM*/
  253  /* Eq. (63) of https://dcc.ligo.org/T1600383 for SEOBNRv4 and 22 mode SEOBNRv4HM*/
  254  /* Eqs. (C10, C12, C14, C16) of https://arxiv.org/pdf/1803.10701.pdf for SEOBNRv4HM*/
  255  P2coeff00[2][2] = 2.46654;
  256  P2coeff01[2][2] = 3.13067;
  257  P2coeff02[2][2] = 0.581626;
  258  P2coeff10[2][2] = -6.99396;
  259  P2coeff11[2][2] = -9.61861;
  260  P2coeff20[2][2] = 17.5646;
  261 
  262  P2coeff00[2][1] = 2.7886287922318105;
  263  P2coeff01[2][1] = 4.29290053494256;
  264  P2coeff10[2][1] = -0.8145406685320334;
  265  P2coeff11[2][1] = -15.93796979597706;
  266  P2coeff20[2][1] = 5.549338798935832;
  267  P2coeff21[2][1] = 12.649775582333442;
  268  P2coeff02[2][1] = 2.5582321247274726;
  269  P2coeff12[2][1] = -10.232928498772893;
  270 
  271  P2coeff00[3][3] = 2.7825237371542735;
  272  P2coeff01[3][3] = 2.8796835808075003;
  273  P2coeff10[3][3] = -7.844741660437831;
  274  P2coeff11[3][3] = -34.7670039322078;
  275  P2coeff20[3][3] = 27.181024362399302;
  276  P2coeff21[3][3] = 127.13948436435182;
  277 
  278  P2coeff00[4][4] = 3.111817347262856;
  279  P2coeff01[4][4] = 5.399341180960216;
  280  P2coeff10[4][4] = 15.885333959709488;
  281  P2coeff11[4][4] = -87.92421137153823;
  282  P2coeff20[4][4] = -79.64931908155609;
  283  P2coeff21[4][4] = 657.7156442271963;
  284  P2coeff31[4][4] = -1555.2968529739226;
  285  P2coeff02[4][4] = 2.3832321567874686;
  286  P2coeff12[4][4] = -9.532928476043567;
  287 
  288  P2coeff00[5][5] = 11.102447263357977;
  289  P2coeff01[5][5] = 6.015112119742853;
  290  P2coeff10[5][5] = -58.605776859097084;
  291  P2coeff11[5][5] = -81.68032025902797;
  292  P2coeff20[5][5] = 176.60643662729498;
  293  P2coeff21[5][5] = 266.47345742836745;
  294 
  295 
  296  return P2coeff00[modeL][modeM] + P2coeff01[modeL][modeM] * chi + P2coeff02[modeL][modeM] * chi * chi + P2coeff12[modeL][modeM] * chi * chi * eta + P2coeff10[modeL][modeM] * eta +
  297  P2coeff11[modeL][modeM] * eta * chi + P2coeff20[modeL][modeM] * eta * eta + P2coeff21[modeL][modeM]*eta*eta*chi + P2coeff31[modeL][modeM]*eta*eta*eta*chi;
  298}
  299 
  300 
  301 
  302static INT4 XLALSimFindIndexMaxAmpli( UINT4 * indAmax, REAL8Vector * timeVec, REAL8Vector * ampWave, REAL8 * valAmax, REAL8 tofAmax );
  303 
  304/**
  305 * Generates the ringdown wave associated with the given real
  306 * and imaginary parts of the inspiral waveform. The parameters of
  307 * the ringdown, such as amplitude and phase offsets, are determined
  308 * by solving the linear equations defined in the DCC document T1100433.
  309 * In the linear equations Ax=y,
  310 * A is a 16-by-16 matrix depending on QNM (complex) frequencies,
  311 * x is a 16-d vector of the 8 unknown complex QNM amplitudes,
  312 * y is a 16-d vector depending on inspiral-plunge waveforms and their derivatives near merger.
  313 */
  314static INT4 XLALSimIMREOBHybridRingdownWave(REAL8Vector * rdwave1,
  315                                   /**<< OUTPUT, Real part of ringdown waveform */
  316    REAL8Vector * rdwave2,         /**<< OUTPUT, Imag part of ringdown waveform */
  317    const REAL8 dt,                /**<< Sampling interval */
  318    const REAL8 mass1,             /**<< First component mass (in Solar masses) */
  319    const REAL8 mass2,             /**<< Second component mass (in Solar masses) */
  320    REAL8VectorSequence * inspwave1,
  321                                   /**<< Values and derivs of real part inspiral waveform */
  322    REAL8VectorSequence * inspwave2,
  323                                   /**<< Values and derivs of imag part inspiral waveform */
  324    COMPLEX16Vector * modefreqs,   /**<< Complex freqs of ringdown (scaled by total mass) */
  325    REAL8Vector * matchrange       /**<< Times which determine the comb of ringdown attachment */
  326    )
  327{
  328 
  329    /* XLAL error handling */
  330    INT4 errcode = XLAL_SUCCESS;
  331 
  332    /* For checking GSL return codes */
  333    INT4 gslStatus;
  334 
  335    UINT4 i, j, k, nmodes = 8;
  336 
  337    /* Sampling rate from input */
  338    REAL8 t1, t2, t3, t4, t5, rt;
  339    gsl_matrix *coef;
  340    gsl_vector *hderivs;
  341    gsl_vector *x;
  342    gsl_permutation *p;
  343    REAL8Vector *modeamps;
  344    int s;
  345    REAL8 tj;
  346    REAL8 m;
  347 
  348    /* mass in geometric units */
  349    m = (mass1 + mass2) * LAL_MTSUN_SI;
  350    t5 = (matchrange->data[0] - matchrange->data[1]) * m;
  351    rt = -t5 / 5.;
  352 
  353    t4 = t5 + rt;
  354    t3 = t4 + rt;
  355    t2 = t3 + rt;
  356    t1 = t2 + rt;
  357 
  358    if (inspwave1->length != 3 || inspwave2->length != 3 || modefreqs->length != nmodes) {
  359        XLAL_ERROR(XLAL_EBADLEN);
  360    }
  361 
  362    /* Solving the linear system for QNMs amplitude coefficients using gsl routine */
  363    /* Initiate matrices and supporting variables */
  364    XLAL_CALLGSL(coef = (gsl_matrix *) gsl_matrix_alloc(2 * nmodes, 2 * nmodes));
  365    XLAL_CALLGSL(hderivs = (gsl_vector *) gsl_vector_alloc(2 * nmodes));
  366    XLAL_CALLGSL(x = (gsl_vector *) gsl_vector_alloc(2 * nmodes));
  367    XLAL_CALLGSL(p = (gsl_permutation *) gsl_permutation_alloc(2 * nmodes));
  368 
  369    /* Check all matrices and variables were allocated */
  370    if (!coef || !hderivs || !x || !p) {
  371        if (coef)
  372            gsl_matrix_free(coef);
  373        if (hderivs)
  374            gsl_vector_free(hderivs);
  375        if (x)
  376            gsl_vector_free(x);
  377        if (p)
  378            gsl_permutation_free(p);
  379 
  380        XLAL_ERROR(XLAL_ENOMEM);
  381    }
  382 
  383    /* Define the linear system Ax=y */
  384    /* Matrix A (2*n by 2*n) has block symmetry. Define half of A here as "coef" */
  385    /* The half of A defined here corresponds to matrices M1 and -M2 in the DCC document T1100433 */
  386    /* Define y here as "hderivs" */
  387    for (i = 0; i < nmodes; ++i) {
  388        gsl_matrix_set(coef, 0, i, 1);
  389        gsl_matrix_set(coef, 1, i, -cimag(modefreqs->data[i]));
  390        gsl_matrix_set(coef, 2, i, exp(-cimag(modefreqs->data[i]) * t1) * cos(creal(modefreqs->data[i]) * t1));
  391        gsl_matrix_set(coef, 3, i, exp(-cimag(modefreqs->data[i]) * t2) * cos(creal(modefreqs->data[i]) * t2));
  392        gsl_matrix_set(coef, 4, i, exp(-cimag(modefreqs->data[i]) * t3) * cos(creal(modefreqs->data[i]) * t3));
  393        gsl_matrix_set(coef, 5, i, exp(-cimag(modefreqs->data[i]) * t4) * cos(creal(modefreqs->data[i]) * t4));
  394        gsl_matrix_set(coef, 6, i, exp(-cimag(modefreqs->data[i]) * t5) * cos(creal(modefreqs->data[i]) * t5));
  395        gsl_matrix_set(coef, 7, i, exp(-cimag(modefreqs->data[i]) * t5) * (-cimag(modefreqs->data[i]) * cos(creal(modefreqs->data[i]) * t5)
  396                - creal(modefreqs->data[i]) * sin(creal(modefreqs->data[i]) * t5)));
  397        gsl_matrix_set(coef, 8, i, 0);
  398        gsl_matrix_set(coef, 9, i, -creal(modefreqs->data[i]));
  399        gsl_matrix_set(coef, 10, i, -exp(-cimag(modefreqs->data[i]) * t1) * sin(creal(modefreqs->data[i]) * t1));
  400        gsl_matrix_set(coef, 11, i, -exp(-cimag(modefreqs->data[i]) * t2) * sin(creal(modefreqs->data[i]) * t2));
  401        gsl_matrix_set(coef, 12, i, -exp(-cimag(modefreqs->data[i]) * t3) * sin(creal(modefreqs->data[i]) * t3));
  402        gsl_matrix_set(coef, 13, i, -exp(-cimag(modefreqs->data[i]) * t4) * sin(creal(modefreqs->data[i]) * t4));
  403        gsl_matrix_set(coef, 14, i, -exp(-cimag(modefreqs->data[i]) * t5) * sin(creal(modefreqs->data[i]) * t5));
  404        gsl_matrix_set(coef, 15, i, exp(-cimag(modefreqs->data[i]) * t5) * (cimag(modefreqs->data[i]) * sin(creal(modefreqs->data[i]) * t5)
  405                - creal(modefreqs->data[i]) * cos(creal(modefreqs->data[i]) * t5)));
  406    }
  407    for (i = 0; i < 2; ++i) {
  408        gsl_vector_set(hderivs, i, inspwave1->data[(i + 1) * inspwave1->vectorLength - 1]);
  409        gsl_vector_set(hderivs, i + nmodes, inspwave2->data[(i + 1) * inspwave2->vectorLength - 1]);
  410        gsl_vector_set(hderivs, i + 6, inspwave1->data[i * inspwave1->vectorLength]);
  411        gsl_vector_set(hderivs, i + 6 + nmodes, inspwave2->data[i * inspwave2->vectorLength]);
  412    }
  413    gsl_vector_set(hderivs, 2, inspwave1->data[4]);
  414    gsl_vector_set(hderivs, 2 + nmodes, inspwave2->data[4]);
  415    gsl_vector_set(hderivs, 3, inspwave1->data[3]);
  416    gsl_vector_set(hderivs, 3 + nmodes, inspwave2->data[3]);
  417    gsl_vector_set(hderivs, 4, inspwave1->data[2]);
  418    gsl_vector_set(hderivs, 4 + nmodes, inspwave2->data[2]);
  419    gsl_vector_set(hderivs, 5, inspwave1->data[1]);
  420    gsl_vector_set(hderivs, 5 + nmodes, inspwave2->data[1]);
  421 
  422    /* Complete the definition for the rest half of A */
  423    for (i = 0; i < nmodes; ++i) {
  424        for (k = 0; k < nmodes; ++k) {
  425            gsl_matrix_set(coef, i, k + nmodes, -gsl_matrix_get(coef, i + nmodes, k));
  426            gsl_matrix_set(coef, i + nmodes, k + nmodes, gsl_matrix_get(coef, i, k));
  427        }
  428    }
  429 
  430#if 0
  431    /* print ringdown-matching linear system: coefficient matrix and RHS vector */
  432    printf("\nRingdown matching matrix:\n");
  433    for (i = 0; i < 16; ++i) {
  434        for (j = 0; j < 16; ++j) {
  435            printf("%.12e ", gsl_matrix_get(coef, i, j));
  436        }
  437        printf("\n");
  438    }
  439    printf("RHS:  ");
  440    for (i = 0; i < 16; ++i) {
  441        printf("%.12e   ", gsl_vector_get(hderivs, i));
  442    }
  443    printf("\n");
  444#endif
  445 
  446    /* Call gsl LU decomposition to solve the linear system */
  447    XLAL_CALLGSL(gslStatus = gsl_linalg_LU_decomp(coef, p, &s));
  448    if (gslStatus == GSL_SUCCESS) {
  449        XLAL_CALLGSL(gslStatus = gsl_linalg_LU_solve(coef, p, hderivs, x));
  450    }
  451    if (gslStatus != GSL_SUCCESS) {
  452        gsl_matrix_free(coef);
  453        gsl_vector_free(hderivs);
  454        gsl_vector_free(x);
  455        gsl_permutation_free(p);
  456        XLAL_ERROR(XLAL_EFUNC);
  457    }
  458 
  459    /* Putting solution to an XLAL vector */
  460    modeamps = XLALCreateREAL8Vector(2 * nmodes);
  461 
  462    if (!modeamps) {
  463        gsl_matrix_free(coef);
  464        gsl_vector_free(hderivs);
  465        gsl_vector_free(x);
  466        gsl_permutation_free(p);
  467        XLAL_ERROR(XLAL_ENOMEM);
  468    }
  469 
  470    for (i = 0; i < nmodes; ++i) {
  471        modeamps->data[i] = gsl_vector_get(x, i);
  472        modeamps->data[i + nmodes] = gsl_vector_get(x, i + nmodes);
  473    }
  474 
  475    /* Free all gsl linear algebra objects */
  476    gsl_matrix_free(coef);
  477    gsl_vector_free(hderivs);
  478    gsl_vector_free(x);
  479    gsl_permutation_free(p);
  480 
  481    /* Build ring-down waveforms */
  482 
  483    REAL8 timeOffset = fmod(matchrange->data[1], dt / m) * dt;
  484 
  485    for (j = 0; j < rdwave1->length; ++j) {
  486        tj = j * dt - timeOffset;
  487        rdwave1->data[j] = 0;
  488        rdwave2->data[j] = 0;
  489        for (i = 0; i < nmodes; ++i) {
  490            rdwave1->data[j] += exp(-tj * cimag(modefreqs->data[i]))
  491                * (modeamps->data[i] * cos(tj * creal(modefreqs->data[i]))
  492                + modeamps->data[i + nmodes] * sin(tj * creal(modefreqs->data[i])));
  493            rdwave2->data[j] += exp(-tj * cimag(modefreqs->data[i]))
  494                * (-modeamps->data[i] * sin(tj * creal(modefreqs->data[i]))
  495                + modeamps->data[i + nmodes] * cos(tj * creal(modefreqs->data[i])));
  496        }
  497    }
  498 
  499    XLALDestroyREAL8Vector(modeamps);
  500    return errcode;
  501}
  502 
  503/**
  504 * Function which calculates the value of the waveform, plus its
  505 * first and second derivatives, for the points which will be required
  506 * in the hybrid comb attachment of the ringdown.
  507 */
  508static INT4 XLALGenerateHybridWaveDerivatives(REAL8Vector * rwave,
  509                                     /**<< OUTPUT, values of the waveform at comb points */
  510    REAL8Vector * dwave,             /**<< OUTPUT, 1st deriv of the waveform at comb points */
  511    REAL8Vector * ddwave,            /**<< OUTPUT, 2nd deriv of the waveform at comb points */
  512    REAL8Vector * timeVec,           /**<< Vector containing the time */
  513    REAL8Vector * wave,              /**<< Last part of inspiral waveform */
  514    REAL8Vector * matchrange,        /**<< Times which determine the size of the comb */
  515    REAL8 dt,                        /**<< Sample time step */
  516    REAL8 mass1,                     /**<< First component mass (in Solar masses) */
  517    REAL8 mass2                      /**<< Second component mass (in Solar masses) */
  518    )
  519{
  520 
  521    /* XLAL error handling */
  522    INT4 errcode = XLAL_SUCCESS;
  523 
  524    /* For checking GSL return codes */
  525    INT4 gslStatus;
  526 
  527    UINT4 j;
  528    UINT4 vecLength;
  529    REAL8 m;
  530    double *y;
  531    double ry, dy, dy2;
  532    double rt;
  533    double *tlist;
  534    gsl_interp_accel *acc;
  535    gsl_spline *spline;
  536 
  537    /* Total mass in geometric units */
  538    m = (mass1 + mass2) * LAL_MTSUN_SI;
  539 
  540    tlist = (double *)LALMalloc(6 * sizeof(double));
  541    rt = (matchrange->data[1] - matchrange->data[0]) / 5.;
  542    tlist[0] = matchrange->data[0];
  543    tlist[1] = tlist[0] + rt;
  544    tlist[2] = tlist[1] + rt;
  545    tlist[3] = tlist[2] + rt;
  546    tlist[4] = tlist[3] + rt;
  547    tlist[5] = matchrange->data[1];
  548 
  549    /* Set the length of the interpolation vectors */
  550    vecLength = (m * matchrange->data[2] / dt) + 1;
  551 
  552    /* Getting interpolation and derivatives of the waveform using gsl spline routine */
  553    /* Initiate arrays and supporting variables for gsl */
  554    y = (double *)LALMalloc(vecLength * sizeof(double));
  555 
  556    if (!y) {
  557        XLAL_ERROR(XLAL_ENOMEM);
  558    }
  559 
  560    for (j = 0; j < vecLength; ++j) {
  561        y[j] = wave->data[j];
  562    }
  563 
  564    XLAL_CALLGSL(acc = (gsl_interp_accel *) gsl_interp_accel_alloc());
  565    XLAL_CALLGSL(spline = (gsl_spline *) gsl_spline_alloc(gsl_interp_cspline, vecLength));
  566    if (!acc || !spline) {
  567        if (acc)
  568            gsl_interp_accel_free(acc);
  569        if (spline)
  570            gsl_spline_free(spline);
  571        LALFree(y);
  572        XLAL_ERROR(XLAL_ENOMEM);
  573    }
  574 
  575    /* Gall gsl spline interpolation */
  576    gslStatus = gsl_spline_init(spline, timeVec->data, y, vecLength);
  577    if (gslStatus != GSL_SUCCESS) {
  578        gsl_spline_free(spline);
  579        gsl_interp_accel_free(acc);
  580        LALFree(y);
  581        XLAL_ERROR(XLAL_EFUNC);
  582    }
  583 
  584    /* Getting first and second order time derivatives from gsl interpolations */
  585    for (j = 0; j < 6; ++j) {
  586        gslStatus = gsl_spline_eval_e(spline, tlist[j], acc, &ry);
  587        if (gslStatus == GSL_SUCCESS) {
  588            gslStatus = gsl_spline_eval_deriv_e(spline, tlist[j], acc, &dy);
  589            gslStatus = gsl_spline_eval_deriv2_e(spline, tlist[j], acc, &dy2);
  590        }
  591        if (gslStatus != GSL_SUCCESS) {
  592            gsl_spline_free(spline);
  593            gsl_interp_accel_free(acc);
  594            LALFree(y);
  595            XLAL_ERROR(XLAL_EFUNC);
  596        }
  597        rwave->data[j] = (REAL8) (ry);
  598        dwave->data[j] = (REAL8) (dy / m);
  599        ddwave->data[j] = (REAL8) (dy2 / m / m);
  600 
  601    }
  602 
  603    /* Free gsl variables */
  604    gsl_spline_free(spline);
  605    gsl_interp_accel_free(acc);
  606    LALFree(tlist);
  607    LALFree(y);
  608 
  609    return errcode;
  610}
  611 
  612/**
  613 * The main workhorse function for performing the ringdown attachment for EOB
  614 * models EOBNRv2 and SEOBNRv1. This is the function which gets called by the
  615 * code generating the full IMR waveform once generation of the inspiral part
  616 * has been completed.
  617 * The ringdown is attached using the hybrid comb matching detailed in
  618 * The method is describe in Sec. II C of Pan et al. PRD 84, 124052 (2011),
  619 * specifically Eqs. 30 - 32.. Further details of the
  620 * implementation of the found in the DCC document T1100433.
  621 * In SEOBNRv1, the last physical overtone is replace by a pseudoQNM. See
  622 * Taracchini et al. PRD 86, 024011 (2012) for details.
  623 * STEP 1) Get mass and spin of the final black hole and the complex ringdown frequencies
  624 * STEP 2) Based on least-damped-mode decay time, allocate memory for rigndown waveform
  625 * STEP 3) Get values and derivatives of inspiral waveforms at matching comb points
  626 * STEP 4) Solve QNM coefficients and generate ringdown waveforms
  627 * STEP 5) Stitch inspiral and ringdown waveoforms
  628 */
  629//static INT4 XLALSimIMREOBHybridAttachRingdown(
  630static UNUSED INT4 XLALSimIMREOBHybridAttachRingdown(REAL8Vector * signal1,
  631                           /**<< OUTPUT, Real of inspiral waveform to which we attach ringdown */
  632    REAL8Vector * signal2, /**<< OUTPUT, Imag of inspiral waveform to which we attach ringdown */
  633    const INT4 l,          /**<< Current mode l */
  634    const INT4 m,          /**<< Current mode m */
  635    const REAL8 dt,        /**<< Sample time step (in seconds) */
  636    const REAL8 mass1,     /**<< First component mass (in Solar masses) */
  637    const REAL8 mass2,     /**<< Second component mass (in Solar masses) */
  638    const REAL8 spin1x,    /**<<The spin of the first object; only needed for spin waveforms */
  639    const REAL8 spin1y,    /**<<The spin of the first object; only needed for spin waveforms */
  640    const REAL8 spin1z,    /**<<The spin of the first object; only needed for spin waveforms */
  641    const REAL8 spin2x,    /**<<The spin of the second object; only needed for spin waveforms */
  642    const REAL8 spin2y,    /**<<The spin of the second object; only needed for spin waveforms */
  643    const REAL8 spin2z,    /**<<The spin of the second object; only needed for spin waveforms */
  644    REAL8Vector * timeVec, /**<< Vector containing the time values */
  645    REAL8Vector * matchrange,
  646                           /**<< Time values chosen as points for performing comb matching */
  647    Approximant approximant/**<<The waveform approximant being used */
  648    ) {
  649 
  650    COMPLEX16Vector *modefreqs;
  651    //COMPLEX16       freq7sav;
  652    UINT4 Nrdwave;
  653    UINT4 j;
  654 
  655    UINT4 nmodes;
  656    REAL8Vector *rdwave1;
  657    REAL8Vector *rdwave2;
  658    REAL8Vector *rinspwave;
  659    REAL8Vector *dinspwave;
  660    REAL8Vector *ddinspwave;
  661    REAL8VectorSequence *inspwaves1;
  662    REAL8VectorSequence *inspwaves2;
  663    REAL8 eta, a, chi, NRPeakOmega22;   /* To generate pQNM frequency */
  664    REAL8 sh, kk, kt1, kt2;     /* To generate pQNM frequency */
  665    REAL8 mTot; /* In geometric units */
  666    REAL8 spin1[3] = { spin1x, spin1y, spin1z };
  667    REAL8 spin2[3] = { spin2x, spin2y, spin2z };
  668    REAL8 finalMass, finalSpin;
  669 
  670    mTot = (mass1 + mass2) * LAL_MTSUN_SI;
  671    eta = mass1 * mass2 / ((mass1 + mass2) * (mass1 + mass2));
  672 
  673    /*
  674     * STEP 1) Get mass and spin of the final black hole and the complex ringdown frequencies
  675     */
  676 
  677    /* Create memory for the QNM frequencies */
  678    nmodes = 8;
  679    modefreqs = XLALCreateCOMPLEX16Vector(nmodes);
  680    if (!modefreqs) {
  681        XLAL_ERROR(XLAL_ENOMEM);
  682    }
  683 
  684    if (XLALSimIMREOBGenerateQNMFreqV2(modefreqs, mass1, mass2, spin1, spin2, l, m, nmodes, approximant) == XLAL_FAILURE) {
  685        XLALDestroyCOMPLEX16Vector(modefreqs);
  686        XLAL_ERROR(XLAL_EFUNC);
  687    }
  688    //UINT4 i;
  689    //for (i=0; i<nmodes; i++){
  690    //    printf("Stas mode %d: %f + i %f \n", i, creal(modefreqs->data[i]), cimag(modefreqs->data[i]));
  691    //}
  692 
  693    /* Call XLALSimIMREOBFinalMassSpin() to get mass and spin of the final black hole */
  694    if (XLALSimIMREOBFinalMassSpin(&finalMass, &finalSpin, mass1, mass2, spin1, spin2, approximant) == XLAL_FAILURE) {
  695        XLAL_ERROR(XLAL_EFUNC);
  696    }
  697 
  698    if (approximant == SEOBNRv1) {
  699        /* Replace the last QNM with pQNM */
  700        /* We assume aligned/antialigned spins here */
  701        a = (spin1[2] + spin2[2]) / 2. * (1.0 - 2.0 * eta) + (spin1[2] - spin2[2]) / 2. * (mass1 - mass2) / (mass1 + mass2);
  702        NRPeakOmega22 = XLALSimIMREOBGetNRSpinPeakOmega(l, m, eta, a) / mTot;
  703        /*printf("a and NRomega in QNM freq: %.16e %.16e %.16e %.16e %.16e\n",spin1[2],spin2[2],
  704         * mTot/LAL_MTSUN_SI,a,NRPeakOmega22*mTot); */
  705        modefreqs->data[7] = (NRPeakOmega22 / finalMass + creal(modefreqs->data[0])) / 2.;
  706        modefreqs->data[7] += I * 10. / 3. * cimag(modefreqs->data[0]);
  707    }
  708 
  709    if (approximant == SEOBNRv2)        //See pages 6 to 12 of the dcc document T1400476-v3 for expressions in this block.
  710    {
  711        /* Replace the last two QNMs with pQNMs */
  712        /* We assume aligned/antialigned spins here */
  713        /* Definitions of a, chi and NRPeakOmega22, where the last one is an approximation of \phi'[tmatch] in T1400476-v3. */
  714        a = (spin1[2] + spin2[2]) / 2. * (1.0 - 2.0 * eta) + (spin1[2] - spin2[2]) / 2. * (mass1 - mass2) / (mass1 + mass2);
  715        NRPeakOmega22 = XLALSimIMREOBGetNRSpinPeakOmegav2(l, m, eta, a) / mTot;
  716 
  717        /* Define chi */
  718        chi = (spin1[2] + spin2[2]) / 2. + (spin1[2] - spin2[2]) / 2. * ((mass1 - mass2) / (mass1 + mass2)) / (1. - 2. * eta);
  719 
  720        /* For extreme chi (>= 0.8), there are scale factors in both complex
  721         * pseudo-QNM frequencies. kk, kt1, kt2 describe those factors. */
  722        // Below definitions of kk, kt1 and kt2 are likely obsolete
  723        kk = kt1 = kt2 = 1.;
  724        if (chi >= 0.8) {
  725            kk = 0.7 + 0.3 * exp(100. * (eta - 0.25));
  726            kt1 = 0.5 * sqrt(1. + 800.0 * eta * eta / 3.0) - 0.125;
  727            kt2 = 0.5 * pow(1. + 0.5 * eta * sqrt(eta) / 0.0225, 2. / 3.) - 0.2;
  728        }
  729        // Above definitions of kk, kt1 and kt2 are likely obsolete
  730        /*printf("a, chi and NRomega in QNM freq: %.16e %.16e %.16e %.16e %.16e %.16e\n",
  731         * spin1[2],spin2[2],mTot/LAL_MTSUN_SI,a,chi,NRPeakOmega22*mTot); */
  732        sh = 0.;
  733        //freq7sav = modefreqs->data[7];
  734 
  735        /* Cases 1, 2 and 3 in T1400476-v3. Note that the difference between the
  736         * chi1=chi2=0 case and the chi<0.7 cases is only in Dtcomb,
  737         * which is not specified or used in this file.
  738         */
  739        modefreqs->data[7] = (2. / 3. * NRPeakOmega22 / finalMass) + (1. / 3. * creal(modefreqs->data[0]));
  740        modefreqs->data[7] += I * 3.5 / 0.9 * cimag(modefreqs->data[0]);
  741        modefreqs->data[6] = (3. / 4. * NRPeakOmega22 / finalMass) + (1. / 4. * creal(modefreqs->data[0]));
  742        modefreqs->data[6] += I * 3.5 * cimag(modefreqs->data[0]);
  743 
  744        /* For extreme chi (>= 0.8), the ringdown attachment should end
  745         * slightly before the value given passed to this function. sh
  746         * gives exactly how long before. */
  747        if (chi >= 0.7 && chi < 0.8) {
  748            sh = -9. * (eta - 0.25);
  749        }
  750        if ((eta > 30. / 31. / 31. && eta <= 10. / 121. && chi >= 0.8) || (eta <= 30. / 31. / 31. && chi >= 0.8 && chi < 0.9)) {        // This is case 4 in T1400476-v3
  751            sh = -9. * (eta - 0.25) * (1. + 2. * exp(-(chi - 0.85) * (chi - 0.85) / 0.05 / 0.05)) * (1. + 1. / (1. + exp((eta - 0.01) / 0.001)));
  752            kk = 0.7 + 0.3 * exp(100. * (eta - 0.25));
  753            kt1 = 0.5 * sqrt(1. + 800.0 * eta * eta / 3.0) - 0.125;
  754            kt2 = 0.5 * pow(1. + 0.5 * eta * sqrt(eta) / 0.0225, 2. / 3.) - 0.2;
  755            modefreqs->data[4] = 0.4 * (1. + kk) * creal(modefreqs->data[6])
  756                + I * cimag(modefreqs->data[6]) / (2.5 * kt2 * exp(-(eta - 0.005) / 0.03));
  757            modefreqs->data[5] = 0.4 * (1. + kk) * creal(modefreqs->data[7])
  758                + I * cimag(modefreqs->data[7]) / (1.5 * kt1 * exp(-(eta - 0.005) / 0.03));
  759            modefreqs->data[6] = kk * creal(modefreqs->data[6]) + I * cimag(modefreqs->data[6]) / kt2;
  760            modefreqs->data[7] = kk * creal(modefreqs->data[7]) + I * cimag(modefreqs->data[7]) / kt1;
  761        }
  762        if (eta < 30. / 31. / 31. && chi >= 0.9) {      // This is case 5 in T1400476-v3
  763            sh = 0.55 - 9. * (eta - 0.25) * (1. + 2. * exp(-(chi - 0.85) * (chi - 0.85) / 0.05 / 0.05)) * (1. + 1. / (1. + exp((eta - 0.01) / 0.001)));
  764            kk = 0.7 + 0.3 * exp(100. * (eta - 0.25));
  765            kt1 = 0.5 * sqrt(1. + 800.0 * eta * eta / 3.0) - 0.125;
  766            kt2 = 0.5 * pow(1. + 0.5 * eta * sqrt(eta) / 0.0225, 2. / 3.) - 0.2;
  767            modefreqs->data[4] = 1.1 * 0.4 * (1. + kk) * creal(modefreqs->data[6])
  768                + I * cimag(modefreqs->data[6]) / (1.05 * 2.5 * kt2 * exp(-(eta - 0.005) / 0.03));
  769            modefreqs->data[5] = 0.4 * (1. + kk) * creal(modefreqs->data[7])
  770                + I * cimag(modefreqs->data[7]) / (1.05 * 1.5 * kt1 * exp(-(eta - 0.005) / 0.03));
  771            modefreqs->data[6] = kk * creal(modefreqs->data[6]) + I * cimag(modefreqs->data[6]) / kt2;
  772            modefreqs->data[7] = kk * creal(modefreqs->data[7]) + I * cimag(modefreqs->data[7]) / kt1;
  773        }
  774        if (eta > 10. / 121. && chi >= 0.8) {   // This is case 6 in T1400476-v3
  775            sh = 1. - 9. * (eta - 0.25) * (1. + 2. * exp(-(chi - 0.85) * (chi - 0.85) / 0.05 / 0.05)) * (1. + 1. / (1. + exp((eta - 0.01) / 0.001)));
  776            kk = 0.7 + 0.3 * exp(100. * (eta - 0.25));
  777            kt1 = 0.45 * sqrt(1. + 200.0 * eta * eta / 3.0) - 0.125;
  778            kt2 = 0.5 * pow(1. + 0.5 * eta * sqrt(eta) / 0.0225, 2. / 3.) - 0.2;
  779            modefreqs->data[6] = kk * creal(modefreqs->data[6]) + I * cimag(modefreqs->data[6]) / 0.95 / kt2;
  780            modefreqs->data[7] = kk * creal(modefreqs->data[7]) + I * cimag(modefreqs->data[7]) / kt1;
  781        }
  782        // The last line of T1400476-v3
  783        matchrange->data[0] -= sh;
  784        matchrange->data[1] -= sh;
  785/*
  786modefreqs->data[7] = 0.38068371/mTot + I/1.4677128/mTot;
  787modefreqs->data[6] = 0.37007703/mTot + I/1.3359367/mTot;
  788modefreqs->data[5] = 0.36980703/mTot + I/1.7791212/mTot;
  789modefreqs->data[4] = 0.3595034/mTot + I/2.6989764/mTot;
  790printf("sh = %f\n",sh);
  791printf("PeakOmega = %f, mTot = %f\n",NRPeakOmega22,mTot);
  792printf("w0 = %f, t0 = %f\n",creal(modefreqs->data[0])*mTot, 1./cimag(modefreqs->data[0])/mTot);
  793printf("w1 = %f, t1 = %f\n",creal(modefreqs->data[6])*mTot, 1./cimag(modefreqs->data[6])/mTot);
  794printf("w2 = %f, t2 = %f\n",creal(modefreqs->data[7])*mTot, 1./cimag(modefreqs->data[7])/mTot);
  795printf("w3 = %f, t3 = %f\n",creal(modefreqs->data[4])*mTot, 1./cimag(modefreqs->data[4])/mTot);
  796printf("w4 = %f, t4 = %f\n",creal(modefreqs->data[5])*mTot, 1./cimag(modefreqs->data[5])/mTot);
  797*/
  798    }
  799    // Move ringdown comb boundaries to sampling points to avoid numerical artifacts.
  800    matchrange->data[0] -= fmod(matchrange->data[0], dt / mTot);
  801    matchrange->data[1] -= fmod(matchrange->data[1], dt / mTot);
  802    /*for (j = 0; j < nmodes; j++)
  803     * {
  804     * printf("QNM frequencies: %d %d %d %f %f\n",l,m,j,creal(modefreqs->data[j])*mTot,1./cimag(modefreqs->data[j])/mTot);
  805     * } */
  806 
  807    /* Ringdown signal length: 10 times the decay time of the n=0 mode */
  808    Nrdwave = (INT4) (EOB_RD_EFOLDS / cimag(modefreqs->data[0]) / dt);
  809 
  810    /* Check the value of attpos, to prevent memory access problems later */
  811    if (matchrange->data[0] * mTot / dt < 5 || matchrange->data[1] * mTot / dt > matchrange->data[2] * mTot / dt - 2) {
  812        XLALPrintError("More inspiral points needed for ringdown matching.\n");
  813        printf("%.16e,%.16e,%.16e\n", matchrange->data[0] * mTot / dt, matchrange->data[1] * mTot / dt, matchrange->data[2] * mTot / dt - 2);
  814        XLALDestroyCOMPLEX16Vector(modefreqs);
  815        XLAL_ERROR(XLAL_EFAILED);
  816    }
  817 
  818    /*
  819     * STEP 2) Based on least-damped-mode decay time, allocate memory for rigndown waveform
  820     */
  821 
  822    /* Create memory for the ring-down and full waveforms, and derivatives of inspirals */
  823 
  824    rdwave1 = XLALCreateREAL8Vector(Nrdwave);
  825    rdwave2 = XLALCreateREAL8Vector(Nrdwave);
  826    rinspwave = XLALCreateREAL8Vector(6);
  827    dinspwave = XLALCreateREAL8Vector(6);
  828    ddinspwave = XLALCreateREAL8Vector(6);
  829    inspwaves1 = XLALCreateREAL8VectorSequence(3, 6);
  830    inspwaves2 = XLALCreateREAL8VectorSequence(3, 6);
  831 
  832    /* Check memory was allocated */
  833    if (!rdwave1 || !rdwave2 || !rinspwave || !dinspwave || !ddinspwave || !inspwaves1 || !inspwaves2) {
  834        XLALDestroyCOMPLEX16Vector(modefreqs);
  835        if (rdwave1)
  836            XLALDestroyREAL8Vector(rdwave1);
  837        if (rdwave2)
  838            XLALDestroyREAL8Vector(rdwave2);
  839        if (rinspwave)
  840            XLALDestroyREAL8Vector(rinspwave);
  841        if (dinspwave)
  842            XLALDestroyREAL8Vector(dinspwave);
  843        if (ddinspwave)
  844            XLALDestroyREAL8Vector(ddinspwave);
  845        if (inspwaves1)
  846            XLALDestroyREAL8VectorSequence(inspwaves1);
  847        if (inspwaves2)
  848            XLALDestroyREAL8VectorSequence(inspwaves2);
  849        XLAL_ERROR(XLAL_ENOMEM);
  850    }
  851 
  852    memset(rdwave1->data, 0, rdwave1->length * sizeof(REAL8));
  853    memset(rdwave2->data, 0, rdwave2->length * sizeof(REAL8));
  854 
  855    /*
  856     * STEP 3) Get values and derivatives of inspiral waveforms at matching comb points
  857     */
  858 
  859    /* Generate derivatives of the last part of inspiral waves */
  860    /* Get derivatives of signal1 */
  861    if (XLALGenerateHybridWaveDerivatives(rinspwave, dinspwave, ddinspwave, timeVec, signal1, matchrange, dt, mass1, mass2) == XLAL_FAILURE) {
  862        XLALDestroyCOMPLEX16Vector(modefreqs);
  863        XLALDestroyREAL8Vector(rdwave1);
  864        XLALDestroyREAL8Vector(rdwave2);
  865        XLALDestroyREAL8Vector(rinspwave);
  866        XLALDestroyREAL8Vector(dinspwave);
  867        XLALDestroyREAL8Vector(ddinspwave);
  868        XLALDestroyREAL8VectorSequence(inspwaves1);
  869        XLALDestroyREAL8VectorSequence(inspwaves2);
  870        XLAL_ERROR(XLAL_EFUNC);
  871    }
  872    for (j = 0; j < 6; j++) {
  873        inspwaves1->data[j] = rinspwave->data[j];
  874        inspwaves1->data[j + 6] = dinspwave->data[j];
  875        inspwaves1->data[j + 12] = ddinspwave->data[j];
  876    }
  877 
  878    /* Get derivatives of signal2 */
  879    if (XLALGenerateHybridWaveDerivatives(rinspwave, dinspwave, ddinspwave, timeVec, signal2, matchrange, dt, mass1, mass2) == XLAL_FAILURE) {
  880        XLALDestroyCOMPLEX16Vector(modefreqs);
  881        XLALDestroyREAL8Vector(rdwave1);
  882        XLALDestroyREAL8Vector(rdwave2);
  883        XLALDestroyREAL8Vector(rinspwave);
  884        XLALDestroyREAL8Vector(dinspwave);
  885        XLALDestroyREAL8Vector(ddinspwave);
  886        XLALDestroyREAL8VectorSequence(inspwaves1);
  887        XLALDestroyREAL8VectorSequence(inspwaves2);
  888        XLAL_ERROR(XLAL_EFUNC);
  889    }
  890    for (j = 0; j < 6; j++) {
  891        inspwaves2->data[j] = rinspwave->data[j];
  892        inspwaves2->data[j + 6] = dinspwave->data[j];
  893        inspwaves2->data[j + 12] = ddinspwave->data[j];
  894    }
  895 
  896    /*
  897     * STEP 4) Solve QNM coefficients and generate ringdown waveforms
  898     */
  899 
  900    /* Generate ring-down waveforms */
  901    if (XLALSimIMREOBHybridRingdownWave(rdwave1, rdwave2, dt, mass1, mass2, inspwaves1, inspwaves2, modefreqs, matchrange) == XLAL_FAILURE) {
  902        XLALDestroyCOMPLEX16Vector(modefreqs);
  903        XLALDestroyREAL8Vector(rdwave1);
  904        XLALDestroyREAL8Vector(rdwave2);
  905        XLALDestroyREAL8Vector(rinspwave);
  906        XLALDestroyREAL8Vector(dinspwave);
  907        XLALDestroyREAL8Vector(ddinspwave);
  908        XLALDestroyREAL8VectorSequence(inspwaves1);
  909        XLALDestroyREAL8VectorSequence(inspwaves2);
  910        XLAL_ERROR(XLAL_EFUNC);
  911    }
  912 
  913    /*
  914     * STEP 5) Stitch inspiral and ringdown waveoforms
  915     */
  916 
  917    /* Generate full waveforms, by stitching inspiral and ring-down waveforms */
  918    //UINT4 attachIdx = matchrange->data[1] * mTot / dt;
  919    UINT4 attachIdx = round(matchrange->data[1] * mTot / dt);
  920    for (j = 1; j < Nrdwave; ++j) {
  921        signal1->data[j + attachIdx] = rdwave1->data[j];
  922        signal2->data[j + attachIdx] = rdwave2->data[j];
  923    }
  924 
  925    memset(signal1->data + Nrdwave + attachIdx, 0, (signal1->length - Nrdwave - attachIdx) * sizeof(REAL8));
  926    memset(signal2->data + Nrdwave + attachIdx, 0, (signal2->length - Nrdwave - attachIdx) * sizeof(REAL8));
  927 
  928    /* Free memory */
  929    XLALDestroyCOMPLEX16Vector(modefreqs);
  930    XLALDestroyREAL8Vector(rdwave1);
  931    XLALDestroyREAL8Vector(rdwave2);
  932    XLALDestroyREAL8Vector(rinspwave);
  933    XLALDestroyREAL8Vector(dinspwave);
  934    XLALDestroyREAL8Vector(ddinspwave);
  935    XLALDestroyREAL8VectorSequence(inspwaves1);
  936    XLALDestroyREAL8VectorSequence(inspwaves2);
  937 
  938    return XLAL_SUCCESS;
  939}
  940 
  941/* Search for index at which t = tofAmax */
  942//RC: this function is not actually looking for the max, but it's looking for the index at which t corresponds to tofAmax which
  943//is fed as an input. For the model SEOBNRv4 this tofAmax is the peak of the amplitude
  944// of the 22 mode. For the model SEOBNRv4HM tofAmax is the maximum of the amplitude of the 22 mode with the exception of the
  945// the 55 mode for which this function is finding the index of tpeak22 -10M, which I
  946//feed as input as tofAmax.
  947static INT4 XLALSimFindIndexMaxAmpli( UINT4 * indAmax, REAL8Vector * timeVec, REAL8Vector * ampWave, REAL8 * valAmax, REAL8 tofAmax ) {
  948    if ( indAmax == NULL || timeVec == NULL || ampWave == NULL || valAmax == NULL ) {
  949        return XLAL_FAILURE;
  950    }
  951    INT4 debugSB = 0;
  952    *indAmax = 0;
  953    INT4 found = 0;
  954    for (UINT4 i = 0; i < timeVec->length - 1; i++) {
  955        if (timeVec->data[i] == tofAmax) {
  956            found = 1;
  957            *indAmax = i;
  958            *valAmax = ampWave->data[i];
  959        }
  960    }
  961    if (found == 0) {
  962        return XLAL_FAILURE;
  963    }
  964    else {
  965        if (debugSB) {
  966            printf(" found maximum times: %f,   %f \n", timeVec->data[*indAmax], tofAmax );
  967        }
  968        return XLAL_SUCCESS;
  969    }
  970}
  971 
  972/**
  973 * The main  function for performing the ringdown attachment for SEOBNRv4 (and beyond)
  974 * This is the function which gets called by the code generating the full IMR waveform once
  975 * generation of the inspiral part has been completed.
  976 * The ringdown is attached by factoring the less damped harmonics and apply tanh fit to the rest.
  977 * STEP 1) Get mass and spin of the final black hole and the complex ringdown frequencies
  978 * STEP 2) Apply the fit function from the attachment time
  979 * STEP 3) Construct the full RD by applying (factor) of less damped 220 mode
  980 * STEP 4) Constructing the RD stitched to the inspiral-merger
  981 * See Section 5.2 of https://dcc.ligo.org/T1600383
  982 */
  983static UNUSED INT4 XLALSimIMREOBAttachFitRingdown(
  984    REAL8Vector * signal1, /**<< OUTPUT, Real of inspiral waveform to which we attach ringdown */
  985    REAL8Vector * signal2, /**<< OUTPUT, Imag of inspiral waveform to which we attach ringdown */
  986    const INT4 l,          /**<< Current mode l */
  987    const INT4 m,          /**<< Current mode m */
  988    const REAL8 dt,        /**<< Sample time step (in seconds) */
  989    const REAL8 mass1,     /**<< First component mass (in Solar masses) */
  990    const REAL8 mass2,     /**<< Second component mass (in Solar masses) */
  991    const REAL8 spin1x,    /**<<The spin of the first object;  */
  992    const REAL8 spin1y,    /**<<The spin of the first object;  */
  993    const REAL8 spin1z,    /**<<The spin of the first object;  */
  994    const REAL8 spin2x,    /**<<The spin of the second object; */
  995    const REAL8 spin2y,    /**<<The spin of the second object; */
  996    const REAL8 spin2z,    /**<<The spin of the second object; */
  997    const REAL8 domega220,  /**<<Fractional deviation in the frequency of the 220 mode; */
  998    const REAL8 dtau220,           /**<<Fractional deviation in the damping time of the  220 mode; */
  999    const REAL8 domega210,  /**<<Fractional deviation in the frequency of the 210 mode; */
 1000    const REAL8 dtau210,    /**<<Fractional deviation in the damping time of the  210 mode; */
 1001    const REAL8 domega330,  /**<<Fractional deviation in the frequency of the 330 mode; */
 1002    const REAL8 dtau330,    /**<<Fractional deviation in the damping time of the  330 mode; */
 1003    const REAL8 domega440,  /**<<Fractional deviation in the frequency of the 440 mode; */
 1004    const REAL8 dtau440,    /**<<Fractional deviation in the damping time of the  440 mode; */
 1005    const REAL8 domega550,  /**<<Fractional deviation in the frequency of the 550 mode; */
 1006    const REAL8 dtau550,    /**<<Fractional deviation in the damping time of the  550 mode; */
 1007    const UINT2 TGRflag,    /**<< Flag for using the TGR ringdown waveform length */
 1008    REAL8Vector * timeVec, /**<< Vector containing the time values */
 1009    REAL8Vector * matchrange,
 1010                           /**<< Time values chosen as points for performing comb matching */
 1011    Approximant approximant,/**<<The waveform approximant being used */
 1012    UINT4 * indAmpMax  /**<<This is used only for SEOBNRv4HM, it is needed to remember
 1013                        the attaching point of the 22 mode without computing it every time */
 1014    ) {
 1015    if ( mass1 <= 0. || mass2 <= 0.
 1016        || fabs(spin1x) > 1. || fabs(spin1y) > 1. || fabs(spin1z) > 1.
 1017        || fabs(spin2x) > 1. || fabs(spin2y) > 1. || fabs(spin2z) > 1.
 1018        || spin1x*spin1x + spin1y*spin1y + spin1z*spin1z > 1.
 1019        || spin2x*spin2x + spin2y*spin2y + spin2z*spin2z > 1.
 1020        ) {
 1021            return XLAL_FAILURE;
 1022        }
 1023    INT4 debugSB = 0;
 1024    UINT4 i;
 1025    UNUSED INT4 phasecount;
 1026    REAL8Vector *ampWave;
 1027    REAL8Vector *phWave;
 1028    REAL8Vector *rdtime;
 1029    COMPLEX16Vector *modefreqs;
 1030    COMPLEX16Vector *modefreqs22; //RC: we use this variable to compute the damping time of the 22 mode which will be used to set the lenght of the ringdown for all the modes
 1031 
 1032    ampWave = XLALCreateREAL8Vector(signal1->length);
 1033    phWave = XLALCreateREAL8Vector(signal1->length);
 1034 
 1035    REAL8 mtot = mass1 + mass2;
 1036    REAL8 eta = mass1 * mass2 / (mtot * mtot);
 1037 
 1038    /* Here I assume that the spins were properly projected (is precessing) and only spin1z, spin2z
 1039     * are relevant, if not we need to add extra function to define what we call chi1, chi2 */
 1040    REAL8 chi1 = spin1z;
 1041    REAL8 chi2 = spin2z;
 1042    REAL8 spin1[3] = { spin1x, spin1y, spin1z };
 1043    REAL8 spin2[3] = { spin2x, spin2y, spin2z };
 1044 
 1045    Approximant appr;
 1046    appr = approximant;
 1047 
 1048    gsl_spline *spline0 = NULL;
 1049    gsl_interp_accel *acc0 = NULL;
 1050 
 1051 
 1052 
 1053    if (debugSB) {
 1054        printf("RDfit: we use spin1 %f, spin2 %f, and it should be dimensionless [-1,1] \n", chi1, chi2);
 1055        printf("We use approximant = %d \n", appr);
 1056    }
 1057    REAL8 chi = 0.5 * (chi1 + chi2) + 0.5 * (chi1 - chi2) * (mass1 - mass2)/(mass1 + mass2) / (1.0 - 2.0 * eta);
 1058 
 1059 
 1060 
 1061    /*********************************************************************************************/
 1062    /*                                          QNMs of the remnant                                        */
 1063    /*********************************************************************************************/
 1064    /* Getting  QNMs */
 1065    modefreqs = XLALCreateCOMPLEX16Vector(1);
 1066    if (XLALSimIMREOBGenerateQNMFreqV2(modefreqs, mass1, mass2, spin1, spin2, l, m, 1, appr) == XLAL_FAILURE) {
 1067        XLALDestroyCOMPLEX16Vector(modefreqs);
 1068        XLAL_ERROR(XLAL_EFUNC);
 1069    }
 1070 
 1071    if (( l == 2 ) && (m == 2)){
 1072       modefreqs->data[0] = creal(modefreqs->data[0])*(1. + domega220) + I*cimag(modefreqs->data[0])/(1. + dtau220);
 1073    }
 1074    if (( l == 2 ) && ( m == 1)) {
 1075       modefreqs->data[0] = creal(modefreqs->data[0])*(1. + domega210) + I*cimag(modefreqs->data[0])/(1. + dtau210);
 1076    }
 1077    if (( l == 3 ) && ( m == 3)) {
 1078       modefreqs->data[0] = creal(modefreqs->data[0])*(1. + domega330) + I*cimag(modefreqs->data[0])/(1. + dtau330);
 1079    }
 1080    if (( l == 4 ) && ( m == 4)) {
 1081       modefreqs->data[0] = creal(modefreqs->data[0])*(1. + domega440) + I*cimag(modefreqs->data[0])/(1. + dtau440);
 1082    }
 1083    if (( l == 5 ) && ( m == 5)) {
 1084       modefreqs->data[0] = creal(modefreqs->data[0])*(1. + domega550) + I*cimag(modefreqs->data[0])/(1. + dtau550);
 1085    }
 1086 
 1087    //RC: we use this variable to compute the damping time of the 22 mode which will be used to set the lenght of the ringdown for all the modes
 1088    modefreqs22 = XLALCreateCOMPLEX16Vector(1);
 1089    if (XLALSimIMREOBGenerateQNMFreqV2(modefreqs22, mass1, mass2, spin1, spin2, 2, 2, 1, appr) == XLAL_FAILURE) {
 1090        XLALDestroyCOMPLEX16Vector(modefreqs);
 1091        XLAL_ERROR(XLAL_EFUNC);
 1092    }
 1093    /* Least-damped QNM */
 1094    COMPLEX16 sigmalm0;
 1095    sigmalm0 = (-cimag(modefreqs->data[0]) - I * creal(modefreqs->data[0])) * (mtot * LAL_MTSUN_SI);
 1096    // sigmalm0 = -0.08119703120243188 - I*0.5040714995216017;
 1097 
 1098    if (debugSB) {
 1099      printf("Mode %d %d \n",l, m);
 1100        printf("matchpoints are: %.16f,  %.16f,   %.16f, %.16f\n", matchrange->data[0], matchrange->data[1], matchrange->data[2], matchrange->data[3]);
 1101        printf("the 0-overtone is: %.16f + i %.16f \n", creal(sigmalm0), cimag(sigmalm0));
 1102    }
 1103 
 1104 
 1105 
 1106    /*********************************************************************************************/
 1107    /*                                         Prepare inspiral signal                                         */
 1108    /*                   This is needed to guarantee continuity with RD signal               */
 1109    /*********************************************************************************************/
 1110    /*  Compute amplitude and the unwrapped phase of the inspiral */
 1111    phasecount = 0;
 1112    for (i = 0; i < signal1->length; i++) {
 1113        ampWave->data[i] = 0.0;
 1114        phWave->data[i] = 0.0;
 1115    }
 1116    REAL8 prev, now, corph;
 1117    prev = atan2(signal2->data[0], signal1->data[0]);
 1118    phWave->data[0] = prev;
 1119    for (i = 0; i < timeVec->length; i++) {
 1120        ampWave->data[i] = sqrt(signal1->data[i] * signal1->data[i] + signal2->data[i] * signal2->data[i]);
 1121        now = atan2(signal2->data[i], signal1->data[i]);
 1122        if (i > 0) {
 1123            /* Unwrapping */
 1124            corph = now - prev;
 1125            corph = corph > LAL_PI ? corph - LAL_TWOPI : (corph < -LAL_PI ? corph + LAL_TWOPI : corph);
 1126 
 1127            phWave->data[i] = phWave->data[i - 1] + corph;
 1128            prev = now;
 1129        }
 1130        //phWave->data[i] = now;
 1131    }
 1132    FILE *fout = NULL;
 1133    if (debugSB) {
 1134        char filename2[sizeof "CheckStasAmplPhaseXX.dat"];
 1135        sprintf(filename2,"CheckStasAmplPhase%01d%01d.dat",l,m);
 1136        fout = fopen(filename2, "w");
 1137        printf("Check the length: time %d, signal %d \n", timeVec->length, signal1->length);
 1138        for (i = 0; i < timeVec->length; i++) {
 1139            fprintf(fout, "%f   %.16e   %.16e   %.16e   %.16e  \n", timeVec->data[i], ampWave->data[i], phWave->data[i], signal1->data[i], signal2->data[i]);
 1140        }
 1141 
 1142        fclose(fout);
 1143    }
 1144    /* For the modes 22, 33, 21, 44 search for index at which the maximum of the amplitude of the 22 mode occurs */
 1145    /* For the mode 55 search for the index corresponding at the time tpeak22-10M, where tpeak22 is the time of the maximum of the amplitude of the 22 mode*/
 1146    /* See Eq.(4.3) of https://arxiv.org/pdf/1803.10701.pdf */
 1147 
 1148    REAL8 valAmax = ampWave->data[0];
 1149    REAL8 valdAmax = 0;
 1150    REAL8 tofAmax = matchrange->data[1];
 1151    UINT4 indAmax;
 1152    if (l == 5 && m==5) {
 1153      tofAmax = matchrange->data[3];
 1154    }
 1155    //RC we should find indAmax only for the mode 22, for the other one the attaching point is the same, with the exception of the 55
 1156    //For the 55 mode we need to find tpeak22 -10M, which in that case is fed as matchrange->data[3]
 1157    if((l == 2 && m == 2) || (l == 5 && m == 5)){
 1158      if ( XLALSimFindIndexMaxAmpli( &indAmax, timeVec, ampWave, &valAmax, tofAmax ) == XLAL_FAILURE )
 1159      {
 1160          XLALPrintError("Time of maximum amplitude is not found .\n");
 1161          XLALDestroyCOMPLEX16Vector(modefreqs);
 1162          XLAL_ERROR(XLAL_EFUNC);
 1163        }
 1164      if (l==2 && m==2) {
 1165        *indAmpMax = indAmax;
 1166      }
 1167      //RC for the 55 mode we also need to find the derivative at the attachment point, since we are not making the attachment
 1168      //at the peak of the mode where the derivative is zero, see Eq.(4.3) of https://arxiv.org/pdf/1803.10701.pdf */
 1169      if(l == 5 && m == 5){
 1170        spline0 = gsl_spline_alloc (gsl_interp_cspline, timeVec->length);
 1171        acc0 = gsl_interp_accel_alloc ();
 1172        gsl_spline_init (spline0, timeVec->data, ampWave->data, timeVec->length);
 1173        gsl_interp_accel_reset (acc0);
 1174        valdAmax = gsl_spline_eval_deriv (spline0, tofAmax, acc0);
 1175        }
 1176      }
 1177      else{
 1178        indAmax = *indAmpMax;
 1179        valAmax = ampWave->data[indAmax];
 1180        /*For the modes different from 22, this IS NOT the value of the maximum of the amplitude of the mode, but is the value of the amplitude at the peak of the 22 mode*/
 1181        /*For the SEOBNRv4HM model we need to compute also the derivative at the attaching point. This is not zero because we are attaching the HMs not at the paek of the lm mode, but at the peak of the 22 mode*/
 1182        /*See Eqs. (4.22-4.23) of https://arxiv.org/pdf/1803.10701.pdf */
 1183        spline0 = gsl_spline_alloc (gsl_interp_cspline, timeVec->length);
 1184        acc0 = gsl_interp_accel_alloc ();
 1185        gsl_spline_init (spline0, timeVec->data, ampWave->data, timeVec->length);
 1186        gsl_interp_accel_reset (acc0);
 1187        valdAmax = gsl_spline_eval_deriv (spline0, tofAmax, acc0);
 1188        // valAmax = 0.019835031225903733;
 1189        // valdAmax = 0.00020163171965464758;
 1190      }
 1191 
 1192 
 1193    if (debugSB) {
 1194        printf("Check: The maximum of amplitude is %.16e found at t=%f, index = %d (out of %d) \n", valAmax, tofAmax, indAmax, timeVec->length);
 1195        printf("Amp@Attachment = %.16f \n", valAmax);
 1196        printf("dAmp@Attachment = %.16f \n", valdAmax);
 1197        FILE *indMax = NULL;
 1198        char filename2[sizeof "indexMaxXXHi.dat"];
 1199        sprintf(filename2,"indexMax%01d%01dHi.dat",l,m);
 1200        indMax = fopen (filename2, "w");
 1201        fprintf(indMax, "%d \n",indAmax);
 1202        fclose(indMax);
 1203    }
 1204 
 1205 
 1206 
 1207    /*********************************************************************************************/
 1208    /*                  Constant coefficients entering RD fitting formulas                      */
 1209    /*********************************************************************************************/
 1210    /* Computing fit coefficients that enter amplitude and phase of the RD signal */
 1211    /* Numeircal constants are defined at the top of this file */
 1212    /* Eq. (54) of https://dcc.ligo.org/T1600383 for SEOBNRv4 and 22 mode SEOBNRv4HM*/
 1213    /* Eqs. (C1, C3, C5, C7) of https://arxiv.org/pdf/1803.10701.pdf for SEOBNRv4HM*/
 1214 
 1215    REAL8 ampcf1;
 1216    // ampcf1 = A1coeff00[l][m] + A1coeff01[l][m] * chi + A1coeff02[l][m] * chi * chi + A1coeff10[l][m] * eta + A1coeff11[l][m] * eta * chi + A1coeff20[l][m] * eta * eta;
 1217    ampcf1 = XLALCalculateRDAmplitudeCoefficient1(l, m, eta, chi);
 1218    //ampcf1 = 0.08953902308302486;
 1219    if(debugSB){
 1220      printf("ampcf1 = %.16f \n", ampcf1);
 1221    }
 1222 
 1223    /* Eq. (55) of https://dcc.ligo.org/T1600383 for SEOBNRv4 and 22 mode SEOBNRv4HM*/
 1224    /* Eqs. (C2, C4, C6, C8) of https://arxiv.org/pdf/1803.10701.pdf for SEOBNRv4HM*/
 1225    REAL8 ampcf2;
 1226    // ampcf2 = A2coeff00[l][m] + A2coeff01[l][m] * chi + A2coeff10[l][m] * eta + A2coeff11[l][m] * eta * chi + A2coeff20[l][m] * eta * eta + A2coeff21[l][m] * eta * eta * chi;
 1227    ampcf2 = XLALCalculateRDAmplitudeCoefficient2(l, m, eta, chi);
 1228    //ampcf2 =  -0.506368869538912;
 1229    if(debugSB){
 1230      printf("ampcf2 = %.16f \n", ampcf2);
 1231    }
 1232//    printf("creal(sigma220), 2.*ampcf1*tanh(ampcf2) = %.16e %.16e\n",1./creal(sigma220), 2.*ampcf1*tanh(ampcf2));
 1233    /* Eqs. (57)-(58) of https://dcc.ligo.org/T1600383 */
 1234    if( l == 2 && m == 2){
 1235      if (creal(sigmalm0) > 2. * ampcf1 * tanh(ampcf2)) {
 1236          ampcf1 = creal(sigmalm0) / (2. * tanh(ampcf2));
 1237        }
 1238      }
 1239    /* Eq. (62) of https://dcc.ligo.org/T1600383 for SEOBNRv4 and 22 mode SEOBNRv4HM*/
 1240    /* Eqs. (C9, C11, C13, C15) of https://arxiv.org/pdf/1803.10701.pdf for SEOBNRv4HM*/
 1241    REAL8 phasecf1;
 1242    // phasecf1 = P1coeff00[l][m] + P1coeff01[l][m] * chi + P1coeff02[l][m] * chi * chi + P1coeff10[l][m] * eta + P1coeff11[l][m] * eta * chi + P1coeff20[l][m] * eta * eta;
 1243    phasecf1 = XLALCalculateRDPhaseCoefficient1(l, m, eta, chi);
 1244    if(debugSB){
 1245      printf("phasecf1 = %.16f \n", phasecf1);
 1246    }
 1247 
 1248    /* Eq. (63) of https://dcc.ligo.org/T1600383 for SEOBNRv4 and 22 mode SEOBNRv4HM*/
 1249    /* Eqs. (C10, C12, C14, C16) of https://arxiv.org/pdf/1803.10701.pdf for SEOBNRv4HM*/
 1250    REAL8 phasecf2;
 1251    // phasecf2 = P2coeff00[l][m] + P2coeff01[l][m] * chi + P2coeff02[l][m] * chi * chi + P2coeff10[l][m] * eta + P2coeff11[l][m] * eta * chi + P2coeff20[l][m] * eta * eta;
 1252    phasecf2 = XLALCalculateRDPhaseCoefficient2(l, m, eta, chi);
 1253    if(debugSB){
 1254      printf("phasecf2 = %.16f \n", phasecf2);
 1255    }
 1256 
 1257    /*********************************************************************************************/
 1258    /*                                            RD fitting formulas                                           */
 1259    /*********************************************************************************************/
 1260    /* Ringdown signal length: 10 times the decay time of the n=0 mode */
 1261    UINT4 Nrdwave;
 1262 
 1263    if (TGRflag == 0) {
 1264        Nrdwave = (INT4) (EOB_RD_EFOLDS / cimag(modefreqs22->data[0]) / dt);
 1265    } else {
 1266        Nrdwave = (INT4) (EOB_RD_EFOLDS / cimag(modefreqs->data[0]) / dt);
 1267    }
 1268    //printf("Stas Nrdwave %d,  dt = %f", Nrdwave, dt);
 1269    REAL8 dtM = dt / (mtot * LAL_MTSUN_SI);     // go to geometric units
 1270    rdtime = XLALCreateREAL8Vector(Nrdwave);
 1271    for (i = 0; i < Nrdwave; i++) {
 1272            rdtime->data[i] = i * dtM;      // this time for RD and it starts with 0
 1273    }
 1274    REAL8 tcons = 0.;
 1275 
 1276    /* Rescalings to guarantee continuity with inspiral */
 1277    REAL8 Arescaledtcons = valAmax * exp(-creal(sigmalm0) * tcons) / eta;
 1278    REAL8 dtArescaledtcons = (valdAmax - creal(sigmalm0) * valAmax) * exp(-creal(sigmalm0) * tcons) / eta;    // valdAmax = 0 - assumes extermum (max) of peak amplitude //RC: valdAmax = 0 for 22 mode
 1279    /*Eq (4.22) of https://arxiv.org/pdf/1803.10701.pdf*/
 1280    REAL8 ampcc1 = dtArescaledtcons * pow(cosh(ampcf2), 2) / ampcf1;
 1281    /*Eq (4.23) of https://arxiv.org/pdf/1803.10701.pdf*/
 1282    REAL8 ampcc2 = (Arescaledtcons * ampcf1 - dtArescaledtcons * cosh(ampcf2) * sinh(ampcf2)) / ampcf1;
 1283 
 1284 
 1285    REAL8Vector *ampRD;
 1286    REAL8Vector *phRD;
 1287    ampRD = XLALCreateREAL8Vector(Nrdwave);
 1288    phRD = XLALCreateREAL8Vector(Nrdwave);
 1289 
 1290    /* Construct RD amplitude */
 1291    /* Eqs. (48)-(49) of https://dcc.ligo.org/T1600383 */
 1292    for (i = 0; i < Nrdwave; i++) {
 1293        ampRD->data[i] = eta * exp(creal(sigmalm0) * rdtime->data[i]) * (ampcc1 * tanh(ampcf1 * rdtime->data[i] + ampcf2) + ampcc2);
 1294    }
 1295    if (debugSB) {
 1296        char filename[sizeof "StasAmpRD_fullXX.dat"];
 1297        sprintf(filename,"StasAmpRD_full%01d%01d.dat",l,m);
 1298        fout = fopen (filename, "w");
 1299        // for (i = 0; i < indAmax; i++) {
 1300        //     fprintf(fout, "%.16e    %.16e \n", timeVec->data[i], ampWave->data[i]);
 1301        // }
 1302        for (i = 1; i < Nrdwave; i++) {
 1303            fprintf(fout, "%.16e    %.16e \n", rdtime->data[i] + tofAmax*0, ampRD->data[i]);
 1304        }
 1305        fclose(fout);
 1306    }
 1307 
 1308    /* Construct RD phase */
 1309    REAL8 omegarescaledtcons = (phWave->data[indAmax] - phWave->data[indAmax - 1]) / dtM - cimag(sigmalm0);
 1310    // omegarescaledtcons = -0.2354501785436996 - cimag(sigmalm0); 21 mode
 1311    // omegarescaledtcons = -0.6076660197512114 - cimag(sigmalm0); 33 mode
 1312    // omegarescaledtcons = -0.8063013198270685 - cimag(sigmalm0); 44 mode
 1313    // omegarescaledtcons = -0.7813933465833801 - cimag(sigmalm0); 55 mode
 1314    if(debugSB){
 1315      printf("omega0 = %.16f\n", phWave->data[0]);
 1316      printf("omega0fit = %.16f, omega0numder = %.16f \n", XLALSimIMREOBGetNRSpinPeakOmegaV4 (l, m, eta, chi), (phWave->data[indAmax] - phWave->data[indAmax - 1]) / dtM);
 1317    }
 1318    REAL8 phasecc1 = omegarescaledtcons * (phasecf2 + 1.0) / phasecf2 / phasecf1;
 1319    REAL8 phi0 = phWave->data[indAmax];
 1320    // phi0 = -165.37581501842033; 21 mode
 1321    // phi0 = -486.98433862793974; 33 mode
 1322    // phi0 = -651.2335864724689; 44 mode
 1323    // phi0 = -805.2637568966843; 55 mode
 1324    if(debugSB){
 1325      printf("phi_0 = %.16f \n", phi0);
 1326    }
 1327    REAL8 logargnum, logargden;
 1328    /* Eq. (59)-(60) of https://dcc.ligo.org/T1600383 */
 1329    for (i = 0; i < Nrdwave; i++) {
 1330        logargnum = 1. + phasecf2 * exp(-phasecf1 * rdtime->data[i]);
 1331        logargden = 1. + phasecf2;
 1332        phRD->data[i] = phi0 - phasecc1 * log(logargnum / logargden) + cimag(sigmalm0) * rdtime->data[i];
 1333    }
 1334    if (debugSB) {
 1335        char filename[sizeof "StasPhRD_fullXX.dat"];
 1336        sprintf(filename,"StasPhRD_full%01d%01d.dat",l,m);
 1337        fout = fopen (filename, "w");
 1338        // for (i = 0; i < indAmax; i++) {
 1339        //     fprintf(fout, "%.16e    %.16e \n", timeVec->data[i], phWave->data[i]);
 1340        // }
 1341        for (i = 1; i < Nrdwave; i++) {
 1342            fprintf(fout, "%.16e    %.16e \n", rdtime->data[i] + tofAmax*0, phRD->data[i]);
 1343        }
 1344        fclose(fout);
 1345 
 1346        // Compute the frequency of the ful signal
 1347        UINT4 totSz = indAmax + Nrdwave;
 1348        REAL8Vector *PhFull;
 1349        PhFull = XLALCreateREAL8Vector(totSz);
 1350        REAL8Vector *tFull;
 1351        tFull = XLALCreateREAL8Vector(totSz);
 1352        REAL8Vector *frFull;
 1353        frFull = XLALCreateREAL8Vector(totSz);
 1354 
 1355        for (i = 0; i < indAmax; i++) {
 1356            tFull->data[i] = timeVec->data[i];
 1357            PhFull->data[i] = phWave->data[i];
 1358        }
 1359        for (i = 0; i < Nrdwave; i++) {
 1360            tFull->data[i + indAmax] = rdtime->data[i] + tofAmax;
 1361            PhFull->data[i + indAmax] = phRD->data[i];
 1362        }
 1363        fout = fopen("StasPhRD_full2.dat", "w");
 1364        for (i = 0; i < totSz; i++) {
 1365            fprintf(fout, "%.16e   %.16e \n", tFull->data[i], PhFull->data[i]);
 1366        }
 1367        fclose(fout);
 1368 
 1369        gsl_spline *spline = NULL;
 1370        gsl_interp_accel *acc = NULL;
 1371        spline = gsl_spline_alloc(gsl_interp_cspline, totSz);
 1372        acc = gsl_interp_accel_alloc();
 1373        gsl_spline_init(spline, tFull->data, PhFull->data, totSz);
 1374        for (i = 0; i < totSz; i++) {
 1375            frFull->data[i] = gsl_spline_eval_deriv(spline, tFull->data[i], acc);
 1376        }
 1377        fout = fopen("StasFrRD_full.dat", "w");
 1378        for (i = 0; i < totSz; i++) {
 1379            fprintf(fout, "%.16e   %.16e \n", tFull->data[i], frFull->data[i]);
 1380        }
 1381        fclose(fout);
 1382 
 1383        gsl_spline_free(spline);
 1384        gsl_interp_accel_free(acc);
 1385 
 1386        XLALDestroyREAL8Vector(PhFull);
 1387        XLALDestroyREAL8Vector(tFull);
 1388        XLALDestroyREAL8Vector(frFull);
 1389 
 1390    }
 1391 
 1392    /* Construct RD signal */
 1393    for (i = 0; i < Nrdwave; i++) {
 1394        signal1->data[i + indAmax] = ampRD->data[i] * cos(phRD->data[i]);
 1395        signal2->data[i + indAmax] = ampRD->data[i] * sin(phRD->data[i]);
 1396    }
 1397 
 1398    gsl_spline_free (spline0);
 1399    gsl_interp_accel_free (acc0);
 1400 
 1401    XLALDestroyREAL8Vector(ampWave);
 1402    XLALDestroyREAL8Vector(phWave);
 1403    XLALDestroyCOMPLEX16Vector(modefreqs);
 1404    XLALDestroyCOMPLEX16Vector(modefreqs22);
 1405    XLALDestroyREAL8Vector(rdtime);
 1406    XLALDestroyREAL8Vector(ampRD);
 1407    XLALDestroyREAL8Vector(phRD);
 1408 
 1409    return XLAL_SUCCESS;
 1410 
 1411}
 1412 
 1413 
 1414static UNUSED INT4 XLALSimIMREOBTaper(
 1415                                                  REAL8Vector * signal1, /**<< OUTPUT, Real of inspiral waveform to which we attach ringdown */
 1416                                                  REAL8Vector * signal2, /**<< OUTPUT, Imag of inspiral waveform to which we attach ringdown */
 1417                                                  const INT4 l,          /**<< Current mode l */
 1418                                                  const INT4 m,          /**<< Current mode m */
 1419                                                  const REAL8 dt,        /**<< Sample time step (in seconds) */
 1420                                                  const REAL8 mass1,     /**<< First component mass (in Solar masses) */
 1421                                                  const REAL8 mass2,     /**<< Second component mass (in Solar masses) */
 1422                                                  const REAL8 spin1x,    /**<<The spin of the first object;  */
 1423                                                  const REAL8 spin1y,    /**<<The spin of the first object;  */
 1424                                                  const REAL8 spin1z,    /**<<The spin of the first object;  */
 1425                                                  const REAL8 spin2x,    /**<<The spin of the second object; */
 1426                                                  const REAL8 spin2y,    /**<<The spin of the second object; */
 1427                                                  const REAL8 spin2z,    /**<<The spin of the second object; */
 1428                                                  REAL8Vector * timeVec, /**<< Vector containing the time values */
 1429                                                  REAL8Vector * matchrange,
 1430                                                  /**<< Time values chosen as points for performing comb matching */
 1431                                                  Approximant approximant/**<<The waveform approximant being used */
 1432) {
 1433    if ( mass1 <= 0. || mass2 <= 0.
 1434        || fabs(spin1x) > 1. || fabs(spin1y) > 1. || fabs(spin1z) > 1.
 1435        || fabs(spin2x) > 1. || fabs(spin2y) > 1. || fabs(spin2z) > 1.
 1436        || spin1x*spin1x + spin1y*spin1y + spin1z*spin1z > 1.
 1437        || spin2x*spin2x + spin2y*spin2y + spin2z*spin2z > 1.
 1438        ) {
 1439        return XLAL_FAILURE;
 1440    }
 1441    INT4 debugSB = 0;
 1442    UINT4 i;
 1443    UNUSED INT4 phasecount;
 1444    REAL8Vector *ampWave;
 1445    REAL8Vector *phWave;
 1446    REAL8Vector *rdtime;
 1447    COMPLEX16Vector *modefreqs;
 1448 
 1449    ampWave = XLALCreateREAL8Vector(signal1->length);
 1450    phWave = XLALCreateREAL8Vector(signal1->length);
 1451 
 1452    REAL8 mtot = mass1 + mass2;
 1453    REAL8 eta = mass1 * mass2 / (mtot * mtot);
 1454 
 1455    /* Here I assume that the spins were properly projected (is precessing) and only spin1z, spin2z
 1456     * are relevant, if not we need to add extra function to define what we call chi1, chi2 */
 1457    REAL8 chi1 = spin1z;
 1458    REAL8 chi2 = spin2z;
 1459    REAL8 spin1[3] = { spin1x, spin1y, spin1z };
 1460    REAL8 spin2[3] = { spin2x, spin2y, spin2z };
 1461 
 1462    Approximant appr;
 1463    appr = approximant;
 1464 
 1465    if (debugSB) {
 1466        printf("RDfit: we use spin1 %f, spin2 %f, and it should be dimensionless [-1,1] \n", chi1, chi2);
 1467        printf("We use approximant = %d \n", appr);
 1468    }
 1469    REAL8 chi = 0.5 * (chi1 + chi2) + 0.5 * (chi1 - chi2) * (mass1 - mass2)/(mass1 + mass2) / (1.0 - 2.0 * eta);
 1470 
 1471 
 1472 
 1473    /*********************************************************************************************/
 1474    /*                                          QNMs of the remnant                                        */
 1475    /*********************************************************************************************/
 1476    /* Getting  QNMs */
 1477    modefreqs = XLALCreateCOMPLEX16Vector(1);
 1478    if (XLALSimIMREOBGenerateQNMFreqV2(modefreqs, mass1, mass2, spin1, spin2, l, m, 1, appr) == XLAL_FAILURE) {
 1479        XLALDestroyCOMPLEX16Vector(modefreqs);
 1480        XLAL_ERROR(XLAL_EFUNC);
 1481    }
 1482    /* Least-damped QNM */
 1483    COMPLEX16 sigma220;
 1484    //sigma220 = -0.0609 - I*0.8326;
 1485    sigma220 = (-cimag(modefreqs->data[0]) - I * creal(modefreqs->data[0])) * (mtot * LAL_MTSUN_SI);
 1486 
 1487    if (debugSB) {
 1488        printf("matchpoints are: %f,  %f,   %f \n", matchrange->data[0], matchrange->data[1], matchrange->data[2]);
 1489        printf("the 0-overtone is: %f + i %f \n", creal(sigma220), cimag(sigma220));
 1490    }
 1491 
 1492 
 1493 
 1494    /*********************************************************************************************/
 1495    /*                                         Prepare inspiral signal                                         */
 1496    /*                   This is needed to guarantee continuity with RD signal               */
 1497    /*********************************************************************************************/
 1498    /*  Compute amplitude and the unwrapped phase of the inspiral */
 1499    phasecount = 0;
 1500    for (i = 0; i < signal1->length; i++) {
 1501        ampWave->data[i] = 0.0;
 1502        phWave->data[i] = 0.0;
 1503    }
 1504    REAL8 prev, now, corph;
 1505    prev = atan2(signal2->data[0], signal1->data[0]);
 1506    phWave->data[0] = prev;
 1507    for (i = 0; i < timeVec->length; i++) {
 1508        ampWave->data[i] = sqrt(signal1->data[i] * signal1->data[i] + signal2->data[i] * signal2->data[i]);
 1509        now = atan2(signal2->data[i], signal1->data[i]);
 1510        if (i > 0) {
 1511            /* Unwrapping */
 1512            corph = now - prev;
 1513            corph = corph > LAL_PI ? corph - LAL_TWOPI : (corph < -LAL_PI ? corph + LAL_TWOPI : corph);
 1514 
 1515            phWave->data[i] = phWave->data[i - 1] + corph;
 1516            prev = now;
 1517        }
 1518        //phWave->data[i] = now;
 1519    }
 1520    FILE *fout = NULL;
 1521    if (debugSB) {
 1522        fout = fopen("CheckStasAmplPhase.dat", "w");
 1523        printf("Check the length: time %d, signal %d \n", timeVec->length, signal1->length);
 1524        for (i = 0; i < timeVec->length; i++) {
 1525            fprintf(fout, "%f   %.16e   %.16e   %.16e   %.16e  \n", timeVec->data[i], ampWave->data[i], phWave->data[i], signal1->data[i], signal2->data[i]);
 1526        }
 1527 
 1528        fclose(fout);
 1529    }
 1530 
 1531    /* For the modes 22, 33, 21, 44 search for index at which the maximum of the amplitude of the 22 mode occurs */
 1532    /* For the mode 55 search for the index corresponding at the time tpeak22-10M, where tpeak22 is the time of the maximum of the amplitude of the 22 mode*/
 1533    REAL8 valAmax;
 1534    REAL8 tofAmax = matchrange->data[1];
 1535    UINT4 indAmax;
 1536    if ( tofAmax != timeVec->data[timeVec->length-1] ) {
 1537    if ( XLALSimFindIndexMaxAmpli( &indAmax, timeVec, ampWave, &valAmax, tofAmax ) == XLAL_FAILURE )
 1538    {
 1539        XLALPrintError("Time of maximum amplitude is not found .\n");
 1540        XLALDestroyCOMPLEX16Vector(modefreqs);
 1541        XLAL_ERROR(XLAL_EFUNC);
 1542    }
 1543    }
 1544    else {
 1545        indAmax = timeVec->length-1;
 1546        valAmax = ampWave->data[indAmax];
 1547    }
 1548    if (debugSB) {
 1549        printf("Check: The maximum of amplitude is %.16e found at t=%f, index = %d (out of %d) \n", valAmax, tofAmax, indAmax, timeVec->length);
 1550    }
 1551 
 1552 
 1553    /*********************************************************************************************/
 1554    /*                  Constant coefficients entering RD fitting formulas                      */
 1555    /*********************************************************************************************/
 1556    /* Computing fit coefficients that enter amplitude and phase of the RD signal */
 1557    /* Numeircal constants are defined at the top of this file */
 1558    /* Eq. (28) of https://dcc.ligo.org/T1600383 for SEOBNRv4*/
 1559    /* Eqs. (C1, C3, C5, C7) of https://arxiv.org/pdf/1803.10701.pdf for SEOBNRv4HM*/
 1560    REAL8 ampcf1;
 1561    // ampcf1 = A1coeff00 + A1coeff01 * chi + A1coeff02 * chi * chi + A1coeff10 * eta + A1coeff11 * eta * chi + A1coeff20 * eta * eta;
 1562    ampcf1 = XLALCalculateRDAmplitudeCoefficient1(l, m, eta, chi);
 1563 
 1564    /* Eq. (29) of https://dcc.ligo.org/T1600383 */
 1565    /* Eqs. (C2, C4, C6, C8) of https://arxiv.org/pdf/1803.10701.pdf for SEOBNRv4HM*/
 1566    REAL8 ampcf2;
 1567    // ampcf2 = A2coeff00 + A2coeff01 * chi + A2coeff10 * eta + A2coeff11 * eta * chi + A2coeff20 * eta * eta + A2coeff21 * eta * eta * chi;
 1568    ampcf2 = XLALCalculateRDAmplitudeCoefficient2(l, m, eta, chi);
 1569 
 1570    //    printf("creal(sigma220), 2.*ampcf1*tanh(ampcf2) = %.16e %.16e\n",1./creal(sigma220), 2.*ampcf1*tanh(ampcf2));
 1571    /* Eqs. (31)-(32) of https://dcc.ligo.org/T1600383 */
 1572    if (creal(sigma220) > 2. * ampcf1 * tanh(ampcf2)) {
 1573        ampcf1 = creal(sigma220) / (2. * tanh(ampcf2));
 1574    }
 1575 
 1576    /* Eq. (36) of https://dcc.ligo.org/T1600383 */
 1577    REAL8 phasecf1;
 1578    // phasecf1 = P1coeff00 + P1coeff01 * chi + P1coeff02 * chi * chi + P1coeff10 * eta + P1coeff11 * eta * chi + P1coeff20 * eta * eta;
 1579    phasecf1 = XLALCalculateRDPhaseCoefficient1(l, m, eta, chi);
 1580 
 1581    /* Eq. (37) of https://dcc.ligo.org/T1600383 */
 1582    REAL8 phasecf2;
 1583    // phasecf2 = P2coeff00 + P2coeff01 * chi + P2coeff02 * chi * chi + P2coeff10 * eta + P2coeff11 * eta * chi + P2coeff20 * eta * eta;
 1584    phasecf2 = XLALCalculateRDPhaseCoefficient2(l, m, eta, chi);
 1585 
 1586 
 1587 
 1588    /*********************************************************************************************/
 1589    /*                                            RD fitting formulas                                           */
 1590    /*********************************************************************************************/
 1591    /* Ringdown signal length: 10 times the decay time of the n=0 mode */
 1592    UINT4 Nrdwave = (INT4) (EOB_RD_EFOLDS / cimag(modefreqs->data[0]) / dt);
 1593    //printf("Stas Nrdwave %d,  dt = %f", Nrdwave, dt);
 1594    REAL8 dtM = dt / (mtot * LAL_MTSUN_SI);     // go to geometric units
 1595    rdtime = XLALCreateREAL8Vector(Nrdwave);
 1596    for (i = 0; i < Nrdwave; i++) {
 1597        rdtime->data[i] = i * dtM;      // this time for RD and it starts with 0
 1598    }
 1599    REAL8 tcons = 0.;   //attachment point relative to peak; possibility for non zero values not fully implemented
 1600 
 1601    /* Rescalings to guarantee continuity with inspiral */
 1602    REAL8 Arescaledtcons = valAmax * exp(-creal(sigma220) * tcons) / eta;
 1603    REAL8 dtArescaledtcons = (0. - creal(sigma220) * valAmax) * exp(-creal(sigma220) * tcons) / eta;    // 0 - assumes extermum (max) of peak amplitude
 1604    REAL8 ampcc1 = dtArescaledtcons * pow(cosh(ampcf2), 2) / ampcf1;
 1605    REAL8 ampcc2 = (Arescaledtcons * ampcf1 - dtArescaledtcons * cosh(ampcf2) * sinh(ampcf2)) / ampcf1;
 1606 
 1607    REAL8Vector *ampRD;
 1608    REAL8Vector *phRD;
 1609    ampRD = XLALCreateREAL8Vector(Nrdwave);
 1610    phRD = XLALCreateREAL8Vector(Nrdwave);
 1611 
 1612    /* Construct RD amplitude */
 1613    /* Eqs. (22)-(23) of https://dcc.ligo.org/T1600383 */
 1614//    REAL8 dpar = 0.1;
 1615    for (i = 0; i < Nrdwave; i++) {
 1616        ampRD->data[i] = eta * exp(creal(sigma220) * rdtime->data[i]) * (ampcc1 * tanh(ampcf1 * rdtime->data[i] + ampcf2) + ampcc2);
 1617//        ampRD->data[i] = valAmax/dpar * exp(creal(sigma220) * rdtime->data[i]) * (dpar + tanh(dpar*creal(sigma220) * rdtime->data[i]));
 1618 
 1619    }
 1620    if (debugSB) {
 1621        fout = fopen("StasAmpRD_full.dat", "w");
 1622        for (i = 0; i < indAmax; i++) {
 1623            fprintf(fout, "%.16e    %.16e \n", timeVec->data[i], ampWave->data[i]);
 1624        }
 1625        for (i = 0; i < Nrdwave; i++) {
 1626            fprintf(fout, "%.16e    %.16e \n", rdtime->data[i] + tofAmax, ampRD->data[i]);
 1627        }
 1628        fclose(fout);
 1629    }
 1630 
 1631    /* Construct RD phase */
 1632    REAL8 omegarescaledtcons = (phWave->data[indAmax] - phWave->data[indAmax - 1]) / dtM - cimag(sigma220);
 1633    REAL8 phasecc1 = omegarescaledtcons * (phasecf2 + 1.0) / phasecf2 / phasecf1;
 1634    REAL8 phi0 = phWave->data[indAmax];
 1635    REAL8 logargnum, logargden;
 1636    /* Eq. (33)-(34) of https://dcc.ligo.org/T1600383 */
 1637    for (i = 0; i < Nrdwave; i++) {
 1638        logargnum = 1. + phasecf2 * exp(-phasecf1 * rdtime->data[i]);
 1639        logargden = 1. + phasecf2;
 1640        phRD->data[i] = phi0 - phasecc1 * log(logargnum / logargden) + cimag(sigma220) * rdtime->data[i];
 1641        phRD->data[i] = phi0 + ((phWave->data[indAmax] - phWave->data[indAmax - 1]) / dtM) * rdtime->data[i];
 1642    }
 1643 
 1644    if (debugSB) {
 1645        fout = fopen("StasPhRD_full.dat", "w");
 1646        for (i = 0; i < indAmax; i++) {
 1647            fprintf(fout, "%.16e    %.16e \n", timeVec->data[i], phWave->data[i]);
 1648        }
 1649        for (i = 0; i < Nrdwave; i++) {
 1650            fprintf(fout, "%.16e    %.16e \n", rdtime->data[i] + tofAmax, phRD->data[i]);
 1651        }
 1652        fclose(fout);
 1653 
 1654        // Compute the frequency of the ful signal
 1655        UINT4 totSz = indAmax + Nrdwave;
 1656        REAL8Vector *PhFull;
 1657        PhFull = XLALCreateREAL8Vector(totSz);
 1658        REAL8Vector *tFull;
 1659        tFull = XLALCreateREAL8Vector(totSz);
 1660        REAL8Vector *frFull;
 1661        frFull = XLALCreateREAL8Vector(totSz);
 1662 
 1663        for (i = 0; i < indAmax; i++) {
 1664            tFull->data[i] = timeVec->data[i];
 1665            PhFull->data[i] = phWave->data[i];
 1666        }
 1667        for (i = 0; i < Nrdwave; i++) {
 1668            tFull->data[i + indAmax] = rdtime->data[i] + tofAmax;
 1669            PhFull->data[i + indAmax] = phRD->data[i];
 1670        }
 1671        fout = fopen("StasPhRD_full2.dat", "w");
 1672        for (i = 0; i < totSz; i++) {
 1673            fprintf(fout, "%.16e   %.16e \n", tFull->data[i], PhFull->data[i]);
 1674        }
 1675        fclose(fout);
 1676 
 1677        gsl_spline *spline = NULL;
 1678        gsl_interp_accel *acc = NULL;
 1679        spline = gsl_spline_alloc(gsl_interp_cspline, totSz);
 1680        acc = gsl_interp_accel_alloc();
 1681        gsl_spline_init(spline, tFull->data, PhFull->data, totSz);
 1682        for (i = 0; i < totSz; i++) {
 1683            frFull->data[i] = gsl_spline_eval_deriv(spline, tFull->data[i], acc);
 1684        }
 1685        fout = fopen("StasFrRD_full.dat", "w");
 1686        for (i = 0; i < totSz; i++) {
 1687            fprintf(fout, "%.16e   %.16e \n", tFull->data[i], frFull->data[i]);
 1688        }
 1689        fclose(fout);
 1690 
 1691        gsl_spline_free(spline);
 1692        gsl_interp_accel_free(acc);
 1693 
 1694        XLALDestroyREAL8Vector(PhFull);
 1695        XLALDestroyREAL8Vector(tFull);
 1696        XLALDestroyREAL8Vector(frFull);
 1697 
 1698    }
 1699 
 1700    /* Construct RD signal */
 1701    for (i = 0; i < Nrdwave; i++) {
 1702        signal1->data[i + indAmax] = ampRD->data[i] * cos(phRD->data[i]);
 1703        signal2->data[i + indAmax] = ampRD->data[i] * sin(phRD->data[i]);
 1704    }
 1705 
 1706    XLALDestroyREAL8Vector(ampWave);
 1707    XLALDestroyREAL8Vector(phWave);
 1708    XLALDestroyCOMPLEX16Vector(modefreqs);
 1709    XLALDestroyREAL8Vector(rdtime);
 1710    XLALDestroyREAL8Vector(ampRD);
 1711    XLALDestroyREAL8Vector(phRD);
 1712 
 1713    return XLAL_SUCCESS;
 1714 
 1715}
 1716 
 1717#endif /*_LALSIMIMREOBHYBRIDRINGDOWN_C*/
