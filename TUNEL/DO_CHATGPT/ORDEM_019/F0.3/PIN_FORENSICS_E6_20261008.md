# F0.3.E6 — complemento forense ao lado

[ERRATA AO LADO, em nome de codex-coordenadora] A F0.3.E5 incluiu o estado posterior 673780c0 e o atual cb0a73cb do ADENDO_TEMPERATURA_DIAGNOSTICO.md, mas seu texto .md omitiu o estado anterior da2513df, embora o JSON registre o pino. O backup `ADENDO_TEMPERATURA_DIAGNOSTICO.md.bak_20261008_114746` tem SHA-256 `da2513df5051ef9d5f2bb1f6783e8dd1a3f5bd3c1c9ee5bd1461c4814748d715` (4.789 B), pinado nos mapas 817 e 829. Os bytes da2513df são prefixo de 673780c0, que é prefixo do estado atual cb0a73cb. Uma sonda preliminar desta E6 supôs a ordem inversa e falhou antes de qualquer escrita; esta cadeia segue a medida dos tamanhos e bytes.

[REAL — F1.1] O pino do quadro 73 do `F1.1/INVENTARIO.md` (`04a42d036db5b2b989b842260573232d2dd5f9658f4d71cb6fcf15ee076a0c0e`, 5.314 B) existe em `INVENTARIO.md.bak_20261008_010215`. É prefixo dos bytes atuais. A E4 começou no pino 241, então este pino mais antigo precisava de registro próprio.

[REAL — AVISO] Os mapas 821 e 822 pinaram `AVISO_GERENCIA.md` em `ba43258263a608ef41cd3af179d26cb750bda173f33e5ddb7e40634294607efd` (31.561 B). O backup `AVISO_GERENCIA.md.bak_20261008_052608_296884` é prefixo do estado anterior a esta E6. Por ser memória viva, novas notas mudam o hash; o recibo de memória E6 registrará o próximo estado.

[REAL — F3.6] O mapa 816 pinou `asimov_lambda.cpython-312.pyc` com SHA-256 `111fea0c0eaafed31fd7fa41b2de834b17c01613c6225fbf7f45d42c268f7717` (19.958 B). A higiene E5 removeu o cache; o plano registra caminho, tamanho e hash, mas o arquivo não existe mais e não há cópia em `evidencias/`. **Esse pino histórico não se reproduz dos arquivos atuais.** Não reivindicamos custódia dos bytes nem regeneração idêntica.

[ESTADO] Os dois documentos append-only preservam os bytes antigos; a ausência do `.pyc` é uma perda de reprodutibilidade desse pino específico. Nenhum pino foi editado nesta unidade. Sem dado aberto, publicação ou mudança de gate.
