"""Record the conditional proof and verify immutable delivery; standard library only."""
import hashlib
import importlib.util
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
CENTRAL = Path(r'C:\IALD\Central de Patentes')
REQUEST = '6273a822-5880-4742-a82c-b7cf93f7c128'
MARKER = 'F9_CALIBRATION_BOUND_' + REQUEST


def pin(path):
    data = path.read_bytes()
    return {'path': str(path), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def new(path, value):
    data = value.encode('utf-8') if isinstance(value, str) else (
        json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    if path.exists():
        raise FileExistsError(str(path))
    tmp = path.with_name(path.name + '.tmp')
    with tmp.open('xb') as stream:
        stream.write(data)
    if tmp.read_bytes() != data:
        raise OSError('Temporary verification failed')
    os.rename(tmp, path)
    if path.read_bytes() != data:
        raise OSError('Final verification failed')


def main():
    now = datetime.now(timezone.utc).isoformat()
    sources = json.loads((HERE / 'SOURCES.json').read_text(encoding='utf-8'))
    for item in sources['sources']:
        for role in ('original', 'snapshot'):
            if pin(Path(item[role]['path'])) != item[role]:
                raise ValueError('Source or snapshot changed: ' + item[role]['path'])
    candidate_pin = pin(HERE / 'CALIBRATION_BOUND_CANDIDATE.json')
    proof_pin = pin(HERE / 'PROVA_COTA_CALIBRACAO_F9.md')
    text = f'''## 06/10/2026 — F9: envelope analítico de cauda, proposta documental

[INPUT] Unidade `{REQUEST}` delegada pela coordenação: evitar Monte Carlo extremo obrigatório por uma cota conservadora de tamanho finito. Diretório `{HERE}`. Pedido preservado, sem abertura observada, solver, simulação, ajuste ou nova chamada de provedor.

[DERIVED condicional — revisão independente pendente] Erro gaussiano com C fixa/conhecida/comum, suporte afim comum e X63 suportado: R X=0, R C R^T=I, nu=rank(C)-63. No parâmetro físico verdadeiro q~chi2_nu; Gnull<=q, Q1<=G1 e Tj1<=Gj. A cauda fornece p superior uniforme, sem Wilks. Não é distribuição exata do mínimo, e não se subtraem parâmetros cosmológicos adicionais.

[DERIVED condicional — refinamento] Se TODAS as diferenças de médias competitor-null estão num subespaço fixo V do quociente, ganho<=||ProjV Z||²~chi2_dimV. No recorte Planck3+BAO13 e resposta local a_h h, limites estruturais17 para Q1/T21/T51; H4 acrescenta c_C e dá18. Não são postos efetivos medidos. Whitening/projeção específicos de cada cenário; não usar espaço tangente local como inclusão global. G1 pode usar limite148 apenas com283linhas,72vínculos exatos de covariância e X63 no suporte. Subset262/143 não substitui267/148.

[PROPOSTA operacional] Para aplicação, certificar L_i<=mínimo_RSS_i<=U_i: ellG=max(0,L1), ellQ=max(0,L1-U3) com aninhamento, ellT=Lj-U1; mínimo local é U, jamais L. Usar SF superior certificada, p1 para limite não positivo, max_s na família inteira e Bonferroni5. Cota fraca válida é não-rejeição conservadora, não falta de calibração; não implica que p exato seja grande. Bayes separado. Erros plug-in/C paramétrica exigem hipótese/prova adicional. V2/VC-01 foi lido, não alterado; predicados de disponibilidade permanecem.

[REAL documental]62checagens de estrutura/pins aprovadas;13snapshots de fontes. Protocolo de8controles sintéticos determinísticos futuros NÃO executado. Nenhuma matriz, posto numérico, cauda, dadoD, centro, y/S/g/H0/lnB/sigma ou poder novo calculado. Contribuição entregue à coordenação oficial para revisão, não ratificação científica. Nenhum original científico, kernel, gate, motor, serviço ou interface modificado.

[REAL operacional separado] Bancada respondeu pronta, motorCUDA, RAM255,5GiB total/153,1livres e RTX5090; retrato read-only, não benchmark. Prioridade operacional: F9 acústica+distâncias locais e piloto ringdown já coordenado, sem duplicar execuções. Capacidade residente facilita consultas/rastreabilidade, não garante detecção.

[DECLARADO — mensagem oficial posterior da ROOT] INIT003 encerrou: GR STOPPED_NOT_CONVERGED e falha de parada após tentativas de cachepyc bloqueadas; segundo job RB interrompido sem resultado final. Revisão independente em curso; nenhum rerun nem dadosD abertos. O estado anterior em curso é histórico. Esta unidade6273 não executou/inspecionou ciência do piloto e segue exclusivamente documental.

[ARTEFATOS] PROVA_COTA_CALIBRACAO_F9.md SHA256 {proof_pin['sha256']}; CALIBRATION_BOUND_CANDIDATE.json SHA256 {candidate_pin['sha256']}; PROTOCOLO_CONTROLES_FUTUROS.json; SOURCES.json; VALIDACAO_DOCUMENTAL.json; CONTEXTO_DA_INVESTIGACAO.md. Ler os recibos posteriores de revisão/decisão antes de implementar. Âncora científica histórica consultada v386 permanece histórica; esta unidade não executou nem verificou nova versão do um.py.
'''
    new(HERE / 'MEMORIA_DA_UNIDADE.md', text + '\n')
    helper = CENTRAL / 'Chatgpt/TGL_BANCADA_OFICIAL/record_universe_delivery.py'
    spec = importlib.util.spec_from_file_location('byte_backup_append', helper)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    paths = [CENTRAL / 'memory' / name for name in (
        'TGL_ATLAS.md', 'TGL_INDICE_VIVO.md', 'TGL_CORE_MEMORY.md')]
    paths += [CENTRAL / 'Chatgpt/TGL_BANCADA_OFICIAL' / name for name in (
        'MEMORIA_CENTRAL.md', 'REGISTRO_DAS_CONVERSAS.md')]
    receipts = []
    for path in paths:
        before = path.read_bytes()
        before_pin = pin(path)
        backups_before = set(path.parent.glob(path.name + '.bak_*'))
        module.append(path, text, MARKER)
        after = path.read_bytes()
        if not after.startswith(before) or MARKER.encode() not in after or len(after) <= len(before):
            raise ValueError('Additive memory verification failed: ' + str(path))
        new_backups = set(path.parent.glob(path.name + '.bak_*')) - backups_before
        exact = [p for p in new_backups if p.read_bytes() == before]
        if len(exact) != 1:
            raise ValueError('Immediate exact byte backup not found: ' + str(path))
        receipts.append({'before': before_pin, 'backup': pin(exact[0]), 'after': pin(path),
                         'additive_verified': True})
    new(HERE / 'MEMORY_UPDATE_RECEIPT.json', {'created_utc': now, 'marker': MARKER,
        'surfaces': receipts, 'other_houses_written': False})

    excluded = {'MANIFESTO_ENTREGA.json', 'FINAL_CHECK.json', 'RECIBO_MAPA.json'}
    artifacts = [pin(p) for p in sorted(HERE.rglob('*')) if p.is_file() and
                 p.name not in excluded and '.tmp' not in p.name and '.bak_' not in p.name]
    manifest = {'request_id': REQUEST, 'created_utc': now,
        'status': 'DOCUMENTARY_DELIVERY_FOR_INDEPENDENT_REVIEW_NOT_SCIENTIFIC_RATIFICATION',
        'artifacts': artifacts, 'source_snapshot_count': len(sources['sources']),
        'opening_authorized': False, 'new_science_executed': False,
        'simulations': 0, 'solver_runs': 0, 'model_provider_calls': 0,
        'observed_data_D_opened': False, 'originals_modified': False,
        'consumed_verdict_contract_modified': False,
        'review_status_at_delivery': 'PENDING',
        'map_receipt_policy': 'Recorded after manifest; its status does not change scientific adoption'}
    new(HERE / 'MANIFESTO_ENTREGA.json', manifest)
    all_match = all(pin(Path(item['path'])) == item for item in artifacts)
    if not all_match:
        raise ValueError('Delivery file changed during final verification')
    final = {'status': 'PASS_CUSTODY_ONLY', 'request_id': REQUEST, 'created_utc': now,
        'files_verified': len(artifacts), 'manifest': pin(HERE / 'MANIFESTO_ENTREGA.json'),
        'proof': proof_pin, 'candidate': candidate_pin, 'all_hashes_match': all_match,
        'no_numeric_science': True, 'memory_surfaces_updated': len(receipts)}
    new(HERE / 'FINAL_CHECK.json', final)
    print(json.dumps(final, ensure_ascii=False))


if __name__ == '__main__':
    main()
