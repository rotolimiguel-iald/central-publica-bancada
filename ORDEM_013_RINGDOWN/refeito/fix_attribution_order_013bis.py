"""Finish all document bytes before hashing attributions, in a new candidate."""
from pathlib import Path
import ast
R=Path(__file__).resolve().parent
s=(R/'build_independent_v3_2_013bis.py').read_text(encoding='utf-8')
s=s.replace('C7_INDEPENDENT_v3_2','C7_INDEPENDENT_v3_3').replace('C7_V3_2_BUILD.json','C7_V3_3_BUILD.json')
start=s.index('licence_rows=[]');end=s.index("for n in ('README.md','OVERVIEW.md'):",start)
block=s[start:end];s=s[:start]+s[end:]
anchor='for n,raw in sorted(content.items()):put(n,raw)'
guard='''attributions=json.loads(content['provenance/SHIPPED_ATTRIBUTIONS.json'])['files']
expected=set(content)-{'provenance/SHIPPED_ATTRIBUTIONS.json'}
names=[r['path'] for r in attributions]
if len(names)!=len(set(names)) or set(names)!=expected:raise ValueError('Attribution coverage/duplicates')
for row in attributions:
    if row['sha256']!=hashlib.sha256(content[row['path']]).hexdigest():raise ValueError('Attribution bytes differ')
'''
if s.count(anchor)!=1:raise ValueError('Anchor')
s=s.replace(anchor,block+guard+anchor);ast.parse(s)
with (R/'build_independent_v3_3_013bis.py').open('xb') as f:f.write(s.encode())
s=(R/'build_final_bundle_v3_013bis.py').read_text(encoding='utf-8').replace('C7_INDEPENDENT_v3_2','C7_INDEPENDENT_v3_3')
s=s.replace('The recorded fresh C6-pre replay has 75 rows', 'The recorded fresh C6-pre replay of v3_2, whose complete execution tree is byte-identical to v3_3, has 75 rows')
s=s.replace("'bis/C7_V3_2_CLEAN_VALIDATION.json',", "'bis/C7_V3_2_CLEAN_VALIDATION.json','bis/C7_V3_3_DOCUMENTARY_VALIDATION.json',")
ast.parse(s)
with (R/'build_final_bundle_v3_3_013bis.py').open('xb') as f:f.write(s.encode())
