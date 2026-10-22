"""Emit the F5.3 documentary link from the original bytes, without running science."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile


OUT = Path(__file__).resolve().parent
SOURCES = {
    "adendo004": Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_019_ADENDO_004_correcoes_do_critico.md"),
    "nivel2_frozen_worker": Path(r"C:\IALD\Artigo\teste_acustico_beta_tgl_v1\12_nivel2_frozen_e_verossimilhanca.py"),
    "nivel2_result_canonical": Path(r"C:\IALD\Artigo\teste_acustico_beta_tgl_v1\13_nivel2_resultado.json"),
    "nivel2_chain_canonical": Path(r"C:\IALD\Artigo\teste_acustico_beta_tgl_v1\13_nivel2_chains.h5"),
    "nivel2_analysis": Path(r"C:\IALD\Artigo\teste_acustico_beta_tgl_v1\14_ANALISE_NIVEL2_FECHADO.md"),
    "nivel2_result_nos_continuation": Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\nivel2_mcmc\13_nivel2_resultado.json"),
    "so_s4_prereg": Path(r"C:\IALD\Artigo\MCMC_V2_RAZAO\22_prereg_SO_S4.json"),
    "fisher_verdict": Path(r"C:\IALD\Artigo\MCMC_V2_RAZAO\VEREDITO_DO_PLANEJAMENTO.md"),
    "fisher_power_map": Path(r"C:\IALD\Artigo\MCMC_V2_RAZAO\MAPA_DE_PODER.md"),
    "fase8_v1_json": Path(r"C:\IALD\Bancada_Um\investigacao\preregistro_fase8_primordial\PREREGISTRO_FASE8_UNIVERSO_PRIMORDIAL_V1.json"),
    "fase8_v1_md": Path(r"C:\IALD\Bancada_Um\investigacao\preregistro_fase8_primordial\PREREGISTRO_FASE8_UNIVERSO_PRIMORDIAL_V1.md"),
    "fase8_hashes": Path(r"C:\IALD\Bancada_Um\investigacao\preregistro_fase8_primordial\V1_FASE8_HASHES.json"),
    "bancada_neff": Path(r"C:\IALD\Bancada_Um\bancada\neff_canal.py"),
    "cosmology_audit": Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\TETELESTAI\BANCADA_OFICIAL\COSMOLOGY_CANONICAL_ROUTE_AUDIT.md"),
    "um_py": Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"),
}


def pin(path: Path) -> dict[str, object]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
            size += len(block)
    return {"path": str(path), "bytes": size, "sha256": digest.hexdigest()}


def atomic_new(path: Path, data: bytes) -> None:
    if path.exists():
        raise RuntimeError(f"Refusing to overwrite existing artifact: {path}")
    with NamedTemporaryFile(dir=path.parent, prefix=path.name + ".tmp_", delete=False) as temp:
        temp.write(data)
        temp.flush()
        os.fsync(temp.fileno())
        temporary = Path(temp.name)
    if temporary.stat().st_size != len(data):
        temporary.unlink(missing_ok=True)
        raise RuntimeError(f"Short write: {path}")
    os.replace(temporary, path)
    if path.read_bytes() != data:
        raise RuntimeError(f"Verification failed: {path}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    pins = {key: pin(path) for key, path in SOURCES.items()}
    result = json.loads(SOURCES["nivel2_result_canonical"].read_text(encoding="utf-8"))
    continuation = json.loads(SOURCES["nivel2_result_nos_continuation"].read_text(encoding="utf-8"))
    prereg = json.loads(SOURCES["so_s4_prereg"].read_text(encoding="utf-8"))
    fase8 = json.loads(SOURCES["fase8_v1_json"].read_text(encoding="utf-8"))
    fase8_hashes = json.loads(SOURCES["fase8_hashes"].read_text(encoding="utf-8"))
    spec = fase8["spec"]
    forecast = prereg["frozen"]["sigma_previsto_por_experimento"]
    s = result["variantes"]["S"]
    l = result["variantes"]["L"]
    identifier = prereg["frozen"]["version"]

    assert identifier == "TGL_NIVEL2_SO_S4_V1"
    assert result["frozen_hash"] == continuation["frozen_hash"]
    assert s["veredito"] == "N2_INCAPAZ" and s["convergiu"] is True
    assert l["veredito"] == "N2_NOT_CONVERGED" and l["convergiu"] is False
    assert s["beta_vs_teoria"]["sigma_sobre_beta"] > 1
    assert l["beta_vs_teoria"]["sigma_sobre_beta"] > 1
    assert "Nivel 2 canonico" in spec["decisoes_padrao_da_gerencia"]["D11"]
    assert "CMB-S4" in spec["futuro_declarado"]["CMB_S4"]
    assert spec["canal_bancada"]["modulo_sha256"] == pins["bancada_neff"]["sha256"]
    assert fase8_hashes["arquivos"][SOURCES["fase8_v1_json"].name]["sha256"] == pins["fase8_v1_json"]["sha256"]
    assert fase8_hashes["arquivos"][SOURCES["fase8_v1_md"].name]["sha256"] == pins["fase8_v1_md"]["sha256"]

    literal_scans = {
        key: {"literal": identifier, "count": SOURCES[key].read_text(encoding="utf-8").count(identifier)}
        for key in ("fase8_v1_json", "fase8_v1_md", "um_py", "bancada_neff")
    }
    assert all(row["count"] == 0 for row in literal_scans.values())
    manifest = {
        "unit": "F5.3",
        "status": "DOCUMENTARY_LINK_ONLY__UNIT_REMAINS_BLOQUEADA",
        "no_new_scientific_run": True,
        "originals_modified": False,
        "new_data_opened": False,
        "runtime_wiring_installed": False,
        "frozen_prereg_modified": False,
        "gate_changed": False,
        "source_pins": pins,
        "embedded_pins": {
            "nivel2_frozen_hash": result["frozen_hash"],
            "so_s4_frozen_hash": prereg["FROZEN_HASH"],
            "fase8_spec_sha256": fase8["spec_sha256"],
        },
        "canonical_vs_continuation": {
            "canonical_source": str(SOURCES["nivel2_result_canonical"]),
            "continuation_source": str(SOURCES["nivel2_result_nos_continuation"]),
            "canonical_and_continuation_files_differ": pins["nivel2_result_canonical"]["sha256"] != pins["nivel2_result_nos_continuation"]["sha256"],
            "canonical_S_sigma_over_beta": s["beta_vs_teoria"]["sigma_sobre_beta"],
            "canonical_L_sigma_over_beta": l["beta_vs_teoria"]["sigma_sobre_beta"],
        },
        "forecast_ratios_sigma_over_beta": {
            "Planck_plus_ACT_optimistic": forecast["Planck_mais_ACT"]["otimista"]["sigma_sobre_beta"],
            "SO_like": forecast["SO_like"]["sigma_sobre_beta"],
            "S4_like_historical": forecast["S4_like"]["sigma_sobre_beta"],
        },
        "literal_scans": literal_scans,
        "fase8_existing_pointers": [
            "/spec/decisoes_padrao_da_gerencia/D11",
            "/spec/mapas/A_N2",
            "/spec/canal_bancada",
            "/spec/futuro_declarado/CMB_S4",
        ],
        "map_routes_reused": ["cmb.nivel2_mcmc", "cmb.fisher_gates_e_prereg_so_s4_14ago"],
    }
    manifest_path = OUT / "VINCULO_DOCUMENTAL_SO_S4.json"
    atomic_new(manifest_path, (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))

    rows = "\n".join(
        f"| {key} | `{value['path']}` | {value['bytes']} | `{value['sha256']}` |"
        for key, value in pins.items()
    )
    note = f"""# F5.3 — fiação documental do Nível 2 e errata ao lado do ramo CMB-S4

**Estatuto:** `[REAL — leitura de bytes e dos termos documentais]`; sem rodada científica nova. A unidade permanece `BLOQUEADA`. Este arquivo liga fontes existentes por caminho e SHA-256; não altera o pré-registro congelado, o V1 da Fase 8, a Bancada, o `um.py` ou o gate.

## O que o Nós Vivo e o mapa já tinham

O Nós Vivo lista a rota `cmb.nivel2_mcmc`, que registra o CAMB com os fechamentos S e L, e `core.nivel2_rite` com `all_verified=False`. O mapa já contém `cmb.nivel2_mcmc` (`EXAMINADA`) e `cmb.fisher_gates_e_prereg_so_s4_14ago` (`EXAMINADA`). A auditoria canônica de 28/09 distingue o Nível 2 S/L do solver V3 e deixa a escolha do fechamento perturbativo aberta. Nenhum desses elementos foi reexecutado aqui.

## Ligações que o pacote fixa

| Origem existente | Destino existente | Relação comprovada | Limite |
|---|---|---|---|
| `TGL_NIVEL2_V1` (pin interno `{result['frozen_hash']}`) e resultado canônico de agosto | Fase 8 V1, `/spec/decisoes_padrao_da_gerencia/D11` e `/spec/mapas/A_N2` | O V1 já identifica o frozen original como canônico, a cópia do Nós como continuação e o Nível 2 S como diagnóstico. | O resultado canônico e a continuação do Nós têm SHA-256 de arquivo diferentes; não transportar seus números como se fossem a mesma rodada. |
| `TGL_NIVEL2_SO_S4_V1` (pin interno `{prereg['FROZEN_HASH']}`; arquivo `so_s4_prereg` na tabela abaixo) | Fase 8 V1, `/spec/futuro_declarado/CMB_S4`, e Bancada `bancada/neff_canal.py` | Este pacote dá ao pré-registro de 14/08 uma remissão direta e versionada à Fase 8 e ao canal N_eff já pinado nela. | O identificador literal aparece **zero** vezes no JSON/MD do V1, no `um.py` e no módulo da Bancada. A fiação é documental aqui; nenhum consumidor runtime do pré-registro foi instalado. |
| Pré-registro SO/S4 e gates de Fisher | Rota `cmb.fisher_gates_e_prereg_so_s4_14ago` | O arquivo congelado prevê σ/β = {forecast['SO_like']['sigma_sobre_beta']:.2f} para SO-like e {forecast['S4_like']['sigma_sobre_beta']:.2f} para S4-like; Planck+ACT otimista fica em {forecast['Planck_mais_ACT']['otimista']['sigma_sobre_beta']:.2f}. | Projeções *like* não são vereditos de observação nem garantias de poder futuro. |

O resultado **canônico** de agosto mede S convergente, `N2_INCAPAZ`, σ/β = {s['beta_vs_teoria']['sigma_sobre_beta']:.3f}; L registra `N2_NOT_CONVERGED`, σ/β = {l['beta_vs_teoria']['sigma_sobre_beta']:.3f}. A análise de 14/08 manda não estender a cadeia L: ambas as razões excedem 1, mas o veredito formal de L continua `N2_NOT_CONVERGED`. A degenerescência radiativa `N_eff ↔ H₀` é a causa indicada. `[OPEN]` A escolha/derivação do fechamento perturbativo S × L × fluido total V3 continua teórica; este índice não a decide.

## Errata histórica ao lado — CMB-S4

Ao lado da frase de 14/08 `ESPERAR_SO_OU_S4`: **o ramo S4-like permanece no frozen como cenário de poder histórico**, σ/β = {forecast['S4_like']['sigma_sobre_beta']:.2f}; não funciona como calendário ativo de obtenção de dados. O ADENDO 004 da gerência e a própria Fase 8 V1 (`/spec/futuro_declarado/CMB_S4`) registram o encerramento CMB-S4 como `[DECLARADO]`. A rota SO-like permanece expectativa condicionada à disponibilidade real do dado e às condições do pré-registro. O frozen `TGL_NIVEL2_SO_S4_V1` não foi reescrito.

## Fontes conferidas em bytes

| Papel | Caminho absoluto | Bytes | SHA-256 |
|---|---|---:|---|
{rows}

O pin interno do frozen SO/S4 (`{prereg['FROZEN_HASH']}`) é distinto do SHA-256 do próprio arquivo; ambos constam no manifesto `VINCULO_DOCUMENTAL_SO_S4.json`. O V1 da Fase 8 mantém seu pin de especificação `{fase8['spec_sha256']}`. O código `ALPHA_FINE_CODATA_2018 × √e` permanece a forma de β em runtime. Nenhum dado observacional novo foi aberto; a cadeia MCMC foi lida apenas para SHA-256, sem análise ou execução. Não houve CAMB, teste de natureza, instalação ou publicação.
"""
    note_path = OUT / "NOTA_FIACAO_E_ERRATA_S4.md"
    atomic_new(note_path, note.encode("utf-8"))
    print(json.dumps({"manifest": pin(manifest_path), "note": pin(note_path)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
