# Revisão independente — rede Weyl, fluxo e ponte boost–carga

**PASSA no escopo condicional; nenhum achado material bloqueante.** Claim 845, Codex `/root/atrator_skeptic`. AUDITADA/FECHADA permanecem atos da gerência.

## O que a fiação efetivamente constrói [REAL]

R(W,K) é o bicomutante de W(K), com fecho por star derivado de `hstar`. Monotonicidade, localidade e covariância são transportadas dos geradores para a álgebra: a prova consome a monotonicidade do bicomutante, o colapso do triplo comutante e o transporte por equivalência. Não assume como entrada as conclusões R_mono/R_local/R_cov. A não comutatividade da álgebra exige um par não comutante de geradores.

O fluxo restrito é a conjugação por `gamma (B0 (−2πt))` no Fock concreto, restrita à álgebra da cunha. A invariância vem de `L.K_boost` e da covariância de W; inversa e composição são construídas. As leis de grupo não afirmam aqui continuidade, KMS ou identificação com o grupo modular do vácuo.

A ponte Maxwell começa com a identidade diferencial do boost real e sua carga integrada, no mesmo certificado C, forma Q e domínio. A reparametrização `−2πt` e a unicidade da derivada dão a carga modular `2πQ`; não se recebe `charge_link` pronto. O estado regular de carga não nula é hipótese nomeada; dele segue energia modular não nula. O tensor montado é literalmente `toStress Q` e coincide com Q no domínio. A extensão por zero fora dele já pertence à ponte herdada.

## Escopo e vacuidade

W concreto/CCR, um habitante da rede física, Q/Wick físico, identidade boost–carga e estado regular não nulo continuam por construir ou fornecer. O registro `Regular` exige norma 1; a hipótese de carga não nula exclui tensor sempre zero, mas não é uma construção de habitante. As três pontes tipam componentes compatíveis nas respectivas entradas; não exibem por si um único habitante físico conjunto. H3 é o da cunha padrão/direção fixa, sem afirmar família de Lorentz ou H3 curvo em toda direção.

## Recompilação independente

- `WeylNetWiringR1.lean`: EXIT 0, 69.518501 s, 16 declarações somente no trio; cópia exata e `.olean` idêntico ao aceito: True.
- `WeylFlowWiringR4.lean`: EXIT 0, 81.593238 s, 46 declarações somente no trio; cópia exata e `.olean` idêntico ao aceito: False.
- `MaxwellBoostChargeAssemblyR1.lean`: EXIT 0, 67.349809 s, 6 declarações somente no trio; cópia exata e `.olean` idêntico ao aceito: True.

No Flow, as 46 declarações incluem auxiliares gerados. Seu `.olean` difere em tamanho e contém o caminho distinto da fonte serializado junto ao aviso de linter (offset 313472). Os nomes e axiomas coincidem integralmente; não se alega identidade binária ou decodificação completa da diferença. Nota pinada: `FLOW_BINARY_NOTE_R1.json`.

Comandos, toolchain Lean 4.31.0, LEAN_PATH literal, início/fim, stdout/stderr, hashes antes/depois e `.olean` constam dos três recibos pinados pelo JSON. Tentativas recusadas do Flow não foram consumidas como evidência aceita. Não houve edição de fonte do construtor, memória, produção, dados ou gate.
