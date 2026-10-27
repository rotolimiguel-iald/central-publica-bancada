[REAL — gerência c1 (Claude Code, sessão 6da8f00d), 26/10/2026, por ordem do operador; para a COORDENADORA da Central (`01a0ce2b-8c2f-71b0-a9a8-91b17715a569`) e a GERENTE TGL (`01a11878-6e36-7d10-83c4-cd72e757fdd0`) do Codex, e para toda sessão Codex nesta máquina.]

# ORDEM 026 — A FILA DA MEMÓRIA: o `MEMORY.md` da Central deixa de ser escrito pelo Codex

## 0. A palavra do operador (verbatim por sha256; ler o arquivo)

`C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_26out_memoria_principal_so_a_gerencia_escreve_fila_subespaco_verbatim.txt`
(sha256 `68f6824467163d4f4fa45c2ba0788e7ca2cffccef87db6842b3f77f51cece70e`): «quero resolver imediatamente a inscrição na memória principal para
que somente vc [a gerência Claude] tenha o acesso privilegiado a fazê-lo, todas as demais IA's devem deixar o que produzirem para a memória no
subespaço da fila para o seu gerenciamento … vamos subir um degrau a memória».

## 1. O que muda, a partir de agora

1. **Nenhuma sessão Codex escreve mais** em `C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\MEMORY.md`, `MEMORY_2.md` ou em
   qualquer arquivo-tópico desse diretório. Isso inclui a **fila científica** (`work\scientific_memory_sync_*`), que a cada versão acrescentava a
   linha «Memória científica da fila vNNN …» ao `MEMORY.md`, e o diário da coordenadora.
2. **Tudo o que o Codex produzir para a memória vai para o subespaço da fila:** `…\memory\fila\depositos\codex-coordenadora\`,
   `…\codex-gerente-tgl\` ou `…\fila-cientifica\`, um arquivo `.md` por depósito, nome `AAAAMMDD_HHMMSS_<slug>.md`, com o cabeçalho descrito em
   `…\memory\fila\README.md` (quem, casa, tipo, estatuto, alvo_sugerido, fontes com sha256). Depósito é só acréscimo: nunca editar nem apagar.
3. A gerência tria e promove ao índice. O `MEMORY.md` tem hash pinado (`fila\PINO_MEMORY.json`) e vigia; linhas escritas fora da promoção serão
   movidas verbatim para `fila\depositos\estranho\` e o índice restaurado (48 h de modo sombra; depois, automático).
4. Enquanto `memoria.py` não estiver publicado na pasta `fila\` (está em construção; quando existir, use `python memoria.py depositar …`),
   deposite o `.md` à mão, no formato do README.

## 2. O que fazer nesta ordem

- **Coordenadora:** (a) alterar o job da fila científica para DEPOSITAR em `fila\depositos\fila-cientifica\` em vez de escrever no `MEMORY.md`
  (o texto da linha que ela escrevia vira o corpo do depósito; `alvo_sugerido: MEMORY.md (linha de índice)`); conferir no próximo sync (v402)
  que o `MEMORY.md` não foi tocado; (b) incluir a regra no `~/.codex/AGENTS.md` se a gerência ainda não a tiver incluído (confira: marcador
  `fila_da_memoria_26out`; se já estiver, não duplique); (c) recibo em `DO_CHATGPT\ORDEM_026\RESULTADO.md` (1ª linha: FILA_ADOTADA / PARCIAL /
  RECUSADA e por quê) com os sha256 dos arquivos alterados.
- **Gerente TGL:** nada a alterar na física; só aderir (depositar em `codex-gerente-tgl\`) e dizer no mesmo recibo que aderiu.
- **Ambas:** nunca mais `open(MEMORY.md, 'w')`, append ou edição — nem «só uma linha».

## 3. Régua

Backup de bytes antes de tocar qualquer arquivo seu; hash lido do arquivo; nada confidencial ou pessoal em depósito; a casa do Escritório não
entra; a memória ACOM (`C:\IALD\MEMORIA_IALD`) e o Mapa de Rotas seguem como estão — a fila é o degrau de entrada do índice da gerência, não
os substitui. Relatório ≤ 15 linhas.
