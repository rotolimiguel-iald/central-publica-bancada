[REAL — controles numéricos passaram; OPEN — precisão integral e calibração]

# ORDEM 013 — Refinamento iniciado e API contínua verificada

Registro: 2026-09-22T09:47:39.740096+00:00. N/A — sem alteração do cânone, Lean, Atlas ou C6.

**Controle de resolução Phenom:**57200 terminou código0;347 pontos dominantes,
8192→16384Hz. Maior |ΔlogL|=0.0136696520976<0.1.
O controle SEOB196 pontos já havia passado. São controles pontuais, não limites
globais de erro do posterior nem provas de precisão da integração de fonte.

**Nova rodada começou:**34860,quatro trabalhadores;32768 propostas,seed130972,
`phase_real_refined/IMRPhenomXPHM_seed130972_N32768`. Mesmos priors e likelihood;
a proposta numérica foi ajustada e registrada na etapa anterior. O instantâneo
de36 blocos conferiu576 vetores completos
e seus controles guardados atomicamente dentro dos NPZ. Não reiniciar o processo.
A repetição SEOB16384/seed130942 continua no handle40860,quatro trabalhadores.

**API contínua:** a função de integração de fase já existente recebeu somente
o leitor real de Nyquist, em cópia separada. Foram examinados os pontos reais
Phenom15627(o que havia interrompido a rodada) e SEOB1002(dominante no piloto),
com intensidades[-2,0,0.37,1,4],três fases fora da grade e O4/O5.
São60 controles diretos: máximo erro relativo
1.24055410548e-07; máximo erro logL
1.17639992538e-05. Os extremos a=0/1 concordaram
exatamente nas duas famílias. Intensidade negativa é extensão diagnóstica,
não afirmação de dinâmica GKLS física. Nenhum prior sobre a foi escolhido.

**O que continua faltando:** as curvas de fonte marginalizadas Z(a), além dos
dois extremos, e a calibração por injeções. Esta validação de API não entrega
viés/cobertura. Reutilizar os leitores de intervalos existentes quando houver
curvas completas; dois pontos não determinam um máximo ou um intervalo.
Intervalo truncado pelo domínio, curva sem identificação ou integração sem
precisão devem permanecer falhas visíveis, sem fabricar erro/sigma.

**Sequência:** revalidar34860 e40860. Quando terminarem, auditar densidades e
somas, conferir controles completos e comparar com as rodadas anteriores.
O controle de resolução da nova proposta deve abranger seus próprios pontos
dominantes; não herda automaticamente a aprovação dos pontos antigos.
`combine_continuation_families.py run` mantém os caminhos já registrados
(Phenom16384 + SEOB16384); não trocar pelo novo32768 sem registro separado.
A rodada Phenom16384 segue512/1200 em precisão local e120 diferençaslnB>0.2.
Não anunciar nova significância física. Restam convergência e viés/cobertura
da intensidade contínua no escopo completo.
