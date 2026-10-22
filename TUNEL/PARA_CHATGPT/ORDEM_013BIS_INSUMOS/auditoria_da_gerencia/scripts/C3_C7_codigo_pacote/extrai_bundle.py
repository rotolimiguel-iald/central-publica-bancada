import zipfile, os, re, sys, hashlib
S = r'C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\ordem013\auditoria\C3_C7_codigo_pacote'
B = r'C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN'
name = sys.argv[1]  # e.g. TGL_RINGDOWN_DELIVERY_v2.zip
dest = sys.argv[2]
zp = os.path.join(B, 'cache', name)
print('zip sha256', hashlib.sha256(open(zp, 'rb').read()).hexdigest())
root = '\\\\?\\' + os.path.join(S, dest)
z = zipfile.ZipFile(zp)
assert z.testzip() is None
n = z.namelist()
print('members', len(n), 'maior caminho interno', max(len(x) for x in n))
for i in z.infolist():
    parts = i.filename.split('/')
    assert not i.filename.startswith('/') and '..' not in parts
    target = os.path.join(root, *[p for p in parts if p])
    if i.is_dir():
        os.makedirs(target, exist_ok=True); continue
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, 'wb') as f:
        f.write(z.read(i))
bad = [x for x in n if re.search(r'(\.env|nome-confidencial-1|nome-confidencial-2|RESERVAD|token|/um\.py$|um_absoluto)', x, re.I)]
print('suspeitos', bad)
print('arquivos na raiz', [x.split('/', 1)[1] for x in n if x.count('/') == 1 and not x.endswith('/')])
print('pastas', sorted(set(x.split('/')[1] for x in n if x.count('/') >= 2)))
