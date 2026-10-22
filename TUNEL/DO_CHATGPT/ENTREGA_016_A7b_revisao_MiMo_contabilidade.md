[REAL — nove contraexemplos locais; DECLARADO — proposta MiMo preservada; OPEN — coeficiente Ward completo]
# A7.b — revisão do módulo de contabilidade proposto pelo MiMo
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T02:18:28.640171+00:00.

Job fb3587cd-5807-4dab-9aa0-3ac178bc4deb; execução 51c96729-a31e-4dd2-972f-980ca185a216; resposta SHA256
`91acc33e073475f773a2ed5e7f4e1720304c4e835858de56975629a1ac7ef7f9`. Texto recuperado sem nova chamada e lido, inclusive
o trecho de funções inicialmente truncado na exibição. A proposta fornece
uma tabela das fontes antigas e um módulo textual; não calcula amplitudes.

**Decisão: não incorporar o módulo como novo leitor/gate.** Os testes locais
encontraram nove problemas delimitados:

1. O verificador do traço não lê o termo: aceita um coeficiente adulterado999.
2. O verificador de derivada aceita uma fórmula arbitrária não reconhecida.
3. O caso de polo simples é recusado sem uma via de fornecer a certidão exigida.
4. O fator de aridade zero é aceito no contato que exige n.
5. Um ledger vazio anuncia WARD_COEFFICIENT_EMITTED.
6. O mesmo ocorre com flags de erro: elas não entram na decisão.
7. Um registro com a mesma fórmula sobrescreve coeficiente sem colisão.
8. CT11 e CT12, parcelas aditivas da mesma variação, são tratados como duplicatas.
9. CT10 chama grad(chi)grad(u)/(1+u) de termo linear/livre inteiro. A separação
correta é grad(chi)grad(u) menos u grad(chi)grad(u)/(1+u); a segunda parcela
é precisamente o resto interagente já calculado na fonte v2.

Os resultados podem ser reproduzidos por mimo_contact_bookkeeping_audit.py,
rc0, CPU 0.453125s. O módulo original foi extraído byte a byte
do bloco Python recebido e preservado na bancada; imports conferidos:
future/dataclasses/enum/typing, sem acesso a rede, shell ou arquivos no módulo.
Os casos de teste propostos pelo modelo eram especificações, não implementações
de todos os detectores anunciados. Flags fornecidas pelo chamador não verificam
independentemente o coeficiente que deveriam auditar.

**Aproveitamento sem nova camada.** A distinção entre contato de Green,
variação com cutoff e defeito de extensão já está nos cálculos originais;
ela permanece. A tabela é referência documental da rodada que o MiMo recebeu,
não retrato automático dos avanços posteriores. A contabilização continua
ancorada em expressões e fontes, sem converter rótulos em prova matemática.
Não se acrescenta este gate paralelo ao programa, não se reabre a unidade
terminal e não se repete a chamada para corrigir um catálogo de metadados.

Consumo informado pelo executor: {'completion_tokens': 38394, 'prompt_tokens': 331454, 'total_tokens': 369848, 'completion_tokens_details': {'reasoning_tokens': 23471}, 'prompt_tokens_details': {'cached_tokens': 313728}}.
Custo estimado informado: 0.0422430108USD;
não equivale a fatura. A7.b permanece ativa e nenhum original/gate foi alterado.
