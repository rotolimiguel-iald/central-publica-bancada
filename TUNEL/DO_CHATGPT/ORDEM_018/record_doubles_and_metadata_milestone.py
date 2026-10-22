"""Record inspected results and refresh only the documentary consolidation."""
from pathlib import Path
from datetime import datetime,timezone
import json
from audit_inputs import file_info,save_json,safe_write

ROOT=Path(__file__).resolve().parent
MEM=Path(r'C:\IALD\Central de Patentes\memory')
MARK='<!-- ORDEM018_DOUBLES_PASS_METADATA_D_F9_REVIEW_20261006 -->'

def main():
    out=ROOT/'RECIBO_MEMORIA_DOUBLES_D_METADATA.json'
    assert not out.exists()
    pins={k:file_info(ROOT/n) for k,n in {
        'doubles':'RECIBO_ROOT_DOUBLES_GUARD_PASS.json',
        'documentary_acceptance':'RECIBO_ROOT_D_METADATA_E_F9_REVIEW.json',
        'F9_review':'proveniencia/revisao_f9_consolidado/RECIBO_REVISAO_F9_CONSOLIDADO.json',
        'D_metadata':'preregistros/conjunto_d/d_metadata_semantics/MANIFESTO_ENTREGA.json',
        'calibration_inventory_request':'D_CALIBRATION_MEMBER_INVENTORY_REQUEST.json'}.items()}
    w=json.loads(Path(pins['doubles']['path']).read_bytes())
    assert w['tests_run']==21 and w['status']=='21_PURE_DOUBLES_PASSED_ONCE'
    now=datetime.now(timezone.utc).isoformat()
    note=f'''{MARK}
## 06/10/2026 UTC — Doubles operacionais concluídos e semântica D recebida

[REAL — mapa497] Os21 testes com doubles do latch/aceitação passaram em execução única, request {w['request_id']}; zero falhas/erros, total {w['total_wall_s']:.9f}s, suíte {w['suite_wall_s']:.9f}s. Claims, identidades/PIDs, nomes, pins e streams conferidos por ROOT. Recibo SHA256 {pins['doubles']['sha256']}. Isto qualifica esses controles puros, não integração nativa, hook/journal físico, cobertura ou PE. INIT003 permanece terminal não qualificado; nenhum job consumido foi repetido.

[REAL documental — mapa494] Rascunho consolidado F9 aceito no recorte documental:43 pins,7 arquivos e128 verificações independentes; modelos/priors/V2/cota e supersessões coerentes. ROOT leu o parecer e conferiu seu manifesto. Recibo de revisão SHA256 {pins['F9_review']['sha256']}. F1 continua preparação, sem V1 congelado/abertura ou novo veredito; E45 é histórico. Envelope racional da cauda é proposta matemática separada em revisão, ainda sem implementação/adoção.

[KNOWN documental / REAL custódia — mapa495] Gerente respondeu c1fe821a com21 arquivos conferidos por ROOT. Documentação oficial O4 define9DQ/5INJ a1Hz; DATA não implica ausência de injeção; CW exige política explícita. Leitor existente presume origem temporal das máscaras; presença/alinhamento local continuam não verificados. Documentação diferencia O4a GDS e O4b DCS/AR01 com composição C00/C01. Produto horário DCC descreve magnitude R_true/R_model e fase em radianos, sem fornecer por si covariância completa. Hashes de excertos não são hashes de corpos HTTP. Nenhum strain/container/PE/posterior/centro foi aberto. Manifesto SHA256 {pins['D_metadata']['sha256']}; contrato,14eventos/quatro holds/PSD A/B permanecem intactos.

[INPUT operacional] Nova unidade a178d269-5b24-443a-b59b-4060aebe9a4c enviada à mesma gerente: inventário exclusivamente de nomes/cabeçalhos dos dois arquivos públicos DCC de calibração, limitado a50MiB cada/100MiB total, sem ler linhas numéricas, sem retry automático, sem adotar CAL_B ou abrir D. Solicitação persistida nos slots; aguardar resposta sem cobrança duplicada. A fila conserva uma coordenação antiga bloqueada por geração divergente e zero execuções; limites5/3/1 conferidos no código corrente. Zero provedor remoto/Work nesta etapa, kernel/gate/originais intactos. A recusa automática SBF anterior continua preservada sem repetição.'''
    changes=[]
    for p in (MEM/'TGL_ATLAS.md',MEM/'TGL_INDICE_VIVO.md',MEM/'TGL_CORE_MEMORY.md',ROOT/'ENTREGA_018_F1_HUBBLE.md',ROOT/'ENTREGA_018_F3_PRIMORDIAL_E_RINGDOWN.md'):
        old=p.read_bytes();assert MARK.encode() not in old
        new=old+('\r\n\r\n'+note.replace('\n','\r\n')+'\r\n').encode()
        assert p.read_bytes()==old
        safe_write(p,new);assert p.stat().st_size>len(old)
        changes.append({'before_bytes':len(old),'after':file_info(p)})
    p=ROOT/'CONTINUIDADE.json';old=p.read_bytes();v=json.loads(old)
    v['updated_at']=now
    v['phases']['F1']='E45_COMPLETE; CONDITIONAL_BOUND_AND_EIGHT_CONTROLS_ACCEPTED; CONSOLIDATED_DRAFT_REVIEW_ACCEPTED; OBSERVED_COMPOSITE_CLOSED'
    v['phases']['F3']='INIT003_TERMINAL_UNQUALIFIED; GUARD_STATIC_REVIEW_AND_21_DOUBLES_PASS; D_METADATA_DOCUMENTED; CALIBRATION_MEMBER_INVENTORY_PENDING; D_CLOSED'
    v['F9_consolidated_review_accepted']=pins['F9_review'];v['guard_doubles_receipt']=pins['doubles'];v['D_metadata_documented']=pins['D_metadata']
    v['milestone_sequences']=sorted(set(v.get('milestone_sequences',[])+[494,495,496,497,498]))
    v['next_steps']=['Review proposed rational tail envelope before implementation; no observed data.',
                     'Prepare real operational integration checks separately from already consumed doubles and INIT003, without new PE authorization.',
                     'Receive requested D calibration member inventory; complete concrete DQ/injection/calibration policy.',
                     'Finish reviewable F1/F3 preparation before requesting operator decision on data opening under ORDEM018 section6.']
    assert p.read_bytes()==old;save_json(p,v);changes.append({'after':file_info(p)})
    save_json(out,{'at':now,'marker':MARK,'pins':pins,'changes':changes,'backup_policy':'Same-folder exact-byte backup before atomic replacement; CAS; no backup deletion.'})
    p=ROOT/'MANIFESTO_CONSOLIDACAO_PARCIAL.json';old=p.read_bytes();m=json.loads(old);previous=file_info(p)
    paths={Path(e['path']) for e in m['files']}
    paths.update(ROOT/n for n in ('RECIBO_ROOT_CONTROLES_COTA_CONCLUIDOS.json','RECIBO_MEMORIA_CONTROLES_E_GUARD_REVIEW.json','RECIBO_ROOT_DOUBLES_GUARD_PASS.json','RECIBO_ROOT_D_METADATA_E_F9_REVIEW.json','RECIBO_MEMORIA_DOUBLES_D_METADATA.json','D_METADATA_SEMANTICS_REQUEST.json','D_CALIBRATION_MEMBER_INVENTORY_REQUEST.json'))
    for folder in ('f9_consolidated_draft','f9_calibration_bound/controls_preparation','proveniencia/revisao_f9_consolidado','preregistros/conjunto_d/audit_guard_repair_preparation','preregistros/conjunto_d/revisao_audit_guard_repair','preregistros/conjunto_d/guard_doubles_run_preparation','preregistros/conjunto_d/d_metadata_semantics'):
        paths.update(q for q in (ROOT/folder).rglob('*') if q.is_file() and '.bak_' not in q.name and '__pycache__' not in q.parts)
    assert all(q.resolve().is_relative_to(ROOT.resolve()) for q in paths)
    m.update(updated_at=now,status='PARTIAL_CURRENT_BYTES_8_CALIBRATION_CONTROLS_21_DOUBLES_PASS_DOCUMENTARY_D_F9_REVIEW_NO_OPENING',previous_snapshot=previous,files=[file_info(q) for q in sorted(paths,key=lambda q:str(q).casefold())])
    assert p.read_bytes()==old;save_json(p,m)
    print(json.dumps({'receipt':file_info(out),'manifest':file_info(p),'files':len(m['files'])}))

if __name__=='__main__':main()
