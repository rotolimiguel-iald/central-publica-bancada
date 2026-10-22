from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json
ROOT=Path(__file__).resolve().parent
CHAT=ROOT.parent;OUT=CHAT/'TUNEL/DO_CHATGPT';DEST=ROOT/'A7';DEST.mkdir(exist_ok=True)
catalog_path=CHAT/'TUNEL/PARA_CHATGPT/ORDEM_016_INSUMOS/FONTES_DA_CASA.json'
catalog=json.loads(catalog_path.read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):
    raw=v if isinstance(v,bytes) else (v.encode() if isinstance(v,str) else json.dumps(v,ensure_ascii=False,indent=2).encode())
    stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    if p.exists():
        old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+stamp);bak.write_bytes(old);assert bak.read_bytes()==old
    temp=p.with_name(p.name+'.tmp_'+stamp);temp.write_bytes(raw);assert temp.read_bytes()==raw and raw;temp.replace(p)
def find_named(obj,key):
    if isinstance(obj,dict):
        if key in obj:return obj[key]
        for v in obj.values():
            found=find_named(v,key)
            if found is not None:return found
    elif isinstance(obj,list):
        for v in obj:
            found=find_named(v,key)
            if found is not None:return found
    return None
sources=[]
for key in ['ENTREGA_087','ENTREGA_075','ADMISSIBILIDADE_SIMBOLO_EXTRATOR']:
    ref=find_named(catalog,key);assert ref
    p=Path(ref['caminho']);actual=sha(p)
    assert actual==ref['sha256'],(key,actual,ref['sha256'])
    sources.append(dict(key=key,path=str(p),sha256=actual,manifest_match=True,lines=len(p.read_text(encoding='utf-8').splitlines())))
for relative in ['REEXAME_SUFICIENCIA_087_20260910/REEXAME_SUFICIENCIA.md',
                 'REEXAME_SUFICIENCIA_075_20260910/REEXAME_SUFICIENCIA.md',
                 'COMPARACAO_CAUSAL_FUNDOS_072_20260910/CONTRATO_ADMISSIBILIDADE_Q2.md',
                 'DIAMANTE_MODULAR_20260916/PRIMITIVA_RELATIVA_RELOGIOS.md']:
    p=CHAT/relative;sources.append(dict(path=str(p),sha256=sha(p),manifest_match=None,
                                     provenance='Direct reference in named source; read in full this turn',lines=len(p.read_text(encoding='utf-8').splitlines())))
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md');now=datetime.now(timezone.utc)
registry=dict(status='REAL_SOURCE_AUDIT_NOT_NEW_ANOMALY_CALCULATION',at=now.isoformat(),opening_sha256=opening,
 sources=sources,catalog_sha256=sha(catalog_path),
 classical_relative_primitive='Written result in localized physical-clock complex, finite jets per coefficient, no uniform causal scaling bound established',
 truncated_087='Oriented Lorentzian four-dimensional space form; constant sigma; real K>0; not the physical sigma=id background',
 order_bound='First-order differential extractor; possible +1 jet-order under homotopy is an upper bound, not an actual anomaly',
 actual_quantum_break='NOT_COMPUTED_IN_READ_SOURCES',
 required_next='Declare temporal-product prescription and model data before computing quantum Ward breaking and its Wess-Zumino consistency',
 no_new_lean_cas=True,gate_changed=False)
save(DEST/'A7a_SOURCE_REGISTER.json',registry)
text=f'''[REAL — auditoria de fontes; DERIVED/OPEN — estatutos preservados das notas escritas]

# A7.a — limite superior não é anomalia

Abertura SHA256: `{opening}`.

As três fontes nominais da ordem foram relidas integralmente e seus SHA256 conferidos com FONTES_DA_CASA.json. Quatro remissões diretas também foram lidas por inteiro. Pins, linhas e proveniência constam de A7a_SOURCE_REGISTER.json. Não houve novo cálculo de diagramas, CAS ou Lean nesta etapa documental.

| Objeto | O que a fonte estabelece | O que não estabelece |
|---|---|---|
| Descida075 | Um cociclo total (s+d_H)Ω=0 na classe declarada | Primitiva total, normalização causal ou QME |
| Primitiva relativa nos relógios físicos | a=sB+d_HC, ghost positivo, na completação localizada com jatos finitos por coeficiente | Família multilinear de contratermos com cotas/contatos/regularidade em todas as aridades |
| Teste087, sigma constante | Resultados CE e linha clássica em H⁴ no truncamento espaço-forma | Anomalia de ghost1/forma4; fundo físico sigma=id; QME |
| Símbolo do extrator F | Ordem diferencial1; a homotopia pode elevar a ordem máxima em até1 | Quebra efetiva não nula, excesso real da cota ou impossibilidade de remoção |

O negativo honesto permanece: a primitiva relativa está paga no estatuto escrito e no seu domínio; a primeira quebra quântica concreta da construção causal Q2 ainda não foi calculada nas fontes lidas. Uma classe cohomológica disponível não determina o coeficiente que os produtos temporais efetivamente geram. A classe par H⁴ da 087 também não tem, por nome, o grau da anomalia física.

Não transportar a contração por relógios para sigma constante: sua localização exige inversibilidade de E(v)=(dφ̄(v),dX̄(v)); o domínio regular que admite sigma constante é distinto. Não transportar tampouco os resultados de sigma constante para φ̄=id. Não voltar a pedir FK=Id ou estado livre067 para suprir a pendência causal já localizada.

Para A7.b, a quantidade a medir é a quebra da Ward/QME de uma prescrição efetiva, na ordem de ħ e aridade especificadas. A notação “Q2” nomeia a construção causal da linhagem; não identifica por si um coeficiente de dois laços. Registrar prescrição, entradas BV, contatos e liberdade finita antes de qualquer cálculo. Depois conferir consistência de Wess–Zumino e admissibilidade da família de contratermos na mesma classe.

Próximas fontes diretas: PRODUTOS_TEMPORAIS_E_ANOMALIA_LOCAL.md e DICIONARIO_GRASSMANN_E_ACAO_BV.md, vinculadas pelo contrato Q2. Não foi inferida nova anomalia ou sua ausência. A7.a PAGO como registro; A7.b ainda em preparação. Gate intacto.
'''
save(OUT/'ENTREGA_016_A7a_registro_limite_anomalia.md',text)
ledger=OUT/'LEDGER_016.jsonl';old=ledger.read_bytes();marker='A7A_REGISTER_SCOPE_20260924'
if marker.encode() not in old:
    entry=dict(event=marker,at=now.isoformat(),manifest=str(DEST/'A7a_SOURCE_REGISTER.json'),manifest_sha256=sha(DEST/'A7a_SOURCE_REGISTER.json'),external_execution=False)
    save(ledger,old+(json.dumps(entry,ensure_ascii=False)+'\n').encode())
events=[json.loads(l) for l in ledger.read_text(encoding='utf-8-sig').splitlines() if l.strip()];costs={}
for e in events:
    c=e.get('cost_estimate_usd',e.get('cost_usd',e.get('custo_usd')));key=e.get('execution_id') or e.get('job_id') or e.get('request_id') or e.get('execution_task_id')
    if c is not None and key:costs[key]=Decimal(str(c))
p=OUT/'ENTREGA_016_PROGRESSO.md';old=p.read_bytes()
if marker.encode() not in old:
    save(p,old+f'\n- {now.isoformat()} — A7.a PAGO como registro documental: 3 hashes nominais conferidos e 4 remissões diretas lidas. Primitiva relativa/CE/ordem do extrator separados da quebra quântica concreta ainda não calculada. Máquina matemática 0h; bancada não exclusiva. Custos explícitos US${sum(costs.values(),Decimal(0))}, incompletos. Abertura {opening}. Não move gate; próximo A7.b prescrição antes do cálculo. [{marker}]\n'.encode())
print(json.dumps(dict(status=registry['status'],sources=len(sources),catalog_matches=3)))
