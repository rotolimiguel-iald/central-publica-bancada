"""Archive the primary follow-up text actually read, not the inaccessible 1991 paper."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import urllib.request

ROOT = Path(__file__).resolve().parent
TARGET = ROOT/'cache/literature_milburn_followup'
URL = 'https://arxiv.org/html/gr-qc/0308021'


def main():
    TARGET.mkdir(exist_ok=False)
    request = urllib.request.Request(URL, headers={'User-Agent': 'TGL-Order013-primary-source-audit/1.0'})
    with urllib.request.urlopen(request, timeout=40) as response:
        raw = response.read()
        final_url = response.geturl()
        content_type = response.headers.get('Content-Type', '')
    if len(raw) < 20000 or b'Lorentz invariant intrinsic decoherence' not in raw:
        raise ValueError('Unexpected primary source response')
    temporary = TARGET/'milburn_grqc0308021.html.part'
    temporary.write_bytes(raw)
    if temporary.stat().st_size != len(raw):
        raise ValueError('Short download write')
    temporary.replace(TARGET/'milburn_grqc0308021.html')
    record = dict(status='PRIMARY_FOLLOWUP_HTML_ARCHIVED', date_utc=datetime.now(timezone.utc).isoformat(),
        requested_url=URL, final_url=final_url, content_type=content_type, bytes=len(raw),
        sha256=hashlib.sha256(raw).hexdigest(),
        work='G. J. Milburn, Lorentz invariant intrinsic decoherence, arXiv:gr-qc/0308021',
        displayed_identifier='arXiv:gr-qc/0308021v1, 07 Aug 2003',
        consulted_scope='HTML body sections I-III and references read via web; equations23,35,36 used. No figure inspection or original LaTeX/PDF verification.',
        metadata_caution='HTML body contains an automatically regenerated date. Use arXiv identifier/version metadata, not that body date, for the historical version.',
        does_not_represent='Full-text access to Milburn1991 or Kay-Wald1991; these access limits remain explicit',
        no_physical_partition_selected=True, no_current_template_changed=True)
    data = (json.dumps(record, indent=2, ensure_ascii=False)+'\n').encode()
    temporary = TARGET/'PROVENANCE.json.part'
    temporary.write_bytes(data)
    if temporary.stat().st_size != len(data):
        raise ValueError('Short provenance write')
    temporary.replace(TARGET/'PROVENANCE.json')
    print(json.dumps(record, ensure_ascii=False))


if __name__ == '__main__':
    main()
