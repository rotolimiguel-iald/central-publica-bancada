import json,datetime
from pathlib import Path
from audit_provenance import OUT,atomic,metadata
root=OUT.parent;mp=root/'F9_ASSEMBLY_MANIFEST.json';manifest=json.loads(mp.read_text());sources=[];pins=[]
for x in [manifest['note']]+manifest['sources']:
 m,raw=metadata(Path(x['path']));sources.append(m);pins.append({'path':m['path'],'match':m['sha256']==x['sha256'] and m['bytes']==x['bytes']})
sources.append(metadata(mp)[0]);sources.append(metadata(OUT/'REVISAO_SUPORTE_H0DN.md')[0])
snapshot=OUT/'f9_assembly_snapshot';snapshot.mkdir(exist_ok=True)
for name in ['F9_LIKELIHOOD_ASSEMBLY_CANDIDATE.md','F9_ASSEMBLY_MANIFEST.json']:
 p=root/name;dest=snapshot/name
 if dest.exists():assert dest.read_bytes()==p.read_bytes()
 else:atomic(dest,p.read_bytes())
note='''# Revisão documental F9 — montagem comum candidata

**F9-01 — P2 localizado: restringir a frase sobre priors finitos, linha29.** O fator de probabilidade de truncamento nessa dedução vale para um prior uniforme em domínio finito, junto de sua constante normalizadora. Não é a marginalização geral de qualquer prior próprio da alternativa1. Para uma uniforme em D de volume V, nas condições já declaradas, a integral normalizada é L_perfilada (2pi)^(p/2)/sqrt(det G) × Pr[N(eta_hat,G^-1) em D]/V. Para prior próprio gaussiano eta~N(m,S), independente do ruído, a distribuição marginal tem média a_h h+c_C delta_C+Xm e covariância C+XSX^T, com suporte/normalização correspondentes. Esta segunda identidade já foi auditada na biblioteca de suporte; não foi reexecutada aqui. Correção concreta: trocar a frase genérica por “Priors uniformes em domínios finitos acrescentam o fator de truncamento e 1/Vol; outros priors próprios exigem sua integral normalizada, como a convolução gaussiana já revista”. Não é falha observacional ou ajuste realizado, mas precisão necessária antes de transcrever a proposta para algoritmo.

Nenhum outro achado acionável no recorte examinado. [DERIVED condicional] A integral com medida plana está corretamente restrita a N^T X=0, G=X^T C+X invertível, condição de núcleo satisfeita, suporte afim comum, domínio R^p e mesma medida. Completar o quadrado produz o fator (2pi)^(p/2)/sqrt(det G); sua remoção comparativa exige o determinante e a constante arbitrária comuns. Dimensão/rank comum sozinhos não bastam para medida de suporte comum. A nota preserva essas restrições e exige parametrizar o subespaço admissível quando N^T X não é zero.

[DERIVED/INPUT] A resposta h=log10(H0_bg)+I beta/ln10 tem sinal positivo coerente com Hlocal=Hbg exp(I beta). A coluna efetiva a_h do sistema transporta essa mudança; não há soma indiscriminada a todas as medidas. O adendo H0DN previamente revisto fixa viés diferencial positivo no módulo publicado e delta_C=-5log10(1+s) para a escada pura; a nota não estende automaticamente essa resposta ao H0 misto. X contém somente os nuisance restantes após separar h, evitando a dupla coluna de h. A absorção de deslocamento universal na rede isolada diz respeito a uma mudança ao longo da coluna a_h, não a qualquer vetor arbitrário de viés.

[REAL documental / OPEN] H5 A é apresentada como opção não selecionada, preservando r_drag/r_star e a qualificação pendente da compressão. Mesmo conjunto de dados/medida, dependências entre blocos e prevenção de duplicação estão explícitos. Não há ajuste, centro novo, evidência calculada ou V1 ratificado. Matriz numérica, resposta física, priors nuisance, covariância residual e implementação continuam OPEN. Não foram repetidos ensaios nem feitas buscas ou execuções físicas. Hashes lidos dos arquivos e conferência do manifesto constam do recibo; originais não modificados pelo revisor.
'''
atomic(OUT/'REVISAO_F9_ASSEMBLY.md',note)
r={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ONE_LOCALIZED_PRIOR_FORMULA_CLARIFICATION_REQUIRED','findings':[{'id':'F9-01','priority':'P2','state':'OPEN','line':29,'scope':'Restrict truncation-probability formula to bounded uniform prior, with normalization; distinguish general proper Gaussian integration'}],'sources':sources,'manifest_checks':pins,'report':metadata(OUT/'REVISAO_F9_ASSEMBLY.md')[0],'new_scientific_tests':False,'observations_opened':False,'fits':False,'author_files_modified':False}
atomic(OUT/'REVISAO_F9_ASSEMBLY.json',json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'report':r['report'],'manifest_all_match':all(x['match'] for x in pins),'manifest_count':len(pins)},ensure_ascii=False))
