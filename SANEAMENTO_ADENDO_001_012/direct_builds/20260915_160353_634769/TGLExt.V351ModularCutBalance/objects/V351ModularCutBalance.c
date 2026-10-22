// Lean compiler output
// Module: TGLExt.V351ModularCutBalance
// Imports: public import Init public meta import Init public import TGLExt.V351ModularImplementation public import TGLExt.V351SineResolventApprox public import TGLExt.V351AntiunitaryResolventPhase public import TGLExt.V350ScalarGNSNormality public import TGLExt.V350CorePolarInclusion public import TGLExt.V351RegularDomainCut public import TGLExt.PhaseFrequencySeparation public import Mathlib.Analysis.CStarAlgebra.GelfandDuality
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
lean_object* initialize_TGLExt_V351ModularImplementation(uint8_t builtin);
lean_object* initialize_tgl__kernel_TGLExt_V351SineResolventApprox(uint8_t builtin);
lean_object* initialize_TGLExt_V351AntiunitaryResolventPhase(uint8_t builtin);
lean_object* initialize_tgl__kernel_TGLExt_V350ScalarGNSNormality(uint8_t builtin);
lean_object* initialize_tgl__kernel_TGLExt_V350CorePolarInclusion(uint8_t builtin);
lean_object* initialize_tgl__kernel_TGLExt_V351RegularDomainCut(uint8_t builtin);
lean_object* initialize_tgl__kernel_TGLExt_PhaseFrequencySeparation(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Analysis_CStarAlgebra_GelfandDuality(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_TGLExt_V351ModularCutBalance(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_TGLExt_V351ModularImplementation(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_tgl__kernel_TGLExt_V351SineResolventApprox(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_TGLExt_V351AntiunitaryResolventPhase(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_tgl__kernel_TGLExt_V350ScalarGNSNormality(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_tgl__kernel_TGLExt_V350CorePolarInclusion(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_tgl__kernel_TGLExt_V351RegularDomainCut(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_tgl__kernel_TGLExt_PhaseFrequencySeparation(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_Analysis_CStarAlgebra_GelfandDuality(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
