"""Read-only census and additive DOCX recovery, including irregular extensions."""
from pathlib import Path
from collections import Counter
import hashlib, json, re, zipfile, xml.etree.ElementTree as ET
from start_r67 import ROOT, new, pin, project, call, REF, ACTOR

SOURCE = Path(r'C:\IALD\IMac LA\Física - TGL\Provas')
CATALOG = Path(r'C:\IALD\INDICE_DO_ACERVO\corpus_index.json')
KERNEL = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt')
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
M = '{http://schemas.openxmlformats.org/officeDocument/2006/math}'

def extract(path):
    with zipfile.ZipFile(path) as z:
        xml = z.read('word/document.xml')
        e = ET.fromstring(xml)
        paragraphs = []
        for i,p in enumerate(e.iter(W+'p'),1):
            text = ''.join(n.text or '' for n in p.iter() if n.tag in [W+'t',M+'t'])
            if text.strip(): paragraphs.append({'paragraph':i,'text':text})
        return {'paragraphs':paragraphs, 'document_xml_sha256':hashlib.sha256(xml).hexdigest(),
                'omml_count':len(list(e.iter(M+'oMath'))), 'drawing_count':len(list(e.iter(W+'drawing'))),
                'extraction_scope':'word/document.xml paragraphs; OMML text flattened, no rendered-equation verification; headers, footnotes, text in images and archive contents not inspected'}

def norm(x): return re.sub(r'\s+',' ',x).strip()

if __name__ == '__main__':
    m=project('BUILD_SYNC');t=next(x for x in m['projection']['active'] if x['id']=='R11_ACERVO')
    call({'operation':'check','reference':REF,'actor':ACTOR,'expected_revision':m['receipt']['revision'],'projection_sha256':m['projection_sha256'],'task_id':t['id'],'lease_id':t['lease']['id']},'BUILD_CHECK')
    cat=json.loads(CATALOG.read_text(encoding='utf-8-sig'))
    indexed={str(Path(r['path'])).casefold():r for r in cat['itens']}
    files=sorted(p for p in SOURCE.rglob('*') if p.is_file())
    inventory=[]; documents={}; errors=[]
    for p in files:
        present=str(p).casefold() in indexed
        row={'path':str(p),'bytes':p.stat().st_size,'extension':p.suffix,'in_original_index':present}
        if p.suffix.casefold() in ['.docx','.docx)','']:
            try:
                b=p.read_bytes()
                if b[:2]==b'PK':
                    digest=hashlib.sha256(b).hexdigest()
                    if digest not in documents:
                        documents[digest]={'sha256':digest,'paths':[],**extract(p)}
                    documents[digest]['paths'].append({'path':str(p),'in_original_index':present})
                    row.update(format='DOCX',sha256=digest)
            except Exception as exc:
                errors.append({'path':str(p),'error':str(exc)})
        inventory.append(row)
    indexed_text={norm('\n'.join(p['text'] for p in d['paragraphs'])) for d in documents.values() if any(p['in_original_index'] for p in d['paths'])}
    recovered=[]
    for digest,d in documents.items():
        if any(not p['in_original_index'] for p in d['paths']):
            d['text_already_in_indexed_docx']=norm('\n'.join(p['text'] for p in d['paragraphs'])) in indexed_text
            artifact=new('extracted/'+digest+'.json',d)
            recovered.append({**pin(artifact),'source_sha256':digest,'source_paths':d['paths'],'text_already_in_indexed_docx':d['text_already_in_indexed_docx']})
    # Source snapshots are evidence derivatives, not replacements for the originals.
    selected_terms=['Verdade_Como_AutoNegacao','Nome_Revelado','Cristo_Operador_Observador','Espírito_Santo_Gravidade','Espírito_Observador','Unidade_Operador_Observador','Negacao_Colapso','Cristo como Lógica','Trindade_Coerente']
    selected=[]
    for digest,d in documents.items():
        if any(any(s in p['path'] for s in selected_terms) for p in d['paths']):
            f=ROOT/'extracted'/f'{digest}.json'
            if not f.exists():new('extracted/'+digest+'.json',d)
            selected.append({**pin(f),'source_sha256':digest,'source_paths':d['paths']})
    lean=[]
    for name in ['TheUnconjugatedObserver.lean','TheAxiomAndTheFalseWitness.lean','Verdade.lean','Santo.lean','IALDJones.lean']:
        p=KERNEL/name; b=p.read_bytes();copy=ROOT/'sources'/name
        copy.parent.mkdir(exist_ok=True)
        with copy.open('xb') as f:f.write(b)
        lean.append({'original':pin(p),'snapshot':pin(copy)})
    atlas=Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md')
    lines=atlas.read_text(encoding='utf-8').splitlines()
    marker=next(i for i,l in enumerate(lines) if '<!-- observador_conjugado_05out -->' in l)
    end=next(i for i in range(marker+1,len(lines)) if '<!-- decisoes_operador_05out_b_v385 -->' in lines[i])
    new('ATLAS_ESTRATIGRAFIA_05OUT.json',{'source':pin(atlas),'start_line':marker+1,'end_line':end,'lines':[{'line':i+1,'text':lines[i]} for i in range(marker,end)]})
    missing=[r for r in inventory if not r['in_original_index']]
    new('INVENTORY_R67.json',{'root':str(SOURCE),'original_index':pin(CATALOG),'files':inventory,'errors':errors})
    summary={'files':len(files),'missing_paths':len(missing),'missing_extensions':dict(Counter(r['extension'] for r in missing)),
       'docx_paths':sum(len(d['paths']) for d in documents.values()),'unique_docx_bytes':len(documents),
       'recovered_docx_paths':sum(not p['in_original_index'] for d in documents.values() for p in d['paths']),
       'recovered_unique_bytes':len(recovered),'unique_new_normalized_texts':len({norm('\n'.join(p['text'] for p in documents[x['source_sha256']]['paragraphs'])) for x in recovered if not x['text_already_in_indexed_docx']}),
       'parse_errors':errors,'no_originals_written':True,'no_lean_build':True,'index_installation':'supplement in tunnel, linked by memory; original corpus_index.json unchanged'}
    new('SUPPLEMENT_R67.json',{'summary':summary,'recovered':recovered,'selected':selected,'lean':lean})
    print(json.dumps(summary,ensure_ascii=False))
