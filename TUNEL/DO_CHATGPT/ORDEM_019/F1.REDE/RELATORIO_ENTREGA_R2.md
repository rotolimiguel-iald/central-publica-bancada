# F1.REDE — etapa R2: conjugação geométrica e Fock concreto

Autor operacional: codex-gerente-tgl. Base: v392 autorizada pelo operador. Unidade permanece EM_CURSO; entrega de etapa em sandbox.

## Avanço verificado

[REAL — sandbox e revisão independente] A conjugação espectral J_W coincide com a ação geométrica que reflete o momento transversal, preserva a rapidez, conjuga e troca as helicidades. Também vale J_W U1(a) J_W = U1(j_W a), com j_W = diag(−1,−1,+1,+1). A igualdade usa o U1 canônico.

[REAL — sandbox e revisão independente] Construídos os setores H_n como fechos dos spans de x tensorizado n vezes, sua soma de Hilbert F = ⊕_n H_n, o vácuo normalizado, uma família ortonormal infinita e o funtor Γ(u) = ⊕_n Γ_n(u). A inclusão ι do H1 canônico é isométrica e Γ(u)ι = ιu. Γ preserva identidade, composição e vácuo.

[REAL — sandbox e revisão independente] A continuidade forte de Γ é derivada da continuidade no H1, para qualquer espaço de parâmetros. A prova usa continuidade dos tensores puros, fecho das órbitas contínuas e convergência dominada na soma, com majorante 4‖f_n‖². As translações de quatro parâmetros e os boosts canônicos são contínuos no Fock. Suas leis de grupo e covariância por conjugação também foram transportadas.

São 14 recompilações independentes nesta R2, incluindo os auditores de axiomas: EXIT 0, somente propext, Classical.choice e Quot.sound, zero sorry. Construtores e revisor são agentes distintos. Contagens e comparações de .olean estão nos recibos; não se afirma identidade binária de todos os .olean. Tentativas falhas e fontes de cada tentativa foram conservadas.

## Correspondência com o contrato

A matriz `MATRIZ_CONTRATO_FOCK_R2.json` fornece arquivo, linha e hash de cada objeto/teorema que preenche a parte cinemática do FockCertificate v392. As hipóteses de continuidade não foram simplesmente deslocadas para os setores: foram provadas a partir do H1. A formulação por fecho do span dos poderes diagonais é a usada nesta construção. Sua equivalência com a apresentação geral por fixos de todas as permutações não foi formalizada aqui; o setor 2 separado já possui a construção por fixos do flip.

## O que permanece aberto

- Rede 4D com ação completa de Poincaré, independência da escolha da cunha e localização global. O resultado atual cobre a cunha-padrão, a rede de semirretas e os fluxos explicitados.
- Operadores W(f), relações CCR e álgebras R(K) = {W(f): f ∈ K}''; propriedades cíclica/separante do vácuo e realização modular da mesma álgebra.
- Preservação geral do espectro positivo, unicidade do vácuo e segunda quantização antiunitária exigidas pelo registro completo.
- Núcleo de Takesaki ligado à representação construída; o resultado V351 de escala/traço continua reaproveitado, mas não substitui essa identificação.
- Forma de Maxwell concreta, estado regular não nulo e ligação à energia modular. A extensão por zero já está em MaxwellLiteratureBridge e será reaproveitada.
- A implicação Einstein no atlas já existente continua condicional ao H3 nomeado; este trabalho não deriva o H3 do estado nem constrói solução global. O refinamento dispositivo→rede contínua também não é concluído aqui.

Não existe nesta entrega um habitante do FockCertificate completo nem do MaxwellCertificate. Construir parte dos campos não permite inferir os demais.

## Diário e continuidade

O diário vivo é `memory/DIARIO_CONSTRUCAO_QG.md`. Cada etapa material recebe fontes e estatutos; a escrita é aditiva, com backup imediato de bytes e retratos imutáveis em `diary_events`. O Atlas permanece a referência conceitual. Isso não instala memória nos pesos nem cria automação.

Os 323 artefatos da entrega R1 foram relidos e permanecem byte a byte iguais. Novas evidências têm nomes próprios. Próxima etapa matemática: construir W(f) e a rede de álgebras sobre este Fock, usando os objetos já construídos; não repetir Fubini, J, setores ou continuidade.

Nenhuma chamada de provedor foi repetida. Kimi/Takesaki continua com sua autorização específica pendente. Nenhuma implantação em um.py, kernel, Bancada ou gate; nenhum dado observado foi aberto. A revisão técnica local não substitui a auditoria/ratificação da gerência.
