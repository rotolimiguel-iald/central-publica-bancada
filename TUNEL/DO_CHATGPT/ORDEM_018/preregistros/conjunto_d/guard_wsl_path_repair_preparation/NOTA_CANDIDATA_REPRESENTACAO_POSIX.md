# Candidata documental: caminhos Linux no argv Windows → WSL

[DERIVED — candidata; OPEN — comportamento ainda não validado] A correção proposta separa a representação POSIX dos tokens de destino dos objetos `Path` usados no I/O de cada host. A única cópia candidata é `common.py.candidate.txt`, acompanhada de um delta textual; não há launcher novo nem módulo candidato importado ou executado. A request `4f5d0b21-e1d2-4906-a6ce-eb70e60bc6cf` continua falha terminal e não será reutilizada.

## Causa e responsabilidade

[REAL — evidência documental] O recibo ROOT e a errata do mapa 529 registram que os dois processos Python, principal e limpeza, retornaram 2 antes de abrir `linux_control.py`; o launcher externo retornou 1. Em `common.py` consumido, linha 8, escrevi a base Linux como `Path`. As linhas 64–66 serializavam `str(LINUX/script)`. No Windows, o tipo concreto escolhido foi `WindowsPath`, e os dois recibos `WSL_PROCESS` mostram o token do script começando com barra invertida. Essa foi uma falha da preparação: preservar o AST não conferia a semântica do caminho entre hosts.

O `pathlib` primário instalado foi lido como texto: `Path` escolhe a classe concreta pelo host (linhas 632–635), `PurePosixPath` usa `posixpath` e pode ser instanciado em qualquer sistema (601–607), e `as_posix()` substitui o separador do parser (325–328). As fontes e os hashes lidos estão no recibo. Não foi importada a candidata para demonstrar essa propriedade.

A falha de abertura não qualifica hook, latch, journal, limpeza Linux ou ciência. O rótulo original `UNCERTAIN_ORPHAN_STATE` permanece na evidência consumida. A inspeção posterior de ROOT encontrou zero identidades exatas no instante examinado; não se transforma esse retrato em garantia absoluta de ausência de órfãos.

## Duas alternativas e escolha limitada

| Alternativa | Mudança | Avaliação documental |
|---|---|---|
| A, escolhida | Base de transporte `PurePosixPath`, token por `.as_posix()`; `Path` concreto separado para I/O | Expressa a sintaxe de destino independentemente de `os.name`; todos os lançamentos e comparações de identidade usam o mesmo construtor existente. `posixpath` seria outra implementação possível da mesma fronteira. |
| B | Converter `(LINUX/script).as_posix()` no retorno atual | É menor e atende ao literal fixo lido; a interpretação inicial ainda depende do parser concreto do host, deixando a fronteira menos explícita. Não é genericamente equivalente para drives, UNC ou entradas arbitrárias. |

A candidata altera somente o import, o vínculo da base POSIX e a expressão do token de script. Mantém `WIN`, `BASE`, funções de identidade/STOP/gate/pidfd e os consumidores inalterados. `LINUX = Path(LINUX_ARGV_ROOT.as_posix())` continua concreto; no Windows, o I/O usa `WIN`, e no Linux usa `LINUX`. A proposta não pretende converter caminhos Windows arbitrários, aceitar novos nomes ou ampliar a allowlist.

**A cópia textual conserva o caminho e o request históricos exclusivamente para representar o delta mínimo. Não aplicar o patch no pacote consumido, renomear o `.txt` para execução, remover CLAIM ou usar esses identificadores em novo lançamento.** Uma eventual integração teria de receber decisão própria, novos identificadores e pins coerentes; nada disso foi criado aqui.

## Contrato e inventário de tokens

O transporte permanece uma lista de argumentos, sem shell, `split`, aspas embutidas nem URL encoding. `C:\Windows\System32\wsl.exe` é caminho Windows e permanece assim. `/opt/lal_env/bin/python` já é literal POSIX. As opções `--distribution`, `Ubuntu-24.04`, `--exec` e as flags Python não são caminhos.

O token corrigido é o script, índice 6 da lista interna e 10 da lista externa. Deve começar por `/`, usar separadores `/` e manter `Central de Patentes` como parte de um único elemento. Os papéis `--supervisor` e `--cleanup` apontam para `linux_control.py`; `--child` aponta para `worker.py`. Ambos os lançamentos Windows, o filho Linux, a comparação de identidade do pai e a busca restrita de processos convergem para `argv_for`, preservando a igualdade do que se lança e do que se procura.

[REAL — inventário delimitado] `--root` não aparece nos quatro instrumentos lidos (`common.py`, `launch_windows.py`, `linux_control.py`, `worker.py`); a candidata não acrescenta esse argumento. O root reside nas constantes. `EXEMPLOS_ESPERADOS_DADOS.json` registra a representação esperada do root como dado de interface, caso outra interface seja explicitamente aprovada depois. Não se afirma ausência global da opção no acervo. Caminhos de `/proc`, arquivos/journal e fixtures continuam objetos de I/O do host pertinente.

Os exemplos incluem os três papéis, nomes com espaços e placeholders explícitos para request/nonce futuros, não criados. São expectativas escritas, não saída de execução. O inventário contém também os dois tokens reais defeituosos para confronto e as linhas de todos os consumidores afetados.

## O que foi conferido e o que falta

[REAL — preparação] Foram feitas 55 conferências documentais/estáticas: pins de evidência terminal e errata, integridade de fontes, AST e preservação das funções fora do delta, além dos tokens efetivamente registrados. Todas constam como verdadeiras no recibo. Essa contagem não representa testes de integração, execução do construtor, WSL ou validação do reparo. Zero chamadas WSL, importações/execuções de candidata, hooks, controles, solver, dados D, novos IDs de execução, CLAIMs ou autorizações.

Somente duas verificações futuras mínimas agregariam evidência, se decididas separadamente:

1. Conferência pura e isolada do construtor de tokens, com os exemplos já fixados, cobrindo os três papéis, posições, barras e espaços e a igualdade entre lançamento e identidade. Essa verificação ataca diretamente a propriedade que a preservação de AST não mediu, sem hook ou WSL.
2. Se uma nova unidade concreta de transporte vier a ser autorizada, observar o argv recebido no destino e confrontar token, exitcode e recibos nessa própria unidade ou em receptor mínimo especificamente aprovado. Strings locais corretas não provam transporte por `wsl.exe`; não se cria uma campanha adicional automaticamente.

[OPEN] Nenhuma dessas verificações foi executada nesta preparação. A qualificação de latch/journal no runtime WSL permanece aberta. Nenhum avanço científico, reabertura de INIT003 ou nova PE decorre deste delta.

## Custódia do recorte

O mapa foi consultado antes, com os registros 528/529 preservados em `MAPA_ANTES.json`. O recibo fixa as fontes lidas; o manifesto fixa os artefatos desta preparação. O pacote consumido foi somente lido. Nenhuma memória compartilhada foi editada; o registro posterior do mapa classifica exclusivamente preparação documental/estática.

Cópia candidata: 4742 bytes, SHA256 `f0ddcbff558ccd0796889e4300a1c52c932a213e82569a9a3c678b193be05b91`.
Contrato de interface: 3801 bytes, SHA256 `10b6c782f5f681bb798efb4f263b45eb564322a20db7cfd1019e3ef7a46711a9`.
