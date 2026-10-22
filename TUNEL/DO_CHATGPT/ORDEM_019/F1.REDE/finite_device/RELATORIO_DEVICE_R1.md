# F1.REDE — integração finita do dispositivo
[REAL — teste numérico sintético; parâmetros INPUT] PASSA: 142/142 verificações, EXIT 0; sem dado observado.
Pré-registro anterior à execução: SHA256 6e4e2ce553aea405878e967df9314be2af030b45e234dd35dbe1b30731d2560a; freeze 2026-10-13T21:29:11.469375+00:00; início 2026-10-13T21:29:37.168553+00:00.
Geometria documental: 27 sítios (8 vértices, 12 arestas, 6 faces, 1 centro); 54 conexões por vizinhança cartesiana [INPUT]. Não alocamos o Hilbert de 27 qubits.
Modelo reduzido: Hilbert 2×2×2, H e salto a_out†σ_-+σ_+a_in da fonte TeX, γ_holo=βγ_Λ; β=α_CODATA2018√e em runtime. Taxas e frequências adimensionais INPUT, sem ajuste.
Álgebras dos 3 fatores: 8 regiões; 4913 produtos, 216 inclusões e 729 comutadores disjuntos, resíduos máximos zero.
15 canais exp(tL): mínimo de Choi -2.085e-15, erro TP máximo 1.450e-15; tolerância 1e-10, 29 estados por canal preservados.
Livro de energia aberto: max|Tr(HLρ)−Tr(ρL†H)|=3.474e-17; erro integrado 2.776e-16. Fluxo oposto é contabilidade, não construção microscópica do banho.
Controle PSD: ρ01=1−β literal foi recusado (λ_min=-0.487968699599); C=2|ρ01|=1−β é normalizado e admissível, sem predizer um platô dinâmico.
Reuso explícito: one_mqc.py já resolve desde 29/07 um GKLS qutrit de reset com C normalizado; citado sem rerrodar. A presente integração 2×2×2 usa outro salto, o explícito do Supercondutor.
Raiz aplicada a amplitudes e normalizada: duas decomposições da mesma ρ deram distância 0.178202873547; essa interpretação não é canal linear CPTP. Codificação/decodificação clássica segue válida.
Taxas negativas, NaN, infinito e booleano recusados. Corte 0/1 fóton: [a,a†]=diag(1,−1), não I. O terceiro nível |Ψ⟩ do MQC está fora deste modelo reduzido.
Sem alegação de realização de hardware, transporte instantâneo, fidelidade experimental, 5σ ou rede 4D. Aprovação independente e integração são etapas posteriores.
Fontes, versões NumPy/SciPy, seed, parâmetros, tolerâncias, resultados e comando/início/fim estão pinados nos arquivos vizinhos. Nenhuma produção ou memória alterada.
