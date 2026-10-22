"""Search the immutable supplemental DOCX index without executing source content."""
from pathlib import Path
import argparse, hashlib, json, unicodedata

ROOT=Path(__file__).resolve().parent
def fold(s):
    return ''.join(c for c in unicodedata.normalize('NFKD',s.casefold()) if not unicodedata.combining(c))

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('query');ap.add_argument('--max',type=int,default=15);a=ap.parse_args()
    d=json.loads((ROOT/'SUPPLEMENT_R67.json').read_text(encoding='utf-8')); seen=set();found=[]
    for r in d['recovered']+d['selected']:
        key=r['source_sha256']
        if key in seen:continue
        seen.add(key);p=ROOT/'extracted'/f'{key}.json';b=p.read_bytes()
        if hashlib.sha256(b).hexdigest()!=r['sha256']:raise ValueError(f'Extract hash mismatch: {p}')
        doc=json.loads(b)
        for x in doc['paragraphs']:
            if fold(a.query) in fold(x['text']):found.append({'sources':doc['paths'],'source_sha256':key,**x})
    print(json.dumps({'matches':len(found),'shown':found[:a.max],'scope':'supplemental extraction, not entire corpus'},ensure_ascii=False,indent=2))
