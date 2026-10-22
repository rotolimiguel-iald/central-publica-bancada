"""Complete the C1 metadata contract from frozen sources and existing numbers."""
from pathlib import Path
from fractions import Fraction as F
from datetime import datetime, timezone
import hashlib
import json
from fetch_public import atomic_json

ROOT=Path(__file__).resolve().parent


def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        while block:=stream.read(8*1024*1024):
            h.update(block)
    return h.hexdigest()


def anchor(name, phrase):
    path=ROOT/name
    lines=path.read_text(encoding='utf-8-sig').splitlines()
    hits=[i+1 for i,line in enumerate(lines) if phrase in line]
    if not hits:
        raise ValueError('Missing source anchor: '+phrase)
    return dict(path=name,sha256=sha(path),lines=hits,matching_text=phrase)


def main():
    output=ROOT/'C1_LEITURAS.json'
    if output.exists():
        raise FileExistsError('Preserve completed contract')
    data=json.loads((ROOT/'C1_TABLES.json').read_bytes())
    c0=json.loads((ROOT/'C0_C3_checks.json').read_bytes())
    clock=json.loads((ROOT/'cache/casa/um_absoluto.json').read_bytes())['core']['clock_test_result_v369']
    refs={
        'quadratic':anchor('cache/casa/um.py','"law": "Gamma_omega = (1/2) beta tau_star omega^2'),
        'legacy':anchor('cache/casa/ringdown_dephasing_v2.py','delta_B = -0.5 * BETA * gm'),
        'root':anchor('cache/casa/um.py','def _verb_L(ONE):'),
        'root_offset':anchor('cache/casa/um.py','so\' coincide com kbar = 1/4'),
        'linear':anchor('cache/casa/NoFullWitness.lean','e^{−tβ·gap} < 1'),
        'FP5':anchor('cache/casa/TheHorizonRate.lean','structure HorizonRateWitness'),
        'FP5_scope':anchor('cache/casa/TheHorizonRate.lean','κ = F(α, β, θ_M, …)'),
        'partition':anchor('cache/casa/um.py','"partition_declared": ("MODULAR_LAB_BRIDGE_OPEN'),
        'own_derivation':anchor('C2_MAPEAMENTO_ANALITICO.md','## 5. Massa, spin e distância'),
    }
    simple_excluded=clock['root_law']['kbar_zero_excluded']
    rest_excluded=clock['root_law']['kbar_rest_mass_excluded']
    linear_rate=2*clock['root_law']['kbar_zero_Gamma_per_s']
    if not linear_rate>clock['root_law']['Gamma_ub_Sr_95_per_s']:
        raise ValueError('Universal linear comparison failed')
    definitions=[
      ('R-A','H=hbar*omega*N; K=tau_star*H/hbar; L_phys=sqrt(beta/tau_star)*K',
       'tau_star,src=t_P; tau_star,det=(1+z)*t_P','INPUT_PRINCIPLED_IDENTIFICATION',
       'beta*(1+z)*t_P*omega^2/2','EXISTING_QUADRATIC_LAW__EFFECTIVE_QNM_BRIDGE_INPUT',
       ['quadratic','legacy'],None,'PARTITION_DEPENDENT: v369 P1 not excluded; P2 light-mode interpretation excluded. No universal verdict from ringdown alone.'),
      ('R-B','H=hbar*omega*N; K=tM*H/hbar; L_phys=sqrt(beta/tM)*K',
       'tau_star,src=G*M_src/c^3; tau_star,det=tM','INPUT_SOURCE_MASS_CLOCK',
       'beta*w(chi)^2/(2*tM)','EXISTING_V346_BRANCH__NOT_DERIVED_CLOCK',
       ['quadratic','legacy'],None,'A source-dependent mass clock is not one universal constant. v369 G*m_atom/c^3 is invisible; G*M_Earth/c^3 is excluded. Reusing a BH mass clock in an atom would be a different, excluded common-clock assumption.'),
      ('R-MOD','K=(2*pi/kappa)*(omega-m*Omega_H)*N+log(Z); d rho/ds=-(beta/2)[K,[K,rho]]',
       'ds/dt=kappa/(2*pi), with Kerr kappa and positive corotating gap','CONJECTURE_KMS_OSCILLATOR_IDENTIFICATION',
       'pi*beta*(omega-m*Omega_H)^2/kappa','NEW_MANAGEMENT_HYPOTHESIS__NOT_TGL_CANON',
       ['FP5','own_derivation'],None,'Not a universal Unruh-g identification. Extension to arbitrary accelerated matter is an additional hypothesis; v369 excludes its terrestrial-clock analogue. The finite KMS model is not a physical global Kerr-state construction.'),
      ('R-RAIZ-0','K=tau_star*omega*N>=0; L_phys=sqrt(beta/tau_star)*sqrt(K); coherence 0 to 1',
       's=t/tau_star; tau_star cancels from the positive-root gap','INPUT_POSITIVE_GENERATOR_AND_VACUUM_COHERENCE',
       'beta*omega/2','FINITE_ROOT_FORM_CANON__OSCILLATOR_READOUT_CONDITIONAL',
       ['root','root_offset'],simple_excluded,'EXCLUDED_IF_UNIVERSAL to the measured Sr atomic transition, as recorded in v369. Does not by itself exclude a BH-only partition or a macroscopic coherent state.'),
      ('R-RAIZ-EP4','K=tau_star*(omega0+omega*N)>=0; L_phys=sqrt(beta/tau_star)*sqrt(K)',
       'omega0=1/[4*t_P*(1+z)] from an E_P/4 source offset','INPUT_BACKGROUND_E_P_OVER_4',
       'beta*omega^2/[2*(sqrt(omega0+omega)+sqrt(omega0))^2]',
       'EXISTING_V369_OFFSET_RECONCILIATION__PHYSICAL_IDENTIFICATION_INPUT',
       ['root','root_offset'],False,'For the atomic matter readout in v369, the Planckian quadratic limit is not excluded. This does not decide the separate light-mode P2 partition.'),
      ('R-RAIZ-REST','Same positive-root generator with source-rest-energy background',
       'omega0=M_src*c^2/[hbar*(1+z)]','CONJECTURE_REMNANT_REST_OFFSET',
       'beta*omega^2/[2*(sqrt(omega0+omega)+sqrt(omega0))^2]',
       'ATOMIC_OFFSET_TEST_CANON__REMNANT_TRANSPOSITION_NEW',
       ['root','root_offset'],rest_excluded,'EXCLUDED_IF_UNIVERSAL using the rest energy of each atomic system, recorded in v369. The BH rest-energy offset is a distinct, explicitly conditional transposition.'),
      ('R-RAIZ-COHERENT','Positive-root generator of N on a coherent state with mean occupation Nbar',
       'Root clock cancels; Nbar=E_mode/(hbar*omega_src) needs an excitation model','CONJECTURE_OCCUPATION_AND_READOUT',
       'Gamma_initial=(beta*omega/2)*E_Poisson[1/(sqrt(n+1)+sqrt(n))^2] ~ beta*omega/(8*Nbar)',
       'NEW_COHERENT_READOUT_OF_EXISTING_ROOT_FORM',
       ['root','own_derivation'],None,'No universal exclusion follows from the 0-to-1 atomic test without specifying occupation and observable. Nbar=10^78 is a scenario, not a measured source energy.'),
      ('R-LIN','Schur generator D(rho_nm)=-beta*omega*abs(n-m)*rho_nm; Cauchy phase representation',
       'Physical spectral gap omega*abs(n-m); coefficient 1 is a bridge assumption','CONJECTURE_LINEAR_GAP_PHYSICAL_BRIDGE',
       'beta*omega','CANON_LINEAR_GAP_COMMENT__PHYSICAL_QNM_BRIDGE_NEW',
       ['linear'],True,'DERIVED conditional exclusion if the coefficient-1 linear law is universal on Sr: rate is twice the already-excluded root vacuum rate. This is not a new clock measurement.'),
      ('R-GLOBAL','Common total-Hamiltonian time noise on system AND reference; relational observable commuting with total H',
       'Same time noise in system/reference; cancellation is conditional','INPUT_RELATIONAL_PARTITION',
       'Gamma_relative=0','V369_P3_CONDITIONAL_NO_LOCAL_OBSERVABLE',
       ['partition'],None,'No local observable under the declared cancellation assumptions, hence no local exclusion. Not a statement that every measurement is insensitive to global dephasing.'),
      ('R-PROP','Independent local quadratic time noise on propagated spectral components in FLRW',
       'Local source/rest clock t_P along the path; FLRW time-redshift relation','CONJECTURE_PROPAGATION_MODEL',
       'Xi=(beta*t_P*omega_obs^2/2)*integral_0^z (1+zprime)/H(zprime) dzprime',
       'NEW_PROPAGATION_TRANSPOSITION__NOT_A_RINGDOWN_RATE',
       ['own_derivation'],None,'Atomic limits bound the universal clock conditionally; they do not fix spatial noise correlations or the propagation readout. Source-mass clock over the whole path would be a further assumption.'),
    ]
    # Independent dimensions expressed as powers of seconds. Beta, N and w are dimensionless.
    unit_exponents={'R-A':F(1)+2*F(-1),'R-B':-F(1),'R-MOD':2*F(-1)-F(-1),
        'R-RAIZ-0':F(-1),'R-RAIZ-EP4':2*F(-1)-2*(F(-1)/2),
        'R-RAIZ-REST':2*F(-1)-2*(F(-1)/2),'R-RAIZ-COHERENT':F(-1),
        'R-LIN':F(-1),'R-GLOBAL':F(-1),'R-PROP':F(1)+2*F(-1)+F(1)}
    rows=[]
    for reading,operator,clock_text,clock_status,formula,canonical,sourcekeys,excluded,exclusion_scope in definitions:
        exp=unit_exponents[reading]
        if exp!=(0 if reading=='R-PROP' else -1):
            raise ValueError('Incorrect dimensional exponent: '+reading)
        measured=[]
        for r in data['rows']:
            if r['prediction']['reading']!=reading:
                continue
            p=r['prediction']
            measured.append(dict(event=r['event'],input_reference=r['inputs']['source'],
                gamma_per_s=p['gamma_per_s'],gamma_over_omega=p['gamma_over_omega'],
                x=None if reading=='R-RAIZ-COHERENT' else p['x'],delta_tau=p.get('delta_tau_ensemble_exact'),
                type='INITIAL_SLOPE_ONLY' if reading=='R-RAIZ-COHERENT' else 'ENSEMBLE_ADDITIVE_RATE'))
        if reading!='R-PROP' and len(measured)!=2:
            raise ValueError('Missing two-event measurements: '+reading)
        rows.append(dict(reading=reading,operator=operator,clock=clock_text,clock_status=clock_status,
            rate_or_spectral_exponent=formula,canonical_scope=canonical,sources=[refs[k] for k in sourcekeys],
            compatible_with_FP5=True,FP5_scope='No kappa or tau_star inferred from alpha/beta; physical scale supplied, or absent. This is compliance with the construction rule, not a compiled theorem about this physical identification.',
            units=dict(seconds_power=int(exp),quantity='dimensionless spectral exponent' if reading=='R-PROP' else 'rate in inverse seconds'),
            distance_dependence='Via z(D) and path integral; not assigned a local ringdown x' if reading=='R-PROP' else 'No independent D dependence in local rate; D enters received amplitude/SNR and z(D) in frame conversion',
            excluded_if_universal=excluded,exclusion_scope=exclusion_scope,
            measurements=measured,propagation_example=data['propagation_example'] if reading=='R-PROP' else None,
            relation_to_operator_16Sep=None,physical_selection=None))
    result=dict(status='C1_CONTRACT_COMPLETED_WITH_CONDITIONAL_STATUTES',created_utc=datetime.now(timezone.utc).isoformat(),
        rows=rows,source_references=refs,FP5_source=refs['FP5'],hypothesis_selected=False,
        clock_evidence=dict(path='cache/casa/um_absoluto.json',sha256=sha(ROOT/'cache/casa/um_absoluto.json'),
            key='core.clock_test_result_v369',root_law=clock['root_law'],alternatives=clock['tau_star_alternatives'],
            linear_universal_Sr_rate_per_s=linear_rate,linear_rate_is_new_measurement=False),
        numerical_source=dict(path='C1_TABLES.json',sha256=sha(ROOT/'C1_TABLES.json')),
        limits=['Null universal flag means not decidable without the stated partition; it never means false.',
            'Propagation Xi and coherent initial slope are not exponential ringdown predictions.',
            'Source program is a frozen read-only copy; presence of a Lean declaration does not certify a new compilation.',
            'Kerr KMS identification is conditional; primary Kay-Wald full text has not been read in this task.'],
        generator_sha256=sha(Path(__file__)))
    atomic_json(output,result)
    text=['[DERIVED condicional; INPUT/CONJECTURE por leitura; REAL na recuperação dos números e fontes]',
          '', '# C1 — contrato completo das leituras', '',
          'Complemento aditivo: `C1_LEITURAS_E_RELOGIOS.md` explica as derivações; `C1_TABLES.json` contém os números originais. Nenhuma leitura foi selecionada. Não se repetiu a estimação nem se alterou o programa canônico.',
          '', 'As colunas de relação com as falas do operador e de escolha física permanecem vazias (`null`), conforme a ordem. `excluded_if_universal=null` significa indecidível sem a partição explícita, nunca “não excluído”. Todos os hashes abaixo foram lidos nesta execução.',
          '', '| Leitura | Operador / relógio | Fonte e estatuto | Universalidade | FP-5 / unidade |',
          '|---|---|---|---|---|']
    for r in rows:
        sources='; '.join(f'{s["path"]}:{s["lines"][0]}' for s in r['sources'])
        cells=[r['reading'],r['operator']+'; '+r['clock'],r['canonical_scope']+'; '+r['clock_status']+'; '+sources,
               str(r['excluded_if_universal'])+': '+r['exclusion_scope'],
               'Compatível sob escala fornecida; s^'+str(r['units']['seconds_power'])]
        text.append('| '+' | '.join(c.replace('|','&#124;') for c in cells)+' |')
    text += ['', '## Medidas já executadas', '', '| Leitura | Evento | Gamma (s^-1) | Gamma/omega | x | delta_tau | Tipo |',
             '|---|---|---:|---:|---:|---:|---|']
    for r in rows:
        for m in r['measurements']:
            fmt=lambda value:'N/A' if value is None else f'{value:.9g}'
            text.append('| '+' | '.join([r['reading'],m['event'],fmt(m['gamma_per_s']),fmt(m['gamma_over_omega']),fmt(m['x']),fmt(m['delta_tau']),m['type']])+' |')
    text += ['', 'R-PROP: Xi='+str(data['propagation_example']['Xi'])+' no FLRW ilustrativo dos insumos. Não se declara x nem delta_tau de ringdown. Distância, redshift e hipóteses estão no JSON.',
             '', '## Limites da conclusão', '',
             'A regra FP-5 é respeitada porque nenhuma escala é inferida de alpha/beta. Isso não identifica o relógio físico. A realização modular finita prova a taxa condicional, não que um estado global de Kerr tenha sido construído. A leitura R-LIN usa um gerador de Schur/Cauchy, não um único salto raiz disfarçado. A distinção das leis permanece explícita.',
             'Os testes atômicos são resultados da v369 na partição declarada; não são uma nova medição nem autorização para transportar exclusões entre sistemas sem a hipótese de universalidade. O conteúdo das quatro línguas do operador não foi reinterpretado para escolher uma linha.',
             '', 'Axiomas: N/A — sem Lean novo. JSON companheiro contém âncoras, hashes, dimensões conferidas por script e medidas fonte.']
    path=ROOT/'C1_LEITURAS.md'
    if path.exists():
        raise FileExistsError('Preserve prior C1 document')
    raw=('\n'.join(text)+'\n').encode('utf-8')
    tmp=path.with_name(path.name+'.tmp');tmp.write_bytes(raw)
    if tmp.stat().st_size!=len(raw):
        raise ValueError('Short write')
    tmp.replace(path)
    print(json.dumps(dict(status=result['status'],readings=len(rows),numeric_rows=sum(len(r['measurements']) for r in rows),
        dimensional_checks=len(unit_exponents),source_anchors=len(refs),hypothesis_selected=False)))


if __name__=='__main__':
    main()
