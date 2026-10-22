"""Append an auditable U3 delivery to the existing memory surfaces."""
import argparse,hashlib,json
from datetime import datetime
from pathlib import Path
from record_universe_delivery import append
HERE=Path(__file__).resolve().parent
CENTRAL=Path(r'C:\IALD\Central de Patentes')
CANON=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\TETELESTAI\BANCADA_OFICIAL')
CAMPAIGN=CENTRAL/'Chatgpt/IALD_ORQUESTRACAO_20260923/ORDEM_018_TESTE_SENSIBILIDADE/campaign.json'

def main():
 parser=argparse.ArgumentParser();parser.add_argument('receipt');args=parser.parse_args()
 receipt=Path(args.receipt).resolve();d=json.loads(receipt.read_text(encoding='utf-8'))
 if d['status']!='DEPLOYED_EVENT_UI_BACKEND_VALIDATED_NOT_INFERENCE':raise ValueError('Unverified delivery')
 norm=d['example']['channels'][0]['normalization']
 if norm['method']!='RIGHT_POLAR_FACTOR_SQRT_W_TRANSPOSE_W':raise ValueError('Wrong normalization receipt')
 s=d['resident'];stamp=datetime.now().strftime('%d/%m/%Y %H:%M')
 marker='TGL_U3_EVENT_VERIFIED_'+d['load_id'];digest=hashlib.sha256(receipt.read_bytes()).hexdigest()
 destination=CANON/'state'/receipt.name;raw=receipt.read_bytes();temp=destination.with_suffix('.new');temp.write_bytes(raw)
 if temp.stat().st_size!=len(raw):raise OSError('Incomplete receipt copy')
 temp.replace(destination)
 cp=json.loads(CAMPAIGN.read_text(encoding='utf-8-sig'))
 text=f'''## {stamp} — U3: GW250114 nos dados residentes; ORDEM 18 em coordenação

[REAL] A interface /universe ganhou o painel GW250114_082203: H1/L1, cinco janelas C6 registradas, 410 amostras a 2048 Hz por detector, dado/GR/TGL/resíduos e controles de massa, spin, z, relógio, amplitudes e fases manuais. DQ/injeções são aplicadas no intervalo original inteiro, pelos seus próprios tempos. Hashes de arquivos, payloads e operadores de ruído são distintos e rastreáveis. Vistas bruta e normalizada (B=sqrt(WᵀW), do W407×410) usam a mesma transformação para dado e modelos; preservação da norma verificada. A vista normalizada usa índices de referência e coordenadas adimensionais não locais; não é reconstrução de sinal ou 410 observações independentes.

[REAL — medição após instalação] {s['loaded_files']}/{s['total_files']} arquivos, {s['resident_bytes']} bytes de arrays próprios; RSS {s['worker_rss_bytes']} bytes; swap {s['worker_swap_bytes']} bytes. Cinco consultas HTTP entre {min(q['http_ms'] for q in d['queries']):.2f} e {max(q['http_ms'] for q in d['queries']):.2f} ms; nenhuma releitura de strain. Controle R-GLOBAL=GR e parâmetros alterando modelo sem alterar dados passaram. 29 testes científicos (18 manifesto, 6 evento, 5 worker) aprovados; suíte Windows tinha 37 aprovados e 14 omitidos por runtime científico antes das duas novas regressões exclusivas WSL. CUA conferiu evento, parâmetros, GPUs WebGL2, curvas e troca entre vistas. Estes são controles do aplicativo, não testes novos de significância.

[OPEN] U3 ainda não inclui projeção física de antena/posterior com calibração marginalizada. O painel220 efetivo não substitui a inferência220+440 de C6. INCONCLUSIVE_SYSTEMATICS da análise anterior permanece. U4-U6, demais eventos/domínios, voz e cena espacial científica continuam no plano. Nenhum original científico, kernel ou gate alterado.

[INPUT] Pedido do operador nesta rodada: “Siga para a próxima etapa. Eu quero que enquanto vc trabalha vc peça ao Kimi ao mimo e ao DeepSeek para carregarem a memória completa da TGL que é a última versão do um.py v375 e pensarem qual seria o teste com a sensibilidade dos atuais atuais que eu tenho que poderia nos dar um 5 sigma, peça para os três discutirem e depois passar pelo meu chatgpt para explicar ao opus (Claude) - mandar pra ele pelo orquestrador - para ele desenhar o teste escrever a ordem 18 para você executar o teste (usando nosso stack sempre que possível)”.

[DECLARADO — coordenação externa rastreada] ORDEM_018_TESTE_SENSIBILIDADE usa a fila única sob a tarefa irmã 01a0ce2b-8c2f-71b0-a9a8-91b17715a569. Base indicada {cp['um_py']['version']}, {cp['um_py']['bytes']} bytes, SHA {cp['um_py']['sha256']}; cobertura de cada consulta é parcial e registrada, nunca tratada como memória integral. Propostas, crítica cruzada, ChatGPT/Física e Claude têm recibos e fases distintas em `{CAMPAIGN}`. Registrar uma tarefa não conclui a ordem e nenhum >=5sigma foi obtido nesta entrega. 173 hashes distintos NÃO significam 173 eventos. Inventário de eventos em state/EVENT_INVENTORY_018.json quando verificado.

Porta técnica: `{CANON/'U3_EVENTO_OBSERVADO.md'}`. Recibo `{destination}`, SHA256 {digest}. Espelho de desenvolvimento: `{HERE}`. Implantação local própria; app público web/iOS/Android não alterados, builds mobile não aplicáveis.
'''
 for root in (HERE,CANON):
  for name in ('MEMORIA_CENTRAL.md','REGISTRO_DAS_CONVERSAS.md'):append(root/name,text,marker)
 for name in ('TGL_ATLAS.md','TGL_INDICE_VIVO.md','TGL_CORE_MEMORY.md'):append(CENTRAL/'memory'/name,text,marker)
 for root in (HERE,CANON):
  append(root/'PLANO_UNIVERSO_RESIDENTE.md',f'## {stamp} — U3 inicial verificada\n\nEvento GW250114 ligado ao par H1/L1 residente, DQ/injeções, ruído, normalização e controles manuais. Ver U3_EVENTO_OBSERVADO.md e recibo {receipt.name}. U3 permanece parcial: antena e posterior físico/calibração aguardam ligação. ORDEM18 coordena a escolha/revisão do próximo teste; nenhuma significância foi produzida pelo painel.',marker+'_PLAN')
  readme=root/'README.md'
  if readme.exists():append(readme,'## Evento interativo\n\nAbra /universe e escolha GW250114. Carregue GWOSC, selecione um relógio e varie os parâmetros. Vistas bruta e normalizada disponíveis; diagnóstico não é fit nem sigma. Consulte U3_EVENTO_OBSERVADO.md.',marker+'_README')
 print(json.dumps({'marker':marker,'receipt_sha256':digest},ensure_ascii=False))
if __name__=='__main__':main()
