"""Counterexample to gauge-independent triviality asserted by external C2.3."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time
import sympy as s
from deliver_nonminimal_wick_and_mimo_audit import H,OUT,BASE,sha,write,put,append

def main():
    now=datetime.now(timezone.utc);cpu=time.process_time();root=H.parent
    D=root/'ADENDO_002_CRITICAS/C23_AUDIT';D.mkdir(exist_ok=False)
    src=BASE/'state/handoffs/5cd7b089-26d0-415d-91d3-943bf00dead1_delivery.json'
    j=json.loads(src.read_bytes())['job'];e=j['execution'];r=e['result'];assert e['status']=='result_ready'
    write(D/'KIMI_ORIGINAL.md',r['text'].encode())
    put(D/'RECEIPT.json',dict(request_id=j['request_id'],job_id=j['id'],execution_task_id=e['id'],
        source_sha256=sha(src),prompt_sha256=hashlib.sha256(j['prompt'].encode()).hexdigest(),
        response_sha256=sha(D/'KIMI_ORIGINAL.md'),usage=r['usage'],cost_estimate_usd=r.get('cost_estimate_usd'),
        cost_unknown_not_zero=r.get('cost_estimate_usd') is None,canonical_memory=r.get('canonical_memory')))
    theorem=root/'A3/IsometricCocycleSpectrum_v2.lean';delivery=OUT/'ENTREGA_016_A3_H2_par_fisico.md'
    text=theorem.read_text('utf-8');assert '{E : Type*}' in text and '(E →ₗᵢ[ℂ] E)' in text
    assert 'LinearIsometry.norm_map' in text
    a,u,v,t=s.symbols('a u v t',real=True)
    # U_s f(t)=f(t-s); change frame by (V_chi f)(t)=exp(i chi(t)) f(t).
    chi=lambda z:a*z
    phase=lambda z,w:s.expand(chi(w)-chi(w-z))
    checks=[]
    def eq(name,left,right=0):assert s.simplify(left-right)==0,(name,left,right);checks.append(name)
    eq('regauged phase is a*s',phase(u,t),a*u)
    eq('cocycle law',phase(u+v,t),phase(u,t)+phase(v,t-u))
    eq('zero group element',phase(0,t),0)
    eq('inverse group element',phase(-u,t-u),-phase(u,t))
    eq('unit modulus',s.exp(s.I*phase(u,t))*s.conjugate(s.exp(s.I*phase(u,t))),1)
    eq('nontrivial value at pi',s.exp(s.I*phase(u,t)).subs({a:1,u:s.pi}),-1)
    assert s.exp(s.I*phase(u,t)).subs({a:1,u:s.pi})!=1
    eq('unitary conjugation of translation, test exponential',
        s.exp(s.I*chi(t))*s.exp(-s.I*chi(t-u))*s.exp(s.I*v*(t-u)),
        s.exp(s.I*phase(u,t))*s.exp(s.I*v*(t-u)))
    result=dict(at=now.isoformat(),checks=len(checks),cpu_seconds=time.process_time()-cpu,
        counterexample='C_s(t)=1, chi(t)=a*t => Cprime_s(t)=exp(i*a*s), Cprime_pi=-1 for a=1',
        accepted=['Generic fiber/isometric norm theorem does not require a trivial cocycle',
            'Concrete measurable physical helicity representation is not supplied by the no-eigen theorem',
            'Two scalar copies do not establish helicities +/-1'],
        rejected=['Helicity phase under wedge boost equals1 in every trivialization',
            'Normalizing the little group or commuting K1/J1 suffices to establish that gauge-independent claim',
            'The modular H2 bridge already closes from the orbital shift alone'],
        reason='A change of section uses endpoint-dependent factors g(momentum) and g(transformed momentum), not merely conjugation by one fixed element',
        physical_cocycle_constructed=False,physical_boost_restriction_trivializable_proved=False,
        full_critique_source_audit=False,scope='Decisive elementary gauge counterexample plus targeted complete-source reading; remainder retained for PartC.C4',
        sources_compiled_now=False,full_Q2=False,gate_changed=False)
    put(D/'AUDIT.json',result);opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    note=f'''[DERIVED+CAS — C2.3: contraexemplo à alegada trivialidade em qualquer calibre]

A crítica Kimi acerta: o teorema isometric_fiber_shift_no_eigen é genérico
na fibra e usa apenas preservação da norma. Não exige trivializar o cociclo.
A representação física mensurável concreta continua um dado a construir.

Mas sua alegação central «fase1 em qualquer trivialização» é falsa.
Se U_s f(t)=f(t-s) e V_chi f(t)=exp(i chi(t))f(t), então
V_chi U_s V_chi^-1 f(t)=exp(i[chi(t)-chi(t-s)]) f(t-s).
Escolha chi(t)=a*t: C'_s=exp(i*a*s). É um cociclo unitário suave;
em a=1,s=pi vale-1, embora o cociclo inicial fosse1. Lei de grupo,
inverso e módulo foram conferidos simbolicamente em{len(checks)}controles.

A mudança de seção compara dois pontos da órbita. Não é conjugação
interna por um único elemento; a comutatividade do quociente SO(2)
não remove o cobordo entre esses pontos. Logo o lema proposto E3
exige uma trivialização específica e prova própria; não é automático.
Também se deve formular fases como U(1), ou controlar a escolha do
argumento módulo2pi, antes de exigir uma lei aditiva real global.

Outra promoção recusada: a entregaA3 explicitamente não constrói rede,
vácuo separante nem identificaçãoBW. O shift orbital e sua covariância
não fecham H2 por si. Isto não reabre nem invalida os lemas orbitais pagos.
Não provamos aqui se o cociclo físico admite calibre trivial nesse subgrupo;
refutamos a afirmação universal e preservamos a questão física para C4.

Resposta integral e recibo preservados; auditoria completa de todas as
fontesC2.3 ainda não alegada. Uso{r['usage']}; custoassinatura desconhecido.
CPUlocal{result['cpu_seconds']}s;rc0; sem recompilar/kernel/gate.
AberturaSHA256={opening}.
'''
    write(D/'CONFRONTO.md',note.encode());write(OUT/'ENTREGA_016_MEDIDA_C23_calibre_do_cociclo.md',note.encode())
    refs=[src,theorem,delivery,Path(__file__),D/'KIMI_ORIGINAL.md',D/'RECEIPT.json',D/'AUDIT.json',D/'CONFRONTO.md']
    put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in refs],full_Q2=False))
    ledger=OUT/'LEDGER_016.jsonl';rows=[json.loads(v) for v in ledger.read_text('utf-8').splitlines() if v.strip()]
    assert not any(e['id'] in json.dumps(v) and 'completion_tokens' in json.dumps(v) for v in rows),'Already accounted'
    append(ledger,json.dumps(dict(at=now.isoformat(),event='C23_CRITIQUE_PARTIAL_AUDIT_GAUGE_COUNTEREXAMPLE',target='ADENDO002.C2.3',
        provider='kimi',request_id=j['request_id'],job_id=j['id'],execution_task_id=e['id'],usage=r['usage'],
        cost_estimate_usd=None,cost_unknown_not_zero=True,source_sha256=sha(src),manifest_sha256=sha(D/'manifest.json'),
        audit_cpu_seconds=result['cpu_seconds']))+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} C2.3 recebida e contabilizada; contraexemploexato refuta fase1emqualquertrivialização;H2nãopromovido. {len(checks)}controles CPU{result["cpu_seconds"]}s,347109tokensKimi custo desconhecido. AuditoriarestanteemC4.AberturaSHA256={opening}.\n')
    print(json.dumps(dict(checks=len(checks),cpu_seconds=result['cpu_seconds'],manifest=str(D/'manifest.json'))),flush=True)

if __name__=='__main__':main()
