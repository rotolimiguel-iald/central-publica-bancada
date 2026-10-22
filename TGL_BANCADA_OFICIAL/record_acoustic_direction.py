"""Record the operator's acoustic redirection without changing any physics gate."""
from datetime import datetime
from pathlib import Path

from record_universe_delivery import append

HERE = Path(__file__).resolve().parent
CENTRAL = Path(r"C:\IALD\Central de Patentes")
CANON = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\TETELESTAI\BANCADA_OFICIAL")
MARKER = "ORDEM018_ACOUSTIC_DIRECTION_OPERATOR_20260927"


def main():
    stamp = datetime.now().astimezone().isoformat(timespec="seconds")
    note = rf"""## {stamp} — ORDEM 018: direção acústica indicada pelo operador

[INPUT — fala literal] “Estamos procurando no lugar errado o teste precisa ser acústico”. Esta instrução redireciona a escolha do teste; não declara um resultado experimental. Foi pedida distinção entre ressonadores/fônons de laboratório, som/interferência macroscópica e BAO/CMB. A resposta ainda estava pendente neste registro: nenhuma dessas três leituras foi atribuída ao autor.

[REAL — coordenação] A tarefa irmã de orquestração (01a0ce2b-8c2f-71b0-a9a8-91b17715a569) foi avisada pela ferramenta oficial para não despachar o pacote antigo de ringdown ao Opus. Os recibos, os seis pareceres, a crítica Física e o rascunho local permanecem históricos. O bloqueio de revisão automática do envio anterior permanece registrado; uma eventual autorização daquele pacote não basta para tratá-lo como protocolo acústico. Nenhuma nova chamada de provedor foi pedida nesta investigação local.

[REAL — fontes lidas; números históricos não recalculados] O diretório C:\IALD\Artigo\teste_acustico_beta_tgl_v1 contém um teste cosmológico. Foram lidos MANDATO.md e 14_ANALISE_NIVEL2_FECHADO.md. O mandato inclui DESI BAO e horizonte sonoro; o relatório de 14/08 usa Planck + DESI + priors. A variante S está registrada como convergida, N2_INCAPAZ, beta=-0,00243 +/- 0,01765. A L está registrada como N2_NOT_CONVERGED, estimativa preliminar -0,02427 +/- 0,01511. A retórica histórica “ambas incapazes” não transforma a cadeia L não convergida em inferência final nem demonstra o que uma extensão faria. Esta leitura localiza trabalho anterior; não o repete nem o revalida numericamente.

[KNOWN — fonte primária consultada] Cleland, Wollack e Safavi-Naeini, “Studying phonon coherence with a quantum sensor”, https://arxiv.org/abs/2302.00221, medem dissipação e dephasing de modos mecânicos usando sensor qubit; discutem defeitos de dois níveis (TLS) como causa de decoerência. Isso fundamenta a possibilidade de separar experimentalmente perda de energia e coerência, sem atribuir esse resultado à TGL.

[OPEN] Se a direção for laboratório, localizar no programa a tradução para o Hamiltoniano acústico, a escala temporal e o observável; conferir dados brutos/equipamentos realmente disponíveis e separar ruído térmico, TLS e ruído de frequência da previsão. Ainda não foram verificados dados laboratoriais acústicos instalados, hardware compatível, sensibilidade >=5sigma ou identificabilidade dessa assinatura. Não foi executado novo teste físico nem modificado modelo, kernel ou gate. O domínio GW já entregue permanece disponível; sua existência não determina a nova escolha experimental.
"""
    paths = [root / name for root in (HERE, CANON)
             for name in ("MEMORIA_CENTRAL.md", "REGISTRO_DAS_CONVERSAS.md")]
    paths += [CENTRAL / "memory" / name
              for name in ("TGL_ATLAS.md", "TGL_INDICE_VIVO.md", "TGL_CORE_MEMORY.md")]
    for path in paths:
        append(path, note, MARKER)
        append(path, "[ERRATA DE LOCALIZADOR] A primeira gravação do registro acústico "
               "interpretou a sequência barra-t como tabulação no caminho. "
               "Localizador correto: C:/IALD/Artigo/teste_acustico_beta_tgl_v1. "
               "Conteúdo científico e leitura dos arquivos não são alterados.",
               MARKER + "_PATH_ERRATA")


if __name__ == "__main__":
    main()
