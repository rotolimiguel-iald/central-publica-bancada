"""Verify every copied dependency and the exact list of 90 contract consumers."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json,re
R=Path(__file__).resolve().parents[1];D=R/'D4';OUT=R.parent/'TUNEL/DO_CHATGPT'
sys.path.insert(0,str(R))
from prepare_part_d import sha,save,write
now=datetime.now(timezone.utc);manifest=json.loads((D/'COPY_MANIFEST.json').read_bytes())
for x in manifest['sources'].values():assert sha(Path(x['path']))==x['sha256']
batches=[('PhotonWitness.lean','witness_01',0),('PhotonModularRealization.lean','modular_01',0),('PhotonMassiveTransport.lean','transport_01',5),('PhotonContract_v2.lean','contract_02',6),('PhotonContractTheorems_v2.lean','theorems_01',90),('WeightControls_v2.lean','weights_01',5)]
proofs=[]
for fn,label,n in batches:
 p=D/fn;log=D/(label+'.log');rp=D/(label+'.json');x=json.loads(rp.read_bytes())
 assert x['rc']==0 and x['source_sha256']==sha(p) and x['log_sha256']==sha(log)
 assert not x['newer_kernel_files'] and not x['scan_errors']
 text=log.read_text('utf-8-sig');assert 'sorryAx' not in text and ': error' not in text
 ax=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",text,re.S)
 assert len(ax)==n and all({a.strip() for a in v.split(',')}<={'propext','Classical.choice','Quot.sound'} for _,v in ax)
 proofs.append(dict(source=str(p),source_sha256=sha(p),receipt_sha256=sha(rp),log_sha256=sha(log),declarations=dict(ax)))
orig=Path(manifest['sources']['TGLExt/ContratoQG_v31_Teoremas.lean']['path']).read_text('utf-8-sig')
new=(D/'PhotonContractTheorems_v2.lean').read_text('utf-8-sig')
orig_print=re.findall(r'^#print axioms (.+)$',orig,re.M);new_print=re.findall(r'^#print axioms (.+)$',new,re.M)
assert len(orig_print)==len(new_print)==90 and orig_print==new_print
# Aside from namespace/import retargeting and explicit legacy object conversion,
# the 90 theorem statements/proof bodies are verbatim copies.
expected=orig.replace('import TGLExt.ContratoQG_v31','import PhotonContract_v2').replace('TGL.SpecificAQFT','ORDEM016.Photon.SpecificAQFT').replace('TGL.ModularRealization','ORDEM016.Photon.ModularRealization').replace('TGLExt.ContratoQGv31','ORDEM016.Photon.Contract').replace('theSpecificAQFTWitness','ORDEM016.Photon.Transport.legacyW').replace('regularModularRealization','ORDEM016.Photon.Transport.legacyR').replace('namespace ORDEM016.Photon.Contract\n','namespace ORDEM016.Photon.Contract\nopen TGLExt\n')
assert new[new.index('import PhotonContract_v2'):]==expected
attempts=[json.loads((D/(label+'.json')).read_bytes()) for _,label,_ in batches]+[json.loads((D/'contract_01.json').read_bytes())]
r=dict(at=now.isoformat(),status='D4_PAGO_RETYPE_AND_90_CONSUMERS',proofs=proofs,consumer_count=90,consumer_body_comparison='EXACT_AFTER_DECLARED_NAMESPACE_IMPORT_LEGACY_SUBSTITUTIONS',all_original_source_hashes_unchanged=True,new_spectral_predicate='0 < m or helicity != 0',massless_scalar='REJECTED_BY_TYPE_THEOREM',photon_network_constructed=False,negative_mass_scope='Disjunction alone admits m<0 with nonzero helicity; the selected physical input is m=0. No extra nonnegativity postulate silently inserted.',cpu_seconds=sum(x['cpu_user_seconds']+x['cpu_kernel_seconds'] for x in attempts),wall_seconds=sum(x['wall_seconds'] for x in attempts),bench_hours=(now-datetime.fromisoformat(json.loads((D/'START.json').read_bytes())['at'])).total_seconds()/3600,opening_sha256=sha(OUT/'ENTREGA_016_ABERTURA_operador.md'),gate_changed=False)
save(D/'RESULTS.json',r)
text=f'''[REAL — D4 PAGO no escopo da retipagem e recompilação, sem testemunha física nova]

Abertura016SHA256: {r['opening_sha256']}

O campo m_pos estava em TGL/SpecificAQFTWitness.lean, não no próprio ContratoQG_v31. Foram copiadas e retipadas a testemunha, a realização modular, o contrato e os consumidores em namespaces isolados ORDEM016.Photon. Troca autorizada: helicity:ℤ e peso_do_nome:0<m ∨ helicity≠0. Todos os outros campos de rede, localidade, vácuo, translações e conteúdo modular foram preservados.

Os90 consumidores recompilaram com rc0 e somente o trio. Comparação por script confirma a mesma lista e corpos, exceto imports/namespaces e referências aos três controles legados. Cinco conversões campo a campo preservam as testemunhas MASSIVAS antigas para esses controles; não as chamam de fótons. O contrato tem seis declarações auditadas, os controles de peso cinco. Fonte/log/hash de cada etapa em D4/RESULTS.json.

O escalar m=0,h=0 é recusado por teorema sobre qualquer testemunha do tipo novo. As escolhas m=0,h=±1 satisfazem a condição de peso; isso não constrói a rede do fóton. Diagnóstico de escopo preservado: a disjunção isolada também admite m<0,h≠0. A escolha física vigente é m=0; não foi inserido outro postulado de não-negatividade sem ordem.

Primeira cópia do contrato falhou por nomes TGLExt que antes eram implícitos no namespace pai; a segunda acrescenta open TGLExt. Nenhuma prova foi relaxada. Um ciclo para testemunha/realização/conversões/90consumidores/controles, dois para o contrato. CPU{r['cpu_seconds']:.6f}s; parede{r['wall_seconds']:.6f}s; bancada{r['bench_hours']:.6f}h/teto6h. Hashes dos originais relidos e inalterados.

Não há alteração do canônico, um.py ou gate. PróximoD5: dilatações e auto-similaridade, mantendo aberta a covariância da rede até sua construção/identificação.
'''
write(OUT/'ENTREGA_016_D4_peso_do_nome.md',text.encode())
q=OUT/'ENTREGA_016_PROGRESSO.md';write(q,q.read_bytes()+f'\n{now.isoformat()} — D4 PAGO:retipagem+90consumidores, controle escalar recusado; nenhuma rede física nova. Bancada{r["bench_hours"]:.6f}h CPU{r["cpu_seconds"]:.6f}s. PróximoD5. AberturaSHA256 {r["opening_sha256"]}.\n'.encode(),True)
q=R/'A7/CONTINUIDADE.json';c=json.loads(q.read_bytes());c.update(at=now.isoformat(),own_live_process=None,own_live_processes=[],D4_delivery=str(D/'RESULTS.json'),next='D5 dilation geometry and conditional network modular selfsimilarity; then B. D4 retyping+90 consumers paid, no photon network constructed. Three new remote payloads remain pending explicit authorization.');save(q,c,True)
print(json.dumps({k:r[k] for k in ['status','consumer_count','cpu_seconds','bench_hours']},ensure_ascii=False))
