"""Task memory and partial handoff from current measured artifacts.

No canonical Atlas, um.py, kernel or published surface is modified.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
from fetch_public import atomic_json

ROOT=Path(__file__).resolve().parent

def read(name):return json.loads((ROOT/name).read_bytes())

def append_atomically(path,text):
    previous=path.read_bytes() if path.exists() else b''
    if previous:
        stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        backup=path.with_name(path.name+'.bak_'+stamp)
        backup.write_bytes(previous)
        assert backup.read_bytes()==previous
    raw=previous+text.encode('utf-8')
    temporary=path.with_suffix(path.suffix+'.tmp');temporary.write_bytes(raw)
    assert temporary.stat().st_size==len(raw)
    temporary.replace(path)

def main():
    c0,c2,c4,valid,fisher=[read(p) for p in ['C0_AUDITORIA.json','C2_TEMPLATE_CHECKS.json',
                       'C4_220_INITIAL.json','C4_VALIDATION.json','C5_FISHER.json']]
    b=next(r for r in c4['rows'] if r['reading']=='R-B')
    refs=['C0_AUDITORIA.json','C0_AUDITORIA.md','C0_C3_checks.json','C2_MAPEAMENTO_ANALITICO.md',
          'C2_TEMPLATE_CHECKS.json','tgl_ringdown_prediction.py','tgl_ringdown_template.py',
          'C5_FISHER.json','PSD_CONTROLS.json','FISHER_INPUTS.json',
          'REGISTRO_C4.json','C4_SCHEMA.json','C4_220_INITIAL.json','C4_VALIDATION.json']
    hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in refs}
    now=datetime.now(timezone.utc).isoformat()
    remaining=[
      'C0: arquivar fontes primárias consultadas, com hash; não alegar leitura integral dos cinco relatórios de gerência.',
      'C1: tabela completa de todas as leituras, relógios, partições, unidades, efeitos de distância e exclusões condicionais da v369.',
      'C2: distribuição dos estimadores em trajetórias com ruído colorido; tratar lei linear/Cauchy e raiz sem impor desenrolamento browniano.',
      'C3: verificar integração com consumidor de inferência; campo coerente-raiz não é exponencial; optional 221 não implementado.',
      'C4: R-MOD em grade exata, priors livres de tau, pyRing, catálogo sem duplicação, versão do fit de remanescente, hipóteses 220+440.',
      'C5: injeção/recuperação N>=50 por célula, viés/cobertura e duas famílias; Fisher com massa/spin livres requer informação adicional.',
      'C6: registro próprio antes de ler strain na janela; PSD fora da fonte; execução registrada e comparação de tempos.',
      'C7: pacote independente em inglês, manifesto e reprodução final, apenas após completar a matriz de evidências.'
    ]
    failures=[
      'WSL sem elevação retornou E_ACCESSDENIED; acesso científico somente leitura foi autorizado e funcionou.',
      'Rede sandbox retornou WinError10051; download público autorizado concluiu e checksum confere.',
      'qnm sem numba falhou; dependências instaladas somente em cache/vendor, /opt preservado.',
      'Quadratura inicial atingiu limite de subdivisões; resolução aumentada, resultado anterior preservado em backup; novo teste sem aviso.',
      'Controle PSD inicial recusou zero em Nyquist; a convenção foi explicitada, apenas esse endpoint excluído, interiores validados.'
    ]
    status=dict(date_utc=now,goal_status='ACTIVE_NOT_COMPLETE',
      full_objective='Confrontação TGL-ringdown: derivar taxas em M,spin,D; formas de onda; distribuição de evidência O4/O5; posteriores e strain atuais; pacote independente.',
      previous_visible_nonresearch_turn='NO_GOAL_PROGRESS: resposta ao pedido de prompt, seguida de retomada efetiva nesta rodada',
      this_goal_turn='PROGRESS: código, provas condicionais, previsões e confronto inicial em amostras públicas verificados',
      no_blocker_recurrence=True,requirements_remaining=remaining,
      verified=dict(C0_claims=len(c0['claims']),C0_uncovered_lines=c0['coverage']['missing'],
          posterior_draws=c4['N'],R_B_logB_220_with_free_440=b['lnB_joint_spin_curve'],
          R_B_logB_bootstrap95=b['lnB_bootstrap_025_50_975'],
          independent_quadrature_difference=valid['quadrature_minus_residual_KDE_logB'],
          PSD_forecast_scenarios=len(fisher['records']),PSD_controls='PSD_CONTROLS.json',
          exact_QNM_crosscheck='C4_VALIDATION.json',single_220_degeneracy=fisher['mass_spin_free']),
      scoped_results='B_L220/GR220 marginaliza 440 livre em ambos; não é Bayes factor TGL completa/GR completa; template de ensemble é hipótese física adicional.',
      active_processes=[],archives=dict(GW250114='download/listagem/extração/pinos concluídos',GWTC5='metadados conferidos; tarballs ainda não baixados'),
      preserved_failures=failures,hashes=hashes,
      next_action='Completar C1 e análise de todas as leituras; reutilizar C4 atual, estender para controles de modelos e catálogo, sem refazer V346.',
      source_versions='v369 local congelada em cache/casa; nenhuma edição/compilação do programa canônico nesta rodada')
    atomic_json(ROOT/'STATUS_ORDEM_013.json',status)
    text=f'''\n[REAL — progresso parcial, objetivo integral ativo]\n\n## Rodada {now}\n\nA auditoria cobre {len(c0['claims'])} itens e todas as {len(c0['coverage']['required_nonempty_lines'])} linhas não vazias exigidas. O módulo recupera os dois ramos V346; a derivação GKSL diferencia taxa de salto, coerência, amplitude e potência. Os modos exatos qnm concordam com Leaver, e quatro curvas PSD foram usadas no forecast, com controles PyCBC/LAL em arquivo separado. O C5_FISHER conserva o retrato anterior em sua lista not_done; os controles foram pagos depois dele e estão em PSD_CONTROLS.json.\n\nNo primeiro confronto público ({c4['N']} amostras), ramo B: ln B={b['lnB_joint_spin_curve']:.9f}, bootstrap 95% de ln B={b['lnB_bootstrap_025_50_975']}. Desvio previsto mediano em tau={b['shift_quantiles_05_50_95'][1]:.9f}; correção/erro marginal={b['correction_over_marginal_sigma']:.6f}. A quadratura tridimensional independente difere por {valid['quadrature_minus_residual_KDE_logB']:.3g} em ln B. Isso é comparação do 220 mantendo 440 livre, sob hipótese de amortecimento de ensemble; não é confirmação nem decisão sobre a teoria inteira.\n\n**Ainda falta**\n\n'''+''.join('- '+s+'\n' for s in remaining)+'\n**Falhas e correções preservadas**\n\n'+''.join('- '+s+'\n' for s in failures)+'''\nMemória de retomada: STATUS_ORDEM_013.json contém os caminhos, hashes lidos, estados e próxima ação. Nenhum processo permanece rodando nesta gravação; arquivos de resultados não são prova de processo vivo. Nenhum strain da janela do evento foi lido.\n'''
    append_atomically(ROOT/'PROGRESSO.md',text)
    target=ROOT.parent/'TUNEL/DO_CHATGPT/ENTREGA_013_PARCIAL_220_E_FORECAST_20260921.md'
    if target.exists():raise FileExistsError('Receipt already exists; use a dated amendment')
    header='[REAL — entrega parcial; não encerra M1, M2 ou a ORDEM 013]\n\n'
    table='\n## Artefatos verificados\n\n'+''.join(f'- `{ROOT/p}` — SHA256 `{h}`\n' for p,h in hashes.items())
    append_atomically(target,header+text+table+'\nPAGO/NÃO PAGO: os testes explicitados acima estão pagos no escopo indicado; cada item da lista de pendências permanece NÃO PAGO. Kernel/axiom report: NÃO APLICÁVEL, sem alterações Lean.\n')
    print(json.dumps(dict(status=str(ROOT/'STATUS_ORDEM_013.json'),handoff=str(target),goal_complete=False)),flush=True)

if __name__=='__main__':main()
