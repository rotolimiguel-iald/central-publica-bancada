# -*- coding: utf-8 -*-
"""CANDIDATO F5.2 R2 -- cópia do canal N_eff para auditoria; NÃO instalado.

A lei veste o fluido TOTAL (identidade ρ+p, pedra 105 `RhoPlusPClosure`; derivação do operador de 08/08):
    ρ_TGL = β(ρ+p) = β[(4/3)ρ_r + ρ_m]  ⟹  H² = (1 + 4β/3)ρ_r + (1 + β)ρ_m + ρ_Λ
Na era da radiação isso é um deslocamento EXATO de N_eff, sem parâmetro livre:
    ΔN_eff = (4/3)(1 + F·N)/F · β,   F = (7/8)(4/11)^(4/3).

O que este módulo faz (e só isto):
  * lê a fonte congelada por AST e recusa sua linha CMB-SPA mal atribuída;
  * mostra CMB-SPA v2 com Y_P pela BBN e Y_P livre, fonte custodiada por SHA-256;
  * deixa a escolha da hipótese [OPEN] e não emite um centro decisório;
  * β = ALPHA_FINE_CODATA_2018 (lido do um.py por regex) × √e, em runtime — nunca literal;
  * devolve as DUAS convenções de citação lado a lado (D9): separação TGL–SM em σ e tensão de cada modelo contra o centro medido;
  * o controle anti-dupla-contagem (D3): o H(z) da era da radiação pelo motor V3 (Φ_total, N_eff fixo) = o do ΛCDM com
    nnu = N_base + ΔN_eff, a < 1e-4 — uma entrada de β por instrumento, nunca as duas somadas.
Não emite veredito de natureza: as medidas seguem [DECLARADO] até as fontes primárias por sha256 (D8, ato do operador).
NOT_FALSIFIED nunca é CONFIRMED; a RG/ΛCDM é o limite clássico.
"""
import ast
import hashlib
import math
import re

FROZEN = r"C:\IALD\Artigo\teste_acustico_beta_tgl_v1\10_frozen_neff_v1.py"
UM = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
SPT_V2 = r"C:\IALD\PROGRAMA_IALD\auditorias\F4.3_F5.2\web\2506.20707v2.html"
FROZEN_SHA256 = "9d3bceac4f6f54985a0c89ac465bc0a2783ee843da9c51181e0c747b7cda44e7"
SPT_V2_SHA256 = "be14d2e40592e55b0becd6cb332709e708dc094d8d46cc3c1cf8963b897d93d9"
F_NU = (7.0 / 8.0) * (4.0 / 11.0) ** (4.0 / 3.0)


def _sha(p):
    with open(p, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def _require_pin(path, expected):
    actual = _sha(path)
    if actual != expected:
        raise ValueError("SHA-256 divergente: %s (esperado %s; obtido %s)" % (path, expected, actual))
    return actual


def opcoes_yp(source=SPT_V2):
    """Tabela 5 de arXiv:2506.20707v2; condicionamentos explícitos, escolha [OPEN]."""
    pin = _require_pin(source, SPT_V2_SHA256)
    comum = {"conjunto": "CMB-SPA (SPT-3G D1 + Planck + ACT)",
             "fonte": "arXiv:2506.20707v2, Tabela 5", "source_sha256": pin,
             "source_path": source,
             "estatuto": "[DECLARADO — fonte primária custodiada pela auditoria c1; admissão D8/X16 ainda [OPEN]]"}
    return [
        {**comum, "yp": "BBN_CONSISTENCY", "N_eff_obs": 2.82,
         "sigma": 0.12, "sigma_plus": 0.12, "sigma_minus": 0.12},
        {**comum, "yp": "FREE", "N_eff_obs": 2.96,
         "sigma": None, "sigma_plus": 0.21, "sigma_minus": 0.24,
         "nota": "intervalo assimétrico preservado; nenhuma compressão gaussiana decisória"},
    ]


def beta_runtime(um=UM):
    with open(um, "rb") as handle:
        src = handle.read()
    match = re.search(rb"^ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)", src, re.M)
    if match is None:
        raise ValueError("ALPHA_FINE_CODATA_2018 ausente no um.py")
    alpha = float(match.group(1))
    return alpha * math.sqrt(math.e), alpha, hashlib.sha256(src).hexdigest()


def ler_fonte(p=FROZEN):
    """As atribuições MEDIDAS, PROJECOES e NEFF_SM da fonte congelada, por AST (literal_eval), sem executar o arquivo."""
    with open(p, "rb") as handle:
        arv = ast.parse(handle.read().decode("utf-8"))
    alvo = {"MEDIDAS": None, "PROJECOES": None, "NEFF_SM": None}
    for no in arv.body:
        if isinstance(no, ast.Assign) and len(no.targets) == 1 and isinstance(no.targets[0], ast.Name) and no.targets[0].id in alvo:
            alvo[no.targets[0].id] = ast.literal_eval(no.value)
    if any(v is None for v in alvo.values()):
        raise ValueError("fonte congelada sem MEDIDAS/PROJECOES/NEFF_SM: falha visível (fail-closed)")
    return alvo, _sha(p)


def dN_dbeta(N):
    return (4.0 / 3.0) * (1.0 + F_NU * N) / F_NU


def canal(N_base=None, sigmas_extra=(), frozen=FROZEN, um=UM, source=SPT_V2):
    """As duas convenções (D9) por medida e o poder por σ futura. N_base = N_SM da fonte (3,044) se None."""
    beta, alpha, um_sha = beta_runtime(um)
    fonte_sha = _require_pin(frozen, FROZEN_SHA256)
    fonte, _ = ler_fonte(frozen)
    linhas_yp = opcoes_yp(source)
    N_sm = fonte["NEFF_SM"] if N_base is None else float(N_base)
    dNdb = dN_dbeta(N_sm)
    dN = dNdb * beta
    N_tgl = N_sm + dN
    medidas = []
    linha_errada = 0
    for (v, s, rot, arx, indep) in fonte["MEDIDAS"]:
        if "CMB-SPA" in rot:
            if (v, s, arx) != (2.97, 0.12, "arXiv:2506.20707"):
                raise ValueError("linha CMB-SPA congelada mudou: requer nova auditoria")
            linha_errada += 1
            continue
        medidas.append({"rotulo": rot, "fonte": arx, "independente": indep, "N_eff_obs": v, "sigma": s,
                        "separacao_TGL_SM_sigma": dN / s,
                        "tensao_TGL_contra_centro_sigma": abs(N_tgl - v) / s,
                        "tensao_SM_contra_centro_sigma": abs(N_sm - v) / s,
                        "centro_abaixo_do_SM": v < N_sm,
                        "estatuto": "[DECLARADO — transcrito na fonte congelada de 08/08 com arXiv; PDF por sha256 = D8, ato do operador]"})
    if linha_errada != 1:
        raise ValueError("CMB-SPA deve aparecer uma vez na fonte congelada")
    proj = [{"rotulo": rot, "fonte": arx, "sigma_N_eff": s, "separacao_TGL_SM_sigma": dN / s,
             "estatuto": "[DECLARADO — projeção histórica; sem calendário operacional]"} for (s, rot, arx, q) in fonte["PROJECOES"]]
    proj += [{"rotulo": "sigma informada", "sigma_N_eff": float(s), "separacao_TGL_SM_sigma": dN / float(s)} for s in sigmas_extra]
    return {"beta_runtime": beta, "alpha_lido_do_um_py": alpha, "um_py_sha256": um_sha, "fonte_congelada": frozen, "fonte_sha256": fonte_sha,
            "N_base": N_sm, "dN_eff_dbeta": dNdb, "delta_N_eff": dN, "N_eff_TGL": N_tgl, "sinal_fixado_pela_lei": "ΔN_eff > 0 (D7)",
            "sigma_para_5sigma_de_separacao": dN / 5.0, "medidas": medidas, "projecoes": proj,
            "opcoes_CMB_SPA_Yp": linhas_yp, "escolha_Yp": "[OPEN — operador X16; nenhuma linha decisória selecionada]",
            "errata_frozen_CMB_SPA": "2.97 ± 0.12 não é linha CMB-SPA na Tabela 5 v1/v2; excluída da lista medidas",
            "cronologia": "SO 0.045: levantamento completo 2025–2034; CMB-S4 0.030: cenário histórico, projeto encerrado após decisão DOE/NSF de 09/07/2025",
            "convencao_D9": "citar SEMPRE as duas: a separação TGL–SM em σ (poder) e a tensão de cada modelo contra o centro medido",
            "veredito": "NENHUM — o canal mede e cita; a cobrança de natureza é do pré-registro (Fase 8) com fontes por hash"}


def controle_anti_dupla_contagem(z=(1.0e6, 1.0e7), H0=67.36, ombh2=0.02237, omch2=0.1200, dispositivo="cpu", n_grade=20001, tol=1.0e-4):
    """D3: E_TGL(z) [motor V3: Φ_total, N_eff da Bancada fixo] / E_ΛCDM(z) [nnu = N_bancada + ΔN_eff(N_bancada)] − 1, na era da radiação."""
    import torch
    from bancada.fundo_gpu import FundoV3Lote
    beta, _, _ = beta_runtime()
    base = FundoV3Lote(dispositivo=dispositivo, n_grade=n_grade)
    N_b = base.Neff
    N_desl = N_b + dN_dbeta(N_b) * beta
    desl = FundoV3Lote(dispositivo=dispositivo, n_grade=n_grade, Neff=N_desl)
    t = lambda x: torch.tensor([x], dtype=torch.float64, device=base.dev)
    fd_tgl = base.fundo(t(H0), t(ombh2), t(omch2), t(beta), t(0.0))
    fd_neff = desl.fundo(t(H0), t(ombh2), t(omch2), t(0.0), t(0.0))
    zz = torch.tensor([list(z)], dtype=torch.float64, device=base.dev)
    r = (base.Ez(fd_tgl, zz) / desl.Ez(fd_neff, zz))[0].tolist()
    dif = [x - 1.0 for x in r]
    return {"z": list(z), "N_eff_bancada": N_b, "N_eff_deslocado": N_desl, "razao_E_menos_1": dif, "tolerancia": tol,
            "passou": all(abs(d) < tol for d in dif),
            "leitura": "na era da radiação J → (4/3)ρ_r, logo E² → (1+4β/3)ρ_r = o ΛCDM com nnu deslocado; o resíduo é o βρ_m (∝ 1/(1+z))",
            "nota_N_base": "a Bancada usa N_eff = %.3f (fundo_gpu.py); a fonte congelada usa N_SM = 3,044: o controle usa o da Bancada, a citação o da fonte (diferença em ΔN_eff ~ 3e-5, dita)" % N_b}
