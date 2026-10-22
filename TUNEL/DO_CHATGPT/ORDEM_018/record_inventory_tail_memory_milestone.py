"""Append a verified documentary milestone with byte backups and CAS."""
from pathlib import Path
from datetime import datetime, timezone
import json
from audit_inputs import file_info, save_json, safe_write

ROOT = Path(__file__).resolve().parent
MEM = Path(r'C:\IALD\Central de Patentes\memory')
MARK = '<!-- ORDEM018_CALIBRATION_INVENTORY_TAIL_V2_REPORT_20261006 -->'


def main():
    out = ROOT / 'RECIBO_MEMORIA_INVENTARIO_ENVELOPE_V2.json'
    assert not out.exists()
    receipt_path = ROOT / 'RECIBO_ROOT_INVENTARIO_CALIBRACAO_ENVELOPE_V2_CONSOLIDACAO.json'
    receipt = json.loads(receipt_path.read_bytes())
    assert receipt['status'] == 'DOCUMENTARY_DELIVERIES_VERIFIED_NOT_SCIENTIFIC_ADOPTION'
    pins = {'root_receipt': file_info(receipt_path),
            'inventory': receipt['manifests']['D_inventory']['manifest'],
            'tail': receipt['manifests']['tail_V2']['manifest'],
            'review': receipt['manifests']['tail_V2_review']['manifest'],
            'report': file_info(ROOT / 'CONSOLIDACAO_018_PARA_DECISAO.md'),
            'MM_request': file_info(ROOT / 'F9_MM_MODEL_PREPARATION_REQUEST.json')}
    request = json.loads(Path(pins['MM_request']['path']).read_bytes())
    assert request['status'] == 'SENT_DOCUMENTARY_RESPONSE_PENDING' and request['official_send_ack']
    now = datetime.now(timezone.utc).isoformat()
    note = f'''{MARK}
## 06/10/2026 UTC — Inventário de calibração, correção da cauda e consolidação provisória

[REAL documental — mapa504] A unidade a178d269 foi entregue pela gerente oficial e seus24 arquivos conferidos por ROOT. Dois pacotes DCC somam63271057 bytes;16408 cabeçalhos contêm16404 arquivos regulares e4diretórios. Foram identificados28 candidatos nominais evento/detector. GW241111_111552 usa épocas candidatas distintas emH1/L1; cinco espaçamentos entre nomes vizinhos superam1h. Proximidade/intervalos de nomes não provam validade de calibração nem lacunas de strain. Somente cabeçalhos foram interpretados; nenhum membro extraído ou linha numérica de calibração analisada. CAL_B, contratos,14eventos/quatro holds e aberturaD permanecem pendentes/intactos. Manifesto SHA256 {pins['inventory']['sha256']}.

[REAL documental / DERIVED condicional — mapas498/501/502/503] Revisão independente encontrou TE-01 no primeiro contrato da cauda. A propostaV2 corrigiu F9 com dimensão0 e limite estatístico positivo para INVALID/null e CONTRACT_INCOHERENCE_NOT_REJECTION antes de recursos/agregação. O átomo matemático não autoriza rejeição automática. Ramo positivo, N256/Q10^30, modelos, alpha eBonf5 preservados. ROOT leu contrato/casos/adendo e conferiu os manifestos; V2 SHA256 {pins['tail']['sha256']}, revisão SHA256 {pins['review']['sha256']}. Preparação de módulo/controles delimitados foi delegada separadamente, sem execução, abertura ou adoção científica neste marco.

[REAL documental — mapa500] ROOT aceitou a consolidação provisória como fotografia documental, nãoF4 nem conclusão da missão. Foram conferidas42 versões de fontes; duas versões anteriores de acumuladores F1/F3 foram recuperadas dos backups byte-a-byte compatíveis com os pins. Relatório SHA256 {pins['report']['sha256']}. F0/F2 entregues no alcance declarado; F1/F3 ainda incompletas. Nenhuma reprodução científica ou controle consumido foi repetido para esta conferência.

[INPUT operacional] Nova unidade {request['request_id']} enviada uma vez à gerente: especificação simbólica/documental dos cinco termosMM/maser, comparando experimento gaussiano condicional com medida primitiva/transformação e respectivas consequências para covariância/suporte/calibração. Somente fontes locais já admitidas, sem valores centrais, downloads, execução científica ou modelos. Resposta pendente no ledger de slots; não repetir solicitação. Em paralelo seguem a preparação do envelope e da integração stdlib real do guard, sem novaPE.

[REAL operacional] A consulta next falhou novamente na validação da geração canônica da única coordenação antiga; registrado needs_attention, nunca idle falso. Zero execuções da fila; pin original, falhas/incertezas e bloqueio preservados. Não houve chamada de executor/Work nem mudança de automação, kernel, gate ou originais. Recibo ROOT SHA256 {pins['root_receipt']['sha256']}. A recusa automática anterior do download SBF continua preservada, sem repetição ou troca de rota para contorná-la.'''
    changes = []
    for p in (MEM / 'TGL_ATLAS.md', MEM / 'TGL_INDICE_VIVO.md', MEM / 'TGL_CORE_MEMORY.md',
              ROOT / 'ENTREGA_018_F1_HUBBLE.md', ROOT / 'ENTREGA_018_F3_PRIMORDIAL_E_RINGDOWN.md'):
        old = p.read_bytes()
        assert MARK.encode() not in old
        new = old + ('\r\n\r\n' + note.replace('\n', '\r\n') + '\r\n').encode()
        assert p.read_bytes() == old
        safe_write(p, new)
        assert p.stat().st_size > len(old)
        changes.append({'before_bytes': len(old), 'after': file_info(p)})
    p = ROOT / 'CONTINUIDADE.json'; old = p.read_bytes(); v = json.loads(old)
    v.update(updated_at=now, documentary_milestone=pins,
             calibration_member_inventory_status='RECEIVED_AND_VERIFIED_NO_NUMERIC_ENVELOPE_OR_D_OPENING',
             tail_envelope_status='V2_DOCUMENTARY_REVIEW_ACCEPTED_IMPLEMENTATION_PREPARATION',
             MM_model_status='DOCUMENTARY_SYMBOLIC_REQUEST_SENT_PENDING')
    v['milestone_sequences'] = sorted(set(v.get('milestone_sequences', []) + [498, 500, 501, 502, 503, 504]))
    v['phases']['F1'] = 'CONSOLIDATED_DRAFT_REVIEW_ACCEPTED; TAIL_IMPLEMENTATION_PREPARATION; MM_SYMBOLIC_CONTRACT_PENDING; OBSERVED_COMPOSITE_CLOSED'
    v['phases']['F3'] = 'INIT003_TERMINAL_UNQUALIFIED; GUARD_REAL_STDLIB_INTEGRATION_PREPARATION; D_CALIBRATION_MEMBER_INVENTORY_VERIFIED; D_CLOSED'
    assert p.read_bytes() == old; save_json(p, v); changes.append({'after': file_info(p)})
    save_json(out, {'at': now, 'marker': MARK, 'pins': pins, 'changes': changes,
                    'policy': 'Same-folder exact-byte backup, verified temporary file, atomic replace, CAS; no backup removal.'})
    p = ROOT / 'MANIFESTO_CONSOLIDACAO_PARCIAL.json'; old = p.read_bytes(); m = json.loads(old)
    previous = file_info(p); paths = {Path(x['path']) for x in m['files']}
    paths.update(ROOT / n for n in ('RECIBO_ROOT_INVENTARIO_CALIBRACAO_ENVELOPE_V2_CONSOLIDACAO.json',
                 'RECIBO_MEMORIA_INVENTARIO_ENVELOPE_V2.json', 'CONSOLIDACAO_018_PARA_DECISAO.md',
                 'CONSOLIDACAO_018_PARA_DECISAO.json', 'F9_MM_MODEL_PREPARATION_REQUEST.json'))
    for folder in ('preregistros/conjunto_d/d_calibration_member_inventory', 'f9_tail_envelope_proposal',
                   'f9_tail_envelope_proposal_v2', 'derivacoes/revisao_tail_envelope', 'proveniencia/consolidacao_018'):
        paths.update(q for q in (ROOT / folder).rglob('*') if q.is_file() and '.bak_' not in q.name and '__pycache__' not in q.parts)
    assert all(q.resolve().is_relative_to(ROOT.resolve()) for q in paths)
    m.update(updated_at=now, status='PARTIAL_DOCUMENTARY_INVENTORY_TAIL_V2_ACCEPTED_IMPLEMENTATION_PENDING_NO_OPENING',
             previous_snapshot=previous, files=[file_info(q) for q in sorted(paths, key=lambda x: str(x).casefold())])
    assert p.read_bytes() == old; save_json(p, m)
    print(json.dumps({'receipt': file_info(out), 'manifest': file_info(p), 'files': len(m['files'])}))


if __name__ == '__main__':
    main()
