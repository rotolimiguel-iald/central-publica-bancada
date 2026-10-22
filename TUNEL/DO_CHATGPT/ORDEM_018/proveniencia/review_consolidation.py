"""Bounded consistency audit of F0/F2 consolidation; no data centres or fits."""
from pathlib import Path
import json,hashlib,math,datetime
from audit_provenance import OUT,atomic,metadata
ROOT=OUT.parent
sources={};checks=[]
def record(path,expected=None):
 p=Path(path);key=str(p)
 if key not in sources:
  m,b=metadata(p);sources[key]=m
 else:b=p.read_bytes()
 if expected is not None:
  same=hashlib.sha256(b).hexdigest()==expected
  checks.append({'check':'reference_identity','path':key,'passed':same})
  assert same,key
 return b
names=['ENTREGA_018_F0_RANKING.md','F0_RANKING_REGISTRY.json','ENTREGA_018_F2_DERIVACOES.md','F0_POWER_PROTOCOL_V1.json','F0_POWER_PROTOCOL_HASHES.json','F0_POWER_RESULT.json','poder_f0.py','F0_UPDATED_SIGMAS_PROTOCOL.json','F0_UPDATED_SIGMAS_PROTOCOL_SEAL.json','F0_UPDATED_SIGMAS_RESULT.json','F0_ADDITIONAL_POWER_PROTOCOL.json','F0_ADDITIONAL_POWER.json','F0_SIMONS_PROTOCOL.json','F0_SIMONS_RESULT.json','FONTES_PUBLICAS.json','FONTES_PUBLICAS_ADICIONAIS.json','FONTES_ATUALIZACAO_F0.json','FONTE_SIMONS.json','derivacoes/NOTA_DERIVACOES_F2.md','derivacoes/ERRATA_R_G_FPHI.md','derivacoes/MANIFESTO_F2.json','derivacoes/F2_CALCULOS_CONDICIONAIS.json','derivacoes/F2_FONTES_SHA256.json','derivacoes/poder_forma/PODER_FORMA.json','derivacoes/poder_forma/NOTA_PODER_FORMA.md','derivacoes/R_I_PISO_E_PERFIL.md','preregistros/primordial/CALCULO_SENSIBILIDADES_SIGMAS.json','VERIFICACAO_INDEPENDENTE_RINGDOWN_SHAPE.json','proveniencia/REVISAO_ADVERSARIAL_F2_FONTES.json','proveniencia/REVISAO_PODER_FORMA.json']
blobs={n:record(ROOT/n) for n in names}
def obj(n):return json.loads(blobs[n])
def ok(name,cond,detail=None):
 checks.append({'check':name,'passed':bool(cond),'detail':detail});assert cond,name
# Compare only archived identities, without decoding archived scientific HTML or observed tables.
archive_count=0
for n in ['FONTES_PUBLICAS.json','FONTES_PUBLICAS_ADICIONAIS.json','FONTES_ATUALIZACAO_F0.json','FONTE_SIMONS.json']:
 data=obj(n)
 entries=data if isinstance(data,list) else [data]
 for item in entries:
  if 'path' in item and 'sha256' in item:
   record(item['path'],item['sha256']);archive_count+=1
for n in ['F0_POWER_RESULT.json','F0_UPDATED_SIGMAS_RESULT.json','F0_ADDITIONAL_POWER.json','F0_SIMONS_RESULT.json']:
 r=obj(n)
 for k in ['protocol','script']:
  if k in r:record(r[k]['path'],r[k]['sha256'])
seal=obj('F0_POWER_PROTOCOL_HASHES.json')
ok('F0_protocol_seal',hashlib.sha256(blobs['F0_POWER_PROTOCOL_V1.json']).hexdigest()==seal['protocol_sha256'])
ok('F0_script_seal',hashlib.sha256(blobs['poder_f0.py']).hexdigest()==seal['script_sha256'])
reg=obj('F0_RANKING_REGISTRY.json');routes={r['route']:r for r in reg['routes']}
ok('13_unique_routes',len(routes)==13==len(reg['routes']))
f0=blobs['ENTREGA_018_F0_RANKING.md'].decode('utf-8');f2=blobs['ENTREGA_018_F2_DERIVACOES.md'].decode('utf-8')
for route,entry in routes.items():
 ok('registry_text_'+route,all(entry[k] in f0 for k in ['prediction','statute','data','separation','decision','map']))
# Document pins: unchanged numeric artifacts and original reviewed note prefix.
previous=obj('proveniencia/REVISAO_ADVERSARIAL_F2_FONTES.json')
for n in ['f2_analysis.py','F2_CALCULOS_CONDICIONAIS.json']:
 ref=next(s for s in previous['sources'] if Path(s['path']).name==n);record(ROOT/'derivacoes'/n,ref['sha256'])
oldnote=next(s for s in previous['sources'] if Path(s['path']).name=='NOTA_DERIVACOES_F2.md')
ok('reviewed_F2_original_prefix_preserved',hashlib.sha256(blobs['derivacoes/NOTA_DERIVACOES_F2.md'][:oldnote['bytes']]).hexdigest()==oldnote['sha256'])
shapeaudit=obj('proveniencia/REVISAO_PODER_FORMA.json')
shaperef=next(s for s in shapeaudit['sources'] if Path(s['path']).name=='PODER_FORMA.json')
record(ROOT/'derivacoes/poder_forma/PODER_FORMA.json',shaperef['sha256'])
# Arithmetic identities from frozen forecast outputs only: no observational means or refit.
p=obj('F0_POWER_PROTOCOL_V1.json');f=p['fiducials_INPUT_not_measured_centres'];b=f['alpha_CODATA2018']*math.sqrt(math.e)
e2=f['Omega_m']*(1+f['zstar'])**3+f['Omega_r']*(1+f['zstar'])**4+1-f['Omega_m']-f['Omega_r'];K=e2**(b/3);delta=(K-1)*f['Hfid']
power=lambda D:.5*math.erfc((5-D)/math.sqrt(2))+.5*math.erfc((5+D)/math.sqrt(2))
fr=obj('F0_POWER_RESULT.json');ur=obj('F0_UPDATED_SIGMAS_RESULT.json');ar=obj('F0_ADDITIONAL_POWER.json');sr=obj('F0_SIMONS_RESULT.json')
arithmetic=[]
for item in fr['hubble']:
 sigma=math.sqrt(sum(x*x for x in p['local_sigma_components'][item['method']]));D=delta/math.hypot(sigma,K*p['background_sigma']['sigma']);P=power(D)
 ok('Hubble_D_'+item['method'],abs(D-item['expected_separation'])<1e-12)
 ok('Hubble_power_'+item['method'],abs(P-item['power_at_5sigma_unadjusted'])<1e-12)
 arithmetic.append({'id':item['method'],'D':D,'power_bilateral_absZ_gt5':P})
D=delta/math.hypot(ur['h0dn']['sigma'],K*p['background_sigma']['sigma']);P=power(D)
ok('H0DN_D',abs(D-ur['h0dn']['expected_separation'])<1e-12);ok('H0DN_power',abs(P-ur['h0dn']['gaussian_power_at_5sigma'])<1e-12)
arithmetic.append({'id':'H0DN','D':D,'power_bilateral_absZ_gt5':P})
cnu=(7/8)*(4/11)**(4/3);dn=(4*b/3)*(1/cnu+f['Neff_SM'])
ok('delta_Neff',abs(dn-fr['neff']['delta'])<1e-12)
ok('Simons_D',abs(dn/sr['sigma']-sr['expected_separation'])<1e-12)
for a in ur['act']:ok('ACT_'+a['combination'],abs(dn/a['sigma']-a['expected_separation'])<1e-12)
prim=obj('preregistros/primordial/CALCULO_SENSIBILIDADES_SIGMAS.json')
old03=next(x for x in prim['cmb_sigma_only_scenarios'] if x['id']=='CMB_S4_BBN_consistency_historical')
old09=next(x for x in prim['cmb_sigma_only_scenarios'] if x['id']=='CMB_S4_Yp_free_historical')
s4line=next((l for l in f0.splitlines() if 'cenário histórico CMB-S4' in l),'')
rf_f0=next(l for l in f0.splitlines() if '**R-F ' in l);rf_f2=next(l for l in f2.splitlines() if l.startswith('| R-F |'))
findings=[]
if 'BBN' not in s4line:
 findings.append({'id':'CONS-01','severity':'P2_scope_condition','file':'ENTREGA_018_F0_RANKING.md','line':f0.splitlines().index(s4line)+1,'issue':'The historical CMB-S4 sigma_Neff=.03 omits its assumed BBN consistency relation. The cited JSON separately has .09 for free Yp.','remedy':'Add explicit BBN-consistency condition to .03; retain historical/no-calendar label; this is a theoretical BBN-consistency condition, not proof of reuse of abundance data. Do not transfer .03 to free Yp or modified BBN without a consistent joint treatment.','evidence':{'BBN_consistency':old03,'Yp_free':old09}})
if not all('adiab' in x.lower() for x in [rf_f0,rf_f2,routes['R-F']['prediction']]):
 findings.append({'id':'CONS-02','severity':'P2_scope_condition','files':['ENTREGA_018_F0_RANKING.md','F0_RANKING_REGISTRY.json','ENTREGA_018_F2_DERIVACOES.md'],'lines':{'F0':f0.splitlines().index(rf_f0)+1,'F2':f2.splitlines().index(rf_f2)+1},'issue':'Conservative dephasing is compressed into the cosmological temperature law without restating the same-H basis, usual geometric redshift and adiabatic expansion required in original F2 line60. Trace conservation alone does not derive T(z).','remedy':'Restore same-H dephasing, usual geometric redshift and adiabatic expansion before T=T0(1+z), and preserve blackbody/photon-number conditions for nonzero gamma_T.'})
report={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Frozen F0/F2 consolidation review against prior audited artifacts and conditional design JSON; no rites, fits, new centres, original code execution, remote executor or network','sources':list(sources.values()),'archived_reference_records_checked':archive_count,'checks':checks,'checks_passed':sum(x['passed'] for x in checks),'arithmetic_crosschecks':arithmetic,'findings':findings,'supported':['f_phi fit/true direction and corrected H ratio','Q integral and published shape separation; no endpoint swap','amplitude and Omega_m projection scope maintained','no 2027 or 2030 estimator forecast fabricated; Simons horizon2034 remains separate','A/B maps not merged and OPEN bridges preserved','H0DN vs SH0ES/CCHP, Planck/ACT, ACT+BBN vs BBN, SN/duality, lens Pantheon dependence and JUNO/NuFIT overlaps preserved; theoretical BBN consistency is distinct from shared observed data','Gaussian power R-A refers only to explicit abs(Z)>5 design, not observed significance or a five-model calibrated test'],'limitations':['archived public byte identity checked without opening their scientific centre values','no new public-source content validation or historical execution certification','primordial and ringdown figures compared as supplied review artifacts, not new independent physical verification'],'new_observed_centres_opened':False,'original_programs_run':False,'fits_or_rites_run':False,'new_remote_executor':False}
atomic(OUT/'REVISAO_CONSOLIDACAO_F0_F2.json',json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
print(json.dumps({'checks_passed':report['checks_passed'],'sources':len(sources),'archived_records':archive_count,'findings':findings,'arithmetic':arithmetic},ensure_ascii=False,indent=2))
