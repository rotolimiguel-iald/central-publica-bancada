# F5.1 — contrato para BBN com expansão TGL

07/10/2026 · [REAL] Consulta `NOS_VIVO\consultar.py --unidade F5.1`, leitura do `ORDEM_018_ADENDO_001_era_da_radiacao.md` e do `BBN_METADATA.json` da ORDEM 018. O arquivo local CAMB fornece somente eixos/tabela padrão; seu estado é `axes_only_not_BBN_prediction`. Não é uma previsão BBN TGL.

## Código e versão propostos

[KNOWN, fonte primária consultada em 07/10] Candidato: [PRIMAT Python 0.3.3, repositório do autor](https://github.com/CyrilPitrou/primat/blob/master/README.md). A documentação apresenta `run_bbn`, backend C e alternativa Python; redes `small` (12 reações nucleares + n↔p), `small_parthenope` (mesma rede com taxas PArthENoPE 3.0) e `large` (428 + n↔p). **Na instalação pelo operador:** fixar artefato exato por SHA-256 e commit/tag efetivo, registrar `primat --version`, backend e dependências. A versão do README é candidata, não uma instalação medida nesta máquina.

## Equação a inserir

[DERIVED da lei de fundo da casa] Calcular `beta = ALPHA_FINE_CODATA_2018 * sqrt(e)` em runtime e aplicar ao fundo de radiação `S(T)=sqrt(1+4*beta/3)` no histórico de expansão usado pelas ODEs de BBN. O fator é constante na era considerada; a tradução para `DeltaNeff` **muda antes/depois da aniquilação e±**. A tabela CAMB em `DeltaN` serve apenas como bracket declarado, sem substituir a integração com `S(T)`. Não alimentar simultaneamente o código com `S(T)` e um `DeltaNeff` equivalente, pois duplicaria a correção.

## Taxas, parâmetros e controles

| Item | Contrato antes de rodar |
|---|---|
| Taxas fracas n↔p | Manter correções padrão da versão pinada e registrar tempo de vida do nêutron, normalização e fingerprint dos caches. |
| Rede nuclear | Primária `small`; sensibilidade `small_parthenope`; `large` só para verificar truncamento, conforme custo medido no piloto. Arquivar os arquivos/tabelas de taxa e hashes após instalar. |
| Densidade bariônica | Prior `ω_b` do CMB definido antes de ver D/H. Não ajustar `ω_b` ao próprio D/H que entra no veredito. |
| Saídas | `Y_p`, D/H, evolução térmica, parâmetros, taxas, backend, tolerâncias e logs; comparação com baseline `S=1` no mesmo pin. |
| Incerteza | Variação nuclear e `τ_n` por amostras pareadas, usando o mesmo conjunto de sementes nos braços baseline/TGL; covariância entre `Y_p` e D/H. A [documentação do autor](https://github.com/CyrilPitrou/primat/blob/master/README.md) descreve `run_mc()` e parâmetros `p_<reaction>`. |
| Validação | Reproduzir primeiro referências da versão pinada com a tolerância oficial; comparar backend C/Python; depois alterar somente a rotina de expansão. Registrar diferença numérica e orçamento de erro. |

## Custo e gate

[ESTIMATIVA] Software local sem preço de API identificado na documentação consultada; o custo computacional depende do backend, das correções térmicas e do número de amostras. A documentação do autor relata backend C mais rápido que Python e uma suíte integral de testes da ordem de 20 minutos; isso **não mede** esta máquina nem o patch de `S(T)`. Planejar um piloto local de 2 baselines + 2 execuções TGL e 10 amostras pareadas, medir segundos/execução, pico de RAM e arquivos; só depois dimensionar o MC final. Não há aqui autorização para instalar nem execução BBN.

[INPUT/OPEN] A ORDEM 019 atribui a **instalação ao operador**. Entregamos código candidato, versão, política de taxas, critérios de validação e custo a medir. O quadro deve mostrar F5.1 em `AGUARDA_OPERADOR` para o pin/instalação, com a preparação concluída. Nenhum resultado observacional ou veredito da natureza é declarado.
