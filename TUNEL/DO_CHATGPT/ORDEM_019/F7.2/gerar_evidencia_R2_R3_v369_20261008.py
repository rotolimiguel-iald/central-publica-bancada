# -*- coding: utf-8 -*-
"""Produce new, non-overwriting R2/R3 evidence from the sealed v369 records."""

import hashlib
import json
import math
import os
from pathlib import Path


HERE = Path(__file__).resolve().parent
CORE = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json")
COPY369 = Path(r"C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\project_fisica\v369_um_absoluto.json")
AUDIT = Path(r"C:\IALD\PROGRAMA_IALD\auditorias\F7.2\AUDITORIA_F7_2_C1_RELATORIO_aed6e453.md")
ARITH = Path(r"C:\IALD\PROGRAMA_IALD\auditorias\F7.2\aritmetica_f72.json")
OUT_JSON = HERE / "EVIDENCIA_R2_R3_V369_ORDENS_20261008.json"
OUT_MD = HERE / "EVIDENCIA_R2_R3_V369_ORDENS_20261008.md"


def load_json(path):
    blob = path.read_bytes()
    return json.loads(blob.decode("utf-8")), hashlib.sha256(blob).hexdigest(), len(blob)


def hash_file(path):
    blob = path.read_bytes()
    return {"path": str(path), "sha256": hashlib.sha256(blob).hexdigest(), "bytes": len(blob)}


def write_new(path, blob):
    if path.exists():
        raise FileExistsError(f"Evidence file exists; refusing overwrite: {path}")
    temporary = path.with_name(f".{path.name}.tmp_{os.getpid()}")
    fd = os.open(temporary, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(blob)
            stream.flush()
            os.fsync(stream.fileno())
        if temporary.stat().st_size != len(blob) or not blob:
            raise OSError("Temporary evidence failed size check")
        os.rename(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def approx_equal(x, y):
    return math.isclose(x, y, rel_tol=2e-12, abs_tol=0)


core_doc, core_sha, core_bytes = load_json(CORE)
copy_doc, copy_sha, copy_bytes = load_json(COPY369)
arith, arith_sha, arith_bytes = load_json(ARITH)
current = core_doc["core"]["clock_test_result_v369"]
earlier = copy_doc["core"]["clock_test_result_v369"]

alpha_fine_codata_2018 = 7.2973525693e-3
beta = alpha_fine_codata_2018 * math.sqrt(math.e)
hbar_eV_s = 6.582119569e-16
tau_star = earlier["tau_star_s"]
assert approx_equal(beta, earlier["beta_runtime"])
assert approx_equal(beta, current["beta_runtime"])
assert tau_star == current["tau_star_s"]

fields = [
    ("P1", "best_matter"),
    ("P1", "best_matter_bound_orders"),
    ("P1", "best_matter_bound_kind"),
    ("P1", "tau_star_bound_best_s"),
    ("P1", "clock_5sigma_deficit_orders"),
    ("P3", "verdict"),
    ("root_law", "kbar_rest_mass_excluded"),
]
for group, key in fields:
    assert earlier[group][key] == current[group][key], (group, key)
assert earlier["partition_tag"] == current["partition_tag"]
assert earlier["five_sigma_requirement"] == current["five_sigma_requirement"]

p1 = earlier["P1"]
sr = next(p for p in p1["platforms"] if p["id"] == "sr87_kim2025")
zn = next(p for p in p1["platforms"] if p["id"] == "zn67_potzel1976")
req = earlier["five_sigma_requirement"]

sr_sigma_needed = sr["Gamma_pred_per_s"] / 5
sr_orders = math.log10(sr["sigma_excess_per_s"] / sr_sigma_needed)
matter_bound_orders = math.log10(zn["Gamma_ub_per_s"] / zn["Gamma_pred_per_s"])
matter_sigma_needed_proxy = zn["Gamma_pred_per_s"] / 5
matter_sigma_orders_proxy = math.log10(zn["sigma_per_s"] / matter_sigma_needed_proxy)
matter_omega_needed_proxy = zn["omega_rad_s"] * math.sqrt(
    5 * zn["sigma_per_s"] / zn["Gamma_pred_per_s"]
)
matter_hbar_omega_needed_proxy = hbar_eV_s * matter_omega_needed_proxy
assert approx_equal(sr_orders, p1["clock_5sigma_deficit_orders"])
assert approx_equal(sr_sigma_needed, req["sigma_excess_needed_per_s"])
assert approx_equal(matter_bound_orders, p1["best_matter_bound_orders"])
assert zn["sigma_excess_per_s"] is None
assert zn["Z_expected"] is None
assert zn["bound_kind"] == "NOMINAL"
assert zn["falsifiable"] is False

dm2_21_eV2 = 7.50e-5
dm2_31_eV2 = 2.5e-3
pivot_eV = 1e9
neutrino_rows = []
for row in arith["linhas"]:
    dm2 = dm2_31_eV2 if row["canal"].startswith("ORCA6 G31") else dm2_21_eV2
    delta_E_eV = dm2 / (2 * pivot_eV)
    gamma_pred_eV = (beta / 2) * (tau_star / hbar_eV_s) * delta_E_eV**2
    limit_eV = row["limite_GeV"] * 1e9
    orders = math.log10(limit_eV / gamma_pred_eV)
    assert approx_equal(orders, row["deficit_ordens"])
    neutrino_rows.append({
        "canal": row["canal"],
        "limite_publicado_GeV": row["limite_GeV"],
        "delta_m2_eV2_assumido": dm2,
        "Gamma_TGL_condicional_eV": gamma_pred_eV,
        "distancia_ordens_condicional": orders,
        "estatuto": "DERIVED; vacuum, Kfac=1, tau*=t_P; no TGL operator-to-experiment map",
    })

juno = next(r for r in neutrino_rows if r["canal"].startswith("JUNO"))
result = {
    "title": "F7.2 R2/R3: v369, matéria e ordens condicionais",
    "status": "NEW_EVIDENCE; GATE_UNTOUCHED",
    "sources": [
        {"path": str(CORE), "sha256": core_sha, "bytes": core_bytes},
        {"path": str(COPY369), "sha256": copy_sha, "bytes": copy_bytes},
        hash_file(AUDIT),
        {"path": str(ARITH), "sha256": arith_sha, "bytes": arith_bytes},
    ],
    "core_paths_checked_identical": [f"core.clock_test_result_v369.{g}.{k}" for g, k in fields]
    + ["core.clock_test_result_v369.partition_tag", "core.clock_test_result_v369.five_sigma_requirement"],
    "constants": {
        "alpha_fine_codata_2018": alpha_fine_codata_2018,
        "beta_runtime": beta,
        "hbar_eV_s": hbar_eV_s,
        "tau_star_s_from_v369": tau_star,
    },
    "core_r2": {
        "best_matter": p1["best_matter"],
        "best_matter_bound_kind": p1["best_matter_bound_kind"],
        "best_matter_bound_orders": p1["best_matter_bound_orders"],
        "best_matter_tau_star_bound_s": p1["tau_star_bound_best_s"],
        "best_matter_full_text_verified": False,
        "P3_verdict": earlier["P3"]["verdict"],
        "P3_reason": earlier["P3"]["reason"],
        "root_law_kbar_rest_mass_excluded": earlier["root_law"]["kbar_rest_mass_excluded"],
        "partition_tag": earlier["partition_tag"],
    },
    "sr87_requirement": {
        "platform": req["platform"],
        "Gamma_pred_per_s": sr["Gamma_pred_per_s"],
        "sigma_excess_today_per_s": sr["sigma_excess_per_s"],
        "sigma_excess_5sigma_needed_per_s": sr_sigma_needed,
        "deficit_5sigma_orders": sr_orders,
        "hbar_omega_needed_eV_at_todays_sigma": req["hbar_omega_needed_eV_at_todays_sigma"],
        "ghz_N_needed": req["ghz_N_needed"],
        "estatuto": "DERIVED in v369 under P1; current Sr resolution; lower requirements",
    },
    "zn67_matter": {
        "platform": zn["id"],
        "species": zn["species"],
        "omega_rad_s": zn["omega_rad_s"],
        "Gamma_pred_per_s": zn["Gamma_pred_per_s"],
        "Gamma_ub_nominal_per_s": zn["Gamma_ub_per_s"],
        "sigma_raw_per_s": zn["sigma_per_s"],
        "sigma_excess_per_s": zn["sigma_excess_per_s"],
        "Z_expected": zn["Z_expected"],
        "falsifiable_in_v369": zn["falsifiable"],
        "nominal_bound_deficit_orders": matter_bound_orders,
        "sigma_needed_5sigma_raw_proxy_per_s": matter_sigma_needed_proxy,
        "sigma_reduction_raw_proxy_orders": matter_sigma_orders_proxy,
        "hbar_omega_needed_raw_proxy_eV": matter_hbar_omega_needed_proxy,
        "less_than_sr_5sigma_orders_by": sr_orders - matter_bound_orders,
        "estatuto": "DERIVED proxy; raw sigma is not sigma_excess and this is not registered power",
    },
    "neutrino_comparisons": neutrino_rows,
    "neutrino_range_orders": [min(r["distancia_ordens_condicional"] for r in neutrino_rows), max(r["distancia_ordens_condicional"] for r in neutrino_rows)],
    "juno_G21_component_orders": juno["distancia_ordens_condicional"],
    "wall": "No effective omega per atom/molecule/nanoparticle path, no TGL operator -> visibility and nuisance map, and no verified sigma_excess; partition MODULAR_LAB_BRIDGE_OPEN. Published contrasts cannot yield power in orders or tau* limits.",
    "gate_effect": "NONE",
}

rows_md = "\n".join(
    f"| {r['canal']} | {r['limite_publicado_GeV']:.2e} | {r['Gamma_TGL_condicional_eV']:.3e} | {r['distancia_ordens_condicional']:.2f} |"
    for r in neutrino_rows
)

report = f"""# F7.2 — evidência nova R2/R3: leitura da v369 e ordens

**Estatuto:** [REAL] leitura e comparação das chaves de dois arquivos; [DERIVED] apenas as contas explicitamente condicionais. Esta evidência não altera os originais, o canal, o MCP ou o gate. `NOT_FALSIFIED` não é creditação.

## Custódia e escopo da leitura

- Core atual `um_absoluto.json`: SHA-256 `{core_sha}` ({core_bytes} bytes).
- Cópia v369 `v369_um_absoluto.json`: SHA-256 `{copy_sha}` ({copy_bytes} bytes).
- Parecer cético c1 `AUDITORIA_F7_2_C1_RELATORIO_aed6e453.md`: SHA-256 `{result['sources'][2]['sha256']}`.
- Aritmética do auditor `aritmetica_f72.json`: SHA-256 `{arith_sha}`.
- As chaves de v369 citadas abaixo foram lidas da cópia e confrontadas com `core.clock_test_result_v369` no core atual. β foi reconstruído em runtime como `ALPHA_FINE_CODATA_2018 × √e = {beta:.17g}`; `τ★ = t_P = {tau_star:.15e} s` é a hipótese da v369, não uma medida de τ★.

## R2 — o que o core já havia decidido

1. `core.clock_test_result_v369.P1.best_matter = zn67_potzel1976`: Mössbauer de ⁶⁷Zn, 93 keV. O core dá `best_matter_bound_kind = NOMINAL`, `best_matter_bound_orders = {matter_bound_orders:.9f}` e `tau_star_bound_best_s = {p1['tau_star_bound_best_s']:.9e} s` **dentro da leitura P1**. A ficha da plataforma (`P1.platforms[id=zn67_potzel1976]`) registra que só o resumo de Potzel 1976 foi aberto, mais E e T½ do ENSDF; o texto integral não foi verificado. Logo essa cota não deve ser apresentada como limite experimental direto da TGL.
2. `P3.verdict = {earlier['P3']['verdict']}`. Na leitura de tempo estocástico universal, o Hamiltoniano total reparametriza o tempo comum; o core diz que razão de frequências, largura e franja locais não veem o efeito.
3. `root_law.kbar_rest_mass_excluded = true`: a leitura da lei-raiz por massa de repouso foi excluída **na leitura do core**, não como exclusão universal da teoria.
4. `partition_tag = {earlier['partition_tag']}`. A escolha física entre P1/P2/P3 ainda depende dessa ponte. O próprio protocolo marca as leituras condicionais.

## R3 — grandezas comparáveis e parede de interpretação

**Sr da v369, [DERIVED sob P1].** Em `sr87_kim2025`, `Γ_pred = {sr['Gamma_pred_per_s']:.9e} s⁻¹`. Para 5σ, `σ_excesso necessário = Γ_pred/5 = {sr_sigma_needed:.9e} s⁻¹`; o `σ_excesso` publicado usado pela v369 é `{sr['sigma_excess_per_s']:.9e} s⁻¹`. A razão tem `log10(σ_hoje/σ_necessário) = {sr_orders:.9f}` ordens, reproduzindo `P1.clock_5sigma_deficit_orders`. O requisito `five_sigma_requirement` é **para essa plataforma com o σ de hoje**: `ℏω ≥ {req['hbar_omega_needed_eV_at_todays_sigma']:.6f} eV` ou GHZ `N ≥ {req['ghz_N_needed']:.6f}` no cenário projetado. O core os chama de limites inferiores.

**Melhor matéria no core, [DERIVED sob P1; NOMINAL].** Para `zn67_potzel1976`, `ω = {zn['omega_rad_s']:.9e} rad/s`, `Γ_pred = {zn['Gamma_pred_per_s']:.9e} s⁻¹`, e a cota nominal é `{zn['Gamma_ub_per_s']:.9e} s⁻¹`. A separação é `log10(Γ_ub/Γ_pred) = {matter_bound_orders:.9f}` ordens. É numericamente {sr_orders-matter_bound_orders:.2f} ordens menor que a distância de 5σ do Sr, mas os estimadores e estatutos são diferentes: esta subtração **não é um teste entre plataformas**.

O `σ_per_s = {zn['sigma_per_s']:.9e} s⁻¹` da ficha Mössbauer daria, como **proxy cru e condicional [DERIVED]**, `Γ_pred/5 = {matter_sigma_needed_proxy:.9e} s⁻¹` e uma redução de `log10(5σ/Γ_pred) = {matter_sigma_orders_proxy:.9f}` ordens, equivalente por `Γ ∝ ω²` a `ℏω ≈ {matter_hbar_omega_needed_proxy:.6e} eV` se todo o resto ficasse fixo. O próprio core põe `sigma_excess_per_s = null`, `Z_expected = null` e `falsifiable = false` nessa plataforma. Portanto o proxy **não é requisito de poder registrado**, nem projeto experimental fisicamente validado.

**Neutrinos, [DERIVED condicional; comparação dimensional, não likelihood TGL].** Com `E₀ = 1 GeV`, `τ★ = t_P`, vácuo, `Kfac = 1`, `Δm²₂₁ = 7,50×10⁻⁵ eV²` ou `Δm²₃₁ = 2,5×10⁻³ eV²` aproximados, usei `Γ_ν = (β/2)(τ★/ℏ)(Δm²/2E₀)²` em eV. Os limites publicados (GeV) e o confronto condicional são:

| Canal | Cota GeV | Γ TGL hipotética eV | log₁₀(cota/Γ) |
|---|---:|---:|---:|
{rows_md}

A faixa é {min(r['distancia_ordens_condicional'] for r in neutrino_rows):.2f}–{max(r['distancia_ordens_condicional'] for r in neutrino_rows):.2f} ordens; a componente Γ₂₁ do cenário JUNO de taxas iguais fica a {juno['distancia_ordens_condicional']:.2f}. **A hipótese `Γ₂₁ = Γ₃₁` do artigo JUNO não é produzida por esta substituição de Δm² na lei TGL;** sem operador TGL em matéria, evolução, ordenamento, `Kfac` e likelihood do mesmo cenário, a razão não é uma cota sobre τ★. Fogli também usa dissipador solar distinto do dephasing puro.

**Parede para interferometria de matéria [OPEN].** Para átomos, C₇₀ e nanopartículas, a tabela custodiada traz contraste e visibilidade publicados, mas não define `ω` físico efetivo por estado/caminho, a passagem do operador TGL `Γ→visibilidade`, o fundo instrumental separado nem `σ_excesso` verificado. A partição `MODULAR_LAB_BRIDGE_OPEN` impede selecionar P1/P2/P3 como identidade física já testada. Assim, não existe número honesto de poder em ordens nem `τ★_limite` desses interferômetros hoje. O `ω` de Mössbauer acima pertence a uma transição nuclear, não preenche essa lacuna das franjas.

**Efeito no gate:** nenhum. `SEM_LIMITE_TGL` permanece [OPEN] da ponte operador/canal; `NOT_FALSIFIED` não é creditação.
"""

json_blob = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
md_blob = report.encode("utf-8")
write_new(OUT_JSON, json_blob)
write_new(OUT_MD, md_blob)
print(json.dumps({"json": hash_file(OUT_JSON), "md": hash_file(OUT_MD)}, ensure_ascii=False, indent=2))
