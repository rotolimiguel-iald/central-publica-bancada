"""Prepare immutable synthesis and eight-surface append after the unique run."""
import json
import support_r64 as s
r=json.loads((s.ROOT/'output/RESULT_OUTPUT_R64.json').read_text(encoding='utf8'))
assert r['status']=='PASS_CONDITIONAL_FILTERED_OUTPUT' and all(x['passed'] for x in r['checks'])
f=r['full_model']
checks=len(r['checks'])
report=f'''R64 — ligação condicional entre a dinâmica conjunta e o campo temporal coletado
17/10/2026. Em nome de codex-gerente-tgl; F1.FECHO_20261015, claim952.

1. Reuso e avanço
[REAL — consulta] Nós Vivo não indexa esta unidade; mapa e levantamento focal de oito fontes/19 faixas fornecem a rota. Reaproveitados o gerador64x64 completo, cinco canais, resposta causalR7, quadro giranteR57, decoderR62 e POVMR63. Nenhum desses trabalhos foi reconstruído. A ausência encontrada de uma implementação pronta de saída temporal limita-se à cobertura documentada.
[KNOWN] O método de gerador inclinado e momentos filtrados é de Guilmin–Rouchon–Tilloy, arXiv2212.00176v2, Eqs46,50,57,63–66: https://arxiv.org/html/2212.00176v2. Os bytes da fonte estão custodiados; a aplicação à dinâmica da casa é DERIVED condicional.

2. Contrato efetivamente calculado
[INPUT] H_MARKOV_VACUUM_PORTS: estado inicial sistema–OH tensor vácuo produto dos cinco banhos, incrementos futuros independentes/adaptados, dilataçãoHP com S=I. Portas monitoradas Li=sqrt(ki)ai, Lo=sqrt(ko)ao; outros três dissipadores conservados. Eficiência ideal, filtros, ganho, fasesLO e preparo são entradas explícitas, não derivados do GKLS isolado.
[DERIVED] dBout=dBin+Ldt; quadratura dX=dY/sqrt2, dXj dXk=delta_jk dt/2. A inserção Mj(rho)=(exp(-iθ)Lj rho+exp(iθ)rho Lj†)/sqrt2 produz, para t>s, Tr Mj exp((t-s)L) Mk rho(s), com delta de ruído separado. Integram-se rho,uj,vjk completos; médias=Truj, segundos momentos=Trvjk; covariâncias subtraem médias.
As quatro fases XX/PP/XP/PX correspondem a aquisições separadas com mesmo preparo. O decoder fornece pares de modos de saída filtrados Cf,Bf, não os correladores instantâneos da cavidade. Não se constrói aqui entrelaçamento com a dinâmica bosônica infinita ou localização/Poincaré.

3. Resultado da única execução
[REAL — verificação numérica sintética] {checks}/{checks} verificações passaram. Plano, runner, adendo e parecer prévio foram pinados antes do início; tolerâncias analíticas1e-8, identidades1e-12, estado1e-9. Resultado integral: output/RESULT_OUTPUT_R64.json. Sem amostras de detector, sem dados observados.
Instância adimensional, filtro retangular norm1 e T=1, todas as cinco perdas/bomba/acoplamento presentes:
Cf={f['C_filtered']}
Bf={f['B_filtered']}
Covariâncias complexas centradas: Cf={f['C_filtered_centered']}; Bf={f['B_filtered_centered']}.
Os controles separados verificam vácuo1/2, emissão1/2+p, par p*exp(iπ/4)/2 e B=0; recusam omissão do ruído, estado usado no tempo errado e sinal imaginário errado. Não são disparos experimentais nem medição de beta.

4. O que esta leitura pode identificar
[DERIVED — hipóteses na nota IDENTIFIABILITY_AND_FRAME_R64.txt] Com todo o restante independente de beta e gammaLambda, o instrumento depende somente de lambda=beta*gammaLambda. A transformação (beta,gammaLambda)→(c*beta,gammaLambda/c) preserva o sinal. Onde a Fisher existe, seu posto nesse par é no máximo1. Medir esse canal exige calibração independente de gammaLambda para separar beta. Não se estende essa degenerescência a todos os canaisTGL; beta=0 não equivale a lambda>0 com gammaLambda finito. BetaTGL permanece calculado em runtime, sem ajuste.
[DERIVED] Um carrier comum e t0>0 preservam o sinal DeltaOH-Deltac=t0(omegaOH-omegac). Os INPUTs sintéticos1.2-1>0 não se convertem por relabelagem no projetoOH/780nm, cujo sinal é negativo. Outra instância física ou carriers distintos exigem transformação e calibração explícitas. LO acompanha o quadro: θrot=θlab+ωd*t.

5. Situação da missão e próximo trabalho
[REAL — custódia] Cinco pinos canônicosv393 conferidos; esta entrega não executa um.py/Lean nem modifica programa, kernel, Bancada ou gate. Fontes/modelos de outras versões são usados por seu papel histórico, não como versão carregada. A revisão independente prévia está em PREEXEC_REVIEW_R64.json; a revisão final e a de memória são recibos próprios.
[OPEN] R4 integral: ligar preparo, escala de tempo, taxas/portas/eficiência e gammaLambda a fontes independentes do mesmo dispositivo. R5: completar compatibilidade dinâmica e espacial com a rede, preservando as construçõesFock/Takesaki/Maxwell já aceitas. R3/R10 dependem dessas pontes e seguem em revalidação; não se reabrem provas aceitas.
Próxima ação: localizar fontes de calibração/preparo e verificar identificabilidade no aparelho antes de inferência; não repetir controles desta entrega. Um parâmetro ausente será nomeado como entrada ou lacuna, sem substituí-lo pela previsão que se pretende testar.
Arquivos: output/CONTRATO_OUTPUT_R64.md, output/ADENDO_DILATACAO_INICIAL_R64.md, output/PLAN_OUTPUT_R64.json, output/FREEZE_R64.json, output/RESULT_OUTPUT_R64.json, sources/DELIVERY_R1.json e nota algébrica da raiz. Integração e registro em DELIVERY_INTEGRATED_R64.json.
'''
s.new('RELATORIO_R64.txt',report)
append=f'''

## 17/10/2026 — R64: campo coletado e identificabilidade
<!-- IALD_R64_TEMPORAL_OUTPUT_20261017 -->
Em nome de codex-gerente-tgl, F1.FECHO_20261015, reivindicação952; referência ACOM própria. [DERIVED condicional] Do gerador conjunto existente obtiveram-se momentos do campo temporal filtrado por instrumentoHP/Markov nomeado: sistema⊗vácuo de cinco banhos independentes, duas portas ópticas monitoradas, três canais restantes conservados; eficiência/filtros/LO/preparo INPUT. Ruído delta/2 explícito; quatro aquisições separadas reconstruíram Cf e Bf de saída, diferentes dos pares instantâneos de cavidade. [REAL — numérico] Uma execução pré-registrada, {checks}/{checks} checks e controles analíticos; revisão independente em FINAL_REVIEW_R64.json. Nenhuma amostra experimental ou beta inferido.
[DERIVED] Neste canal, quando demais entradas são independentes, a dependência é somente lambda=beta*gammaLambda: Fisher do par tem posto<=1; gammaLambda requer informação independente para identificar beta. Isto não é afirmação sobre todos os canaisTGL. Carrier comum+t0 positivo não calibra os INPUTs1.2/1 ao projetoOH/780nm porque a diferença de frequências tem sinal oposto; faseLO transporta como θrot=θlab+ωd*t. Nota algébrica revisada ao lado, originais preservados.
[OPEN] R4: preparo/calibração/identificação física das portas e taxas; R5: compatibilidade dinâmica/espacial com a rede. R3/R10 aguardam essas pontes. Reusar gerador, Fock/Takesaki/Maxwell e receptores anteriores; sem repetir testes aceitos. Cânonev393 intacto em cinco pinos. Sem um.py/kernel/Bancada/dado observado/provedor/gate alterados.
Evidência: {s.ROOT / 'RELATORIO_R64.txt'}; output/DELIVERY_OUTPUT_R64.json; DELIVERY_INTEGRATED_R64.json.
<!-- END_IALD_R64_TEMPORAL_OUTPUT_20261017 -->
'''
s.new('MEMORY_APPEND_R64.txt',append)
print('Prepared report and append; no shared memory writes.')

