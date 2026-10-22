from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,sys,uuid
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
BASE=ROOT.parent/'IALD_ORQUESTRACAO_20260923'
DEST=HERE/'orchestration'
OUT=ROOT.parent/'TUNEL/DO_CHATGPT'
KERNEL=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,value):
    raw=value.encode('utf-8') if isinstance(value,str) else json.dumps(value,ensure_ascii=False,indent=2).encode('utf-8')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    if p.exists():
        old=p.read_bytes();b=p.with_name(p.name+'.bak_'+stamp);b.write_bytes(old);assert b.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+stamp);t.write_bytes(raw);assert raw and t.read_bytes()==raw;t.replace(p)
def excerpt(p,a=1,b=None):
    lines=p.read_text(encoding='utf-8-sig').splitlines();b=min(b or len(lines),len(lines))
    return f'\nSOURCE {p.name}; sha256={sha(p)}; lines={a}-{b}\n'+'\n'.join(f'{i}: {lines[i-1]}' for i in range(a,b+1))
source=HERE/'A_reproducao/TheEquationOfTruth.lean'
common=('ORDEM_016, A6: unidade científica nova solicitada pela bancada 01a070fc-9484-7e13-a654-c6b5f61093a4. '
        'Operador prioriza Kimi máximo e ampliou distribuição. Memória científica comum obrigatória. '
        'Somente texto matemático, sem ferramentas, sem editar arquivos, sem execução/compilação alegada. '
        'Use fontes abaixo e reuso dos lemas existentes; sem nova rede Fock, sem física ou gate inferidos. '
        'Contribuição DECLARADO até compilação local. O semigrupo dissipativo exp(-sH) deste alvo '
        'não é fluxo modular Delta_it nem boost. A bancada controla sequência e implementação.\n')
units=[
 ('kimi_single_time_converse','kimi','A-6.B1c','draft',
  'Pergunta única: qual prova mínima, com esqueleto Lean 4.31, descarrega a recíproca de UMA amostra temporal? '
  'Para H limitado auto-adjunto não negativo em dimensão finita, s0>0, leitor contínuo l num espaço T2, '
  'l(T H s0 x)=l x para todo x deve implicar l x=l(reading H x). Reuse o limite e exponencial abaixo; '
  'demonstre T(s0)^[n]=T(n*s0), transporte do limite e unicidade. Não assumir conservação para todo s '
  'nem o limite discreto como novo axioma. Dê hipóteses precisas e um controle s0=0 que invalida a '
  'conclusão. Nomes de API não verificados devem ser marcados candidatos. Nenhum código executado.',
  [(source,1,None)]),
 ('kimi_infinite_strong_limit','kimi','A-6.B1d','skeptic',
  'Pergunta única: sob quais passos analíticos adicionais o FlowTendsToFamily abaixo pode ser '
  'demonstrado para H limitado auto-adjunto positivo num Hilbert INFINITO, e qual passo exato não '
  'decorre de CFC contínuo em norma? Audite a rota via medidas espectrais/convergência dominada '
  'ou densidade de ran H + ker H e contração uniforme. Dê prova escrita completa da rota escolhida '
  'com hipótese e domínio explícitos, e o exemplo diag(1/n) em l2 que separa forte de norma. '
  'Não substituir o objetivo pelo FlowTendsToFamily assumido, não inferir limite uniforme porque '
  'e^(-s lambda) converge ponto a ponto no espectro, não exigir gap para forte. Proponha '
  'enunciados Lean candidatos sem inventar disponibilidade das APIs.',
  [(source,1,None)]),
 ('mimo_penalty_h3l_bridge','mimo','A-6.B4','draft',
  'Pergunta única: qual ponte Lean mínima identifica penalty ![Dc.toContinuousLinearMap, '
  'Db.toContinuousLinearMap,Dz.toContinuousLinearMap] com TGL.FiniteThreeLocks.H3L Dc Db Dz '
  'como LinearMap em EuclideanSpace Complex (Fin n), e reading com PF? Use a identidade '
  'LinearMap.adjoint_toContinuousLinearMap como candidata a conferir na bancada. Preserve '
  'os tipos e coerções: soma de ContinuousLinearMap versus soma/composição LinearMap. '
  'Não apenas igualdade da forma quadrática ou isomorfismo abstrato. Dê termo candidato '
  'por extensionalidade e simp, sem declarar compilação. Opcional dentro desta ponte: '
  'projetor ortogonal P satisfaz P=adjoint(P)*P. Não alegar instância das matrizes float '
  'do runtime, nem relação com o gerador modular K.',
  [(source,42,145),(source,185,231),(KERNEL/'TGL/FiniteThreeLocks.lean',1,130)])]
sys.path.insert(0,str(BASE))
from iald_orchestrator.runtime import Runtime
runtime=Runtime(recover=False)
status=runtime.status()
save(DEST/'runtime_status.json',dict(at=datetime.now(timezone.utc).isoformat(),providers=[
    {k:p.get(k) for k in ('id','status','model','thinking_effort','context_budget')}
    for p in status.get('providers',[]) if p['id'] in ('kimi','mimo')]))
prepared=[]
for slug,provider,branch,role,question,sources in units:
    path=DEST/(slug+'_submit.json')
    if path.exists():payload=json.loads(path.read_bytes())
    else:
        prompt=common+question+''.join(excerpt(*s) for s in sources)
        c=dict(mission_id='ORDEM_016',branch_id=branch,lemma_id=slug,role=role,required_provider=provider,max_calls=1)
        if provider=='mimo':c.update(max_cost_usd=None,max_output_tokens=131072)
        payload=dict(operation='submit',request_id=str(uuid.uuid4()),prompt=prompt,execution_constraints=c)
        save(path,payload)
        save(DEST/(slug+'_receipt.json'),dict(request_id=payload['request_id'],provider=provider,branch=branch,
             origin_thread_id='01a070fc-9484-7e13-a654-c6b5f61093a4',origin_directory=str(HERE),
             at=datetime.now(timezone.utc).isoformat(),status='PREPARED_NOT_SUBMITTED',prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest()))
    preview=runtime.preview(payload['prompt'],payload['execution_constraints'])
    save(DEST/(slug+'_preview.json'),preview)
    assert preview.get('selected')==provider, 'ROTA_NAO_DISPONIVEL: '+slug
    prepared.append(dict(slug=slug,provider=provider,branch=branch,request_id=payload['request_id'],
         selected=preview['selected'],payload=str(path),payload_sha256=sha(path),status='PREPARED_NOT_SUBMITTED'))
save(DEST/'prepared_units.json',prepared)
ledger=OUT/'LEDGER_016.jsonl';old=ledger.read_text(encoding='utf-8-sig')
for u in prepared:
    marker=u['request_id']
    if marker not in old:
        payload=json.loads(Path(u['payload']).read_bytes())
        old+=json.dumps(dict(event='unit_prepared_for_coordination',at=datetime.now(timezone.utc).isoformat(),
            request_id=marker,provider=u['provider'],branch=u['branch'],prompt_sha256=hashlib.sha256(payload['prompt'].encode()).hexdigest(),
            external_execution=False,tokens=None,cost_estimate_usd=None),ensure_ascii=False)+'\n'
save(ledger,old)
print(json.dumps(prepared,ensure_ascii=False))
