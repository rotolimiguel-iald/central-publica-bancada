# Cético — proposta C-01 (erratas documentais ao lado), ORDEM 013-bis

Fontes lidas por script (sha16): E0_CORE.json ce5fa2f3bfc98513 · PORTAO_DA_AMPLIACAO_V1.json 710028a7d2af7b64 ·
RINGDOWN_5SIGMA_V1.json e1be6b0409720c68 · PUBLICATION_CENSUS.json 505eb16a608070ab · GWOSC_INVENTORY.json b5860044f456d5d5 ·
MANIFESTO_DOWNLOADS_013BIS_v2.json 2fb3898fe9607ecd · F0_CLOSED_20260922T215825Z.json 2e867cd824a6969d ·
E7_FULLSAMPLE_RESULT_V1.json c2f96864c18f3aea · QUADRO_DE_ALCANCE_V1.md 7b2e772c464033df · ORCAMENTO_40H.json 892e416585062eef ·
ordem 013-bis a907d07bc484b53c.

## Itens que sobrevivem (defeito real, errata cabe)
- F0: F0_CLOSED sem nome da ordem (string 'ORDEM'/'013BIS' ausente), signals=[] e after_processes=[] (jobs já mortos; último PROGRESS 20:00:30Z). OK.
- 1.ª linha: B1/B2/E2_REGISTRO abrem «[NÃO-CEGO — …]» sem estatuto; B3 abre «[REAL — …]» sem NÃO-CEGO (compara Kerr com posterior publicado). OK.
- Quadro E6 (.md): 'limite clássico' 0 ocorrências; coluna Taxa/IC OPEN em 2540/2540 linhas embora rate_contexts do JSON tenha IC90 [0,035; 3,27]/ano. OK.
- Parte A fora do ledger: ledger começa 19:06:33Z; Parte A 16:58Z→19:06Z ≈ 2,13 h; MA diz «orçamento só começa com seu registro». OK (frase ao lado).
- E0.6 herdado: E0_CORE/systematics/*/components[].magnitude_inherited com source = TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/.../C_piso_sinais_catalogo.json (JSON da gerência). Defeito real — MAS a ordem §4.0 manda «a bancada REFAZ, nunca copia»: rótulo 'herdado' não basta, tem de refazer.
- Composição 19/13/1: EXTRACTION_PLAN.json/events dataset = {pSEOBNRv5PHM-reweighted 19, pseob-rd 13, pSEOBNRv5PHM 1}. OK.
- E1.5 em σ: NUISANCE_V1 E1_5 = LOCAL_DESCRIPTIVE_DISTANCES_ONLY; frase cabe (números a computar pela bancada, não copiar).
- STATUS_013BIS: STATUS_ORDEM_013.json datado 13:04Z 22/09 (anterior à 013-bis), goal_status WORK_RESUMED_NOT_COMPLETE; a ordem (l.248) o deixa fora do recibo — não exigido; NOTA opcional.

## Itens refutados / a corrigir na própria proposta
1. «centro +0,0738/+0,0668 ± 0,0336 e dominância 32,7 %» mistura conjuntos e convenções:
   - +0,0668 ± 0,0336 = GWTC5_31, centro MEDIANO (std_ddof1); média-controle do 31 = +0,0787; dominância do 31 = 33,7 % (0,3375).
   - +0,0738 = GWTC5_33, MÉDIA-controle (E0) = E7 descriptive_uncorrected_dtau_weighted_mean; mediana do 33 = +0,0614 ± 0,0331; dominância 32,7 % (0,3272) é do 33.
   Errata tem de dizer por conjunto e por estimador; como está, propaga número híbrido.
2. «ledger de informação dos 53 cegos … z ≤ 0,87 R-B … 3,08 R-LIN com TODOS os cegos» — não é número da bancada (não existe em nenhum artefato da 013-bis; é derivação da gerência) e o rótulo é falso:
   - Registro: test_candidates = 44 (14 elegíveis / 8 AWAITING_GR_METADATA / 22 INPUT_NOT_MET). Inventário GWOSC: O4 SNR≥12 fora da calibração = 44 exatamente (0 dos 9 publicados).
   - 53 = 44 + 9 published_exclusions (censo: «EXCLUIR do cego»). Reproduzido: ΣE[I](53)=922,0 (bate com o «I≈922»). Logo os «53 cegos» incluem 9 eventos NÃO cegos e 22 fora do corte de qualidade.
   - Refeito com ajuste GWTC5_31 (μ=1,4166−0,945 ln ρ; s=0,2251; E[I]=e^{−2μ+2s²}); z_teto=|δ|√(ΣI+I31), I31=887,15:
     44 registrados: ΣE[I]=833,6 → R-B 0,82 · R-MOD 1,53 · R-RAIZ-0 1,54 · R-LIN 2,96 (só novos: 0,57/1,06/1,07/2,06)
     14 elegíveis: ΣE[I]=135,0 → 0,63/1,18/1,18/2,29 (só novos: 0,23/0,43/0,43/0,83)
     53 (44+9 publicados): 922,0 → 0,84/1,57/1,58/3,04 (a proposta diz 0,87/1,54/1,60/3,08 — não reproduz exatamente).
   - É teto de planejamento (fórmula offset-zero, PROIBIDA_COMO_TESTE), [DERIVED, planejamento], jamais «medido».
   - A conclusão (PE dos cegos O4 não é rota de 5σ) sobrevive e fica MAIS forte com 44 (R-B ≤ 0,82).
3. «licença v3» (DG-20 «1.002/1.064 null; GWOSC e 17461225 ausentes»): FALSO. Manifesto v2: 1064 entradas, license.id atribuído em 805 (772 cc-by-4.0 + 24 mit + 9 cc-by via URL); 259 NOT_ASSIGNED_BY_THIS_MANIFEST, todos produtos DERIVADOS da bancada (source_tangents 207, source_distributions 18, recolored 12, literature 7, …), não downloads; GWOSC 9/9 cc-by-4.0; 17461225 19/19 cc-by-4.0. Uma v3 só cabe para rotular os 259 derivados como «derivado / licença herdada da fonte».
4. Estatuto «[REAL — números já medidos]» da linha C-01: só vale para F0, 1.ª linha, quadro, ledger, 19/13/1; para o item 2 é [DERIVED pela gerência, não reproduzido pela bancada]; para o 3 é falso.
5. Custo «≤ 2 h de bancada; 0 h de máquina»: subestimado porque E0.6 e o ledger dos cegos exigem REFAZER (minutos de CPU, ~1 h de bancada a mais); segue barato.
