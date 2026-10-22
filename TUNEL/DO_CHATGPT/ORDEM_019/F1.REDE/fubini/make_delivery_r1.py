from pathlib import Path
import hashlib, json, re, datetime
B=Path(__file__).resolve().parent
A=B/'attempts'/'20261013T213116_037514Z'
K=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
def rec(p):
 b=p.read_bytes(); return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(p,b):
 with p.open('xb') as f: f.write(b)
 assert p.read_bytes()==b
r=json.loads((A/'RECEIPT.json').read_text(encoding='utf-8'))
src=(A/'FubiniL2.lean').read_text(encoding='utf-8')
axioms=(A/'AXIOMS.txt').read_text(encoding='utf-8')
assert r['exit_code']==0
assert (B/'FubiniL2.lean').read_bytes()==(A/'FubiniL2.lean').read_bytes()
assert not re.search(r'\b(sorry|admit|axiom)\b',src)
assert 'sorryAx' not in axioms
rows=re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]",axioms)
assert rows and all(set(a.split(', ')) <= {'propext','Classical.choice','Quot.sound'} for _,a in rows)
deps=[K/'TGLExt'/'LightNetStandardWedgeDataBGL.lean',K/'TGLExt'/'TheImportedSecondQuantization.lean',K/'TGLExt'/'O16'/'OrbitalBoostTransport.lean',K/'TGLExt'/'O16'/'OrbitalRapidityMeasure_v4.lean',K/'TGLExt'/'V351FourierTranslation.lean',K/'.lake'/'packages'/'mathlib'/'Mathlib'/'MeasureTheory'/'Integral'/'Prod.lean',K/'.lake'/'packages'/'mathlib'/'Mathlib'/'MeasureTheory'/'Function'/'SimpleFuncDenseLp.lean',K/'.lake'/'packages'/'mathlib'/'Mathlib'/'MeasureTheory'/'Measure'/'SeparableMeasure.lean',K/'lean-toolchain',K/'lake-manifest.json']
m={'unit':'F1.REDE','scope':'D1a.1 vector-valued L2 Fubini on unchanged canonical H1, plus explicit boost/Fourier intertwining','status':'CANDIDATE_KERNEL_CHECKED_AWAITS_INDEPENDENT_REVIEW','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'final_attempt':str(A),'build':r,'artifacts':[rec(p) for p in (B/'FubiniL2.lean',B/'build_fubini.py',Path(__file__),A/'RECEIPT.json')],'dependencies_read_only':[rec(p) for p in deps],'attempt_receipts':[rec(p) for p in sorted((B/'attempts').glob('*/RECEIPT.json'))],'declaration_count':len(re.findall(r'^(?:noncomputable )?(?:def|theorem) ',src,re.M)),'axiom_checks':rows,'source_has_sorry_admit_axiom':False,'canonical_hilbert_unchanged':True,'uses_assumed_fubini':False,'out_of_scope':['J_W construction','self-adjoint half-modular operator','standard wedge subspace','complete 4D light net','second quantization','physical confirmation'],'production_mutated':False,'new_junctions':False}
save(B/'DELIVERY_R1.json',(json.dumps(m,ensure_ascii=False,indent=2)+'\n').encode())
readme='''# F1.REDE — ponte de Fubini L² vetorial, R1

[REAL — compilação local; revisão independente pendente] `FubiniL2.lean` constrói a equivalência, sem assumi-la como campo.
A aplicação é a seção f(q,r) ↦ (r ↦ [q ↦ f(q,r)]), totalizada por zero somente onde a seção não é L² (conjunto nulo provado).
Prova: mensurabilidade pelas distâncias; Fubini do quadrado da norma; linearidade no quociente; sobrejetividade por indicadores finitos e imagem fechada.
Hipóteses genéricas explícitas: medidas SFinite, medida transversal separável, fibra Hilbert real separável e completa, ação escalar normada.
A especialização `canonicalFub` habita o tipo exato `Lp Fib 2 momentumMeasure ≃ₗᵢ[ℂ] RapidityHilbert`; H1, Fib e a medida canônicos permanecem os mesmos.
`canonicalFub_sections` fixa a ação a.e.; `canonicalFub_shift` e `canonical_toRapidity_boost` provam o entrelaçamento, evitando uma identificação abstrata arbitrária.
`canonicalPartialFourier` é a composição efetiva da carta existente, Fubini e Fourier L² vetorial já disponível.
`canonicalPartialFourier_boost` dá o multiplicador 2πs; para B0(−2πt), `canonicalSigma ξ = 4π²ξ` e `canonical_modularGroupIsBoost` comprovam o sinal e a normalização.
[OPEN] J_W, T = Δ^(1/2), Δ = S†S, StandardSubspace e a rede completa não são construídos nesta etapa; nenhum habitante D1a3OutputBGL é reivindicado.
Build final: `attempts/20261013T213116_037514Z`; EXIT 0, 17 declarações impressas apenas com propext/Classical.choice/Quot.sound, zero sorry/admit/axioma novo na fonte.
`BUILD.log` traz comando, toolchain, LEAN_PATH literal, início, fim, segundos e exit; `RECEIPT.json` pina fonte, .olean, log e transcrito de axiomas.
`DELIVERY_R1.json` pina esta entrega, dependências lidas e todos os recibos de tentativa. Nenhum arquivo do Nós, produção, memória, quadro ou gate foi alterado; nenhuma junção foi criada.
'''
save(B/'README_R1.md',readme.encode())
print(json.dumps({'manifest':rec(B/'DELIVERY_R1.json'),'readme':rec(B/'README_R1.md'),'source':rec(B/'FubiniL2.lean'),'declarations':m['declaration_count'],'axiom_checks':len(rows),'start':r['start_utc'],'end':r['end_utc'],'seconds':r['seconds']},ensure_ascii=False))