"""Exact vector invariant reconstruction and current A7.b acceptance coverage."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,time
import sympy as s
from deliver_nonminimal_wick_and_mimo_audit import H,OUT,sha,write,put,append

def main():
    now=datetime.now(timezone.utc);start=time.process_time();D=H/'curved_coverage_before_deadline';D.mkdir(exist_ok=False)
    names=['bilocal_vector_euler_zerojet','bilocal_scalar_euler_zerojet','principal_sector_assembly',
        'temporal_ward_consistency_polarization','finite_contact_second_curvature_primitive',
        'bilocal_curved_contact_primitive','smooth_line_compatibility_v2']
    sources=[Path(__file__)];r={}
    for name in names:
        p=H/name/'results.json';r[name]=json.loads(p.read_bytes());sources.append(p)
    tablepath=H/'bilocal_vector_euler_zerojet/TABLE.json';sources.append(tablepath)
    table=json.loads(tablepath.read_bytes());checks=[]
    for key,values in table.items():
        a,b,c,d=ast.literal_eval(key)
        expected=s.Rational(7,16)*int(a==b)*int(c==d)
        for endpoint,v in enumerate(values):
            assert s.sympify(v)==expected,(key,endpoint,v);checks.append((key,endpoint))
    assert r['bilocal_vector_euler_zerojet']['endpoint_differences']==0
    assert r['principal_sector_assembly']['localized_nonzero_residual']==0
    assert not r['finite_contact_second_curvature_primitive']['actual_second_curvature_contact_measured']
    assert not r['smooth_line_compatibility_v2']['global_family_admissibility']
    coverage=[
        dict(requirement='Declared prescription before its own calculation',status='PARTIAL',
            evidence='PRE_REGISTER per batch: Rraw and R_bal explicitly different; smooth-line completion explicit',
            missing='A single fully covariant causal time-ordered family satisfying all used normalizations has not been constructed'),
        dict(requirement='Actual principal flat h/c one-loop representative including three scalar modes',status='MEASURED_IN_STATED_SECTOR',
            evidence='principal_sector_assembly/results.json',missing='Neither higher field arities nor all curved insertions'),
        dict(requirement='Inhomogeneous temporal Ward consistency at hbar and arity2',status='PARTIAL',
            evidence='General identity polarized; principal flat two sampled localized orderings0/16; odd insertion sign independently audited',
            missing='Complete same-family curved a1, a2, antifield/nonminimal and boundary-of-cutoff insertions'),
        dict(requirement='Curved Q2 representative in model087',status='NOT_COMPLETE',
            evidence='Scalar zerojet CE*K/4; vector pair CE*K*7delta_abdelta_cd/16 at both endpoints',
            missing='Tensor pair transport, derivative slots, interaction vertex contractions, K² terms and remaining nonlinear arities'),
        dict(requirement='Actual cohomology class of the complete Q2',status='NOT_ESTABLISHED',
            evidence='Principal free-BRST h/c primitive exists; earlier K/K² primitive families conditional',
            missing='Complete consistent anomaly density/cochain in the declared temporal family before assigning its class'),
        dict(requirement='Physical interacting state, QME and UV scope',status='NOT_DISCHARGED',
            evidence='No artifact in this calculation claims full_Q2 or physical state',
            missing='Outside completion of these Euclidean local pair checks; A7.d explicitly only types UV alternatives')]
    data=dict(at=now.isoformat(),checks=len(checks),cpu_seconds=time.process_time()-start,
        vector_invariant='7/16 delta_ab delta_cd',scalar_invariant='1/4',normalization='coefficient of CE*K*delta only',
        vector_scalar_coefficients_not_interchangeable=True,coverage=coverage,
        actual_cohomological_nonzero_obstruction_proved=False,
        homogeneous_cohomology_warning='The isolated arity2 coefficient is not assumed s0-closed: a1 and odd-insertion terms occur in the polarized WZ identity',
        counterterm_families_to_control=['Same-family natural curved extension of local contacts',
            'Quadratic h/h Hessian N4+K*N2+K²*N0 with selfadjointness and BRST image checked',
            'Ghost/antifield/nonminimal and nonlinear-arity counterterms fixed together with T1/T2',
            'Cutoff-derivative terms required by the inhomogeneous temporal Ward identity'],
        no_new_physical_counterterm_selected=True,timebox_exhausted=now>=datetime(2026,9,25,20,32,tzinfo=timezone.utc),
        no_c_branch_started=True,full_Q2=False,gate_changed=False)
    put(D/'results.json',data);opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    note=f'''[DERIVED+CAS — forma invariante vetorial e cobertura real do A7.b]

Os512valores (256componentes x2pontas) recompõem exatamente
7/16 delta_ab delta_cd no coeficiente de CE*K*delta. O escalar dá1/4.
São pares com inserção de Euler, antes de sinais de Wick e vértices;
não se substitui um pelo outro nem se soma como anomalia completa.

O termo principal plano Einstein+3sigma tem primitiva livre e consistência
localizada medida. A prescrição curva já tem termos concretos e controles,
mas o pacote temporal completo ainda não está construído. O candidato
de segunda curvatura anterior conserva coeficientes u,v NÃO medidos.

A condição de aridade2 é inhomogênea: contém a1, anticolchetes e
inserções ímpares. Portanto não se pode atribuir uma classe de H(s0)
ao a2 isolado sem esses termos. Para uma densidade local completa,
a interpretação em H_loc^(1,4)(s|d) exige primeiro a consistência
s a + d b=0 no complexo e nas hipóteses declaradas. Não demonstramos
uma classe não nula nem a nulidade da classe completa.

Famílias ainda a controlar: a mesma extensão covariante dos contatos;
N4+K*N2+K²*N0; setores fantasma/antifield/não mínimo e aridades
não lineares; termos de derivadas dos cortes. A evidência e o alcance
de cada requisito estão em results.json, sem converter presença de
arquivo em conclusão. Nenhum contratermo físico novo foi escolhido.

Auditoria preparada dentro do A7.b, antes de seu encerramento;
A7.c não iniciado por este arquivo. Prazo20:32UTC mantido.
CPU{data['cpu_seconds']}s,rc0. AberturaSHA256={opening}.
'''
    write(D/'DERIVACAO.md',note.encode());write(OUT/'ENTREGA_016_MEDIDA_cobertura_curva_A7b.md',note.encode())
    put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'results.json',D/'DERIVACAO.md']],full_Q2=False))
    append(OUT/'LEDGER_016.jsonl',json.dumps(dict(at=now.isoformat(),event='CURVED_COVERAGE_BEFORE_DEADLINE',target='A7.b',checks=len(checks),cpu_seconds=data['cpu_seconds'],remote_call=False,manifest_sha256=sha(D/'manifest.json')))+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7.b:512componentesconfirmamforma vetorial7/16deltaab*deltacd; cobertura completaQ2 continua NÃO PAGA, classe totalnãoatribuída. CPU{data["cpu_seconds"]}s.AberturaSHA256={opening}.\n')
    print(json.dumps(dict(checks=len(checks),cpu_seconds=data['cpu_seconds'],deadline_exhausted=data['timebox_exhausted'])),flush=True)

if __name__=='__main__':main()
