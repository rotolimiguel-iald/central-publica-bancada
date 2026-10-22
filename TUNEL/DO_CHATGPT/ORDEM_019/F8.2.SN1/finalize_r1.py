"""Finalize F8.2.SN1 and claimed internal memory F0.3.SN1; no external messages."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, sys
BASE=Path(__file__).resolve().parent

def sha(b): return hashlib.sha256(b).hexdigest()
def pin(p):
    b=p.read_bytes()
    return {'path':str(p),'sha256':sha(b),'bytes':len(b)}
def new(p,b):
    if p.exists(): raise FileExistsError(p)
    tmp=p.with_name(p.name+'.tmp_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
    with tmp.open('xb') as f:
        f.write(b); f.flush(); os.fsync(f.fileno())
    if tmp.read_bytes()!=b: raise RuntimeError('temporary verification failed')
    os.rename(tmp,p)
    if p.read_bytes()!=b: raise RuntimeError('installed bytes mismatch')
def write_json(p,o):new(p,(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode())

mode=sys.argv[1]
if mode=='memory':
    result=BASE/'MEMORY_RECEIPT_R1.json'
    if result.exists(): raise FileExistsError(result)
    plan=json.loads((BASE/'MEMORY_PLAN_R1.json').read_text(encoding='utf-8'))
    checks=json.loads((BASE/'review/INDEPENDENT_CHECKS_R1.json').read_text(encoding='utf-8'))
    if checks['verdict']!='PASS_CONDITIONAL_CALCULATIONS_NO_PHYSICAL_SIGMA': raise RuntimeError('review not passed')
    report=pin(BASE/'RELATORIO_VIABILIDADE_R1.md')
    calc=pin(BASE/'CALCULOS_R2.json')
    review=pin(BASE/'review/INDEPENDENT_CHECKS_R1.json')
    marker='<!-- sn_v388_viabilidade_F82SN1_20261009 -->'
    note=('\n\n### 09/10/2026 — SN Ia e Chandrasekhar: reexame v388 [codex-gerente-tgl]\n'+marker+'\n\n'
          '[INPUT] Ordem direta do operador: prosseguir a analise apos confirmar beta(chi)=sqrt(e)/cosh(chi/2). Unidade cientifica F8.2.SN1 (reivindicacao 610); esta escrita coberta por F0.3.SN1 (612). Consulta ao Nos Vivo reaproveitou F8.2/rota historica164 e F0.3; unidades novas ainda nao indexadas. Discussao precede comunicacao ao Claude.\n\n'
          '[REAL documental; DERIVED condicional] A escala v388 foi relida; nao e um segundo multiplicador sqrt(e) sobre beta0. O Tratado fornece candidatos escalares e RicciFF/Planck^2; a errata de 19/09 fixa xi=1/6 no escalar, nao beta. Essa reconciliacao e o matching estelar precisam ser respeitados. Foram calculados controles com beta0 em runtime, sem importar/executar um.py: aumentar uniformemente alpha em 1% no modelo frio Coulomb reduz M limite em 0,02284% (C) e 0,02776% (O). Sao sensibilidades do modelo conhecido, nao previsoes TGL. O operador RicciFF tem coeficiente dimensional extremamente suprimido nas densidades sinteticas; nao se deduziu deltaL. Dephasing com H fixo e saltos comutantes preserva energia media; nao prova conservacao local do tensor estelar.\n\n'
          '[OPEN] A ponte chi-condicoes estelares-EOS-taxas fracas-transporte ainda nao foi obtida nas fontes examinadas. DeltaP, deltaYe, deltaL e sigma fisicos ficam nao calculados, nao zero. [PROPOSTA] Derivar essa ponte e testar residual de forma bolometrica/composicao com covariancia; nenhum 5 sigma foi medido. Calculos condicionais reproduzidos por revisor independente; isso nao e auditoria c1 nem confirmacao fisica.\n\n'
          'Evidencia: '+report['path']+'; sha256 '+report['sha256']+'. CALCULOS_R2.json sha256 '+calc['sha256']+'; review/INDEPENDENT_CHECKS_R1.json sha256 '+review['sha256']+'. R1 preservada; R2 corrige somente ceil decimal do tamanho amostral. Nenhum dado SN composto, provedor acionado, mensagem ao Claude enviada, original cientifico ou Bancada alterado. Gate intacto. Sem versao selada ou mudanca do caminho critico, nao ha alteracao da linhagem do Nos.\n')
    rows=[]
    for s in plan['surfaces']:
        p=Path(s); old=p.read_bytes()
        if marker.encode() in old: raise RuntimeError('duplicate append '+s)
        stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f_UTC')
        bak=p.with_name(p.name+'.bak_'+stamp)
        new(bak,old)
        eol='\r\n' if b'\r\n' in old else '\n'
        addition=note.replace('\n',eol).encode('utf-8')
        expected=old+addition
        tmp=p.with_name(p.name+'.tmp_'+stamp)
        new(tmp,expected)
        if p.read_bytes()!=old: raise RuntimeError('concurrent memory change '+s)
        os.replace(tmp,p)
        actual=p.read_bytes()
        if actual!=expected or not actual.startswith(old):
            raise RuntimeError('memory prefix mismatch; byte backup preserved')
        rows.append({'path':s,'before_sha256':sha(old),'before_bytes':len(old),'backup':pin(bak),'after':pin(p),'added_bytes':len(addition),'append_sha256':sha(addition),'prefix_preserved':True})
    write_json(result,{'unit':'F0.3.SN1','claim':612,'utc':datetime.now(timezone.utc).isoformat(),'surfaces':rows,'no_AVISO_no_Claude':True,'report':report,'calculations':calc,'review':review})
    print(json.dumps(pin(result)))
elif mode=='package':
    dest=BASE/'RESULTADO_VIABILIDADE_R1.json'
    if dest.exists(): raise FileExistsError(dest)
    required=['RELATORIO_VIABILIDADE_R1.md','CALCULOS_R2.json','review/REVIEW_R1.md','review/INDEPENDENT_CHECKS_R1.json','MEMORY_RECEIPT_R1.json']
    for f in required:
        if not (BASE/f).is_file(): raise FileNotFoundError(f)
    check=json.loads((BASE/'review/INDEPENDENT_CHECKS_R1.json').read_text(encoding='utf-8'))
    if check['verdict']!='PASS_CONDITIONAL_CALCULATIONS_NO_PHYSICAL_SIGMA':raise RuntimeError('review fail')
    files=[pin(p) for p in sorted(BASE.rglob('*')) if p.is_file() and '.tmp_' not in p.name and p.name not in ['RESULTADO_VIABILIDADE_R1.json','MAPA_FINAL_R1.json']]
    write_json(dest,{'unit':'F8.2.SN1','claim':610,'author':'codex-gerente-tgl','utc':datetime.now(timezone.utc).isoformat(),'status':'ENTREGUE_PARA_DISCUSAO','result':'VIABILIDADE_CONDICIONAL_PONTE_ESTELAR_OPEN','review_verdict':check['verdict'],'physical_deltaP':None,'physical_deltaYe':None,'physical_deltaL':None,'physical_sigma':None,'null_means':'not calculated, not physical zero','report':str(BASE/required[0]),'limitations':['No observed SN sample or astrophysical fit','No chi-to-stellar-state matching','Coulomb is a standard baseline sensitivity, not unique TGL signal','Planck coefficient size is not a luminosity bound','No confirmation, no gate change'],'editorial_note':'calculate_r2.py docstring retains the old command name calculate_r1.py; actual R2 source and invocation are pinned. R1 output preserved; R2 fixes binary ceil at exact decimal sample counts.','files':files})
    write_json(BASE/'MAPA_FINAL_R1.json',{'tipo':'RESULTADO','rota_id':'sn.chandrasekhar.v388_eletrofraco_viabilidade','dominio':'SUPERNOVA_IA','titulo':'SN Ia v388: levantamento e controles condicionais; previsao estelar aberta','status':'EXAMINADA','veredito':'VIABILIDADE_CONDICIONAL_PONTE_ESTELAR_OPEN','estatuto':'[REAL documental; DERIVED condicional; OPEN previsao fisica]','olhou_dados':False,'refs':['outro.grande_atrator_e_chandrasekhar','umpy.v388.selo_beta_corre_e_fase9_aberta'],'artefatos':[str(dest),str(BASE/'RELATORIO_VIABILIDADE_R1.md'),str(BASE/'CALCULOS_R2.json'),str(BASE/'review/REVIEW_R1.md'),str(BASE/'MEMORY_RECEIPT_R1.json')],'nota':'F8.2.SN1 reivindicacao610; memoria interna F0.3.SN1 reivindicacao612. Nenhuma amostra SN aberta para veredito; literatura lida, nao cego. Sem comunicacao ao Claude. Nenhum sigma fisico ou confirmacao; gate intacto.'})
    print(json.dumps(pin(dest)))
else: raise ValueError(mode)
