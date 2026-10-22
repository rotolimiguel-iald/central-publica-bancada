"""Custody and register reviewed R66 components, preserving open mission criteria."""
import datetime as dt,json,subprocess,sys
import support_r66 as s

def once(label,cmd):
 s.new(label+'_INTENT.json',{'command':cmd,'utc':dt.datetime.now(dt.timezone.utc).isoformat()})
 cp=subprocess.run(cmd,capture_output=True,encoding='utf-8')
 p=s.new(label+'_RESULT.json',{'exit_code':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr})
 if cp.returncode:raise RuntimeError(str(p))
 print(cp.stdout[:600]);return p

def main():
 s.preflight('R4','DELIVERY_R4_R66');s.preflight('R5','DELIVERY_R5_R66')
 review=json.loads((s.ROOT/'FINAL_REVIEW_R66.json').read_text(encoding='utf-8'))
 assert review['status'].startswith('PASS') and review['reviewer']!=s.ACTOR['id']
 for row in review['evidence']:assert s.pin(row['path'])['sha256']==row['sha256']
 for row in json.loads((s.ROOT/'CANONICAL_PINS_R66.json').read_text())['checks']:assert s.pin(row['expected']['path'])==row['expected']
 names=['RELATORIO_R66.txt','BOSONIC_CONTINUUM_R66.txt','RESERVOIR_ENERGY_AND_SECTORS_R66.txt','JOINT_RESERVOIR_CONTINUUM_LIMIT_R66.txt',
 'construction/DELIVERY_CONSTRUCTION_R66.json','construction/CONSTRUCTION_R66.md','construction/CONVENTIONS_R66.txt',
 'construction/RESULT_COLLISION_R66.json','construction/COMMAND_COLLISION_R66.json','sources/DELIVERY_R66.json','sources/REUSE_R66.json','sources/KNOWN_SEMIGROUPS_R66.json',
 'PLAN_BOSONIC_R66.json','run_bosonic_r66.py','RESULT_BOSONIC_R66.json','FREEZE_BOSONIC_R66.json','BOSONIC_COMMAND_RESULT_R66.json',
 'CANONICAL_PINS_R66.json','FINAL_REVIEW_R66.json','MEMORY_REVIEW_R66.json','MEMORY_APPLIED_R66.json','BOARD_R66.json','NOS_VIVO_R66.json','MAP_R66.json','HANDOFF_R66.json','finish_r66.py','memory_r66.py']
 delivery=s.new('DELIVERY_INTEGRATED_R66.json',{'status':'REVIEWED_RESERVOIR_DRIVE_BOSONIC_COMPONENT','unit':'F1.FECHO_20261015','claim':956,'author':s.ACTOR['id'],
 'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'reference':s.pin(s.REF),'evidence':[s.pin(s.ROOT/n) for n in names],
 'campaigns':[{'kind':'finite_repeated_interactions','checks':115,'passes':115},{'kind':'bosonic_excitation_cuts','checks':68,'passes':68}],
 'mathematics':'Explicit engineered reservoir and coherent OH pump, conservative unbounded two-mode bosonic generator and joint reduced-channel limit, plus dynamical Fock embedding. Analytical proof reviewed, not Lean compiled.',
 'new_lean_builds':0,'R4_R5_integrally_satisfied':False,'canonical_changed':False,'gate_changed':False,'physical_beta_measured':False})
 entry=s.new('MAP_ENTRY_R66.json',{'tipo':'RESULTADO','rota_id':'formal.f1_rede.concrete_bosonic_kinematics','dominio':'FORMAL',
 'titulo':'R66: reservatorio, bombeamento e gerador bosonico completo ligados',
 'metodo':'Reuso R7/R57/R62-R65/Fock; prova analitica por colisoes, cortes compativeis e perturbacao limitada; duas campanhas preregistradas e revisao independente.',
 'resultado':'Colisoes 115/115 e cortes bosonicos68/68 EXIT0. Entrada coerenteOH produz Omega sigma_x; banho comum preservaJ=A+B. Semigrupo bosonico conservativo e limite reduzido conjunto construidos; inclusao Fock agora entrelaca dinamica.',
 'veredito':'PASS_COMPONENT_WITH_SCOPE','estatuto':'DERIVED','status':'EM_CURSO','olhou_dados':False,
 'defeito':'Sem novo termoLean, calibracao fisica, localizacao causal dos modos/acoplamentos, identificacao de relogio global ou limite de saidas ilimitadas. R4/R5 nao integralmente satisfeitos.',
 'nao_refazer':'Reusar construcao R66 e R64; nao voltar a ausencia de Fock/Takesaki/Maxwell. Nao identificar hardcore0/1 com aniquilador bosonico ou banho temporal com rede espacial.',
 'proximo_passo':'Localizar fi/fo e acoplamentos na rede K(O)/algebras locais, confrontar causalidade e transporte do relogio usando representacoes existentes; formalizar demonstracoes novas quando integradas.',
 'artefatos':[str(delivery),str(s.ROOT/'RELATORIO_R66.txt')],'onde':str(s.ROOT)})
 mr=once('MAP_REGISTER_R66',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(entry),'--quem',s.ACTOR['id']])
 br=once('BOARD_REGISTER_R66',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar','F1.FECHO_20261015','--quem',s.ACTOR['id'],'--status','EM_CURSO','--evidencia',str(delivery),'--nota','R66: reservatorio comum, bombaOH e gerador bosonico completos em escopo de dois modos; prova analitica revisada e183checks sinteticos emduascampanhas. Avanco dinamicoFock; sem aceiteintegralR4/R5 ou novoLean.'])
 reg=s.new('REGISTRATION_R66.json',{'delivery':s.pin(delivery),'map':s.pin(mr),'board':s.pin(br)})
 # Release the temporary leases explicitly; preserve all criteria and prior evidence.
 for task in ['R4','R5']:
  m=s.project('RELEASE_'+task+'_PROJECT_R66')
  s.call('mission_cli.py',{'operation':'release','reference':str(s.REF),'actor':s.ACTOR,'expected_revision':m['receipt']['revision'],
   'projection_sha256':m['projection_sha256'],'event_id':'r66-release-'+task.lower(),'task_id':task,
   'reason':'Componente R66 construido e revisado, custodiado. Liberacao da posse temporaria ao concluir etapa; criterio integral permanece aberto, sem apagar resultados nem repetir execucoes.',
   'sources':[s.pin(delivery)]},'RELEASE_'+task+'_R66')
 state=s.call('session_memory.py',{'operation':'get','reference':str(s.REF)},'FINISH_GET_R66')
 handles=state['p']['handles']
 for h in handles:
  if h['id'] in ('r66-sources','r66-construction','r66-review'):h.update(status='completed',result=s.pin(delivery))
 s.call('session_memory.py',{'operation':'transition','reference':str(s.REF),'actor':s.ACTOR,'expected_revision':state['revision'],'event_id':'r66-reservoir-bosonic-bridge-reviewed',
 'changes':{'records':[{'id':'r66-reservoir-drive-bosonic-dynamics','kind':'fact','statute':'DERIVED','sources':[{'kind':'artifact','ref':str(p),'sha256':s.pin(p)['sha256']} for p in (delivery,reg)],
 'text':'R66: banho engenheirado comum paraJ=A+B e entrada coerenteOH constroem geradorcompleto. Cortes totalN compativeis sempump, extensaoCPTPconservativaT1, bomba limitada porDyson/Trotter; cota conjunta colisao+corte liga reservatorio ao geradorbosonico ilimitado2modosOH. Inclusao de ocupacoes noFockexistente entrelaca dinamica; covariancia dafamilia, nao invarianciadoaparelho. Revisaoindependente e115/115+68/68checks, duasexecucoesunicas. Sem novoLean; R4calibracao eR5localizacao/causalidade/relogio permanecemabertos. Cincopinosv393 e gateintactos. LeasesR4/R5liberados explicitamente; retomada exigeclaim/check, nao invalidacao porvencimento.'}],
 'flow':{'phase':'r66_reservoir_drive_bosonic_bridge_reviewed','next_action':'Reivindicar R5 e construir ligacao espacial: fi/fo e acoplamentos em K(O)/algebras locais, causalidade e transporte do relogio da representacao existente. Reusar R66 para gerador/bomba/reservatorio e R64 para instrumento; nao confundir Focktemporal e espacial. R4 calibra independente.','handles':handles}}},'FINISH_TRANSITION_R66')
 print(delivery)
if __name__=='__main__':main()
