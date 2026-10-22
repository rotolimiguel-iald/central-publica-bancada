"""Build a reviewable final report from completed stage receipts, without new science."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, math, os

B = Path(__file__).resolve().parents[1]
R = B.parent
D = R / 'TUNEL/DO_CHATGPT'

def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for x in iter(lambda:f.read(1048576), b''): h.update(x)
    return h.hexdigest()

def load(p): return json.loads(Path(p).read_bytes())
def number(x): return 'OPEN' if x is None else format(x, '.6g')
def new(p, raw):
    if isinstance(raw,str): raw=raw.encode()
    tmp=p.with_name(p.name+'.pending')
    with tmp.open('xb') as f: f.write(raw); f.flush(); os.fsync(f.fileno())
    if tmp.stat().st_size!=len(raw): raise OSError('Short staged write')
    os.link(tmp,p); tmp.unlink()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--e6-result',type=Path,required=True)
    ap.add_argument('--e7-review',type=Path,required=True)
    ap.add_argument('--integrity-receipt',type=Path,required=True)
    ap.add_argument('--extra-manifest',type=Path,required=True)
    a=ap.parse_args()
    e7=load(B/'bis/E7_FULLSAMPLE_RESULT_V1.json')
    execution=load(B/'bis/E7_FINAL_EXECUTION_V1.json')
    review=load(a.e7_review)
    if execution['failure'] is not None or review.get('approved') is not True:
        raise ValueError('E7 must pass before final drafting')
    if review.get('e7_result_sha256')!=sha(B/'bis/E7_FULLSAMPLE_RESULT_V1.json'):
        raise ValueError('E7 independent review does not bind result')
    e6=load(a.e6_result); e0=load(B/'PORTAO_DA_AMPLIACAO_V1.json')
    budget=load(B/'bis/PART_B_BUDGET_START.json')
    native=load(B/'bis/e3_pilot_review/PILOT_NATIVE_DIAGNOSIS_CLOSING_REVIEW.json')
    if native['status']!='BOUNDED_DIAGNOSIS_CLOSED_TECHNICAL_WALL_NO_SUPPORTED_PE_ADAPTER':
        raise ValueError('Technical wall not reviewed')
    expected_notes=['ENTREGA_013BIS_ABERTURA_operador.md','ENTREGA_013BIS_MA_fechamento.md',
        'ENTREGA_013_M1_fechamento.md','ENTREGA_013_M2_C4_fechamento.md','ENTREGA_013_M3_C3_2_C2_RMOD.md',
        'ENTREGA_013_M4_C5_parede_e_portao.md','ENTREGA_013_M5_C6pre.md','ENTREGA_013_M6_C7_final.md',
        'ENTREGA_013_ERRATA_contrato.md','ENTREGA_013BIS_B1_portao_e_nuisance.md',
        'ENTREGA_013BIS_E2_REGISTRO_V1.md','ENTREGA_013BIS_B2_registro_e_440.md',
        'ENTREGA_013BIS_B3_piloto_e_orcamento.md','ENTREGA_013BIS_B4_calibracao_e_cegos.md',
        'ENTREGA_013BIS_TESTE_O4_cegos.md','ENTREGA_013BIS_B5_quadro_e_modulo.md']
    paths=[D/n for n in expected_notes]+[a.e6_result,a.e7_review,a.integrity_receipt,a.extra_manifest,
        B/'ORCAMENTO_40H.json',B/'RINGDOWN_5SIGMA_V1.json',B/'NUISANCE_V1.json',
        B/'PORTAO_DA_AMPLIACAO_V1.json',B/'bis/E7_FULLSAMPLE_RESULT_V1.json',
        B/'bis/E7_FINAL_EXECUTION_V1.json',B/'bis/e3_pilot_review/PILOT_NATIVE_DIAGNOSIS_CLOSING_REVIEW.json',
        B/'bis/e3_pilot_failure_diagnostic/MANIFEST.json',
        B/'bis/e3_pyring_review/KERR_V2_POST_RESULT_REVIEW.json',
        B/'bis/M6_MA_DELIVERY_MANIFEST.json',B/'bis/B2_DELIVERY_MANIFEST.json']
    for item in load(a.extra_manifest)['files']:
        p=Path(item)
        if not p.is_absolute(): p=R/p
        paths.append(p)
    paths=list(dict.fromkeys(p.resolve() for p in paths))
    if any(not p.is_relative_to(R) for p in paths): raise ValueError('Output reference outside Chatgpt')
    files={p.relative_to(R).as_posix():dict(sha256=sha(p),bytes=p.stat().st_size) for p in paths}
    now=datetime.now(timezone.utc)
    elapsed=(now-datetime.fromisoformat(budget['started_utc'])).total_seconds()/3600
    if not elapsed<40: raise TimeoutError('Budget envelope expired')
    opening=sha(D/expected_notes[0])
    lines=['[REAL — relatório final da bancada; encerramento por resultados e paredes medidas. Calibração física e teste cego NÃO PAGOS.]','',
        '# ORDEM 013BIS — relatório final','',
        'O trabalho entrega o registro, os resultados condicionais, o quadro de alcance e o módulo de leitura. '
        'Não produziu um novo posterior pSEOB válido nem demonstrou 5σ físico. O piloto IMR terminou em falha nativa; '
        'a revisão do diagnóstico não encontrou um reparo validado que preservasse a região de parâmetros registrada. '
        'Por isso a ampliação por PE foi encerrada como parede técnica nesta configuração, e não como falta de tempo ou impossibilidade geral da rota.','',
        f'Abertura do operador: `{opening}`. A ordem foi conduzida até este relatório, sem parada de marco. '
        'A incorporação no programa canônico e a ratificação continuam com a gerência/operador.','',
        '## Cumprimento por alvo','',
        '| Alvo | PAGO | NÃO PAGO / limite |','|---|---|---|',
        '| F0 | Encerramento conferido dos trabalhos antigos antes do piloto; recibo próprio. | Seus resultados não entram para mudar vereditos. |',
        '| F1 | Entrega M1, correções e portão medido. | Não promove diagnóstico em prova física. |',
        '| F2 | Entrega M2, catálogos, controles e correções ao lado. | C4 permanece INCONCLUSIVE_SYSTEMATICS, NÃO-CEGA. |',
        '| F3 | Entrega M3, template/oráculo e leituras com escopo. | Pontes/identificações abertas não são escolhidas. |',
        '| F4 | Entrega M4, parede C5 e portão do poder. | Calibração livre de massa/spin da C5. |',
        '| F5 | Entrega M5, C6 reclassificada e inícios realizados. | C6 permanece diagnóstico anterior ao portão. |',
        '| F6 | Entrega M6, pacote e reproduções documentadas. | Não converte entrega em evidência física. |',
        '| F7 | Fichas, licenças documentais, arquivos grandes em cache e conferência de integridade. | Custódia/publicação externa não realizadas. |',
        '| F8 | Parte A fechada por resultado/falsificador/parede; MA entregue. | Paredes físicas explicitadas. |',
        '| E0 | Portão refeito, dez leituras, alvos em informação e cenários. | N90 condicionado não garante poder com sistemática real. |',
        '| E1 | Nuisance condicional, seleção documentada e controles existentes. | Eficiência de seleção, normalização e covariância físicas. |',
        '| E2 | Registro com testemunha, hashes, guardas e nulos sintéticos. | Cauda física da pipeline e autorização estatística de descegamento. |',
        '| E3.1 | Comparação Kerr e custo da tentativa IMR; diagnóstico independente. | Reprodução exatamente equivalente do pyRing; posterior pSEOB convergido e custo por evento válido. |',
        '| E3.2 | Orçamento registrado, cinco alternativas, pesos esperados e custo observado separados. | Custo calibrado por posterior/injeção e ganho por hora desconhecidos. |',
        '| E3.3 | Parede, alocação sem novos jobs e estado do gate registrados. | Novas injeções RG/TGL, c(SNR), sigma_sys, cobertura e PE cega. |',
        '| E4 | Fisher440 condicionado, sensibilidade 2D e leituras/modos separados. | Comparação de PE multimodo equivalente e lnB físico normalizado. |',
        '| E5 | Nulo LRT sintético e informação 1/sigma^4. | Transferência browniana na recuperação e sigma_sys físicos. |',
        '| TESTE | Estado sem dados executado/registrado sob E2. | Nenhum evento novo admitido ou descego; AWAITING_DATA. |',
        '| E6 | Quadro gerado por script com origens e revisão. | Projeções futuras não são observações nem promessa de datas. |',
        '| E7 | Extrator e consumidor congelados, amostras pareadas completas e revisão. | Likelihood restrita normalizada, seleção e teste físico não implementados/pagos. |','',
        '## O portão e as dez leituras','',
        'Referência de planejamento: população GWTC5_31, mistura de precisões preservada. '
        'N90 abaixo é o cenário de média gaussiana sem sistemática, não um N garantido para a análise física. '
        'O piso é |delta|/5; |delta|/15 permanece sensibilidade. Sigma(c) físico é OPEN em todas as leituras. '
        'R-GLOBAL dá efeito local zero; zero não é um piso positivo atendido. Correção/sigma é diagnóstico condicional, nunca significância física com gate vermelho.','',
        '| Leitura | delta de referência | Piso primário | N90 mistura (arredondado acima) | Informação-alvo N90 | Correção/sigma condicional dos31 | Estado do teste novo |',
        '|---|---:|---:|---:|---:|---:|---|']
    targets={r['reading']:r for r in e0['planning_targets'] if r['population']=='GWTC5_31'}
    old={r['reading']:r for r in e0['inherited_C4_nonblind'] if r['dataset']=='GWTC5_31'}
    for row in e0['systematic_conditions']:
        t=targets[row['reading']]; n=t['N90_mixture_illustration_not_selection']
        lines.append('| '+ ' | '.join([row['reading'],number(row['delta_GW250114']),number(row['floor5_INPUT']),
            'OPEN' if n is None else str(math.ceil(n)),number(t['I_tau_expected_target90']),
            number(old[row['reading']]['correction_over_sigma']),'AWAITING_DATA; gate vermelho'])+' |')
    lines+=['','Todas as leituras foram preservadas; nenhuma partição, relógio, deformação440 ou realização estocástica foi escolhida. '
        'A RG é o limite clássico/controle. Os escores históricos da C4 ficam nas entregas M2/B1, com seu escopo220 condicional e o veto da cláusula relativa.','',
        '## Resultados que não se confundem','',
        'O controle Kerr do evento conhecido convergiu nos critérios registrados para a variante com PSD pública. '
        'A diferença contra o posterior publicado é descritiva, com famílias/configurações e equivalência incompleta explicitadas em B3. '
        'A variante Welch foi recusada por condicionamento; o primeiro resultado com PSD pública parou parcial. Ambos foram preservados.','',
        'O piloto IMR sofreu SIGSEGV antes de produzir posterior aceito. No diagnóstico isolado, aumentar a frequência de geração '
        'produziu também um aborto de alocação de memória num ponto do prior. A hipótese de capacidade do buffer é CONJECTURE; '
        'a causa exata do SIGSEGV original continua OPEN. Recusar numericamente pontos do prior, remover modos ou estreitar priors '
        'não foi tratado como reparo científico.','',
        'Os nulos sintéticos, o Fisher440 e as razões de densidade foram medidos e revisados. '
        'A cauda t5 excede muito a referência gaussiana5σ; zero excedências em uma simulação finita é apenas um limite superior de probabilidade. '
        'O modo440 não é observação independente do220 no mesmo evento. A rotaIV mantém a dependência da realização estocástica e da transferência ainda aberta.','',
        'As candidatas foram classificadas por metadados anteriores à PE: 14 sem publicação encontrada no escopo, dez sem hold e quatro com hold. '
        'Os pesos esperados são projeções do ajuste em SNR; nenhum desses pesos é informação observada de uma PE nova. '
        'Não houve download de strain novo para teste, posterior novo de teste ou descegamento.','',
        f'E7 processou {e7["calibration_events"]} produtos de calibração. O consumidor devolveu {len(e7["matrix"])} linhas '
        '(dez leituras × duas variantes de modos), sem eventos de teste acrescentados. z físico, lnB físico e correção/sigma física permanecem null.','',
        '## Custo e itens não pagos','',
        f'Contador conservador contínuo até a emissão deste rascunho final: {elapsed:.6f}h de40; saldo {40-elapsed:.6f}h. '
        f'Início `{budget["started_utc"]}`; deadline inalterado `{budget["hard_deadline_utc"]}`. '
        'Orquestração e revisão contam; trabalhos simultâneos não são somados em dobro. O contador final da publicação será atualizado no recibo final.','',
        'Os custos medidos de cada campanha e da tentativa falha estão no orçamento/B3; 11 segundos até um crash não são custo por evento convergido. '
        'As contagens necessárias para calibrar os pisos e as cinco alternativas estão explicitadas, com custo em horas OPEN quando falta medição válida. '
        'Saldo não utilizado não significa que a condição sistemática foi satisfeita. Não se gastou o restante repetindo uma pipeline inválida.','',
        '## Reprodução, incidentes e custódia','',
        'As entregas intermediárias contêm os comandos e fichas por alvo. Execuções recusam destinos existentes: '
        'reprodução exige cópia isolada e novo registro quando altera o instrumento. O extrator usa h5py no runtime pinado; '
        'o consumidor usa NumPy, valida os hashes e preserva amostras completas. N/A — sem Lean; nenhum teorema/gate formal movido.','',
        'Foram conservados os abortos, resultados parciais, correções documentais de hashes, revisões recusadas e versões substituídas. '
        'A custódia da semente é procedural no mesmo host; não representa separação de administradores. Nenhum conteúdo de semente ou offset foi divulgado. '
        'O detalhamento das tentativas de selagem, permissões e do código de preparação permanece em B2/B3/B5 e nos manifestos.','',
        'A conferência final dos insumos/fontes/ParteA está no recibo de integridade: qualquer exceção de leitura de metadados é explícita. '
        'Não houve edição de canônico, kernel, memória, Atlas, site ou espelho, nem commit/push/publicação. '
        'O pacote da bancada aguarda auditoria externa da gerência e ratificação do operador, como determina a ordem.','',
        '## Arquivos, hashes e portas de auditoria','']
    for name,entry in files.items():
        lines.append(f'- [{name}](<{(R/name).as_posix()}>) — `{entry["sha256"]}` ({entry["bytes"]} B).')
    draft=B/'bis/FINAL_REVIEW_DRAFT.md'
    new(draft,'\n'.join(lines)+'\n')
    manifest=dict(status='DRAFT_FOR_INDEPENDENT_FINAL_REVIEW',created_utc=now.isoformat(),
        draft_sha256=sha(draft),files=files,elapsed_wall_hours=elapsed,opening_sha256=opening,
        script_sha256=sha(Path(__file__)))
    out=B/'bis/FINAL_REVIEW_DRAFT_MANIFEST.json'
    new(out,json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(draft=str(draft),sha256=sha(draft),manifest_sha256=sha(out))))

if __name__=='__main__':main()
