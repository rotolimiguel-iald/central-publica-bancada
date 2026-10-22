[REAL — leitura integral e CAS exato; DERIVED — condicionado às famílias meromorfas; OPEN — Q2 curva]
# A7.b — revisão Kimi dos contatos, incorporada com correções
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T02:05:59.613407+00:00.

Recebido Kimi K3 máximo, job 9eefec6b-74ed-41c0-a50f-d5098179eba0, execução d23c96cf-09be-4eca-9dc0-841ffe008d61.
Resposta SHA256 `fb30e1bb7190a8227f37dbd03306a0d275b4a230c489d98d61c144e09804a306`. A resposta é DECLARADO até auditoria;
seu parecer favorável não substitui prova distribucional ou a soma causal completa.
Uso: {'prompt_tokens': 317940, 'completion_tokens': 48274, 'cached_input_tokens': 311296, 'total_tokens': 366214}. Custo não informado; não é zero.

**O que permanece.** A recorrência meromorfa, os resíduos, o tensor de posto dois
e o contato que corrige seu traço continuam compatíveis com os cálculos existentes.
O relatório original já declarava os insumos analíticos e o escopo de um par plano.
As 41 assertivas originais têm dependências comuns; não são 41 provas independentes.

**Correções ao parecer.**
1. Cancelar log(z)delta não é uma prova: o produto não foi definido. Não adotamos
essa rota nem os limites epsilon/z^k alegados sem demonstração. Basta a rota
meromorfa: zR_n=R_(n-1) e R_n=D_n+h_n Res U_n implicam
zD_n-D_(n-1)=(h_(n-1)-h_n)Res U_(n-1). Para n=3:3Cdelta/8.
2. Preservar R2=D2 determina g1=-1 em g(a)=1+g1 a+g2 a²+…;
não determina g(a) inteiro. Se U=r/a+v0+v1 a+…, FP(gU)=v0+g1r,
mas FP(gU')=v1-g2r. Portanto 1-a e 1-a+a² concordam na primitiva e
diferem no log por -r. A prescrição 1-a continua a já escolhida, sem ajuste novo.
3. A fórmula literal da seção2.2 do parecer duplica z^a. Corrigida, usa
mu^(2a)z^(-1+a); a duplicação altera a derivada por log(z)/z.

**Instância adicional.** Diferenciar U2(a) antes da parte finita dá
partial_mu U2=(-4+2a)x_mu U3. Logo

    partial_mu R2 - R(partial_mu z^-2)
      =2x_mu Res U3 =-(C/16)x_mu box delta =(C/8)partial_mu delta.

Não se usou multiplicação log(z)delta. CAS: 21 assertivas formais,
rc0, CPU 0.125s; não prova existência das distribuições.
Log e manifestação em A7/tensor_review_local. Nenhum original/gate alterado.

**Distribuição.** Coordenadora confirmou MiMo contact_bookkeeping iniciado;
Kimi marked_tensor_identity v2 registrado no job7af2e0e2-f377-4d51-87d3-db09350b51e4.
Os dois novos pacotes, Kimi curved_antifield_source e DeepSeek
logarithmic_contact_skeptic, tiveram rota prévia correta e staging confirmado.
Estão aguardando a ordem da fila; preparação não é execução. Um worker,
cinco pedidos não terminais e oito em staging no último status recebido.
Não repetimos falhas nem contaminamos revisões pendentes com o resultado desejado.
