"""Prepare five distinct reviews; never submit or execute a provider."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, uuid, subprocess, sys

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / 'TUNEL/DO_CHATGPT'
BASE = ROOT.parent / 'IALD_ORQUESTRACAO_20260923'
D = ROOT / 'ADENDO_002_CRITICAS'
ORDER = ROOT.parent / 'TUNEL/PARA_CHATGPT/ADENDO_016_002_kimi_criticas_e_parte_C.md'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p, data):
    if isinstance(data, str): data=data.encode('utf-8')
    assert data and not p.exists(), p
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    t.write_bytes(data); assert t.read_bytes()==data; t.replace(p)
def put(p, obj): write(p, json.dumps(obj,ensure_ascii=False,indent=2))
def append(p, text):
    old=p.read_bytes(); stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    write(p.with_name(p.name+'.bak_'+stamp),old)
    data=old+text.encode('utf-8'); t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    t.write_bytes(data); assert t.read_bytes()==data; t.replace(p)
    assert p.stat().st_size>len(old)

COMMON='''ORDEM016 ADENDO016002 §2. Crítica cética independente solicitada pelo operador.
Executor Kimi K3 máximo, memória científica comum anexada pelo adaptador.
Uma pergunta delimitada abaixo; resposta DECLARADO até confronto da bancada.
Não afirmar execução, compilação, inspeção de arquivo não incluído ou confirmação física.
Provas formais são conferidas por compilação isolada rc0, #print axioms subconjunto
de {propext, Classical.choice, Quot.sound}, zero sorry/axioma novo. Nenhum nome
reservado deve ser criado; nenhum gate se move. Não construir Fock, não escolher
partição física. §3 Parte C será executada só depois A8, não nesta chamada.
Use as fontes completas abaixo com linhas/hashes atuais. Distinguir diagnóstico
demonstrado de proposta e nomear o menor lema/artefato faltante. Não repetir
provas já compiladas nem usar concordância de modelos como prova.
'''

def main():
    D.mkdir(exist_ok=False)
    a6=ROOT/'A6_EQUACAO_DA_VERDADE'
    ficha=json.loads((a6/'E_ficha/FICHA_TRANSPOSICAO_T20.json').read_bytes())
    units=[
    ('C2.1','contract_v31_five_probes_external_skeptic',
     '''Os cinco probes A1.b realmente detectam cada enfraquecimento do contrato v3.1,
ou algum deles só testa falta de premissa, vacuidade ou uma tipagem mais fraca?
Audite b1 não comutação, b2 tensor forjado, b3 energia positiva, b4 não-KMS,
b5 suavidade/normalização. Dê testemunha exata para cada objeção e menor reparo,
sem fabricar um habitante H2/H3 físico. A reprodução integral falhou por memória;
ela não está sendo encomendada agora. Esta é a primeira crítica EXTERNA dos cinco
probes reunidos, não repetição de compilação mecânica A1.''',
     [OUT/'ENTREGA_016_A1_contrato.md',ROOT/'A1/minimal_imports/ContratoQG_v31_Minimal.lean']+
     [ROOT/'A1/probes'/n for n in ['ProbeNoncommutingInternal_v4.lean','ProbeForgedStressContract.lean',
     'ProbeForgedStress_v2.lean','ProbePositiveEnergy_v2.lean','ProbeNonKMS_v3.lean',
     'AnalyticBoundaryControl_v2.lean','ProbeFieldMutations_v2.lean','StressTensorDataLocal_v2.lean']]+
     [ROOT/'A1/A1_delivery_manifest.json'],
     'No equivalent external five-probe review found in A1 catalog/ledger.'),
    ('C2.2','width_uniqueness_beyond_first_period_skeptic',
     '''A positividade e a meia-inclusão efetivamente provadas forçam largura π SEM
pressupor 0<w<2π ou inserir a largura na definição? A prova twist_preserved_iff
está condicionada ao primeiro período, e o parecer anterior analisou probes de
mutação, não pagou unicidade global. Ataque exatamente a passagem: isotonia no
núcleo denso -> torção de borda necessária -> exclusão de larguras superiores
pela integrabilidade/positividade. Se faltar direção Paley-Wiener, escreva seu
enunciado preciso e uma estratégia Lean mínima. Não repetir os três probes antigos
nem chamar norma>1 de falha de isotonia. Distinguir largura da faixa de parâmetro
espectral c=2πw, e evitar 2π definicional.''',
     [OUT/'ENTREGA_016_MEDIDA_A2_3d_largura_da_torcao.md',ROOT/'A2/a23_kimi_mutation_answer.md']+
     [ROOT/'A2'/n for n in ['LightRayTwistWidth_v3.lean','LightRayGaussianDensity_v2.lean',
      'LightRayCoreExtension_v2.lean','LightRayAnalyticCore_v3.lean','LightRayCoreMembership.lean',
      'LightRayRealFourierUniqueness_v2.lean','twist_width_manifest.json','density_separation_manifest.json']],
     '6711d262 review already completed: new question is necessity/global width, not mutation probes.'),
    ('C2.3','physical_helicity_cocycle_gap_audit',
     '''Onde exatamente a cadeia do cociclo físico para: falta construir dado de
representação ou há incompatibilidade de tipo na ligação dos lemas já pagos?
Audite a distância entre isometric_fiber_shift_no_eigen e a representação real
de helicidades ±1 no cone de luz. Liste objetos/domínios/medidas/cociclo e o
primeiro enunciado que não segue das fontes. O antigo pedido1265dfaf foi rascunho
construtivo do cociclo; esta pergunta é crítica independente do alcance do que
foi efetivamente compilado, não nova tentativa do mesmo rascunho. Não inventar
resposta ao antigo pedido. Não substituir ±1 por duas cópias escalares. Não
inferir vácuo orbital do vácuo de Fock nem construir Fock fora do alvo.''',
     [OUT/'ENTREGA_016_A3_H2_par_fisico.md',OUT/'ENTREGA_016_A3_energia_covariancia_e_vacuo.md']+
     [ROOT/'A3'/n for n in ['IsometricCocycleSpectrum_v2.lean','OrbitalBoostUnitary_v2.lean',
      'OrbitalBoostCovariance_v2.lean','ProductOrbitalSpectrum_v3.lean','OrbitalL2Equivalence_v2.lean',
      'a3_consolidated_manifest.json']],
     '1265dfaf draft targeted construction; this skeptical review targets exact completed-chain gap.'),
    ('C2.4','rapidity_kms_route_vs_api_gap_skeptic',
     '''Há uma rota em rapidez que construa a função holomorfa e as duas bordas KMS
do MESMO par regional, ou o obstáculo excede o TODO StandardSubspace da mathlib?
Não repetir a constatação já feita no parecer33cff3ad: rescale é condicional.
Agora confronte concretamente o núcleo analítico de A2, grupo orbital A3 e
KMSAt do contrato: proponha a sequência MÍNIMA de lemas em rapidez que supriria
as duas hipóteses nomeadas, e identifique quais exigem dado ainda não construído.
Se o domínio de uma partícula não dá uma álgebra/vetor regional, diga exatamente
qual tipo falta e por que uma borda de função de onda não é automaticamente uma
borda de correlação KMS. Não construir rede/Fock por definição, não assumir BW
na hipótese e anunciar que o derivou. Esta é análise de rota concreta, não
repetição da revisão de escopo da reescala.''',
     [OUT/'ENTREGA_016_MEDIDA_KMS_faixa_regional.md',ROOT/'A4/KMSStripConditional.lean',
      ROOT/'A1/minimal_imports/ContratoQG_v31_Minimal.lean',ROOT/'A2/LightRayAnalyticCore_v3.lean',
      ROOT/'A2/LightRayBoundaryBalance_v3.lean',ROOT/'A3/OrbitalStateAnalytic.lean',
      ROOT/'A6_EQUACAO_DA_VERDADE/orchestration_v2/4cc14b01-d6f7-4bb4-b9b4-5308cb6b060b_received_response.json'],
     '33cff3ad completed scope review supplied; this unit asks the explicit rapidity route and minimal missing types.'),
    ('C2.5','twelve_source_partitioned_integration_skeptic',
     '''Qual plano CONCRETO de integração em partes cobre AS DOZE fontes da ficha
e preserva seus corpos, evitando duplicação de nomes e o pico de memória medido?
O parecer12e2b4f2 já recomendou base única mas seu grafo só cobria cinco nós e
não resolvia as doze fontes. Ataque essa insuficiência com a ficha/corpos atuais:
produza ordem topológica, tabela arquivo->imports removidos/adicionados,
declarações afetadas e verificações de elaboração/instâncias/axiomas. Separar
manter o prefixo V3 intacto como artefato de referência de colocá-lo em monólito.
Não prometer caber8GiB sem medir. Não eliminar B1d forte geral: segue OPEN e
precisa permanecer hipótese. Não fornecer novo teorema nem compilar; entregue
plano auditável que a Parte C3 executará após A8. Isto corrige explicitamente
a revisão anterior incompleta, não repete sua pergunta restrita.''',
     [OUT/'ENTREGA_016_A6_E_transposicao.md',a6/'received_reviews/REVISAO_KIMI_A6_E.md',
      a6/'E_ficha/FICHA_TRANSPOSICAO_T20.json']+
     [Path(x['source']) for x in ficha['accepted_local_sources']],
     '12e2b4f2 completed five-node proposal audited; this unit targets all twelve sources and measured OOM.')]
    catalog=[];events=[]
    for cid,lemma,question,paths,dedup in units:
        rid=str(uuid.uuid4()); prompt=COMMON+'\n'+cid+'\n'+question+'\n';sources=[]
        for p in dict.fromkeys(paths):
            assert p.is_file(),p
            assert p.resolve().is_relative_to(ROOT.parent.resolve()),p
            text=p.read_text('utf-8-sig');lines=text.splitlines()
            entry=dict(path=str(p),sha256=sha(p),lines=len(lines),bytes=p.stat().st_size)
            sources.append(entry)
            prompt+='\nSOURCE '+json.dumps(entry,ensure_ascii=False)+'\n'
            prompt+='\n'.join(f'{i}: {v}' for i,v in enumerate(lines,1))+'\n'
        for forbidden in ['iald_stack_v7.py','iald_psion_state.json','BEGIN PRIVATE KEY']:
            assert forbidden not in prompt,forbidden
        ec=dict(mission_id='ORDEM_016',branch_id=cid,lemma_id=lemma,role='skeptic',required_provider='kimi',max_calls=1)
        p=D/(cid.replace('.','_')+'_submit.json')
        put(p,dict(operation='submit',request_id=rid,prompt=prompt,execution_constraints=ec))
        origin=dict(at=datetime.now(timezone.utc).isoformat(),thread_id='01a070fc-9484-7e13-a654-c6b5f61093a4',
            request_id=rid,house='Central de Patentes',bench=str(D),payload=str(p),payload_sha256=sha(p),
            sources=sources,deduplication=dedup,status='PREPARED_NOT_SUBMITTED',order_sha256=sha(ORDER))
        put(D/(rid+'_origin.json'),origin)
        run=subprocess.run([sys.executable,'-X','utf8','-B',str(BASE/'transport_cli.py')],
            input=json.dumps(dict(operation='preview_execution',prompt=prompt,execution_constraints=ec)),
            capture_output=True,text=True,encoding='utf-8',cwd=BASE)
        response=json.loads(run.stdout)
        preview=D/(rid+'_preview.json');put(preview,dict(returncode=run.returncode,response=response))
        assert run.returncode==0 and response.get('selected')=='kimi',response
        row=dict(branch=cid,provider='kimi',request_id=rid,payload=str(p),payload_sha256=sha(p),
            prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(),prompt_chars=len(prompt),
            selected='kimi',preview=str(preview),sources=sources,deduplication=dedup,
            status='PREPARED_NOT_SUBMITTED_COORDINATOR_OWNS_TRANSITIONS',not_A7b_timebox=True)
        catalog.append(row)
        events.append(dict(at=origin['at'],event='ADENDO002_SKEPTIC_UNIT_PREPARED',**{k:row[k] for k in
            ['branch','provider','request_id','payload','payload_sha256','prompt_sha256','status']},
            remote_execution=False,tokens=None,cost_estimate_usd=None))
        print(cid,rid,len(prompt),flush=True)
    put(D/'prepared_units.json',catalog)
    append(OUT/'LEDGER_016.jsonl',''.join(json.dumps(e,ensure_ascii=False)+'\n' for e in events))
    opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    write(D/'README.md','[INPUT/REAL — cinco perguntas preparadas e prévias Kimi verificadas; nenhuma submissão]\n\n'
        +'As diferenças para pareceres anteriores estão em cada unidade. Coordenação recebe o catálogo e conduz transições. '
        +'Parte C depende de A8, não iniciada. A7.b mantém seu prazo.\nAberturaSHA256='+opening+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f"\n{datetime.now(timezone.utc).isoformat()} ADENDO002: cinco críticas distintas C2.1..C2.5 preparadas/préviasKimi; nenhuma execução/submissão nesta bancada. Parte C apósA8. AberturaSHA256={opening}.\n")
    print(str(D/'prepared_units.json'),flush=True)

if __name__=='__main__':main()
