# ORDEM_015_INSUMOS — o que há aqui e como ler

[REAL — pasta montada por script pela gerência em 23/09/2026; sha16 de cada arquivo em `MANIFESTO_INSUMOS.json`, gerado na publicação; conferir por script antes de usar]

**Ordem de leitura sugerida:** a ORDEM 015 inteira → `PROTOCOLO_ANTI_PAREDE.md` → `auditoria_da_gerencia_013bis\SINTESE_AUDITORIA_013BIS.md` → `auditoria_da_gerencia_013bis\CETICOS_COMPLETOS_013BIS.md` (as versões CORRIGIDAS que a ordem usa) → `reproducoes_da_gerencia\` (a medição da parede) → os JSON de estado.

- `ORDEM_OPERADOR_VERBATIM_22_23SET.md` — as falas do operador de 22 e 23/09, verbatim; a terceira fala de 23/09 fica em remissão (a razão está no próprio arquivo).
- `PROTOCOLO_ANTI_PAREDE.md` — a regra vinculante da §3 da ordem, integral.
- `auditoria_da_gerencia_013bis\`
  - `SINTESE_AUDITORIA_013BIS.md` — a síntese da auditoria da gerência à ORDEM 013-bis: veredito geral; estado por alvo; resultados físicos com estatuto; DG-01…DG-22; a parede técnica e a saída; a continuação C-01…C-20; as decisões do operador. **Fica como está**: a errata dela é a §2.6 da ORDEM 015.
  - `RESUMO_AUDITORIA_013BIS.txt` — a mesma síntese em texto corrido, com o veredito do cético (MANTIDO/REFUTADO) e o início da correção em cada DG e C.
  - `CETICOS_COMPLETOS_013BIS.md` e `VERIFICADOS_CETICOS_013BIS.json` — os 30 céticos (DG-01…DG-22 e C-01…C-08), com o MOTIVO e a CORREÇÃO integrais. É daqui que a ordem tira as versões corrigidas.
  - `SINTESE_ESTRUTURADA_013BIS.json` — a síntese em JSON (campos por alvo, defeitos, continuação, decisões).
  - `RELATORIOS_DAS_SETE_FRENTES_013BIS.json` / `.md` — os relatórios das sete frentes (A Parte A · B E0/E1 · C E2/E5/E4 · D E3 · E E6/E7/relatório · F régua/segurança/higiene · G caminho para o 5σ), cada um com o seu «NÃO ENCONTRADO».
- `reproducoes_da_gerencia\` — os scripts, as especificações e os resultados das reproduções da gerência (a parede do piloto: frentes D em `E3_piloto_orcamento_cegos\`, F em `regua_seguranca_higiene_custodia\pilot_repro\`, G em `caminho_5sigma\`; e os céticos: `cetico_C04\`, `DG02\`, `dg14\`, `DG11\`, `cetico_DG03\`, `dg06\`, `C08_E4_440\`, `E0_E1\`, `E2_E4_E5\`, `E6_E7_RELATORIO\`, `parteA\` e os demais). Os caminhos `…\scratchpad\aud013bis\…` citados dentro dos arquivos são da sessão da gerência e **efêmeros**: cada arquivo está aqui no mesmo caminho relativo. **Para rodar, copie para `Chatgpt\ORDEM_013_RINGDOWN\refeito\015\<subpasta>\` SÓ os `.py` e as entradas que eles leem — nunca os JSON/JSONL de resultado (os scripts gravam no diretório onde estão) — troque todo caminho de saída absoluto pela pasta da cópia e rode a cópia** (no WSL, `/opt/lal_env`, só leitura); compare por script com os resultados daqui, só leitura (§2.5 da ordem). **A bancada REFAZ; não copia o número.**
- `ESTADO_AUDITADO_013BIS.json` — sha16 de 83 artefatos-chave da bancada (o registro com o sha256 inteiro), lidos por hashlib em 23/09; o STATUS marcado `vivo`; a semente cega NÃO foi lida nem hasheada. Divergência de artefato da bancada NÃO é bloqueio: lista-se na entrega com os dois sha16 e a causa.
- `FONTES_DA_CASA.json` — as 31 fontes do `FONTES_DA_CASA.json` da 013-bis re-hasheadas + a própria ORDEM 013-bis, o seu MANIFESTO e o seu FONTES (34 entradas). Em 23/09, `um.py` `d9f5bd5dffc3333d` igual; só o diário da linhagem mudou (fonte VIVA, append).
- `SANEADOS.json` — os arquivos de texto em que termos restritos da casa (nomes de arquivos confidenciais; uma superfície de memória da gerência; a palavra de um log reservado) foram substituídos por remissão; o sha16 da cópia difere do original, e os dois estão ali.
- `NAO_COPIADOS.json` — o que da pasta de auditoria da gerência não veio ao túnel, e por quê (cópias de arquivos da própria bancada; varreduras de segurança da casa; um dump de chaves do JSON do programa; o gerador da síntese).
- `PROMPT_CODEX_ORDEM_015.txt` — o prompt para o operador abrir esta ordem no Codex, com o bloco [OPERADOR] a preencher.
- `MANIFESTO_INSUMOS.json` — sha16 de cada arquivo desta pasta e da própria ordem; não se lista a si mesmo.
