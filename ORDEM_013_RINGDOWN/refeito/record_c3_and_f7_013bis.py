"""Read-only timing/accounting checks and additive C3/F7 documentation."""
from pathlib import Path
from datetime import datetime,timezone
import os,json,hashlib,math
ROOT=Path(__file__).resolve().parents[1]
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(2**20),b''):h.update(chunk)
    return h.hexdigest()
def new(p,s):
    if p.exists():raise FileExistsError(p)
    raw=s.encode();tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(raw)
    if tmp.read_bytes()!=raw:raise RuntimeError('Write mismatch')
    tmp.replace(p)
def main():
    regpath=ROOT/'REGISTRO_C6.json'; reg=json.loads(regpath.read_bytes())
    times=[];inputs=[regpath,ROOT/'tgl_ringdown_template.py',ROOT/'tgl_ringdown_prediction.py',
        ROOT/'diagnose_overtones.py',ROOT/'c6_engine.py',ROOT/'C6_PYRING_START_COMPARISON.json',
        ROOT/'C1_ADENDO_CORRECOES_013BIS_v2.md']
    for start in reg['start_times_tM']:
        p=ROOT/f'C6_STRAIN_{start:g}M_GRID_1.json';inputs.append(p)
        d=json.loads(p.read_bytes())
        if d['registration_sha256']!=sha(regpath):raise ValueError('C6 registration mismatch')
        for w in d['windows']:
            actual=w['first_sample_GPS']; ref=reg['reference_peak_GPS'][w['detector']]
            requested=ref+start*reg['reference_tM_seconds']
            if requested!=w['requested_GPS']:raise ValueError('Requested onset differs')
            delay=actual-requested
            if not 0<=delay<1/4096+1e-6:raise ValueError('First-sample rounding invalid')
            times.append(dict(**w,reference_peak_GPS=ref,rounding_seconds=delay,
                realized_start_tM=(actual-ref)/reg['reference_tM_seconds']))
    data=dict(status='TIMING_AND_CONVENTION_DOCUMENTED__C6_PRE_ONLY',
        utc=datetime.now(timezone.utc).isoformat(),rows=times,
        inputs={str(p.relative_to(ROOT)):sha(p) for p in inputs},
        on_source_strain_read_this_run=False,
        timing_scope='Recomputed from frozen JSON window metadata, no new strain processing')
    target=ROOT/'bis/C3_C6_TIMING_013BIS.json';new(target,json.dumps(data,indent=2)+'\n')
    opening=ROOT.parent/'TUNEL/DO_CHATGPT/ENTREGA_013BIS_ABERTURA_operador.md'
    lines=['[REAL — código e metadados conferidos; observável físico OPEN]', '',
      '# C3.1 — README de convenções e lacunas (013BIS)', '',
      'O módulo prediction(..., observable="realization") não fornece uma previsão universal de δτ̂ médio ou dp(δf̂): **NÃO PAGO** como distribuição física calibrada. Os estimadores condicionais de C2 estão em C2_ADENDO_OBSERVAVEL.md e no JSON de mil trajetórias, com seus desenrolamentos nomeados; não preenchem esse campo por identidade de nomes.',
      '', '## Relógio, regressão e constantes', '',
      'A chave que reproduz o v346 é delta_tau_linear=−x, x=ΓτGR. A expressão de ensemble exata é delta_tau_ensemble_exact=−x/(1+x). LEGACY_V346 mantém constantes históricas e não é CODATA2018/IAU2015. As diferenças medidas do perfil completo, em z=0, e as 264 linhas de compatibilidade estão em C1_ADENDO_CORRECOES_013BIS_v2.md; o controle atualizado recusa cobertura parcial, duplicatas, NaN e dependências alteradas.',
      '', '## t_start, pico e t0', '',
      'tgl_ringdown_template.py:58–59 usa time>=t_start e elapsed=time−t_start, em segundos no referencial do detector. Se time contém GPS, t_start deve conter GPS; se time já mede tempo desde um pico, t_start é um deslocamento nessa mesma origem. O template não identifica o pico automaticamente e sua amplitude/fase são definidas no início declarado.',
      'Na C6-pre, requested=reference_peak_GPS[detector]+n×reference_tM_seconds; seleciona-se o primeiro sample original a 4096 Hz não anterior ao pedido e depois stride=2. A base de c6_engine.py:82 recomeça em zero no primeiro sample retido; portanto o início realizado pode diferir de n tM. Massa de referência do corte é fixa, não a massa corrente de cada ponto do posterior. São hipóteses e convenções do diagnóstico antigo, não um novo ajuste.',
      '', '| n nominal | detector | GPS pedido | GPS primeiro sample | arredondamento (µs) | n realizado |',
      '|---:|---|---:|---:|---:|---:|']
    for r in times:
        lines.append(f"| {r['start_tM']:g} | {r['detector']} | {r['requested_GPS']:.7f} | {r['first_sample_GPS']:.7f} | {r['rounding_seconds']*1e6:.6g} | {r['realized_start_tM']:.8g} |")
    lines+=['', 'C6_PYRING_START_COMPARISON.json registra pico H1 de Kerr pyRing 1420878141,2190118 e referência TEOB da bancada 1420878141,2189023: origens distintas, diferença aproximada 109,5 µs. Esse número é lido do controle arquivado; a presente conferência não reextraiu as configurações primárias. Kerr220/221 a 6,8,10,12 tM têm posteriores liberados; não há 10,5 tM nesse índice. A comparação de pipelines não é reprodução da mesma likelihood: modos, priors, banda, PSD e origem temporal diferem.',
      '', '## Γ e overtones', '',
      'O template geral calcula Γ por mode=(l,m,n) e QNM exato fornecido. A chamada para um overtone pode produzir uma taxa diferente da fundamental. Os controles C5 em diagnose_overtones.py:40–47 impõem outra hipótese: todos os overtones 22 recebem Γ220; os 44 recebem Γ440; os demais harmônicos ficam sem modificação. Isso acompanha a injeção fabricada que amortece o harmônico inteiro. Não são a mesma lei multimodo, nem uma escolha física inferida dos dados. O Fisher original usa só 220 e não resolve essa ponte.',
      '', 'PAGO: documentação das convenções, diferenças de constantes, chave de regressão e início realizado a partir do registro. NÃO PAGO: observável de realização universal, identificação física da lei dos overtones e reprodução completa da PE pyRing (reservada a E3.1). Nenhum strain foi relido.',
      '', 'Evidência JSON SHA256 '+sha(target)+'. Reprodução: `python -B -X utf8 refeito/record_c3_and_f7_013bis.py` (saídas únicas; usar cópia de bancada para repetição). Fontes/hashes no JSON. Abertura SHA256 '+sha(opening)+'. Axiomas: N/A — sem Lean.', '']
    new(ROOT/'C3_README_013BIS.md','\n'.join(lines))
    new(ROOT/'REAPROVEITAMENTO_C3.md',
        '[REAL — ficha C3; sem execução de fonte canônica]\n\n'
        'Existia: tgl_ringdown_prediction.py::prediction; tgl_ringdown_template.py::ringdown; '
        'c6_engine.py::observed_windows/evaluate_grid; diagnose_overtones.py::mode_basis; '
        'REGISTRO_C6.json e C6_STRAIN_* congelados. Reusado: código e metadados de janela, '
        'sem reexecutar o strain. Novo: tabela de corte nominal/realizado e README explícito '
        'sobre realization NÃO PAGO, perfis e taxas por harmônico/mode.\n\n'
        'Motivo: documentar as diferenças que impedem chamar a comparação de reprodução '
        'física equivalente. Fonte de reprodução e lacunas em C3_README_013BIS.md, SHA256 '+
        sha(ROOT/'C3_README_013BIS.md')+'. Abertura SHA256 '+sha(opening)+
        '. Axiomas: N/A — sem Lean.\n')
    # Final narrow hygiene check; skip only the actual first-level cache.
    large=[];errors=[]
    for folder,dirs,files in os.walk(ROOT,onerror=lambda e:errors.append(str(e))):
        if Path(folder)==ROOT:dirs[:]=[x for x in dirs if x!='cache']
        for name in files:
            p=Path(folder)/name
            try:
                if p.stat().st_size>25_000_000:large.append(dict(path=str(p),bytes=p.stat().st_size))
            except OSError as e:errors.append(str(e))
    plan=json.loads((ROOT/'bis/F7_DUPLICATE_REMOVAL_PLAN.json').read_bytes())
    removed=[]
    for row in plan['entries']:
        if not row['eligible_for_authorized_removal']:continue
        canonical=Path(row['canonical_path'])
        if Path(row['path']).exists():raise ValueError('Duplicate still exists')
        if sha(canonical)!=row['canonical_sha256']:raise ValueError('Canonical copy changed')
        removed.append(row)
    dirs=json.loads((ROOT/'bis/F7_NAMED_TEMPORARIES_REMOVED.json').read_bytes())
    for row in dirs['directories']:
        if Path(row['target']).exists():raise ValueError('Named temporary reappeared')
    receipt=dict(status='PASS_NARROW_HYGIENE_CHECK' if not large and not errors else 'FAIL_HYGIENE',
        utc=datetime.now(timezone.utc).isoformat(),large_files_outside_first_level_cache=large,
        scan_errors=errors,removed_count=len(removed),removed_bytes=sum(x['bytes'] for x in removed),
        count_above_25MiB=sum(x['bytes']>25*1024*1024 for x in removed),
        threshold_note='25 MB decimal used; original audit used 25 MiB. Four extra 25.06–25.89 MB exact duplicates removed.',
        named_temporaries_absent=True,canonical_duplicate_hashes_rechecked=True,
        still_pending=['finally cleanup in versioned reproduction scripts','eight reuse fiches','license per file','contract errata','registration amendment'])
    new(ROOT/'bis/F7_POST_REMOVAL_CHECK.json',json.dumps(receipt,indent=2)+'\n')
    print('C3',sha(target),'F7',sha(ROOT/'bis/F7_POST_REMOVAL_CHECK.json'))

if __name__=='__main__':main()
