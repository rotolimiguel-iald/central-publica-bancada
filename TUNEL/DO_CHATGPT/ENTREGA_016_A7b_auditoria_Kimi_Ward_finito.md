[REAL — auditoria CAS; DERIVED — recorrência escalar; DECLARADO — parecer externo]
# A7.b — revisão da contribuição Kimi finite_two_point_ward_contact
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T06:44:11.398178+00:00.
Job `7ed451ee-e554-4667-9d52-86c0f7c3c55b`, modelo kimi-code/k3. O original foi preservado
integralmente. Uso informado: {'prompt_tokens': 318267, 'completion_tokens': 75714, 'cached_input_tokens': 0, 'total_tokens': 393981}. Assinatura: sem cobrança
incremental estimada aqui. Nenhuma repetição da chamada.

**Aproveitado:** recorrências dos contatos de potências puras e mudança de
referência escalar. Para U_n=z^-n e D_n=Box^(n-2)R(U2)/
[4^(n-2)(n-1)!(n-2)!], na referência plana:

    R(U_n)-D_n = [H_(n-1)+H_(n-2)-1] Res(U_n),
    R(U3)-D3 = -3 C Box delta/64,
    R(U4)-D4 = -7 C Box² delta/2304.

A recorrência foi confrontada com o motor meromorfo já auditado, n2..8.
É uma conversão escalar PLANA; ainda não é transporte da amplitude curva.

**Erros medidos e limites:**
- Script recebido: 24 PASS, 1 FAIL, rc1. T7 deixa D3-D2, símbolos
  independentes; usou D3 onde a identidade para zD3 pede D2. A identidade
  distribucional multiplicativa não é refutada por esse erro no teste.
- A substituição Riem1²=2Ric1²-R1²/3 módulo derivada total está incorreta.
  No controle transversal h12=h21=1, p=e0: Riem1²=2, Ric1²=1/2, R1=0;
  a fórmula proposta erra por 1. A combinação de Euler é 4Ric1²-R1².
- Pi G=0 não substitui a STI completa com fonte antifield e tadpole.
- Localidade sozinha não demonstra que uma quebra está na imagem BRST.
  Calculamos algo mais limitado: a matriz Ward do símbolo plano simétrico
  de cinco coeficientes tem posto3 e núcleo2. Os dois quadráticos covariantes
  Ric1² e R1² são Ward-neutros; não cancelam uma quebra não nula por si sós.
- Ric1(G)=R1(G)=0 não demonstra Wess–Zumino para a quebra calculada.
  h*local h, tal como escrito sem ghost, tampouco tem grau de ghost zero.

Auditoria própria v2: 51 verificações, rc0, CPU3.046875s.
A v1 local falhou por confundir resíduo de x_i U com q_i Res(U)/q² na
expressão esperada; foi corrigida em arquivo novo. Fonte/log v1 preservados.
Uma tentativa de gerar v2 por comando PowerShell falhou na interpretação
de aspas antes de criar o arquivo; substituída por preparador em arquivo.

O Kimi deixou L1/L2, curvatura e anomalia integral abertos. A bancada já
possui cálculos posteriores para parte desses itens; isso não retroage
ao pacote recebido pelo revisor. Parecer incorporado apenas neste escopo.
