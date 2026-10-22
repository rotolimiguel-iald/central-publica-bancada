"""Seal documentary verdict candidate and register separately executed theory controls."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,importlib.util,json,sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;CENTRAL=Path(r'C:\IALD\Central de Patentes')
ID='18dced03-6d38-4a2e-a2c8-a44ab39ed171'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(name,obj):
 p=HERE/name;b=(json.dumps(obj,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode();t=p.with_name(p.name+'.new')
 if p.exists():raise FileExistsError(p)
 with t.open('xb') as f:f.write(b)
 assert t.stat().st_size==len(b);t.rename(p)
def textnew(name,text):
 p=HERE/name;t=p.with_name(p.name+'.new');b=text.encode()
 if p.exists():raise FileExistsError(p)
 with t.open('xb') as f:f.write(b)
 assert t.stat().st_size==len(b);t.rename(p)
spec=importlib.util.spec_from_file_location('memory_append',CENTRAL/'Chatgpt/TGL_BANCADA_OFICIAL/record_universe_delivery.py');mem=importlib.util.module_from_spec(spec);spec.loader.exec_module(mem)
background=ROOT/'f9_background_prediction'
rpath=background/'THEORY_CONTROL_ROOT_RECEIPT.json';cpath=background/'theory_controls_01/CONTROL_RECEIPT.json'
r=json.loads(rpath.read_text());c=json.loads(cpath.read_text())
assert sha(cpath)==r['receipt']['sha256'];assert sha(background/'background_controls.py')==r['engine']['sha256']==c['engine_sha256'];assert sha(background/'PROTOCOL.json')==r['protocol']['sha256']==c['protocol_sha256']
assert c['solver_calls_attempted']==10 and len(c['results'])==5 and all(x['status']=='PASS_AT_LISTED_POINT' for x in c['results'])
extra=[]
for name,p in [('BACKGROUND_ROOT_RECEIPT.json',rpath),('BACKGROUND_CONTROL_RECEIPT.json',cpath)]:
 out=HERE/'sources'/name;b=p.read_bytes()
 with out.open('xb') as f:f.write(b)
 assert out.read_bytes()==b
 extra.append({'source':str(p),'snapshot':'sources/'+name,'bytes':len(b),'sha256':sha(p)})
new('BACKGROUND_CONTROL_REFERENCE.json',{'source_files':extra,'executed_by':'ROOT in separate authorized unit, not this documentary unit','status':r['status'],'solver_units':r['logical_solver_units'],'max_relative_difference':r['max_relative_difference'],'wall_controller_s':r['wall_controller_s'],'max_RSS_KiB':r['max_RSS_KiB'],'solver_seconds_total':r['solver_seconds_total'],'full_prior_qualified':False,'statistical_tail_calibrated':False,'scientific_ratification':False,'observed_inputs':False,'engine_and_protocol_pins_rechecked':True,'raw_prediction_values_not_read_in_this_unit':True})
add=f'''## 11. Atualização de prontidão — lote teórico da ROOT, sem ampliar escopo

[REAL — recibos consultados, não rerun] Depois da preparação deste contrato, a coordenação executou sua unidade autorizada com o motor corrigido. Dez unidades / cinco pares baseline-referência passaram; maior diferença relativa {r['max_relative_difference']:.12g} (zdrag/corner_LLL), abaixo do limiar1e−5. Controlador {r['wall_controller_s']:.9f}s; solvers somados {r['solver_seconds_total']:.9f}s; RSSmáximo {r['max_RSS_KiB']}KiB. O custo dominante desta pequena rodada foi processo/bootstrap. Nenhuma tabela/grade ampliada, ajuste ou dado observado foi aberto por esse controle.

Esta unidade leu somente os dois recibos e conferiu seus hashes e os pins do motor/protocolo; não releu as previsões brutas nem repetiu pontos. `BACKGROUND_CONTROL_REFERENCE.json` e dois snapshots adicionais registram a fonte. O resultado qualifica apenas os5pontos, não o prior contínuo, a compatibilidade de compressõesPlanck, a integral bayesiana ou a cauda de5σ. Os campos observados/calibrados do contrato permanecem null. Motor e protocolo consumidos não foram alterados após a execução da ROOT.
'''
mem.append(HERE/'CONTRATO_DE_VEREDITO_F9.md',add,'F9_VERDICT_ROOT_THEORY_CONTROL_READONLY_20261006')
body=f'''## 06/10/2026 — F9: função de veredito definida como candidato, sem composto

[INPUT] Unidade `{ID}`. Entrega documental em `{HERE}`;14snapshotsoriginais e2recibosteóricosadicionais. CandidatoF9 solicitado conferido por hash, sem ratificar V1 ou abrir dados. Não houve fit, centroscompostos,y/S/g/H0,lnB,simulação,CAMB,rede/Work/provedor nesta unidade.

[DERIVED — contrato] Cinco testes primários na rotaR-A: G1 de adequação absoluta, Q1 da leiβfixa contraβlivre, T21/T41/T51 dirigidos contraΛCDM,Cefeidas diferenciais e rdBAOlivre. Perfis de amostragem separados da integral nuisanceplana comum. H3 contémH1; não se rejeita a classeβlivre emfavor de seu submodelo. Priors/mapas eH5padrãoCMB preservados.

[PROPOSTA]600etiquetas de sensibilidade(300estelares×2SBF), cobertura restrita e não distribuição medida. Robustez p=max_s p_s; cinco perguntas porBonferroni min(1,5p). Cada p_s exige nulo composto/rotina inteira calibrados; gradefinita não prova supremo. α5=erfc(5/√2)/2 eZequivalente apenas convenção de cauda. Não Wilks presumido, não sqrtDeltaχ²automático, não lnB→sigma, não independência de rotas compartilhadas. lnBrelativos reportados nos5modelos/dezpares, com limites e erros separados.

[CORREÇÃO DE DECISÃO]Underpowered deixa de ser saída antecipada. Resíduos e rejeições válidos vêm antes da classificação de poder; cobertura sistemática limitada sempre aparece. Sem calibração, CALIBRATION_UNAVAILABLE, não NOT_FALSIFIED automático. AlternativaA(calibraçãofrequentista+Bayesseparado)recomendada para meta5σ;B(Bayes+preditivopróprio)sem prometer sigma. Retrodição semajuste permanece evidência; proveniência/seleção herdadas da auditoria comseuslimites.

[REAL documental]29checagens deestrutura/pins aprovadas; não calibração científica. Preflight262 reutilizado com suas duas covariânciascondicionais,sem5MM,não poderF9. ROOT executou depois os5paresteóricos background com10unidades; recibos/pins lidos: máximoerrorelativo{r['max_relative_difference']:.12g},controlador{r['wall_controller_s']:.9f}s. Só5pontos qualificados; não priorcontínuo, compatibilidadePlanck nemcauda. Motor/protocolo intocados, nenhuma repetição.

[ENTREGA] `CONTRATO_DE_VEREDITO_F9.md`, `F9_VERDICT_CONTRACT_CANDIDATE.json`, `SOURCES.json`, `VALIDACAO_DOCUMENTAL.json`, `BACKGROUND_CONTROL_REFERENCE.json`, `MANIFESTO_ENTREGA.json`. ContratoSHA256 {sha(HERE/'F9_VERDICT_CONTRACT_CANDIDATE.json')}. Proposta para revisão/decisãoROOT,nenhum gate/confirmacao fisica/nova ciencia. Próximo passo é revisar o contrato e escolher critérios/domínios; não se cria automaticamente uma execução científica.
'''
textnew('MEMORIA_DA_UNIDADE.md','# Memória da unidade — append-only\n\n'+body)
marker='F9_VERDICT_CONTRACT_'+ID
for p in [CENTRAL/'memory'/n for n in ('TGL_ATLAS.md','TGL_INDICE_VIVO.md','TGL_CORE_MEMORY.md')]+[CENTRAL/'Chatgpt/TGL_BANCADA_OFICIAL'/n for n in ('MEMORIA_CENTRAL.md','REGISTRO_DAS_CONVERSAS.md')]:mem.append(p,body,marker)
contract=json.loads((HERE/'F9_VERDICT_CONTRACT_CANDIDATE.json').read_text());assert not contract['opening_authorized'] and all(v is None for v in contract['outputs_now'].values())
for x in json.loads((HERE/'SOURCES.json').read_text())['files']:assert sha(HERE/x['snapshot'])==x['sha256']
files=[{'path':p.relative_to(HERE).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(HERE.rglob('*')) if p.is_file() and '.bak_' not in p.name and '.tmp_' not in p.name and p.name not in ('MANIFESTO_ENTREGA.json','FINAL_CHECK.json','RECIBO_MAPA.json')]
new('MANIFESTO_ENTREGA.json',{'request_id':ID,'created_utc':datetime.now(timezone.utc).isoformat(),'status':'DOCUMENTARY_CANDIDATE_COMPLETE_NOT_RATIFIED','science_runs_in_unit':0,'observed_compound_opened':False,'calibration_executed':False,'historical_note_validation':'VALIDACAO_DOCUMENTAL.json checked note before ROOT-theory addendum; current full-note pin below','files':files})
for x in files:assert sha(HERE/x['path'])==x['sha256']
new('FINAL_CHECK.json',{'status':'PASS_DOCUMENTARY_NO_SCIENCE','manifest_sha256':sha(HERE/'MANIFESTO_ENTREGA.json'),'files_checked':len(files),'source_snapshots':len(list((HERE/'sources').iterdir())),'contract_sha256':sha(HERE/'F9_VERDICT_CONTRACT_CANDIDATE.json'),'note_sha256':sha(HERE/'CONTRATO_DE_VEREDITO_F9.md'),'opening_authorized':False,'all_observed_outputs_null':True,'no_background_rerun':True})
print(json.dumps({'files':len(files),'manifest_sha256':sha(HERE/'MANIFESTO_ENTREGA.json'),'contract_sha256':sha(HERE/'F9_VERDICT_CONTRACT_CANDIDATE.json'),'note_sha256':sha(HERE/'CONTRATO_DE_VEREDITO_F9.md')}))