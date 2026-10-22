"""Prepare bounded projections of units refused before submission; no remote calls."""
from pathlib import Path
import ast, hashlib, json, uuid
from datetime import datetime, timezone

R=Path(__file__).resolve().parent
D=R/'orchestration_final_stage'
B=R.parent/'ORDEM_013_RINGDOWN'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):
    raw=(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
    temp=p.with_suffix(p.suffix+'.pending')
    with temp.open('xb') as f: f.write(raw)
    assert temp.read_bytes()==raw
    if p.exists(): raise FileExistsError(p)
    temp.rename(p)
def excerpt(p,a,b):
    lines=p.read_text('utf-8-sig').splitlines()
    ref={'path':str(p),'sha256':sha(p),'first_line':a,'last_line':min(b,len(lines))}
    return '\nSOURCE '+json.dumps(ref,ensure_ascii=False)+'\n'+'\n'.join(f'{i+1}: {lines[i]}' for i in range(a-1,min(b,len(lines)))),ref
order=R.parent/'TUNEL/PARA_CHATGPT/ORDEM_015_continuacao_do_ringdown_rumo_ao_5sigma.md'
catalog=[]
for provider in ('mimo','deepseek','gemini'):
    old=D/('antigravity_v2_submit.json' if provider=='gemini' else provider+'_submit.json')
    payload=json.loads(old.read_bytes())
    refs=[]
    if provider=='gemini':
        prompt=payload['prompt']
        refs=json.loads((D/'prepared_units_v2.json').read_bytes())[-1]['sources']
    else:
        prompt=payload['prompt'].split('\nSOURCE ',1)[0]
        prompt+='\nProjeção revisada após recusa LOCAL, sem execução anterior. Escopo delimitado aos excertos abaixo. Não supor acesso ao restante dos arquivos. Não inventar campos ou resultados.\n'
        if provider=='mimo':
            prompt+='\nEm vez de reproduzir o gerador, implementar pós-processador documental do JSON já existente. Estrutura real representativa abaixo; preservar todas as células e métricas, percorrendo-as genericamente.\n'
            ranges=[(order,208,218),(B/'bis/e6_prepare_v3/generate_reach_table.py',125,174),(B/'bis/e6_prepare_v3/generate_reach_table.py',466,497)]
            p=B/'bis/e6_prepare_v3/runs/wall_actual_001/QUADRO_DE_ALCANCE_V1.json'
            obj=json.loads(p.read_bytes())
            samples=[]
            for group in ('O4_HOJE','O4_CEGO'):
                c=next(c for c in obj['cells'] if c['data_group']==group)
                sample={k:c[k] for k in ('route','reading','data_group')}
                sample['rate_contexts']=c.get('rate_contexts',[])[:1]
                scenario=c['scenarios'][0]
                sample['scenario_keys']=list(scenario)
                sample['metric_examples']=list(scenario.get('metrics',{}).items())[:2]
                samples.append(sample)
            prompt+='\nEXTRACAO JSON (somente duas células, primeiro cenário de cada): '+json.dumps({'path':str(p),'sha256':sha(p),'top_keys':list(obj),'cells':samples},ensure_ascii=False,separators=(',',':'))
            refs.append({'path':str(p),'sha256':sha(p),'projection':'two representative cells, first scenario only'})
        else:
            prompt+='\nDelimitação desta entrega: núcleo puro de validação da cadeia e subobjeto congelado + testes negativos; adaptador da API legado pode ser descrito como plano de integração, NÃO declarar guarda completa/ativada. Acrescentar validação das testemunhas e da cronologia; dependências R5/R7 continuam explícitas.\n'
            ranges=[(order,239,243),(order,250,255),(B/'bis/e2_code/registration_guard.py',112,168)]
            p=B/'bis/e2_code/registration_guard.py'
            tree=ast.parse(p.read_text('utf-8-sig'))
            api=[f'{n.lineno}: def {n.name}({ast.unparse(n.args)})' for n in tree.body if isinstance(n,ast.FunctionDef)]
            prompt+='\nAPI LEGADA (assinaturas apenas): '+json.dumps({'path':str(p),'sha256':sha(p),'signatures':api},ensure_ascii=False)
        for p,a,b in ranges:
            txt,ref=excerpt(p,a,b);prompt+=txt;refs.append(ref)
    assert len(prompt)<=24000,(provider,len(prompt))
    predecessor=payload['request_id']
    payload.update(request_id=str(uuid.uuid4()),prompt=prompt)
    payload['execution_constraints']['required_provider']=provider
    path=D/(provider+'_bounded_submit.json')
    save(path,payload)
    catalog.append({'provider':provider,'request_id':payload['request_id'],'predecessor_not_submitted':predecessor,'branch':payload['execution_constraints']['branch_id'],'payload':str(path),'payload_sha256':sha(path),'prompt_sha256':hashlib.sha256(prompt.encode()).hexdigest(),'chars':len(prompt),'sources':refs,'status':'PREPARED_NOT_SUBMITTED'})
save(D/'prepared_units_v3.json',catalog)
save(D/'REVISION_v3.json',{'at':datetime.now(timezone.utc).isoformat(),'reason':'Queue input ceiling and technical provider ID; predecessors were refused before job creation','kimi_terminal_no_retry':True,'scientific_originals_changed':False})
print(json.dumps([{k:v for k,v in u.items() if k!='sources'} for u in catalog],indent=2))
