"""Record scope and falsifiers before the R60 synthetic algebra checks."""
import support_r60 as s

def main():
    s.preflight('R5','START_R60')
    source=s.new('OPERADOR_R60.txt','Prossiga')
    prereg=s.new('PREREG_R60.json',{
      'status':'INPUT_CONDITIONAL_MEASUREMENT_MODELS', 'unit':'F1.FECHO_20261015','claim':939,
      'operator_source':s.pin(source),'parent_delivery':s.pin(s.ROOT.parent/'pair_covariance_r59/DELIVERY_R59.json'),
      'objective':'Locate and test relational estimators with explicit nuisance parameters. No presumed equality of measured channel b or squeeze rho with betaTGL.',
      'models':[
        {'id':'CROSS_RATIO','assumptions':'Two inputs, common symmetric lossless power transfer [[1-b,b],[b,1-b]], positive unknown input intensities IA,IB, fixed positive port gains g1,g2, backgrounds removed, 0<b<1.',
         'equations':'A1=g1*IA*(1-b); A2=g2*IA*b; B1=g1*IB*b; B2=g2*IB*(1-b). Q=A2*B1/(A1*B2).',
         'claim':'sqrt(Q)=b/(1-b), b=sqrt(Q)/(1+sqrt(Q)); no target beta input.',
         'falsifiers':'Symbolic residual nonzero; injected channel b not recovered. Single configuration with unknown gains must be nonidentifiable; configuration-dependent gains must break recovery.'},
        {'id':'PAIR_LOSS','assumptions':'R59 pure zero-mean two-mode squeezed input; independent vacuum loss etaA,etaB in (0,1]; calibrated photon units; no extra additive noise, mixing or phase jitter; n>0.',
         'equations':'x=etaA*n; y=etaB*n; z=|m_out|^2=etaA*etaB*n*(n+1); d=z-x*y.',
         'claim':'n=x*y/d; etaA=d/y; etaB=d/x. Local identifiability with determinant nonzero. This does not yield beta.',
         'falsifiers':'Exact reconstruction fails; boundary d<=0 must refuse; arbitrary mixed input must permit indistinguishable states, including ones passing ideal-domain checks.'}
      ],
      'verification':'SymPy exact identities and rational synthetic controls; numerical checks only if named and tolerance fixed. No observed data, no 5-sigma or empirical power claim.',
      'scope':'R5 readout/covariance component only. R4 recovery, OH generator and clock unchanged; no accepted mission requirement.',
      'no_changes':['um.py','kernel','Bancada','observed data','gate'], 'provider_calls':0})
    state=s.call('session_memory.py',{'operation':'get','reference':str(s.REF)},'START_GET')
    hs=state['p']['handles']
    hs.append({'id':'r60-source-survey','kind':'agent','task_id':'R60_sources','agent':'/root/maxwell_covariance_review','status':'running','no_repeat':True,'start_receipt':s.pin(prereg)})
    s.call('session_memory.py',{'operation':'transition','reference':str(s.REF),'actor':s.ACTOR,
      'expected_revision':state['revision'],'event_id':'r60-relational-readout-start-20261017',
      'changes':{'records':[{'id':'r60-relational-readout-scope','kind':'decision','statute':'INPUT',
        'sources':[{'kind':'artifact','ref':str(p),'sha256':s.pin(p)['sha256']} for p in [source,prereg]],
        'text':'Continuidade R5: levantamento e estimadores relacionais condicionais, sem igualdade presumida entre rho/refletividade e beta. R4 permanece pendente; nenhuma recuperação ou dinâmicaOH.'}],
        'flow':{'phase':'r60_relational_readout','next_action':'Conferir fontes e identifiabilidade dos modelos de leitura; revisão independente antes de memória.','handles':hs}}},'START_TRANSITION')
    print(prereg)

if __name__=='__main__':main()
