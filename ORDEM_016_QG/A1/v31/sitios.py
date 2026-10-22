# sitios.py <arquivo.lean> <log> : mapeia cada linha de erro ao (declaracao.campo) que a contem.
import re, sys, json, os

def sites(path):
    out = {}; decl = None; fld = None
    for n, l in enumerate(open(path, encoding='utf-8').read().split('\n'), start=1):
        m = re.match(r'^(?:private |protected |noncomputable )*(theorem|def|lemma|abbrev|instance|example)\s+([^\s(:{\[]*)', l)
        if m:
            decl = m.group(2) or m.group(1); fld = None
        m2 = re.match(r"^  ([A-Za-zΔ_][\w'Δ₀-₉]*) :=", l)
        if m2 and decl is not None:
            fld = m2.group(1)
        out[n] = (decl + ('.' + fld if fld else '')) if decl else '?'
    return out

def errs(src, log):
    s = open(log, encoding='utf-8', errors='replace').read() if os.path.exists(log) else ''
    st = sites(src)
    base = os.path.basename(src)
    lines = sorted(set(int(m.group(1)) for m in re.finditer(re.escape(base) + r':(\d+):\d+: error', s)))
    rc = re.findall(r'rc=(\d+)', s)
    sorry = sorted(set(re.findall(r"'([^']+)' depends on axioms: \[[^\]]*sorryAx", s, re.S)))
    return {'rc': int(rc[-1]) if rc else None, 'linhas': lines,
            'sitios': sorted(set(st.get(n, '?') for n in lines)), 'sorryAx': sorry,
            'oom': 'bad_alloc' in s}

if __name__ == '__main__':
    print(json.dumps(errs(sys.argv[1], sys.argv[2]), ensure_ascii=False))
