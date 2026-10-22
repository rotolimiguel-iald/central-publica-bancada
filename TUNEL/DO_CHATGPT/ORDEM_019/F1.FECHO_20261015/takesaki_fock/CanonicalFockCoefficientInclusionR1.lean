import CanonicalFockCoefficientIntervalsR2
import CoefficientFockPointwiseR1
import RealTomitaGraphDenseR1
/-! The full closed coefficient Tomita graph embeds in the actual dual-weight
GNS Tomita graph. This is one inclusion only: the reverse inclusion needs
actual regularization and is not inferred from involutivity or covariance. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace F1Fecho.CanonicalFockCoefficientInclusion
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Rede.CanonicalWedge
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockCoefficientGNS F1Fecho.CanonicalFockCoefficientIntervals
open F1Fecho.CanonicalFockPolar F1Fecho.ExponentialTomita F1Fecho.ExponentialLift
open F1Fecho.CoefficientFockConjugation F1Fecho.WedgePairTomita
open TGLV350.Regular ChatgptAudit.Continuous050 ORDEM016.D6

 def basePairs : Set (LpPairTransport.PairH F) :=
  (WithLp.ofLp : LpPairTransport.PairH F→F×F) ⁻¹' pairTomitaGraph (algebra KWR) vacuum

 theorem basePairs_dense : closure basePairs=
    (RealTomitaGraph.graph (resolventSquareRoot modularR modularR_nonneg modularR_injective) JF:
      Set (LpPairTransport.PairH F)) := by
  apply RealTomitaGraph.dense_pair_graph
  calc
    closure (pairTomitaGraph (algebra KWR) vacuum)=CoefficientTomitaSquare.graph canonicalLift JF := actualGraph_eq
    _=CoefficientTomitaSquare.graph (resolventSquareRoot modularR modularR_nonneg modularR_injective) JF :=
      congrArg (fun T=>CoefficientTomitaSquare.graph T JF) CoefficientFockPointwise.base_root_eq.symm

 theorem base_interval_mem (a b:ℝ) (v:LpPairTransport.PairH F) (hv:v∈basePairs) :
    LpPairTransport.decode fockFlow (RealLpGraphCore.intervalVector a b v)∈coefficientGraph := by
  obtain ⟨A,hA,hv'⟩ := hv
  rw [CoefficientGraphCore.decode_interval,hv']
  exact interval_pair_mem A hA a b

 theorem coefficient_graph_into_GNS (f g:RegularHilbert F)
    (hfg:(f,g)∈CoefficientTomitaSquare.graph coefficientRoot coefficientJ) :
    (coefficientEmbedding f,coefficientEmbedding g)∈RegularScalarRealGraph.closedGraph weightContext := by
  apply (coefficientGraph_mem f g).mp
  exact CoefficientGraphCore.coefficient_mem_of_dense_intervals
    modularR modularR_nonneg modularR_le_one modularR_injective
    fockFlow JF F1Fecho.Antilinear.canonicalFockJ_involutive JF_boost
    basePairs basePairs_dense coefficientGraph coefficientGraph_closed base_interval_mem f g hfg
end F1Fecho.CanonicalFockCoefficientInclusion
#print axioms F1Fecho.CanonicalFockCoefficientInclusion.basePairs_dense
#print axioms F1Fecho.CanonicalFockCoefficientInclusion.base_interval_mem
#print axioms F1Fecho.CanonicalFockCoefficientInclusion.coefficient_graph_into_GNS
