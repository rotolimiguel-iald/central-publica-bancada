import GeneralSineResolventApproxR2
import GenericModularCutToolsR1
/-! CFC and bounded-strong transport for the actual regular generator in any
representation of its core. Strong continuity and commutation are explicit
premises, to be discharged by the concrete Fock GNS representation. -/
set_option autoImplicit false
set_option quotPrecheck false
set_option maxHeartbeats 150000
noncomputable section
namespace F1Fecho.RepresentedRegularResolvent
open TGLV350.Regular MeasureTheory Filter
open F1Fecho.RegularPositiveFlow F1Fecho.RegularCovariantCore
open scoped Topology
variable {H K : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable [NormedAddCommGroup K] [InnerProductSpace ℂ K] [CompleteSpace K]
local instance : NormedSpace ℂ (K →L[ℂ] K) := inferInstance
local instance : Module ℂ (K →L[ℂ] K) := ContinuousLinearMap.module
local instance : ContinuousFunctionalCalculus ℂ (K →L[ℂ] K) IsStarNormal :=
  IsStarNormal.instContinuousFunctionalCalculus (A := K →L[ℂ] K)
local instance : IsometricContinuousFunctionalCalculus ℂ (K →L[ℂ] K) IsStarNormal :=
  IsStarNormal.instIsometricContinuousFunctionalCalculus (A := K →L[ℂ] K)
local instance : SMulCommClass ℂ (K →L[ℂ] K) (K →L[ℂ] K) := ⟨by
  intro c a b
  ext1 x
  change c • a (b x) = a (c • b x)
  exact (a.map_smul c (b x)).symm⟩
local instance : IsScalarTower ℂ (K →L[ℂ] K) (K →L[ℂ] K) := ⟨by
  intro c a b
  ext1 x
  rfl⟩
variable (Q : UnitaryFlow H) (M : VonNeumannAlgebra H)
local notation "N" => (F1Fecho.RegularCovariantCore.core Q M).toStarSubalgebra
variable (π : N →⋆ₐ[ℂ] (K →L[ℂ] K))

def groupElement (t : ℝ) : N :=
  ⟨F1Fecho.RegularCovariantCore.regularUnitary Q t,regular_mem Q M t⟩

def resolventElement : N :=
  ⟨F1Fecho.RegularPositiveFlow.regularSpectralResolvent Q,
    F1Fecho.RegularPositiveFlow.regularSpectralResolvent_mem Q M⟩

def windowElement (m : ℝ) : N :=
  (1/2 : ℂ) • 1 + (1/(4*Complex.I) : ℂ) •
    (groupElement Q M (-1/m)-groupElement Q M (1/m))

theorem windowElement_val (m : ℝ) : (windowElement Q M m).val =
    F1Fecho.RegularPositiveFlow.regularSineWindow Q m := rfl

private theorem core_closed : IsClosed (N : Set (RegularHilbert H →L[ℂ] RegularHilbert H)) := by
  change IsClosed (F1Fecho.RegularCovariantCore.core Q M : Set (RegularHilbert H →L[ℂ] RegularHilbert H))
  rw [← VonNeumannAlgebra.centralizer_centralizer (F1Fecho.RegularCovariantCore.core Q M)]
  exact Set.isClosed_centralizer _


set_option diagnostics true
set_option pp.universes true
#check π
#check π.toFun
#check π.toFun (groupElement Q M 0)
#check (π : N → (K →L[ℂ] K))
def represented (a : N) : K →L[ℂ] K := π.toFun a
#check represented Q M π (groupElement Q M 0)
end F1Fecho.RepresentedRegularResolvent
