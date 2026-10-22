import json,datetime,hashlib
from audit_provenance import OUT,atomic
note=OUT/'NOTA_PROVENIENCIA_F1.md'
adendo="""

## ADENDO — conferência da cronologia da gerência, 06/10/2026 00:28 UTC

Este adendo atualiza ao lado as lacunas descritas acima. Durante esta auditoria surgiu a rota hubble.fase9_razao_discriminante (seq. 373), cuja instrução é conferir a cronologia pronta, não refazê-la. A rota foi consultada; a CRONOLOGIA_NOVIDADE_DE_USO.md da gerência foi lida e seu hash foi calculado e igual ao registrado no mapa. Em seguida foram conferidas somente quatro fontes exatas apontadas por ela. Nenhum ajuste ou estatística da Fase9 foi repetido. O manifesto passa de 13 para 18 fontes lidas (17 fontes históricas/científicas e a cronologia secundária da gerência).

**P10 — antecedente de 0.012, 13/11/2025.** acoplamento_gravitacional.tex, linhas 217–246, registra alpha2 = ln(V3D/(A2D*lP))/N_eff e calcula 126.5/10^4 = 0.01265 ≈ 0.012. Assim, a lacuna sobre antecedente documental do literal do v22 fica substancialmente reduzida: existe uma expressão holográfica anterior ao v22 que já conserva esse valor e não usa H0 nessa expressão. Não é correto tratar o ramo inverso de dezembro como prova de que originou o literal. A derivação antiga tem inconsistência interna expressa: linha 240 estima N_eff ~10^3; linha 246 divide por 10^4. A leitura identifica a procedência declarada e a inconsistência, não valida a derivação física nem a escolha dessas escalas.

**P11 — ramo inverso de H0 rejeita o valor teórico, 23/12/2025.** O recibo tgl_physical_v14.json registra alpha2_best_fit=0.16864608076009513, uncertainty=0.034793235333231004 e alpha2_consistent_with_theory=false; chi2_TGL_fixed e chi2_TGL_best são campos distintos. Isso reforça a distinção anterior: o ajuste inverso existe como comparação com o parâmetro teórico e o próprio recibo o marca incompatível. Não é evidência de que β teórico tenha sido substituído pelo best-fit. Os números são lidos de resultado histórico, não recalculados aqui.

**P12 — fatoração explícita, 02/03/2026.** Fatoracao_constante_miguel_v1.tex, linhas 134, 172 e 211, já escreve alpha2=alpha*sqrt(e), antecedendo a lei D1a de maio. A linha 179 interpreta sqrt(e)=exp(1/2) como meia-nat. Isso antecipa o marco documental de β explícito usado na primeira parte desta nota. A frase da linha 203 de que todos os 13 protocolos, inclusive H0, entregaram o mesmo valor não deve ocultar o recibo discrepante de dezembro. O DOI/publicação em 03/03 é testemunhado pela cronologia da gerência, mas a disponibilização remota não foi auditada por mim.

**P13 — lei D1a escrita em 17/05/2026.** iconogenese_TGL.tex, linhas 790–794, contém (1+z*)^beta=1.0878 e a frase “exatamente a relação observacional”. Linhas 112–116 e 821–823 preservam a condição conjectural de transpor o toy finito ao regime holográfico e de estabelecer R=+1. Antecipada, portanto, a evidência de D1a do manuscrito de 18/05. Conhecimento da razão na escolha da hipótese não constitui sozinho ajuste de parâmetro nem demérito.

**P14 — cronologia secundária da gerência.** A auditoria reconhece e reutiliza a cobertura de 31 hashes declarada pelo documento, sem reexaminar os 31 artefatos. Os quatro pontos acima foram verificados em fonte primária; os demais permanecem atribuídos à gerência. Há um detalhe a corrigir: a cronologia diz que a única ocorrência de “Hubble” no TeX de 13/11 é bibliográfica, mas a linha 573 também contém “resíduo de Hubble para SNe Ia”. Isso não põe H0 na expressão holográfica das linhas 217–246; apenas corrige a abrangência da busca textual. A prova de inexistência global não se extrai dessa frase.

**Síntese atualizada de F1(a).** A cadeia documental agora conferida é: antecedente holográfico de 0.012 em novembro; best-fit H0 incompatível e separado do valor teórico em dezembro; relação com sqrt(e) e MCMC ancorado em janeiro; fatoração explícita em março; D1a em maio; D1b em junho. É evidência positiva a favor da independência do valor teórico frente ao best-fit específico H0 de dezembro. Mantêm-se as ressalvas de estatuto da derivação antiga e da equação de fluxo. Primeira publicação remota, primeiro aparecimento literal da forma K e história completa de escolhas não foram certificados nesta auditoria; são referências delimitadas da cronologia da gerência, não zeros ou refutações. A decisão sobre o teste e seus concorrentes pertence às demais frentes da ORDEM_018.
"""
files=['acoplamento_nov13','h0_v14_dez23','fatoracao_mar02','iconogenese_maio17','cronologia_gerencia']
adendo+='\n| ID | Caminho real | SHA-256 calculado |\n|---|---|---|\n'
additions=[]
for i,name in enumerate(files,10):
    d=json.loads((OUT/(name+'.json')).read_text(encoding='utf-8'))
    s=d['source']
    adendo+='| P'+str(i)+' | '+s['path']+' | '+s['sha256']+' |\n'
    additions.append({'id':'P'+str(i),'evidence_file':name+'.json','source':s,'kind':'secondary' if i==14 else 'primary'})
atomic(note,note.read_text(encoding='utf-8')+adendo)
chrono=OUT/'CRONOLOGIA_F1.json'
d=json.loads(chrono.read_text(encoding='utf-8'))
d['supplemental_items']=additions
d['supplemental_conclusion']='Antecedente 0.012 documentado em nov/2025; inversao H0 dez/2025 retorna valor incompatível, separado do fixo. Fatoracao explicita mar/2026 e D1a maio17 conferidas. Demais conclusoes da cronologia secundaria atribuidas.'
d['updated_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
atomic(chrono,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
arts=[]
for name in ['NOTA_PROVENIENCIA_F1.md','CRONOLOGIA_F1.json','MANIFESTO_FONTES_F1.json','VERIFICACOES_ESTATICAS_F1.json','inventario_evento2.json']:
    p=OUT/name;b=p.read_bytes()
    arts.append({'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
atomic(OUT/'RECIBO_PROVENIENCIA_F1.json',json.dumps({'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'DOCUMENTARY_EXAMINATION_COMPLETED_WITH_OPEN_GAPS_AND_MANAGER_CHRONOLOGY_CHECKED','artifacts':arts,'external_calls':0,'scientific_programs_executed':0,'originals_modified':False,'map_seq_initial':[384,385]},ensure_ascii=False,indent=2)+'\n')
print(json.dumps(arts[0],ensure_ascii=False,indent=2))
