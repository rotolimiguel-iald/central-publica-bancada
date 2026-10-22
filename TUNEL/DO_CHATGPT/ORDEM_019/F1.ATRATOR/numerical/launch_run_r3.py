from pathlib import Path
import hashlib,json,datetime,sys,subprocess,time
root=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.ATRATOR')
out=root/'numerical';script=out/'run_optical_r3.py';pre=root/'PREREGISTRO_R1.json'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):
 with p.open('x',encoding='utf-8',newline='\n') as f: json.dump(x,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')
expected='db52519d336955e9d93c1beee775a721b40633ae5c99a78a35e57f95c00da731'
if sha(pre)!=expected: raise RuntimeError('Frozen prereg hash differs')
command=[sys.executable,'-B','-X','utf8',str(script)]
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
write(out/'RUN_MANIFEST_R3.json',{'unit':'F1.ATRATOR','started_utc':started,'command':command,'cwd':str(out),'script_sha256':sha(script),'preregister_sha256':sha(pre),'preregistered_utc':json.loads(pre.read_text(encoding='utf-8'))['created_utc'],'observed_data':False,'production_execution':False})
t=time.perf_counter();r=subprocess.run(command,cwd=out,capture_output=True,text=True,encoding='utf-8');elapsed=time.perf_counter()-t
finished=datetime.datetime.now(datetime.timezone.utc).isoformat()
log=out/'RUN_R3.log'
with log.open('x',encoding='utf-8',newline='\n') as f:f.write('COMMAND: '+repr(command)+'\nSTART: '+started+'\nEND: '+finished+'\nELAPSED_SECONDS: '+str(elapsed)+'\nEXIT: '+str(r.returncode)+'\nSTDOUT:\n'+r.stdout+'\nSTDERR:\n'+r.stderr)
write(out/'RUN_RECEIPT_R3.json',{'command':command,'started_utc':started,'finished_utc':finished,'seconds':elapsed,'exit_code':r.returncode,'log_sha256':sha(log),'script_sha256':sha(script),'preregister_sha256':sha(pre),'result_sha256':sha(out/'RESULTADOS_NUMERICOS_R3.json') if (out/'RESULTADOS_NUMERICOS_R3.json').exists() else None})
print(r.stdout);print(r.stderr);print('EXIT',r.returncode)
sys.exit(r.returncode)
