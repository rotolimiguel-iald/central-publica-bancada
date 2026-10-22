"""Issue the inspected documentary errata; preserve candidate and all old notes."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,subprocess,sys
B=Path(__file__).resolve().parents[1];D=B.parent/'TUNEL/DO_CHATGPT';S=B/'bis/contract_errata'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
out=D/'ENTREGA_013_ERRATA_contrato.md';receipt=B/'bis/CONTRACT_ERRATA_ISSUED.json'
if '--verify' in sys.argv:
    data=json.loads(receipt.read_bytes())
    for name,digest in data['files'].items():
        if sha(Path(name))!=digest:raise ValueError('Changed '+name)
    process=subprocess.run([sys.executable,'-B',str(S/'contract_errata.py'),'--verify'],check=True)
    print('PASS_FORMAL_ERRATA_DOCUMENTARY_ONLY');raise SystemExit
if out.exists() or receipt.exists():raise FileExistsError('Preserve issued errata')
process=subprocess.run([sys.executable,'-B',str(S/'contract_errata.py'),'--verify'],capture_output=True,check=True)
verified=json.loads(process.stdout)
if verified['status']!='PASS_DOCUMENTARY_SNAPSHOT_ONLY' or verified['writes']!=0:raise ValueError('Candidate failed')
candidate=S/'CANDIDATE.md';opening=D/'ENTREGA_013BIS_ABERTURA_operador.md'
text=f'''[REAL — errata contratual emitida, NÃO-CEGA; OPEN nos critérios científicos não pagos]

# ENTREGA 013 — errata do contrato

Emitida em {datetime.now(timezone.utc).isoformat()}. Abertura do operador SHA256 `{sha(opening)}`.

PAGO documental: complementação das oito notas identificadas pela auditoria, mais C4a como nona aditiva; estatutos, PAGO/NÃO PAGO, fontes/hashes, reprodução, axiomas e falhas estão no anexo integral abaixo. O construtor da candidata foi um agente distinto; a bancada leu o anexo e conferiu o snapshot: {verified['checked']} arquivos/ausências controlados, zero divergência atual, uma divergência de hash histórico explicada pelo backup correspondente. Isso não é nova aprovação científica.

NÃO PAGO por esta errata: recibo da gerência, calibração, retorno ao C5, correção física de dados antigos ou alteração da cronologia. A emissão formal que o anexo ainda chama de pendente é cumprida por esta capa; o corpo é preservado como documento de origem, sem reescrevê-lo.

Axiomas: N/A — sem Lean. Teoremas novos: 0; não houve declaração ou compilação Lean. As oito notas e a aditiva permanecem byte a byte nos caminhos originais. Falhas históricas não são apagadas; divergência do manifesto antigo tem backup com bytes correspondentes. Nenhum canônico, memória ou gate foi alterado.

Precisão editorial ao lado de M1: a tentativa preservada citada como “record_c0_c3 erro percentual” está no arquivo `refeito/record_c0_013bis.py.failed_PERCENT_FORMAT`; o nome anterior era inexato. Expressões concatenadas em M1/M4 são defeitos editoriais, não novos conceitos ou identificadores. As tabelas e fontes hasheadas governam os números.

Reprodução somente leitura:
```powershell
& C:\\Python314\\python.exe -B "{Path(__file__)}" --verify
```

Candidata: `{candidate}`, SHA256 `{sha(candidate)}`. Manifesto de seus {verified['checked']} controles: `{S/'MANIFEST.json'}`, SHA256 `{sha(S/'MANIFEST.json')}`. Script de verificação: `{S/'contract_errata.py'}`, SHA256 `{sha(S/'contract_errata.py')}`. Os campos e limites por nota seguem integralmente; os hashes abaixo são os lidos pelo construtor e reconferidos pelo snapshot.

---

'''+candidate.read_text(encoding='utf-8')
raw=text.encode();tmp=out.with_name(out.name+'.tmp')
with tmp.open('xb') as f:f.write(raw)
if tmp.read_bytes()!=raw:raise ValueError('Write mismatch')
tmp.replace(out)
paths=[out,candidate,S/'MANIFEST.json',S/'contract_errata.py',Path(__file__),opening]
with receipt.open('xb') as f:f.write((json.dumps(dict(files={str(p):sha(p) for p in paths},verification=verified),indent=2)+'\n').encode())
print('ISSUED',sha(out))
