from pathlib import Path
import datetime,hashlib,json,re
B=Path(__file__).resolve().parent
def pin(p):
 p=Path(p);b=p.read_bytes();return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def put(p,s):
 if isinstance(s,str):s=s.encode('utf-8')
 with p.open('xb') as f:f.write(s)
receipts=[];failed=[]
for p in sorted((B/'attempts').glob('*/RECEIPT.json')):
 r=json.loads(p.read_text(encoding='utf-8'))
 if r['passed']:receipts.append((p,r))
 else:failed.append(pin(p))
modules=[]
for name in ['BoundedWeakAnalyticR6','OrbitalContractionAnalyticR1','CanonicalGammaPositiveR3']:
 matches=[(p,r) for p,r in receipts if Path(r['source']['path']).stem==name];assert len(matches)==1,name
 p,r=matches[0];assert pin(B/(name+'.lean'))==r['source']
 assert r['exit_code']==0 and all(set(a)<={'propext','Classical.choice','Quot.sound'} for a in r['axioms'].values())
 modules.append({'source':pin(B/(name+'.lean')),'receipt':pin(p),'build':r['build_log'],'olean':r['olean'],'exit_code':r['exit_code'],'seconds':r['seconds'],'printed_axioms':r['axioms']})
p,a=next((p,r) for p,r in receipts if Path(r['source']['path']).stem=='GammaPositiveAuditR2')
counts={k:sum(k in n for n in a['axioms']) for k in ['F1Fecho.BoundedWeakAnalytic','F1Fecho.OrbitalContraction','F1Fecho.CanonicalGammaPositive']}
assert all(counts.values())
r={'unit':'F1.FECHO_20261015','claim':845,'author':'codex atrator_skeptic','status':'REAL_COMPILED_PENDING_INDEPENDENT_REVIEW','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'modules':modules,'all_local_audit':pin(p),'all_local_count':len(a['axioms']),'all_local_counts':counts,'all_local_axioms':a['axioms'],'failed_attempts_preserved':failed,'main_export':'F1Fecho.CanonicalGammaPositive.gamma_positive','stronger_export':'F1Fecho.CanonicalGammaPositive.positive_energy','construction':['V(z) is the actual exp(i z p.a) Holder multiplier on the massless orbital H1, contractive for Im(z)>=0; it is set to zero below the half-plane, outside the asserted analytic domain.','Diagonal coefficients are the finite-density spectral integrals already proved analytic in O16. Polarization derives every mixed coefficient.','The actual sectorwise bounded second quantization maps e(f) to e(V(z)f), has norm <=1 and equals the preexisting unitary gamma(U1(t a)) at the real boundary by totality of exponential vectors.','A generic uniform-coefficient estimate makes the analytic property closed in both vector arguments. Two span/closure inductions extend exponential coefficient analyticity to every vector of the same Fock.'],'conclusion':'For each a in forwardCone and psi in the canonical Fock, an analytic upper-half-plane coefficient is continuous on the closed half-plane, uniformly bounded by ||psi||^2, with real boundary <psi,gamma(U1(t a))psi>.','legacy_field':'The wrapper has the exact old OneParticlePositiveEnergy -> Γ_positive signature. The premise is unused: the stronger theorem constructs the result directly from the actual orbital dynamics.','not_claimed':['Gamma_no_fixed','KMS','all-wedge modular identification','full inhabitant of RemainingNonabelianCoreInput','physical confirmation'],'independent_review':'Required from another author before integration; this receipt is construction evidence only.','originals_memory_production_gate_modified':False}
p=B/'FINAL_GAMMA_POSITIVE_RECEIPT_R1.json';put(p,json.dumps(r,ensure_ascii=False,indent=2)+'\n')
md='# Energia positiva na Fock canônica\n\n[REAL — compilação local] Três módulos compilados em Lean 4.31, EXIT 0, zero sorry. A auditoria de todas as declarações dos três módulos, incluindo auxiliares, mantém somente propext, Classical.choice e Quot.sound.\n\nO multiplicador orbital contrativo V(z) é construído no H1 de massa zero. Seus coeficientes são analíticos pelo integral espectral O16 e polarização. A Γ limitada já construída o eleva à mesma Fock; a identidade em exponenciais e a totalidade fixam a fronteira gamma(U1(t a)). Um lema novo de limite uniforme e duas induções no span/fecho estendem a analiticidade a todos os vetores. O limite explícito é ||psi||².\n\nO teorema positivo não depende da antiga premissa OneParticlePositiveEnergy; o wrapper fornece exatamente o campo antigo com essa premissa não consumida. Nenhum pressuposto analítico sobre a Fock é acrescentado. Γ_no_fixed, KMS e o habitante do contrato completo não são reivindicados. A revisão independente é a próxima etapa; nenhum original, memória, produção ou gate foi alterado.\n'
put(B/'ENTREGA_GAMMA_POSITIVE_R1.md',md)
print(json.dumps({'receipt':pin(p),'count':len(a['axioms']),'counts':counts},ensure_ascii=False))
