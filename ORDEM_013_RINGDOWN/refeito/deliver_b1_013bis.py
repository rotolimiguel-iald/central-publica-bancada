"""Seal E1's conditional scope and deliver B1 with every unpaid layer visible."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,math
B=Path(__file__).resolve().parents[1];R=B.parent;D=R/'TUNEL/DO_CHATGPT'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(n):return json.loads((B/n).read_bytes())
def create(p,value):
    raw=value if isinstance(value,bytes) else (json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
    if p.exists():raise FileExistsError(p)
    tmp=p.with_suffix(p.suffix+'.pending')
    with tmp.open('xb') as f:f.write(raw)
    if tmp.read_bytes()!=raw:raise IOError('Temporary bytes differ')
    try:os.link(tmp,p)
    finally:tmp.unlink()
def main():
    names=['PORTAO_DA_AMPLIACAO_V1.json','PORTAO_DA_AMPLIACAO_V1.md',
      'bis/e1_nuisance_v2/runs/authorized_001/NUISANCE_DIAGNOSTIC.json',
      'bis/e1_nuisance_v2/runs/authorized_001/RECEIPT.json','bis/e1_nuisance_v2/DESIGN_MANIFEST.json',
      'bis/e1_nuisance_v2/AUTHORIZATION.json','bis/e1_nuisance_v2/prepare_e1.py','bis/e1_nuisance_v2/PLAN.md',
      'bis/e1_nuisance_v2/FAILURE_001.json','bis/e1_nuisance_v2/RESULT_SCOPE_NOTE.md',
      'bis/E1_DIRECT_KDE_REVIEW.json','bis/E1_INDEPENDENT_SCOPE_REVIEW.md',
      'bis/e1_selection/SELECTION_AND_CONTROLS.json','bis/e1_selection/SELECTION_AND_CONTROLS.md',
      'bis/e1_selection/SOURCE_PASSAGES.json','bis/e1_selection/RECEIPT.json',
      'bis/e1_selection/NUISANCE_SCOPE_CONTROLS.json','bis/PART_B_BUDGET_START.json']
    files={n:{'sha256':sha(B/n),'bytes':(B/n).stat().st_size} for n in names}
    raw=read(names[2]);receipt=read(names[3]);selection=read(names[12]);review=read(names[10]);gate=read(names[0])
    if receipt['result_sha256']!=files[names[2]]['sha256'] or review['result_sha256']!=receipt['result_sha256']:raise ValueError('Review result chain differs')
    if review['status']!='PASS_INDEPENDENT_DIRECT_KDE_GR_RB__CONDITIONAL_ONLY':raise ValueError('Numerical review failed')
    for n,h in selection['source_hashes'].items():
        p=Path(n)
        if sha(p)!=h['sha256']:raise ValueError('Selection source changed')
    allowed=[f for f in raw['fits'] if f['result']['status']=='CONDITIONAL_DENSITY_DIAGNOSTIC_NOT_CALIBRATED_TEST']
    unpaid=[f for f in raw['fits'] if f not in allowed]
    if len(allowed)!=288 or len(unpaid)!=36 or len(raw['events'])!=33:raise ValueError('Unexpected E1 coverage')
    gr=next(f['result'] for f in allowed if f['reading']=='GR' and f['group']=='GWTC5_31' and f['covariate']=='sigma' and f['bandwidth_factor']==1)
    rho=next(f['result'] for f in allowed if f['reading']=='GR' and f['group']=='GWTC5_31' and f['covariate']=='inverse_SNR' and f['bandwidth_factor']==1)
    value={'status':'NONBLIND_CONDITIONAL_NUISANCE_V1__PHYSICAL_CALIBRATION_AND_SELECTION_OPEN',
      'created_utc':datetime.now(timezone.utc).isoformat(),'E0_sha256':files[names[0]]['sha256'],
      'observable':'Marginal dtau220, with df220 free/integrated; not joint GR point or calibrated population likelihood',
      'primary_calibration_fit':'Fullsample paired residual u=dtau-delta_L(Mdet,spin,z), KDE nominal Scott; df integrated',
      'conditional_diagnostics':raw,'selection_and_controls':selection,
      'synthetic_E2_nuisance_INPUT':{'reference':'GR means dtau=0 with df marginalized, not full GR',
        'population':'GWTC5_31','sigma_model':{'mean_c0_k':[gr['c0'],gr['k']],'covariance':gr['covariance']},
        'SNR_model':{'mean_c0_k':[rho['c0'],rho['k']],'covariance':rho['covariance'],'x':'40/SNR_GWOSC'},
        'status':'INPUT_GAUSSIAN_LOCAL_CURVATURE_FOR_SYNTHETIC_NULL_ONLY_NOT_PHYSICAL_COVARIANCE',
        'bandwidth_sensitivity':'All 0.7/1/1.4 fits remain in diagnostics; physical uncertainty not exhausted by nominal matrix'},
      'gate':{'systematic_calibration_paid':False,'sigma_c_physically_calibrated':None,'selection_efficiency':None,
        'global_restricted_prior_normalization':None,'physical_likelihood_paid':False,
        'maximum_current_verdict':'INCONCLUSIVE_SYSTEMATICS','fixed_offset_zero':'PROIBIDA_COMO_TESTE'},
      'acceptance_by_item':{'E1.1':'PAGO_CONDITIONAL_FULLSAMPLE_DIAGNOSTIC; physical calibration unpaid',
        'E1.2':'PAGO_SOURCE_SECTIONS_AND_OPERATIONAL_RULE; efficiency and full-paper reading unpaid',
        'E1.3':'PAGO_INVENTORY_AND_SINGLE_POINT_LIMIT; bias versus SNR curve unpaid',
        'E1.4':'PAGO_TWO_DISTINCT_ARCHIVED_ESTIMATORS_WITH_N_ERRORS; transfer unpaid',
        'E1.5':'PAGO_DESCRIPTIVE_DISTANCES; calibrated GR/prediction separation unpaid'},
      'independent_reviews':{'numeric':names[10],'scope':names[11]},'source_files':files,
      'not_performed':['New posterior download','New PE','Waveform generation','Physical 5sigma','Canonical code/memory/site modification'],
      'code_sha256':sha(Path(__file__))}
    create(B/'NUISANCE_V1.json',value)
    opening=D/'ENTREGA_013BIS_ABERTURA_operador.md';budget=read('bis/PART_B_BUDGET_START.json');now=datetime.now(timezone.utc)
    hours=(now-datetime.fromisoformat(budget['started_utc'])).total_seconds()/3600
    fiche='REAPROVEITAMENTO_AMPLIACAO_B1.md'
    ftext=f'''[REAL — reaproveitamento B1; NÃO-CEGO; sem novo dado de teste]

Reutilizado: posteriores publicados, fontes primárias, C4, estimadores C2/C5, injeção única LVK e RD; todos com hashes nos manifestos. Não repetidos C5, PE, ondas ou downloads de posterior. Novos: cálculos E0, MC de poder, ajuste E1 fullsample, controles diretos e revisões; código em refeito/ e bis/. Artefatos originais imutáveis.

PAGO: portão condicional, informação esperada, critério pré-análise, nuisance descritivo e limites de seleção. NÃO PAGO: seleção normalizada, calibração física pSEOB, ponte jitter, novo teste. Axiomas N/A — sem Lean; teoremas zero.

Prova: PORTAO_DA_AMPLIACAO_V1.json `{sha(B/'PORTAO_DA_AMPLIACAO_V1.json')}`; NUISANCE_V1.json `{sha(B/'NUISANCE_V1.json')}`. Abertura `{sha(opening)}`. As hipóteses continuam explícitas; nada move gate.
'''
    create(B/fiche,ftext.encode())
    lines=['[NÃO-CEGO — B1 entregue: portão e nuisance condicionais PAGOS; calibração física e eficiência de seleção NÃO PAGAS]',
      '', '# B1 — portão da ampliação e nuisance', '',
      f"Abertura vinculante: `{opening.name}`, SHA256 `{sha(opening)}`. Ficha `{fiche}`, SHA256 `{sha(B/fiche)}`.", '',
      'E0 conserva dez leituras, cinco conjuntos e os resultados C4 herdados. O alvo é informação esperada, condicionado à mistura de sinais/precisões, não uma seleção por largura posterior. N90/N50=1,578315602824 no cenário gaussiano de média; rotaIV calculada separadamente por MC.', '',
      'O critério [INPUT] usa SNR GWOSC≥12, mediana GR Mf,det≥40 M☉ e 0≤χf<0,98, com prioridade SNR≥30. Na cobertura atual O4b, 27 passam entre 45 com SNR≥12; um aguarda Mf/χf. A ausência de metadados não é reprovação física; o censo de teste e preenchimento de metadados serão fixados em E2 antes de PE.', '',
      '| Alvo | Estatuto e prova |','|---|---|',
      '| E0.1–E0.5 | PAGO: combinações, alvos, SNR, tendência e falsificador espúrio. Offset zero PROIBIDA_COMO_TESTE. |',
      '| E0.6 | PAGO como parede: controles C5 recalculados; σ(c) pSEOB livre NÃO PAGO. Gate de admissão falso. |',
      '| E0.7–E0.8 | PAGO como cenários com fontes/datas e C4 herdada; nenhuma promessa de calendário. |',
      '| E1.1 | PAGO no escopo condicional: 33 eventos, 608.681 amostras pareadas; 288 ajustes e 36 recortes não identificáveis preservados. |',
      '| E1.2 | Regra pSEOB inspiral E pós-inspiral≥8 documentada em seções primárias; eficiência α(Λ) e leitura integral dos artigos NÃO PAGAS. |',
      '| E1.3 | Uma injeção LVK com duas recuperações; curva por SNR NÃO PAGA. RD não mede 220 livre. |',
      '| E1.4 | Dois estimadores C2/C5 com N/erro, sem juntá-los numa curva física. |',
      '| E1.5 | Distâncias locais descritivas PAGAS; significância/separação física NÃO PAGA. |','',
      f"No ajuste principal c(σ), referência δτ=0 com δf marginalizado: c0={gr['c0']:.6f} ±{gr['stderr'][0]:.6f}, k={gr['k']:.6f} ±{gr['stderr'][1]:.6f}. Erros de curvatura local, não intervalos calibrados. O controle mediana/q90 reproduz −0,061048529 ±0,068315127 e k=0,791656052 ±0,369307648; a diferença é de estimador, não ganho físico demonstrado.", '',
      'R-B residual no mesmo recorte: −0,032749 ±0,049576. As leituras são ajustadas sobre os mesmos dados e compartilham o nuisance: não somar essas variâncias como independentes. Todas as bandas e recortes ficam no JSON. Nenhuma leitura escolhida.', '',
      'A verificação independente por KDE exata conferiu oito ajustes GR/R-B, sem importar o produtor; maior distância entre parâmetros =0,001506 na métrica local. Outra revisão conferiu escopo, priors, 297 identidades de momentos e cadeia de custódia. Para as demais leituras, a verificação combina controles diretos do produtor e revisão documental; não se afirma refit independente integral.', '',
      'As declarações Uniform não fecham a normalização global do modelo restrito. Portanto os escores E1 não são lnB nem likelihood hierárquica calibrada. NUISANCE_V1 transporta a matriz nominal apenas como INPUT para nulos sintéticos de E2; σ(c) físico permanece null.', '',
      f"Custo do ajuste: {receipt['wall_seconds']:.6f} s de parede e {receipt['cpu_seconds']:.6f} s CPU. Revisão direta: {review['wall_seconds']:.6f} s. Tempo contínuo consumido na Parte B ao fechar esta nota: {hours:.4f} h de 40; deadline `{budget['hard_deadline_utc']}`. Simultaneidade não é somada em dobro.", '',
      'Tentativas preservadas: v1 parou antes da leitura HDF por ausência de threadpoolctl; v2 retirou só essa dependência e executou. Contagem de threads foi solicitada por ambiente, não medida. Dois candidatos MC da mistura33 falharam o limite inferior de poder e subiram na grade já fixada; os negativos permanecem. Guardas MC corrigidas ao lado, com custódia posterior explicitada.', '',
      'Reprodução: planos/manifestos, scripts e comandos nos recibos vinculados abaixo. Os produtores recusam saída existente: repetir em cópia isolada e destino novo. Não executar o canônico. N/A — sem Lean; zero teoremas.', '',
      '**Próximo passo obrigatório:** E2 com código completo, nulos sintéticos e testemunha no túnel antes de qualquer dado/PE de teste; depois E5/E4 e piloto. B1 não encerra a ordem.', '',
      '## Arquivos e hashes', '',f"- `NUISANCE_V1.json` — `{sha(B/'NUISANCE_V1.json')}`."]
    for n,h in files.items():lines.append(f"- `{n}` — `{h['sha256']}` ({h['bytes']} B).")
    delivery=D/'ENTREGA_013BIS_B1_portao_e_nuisance.md';create(delivery,('\n'.join(lines)+'\n').encode())
    create(B/'bis/B1_DELIVERY_MANIFEST.json',{'utc':now.isoformat(),'delivery_sha256':sha(delivery),
      'nuisance_sha256':sha(B/'NUISANCE_V1.json'),'E0_sha256':sha(B/'PORTAO_DA_AMPLIACAO_V1.json'),
      'fiche_sha256':sha(B/fiche),'opening_sha256':sha(opening),'hours_elapsed_part_b':hours,'code_sha256':sha(Path(__file__))})
    print(json.dumps({'delivery':str(delivery),'sha256':sha(delivery),'nuisance_sha256':sha(B/'NUISANCE_V1.json'),'hours_elapsed':hours}))
if __name__=='__main__':main()
