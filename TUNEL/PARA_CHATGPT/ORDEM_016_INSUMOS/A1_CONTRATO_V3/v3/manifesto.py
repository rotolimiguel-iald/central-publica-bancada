# manifesto.py — lê do DISCO (nunca de memória) o sha16, o rc e os axiomas de cada artefato da frente contrato_v3.
import hashlib, json, os, re
V3 = os.path.dirname(os.path.abspath(__file__))
TRIO = {'propext', 'Classical.choice', 'Quot.sound'}

def sha16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]

ARQ = [
 ('ContratoQG_v3.lean', 'O TIPO v3 (estruturas WedgeBoostRep, ContratoH2, ContratoH3, ContratoImportH3; só definições)', 'final_core.txt', 'deve compilar'),
 ('ContratoQG_v3_Teoremas.lean', 'teoremas da v3 (coerência espectral, Unruh-KMS, κ, Clausius derivado, paredes)', 'final_teoremas.txt', 'deve compilar'),
 ('ContratoQG_v3_Paredes.lean', 'v2∩v3=∅, brinquedo de W5, par legado, único W do kernel', 'final_paredes.txt', 'deve compilar'),
 ('FlagNetV3.lean', 'rede por bandeiras exclui a v3 (condicional a KMSUnique/Takesaki)', 'final_flagnet.txt', 'deve compilar'),
 ('GuardasV3.lean', 'uma guarda por campo Prop (37)', 'final_guardas.txt', 'deve compilar'),
 ('ProbeToyV3.lean', 'probe negativo: brinquedo de W5 contra a v3', 'final_probe_toy.txt', 'DEVE FALHAR em {translations_faithful, positive_energy, null_ergodic}'),
 ('ProbeLegacyV3.lean', 'probe negativo: par legado (U=1) contra a v3', 'final_probe_legacy.txt', 'DEVE FALHAR em {translations_faithful, null_ergodic}'),
 ('ProbeVacuousImportV3.lean', 'probe negativo: import ex falso (índice inexistente)', 'final_probe_vacuo.txt', 'DEVE FALHAR em {vacuousImportLegacy, vacuousImportToy}'),
 ('ProbeTrivialH3v3.lean', 'probe negativo: balanço vazio em H3', 'final_probe_h3.txt', 'DEVE FALHAR em {admissible_nontrivial}'),
 ('ProbeAjusteH3v3.lean', 'probe positivo: a liberdade residual de H3 (resposta geométrica)', 'final_probe_ajuste.txt', 'deve compilar'),
 ('ContratoQG.lean', 'cópia byte-idêntica da v2 (W2_final) — referência', 'final_v2ref.txt', 'deve compilar'),
 ('W5ParedeEspectral.lean', 'cópia byte-idêntica (W5_final) — referência', 'final_w5parede.txt', 'deve compilar'),
 ('ProbeToyContratoH2.lean', 'cópia byte-idêntica (W5_final) — o brinquedo', 'final_w5toy.txt', 'deve compilar'),
 ('compile.sh', 'compilador (lake env LEAN_PATH + lean -R/-o fora do kernel; find -newer)', None, None),
 ('mutacao/mutar.py', 'harness de mutação campo a campo', None, None),
 ('mutacao/analisa.py', 'leitor da matriz de mutação', None, None),
 ('mutacao/matriz_mutacao.json', 'a matriz medida', None, None),
 ('ax_check.py', 'conferidor de axiomas', None, None),
]

def read_log(name):
    p = os.path.join(V3, 'logs', name)
    if not os.path.exists(p):
        return None
    s = open(p, encoding='utf-8', errors='replace').read()
    items = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", s, re.S)
    bad = [(n, a) for n, a in items if set(x.strip() for x in a.split(',')) - TRIO]
    rc = re.findall(r'rc=(\d+)', s)
    kt = re.findall(r'kernel_files_newer_than_stamp=(\d+)', s)
    lines = sorted(set(int(m.group(1)) for m in re.finditer(r'\.lean:(\d+):\d+: error', s)))
    return {'rc': int(rc[-1]) if rc else None, 'decls_no_trio': len(items) - len(bad), 'fora_do_trio': bad,
            'sorry': s.count('sorry'), 'linhas_com_erro': lines, 'kernel_touched': kt[-1] if kt else None,
            'warnings': s.count(': warning')}

out = []
for f, papel, log, esperado in ARQ:
    p = os.path.join(V3, f)
    e = {'arquivo': f, 'sha16': sha16(p) if os.path.exists(p) else None,
         'bytes': os.path.getsize(p) if os.path.exists(p) else None, 'papel': papel, 'esperado': esperado}
    if log:
        e['log'] = read_log(log)
    out.append(e)
json.dump(out, open(os.path.join(V3, 'MANIFESTO_V3.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for e in out:
    lg = e.get('log') or {}
    print(e['arquivo'], e['sha16'], 'rc=', lg.get('rc'), 'trio=', lg.get('decls_no_trio'), 'fora=', lg.get('fora_do_trio'),
          'erros_linhas=', lg.get('linhas_com_erro'), 'kt=', lg.get('kernel_touched'))
