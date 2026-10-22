"""Record finite conjugated form and the contract-dependent stationary readout."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json,re
R=Path(__file__).resolve().parents[1];D=R/'D3prime';OUT=R.parent/'TUNEL/DO_CHATGPT'
sys.path.insert(0,str(R))
from prepare_part_d import sha,save,write
now=datetime.now(timezone.utc);proofs=[];names=[]
for fn,label,n in [('ConjugatedFormScope_v2.lean','conjugated_02',11),('FiniteCenterFlow_v2.lean','finite_flow_02',4),('ContractFixedReadout.lean','contract_fixed_01',3)]:
 p=D/fn;log=D/(label+'.log');rp=D/(label+'.json');x=json.loads(rp.read_bytes())
 assert x['rc']==0 and x['source_sha256']==sha(p) and x['log_sha256']==sha(log)
 assert not x['newer_kernel_files'] and not x['scan_errors']
 assert not re.search(r'\b(sorry|axiom)\b',p.read_text('utf-8'))
 ax=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",log.read_text('utf-8-sig'),re.S)
 assert len(ax)==n and all({a.strip() for a in v.split(',')}<={'propext','Classical.choice','Quot.sound'} for _,v in ax)
 names.extend(k for k,_ in ax)
 proofs.append(dict(source=str(p),source_sha256=sha(p),receipt_sha256=sha(rp),log_sha256=sha(log),declarations=dict(ax)))
attempts=[json.loads((D/(k+'.json')).read_bytes()) for k in ['conjugated_01','conjugated_02','finite_flow_01','finite_flow_02','contract_fixed_01']]
r=dict(at=now.isoformat(),status='REAL_FINITE_AND_CONDITIONAL_CONTRACT_BRIDGE',proofs=proofs,new_declarations=sum(n.startswith('ORDEM016.') for n in names),reused_declarations=sum(n.startswith('TGLExt.') for n in names),named_remaining='StationaryLightCenterModularIdentificationMeasured',obligations=['Embed selected finite center into chosen photon net/tower and prove SAME element fixed by its modular flow','Supply actual photon ContratoH2, whose no_point_spectrum theorem is used conditionally','Distinguish fixed observable, vacuum-line readout and a nonzero-momentum one-particle state; identify the target of any Weinberg-Witten claim'],cpu_seconds=sum(t['cpu_user_seconds']+t['cpu_kernel_seconds'] for t in attempts),wall_seconds=sum(t['wall_seconds'] for t in attempts),bench_hours=(now-datetime.fromisoformat(json.loads((D/'START.json').read_bytes())['at'])).total_seconds()/3600,opening_sha256=sha(OUT/'ENTREGA_016_ABERTURA_operador.md'),gate_changed=False)
save(D/'RESULTS.json',r)
text=f'''[REAL — forma finita e ponte condicional pelo contrato; OPEN — identificação na rede escolhida]

Abertura016SHA256: {r['opening_sha256']}

D3′ reutiliza três teoremas do kernel: quadrado da luz, conjugação através do quadrado e forma conjugada resultante. Acrescenta {r['new_declarations']} declarações: o centro finito ¼ root₊root₋ é projPlus, comuta com a família angular e é fixo por sua conjugação; o vetor lightPlus muda em π/2. Esse projPlus não foi chamado centro de toda M₂ nem confundido com fluxo hiperbólico modular.

O vínculo físico condicional foi localizado no PRÓPRIO contrato: ContratoH2.no_point_spectrum. Dado um habitante H2, qualquer vetor fixo por todo Δit está em ℂΩ e todas as translações o fixam. Se um operador A é fixo por Ad(Δit), então AΩ está nessa reta. Três lemas verificam essa cadeia a partir do contrato existente; não se criou outro princípio de momento. A presença do habitante H2 continua hipótese, não definição satisfeita nesta entrega.

Controle adicional: um operador não nulo em dimensão três pode ser fixo por um grupo unitário diagonal e ter peso 1 para OUTRO gerador. Isso mostra por que fixidez isolada não basta; não contradiz H2, que contém as relações adicionais de covariância e ergodicidade usadas na prova acima. Logo a seta «ponto fixo ⇒ sem momento» só é usada aqui com esse conteúdo adicional e no vetor AΩ.

Escape Weinberg–Witten: somente condicional. Se a forma em questão se realiza como esse observável fixo, com esse H2, sua leitura AΩ é de vácuo e não uma excitação de momento não nulo. Isso não declara a existência de um gráviton propagante, não demonstra por si só o teorema externo e não identifica o observável com todos os seus estados. Não se promove a identidade finita ao J/PCT da rede.

StationaryLightCenterModularIdentificationMeasured fica NOMEADO: realização do centro finito na rede/tore física selecionada, preservação pela ação modular correspondente e efetivo habitante H2. A aceitação alternativa do adendo é atendida por teoremas finitos e MEDIDA dessa ponte. Nenhum axioma novo, sorry ou gate alterado.

Três fontes, 18 declarações auditadas:15 novas e3 reutilizadas, todas rc0 e trio. Manifesto completo em D3prime/RESULTS.json. Dois ciclos em cada arquivo finito, um na ponte do contrato. CPU{r['cpu_seconds']:.6f}s; parede{r['wall_seconds']:.6f}s; bancada{r['bench_hours']:.6f}h/teto8h. PróximoD4: retipagem em cópias e recompilação dos90 consumidores.
'''
write(OUT/'ENTREGA_016_D3prime_forma_conjugada.md',text.encode())
q=OUT/'ENTREGA_016_PROGRESSO.md';write(q,q.read_bytes()+f'\n{now.isoformat()} — D3′ REAL/MEDIDA:15 declarações novas,3 reutilizadas; fixo⇒reta do vácuo condicional a H2; identificação modular do centro na rede nomeada. Bancada{r["bench_hours"]:.6f}h CPU{r["cpu_seconds"]:.6f}s. PróximoD4. AberturaSHA256 {r["opening_sha256"]}.\n'.encode(),True)
q=R/'A7/CONTINUIDADE.json';c=json.loads(q.read_bytes());c.update(at=now.isoformat(),own_live_process=None,own_live_processes=[],D3prime_delivery=str(D/'RESULTS.json'),next='D4 retipagem peso_do_nome in copies and recompile contract + 90 declarations. m_pos is in TGL/SpecificAQFTWitness, not the contract. Clone dependency namespaces, preserve originals. 3 new remote calls still awaiting specific approval. Then D5, B.');save(q,c,True)
print(json.dumps({k:r[k] for k in ['status','new_declarations','reused_declarations','cpu_seconds','bench_hours']},ensure_ascii=False))
