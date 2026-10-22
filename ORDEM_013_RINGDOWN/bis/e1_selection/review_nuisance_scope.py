"""E1 scope/custody checks from JSON and AST only; no scientific execution."""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
import ast,collections,datetime,hashlib,itertools,json,math,sys
from pathlib import Path
import numpy as np
B=Path(__file__).resolve().parents[2];ROOT=B.parent;O=Path(__file__).resolve().parent
N=B/'bis/e1_nuisance_v2';RUN=N/'runs/authorized_001';hashes={}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):
    raw=p.read_bytes();hashes[str(p)]={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()};return json.loads(raw)
def require(ok,msg):
    if not ok:raise ValueError(msg)
def equal(a,b):require(math.isclose(float(a),float(b),rel_tol=5e-10,abs_tol=1e-12),(a,b))
def strict_read(p):
    return json.loads(p.read_text(encoding='utf-8'),parse_constant=lambda s:(_ for _ in ()).throw(ValueError(s)))
def new(p,data):
    with p.open('xb') as f:f.write(data)
report=B/'bis/E1_INDEPENDENT_SCOPE_REVIEW.md';out=O/'NUISANCE_SCOPE_CONTROLS.json'
require(not report.exists() and not out.exists(),'Existing audit output')
manifest=load(N/'DESIGN_MANIFEST.json');auth=load(N/'AUTHORIZATION.json');receipt=load(RUN/'RECEIPT.json');result=load(RUN/'NUISANCE_DIAGNOSTIC.json');strict_read(RUN/'NUISANCE_DIAGNOSTIC.json')
for f in manifest['files']:
    p=(ROOT/f['path']).resolve();require(p.is_relative_to(ROOT),'manifest confinement');raw=p.read_bytes()
    require(len(raw)==f['bytes'] and hashlib.sha256(raw).hexdigest()==f['sha256'],'manifest changed '+str(p));hashes[str(p)]={'bytes':len(raw),'sha256':sha(p)}
for field,p in [('script_sha256',N/'prepare_e1.py'),('manifest_sha256',N/'DESIGN_MANIFEST.json'),('authorization_sha256',N/'AUTHORIZATION.json'),('result_sha256',RUN/'NUISANCE_DIAGNOSTIC.json'),('budget_source_sha256',B/'bis/PART_B_BUDGET_START.json')]:require(receipt[field]==sha(p),field)
require(auth['design_manifest_sha256']==sha(N/'DESIGN_MANIFEST.json'),'authorized manifest')
require(auth['sealed_E0_sha256']==sha(ROOT/auth['sealed_E0_path']),'E0 seal')
dt=datetime.datetime.fromisoformat
start=dt(receipt['started_utc']);end=start+datetime.timedelta(seconds=receipt['wall_seconds'])
require(dt(manifest['created_utc'])<dt(auth['issued_utc'])<=start<end<dt(auth['expires_utc']),'chronology')
oldtree=ast.parse((B/'bis/e1_nuisance/prepare_e1.py').read_text(encoding='utf-8'));newtree=ast.parse((N/'prepare_e1.py').read_text(encoding='utf-8'))
def defs(tree):return {n.name:ast.dump(n,include_attributes=False) for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
od,nd=defs(oldtree),defs(newtree);changed=[k for k in od if od[k]!=nd.get(k)]
require(changed==['main'],'scientific AST changed')
require(not any(isinstance(n,ast.Assert) for n in ast.walk(newtree)),'guard assert')
dataset=load(B/'bis/e0_core/DATASET.json');events=result['events'];rows={r['product_id']:r for r in dataset['rows']}
require(set(events)==set(dataset['sets']['GWTC5_33']) and len(events)==33,'event population')
require(sum(e['N'] for e in events.values())==608681,'rows')
variance_checks=0
for pid,e in events.items():
    r=rows[pid];require(e['N']==r['N'] and e['source_sha256']==r['source_sha256'] and e['dataset']==r['dataset'],'inherited source contract '+pid)
    equal(e['sigma_dtau_ddof1'],r['stdtau']);require(e['ESS'] is None,'ESS not measured')
    for prior in e['priors'].values():
        require(prior['status']=='UNIFORM_MARGINAL_DECLARATION_VERIFIED__JOINT_FACTORIZATION_OPEN','prior statute')
        require(prior['bounds'][0]<prior['bounds'][1] and all(math.isfinite(v) for v in prior['bounds']),'prior bounds')
    c=np.array(e['paired_covariance']);require(np.all(np.isfinite(c)) and np.allclose(c,c.T,rtol=0,atol=1e-12),'paired covariance')
    ix=e['paired_covariance_fields'].index('dtau');equal(c[ix,ix],e['sigma_dtau_ddof1']**2)
    for reading,p in e['predictions'].items():
        equal(p['u_mean'],e['mean_dtau']-p['mean'])
        equal(p['u_std_ddof1']**2,e['sigma_dtau_ddof1']**2+p['std_ddof1']**2-2*p['cov_dtau_delta']);variance_checks+=1
    require(e['predictions']['GR']['scope']=='REFERENCE_DTAU_ZERO_WITH_FREE_DF','GR scope')
groups={}
for name in ['GWTC5_31','GWTC5_33']:
    ids=dataset['sets'][name];groups[name]=ids
    for cut in [.15,.20,.25]:groups[f'{name}/sigma_lt_{cut:.2f}']=[i for i in ids if events[i]['sigma_dtau_ddof1']<cut]
    for run in ['O1-O3','O4a','O4b']:
        allowed=['O1','O2','O3','O3a','O3b'] if run=='O1-O3' else [run]
        groups[f'{name}/{run}']=[i for i in ids if events[i]['metadata']['run'] in allowed]
readings=set(next(iter(events.values()))['predictions'])
expected={(r,g,c,bw) for r in readings for g in groups for c in ['sigma','inverse_SNR'] for bw in ([1.] if '/' in g else [.7,1.,1.4])}
actual=set();ok=[];opens=[]
for f in result['fits']:
    key=(f['reading'],f['group'],f['covariate'],f['bandwidth_factor']);require(key not in actual,'duplicate fit');actual.add(key)
    require(f['product_ids']==groups[f['group']],'group membership')
    r=f['result'];require(r['n']==len(f['product_ids']),'n')
    if r['status'].startswith('CONDITIONAL'):
        ok.append(r);cov=np.array(r['covariance']);require(np.allclose(cov,cov.T,atol=1e-12) and np.linalg.eigvalsh(cov).min()>0,'local covariance')
        for i in [0,1]:equal(r['stderr'][i]**2,cov[i,i])
        equal(r['c0_local_wald_to_zero'],r['c0']/r['stderr'][0])
        for sign,v in zip([-1,1],r['c0_local_interval_95']):equal(v,r['c0']+sign*1.959963984540054*r['stderr'][0])
        constant=math.fsum(math.log(events[i]['priors']['dtau']['bounds'][1]-events[i]['priors']['dtau']['bounds'][0]) for i in f['product_ids'])
        equal(r['uniform_width_log_constant'],constant)
        require(r['log_evidence'] is None and r['z_vs_GR_calibrated'] is None and r['z_vs_reading_calibrated'] is None,'false significance')
        require(r['support_distance_h']>=3 and r['newton_distance']<=.05 and r['max_direct_log_error']<=.002,'saved quality flags')
    else:
        opens.append((f['group'],r['n'],r['status']));require(r['n']==3 and r['status']=='NAO_PAGO_NOT_IDENTIFIABLE','open cause')
require(actual==expected and len(ok)==288 and len(opens)==36,'coverage324')
require(receipt['open_cells']==36,'receipt count')
controls=result['kde_controls'];require(len(controls)==891,'KDE controls')
keys={(r['product_id'],r['reading'],r['bandwidth_factor']) for r in controls};require(keys==set(itertools.product(events,readings,[.7,1.,1.4])),'KDE coverage')
require(all(abs(r['integral']-1)<=1e-6 and r['max_direct_log_error']<=.002 for r in controls),'saved KDE flags')
require(set(result['all_readings'])==readings-{'GR'}|set(result['open_readings']) and len(result['all_readings'])==10,'allreadings')
require(set(result['open_readings'])=={'R-PROP','R-RAIZ-COHERENT'},'physical OPEN')
require(all(x['z_calibrated'] is None for x in result['descriptive_comparisons']),'comparison calibrated')
summary={'status':'PASS_SCOPE_CUSTODY_AND_JSON_CONSISTENCY__NOT_SCIENTIFIC_REFIT','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'events':33,'declared_paired_rows':608681,'fits_complete':288,'open_n3_cells':36,'grid_total':324,'kde_saved_checks':891,'variance_identities':variance_checks,
 'dtau_prior_bounds_counts':{str(k):v for k,v in collections.Counter(tuple(e['priors']['dtau']['bounds']) for e in events.values()).items()},
 'max_saved_optimum_log_error':max(r['max_direct_log_error'] for r in ok),'max_saved_newton_distance':max(r['newton_distance'] for r in ok),'min_saved_support_distance_h':min(r['support_distance_h'] for r in ok),
 'manifest_files_verified':len(manifest['files']),'source_contract':'33 N/hash/dataset identities matched frozen DATASET; raw HDF5 bytes not rehashed/read in this scope audit. Producer code checks each before and after execution; scientific independent GR/RB checks belong to principal.',
 'scientific_AST_unchanged_v1_v2':True,'changed_function':'main','raw_HDF_read':False,'KDE_rerun':False,'posterior_refit':False,'code_sha256':sha(Path(__file__)),'source_hashes':hashes}
new(out,(json.dumps(summary,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode())
md=f'''# E1 — revisão independente de escopo e preservação

[REAL — leitura de código, custódia documental e consistência de JSON; não refit científico]

**Sem bloqueante novo encontrado para publicar este produto como diagnóstico condicional NÃO-CEGO. Não é likelihood populacional hierárquica calibrada, Bayes factor ou teste físico.** Resultado examinado: `bis/e1_nuisance_v2/runs/authorized_001/NUISANCE_DIAGNOSTIC.json`. A execução de {receipt['wall_seconds']:.5f}s é do agente principal autorizado; não foi repetida aqui.

## Cobertura e preservação

Conferidos os {len(manifest['files'])} arquivos do manifesto por tamanho/SHA256, os vínculos do recibo com código, manifesto, autorização, resultado e orçamento, além da cronologia plano→autorização→execução. A AST dos métodos científicos é idêntica entre v1 e v2; apenas main mudou. A versão antiga, seu plano/manifesto e o registro de falha de dependência permanecem. O status UNEXECUTED do plano é histórico; o recibo posterior comprova a etapa executada.

O conjunto tem 33 eventos/608.681 linhas declaradas, com N, dataset e hash de cada produto iguais ao DATASET congelado. Esta revisão **não reabriu nem rehasheou HDF5**: conferiu a cadeia documental e o código que verifica esses arquivos antes/depois. A conferência científica GR/R-B independente conduzida pelo principal é distinta deste parecer.

Grade completa: nove referências calculáveis (GR marginal + oito leituras), 14 grupos, dois covariáveis; três bandas nas populações31/33 e banda nominal nos recortes. São **324 células =288 ajustes condicionais +36 NÃO PAGO**, estes exclusivamente nos dois recortes σ<0,15, com três eventos cada. Não são 36 falhas descartadas ou substituídas por zero. R-PROP e R-RAIZ-COHERENT são duas leituras físicas adicionais OPEN, fora dessa grade calculável; não confundí-las com as 36 células pequenas. As dez leituras estão conservadas.

Os 891 controles KDE registrados cobrem 33×9×3 sem duplicatas. As flags salvas respeitam limites de integral, erro direto, estacionariedade e distância de suporte. Maior erro de logdensidade no ótimo: {summary['max_saved_optimum_log_error']:.8g}; distância de Newton máxima {summary['max_saved_newton_distance']:.8g}; margem mínima {summary['min_saved_support_distance_h']:.8g} h. Isso é conferência de resultados/limiares registrados, **não nova execução das somas KDE**, certificação de ótimo global ou cobertura estatística.

## Objeto efetivamente ajustado

O código preserva linhas conjuntas e calcula u=δτ−δ_L(Mf_det,chi_f,z) amostra por amostra. Não substitui os parâmetros por medianas nem corta δf. A marginalização sobre δf e parâmetros auxiliares mantém suas correlações na distribuição de u, mas **remove a restrição δf=0**. A referência GR aqui é δτ=0 com δf marginalizado/livre, diferente do ponto GR conjunto (δf,δτ)=(0,0) e do lnB da curva anterior. É indispensável conservar esse qualificador ao exportar tabelas; rótulo isolado “GR” seria ambíguo.

Conferidas {variance_checks} identidades a partir dos momentos publicados: E[u]=E[δτ]−E[δ_L] e Var(u)=Var(δτ)+Var(δ_L)−2Cov(δτ,δ_L). A matriz pareada é simétrica e sua entrada δτ coincide com σ². Isso apoia a preservação das correlações no produto, sem provar novamente a extração científica das amostras. R-GLOBAL e ramos abaixo da resolução podem ser idênticos numericamente ao controle marginal, sem virarem medições independentes nem efeito analítico literalmente nulo.

## Priors e constantes

O parser lê declarações Uniform via AST de literais; não executa texto de prior. Os recibos registram **29 priors δτ em [−0,8;2] e quatro em [−0,8;4]**. Reobtida Σlog W individual para cada um dos288 ajustes: não há substituição universal por largura2,8. A constante está registrada separadamente; `conditional_log_density` é soma de log p_u, e não evidência normalizada.

A identidade W p_u(c) só representa integral restrita proporcional à likelihood sob prior τ fatorizado constante, prior auxiliar comum/normalizado e suporte global compatível. A transformação u=τ−δ_L(η) não torna o prior de u uniforme. Declarações marginais e draws dentro dos limites não provam essas hipóteses. Código/plano mantêm **fatorização, suporte global e normalização restrita OPEN**. A interseção empírica [τmin−minδ,τmax−maxδ] e a margem3h são guardas conservadoras; não são prior exato nem correção de borda. Seu cumprimento não fecha essas lacunas.

## σ, covariância e interpretação

c(σ)=c0+kσ usa σ=DP posterior de δτ, ddof1, comum às leituras. A KDE usa a dispersão própria de u; o comparador gaussiano usa Var(u). São papéis diferentes, corretamente separados. σ é estimado do mesmo posterior: há endogeneidade, erro no covariável e possível efeito de prior/seleção. Não foram resolvidos por tratar σ como fixo. A variante c(ρ)=c∞+kρ·40/ρ é INPUT, não lei deduzida; sua SNR total GWOSC não substitui as duas SNRs da seleção pSEOB.

A Hessiana usa derivadas da soma gaussiana direta e a transformação de coordenadas devolve covariância local de(c0,k). Diagonais/EP, razões c0/EP e intervalos Wald salvos são coerentes aritmeticamente. Isso não calibra a distribuição amostral ou um posterior dos hiperparâmetros: ESS é desconhecida, banda varia, grupos se sobrepõem, não há lei de seleção/população normalizada nem validação de cobertura. Os z físicos, evidências e comparações calibradas continuam **null**. Diferenças entre escores de leituras com intercepto livre não são LR ou sigma; deslocamento quase constante é degenerado com c0.

O controle da gerência usa mediana/q90/1,6449 e covariância WLS absoluta, sem reescalaχ²; o KDE fullsample é outro estimador. Diferença entre seus erros não é ganho de precisão física demonstrado. Não reajustei nem repeti esse controle científico.

## Seleção, preservação operacional e conclusão de escopo

Eficiência α(Λ) segue UNKNOWN_NORMALIZATION. A norma escolhida de seleção, os vieses possíveis, a injeção LVK de ponto único e os dois estimadores C2/C5 estão no parecer lateral `bis/e1_selection/SELECTION_AND_CONTROLS.md`; não transformam o ajuste em inferência hierárquica calibrada. A expressão FULL_TEXT_READING_REQUIRED no JSON descreve pendência daquele script: o parecer lateral documenta passagens primárias efetivamente lidas, **não leitura integral dos PDFs**.

Guardas usam exceções explícitas, não assert. Caminhos resolvidos ficam na raiz autorizada, tag é restrita, destino preexistente é recusado; publicação por hard link de temporário completo não substitui saída existente. Falha deixa registro/temporário, sem apagar ciência antiga. Limite temporal é cooperativo. Uma thread foi solicitada por variáveis de ambiente, não medida; o recibo diz isso corretamente. Nenhum desses controles é autorização automática para nova execução.

**Aprovação limitada ao estatuto documental/condicional e à preservação conferida.** Curva de calibração pSEOB, eficiência de seleção, prior restrito global e significância/likelihood populacional calibrada continuam NÃO PAGOS/OPEN. Nenhuma produção alterada, nenhum gate movido, nenhuma leitura escolhida.

Controle: `bis/e1_selection/review_nuisance_scope.py`; recibo `NUISANCE_SCOPE_CONTROLS.json` (hashes completos). SHA256 do resultado examinado: `{sha(RUN/'NUISANCE_DIAGNOSTIC.json')}`. Axiomas N/A; teoremas0.
'''
new(report,md.encode());print(json.dumps({k:v for k,v in summary.items() if k not in ['source_hashes']}))
