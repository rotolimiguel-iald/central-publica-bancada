# D10/CMB–BAO: pareceres conferidos e linhagem dos dados

27/09/2026 — coordenação IALD/Codex. Nenhum ajuste cosmológico novo.

## Resultado que muda a preparação

[REAL — comparação de arquivos locais] Os 12 pontos literais do Nível 2 são exatamente as primeiras 12 entradas da tabela de fallback histórica do D9. Eles **não** são as primeiras 12 medições do vetor DR2 atualmente disponível no cache/arquivo de médias. A avaliação antiga deve conservar o rótulo e os dados que realmente usou.

O vetor local DR2 tem 13 medições em **sete** redshifts distintos. A descrição histórica de D9 dizia nove; ela não descreve corretamente este vetor. Entre DR2 local e N2, só sete chaves exatas `(z, tipo)` coincidem; mesmo nessas chaves os valores/erros não coincidem. Nos demais há diferenças de redshift e de observável, incluindo QSO: DV em1,491 no fallback versus DM e DH em1,484 no arquivo DR2. Nenhum desses produtos deve ser somado como evidência independente.

[REAL — verificação numérica local] A covariância que acompanha as 13 médias está instalada:13×13, simétrica, com pivôs positivos de Cholesky; erro máximo da reconstrução LLᵀ=2,78e−17. Tem seis pares fora da diagonal não nulos. A correlação DM–DH em z=1,484 é aproximadamente−0,494; em z=0,510,−0,452. Descartar esses termos é uma aproximação concreta, não ausência de covariância disponível.

O cache rotulado LIVE reproduz as médias e erros derivados da diagonal desse arquivo dentro do arredondamento a cinco casas. O cache atual não demonstra que tenha sido o dado de qualquer execução histórica. O teste de simetria/Cholesky também não autentica a release remota ou substitui validação científica da likelihood. O próximo congelamento deve registrar a release/commit recuperável, bytes locais e ordem das medições.

Recibo: `state/D10_BAO_LINEAGE_AUDIT.json`. Auditor reprodutível: `audit_d10_bao_lineage.py`. Ele interpreta literais por AST, lê os arquivos de dados e faz a álgebra da matriz; não importa/roda os programas originais, não ajusta espectros e não acessa a rede.

## Parecer Kimi: o que permanece e o que foi corrigido

[DERIVED — condicional ao mesmo executor, likelihood e suporte] A varianteS histórica chama CAMB com

    Neff = NEFF_SM + DNDB * beta
    omega_c_eff = (1 + beta) * omega_c + beta * omega_b

e os demais parâmetros usuais. Se o rival LCDM+Neff(+massa de neutrinos) admite esses pontos, inclui essas distribuições observáveis. Logo seu máximo de log-likelihood é pelo menos o da varianteS fixa. Um teste com erro tipoI controlado uniformemente no rival não pode ter potência maior que seu nível nos pontosTGL que também pertencem ao rival. Isso é uma limitação desse contraste/implementação, não refutação da teoria canônica.

Correções ao parecer externo, preservado integralmente na campanha:

- **p não é automaticamente1.** O sinal T≤0 não determina seu p-valor calibrado. A conclusão legítima é sobre inclusão e potência, condicionada ao suporte e à likelihood.
- **S com beta livre não é uma curva1D no plano(Neff,omega_c_eff).** omega_c também é livre. Fixando omega_b, o determinante do mapa `(beta,omega_c)` é `DNDB*(1+beta)`, não nulo no suporte histórico. É um mapa de posto2; chamar o teste de “curva versus plano” congela indevidamente outro parâmetro.
- A fonte usa **NEFF_SM=3,044**, não o3,046 ilustrativo assumido no parecer. A fórmula DNDB da fonte dá9,929606216611285.
- No suporte histórico, o ínfimo de omega_c_eff é0,0746, e não0,07515; para beta negativo, o extremo usa omega_b máximo. O supremo é0,1898. Os intervalos são abertos na fonte; os números são limites da sua aderência.
- Baixa precisão na estimativa de beta não prova isoladamente falha de Wilks. Uma regra de parada sigma(beta)>beta/2 é proposta do modelo, não regra universal adotada.
- **Não retirar um rival por ser difícil ou indistinguível para facilitar5sigma.** Mantê-lo na tabela, com a limitação explicitada. Comparação bayesiana/penalizada responde outra pergunta e exige priors/penalizações declarados.

## Parecer MiMo: recomendações úteis, sem promover hipóteses a fatos

[REAL — código] BAO entra diagonal tanto no D9 histórico quanto em LikeN2. A matriz correta só pode acompanhar o vetor correspondente e sua ordenação; não aplicar a matriz13×13 ao vetor fallback12 por associação de nome.

Correções/limites para a implementação:

- O cenário “12pontos talvez sejamDR1” era conjectura do parecer. A comparação local estabeleceu a igualdade com o fallback; o rótulo de release não deve ser inferido da contagem.
- **Dependência comum de um parâmetro não é duplicação de dados.** AbundânciasBBN e CMB podem fornecer likelihoods condicionalmente independentes dado o mesmo omega_b; omega_b também determinar rd é a ligação física esperada. É preciso auditar a origem das medições/auxiliares e as dependências reais.
- Low-ellTT e lowE são observáveis diferentes; não foi demonstrada “dupla contagem parcial” apenas por ambos dependerem de tau. O caso vedado é reutilizar o próprio lowE simultaneamente com sua compressão em tau como medição independente. Conferir covariâncias/hipóteses de combinação apropriadas.
- Gaussianas de BBN/tau podem representar dados auxiliares legítimos numa likelihood frequentista conjunta. Não remover automaticamente todo termo gaussiano por ser chamado “prior”: separar informação experimental de prior subjetivo, documentar a origem e simular o experimento auxiliar quando aplicável.
- A lista exata de nuisance marginalizados pela versão instalada precisa ser lida; não assumir sem fonte que A_planck foi eliminado. Efeitos de lenteamento nos espectros e likelihood de reconstrução de lenteamento são objetos distintos.
- Não usar erro relativo ΔDl/Dl sem tratamento dos zeros, especialmente TE. Preferir métricas ponderadas pela covariância e estabilidade da likelihood, além dos testes por espectro.
- Exigir z_drag perto de1059,4 não é teste geral de precisão: a cosmologia pode deslocá-lo fisicamente. Confrontar a mesma cosmologia em resoluções/refinamentos diferentes.
- CAMB versus CLASS é controle independente útil quando existe implementação equivalente. Sua ausência isolada não cria um novo bloqueio automático. As tolerâncias numéricas sugeridas pelo MiMo permanecem propostas até validação/congelamento.

## Sequência prática preservada

1. Nomear separadamente o vetor histórico fallback e o vetor DR2 local; conservar resultados antigos como históricos.
2. Vincular a likelihood BAO ao par exato média/covariância e congelar a proveniência.
3. Recuperar e conferir a tradução cosmológica canônica atual. A ausência dela nos excertos dos revisores não demonstra ausência no acervo.
4. Verificar a identificabilidade com os rivais e a precisão do executor antes de grandes cadeias e simulações de cauda.
5. Relatar ajustefixo, betalivre, tensão e poder separadamente conforme o contrato. Nenhum resultado novo5sigma foi produzido.

Os dois pareceres externos foram concluídos uma vez cada e seguem[DECLARADO] até as verificações especificadas. Esta revisão não executa o congelamento final, não é a Ordem18 do Opus e não altera qualquer gate.
