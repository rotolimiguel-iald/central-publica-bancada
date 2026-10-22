"""Deliver reviewed E6/E7 with physical limitations and exact artifact hashes."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, os, math
B=Path(__file__).resolve().parents[1];R=B.parent;D=R/'TUNEL/DO_CHATGPT'
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for x in iter(lambda:f.read(1048576),b''):h.update(x)
    return h.hexdigest()
def load(p):
    def pairs(items):
        out={}
        for k,v in items:
            if k in out:raise ValueError('Duplicate JSON key')
            out[k]=v
        return out
    def number(s):
        v=float(s)
        if not math.isfinite(v):raise ValueError('Nonfinite JSON number')
        return v
    def invalid(s):raise ValueError('Invalid JSON constant')
    return json.loads(Path(p).read_bytes(),object_pairs_hook=pairs,parse_float=number,parse_constant=invalid)
def new(p,s):
    raw=s.encode();tmp=p.with_name(p.name+'.pending')
    with tmp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    if tmp.stat().st_size!=len(raw):raise OSError('Short write')
    os.link(tmp,p);tmp.unlink()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--e6-result',type=Path,required=True)
    ap.add_argument('--e6-review',type=Path,required=True);ap.add_argument('--e7-review',type=Path,required=True);a=ap.parse_args()
    p7=B/'bis/E7_FULLSAMPLE_RESULT_V1.json';e7=load(p7);e6=load(a.e6_result)
    for review,result,key in [(a.e6_review,a.e6_result,'e6_result_sha256'),(a.e7_review,p7,'e7_result_sha256')]:
        v=load(review)
        if v.get('approved') is not True or v.get(key)!=sha(result):raise ValueError('Independent result review missing')
    execution=load(B/'bis/E7_FINAL_EXECUTION_V1.json')
    if execution['failure'] is not None or e7['test_events_added']!=0 or e7['calibration_events']!=33:raise ValueError('E7 scope mismatch')
    if len(e6['cells'])!=180 or len(e7['matrix'])!=20:raise ValueError('Required coverage absent')
    if any(x['verdict']!='AWAITING_DATA' or x['z_physical'] is not None or x['lnB'] is not None or x['correction_over_sigma_physical'] is not None for x in e7['matrix']) or e7['z_physical'] is not None or e7['lnB'] is not None:raise ValueError('Unexpected physical result')
    payload=B/'cache/POSTERIORES_PSEOB_GWTC5_33_013BIS_V1.json';authpath=B/'bis/E7_FINAL_AUTHORIZATION_V1.json';auth=load(authpath)
    if execution['status']!='E7_EXECUTED_NO_PHYSICAL_TEST' or execution['authorization_sha256']!=sha(authpath):raise ValueError('Execution authorization differs')
    for p in (p7,payload):
        if execution['products'][p.name]['sha256']!=sha(p) or execution['products'][p.name]['bytes']!=p.stat().st_size:raise ValueError('Executed product differs')
    if auth['registration_sha256']!=sha(B/'RINGDOWN_5SIGMA_V1.json') or auth['allocation_sha256']!=sha(B/'ORCAMENTO_40H.json') or auth['e6_result_sha256']!=sha(a.e6_result) or auth['e6_review_sha256']!=sha(a.e6_review):raise ValueError('Authorization parents differ')
    if e7['posterior_sha256']!=sha(payload) or e7['authorization_sha256']!=sha(authpath):raise ValueError('Consumer transport differs')
    cmds=execution['commands']
    if len(cmds)!=2 or any(c['returncode']!=0 or c['direct_child_reaped'] is not True or c['error'] is not None for c in cmds):raise ValueError('Execution not completed as claimed')
    deadline=min(datetime.fromisoformat(load(B/'bis/PART_B_BUDGET_START.json')['hard_deadline_utc']),datetime.fromisoformat(load(B/'ORCAMENTO_40H.json')['wall_accounting']['finalization_stop_utc']))
    if not datetime.fromisoformat(auth['registered_utc'])<=datetime.fromisoformat(execution['started_utc'])<=datetime.fromisoformat(execution['finished_utc'])<deadline:raise ValueError('Execution chronology exceeds envelope')
    readings=load(B/'RINGDOWN_5SIGMA_V1.json')['readings']
    expected={(route,reading,group) for route in ('TAU220_POPULATION','TAU440_FIXED_SOURCE_FISHER','DF220_POPULATION_WIDTH_IV') for reading in readings for group in ('O4_HOJE','O4_CEGO','O4C_GWTC6','O5_BANDA','ET','CE')}
    if {(r['route'],r['reading'],r['data_group']) for r in e6['cells']}!=expected:raise ValueError('E6 coverage differs')
    if {(r['reading'],r['mode_variant']) for r in e7['matrix']}!={(r,m) for r in readings for m in ('220_only','220_plus_440_INPUT')}:raise ValueError('E7 coverage differs')
    opening=sha(D/'ENTREGA_013BIS_ABERTURA_operador.md');now=datetime.now(timezone.utc)
    if now>=datetime.fromisoformat(load(B/'ORCAMENTO_40H.json')['wall_accounting']['finalization_stop_utc']):raise TimeoutError('Reserve expired')
    fiche=B/'REAPROVEITAMENTO_AMPLIACAO_B5.md';delivery=D/'ENTREGA_013BIS_B5_quadro_e_modulo.md';manifest=B/'bis/B5_DELIVERY_MANIFEST.json'
    if any(p.exists() or p.with_name(p.name+'.pending').exists() for p in (fiche,delivery,manifest)):raise FileExistsError('Keep prior delivery')
    new(fiche,'[REAL — B5; quadro condicional e módulo de amostras, sem teste físico]\n\n'
        'Reutilizados E0/E1/E2, resultados E4/E5 e paredes E3/TEST revisadas. Novos: montagem E6 por ponteiros, '
        'extração das cinco colunas pareadas completas e execução do consumidor NumPy. PAGO transporte/diagnóstico descrito; '
        'NÃO PAGO calibração física, modelo restrito normalizado e ponte cega. N/A — sem Lean. '
        f'Abertura `{opening}`.\n')
    samples=sum(x['N'] for x in e7['fullsample_diagnostics']['events'])
    payload=B/'cache/POSTERIORES_PSEOB_GWTC5_33_013BIS_V1.json'
    rows=e7['matrix']
    lines=['[REAL — B5 entregue: quadro condicional e módulo executado/revisado; inferência física NÃO PAGA]','',
        '# B5 — quadro de alcance e módulo para incorporação','',
        f'Abertura `{opening}`; ficha `{sha(fiche)}`.','',
        '| Critério | PAGO / limite |','|---|---|',
        '| E6 | PAGO:180 células,3 rotas×10 leituras×6 grupos, cenários e ponteiros de origem conferidos. |',
        '| E7 extração | PAGO:33 produtos arquivados, cinco campos pareados completos, priors com estatuto, fontes/tar/runtime e hashes. |',
        '| E7 consumidor | PAGO: execução NumPy, guardas, descritores condicionais e matriz de estado. |',
        '| E7 inferência física | NÃO PAGA: seleção, likelihood restrita normalizada, covariância física e adaptador de liberação cega. |',
        '| Incorporação no um.py | Não realizada pela bancada; responsabilidade da gerência após auditoria. |','',
        f'Foram transportadas {samples:,} linhas de amostras em33 produtos de calibração, preservando a ordem comum de '
        'delta_f220, delta_tau220, Mf no referencial do detector, spin final e redshift. Sem thinning. '
        'Pesos são os iguais armazenados no produto de origem; isso não demonstra independência das amostras nem uniformidade dos priors derivados. '
        'O JSON completo está em cache, separado do consumidor; os quantis não substituem amostras.','',
        'A fronteira de dependências permanece explícita: extrator com h5py; consumidor com NumPy como única dependência científica. '
        'A guarda externa confere o runtime e os bytes registrados. Os dois módulos congelados são entregues nos seus caminhos registrados, '
        'sem copiar um executável para outro lugar e alegar que o pin antigo aprova esse novo local.','',
        '## Matriz de estado','',
        '| Leitura | Variante | Estatuto | Veredito | Gate |','|---|---|---|---|---|']
    for row in rows:lines.append(f'| {row["reading"]} | {row["mode_variant"]} | {row["statute"]} | {row["verdict"]} | {row["systematic_gate"]} |')
    lines+=['','Nenhum evento de teste foi acrescentado. A variante220+440 mantém aviso de posterior440/QNM exato não extraído neste contrato. '
        'Amostras do catálogo público são calibração NÃO-CEGA; não pagam a ampliação por teste novo. '
        'Todos os números físicos de significância continuam null.','',
        '## Quadro e interpretação','',
        'O4 hoje é cenário derivado de calibração arquivada; O4 cego registra a ausência de novos posteriores. '
        'O4c/GWTC-6, O5, ET e CE conservam somente projeções condicionais, com dados futuros AWAITING_DATA. '
        'As taxas/IC, ganhos de SNR, âncoras de fonte e limites de sistemática não são combinados em promessa de calendário. '
        'O quadro separa informação, contagem e equivalentes; não transporta piso220 para440 ou para variância de frequência. '
        'Correção/sigma condicional é identificada como tal; gate vermelho não permite z físico.','',
        '## Verificação, execução e limites','',
        f'Parede observada da execução E7={execution["wall_seconds"]:.6f}s, dentro da reserva; não inclui novamente o tempo dos estudos anteriores. '
        'Os comandos exatos de extração/consumo estão em E7_FINAL_EXECUTION_V1.json, e a autorização está pinada antes dos processos. '
        'O processo filho direto foi aguardado; não se declara medição independente de ausência de uma árvore de processos.','',
        'A revisão E6 conferiu o transporte de valores/ponteiros e os estados. A revisão E7 tem seu escopo no parecer vinculado; '
        'essa aprovação de custódia/aritmética não é certificação da teoria pela natureza. As fixtures anteriores incluem recusas de '
        'hashes, formatos, cronologia e dados ausentes; as falhas históricas e suas versões permanecem.','',
        'Comandos/localizadores: E6 `generate_reach_table.py --execute --authorization ... --authorization-sha256 ...`; '
        'E7 `refeito/activate_e7_final_v2_013bis.py --e6-result ... --e6-review ... --e6-review-sha256 ...`. '
        'As reticências são abreviação; usar os comandos integrais pinados nos recibos para reprodução em destino isolado. '
        'N/A — sem Lean. Nenhum canônico foi executado ou alterado por estes scripts.','',
        '## Arquivos e hashes','']
    refs=[a.e6_result,a.e6_result.with_name('QUADRO_DE_ALCANCE_V1.md'),a.e6_result.with_name('RESULT_RECEIPT.json'),a.e6_review,
        a.e7_review,p7,payload,B/'bis/E7_FINAL_EXECUTION_V1.json',B/'bis/E7_FINAL_AUTHORIZATION_V1.json',
        B/'bis/e7_prepare/producer/extrai_posteriores_pseob.py',B/'bis/e7_prepare/producer/tgl_ringdown_ampliacao.py',
        B/'bis/e7_prepare/EXTRACTION_PLAN.json',B/'bis/e3_pilot_review/E7_ORCHESTRATION_V2_CLOSING_REVIEW.json',
        B/'bis/e6_review/E6_FOCUSED_CLOSING_V3_RECEIPT.json',fiche]
    files={p.relative_to(R).as_posix():dict(sha256=sha(p),bytes=p.stat().st_size) for p in refs}
    for p,v in files.items():lines.append(f'- [{p}](<{(R/p).as_posix()}>) — `{v["sha256"]}` ({v["bytes"]} B).')
    new(delivery,'\n'.join(lines)+'\n')
    files[delivery.relative_to(R).as_posix()]=dict(sha256=sha(delivery),bytes=delivery.stat().st_size)
    new(manifest,json.dumps(dict(status='B5_DELIVERED_CONDITIONAL_AND_FAIL_CLOSED',created_utc=now.isoformat(),files=files,
        opening_sha256=opening,full_paired_samples=samples,script_sha256=sha(Path(__file__))),ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(delivery_sha256=sha(delivery),manifest_sha256=sha(manifest),samples=samples)))
if __name__=='__main__':main()
