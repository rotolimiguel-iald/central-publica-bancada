# Errata ao lado — R-G: convenção explícita de f_phi
[DERIVED condicional / OPEN na ponte física] 06/10/2026 UTC. Autor: chatgpt-codex/ordem-018/derivacoes. Responde ao achado F2-REV-01 da revisão adversarial, registrado no mapa seq391, e corrige a ambiguidade da rota seq379. O texto anterior da NOTA_DERIVACOES_F2.md é preservado integralmente como história.

## Convenção adotada e derivação
Para o mesmo par ordenado de imagens, diferenças de potencial não nulas e o mesmo redshift da lente, fixam-se:
- F_D = f_l f_s/f_ls, com D_Delta_t,phys = F_D D_Delta_t,bg.
- Delta_t_phys = D_Delta_t,phys Delta_phi_true/c.
- f_t = Delta_t_obs/Delta_t_phys, logo Delta_t_obs = f_t D_Delta_t,phys Delta_phi_true/c.
- **f_phi = Delta_phi_fit/Delta_phi_true**: potencial reconstruído dividido pelo verdadeiro.
- O ajuste usa Delta_t_obs = D_Delta_t,fit Delta_phi_fit/c.

Igualando as duas expressões do atraso observado:
D_Delta_t,fit Delta_phi_fit = f_t D_Delta_t,phys Delta_phi_true.
Portanto, na convenção agora explícita:
**D_Delta_t,fit/D_Delta_t,bg = f_t F_D/f_phi = f_t f_l f_s/(f_phi f_ls).**
Mantendo fixos os demais parâmetros da geometria de referência, D_Delta_t,bg é proporcional a H0_bg^(-1), e a leitura correspondente é:
**H0_fit/H0_bg = f_phi/(f_t F_D) = f_phi f_ls/(f_t f_l f_s).**

Estas expressões qualificam as linhas74–76 e o resumo R-G na linha132 da versão originalmente revisada. Não há mais um f_phi sem direção definida.

## Reconciliação da expressão histórica
O produto escrito anteriormente, D_fit/D_bg = f_t f_phi F_D, só corresponde à convenção inversa. Se desejado, denote-a agora por g_phi = Delta_phi_true/Delta_phi_fit = 1/f_phi; então D_fit/D_bg = f_t g_phi F_D e H_fit/H_bg = (f_t g_phi F_D)^(-1). Os símbolos f_phi e g_phi não podem ser intercambiados sem a inversão. Isso preserva a expressão histórica com seu alcance explicitado, em vez de apagá-la.

Como controle algébrico de direção: com f_t=F_D=1 e Delta_phi_fit=2 Delta_phi_true, a equação de ajuste exige D_fit=D_phys/2 e H_fit=2H_bg. Não se trata de cálculo observacional ou escolha de modelo pelo dado.

## Impacto delimitado
Os casos anteriores com f_phi=1 mantêm exatamente as relações e números já escritos. Os proxies de endpoint de F2_CALCULOS_CONDICIONAIS.json não variam esse fator e permanecem byte a byte intactos, assim como f2_analysis.py. A presente errata não recalcula integrais, dados, poder, lentes ou covariâncias e não altera o forecast poder_forma.

K(z) sozinho ainda não determina F_D, f_t nem Delta_phi_fit/Delta_phi_true. A ponte física de lentes permanece [OPEN]. A correção de convenção é [DERIVED condicional]; não é aprovação de um mapa físico, veredito ou alteração de gate.

## Rastreabilidade
Revisão lida: ../proveniencia/REVISAO_ADVERSARIAL_F2.md e REVISAO_ADVERSARIAL_F2_FONTES.json. Seus hashes foram recalculados dos bytes nesta correção. Não foram alterados os documentos da revisora.
Antes de cada alteração de documento/recibo existente, fez-se backup imediato de bytes na mesma pasta; gravação temporária, verificação e substituição. O prefixo integral da nota anterior foi conferido contra a cópia e a identidade indicada pela revisão. MANIFESTO_F2.json registra os novos hashes; o recibo do mapa recebe a errata sem apagar a inscrição anterior.
