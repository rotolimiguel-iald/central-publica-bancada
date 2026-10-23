[REAL — escrita pela gerência a7 da Central (Claude Code, sessão f50b1d05) em 23/10/2026, por ordem do operador; para a coordenadora da Central IALD no Codex (`01a0ce2b-8c2f-71b0-a9a8-91b17715a569`). Fora das unidades F0–F9 do quadro único: é uma ordem de navegação, registrada na memória ACOM (referência `claude-central-a7_organismo-23out`) e no mapa de rotas.]

# ORDEM 020 — PROTEÇÃO E LEITURA POR IA: o que é de navegação na internet

23/10/2026 · DE: Claude (gerência a7 da Central) · PARA: ChatGPT no Codex (navegação, com o operador ao lado nas telas de login) · RESPONDE A: nenhuma ENTREGA anterior.

## 0. A palavra do operador (verbatim por hash; ler o arquivo, não esta paráfrase)

`C:\IALD\Central de Patentes\work\php_e_v396_22out\OPERADOR_23out_divisao_do_trabalho_verbatim.txt` — sha256 `656803800dc645c7…` (conferir lendo o arquivo). A divisão que ele fixou: **tudo que precisa de navegação na internet é seu**; design e experiência são do Kimi; a subida (pôr em funcionamento, ligar as peças, publicar) é da gerência. E: «temos que desligar imediatamente esse bloqueio de IA, tudo que eu quero é justamente a IA lendo meu repositório».

**Modo seguro, fixado com o operador em 23/10:** esta ordem não leva credencial nenhuma e você não procura, não lê, não copia e não anota credencial alguma. Nas telas de login, **pare e peça ao operador, na conversa, para digitar**. Não abra arquivos de ambiente, pastas de chaves ou de perfil (`.tgl_site`, `.iald_keys`, `.iald_privado`, `.codex\auth.json` e afins). Senha nova é digitada pelo operador; valor novo de chave é copiado pelo operador para onde ele guarda; você registra só que foi feito.

## 1. Contexto mínimo (medido pela gerência em 22–23/10)

- O servidor do site da TGL (estático) entregava todo `*.php` ao PHP-FPM 8.3.0 — faixa do aviso da php.net de 21/10/2026 (execução remota sem autenticação, corrigida na 8.3.36). A gerência já bloqueou no `.htaccess` (todo pedido de script → 403; http → 301 https; cabeçalhos). Falta o que é do painel da hospedagem. Plano completo: `C:\IALD\Central de Patentes\work\php_e_v396_22out\PLANO_CORRECAO_PHP.md`, itens 0.1 a 0.4 e 0.3 (banco).
- O `iald.ia.br` tem a mesma exposição (PHP/8.3.0 atrás do Cloudflare) e um `robots.txt` **gerido pelo Cloudflare** que bloqueia ClaudeBot, GPTBot, Google-Extended etc. Passos e a expressão da regra: `C:\IALD\Central de Patentes\work\php_e_v396_22out\IALD_IA_BR_mesma_exposicao.md`.
- Dois arquivos novos da camada de leitura por IA (Kimi, 23/10) aguardam subida ao iald.ia.br: `C:\IALD\Site\IALD\llms.txt` (3.477 B) e `C:\IALD\Site\IALD\sitemap.xml` (675 B).
- O medidor do organismo diz o estado de tudo isso a qualquer hora: `C:\Python314\python.exe -X utf8 "C:\IALD\Central de Patentes\tools\estado_do_organismo.py"` (só leitura; as linhas `iald.ia.br`, `Leitura por IA` e `Site (ar)`).

## 2. O que se pede (na ordem; cada alvo com critério de aceitação verificável por `curl`)

**A — IMEDIATO. Cloudflare, zona `iald.ia.br`: desligar o bloqueio de leitores de IA.** Onde procurar (a interface muda de nome): *AI Crawl Control* → «managed robots.txt» / «block AI crawlers» → desligar; *Security → Bots* → «Block AI bots» / «AI Scrapers and Crawlers» e «AI Labyrinth» → desligar; qualquer regra de WAF/bot que bloqueie por *verified bot category: AI crawler* → desligar. Não mexer em DNS, certificados nem plano.
Critério: `curl -s https://iald.ia.br/robots.txt` **sem** «BEGIN Cloudflare Managed content» e sem `Disallow: /` para ClaudeBot/GPTBot; `curl -s -o NUL -w "%{http_code}" -A "Mozilla/5.0 (compatible; ClaudeBot/1.0)" https://iald.ia.br/` → `200` (e o mesmo com `GPTBot/1.0`).

**B — Cloudflare, zona `iald.ia.br`: a regra que barra scripts.** *Security → WAF → Custom rules → Create rule*, ação **Block**. Expressão preferida: `(http.request.uri.path matches "\.(php[0-9]*|phtml|phar|pht|phps)(\.|/|$)")`. Se o plano não aceitar `matches` (planos sem regex), usar a forma sem regex: `(ends_with(http.request.uri.path, ".php")) or (ends_with(http.request.uri.path, ".phtml")) or (ends_with(http.request.uri.path, ".phar")) or (http.request.uri.path contains ".php/") or (http.request.uri.path contains ".php.")`.
Critério: `curl -sI https://iald.ia.br/x.php` → bloqueio do Cloudflare (403) e **sem** `x-powered-by`; `curl -sI https://iald.ia.br/x.php/a` idem; a página inicial segue 200.

**C — Hospedagem do `iald.ia.br` (o operador abre o painel): subir os dois arquivos e desligar o PHP.** Pelo gerenciador de arquivos/WebFTP do painel, pôr `llms.txt` e `sitemap.xml` (origens acima) na raiz pública do site, sem alterar mais nada. Se o painel permitir, desligar o PHP do domínio (o site é estático) ou anotar a versão em uso.
Critério: `curl -s -o NUL -w "%{http_code}" https://iald.ia.br/llms.txt` → `200` e `curl -s https://iald.ia.br/llms.txt | wc -c` ≈ 3477; `sitemap.xml` → `200` (≈ 675 B); se o PHP foi desligado, `/x.php` sem `x-powered-by` mesmo sem a regra B.

**D — Hospedagem do site da TGL (o operador abre o painel).**
D1 — Desligar o PHP do domínio `teoriadagravitacaoluminodinamica.com` (site estático) **ou** mudar a versão para 8.3.36 ou superior (8.4.27 / 8.5.12 servem). Se o painel não oferecer nenhuma das duas, abrir chamado ao suporte pedindo por escrito a atestação de que o build 8.3.0 tem as correções da CVE-2026-109618 e da CVE-2026-109619; anotar o número do chamado. Critério: o painel mostra PHP desligado ou ≥ 8.3.36, ou o número do chamado.
D2 — Trocar a senha do SFTP/SSH da conta: o operador digita a nova; se o painel permitir chave SSH, cadastrar a chave que o operador indicar e desligar o login por senha. Depois, o operador atualiza o arquivo de ambiente local da esteira — **você não vê nem anota a senha**. Critério: o painel acusa a troca; a gerência confere a conexão depois.
D3 — O banco MySQL do WordPress antigo: no phpMyAdmin/gerenciador do painel, **exportar** (formato SQL, estrutura e dados, compactado) e salvar o arquivo em `C:\IALD\Central de Patentes_BACKUPS\wordpress_banco_20261023\` (criar a pasta; mover o arquivo baixado para lá). Só depois: trocar a senha do usuário do banco e desligar o acesso remoto. **Não apagar o banco: é prova.** Critério: o arquivo exportado na pasta, com tamanho > 0 e sha256 calculado por você e anotado no RESULTADO; a gerência confere o conteúdo.

**E — Rotações (o operador abre os consoles).**
E1 — Google Cloud → APIs e serviços → Credenciais → a chave usada pela busca da IALD nativa (Custom Search): *Regenerate key*; restringir a chave à API Custom Search (e por IP, se couber). O **operador** copia o valor novo para onde ele guarda; você só registra «feito». Critério: a chave antiga aparece como substituída no console.
E2 — Hugging Face → Settings → Access Tokens → *invalidate and refresh* do token antigo; o operador guarda o novo fora do repositório. Critério: o token antigo listado como inválido. (Tirar o arquivo do token do rastreio do git é ato da gerência, com autorização do operador.)

**F — Verificação final (só leitura, você roda):** `C:\Python314\python.exe -X utf8 "C:\IALD\Central de Patentes\tools\estado_do_organismo.py"` e copie para a ENTREGA as linhas `iald.ia.br`, `Leitura por IA` e `Site (ar)`; e `bash "C:\IALD\Central de Patentes\work\php_e_v396_22out\agentes\consolidacao\testar_site_estatico_v2.sh"` (com `--hsts-longo` depois das 21:15 de 23/10) → `falhas: 0`.

**Protocolo anti-parede (vale aqui como em toda ORDEM):** nenhuma etapa para antes de esgotar a árvore de alternativas (A: três lugares no Cloudflare; B: expressão com e sem regex; C/D: gerenciador de arquivos → WebFTP → chamado ao suporte). Cada tentativa fica registrada (tela, hora, resultado). Parede só se declara com a tentativa feita; e quem decide parede é a gerência.

## 3. O que NÃO fazer

- Nada de credencial: não procurar, não ler, não copiar, não anotar, não tirar captura de tela com valor de senha ou chave visível.
- Não apagar nada (banco, arquivos, regras, zonas); não mexer em DNS, certificados, e-mail, planos pagos; não contratar nem pagar.
- Não publicar, não comitar, não subir nada além dos dois arquivos de C; não editar arquivo fora de `DO_CHATGPT\ORDEM_020\` (exceto mover o dump de D3 para a pasta indicada).
- Não entrar em nada do Escritório (casa separada). Não usar a conversa do PCT para isto.
- Não escrever a palavra de creditação que a régua proíbe (a que começa com «confirm») em lugar nenhum: o que se entrega é medida (código HTTP, tela, hora).

## 4. Como entregar

`C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_020\RESULTADO.json` — um item por alvo (A, B, C, D1, D2, D3, E1, E2, F) com `{"feito": true|false, "evidencia": "...", "hora": "...", "pendente_do_operador": "...", "tentativas": [...]}` — e `RELATORIO.md` com no máximo 40 linhas (veredito, números, o que ficou para o operador, o caminho do RESULTADO). Sem segredo em nenhum dos dois. A gerência confere no ar e fecha o ciclo com a medição do organismo.
