"""Select the reviewed package revisions without overwriting an earlier builder."""
from pathlib import Path
R=Path(__file__).resolve().parent
s=(R/'build_final_bundle_v3_3_013bis.py').read_text(encoding='utf-8')
for base in ['C7_POSTERIOR_REPRODUCTION','C7_GWTC3_REPRODUCTION','C7_INJECTION_REPRODUCTION']:
    s=s.replace(base+'_v3',base+'_v3_1')
s=s.replace("'bis/C7_SUPPLEMENTS_V3_CLEANUP_CONTROLS.json',","'bis/C7_SUPPLEMENTS_V3_CLEANUP_CONTROLS.json','bis/C7_SUPPLEMENTS_V3_1_BUILD.json',")
with (R/'build_final_bundle_v3_final_013bis.py').open('xb') as f:f.write(s.encode())
