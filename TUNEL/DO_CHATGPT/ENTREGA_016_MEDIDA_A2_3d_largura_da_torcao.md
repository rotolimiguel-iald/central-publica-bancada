[DERIVED — compilação isolada auditada; revisão externa da meia-inclusão pendente]

# A-2.3.d — largura da torção

Data UTC: 2026-09-24T13:52:26.874176+00:00. ABERTURA sha256: `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`.

Para a>0 e 0<w<2π, foi compilada a equivalência:
`(∀ x, m_a(x+iw) = conj(m_a(x))) ↔ w=π`, onde `m_a(z)=exp(i a exp(z))`.
O módulo no ponto x=0 força sin(w)=0; o intervalo aberto seleciona π.
8 declarações auditadas, rc 0, axiomas apenas propext/Classical.choice/Quot.sound,
sem sorry e sem alteração detectada no kernel.

Controles demonstrados: torção falha em π/2 e 3π/2 para a>0;
para a<0, |m_a(iπ/2)|>1; para a=0, a torção vale para toda largura.
Falha de contração não foi promovida a falha da isotonia. A equivalência não demonstra
que π é a única largura de isotonia em todo regime nem identifica sozinha potências
modulares ilimitadas. A-2.3.d+ permanece opcional; o cético do teorema principal está em execução.

Comando: `C:\Python314\python.exe -X utf8 -B A0\compile_isolated_v2.py <kernel> A2\LightRayTwistWidth_v3.lean twist_width_04 <A2>`.
Tentativas anteriores preservadas: v1 falhou na coerção do zero na norma; v2 corrigiu o
lado da faixa e v3 corrigiu a mesma coerção no lado real. Uma tentativa intermediária
não iniciou elaboração por sandbox negar acesso a dependências; log preservado.
Máquina acumulada: 41.090 s parede, 41.000 s CPU. Bancada decorrida: 444.487 s.
Nenhuma chamada remota nova nesta etapa; total monetário conhecido no ledger: US$ 0.159306135.
Valores não informados pelos provedores continuam desconhecidos.

Fonte sha256: `bc283090a6269da1fd59717252c553da945213277857496c76985eede5ef2828`.
Log sha256: `891bfc145f0a1e814bd76e1eb2201fea60a4d2ec37a59e4cc3064035386d0bb4`.
Manifesto completo: `C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A2\twist_width_manifest.json`.
Não move o gate. Próximo alvo: A-2.4, âncoras do vácuo; depois A-2.5.
