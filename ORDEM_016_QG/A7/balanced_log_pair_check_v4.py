"""Convert Hadamard radial/log profiles without mixing raw and balanced schemes."""
from pathlib import Path
from datetime import datetime,timezone
from itertools import combinations_with_replacement
import json,time
import sympy as s
import balanced_log_pair_engine as E
from balanced_pair_normalization_check_v2 import correction as old_correction
from deliver_nonminimal_wick_and_mimo_audit import H,OUT,sha,write,put,append

D=H/'balanced_log_pair_v4'

def main():
    D.mkdir(exist_ok=False);now=datetime.now(timezone.utc)
    sources=[Path(__file__),H/'balanced_log_pair_check_v3.py',H/'balanced_log_pair_v3/results.json',H/'smooth_line_compatibility_check.py',H/'smooth_line_compatibility_run.log',H/'balanced_log_pair_check_v2.py',H/'balanced_log_pair_run_v2.log',H/'balanced_log_pair_check.py',H/'balanced_log_pair_run.log',H/'balanced_log_pair_engine.py',H/'balanced_pair_normalization_check_v2.py',
        H/'logarithmic_contact_engine.py',H/'hadamard_pair_curvature/results.json',H/'bilocal_first_curvature_engine.py']
    put(D/'PRE_REGISTER.json',dict(at=now.isoformat(),
        prescription='Same Dtot/Dbal decomposition; each balanced primary extended by the fixed raw (1-a) Mellin prescription, total derivatives after extension',
        profiles=['f=1/z','log(mu2 z)','1'],
        tasks=['Agree with previous f/f engine','Exchange and total derivative identities',
            'Table of f/log and f/1 corrections through order4','Radial scalar Euler zero-jet O(K) contact'],
        scope='Labelled radial line profiles only; full two-endpoint tensor connections and curved vertices not included',
        sources=[dict(path=str(p),sha256=sha(p)) for p in sources]))
    cpu=time.process_time();checks=[];table=[]
    def eq(name,a,b=0):
        assert s.cancel(a-b)==0,(name,a,b);checks.append(name)
    profiles=[((1,0),(1,0)),((1,0),(0,1)),((1,0),(0,0))]
    words=[tuple(w) for degree in range(5) for w in combinations_with_replacement(range(4),degree)]
    for a,b in profiles:
        count=0
        for u in words:
            for v in words:
                if len(u)+len(v)>4:continue
                value=E.correction(a,b,u,v)
                eq('exchange profiles and words',value,E.correction(b,a,v,u))
                if a==b:eq('same existing f/f extension',value,old_correction(u,v))
                if len(u)+len(v)<=3:
                    raw=E.line(*a,u)*E.line(*b,v)
                    for i in range(4):
                        lhs=E.correction(a,b,tuple(sorted(u+(i,))),v)+E.correction(a,b,u,tuple(sorted(v+(i,))))-E.Q[i]*value
                        eq('total derivative identity',lhs,-E.contact(s.expand(raw),(i,)))
                table.append(dict(profiles=[a,b],left=u,right=v,delta_over_CE=str(value)));count+=1
        print(json.dumps(dict(profile=[a,b],entries=count,cpu_seconds=time.process_time()-cpu)),flush=True)
    f,lg,one=(1,0),(0,1),(0,0);q2=sum(q*q for q in E.Q)
    ef_f=E.euler_correction(f,f);ef_l=E.euler_correction(f,lg);el_f=E.euler_correction(lg,f);ef_1=E.euler_correction(f,one)
    eq('f/f Euler unchanged',ef_f,3*q2/32)
    eq('measured smooth-line incompatibility',ef_1,s.Rational(3,4))
    eq('derivative of constant line spuriously nonzero',E.euler_correction(one,f),-s.Rational(1,4))
    # Scalar normal-coordinate radial profile H=f+K(1/4-log(z)/2)+O(K²).
    # Radial Laplacian L=L0-2K z d/dz. L1 f=+2f.
    # At O(K) the raw -1/2*(Box log)f+2f*f cancels exactly off diagonal.
    log_box=sum(E.dx(E.dx(E.L,i),i) for i in range(4))
    eq('radial offdiagonal Euler cancellation',log_box.subs(E.z,sum(x*x for x in E.x))-4/sum(x*x for x in E.x))
    geometry=sum(s.diff(ef_f,q,2) for q in E.Q)/3
    geometry-=sum(s.diff(E.correction(f,f,tuple(sorted((i,j))),()),E.Q[i],E.Q[j]) for i in range(4) for j in range(4))/3
    geometry+=2*sum(s.diff(E.correction(f,f,(i,),()),E.Q[i]) for i in range(4))
    eq('ordered geometric Laplacian contact',geometry,s.Rational(3,8))
    radial_euler_K=s.expand(ef_1/4-ef_l/2-el_f/2+geometry)
    # Reconstruct the same correction by multilinearity before summing the Laplacian.
    direct=sum(E.correction(f,one,(i,i),())/4-E.correction(f,lg,(i,i),())/2-E.correction(lg,f,(i,i),())/2 for i in range(4))
    eq('radial O(K) composite Euler direct assembly',radial_euler_K,direct+geometry)
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),cpu_seconds=time.process_time()-cpu,
        pair_entries=len(table),Euler_corrections_over_CE=dict(f_f=str(ef_f),f_log=str(ef_l),log_f=str(el_f),f_one=str(ef_1)),
        radial_scalar_Euler_zerojet_K=str(radial_euler_K),smooth_compatibility=False,geometric_operator_contact=str(geometry),
        radial_model='H=1/z+K/4-K*log(mu2 z)/2, Box_radial=4z dzz+(8-2Kz)dz, normalized leading coefficient1',
        caveat='Radial zero-jet composite, not the full covariant Euler insertion with arbitrary derivative slots; smooth W and tensor connections are separate',
        family_changed=False,full_Q2=False,gate_changed=False)
    put(D/'TABLE.json',table);put(D/'results.json',result);opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    note=f'''[DERIVED+CAS — conversão balanceada dos perfis logarítmicos de Hadamard]

A tentativa v1 falhou no controle de linha suave: o valor é3/4, não1.
A v4 registra essa incompatibilidade; não a elimina trocando a expectativa
por uma alegação de sucesso. O motor e as tentativas originais são preservados. A v2 falhou apenas
na redução de uma identidade racional (expand não reduz denominadores);
a v3 usa cancel no verificador, sem alterar as expressões do motor.
A v4 corrige o sinal do termo z delta_ij: x_i x_j atua como
+derivada_qi derivada_qj, portanto z atua como +Laplaciano_q.
A v3 errou este sinal; seu contato geométrico -1/8 fica substituído
por +3/8. A falha do controle de densidade detectou o erro.

O motor mantém a mesma prescrição R_bal, agora em linhas rotuladas
1/z,log(mu²z),1. Não soma coeficientes de Rraw aos grafos balanceados.
{len(table)} entradas até ordem4 foram calculadas; troca de linhas/perfis,
Leibniz até ordem3 e coincidência com o motor f/f existente conferidas.

Correções de Euler normalizadas por CE:
 f/f:{ef_f}; f/log:{ef_l}; log/f:{el_f}; f/1:{ef_1}.
Os valores f/log e log/f não devem ser confundidos: na segunda posição
o Laplaciano age na outra linha; trocar as linhas troca também a inserção.

A extensão ingênua dá R_bal((Box f)1)/CE=3/4 e
R_bal(f Box1)/CE=-1/4. Isso não respeita a linha constante como suave;
Leibniz sozinho não fixa essa compatibilidade. A tabela, portanto,
NÃO é promovida a família temporal completa.

No modelo RADIAL escalar de primeira curvatura,
H=1/z+K/4-K log(mu²z)/2 e L=4z dzz+(8-2Kz)dz.
L1(1/z)=2/z cancela o termo -Box(log)/(2z) fora da diagonal.
Mas não se pode reduzir L1 antes de estender: seus coeficientes
(z delta_ij-x_i x_j)/3 e -2x_i deixam contato adicional +3/8.
Este contato é mantido na conta abaixo.
O contato composto no jato sem derivadas adicionais é
 CE[3q²/32+K*({radial_euler_K})] no recorte descrito.
Esse número pertence à extensão com o defeito suave identificado acima.
Não é o valor de uma família temporal admissível nem a anomalia curva.

Faltam os jatos covariantes bilocais/tensoriais, a referência suave e a
montagem dos vértices de curvatura na MESMA família. Esta conta não
identifica o horizonte físico nem demonstra causalidade lorentziana.
{len(checks)}controles;CPU{result['cpu_seconds']}s,rc0. Sem chamadas/gate.
AberturaSHA256={opening}.
'''
    write(D/'DERIVACAO.md',note.encode());write(OUT/'ENTREGA_016_MEDIDA_perfis_log_balanceados_v4.md',note.encode())
    put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'TABLE.json',D/'results.json',D/'DERIVACAO.md']],full_Q2=False))
    append(OUT/'LEDGER_016.jsonl',json.dumps(dict(at=now.isoformat(),event='BALANCED_LOG_HADAMARD_PROFILES',target='A7.b',checks=len(checks),cpu_seconds=result['cpu_seconds'],remote_call=False,manifest_sha256=sha(D/'manifest.json')))+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7.b: perfis f/log/1 convertidos em R_bal;{len(table)}pares,{len(checks)}controles CPU{result["cpu_seconds"]}s. ContatoEulerKradial={radial_euler_K},Q2curvaOPEN.AberturaSHA256={opening}.\n')
    print(json.dumps(result),flush=True)

if __name__=='__main__':main()
