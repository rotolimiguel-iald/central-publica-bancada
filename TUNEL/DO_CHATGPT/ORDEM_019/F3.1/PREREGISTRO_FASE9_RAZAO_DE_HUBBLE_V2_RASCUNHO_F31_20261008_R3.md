# Fase 9 V2 R3 autossuficiente — rascunho não congelado

Spec sha256: 21a624f5c6e716b3b9a1b9301747b94ae74b82bed2502654885a0709ec9d0dcb. V1 1893261e730994b3508d14dd2105f8aae3a764d3d217e28bd5939cb58f865273; R2 4a6a927fb13ad2e3efbaeea92dd67f1953ff33675a73fd865993203c8b8c15b9; vínculo 885efb944728efb41b62b47fa653c6d3a3956bd1cb086cb8595b958b6a410c52.

[REAL documental] Quinze seções V1 recompostas com texto V2. Nenhum alvo, composto real, congelamento ou gate tocado.

## Correções quantitativas

- [DERIVED inferência] Nota a CCHP Table 6 marca TRGB (JWST) 1,9%, não HST+JWST; N/T do 1,33 é teto inferido.
- [INPUT DECLARADO] SBF 0,031 é fator operacional 3,1%, H0 implícito 74,19; não verificado como constante publicada.
- [DERIVED] L1N/L1bN/L4N usam BG1 nu 68.531, não K*BG1; L1bN=0.930000, cap 0,93.
- [DERIVED c1 R2] λ_N comum deu sigma máximo 0,94929; quatro termos independentes 0,94946. R3 recompõe pontas.
- [DERIVED c1] TDCOSMO sigma 3,9: cinco 5,695, seis 5,439 (R2); cinco R3 5.694998.
- [REAL documental] Seis leitores pinados; L1b/L6 declarados; D-H pendente para todos.
- [INPUT/DERIVED] n_alvos_declarados inventário inteiro=2, primário INCONCLUSIVE; preflight=staged.
- [DERIVED] R25 L1b sigma 0,93 aciona gatilho e liga L1bN a L2N/L3N; réplica diagnóstica.

## base

{
  "R2_sha256": "4a6a927fb13ad2e3efbaeea92dd67f1953ff33675a73fd865993203c8b8c15b9",
  "V1_sha256": "1893261e730994b3508d14dd2105f8aae3a764d3d217e28bd5939cb58f865273",
  "gate": "UNTOUCHED",
  "state": "RASCUNHO_NAO_CONGELADO"
}

## contaminacao_declarada

{
  "R3": "non-blind; no target opened or real composite run",
  "consequencia": "a novidade e de USO e de RIGOR (fontes por hash, covariancia, cinco hipoteses, funcao fixada antes do composto), nao de cegueira: todo token leva __NOT_BLIND_TO_DATA_STATED",
  "ja_lido_pela_casa": "Fases 3-5 (ensaio nao-cego da Fase 9 e o desenho: TGL -1,4 sigma, LCDM +4,5 sigma com BG1/R22, lido de FASE9_DESENHO_RESULTADO.json)",
  "validacao_F14": "o alvo de validacao 73,6 +- 1,1 (Brout+22) segue [DECLARADO]; estimador de V = LCDM plano, SNe + 77 calibradores Cefeida, M perfilado — fixado aqui"
}

## decisoes_padrao_da_gerencia

{
  "D-A": "fundo primario BG1 = LCDM nu Planck-comp + DESI DR2 SEM escada (68.531 +- 0.301); BG2 Planck 2018 replica; BG3 DESI+BBN replica [DECLARADO]; o 68,4298 da Fase 4 (ajuste COM a escada) NAO e fundo de previsao (F2)",
  "D-B": "leitor primario da escada R22 (73.04 +- 1.04); R25 replica ao lado; nunca somados",
  "D-C": "CCHP TRGB/JAGB (70.39 +- 1.936) e TESTE dentro do composto; gatilho FALSIFIED por leitor unico so com sigma_i <= 1,0 e |z_i| >= 5",
  "D-D": "UMA funcao de veredito (secao funcao_de_veredito), estatisticas do pre-registro + o degrau TENSION do desenho; FALSIFIED/TENSION antes de UNDERPOWERED (a exclusao da previsao nao precisa de poder discriminante; esconde-la atras de UNDERPOWERED seria fail-open) — desvio da ordem do rascunho, dito",
  "D-E": "__USE_NOVEL pelos PARAMETROS (Worrall [KNOWN]); a selecao da FORMA dita ao lado, nao decisoria (lei de 05/10)",
  "D-F": "sirenes = diagnostico fora do composto",
  "D-G": "shift so nos leitores de Cefeidas do SH0ES (s em U[-0,15; 0,15]); fundo-livre = r_d em U[130; 160] Mpc; beta-livre U[-0,05; 0,05]; lnB sempre com a largura ao lado (Occam ~ ln 2 por fator 2)",
  "D-H": "Six sources pinned documentally, L1b/L6 declared; all D-H admissions pending",
  "D-I": "canal do livro de cobrancas: R1 v2 (mesma lei, mesma cobranca, funcao nova); R1b so se o objeto mudar",
  "D-J": "Final token name operator decision, pending",
  "D-K": "registro no mapa de rotas (lentes, critica e este V1) feito pela gerencia no mesmo passo",
  "NAT22_X13": "Observed executor deviations stated, operator decision pending",
  "fonte_da_delegacao": "operador 05/10: «o resto vc consegue responder tudo agroa»; «prossiga» (memorias proximo-passo-06out, handoff-sessao-nova-06out)"
}

## especificacao_do_runner

[
  "R0 pin V2 R3 spec/function/runner before real composite, no freeze now",
  "R1 inventory-wide n_alvos with the same predicate in preflight and staged",
  "R2 recompute BG1 and beta/K at runtime, fail on mismatch",
  "R3 power from sigmas at both covariance endpoints before local centers",
  "R4 real opening only after F3.4, NAT22/X13, D-H, c1 audit and operator act",
  "R5 five hypotheses, GLS/dispersion both endpoints, four lnB incl free background, pinned verdict",
  "R6 R_r25 and S_com_sirenes diagnostics, their own covariance; never sum replacements",
  "R7 subsequent changes new version beside, no overwrite"
]

## estado

"RASCUNHO_NAO_CONGELADO; F3.4/NAT22 before freeze; D-H before opening"

## estatisticas

{
  "background": "marginalized by observed executor; NAT22 pending",
  "dispersao": "chi2/(n-1)>2 OR p<0.01 at EITHER endpoint gives INCONCLUSIVE",
  "lnB": "n>=100 quadrature, check n=100/200; compare LCDM, beta-free, shift, free background",
  "sigma_beta": "mean asymmetric sides, local Gaussian",
  "z_delta": "profile -2lnL including log determinant at minimum-sigma endpoint",
  "z_disc": "quadratic form at maximum-sigma endpoint",
  "z_i": "active family; sigma<=1 and |z_i|>=5; R25 L1b has sigma 0.93"
}

## fontes_lidas_sha256

{
  "CCHP_Table6": "e32d608358cc0f0dcc3def744beef4b9afea24a967c8f730c90027dc589b6dcc",
  "R2": "4a6a927fb13ad2e3efbaeea92dd67f1953ff33675a73fd865993203c8b8c15b9",
  "V1": "1893261e730994b3508d14dd2105f8aae3a764d3d217e28bd5939cb58f865273",
  "V1x_binding": "885efb944728efb41b62b47fa653c6d3a3956bd1cb086cb8595b958b6a410c52",
  "status": "DOCUMENTARY_ONLY_D_H_PENDING_NO_TARGET_OPENED"
}

## funcao_de_veredito

{
  "estatuto": "PROPOSTA_SINTETICA_NAO_CONGELADA",
  "final_token": "D_J_PENDING",
  "fonte": "def veredito_fase9_v2_r3_proposta(r):\n    \"\"\"Draft only. D-J names final token; use minimum and maximum covariance endpoints.\"\"\"\n    import math\n    def f(x): return (\"M\" if x<0 else \"P\")+(\"%.1f\"%abs(x)).replace(\".\",\"P\")\n    base=\"TGL_FASE9_RAZAO_DE_HUBBLE_V2_R3_DRAFT__\"\n    suf=(\"__D1B__FUNDO_%s__NOT_BLIND_TO_DATA_STATED\"\n         \"__NOT_A_CONFIRMATION__GATE_UNTOUCHED\")%r[\"fundo\"]\n    if (r[\"n_alvos_declarados\"]>0 or not r[\"required_sources_admitted\"]\n        or r[\"beta_livre_no_limite\"]\n        or any(e[\"chi2_por_gl\"]>2 or e[\"p\"]<0.01\n               for e in r[\"dispersao_endpoints\"].values())):\n        return base+\"INCONCLUSIVE_SYSTEMATICS\"+suf\n    low,high=r[\"minimum\"],r[\"maximum\"]\n    zd=abs(low[\"z_delta\"])\n    if zd>=5 or any(s<=1 and abs(z)>=5 for s,z in low[\"sigma_z_por_alvo\"]):\n        return base+\"FALSIFIED_AT_5SIGMA\"+suf\n    if zd>=3: return base+\"TENSION_3_TO_5_SIGMA\"+suf\n    if high[\"poder_previo\"]<5:\n        return base+\"NOT_FALSIFIED_UNDERPOWERED__POWER_%s_OF_5_SIGMA\"%f(high[\"poder_previo\"])+suf\n    if high[\"z_disc\"]>=5 and zd<3 and high[\"lnB_lcdm\"]>=5 and high[\"lnB_livre\"]>=-1:\n        t=(base+\"NOT_FALSIFIED_POWERED__DISCRIMINATES_FROM_LCDM_AT_%dSIGMA\"\n           \"__ZERO_FREE_PARAMETERS\"%int(math.floor(high[\"z_disc\"])))\n        t+=\"__USE_NOVEL\" if r[\"use_novel_parametros\"] else \"__USE_NOVELTY_PENDING\"\n        t+=\"__VS_LADDER_SYSTEMATIC_LNB_%s__VS_FREE_BACKGROUND_LNB_%s\"%(f(high[\"lnB_shift\"]),f(high[\"lnB_fundo_livre\"]))\n        if high[\"lnB_shift\"]<0 and high[\"poder_nao_cefeida\"]>=5:\n            t+=\"__NOT_DISCRIMINATED_FROM_LADDER_SYSTEMATIC\"\n        if abs(high[\"lnB_fundo_livre\"])<1:\n            t+=\"__NOT_DISCRIMINATED_FROM_FREE_BACKGROUND\"\n        return t+suf\n    t=base+\"NOT_FALSIFIED_POWERED__\"+(\"DEVIATION_CONSISTENT_WITHIN_1SIGMA\" if zd<1 else \"DEVIATION_1_TO_3_SIGMA\")\n    if high[\"z_disc\"]<5: t+=\"__NOT_DISCRIMINATED_FROM_LCDM_AT_AVAILABLE_SENSITIVITY\"\n    return t+suf\n",
  "n_alvos_declarados_rule": {
    "current_count": 2,
    "current_ids": [
      "L1b_sh0es_r25",
      "L6_sirenes"
    ],
    "predicate": "NOT gate_verified AND NOT operator_admitted_in_pinned_D_H_register",
    "primary_result": "INCONCLUSIVE_SYSTEMATICS until L1b/L6 gate verification/admission; D-H separately blocks opening",
    "same_in": [
      "preflight",
      "staged_runner"
    ],
    "universe": "whole V1.x inventory, not active family"
  },
  "nome": "veredito_fase9_v2_r3_proposta",
  "sha256": "a497c29bc60211080388fedfb2872686e30a0d924799fa53e8896347514384f9",
  "thresholds": {
    "beta_free_prior_edge": "INCONCLUSIVE_SYSTEMATICS",
    "discrimination_z_ge": 5.0,
    "dispersion_chi2_per_dof_gt": 2.0,
    "dispersion_p_lt": 0.01,
    "falsification_abs_z_ge": 5.0,
    "free_background_abs_lnB_lt": 1.0,
    "lnB_beta_free_ge": -1.0,
    "lnB_lcdm_ge": 5.0,
    "power_ge": 5.0,
    "single_reader_sigma_le": 1.0,
    "tension_abs_z_ge": 3.0
  }
}

## hipoteses

{
  "H_LCDM": "todos leem H0_bg (beta = 0)",
  "H_TGL": "bare BG1 plus fixed K=E(z*)^(2beta/3), beta=ALPHA_FINE_CODATA_2018*sqrt(e) at runtime",
  "H_beta_livre": "K(beta), beta em U[-0,05; 0,05]; fitted beta at prior edge => INCONCLUSIVE_SYSTEMATICS",
  "H_fundo_livre": "LCDM + r_d livre U[130; 160] Mpc (proxy de fundo precoce [INPUT da gerencia]); todos leem o mesmo H0",
  "H_shift_cefeidas": "Only L1 or replacement L1b receives shift s~U[-0.15,0.15]; CCHP TRGB-only does not"
}

## nao_decide

[
  "o gate (18 bandeiras, funcao so do formal)",
  "a implicacao da QG e a correspondencia com a RG",
  "beta (a regra matriz)",
  "qual fundo e o da natureza (aqui so o primario do registro)",
  "o mecanismo [CONJECTURE]",
  "a dependencia em z de K (<= 0,9 % em z = 2, abaixo do poder)",
  "D-H admission",
  "F3.4 governing specification",
  "NAT22/X13"
]

## novidade_de_uso

{
  "ao_lado_nao_decisorio": "a FORMA D1a foi escrita «exatamente a relacao observacional» (17/05/2026) e a classe do fluxo retida porque a Friedmann «nao resolve» (05/06/2026): selecao de hipotese, nao ajuste de parametro; pela lei de 05/10 nao e demerito",
  "clausula_D-E": "o teste e use-novel se nenhum PARAMETRO numerico da lei foi ajustado a razao local/fundo: beta (valor 0,012 em 13/11/2025; forma alpha.sqrt(e) publicada 03/03/2026; lei de 17/05/2026), z* [KNOWN Planck], o expoente 2/3 (Raychaudhuri/FRW), o fundo nu do CMB+BAO",
  "cronologia_por_hash": {
    "arquivo": "evidencias/CRONOLOGIA_NOVIDADE_DE_USO.json",
    "sha256": "8c13eb249b104564d8e97134126846cde96a7b35a68276f22b989973316a8023"
  },
  "etiqueta": "retrodição sem ajuste; no theory parameter fit to local H0",
  "literatura": "Worrall, J. (1985/1989/2014) sobre use-novelty; Le Verrier 1859 (excesso do perielio de Mercurio) e Einstein 1915 [KNOWN — nao conferido em disco (F12)]",
  "use_novel_parametros": true
}

## sistematicas

{
  "calibradores": "Cefeidas x TRGB/JAGB entram como estao; a dispersao interna decide INCONCLUSIVE",
  "covariancia": "Cauchy-Schwarz sensitivity box, common lambda_N and lambda_T; SN/Pantheon cross terms OPEN",
  "free_background": "NOT_DISCRIMINATED_FROM_FREE_BACKGROUND if abs(lnB_TGL_vs_free)<1",
  "fundo": "BG1 preselected, BG2/BG3 diagnostic; executor marginalizes background",
  "ladder": "ladder suffix requires lnB_shift<0 AND no-Cepheid power>=5",
  "local": "velocidades peculiares / vazio local nao modelados (declarado)",
  "multiplicidade": "familia entra no livro da Bancada (Sidak); local ao lado da corrigida"
}

## supersede

{
  "R2_sha256": "4a6a927fb13ad2e3efbaeea92dd67f1953ff33675a73fd865993203c8b8c15b9",
  "V1_remains_frozen": true,
  "draft_R2_only": "C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_019\\F3.1\\PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V2_RASCUNHO_F31_20261008_R2.json"
}

## token_base_provisorio

"TGL_FASE9_RAZAO_DE_HUBBLE_V2_R3_DRAFT__LAW_D1B__BG1"

## token_estado

"RASCUNHO_NAO_CONGELADO__F3_4_NAT22_D_J_PENDING__GATE_UNTOUCHED"

## Função completa proposta

def veredito_fase9_v2_r3_proposta(r):
    """Draft only. D-J names final token; use minimum and maximum covariance endpoints."""
    import math
    def f(x): return ("M" if x<0 else "P")+("%.1f"%abs(x)).replace(".","P")
    base="TGL_FASE9_RAZAO_DE_HUBBLE_V2_R3_DRAFT__"
    suf=("__D1B__FUNDO_%s__NOT_BLIND_TO_DATA_STATED"
         "__NOT_A_CONFIRMATION__GATE_UNTOUCHED")%r["fundo"]
    if (r["n_alvos_declarados"]>0 or not r["required_sources_admitted"]
        or r["beta_livre_no_limite"]
        or any(e["chi2_por_gl"]>2 or e["p"]<0.01
               for e in r["dispersao_endpoints"].values())):
        return base+"INCONCLUSIVE_SYSTEMATICS"+suf
    low,high=r["minimum"],r["maximum"]
    zd=abs(low["z_delta"])
    if zd>=5 or any(s<=1 and abs(z)>=5 for s,z in low["sigma_z_por_alvo"]):
        return base+"FALSIFIED_AT_5SIGMA"+suf
    if zd>=3: return base+"TENSION_3_TO_5_SIGMA"+suf
    if high["poder_previo"]<5:
        return base+"NOT_FALSIFIED_UNDERPOWERED__POWER_%s_OF_5_SIGMA"%f(high["poder_previo"])+suf
    if high["z_disc"]>=5 and zd<3 and high["lnB_lcdm"]>=5 and high["lnB_livre"]>=-1:
        t=(base+"NOT_FALSIFIED_POWERED__DISCRIMINATES_FROM_LCDM_AT_%dSIGMA"
           "__ZERO_FREE_PARAMETERS"%int(math.floor(high["z_disc"])))
        t+="__USE_NOVEL" if r["use_novel_parametros"] else "__USE_NOVELTY_PENDING"
        t+="__VS_LADDER_SYSTEMATIC_LNB_%s__VS_FREE_BACKGROUND_LNB_%s"%(f(high["lnB_shift"]),f(high["lnB_fundo_livre"]))
        if high["lnB_shift"]<0 and high["poder_nao_cefeida"]>=5:
            t+="__NOT_DISCRIMINATED_FROM_LADDER_SYSTEMATIC"
        if abs(high["lnB_fundo_livre"])<1:
            t+="__NOT_DISCRIMINATED_FROM_FREE_BACKGROUND"
        return t+suf
    t=base+"NOT_FALSIFIED_POWERED__"+("DEVIATION_CONSISTENT_WITHIN_1SIGMA" if zd<1 else "DEVIATION_1_TO_3_SIGMA")
    if high["z_disc"]<5: t+="__NOT_DISCRIMINATED_FROM_LCDM_AT_AVAILABLE_SENSITIVITY"
    return t+suf

F3.4 e NAT22/X13 antecedem congelamento; D-H antecede abertura; D-J nomeia token. NOT_FALSIFIED não credita.
