from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
OUT=ROOT.parent/'TUNEL/DO_CHATGPT'
sys.path.insert(0,str(ROOT/'A0'))
from auditar_axiomas import audita
now=datetime.now(timezone.utc)
stamp=now.strftime('%Y%m%d_%H%M%S_%f')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write(path,data):
    if path.exists():
        previous=path.read_bytes()
        backup=path.with_name(path.name+'.bak_'+stamp)
        with backup.open('xb') as f:f.write(previous)
        assert backup.read_bytes()==previous
    temporary=path.with_name(path.name+'.tmp_'+stamp)
    with temporary.open('xb') as f:f.write(data)
    assert temporary.read_bytes()==data and data
    temporary.replace(path)
    assert path.read_bytes()==data
entries=[]
for name,label in [('WedgeDraggedFrame_v6','wedge_frame_06'),('ExistingKillingCalibration','existing_calibration_01')]:
    source=HERE/(name+'.lean'); log=HERE/(label+'.log')
    receipt=json.loads((HERE/(label+'.json')).read_text(encoding='utf8'))
    assert receipt['rc']==0 and receipt['source_sha256']==sha(source) and receipt['log_sha256']==sha(log)
    assert not receipt['newer_kernel_files'] and not receipt['scan_errors']
    audit=audita(str(source),str(log)); assert audit['auditoria']=='PASSA',audit
    entries.append(dict(source=str(source),source_sha256=sha(source),log_sha256=sha(log),
                        receipt_sha256=sha(HERE/(label+'.json')),audit=audit))
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
receipts=[json.loads(p.read_text(encoding='utf8')) for p in HERE.glob('wedge_frame_??.json')]
receipts+=[json.loads((HERE/'existing_calibration_01.json').read_text(encoding='utf8'))]
wall=sum(x['wall_seconds'] for x in receipts)
cpu=sum(x['cpu_user_seconds']+x['cpu_kernel_seconds'] for x in receipts)
manifest=dict(status='REAL',utc=now.isoformat(),opening_sha256=opening,entries=entries,
              count_audited=sum(x['audit']['n_declaracoes_auditadas'] for x in entries),
              reused_proof_count=2,new_composition_count=1,wall_seconds=wall,cpu_seconds=cpu,
              scope='Geometric fields of ContratoH2 for arbitrary supplied N; not a full H2 inhabitant.')
write(HERE/'geometric_reuse_manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2).encode())
report=f'''[REAL — compilação isolada e auditoria; escopo geométrico]

# ORDEM 016 — A-3.d: composição com a normalização já existente

UTC {now.isoformat()}. ABERTURA sha256 `{opening}`.

**PAGO no escopo pedido dos campos geométricos de H2 dado o boost.** Para todo
`N : KillingNormalization` admissível, a composição entrega κ>0, norma de Killing
unitária no ponto N, frame regional suave com determinante invertível, arrasto
`E(boost(s)x)=boostMat(s)E(x)` e coluna fiducial positivamente proporcional ao Killing.
Não escolhe N, rede W, realização R, massa ou partição física.

O frame utilizado é `E(x)=[[x¹,x⁰,0,0],[x⁰,x¹,0,0],[0,0,1,0],[0,0,0,1]]`:
`det E=(x¹)²−(x⁰)²>0` na cunha. A taxa é `κ=1/sqrt((N¹)²−(N⁰)²)`.

**Reaproveitamento explícito:** `refRadius`, `refRadius_pos` e
`observer_unit_of_index` foram extraídos de ContratoQG_v31_Teoremas sem mudar seus
corpos, apenas com import/namespace de bancada para compilação isolada.
O lema de composição `geometric_fields_reused` consome esses dois resultados e os
fornecedores de WedgeDraggedFrame_v6. Não se anuncia nova derivação da normalização.
As variantes WedgeKillingNormalization até v4 ficam preservadas como rascunhos não
compilados e não são necessárias para estes campos. A derivada do boost já existe
em ApproximateBoostFlow; A2/BoostRepresentationBridges conserva a ligação de matriz
por permutação dos eixos e inversão de rapidez. Nenhuma nova derivada foi alegada aqui.

**Validação:** rc 0, 3 declarações auditadas na composição/extrato (duas reutilizadas,
uma composição), acrescidas às 7 do frame: 10 declarações verificadas no trio permitido,
zero sorry/axiom novo. Fonte/log/recibos e hashes completos em
`A3/geometric_reuse_manifest.json`. Nova rodada `existing_calibration_01` em
`lake env lean -j1 -M8192`, dependências mínimas do contrato; original do kernel intacto.
Os 6 ciclos anteriores do determinante permanecem preservados; extração/composição
passou no primeiro ciclo. Máquina total desta frente: {wall/3600:.6f} h parede,
{cpu/3600:.6f} h CPU. Novas chamadas externas apenas registradas, custo ainda não medido.

**Move / não move a fronteira da QG:** não move o gate. Entrega a parte geométrica
do tipo; não fornece por si W, R, KMS, BW unitário, energia positiva ou segunda
quantização. Kimi e MiMo verificam o reaproveitamento mais amplo do acervo em unidades
separadas; suas respostas não substituem estes recibos Lean.

Próximo ramo prescrito: sub-alvo 1, fidelidade das translações nas três órbitas,
lado a lado; depois sub-alvo 4. A crítica externa pode corrigir a composição,
mas não exige refazer a seleção de horizonte já registrada.
'''
write(OUT/'ENTREGA_016_A3d_geometria_com_reaproveitamento.md',report.encode())
progress=OUT/'ENTREGA_016_PROGRESSO.md'
start=datetime.fromisoformat('2026-09-24T14:56:15.032718+00:00')
bench=(now-start).total_seconds()/3600
write(progress,progress.read_bytes()+f'\n{now.isoformat()} | A-3.d PAGO campos geométricos para N fornecido; 10 declarações auditadas (2 provas existentes reusadas), H2 completo não alegado. Bancada decorrida {bench:.6f}h; máquina total {wall/3600:.6f}h parede/{cpu/3600:.6f}h CPU. Próximo A3 sub-alvo 1 nas três órbitas.\n'.encode())
print(json.dumps(dict(audit='PASSA',declarations=manifest['count_audited'],wall_seconds=wall,cpu_seconds=cpu),ensure_ascii=False))
