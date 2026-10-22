"""Add a dated correction beside historical state, with byte backups and CAS."""
from pathlib import Path
from datetime import datetime, timezone
import json
from audit_inputs import file_info, save_json, safe_write
from reconcile_documentary_milestone_20261006 import verify_manifest

ROOT = Path(__file__).resolve().parent
MEM = Path(r'C:\IALD\Central de Patentes\memory')
SLOT = Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\state\handoffs\slot_management.json')
MARK = '<!-- ORDEM018_V2_BOUND_ACCEPTED_INIT003_TERMINAL_20261006 -->'

def append_once(path, text):
    before = path.read_bytes()
    if MARK.encode() in before:
        raise RuntimeError('Milestone already recorded: ' + str(path))
    data = before + ('\r\n\r\n' + text.replace('\n', '\r\n') + '\r\n').encode('utf-8')
    assert path.read_bytes() == before, 'Concurrent memory write'
    safe_write(path, data)
    assert path.stat().st_size > len(before)
    return {'before_bytes': len(before), 'after': file_info(path)}

def update_json(path, mutate):
    old = path.read_bytes()
    value = json.loads(old)
    mutate(value)
    assert path.read_bytes() == old, 'Concurrent state update'
    save_json(path, value)
    return file_info(path)

def main():
    now = datetime.now(timezone.utc).isoformat()
    f = ROOT / 'f9_calibration_bound'
    review = ROOT / 'derivacoes/revisao_cota_calibracao_f9'
    pins = {
        'verdict_v2': file_info(ROOT / 'f9_verdict_contract/F9_VERDICT_CONTRACT_CANDIDATE_V2.json'),
        'proof': file_info(f / 'PROVA_COTA_CALIBRACAO_F9.md'),
        'bound': file_info(f / 'CALIBRATION_BOUND_CANDIDATE.json'),
        'bound_review': file_info(review / 'RECIBO_REVISAO_COTA_F9.json'),
        'terminal': file_info(ROOT / 'preregistros/conjunto_d/p3_init_qualified_003/RECIBO_ROOT_ENCERRAMENTO_INIT003.json'),
        'terminal_review': file_info(ROOT / 'proveniencia/revisao_encerramento_init003/RECIBO_REVISAO_ENCERRAMENTO_INIT003.json'),
        'D_proposal': file_info(ROOT / 'preregistros/conjunto_d/d_psd_dq_contract/CONTRATO_PSD_DQ_SELECAO_D_PROPOSTA.json')}
    checked = verify_manifest(review / 'MANIFESTO_REVISAO_COTA_F9.json')
    gr = json.loads((ROOT / 'preregistros/conjunto_d/p3_init_qualified_003/EXECUTION_INIT_QUALIFIED_003/P3_GR_INIT_QUALIFIED_003/RESULT.json').read_bytes())
    assert gr['status'] == 'STOPPED_NOT_CONVERGED' and gr['likelihood_calls'] == 9738
    assert len(gr['blocked_operations']) == 5 and not gr['D_read']
    text = f'''{MARK}
## 06/10/2026 UTC — Cota F9 aceita condicionalmente; INIT003 terminal e não qualificado

[REAL documental] O contrato de veredito F9 recebeu correção VC-01 separada: V2 exige disponibilidade e calibração completas para declarar não-rejeição; uma rejeição válida não desaparece porque outro teste está indisponível. A regra antiga de z indefinido/underpowered antecipado é histórica e não executável. Revisão478 e aceite ROOT preservados. V2 SHA256 {pins['verdict_v2']['sha256']}; não ratificado como V1 e sem autorização de abertura.

[DERIVED condicional, revisão independente484 aceita] Sob erro gaussiano com C fixa/comum/conhecida e suporte comum, perfil linear eta63 dá cota uniforme de cauda por chi2_nu. Diferenças de médias globalmente contidas nas16 coordenadas de fundo+a_h(+c_C) permitem limites estruturais17 para Q/T21/T51 e18 para T41. G1 usa a dimensão residual justificada;148 somente com os72 vínculos exatos e X suportado. Não são postos medidos ou Wilks. Certificados L_i<=g_i<=U_i e limite superior da SF preservam conservadorismo; máximo sobre todos os cenários e Bonferroni5 permanecem. A prova não certifica covariância estimada, modelo físico, mínimos globais ou poder. Prova SHA256 {pins['proof']['sha256']}; recibo da revisão SHA256 {pins['bound_review']['sha256']}. Oito controles determinísticos em preparação, ainda não executados; sem Monte Carlo extremo obrigatório nem nova cauda observada.

[REAL — campanha sintética encerrada479, auditoria482 aceita em483] INIT003 teve autorização específica476 após revisão475 e foi executada uma vez. GR terminou {gr['status']} com {gr['likelihood_calls']} avaliações/{gr['native_calls']} chamadas nativas, parede{gr['wall_s']:.9f}s, CPU{gr['cpu_s']:.9f}s e delta_logZ{gr['delta_logz_before_live_addition']:.9f}; ESS ausente. Cinco tentativas de cache pyc foram bloqueadas mas não provocaram parada durante a amostragem. O supervisor aceitou indevidamente o parcial e iniciou RB; ROOT conferiu identidade/grupo e enviou SIGTERM. RB retornou−15 sem RESULT, sem totais finais conhecidos. Último progresso não vira total. Campanha não qualificada, sem cobertura/recuperação/veredito. Recibo terminal SHA256 {pins['terminal']['sha256']}. Dois defeitos confirmados: guard persistente ausente durante sampler e aceitação/exit do supervisor inadequados. Reparos e controles com doubles são preparação separada, não autorização para repetir PE. Todos os jobs consumidos permanecem terminais.

[REAL documental / PROPOSTA480] ContratoD oferece A256s Welch-mediana ou B512s Welch-média, com janela/grade/seleção por flags definidas. B não cabe no arquivo nomeado do último evento sob exclusão64s; a geometria não mede DQ. Nomes/máscaras DQ, envelopes/tratamento de calibração e qualificação do limiar de estacionariedade2 continuam OPEN. Nenhuma opção ratificada;14 eventos/ordem/quatro holds/V1 preservados; zero séries ou posteriores D abertos. Contrato SHA256 {pins['D_proposal']['sha256']}.

[REAL operacional] Fila conferida: uma coordenação Claude antiga prompt_ready bloqueada por geração canônica divergente, zero execuções e limites5/3/1; registrado needs_attention, sem repin/retry/cobrança duplicada. A entrega6273 da gerente foi recebida e conferida24 arquivos. Não houve novo provedor remoto/Work, abertura F9/D, original canônico, versão científica, kernel ou gate alterado. A recusa automática anterior do download SBF permanece preservada sem repetição. Continuidade: rascunho F9 consolidado e controles instrumentais preparados em paralelo; objetivo ainda em curso.'''
    updates = []
    for path in [MEM / 'TGL_ATLAS.md', MEM / 'TGL_INDICE_VIVO.md', MEM / 'TGL_CORE_MEMORY.md', ROOT / 'ENTREGA_018_F1_HUBBLE.md', ROOT / 'ENTREGA_018_F3_PRIMORDIAL_E_RINGDOWN.md']:
        updates.append(append_once(path, text))
    choice_text = f'''{MARK}
## Atualização das escolhas — {now}

As propostas anteriores permanecem históricas. Fundo direto foi medido em cinco pares de precisão (recibo470), e o fluxo SN/preflight262 foram revistos. Essas medidas não qualificam o domínio físico inteiro nem a inferência sobre novos centros.

Recomendo o contrato de veredito V2, com testes G1/Q1/T21/T41/T51 separados de lnB. A cota analítica revisada484 é a candidata de calibração: G por dimensão residual justificada; Q/T pelo span global17/18 quando demonstrado na implementação. Alternativa mais conservadora é usar dimensão residual para todos; cauda específica mais apertada continua opção futura se necessária. Ausência de calibração não significa não-rejeição, e cota válida frouxa não é ausência de calibração.

Continuam necessários os certificados de mínimos/SF e a especificação explícita do modelo gaussiano e da covariância. As cinco variâncias maser permanecem simbólicas na preparação sem centros; propagação aproximada ou covariância estimada não recebe validade finita da prova por mera declaração. O cenário condicional com erros publicados pode ser proposto com seu alcance, sem prometer cobertura física além do modelo.

O rascunho consolidado está sendo preparado sem modificar as fontes consumidas. V2 SHA256 {pins['verdict_v2']['sha256']}; cota candidata SHA256 {pins['bound']['sha256']}. Nada neste adendo congela V1 ou autoriza ler o composto.'''
    updates.append(append_once(ROOT / 'F9_ESCOLHAS_CONCRETAS_PROPOSTAS.md', choice_text))
    def cont(v):
        v['updated_at'] = now
        v['phases']['F1'] = 'E45_COMPLETE; VERDICT_V2_AND_CONDITIONAL_BOUND_REVIEW_ACCEPTED; CLEAN_DRAFT_AND_CONTROLS_PREPARATION; OBSERVED_COMPOSITE_CLOSED'
        v['phases']['F3'] = 'INIT003_TERMINAL_UNQUALIFIED_AUDIT_REVIEW_ACCEPTED; D_PSD_DQ_PROPOSAL_UNRATIFIED; GUARD_REPAIR_PREPARATION_ONLY; D_CLOSED'
        v['milestone_sequences'] = sorted(set(v.get('milestone_sequences', []) + [479,480,481,482,483,484]))
        v['next_steps'] = ['Review and qualify new bounded analytic-calibration controls after exact contract and specific decision.', 'Consolidate clean F9 candidate without observed data; distinguish model assumptions and numerical certificates.', 'Prepare and review isolated persistent audit-guard/supervisor repair using doubles only; no new PE authorization.', 'Complete concrete DQ/calibration policy and preserve operator decision before D/F9 opening.']
        v['analytic_bound_review_accepted'] = pins['bound_review']
        v['analytic_bound_candidate'] = pins['bound']
        v['synthetic_terminal_review'] = pins['terminal_review']
        v['D_PSD_DQ_proposal'] = pins['D_proposal']
        v['synthetic_active_session'] = None
    updates.append(update_json(ROOT / 'CONTINUIDADE.json', cont))
    def candidate(v):
        v['current_documentary_companions_20261006'] = {'at': now, 'verdict': pins['verdict_v2'], 'calibration': pins['bound'], 'independent_review': pins['bound_review'], 'status': 'REVIEWED_CONDITIONAL_PROPOSALS_NOT_FROZEN_V1', 'supersedes_for_future_draft': ['top-level undefined z verdict_proposal_order', 'early underpowered return', 'aggregated pure-ladder H4 response'], 'opening_authorized': False, 'old_fields_retained_as_history': True}
    updates.append(update_json(ROOT / 'FASE9_V1_CANDIDATE.json', candidate))
    def request(v):
        v.update({'status': 'RESPONDED_CONDITIONAL_PROOF_REVIEW_ACCEPTED', 'resolved_at': now, 'response_manifest': file_info(f / 'MANIFESTO_ENTREGA.json'), 'review': pins['bound_review'], 'map_seq': 484, 'opening_authorized': False})
    updates.append(update_json(ROOT / 'F9_CALIBRATION_BOUND_REQUEST.json', request))
    def slots(v):
        request(v['ordem018_calibration_bound_request'])
    updates.append(update_json(SLOT, slots))
    receipt = {'at': now, 'marker': MARK, 'status': 'ADDITIVE_DOCUMENTARY_MILESTONE_NO_NEW_SCIENCE', 'review_manifest_checked': checked, 'source_pins': pins, 'updated': updates, 'backup_policy': 'Exact prior bytes in same directory; atomic temporary replacement; CAS; no backups removed.'}
    save_json(ROOT / 'RECIBO_MEMORIA_V2_BOUND_INIT003_TERMINAL.json', receipt)
    print(json.dumps({'receipt': file_info(ROOT / 'RECIBO_MEMORIA_V2_BOUND_INIT003_TERMINAL.json'), 'updated': len(updates), 'scientific_execution': False}))

if __name__ == '__main__':
    main()
