"""Documentary closure only; no scientific runtime, waveform or PE execution."""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,itertools,json,math

O=Path(__file__).resolve().parent
B=O.parents[2]
R=B/'bis/e2_review'
P=O.parent/'PE_INDEPENDENT_REVIEW.md'


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def require(x,msg):
    if not x:raise ValueError(msg)
def functions(p):return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(p.read_text()).body if isinstance(n,ast.FunctionDef)}


def main():
    final=O/'A_CLOSING_INDEPENDENT_RECEIPT.json'
    require(not final.exists(),'Closure exists')
    receipt=load(R/'PE_CLOSING_RECEIPT.json')
    snap=O/'a_closing_snapshot';snap.mkdir(exist_ok=False)
    pins={}
    for mapping in ['source_sha256','new_files_sha256']:
        for relative,digest in receipt[mapping].items():
            path=B/relative
            require(sha(path)==digest,'Changed A receipt pin: '+relative)
            pins[relative]=digest
            destination=snap/Path(relative).name
            require(not destination.exists(),'Duplicate snapshot basename')
            with destination.open('xb') as f:f.write(path.read_bytes())
    pins['bis/e2_review/PE_CLOSING_RECEIPT.json']=sha(R/'PE_CLOSING_RECEIPT.json')
    with (snap/'PE_CLOSING_RECEIPT.json').open('xb') as f:f.write((R/'PE_CLOSING_RECEIPT.json').read_bytes())
    temporal=load(R/'TEMPORAL_REMNANT_SCALAR_TEST.json')
    contracts=load(R/'CLOSING_CONTRACTS.json')
    rows=temporal['temporal']['rows']
    expected={(a,b,c,d) for a,b,c,d in itertools.product([15.,100.],[10.,100.],[-.99,.99],[-.99,.99]) if .125<=b/a<=1}
    observed={(r['mass_1'],r['mass_2'],r['chi_1'],r['chi_2']) for r in rows}
    require(observed==expected and len(rows)==2*len(expected)==16,'Declared finite endpoint coverage')
    for row in rows:
        require(abs(row['earliest_GPS']-(row['trigger']-.022-row['inspiral_s']-row['merger_s']))<1e-6,'Earliest arithmetic')
        require(abs(row['latest_GPS']-(row['trigger']+.022+row['tail_with_max_dtau_s']))<1e-6,'Latest arithmetic')
    earliest=min(r['earliest_GPS'] for r in rows);latest=max(r['latest_GPS'] for r in rows)
    windows=[]
    for start,duration in [(1420878135.,8.),(1420878129.,16.)]:
        left=earliest-(start+.2);right=start+duration-.2-latest
        windows.append({'start_GPS':start,'duration_s':duration,'left_margin_s':left,'right_margin_s':right,'passes_stored_endpoints':min(left,right)>=0})
    c=contracts['candidate_window']
    require(windows[1]['left_margin_s']==c['left_margin_s'] and windows[1]['right_margin_s']==c['right_margin_s'],'Candidate margin transport')
    require(not windows[0]['passes_stored_endpoints'] and windows[1]['passes_stored_endpoints'],'Window classification')
    rem=temporal['remnant'];out=rem['derived']
    require(out['final_mass_detector'][1]/out['final_mass_detector'][0]==rem['mass_scaling_ratio']==2.,'Mass scaling receipt')
    require(out['final_spin'][1]-out['final_spin'][0]==rem['spin_scaling_difference']==0.,'Spin scaling receipt')
    old=functions(O/'snapshot/pe_runner.py');new=functions(snap/'pe_runner.py')
    unchanged={n:old[n]==new[n] for n in ['sampler_class','terminal_state','convergence','validate_config','posterior_columns']}
    require(all(unchanged.values()),'Sampler tested code changed')
    text=(snap/'pe_runner.py').read_text()
    require('remnant_conversion_wall_seconds=' in text and 'parent_cpu_seconds=time.process_time()-cpu)' in text,'Final remnant cost not integrated')
    require('for k in PHYSICAL+DERIVED_PHYSICAL' in text,'Paired derived columns missing')
    # Confirm documented outstanding integration findings remain on exact producer bytes.
    injection_sha=sha(B/'bis/e2_code/injection_design.py')
    tested_injection_sha=sha(O/'integration_snapshot/injection_design.py')
    require(injection_sha==tested_injection_sha,'Injection changed: do not transfer old blockers without reinspection')
    before=sha(P);backup=O/('PE_INDEPENDENT_REVIEW_before_A_closure_'+before[:12]+'.md')
    with backup.open('xb') as f:f.write(P.read_bytes())
    stamp=datetime.now(timezone.utc).isoformat()
    add=f'''

## Adendo independente de fechamento das seis fontes A — {stamp}

**[REAL — fechamento documental e aritmético, sem novo runtime científico]** Os oito pins de fonte/INPUT e seis pins de novos arquivos de `PE_CLOSING_RECEIPT.json` conferem com os bytes encontrados. Este adendo prevalece sobre a fotografia anterior nos pontos explicitamente atualizados; não apaga os achados de integração da calibração.

**Fechados no escopo de preparação das seis fontes:** integração pareada de remanescente, Planck18 explicitamente INPUT, guarda de hold/revisão documental, reserva temporal de detector e atualização do custo de wall/CPU após a conversão. O runner agora tem SHA256 `{pins['bis/e2_code/pe_runner.py']}`. As cinco funções PE exercidas pelo toy independente permanecem AST-idênticas; não se alegou repetição do toy para o main novo. A diferença posterior acrescenta cronômetro próprio da conversão e atualiza wall/CPU finais antes da saída ao analista. Essa parte temporal de PE-R3 está fechada; contador de invocações reais da likelihood ainda não foi acrescentado.

**Janela:** recomputei somente contas a partir dos limites escalares já registrados por A. Em8s/start1420878135, margens `{windows[0]['left_margin_s']:.9f}` e `{windows[0]['right_margin_s']:.9f}`s: falha. Em16s/start1420878129, margens `{windows[1]['left_margin_s']:.9f}` e `{windows[1]['right_margin_s']:.9f}`s: passa os16 registros de extremos fornecidos. São dois pares de massa (15,10)/(100,100), quatro pares de spins e dois tempos. Isso cobre os cantos retangulares admissíveis examinados, **não** o interior nem todos os vértices que surgem ao recortar o domínio pela constraint de mass_ratio. Não certifica suporte de waveform. O aborto por violação durante execução permanece obrigatório. A configuração16s deve entrar no draft003/registro antes da execução; não alterei o draft002.

**Remanescente:** a razão2 de massa e diferença0 de spin conferem aritmeticamente nos arrays de duas linhas já produzidos por A. O erro de inversão Planck18≈5,1587e−9 é resultado do executor escalar A, conferido em código/recibo; não foi recalculado aqui. Os sete mocks independentes anteriores continuam aplicáveis ao mesmo hash de `remnant_conversion.py`. Não chamar isso de validação em todo posterior, fit independente de inspiral ou cosmologia derivada da TGL.

**Permanecem separados e abertos antes da calibração de duas famílias:** PE-R1 (suporte temporal XPHM) e PE-R2 (verdade injetada versus todos os priors/constraints), no módulo do principal `injection_design.py`, que não pertence às seis fontes A. Seu hash permanece `{injection_sha}`, igual ao das fixtures independentes. O adendo A não modifica esse caminho e não fecha esses dois achados. PE-R3, na parte de chamadas reais de likelihood, continua requisito para afirmar custo/chamada e teto global; `sampler_ncall`/`source_calls` mantêm as distinções medidas pelo toy. Não transformar esse ponto em alegação de falsa convergência: a recusa por maxcall passou.

**Disposição:** preparação das seis fontes A e complemento remnant/hold aceitos no alcance documental/finito descrito, com janela16s como INPUT a registrar e suporte interior OPEN. Não equivale a autorização de PE, ciência executada, calibração de duas famílias pronta ou registro E2 aprovado. O principal pode preparar/fixar o draft003 mantendo os bloqueantes de injeção visíveis e resolvendo-os antes das respectivas células de calibração. E4/E5 segue sem execução.

Nova fotografia e verificações: `pe_review_001/a_closing_snapshot/` e `pe_review_001/A_CLOSING_INDEPENDENT_RECEIPT.json`. Os bytes anteriores deste parecer foram preservados ao lado nas fixtures.
'''
    raw=P.read_bytes()+add.encode('utf-8')
    temp=O/'review_with_A_closure.pending'
    with temp.open('xb') as f:f.write(raw)
    require(temp.stat().st_size==len(raw),'Incomplete report')
    require(sha(P)==before,'Report changed concurrently')
    temp.replace(P)
    report={'status':'SIX_A_SOURCE_PREPARATION_CLOSED_WITH_SEPARATE_CALIBRATION_BLOCKERS','utc':stamp,
            'source_and_document_pins_verified':pins,'windows_recomputed_from_stored_bounds':windows,
            'finite_endpoint_rows':16,'interior_or_full_constrained_domain_certified':False,
            'sampler_functions_AST_unchanged':unchanged,'new_scientific_runtime':False,
            'real_waveforms':False,'PE':False,'strain_read':False,
            'remaining_blockers':['PE-R1_XPHM_SUPPORT','PE-R2_ALL_INJECTION_PRIOR_SUPPORT'],
            'remaining_cost_item':'PE-R3_ACTUAL_LIKELIHOOD_COUNT',
            'report_previous_sha256':before,'report_sha256':sha(P),'script_sha256':sha(Path(__file__)),
            'after_read_pins_unchanged':all(sha(B/p)==h for p,h in pins.items())}
    require(report['after_read_pins_unchanged'],'Source changed during closure')
    with final.open('x') as f:json.dump(report,f,indent=2)
    print(json.dumps({'status':report['status'],'review_sha256':sha(P),'window16':windows[1]}))


if __name__=='__main__':main()
