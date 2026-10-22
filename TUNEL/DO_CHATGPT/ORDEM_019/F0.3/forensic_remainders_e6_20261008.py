"""Read-only forensic of remaining historical pins after F0.3.E5."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime
import json,os
O=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019');B=Path(r'C:\IALD\PROGRAMA_IALD');D=O/'F0.3'
OUT=D/'PIN_FORENSICS_E6_20261008.json';MD=D/'PIN_FORENSICS_E6_20261008.md'
def h(p):return sha256(p.read_bytes()).hexdigest()
def pin(p):
 s=p.stat();return dict(path=str(p),sha256=h(p),bytes=s.st_size,mtime_local=datetime.fromtimestamp(s.st_mtime).astimezone().isoformat())
def wx(p,b):
 with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
def main():
 if OUT.exists() or MD.exists():raise FileExistsError('E6 outputs exist')
 inv=O/'F1.1'/'INVENTARIO.md';inv_old=inv.with_name('INVENTARIO.md.bak_20261008_010215')
 aviso=O/'AVISO_GERENCIA.md';aviso_old=aviso.with_name('AVISO_GERENCIA.md.bak_20261008_052608_296884')
 f23=O/'F2.3'/'ADENDO_TEMPERATURA_DIAGNOSTICO.md';f23_old=f23.with_name('ADENDO_TEMPERATURA_DIAGNOSTICO.md.bak_20261008_141543');f23_mid=f23.with_name('ADENDO_TEMPERATURA_DIAGNOSTICO.md.bak_20261008_114746')
 e5=json.loads((D/'PIN_FORENSICS_E5_20261008.json').read_text(encoding='utf8'))
 plan=D/'CACHE_HYGIENE_E5_PLAN_20261008.json';cache=json.loads(plan.read_text(encoding='utf8'))
 pyc=O/'F3.6'/'ASIMOV_LAMBDA_SANDBOX'/'__pycache__'/'asimov_lambda.cpython-312.pyc';pychash='111fea0c0eaafed31fd7fa41b2de834b17c01613c6225fbf7f45d42c268f7717'
 cached=[x for d in cache['targets'] for x in d['files'] if x['path']==str(pyc)]
 assert len(cached)==1 and cached[0]['sha256']==pychash and cached[0]['bytes']==19958
 assert h(inv_old)=='04a42d036db5b2b989b842260573232d2dd5f9658f4d71cb6fcf15ee076a0c0e' and inv.read_bytes().startswith(inv_old.read_bytes())
 assert h(aviso_old)=='ba43258263a608ef41cd3af179d26cb750bda173f33e5ddb7e40634294607efd' and aviso.read_bytes().startswith(aviso_old.read_bytes())
 assert h(f23_mid)=='da2513df5051ef9d5f2bb1f6783e8dd1a3f5bd3c1c9ee5bd1461c4814748d715' and f23.read_bytes().startswith(f23_mid.read_bytes())
 assert h(f23_old)=='673780c016334c72a2463453ac5bbc8179a301c19fb2ce66814fe323def099f9' and f23_mid.read_bytes().startswith(f23_old.read_bytes())
 assert not pyc.exists() and not list((B/'evidencias').glob(pychash+'*'))
 data=dict(unit='F0.3.E6',author='codex-coordenadora',source_audit=r'C:\IALD\PROGRAMA_IALD\auditorias\F0.3.E5\AUDITORIA_F0_3_E5_C1_a181bf67.md',inventory_f11=dict(board_seq=73,old=pin(inv_old),pre_e6=pin(inv),old_prefix_of_pre_e6=True),aviso_gerencia=dict(map_seq=[821,822],old=pin(aviso_old),pre_e6=pin(aviso),old_prefix_of_pre_e6=True),f23_intermediate=dict(map_seq=[817,829],before=pin(f23_old),intermediate=pin(f23_mid),current=pin(f23),before_prefix_of_intermediate=True,intermediate_prefix_of_current=True,previous_forensics=str(D/'PIN_FORENSICS_E5_20261008.json'),previous_forensics_sha256=h(D/'PIN_FORENSICS_E5_20261008.json')),pyc_f36=dict(map_seq=816,path=str(pyc),sha256=pychash,bytes=19958,cache_plan_path=str(plan),cache_plan_sha256=h(plan),physical_file_present=False,official_evidence_copy_present=False,reproducibility='HISTORICAL_PIN_NOT_REPRODUCIBLE_FROM_CURRENT_FILES; do not pretend the bytes were custodied'),no_gate=True,no_pinned_original_edited=True)
 wx(OUT,(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
 text=['# F0.3.E6 — complemento forense ao lado','', '[ERRATA AO LADO, em nome de codex-coordenadora] A F0.3.E5 incluiu o estado inicial 673780c0 e o atual cb0a73cb do ADENDO_TEMPERATURA_DIAGNOSTICO.md, mas seu texto .md omitiu o estado intermediário. O backup `ADENDO_TEMPERATURA_DIAGNOSTICO.md.bak_20261008_114746` tem SHA-256 `da2513df5051ef9d5f2bb1f6783e8dd1a3f5bd3c1c9ee5bd1461c4814748d715` (4.789 B), pinado nos mapas 817 e 829. Os bytes 673780c0 são prefixo de da2513df, que é prefixo do estado atual cb0a73cb.','', '[REAL — F1.1] O pino do quadro 73 do `F1.1/INVENTARIO.md` (`04a42d036db5b2b989b842260573232d2dd5f9658f4d71cb6fcf15ee076a0c0e`, 5.314 B) existe em `INVENTARIO.md.bak_20261008_010215`. É prefixo dos bytes atuais. A E4 começou no pino 241, então este pino mais antigo precisava de registro próprio.','', '[REAL — AVISO] Os mapas 821 e 822 pinaram `AVISO_GERENCIA.md` em `ba43258263a608ef41cd3af179d26cb750bda173f33e5ddb7e40634294607efd` (31.561 B). O backup `AVISO_GERENCIA.md.bak_20261008_052608_296884` é prefixo do estado anterior a esta E6. Por ser memória viva, novas notas mudam o hash; o recibo de memória E6 registrará o próximo estado.','', '[REAL — F3.6] O mapa 816 pinou `asimov_lambda.cpython-312.pyc` com SHA-256 `111fea0c0eaafed31fd7fa41b2de834b17c01613c6225fbf7f45d42c268f7717` (19.958 B). A higiene E5 removeu o cache; o plano registra caminho, tamanho e hash, mas o arquivo não existe mais e não há cópia em `evidencias/`. **Esse pino histórico não se reproduz dos arquivos atuais.** Não reivindicamos custódia dos bytes nem regeneração idêntica.','', '[ESTADO] Os dois documentos append-only preservam os bytes antigos; a ausência do `.pyc` é uma perda de reprodutibilidade desse pino específico. Nenhum pino foi editado nesta unidade. Sem dado aberto, publicação ou mudança de gate.','']
 wx(MD,('\n'.join(text)).encode('utf8'))
 print(json.dumps(dict(json=str(OUT),json_sha256=h(OUT),md=str(MD),md_sha256=h(MD)),ensure_ascii=False))
if __name__=='__main__':main()