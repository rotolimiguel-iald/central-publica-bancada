from pathlib import Path
import datetime,hashlib,json,re
B=Path(__file__).resolve().parent
P=B.parent
CAN=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return {'path':str(p),'sha256':sha(p),'bytes':Path(p).stat().st_size}
def put(p,raw):
 if isinstance(raw,str):raw=raw.encode('utf-8')
 with p.open('xb') as f:f.write(raw)
 assert p.read_bytes()==raw
receipts=[]
for name in ['net','flow','maxwell']:
 p=B/name/'RECEIPT_R1.json';r=json.loads(p.read_text(encoding='utf-8'));assert r['passed'] and r['exit_code']==0 and r['source_exact_copy']
 for key in ['source','stdout','stderr','olean','log','original_receipt']:
  assert sha(r[key]['path'])==r[key]['sha256']
 for x in r['dependencies_before_after']:assert sha(x['path'])==x['sha256']
 receipts.append((p,r))
sources=[CAN/'TGLExt'/n for n in ['V350DualFixedCore.lean','TheOathOnTheTower.lean','TheConjugationMapsCommutants.lean','Commutant.lean','QGSolutionComplete.lean','FlagNetV31.lean','TheImportedSecondQuantization.lean','MaxwellLiteratureBridge.lean','ContratoQG_v31.lean','ContratoQG_v31_Teoremas.lean']]
for n in ['MaxwellLiteratureBridge.lean','TheImportedSecondQuantization.lean','ContratoQG_v31.lean','ContratoQG_v31_Teoremas.lean']:
 assert (CAN/'TGLExt'/n).read_bytes()==(P.parent/'F1.TEMPO.V394/candidate_r2/tgl_kernel/TGLExt'/n).read_bytes()
claims=[
 {'topic':'rede','verdict':'PASSA_CONDICIONAL','statute':'REAL','finding':'R(W,K) é o duplo comutante dos geradores W(K) quando hstar garante fecho por star. R_mono usa monotonicidade do bicomutante; R_local usa comutação dos geradores e colapso do triplo comutante; R_cov usa o transporte pelo star-algebra equivalence e hcov nos geradores. As conclusões R_* não são hipóteses.'},
 {'topic':'fluxo','verdict':'PASSA_CONDICIONAL','statute':'REAL','finding':'A ação é a conjugação pela gamma concreta de B0(-2*pi*t), no mesmo Fock F. L.K_boost e hcov dão invariância da álgebra da cunha; restrictAutomorphism produz a restrição com inversa e leis de grupo. Não substitui por automorfismo abstrato sem implementação.'},
 {'topic':'Maxwell','verdict':'PASSA_CONDICIONAL','statute':'REAL','finding':'BoostChargeIdentity afirma derivada de coeficiente matricial do boost efetivo igual a i vezes a carga integrada. linked_modular_charge deriva o fator 2*pi pela reparametrização BW e unicidade da derivada. Não recebe charge_link pronto. NonzeroChargeState fornece carga diferente de zero em Regular, que inclui norma 1; a testemunha modular não nula é derivada.'},
 {'topic':'tipos','verdict':'PASSA','statute':'REAL','finding':'Maxwell preserva o mesmo C:FockCertificate L, Q:MaxwellQuadraticForm C, relógio N, domínio e tensor toStress Q. assembled_tensor_is_original é rfl; on_domain usa a extensão existente por zero somente fora do domínio. standardWedgeH3 usa exatamente esse tensor, não outro substituto.'},
]
limits=[
 'Nenhuma família concreta W/CCR foi construída: hstar, comutação local e covariância de geradores são entradas. O critério não abeliano requer um par de geradores não comutantes; não produz esse par.',
 'Nenhum habitante físico LightNetData/FockCertificate/MaxwellQuadraticForm com essas novas hipóteses foi exibido. A tipagem das pontes não demonstra sua existência conjunta.',
 'O fluxo restrito tem leis algébricas de grupo e implementação concreta; esta pedra não prova continuidade forte, KMS, ciclicidade/separação do vácuo ou igualdade com o grupo modular do vácuo.',
 'O nome MaxwellQuadraticForm é o registro herdado; fornecer Q físico/Wick, a identidade diferencial boost-carga e estado regular de carga não nula continua obrigação, não consequência desta fiação.',
 'A forma zero está excluída pelo requisito explícito de carga não nula; isso não substitui a exibição de um estado físico que o satisfaça.',
 'H3 entregue refere-se à cunha padrão e direção nula fixa. Não fecha por si só família de Lorentz de todas as cunhas nem H3 curvo em toda direção.',
 'Flow R4 recompila com os mesmos 46 registros de axiomas (incluindo auxiliares), mas seu .olean difere: 317656 versus 317672 bytes. Os dois serializam caminhos de fonte diferentes no offset 313472, junto ao aviso de linter. Não se alega identidade binária nem decodificação completa dessa diferença.',
 'WeylFlow R1/R2/R3 falharam no construtor e ficam fora do aceite. A revisão recompilou apenas o fonte aceito indicado no recibo próprio; originais e tentativas históricas preservados.',
 'Revisão em sandbox de componentes. Não executou rito integral, main, memória, produção, kernel original, dado observado ou gate.'
]
items=[]
for p,r in receipts:
 items.append({'receipt':pin(p),'source':r['source'],'exit':r['exit_code'],'seconds':r['seconds'],'axiom_count':r['axiom_count'],'olean_identical_to_accepted':r['olean_identical_to_accepted'],'source_exact':r['source_exact_copy']})
md='''# Revisão independente — rede Weyl, fluxo e ponte boost–carga

**PASSA no escopo condicional; nenhum achado material bloqueante.** Claim 845, Codex `/root/atrator_skeptic`. AUDITADA/FECHADA permanecem atos da gerência.

## O que a fiação efetivamente constrói [REAL]

R(W,K) é o bicomutante de W(K), com fecho por star derivado de `hstar`. Monotonicidade, localidade e covariância são transportadas dos geradores para a álgebra: a prova consome a monotonicidade do bicomutante, o colapso do triplo comutante e o transporte por equivalência. Não assume como entrada as conclusões R_mono/R_local/R_cov. A não comutatividade da álgebra exige um par não comutante de geradores.

O fluxo restrito é a conjugação por `gamma (B0 (−2πt))` no Fock concreto, restrita à álgebra da cunha. A invariância vem de `L.K_boost` e da covariância de W; inversa e composição são construídas. As leis de grupo não afirmam aqui continuidade, KMS ou identificação com o grupo modular do vácuo.

A ponte Maxwell começa com a identidade diferencial do boost real e sua carga integrada, no mesmo certificado C, forma Q e domínio. A reparametrização `−2πt` e a unicidade da derivada dão a carga modular `2πQ`; não se recebe `charge_link` pronto. O estado regular de carga não nula é hipótese nomeada; dele segue energia modular não nula. O tensor montado é literalmente `toStress Q` e coincide com Q no domínio. A extensão por zero fora dele já pertence à ponte herdada.

## Escopo e vacuidade

W concreto/CCR, um habitante da rede física, Q/Wick físico, identidade boost–carga e estado regular não nulo continuam por construir ou fornecer. O registro `Regular` exige norma 1; a hipótese de carga não nula exclui tensor sempre zero, mas não é uma construção de habitante. As três pontes tipam componentes compatíveis nas respectivas entradas; não exibem por si um único habitante físico conjunto. H3 é o da cunha padrão/direção fixa, sem afirmar família de Lorentz ou H3 curvo em toda direção.

## Recompilação independente

'''
for item in items:
 md+=f"- `{Path(item['source']['path']).name}`: EXIT {item['exit']}, {item['seconds']:.6f} s, {item['axiom_count']} declarações somente no trio; cópia exata e `.olean` idêntico ao aceito: {item['olean_identical_to_accepted']}.\n"
md+='''
No Flow, as 46 declarações incluem auxiliares gerados. Seu `.olean` difere em tamanho e contém o caminho distinto da fonte serializado junto ao aviso de linter (offset 313472). Os nomes e axiomas coincidem integralmente; não se alega identidade binária ou decodificação completa da diferença. Nota pinada: `FLOW_BINARY_NOTE_R1.json`.

Comandos, toolchain Lean 4.31.0, LEAN_PATH literal, início/fim, stdout/stderr, hashes antes/depois e `.olean` constam dos três recibos pinados pelo JSON. Tentativas recusadas do Flow não foram consumidas como evidência aceita. Não houve edição de fonte do construtor, memória, produção, dados ou gate.
'''
put(B/'REVISAO_REDE_MATERIA_R1.md',md)
report={'unit':'F1.FECHO_20261015','claim_event':845,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'/root/atrator_skeptic','verdict':'PASSA_COMPONENTES_CONDICIONAIS','material_blocking_findings':[],'binary_scope_note':pin(B/'FLOW_BINARY_NOTE_R1.json'),'builds':items,'all_axioms_subset':['propext','Classical.choice','Quot.sound'],'claims':claims,'limits':limits,'source_context':[pin(p) for p in sources],'delivery_maxwell':pin(P/'matter_h3_inventory/DELIVERY_R1.json'),'failed_flow_attempts':[pin(p) for p in (P/'weyl_net_wiring/attempts').glob('*/RECEIPT.json') if json.loads(p.read_text(encoding='utf-8'))['exit_code'] != 0],'markdown':pin(B/'REVISAO_REDE_MATERIA_R1.md'),'sealing_script':pin(__file__),'originals_memory_production_gate_touched':False}
put(B/'REVISAO_REDE_MATERIA_R1.json',json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'report':pin(B/'REVISAO_REDE_MATERIA_R1.json'),'md':report['markdown'],'verdict':report['verdict']},ensure_ascii=False))
