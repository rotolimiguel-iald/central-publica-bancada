"""Assemble three scoped reviews after successful independent recompilations."""
from pathlib import Path
import datetime,hashlib,json,re
B=Path(__file__).resolve().parent;P=B.parent
def pin(p):
 p=Path(p);b=p.read_bytes();return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def read(p):return json.loads(Path(p).read_bytes())
def put(p,v):
 b=(json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode() if isinstance(v,dict) else v.encode()
 with p.open('xb') as f:f.write(b)
 assert p.read_bytes()==b
allp=B/'all_local/RECEIPT_R1.json';audit=read(allp)
assert audit['passed'] is True and audit['exit_code']==0
groups={
 'TOMITA':{'names':['inclusion','finite','equality'],'prefixes':['F1Fecho.ExponentialTomitaInclusion','F1Fecho.WeylFiniteAlgebra','F1Fecho.ExponentialTomitaEquality'],
 'finals':['gamma_unbounded/FINAL_TOMITA_INCLUSION_RECEIPT_R1.json','gamma_unbounded/FINAL_WEYL_FINITE_ALGEBRA_RECEIPT_R1.json','gamma_unbounded/FINAL_TOMITA_EQUALITY_RECEIPT_R1.json','star_graph_density/FINAL_STAR_GRAPH_DENSITY_RECEIPT_R1.json','star_graph_root_review_r1/REVISAO_STAR_GRAPH_ROOT_R1.json'],
 'verdict':'PASSA_COMPOSICAO_TOMITA_COM_AUTORIA_AUXILIAR_EXPLICITA',
 'findings':['O domínio e o grafo da inclusão Sexp⊆S_par são efetivos no Fock canônico, obtidos pelo core conjunto F×F, não por densidade somente na primeira coordenada.','finiteAlgebra é de fato a span complexa dos Weyl de KWR: unidade, produto por CCR e estrela são provados, sem campo abstrato de álgebra fornecida.','finite_algebra_graph trata corretamente a conjugação escalar de Sexp; o par (aΩ,a*Ω) usa uma subestrutura REAL na separação do grafo.','A inclusão inversa usa densidade de dois vetores no bicomutante e fecho do grafo de Sexp. closure_minimal e a identidade do grafo fechado do par produzem igualdade dos grafos, domínios e ações.','A representação Fock, o vácuo e KWR são os mesmos objetos dos componentes concretos anteriores. Nenhuma nova hipótese de densidade, igualdade ou core é introduzida no consumidor final.'],
 'authorship':'StarGraphDensityR3 e BicommutantStarGraphR1 foram construídos por este revisor. Esta revisão NÃO é independente para esses dois componentes; a raiz os reviu separadamente, junto com BicommutantTwoVectorR2, no recibo REVISAO_STAR_GRAPH_ROOT_R1.json: três EXIT 0 e 61 declarações no trio. O parecer aqui avalia os três consumidores novos do outro construtor e suas recompilações.',
 'open':['Auto-adjunção de G=canonicalLift.','Identificação de G com o fator polar positivo, grupo modular Γ(B0) e KMS.','Habitante do contrato físico/analítico conjunto.']},
 'DUALIDADE':{'names':['duality'],'prefixes':['F1Fecho.OneParticleDuality'],
 'finals':['weyl_net_wiring/attempts/20261015T193303_165516Z/RECEIPT.json'],
 'verdict':'PASSA_DUALIDADE_SIMPLECTICA_EM_H1',
 'findings':['symplectic_tomita_pairing usa o domínio verdadeiro de TW e a decomposição x=h+ik com h,k fixos por SW; não assume uma decomposição de todo H1 fora do domínio.','O pareamento real no complemento simplético implica o pareamento de adjunto. generic_adjoint_maximal usa a auto-adjunção já provada de TW para obter Jg no domínio e TW(Jg)=g.','A involução de J e o critério KWR_mem fornecem J(KWR)=KWR′ como igualdade exata de conjuntos, completando a inclusão anterior.','São quatro teoremas concretos em H1, sem hipótese adicional de dualidade Haag nem identificação polar no Fock.'],
 'authorship':'Fonte construída pela raiz; leitura e recompilação independentes por codex-atrator-skeptic.',
 'open':['Esta igualdade em H1 não é, sozinha, identificação do operador polar Γ(J) no Fock.','KMS e contrato conjunto continuam fora deste componente.']},
 'PESO_E_ADAPTADOR':{'names':['weight','traced'],'prefixes':['F1Fecho.CanonicalFockWeight','F1Fecho.NetworkTracedCore'],
 'finals':['takesaki_fock/FOCK_DUAL_WEIGHT_RECEIPT_R1.json','takesaki_fock/TRACED_CORE_ASSEMBLY_RECEIPT_R1.json'],
 'verdict':'PASSA_PESO_ESCALAR_E_ADAPTADOR_CONDICIONAL',
 'findings':['PositiveInput é o cone positivo do core concreto em L²(ℝ;Fock); regularFockVacuum usa o mesmo vacuum, com norma 1 e não nulidade provadas.','weight é a integral quadrática dual efetiva no vetor especificado. Aditividade, homogeneidade não negativa, monotonicidade e invariância dual são consumidas dos teoremas genéricos V350.','weight_one=∞ e weight_zero=0 provam não nulidade do peso e do cone; não provam a existência de elemento de peso estritamente positivo finito.','weight_monotone_strong_limit preserva o supremo de uma rede positiva crescente sob a hipótese tipada de convergência forte para S. Não se substitui a hipótese por mera convergência verbal.','O adaptador fornece Core, instâncias, embedding fiel e dualAction por termos no mesmo core, usando D.wedge_glue. O traço, suas leis, projeção finita, divisão, KMS e Tomita analítico continuam campos explícitos.','A fonte do adaptador não importa nem usa o novo peso como traço: o peso é invariante, enquanto o traço exigido escala por exp(-s). A distinção é correta.'],
 'authorship':'Fontes construídas por tempo_math_review; leitura e recompilação independentes por codex-atrator-skeptic.',
 'open':['Fidelidade e semifinitude deste peso escalar.','Traço com lei exp(-s), sua implementação modular e equivalência com a torre V351.','Habitante de RemainingTracedCoreInput e do certificado conjunto.']}}
summaries=[]
for label,g in groups.items():
 builds=[];sources=[];printed=0;theorems=0
 for name in g['names']:
  rp=B/name/'RECEIPT_R1.json';r=read(rp)
  assert r['passed'] is True and r['exit_code']==0 and r['source_exact_copy']
  assert all(set(v)<={'propext','Classical.choice','Quot.sound'} for v in r['axioms'].values())
  for key in ['source','stdout','stderr','olean','log']:assert pin(r[key]['path'])==r[key]
  builds.append({'name':name,'receipt':pin(rp),'exit_code':r['exit_code'],'seconds':r['seconds'],'printed_axioms':r['axiom_count'],'olean_identical':r['olean_identical_to_accepted']})
  printed+=r['axiom_count'];sources.append(r['source'])
  theorems+=len(re.findall(r'^theorem\s',Path(r['source']['path']).read_text(encoding='utf-8'),re.M))
 count=sum(audit['counts'][p] for p in g['prefixes'])
 report={'unit':'F1.FECHO_20261015','claim_event':845,'reviewer':'codex-atrator-skeptic','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'verdict':g['verdict'],'material_findings':[],'authorship_and_independence':g['authorship'],'mathematical_findings':g['findings'],'open':g['open'],'builds':builds,'printed_axioms_total':printed,'explicit_theorem_count':theorems,'all_local_declarations':count,'all_local_audit':pin(allp),'sources':sources+[pin(P/f) for f in g['finals']],'script':pin(__file__),'scope':'Termos de sandbox compilados; nenhuma confirmação física, mudança de gate, memória, cânone ou produção. O ato de auditoria/fechamento da gerência é separado.'}
 target=B/('REVISAO_'+label+'_R1.json');put(target,report)
 md='# Revisão '+label+'\n\n**'+g['verdict']+'**\n\n[REAL] '+str(len(builds))+' recompilações EXIT 0, '+str(printed)+' impressões de axiomas e '+str(count)+' declarações locais (incluindo auxiliares) verificadas somente no trio. Zero sorry.\n\n'+'\n\n'.join(g['findings'])+'\n\n**Independência:** '+g['authorship']+'\n\n**[OPEN]** '+'; '.join(g['open'])+'\n\nFontes, hashes, logs com início/fim/tempo/LEAN_PATH e alcance em '+target.name+'. Nenhum gate muda.\n'
 put(B/('REVISAO_'+label+'_R1.md'),md)
 summaries.append({'label':label,'review':pin(target),'verdict':g['verdict'],'builds':len(builds),'printed':printed,'all_local':count})
print(json.dumps(summaries,ensure_ascii=False))
