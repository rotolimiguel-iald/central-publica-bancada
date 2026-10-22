# analisa_c.py — matriz de MORDIDA (cético 2): por campo, (a) erros REMOVIDOS de probes negativos (mordida);
# (b) teoremas que QUEBRAM (erro novo ou sorryAx novo) nos arquivos de teoremas/paredes/cético.
import json, os
CV = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = json.load(open(os.path.join(CV, 'mut', 'resultado_c.json'), encoding='utf-8'))
base = next(r for r in R if r['name'] == 'BASE')
NEG = ['ProbeToyV3.lean', 'ProbeLegacyV3.lean', 'ProbeVacuousImportV3.lean', 'ProbeTrivialH3v3.lean']
THM = ['ContratoQG_v3_Teoremas.lean', 'ContratoQG_v3_Paredes.lean', 'FlagNetV3.lean', 'ProbeAjusteH3v3.lean',
       'CeticoKappaGauge.lean', 'CeticoH3Ajuste.lean']
out = []; kt = set(); oom = 0
for r in R:
    for f in r:
        if isinstance(r[f], dict) and 'kt' in r[f]:
            kt.update(r[f]['kt']); oom += int(r[f]['oom'])
    if r['name'] == 'BASE': continue
    row = {'campo': f"{r['struct']}.{r['field']}", 'core_rc': r['ContratoQG_v3.lean']['rc']}
    row['mordida_neg'] = {f[:-5]: sorted(set(base[f]['errors']) - set(r[f]['errors'])) for f in NEG
                          if set(base[f]['errors']) - set(r[f]['errors'])}
    row['novos_erros_neg'] = {f[:-5]: sorted(set(r[f]['errors']) - set(base[f]['errors'])) for f in NEG
                              if set(r[f]['errors']) - set(base[f]['errors'])}
    br = {}
    for f in THM:
        e = sorted(set(r[f]['errors']) - set(base[f]['errors']))
        s = sorted(set(r[f]['sorry_decls']) - set(base[f]['sorry_decls']))
        if e or s: br[f[:-5]] = {'erros': e, 'sorryAx': [x.split('.')[-1] for x in s]}
    row['teoremas_quebrados'] = br
    out.append(row)
json.dump({'linhas': out, 'kernel_touched': sorted(kt), 'oom_logs': oom}, open(os.path.join(CV, 'mut', 'matriz_c.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
bite = [x['campo'] for x in out if x['mordida_neg']]
DER = ['ContratoQG_v3_Teoremas', 'ContratoQG_v3_Paredes', 'FlagNetV3']
cons = [x['campo'] for x in out if any(k in DER for k in x['teoremas_quebrados'])]
none = [x['campo'] for x in out if not x['mordida_neg'] and not any(k in DER for k in x['teoremas_quebrados'])]
print('n', len(out), 'core_rc!=0', [x['campo'] for x in out if x['core_rc'] != 0], 'kernel_touched', sorted(kt), 'oom', oom)
print('MORDIDOS por probe negativo (%d):' % len(bite), bite)
print('CONSUMIDOS por teorema do projetista (Teoremas/Paredes/FlagNet) (%d)' % len(cons))
print('NEM MORDIDA NEM CONSUMO (%d):' % len(none), none)
for x in out:
    print(x['campo'], '| mordida:', x['mordida_neg'], '| quebra:', {k: len(v['erros']) + len(v['sorryAx']) for k, v in x['teoremas_quebrados'].items()})
