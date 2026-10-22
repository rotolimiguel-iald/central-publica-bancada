# Bancada Um versus um.py corrente — auditoria de compatibilidade

09/10/2026 · codex-gerente-tgl · F0.3.B1, reivindicação 621.

## Conclusão

**[REAL documental e estado vivo] A Bancada está operacional, mas não está integralmente preparada nem certificada para executar o novo teste neutrinos–luminosidade–Chandrasekhar com a identidade atual da TGL.** Há módulos históricos válidos para seus contratos, opções atuais já disponíveis e correções/canais ainda em sandbox. Não é seguro tratar qualquer chamada da Bancada como uma execução do um.py corrente.

O exame cobriu as 25 ferramentas MCP declaradas em disco, os módulos da Bancada, fontes/validações pertinentes, GW e Fase 9. Consultas vivas foram apenas de estado/proveniência; não houve ajuste, composto observado, leitura de série cega, recarga, instalação ou escrita na Bancada. Os controles de neutrinos da F8.2.NU2 correram em sandbox, não na GPU do motor residente.

## Identidade medida

| Superfície | Medição |
|---|---|
| um.py canônico em disco | **v391**, SHA256 `8e7b9927ceae64b8b6812019f77cca24c08296222ae7968af41baf2fe7a67dc6` |
| Selo atual | v391; seu pin de um.py confere com os bytes lidos |
| Processo HTTP | versão interna 0.1, pronto, no ar desde 01/10/2026 17:14:06 |
| Origem de α registrada em RAM | SHA256 `65d0567929798915c50c0610fc380cea27cb3c3da19bcb67ef258278e9862e88`, igual byte a byte ao um.py **v379** custodiado |
| α e β carregados | α=0,0072973525693 e β=α√e=0,012031300400803142; valores coincidem com o programa corrente |
| Instrumento | RTX 5090, CUDA; 31,8 GiB de VRAM total; disponível na consulta |

Fontes: LIVE_STATE_FULL_R1.json, RUNTIME_COMPARISON_R1.json e VERSION_IDENTITY_R1.json. A igualdade numérica de α/β foi verificada; ela não certifica as equações, fontes, escala de cada canal ou função de veredito. O hash antigo é a **proveniência da leitura de α**, não prova de que todo código em RAM corresponda à v379: o motor é separado do um.py. Não existe, no estado exposto, uma impressão criptográfica de todos os módulos residentes. Mtime de disco tampouco a substitui.

## Matriz por canal

| Canal/formato | O que já existe | Adequação ao teste atual |
|---|---|---|
| Cosmologia GPU | Fundo V3, CAMB interpolado, modos selado/corrigido/tgl/artigo, covariâncias e controles históricos | **Condicional ao modo, domínio e fontes explicitados.** O padrão é selado/nu, preservado para reprodução; tgl usa as correções e mapa efetivo. Não se deve deixar o modo implícito. |
| Pantheon/SH0ES/cronômetros | Leituras e covariâncias; PantheonCov está ligado no motor | Reaproveitável sob contrato; parte da documentação antiga ainda diz que a covariância não está ligada. Não confundir disponibilidade com independência dos conjuntos. |
| N_eff | Canal lê frozen de agosto e apresenta medidas/poder | **Correção pendente de instalação.** Ainda herda CMB-SPA 2,97±0,12, linha já corrigida pela F5.2. Candidato R3 existe; escolha de convenção/admissão mantém os atos vigentes. |
| Neutrinos F7.2 v2 | Conferência por hash das fontes e modelos publicados | **Proveniência, não executor espectral.** Retorna SEM_LIMITE_TGL; τ★ TGL e mapeamento permanecem nulos/abertos. Depende do túnel e retrato v369; cópia R8 externa é inerte. |
| Ia, massa e luminosidade | Sensibilidades e inventários SN1/NU2 em sandbox | **Não há canal instalado identificado que encadeie operador → emissão/transporte → EOS/Ye → luminosidade com resposta do detector e covariâncias.** A lacuna física já consta dos inventários; não se resolve trocando um formato de arquivo. |
| GW | ECO Fase 6 V3/V4/V5, séries NPZ, filtros e empilhamento | **Histórico específico.** Não implementa automaticamente ringdown do ramo B nem F4.3 220+440. Relógio do eco e τ★ do dissipador precisam de contratos separados. |
| Fase 9 | Runner histórico V1 na Bancada; R5.2/E1 no túnel | **Identidades distintas.** O candidato recente aceita apenas synthetic_only; não é atualização instalada. X13/D-H e demais atos mantêm o alcance vigente. |
| Lago de dados | FITS/NPY/NPZ/CSV/DAT/TXT e ferramentas de colunas/histogramas/mapas | Formatos de armazenamento disponíveis não constituem verossimilhança nem matching físico do novo teste. |

## Achados que podem mudar números ou interpretações

1. **Modo histórico como padrão.** mcp_um.py oferece tgl/eff e artigo/d1b, mas preserva defaults históricos. A solução é seleção explícita por teste, com um recibo de opções; não apagar a reprodução histórica.
2. **Curvas versus opções.** A leitura estática de evidencia.py identifica _curvas(th) sem transmissão das opções do ajuste. No modo artigo isso pode exibir uma curva com β no fundo, embora o contrato desse modo use β só na lei. A reprodução delimitada e as linhas ficam no inventário do motor; não é inferência sobre um resultado observado novo.
3. **Combinações sobrepostas.** A API tem conjuntos distintos que compartilham dados. Não deve somar DR1/DR2 ou Pantheon/Pantheon+SH0ES/SH0ES por omissão e interpretar como medidas independentes. Repetir um identificador não duplica o termo de χ² por membership, mas pode duplicar contagem de n_dados; ver inventário do motor.
4. **Domínio CAMB.** A tabela é finita e recusa pontos fora do suporte. Isso é proteção numérica, mas não representa um prior físico: o domínio útil cobre apenas uma fração do prior amplo. Uma evidência bayesiana não deve normalizar pelo prior completo e tratar falha do instrumento como probabilidade física zero.
5. **Fonte N_eff antiga.** A correção por fonte é material. Reiniciar o processo sem instalar o candidato auditado não a altera.
6. **Guarda de formatos.** Há lacunas estáticas em validações de entrada GW e N_eff, detalhadas pelos inventários. Nenhuma corrupção de amostra foi observada nesta verificação.
7. **Validações visíveis como null.** /api/estado procura a chave resumo_curto. Os arquivos corrigido/Pantheon têm outros esquemas e vereditos existentes. O null da interface não prova que a validação não exista ou tenha falhado; também não certifica compatibilidade com todo o programa atual.

## Escala para a questão dos neutrinos

A v388 distingue β₀ de fronteira e β(χ) de bulk. O dephasing vigente usa β₀ constante, segundo as fontes relidas na NU2. Não inserir β(E) em todos os canais como uma atualização geral: o vínculo χ↔escala física e a incidência em taxas fracas/EOS precisam de derivação própria. Igualmente, não trocar a textura (Δm²ij)² pela textura do limite JUNO publicado, nem transformar desfasamento em perda de energia.

O cálculo sintético NU2 permanece válido no escopo explicitado: τ★=tP e Kfac=1 são hipóteses; o número muito pequeno obtido não é medição real nem exclusão de todos os regimes da TGL. Ele não depende de uma suposta compatibilidade automática da Bancada.

## Adequação concreta necessária antes de um teste novo

- Fixar o snapshot do programa e selo, mais hashes do executor e de suas dependências, e conferir isso no processo efetivamente carregado.
- Um manifesto por teste deve declarar: observável, operador, regime, β₀ ou β(χ), origem de χ, τ★, curvatura, relógio, unidades, quadros de referência e modos/covariâncias. Campos físicos não resolvidos devem recusar execução física, não receber valores silenciosos.
- Pinar resposta do detector, fontes, transformações, seleção e correlações. No canal proposto, registrar a textura completa Γij, massa/energia em unidades explícitas e se o estado inicial já é incoerente.
- Corrigir em sandbox as divergências técnicas demonstradas; reaproveitar os candidatos F5.2/F7.2/F3.2 e auxiliares históricos que já foram verificados, preservando seus limites.
- Validar com controles sintéticos e referência independente. Uma recarga posterior precisa emitir recibo do que carregou e recusar hashes diferentes. Só depois atribuir um resultado ao contrato identificado.

**Esta entrega verifica e especifica; não implanta.** A regra expressa do operador/gerência de 08/10 exige evento da c1 nomeando qualquer gravação na Bancada; a recarga mantém o ato próprio X17. Não houve pedido de aprovação nova aqui nem mensagem a Claude/provedores. Nada moveu o gate.

## Evidência e limites

As leituras detalhadas estão em motor_inventory, channels_inventory e gw_f9_inventory. A consulta prévia reaproveitou F0.3, infra.bancada_um.validacao, F5.2, F7.2 e as entregas F3.1/F3.2; F0.3.B1 ainda não estava no grafo e isso foi registrado. Esta auditoria não reproduziu todas as inferências históricas, não examinou toda a memória do processo e não certifica dados cegos. O número de ferramentas é o das declarações MCP em disco, não contagem de módulos de física.
