# Revisão independente R1 — F8.2.SN1

09/10/2026. Autoria: codex/sn_skeptic, delegado pela gerente TGL, sob reivindicação 610. Nenhuma aprovação c1 é reivindicada.

## Veredito

**[REAL, verificação local] PASS_CONDITIONAL_CALCULATIONS_NO_PHYSICAL_SIGMA.** Recomputação independente das expressões numéricas e leitura do relatório: nenhum erro material encontrado. O escopo declarado é adequado. Isso aprova os controles condicionais examinados; não prova um sinal TGL estelar, habitante formal, teste da natureza ou cinco sigmas.

## O que foi conferido

- Alfa foi extraído novamente dos bytes do um.py por atribuição literal ancorada; o arquivo foi apenas lido, nunca importado/executado. O SHA atual coincide com o da entrega. Beta runtime é 0,012031300400803142.
- A expressão de Coulomb foi lida diretamente nas Eq.37–38 do HTML custodiado de Chamel et al.; Eq.6–7 sustentam a relação pressão–energia. Recomputação por diferenças de logaritmos reproduz os quatro deslocamentos não nulos e as derivadas. Carbono: −0,0228387389% e −0,1141763035%; oxigênio: −0,0277562845% e −0,1387557349%. Os multiplicadores de alfa são hipóteses uniformes de sensibilidade, não running estelar derivado. O sinal deste termo não decide o sinal eletrofraco completo.
- A estimativa RicciFF foi recalculada pela forma expandida 8πβℏG²ρ/c⁵, sem reutilizar intermediários do produtor. Os extremos 5,86592524e−87 e 5,86592524e−85 conferem. As linhas 575–585 do Tratado foram lidas para conferir operador e convenção não reduzida de Planck. Isso mede o coeficiente dimensional; não limita diretamente ΔL/L.
- O dephasing foi recalculado pela solução espectral, sem funções do produtor. Conserva energia=1 e populações=1/3, reduzindo pureza. A identidade analítica Tr(H[H,[H,ρ]])=0 exige aqui H fixo e saltos comutantes; não demonstra ∇T local num sistema estelar dinâmico. O relatório preserva essa restrição.
- Contagens gaussianas independentes com Decimal: 2.500/250.000 para separação mediana; 3.946/394.579 para poder90% unilateral. São exemplos com amplitude, ruído e modelo de referência estipulados. Não representam amostra selecionada nem previsão TGL. Um sinal constante está no espaço de um intercepto livre e não é identificável nessa comparação; Z²=0 está correto.
- Os nulls físicos deltaP/deltaYe/deltaL/sigma são ausência de cálculo, expressamente separados de zero físico. O relatório mantém essa distinção e não promove a correção padrão Coulomb a evidência exclusiva TGL.

## Limitações e ressalvas menores

1. O relatório e o levantamento explicam corretamente que a curva beta(chi) exige matching com matéria; a inversão de alfa não mede chi na estrela. A definição de uma fonte dinâmica para chi é necessária para uma conservação covariante autossuficiente.
2. Uma SN Ia ordinária/anã branca não possui horizonte de eventos no modelo de progenitor padrão. Schwarzschild de vácuo é um controle exterior idealizado; não é a solução interior nem a explosão. A formulação final deve preservar a distinção já declarada no relatório.
3. A proposta temporal L(t)/integral(tL) cancela a normalização, mas a previsão TGL da forma ainda não existe nesta entrega; hipóteses de expansão/energia e composição precisam permanecer explícitas.
4. A docstring de calculate_r2.py ainda exemplifica o nome calculate_r1.py. É detalhe editorial, sem efeito na execução ou resultados; não exige reabrir a camada numérica.
5. A revisão não recompilou Lean nem reproduziu MESA/artigos de explosão. Fonte bibliográfica custodiada e consistência de fórmulas não equivalem a validação estelar. As leituras iniciais do Tratado foram recusadas pelo sandbox; a releitura autorizada posterior e a recomputação concluíram exit0. Nenhum arquivo original foi alterado.

## Reprodutibilidade

Executável independente: independent_review_r1.py. Recibo: INDEPENDENT_CHECKS_R1.json. O módulo do produtor nunca foi importado. Novas saídas somente nesta pasta; sem memória, quadro, mapa, Bancada ou provedor externo. Pinos desta revisão:

- `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F8.2.SN1\review\INDEPENDENT_CHECKS_R1.json`: `fd82956e38f5f3489f27a07d557056e96c4d48a21c615a11352eae48710896e1` (5939 bytes).
- `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F8.2.SN1\review\independent_review_r1.py`: `e49bb10f5dfad9ebbd1ed06799e6cdddfdc12bda56b031e8d88ee63857e5ddba` (4836 bytes).
- `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F8.2.SN1\RELATORIO_VIABILIDADE_R1.md`: `ccdd09e4698b3907285aba55abe6e3c6d477f77a16134ee38ace932d6fec2f06` (12436 bytes).
