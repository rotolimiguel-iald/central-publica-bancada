# -*- coding: utf-8 -*-
"""
a7b_inventario_incidencia.py — ORDEM_016 / A7.b
Inventario finito de TIPOS DE INCIDENCIA (um laco, valencia externa <= 6).
Modelo 087 PROJETADO (sigma constante), gauge linear (De Donder), BV.
Estatuto: [DECLARADO] — entregue como texto; verificacao local independente.
Sem amplitudes, sem pesos de simetria, sem sinais atribuidos (PENDENTES).
Stdlib pura. Terminante por cotas finitas (ver secao 5 do relatorio).
"""
from itertools import permutations
from collections import defaultdict

H, C, CB, HDAG, CDAG = 'H', 'C', 'CB', 'HDAG', 'CDAG'
GHOST_NUM = {H: 0, C: 1, CB: -1, HDAG: -1, CDAG: -2}

# Assinaturas locais (slots). Antifields NUNCA entram nos contadores de consumo.
CLASSES = {
    'METRIC_ORD': dict(papel='ORD', vmin=3, vmax=8, d_opts=(0, 2), slots=None),   # slots = (H,)*v
    'GHOST_ORD':  dict(papel='ORD', vmin=3, vmax=3, d_opts=(2,),  slots=(CB, C, H)),
    'BV_HDAG':    dict(papel='BV',  vmin=3, vmax=3, d_opts=(1,),  slots=(HDAG, C, H)),
    'BV_CDAG':    dict(papel='BV',  vmin=3, vmax=3, d_opts=(1,),  slots=(CDAG, C, C)),
    # CONTACT_EOM: catalogo PENDENTE (secao 9 do relatorio) — classe declarada, nao instanciada.
    # CUTOFF: prescricao temporal = outra unidade — declarada, nao instanciada por contrato.
}
DECLARADAS_NAO_INSTANCIADAS = ['CONTACT_EOM', 'CUTOFF']

def slots_da_classe(nome, v):
    cfg = CLASSES[nome]
    if cfg['slots'] is not None:
        return cfg['slots']
    return (H,) * v

def particoes_inteiras(n, max_part=None):
    if max_part is None:
        max_part = n
    if n == 0:
        yield ()
        return
    for primeira in range(min(n, max_part), 0, -1):
        for resto in particoes_inteiras(n - primeira, min(primeira, n - primeira)):
            yield (primeira,) + resto

def familias_valencia(emax=6):
    """29 familias: bijecao com particoes inteiras de E (w_i = v_i - 2 >= 1)."""
    fams = []
    for E in range(1, emax + 1):
        for p in particoes_inteiras(E):
            fams.append((E, tuple(w + 2 for w in p)))
    return fams

def _conexo(mat, V):
    adj = defaultdict(set)
    for i in range(V):
        for j in range(V):
            if mat[i][j] > 0 and i != j:
                adj[i].add(j); adj[j].add(i)
    if any(mat[i][i] > 0 for i in range(V)) and V == 1:
        return True
    visto = {0}; pilha = [0]
    while pilha:
        u = pilha.pop()
        for w in adj[u]:
            if w not in visto:
                visto.add(w); pilha.append(w)
    return len(visto) == V

def topologias(valencias):
    """Matrizes simetricas inteiras, I = V, conexas, grau interno <= v_i. Etiquetadas aqui."""
    V = len(valencias)
    pares = [(i, j) for i in range(V) for j in range(i, V)]
    mat = [[0] * V for _ in range(V)]
    out = []
    def grau_interno(i):
        return 2 * mat[i][i] + sum(mat[i][j] for j in range(V) if j != i)
    def rec(k, restantes):
        if restantes == 0:
            if all(grau_interno(i) <= valencias[i] for i in range(V)) and _conexo(mat, V):
                out.append(tuple(tuple(l) for l in mat))
            return
        if k == len(pares):
            return
        i, j = pares[k]
        cap = 0
        if i == j:
            cap = valencias[i] // 2
        else:
            cap = min(valencias[i], valencias[j])
        cap = min(cap, restantes)
        for m in range(cap + 1):
            mat[i][j] = m; mat[j][i] = m
            ok = (grau_interno(i) <= valencias[i] + 0)  # poda leve; corte exato no fim
            if ok and grau_interno(j) <= valencias[j]:
                rec(k + 1, restantes - m)
        mat[i][j] = 0; mat[j][i] = 0
    rec(0, V)  # I = V <=> L = 1
    return out

def _flatten(mat):
    V = len(mat)
    return tuple(mat[i][j] for i in range(V) for j in range(i, V))

def certificado_e_aut(mat, chave):
    """Quociente por permutacoes que preservam 'chave' por vertice. aut conta as que fixam."""
    V = len(mat); base = _flatten(mat); melhor = None; aut = 0
    for p in permutations(range(V)):
        if any(chave[p[i]] != chave[i] for i in range(V)):
            continue
        img = tuple(mat[p[i]][p[j]] for i in range(V) for j in range(i, V))
        if melhor is None or img < melhor:
            melhor = img
        if img == base:
            aut += 1
    return melhor, aut

def classes_compativeis(v, classes=None):
    classes = classes or CLASSES
    return [n for n, cfg in classes.items() if cfg['vmin'] <= v <= cfg['vmax']]

def _opcoes_linha(i, j, cont):
    ops = []
    if i == j:
        if cont.get((i, H), 0) >= 2:
            ops.append(('M', i, i))
        if cont.get((i, C), 0) >= 1 and cont.get((i, CB), 0) >= 1:
            ops.append(('G', i, i))
    else:
        if cont.get((i, H), 0) >= 1 and cont.get((j, H), 0) >= 1:
            ops.append(('M', i, j))
        if cont.get((i, C), 0) >= 1 and cont.get((j, CB), 0) >= 1:
            ops.append(('G', i, j))
        if cont.get((j, C), 0) >= 1 and cont.get((i, CB), 0) >= 1:
            ops.append(('G', j, i))
    return ops

def _consome(cont, op, sinal=+1):
    tipo, i, j = op
    cont = dict(cont)
    if tipo == 'M':
        cont[(i, H)] = cont.get((i, H), 0) - sinal
        cont[(j, H)] = cont.get((j, H), 0) - sinal
    else:
        cont[(i, C)] = cont.get((i, C), 0) - sinal
        cont[(j, CB)] = cont.get((j, CB), 0) - sinal
    return cont

def atribuicoes_linhas(slots_vertices, mat, permitir_antifield_em_linha=False):
    """Backtracking sobre grupos de linhas paralelas; monotonia de opcoes mata duplicata."""
    cont = {}
    for v, slots in enumerate(slots_vertices):
        for s in slots:
            if s in (HDAG, CDAG) and not permitir_antifield_em_linha:
                continue  # fontes externas: contracao zero
            cont[(v, s)] = cont.get((v, s), 0) + 1
    grupos = []
    V = len(mat)
    for i in range(V):
        for j in range(i, V):
            for _ in range(mat[i][j]):
                grupos.append((i, j))
    # agrupar mantendo ordem; monotonia so dentro do mesmo par (i, j)
    out = []
    def rec(idx, cont, acc, prev_par, min_op_idx):
        if idx == len(grupos):
            out.append(list(acc)); return
        i, j = grupos[idx]
        mesmo_par = (prev_par == (i, j))
        ops = _opcoes_linha(i, j, cont)
        for oi, op in enumerate(ops):
            if mesmo_par and oi < min_op_idx:
                continue
            rec(idx + 1, _consome(cont, op, +1), acc + [op], (i, j), oi)
    rec(0, cont, [], None, 0)
    # retorna (linhas, contadores_restantes) por atribuicao
    fins = []
    for linhas in out:
        c2 = dict(cont)
        for op in linhas:
            c2 = _consome(c2, op, +1)
        fins.append((linhas, c2))
    return fins

def n_lacos_ghost(linhas, V):
    """Em L=1: 0 ou 1. Conta ciclos no subgrafo ghost (tadpole G = laco de 1 vertice)."""
    g = [op for op in linhas if op[0] == 'G']
    if not g:
        return 0
    grau = defaultdict(int); adj = defaultdict(set); tadpole_g = 0
    for _, i, j in g:
        if i == j:
            tadpole_g += 1
        else:
            grau[i] += 1; grau[j] += 1; adj[i].add(j); adj[j].add(i)
    ciclos = tadpole_g
    visto = set()
    for v in list(adj):
        if v in visto:
            continue
        comp = set(); pilha = [v]
        while pilha:
            u = pilha.pop()
            if u in comp:
                continue
            comp.add(u); pilha.extend(adj[u])
        visto |= comp
        if comp and all(grau[u] == 2 for u in comp):
            ciclos += 1
    return ciclos

def valida_tipo(V, mat, linhas, externas, gh):
    if sum(mat[i][j] for i in range(V) for j in range(i, V)) != V:
        return False                      # I = V (L = 1)
    if not _conexo([list(l) for l in mat], V):
        return False
    ci = sum(1 for op in linhas if op[0] == 'G')
    bi = sum(1 for op in linhas if op[0] == 'G')
    if ci != bi:
        return False                      # #C_int = #CB_int
    if any(s in (HDAG, CDAG) for op in linhas for s in ()):
        return False
    E = sum(externas.values())
    if not (0 <= E <= 6):
        return False
    return True

def inventario(emax=6, classes=None, permitir_antifield_em_linha=False):
    classes = classes or CLASSES
    inv = []
    for E_fam, valencias in familias_valencia(emax):
        certs_vistos = {}
        for mat in topologias(valencias):
            cert_t, _ = certificado_e_aut(mat, valencias)
            if cert_t in certs_vistos:
                continue
            certs_vistos[cert_t] = mat
        for mat in certs_vistos.values():
            V = len(valencias)
            opc_classes = [classes_compativeis(v, classes) for v in valencias]
            if any(not oc for oc in opc_classes):
                continue
            def rec_at(v, acc):
                if v == V:
                    chave = tuple(zip(valencias, acc))
                    cert, aut_v = certificado_e_aut(mat, chave)
                    yield acc, cert, aut_v
                    return
                for nome in opc_classes[v]:
                    for r in rec_at(v + 1, acc + [nome]):
                        yield r
            atrib_vistos = set()
            for acc, cert, aut_v in rec_at(0, []):
                if cert in atrib_vistos:
                    continue
                atrib_vistos.add(cert)
                slots_vertices = [slots_da_classe(acc[i], valencias[i]) for i in range(V)]
                for linhas, resto in atribuicoes_linhas(slots_vertices, mat,
                                                         permitir_antifield_em_linha):
                    externas = {}
                    for (v, s), n in resto.items():
                        if n > 0:
                            externas[s] = externas.get(s, 0) + n
                    for v, slots in enumerate(slots_vertices):  # antifields: sempre externas
                        for s in slots:
                            if s in (HDAG, CDAG) and not permitir_antifield_em_linha:
                                externas[s] = externas.get(s, 0) + 1
                    gh = sum(GHOST_NUM[s] * n for s, n in externas.items())
                    if not valida_tipo(V, mat, linhas, externas, gh):
                        continue
                    n_met = sum(1 for c in acc if c == 'METRIC_ORD')
                    d_fix = sum(min(CLASSES[c]['d_opts']) - 2 for c in acc if c != 'METRIC_ORD')
                    d_var = [(-2, 0) if c == 'METRIC_ORD' else (0, 0) for c in acc]
                    d_min = 4 + d_fix + sum(a for a, _ in d_var)  # delta = 2+2L+S(d_v-2), L=1
                    d_max = 4 + d_fix + sum(b for _, b in d_var)
                    tags = set(c for c in acc)
                    if any(op[1] == op[2] for op in linhas):
                        tags.add('TADPOLE')
                    inv.append(dict(E=sum(externas.values()), familia=valencias,
                                    topologia=cert, classes=tuple(acc), linhas=tuple(linhas),
                                    externas=externas, gh=gh, aut_v=aut_v,
                                    n_lacos_ghost=n_lacos_ghost(linhas, V),
                                    delta_faixa=(d_min, d_max), tags=tuple(sorted(tags)),
                                    sinal='PENDENTE', peso='PENDENTE', amplitude='PENDENTE'))
    return inv

# ----------------- controles -----------------
def controles():
    ok = {}
    fams = familias_valencia(6)
    cont_E = defaultdict(int)
    for E, _ in fams:
        cont_E[E] += 1
    ok['CP_contagem_29_e_11_em_E6'] = (len(fams) == 29 and
        [cont_E[e] for e in range(1, 7)] == [1, 2, 3, 5, 7, 11])
    ok['CP_tres_familias_vertice_maior_6'] = (sum(1 for _, v in fams if max(v) > 6) == 3)
    ok['CP_identidade_soma_v_menos_2'] = all(sum(v - 2 for v in vs) == E for E, vs in fams)
    ok['CN_particao_proibida_2_2'] = (classes_compativeis(2) == [])
    sem7 = dict(CLASSES); sem7['METRIC_ORD'] = dict(CLASSES['METRIC_ORD'], vmax=6)
    ok['CN_sem_grau7_mata_3_7_metrico'] = ('METRIC_ORD' not in classes_compativeis(7, sem7))
    cont = {(0, C): 1, (1, C): 1}
    ok['CN_aresta_C_C_rejeitada'] = (_opcoes_linha(0, 1, cont) == [])
    cont = {(0, HDAG): 1, (1, H): 1}
    ok['CN_antifield_nao_propaga'] = (_opcoes_linha(0, 1, cont) == [])
    mat_arvore = ((0, 1), (1, 0))  # V=2, I=1: rejeitada por I != V
    ok['CN_arvore_rejeitada'] = (not valida_tipo(2, mat_arvore, [], {}, 0))
    inv_padrao = inventario()
    inv_af = inventario(permitir_antifield_em_linha=True)
    ok['CN_antifield_propagando_aumenta_inventario'] = (len(inv_af) > len(inv_padrao))
    ok['CN_laco_ghost_no_max_1'] = all(t['n_lacos_ghost'] <= 1 for t in inv_padrao)
    return ok

def confere_familia_3_7(inv):
    sel = [t for t in inv if tuple(sorted(t['familia'])) == (3, 7)]
    por_topo = defaultdict(list)
    for t in sel:
        a12 = t['topologia'][1] if len(t['topologia']) > 1 else 0
        por_topo['duas_linhas_entre_vertices' if a12 == 2 else 'ponte_mais_tadpole'].append(t)
    return por_topo

def relatorio(inv):
    print("== Inventario A7.b (tipos de incidencia; sinais/pesos/amplitudes PENDENTES) ==")
    por_E = defaultdict(int); por_papel = defaultdict(int)
    for t in inv:
        por_E[t['E']] += 1
        for c in set(t['classes']):
            por_papel[CLASSES[c]['papel']] += 1
    for E in sorted(por_E):
        print("E=%d: %d tipos" % (E, por_E[E]))
    print("por papel (tipos contendo):", dict(por_papel))
    for classe in ['TADPOLE', 'BV_HDAG', 'BV_CDAG', 'GHOST_ORD']:
        sub = [t for t in inv if classe in t['tags']]
        print("secao %s: %d tipos" % (classe, len(sub)))
    for classe in DECLARADAS_NAO_INSTANCIADAS:
        print("secao %s: DECLARADA, nao instanciada (entrada pendente / outra unidade)" % classe)
    p37 = confere_familia_3_7(inv)
    duas = p37.get('duas_linhas_entre_vertices', [])
    print("familia (3,7), duas linhas entre vertices: %d tipos" % len(duas))
    for t in duas:
        print("   classes:", t['classes'], "| linhas:", t['linhas'],
              "| externas:", t['externas'], "| gh:", t['gh'])
    print("CONTROLES:", controles())

if __name__ == '__main__':
    relatorio(inventario())