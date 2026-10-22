[REAL] A-1.b1 — controle não comutante e rejeição por fidelidade.

Abertura SHA256: 216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a

[DERIVED — Lean isolado] V=C³, Ω=e0; U(a)=diag(1,exp(i*a0),1); D(t) fixa e0 e gira o plano (e1,e2). Foram provadas continuidade, leis de grupo, unitariedade matricial e preservação de Ω. Para a=(π,0,0,0), t=π/2 e ψ=e1, D(t)U(a)ψ≠U(a)D(t)ψ. Assim o controle está fora da hipótese de commuting_translations_excluded.

Mas U(0,1,0,0)=I. O teorema contract_rejects_this_translation_action recebe o ContratoH2 REAL e uma leitura injetiva entrelaçando suas translações com o controle; deriva contradição precisamente de translations_faithful. Não usa a parede de comutação. Não se construiu W, rede ou realização modular a partir das matrizes, nem se identificou D com um fluxo modular verdadeiro. Esta é uma rejeição condicional por campo, não um arquivo negativo rc 1 de preenchimento do registro.

Quatro compilações; rc final 0; 16 declarações auditadas no trio, sem sorry/axioma novo. As falhas iniciais eram de redução de notação e conjugação dos coeficientes reais. ERRO OPERACIONAL preservado: v3 ficou byte-idêntica a v2 (True), pois a substituição não encontrou o texto; sua repetição não foi avanço matemático. Após diagnosticar isso, v4 aplica a mudança com assert e fecha. Não excedeu seis ciclos.

Fonte C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A1\probes\ProbeNoncommutingInternal_v4.lean SHA256 524b65f8bd77c2c7b3a4142cebc747a9f8771a92613dbf99433f781a0ef8dd6e
Log C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A1\probes\noncommuting_internal_04.log SHA256 ccad284f37e14b3df561f598fa28f6d79108c570fff023ba94d1aa88449aefbc
Recibo/comando C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A1\probes\noncommuting_internal_04.json SHA256 f532ef22fd1dcc14357ac9b131a68afec121cb2ae9c172bc52d19eec44a20043
Auditoria C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A1\probes\noncommuting_internal_axioms.json SHA256 e41c9cf9a08d6b9b17c65d3a0b851d84189998dd9b1a62b02d7e7bf91b03e4dc
Passe final: 25.203999999997905s parede; 24.859375s CPU; pico committed 8486883328 bytes; zero alteração canônica detectada. Não move gate. Próximo A-2.1.
