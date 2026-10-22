[REAL] A-2.1 — pontes dos quatro boosts compiladas.

Abertura SHA256: 216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a

A-2.1.1: BoostHomonymBridge reproduzida byte a byte; boost4=boostMat e a exclusão de entrelaçamento isométrico injetivo para rapidez não nula passam com rc 0.
A-2.1.2: boostMatrix(rate,s)=P13*boostMat(-(rate*s))*P13, onde P13 troca coordenadas 1 e 3 e P13²=I. O sinal e a troca de plano são explicitamente provados sobre as declarações reais importadas.
A-2.1.3: boost(s) 2×2 coincide por entradas com o bloco 0,1 de boostMat(s). Isso não declara idênticas todas as convenções de assinatura/ordem de coordenadas da literatura.
A-2.1.4: lei de grupo de boost4 herdada de theBoost_add via a ponte; identidade em zero também compilada.

Nove declarações auditadas no trio permitido, sem sorry/axioma novo. Não se repetiu a demonstração da lei de grupo ou da exclusão: foram reutilizadas. Fontes fora do kernel; duas compilações rc 0, zero alterações canônicas detectadas. Tempo dos passes: 0.014223056h parede e 0.014062500h CPU. Nenhuma chamada remota ou máquina pesada B nesta entrega.

Fonte C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A2\BoostHomonymBridge.lean SHA256 36b82810e2850942b43ec5456df0481ff8f4e039fb5af8da3d5f102ec558ea6f
Log C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A2\boost_homonym_01.log SHA256 89ce58bf751002448dcc2c25bb64dcdbb46575c928e6e483e551757cff16af80
Comando/recibo C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A2\boost_homonym_01.json SHA256 ca9db059e0263fe5ad0cec2bf320f16910f39457d086373079fc35a5c6414e3a

Fonte C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A2\BoostRepresentationBridges.lean SHA256 f5d0834440a9d3455bc2d3f97d0b107d4a5a351b9f6966b876a54b8bf3395d68
Log C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A2\boost_bridges_01.log SHA256 5887483a95a25804120c0b5d7e7bb212bff9ad0e2ec642483db6175d85b8a548
Comando/recibo C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A2\boost_bridges_01.json SHA256 17980613af9c83b14ef5f96ab7037bc802ac08c866230f33c13a017d21424185

Manifesto C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A2\boost_bridges_manifest.json SHA256 1e255b17b1814b6620ab44d080f256c4f86a6077fdd996f2d0cfbbce70c47079.
Não move o gate: remove ambiguidades entre representações existentes. Próximo A-2.2: Fourier–Plancherel e a constante c0.
