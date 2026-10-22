"""Resume custody of the existing finite exploration after approved R4 recovery."""
import support_r61 as s

def main():
    s.preflight('R4','START')
    p=s.ROOT.parent
    scope=s.new('SCOPE_R61.json',{'claim':939,'unit':'F1.FECHO_20261015',
      'recovery':s.pin(p/'r4_recovery_authorized_20261017/RECOVERY_RESULT.json'),
      'existing_exploration':s.pin(p/'pair_covariance_r59/oh_correlation/EXPLORATION_R59.json'),
      'existing_script':s.pin(p/'pair_covariance_r59/oh_correlation/explore_pairs_r59.py'),
      'objective':'Custody and independently review the previously executed finite OH pair-generator exploration. No rerun of original execution.',
      'scope':'Two-level optical cutoffs plus two-level auxiliary; not bosonic infinite generator, physical instrument identification, or full R4 satisfaction.',
      'prohibited':['Repeat original scientific run','Providers','Observed data','Canonical program/kernel/Bancada edits','Gate changes']})
    state=s.call('session_memory.py',{'operation':'get','reference':str(s.REF)},'START_GET')
    hs=state['p']['handles'];hs.append({'id':'r61-oh-custody','kind':'agent','task_id':'R61_OH','agent':'/root/miguel_r56_review','status':'running','no_repeat':True,'start_receipt':s.pin(scope)})
    s.call('session_memory.py',{'operation':'transition','reference':str(s.REF),'actor':s.ACTOR,
      'expected_revision':state['revision'],'event_id':'r61-existing-exploration-custody-start-20261017',
      'changes':{'flow':{'phase':'r61_existing_oh_exploration_review','next_action':'Revisar exploração existente de pares no corte finito; distinguir hierarquia dinâmica de covariância R59/R60.','handles':hs}}},'START_TRANSITION')
    print(scope)

if __name__=='__main__':main()
