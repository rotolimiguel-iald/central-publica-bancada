"""Freeze the documentary review using measured local receipts; no extra science."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os

HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]
ROOT=BASE.parent
P=BASE/'bis/e3_blind_prepare'


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def publish(name,raw):
    if len(raw)>25_000_000:raise ValueError('Size cap')
    p=HERE/name;temp=p.with_name(p.name+'.pending')
    with temp.open('xb') as f:f.write(raw)
    if temp.stat().st_size!=len(raw):raise ValueError('Short write')
    os.link(temp,p);temp.unlink()


def main():
    data=json.loads((HERE/'AUDIT_RESULTS_V1.json').read_bytes())
    phases=json.loads((HERE/'PHASE_CONTRACT_RESULTS_V1.json').read_bytes())
    source=json.loads((HERE/'SOURCE_SNAPSHOT_V1.json').read_bytes())
    for name,digest in source['source_pins_relative_to_Chatgpt'].items():
        if sha(ROOT/name)!=digest:raise ValueError('Source changed: '+name)
    candidates=json.loads((P/'CANDIDATES_SORTED.json').read_bytes())
    if not all(r['publication_metadata_review']['review_passed'] is True for r in candidates['candidates']):
        raise ValueError('Current publication review not passed')
    if data['metadata_passed']!=data['metadata_checks'] or data['scalar_passed']!=data['scalar_checks'] or phases['total']!=phases['passed']:
        raise ValueError('Unresolved audit check failure; preserve receipts')
    held=', '.join('`'+e+'`' for e in data['held_events'])
    report=f'''# Revisão independente — prontidão documental E3 cego, V1

**ACCEPTED_DOCUMENTARY_ARITHMETIC_ONLY_WITH_REUSE_ADVISORY. Não é admissão, alocação, autorização de download ou PE.** Artefatos atuais consistentes com as fontes pinadas; há uma correção de comparação de datas a fazer numa nova versão do construtor antes de reutilizá-lo. Originais e pareceres anteriores preservados.

## Resultado e alcance

[REAL — metadados locais e aritmética finita] Conferidos **{data['metadata_passed']}/{data['metadata_checks']} checks documentais**, **{data['scalar_passed']}/{data['scalar_checks']} comparações escalares** e **{phases['passed']}/{phases['total']} fixtures da sequência de hashes**. Nenhum produtor importado/executado; não houve rede, download, strain, posterior, waveform, bootstrap, refit, RNG, seed real ou PE. As fixtures usam cópia byte a byte do guard em raiz fictícia própria. Não foi chamada a ativação real E2 nem o launcher.

Manifesto, adendo de duas fases e todos os pins de fonte foram conferidos e relidos ao fechar. O guard conferido coincide com `own_code_tree_sha256` do E2. A validação dos metadados não demonstra validade física dos arquivos de strain nem completude universal do censo de publicações.

## As 14 candidatas e os holds

[REAL] Lista exata, sem perda/duplicação: **14 candidatas; 10 sem hold e quatro com hold**. Ordenação por SNR E0 decrescente, desempate por ID, preservada. CSV, linha, valor SNR, versão e descritor de origem conferidos. Não se usou largura de posterior, peso calculado ou custo para selecionar/admitir eventos.

Holds preservados: {held}. As 14 reviews de publicação têm hash/descritor consistentes com o índice R, `review_passed=true` e timestamps conferidos como instantes com timezone após E2. Não equivalem a resolução DQ. `admission=null` e `blindness_certified_here=false` continuam nos 14 itens.

Os cinco alvos de inspeção documental são exatamente os cinco primeiros **sem hold**. Isso explica `unheld:5` no resumo do builder; o total sem hold é 10, já dito na documentação. As nove candidatas restantes continuam na lista; os metadados remotos anteriores dos cinco não certificam as outras nove. “Não encontrado no escopo” não vira ausência universal de publicação.

## Pesos esperados: quatro objetos distintos

[INPUT — modelo empírico de planejamento] Para x=lnρ, μ=a+bx e dispersão residual s de lnσ:

- mediana condicional de σ: exp(μ);
- proxy inverso da mediana ao quadrado: exp(−2μ);
- esperança lognormal de informação: E[1/σ²]=exp(−2μ+2s²);
- inverso do quadrado da média de σ: 1/E[σ]²=exp(−2μ−s²), que não é nenhum dos dois pesos anteriores.

A propagação usa a matriz completa: Var(μ)=[1,x] Cov(a,b) [1,x]ᵀ, incluindo os termos cruzados. Os IC95 publicados transformam μ±t·sqrt(Var μ), **com s fixo**. A integração exp(2 Var μ) adicional é aproximação gaussiana para os coeficientes, separada do IC t; não é posterior preditivo exato nem incerteza de s integrada.

[REAL — auditoria independente] Usei Decimal com 80 dígitos, produto vetor–matriz–vetor e transformações independentes sobre os coeficientes pinados, sem chamar `project` do produtor. Foram conferidos todos os 28 pares candidata×fit, incluindo dispersão residual 5/50/95, intervalos, proxy, esperança e integração gaussiana. Maior erro relativo **{data['max_scalar_relative_error']:.17g}**, tolerância fixada antes **{data['relative_tolerance']:.1e}**. Covariâncias positivas e preservadas; grades bootstrap antigas preservadas sem interpolação nem draws novos.

Exemplo da primeira candidata, mesma fonte de SNR:

| Fit | Proxy 1/mediana² | E[1/σ²] | 1/E[σ]² | E[I]/proxy |
|---|---:|---:|---:|---:|
'''
    for r in data['top_event_examples']:
        report+=f"| {r['population']} | {r['proxy']:.8f} | {r['lognormal_expectation']:.8f} | {r['inverse_square_mean_sigma']:.8f} | {r['expectation_proxy_ratio']:.8f} |\n"
    report+=f'''
Fit31 e fit33 são populações sobrepostas, não replicações independentes. Três extrapolações no fit31 (ρ<12,9): {', '.join('`'+e+'`' for e in data['domain_extrapolations']['GWTC5_31'])}; nenhuma no fit33. As flags estão corretas e os eventos não foram descartados por esse motivo.

[OPEN] Os intervalos não incluem erro de SNR, incerteza de s, seleção, mudança de priors/família, cobertura ou transferência para a PE própria. SNR de rede/preferred pode incluir Virgo; não é automaticamente SNR H1/L1 nem de ringdown. Coeficientes compartilhados correlacionam a incerteza entre candidatas; não somar erros como independentes ou usar os fits31/33 como duas evidências. `information_for_actual_new_PE` permanece null nas 28 linhas. Não há ganho por hora, informação observada ou potência física pagos.

## Datas: correção antes de reutilizar o construtor

**R1 [P2, alcance futuro]** `build_readiness.py` compara `reg['registered_utc'] <= review['reviewed_utc'] <= now.isoformat()` como strings. Essa relação não preserva ordem cronológica entre fusos e não exige timezone. Fixture finita: now=`2026-09-22T10:00:00+00:00`; review=`2026-09-22T09:30:00-02:00` passa lexicalmente, mas é 11:30 UTC, portanto futura. Parsear timestamps aware e comparar instantes normalizados em nova versão, com negativos futuro/naive/malformed.

Isso **não invalida as 14 datas desta entrega**: a revisão independente converteu todas para UTC e confirmou E2 ≤ review ≤ agora. O builder é documental, não guard de admissão; nenhuma autorização foi concedida pelo defeito. Não editar retrospectivamente o artefato ou manifesto publicado.

## Sequência A→B e limites do guard

[REAL — código e fixtures locais] O adendo descreve corretamente que `ORCAMENTO_40H.json` é o **conteúdo completo ativo** no caminho fixado pelo E2, não um arquivo apontador nem descoberta automática de versões. A proposta de dois estágios exige decisão explícita do principal de tratar esse slot como projeção substituível de versões arquivadas imutáveis. Se o slot também for imutável para sempre, a transição não cabe no contrato atual; o adendo não resolve isso por autorização implícita.

Fase A: configuração imutável downloads-only (`jobs={{}}`, schema E2_PE_JOBS_V2), hash da configuração → orçamento A completo/versionado → mesmos bytes no slot ativo → testemunha A do orçamento → validação antes de baixar. Jobs estáticos permanecem. MD5 do provedor não gera SHA256 local; esse hash só é conhecido/verificado nos recibos após streaming/integridade. Nenhum SHA ausente foi inventado.

Fase B: configuração sucessora imutável com hashes locais, priors/janelas/reviews completos; orçamento/testemunha novos e referência documental à fase anterior. Preservar A/config/testemunha/recibos. Parar downloads e controladores dependentes durante a troca; sem execução na janela entre troca do slot e testemunha nova. Revalidar relógio global e configuração antes de cada lançamento. A ordem e o prazo não reiniciam.

As nove fixtures com a função exata do guard e testemunhas reais **dentro da raiz fictícia** confirmaram: ausência da testemunha A ou B é recusada; downloads-only preserva job estático; versões A permanecem idênticas; B não herda automaticamente downloads A. Campo extra `lineage_INPUT` falso não é rejeitado pelo guard: a cadeia histórica é responsabilidade da revisão, não gate core. O guard verifica a versão corrente e seus pins.

**Limitação de hold confirmada:** receita downloads-only para candidata fictícia held atravessa `load_authorized_configuration`; `authorize_event` também só classifica elegibilidade/censo. Não há job dinâmico ao qual aplicar `validate_job_reviews`. Isso não libera held real: o principal deve restringir fase A às candidatas autorizáveis sem hold/reviews pendentes. Ao existir job, review de publicação ausente foi recusada. Nenhum fetch foi chamado na fixture. Não apresentar essa diferença como nova proteção core.

O helper antigo continua inadequado às duas fases: exige jobs não vazios, fixa downloads vazio, exige piloto aceito e recusa slot já existente. Esta revisão não o corrige nem reutiliza; preserva o parecer anterior. Um sucessor para custo parcial/emenda do piloto e download-only precisa de revisão própria. O fracasso do piloto informado pelo principal não oferece custo convergido: gasto observado é gasto; custo por PE convergida e ganho/hora seguem OPEN. Não é motivo para suspender a ordem nem para preencher custos fictícios.

## Metadados não são dados admitidos

[REAL documental] {data['provider_file_records']} registros de arquivo conferidos contra as linhas MD5 locais arquivadas e mapeamento de licença pinado. `local_sha256`, `expected_bytes` e `maximum_bytes` dos fragmentos permanecem null; checksums do provedor não foram verificados contra strain. Templates sem schema de jobs, incompletos e explicitamente não executáveis. Não há alocação nem publicação ativa aqui.

As flags no instante do evento e os blocos de 256 s são apenas sondagens documentais. A futura análise exige cobertura integral da janela, finitude, PSD positiva/adequada e corte anterior ao início de análise; passing de timeline não remove hold. Priors, tempos, banda/Nyquist e suporte em toda a região relevante precisam de revisão própria; não transportar 16 s/20 Hz ou medianas GR como configuração certificada. Nenhuma licença foi reavaliada juridicamente nem disponibilidade remota reconfirmada por esta auditoria.

## Pins e custódia desta entrega

- Manifesto produtor: `{sha(P/'MANIFEST.json')}`.
- Expected information: `{sha(P/'EXPECTED_INFORMATION.json')}`.
- Builder: `{sha(P/'build_readiness.py')}`.
- Adendo da sequência: `{sha(P/'TWO_PHASE_HASH_SEQUENCE.md')}`.
- Guard congelado: `{phases['frozen_guard_sha256']}`.
- Recibos próprios: `AUDIT_RESULTS_V1.json`, `PHASE_CONTRACT_RESULTS_V1.json`, `SOURCE_SNAPSHOT_V1.json`; cópia byte a byte em `snapshot_001/`.

Originais, E2, parecer de alocação, E4/E7 e E6 intactos. E6 continua sem execução, E7 sem extração. Resultado limitado à revisão documental/aritmética e ao contrato em fixtures fictícias; nenhuma candidata admitida, alocação selecionada ou ordem concluída.
'''
    publish('INDEPENDENT_BLIND_READINESS_REVIEW_V1.md',report.encode())
    artifacts={p.name:dict(sha256=sha(p),bytes=p.stat().st_size) for p in HERE.iterdir() if p.is_file() and not p.name.endswith('.pending')}
    receipt=dict(status='ACCEPTED_DOCUMENTARY_ARITHMETIC_ONLY_WITH_REUSE_ADVISORY',created_utc=datetime.now(timezone.utc).isoformat(),
        reviewed_manifest_sha256=sha(P/'MANIFEST.json'),artifacts=artifacts,
        metadata_checks=data['metadata_passed'],scalar_checks=data['scalar_passed'],phase_fixtures=phases['passed'],
        current_artifact_blockers=[],before_builder_reuse=['R1_AWARE_CHRONOLOGY_NOT_LEXICOGRAPHIC'],
        admission=False,actual_allocation=False,E6_executed=False,E7_extracted=False,order_completed=False)
    publish('REVIEW_RECEIPT_V1.json',(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n').encode())
    print(json.dumps(dict(status=receipt['status'],report_sha256=sha(HERE/'INDEPENDENT_BLIND_READINESS_REVIEW_V1.md'),
        receipt_sha256=sha(HERE/'REVIEW_RECEIPT_V1.json'))))


if __name__=='__main__':main()
