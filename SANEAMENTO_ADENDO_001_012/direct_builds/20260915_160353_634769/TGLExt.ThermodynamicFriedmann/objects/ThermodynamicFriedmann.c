// Lean compiler output
// Module: TGLExt.ThermodynamicFriedmann
// Imports: public import Init public meta import Init public import TGLExt.SectorFriedmann public import Mathlib.Analysis.Calculus.MeanValue
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
extern lean_object* lp_mathlib_Real_definition_00___x40_Mathlib_Data_Real_Basic_1279875089____hygCtx___hyg_8_;
lean_object* lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_1138242547____hygCtx___hyg_8_(lean_object*, lean_object*, lean_object*);
lean_object* lp_mathlib_abs___at___00BoundingSieve_errSum_spec__0(lean_object*);
lean_object* lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_4214226450____hygCtx___hyg_8_(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_entropyFactor(lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_entropyFactor(lean_object* v_c_1_, lean_object* v_w_2_){
_start:
{
lean_object* v___x_3_; lean_object* v___f_4_; lean_object* v___x_5_; lean_object* v___f_6_; lean_object* v___f_7_; 
v___x_3_ = lp_mathlib_Real_definition_00___x40_Mathlib_Data_Real_Basic_1279875089____hygCtx___hyg_8_;
v___f_4_ = lean_alloc_closure((void*)(lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_1138242547____hygCtx___hyg_8_), 3, 2);
lean_closure_set(v___f_4_, 0, v___x_3_);
lean_closure_set(v___f_4_, 1, v_w_2_);
v___x_5_ = lp_mathlib_abs___at___00BoundingSieve_errSum_spec__0(v___f_4_);
v___f_6_ = lean_alloc_closure((void*)(lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_4214226450____hygCtx___hyg_8_), 3, 2);
lean_closure_set(v___f_6_, 0, v_c_1_);
lean_closure_set(v___f_6_, 1, v___x_5_);
v___f_7_ = lean_alloc_closure((void*)(lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_1138242547____hygCtx___hyg_8_), 3, 2);
lean_closure_set(v___f_7_, 0, v___x_3_);
lean_closure_set(v___f_7_, 1, v___f_6_);
return v___f_7_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_TGLExt_SectorFriedmann(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Analysis_Calculus_MeanValue(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_TGLExt_ThermodynamicFriedmann(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_TGLExt_SectorFriedmann(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_Analysis_Calculus_MeanValue(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
