"""Prepare distinct, source-bound units; the existing coordinator dispatches."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, uuid, sys

R=Path(__file__).resolve().parent
CHAT=R.parent
OUT=CHAT/'TUNEL/DO_CHATGPT'
D=R/'orchestration_final_stage'
sys.path.insert(0,str(R/'A7'))
from deliver_nonminimal_wick_and_mimo_audit import put,write,sha,append

def source(p,first=1,last=None):
    lines=p.read_text('utf-8-sig').splitlines()
    end=len(lines) if last is None else min(last,len(lines))
    meta=dict(path=str(p),sha256=sha(p),first_line=first,last_line=end,total_lines=len(lines))
    return '\nSOURCE '+json.dumps(meta,ensure_ascii=False)+'\n'+'\n'.join(f'{i+1}: {lines[i]}' for i in range(first-1,end))+'\n',meta

def main():
    D.mkdir(exist_ok=False)
    order=CHAT/'TUNEL/PARA_CHATGPT/ORDEM_015_continuacao_do_ringdown_rumo_ao_5sigma.md'
    common='''Missão ORDEM016, incluindo ParteB/ORDEM015. O operador pediu distribuir
tarefas em26/09 para preservar a cota da bancada e autorizou Antigravity em
baixa complexidade. Sua resposta é contribuição textual DECLARADO, nunca
prova de execução. A memória científica comum será anexada pelo adaptador.
Não executar comandos nem alegar acesso ao disco. Não ler segredos, semente
cega, acervo jurídico nem outros arquivos. Não alterar originais/kernel/gate.
Uma pergunta delimitada por unidade, uma chamada. Entregar resultado concreto,
com referências às linhas fornecidas e lacunas explícitas; não recontar a missão.
'''
    units=[
      ('kimi','skeptic','C2.2','critique_current_width_v2',
       '''Critique a prova ATUAL WidthFromContraction_v2 e a fronteira exata
entre o critério analítico provado e IsotonyImpliesStripMultiplierCriterion.
A chamada antiga1ceac5cf terminou em timeout antes desta versão; NÃO reabrir
a unidade antiga. Esta unidade recebe a prova nova, sem hipótese w<2pi,
e deve responder: o relatório atual exagera alguma implicação ou omite hipótese?
Se houver falha, dê contraexemplo/enunciado corrigido; se não, registre o
escopo válido e a necessidade que segue sem prova. Não elaborar novo ramo
de pesquisa, não alegar compilação. A evidência de compilação é da bancada.''',
       [(R/'C2/WidthFromContraction_v2.lean',1,None),
        (R/'A2/LightRayTwistWidth_v3.lean',1,None),
        (R/'A2/LightRayCoreExtension_v2.lean',1,None),
        (R/'C2/RESULTS.json',1,None),(R/'C2/AXIOM_AUDIT.json',1,None),
        (R/'C2/RELATORIO.md',1,None)]),
      ('mimo','draft','B.T01.g','reach_table_metadata_correction',
       '''Como implementar a correção T01(g) em um script Python novo,
preservando todos os números/fontes do quadro existente? Entregue um módulo
executável (texto) que leia QUADRO_DE_ALCANCE_V1.json e emita _v2.json/.md
ao lado por escrita exclusiva, acrescente supersedes/hash lido, resolva cada
JSON pointer contra a fonte e confira sha. Taxa/IC somente30célulasO4_HOJE,
com categoria/exposição das rate_contexts; demais OPEN com reason.
Campos inexistentes não viram zero. Os20ponteiros ausentes devem receber
NO_FIELD_IN_SOURCE__OPEN_NO_UNIQUE_LOCAL_DTAU. Não importar o gerador antigo
com efeitos nem executar ciência. Inclua controles de ponteiro ausente,
hash adulterado e taxa indevida em grupo futuro. A bancada fará execução.''',
       [(order,208,226),
        (CHAT/'ORDEM_013_RINGDOWN/bis/e6_prepare_v3/generate_reach_table.py',1,None)]),
      ('deepseek','draft','B.T03','registration_v11_guard_contract',
       '''Entregue o rascunho concreto da guardaV1.1 da T03(x/xi) e seus
probes negativos como códigoPython, preservando a API pública da guardaV1.
Prioridade: estatísticaV1 imutável, cadeias consecutivas sem buracos,
testemunhas/cronologia, relógioR7 separado, calibração versus blind_test,
árvores e pinos, idsV1 nunca relançados. Não reproduzir check_activationV1
como autorizaçãoV1.1. Não relaxar guarda para conseguir executar.
Use funções puras separadas do I/O para testes. Marque dependências do
reciboR5 e da testemunha ainda ausentes. Não emitir registro real nem ler
semente. A bancada integrará junto aos demais leitores e verificará.''',
       [(order,105,112),(order,238,260),
        (CHAT/'ORDEM_013_RINGDOWN/bis/e2_code/registration_guard.py',1,None),
        (CHAT/'ORDEM_013_RINGDOWN/bis/e2_code/null_runner.py',1,90),
        (CHAT/'ORDEM_013_RINGDOWN/bis/e2_code/null_campaign.py',1,70)]),
      ('antigravity','skeptic','B.T01.h','documentary_statute_inventory',
       '''Tarefa de baixa complexidade, somente conferência documental:
produza uma tabela de correções exigidas por T01(h), ligando cada correção
à frase/linha fornecida; indique o que não é verificável nos excertos.
Proponha texto curto dos adendos de primeira linha B1/B2/E2 e da comparação
NÃO-CEGA da B3. Não calcular estatística, não derivar física, não inventar
hashes; use somente os hashes nos cabeçalhosSOURCE. Nada se considera
implementado por seu parecer. Identifique lacunas, sem pedir acesso extra.''',
       [(order,210,226),
        (OUT/'ENTREGA_013BIS_B1_portao_e_nuisance.md',1,80),
        (OUT/'ENTREGA_013BIS_B2_registro_e_440.md',1,80),
        (OUT/'ENTREGA_013BIS_E2_REGISTRO_V1.md',1,60),
        (OUT/'ENTREGA_013BIS_B3_piloto_e_orcamento.md',1,85)])]
    catalog=[]
    for provider,role,branch,lemma,question,paths in units:
        prompt=common+'\n'+question+'\n';refs=[]
        for p,first,last in paths:
            text,ref=source(p,first,last);prompt+=text;refs.append(ref)
        rid=str(uuid.uuid4())
        constraints=dict(mission_id='ORDEM_016',branch_id=branch,lemma_id=lemma,
                         role=role,required_provider=provider,max_calls=1)
        if provider in ('mimo','deepseek'):
            constraints.update(max_cost_usd=None,max_output_tokens=131072 if provider=='mimo' else 393216)
        path=D/(provider+'_submit.json')
        put(path,dict(operation='submit',request_id=rid,prompt=prompt,execution_constraints=constraints))
        catalog.append(dict(provider=provider,request_id=rid,branch=branch,
            payload=str(path),payload_sha256=sha(path),prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(),
            chars=len(prompt),sources=refs,status='PREPARED_NOT_SUBMITTED'))
    put(D/'prepared_units.json',catalog)
    now=datetime.now(timezone.utc).isoformat()
    put(D/'ORIGIN.json',dict(at=now,thread_id='01a070fc-9484-7e13-a654-c6b5f61093a4',
        authorization=['distribua as tarefas para nossas IA\'s para preserva a sua cota para não acabar novamente antes de terminarmos por completo o nosso trabalho',
        'vc tem também o antigravity para tarefas de baixa complexidade que também pode ser usado'],
        old_C22_terminal_preserved=True,C6_not_reopened=True))
    append(OUT/'LEDGER_016.jsonl',''.join(json.dumps(dict(at=now,event='EXTERNAL_UNIT_PREPARED',
        provider=u['provider'],request_id=u['request_id'],target=u['branch'],
        prompt_sha256=u['prompt_sha256'],payload_sha256=u['payload_sha256'],external_call=False))+'\n' for u in catalog))
    print(json.dumps([{k:v for k,v in u.items() if k!='sources'} for u in catalog],indent=2))

if __name__=='__main__':main()
