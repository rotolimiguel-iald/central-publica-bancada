"""Publish E3.3 and TEST wall notes from independently reviewed stage evidence."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, json, hashlib, os
B=Path(__file__).resolve().parents[1];R=B.parent;D=R/'TUNEL/DO_CHATGPT'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_bytes())
def new(p,s):
    raw=s.encode();tmp=p.with_name(p.name+'.pending')
    with tmp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    if tmp.stat().st_size!=len(raw):raise OSError('Short write')
    os.link(tmp,p);tmp.unlink()
def checked(ref):
    p=(R/ref['path']).resolve()
    if not p.is_relative_to(R) or sha(p)!=ref['sha256']:raise ValueError('Stage reference differs')
    return p
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--calibration-stage',type=Path,required=True)
    ap.add_argument('--test-stage',type=Path,required=True);a=ap.parse_args()
    refs=[];sources={}
    for stage,p in [('E3.3',a.calibration_stage),('TEST',a.test_stage)]:
        d=load(p);artifact=checked(d['artifact']);review=checked(d['review']);v=load(review)
        if (d['schema']!='E6_REVIEWED_STAGE_V2' or d['stage']!=stage or d['outcome'] not in ('PARTIAL','BLOCKED','UNAVAILABLE')
            or v['status']!='ACCEPTED_FOR_E6_MAPPING' or v['blocking_findings'] or v['bindings']!=d['bindings']
            or v['artifact_sha256']!=d['artifact']['sha256'] or v['timeline']!=d['timeline']
            or d['registration_sha256']!=sha(B/'RINGDOWN_5SIGMA_V1.json')):raise ValueError('Stage not independently reviewed')
        source=load(artifact)
        if source['status']!='NO_EXECUTION' or source['test_posterior_available'] is not False:raise ValueError('Not a no-test wall')
        sources[stage]=source;refs += [p,artifact,review]
    test=load(a.test_stage)
    if checked(test['predecessor'])!=a.calibration_stage.resolve():raise ValueError('Stage chain differs')
    rows=sources['TEST']['rows']
    if len(rows)!=180 or any(x['summary']!={'test_data_present':False,'verdict':'AWAITING_DATA'} or x['gate']['color']!='red'
        or any(v is not None for v in x['metrics'].values()) for x in rows):raise ValueError('Wall matrix has unexpected physical result')
    opening=sha(D/'ENTREGA_013BIS_ABERTURA_operador.md')
    budget=B/'ORCAMENTO_40H.json';now=datetime.now(timezone.utc)
    if now>=datetime.fromisoformat(load(budget)['wall_accounting']['finalization_stop_utc']):raise TimeoutError('Reserve expired')
    b4=D/'ENTREGA_013BIS_B4_calibracao_e_cegos.md';td=D/'ENTREGA_013BIS_TESTE_O4_cegos.md'
    fiche=B/'REAPROVEITAMENTO_AMPLIACAO_B4_TESTE.md';manifest=B/'bis/B4_TEST_DELIVERY_MANIFEST.json'
    if any(p.exists() or p.with_name(p.name+'.pending').exists() for p in (b4,td,fiche,manifest)):raise FileExistsError('Existing delivery retained')
    new(fiche,'[REAL — reaproveitamento B4/TESTE, parede sem execução observacional]\n\n'
        'Reutilizados E2, orçamento revisado, portão E0, diagnóstico nativo e revisão. Novos: declarações cronológicas de parede '
        'e matriz de estado sem dados, não novos resultados físicos. PAGO documental; NÃO PAGO calibração, novas PE e teste observacional. '
        f'N/A — sem Lean. Abertura `{opening}`.\n')
    shared=[f'Abertura `{opening}`; ficha `{sha(fiche)}`; orçamento `{sha(budget)}`.','',
        'A alocação foi registrada antes destas declarações. Há saldo de tempo; a causa de não executar foi a parede do instrumento '
        'documentada em B3, não falta de autorização do operador. Nenhuma conclusão de impossibilidade geral da PE é inferida.','',
        'O censo conserva14 candidatas documentais,10 sem hold e4 com hold. Pesos esperados estão em B3/orçamento. '
        'Ausência de publicação encontrada é limitada ao escopo do censo; não certifica cegueira universal. '
        'Na execução desta bancada não houve PE de candidata, download de strain de teste ou descegamento.','',
        'Custo por posterior convergido permanece null. Sigma(c), sigma_sys(df), cobertura e transferência browniana permanecem OPEN. '
        'Os pisos /5 e /15 do220 são INPUTs transportados do portão; não são erros calibrados. '
        'Pisos de outro canal não são reutilizados como calibração440 ou de largura populacional.','',
        'Registros NO_EXECUTION têm a hora real da declaração e a razão, sem fabricar início/fim de experimento. '
        'As revisões vinculam exatamente fontes, unidades, ponteiros e predecessores. Hash é vínculo de bytes, não prova independente do relógio físico.','',
        'Reprodução: `bis/e3_wall_stages/wall_stage_adapter.py prepare/finalize` com os argumentos de autorização/revisão dos recibos. '
        'Esses são localizadores abreviados; as autorizações, comandos e manifests definem os bytes e o destino. '
        'Não executar o piloto antigo nem sobrescrever saídas. N/A — sem Lean.','',
        'Tentativas falhas foram preservadas: piloto e diagnóstico nativo de B3; versões de preparação/revisão dos adaptadores e do quadro. '
        'Nenhum resultado de natureza foi produzido por esses adaptadores.','']
    refs += [budget,fiche,B/'bis/B3_DELIVERY_MANIFEST.json']
    files={p.relative_to(R).as_posix():{'sha256':sha(p),'bytes':p.stat().st_size} for p in refs}
    links=[f'- [{p}](<{(R/p).as_posix()}>) — `{x["sha256"]}` ({x["bytes"]} B).' for p,x in files.items()]
    new(b4,'\n'.join(['[REAL — B4 fechada como parede técnica; calibração e novas PE NÃO PAGAS]','',
        '# B4 — calibração possível e eventos cegos','',
        '| Critério E3.3 | Estado |','|---|---|',
        '| Matriz RG/TGL, duas famílias, massa/spin livres | NÃO PAGA: nenhum novo job lançado após a parede do piloto. |',
        '| c(SNR), sigma_sys, cobertura e440 | NÃO PAGOS: nenhuma amostra válida de recuperação nova. |',
        '| Custo, orçamento e critério de parada | PAGOS documentalmente: zero novos jobs, reserva final limitada, parede preservada. |',
        '| PE cega | NÃO PAGA: nenhuma candidata admitida ou analisada. |','',*shared,*links])+'\n')
    new(td,'\n'.join(['[REAL — estado AWAITING_DATA registrado; TESTE observacional não executado]','',
        '# TESTE O4 cego — estado sob o registro','',
        '**AWAITING_DATA nas dez leituras.** Não há posterior novo de teste disponível nesta execução; gate vermelho. '
        'z físico, lnB físico e correção/sigma física são null. A ausência de teste não é NOT_FALSIFIED.','',
        'A matriz180 cobre3 rotas×10 leituras×6 grupos. Os cenários futuros também permanecem AWAITING_DATA. '
        'Isso paga a declaração e a verificação do estado, não a execução de um teste observacional. '
        'Os resultados dos33 catálogos já públicos continuam calibração NÃO-CEGA e não são promovidos a teste.','',
        '| Critério | Estado |','|---|---|',
        '| Registro e ordem temporal | PAGOS documentalmente, com revisão dos adaptadores. |',
        '| Novos dados cegos e estatística física | NÃO PAGOS; número de eventos acrescentados=0. |',
        '| Gate sistemático | Vermelho/OPEN: condições físicas não calibradas. |','',*shared,*links])+'\n')
    files.update({p.relative_to(R).as_posix():{'sha256':sha(p),'bytes':p.stat().st_size} for p in (b4,td)})
    new(manifest,json.dumps(dict(status='B4_TEST_WALL_DELIVERED_NO_OBSERVATIONAL_TEST',created_utc=now.isoformat(),
        files=files,opening_sha256=opening,script_sha256=sha(Path(__file__))),ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(B4_sha256=sha(b4),TEST_sha256=sha(td),manifest_sha256=sha(manifest))))
if __name__=='__main__':main()
