"""Deliver the calculated finite extension contact, preserving its scope."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,uuid
HERE=Path(__file__).resolve().parent; CHAT=HERE.parents[1];OUT=CHAT/'TUNEL/DO_CHATGPT'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,b):
    if isinstance(b,str):b=b.encode()
    if p.exists():
        old=p.read_bytes()
        if old==b:return
        bk=p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
        bk.write_bytes(old);assert bk.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b)
    assert b and t.read_bytes()==b;t.replace(p)
now=datetime.now(timezone.utc).isoformat();opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
r=json.loads((HERE/'finite_principal_contact/results.json').read_bytes())
v=json.loads((HERE/'finite_contact_angular/results.json').read_bytes())
report=f'''[DERIVED — contato finito principal de um par; REAL — dois CAS exatos; OPEN — soma causal completa]
# A7.b — contato longitudinal produzido pela extensão escolhida
Abertura SHA256 `{opening}`. UTC {now}.

**Prescrição anterior ao cálculo.** Mantida R(u)=FP_a[(1-a)mu^(2a)z^a u],
mu>0 fixo, a mesma extensão de tensor_extension. Para U2=z^-2 e D de ordem4,
defina o contato local N_D por R(DU2)-D R(U2)=C N_D(delta).
C=4i pi² em assinatura+---; C_E=-4pi² na realização euclidiana.
As identidades distribucionais são entradas analíticas previamente derivadas;
o CAS verifica os coeficientes, não constrói distribuições por amostragem.

**Derivação.** Escreva D[mu^(2a)z^(a-2)]=Σ_j c_j(a)T_j(a), onde T_j
tem numerador monomial independente de a. Como os polos são simples,

    C N_D=-Σ_j c'_j(0) Res T_j.

Isso decorre de comparar c_j(0) com c_j(a) ANTES da parte finita, e usa
Res U_n=C r_n box^(n-2)delta, r_n=-1/[4^(n-1)(n-1)!(n-2)!]. Multiplicar
por x^i age como -partial/partial q_i sobre o polinômio dos jatos de delta.
O fator(1-a) é mantido; não se escolhe um coeficiente após olhar Ward.

O resultado universal, para P(q) homogêneo de grau4, é

    N[P]=-77P/240 - q² Lap_q(P)/80 +(q²)² Lap_q²(P)/5120.

Lap_q usa a métrica dual dos índices de q. Equivalentemente, para quatro
derivadas abertas, os coeficientes de q_iq_jq_kq_l, q²Σ_6g_ijq_kq_l e
(q²)²Σ_3g_ijg_kl são {-77}/{240}, {-1}/{40}, {1}/{640}.

**Aplicação ao tensor já medido.** O polinômio P(T,H;q) da Hessiana métrica
mais laço ghost, retirado ħA0, tem coeficientes
[-61/120,-23/120,23/120,61/60,-7/10] na base

    q4 tr(TH), q4 trT trH,
    q²(trT qHq+trH qTq), q² qTHq, (qTq)(qHq).

Todas as contrações usam a métrica da assinatura. P(T,K_qv)=0 já estava
provado. Para a extensão uniforme, N[P] tem os coeficientes NOVOS

    {r['finite_contact_coefficients_over_C']}.

Assim, embora P(partial)R(U2) seja transversal, R(P(partial)U2) difere dele
pelo contato C N[P](partial)delta e NÃO é transversal sozinho. Explicitamente,

    N[P](T,K_qv)= (187/1920)q4(Tq·v)
                  +(43/960)q4 trT(q·v)
                  -(7/40)q²(qTq)(q·v).

Exemplo: q=v=e0, T=e11 dá43/960. A subtração LOCAL -C N[P](partial)delta
restaura a transversalidade desse tensor de dois pontos. É simétrica nos
dois tensores e tem quatro derivadas. Apagar esse contato antes de calculá-lo
ou inverter a subtração falha. Isto é uma diferença finita explícita entre
duas extensões, e não uma conclusão a partir do logUV sozinho.

**Normalização e limites.** No plano euclidiano, G_E²=U2/(16pi^4), e a
extensão tem mu dR(G_E²)/dmu=A0 delta, A0=1/(8pi²). Sua transformada contém
-A0 log(p²/mu²)/2. Por isso o tensor não local principal associado ao
logaritmo medido tem representante ħP(partial)U2/(16pi^4), até termos locais.
Nessa calibração, a diferença de extensões dividida por ħA0 é -2N[P], isto é,
{v['Euclidean_contact_over_hbar_A0']}.

Essa calibração euclidiana não fixa por si as fases da identidade BV causal
Lorentziana. A checagem Lorentziana abaixo verifica os índices do contato,
não uma continuação de todos os laços. A soma hc ainda inclui a inserção
h* c e seus próprios contatos; P(transversal) não permite apagá-los.
Curvatura Kq²/K², cutoffs, aridades superiores e normalização multilinear
T10/T11 continuam por conferir. Portanto não declaramos o coeficiente
completo a1 calculado, nem uma anomalia cohomológica não removível.

**Evidência.** Cálculo direto:350identidades,5negativos,rc0,
CPU{r['cpu_seconds']}s. Auditoria por OUTRA rota: resíduo como metade da
integral angular em S3 dos jatos de Taylor do teste;39checagens,2negativos,
rc0,CPU{v['cpu_seconds']}s. Reproduz os35componentes quárticos, sem usar
a regra de multiplicação de derivadas de delta do primeiro motor.
Scripts, planos, resultados e logs estão nos dois manifestos desta entrega.
Sem chamada remota nesta conta, alteração de original, kernel ou gate.
'''
rp=HERE/'finite_principal_contact/DERIVACAO_CONTATO_FINITO.md';save(rp,report)
save(OUT/'ENTREGA_016_A7b_contato_finito_principal.md',report)
for folder,script,log in [('finite_principal_contact','finite_principal_contact_check.py','finite_principal_contact_run.log'),
                         ('finite_contact_angular','finite_contact_angular_audit.py','finite_contact_angular_run.log')]:
    files=[HERE/script,HERE/log,HERE/folder/'PRE_REGISTER.json',HERE/folder/'results.json',rp,
        HERE/'metric_bubble_v2/results.json',HERE/'metric_bubble_v2/DERIVACAO_CORRIGIDA.md',
        HERE/'tensor_extension/DERIVACAO_TENSORIAL.md']
    save(HERE/folder/'manifest.json',json.dumps(dict(at=now,opening_sha256=opening,
        artifacts=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in files]),ensure_ascii=False,indent=2))
ledger=OUT/'LEDGER_016.jsonl';cpu=r['cpu_seconds']+v['cpu_seconds']
event=dict(event='A7_FINITE_PRINCIPAL_EXTENSION_CONTACT',at=now,provider='local',target='A-7.b',
    direct_checks=350,independent_checks=39,cpu_seconds=cpu,
    report_sha256=sha(rp),full_Q2=False,gate_changed=False)
save(ledger,ledger.read_bytes()+(json.dumps(event,ensure_ascii=False)+'\n').encode())
cont=HERE/'CONTINUIDADE.json';d=json.loads(cont.read_bytes())
d.update(at=now,status='ACTIVE',previous_goal_turn='PROGRESS',
    completed_this_turn=['Finite one-pair extension contact computed for quartic principal Hessian',
        '350 exact identities plus independent spherical-residue audit39 checks',
        'Explicit nonzero longitudinal local term and finite restoring subtraction derived'],
    finite_principal_contact_manifest=str(HERE/'finite_principal_contact/manifest.json'),
    finite_contact_angular_manifest=str(HERE/'finite_contact_angular/manifest.json'),
    next=['Compute finite contact for the h* c insertion and combine with Hessian contact, preserving global phases',
          'Complete curved/cutoff/multilinear prescription within A7b timebox',
          'Review queued results; do not repeat or refit coefficients'],full_ward_coefficient_computed=False)
save(cont,json.dumps(d,ensure_ascii=False,indent=2))
progress=OUT/'ENTREGA_016_PROGRESSO.md'
save(progress,progress.read_bytes()+f'\n- {now} — A7.b PROGRESSO: contato FINITO longitudinal principal calculado,350checks+5negativos e auditoria angular39+2negativos;CPU{cpu}s. Subtração local explícita, hc completo/fases/curvatura/hierarquia aindaOPEN. Abertura{opening}.\n'.encode())
print(json.dumps(dict(report=str(rp),cpu_seconds=cpu,full_Q2=False),ensure_ascii=False))
