"""Deliver path-bounded hygiene with limitations retained; proceed to T03."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,uuid
B=Path(__file__).resolve().parents[2];D=B/'bis/015/t13';ROOT=B.parent;OUT=ROOT/'TUNEL/DO_CHATGPT';now=datetime.now(timezone.utc)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_bytes())
def write(p,raw,replace=False):
    if p.exists():
        assert replace;old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+now.strftime('%Y%m%d_%H%M%S_%f'))
        with bak.open('xb') as f:f.write(old)
        assert bak.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    with tmp.open('xb') as f:f.write(raw)
    assert tmp.read_bytes()==raw;tmp.replace(p)
def main():
    w=load(D/'WINDOWS_CLEANUP.json');u=load(D/'WSL_UNLINK.json');a=load(D/'ACL_FINALLY_TEST.json');c=load(D/'CACHE_INVENTORY_WSL.json')
    i=load(D/'INTEGRITY_V3_RUN.json');v=load(Path(i['receipt']))
    elevated=[p for p in D.glob('FINAL_INTEGRITY_015_*.json') if '_v3_' not in p.name];assert len(elevated)==1
    e=load(elevated[0]);mismatches=[r for r in e['checks'] if not r['matches']]
    assert all(r['status']=='REMOVED' for r in w['rows'])
    assert w['junction']['status']=='UNLINKED_WITHOUT_TARGET_RECURSION' and u['unlink']['status']=='UNLINKED'
    assert u['seed_metadata_same'] and a['removed'] and a['finally_entered'] and a['worker_rc']==1
    assert 'RuntimeError: T13_INJECTED_FAILURE_AFTER_NATIVE_ACL_CREATION' in (D/'ACL_FINALLY_TEST.log').read_text('utf-8-sig')
    assert all(not r['errors'] for r in c['rows'])
    copies=load(D/'FIXTURE_SOURCE_MANIFEST.json')
    for r in copies['rows']:assert sha(Path(r['source']))==r['sha256']==sha(Path(r['copy']))
    exclusions=[r['path'] for r in v['directory_enumeration_errors']]
    evidence={str(p):sha(p) for p in sorted(D.glob('*')) if p.is_file() and p.suffix in ['.json','.log']}
    result=dict(at=now.isoformat(),status='T13_NAMED_CLEANUP_COMPLETED_WITH_VISIBLE_LIMITATIONS',removed_fixtures=3,unlinked=2,
        metadata_only_seed_check=u['seed_before'],metadata_unchanged_in_wsl_action=True,pre_windows_seed_stat_denied=True,
        no_seed_content_read=True,no_real_seed_mutation=True,no_canonical_writes=True,unlisted_fixture_exclusions=exclusions,
        canonical_differences=mismatches,cache_inventory=c['rows'],evidence=evidence,
        scope_limits=['WSL seed metadata bracket covers unlink; initial Windows bracket denied stat, so not a complete independent before/after of earlier fixture deletions.',
          '214951 is different from authorized 214938; remained outside removal scope and listed as unreadable in default identity.',
          'Native helper synthetic failure cleanup tested. Full cross-identity custody repair cleanup not replayed; its original main never run.',
          'Existing reproduction wrappers already contain finally; static verification, no old scientific replay.'],
        heavy_machine_hours=0,external_calls=0,gate_changed=False,
        opening015_sha256=sha(OUT/'ENTREGA_015_ABERTURA_operador.md'),opening016_sha256=sha(OUT/'ENTREGA_016_ABERTURA_operador.md'))
    first=(B/'bis/015/t13_cleanup.ps1').stat().st_mtime
    result['bench_interval_hours_from_first_script']=(now.timestamp()-first)/3600
    report=f'''[REAL — higiene e integridade documental; limitações explícitas]

Abertura015SHA256: {result['opening015_sha256']}
Abertura016SHA256: {result['opening016_sha256']}

As três pastas EXATAS da T13 foram removidas pela identidade criadora; o junction e o symlink foram desvinculados sem seguir destinos e sem takeown. Journal: bis/015/t13/WINDOWS_CLEANUP.json e WSL_UNLINK.json. Nenhuma ampliação de caminho. A pasta 214951 é distinta da 214938 autorizada e permanece fora do escopo; a nova auditoria a registra como ilegível no sandbox e excluída da custódia por caminho: {exclusions}.

Semente REAL: cache/E2_PRIVATE/BLIND_SEED_V1.bin; o caminho bis/cache da ordem não existe. O sandbox não conseguiu stat antes/depois das remoções Windows. No WSL, antes/depois da desvinculação, 32 bytes e mtime_ns {u['seed_before'][0].get('mtime_ns')} idênticos. Nunca se leu conteúdo. A limitação do primeiro intervalo permanece; não declarar uma conferência completa que não ocorreu.

Novo harness t13_acl_fixture_harness.ps1: finally cobre a criação e falha da fixture. Cópia pinada do helper cria/verifica ACL nativa; falha injetada rc1; finally executou e removeu a fixture. O reparador foi copiado sem executar o main real; limpeza após transferência entre identidades não foi reencenada. Cinco wrappers de reprodução já tinham finally, conferidos por AST e hash em EXISTING_FINALLY.json; não criamos versões redundantes nem reabrimos campanhas.

final_integrity_015_v2.py acrescenta onerror. A primeira execução no sandbox falhou ao hashear um.py; tentativa preservada. A repetição somente de leitura no host conferiu 217 insumos,31 fontes,47 entregas A: quatro diferenças canônicas contra o retrato antigo, zero diferença nos insumos/entregas A e zero arquivo excedente. A v3 conserva erros individuais de leitura e registra a pasta ilegível 214951; seu estatuto NÃO é PASS. Recibos: {elevated[0].name} e {Path(i['receipt']).name}. As diferenças não foram corrigidas sobrescrevendo fontes.

Inventário sem conteúdo nem remoção: guard_7h3lo515={c['rows'][0]['bytes']} B; native_package_tamper={c['rows'][1]['bytes']} B; delivery_fresh={c['rows'][2]['bytes']} B; delivery_v2_fresh={c['rows'][3]['bytes']} B. O primeiro levantamento Windows ficou parcial por caminhos longos; o WSL mediu os quatro sem erros. Papéis inferidos pelos nomes históricos; apagabilidade não demonstrada, mantidos para auditoria de referências.

Intervalo documentado desde o primeiro script: {result['bench_interval_hours_from_first_script']:.4f}h; comandos leves, pesada0h, chamadas externas0. T13 aceita como MEDIDA de higiene com limites nomeados. Próximo ramo: T03, preparação da V1.1 sem iniciar relógioR7 nem dados cegos.
'''
    write(OUT/'ENTREGA_015_T13_higiene.md',report.encode())
    write(D/'RESULT.json',(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode())
    p=OUT/'LEDGER_016.jsonl';write(p,p.read_bytes()+(json.dumps(dict(at=now.isoformat(),event='PARTB_T13_COMPLETED_WITH_LIMITATIONS',receipt=str(D/'RESULT.json'),external_calls=0))+'\n').encode(),True)
    p=OUT/'ENTREGA_016_PROGRESSO.md';write(p,p.read_bytes()+f'\n{now.isoformat()} — B/T13 MEDIDA: 3fixtures+2links removidos; finally sintético e auditoria onerror; 214951 excluída por caminho e4diferenças canônicas preservadas. Intervalo mínimo{result["bench_interval_hours_from_first_script"]:.4f}h, pesada0h. PróximoT03.\n'.encode(),True)
    p=ROOT/'ORDEM_016_QG/A7/CONTINUIDADE.json';state=load(p);state.update(at=now.isoformat(),T13_final=str(D/'RESULT.json'),own_live_process=None,next='T03 prepare V1.1; original V1 guard before/after in /opt/lal_env; R5 qualification and witness before heavy R7. Revised external payload approval still pending; C6 closed.')
    state['remaining_full_goal']=['C2.2 independent critique remains unpaid after terminal Kimi failure','ORDEM015 Part B ordered tree from T03; T01/T02 delivered, T13 limitations recorded','final completion audit and both reports']
    write(p,(json.dumps(state,ensure_ascii=False,indent=2)+'\n').encode(),True)
    print(json.dumps(dict(status=result['status'],cache_bytes=[r['bytes'] for r in c['rows']],canonical_mismatches=len(mismatches),next='T03')))
if __name__=='__main__':main()
