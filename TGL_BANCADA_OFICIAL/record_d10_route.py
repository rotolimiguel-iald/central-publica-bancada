"""Record the clarified CMB/BAO direction with byte backups and atomic appends."""
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path

from record_universe_delivery import append

HERE = Path(__file__).resolve().parent
CENTRAL = Path(r"C:\IALD\Central de Patentes")
CANON = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\TETELESTAI\BANCADA_OFICIAL")
MARKER = "ORDEM018_D10_CMB_BAO_OPERATOR_CLARIFIED_20260927"
NAME = "ORDEM018_D10_CMB_BAO_CONTRATO_AVALIACAO.md"


def main():
    data = (HERE / NAME).read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    destination = CANON / NAME
    if destination.exists():
        if destination.read_bytes() != data:
            raise FileExistsError("Different protocol already exists; preserve it")
    else:
        temp = destination.with_name(NAME + ".new")
        with temp.open("xb") as handle:
            handle.write(data)
        if temp.read_bytes() != data:
            raise OSError("Incomplete protocol copy")
        temp.replace(destination)
    note = f"""## {datetime.now().astimezone().isoformat(timespec='seconds')} — D10/CMB–BAO acústico prioritário

[INPUT] O operador esclareceu: D10/CMB–BAO é a primeira rota de avaliação de 5σ global, com ΛCDM e alternativas cosmológicas explícitas. Congelar previsão fixa da TGL, calcular espectros/distâncias com precisão controlada, ajustar cosmologia/nuisance, usar covariance/sobreposições e calibrar por simulações. Separar (i) ajuste fixo, (ii) beta livre, (iii) tensão entre ambos e (iv) poder contra cada rival. Resolve a pendência laboratório versus BAO do registro anterior; a rota escolhida é cosmológica.

[REAL — preparação, sem novo experimento] Foi criado {destination}, SHA256 {digest}, espelhado na bancada Central. É plano IALD/Codex, não ordem final do Opus nem congelamento científico concluído. A coordenação irmã recebeu a direção e preparação de unidades Kimi/MiMo. O pacote antigo de ringdown continua retido com histórico de bloqueio; nenhuma nova execução de modelo é inferida dessa mensagem.

[DERIVED — contrato estatístico] D9/D10 e resumos/ajustes dos mesmos CMB/BAO contam uma vez. Beta fixa não fixa automaticamente perturbações. Adotar likelihoods compatíveis, nuisance/priors sem reaproveitamento circular, rivais declarados, ajuste refeito por simulação, cobertura composta e seleção explícita. Separar ajuste, tensão, p-valor e potência. Quantis posteriores antigos chamados5sigma não calibram cauda global. O exemplo zero excedências exige 10.450.778 simulações independentes para limite superior95% abaixo do p unilateral de5sigma; cálculo local, não simulações executadas. Métodos de cauda precisam validação.

[OPEN] Localizar tradução D9/D10 atual, fixar releases/overlap/modelos de perturbações, reproduzir referência, revisar e congelar protocolo antes dos novos ajustes. Nenhuma significância nova, alteração de kernel/gate ou original científico. Memórias receberam append com backup imediato de bytes.
"""
    paths = [root / name for root in (HERE, CANON)
             for name in ("MEMORIA_CENTRAL.md", "REGISTRO_DAS_CONVERSAS.md")]
    paths += [CENTRAL / "memory" / name
              for name in ("TGL_ATLAS.md", "TGL_INDICE_VIVO.md", "TGL_CORE_MEMORY.md")]
    for path in paths:
        append(path, note, MARKER)
    print("protocol_sha256=" + digest)


def record_anchors():
    text = """## Âncoras cosmológicas conferidas após a preparação — 27/09/2026

[REAL — leitura, sem execução] Na cópia histórica C:/IALD/Artigo/teste_acustico_beta_tgl_v1/_originais/tgl_paper_unified.py, D9_DESI_BAO começa na linha4231: seu texto descreve13 medidas DESI DR2 em9 redshifts e seu laço usa erros individuais, com H0/Om0/rd de referência. D10_acoustic_scale_closure começa na linha4337; sound_horizon na4317. D10 calcula escalas acústicas a fundo fixo, e as linhas4375–4381 declaram que o desvio absoluto em sigma tem limitação de precisão e não é tensão medida. Portanto, reutilizar a integral correta é distinto de reaproveitar aquele sigma como resultado global.

[OPEN — reconciliação] O frozen do Nível2 tem12 BAO. A seleção13/12 e as releases devem ser conferidas pelos arquivos de medições, não resolvidas somando os dois conjuntos. A inspeção local não estabeleceu equivalência entre os fechamentos S/L antigos e a implementação canônica atual. Isso é pendência localizada de recuperação/verificação, não afirmação de que tal derivação inexista no acervo. Revisão local delegada a Fermat, seguida de leitura direta das âncoras D9/D10 pela coordenação.
"""
    for root in (HERE, CANON):
        append(root / NAME, text, MARKER + "_ANCHORS")
    data = (HERE / NAME).read_bytes()
    if (CANON / NAME).read_bytes() != data:
        raise OSError("Protocol mirrors differ")
    digest = hashlib.sha256(data).hexdigest()
    note = text + "\nPlano atualizado: " + str(CANON / NAME) + "\nSHA256 medido: " + digest
    paths = [root / name for root in (HERE, CANON)
             for name in ("MEMORIA_CENTRAL.md", "REGISTRO_DAS_CONVERSAS.md")]
    paths += [CENTRAL / "memory" / name
              for name in ("TGL_ATLAS.md", "TGL_INDICE_VIVO.md", "TGL_CORE_MEMORY.md")]
    for path in paths:
        append(path, note, MARKER + "_ANCHORS")
    print("protocol_sha256=" + digest)


def record_source_review():
    source = HERE / "state" / "D10_CMB_BAO_SOURCE_EXCERPTS.json"
    raw = source.read_bytes()
    bundle = json.loads(raw)
    if bundle["status"] != "SOURCE_EXCERPTS_READ_NOT_EXECUTED":
        raise ValueError("Unexpected source bundle")
    digest = hashlib.sha256(raw).hexdigest()
    note = f"""## {datetime.now().astimezone().isoformat(timespec='seconds')} — Revisão dos payloads D10 e leitura do Nível2

[REAL] Os dois rascunhos locais Kimi/MiMo da coordenação foram conferidos: hashes de prompt consistentes e contrato integral presente. Ainda não submetidos nesta revisão. Foram pedidos adendos com fontes primárias e nova prévia; nenhuma chamada externa é inferida da preparação. A regra que a coordenação mencionou para MiMo após falha antiga foi solicitada com recibo/estado, sem remover restrições ou reabrir a unidade falha.

[REAL — leitura direta, sem executar fontes] Bundle científico {source}, SHA256 {digest}, {len(raw)} bytes. Trechos históricos D9/D10, implementação S/L, frozen e resultado N2, com hash de cada original e linhas. LikeN2.log_post em12_nivel2_frozen_e_verossimilhanca.py usa soma de resíduos BAO divididos por erros individuais: BAO diagonal, não covariance BAO completa. A fonteCAMB S altera somente Neff=NEFF_SM+DNDB*beta e omch2_eff=omch2+beta*(ombh2+omch2), com mnu fixado a0.06 e parâmetros usuais. Extrator local teve erro de sintaxe antes de qualquer escrita, corrigido; fontes científicas intactas.

[DERIVED — condicional a equivalência do executor e suporte] Se o rival LCDM+Neff(+massa de neutrino) admite os mesmos parâmetros efetivos e a mesma likelihood da varianteS, inclui suas distribuições observáveis. Então sup logL(rival)>=sup logL(Sbeta_fixa). Um teste com tamanho controlado uniformemente nesse rival não terá alto poder de rejeitá-lo quando o ponto verdadeiro daS também lhe pertence. Esse diagnóstico é da implementação históricaS; não declara equivalência da teoria atual com o rival. Incluir comparação bayesiana/penalizada responderia outra pergunta, com priors/penalizações explícitos. Kimi revisará a identificabilidade antes de caudas caras; MiMo revisará linhagem e covariance. Nenhuma medição nova de5sigma.
"""
    paths = [root / name for root in (HERE, CANON)
             for name in ("MEMORIA_CENTRAL.md", "REGISTRO_DAS_CONVERSAS.md")]
    paths += [CENTRAL / "memory" / name
              for name in ("TGL_ATLAS.md", "TGL_INDICE_VIVO.md", "TGL_CORE_MEMORY.md")]
    for path in paths:
        append(path, note, MARKER + "_SOURCE_REVIEW_" + digest)


if __name__ == "__main__":
    if sys.argv[1:] == ["--anchors"]:
        record_anchors()
    elif sys.argv[1:] == ["--source-review"]:
        record_source_review()
    else:
        main()
