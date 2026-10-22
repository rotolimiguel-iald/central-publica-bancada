"""Deliver B2 only from completed, reviewed E2/E4/E5 receipts."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,os,sys
B=Path(__file__).resolve().parents[1];R=B.parent;D=R/'TUNEL/DO_CHATGPT'
sys.path.insert(0,str(B/'bis/e2_code'))
from registration_guard import checked_registration,publish_new,sha

def read(n):return json.loads((B/n).read_bytes())
def number(x):return 'OPEN' if x is None else f'{x:.6g}'
def text_new(path,text):
    raw=text.encode();tmp=path.with_name(path.name+'.pending')
    with tmp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    if tmp.stat().st_size!=len(raw):raise OSError('Incomplete delivery retained')
    os.link(tmp,path);tmp.unlink()

def main():
    reg,digest=checked_registration()
    names=['RINGDOWN_5SIGMA_V1.json','bis/E2_REGISTRATION_RECEIPT.json','bis/E2_REVIEW_APPLICATION_V2.json',
      'bis/E2_REGISTRATION_SMOKE.json','bis/E2_NULL_RECEIPTS_AUDIT_V1.json','bis/RESULT_E2_NULL_CAMPAIGN.json',
      'bis/E4_E5_EXECUTION_V1.json','bis/E4_E5_AUTHORIZATION_V1.json','bis/E4_INDEPENDENT_AUTHORIZATION_V1.json',
      'bis/e4_e5_prepare/runs/authorized_001/DETERMINISTIC_DIAGNOSTICS.json',
      'bis/e4_e5_prepare/runs/authorized_001/RESULT_RECEIPT.json',
      'bis/e4_indep_review/runs/authorized_001/INDEPENDENT_REVIEW.json',
      'bis/E2_SEAL_ATTEMPT_001_FAILED_SCRIPT_EXECUTION_POLICY.json',
      'bis/E2_SMOKE_ATTEMPT_001_FAILED_PRIVATE_ACCESS.json','bis/E2_CUSTODY_TRANSFER_BEFORE_V1.json',
      'bis/E2_CUSTODY_TRANSFER_V1.json','bis/E2_CUSTODY_HOST_VERIFIED_V1.json',
      'bis/PART_B_BUDGET_START.json','PORTAO_DA_AMPLIACAO_V1.json','NUISANCE_V1.json',
      'bis/e2_publication_census/E2_RUNTIME_CUSTODY_CLOSING_REVIEW.md',
      'bis/e4_indep_review/E4_E5_INDEPENDENT_REVIEW.md','refeito/repair_e2_runtime_custody_013bis.py']
    files={n:{'sha256':sha(B/n),'bytes':(B/n).stat().st_size} for n in names}
    smoke=read(names[3]);null=read(names[4]);campaign=read(names[5]);execution=read(names[6])
    result=read(names[9]);receipt=read(names[10]);review=read(names[11]);budget=read(names[17]);e0=read(names[18])
    if smoke['status']!='PASS_REAL_REGISTRATION_RUNTIME_WITNESS_AND_E7_CONTEXT_NO_SCIENCE':raise ValueError('Runtime smoke incomplete')
    if null['status']!='RECEIPTS_AND_BINOMIAL_ENDPOINTS_VERIFIED__SYNTHETIC_ONLY' or null['campaign_sha256']!=sha(B/names[5]):raise ValueError('Null audit differs')
    if campaign['failed'] is not None or execution['failure'] is not None:raise ValueError('Unclosed execution failure')
    if receipt['result_sha256']!=sha(B/names[9]) or review['producer_result_sha256']!=sha(B/names[9]):raise ValueError('Review chain differs')
    if review['status']!='PASS_CONDITIONAL_ARITHMETIC_ONLY' or review['failed']!=0:raise ValueError('Independent arithmetic review requests changes')
    if any(v.get('registration_sha256',digest)!=digest for v in (smoke,null,campaign,execution)):raise ValueError('Registration mismatch')
    if result['E2_registration_sha256']!=digest or result['scientific_reading_selected'] is not False:raise ValueError('Scientific scope mismatch')
    if read(names[16])['status']!='HOST_EXCLUSIVE_DACL_AND_UNCHANGED_SEED_COMMITMENT_VERIFIED':raise ValueError('Custody transfer not verified')
    now=datetime.now(timezone.utc);hours=(now-datetime.fromisoformat(budget['started_utc'])).total_seconds()/3600
    opening=D/'ENTREGA_013BIS_ABERTURA_operador.md';witness=D/'ENTREGA_013BIS_E2_REGISTRO_V1.md'
    fiche=B/'REAPROVEITAMENTO_AMPLIACAO_B2.md'
    text_new(fiche,'[REAL — B2; cálculos sintéticos e calibração arquivada NÃO-CEGA]\n\n'
      'Reutilizados E0/E1, QNM/PSDs pinados, posteriores públicos pareados e configuração do registro. Novos: nulos registrados, Fisher440 condicionado, diagnósticos 2D e conferência independente. Nenhuma nova PE, waveform ou posterior de teste.\n\n'
      'PAGO: execução e auditoria descritas na entrega. NÃO PAGO: lnB físico normalizado do440, comparação PE fixed/free equivalente, transferência browniana, sigma_sys e c(SNR) calibrados. N/A — sem Lean; nenhum gate formal alterado.\n\n'
      f'Abertura `{sha(opening)}`. Registro `{digest}`. Resultado E4/E5 `{sha(B/names[9])}`.\n')
    high=[v for v in e0['events_preanalysis'] if v['eligible_INPUT_rule'] is True and v['priority_snr30'] is True]
    lines=['[NÃO-CEGO — B2: registro, nulos sintéticos e diagnósticos condicionais PAGOS; calibração e significância físicas NÃO PAGAS]',
      '', '# B2 — registro, modo440 e rotaIV', '',
      f'Abertura `{opening.name}` — `{sha(opening)}`. Ficha `{fiche.name}` — `{sha(fiche)}`.',
      f'Registro E2 `{digest}`; testemunha `{witness.name}` — `{sha(witness)}`.', '',
      'A testemunha e a ativação precedem as campanhas. O desenho é NÃO-CEGO; nenhuma PE cega foi iniciada nesta etapa. '
      'As dez leituras permanecem paralelas, sem escolher a favorável. O gate físico continua INCONCLUSIVE_SYSTEMATICS.', '',
      '| Item | Pago e limite |','|---|---|',
      '| E2 | PAGO: registro, testemunha, árvores/input/runtime pinados, critérios e nulos sintéticos. A cauda física da pipeline não foi calibrada. |',
      '| E4.1 | PAGO: Fisher440 condicionado a massa/spin e fonte fixa, quatro PSDs, duas variantes, dois perfis e duas convenções de SNR. Degenerescência da fonte livre NÃO PAGA. |',
      '| E4.2 | PAGO: razões de densidade 2D com amostras pareadas, quatro estimadores, bordas/prior e suporte. lnB físico normalizado NÃO PAGO; não se promove KDE4D. |',
      '| E4.3 | PAGO: só220 e220+440 separados. Deformar440 é INPUT; não é escolha inferida dos dados. |',
      '| E4.4 | PAGO: lista nominal E0 por corrida e prioridade por SNR; GW250207_115645 permanece candidato futuro AWAITING_DATA. |',
      '| E5 | PAGO: contrato de amostras completas, LRT nulo heterogêneo, informação1/sigma^4 e secundário registrado. Transferência browniana e sigma_sys físicos NÃO PAGOS. |','',
      '## Nulos registrados', '',
      f"Foram executadas {len(null['cells'])} células, total de {null['total_draws']:,} draws. Parede da campanha: {campaign['wall_seconds']:.3f}s. "
      'O controle gaussiano e o controle com medida elíptica t5 mais nuisance gaussiano são modelos distintos. A covariância E1 é INPUT de curvatura local, não erro físico calibrado. '
      'Cada intervalo abaixo é pontual95%; desacordo ocasional com o valor analítico em várias células não autoriza escolher ou refazer células. Na rotaIV, zero contagens significa limite superior finito, nunca p=0.', '',
      '| Célula | Draws | Excedências | p empírico | UL95 unilateral | p analítico |','|---|---:|---:|---:|---:|---:|']
    for r in null['cells']:lines.append(f"| {r['cell']} | {r['draws']} | {r['false_positives']} | {number(r['empirical_p'])} | {number(r['one_sided_upper95'])} | {number(r['analytic_p'])} |")
    lines += ['', 'Os alvos N90 do portão sem nuisance não garantem90% de poder com nuisance. Não somar significâncias entre modelos de ruído ou leituras.', '',
      '## Modo440: referência declarada', '',
      'Recorte de exibição fixado pelo script: SNR isolado do440=10, perfil FREE_FREQUENCY_FIXED_TAU_GR, mesma SNR por PSD. '
      'Todos os1920 cenários, inclusive amplitude fixa e outro perfil, estão no JSON. Massa/spin e perfil GR da fonte são fixos. '
      'N90 pressupõe fontes independentes idênticas, covariância conhecida e nenhuma sistemática; não é previsão astrofísica.', '',
      '| Leitura | Variante | PSD | delta_tau440 | sigma local | delta/sigma | N90 condicional | Estatuto |',
      '|---|---|---|---:|---:|---:|---:|---|']
    rows=[r for r in result['E4_fisher'] if r['profile']=='FREE_FREQUENCY_FIXED_TAU_GR' and r['snr_route']=='ISOLATED_440_GRID' and r['rho_440_equal_per_PSD_INPUT']==10]
    for r in rows:lines.append(f"| {r['reading']} | {r['variant']} | {r['psd']} | {number(r['delta_tau_440'])} | {number(r['sigma_delta_tau_local_GR'])} | {number(r['expected_local_z'])} | {number(r['N90_conditional'])} | {r['target_status']} |")
    lines += ['', '## Posterior arquivado do440', '',
      'Faixas entre KDE2D nas três bandas e gaussiana por momentos completos; são sensibilidade a estimadores, não IC nem lnB. '
      '220 e440 compartilham o evento e parâmetros: não multiplicar as razões marginais como evidências independentes.', '',
      '| Leitura | Faixa do log de razão de densidade440 | Estatuto |','|---|---|---|']
    for r in result['E4_archived_marginals']['rows']:
        if r['mode']=='440':lines.append(f"| {r['reading']} | {r.get('estimator_range','OPEN')} | {r['status']} |")
    lines += ['', '## Informação e eventos', '',
      'A informação gaussiana local da variância escala com1/sigma^4; esse peso já vem da likelihood e não é multiplicado novamente no LRT. '
      'O contrato de posterior completo permanece explícito; não foi executado ajuste populacional físico nesta etapa.', '',
      '| Conjunto de calibração | Equivalentes GW250114 no cenário sigma_sys=0 |','|---|---:|']
    for r in result['E5_information']:lines.append(f"| {r['population']} | {number(r['N_GW250114_equivalent'])} |")
    lines += ['', '| Evento que passa E0 e SNR>=30 | Corrida | SNR rede público |','|---|---|---:|']
    for r in high:lines.append(f"| {r['event']} | {r['run']} | {r['network_snr']} |")
    lines += ['', '## Revisão, incidentes e custo', '',
      f"A revisão independente passou em {review['passed']} verificações, zero falhas. Compartilha os QNM/PSDs pinados, mas usa derivadas/projeção, somas KDE diretas e fórmulas de informação independentes. "
      'Oito pares de densidade foram predefinidos; não se afirma refit independente universal. Nenhuma revisão transforma o diagnóstico em calibração física.', '',
      'Falhas preservadas: selagem inicial barrada pela política de scripts antes de pasta/seed; substituição por API nativa revisada, sem mudar política. '
      'A primeira integração WSL recusou a semente porque as identidades Windows de criação e runtime diferem. A DACL foi transferida exclusivamente para a identidade do runtime; '
      'o compromisso dos mesmos32bytes foi verificado. Registro, testemunha e seed não foram reescritos. O proprietário Windows original não mudou: a DACL restringe a leitura normal, mas não elimina seus poderes de gerir permissões. Custódia procedural local, sem separação de administradores; nenhum conteúdo da seed ou offset foi divulgado.', '',
      f"E4/E5: {receipt['wall_seconds_through_result_hash']:.6f}s parede; revisão: {review['wall_seconds']:.6f}s. "
      f"Tempo contínuo da Parte B até esta entrega: {hours:.6f}h de40. Deadline `{budget['hard_deadline_utc']}`. Campanhas simultâneas não se somam em dobro.", '',
      'Comandos executados: `python -B bis/e2_code/null_campaign.py`; `python -B refeito/activate_e4_e5_013bis.py`; '
      '`python -B bis/e4_indep_review/independent_review.py --execute --authorization <arquivo pinado> --authorization-sha256 <hash>`; '
      '`python -B refeito/audit_e2_null_receipts_013bis.py`. Runtime WSL /opt/lal_env; BLAS solicitado com1thread. '
      'Saídas são exclusivas; reproduzir em destino isolado sob registro próprio. N/A — sem Lean. Próximo: E3.1, encerramento dos diagnósticos F0, Kerr e piloto, sem parar no marco.', '',
      '## Arquivos e hashes','']
    for name,item in files.items():lines.append(f"- `{name}` — `{item['sha256']}` ({item['bytes']}B).")
    delivery=D/'ENTREGA_013BIS_B2_registro_e_440.md';text_new(delivery,'\n'.join(lines)+'\n')
    manifest={'status':'B2_DELIVERED_CONDITIONAL_ONLY','created_utc':now.isoformat(),'delivery_sha256':sha(delivery),
      'fiche_sha256':sha(fiche),'opening_sha256':sha(opening),'registration_sha256':digest,'witness_sha256':sha(witness),
      'files':files,'hours_elapsed_part_b':hours,'code_sha256':sha(Path(__file__))}
    publish_new(B/'bis/B2_DELIVERY_MANIFEST.json',manifest)
    print(json.dumps({'status':manifest['status'],'delivery':str(delivery),'sha256':sha(delivery),'hours_elapsed':hours}))

if __name__=='__main__':main()
