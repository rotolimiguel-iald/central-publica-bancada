"""Read-only primary-source inventory for claimed unit F8.2.NU2 (event 618)."""
from pathlib import Path
import datetime
import hashlib
import json

ROOT = Path(__file__).resolve().parent
KERNEL = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt")
F72 = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F7.2")
SCRIPTS = F72 / "V3_STAGING/fontes_externas/F7.2/scripts"
SOURCES = [
    (KERNEL / "TheCouplingRunsBoundedBelow.lean", [(5, 27), (33, 37), (65, 69), (96, 102)], "KERNEL source; no new compilation; physical identification explicitly INPUT/ONTO"),
    (KERNEL / "TheWholeIsOne.lean", [(55, 62)], "Contract restricts physical coupling to beta<1"),
    (Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\A Ponte Einstein Cartan Miguel.tex"), [(1301, 1306), (1328, 1341), (1367, 1371), (720, 731), (818, 827)], "Canonical article; dephasing coefficient fixed at Thomson; historical empirical claims not revalidated"),
    (Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"), [(165419, 165421), (166219, 166232), (194714, 194717), (194734, 194747), (194754, 194764)], "Read bytes only; never imported/executed; no claim of current compilation or seal"),
    (SCRIPTS / "tgl_neutrino_decoherence.py", [(5, 28), (40, 58)], "Historical script; rate uses fixed BETA and Kfac input, revised by F7.2"),
    (SCRIPTS / "tgl_decoherence_contour.py", [(5, 19), (66, 75)], "Historical script; tau is input; no current bound inferred"),
    (F72 / "PARECER_KIMI_CONFERIDO.md", [(5, 31), (33, 43)], "Local audited reconciliation; explains bounds/model incompatibility and matter bridge OPEN"),
    (F72 / "EVIDENCIA_R2_R3_V369_ORDENS_20261008_V2.md", [(15, 49)], "Conditional comparisons and P1/P3/MODULAR_LAB_BRIDGE_OPEN"),
    (Path(r"C:\IALD\Central de Patentes\memory\TGL_ATLAS.md"), [(35123, 35127)], "Memory pointer only; checked against primary article and runtime"),
    (KERNEL / "TheDensityIsTransport.lean", [(12, 37)], "Structural theorem; identification with neutrino ONTO and physical observable OPEN"),
    (KERNEL / "TheStation.lean", [(32, 41), (166, 177)], "Finite matrix theorem; no stellar rate/matching equation"),
    (Path(r"C:\IALD\Artigo\Tratado\secao_03_particulas.tex"), [(406, 435), (452, 461)], "Historical phenomenology; no weak-rate derivation; geodesic RHS=0 does not erase connection on LHS"),
    (Path(r"C:\IALD\Artigo\Tratado\secao_01_fundamentos.tex"), [(234, 234), (266, 266), (578, 584)], "Historical scalar/Ricci-FF operators; not a weak interaction matching calculation"),
    (Path(r"C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\project_fisica\ERRATA_20260919_sinal_do_acoplamento_nao_minimo.md"), [(23, 29)], "Signed erratum selects conformal xi=1/6, explicitly not beta"),
    (Path(r"C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\project_fisica\O_Custo_Geometrico_do_Zero_Absoluto_Haja_Luz.tex.txt"), [(3115, 3122), (3307, 3307)], "Snapshot/history; identifies K as Kretschmann, not modular K; empirical claims superseded by F7.2"),
]


def main():
    out = ROOT / "INVENTARIO_FONTES_NU2_20261009.json"
    if out.exists():
        raise FileExistsError(out)
    records = []
    for p, ranges, status in SOURCES:
        raw = p.read_bytes()
        lines = raw.decode("utf-8-sig").splitlines()
        excerpts = []
        for start, end in ranges:
            if not (1 <= start <= end <= len(lines)):
                raise ValueError((p, start, end, len(lines)))
            excerpts.append({"first_line": start, "last_line": end,
                             "text": "\n".join(f"{i}: {lines[i-1]}" for i in range(start, end+1))})
        records.append({"path": str(p), "sha256": hashlib.sha256(raw).hexdigest(),
                        "size_bytes": len(raw), "line_count": len(lines),
                        "status": status, "excerpts": excerpts})
    payload = {"unit": "F8.2.NU2", "claim_event": 618,
               "created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
               "author": "codex-gerente-tgl / nu2_theory_sources",
               "originals_modified": False, "original_program_executed_or_imported": False,
               "observed_dataset_opened": False,
               "search_scope": "Atlas and live index pointers, Nos Vivo F7.2/F8.2, named v388 and related kernel files, TGLExt lexical search, six F7.2 June script copies, two Tratado chapters, canonical Ponte and Custo snapshot. This is not a proof of global absence.",
               "sources": records}
    with out.open("x", encoding="utf-8", newline="\n") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")
    b = out.read_bytes()
    print(json.dumps({"path": str(out), "sha256": hashlib.sha256(b).hexdigest(),
                      "source_count": len(records)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
