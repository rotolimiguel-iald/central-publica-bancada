"""Publish closing review and metadata-only guard refresh, no experiments."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os
OUT=Path(__file__).resolve().parents[1];BASE=OUT.parents[1];ROOT=BASE.parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def raw_save(name,raw):
    p=OUT/name;t=p.with_suffix(p.suffix+'.pending')
    with t.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    assert t.stat().st_size==len(raw)
    os.link(t,p);t.unlink()
def save(name,obj):raw_save(name,(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode())
snapshot=json.loads((OUT/'MAIN_CODE_REVIEW_SNAPSHOT_V3.json').read_bytes())
results=json.loads((OUT/'MAIN_CODE_REVIEW_FIXTURES_V3.json').read_bytes())
previous=json.loads((OUT/'MAIN_CODE_REVIEW_SNAPSHOT_V2.json').read_bytes())
pins=snapshot['files'];guard=BASE/'bis/e2_code/registration_guard.py';guard_sha=sha(guard)
assert guard_sha==pins['bis/e2_code/registration_guard.py']['sha256'],'Guard changed since closing fixtures'
assert results['passed']==20 and results['failed']==0
changed=[n for n,v in pins.items() if sha(BASE/n)!=v['sha256']]
assert all(n=='bis/e2_code/pseob_source.py' for n in changed),changed
unchanged=[Path(n).name for n in pins if n in previous['files'] and pins[n]['sha256']==previous['files'][n]['sha256']]
rows='\n'.join('| '+n+' | `'+v['sha256']+'` |' for n,v in pins.items())
report=f'''# Fechamento da revisão do código principal — v3

[REAL] **20/20 verificações incrementais passaram.** Nos bytes fotografados abaixo, os problemas de recibo agregado e mapa GPS foram corrigidos; a fronteira `load_jobs` recusa quality holds sem resolução válida. Nenhum novo bloqueador foi encontrado nessas fronteiras. Esta revisão limitada não executa nem registra E2 e não encerra ORDEM013BIS.

Snapshot: `MAIN_CODE_REVIEW_SNAPSHOT_V3.json`, SHA256 `{sha(OUT/'MAIN_CODE_REVIEW_SNAPSHOT_V3.json')}`. Resultados: `MAIN_CODE_REVIEW_FIXTURES_V3.json`, SHA256 `{sha(OUT/'MAIN_CODE_REVIEW_FIXTURES_V3.json')}`. Script: `review_main_closing_fixtures_v3.py`, SHA256 `{sha(OUT/'review_main_closing_fixtures_v3.py')}`. Os módulos foram compilados dos bytes fotografados. Fontes alteradas depois das fixtures: {', '.join(changed) or 'nenhuma'}. A nova revisão de pseob_source/contratos temporais pertence a B; este fechamento não aprova automaticamente esses bytes posteriores. Null, fetch e guarda conferidos aqui permanecem iguais ao snapshot.

## Correção ao lado da interpretação da v2

O resultado v2 27/34 permanece preservado. **As quatro sondas de `authorize_event` não demonstravam bypass de lançamento:** essa função classifica identidade/papel; o bloqueio de resolução de qualidade pertence a `load_jobs`/`validate_job_reviews`, chamado na cadeia de lançamento. A afirmação preliminar de ausência desse bloqueio fica retirada. Os novos testes exercitam essa fronteira, com testemunha simulada e verificação real dos hashes, datas e flags da evidência sintética.

- Os quatro eventos sob hold são recusados sem `data_quality_resolution`. Resolução reprovada ou SHA divergente também é recusada. Controle com resolução válida passa. A mesma regra foi testada para job de alocação dinâmica. Nenhum job foi lançado.
- `null_campaign` agora publica `SYNTHETIC_NULL_CAMPAIGN_FAILED` para exceção do deadline anterior ao filho, recibo de célula inconsistente e TimeoutExpired com stdout/stderr em bytes. Fixtures tiveram 0, 1 e 1 chamadas ao stub; nenhum subprocesso científico. Os 25 callbacks de sucesso já haviam sido verificados na v2 e não foram repetidos.
- Downloader: handler de prazo global levanta TimeoutError; cleanup restaura handler e desarma timer; timer preexistente é recusado. Teste determinístico simulado, sem sinal real/socket/rede; não demonstra latência máxima do sistema operacional. Comentário agora distingue timeout de inatividade e prazo global.
- Draft003: `validate_config` passa com duração 16 s e início GPS 1420878129; mapa `event_reference_GPS` coincide com o piloto em 1420878141.2; há exatamente 25 células registráveis. Não é validação de waveform/cobertura numérica do sinal.
- Integração de `derive` em `pe_runner` e publicação de recibo privado foram conferidas estaticamente. Nenhuma PE/conversão numérica foi executada nesta rodada; os dois remanescentes sintéticos do parecer original são evidência anterior distinta.

## Fechamento dos achados anteriores

A v2 já reproduziu as correções de disjunção da janela inteira de injeção contra GPS real pinado; segunda família XPHM somente GR; parâmetros Planck18 iguais ao INPUT nomeado; transferência truncada/tamanho/checksum ausente; recipe/allocation/jobs SHA e revalidação antes da promoção. Essas fixtures não foram repetidas indiscriminadamente. Arquivos idênticos entre snapshots v2/v3: {', '.join(unchanged)}.

As conclusões científicas do parecer original permanecem condicionais: composição balanceada fixa nos matched nulls difere da composição multinomial da rota IV; ceil(N90) herdado do forecast sem nuisance não se torna N90 calibrado com nuisance. As larguras e seeds são INPUTs congelados; covariância local não vira covariância física. Nenhum novo nulo/MC foi calculado aqui. O censo continua ausência no escopo, não ausência universal de publicação; nove conhecidos ficam em calibração, 14 têm escopo e quatro exigem resolução de qualidade.

## Limites para o freeze

Montagem final deve conferir próprias árvores, extra_code_roots E7/E4, pins, runtime, orçamento e testemunha real. Draft003 não é registro. Integração de guarda real, lançamento, monitoramento de deadline e resultados de PE não foram executados por este revisor. Fatores de Bayes físicos, seleção e covariância calibrada continuam OPEN.

E7 é obra deste autor e precisa do fechamento independente de Russell. A v3 corrigiu F1/F2 e passou 46 testes do autor, mas isso não é aprovação independente. O principal autorizou o montador a rehashar explicitamente a guarda final antes de E2, conservando a proveniência do fragmento v3 e a revisão correspondente. O pin do fragmento v3 tornou-se histórico durante as alterações concorrentes; não declarar que coincide automaticamente com a guarda final. Não alterar registro publicado para fazê-lo passar. Não foi necessário emitir fragmento v3.1: integração final permanece do principal.

Nenhum arquivo anterior foi sobrescrito; nenhuma rede, posterior real, strain, PE, waveform ou MC. Nenhuma leitura C1 foi escolhida por este revisor. NOT_FALSIFIED não significa CONFIRMED.

## Pins das fontes do fechamento

| Fonte relativa a ORDEM_013_RINGDOWN | SHA256 |
|---|---|
{rows}
'''
raw_save('MAIN_CODE_REVIEW_CLOSING_V3.md',report.encode())
print(json.dumps(dict(closing_report_sha256=sha(OUT/'MAIN_CODE_REVIEW_CLOSING_V3.md'),changed_after_snapshot=changed),indent=2))
