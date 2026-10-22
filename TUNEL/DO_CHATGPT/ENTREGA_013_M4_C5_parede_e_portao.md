[REAL — PAREDE MEDIDA; DERIVED nas previsões locais; C5 fechada sem aprovação de calibração]

# ENTREGA 013 M4 — C5, parede e portão

## Critérios

| Critério | Resultado e prova |
|---|---|
| Duas bases de SNR e dez leituras | PAGO: 4referências família/PSD a403Mpc + normaGW25011410tM, 50linhas; referênciaGR e SNRa1 separados. |
| Fonte fixa e desconhecida | PAGO como Fisher de forma220referência: fontefixa é hipóteseotimista; 220comM/spinlivres não identificável. Não se generaliza degenerescência para IMR completo. |
| Portão com hash, antes de qualquer nova PE | PAGO nesta correção NÃO-CEGA; não foi anterior à antiga C6, agora C6-pre. Todos os cenários atuais ficam abaixo de5. |
| Calibração de duas famílias | NÃO PAGO científico; PAGO como parede: FULL_IMR0/288, MATCHED_RINGDOWN94/288, famíliasopostas0/96. Não dizer que nenhum grupo de toda a matriz passou. |
| Mistura e crime inverso | PAGO como correção:19/24 é conjuntofechado com verdade dentro da mistura; não resolve erro de forma. SEOBaltoSNR continua não resolvido. |
| Malha interna | PAGO como errata: taxasinternas131072/262144/524288Hz, não uma certificação até32768Hz. Todos os controles de taxa não passaram; SNR200/600 permanecem limitados. |
| Rigor assimétrico | PAGO documental: busca não linear/fonte livre existente sóR-B; outrasleituras NÃO PAGAS nessa matriz. Opção adotada é declarar a assimetria, não iniciar campanha. |
| Amplitude/relógio livre Fisher | PAGO no modeloesc alar gaussiano com fontefixa: integralUniforme[0,1]48casos; equivalência aτ★uniforme só na lei quadrática/partiçãofixa. NÃO PAGO como evidênciaIMR física. |
| N, ponto e log1p | PAGO:384linhas; N é mediano(50%) de eventos idênticosindependentes, recebe SUBRESOLUTION quando aplicável. A tabela same_source usaagora convençãolog, velha preservada. |
| Parada | PAGO: C5não reabre nesta ordem; ParteBterá registroecritérios próprios. F0antigoé anexo diagnóstico, nunca veredito. |

## Poder e suas hipóteses

| Base | rho | rho/40 | z local R-B |
|---|---:|---:|---:|
| REFERENCE_INJECTION_403Mpc | 10.065913 | 0.25164782 | 0.10171847 |
| REFERENCE_INJECTION_403Mpc | 10.653501 | 0.26633753 | 0.10171847 |
| REFERENCE_INJECTION_403Mpc | 17.055144 | 0.4263786 | 0.10171847 |
| REFERENCE_INJECTION_403Mpc | 18.065253 | 0.45163131 | 0.10171847 |
| GW250114_MEASURED_NORM_10tM | 19.099706 | 0.47749265 | 0.19300711 |

O rho da janela é sqrt(norm²−dof), erro aproximado1,45 sob ruído gaussianoestacionário; não é SNR de filtro casado nem significância de detecção. O transporte porrho preserva a forma220de referência, não mede FisherIMR do evento. Os controlesPSD por detector são cenários separados, cada um normalizado ao mesmorho da rede; não se somam como informação independente. O maior z desses50cenários é 0.7132090215113822.

Mesmo se o modelo local tivesse calibração aprovada, a leitura continuaria subpotente. Hoje permanece INCONCLUSIVE_SYSTEMATICS por FAILED_TWO_FAMILY_CALIBRATION. NOT_FALSIFIED não é confirmação.

## Aviso de Occam e alcance do cálculo livre

Em SNR≤40, lnBpositivo soba=0 pode ser efeito de volume de prior; nunca converter emσ. As faixas específicas estão no reciboC5_WALL_COUNTS, com aviso emcada linha, inclusive valores maiores emR-MOD. A integral livre R-B aSNR40 dá média≈0,0616 soba=1 e≈−0,0203 soba=0 no Fisheratual; o≈0,05 da ordem usaσaproximado, não mesma geometriaexata. Esses objetos diferem da evidência pontual e da evidência sobre a fonte astrofísica inteira.

NÃO PAGO: cobertura/viés com fonte marginalizada, outras leituras na matriz de fonte livre, ET/CE na recuperaçãoIMR e limitesfísicos deτ★. Nenhuma nova campanha de injeção foi executada para esta entrega. TentativaF4inicial com basesSNRambíguas preservada no primeiro builder; o v2 reutilizou norma/Fisher somente após igualdade dos resultados, e v3corrigiu a tabelaauxiliar. A reprodução numérica dos revisores e os hashes estão abaixo.

## Arquivos e ficha

| Arquivo | SHA256 lido |
|---|---|
| [PORTAO_DO_PODER_013.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/PORTAO_DO_PODER_013.json>) | `ec5e012bc40a3e005bc83533b4b5dab4af0d221c86ee92aa521a96b3f067cab0` |
| [PORTAO_DO_PODER_013_v2.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/PORTAO_DO_PODER_013_v2.json>) | `c2972e3cc32286532908875b2a3ddb5d168d0669a6846e3e2c1d16e855c2b133` |
| [C5_FISHER_v2.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/C5_FISHER_v2.json>) | `ac36fe7eb92d6b315a368ba8ea43ee09ad2d52e4456a0c9bfc61ae06bffb5b6f` |
| [C5_FISHER_v3.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/C5_FISHER_v3.json>) | `ef7a800369ba07328852b2ffe6a54c13f9b20476775f557113ca31fc50a5a22b` |
| [bis/F4_GW250114_WINDOW_POWER_NORM.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/F4_GW250114_WINDOW_POWER_NORM.json>) | `6accdff1858d3a6a67298d231f4a3090f62ff735438359abfde70dcb01317b8a` |
| [bis/C5_WALL_COUNTS_013BIS.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/C5_WALL_COUNTS_013BIS.json>) | `df21c6792664e63df63f4496ae7a725c7e5eb903d7ed57ac40f2b0636ec38723` |
| [C5_NATIVE_MESH_AND_BALANCED_START.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/C5_NATIVE_MESH_AND_BALANCED_START.json>) | `536ba75cb6f433c47d3c758bb9fa63d1f853f67cbee25ff411e7fa71fc1f2cb7` |
| [bis/F4_POWER_GATE_REVIEW.md](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/F4_POWER_GATE_REVIEW.md>) | `35b02b3d0a4d45ecfbacc156f73c909eeab10f9e12bf07a6ca169b37b6d4d914` |
| [bis/F4_CLOSING_REVIEW.md](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/F4_CLOSING_REVIEW.md>) | `3fcb72793d5a217033d2f374283f734e2ca07f1d35738a90684d9cdacefd3c05` |
| [REAPROVEITAMENTO_C5.md](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/REAPROVEITAMENTO_C5.md>) | `a7860871a2f86e36c15dbf9dfcc655430e85b9cafe7fb08c0ac6cf9bff459f97` |
| [refeito/measure_power_gate_013bis_v2.py](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/refeito/measure_power_gate_013bis_v2.py>) | `d18e47c7a183165c99d430b69aca8ac0e544dc2a6718842df8d96be477bcd349` |
| [refeito/correct_f4_review_013bis.py](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/refeito/correct_f4_review_013bis.py>) | `e230fb2fde0175d100f0162c13753eac51f54e929f61294992d1a7841285027f` |
| [refeito/summarize_c5_wall_013bis.py](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/refeito/summarize_c5_wall_013bis.py>) | `f89d64e0a0cc820dd05619a4420b47eca10405c26a09c5879370c9c7d3bb9674` |

Abertura do operador SHA256 `0118a54b7a806a0a5ef5572afc8349c223cc3da4bec62ff18a9cd1b07433f9f0`. Data UTC 2026-09-22T18:14:22.259453+00:00. Ordem única 013BIS; não há pausa de marco. A aceitação aqui é documental/numérica no escopo indicado; não substitui a auditoria da gerência. Axiomas: **N/A — sem Lean**; teoremas novos: **0** (nenhum fonte Lean foi produzido). Nenhuma escrita em um.py, kernel, memória, Atlas, diário, espelho ou site.

Verificação não destrutiva nesta máquina:
```powershell
& C:\Python314\python.exe -B "C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\refeito\deliver_m1_m4_013bis.py" --verify
```
Os medidores citados recusam sobrescrita: reprodução computacional completa usa cópia isolada da bancada com os insumos preservados. O script da entrega verifica hashes, não repete PE ou confirma leis físicas.
