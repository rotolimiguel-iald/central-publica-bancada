// Lean compiler output
// Module: TGLExt.V351ScalarImaginaryCoreAction
// Imports: public import Init public meta import Init public import TGLExt.V351ScalarImaginaryLeftTransport public import TGLExt.V350BasePolarStrongLimit public import TGLExt.V350ScalarGNSGeneratorTransport
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
lean_object* initialize_TGLExt_V351ScalarImaginaryLeftTransport(uint8_t builtin);
lean_object* initialize_tgl__kernel_TGLExt_V350BasePolarStrongLimit(uint8_t builtin);
lean_object* initialize_tgl__kernel_TGLExt_V350ScalarGNSGeneratorTransport(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_TGLExt_V351ScalarImaginaryCoreAction(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_TGLExt_V351ScalarImaginaryLeftTransport(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_tgl__kernel_TGLExt_V350BasePolarStrongLimit(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_tgl__kernel_TGLExt_V350ScalarGNSGeneratorTransport(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
