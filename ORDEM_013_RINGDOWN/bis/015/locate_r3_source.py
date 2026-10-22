"""Pin already-cached primary source for the later R3 step; no patch/build."""
from pathlib import Path
from datetime import datetime,timezone
import json,sys
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;B=D.parents[1];ROOT=B.parent;OUT=ROOT/'TUNEL/DO_CHATGPT'
sys.path.insert(0,str(ROOT/'ORDEM_016_QG'))
from prepare_part_d import save,write,sha

def main():
    primary=B/'cache/source_evidence/lal_generator_source_gitlab'
    source=primary/'LALSimIMRSpinAlignedEOB.c';provenance=primary/'PROVENANCE.json'
    p=json.loads(provenance.read_bytes());assert sha(source)==p['sha256'] and source.stat().st_size==p['bytes']
    lines=source.read_text().splitlines()
    assert lines[2059].strip()=='if(dtau220 > 0)'
    excerpt='\n'.join(f'{i+1}: {lines[i]}' for i in range(2058,2099))+'\n'
    dest=D/'r3/source_location';write(dest/'buffer_excerpt.txt',excerpt.encode())
    allocation=B/'ORCAMENTO_015_v1.json';a=json.loads(allocation.read_bytes())
    items=[x for x in a['items'] if 'patch' in x['item'].lower() or 'r3' in x['item'].lower()]
    record=dict(at=datetime.now(timezone.utc).isoformat(),status='SOURCE_LOCATED_ONLY_NOT_R3_EXECUTED',
        source_relative_to_Chatgpt=source.relative_to(ROOT).as_posix(),source_sha256=sha(source),
        provenance_sha256=sha(provenance),url=p['url'],declared_commit=p['installed_commit'],
        declared_tag=p['installed_tag'],excerpt_sha256=sha(dest/'buffer_excerpt.txt'),lines=[2059,2099],
        evidence='Exact bytes match cached primary-source provenance; native binary reproducibility not established',
        allocation_sha256=sha(allocation),allocation_items=items,
        next='After T04: isolated own-venv build and122point qualification within recorded R3budget; no scientific use',
        patches=0,builds=0,scientific_runs=0,new_network_calls=0,gate_changed=False,
        operational_errata=[
            'One guessed R5_RESULT.json path was absent; recovered actual inputmanifest and originals listing; no rerun.',
            'Filename search under cache reported accessdenied for E2_PRIVATE despite exclusion; no content read. Continue only exact source_evidence paths.'])
    save(dest/'LOCATION.json',record)
    note=f'''[REAL — localização e hash de fonte já em cache; reparo R3 NÃO executado]

Abertura016SHA256: {sha(OUT/'ENTREGA_016_ABERTURA_operador.md')}
Data: {record['at']}

Fonte primária: {record['source_relative_to_Chatgpt']}, SHA256 {record['source_sha256']}. URL e commit lidos de PROVENANCE.json (SHA256 {record['provenance_sha256']}); os bytes conferem. Trecho2059–2099 preservado em bis/015/r3/source_location/buffer_excerpt.txt, SHA256 {record['excerpt_sha256']}.

O trecho dimensiona os quatro vetores pelo parâmetro dtau220; os outrosdtau são lidos logo antes. Essa inspeção identifica onde a receitaR3 atua. Não prova o reparo nem a identidade do binário instalado. O build isolado e a grade122continuam depois do T04, limitados ao orçamento registrado e sem uso científico do patch.

Recibo: bis/015/r3/source_location/LOCATION.json, SHA256 {sha(dest/'LOCATION.json')}. Zero patch, build, waveform, PE ou chamada remota nesta localização. A campanhaT03 existente segue; não foi repetida. Nenhum original, gate ou ambiente/opt alterado.
'''
    write(OUT/'ENTREGA_015_R3_fonte_localizada.md',note.encode())
    cp=ROOT/'ORDEM_016_QG/A7/CONTINUIDADE.json';state=json.loads(cp.read_bytes())
    state.update(at=record['at'],previous_goal_turn='PROGRESS_AND_VERIFIED_WAIT',R3_source_location=str(dest/'LOCATION.json'),
        scientific_execution_environment='WSL POSIX: terminal guard uses /proc; execute budgetpreparer,fixture,qualification andpilot there, never in Windows Python')
    save(cp,state,True)
    progress=OUT/'ENTREGA_016_PROGRESSO.md'
    write(progress,progress.read_bytes()+f"\n{record['at']} | B/R3 localização preparatória | fonteC e proveniência conferidas; NÃO é execução do ramo | máquina adicional0h; T03existente ativo\n".encode(),True)
    print(json.dumps(record))
if __name__=='__main__':main()
