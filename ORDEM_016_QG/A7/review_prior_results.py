from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
import hashlib,json

HERE=Path(__file__).resolve().parent
A5=HERE.parent/'A5'
OUT=HERE.parents[1]/'TUNEL/DO_CHATGPT'
DEST=A5/'received_results'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,text):
    raw=text.encode('utf-8') if isinstance(text,str) else json.dumps(text,ensure_ascii=False,indent=2).encode()
    assert not p.exists(),p
    t=p.with_suffix(p.suffix+'.tmp');t.write_bytes(raw);assert t.read_bytes()==raw and raw;t.replace(p)

ids=['08addf0a-def3-4757-9140-958cb96b72fc','51a28f15-0463-43f7-b2d0-ad712e390cd3']
pins={}
for job in ids:
    receipt=json.loads((DEST/(job+'.json')).read_bytes())
    assert sha(DEST/(job+'.md'))==receipt['response_sha256']
    pins[str(DEST/(job+'.md'))]=receipt['response_sha256']
source_checks=[]
m=json.loads((A5/'constructed_import_manifest.json').read_bytes())
for entry in m['proofs']:
    assert sha(Path(entry['source']))==entry['source_sha256']
    assert sha(Path(entry['log']))==entry['log_sha256']
    assert entry['receipt']['rc']==0 and entry['audit']['auditoria']=='PASSA'
    source_checks.append(dict(source=entry['source'],source_sha256=entry['source_sha256'],
                              log_sha256=entry['log_sha256'],stored_rc=0,stored_audit='PASSA'))
assert m['negative']['rc']==1
source=A5/'two_body_first_order_exact_v2.py'
res=json.loads((A5/'two_body_first_order_exact_v2.json').read_bytes())
assert sha(source)==res['source_sha256'] and res['all_passed']
for p in [source,A5/'two_body_first_order_exact_v2.json',A5/'ConstructedImportH3_v2.lean',
          A5/'ProbeEmptyIndexRejected.lean',A5/'constructed_import_manifest.json']:
    pins[str(p)]=sha(p)

opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
now=datetime.now(timezone.utc).isoformat()
body=f'''[DERIVED — revisão local de contribuições; REAL — custódia dos resultados existentes]

# A5 — consumo crítico de DeepSeek H3 e MiMo dois corpos

Abertura SHA256: `{opening}`. Data UTC: {now}.

DeepSeek, job {ids[0]}: o termo central coincide com a construção local existente:
produce recebe h e usa hmc(h), hAn(h), hflat(h); same_horizon é rfl. Isto confirma
uma leitura do enunciado, não cria prova nova. ConstructedImportH3_v2.lean já usa
esse corpo, com compilação registrada rc0 e auditoria PASSA, fontes/logs conferidos
por hash nesta leitura. O rearranjo de módulos proposto não foi necessário: a bancada
já eliminou a duplicação via NullSolutionConsumerReuse. Não o substituir por imports
candidatos não compilados.

Recusa parcial: o controle de h2 fixo testa a dependência do horizonte, não a
ausência de habitante do índice. Mesmo h2=h pode ser demonstrável em contextos
particulares; ausência de rfl genérico não prova impossibilidade absoluta. Mantém-se
o controle existente ProbeEmptyIndexRejected (rc1 registrado) e o teorema
no_import_over_empty_h2. H2 físico, T0, hmc, hAn e hflat não foram derivados pelo
modelo. Contribuição consumida como revisão de composição condicional.

MiMo, job {ids[1]}: a expansão da expectativa normalizada está correta SOB as
hipóteses de normalização/ortogonalidade e domínio do operador. Corrige-se a frase
da seção4 que a chama incondicional para todo φ. Para Ω unitário, a fórmula geral é

    q'_A(0)=2 Re<φ,AΩ>−2 Re<Ω,φ><Ω,AΩ>.

Contraexemplo exato à afirmação incondicional: A=id, φ=Ω. A expectativa normalizada
vale1 perto de ε=0, logo sua derivada é0; a fórmula sem correção daria2. O próprio
controle de normalização do modelo já reconhece essa restrição, contradizendo a
frase geral. Para A ilimitado, ainda precisam ser fixados domínios adequados.

Recusas adicionais: |1> não é “estado coerente”; a matriz de emparelhamento escolhida
ad hoc e a matriz de número de pares não derivam o mesmo tensor local do horizonte.
A menção à hiperfinitude não fornece o transporte de observáveis, estados, domínios
e derivadas entre esse exemplo e uma rede III1. O Lean sugerido contém sorry e
native_decide e não é candidato aceito sob a régua desta missão. As referências
a CTT/Clausius não foram verificadas por esse modelo e não são importadas aqui.

A bancada já possui um controle mais específico: two_body_first_order_exact_v2
usa a MESMA densidade quadrática normal-ordenada, integra suas duas semirretas e
obtém as cargas comprimidas; {res['count']} checks registrados passaram. Fonte e resultado
conferidos por hash, sem reexecutar. Seu alcance continua um modelo de carga;
não fornece o T0 físico nem a rede completa. O exemplo ad hoc MiMo não o substitui.

Resultado: nenhuma nova função ou camada acrescentada ao caminho de H3. As partes
úteis foram reconhecidas no trabalho existente; os exageros e controles inadequados
foram recusados. Nenhum gate ou fonte original mudou. Manifesto próprio lista os
hashes medidos, recibos e o estatuto das contribuições.
'''
save(DEST/'REVISAO_DEEPSEEK_MIMO_A5.md',body)
save(DEST/'review_manifest.json',dict(status='LOCAL_REVIEW_COMPLETE_SCOPED',at=now,
 opening_sha256=opening,response_and_source_pins=pins,verified_prior_sources=source_checks,
 deepseek='Composition already compiled locally; reject replacing missing-index control',
 mimo='Conditional algebra accepted; unconditional claim and coherent-state label rejected',
 new_lean_or_cas=False,gate_changed=False))
costs={}
for line in (OUT/'LEDGER_016.jsonl').read_text(encoding='utf-8-sig').splitlines():
    if not line.strip():continue
    e=json.loads(line);c=e.get('cost_estimate_usd',e.get('cost_usd',e.get('custo_usd')))
    key=e.get('execution_id')or e.get('job_id')or e.get('request_id')or e.get('execution_task_id')
    if c is not None and key:costs[key]=Decimal(str(c))
total=sum(costs.values(),Decimal(0))
save(OUT/'ENTREGA_016_A5_revisoes_deepseek_mimo.md',f'''[REAL — recuperação de recibos; DERIVED — revisão local, sem prova nova]

Abertura SHA256 `{opening}`.

DeepSeek H3 e MiMo dois corpos foram recebidos integralmente pela API de coordenação,
sem nova chamada a provedor. O termo DeepSeek corresponde à composição condicional
já compilada. Seu controle não substitui o teste existente de índice ausente.
MiMo repete o lema algébrico sob hipóteses, mas sua frase “todo φ” omite normalização
e a etiqueta “coerente” para |1> é incorreta. O exemplo ad hoc não substitui o harness
local de duas semirretas. Não foram introduzidas novas camadas de código.

Revisão integral: `{DEST/'REVISAO_DEEPSEEK_MIMO_A5.md'}`.
Manifesto SHA256 `{sha(DEST/'review_manifest.json')}`.
Recibos, prompts em hash e respostas em hash constam do ledger; soma explícita
deduplicada estimada US${total}, ainda incompleta, sem custo de assinatura convertido
artificialmente em zero. Nenhuma execução científica repetida; nenhum gate movido.
''')
print(json.dumps(dict(status='LOCAL_REVIEW_COMPLETE_SCOPED',recorded_estimated_usd=str(total),
                     report=str(DEST/'REVISAO_DEEPSEEK_MIMO_A5.md'))))
