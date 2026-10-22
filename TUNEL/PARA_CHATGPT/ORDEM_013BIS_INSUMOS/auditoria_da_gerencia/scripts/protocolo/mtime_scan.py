import os,time,sys
cut=time.mktime(time.strptime("2026-09-21 19:40:00","%Y-%m-%d %H:%M:%S"))
roots=[r"C:\IALD\Artigo", r"C:\IALD\Central de Patentes", r"C:\IALD\Site", r"C:\IALD\CLAUDE.md", r"C:\IALD\projetos_pyhton\IALD", r"<memória da gerência, fora do túnel>", r"<raiz da casa fora do túnel>"]
prune={'.git','.lake','node_modules','__pycache__','.venv','venv'}
out=[]
for r in roots:
    if os.path.isfile(r):
        if os.stat(r).st_mtime>cut: out.append(r)
        continue
    for dp,ds,fs in os.walk(r):
        if os.path.normcase(dp).startswith(os.path.normcase(r"C:\IALD\Central de Patentes\Chatgpt")): ds[:]=[]; continue
        ds[:]=[d for d in ds if d not in prune]
        for f in fs:
            p=os.path.join(dp,f)
            try:
                if os.stat(p).st_mtime>cut: out.append(p)
            except: pass
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'mtime_after_order.txt'),'w',encoding='utf-8') as fh:
    for p in out: fh.write(time.strftime("%m-%d %H:%M:%S",time.localtime(os.stat(p).st_mtime))+"\t"+p+"\n")
print(len(out))
