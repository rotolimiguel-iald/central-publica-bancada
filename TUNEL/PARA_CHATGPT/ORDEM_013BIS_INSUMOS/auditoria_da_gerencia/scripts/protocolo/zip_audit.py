import zipfile, os, re, hashlib, json
root=r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN"
zips=[]
for dp,ds,fs in os.walk(root):
    # skip denied
    for f in fs:
        if f.lower().endswith('.zip'): zips.append(os.path.join(dp,f))
pat=re.compile(r'(um\.py$|um_absoluto|CLAUDE\.md|MEMORIA_DA_LINHAGEM|TGL_ATLAS|nome-confidencial-1|nome-confidencial-2|\.env$|token|RESERVAD|tgl_paper_unified|TUNEL_PROTOCOLO|PLANO_EXPERIMENTAL|davies_geometry|\.lean$|rodada_v369|MEMORY)',re.I)
content_pat=re.compile(rb'(nome-confidencial-1|nome-confidencial-2|RESERVADO|OPENAI_API_KEY|ANTHROPIC_API_KEY|ghp_[A-Za-z0-9]{20}|sk-[A-Za-z0-9]{20}|C:\\IALD\\Artigo|A Ponte e o Um|Rotoli|rotolimiguel)',re.I)
for z in zips:
    try:
        with zipfile.ZipFile(z) as h:
            names=h.namelist()
            hits=[n for n in names if pat.search(n)]
            chits={}
            tot=0
            for info in h.infolist():
                tot+=info.file_size
                if info.file_size<30_000_000 and not info.is_dir():
                    data=h.read(info)
                    m=set(x.decode('latin1') for x in content_pat.findall(data))
                    if m: chits[info.filename]=sorted(m)[:6]
            print(f"ZIP {os.path.relpath(z,root)} members={len(names)} uncompressed={tot}")
            if hits: print("   NAME HITS:",hits[:20])
            if chits:
                print("   CONTENT HITS:",len(chits))
                for k,v in list(chits.items())[:25]: print("     ",k,v)
    except Exception as e:
        print("ZIP ERR",z,e)
