# F9 — seleção local de aritmética e menor unidade seguinte

Pedido bf2a5692-1aff-423e-9345-7bfa256d5072, 06/10/2026. **[REAL documental]** Inventário e leitura estática locais. **[DERIVED]** Fixture e critérios algébricos abaixo. **[INPUT proposto]** Seleção para implementação posterior, sem adoção/execução científica. Nenhum candidato foi importado nesta unidade.

## Decisão

**Selecionar inteiros Python + `fractions.Fraction`, com entrada racional canônica, para preparar somente NC02-RAT-01.** A unidade é pequena, usa aritmética exata e verifica a ligação entre um certificado dual inferior e uma testemunha superior factível. Não precisa de exponencial, logaritmo, álgebra linear geral, `mpmath`, CAMB ou WSL. A disponibilidade documental do runtime e da fonte foi conferida; o novo instrumento ainda será implementado e revisto em unidade própria.

Isto não escolhe o backend definitivo de toda a F9. A qualificação do motor contínuo, das funções transcendentes e das integrais permanece separada. Não se repete a cauda racional V2: seu recibo é uma dependência já consumida, e sua API não será chamada por NC02.

## 1. Inventário efetivamente observado

Foram enumerados somente `C:\Python314\Lib\site-packages`, o user-site Python314 do operador e `/opt/lal_env/lib/python3.12/site-packages` da distribuição Ubuntu-24.04. Metadados de distribuição não comprovam importação bem-sucedida, ABI compatível ou precisão de funções. Ausência nessas listas não significa ausência no computador inteiro.

| Local | Evidência presente | Alcance |
|---|---|---|
| Windows, Python3.14.3 | `fractions.py`, `decimal.py`, `_pydecimal.py`, binário `_decimal`, executável e DLL principal pinados | Fontes/bytes disponíveis; nenhum desses candidatos importado para teste |
| Windows, user-site | mpmath1.3.0, NumPy2.4.3, SciPy1.18.0, SymPy1.14.0 em METADATA | Pacotes identificados documentalmente; fora da resolução automática do Python `-I -S` |
| WSL, `/opt/lal_env` | Python3.12.3; mpmath1.3.0, CAMB2.0.4, NumPy2.5.3, SciPy1.18.1, SymPy1.14.0 em METADATA | Leitura atual de metadados; nenhum import/solver |
| Três raízes enumeradas | Nenhum METADATA correspondente a python-flint/flint, gmpy2, MPFI/MPFR, Arb ou pacotes intervalares adicionais na lista pesquisada | Não afirmar indisponibilidade global; nenhuma instalação proposta nesta unidade |

A enumeração inicial sob o sandbox não tinha acesso ao user-site e ao serviço WSL. A leitura elevada, restrita a metadados/fontes, foi aprovada e concluiu. Essa falha de acesso não foi interpretada como ausência de pacotes. O comando WSL de metadados usa `python -I -S -B -c` com código textual, sem caminho Windows no argv Linux. Isso não reabre nem corrige o controle WSL4f5d consumido.

`METADADOS_BACKENDS_LOCAIS.json` contém30 pins locais, cinco METADATA WSL com SHA, faixas de fonte e o escopo exato da enumeração. O coletor importa apenas bibliotecas de infraestrutura para ler bytes/JSON e executar a consulta de metadados. Não importa `fractions`, `decimal`, `mpmath`, NumPy, SciPy, SymPy, CAMB ou o módulo da cauda.

## 2. Estratégias comparadas

### A — racional exato, recomendado para a unidade mínima

A fonte de `Fraction` usa numerador/denominador inteiros e normalização por gcd nas operações racionais examinadas. Isso sustenta o escopo escolhido de soma, produto, divisão por racional não nulo e comparação exata, condicionado ao runtime pinado e aos recursos. Não chamar isso de prova formal de todo CPython.

Aceitar apenas os pares `{numerator,denominator}` de strings inteiras canônicas já especificados em `tail_envelope.py:119–149`; denominador positivo, gcd1 e limites lexicais antes de converter. **Reutilizar o codec existente por um adaptador explícito em futura unidade autorizada**, sem copiar ou modificar a fonte da cauda, e sem chamar `tail_upper`, agregador, worker ou seus controles. O codec privado precisa de dependência por hash e contrato de retorno `(a,b)`; seu sucesso prévio não testa o novo certificado dual. A aritmética interna pode construir `Fraction(a,b)` desses inteiros. Recusar entradas float: `Fraction(float)` representa o binário recebido, não o decimal que alguém talvez tivesse em mente.

Os recursos limitam a exatidão disponível operacionalmente: crescimento de numeradores não é erro de arredondamento, mas pode esgotar memória/tempo. Limite de bits e domínio pequeno devem preceder operações caras; esgotamento é saída explícita, sem aproximação float silenciosa. A unidade proposta não promete suportar matrizes283×283 ou qualquer célula cosmológica.

Para funções elementares futuras existe uma construção racional já documentada na proposta de cauda, **não uma implementação transcendental qualificada pelo PASS da cauda**. Para a≥0 racional, y=a/2^k≤1, S_n=Σ_{j=0}^n y^j/j! e t=y^(n+1)/(n+1)!:

\[
S_n\le e^y\le S_n+\frac{t}{1-y/(n+2)},\qquad
\left(S_n+\frac{t}{1-y/(n+2)}\right)^{-2^k}\le e^{-a}\le S_n^{-2^k}.
\]

Todos os extremos são racionais. A cauda posterior tem razões de termos limitadas por y/(n+2)<1, o que dá o resto geométrico. Essa rota é pertinente para integrar bounds positivos no futuro; é desnecessária para NC02 e fica fora de seu payload. A cauda V2 realmente executada usa uma majorante racional sem exp/log, não mede o erro dessas funções. Não transferir seu PASS a uma implementação ainda inexistente.

### B — mpmath.iv, disponível documentalmente, não qualificado aqui

As fontes instaladas contêm contexto intervalar e funções `mpi_add`, `mpi_exp`, `mpi_log`, `mpi_sqrt`; estas últimas encaminham os extremos a operações com `round_floor`/`round_ceiling`. Isso mostra o mecanismo pretendido, não prova a inclusão para todo argumento/ramo utilizado na F9.

O METADATA local, seção de problemas conhecidos, registra que o arredondamento dirigido é suportado para operações aritméticas e pode ser heurístico em outras, além de limitações perto de singularidades e na troca de contexto. Por isso não presumir certificado global de transcendentes, matrizes ou quadratura apenas por escolher `iv`. Também não deduzir que toda chamada `iv` está errada: esta unidade não executou teste algum. Um adaptador de escopo estreito poderia ser examinado depois com domínio, conversões, funções e bounds próprios. Acrescentar arbitrariamente duas ulps não é prova de cobertura universal.

### C — Decimal com envoltórias explícitas, alternativa secundária

O Python instalado contém a interface Decimal e o acelerador `_decimal`; a fonte fallback `_pydecimal.py` foi lida. Nela, exp/ln fazem arredondamento final HALF_EVEN nos trechos examinados. Logo não basta alterar `Context.rounding` e declarar que já se possui uma API intervalar para essas funções. Um adaptador poderia usar uma garantia de arredondamento corretamente delimitada e vizinhos externos, com domínio/exceções/overflow tratados. O contrato do acelerador e esse adaptador não foram qualificados aqui; não atribuir ao binário uma prova obtida apenas lendo o fallback.

A não precisa dessas funções na unidade mínima e evita tal dependência. B/C podem ser mais convenientes em etapas maiores, mas conveniência ou mais dígitos não são certificado. Não se mediu desempenho relativo. Backends adicionais não localizados nas raízes consultadas não geram pedido de instalação ou uma tarefa fictícia.

## 3. Unidade mínima NC02-RAT-01

Identidade proposta: `bf2a5692-1aff-423e-9345-7bfa256d5072::NC02-RAT-01`. É uma **unidade proposta de implementação**, não request/claim/RUN de execução. O JSON do payload fica pinado nesta entrega; `execution_request_id` e hash de worker ainda inexistente permanecem null. Após implementação/revisão, a coordenação deve vincular os hashes do código e o identificador de execução próprio antes de rodar uma única vez. Nada é despachado agora.

Recorte do NC02 já planejado: uma caixa sintética, duas coordenadas de observação, um nuisance, um caso positivo e um negativo de anulamento. Não há função exponencial, cauda, quadratura, sorteio, observação física ou varredura cosmológica.

Defina

\[
C=I_2,\quad X=(1,1)^T,\quad b(u)=(1,u)^T,\quad u\in[0,1/2],\quad \eta\in\mathbb R.
\]

Por completar o quadrado,

\[
\|b(u)-X\eta\|^2=2\left(\eta-\frac{1+u}{2}\right)^2+\frac{(1-u)^2}{2}.
\]

Assim q(u)=(1−u)²/2 e o ínfimo na caixa é1/8, atingido em u=1/2. Estes são resultados **algébricos esperados**, não medições de execução.

**Caso positivo.** Escolher v=(1/4,−1/4), que satisfaz Xᵀv=0 exatamente. O certificado dual é

\[
2v^Tb(u)-v^TCv=3/8-u/2\ge1/8.
\]

A testemunha u=1/2, η=3/4 tem resíduo (1/4,−1/4), norma ao quadrado1/8. Portanto o artefato esperado deve conter **L=U=1/8**, vínculo com a caixa e prova de anulamento, sem resolver uma matriz ou invocar otimizador. O verificador independente pode conferir o limite inferior pelo coeficiente afim/extremo racional e o superior pelo resíduo racional da testemunha.

**Caso negativo.** Trocar somente v por (1/4,−255/1024). Agora Xᵀv=1/1024, não zero. Deve retornar `INVALID_DUAL_ANNIHILATION`, sem limite aceito. Um cutoff que aceite esse valor pequeno torna inválida a eliminação do nuisance irrestrito. Não se testa novamente o parser de denominadores, a SF ou o guard; os recibos correspondentes apenas permanecem como dependências.

## 4. Contrato para a implementação seguinte

O payload exige strings racionais canônicas, IDs/ordem exata dos dois casos, matriz C e coluna X fixadas, caixa inteira, coeficiente de b, vetores duais e testemunha. O resultado esperado pertence ao avaliador e não pode ser usado pelo construtor como constante de saída. `builder` e `verifier` precisam de caminhos separados; o verificador recompõe os resíduos, coeficientes e comparações inteiras em vez de confiar em `valid=true`.

Dependências/pins são lidos dos artefatos: interface e revisão aceitas; recibo tailV2 e sua fonte/codec; Pythonexe/DLL/Fraction; payload e inventário local. O conjunto completo de imports do futuro worker só poderá ser pinado depois de ele existir: esta entrega não finge um runtime hermético. Preferir Windows no runtime já documentado; nada depende da unidade WSL falha ou de corrigir provedores.

Escopo proposto: uma execução futura, dois casos fixos, nenhuma chamada remota, nenhuma tolerância de ponto flutuante, um processo científico simples sem subprocesso de solver; supervisão pelo mecanismo já existente se aprovada pela coordenação. Teto proposto10s de worker,30s totais incluindo persistência, uma thread,256MiB RSS e128KiB de saída. São requisitos para implementar/verificar, não limites do SO já demonstrados. O limite canônico de entrada512bits vem do codec existente; o caso tem dimensão fixa2×1 e as operações intermediárias devem ser recusadas antes de exceder o orçamento de bits que o implementador fixar e revisar. Não expandir para gerador arbitrário de fixtures.

Claims e saídas exclusivas serão criados somente na unidade autorizada; esta preparação não cria identidade executada nem permite retry após terminal incerto. O payload não recebe autorização por estar hasheado. Não rodar os dois casos nesta etapa. O novo instrumento deve usar a dependência codec sem chamar worker/tail/controle antigo.

## 5. Limites e continuidade

Existe uma próxima unidade útil e suficientemente pequena: preparar o código NC02 com aritmética racional local, não inventar um backend cosmológico pronto. Seu eventual PASS verificará esse recorte de interface, não a minimização global da F9, a cobertura do CAMB, as integrais relativas ou significância física.

A fila de modelos continua fora desta tarefa. Metadados oficiais registram falha de memória canônica/integridade e o pedido Claude antigo permanece bloqueado. Não houve reparo, repin, admissão ou despacho. Não foram repetidos CAMB, C01–C08, tailV2, guard, INIT003 ou WSL4f5d.

Os arquivos desta pasta são preparação e custódia; nenhum original, memória compartilhada, modelo físico, prior, alpha, V1, §6 ou gate foi alterado. A coordenação recebe o pacote para revisão e definição da próxima execução, se pertinente.
