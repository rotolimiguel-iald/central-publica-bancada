# NS-01 — composição de e(M110) e alcance de M110_offset

[REAL — exame documental local em 06/10/2026 UTC; nenhuma execução upstream]
Parecer: **o offset comum não justifica omitir integralmente e(M110) no fluxo SBF**. A documentação primária do próprio H0DN destina essa coluna a erros de cor e largura intrínseca, excluindo a incerteza da calibração absoluta. A composição numérica por objeto permanece parcialmente [OPEN]: a receita que produziu cada e(M110) não foi estabelecida neste recorte. Não é possível afirmar qual componente predomina quantitativamente, nem chamar toda a coluna de ruído independente.

## Evidência decisiva no código pinado

Fonte: h0dn_documentary_review/upstream/idlcode/org_v3p9.pro, commit registrado no manifesto local. SHA lido, verificado e incluído em EVIDENCIA_COMPONENTES_SBF.json.

- Linhas 1817–1824: o arquivo processado terá M110 calculado da cor, com propagação de erro e um termo adicional de largura intrínseca, cuja determinação o comentário ainda deixa pendente.
- Linhas 1846–1859: distingue o erro de M110 do erro fotométrico de m110; exclui explicitamente a incerteza da calibração de distância e a atribui ao parâmetro m_offset. Admite uma aproximação sem correlações entre objetos e reconhece que parâmetros internos da calibração, distintos do offset absoluto, geram correlações consideradas subdominantes pelos autores.
- O comentário 1846–1848 também menciona “velocity and parameters”. Isso não é uma fórmula de construção da coluna e não deve ser promovido a prova de que ela contém erro de velocidade. A descrição anterior liga M110 à cor; a velocidade possui propagação própria em compute_alpha. A redação heterogênea reforça a necessidade de separar intenção declarada e implementação.
- Linhas 1805–1811: os calibradores somam os quadrados dos erros de M110 e m110, identificados como cor, largura intrínseca e fotometria.
- **Linha 1867: o fluxo recebe apenas sigma_m110_sbf_hf.** sigma_big_m110_sbf_hf foi lido na linha 1830, mas não é argumento dessa chamada.

A implementação Python confirma a assimetria: equations.py:454 soma os dois erros nos calibradores; equations.py:603 fornece apenas e(m110) a compute_alpha no fluxo. equations.py:255–266 define um único M110_offset livre, sem limite ativo. Logo:

1. [REAL] a omissão existe nas duas implementações examinadas.
2. [DECLARADO na documentação primária] e(M110) não foi concebido como a incerteza da escala absoluta já representada pelo offset.
3. [OPEN] não foi identificado o gerador numérico dos valores da coluna; os comentários, por si, não certificam uma decomposição exata.

## Artigo e catálogo oficial já consultados

[KNOWN/DECLARADO nas fontes] Jensen et al. 2025, §3.1, Eq. (2), usa uma relação linear entre M110 e cor PanSTARRS, com inclinação 1,86 ± 0,16 e pivot 1,30. A incerteza de cor inclui extinção; a transformação DECam–PanSTARRS recebe dispersão adicional. O §3.3 separa a calibração sistemática ligada a NGC4258/TRGB e ao zero-point. Isso sustenta separar erro local de cor, parâmetros comuns da relação e calibração absoluta; não fornece a decomposição da coluna processada pelo H0DN. Fonte: https://arxiv.org/html/2502.15935v2#S3 .

O README oficial identifica a tabela de 2025 como atualização da calibração e das cores, medidas em anéis correspondentes aos da SBF. Não é um manifesto do pré-processamento H0DN: https://github.com/jjensen-uvu/sbf_distances_2021 .

O H0DN arquivado, Apêndice A.4, linhas 1821–1845 de sources/h0dn.txt, liga explicitamente suas entradas a essa calibração e distingue sistemática da inclinação e do zero-point. A tabela de proveniência nas linhas 488–490 menciona informação auxiliar por comunicação privada. Portanto, a fonte pública é informativa, mas não certifica todos os detalhes da coluna intermediária. Nenhuma comunicação ao autor foi enviada.

## O que o offset pode e não pode representar

[DERIVED — álgebra, sem avaliação observacional] Escreva M(c)=a+b(c−c*), com a associado à escala comum. Para um objeto, o erro residual de m−M, condicionado a a e b, tem a forma

    ε_i = ε_m,i − b ε_c,i − ε_int,i
    Var(ε_i) = σ_m,i² + b²σ_c,i² + σ_int,i² − 2b Cov(m_i,c_i)

quando os demais termos são independentes segundo o modelo escolhido. A independência aqui é uma hipótese finita do modelo, não uma exigência física absoluta. Extinção ou calibração fotométrica compartilhadas podem ser representadas explicitamente.

Uma incerteza comum na inclinação acrescentaria a estrutura σ_b² x xᵀ, x_i=c_i−c*, antes de qualquer compressão, se b fosse um parâmetro externo independente com esse prior. Covariâncias entre inclinação e intercepto exigem o bloco correspondente. Um deslocamento comum ocupa a direção 1; cor variável e largura intrínseca não ocupam apenas essa direção. Assim, um único offset não elimina esses erros.

Na parametrização concreta do H0DN, y_cal=m−M=μ+M_offset e α_HF=log(v)−0,2(m−M). Uma mudança de convenção M→M+Δ comum leva a M_offset→M_offset−Δ e α→α+0,2Δ, deixando h na equação h−0,2M_offset=α+5 invariante. Isso demonstra a redundância de uma translação comum quando o offset é livre. Não demonstra absorção de erros diferenciais. Com prior próprio ou truncamento do offset, é necessário transformar também o prior; a invariância não é automática.

Como os calibradores e o fluxo usam a mesma relação por cor, eventual incerteza de inclinação pode correlacionar os dois blocos. Não deve ser reintroduzida como vários priors independentes, nem como prior externo derivado dos mesmos calibradores que já entram no ajuste, sem tratar a reutilização. Nenhuma matriz observacional foi montada aqui.

## Duas alternativas finitas para a coordenação

**A — reprodução upstream, com limitação explícita.** Preservar o argumento e(m110) no fluxo, a soma em quadratura nos calibradores e o offset comum. É uma especificação reprodutível do código disponível. A nota deve dizer que a contribuição e(M110) do fluxo foi omitida e que isso não é justificado integralmente pelo offset. Não chamar essa prescrição de covariância publicada completa. Nenhum cálculo foi feito para medir o impacto da omissão.

**B — reconstrução condicionada à origem dos componentes.** A separação conceitual está documentada, mas a reconstrução numérica integral ainda não está fechada. É suficiente um contrato finito que determine:
- quais termos de cor, extinção e dispersão intrínseca estão em cada e(M110), e quais já estão em e(m110);
- se a incerteza de inclinação está incluída, e como a dependência comum atravessa calibração e fluxo;
- que parte da calibração absoluta já é representada pelo offset/rede, evitando contagem dupla.

Usar e(m110)²+e(M110)² também no fluxo pode ser **uma variante diagonal explicitamente aproximada**, coerente com a intenção declarada do IDL se os termos residuais forem tratados como independentes e excluírem o zero-point. Não é uma decomposição independente verificada e não foi adotada, executada ou promovida a correção obrigatória nesta unidade. Não subtrair da coluna um zero-point tomado do artigo por mera coincidência numérica.

Conclusão operacional: NS-01 está esclarecido quanto à distinção offset versus erro residual; continua aberto quanto à partição numérica e às correlações dos valores fornecidos. A alternativa A permite reproduzir a prescrição com seu limite; B requer esse esclarecimento finito, não uma matriz idealizada infinita ou independência absoluta.

## Recibo, alcance e bloqueio de arquivamento

O script audit_sbf_components.py leu 14 fontes locais e verificou sete pins de arquivos upstream contra os manifestos herdados. Preservou trechos com linhas, cabeçalhos e hashes; nenhuma coluna central dos catálogos foi convertida ou exibida nesta extração. Reutilizou o inventário de erros anterior. A conclusão de ausência do gerador limita-se aos artefatos admitidos examinados, sem alegar inventário integral do repositório remoto.

A tentativa de arquivar quatro fontes públicas falhou na rede do sandbox. O escalonamento foi rejeitado pela revisão automática por considerar o download fora da autorização visível do heartbeat e originado em contexto de agente não confiável. O comando elevado não executou. Não houve repetição ou rota alternativa. A coordenação determinou fechar esta unidade sem esse arquivamento dispensável. WEB_SOURCES.json conserva as falhas locais; as duas referências web acima foram lidas, **mas não têm cópia externa por bytes/hash certificada nesta entrega**.

Nenhum centro, intercepto, H0, S/g, likelihood, evidência ou fit foi calculado; nenhum programa upstream ou executor remoto foi chamado; D permaneceu fechado. Não se adotou V1, uma nova covariância ou qualquer veredito físico.
