"""Register reviewed calibration contract; preserve open physical and global requirements."""
import datetime as dt,json,subprocess,sys
import support_r65 as s

def once(label,command):
 s.new(label+'_INTENT.json',{'command':command,'utc':dt.datetime.now(dt.timezone.utc).isoformat()})
 cp=subprocess.run(command,capture_output=True,encoding='utf8')
 p=s.new(label+'_RESULT.json',{'exit_code':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr})
 if cp.returncode:raise RuntimeError(str(p))
 print(cp.stdout[:900]);return p

def main():
 s.preflight('R4','DELIVERY_R65')
 review=json.loads((s.ROOT/'FINAL_REVIEW_R65.json').read_text())
 assert review['status'].startswith('PASS') and review['reviewer']!=s.ACTOR['id']
 for row in review['evidence']:assert s.pin(row['path'])['sha256']==row['sha256']
 for row in json.loads((s.ROOT/'CANONICAL_PINS_R65.json').read_text())['checks']:assert s.pin(row['expected']['path'])==row['expected']
 names=['RELATORIO_R65.txt','IDENTIFIABILITY_COMPLETION_R65.txt','THERMAL_ROUTE_SOURCE_R65.json','THERMAL_ROUTE_SCOPE_R65.txt',
 'BARE_FREQUENCY_COVARIANCE_R65.txt','calibration/DELIVERY_CALIBRATION_R65.json','calibration/CONTRATO_CALIBRACAO_R65.md',
 'calibration/ROTAS_ESCALA_JA_ESCRITAS_R65.md','calibration/SOURCE_PINS_AND_ANCHORS_R65.json','sources/DELIVERY_R1.json',
 'CANONICAL_PINS_R65.json','FINAL_REVIEW_R65.json','MEMORY_REVIEW_R65.json','MEMORY_APPLIED_R65.json','BOARD_R65.json',
 'NOS_VIVO_R65.json','MAP_R65.json','finish_r65.py','memory_r65.py']
 delivery=s.new('DELIVERY_INTEGRATED_R65.json',{'status':'REVIEWED_CALIBRATION_AND_BATH_CONTRACT','unit':'F1.FECHO_20261015',
 'claim':952,'author':s.ACTOR['id'],'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'reference':s.pin(s.REF),
 'evidence':[s.pin(s.ROOT/n) for n in names],'new_numerical_campaigns':0,'new_lean_builds':0,'physical_beta_measured':False,
 'R4_R5_integrally_satisfied':False,'canonical_changed':False,'gate_changed':False,
 'result':'Scale/J normalization and independent-reference identifiability contract; thermal stationarity sufficiency counterexample and bare-frequency covariance probe, both with named scope; coherent preparation limitation. Existing clock/root/bath routes reused.'})
 entry=s.new('MAP_ENTRY_R65.json',{'tipo':'RESULTADO','rota_id':'formal.f1_rede.concrete_bosonic_kinematics','dominio':'FORMAL',
 'titulo':'R65: contrato de calibracao/preparo e sondas da rota termica e de frequencias do banho',
 'metodo':'Levantamento primario focal, derivacoes analiticas e revisao independente; zero campanha numerica ou aquisicao.',
 'resultado':'J e tempo normalizados; beta=r/c exige referencia independente. Estacionario finito isolado nao fixa piso de taxa; D[J] nao e covariante emh0livre foraressonancia. Preparo coerente passivo nao equivale aFock/par. Rotas existentes preservadas.',
 'veredito':'PASS_COMPONENT_WITH_SCOPE','estatuto':'DERIVED','status':'EM_CURSO','olhou_dados':False,
 'defeito':'Calibracao independente e realizacao do banho/drive no mesmoJ abertas; diagnostico livre nao e resultado sobrefullH ou redePoincare.',
 'nao_refazer':'Reusar R64, R7, Fock/Takesaki/Maxwell; gammaLambda=1 nao vira calibracao; nao trocar D[A+B] porD[A]+D[B] silenciosamente.',
 'proximo_passo':'Avancar ponte matematica reservatorio/drive e gerador completo, distinguindo representacaoHP abstrata de realizacao fisica. R5 formal pode avancar sem esperar beta experimental.',
 'artefatos':[str(delivery),str(s.ROOT/'RELATORIO_R65.txt')],'onde':str(s.ROOT)})
 mr=once('MAP_REGISTER_R65',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(entry),'--quem',s.ACTOR['id']])
 br=once('BOARD_REGISTER_R65',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar','F1.FECHO_20261015','--quem',s.ACTOR['id'],'--status','EM_CURSO','--evidencia',str(delivery),'--nota','R65 revisada: contrato de escalas/preparo/calibracao; rota termica e covariancia deh0 com sondasanaliticas. SemsimulacaoouaceiteR4/R5; R5 formal independente de confirmacaoexperimental.'])
 reg=s.new('REGISTRATION_R65.json',{'delivery':s.pin(delivery),'map':s.pin(mr),'board':s.pin(br)})
 state=s.call('session_memory.py',{'operation':'get','reference':str(s.REF)},'FINISH_GET_R65')
 handles=state['p']['handles']
 for h in handles:
  if h['id'] in ('r65-sources','r65-calibration','r65-review'):h.update(status='completed',result=s.pin(delivery))
 s.call('session_memory.py',{'operation':'transition','reference':str(s.REF),'actor':s.ACTOR,'expected_revision':state['revision'],
 'event_id':'r65-reviewed-calibration-contract-custodied','changes':{'records':[{'id':'r65-calibration-and-bath-contract','kind':'fact','statute':'DERIVED',
 'sources':[{'kind':'artifact','ref':str(p),'sha256':s.pin(p)['sha256']} for p in (delivery,reg)],
 'text':'R65 contrato revisado: normalizacaoJ e tempo/portas/filtros/LO; beta=r/c exigeGamma/kappa independente. Fisherlocal com calibracao separada det=Gamma²I_lambdaI_Gamma. Rotas termica/planckiana/lei-raiz/Davies ja existem mas vinculosmesmoJ/normalizacao/saturacao permanecemnomeados. Sondaqubit estacionariofinito permiteepsarbitrario; soessa condicao naoimpoepiso. D[J]foraressonancia naoecovariante no h0LIVRE: [D[J],U]X=-2i sinδtY; naoinferefullH/rede. Coerenteatenuado naoFock/par, squeezedt.5cauda1/16. Zero nova campanha, dado ou beta inferido. R4calibracao aberta; R5 podeavancarformalmente sem medicaobeta; R3/R10dependentes; canonico/gate intactos.'}],
 'flow':{'phase':'r65_reviewed_calibration_contract_custodied','next_action':'Construir ponte matematica do reservatorio/drive ao gerador completo e compatibilidade dinamica/espacial, reaproveitandoFock/rede e separandoHP abstrato, covariancialivre e calibracaofisica. Nao bloquearformalR5 por confirmacaobeta.','handles':handles}}},'FINISH_TRANSITION_R65')
 print(delivery)
if __name__=='__main__':main()

