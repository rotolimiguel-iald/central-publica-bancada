"""Issue M6 and the Part A closure with byte-linked evidence; no scientific run."""
from pathlib import Path
from datetime import datetime,timezone
import os,json,hashlib,sys,zipfile
B=Path(__file__).resolve().parents[1];D=B.parent/'TUNEL/DO_CHATGPT'
receipt=B/'bis/M6_MA_DELIVERY_MANIFEST.json'
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for c in iter(lambda:f.read(4194304),b''):h.update(c)
    return h.hexdigest()
if '--verify' in sys.argv:
    m=json.loads(receipt.read_bytes())
    for name,h in m['files'].items():
        if sha(Path(name))!=h:raise ValueError('Changed '+name)
    print('PASS',len(m['files']));raise SystemExit
files={}
def cite(p):
    files[str(p)]=sha(p)
    return f'[{p.name}](<{p.as_posix()}>) SHA256 `{files[str(p)]}`'
def new(p,s):
    if p.exists():raise FileExistsError(p)
    raw=s.encode('utf-8');t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(raw)
    if t.read_bytes()!=raw:raise ValueError('Write mismatch')
    t.replace(p);files[str(p)]=sha(p)
def load(n):
    p=B/n;files[str(p)]=sha(p);return json.loads(p.read_bytes())
closing=B/'bis/C7_SUPPLEMENTS_V3_2_CLOSING_REVIEW.md'
if not closing.exists():raise FileNotFoundError('Await independent closure: '+str(closing))
now=datetime.now(timezone.utc).isoformat();opening=D/'ENTREGA_013BIS_ABERTURA_operador.md'
bundle=load('bis/C7_FINAL_BUNDLE_V3_1_VALIDATION.json')
replay=load('bis/C7_V3_2_C6_REPLAY.json');clean=load('bis/C7_V3_2_CLEAN_VALIDATION.json')
if bundle['status']!='PASS_CLEAN_BUNDLE_BYTE_VERIFICATION' or replay['status']!='PASS_NUMERICAL_REPRODUCTION':raise ValueError('Validation failed')
archive=B/bundle['archive']
if sha(archive)!=bundle['archive_sha256']:raise ValueError('Bundle changed')
with zipfile.ZipFile(archive) as z:
    m=json.loads(z.read('TGL_RINGDOWN_DELIVERY_v3_1/MANIFEST.json'))
    expected=['C7_INDEPENDENT_v3_3','C7_POSTERIOR_REPRODUCTION_v3_2','C7_GWTC3_REPRODUCTION_v3_2','C7_INJECTION_REPRODUCTION_v3_2','C7_IMR_RECOVERY_REPRODUCTION_v3','C7_COHERENT_SOURCE_REPRODUCTION_v3','C7_NATIVE_SEOB_WAVEFORM_v3']
    if [r['package'] for r in m['source_packages']]!=expected:raise ValueError('Stale package selection')
    for r in m['files']:
        raw=z.read('TGL_RINGDOWN_DELIVERY_v3_1/'+r['path'])
        if hashlib.sha256(raw).hexdigest()!=r['sha256'] or len(raw)!=r['bytes']:raise ValueError('Changed bundle member')
ledger=load('cache/MANIFESTO_DOWNLOADS_013BIS_v2.json')
if ledger['absent'] or ledger['changed'] or any('license' not in r for r in ledger['files']):raise ValueError('Licence ledger incomplete')
fiche='''[REAL — ficha C7; reprodução numérica separada de calibração física]

# Reaproveitamento C7

Existiam os sete pacotes C7_* originais, reproduce_c6.py e reproduce.py, seus MANIFEST.json::files/shipped_files e os resultados congelados. São reusados sem refazer ciência: cálculos originais em reproduction/ ou reproduce_legacy.py, resultados C4/C6, insumos mínimos per_series[2] com origem e hash. Os wrappers e provas abaixo são novos porque os originais permitiam conflito de saída, resultado não finito, criação interna ou vazamento de temporário.

Novo: pacote principal v3_3; suplementos POSTERIOR/GWTC3/INJECTION v3_2 e IMR/COHERENT/NATIVE v3; bundle único v3_1; guardas de finitude, escopo por leitura, proveniência/licenças, fixture e unidades, output externo e finally. Os scripts e linhas de origem estão no manifesto/árvores congeladas; a tabela reading_scope.json contém dez leituras e seis conjuntos. O construtor é refeito/build_final_bundle_v3_1_013bis.py::main; verificadores são verify_delivery.py e reproduce_c6.py::main.

PAGO: identidade de bytes em extração limpa, 75 resultados C6 reproduzidos, diferença zero, negativas e downgrade testados. NÃO PAGO: calibração de forma de onda, observável de realização única, mapeamento Kerr/laboratório, pasta profunda (aviso MAX_PATH usado conforme F6), nova reprodução científica de todos os suplementos. Esses limites são explícitos nos READMEs. Nenhuma campanha C5 reaberta. As versões defeituosas permanecem ao lado.

Reprodução: conferir o bundle com python -B verify_delivery.py; os comandos completos de replay estão no README e em bis/C7_V3_2_CLEAN_VALIDATION.json. Usar caminhos externos a TODA a entrega, não só ao subpacote. A guarda de cada wrapper protege seu subpacote; proteção automática do diretório-pai inteiro não foi demonstrada. Axiomas: N/A — sem Lean.
'''
fiche+='\nÂncoras medidas nos arquivos existentes (arquivo:linha):\n'
for name,token in [('C7_INDEPENDENT/reproduce_c6.py','def main('),('C7_POSTERIOR_REPRODUCTION/reproduce.py','def main('),('C7_GWTC3_REPRODUCTION/reproduce.py','def main('),('C7_INJECTION_REPRODUCTION/reproduce.py','def main(')]:
    p=B/name;lines=p.read_text(encoding='utf-8').splitlines()
    matches=[i+1 for i,line in enumerate(lines) if token in line]
    if len(matches)!=1:raise ValueError('Unresolved source anchor: '+name)
    fiche+=f'- `{name}:{matches[0]}`; SHA256 `{sha(p)}`.\n';files[str(p)]=sha(p)
fiche+='\nAbertura: '+cite(opening)+'\nPacote: '+cite(archive)+'\n'
new(B/'REAPROVEITAMENTO_C7.md',fiche)
large=[];errors=[]
def error(e):errors.append(str(e))
for root,dirs,names in os.walk(B,onerror=error):
    root=Path(root)
    if root==B:dirs[:]=[x for x in dirs if x!='cache']
    for n in names:
        p=root/n
        try:
            size=p.stat().st_size
            if size>25000000:large.append(dict(path=str(p),bytes=size))
        except OSError as e:errors.append(str(e))
if large or errors:raise ValueError('F7 final scan failed: '+repr((large,errors)))
fiches=[B/f'REAPROVEITAMENTO_C{i}.md' for i in range(8)]
for p in fiches:cite(p)
for n in ['REAPROVEITAMENTO_C1_v3.md','REAPROVEITAMENTO_C2_v2.md','REAPROVEITAMENTO_C6_v2.md']:cite(B/n)
hygiene=dict(status='PASS_PART_A_FINAL_HYGIENE',utc=now,large_files_outside_first_level_cache=large,scan_errors=errors,threshold_bytes=25000000,reuse_fiches=[str(p) for p in fiches],licence_ledger_sha256=sha(B/'cache/MANIFESTO_DOWNLOADS_013BIS_v2.json'),frozen_original_download_ledger_preserved=True,old_jobs_final_snapshot_deferred_to_E3_1=True)
new(B/'bis/F7_FINAL_PART_A.json',json.dumps(hygiene,indent=2)+'\n')
text=f'''[REAL — NÃO-CEGO; F6/F7 fechados como reprodução e documentação, sem calibração física]

# ENTREGA 013 M6 — pacote final

Data UTC {now}. {cite(opening)}. Axiomas: N/A — sem Lean. Nenhuma leitura escolhida; nenhum gate ou canônico alterado.

| Critério | Estado e prova |
|---|---|
| Saída e temporários | PAGO: reprodução em destino externo, recusas antes de mkdir interno, finally cobrindo preparação/execução; revisões independentes anexas. |
| C6 em extração limpa | PAGO: {replay['rows']} linhas, diferença máxima {replay['max_lnB_difference']}, tempo {replay['elapsed_seconds']:.6f}s. Resultado físico {replay['actual_scientific_status']}. Os bytes executáveis da v3_2 reproduzida são idênticos aos da v3_3; a única correção posterior foi atribuição documental. |
| Dez leituras | PAGO: 60 linhas geradas com bandas, ln B, estatuto, z/HPD da RG e exclusão condicional universal; setor 220 condicional com modos superiores de Kerr. R-MOD marcada CONJECTURE — management hypothesis, not TGL canon nas superfícies pedidas, com paredes. |
| Unidades e convenções | PAGO: fixture per_series[2], constantes LEGACY/CODATA, BCW/exato, onset, overtones e delta_tau_linear; realização única segue OPEN/NÃO PAGO como observável físico. |
| Vereditos e negativas | PAGO: finitude/tipo, ausência/duplicata e downgrade; aprovação numérica não fixa o veredito físico. |
| Bundle inglês único | PAGO: sete versões finais, {bundle['files']} arquivos verificados em extração limpa; entrada e instruções inglesas. Documentos portugueses preservados e identificados como fontes históricas. |
| Pasta profunda | NÃO EXECUTADO: aviso MAX_PATH paga a alternativa expressa de F6. Preferir extração curta. |
| Higiene global | PAGO: nenhum arquivo >25 MB decimais fora do cache de primeiro nível, sem erro de leitura; remoções anteriores documentadas hash a hash, oito fichas e errata completas. |
| Licença por arquivo | PAGO documental: {len(ledger['files'])} entradas com campo e fonte de licença; ledger aditivo v2 substitui para consulta o congelado original, que não foi reescrito. Não foi atribuída licença geral ao código da pesquisa. |
| Ciência dos suplementos | NÃO REEXECUTADA nesta correção de empacotamento. Recibos anteriores preservados; wrappers genéricos testados em modo leve. C5 continua parede medida. |

As referências dos pareceres a “execução do operador” significam a execução pelo agente principal sob autorização; não houve alegação verificada de que o humano executou os comandos. Os wrappers protegem o próprio subpacote. A instrução externa a toda a entrega é requisito de operação, não guarda automaticamente provada para o diretório-pai do bundle.

## Tentativas preservadas

v3/v3_1/v3_2 do principal e v3/v3_1 dos suplementos permanecem. Defeitos identificados: guarda NaN; criação fora de finally; texto UTF-8 corrompido; hashes de atribuição anteriores ao texto final; mkdir anterior à recusa. Foram corrigidos em versões novas. Os primeiros builders de bundle e o primeiro bundle v3 são históricos, não a seleção final. Não apagar nem chamar essas tentativas de aprovadas.

## Arquivos e reprodução

'''
names=['bis/C7_V3_2_C6_REPLAY.json','bis/C7_V3_2_CLEAN_VALIDATION.json','bis/C7_V3_3_DOCUMENTARY_VALIDATION.json','bis/C7_V3_2_CLOSING_REVIEW.md','bis/C7_V3_3_CLOSING_REVIEW.md','bis/C7_SUPPLEMENTS_V3_2_CLOSING_REVIEW.md','bis/C7_SUPPLEMENTS_V3_2_BUILD.json','bis/C7_OTHER_V3_BUILD.json','bis/C7_FINAL_BUNDLE_V3_1_VALIDATION.json','bis/C7_FINAL_BUNDLE_V3_1_VERIFY.log','bis/F7_FINAL_PART_A.json','bis/F7_POST_REMOVAL_CHECK.json','bis/F7_NAMED_TEMPORARIES_REMOVED.json','bis/F7_DELETION_JOURNAL.jsonl','cache/MANIFESTO_DOWNLOADS_013BIS_v2.json','C4_EMENDA_TECNICA_013BIS.md','bis/REGISTRO_C4_EMENDA_013BIS.json','REAPROVEITAMENTO_C7.md','refeito/close_supplement_confinement_013bis.py','refeito/build_final_bundle_v3_1_013bis.py']
text+='- '+cite(archive)+'\n- '+cite(D/'ENTREGA_013_ERRATA_contrato.md')+'\n'
for n in names:text+='- '+cite(B/n)+'\n'
text+=f'\nVerificação dos artefatos: `C:\\Python314\\python.exe -B "{Path(__file__)}" --verify`. Replay completo: comandos do README; não iniciar C5. Nenhum posterior novo, PE de evento cego ou código canônico foi tocado.\n'
new(D/'ENTREGA_013_M6_C7_final.md',text)
ma=f'''[REAL — Parte A encerrada por resultado, falsificador ou parede medida; NÃO-CEGO]

# ENTREGA 013BIS MA — fechamento da Parte A

UTC {now}. {cite(opening)}. F1–F6 têm seis entregas formais; F7 tem oito fichas, errata de contrato, licença por arquivo e scan final limpo; F8 está satisfeito documentalmente. A regra de F0 mantém os trabalhos antigos somente até E3.1; o anexo final de encerramento dos processos será produzido então, sem usar seus produtos para mudar veredito.

PAGO: correções medidas e limites explícitos, reprodução C6 de 75 linhas e pacote final. NÃO PAGO físico: calibração C5, observável de realização, corte de relógio com suporte suficiente, escolha de partição. Esses itens fecham como paredes, não como êxito experimental. C4 = INCONCLUSIVE_SYSTEMATICS, NÃO-CEGA; C6 = diagnóstico pré-portão; C5 = parede medida. O portão corrente é PORTAO_DO_PODER_013_v2.json ao lado do original imutável, não uma sobrescrita do arquivo solicitado.

Não houve commit/push/publicação, edição de memória ou canônico. Axiomas: N/A — sem Lean. Parte B seguirá E0→E1→E2→E5/E4→E3 e etapas finais, sem pausa de marco; o orçamento só começa com seu registro próprio, posterior a esta entrega.

'''
for i in range(1,7):
    matches=list(D.glob(f'ENTREGA_013_M{i}_*.md'))
    if len(matches)!=1:raise ValueError('Milestone ambiguity')
    ma+='- '+cite(matches[0])+'\n'
for p in fiches:ma+='- '+cite(p)+'\n'
for n in ['PORTAO_DO_PODER_013_v2.json','bis/F7_FINAL_PART_A.json','bis/CONTRACT_ERRATA_ISSUED.json']:ma+='- '+cite(B/n)+'\n'
ma+='- '+cite(D/'ENTREGA_013_ERRATA_contrato.md')+'\n\nReprodução e tentativas: contratos M1–M6 e errata, com comandos, falhas preservadas e limitações por alvo. Verificação: deliver_m6_ma_013bis.py --verify.\n'
new(D/'ENTREGA_013BIS_MA_fechamento.md',ma)
files[str(Path(__file__))]=sha(Path(__file__))
new(receipt,json.dumps(dict(utc=now,files=files),indent=2,ensure_ascii=False)+'\n')
print('DELIVERED',sha(D/'ENTREGA_013_M6_C7_final.md'),sha(D/'ENTREGA_013BIS_MA_fechamento.md'))
