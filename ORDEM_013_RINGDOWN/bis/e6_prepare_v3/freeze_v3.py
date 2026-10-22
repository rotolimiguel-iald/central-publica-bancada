"""Freeze a one-label correction only; no E6 execution or contract expansion."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os

H=Path(__file__).resolve().parent
V2=H.parent/'e6_prepare_v2'
B=H.parents[1]


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def emit(name,value):
    raw=value.encode() if isinstance(value,str) else (json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode()
    if len(raw)>25_000_000:raise ValueError('Size cap')
    p=H/name;t=p.with_name(p.name+'.pending')
    with t.open('xb') as f:f.write(raw)
    if t.stat().st_size!=len(raw):raise ValueError('Short write')
    os.link(t,p);t.unlink()


def main():
    before=(V2/'generate_reach_table.py').read_bytes();after=(H/'generate_reach_table.py').read_bytes()
    old=b"('N90_information_target','operational_information_target','source_declared_information')"
    new=b"('N90_information_target','operational_information_target','sum_inverse_variance_dtau')"
    if before.count(old)!=1 or before.replace(old,new)!=after:raise ValueError('Delta is not exactly one semantic label')
    for name in ('CONTRACT.json','OUTPUT_SCHEMA.json','SOURCE_PINS.json','STAGE_RECEIPT_SCHEMA.json'):
        if sha(H/name)!=sha(V2/name):raise ValueError('Unexpected contract change')
    v2manifest=json.loads((V2/'PREPARATION_MANIFEST_V2.json').read_bytes())
    if any(sha(V2/name)!=p['sha256'] for name,p in v2manifest['artifacts'].items()):raise ValueError('V2 changed')
    tests=json.loads((H/'FIXTURE_RESULTS_V2_002.json').read_bytes())
    if tests['negative_accepted'] or tests['failures'] or tests['generator_sha256']!=sha(H/'generate_reach_table.py'):
        raise ValueError('Current test evidence mismatch')
    source_files=[B/'refeito/e0_rate_and_o5_scenarios_013bis.py',B/'bis/e0_core/calculate_e0_core.py']
    sources={p.relative_to(B.parent).as_posix():sha(p) for p in source_files}
    emit('DELTA_AND_HANDOFF_V3.md',f'''# E6 V3 — correção focal O5, congelada para R

**READY_FOR_FOCUSED_INDEPENDENT_CLOSING_NOT_AUTHORIZED.** Diretório definitivo: `bis/e6_prepare_v3`. V1 e V2 preservadas; V2 reconferida byte a byte contra seu manifesto. O snapshot integral anterior permanece em `superseded_freeze_001/` nesta V3. Manifestações V2 copiadas nesta árvore são proveniência histórica; o manifesto corrente é `PREPARATION_MANIFEST_V3.json`.

Delta executável **exatamente uma substituição de rótulo** em `assemble_baselines`: `operational_information_target` O5 recebe `sum_inverse_variance_dtau`, em vez de `source_declared_information`. Fonte declarada: `e0_rate_and_o5_scenarios_013bis.py` transporta `r['I_tau_target90']`; `calculate_e0_core.py` define informação de dtau como soma de 1/sigma². Os dois arquivos foram apenas lidos e pinados no manifesto. Nenhum número recalculado, fonte editada ou contrato expandido.

O contrato/schema semântico continua V2 e é byte a byte idêntico ao congelado. O nome V3 identifica esta revisão do pacote/código. R1/R2/R4/R5 e demais ramos R3 não mudaram. Os 32 valores não nulos entre 80 cenários O5 apontados por R deixam de falhar pela unidade; a presente verificação de execução usa somente um O5 fictício, não monta dados reais.

Rodada preservada `FIXTURE_RESULTS_V2_002.json`: **{tests['passed']}/{tests['total']} checks**, negativos aceitos=0. Inclui positivo O5 com informação dummy não nula e pointer preservado; negativo rejeita o antigo rótulo sem tipo. Inclui regressão dos cinco achados e 180 células vazias. A rodada foi concluída antes da separação dos diretórios V2/V3; hashes do código testado e script conferem com estes bytes. V2 foi restaurada de seu snapshot sem divergências; nenhuma fonte científica foi executada na operação.

Encaminhar a R este delta, manifesto V3 e evidências para fechamento focal. Não executar E6. Nenhuma autorização real E6, nenhum estágio real, nenhuma extração E7 ou conclusão da ordem. O helper de paredes será preparado separadamente depois deste freeze.
''')
    files={p.relative_to(H).as_posix():dict(sha256=sha(p),bytes=p.stat().st_size) for p in sorted(H.rglob('*')) if p.is_file()}
    if any(p['bytes']>25_000_000 for p in files.values()):raise ValueError('File cap')
    manifest=dict(schema='E6_PREPARATION_MANIFEST_V3',status='FROZEN_AWAITING_R_CLOSING',frozen_utc=datetime.now(timezone.utc).isoformat(),
        artifacts=files,predecessor_manifest_sha256=sha(V2/'PREPARATION_MANIFEST_V2.json'),v2_preserved=True,
        delta_exactly_one_label=True,source_definition_pins=sources,contract_unchanged_from_V2=True,
        activation_package_sha256={n:sha(H/n) for n in ('generate_reach_table.py','CONTRACT.json','SOURCE_PINS.json','OUTPUT_SCHEMA.json')},
        cases=tests['total'],negative_accepted=[],actual_E6_executed=False,actual_authorization_created=False,
        fixture_sha256=sha(H/'FIXTURE_RESULTS_V2_002.json'),order_completed=False)
    emit('PREPARATION_MANIFEST_V3.json',manifest)
    print(json.dumps(dict(manifest_sha256=sha(H/'PREPARATION_MANIFEST_V3.json'),generator_sha256=sha(H/'generate_reach_table.py'),
        delta_sha256=sha(H/'DELTA_AND_HANDOFF_V3.md'),fixture_sha256=sha(H/'FIXTURE_RESULTS_V2_002.json'),status=manifest['status'])))


if __name__=='__main__':main()
