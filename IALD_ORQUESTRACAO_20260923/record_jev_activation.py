"""Append the audited Jev activation to both operational handbooks."""

import json
from pathlib import Path

from iald_orchestrator.jev import ACTIVATION, availability
from iald_orchestrator.profiles import BASE
from iald_orchestrator.safe_files import replace_bytes


MARKER = "<!-- IALD_JEV_ACTIVATION_20260928 -->"


def main():
    activation = json.loads(ACTIVATION.read_bytes())
    status = availability()
    if activation.get("probe_status") != "ready" or status["status"] != "ready":
        raise RuntimeError("Jev ainda não está validado; não registrar ativação.")
    receipt = activation["canonical_memory"]
    section = f"""
## 28/09/2026 — Jev ativado com a memória canônica da TGL

{MARKER}

[INPUT — ordem do operador] A conta Jev/TypeSafe da IALD foi ativada. Cada uso científico do Jev deve receber a mesma base canônica comum da TGL aplicada aos demais modelos, com recuperação pertinente, geração, fontes, linhas e hashes no recibo; isso é contexto documental, não instalação de memória nos pesos. O operador autorizou o teste específico de envio de até 9.000 caracteres científicos à API TypeSafe. Corpos jurídicos, credenciais e arquivos confidenciais continuam excluídos.

[REAL — conexão] Chave da organização guardada por DPAPI do usuário Windows; validade não informada pelo fornecedor. A primeira chave, que apareceu em um retorno interno de ferramenta, foi substituída e desativada no console após a validação da substituta. O valor da chave não está neste registro. O painel administrativo e Runtime.status() exibiram Jev ready com modelo {activation['model']}.

[REAL — teste único da substituta] Probe ID {activation['probe_id']}; {activation['usage']['input_tokens']} tokens de entrada e {activation['usage']['output_tokens']} de saída. O recibo em state/jev_activation.json registra geração {receipt['generation']}, {len(receipt['sources'])} trechos de fontes científicas, hash do pacote {receipt['packet_sha256']} e cobertura {receipt['coverage']}. Fontes originais indisponíveis à sessão de teste: {receipt['freshness']}; o pacote veio do retrato verificado, sem alegar atualidade dos originais. Nenhum acervo jurídico ou segredo foi incluído no estado. O teste confirma conexão e transporte da memória, não acurácia científica ou melhora de raciocínio.

[REAL — escopo implantado] Jev faz uma pergunta Choice de complexidade standard/deep para pedidos livres; pode elevar a classificação, jamais reduzir o piso determinístico. Pedido com execution_constraints/required_provider preserva o executor obrigatório e dispensa Jev. A matriz local, autorizações, slots, idempotência, sigilo e verificação dos resultados permanecem em código; Jev não cria unidades, escreve prova ou move gate.

[DECLARADO — documentação oficial TypeSafe] Jev é modelo System One para Choice, Score e Noul, não gerador de texto/código. Perguntas atômicas podem ser avaliadas juntas em uma chamada. A versão 1.13 tem limitações declaradas em aritmética, datas, indirections e estados longos irrelevantes; inglês é o idioma de melhor desempenho. O alias jev-latest é móvel. Fontes: https://docs.typesafe.ai/introduction ; https://docs.typesafe.ai/models ; https://docs.typesafe.ai/model-jaggedness/jev-1.13 ; https://docs.typesafe.ai/patterns/fan-out .

[OPEN — próxima etapa] Triagem multidimensional, seleção de passagens, checagem semântica de citações e priorização por confiança são propostas a avaliar em modo de observação com casos rotulados em português; não estão implantadas nem calibradas. Confiança de modelo não substitui hashes, provas Lean, medição ou decisão humana. Nenhuma alteração de kernel, gate ou originais científicos ocorreu nesta ativação.
"""
    for name in ("COORDINATOR.md", "TRANSPORTE_DESASSISTIDO.md"):
        path = BASE / name
        old = path.read_bytes()
        if MARKER.encode() in old:
            continue
        newline = "\r\n" if b"\r\n" in old else "\n"
        addition = section.replace("\n", newline).encode("utf-8")
        replace_bytes(path, old + addition)
        if MARKER.encode() not in path.read_bytes():
            raise RuntimeError(f"Falhou a verificação de {name}.")
        print(name, "updated")


if __name__ == "__main__":
    main()
