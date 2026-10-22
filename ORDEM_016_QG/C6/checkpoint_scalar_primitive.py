"""Record the explicit scalar primitive and mixed-profile regression without closing C6."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json
ROOT=Path(__file__).resolve().parents[1];H=ROOT/'A7';C=ROOT/'C6';D=C/'scalar_primitive_checkpoint'
sys.path.insert(0,str(H))
from deliver_nonminimal_wick_and_mimo_audit import OUT,sha,put,write,append

def main():
    D.mkdir(exist_ok=False);now=datetime.now(timezone.utc);opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    adj=json.loads((C/'scalar_formal_adjoint/results.json').read_bytes());mixed=json.loads((C/'labelled_covariant_xy/results.json').read_bytes())
    # Verify every dependency explicitly enumerated in the new manifests.
    verified={}
    manifests=[C/'scalar_K2_delivery/manifest.json',C/'scalar_formal_adjoint/manifest.json',C/'labelled_covariant_xy/manifest.json',C/'scalar_second_parallel_primitive/manifest.json']
    for manifest in manifests:
        m=json.loads(manifest.read_bytes())
        for entry in m['files']:
            p=Path(entry['path']);value=sha(p);assert value==entry['sha256'],p;verified[str(p)]=value
    jobs=[dict(provider='mimo',request_id='e4fa07c7-dc54-4e38-a4e8-5d518aa3d148',job_id='d35f5145-adb0-43ce-8636-1863a2d13dd3',execution_task_id='0d0489df-2a6e-4dd8-97d5-5dea0fa5bc89'),
        dict(provider='kimi',request_id='2877213d-3931-4e0e-8cf1-0faf605432d7',job_id='e160b57b-85e3-4ae7-842d-ec6da2fd5166',execution_task_id='1b934883-e929-4957-8594-de471ba7b1b5')]
    put(D/'ORCHESTRATION_REPORTED.json',dict(at=now.isoformat(),source='Official message from coordinator01a0ce2b-8c2f-71b0-a9a8-91b17715a569',state='RUNNING_REPORTED',worker=32907,jobs=jobs,own_worker=False))
    note=f'''[DERIVED+CAS — primitiva escalar linearizada, prescrição e suporte declarados]

AberturaSHA256={opening}.

A correspondência local escalar até K² foi completada por uma prova escrita
de adjunção formal. Cada palavra de derivadas de N é COMPLETAMENTE
simetrizada. Integração por partes reverte a palavra par; a simetrização
é invariante sob essa reversão. Os coeficientes são paralelos, feitos da
métrica e de K constante. O transposto das fibras foi conferido com o
peso correto2 dos componentes fora da diagonal. As duas parcelas cruzadas
têm o mesmo coeficiente; retirar uma delas deixa defeito não nulo.

Sob suporte compacto/ausência de contribuição de borda, portanto N*=N.
Com s0h=G(c), h par, a regra graduada dá
 s0(1/2 integral h.Nh)=integral h.NG(c).
Na orientação distributiva calculada,
 A_scalar=−CE integral h.NG(c),
 B_scalar=−CE/2 integral h.Nh,
 e s0 B_scalar=A_scalar.
O termo de sinal oposto cancela ESTE representante linearizado. Não se
escolheu b,c,t; a família inteira é preservada. O fator temporal/QME do
grafo ainda não foi combinado com os outros setores.

404controles algébricos,CPU{adj['cpu_seconds']}s,rc0. O motor de jatos mistos
X/Y também passou{mixed['checks']}controles,CPU{mixed['cpu_seconds']}s,rc0:
perfis métricos covariantes e ghost contravariante em X/covariante em Y,
incluindo conexões dos próprios slots de derivada. Regressões recuperam
zerojets e a tabela tensorial rotulada anterior; não são evidência nova
daquelas parcelas já computadas.

Não concluídos: prescrição temporal causal integral/natural, cutoff variável,
montagem do inverso não mínimo com blocos h,b, setor métrico/ghost completo,
classe integral deQ2. Não houve compilação Lean neste lote. Nenhum gate
ou original foi tocado. C6 continuaACTIVE até o teto original; PartB segue
pendente. Críticas MiMo/Kimi em execução pela tarefa coordenadora, worker32907;
não iniciar outro worker nem repetir IDs. Custo parcial conhecido inalterado.
'''
    write(D/'DERIVACAO.md',note.encode());write(OUT/'ENTREGA_016_MEDIDA_C6_primitiva_escalar_linearizada.md',note.encode())
    put(D/'manifest.json',dict(at=now.isoformat(),opening_sha256=opening,verified_sources=verified,
        files=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),D/'DERIVACAO.md',D/'ORCHESTRATION_REPORTED.json']],full_Q2=False))
    next_text='''[OPEN — próxima etapa da mesma C6; prazo não reiniciado]
Deadline: 2026-09-26T06:07:12.868245+00:00. A7b permanece encerrada.
1. Aguardar/auditar duas críticas escalares pelos IDs de ORCHESTRATION_REPORTED.json. Não repetir.
2. O setor escalar local graus5,3,1 e sua primitiva linearizada estão medidos; não recalcular sem falha nova.
3. Próxima ligação científica: inserir o Euler COMPLETO do bloco não mínimo nos pares métricos/ghost. O roughBox tensorial isolado não é automaticamente P_HH. Reutilizar A7/nonminimal_wick_heat_ward_check.py: P H no bloco hh=D HD−Cstar S, S=ell C HD−HQ Kstar. A identidade de blocos está paga; faltam os contatos rotulados com os vértices. Não adotar o falso resíduo MiMo (auditoria em mimo_parametrix_audit_v2).
4. Usar C6/labelled_covariant_xy.py para derivadas X/Y e L.pair existente. Não expandir a palavra radial em outro perfil antes da extensão; a regressão LABELLED_REGRESSION.json mostrou por quê.
5. Ghost atual tem X contravariante/Y covariante. Qbarc requer dualização (gX H gY^{-1}) e conexões com os sinais respectivos, antes de atribuir sinais Wick. Não reutilizar automaticamente como covetor X.
6. A soma temporal e a família causal continuam abertas; não confundir primitivas de um setor com nulidade de Q2 inteira.
7. EncerradoC6 por aceitação/teto: entregaMEDIDA e ORDEM015 PartB integral; depois relatórios finais015/016. Não fechar a meta antes.
'''
    write(D/'NEXT.md',next_text.encode())
    events=[dict(at=now.isoformat(),event='C6_SCALAR_FORMAL_PRIMITIVE_AND_MIXED_JETS',remote_call=False,checks=adj['checks']+mixed['checks'],cpu_seconds=adj['cpu_seconds']+mixed['cpu_seconds'],manifest_sha256=sha(D/'manifest.json'))]
    events += [dict(at=now.isoformat(),event='C6_SCALAR_REVIEW_RUNNING_REPORTED',source='official coordinator',tokens=None,cost_usd=None,**job) for job in jobs]
    append(OUT/'LEDGER_016.jsonl',''.join(json.dumps(e)+'\n' for e in events))
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} | C6 ACTIVE: primitiva escalar local s0B=A atéK²;404controles adjunto+5396regressões mistas,CPU{adj["cpu_seconds"]+mixed["cpu_seconds"]}s | duas críticas running;Q2 integral OPEN;prazo06:07:12UTC.\n')
    cp=H/'CONTINUIDADE.json';c=json.loads(cp.read_bytes());c.update(at=now.isoformat(),C6_scalar_primitive_manifest=str(D/'manifest.json'),C6_mixed_jets_manifest=str(C/'labelled_covariant_xy/manifest.json'),
        own_live_process=None,own_live_processes=[],C6_jobs=jobs,pending_orchestration='Two scalarK2 units RUNNING reported by coordinator worker32907; initial three C6 units audited terminal',
        next=['C6 complete nonminimal Euler pair assembly, see scalar_primitive_checkpoint/NEXT.md','Audit two pending scalar reviews','ORDEM015 PartB','Final audit/report'])
    put(cp,c,True);print(json.dumps(dict(status='C6_ACTIVE',verified_artifacts=len(verified),cost_partial=c['partial_metered_cost_usd'],own_processes=[])),flush=True)
if __name__=='__main__':main()
