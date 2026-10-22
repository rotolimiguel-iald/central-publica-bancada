import WeightedPalatiniR86_3

/-! R87: covariant identification of the actual curved Palatini current for a
symmetric covariant metric variation g+t h. No flat-background restriction.
The contractions below are of covariant h-jets with inverse metrics, not a
new definition of the Palatini current. This layer does not yet identify their
ordinary derivatives with derivatives of the raised tensor, derive the Hessian
weighted current, or infer field equations from stationarity in P. -/
set_option autoImplicit false
set_option maxHeartbeats 16000000
namespace ChatgptAudit.SymmetricBoundaryR87
open Matrix Filter Topology Set ChatgptAudit.CurvedConnection
  ChatgptAudit.MetricVariation ChatgptAudit.MetricRicci ChatgptAudit.MetricLieConnection
  ChatgptAudit.PalatiniBoundaryR85
noncomputable section

theorem lower_covariant_variation (h : Tensor4) (dh Gamma : Fin 4 → Tensor4)
    (hs : hᵀ=h) (ht : ∀ i j l, Gamma i l j=Gamma j l i) (i : Fin 4) :
    lowerChristoffelJet (covariantTensorJet h dh Gamma) i =
      lowerChristoffelJet dh i - h * Gamma i := by
  ext j k
  have he (a b : Fin 4) : h b a=h a b := congrArg (fun A : Tensor4 => A a b) hs
  simp only [lowerChristoffelJet, covariantTensorJet, Matrix.sub_apply,
    Matrix.mul_apply, Matrix.transpose_apply, Fin.sum_univ_four,
    ht k j, ht j i, ht k i, he j 0, he j 1, he j 2, he j 3]
  ring

theorem actual_connection_variation_covariant
    (U : Set Coordinate4) (hU : IsOpen U) (g h : TensorField4)
    (hs : ∀ y∈U, (g y)ᵀ=g y) (x : Coordinate4) (hx : x∈U)
    (hh : (h x)ᵀ=h x) (i : Fin 4) :
    metricConnectionVariation g h x i = (g x)⁻¹ *
      lowerChristoffelJet (covariantTensorJet (h x) (tensorFieldJet h x)
        (leviCivitaField g (fun y => (g y)⁻¹) x)) i := by
  rw [lower_covariant_variation _ _ _ hh
    (levi_civita_field_torsion_free U hU g (fun y => (g y)⁻¹) hs x hx) i,
    metric_connection_variation_formula]
  noncomm_ring

theorem covariant_variation_symmetric (h : Tensor4) (dh Gamma : Fin 4 → Tensor4)
    (hs : hᵀ=h) (hd : ∀ i, (dh i)ᵀ=dh i) (i : Fin 4) :
    (covariantTensorJet h dh Gamma i)ᵀ=covariantTensorJet h dh Gamma i := by
  simp only [covariantTensorJet, Matrix.transpose_sub, Matrix.transpose_mul,
    Matrix.transpose_transpose, hs, hd]
  abel

/-- Pure contraction of the covariant variation, with no desired identity assumed. -/
theorem contracted_covariant_variation (q : Tensor4) (D : Fin 4 → Tensor4)
    (hq : qᵀ=q) (hd : ∀ i, (D i)ᵀ=D i) (a : Fin 4) :
    (∑ b : Fin 4, ∑ j : Fin 4,
      (q b j * (q * lowerChristoffelJet D j) a b -
       q b a * (q * lowerChristoffelJet D j) j b)) =
      (∑ b : Fin 4, (q * D b * q) a b) -
        ∑ k : Fin 4, q a k * Matrix.trace (q * D k) := by
  have q01 : q 1 0=q 0 1 := congrArg (fun A : Tensor4 => A 0 1) hq
  have d01 (i : Fin 4) : D i 1 0=D i 0 1 := congrArg (fun A : Tensor4 => A 0 1) (hd i)
  have q02 : q 2 0=q 0 2 := congrArg (fun A : Tensor4 => A 0 2) hq
  have d02 (i : Fin 4) : D i 2 0=D i 0 2 := congrArg (fun A : Tensor4 => A 0 2) (hd i)
  have q03 : q 3 0=q 0 3 := congrArg (fun A : Tensor4 => A 0 3) hq
  have d03 (i : Fin 4) : D i 3 0=D i 0 3 := congrArg (fun A : Tensor4 => A 0 3) (hd i)
  have q12 : q 2 1=q 1 2 := congrArg (fun A : Tensor4 => A 1 2) hq
  have d12 (i : Fin 4) : D i 2 1=D i 1 2 := congrArg (fun A : Tensor4 => A 1 2) (hd i)
  have q13 : q 3 1=q 1 3 := congrArg (fun A : Tensor4 => A 1 3) hq
  have d13 (i : Fin 4) : D i 3 1=D i 1 3 := congrArg (fun A : Tensor4 => A 1 3) (hd i)
  have q23 : q 3 2=q 2 3 := congrArg (fun A : Tensor4 => A 2 3) hq
  have d23 (i : Fin 4) : D i 3 2=D i 2 3 := congrArg (fun A : Tensor4 => A 2 3) (hd i)
  have ha : a = 0 ∨ a = 1 ∨ a = 2 ∨ a = 3 := by omega
  rcases ha with rfl | rfl | rfl | rfl <;>
    simp only [lowerChristoffelJet, Matrix.mul_apply, Matrix.trace, Matrix.diag_apply,
      Fin.sum_univ_four, q01, q02, q03, q12, q13, q23, d01, d02, d03, d12, d13, d23] <;> ring

theorem actual_palatini_current_covariant
    (U : Set Coordinate4) (hU : IsOpen U) (g h : TensorField4)
    (hs : ∀ y∈U, (g y)ᵀ=g y) (hh : ∀ y∈U, (h y)ᵀ=h y)
    (hi : ∀ y∈U, IsUnit (g y)) (x : Coordinate4) (hx : x∈U) (a : Fin 4) :
    palatiniCurrent (fun y => (g y)⁻¹) (metricConnectionVariation g h) x a =
      (∑ b : Fin 4, ((g x)⁻¹ * covariantTensorJet (h x) (tensorFieldJet h x)
        (leviCivitaField g (fun y => (g y)⁻¹) x) b * (g x)⁻¹) a b) -
      ∑ k : Fin 4, (g x)⁻¹ a k * Matrix.trace ((g x)⁻¹ *
        covariantTensorJet (h x) (tensorFieldJet h x)
          (leviCivitaField g (fun y => (g y)⁻¹) x) k) := by
  unfold palatiniCurrent
  simp_rw [actual_connection_variation_covariant U hU g h hs x hx (hh x hx)]
  apply contracted_covariant_variation
  · exact inverse_symmetric_of_symmetric (g x) (g x)⁻¹ (hs x hx)
      (actual_inverse_left (g x) (hi x hx))
  · exact covariant_variation_symmetric (h x) (tensorFieldJet h x) _ (hh x hx)
      (tensorFieldJet_symmetric_on U hU h hh x hx)

#print axioms lower_covariant_variation
#print axioms actual_connection_variation_covariant
#print axioms covariant_variation_symmetric
#print axioms contracted_covariant_variation
#print axioms actual_palatini_current_covariant
end
end ChatgptAudit.SymmetricBoundaryR87
