from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
import hashlib, json, subprocess, sys

p=Path(__file__).resolve().parent
root=p.parent; out=root.parent/'TUNEL/DO_CHATGPT'
kernel=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
now=datetime.now(timezone.utc)
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def write(path,data,replace=False):
    if replace:
        write(path.with_name(path.name+'.bak_'+now.strftime('%Y%m%d_%H%M%S_%f')),path.read_bytes())
    else: assert not path.exists(),path
    t=path.with_name(path.name+'.tmp')
    with t.open('xb') as f:f.write(data)
    assert t.read_bytes()==data
    t.replace(path)

source=p/'WedgeDraggedFrame_v6.lean'; log=p/'wedge_frame_06.log'
receipt=json.loads((p/'wedge_frame_06.json').read_bytes())
assert receipt['rc']==0 and receipt['source_sha256']==sha(source) and receipt['log_sha256']==sha(log)
cmd=[sys.executable,'-X','utf8','-B',str(root/'A0/auditar_axiomas.py'),str(source),str(log)]
a=subprocess.run(cmd,capture_output=True,check=True)
write(p/'wedge_frame_axioms.json',a.stdout)
audit=json.loads(a.stdout);assert audit[0]['n_declaracoes_auditadas']==7
paths=[kernel.parent/'um.py',kernel/'TGLExt/ThePhysicalHorizon.lean',
 kernel/'TGLExt/TheModularFlowIsAHorizon.lean',kernel/'TGLExt/TheMasterFires.lean',
 kernel/'TGLExt/StrongAssembly.lean',kernel/'TGLExt/StrongFrame.lean',
 root.parent/'AUDITORIA_V368_20260919/ConexoesExistentes.lean',
 root.parent/'AUDITORIA_V368_20260919/conexoes/resultado.json',
 root.parent/'AUDITORIA_V368_20260919/conexoes/ConexoesExistentes.txt',
 root.parent/'AUDITORIA_V368_20260919/contexto/PORTA.md',
 root.parent/'AUDITORIA_V368_20260919/MEMORIA_CONSOLIDACAO.md',
 root/'A1/v31/ContratoQG_v31_Teoremas.lean']
anchors=['PhysicalHorizonChange','physical_horizon_preserves_eta','physical_horizon_preserves_wedge',
 'theorem the_master_fires','def theHorizon','def qgStrongCertificate_frame','def modularHorizon',
 'existingFrameSuppliesLorentzAtEveryPoint','existingHorizonSuppliesThermalCoefficient',
 'frame_ne_curvedFrame_by_drag','frame_ne_curvedFrame_by_fiducial']
records=[]
for f in paths:
    lines=f.read_text(encoding='utf-8').splitlines()
    matches={k:[i+1 for i,l in enumerate(lines) if k in l] for k in anchors}
    records.append({'path':str(f),'sha256':sha(f),'bytes':f.stat().st_size,
                    'anchors':{k:v for k,v in matches.items() if v}})
old=json.loads((root.parent/'AUDITORIA_V368_20260919/conexoes/resultado.json').read_bytes())
attempts=[json.loads(f.read_bytes()) for f in sorted(p.glob('wedge_frame_0*.json'))]
wall=sum(x['wall_seconds'] for x in attempts)
cpu=sum(x['cpu_user_seconds']+x['cpu_kernel_seconds'] for x in attempts)
latest={}
for line in (out/'LEDGER_016.jsonl').read_text(encoding='utf-8').splitlines():
    if line:
        d=json.loads(line)
        if d.get('request_id'):latest[d['request_id']]={**latest.get(d['request_id'],{}),**d}
cost=sum(Decimal(str(d.get('custo_usd',d.get('cost_usd')))) for d in latest.values()
         if d.get('custo_usd',d.get('cost_usd')) is not None)
opening=sha(out/'ENTREGA_016_ABERTURA_operador.md')
manifest={'utc':now.isoformat(),'status':'EXISTING_HORIZON_RECOVERED_NO_NEW_PHYSICAL_CHOICE',
 'opening_sha256':opening,'sources':records,'new_frame_source_sha256':sha(source),
 'new_frame_log_sha256':sha(log),'new_frame_audit_sha256':sha(p/'wedge_frame_axioms.json'),
 'new_frame_declarations':7,'attempts':len(attempts),'wall_seconds':wall,'cpu_seconds':cpu,
 'known_external_cost_usd':str(cost),'historical_positive_receipt':old['positive'],
 'remaining_work':'Compare existing suppliers with specific ContratoH2 fields; WedgeKillingNormalization drafts not compiled.'}
write(p/'existing_horizon_recovery.json',(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())
report=f'''[REAL — recuperação de fontes e recibos; não anúncio de uma nova identificação física]

# Horizonte existente — correção da recuperação de contexto

UTC {now.isoformat()}. ABERTURA sha256 `{opening}`.
Ordem posterior do operador: “sim, já está derivada no um.py. relembre que vc tem uma pasta
de bancada gigante onde vc já derivou muita coisa também”. A consulta foi ampliada para
as rotas da bancada apontadas pelo índice existente, sem executar um.py nem alterar fontes.

**Correção da frase da bancada:** não pedir novamente uma escolha genérica de horizonte.
O um.py já incorpora PhysicalHorizonChange(U) := ∃χ, U=boost χ; os lemas preservam η e a
cunha. A escolha do canal geométrico nessa realização está registrada pelo autor.

| Fornecedor recuperado | O que já entrega | Comparação específica a manter |
|---|---|---|
| ThePhysicalHorizon | boost da cunha, grupo, preservação da métrica e da cunha | Matriz 2×2; identificação BW contínua explicitamente importada nessa fonte. |
| qgStrongCertificate_frame | frame suave não constante; coframe/métrica lorentziana | ContratoH2 pede também arrasto por boost e fiducial modular. O contrato contém controles para o frame diagonal legado. |
| theHorizon e the_master_fires | instância de equilíbrio e coeficiente térmico | A fonte especifica κ=G=δA=1; isso não é o mesmo dado que N externo no contrato v3.1. |
| modularHorizon | fluxo efetivo da torre, normalização do fator e preservação de ω | TowerHorizon e a representação geométrica sobre região não são tipos intercambiáveis por nome. |
| ConexoesExistentes.lean, 19/09 | três adaptadores e recibo rc0/trio para Lorentz e horizonte | Reaproveitar; não criar novos adaptadores idênticos. |

Não inferir lacuna de uma flag falsa: evaluate_v350_kernel_frontier contém uma lista literal
de remaining. A leitura dessa lista não verifica se a bancada posterior já fornece o argumento.
Também não inferir equivalência de contratos só por Lorentz, H2 ou horizonte no nome.
O próximo trabalho é fornecedor → tipo/hipóteses → consumidor → evidência, seguindo a PORTA
da consolidação, inclusive preparação/Einstein/colagem onde pertinente.

**Estado do trabalho novo já executado antes desta correção:** WedgeDraggedFrame_v6.lean,
7 declarações auditadas no trio, rc0. E(x) tem bloco [[x¹,x⁰],[x⁰,x¹]], determinante
(x¹)²−(x⁰)²>0 na cunha, suavidade, arrasto pelo boost e fiducial proporcional ao Killing.
Não é apresentado como primeira construção lorentziana do acervo. O alvo foi o campo
adicional de arrasto do contrato, não refazer Lorentz. Se um fornecedor equivalente for
localizado na bancada, este artefato vira redundância documentada, sem implantação.
WedgeKillingNormalization e suas variantes são rascunhos ainda NÃO compilados; nenhum
H2 completo foi declarado. A-3.d permanece em curso, não PAGO integral.

Seis tentativas do frame, todas preservadas: {wall:.6f}s parede, {cpu:.6f}s CPU.
Gasto externo conhecido agregado por request_id: US${cost}; custos não informados não
contados como zero. Nenhuma chamada externa nova nesta recuperação. Nenhuma alteração
de um.py, kernel, Atlas ou gate. Manifesto de hashes/linhas: A3/existing_horizon_recovery.json.
'''
write(out/'ENTREGA_016_MEDIDA_horizonte_existente_recuperado.md',report.encode())
progress=out/'ENTREGA_016_PROGRESSO.md'
write(progress,progress.read_bytes()+f'\n{now.isoformat()} | A-3.d EM CURSO: frame arrastado, 7 declarações auditadas; 6 tentativas, {wall/3600:.6f}h parede/{cpu/3600:.6f}h CPU. Ordem posterior: recuperar fornecedores no um.py e bancada antes de nova derivação; horizonte boost e frame Lorentz já localizados. Normalização em rascunho, sem H2 completo. Custo externo conhecido US${cost}.\n'.encode(),True)
print(json.dumps({'report':str(out/'ENTREGA_016_MEDIDA_horizonte_existente_recuperado.md'),'frame_audit':'PASSA','count':7,'cost_known':str(cost)},ensure_ascii=False))
