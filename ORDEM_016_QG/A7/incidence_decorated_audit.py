"""Independent half-edge oracle and color-preserving permutation audit."""
from pathlib import Path
from datetime import datetime, timezone
from itertools import combinations, permutations, product
from collections import Counter, defaultdict
import hashlib, json, time, uuid

HERE = Path(__file__).resolve().parent
DEST = HERE / 'incidence_decorated_audit'
DEST.mkdir(exist_ok=True)

def write_new(name, obj):
    p = DEST / name
    assert not p.exists()
    data = json.dumps(obj, ensure_ascii=False, indent=2).encode()
    tmp = p.with_name(p.name + '.tmp_' + uuid.uuid4().hex)
    tmp.write_bytes(data)
    assert tmp.read_bytes() == data
    tmp.replace(p)

write_new('PRE_REGISTER.json', dict(at=datetime.now(timezone.utc).isoformat(),
    route='No imports from production engine: explicit slot matchings E<=3; all color-preserving vertex permutations for every stored row',
    inventory_sha256=hashlib.sha256((HERE/'incidence_decorated/inventory.json').read_bytes()).hexdigest(),
    script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    cpu_budget_seconds=120, scope='Action types only, not amplitudes or Ward insertions'))
start = time.process_time()
catalog = json.loads((HERE/'incidence_decorated/inventory.json').read_bytes())
signatures = {'GHOST': ['CB','C','H'], 'HDAG': ['HDAG','C','H'], 'CDAG': ['CDAG','C','C']}
ghost = dict(H=0, C=1, CB=-1, HDAG=-1, CDAG=-2)

def normalized(colors, edges):
    groups = defaultdict(list)
    for i, color in enumerate(colors):
        groups[color].append(i)
    best = None
    count = 0
    for ps in product(*(permutations(groups[c]) for c in sorted(groups))):
        order = sum(ps, ())
        inv = {old:new for new, old in enumerate(order)}
        new_edges = []
        for typ, a, b in edges:
            a, b = inv[a], inv[b]
            if typ == 'M': a, b = min(a,b), max(a,b)
            new_edges.append((typ,a,b))
        key = tuple(sorted(new_edges))
        if best is None or key < best: best, count = key, 1
        elif key == best: count += 1
    return (tuple(sorted(colors)), best), count

def check_row(row):
    colors = list(zip(row['valences'],row['classes']))
    n = len(colors)
    rem = [Counter(['H']*v if kind=='METRIC' else signatures[kind]) for v,kind in colors]
    adjacent = [set() for _ in colors]
    for typ,i,j in row['edges']:
        assert typ in ('M','G') and 0<=i<n and 0<=j<n
        f,g = ('H','H') if typ=='M' else ('C','CB')
        rem[i][f]-=1;rem[j][g]-=1
        adjacent[i].add(j);adjacent[j].add(i)
    assert all(x>=0 for r in rem for x in r.values())
    seen={0};todo=[0]
    while todo:
        for j in adjacent[todo.pop()]-seen: seen.add(j);todo.append(j)
    assert len(seen)==n and len(row['edges'])-n+1==1
    ext=Counter()
    for r in rem: ext.update({k:v for k,v in r.items() if v})
    assert dict(ext)==row['external'] and sum(ext.values())==row['E']
    assert sum(ghost[k]*v for k,v in ext.items())==row['ghost']==0
    assert [dict((k,v) for k,v in r.items() if v) for r in rem]==row['external_by_vertex']
    key,aut=normalized(colors,row['edges'])
    assert aut==row['vertex_automorphisms']
    return key

keys_by_E=defaultdict(set)
for row in catalog:
    key=check_row(row)
    assert key not in keys_by_E[row['E']]
    keys_by_E[row['E']].add(key)
    if time.process_time()-start>120: raise RuntimeError('Audit budget')

def oracle_family(valences):
    n=len(valences);out=set();raw=0
    choices=[['METRIC','GHOST','HDAG','CDAG'] if v==3 else ['METRIC'] for v in valences]
    for kinds in product(*choices):
        half=[]
        for i,(v,k) in enumerate(zip(valences,kinds)):
            half.extend((i,s) for s in (['H']*v if k=='METRIC' else signatures[k]))
        possible=[]
        for a,b in combinations(range(len(half)),2):
            i,f=half[a];j,g=half[b]
            if f==g=='H': possible.append((a,b,('M',i,j)))
            elif {f,g}=={'C','CB'}:
                possible.append((a,b,('G',i,j) if f=='C' else ('G',j,i)))
        for selection in combinations(possible,n):
            used=[x for a,b,e in selection for x in (a,b)]
            if len(set(used))!=2*n: continue
            reach={0}
            for _ in range(n):
                reach |= {j for a,b,(t,i,j) in selection if i in reach}
                reach |= {i for a,b,(t,i,j) in selection if j in reach}
            if len(reach)!=n:continue
            raw+=1
            out.add(normalized(list(zip(valences,kinds)),[e for a,b,e in selection])[0])
    return out,raw

families={1:[(3,)],2:[(4,),(3,3)],3:[(5,),(4,3),(3,3,3)]}
oracle=[]
for E,vs_list in families.items():
    total=set();raw=0
    for vs in vs_list:
        found, nr=oracle_family(vs);total|=found;raw+=nr
    assert total==keys_by_E[E], (E,len(total),len(keys_by_E[E]))
    oracle.append(dict(E=E,types=len(total),labeled_slot_matchings=raw))

# A real class mutation must change the certificate of the metric tadpole.
assert normalized([(3,'METRIC')],[('M',0,0)])[0]!=normalized([(3,'GHOST')],[('G',0,0)])[0]
# Same and opposite orientations are distinct, whether physically admissible or not.
cols=[(3,'GHOST')]*2
assert normalized(cols,[('G',0,1),('G',1,0)])[0]!=normalized(cols,[('G',0,1),('G',0,1)])[0]
bad=dict(catalog[0]);bad['external']={'H':999}
try:check_row(bad)
except AssertionError:pass
else:raise AssertionError('Mutation escaped independent validator')
result=dict(at=datetime.now(timezone.utc).isoformat(),rows_checked=len(catalog),
    no_duplicate_types=True,all_vertex_automorphisms_independently_checked=True,
    oracle=oracle,negative_controls=3,all_amplitude_weights_unassigned=True,
    cpu_seconds=time.process_time()-start,full_quantum_anomaly=False)
assert all(row['amplitude_weight'] is None for row in catalog)
write_new('results.json',result)
print(json.dumps(result),flush=True)
