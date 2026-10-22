"""Close only T1/T2/C6-R1 from frozen data; never execute production writers."""
import ast,copy,csv,hashlib,json,math,sys
from datetime import datetime,timezone
from pathlib import Path

R=Path(__file__).resolve().parents[2]
def need(ok,message):
    if not ok:raise ValueError(message)
def get(name):return json.loads((R/name).read_bytes())
def sha(path):
    with path.open('rb') as handle:return hashlib.file_digest(handle,'sha256').hexdigest()
def write_new(path,raw):
    need(not path.exists(),'Review output exists')
    tmp=path.with_name(path.name+'.tmp')
    with tmp.open('xb') as handle:handle.write(raw)
    need(tmp.read_bytes()==raw and len(raw)>0,'Review bytes differ')
    need(not path.exists(),'Review output appeared');tmp.rename(path)

report=R/'bis/F2_C6_CLOSING_REVIEW.md'
receipt=R/'bis/c1_review/f2_c6_closing_results.json'
need(not report.exists() and not receipt.exists(),'Review output exists')
need(sys.flags.optimize==1,'Run this audit under -O')
old=get('bis/F2_ALL_READING_TABLES.json');table=get('bis/F2_ALL_READING_TABLES_v2.json')
c0=get('C6_ADENDO_REALIZADO.json');c6=get('C6_ADENDO_REALIZADO_v2.json')
previous=get('bis/c1_review/f2_tables_c6_results.json')
names=set(previous['input_hashes'])|set(table['source_sha256'])|set(c6['source_sha256'])|{
    'bis/F2_ALL_READING_TABLES_v2.json','bis/F2_ALL_READING_TABLES_v2.csv',
    'C6_ADENDO_REALIZADO_v2.json','REAPROVEITAMENTO_C6.md','REAPROVEITAMENTO_C6_v2.md',
    'refeito/summarize_f2_tables_013bis_v2.py','refeito/record_c6pre_013bis_v2.py',
    'bis/F2_TABLES_C6PRE_REVIEW.md','bis/c1_review/f2_tables_c6_results.json'}
before={name:sha(R/name) for name in names}
for name,digest in previous['input_hashes'].items():need(before[name]==digest,'Previously audited input changed: '+name)
for doc,origin,builder in [(table,'bis/F2_ALL_READING_TABLES.json','refeito/summarize_f2_tables_013bis_v2.py'),(c6,'C6_ADENDO_REALIZADO.json','refeito/record_c6pre_013bis_v2.py')]:
    need(doc['supersedes']==origin and doc['supersedes_sha256']==before[origin],'Supersedes differs')
    need(doc['code_sha256']==before[builder],'Builder provenance differs')
    for name,digest in doc['source_sha256'].items():need(before[name]==digest,'Source hash differs')
    need(doc['opening_sha256']==sha(R.parent/'TUNEL/DO_CHATGPT/ENTREGA_013BIS_ABERTURA_operador.md'),'Opening differs')

# T1: compile the actual guard block only, bounded by the first rows=[].
builder=R/'refeito/summarize_f2_tables_013bis_v2.py'
tree=ast.parse(builder.read_text(encoding='utf-8'))
def assigns(node,name):return isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in node.targets)
start=next(i for i,n in enumerate(tree.body) if assigns(n,'EXPECTED_COMPUTED'))
end=next(i for i,n in enumerate(tree.body) if i>start and assigns(n,'rows'))
guards=tree.body[start:end]
need(not any(isinstance(n,ast.Assert) for top in guards for n in ast.walk(top)),'Guard relies on assert')
writer_lines=[n.lineno for n in tree.body if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='new']
need(writer_lines and min(writer_lines)>tree.body[end].lineno,'Write precedes coverage guard')
guard_code=compile(ast.fix_missing_locations(ast.Module(body=guards,type_ignores=[])),str(builder),'exec',optimize=1)
cat=get('C4_CATALOG_220.json');legacy=get('C4_GWTC3_220.json');py=get('C4_PYRING.json')
readings=[r['reading'] for r in cat['catalog']]+['R-PROP','R-RAIZ-COHERENT']
def guard_run(category=None,mutation=None):
    env={'cat':copy.deepcopy(cat),'old':copy.deepcopy(legacy),'py':copy.deepcopy(py),'readings':readings[:]}
    if category:
        event=env['py'] if category=='pyRing' else env['cat' if category=='pSEOB' else 'old']['rows'][0]
        if mutation=='missing':event['rows']=[r for r in event['rows'] if r['reading']!='R-MOD']
        elif mutation=='duplicate':event['rows'].append(copy.deepcopy(event['rows'][0]))
        elif mutation=='extra':event['rows'].append({'reading':'UNEXPECTED_READING'})
    try:exec(guard_code,env)
    except ValueError as exc:return dict(rejected=True,error=str(exc),reached_post_guard=False)
    return dict(rejected=False,reached_post_guard=True,computed=sorted(env['EXPECTED_COMPUTED']),pyRing_computed=sorted(env['PYRING_COMPUTED']))
positive=guard_run();need(not positive['rejected'],'Unmodified input refused')
need(set(positive['computed'])==set(readings)-{'R-PROP','R-RAIZ-COHERENT'} and len(positive['computed'])==8,'Eight-reading set')
need(set(positive['pyRing_computed'])=={'R-B','R-RAIZ-0','R-LIN','R-MOD'},'pyRing set')
mutations=[]
for category in ['pyRing','pSEOB','GWTC3']:
    for mutation in ['missing','duplicate','extra']:
        result=guard_run(category,mutation);need(result['rejected'],'Coverage mutation accepted')
        mutations.append(dict(category=category,mutation=mutation,**result))

# T2: all old values stay, new row statutes and the CSV companion hash survive.
need(len(table['rows'])==60 and len({(r['dataset'],r['reading']) for r in table['rows']})==60,'Table coverage')
row_checks=[]
for former,row in zip(old['rows'],table['rows']):
    need({k:row[k] for k in former if k!='analytic_scope'}=={k:v for k,v in former.items() if k!='analytic_scope'},'Original row changed')
    need(row['nonblind'] is True and row['source_conditional_verdict']==former['verdict'],'Conditional verdict/nonblind')
    need(row['physical_status']=='INCONCLUSIVE_SYSTEMATICS__NO_PHYSICAL_CONFIRMATION','Physical status')
    need('not calibrated significance' in row['z_scope'] and 'never converted from lnB' in row['z_scope'],'z scope')
    reading=row['reading']
    if reading=='R-GLOBAL':expected='RELATIONAL_IDENTITY_IN_DECLARED_IMPLEMENTATION'
    elif reading in ('R-PROP','R-RAIZ-COHERENT'):expected='CONDITIONAL_NUMERICAL_EQUIVALENCE__PHYSICAL_MAPPING_OPEN'
    elif row['analytic']:expected='CONDITIONAL_NUMERICAL_EQUIVALENCE__BELOW_RESOLUTION'
    else:expected='COMPUTED_CONDITIONAL_DENSITY'
    need(row['result_type']==expected,'Result type differs')
    if expected!='COMPUTED_CONDITIONAL_DENSITY':need(bool(row['analytic_scope']),'Missing analytic/identity scope')
    row_checks.append(dict(dataset=row['dataset'],reading=reading,result_type=expected))
skip={'utc','code_sha256','supersedes','supersedes_sha256','rows'}
need({k:v for k,v in table.items() if k not in skip}=={k:v for k,v in old.items() if k not in skip},'Unexpected table metadata change')
csvpath=R/'bis/F2_ALL_READING_TABLES_v2.csv'
with csvpath.open(encoding='utf-8',newline='') as handle:csvrows=list(csv.DictReader(handle))
required={'analytic','analytic_scope','scope','nonblind','physical_status','z_scope','source_conditional_verdict','result_type','reason','companion_json','companion_json_sha256'}
need(len(csvrows)==60 and required<=set(csvrows[0]),'CSV context missing')
for csvrow,row in zip(csvrows,table['rows']):
    for key,value in csvrow.items():
        if key=='companion_json':need((csvpath.parent/value).resolve()==(R/'bis/F2_ALL_READING_TABLES_v2.json').resolve(),'CSV companion path')
        elif key=='companion_json_sha256':need(value==before['bis/F2_ALL_READING_TABLES_v2.json'],'CSV companion hash')
        else:need(value==('' if row[key] is None else str(row[key])),'CSV value/context differs: '+key)

# C6-R1: compare with the previous independent corrected-reference receipt.
reg=get('REGISTRO_C6.json');reference=c6['primary_reference']
need(reference['redshift']==reg['reference_redshift']==.086 and reference['constants_profile']=='CODATA2018_IAU2015','C6 frame/profile')
need({k:reference[k] for k in c0['primary_reference']}==c0['primary_reference'],'C6 fixed median changed')
need(c6['historical_result_sha256']==before['C6_RESULTS.json'],'Historical C6 hash')
c6tree=ast.parse((R/'refeito/record_c6pre_013bis_v2.py').read_text(encoding='utf-8'))
calls=[n for n in ast.walk(c6tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='prediction']
need(len(calls)==1,'Unexpected prediction call count')
kwargs={k.arg:k.value for k in calls[0].keywords}
need(ast.dump(kwargs['redshift'])==ast.dump(ast.parse("reg['reference_redshift']",mode='eval').body),'C6 call ignores registered redshift')
need(isinstance(kwargs['profile'],ast.Constant) and kwargs['profile'].value==reference['constants_profile'],'C6 call profile')
expect={v['reading']:v for v in previous['C6']['predictions']};prediction_checks=[]
need(len(c6['rows'])==10,'C6 row count')
for former,row in zip(c0['rows'],c6['rows']):
    need({k:v for k,v in former.items() if k!='delta_L_at_GR_median'}=={k:v for k,v in row.items() if k!='delta_L_at_GR_median'},'C6 scope, lnB or uncertainty changed')
    reading=row['reading'];actual=row['delta_L_at_GR_median']
    if reading in expect:
        expected=expect[reading]['at_registered_z']
        need(math.isclose(actual,expected,rel_tol=1e-12,abs_tol=0),'C6 corrected prediction differs')
        prediction_checks.append(dict(reading=reading,value=actual,independent_previous_expected=expected,changed=actual!=former['delta_L_at_GR_median']))
    else:need(actual is None,'Open route gained a value')
cskip={'utc','supersedes','supersedes_sha256','historical_result_sha256','code_sha256','primary_reference','rows'}
need({k:v for k,v in c0.items() if k not in cskip}=={k:v for k,v in c6.items() if k not in cskip},'Unexpected C6 metadata change')
note=(R/'REAPROVEITAMENTO_C6_v2.md').read_text(encoding='utf-8')
need(before['C6_ADENDO_REALIZADO_v2.json'] in note and c6['opening_sha256'] in note and 'record_c6pre_013bis_v2.py' in note,'C6 reuse receipt mismatch')
need('NÃO-CEGA' in note and 'não calibrada' in note and 'Não pago: sigma calibrada' in note,'Reuse receipt promotes status')
need(before=={n:sha(R/n) for n in before},'Inputs changed during closure')
result=dict(utc=datetime.now(timezone.utc).isoformat(),status='T1_T2_C6_R1_CLOSED',optimization=sys.flags.optimize,script_sha256=sha(Path(__file__)),input_hashes=before,
 positive_guard=positive,negative_guards=mutations,guard_block_lines=[guards[0].lineno,tree.body[end].lineno-1],first_top_level_write_line=min(writer_lines),
 table_rows=60,csv_rows=60,table_row_types=row_checks,original_table_values_unchanged=True,companion_hash_matches_all_60=True,
 C6_predictions=prediction_checks,C6_lnB_and_uncertainties_unchanged=True,inputs_unchanged=True,
 limitations='Only the three named findings. Actual guard block isolated via AST; production writers/builders not executed. No strain, posterior, C5, density or QNM computation.')
write_new(receipt,(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode())
preds='\n'.join(f"| {v['reading']} | {v['value']:.15g} |" for v in prediction_checks if v['reading'] in ['R-A','R-RAIZ-EP4','R-RAIZ-REST'])
display=['refeito/summarize_f2_tables_013bis_v2.py','bis/F2_ALL_READING_TABLES_v2.json','bis/F2_ALL_READING_TABLES_v2.csv','refeito/record_c6pre_013bis_v2.py','C6_ADENDO_REALIZADO_v2.json','REAPROVEITAMENTO_C6_v2.md']
hash_table='\n'.join(f'| `{name}` | `{before[name]}` |' for name in display)
text=f'''[REAL — fechamento somente de T1/T2/C6-R1; sem mudança de gate]

# Fechamento F2/C6

Data UTC: {result['utc']}. **Os três achados estão encerrados nas versões examinadas.** Não restou bloqueante desses achados. Isto não aprova toda a ordem, o pacote v3 em construção, a calibração ou limites físicos.

| Achado | Controle independente e resultado |
|---|---|
| T1 — cobertura | Bloco real das guardas isolado por AST e compilado com optimize=1. Dados íntegros passam; 9/9 mutações são recusadas: falta de R-MOD, duplicata e leitura extra, cada uma em pyRing, pSEOB e GWTC3. O bloco precede a primeira escrita; nenhuma mutação alcança o ponto posterior às guardas. |
| T2 — CSV/estatutos | 60/60 linhas conservam os números e vereditos condicionais anteriores. CSV transporta analytic, analytic_scope, scope, nonblind, physical_status, z_scope, source_conditional_verdict, result_type e reason. Caminho e SHA256 do JSON companheiro conferem nas 60 linhas. |
| C6-R1 — referencial | A chamada usa redshift do registro (0,086) e perfil CODATA2018_IAU2015, ambos gravados em primary_reference. Os valores corrigidos coincidem com o controle independente anterior. |

As guardas exigem oito leituras calculadas nas fontes pSEOB/GWTC3 e as quatro explícitas do pyRing. A complementação analítica não é mais acionada pela mera ausência de um resultado obrigatório. As categorias separam identidade relacional R-GLOBAL, equivalência sub-resolução e R-PROP/coerente com mapeamento OPEN. `analytic` conserva sua função de origem/complemento, enquanto result_type registra o significado físico-condicional.

No C6, as três predições corrigidas são:

| Leitura | delta no referencial registrado |
|---|---:|
{preds}

A mediana de massa/spin permaneceu fixa. As demais predições conferem; as duas rotas abertas continuam null. Os dez lnB, sigma/z efetivos null, Fisher de referência separado, timing, ruído, variante DECLARADO do auditor, limitações e vereditos permanecem iguais. Nenhuma ciência foi refeita: confrontei as correções com os valores esperados já medidos na revisão anterior e conferi a passagem explícita dos parâmetros no código.

Proveniência: supersedes, fontes, builders, abertura e vínculo CSV→JSON conferem. REAPROVEITAMENTO_C6_v2.md cita o hash correto do adendo v2 e mantém NÃO-CEGO/não calibrado e as lacunas. Os insumos antigos monitorados mantêm os hashes da revisão anterior; todos os insumos novos/antigos permaneceram intactos durante esta verificação. Os builders foram encontrados em `ORDEM_013_RINGDOWN/refeito/`; não existe a subpasta `B/` mencionada no pedido.

Controle próprio: `bis/c1_review/close_f2_c6_findings.py`, executado com Python bundled `-B -O`. Evidência: `bis/c1_review/f2_c6_closing_results.json`, SHA256 `{sha(receipt)}`. Script SHA256 `{sha(Path(__file__))}`. Para repetir, usar cópia isolada mantendo os caminhos relativos; saídas recusam sobrescrita. Somente o bloco puro de guardas foi executado, com dados em memória; nenhum builder/escritor de produção foi executado. Sem strain, posteriores, C5, memória ou canônico. Axiomas: N/A — sem Lean.

| Caminho relativo a ORDEM_013_RINGDOWN | SHA256 lido |
|---|---|
{hash_table}
'''
write_new(report,text.encode())
print(json.dumps(dict(status=result['status'],guard_mutations=len(mutations),csv_rows=60,report_sha256=sha(report)),ensure_ascii=False))
