"""Freeze the additive A5/A6 protocol before numerical or Lean experiments."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os

B = Path(__file__).resolve().parent
P = B.parent
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def create(p, content):
    data = content if isinstance(content, bytes) else content.encode('utf-8')
    if p.exists():
        raise FileExistsError(p)
    tmp = p.with_name(p.name + '.tmp')
    with tmp.open('xb') as f:
        f.write(data); f.flush(); os.fsync(f.fileno())
    assert tmp.read_bytes() == data
    os.rename(tmp, p)
def js(x):
    return json.dumps(x, ensure_ascii=False, indent=2, allow_nan=False) + '\n'

targets = [B/n for n in ('PREREGISTRO_ADENDO1_R1.json','PREREGISTRO_ADENDO1_R1.md','FREEZE_ADENDO1_R1.json','MAPA_PREREGISTRO_ADENDO1_R1.json')]
assert not any(p.exists() for p in targets)
custody = json.loads((B/'sources/CUSTODIA_VERBATIMS_R1.json').read_bytes())
for s in custody['sources']:
    assert sha(Path(s['source'])) == sha(Path(s['custody'])) == s['sha256']
    assert s['verbatim_utf8'].encode('utf-8') == Path(s['source']).read_bytes()
protocol = {
 'schema':'F1.ATRATOR.ADENDO1.preregister/v1',
 'created_utc':datetime.now(timezone.utc).isoformat(), 'claim':668,
 'author':'codex-gerente-tgl; revisão matemática prévia independente atrator_skeptic',
 'status':'PREREGISTERED_BEFORE_NEW_TESTS',
 'constraints':['sandbox only','no production Bench','no kernel or um.py changes','no observed data','no gate','new files only'],
 'verbatims':custody['sources'],
 'verbatim_statute':'INPUT: ordem/cunhagem; ONTO: conteúdo universal; nenhuma frase citada é promovida por inclusão documental',
 'reuse':[{'path':str(p),'sha256':sha(p)} for p in [P/'PREREGISTRO_R1.json',P/'RESULTADO_F1_ATRATOR_R1.json',P/'numerical/RESULTADOS_NUMERICOS_R3.json',B/'review/REVISAO_PREVIA_R1.json',B/'lean_survey/SOURCE_HASHES_R1.json',B/'lean_survey/ERRATA_LINHAS_R1.md']],
 'prior_knowledge':'O controle identidade da R1 já preserva A1–A3 e falha A4. O resultado provável A6=FALHA é declarado antes da nova rodada; teste sintético não cego e sem ajuste ao dado.',
 'mapping':{
   'statute':'INPUT da gerência: retirar T/G/L; tradução operacional abaixo proposta e fixada pela coordenação antes do teste',
   'T':'Propagador de estados/populações; retirar evolução significa GERADOR zero, logo propagador identidade. Não confundir com mapa zero.',
   'G':'Espaço H não trivial e conjunto de estados normalizados; controle afim sem ponto fixo fora da classe linear/CPTP, controle de suporte vazio inadmissível.',
   'L':'Leitura intrínseca R=projeção ortogonal em Fix(T). β=0 é proxy solicitado de transmissão total; não apaga o conjJ canônico. Retirar R fornecido é ausência de interface, não ausência matemática.',
   'A5_reading':'No Pair real canônico: AdJ(F)(p)=conjJ(F(conjJ(p))); E_J(F)=(F+AdJ(F))/2. ConjJ é a troca; pairK(d) é diag(d,-d). E_J é leitura SOBRE operadores; R de A1–A4 age SOBRE estados.',
   'regimes':'Convergência somente na dinâmica de estados. A leitura angular observing_adds_nothing conserva seu tipo e não recebe limite nem identificação com E_J por homônimo.'},
 'A5':{
   'primary':['J²=I','JKJ=-K','AdJ(J)=J','E_J(J)=J','E_J²=E_J','AdJ E_J=E_J AdJ=E_J','E_J(K)=0','E_J(I)=I'],
   'finite_face':'n=1 Pair; J=[[0,1],[1,0]], K=diag(1,-1). Matrizes complexas somente complexificação finita da mesma representação real, não J antiunitário de Tomita.',
   'falsifier':'Com J e K satisfazendo as hipóteses, qualquer identidade primária falha além da tolerância ou a construção requer parâmetro independente de leitor. Recusa de hipótese não é falsificação da implicação.',
   'limitations':['J∘J=I e não J: diagnóstico literal deve FALHAR','E_J fixa I e J e tem dimensão fixa 2; não é o R de dimensão1 da A4','autoconjugação isolada é identidade algébrica, não testemunho empírico discriminante','não se prova ontologia nem ausência física de observador'],
   'controls':['K=I viola JKJ=-K e E_J(K)=0, embora a autoleitura de J sobreviva','J_bad=2J sob a mesma fórmula J_bad A J_bad: falha involução/esperança; classificar hipótese recusada, não Ad com inversa']},
 'A6':{
   'target':'Necessidade de cada T/G/L para A1 ∧ A2 ∧ A3. Um caso admissível que preserve a conjunção produz FALHA; não acrescentar A4 ou movimento não trivial depois.',
   'reading_after_ablation':'Recalcular R intrínseco do espaço fixo APÓS intervenção. Guardar R antigo errado como diagnóstico secundário, sem usá-lo como prova de minimalidade.',
   'cases':[
     {'id':'T_zero_generator','T':'I_2','R':'I_2','admissible':True},
     {'id':'T_zero_boundary_angle','S':'I_2 (theta=0)','T':'I_2 nas populações; D nas densidades','R':'I_2 ou D respectivamente','admissible':True},
     {'id':'L_beta_zero','beta_ablation':0,'T':'I_2 nas populações; D nas densidades','R':'I_2 ou D respectivamente','admissible':True,'note':'0 é valor da intervenção, nunca beta_TGL literal'},
     {'id':'L_missing_supplied_readout','T':'primário intacto','R':'reconstruído de Fix(T) por SVD; R fornecido ausente','admissible':True,'note':'Sobrevivência do objeto; interface sem R é RECUSA de avaliação, não FALHA matemática'},
     {'id':'G_no_fixed_point','T':'x -> x+1 em R','R':None,'admissible':False,'note':'Controle externo; iterar 4096 passos e médias, A1 falha; A2/A3 não aplicáveis'},
     {'id':'G_no_support','T':'espaço zero','R':'zero-dimensional','admissible':False,'note':'Sem estado de traço1; RECUSA_NAO_VACUIDADE, identidades vazias não são evidência'},
     {'id':'diagnostic_old_R_on_identity','T':'I_2','R':'ones(2,2)/2 antigo','admissible':False,'note':'A1 e A3 da projeção falham; atribuição errada de R, não refutação da projeção intrínseca'}],
   'falsifier':'Qualquer caso admissível de retirada preserva A1–A3. Relatar a dimensão fixa separadamente; A4 não substitui o alvo.',
   'outside_scope':'A tríade como célula unitária da realidade permanece ONTO.'},
 'numeric':{'dtype':'float64/complex128','seed':20261010,'random_operators':256,'norm':'Frobenius/Euclidean','atol':1e-10,'rtol':1e-10,'rank_threshold':1e-10,'ambiguous_singular_band':[5e-11,2e-10],'powers':[0,1,2,8,32,128,512,1024,4096],'finite_required':True,'nonfinite':'RECUSA','beta_runtime':'ALPHA_FINE_CODATA_2018 * sqrt(e), unique canonical assignment and sealed wrapper cross-check; never import/execute um.py','primary_channel':'S=[[sqrt(1-b),sqrt(b)],[-sqrt(b),sqrt(1-b)]]; C=D Ad(S) D; population T=abs(S)^2','projection':'SVD null(T-I), U U*; rank ambiguous => RECUSA','A1_finite_test':'Contraction finite primary or exact idempotent ablation; powers test plus exact formulas; finite iterations alone do not prove universal convergence'},
 'lean':{'toolchain':'4.31.0','readonly_LEAN_PATH':'kernel .lake/build/lib/lean plus .lake/packages/*/.lake/build/lib/lean','sandbox_outputs_only':True,'axioms_allowed':['propext','Classical.choice','Quot.sound'],'sorry':0,'new_stones':['original A1–A4 body preserved with full verbatim docstring in new file','A5 same Pair/conjJ and A6 identity counterexample with full verbatim docstring'],'independent_review':True},
 'verdict':'A1–A4 retain R1 scope; A5 PASSA/FALHA for explicitly mapped algebra; A6 PASSA/FALHA for operational minimality, refusals separately. Validity in tested face, never creditação.'
}
create(targets[0],js(protocol))
md = '# F1.ATRATOR — ADENDO1: pré-registro A5/A6\n\n'
md += '[INPUT — protocolo] Reivindicação 668. Versão aditiva; leitura e revisão prévias concluídas, nenhum ensaio novo executado. O JSON ao lado é o contrato integral dos testes.\n\n'
md += '## Mapeamento, hipóteses e falsificadores\n\n```json\n' + js({k:protocol[k] for k in ('prior_knowledge','mapping','A5','A6','numeric','lean','verdict')}) + '```\n\n'
md += '## Cunhagens integrais [INPUT/ONTO]\n\nOs delimitadores pertencem ao documento; entre eles estão os bytes exatos das fontes, sem normalização.\n\n'
for s in custody['sources']:
    md += f"### {s['id']} — SHA256 {s['sha256']}\n\nFonte: `{s['source']}`\n\n[BEGIN VERBATIM {s['id']}]\n" + s['verbatim_utf8'] + f"\n[END VERBATIM {s['id']}]\n\n"
create(targets[1],md)
insertions=[]
for s in custody['sources']:
    raw=Path(s['source']).read_bytes(); b=targets[1].read_bytes(); i=b.index(raw)
    assert b[i:i+len(raw)] == raw
    insertions.append({'source':s['id'],'sha256':s['sha256'],'byte_range':[i,i+len(raw)]})
freeze={'created_utc':datetime.now(timezone.utc).isoformat(),'before_new_experiments':True,'files':[{'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size} for p in targets[:2]],'verbatim_insertions':insertions,'generator_sha256':sha(Path(__file__))}
create(targets[2],js(freeze))
entry={'tipo':'ANOTACAO','rota_id':'formal.singularidade_le_atrator','dominio':'FORMAL','titulo':'F1.ATRATOR ADENDO1: verbatims e pré-registro A5/A6','status':'EM_CURSO','estatuto':'INPUT protocolo; ONTO cunhagens; DERIVED desenho','olhou_dados':False,'refs':['formal.singularidade_le_atrator'],'artefatos':[str(p) for p in targets[:3]],'nota':'A5 média da conjugação tipada no Pair; A6 admite contraexemplo identidade/β=0 preservando A1–A3. Sem ensaios novos antes deste freeze; sem produção/gate. Reivindicação668.'}
create(targets[3],js(entry))
print(js(freeze))
