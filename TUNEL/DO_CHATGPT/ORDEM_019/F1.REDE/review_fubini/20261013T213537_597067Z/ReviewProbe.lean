import FubiniL2
open MeasureTheory TGLExt.ImportedSQ AuditF13v31 F1Rede.Canonical
example : Function.Surjective canonicalFub := canonicalFub.surjective
example : Function.Surjective canonicalPartialFourier := canonicalPartialFourier.surjective
example (f : H1) : canonicalPartialFourier.symm (canonicalPartialFourier f) = f :=
  canonicalPartialFourier.symm_apply_apply f
#check F1Rede.fubiniL2Equiv
#check F1Rede.curryLinearIsometry_surjective
#check canonicalFub
#check canonicalPartialFourier
#check canonical_modularGroupIsBoost
#print axioms F1Rede.measurable_of_distances
#print axioms F1Rede.memLp_section_ae
#print axioms F1Rede.sectionLp
#print axioms F1Rede.sectionLp_coe_ae
#print axioms F1Rede.measurable_section_eLpNorm
#print axioms F1Rede.measurableSet_good_sections
#print axioms F1Rede.sectionLp_dist
#print axioms F1Rede.sectionLp_stronglyMeasurable
#print axioms F1Rede.norm_sq_integral
#print axioms F1Rede.sectionLp_norm_ae
#print axioms F1Rede.norm_sq_disintegration
#print axioms F1Rede.sectionLp_memLp
#print axioms F1Rede.curryLp
#print axioms F1Rede.curryLp_coe_ae
#print axioms F1Rede.curryLp_norm
#print axioms F1Rede.ae_ae_reverse
#print axioms F1Rede.curryLp_add
#print axioms F1Rede.curryLp_smul
#print axioms F1Rede.curryLinearIsometry
#print axioms F1Rede.rectangle_memLp
#print axioms F1Rede.indicator_in_range
#print axioms F1Rede.curryLinearIsometry_surjective
#print axioms F1Rede.fubiniL2Equiv
#print axioms F1Rede.Canonical.canonicalFub
#print axioms F1Rede.Canonical.canonicalFub_sections
#print axioms F1Rede.Canonical.canonicalPartialFourier
#print axioms F1Rede.Canonical.canonicalFub_shift
#print axioms F1Rede.Canonical.canonical_toRapidity_boost
#print axioms F1Rede.Canonical.canonicalPartialFourier_boost
#print axioms F1Rede.Canonical.canonicalSigma
#print axioms F1Rede.Canonical.canonical_modularGroupIsBoost

open Lean in
run_cmd do
  for n in [``F1Rede.measurable_of_distances, ``F1Rede.memLp_section_ae, ``F1Rede.sectionLp, ``F1Rede.sectionLp_coe_ae, ``F1Rede.measurable_section_eLpNorm, ``F1Rede.measurableSet_good_sections, ``F1Rede.sectionLp_dist, ``F1Rede.sectionLp_stronglyMeasurable, ``F1Rede.norm_sq_integral, ``F1Rede.sectionLp_norm_ae, ``F1Rede.norm_sq_disintegration, ``F1Rede.sectionLp_memLp, ``F1Rede.curryLp, ``F1Rede.curryLp_coe_ae, ``F1Rede.curryLp_norm, ``F1Rede.ae_ae_reverse, ``F1Rede.curryLp_add, ``F1Rede.curryLp_smul, ``F1Rede.curryLinearIsometry, ``F1Rede.rectangle_memLp, ``F1Rede.indicator_in_range, ``F1Rede.curryLinearIsometry_surjective, ``F1Rede.fubiniL2Equiv, ``F1Rede.Canonical.canonicalFub, ``F1Rede.Canonical.canonicalFub_sections, ``F1Rede.Canonical.canonicalPartialFourier, ``F1Rede.Canonical.canonicalFub_shift, ``F1Rede.Canonical.canonical_toRapidity_boost, ``F1Rede.Canonical.canonicalPartialFourier_boost, ``F1Rede.Canonical.canonicalSigma, ``F1Rede.Canonical.canonical_modularGroupIsBoost] do
    let axs ← collectAxioms n
    unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
      throwError "AXIOM_AUDIT_REFUSED: {n}"
    let ci ← getConstInfo n
    match ci with
    | .axiomInfo _ => throwError "NEW_AXIOM_REFUSED: {n}"
    | _ => pure ()
