"""Archive the scoped investigation and append its verified operational memory."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

from install_canonical import install_file
from record_universe_delivery import append, CANON, CENTRAL

HERE = Path(__file__).resolve().parent
OUT = HERE / 'state' / 'investigation_20260928'
REPORT = HERE / 'INVESTIGACAO_PRIORIDADES_20260928.md'
STACK = HERE.parent / 'IALD_ORQUESTRACAO_20260923' / 'ORDEM_018_TESTE_SENSIBILIDADE'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def new_atomic(path, data):
    if path.exists():
        if path.read_bytes() != data:
            raise RuntimeError(f'Refusing to replace prior artifact: {path}')
        return
    temp = path.with_name(path.name + '.tmp')
    with temp.open('xb') as handle:
        handle.write(data)
    if temp.stat().st_size != len(data):
        raise RuntimeError('Incomplete artifact')
    temp.replace(path)


def write_json(path, value):
    new_atomic(path, (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))


def prepare():
    for name in ('MIMO_OPPORTUNITY_RESULT_DECLARADO.txt', 'MIMO_OPPORTUNITY_LOCAL_AUDIT.json'):
        new_atomic(OUT / name, (STACK / name).read_bytes())
    audit = json.loads((OUT / 'MIMO_OPPORTUNITY_LOCAL_AUDIT.json').read_text(encoding='utf-8'))
    assert sha(OUT / 'MIMO_OPPORTUNITY_RESULT_DECLARADO.txt') == audit['raw_result_sha256']
    # C=diag(1,4), J=(1,1)^T. Whitened A=(1,.5)^T.
    a = (1., .5)
    p = ((.2, -.4), (-.4, .8))
    original_coordinate_p = ((.2, -.2), (-.8, .8))
    apply = lambda matrix, vector: [sum(x*y for x,y in zip(row,vector)) for row in matrix]
    good = math.hypot(*apply(p,a))
    bad = math.hypot(*apply(original_coordinate_p,a))
    assert good < 1e-14 and bad > .4
    x = .0625137033
    target = .5*math.erfc(5/math.sqrt(2))
    write_json(OUT/'mimo_independent_review.json', {
        'status': 'PASS_WITH_CORRECTIONS_TO_PROVIDER_PROPOSAL',
        'scope': 'ALGEBRA_AND_BASIC_COVERAGE_NOT_NEW_PHYSICAL_FIT',
        'raw_result_sha256': sha(OUT/'MIMO_OPPORTUNITY_RESULT_DECLARADO.txt'),
        'correct_whitened_projector_times_A_norm': good,
        'wrong_coordinate_projector_times_A_norm': bad,
        'delta_tau_exact': -x/(1+x), 'delta_tau_linear': -x,
        'gaussian_one_sigma_coverage': math.erf(1/math.sqrt(2)),
        'one_sided_five_sigma_tail': target,
        'zero_exceedances_10000_upper_95': -math.expm1(math.log(.05)/10000),
        'zero_exceedances_count_needed_for_95_upper_below_target': math.ceil(math.log(.05)/math.log1p(-target)),
        'review_document': 'MIMO_REVISAO_COORDENACAO.md',
    })
    for name in ('system_measurement.json', 'bao_independent_review.json', 'gw_independent_review.json', 'other_domains_independent_review.json'):
        assert json.loads((OUT/name).read_text(encoding='utf-8'))['status'] == 'PASS', name
    files = sorted(p for p in OUT.rglob('*') if p.is_file() and p.name != 'MANIFESTO_ENTREGA.json' and '__pycache__' not in p.parts and '.bak_' not in p.name and not p.name.endswith('.tmp'))
    files += [REPORT, Path(__file__).resolve()]
    write_json(OUT/'MANIFESTO_ENTREGA.json', {
        'date': '2026-09-28', 'status': 'INVESTIGATION_COMPLETED_NO_NEW_GLOBAL_SIGNIFICANCE',
        'canonical_originals_modified': False, 'scientific_gate_modified': False,
        'resident_service_restarted': False, 'new_event_fit': False,
        'mimo': {'job_id': audit['job_id'], 'request_id': audit['request_id'], 'status': 'completed', 'review': 'CORRECTIONS_REQUIRED_RECORDED'},
        'kimi': {'job_id': '0898f7cb-bd8e-4d67-96e9-e44e03a19762', 'request_id': '26caa026-a881-4cc8-b8e4-1b138621ce19', 'status': 'failed', 'retried': False, 'source': 'OFFICIAL_COORDINATOR_MESSAGE'},
        'local_agents_completed': ['BAO_CMB', 'GW_ECHO_RINGDOWN', 'VOIDS_NEUTRINOS_CLOCKS'],
        'files': [{'path': p.relative_to(HERE).as_posix(), 'bytes': p.stat().st_size, 'sha256': sha(p)} for p in files],
    })
    print(json.dumps({'status':'PREPARED', 'files': len(files), 'report_sha256': sha(REPORT)}))


def deliver():
    manifest = json.loads((OUT/'MANIFESTO_ENTREGA.json').read_text(encoding='utf-8'))
    for row in manifest['files']:
        assert sha(HERE/row['path']) == row['sha256'], row['path']
    memories = [root/name for root in (HERE, CANON) for name in ('MEMORIA_CENTRAL.md', 'REGISTRO_DAS_CONVERSAS.md', 'PLANO_UNIVERSO_RESIDENTE.md', 'DESENHO_DO_COCKPIT.md')]
    memories += [CENTRAL/'memory'/name for name in ('TGL_ATLAS.md','TGL_INDICE_VIVO.md','TGL_CORE_MEMORY.md')]
    assert all(p.is_file() for p in memories)
    for row in manifest['files']:
        install_file(row['path'])
    install_file((OUT/'MANIFESTO_ENTREGA.json').relative_to(HERE).as_posix())
    marker = 'TGL_INVESTIGATION_20260928_' + sha(REPORT)[:16]
    passage = f'''## 28/09/2026 — Investigação da bancada com agentes, sem novo sigma

[INPUT] Operador pediu examinar o sistema residente e investigar com agentes onde há melhores condições de testar a TGL.

[REAL] Três agentes locais concluídos e verificações independentes PASS: 21 cenários BAO; 29 fontes GW e inversão de Q; sete blocos canônicos e trechos do programa. MiMo concluiu parecer, preservado como DECLARADO com correções matemáticas/estatísticas ao lado. Kimi falhou sem resposta aceita, sem repetição. Nenhum resultado novo atribuído a Claude/DeepSeek nesta rodada.

[REAL — sistema] 180/180 arquivos GW, 22,50550 GiB de arrays, swap zero, seis vistas em 31–80 ms, mesmo load_id e nenhuma releitura. É ensaio em uma série, não benchmark de ajuste/concorrência. Catálogo 1.350 arquivos/~72 GiB inclui duplicatas. BAO residente contém 13 pontos e covariância 13x13; não representa todos os catálogos/mapas. GPU atende renderização; cálculo científico em GPU não medido.

[REAL/DERIVED — achados] Na comparação BAO, escala e densidade reduzem d² de 0,55873894 para 0,00473259 (99,153% da distância quadrática), exemplo entre modelos, não fit/sigma. Um modo de ringdown é compensável por massa/spin na aproximação exploratória BCW. C6 segue INCONCLUSIVE_SYSTEMATICS, lnB primário -0,002595.

[CORREÇÃO AO LADO — ACT V9] Fisher compara delta_c=-0,95, s1=1, pisos 0 e beta. O perfil é >=0,05>beta: os dois modelos são idênticos antes do ruído, F=0 estrutural nesse ensaio. Fonte e linhas conferidas; controle positivo delta_c=-1 ativa o piso, mas é diagnóstico, não nova previsão/inferência. A grade de likelihood posterior é distinta e não foi declarada toda cega. Preservado o UNDERPOWERED histórico; sua causa não pode ser atribuída somente à sensibilidade do ACT. Nenhum original alterado.

[PLANO] D10 CMB–BAO mantém prioridade estratégica: ligar tradução perturbativa/r_d e likelihoods existentes com covariâncias/overlaps. Auditar primeiro a sensibilidade ACT em cópia; para GW, diagnóstico 220+440 do mesmo remanescente na métrica de ruído, projetando nuisance e exigindo amplitude informativa. Neutrino é confronto condicionado; ecos exigem recuperação qualificada; relógios P1 têm déficit de sensibilidade no protocolo atual. Nenhuma rota recebeu poder 5sigma global demonstrado.

[ESCOPO] Relatório `{CANON / REPORT.name}` (SHA256 {sha(REPORT)}). Evidências/manifesto em `{CANON / 'state' / OUT.name}`; hashes calculados por script. Serviços/RAM preservados, sem alteração de original científico, kernel, gate, interface, app público/mobile. Memórias operacionais desta bancada e índices centrais recebem append com backup de bytes; linhagem científica Nós não tocada porque nenhuma versão foi selada.
'''
    for path in memories:
        append(path, passage, marker)
        assert marker.encode() in path.read_bytes()
    for row in manifest['files']:
        assert sha(CANON/row['path']) == row['sha256']
    delivery = {'status':'PASS', 'created_utc':datetime.now(timezone.utc).isoformat(), 'marker':marker,
                'files_verified':len(manifest['files']), 'memories_updated':len(memories),
                'report_sha256':sha(REPORT), 'manifest_sha256':sha(OUT/'MANIFESTO_ENTREGA.json')}
    # Delivery receipt is a new, uniquely dated operational artifact.
    path = OUT/('DELIVERY_'+datetime.now().strftime('%Y%m%d_%H%M%S')+'.json')
    write_json(path,delivery)
    install_file(path.relative_to(HERE).as_posix())
    print(json.dumps(delivery))


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('mode',choices=['prepare','deliver'])
    args=parser.parse_args()
    prepare() if args.mode=='prepare' else deliver()
