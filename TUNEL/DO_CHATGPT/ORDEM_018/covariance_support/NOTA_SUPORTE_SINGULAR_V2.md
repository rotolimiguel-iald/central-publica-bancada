# Suporte singular — revisão V2

[REAL computacional sintético] A revisão independente encontrou dois P2 no protótipo01: tolerâncias não finitas podiam desativar a rejeição de suporte; formas incorretas podiam produzir broadcasting. Original, protocolo,18 controles e manifesto continuam byte a byte. A correção está em singular_gaussian_v2.py.

V2 valida tolerâncias escalares finitas não negativas, recusa limiares derivados não finitos e confere exatamente dimensões/finitude de y,mu,C,A,m,S antes da álgebra. Passaram37 controles do autor e16 verificações independentes do delta. A tentativa no sandbox parou no import por ausência de NumPy; o processo normal autorizado concluiu com o NumPy existente, sem instalação.

Normalização, suporte, prior gaussiano, sinal/Jacobiano do exemplo Cefeida e ausência de JAGB no baseline conferem no parecer. Isso qualifica somente o protótipo sintético e as transformações explícitas. Limiares/unidades da C real não estão qualificados; densidades de suportes diferentes exigem medida comum. Nenhum fit, dado real, evidência F9 ou ratificação de V1. Mapa416; parecer: ../proveniencia/REVISAO_SUPORTE_H0DN.md.
