[REAL] A-1.b5 — os campos smooth_on e admissible_unit excluem controles explícitos.

Abertura SHA256: 216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a

[DERIVED — Lean isolado] roughFrame preserva arrasto por boosts, determinante não nulo na cunha e coluna fiducial modular, mas seu coeficiente E22=1+|x2| não é diferenciável em x2=0. replaceFrame transforma qualquer H2 em um registro idêntico salvo smooth_on:True, usando esse quadro. Portanto, retirar smooth_on não é mera convenção. Não se afirma ter construído o H2 inicial.

[DERIVED — condicional] admitZero transforma H3 em H3WithoutUnit, substituindo admissible por insert 0 admissible. Exige explicitamente T(0,x)=0 e theta(0,x)=0, além do H3 inicial; não são extraídas gratuitamente do tipo. Todos os demais campos são preservados, inclusive não trivialidade, carga modular e Raychaudhuri. admitZero_not_unit prova que a normalização falha no novo conjunto. Logo admissible_unit tem efeito demonstrado nessa classe.

Não houve edição do contrato da gerência. Os dois registros de mutação foram extraídos de sua fonte e alteram somente o campo-alvo para True. Fonte inicial e falha permanecem. Segunda compilação rc=0; nove declarações auditadas, somente propext/Classical.choice/Quot.sound; sem sorry ou axioma novo. Avisos de tática redundante não alteram o resultado.

Fonte: C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A1\probes\ProbeFieldMutations_v2.lean, SHA256 8d2c8a161813327ce34b563795e3ab904fffa552462adc39c9e95693c977a578
Log: C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A1\probes\field_mutations_02.log, SHA256 115070130ef114392887652fa7e08141da9468e62a5e6365e21c3e5b95ee3f9d
Recibo com comando completo: C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A1\probes\field_mutations_02.json, SHA256 91528c9f067f43884ba6695d6965b852313c7bf86a17886b82f0b05e08eb1318
Auditoria: C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A1\probes\field_mutations_axioms.json, SHA256 bc092b2b7da6090ebdd53f655483c9279b66925a90fef21fce4cb61b5a6abf57

Passe: 27.391000 s parede; 27.046875 s CPU; pico committed 8459452416 bytes. Zero arquivos canônicos posteriores ao marcador. Falha anterior preservada em field_mutations_01. B pesada: 0 h. Não move o gate nem constrói o par físico. Próximo: controle não comutante A-1.b1 e extensão A-1.c.
