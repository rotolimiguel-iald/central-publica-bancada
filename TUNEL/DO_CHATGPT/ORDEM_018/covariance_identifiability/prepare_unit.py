"""Prepare one bounded skeptical review; synthetic checks only, no provider call."""
import hashlib
import json
import math
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parent
CENTRAL=next(p for p in ROOT.parents if p.name=='Central de Patentes')
STACK=CENTRAL/'Chatgpt/IALD_ORQUESTRACAO_20260923'
ORDER=CENTRAL/'Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_018_o_discriminante.md'
CRITIC=Path(r'C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\fase9_hubble\critico\CRITICA_FASE9.md')

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def save(p,obj):
    data=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():
        if p.read_bytes()==data:return
        raise RuntimeError('Existing artifact preserved: '+str(p))
    temp=p.with_name(p.name+'.tmp')
    with temp.open('xb') as f:f.write(data)
    assert temp.stat().st_size==len(data)
    temp.replace(p)

def rank(matrix):
    a=[row[:] for row in matrix]; n=len(a);m=len(a[0]);r=0
    for j in range(m):
        k=max(range(r,n),key=lambda i:abs(a[i][j]),default=r)
        if r==n or abs(a[k][j])<1e-12:continue
        a[r],a[k]=a[k],a[r]
        v=a[r][j];a[r]=[x/v for x in a[r]]
        for i in range(n):
            if i!=r:
                v=a[i][j];a[i]=[x-v*y for x,y in zip(a[i],a[r])]
        r+=1
    return r

def prepare():
    started=time.perf_counter()
    alpha=7.2973525693e-3
    beta=alpha*math.sqrt(math.e)
    # Arbitrary dimensionless synthetic nuisance/background; not cosmological data.
    b=1.7;kappa=.8;K=math.exp(kappa*beta);shift=b*(K-1)
    mu_beta=[b*K]*4;mu_shift=[b+shift]*4
    err=max(abs(x-y) for x,y in zip(mu_beta,mu_shift))
    local=[[K,b*kappa*K] for _ in range(4)]
    joint=[[1.,0.]]+local
    selective=[[1.,float(i<2)] for i in range(4)]
    ranks={'universal_local':rank(local),'with_background':rank(joint),'selective_local':rank(selective)}
    assert err<1e-14 and ranks=={'universal_local':1,'with_background':2,'selective_local':2}
    stat=2.; common=3.; n=4
    C=[[stat**2*float(i==j)+common**2 for j in range(n)] for i in range(n)]
    meanvar=sum(map(sum,C))/n**2
    differencevar=C[0][0]+C[2][2]-2*C[0][2]
    assert abs(meanvar-(stat**2/n+common**2))<1e-13
    assert abs(differencevar-2*stat**2)<1e-13
    # Synthetic joint covariance for (background, one local reader).
    cbb,chh,chb=.25,1.,.1
    direct=K*K*cbb+chh-2*K*chb
    T=(-K,1.)
    joint_cov=((cbb,chb),(chb,chh))
    transformed=sum(T[i]*joint_cov[i][j]*T[j] for i in range(2) for j in range(2))
    assert abs(direct-transformed)<1e-14
    eps=1e-6
    numerical=b*(math.exp(kappa*(beta+eps))-math.exp(kappa*(beta-eps)))/(2*eps)
    analytic=b*kappa*math.exp(kappa*beta)
    assert abs(numerical-analytic)<1e-9
    save(ROOT/'SYNTHETIC_CHECKS.json',{'status':'PASS_SYNTHETIC_ONLY','observational_centers_used':False,
         'beta_runtime_expression':'ALPHA_FINE_CODATA_2018*sqrt(e)','beta':beta,
         'synthetic_b':b,'synthetic_kappa':kappa,'universal_reparametrization_max_error':err,
         'ranks':ranks,'shared_variance_counted_once_diagonal':C[0][0],
         'double_counted_diagonal_counterexample':C[0][0]+common**2,
         'common_mean_variance':meanvar,'inter_method_difference_variance':differencevar,
         'covariance_eigenvalues':[stat**2]*(n-1)+[stat**2+n*common**2],
         'synthetic_covariance_condition_number':(stat**2+n*common**2)/stat**2,
         'residual_variance_transform_error':abs(direct-transformed),
         'prior_jacobian_absolute_error':abs(numerical-analytic),
         'elapsed_seconds':time.perf_counter()-started})
    route=json.loads((ROOT/'MAPA_SEQ373.json').read_text(encoding='utf-8'))
    if 'content' in route:
        route=json.loads(next(c['text'] for c in route['content'] if c['type']=='text'))
    ref=next(a for a in route['rota']['artefatos'] if a['caminho']==str(CRITIC))
    assert digest(CRITIC)==ref['sha256']
    sources=[ORDER,CRITIC,ROOT/'REVISAO_LOCAL.md',ROOT/'MAPA_SEQ373.json',Path(__file__).resolve()]
    manifest={'status':'SOURCE_BYTES_VERIFIED_NOT_NEW_OBSERVATIONAL_VERDICT','route_seq':373,
              'files':[{'path':str(p),'bytes':p.stat().st_size,'sha256':digest(p)} for p in sources]}
    save(ROOT/'FONTES.json',manifest)
    refs='\n'.join(f"- {Path(r['path']).name}: SHA256 {r['sha256']}" for r in manifest['files'])
    prompt='''ORDEM018 do TUNEL de 05/10/2026, R-A Hubble. Unidade NOVA, fechada: revisão adversarial da identificabilidade e da covariância das cinco hipóteses. Não é retentativa de unidade anterior. Papel MiMo: cético matemático, sem ferramentas, sem ler ou estimar novos centros observacionais, sem veredito nem despacho. O worker fornece a mesma memória científica canônica parcial e rastreável. Fontes abaixo são extratos/metadados e uma nota local; não alegue leitura integral dos originais ou execução. Mantenha DECLARADO para seu parecer. A lei da casa admite retrodição sem ajuste/novidade de uso; data anterior do dado não é demérito. O V1 do teste ainda precisa ser unificado e congelado pela gerência. Não inventar nova física nem alterar beta_TGL.

Antecedente que NÃO deve ser refeito: mapa hubble.fase9_razao_discriminante seq373 e CRITICA_FASE9.md §§1c/1d/3 já registram (i) deslocamento universal degenera com beta livre; (ii) duas especificações: shift universal versus só Cefeidas; fundo multiplicativo versus rd livre; (iii) risco de repetir componente SN no erro total; (iv) covariâncias cruzadas precisam de fonte. Esses são registros históricos, não resultados novos desta unidade. Sua tarefa é criticar a formalização abaixo, procurando contraexemplos e condições omitidas.

ENTREGA PEDIDA: (1) o que está correto sob quais hipóteses; (2) erros e fórmula corrigida; (3) estatísticas mínimas que distinguem efeito universal versus Cefeidas com compartilhamento de âncoras/fluxo; (4) contrato mínimo do quinto modelo rd livre usando BAO, sem fingir EDE completa; (5) checklist curto para V1. Não repetir cronologia ou números de significância históricos. Priors de rivais podem ser especificados para diagnóstico; beta_TGL fixo nunca é ajustado ou prior da teoria. Não converter lnB, Fisher, diferença de vetores ou posto em sigma. Não escrever protocolo de 5sigma apoiado só em 10 mil nulos. Nenhum pedido de chamada adicional.

FONTES E CUSTODIA (hash lido dos bytes):
'''+refs+'\n\nNOTA LOCAL A CRITICAR INTEGRALMENTE:\n'+(ROOT/'REVISAO_LOCAL.md').read_text(encoding='utf-8')
    assert len(prompt)<24000
    request_id=str(uuid.uuid4())
    constraints={'mission_id':'TGL_BANCADA_OFICIAL','branch_id':'TUNEL_018_RA_COV_HYP_20261005',
                 'lemma_id':'five_hypotheses_covariance_contract_v1','role':'skeptic','required_provider':'mimo',
                 'max_calls':1,'max_cost_usd':None,'max_output_tokens':131072,'max_projection_chars':None}
    request={'operation':'submit','request_id':request_id,'prompt':prompt,'execution_constraints':constraints}
    save(ROOT/'UNIT_MIMO.json',request)
    save(STACK/'state/session_requests'/f'{request_id}.json',{
         'request_id':request_id,'job_id':None,'status':'PREPARED_NOT_SUBMITTED','created_utc':datetime.now(timezone.utc).isoformat(),
         'origin_thread_id':'01a070fc-9484-7e13-a654-c6b5f61093a4','coordinator_thread_id':'01a0ce2b-8c2f-71b0-a9a8-91b17715a569',
         'origin_house':str(CENTRAL),'unit_path':str(ROOT/'UNIT_MIMO.json'),'unit_sha256':digest(ROOT/'UNIT_MIMO.json'),
         'mission_description':'ORDEM_018_TUNEL_05OUT_NEW_COVARIANCE_REVIEW','execution_constraints':constraints})
    print(json.dumps({'status':'PREPARED','request_id':request_id,'prompt_chars':len(prompt),'synthetic_checks':'PASS'}))

def preview():
    req=json.loads((ROOT/'UNIT_MIMO.json').read_text(encoding='utf-8'))
    query={**req,'operation':'preview_execution'}
    started=time.perf_counter()
    r=subprocess.run([sys.executable,'-X','utf8',str(STACK/'transport_cli.py')],input=json.dumps(query,ensure_ascii=False),
                     capture_output=True,text=True,encoding='utf-8',cwd=str(STACK),timeout=180)
    if r.returncode:
        save(ROOT/'PREVIEW_REFUSAL.json',{'returncode':r.returncode,'stderr':r.stderr,'elapsed_seconds':time.perf_counter()-started})
        print('PREVIEW_REFUSED');return
    data=json.loads(r.stdout)
    save(ROOT/'PREVIEW_MIMO.json',data)
    save(ROOT/'PREVIEW_RECEIPT.json',{'status':'PREVIEW_ONLY_NO_PROVIDER_CALL','request_id':req['request_id'],
         'selected':data.get('selected'),'elapsed_seconds':time.perf_counter()-started,
         'memory_generation':data.get('canonical_memory',{}).get('generation'),
         'memory_mode':data.get('canonical_memory',{}).get('memory_mode'),
         'unit_sha256':digest(ROOT/'UNIT_MIMO.json'),'preview_sha256':digest(ROOT/'PREVIEW_MIMO.json')})
    print(json.dumps({'selected':data.get('selected'),'request_id':req['request_id'],
                      'memory_generation':data.get('canonical_memory',{}).get('generation')}))

if __name__=='__main__':
    prepare() if sys.argv[1]=='prepare' else preview()
