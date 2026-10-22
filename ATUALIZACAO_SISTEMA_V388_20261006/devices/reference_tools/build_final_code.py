# -*- coding: utf-8 -*-
"""AMALGAMADOR — o codigo-fonte FINALIZADO de cada patente (forma=conteudo, o destino da regua).

Cada patente ja tem um runner (one_<slug>.py) que demonstra + sela + renderiza, mas depende de
_<slug>_core/, prototype_src/ e do piloto compartilhado (CENTRAL/Patentes/Skygrid/SkyGrid_Piloto/
skygrid_sim, de onde o runner reconstroi o nucleo destilado tgl_core / beta). Este amalgamador
CONSOLIDA tudo num UNICO arquivo auto-contido `<SLUG>_FINAL.py` (bundle auto-extraivel: embute
toda a arvore de dependencia — em layout CENTRAL-relativo — em base64; extrai para um temp em
runtime e roda o runner la', recriando o layout real). Robusto a subprocess/temp/import dinamico.
Expoe `demonstrate()` (importavel => vira modulo do SkyGrid), roda standalone, e carrega um
MANIFESTO com SHA-256 por arquivo + hash combinado do bundle. Integridade verificada em runtime.

REGUA: nunca empacota confidenciais (iald_stack_v7, iald_psion_state, iald_web_server*,
token_huggin*). Nao altera os originais do INPI. beta nunca literal (herdado do runner).

Uso:  python tools/build_final_code.py [<ID_pasta> ...]
"""
import sys, io, os, re, json, zipfile, base64, hashlib
from pathlib import Path
from datetime import datetime, timezone

CENTRAL = Path(__file__).resolve().parent.parent
PATENTS = CENTRAL / "patents"
PILOTO_REL = Path("Patentes") / "Skygrid" / "SkyGrid_Piloto"
CONFIDENTIAL = ("iald_stack_v7", "iald_psion_state", "iald_web_server", "token_huggin")
SKIP_DIRS = ("__pycache__", "results", "seals", "renders", "notes", "visuals", ".git")
SRC_EXT = (".py", ".json", ".txt", ".csv", ".yaml", ".yml", ".npy", ".md")
MAX_FILE = 3_000_000


def _confidential(name):
    n = name.lower(); return any(c in n for c in CONFIDENTIAL)
def _sha(b): return hashlib.sha256(b).hexdigest()
def find_runner(pdir):
    c = list((pdir / "runner").glob("one_*.py")); return c[0] if c else None


def _walk(base: Path, central_prefix: Path, out: dict):
    """Adiciona arquivos-fonte sob `base` ao dict out {central_rel_posix: abs_path}."""
    if not base.exists():
        return
    for f in sorted(base.rglob("*")):
        if not f.is_file():
            continue
        rel = f.relative_to(base)
        if any(p in SKIP_DIRS for p in rel.parts) or _confidential(f.name):
            continue
        if f.name.endswith("_FINAL.py") or f.name.endswith("_FINAL.manifest.json"):
            continue                                       # nao embutir o proprio bundle
        if f.suffix.lower() not in SRC_EXT or f.stat().st_size > MAX_FILE:
            continue
        out[(central_prefix / rel).as_posix()] = f


def collect(pdir: Path, runner: Path):
    """Fontes CENTRAL-relativas: a patente + os subdirs do piloto que o runner referencia."""
    files = {}
    prel = pdir.relative_to(CENTRAL)                       # patents/<ID>
    _walk(pdir, prel, files)                               # raiz da patente (render3d.json, components.json, ...)
    _walk(pdir / "runner", prel / "runner", files)
    _walk(pdir / "prototype_src", prel / "prototype_src", files)
    # bundla os subdirs do piloto cujo NOME aparece citado no runner (robusto a PILOTO/"lit" e a
    # listas tipo CORE_DIRS=[...] via PILOTO/d). skygrid_sim sempre (o beta/tgl_core vem dele).
    txt = runner.read_text(encoding="utf-8", errors="ignore")
    piloto = CENTRAL / PILOTO_REL
    needed = {"skygrid_sim"}
    if piloto.exists():
        for sub in piloto.iterdir():
            if sub.is_dir() and f'"{sub.name}"' in txt:
                needed.add(sub.name)
    for sub in sorted(needed):
        _walk(piloto / sub, PILOTO_REL / sub, files)
    # 01/10/2026 (custodia v379): a FORMULA COMPLETA, camada comum dos 16 dispositivos, vai em todo bundle
    _walk(PATENTS / "_formula_completa", Path("patents") / "_formula_completa", files)
    return files


def build_patent(pdir: Path):
    pid = pdir.name.split("_", 1)[0]
    slug = pdir.name.split("_", 1)[1].lower() if "_" in pdir.name else pdir.name.lower()
    runner = find_runner(pdir)
    if not runner:
        return f"{pdir.name[:28]:28} SEM runner"
    files = collect(pdir, runner)
    buf, manifest = io.BytesIO(), []
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for rel, abs_ in sorted(files.items()):
            data = abs_.read_bytes()
            z.writestr(rel, data)
            manifest.append({"path": rel, "sha256": _sha(data), "bytes": len(data)})
    bundle = buf.getvalue()
    combined = _sha(bundle)
    runner_rel = runner.relative_to(CENTRAL).as_posix()    # patents/<ID>/runner/one_<slug>.py
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    final = _TEMPLATE.format(
        pid=pid, slug=slug, ts=ts, runner_rel=runner_rel, combined=combined,
        n=len(manifest), manifest=json.dumps(manifest, ensure_ascii=False),
        b64=base64.b64encode(bundle).decode("ascii"))
    for _n in (f"{slug}_FINAL.py", f"{slug}_FINAL.manifest.json"):     # backup de BYTES antes de reescrever (regra 22/08)
        if (pdir / _n).is_file():
            (pdir / (_n + ".bak_" + ts.replace(":", "").replace("-", ""))).write_bytes((pdir / _n).read_bytes())
    (pdir / f"{slug}_FINAL.py").write_text(final, encoding="utf-8")
    (pdir / f"{slug}_FINAL.manifest.json").write_text(json.dumps(
        {"patent_id": pid, "slug": slug, "generated_utc": ts, "runner": runner_rel,
         "combined_sha256": combined, "n_files": len(manifest),
         "final_bytes": len(final.encode("utf-8")), "files": manifest},
        ensure_ascii=False, indent=1), encoding="utf-8")
    return f"{pdir.name[:28]:28} OK -> {slug}_FINAL.py ({len(manifest)} fontes, {len(final)//1024} KB, {combined[:12]})"


_TEMPLATE = r'''# -*- coding: utf-8 -*-
"""{slug}_FINAL — CODIGO-FONTE FINALIZADO da patente {pid} (forma=conteudo).

UM unico arquivo auto-contido que demonstra a patente por completo. Bundle auto-extraivel: toda a
arvore computacional (runner + _core + prototype_src + piloto skygrid_sim) esta' embutida em
base64 (layout CENTRAL-relativo). `demonstrate()` verifica a integridade (SHA-256 combinado),
extrai para um temp e roda a demonstracao, devolvendo o selo. Importavel (entra no compilador
SkyGrid como modulo). Gerado por tools/build_final_code.py em {ts}. NAO editar (regenerar).
Integridade: combined_sha256 = {combined}  ({n} fontes). beta nunca literal (herdado do runner).
"""
import sys, io, os, json, base64, zipfile, hashlib, subprocess, tempfile, glob, shutil
from pathlib import Path

PATENT_ID = "{pid}"
SLUG = "{slug}"
RUNNER_REL = r"{runner_rel}"
COMBINED_SHA256 = "{combined}"
MANIFEST = {manifest}
_B64 = "{b64}"

def _bundle(): return base64.b64decode(_B64.encode("ascii"))

def verify_integrity():
    b = _bundle(); combined = hashlib.sha256(b).hexdigest(); files_ok = True
    with zipfile.ZipFile(io.BytesIO(b)) as z:
        names = set(z.namelist())
        for e in MANIFEST:
            got = hashlib.sha256(z.read(e["path"])).hexdigest() if e["path"] in names else None
            files_ok = files_ok and (got == e["sha256"])
    return {{"combined_ok": combined == COMBINED_SHA256, "combined_sha256": combined,
            "expected": COMBINED_SHA256, "files_ok": files_ok, "n_files": len(MANIFEST)}}

def demonstrate(workdir=None, verify=True, timeout=1200):
    """Extrai o bundle (layout CENTRAL) e roda a demonstracao completa. Retorna o selo (dict)."""
    integ = verify_integrity()
    if verify and not (integ["combined_ok"] and integ["files_ok"]):
        raise RuntimeError(f"INTEGRIDADE FALHOU ({{PATENT_ID}}): {{integ}}")
    root = Path(workdir) if workdir else Path(tempfile.mkdtemp(prefix=f"final_{{SLUG}}_"))
    made = workdir is None
    try:
        with zipfile.ZipFile(io.BytesIO(_bundle())) as z:
            z.extractall(root)                          # root = CENTRAL: patents/<ID>/... + Patentes/...
        runner = root / RUNNER_REL
        proc = subprocess.run([sys.executable, str(runner)], cwd=str(runner.parent),
                              capture_output=True, text=True, timeout=timeout,
                              env={{**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}})
        res = sorted(glob.glob(str(runner.parent.parent / "results" / "**" / "*.json"), recursive=True))
        seal = None
        if res:
            try: seal = json.loads(Path(res[-1]).read_text(encoding="utf-8"))
            except Exception: seal = None
        return {{"patent_id": PATENT_ID, "slug": SLUG, "integrity": integ,
                "returncode": proc.returncode, "seal": seal,
                "stdout_tail": proc.stdout[-1500:], "stderr_tail": proc.stderr[-800:]}}
    finally:
        if made: shutil.rmtree(root, ignore_errors=True)

def main():
    print(f"{{SLUG}}_FINAL — patente {{PATENT_ID}} (codigo-fonte finalizado, forma=conteudo)")
    integ = verify_integrity()
    print(f"  integridade: combined_ok={{integ['combined_ok']}} files_ok={{integ['files_ok']}} ({{integ['n_files']}} fontes)")
    print(f"  combined_sha256 = {{COMBINED_SHA256}}")
    r = demonstrate()
    s = r.get("seal") or {{}}
    v = s.get("verdict") or s.get("max_verdict") or "(sem selo)"
    print(f"  demonstracao: returncode={{r['returncode']}} verdict={{v}}")
    if r["returncode"] != 0: print("  stderr:", r["stderr_tail"][-400:])
    return 0 if r["returncode"] == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
'''


def main():
    targets = sys.argv[1:] or [p.name for p in sorted(PATENTS.iterdir()) if p.is_dir() and not p.name.startswith("_")]
    print(f"Amalgamando {len(targets)} patente(s)...\n")
    for name in targets:
        pdir = PATENTS / name
        if not pdir.is_dir():
            print(f"  {name}: nao encontrada"); continue
        try:
            print("  " + build_patent(pdir))
        except Exception as e:
            import traceback; print(f"  {name[:28]:28} ERRO: {e}"); traceback.print_exc()


if __name__ == "__main__":
    main()
