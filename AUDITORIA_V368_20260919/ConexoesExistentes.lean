import TGLExt.TheMasterFires
import TGLExt.StrongAssembly
import TGLExt.TheImportedEquilibrium

/- Audit adapters only. No reserved flag is introduced or changed. -/
namespace RouteAudit
open TGLExt
noncomputable section

def existingHorizon : HorizonEquilibriumData := theHorizon

def existingSmoothFrame : SmoothFrameData := qgStrongCertificate_frame.1

theorem existingFrameNonconstant :
    ∃ x y : Fin 4 → ℝ, existingSmoothFrame.E x ≠ existingSmoothFrame.E y :=
  qgStrongCertificate_frame.2

theorem existingFrameSuppliesLorentzAtEveryPoint (x : Fin 4 → ℝ) :
    (existingSmoothFrame.E x)⁻¹ * existingSmoothFrame.E x = 1 ∧
    LorentzByCongruence (solderMetric4 (existingSmoothFrame.E x)⁻¹) :=
  four_frame_gives_lorentz_metric _ (existingSmoothFrame.det_unit x)

theorem existingHorizonSuppliesThermalCoefficient :
    existingHorizon.dQ = existingHorizon.kappa * existingHorizon.dA /
      (8 * Real.pi * existingHorizon.G) :=
  the_master_fires.2.2.2

#check the_master_fires
#check qgImport_H3_localHorizonEquilibrium_bridged
#print axioms existingFrameNonconstant
#print axioms existingFrameSuppliesLorentzAtEveryPoint
#print axioms existingHorizonSuppliesThermalCoefficient
end
end RouteAudit
