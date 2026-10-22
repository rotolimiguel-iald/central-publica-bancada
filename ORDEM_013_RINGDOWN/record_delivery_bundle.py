"""Record completed replay and consolidated delivery with byte-safe task memory."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
from fetch_public import atomic_json

ROOT=Path(__file__).resolve().parent


def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        while block:=stream.read(8*1024*1024):
            h.update(block)
    return h.hexdigest()


def new(path, raw):
    if path.exists():
        raise FileExistsError('Preserve prior delivery')
    tmp=path.with_name(path.name+'.tmp')
    tmp.write_bytes(raw)
    if tmp.stat().st_size!=len(raw):
        raise ValueError('Short write')
    tmp.replace(path)


def append(path, raw):
    previous=path.read_bytes()
    backup=path.with_name(path.name+'.bak_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
    backup.write_bytes(previous)
    if backup.read_bytes()!=previous:
        raise ValueError('Backup not byte-identical')
    tmp=path.with_name(path.name+'.tmp')
    tmp.write_bytes(previous+raw)
    if tmp.stat().st_size!=len(previous)+len(raw):
        raise ValueError('Short memory write')
    tmp.replace(path)
    if path.read_bytes()!=previous+raw:
        raise ValueError('Memory prefix altered')


def main():
    handoff=ROOT.parent/'TUNEL/DO_CHATGPT/ENTREGA_013_C7_pacote_unificado_e_auditoria.md'
    if handoff.exists():
        raise FileExistsError('Create-once progress registrar')
    replay=json.loads((ROOT/'C7_GWTC3_REPRODUCTION_VALIDATION.json').read_bytes())
    bundle=json.loads((ROOT/'C7_DELIVERY_BUNDLE_VALIDATION.json').read_bytes())
    audit=json.loads((ROOT/'C7_REQUIREMENTS_AUDIT.json').read_bytes())
    if replay['status']!='PASS' or bundle['status']!='PASS':
        raise ValueError('Delivery verification failed')
    for item in [replay,bundle]:
        if sha(ROOT/item['archive'])!=item['sha256']:
            raise ValueError('Changed delivery archive')
    leaves=sum(x['numerical_leaves'] for x in replay['scientific_comparisons'])
    if any(x['max_absolute_difference']!=0 for x in replay['scientific_comparisons']):
        raise ValueError('Unexpected replay difference')
    now=datetime.now(timezone.utc).isoformat()
    artifacts=['package_reproduce_gwtc3.py','build_gwtc3_reproduction.py',
        'verify_gwtc3_reproduction.py','C7_GWTC3_REPRODUCTION/MANIFEST.json',
        'C7_GWTC3_REPRODUCTION_VALIDATION.json','cache/C7_GWTC3_REPRODUCTION_v1.zip',
        'build_delivery_audit.py','C7_REQUIREMENTS_AUDIT.json','C7_REQUIREMENTS_AUDIT.md',
        'C7_DELIVERY_OVERVIEW.md','build_delivery_bundle.py','C7_DELIVERY_BUNDLE_VALIDATION.json',
        'cache/TGL_RINGDOWN_DELIVERY_v1.zip']
    hashes={name:sha(ROOT/name) for name in artifacts}
    downloads=json.loads((ROOT/'cache/MANIFESTO_DOWNLOADS.json').read_bytes())
    files={x['path'].replace('\\','/'):x for x in downloads['files']}
    for item in [replay,bundle]:
        files[item['archive']]=dict(path=item['archive'],bytes=item['bytes'],sha256=item['sha256'],
                                    origin='Own conditional-research reproduction delivery; attributed public/derived inputs')
    downloads.update(at=now,files=list(files.values()))
    atomic_json(ROOT/'cache/MANIFESTO_DOWNLOADS.json',downloads)
    hashes['cache/MANIFESTO_DOWNLOADS.json']=sha(ROOT/'cache/MANIFESTO_DOWNLOADS.json')
    status=json.loads((ROOT/'STATUS_ORDEM_013.json').read_bytes())
    status.update(date_utc=now,goal_status='ACTIVE_NOT_COMPLETE',active_processes=[],
        previous_goal_turn='NO_PROGRESS: respondeu somente ao pedido de prompt curto; objetivo revalidado integralmente nesta continuação',
        this_goal_turn='PROGRESS: GWTC3 reproduzido do ZIP; auditoria de requisitos e síntese em inglês; quatro pacotes reunidos e verificados',
        no_blocker_recurrence=True)
    remaining=[
        'Concluir a revisão granular do objetivo a partir de C7_REQUIREMENTS_AUDIT: a matriz reúne 14 grupos, mas não autoriza declarar todo requisito estrito pago. Conferir especialmente a tabela C1 por leitura (colunas de FP-5, fontes e universalidade) e as limitações da validação externa C6.',
        'Distinguir a entrega condicional calculada da aceitação científica: zero grupos FULL_IMR passaram simultaneamente nas duas famílias/duas injeções. Não rerodar o mesmo experimento nem trocar critérios para obter aprovação.',
        'Partição física, relógio e desenrolamento continuam sem escolha, como manda a ordem. Versões legadas e fusão pyRing não recuperadas; Kay-Wald/Milburn apenas resumos. Não promover essas limitações a prova ou confirmação.',
        'Não refazer os posteriores, a seleção GWTC3, o empacotamento ou as reproduções concluídas; pacote unificado e síntese já entregues.'
    ]
    status.update(requirements_remaining=remaining,next_action=remaining[0])
    status['verified']['C7_GWTC3_reproduction']=replay
    status['verified']['C7_delivery_bundle']=bundle
    status['verified']['C7_requirements_audit']=dict(path='C7_REQUIREMENTS_AUDIT.json',
        requirement_groups=len(audit['requirements']),evidence_files=len(audit['evidence']),
        scientific_acceptance_failures=audit['unresolved_acceptance'],goal_completion_claimed=False)
    status['verified']['C7']['status']='UNIFIED_DELIVERY_AND_FRESH_GWTC3_REPLAY_VERIFIED__FINAL_SCOPE_AUDIT_OPEN'
    status['preserved_failures'] += [
        'First WSL call denied by sandbox service; same authorized command succeeded after escalation, process 76869 exited zero. No running handle remains.',
        'A local inspection print failed on cp1252 emoji encoding; rerun with -X utf8 succeeded, no scientific output mutated.',
        'Requirement-table Markdown initially contained unescaped vertical bars in |K|; immediate byte backup retained and delimiter escaped before bundling.'
    ]
    status['hashes'].update(hashes)
    atomic_json(ROOT/'STATUS_ORDEM_013.json',status)
    text=['[REAL — reprodução e custódia verificadas; predições DERIVED/INPUT/CONJECTURE; interpretação NÃO-CEGA]',
        '', '# Ordem 013 — pacote unificado e auditoria de cobertura', '', 'UTC: '+now+'. Axiomas: N/A — sem Lean novo.',
        '', '## Critérios pagos', '',
        f'- **PAGO:** GWTC-3 recalculado em pasta limpa, com nova extração dos 18 HDF5 do ZIP público já conferido. {leaves} campos numéricos coincidiram exatamente; identidades, seleção e vereditos também. A seleção de dez eventos foi novamente extraída da Tabela 13 e das exclusões do artigo.',
        '- **PAGO:** oito controles adversariais recusaram arquivo adulterado, caminhos inválidos, identidade, veredito, contagem e medida alterados.',
        f'- **PAGO:** quatro pacotes prévios reunidos em `cache/TGL_RINGDOWN_DELIVERY_v1.zip` ({bundle["bytes"]} bytes; {bundle["members"]} entradas). Extração nova validou {bundle["fresh_verifier"]["files"]} arquivos do manifesto. Os bytes das entregas anteriores foram preservados.',
        '- **PAGO:** `C7_DELIVERY_OVERVIEW.md`, resumo científico em inglês com as quatro respostas, taxas por leitura, exemplo de distribuição de ln B, dados reais, comandos de reprodução e limitações.',
        '- **PAGO:** `C7_REQUIREMENTS_AUDIT.json/.md`, inspeção de 14 grupos de requisitos e 51 artefatos com hashes. Separação explícita entre cálculo concluído e critério científico reprovado.',
        '', '## Critérios não pagos e escopo', '',
        '- **NÃO PAGO — aceitação científica C5:** nenhum grupo FULL_IMR testado passa conjuntamente os critérios de viés/cobertura nas duas famílias e nas duas amplitudes injetadas. Não é consertado por escolher só células favoráveis.',
        '- **PARCIAL — comparação externa C6:** oito posteriores pyRing comparados, mas não reprodução idêntica de modelos/priors; não há produto 10,5 tM no release inspecionado. O próprio C6 foi integralmente reproduzido.',
        '- **ABERTO por escopo:** identificação física de partição, relógio e desenrolamento; a bancada não fez essa escolha. A realização finita condicional não demonstra um estado global de Kerr.',
        '- **PENDENTE de revisão final:** conferir cada exigência granular contra a matriz consolidada, especialmente colunas C1 e alcance de validação externa. O objetivo permanece ativo; não se declara integralmente concluído.',
        '', '## Resultado que pode ser comunicado', '',
        'No ramo B, no GW250114 de referência: Gamma ≈ 4,95 s⁻¹, Gamma/omega ≈ 0,00316 e delta_tau ≈ −0,01985, sob o relógio de massa assumido. A medida primária de strain dá ln B ≈ −0,002595. Os catálogos corrente e GWTC-3 dão −1,80828 e −0,820834 em seus respectivos recortes. Não multiplicar esses resultados: há dados sobrepostos. Os vereditos continuam INCONCLUSIVE_SYSTEMATICS; nenhum desses números é sigma.',
        '', '## Reprodução', '',
        'Descompactar `TGL_RINGDOWN_DELIVERY_v1.zip`, ler `README.md` e executar `python verify_delivery.py`. Cada uma das quatro subpastas tem manifesto e instruções próprias. Para o GWTC-3: `python reproduce.py full --archive-cache /path/to/public` ou `--download`; o teste desta rodada usou o ZIP local verificado, não repetiu a transferência.',
        '', '## Aproveitamento e memória', '',
        'Reaproveitados os três scripts científicos GWTC-3 sem alteração. Acrescentados um leitor de ZIP com hash/CRC, comparação exata de identidades e empacotamento. Nenhuma função nova em um.py, nenhuma fonte canônica modificada. O registro C6 e seus insumos continuam íntegros. STATUS, PROGRESSO e manifesto local recebem backups imediatos byte a byte.',
        'Notas antigas de pendência foram corrigidas por adendo e índice: a recuperação de trajetórias, os posteriores, as injeções, o strain e o GWTC-3 já têm execução e reprodução. Não é necessário refazê-los. Falhas de acesso WSL, codificação de saída e tabela Markdown estão preservadas no STATUS; não alteraram resultados científicos.',
        '', '## Custódia medida', '', '| Artefato | SHA-256 |','|---|---|']
    text += [f'| `{name}` | `{digest}` |' for name,digest in hashes.items()]
    raw=('\n'.join(text)+'\n').encode('utf-8')
    new(handoff,raw)
    append(ROOT/'PROGRESSO.md',b'\n\n'+raw)
    print(json.dumps(dict(status='PROGRESS_NOT_COMPLETE',handoff=str(handoff),bundle=bundle['archive'],
        replay_numerical_fields=leaves,active_processes=[],remaining=remaining[0])))


if __name__=='__main__':
    main()
