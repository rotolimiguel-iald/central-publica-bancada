from pathlib import Path
import hashlib,importlib.util,json,subprocess,sys
from datetime import datetime,timezone
B=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015')
REV=B/'mission_review_20261016';RES=B/'mission_resume_20261016'
REF=Path(r'C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json')
ACTOR={'id':'codex-mission-memory-review','kind':'agent'}
REQ=REV/'R52_R8_ACCEPT_REQUEST_R1.json';REC=REV/'R52_R8_ACCEPT_RECEIPT_R1.json'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def pin(p):
    d=p.read_bytes();return {'path':str(p),'sha256':hashlib.sha256(d).hexdigest(),'bytes':len(d)}
def save(p,o):
    assert not p.exists(),str(p)
    d=(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode('utf-8');t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(d)
    assert t.stat().st_size==len(d);t.replace(p);return pin(p)
def project(label):
    s=importlib.util.spec_from_file_location('r52_r8_accept_project',RES/'live_mission_r39.py')
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);assert Path(m.REFERENCE)==REF
    return m.call('mission_cli.py',{'operation':'project','reference':str(REF),'actor':ACTOR,'max_chars':100000},label)
if sys.argv[1]=='prepare':
    reviewpath=REV/'R52_R8_FULL_REVIEW_R1.json';review=read(reviewpath)
    assert review['reviewer']==ACTOR and review['requirement_satisfied'] and review['eligible_for_acceptance']
    r,p=project('R52_R8_ACCEPT_FRESH_PROJECT');q=r['projection'];task=next(t for t in q['active'] if t['id']=='R8')
    assert task['status']=='review_pending' and task['submitted_by']!=ACTOR['id']
    assert task['criterion']==review['criterion']
    for e in task['evidence']:assert pin(Path(e['path']))['sha256']==e['sha256']
    assert pin(Path(review['delivery']['path']))==review['delivery']
    ev=pin(reviewpath)
    request={'operation':'accept','reference':str(REF),'actor':ACTOR,'task_id':'R8',
      'expected_revision':q['revision'],'projection_sha256':r['projection_sha256'],
      'event_id':'r52-r8-independent-accept-codex-mission-memory-review',
      'review_evidence':[{'path':ev['path'],'sha256':ev['sha256']}],
      'note':'Revisão independente do critério original R8: MaxwellCertificate completo na rede física, mesmo estado/forma Wick/carga/fonte H3; 26 prints trio e pinos conferidos. H3 nulo fixo/linearizado, N e G explícitos. R4/R5 e demais pendências preservados; sem ato de quadro/gate ou confirmação empírica.'}
    rp=save(REQ,request)
    prep=save(REV/'R52_R8_ACCEPT_PREPARATION_R1.json',{'reviewer':ACTOR,'created_utc':datetime.now(timezone.utc).isoformat(),
      'fresh_project':pin(p),'revision':q['revision'],'state_sha256':q['state_sha256'],'review':ev,'request':rp,
      'other_requirements':{t['id']:t for t in q['active']+q['settled'] if t['id']!='R8'}})
    print(json.dumps({'ok':True,'revision':q['revision'],'request':rp,'preparation':prep},ensure_ascii=False))
elif sys.argv[1]=='accept':
    assert not REC.exists(), 'Existing receipt must be reconciled, not repeated'
    request=read(REQ);assert request['actor']==ACTOR and request['reference']==str(REF) and request['task_id']=='R8'
    for e in request['review_evidence']:assert pin(Path(e['path']))['sha256']==e['sha256']
    cp=subprocess.run([r'C:\Python314\python.exe','-B','-X','utf8',r'C:\IALD\MEMORIA_IALD\mission_cli.py'],
      input=json.dumps(request,ensure_ascii=False).encode('utf-8'),capture_output=True)
    try:o=json.loads(cp.stdout.decode('utf-8'))
    except Exception:o={'ok':False,'outcome':'UNCERTAIN_INVALID_CLI_OUTPUT','exit_code':cp.returncode,'stdout':cp.stdout.decode('utf-8',errors='replace'),'stderr':cp.stderr.decode('utf-8',errors='replace')}
    rp=save(REC,o);print(json.dumps({'receipt':rp,'exit_code':cp.returncode,'response':o},ensure_ascii=False))
    assert cp.returncode==0 and o['ok'], 'Accept refused or uncertain; inspect saved receipt'
elif sys.argv[1]=='verify':
    o=read(REC);assert o['ok']
    r,p=project('R52_R8_AFTER_ACCEPT_PROJECT');q=r['projection'];task=next(t for t in q['settled'] if t['id']=='R8')
    assert task['status']=='satisfied' and task['reviewed_by']==ACTOR['id']
    prior=read(REV/'R52_R8_ACCEPT_PREPARATION_R1.json')['other_requirements'];current={t['id']:t for t in q['active']+q['settled'] if t['id']!='R8'}
    assert prior==current,'Concurrent changes to other requirements: inspect before claiming unchanged'
    vp=save(REV/'R52_R8_ACCEPT_VERIFICATION_R1.json',{'ok':True,'reviewer':ACTOR,'revision':q['revision'],
      'receipt':pin(REC),'after_project':pin(p),'R8':task,'other_requirements_unchanged':True,'tetelestai':q.get('tetelestai')})
    print(json.dumps({'ok':True,'revision':q['revision'],'receipt':pin(REC),'verification':vp,'after_project':str(p),'tetelestai':q.get('tetelestai')},ensure_ascii=False))
else:raise ValueError('Unknown action')
