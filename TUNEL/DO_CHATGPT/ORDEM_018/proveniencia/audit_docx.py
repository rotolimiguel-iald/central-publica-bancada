"""Extract selected OOXML text evidence from scientific DOCX; originals read only."""
from pathlib import Path
import argparse, json, re, zipfile, xml.etree.ElementTree as ET
from audit_provenance import atomic, metadata, OUT
ap = argparse.ArgumentParser()
ap.add_argument('name'); ap.add_argument('file'); ap.add_argument('pattern'); ap.add_argument('--context', type=int, default=3)
a = ap.parse_args()
p=Path(a.file)
meta, raw=metadata(p)
with zipfile.ZipFile(p) as z:
    root=ET.fromstring(z.read('word/document.xml'))
    paragraphs=[''.join(node.itertext()) for node in []]
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    paragraphs=[''.join(t.text or '' for t in node.findall('.//w:t', ns)) for node in root.findall('.//w:p',ns)]
    core=z.read('docProps/core.xml').decode('utf-8') if 'docProps/core.xml' in z.namelist() else None
rx=re.compile(a.pattern,re.I)
hits=[i for i,t in enumerate(paragraphs) if rx.search(t)]
record={'source':meta,'method':'stdlib zipfile + OOXML w:p/w:t; no execution; pandoc absent','core_properties':core,'paragraphs':len(paragraphs),'matched_paragraphs':len(hits),'pattern':a.pattern,'excerpts':[]}
for i in hits:
    first=max(0,i-a.context); last=min(len(paragraphs),i+a.context+1)
    record['excerpts'].append({'match_paragraph':i+1,'first_paragraph':first+1,'last_paragraph':last,'text':'\n'.join(paragraphs[first:last])})
atomic(OUT/(a.name+'.json'),json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(record,ensure_ascii=False,indent=2)[:24000])