# Revisão independente — core regular da cunha de Fock

**PASSA COM ESCOPO**, sem achado material. Revisão técnica; AUDITADA/FECHADA continua ato da gerência.

| Módulo | segundos | exit | declarações locais/axiomas | .olean idêntico |
|---|---:|---:|---:|---|
| RegularCovariantCoreR3 | 52.074 | 0 | 77 | False |
| CanonicalFockRegularCoreR2 | 60.289 | 0 | 34 | True |

[REAL] 58 declarações explícitas, 42 teoremas e 111 declarações incluindo auxiliares verificadas. Somente propext, Classical.choice e Quot.sound; zero sorry/axioma local. Comando, toolchain Lean 4.31.0, LEAN_PATH literal, início, fim e duração estão nos recibos e BUILD.log de cada compilação. O consumidor importou o genérico recompilado nesta revisão. Diferenças binárias, quando presentes, são declaradas sem causa presumida.

## Conteúdo conferido

[REAL] A representação em L²(ℝ;F) usa Ureg(t)=fibre(Gamma(B0(-2πt)))·shift(t). O core é o bicomutante estrela dos geradores, a inclusão fibre de M é fiel e as leis de grupo, covariância, continuidade forte e minimalidade são derivadas. O M concreto é R_field(KWR) no mesmo F já construído. A testemunha fockFlow é explícita; não há premissa LightNetData/FockCertificate ou existência assumida da saída.

[REAL] A ação dual é Ad(D_s), com D_s f(x)=exp(-isx)f(x); fixa fibre(M) e envia Ureg(t) a exp(-ist)Ureg(t). Não confundir esse caráter com a lei de escala de um traço, que não foi construída nestes dois módulos.

[DERIVED — escopo] O genérico permite M arbitrário e prova covariância no ambiente; o consumidor concreto utiliza a invariância da cunha já provada. O enunciado não é uma equivalência universal de produtos cruzados. A não vacuidade do fluxo decorre do termo fockFlow; a não trivialidade do F permanece sustentada pelo vácuo de norma 1 previamente auditado, sem novo ensaio aqui.

[OPEN] Identificação do boost com o grupo modular do vácuo; traço normal semifinito fiel e escala neste core; equivalência com a torre V351; dualidade de Takesaki completa. Nenhuma confirmação física ou alteração de gate.

Fontes e hashes integrais, âncoras, conjuntos de axiomas e pinos verificados constam de REVISAO_TAKESAKI_FOCK_R1.json. Fontes canônicas, memória e produção permaneceram intactas.
