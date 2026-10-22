"""Record measured GWTC-3 progress; preserve task memory byte for byte."""
from pathlib import Path
from datetime import datetime, timezone
import csv
import io
import json
import zipfile
from fetch_public import atomic_json, digests

ROOT=Path(__file__).resolve().parent


def read(name):
    return json.loads((ROOT/name).read_bytes())


def sha(path):
    return digests(path)[1]


def write_new(path,raw):
    if path.exists():
        raise FileExistsError(str(path))
    tmp=path.with_name(path.name+'.tmp')
    tmp.write_bytes(raw)
    if tmp.stat().st_size!=len(raw):
        raise ValueError('Short write')
    tmp.replace(path)


def append_memory(path,raw):
    old=path.read_bytes()
    backup=path.with_name(path.name+'.bak_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
    backup.write_bytes(old)
    if backup.read_bytes()!=old:
        raise ValueError('Byte backup failed')
    tmp=path.with_name(path.name+'.tmp')
    tmp.write_bytes(old+raw)
    if tmp.stat().st_size!=len(old)+len(raw):
        raise ValueError('Short memory write')
    tmp.replace(path)
    if path.read_bytes()[:len(old)]!=old:
        raise ValueError('Memory prefix changed')


def main():
    delivery=ROOT.parent/'TUNEL/DO_CHATGPT/ENTREGA_013_C4_C7_gwtc3_e_reproducao.md'
    if delivery.exists():
        raise FileExistsError('Create-once registrar')
    old=read('C4_GWTC3_220.json')
    primary=read('C4_GWTC3_PUBLISHED_COMBINATION.json')
    control=read('C4_GWTC3_COMBINATION.json')
    selection=read('C4_GWTC3_SELECTION.json')
    supplements=read('C7_SUPPLEMENTS_VALIDATION.json')
    if supplements['status']!='PASS':
        raise ValueError('Supplement validation failed')
    reg=read('REGISTRO_C6.json');regsha=sha(ROOT/'REGISTRO_C6.json')
    receipt=ROOT.parent/'TUNEL/DO_CHATGPT/ENTREGA_013_C6a_REGISTRO_TOEPLITZ.md'
    if regsha not in receipt.read_text(encoding='utf-8'):
        raise ValueError('C6 receipt mismatch')
    for name,wanted in reg['code_and_input_hashes'].items():
        if sha(ROOT/name)!=wanted:
            raise ValueError('C6 input changed: '+name)
    leaves=0;replays=[]
    for package in supplements['packages']:
        base=ROOT/package['package'];manifest=json.loads((base/'MANIFEST.json').read_bytes())
        if sha(base/'MANIFEST.json')!=package['manifest_sha256'] or sha(ROOT/package['archive'])!=package['sha256']:
            raise ValueError('Package custody changed')
        for row in manifest['shipped_files']:
            p=base/row['path']
            if p.stat().st_size!=row['bytes'] or sha(p)!=row['sha256']:
                raise ValueError('Shipped file changed')
        with zipfile.ZipFile(ROOT/package['archive']) as z:
            if z.testzip() is not None:
                raise ValueError('Archive CRC error')
        for replay in package['replays']:
            p=ROOT/replay['path']
            if sha(p)!=replay['sha256']:
                raise ValueError('Replay receipt changed')
            result=json.loads(p.read_bytes())
            if result['status']!='PASS' or result['reference_results_copied_as_inputs']:
                raise ValueError('Invalid fresh replay')
            for row in result['comparisons']:
                if sha(p.parent/'ORDEM_013_RINGDOWN'/row['output'])!=row['output_sha256']:
                    raise ValueError('Recomputed output changed')
                leaves+=row['numerical_leaves']
            replays.append(dict(package=package['package'],stage=replay['stage'],receipt_sha256=replay['sha256']))
    if set(primary['selected_events'])!=set(selection['selected_events']):
        raise ValueError('Selection mismatch')
    if control['input_sha256']['combine_gwtc3.py']!=sha(ROOT/'combine_gwtc3.py.bak_ALL18_ONLY'):
        raise ValueError('All-18 code backup differs')
    for result in [control,primary]:
        events=[r for r in old['rows'] if r['event'] in result['selected_events']]
        for line in result['catalog']:
            summed=sum(next(x for x in r['rows'] if x['reading']==line['reading'])['lnB_conditional_uniform_prior'] for r in events)
            if abs(summed-line['lnB'])>1e-12:
                raise ValueError('Catalog sum mismatch')
    now=datetime.now(timezone.utc).isoformat()
    downloads=read('cache/MANIFESTO_DOWNLOADS.json')
    files={r['path'].replace('\\','/'):r for r in downloads['files']}
    archive_rel='cache/public/17461225/IGWN-GWTC3-TGR-v2-rin.zip'
    md5,digest=digests(ROOT/archive_rel)
    archive_receipt=read(archive_rel+'.receipt.json')
    official=next(x for x in read('cache/public/17461225/record.json')['files'] if x['key']==Path(archive_rel).name)
    if digest!=archive_receipt['sha256'] or official['checksum']!='md5:'+md5:
        raise ValueError('Public ZIP checksum mismatch')
    inputs=[(archive_rel,'LVK Zenodo 17461225, CC BY 4.0')]
    for item in read('C4_GWTC3_SCHEMA.json')['rows']:
        if sha(ROOT/item['path'])!=item['sha256']:
            raise ValueError('Public posterior changed')
        inputs.append((item['path'],'LVK Zenodo 17461225, CC BY 4.0'))
    inputs += [(r['path'],r['url']) for r in read('C4_GWTC3_SOURCE_DOCS.json')['sources'] if r['status']=='RETRIEVED']
    paper=read('C4_GWTC3_PAPER_RECEIPT.json');inputs.append((paper['path'],paper['url']))
    inputs += [(p['archive'],'Own reproduction code and attributed public/derived inputs') for p in supplements['packages']]
    for rel,origin in inputs:
        p=ROOT/rel;files[rel]=dict(path=rel,bytes=p.stat().st_size,sha256=sha(p),origin=origin)
    downloads.update(at=now,files=list(files.values()))
    atomic_json(ROOT/'cache/MANIFESTO_DOWNLOADS.json',downloads)
    buffer=io.StringIO(newline='');writer=csv.writer(buffer)
    writer.writerow(['release','event','published_selection','current_overlap','reading','delta_tau_median','gamma_over_omega_median','lnB','correction_over_sigma','verdict','posterior_sha256'])
    for event in old['rows']:
        for line in event['rows']:
            p=line['median_prediction']
            writer.writerow(['GWTC3_TGR_v2',event['event'],event['event'] in selection['selected_events'],bool(event['mapped_current_event']),line['reading'],p['delta_tau_ensemble_exact'],p['gamma_over_omega'],line['lnB_conditional_uniform_prior'],line['correction_over_sigma'],line['verdict'],event['source_sha256']])
    write_new(ROOT/'C7_GWTC3_EVENT_READINGS.csv',buffer.getvalue().encode('utf-8'))
    artifacts=['C0_ADENDO_ESCOPO_LITERATURA.md','C4_GWTC3_220.json','C4_GWTC3_SCHEMA.json','C4_GWTC3_COMBINATION.json','C4_GWTC3_PUBLISHED_COMBINATION.json','C4_GWTC3_SELECTION.json','C4_GWTC3_CONVENTIONS.json','C4_GWTC3_SOURCE_DOCS.json','C4_GWTC3_PAPER_RECEIPT.json','gwtc3_posterior_readout.py','combine_gwtc3.py','combine_gwtc3.py.bak_ALL18_ONLY','read_gwtc3_selection.py','record_gwtc3_conventions.py','C7_GWTC3_EVENT_READINGS.csv','C7_SUPPLEMENTS_VALIDATION.json','cache/C7_POSTERIOR_REPRODUCTION_v1.zip','cache/C7_INJECTION_REPRODUCTION_v1.zip','cache/MANIFESTO_DOWNLOADS.json']
    hashes={name:sha(ROOT/name) for name in artifacts}
    remaining=[
        'Incorporar a análise separada GWTC-3 e a seleção publicada ao suplemento independente; verificar o acréscimo em pasta limpa.',
        'Completar auditoria de cobertura C0-C7 contra o objetivo integral e síntese científica final em inglês; não repetir posteriores/injeções já reproduzidos.',
        'Discriminar limites de inferência: versão do binário/fusão pyRing não documentados, Kay-Wald/Milburn consultados por resumos e partição/relógio/desenrolamento físico não selecionados.',
        'Calibração nas duas famílias não passou conjuntamente. É resultado limitante da inferência, não dívida que autorize escolher amostras favoráveis ou alterar C6.'
    ]
    status=read('STATUS_ORDEM_013.json')
    status.update(date_utc=now,goal_status='ACTIVE_NOT_COMPLETE',previous_goal_turn='NO_PROGRESS: respondeu ao pedido de prompt curto; objetivo e estado revalidados nesta rodada',this_goal_turn='PROGRESS: GWTC-3 lido, seleção publicada recuperada e calculada, cinco reproduções verificadas e memória atualizada',no_blocker_recurrence=True,active_processes=[],requirements_remaining=remaining,next_action=remaining[0])
    status['verified']['GWTC3']=dict(N_products=len(old['rows']),N_published=len(primary['selected_events']),N_draws=sum(r['N'] for r in old['rows']),reconciliation=old['duplicate_reconciliation'],catalog=primary['catalog'],GR_diagnostics=primary['common_deformation_GR_diagnostics'],all18_is_control=True)
    status['verified']['C7_supplements']=dict(replays=replays,numerical_leaves=leaves,scope='Fresh local replays and current output hashes; original LVK samplers not rerun, network bootstrap not refetched')
    status['verified']['C7']['status']='V1_AND_TESTED_POSTERIOR_INJECTION_SUPPLEMENTS__GWTC3_EXTENSION_PENDING'
    status['verified']['C0_access_correction']='See C0_ADENDO_ESCOPO_LITERATURA.md: one source archive and two abstract-page failures, not three full-text failures'
    status['archives']['GWTC3']='18 products; ten-event published selection plus all-18 control. 12 overlaps and six older-only products; no union evidence'
    status['preserved_failures'] += ['Unversioned LAL source URL returned 404; versioned 7.26 source inspected. Original binary version unavailable.','Guessed arXiv HTML v4 absent; source abstract identified v3, retrieved and inspected.','First local HTML read raised cp1252 UnicodeDecodeError; UTF-8 reread succeeded without file mutation.','Initial all-18 combination is an auxiliary control; source Table 13 selection and exclusions recovered, yielding separate ten-event result.','First attempt to add the progress registrar had a malformed patch; tool rejected it and no file was created. Corrected patch applied.']
    status['hashes'].update(hashes)
    atomic_json(ROOT/'STATUS_ORDEM_013.json',status)
    lines=['[REAL — medido e conferido; predições condicionais DERIVED/INPUT/CONJECTURE; NÃO-CEGO]', '', '# Ordem 013 — GWTC-3 e reprodução dos posteriores/injeções', '', 'Data UTC: '+now+'. Axiomas: N/A — sem Lean.', '',
      '## Critérios e resultados', '',
      '- **PAGO:** 18 HDF5 pSEOB220, '+str(sum(r['N'] for r in old['rows']))+' amostras; ZIP conferido contra MD5 oficial e SHA medido. Convenções de prior e amortecimento documentadas com fontes versionadas.',
      '- **PAGO:** 12 sobreposições com o catálogo corrente e seis produtos antigos adicionais. A união nominal tem 39 eventos; nenhuma evidência foi multiplicada entre releases.',
      '- **PAGO:** seleção primária recuperada da Tabela 13 e das duas exclusões explícitas: dez eventos. O controle de todos os 18 arquivos permanece separado.',
      '- **PAGO:** cinco reproduções em pastas novas, desde os posteriores ou ruído bruto; '+str(leaves)+' campos numéricos coincidem, sem diferença nos campos conferidos. Isso conta campos, não medições independentes. Manifestos, arquivos e resultados recalculados foram reconferidos nesta rodada.',
      '- **PAGO:** integridade do registro C6 e de todos os seus insumos. Nenhuma nova leitura do strain nesta entrega.',
      '- **NÃO PAGO:** empacotar o acréscimo GWTC-3 e terminar a auditoria integral C0-C7. Objetivo ativo.', '',
      '## Seleção publicada do GWTC-3', '', '| leitura | ln B condicional contra RG | veredito |','|---|---:|---|']
    lines += [f"| {r['reading']} | {r['lnB']:.8g} | {r['verdict']} |" for r in primary['catalog']]
    diag=primary['common_deformation_GR_diagnostics'][1]
    lines += ['',f"Controle central: {diag['draws']} pontos, ESS={diag['importance_ESS']:.2f}; conteúdo HPD no ponto RG={diag['GR_HPD_content']:.6f}. As quatro verificações deixam RG fora de 95%. A regra relativa impede exclusão da TGL com esse diagnóstico. A incerteza Monte Carlo não cobre viés de KDE ou sistemáticas; não convertê-la em sigma.", '',
      'A soma do controle de 18 tem pouco suporte local em dois produtos e não reproduz a seleção do artigo. As razões são do setor 220 sob priors uniformes condicionais; não representam uma teoria TGL completa. Versões originais do binário/fits não recuperadas.', '',
      'Seleção conferida em [LVK, VIII.1.2 e Tabela 13](https://arxiv.org/html/2112.06861v3#S8.SS1.SSS2), com leitura do Apêndice A.3. Não se declara leitura integral nem se substituem amostras por números do artigo.', '',
      '## Reprodução e entrega', '',
      'Na bancada: `python -B gwtc3_posterior_readout.py`, `python -B read_gwtc3_selection.py`, `python -B combine_gwtc3.py`. Os dois últimos recusam sobrescrita; repetir em pasta nova com os insumos relativos. O backup ALL18_ONLY preserva o gerador do controle anterior.', '',
      'Os suplementos já testados estão em `cache/C7_POSTERIOR_REPRODUCTION_v1.zip` e `cache/C7_INJECTION_REPRODUCTION_v1.zip`. Cada um contém README em inglês, manifesto, scripts e recibos. No primeiro: `python reproduce.py primary|joint|free_clock|catalog --source-root /path/to/ORDEM_013_RINGDOWN` (escolher um estágio). No segundo: `python reproduce.py full --source-root /path/to/ORDEM_013_RINGDOWN --imr-python /path/to/pycbc/python`.', '',
      '`--download` é a alternativa pública documentada; essa via de rede não foi novamente exercitada na reprodução local. Samplers LVK não foram rerodados. Tabela adicional: `C7_GWTC3_EVENT_READINGS.csv`, 144 linhas, com indicação da seleção publicada e de sobreposição.', '',
      '## Memória, limites e aproveitamento', '',
      'A automação de posteriores/injeções já foi entregue e não deve ser refeita. O adendo C0 corrige o rótulo antigo de três leituras integrais falhadas. STATUS e PROGRESSO recebem backups byte a byte; nenhuma memória canônica ou programa de outra casa foi alterado.', '',
      'Reutilizados ratio_pair, local_support, weighted_quantile, registro C4 e grade QNM. Acrescentados os posteriores antigos e sua seleção documental. Nenhuma função nova no um.py. Falhas de URL, codificação e patch ficam no STATUS; não viraram dados científicos.', '',
      'A calibração de duas famílias continua negativa. A partição, relógio e desenrolamento físico não foram escolhidos. O objetivo não exige números favoráveis, nem permite transformar NOT_EXCLUDED em confirmação.', '',
      '## Custódia medida', '', '| arquivo | SHA-256 |','|---|---|']
    lines += [f'| `{name}` | `{digest}` |' for name,digest in hashes.items()]
    raw=('\n'.join(lines)+'\n').encode('utf-8')
    write_new(delivery,raw);append_memory(ROOT/'PROGRESSO.md',b'\n\n'+raw)
    print(json.dumps(dict(status='PROGRESS_NOT_COMPLETE',delivery=str(delivery),numerical_leaves=leaves,N_replays=len(replays),N_GWTC3=len(old['rows']),N_published=len(primary['selected_events']))))


if __name__=='__main__':
    main()
