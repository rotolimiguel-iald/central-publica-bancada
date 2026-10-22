[REAL — reprodução isolada e auditoria]
# A6.A — Pedra reproduzida
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`.

PAGO: fonte original copiada byte a byte, 28141 bytes,
SHA256 `35b91f86b88b8e6c498e8e18305e32ece6802a8e3bf1d6647e6fe75980774ca6`. Compilação rc0: 46 teoremas, 46 entradas auditadas,
somente axiomas do trio, zero erros/admissões e 15 avisos preservados.
Não houve necessidade da variante só-Mathlib. O olean não é usado como
critério de identidade entre caminhos.

Contorno: sete declarações existentes importadas e auditadas, todas dentro
do trio (duas sem axiomas). Este arquivo audita o olean disponível;
não recompila a fonte canônica do Contorno.

90 insumos do A6 conferidos contra o manifesto. Comandos completos,
fontes/logs/axiomas e recursos estão em A_reproducao/reproduction_manifest.json,
SHA256 `a8a746045585f27d555d747943d582e2a8983fc4ff353d59c615b55d5c89a76d`.
Reprodução: compile_isolated_v2.py kernel fonte label, fora do kernel;
auditar_axiomas.py fonte log. Fontes originais e kernel sem alteração.
Máquina 53.390176s parede / 53.296875s CPU, bancada não exclusiva;
estimativas remotas acumuladas US$0.2662637382, incompletas.

Não move gate. Trata-se de semigrupo dissipativo e conservação da leitura;
não é identificação com o fluxo modular nem uma prova do par físico H2/H3.
Segue B5 → B2a → B2b → B7 → B4 na ordem fixada.
