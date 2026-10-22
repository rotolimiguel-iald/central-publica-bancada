[NÃO-CEGO — E2 registrado; campanhas e teste físico ainda NÃO PAGOS]

# E2 — registro testemunhado antes dos dados novos

registro_sha256: e1be6b0409720c6883af5281458922fb03c5329bc0b08df7efe129d65e487416
registered_utc: 2026-09-22T21:44:43.687549+00:00

Abertura vinculante `ENTREGA_013BIS_ABERTURA_operador.md` — SHA256 `0118a54b7a806a0a5ef5572afc8349c223cc3da4bec62ff18a9cd1b07433f9f0`.
Ficha `REAPROVEITAMENTO_AMPLIACAO_E2.md` — SHA256 `6725472922bad1d3b52ef279e1e17c2ef50ad30c24ebafd4b6bc3371026f42e8`.

PAGO: desenho, código integral pinado, critérios pré-análise, leituras paralelas, protocolo de cegueira e controles finitos. NÃO PAGO nesta nota: nulos de campanha, Kerr/piloto IMR, calibração de duas famílias, PE cega, normalização hierárquica e teste físico. A aplicação do GO existente está vinculada às revisões; só o recibo final E2_ACTIVATION_COMPLETE permite execução. Esta nota isolada não ativa o registro nem relata resultado científico.

O censo contém 48 identidades de calibração/exclusão de cegueira. 14 eventos elegíveis não foram localizados no escopo documental congelado; 4 têm pendência de qualidade. Ausência no escopo não é ausência universal de publicação. Nova conferência documental precede cada admissão. Os 9 publicados fora do antigo corpus permanecem excluídos da rota cega; a exposição incidental descrita no censo fica preservada.

Os alvos E0 não garantem 90% de poder após incorporar nuisance. A matriz E1 entra apenas como INPUT sintético. O registro conserva 10 leituras, nenhuma escolhida, e proíbe offset fixo em zero como estatística de teste. Com gate sistemático vermelho não se declara significância física nem se combina eventos para uma descoberta.

Nulos: 25 células pré-fixadas, 1,609,000,000 desenhos sintéticos no total. Gaussianos e cauda t5 de medida com nuisance gaussiano têm interpretações distintas; os limites empíricos de resolução são reportados. Não equivalem a calibração física da pipeline.

Piloto GW250114: janela 16 s, fonte IMR e quatro deformações livres, priors INPUT; Kerr220/10M precede a execução IMR. A família alinhada pSEOBNRv4HM_PA difere do produto publicado precessante v5PHM. O limite temporal foi verificado nos cantos dos priors; o interior não é certificado por esse teste. Remanescente usa fit GR nomeado e redshift usa Planck18 externo INPUT; não são observáveis independentes.

Cegueira procedural no mesmo computador: somente o compromisso SHA256 da seed fica no registro; logs e intermediários sem deslocamento permanecem privados. Não há custódia humana independente. Descegamento exige informação suficiente, gate sistemático verde e revisão vinculada ao conjunto.

Prazo rígido contínuo: `2026-09-24T11:06:33.802143+00:00`. E3.2 fixará alocação adicional com custo medido do piloto e testemunha própria antes de novos jobs. Nenhuma autorização para ultrapassar 40 h. Catálogos futuros: AWAITING_DATA.

Tentativas e correções anteriores permanecem nas revisões: adaptador inicialmente rejeitado, janela de 8 s insuficiente, guardas de downloads, publicação, qualidade e payload reforçadas. A primeira tentativa de selagem falhou na política de execução de scripts do PowerShell antes de criar pasta privada, seed ou registro. A aplicação V1 e o candidato002 foram preservados; a aplicação V2 usa API nativa Win32 de ACL, revisada separadamente, sem alterar a política de execução. Nenhuma dessas correções é resultado físico. N/A — sem Lean.

Comandos previstos (WSL /opt/lal_env, dentro do prazo): `python -B bis/e2_code/null_campaign.py`; `python -B -O bis/e4_e5_prepare/deterministic_e4_e5.py --execute --authorization <ativação pinada>`; `python -B bis/e2_code/run_controlled.py --job GW250114_PILOT` somente após E3.1/Kerr e encerramento F0. Saídas existentes são recusadas. Reprodução exige destino isolado e novo registro explícito, não sobrescrita.

## Revisões e código

- Registro — `e1be6b0409720c6883af5281458922fb03c5329bc0b08df7efe129d65e487416`.
- Candidato — `172811a2fe94f8db540459d782e24517df9b672b21b6b6a3b6dd8759ee4234e5`.
- Aplicação técnica do GO — `196625fd41c15fec6351f2abe8f6f0c897413d1c448c6dd00c994b05122a1c4d`.
- `bis/e4_e5_prepare/PE_R1_R2_R3_CLOSING_REVIEW.md` — `1da6c752d3313e18e2dd8e086d7254555d472a7aa8c0f9dcf14759d1569ef30f`.
- `bis/e7_prepare/MAIN_CODE_REVIEW_CLOSING_V3.md` — `03c85cf53fa30c67ca60454d5ca70320406c8281994ef8d92de5acd3f33fd993`.
- `bis/e2_publication_census/E7_INDEPENDENT_REVIEW_V3.md` — `b9134bbcadd34726b2368b1e38b06d66901aee3654aa54ebbd0a13aa6035296c`.
- `bis/e2_publication_census/E7_INDEPENDENT_REVIEW_V4.md` — `ef51c72771f903c9bd973956bcf43c2cc58b2c0d52a84aa93c5b6f2e8f5eb20d`.
- `bis/e2_publication_census/E2_SEALER_CLOSING_REVIEW_V3.md` — `eb64d998cf36a29af0c3ca9a279fe1b43df7eaa5f4148ae5475d065bae39b7b8`.
- `bis/e2_code/blinding.py` — `7d4407fde07c66929651b017501873ecd4bd69ca80fd3e6cd03eaf8e653c6bc5`.
- `bis/e2_code/fetch_registered.py` — `a6066c933d29f13fea6a786dac8d9c6c2ecd4496bc0ff2c6d36a543e798132cb`.
- `bis/e2_code/injection_design.py` — `12017563c123df76b856ddedecf9166ddc4c25fe26a5c8b773bc82086b6c842d`.
- `bis/e2_code/null_campaign.py` — `9fa748e79ba55312543220542f4e470b8759360cd30040ae7fc1f35bf7859785`.
- `bis/e2_code/null_runner.py` — `1b6bf00beced255d45ac642de5209d32440e486f8a3af469e92a47c58fe1c561`.
- `bis/e2_code/pe_runner.py` — `6712610a0392abe629b6ea5b5f4fa5a45b2c8b9a3dfb123c952513f18cef68fa`.
- `bis/e2_code/pseob_source.py` — `2c9a053177bd2671da1879f60343434b3605b3274994b42d68aa50cd68f4ff2f`.
- `bis/e2_code/registration_guard.py` — `3cb2d9ef0672ccdf9bbca8547102b9a1323ea9d51bbc780732bb78bad99b40d7`.
- `bis/e2_code/remnant_conversion.py` — `87604de5c8fa7139cd6aa4d0c4fde09476105769735e44d476f3b9a55aa11bc1`.
- `bis/e2_code/route_iv_null.py` — `dfcf9491ab98f9d32aae119177f53a3622289593c19c528e50cd091ebd7000cd`.
- `bis/e2_code/run_controlled.py` — `7b5dd6484014942ee5fdd9fc3e529eaf05f9dffe463f35cdd10a01bdcf86334d`.
- `bis/e2_code/strain_io.py` — `a52faf32e88088320c57d303987a31ec2b9b59c93e162923d603c2c96b21a5b6`.
- `bis/e2_code/synthetic_null.py` — `be0fa6d4b678993edcbc7dec15f311950c51e466020dc99c5d0f043763eb65f1`.
- `bis/e2_code/temporal_contract.py` — `c8f4ecbc28d4312e3885d61c14f174062c6055eee0bbd54897e725a18240b605`.
