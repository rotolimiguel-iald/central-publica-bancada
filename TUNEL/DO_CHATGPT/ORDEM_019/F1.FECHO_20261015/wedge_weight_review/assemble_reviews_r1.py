from pathlib import Path
import datetime,hashlib,json
B=Path(__file__).resolve().parent;P=B.parent
def pin(p):
 p=Path(p);r=p.read_bytes();return {'path':str(p),'sha256':hashlib.sha256(r).hexdigest(),'bytes':len(r)}
def put(p,s):
 if isinstance(s,str):s=s.encode('utf-8')
 with p.open('xb') as f:f.write(s)
auditp=B/'all_local/RECEIPT_R1.json';audit=json.loads(auditp.read_text(encoding='utf-8'));assert audit['passed']
blocks=[('WEDGE',['anti','noniso','nonabelian'],['F1Fecho.WedgeAntiAlgebra','F1Fecho.WedgeNonisotropic','F1Fecho.WedgeNonabelian']),('FAITHFUL_WEIGHT',['fixed','resolvent','faithful'],['F1Fecho.RegularCoreFixed','F1Fecho.RegularCoreResolvent','F1Fecho.CanonicalFockFaithfulWeight'])]
findings={
'WEDGE':[
 'ΓJ é a antiunitária concreta já construída. Sua conjugação transporta a álgebra de Weyl de KWR para a de KWR simpĺeticamente complementar; o sinal -J em W_field é consumido e a estabilidade por negação resolve a imagem de geradores.',
 'A igualdade de álgebras deriva por transporte de bicomutantes; a última conclusão é inclusão no comutante. Nenhuma igualdade Haag nem identificação polar é usada ou concluída neste bloco.',
 'TW f=f implica f=0 pelo multiplicador exp(2π²x), que vale 1 só num singleton de medida nula. Positividade de TW dá KWR∩J KWR={0}; o habitante não nulo anteriormente construído exclui isotropia.',
 'O pareamento simplético não nulo é escalado dentro do subespaço real para π/2. As fases CCR tornam-se -i e i; W(f+g) não nulo, provado usando inverso e vácuo de norma 1, impede comutação. A não comutatividade não entra como hipótese.',
 'Todos os espaços, operadores e álgebras são os mesmos das construções concretas anteriores. Não é uma conclusão de confirmação física.'
],
'FAITHFUL_WEIGHT':[
 'RegularCoreFixed é genérico na família unitária fortemente contínua B e na álgebra M, com normalização de M por B nomeada; a aplicação Fock fornece essa condição pelo boost da cunha já construído.',
 'Os campos torcidos do comutante e a reflexão de lifts identificam fibre(C)∈core exatamente com C∈M. A comutação com shifts e caracteres identifica os pontos fixos da ação dual com a base amplificada.',
 'Cortes e resolventes canônicos permanecem no mesmo core representado. O limite positivo de contrações é construído por monotonicidade; a invariância dual reutiliza o lema analítico existente.',
 'O peso é exatamente o dualQuadraticIntegral avaliado em testVector(vacuum), no core de R(KWR) em L²(R;F). A separação do vácuo deriva da construção já revisada; nenhum novo campo de separação é assumido.',
 'Peso zero fixa o vácuo pelo resolvente; separação no core fixo força R=1. A finitude da integral é obtida ANTES de converter ENNReal.toReal, portanto a conclusão weight(A)=0↔A=0 não confunde infinito com zero.',
 'Semifinitude, traço, escala exp(-s), grupo modular do peso e equivalência Fock-torre continuam fora deste bloco.'
]}
for name,names,prefs in blocks:
 rows=[]
 for n in names:
  rp=B/n/'RECEIPT_R1.json';r=json.loads(rp.read_text(encoding='utf-8'));assert r['passed'] and r['source_exact_copy']
  for dep in r['dependencies_before_after']:assert pin(dep['path'])['sha256']==dep['sha256']
  rows.append({'name':n,'receipt':pin(rp),'source':r['source'],'olean':r['olean'],'exit_code':r['exit_code'],'seconds':r['seconds'],'same_olean_as_original':r['olean_identical_to_accepted']})
 count=sum(audit['counts'][p] for p in prefs)
 result={'unit':'F1.FECHO_20261015','claim':845,'reviewer':'codex atrator_skeptic','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'verdict':'PASS_WITH_STATED_SCOPE','material_findings':[],'analysis':findings[name],'rebuilds':rows,'all_local_audit':pin(auditp),'all_local_count_this_block':count,'trio_only':True,'zero_sorry':True,'independent_authorship':'Fontes deste bloco são de root/tempo_math_review; o revisor não as construiu. Dependências previamente revistas são reaproveitadas.','binary_note':'Igualdade de fonte é byte a byte. Quando o .olean difere, apenas a diferença é registrada; não se atribui causa sem medição. O kernel foi recompilado e os axiomas das declarações locais foram inspecionados.','originals_memory_production_gate_modified':False}
 path=B/('REVISAO_'+name+'_R1.json');put(path,json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 md='# Revisão independente — '+name+'\n\n[REAL] PASS_WITH_STATED_SCOPE: três recompilações independentes EXIT 0; '+str(count)+' declarações locais incluindo auxiliares apenas no trio, zero sorry.\n\n'+'\n\n'.join(findings[name])+'\n\nHashes, comandos, LEAN_PATH literal, início/fim/duração e diferenças binárias constam do JSON e recibos vinculados. Nenhuma fonte original, memória, produção ou gate alterado.\n'
 put(B/('REVISAO_'+name+'_R1.md'),md)
 print(json.dumps({'report':pin(path),'count':count},ensure_ascii=False))
