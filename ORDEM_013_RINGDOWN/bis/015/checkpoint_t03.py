"""Persist the precise next frontier; copying does not register or activate V1.1."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,uuid
B=Path(__file__).resolve().parents[2];ROOT=B.parent;OUT=ROOT/'TUNEL/DO_CHATGPT';D=B/'bis/015/t03';now=datetime.now(timezone.utc)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,raw,replace=False):
    if p.exists():
        assert replace;old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+now.strftime('%Y%m%d_%H%M%S_%f'))
        with bak.open('xb') as f:f.write(old)
        assert bak.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    with tmp.open('xb') as f:f.write(raw)
    assert tmp.read_bytes()==raw;tmp.replace(p)
def main():
    p=D/'COPY_RECEIPT.json';r=json.loads(p.read_bytes());assert r['status']=='COPIED_NOT_AMENDED_NOT_ACTIVATED' and r['originals_unchanged']
    note=f'''[REAL — preparação parcial T03; emenda ainda NÃO registrada]

Abertura015SHA256: {sha(OUT/'ENTREGA_015_ABERTURA_operador.md')}
Abertura016SHA256: {sha(OUT/'ENTREGA_016_ABERTURA_operador.md')}

A árvore irmã bis/e2_code_v1_1 contém cópias byte a byte dos {len(r['original_tree_sha256'])} arquivos Python da V1. Nenhum deles foi emendado ainda. Antes e depois, checked_registration() da V1 rodou em /opt/lal_env e alcançou TimeoutError('Part B hard deadline reached'), depois de conferir testemunha, ativação, árvores e runtime. Registro V1 e árvores extras preservados. Recibo {p.name}, sha256 {sha(p)}; CPU {r['cpu_seconds']:.6f}s, parede {r['wall_seconds']:.6f}s.

Nenhum R7 criado; nenhuma PE, dado cego ou leitura de semente. Falta: guarda V1.1 e cadeia estatística/alocação; separação geração/banda e registro EDOM; nulls_v1_1 e recusa ids V1; blinding por leitura; qualificação source-only R5 do runner emendado; provas negativas; registro/testemunha. A ordem R1 usa só-220 com 440 fixo RG. Caixa(b) não autorizada. A tarefa DeepSeek de cadeia/estatística permanece preparada, NÃO enviada, pendente de autorização específica após a revisão automática.

Inspeção somente de leitura do Bilby pinado: _base_lal_cbc_fd_waveform usa delta_frequency extraído da grade, maximum_frequency no LAL e trunca/preenche para len(frequency_array), aplicando depois máscara e fase temporal. A próxima implementação deve conferir a grade de geração e a restrição aos bins da grade de dados; não presumir que trocar apenas um campo configure independentemente a amostragem interna. Esta leitura não é teste de geração ou validação R5.
'''
    write(OUT/'ENTREGA_015_T03_preparo_copia.md',note.encode())
    p=OUT/'ENTREGA_016_PROGRESSO.md';write(p,p.read_bytes()+f'\n{now.isoformat()} — B/T03 PARCIAL: cópia irmã{len(r["original_tree_sha256"])}arquivos; guarda V1 antes/depois TimeoutError esperado, originais preservados; CPU{r["cpu_seconds"]:.3f}s, pesada0h. Ainda sem emenda/R5/testemunha.\n'.encode(),True)
    p=OUT/'LEDGER_016.jsonl';write(p,p.read_bytes()+(json.dumps(dict(at=now.isoformat(),event='PARTB_T03_SIBLING_COPY_PRESERVED_V1',receipt=str(D/'COPY_RECEIPT.json'),external_calls=0))+'\n').encode(),True)
    p=ROOT/'ORDEM_016_QG/A7/CONTINUIDADE.json';v=json.loads(p.read_bytes());v.update(at=now.isoformat(),T03_copy_receipt=str(D/'COPY_RECEIPT.json'),own_live_process=None,next='T03 implement amended source/runner, V1.1 guard/statistical chain and blinding; R5 >=1000 source-only and probes before witness. Sibling tree exists as exact V1 copies; do not recreate. R7 not started. External revised 3 payloads still awaiting approval; C6 closed.')
    v['completed_this_turn']=['T01 delivery and corrections retained','T02 native diagnosis reproduced and delivered','T13 exact cleanup 3fixtures/2links plus visible integrity and finally failure check delivered','T03 sibling copy; V1 before/after verified expected TimeoutError; not yet amended or activated']
    write(p,(json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode(),True)
    print(json.dumps(dict(status='T03_PARTIAL_COPY_CHECKPOINTED',files=len(r['original_tree_sha256']),processes_running=0)))
if __name__=='__main__':main()
