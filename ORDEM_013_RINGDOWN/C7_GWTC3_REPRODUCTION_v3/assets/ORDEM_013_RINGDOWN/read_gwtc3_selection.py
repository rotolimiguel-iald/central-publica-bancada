"""Recover the paper's Table 13 and explicit joint-analysis exclusions."""
from pathlib import Path
import hashlib
import html
import json
import re
from fetch_public import atomic_json

ROOT=Path(__file__).resolve().parent


def plain(text):
    return re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]+>',' ',text))).strip()


def main():
    out=ROOT/'C4_GWTC3_SELECTION.json'
    if out.exists():
        raise FileExistsError('Preserve inspected selection')
    receipt=json.loads((ROOT/'C4_GWTC3_PAPER_RECEIPT.json').read_bytes())
    path=ROOT/receipt['path']
    raw=path.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=receipt['sha256']:
        raise ValueError('Paper changed')
    text=raw.decode('utf-8')
    figure=re.search(r'<figure id="S8.T13".*?</figure>',text,re.S)
    if figure is None:
        raise ValueError('Published Table 13 missing')
    names=re.findall(r'GW\d{6}(?:[_ ]\d{6})?',plain(figure[0]))
    catalog=json.loads((ROOT/'C4_GWTC3_220.json').read_bytes())['rows']
    full_names=[r['event'] for r in catalog]
    mapped=[]
    for name in names:
        normalized=name.replace(' ','_')
        candidates=[n for n in full_names if n==normalized or ('_' not in normalized and n.startswith(normalized+'_'))]
        if len(candidates)!=1:
            raise ValueError('Ambiguous event identity in source table: '+name)
        mapped.append(candidates[0])
    if len(set(mapped))!=len(mapped) or len(mapped)!=12:
        raise ValueError('Unexpected table extraction')
    paragraphs=[(m[0],plain(m[0])) for m in re.finditer(r'<p\b[^>]*>.*?</p>',text,re.S)]
    exclusions=[p for raw_p,p in paragraphs if 'do not include them in the computation of the joint bounds' in p]
    if len(exclusions)!=1:
        raise ValueError('Explicit source exclusion not unique')
    first_sentence=exclusions[0].split('joint bounds')[0]
    excluded=list(dict.fromkeys(re.findall(r'GW\d{6}_\d{6}',first_sentence)))
    if len(excluded)!=2 or not set(excluded)<=set(mapped):
        raise ValueError('Invalid source exclusion extraction')
    selected=[n for n in mapped if n not in excluded]
    atomic_json(out,dict(status='PRIMARY_PAPER_SELECTION_READ',source=receipt['url']+'#S8.SS1.SSS2',
        source_path=receipt['path'],source_sha256=receipt['sha256'],table_id='S8.T13',
        table_events=mapped,excluded_by_authors=excluded,selected_events=selected,
        archive_products_outside_table=sorted(set(full_names)-set(mapped)),
        basis='Table 13 and explicit exclusion paragraph in Sec VIII.1.2, not selected by our likelihood results',
        interpretation='All 18 archive products remain an auxiliary control. The published-event selection has 10 entries after two author exclusions; no current-catalog likelihood is multiplied into it.',
        reading_scope='Sec VIII.1.2, Table 13 and Appendix A.3 inspected; not a full-article reading',
        no_article_parameter_values_used_as_samples=True))
    print(json.dumps(dict(table=len(mapped),excluded=excluded,selected=selected,outside_table=len(full_names)-len(mapped))))


if __name__=='__main__':
    main()
