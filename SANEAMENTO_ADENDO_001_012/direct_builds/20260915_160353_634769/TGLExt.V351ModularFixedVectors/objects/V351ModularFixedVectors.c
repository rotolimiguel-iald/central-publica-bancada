// Lean compiler output
// Module: TGLExt.V351ModularFixedVectors
// Imports: public import Init public meta import Init public import TGLExt.V351AverageFixedPair public import TGLExt.V351ResolventImaginaryIntertwining public import TGLExt.V351ScalarTomitaImaginaryPowers public import Mathlib.Analysis.InnerProductSpace.LinearMap
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
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_TGLExt_V351AverageFixedPair(uint8_t builtin);
lean_object* initialize_tgl__kernel_TGLExt_V351ResolventImaginaryIntertwining(uint8_t builtin);
lean_object* initialize_tgl__kernel_TGLExt_V351ScalarTomitaImaginaryPowers(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Analysis_InnerProductSpace_LinearMap(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_TGLExt_V351ModularFixedVectors(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_TGLExt_V351AverageFixedPair(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_tgl__kernel_TGLExt_V351ResolventImaginaryIntertwining(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_tgl__kernel_TGLExt_V351ScalarTomitaImaginaryPowers(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_Analysis_InnerProductSpace_LinearMap(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
