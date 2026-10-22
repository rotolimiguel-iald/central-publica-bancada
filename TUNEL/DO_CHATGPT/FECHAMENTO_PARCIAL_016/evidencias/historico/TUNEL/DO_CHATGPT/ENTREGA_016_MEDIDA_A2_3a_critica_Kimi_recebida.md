[DECLARADO — crítica externa recebida; testes formais adicionais ainda não executados]

# A-2.3.a — recibo da crítica Kimi

Data UTC: 2026-09-24T14:02:20.463465+00:00. ABERTURA sha256: `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`.
Uma única execução Kimi K3 MAX, task `f0e1a3b8-d8b8-47af-9cf1-79b4a5528153`, encerrada em result_ready.
Resposta preservada em `C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A2\a23_kimi_mutation_answer.md`; sha256 `d5e6ed2fa42b1d806bc583484609f710f45727623fdf64fbbdd7ce8e6a8e510d`.
Uso informado: `{"prompt_tokens": 317629, "completion_tokens": 31097, "cached_input_tokens": 0, "total_tokens": 348726}`.
Tempo informado: 868.779 s. Custo monetário não informado.

A crítica reconhece a densidade REAL agora demonstrada e o alcance de halfline_isotony:
subespaço real padrão 1+1 para a≥0. Não apontou contradição nessa conclusão, mas não
compilou nem recebeu todos os corpos dependentes. Isso não substitui a auditoria Lean.

Propõe três controles: sinal negativo (crescimento em fatia interna), π/2 (torção de
borda falha), 3π/2 (borda e crescimento interno). A-2.3.d, compilado durante a chamada,
já prova falha da TORÇÃO nessas duas larguras e falha da CONTRAÇÃO para a<0.
Isso não basta para provar não-pertença ao subespaço padrão. O próprio crítico identifica
a dependência ainda necessária no controle de sinal: a direção inversa da ponte de
faixa de Paley–Wiener, ou uma prova direta de não-integrabilidade espectral.

Correção de alcance à resposta: integração numérica em truncamentos finitos não prova
divergência até infinito nem dispensa essa ponte para concluir não-isotonia. A afirmação
final do crítico de que os três probes já verificam a necessidade das hipóteses é,
neste estado, um roteiro analítico, não três testes executados pela bancada.
Também não se transporta a falha de elaboração de um argumento à falsidade da proposição.

Próximo: registrar controles explícitos no escopo analítico e discriminar a ponte ainda
não formalizada; seguir A-2.5 sem reabrir a prova de densidade já auditada.
Nenhuma alteração de kernel/gate. Nenhuma reexecução da unidade.
