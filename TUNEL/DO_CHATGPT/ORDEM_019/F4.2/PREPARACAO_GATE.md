# F4.2 — conjunto D, preparação até o gate

07/10/2026 · [REAL] Consulta `NOS_VIVO\consultar.py --unidade F4.2`, seguida da leitura do manifesto e da proposta de metadados da ORDEM 018. Os hashes medidos constam em `RESULTADO.json`.

**Estado observado.** `MANIFESTO_CONJUNTO_D.json` diz `PREPARACAO_PARCIAL_NAO_RATIFICADA`: 9 artefatos preparatórios, 0 formas de onda novas, 0 injeções novas, 0 PE novo e nenhuma observação D aberta. A proposta de metadados é catálogo de candidatos, não manifesto de análise ratificado. Ela reúne 14 eventos e 4 holds; a existência de 28 arquivos HDF5/NPZ descritos não fixa por si as janelas, a qualidade dos dados nem a PSD para o teste.

**Contrato para a próxima etapa autorizada.** Antes de qualquer PE do conjunto D, congelar em manifesto próprio: identidade e hash SHA-256 de cada entrada efetivamente lida; seleção de eventos/holds; janelas off-source; máscaras DQ; estimador e faixa de PSD/ASD; calibração e sua versão; prior, hipótese, likelihood, semente e função de veredito; orçamento e limite de rodadas; saída permitida e hash do pré-registro. Toda troca de entrada após congelamento exige versão nova do manifesto, sem reaproveitar o veredito antigo.

**Gate.** [OPEN/INPUT] Falta a autorização registrada do operador para abrir os dados observados e executar o PE; a prévia de metadados não é essa autorização. F4.1 permanece em `AGUARDA_OPERADOR` para P3 A02, e F4.2 depende de seu contrato ratificado para o ramo P3→PE solo-220. Nenhuma leitura de arrays observados, injeção, PE ou mudança de V1/holds foi feita nesta entrega. O quadro deve mostrar F4.2 em `AGUARDA_OPERADOR` com este recibo, sem alterar o gate de F4.1.
