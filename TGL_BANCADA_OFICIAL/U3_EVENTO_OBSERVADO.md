# Evento observado e modelo — U3 inicial

A bancada agora liga as amostras de GW250114_082203 aos picos de H1/L1 do registro C6. O adaptador lê os arrays residentes e reutiliza as cópias verificadas de tgl_ringdown_prediction.py e tgl_ringdown_template.py.

## Como pesquisar no painel

1. Carregue o domínio de ondas gravitacionais. Abra GW250114 na navegação superior.
2. Escolha explicitamente uma leitura de relógio. R-A/R-B e outras leituras preservam as hipóteses do executor.
3. Escolha uma das cinco janelas registradas; varie massa da fonte, spin e redshift. A janela dos dados continua referida à massa de referência do registro, independentemente desses controles.
4. Ajuste as amplitudes e fases efetivas de H1 e L1. Elas são definidas no primeiro instante da janela, não no pico. As curvas compartilham as unidades de strain do dado.
5. Compare dados, GR, TGL e resíduos. O controle R-GLOBAL reproduz GR no executor atual.

## O que está conectado

- Dois arquivos HDF5 originais, identificados pelo manifesto C6 e SHA-256, dentro do domínio integral GWOSC.
- Cinco janelas: 6, 8, 10, 10,5 e 12 tM de referência, com 410 amostras a 2048 Hz. O passo 2 sem filtro anterior ao início segue o registro C6.
- Tempo GPS de cada detector, convertido para segundos relativos a seu pico, preservando a diferença H1/L1. Não existe um GPS geocêntrico inventado.
- DQ e máscaras de injeção verificadas no intervalo original inteiro, pelos nomes dos bits e pelo tempo próprio das máscaras. CW não foi acrescentada como veto não registrado.
- PSD de treino off-source e operador de ruído 407×410; input strain×1e21. A matriz inclui quociente por polinômios de grau 2. Suas 407 coordenadas não são um novo eixo temporal.
- Normas quadráticas dos resíduos com parâmetros fixados manualmente. São diagnósticos exploratórios, sem conversão para p, sigma ou evidência Bayesiana.
- Recusa de fontes/hash incompatíveis, intervalos inválidos e qualidade reprovada. Um domínio PARTIAL pode fornecer o evento se seu par registrado estiver íntegro; a carga parcial permanece visível.

## Alcance científico

[REAL] O painel calcula uma sobreposição exploratória do modo 220 efetivo em cada detector. Os coeficientes de amplitude/fase são independentes e manuais. Não executa ajuste automático, marginalização de calibração instrumental, posterior conjunto ou reconstrução de antena. O executor 220 usa o ajuste BCW que já existia na bancada; não deve ser apresentado como a inferência Kerr exata 220+440 de C6.

[DECLARADO na fonte, integridade conferida] C6_RESULTS.json mantém INCONCLUSIVE_SYSTEMATICS por falha do critério de calibração com duas famílias IMR. C7 é consultado como adendo, sem promover o resultado anterior. Uma interface nova não altera esse estatuto, o kernel ou o gate formal.

[OPEN] U3 completa ainda requer ligar a geometria de antena e os posteriores com suas hipóteses e incertezas; U4 ligará as inferências existentes e seus controles. Demais eventos e domínios precisam de perfis próprios. Este painel não transforma todos os 180 arquivos em eventos distintos.

## Orquestração paralela ORDEM 18

Pedido atual do operador: Kimi/MiMo/DeepSeek discutem sensibilidade dos dados instalados; ChatGPT/Física sintetiza; Claude Opus desenha o teste e redige ORDEM 18; a bancada executa após conferir o protocolo. Estado vivo e recibos pertencem à fila única:

`C:/IALD/Central de Patentes/Chatgpt/IALD_ORQUESTRACAO_20260923/ORDEM_018_TESTE_SENSIBILIDADE/campaign.json`

O programa integral v375 tem 32,6 MB. Cada consulta externa declara seus trechos e hashes; recuperação parcial não é carregamento integral. A busca de um teste com potência para distinguir TGL/GR é separada de significância já observada; nenhuma dessas etapas garante 5 sigma.

## Vista normalizada pelo ruído

A deriva do dado bruto é muito maior que a amplitude manual inicial do modelo. O painel conserva a vista bruta e oferece uma transformação visual comum aos dados e aos modelos: se W é o operador registrado 407×410, usa B = sqrt(WᵀW), calculado pelo fator polar direito da SVD. Para todo resíduo x, ||Bx||² = ||Wx||²; o runtime verifica essa igualdade numericamente e recusa a resposta se falhar. A multiplicação por 1e21 segue o escalonamento do cache de ruído.

A saída tem 410 coordenadas transformadas adimensionais, posto no máximo 407. Cada coordenada mistura amostras não localmente e não representa uma nova medição naquele instante. Por isso o eixo mostra índices da amostra de referência, com a grade/GPS original separados. Não se obtém reconstrução de sinal, independência de 410 observações ou significância. O mesmo B é aplicado a dado, GR, TGL e resíduos; nenhuma curva recebe tratamento privilegiado.
