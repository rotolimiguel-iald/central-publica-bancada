"""Build the F7.2 source-pinned channel table without running scientific scripts."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCES = HERE / "fontes_primarias"
OUT = HERE / "TABELA_DE_PODER_POR_CANAL.md"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_verified_manifest(name: str) -> dict[str, dict]:
    manifest = json.loads((SOURCES / name).read_text(encoding="utf-8"))
    result = {}
    for entry in manifest["sources"]:
        path = Path(entry["file"])
        if path.parent.resolve() != SOURCES.resolve():
            raise ValueError(f"Unexpected source directory: {path}")
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != entry["sha256"]:
            raise ValueError(f"SHA mismatch: {path}")
        if path.suffix.lower() == ".pdf" and not raw.startswith(b"%PDF-"):
            raise ValueError(f"Not a PDF: {path}")
        result[path.name] = entry
    return result


neutrino = load_verified_manifest("SOURCE_CUSTODY.json")
matter = load_verified_manifest("MATTER_SOURCE_CUSTODY.json")
validation = HERE / "MATTER_SOURCE_CUSTODY_VALIDATION.json"
if not validation.is_file():
    raise FileNotFoundError(validation)
validation_raw = validation.read_bytes()
if not validation_raw.strip():
    raise ValueError("Empty matter-source validation")
validation_data = json.loads(validation_raw)
if not isinstance(validation_data, dict):
    raise ValueError("Invalid matter-source validation")
for name in ("Kovachy_2015_Nature_abstract.html", "Fein_2019_NaturePhysics_abstract.html"):
    raw = (SOURCES / name).read_bytes()
    if b"Client Challenge" not in raw or b"nature16155" in raw or b"s41567-019-0663-9" in raw:
        raise ValueError(f"Unexpected HTML status: {name}")


def link(entry: dict, label: str) -> str:
    return f"[{label}]({entry['url']}) (SHA-256 `{entry['sha256']}`)"


fogli = neutrino["Fogli_2007_arxiv_0704.2568.pdf"]
deromeri = neutrino["DeRomeri_2023_arxiv_2306.14699.pdf"]
orca = neutrino["ORCA6_2025_arxiv_2410.01388.pdf"]
icecube = neutrino["IceCube_2024_arxiv_2308.00105.pdf"]
coloma = neutrino["Coloma_2018_arxiv_1803.04438.pdf"]
chapman = matter["Chapman_1995_author.pdf"]
hack = matter["Hackermueller_2004_arxiv_quant-ph_0402146.pdf"]
pedalino = matter["Pedalino_2026_published_author.pdf"]
pedalino_preprint = matter["Pedalino_2025_preprint_arxiv_2507.21211v1.pdf"]

text = f"""# F7.2 — tabela de poder por canal, com custódia das fontes

**Estado:** [REAL — leitura documental, hashes conferidos dos bytes locais em 07/10/2026]. Os valores experimentais abaixo são [KNOWN] dos modelos e aparelhos de cada artigo. A associação com uma cota da TGL está [OPEN]; em todas as linhas, `τ★_limite = null`, `SEM_LIMITE_TGL`. Nenhum dado bruto foi aberto ou ajustado, e nenhum gate mudou.

O Nós Vivo (`consultar.py --unidade F7.2`) já localizava os scripts de junho: assinatura `n = −2` permitida, `NO DETECTION` e expoente não medido. A v369 já tratou **relógios** (`clock_test_protocol_v369`/`clock_test_result_v369`); o ADENDO 004 registra [DECLARADO] a projeção condicional de 5σ: GHZ `N ≳ 1,69 × 10⁶` ou `ℏω ≳ 3,0 MeV` (valores aproximados; limiares exatos da saída v369: 1.693.625,635… e 3,006430… MeV), e não mede interferometria de matéria. Esta F7.2 reaproveita ambos os registros e liga um canal de consulta à Bancada. Ver [rebase local](REAPROVEITAMENTO_E_ERRATA.md) e [parecer cético confrontado](PARECER_KIMI_CONFERIDO.md).

## Neutrinos

| Canal/modelo | Resultado publicado | Poder que o artigo oferece | Poder TGL hoje | Fonte primária sob custódia |
|---|---|---|---|---|
| Fogli 2007, solar+KamLAND, `n = −2`, `E₀ = 1 GeV` | `γ₀ < 8,1 × 10⁻²⁹ GeV`, 95% CL | Limita o dissipador solar do artigo; **não** o dephasing puro da TGL. | Sem projeção de operador; a extrapolação histórica para `τ★` é inválida. | {link(fogli, 'Eq. 3 e Tabela I')} |
| KamLAND, De Romeri 2023 modelo A, `n = −2`, `E₀ = 1 GeV` | `Γ₀ < 7,8 × 10⁻²⁷ GeV`, 90% CL | Limite atual do cenário de três taxas iguais. | Curva de taxas da TGL em matéria ainda não modelada. | {link(deromeri, 'Tabela 3 e §V')} |
| KamLAND, De Romeri 2023 modelo E, `n = −2`, `E₀ = 1 GeV` | `Γ₂₁ < 7,9 × 10⁻²⁷ GeV`, 90% CL | Limite atual do cenário só `Γ₂₁`; não é projeção JUNO/DUNE. | Falta canal físico e `Kfac`. | {link(deromeri, 'Tabela 3')} |
| ORCA6, `n = −2`, `E₀ = 1 GeV` | `Γ₂₁` NO/IO `< 2,8/4,6 × 10⁻²¹ GeV`; `Γ₃₁` NO/IO `< 8,4/2,2 × 10⁻²¹ GeV`, 90% CL | Quatro limites perfilados, dependentes do ordenamento e da relação de taxas assumida. | Precisa projetar o dissipador TGL na família ORCA e sua likelihood. | {link(orca, 'Tabela 3 e Eq. 10')} |
| IceCube 2024, *state selection*, `n = 0`, `E₀ = 1 TeV` | `Γ₀ ≤ 1,17 × 10⁻¹⁵ eV`, 90% CL | Limita outra classe; **não** fornece linha `n = −2`. | Sem teste direto da assinatura proposta. | {link(icecube, 'Tabela 1')} |

{link(coloma, 'Coloma et al. 2018, nota 6')} explicita a incompatibilidade entre a cota solar de Fogli e o dephasing puro; {link(deromeri, 'De Romeri 2023, §§IV–V')} explica por que o canal solar promediado não tem aquela sensibilidade. O `χ²_min(n) = 0` dos scripts de junho decorre de incluir `γ₀ = 0` na grade; não mede `n` nem poder de discriminação. O parecer do Kimi é [DECLARADO] até o confronto local registrado no documento acima.

## Interferometria de matéria

| Canal | Observável publicado e alcance medido | Poder TGL hoje | Fonte primária sob custódia |
|---|---|---|---|
| Átomos, Chapman 1995 | O contraste cai a zero em separação de trajetórias próxima a meio comprimento de onda do fóton espalhado; seleção angular recuperou mais de 60% do contraste perdido (p. 3). A porcentagem é resultado experimental dos autores, não cota de dephasing gravitacional. | Falta `ω` efetivo, mapa `Γ → contraste` e separação do espalhamento de fótons. | {link(chapman, 'PDF do autor, p. 3')} |
| Moléculas C₇₀, Hackermüller 2004 | Visibilidades medidas 47/29/7/0% para aquecimento 0/3/6/10,5 W, respectivamente, a 190 m/s (p. 2, Fig. 2). | Falta separar emissão térmica e ruído da taxa TGL. | {link(hack, 'arXiv, p. 2 e Fig. 2')} |
| Nanopartículas, Pedalino 2026 | O experimento inclui objetos com mais de 7.000 átomos; as franjas cobrem 143–197 kDa. Duas corridas com massa média 172 kDa tiveram visibilidades ajustadas `V = 0,10 ± 0,01` e `0,08 ± 0,01` (pp. 1–3). O artigo atribui uma limitação de visibilidade à fotodepleção. | Falta modelo TGL para a geometria, a visibilidade e os fundos. | {link(pedalino, 'PDF publicado dos autores, pp. 1–2')} |

{link(pedalino_preprint, 'Preprint de Pedalino 2025')} foi preservado como versão anterior; a linha usa os números da versão publicada. Kovachy 2015 e Fein 2019 aparecem como pistas bibliográficas, sem hash de artigo local: as duas respostas HTML recebidas do editor são páginas `Client Challenge` byte-idênticas, **não resumos científicos**. O [recibo de validação](MATTER_SOURCE_CUSTODY_VALIDATION.json) documenta essa recusa (SHA-256 `{digest(validation)}`). Não há dados brutos nem likelihood sob custódia para esses interferômetros.

## Próxima medida que poderia dar poder

Neutrinos: especificar `Lᵢ`/operador TGL em matéria, evolução e taxas `Γ₂₁/Γ₃₁` com ordenamento e `Kfac`; confrontar likelihood compatível e pré-registrada. Matéria: definir `ω` físico por estado/caminho, `Γ` e a função de visibilidade com ruídos instrumentais, pré-registrar por hash a função de veredito e estimar poder antes de compor o resultado. Até isso existir, nenhuma cota publicada acima se converte em `τ★`; `NOT_FALSIFIED` não é `CONFIRMED`.
"""

raw = text.encode("utf-8")
tmp = OUT.with_name(OUT.name + ".tmp")
with tmp.open("wb") as stream:
    stream.write(raw)
    stream.flush()
    os.fsync(stream.fileno())
if tmp.stat().st_size != len(raw):
    raise OSError("Incomplete temporary table")
if OUT.exists():
    raise FileExistsError(f"Refusing to overwrite {OUT}; back up bytes and review first")
os.replace(tmp, OUT)
print(json.dumps({"file": str(OUT), "sha256": digest(OUT), "bytes": len(raw)}, ensure_ascii=False))
