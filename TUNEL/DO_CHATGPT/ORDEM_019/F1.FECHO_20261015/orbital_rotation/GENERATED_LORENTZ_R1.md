# Representação escalar do subgrupo de Lorentz gerado — candidato R1

[REAL — compilado em sandbox; revisão independente pendente.]

## Construção

- The subgroup generated in the actual LorentzGrp by all real spatial orthogonal transformations and the longitudinal boost is constructed. Every element and inverse has a measure-preserving mass-shell lift, proved by subgroup closure.
- The explicit action shellAction(L,p)=momentumOf(L*shellMomentum(p)) agrees almost everywhere with every such lift. Injectivity of shellMomentum proves uniqueness, so mixed words giving the same Lorentz matrix give the same L2 operator.
- Inverse pullback on the original H1 is a genuine LinearIsometryEquiv and a group homomorphism. Its spatial and longitudinal generators are exactly the existing scalarOrthogonalH1 and B0, not merely isomorphic copies.
- The Lorentz group and generated subgroup carry the induced matrix topology. Strong continuity is proved with the explicit continuous pullback family and local regularity of the existing orbital measure.
- The representation satisfies actual U1 translation covariance for every element, and the resulting representation of the semidirect Poincare subgroup has the correct product law.

## Alcance

- This receipt does not assert that the generated subgroup exhausts all future Lorentz transformations. The decomposition is subsequent work and not silently included here.
- Spatial generators include orthogonal reflections. The action is scalar on both complex coordinates, not the induced photon helicity representation. The name H1 is the unchanged canonical type and does not by itself fix physical helicity.
- CanonicalNetInput receives no completed field: a global K with isotony, locality, translation/boost covariance and the exact wedge_glue still needs construction. Operator covariance alone is not net covariance.
- PhotonCharacterCocycle.screen_phase_cocycle is reusable but still requires its explicit ScreenOrientationMeasured obligation; F1.3 also records the global-helicity obligation. Neither is discharged by this scalar representation.
- Independent review is pending with the parent; all production, canonical memory and the gate stay unchanged.

## Evidência

Quatro compilações aceitas, incluindo auditor de todas as 73 declarações locais (privadas e auxiliares incluídas), só o trio; zero sorry nas fontes aceitas. As 13 tentativas recusadas estão preservadas e pinadas no recibo. Comandos, LEAN_PATH literal, início/fim, segundos e saída estão nos recibos de cada tentativa.

A construção reaproveita orbitalMeasure, energia, orbitalTranslation e U1 canônicos. Nenhuma invariância de medida é premissa adicionada ao resultado: ela decorre da carta euclidiana, da preservação de volume e da invariância da energia.
