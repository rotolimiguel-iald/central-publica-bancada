from pathlib import Path
import datetime,json,hashlib
from audit_provenance import OUT,atomic
names=['v22_docx','eletro_janeiro','cruz_janeiro','errata_exata','lei_maio18','lei_h0_primitiva','main_predict','memoria_evento2','d1b_setembro']
anchors=['OOXML; paragrafos 80-81,108-118,130-134,584-599','OOXML; paragrafos 173-178,219,330-350,853-856,869-871','OOXML; igualdade normalizada com CRUZ_original.py','linhas 66-70,159-169,342,450-458','linhas 126-137,312-327','linha 3354 e seguintes','linhas 198-202,3617-3682','memoria integral; inventario_evento2.json','linhas 2-7,693']
items=[]
for i,(name,anchor) in enumerate(zip(names,anchors),1):
    record=json.loads((OUT/(name+'.json')).read_text(encoding='utf-8'))
    items.append({'id':'P'+str(i).zfill(2),'evidence_file':name+'.json','source':record['source'],'anchor':anchor})
atomic(OUT/'CRONOLOGIA_F1.json',json.dumps({'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Proveniencia documental; sem fit, execucao cientifica ou veredito','items':items,'dates_note':'mtime e datas OOXML sao metadados locais; nao timestamp imutavel de publicacao'},ensure_ascii=False,indent=2)+'\n')
note=OUT/'NOTA_PROVENIENCIA_F1.md'
text=note.read_text(encoding='utf-8')
section='\n\n## Fontes primarias e hashes lidos dos bytes\n\n| ID | Caminho real | SHA-256 |\n|---|---|---|\n'
for item in items:
    s=item['source']
    section+='| '+item['id']+' | '+s['path']+' | '+s['sha256']+' |\n'
section+='\nFontes auxiliares CRUZ original/alpha-free e duas fontes de novembro constam do manifesto. Esta tabela ancora os IDs usados acima. O inventario de nomes em ORDEM_018_INSUMOS nao mostrou um artefato FASE9; nao se estendeu a busca por essa fase nesta subtarefa.\n'
atomic(note,text+section)
artifacts=[]
for name in ['NOTA_PROVENIENCIA_F1.md','CRONOLOGIA_F1.json','MANIFESTO_FONTES_F1.json','VERIFICACOES_ESTATICAS_F1.json','inventario_evento2.json']:
    p=OUT/name
    b=p.read_bytes()
    artifacts.append({'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
atomic(OUT/'RECIBO_PROVENIENCIA_F1.json',json.dumps({'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'DOCUMENTARY_EXAMINATION_COMPLETED_WITH_OPEN_GAPS','artifacts':artifacts,'external_calls':0,'scientific_programs_executed':0,'originals_modified':False},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'artifacts':artifacts,'source_count':len(json.loads((OUT/'MANIFESTO_FONTES_F1.json').read_text(encoding='utf-8'))['sources'])},ensure_ascii=False,indent=2))
