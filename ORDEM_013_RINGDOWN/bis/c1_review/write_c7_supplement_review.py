"""Append scoped six-wrapper review, retaining the previous review byte for byte."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
B=Path(__file__).resolve().parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_bytes())
def need(ok,msg):
    if not ok:raise ValueError(msg)
first=read(B/'bis/c1_review/c7_supplement_cleanup_results.json')
fixed=read(B/'bis/c1_review/c7_supplement_v3_1_results.json')
other=read(B/'bis/c1_review/c7_other_wrapper_results.json')
for result,field in [(first,'rows'),(fixed,'rows'),(other,'packages')]:
    for row in result[field]:
        root=B/row['package'];manifest=read(root/'MANIFEST.json')
        expected=row.get('manifest_sha256',row.get('new_manifest_sha256'))
        need(sha(root/'MANIFEST.json')==expected,'Audited manifest changed')
        for entry in manifest.get('files',manifest.get('shipped_files')):need(sha(root/entry['path'])==entry['sha256'],'Package changed')
now=datetime.now(timezone.utc);report=B/'bis/C7_V3_REVIEW.md';original=report.read_bytes()
backup=report.with_name(report.name+'.bak_'+now.strftime('%Y%m%d_%H%M%S'))
with backup.open('xb') as f:f.write(original)
need(backup.read_bytes()==original,'Byte backup failed')
rows='\n'.join(f"| `{r['package']}` | {r['files']} | negativa fonte ausente, removido | janela fechada; mkdir antes da guarda permanece |" for r in fixed['rows'])
rows+='\n'+'\n'.join(f"| `{r['package']}` | {r['manifest_files']} | prepare-only sem ciência, removido | desenho/controles leves aprovados |" for r in other['packages'])
paths=['refeito/build_supplements_v3_013bis.py','refeito/close_supplement_creation_window_013bis.py','refeito/replay_legacy_in_temporary_v3.py','refeito/build_other_packages_v3_013bis.py',
       'bis/C7_SUPPLEMENTS_V3_CLEANUP_CONTROLS.json','bis/C7_SUPPLEMENTS_V3_1_BUILD.json','bis/C7_OTHER_V3_BUILD.json',
       'bis/c1_review/c7_supplement_cleanup_checks.py','bis/c1_review/c7_supplement_cleanup_results.json','bis/c1_review/c7_supplement_v3_1_checks.py','bis/c1_review/c7_supplement_v3_1_results.json',
       'bis/c1_review/c7_other_wrapper_checks.py','bis/c1_review/c7_other_wrapper_results.json']
hashrows='\n'.join(f'| `{n}` | `{sha(B/n)}` |' for n in paths)
adendum=f'''

---

## Adendo — seis wrappers e fechamento parcial dos suplementos

[REAL — auditoria de bytes, recibos e controles em memória; OPEN — confinamento antes de mkdir dos três suplementos]

Data UTC: {now.isoformat()}. O parecer v3_1 acima é histórico. **No pacote principal, C7-R1–R3 estão fechados pelo C7_V3_2_CLOSING_REVIEW.md e C7-R4 está fechado pelo C7_V3_3_CLOSING_REVIEW.md.** Este adendo trata somente do desenho de execução/cleanup dos suplementos. Não reabre ciência C5, PE, injeções, F2/C6 ou o diagnóstico de injeção A, reservado a outro revisor.

| Pacote efetivamente revisto | Arquivos no manifesto | Recibo do operador | Resultado da revisão |
|---|---:|---|---|
{rows}

### Três suplementos POSTERIOR/GWTC3/INJECTION

Verifiquei as v3 e v3_1, os manifestos/ZIPs e a igualdade dos assets científicos. A v3_1 altera somente README e reproduce.py entre os arquivos embarcados; manifests mudam como esperado. Os ZIPs v1 permanecem disponíveis, com os membros científicos coincidentes com seus manifestos e os recibos históricos extras identificados nos controles. Não foi executado programa científico nem nova preparação pela auditoria.

As seis negativas do operador (três v3, três v3_1) são FileNotFoundError por ausência de fonte; os logs, intenções e recibos foram lidos e hasheados, o manifesto indicado confere e cada temporário é filho próprio do work-root e está ausente. Isso demonstra aqueles caminhos de falha, não todos os caminhos possíveis.

**C7-S1 — janela anterior ao try, corrigida na v3_1.** Na v3, preserved.mkdir podia falhar depois de mkdtemp, deixando o filho criado; reproduzi por mock nos três wrappers. Na v3_1, preserved.mkdir antecede mkdtemp e a preparação fica sob finally. As mesmas sondas agora mostram zero temporários criados nesse erro. O finally normal remove o filho validado; o finally interno também é executado se falha a escrita de CLEANUP_INTENT. Foram cinco casos por wrapper em cada versão, 30 sondas em memória sob optimize=1; nenhum diretório real foi criado/removido por elas.

**C7-S2 — P2, ainda aberto na v3_1: escrita anterior à checagem de confinamento.** POSTERIOR reproduce.py:127–130, GWTC3:130–133 e INJECTION:128–131 executam workroot.mkdir e outputroot.mkdir antes de perguntar se esses caminhos estão dentro de ROOT. Ao fornecer ROOT/new_work ou ROOT/new_output, a sonda registra mkdir interno antes do ValueError. A execução científica não chega a começar, mas o pacote que se declara imutável já recebeu um diretório.

Correção exata: resolver ambos os caminhos, comparar ambos com ROOT resolvido e recusar os internos **antes de qualquer mkdir**; somente então criar raízes externas/destino, e finalmente o temporário sob try/finally. Em nova versão, testar separadamente work-root e output-root internos: ValueError, zero mkdir, zero mkdtemp, zero subprocess. Preservar a correção S1 e os assets. Nenhuma campanha é necessária para testar isso.

### Três suplementos COHERENT_SOURCE/IMR_RECOVERY/NATIVE_SEOB

**Sem bloqueante encontrado no recorte de execução/cleanup examinado.** Os 25, 25 e 12 arquivos conferem com os manifestos e ZIPs. reproduce_legacy.py é byte a byte igual ao reproduce.py original de cada pacote, e todos os demais arquivos históricos têm cópia idêntica (README renomeado como histórico). Os três wrappers novos são exatamente o script genérico hasheado. Os ZIPs v1 continuam legíveis e coincidem com os arquivos/manifestos antigos.

O wrapper exige opção explícita para preparar/rodar; modo padrão apenas confere hashes. work/output internos são recusados antes de mkdir; destino é criado antes do temporário; cópia, subprocesso e coleta de resultados ficam sob finally, com alvo de remoção validado como filho próprio. O subprocesso explicitamente autorizado apontaria para reproduce_legacy.py da cópia, com cwd nessa cópia. O estatuto emitido é LEGACY_REPLAY_EXIT_ZERO, não calibração científica, e scientific_calibration fica false.

Oito controles do main real em memória sob optimize=1: default, prepare-only, subprocesso **simulado** com retorno zero e um, falha de cópia, cada raiz interna e falha do destino externo. Confirmados: nenhum subprocesso em default/prepare-only; remoção e propagação nos erros de cópia/execução; zero mkdir nas raízes internas; zero temporários no erro de destino. Não houve subprocesso científico real. Os três recibos prepare-only já produzidos pelo operador coincidem com C7_OTHER_V3_BUILD; temporários estão ausentes. A compatibilidade científica completa do replay legado permanece fora desta revisão.

### Integração final ainda não executada pela revisão

Na leitura de `{fixed['final_builder_read_only']['path']}`, SHA256 `{fixed['final_builder_read_only']['sha256']}`, a lista de packages ainda selecionava POSTERIOR/GWTC3/INJECTION **v3**, não v3_1. Antes de gerar o bundle, apontar aos três suplementos finalmente corrigidos e transportar seus recibos correspondentes. Conferir essa seleção por script, além dos hashes internos, para não empacotar uma versão anterior que é íntegra mas conserva o defeito. O builder final não foi executado; nenhuma extração final é certificada aqui. A checagem de raiz dos wrappers analisados se refere ao seu pacote próprio; não foi demonstrada proteção automática do diretório-pai de uma entrega composta.

O adendo não promove NOT_FALSIFIED/PASS numérico a CONFIRMED. Escritas desta revisão limitadas a pareceres e controles próprios. Backup imediato byte a byte deste parecer: `{backup.name}`, SHA256 `{sha(backup)}`.

| Caminho relativo à raiz | SHA256 lido |
|---|---|
{hashrows}
'''
raw=original+adendum.encode('utf-8');temp=report.with_name(report.name+'.supplement.tmp')
with temp.open('xb') as f:f.write(raw)
need(temp.read_bytes()==raw and len(raw)>len(original),'Append failed');temp.replace(report)
need(report.read_bytes()==raw,'Final review mismatch')
print(json.dumps(dict(report=str(report),sha256=sha(report),bytes=len(raw),backup=str(backup),main_R1_R4='CLOSED_IN_SEPARATE_REVIEWS',supplements='S1_CLOSED_S2_OPEN',generic_three='PASS_SCOPED_DESIGN')))
