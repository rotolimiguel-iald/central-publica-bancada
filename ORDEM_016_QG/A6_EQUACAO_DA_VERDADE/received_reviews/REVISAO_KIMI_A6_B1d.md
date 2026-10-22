[DERIVED — revisão escrita; DECLARADO — candidatos Lean; OPEN — compilação do limite forte]
# Revisão Kimi A6.B1d

Abertura sha256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`.
Resposta lida inteira: `93c0358f-04f8-4bea-a4d6-6977171d6fed.md`, sha256 `bb51bf9da6ac2208913ddd3b74bb2ef5e64aed7bdbe1419bac40fbc1cb59838a`.
Fonte de definições lida: `TheEquationOfTruth_T20_v3.lean`, sha256 `a02ec47f3cac151f017989339c24a0d4677d2c753aece809004e5568901e6f64`.
T/flow nas linhas174–177 não pressupõem dimensão finita; reading nas linhas182–183
é a projeção ortogonal do kernel; FlowTendsToFamily nas linhas299–300 é convergência
para cada vetor. Isso confirma a tipagem que o executor inferiu.

A rota por densidade é coerente para H limitado, positivo e auto-adjunto em
Hilbert completo: ran(H)^perp=ker(H), logo closure(ran(H))=ker(H)^perp.
Das cotas ||exp(−sH)||<=1 e ||exp(−sH)H||<=1/(e s), para z nesse fecho,
escolhe-se Hy a distância <epsilon/2 de z e s>2||y||/(e epsilon).
Então ||exp(−sH)z||<epsilon. A parcela na projeção permanece fixa.
As cotas espectrais precisam ser demonstradas no formalismo Lean, não assumidas
como nomes de API. O texto recebido não contém corpos Lean nem compilação.

Correções: a afirmação de que CFC não produz o candidato é excessiva. No próprio
diag(1/n), a projeção é 0, que é CFC da função zero; o que falha é a convergência
uniforme das exponenciais. Sem gap significa ausência de taxa uniforme em norma,
não ausência de toda taxa para um vetor. H=0 deve ser tratado separadamente quando
se escreve mínimo do espectro positivo vazio. A rota de Vigier exige cotas para
s,t>=0; não se deve aplicar 0<=T_s−T_t<=I para tempos negativos.

A auditoria local anterior já havia localizado a passagem por densidade como
pendência. A resposta desenvolve sua prova escrita, sem substituir a compilação
nem pagar B1d. Nenhum novo ciclo Lean foi gasto nesta revisão, nenhum gate alterado.
Execução única 2589ad40-f3aa-498a-9996-4f16cd0aa9e7; metadados preservados no recibo JSON.
Nenhuma nova chamada: o resultado foi recuperado pela API existente.
