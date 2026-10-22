"""Synchronize R62 audit and targeted readout work under existing R4 claim."""
import support_r62 as s

def main():
    s.preflight('R4','PREFLIGHT_START')
    original=s.ROOT/'OPERADOR_R62.txt'
    state=s.call('session_memory.py',{'operation':'get','reference':str(s.REF)},'START_GET')
    hs=state['p']['handles']
    for name,agent in [('audit','mission_memory_review'),('sources','maxwell_covariance_review'),('readout','miguel_r56_review')]:
        hs.append({'id':'r62-'+name,'kind':'agent','agent':'/root/'+agent,'status':'running','no_repeat':True,'source':s.pin(original)})
    s.call('session_memory.py',{'operation':'transition','reference':str(s.REF),'actor':s.ACTOR,
      'expected_revision':state['revision'],'event_id':'r62-audit-reuse-and-targeted-readout-start',
      'changes':{'flow':{'phase':'r62_mission_audit_and_readout_reuse','next_action':'Conferir aceites/pinos, aproveitar gerador conjunto existente e preparar contrato observavel do receptor antes de novo teste.','handles':hs}}},'START_TRANSITION')
    print('R62 anchored, audit/reuse/readout handles recorded.')

if __name__=='__main__': main()
