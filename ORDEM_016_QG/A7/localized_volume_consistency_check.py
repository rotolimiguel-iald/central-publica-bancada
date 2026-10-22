"""Keep the cutoff source in the volume primitive's inhomogeneous BV identity."""
from pathlib import Path
from datetime import datetime,timezone
from itertools import combinations_with_replacement
import ast,json,time
import sympy as s
from deliver_nonminimal_wick_and_mimo_audit import H,OUT,sha,write,put,append
D=H/'localized_volume_consistency'

def main():
    D.mkdir(exist_ok=False);now=datetime.now(timezone.utc)
    src=H/'antifield_quadratic_primitive_check.py'
    sources=[Path(__file__),src,H/'volume_primitive_second_order/results.json',
             H/'linear_slot_ward_bridge/results.json']
    put(D/'PRE_REGISTER.json',dict(at=now.isoformat(),
        target='Polarized cutoff source of the measured A1 volume primitive, identified with (I1,B1)',
        scope='Order u hbar consistency source, not a numerical A2(Vchi,Veta)',
        hypotheses=['q0 h=Kg c, q1_chi h=chi Lie_c h, q1_chi c=chi c.d c',
                    'alpha_W is constant, test cutoffs chi and eta are independent'],
        sources=[dict(path=str(p),sha256=sha(p)) for p in sources],
        negative_control='Discarding derivatives of the cutoffs must fail'))
    start=time.process_time();names={'clean','add','scale','mul','atom'}
    nodes=[n for n in ast.parse(src.read_text('utf-8')).body if isinstance(n,ast.FunctionDef) and n.name in names]
    ns={'s':s};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(src),'exec'),ns)
    clean,add,scale,mul,atom=[ns[n] for n in ['clean','add','scale','mul','atom']]
    alpha,chi,eta=s.symbols('alpha_W chi eta');l=s.symbols('dchi0:4');e=s.symbols('deta0:4')
    lab=[('c',i) for i in range(4)]+[('dc',i,j) for i in range(4) for j in range(4)]
    lab += [('ddc',i,j,k) for i,j in combinations_with_replacement(range(4),2) for k in range(4)]
    a={v:atom(i) for i,v in enumerate(lab)}
    c=lambda i:a['c',i];dc=lambda i,j:a['dc',i,j]
    ddc=lambda i,j,k:a['ddc',min(i,j),max(i,j),k]
    w=[add(*(mul(c(j),dc(j,i)) for j in range(4))) for i in range(4)]
    dw=add(*(mul(dc(i,j),dc(j,i)) for i in range(4) for j in range(4)),
           *(mul(c(j),ddc(i,j,i)) for i in range(4) for j in range(4)))
    checks=[]
    def eq(name,A,B=None):
        assert not add(A,scale(B or {},-1)),(name,A,B);checks.append(name)
    # q0(chi eta a2)=-alpha chi eta div(w), from the independently checked volume descent.
    q0a2=scale(dw,-alpha*chi*eta)
    q1chi_a1eta=scale(add(scale(dw,chi),*(scale(w[i],l[i]) for i in range(4))),alpha*eta)
    q1eta_a1chi=scale(add(scale(dw,eta),*(scale(w[i],e[i]) for i in range(4))),alpha*chi)
    residual=add(q0a2,scale(add(q1chi_a1eta,q1eta_a1chi),s.Rational(1,2)))
    target=add(*(scale(w[i],alpha*(eta*l[i]+chi*e[i])/2) for i in range(4)))
    eq('polarized localized consistency source',residual,target)
    same=clean({mon:coef.subs({eta:chi,**dict(zip(e,l))},simultaneous=True) for mon,coef in residual.items()})
    eq('equal cutoffs',same,add(*(scale(w[i],alpha*chi*l[i]) for i in range(4))))
    assert residual;checks.append('cutoff source is nonzero')
    zero=clean({mon:coef.subs(dict.fromkeys(l+e,0)) for mon,coef in residual.items()})
    eq('constant cutoffs restore homogeneous identity',zero)
    # q0 q1_chi h + q1_chi q0 h = [Kg,chi]w.
    # The symmetric gradient commutator is evaluated in both metric signatures.
    for sig in [(1,1,1,1),(-1,1,1,1)]:
        comm={(i,j):add(scale(w[j],sig[j]*l[i]),scale(w[i],sig[i]*l[j]))
              for i in range(4) for j in range(4)}
        trace=add(*(scale(comm[i,i],sig[i]) for i in range(4)))
        eq('trace of symmetric-gradient cutoff commutator '+str(sig),trace,
           add(*(scale(w[i],2*l[i]) for i in range(4))))
        eq('(I1chi,B1chi) '+str(sig),scale(trace,alpha*chi/2),same)
    # Integration by parts: int chi eta div(w)=-int(eta dchi+chi deta).w.
    integrated_div=add(*(scale(w[i],-(eta*l[i]+chi*e[i])) for i in range(4)))
    integrated_q0=scale(integrated_div,-alpha)
    integrated_q1=add(*(scale(w[i],-alpha*(chi*e[i]+eta*l[i])/2) for i in range(4)))
    eq('integrated compact-support source',add(integrated_q0,integrated_q1),target)
    assert integrated_q0
    checks.append('compact support does not erase the cutoff source')
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),cpu_seconds=time.process_time()-start,
        source='alpha_W/2*(eta*dchi+chi*deta).(c.nabla c)',
        identity='q0(chi eta a2)+1/2[q1_chi(eta a1)+q1_eta(chi a1)]=source',
        equal_cutoff='alpha_W chi dchi.(c.nabla c)=(I1chi,B1chi)',
        mechanism='q_localized squared h = u [Kg,chi](c.nabla c)+O(u^2)',
        scope='Required inhomogeneous source from the volume completion; not complete A2 or all sources I1/I2',
        full_Q2=False,gate_changed=False)
    put(D/'results.json',result)
    opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    note=f'''[DERIVED+CAS — fonte de consistência localizada da primitiva; Q2 completa OPEN]

A continuação de volume anterior fornece a1=alpha_W div(c),
a2=alpha_W div(c trh)/2 e q0a2+q1a1=0 para o diferencial não localizado.
Agora localizamos a interação: q1_chi h=chi Lie_c h, q1_chi c=chi w,
w=c.nabla c. Para duas funções independentes chi e eta, a regra de produto dá

 q0(chi eta a2)+[q1_chi(eta a1)+q1_eta(chi a1)]/2
 =alpha_W(eta dchi+chi deta).w/2.

Para chi=eta, a fonte é alpha_W chi dchi.w, em geral não nula.
Seu endereço BV é preciso: q_localizado²h=u[Kg,chi]w+O(u²), pois
Kg(chi w)-chi Kg w=[Kg,chi]w. O termo de anticampo da inserção I1=s0Vchi
é -hdag[Kg,chi]w nas coordenadas B. Com B1chi=alpha_W int chi trh/2,
(I1chi,B1chi)=alpha_W int chi dchi.w. O traço do comutador é
tr[Kg,chi]w=2dchi.w. Não se trata de uma nova anomalia por si só: é a
fonte da identidade INHOMOGÊNEA já exigida pela localização.

São {result['checks']} verificações exatas, CPU {result['cpu_seconds']}s, rc0,
incluindo duas assinaturas, polarização, chi=eta, cutoffs constantes e
integração por partes. Suporte compacto elimina a integral da divergência
total; não elimina as derivadas dos cutoffs que restam. O controle que
descarta essa fonte falha. Nenhum tau foi escolhido para ajustar resíduo.

Este resultado liga a primitiva conhecida de A1 ao setor de anticampos
I1. Ainda não identifica o representante A2(Vchi,Veta) nem soma todos os
termos de consistência de duas entradas. O contato Euler composto e sua
normalização distribucional permanecem o passo seguinte da mesma árvore.
Originais e gate intactos. AberturaSHA256={opening}.
'''
    write(D/'DERIVACAO.md',note.encode('utf-8'))
    write(OUT/'ENTREGA_016_MEDIDA_fonte_localizada_primitiva_A1.md',note.encode('utf-8'))
    put(D/'manifest.json',dict(at=now.isoformat(),artifacts=[dict(path=str(p),sha256=sha(p)) for p in
        sources+[D/'PRE_REGISTER.json',D/'results.json',D/'DERIVACAO.md']],full_Q2=False,opening_sha256=opening))
    append(OUT/'LEDGER_016.jsonl',json.dumps(dict(at=now.isoformat(),target='A7.b',event='LOCALIZED_VOLUME_PRIMITIVE_SOURCE',
        checks=result['checks'],cpu_seconds=result['cpu_seconds'],remote_call=False,
        manifest_sha256=sha(D/'manifest.json')),ensure_ascii=False)+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f"\n{now.isoformat()} A7.b PROGRESS: fonte localizada alpha_W chi dchi.w identificada com (I1chi,B1chi); {result['checks']} controles, CPU {result['cpu_seconds']}s. Q2 completa OPEN. AberturaSHA256={opening}.\n")
    p=H/'CONTINUIDADE.json';st=json.loads(p.read_bytes())
    st.setdefault('head_history',[]).append({k:st.get(k) for k in ['at','previous_goal_turn','completed_this_turn','next','pending_orchestration']})
    st.update(at=now.isoformat(),previous_goal_turn='PROGRESS',completed_this_turn=[
        'MiMo57e reviewed; coordinate equivalence accepted with Lie-square explanatory correction',
        'Quadratic volume primitive checked with20controls',
        'Localized polarized source identified as the I1/B1 bracket;10controls'],
        next=['Compute/identify composite Euler source with actual radial two-entry extension',
              'Receive DeepSeekcd6 and authorized Kimi responses; no repeats',
              'A7b deadline20:32UTC; A7c/d,A8,PartB/final remain'])
    st['localized_volume_update']=dict(manifest=str(D/'manifest.json'),full_Q2=False)
    put(p,st,True)
    for a in json.loads((D/'manifest.json').read_bytes())['artifacts']:assert sha(Path(a['path']))==a['sha256']
    print(json.dumps(dict(manifest=str(D/'manifest.json'),checks=result['checks'],cpu_seconds=result['cpu_seconds']),ensure_ascii=False))

if __name__=='__main__':main()
