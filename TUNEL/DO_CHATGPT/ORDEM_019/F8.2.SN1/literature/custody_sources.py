"""Fetch only the seven public literature pages named in this survey.

Create-only outputs. No supernova catalogue, fit, provider, or original TGL file.
"""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import urllib.request

ROOT = Path(__file__).resolve().parent
SOURCES = [
    ("L01", "Chamel et al. (2021/2023), Electron Captures and Stability of White Dwarfs", "https://arxiv.org/html/2110.11038v1", "L01_chamel_2110_11038v1.html", "Sections 2-4; equations 6-17, 31-39. Authors' analytical results, with stated cold single-species approximations."),
    ("L02", "Martinez-Rodriguez et al. (2016), Neutronization During Carbon Simmering In Type Ia Supernova Progenitors", "https://arxiv.org/abs/1602.00673v2", "L02_martinez_1602_00673v2_abs.html", "Abstract. MESA evolution, weak reactions, neutron excess and metallicity. Full model not reproduced."),
    ("L03", "Piro and Bildsten (2008), Neutronization During Type Ia Supernova Simmering", "https://arxiv.org/abs/0710.1600", "L03_piro_0710_1600_abs.html", "Abstract. Weak reactions, carbon burned and convective Urca; compared with the later L02."),
    ("L04", "Timmes, Brown and Truran (2003), On Variations in the Peak Luminosity of Type Ia Supernovae", "https://arxiv.org/abs/astro-ph/0305114", "L04_timmes_0305114_abs.html", "Abstract. Conditional relation between electron fraction, metallicity and Ni56 yield; no universal luminosity-mass law."),
    ("L05", "Katz, Kushnir and Dong (2013), An exact integral relation between the Ni56 mass and the bolometric light curve of a type Ia supernova", "https://arxiv.org/abs/1301.6766", "L05_katz_1301_6766_abs.html", "Abstract with derivation of the time-weighted energy integral and its three assumptions."),
    ("L06", "Wygoda, Elbaz and Katz (2019), Type Ia supernovae have two physical width-luminosity relations... I. Bolometric", "https://academic.oup.com/mnras/article/484/3/3941/5289612", "L06_wygoda_stz145.html", "Sections 2.1, 2.3, 3.3 and 6: flux ratios, gamma escape time, systematics and non-unique ejecta mass."),
    ("L07", "Erler and Ramsey-Musolf (2005/2007), Weak mixing angle at low energies", "https://arxiv.org/html/hep-ph/0409169v2", "L07_erler_0409169v2.html", "Introduction equations 1-5 and RGE/matching sections: separate gauge couplings, scheme, scale and physical amplitudes."),
]

def fetch(entry):
    ident, title, url, filename, anchor = entry
    target = ROOT / filename
    if target.exists():
        raise FileExistsError(target)
    start = datetime.now(timezone.utc).isoformat()
    request = urllib.request.Request(url, headers={"User-Agent": "IALD-public-literature-survey/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            data = response.read()
            content_type = response.headers.get("Content-Type", "")
            final_url = response.url
            status = response.status
        if status != 200 or len(data) < 500 or "html" not in content_type.lower():
            raise ValueError(f"Unexpected response: {status}, {content_type}, {len(data)} bytes")
        with target.open("xb") as stream:
            stream.write(data)
        if target.read_bytes() != data:
            raise ValueError("Written bytes differ")
        return dict(id=ident, title=title, source_url=url, final_url=final_url,
                    local_file=filename, bytes=len(data), sha256=sha256(data).hexdigest(),
                    content_type=content_type, acquired_utc=start, anchor=anchor,
                    status="CUSTODIED_HTML_BYTES_NOT_FULL_PDF")
    except Exception as error:
        return dict(id=ident, title=title, source_url=url, anchor=anchor,
                    acquired_utc=start, status="WEB_CONSULTED_NO_LOCAL_CUSTODY",
                    error=f"{type(error).__name__}: {error}")

def main():
    result_path = ROOT / "SOURCE_CUSTODY.json"
    if result_path.exists():
        raise FileExistsError(result_path)
    for row in SOURCES:
        if (ROOT / row[3]).exists():
            raise FileExistsError(ROOT / row[3])
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(fetch, SOURCES))
    payload = dict(unit="F8.2.SN1", author="codex / sn_ew_literature", sources=results,
                   note="Public scientific literature only. No supernova sample opened for a verdict, no composite computed. HTML custody is not a PDF pin.")
    with result_path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(payload, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps({"sources": len(results), "custodied": sum(r["status"].startswith("CUSTODIED") for r in results), "manifest": str(result_path)}, ensure_ascii=False))

if __name__ == "__main__":
    main()
