# Parecer independente — ponte I05→I06, V2

**PASS — STATIC_REVIEW_ONLY.** Não foi localizado bloqueador remanescente no recorte após a correção do achado BRIDGE-01. Este parecer aceita a composição por inspeção; não autoriza execução, ratificação, abertura de dados ou uso científico dos doubles.

## Identidade e método

Revisor: chatgpt-codex/ordem018_preregistros; autor: ordem018_controller. Pacote final: f9_profile_decision_bridge_preparation_v2. Manifesto final lido: 9.435 bytes, SHA256 1f4bd38c8e7e3a204d2557fdcdfffaf7a8622bd0dabfc40c8677accea913a917. V1 preservada: manifesto 10.949 bytes, SHA256 7689dc4dc91ed3a717acd239c88afd298dde61f4545671a163ce9d88ce1fe19c.

[REAL — inspeção documental] Conferidos 20 membros e 17 fontes de V1, depois 15 membros e as mesmas 17 fontes de V2: 69 relações tamanho/hash, sem divergência. Os quatro Python da V2 foram analisados por AST, sem importação; a contagem estrutural encontrou 27 métodos de teste preparados. Nenhum teste, callback candidato, módulo científico, NumPy, solver, WSL, provedor ou dado observado foi executado/lido nesta revisão. Os recibos detalham os pins efetivamente lidos.

## Achado e fechamento

BRIDGE-01, P2, identificado no V1: profile_decision_bridge.py:195–206 só verificava o prazo antes de object_verifier; estimate_family:347–353 fazia essa chamada final e retornava sem outra checagem. Um recibo válido porém devolvido após o deadline permitiria resultado de engenharia tardio. Trata-se de checagem cooperativa ausente, não de exigência de hard realtime.

[REAL — delta estático] V2 insere self.checkpoint() na linha199, imediatamente após o callback e antes de aceitar o recibo. Removendo apenas esse nó da AST V2, a árvore restante é idêntica à V1. O caminho comum protege também a publicação final de estimate_family. O teste novo nas linhas371–387 prepara relógio e recibo falsos: a segunda chamada termina no deadline e deve falhar. Esse teste foi lido, não executado. Os 26 métodos anteriores permanecem idênticos em AST; o cabeçalho histórico foi esclarecido.

**BRIDGE-01: RESOLVED_BY_STATIC_DELTA.** A V1 selada permanece íntegra e não recebe aprovação retroativa de execução.

## Composição científica e matemática conferida

1. Família e identidade. Os 600 IDs únicos de frozen_contract são exatamente a sequência de family_metadata.family_labels; nenhuma deduplicação ou subconjunto. Os cinco modelos e os cinco testes/nulos coincidem com o contrato6b511. H1 é H1_TGL e H2 é H2_LCDM. A nomenclatura histórica invertida de outra tabela não é reutilizada. MODELS em profile/theta/assembler coincide; os limites/prior do domínio copiado coincidem com INTERFACE_CERTIFICADOS_F9 e o hash canônico DOMAIN foi recalculado.

2. Estimativas. estimate_family, V2:249–354, exige o plano completo600×(2^l+1)^3, nomes/ordem dos nós, hashes, proveniência, cinco modelos, estados e parâmetros do domínio. Preserva prior de fundo50/3 não aplicado e não integrado, sem priors extras na minimização. Aceita zero de suporte somente com os estados e a tag -inf previstos; falha desconhecida não é zero. Retorna ENGINEERING_ONLY e não promove mínimos da malha a L/U globais. O orçamento max_records é um requisito mínimo de completude, não medição de custo nem autorização de um nível.

3. L/U. _minimum e reduce_certificates, V2:356–486, distinguem ausência, erro não limitado e corrupção/identidade. A composição usa G_lower=max(0,L1), Q_lower=max(0,L1-U3) após inclusão qualificada, e T_j1_lower=Lj-U1. Grau é inteiro não booleano0..148; suporte, dominação, grau e inclusão exigem materiais vinculados e verificador semântico. L=0 analítico não produz U. d=0 com estatística positiva permanece INVALID. Ausência não é p=1; a cota trivial válida do módulo de cauda conserva seus pré-requisitos.

4. Normalização. A equivalência entre diferenças de q e2 diferenças de ellhat exige C, suporte afim e X comuns dentro de cada cenário, além das demais hipóteses do contrato. O componente não usa log da integral plana sobre eta como likelihood amostral nem acrescenta densidades/Jacobianos dos priors ao perfil. A medida comum kappa d eta pertence aos usos relativos de evidência na interface apropriada. A ponte não calcula lnB, evidência, sigma ou poder. A efetiva validade dessas hipóteses é obrigação do verificador externo, não conclusão de ler pins.

5. Limiar/log. threshold_audit.py:37–78 implementa a direção correta de Taylor, Machin e raízes inteiras. profile_decision_bridge.py:98–140 usa a série atanh normalizada e ceil em grade10^80 para obter log superior; nextafter é conferido por Fraction/as_integer_ratio. p=1 tem log0 exato. A nota PROVA_LIMIAR_RACIONAL.md fornece a derivação independente e os limites. Não foi repetida a conferência aritmética anterior nem avaliada a implementação nesta revisão.

6. Multiplicidade e estados. A ponte chama tail_upper por cenário/teste e o redutor uma vez, sem aggregate_bounds. threshold_audit.py:81–181 usa os p racionais originais, máximo somente da família completa e fator5 uma vez. Confere decisões por cenário, completas/robustas, direção, compatibilidade, comparações e estado final. Cruzamento de alpha ou divergência float deixa a decisão indisponível. A saída exata reconstitui racionais/booleanos/estados; p/log/exp float da proposta ficam diagnósticos. Não rejeição pelo majorante não prova p verdadeiro alto.

7. Autoridade. Os recibos tipados vinculam papel, payload, referências, verificador e escopo; um booleano não satisfaz a interface. Sem opening/admissão qualificada, o caminho permanece fechado. Na V2:516–529, SYNTHETIC_CONTROL_ONLY produz somente synthetic_decision e scientific_decision=None, mesmo no caso nominal. A fonte dos objetos e a verdade física dos certificados dependem de loader/verificador confiável ainda externo; flags/pins/doubles não os fornecem.

## Limites e próximo passo

[OPEN] A futura execução stdlib27 é qualificação de composição e recusas, não prova de solver, convergência, cobertura, certificados físicos ou funcionamento de supervisão real. Seu escopo proposto é um processo120s totais e1GiB, a ser controlado pela coordenação. Não executei esse comando nem criei AUTH/CLAIM/ROOT_DECISION.

[OPEN] A recepção dos materiais já alocados e os limites de tamanho constituem guardas da interface; não equivalem a limite de RAM agregado. O deadline é cooperativo, não preempção de callback bloqueado. Persistência, isolamento do loader, supervisão, orçamento e no-retry pertencem à integração futura. callbacks_executed=0 significa zero callbacks científicos/solver/perfil, conforme adendo V2; object_verifier é chamado.

A documentação atual separa domínio físico, estimativa finita, cota condicionada e veredito. Nenhum erro adicional de grau P2 ou superior foi localizado no recorte. A coordenação pode avaliar separadamente o ensaio stdlib delimitado sobre os pins V2; esta revisão não concede sua autorização e não altera d72/P3, fontes seladas, mapa, memórias ou ledger.
