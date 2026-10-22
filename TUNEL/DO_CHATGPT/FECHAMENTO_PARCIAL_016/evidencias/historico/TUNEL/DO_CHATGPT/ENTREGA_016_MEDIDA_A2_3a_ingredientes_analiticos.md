[REAL] A-2.3.a em curso — ingredientes analíticos e core gaussiano em L1/L2.

Abertura SHA256: 216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a

[DERIVED — Lean isolado] Para m_a(z)=exp(i a exp z), provados holomorfia e |m_a(x+iy)|=exp(-a exp(x) sin(y)); a>=0 e y em [0,π] implicam contração. Para f_(b,r)(z)=exp(-b(z-r-iπ/2)^2), b>0, provadas holomorfia, torção f(x+iπ)=conj f(x), fórmula da norma, integrabilidade L1 e L2 de cada seção horizontal e majorante uniforme pela norma do bordo real. O produto m_a f herda a torção, L1, L2 e a majorante na faixa. Os lemas gaussianos da Mathlib foram reutilizados.

Quinze teoremas novos auditados, todos no trio permitido. Código 0 nas três pedras finais. Oito compilações totais: 3 na pedra analítica, 4 em L2 e 1 em L1; as cinco falhas foram preservadas. Restou um warning de tática redundante no passe L2, sem efeito no termo nem no auditor. Recursos totais 119.719000s parede e 119.046875s CPU; nenhum arquivo canônico alterado segundo os recibos.

[OPEN — este ramo ainda não foi entregue como PAGO] Ter torção e integrabilidade não foi promovido a pertencer ao K fechado. Faltam a correspondência Fourier/domínio no produto e a densidade do span REAL da família, para estender ao K inteiro. Tampouco foi provada unicidade de π ou meia-inclusão. Esses são passos separados; o alvo A2.3.a continua ativo, dentro de seu teto, sem recuo prematuro.

[INPUT/OPERAÇÃO] Pergunta específica ao MiMo preparada com request_id 4b84b6c7-4167-4ebb-ab89-129e9e1fd4b3, ainda não submetida, aguardando schema de executor obrigatório. Teto financeiro/tamanho artificial MiMo retirados do recibo após conferir as novas falas do operador na tarefa coordenadora (read_thread, mensagens 01a0d357-671a-7de1-ae66-192c6276126c e 01a0d357-672b-7562-9640-79d7796a4c7c). Nenhuma chamada remota científica feita nesta unidade. A resposta do modelo será rascunho, não prova nem execução local. Não move gate.

- C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A2\LightRayAnalyticCore_v3.lean — SHA256 64c0a9ca42a61ca754a3dc9e2c59aa206599fde7a861cd3d28abd774fdfb12a4
- C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A2\analytic_core_03.log — SHA256 b7cefd70e53c8647be37b2c5a80656a697205bdf6d2231660bce46a609d05e3c
- C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A2\analytic_core_03.json — SHA256 a83848562690d75f8cf11ccc968a3023d706bbc40cd891981fbd3c2d611b3ae0
- C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A2\LightRayGaussianL2_v4.lean — SHA256 d7971194dd2d94549a0d9a1a6cbdbe636641d8ea21c8b97a996fd4f309678afa
- C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A2\gaussian_l2_04.log — SHA256 2677704849eb1f45ce57dcaf4f376a0ae6c7ff92aaf6f5e750ce01b0eb125975
- C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A2\gaussian_l2_04.json — SHA256 de90384eb071b474841b0c934bc46955c0c036972305eae3868233dac52854b4
- C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A2\LightRayGaussianL1.lean — SHA256 684140e5d40badb32218144a0c22a44ea753bfb02494383d3e7b6ccfc3b6fdb9
- C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A2\gaussian_l1_01.log — SHA256 d3741da2de923012752e303455c653a18729e50a310b08573c91c8b19e9c95ab
- C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A2\gaussian_l1_01.json — SHA256 2560b5551d67891b9ee56b213c4a2715bb9e737417775313998927e1bf5a557c
Manifesto: C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A2\analytic_checkpoint_manifest.json — 02cd40977e4aafc9f287290757eec4385d58065222951a7244e9c16b6f0ec3e0
Auditor: C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A2\analytic_core_axioms.json — 99d222e854165288b844d029ab839d38e48e3d0a7c76300e43c1c86330e18e95
