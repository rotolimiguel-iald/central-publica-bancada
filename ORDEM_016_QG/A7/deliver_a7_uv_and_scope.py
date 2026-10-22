"""Deliver A7.d typed scope and consolidate A7 without promoting partial Q2."""
from pathlib import Path
from datetime import datetime,timezone
import json
from deliver_nonminimal_wick_and_mimo_audit import H,OUT,sha,write,put,append

def main():
    now=datetime.now(timezone.utc);D=H/'uv_scope';src=D/'UVScope016_v3.lean';log=D/'uv_scope_03.log'
    auditpath=D/'axiom_audit_v3.json';audit=json.loads(auditpath.read_bytes())[0]
    assert audit['auditoria']=='PASSA' and audit['n_theorem_lemma_na_fonte']==11
    assert audit['n_declaracoes_auditadas']==11 and all(not v for v in audit['axiomas'].values())
    receipts=[]
    for i in range(1,4):
        p=D/f'uv_scope_{i:02}.json';r=json.loads(p.read_bytes());sp=Path(r['command'][-1]);lp=p.with_suffix('.log')
        assert sha(sp)==r['source_sha256'] and sha(lp)==r['log_sha256'];receipts.append(r)
    assert receipts[-1]['rc']==0 and not receipts[-1]['scan_errors']
    assert receipts[0]['rc']==1 and receipts[1]['rc']==1
    wall=sum(r['wall_seconds'] for r in receipts);cpu=sum(r['cpu_user_seconds']+r['cpu_kernel_seconds'] for r in receipts)
    source_state=OUT.parent/'PARA_CHATGPT/ORDEM_016_INSUMOS/ESTADO_QG_v370.json'
    historical=json.loads(source_state.read_bytes())
    verdict=historical['selo']['renormalization_wall_verdict']
    opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    result=dict(at=now.isoformat(),status='TYPED_SCOPE_ONLY',route_A='ZeroEffectiveHamiltonianRoute',route_B='MetricOperatorRoute',
        explicit_inputs=['isTypeIII1','effectiveHamiltonian_zero','metricSymmetric','commonDenseDomain','covariance','classicalLimit'],
        separate_completion_requirements=['renormalizedAllOrders','interactingQME','matchesPhysicalPair'],
        predicates_uninterpreted_named_inputs=True,physical_metric_constructed=False,typeIII_analysis_constructed=False,
        negative_controls='Pure logical countermodel only; not a physical factor or a theory of gravity',
        lean_theorems=11,axiom_audit='PASSA',all_printed_axioms=[],compile_attempts=3,
        compile_wall_seconds=wall,compile_cpu_seconds=cpu,physical_uv_resolved=False,
        historical_source_sha256=sha(source_state),historical_renormalization_label=verdict,
        denied_original_source_read='Read-only rg on current canonical um.py denied by filesystem; no original executed or imported',
        first_compile_failure='lake env attempted missing mathlib checkout in protected kernel; permission denied; rc1. Global scan also denied packages.',
        final_environment='Bench-only dependency-free lake project, import Init, Lean4.31.0',
        second_compile_failure='Universe levels in logical countermodel; v3 PUnit generalizes levels. v2 retained.',
        external_scientific_review_of_this_typing=False,gate_changed=False)
    put(D/'RESULTS.json',result)
    note=f'''[REAL — escopoUV tipado em Lean; hipóteses explícitas; UV físico não resolvido]

A7.d cumprido no alcance pedido: estruturas para as duas rotas.
ZeroEffectiveHamiltonianRoute exige álgebra, hipótese isTypeIII1 e
H_eff=0 fornecida; não deriva H_eff=0 de tipoIII. MetricOperatorRoute
exige candidato métrico, simetria, domínio comum denso, covariância e
limite clássico fornecidos. Esses predicados são INPUTS nomeados;
o arquivo não implementa análise de fatores ou operadores não limitados.

Completion exige SEPARADAMENTE renormalização em todas as ordens,
QME interagente e correspondência com o par físico. O contraexemplo
é puramente lógico: dois pacotes de rota e canto finito não implicam
esses pagamentos em um esquema de hipóteses arbitrárias. Não é um
contramodelo físico nem um habitanteTGL fabricado.

Compilação final rc0;11teoremas,11prints auditados, nenhum axioma
utilizado, zero sorry/erro. Auditorv2 da gerência: PASSA.
Lean4.31.0, projeto lake isolado da bancada, import Init, sem dependências.
Comando integral e hash fonte/log em uv_scope_03.json. Reprodução:
python A0/compile_isolated_v2.py <uv_scope/compiler_env>
 <uv_scope/UVScope016_v3.lean> <novo_label>.
O helper executa lake env lean, nunca lake build.

Falhas preservadas:01tentou dependência no kernel protegido e foi
recusada; a leitura do um.py original também foi negada. Não insistimos.
02tinha conflito de universos no contramodelo;03generaliza comPUnit.
Os recibos distinguem o ambiente de bancada do kernel canônico.
A checagem global do primeiro ambiente foi limitada pela permissão;
nenhuma instalação nele foi concluída. A rodada final escreve só aqui.

Recursos3tentativas: parede{wall:.6f}s;CPU{cpu:.6f}s.
O nomeGoroff–Sagnotti permanece rótuloDECLARADO do selo histórico;
nenhum teorema da literatura foi acrescentado como premissa. Sem
revisão científica externa nova desta tipagem; compilador e auditor
verificam o alcance lógico acima. Nenhum gate/identificação física muda.
AberturaSHA256={opening}.
'''
    write(D/'DERIVACAO.md',note.encode());write(OUT/'ENTREGA_016_A7d_escopo_UV_tipado.md',note.encode())
    refs=[Path(__file__),src,log,auditpath,D/'RESULTS.json',D/'DERIVACAO.md',source_state,
        D/'compiler_env/lakefile.toml',D/'compiler_env/lean-toolchain',D/'compiler_env/lake-manifest.json',src.with_suffix('.olean')]
    for i in range(1,4):
        p=D/f'uv_scope_{i:02}.json';r=json.loads(p.read_bytes());refs += [p,p.with_suffix('.log'),Path(r['command'][-1])]
    refs=list(dict.fromkeys(refs));put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in refs],physical_uv_resolved=False))
    a7c=json.loads((H/'A7c_named_remainder/results.json').read_bytes())
    whole=dict(at=now.isoformat(),A7a='SOURCE_REGISTER_PAID',A7b='FULL_Q2_NOT_PAID_TIMEBOX_MEASURED',
        A7c='PRECISE_REMAINDER_NAMED',A7d='SCOPE_TYPED_PHYSICAL_UV_OPEN',
        receipts=[str(H/'A7a_SOURCE_REGISTER.json'),str(H/'A7c_named_remainder/manifest.json'),str(D/'manifest.json')],
        interacting_frontier_discharged=False,gate_changed=False,next='A8')
    put(H/'A7_FINAL_STATUS.json',whole)
    report=f'''[REAL/DERIVED/OPEN — A7 entregue com MEDIDA; escopo interagente não fechado]

|Ramo|Entrega|Resultado|
|---|---|---|
|A7.a|A7a_SOURCE_REGISTER.json|Primitiva clássica e limite de ordem separados de anomalia quântica|
|A7.b|A7c_named_remainder/manifest.json|Timebox20:32UTC encerrado; Q2curva completa NÃO PAGA|
|A7.c|ENTREGA_016_MEDIDA_A7b_timebox_e_A7c.md|Família temporal, representante, WZ/classe e contratermos nomeados|
|A7.d|uv_scope/manifest.json|Duas rotas tipadas,11teoremas lógicos rc0/auditorPASSA; UV físico OPEN|

O resultado quantitativo plano é a soma Einstein+3sigma com primitiva
livre e consistência localizada nos jatos testados. Os contatos curvos
escalares e vetoriais coincidem entre pontas após densidade/conexões.
Isso não é a quebra curva total. As tabelas e erros corrigidos estão
nos manifestos de cada lote; nenhuma tentativa falha foi apagada.

Na ordemhbar e aridade temporal2 faltam a família conjunta covariante,
os termos tensoriais e demais inserções/vértices/ordens. Não se atribui
classe não nula a um representante ainda incompleto. O h/c tem ansatz
de contratermosN4+K*N2+K²*N0, com extensões adicionais necessárias.

**Não move** interacting_quantum_state_BRST_QME_anomalies_and_UV_scope:
nenhum estado interagente físico, QME completa ou UV resolvido foi
produzido. Nenhum original, identificador reservado ou gate é editado.
As alternativasUV só registram condições; cantoBreuer finito não as paga.

RecursosA7.b: corte de{a7c['A7b']['hours_anchor_to_deadline']:.6f}h desde
a âncora registrada; CPU por lote em recibos, sem confundir intervalo
com raciocínioativo. A7.d3compilações: parede{wall:.6f}s,CPU{cpu:.6f}s.
Custo da continuação C6: teto8h do adendo, sem promessa de conclusão.
Custos de assinatura sem recibo monetário permanecem desconhecidos.

ManifestoUVSHA256={sha(D/'manifest.json')}.
ManifestoA7cSHA256={sha(H/'A7c_named_remainder/manifest.json')}.
AberturaSHA256={opening}. **PróximoA8**, depoisParteC,ParteB e relatório.
'''
    write(OUT/'ENTREGA_016_A7_setor_interagente.md',report.encode())
    state=H/'CONTINUIDADE.json';j=json.loads(state.read_bytes())
    j.update(at=now.isoformat(),status='ACTIVE',previous_goal_turn='PROGRESS',next=['A8 typed gate proposal + exact-type negative probes; then ADENDO002PartC C1-C6, ORDEM015PartB and final full audit'],
        remaining_full_goal=['A8','ADENDO002 critique remaining audits C2.3/4/5 and C2.2 terminal measurement','ADENDO002 PartC C1-C6 AFTER A8','ORDEM015 PartB','Final full requirement audit and reports'],
        A7_complete_as_requested_measurement=True,A7_status=str(H/'A7_FINAL_STATUS.json'),A7d_uv_scope=result,
        newest_vector_and_arity_one=dict(vector_manifest=str(H/'bilocal_vector_euler_zerojet/manifest.json'),
            vector_coefficient='7/16 delta_ab delta_cd',coverage_manifest=str(H/'curved_coverage_before_deadline/manifest.json'),
            arity_one_manifest=str(H/'temporal_known_arity_one_terms_v2/manifest.json')),
        C23_partial_audit=str(H.parent/'ADENDO_002_CRITICAS/C23_AUDIT/manifest.json'),
        pending_orchestration='C2.3 received/accounted and gauge-invariance claim refuted; full source audit awaitsPartC.C4. C2.4 running job7f044602-7a5c-4c9a-8f59-7930175e4e93 executionde835ad4-13f0-42a9-8fea-351d7f4631fe worker90173 coordinator-owned; C2.5 FIFO. d3 not dispatched before cutoff, no dispatch in closed A7b window.',own_processes=[])
    put(state,j,True)
    append(OUT/'LEDGER_016.jsonl',json.dumps(dict(at=now.isoformat(),event='A7D_UV_TYPED_DELIVERY',target='A7.d',compile_attempts=3,
        compile_wall_seconds=wall,compile_cpu_seconds=cpu,remote_call=False,manifest_sha256=sha(D/'manifest.json')))+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7 entregue COMMEDIDA: bQ2NÃO PAGA,cobstruçãonomeada,dUVtipado11teoremas/11prints/auditorPASSA.3compilaçõesCPU{cpu:.6f}s. Não movefronteirainteragente.PróximoA8.AberturaSHA256={opening}.\n')
    print(json.dumps(dict(status=whole,next='A8',uv_manifest=str(D/'manifest.json'))),flush=True)

if __name__=='__main__':main()
