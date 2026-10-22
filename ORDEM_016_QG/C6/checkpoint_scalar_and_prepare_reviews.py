"""Publish measured scalar K² matching and prepare distinct textual reviews."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json,uuid,hashlib,subprocess
ROOT=Path(__file__).resolve().parents[1];C=ROOT/'C6';H=ROOT/'A7';D=C/'scalar_K2_delivery';Q=C/'orchestration_scalar_K2'
sys.path.insert(0,str(H))
from deliver_nonminimal_wick_and_mimo_audit import OUT,BASE,sha,put,write,append

def main():
    D.mkdir(exist_ok=False);Q.mkdir(exist_ok=False);now=datetime.now(timezone.utc);opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    names=['scalar_parallel','scalar_measured_primitive','scalar_second_curvature_v2','scalar_second_parallel_primitive']
    batches={n:json.loads((C/n/'results.json').read_bytes()) for n in names}
    final=batches['scalar_second_parallel_primitive']
    note=f'''[DERIVED+CAS — setor escalar até K²; correspondência local medida, Q2 integral OPEN]

AberturaSHA256={opening}.

No mesmo auxiliar euclidiano4D espaço-forma, calculamos o contato real
Euler_phi(X)c.grad(phi)(X) com o vértice cúbico h(phi,phi)(Y), três sabores,
na extensão parcial rotulada R_bal mais a regra de linha suave já fixada.
O parametrix singular local, sem acrescentar estado suave, é
H(r)=1/r²+K(1/4−log(r²)/2)+19K²r²/480.
A distância bilocal r²=w+K d1+K²d2 vem da lei dos cossenos do espaço-forma:
d1=−(xx yy−xy²)/3;d2=−(xx+yy−4xy)(xx yy−xy²)/45.
A verificação radial dá Lap H=29K²/20, compatível com o coeficiente de
calor anterior. É um parametrix, não um estado/bissolução global. A derivada
em Y desse termo constante desaparece nesta ordem; mantivemos isso separado
da extensão na diagonal. A primeira tentativa de controle exigia expand=0
numa expressão racional; cancel confirma a mesma identidade, sem trocar H.

O contato K² CE em derivadas coordenadas de delta é
 509/1920 δab Qr −187/1920(δar Qb+δbr Qa).
A leitura no fantasma contravariante transportado inclui P1=(xx I−xxᵀ)/6
e P2=7xx(xx I−xxᵀ)/360. Ela dá
 1289/5760 δab Qr −17/1152(δar Qb+δbr Qa).
Os jatos de transporte foram conferidos por preservação métrica e pela
ação das distribuições em funções-teste. Não se confundem esses dois pares.

Com os contatos de graus5,3,1, obteve-se N=N4+K N2+K² N0, usando o motor
covariante de jatos existente. N G(c) coincide com o polinômio medido nas
quatro polarizações, com momento simbólico e parâmetros b,c,t ainda livres.
N4,N2,N0 completos estão no results.json; nenhum parâmetro foi escolhido.
O fator da distribuição integrada em exp(ipx) é−i CE; ele foi mantido
explícito para não trocar o sinal entre graus5,3,1.

Isso paga a correspondência local deste setor na leitura declarada.
Ainda NÃO paga a naturalidade da família temporal integral, o setor
métrico/ghost completo, os cutoffs, as inserções compostas nem a classe
de Q2 inteira. O emprego como contratermo BRST exige conferir o adjunto
formal e transportar a identidade local ao funcional com esse mesmo sinal.
Crítica Kimi preparada para essa ligação; MiMo para a construção geométrica
de H até K². Resultados de modelos serão auditados separadamente.

Comandos,rc0 e CPU: scalar_parallel_readout.py,{batches['scalar_parallel']['cpu_seconds']}s;
scalar_measured_primitive.py,{batches['scalar_measured_primitive']['cpu_seconds']}s;
scalar_second_curvature_check_v2.py,{batches['scalar_second_curvature_v2']['cpu_seconds']}s;
scalar_second_parallel_primitive.py,{final['cpu_seconds']}s.
Controles respectivos217,128,312,296. São controles CAS exatos, não
compilações Lean. C6ACTIVE; prazo original inalterado. Originais/gate intactos.
'''
    write(D/'DERIVACAO.md',note.encode());write(OUT/'ENTREGA_016_MEDIDA_C6_escalar_K2_e_correspondencia.md',note.encode())
    files=[Path(__file__),D/'DERIVACAO.md']+[C/n/'manifest.json' for n in names]+[C/n/'results.json' for n in names]
    files += [C/'scalar_second_curvature_check.py',C/'scalar_second_curvature_run.log',C/'scalar_second_curvature_check_v2.py',C/'scalar_second_curvature_engine.py']
    put(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in files],batches=batches,full_Q2=False))
    prefix='ORDEM016 ParteC.C6. Memória científica comum obrigatória; texto somente, sem executar/alterar arquivos, sem gate ou confirmação física. Auxiliar euclidiano4D espaço-forma K constante, não escolher horizonte/estado físico. Uma pergunta por unidade; não repetir unidades antigas. Resultados locais abaixo são para crítica, não concordância automática. Prescrição parcial R_bal rotulada mais linha suave, não Rraw. '
    units=[('mimo','scalar_Hadamard_K2_bilocal_construction','draft',
        'Derive independentemente o parametrix escalar sem massa até K², com termo suave adicional zero, e a expansão da distância bilocal em uma carta RNC. A construção no código realmente coincide com a prescrição singular Hadamard/heat anterior (H=U0/r²-U1 log(r²)/4+U2 r² log(r²)/16+...), ou introduz termo suave não autorizado? Dê as recorrências/coeficientes e o defeito Euler, incluindo se a derivada Y do defeito suave pode ser descartada nesta ordem para o gráfico Ephi*dphi; diferencie valor coincidente de afirmação bilocal. Se identificar erro, exiba resíduo, sem alterar coeficientes para ajustar o resultado. Isto é unidade distinta da crítica tensorial anterior, já auditada; não a repetir.',
        [(C/'scalar_second_curvature_engine.py',None),(C/'scalar_second_curvature_check_v2.py',(1,48)),(H/'curved_parametrix_euler_defect_check.py',(18,99))]),
        ('kimi','scalar_actual_contact_to_local_BRST_primitive_K2','skeptic',
        'Audite a ligação nova: o contato escalar REAL, calculado e lido em campos paralelos, coincide em jatos com N G(c) para N4+K N2+K² N0. Escreva a definição de N com ordem simetrizada, verifique se é formalmente autoadjunto no produto natural de tensores e qual funcional quadrático B tem s0 B igual ao contato com o sinal correto (s0h=G(c), h par, c ímpar). A igualdade em quatro polarizações com momento simbólico e transporte paralelo é suficiente para o operador local linearizado neste fundo, ou resta uma hipótese adicional concreta? Distinguir isso da família causal/natural completa e do caso cutoff variável; se suficiente apenas com hipótese, nomeie-a. Não reivindicar Q2 completa nem recalcular o setor tensorial da unidade MiMo. Uma pergunta é exatamente a ligação contato medido→primitiva, não uma revisão geral da teoria.',
        [(C/'scalar_second_parallel_primitive/results.json',None),(C/'scalar_measured_primitive.py',None),(C/'scalar_second_parallel_primitive.py',None),(H/'oneform_second_curvature_engine_v2.py',None)])]
    rows=[]
    for provider,lemma,role,question,refs0 in units:
        prompt=prefix+question+'\n';refs=[]
        for p,span in refs0:
            lines=p.read_text('utf-8-sig').splitlines();lo,hi=span if span else (1,len(lines));part=lines[lo-1:hi]
            ref=dict(path=str(p),sha256=sha(p),first_line=lo,last_line=lo+len(part)-1);refs.append(ref)
            prompt+='\nSOURCE '+json.dumps(ref,ensure_ascii=False)+'\n'+'\n'.join(f'{lo+i}: {line}' for i,line in enumerate(part))+'\n'
        assert len(prompt)<=20000,(provider,len(prompt))
        rid=str(uuid.uuid4());ec=dict(mission_id='ORDEM_016',branch_id='C6',lemma_id=lemma,role=role,required_provider=provider,max_calls=1)
        if provider=='mimo':ec.update(max_cost_usd=None,max_output_tokens=131072)
        payload=Q/f'{provider}_submit.json';put(payload,dict(operation='submit',request_id=rid,prompt=prompt,execution_constraints=ec))
        put(Q/f'{rid}_origin.json',dict(at=now.isoformat(),thread_id='01a070fc-9484-7e13-a654-c6b5f61093a4',request_id=rid,payload=str(payload),payload_sha256=sha(payload),sources=refs,status='PREPARED_NOT_SUBMITTED'))
        res=subprocess.run([sys.executable,'-X','utf8','-B',str(BASE/'transport_cli.py')],input=json.dumps(dict(operation='preview_execution',prompt=prompt,execution_constraints=ec)),text=True,encoding='utf-8',capture_output=True,cwd=BASE)
        assert res.returncode==0,res.stderr
        preview=json.loads(res.stdout);put(Q/f'{provider}_preview.json',preview);assert preview.get('selected')==provider
        rows.append(dict(provider=provider,request_id=rid,payload=str(payload),payload_sha256=sha(payload),prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(),sources=refs,preview=str(Q/f'{provider}_preview.json'),prompt_chars=len(prompt),status='PREPARED_NOT_SUBMITTED'))
    put(Q/'prepared_units.json',rows)
    events=[dict(at=now.isoformat(),event='C6_SCALAR_K2_MATCHING',target='C6',remote_call=False,manifest_sha256=sha(D/'manifest.json'),batches=batches)]
    events += [dict(at=now.isoformat(),event='C6_SCALAR_REVIEW_PREPARED',remote_call=False,**r) for r in rows]
    append(OUT/'LEDGER_016.jsonl',''.join(json.dumps(e,ensure_ascii=False)+'\n' for e in events))
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} | C6 ACTIVE: escalar K² real e família local NG com b,c,t livres;217+128+312+296controles CAS, não somar rodadas prévias novamente | revisões MiMo/Kimi preparadas, sem execução nesta preparação; Q2 integral OPEN.\n')
    cp=H/'CONTINUIDADE.json';c=json.loads(cp.read_bytes());c.update(at=now.isoformat(),C6_scalar_K2_manifest=str(D/'manifest.json'),C6_new_reviews=str(Q/'prepared_units.json'),own_live_process=None,
        pending_orchestration='C6 initial three units terminal/audited; two new scalar K2 reviews prepared, not yet admitted',next=['C6 scalar review and remaining curved metric/ghost assembly','ORDEM015 PartB','Final audit/report'])
    put(cp,c,True);print(json.dumps(rows,ensure_ascii=False),flush=True)
if __name__=='__main__':main()
