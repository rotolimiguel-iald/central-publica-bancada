"""Write the source-corrected T08 method note with hashes read from bytes."""
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHAT = HERE.parents[3]
files = {name: HERE / name for name in (
    "T08_PUBLIC_COVERAGE.json", "T08_PE_METADATA_INDEX.json",
    "GW231206_GR_PE_DOWNLOAD_RECEIPT.json", "GW231206_SPLIT_SNR_PILOT.json",
    "GW231206_CUTOFF_VALIDATION.json", "T08_MIMO_SCIENTIFIC_AUDIT.json")}
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

lines = [
    "[REAL — inventário/piloto; KNOWN — método LVK; OPEN — seleção de 74, ε e α]",
    "",
    "# ORDEM 015 / T08 — auditoria das fontes e piloto",
    "",
    "O censo local contém 74 eventos O4 com SNR de rede ≥12. Os três lançamentos públicos de PE indexados listam arquivos para 70; quatro não aparecem neles. A soma dos 70 arquivos é 40,77 GB. O censo já continha medianas GR para 66 eventos; mediana do remanescente não é MAP completo. A tabela por evento e o estado de cada fonte constam em `T08_PUBLIC_COVERAGE.json`. Nenhum evento recebeu SNR dividido por inferência da mediana.",
    "",
    "A ordem chama ≥8 e ≥8 de regra LVK. Os artigos primários [GWTC-3](https://eprints.whiterose.ac.uk/id/eprint/234685/7/2112.06861v3.pdf) (§IV B e Tabela IV) e [GWTC-4](https://arxiv.org/pdf/2603.19019) (§4.2 e Tabela 7) usam **>6 em ambas as partes** para o teste IMR. ≥8/≥8 é um limiar interno mais estrito, que pode ser calculado em paralelo; não se atribui ao LVK. A Tabela IV do GWTC-3 contém frequência de corte e SNRs divididos para eventos O3b selecionados, não MAP GR dos 74 O4.",
    "",
    "A fronteira publicada é a frequência dominante da órbita ISCO do remanescente Kerr. GWTC-3 a calculou a partir de medianas de parâmetros de origem; GWTC-4 passou a usar a mediana da distribuição posterior da própria frequência de corte. O [GWTC-5](https://dcc.ligo.org/public/0204/P2500781/017/paper.pdf) (§1) não incluiu o teste IMR de consistência, citando vieses espúrios identificados na literatura. Por isso esta seleção é exploração da bancada, sem reivindicação de endosso do teste pelo catálogo recente.",
    "",
    "Piloto independente GW231206_233901: o arquivo público GR PE contém posterior completo, duas PSDs, licença CC BY 4.0 e checksum conferido. O máximo entre as amostras de log-verossimilhança+log-prior dá f_ISCO=111,6905 Hz; a mediana de f_ISCO sobre o posterior dá 112,2122 Hz; a Tabela 7 publicada registra 113 Hz. A norma ótima PyCBC/LAL no MAP amostral deu SNR de rede 14,6456 (inspiral), 13,4037 (pós) e 19,8533 (total); a Tabela 7 traz 16,5 / 14,4 / 21,9. O valor de SNR ótimo guardado na própria amostra é 20,0696. A diferença impede chamar o piloto de reprodução LVK aceita sem verificar convenções de waveform/calibração e versão de PE. Nenhum desses números é o ρ de potência F4 do T07.",
    "",
    "Para a função de seleção, a tipagem é ε(θ)=Pr[S=1|θ] sob injeções e recuperação especificadas, com S=1{ρ_insp≥c e ρ_pos≥c}. Por leitura Λ, α(Λ)=∫ε(θ)p(θ|Λ)dθ exige p(θ|Λ) e suporte definidos antes da medição. Sem uma população/medida de injeção registrada, IC para ε e α não são identificáveis. O rascunho MiMo confundiu ε com amplitude de eco e α com acoplamento; foi recusado na auditoria. Não se inventam tais distribuições para fechar T08.",
    "",
    "Custódia (SHA-256 calculado dos arquivos desta rodada):",
]
for name, path in files.items():
    lines.append(f"- `{name}`: `{sha(path)}`")
lines += ["", "[OPEN] Restam MAP/PSD verificados por evento, a escolha explícita entre corte >6 e ≥8, a reconciliação do piloto com o produto IMRCT e o desenho de injeções/população para ε e α. Esses itens não movem o gate matemático."]
out = CHAT / "TUNEL" / "DO_CHATGPT" / "ENTREGA_015_MEDIDA_T08_fontes_e_piloto.md"
with out.open("xb") as stream:
    stream.write(("\n".join(lines) + "\n").encode())
print(sha(out))
