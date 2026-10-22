[DERIVED — álgebra do estimador; REAL — controles numéricos; OPEN — inferência astrofísica]

# Combinação de famílias com incerteza de integração

Esta etapa combina as duas famílias de recuperação da mesma simulação. Não
combina simulações como se fossem eventos. O prior discreto explícito é
`pi(Phenom)=pi(SEOB)=1/2`, igual sob `a=0` e `a=1`, uma escolha estatística
condicional já usada no controle anterior `REGISTRO_C5_IMR_RECOVERY.json`.
Não é uma constante derivada da TGL. O registro desta etapa está em
`source_family_combination/REGISTRATION.json` e precede a leitura dos resultados
finais das duas novas integrações.

Para cada conjunto de dados d, separadamente:

    Z_a(d) = sum_f pi_f Z_fa(d),
    ln B(d) = log Z_1(d) - log Z_0(d).

Fazer a média dos ln B das famílias dá outro objeto. Escolher a família que
favorece cada hipótese também dá outro objeto. A mistura conserva os priors
de fonte existentes, as duas polarizações comuns e os sete parâmetros da
fonte integrados. O centramento da log-verossimilhança é idêntico entre famílias
e hipóteses para cada d; por isso cancela no quociente.

## Erro de Monte Carlo com pareamento

Defina `Zhat_fa = (1/N_f) sum_i L_fa(u_i)/q_f(u_i)` e os pesos normalizados
`p_fai = (L_fa/q_f)/sum_j(L_fa/q_f)`. Propostas fora do suporte têm peso zero e
continuam em N_f. A responsabilidade da família é

    r_fa = pi_f Zhat_fa / sum_g pi_g Zhat_ga.

As hipóteses usam os mesmos pontos dentro de cada família. As famílias usam
sorteios independentes, condicionados às propostas já congeladas. Pelo método
delta aplicado às médias amostrais, a influência de um sorteio é proporcional a

    d_fi = r_f1 p_f1i - r_f0 p_f0i.

Logo a estimativa da variância de ln B é

    sum_f N_f/(N_f-1) sum_i (d_fi - mean_i d_fi)^2.

O centramento é necessário: `sum_i d_fi = r_f1-r_f0`, que em geral não é zero.
Na comparação dentro de uma família isolada, ambas as responsabilidades são 1
e esse termo já se anula. Importar a fórmula desse caso sem a correção adiciona
uma incerteza fictícia à mistura.

## Controles que podem refutar o código

`validate_source_family_mixture.py` compara com integrais constantes, invariância
por centramento comum, cancelamento de covariância com pesos idênticos e um
oráculo de integrais lognormais com médias conhecidas. Foram feitos 4000
experimentos independentes do oráculo, cada um com 512 pontos por família.
Os números medidos ficam em `source_family_mixture_validation/RESULT.json`.
Esse oráculo não contém ondas gravitacionais nem mede poder astrofísico.

Quatro entradas inválidas são recusadas. Um quociente com erro que cancela mas
ESS insuficiente continua reprovado. O consumidor das rodadas reais exige
`RESULT.json` e uma auditoria correspondente da densidade em ambas as famílias;
um arquivo de progresso não basta.

## O que a combinação não resolve

Cada componente continua sujeita a ESS >= 100, peso máximo <= 0,05, repetição
independente e controles de taxa. A aproximação delta perde confiabilidade
quando poucos pesos dominam. A mistura não cura essa falha.

Os 1200 conjuntos simulados reutilizam 50 intervalos de ruído pareados. O
consumidor reporta a distribuição por célula e não multiplica seus fatores de
Bayes. O4/O5 aqui têm SNR40 normalizada separadamente; a comparação não é uma
previsão de detecções a distância fixa. Viés/cobertura da intensidade contínua
e erros de modelo continuam requisitos independentes. Nada nesta combinação
converte ln B em sigma ou seleciona o relógio físico da TGL.

## Execução após as rodadas terminarem

No diretório desta nota, sob o ambiente `/opt/pycbc_env`:

```text
python -B audit_registered_transport.py IMRPhenomXPHM_seed130892_N16384 --stage phase_ringdown_balanced
python -B audit_registered_transport.py SEOBNRv4HM_seed130901_N2048 --stage phase_native_seob
python -B combine_source_families.py run
```

A execução acima só lê rodadas concluídas. Os controles de taxa, a repetição e
a calibração ainda são necessários depois dela. O registro já foi criado: não
executar `register` de novo. Resultados são preservados, nunca sobrescritos.
