from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parent
src=p/'VectorRapiditySpectrum.lean';raw=src.read_bytes();s=raw.decode()
body=s[s.index('  -- cada ladrilho'):s.index('  have hgm :')]
head='''import OrbitalBoostTransport
import VectorRapiditySpectrum

set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
open MeasureTheory Filter Set
open scoped ENNReal
namespace ChatgptAudit.WignerRapidityMeasure016

/-- Existing integer-tile argument, factored out without changing its proof. -/
theorem integer_periodic_lintegral_zero (g : ℝ → ℝ≥0∞)
    (hfin : ∫⁻ x, g x < ∞)
    (hper : ∀ n : ℤ, (fun x => g (x+n)) =ᵐ[volume] g) : ∫⁻ x, g x = 0 := by
'''
tail='''  exact hzero

variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℂ E]

theorem product_norm_periodic_zero (f : Lp E 2 momentumMeasure)
    (hper : ∀ n : ℤ,
      (fun y : MomentumCoordinates => ‖f (y.1,y.2+n)‖ₑ) =ᵐ[momentumMeasure]
        (fun y => ‖f y‖ₑ)) : f=0 := by
  let F : MomentumCoordinates → ℝ≥0∞ := fun y => ‖f y‖ₑ ^ ((2 : ℝ≥0∞).toReal)
  have hFm : AEMeasurable F momentumMeasure :=
    ((Lp.aestronglyMeasurable f).enorm).pow_const _
  have hfin : ∫⁻ y, F y ∂momentumMeasure < ∞ :=
    lintegral_rpow_enorm_lt_top_of_eLpNorm_lt_top (p := 2) two_ne_zero ENNReal.ofNat_ne_top
      (Lp.eLpNorm_lt_top f)
  let g : ℝ → ℝ≥0∞ := fun x => ∫⁻ q : Transverse, F (q,x)
  have htonelli : (∫⁻ y, F y ∂momentumMeasure) = ∫⁻ x, g x :=
    lintegral_prod_symm F hFm
  have hgf : ∫⁻ x, g x < ∞ := by rw [← htonelli]; exact hfin
  have hgp : ∀ n : ℤ, (fun x => g (x+n)) =ᵐ[volume] g := by
    intro n
    have hn := (measurePreserving_swap (μ := (volume : Measure ℝ))
      (ν := (volume : Measure Transverse))).quasiMeasurePreserving.ae (hper n)
    have hna := ae_ae_of_ae_prod hn
    filter_upwards [hna] with x hx
    apply lintegral_congr_ae
    filter_upwards [hx] with q hq
    exact congrArg (fun z : ℝ≥0∞ => z ^ ((2 : ℝ≥0∞).toReal)) hq
  have hz : ∫⁻ y, F y ∂momentumMeasure = 0 :=
    htonelli.trans (integer_periodic_lintegral_zero g hgf hgp)
  have hzae : F =ᵐ[momentumMeasure] 0 := (lintegral_eq_zero_iff' hFm).mp hz
  apply Lp.ext
  filter_upwards [hzae, Lp.coeFn_zero E 2 momentumMeasure] with y hy hzero
  rw [hzero]
  change ‖f y‖ₑ ^ ((2 : ℝ≥0∞).toReal) = 0 at hy
  have hpos : (0 : ℝ) < (2 : ℝ≥0∞).toReal := by norm_num
  rw [ENNReal.rpow_eq_zero_iff] at hy
  rcases hy with ⟨h0,_⟩ | ⟨_,hneg⟩
  · simpa using h0
  · exact absurd hneg (not_lt.mpr hpos.le)

theorem productRapidityShift_no_eigen (f : Lp E 2 momentumMeasure)
    (h : ∀ s : ℝ, ∃ c : ℂ, ‖c‖=1 ∧ productRapidityShift s f = c • f) : f=0 := by
  apply product_norm_periodic_zero f
  intro n
  obtain ⟨c,hc,he⟩ := h (-(n : ℝ))
  have h1 := productRapidityShift_ae (-(n : ℝ)) f
  rw [he] at h1
  have h2 := Lp.coeFn_smul c f
  have hce : ‖c‖ₑ=1 := by rw [← ofReal_norm, hc, ENNReal.ofReal_one]
  filter_upwards [h1,h2] with y e1 e2
  simp only [coordinateShift, neg_neg] at e1
  rw [← e1, e2, Pi.smul_apply, enorm_smul, hce, one_mul]

theorem orbitalScalarBoost_no_eigen (m : ℝ) (f : Lp E 2 (orbitalMeasure m))
    (h : ∀ s : ℝ, ∃ c : ℂ, ‖c‖=1 ∧ orbitalScalarBoost m s f = c • f) : f=0 := by
  have hz : orbitalL2Pullback m f = 0 := by
    apply productRapidityShift_no_eigen
    intro s
    obtain ⟨c,hc,he⟩ := h s
    refine ⟨c,hc,?_⟩
    rw [← orbitalScalarBoost_intertwines, he, map_smul]
  apply (orbitalL2Pullback m).injective
  simpa using hz

#print axioms integer_periodic_lintegral_zero
#print axioms product_norm_periodic_zero
#print axioms productRapidityShift_no_eigen
#print axioms orbitalScalarBoost_no_eigen
end ChatgptAudit.WignerRapidityMeasure016
'''
dest=p/'ProductOrbitalSpectrum.lean';assert not dest.exists()
data=(head+body+tail).encode();tmp=dest.with_suffix('.tmp')
with tmp.open('xb') as f:f.write(data)
assert tmp.read_bytes()==data;tmp.rename(dest)
info=dict(source=str(src),source_sha256=hashlib.sha256(raw).hexdigest(),extraction='integer interval tiling block, unchanged; final exact hzero added',target_sha256=hashlib.sha256(data).hexdigest())
d=p/'product_spectrum_provenance.json';t=d.with_suffix('.tmp');b=json.dumps(info,indent=2).encode()
with t.open('xb') as f:f.write(b)
assert t.read_bytes()==b;t.rename(d)
