# -*- coding: utf-8 -*-
import os, re, hashlib, json, sys
sys.stdout.reconfigure(encoding='utf-8')
ORD = r'C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\ordem013\bis\ORDEM_013BIS_fechamento_e_ampliacao_dos_eventos_ate_5sigma.md'
BENCH = r'C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN'
PC = r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT'
h16 = lambda b: hashlib.sha256(b).hexdigest()[:16]
lines = open(ORD, encoding='utf-8').read().split('\n')
print('ORDEM bytes', os.path.getsize(ORD), 'sha16', h16(open(ORD,'rb').read()))
# 1) all hex tokens >= 8
tok = {}
for i, l in enumerate(lines, 1):
    for m in re.finditer(r'(?<![0-9a-zA-Z])([0-9a-f]{8,64})(?![0-9a-zA-Z])', l):
        t = m.group(1)
        if re.fullmatch(r'[0-9]+', t): continue
        tok.setdefault(t, []).append(i)
print('\n== TOKENS HEX (>=8) na ordem:')
for t, ls in tok.items(): print(f'  {t}  linhas {ls}')
# 2) tabela §7
print('\n== TABELA §7:')
ok = bad = 0
tab_hashes = {}
for i, l in enumerate(lines, 1):
    if l.startswith('| ') and (chr(96) + 'C:' + chr(92)) in l:
        c = [x.strip() for x in l.strip('|').split('|')]
        path = c[1].strip('`'); nb = int(c[2].replace(',', '')); sh = c[3].strip('`'); lado = c[4]
        tab_hashes[sh] = path
        if not os.path.isfile(path):
            print(f'  L{i} NAO EXISTE: {path}'); bad += 1; continue
        b = open(path, 'rb').read(); s = h16(b)
        st = 'OK' if (s == sh and len(b) == nb) else f'DIVERGE disco bytes={len(b)} sha16={s}'
        if st == 'OK': ok += 1
        else: bad += 1
        print(f'  L{i} {st} | {os.path.basename(path)} | tab bytes={nb} sha16={sh} | lado={lado}')
print(f'  tabela: OK={ok} BAD={bad}')
# 3) FONTES_DA_CASA.json (ORDEM 013) comparacao coluna "igual"
old = json.load(open(os.path.join(PC, 'ORDEM_013_INSUMOS', 'FONTES_DA_CASA.json'), encoding='utf-8'))
print('\n== FONTES_DA_CASA da ORDEM 013 (keys):', list(old.keys()))
for f in old['fontes']:
    b = open(f['caminho'], 'rb').read(); s = h16(b)
    if s != f['sha16'] or len(b) != f['bytes']:
        print(f"  MUDOU desde a 013: {f['caminho']} 013={f['sha16']}/{f['bytes']} hoje={s}/{len(b)}")
print('  (fim; sem linhas MUDOU = todas iguais)')
# 4) hashes soltos
for t in ['d4440c6a28eaad4b', 'd9f5bd5dffc3333d', 'ef951a3fc8fe840e', '4234902dc6f5e03c']:
    print('  citado', t, 'na tabela:', t in tab_hashes)
# 5) procurar 9c5271fba4aaa144 na bancada (cache/literature + manifesto)
print('\n== BUSCA 9c5271fba4aaa144 / ef1b4d69 na bancada')
targets = {'9c5271fba4aaa144': [], 'ef1b4d69': []}
# a) por hash de arquivo em cache/literature e cache
for sub in ['cache\literature', 'cache']:
    d = os.path.join(BENCH, sub)
    if not os.path.isdir(d): print('  sem pasta', d); continue
    for dp, dn, fn in os.walk(d):
        for f in fn:
            p = os.path.join(dp, f)
            try:
                if os.path.getsize(p) > 200*1024*1024: continue
                s = hashlib.sha256(open(p,'rb').read()).hexdigest()
            except Exception as e: continue
            if s.startswith('9c5271fba4aaa144'): targets['9c5271fba4aaa144'].append(('ARQUIVO', p))
            if s.startswith('ef1b4d69'): targets['ef1b4d69'].append(('ARQUIVO', p))
    break
print('  por hash de arquivo:', targets)
# b) por texto em JSON/MD da bancada e DO_CHATGPT
hits = {'9c5271fba4aaa144': [], 'ef1b4d69': []}
for root in [BENCH, os.path.join(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL', 'DO_CHATGPT')]:
    for dp, dn, fn in os.walk(root):
        if '.lake' in dp or 'tex_environment' in dp: continue
        for f in fn:
            if not f.lower().endswith(('.json', '.md', '.txt', '.py', '.csv')): continue
            p = os.path.join(dp, f)
            try:
                if os.path.getsize(p) > 30*1024*1024: continue
                t = open(p, 'rb').read().decode('utf-8', 'replace')
            except Exception: continue
            for k in hits:
                if k in t:
                    for j, ln in enumerate(t.split('\n'), 1):
                        if k in ln: hits[k].append((p, j, ln.strip()[:220])); break
for k, v in hits.items():
    print(f'  texto "{k}": {len(v)} arquivos')
    for p, j, ln in v[:12]: print('    ', p, 'L', j, '|', ln)
