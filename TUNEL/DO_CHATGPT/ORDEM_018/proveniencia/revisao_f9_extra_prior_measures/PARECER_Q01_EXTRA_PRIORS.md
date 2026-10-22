# Revisão independente — Q01_EXTRA_PRIOR_MEASURES

[REAL documental] ROOT revisou o pacote produzido pela gerente 01a070fc-9484-7e13-a654-c6b5f61093a4. O revisor não escreveu nem alterou o candidato. A entrega oficial responde ao pedido 2f83697e-2a4b-4b15-9397-83ecd29a42a6; a unidade é 4f5a24b4-594d-4c6d-84f6-cd06dc4c6064. O recibo JSON ao lado contém hashes relidos, não transcritos como prova.

Parecer: ACEITO para decisão ROOT de uma execução local delimitada; não é resultado de execução. Foram lidos contrato, referências, cases.py, driver.py e operadores originais df482/f820. O manifesto tem oito membros e quatro backups; foram conferidos os quinze pins de fontes e o executável. Driver e cases passam análise AST sem importação. Nenhum marcador de consumo existia durante esta revisão.

A reconstrução gaussiana escalar é coerente: b=a(m-x0); o máximo restrito original recebe o deslocamento t/a. H3 usa densidade 10 no intervalo de comprimento 0,1. Em H4, delta=-5log10(1+s) implica densidade lambda*exp(-lambda*delta)/0,30, lambda=ln(10)/5, e máximo do integrando em m-lambda/a. A primitiva independente por completar quadrados conserva a normalização. H5 usa q=1/rd e densidade 1/(30q²); a referência integra em rd original por 256 painéis Simpson e 257 avaliações, separada da rotina adaptativa em q.

O limite de quarta derivada da referência H5 foi conferido: g1=a*z/r²; g2=-a/r⁴-2a*z/r³; g3=6a/r⁵+6a*z/r⁴; g4=-36a/r⁶-24a*z/r⁵. A expansão f4/f=g4+4g1*g3+3g2²+6g1²*g2+g1⁴ dá o majorante usado. O resto da média é h⁴*B4/180. A avaliação em float não arredonda para fora; tolerância logarítmica 3e-8 e margem 5e-12 são engenharia, não certificado intervalar.

Os casos F01–F03 cobrem os atalhos de densidade constante, sem demonstrar Jacobianos nessa ramificação. Z01 pressupõe o sinalizador de suporte, não prova geometria matricial. N01 exige erro por identidade de serviço; N02 verifica erro engolido com causa preservada; N03 distingue área zero/underflow de suporte físico nulo. Os controles negativos são serviços falsos declarados, não monkeypatch dos operadores originais.

Tetos coerentes: onze entradas escalares, quatro chamadas reais f820, três serviços negativos e quatro atalhos. No máximo 16393 avaliações de serviço/callback, 4105 leituras da curva e 257 avaliações independentes. Um filho Windows oculto, casos seriais, 30 segundos nominais desde main. O prazo não é tempo real garantido; sem quota rígida de RAM/disco; limite dos streams é de aceite posterior. Executável pinado, fechamento completo DLL/stdlib não pinado.

A marca exclusiva antecede o filho; a marca do filho antecede imports; cada caso tem marca própria. Existência de saída/claim parcial bloqueia repetição. Sucesso requer exit zero externo, terminal PASS, onze resultados e ausência de falhas. O driver valida apenas forma do campo review_reference: ROOT deve conferir o hash real do parecer antes de gravar a decisão. A carga científica compila bytes pinados e registra código/funções; sem NumPy, SciPy, CAMB, WSL, rede ou leitura de observados no código inspecionado.

Não há achado bloqueador para esse recorte. Continuam abertas a construção matricial _Curve.__init__, prepare_joint/evaluate_five/integrate_at_fixed_theta, junção 283x63, transporte C/y/offsets, readmissão I02, guard/filesystem, Q02/Q03 e V1 composto. Este parecer não autoriza abrir observados, executar solver, chamar provedor, reabrir unidades consumidas ou alterar originais/kernel/gate.

A tentativa anterior de persistir este parecer falhou na análise sintática do script de gravação, antes de qualquer instrução; não foi uma execução do candidato. Esta gravação corrige apenas as aspas desse script, sem repetir unidade científica.
