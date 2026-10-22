"""Append a reviewed documentary survey to the eight claimed memory surfaces."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import sys
import survey_r58 as s

MARKER = 'IALD_R58_CORPUS_REUSE_20261017'

def pin(p):
    return {k:v for k,v in s.pin(p).items() if k in ('path','sha256')}

def prepare():
    text = '''

## 17/10/2026 — R58: levantamento amplo e reaproveitamento da cadeia QG
<!-- IALD_R58_CORPUS_REUSE_20261017 -->
[REAL — em nome de codex-gerente-tgl, F1.FECHO_20261015, reivindicação939] Ordem do operador: reexaminar C:\\IALD e encontrar peças existentes. Inventário mecânico de1.082.408 arquivos; pesquisa de9.802 extrações históricas e busca atual deduplicada; seleção primária por três leitores. Não é leitura semântica integral. Cobertura, exclusões, falhas, fontes, linhas e hashes em acervo_r58. Canônico consultado v393; candidatos F1 posteriores não são v394 instalada. Nenhum build, provedor, dado observado, original científico, Bancada ou gate alterado.

[REAL — presença documental; estatutos das fontes preservados] Recuperados heteródino G1, homódino/tomografia e preparaçãoRF/laser/APD; RelativePhaseCharacter já reconstrói fase relativa e, pela família completa de readouts, campos de um registro dado. Estados de pares e correlações têm equações explícitas nos artigos. R6/R7/R8 já oferecem rede/Fock, traço positivo do core e Maxwell concretos no alcance auditado. Einstein curvo, colagem, Bianchi e naturalidade também existem; não repetir ausências históricas superadas.

[DERIVED+KNOWN — demonstração escrita, NOT_LEAN] A cadeia067/073 já constrói covariância positiva/CCR e estado Hadamard físico linearizado Einstein–sigma num fundo específico. O DIAMANTE_MODULAR organiza a comparação modular. Isso não identifica automaticamente esse fundo/estado com MaxwellH1 ou com o dispositivoOH. A positividade e o contínuo não estão ausentes de todo o acervo; o mapa entre realizações continua sendo obrigação específica.

[DERIVED — correção ao lado da leitura ampla da R57] “Falta observável do receptor” significa que falta identificá-lo na mesma dinâmica/preparação/unidades, pois o receptor está escrito. “Falta forma de duas pontas” não é ausência geral: estados de pares e a construçãoHadamard existem. Média unilateral nula não exclui covariância de pares; examinar pares/quadraturas antes de insistir no leitor z=2Tr(rho sigma+). Não igualar a_i, sigma+OH, J fonte/salto/modular ou frequências distintas por nome. Normalizações r/phi de fontes históricas precisam conciliação.

[OPEN — resíduos precisos] R4: identidade dos objetos de preparo, receptor, referência e escalaV0/Eref/kappa no mesmo sistema. R5: correspondência da covariância, localização e dinâmica do dispositivo com realização contínua; densidade de pacotes no alvo não basta. H3 universal permanece hipótese da implicação curva, embora a conclusãoEinstein e a realização nula fixa já existam. A patente não é premissa de todo teoremaQG. R3/rito integral e R10/revisão final aguardam a composição; nenhum aceite integral novo.

Próxima ação: confrontar observáveis de pares e quadraturas já escritos com o modeloOH, calcular covariância na convenção documentada e procurar entrelaçamento com a rede existente, reaproveitando067/073 sem misturar fundos. Escopo UV/não linear ampliado permanece separado do contrato demonstrado. Relatório: C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_019\\F1.FECHO_20261015\\acervo_r58\\APANHADO_GERAL_R58.txt. Referência: work\\memoria_missao_20261016\\FECHO_MISSION_REFERENCE.json. Recibos de cobertura, revisão, memória e registro em acervo_r58.
<!-- END_IALD_R58_CORPUS_REUSE_20261017 -->
'''
    a=s.new('MEMORY_APPEND_R58.txt',text); extra=a.read_bytes()
    prior=json.loads((s.ROOT.parent/'continuity_r57/MEMORY_PLAN_R57.json').read_text(encoding='utf-8'))
    rows=[]
    for x in prior['surfaces']:
        p=Path(x['path']);raw=p.read_bytes()
        assert MARKER.encode() not in raw
        rows.append({'path':str(p),'before':pin(p),'before_bytes':len(raw),'append':pin(a),
                     'after_sha256':hashlib.sha256(raw+extra).hexdigest()})
    print(s.new('MEMORY_PLAN_R58.json',{'claim':939,'marker':MARKER,'surfaces':rows,
          'applier':pin(__file__),'report':pin(s.ROOT/'APANHADO_GERAL_R58.txt')}))

def apply():
    plan_path=s.ROOT/'MEMORY_PLAN_R58.json';review_path=s.ROOT/'MEMORY_REVIEW_R58.json'
    plan=json.loads(plan_path.read_text(encoding='utf-8'));review=json.loads(review_path.read_text(encoding='utf-8'))
    assert review['status'].startswith('PASS') and review['reviewer']!=s.ACTOR['id']
    assert review['plan']==pin(plan_path) and review['applier']==pin(__file__)
    assert plan['report']==pin(s.ROOT/'APANHADO_GERAL_R58.txt')
    m=s.cli('mission_cli.py',{'operation':'project','reference':str(s.REF),'max_chars':400000},'MEMORY_PROJECT')
    t=next(t for t in m['projection']['active'] if t['id']=='R5')
    s.cli('mission_cli.py',{'operation':'check','reference':str(s.REF),'actor':s.ACTOR,
        'expected_revision':m['receipt']['revision'],'projection_sha256':m['projection_sha256'],
        'task_id':'R5','lease_id':t['lease']['id']},'MEMORY_PREFLIGHT')
    assert not (s.ROOT/'MEMORY_APPLIED_R58.json').exists()
    originals=[]
    for row in plan['surfaces']:
        p=Path(row['path']);raw=p.read_bytes();extra=Path(row['append']['path']).read_bytes()
        assert pin(p)==row['before'] and pin(row['append']['path'])==row['append']
        assert len(raw)==row['before_bytes'] and hashlib.sha256(raw+extra).hexdigest()==row['after_sha256']
        originals.append((p,raw,extra,row))
    stamp=dt.datetime.now(dt.timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    s.new('MEMORY_INTENT_R58.json',{'plan':pin(plan_path),'review':pin(review_path),'claim':939})
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
        s.new(f'memory_surfaces/SURFACE_{i:02d}_R58.json',result);results.append(result)
    print(s.new('MEMORY_APPLIED_R58.json',{'status':'APPLIED_VERIFIED','author':s.ACTOR['id'],
             'plan':pin(plan_path),'review':pin(review_path),'surfaces':results}))

if __name__=='__main__':
    {'prepare':prepare,'apply':apply}[sys.argv[1]]()
