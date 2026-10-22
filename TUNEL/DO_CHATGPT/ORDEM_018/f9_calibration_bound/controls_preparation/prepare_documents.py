from pathlib import Path
import os,json,hashlib,sys,ast,importlib.util,datetime
BASE=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\f9_calibration_bound\controls_preparation')
PARENT=BASE.parent
RID="8b53f7c0-9f5f-49e1-87bc-cf73a7e1f79d"
def pin(p):
 b=p.read_bytes();return {"path":str(p),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
def write(name,obj):
 p=BASE/name;assert not p.exists()
 data=obj.encode() if isinstance(obj,str) else (json.dumps(obj,ensure_ascii=False,indent=2)+"\n").encode()
 temp=p.with_suffix(p.suffix+".tmp");temp.write_bytes(data);assert temp.read_bytes()==data;os.replace(temp,p)
parents=[PARENT/'PROTOCOLO_CONTROLES_FUTUROS.json',PARENT/'PROVA_COTA_CALIBRACAO_F9.md',PARENT/'CALIBRATION_BOUND_CANDIDATE.json',PARENT/'MANIFESTO_ENTREGA.json']
before=[pin(p) for p in parents]
future=json.loads(parents[0].read_bytes())
dependencies=[]
for name in ['fractions','math','json','hashlib','subprocess','ast','decimal','pathlib','os','sys','time','datetime']:
 spec=importlib.util.find_spec(name);origin=spec.origin
 dependencies.append({"module":name,"origin":origin,"pin":pin(Path(origin)) if origin not in (None,'built-in','frozen') else None,"read_only":True})
runtime=[pin(Path(sys.executable)),pin(Path(sys.base_prefix)/'python314.dll')]
cases=[
{"id":"C01_FIXED_QUOTIENT","inputs":{"C":[[4,0,0],[0,9,0],[0,0,0]],"X":[[2],[0],[0]],"R":[[0,"1/3",0]],"Y":[10,6,0],"mu":"(0,3a,0), a in [-1,1]; true a=0"},
"expected":{"RX":0,"RCRt":1,"residual_rank":1,"q_true":4,"g_null":1},
"justification":"C range is first two coordinates; X has rank1 within it; R erases X and whitens second coordinate. Min (2-a)^2 on [-1,1] is1. Thus0<=g<=qtrue=4. Fixed nuisance only, no reused integration control."},
{"id":"C02_GLOBAL_NONLINEAR_SPAN","inputs":{"z":[0,2,3],"mu_null":[0,0,0],"mu_comp":"(a,a^2,0), a in [-1,1]","V":"span(e1,e2)"},
"expected":{"g_null":13,"g_comp":11,"distance_relaxation":9,"gain":2,"projection_bound":4},
"justification":"All polynomial coefficients lie in fixed V globally. Setting u=a² in[0,1], q=13-3u+u² has derivative -3+2u<0; minimum11 at u1. Distance to V is9, gain2<=4."},
{"id":"C03_TANGENT_IS_NOT_GLOBAL_SPAN","inputs":{"curve":"(a,a²,0)","tangent_at0":[1,0,0],"witness_at1":[1,1,0]},
"expected":{"tangent_certificate":"REJECTED","tangent_dimension":1,"global_span_dimension":2},
"justification":"The e2 coefficient is nonzero globally and cannot lie in span(e1). One tangent is not a global certificate."},
{"id":"C04_DIRECTED_SIGN_AND_ZERO_DF","inputs":{"signed_values":["-3/2",0],"rank_zero_values":[0,1]},
"expected":{"nonpositive_p":1,"atom0_inclusive_tail_at0":1,"atom0_tail_at1":0,"positive_rank0":"CONTRACT_INCOHERENCE_NOT_VALID_REJECTION"},
"justification":"S<=0 is p1 by directed definition. Rank0 pivot has atom0; positive S under valid rank0 null impossible. No SciPy df0."},
{"id":"C05_MINIMUM_CERTIFICATE_DIRECTION","inputs":{"local_only_U_null":9,"true_synthetic_g_null":1,"true_synthetic_g_comp":0,"global_null_interval":[0,9],"global_comp_interval":[0,2]},
"expected":{"local_U_as_L":"REJECTED","ell_G":0,"ell_Q_nested":0,"ell_T":-2,"second_exact_interval_example":"Lnull=3,Ucomp=2 => ell=1"},
"justification":"A feasible local value is U>=g, never automatically L. Lnull-Ucomp is -2. Truncate Q only under nested qualification. Synthetic exact minima make intervals checkable; no optimizer run."},
{"id":"C06_DIFFERENT_COVARIANCE","inputs":{"variance_null":1,"variance_comp":"1/4","epsilon":"1/2","y":0},
"expected":{"RSS_true":0,"directed_T":"2 log2 >1","RSS_likelihood_envelope":"REJECTED"},
"justification":"T=-2log epsilon+(1-epsilon^-2)y². Integral_1^2 dt/t>1/2 proves log2>1/2 without float; T>1>0=RSS. Covariance equality guard must block reuse."},
{"id":"C07_COMPLETE_SCENARIOS","inputs":{"required_scenarios":["a","b","c"],"G":{"a":"1/1000","b":"1/2000","c":"1/4000"},"Q":{"a":"1/1000","b":"1/2000"},"synthetic_alpha":"1/100","family_factor":5},
"expected":{"G_FWER":"1/200","Q_FWER":None,"valid_H1_rejection":True,"H1_nonrejection_available":False},
"justification":"Complete maxG=1/1000; Bonferroni5=1/200<=synthetic alpha. Missing c makes Q unavailable without discarding complete valid G rejection. No best-case selection; no numerical5sigma claim."},
{"id":"C08_TAIL_CERTIFICATE","inputs":{"recurrence_pairs":[[1,2],[2,2],[3,2],[4,2],[2,2000]],"integer_terms":32,"alternate_terms_plus_next":33,"exp_reduction":1024,"sqrt_scale_power10":50},
"expected":{"Q_half_1":"[15/100,16/100]","Q_1_1":"[36/100,37/100]","Q_3half_1":"[57/100,58/100]","Q_2_1":"[73/100,74/100]",
"extreme_e_minus_1000":"strictly between 10^-500 and10^-400, positive","small_tail_interval_width_max":"10^-25","extreme_relative_width_max":"10^-20","certified_enclosures":"overlap recurrence vs integrated-series certificate; extreme vs unit-exponential power"},
"justification":"Exact integer/half-integer upper-gamma recurrences. Independently enclose lower-gamma integral at x1 by alternating exp series; Gamma half via certified sqrt(pi). pi uses exact Machin identity and alternating remainders. exp(-1000) via reciprocal positive-exp Taylor geometric remainder and range reduction; cross-check [exp(-1)]^1000. Rational intervals, not float values, carry certificate.",
"certificate_rules":{"alternating":"Retain32 terms plus next; mathematical decreasing terms tend to0, enclosure between consecutive partial sums.",
"positive_exp":"For0<=y<=1, S=sum0..32 y^k/k!, next=y^33/33!, tail <= next/(1-y/34). Hence exp(-y) lies[1/(S+tail),1/S].",
"sqrt":"isqrt(floor(q*10^100))/10^50 gives lower endpoint; upper integer+1 gives strict upper. Interval endpoints use rational arithmetic.",
"Machin":"pi=16atan(1/5)-4atan(1/239), exact identity; alternating arctan terms.",
"output":"Exact numerator/denominator hexadecimal; no ordinary floating SF or decimal rounded value called certificate.",
"failure":"Visible failure on domain/size/time/certification mismatch; no float fallback, no rerun."}}]
for c in cases:c['expected_statute']="DERIVED_A_PRIORI_SYNTHETIC_CONDITIONAL_NOT_MEASURED"
assert [x['id'] for x in cases]==[x['id'] for x in future['controls']]
execution_pins=[pin(BASE/'controls.py'),pin(BASE/'supervisor.py')]+runtime+[d['pin'] for d in dependencies if d['pin'] is not None]
contract={"schema":"F9_BOUND_EIGHT_CONTROLS_PREPARATION_V1","request_id":RID,"parent_request_id":future["request_id"],
"status":"PREPARED_NOT_EXECUTED_NOT_AUTHORIZED_PROOF_REVIEW_PENDING","created_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
"scope":"Exactly C01-C08 deterministic tiny synthetic controls; independent proof acceptance and specific ROOT execution authorization required.",
"limits":{"cases":8,"matrix_dimension_max":8,"worker_threads":1,"max_wall_seconds":30,"cooperative_worker_seconds":28,"post_kill_cleanup_seconds_max":5,
"execution_count_per_identity_max":1,"random_simulations":0,"CAMB_runs":0,"catalogue_reads":0,"observed_reads":0,"remote_calls":0,"scientific_imports":0,
"max_rational_component_bits":524288,"max_worker_stdout_bytes":4194304,"max_worker_stderr_bytes":65536},
"alternatives_before_measurement":[
{"id":"A_SELECTED","implementation":"Python stdlib Fraction, exact rational matrix operations, explicit series remainders and interval algebra; exact sqrt enclosure via isqrt.","advantage":"Auditable exact bounds and positive tiny tails; no scientific packages needed.","limitation":"Potential integer cost, not benchmarked; timeout or size guard yields failure."},
{"id":"B_NOT_SELECTED","implementation":"Decimal directed rounding with proven series remainders and outward arithmetic contexts, same8cases.","advantage":"Bounded precision can reduce large integer cost.","limitation":"Must qualify every outward-rounded operation/context separately; ordinary mpmath/SciPy/float is not a rigorous interval certificate. No alternate code/run prepared."}],
"selected_implementation":"A","cases":cases,"execution_pins":execution_pins,"source_pins":before,
"dependencies":{"python":sys.version,"direct_metadata":dependencies,"closure_limit":"Pins cover entry interpreter/DLL and named direct stdlib sources; not a complete transitive runtime attestation. No packages installed or scientific modules imported."},
"identity_policy":{"request_id":RID,"run_once":"Exclusive CLAIM.json and new RUN directory, terminal consumption including uncertainty. No resume/fallback/relaunch.",
"required_authorization_file":"AUTORIZACAO_ROOT.json — absent; not generated here",
"authorization_fields":["request_id","contract_sha256","authorized=true","scope=C01_C08_SYNTHETIC_ONLY_ONCE","max_execution_count=1","max_wall_seconds=30","worker_threads=1","independent_proof_review.path/sha256/accepted_for_these_controls=true"],
"proof_review_path_constraint":"Existing .md/.json under ORDEM_018/derivacoes, exact hash verified. ROOT explicitly attests acceptance for these controls; file presence alone is not acceptance.",
"worker":"Single sequential worker, no pool/threads; thread environment1. Supervisor waits and enforces wall timeout; on timeout kills once and preserves receipt.",
"wall":"30 seconds from claim/launch phase; <=5 additional seconds only to collect killed-process output, not continued computation."},
"current_execution_count":0,"claim_exists":False,"authorization_exists":False,"results_exist":False,
"does_not_validate":future["does_not_validate"],"prohibitions":future["do_not_repeat"],
"not_modified":["parent proof/protocol/candidate6273","consumed packages","Atlas","kernel","gate"],
"review_condition":"Any proof-review correction affecting controls requires separate version/delta and new pins before authorization; no automatic adoption."}
write('PROTOCOLO_EXATO.json',contract)
write('IDENTIDADE_PREPARADA.json',{"request_id":RID,"parent_request_id":future["request_id"],"status":"PREPARED_ONLY","execution_count":0,"authorization_granted":False,"contract":pin(BASE/'PROTOCOLO_EXATO.json')})
write('COMANDO_PROPOSTO_NAO_EXECUTADO.json',{"request_id":RID,"argv":[sys.executable,"-I","-B",str(BASE/'supervisor.py'),"--run-once"],
"working_directory":str(BASE),"status":"NOT_EXECUTED_NOT_AUTHORIZED","requires":"Independent proof review and ROOT authorization matching exact contract hash; no authorization or CLAIM exists."})
checks=[]
for name in ('controls.py','supervisor.py'):
 source=(BASE/name).read_text();tree=ast.parse(source,filename=name)
 imports=[]
 for node in ast.walk(tree):
  if isinstance(node,ast.Import):imports.extend(a.name for a in node.names)
  elif isinstance(node,ast.ImportFrom):imports.append(node.module)
 checks.append({"check":name+" AST syntax","pass":True})
 checks.append({"check":name+" imports stdlib only","pass":all(x.split('.')[0] in {'fractions','math','json','sys','time','pathlib','os','hashlib','subprocess','datetime'} for x in imports),"imports":imports})
 if name=='controls.py':
  funcs=[n.name for n in tree.body if isinstance(n,ast.FunctionDef) and n.name.startswith('C0')]
  checks.append({"check":"exactly eight case functions ordered","pass":funcs==[c['id'] for c in cases]})
  scientific_calls=[n for n in tree.body if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call)]
  checks.append({"check":"no top-level call expression except guarded main","pass":len(scientific_calls)==0})
checks.extend([{"check":"parent pins unchanged","pass":[pin(p) for p in parents]==before},
{"check":"no CLAIM/RUN/auth generated","pass":all(not (BASE/n).exists() for n in ('CLAIM.json','RUN','AUTORIZACAO_ROOT.json'))},
{"check":"8 cases retain parent IDs","pass":[c['id'] for c in cases]==[c['id'] for c in future['controls']]},
{"check":"parent limits preserved","pass":future['max_cases']==8 and future['matrix_dimension_max']==8 and future['max_wall_seconds']==30 and future['worker_threads']==1}])
assert all(c['pass'] for c in checks)
write('RECIBO_PREPARACAO_AST_PINS.json',{"status":"STATIC_PREPARATION_ONLY","request_id":RID,"checks":checks,"checks_count":len(checks),
"control_executions":0,"numerical_tail_evaluations":0,"matrix_control_evaluations":0,"scientific_imports":0,"scope":"AST, IDs, pin reads only; controls.py and supervisor.py neither imported nor run."})
note="""# Oito controles F9 — pacote preparado, sem execução

[REAL documental] Request_id próprio registrado em IDENTIDADE_PREPARADA.json. O pacote contém exatamente C01–C08 do protocolo da unidade6273. A prova continua condicionante: a ROOT deve conferir o parecer independente e decidir a execução desta identidade. Nenhuma autorização, CLAIM ou RUN foi criada; nenhuma matriz de controle, SF, solver, catálogo ou dado observado foi avaliado nesta preparação.

[INPUT/DERIVED prévio] PROTOCOLO_EXATO.json fixa todos os números sintéticos e resultados esperados, com justificativas algébricas. C01 usa geometria singular racional3×3 e nuisance suportado; C02 prova a inclusão global de uma parábola num plano; C03 rejeita sua tangente como certificado global. C04 separa sinal e átomo de postozero. C05 rejeita mínimo local como limite inferior. C06 usa o contraexemplo de covariâncias1 e1/4 em y0. C07 preserva rejeição completa válida quando outro controle não dispõe de todos os cenários; alpha=1/100 é estritamente sintético.

Foram comparadas antes de medir duas implementações: A, Fraction e intervalos racionais exatos; B, Decimal com arredondamento dirigido e resto rigoroso. A foi escolhida por tornar os certificados auditáveis sem dependências científicas. B não foi implementada. Python3.14.3 e fontes stdlib diretas foram localizados/pinados, sem instalação. Os pins não são atestado completo de toda dependência transitiva.

C08 implementa as recorrências qui-quadrado para df1/2/3/4 em t2 e df2 em t2000. Os certificados usam séries alternadas com próximo termo, resto geométrico positivo da exponencial, identidade de Machin e sqrt racional limitado por isqrt. A recorrência é comparada à integral inferior expandida; a cauda extrema também a [exp(-1)]^1000. Os resultados esperados são intervalos racionais pré-fixados e positivos. A saída é numerador/denominador hexadecimal exatos; float comum não é certificado. A certificação proposta depende da correção matemática e computacional desse código, ainda não executado nem aprovado. Não há promessa de desempenho em30s.

O supervisor proposto exige autorização ROOT por hash do contrato e parecer independente pinado com aceite explícito. Executa somente um worker sequencial, oito casos, matrizes≤8, sem MC, CAMB ou import científico. Teto de30s de processamento, parada cooperativa aos28s, kill no prazo e até5s adicionais apenas para recolher processo morto. Inteiros têm limite de tamanho; falha em certificado, orçamento ou identidade é terminal e visível, sem retry/fallback. A identidade consumida permanece consumida mesmo com resultado incerto.

Validação presente: apenas sintaxe AST, identidade, lista de imports e pins. Não é resultado dos controles, prova empírica, validação de Gaussianidade/covariância física, certificado de mínimos F9, poder5sigma ou significância observada. Não foram modificados prova/protocolo/candidato6273, contratos consumidos, Atlas ou gate.
"""
write('NOTA_PREPARACAO_CONTROLES.md',note)
write('MANIFESTO_PREPARACAO.json',{"request_id":RID,"status":"PREPARED_ONLY_ZERO_CONTROL_EXECUTIONS","files":[pin(p) for p in sorted(BASE.iterdir()) if p.is_file()],
"source_pins":before,"next":"Independent review then explicit ROOT execution decision. Do not execute to validate preparation."})
print(json.dumps({"request_id":RID,"manifest":pin(BASE/'MANIFESTO_PREPARACAO.json'),"contract":pin(BASE/'PROTOCOLO_EXATO.json'),"AST_checks":len(checks)},ensure_ascii=False))
