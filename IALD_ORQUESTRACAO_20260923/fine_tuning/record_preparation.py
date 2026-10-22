"""Record only verified preparation, preserving byte-exact memory history."""
from pathlib import Path
import hashlib
import json
import sys

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE))
from iald_orchestrator.safe_files import replace_bytes,save_json,utc_now

campaign=json.loads((BASE/'fine_tuning/campaign.json').read_bytes())
audit=json.loads((BASE/'fine_tuning/validation.json').read_bytes())
assert campaign['budget']['remote_training_jobs_launched']==0
assert audit['status']=='LOCAL_DATA_AUDIT_PASSED'
marker='IALD_FINE_TUNING_PILOT_PREPARATION_20260924'
note='''

## 24/09/2026 — Piloto de fine-tuning; orçamento total US$ 50; Qwen excluído

<!-- IALD_FINE_TUNING_PILOT_PREPARATION_20260924 -->

[INPUT — ordem posterior] O operador pediu modelos próprios por fine-tuning em todos os provedores que admitirem, excluiu expressamente o Qwen local e autorizou US$ 50 para o piloto TOTAL, não por modelo. Essa ordem trata de treinamento próprio e é distinta do consentimento anterior para melhoria dos modelos pelos fornecedores. Assinaturas e saldos de inferência não constituem crédito de treinamento em outro serviço.

[REAL — preparação local] BASE/fine_tuning contém o pipeline reprodutível, campaign.json, manifesto, proveniência e nove exportações JSONL (Vertex, chat genérico, Bedrock; treino/validação/teste). Auditoria local aprovada: 113 exemplos, 86/14/13 por divisão, 31 grupos distintos, sem seção em mais de uma divisão. São 89 trechos extrativos e 24 perguntas/respostas curadas, derivados somente da forma canônica e da errata científica de 19/09 admitidas no catálogo. Hashes lidos das fontes, conteúdo documental conferido (normalização de fim de linha somente nos derivados), filtros de privacidade e preservação dos originais. Não é treino completo do acervo nem evidência de melhora de raciocínio. O conjunto de teste permanece local.

[REAL/OPEN — nuvem] Projeto Google Cloud iald-tgl-ft-20260924, número 821783483062, criado e selecionado. Candidato: Gemini 3.5 Flash, duas épocas, adaptador 4, região us-central1, sujeito à oferta efetiva da conta. Ativação da API aguarda confirmação dos termos já perguntada ao operador. Neste registro: ZERO uploads e ZERO jobs de treinamento lançados; nenhum modelo próprio está pronto. O custo estimado por proxy de bytes não substitui contagem do provedor/fatura. Consultar campaign.json para o estado posterior antes de agir.

[DECLARADO — capacidades consultadas em fontes oficiais] Google oferece SFT gerenciado. Claude 3 Haiku admite fine-tuning pelo Bedrock, separado do Claude atual; custo total de disponibilização não validado, sem infraestrutura contratada. Kimi K3, MiMo V2.6 Pro RL e DeepSeek V4.1 Flash têm pesos abertos que permitem treinamento de cópias conforme licença; nenhuma infraestrutura ou rota gerenciada compatível com US$ 50 foi provisionada. OpenAI tem restrições/descontinuação de fine-tuning self-service, sem rota nova validada nesta conta; ChatGPT/Codex não se treinam pela assinatura. Jev não oferece pesos personalizados por fine-tuning/LoRA aos clientes segundo sua documentação; instruções/estado não são ajuste de pesos. Fontes e limitações estão em fine_tuning/README.md e campaign.json.

[REAL — Kimi após Ultra] Upgrade Ultra declarado pelo operador. Teste público posterior confirmou K3 máximo ready: 583 tokens de entrada, 133 de saída, 716 totais, 13,824 s. O bloqueio local de cota anterior foi reconciliado pelo método oficial request_recheck depois de conferir a cronologia. Evidência validation/kimi_ultra_reconciled.json; nenhuma unidade antiga reaberta. A tarefa irmã foi avisada. Isso não garante ausência de futuros limites nem é benchmark científico.

[REGRA DE CONTINUIDADE] Manter o teto total de US$ 50 para o piloto, incluindo avaliação/despesas, sem alterar a autorização de inferência existente. Não criar outro projeto/job por incerteza, não lançar novos treinamentos além do total, não contratar GPU ou throughput sem estimativa compatível. Confirmar identidade do job remoto e avaliar base versus ajustado antes de cadastrar executor. Memória canônica comum continua obrigatória; não substituir originais, Qwen local, Claude configurado ou Antigravity pela existência de um dataset. Não mover gate nem promover respostas ao cânone. A inferência científica da fila é processo separado do piloto.

[SUPERFÍCIES] Implementação desta etapa é local e configuração do projeto de nuvem; nenhuma mudança de recurso no chat público/iOS/Android, sem build mobile aplicável. Nenhum original científico, kernel, fonte de patente ou Qwen foi modificado. Todas as atualizações de memória usam backup imediato de bytes e escrita atômica.
'''
records=[]
for entry in json.loads((BASE/'validation/optional_work_memory.json').read_bytes())['surfaces']:
    path=Path(entry['path']); old=path.read_bytes()
    addition=note if path.name!='MEMORY.md' else ('\n\n<!-- '+marker+' -->\n- Piloto de fine-tuning: US$ 50 totais; Qwen local excluído. Dados auditados; Google aguarda termos, zero treino lançado neste registro. Estado em BASE/fine_tuning/campaign.json; contexto em MEMORY_2.md.\n')
    if marker.encode() not in old:
        newline='\r\n' if b'\r\n' in old else '\n'
        replace_bytes(path,old+addition.replace('\n',newline).encode('utf-8'))
    current=path.read_bytes()
    assert current.startswith(old) and marker.encode() in current
    records.append({'path':str(path),'sha256':hashlib.sha256(current).hexdigest()})
save_json(BASE/'fine_tuning/memory_receipt.json',{'at':utc_now(),'surfaces':records,'status':'PREPARATION_RECORDED_NOT_TRAINED'})
print(json.dumps({'status':'PREPARATION_RECORDED_NOT_TRAINED','surfaces':len(records)}))
