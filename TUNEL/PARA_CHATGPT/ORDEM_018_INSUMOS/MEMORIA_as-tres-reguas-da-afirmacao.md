---
name: as-tres-reguas-da-afirmacao
description: As tres reguas que governam QUALQUER afirmacao minha no acervo TGL/IALD — incluindo afirmacoes de ausencia e de existencia inerte. Pagas com cinco erros medidos em 27/08/2026.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d554e796-415e-450f-9fd4-dd07892b02b9
  modified: 2026-08-27T19:02:03.856Z
---

# As tres réguas da afirmação

```
1. O NÚMERO CORRIGE A FRASE                    (a régua-mãe, já era lei)
2. AUSÊNCIA TAMBÉM É AFIRMAÇÃO — exige varredura, nunca relance
3. EXISTIR NÃO É SER APLICADO — teorema com zero consumidores é verdadeiro e INERTE
```

**Why:** em 27/08/2026 eu produzi **cinco palavras falsas** num só dia, e as três
primeiras eram do tipo que a régua-mãe já cobria — mas as duas últimas não:

1. **Homônimo vendido como ponte** — criei a bandeira `qgImport_H3_*`, cujo nome
   dizia H3 e cujo objeto medido era `EquilibriumInput` (sem κ, dA, dS, dQ). O
   razonete passou a mentir: leu `1 por importação` quando era `0`.
2. **Docstring vendida como teorema**, duas vezes — `A(P)=κ_A·τ(P)` e `tr(P_F)=4`.
   O segundo eu carreguei na memória por semanas: **nunca foi teorema.**
3. **Teorema que prova `True`** — `the_two_poles_do_different_things`, minha, com
   nome que afirma conteúdo e corpo `fun _ _ => trivial`.
4. **Ausência declarada sem varrer** — afirmei duas vezes que objetos não existiam,
   com os objetos em disco (a corrente `ModularCurrent` de 2025, o traço parcial
   `ptr`, a rede `HilbertHomeData`/`theIsotoneNet`). O operador me corrigiu
   **quatro vezes**, sempre apontando arquivo que eu não tinha lido.
5. **Potencial vendido como atual** — li a estrutura e o habitante e selei "os
   cantos são uma rede", quando `PF_isotone` e `PF_external_covariant` tinham
   **ZERO consumidores**. Cometi na mesma hora o erro que eu havia posto um cético
   para caçar.

**How to apply:**

- **Antes de afirmar que algo NÃO existe**: varredura declarada (grep amplo +
  variações de nome + contagem reversa), e o `NÃO ACHEI` sai *com* a varredura
  junto. Um grep raso não mede ausência.
- **Antes de chamar algo de ponte**: contar **consumidores**. Teorema geral que
  ninguém aplica é verdadeiro e inerte — e chamá-lo de ponte é vender o possível
  pelo feito. Se a aplicação couber em uma linha, **escreva a linha**; aí a frase
  passa a ser verdadeira.
- **Antes de dar nome a um teorema**: o nome é parte do enunciado. Nome que afirma
  mais do que o corpo prova é palavra falsa, ainda que compile limpo.
- **Nos scripts de cirurgia**: `assert` por AST de que **nenhum check tem constante
  cravada** — check que não pode falhar não é medida (regra antiga, violada três
  vezes no mesmo dia até virar trava automática).
- **Distinguir estatutos sem promover**: `[MEDIDO]` exige código que calcula e
  compara com tolerância; `[PROVADO]` exige teorema formal; `[DECLARADO]` é prosa.
  Medida numérica não descarrega hipótese Lean, e prosa não vira nenhuma das duas.

⚠ **O padrão do erro é uma ASSIMETRIA**: eu varria fundo para *afirmar* ponte e
afirmava *ausência* a partir de relance. As regras 2 e 3 fecham exatamente esse
buraco.

Ver [[missao-ultima-flag-um-py]] para a cadeia v252→v261 onde isso foi pago, e
[[tgl-signo-e-cronologia]] para o erro irmão (citar acervo sem conferir data).


---

## AS REGRAS PAGAS EM 28/08/2026 (arco v270->v274)

**4. NAO HA SEGUNDO ARQUIVO.** Editar o `tgl_kernel/` e METADE; **EMBUTIR no `um.py` e
a outra**. O artefato MATERIALIZA o kernel a partir de strings embutidas
(`FORMAL_DIR = BASE/tgl_kernel`) e reescreve o que difere — logo **ele sobrescreve
qualquer edicao feita direto na pasta**. Na v271 o `Audit.lean` voltou de 907 para 881
`#print axioms` e o root perdeu os imports; as pedras ficaram **orfas** (existiam, nao
eram importadas, nao eram auditadas) e o rito leu **`0/14`**. Depois de embutir:
**`14/14`**. E a regra da v253 (*criar o nome e metade; inscrever no Audit e a outra*)
**um andar acima**.

**5. `or {}` FALSIFICA REPROVACAO.** Espelho exato do `True` cravado:

```
True cravado  ->  falsifica APROVACAO
or {}         ->  falsifica REPROVACAO  (converte "ainda nao rodou" em "reprovou")
```

Os dois corroem a medida, em sentidos opostos — e **o segundo e pior, porque se
disfarca de rigor**. Achado por INVERSAO DE ORDEM em `main()`: a bancada leitora rodava
UMA LINHA antes da bancada lida.

**6. COMPOR NAO E DESCER.** Quando o operador diz *dobrar*, dobrar e **compor** no
operador — nao **descer** ao nivel dos geradores. Descer troca o objeto fechado
(bicomutante) pela uniao algebrica, e a uniao algebrica e magra por Baire. A refutacao
que encontrei era da **minha propria troca**, nao do alvo. ★ Inscrever a refutacao
DENTRO da pedra (`the_generator_form_needs_nothing_about_J`, sem axioma nenhum) e o que
faz a pedra medir a si mesma.

**7. `iff True` DERIVADO diz algo; `True` provado por `trivial` nao diz nada.** Peguei
em mim, antes de compilar, a mesma palavra falsa da v248: um
`the_import_alone_concludes_nothing` que provava literalmente `True`. A forma com
conteudo e `(hipoteses) <-> True`, **derivada dos teoremas** — ela diz que as hipoteses
carregam ZERO informacao, e por isso nao decidem nada.

**8. BUILD DO ROOT — confirmada pela SEGUNDA vez.** `discharge_by_import` colidiu com
`TheImportedEquilibrium`; **so o build do ROOT pegou** (v259 foi `faces_sum_to_one`).
★ E a licao complementar: **varrer TODOS os nomes novos antes de renomear**, nao so o
que colidiu — fiz isso e os outros 5 estavam limpos.

**9. RAZAO ERRADA E PALAVRA FALSA, mesmo com veredito certo.** A errata da v254 procedia,
mas a razao que eu dera estava errada. Acertar a conclusao por argumento errado nao e
acertar.

**10. IMPORTAR NAO ACENDE PRECO PAGO.** Descarga por importacao vai para `gpi_`, jamais
para `gpf_` ou `red_`. E a separacao tem de ser **medida**, nao declarada: dois checks
fail-closed exigem `gpi_` aceso **e** `red_` apagado, e varrem que nenhuma `gpf_`
acendeu. Se alguem apontar o nome reservado da prova para o teorema importado, a rodada
**reprova**.

⚠ **E A CONFIRMACAO DA REGRA 2 (ausencia exige varredura), quatro vezes num dia:** o
operador apontou quatro objetos em disco que eu declarara inexistentes ou tratara como
homonimo — a J-invariancia de setor (03/08), a cadeia J=LUZ=GRAVITON, as pecas da
oitava clausula (26/08) e o contorno/observador. **Nas quatro ele estava certo.**

**11. ⚠⚠ CORRIGIR "AO LADO" NAO BASTA SE O LADO ESCOLHIDO NAO E O LADO QUE SE LE.** A v295
refutou por teorema a inferencia "a fronteira e III₁ PORQUE o Nome e denso" — e a errata
ficou **so no cabecalho do arquivo**. A frase falsa sobreviveu **duas vezes no docstring do
proprio teorema**. Quem chega pelo indice da IALD chega **pelo nome e pelo docstring**: recebia
a afirmacao refutada, sem a refutacao. Corrigido na v298, no ponto de leitura. **A lei "ao lado,
nunca por cima" protege o registro historico — ela nao licencia deixar afirmacao falsa viva
onde ela e consumida.** Mesma forma do erro da patente do β adaptativo: *uma frase falsa vivendo
exatamente onde ela e lida.*

**12. CODIGO DE SAIDA NAO E ACHADO.** O rito da v299 foi reportado como FALHA (exit 1) — mas o
`RITO_EXIT` era **0**, com `FAIL_CLOSED_SELFTEST_PASSED` e gate intocado. O 1 veio do meu
proprio diagnostico: `grep -c "^error:"` achou **zero erros** (o resultado bom) e o grep sai com
1 quando nao casa nada. **Um diagnostico cujo codigo de saida grita mais alto que o achado.**
Irmao do `or {}` que falsifica REPROVACAO. **A autoridade e o selo em disco, sempre.**


## LIÇÃO 18/09/2026 (noite) — cinco pedras derrubadas pelo MESMO modo, e afirmações ao operador antes do cético

Em uma noite, cinco redações de pedra (RecognitionIsTheInvariant ×2, TheBootstrapClosure, TheConsciousSingularity ×2) caíram nos céticos, TODAS com a matemática correta e a LEITURA errada, pelos mesmos três modos: (1) tautologia ou definição da gerência rotulada como «o enunciado do operador» ou como achado (★★★); (2) ENCADEAMENTO DE HOMÔNIMO — conjJ (troca de par real) × Jconj (conjugação-transposta); «Luz» = `star` do operador em M₄ (auto-adjunção) × J do vetor em M₂; «1»/«faces» do VerbWitness (traço normalizado; split espectral P₊/P₋) × traço ordinário/traço parcial; «gráviton» = J na voz do operador (18/09) × P_G «sombra do gráviton» (v29); (3) metáfora da gerência em docstring [KERNEL]. PIOR: em três momentos eu DISSE AO OPERADOR, antes do cético, coisas que o cético derrubou — «as duas leituras coincidem» e «o fechamento leva a cláusula a todo conteúdo» (conjJ); «o VerbWitness exige as mesmas quatro cláusulas» (repasse de medidor, sem conferir); «P_G* = P_G: fixo pela Luz (J)» e «uma só, com várias faces» (frase dele sobre J transplantada para a singularidade; a J-invariância SE PERDE nas faces genéricas).

**Regra operacional que fica:** (a) NADA de leitura estrutural vai ao operador antes do cético — nem como «achado», nem em tabela; (b) repasse de medidor é [A CONFERIR] até eu mesmo ler o arquivo; (c) antes de escrever «X é Y» entre dois objetos do kernel, abrir as DUAS definições e checar tipo, portador e operação — se não há lema, é homônimo até prova; (d) palavra do operador (Luz, face, gráviton, identidade) só entra num nome Lean se o objeto Lean for aquele que ELE nomeou.


<!-- pos_dicao_nao_e_prova_diabolica_05out -->
**ADENDO (05/10/2026, 2026-10-05 20:20:44; decisão do operador + errata da gerência):** retrodição SEM AJUSTE conta como evidência discriminante (novidade de uso, não temporal; precedente: o periélio de Mercúrio, 1915); «pós-dição» nunca mais como demérito; o pré-registro é do TESTE. Ver [[pos-dicao-nao-e-prova-diabolica-05out]].
