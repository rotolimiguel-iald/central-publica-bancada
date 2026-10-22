// Lean compiler output
// Module: TGLExt.SectorFluidClosure
// Imports: public import Init public meta import Init public import TGLExt.TheSameBetaReadsThreeFaces public import TGLExt.FLRWFieldEquations
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
lean_object* lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_4214226450____hygCtx___hyg_8_(lean_object*, lean_object*, lean_object*);
extern lean_object* lp_mathlib_Real_instAddCommMonoid;
lean_object* lp_mathlib_Finset_sum___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_totalRho___redArg___lam__0(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_totalRho___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_totalRho(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_totalRho___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_totalPressure___redArg___lam__0(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_totalPressure___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_totalPressure(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_totalPressure___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_enthalpy___redArg___lam__0(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_enthalpy___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_enthalpy(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_enthalpy___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_correctedRho___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_correctedRho(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_correctedRho___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_correctedTotalRho___redArg___lam__0(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_correctedTotalRho___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_correctedTotalRho(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_correctedTotalRho___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_correctedTotalPressure___redArg___lam__0(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_correctedTotalPressure___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_correctedTotalPressure(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_correctedTotalPressure___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_totalRho___redArg___lam__0(lean_object* v_F_1_, lean_object* v_t_2_, lean_object* v_i_3_){
_start:
{
lean_object* v_rho_4_; lean_object* v___x_5_; 
v_rho_4_ = lean_ctor_get(v_F_1_, 0);
lean_inc(v_rho_4_);
lean_dec_ref(v_F_1_);
v___x_5_ = lean_apply_2(v_rho_4_, v_i_3_, v_t_2_);
return v___x_5_;
}
}
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_totalRho___redArg(lean_object* v_inst_6_, lean_object* v_F_7_, lean_object* v_t_8_){
_start:
{
lean_object* v___f_9_; lean_object* v___x_10_; lean_object* v___x_11_; 
v___f_9_ = lean_alloc_closure((void*)(l_ChatgptAudit_FLRW_SectorFluid_totalRho___redArg___lam__0), 3, 2);
lean_closure_set(v___f_9_, 0, v_F_7_);
lean_closure_set(v___f_9_, 1, v_t_8_);
v___x_10_ = lp_mathlib_Real_instAddCommMonoid;
v___x_11_ = lp_mathlib_Finset_sum___redArg(v___x_10_, v_inst_6_, v___f_9_);
return v___x_11_;
}
}
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_totalRho(lean_object* v_00_u03b9_12_, lean_object* v_inst_13_, lean_object* v_I_14_, lean_object* v_H_15_, lean_object* v_F_16_, lean_object* v_t_17_){
_start:
{
lean_object* v___x_18_; 
v___x_18_ = l_ChatgptAudit_FLRW_SectorFluid_totalRho___redArg(v_inst_13_, v_F_16_, v_t_17_);
return v___x_18_;
}
}
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_totalRho___boxed(lean_object* v_00_u03b9_19_, lean_object* v_inst_20_, lean_object* v_I_21_, lean_object* v_H_22_, lean_object* v_F_23_, lean_object* v_t_24_){
_start:
{
lean_object* v_res_25_; 
v_res_25_ = l_ChatgptAudit_FLRW_SectorFluid_totalRho(v_00_u03b9_19_, v_inst_20_, v_I_21_, v_H_22_, v_F_23_, v_t_24_);
lean_dec(v_H_22_);
return v_res_25_;
}
}
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_totalPressure___redArg___lam__0(lean_object* v_F_26_, lean_object* v_t_27_, lean_object* v_i_28_){
_start:
{
lean_object* v_rho_29_; lean_object* v_w_30_; lean_object* v___x_31_; lean_object* v___x_32_; lean_object* v___f_33_; 
v_rho_29_ = lean_ctor_get(v_F_26_, 0);
lean_inc(v_rho_29_);
v_w_30_ = lean_ctor_get(v_F_26_, 1);
lean_inc(v_w_30_);
lean_dec_ref(v_F_26_);
lean_inc(v_i_28_);
v___x_31_ = lean_apply_1(v_w_30_, v_i_28_);
v___x_32_ = lean_apply_2(v_rho_29_, v_i_28_, v_t_27_);
v___f_33_ = lean_alloc_closure((void*)(lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_4214226450____hygCtx___hyg_8_), 3, 2);
lean_closure_set(v___f_33_, 0, v___x_31_);
lean_closure_set(v___f_33_, 1, v___x_32_);
return v___f_33_;
}
}
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_totalPressure___redArg(lean_object* v_inst_34_, lean_object* v_F_35_, lean_object* v_t_36_){
_start:
{
lean_object* v___f_37_; lean_object* v___x_38_; lean_object* v___x_39_; 
v___f_37_ = lean_alloc_closure((void*)(l_ChatgptAudit_FLRW_SectorFluid_totalPressure___redArg___lam__0), 3, 2);
lean_closure_set(v___f_37_, 0, v_F_35_);
lean_closure_set(v___f_37_, 1, v_t_36_);
v___x_38_ = lp_mathlib_Real_instAddCommMonoid;
v___x_39_ = lp_mathlib_Finset_sum___redArg(v___x_38_, v_inst_34_, v___f_37_);
return v___x_39_;
}
}
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_totalPressure(lean_object* v_00_u03b9_40_, lean_object* v_inst_41_, lean_object* v_I_42_, lean_object* v_H_43_, lean_object* v_F_44_, lean_object* v_t_45_){
_start:
{
lean_object* v___x_46_; 
v___x_46_ = l_ChatgptAudit_FLRW_SectorFluid_totalPressure___redArg(v_inst_41_, v_F_44_, v_t_45_);
return v___x_46_;
}
}
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_totalPressure___boxed(lean_object* v_00_u03b9_47_, lean_object* v_inst_48_, lean_object* v_I_49_, lean_object* v_H_50_, lean_object* v_F_51_, lean_object* v_t_52_){
_start:
{
lean_object* v_res_53_; 
v_res_53_ = l_ChatgptAudit_FLRW_SectorFluid_totalPressure(v_00_u03b9_47_, v_inst_48_, v_I_49_, v_H_50_, v_F_51_, v_t_52_);
lean_dec(v_H_50_);
return v_res_53_;
}
}
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_enthalpy___redArg___lam__0(lean_object* v_F_54_, lean_object* v_t_55_, lean_object* v_i_56_){
_start:
{
lean_object* v_rho_57_; lean_object* v_w_58_; lean_object* v___x_59_; lean_object* v___x_60_; lean_object* v___f_61_; lean_object* v___x_62_; lean_object* v___f_63_; 
v_rho_57_ = lean_ctor_get(v_F_54_, 0);
lean_inc(v_rho_57_);
v_w_58_ = lean_ctor_get(v_F_54_, 1);
lean_inc(v_w_58_);
lean_dec_ref(v_F_54_);
v___x_59_ = lp_mathlib_Real_definition_00___x40_Mathlib_Data_Real_Basic_1279875089____hygCtx___hyg_8_;
lean_inc(v_i_56_);
v___x_60_ = lean_apply_1(v_w_58_, v_i_56_);
v___f_61_ = lean_alloc_closure((void*)(lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_1138242547____hygCtx___hyg_8_), 3, 2);
lean_closure_set(v___f_61_, 0, v___x_59_);
lean_closure_set(v___f_61_, 1, v___x_60_);
v___x_62_ = lean_apply_2(v_rho_57_, v_i_56_, v_t_55_);
v___f_63_ = lean_alloc_closure((void*)(lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_4214226450____hygCtx___hyg_8_), 3, 2);
lean_closure_set(v___f_63_, 0, v___f_61_);
lean_closure_set(v___f_63_, 1, v___x_62_);
return v___f_63_;
}
}
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_enthalpy___redArg(lean_object* v_inst_64_, lean_object* v_F_65_, lean_object* v_t_66_){
_start:
{
lean_object* v___f_67_; lean_object* v___x_68_; lean_object* v___x_69_; 
v___f_67_ = lean_alloc_closure((void*)(l_ChatgptAudit_FLRW_SectorFluid_enthalpy___redArg___lam__0), 3, 2);
lean_closure_set(v___f_67_, 0, v_F_65_);
lean_closure_set(v___f_67_, 1, v_t_66_);
v___x_68_ = lp_mathlib_Real_instAddCommMonoid;
v___x_69_ = lp_mathlib_Finset_sum___redArg(v___x_68_, v_inst_64_, v___f_67_);
return v___x_69_;
}
}
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_enthalpy(lean_object* v_00_u03b9_70_, lean_object* v_inst_71_, lean_object* v_I_72_, lean_object* v_H_73_, lean_object* v_F_74_, lean_object* v_t_75_){
_start:
{
lean_object* v___x_76_; 
v___x_76_ = l_ChatgptAudit_FLRW_SectorFluid_enthalpy___redArg(v_inst_71_, v_F_74_, v_t_75_);
return v___x_76_;
}
}
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_enthalpy___boxed(lean_object* v_00_u03b9_77_, lean_object* v_inst_78_, lean_object* v_I_79_, lean_object* v_H_80_, lean_object* v_F_81_, lean_object* v_t_82_){
_start:
{
lean_object* v_res_83_; 
v_res_83_ = l_ChatgptAudit_FLRW_SectorFluid_enthalpy(v_00_u03b9_77_, v_inst_78_, v_I_79_, v_H_80_, v_F_81_, v_t_82_);
lean_dec(v_H_80_);
return v_res_83_;
}
}
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_correctedRho___redArg(lean_object* v_F_84_, lean_object* v_c_85_, lean_object* v_i_86_, lean_object* v_t_87_){
_start:
{
lean_object* v_rho_88_; lean_object* v_w_89_; lean_object* v___x_90_; lean_object* v___x_91_; lean_object* v___f_92_; lean_object* v___f_93_; lean_object* v___f_94_; lean_object* v___x_95_; lean_object* v___f_96_; 
v_rho_88_ = lean_ctor_get(v_F_84_, 0);
lean_inc(v_rho_88_);
v_w_89_ = lean_ctor_get(v_F_84_, 1);
lean_inc(v_w_89_);
lean_dec_ref(v_F_84_);
v___x_90_ = lp_mathlib_Real_definition_00___x40_Mathlib_Data_Real_Basic_1279875089____hygCtx___hyg_8_;
lean_inc(v_i_86_);
v___x_91_ = lean_apply_1(v_w_89_, v_i_86_);
v___f_92_ = lean_alloc_closure((void*)(lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_1138242547____hygCtx___hyg_8_), 3, 2);
lean_closure_set(v___f_92_, 0, v___x_90_);
lean_closure_set(v___f_92_, 1, v___x_91_);
v___f_93_ = lean_alloc_closure((void*)(lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_4214226450____hygCtx___hyg_8_), 3, 2);
lean_closure_set(v___f_93_, 0, v_c_85_);
lean_closure_set(v___f_93_, 1, v___f_92_);
v___f_94_ = lean_alloc_closure((void*)(lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_1138242547____hygCtx___hyg_8_), 3, 2);
lean_closure_set(v___f_94_, 0, v___x_90_);
lean_closure_set(v___f_94_, 1, v___f_93_);
v___x_95_ = lean_apply_2(v_rho_88_, v_i_86_, v_t_87_);
v___f_96_ = lean_alloc_closure((void*)(lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_4214226450____hygCtx___hyg_8_), 3, 2);
lean_closure_set(v___f_96_, 0, v___f_94_);
lean_closure_set(v___f_96_, 1, v___x_95_);
return v___f_96_;
}
}
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_correctedRho(lean_object* v_00_u03b9_97_, lean_object* v_inst_98_, lean_object* v_I_99_, lean_object* v_H_100_, lean_object* v_F_101_, lean_object* v_c_102_, lean_object* v_i_103_, lean_object* v_t_104_){
_start:
{
lean_object* v___x_105_; 
v___x_105_ = l_ChatgptAudit_FLRW_SectorFluid_correctedRho___redArg(v_F_101_, v_c_102_, v_i_103_, v_t_104_);
return v___x_105_;
}
}
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_correctedRho___boxed(lean_object* v_00_u03b9_106_, lean_object* v_inst_107_, lean_object* v_I_108_, lean_object* v_H_109_, lean_object* v_F_110_, lean_object* v_c_111_, lean_object* v_i_112_, lean_object* v_t_113_){
_start:
{
lean_object* v_res_114_; 
v_res_114_ = l_ChatgptAudit_FLRW_SectorFluid_correctedRho(v_00_u03b9_106_, v_inst_107_, v_I_108_, v_H_109_, v_F_110_, v_c_111_, v_i_112_, v_t_113_);
lean_dec(v_H_109_);
lean_dec(v_inst_107_);
return v_res_114_;
}
}
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_correctedTotalRho___redArg___lam__0(lean_object* v_F_115_, lean_object* v_c_116_, lean_object* v_t_117_, lean_object* v_i_118_){
_start:
{
lean_object* v___x_119_; 
v___x_119_ = l_ChatgptAudit_FLRW_SectorFluid_correctedRho___redArg(v_F_115_, v_c_116_, v_i_118_, v_t_117_);
return v___x_119_;
}
}
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_correctedTotalRho___redArg(lean_object* v_inst_120_, lean_object* v_F_121_, lean_object* v_c_122_, lean_object* v_t_123_){
_start:
{
lean_object* v___f_124_; lean_object* v___x_125_; lean_object* v___x_126_; 
v___f_124_ = lean_alloc_closure((void*)(l_ChatgptAudit_FLRW_SectorFluid_correctedTotalRho___redArg___lam__0), 4, 3);
lean_closure_set(v___f_124_, 0, v_F_121_);
lean_closure_set(v___f_124_, 1, v_c_122_);
lean_closure_set(v___f_124_, 2, v_t_123_);
v___x_125_ = lp_mathlib_Real_instAddCommMonoid;
v___x_126_ = lp_mathlib_Finset_sum___redArg(v___x_125_, v_inst_120_, v___f_124_);
return v___x_126_;
}
}
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_correctedTotalRho(lean_object* v_00_u03b9_127_, lean_object* v_inst_128_, lean_object* v_I_129_, lean_object* v_H_130_, lean_object* v_F_131_, lean_object* v_c_132_, lean_object* v_t_133_){
_start:
{
lean_object* v___x_134_; 
v___x_134_ = l_ChatgptAudit_FLRW_SectorFluid_correctedTotalRho___redArg(v_inst_128_, v_F_131_, v_c_132_, v_t_133_);
return v___x_134_;
}
}
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_correctedTotalRho___boxed(lean_object* v_00_u03b9_135_, lean_object* v_inst_136_, lean_object* v_I_137_, lean_object* v_H_138_, lean_object* v_F_139_, lean_object* v_c_140_, lean_object* v_t_141_){
_start:
{
lean_object* v_res_142_; 
v_res_142_ = l_ChatgptAudit_FLRW_SectorFluid_correctedTotalRho(v_00_u03b9_135_, v_inst_136_, v_I_137_, v_H_138_, v_F_139_, v_c_140_, v_t_141_);
lean_dec(v_H_138_);
return v_res_142_;
}
}
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_correctedTotalPressure___redArg___lam__0(lean_object* v_F_143_, lean_object* v_c_144_, lean_object* v_t_145_, lean_object* v_i_146_){
_start:
{
lean_object* v_w_147_; lean_object* v___x_148_; lean_object* v___x_149_; lean_object* v___f_150_; 
v_w_147_ = lean_ctor_get(v_F_143_, 1);
lean_inc(v_w_147_);
lean_inc(v_i_146_);
v___x_148_ = lean_apply_1(v_w_147_, v_i_146_);
v___x_149_ = l_ChatgptAudit_FLRW_SectorFluid_correctedRho___redArg(v_F_143_, v_c_144_, v_i_146_, v_t_145_);
v___f_150_ = lean_alloc_closure((void*)(lp_mathlib_Real_definition___lam__0_00___x40_Mathlib_Data_Real_Basic_4214226450____hygCtx___hyg_8_), 3, 2);
lean_closure_set(v___f_150_, 0, v___x_148_);
lean_closure_set(v___f_150_, 1, v___x_149_);
return v___f_150_;
}
}
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_correctedTotalPressure___redArg(lean_object* v_inst_151_, lean_object* v_F_152_, lean_object* v_c_153_, lean_object* v_t_154_){
_start:
{
lean_object* v___f_155_; lean_object* v___x_156_; lean_object* v___x_157_; 
v___f_155_ = lean_alloc_closure((void*)(l_ChatgptAudit_FLRW_SectorFluid_correctedTotalPressure___redArg___lam__0), 4, 3);
lean_closure_set(v___f_155_, 0, v_F_152_);
lean_closure_set(v___f_155_, 1, v_c_153_);
lean_closure_set(v___f_155_, 2, v_t_154_);
v___x_156_ = lp_mathlib_Real_instAddCommMonoid;
v___x_157_ = lp_mathlib_Finset_sum___redArg(v___x_156_, v_inst_151_, v___f_155_);
return v___x_157_;
}
}
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_correctedTotalPressure(lean_object* v_00_u03b9_158_, lean_object* v_inst_159_, lean_object* v_I_160_, lean_object* v_H_161_, lean_object* v_F_162_, lean_object* v_c_163_, lean_object* v_t_164_){
_start:
{
lean_object* v___x_165_; 
v___x_165_ = l_ChatgptAudit_FLRW_SectorFluid_correctedTotalPressure___redArg(v_inst_159_, v_F_162_, v_c_163_, v_t_164_);
return v___x_165_;
}
}
LEAN_EXPORT lean_object* l_ChatgptAudit_FLRW_SectorFluid_correctedTotalPressure___boxed(lean_object* v_00_u03b9_166_, lean_object* v_inst_167_, lean_object* v_I_168_, lean_object* v_H_169_, lean_object* v_F_170_, lean_object* v_c_171_, lean_object* v_t_172_){
_start:
{
lean_object* v_res_173_; 
v_res_173_ = l_ChatgptAudit_FLRW_SectorFluid_correctedTotalPressure(v_00_u03b9_166_, v_inst_167_, v_I_168_, v_H_169_, v_F_170_, v_c_171_, v_t_172_);
lean_dec(v_H_169_);
return v_res_173_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_tgl__kernel_TGLExt_TheSameBetaReadsThreeFaces(uint8_t builtin);
lean_object* initialize_tgl__kernel_TGLExt_FLRWFieldEquations(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_TGLExt_SectorFluidClosure(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_tgl__kernel_TGLExt_TheSameBetaReadsThreeFaces(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_tgl__kernel_TGLExt_FLRWFieldEquations(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
