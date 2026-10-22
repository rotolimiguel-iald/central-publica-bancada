"""Publish the additive activation correction and the phase-L index."""
from pathlib import Path
from datetime import datetime, timezone
import json,sys
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent; B=D.parents[1]; ROOT=B.parent
OUT=ROOT/'TUNEL/DO_CHATGPT'; R=ROOT/'ORDEM_016_QG'
sys.path.insert(0,str(R))
from prepare_part_d import write,save,sha

def main():
    at=datetime.now(timezone.utc).isoformat()
    result=json.loads((D/'activation_v2/REGISTERED_RESULT.json').read_bytes())
    reg=B/'RINGDOWN_5SIGMA_V1_1_2.json'
    assert sha(reg)==result['registration_sha256']
    assert result['allocation_chain_verified'] and result['actual_guard_outcome']['expected']
    old=OUT/'ENTREGA_015_MEDIDA_ativacao_por_elo.md'
    opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    note=f'''[REAL — integração corrigida em cópia versionada; nenhuma alteração científica]

# Resolução ao lado da MEDIDA de ativação

Abertura016SHA256: {opening}
Data: {at}
supersedes: {old.name}; sha256: {sha(old)}

Correção de escopo da nota anterior: T03-C e T03(xi) já autorizam reparar as sondas/guarda e registrar uma subemenda. Foi feito em árvore irmã NOVA `bis/e2_code_v1_1_2`, alterando somente `check_activation_v1_1`. A identidade da testemunha determina o recibo imutável daquele elo; recibos antigos continuam intactos. V1.1.1 não é retroativamente declarada executável.

Registro atual V1.1.2: {sha(reg)}. Guarda: {result['guard_sha256']}. Recibo: {result['receipt_sha256']}. A execução real de checked_registration em /opt/lal_env passou pelas verificações e recusou somente o relógio R7 ainda ausente, como esperado. A cadeia do orçamento foi verificada.

Controles: 53 executados nesta correção; 109 anteriores transportados por identidade de código/AST, NÃO reexecutados. Evidência: `ORDEM_013_RINGDOWN/bis/015/activation_v2/REGISTERED_RESULT.json`, sha256 {sha(D/'activation_v2/REGISTERED_RESULT.json')}.

Máquina pesada 0h; chamadas externas novas 0; custo da coordenação não informado. Nenhuma semente/dado cego aberto, nenhum canônico ou gate modificado. Próximo: R7 imediatamente antes dos nulos T03.
'''
    write(OUT/'ENTREGA_015_MEDIDA_ativacao_por_elo_RESOLVIDA.md',note.encode())
    sources=[B/'bis/015/t05/RESULT.json',B/'bis/015/t06/RESULT.json',
        B/'bis/neutrino_m2_reader/DELIVERY.json',B/'bis/e7_prepare_v1_1/DELIVERY.json',
        B/'ORCAMENTO_015_v1.json',reg,D/'activation_v2/REGISTERED_RESULT.json']
    table='\n'.join(f'- `{p.relative_to(ROOT).as_posix()}`: `{sha(p)}`' for p in sources)
    text=f'''[REAL — fase leve concluída; projeções condicionais não são detecção]

Abertura015SHA256: {sha(OUT/'ENTREGA_015_ABERTURA_operador.md')}
Abertura016SHA256: {opening}
Data: {at}

T05: QNM pareado 220 e 440, com hipóteses e limitações. T06: rota IV não cega sobre calibração; LRT não convertido em sigma físico. T11: leitor neutrino, 19 controles e referência reproduzida; nenhuma observação nova. T12: consumidor rito, 53 controles históricos e 72 aplicáveis da variante; replay não cego rc0 e 330 linhas220 concordantes com T05. O 440 é transportado, não reextraído.

Orçamento 9b registrado e testemunhado. A falha de ativação encontrada após T12 está resolvida na V1.1.2, com recibos anteriores preservados. Ver nota RESOLVIDA. Nenhum job pesado ou relógio iniciado nesta entrega. Gate permanece inalterado; originais preservados.

Artefatos conferidos:
{table}

O fechamento parcial016 permanece selado: PRONTO.json SHA256 {sha(OUT/'FECHAMENTO_PARCIAL_016/PRONTO.json')}. Nenhum pedido corretivo RECIBO_016_FECHAMENTO_PARCIAL*.md presente neste instante.

→ CONTINUE: R7, 30 células nulas T03, piloto T04; limite de processos e alocações mantidos. Não autoriza PE cega nem 440 livre.
'''
    write(OUT/'ENTREGA_015_P_leves.md',text.encode())
    write(OUT/'ENTREGA_015_FASE_L_CONCLUIDA.md',('[REAL]\n\nAbertura016SHA256: '+opening+'\n\nÍndice: ENTREGA_015_P_leves.md; sha256 '+sha(OUT/'ENTREGA_015_P_leves.md')+'\nR7 ainda ausente; pronto para passo10 conforme recibo de máquina livre.\n').encode())
    p=OUT/'ENTREGA_016_PROGRESSO.md'
    write(p,p.read_bytes()+f'\n{at} | B/faseL e ativação | PAGO integração V1.1.2;53 controles frescos+109 herdados | máquina0h | próximo R7/T03\n'.encode(),True)
    cp=R/'A7/CONTINUIDADE.json'; state=json.loads(cp.read_bytes())
    state.update(at=at,next='PART_B_R7_THEN_T03_NULLS',next_action='PART_B_R7_THEN_T03_NULLS',active_process=None,
        current_code_directory=str(B/'bis/e2_code_v1_1_2'),current_registration_sha256=sha(reg),
        activation_result=str(D/'activation_v2/REGISTERED_RESULT.json'),
        budget_delivery=str(D/'BUDGET_V1_DELIVERY.json'))
    save(cp,state,True)
    print(json.dumps({'phase_L':'DELIVERED','registration_sha256':sha(reg),'clock_started':False}))
if __name__=='__main__':main()
