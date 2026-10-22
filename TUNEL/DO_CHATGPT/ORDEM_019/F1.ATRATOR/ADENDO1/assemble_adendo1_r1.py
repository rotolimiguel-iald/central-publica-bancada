"""Assemble verified immutable evidence; does not run scientific tests or deploy."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os

B=Path(__file__).resolve().parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p): return {'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
def create(p,data):
    data=data if isinstance(data,bytes) else data.encode('utf-8')
    if p.exists(): raise FileExistsError(p)
    tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:
        f.write(data); f.flush(); os.fsync(f.fileno())
    assert tmp.read_bytes()==data
    os.rename(tmp,p)
def js(obj): return json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n'

def main():
    outputs=[B/n for n in ('RELATORIO_ADENDO1_R1.md','VERBATIM_INSERTIONS_FINAL_R1.json','RESULTADO_ADENDO1_R1.json','MAPA_ENTREGA_ADENDO1_R1.json')]
    assert not any(p.exists() for p in outputs)
    cfg=json.loads((B/'ASSEMBLY_INPUTS_R1.json').read_bytes())
    assert cfg['independent_review_passed'] is True
    evidence=[]
    for row in cfg['evidence']:
        p=Path(row['path']); assert sha(p)==row['sha256'];evidence.append(pin(p))
    freeze=json.loads((B/'FREEZE_ADENDO1_R1.json').read_bytes())
    for row in freeze['files']: assert sha(Path(row['path']))==row['sha256']
    old=json.loads((B.parent/'HASHES_ENTREGA_R1.json').read_bytes())
    for row in old['files']: assert sha(Path(row['path']))==row['sha256']
    custody=json.loads((B/'sources/CUSTODIA_VERBATIMS_R1.json').read_bytes())
    for s in custody['sources']:
        assert sha(Path(s['source']))==sha(Path(s['custody']))==s['sha256']
    text='''# F1.ATRATOR — ADENDO1: cunhagens integrais, A5 e A6

Autor: codex-gerente-tgl, sob reivindicação 668. Entrega para auditoria da c1. Arquivos anteriores preservados; nenhum provedor chamado. O pré-registro está na seq 1002 do mapa e foi congelado antes dos novos ensaios.

## Resultado item a item

| Item | Veredito | Alcance |
|---|---|---|
| A1 | PASSA, alcance R1 | Cesàro no Hilbert geral sob a hipótese; convergência forte no canal finito dissipativo. |
| A2 | PASSA, alcance R1 | RT=TR=R. |
| A3 | PASSA, alcance R1 | R²=R e projeção sobre Fix(T); letra normalizada reaproveitada. |
| A4 | PASSA CONDICIONAL, alcance R1 | Dimensão fixa1 sob contração estrita no complemento de vetor fixo não nulo; sem hipótese há dimensão2. |
| A5 | PASSA NO MAPEAMENTO DECLARADO | E_J=(Id+AdJ)/2, E_J²=E_J, E_J(J)=J e E_J(K)=0. |
| A6 | FALHA DA MINIMALIDADE OPERACIONAL | Gerador zero e transmissão total preservam A1–A3 com a projeção intrínseca recalculada. |

[REAL] Os ensaios são sintéticos e as provas são candidatas de sandbox. [ONTO] A leitura universal, a célula unitária da realidade e o nome Luz conservam o estatuto da cunhagem. Nenhuma significância física ou creditação foi obtida.

## A5: a operação que foi testada

[INPUT — tradução operacional fixada antes da rodada] No Pair real do kernel, J=conjJ troca as componentes; K=pairK(d). A leitura atua sobre funções/operadores: AdJ(F)=J∘F∘J e E_J(F)=(F+AdJ(F))/2. O caso matricial usa a mesma troca real em dimensão2; não se presume o J antiunitário geral de Tomita.

[REAL/DERIVED — análise técnica, não citação do autor] J²=I permite provar que AdJ é involutiva e E_J é idempotente. JKJ=−K entra na prova de E_J(K)=0. E_J(J)=J fecha sem parâmetro independente de leitor. A autoconjugação isolada de J é uma identidade algébrica; ela não discrimina uma teoria física. O produto simples J² devolve I e o teste de J²=J falha para a troca não trivial.

E_J fixa I e J; sua imagem em M₂ tem dimensão2. A projeção R de A1–A4 atua sobre estados e tem dimensão1 sob a hipótese. Não há igualdade afirmada entre esses objetos. observing_adds_nothing é reaproveitado com seu tipo angular próprio; a leitura angular não recebeu limite.

## A6: retiradas e falsificador

[INPUT da gerência — implementação operacional explicitada no pré-registro] T designa a evolução, G o suporte e L a leitura/transmissão. Retirar o gerador de evolução dá T=I. Toda trajetória fica constante, Fix(T)=H e R=I; A1, A2 e A3 continuam verdadeiras. Assim a condição universal de minimalidade é falsa nesta tradução.

Na intervenção β=0, S=I. Nas populações o canal é I; mantendo a descoerência nas densidades, o canal é D e sua projeção é D. A1–A3 sobrevivem, com dimensão fixa2. θ=0 e β=0 coincidem aqui: não são evidências independentes de retirada de T e L. β=0 é um controle e não redefine β_TGL, calculado em runtime. A intervenção tampouco remove o J canônico.

Apagar R da interface deixa a entrada incompleta, mas a projeção intrínseca pode ser reconstruída do canal. O suporte vazio é recusado pela ausência de estado normalizado. O controle afim x↦x+1 não tem ponto fixo, falha A1 e está fora da classe linear/CPTP. Manter o antigo R de dimensão1 sobre T=I gera um leitor incorreto; isso não prova inexistência de outra leitura. Esses diagnósticos não são convertidos em evidência favorável à minimalidade.

[DERIVED] O resultado negativo delimita este mapeamento da tríade. A exigência de dissipação para convergir a um único estado normalizado corresponde ao alcance de A4; ela não pode ser acrescentada depois ao alvo A1–A3 de A6. A ontologia universal não foi testada.

## Reaproveitamento e revisão

R1 forneceu A1–A4, MeanErgodic, PALAVRA/letra normalizada e os controles de dimensão2. O levantamento do ADENDO1 abriu ConjugateAct, DecisionCommutation, LightIsJ e TheObserverReadsTheAngle; hashes e linhas estão em lean_survey, inclusive a errata aditiva de duas âncoras. Não se reconstruiu o que já existia.

O Atlas §I.5 (linhas632–641 no retrato consultado) orientou a busca por J/K; o Índice Vivo, linha5769, preserva o alcance da releitura angular. A fonte formal foi conferida no tipo concreto. A ressalva sobre flatK=0 em TheTwoPairings está no levantamento: K=0 também satisfaz JKJ=−K, portanto esse exemplo não prova indispensabilidade da anticomutação.

'''
    text+='### Medidas e builds desta camada\n\n'+cfg['verified_summary_markdown']+'\n\n'
    text+='### Evidências principais\n\n'
    for row in evidence:
        text+=f"- `{row['path']}` — SHA256 `{row['sha256']}`.\n"
    text+='\n## Quatro cunhagens integrais, sem paráfrase [INPUT/ONTO]\n\nOs delimitadores abaixo são do relatório. Cada intervalo interno reproduz os bytes originais; a matriz de offsets está em VERBATIM_INSERTIONS_FINAL_R1.json. O texto técnico anterior é interpretação matemática, não substituição dos verbatims.\n\n'
    for s in custody['sources']:
        text+=f"### {s['id']} — SHA256 {s['sha256']}\n\nFonte: `{s['source']}`\n\n[BEGIN VERBATIM {s['id']}]\n"+s['verbatim_utf8']+f"\n[END VERBATIM {s['id']}]\n\n"
    create(outputs[0],text)
    targets=[B/'PREREGISTRO_ADENDO1_R1.md',outputs[0]]+[Path(p) for p in cfg['verbatim_lean_files']]
    insertions=[]
    for p in targets:
        data=p.read_bytes()
        for s in custody['sources']:
            raw=Path(s['custody']).read_bytes(); i=data.index(raw)
            assert data[i:i+len(raw)]==raw
            insertions.append({'artifact':str(p),'artifact_sha256':sha(p),'source':s['id'],'source_sha256':s['sha256'],'byte_range':[i,i+len(raw)],'exact_bytes':True})
    create(outputs[1],js({'created_utc':datetime.now(timezone.utc).isoformat(),'insertions':insertions,'all_exact':True}))
    result={'unit':'F1.ATRATOR','layer':'ADENDO1_R1','claim':668,'author':'codex-gerente-tgl','created_utc':datetime.now(timezone.utc).isoformat(),'management_status_requested':'ENTREGUE','claims':{**{f'A{i}':{'verdict':'PASSA_NO_ESCOPO_R1','evidence':str(B.parent/'RESULTADO_F1_ATRATOR_R1.json')} for i in range(1,5)},'A5':{'verdict':'PASSA_NO_MAPEAMENTO_DECLARADO','literal_J_squared_equals_J':'FALHA','ontology':'ONTO'},'A6':{'verdict':'FALHA_MINIMALIDADE_OPERACIONAL','counterexample':'T=I,R=I; beta=0 preserves A1-A3','ontology':'ONTO'}},'independent_review_passed':True,'evidence':evidence,'report':pin(outputs[0]),'verbatim_insertions':pin(outputs[1]),'previous_delivery_integrity':{'checked':len(old['files']),'all_match':True},'preregister':pin(B/'PREREGISTRO_ADENDO1_R1.json'),'physical_sigma':None,'gate_changed':False,'production_changes':False,'ontology_promoted':False,'integration':'NONE; c1/operator general bench consolidation','notes':cfg.get('notes',[])}
    create(outputs[2],js(result))
    entry={'tipo':'RESULTADO','rota_id':'formal.singularidade_le_atrator','dominio':'FORMAL','titulo':'F1.ATRATOR ADENDO1: A5 passa; A6 falha na minimalidade operacional','status':'ENTREGUE','estatuto':'REAL no sandbox; ONTO cunhagens universais','veredito':'A5_PASSA_TIPADO__A6_FALHA_MINIMALIDADE','olhou_dados':False,'refs':['formal.singularidade_le_atrator'],'artefatos':[str(p) for p in outputs[:3]],'nota':'Quatro verbatims integrais por hash no preregistro/docstrings/relatorio; Lean e numerico revisados. T=I e beta=0 preservam A1-A3, com R recalculado. Reivindicação668; sem produção/gate. Integração futura é da gerência.'}
    create(outputs[3],js(entry))
    print(js({'result':pin(outputs[2]),'report':pin(outputs[0]),'insertions':len(insertions)}))

if __name__=='__main__':main()
