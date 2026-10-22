"""Record the labelled dual and Schur links; prepare one independent skeptic unit."""
from pathlib import Path
from datetime import datetime,timezone
import json,sys,uuid
import sympy as s
ROOT=Path(__file__).resolve().parents[1];C=ROOT/'C6';H=ROOT/'A7'
sys.path.insert(0,str(H))
from deliver_nonminimal_wick_and_mimo_audit import OUT,sha,write,put,append


def main():
    now=datetime.now(timezone.utc);D=C/'dual_schur_delivery';D.mkdir(exist_ok=False)
    dual=json.loads((C/'ghost_dual_check/results.json').read_bytes())
    schur=json.loads((C/'nonminimal_metric_euler_check_v2/results.json').read_bytes())
    table=json.loads((C/'nonminimal_metric_euler_check_v2/TABLE.json').read_bytes())
    checks=0
    for key,row in table.items():
        import ast
        a,b,c,d=ast.literal_eval(key)
        ident=s.Rational(int(a==c)*int(b==d)+int(a==d)*int(b==c),2)
        trace=int(a==b)*int(c==d)
        assert s.sympify(row['full'])==(10*ident+31*trace)/128
        assert s.sympify(row['mixed_correction'])==(18*ident-trace)/128
        checks+=2
    opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    note=f'''[DERIVED+CAS — ligação dual ghost e Euler métrico completo em primeira curvatura; Q2 OPEN]

AberturaSHA256={opening}.

1. Ghost: H^a_b foi dualizado para gX_ac H^c_d gY^db usando o motor
rotulado existente. A compatibilidade métrica foi confrontada com uma
recursão independente, com conexões covetorX/vetorY: 57 palavras,
{dual['checks']} verificações, CPU{dual['cpu_seconds']}s, rc0. Não há sinal
de Wick atribuído nesta ligação. Nos contatos sem jatos extras com
espectador ghost,16 dos256 valores mudam: nas componentes diagonais,
7/16 passa a1/4 (diferença−3/16), em unidades CE*K. O plano é preservado.

2. Métrica: implementado PH_hh=I_tr Lh P−Cstar S com
S=−2CP−HQ Kstar; P=Hh I_tr, HD=−4κP, ell=1/(2κ).
Cstar v=−sym∇v+g div(v)/2. Métricas, derivadas e densidade são
aplicadas antes da extensão. O código reaproveita os perfis e palavras
radiais; não introduz outro parâmetro nem troca a prescrição.
{schur['checks']} verificações, CPU{schur['cpu_seconds']}s, rc0.

O bloco misto é zero fora da diagonal atéK, mas suas palavras rotuladas
não somam zero antes da extensão:22 dos100 contatos ganham contribuição.
Para o espectador métrico(01,01), a tabela inteira verifica:
 contato_misto/(CE*K)=(18 Id_sym−g⊗g)/128;
 contato_completo/(CE*K)=(10 Id_sym+31 g⊗g)/128.
{checks} comparações adicionais conferem estas fórmulas nas100 componentes.
Não extrapolamos essa tabela a espectador arbitrário nem a jatos maiores.

Falha preservada: o primeiro verificador deixou w independente de|x−y|²
na comparação fora da diagonal. Seu rc1 e log permanecem. A v2 impõe
essa relação só na realização ordinária; o motor rotulado não mudou.

Alcance: ligações necessárias à montagem, não a soma final de vértices.
Pesos temporais, montagem completa e Q2 integral continuam OPEN.
Crítica externa específica preparada; resultado ainda não recebido.
Nenhum original, kernel, gate, Atlas ou diário canônico foi alterado.
'''
    write(D/'DERIVACAO.md',note.encode());write(OUT/'ENTREGA_016_MEDIDA_C6_dual_ghost_e_Schur.md',note.encode())
    paths=[Path(__file__),C/'labelled_ghost_dual.py',C/'labelled_ghost_dual_check.py',C/'labelled_ghost_dual_check_run.log',
      C/'ghost_dual_check/manifest.json',C/'labelled_nonminimal_metric_euler.py',C/'labelled_nonminimal_metric_euler_check.py',
      C/'labelled_nonminimal_metric_euler_check_run.log',C/'labelled_nonminimal_metric_euler_check_v2.py',
      C/'labelled_nonminimal_metric_euler_check_run_v2.log',C/'nonminimal_metric_euler_check_v2/manifest.json',D/'DERIVACAO.md',
      C/'audit_mimo_scalar_K2_run.log',C/'mimo_scalar_K2_audit/manifest.json']
    put(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in paths],opening_sha256=opening,
       formula_checks=checks,full_Q2=False,gate_changed=False))
    O=C/'orchestration_dual_schur';O.mkdir(exist_ok=False)
    prompt='''ORDEM016 ParteC.C6, unidade nova e única, crítica independente. Texto somente; não executar/alterar arquivos nem mover gate. Auxiliar euclidiano4D de curvatura constante, não escolher horizonte/estado físico. Memória científica comum obrigatória. PERGUNTA: a tradução do bloco não mínimo PH_hh=D HD−Cstar S, com S=ell C HD−HQ Kstar, para os índices/palavras do motor abaixo preserva os sinais, a dualização e os fatores de traço? Verificar também a dualização necessária da linha antighost, pois ela entra na mesma montagem. Use C h=div h−d tr(h)/2; K c=2sym∇c; Kstar h=−2div h; Cstar v=−sym∇v+g div(v)/2; HD=−4κP; P=Hh Itr; ell=1/(2κ), D=−Itr Lh/(4κ); Lh=roughBox−2K+2Kg tr, Q=roughBox+3K. P tem quatro slots covariantes; HQ tem vetorX/covetorY. Todos os termos mantêm o mesmo rótulo radial até a extensão. Plano PH_hh=Id_sym box f passou; fora da diagonal a ordemK é zero após impor w=|x−y|², mas há contatos locais da prescrição parcial. Não exigir que palavras rotuladas com mesma realização fora da diagonal tenham mesma extensão — isso é justamente o defeito de Ward local a medir. Se houver erro, exiba índice/sinal/contramodelo explícito; não conclua Q2 inteira. Os coeficientes são resultados CAS declarados, não provas kernel. A pergunta é a ligação Schur/dual tipada, não revisar toda TGL.\n'''
    selected=[C/'labelled_nonminimal_metric_euler.py',C/'labelled_ghost_dual.py',C/'labelled_covariant_xy.py',C/'labelled_bilocal_jet_engine.py',D/'DERIVACAO.md']
    refs=[]
    for p in selected:
        lines=p.read_text('utf-8').splitlines();ref=dict(path=str(p),sha256=sha(p),first_line=1,last_line=len(lines));refs.append(ref)
        prompt+='\nSOURCE '+json.dumps(ref,ensure_ascii=False)+'\n'+'\n'.join(f'{i}: {line}' for i,line in enumerate(lines,1))+'\n'
    assert len(prompt)<=20000,len(prompt)
    request=str(uuid.uuid4())
    payload=dict(operation='submit',request_id=request,prompt=prompt,execution_constraints=dict(mission_id='ORDEM_016',branch_id='C6',lemma_id='full_nonminimal_Schur_dual_labelled_typing',role='skeptic',required_provider='kimi',max_calls=1))
    put(O/'kimi_submit.json',payload);put(O/'ORIGIN.json',dict(at=now.isoformat(),request_id=request,origin_thread_id='01a070fc-9484-7e13-a654-c6b5f61093a4',status='PREPARED_NOT_SUBMITTED',prompt_characters=len(prompt),sources=refs,payload_sha256=sha(O/'kimi_submit.json')))
    append(OUT/'LEDGER_016.jsonl',json.dumps(dict(at=now.isoformat(),event='C6_DUAL_SCHUR_LOCAL_LINKS',target='C6',remote_call=False,
      formula_checks=checks,ghost_checks=dual['checks'],Schur_checks=schur['checks'],successful_cpu_seconds=dual['cpu_seconds']+schur['cpu_seconds'],failed_cpu_unknown=True,
      manifest_sha256=sha(D/'manifest.json')),ensure_ascii=False)+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} | C6ACTIVE: dualghost e PH_hh completo ligados à extensão rotulada; {dual["checks"]+schur["checks"]+checks}verificações,CPUdasduasrodadas{dual["cpu_seconds"]+schur["cpu_seconds"]}s;1falha de verificador preservada; críticaKimi apenas preparada;Q2OPEN.\n')
    p=H/'CONTINUIDADE.json';state=json.loads(p.read_bytes());state.update(at=now.isoformat(),C6_dual_schur_manifest=str(D/'manifest.json'),C6_new_skeptic_origin=str(O/'ORIGIN.json'),pending_orchestration='Dual/Schur Kimi unit PREPARED_NOT_SUBMITTED; previous C6 units audited',next='Conferir critica Schur/dual e montar vertices metricos/ghost existentes; nao confundir os zerojets com Q2 completa. Deadline C6 inalterado.')
    put(p,state,True)
    print(json.dumps(dict(request_id=request,payload=str(O/'kimi_submit.json'),chars=len(prompt),manifest=str(D/'manifest.json')),ensure_ascii=False))


if __name__=='__main__':main()
