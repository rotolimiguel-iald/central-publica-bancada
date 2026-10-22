"""Append a reviewed documentary survey to the eight claimed memory surfaces."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import sys
import support_r59 as s

MARKER = 'IALD_R59_PAIR_COVARIANCE_20261017'

def pin(p):
    return {k:v for k,v in s.pin(p).items() if k in ('path','sha256')}

def prepare():
    text = '''

## 17/10/2026 — R59: covariância de pares e limite de ocupação
<!-- IALD_R59_PAIR_COVARIANCE_20261017 -->
[DERIVED — em nome de codex-gerente-tgl, F1.FECHO_20261015, reivindicação939] Continuidade autorizada apósR58: estado de dois modos do artigo, sem reconstruir rede/Fock/Takesaki. Para coeficiente rho do gerador, n=sinh²rho e m=<ab>=exp(i phi)sinh(rho)cosh(rho); <a>=<b>=0. Quadraturas recuperam Re/Im(m), e m/|m| recupera exp(i phi) para rho>0. Em rho=0 a fase é indeterminada; fase relativa módulo2pi não é relógio absoluto. Artigo usa rho=r; trecho do Tratado usa rho=r/2. Não identificar rho/phi com beta sem fonte.

[DERIVED — componente finito] Covariância C=V+iOmega/2 tem fatoração de Gram K†K/2 e transformação real simplética. Dois perfis ortonormais fornecidos permitem realização finita no H1; isso não escolhe os modos físicos. O mapa mistura criação/aniquilação: não é automaticamente unitário complexo de uma partícula preservando somente aniquiladores. <ab> e <a†b> são leituras diferentes. Não transferir frequência livre do par ao OH bombeado.

[DERIVED — limite controlado] No mesmo Fock de dois modos, psiN=P_Npsi/||P_Npsi|| tem fidelidade1-q^(N+1), q=tanh²rho<1. Erros exatos de ocupação e par convergem; caudas controlam potências finitas de número. [aN,aN†]=I-(N+1)|N><N|: o corte altera quadraturas/CCR. N=1 dá |m1|²=n1(1-n1), não a lei bosônica n(n+1). Não é convergência espacial da rede nem prova de domínioGKLS/regularFockDomainR8.

[REAL — execução delimitada] Scripts locais simbólicos e controles negativos; corte37verificações+5controles, com reprodução independente esparsa. Squeezing distingue identidades e casos sintéticos no recibo próprio. Sem buildLean novo, provedor, dado observado ou alteração de um.py/kernel/Bancada/gate. Resultado de componente não satisfaz R4/R5 integrais.

[OPEN — administrativo e científico] Revisão automática bloqueou recuperação do leaseR4vencido por alcance em dependentes; pedido específico ao operador, unidade F1.FECHO.R4_LEASE_R59, evento945. Nenhum resetexecutado. ExploraçãoOH anterior ao aviso preservada mas não integrada como resultado revisado; apósaviso só leitura/preparo. R5seguiu com leaseválido. Faltam modos/preparação/referência física, dinâmicaOH completa, refinamentoespacial/entrelaçamento e H3universal no alcance ampliado. Próximo: ligar a covariância calculada aos observáveis físicos já escritos, respeitando o bloqueio administrativoR4.

Relatório e recibos: C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015\pair_covariance_r59\RELATORIO_R59.txt; squeezing/, CUTOFF_DERIVATION_R59.txt, CUTOFF_RESULT_R59.json e independent_review/. Referência própria work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json; canônico consultado v393, sem promoção a v394.
<!-- END_IALD_R59_PAIR_COVARIANCE_20261017 -->
'''
    a=s.new('MEMORY_APPEND_R59.txt',text); extra=a.read_bytes()
    prior=json.loads((s.ROOT.parent/'acervo_r58/MEMORY_PLAN_R58.json').read_text(encoding='utf-8'))
    rows=[]
    for x in prior['surfaces']:
        p=Path(x['path']);raw=p.read_bytes()
        assert MARKER.encode() not in raw
        rows.append({'path':str(p),'before':pin(p),'before_bytes':len(raw),'append':pin(a),
                     'after_sha256':hashlib.sha256(raw+extra).hexdigest()})
    print(s.new('MEMORY_PLAN_R59.json',{'claim':939,'marker':MARKER,'surfaces':rows,
          'applier':pin(__file__),'report':pin(s.ROOT/'RELATORIO_R59.txt')}))

def apply():
    plan_path=s.ROOT/'MEMORY_PLAN_R59.json';review_path=s.ROOT/'MEMORY_REVIEW_R59.json'
    plan=json.loads(plan_path.read_text(encoding='utf-8'));review=json.loads(review_path.read_text(encoding='utf-8'))
    assert review['status'].startswith('PASS') and review['reviewer']!=s.ACTOR['id']
    assert review['plan']==pin(plan_path) and review['applier']==pin(__file__)
    assert plan['report']==pin(s.ROOT/'RELATORIO_R59.txt')
    m=s.call('mission_cli.py',{'operation':'project','reference':str(s.REF),'max_chars':400000},'MEMORY_PROJECT')
    t=next(t for t in m['projection']['active'] if t['id']=='R5')
    s.call('mission_cli.py',{'operation':'check','reference':str(s.REF),'actor':s.ACTOR,
        'expected_revision':m['receipt']['revision'],'projection_sha256':m['projection_sha256'],
        'task_id':'R5','lease_id':t['lease']['id']},'MEMORY_PREFLIGHT')
    assert not (s.ROOT/'MEMORY_APPLIED_R59.json').exists()
    originals=[]
    for row in plan['surfaces']:
        p=Path(row['path']);raw=p.read_bytes();extra=Path(row['append']['path']).read_bytes()
        assert pin(p)==row['before'] and pin(row['append']['path'])==row['append']
        assert len(raw)==row['before_bytes'] and hashlib.sha256(raw+extra).hexdigest()==row['after_sha256']
        originals.append((p,raw,extra,row))
    stamp=dt.datetime.now(dt.timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    s.new('MEMORY_INTENT_R59.json',{'plan':pin(plan_path),'review':pin(review_path),'claim':939})
    backups=[]
    for p,raw,extra,row in originals:
        b=p.with_name(p.name+'.bak_'+stamp)
        with b.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        assert b.read_bytes()==raw;backups.append(b)
    results=[]
    for i,((p,raw,extra,row),b) in enumerate(zip(originals,backups)):
        assert p.read_bytes()==raw
        tmp=p.with_name(p.name+'.tmp_'+stamp)
        with tmp.open('xb') as f:f.write(raw+extra);f.flush();os.fsync(f.fileno())
        assert tmp.read_bytes()==raw+extra and p.read_bytes()==raw
        os.replace(tmp,p);assert p.read_bytes()==raw+extra
        result={'before':row['before'],'after':pin(p),'backup':pin(b),'append':row['append'],
                'prefix_preserved':True,'growth_bytes':len(extra)}
        s.new(f'memory_surfaces/SURFACE_{i:02d}_R59.json',result);results.append(result)
    print(s.new('MEMORY_APPLIED_R59.json',{'status':'APPLIED_VERIFIED','author':s.ACTOR['id'],
             'plan':pin(plan_path),'review':pin(review_path),'surfaces':results}))

if __name__=='__main__':
    {'prepare':prepare,'apply':apply}[sys.argv[1]]()
