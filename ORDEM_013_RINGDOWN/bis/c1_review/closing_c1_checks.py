"""Close named C1 findings under -O, without executing any producer main."""
from pathlib import Path
from datetime import datetime, timezone
import ast, copy, csv, hashlib, importlib.util, json, re, sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads((ROOT/p).read_bytes())
def require(v,msg):
    if not v:raise RuntimeError(msg)
def write_new(p,obj):
    require(not p.exists(),'Existing review output')
    raw=obj.encode('utf-8');tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(raw)
    require(tmp.read_bytes()==raw,'Review write differs')
    require(not p.exists(),'Output appeared');tmp.rename(p)
def main():
    require(sys.flags.optimize==1,'Run with -O')
    prior=load('bis/c1_review/final_artifact_checks.json')
    added=['refeito/c1_evidence_guards_v2.py','refeito/record_c1_013bis_v4.py','C1_LEITURAS_v4.json',
           'C1_ADENDO_CORRECOES_013BIS_v3.md','REAPROVEITAMENTO_C1_v3.md']
    before={p:sha(ROOT/p) for p in set(prior['input_hashes'])|set(added)}
    require(all(before[p]==h for p,h in prior['input_hashes'].items()),'Historical input changed')
    spec=importlib.util.spec_from_file_location('guard_v2',ROOT/added[0]);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
    m=load('bis/C1_NUMERICAL_CONTROLS_v2.json');c=load('cache/casa/um_absoluto.json')['core']['clock_test_result_v369'];cat=load('C4_CATALOG_220.json')
    with (ROOT/'C7_INDEPENDENT/tables/event_reading_predictions.csv').open(encoding='utf-8-sig') as f:r=list(csv.DictReader(f))
    g.validate_inputs(r,cat);positive=g.validate_evidence(ROOT,m,c)
    tests=[]
    def probe(name,fn):
        try:fn()
        except (ValueError,TypeError,KeyError) as e:tests.append(dict(name=name,rejected=True,reason=str(e)))
        else:tests.append(dict(name=name,rejected=False))
    x=copy.deepcopy(r);x.insert(0,dict(x[0],delta_tau='12345'));probe('conflicting_duplicate_csv',lambda:g.validate_inputs(x,cat))
    x=copy.deepcopy(r);x[-1]['delta_tau']='NaN';probe('nan_last_csv_column',lambda:g.validate_inputs(x,cat))
    probe('missing_csv_row',lambda:g.validate_inputs(r[:-1],cat))
    x=copy.deepcopy(m);x['csv_checks'][0]['relative_errors']['delta_tau']=float('nan');probe('nan_recorded_error',lambda:g.validate_evidence(ROOT,x,c))
    x=copy.deepcopy(m);x['dependencies'].pop('refeito/c1_evidence_guards.py');probe('missing_dependency',lambda:g.validate_evidence(ROOT,x,c))
    x=copy.deepcopy(m);x['dependencies']['tgl_ringdown_prediction.py']='0'*64;probe('changed_dependency',lambda:g.validate_evidence(ROOT,x,c))
    x=copy.deepcopy(m);x['checked']=263;probe('wrong_coverage_count',lambda:g.validate_evidence(ROOT,x,c))
    x=copy.deepcopy(c);x['P1']['verdict']='P1_FALSIFIED_IN_READING';probe('changed_P1',lambda:g.validate_evidence(ROOT,m,x))
    x=copy.deepcopy(c);x['all_verified']=False;probe('unsealed_clock',lambda:g.validate_evidence(ROOT,m,x))
    x=copy.deepcopy(m);x['P2_tau_star_bound_tP']*=2;probe('changed_bound',lambda:g.validate_evidence(ROOT,x,c))
    x=copy.deepcopy(m)
    for row in x['csv_checks']:row['event']='WRONG_'+row['event']
    probe('evidence_keys_disjoint_from_hashed_csv',lambda:g.validate_evidence(ROOT,x,c))
    x=copy.deepcopy(m);x['profile_comparison']=[];probe('empty_profile_table',lambda:g.validate_evidence(ROOT,x,c))
    x=copy.deepcopy(m);x['profile_comparison'][0]['comparison_redshift']=1;probe('profile_redshift_not_zero',lambda:g.validate_evidence(ROOT,x,c))
    x=copy.deepcopy(m)
    for row in x['spin_comparison']:row.pop('exact_qnm')
    probe('all_qnm_pairs_missing',lambda:g.validate_evidence(ROOT,x,c))
    tree=ast.parse((ROOT/added[1]).read_text(encoding='utf-8-sig'))
    fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='write_new')
    namespace={'require':g.require};exec(compile(ast.Module(body=[fn],type_ignores=[]),'fakepath_only','exec',optimize=1),namespace)
    class FakePath:
        name='fake'
        def __init__(self,corrupt):self.corrupt=corrupt;self.replaced=False;self.data=b''
        def exists(self):return False
        def with_name(self,name):return self
        def open(self,mode):return self
        def __enter__(self):return self
        def __exit__(self,*args):return False
        def write(self,data):self.data=data;return len(data)
        def read_bytes(self):return self.data+(b'CORRUPTED' if self.corrupt else b'')
        def replace(self,target):self.replaced=True
    writes=[]
    for corrupt in (False,True):
        p=FakePath(corrupt);exc=None
        try:namespace['write_new'](p,'review payload')
        except ValueError as e:exc=str(e)
        writes.append(dict(corrupt=corrupt,replaced=p.replaced,error=exc))
    v=load('C1_LEITURAS_v4.json');v3=load('C1_LEITURAS_v3.json')
    checks={'v4_rows_equal_v3':v['rows']==v3['rows'],'numeric_v2_preserved':sha(ROOT/'bis/C1_NUMERICAL_CONTROLS_v2.json')==prior['input_hashes']['bis/C1_NUMERICAL_CONTROLS_v2.json'],
      'generator_hash':sha(Path(v['v4_generator']['path']))==v['v4_generator']['sha256'],
      'validator_hash':sha(ROOT/v['evidence_validator']['path'])==v['evidence_validator']['sha256'],
      'origin_hash':sha(ROOT/'complete_c1_contract.py')==v['origin_generator_sha256'],
      'supersedes_v3':v['supersedes']=='C1_LEITURAS_v3.json' and v['supersedes_sha256']==sha(ROOT/'C1_LEITURAS_v3.json'),
      'numeric_ref':v['numerical_controls']['sha256']==sha(ROOT/'bis/C1_NUMERICAL_CONTROLS_v2.json'),
      'primary_ref':v['primary_retrievals']['sha256']==sha(ROOT/'bis/C1_PRIMARY_RETRIEVALS.json')}
    ad=(ROOT/added[3]).read_text(encoding='utf-8');oldad=(ROOT/'C1_ADENDO_CORRECOES_013BIS_v2.md').read_text(encoding='utf-8')
    # Compare body apart from generation timestamp and output-reference line.
    normalize=lambda text:'\n'.join(line for line in text.splitlines()[1:] if not line.startswith('- C1_LEITURAS_'))
    checks['editorial_body_preserved']=normalize(ad)==normalize(oldad)
    known=set(before.values())|{sha(ROOT.parent/'TUNEL/DO_CHATGPT/ENTREGA_013BIS_ABERTURA_operador.md')}
    for filename in added[3:]:
        checks['hashes_in_'+filename]=all(h in known for h in re.findall(r'\b[0-9a-f]{64}\b',(ROOT/filename).read_text(encoding='utf-8')))
    require(all(t['rejected'] for t in tests),'Mutation accepted')
    require(writes[0]['replaced'] and not writes[1]['replaced'] and writes[1]['error'],'Write guard failed')
    require(all(checks.values()),'Artifact check failed: '+str(checks))
    require(all(sha(ROOT/p)==h for p,h in before.items()),'Inputs changed during review')
    result=dict(status='PASS_C1_NAMED_FINDINGS_CLOSED',utc=datetime.now(timezone.utc).isoformat(),optimization=sys.flags.optimize,python=sys.version,
      script_sha256=sha(Path(__file__)),input_hashes=before,positive_control=positive,mutations=tests,fakepath_bytes=writes,artifact_checks=checks,inputs_unchanged=True)
    resultpath=HERE/'closing_c1_results.json';write_new(resultpath,json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    manifest='\n'.join(f'| `{p}` | `{sha(ROOT/p)}` |' for p in added+['bis/C1_NUMERICAL_CONTROLS_v2.json','bis/c1_review/closing_c1_checks.py','bis/c1_review/closing_c1_results.json'])
    report=f'''[REAL — C1/F1: B1/B2 e R1–R3 encerrados para os artefatos e controles auditados; sem alteração de gate]

# Fechamento da revisão C1

Data UTC: {result['utc']}. Raiz dos caminhos: `{ROOT}`.

**APROVADO no escopo desta revisão.** Os dez controles originais e as quatro mutações adicionais foram recusados sob `python -B -O` (optimize=1). A guarda de bytes também recusa a divergência nesse modo. Não restou bloqueante dos achados nomeados. Esta aprovação não certifica ausência universal de defeitos nem aprova F1/F4 ou a ordem inteira.

| Achado | Evidência de encerramento |
|---|---|
| B1 — duplicatas/NaN/cobertura | Guardas explícitas permanecem operantes com otimização; controles positivos passam e mutações anteriores são recusadas. |
| B2/R1 — chaves da evidência | A validação reabre CSV/catálogo cujos hashes conferiu e compara a grade de evidência com as chaves efetivas. Prefixar todos os eventos com WRONG_ agora é recusado. |
| B2/R2 — cinco perfis | Tabela vazia e redshift alterado são recusados; esquema e conjunto exato de cinco leituras são exigidos. |
| B2/R2 — sete QNM | Remover os pares é recusado; esquema exato e par finito com convenção real positiva/imaginária negativa são exigidos nos sete spins. |
| R3 — bytes | Corpo isolado de write_new compilado com optimize=1: bytes íntegros alcançam replace; bytes simulados divergentes recebem ValueError antes de replace. |

Os testes alteram somente cópias em memória. Importei o módulo de guardas inspecionado; não executei main do medidor, registrador, teste original ou um.py. A sonda de escrita usou caminhos simulados sem operações no disco de produção.

**Proveniência e preservação:** v4_generator e evidence_validator conferem por hash com os novos scripts; supersedes aponta à v3 correta; origin_generator continua identificando o gerador original. É correto que o controle numérico v2 continue citando a guarda v1 que o produziu: a nova guarda v2 está identificada separadamente como validador do registrador v4. Não houve reatribuição retrospectiva de proveniência.

O controle numérico v2 permanece byte a byte igual. As dez linhas de C1_LEITURAS_v4 são iguais às da v3. Mantém-se a conferência independente anterior: 264/264 linhas, diferença relativa máxima 2,1237132116536×10⁻¹⁵, 99 pequenas não nulas + 33 R-GLOBAL = 132; sete QNM, dimensões e perfis conferidos. A revisão não repetiu computação sem mudança de valores.

O corpo editorial foi preservado: cota P2 da série mediana com calibração e sem confiança atribuída; ν com ω_R e κ em s⁻¹; BW limitado às seções lidas; Kay–Wald/Sewell sem promoção a integrais lidos; Kerr–KMS ainda [CONJECTURE]; nenhuma escolha física ou fala do operador preenchida. Todos os hashes citados no novo adendo/ficha foram reconhecidos contra os arquivos lidos. As versões históricas monitoradas permaneceram intactas.

## Reprodução

Controle e evidência em bis/c1_review/closing_c1_checks.py e closing_c1_results.json. Comando executado da Central:

```powershell
& 'C:\\Users\\rotol\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\python\\python.exe' -B -O 'Chatgpt/ORDEM_013_RINGDOWN/bis/c1_review/closing_c1_checks.py'
```

As saídas recusam sobrescrita. Para reproduzir novamente, usar uma cópia isolada preservando a estrutura relativa e os insumos. Axiomas: N/A — sem Lean. Sem PE, injeções, alteração de memória/canônico ou execução de produção.

| Arquivo | SHA256 lido por script |
|---|---|
{manifest}
'''
    write_new(ROOT/'bis/C1_CLOSING_REVIEW.md',report)
    print(json.dumps(dict(status=result['status'],mutations_rejected=len(tests),fakepath_bytes=writes,artifact_checks=checks,report_sha256=sha(ROOT/'bis/C1_CLOSING_REVIEW.md')),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
