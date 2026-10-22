from pathlib import Path
from datetime import datetime, timezone
import hashlib, json

p = Path(__file__).resolve().parent
root = p.parent
base = root.parent / 'IALD_ORQUESTRACAO_20260923'
out = root.parent / 'TUNEL/DO_CHATGPT'
now = datetime.now(timezone.utc)
def sha(b): return hashlib.sha256(b).hexdigest()
def write(path, data, replace=False):
    if replace:
        old = path.read_bytes()
        write(path.with_name(path.name+'.bak_'+now.strftime('%Y%m%d_%H%M%S_%f')), old)
    else: assert not path.exists(), path
    temp = path.with_name(path.name+'.tmp')
    with temp.open('xb') as f: f.write(data)
    assert temp.read_bytes() == data
    temp.replace(path)

src = base/'state/handoffs/f16dd00e-d6ff-48d4-943e-8c82f3911024_completed.json'
d = json.loads(src.read_bytes()); ex = d['execution']; result = ex['result']
assert d['request_id']=='c101844e-52f8-4aac-8dfb-881771481a24'
assert d['stage']=='completed' and ex['status']=='result_ready'
answer = result['text'].encode('utf-8')
write(p/'a25c_kimi_scope_answer.md', answer)
manifest = json.loads((p/'unbounded_complete_manifest.json').read_bytes())
for a in manifest['artifacts']:
    for field in ['source','log','receipt']:
        assert sha((p/a[field]).read_bytes())==a[field+'_sha256']
    receipt=json.loads((p/a['receipt']).read_bytes())
    assert receipt['rc']==0 and not receipt['newer_kernel_files']
audit=json.loads((p/'unbounded_complete_axioms.json').read_bytes())
assert all(a['auditoria']=='PASSA' for a in audit)
assert sum(a['n_declaracoes_auditadas'] for a in audit)==55
ledger=out/'LEDGER_016.jsonl'; old=ledger.read_bytes()
events=[json.loads(x) for x in old.splitlines() if x.strip()]
prior=[x for x in events if x.get('request_id')==d['request_id']]
assert not any(x.get('event')=='coordination_executor_result_received' for x in prior)
entry={'ts':now.isoformat(),'event':'coordination_executor_result_received',
 'request_id':d['request_id'],'job_id':d['id'],'execution_task_id':ex['id'],
 'alvo':'A-2','ramo':'A-2.5.c','provedor':'kimi',
 'question_sha256':sha(d['prompt'].encode()),'answer_sha256':sha(answer),
 'raw_usage':result.get('usage'),'custo_usd':None,'elapsed_seconds':result.get('elapsed_seconds'),
 'provider_calls_observed':1,'desfecho':'completed','status_mathematics':'DECLARADO_STATIC_REVIEW_OLD_PACKET',
 'receipt_path':str(src),'receipt_sha256':sha(src.read_bytes())}
write(p/'a25c_kimi_scope_receipt.json',(json.dumps(entry,ensure_ascii=False,indent=2)+'\n').encode())
write(ledger,old+(json.dumps(entry,ensure_ascii=False)+'\n').encode(),True)
opening=sha((out/'ENTREGA_016_ABERTURA_operador.md').read_bytes())
report=f'''[REAL — confronto documental com provas compiladas; parecer externo DECLARADO]

# A-2.5.c — crítica Kimi recebida e reconciliada

Data UTC: {now.isoformat()}. ABERTURA sha256: `{opening}`.
Resposta bruta: `a25c_kimi_scope_answer.md`, sha256 `{sha(answer)}`.
Recibo: `a25c_kimi_scope_receipt.json`. Uma execução, {result.get('elapsed_seconds')} s,
uso `{json.dumps(result.get('usage'))}`. Custo monetário não informado.

O Kimi leu apenas os quatro arquivos do primeiro pacote (17 declarações), sem os módulos
importados. Não executou Lean. A revisão não cobre por extensão os 55 teoremas atuais.
As 12 fontes, logs e recibos atuais foram reconferidos por hash: rc 0, auditoria PASSA,
55 declarações e nenhuma alteração de kernel registrada.

| Ressalva do parecer | Confronto com o estado atual |
|---|---|
| R1: inversa à direita não basta | O módulo canônico V350PartialPositiveResolvent já contém partialOneAdd_injective e partialPositiveResolvent_inverse: R((I+D²)u)=u no domínio efetivo. selfadjointSquareResolvent instancia essa construção; não falta criar outra inversa. |
| P1: resolvente para D prescrito | selfadjoint_one_add_square_onto e selfadjointSquareResolvent, auditados. |
| P4: igualdade dos domínios | sameSquare_domain_eq, selfadjoint_absolute_domain e selfadjoint_normalizer_range, auditados. |
| P3: distinguir D de sua raiz positiva | unboundedTransform é literalmente D composto com normalizedInput = sqrt(R). Só a NORMA é comparada à de sqrt(1-R); não se substitui D por sua raiz positiva. |
| Gap ótimo | O contrato transporta limites inferiores. unboundedTransform_attainment transporta uma igualdade de normas dada; não declara por si só supremo espectral ou vetor não nulo no setor ortogonal. |

A construção atual não monta todos os campos de NormalizedGraphWitness para D arbitrário:
ela prova diretamente o contrato solicitado. Em particular, não declarar um novo teorema
de auto-adjunção/comutação do b construído que não esteja nessas fontes.
O controle unboundedTransform_ne_nonzero_idempotent impede identificá-lo literalmente
com um projetor não nulo. regularMinimalLock conserva seu papel de representante mínimo.

[REAL — correção de estado ao manifesto anterior] Kimi concluído. DeepSeek autorizado pelo
operador, porém a prévia classificou o pedido deep e excluiu seu tier standard: selected=null,
nenhum job nem envio à API. Evidência: a25c_deepseek_hypothesis_preview.json.
Não houve nova chamada, mudança de tier nem substituição de executor.

Próximo ramo: A-3.0 → A-3.d. Originais, gate e memórias canônicas intactos.
'''
write(out/'ENTREGA_016_MEDIDA_A2_5c_critica_Kimi_confrontada.md',report.encode())
a3=root/'A3'; a3.mkdir(exist_ok=True)
decision=f'''[INPUT — padrão explícito da ORDEM016; nenhuma partição escolhida pela bancada]

# A-3.0 — pré-decisão de tipo

UTC: {now.isoformat()}. ABERTURA sha256: `{opening}`.
Antes de código novo, registram-se as três opções reservadas ao operador:
(i) retipar m_pos para 0≤m amarrado a P²; (ii) conservar m>0 e construir o ramo massivo;
(iii) dois habitantes. Nenhuma delas foi escolhida aqui.
Padrão executado: namespace próprio, kernel intocado, sem habitar TGLSpecificAQFTWitness.
Medir escalar sem massa, escalar massivo e helicidades +1⊕−1 lado a lado na ordem prescrita.
A-3.d primeiro: frame suave invertível arrastado por boostMat, Killing e normalização por
um ponto N fornecido. Isso não produz a rede W, sua realização modular R nem identificação
com um horizonte físico. A-3.0 PAGO como registro, zero compilação; A-3.d inicia agora.
'''
write(a3/'PRE_DECISAO_TIPO.md',decision.encode())
progress=out/'ENTREGA_016_PROGRESSO.md'
write(progress,progress.read_bytes()+f'\n{now.isoformat()} | A-2.5.c crítica Kimi recebida/confrontada; 55 declarações reconferidas, nenhuma nova compilação | A-3.0 PAGO (pré-decisão sem escolher partição); próximo A-3.d. Custo Kimi não informado; DeepSeek sem chamada.\n'.encode(),True)
print(json.dumps({'review':str(out/'ENTREGA_016_MEDIDA_A2_5c_critica_Kimi_confrontada.md'),'audited':55,'next':'A-3.d'},ensure_ascii=False))
