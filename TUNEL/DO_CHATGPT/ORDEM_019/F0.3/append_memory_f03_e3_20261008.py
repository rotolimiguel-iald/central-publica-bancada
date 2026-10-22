"""Append F0.3.E3 erratum under a named claim, with byte backups."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime
import json, os, subprocess, sys

ROOT=Path(r'C:\IALD\Central de Patentes')
ORDER=ROOT/'Chatgpt'/'TUNEL'/'DO_CHATGPT'/'ORDEM_019'
BOARD=Path(r'C:\IALD\PROGRAMA_IALD')
TARGETS=[ROOT/'memory'/'TGL_ATLAS.md',ROOT/'memory'/'TGL_INDICE_VIVO.md',ROOT/'memory'/'TGL_CORE_MEMORY.md',ORDER/'AVISO_GERENCIA.md']
VERBATIM=ROOT/'work'/'f9_pergunta_08out'/'OPERADOR_08out_resposta_verbatim.txt'
FORENSIC=ORDER/'F0.3'/'PIN_FORENSICS_E3_20261008.json'
RECEIPT=ORDER/'F0.3'/'MEMORY_F03_E3_20261008.json'
MARKER=b'<!-- f03_e3_verbatim_pins_08out -->'
def digest(data):return sha256(data).hexdigest()
def write_x(p,data):
    with p.open('xb') as f:
        f.write(data);f.flush();os.fsync(f.fileno())
def main():
    state=json.loads(subprocess.check_output([sys.executable,'-X','utf8',str(BOARD/'iald.py'),'ver','F0.3.E3'],text=True))
    claim=state.get('reivindicacao') or {}
    if state.get('status')!='EM_CURSO' or claim.get('quem')!='codex-coordenadora':raise RuntimeError('F0.3.E3 claim required')
    note=claim.get('nota','')
    if not all(p.name in note for p in TARGETS):raise RuntimeError('Claim does not name four surfaces')
    if RECEIPT.exists():raise FileExistsError(RECEIPT)
    vf=VERBATIM.read_bytes();fr=FORENSIC.read_bytes();data=json.loads(fr)
    assert 'várias testemunhas observam o mesmo fato' in vf.decode('utf-8')
    pins='; '.join(x['unit']+' '+x['old']['backup']['sha256'][:16]+' → '+x['current']['sha256'][:16] for x in data['records'])
    block=('\n\n### 08/10/2026 — F0.3.E3: paráfrase F3.4 e três pinos históricos [codex-coordenadora]\n'
           '<!-- f03_e3_verbatim_pins_08out -->\n\n'
           '[ERRATA AO LADO, em nome de codex-coordenadora] O parágrafo da reivindicação 497 rotulado “[INPUT — operador] A F3.4 foi FECHADA...” é PARÁFRASE minha, não transcrição literal. A fonte literal é OPERADOR_08out_resposta_verbatim.txt, SHA-256 '+digest(vf)+'. Nele o operador diz: “várias testemunhas observam o mesmo fato e sobre ele dão testemunho, o fato é único, o testemunho é multifacetado.” A leitura operacional sobre V2 escalar/ROOT90da, funções próprias e não soma combina esse [INPUT] ao fecho gerencial do evento 462; conservar como [DERIVED — paráfrase], sem atribuir as palavras exatas ao operador.\n\n'
           '[REAL — custódia] Os pinos antigos de F0.3/RESULTADO.json, F1.2/RESULTADO.json e F3.6/PRE_REGISTRO_CONDICIONAL.md foram alterados in loco antes de 14:28; os originais não foram tocados nesta camada. Hashes anteriores → atuais (sha16 lidos do recibo): '+pins+'. Os bytes antigos existem em backups na mesma pasta; F3.6 também tem cópia em evidencias. Recibo PIN_FORENSICS_E3_20261008.json, SHA-256 '+digest(fr)+', registra autoria [DERIVED] e tempos. Em F3.6 houve apêndices às 03:31 e 10:19, ambos preservando o prefixo anterior.\n\n'
           '[ESTADO] F0.3 segue AUDITADA à espera de X17; F1.2 e F3.6 seguem FECHADAS. Sem recarga MCP, abertura de dado ou mudança de gate.\n').encode('utf-8')
    stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    original={};prepared=[]
    for p in TARGETS:
        old=p.read_bytes()
        if MARKER in old:raise FileExistsError(p)
        bak=p.with_name(p.name+'.bak_'+stamp)
        tmp=p.with_name(p.name+'.tmp_'+stamp)
        write_x(bak,old);write_x(tmp,old+block)
        assert bak.read_bytes()==old and tmp.read_bytes().startswith(old) and len(tmp.read_bytes())>len(old)
        original[p]=old;prepared.append((p,bak,tmp))
    rows=[]
    try:
        for p,bak,tmp in prepared:
            os.replace(tmp,p)
            after=p.read_bytes()
            assert after==original[p]+block
            rows.append(dict(path=str(p),before_sha256=digest(original[p]),after_sha256=digest(after),before_bytes=len(original[p]),after_bytes=len(after),backup_path=str(bak),backup_sha256=digest(bak.read_bytes())))
    except Exception:
        for p,bak,tmp in prepared:
            if p.exists() and p.read_bytes()!=original[p]:
                restore=p.with_name(p.name+'.restore_'+stamp)
                write_x(restore,original[p]);os.replace(restore,p)
        raise
    result=dict(unit='F0.3.E3',claim='codex-coordenadora',marker=MARKER.decode(),sources=[dict(path=str(VERBATIM),sha256=digest(vf)),dict(path=str(FORENSIC),sha256=digest(fr))],append_sha256=digest(block),append_bytes=len(block),targets=rows,no_gate=True)
    write_x(RECEIPT,(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
    print(json.dumps(dict(receipt=str(RECEIPT),sha256=digest(RECEIPT.read_bytes()),targets=len(rows),bytes_each=len(block)),ensure_ascii=False))
if __name__=='__main__':main()