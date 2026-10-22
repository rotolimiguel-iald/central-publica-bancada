"""Finalize the independent F3 review without touching the author's pilot."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
from audit_provenance import OUT,atomic,metadata
P=OUT.parent/'preregistros/conjunto_d/piloto_sintetico'
J=OUT/'REVISAO_PILOTO_SINTETICO_F3.json';d=json.loads(J.read_bytes())
rp=OUT/'REVISAO_PILOTO_SINTETICO_F3_RUNTIME.json';runtime=json.loads(rp.read_bytes())
assert d['all_checks_pass'] and runtime['result']['all_match'] and runtime['result']['count']==165
pins={Path(x['path']).name:x for x in d['sources']}
def pin(rel):return metadata(P/rel)[0]['sha256']
def link(label,rel,line=None):return '['+label+'](<'+str(P/rel).replace('\\','/')+((':'+str(line)) if line else '')+'>)'
d['review_status']='ACCEPTED_WITHIN_PINNED_P0_P2_SOURCE_INJECTION_SCOPE__NO_P3_OR_PE_CERTIFICATION'
d['finished_utc']=datetime.now(timezone.utc).isoformat()
d['findings']=[{'id':'F3-01','priority':'P3','status':'RESOLVED_BY_ADJACENT_ERRATA','text':'Contract02 explanatory read_allowlist_policy inherited RUN_001. Frozen run_id/code/receipt use RUN_002; adjacent errata corrects prose and preserves all pins.','errata':metadata(P/'ERRATA_ALLOWLIST_RUN002.json')[0]}]
d.pop('findings_pending_document_review',None)
d['runtime_independent_review']=metadata(rp)[0]
d['static_conclusions']={
'entry_contract':'Fixed SYN_A/SYN_B config rejects real-event/path/file-PSD fields; author scripts inspected, not executed by reviewer.',
'only220_scope':'pSEOBNRv4HM_PA full IMR and family GR harmonics remain; only DTau220 can depart zero in registered wrapper and six-call trace.',
'source_repeat_evidence':'GR/RB/GR and unique dictionary checks are supported by pinned source, executable guards, process stdout/rc and structured trace. Reviewer did not regenerate native waveforms.',
'audit_boundary':'Python audit hook installed after fixed pilot/runtime imports and runtime pin reads. Hook is not an OS sandbox or complete syscall trace; mounted open log excludes pre-hook activity and not every final write.',
'api_origin_scope':'V2 pins object/truth/array origin, rejects foreign/replaced/reused fixtures in recorded cases; process-local Python registries are not tamper-proof against arbitrary code or PE lifecycle certification.',
'prior_scope':'32 physical corners plus 32 rejected by q constraint, not continuous-prior tail/leakage proof.',
'statistics_scope':'Only three distinct synthetic injection cases; revision regression reuses arrays/noise. No independent evidence multiplication, recovery, coverage, bias, significance, power or cost of D PE.',
'v1_scope':'Only existing V1 file bytes hashed and compared with earlier audit; no events/data parsed anew.'}
d['excerpts']=[]
for rel,lo,hi in [('src/pseob_source.py',89,111),('src/synthetic_adapter_v2.py',18,28),('src/synthetic_adapter_v2.py',123,146),('src/synthetic_adapter_v2.py',156,164),('qualify_synthetic_v2.py',9,24),('qualify_synthetic_v2.py',37,51),('qualify_synthetic_v2.py',128,139),('NOTA_QUALIFICACAO_P0_P2.md',33,47)]:
 lines=(P/rel).read_text(encoding='utf-8-sig').splitlines();d['excerpts'].append({'path':str(P/rel),'sha256':pin(rel),'first_line':lo,'last_line':hi,'text':'\n'.join(lines[lo-1:hi])})
atomic(J,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
text=f'''# Revisão independente F3 — piloto sintético P0–P2

[REAL — auditoria local] **Nenhum achado bloqueante no recorte congelado P0–P2.** Uma errata documental P3 foi identificada e resolvida ao lado, preservando contratos, código e rodadas. A revisão aceita a qualificação de fonte e construção de injeções nos casos exercitados. **P3/PE, recuperação, cobertura, viés e poder do conjunto D permanecem OPEN e não foram executados.**

## Achado e resolução

**F3-01 — P3, resolvido.** O campo `read_allowlist_policy` do contrato02 dizia `writes RUN_001 only`; `run_id`, a expressão `run=ROOT/contract["run_id"]`, o hook e os caminhos registrados usam RUN_002. A {link('errata documental','ERRATA_ALLOWLIST_RUN002.json')} corrige a frase, mantém os hashes e não produz nova execução. A identidade do contrato, script e RESULT citados na errata foi reconferida. Nenhum código do autor foi modificado nesta revisão.

A abertura da API01 para objetos arbitrários em memória havia sido detectada pelo autor. A revisão02 acrescenta registro da origem/truth/hash das polarizações, identidade e estado dos IFOs, PSD, grade e ruído; rejeita troca desses objetos e reinjeção nos controles registrados. Isso foi conferido no {link('delta V2','DIFF_ADAPTER_V2.patch')} e no {link('adaptador final','src/synthetic_adapter_v2.py',18)}. A execução01 preservada não é usada como prova automática da API02.

## Evidência conferida

O script independente `review_synthetic_f3.py` executou **212 conferências**, todas aprovadas, em **44 arquivos**: pins do manifesto, contratos, launchers, inputs, logs/recibos, fontes originais e cópias, V1 por bytes, resultados e arrays estritamente sintéticos. Leitura `numpy.load(..., allow_pickle=False)`; nenhum módulo do autor importado ou executado. Uma segunda leitura independente por biblioteca padrão conferiu os **165 arquivos de runtime** pinados em `/opt/lal_env/lib/`: todos os hashes e tamanhos coincidem. Ambos os recibos estão ao lado desta nota em JSON.

| Escopo | RUN_001 | RUN_002 |
|---|---:|---:|
| Controles registrados aprovados | 30 | 38 |
| Gerações nativas registradas | 6 | 6 |
| rc do processo | 0 | 0 |
| EDOM / PE | 0 / 0 | 0 / 0 |
| stderr | vazio | vazio |

São **12 gerações no total**, sob teto agregado32; segunda rodada tinha saldo26. Os contratos precedem os horários registrados de início, os launchers conferem seus próprios pins e inputs antes do processo, e stdout/rc/RESULT concordam. O limite e os hashes foram conferidos no disco; não são apenas frases da nota. As seis construções de injeção das duas revisões correspondem a **três casos distintos** repetidos, com os mesmos arrays. Os controles registrados não são 38 realizações estatísticas independentes.

**Fonte e grade [REAL documental/processual].** A família é IMR `pSEOBNRv4HM_PA`; somente DTau220 se deforma. DTau440, DOmega220 e DOmega440 são zeros nas validações, nos dicionários lidos e nas 12 entradas de trace. “Só-220” se refere à deformação livre; os demais harmônicos GR da família continuam presentes. A {link('fonte copiada','src/pseob_source.py',101)} cria `lal.CreateDict()` a cada geração. O guard da {link('qualificação','qualify_synthetic_v2.py',128)} inspeciona o dicionário entregue à chamada e a grade:8192Hz de geração, Nyquist4096Hz,131073 bins. Dados sintéticos4096Hz,65537 bins, passo0,03125Hz; banda20–1024Hz com32129 bins. Os hashes das cópias pSEOB/temporal e seus originais coincidem.

**GR→RB→GR [REAL no recibo conferido].** O trace é 0 → −0,42461995389788576 → 0 em DTau220; o controle registra retorno GR bit a bit, erro relativo0. O segundo fixture usa −0,5421017699312789. A aritmética beta=ALPHA_FINE_CODATA_2018×sqrt(e), k, F, Q e −x/(1+x) foi refeita localmente a partir do spin sintético registrado e coincide. O fit remanescente e os espectros nativos não foram recalculados pelo revisor: sua proveniência é código pinado + guard + trace + recibo de processo. Não há nova observação natural aqui. A diferença relativa RB/GR e a repetibilidade são controles de implementação, não detecção da TGL.

**Arrays e normalização [REAL independente].** Cada NPZ tem14 arrays, sem objetos serializados. Hashes de PSD, ruído e sinal coincidem. A soma independente `noise + signal` reconstrói **exatamente os 12 hashes de strain injetado** dos recibos. `sqrt((4/T) Σ_det,bin |signal|²/PSD)` dá20 nos três casos de cada rodada. É SNR ótimo de rede do IMR completo, não SNR exclusivo de ringdown. PSD tem unidades strain²/Hz, coeficientes de Fourier strain·s; `df=1/T`. A PSD é analítica no código pinado, positiva e finita na banda e infinita fora. A revisão não importou LAL para gerar uma segunda PSD.

O ruído gaussiano tem quadráticos H1=64401,02866412935 e L1=64082,783819217395 para64258 graus de liberdade, z=0,39897389673 e −0,48875994782. O caso zero contém zeros; H1/L1 não são arrays iguais; GR/RB usam os mesmos ruídos emparelhados. Isso confere a normalização desta realização; não estabelece cobertura ou independência estatística a partir de uma única seed. Os dois NPZ são idênticos por hash. A distância foi reescalada para o mesmo SNR por projeto: esse procedimento de simulação não é ajuste de beta a dados D.

## Entrada, isolamento e limites

[REAL — código/recibos] Configuração fixa SYN_A/SYN_B, PSD analítica, sem entrada de caminho/evento D. Os três priors fixos são zeros numéricos admitidos; priors livres ou valores não zero nesses campos são rejeitados. Os scripts qualificados foram inspecionados estaticamente, incluindo o inventário de chamadas AST. O hook instalado bloqueia aberturas fora da allowlist e eventos Python de rede/processo; o sentinela inexistente é negado antes da leitura. As aberturas `/mnt` permitidas registradas estão somente no piloto, com escritas da rodada correta. A proteção de `bilby.run_sampler` e o fluxo inspecionado não contêm inferência executada.

[OPEN — alcance explícito] O hook é instalado **depois** de imports/leituras fixas de piloto/runtime e abertura do log EDOM; a lista de operações não é uma captura completa do sistema operacional. Não prova ausência universal de syscall nativa não auditada. Os165 pins reforçam identidade do runtime enumerado, sem transformar esse conjunto em auditoria de toda dependência transitiva do SO. Registros Python em memória não resistem a código arbitrário malicioso, e seu ciclo de vida não certifica um driver geral de PE. Esses limites já constam da {link('nota do autor','NOTA_QUALIFICACAO_P0_P2.md',35)} e permanecem nesta aprovação restrita.

[REAL/OPEN] O teste temporal cobre32 cantos físicos do prior, com outros32 excluídos por razão de massas e margem mínima13,602284550666809s. Não é varredura/prova de todos os pontos interiores, vazamento FFT ou tail exato. Dois progenitores sintéticos, três cenários e uma seed não constituem campanha de recuperação, sistemáticas, viés ou cobertura. Não há significância observada, separação D ou potência de teste medida. O custo de geração não estima o custo de PE de14 eventos.

[REAL — preservação] O V1 foi apenas hasheado e comparado à auditoria anterior: bytes e SHA coincidem. Nenhum strain, posterior, centro observado, lista ou hold foi aberto para novo exame. Fontes/rodadas do autor e originais científicos ficaram read-only; todas as saídas desta revisão ficam em `proveniencia`. Zero nova geração nativa, zero PE e zero provedor remoto pelo revisor.

## Identidades finais

| Artefato | SHA256 lido por script |
|---|---|
| Manifesto final do piloto | `{pin('MANIFESTO_PILOTO_SINTETICO.json')}` |
| Contrato02 | `{pin('CONTRATO_P0_P2_V2.json')}` |
| Adaptador02 | `{pin('src/synthetic_adapter_v2.py')}` |
| RESULT02 | `{pin('RUN_002/RESULT.json')}` |
| Arrays02 | `{pin('RUN_002/SYNTHETIC_ARRAYS.npz')}` |
| Errata ao lado | `{pin('ERRATA_ALLOWLIST_RUN002.json')}` |

Os hashes completos, tamanhos, trechos com linhas,212 resultados e inventário de chamadas estão em `REVISAO_PILOTO_SINTETICO_F3.json`; os165 hashes de runtime lidos novamente em `REVISAO_PILOTO_SINTETICO_F3_RUNTIME.json`. Esta revisão encerra a verificação de P0–P2 no recorte fixado; não autoriza P3 nem muda gate ou estatuto físico.
'''
atomic(OUT/'REVISAO_PILOTO_SINTETICO_F3.md',text)
files=[OUT/'REVISAO_PILOTO_SINTETICO_F3.md',J,rp,OUT/'review_synthetic_f3.py',Path(__file__)]
atomic(OUT/'REVISAO_PILOTO_SINTETICO_F3_RECIBO.json',json.dumps({'created_utc':d['finished_utc'],'status':d['review_status'],'artifacts':[metadata(p)[0] for p in files],'open_findings':0,'resolved_findings':['F3-01'],'new_native_generations':0,'PE':0,'D_opened':False,'map_pending':True},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'note':metadata(files[0])[0],'checks':len(d['checks']),'sources':len(d['sources']),'runtime_pins':165,'open_findings':0},ensure_ascii=False))
