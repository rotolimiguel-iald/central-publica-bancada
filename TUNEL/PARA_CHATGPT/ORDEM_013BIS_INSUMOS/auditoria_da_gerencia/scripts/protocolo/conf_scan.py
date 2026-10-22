import os,re,collections
roots=[r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN", r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT"]
skip_parts={'vendor','public','casa','site-packages','numba','qnm','pyring_oracle','delivery_fresh_20260922_025830_447404','delivery_v2_fresh_20260922_032436_194092'}
exts={'.py','.json','.md','.txt','.log','.sh','.csv','.out','.err','.toml','.cfg','.ini','.yaml','.yml'}
pats={
 'nome-confidencial-1':re.compile(rb'nome-confidencial-1',re.I),
 'nome-confidencial-2':re.compile(rb'nome-confidencial-2',re.I),
 'dotenv':re.compile(rb'(?<![A-Za-z0-9_])\.env(?![A-Za-z0-9_])'),
 'token':re.compile(rb'\btoken',re.I),
 'RESERVADO':re.compile(rb'RESERVAD',re.I),
 'Escritorio':re.compile(rb'Escritorio|Escrit\xc3\xb3rio',re.I),
 'E_drive':re.compile(rb'(?<![A-Za-z])E:\\|/mnt/e/',re.I),
 'CONFIRMED':re.compile(rb'CONFIRMED'),
 'PROVED':re.compile(rb'\bPROVED\b'),
 'apikey':re.compile(rb'(api[_-]?key|secret|password|senha)',re.I),
}
hits=collections.defaultdict(list); nfiles=0; skipped=0
for r in roots:
    for dp,ds,fs in os.walk(r):
        ds[:]=[d for d in ds if d not in skip_parts and not d.startswith('.venv')]
        for f in fs:
            p=os.path.join(dp,f)
            if os.path.splitext(f)[1].lower() not in exts and '.bak' not in f: continue
            try:
                if os.path.getsize(p)>60_000_000: skipped+=1; continue
                data=open(p,'rb').read()
            except Exception as e:
                skipped+=1; continue
            nfiles+=1
            for k,pt in pats.items():
                for m in pt.finditer(data):
                    s=max(0,m.start()-90); e=min(len(data),m.end()+90)
                    hits[k].append((os.path.relpath(p,r), data[s:e].decode('utf-8','replace').replace('\n',' ')))
print("files scanned",nfiles,"skipped",skipped)
for k,v in hits.items():
    files=collections.Counter(x[0] for x in v)
    print(f"== {k}: {len(v)} hits in {len(files)} files")
    for fn,c in files.most_common(12): print("   ",c,fn)
import pickle; pickle.dump(dict(hits),open(os.path.join(os.path.dirname(__file__),'conf_hits.pkl'),'wb'))
