import OrbitalSpatialUnitaryR3
import OrbitalQuarterTurnR4

/-! A spatial quarter-turn covariantly rotates the already existing four
translations on the unchanged H1. This pays scalar orbital covariance; no
photon-helicity cocycle, locality or global standard-subspace net is inferred. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
open MeasureTheory Filter
namespace F1Fecho.OrbitalSpatial
open ChatgptAudit.WignerRapidityMeasure016 ChatgptAudit.WignerOrbit016

theorem quarterTurn_inverse_coordinates (p : MomentumCoordinates) :
    spatialAction quarterTurn.symm p = (![-p.2,p.1 1],p.1 0) := rfl

def quarterTurnSpacetime (a : Fin 4→ℝ) : Fin 4→ℝ :=
  ![a 0,-a 2,a 1,a 3]

theorem quarterTurn_phase (m : ℝ) (a : Fin 4→ℝ) (p : MomentumCoordinates) :
    orbitalPhase m a (spatialAction quarterTurn.symm p) =
      orbitalPhase m (quarterTurnSpacetime a) p := by
  unfold orbitalPhase
  apply congrArg phase
  unfold orbitPairing shellMomentum
  have he := spatialAction_energy quarterTurn.symm m p
  simp only [Matrix.cons_val_zero,Matrix.cons_val_one,Matrix.cons_val_two,
    Matrix.cons_val_three,Matrix.head_cons,Matrix.tail_cons]
  rw [he,quarterTurn_inverse_coordinates]
  simp [quarterTurnSpacetime,Matrix.cons_val_two,Matrix.cons_val_three,
    Matrix.head_cons,Matrix.tail_cons]
  ring

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]

theorem spatialQuarter_translations (m : ℝ) (a : Fin 4→ℝ)
    (f : Lp E 2 (orbitalMeasure m)) :
    spatialUnitary m quarterTurn (orbitalTranslation m a f) =
      orbitalTranslation m (quarterTurnSpacetime a) (spatialUnitary m quarterTurn f) := by
  have htr := (spatialAction_orbital quarterTurn.symm m).quasiMeasurePreserving.ae
    (orbitalTranslation_ae m a f)
  apply Lp.ext
  filter_upwards [spatialUnitary_ae m quarterTurn (orbitalTranslation m a f),htr,
    orbitalTranslation_ae m (quarterTurnSpacetime a) (spatialUnitary m quarterTurn f),
    spatialUnitary_ae m quarterTurn f] with p h1 h2 h3 h4
  rw [h1,h2,h3,h4,quarterTurn_phase]

theorem scalarSpatialH1_quarter_U1 (a : Fin 4→ℝ) (f : TGLExt.ImportedSQ.H1) :
    scalarSpatialH1 quarterTurn (TGLExt.ImportedSQ.U1 a f) =
      TGLExt.ImportedSQ.U1 (quarterTurnSpacetime a) (scalarSpatialH1 quarterTurn f) :=
  spatialQuarter_translations 0 a f

theorem scalarSpatialH1_quarter_conjugates_U1 (a : Fin 4→ℝ)
    (f : TGLExt.ImportedSQ.H1) :
    scalarSpatialH1 quarterTurn
      (TGLExt.ImportedSQ.U1 a ((scalarSpatialH1 quarterTurn).symm f)) =
        TGLExt.ImportedSQ.U1 (quarterTurnSpacetime a) f := by
  rw [scalarSpatialH1_quarter_U1,LinearIsometryEquiv.apply_symm_apply]

end F1Fecho.OrbitalSpatial
#print axioms F1Fecho.OrbitalSpatial.quarterTurn_phase
#print axioms F1Fecho.OrbitalSpatial.spatialQuarter_translations
#print axioms F1Fecho.OrbitalSpatial.scalarSpatialH1_quarter_U1
#print axioms F1Fecho.OrbitalSpatial.scalarSpatialH1_quarter_conjugates_U1
