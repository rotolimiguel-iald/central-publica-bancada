// Lean compiler output
// Module: TGLExt.SectorRouteComparison
// Imports: public import Init public meta import Init public import TGLExt.ThermodynamicFriedmann
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
lean_object* l_npowRec___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_4214226450____hygCtx___hyg_8_(lean_object*, lean_object*, lean_object*);
extern lean_object* lp_mathlib_Real_instAddCommMonoid;
lean_object* lp_mathlib_Finset_sum___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_secondMoment___redArg___lam__0(lean_object*, lean_object*, lean_object*, lean_object*);
static const lean_closure_object l_ChatgptAudit_FLRW_SectorFluid_secondMoment___redArg___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_4214226450____hygCtx___hyg_8_, .m_arity = 3, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* l_ChatgptAudit_FLRW_SectorFluid_secondMoment___redArg___closed__0 = (const lean_object*)&l_ChatgptAudit_FLRW_SectorFluid_secondMoment___redArg___closed__0_value;
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_secondMoment___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_secondMoment(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_secondMoment___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_secondMoment___redArg___lam__0(lean_object* v_F_1_, lean_object* v___f_2_, lean_object* v_t_3_, lean_object* v_i_4_){
_start:
{
lean_object* v_rho_5_; lean_object* v_w_6_; lean_object* v___x_7_; lean_object* v___x_8_; lean_object* v___f_9_; lean_object* v___x_10_; lean_object* v___x_11_; lean_object* v___x_12_; lean_object* v___f_13_; 
v_rho_5_ = lean_ctor_get(v_F_1_, 0);
lean_inc(v_rho_5_);
v_w_6_ = lean_ctor_get(v_F_1_, 1);
lean_inc(v_w_6_);
lean_dec_ref(v_F_1_);
v___x_7_ = lp_mathlib_Real_definition_00___x40_Mathlib_Data_Real_Basic_1279875089____hygCtx___hyg_8_;
lean_inc(v_i_4_);
v___x_8_ = lean_apply_1(v_w_6_, v_i_4_);
v___f_9_ = lean_alloc_closure((void*)(lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_1138242547____hygCtx___hyg_8_), 3, 2);
lean_closure_set(v___f_9_, 0, v___x_7_);
lean_closure_set(v___f_9_, 1, v___x_8_);
v___x_10_ = lean_unsigned_to_nat(2u);
v___x_11_ = l_npowRec___redArg(v___x_7_, v___f_2_, v___x_10_, v___f_9_);
v___x_12_ = lean_apply_2(v_rho_5_, v_i_4_, v_t_3_);
v___f_13_ = lean_alloc_closure((void*)(lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_4214226450____hygCtx___hyg_8_), 3, 2);
lean_closure_set(v___f_13_, 0, v___x_11_);
lean_closure_set(v___f_13_, 1, v___x_12_);
return v___f_13_;
}
}
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_secondMoment___redArg(lean_object* v_inst_15_, lean_object* v_F_16_, lean_object* v_t_17_){
_start:
{
lean_object* v___f_18_; lean_object* v___f_19_; lean_object* v___x_20_; lean_object* v___x_21_; 
v___f_18_ = ((lean_object*)(l_ChatgptAudit_FLRW_SectorFluid_secondMoment___redArg___closed__0));
v___f_19_ = lean_alloc_closure((void*)(l_ChatgptAudit_FLRW_SectorFluid_secondMoment___redArg___lam__0), 4, 3);
lean_closure_set(v___f_19_, 0, v_F_16_);
lean_closure_set(v___f_19_, 1, v___f_18_);
lean_closure_set(v___f_19_, 2, v_t_17_);
v___x_20_ = lp_mathlib_Real_instAddCommMonoid;
v___x_21_ = lp_mathlib_Finset_sum___redArg(v___x_20_, v_inst_15_, v___f_19_);
return v___x_21_;
}
}
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_secondMoment(lean_object* v_00_u03b9_22_, lean_object* v_inst_23_, lean_object* v_I_24_, lean_object* v_H_25_, lean_object* v_F_26_, lean_object* v_t_27_){
_start:
{
lean_object* v___x_28_; 
v___x_28_ = l_ChatgptAudit_FLRW_SectorFluid_secondMoment___redArg(v_inst_23_, v_F_26_, v_t_27_);
return v___x_28_;
}
}
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_secondMoment___boxed(lean_object* v_00_u03b9_29_, lean_object* v_inst_30_, lean_object* v_I_31_, lean_object* v_H_32_, lean_object* v_F_33_, lean_object* v_t_34_){
_start:
{
lean_object* v_res_35_; 
v_res_35_ = l_ChatgptAudit_FLRW_SectorFluid_secondMoment(v_00_u03b9_29_, v_inst_30_, v_I_31_, v_H_32_, v_F_33_, v_t_34_);
lean_dec(v_H_32_);
return v_res_35_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_TGLExt_ThermodynamicFriedmann(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_TGLExt_SectorRouteComparison(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_TGLExt_ThermodynamicFriedmann(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
