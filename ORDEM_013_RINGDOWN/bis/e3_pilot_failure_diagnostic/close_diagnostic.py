"""Read existing receipts and primary text; no science imports, draws or calls."""
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from collect_static_addendum import Lines

HERE = Path(__file__).resolve().parent
B = HERE.parents[1]
CHECKS = []

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path): return json.loads(path.read_bytes())
def check(name, condition):
    CHECKS.append({'name': name, 'passed': bool(condition)})
    if not condition: raise ValueError(name)
def save(name, obj):
    raw = obj.encode('utf-8') if isinstance(obj, str) else (json.dumps(obj, indent=2, ensure_ascii=False, allow_nan=False)+'\n').encode('utf-8')
    with (HERE/name).open('xb') as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
def pin(path): return {'path': str(path), 'sha256': sha(path), 'bytes': path.stat().st_size}

def main():
    plan = read(HERE/'PLAN_INPUTS.json')
    reg = read(B/'RINGDOWN_5SIGMA_V1.json')
    check('registration_pin', sha(B/'RINGDOWN_5SIGMA_V1.json') == plan['registration_sha256'])
    for name, expected in reg['own_code_tree_sha256'].items():
        check('frozen_E2:'+name, sha(B/'bis/e2_code'/name) == expected)
    mappings = []
    for item in plan['source_evidence']:
        if 'primary_url' not in item: continue
        name = Path(item['copy']).name
        html = HERE/'sources'/(name+'.html'); txt = HERE/'sources'/name
        parser = Lines(); parser.feed(html.read_bytes().decode('utf-8'))
        check('HTML_pin:'+name, sha(html) == item['sha256'])
        check('HTML_size:'+name, html.stat().st_size == item['bytes'])
        check('reextract:'+name, ('\n'.join(parser.lines)+'\n').encode() == txt.read_bytes())
        mappings.append({'primary_url': item['primary_url'], 'original_plan_entry_preserved': item,
                         'correct_html': pin(html), 'correct_extracted_text': pin(txt)})
    save('SOURCE_HASH_ADDENDUM.json', {'status': 'NF_R4_ADDITIVE_MAPPING_CORRECTION',
        'created_utc': datetime.now(timezone.utc).isoformat(), 'original_plan': pin(HERE/'PLAN_INPUTS.json'),
        'error': 'The three C copy fields identify extracted text but sha256/bytes identify adjacent HTML.',
        'impact': 'Static provenance annotation error. HTML and text both preserved. Diagnostic executable local sources were separately pinned; no diagnostic rerun.',
        'mappings': mappings})
    controllers = sorted((HERE/'cases').glob('*.CONTROLLER.json'))
    check('all_processes_counted_against_cap_including_replay', len(controllers) == 10 == plan['max_sequential_waveform_children'])
    cases = []
    for path in controllers:
        result = read(path); label = result['label']
        check('log:'+label, sha(HERE/'cases'/(label+'.log')) == result['log_sha256'])
        check('deadline:'+label, datetime.fromisoformat(result['finished_utc']) < datetime.fromisoformat(plan['deadline_utc']))
        check('child_wall:'+label, result['wall_seconds'] < plan['per_child_wall_cap_seconds'])
        casepath = HERE/'cases'/(label+'.json')
        calls = sorted((HERE/'cases').glob(label+'.CALL_*.json'))
        returns = sorted((HERE/'cases').glob(label+'.RETURN_*.json'))
        row = {'label': label, 'controller': result, 'controller_pin': pin(path),
               'case': read(casepath) if casepath.exists() else None,
               'pre_call_records': [],
               'returns': [dict(read(p), evidence=pin(p)) for p in returns]}
        row['pre_call_records'] = [{'record': read(p), 'evidence': pin(p)} for p in calls]
        if casepath.exists():
            check('case_plan:'+label, row['case']['plan_sha256'] == sha(HERE/'PLAN_INPUTS.json'))
            expected_calls = row['case'].get('sequence', [row['case']['parameters']])
            check('calls_count:'+label, len(calls) == len(expected_calls))
            for p, expected in zip(calls, expected_calls): check('input:'+p.name, read(p)['parameters'] == expected)
        cases.append(row)
    total_calls = sum(len(x['pre_call_records']) for x in cases)
    total_returns = sum(len(x['returns']) for x in cases)
    check('native_calls_16', total_calls == 16)
    check('native_returns_15', total_returns == 15)
    a = read(HERE/'cases/DRAW8_1024.json'); b = read(HERE/'cases/DRAW8_2048.json')
    check('DRAW8_only_fmax_differs', {k:v for k,v in a.items() if k != 'generation_fmax'} == {k:v for k,v in b.items() if k != 'generation_fmax'})
    check('DRAW8_abort', read(HERE/'cases/DRAW8_2048.CONTROLLER.json')['returncode'] == -6)
    check('DRAW8_allocator_message', 'free(): invalid next size (normal)' in (HERE/'cases/DRAW8_2048.log').read_text())
    original = read(HERE/'sources/original_CONTROLLER.json')
    launch = read(B/'cache/E3_PSEOB_PILOT_V1/LAUNCH_CONTEXT.json')
    original_stop = launch['stop_utc']
    check('original_log_intact', sha(B/'cache/E3_PSEOB_PILOT_V1/PRIVATE.log') == original['private_log_sha256'])
    check('original_crash_distinct', original['returncode'] == -11)
    review = B/'bis/e3_pilot_review/PILOT_NATIVE_DIAGNOSTIC_INDEPENDENT_REVIEW.json'
    review_content = read(review)
    cpu = sum(x['controller']['child_cpu_seconds'] for x in cases)
    wall = sum(x['controller']['wall_seconds'] for x in cases)
    last = max(datetime.fromisoformat(x['controller']['finished_utc']) for x in cases)
    elapsed = (last-datetime.fromisoformat(plan['created_utc'])).total_seconds()
    result = {
        'status': 'DIAGNOSTIC_COMPLETE_REPAIR_NOT_IMPLEMENTED_OR_APPROVED',
        'created_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Existing receipts and finite source-only children. No strain, posterior, likelihood or PE; no E2/runtime edits.',
        'original_crashing_tuple': None,
        'original_SIGSEGV_cause': 'OPEN. Eight original-fmax source calls returned; draws 2/8 match logged domain-error masses, not a crash tuple.',
        'original': {'controller': original, 'launch_pin': pin(B/'cache/E3_PSEOB_PILOT_V1/LAUNCH_CONTEXT.json'),
                     'stop_utc_retained': original_stop, 'configuration': plan['pilot_configuration_INPUT']},
        'cause_differentiation': {
            'GR550_EDOM': 'REAL source path: fmax1024 implies internal fs2048, Nyquist1024; high-mode GR550 check does not consume TGRParams. No automatic attribution to domega.',
            'changed_DRAW8_SIGABRT': 'REAL: same complete source tuple as DRAW8_1024, only generation_fmax2048, rc-6 allocator message. Original SIGSEGV not reproduced.',
            'buffer_hypothesis': 'CONJECTURE: sigReHi/sigImHi capacity uses dtau220 only; AttachFitRingdown uses mode-specific dtau440 for Nrdwave at TGRflag1, then unchecked i+indAmax writes. Internal lengths and native stack not captured; no demonstrated inequality for this tuple.',
            'cleanup_bug': 'OPEN. Allocator detects corruption, but its message does not locate the corrupting instruction; no proved double free.'},
        'new_abort_full_case': b, 'pre_call_persisted': pin(HERE/'cases/DRAW8_2048.CALL_1.json'),
        'cases': cases,
        'cost': {'total_processes': len(cases), 'source_children': 9, 'metadata_replay_children': 1,
                 'native_calls': total_calls, 'native_returns': total_returns, 'sum_child_wall_seconds': wall,
                 'sum_child_CPU_seconds': cpu, 'plan_to_last_child_finish_seconds': elapsed,
                 'last_child_finish_utc': last.isoformat(), 'original_diagnostic_deadline': plan['deadline_utc'],
                 'additional_native_execution': False, 'reason': 'Supervisor counts all ten controller receipts against cap. No reset or extra child.',
                 'thread_control': 'Environment caps before numerical imports; no independent runtime thread enumeration.',
                 'group_absence': 'Not independently measured by diagnostic supervisors; return/wait recorded. Original pilot has separate cleanup receipt.'},
        'review_B': {'pin': pin(review), 'status': review_content['status'], 'blocking_findings': review_content['blocking_findings']},
        'repair_proposal': [
            'New versioned amendment only. Preserve data/PSD, detector fs4096, likelihood20-1024, deltaF1/16, epoch/phase, all modes and original prior support.',
            'Separate internal generation fmax from likelihood mask; choose bounded computational policy only after testing exact DRAW8 safety and complex-band/epoch controls with predefined tolerances.',
            'Inspect/fix native vector capacity to accommodate every generated mode-specific ringdown and attachment offset; explicit bounds/overflow checks and visible errors. No patch or build performed here.',
            'Persist full source input before native call in calibration/private custody, contain native failure and abort visibly; never treat numerical inability as physical prior rejection.',
            'New source/binary/runtime-origin pins, parent E2 and witness, exclusive output and independent concrete-code review. Original absolute stop retained; no renewal of eight hours.'
        ],
        'open': ['exact original crash index after known eight', 'native corrupting instruction and buffer lengths',
                 'binary reproduction from official source', 'complex waveform common-band equivalence', 'repair implementation and independent approval'],
        'source_provenance_addendum': pin(HERE/'SOURCE_HASH_ADDENDUM.json'),
        'static_primary_addition': pin(HERE/'STATIC_SOURCE_ADDITION.json'),
        'preserved_failures': ['Original SIGSEGV and domain returns', 'Changed DRAW8 SIGABRT',
            'Initial GitHub raw source 404 preserved in collect_and_plan.failed_github404.py',
            'Static Windows fetch initially denied WinError10013; same text-only collector completed via approved escalation, no runtime mutation'],
        'checks': CHECKS,
    }
    save('DIAGNOSIS.json', result)
    rows = '\n'.join('| '+x['label']+' | '+str(x['controller']['returncode'])+' | '+str(len(x['pre_call_records']))+' | '+', '.join(r['status'] for r in x['returns'])+' |' for x in cases)
    text = f'''# Diagnóstico finito do piloto pSEOB — encerrado

**Reparo não implementado nem aprovado.** [REAL] Foram10 processos (9 de fonte +1 replay),16 chamadas/15 retornos: {wall:.6f}s de wall somado e {cpu:.6f}s CPU dos filhos. Último término: {last.isoformat()}, {elapsed:.3f}s após o plano; limite original {plan['deadline_utc']}. O supervisor conta também o replay no teto10 (`run_diagnostics.py:22`). Não houve filho adicional. Tempo documental posterior não reiniciou a janela de execução.

## Causas distintas

1. [REAL — fonte + execução] O condicionador toma fmax como Nyquist interno (`sources/LALSimInspiralGeneratorConditioning.c:536`,545). fmax1024 e deltaF1/16 dão fs interno2048, embora o grid dos dados seja4096. O teste que emite EDOM usa GR550 no ramo HM (`sources/LALSimIMRSpinAlignedEOB.c:1250`,1256,1279). Essa checagem não lê TGRParams; **não atribuir automaticamente o EDOM a domega**. LOW_GR também recusou em1024.
2. [REAL] As massas dos dois erros originais coincidem com draws2/8. A sequência desses oito em1024 retornou sem crash. **Tuple/índice do SIGSEGV original−11 permanecem OPEN**; um próximo draw não foi executado. Não reproduzimos a inicialização completa nem sua likelihood/dados. Bilby verifica parâmetros e depois faz100 temporizações (`sources/bilby_base_sampler.py:267`,447); isso não identifica o primeiro crash.
3. [REAL] DRAW8_2048 abortou−6 com `free(): invalid next size (normal)`. `cases/DRAW8_2048.CALL_1.json` contém a entrada completa persistida antes da chamada. Comparação por script com DRAW8_1024 confirma que **só generation_fmax mudou**; a falha alterada não é o SIGSEGV original. Elevar fmax sozinho não é reparo estabelecido.
4. [CONJECTURE — hipótese específica, não causa provada] O buffer de alta resolução é ampliado por dtau220 (`sources/LALSimIMRSpinAlignedEOB.c:2060`), sem dtau440. pSEOB4112 liga TGRflag (`:649`); o attach modifica Im(omega440) por /(1+dtau440) (`sources/LALSimIMREOBHybridRingdown.c:1081`), dimensiona Nrdwave por esse modo (`:1263`) e escreve signal[i+indAmax] sem checagem local (`:1393`). No draw8 dtau220<0 e dtau440>0. É uma hipótese concreta de capacidade insuficiente; **não medimos retLen, indAmax, Nrdwave nem demonstramos a desigualdade no caso**. `free()` não prova double-free ou identifica a instrução corruptora.

## Evidência completa e alcance

`DIAGNOSIS.json` inclui configuração original, todos os casos, tuples e retornos/pins. DRAW8: massas detector40.70912464765123/20.237781889510657 Msun; chi1/2 .9196233876975504/.2055129322455731; dtau220/440 −.6157519631492032/1.7780455359890353; domega220/440 −.42647193412015016/.7808349673597068. Distância, ângulos e GPS constam integralmente do precall. Não houve gravação de arrays de onda nem stack nativo/faulthandler; controles de fase/overlap/epoch continuam OPEN.

| Caso | rc | Chamadas | Retornos |
|---|---:|---:|---|
{rows}

## Desenho de reparo para revisão, sem implementação

Separar geração interna da banda científica20–1024, conservando fs4096, deltaF1/16, epoch/fase, todos os modos, PSD/dados e priors. Uma frequência interna maior precisa passar pelo **draw8 exato**, controles complexos na banda comum com tolerância prévia e limites temporais/custo; normas escalares semelhantes no draw2 não pagam isso. Auditar capacidade nativa por máximo de todos os comprimentos/offsets realmente requeridos, com checagens explícitas de limites e overflow. Alterar tamanho de buffer exige validação, não clipping de dtau ou remoção de modos.

Persistência pré-call e isolamento tornam falhas visíveis, mas não fornecem likelihood válida para o ponto. EDOM numérico não deve ser transformado em rejeição física do prior. Reparo concreto exige versão própria, pins de fonte/binário/imports, parentE2/testemunha, saída exclusiva e revisão independente. **Stop original {original_stop} preservado**; não renovar8h. A causa nativa universal não é pré-requisito abstrato adicional: vale a qualificação NF-R1 de B, com demonstração concreta de suporte e falha visível.

## Custódia e lacunas

NF-R4 corrigido **ao lado** em `SOURCE_HASH_ADDENDUM.json`: três entradas do plano apontavam texto C com hash/tamanho do HTML. Reextração byte a byte conferida; ambos os hashes estão no adendo. Plano original preservado. Fontes C adicionais e header VCS estão em `STATIC_SOURCE_ADDITION.json`; header:39/42 concorda com commit/tag instalado, mas compilação reprodutível não foi feita. Leitura primária: https://lscsoft.docs.ligo.org/lalsuite/7.26/lalsimulation/_l_a_l_sim_i_m_r_e_o_b_hybrid_ringdown_8c_source.html . Nenhum código dessa página foi executado.

Os14 fontes E2 conferem com registro. {len(CHECKS)} verificações documentais/escalares passaram, sem ciência nova. Revisão B lida: `{review.name}`, SHA256 `{sha(review)}`. NF-R2/R3 continuam dependentes do reparo concreto; NF-R4 recebe este adendo para revisão. Não foi medido group_absent dos diagnósticos nem número real de threads; há wait/return e caps de ambiente. E2/runtime e resultados originais intactos. Sem strain, posterior, PE ou seed cego. `MANIFEST.json` lista todos os arquivos deste diretório e hashes; o próprio manifesto é listado sem auto-hash circular.
'''
    save('DIAGNOSIS.md', text)
    files = sorted(p for p in HERE.rglob('*') if p.is_file())
    save('MANIFEST.json', {'created_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'All diagnostic files, including prior preserved evidence and additive closure. No file outside this root written by this closure.',
        'files': [dict(pin(p), relative_path=p.relative_to(HERE).as_posix()) for p in files],
        'self': {'relative_path': 'MANIFEST.json', 'sha256': None, 'reason': 'No circular self hash'}})
    print(json.dumps({'checks': len(CHECKS), 'wall_seconds': wall, 'CPU_seconds': cpu, 'artifacts': {n:sha(HERE/n) for n in ['DIAGNOSIS.md','DIAGNOSIS.json','SOURCE_HASH_ADDENDUM.json','MANIFEST.json']}}))

if __name__ == '__main__': main()
