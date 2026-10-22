"""Emit the measured conditional-observable addendum, preserving C2 v1."""
from pathlib import Path
import hashlib,json,math
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,s):
    if p.exists():raise FileExistsError(p)
    raw=s.encode();tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(raw)
    if tmp.read_bytes()!=raw:raise RuntimeError('Output mismatch')
    tmp.replace(p)

def main():
    source=ROOT/'bis/C2_TRAJECTORY_expanded_1000.json'
    d=json.loads(source.read_bytes())
    if d['N_per_cell']<1000 or len(d['rows'])!=11:raise ValueError('Incomplete C2 grid')
    for rel,h in d['sources'].items():
        if sha(ROOT/rel)!=h:raise ValueError('Source changed: '+rel)
    for row in d['rows']:
        for kind in ('noise_free','recolored'):
            c=row[kind]
            if c['N']!=d['N_per_cell'] or len(c['fits'])!=c['N']:raise ValueError('Incomplete cell')
            for k in ('mean_dtau','mean_dtau_standard_error','df_standard_deviation','df_standard_deviation_standard_error'):
                if not math.isfinite(c[k]):raise ValueError('Nonfinite statistic')
    opening=ROOT.parent/'TUNEL/DO_CHATGPT/ENTREGA_013BIS_ABERTURA_operador.md'
    text=['[REAL no controle condicional; desenrolamento físico OPEN] '+datetime.now(timezone.utc).isoformat(),
      '', '# C2 — uma realização e a distribuição do estimador', '',
      '**O detector registra UMA realização; o desenrolamento que a produz é [OPEN]; a C4/C6 desta ordem cobriram só o ensemble.** A Parte B tratará a largura populacional de δf̂ como observável separado, sujeito a transferência e calibração; esta tabela não é teste da natureza.',
      '', 'Foram ajustadas '+str(d['N_per_cell'])+' trajetórias por célula, em 11 cenários de leitura/ocupação e dois regimes de ruído. A execução levou '+format(d['wall_seconds'],'.3f')+' s em uma thread. Todas as trajetórias e ajustes estão no JSON; valores nas bordas são mantidos.',
      '', 'O ensaio usa Mdet=68,1 M☉, χ=0,68, SNR da portadora RG=20 e fase 0,37, em um canal H1 ilustrativo. São 128 amostras a 2048 Hz (62,5 ms), o dobro da janela temporal da v1 a 4096 Hz. O ajuste reaproveita o projetor variável de amplitude/fase, δf∈[−0,5;0,5], log(τ/τRG)∈[−2;2] e três pontos iniciais. A janela e a PSD foram explicitadas; os resultados não devem ser subtraídos da v1 como se apenas N tivesse mudado.',
      '', 'O ruído vem dos 256 intervalos fora da fonte de C5_RECOLORED_NOISE, transportados à PSD de referência O4 pela convenção arquivada. São mil sorteios com reposição dessa biblioteca finita, não mil intervalos de ruído independentes nem uma nova PSD medida O4. Os erros padrão ruidosos usam somas da função de influência agrupadas pelo intervalo original; não incluem incerteza da PSD, dependência entre intervalos ou erro de modelo. Sem ruído, os erros padrão são de Monte Carlo IID. A aproximação de influência para o desvio padrão é assintótica.',
      '', '| Leitura / ocupação | Ruído | média δτ̂ ± EP | dp(δf̂) ± EP | bordas / falhas |',
      '|---|---|---:|---:|---:|']
    for row in d['rows']:
        name=row['reading']+(' N='+str(row['occupation']) if 'occupation' in row else '')
        for kind,label in [('noise_free','sem ruído'),('recolored','recolorido')]:
            c=row[kind]
            text.append(f"| {name} | {label} | {c['mean_dtau']:.7g} ± {c['mean_dtau_standard_error']:.3g} | {c['df_standard_deviation']:.7g} ± {c['df_standard_deviation_standard_error']:.3g} | {c['boundary_count']} / {c['optimizer_failures']} |")
    text+=['','Os zeros ajustados das leituras de efeito minúsculo são resolução numérica do estimador; não anulam suas taxas analíticas. Em R-LIN, o processo é Cauchy: sua fase não tem variância. A dispersão tabelada pertence ao estimador limitado, que atingiu bordas; não é uma variância da fase nem demonstra normalidade.',
      '', '## Perda do filtro casado', '',
      'A perda abaixo é 1−||projeção na base seno/cosseno RG||/||sinal limpo||, com frequência e amortecimento RG fixos e fase/amplitude maximizadas. É perda fracional de SNR frente ao filtro ótimo do sinal, não perda de energia. Resíduos negativos de ordem 10⁻¹⁶ são arredondamento e foram preservados.',
      '', '| Leitura / ocupação | Perda média fracional de SNR |', '|---|---:|']
    for row in d['rows']:
        name=row['reading']+(' N='+str(row['occupation']) if 'occupation' in row else '')
        text.append('| '+name+' | '+format(row['gr_matched_filter_snr_fractional_loss']['mean'],'.9g')+' |')
    text += ['', 'Wiener e Cauchy de fase preservam o módulo da portadora em cada trajetória, mas a média coerente decai. No ramo coerente, o fator é uma média quântica condicional ⟨a⟩ com soma de Poisson e um Wiener comum; |⟨a⟩|² não é a energia do oscilador. N=4,64,256 são cenários ilustrativos, sem lei distância→ocupação. O gerador GKSL sozinho não seleciona nenhum desses readouts clássicos.',
      '', 'R-PROP é expoente acumulado de propagação e não fornece, no módulo atual, um processo temporal local único de ringdown. Não se inventou sua célula estocástica; essa conversão permanece NÃO PAGA. R-GLOBAL fornece o controle nulo relacional sob sua hipótese. Os demais ramos têm seus processos nomeados no JSON.',
      '', '## Reprodução e custódia', '',
      '`wsl -e /opt/lal_env/bin/python -B "/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/refeito/measure_c2_013bis.py" --n 1000 --tag expanded_1000`',
      'O comando recusa resultado existente; uma repetição usa tag nova e preserva a saída anterior. Não há PE, acesso a strain da fonte ou alteração dos resultados C4/C6.',
      '', 'JSON de resultados SHA256 '+sha(source)+'. Código SHA256 '+sha(ROOT/'refeito/measure_c2_013bis.py')+'.',
      'C2_TRAJECTORY_RECOVERY.json anterior SHA256 '+sha(ROOT/'C2_TRAJECTORY_RECOVERY.json')+'; intacto. C5_RECOLORED_NOISE.json SHA256 '+sha(ROOT/'C5_RECOLORED_NOISE.json')+'.',
      'Abertura do operador SHA256 '+sha(opening)+'.',
      '', 'PAGO: ampliação condicional, médias/dispersões com EP, ruído fora da fonte recolorido e perda do filtro. NÃO PAGO: identificação do desenrolamento físico, calibração IMR/duas famílias, transferência ao posterior de eventos e conversão R-PROP. Nenhum gate alterado. Tentativa benchmark preservada em bis/C2_TRAJECTORY_benchmark.json; não houve falha de execução nesta ampliação. Axiomas: N/A — sem Lean.', '']
    new(ROOT/'C2_ADENDO_OBSERVAVEL.md','\n'.join(text))
    new(ROOT/'REAPROVEITAMENTO_C2.md',
      '[REAL — ficha C2; readouts condicionais]\n\n'
      'Existia: trajectory_recovery.py::fit/main, tgl_ringdown_unravelings.py::poisson_support, '
      'tgl_ringdown_prediction.py::prediction, prepare_empirical_noise.py::polynomial_whitener, '
      'C2_MAPEAMENTO_ANALITICO.md e C5_RECOLORED_NOISE.json.\n\n'
      'Reusado: estimador de três inícios, fórmulas de predição, soma de Poisson, grade QNM e ruído '
      'arquivado; nenhuma reimplementação do kernel. Novo: mil trajetórias por célula, janela '
      'explicitada, agrupamento por intervalo de ruído no EP e diagnóstico de perda de SNR. '
      'Motivo: F1 pede distinguir uma realização do ensemble e medir a distribuição ajustada.\n\n'
      'Resultados SHA256 '+sha(source)+'; adendo SHA256 '+sha(ROOT/'C2_ADENDO_OBSERVAVEL.md')+
      '; abertura SHA256 '+sha(opening)+'. Reprodução e lacunas no adendo; axiomas N/A — sem Lean.\n')
    print('C2 addendum',sha(ROOT/'C2_ADENDO_OBSERVAVEL.md'))

if __name__=='__main__':main()
