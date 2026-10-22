[REAL — recuperação de fontes e recibos; não anúncio de uma nova identificação física]

# Horizonte existente — correção da recuperação de contexto

UTC 2026-09-24T15:08:59.972974+00:00. ABERTURA sha256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`.
Ordem posterior do operador: “sim, já está derivada no um.py. relembre que vc tem uma pasta
de bancada gigante onde vc já derivou muita coisa também”. A consulta foi ampliada para
as rotas da bancada apontadas pelo índice existente, sem executar um.py nem alterar fontes.

**Correção da frase da bancada:** não pedir novamente uma escolha genérica de horizonte.
O um.py já incorpora PhysicalHorizonChange(U) := ∃χ, U=boost χ; os lemas preservam η e a
cunha. A escolha do canal geométrico nessa realização está registrada pelo autor.

| Fornecedor recuperado | O que já entrega | Comparação específica a manter |
|---|---|---|
| ThePhysicalHorizon | boost da cunha, grupo, preservação da métrica e da cunha | Matriz 2×2; identificação BW contínua explicitamente importada nessa fonte. |
| qgStrongCertificate_frame | frame suave não constante; coframe/métrica lorentziana | ContratoH2 pede também arrasto por boost e fiducial modular. O contrato contém controles para o frame diagonal legado. |
| theHorizon e the_master_fires | instância de equilíbrio e coeficiente térmico | A fonte especifica κ=G=δA=1; isso não é o mesmo dado que N externo no contrato v3.1. |
| modularHorizon | fluxo efetivo da torre, normalização do fator e preservação de ω | TowerHorizon e a representação geométrica sobre região não são tipos intercambiáveis por nome. |
| ConexoesExistentes.lean, 19/09 | três adaptadores e recibo rc0/trio para Lorentz e horizonte | Reaproveitar; não criar novos adaptadores idênticos. |

Não inferir lacuna de uma flag falsa: evaluate_v350_kernel_frontier contém uma lista literal
de remaining. A leitura dessa lista não verifica se a bancada posterior já fornece o argumento.
Também não inferir equivalência de contratos só por Lorentz, H2 ou horizonte no nome.
O próximo trabalho é fornecedor → tipo/hipóteses → consumidor → evidência, seguindo a PORTA
da consolidação, inclusive preparação/Einstein/colagem onde pertinente.

**Estado do trabalho novo já executado antes desta correção:** WedgeDraggedFrame_v6.lean,
7 declarações auditadas no trio, rc0. E(x) tem bloco [[x¹,x⁰],[x⁰,x¹]], determinante
(x¹)²−(x⁰)²>0 na cunha, suavidade, arrasto pelo boost e fiducial proporcional ao Killing.
Não é apresentado como primeira construção lorentziana do acervo. O alvo foi o campo
adicional de arrasto do contrato, não refazer Lorentz. Se um fornecedor equivalente for
localizado na bancada, este artefato vira redundância documentada, sem implantação.
WedgeKillingNormalization e suas variantes são rascunhos ainda NÃO compilados; nenhum
H2 completo foi declarado. A-3.d permanece em curso, não PAGO integral.

Seis tentativas do frame, todas preservadas: 218.925249s parede, 217.281250s CPU.
Gasto externo conhecido agregado por request_id: US$0.159306135; custos não informados não
contados como zero. Nenhuma chamada externa nova nesta recuperação. Nenhuma alteração
de um.py, kernel, Atlas ou gate. Manifesto de hashes/linhas: A3/existing_horizon_recovery.json.
