import ContratoQG
import TGLExt.ModularFlowSpectrum

set_option autoImplicit false

/-!
# W5ParedeEspectral — a cláusula (S) do ANEXO A força ESPECTRO PONTUAL em Δ^{it}
  (frente W5_final, 23/09/2026; scratchpad; NÃO cunha nome reservado; NÃO entra no kernel nesta sessão)

  O `ContratoH2` de W2_final (02fd013827dca251) exige, na cláusula (S), uma isometria
  `stateIso : TowerHilbert profile ≃ₗᵢ[ℂ] W.H` que ENTRELAÇA o fluxo modular da torre com `Δit`
  (`state_flow`). O kernel já prova que o fluxo da torre tem uma família TOTAL de autovetores
  (`modularFlow_eigenvector`, `localEigenvectors_total`, ModularFlowSpectrum.lean). Logo:

  `contratoH2_forces_point_spectrum` [DERIVED]: em todo habitante do contrato, `Δit` tem autovetores
  FORA da reta do vácuo — senão W.H teria dimensão ≤ 1, contra `R.infiniteHilbert`.

  Leitura [KNOWN — não formalizado aqui]: na rede do escalar livre, Bisognano–Wichmann dá
  Δ^{it} = U(Λ(−2πt)), e o boost não tem autovetor fora de ℂΩ (espectro absolutamente contínuo no
  complemento do vácuo). Portanto, com a cláusula (S) como está, o ANEXO A é VAZIO no par físico
  que a partição M01 descreve (FORMA II sob H_rede) — e só é habitável por pares de espectro pontual
  (torres; ver ProbeToyContratoH2). É a «parede funda» do antigo A3.5 (fluxo com espectro pontual
  × boost com espectro de Lebesgue), agora como TEOREMA sobre o tipo, condicionado ao [KNOWN].

  Estatutos: [DERIVED] o teorema; [KNOWN] o espectro do boost livre; [OPEN] a correção de (S)
  (quem a redige é a gerência/frente W2). β não aparece. Sem sorry, sem axiom.
-/

namespace W5Final.Espectral

open TGL.SpecificAQFT TGL.ModularRealization ChatgptAudit
open TGLExt TGLExt.ContratoQG

noncomputable section

/-- «Δit não tem autovetor fora da reta do vácuo» (o caso do boost livre, [KNOWN]). -/
def NoEigenOutsideVacuum (W : TGLSpecificAQFTWitness) (D : ℝ → (W.H ≃ₗᵢ[ℂ] W.H)) : Prop :=
  ∀ (v : W.H) (r : ℝ), (∀ t : ℝ, D t v = modularPhase t r • v) → v ∈ (ℂ ∙ W.vac)

/-- [DERIVED] ★★ a cláusula (S) do contrato força espectro pontual: nenhum habitante de `ContratoH2`
    tem `Δit` sem autovetores fora de ℂ·vácuo. -/
theorem contratoH2_forces_point_spectrum {W : TGLSpecificAQFTWitness}
    {R : TGLModularRealization W} (C : ContratoH2 W R) :
    ¬ NoEigenOutsideVacuum W C.Δit := by
  intro hno
  set P := C.profile
  set S : Submodule ℂ W.H := ℂ ∙ W.vac with hS
  -- (1) a imagem de cada autovetor da torre cai na reta do vácuo
  have heig : ∀ (N : ℕ) (i j : chainIdx N), C.stateIso (localEigenvector P N i j) ∈ S := by
    intro N i j
    refine hno _ (Real.log (localEigenvalue P N i j)) (fun t => ?_)
    rw [← C.state_flow]
    change C.stateIso (modularFlow P t (localEigenvector P N i j)) = _
    rw [modularFlow_eigenvector, LinearIsometryEquiv.map_smul]
  -- (2) logo o span dos autovetores também
  have hspan : ∀ x ∈ Submodule.span ℂ (localEigenvectors P), C.stateIso x ∈ S := by
    intro x hx
    induction hx using Submodule.span_induction with
    | mem x hx =>
      obtain ⟨N, i, j, rfl⟩ := hx
      exact heig N i j
    | zero => rw [map_zero]; exact S.zero_mem
    | add x y _ _ hxe hye => rw [map_add]; exact S.add_mem hxe hye
    | smul c x _ he => rw [LinearIsometryEquiv.map_smul]; exact S.smul_mem c he
  -- (3) densidade + S fechado ⟹ S = tudo
  have hclosed : IsClosed (S : Set W.H) := Submodule.closed_of_finiteDimensional S
  have hall : ∀ w : W.H, w ∈ S := by
    intro w
    have hx : C.stateIso.symm w ∈
        closure (Submodule.span ℂ (localEigenvectors P) : Set (TowerHilbert P)) :=
      localEigenvectors_total (P := P) _
    have himg := mem_closure_image C.stateIso.continuous.continuousAt hx
    rw [LinearIsometryEquiv.apply_symm_apply] at himg
    have hsub : C.stateIso '' (Submodule.span ℂ (localEigenvectors P) : Set (TowerHilbert P))
        ⊆ (S : Set W.H) := by
      rintro _ ⟨x, hx, rfl⟩
      exact hspan x hx
    exact hclosed.closure_subset_iff.mpr hsub himg
  -- (4) então W.H tem dimensão finita — contra a realização
  have hsurj : Function.Surjective (S.subtype) := fun w => ⟨⟨w, hall w⟩, rfl⟩
  have : FiniteDimensional ℂ W.H := Module.Finite.of_surjective S.subtype hsurj
  exact R.infiniteHilbert this

/-- [DERIVED] ★★ a forma de parede: num par em que o implementador de qualquer habitante — i.e. um
    unitário que implementa o fluxo modular de R e fixa o vácuo (campos (Δ)) — não tem autovetores
    fora do vácuo (o caso físico: o implementador é único e é o boost de BW, [KNOWN]), o contrato do
    ANEXO A é VAZIO. A hipótese é sobre `C.Δit`, não sobre todo unitário (a identidade tem autovetores). -/
theorem contratoH2_empty_of_no_point_spectrum (W : TGLSpecificAQFTWitness)
    (R : TGLModularRealization W)
    (h : ∀ C : ContratoH2 W R, NoEigenOutsideVacuum W C.Δit) :
    IsEmpty (ContratoH2 W R) :=
  ⟨fun C => contratoH2_forces_point_spectrum C (h C)⟩

#print axioms contratoH2_forces_point_spectrum
#print axioms contratoH2_empty_of_no_point_spectrum

end

end W5Final.Espectral
