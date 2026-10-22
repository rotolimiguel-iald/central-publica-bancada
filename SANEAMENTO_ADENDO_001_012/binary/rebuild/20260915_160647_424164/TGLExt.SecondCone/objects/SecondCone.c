// Lean compiler output
// Module: TGLExt.SecondCone
// Imports: public import Init public meta import Init public import TGLExt.GNSTower
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
lean_object* lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_2451848184____hygCtx___hyg_8_(lean_object*, lean_object*);
lean_object* lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_1138242547____hygCtx___hyg_8_(lean_object*, lean_object*, lean_object*);
lean_object* lean_nat_mod(lean_object*, lean_object*);
extern lean_object* lp_mathlib_Real_definition_00___x40_Mathlib_Data_Real_Basic_1850581184____hygCtx___hyg_8_;
uint8_t lean_nat_dec_eq(lean_object*, lean_object*);
lean_object* lp_tgl__kernel_TGLExt_epsTT(lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* lp_tgl__kernel_TGLExt_lightWave(lean_object*, lean_object*);
lean_object* lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_4214226450____hygCtx___hyg_8_(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_tgl__kernel_TGLExt_lightCone2___lam__0(lean_object*, lean_object*, lean_object*);
static lean_once_cell_t lp_tgl__kernel_TGLExt_lightCone2___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_tgl__kernel_TGLExt_lightCone2___closed__0;
static lean_once_cell_t lp_tgl__kernel_TGLExt_lightCone2___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_tgl__kernel_TGLExt_lightCone2___closed__1;
static lean_once_cell_t lp_tgl__kernel_TGLExt_lightCone2___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_tgl__kernel_TGLExt_lightCone2___closed__2;
LEAN_EXPORT lean_object* lp_tgl__kernel_TGLExt_lightCone2;
LEAN_EXPORT lean_object* lp_tgl__kernel_TGLExt_lightWave2(lean_object*, lean_object*);
static lean_once_cell_t lp_tgl__kernel_TGLExt_epsTT2___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_tgl__kernel_TGLExt_epsTT2___closed__0;
static lean_once_cell_t lp_tgl__kernel_TGLExt_epsTT2___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_tgl__kernel_TGLExt_epsTT2___closed__1;
LEAN_EXPORT lean_object* lp_tgl__kernel_TGLExt_epsTT2(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_tgl__kernel_TGLExt_epsTT2___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_tgl__kernel_TGLExt_ttWave2(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_tgl__kernel_TGLExt_ttWave2___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_tgl__kernel_TGLExt_ttCross(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_tgl__kernel_TGLExt_ttCross___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_tgl__kernel_TGLExt_lightCone2___lam__0(lean_object* v___x_1_, lean_object* v___x_2_, lean_object* v___y_3_){
_start:
{
lean_object* v___x_4_; lean_object* v___x_5_; lean_object* v___f_6_; lean_object* v___f_7_; 
lean_inc(v___y_3_);
v___x_4_ = lean_apply_1(v___y_3_, v___x_1_);
v___x_5_ = lean_apply_1(v___y_3_, v___x_2_);
v___f_6_ = lean_alloc_closure((void*)(lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_2451848184____hygCtx___hyg_8_), 2, 1);
lean_closure_set(v___f_6_, 0, v___x_5_);
v___f_7_ = lean_alloc_closure((void*)(lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_1138242547____hygCtx___hyg_8_), 3, 2);
lean_closure_set(v___f_7_, 0, v___x_4_);
lean_closure_set(v___f_7_, 1, v___f_6_);
return v___f_7_;
}
}
static lean_object* _init_lp_tgl__kernel_TGLExt_lightCone2___closed__0(void){
_start:
{
lean_object* v___x_8_; lean_object* v___x_9_; lean_object* v___x_10_; 
v___x_8_ = lean_unsigned_to_nat(4u);
v___x_9_ = lean_unsigned_to_nat(2u);
v___x_10_ = lean_nat_mod(v___x_9_, v___x_8_);
return v___x_10_;
}
}
static lean_object* _init_lp_tgl__kernel_TGLExt_lightCone2___closed__1(void){
_start:
{
lean_object* v___x_11_; lean_object* v___x_12_; lean_object* v___x_13_; 
v___x_11_ = lean_unsigned_to_nat(4u);
v___x_12_ = lean_unsigned_to_nat(0u);
v___x_13_ = lean_nat_mod(v___x_12_, v___x_11_);
return v___x_13_;
}
}
static lean_object* _init_lp_tgl__kernel_TGLExt_lightCone2___closed__2(void){
_start:
{
lean_object* v___x_14_; lean_object* v___x_15_; lean_object* v___f_16_; 
v___x_14_ = lean_obj_once(&lp_tgl__kernel_TGLExt_lightCone2___closed__1, &lp_tgl__kernel_TGLExt_lightCone2___closed__1_once, _init_lp_tgl__kernel_TGLExt_lightCone2___closed__1);
v___x_15_ = lean_obj_once(&lp_tgl__kernel_TGLExt_lightCone2___closed__0, &lp_tgl__kernel_TGLExt_lightCone2___closed__0_once, _init_lp_tgl__kernel_TGLExt_lightCone2___closed__0);
v___f_16_ = lean_alloc_closure((void*)(lp_tgl__kernel_TGLExt_lightCone2___lam__0), 3, 2);
lean_closure_set(v___f_16_, 0, v___x_15_);
lean_closure_set(v___f_16_, 1, v___x_14_);
return v___f_16_;
}
}
static lean_object* _init_lp_tgl__kernel_TGLExt_lightCone2(void){
_start:
{
lean_object* v___f_17_; 
v___f_17_ = lean_obj_once(&lp_tgl__kernel_TGLExt_lightCone2___closed__2, &lp_tgl__kernel_TGLExt_lightCone2___closed__2_once, _init_lp_tgl__kernel_TGLExt_lightCone2___closed__2);
return v___f_17_;
}
}
LEAN_EXPORT lean_object* lp_tgl__kernel_TGLExt_lightWave2(lean_object* v_w_18_, lean_object* v_x_19_){
_start:
{
lean_object* v___x_34__overap_20_; lean_object* v___x_21_; lean_object* v___x_22_; 
v___x_34__overap_20_ = lp_tgl__kernel_TGLExt_lightCone2;
v___x_21_ = lean_apply_1(v___x_34__overap_20_, v_x_19_);
v___x_22_ = lean_apply_1(v_w_18_, v___x_21_);
return v___x_22_;
}
}
static lean_object* _init_lp_tgl__kernel_TGLExt_epsTT2___closed__0(void){
_start:
{
lean_object* v___x_23_; lean_object* v___x_24_; lean_object* v___x_25_; 
v___x_23_ = lean_unsigned_to_nat(4u);
v___x_24_ = lean_unsigned_to_nat(1u);
v___x_25_ = lean_nat_mod(v___x_24_, v___x_23_);
return v___x_25_;
}
}
static lean_object* _init_lp_tgl__kernel_TGLExt_epsTT2___closed__1(void){
_start:
{
lean_object* v___x_26_; lean_object* v___x_27_; lean_object* v___x_28_; 
v___x_26_ = lean_unsigned_to_nat(4u);
v___x_27_ = lean_unsigned_to_nat(3u);
v___x_28_ = lean_nat_mod(v___x_27_, v___x_26_);
return v___x_28_;
}
}
LEAN_EXPORT lean_object* lp_tgl__kernel_TGLExt_epsTT2(lean_object* v_a_29_, lean_object* v_b_30_, lean_object* v_00_u03bc_31_, lean_object* v_00_u03bd_32_){
_start:
{
lean_object* v___x_33_; uint8_t v___y_35_; uint8_t v___x_39_; uint8_t v___y_41_; lean_object* v___y_42_; 
v___x_33_ = lean_obj_once(&lp_tgl__kernel_TGLExt_epsTT2___closed__0, &lp_tgl__kernel_TGLExt_epsTT2___closed__0_once, _init_lp_tgl__kernel_TGLExt_epsTT2___closed__0);
v___x_39_ = lean_nat_dec_eq(v_00_u03bc_31_, v___x_33_);
if (v___x_39_ == 0)
{
goto v___jp_44_;
}
else
{
uint8_t v___x_49_; 
v___x_49_ = lean_nat_dec_eq(v_00_u03bd_32_, v___x_33_);
if (v___x_49_ == 0)
{
goto v___jp_44_;
}
else
{
return v_a_29_;
}
}
v___jp_34_:
{
if (v___y_35_ == 0)
{
lean_object* v___x_36_; 
v___x_36_ = lp_mathlib_Real_definition_00___x40_Mathlib_Data_Real_Basic_1850581184____hygCtx___hyg_8_;
return v___x_36_;
}
else
{
uint8_t v___x_37_; 
v___x_37_ = lean_nat_dec_eq(v_00_u03bd_32_, v___x_33_);
if (v___x_37_ == 0)
{
lean_object* v___x_38_; 
v___x_38_ = lp_mathlib_Real_definition_00___x40_Mathlib_Data_Real_Basic_1850581184____hygCtx___hyg_8_;
return v___x_38_;
}
else
{
lean_inc(v_b_30_);
return v_b_30_;
}
}
}
v___jp_40_:
{
if (v___x_39_ == 0)
{
v___y_35_ = v___y_41_;
goto v___jp_34_;
}
else
{
uint8_t v___x_43_; 
v___x_43_ = lean_nat_dec_eq(v_00_u03bd_32_, v___y_42_);
if (v___x_43_ == 0)
{
v___y_35_ = v___y_41_;
goto v___jp_34_;
}
else
{
lean_inc(v_b_30_);
return v_b_30_;
}
}
}
v___jp_44_:
{
lean_object* v___x_45_; uint8_t v___x_46_; 
v___x_45_ = lean_obj_once(&lp_tgl__kernel_TGLExt_epsTT2___closed__1, &lp_tgl__kernel_TGLExt_epsTT2___closed__1_once, _init_lp_tgl__kernel_TGLExt_epsTT2___closed__1);
v___x_46_ = lean_nat_dec_eq(v_00_u03bc_31_, v___x_45_);
if (v___x_46_ == 0)
{
lean_dec(v_a_29_);
v___y_41_ = v___x_46_;
v___y_42_ = v___x_45_;
goto v___jp_40_;
}
else
{
uint8_t v___x_47_; 
v___x_47_ = lean_nat_dec_eq(v_00_u03bd_32_, v___x_45_);
if (v___x_47_ == 0)
{
lean_dec(v_a_29_);
v___y_41_ = v___x_46_;
v___y_42_ = v___x_45_;
goto v___jp_40_;
}
else
{
lean_object* v___f_48_; 
v___f_48_ = lean_alloc_closure((void*)(lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_2451848184____hygCtx___hyg_8_), 2, 1);
lean_closure_set(v___f_48_, 0, v_a_29_);
return v___f_48_;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_tgl__kernel_TGLExt_epsTT2___boxed(lean_object* v_a_50_, lean_object* v_b_51_, lean_object* v_00_u03bc_52_, lean_object* v_00_u03bd_53_){
_start:
{
lean_object* v_res_54_; 
v_res_54_ = lp_tgl__kernel_TGLExt_epsTT2(v_a_50_, v_b_51_, v_00_u03bc_52_, v_00_u03bd_53_);
lean_dec(v_00_u03bd_53_);
lean_dec(v_00_u03bc_52_);
lean_dec(v_b_51_);
return v_res_54_;
}
}
LEAN_EXPORT lean_object* lp_tgl__kernel_TGLExt_ttWave2(lean_object* v_a_55_, lean_object* v_b_56_, lean_object* v_v_57_, lean_object* v_00_u03bc_58_, lean_object* v_00_u03bd_59_, lean_object* v_x_60_){
_start:
{
lean_object* v___x_61_; lean_object* v___x_62_; lean_object* v___f_63_; 
v___x_61_ = lp_tgl__kernel_TGLExt_epsTT2(v_a_55_, v_b_56_, v_00_u03bc_58_, v_00_u03bd_59_);
v___x_62_ = lp_tgl__kernel_TGLExt_lightWave2(v_v_57_, v_x_60_);
v___f_63_ = lean_alloc_closure((void*)(lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_4214226450____hygCtx___hyg_8_), 3, 2);
lean_closure_set(v___f_63_, 0, v___x_61_);
lean_closure_set(v___f_63_, 1, v___x_62_);
return v___f_63_;
}
}
LEAN_EXPORT lean_object* lp_tgl__kernel_TGLExt_ttWave2___boxed(lean_object* v_a_64_, lean_object* v_b_65_, lean_object* v_v_66_, lean_object* v_00_u03bc_67_, lean_object* v_00_u03bd_68_, lean_object* v_x_69_){
_start:
{
lean_object* v_res_70_; 
v_res_70_ = lp_tgl__kernel_TGLExt_ttWave2(v_a_64_, v_b_65_, v_v_66_, v_00_u03bc_67_, v_00_u03bd_68_, v_x_69_);
lean_dec(v_00_u03bd_68_);
lean_dec(v_00_u03bc_67_);
lean_dec(v_b_65_);
return v_res_70_;
}
}
LEAN_EXPORT lean_object* lp_tgl__kernel_TGLExt_ttCross(lean_object* v_a_71_, lean_object* v_b_72_, lean_object* v_a_x27_73_, lean_object* v_b_x27_74_, lean_object* v_w_75_, lean_object* v_v_76_, lean_object* v_00_u03bc_77_, lean_object* v_00_u03bd_78_, lean_object* v_y_79_){
_start:
{
lean_object* v___x_80_; lean_object* v___x_81_; lean_object* v___f_82_; lean_object* v___x_83_; lean_object* v___x_84_; lean_object* v___f_85_; lean_object* v___f_86_; 
v___x_80_ = lp_tgl__kernel_TGLExt_epsTT(v_a_71_, v_b_72_, v_00_u03bc_77_, v_00_u03bd_78_);
lean_inc(v_y_79_);
v___x_81_ = lp_tgl__kernel_TGLExt_lightWave(v_w_75_, v_y_79_);
v___f_82_ = lean_alloc_closure((void*)(lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_4214226450____hygCtx___hyg_8_), 3, 2);
lean_closure_set(v___f_82_, 0, v___x_80_);
lean_closure_set(v___f_82_, 1, v___x_81_);
v___x_83_ = lp_tgl__kernel_TGLExt_epsTT2(v_a_x27_73_, v_b_x27_74_, v_00_u03bc_77_, v_00_u03bd_78_);
v___x_84_ = lp_tgl__kernel_TGLExt_lightWave2(v_v_76_, v_y_79_);
v___f_85_ = lean_alloc_closure((void*)(lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_4214226450____hygCtx___hyg_8_), 3, 2);
lean_closure_set(v___f_85_, 0, v___x_83_);
lean_closure_set(v___f_85_, 1, v___x_84_);
v___f_86_ = lean_alloc_closure((void*)(lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_1138242547____hygCtx___hyg_8_), 3, 2);
lean_closure_set(v___f_86_, 0, v___f_82_);
lean_closure_set(v___f_86_, 1, v___f_85_);
return v___f_86_;
}
}
LEAN_EXPORT lean_object* lp_tgl__kernel_TGLExt_ttCross___boxed(lean_object* v_a_87_, lean_object* v_b_88_, lean_object* v_a_x27_89_, lean_object* v_b_x27_90_, lean_object* v_w_91_, lean_object* v_v_92_, lean_object* v_00_u03bc_93_, lean_object* v_00_u03bd_94_, lean_object* v_y_95_){
_start:
{
lean_object* v_res_96_; 
v_res_96_ = lp_tgl__kernel_TGLExt_ttCross(v_a_87_, v_b_88_, v_a_x27_89_, v_b_x27_90_, v_w_91_, v_v_92_, v_00_u03bc_93_, v_00_u03bd_94_, v_y_95_);
lean_dec(v_00_u03bd_94_);
lean_dec(v_00_u03bc_93_);
lean_dec(v_b_x27_90_);
lean_dec(v_b_88_);
return v_res_96_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_tgl__kernel_TGLExt_GNSTower(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_tgl__kernel_TGLExt_SecondCone(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_tgl__kernel_TGLExt_GNSTower(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
lp_tgl__kernel_TGLExt_lightCone2 = _init_lp_tgl__kernel_TGLExt_lightCone2();
lean_mark_persistent(lp_tgl__kernel_TGLExt_lightCone2);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
