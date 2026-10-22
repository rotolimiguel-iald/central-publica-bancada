"""Audit external C2.1 criticism against full existing A1 sources and custody."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re,time
import sympy as s
from deliver_nonminimal_wick_and_mimo_audit import H,OUT,BASE,sha,write,put,append

def main():
    start=time.process_time();now=datetime.now(timezone.utc)
    root=H.parent;A=root/'A1';D=root/'ADENDO_002_CRITICAS/C21_AUDIT';D.mkdir(exist_ok=False)
    source=BASE/'state/handoffs/3bafcf09-fb40-4080-9b4d-6237cc26fd6a_delivery.json'
    j=json.loads(source.read_bytes())['job'];e=j['execution'];r=e['result'];assert e['status']=='result_ready'
    write(D/'KIMI_ORIGINAL.md',r['text'].encode())
    put(D/'RECEIPT.json',dict(request_id=j['request_id'],job_id=j['id'],execution_id=e['id'],
        source_sha256=sha(source),prompt_sha256=hashlib.sha256(j['prompt'].encode()).hexdigest(),
        response_sha256=sha(D/'KIMI_ORIGINAL.md'),usage=r['usage'],cost_estimate_usd=r.get('cost_estimate_usd'),
        canonical_memory=r.get('canonical_memory'),cost_unknown_not_zero=r.get('cost_estimate_usd') is None))
    contract=A/'minimal_imports/ContratoQG_v31_Minimal.lean';original=A/'v31/ContratoQG_v31.lean'
    def body(p):return '\n'.join(line for line in p.read_text('utf-8').splitlines() if not line.startswith('import '))
    assert body(contract)==body(original)
    original_manifest=A/'A1_delivery_manifest.json';manifest=json.loads(original_manifest.read_bytes())
    refs=[source,contract,original,original_manifest,Path(__file__)];receipts=[]
    # Read all existing receipts; this is not a new compilation.
    for record in manifest['all_compile_receipts']:
        p=Path(record['file']);assert sha(p)==record['sha256'];refs.append(p)
        rec=json.loads(p.read_bytes());assert rec['rc']==record['rc']
        receipts.append(dict(path=str(p),sha256=sha(p),rc=rec['rc']))
    selected=['v31_minimal_01','field_mutations_02','forged_contract_01','local_stress_02',
        'noncommuting_internal_04','non_kms_02','positive_energy_02']
    checked=[]
    for record in manifest['all_compile_receipts']:
        rp=Path(record['file'])
        if rp.stem not in selected:continue
        rec=json.loads(rp.read_bytes());src=Path(rec['command'][-1]);log=rp.with_suffix('.log')
        assert rec['rc']==0 and sha(src)==rec['source_sha256'] and sha(log)==rec['log_sha256']
        text=log.read_text('utf-8')
        assert 'sorryAx' not in text
        axiom_lists=re.findall(r'depends on axioms:\s*\[([^]]*)\]',text,re.S)
        assert axiom_lists,(rp,text)
        allowed={'propext','Classical.choice','Quot.sound'}
        for group in axiom_lists:assert {v.strip() for v in group.split(',') if v.strip()}<=allowed
        refs.extend([src,log]);checked.append(dict(source=str(src),receipt=str(rp),log=str(log),
            source_sha256=sha(src),log_sha256=sha(log),printed_axiom_lists=len(axiom_lists),rc=0))
    paths={key:A/'probes'/name for key,name in dict(
        b1='ProbeNoncommutingInternal_v4.lean',b2='ProbeForgedStressContract.lean',
        b3='ProbePositiveEnergy_v2.lean',b4='ProbeNonKMS_v3.lean',b5='ProbeFieldMutations_v2.lean',
        local='StressTensorDataLocal_v2.lean',forge='ProbeForgedStress_v2.lean').items()}
    refs.extend(paths.values());anchors={}
    targets={'b2':['forged_nullEnergy','forged_nullPlaneCharge','symSource_forged','transportH3','same_response'],
        'b3':['positive_energy_excludes_negative_unit_mode'],
        'b4':['identity_kms_forces_tracial_boundary','identity_flow_not_kms'],
        'b5':['roughFrame_not_smooth','replaceFrame','admitZero','admitZero_not_unit'],
        'local':['StressTensorDataLocal','forged_tensor_rejected']}
    for key,names in targets.items():
        lines=paths[key].read_text('utf-8').splitlines()
        anchors[key]={name:next(i for i,line in enumerate(lines,1) if re.match(r'(?:theorem|def|structure) '+name+r'\b',line)) for name in names}
    ctext=contract.read_text('utf-8');assert 'def PositiveEnergy' in ctext and 'DiffContOnCl ℂ F upperHalf' in ctext
    # Algebraic counterexample to treating an x-dependent skew amplitude as constant.
    x=s.symbols('x0:4');skew=s.zeros(4);skew[2,3]=x[2];skew[3,2]=-x[2]
    n=s.Matrix([1,1,0,0]);assert (n.T*skew*n)[0]==0
    div=[sum((1 if mu==0 else -1)*s.diff(skew[mu,nu],x[mu]) for mu in range(4)) for nu in range(4)]
    assert div==[0,0,0,-1]
    result=dict(at=now.isoformat(),scope='C2.1 documentary/source audit plus one algebraic counterexample, no new Lean compilation',
        body_equal_after_removing_import_lines=True,receipts_checked=len(receipts),successful_source_log_pairs=len(checked),
        checked=checked,anchors=anchors,skew_variable_amplitude_divergence=list(map(str,div)),
        accepted=['b1 is explicitly a weaker finite control, not H2','No probe establishes physical nonvacuity',
            'b2 targets symmetry, not operator microcausality','b4 exclusion assumes contrast/nontraciality',
            'Positive tracial KMS control remains an additional possible check'],
        corrections=['Minimal body textual fidelity already verifiable; imports only differ',
            'b3 directly consumes actual analytic PositiveEnergy, no new Stone-Hardy bridge needed for its stated conclusion',
            'b4 already explicitly has height1 and hcontrast in the final theorem',
            'b5 has explicit conditional constructions and rejection theorems, omitted by the projection',
            'b2 preserves actual null energy, plane charge and response in existing lemmas',
            'Local extension already has symmetric field and forged_tensor_rejected',
            'Skew amplitude in forgedTensor is nullEnergy(T,psi,x), not spatially constant',
            'Number of phases alone is not sufficient for faithfulness of arbitrary frequencies; existence needs a suitable frequency choice'],
        limitations=['Only textual body equivalence; unchanged type proof is not a new reproduction of original imported environment',
            'No new H2/H3 inhabitant','No recompilation billed or claimed','No dimension theorem compiled'],
        cpu_seconds=time.process_time()-start,full_Q2=False,gate_changed=False)
    put(D/'AUDIT.json',result);opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    note=f'''[REAL — auditoria das fontes completas e recibos existentes; crítica Kimi parcialmente corrigida]

C2.1 recebida integralmente. O executor declarou as lacunas da projeção.
Confronto feito com fontes completas; não houve recompilação nem novo habitante.

1. Fidelidade: os corpos do contrato original copiado e Minimal são textualmente
iguais após retirar apenas linhas import. Isso não reproduz o ambiente original.
2. b1: permanece controle finito mais fraco, explicitamente não-H2. A condição
de pelo menos n+1 fases é necessária no modelo de caracteres de R^n, mas não
suficiente para qualquer escolha de frequências. Não compilamos novo lema.
3. b2: forged_nullEnergy, forged_nullPlaneCharge, symSource_forged,
transportH3 e same_response JÁ fornecem as preservações pedidas. A extensão
StressTensorDataLocal JÁ exige simetria e tem forged_tensor_rejected.
A crítica supõe amplitude constante; o código usa nullEnergy(T,psi,x).
Contraexemplo ao argumento de conservação: skew23=x2,skew32=-x2 tem
leitura nn nula e divergência covariante (0,0,0,-1). Não é um novo H3.
4. b3: PositiveEnergy é DEFINIDO na forma analítica; o teorema
positive_energy_excludes_negative_unit_mode consome exatamente esse campo.
Não falta uma nova ponte Stone/Hardy para esta conclusão já declarada.
5. b4: identity_flow_not_kms JÁ fixa altura1 e exige hcontrast explicitamente.
Controle positivo tracial seria complementar; não o declaramos executado.
6. b5: roughFrame_not_smooth e replaceFrame fornecem mutação explícita
CONDICIONAL a H2; admitZero e admitZero_not_unit fazem o mesmo sob H3,
T(0)=0 e theta(0)=0. Nenhuma construção prova não-vacuidade física.

{len(receipts)}recibos conferidos por hash; {len(checked)}pares relevantes
fonte/log rc0 cruzados com seus hashes e axiomas impressos permitidos.
São evidências históricas conferidas, não novas compilações. Não duplicar CPU.
Custos desta chamada Kimi por assinatura não informados; não são zero.
Uso: {r['usage']}. Recibo e resposta integral preservados no manifesto.

A crítica evita promoção dos probes, mas não cria dívida nova onde as fontes
já pagaram a ligação. Não-vacuidade física e localidade de operadores
mantêm seus estatutos. Nada altera kernel, originais ou gate.
AberturaSHA256={opening}.
'''
    write(D/'CONFRONTO.md',note.encode());write(OUT/'ENTREGA_016_MEDIDA_C21_confronto_fontes.md',note.encode())
    refs += [D/'KIMI_ORIGINAL.md',D/'RECEIPT.json',D/'AUDIT.json',D/'CONFRONTO.md']
    unique=list(dict.fromkeys(refs));put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in unique],full_Q2=False))
    ledger=OUT/'LEDGER_016.jsonl'
    existing=[json.loads(line) for line in ledger.read_text('utf-8').splitlines() if line.strip()]
    assert not any(e['id'] in json.dumps(item) and 'completion_tokens' in json.dumps(item) for item in existing),'Already accounted'
    append(ledger,json.dumps(dict(at=now.isoformat(),event='C21_EXTERNAL_CRITIQUE_AUDITED',target='ADENDO002.C2.1',
        provider='kimi',request_id=j['request_id'],job_id=j['id'],execution_task_id=e['id'],usage=r['usage'],
        cost_estimate_usd=None,cost_unknown_not_zero=True,source_sha256=sha(source),response_sha256=sha(D/'KIMI_ORIGINAL.md'),
        manifest_sha256=sha(D/'manifest.json'),audit_cpu_seconds=result['cpu_seconds']))+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} ADENDO002 C2.1 crítica externa confrontada: b3/b5 e ligaçõesb2 já existentes; {len(receipts)}recibos,{len(checked)}fontes/logs conferidos, sem recompilar. Kimi344357tokens, custoassinatura desconhecido. AberturaSHA256={opening}.\n')
    print(json.dumps(dict(manifest=str(D/'manifest.json'),receipts=len(receipts),successful_pairs=len(checked),cpu_seconds=result['cpu_seconds'])),flush=True)

if __name__=='__main__':main()
