from pathlib import Path
import json,datetime
from audit_provenance import OUT,atomic,metadata
p=OUT/'REVISAO_P3_PREPARACAO.md'
r=json.loads((OUT/'REVISAO_P3_DELTA_RESULT.json').read_text());assert r['count']==r['passed']
text='''
## Resolução ao lado — delta V2

[REAL — revisão independente posterior] **P3-01 resolvido no escopo da preparação, sem outro P2+ identificado.** A classificação nova envolve a callable efetivamente vinculada ao WaveformGenerator, conserva assinatura, argumentos e retorno, registra a mesma exceção uma vez e a relança. None é aborto próprio não promovido a EDOM; domínio reconhecido por texto/errno fica separado de exceção indeterminada. `domain_error_total=null` preserva o desconhecido. O status externo conserva o estágio já registrado: timeout genérico depois da tentativa não vira budget prévio por mera mensagem. O contador chamado native_attempts neste recibo é o da tentativa de waveform via wrapper Bilby; não inventaria toda chamada C auxiliar feita pela guarda temporal.

Protocolo de delta e snapshot V2 foram fixados antes dos controles. Passaram 151 verificações independentes, puras/estáticas, incluindo pins do manifesto V2, entradas, invariância dos priors/alvos/PSD/grade/seeds/limites, preservação das fontes P0–P2, classificação com stubs, deduplicação pelo objeto de exceção, assinatura/encaminhamento, handlers copiados por AST e recusa da chamada10001. A guarda de budget é idêntica por AST à anterior. Zero PE, waveform nativa ou likelihood científico instanciado; testes próprios não executaram os scripts originais. Os 100 controles de exceções e40 de preparação do autor também ficaram pinados, sem tomar essa contagem como execução P3.

**Comando apto para autorização pela coordenação, exclusivamente no contrato V2 e nos limites fixados.** Seu vetor exato foi lido de `COMANDO_EXATO_NAO_EXECUTADO.json` e o hash final coincide com os bytes do contrato (recibo do delta). Esta conclusão não é autorização emitida pelo revisor: continuam necessários o recibo verdadeiro de coordenação e a execução única pelo supervisor. O exemplo permanece falso. Não existe garantia de convergência, recuperação, cobertura, custo previsto ou prontidão para D; os limites da análise original permanecem válidos. Contrato/parecer original e achado foram preservados em snapshot e backups, com correção ao lado.
'''
atomic(p,p.read_bytes()+text.encode('utf-8'))
q=OUT/'REVISAO_P3_PREPARACAO_RECIBO.json';rec=json.loads(q.read_text());rec['resolution']={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'P3_01_RESOLVED_COMMAND_ELIGIBLE_FOR_COORDINATION_AUTHORIZATION','finding':'P3-01','contract_sha256_read':r['contract_sha256_read'],'checks':r['count'],'command_authorized_by_reviewer':False,'delta_artifacts':[metadata(OUT/x)[0] for x in ['REVISAO_P3_DELTA_PROTOCOL.json','REVISAO_P3_DELTA_RESULT.json','verify_p3_delta.py']]};rec['latest_report']=metadata(p)[0];atomic(q,json.dumps(rec,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'report':metadata(p)[0],'receipt':metadata(q)[0]},ensure_ascii=False))
