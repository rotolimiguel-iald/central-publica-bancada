[REAL — correção numérica verificada; OPEN — convergência científica]

# ORDEM 013 — Recuperação da interpolação real

Registro: 2026-09-22T09:18:50.829512+00:00. N/A — sem alteração de Lean, um.py, Atlas ou C6.

O processo Phenom62818 terminou com código1. Foram preservados8128 vetores
completos em508 blocos;426 avaliações ainda faltavam. O diagnóstico80765
reproduziu a falha somente no índice15627 entre32 pontos: os outros31 passaram.
Os arquivos da rodada original continuam intactos e sem RESULT.json.

## Causa e correção verificadas

Para dados reais com N par, o coeficiente de Nyquist real deve multiplicar
cos(Nφ/2). O leitor antigo usava a exponencial complexa isolada e recusava
sua parte imaginária, embora devolvesse apenas a parte real. Substituir
essa exponencial pelo cosseno preserva a interpolação real anterior.
O novo leitor verifica dados/coeficientes, simetria conjugada e resíduo
imaginário. Os limites contra a forma de onda completa e a quadratura
permaneceram1e-6 relativo,0.001 em logL e1e-5 na integração de fase.

O primeiro teste da correção falhou por um erro próprio de broadcasting:
comparou matrizes(34,1,9) e(34,9), cruzando fases diferentes. Ele e seu
registro foram preservados. O teste corrigido compara formatos iguais;
erro máximo da integral gaussiana independente=2.13162820728e-14.
Oráculos cardinais N16/N17 e cosseno puro passaram; três entradas adulteradas
foram recusadas. Em dois pontos já aprovados, diferença da integral=0.
No ponto15627: erro relativo de forma de onda
5.76302935514e-08;
erro máximo logL=1.0821500922e-05;
erro de quadratura=4.10052075495e-06.
Os bancos16/32/64 concordaram dentro de0.001. Validador58463 terminou código0.

## Continuação sem apagar o ponto difícil

`phase_ringdown_real_continuation`: cópia byte a byte das16384 propostas e
dos8128 resultados anteriores, mais32 pontos recuperados;394 avaliações
novas. Denominador16384 preservado, inclusive integrandos zero fora do suporte.
As novas avaliações guardam os controles em arquivos junto aos blocos.
**Limitação:** os valores exatos dos controles dos8128 pontos antigos estavam
somente na RAM; não foram recuperados. O caminho original só escrevia um
resultado depois de seus controles passarem, mas isso não recupera seus máximos.

Ativos conferidos nesta sessão:54722(continuação Phenom,2 trabalhadores),
40860(repetição SEOB16384,4 trabalhadores),15254(auditoria SEOB original,
2 trabalhadores,135/196 na consulta). Revalidar os três handles.
O auditor da continuação recusou corretamente a ausência do resultado final.

## Sequência necessária

1. Quando54722 terminar: `audit_registered_transport.py IMRPhenomXPHM_seed130892_N16384 --stage phase_ringdown_real_continuation`;
   `audit_real_phase_continuation.py --rate --processes 2`;
   `compare_phase_runs.py phase_ringdown_regularized/IMRPhenomXPHM_seed130861_N8192 phase_ringdown_real_continuation/IMRPhenomXPHM_seed130892_N16384`.
2. Quando40860 terminar: auditar densidade/taxa e comparar com o piloto SEOB2048.
   Não duplicar o processo enquanto seu handle estiver vivo.
3. A nova combinação já está registrada em `source_family_combination_real_repeat`:
   `combine_continuation_families.py run` espera ambos RESULT e DENSITY_AUDIT.
   Ela utiliza a continuação Phenom e a repetição SEOB16384, com os mesmos pesos
   das famílias e fórmulas verificadas. O registro anterior não foi alterado.
4. Precisão componente a componente, repetição independente e viés/cobertura
   de intensidade contínua ainda são necessários. Nenhum resultado desta
   correção estabelece significância física ou seleciona relógio/partição.
