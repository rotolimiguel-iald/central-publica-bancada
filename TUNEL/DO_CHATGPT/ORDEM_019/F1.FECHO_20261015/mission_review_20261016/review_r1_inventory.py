"""Independent inventory reconciliation; hashes and existing receipts, no builds."""
import datetime as dt
import json
import re
import subprocess
from pathlib import Path
from finish_requirement_reviews import OUT, BASE, REFERENCE, PYTHON, CLI, ACTOR, read, pin, fresh

def main():
    checked = {}
    def verify(entry):
        actual = pin(entry['path'])
        assert actual['sha256'] == entry['sha256'], entry['path']
        checked[actual['path']] = actual
        return actual
    def walk(value):
        if isinstance(value, dict):
            if 'path' in value and 'sha256' in value:
                verify(value)
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)
    inventory_path = BASE / 'network_reuse/INVENTARIO_REAPROVEITAMENTO_R1.json'
    inventory = read(inventory_path)
    progress34 = read(BASE / 'PROGRESS_R34.json')
    progress35 = read(BASE / 'PROGRESS_R35.json')
    current_path = REFERENCE.parent / 'CURRENT_REQUIREMENTS_INVENTORY.json'
    current = read(current_path)
    roots = [inventory_path, BASE / 'PROGRESS_R34.json', BASE / 'PROGRESS_R35.json', current_path,
             BASE / 'PROGRESS_R31.json', BASE / 'PROGRESS_R33.json',
             BASE / 'PROVENIENCIA_V393_REUSO_V351_R1.json',
             OUT / 'PHYSICAL_GLOBAL_NET_REVIEW_R1.json']
    for path in roots:
        checked[str(path)] = pin(path)
        if path.name != 'PHYSICAL_GLOBAL_NET_REVIEW_R1.json':
            walk(read(path))
    anchors = []
    for entry in inventory['sources']:
        verify(entry)
        lines = Path(entry['path']).read_text(encoding='utf-8-sig').splitlines()
        for anchor in entry['anchors']:
            found = [i+1 for i,line in enumerate(lines) if anchor['needle'] in line]
            assert found == anchor['lines'], (entry['path'],anchor,found)
            anchors.append({'path':entry['path'],'needle':anchor['needle'],'lines':found})
    provenance = read(BASE / 'PROVENIENCIA_V393_REUSO_V351_R1.json')
    for field in ('program','seal'):
        verify({'path':provenance[field+'_path'],'sha256':provenance[field+'_sha256']})
    receipt = read(progress35['build']['path'])
    assert receipt['exit_code'] == 0
    walk(receipt['source'])
    walk(receipt['artifacts'])
    build_dir = Path(progress35['build']['path']).parent
    log = (build_dir / 'AXIOMS.txt').read_text(encoding='utf-8')
    parsed = {n: sorted(a.strip() for a in s.split(',') if a.strip())
        for n,s in re.findall(r"'([^']+)'\s+depends on axioms:\s*\[([^\]]*)\]",log)}
    expected = re.findall(r'^#print axioms (\S+)', Path(progress35['source']['path']).read_text(encoding='utf-8'), re.M)
    assert len(expected) == 11 and set(expected) <= set(parsed)
    assert all(set(parsed[n]) <= {'propext','Classical.choice','Quot.sound'} for n in expected)
    sync_raw = subprocess.run([PYTHON,'-B','-X','utf8',CLI],
        input=json.dumps({'operation':'project','reference':str(REFERENCE),'max_chars':60000}),
        text=True,encoding='utf-8',capture_output=True,check=True)
    sync = json.loads(sync_raw.stdout)
    assert sync['ok']
    projection = sync['result']['projection']
    tasks = {t['id']:t for t in projection['active']+projection['settled']}
    assert projection['context_id'] == read(REFERENCE)['context_id']
    assert tasks['R1']['status'] == 'review_pending'
    assert tasks['M0_MEMORIA']['status'] == 'satisfied'
    assert not projection['hold']
    for entry in tasks['R1']['evidence']:
        verify(entry)
    fresh(OUT / 'R1_REVIEW_PROJECT.json', sync)
    mechanical = {
        'statute':'REAL','checked_pins':list(checked.values()),
        'original_inventory_sources':len(inventory['sources']),
        'anchors_checked':anchors,
        'classes':sorted({entry['classification'] for entry in inventory['sources']}),
        'r35_existing_build':{'receipt':pin(progress35['build']['path']),'exit_code':0,
            'printed_declarations':{n:parsed[n] for n in expected},
            'scope':'Existing result inspected; no independent recompilation.'},
        'script':pin(__file__),'new_builds':0,'provider_calls':0
    }
    fresh(OUT / 'R1_MECHANICAL_VERIFICATION.json', mechanical)
    report = {
        'unit':'F1.FECHO_20261015','requirement':'R1',
        'reviewer':{'id':ACTOR,'kind':'agent'},
        'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
        'mission_reference':pin(REFERENCE),'context_id':projection['context_id'],
        'review_revision':projection['revision'],
        'criterion':tasks['R1']['criterion'],'evidence':tasks['R1']['evidence'],
        'additional_current_evidence':[pin(p) for p in roots[2:]],
        'verification':pin(OUT / 'R1_MECHANICAL_VERIFICATION.json'),
        'verdict':'PASS_CURRENT_REUSE_INVENTORY',
        'findings_blocking_criterion':[],
        'assessment':[
            'O inventário inicial contém 16 fontes, hashes integrais, âncoras verificadas, consumo nomeado e resíduo preciso. Distingue EXISTE_LIGADO, EXISTE_NAO_LIGADO, KNOWN/DERIVED documental e OPEN da construção específica.',
            'A leitura vigente é conjunta e cronológica: inventário inicial, inventário dos requisitos e progressos R31/R33/R34/R35. As pendências antigas permanecem história; não são tratadas como ausência atual dos componentes depois construídos.',
            'BosonicFock/continuidade e CanonicalOutput são reaproveitados por montagens posteriores. PROGRESS_R35 e o fonte antes revisado fornecem a ligação da rede compacta física a KWR e recusam a rede nula. Agora o recibo terminal dessa mesma fonte foi conferido: exit 0 e onze declarações no trio.',
            'R31/R33/R34 registram grupo modular, polar, troca da resolvente e fechamento/CFC como construídos no mesmo GNS, preservando os resíduos de ação direita e traço/PF. A autoria e a ausência de recompilação independente são declaradas.',
            'V351 designa módulos reaproveitados dentro da base v393 pinada; não é retorno a programa antigo. A candidata v394 continua separada da produção.',
            'O inventário e a projeção conservam IDs remotos pendentes sem reenvio; construções locais posteriores não são apresentadas como respostas desses jobs.'
        ],
        'current_reconciliation':{
            'R4':'Normalizações/relógio inventariados; identificação física do mesmo dispositivo continua aberta.',
            'R5':'Rede compacta Maxwell livre de Minkowski ligada a KWR por fonte e build existentes; identificação/realização do dispositivo permanece obrigação própria.',
            'R6':'Fock, Weyl/CCR, vácuo, Gamma(J), BW/KMS reaproveitados; a composição nova já teve leitura de fonte, porém seu build em voo não é aceito por este parecer.',
            'R7':'Peso dual/GNS/Tomita/grupo modular/polar disponíveis nas etapas registradas; traço escalado/PF e ligação final da representação não são inferidos.',
            'R8':'Campos/tensor e pontes existentes reconhecidos; charge_link e certificado conjunto permanecem abertos.',
            'R9':'Aceite anterior preservado: H3 universal é antecedente explícito, sem derivação apenas do estado nas evidências revisadas.',
            'R3_R10':'Rito da candidata final e revisão conjunta permanecem separados.'
        },
        'limits':[
            'Aceite documental do reaproveitamento no estado atual; não aceita R4–R8 nem certifica a entrega científica completa.',
            'Revisão de inventário, fontes/âncoras, pinos e recibos existentes; não refaz todos os teoremas do acervo, provas transitivas ou literatura.',
            'Mudanças futuras exigem incorporar novas evidências ao protocolo. Inventários históricos não são reescritos.',
            'Nenhum gate, quadro, kernel, original, memória global ou provedor alterado. R2/R9 não foram reabertos.'
        ],
        'counts':{'source_entries':len(inventory['sources']),'anchor_entries':len(anchors),
                  'checked_files':len(checked),'new_builds':0,'provider_calls':0}
    }
    fresh(OUT / 'R1_REQUIREMENT_REVIEW.json', report)
    print(json.dumps({'report':pin(OUT / 'R1_REQUIREMENT_REVIEW.json'),'counts':report['counts'],
                      'revision':projection['revision'],'verdict':report['verdict']},ensure_ascii=False))

if __name__ == '__main__':
    main()
