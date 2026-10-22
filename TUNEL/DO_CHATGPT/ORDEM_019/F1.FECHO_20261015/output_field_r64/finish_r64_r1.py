"""Custody and registration of reviewed R64; no full R4/R5 acceptance."""
import datetime as dt
import json
import subprocess
import sys
import support_r64 as s

def once(label,command):
    s.new(label+'_INTENT.json',{'command':command,'utc':dt.datetime.now(dt.timezone.utc).isoformat()})
    cp=subprocess.run(command,capture_output=True,encoding='utf8')
    p=s.new(label+'_RESULT.json',{'exit_code':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr})
    if cp.returncode:raise RuntimeError(str(p))
    print(cp.stdout[:1000]);return p

def main():
    s.preflight('R4','DELIVERY_R64')
    review=json.loads((s.ROOT/'FINAL_REVIEW_R64.json').read_text(encoding='utf8'))
    assert review['status'].startswith('PASS') and review['reviewer']!=s.ACTOR['id']
    for row in review['evidence']:assert s.pin(row['path'])['sha256']==row['sha256']
    result=json.loads((s.ROOT/'output/RESULT_OUTPUT_R64.json').read_text(encoding='utf8'))
    assert result['status']=='PASS_CONDITIONAL_FILTERED_OUTPUT' and all(c['passed'] for c in result['checks'])
    n=len(result['checks'])
    names=['RELATORIO_R64.txt','IDENTIFIABILITY_AND_FRAME_R64.txt','output/DELIVERY_OUTPUT_R64.json',
           'output/CONTRATO_OUTPUT_R64.md','output/ADENDO_DILATACAO_INICIAL_R64.md','output/PLAN_OUTPUT_R64.json',
           'output/FREEZE_R64.json','output/START_R64.json','output/RESULT_OUTPUT_R64.json','output/run_filtered_output_r64.py',
           'sources/DELIVERY_R1.json','sources/OUTPUT_FIELD_SOURCE_REPORT_R1.json','sources/FOCAL_SOURCE_PINS_R1.json',
           'CANONICAL_PINS_R64.json','PREEXEC_REVIEW_R64.json','FINAL_REVIEW_R64.json','MEMORY_REVIEW_R64.json',
           'MEMORY_APPLIED_R64.json','BOARD_R64.json','literature/CUSTODY_R64.json','finish_r64.py','finish_r64_r1.py','memory_r64.py']
    for row in json.loads((s.ROOT/'CANONICAL_PINS_R64.json').read_text())['checks']:
        assert s.pin(row['expected']['path'])==row['expected']
    delivery=s.new('DELIVERY_INTEGRATED_R64.json',{'status':'REVIEWED_CONDITIONAL_TEMPORAL_OUTPUT_COMPONENT',
        'unit':'F1.FECHO_20261015','claim':952,'author':s.ACTOR['id'],'utc':dt.datetime.now(dt.timezone.utc).isoformat(),
        'reference':s.pin(s.REF),'evidence':[s.pin(s.ROOT/x) for x in names],
        'checks':n,'R4_R5_integrally_satisfied':False,'beta_measured':False,'canonical_changed':False,
        'observed_data':False,'gate_changed':False,'provider_calls':0,
        'result':'Filtered homodyne output moments from full GKLS under named Markov vacuum instrument; lambda=beta*gammaLambda degeneracy and common-carrier calibration limitation explicit.'})
    entry=s.new('MAP_ENTRY_R64.json',{'tipo':'RESULTADO','rota_id':'formal.f1_rede.concrete_bosonic_kinematics','dominio':'FORMAL',
        'titulo':'R64: campo temporal filtrado, ruido de vacuo e identificabilidade no instrumento nomeado',
        'metodo':f'Reuso de oito fontes; instrumentoMarkov explicito; uma execucao preregistrada com {n} verificacoes e revisao independente.',
        'resultado':'Momentos do sinal exterior calculados sem fatorarOH; shotnoise delta/2, quatro aquisicoes separadas e decoderCf/Bf. Neste canal a dependencia beta,gammaLambda passa somente por lambda=beta*gammaLambda; nao provada identificabilidade positiva nem separada.',
        'veredito':'PASS_COMPONENT_WITH_SCOPE','estatuto':'DERIVED','status':'EM_CURSO','olhou_dados':False,
        'defeito':'Preparo e calibracao fisica do mesmo dispositivo; compatibilidade dinamica e espacial com rede continuam abertos.',
        'nao_refazer':'Nao repetir controlesR64 ou construir novamente gerador/Fock/Takesaki/Maxwell/decoder. Portas e banhos sao INPUT nomeados.',
        'proximo_passo':'Localizar fontes independentes para preparo, escala temporal e gammaLambda; verificar realizacao/calibracao antes de inferir beta e integrar rede.',
        'artefatos':[str(delivery),str(s.ROOT/'RELATORIO_R64.txt')],'onde':str(s.ROOT)})
    mr=once('MAP_REGISTER_R64',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(entry),'--quem',s.ACTOR['id']])
    br=once('BOARD_REGISTER_R64',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar','F1.FECHO_20261015','--quem',s.ACTOR['id'],'--status','EM_CURSO','--evidencia',str(delivery),'--nota',f'R64: campo filtrado sob instrumentoMarkov nomeado, {n} verificacoes, revisao independente. Calibracao/identificabilidade explicitadas; sem aceite integralR4/R5.'])
    reg=s.new('REGISTRATION_R64.json',{'delivery':s.pin(delivery),'map':s.pin(mr),'board':s.pin(br)})
    state=s.call('session_memory.py',{'operation':'get','reference':str(s.REF)},'FINISH_GET_R64')
    handles=state['p']['handles']
    for h in handles:
        if h['id'] in ('r64-sources','r64-output','r64-review'):h.update(status='completed',result=s.pin(delivery))
    s.call('session_memory.py',{'operation':'transition','reference':str(s.REF),'actor':s.ACTOR,
        'expected_revision':state['revision'],'event_id':'r64-reviewed-temporal-output-custodied',
        'changes':{'records':[{'id':'r64-temporal-output-instrument','kind':'fact','statute':'DERIVED',
        'sources':[{'kind':'artifact','ref':str(p),'sha256':s.pin(p)['sha256']} for p in (delivery,reg)],
        'text':f'R64: instrumentoHP/Markov nomeado liga dinamica conjunta a momentos de campo filtrado; {n} checks numa execucao, controles analiticos e revisao independente. Estado sistema tensor vacuo de5banhos, portas/LO/filtros/eficiencia/preparo INPUT. Cf/Bf sao de saida temporal, nao pares instantaneos. Dependencia somente lambda=beta*gammaLambda impede identificar beta sem informacao independente sobre gammaLambda neste canal. Carrier comum e t0positivo nao calibra INPUTs1.2/1 ao projetoOH/780nm por sinal da diferenca. R4/R5 integrais abertos; R3/R10 dependentes. Sem beta medido, dado observado, nova provaLean ou gate alterado.'}],
        'flow':{'phase':'r64_reviewed_temporal_output_custodied','next_action':'Recuperar fontes independentes para preparo/calibracao do instrumento e gammaLambda; verificar identificabilidade e compatibilidade dinamica/espacial com rede. Reusar R64 e provas aceitas, sem nova campanha repetida.','handles':handles}}},'FINISH_TRANSITION_R64')
    print(delivery)

if __name__=='__main__':main()


