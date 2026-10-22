import os, glob, hashlib, re
R = r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN"
D = r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT"


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


targets = {
    'C3_BILBY_CONSUMER.json': 'bc49da2a45a5652f',
    'tgl_ringdown_prediction.py': '458940f77a494305',
    'C3_PREDICTION_COMPATIBILITY.json': '83bb5ed07bf3783b',
    'C7_DELIVERY_OVERVIEW.md': '218a3de59715c9b1',
}
for name, want in targets.items():
    base = os.path.join(R, name)
    found = []
    for p in glob.glob(base + '*'):
        s = sha(p)[:16]
        if s == want:
            found.append(os.path.basename(p))
    print(name, 'cited', want, '-> preserved in:', found or 'NOT FOUND (version cited in the note no longer on disk)')
mans = {}
for p in glob.glob(os.path.join(R, 'cache', 'MANIFESTO_DOWNLOADS.json*')):
    mans[sha(p)[:16]] = os.path.basename(p)
for want in ['6aef8f1dd8d811a0', '727ff51684585428', '4f21bedd862f7a1a', 'f3e8103571721e67', 'de12d0611043dfd2', '4320a6bd4ebfeb81', '580128a3ba513ebd', '6dd8ed1504bc0d18']:
    print('MANIFESTO cited', want, '->', mans.get(want, 'NOT FOUND'))
# PARCIAL note
t = open(os.path.join(D, 'ENTREGA_013_PARCIAL_220_E_FORECAST_20260921.md'), encoding='utf-8').read()
for m in re.finditer(r'`([^`]+)` . SHA256 `([0-9a-f]{64})`', t):
    p = m.group(1)
    cands = [p] + glob.glob(p + '.bak*')
    now = sha(p)
    pres = [os.path.basename(c) for c in cands if os.path.exists(c) and sha(c) == m.group(2)]
    print('PARCIAL', os.path.basename(p), 'match_now' if now == m.group(2) else 'CHANGED', pres)
