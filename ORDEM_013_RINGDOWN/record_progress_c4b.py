"""Record verified progress, download custody, and remaining full-goal work.

Only task-local memory and the authorized return tunnel are modified.
Every existing memory receives an immediate byte backup and atomic replacement.
Scientific assertions below are generated from current result artifacts.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import re
from fetch_public import atomic_json

ROOT=Path(__file__).resolve().parent

def digest(path):
    result=hashlib.sha256()
    with path.open('rb') as stream:
        while block:=stream.read(8*1024*1024):result.update(block)
    return result.hexdigest()

def read(name):return json.loads((ROOT/name).read_bytes())

def atomic_text(path,text):
    raw=text.encode('utf-8')
    old=path.read_bytes() if path.exists() else None
    if old is not None:
        path.with_name(path.name+'.bak_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f')).write_bytes(old)
    temp=path.with_name(path.name+'.tmp');temp.write_bytes(raw)
    if temp.stat().st_size!=len(raw):raise ValueError('Short temporary write')
    temp.replace(path)
    if path.read_bytes()!=raw:raise ValueError('Written bytes differ')

def local_cache_path(text):
    # Receipts were produced on Windows and WSL; map only the known task cache.
    normalized=text.replace('\\','/')
    rel=normalized.split('/ORDEM_013_RINGDOWN/',1)[1]
    path=(ROOT/rel).resolve()
    if not path.is_relative_to((ROOT/'cache').resolve()):
        raise ValueError('Manifest item leaves task cache')
    return path

def downloads():
    files={};failed=[]
    def add(row,kind,extra=None):
        path=local_cache_path(row['path']);actual=digest(path)
        if actual!=row['sha256']:raise ValueError('Custody mismatch: '+str(path))
        files[str(path.relative_to(ROOT))]=dict(path=str(path.relative_to(ROOT)),bytes=path.stat().st_size,
            sha256=actual,kind=kind,origin=row.get('url',row.get('member')),
            extra=extra or {})
    for folder in (ROOT/'cache/public').iterdir():
        if not folder.is_dir():continue
        meta_path=folder/'record.json'
        meta=json.loads(meta_path.read_bytes()) if meta_path.exists() else {}
        extra=dict(record=folder.name,doi=meta.get('doi'),
                   attribution=meta.get('metadata',{}).get('creators'),
                   declared_license=meta.get('metadata',{}).get('license'),
                   data_citation='LIGO Scientific Collaboration, Virgo Collaboration, KAGRA Collaboration; original Zenodo record. Rights remain those of the source.')
        for receipt in folder.glob('*.receipt.json'):
            add(json.loads(receipt.read_bytes()),'public_archive',extra)
        extraction=folder/'extraction_receipt.json'
        if extraction.exists():
            for row in json.loads(extraction.read_bytes())['files']:add(row,'selected_release_product',extra)
    for row in read('LITERATURE_MANIFEST.json')['sources']:
        if row['status']=='RETRIEVED':add(row,'literature',{'reading_scope':row['note']})
        else:failed.append(row)
    for row in read('cache/source_distributions/manifest.json')['packages']:
        add(row,'pinned_source_distribution',{'package':row['package'],'version':row['version'],'installed':False})
    for row in read('cache/source_distributions/source_index.json')['sources']:
        add(row,'inspected_source_excerpt',{'package':row['package']})
    out=dict(status='HASHES_RECOMPUTED_FROM_ALL_LISTED_ARTIFACTS',at=datetime.now(timezone.utc).isoformat(),
             files=list(files.values()),retrieval_failures=failed,
             not_included='Installed vendor tree and copied house artifacts have their own package/custody manifests. This does not assert all source texts were read.',
             on_source_strain_read=False)
    atomic_json(ROOT/'cache/MANIFESTO_DOWNLOADS.json',out)
    return out

def main():
    manifest=downloads()
    py=read('C4_PYRING.json');free=read('C4_FREE_CLOCK.json');oracle=read('C4_FREE_CLOCK_ORACLE.json')
    trajectory=read('C2_TRAJECTORY_RECOVERY.json');compat=read('C3_PREDICTION_COMPATIBILITY.json')
    catalog=read('C4_CATALOG_COMBINATION.json');initial=read('C4_220_INITIAL.json')
    if oracle['status']!='PASS' or compat['status']!='PASS':raise ValueError('Unpassed verification')
    if oracle['tested_sha256']!=digest(ROOT/'free_clock_posterior.py'):raise ValueError('Clock test stale')
    if compat['current_prediction_sha256']!=digest(ROOT/'tgl_ringdown_prediction.py'):raise ValueError('Prediction test stale')
    for result,script in [(py,'pyring_readout.py'),(free,'free_clock_posterior.py'),(trajectory,'trajectory_recovery.py')]:
        if result['code_sha256']!=digest(ROOT/script):raise ValueError('Result/code version mismatch')
    artifacts=['C1_LEITURAS_E_RELOGIOS.md','C1_TABLES.json','C3_BILBY_CONSUMER.json',
               'QNM_GRID.json','C4_CATALOG_220.json','C4_CATALOG_COMBINATION.json','C4_CATALOG_PRIOR_AUDIT.json',
               'C4_PYRING.json','pyring_readout.py','C4_FREE_CLOCK.json','free_clock_posterior.py',
               'C4_FREE_CLOCK_ORACLE.json','verify_free_clock_oracle.py','C2_TRAJECTORY_RECOVERY.json',
               'trajectory_recovery.py','tgl_ringdown_prediction.py','C3_PREDICTION_COMPATIBILITY.json',
               'cache/MANIFESTO_DOWNLOADS.json']
    hashes={name:digest(ROOT/name) for name in artifacts}
    rb=next(r for r in py['rows'] if r['reading']=='R-B')
    initial_rb=next(r for r in initial['rows'] if r['reading']=='R-B')
    primary=next(r for r in catalog['common_deformation_GR_diagnostics']
                 if r['selection']=='release_figure_selection_31' and r['draws']==8192 and r['bandwidth']==1.)
    count=sum(c['N'] for r in trajectory['rows'] for c in r['comparisons'])
    failures=sum(c['optimizer_failures'] for r in trajectory['rows'] for c in r['comparisons'])
    bounds=sum(c['boundary_count'] for r in trajectory['rows'] for c in r['comparisons'])
    when=datetime.now(timezone.utc).isoformat()
    remaining=[
       'C0: três downloads de literatura falharam (403/406), registrados; não equiparar resumo/abstract a leitura integral.',
       'C2/C3: escolhas de desenrolamento continuam hipóteses físicas; portar/explicitar interfaces de Cauchy e soma de Poisson no pacote. O teste atual usa ruído sintético, não off-source.',
       'C4: hipóteses conjuntas 220+440 e tratamento dos demais modos; comparação de início tardio com pyRing; conferência do GWTC-3 sem duplicar eventos; sensibilidade restante de priors e remanescente.',
       'C4: procedência da fusão do weighted_posterior e binário original pyRing não reconstruída; 2.7.0 está fixado no ambiente publicado de figuras. Controle secundário fica condicionado a isso.',
       'C5: PSD fora da fonte, injeções com duas famílias IMR e N>=50 por célula; viés/cobertura sob ruído empírico; completar distribuições de evidência calibradas, além de Fisher.',
       'C6: entregar registro com hash antes de ler strain na janela; executar rota escolhida validada, incluindo cinco tempos de início e controles.',
       'C7: pacote independente em inglês, comandos e teste de reprodução integral; só declarar completo após auditoria do objetivo inteiro.'
    ]
    status=read('STATUS_ORDEM_013.json')
    status.update(date_utc=when,goal_status='ACTIVE_NOT_COMPLETE',
       previous_visible_nonresearch_turn='NO_GOAL_PROGRESS: só respondeu o prompt curto; revalidado o estado e retomada a pesquisa nesta rodada',
       this_goal_turn='PROGRESS: pyRing, relógio livre com quadratura independente, modos de spin negativo sem cortes, 1100 ajustes de trajetórias e consolidação do catálogo previamente concluído',
       requirements_remaining=remaining,active_processes=[],no_blocker_recurrence=True,
       next_action='Completar hipóteses conjuntas dos modos e preparar a verossimilhança de C6 com controles C5 em ruído fora da fonte; registrar antes de acessar strain do evento.',
       archives=dict(GW250114='Verificado, selecionado, pyRing e pSEOB lidos',
                     GWTC5='pSEOB baixado/verificado: 33 eventos; seleção primária literal 31; GW250114 contado uma vez',
                     GWTC3='Ainda não confrontado como release separado; não multiplicar eventos já incluídos'),
       on_source_strain_read=False)
    status['verified'].update(
       C1='Tabela de dez leituras e relógios, construção finita KMS e correções de tipagem em C1_TABLES.json',
       C3='Consumidor Bilby real: arrays coincidem; 264 previsões anteriores preservadas após suporte a spin assinado',
       catalog=dict(unique_events=33,primary_selection=31,GR_HPD_content=primary['GR_HPD_content'],
                    verdict='INCONCLUSIVE_SYSTEMATICS',scope=catalog['physical_model_caution']),
       pyRing=dict(N=py['N'],R_B_lnB=rb['lnB'],GR_HPD_content=py['GR_HPD_content'],
                   negative_spin_samples=py['signed_spin']['N_negative'],discarded=0,
                   scope=py['version_scope']),
       free_clock={r['prior']:r['quantiles'] for r in free['rows']},
       C2_trajectory_fits=dict(cells=len(trajectory['rows'])*2,N_fits=count,optimizer_failures=failures,
                         boundary_hits=bounds,noise='SYNTHETIC_OU_PLUS_WHITE_NOT_EMPIRICAL'))
    status['hashes'].update(hashes)
    status['preserved_failures'].extend(py['preserved_failures'])
    status['preserved_failures'].extend([
        'Busca inicial ampla gerou saída truncada; as fontes científicas usadas foram relidas por faixas, JSONs e funções específicos.',
        'Primeira matriz de trajetórias usava portadora comum BCW no ramo modular; preservada em backup e substituída por portadora/QNM/tempo de amortecimento exatos consistentes.',
        'Comparação de quadratura do prior log-uniforme em 129 e 257 nós não bastou; convergiu em 513 conforme tolerâncias explicitadas.'
    ])
    atomic_json(ROOT/'STATUS_ORDEM_013.json',status)
    lines=[f'[REAL — resultados computacionais condicionais; objetivo integral ATIVO]\n\n## Rodada {when}\n',
       f'Controle pyRing: {py["N"]} amostras; ramo B ln B={rb["lnB"]:.9f} (pSEOB primário: {initial_rb["lnB_joint_spin_curve"]:.9f}). Mesmo evento, sem multiplicação das evidências. As três amostras de spin negativo foram mantidas e verificadas por qnm e Leaver. A versão 2.7.0 é do ambiente de figuras; procedência integral do binário/mesclagem é ressalva explícita.\n',
       f'Catálogo já calculado foi consolidado: 33 produtos, seleção literal primária de 31. Conteúdo HPD da RG na combinação primária: {primary["GR_HPD_content"]:.9f}; RG fora de 95%, portanto o critério registrado conserva INCONCLUSIVE_SYSTEMATICS. Nem esse conteúdo HPD nem ln B são sigma de descoberta.\n',
       'Relógio livre integrado com os dois priors previamente registrados, sem tratá-lo como Bayes de ponto. Limites condicionais de 95% (segundos na fonte): '+', '.join(f'{r["prior"]}: {r["quantiles"]["0.95"]["tau_source_s"]:.9g}' for r in free['rows'])+'. A coordenada de prior permanece quase uniforme; a grande diferença não é evidência de medição precisa. Quadratura independente aprovada em C4_FREE_CLOCK_ORACLE.json.\n',
       f'Trajetórias: {count} ajustes em {len(trajectory["rows"])*2} células, 50 por célula, {failures} falhas de otimizador, {bounds} contatos com limites. Incluem Wiener, Cauchy e Poisson coerente N=4/64/256. Ruído OU sintético, sem alegação de C5 empírico; o ajuste de uma trajetória não é igual ao ajuste da média de ensemble.\n',
       f'Manifesto de downloads: {len(manifest["files"])} arquivos com hash recalculado, falhas de obtenção preservadas. Nenhum strain da janela foi lido. Memórias canônicas e um.py não alterados.\n',
       '**Pendências integrais**\n\n'+'\n'.join('- '+x for x in remaining)+'\n']
    progress=ROOT/'PROGRESSO.md'
    old=progress.read_bytes()
    addition=('\n\n'+'\n'.join(lines)).encode('utf-8')
    # Preserve existing bytes and line endings exactly, then append UTF-8 bytes.
    backup=progress.with_name(progress.name+'.bak_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
    backup.write_bytes(old)
    temp=progress.with_name(progress.name+'.tmp');temp.write_bytes(old+addition)
    assert temp.stat().st_size>len(old)
    temp.replace(progress)
    handoff=ROOT.parent/'TUNEL/DO_CHATGPT/ENTREGA_013_C4b_catalogo_pyring_relogio_e_trajetorias.md'
    if handoff.exists():raise ValueError('Entrega already exists; create an additive dated follow-up')
    report='[REAL — análise computacional condicional, NÃO-CEGA; não move o gate]\n\n# Ordem 013 — catálogo, pyRing, relógio e trajetórias\n\n'
    report+='\n'.join(lines[1:])
    report+='\n## Critérios\n\n| Critério | Estado | Evidência |\n|---|---|---|\n'
    report+='| C1, tabela e unidades | PAGO no escopo condicional | C1_TABLES.json e C1_LEITURAS_E_RELOGIOS.md |\n'
    report+='| C2, distribuição de estimadores sem/com ruído colorido | PAGO como simulação explícita | C2_TRAJECTORY_RECOVERY.json; não substitui ruído empírico |\n'
    report+='| C3, consumidor Bilby | PAGO para fonte 220 | C3_BILBY_CONSUMER.json; regressão preservada |\n'
    report+='| C4, priors, grade e catálogo sem duplicação | PAGO para comparação condicional 220 | C4_CATALOG_220.json + C4_CATALOG_COMBINATION.json |\n'
    report+='| C4, controle pyRing | PARCIAL | C4_PYRING.json; versão da inferência e fusão das amostras não auditadas |\n'
    report+='| C4, relógio livre | PAGO para GW250114/220 | C4_FREE_CLOCK.json + oráculo independente |\n'
    report+='| C4, todos os modos e todas as sensibilidades | NÃO PAGO | lista de pendências acima |\n'
    report+='| C5, ruído empírico e duas famílias IMR | NÃO PAGO | Fisher anterior e simulação OU não bastam |\n'
    report+='| C6, strain registrado | NÃO PAGO | janela ainda não lida |\n'
    report+='| C7, pacote e reprodução integral | NÃO PAGO | objetivo permanece ativo |\n'
    report+='\n## Reprodução\n\nExecutar no WSL, com `/opt/lal_env/bin/python -B` e diretório absoluto `/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN`:\n\n'
    report+='1. `pyring_readout.py` (usa os arquivos públicos e fontes já fixados no cache).\n2. `free_clock_posterior.py`, depois `verify_free_clock_oracle.py`.\n3. `trajectory_recovery.py`.\n4. `verify_prediction_catalog_compatibility.py`.\n\nNão reinstalar nada em `/opt`; vendor próprio fica em cache/vendor. O manifesto de downloads registra as fontes e seus direitos. Os scripts de análise preservam resultados anteriores em backup. O registrador desta entrega não é um teste científico a ser repetido.\n'
    report+='\n## Custódia lida dos artefatos\n\n| Arquivo na Ordem 013 | SHA-256 |\n|---|---|\n'
    report+='\n'.join(f'| {name} | `{value}` |' for name,value in hashes.items())+'\n'
    report+='\n## Ficha de aproveitamento\n\nReutilizados: módulos de predição/KDE/constantes/forma de onda, registro C4, grade QNM, solver Leaver, posteriores verificados e regras de exclusão. Novos: adaptador restrito aos dois ajustes aritméticos pyRing, marginalização do relógio e oráculo, matriz de trajetórias, consolidação de memória e downloads. Nenhum programa ou kernel canônico editado; nenhuma confirmação física ou escolha de partição. Axiomas: N/A — sem Lean.\n'
    report+='\nFalhas preservadas: limiar arbitrário de arredondamento do spin; grade positiva que recusou três amostras negativas; portadora comum inicial; quadratura ainda insuficiente nas primeiras grades. As correções e os controles numéricos estão no diário e nos JSONs.\n'
    atomic_text(handoff,report)
    print(json.dumps(dict(status='PROGRESS_RECORDED_GOAL_ACTIVE',download_artifacts=len(manifest['files']),
        posterior_samples=py['N'],trajectory_fits=count,handoff=str(handoff),remaining=remaining),ensure_ascii=False))

if __name__=='__main__':main()
