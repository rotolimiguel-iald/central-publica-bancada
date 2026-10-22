/-!
DECLARADO / UNCOMPILED replacement fragment, not a standalone module.
Use in a NEW copy of the existing R3 prefix, replacing only the theorem below.
The surrounding namespace/open declarations and regularSineWindow_val are required.
Do not import failed R2/R3 artifacts. Do not redefine or rebuild membership/CFC closure.
No extra hypotheses, spectral calculation, heartbeat increase, or new local instances.
The original theorem statement is preserved verbatim; only its proof body changes.
-/

theorem regularSineResolvent_eq_window_cfc (m : ℝ) :
    regularSineResolvent fockFlow m=
      cfc (fun z : ℂ=>(Real.sigmoid (m*(2*z.re-1)):ℂ)) (regularSineWindowCore m).val := by
  -- Freeze the carrier, predicate and CFC instance at this single application.
  let cfcFixed :
      (TGLV350.Regular.RegularHilbert F1Rede.BosonicFock.F →L[ℂ]
        TGLV350.Regular.RegularHilbert F1Rede.BosonicFock.F) →
      (TGLV350.Regular.RegularHilbert F1Rede.BosonicFock.F →L[ℂ]
        TGLV350.Regular.RegularHilbert F1Rede.BosonicFock.F) :=
    cfc (R := ℂ)
      (A := TGLV350.Regular.RegularHilbert F1Rede.BosonicFock.F →L[ℂ]
        TGLV350.Regular.RegularHilbert F1Rede.BosonicFock.F)
      (p := IsStarNormal)
      (instCFC := (inferInstance : ContinuousFunctionalCalculus ℂ
        (TGLV350.Regular.RegularHilbert F1Rede.BosonicFock.F →L[ℂ]
          TGLV350.Regular.RegularHilbert F1Rede.BosonicFock.F) IsStarNormal))
      (fun z : ℂ => (Real.sigmoid (m * (2 * z.re - 1)) : ℂ))
  have hspectral : regularSineResolvent fockFlow m =
      cfcFixed (regularSineWindow fockFlow m) :=
    regularSineResolvent_cfc fockFlow m
  have harg : cfcFixed (regularSineWindow fockFlow m) =
      cfcFixed (regularSineWindowCore m).val :=
    congrArg cfcFixed (regularSineWindow_val m).symm
  exact hspectral.trans harg
