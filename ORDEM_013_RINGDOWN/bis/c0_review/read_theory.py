"""Fetch primary theory into memory only; retain metadata in the authorized report."""
import hashlib
import io
import json
import os
import urllib.request
from pathlib import Path
from pypdf import PdfReader

base = Path(__file__).resolve().parents[1]
target = base/'C0_ADVERSARIAL_SOURCE_REVIEW.json'
report = json.loads(target.read_bytes())
url = 'https://www.numdam.org/item/10.24033/asens.1247.pdf'
req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
data = urllib.request.urlopen(req, timeout=40).read()
reader = PdfReader(io.BytesIO(data))
pages = [reader.pages[i].extract_text() for i in (1, 2)]
assert 'trace normale' in pages[0] and 'modulaire' in pages[1]
report['external_primary'] = [
 {'author':'Alain Connes','year':1973,'title':'Une classification des facteurs de type III',
  'doi':'10.24033/asens.1247','url':url,'bytes':len(data),
  'sha256':hashlib.sha256(data).hexdigest(),'pages_total':len(reader.pages),
  'read_scope':'Printed pages 133-134 only; PDF pages 2-3. Downloaded into memory; no local PDF written.',
  'short_quote':'une trace normale fidèle semi-finie',
  'criterion':'A factor is not type III iff it admits a faithful normal semifinite trace; III1 is a subtype of III.',
  'ocr_note':'The not-equal sign is OCRed as 7^ in the PDF extraction; author-site indexed mathematical text also checked (not equal III).',
  'attempts':['web.open author and Numdam PDFs: content too large','sandbox urllib: network unreachable','author PDF urllib escalated: HTTP 403','Numdam urllib with User-Agent: success']},
 {'author':'Jonathan Sorce','title':"A short proof of Tomita’s theorem",'arxiv':'2309.16762v2',
  'url':'https://arxiv.org/html/2309.16762v2','read_scope':'Introduction, equations (1)-(6), web extracted lines 30-55; not full proof.',
  'sha256':None,'hash_note':'Read with web tool, original response bytes not available; no hash invented.',
  'result':'For a cyclic separating vector, S=J Delta^(1/2), Delta is positive self-adjoint injective, and modular flow preserves the algebra.'}
]
payload = (json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
tmp = base/'c0_review/theory.tmp'
tmp.write_bytes(payload)
assert tmp.stat().st_size == len(payload)
os.replace(tmp,target)
print(json.dumps(report['external_primary'],ensure_ascii=False,indent=2))
