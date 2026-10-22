from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
OUT=ROOT.parent/'TUNEL/DO_CHATGPT'
sys.path.insert(0,str(ROOT/'A0'))
from auditar_axiomas import audita
now=datetime.now(timezone.utc);stamp=now.strftime('%Y%m%d_%H%M%S_%f')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,data):
    if p.exists():
        old=p.read_bytes(); b=p.with_name(p.name+'.bak_'+stamp)
        with b.open('xb') as f:f.write(old)
        assert b.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+stamp)
    with t.open('xb') as f:f.write(data)
    assert t.read_bytes()==data and data
    t.replace(p);assert p.read_bytes()==data
source=HERE/'VectorRapiditySpectrum.lean';log=HERE/'vector_rapidity_01.log'
receipt=json.loads((HERE/'vector_rapidity_01.json').read_text(encoding='utf8'))
assert receipt['rc']==0 and receipt['source_sha256']==sha(source) and receipt['log_sha256']==sha(log)
assert not receipt['newer_kernel_files'] and not receipt['scan_errors']
audit=audita(str(source),str(log));assert audit['auditoria']=='PASSA'
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
manifest=dict(status='REAL',utc=now.isoformat(),opening_sha256=opening,source_sha256=sha(source),
              log_sha256=sha(log),receipt=receipt,audit=audit,
              pending='Orbit measure and chart intertwining for each physical representation.')
write(HERE/'vector_rapidity_manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2).encode())
report=f'''[REAL — lema funcional compilado; A3.4 em curso]

# ORDEM 016 — ausência de autovetores com fibra transversal

UTC {now.isoformat()}. ABERTURA sha256 `{opening}`.

Para qualquer espaço normado complexo E, seja D(s) em L²(R;E) a composição
f(ξ)↦f(ξ−s). Foi verificado:

`(∀s, ∃c∈C, ‖c‖=1 ∧ D(s)f=c•f) → f=0`.

O argumento reutiliza RetaDeLuzEspectro.D_no_eigen: a energia ‖f‖² fica
periódica sob translações inteiras; cada intervalo [n,n+1) tem a mesma
integral. Como a integral total é finita, todas são zero. A adaptação troca
valores escalares por E e enorm_mul por enorm_smul. O deslocamento é um
operador linear isométrico real, construído pela preservação de Lebesgue.

**Evidência:** primeira compilação rc0, duas declarações auditadas no trio,
sem sorry/axiom novo. {receipt['wall_seconds']:.6f}s parede;
{receipt['cpu_user_seconds']+receipt['cpu_kernel_seconds']:.6f}s CPU.
Fonte, log, recibo, origem e hashes em A3/vector_rapidity_manifest.json e
A3/vector_rapidity_provenance.json. Nenhum original/kernel alterado.

**Ainda não pago:** identificar unitariamente a medida d³p/p⁰ de cada órbita
com a descrição por rapidez e fibra transversal; conferir o conjunto excluído
de medida zero no cone e o transporte das helicidades. Não há, aqui, um
teorema sobre a representação física inteira por simples renomeação de D.
O mesmo argumento funcional pode ser reutilizado nos três ramos quando
essas ligações forem fornecidas. O gate não muda.

Próximo trabalho local A3.4: parametrização
p=(m⊥ cosh ξ,m⊥ sinh ξ,q₂,q₃), m⊥²=m²+q₂²+q₃²;
conferir domínio, jacobiano e medida, e então transportar o lema acima.
Para m=0, q⊥=0 requer tratamento a.e.; não assumir chart global bijetivo.
Para helicidade, não substituir o cociclo por 1 sem prova de equivalência.
'''
write(OUT/'ENTREGA_016_MEDIDA_A3_4_fibra_transversal.md',report.encode())
p=OUT/'ENTREGA_016_PROGRESSO.md'
write(p,p.read_bytes()+f'\n{now.isoformat()} | A3.4 EM CURSO: ausência de autovetores em L²(R;E) reaproveitada/generalizada, 2 declarações auditadas, primeiro ciclo; medida/chart das órbitas pendentes. Máquina {receipt["wall_seconds"]/3600:.6f}h parede; sem nova chamada externa. Próximo ligação de medida em rapidez.\n'.encode())
print(json.dumps(dict(audit='PASSA',declarations=2,next='A3.4 orbit measure/chart'),ensure_ascii=False))
