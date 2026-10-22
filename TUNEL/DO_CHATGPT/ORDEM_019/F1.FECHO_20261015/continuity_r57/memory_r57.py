"""Preserve R57 component results as reviewed byte-additive memory."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import support_r57 as s

MARKER='IALD_R57_CLOCK_PACKET_COMPONENTS_20261017'

def exact_pin(path):
    p=s.pin(path)
    return {'path':p['path'],'sha256':p['sha256']}

def prepare():
    text='''\n\n## 17/10/2026 — R57: relógio local e aproximação da rede
<!-- IALD_R57_CLOCK_PACKET_COMPONENTS_20261017 -->
[REAL — em nome de codex-gerente-tgl, F1.FECHO_20261015, reivindicação939] R57 reutiliza rede/Fock R6, traço R7 e Maxwell R8; não volta à construção da v351 como estado corrente. Quatro componentes Lean verdes,37 relatórios de axiomas restritos a propext/Classical.choice/Quot.sound, zero sorry;34 verificações simbólicas exatas. Revisão independente R57_FINAL_COMPONENT_REVIEW_R2: PASS_COMPONENT_WITH_SCOPE, sem repetir builds. Originais, kernel, Bancada, dados observados e gate preservados.

[REAL — formal] Aβ(z)=zS(θM) tem leitura z exp(iθM), reconstrução e releitura; os pesos |z|²β e |z|²(1−β) mantêm a fronteira fixa. Em z=0 não há fase/normalização. Pacotes finitos de geradores compactos, refinamentos isométricos e covariância entre imagens foram construídos no H1 existente; a complexificação tem união densa. A localização continua real. Para a torre produto e fluxo modular existentes, entrelaçamento V modularFlow(clock(s))=B0(s)V força V=0; não se conclui impossibilidade de todo limite celular.

[DERIVED — modelo finito2×2×2] Com gerador integral e z(ρ)=2Tr(ρσ+), preparação z(0)=a>0 dá φ′(0)=ωOH e φ″(0)=2ΩRabi(γOH+λ)/a. Há inversa local analítica do relógio, com correção quadrática. A fase pura universal a exp(iωOH t) não vale sob bombeamento; a redução OH não é autônoma em geral. A leitura matricial está em Lean; a inversão local vem do cálculo exato/analiticidade, não de um teorema Lean desta rodada. β é runtime, λ=βγΛ. Demodulação ideal relativa cancela portadora externa.

[OPEN — alcance] R4 ainda exige observável do receptor, preparação/calibração e ligação V0/Eref/κ. R5 ainda exige excitações físicas, forma de duas pontas, refinamentos, limite de estados e entrelaçamento de dinâmica/localização. Densidade dos pacotes no alvo não realiza o dispositivo. MQC/Supercondutor/Ψ-NET são complementares. Próxima ação: calcular a forma de duas pontas a partir dos observáveis já escritos e compará-la a circularSmear, sem isometria arbitrária. R3/rito integral e R10/revisão final dependem disso; H3 universal não foi derivado. Nenhuma aceitação integral de R4/R5.

Custódia do DOCX original de janeiro e da tabela recuperada em continuity_r57; a correspondência documental não é entrelaçador físico. Rascunho Packet de8332bytes não foi recuperado; fonte compilada/candidata/snapshot conferidos em9139bytes. Avisos simp de estilo mantidos, sem nova rodada. Recibos e tentativas anteriores preservados.

Relatório: C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_019\\F1.FECHO_20261015\\continuity_r57\\RELATORIO_CONSOLIDADO_R57.txt. Entregas: device_clock_r57\\DELIVERY_R57.json e device_continuum_r57\\DELIVERY_R57.json. Revisão: review_r57\\R57_FINAL_COMPONENT_REVIEW_R2.json. Referência própria: work\\memoria_missao_20261016\\FECHO_MISSION_REFERENCE.json. Apêndice não instala candidato v394 nem presume versão nova do um.py.
<!-- END_IALD_R57_CLOCK_PACKET_COMPONENTS_20261017 -->
'''
    appendix=s.new('MEMORY_APPEND_R57.txt',text);extra=appendix.read_bytes()
    prior=json.loads((s.ROOT.parent/'miguel_reading_r56'/'MEMORY_PLAN_R56.json').read_text(encoding='utf-8'))
    rows=[]
    for row in prior['surfaces']:
        p=Path(row['path']);raw=p.read_bytes()
        assert MARKER.encode() not in raw
        rows.append({'path':str(p),'before':exact_pin(p),'before_bytes':len(raw),'append':exact_pin(appendix),
            'after_sha256':hashlib.sha256(raw+extra).hexdigest()})
    print(s.new('MEMORY_PLAN_R57.json',{'claim':939,'marker':MARKER,'surfaces':rows,'applier':exact_pin(__file__),
          'review_source':exact_pin(s.ROOT.parent/'review_r57'/'R57_FINAL_COMPONENT_REVIEW_R2.json'),
          'report':exact_pin(s.ROOT/'RELATORIO_CONSOLIDADO_R57.txt')}))

def apply():
    plan_path=s.ROOT/'MEMORY_PLAN_R57.json';review_path=s.ROOT/'MEMORY_REVIEW_R57.json'
    plan=json.loads(plan_path.read_text(encoding='utf-8'));review=json.loads(review_path.read_text(encoding='utf-8'))
    assert review['status'].startswith('PASS') and review['reviewer']!=s.ACTOR['id']
    assert review['plan']==exact_pin(plan_path) and review['applier']==exact_pin(__file__)
    p=s.project();task=next(t for t in p['projection']['active'] if t['id']=='R5')
    _,preflight=s.call('mission_cli.py',{'operation':'check','reference':str(s.REFERENCE),'actor':s.ACTOR,
       'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],
       'task_id':'R5','lease_id':task['lease']['id']},'MEMORY_PREFLIGHT')
    assert not (s.ROOT/'MEMORY_APPLIED_R57.json').exists()
    originals=[]
    for row in plan['surfaces']:
        path=Path(row['path']);raw=path.read_bytes();extra=Path(row['append']['path']).read_bytes()
        assert exact_pin(path)==row['before'] and exact_pin(row['append']['path'])==row['append']
        assert len(raw)==row['before_bytes'] and hashlib.sha256(raw+extra).hexdigest()==row['after_sha256']
        originals.append((path,raw,extra,row))
    stamp=dt.datetime.now(dt.timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    s.new('MEMORY_INTENT_R57.json',{'plan':exact_pin(plan_path),'review':exact_pin(review_path),'preflight':exact_pin(preflight)})
    backups=[]
    for path,raw,extra,row in originals:
        bak=path.with_name(path.name+'.bak_'+stamp)
        with bak.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        assert bak.read_bytes()==raw;backups.append(bak)
    results=[]
    for i,((path,raw,extra,row),bak) in enumerate(zip(originals,backups)):
        assert path.read_bytes()==raw
        temp=path.with_name(path.name+'.tmp_'+stamp)
        with temp.open('xb') as f:f.write(raw+extra);f.flush();os.fsync(f.fileno())
        assert temp.read_bytes()==raw+extra and path.read_bytes()==raw
        os.replace(temp,path);assert path.read_bytes()==raw+extra
        result={'before':row['before'],'after':exact_pin(path),'backup':exact_pin(bak),'append':row['append'],
                'prefix_preserved':True,'growth_bytes':len(extra)}
        s.new(f'memory_surfaces/SURFACE_{i:02d}_R57.json',result);results.append(result)
    print(s.new('MEMORY_APPLIED_R57.json',{'status':'APPLIED_VERIFIED','author':s.ACTOR['id'],
              'plan':exact_pin(plan_path),'review':exact_pin(review_path),'surfaces':results}))

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('operation',choices=['prepare','apply'])
    globals()[parser.parse_args().operation]()
