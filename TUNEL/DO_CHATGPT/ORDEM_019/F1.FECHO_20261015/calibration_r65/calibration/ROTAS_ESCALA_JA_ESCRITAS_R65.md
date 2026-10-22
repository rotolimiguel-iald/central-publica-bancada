# R65 — rotas de escala existentes e seus elos condicionais

Em nome de codex-device-clock-r57. Complemento aditivo do contrato, sem execução.

**[REAL documental]** Há duas rotas de escala já escritas; não se deve resumir o resíduo como ausência total de fórmula.

1. **Rota térmica.** A patente v2:321–325 escreve uma taxa mínima proporcional a `alphaii k_B T/hbar`; a mesma fonte:351–354 escreve `alphaii gamma_Lambda D[J]`. O texto histórico identifica sua notação com beta em304–307; a macro histórica não é interpretada como o quadrado do alpha CODATA moderno. Reutiliza-se `../THERMAL_ROUTE_SCOPE_R65.txt`, pinado nesta entrega. Para obter `Gamma=k_B T/hbar`, é necessário demonstrar que a taxa relevante é o coeficiente do **mesmo** `D[J0]`, com a mesma normalização, e que o regime operacional satura o mínimo. Se só houver uma desigualdade para essa taxa, o resultado é um limite, não uma igualdade de calibração. A sonda analítica da raiz mostra que a existência de estacionário fiel de entropia finita, isoladamente, não fixa uma taxa positiva universal. Ela não exclui hipóteses físicas adicionais que a fonte venha a fornecer.

2. **Rota planckiana.** O contrato R7:92–107 já resolve o submodelo com H e perdas convencionais retirados: a média até a ocupação absorvente é `2/(beta gamma_Lambda)`. Igualá-la à duração `t_P/beta` declarada na patente:442–444 produziria `gamma_Lambda=2/t_P`. A álgebra está escrita, mas requer identificar os dois tempos e o mesmo canal. Essa média não era tempo de clique APD, atraso de grupo nem média do GKLS completo com bombeamento, acoplamento e perdas. Portanto não se transporta essa calibração ao R64 sem justificar a redução e o observável. Não se voltou a calcular nem se desligou termo do modelo completo nesta entrega.

**[OPEN localizado]** As fórmulas existentes orientam a árvore A do contrato. Falta a passagem demonstrada ao Gamma do instrumento R64 — ou uma leitura independente dele. O relatório de fontes da raiz complementa a cobertura de Custo/um.py; esta nota não afirma ter relido essas fontes além do R7 e da patente pinados aqui.

**[DERIVED candidato]** Se uma dessas pontes vier demonstrada com normalização e condições físicas fixas, ela pode fornecer c_ref e remover a degenerescência de escala descrita no contrato. Esse caráter condicional não apaga a matemática já existente, tampouco substitui a ponte pelo nome da taxa.
