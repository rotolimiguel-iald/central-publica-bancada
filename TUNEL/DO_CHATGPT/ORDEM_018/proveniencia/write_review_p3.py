from pathlib import Path
import json,datetime
from audit_provenance import OUT,atomic,metadata
base=OUT.parent/'preregistros'/'conjunto_d'/'p3_preparacao'
controls=json.loads((OUT/'REVISAO_P3_CONTROLES.json').read_text())
note='''# Revisão independente P3 — preparação do piloto sintético

## Achado acionável

**P3-01 — P2: o recibo pode reportar EDOM=0 após uma exceção explícita de domínio.** No snapshot do driver, linhas 151–154 tratam a exceção como FAILED, mas a linha 169 publica `EDOM=int(counts[2])`. A fonte copiada incrementa esse contador somente quando o retorno da chamada Bilby é `None` (`src/pseob_source.py`, linhas 116–118). O adaptador exige `catch_waveform_errors=False` (linhas 63–85), e a fonte Bilby instalada/pinada, `bilby/gw/source.py` linhas 643–645, relança a exceção antes do ramo que produz `None`. Logo, o caminho esperado para `Input domain error` aborta corretamente, mas não incrementa esse contador. O controle por stub reproduziu propagação da exceção com contador igual a zero. Isso é um defeito de proveniência do recibo, não uma chamada nativa realizada nesta revisão.

Correção pedida ao autor: no novo driver/recibo, distinguir retornos None, exceções nativas, EDOM reconhecido e ocorrência não classificável, preservando tipo/texto/parâmetros. Não converter falha em -infinito, não repetir a unidade e não alterar a fonte P0–P2 qualificada. Acrescentar controles puros de sucesso, None, EDOM explícito, exceção genérica e interrupções de budget/tempo. A coordenação reteve a autorização de execução até o delta ser revisto.

**Disposição da versão examinada:** preparação majoritariamente coerente, mas comando ainda não apto para autorização sem resolver P3-01. Nenhum outro P2+ foi localizado neste recorte. Revisão estática não demonstra que o piloto executará ou convergirá.

## Evidência examinada e controles

[REAL] Snapshot imutável do contrato, driver, supervisor, prior, fontes copiadas e recibos em `p3_review_snapshot/`; hashes lidos dos bytes no protocolo. Os 25 artefatos do manifesto conferem, assim como os 16 inputs do contrato. Conferi em modo somente leitura 1162 arquivos atuais do runtime e o interpretador; os 165 pins anteriores estão contidos e preservados. Três fontes P0–P2 são byte a byte idênticas às cópias P3. Os dois alvos do contrato têm verdade e hashes de normalização idênticos aos registros GR_GAUSS/RB_GAUSS de RUN_002, cujo NPZ pinado já foi independentemente qualificado. Não foram reabertas observações D nem geradas novas injeções.

[REAL computacional local] Protocolo fixado antes dos controles. Foram concluídos 136 controles puros/estáticos, todos com o resultado esperado, incluindo o contraexemplo P3-01. Não significa que o defeito passou: o controle confirma a sua reprodução. Erro máximo do CDF das massas em 17 posições fixas: 2,220446049250313e-16. Erro relativo máximo do Jacobiano numérico nos interiores examinados: 1,543993821684353e-09, tolerância pré-fixada 2e-7. Nenhum Bilby/LAL/Dynesty/NumPy foi importado pelos controles; nenhum likelihood físico ou sampler foi construído. A consulta WSL negada pelo sandbox foi refeita com escalonamento restrito somente à leitura de bytes, sem importar a pilha científica.

## Matemática e contrato preservados

[DERIVED] A área do retângulo de massas condicionado a 0,2<=m2/m1<=1 é 1687,5+1200+590=3477,5 massas solares². O marginal de m1 é proporcional à largura admissível de m2; a inversa CDF por três trechos e a uniforme condicional de m2 produzem densidade conjunta constante 1/3477,5. Não há uma rejeição de likelihood escondida ou Jacobiano de chirp mass. Os extremos e transições estão coerentes. As transformações acos(1-2u) e asin(2u-1) implementam os priors Sine/Cosine normalizados; índices periódicos 7/9/10 correspondem a RA/psi/fase. Doze coordenadas livres e três deformações fixadas em zero.

[REAL código] `parameters` impõe os três zeros; o adaptador só permite DTau220 variável; a fonte cria uma nova dict LAL e insere explicitamente os quatro valores por avaliação. Mantidas geração8192/max4096, análise4096/32s, banda20–1024 e a guarda temporal. GR/RB são os rótulos dos datasets, não modelos rivais de evidência. Ambos usam o mesmo modelo de recuperação e ruído pareado. O NPZ é lido por nome fixo, allow_pickle=False, com pin integral e conferência de noise/signal/injected; a PSD analítica pinada é reutilizada, sem regeneração.

[REAL código e stubs] A guarda de budget precede o incremento e a avaliação. Um stand-in aritmético recebeu exatamente10000 chamadas, incluindo as que seriam de inicialização; a chamada10001 foi recusada antes de alcançá-lo. Limites de parede e CPU também recusaram antes da avaliação nos controles. O contador interno Dynesty é apenas adicional. Com pool=None/queue_size1 e uma waveform no máximo por likelihood pelo caminho instalado, o limite se conserva para as gerações planejadas. Isso não é medição de custo nativo. RLIMIT_CPU3300/3305, AS8GiB, alarme3600 e supervisor3610 por job estão no código. São envelopes, não consumo medido; hard kill/timeout interrompe o restante sem retry.

[REAL código] Supervisor exige recibo verdadeiro com hash/ação/lista exatos, diretório EXECUTION_001 novo, jobs sequenciais e claim por unidade. Filho recusa RESULT ou CHILD_STARTED existente e marca início antes da pilha científica. O comando não permite override de NPZ/IDs/alvos e não oferece checkpoint/resume. Falha ou processo incerto interrompe o segundo job; exaustão graciosa limitada pode seguir somente ao segundo job já previsto. O exemplo continua falso e nenhum recibo real ou EXECUTION_001 foi criado pela revisão.

[REAL/OPEN isolamento] O hook bloqueia open fora dos arquivos exatos/árvore de saída, processos e rede do filho; foi conferido com eventos artificiais, sem instalar hook no processo do revisor. Imports e verificação de pins antecedem o hook. A lista não dá acesso a diretórios inteiros de dados, mas o hook não é confinamento de syscalls nativas nem auditoria do SO. O código não contém rota de leitura de strain/centros D. A declaração D_read=false no futuro recibo só terá o alcance da execução auditada, não prova universal contra execução nativa externa.

## Limites da conclusão

[OPEN] Qualificação da montagem real, custo em todo o prior, convergência, recuperação e qualquer cobertura permanecem abertos. dlogz<0,1 e ESS>=100 são diagnósticos numéricos previstos, não potência, cobertura ou descoberta de todos os modos. Dois alvos com o mesmo ruído não estimam viés populacional. A log-likelihood ratio omite a mesma constante de ruído por job; não cabe comparar suas evidências entre datasets como Bayes factor físico. Nada nesta revisão aceita V1, abre D, suspende holds ou autoriza PE.
'''
atomic(OUT/'REVISAO_P3_PREPARACAO.md',note)
receipt={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'P2_REPORTING_CORRECTION_REQUIRED_BEFORE_EXECUTION','findings':[{'id':'P3-01','priority':'P2','state':'OPEN','title':'EDOM exception can leave reported EDOM=0'}],'report':metadata(OUT/'REVISAO_P3_PREPARACAO.md')[0],'artifacts':[metadata(OUT/n)[0] for n in ['REVISAO_P3_PROTOCOL.json','REVISAO_P3_RUNTIME.json','REVISAO_P3_CONTROLES.json','verify_p3_pure.py']],'command_authorized':False,'PE':False,'native_waveforms':False,'observed_data':False}
atomic(OUT/'REVISAO_P3_PREPARACAO_RECIBO.json',json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'report':receipt['report'],'receipt':metadata(OUT/'REVISAO_P3_PREPARACAO_RECIBO.json')[0]},ensure_ascii=False))
