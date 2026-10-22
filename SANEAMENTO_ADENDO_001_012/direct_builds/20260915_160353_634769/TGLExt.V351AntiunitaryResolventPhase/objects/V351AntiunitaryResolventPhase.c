// Lean compiler output
// Module: TGLExt.V351AntiunitaryResolventPhase
// Imports: public import Init public meta import Init public import TGLExt.V350LocalBasePolarCommutation public import TGLExt.V351ResolventImaginaryContinuity public import TGLExt.V350AntiunitaryPositiveConjugation public import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Unique
#include <lean/lean.h>
#if defined(__clang__)
#pragma clang diagnostic ignored "-Wunused-parameter"
#pragma clang diagnostic ignored "-Wunused-label"
#elif defined(__GNUC__) && !defined(__CLANG__)
#pragma GCC diagnostic ignored "-Wunused-parameter"
#pragma GCC diagnostic ignored "-Wunused-label"
#pragma GCC diagnostic ignored "-Wunused-but-set-variable"
#endif
#ifdef __cplusplus
extern "C" {
#endif
lean_object* lp_tgl__kernel_TGLV350_Regular_antiunitaryConjugate___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_TGLV350_Regular_antiunitaryConjugateRealHom___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_TGLV350_Regular_antiunitaryConjugateRealHom(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_TGLV350_Regular_antiunitaryConjugateRealHom___redArg(lean_object* v_inst_1_, lean_object* v_inst_2_, lean_object* v_J_3_){
_start:
{
lean_object* v___x_4_; 
v___x_4_ = lean_alloc_closure((void*)(lp_tgl__kernel_TGLV350_Regular_antiunitaryConjugate___boxed), 5, 4);
lean_closure_set(v___x_4_, 0, lean_box(0));
lean_closure_set(v___x_4_, 1, v_inst_1_);
lean_closure_set(v___x_4_, 2, v_inst_2_);
lean_closure_set(v___x_4_, 3, v_J_3_);
return v___x_4_;
}
}
LEAN_EXPORT lean_object* l_TGLV350_Regular_antiunitaryConjugateRealHom(lean_object* v_H_5_, lean_object* v_inst_6_, lean_object* v_inst_7_, lean_object* v_inst_8_, lean_object* v_J_9_){
_start:
{
lean_object* v___x_10_; 
v___x_10_ = lean_alloc_closure((void*)(lp_tgl__kernel_TGLV350_Regular_antiunitaryConjugate___boxed), 5, 4);
lean_closure_set(v___x_10_, 0, lean_box(0));
lean_closure_set(v___x_10_, 1, v_inst_6_);
lean_closure_set(v___x_10_, 2, v_inst_7_);
lean_closure_set(v___x_10_, 3, v_J_9_);
return v___x_10_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_tgl__kernel_TGLExt_V350LocalBasePolarCommutation(uint8_t builtin);
lean_object* initialize_tgl__kernel_TGLExt_V351ResolventImaginaryContinuity(uint8_t builtin);
lean_object* initialize_tgl__kernel_TGLExt_V350AntiunitaryPositiveConjugation(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Analysis_CStarAlgebra_ContinuousFunctionalCalculus_Unique(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_TGLExt_V351AntiunitaryResolventPhase(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_tgl__kernel_TGLExt_V350LocalBasePolarCommutation(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_tgl__kernel_TGLExt_V351ResolventImaginaryContinuity(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_tgl__kernel_TGLExt_V350AntiunitaryPositiveConjugation(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_Analysis_CStarAlgebra_ContinuousFunctionalCalculus_Unique(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
