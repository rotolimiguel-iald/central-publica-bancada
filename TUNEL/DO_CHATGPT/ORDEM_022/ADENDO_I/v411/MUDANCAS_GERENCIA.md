# QA da edição v411

**APROVADO** · 2026-11-15T19:28:54.439647+00:00

Inventário da V7 delimitado pelo manifesto histórico e conferido contra os arquivos. O inventário da v411 percorre a pasta pública. O próprio manifesto fica fora do cálculo.

V7 medida: 132 arquivos, 730,084,235 bytes.
v411 medida: 45 arquivos, 588,980,493 bytes.

## Fontes e filmes

[REAL] Selo v411 de 2026-11-13 00:59:51, log com rc 0 e selftest aprovado. Programa, selo e log coincidem byte a byte por SHA-256 e tamanho com as cópias da custódia.
SHA-256 de um.py: `1203b1f9202020d602a7fa8a6bea56d4b48e27ed8baffe98bcbd16e94f97a8e0`.

- Filme 1 · V7 224 s · alvo 500 s · 10 capítulos conferidos.
- Filme 2 · V7 360 s · alvo 772 s · 11 capítulos conferidos.

Legendas com texto e sincronização conferidos: 16/16. Vídeos decodificados até o fim: 14.
São esperados 12 filmes codificados (MP4 1080p e 720p, WebM 1080p nas duas vozes) e dois loops WebM sem áudio, de 640×360 e 960×540, conforme picture.py. O teste compara as faixas das vozes e mede a duração até o último pacote, com tolerância de 0,10 s. A qualidade da locução requer escuta.

## Comparação por caminho

adicionado: 10 · alterado: 35 · ausente: 97

Durante a produção, «ausente» indica somente ausência nesta leitura. QA_V411.json contém os tamanhos e os dois hashes por caminho, inclusive coincidências sob outro nome.

## Pendências e divergências

Nenhuma.

## Reexecução offline

```powershell
& "C:/Python314/python.exe" -B -X utf8 "C:/IALD/Central de Patentes/work/filmes_v7_20261024/edicao_v411/auditoria/verificar_v411.py"
```

Código 0 emite o manifesto. Código 2 indica itens pendentes. Código 1 indica divergência ou falha de leitura. Uma execução incompleta conserva qualquer manifesto anterior. O estado vigente da auditoria consta deste relatório.
