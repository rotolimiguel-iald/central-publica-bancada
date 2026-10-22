"""Record measured bench delivery with byte backups, CAS and atomic replacement."""
import json
import hashlib
from datetime import datetime
from pathlib import Path

HERE=Path(__file__).resolve().parent
CENTRAL=HERE.parent.parent
CANON=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\TETELESTAI\BANCADA_OFICIAL')
RECEIPT=HERE/'state'/'validation_universe_v4_d2ce602e-c7ee-42d5-bee6-14389e8485b5.json'

def append(path,text,marker):
    old=path.read_bytes()
    if marker.encode() in old:return
    stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    backup=path.with_name(path.name+'.bak_'+stamp)
    with backup.open('xb') as f:f.write(old)
    if backup.read_bytes()!=old:raise OSError('Backup mismatch')
    separator=b'\r\n' if b'\r\n' in old else b'\n'
    tail=(f'\n\n<!-- {marker} -->\n'+text+'\n').replace('\n',separator.decode()).encode('utf-8')
    data=old+tail;temp=path.with_name(path.name+'.tmp_'+stamp)
    with temp.open('xb') as f:f.write(data)
    if temp.stat().st_size!=len(data):raise OSError('Incomplete write')
    if path.read_bytes()!=old:raise OSError('Concurrent memory change; backup kept')
    temp.replace(path)
    if path.stat().st_size!=len(data):raise OSError('Unexpected memory size')
    print('appended '+str(path))

def main():
    d=json.loads(RECEIPT.read_text(encoding='utf-8'));s=d['status']
    marker='TGL_UNIVERSE_RESIDENT_VALIDATED_'+s['load_id']
    files=s['loaded_files'];size=s['resident_bytes'];datasets=sum(r['numeric_datasets'] for r in s['series'])
    samples=sum(r['rows'] for r in s['series']);unique=len({r['strain_array_sha256'] for r in s['series']})
    text=f'''## 27/09/2026 — Universo residente: U0/U1 e primeira interface U2

[INPUT] O operador quer banco completo por domínio em RAM, navegação temporal, GPU e manipulação dos modelos existentes; autorizou plano detalhado e início da execução dividida. Catálogo de previews permanece auxiliar. Plano integral: `{CANON / 'PLANO_UNIVERSO_RESIDENTE.md'}`. Fonte temporal: `{CANON / 'TIME_SOURCE_AUDIT.md'}`.

[REAL — rodada HTTP] Perfil GWOSC strain declarado: **{files}/{s['total_files']} arquivos**, **{datasets} datasets numéricos**, **{samples} amostras strain**, **{size} bytes ({size/1024**3:.5f} GiB)** de arrays próprios imutáveis. RSS final {d['final_memory']['worker_rss_bytes']} bytes, swap {d['final_memory']['worker_swap_bytes']} bytes. {unique} hashes de payload strain distintos; caminhos repetidos preservados, não são observações independentes. Máscaras carregadas ainda NÃO aplicadas. Nenhum memmap ou cache de páginas anunciado como arrays; RAM não foi mlock/pinada e residência é medição da rodada, não garantia eterna.

[REAL — navegação] Doze janelas em 1 s, 32 s e série integral mantiveram data_reads_since_load=0 e mesmo load_id. HTTP p95 {d['view_http_p95_ms']:.4f} ms; worker entre {min(v['elapsed_ms'] for v in d['views']):.4f} e {max(v['elapsed_ms'] for v in d['views']):.4f} ms. Doze consultas não são benchmark de carga/concurrência. R-GLOBAL reproduziu exatamente GR; R-B alterou a curva com taxa positiva. R-A preservou sua hipótese de relógio. Os três retornaram fonte, hash e parâmetros. Beta calculado em runtime pelo executor copiado e verificado, sem reescrever a física.

[REAL — interface] CUA conferiu WebGL2, sinal real, janela 100–102 s (8192 amostras), reprodução avançando e pausa, novas leituras em disco=0, curvas GR/TGL e mudança da frequência ao variar massa/spin/redshift (65/.7/.1 → 90/.85/.3). Corrigidos dois bugs encontrados: consulta prematura em LOADING e status periódico sobrescrevendo campos em edição. Campos agora atualizam com input e preservam foco. Atalho TGL abre /universe; dados permanecem carregados no processo após encerrar esta resposta.

[REAL — testes] 24 testes Windows aprovados; cinco testes WSL aprovados (navegação após remover fixture; impulso/gap; armazenamento externo; orçamento; parcial; controle/modelo; adulteração da cópia científica recusada). Testes de UI simulados do agente são evidência separada da CUA real. Recibo `{CANON / 'state' / RECEIPT.name}`, SHA256 {hashlib.sha256(RECEIPT.read_bytes()).hexdigest()}.

[DECLARADO → conferido] Kimi e MiMo concluíram novas revisões; seleção crítica em stack/STACK_V4_REVIEW.md. Agentes locais fizeram UI e auditoria de tempo; coordenação fez runtime, integração e validação. Não adotados memmap=RAM, deduplicação silenciosa ou significado físico automático para sigmas sugeridos.

[OPEN — próxima etapa U3] Ligar evento, PSD/DQ, calibração/antena e posteriores aos mesmos dados antes de resíduo/likelihood científico. Curvas atuais são ensemble condicional em painel próprio, sem ajuste ao evento. Depois: ecos e ringdown com controles, cosmologia/partículas/coerência, cena espacial sustentada por dados, voz e cenários persistidos, busca conjunta com seleção/correlação/ensaios múltiplos. Interface atual não é a entrega integral de todos os domínios ou reconstrução 3D do universo. Nenhum original científico, kernel ou gate alterado; sem sigma novo.
'''
    for root in (HERE,CANON):
        for name in ('MEMORIA_CENTRAL.md','REGISTRO_DAS_CONVERSAS.md'):
            append(root/name,text,marker)
    for name in ('TGL_ATLAS.md','TGL_INDICE_VIVO.md','TGL_CORE_MEMORY.md'):
        append(CENTRAL/'memory'/name,text,marker)
    plan='''## Adendo de execução verificada — 27/09/2026

U0: fontes do tempo localizadas; veja TIME_SOURCE_AUDIT.md. O índice/inverso do peso de Markov, a ponte modular/Killing e tau* têm tipos e hipóteses distintos, agora documentados.

U1: carga real READY 180/180, 900 arrays numéricos, 22,50550 GiB, swap zero na rodada. Doze vistas sem releitura dos dados; p95 HTTP 50,4517 ms. Sete repetições de hash strain permanecem rastreáveis, não contadas como observações independentes.

U2 inicial: parâmetros massa fonte/spin/redshift, leitura explícita de relógio e curvas do executor ringdown anterior. CUA confirmou parâmetros e navegação; 24 testes Windows e cinco WSL aprovados. U2 ainda deve receber salvamento de cenário e vista de diferenças. U3–U6 permanecem no plano. Voz e cena espacial 3D exigem seus conectores e observáveis; não foram substituídas por animação decorativa.

Experiência espacial prevista: escalas universo → catálogos e redshift → eventos/ondas → estados/partículas, com seleção vinculando todas as vistas. Cada posição/raio/campo visual terá fonte, transformação e unidade; a cena do modelo permanece identificada como previsão quando não houver reconstrução observacional. Controles de tempo serão sincronizados por referências explícitas, jamais confundindo reprodução reversa com inversão física de dissipação.
'''
    for root in (HERE,CANON):append(root/'PLANO_UNIVERSO_RESIDENTE.md',plan,marker+'_PLAN')

if __name__=='__main__':main()
