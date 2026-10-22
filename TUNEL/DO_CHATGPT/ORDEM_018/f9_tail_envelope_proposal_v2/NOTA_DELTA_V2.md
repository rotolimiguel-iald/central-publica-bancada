# Delta documental V2 — guarda F9 d=0 e limite positivo

[REAL documental] A proposta498 foi preservada byte a byte em sua pasta. Esta V2 tem a mesma identidade documental e versão2, sem implementação, autorização, CLAIM ou execução.

[DEFECT — corrigido na proposta, sujeito a revisão] O JSON e T01 anteriores permitiam VALID_ATOM_TAIL/p=0 para d=0,x=1. Embora a cauda abstrata do átomo seja matematicamente zero nesse ponto, a API F9 não pode transformá-la numa rejeição: C04 já registra CONTRACT_INCOHERENCE_NOT_REJECTION. O protocolo esperado usa o rótulo histórico CONTRACT_INCOHERENCE_NOT_VALID_REJECTION; o recibo consumido usa CONTRACT_INCOHERENCE_NOT_REJECTION. Ambos distinguem incoerência operacional de cauda abstrata. Nenhum deles foi alterado ou reexecutado.

[DERIVED/INPUT — correção] Em G/Q/T com d=0 e x_lower>0: INVALID, p_upper=null, motivo CONTRACT_INCOHERENCE_NOT_REJECTION, revisão de suporte/grau ou espaço global/identidade/limite inferior. Guarda anterior à cota trivial por limite de recurso e à agregação. Não emite p=0, p=1, não rejeição ou rejeição. Para d=0 e x_lower<=0 permanece p=1 após validação semântica. A identidade abstrata [1,1,0] em [-1,0,1] permanece apenas explicativa e não é modo alternativo chamável da API.

[REAL documental] Comparações de strings/JSON conferiram igualdade das alternativas, constantes, fórmulas d>0, recursos, integração V2/modelos/alpha/Bonferroni e T02–T08. Isso não é execução dos controles nem certificado científico. DELTA_DOCUMENTAL_V2.diff expõe todas as mudanças nos três artefatos derivados. PROVENIENCIA_FONTES.json liga o predecessor e C04 por hashes lidos.

[OPEN] A nova guarda aguarda aceite independente documental. Nada nesta V2 adota o envelope, comprova os certificados da F9 ou autoriza implementação/avaliação.
