# F0.3.B1 — auditoria estática do motor cosmológico da Bancada

Autor: codex-gerente-tgl / nu2_theory_sources. Reivindicação 621. [REAL documental e controle sintético] Escopo: fontes.py, motor.py, fundo_gpu.py, camb_tabela.py, regua.py, evidencia.py; dependência PantheonCov; validações existentes e decisão de R. Nenhum módulo original foi importado, Motor foi instanciado, fit foi rodado, arquivo de dados observados foi analisado ou byte foi gravado na Bancada. Foram lidos código e recibos históricos (não é nova análise cega). O processo residente é auditoria separada do coordenador.

## Conclusão

**O motor tem a reprodução V3, as correções, o mapa efetivo e D1b; não está certificado como instrumento genérico de nova significância de 5 sigma.** Há um defeito concreto de seleção de regime nas curvas, aceitação de composições sobrepostas, suporte de tabela menor que o prior e limites estatísticos/de custódia. A versão do um.py lida é v391, hash 8e7b9927ceae64b8b6812019f77cca24c08296222ae7968af41baf2fe7a67dc6. Isso não determina a versão residente de cada módulo da Bancada.

## O que está adequado e deve ser reaproveitado

- [REAL] alpha_codata_2018 lê ALPHA_FINE_CODATA_2018 no um.py e confronta com o pipeline D1 (fontes.py:51–62); Motor:83–84 calcula beta=alpha*sqrt(e) em runtime. Os valores conferem. Não há necessidade de substituir beta0 por beta(E); v388 separa bulk e fronteira, como documentado no ramo NU2.
- [REAL] pipeline D1 e tabela CAMB conferem com seus manifestos por SHA-256 na leitura desta auditoria. O JSON de inventário contém os 22 arquivos e hashes completos.
- [REAL] Os quatro presets são distintos e explícitos (motor.py:24–44):

| modo | covariâncias / distância de recombinação | R | lei | beta no fundo |
|---|---|---|---|---|
| selado, default | históricas / direto | nu | d1a | sim |
| corrigido | Chen+DR1 correlacionado / razão CAMB | nu | d1a | sim |
| tgl | corrigidas / razão CAMB | efetivo | d1a | sim |
| artigo | corrigidas / razão CAMB | nu | d1b | não |

O default antigo é intencional para reprodução. A decisão 30/09 sobre R efetivo está no próprio código:30–32 e no arquivo CONFIRMACAO_OPERADOR_MAPA_R_30SET.json pinado. Isso não autoriza misturar os quatro regimes num mesmo teste; requer escolher e registrar opções completas.

- [REAL] D1b usa I=(2/3)ln(E_LCDM), K=exp(beta I), fundo beta=0 em modo artigo (motor:166,184–198). O código alerta sobre contar beta duas vezes ao empilhar lei e fundo beta (36–40).
- [REAL] PantheonCov ESTÁ ligado: motor:119–121 constrói amostras com e sem calibradores, covariância STAT+SYS e M profilado. A afirmação antiga em fontes.py:196–208 de que a covariância não está ligada é stale; não deve virar diagnóstico de ausência.
- [REAL documental; não reexecutado] validacao_bancada.json, 01/10, registra reprodução D1 V3: erro máximo tabela 6,5443e-6 e fundo/worker 2,5456e-9. validacao_corrigido.json, 28/09, registra oito casos aprovados contra referências. validacao_pantheon.json registra a ligação e controle externo. São evidências históricas delimitadas, não certificação de todos os modos atuais ou do processo residente.

## Achados materiais antes de novos testes

### M1 — as curvas não seguem as opções da predição

Evidencia.avaliar:52 chama `_curvas(th)` sem `opcoes`; `_curvas`:64–72 sempre passa beta ao fundo. No modo artigo, a predição do motor usa beta_f=0 (motor:166). Assim o χ²/predito pode seguir o regime artigo, enquanto o painel de curvas mostra outro fundo.

[REAL — sonda AST com mocks simbólicos] PROBE_AST_SINTETICO_20261009.json extraiu as funções do código verificado por hash, sem importar módulo, usar GPU, dados ou calcular distâncias. Com beta=alpha*sqrt(e), interceptou a primeira chamada ao fundo: **esperado no artigo 0; passado pelas curvas 0,012031300400803142**. A sonda comprova o encaminhamento errado, não mede o erro nas curvas físicas.

Correção necessária: curvas receberem e aplicarem o mesmo objeto completo de opções, ou apresentarem-se explicitamente como outra projeção diagnóstica separada. Revalidar com sintético antes de reutilizar.

### M2 — composição observacional aceita sobreposição

Evidencia.avaliar sem conjuntos usa CONJUNTOS inteiro (47); inclui DESI DR1+DR2, Pantheon+Pantheon+SH0ES e SH0ES em duas leituras. Motor.chi2 soma termos distintos sem covariância cruzada ou exclusão dessa sobreposição. _conj:22–27 só confere nomes. A sonda AST reproduziu a aceitação da lista sobreposta e de IDs duplicados.

Precisão: o mesmo ID duplicado não dobra seu termo χ² porque o motor testa pertencimento; porém n_dados soma a lista recebida e dobra a contagem. Já IDs diferentes que compartilham observações entram como termos separados. A saída avaliar é DIAGNOSTICO, o que reduz o alcance da alegação; ela não deve ser promovida a evidência conjunta válida. Ajustar/comparar/amostrar também aceitam listas sobrepostas se fornecidas.

Correção necessária: conjuntos mutuamente exclusivos ou uma likelihood conjunta com correlações justificadas, e recusa explícita de duplicatas. O default de avaliar precisa ser lido como painel de diagnósticos, sem um total interpretável como teste composto.

### M3 — tabela cobre 4,32% do prior tridimensional declarado

O manifesto teórico tem grade bruta H0=[58,78], wb=[.020,.025], wc=[.100,.140]. A máscara em camb_tabela.py:50–69 exclui uma célula em cada ponta: suporte útil H0=[60,76], wb=[.02025,.02475], wc=[.102,.138]. O LIMITES do pipeline efetivamente carregado é H0=[50,90], wb=[.015,.030], wc=[.080,.180]. A razão de volumes, calculada só com metadados, é 0,0432.

Motor:159–162 e chi2:272–273 (ver faixa pinada) impõem simultaneamente prior e suporte, recusando fora da tabela com +infinito. Para posterior/evidência sobre o prior amplo, isso introduz um recorte instrumental não declarado como novo prior. A fração é de volume, **não de massa posterior**. Não invalida automaticamente o ajuste histórico interior, mas impede tratar a tabela como cobertura do prior inteiro. O índice vivo já registrava esta limitação; reaproveitar a rota e não simular correção por extrapolação silenciosa.

### M4 — “significância global” precisa de calibração

regua.py:88–97 usa Šidák só pelo número de famílias; as famílias compartilham dados e nem sequer são garantidamente testes independentes. A contagem não fornece, por si só, controle de erro global nesse cenário. evidencia.py:156–174 usa Wilks com um grau de liberdade como aproximação; requer regularidade, solução interior e comportamento do estimador, não apenas uma chamada a sqrt(Deltaχ²).

Mais diretamente, evidencia.py:209–225 transforma massa de cauda do posterior em p bilateral e depois aplica a mesma correção frequentista. Uma cauda posterior condicionada ao prior/modelo não é automaticamente p-valor calibrado sob hipótese nula. O estatuto POSTERIOR_CONDICIONAL permanece útil; a transformação não sustenta sozinha anúncio de sigma experimental.

Correção necessária: separar resumo posterior, perfil assintótico e teste calibrado, com função de veredito específica; simulações sintéticas completas para tamanho/poder antes do uso de “5 sigma”. Não transformar lnB ou quantidade de chamadas em significância.

### M5 — proveniência calculada não é sempre pin de admissão

fontes.py:95–117 compara cópias existentes de DR2, mas não exige uma cópia nem um hash externo fixo; se todas mudassem juntas, a checagem de igualdade não certificaria bytes previamente admitidos. Cronômetros:126–157 checam forma/positividade e registram SHA atual; não confrontam os JSON com um pin imutável. Planck Chen:163–174 pode devolver covariância mesmo sem PDF (`pdf_sha256=None`). PantheonCov:26–45 aceita cache .npy se o metadata conserva o SHA da fonte, sem verificar hash do próprio cache carregado.

São graus diferentes de custódia, não prova de adulteração atual. O novo teste precisa pinar todos os bytes consumidos e a política de admissão que o rege. O hash do um.py registrado por alpha_codata_2018 não garante atualização automática das equações do motor.

## Limites físicos e operacionais

O fundo é a aproximação V3 em densidades de radiação+matéria+Lambda (fundo_gpu.py:87–126), parâmetros fixos do CAMB2.0.4 (mnu=.06, Neff=3.046, TCMB=2.7255) no manifesto. O modo corrigido usa razões contra CAMB para o viés de neutrino massivo no observável recombinação (motor:174–177). Não é solver de perturbações cosmológicas, transporte de neutrinos, EOS estelar ou luminosidade de SN. Não ligar um nome de versão v391 a capacidades ausentes desse tipo de motor.

Nenhum validadores original foi rodado: eles podem ajustar dados, gravar resultados ou criar SQLite (validar_tudo:73; validar_corrigido:18–20,64–65; PantheonCov pode regenerar cache). A auditoria residente, reload e qualquer implantação são separados. Não se escreveu na Bancada.

## Entrega

INVENTARIO_MOTOR_20261009.json: 22 fontes pinadas, opções extraídas por AST, constantes, suporte e recibos históricos. PROBE_AST_SINTETICO_20261009.json: bug de modo nas curvas e seleção reproduzidos com mocks. Scripts próprios preservados nesta pasta, sem alterar código instalado. Veredicto desta subunidade: **ADEQUADO_PARA_REPRODUCAO_DELIMITADA; RESSALVAS_MATERIAIS_PARA_TESTE_NOVO**. Nenhum gate ou sigma empírico novo.
