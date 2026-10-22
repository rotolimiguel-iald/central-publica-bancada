"""Append one verified operational milestone, with immediate byte backups."""
from pathlib import Path
from datetime import datetime, timezone
import json
from audit_inputs import file_info, save_json, safe_write
from reconcile_documentary_milestone_20261006 import verify_manifest

ROOT=Path(__file__).resolve().parent
MEM=Path(r'C:\IALD\Central de Patentes\memory')
MARK='<!-- ORDEM018_EIGHT_CONTROLS_PASS_GUARD_REVIEW_20261006 -->'

def main():
    receipt_path=ROOT/'RECIBO_MEMORIA_CONTROLES_E_GUARD_REVIEW.json'
    assert not receipt_path.exists(), 'Already recorded; inspect rather than repeat'
    controls=ROOT/'RECIBO_ROOT_CONTROLES_COTA_CONCLUIDOS.json'
    value=json.loads(controls.read_bytes())
    assert value['status']=='EIGHT_FIXED_SYNTHETIC_CONTROLS_PASSED_ONCE'
    review_dir=ROOT/'preregistros/conjunto_d/revisao_audit_guard_repair'
    review=verify_manifest(review_dir/'MANIFESTO_REVISAO.json')
    pins={'controls':file_info(controls),'guard_review':file_info(review_dir/'RECIBO_REVISAO_DOCUMENTAL.json'),
          'draft':file_info(ROOT/'f9_consolidated_draft/RESOLUTOR_F9.json')}
    now=datetime.now(timezone.utc).isoformat()
    note=f'''{MARK}
## 06/10/2026 UTC — Oito controles da cota concluídos; revisão do reparo operacional

[REAL — mapa490] Unidade {value['request_id']} executada uma vez: oito controles C01–C08 PASS, filho exit0, parede total {value['supervisor_wall_s']:.9f}s, dentro do orçamento nominal30s. ROOT conferiu identidade, CLAIM, contrato,12pins e recibos. Casos de projeção/quociente, inclusão global versus tangente, sinal/grau zero, direção de limites dos mínimos, covariância incompatível e cenários incompletos preservam o alcance do protocolo. C08 certificou cinco caudas fixas por intervalos racionais, incluindo cauda positiva sem underflow. C05/C06 são testemunhos sintéticos delimitados; isso não é otimizador global nem algoritmo geral de SF, e não certifica a aplicação completa F9. Recibo SHA256 {pins['controls']['sha256']}. Unidade consumida, sem repetição.

[REAL documental — mapa491] Revisão independente do reparo audit:125 verificações estáticas,26 arquivos e9 originais conferidos; sem P2+ bloqueante localizado no recorte. Latch persistente, journal e checkpoints foram preparados; a aceitação do supervisor cruza resultado/journal e impede continuação após falha. AST científico, allowlist e limites INIT003 preservados. Recibo SHA256 {pins['guard_review']['sha256']}. ROOT aceita a revisão documental para preparação dos21 testes com doubles; eles ainda não rodaram neste marco. Integração nativa, journal físico, hook real e limite pós-kill permanecem OPEN. Não há nova autorização PE; INIT003 continua terminal não qualificado.

[REAL documental] Rascunho F9 consolidado entregue489 com resolutor SHA256 {pins['draft']['sha256']}, fonte única de leitura proposta para as cláusulas atuais e supersessões; revisão independente em fechamento. Nenhuma escolha científica ratificada, V1 congelado ou dado composto/D aberto. Resultados E45 continuam históricos; F1/F3 permanecem em curso. Fila: uma coordenação antiga bloqueada por geração divergente, zero execuções; needs_attention registrado, sem alteração de pin ou cobrança duplicada. Nova consulta documental D à gerente continua pendente. Zero provedor remoto/Work, novo selo, kernel ou gate alterado. A recusa automática anterior de download SBF permanece preservada sem nova tentativa.'''
    updates=[]
    for p in (MEM/'TGL_ATLAS.md',MEM/'TGL_INDICE_VIVO.md',MEM/'TGL_CORE_MEMORY.md',ROOT/'ENTREGA_018_F1_HUBBLE.md',ROOT/'ENTREGA_018_F3_PRIMORDIAL_E_RINGDOWN.md'):
        old=p.read_bytes()
        assert MARK.encode() not in old, 'Marker already present'
        new=old+('\r\n\r\n'+note.replace('\n','\r\n')+'\r\n').encode()
        assert p.read_bytes()==old
        safe_write(p,new)
        assert p.stat().st_size>len(old)
        updates.append({'before_bytes':len(old),'after':file_info(p)})
    path=ROOT/'CONTINUIDADE.json';old=path.read_bytes();v=json.loads(old)
    v['updated_at']=now
    v['phases']['F1']='E45_COMPLETE; CONDITIONAL_BOUND_REVIEWED; EIGHT_FIXED_CONTROLS_PASS; CLEAN_DRAFT_DELIVERED; OBSERVED_COMPOSITE_CLOSED'
    v['phases']['F3']='INIT003_TERMINAL_UNQUALIFIED; AUDIT_GUARD_STATIC_REVIEW_ACCEPTED; DOUBLES_EXECUTION_PREPARATION; D_CLOSED'
    v['milestone_sequences']=sorted(set(v.get('milestone_sequences',[])+[489,490,491]))
    v['analytic_bound_controls']=pins['controls'];v['F9_current_documentary_resolver']=pins['draft'];v['audit_guard_static_review']=pins['guard_review']
    v['next_steps']=['Complete independent acceptance of consolidated F9 draft; implement bounded statistical components without observed data.',
                     'Review exact doubles-only launcher; execute once if accepted, then preserve terminal result.',
                     'Receive pending official DQ/calibration metadata from manager; complete concrete policy before opening decision.',
                     'No new PE or opening of F9/D authorized.']
    assert path.read_bytes()==old
    save_json(path,v);updates.append({'after':file_info(path)})
    save_json(receipt_path,{'at':now,'marker':MARK,'status':'CONTROLS_COMPLETED_GUARD_DOCUMENTARY_REVIEW_ACCEPTED','pins':pins,'verified_review_manifest':review,'updates':updates,'exact_prior_byte_backups_and_CAS':True})
    print(json.dumps({'receipt':file_info(receipt_path),'updated':len(updates)}))

if __name__=='__main__':main()
