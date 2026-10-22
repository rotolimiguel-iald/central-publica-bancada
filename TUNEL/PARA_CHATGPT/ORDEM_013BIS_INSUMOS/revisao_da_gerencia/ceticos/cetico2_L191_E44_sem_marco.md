# CÉTICO 2 — achado executabilidade_tunel, ORDEM 013-bis l.191 (E4.4): alvo sem marco

**Veredito: refutado = false (achado CONFIRMADO por releitura literal). Gravidade: IMPORTANTE (mantida).**

## Medido (grep -n na ordem, 22/09/2026)
- l.191: E4.4 = «a lista dos que passam o corte pré-análise de E0.3 em cada corrida pública; o GW250207_115645 (O4c) marcado como evento de teste (cego) quando sair».
- l.210 (§4.1): «E2 + E5 + E4.1–4.3 (MB2)»; l.229: «MB2 — E2 + E5 + E4.1–4.3»; l.230: «MB3 — E3.1 + E3.2 + E6»; l.231: «MB4 — E3.3 + E7». E4.4 não aparece em MA, MB1–MB4 nem no marco «Teste» (l.232).
- `PROMPT_CODEX_ORDEM_013BIS.txt` l.7 repete «E4.1–4.3 (o modo 440)». `parteB_ampliacao.md` l.97/l.116 idem (rascunho-fonte).
- E4 Aceitação (l.192: «tabela por leitura × detector») não cobre a lista nem a marcação; E0.3 (l.149) pede só a CONTAGEM em GWOSC, não a lista; E6 (l.204) depende de «E0/E1/E4/E5».

## Tentativa de refutação (falhou)
(i) «E4.4 é a lista implícita na contagem de E0.3» — a ordem não o diz; contagem ≠ lista, e a bancada pode entregar «5 com SNR ≥ 30» sem nomear os eventos. (ii) «A marcação do GW250207 é futura ("quando sair")» — mas a marcação é ato do REGISTRO (E2.1: teste = eventos publicados depois do hash), que é MB2; se não for escrita no registro antes do hash, o evento entra no teste sem pré-registro nominal. (iii) «Vale a ordem, não o prompt» (l.284) — a ordem também omite. A lição da C6 (alvo sem recibo → omitido) aplica-se literalmente.

## Correção FINAL (texto exato; estilo e estatutos mantidos)
- l.210: substituir «**E2 + E5 + E4.1–4.3 (MB2)**» por «**E2 + E5 + E4.1–4.4 (MB2)**».
- l.229: substituir «**MB2** — E2 + E5 + E4.1–4.3:» por «**MB2** — E2 + E5 + E4.1–4.4 (a lista de E4.4 é a dos eventos contados em E0.3, nomeados; o GW250207_115645 entra no registro E2.1 como evento de teste nominal, cego):».
- `PROMPT_CODEX_ORDEM_013BIS.txt` l.7: «+ E4.1–4.3 (o modo 440)» → «+ E4.1–4.4 (o modo 440 e a lista nominal dos eventos de SNR alto)». Regenerar o sha16 do prompt no manifesto (l.284) por script.
