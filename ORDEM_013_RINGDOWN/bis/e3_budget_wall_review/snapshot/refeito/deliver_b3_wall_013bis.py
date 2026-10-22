"""Deliver pilot wall and the already activated allocation, without new science."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os

B=Path(__file__).resolve().parents[1];R=B.parent;D=R/'TUNEL/DO_CHATGPT'
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for x in iter(lambda:f.read(1048576),b''):h.update(x)
    return h.hexdigest()
def load(p):return json.loads(Path(p).read_bytes())
def new(p,s):
    raw=s.encode();tmp=p.with_name(p.name+'.pending')
    with tmp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    if tmp.stat().st_size!=len(raw):raise OSError('Short write')
    os.link(tmp,p);tmp.unlink()

def main():
    budget=load(B/'ORCAMENTO_40H.json');receipt=load(B/'bis/E3_WALL_BUDGET_ACTIVATION_V1.json')
    if receipt['budget_sha256']!=sha(B/'ORCAMENTO_40H.json'):raise ValueError('Allocation mismatch')
    review=load(R/budget['independent_review']['path'])
    if sha(R/budget['independent_review']['path'])!=budget['independent_review']['sha256'] or review['approved'] is not True:
        raise ValueError('Allocation review mismatch')
    comp=load(B/'cache/E3_KERR220_CALIBRATION_V2/public_psd/COMPARISON.json')
    costs=budget['measured_costs'];pilot=costs['IMR_pilot_failed_controller'];diagnostic=costs['IMR_native_diagnostic']
    opening=sha(D/'ENTREGA_013BIS_ABERTURA_operador.md')
    fiche=B/'REAPROVEITAMENTO_AMPLIACAO_B3.md'
    new(fiche,'[REAL — B3; calibração Kerr NÃO-CEGA e parede nativa IMR]\n\n'
        'Reutilizados strain/PSD públicos pinados, runtime E2 e comparações arquivadas. Novos: Kerr V1/V2, tentativa IMR, '
        'diagnóstico finito e orçamento documental após revisão. PAGO: medição e limites. NÃO PAGO: reprodução exatamente equivalente, '
        'posterior IMR aceito, custo de PE convergida, calibração de sistemática. N/A — sem Lean.\n\n'
        f'Abertura `{opening}`. Orçamento `{sha(B/"ORCAMENTO_40H.json")}`. Falhas preservadas; nenhum canônico alterado.\n')
    lines=['[REAL — B3 entregue com comparação Kerr e parede técnica do piloto IMR; orçamento registrado. Posterior IMR e calibração física NÃO PAGOS.]','',
        '# B3 — piloto e orçamento','',f'Abertura `{opening}`. Ficha `{sha(fiche)}`. Orçamento `{sha(B/"ORCAMENTO_40H.json")}`.','',
        '| Critério | Resultado e limite |','|---|---|',
        '| Kerr_220_10M | PAGO: comparação de Mf/af, critérios de convergência e revisão. Equivalência integral da versão, strain e PSD NÃO PAGA. |',
        '| Custo IMR | PAGO: custo da tentativa falha. Custo por evento convergido OPEN. |',
        '| Posterior de deformação | NÃO PAGO: SIGSEGV antes de posterior aceito. Nenhum hash/posterior inventado. |',
        '| Comparação delta_tau publicado | NÃO PAGA: falta posterior próprio. Família própria pSEOBNRv4HM_PA alinhada difere da pSEOBNRv5PHM precessante publicada. |',
        '| Alocação E3.2 | PAGA como orçamento de parede: cinco alternativas, pesos esperados e reserva final explícitos. |','',
        '## Kerr, evento conhecido e comparação descritiva','',
        '| Parâmetro | Próprio q05 / q50 / q95 | Publicado q05 / q50 / q95 | Diferença de medianas | Diferença/largura em quadratura |',
        '|---|---|---|---:|---:|']
    for name,row in comp['comparison'].items():
        lines.append(f'| {name} | '+ ' / '.join(f'{x:.8g}' for x in row['own_05_50_95'])+' | '+
            ' / '.join(f'{x:.8g}' for x in row['released_05_50_95'])+f' | {row["median_difference"]:.8g} | {row["difference_over_quadrature_width"]:.8g} |')
    c=comp['convergence']
    lines+=['',f'N={comp["samples"]}; ESS={c["ess"]:.6f}; delta_logZ={c["delta_logz"]:.8g}; chamadas do sampler={c["ncall"]}. '
        'Há sobreposição dos intervalos90%. A razão de larguras não é z calibrado: é o mesmo evento, com dados/configurações relacionados. '
        'Não é teste independente nem evidência adicional da TGL. A revisão conferiu os dados completos e os pins; limite de modos/convergência global permanece.','',
        'A variante Welch foi recusada por condicionamento. A primeira variante com PSD pública parou parcial e foi conservada; '
        'a continuação em nova versão convergiu. A PSD pública usada não foi demonstrada idêntica à PSD externa da análise publicada; '
        'os512 live points também diferem dos4096 publicados. O produto tem comparação aceita com limitações, não reprodução equivalente integral.','',
        '## Parede do instrumento IMR','',
        f'Controle original: retorno {pilot["returncode"]}, {pilot["wall_seconds"]:.9f}s de parede; '
        f'CPU filhos={pilot["children_user_cpu_seconds"]+pilot["children_system_cpu_seconds"]:.6f}s. '
        'O grupo do piloto foi confirmado encerrado. Não há posterior aceito, número de chamadas completo ou diferença contra o delta_tau publicado.','',
        f'Diagnóstico limitado: {diagnostic["total_processes"]} processos, {diagnostic["native_calls"]} chamadas/{diagnostic["native_returns"]} retornos. '
        f'Parede somada dos filhos {diagnostic["sum_child_wall_seconds"]:.6f}s; CPU {diagnostic["sum_child_CPU_seconds"]:.6f}s. '
        'O teto incluiu o replay de metadados e não foi reiniciado. Ausência dos grupos desses diagnósticos não foi medida separadamente.','',
        'O fmax interno1024 gera frequência de amostragem interna2048, apesar do grid de dados4096. A recusa EDOM consultada testa o QNM550 da RG. '
        'Aumentar fmax para2048 causou aborto nativo−6 num ponto completo do prior. Os oito primeiros draws em1024 não reproduziram o SIGSEGV original. '
        'A causa exata desse SIGSEGV permanece OPEN; a possível relação entre buffer dimensionado por dtau220 e extensão440 é hipótese, não prova de causa. '
        'Não houve exclusão de pontos problemáticos do prior, corte de modos ou troca silenciosa de likelihood.','',
        'A revisão independente fechou o diagnóstico como parede do instrumento atual, sem aprovar continuação da PE. '
        'Uma reconstrução/requalificação nativa seria outro desenvolvimento, com fontes/binários e transporte numérico próprios; não foi simulada por retry de Python.','',
        '## Alocação','',
        'Novas PE=0; injeções=0; downloads de strain cego=0. A decisão decorre da falta de instrumento validado neste registro, '
        'não de esgotamento das40h nem de impossibilidade geral do método. A custódia e o registro científico ficam preservados. '
        'Jobs vazios no documento não removem jobs estáticos antigos do guard; não existe autorização para relançar o piloto estático.','',
        f'Reserva final2h contada desde {budget["wall_accounting"]["measured_utc"]}; stop {budget["wall_accounting"]["finalization_stop_utc"]}. '
        f'Saldo de ciência não alocado/devolvido na medição: {budget["wall_accounting"]["unused_science_hours_released_not_spent"]:.6f}h, não gasto. '
        'Atraso de revisão consome reserva; o relógio não reinicia.','',
        '| Alternativa | Decisão e limite |','|---|---|']
    for row in budget['alternatives']:lines.append(f'| {row["id"]}. {row["description"]} | {row["reason"]} Custo por programa qualificado OPEN; alocação0. |')
    lines+=['','N=(sigma_inj/piso)², sob média de réplicas independentes sem viés. Sigma_inj é INPUT ilustrativo, não medição do piloto. '
        'Exemplo comum sigma=.058, cinco bins×duas famílias:','',
        '| Leitura | N por célula (ceil, piso /5) | N dez células |','|---|---:|---:|']
    for row in budget['Ncalib']['readings']:
        cases=[x for x in row['illustrative_sigma_INPUT_from_order'] if x['sigma_inj']==.058]
        if cases:
            x=cases[0];lines.append(f'| {row["reading"]} | {x["N_per_cell_floor5_ceiling"]} | {x["N_ten_cells_floor5_ceiling"]} |')
    lines+=['','As dez leituras e o piso /15 estão no JSON, inclusive coeficientes sub-resolução sem alvo operacional. '
        'Nenhuma contagem acima calibra uma cauda5σ ou um viés desconhecido. Horas por programa = N × custo de recuperação; o segundo fator continua OPEN.','',
        '## Candidatas e informação esperada','',
        '14 candidatas documentais,10 sem hold e4 com hold, ausência de publicação limitada ao escopo pesquisado. '
        'Ordenação por SNR anterior à PE. E[I] usa dispersão lognormal fixa e covariância de coeficientes preservada; '
        'não é informação observada, ganho/hora nem poder de teste. Ajustes31 e33 são alternativas sobrepostas, não se somam.','',
        '| Evento | SNR | Hold | Proxy31 | E[I]31 | Proxy33 | E[I]33 |','|---|---:|---|---:|---:|---:|---:|']
    for row in budget['events']:
        w={x['fit_population']:x for x in row['conditional_expected_weights']}
        vals=[row['event'],str(row['SNR_network']),'sim' if row['data_quality_hold'] else 'não']
        for key in ('GWTC5_31','GWTC5_33'):
            vals += [f'{w[key][field]:.7g}' for field in ('inverse_squared_conditional_median_proxy','expected_inverse_variance_lognormal_s_fixed')]
        lines.append('| '+' | '.join(vals)+' |')
    lines+=['','## Custos, reprodução e fontes','',
        f'Kerr controladores V1+V2: {costs["Kerr_V1_V2_controller_sum_seconds"]:.6f}s; CPU filhos {costs["Kerr_V1_V2_CPU_sum_seconds"]:.6f}s. '
        'Esses tempos explicam o consumo; não são somados novamente ao relógio contínuo da ParteB. Custo de waveform isolada, de Kerr e de PE IMR não são intercambiáveis.','',
        'Comandos e variantes exatas estão em E3_KERR_LAUNCH_V1/V2, nos manifests e no LAUNCH_CONTEXT do piloto; '
        '`bis/e2_code/run_controlled.py --job GW250114_PILOT` foi a tentativa IMR. '
        'O orçamento foi registrado por `refeito/activate_wall_budget_013bis.py --review ... --review-sha256 ...`. '
        'Reproduzir somente em cópia isolada; destinos originais não se sobrescrevem. N/A — sem Lean.','',
        'Falhas conservadas: Welch, Kerr parcial, SIGSEGV, abort−6 e correção ao lado do mapeamento HTML/texto das fontes. '
        'O diagnóstico contém os comandos/entradas precall; os manifests listam cada artefato e fonte primária. '
        'Nenhuma inferência de natureza nem escolha de leitura foi feita.','']
    refs=[B/'ORCAMENTO_40H.json',B/'bis/E3_WALL_BUDGET_ACTIVATION_V1.json',R/budget['independent_review']['path'],
        B/'bis/e3_budget_wall/MANIFEST.json',B/'bis/e3_pilot_failure_diagnostic/MANIFEST.json',
        B/'bis/e3_pilot_review/PILOT_NATIVE_DIAGNOSIS_CLOSING_REVIEW.json',
        B/'bis/e3_pyring_review/KERR_V2_POST_RESULT_REVIEW.json',B/'bis/E3_KERR_LAUNCH_V2.json',
        B/'cache/E3_KERR220_CALIBRATION_V2/public_psd/COMPARISON.json',
        B/'cache/E3_PSEOB_PILOT_V1/CONTROLLER.json',B/'bis/e3_blind_review/REVIEW_RECEIPT_V1.json',fiche]
    files={p.relative_to(R).as_posix():dict(sha256=sha(p),bytes=p.stat().st_size) for p in refs}
    for path,info in files.items():lines.append(f'- [{path}](<{(R/path).as_posix()}>) — `{info["sha256"]}` ({info["bytes"]} B).')
    delivery=D/'ENTREGA_013BIS_B3_piloto_e_orcamento.md';new(delivery,'\n'.join(lines)+'\n')
    new(B/'bis/B3_DELIVERY_MANIFEST.json',json.dumps(dict(status='B3_DELIVERED_WITH_NATIVE_WALL',created_utc=datetime.now(timezone.utc).isoformat(),
        files=files,delivery_sha256=sha(delivery),opening_sha256=opening,script_sha256=sha(Path(__file__))),ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(delivery=str(delivery),sha256=sha(delivery))))

if __name__=='__main__':main()
