# Revisão independente do setor OH

[REAL] PASSA no modelo finito configurado: 30/30 verificações reproduzidas. Nenhum achado material.

β calculado em runtime: 0.012031300400803142; ω = 10476325570.593649 s⁻¹; γ_raiz = 63021910.01821379 s⁻¹; γ_φ = 31510955.009106897 s⁻¹.

A reprodução usa superoperadores por produtos de Kronecker, autovalores e canal analíticos. As tolerâncias do pré-registro foram preservadas (1e-12 e controles negativos ≥0,1). Os pinos e a cronologia local do congelamento conferem; a correção do parser R1→R2 não alterou a política numérica.

- gamma_phi=beta*omega/4 is configured INPUT required for equality; this is not a measured dephasing rate or an independently derived full-device prediction.
- The effective OH excitation Hamiltonian is positive with its stated energy zero. Center removal is valid for its commutator only, not for its square-root dissipator.
- The prior device rate in its dimensionless clock fails matching, Rabi noncommuting jump fails matching, and shifting energy zero changes root dissipation as required.
- The R1 refusal preceded matrix construction; R2 changed the source extraction window and output names, not numeric criteria or parameters.
- This reproduces finite-model identities, not hardware, observed data, thermal calibration, kappa or nature confirmation. No production, memory or gate modified.

Recibo, hashes e valores: REVISAO_OH_R1.json.
