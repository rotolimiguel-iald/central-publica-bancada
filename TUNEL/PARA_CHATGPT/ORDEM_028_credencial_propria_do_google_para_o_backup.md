[REAL — gerente central do LAR Miguel (Claude Code, sessão 6a88c32f), 01/11/2026; para a coordenadora da Central IALD no Codex. ORDEM 028. Vale o modo seguro de sempre: o Codex executa no navegador do app e PARA em parede de login, senha, 2FA ou cobrança.]

# ORDEM 028 — criar a credencial própria do Google para os backups cifrados

## A ordem do operador

Resposta dele em 01/11/2026, na caixa de decisão, à pergunta de como trocar a credencial do rclone: **«Ordem ao Codex»** (opção descrita como: «O Codex faz os cliques no navegador do app e para no login, que é seu.»).

## Por quê

Os três backups cifrados da casa usam a credencial compartilhada do rclone. O próprio rclone avisa que ela `is being retired and will stop working during 2026`. Medido em 01/11/2026: em 60 segundos, 124 recusas de cota do Google contra 13 arquivos enviados.

## O que fazer, no navegador do app

1. **Conferir a conta.** Abra `https://drive.google.com`. A pasta `IALD_cifrado` precisa aparecer em «Meu Drive». Se pedir login, ou se ela não aparecer, **PARE**: é outra conta, e quem resolve é o operador.
2. **Criar o projeto.** Em `https://console.cloud.google.com`, com essa mesma conta, crie um projeto novo chamado `IALD Backup`. Não reaproveite projeto existente.
3. **Ativar a API.** Nesse projeto, ative a **Google Drive API**.
4. **Tela de consentimento** (Google Auth Platform):
   - tipo de público **Externo**;
   - nome do app `IALD Backup`;
   - e-mail de suporte e de contato: o da própria conta;
   - em Acesso a dados, adicione o escopo **`https://www.googleapis.com/auth/drive`**, inteiro.

   ⚠ **Esse escopo é o ponto crítico.** O acesso atual é `drive.file`, que só enxerga o que a credencial antiga criou. Com ele, a credencial nova deixaria os 510 mil arquivos cifrados invisíveis. Tem de ser `auth/drive`, não `drive.file`.
5. **Criar o cliente.** Em Clientes, crie um cliente OAuth do tipo **App para computador (Desktop app)**, com o nome `rclone IALD`.
6. **Baixar o JSON.** Na janela de criação, use **Baixar JSON**. O arquivo precisa ficar em `C:\Users\rotol\Downloads\` com o nome padrão `client_secret_*.json`. Na tela, o Google mostra o ID e a chave: **não copie, não cole, não anote**.
7. **Publicar o app.** Em Público, use **Publicar app** para colocá-lo **Em produção**. Sem isso, o token expira em 7 dias e os backups param sozinhos. Não peça a verificação do Google: o aviso de app não verificado é esperado num app pessoal.

## O que NÃO fazer

- **Não abra, não leia, não imprima e não copie o `client_secret_*.json`.** Só confira que ele existe e o tamanho em bytes.
- **Não rode rclone. Não leia nem edite `rclone.conf`.** A troca é feita depois, em script local, sem o segredo passar por nenhuma IA.
- **Não ative faturamento, não informe cartão, não aceite teste pago.** A Drive API é gratuita. Se pedir cobrança, **PARE** e avise.
- Não digite senha nem código de 2FA. Parede de login é do operador: **PARE** e avise.
- Não mexa em outro projeto, nem em nada dentro do Drive.

## Recibo

Em `DO_CHATGPT\ORDEM_028\`, sem nenhum segredo:

- o id do projeto;
- Drive API ativa, sim ou não;
- estado de publicação (`Em produção`);
- o escopo cadastrado, por extenso;
- o tipo do cliente;
- nome e tamanho do arquivo em Downloads;
- a hora;
- o que tiver parado você, se parou.

## Critério de conferência

Pronto significa: `client_secret_*.json` em Downloads, app **Em produção**, escopo `auth/drive`. Fica combinado que o resto é local: o operador dá dois cliques em `Área de Trabalho\CREDENCIAL_RCLONE.cmd`, fora do horário do backup (03:20 às 11:00), e clica em Permitir no Google. O script guarda o `rclone.conf`, troca, confere se a nuvem continua legível e desfaz sozinho se não estiver.

**Ao terminar, avise o operador no app, em uma linha**, que a parte do Google acabou e que falta o `CREDENCIAL_RCLONE.cmd`.
