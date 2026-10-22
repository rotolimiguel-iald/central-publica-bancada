"""Append the measured V3 delivery to every owned memory surface."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from record_universe_delivery import append, CANON, CENTRAL, HERE


def main():
    import cosmology_runtime as runtime
    validation = HERE / "state" / ("validation_cosmology_v3_" + runtime.ENGINE_GENERATION[:16] + ".json")
    suite = HERE / "state" / "cosmology_final_tests.json"
    run = json.loads(validation.read_text(encoding="utf-8"))
    tests = json.loads(suite.read_text(encoding="utf-8"))
    assert run["gw_unchanged"] and tests["successful"] and tests["skipped"] == 0
    names = ["cosmology_runtime.py", "cosmology_v3_bridge.py", "workers/cosmology_v3_worker.py",
             "scientific_models/tgl_camb_worker_v3.py", "cosmology_scenarios.py", "cosmology_exports.py",
             "cosmology_server.py", "static/cosmos.html", "static/cosmos.js", "static/cosmos.css"]
    hashes = {}
    for name in names:
        source, target = HERE / name, CANON / name
        assert source.read_bytes() == target.read_bytes(), name
        hashes[name] = hashlib.sha256(source.read_bytes()).hexdigest()
    receipt = {"created_utc": datetime.now(timezone.utc).isoformat(), "engine_generation": runtime.ENGINE_GENERATION,
               "files": hashes, "tests": tests, "validation": str(validation),
               "validation_sha256": hashlib.sha256(validation.read_bytes()).hexdigest(),
               "gw": run["gw"], "export": run["export"],
               "ui": "CUA: fixed/zero A-B, delta plot, H0 editing, invalid input save refusal, scenario re-evaluation and server file export verified",
               "scope": "V3_CONDITIONAL_BACKGROUND_NO_NEW_SIGMA"}
    output = HERE / "state" / ("delivery_cosmology_v3_" + runtime.ENGINE_GENERATION[:16] + ".json")
    if not output.exists():
        with output.open("xb") as f:
            f.write(json.dumps(receipt, ensure_ascii=False, indent=2).encode())
    c = run["calls"]
    text = f"""## 28/09/2026 — Cosmos V3 ligado; cenários e comparação A/B

[INPUT] “prossiga, melhore, avance, aprimore”. Continuação da bancada interativa local; originais científicos preservados, sem alteração de kernel/gate.

[REAL — recuperação antes de implementar] Auditoria de leitura localizou `FundoV3` e verificou a cópia contra o literal embutido do um.py v375. Rota: fator no fluido total incluindo Λ, primeira Friedmann por primitiva, P(∞)=ρΛ, C=0, ΩΛ por E(0)=1. Não substituímos por rota setorial, S/L históricos ou face recíproca. Relatório: `{CANON / 'COSMOLOGY_CANONICAL_ROUTE_AUDIT.md'}`.

[REAL / CONDICIONAL — software] Fonte pinada reutilizada em processo WSL próprio; nunca chama CAMB, derivados, rs_integral ou o worker GW. Modelos: TGL_V3_TOTAL_FIXED_BETA, V3_TOTAL_BETA_ZERO (com radiação), CPL exploratório. β por ALPHA_FINE_CODATA_2018×√e. H₀, Ωm total e rd interativos; w0=-1 e wa=0 no V3. Partição representativa dos inputs de matéria não é estimativa física de bárions/neutrinos. rd é externo; TCMB/Neff do worker histórico. E(0), positividade, segunda Friedmann, refinamento local e controle β=0 conferidos; código não promove ramo a previsão cosmológica completa.

[REAL — interface] A/B com referência tracejada, diferença DM/DH/DV por z, controles deslizantes, β/ΩΛ/cache visíveis. Cenários SQLite append-only preservam parâmetros, resultado, fontes, geração de componentes e UTC. Cálculo refeito no servidor antes de salvar/exportar; exportação em state/exports com leitura pelo navegador. O download blob não ficou verificável no IAB e foi substituído por arquivo real no servidor. Originais de cenários permanecem; versões incompatíveis são recusadas como A e podem ser recalculadas como B. Nenhuma aceitação de resultado forjado do cliente.

[REAL — controles desta rodada] {tests['tests_run']} testes passaram, zero ignorados, incluindo WSL real e falhas de integridade. Revisões locais detectaram e corrigiram mistura visual entre gerações, contratos HTTP inconsistentes, respostas V3 incompletas/não finitas e hashes divergentes. Não são teoremas físicos novos. Geração medida: {runtime.ENGINE_GENERATION}.

[REAL — diagnóstico MANUAL, sem sigma] Nos parâmetros H₀=67,4, Ωm=0,315, rd=147,09: χ² zero={c['zero']['chi2']['value']:.12f}; fixo={c['fixed']['chi2']['value']:.12f}; Δχ² B−A={c['fixed']['chi2']['value']-c['zero']['chi2']['value']:.12f}. 13 componentes DESI DR2, covariância completa e distâncias calculadas nos z exatos. Cursor não muda χ²; rd muda a escala. Tempos de executor medidos: primeira chamada {c['zero']['elapsed_ms']:.2f} ms; β fixo {c['fixed']['elapsed_ms']:.2f} ms; cursor quente {c['cursor']['elapsed_ms']:.2f} ms. Uma rodada não é benchmark universal. Não houve fit/nuisance/simulação global; Δχ² não virou Z.

[REAL — preservação] GW continua READY {run['gw']['loaded_files']}/{run['gw']['total_files']}, {run['gw']['resident_bytes']} bytes, load_id {run['gw']['load_id']}, mesmo inventário/hashes. Reiniciado somente Cosmos, porta18766. Atalho TGL no Desktop OneDrive conferido existente. Serviço temporário de desenvolvimento será encerrado; web pública/iOS/Android não alterados, builds não aplicáveis.

[OPEN — próximo trabalho] Integrar as perturbações e precisão CMB/rd no protocolo D10, priors/nuisance e rivais explícitos, sobreposições e simulação global; também continuam a integração dos demais domínios e voz. Navegação de z/grade 3D é representação, não relógio físico TGL nem mapa observado. Esta entrega é reprodução interativa de fundo condicional, não novo resultado 5σ.

Recibo: `{CANON / 'state' / validation.name}`, SHA {hashlib.sha256(validation.read_bytes()).hexdigest()}. Guia: `{CANON / 'COSMOLOGIA_V3_CENARIOS.md'}`. Nenhum original, patente ou acervo jurídico alterado.
"""
    marker = "TGL_COSMOLOGY_V3_SCENARIOS_" + runtime.ENGINE_GENERATION[:16]
    for root in (HERE, CANON):
        for name in ("MEMORIA_CENTRAL.md", "REGISTRO_DAS_CONVERSAS.md"):
            append(root / name, text, marker)
        append(root / "PLANO_UNIVERSO_RESIDENTE.md", text, marker + "_PLAN")
    for name in ("TGL_ATLAS.md", "TGL_INDICE_VIVO.md", "TGL_CORE_MEMORY.md"):
        append(CENTRAL / "memory" / name, text, marker)
    print(str(output))


if __name__ == "__main__":
    main()
