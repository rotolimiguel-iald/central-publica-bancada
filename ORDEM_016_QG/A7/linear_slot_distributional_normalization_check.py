"""Connect existing radial contacts to the linear Green insertion, without changing R."""
from pathlib import Path
from datetime import datetime, timezone
from itertools import product
import json, time
import sympy as s
import logarithmic_contact_engine as R
from full_loop_extension_engine import contact, propagator_derivative, x, z
from deliver_nonminimal_wick_and_mimo_audit import H, OUT, sha, write, put, append

D = H / 'linear_slot_distributional_normalization'

def main():
    D.mkdir(exist_ok=False)
    now = datetime.now(timezone.utc)
    sources = [Path(__file__), H/'logarithmic_contact_engine.py',
               H/'full_loop_extension_engine.py', H/'linear_slot_ward_bridge/results.json',
               H/'linear_anomaly_insertion/results.json']
    put(D/'PRE_REGISTER.json', dict(at=now.isoformat(),
        target='Connect the pre-existing R(D f)-D R(f) contacts to single-line Green normalization',
        scope='Euclidean principal singularity in four dimensions; no curved smooth remainder fixed',
        source_url='https://arxiv.org/pdf/1803.10235v3', source_equations=['158','174-180'],
        negative_control='Extending the pointwise Laplacian zero loses the entire delta source',
        sources=[dict(path=str(p), sha256=sha(p)) for p in sources],
        original_pair_prescription_changed=False, full_Q2=False))
    start = time.process_time()
    checks = []
    def eq(name, value):
        assert s.expand(value) == 0, (name, value)
        checks.append(name)

    # Independent normalization: the outward flux of grad(r^-2) through S^3_r.
    r = s.Symbol('r', positive=True)
    area = 2*s.pi**2*r**3
    flux = s.simplify(area*s.diff(r**-2, r))
    eq('Gauss flux is independent of the sphere radius', flux+4*s.pi**2)
    CE = flux
    # The angular second moment follows from O(4) symmetry and sum n_i^2=1.
    moment = s.Symbol('moment')
    moment_value = s.solve(4*moment-2*s.pi**2, moment)[0]
    for i, j in product(range(4), repeat=2):
        correction = -CE*R.contact(1,0,(i,j))
        boundary = -2*moment_value*(1 if i == j else 0)
        eq('second derivative boundary '+str((i,j)), correction-boundary)
    pointwise_lap = s.expand(sum(propagator_derivative((i,i)) for i in range(4)))
    # z represents sum x_i^2, so first reduce the rational scalar before extension.
    pointwise_lap = s.expand(pointwise_lap.subs(x[3]**2,z-sum(v*v for v in x[:3])))
    eq('pointwise Laplacian vanishes away from zero', pointwise_lap)
    source = -sum(R.contact(1,0,(i,i)) for i in range(4))
    eq('full Laplacian restores exactly one CE delta', source-1)
    assert source != 0
    checks.append('pointwise-only extension fails the Green equation')

    # A new consistency check of the connection, not a new extension algorithm:
    # C_(w,i)(f)=C_i(D_w f)+q_i C_w(f). It checks nested linear insertions.
    for size in (1,2):
        for word in product(range(4), repeat=size):
            for i in range(4):
                lhs=R.contact(1,0,word+(i,))
                rhs=contact(propagator_derivative(word),(i,))+R.Q[i]*R.contact(1,0,word)
                eq('nested derivative contact '+str(word+(i,)),lhs-rhs)
    # A derivative insertion at either endpoint has a fixed relative sign.
    for i in range(4):
        total=R.contact(1,0,(i,i))
        eq('opposite endpoint derivative '+str(i), -total-s.Rational(1,4))

    result=dict(at=datetime.now(timezone.utc).isoformat(), checks=len(checks),
        cpu_seconds=time.process_time()-start,
        principal_green_equation='Delta(1/r^2)=-4*pi^2*delta in Euclidean R^4',
        derivative_extension='D_w R(f)=R(D_w f)-CE*C_w(f), with the existing C_w',
        linear_slot_status='PRINCIPAL_DISTRIBUTIONAL_CONTACTS_COMPATIBLE',
        missing_for_full_same_family=['Curved smooth Green remainder in the same Wick realization',
            'Field independence and action Ward compatibility of all composite insertions',
            'Combination of the two measured A1 terms with the two-entry subtotal'],
        operator_statement='Identidade de ward é o operador de “=“',
        interpretation_statute='INPUT/ONTO; Ward is the typed compatibility identity, not a new unary map',
        full_Q2=False, gate_changed=False)
    put(D/'results.json',result)
    opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    report=f'''[INPUT/ONTO — correspondência do operador; DERIVED+CAS — contato principal; A7.b integral OPEN]

Fala do operador, verbatim: «Identidade de ward é o operador de “=“».
Registro de bancada, sem alteração do Atlas, do kernel ou do programa terminal.

Na leitura proposta, Ward realiza o critério de compatibilidade entre transformação
e leitura. A expressão tipada atualmente usada é shat0 T1(F)=T1(s0F+A1(F)).
Os mapas shat0 e T1 fazem operações distintas; a igualdade relaciona seus resultados.
A correção A1 não se torna nula pela nomenclatura, nem uma classe não trivial foi
demonstrada apenas por haver representante não zero. Não foi criado operador novo.

Ligação concreta aos contatos existentes: a normalização de uma entrada linear
deve usar a distribuição de Green inteira. No controle euclidiano principal,
o fluxo pela esfera S3_r dá (2pi²r³)(-2/r³)=-4pi²=CE. Logo
Delta(1/r²)=CE delta, embora a expressão pontual seja zero fora da origem.
O motor já calcula C_w=(R(D_w f)-D_w R(f))/CE. Assim
D_w R(f)=R(D_w f)-CE C_w; para w=(i,j), C_ij=-delta_ij/4.
A parcela acrescentada à extensão da derivada pontual é -pi² delta_ij delta.
Sua soma é exatamente CE delta. O controle sem contato perde a fonte inteira.

Verificadas também as composições até três derivadas:
C_(w,i)(f)=C_i(D_w f)+q_i C_w(f), em todos os índices ordenados ensaiados.
Isso conecta os contatos à normalização diferencial de uma linha, preservando
a prescrição R já registrada. Não é a soma da Ward com duas interações.
Com uma entrada linear, há no máximo uma contração cruzada; a extensão de um
produto com duas linhas não precisa ser recalculada para esta verificação.
A compatibilidade global dos produtos compostos, porém, não segue dessa contagem.

[KNOWN] Fröb, arXiv1803.10235v3, equações158 e Teorema9, permite impor a
concordância perturbativa linear por renormalização. Sua prova, eq174–180,
identifica a diferença local a remover; não afirma que qualquer prescrição radial
prévia já satisfaça todas as condições. Fonte lida nesta rodada:
https://arxiv.org/pdf/1803.10235v3 .

Ainda preservar: o resto suave curvo do Green, a mesma representação de Wick,
as duas inserções A1 e a normalização dos operadores compostos. O cálculo
presente não apaga A1=(i hbar)alpha int chi div(c), nem determina alpha físico.
Resultado: {len(checks)} controles exatos, CPU {result['cpu_seconds']}s, rc0.
Próximo ramo do mesmo A7.b: montagem de duas entradas, incluindo esses contatos
e os termos de cutoff. Q2 completa continua OPEN. Nenhuma chamada externa nova.
Abertura SHA256={opening}.
'''
    write(D/'DERIVACAO.md',report.encode('utf-8'))
    write(OUT/'ENTREGA_016_MEDIDA_Ward_igualdade_contato_linear.md',report.encode('utf-8'))
    paths=sources+[D/'PRE_REGISTER.json',D/'results.json',D/'DERIVACAO.md']
    put(D/'manifest.json',dict(at=now.isoformat(),opening_sha256=opening,
        artifacts=[dict(path=str(p),sha256=sha(p)) for p in paths],full_Q2=False,gate_changed=False))
    append(OUT/'LEDGER_016.jsonl',json.dumps(dict(at=now.isoformat(),target='A7.b',
        event='WARD_EQUALITY_OPERATOR_INPUT_AND_LINEAR_CONTACT_BRIDGE',checks=len(checks),
        cpu_seconds=result['cpu_seconds'],remote_call=False,
        manifest_sha256=sha(D/'manifest.json')),ensure_ascii=False)+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f"\n{now.isoformat()} A7.b PROGRESS: fala Ward/= registrada; contatos existentes recuperam a fonte linear principal. {len(checks)} controles, CPU {result['cpu_seconds']}s; Q2 integral OPEN. Nenhuma chamada/custo remoto novo. AberturaSHA256={opening}.\n")
    p=H/'CONTINUIDADE.json';state=json.loads(p.read_bytes())
    state.setdefault('head_history',[]).append({k:state.get(k) for k in
        ['at','previous_goal_turn','completed_this_turn','next','pending_orchestration']})
    state.update(at=now.isoformat(),previous_goal_turn='PROGRESS',completed_this_turn=[
        'Operator Ward/= correspondence preserved verbatim as INPUT/ONTO',
        'Existing radial contacts reproduce the principal single-line Green source and derivative compositions'],
        next=['Complete same-family curved/composite normalization; principal linear contact bridge now checked',
              'Assemble both A1 insertions with the measured two-entry subtotal',
              'Receive MiMo57e independent BV review; Kimi requests remain under actual quota',
              'A7b deadline20:32UTC; A7c/d,A8,PartB/final remain'])
    state['ward_equality_linear_contact_update']=dict(manifest=str(D/'manifest.json'),full_Q2=False)
    put(p,state,True)
    for a in json.loads((D/'manifest.json').read_bytes())['artifacts']:
        assert sha(Path(a['path']))==a['sha256']
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
