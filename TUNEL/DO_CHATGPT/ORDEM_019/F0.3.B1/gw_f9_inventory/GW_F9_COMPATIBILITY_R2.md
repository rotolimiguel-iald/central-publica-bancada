# F0.3.B1 — compatibilidade GW e Fase 9, inventário R2

Autor: Codex / nu2_skeptic. Unidade reivindicada 621. Leitura estática em 09/10/2026; nenhum ajuste, série cega, catálogo de eventos, posterior ou resultado de estágio foi aberto. Esta verificação não certifica a versão em RAM.

## Resultado

**COMPATIBILIDADE PARCIAL E COM ESCOPO HISTÓRICO.** O módulo GW implementa a Fase 6 ECO V3/V4/V5, e quatro auxiliares coincidem por AST integral com o pipeline V3; o quinto difere somente pela docstring e tem o mesmo AST executável. Isso não o torna executor do ramo B ringdown nem do diagnóstico 220+440. A Fase 9 disponível em `investigacao/fase9_hubble_abertura` continua sendo o runner V1; o candidato R5.2/E1 existe no túnel, deliberadamente sem abertura física.

## GW: contrato existente e limite

- `mcp_um.py:123–182`, `gw.py:31–34,74,153–157,228–267`: nove ferramentas GW expõem ECO V3/V4/V5. `gw_rodar` usa sempre `rodar_fase6.py`, default `stage=tudo`; só `stage=cego` vira `--so-cego`. Não é ferramenta para testar silenciosamente o ramo B. Nenhuma foi chamada nesta revisão.
- `gw.py:95–120`: catálogo CSV com `commonName`, GPS, src, era, massas, redshift e SNR; duas séries esperadas H1/L1 por evento. Arquivos NPZ `<evento>_<detector>_4096_32s.npz`, chaves `t`, `strain`, `fs`; detector frame na massa remanescente. As séries residem em caches históricos e `fontes_externas/gwosc_o4/strain_32s`.
- `gw.py:27–28,43–68`: 4096 Hz, janela 32s prevista, highpass15Hz, Tukey0,1, Welch Hann4s e 50%, banda20–1024Hz, PSD em t_rel(-14,4;-2). Quatro funções têm AST integral idêntica ao `echo_anchored_v3.py`: mad, welch, band_mask, whiten32. precondition difere somente pela docstring; retirando apenas docstrings, as cinco têm AST executável idêntica [REAL estático]. Não houve avaliação numérica das séries.
- `gw.py:109–120`: o validador do carregamento recusa NaN e fs diferente; não demonstra por si só shape de32s, monotonicidade/uniformidade de t ou ausência de Inf. São lacunas estáticas do contrato de entrada, não corrupção observada.
- `gw.py:128–135,232`: estágios são relidos por mtime, com sha16 informativo; o empilhamento usa critérios/leituras padrão se o pré-registro estiver ausente. A resposta é explicitamente consulta não selada. Esse mecanismo não substitui verificação de pins para novo teste. O executor histórico `rodar_fase6.py:19–24` verifica pipeline, catálogo e séries antes da rodada; não o executei.
- `gw.py:29` e pipeline V3: alfa literal seguido de beta=alfa*sqrt(e), sem corrida espectral. O número pode coincidir com o atual, mas não há vínculo por hash à versão corrente do um.py nesses dois módulos.

## Relógios: não encadear os nomes

`echo_anchored_v3.py:54–56` usa KMS como **atraso do eco**: 4pi(1+sqrt(1-a²))/sqrt(1-a²) GM_f/c³. O ramo B usa a mesma escala como hipótese de **tau_star do dissipador**. Coincidência algébrica não faz a ferramenta de eco calcular amortecimento da envoltória.

A `ERRATA_B2_K.md` separa o Fisher antigo R-B, k=1, da hipótese primária ringdown k=2pi/kappa_hat(a_f). `tgl_ringdown_prediction.py:65–84,108–128` mantém ramos distintos. O V1 ringdown pinado especifica massa M_f no referencial detector, efeito na fonte e delta_tau=-x/(1+x), x=beta k N. O Fisher k=1 não é poder da hipótese com k modular. A F4.3 continua diagnóstico documental, sem campanha de injeções validada nesta revisão.

## Fase 9: V1 da Bancada versus R5.2/E1

- `rodar_fase9_v1.py:1–15,22–25,44–50`: executor histórico da abertura de06/10, fixa V1 por spec e função. Sua docstring declara quadratura n=25 e fundo marginalizado. Não importa o gate/candidato E1.
- `f9_reader_gate_v1x_e1_bytes.py:22–42,86–110`: novo vínculo, oito leitores tipados; cinco masers decisórios e seis apenas diagnóstico; relê os bytes dos cinco ancestrais. O spec E1 é distinto do V1 e ambos foram recomputados do JSON nesta revisão.
- `f9_runner_v1x_preflight_e1_bytes.py:110–129`: X13 e D-H pendentes, V2 não congelada, nenhum dado aberto, nenhum veredito físico. `f9_runner_v1x_staged_e1_bytes.py:487–509` recusa todo modo diferente de synthetic_only; `:414` fixa required_sources_admitted=False, coerente com o rascunho.
- O candidato pinado contém mu_do_rito Thomson, demais atos do operador (incluindo d72), guardas de finitude e regra das duas testemunhas. Sua existência não é instalação na Bancada. A consulta ao mapa reconhece a última camada portable da F3.2 e determina aguardar X13/D-H, sem refazer a cadeia sem achado material.
- `mcp_um.py`, `um_bancada.py` e `gw.py` não contêm entrada dedicada para f9_reader_gate/f9_runner_v1x/R5_2. Ausência limitada a esses arquivos; scripts avulsos de investigação permanecem em disco.

## Consequência operacional

Preservar ECO e V1 para reprodução histórica identificada. Para ciência nova, o despachante deve selecionar explicitamente contrato, relógio, versão e identidade dos dados; não herdar `gw_rodar` ou `rodar_fase9_v1.py` pelo nome genérico Bancada. Um candidato novo pode reutilizar os auxiliares demonstrados, mantendo as pendências documentais vigentes. Esta nota não autoriza implantação, recarga ou abertura.

Hashes, linhas e comparação AST estão em `GW_F9_INVENTORY_R1.json`; as consultas prévias ao Nós e ao mapa foram custodiadas em QUERY_*.txt. F0.3.B1 ainda não está no grafo, por isso foi usado F0.3; nada foi reconstruído.

## Correção de redação em R2

O R1 foi preservado. A redação antecipou cinco ASTs integrais iguais antes de inspecionar a saída; a medição deu quatro. O quinto difere apenas pela docstring. A correção e os hashes estão em GW_F9_AST_CORRECTION_R2.json. Nenhuma conclusão física foi alterada.
