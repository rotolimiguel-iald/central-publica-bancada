"""Prepare four additive F5.2 map errata records; registration is a separate act."""
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent
BASE = HERE.parent
FROZEN = r"C:\IALD\Artigo\teste_acustico_beta_tgl_v1\10_frozen_neff_v1.py"
V1 = r"C:\IALD\Bancada_Um\investigacao\preregistro_fase8_primordial\PREREGISTRO_FASE8_UNIVERSO_PRIMORDIAL_V1.json"
INSTALLED = r"C:\IALD\Bancada_Um\bancada\neff_canal.py"
AUDIT = r"C:\IALD\PROGRAMA_IALD\auditorias\F3.6.E1\AUDITORIA_F3_6_E1_C1_a4f6da3d.md"
V1_HTML = r"C:\IALD\PROGRAMA_IALD\auditorias\F4.3_F5.2\web\2506.20707v1.html"
V2_HTML = r"C:\IALD\PROGRAMA_IALD\auditorias\F4.3_F5.2\web\2506.20707v2.html"
EXTRACT = str(HERE / "EXTRACAO_TABELA5_R3_20261008.json")
CANDIDATE = str(HERE / "neff_canal.py")
OUT = HERE / "ERRATAS_MAPA_F52_R3_20261008.json"

common = {
  "tipo": "ERRATA", "estatuto": "REAL", "olhou_dados": False,
  "dados": ["Tabela 5 do arXiv:2506.20707v1 e v2; somente valores publicados, sem likelihood/dado bruto"],
  "metodo": "Extração de células CMB-SPA do MathML Table 5 em HTML v1/v2 pinado por SHA-256; comparação com frozen e V1 por leitura, candidato só em sandbox",
  "resultado": "CMB-SPA: v1 Yp BBN 2,81±0,12; Yp livre 2,99 +0,22/−0,26. v2 Yp BBN 2,82±0,12; Yp livre 2,96 +0,21/−0,24. O 2,97±0,12 do frozen/V1 combina linhas diferentes e não existe na Tabela 5.",
  "veredito": "ERRATA_DOCUMENTAL_F52_R3__D8_X16_OPEN__CANDIDATE_SANDBOX__GATE_UNTOUCHED",
  "nao_refazer": "Não editar frozen, V1, canal instalado, Bancada, memória ou gate; não selecionar Yp sem X16 nem admitir fonte sem D8.",
  "proximo_passo": "c1 audita esta camada; admissão D8 e escolha Yp X16 permanecem atos do operador antes de uso decisório ou instalação.",
  "nota": "Errata em nome de codex-gerente-tgl, 08/10/2026; valores auditados na F3.6.E1, agora extraídos dos bytes pinados. Fontes oficiais: https://arxiv.org/html/2506.20707v1 e https://arxiv.org/html/2506.20707v2, Tabela 5 (§VII.2.4).",
}

def entry(seq, route, domain, title, status, where, artifacts, defect):
    return {**common, "corrige": seq, "rota_id": route, "dominio": domain,
            "titulo": title, "pergunta": "Qual linha CMB-SPA vale para a fonte publicada e como a errata entra na linhagem sem reescrever o V1?",
            "status": status, "onde": where, "artefatos": artifacts, "defeito": defect,
            "refs": ["neff.frozen_v1_08ago", "cmb.neff_e_rho_mais_p", "primordial.fase8_era_da_radiacao"]}

records = [
  entry(607, "primordial.fase8_era_da_radiacao", "D1_FUNDO_COSMOLOGICO",
        "F5.2 R3 — errata ao V1 congelado da Fase 8 (seq 607)", "EM_CURSO", V1,
        [V1, FROZEN, EXTRACT, CANDIDATE, AUDIT],
        "V1 JSON linha 136 registra CMB-SPA 2,97±0,12; a Tabela 5 v1/v2 não tem esta combinação. V1 permanece selado e D8/X16 abertos."),
  entry(618, "primordial.fase8_era_da_radiacao", "D1_FUNDO_COSMOLOGICO",
        "F5.2 R3 — ressalva ao registro de conferência do V1 (seq 618)", "EM_CURSO", V1,
        [V1, FROZEN, EXTRACT, AUDIT],
        "Conferir hash/bytes do V1 não validou semanticamente a linha CMB-SPA 2,97±0,12; a errata é adjacente, sem mudar o selo ou a reserva D8/X16."),
  entry(606, "cmb.neff_e_rho_mais_p", "D1_FUNDO_COSMOLOGICO",
        "F5.2 R3 — errata ao canal N_eff instalado, por fonte congelada (seq 606)", "EXAMINADA", INSTALLED,
        [INSTALLED, FROZEN, V1, EXTRACT, CANDIDATE, AUDIT],
        "O canal instalado lê a fonte congelada que contém CMB-SPA 2,97±0,12; o literal não está no código do canal. Candidato R3 ainda não instalado."),
  entry(843, "neff.frozen_v1_08ago", "FASE8_PRIMORDIAL",
        "F5.2 R3 — complemento de artefatos e leitura pinada da errata seq 843", "EXAMINADA_COM_DEFEITO", FROZEN,
        [FROZEN, V1, V1_HTML, V2_HTML, EXTRACT, CANDIDATE, AUDIT],
        "A seq 843 já identificava a linha errada, mas não listava frozen/V1 entre artefatos e o candidato R2 usava números literais para a Tabela 5 v2. Este complemento não instala o R3.")
]
with OUT.open("x", encoding="utf-8", newline="\n") as f:
    json.dump(records, f, ensure_ascii=False, indent=2)
    f.write("\n")
print(OUT)