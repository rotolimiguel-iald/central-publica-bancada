"""Append the c1 F4.3 correction and create immutable V2 evidence."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime
from pathlib import Path


HERE = Path(__file__).resolve().parent
PLAN = HERE / "PLANO_E_PREREGISTRO.md"
OLD = HERE / "PREREGISTRO_F4_3.json"
V2 = HERE / "PREREGISTRO_F4_3_V2.json"
RESULT = HERE / "RESULTADO_C1_F43_V2_20261008.json"
AUDIT = Path(r"C:\IALD\PROGRAMA_IALD\auditorias\F4.3_F5.2\AUDITORIA_F4_3_F5_2_C1_20261007.md")
CLOCK = AUDIT.parent / "f43_clock_check.out.json"
RAMO_V1 = Path(r"C:\IALD\Bancada_Um\investigacao\preregistro_ramo_b_05out\PREREGISTRO_RAMO_B_RINGDOWN_V1.json")
QNM = Path(r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\QNM_GRID.json")
MARKER = "F43_C1_R1_R2_R3_V2_20261008"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pin(path: Path) -> dict:
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": sha(path)}


def atomic_new(path: Path, data: bytes) -> None:
    if path.exists():
        raise FileExistsError(path)
    temp = path.with_name(path.name + ".tmp")
    with temp.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    if temp.stat().st_size != len(data):
        raise IOError(f"short write: {temp}")
    os.replace(temp, path)


def json_bytes(obj: dict) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def main() -> None:
    original = PLAN.read_bytes()
    if MARKER.encode() in original:
        raise RuntimeError("plan correction is already present")
    old_sha = sha(PLAN)
    if old_sha != "10c80b981c22df24a826cc454f746df2f0cb493acacd2358e2ca6b21182dbf46":
        raise RuntimeError(f"unexpected plan prefix: {old_sha}")
    if sha(OLD) != "4f60c14d3bffe5faeae67578900c4e605341fbc6a0e1481c4ca23fb98cf0c437":
        raise RuntimeError("old preregistration changed")
    if sha(RAMO_V1) != "86f98fcc124dd9cae04fdb06bd10c14175893253d5b139496bd4c05f109feee0":
        raise RuntimeError("Ramo B V1 changed")
    if sha(QNM) != "4f34367a0906023836fcf8013ada3ccef48877a17f59f697b9dabc25a2494b24":
        raise RuntimeError("QNM grid changed")
    for candidate in (V2, RESULT):
        if candidate.exists():
            raise FileExistsError(candidate)

    old = json.loads(OLD.read_text(encoding="utf-8"))
    ramo = json.loads(RAMO_V1.read_text(encoding="utf-8"))
    clock = json.loads(CLOCK.read_text(encoding="utf-8"))
    audit_pin = pin(AUDIT)
    clock_pin = pin(CLOCK)
    now = datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")
    backup = PLAN.with_name(PLAN.name + f".bak_{now}")
    atomic_new(backup, original)
    if backup.read_bytes() != original:
        raise RuntimeError("backup differs from original")

    correction = f"""

---

## ADENDO AO LADO — c1, 08/10/2026 ({MARKER})

**Alcance.** Corrige as leituras dos §§1, 4, 5 e 6; o texto acima permanece como linhagem. Fonte: auditoria c1 `{audit_pin['sha256']}` e conta do relógio `{clock_pin['sha256']}`. [REAL: hashes e números da sonda lidos; DECLARADO: família contra-rotante aferida pela gerência/cético.] O pedido de autorização ao operador está **SUSPENSO** até a auditoria desta camada; conjunto D, strain e PE não foram abertos.

**R1 — relógio e ramo.** As seq 58/87/91, o `lnB≈−0,0026` do C6, o Fisher B2 e o proxy `0,06σ` de GW250114 pertencem a `k=1`; não medem o poder do relógio V1. O único relógio decisório desta F4.3 é `k(χ_f)=2π/κ̂(χ_f)`, por evento, `τ★=k GM_f/c³`, com a mesma massa e o mesmo k para 220 e 440 (C8). A sonda c1 lê `k=28,495…30,163` para `χ_f=0,6145…0,70`, `δτ̂_220=−0,338…−0,389`, e `δτ̂_440=−0,694…−0,738` com fonte fixa [DERIVED, sem dado novo]. O `Q_220` exigido à RG é `1,979…2,013`, abaixo do mínimo `2,100` da **grade prógrada** pinada; nessa grade nenhum `(M,χ)` absorve o 220 no relógio V1. Segundo a correção da gerência e do cético do ramo B [DECLARADO nesta entrega], a família **contra-rotante** pode absorvê-lo num ajuste só-220 (`χ≈0,10…0,22`, `M/M_f≈0,58…0,72`). Só a espiral completa IMR (controle C3) fecha essa porta. Assim, a frase acima «220 isolado é absorvível por massa/spin GR» vale apenas para a antiga medição `k=1`; o diagnóstico V1 depende do ramo e do IMR. O proxy `0,06σ` do 440 e o `N90=235,554` do B2 não são poder V1.

**R2 — precedência e FWER no mesmo D.** O V1 do ramo B (pin `{sha(RAMO_V1)}`) é o **teste primário por IMR completo**. A F4.3 ringdown-only é **diagnóstico subordinado**, não uma segunda reivindicação independente. O 221 não entra; nem k nem M são escolhidos após ver o dado. Primeiro sai o veredito V1. Uma leitura F4.3 no mesmo sentido só pode **corroborá-lo** se V1 e F4.3 passarem, cada qual, sua cauda unilateral calibrada no limiar `p≤2,8665×10⁻⁷`. A regra de interseção não gasta outra hipótese primária: sob a nula verdadeira, a probabilidade de reivindicação conjunta falsa é no máximo a da rejeição V1 (`≤α`), sem supor independência. Um sinal isolado da F4.3 permanece diagnóstico. O veredito de tensão com RG usa a palavra V1 `NOT_FALSIFIED_POWERED__GR_TENSION_REPORTED`; `FAVORS_PAIR_B_220_440_AT_5SIGMA` é retirado do vocabulário vigente. Se as duas nulidades (RG e par B) forem rejeitadas pela própria calibração, prevalece `INCONCLUSIVE_SYSTEMATICS__BOTH_MODELS_REJECTED`.

**R3 — função e manifesto.** A triagem SVD sintética usa `rcond=10⁻¹⁰` relativo ao maior valor singular de `WJ`, `η_joint≥25` e `η_increment_440=max(0,η_joint−η_220)≥1` [INPUT: tolerâncias de desenho]. Esses limiares **não equivalem a 5σ**, não estimam poder do conjunto D e não autorizam abertura. Na região `x≈0,6` a linearização é insuficiente: o portão exige injeções da forma **exata** `δτ̂=−x/(1+x)`, calibração de ambas as caudas, cobertura, controles e poder de recuperação `≥90%` a 5σ. Faltas no manifesto de eventos/holds, PSD, janelas, priors, início, família de waveform ou hashes fazem `AWAITING_POWER` (fail-closed). O `PREREGISTRO_F4_3_V2.json` fixa esses campos obrigatórios e a ordem dos vereditos; sem manifesto completo e revisão cética, nenhum pedido de abertura do D segue.

**§6 corrigido — ordem da próxima peça.** Em cópia, reproduzir `k=1` das seq 58/87/91 apenas como controle histórico; mudar então para `k=2π/κ̂` e medir separadamente a grade prógrada e a família contra-rotante. A falha em reproduzir o controle `k=1`, o relógio V1 ou a distinção dos ramos interrompe a análise e produz diagnóstico tipado, sem inferir poder. Sob o V1, o teste primário é IMR completo; a SVD 220/440 é triagem e as injeções exatas avaliam o incremento 440 com `M_f,χ_f` comuns. Registrar manifesto e hashes antes de qualquer injeção de poder. Nada abre D ou move gate.
"""
    newline = "\r\n" if b"\r\n" in original else "\n"
    suffix = correction.replace("\n", newline).encode("utf-8")
    temp = PLAN.with_name(PLAN.name + ".tmp")
    with temp.open("xb") as stream:
        stream.write(original + suffix)
        stream.flush()
        os.fsync(stream.fileno())
    if temp.stat().st_size != len(original) + len(suffix):
        raise RuntimeError("plan temporary size mismatch")
    os.replace(temp, PLAN)
    revised = PLAN.read_bytes()
    if not revised.startswith(original) or len(revised) <= len(original):
        os.replace(backup, PLAN)
        raise RuntimeError("plan prefix was not preserved")

    d = ramo["conjuntos"]["D"]
    manifest = {
        "status": "INCOMPLETE_FAIL_CLOSED__NO_POWER_RUN",
        "event_universe_from_v1_not_new_data": d["eventos_elegiveis"],
        "data_quality_holds_from_v1": d["com_data_quality_hold"],
        "event_list_final_pinned": None,
        "event_list_hash": None,
        "psd_per_event_and_detector": None,
        "psd_hashes": None,
        "analysis_windows": None,
        "window_hashes": None,
        "priors_and_bounds": None,
        "prior_hash": None,
        "start_time_rule": None,
        "waveform_family_and_version": None,
        "waveform_hash": None,
        "detector_covariance": None,
        "injection_seed_and_null_repetitions": None,
        "complete_before_power": [
            "event_list_final_pinned", "event_list_hash", "psd_per_event_and_detector", "psd_hashes",
            "analysis_windows", "window_hashes", "priors_and_bounds", "prior_hash", "start_time_rule",
            "waveform_family_and_version", "waveform_hash", "detector_covariance", "injection_seed_and_null_repetitions"
        ],
        "complete_before_data_D": ["power_result_hash", "independent_audit_hash", "operator_specific_opening_act"]
    }
    v2 = {
        "id": "F4.3_220_PLUS_440_SHARED_SOURCE_V2_DESIGN",
        "unit": "F4.3",
        "status": "PRE_REGISTERED_DESIGN__AWAITING_POWER__OPERATOR_REQUEST_SUSPENDED__NO_DATA_OPENED",
        "supersedes_for_reading_only": pin(OLD),
        "plan_with_addendum": pin(PLAN),
        "sources": {"audit_c1": audit_pin, "clock_sonda": clock_pin, "ramo_b_v1": pin(RAMO_V1), "qnm_grid": pin(QNM)},
        "clock": {
            "decision_formula": "tau_star = (2*pi/kappa_hat(chi_f))*G*M_f/c^3; one k and one M_f per event for 220 and 440",
            "k_at_chi_0p6145_0p67847_0p70": [clock["v1_clock"][k]["k"] for k in ("0.614500", "0.678470", "0.700000")],
            "delta_tau_220_exact": [clock["v1_clock"][k]["dtau220_pred"] for k in ("0.614500", "0.678470", "0.700000")],
            "delta_tau_440_fixed_source": [clock["v1_clock"][k]["dtau440_pred_fixed_source"] for k in ("0.614500", "0.678470", "0.700000")],
            "q220_required": [clock["v1_clock"][k]["Q220_required"] for k in ("0.614500", "0.678470", "0.700000")],
            "prograde_grid_q_min": clock["v1_clock"]["0.678470"]["Q220_min_kerr_grid"],
            "prograde_only_conclusion": "no (M,chi) in pinned prograde grid absorbs 220 at V1 clock [DERIVED by c1]",
            "counter_rotating_family": "220-only can be absorbed at chi~0.10..0.22 and M/M_f~0.58..0.72 [DECLARED by c1/skeptic; not recalculated here]",
            "only_full_IMR_closes_counter_rotating_escape": True,
            "legacy_k1_scope": "seq 58/87/91, C6 lnB~-0.0026, B2 Fisher and GW250114 proxy ~0.06 sigma; historical controls only, not V1 power"
        },
        "hypotheses": {
            "GR": "Kerr 220 and 440, same final mass/spin, per-mode amplitudes/phases profiled",
            "B_220_440": "V1 local KMS clock, exact additive-rate envelope for both modes; 440 deformation is INPUT",
            "B_220_only": "control: 220 deformed, 440 Kerr",
            "canonical": "Planck-clock correspondence control"
        },
        "v1_reconciliation_and_fwer": {
            "primary": "sealed Ramo B V1 full IMR on D; control C3",
            "secondary": "F4.3 ringdown-only diagnostic on same D; no independent claim",
            "control_C8": "one k and one M_f; 221 never credited to 440",
            "alpha_one_sided_per_relevant_null": 2.8665e-7,
            "rule": "V1 verdict first; F4.3 can corroborate only the same direction if V1 and F4.3 each have calibrated one-sided p <= alpha. Intersection controls false joint claim at <= primary V1 alpha without independence. F4.3 alone remains diagnostic.",
            "two_tails": {
                "under_B_null": "p_B for evidence excluding the named B pair; calibrated under B injections",
                "under_GR_null": "p_GR for evidence reporting GR tension; calibrated under GR injections",
                "both_rejected": "INCONCLUSIVE_SYSTEMATICS__BOTH_MODELS_REJECTED",
                "neither_rejected": "NOT_FALSIFIED_POWERED if exact injected power passed; otherwise UNDERPOWERED_OR_NONIDENTIFIABLE",
                "single_threshold_note": "same alpha per relevant null; never combine two one-sided p values into a two-sided 5-sigma claim"
            },
            "official_vocabulary": ["FALSIFIED_AT_5SIGMA", "NOT_FALSIFIED_POWERED__GR_TENSION_REPORTED", "NOT_FALSIFIED_POWERED", "NOT_FALSIFIED_UNDERPOWERED", "INCONCLUSIVE_SYSTEMATICS"],
            "retired_v1_draft_token": "FAVORS_PAIR_B_220_440_AT_5SIGMA"
        },
        "synthetic_identifiability_screen_INPUT": {
            "svd_relative_cutoff_rcond": 1e-10,
            "eta_joint_min": 25.0,
            "eta_increment_440_min": 1.0,
            "eta_formula": "eta=||[I-(WJ)(WJ)^+] W(mu_B-mu_GR)||^2; eta_increment_440=max(0,eta_joint-eta_220)",
            "limits": "design choices for synthetic screening only; do not imply 5 sigma, physical power or permission to open D",
            "x_around_0p6": "linear SVD is outside perturbative regime; use exact delta_tau=-x/(1+x) in injections",
            "exact_injection_power_gate": "calibrated >=90% recovery at one-sided 5 sigma, plus null coverage, bias/systematics and waveform/start/PSD checks",
            "failed_or_missing": "UNDERPOWERED_OR_NONIDENTIFIABLE or INCONCLUSIVE_SYSTEMATICS; no D opening"
        },
        "execution_manifest": manifest,
        "ordered_output": ["AWAITING_POWER", "UNDERPOWERED_OR_NONIDENTIFIABLE", "INCONCLUSIVE_SYSTEMATICS", "DIAGNOSTIC_CORROBORATES_V1_SAME_DIRECTION", "DIAGNOSTIC_ONLY"],
        "no_observational_data_opened": True,
        "no_gate_change": True,
        "not_construction_of_physical_solution": True
    }
    atomic_new(V2, json_bytes(v2))
    result = {
        "unit": "F4.3", "status": "ENTREGUE_C1_R1_R2_R3_V2__AWAITING_REAUDIT",
        "scope": "additive correction; no strain/PE/data opened, no power measured, no gate change",
        "existing_from_nos_vivo": "ringdown.modo_unico.degenerescencia seq 58/87/91 and B2/QNM/V1 Ramo B reused",
        "audit_request_suspended": True,
        "files": [pin(PLAN), pin(backup), pin(OLD), pin(V2), audit_pin, clock_pin, pin(RAMO_V1), pin(QNM)],
        "backup_prefix_exact": original == backup.read_bytes(),
        "old_plan_prefix_preserved": PLAN.read_bytes().startswith(original),
        "registration_pending_parent": True
    }
    atomic_new(RESULT, json_bytes(result))
    print(json.dumps({"plan": pin(PLAN), "backup": pin(backup), "v2": pin(V2), "result": pin(RESULT)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
