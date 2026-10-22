"""Five public abstracts to the already-opened scalar V1; no scientific execution."""
from pathlib import Path
import hashlib, json, math, sys
sys.path.insert(0,r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
from iald_orchestrator.safe_files import save_json, replace_bytes, utc_now
ROOT=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018')
OUT=Path(__file__).resolve().parent
BANC=Path(r'C:\IALD\Bancada_Um\investigacao')
def pin(p):
 b=p.read_bytes()
 return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def lines(p,needle):
 found=[i+1 for i,l in enumerate(p.read_text(encoding='utf-8').splitlines()) if needle in l]
 assert found,(p.name,needle)
 return found
rp=BANC/'fase9_hubble_abertura/RESULTADO_FASE9_V1_20261006_110507.json'
vp=BANC/'preregistro_fase9_hubble/PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V1.json'
result=json.loads(rp.read_bytes()); v1=json.loads(vp.read_bytes())
rows=result['primario']['z_por_leitor']
assert 'ALVOS_FASE9_LIDOS.json AUSENTE' in result['R1_alvos']
items=[
('L1_sh0es_r22',ROOT/'fontes_publicas/sh0es_2022.html','2112.04510v3','H0=73.04+-1.04',73.04,[1.04],'identity','Cefeidas + SN Ia; inclui sistemáticos. Âncoras Gaia EDR3, NGC4258 e LMC; Pantheon+ no fluxo de Hubble.'),
('L2_cchp',ROOT/'fontes_publicas/cchp_2025_v3.html','2408.06153v3',r'70.39 $\pm$ 1.22',70.39,[1.22,1.33,.70],'quadrature','TRGB sozinho, 24 calibradores SN Ia HST+JWST; NGC4258 como zero point. Erros estatístico, sistemático e sigma_SN.'),
('L3_sbf',OUT/'sbf_2502.15935v2.html','2502.15935v2',r'73.8\pm 0.7',73.8,[.7,2.3],'quadrature','SBF calibrado por TRGB JWST com âncora NGC4258; fonte descreve independência de Cefeidas e SN Ia. Erros estatístico e sistemático separados.'),
('L4_masers',OUT/'masers_2001.09213v2.html','2001.09213v2',r'73.9 \pm 3.0',73.9,[3.0],'identity','Seis galáxias, incluindo NGC4258; incerteza peculiar fixa250 km/s, sem correção de velocidades peculiares no valor principal.'),
('L5_tdcosmo',ROOT/'fontes_publicas/tdcosmo_2025_v4.html','2506.03023v4',r'71.6^{+3.9}_{-3.3}',71.6,[3.9,3.3],'arithmetic_mean','Oito quasars com atrasos, em LambdaCDM plano, usando restrição Omega_m de Pantheon+. Erros assimétricos; combinação SLACS/SL2S é outro resultado.')]
readers=[]
for key,path,arxiv,needle,center,components,transform,context in items:
 sigma=math.sqrt(sum(x*x for x in components)) if transform=='quadrature' else sum(components)/2 if transform=='arithmetic_mean' else components[0]
 old=rows[key]
 assert old['H0']==center==v1['spec']['leitores'][key]['H0']
 assert math.isclose(old['sigma'],sigma,rel_tol=0,abs_tol=1e-12)
 assert old['sigma']==v1['spec']['leitores'][key]['sigma']
 readers.append({'reader_id':key,'source':pin(path),'primary_version_url':'https://arxiv.org/abs/'+arxiv,'evidence_line_numbers':lines(path,needle),'short_literal_anchor':needle,'H0_published':center,'sigma_published_components':components,'local_transform':transform,'sigma_reconstructed':sigma,'sigma_frozen':old['sigma'],'absolute_difference':abs(old['sigma']-sigma),'numeric_transcription_matches':True,'context':context,'status':'REAL_DOCUMENTARY_MATCH_AND_ARITHMETIC_ONLY','source_statute':'KNOWN_PUBLISHED_RESULT_NOT_REMEASURED','statistical_admission':'NOT_AUTOMATIC_GAUSSIAN_APPROXIMATION_AND_CROSS_COVARIANCE_REQUIRE_REVIEW','frozen_metadata':v1['spec']['leitores'][key]})
provenance=[
(BANC/'fase3_leitores_h0/preregistro_fase3.py',[24,25,49,50,52]),
(BANC/'fase3_leitores_h0/PREREGISTRO_FASE3_LEITORES_20260930.json',[127,128,129,130,131,145,146,147,148,149]),
(BANC/'preregistro_fase9_hubble/gerar_preregistro_fase9_hubble_06out.py',[120,127]),
(BANC/'fase9_hubble_abertura/rodar_fase9_v1.py',[60,61,64,65,112,175,177])]
issues=[
{'id':'D1_CCHP_METHOD_LABEL','finding':'L2 tipo diz TRGB+JAGB+Cef, mas70.39 é TRGB sozinho na fontev3. cefeida=false já existe no congelado; erro do rótulo não implica mudança automática da classificação numérica.'},
{'id':'D2_SBF_DEPENDENCY_FLAGS','finding':'L3 tem grupo_SN=true e grupo_4258=false. A fonte descreve rota independente de SN Ia, calibrada via NGC4258. Revisar interpretação dos grupos e regra de covariância antes de novo composto; não apenas inverter flags.'},
{'id':'D3_MASER_SHARED_OBJECT','finding':'L4 tem grupo_4258=false, mas NGC4258 integra as seis galáxias publicadas. Objeto compartilhado não determina sozinho covariância; requer rastrear medições reutilizadas e pesos.'},
{'id':'D4_TDCOSMO_EXTERNAL_CONSTRAINT','finding':'L5 tem grupo_SN=false, embora Pantheon+ forneça restrição Omega_m. Isso não equivale à calibração SN da escada nem fixa covariância cruzada; a dependência deve constar explicitamente.'},
{'id':'D5_ERROR_COMPRESSION','finding':'Quadraturas CCHP/SBF e média dos lados TDCOSMO reproduzem erros do V1. São compressões locais documentadas, não recuperação da verossimilhança original nem prova de independência dos componentes.'},
{'id':'D6_MEMBERSHIP_IS_NOT_HASH_VERIFICATION','finding':'Runner linhas65,175,177 carrega ALV e usa presença da chave para REAL por hash/contagem de declarados. Nesse ponto não verifica bytes das fontes nem revisão da covariância. Não criar ALVOS_FASE9_LIDOS.json a partir deste vínculo como admissão.'}]
payload={'schema':'F9_SCALAR_V1_DOCUMENTARY_BINDING_V1','created_at':utc_now(),'scope':'Five published scalar readers; documentary matching and three elementary error compressions only. No raw data, likelihood, composite, provider, um.py or runner execution.','alternatives_before_check':[{'id':'A','action':'Apenas referências bibliográficas, sem vínculo numérico.','selected':False},{'id':'B','action':'Vínculo por bytes/hash e compressões/erratas, sem admissão ou veredito.','selected':True}],'frozen_result':pin(rp),'frozen_v1':pin(vp),'original_R1':result['R1_alvos'],'source_archive_receipt':pin(OUT/'NEW_PUBLIC_SOURCES.json'),'existing_source_catalog':pin(ROOT/'FONTES_PUBLICAS.json'),'readers':readers,'provenance':[dict(pin(p),relevant_lines=ls,mode='STATIC_READ_NOT_EXECUTED') for p,ls in provenance],'documentary_findings':issues,'numbers_supported':5,'statistical_admission_decided':False,'originals_modified':False,'verdict_recomputed':False,'official_verdict_changed':False,'distinction':'Scalar manager V1 differs from ROOT full joint comparison; admission/results do not transfer.','next':'Independent documentary review. Preserve frozen V1 and INCONCLUSIVE_SYSTEMATICS. Explicitly decide semantics/covariance and audited intake before any new run.'}
jp=OUT/'VINCULO_DOCUMENTAL_CINCO_LEITORES.json'; mp=OUT/'CORRECOES_DOCUMENTAIS.md'
assert not jp.exists() and not mp.exists(),'Existing artifacts: inspect instead of overwrite'
save_json(jp,payload)
text="""# Fase 9 escalar — fontes dos cinco leitores e correções ao lado

[REAL documental] Os cinco valores centrais e as incertezas usados no V1 escalar têm correspondência nos resumos primários arquivados por SHA-256. Três arquivos foram reutilizados e dois coletados agora. Não houve reexecução do composto nem admissão automática.

| Leitor | Valor publicado (km/s/Mpc) | Transformação local de sigma |
|---|---|---|
| SH0ES R22 v3 | 73,04 ±1,04, com sistemáticos | identidade |
| CCHP v3 | 70,39 ±1,22(stat) ±1,33(sys) ±0,70(sigma_SN) | quadratura =1,935794410571536 |
| SBF v2 | 73,8 ±0,7(stat) ±2,3(sys) | quadratura =2,4041630560342613 |
| Masers v2 | 73,9 ±3,0 | identidade |
| TDCOSMO v4 | 71,6 +3,9/−3,3 | média dos lados =3,6 |

[KNOWN] Resultados publicados pelos autores. [REAL] Transcrição, aritmética elementar dos erros e integridade conferidas aqui. Não reproduz medições ou verossimilhanças dos artigos.

## Correções e limites

"""
text+='\n\n'.join('**'+q['id']+'** — '+q['finding'] for q in issues)
text+="""

A presença de NGC4258 em métodos distintos e o uso de Pantheon+ não permitem inventar covariâncias. O próprio V1 qualifica a covariância cruzada como estimativa de desenho. Os resumos não a promovem a covariância publicada. A simetrização TDCOSMO preserva o resumo escolhido, não a verossimilhança.

O resultado oficial continua INCONCLUSIVE_SYSTEMATICS. ALVOS_FASE9_LIDOS.json não foi criado; V1 e runner intactos; z_disc/evidência não recalculados. d72/P3 e a comparação conjunta ROOT permanecem separados.

## Fontes primárias

"""
for q in readers:
 text+='- ['+q['reader_id']+']('+q['primary_version_url']+'): arquivo '+q['source']['path']+', SHA-256 '+q['source']['sha256']+', linhas '+','.join(map(str,q['evidence_line_numbers']))+'.\n'
text+='\nO JSON registra bytes, hashes, metadados congelados, procedência textual dos erros e limites. Revisão independente entregue separadamente.\n'
replace_bytes(mp,text.encode('utf-8'))
manifest={'schema':'F9_SCALAR_READER_DOCUMENTARY_MANIFEST_V1','created_at':utc_now(),'status':'PREPARED_FOR_INDEPENDENT_DOCUMENTARY_REVIEW','files':[pin(Path(__file__)),pin(jp),pin(mp),pin(OUT/'NEW_PUBLIC_SOURCES.json')],'source_files':[q['source'] for q in readers],'frozen_inputs':[pin(rp),pin(vp)],'scientific_execution':False,'verdict_changed':False}
save_json(OUT/'MANIFESTO.json',manifest)
print(json.dumps({'status':manifest['status'],'readers':len(readers),'binding':pin(jp),'report':pin(mp),'manifest':pin(OUT/'MANIFESTO.json')},ensure_ascii=False,indent=2))
