"""Close the elapsed A7.b timebox and document the precise A7.c remainder."""
from pathlib import Path
from datetime import datetime,timezone
import json,time
from deliver_nonminimal_wick_and_mimo_audit import H,OUT,sha,write,put,append

def main():
    now=datetime.now(timezone.utc);deadline=datetime(2026,9,25,20,32,tzinfo=timezone.utc)
    if now<deadline:
        print(json.dumps(dict(status='TOO_EARLY_NO_MUTATION',now=now.isoformat(),deadline=deadline.isoformat())));return
    cpu=time.process_time();D=H/'A7c_named_remainder';D.mkdir(exist_ok=False)
    names=['principal_sector_assembly','temporal_ward_consistency_polarization',
        'temporal_known_arity_one_terms_v2','odd_insertion_ward_sign_audit',
        'bilocal_scalar_euler_zerojet','bilocal_vector_euler_zerojet',
        'curved_coverage_before_deadline','smooth_line_compatibility_v2',
        'finite_contact_second_curvature_primitive']
    verified=[];sources=[Path(__file__),H/'A7a_SOURCE_REGISTER.json'];evidence={}
    for name in names:
        rp=H/name/'results.json';mp=H/name/'manifest.json'
        r=json.loads(rp.read_bytes());m=json.loads(mp.read_bytes());sources.extend([rp,mp]);evidence[name]=r
        for item in m['artifacts']:
            assert sha(Path(item['path']))==item['sha256'];verified.append(item)
    start=json.loads((H/'A7a_SOURCE_REGISTER.json').read_bytes())['at']
    assert not evidence['smooth_line_compatibility_v2']['global_family_admissibility']
    assert not evidence['finite_contact_second_curvature_primitive']['actual_second_curvature_contact_measured']
    assert evidence['principal_sector_assembly']['localized_nonzero_residual']==0
    assert evidence['bilocal_vector_euler_zerojet']['endpoint_differences']==0
    assert evidence['temporal_known_arity_one_terms_v2']['odd_input_convention_corrected']
    hours_to_cutoff=(deadline-datetime.fromisoformat(start)).total_seconds()/3600
    hypotheses=[
        dict(name='A7_T2_CURVED_NORMALIZATION_PENDING',order='hbar^1, temporal arity2',
            missing='One covariant causal T1/T2 family simultaneously realizing the scalar, vector, tensor, smooth-line and derivative normalizations',
            evidence='Rraw and R_bal were kept separate; naive smooth-line failure repaired only on a subfamily',
            kind='Construction/compatibility hypothesis, not a nonzero cohomology theorem'),
        dict(name='A7_Q2_CURVED_FULL_REPRESENTATIVE_PENDING',order='hbar^1; h/c derivative filtration 5, K*3, K²*1 in the stated truncated sector',
            missing='Remaining tensor kernels, derivative slots, vertex contractions, antifield/nonminimal and nonlinear/cutoff terms in that SAME family',
            evidence='Flat hc graph sum and scalar/vector curvature zerojets computed; K² coefficients still symbolic',
            kind='Missing measured representative'),
        dict(name='A7_WZ_COMPLETE_AND_CLASS_PENDING',order='hbar^1 with temporal arities1 and2 coupled',
            missing='Full polarized consistency including both mixed antibrackets, a1 of bracket and both odd classical insertions',
            evidence='General identity and sampled principal flat consistency verified; corrected curved arity1 comparison known',
            kind='Membership and class of the full consistent anomaly are not yet established'),
        dict(name='A7_ADMISSIBLE_COUNTERTERM_FAMILY_PENDING',order='hbar^1 local finite normalization, all sectors used above',
            missing='Real natural covariant counterterms compatible with causal factorization, smooth multiplication, field derivatives and chosen T1/T2',
            evidence='Formal free h/h primitive N4+K*N2+K²*N0 is not by itself this complete family',
            kind='Compatibility of counterterms, not choice of a fitted physical parameter')]
    result=dict(at=now.isoformat(),A7b=dict(status='MEDIDA_NOT_PAID_FULL_Q2',start_anchor=start,
        start_anchor_description='Timestamp of A7a register retained as conservative opening anchor; not a stopwatch of active reasoning',
        declared_deadline=deadline.isoformat(),closed_at=now.isoformat(),hours_anchor_to_deadline=hours_to_cutoff,
        acceptance_met=False,new_A7b_calculation_after_deadline=False),
        A7c=dict(status='NAMED_REMAINDER_DOCUMENTED',hypotheses=hypotheses,
            class_scope='Candidate complete local anomaly: H_loc^(ghost1,form4)(s|d) after s*a+d*b=0; no class assigned to isolated inhomogeneous arity2 term',
            cohomological_nonzero_obstruction_proved=False,complete_class_zero_proved=False,
            counterterm_hc_symbol='N4+K*N2+K²*N0, orders4/2/0; conditional formal primitives only outside the measured flat sector',
            remaining_cost='PartC.C6 allows8h additional bounded work; completion beyond that is not estimated or promised',
            scientific_scope='Euclidean auxiliary/local truncated spaceform087 with sigma constant, not the physical interacting pair'),
        final_values=dict(flat=evidence['principal_sector_assembly']['per_order_coefficients'],
            scalar_curvature='CE*K/4',vector_curvature='7*CE*K*delta_ab*delta_cd/16',
            curved_zerojet_is_full_loop=False),
        verified_manifest_entries=len(verified),unique_verified_artifacts=len({v['path'] for v in verified}),
        next='A7.d typed UV alternatives, then A8, ADENDO002PartC, ORDEM015PartB, final audit',
        cpu_seconds=time.process_time()-cpu,full_Q2=False,gate_changed=False,originals_modified=False)
    put(D/'results.json',result);opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    note=f'''[DERIVED/OPEN — A7.b encerrado por prazo; A7.c com lacunas nomeadas]

**Resultado:** Q2 curva completa NÃO PAGA. Prazo declarado20:32UTC
atingido; encerramento registrado em{now.isoformat()}. Nenhum novo cálculo
A7.b é iniciado depois do prazo. O intervalo entre o registro de abertura
e o corte foi{hours_to_cutoff:.6f}h; não é medição de raciocínio ativo.

**O que foi calculado:** representante principal plano Einstein+3sigma,
com coeficientes por ordem(-629/6144,-151/6144,167/1536), primitiva livre
e consistência localizada0/16 nos jatos testados. Na curvatura: contatos
escalares CE*K/4 e vetoriais7CE*K*delta_abdelta_cd/16, coincidentes nas
duas pontas com conexões/densidade. Estes últimos não são laços completos.
As falhas, convenções ímpares e correções de sinal permanecem custodiadas.

**Obstrução operacional nomeada, não uma classe não nula provada:**
1. A7_T2_CURVED_NORMALIZATION_PENDING: falta uma família temporal
causal covariante conjunta. A compatibilidade suave foi paga apenas
na subfamília testada. Rraw e R_bal não podem ser misturados.
2. A7_Q2_CURVED_FULL_REPRESENTATIVE_PENDING: ordemhbar, aridade temporal2;
no recorte h/c, ordens de derivada5,K*3,K²*1. Faltam os termos tensoriais,
jatos adicionais, contrações de vértices e restantes setores/inserções.
3. A7_WZ_COMPLETE_AND_CLASS_PENDING: a equação de aridade2 contém fontes
de aridade1 e inserções ímpares. O a2 isolado não é declarado s0-fechado.
Para o representante local completo, o espaço candidato é
H_loc^(1,4)(s|d), condicionado a s*a+d*b=0. Ainda não há classe completa
calculada a declarar zero ou não zero. A primitiva plana não paga isso.
4. A7_ADMISSIBLE_COUNTERTERM_FAMILY_PENDING: N4+K*N2+K²*N0 fornece
o ansatz quadrático formal de ordens4,2,0. Faltam sua compatibilidade
na família real e os termos fantasma/antifield/não mínimo, não lineares
e de derivadas dos cortes. CoeficientesK² u,v anteriores continuam NÃO
medidos; resolver sua equação linear condicional não os mede.

**Aceitação:** o ramo principal não satisfez a aceitação integral. O recuo
entrega a localização precisa do que falta, sem declarar impossibilidade
ou inexistência da teoria. A gerência audita. Não há estado interagente
físico produzido nem alteração de interacting_quantum_state_BRST_QME_
anomalies_and_UV_scope. Breuer finito não é usado como respostaUV.

**Recursos:** cada lote conserva CPU/comando/log no seu recibo;
esta conferênciaCPU{result['cpu_seconds']}s. Custos desconhecidos de
assinatura e chamadas sem resposta não viram zero. O adendo admite
mais8h no C6 posterior ao A8; isso é teto de trabalho, não promessa de
conclusão. Não se encomenda aqui uma extensão ilimitada do A7.b.

**Próximo:** A7.d (UV tipado), A8 (proposta), ParteC e ParteB da missão.
AberturaSHA256={opening}.
'''
    write(D/'DERIVACAO.md',note.encode());write(OUT/'ENTREGA_016_MEDIDA_A7b_timebox_e_A7c.md',note.encode())
    put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'results.json',D/'DERIVACAO.md']],full_Q2=False))
    state=H/'CONTINUIDADE.json';j=json.loads(state.read_bytes())
    j.update(at=now.isoformat(),status='ACTIVE',previous_goal_turn='PROGRESS',A7b_timebox_exhausted=True,
        next=['A7.d ALWAYS: type two UV routes as structures with named hypotheses; check existing kernel before coding; no assertion of solution',
            'A8 typed gate proposal and negative probes; then ADENDO002PartC C1-C6, ORDEM015PartB and full final audit'],
        A7c_named_remainder=dict(manifest=str(D/'manifest.json'),status='NAMED_REMAINDER_DOCUMENTED'),own_processes=[])
    put(state,j,True)
    append(OUT/'LEDGER_016.jsonl',json.dumps(dict(at=now.isoformat(),event='A7B_TIMEBOX_CLOSED_A7C_NAMED',target='A7.c',remote_call=False,
        cpu_seconds=result['cpu_seconds'],manifest_sha256=sha(D/'manifest.json'),full_Q2=False))+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7.b MEDIDA/NÃO PAGO Q2inteira, prazo20:32encerrado; A7.c lacunasnomeadas (famíliatemporal,representante,WZ/classe,contratermos), semclassenãonulaprovada. ConferênciaCPU{result["cpu_seconds"]}s. PróximoA7.d. AberturaSHA256={opening}.\n')
    print(json.dumps(dict(status='A7B_CLOSED_A7C_NAMED',next='A7.d',manifest=str(D/'manifest.json'))),flush=True)

if __name__=='__main__':main()
