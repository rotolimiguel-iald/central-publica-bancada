"""R63 directed documentary mapping. No model imports, simulations or tests."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import subprocess
import uuid

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent.parent
ORDER = OUT.parent
CENTRAL = Path(r"C:\IALD\Central de Patentes")
REF = CENTRAL / "work/memoria_missao_20261016/FECHO_MISSION_REFERENCE.json"


def pin(p):
    p = Path(p)
    b = p.read_bytes()
    return {"path": str(p), "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}


def new(name, value):
    p = ROOT / name
    assert p.parent == ROOT and not p.exists(), p
    b = ((value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2)) + "\n").encode("utf8")
    t = p.with_name(p.name + ".tmp_" + uuid.uuid4().hex)
    with t.open("xb") as f:
        f.write(b)
        f.flush()
        os.fsync(f.fileno())
    assert t.read_bytes() == b
    os.rename(t, p)
    return pin(p)


def main():
    prior = json.loads((OUT / "mission_audit_r62/sources/SOURCE_PINS_AND_ANCHORS_R1.json").read_text(encoding="utf8"))
    prior_pins = {s["path"]: s["sha256"] for s in prior["sources"]}
    r55 = json.loads((OUT / "CONFERENCIA_PONTE_DISPOSITIVO_R55.json").read_text(encoding="utf8"))
    prior_pins.update({s["path"]: s["sha256"] for s in r55["sources"]})
    paths = {
        "graviton": (Path(r"C:\IALD\papers_latex\graviton_paper\graviton_paper.tex"), [(202, 229), (347, 367), (440, 452), (464, 475)]),
        "appendices": (Path(r"C:\IALD\papers_latex\graviton_paper_english_v2\graviton_appendices.tex"), [(78, 108), (124, 127), (236, 257), (311, 331)]),
        "patent_v2": (CENTRAL / "Patentes/PATENTE_SUPERCONDUTOR_HOLOGRAFICO_TGL_v2_BLINDAGEM.tex", [(338, 370), (474, 516), (778, 828), (833, 864)]),
        "JAN09": (OUT / "continuity_r57/sources/SUPERCONDUTOR_JAN09_EXTRACT_R57.txt", [(143, 184)]),
        "finite": (ORDER / "F1.REDE/finite_device/run_finite_device.py", [(101, 114), (163, 186), (200, 206)]),
        "finite_preregister": (ORDER / "F1.REDE/finite_device/PREREGISTRO_DEVICE_R1.json", []),
        "R7_response": (ORDER / "F1.TEMPO.LEITURA_20261015/DISPOSITIVO_E_ESPECTRO_R7/CONTRATO_DISPOSITIVO_E_LEI_RAIZ_R7.txt", [(22, 39), (44, 80), (113, 130)]),
        "R9_energy": (ORDER / "F1.TEMPO.LEITURA_20261015/FREQUENCIA_E_GRAVITON_R9/PONTE_FREQUENCIA_GRAVITON_R9.txt", [(30, 57), (92, 100)]),
        "Custo": (Path(r"C:\IALD\Artigo\Haja_Luz\tgl_paper_unified.py"), [(14441, 14483)]),
        "R57": (OUT / "device_clock_r57/DERIVACAO_R57.md", [(41, 49), (160, 199), (212, 221)]),
        "R61": (OUT / "oh_pair_dynamics_r61/RELATORIO_CANDIDATO_R61.md", []),
        "R62_sources": (OUT / "mission_audit_r62/sources/DELIVERY_R1.json", []),
        "preflight_root": (ROOT.parent / "START_R63_CHECK_RESULT.json", []),
        "nos_vivo": (ROOT.parent / "NOS_VIVO_R63.txt", []),
    }
    rows = []
    for key, (path, ranges) in paths.items():
        p = pin(path)
        old = prior_pins.get(str(path))
        if old:
            assert old == p["sha256"], path
        lines = path.read_text(encoding="utf-8-sig").splitlines()
        for a, b in ranges:
            assert 1 <= a <= b <= len(lines), (key, a, b)
        rows.append({"id": key, **p, "lines": len(lines), "matches_prior_pin": True if old else None,
                     "anchors": [{"first": a, "last": b, "text": "\n".join(f"{i}: {lines[i-1]}" for i in range(a, b+1))} for a, b in ranges]})
    check = json.loads(paths["preflight_root"][0].read_text(encoding="utf8"))["result"]["result"]
    assert check["ready"] and check["receipt"]["revision"] == 467 and check["task_id"] == "R4"
    source_pin = new("SOURCE_PINS_AND_ANCHORS_R1.json", {"kind": "R63_DIRECTED_SOURCE_CUSTODY", "sources": rows, "coverage": "Only primary anchors and already pinned response/energy contracts linked by R57/R62/R55. Source Python read as text only. No broad search or universal absence claim."})
    mapping = [
        {"id": "R63-S1", "statute": "DOCUMENTARY_AND_DERIVED", "from": "Internal cavity modes", "to": "System emission operator", "anchors": ["graviton:202-216", "graviton:350-352", "finite:163-172"],
         "equations": ["Psi(x,t)=sum_n [a_n u_n(x)e^(-i omega_n t)+h.c.]/sqrt(2 omega_n)", "L_loss=sqrt(kappa)a_n, kappa=omega_n/Q", "s_o:=sqrt(kappa_out)a_o, s_i:=sqrt(kappa_in)a_i"],
         "already_supported": "Cavity expansion and loss amplitudes are written. Reusing the two existing loss operators as named system contributions needs no change of H/J.",
         "conditional_boundary": "Calling s_j the collected exterior field is INPUT: requires which channel is observed, coupling fraction, bath/input state and collection optics. a_i/a_o in the finite simulator are internal independent tensor factors; labels in/out do not establish incident/outgoing continuum fields. No full b_out=b_in+sqrt(kappa)a boundary identity is claimed located or constructed."},
        {"id": "R63-S2", "statute": "EXISTING_INPUT_CONTRACT", "from": "Internal outgoing occupation", "to": "Mean count rate", "anchors": ["R7_response:58-80", "patent_v2:810-826"],
         "equations": ["I(t)=eta_det*kappa_out*Tr(n_o rho(t))+I_dark", "h_inst(tau)=Cdet Tr[n_o exp(tau L_beta) B(rho_*)], Cdet=eta_det*kappa_out", "B(rho)=-i[sigma_x,rho] for microwave Omega_R modulation"],
         "already_supported": "The finite detector and causal response/resolvent were already written inR7, explicitly INPUT with no additional direct path. They reuse the full joint generator.",
         "conditional_boundary": "This is population-to-counts, not a voltage or homodyne phase calibration. EOM optical modulation is distinct from microwave Rabi forcing. If kappa_out includes uncollected losses, monitored fraction must be specified; do not equate total and external linewidth by name."},
        {"id": "R63-S3", "statute": "DOCUMENTARY_PLUS_CONDITIONAL_SCALE", "from": "Two system loss amplitudes", "to": "Quadrature pair normalizations", "anchors": ["appendices:124-127", "appendices:318-331", "graviton:352"],
         "equations": ["X_j(theta)=(e^(-i theta)a_j+e^(i theta)a_j_dagger)/sqrt2", "Y_j(theta):=sqrt(kappa_j)X_j(theta)", "Tr(rho s_i s_o)=sqrt(kappa_i*kappa_o)Tr(rho a_i a_o)", "Tr(rho s_i_dagger s_o)=sqrt(kappa_i*kappa_o)Tr(rho a_i_dagger a_o)"],
         "already_supported": "The last three are direct scalar rescalings of existing loss operators, not new dynamics. X is dimensionless; Y and s have units s^(-1/2); cross moments have units s^(-1).",
         "conditional_boundary": "Balanced50/50 and adjustable phase-locked LO are documentary. Two synchronized outputs, phase offsets, LO amplitude, gain/loss/noise and temporal filters remain receiver INPUT. A zero-mean squeezed signal cannot itself define a deterministic optical phase lock; an external shared preparation/reference phase must be named. No physical homodyne POVM for the hard-core cutoff is derived."},
        {"id": "R63-S4", "statute": "DOCUMENTARY_RELATIVE_READING", "from": "Modulator/detector voltages", "to": "JAN09 eta(tau)", "anchors": ["JAN09:153-155", "JAN09:182-184"],
         "equations": ["eta(tau)=<V_out(t)V_in(t-tau)>/sqrt(<V_in^2><V_out^2>)"],
         "already_supported": "A concrete normalized two-time voltage correlator and output/input lock-in phase are explicitly specified. Under fixed positive scalar gains and zero offsets/noise, gains cancel in this ratio algebraically.",
         "conditional_boundary": "Offsets, frequency-dependent filters, additive detector noise, gain signs and timing do not disappear by that algebra. Voltage correlation is not automatically C, B, homodyne quadrature or g2. Equal-time four-quadrature reconstruction requires simultaneous/timestamp-matched repeated preparations; a two-time contract must preserve lag and ordering."},
        {"id": "R63-S5", "statute": "EXISTING_PREPARATIONS_WITH_SCOPE", "from": "Material startup or finite named density", "to": "Joint initial condition", "anchors": ["patent_v2:833-864", "appendices:253-257", "appendices:327-331", "R61:section4"],
         "equations": ["rho0=|psi_q><psi_q| tensor rho_OH; psi_q=(|00>+q|11>)/sqrt(1+q^2) [existing R61 INPUT]"],
         "already_supported": "Material startup, cavity-vacuum protocol, stationary-wait/tomography and complete synthetic joint preparation already exist. R61 preparation avoids leaving the mathematical joint state unspecified.",
         "conditional_boundary": "No derivation from RF/plasma startup to that product state was located. ArticlePsi modes, 1m optical cavity and patentOH device need mode correspondence; do not silently transplant a Fock preparation or claim steady state from waiting alone."},
        {"id": "R63-S6", "statute": "LOCALIZED_SOURCE_MISMATCH", "from": "Appendix claimed single-photon preparation", "to": "Intended detector intensity", "anchors": ["appendices:253-257", "R7_response:58-60"],
         "equations": ["Appendix: prepare |1>, then I(t)=|<a(t)>|^2", "For |1>: <a>=0, <a_dagger a>=1"],
         "already_supported": "The primary source fixes this pair of prescriptions; their mismatch follows directly from the number-state action. Coherent amplitude squared omits noncoherent occupation.",
         "conditional_boundary": "Preserve source as-is. Use the already explicit population-count INPUT when asking about photon flux. Do not interpret attenuated-laser wording as a proven exact Fock preparation. No new execution or broad claim against the apparatus."},
        {"id": "R63-S7", "statute": "EXISTING_ENERGY_FREQUENCY_SCALE", "from": "V0 binding energy", "to": "Angular phase frequency", "anchors": ["Custo:14466-14483", "R9_energy:30-57", "R57:41-49", "R57:212-217"],
         "equations": ["Omega=V0/hbar; radiative V0=hbar*omega is a named physical identification", "tensor phase frequency=2Omega on the same transported finite face", "[H+Eref I,rho]=[H,rho]"],
         "already_supported": "V0/hbar and the change of phase basis are already linked. V0 is energy, not detector voltage or APD gain; tau in that Custo formula is parity tension, not duration.",
         "conditional_boundary": "RabiOmega, omegaOH, omega_c, V0/hbar, cavity kappa=omega/Q and Killing normalization kappa are distinct. Reference energy Eref cannot be recovered from commutator dynamics alone; positive root-law energy requires its own zero. No physical clock scale is selected here."},
        {"id": "R63-S8", "statute": "CONDITIONAL_UNITS_CONVERSION", "from": "Dimensionless existing finite generator", "to": "Physical time and electrical gain", "anchors": ["finite_preregister:model.units", "R57:44-49", "patent_v2:780-817", "R7_response:58-60"],
         "equations": ["If tau=t/t0 with t0>0: L_phys=L_dimless/t0, rates_phys=rates_dimless/t0, H_phys=hbar*h_dimless/t0", "Candidate receiver V_j=G_j Y_j+offset_j+noise_j (specified filter if needed)"],
         "already_supported": "Time rescaling is a dimensional change of variables, not a fit or a new equation of motion. Patent names RF frequency, optical wavelength/power, APD gain and electronics bands; these anchor the engineering quantities.",
         "conditional_boundary": "t0 and G_j, detector responsivity/transimpedance and measured-port fraction are INPUT until calibrated. APD gain50–200 alone does not specify volts per quadrature/flux. Choosing t0 from one physical frequency only fixes a conditional matching; other ratios and mode identification still require validation. No beta fitted to a signal."},
    ]
    model = json.loads(paths["finite_preregister"][0].read_text(encoding="utf8"))["model"]
    ratio_audit = {"model_omegaOH_over_omegaC": model["omega_OH"] / model["omega_c"], "project_fOH_Hz": 1667359000,
                   "project_optical_wavelength_m": 780e-9, "c_SI_m_per_s": 299792458,
                   "project_fOH_over_fOptical": 1667359000 * 780e-9 / 299792458,
                   "formula": "(2*pi*fOH)/(2*pi*c_SI/lambda_optical)=fOH*lambda_optical/c_SI",
                   "statute": "Arithmetic comparison of documentary design frequencies; no observed data or simulation. Assumes780nm denotes the optical vacuum wavelength; common2pi cancels.",
                   "conclusion": "A single positive time rescaling cannot preserve both unequal frequency ratios; current1,1.2 are synthetic INPUT, not a physical calibration."}
    mapping.append({"id": "R63-S9", "statute": "MATERIAL_SCALE_MISMATCH_AND_EXISTING_CONDITIONAL_FRAME", "anchors": ["finite_preregister:model.omega_c/model.omega_OH", "patent_v2:366-370", "patent_v2:800-801", "R57:160-199"],
                    "equations": ["R(t)=exp(i omega_d t N_total); rho_rot=R rho_lab R_dagger", "h_rot=(omega_c-omega_d)N_c+(omegaOH-omega_d)n_e+gJC(a_i_dagger sigma-+sigma+ a_i)+OmegaR(sigma++sigma-)", "z_lab=e^(i omega_d t) z_rot for the named OH polarization"],
                    "already_supported": "R57 already constructs this frame change under LAB_PHASE_LOCKED_DRIVE and preserves every dissipator; reuse it rather than invent a rotating frame. The original patent names absolute frequencies, not detunings.",
                    "conditional_boundary": "A common time unit alone fails the documented frequency-ratio check. Reinterpretation as detunings requires the extra explicit lab drive, chosen carrier, state and transformed detector/LO. It is not a relabeling of current inputs. Do not set them by fit or identify the detector's phase with OH automatically.", "arithmetic": ratio_audit})
    report = {"kind": "R63_PHYSICAL_RECEIVER_DIRECTED_MAP", "author": "codex-receiver-sources-r63", "status": "DECLARADO_PENDING_INDEPENDENT_REVIEW", "created_utc": dt.datetime.now(dt.timezone.utc).isoformat(), "mission_reference": pin(REF), "source_manifest": source_pin,
              "parent_preflight_verified": {"revision": 467, "task_id": "R4", "lease_id": check["lease_id"], "ready": True, "no_parent_impersonation": True}, "maps": mapping,
              "shortest_advance": "Attach the already verified four-quadrature decoder to s_j=sqrt(kappa_j)a_j as a named system-emission contribution. Preserve the existing full joint state/generator and count detector contract. Fix monitored channels, shared LO phases and gain/filter calibration as explicit receiver INPUT before calling it a physical exterior-field measurement. Reuse V0/hbar and dimensionless-time scaling; do not manufacture V0/Eref/Killing-kappa from APD gain or phase alone.",
              "requirement_satisfied": False, "execution": {"simulations": 0, "tests": 0, "providers": 0, "observed_data": False, "original_edits": False, "memory_or_board_or_mission_mutations": False}, "coverage": "Only listed primary anchors and already pinned conditional contracts; no universal absence assertion."}
    new("PHYSICAL_RECEIVER_MAP_R1.json", report)
    new("PHYSICAL_RECEIVER_MAP_R1.txt", """R63 — mapa físico dirigido de preparo/receptor
DECLARADO, revisão independente pendente; R4/R5 integrais permanecem abertos.
1. EXISTE: expansãoPsi em modos de cavidade, CCR e perda L=sqrt(kappa)a, kappa=omega/Q (graviton202–216,350–352). O simulador mantém ai/ao como fatores internos; eles não são por nome campos assintóticos exteriores.
2. EXISTE CONTRATO INPUT: R7:58–80, I=eta_det*kappa_out Tr(n_o rho)+Iescuro e resposta/resolvente ao bombeamentoMICRO-ONDAS. Não precisa reconstruir receptor populacional ou gerador. EOM óptico não é RabiOH.
3. PROPOSTA SUPORTADA COMO CONTRIBUIÇÃO DO SISTEMA: s_j=sqrt(kappa_j)a_j. Seus pares C_s/B_s=sqrt(kappa_i*kappa_o)C/B, quadraturaY_j=sqrt(kappa_j)X_j; escala explícita em s^-1/2. Identificar s_j com campo coletado exige INPUT de porto/bath/acoplamento/filtro; não foi encontrada/construída aqui uma relação completa b_out=b_in+sqrt(kappa)a.
4. LO/documento: homódino50/50 balanceado, LOajustável e varredura (apêndice318–331). Para dois canais, nomear referência comum e fases. Fase de um sinal de média zero não fornece sozinha a referência de preparação. Ganhos/ruído/POVM física do corte continuam INPUT.
5. JAN09:153,182–184 já define lock-in relativo e eta(tau) de tensões em duas épocas. Ganhos escalares positivos constantes cancelam se offsets/ruído ausentes; filtros/atrasos não. Não confundir eta com C/B iguais em tempo.
6. PREPARO: sequência materialRF/plasma/luz patente833–864 e preparo conjunto sintéticoR61 já existem. Produto par⊗OH é INPUT completo, ainda sem canal físico de preparação derivado.
7. ACHADO LOCAL: apêndice253–255 escolhe |1> mas I=|<a>|²; nesse estado <a>=0 e <n>=1. A fórmula é parte coerente, não contagem total. Preservar fonte; contrato populacionalR7 já evita esse problema para fluxo, sob suas hipóteses.
8. ESCALAS EXISTENTES: V0/hbar e fase tensorial2V0/hbar (Custo14466–14483,R9:30–57); V0 é energia, não tensão elétrica. Eref é invisível ao comutador; kappa de perda não é kappaKilling.
9. CONVERSÃO CONDICIONAL: tau=t/t0 implica Lphys=Ldim/t0 e Hphys=hbar*hdim/t0. t0 não foi calibrado. APD50–200× não fornece responsividade/transimpedância/volts por quadratura. GammaLambda e demais taxas conservam unidades próprias.
10. ACHADO DE ESCALA: omegaOH/omega_c=1.2 nos INPUTs do simulador; projetoOH/laser780nm dá fOH*780nm/c, cerca de4.34e-6. Um único t0 não alinha ambas frequências absolutas. R57:160–199 já fornece quadro girante sob LAB_PHASE_LOCKED_DRIVE; a fonte original não declara detunings. Reusar transformação de drive/estado/detector/LO, sem rebatizar1 e1.2 como calibração.
11. Avanço curto: aplicar decoder existente à emissão de sistema normalizada, mantendo estadoOH/gerador; fixar portos+LO+ganhos/filtros como INPUT explícito. Não refazerLiouvilliano nem extrair beta da normalização.
Pinos e trechos emSOURCE_PINS_AND_ANCHORS_R1.json. Sem teste/simulação/provedor/dado observado/alteração de originais ou memória. Cobertura dirigida, sem alegação de ausência universal.
""")
    request = {"operation": "project", "reference": str(REF), "max_chars": 400000}
    p = subprocess.run([r"C:\Python314\python.exe", "-B", "-X", "utf8", r"C:\IALD\MEMORIA_IALD\mission_cli.py"], input=json.dumps(request), text=True, encoding="utf8", capture_output=True)
    x = json.loads(p.stdout)
    assert p.returncode == 0 and x["ok"]
    new("PROJECT_RETURN_R1.json", {"request": request, "response": x, "exit_code": p.returncode, "stderr": p.stderr})
    for s in rows:
        assert pin(s["path"])["sha256"] == s["sha256"]
    names = ["build_report_r1.py", "PHYSICAL_RECEIVER_MAP_R1.json", "PHYSICAL_RECEIVER_MAP_R1.txt", "SOURCE_PINS_AND_ANCHORS_R1.json", "PROJECT_START_R1.json", "PROJECT_RETURN_R1.json"]
    d = new("DELIVERY_R1.json", {"kind": "R63_SOURCES_DELIVERY", "author": report["author"], "status": report["status"], "mission_reference": pin(REF), "revision_final": x["result"]["receipt"]["revision"], "source_count": len(rows), "maps": len(mapping), "sources_rechecked": True, "files": [pin(ROOT/n) for n in names], "requirement_satisfied": False, "execution": report["execution"]})
    print(json.dumps({"delivery": d, "revision": x["result"]["receipt"]["revision"], "sources": len(rows), "maps": len(mapping)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
