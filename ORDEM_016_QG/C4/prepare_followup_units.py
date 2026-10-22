"""Three bounded questions after new measured evidence; coordinator owns submission."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import json,sys,uuid,hashlib,subprocess
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'C4';Q=D/'orchestration'
sys.path.insert(0,str(ROOT/'A7'))
from deliver_nonminimal_wick_and_mimo_audit import OUT,BASE,sha,write,put,append
Q.mkdir(exist_ok=False)
receipt=json.loads((D/'screen_01.json').read_bytes())
put(D/'START.json',dict(at=receipt['utc'],ceiling_hours=16,first_receipt=str(D/'screen_01.json'),
    aim='Explicit transverse frame and physical cocycle; preserve scalar principal and paired helicity distinction',
    source_search='Canonical helicity/rotation hits are different constructions; no actual Wigner phase found in inspected TGLExt/A3 sources'))
common='''ORDEM016, ParteC e críticas do ADENDO002. Nova unidade delimitada sob ordem direta de ocupar vagas úteis; não repetir unidades terminais. Texto somente, sem executar ferramentas, compilar ou alterar gate. Memória científica comum pelo transporte. Nenhum original/confidencial/acervo jurídico. Saída DECLARADO até auditoria local; enunciados e hipóteses explícitos. Uma pergunta, sem Fock nem escolha de partição física. Corpos Lean existentes não devem ser rederivados.\n'''
units=[
 ('mimo','C4','screen_quotient_cocycle_composition','draft',
 '''Pergunta: com os vetores de tela concretos abaixo, qual é o menor lema algébrico que faz a matriz C_ij(g,p)=-<e_i(gp),g e_j(p)> satisfazer C(g h,p)=C(g,hp)C(h,p) e ser SO(2), sem supor a conclusão? A bancada acabou de construir e conferir e1=(sinh xi,cosh xi,0,0),e2=(0,0,-q1/r,q0/r), p=(r cosh xi,r sinh xi,q0,q1),r=sqrt(q0²+q1²),q!=0; boost transporta e1/e2 exatamente. Defina n=(cosh xi,sinh xi,-q0/r,-q1/r)/(2r), com <p,n>=1. Forneça expansão exata de v em p,n,e1,e2 e calcule resto longitudinal de g e_j que cancela na composição. Separe (i) ortogonalidade, (ii) determinante +1 pela orientação espaço-temporal/futura, (iii) mensurabilidade nos conjuntos onde ambas cartas existem. Explique que dados são ainda necessários para obter representação de helicidades +/-1 no Lorentz inteiro; não chamar apenas o shift e duas fases de representação física. Não repetir a seção antiga L=Rx(phi)Bx(xi) que só mapeava k0 a p/r; esta pergunta deriva da nova tela concreta e pede expansão/composição. Entregue álgebra verificável e, se útil, pequeno esqueleto Lean SEM sorry/axiom, sem inventar APIs.''',
 [(D/'NullScreenFrame_v2.lean',None),(ROOT/'A3/OrbitalBoostCovariance_v2.lean',(14,37)),(ROOT/'A3/IsometricCocycleSpectrum_v2.lean',None)]),
 ('kimi','C4','ae_cocycle_diagonal_strictness','skeptic',
 '''Pergunta única: a prova antiga de cobordo, que de ∀s,t a lei de cociclo vale a.e. em(q,xi) substitui t=xi-s e define b(q,xi)=C_xi(q,xi), é válida sem versão estrita comum? Dê contraexemplo mensurável ou justificação rigorosa e o menor enunciado de strictificação necessário. Pista a atacar, não tomar como premissa: modificar C_s(xi)=1 só na diagonal xi=s mantém, para cada s,t fixo, a lei fora de conjunto finito, mas muda arbitrariamente b(xi)=C_xi(xi). Teste C_s(xi)=exp(i*xi²) se xi=s,1 caso contrário. Distinga cociclo pontual de cociclo a.e., mensurabilidade conjunta e escolha de representante, e versão inteira. Não repetir a falsa alegação da críticaC23 de fase1 em qualquer trivialização: C'_s=exp(i[chi(xi)-chi(xi-s)]) já a refuta. A nova tela compilada é uma escolha específica. Este pedido é sobre a legalidade da substituição diagonal, não nova execução da pergunta1265dfaf nem de C2.2. Não concluir impossibilidade de helicidade ou H2 a partir desta lacuna de versão.''',
 [(ROOT/'A5/63b4e640-2b1a-4f7e-8213-76b2eb94d3e5_received_response.json','old_response'),(D/'NullScreenFrame_v2.lean',None),(ROOT/'ADENDO_002_CRITICAS/C23_AUDIT/CONFRONTO.md',None)]),
 ('deepseek','C2.4-followup','vector_kms_standard_representation_counterexample','skeptic',
 '''Pergunta única: o lema L2 da críticaC24, "estado vetorial KMS com vetor cíclico-separante implica dinâmica trivial", é refutado no tipo exato das bordas do contrato pela representação padrão Hilbert-Schmidt de M2? Construa ou refute explicitamente rho=diag(1/3,2/3),Omega=sqrt(rho),M=ação à esquerda,alpha_t(X)=rho^(-it) X rho^(it). Verifique normOmega1, ciclicidade/separação, alpha_tOmega=Omega, grupo não trivial, e F_AB(z)=sum_ij rho_i*A_ij*B_ji*exp(i*z*(log rho_i-log rho_j)). Compare F(t) e F(t+i) com as duas bordas KMSAt fornecidas, não com convenção presumida. Prove holomorfia/limitação na faixa fechada e identifique sinais dos dois autovalores do gerador. Distinguir estado vetorial sobre M de estado puro sobre B(HS); vetor não implica pureza sobre M. Não fabricar W AQFT nem anunciar prova de KMS regional do cone. A unidade audita um argumento falso potencial que bloquearia C5; não é execução de C5 ou retry de DeepSeek antigo cancelado. Entregue conta exata em componentes e hipóteses; pode sugerir núcleo Lean reutilizando ModularGeneratorControl sem repetir seu teorema do comutador.''',
 [(ROOT/'A1/minimal_imports/ContratoQG_v31_Minimal.lean',(130,170)),(ROOT/'ADENDO_002_CRITICAS/C24_RECEIVED/KIMI_ORIGINAL.md',(50,110)),(ROOT/'A6_EQUACAO_DA_VERDADE/B_fechamentos/ModularGeneratorControl.lean',None)])]
catalog=[];events=[]
for provider,branch,lemma,role,question,sources in units:
    rid=str(uuid.uuid4());prompt=common+'\n'+question+'\n';refs=[]
    for path,span in sources:
        raw=path.read_bytes();lines=raw.decode('utf-8-sig').splitlines()
        if span=='old_response':
            text=json.loads(raw)['result']['text'];all_lines=text.splitlines();start=next(i for i,l in enumerate(all_lines) if l.startswith('## 5.'));end=next(i for i,l in enumerate(all_lines) if l.startswith('## 6.'))
            selected=list(range(start,end));lines=all_lines;description='result.text lines'
        else:
            selected=list(range((span[0]-1) if span else 0,min(span[1],len(lines)) if span else len(lines)));description='source lines'
        ref=dict(path=str(path),sha256=sha(path),line_kind=description,included_lines=[i+1 for i in selected]);refs.append(ref)
        prompt+='\nSOURCE '+json.dumps(ref,ensure_ascii=False)+'\n'+'\n'.join(f'{i+1}: {lines[i]}' for i in selected)+'\n'
    assert len(prompt)<=20000,(provider,len(prompt))
    constraints=dict(mission_id='ORDEM_016',branch_id=branch,lemma_id=lemma,role=role,required_provider=provider,max_calls=1)
    if provider in ['mimo','deepseek']:
        constraints.update(max_cost_usd=None,max_output_tokens=131072 if provider=='mimo' else 393216)
    payload=Q/(provider+'_submit.json');put(payload,dict(operation='submit',request_id=rid,prompt=prompt,execution_constraints=constraints))
    origin=Q/(rid+'_origin.json');put(origin,dict(at=datetime.now(timezone.utc).isoformat(),thread_id='01a070fc-9484-7e13-a654-c6b5f61093a4',request_id=rid,
        house='Central de Patentes',payload=str(payload),payload_sha256=sha(payload),sources=refs,status='PREPARED_NOT_SUBMITTED'))
    call=subprocess.run([sys.executable,'-X','utf8','-B',str(BASE/'transport_cli.py')],input=json.dumps(dict(operation='preview_execution',prompt=prompt,execution_constraints=constraints)),text=True,encoding='utf-8',capture_output=True,cwd=BASE)
    resp=json.loads(call.stdout);put(Q/(rid+'_preview.json'),dict(returncode=call.returncode,response=resp))
    assert call.returncode==0 and resp.get('selected')==provider,(provider,resp)
    row=dict(provider=provider,branch=branch,request_id=rid,lemma=lemma,payload=str(payload),payload_sha256=sha(payload),prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(),prompt_chars=len(prompt),sources=refs,
        preview=str(Q/(rid+'_preview.json')),status='PREPARED_NOT_SUBMITTED_COORDINATOR_OWNS_TRANSITIONS')
    catalog.append(row);events.append(dict(at=datetime.now(timezone.utc).isoformat(),event='C4_DISTINCT_UNITS_PREPARED',remote_call=False,**{k:row[k] for k in ['provider','branch','request_id','payload','payload_sha256','prompt_sha256','status']}))
put(Q/'prepared_units.json',catalog)
append(OUT/'LEDGER_016.jsonl',''.join(json.dumps(e)+'\n' for e in events))
print(json.dumps([dict(provider=x['provider'],request_id=x['request_id'],chars=x['prompt_chars']) for x in catalog]))
