[REAL — entrega parcial; não encerra M1, M2 ou a ORDEM 013]


[REAL — progresso parcial, objetivo integral ativo]

## Rodada 2026-09-21T23:22:04.732264+00:00

A auditoria cobre 24 itens e todas as 38 linhas não vazias exigidas. O módulo recupera os dois ramos V346; a derivação GKSL diferencia taxa de salto, coerência, amplitude e potência. Os modos exatos qnm concordam com Leaver, e quatro curvas PSD foram usadas no forecast, com controles PyCBC/LAL em arquivo separado. O C5_FISHER conserva o retrato anterior em sua lista not_done; os controles foram pagos depois dele e estão em PSD_CONTROLS.json.

No primeiro confronto público (40776 amostras), ramo B: ln B=0.029026162, bootstrap 95% de ln B=[-0.03364357129888176, 0.027358577656555028, 0.09183101867182289]. Desvio previsto mediano em tau=-0.019845285; correção/erro marginal=0.343377. A quadratura tridimensional independente difere por -1.13e-06 em ln B. Isso é comparação do 220 mantendo 440 livre, sob hipótese de amortecimento de ensemble; não é confirmação nem decisão sobre a teoria inteira.

**Ainda falta**

- C0: arquivar fontes primárias consultadas, com hash; não alegar leitura integral dos cinco relatórios de gerência.
- C1: tabela completa de todas as leituras, relógios, partições, unidades, efeitos de distância e exclusões condicionais da v369.
- C2: distribuição dos estimadores em trajetórias com ruído colorido; tratar lei linear/Cauchy e raiz sem impor desenrolamento browniano.
- C3: verificar integração com consumidor de inferência; campo coerente-raiz não é exponencial; optional 221 não implementado.
- C4: R-MOD em grade exata, priors livres de tau, pyRing, catálogo sem duplicação, versão do fit de remanescente, hipóteses 220+440.
- C5: injeção/recuperação N>=50 por célula, viés/cobertura e duas famílias; Fisher com massa/spin livres requer informação adicional.
- C6: registro próprio antes de ler strain na janela; PSD fora da fonte; execução registrada e comparação de tempos.
- C7: pacote independente em inglês, manifesto e reprodução final, apenas após completar a matriz de evidências.

**Falhas e correções preservadas**

- WSL sem elevação retornou E_ACCESSDENIED; acesso científico somente leitura foi autorizado e funcionou.
- Rede sandbox retornou WinError10051; download público autorizado concluiu e checksum confere.
- qnm sem numba falhou; dependências instaladas somente em cache/vendor, /opt preservado.
- Quadratura inicial atingiu limite de subdivisões; resolução aumentada, resultado anterior preservado em backup; novo teste sem aviso.
- Controle PSD inicial recusou zero em Nyquist; a convenção foi explicitada, apenas esse endpoint excluído, interiores validados.

Memória de retomada: STATUS_ORDEM_013.json contém os caminhos, hashes lidos, estados e próxima ação. Nenhum processo permanece rodando nesta gravação; arquivos de resultados não são prova de processo vivo. Nenhum strain da janela do evento foi lido.

## Artefatos verificados

- `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\C0_AUDITORIA.json` — SHA256 `f0009e1194282434ac599a35df68573db08967951a320218184670e15e1559cd`
- `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\C0_AUDITORIA.md` — SHA256 `fc85dafd94e7a86c0c1c3e6450104c3644302a94d70917c141d8005ca77ef039`
- `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\C0_C3_checks.json` — SHA256 `0592189981243c503a36967cd9285666e5120c804cca41bb23e233a6bd5230b0`
- `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\C2_MAPEAMENTO_ANALITICO.md` — SHA256 `3b1b04893605f6a01a39e18567903d0a24d678a9fc0276e01b7d99efc9df503e`
- `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\C2_TEMPLATE_CHECKS.json` — SHA256 `b43fa517a37f9b41b8aa2d4f699571a4e24c7da5f6027266e55a86b6ffbe579a`
- `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\tgl_ringdown_prediction.py` — SHA256 `552a07acfd6011d995b5010c412f7599c20a1c64505a93dd4c7fa2c3808cbb3e`
- `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\tgl_ringdown_template.py` — SHA256 `ef1b4d69a687a84435ccd22d2643cb2917d5dfa9f4339ed075408a7e5b0d502c`
- `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\C5_FISHER.json` — SHA256 `71189d65f52d3530e71a1a5ce3a1603b69b57e6166c1fe3c0f7efd887c64fcf9`
- `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\PSD_CONTROLS.json` — SHA256 `eafa22ff5611cc991aa0d53b9d302a91000ec5fb035b6bd4e122fb12d4de9cb9`
- `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\FISHER_INPUTS.json` — SHA256 `4ae8f57dbd312590ea115ed7a38405953e0e37a4088b0eb19a13582235bfa097`
- `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\REGISTRO_C4.json` — SHA256 `2bebc171ddbcef43d7b50b9076dd806b64829a05a769b6e4fe23b73ec121ac59`
- `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\C4_SCHEMA.json` — SHA256 `c4076fca98bcb544f3808a903d6d6005978435b79c4f9dee5371970881ab39d4`
- `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\C4_220_INITIAL.json` — SHA256 `f5550b7b1f129e83b4874f95b223e82ca973e0812bd98c150a6c04cd37747edc`
- `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\C4_VALIDATION.json` — SHA256 `817bc63ea74f4131d1a97fa53c274fef59cd60470b8c1560bbecc6be648d3785`

PAGO/NÃO PAGO: os testes explicitados acima estão pagos no escopo indicado; cada item da lista de pendências permanece NÃO PAGO. Kernel/axiom report: NÃO APLICÁVEL, sem alterações Lean.
