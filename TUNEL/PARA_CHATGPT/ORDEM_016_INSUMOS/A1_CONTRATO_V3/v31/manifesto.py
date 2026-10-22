# manifesto.py — RODADA 2: sha16 LIDO do arquivo (sha256[:16]), rc e axiomas LIDOS dos logs finais.
import hashlib, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sitios import errs  # noqa: E402

def sha16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]

def code_only(p):
    t = open(p, encoding='utf-8').read()
    t = re.sub(r'/-.*?-/', '', t, flags=re.S)
    t = re.sub(r'--[^\n]*', '', t)
    return t

def axioms(log):
    s = open(log, encoding='utf-8', errors='replace').read() if os.path.exists(log) else ''
    items = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", s, re.S)
    bad = [(n, [x.strip() for x in a.split(',')]) for n, a in items
           if set(x.strip() for x in a.split(',')) - {'propext', 'Classical.choice', 'Quot.sound'}]
    noax = re.findall(r"'([^']+)' does not depend on any axioms", s)
    return len(items), len(noax), bad

ARQ = [
 ('ContratoQG_v31.lean', 'O TIPO v3.1 (KillingNormalization, WedgeBoostRep, ContratoH2, StressTensorData, ContratoH3, ContratoImportH3)', 'compila'),
 ('ContratoQG_v31_Teoremas.lean', 'teoremas: coerencia espectral, paredes T1-T4, sinais, kappa fixo dado N e kappa = INPUT, H3 v3.1 (janela, BH, Clausius, 8piG, exclusoes, G nao predito, consumidores)', 'compila'),
 ('ContratoQG_v31_Paredes.lean', 'v2 inter v3.1 vazio, brinquedo W5 excluido (3 rotas), legado, o unico W do kernel => vazio para todo R,N,T', 'compila'),
 ('FlagNetV31.lean', 'rede por bandeiras exclui v3.1 (condicional a KMSUniqueGroup/Takesaki); KMSUniqueFun proibe Z2', 'compila'),
 ('PonteV3V31.lean', 'H2 v3 <=> existe N, H2 v3.1 (a mudanca de H2 e SO o indice)', 'compila'),
 ('ProbeResidualH3v31.lean', 'probe POSITIVO: H3 v3.1 <=> solucao nn covariante como lei fixa da fonte (a divida exata)', 'compila'),
 ('ProbeToyV31.lean', 'probe NEGATIVO: brinquedo W5 vs H2 v3.1', 'falha em {translations_faithful, positive_energy, null_ergodic}'),
 ('ProbeLegacyV31.lean', 'probe NEGATIVO: par legado (U=1) vs H2 v3.1', 'falha em {translations_faithful, null_ergodic}'),
 ('ProbeVacuousImportV31.lean', 'probe NEGATIVO: import ex falso (indice inexistente)', 'falha em {vacuousImportLegacy, vacuousImportToy}'),
 ('ProbeTrivialH3v31.lean', 'probe NEGATIVO: balanco vazio em H3 v3.1', 'falha em {admissible_nontrivial}'),
 ('ProbeAjustadorV31.lean', 'probe NEGATIVO: porte dos ajustadores dos ceticos (toyH3/adjustH3/genericImport/materia por estado)', 'falha em {propagator_covariant, raychaudhuri_einstein, T_covariant}; import herda sorryAx'),
 ('ProbeRekappaV31.lean', 'probe NEGATIVO: porte de rekappa/regauge no mesmo indice N', 'falha em {observer_unit}'),
 ('ContratoQG.lean', 'copia byte-identica da v2 (referencia)', 'compila'),
 ('W5ParedeEspectral.lean', 'copia byte-identica (W5, referencia)', 'compila'),
 ('ProbeToyContratoH2.lean', 'copia byte-identica (o brinquedo W5)', 'compila'),
]
out = []
for f, papel, esperado in ARQ:
    p = os.path.join(HERE, f)
    log = os.path.join(HERE, 'logs', 'final_' + f[:-5] + '.txt')
    e = errs(p, log)
    n, noax, bad = axioms(log)
    s = open(log, encoding='utf-8', errors='replace').read()
    kt = re.findall(r'kernel_files_newer_than_R2_start=(\d+)', s)
    code = code_only(p)
    out.append({'arquivo': f, 'sha16': sha16(p), 'bytes': os.path.getsize(p), 'papel': papel, 'esperado': esperado,
                'rc': e['rc'], 'sitios_de_erro': e['sitios'], 'decls_print_axioms': n, 'sem_axioma': noax,
                'fora_do_trio': bad, 'sorry_no_codigo': len(re.findall(r'\bsorry\b', code)),
                'axiom_no_codigo': len(re.findall(r'^\s*axiom\b', code, re.M)),
                'kernel_touched_since_R2': kt[-1] if kt else None})
for f in ['compile.sh', 'compila_tudo.sh', 'sitios.py', 'ax_check.py', 'manifesto.py', 'DIVERGENCIAS.md',
          'mutacao/mutar.py', 'mutacao/analisa.py', 'mutacao/matriz_mutacao.json', 'mutacao/resultado_mutacao.json']:
    p = os.path.join(HERE, f)
    if os.path.exists(p):
        out.append({'arquivo': f, 'sha16': sha16(p), 'bytes': os.path.getsize(p)})
json.dump(out, open(os.path.join(HERE, 'MANIFESTO_V31.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for o in out:
    print(o['arquivo'], o['sha16'], o.get('rc'), o.get('sitios_de_erro'), o.get('decls_print_axioms'),
          o.get('fora_do_trio'), 'sorry', o.get('sorry_no_codigo'), 'axiom', o.get('axiom_no_codigo'),
          'kt', o.get('kernel_touched_since_R2'))
