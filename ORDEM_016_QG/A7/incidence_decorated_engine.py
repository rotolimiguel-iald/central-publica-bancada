"""Finite decorated one-loop action incidence types; no amplitudes or Ward insertions."""
from collections import Counter,defaultdict
from itertools import permutations,product
from math import factorial

SLOTS={'GHOST':('CB','C','H'),'HDAG':('HDAG','C','H'),'CDAG':('CDAG','C','C')}
GHOST={'H':0,'C':1,'CB':-1,'HDAG':-1,'CDAG':-2}
def slots(kind,valence):
    if kind=='METRIC':return ('H',)*valence
    if valence!=3 or kind not in SLOTS:raise ValueError('Invalid vertex signature')
    return SLOTS[kind]
def families(n,maximum=None):
    if n==0:yield ();return
    for k in range(min(n,maximum or n),0,-1):
        for r in families(n-k,k):yield (k+2,)+r
def connected(n,edges):
    seen={0};change=True
    while change:
        change=False
        for _,i,j in edges:
            if (i in seen) != (j in seen):seen.update([i,j]);change=True
    return len(seen)==n
def canonical(valences,classes,edges):
    """Canonical colors + all typed/directed edges; count decorated vertex automorphisms."""
    n=len(valences);degree=[Counter() for _ in range(n)]
    for typ,i,j in edges:
        if typ in ('M','U'):
            degree[i][typ]+=1;degree[j][typ]+=1
            if i==j:degree[i][typ+'loop']+=1
        else:
            degree[i]['Gout']+=1;degree[j]['Gin']+=1
            if i==j:degree[i]['Gloop']+=1
    groups=defaultdict(list)
    for i in range(n):groups[(valences[i],classes[i],tuple(sorted(degree[i].items())))].append(i)
    blocks=[groups[k] for k in sorted(groups)]
    best=None;aut=0
    for choices in product(*(permutations(block) for block in blocks)):
        order=tuple(i for block in choices for i in block);inv={i:j for j,i in enumerate(order)}
        colors=tuple((valences[i],classes[i]) for i in order)
        remapped=[]
        for typ,i,j in edges:
            u,v=inv[i],inv[j]
            if typ in ('M','U') and u>v:u,v=v,u
            remapped.append((typ,u,v))
        code=(colors,tuple(sorted(remapped)))
        if best is None or code<best:best=code;aut=1
        elif code==best:aut+=1
    return best,aut
def topologies(valences):
    n=len(valences);pairs=[(i,j) for i in range(n) for j in range(i,n)]
    degree=[0]*n;seen=set()
    def visit(start,left,edges):
        if not left:
            if not connected(n,edges):return
            code,_=canonical(valences,('',)*n,edges)
            if code not in seen:
                seen.add(code);yield tuple(edges)
            return
        for k in range(start,len(pairs)):
            i,j=pairs[k]
            if degree[i]+(2 if i==j else 1)>valences[i] or degree[j]+1>valences[j]:continue
            degree[i]+=1;degree[j]+=1
            yield from visit(k,left-1,edges+[('U',i,j)])
            degree[i]-=1;degree[j]-=1
    yield from visit(0,n,[])
def assignments(valences,classes,untyped):
    remaining=[Counter(slots(c,v)) for c,v in zip(classes,valences)]
    def visit(k,edges):
        if k==len(untyped):yield tuple(edges);return
        _,i,j=untyped[k];options=[]
        if (remaining[i]['H']>=2 if i==j else remaining[i]['H'] and remaining[j]['H']):options.append(('M',i,j))
        if remaining[i]['C'] and remaining[j]['CB']:options.append(('G',i,j))
        if i!=j and remaining[j]['C'] and remaining[i]['CB']:options.append(('G',j,i))
        for typ,u,v in sorted(options):
            # Stable option values, not indices in a changing option list.
            if k and untyped[k]==untyped[k-1] and (typ,u,v)<edges[-1]:continue
            f,g=('H','H') if typ=='M' else ('C','CB')
            remaining[u][f]-=1;remaining[v][g]-=1
            yield from visit(k+1,edges+[(typ,u,v)])
            remaining[u][f]+=1;remaining[v][g]+=1
    yield from visit(0,[])
def validate(valences,classes,edges,emax=6):
    """Recompute incidence, slots, ghost and external degree; reject malformed data."""
    n=len(valences)
    if n==0 or len(classes)!=n or len(edges)!=n:raise ValueError('one-loop size')
    remaining=[Counter(slots(c,v)) for c,v in zip(classes,valences)]
    for typ,i,j in edges:
        if typ not in ('M','G') or type(i)!=int or type(j)!=int or not(0<=i<n and 0<=j<n):raise ValueError('edge type/endpoint')
        f,g=('H','H') if typ=='M' else ('C','CB')
        remaining[i][f]-=1;remaining[j][g]-=1
        if any(v<0 for row in remaining for v in row.values()):raise ValueError('slot underflow')
    if not connected(n,edges):raise ValueError('not connected')
    external=Counter()
    for row in remaining:external.update({f:v for f,v in row.items() if v})
    E=sum(external.values());gh=sum(GHOST[f]*v for f,v in external.items())
    if E!=sum(valences)-2*len(edges) or not 1<=E<=emax:raise ValueError('external valence')
    if gh!=0:raise ValueError('action catalog ghost conservation')
    return dict(external=dict(sorted(external.items())),E=E,ghost=gh,
                external_by_vertex=[dict(sorted((f,v) for f,v in row.items() if v)) for row in remaining])
def enumerate_family(valences,emax=6):
    outputs={};colored_seen=set()
    for untyped in topologies(valences):
        choices=[('METRIC','GHOST','HDAG','CDAG') if v==3 else ('METRIC',) for v in valences]
        for classes in product(*choices):
            color_code,_=canonical(valences,classes,untyped)
            if color_code in colored_seen:continue
            colored_seen.add(color_code)
            for edges in assignments(valences,classes,untyped):
                derived=validate(valences,classes,edges,emax)
                code,aut=canonical(valences,classes,edges)
                if code in outputs:continue
                colors,canonical_edges=code
                cv=tuple(v for v,c in colors);cc=tuple(c for v,c in colors)
                derived=validate(cv,cc,canonical_edges,emax)
                multiplicities=Counter(canonical_edges)
                edge_aut=1
                for (typ,i,j),m in multiplicities.items():
                    edge_aut*=factorial(m)
                    if typ=='M' and i==j:edge_aut*=2**m
                outputs[code]=dict(valences=cv,classes=cc,edges=canonical_edges,
                    vertex_automorphisms=aut,edge_permutation_reflection_factor=edge_aut,
                    combinatorial_automorphisms=aut*edge_aut,amplitude_weight=None,**derived)
    return list(outputs.values())
