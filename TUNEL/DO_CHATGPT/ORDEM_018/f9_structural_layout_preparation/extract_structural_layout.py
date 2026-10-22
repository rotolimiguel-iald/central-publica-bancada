"""Extract only structural background layout and alpha provenance.

No numerical catalogue centre is captured, converted, printed, or written.
DESI source bytes are hashed in full; regex captures only redshift and label.
No scientific module, solver, original script, table or control is executed.
"""
from pathlib import Path
import re
import json
import hashlib
import os
import tempfile
import datetime

ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018")
T4 = ROOT / "reproducao_fase45_conjunta"
OUT = ROOT / "f9_structural_layout_preparation"


def pin(path, data=None):
    raw = path.read_bytes() if data is None else data
    return {"path": str(path), "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest()}


def check(path, expected):
    data = path.read_bytes()
    actual = pin(path, data)
    assert actual["sha256"] == expected["sha256"], "PIN_MISMATCH:" + str(path)
    if "bytes" in expected:
        assert actual["bytes"] == expected["bytes"], "SIZE_MISMATCH:" + str(path)
    return data, actual


def new_bytes(name, data):
    path = OUT / name
    assert not path.exists(), "NO_OVERWRITE:" + str(path)
    fd, temporary = tempfile.mkstemp(prefix=name + ".tmp_", dir=OUT)
    with os.fdopen(fd, "wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    assert Path(temporary).read_bytes() == data
    os.replace(temporary, path)
    assert path.read_bytes() == data


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def run():
    OUT.mkdir(exist_ok=True)
    resolver_path = ROOT / "f9_consolidated_draft/RESOLUTOR_F9.json"
    resolver_bytes = resolver_path.read_bytes()
    # Parse only the documentary entry, not the entire resolver content.
    found = re.search(rb'"historical_background_sources"\s*:\s*(\{[^{}]*\})',
                      resolver_bytes)
    assert found is not None, "T4_ENTRY_NOT_FOUND"
    t4_entry = json.loads(found.group(1))
    assert Path(t4_entry["path"]) == T4 / "T4_PROTOCOLO.json"
    proto_bytes, proto_pin = check(T4 / "T4_PROTOCOLO.json", t4_entry)
    proto = json.loads(proto_bytes, parse_float=str)
    historical_manifest_path = T4 / "MANIFESTO.json"
    historical_manifest_bytes = historical_manifest_path.read_bytes()
    historical_manifest = json.loads(historical_manifest_bytes)
    hist = {Path(x["path"]).name: x for x in historical_manifest["artifacts"]}
    audit_bytes, audit_pin = check(T4 / "AUDITORIA_E_CONTRATOS.json",
                                  hist["AUDITORIA_E_CONTRATOS.json"])
    # Select only path/size/hash before the nested definition inventory.
    origin_match = re.search(
        rb'"d1/d1_v3_pipeline.py"\s*:\s*\{\s*"path"\s*:\s*("(?:\\.|[^"\\])*")'
        rb'\s*,\s*"bytes"\s*:\s*([0-9]+)\s*,\s*"sha256"\s*:\s*"([a-f0-9]{64})"',
        audit_bytes)
    assert origin_match is not None, "ALPHA_ORIGIN_PIN_NOT_FOUND"
    origin_path = Path(json.loads(origin_match.group(1)))
    origin_expected = {"bytes": int(origin_match.group(2)),
                       "sha256": origin_match.group(3).decode("ascii")}
    origin_bytes, origin_pin = check(origin_path, origin_expected)
    alpha_matches = []
    alpha_pattern = re.compile(rb"^ALPHA_FINE_CODATA_2018\s*=\s*([0-9]+\.[0-9]+)\s*$")
    for number, raw in enumerate(origin_bytes.splitlines(), 1):
        match = alpha_pattern.fullmatch(raw)
        if match:
            alpha_matches.append({"line": number, "source_text": raw.decode("ascii"),
                                  "decimal_token": match.group(1).decode("ascii")})
    assert len(alpha_matches) == 1, "ALPHA_ASSIGNMENT_AMBIGUOUS"
    alpha = alpha_matches[0]
    inputs_path = T4 / "ENTRADAS_HISTORICAS_E_COVARIANCIAS.json"
    inputs_bytes, inputs_pin = check(inputs_path, {"sha256": proto["file_pins"][inputs_path.name]})
    # Do not json.load the observed means/CC fields. Capture only alpha's lexical token.
    alpha_input = re.search(rb'^\s*"alpha_codata2018"\s*:\s*([0-9]+\.[0-9]+)\s*,',
                            inputs_bytes, flags=re.M)
    assert alpha_input and alpha_input.group(1).decode("ascii") == alpha["decimal_token"]
    alpha_input_line = inputs_bytes[:alpha_input.start()].count(b"\n") + 1

    t4_manifest_path = T4 / "T4_MANIFESTO.json"
    t4_manifest_bytes = t4_manifest_path.read_bytes()
    t4_manifest = json.loads(t4_manifest_bytes)
    t4_pins = {Path(x["path"]).name: x for x in t4_manifest["artifacts"]}
    code_path = T4 / "T4_reproduzir.py"
    code_bytes, code_pin = check(code_path, t4_pins[code_path.name])
    code_lines = code_bytes.decode("utf-8-sig").splitlines()
    expected_lines = {
        40: '    names=("z_star","z_drag","r_star","r_drag","DM_star")',
        74: '        self.beta=float(inputs["alpha_codata2018"])*math.sqrt(math.e)',
        78: '        self.zbao=np.array([float(r[0]) for r in rows]); self.bao=np.array([float(r[1]) for r in rows])',
        79: '        self.kinds=[r[2] for r in rows]; self.Lbao=np.linalg.cholesky(np.loadtxt(dr2cov))',
        99: '        obs={"DM_over_rs":dm,"DH_over_rs":dh,"DV_over_rs":dv}',
        100: '        bao=np.array([obs[k][i] for i,k in enumerate(self.kinds)])/cam["r_drag"]',
        101: '        pl=np.array([math.sqrt(om)*H/self.c*cam["DM_star"],math.pi*cam["DM_star"]/cam["r_star"],wb])',
        102: '        istar=(2/3)*math.log(float(E(PROTO["z_star_law"])))',
    }
    for number, text in expected_lines.items():
        assert code_lines[number - 1] == text, "STRUCTURAL_CODE_CHANGED:" + str(number)

    mean_path = T4 / "T4_desi_mean.txt"
    mean_bytes, mean_pin = check(mean_path, {"sha256": proto["file_pins"][mean_path.name]})
    cov_path = T4 / "T4_desi_cov.txt"
    _, cov_pin = check(cov_path, {"sha256": proto["file_pins"][cov_path.name]})
    # Central column is the non-captured middle token. It is not decoded or parsed.
    pattern = re.compile(
        rb"^\s*([+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+))\s+\S+\s+([A-Za-z_]+)\s*$")
    bao = []
    mapping = {"DM_over_rs": ("DM_over_rdrag", "DM(z)/rdrag"),
               "DH_over_rs": ("DH_over_rdrag", "DH(z)/rdrag"),
               "DV_over_rs": ("DV_over_rdrag", "DV(z)/rdrag")}
    for number, raw in enumerate(mean_bytes.splitlines(), 1):
        if not raw.strip() or raw.lstrip().startswith(b"#"):
            continue
        match = pattern.fullmatch(raw)
        assert match is not None, "UNRECOGNIZED_DESI_ROW:" + str(number)
        z = match.group(1).decode("ascii")
        label = match.group(2).decode("ascii")
        assert label in mapping, "UNRECOGNIZED_DESI_OBSERVABLE"
        name, formula = mapping[label]
        index = len(bao) + 1
        bao.append({"index_1based": index + 3, "block": "desi_dr2",
                    "block_index_1based": index, "observable": name,
                    "source_label": label, "redshift_decimal": z,
                    "redshift_semantics": "effective_BAO_bin_redshift",
                    "units": "1", "distance_units_before_ratio": "Mpc",
                    "prediction_formula": formula,
                    "standard_denominator": "rdrag_Mpc_not_rstar",
                    "source_path": str(mean_path), "source_line": number})
    assert len(bao) == 13, "DESI_COMPONENT_COUNT"
    background_path = ROOT / "f9_background_prediction/PROTOCOL.json"
    background_bytes = background_path.read_bytes()
    background = json.loads(background_bytes, parse_float=str)
    redshifts = background["redshifts"]
    assert redshifts["z_star_law"] == proto["z_star_law"]
    assert redshifts["recombination_z"] == "derived zstar"
    assert redshifts["drag_z"] == "derived zdrag"
    cmb = []
    cmb_fields = (
        ("R", "sqrt(Omega_m)*H0*DM_star/c", "derived_recombination_zstar", "DM_star"),
        ("l_A", "pi*DM_star/rstar", "derived_recombination_zstar", "DM_star_and_rstar"),
        ("omega_b_h2", "omega_b_h2", "physical_density_parameter_no_single_bin_redshift", None),
    )
    for index, (name, formula, epoch, field) in enumerate(cmb_fields, 1):
        cmb.append({"index_1based": index, "block": "planck_comp",
                    "block_index_1based": index, "observable": name,
                    "source_label": name, "redshift_decimal": None,
                    "redshift_semantics": epoch, "thermal_background_field": field,
                    "units": "1", "prediction_formula": formula,
                    "source_path": str(code_path), "source_line": 101})
    source_pins = [
        pin(resolver_path, resolver_bytes), proto_pin,
        pin(historical_manifest_path, historical_manifest_bytes), audit_pin,
        pin(t4_manifest_path, t4_manifest_bytes), code_pin, inputs_pin,
        mean_pin, cov_pin, origin_pin, pin(background_path, background_bytes),
    ]
    layout = {
        "schema": "F9_BACKGROUND_STRUCTURAL_LAYOUT_V1",
        "identity": "chatgpt-codex/ordem-018/derivacoes",
        "created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "status": "STRUCTURAL_PROJECTION_NO_OBSERVED_CENTRES",
        "map_before": 538, "T4_root": str(T4),
        "scope": "ordered 3CMB+13BAO labels, units, redshifts and alpha provenance only",
        "blocks": [{"name": "planck_comp", "count": 3, "start_1based": 1},
                   {"name": "desi_dr2", "count": 13, "start_1based": 4}],
        "components": cmb + bao,
        "ordered_unique_BAO_redshift_decimals": list(dict.fromkeys(x["redshift_decimal"] for x in bao)),
        "redshift_semantics": {
            "z_law_decimal": proto["z_star_law"],
            "z_law_kind": "fixed historical INPUT for E_standard(z_law) in TGL law",
            "z_law_is_not_recombination_zstar": True,
            "zstar_thermal": {"value": None, "origin": "derived CAMB recombination output, parameter dependent"},
            "zdrag_thermal": {"value": None, "origin": "derived CAMB drag output, parameter dependent"},
            "low_z_controls_are_not_data_layout": True,
        },
        "alpha": {"symbol": "ALPHA_FINE_CODATA_2018", "decimal_token": alpha["decimal_token"],
                  "units": "1", "origin": origin_pin, "source_line": alpha["line"],
                  "source_text": alpha["source_text"], "T4_inputs_source": inputs_pin,
                  "T4_inputs_line": alpha_input_line,
                  "representation": "source decimal literal; historical Python float conversion at T4 line74",
                  "beta_rule": "ALPHA_FINE_CODATA_2018 * sqrt(e) at runtime; never stored beta literal",
                  "beta_value": None, "CODATA_lookup_or_remeasurement": False},
        "covariance_order_binding": {
            "planck": "R,l_A,omega_b_h2 from T4 pl array; covariance recipe unchanged",
            "desi": "full13x13 covariance uses exactly the row order of the pinned mean file",
            "desi_covariance": cov_pin, "covariance_values_parsed": False,
        },
        "read_scope": {
            "full_mean_file_bytes_read_and_hashed": True,
            "central_column_captured_decoded_or_converted": False,
            "raw_catalogue_copied_to_output": False,
            "historical_inputs_bytes_read": True,
            "historical_inputs_json_parsed": False,
            "alpha_token_only_extracted_from_inputs": True,
            "source_code_imported_or_executed": False,
            "solver_or_control_executed": False,
            "default_read_alpha_origin_denied_then_narrow_escalated_read": True,
        },
        "structural_code_line_checks": [{"line": k, "text": v} for k, v in expected_lines.items()],
        "sources": source_pins, "observed_values": None, "scientific_verdict": None,
        "does_not_change_models_or_authorize_execution": True,
    }
    note = """# Layout estrutural de fundo F9

[REAL — projeção documental, sem centros] O JSON fornece a API ordenada de16componentes: primeiro Planck R, l_A, omega_b_h2; depois as13linhas DESI na ordem do arquivo pinado no T4. A origem foi localizada pelo RESOLUTOR_F9, sem adivinhar nomes.

Duas rotas foram examinadas: reutilizar metadados/código existentes ou projetar somente rótulo e redshift do catálogo pinado. O código T4 resolve ordem CMB, unidades e denominador BAO, mas recebe redshifts/rótulos do arquivo externo. Por isso usou-se a segunda rota apenas para essas duas colunas.

O extrator lê e hasheia os bytes completos de T4_desi_mean.txt. A expressão regular captura somente a primeira e a terceira colunas; o token central é não capturado, não decodificado, não convertido nem escrito. Não se alega que o arquivo inteiro nunca foi lido. ENTRADAS_HISTORICAS_E_COVARIANCIAS.json também foi lido em bytes, mas não parseado como JSON: somente o token lexical de alpha foi extraído. A covariância DESI foi apenas hasheada, sem valores parseados.

A ordem BAO começa por DV em0.295; segue DM/DH em0.510,0.706,0.934,1.321,1.484; termina em z2.33 com DH e depois DM. Os textos decimais originais são preservados no JSON. Não substituir por redshifts aproximados da DR1 ou pela lista low_z_controls do piloto.

Os rótulos históricos *_over_rs são divididos por r_drag em T4_reproduzir.py:99–100. Portanto a API explicita rdrag, sem trocar por rstar. As16componentes são adimensionais; distâncias e réguas anteriores às razões são em Mpc. O bloco CC histórico do T4 não integra este layout de3+13.

R e l_A usam DM_star e rstar no redshift térmico de recombinação derivado pelo fundo. Esse redshift depende dos parâmetros e fica null até o motor produzir sua previsão. omega_b_h2 é parâmetro de densidade, não uma medida em um bin de redshift. O z_lei histórico1089.95 é fixo, separado, utilizado em E(z_lei); não substitui zstar nem zdrag.

ALPHA_FINE_CODATA_2018 foi lida na linha25 do pipeline histórico admitido. Seu pin coincide com o inventário histórico; o mesmo token consta do input T4 e é consumido na linha74 do reprodutor. A representação e a linha integral constam do JSON. Beta permanece alpha*sqrt(e) em runtime, sem literal beta ou cálculo nesta unidade. O acesso default ao original da linha alpha foi negado; a leitura elevada posterior foi estreita, somente hash/linha, sem execução ou importação.

Nenhum centro, tabela CAMB, solver, controle, hipótese real, veredito, memória compartilhada, download ou modelo remoto foi executado/alterado. A estrutura resolve a lacuna de labels/redshifts/origem de alpha; não certifica a precisão do fundo ou autoriza sua execução. O script de extração é documental e recusa sobrescrever suas saídas.
"""
    new_bytes("LAYOUT_ESTRUTURAL_3CMB_13BAO.json", encoded(layout))
    new_bytes("NOTA_LAYOUT_ESTRUTURAL.md", note.encode("utf-8"))
    outputs = [pin(OUT / "LAYOUT_ESTRUTURAL_3CMB_13BAO.json"),
               pin(OUT / "NOTA_LAYOUT_ESTRUTURAL.md"), pin(Path(__file__).resolve())]
    manifest = {"schema": "STRUCTURAL_LAYOUT_DELIVERY_V1",
                "identity": layout["identity"], "status": layout["status"],
                "files": outputs, "sources": source_pins, "components": 16,
                "observed_centres_projected": False, "scientific_execution": False}
    new_bytes("MANIFESTO_LAYOUT_ESTRUTURAL.json", encoded(manifest))
    print(json.dumps({"files": outputs + [pin(OUT / "MANIFESTO_LAYOUT_ESTRUTURAL.json")],
                      "components": 16, "central_column_extracted": False}))


if __name__ == "__main__":
    run()
