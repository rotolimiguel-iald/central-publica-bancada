// Lean compiler output
// Module: TGLExt.AuditA1Orphans
// Imports: public import Init public meta import Init public import TGLExt.V351ResolventImaginaryIntertwining public import TGLExt.V351ScaledResolventFunctions public import TGLExt.V351ScaledResolventCalculus public import TGLExt.V351ImaginaryPowerScaling public import TGLExt.V351ScalarImaginaryRightTransport public import TGLExt.V351AntiunitaryResolventPhase public import TGLExt.V351ScalarTomitaImaginaryConjugation
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
lean_object* initialize_tgl__kernel_TGLExt_V351ResolventImaginaryIntertwining(uint8_t builtin);
lean_object* initialize_tgl__kernel_TGLExt_V351ScaledResolventFunctions(uint8_t builtin);
lean_object* initialize_tgl__kernel_TGLExt_V351ScaledResolventCalculus(uint8_t builtin);
lean_object* initialize_tgl__kernel_TGLExt_V351ImaginaryPowerScaling(uint8_t builtin);
lean_object* initialize_tgl__kernel_TGLExt_V351ScalarImaginaryRightTransport(uint8_t builtin);
lean_object* initialize_TGLExt_V351AntiunitaryResolventPhase(uint8_t builtin);
lean_object* initialize_TGLExt_V351ScalarTomitaImaginaryConjugation(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_TGLExt_AuditA1Orphans(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_tgl__kernel_TGLExt_V351ResolventImaginaryIntertwining(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_tgl__kernel_TGLExt_V351ScaledResolventFunctions(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_tgl__kernel_TGLExt_V351ScaledResolventCalculus(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_tgl__kernel_TGLExt_V351ImaginaryPowerScaling(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_tgl__kernel_TGLExt_V351ScalarImaginaryRightTransport(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_TGLExt_V351AntiunitaryResolventPhase(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_TGLExt_V351ScalarTomitaImaginaryConjugation(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
