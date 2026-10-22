"""Seal the focused reuse report; read-only mission synchronization."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, re, html, subprocess

HERE=Path(__file__).resolve().parent
REF=Path(r'C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json')
def pin(p):
 p=Path(p);b=p.read_bytes()
 return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def new(name,value):
 p=HERE/name;tmp=p.with_name(p.name+'.tmp')
 b=((value if isinstance(value,str) else json.dumps(value,ensure_ascii=False,indent=2))+'\n').encode('utf-8')
 with tmp.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 assert tmp.stat().st_size==len(b)
 if p.exists():raise FileExistsError(str(p))
 os.rename(tmp,p)
 return pin(p)

fetch=json.loads((HERE/'PRIMARY_FETCH_R66_NETWORK.json').read_text(encoding='utf-8'))
assert all(r.get('status')==200 for r in fetch)
book=HERE/'literature'/'engel_nagel.pdf'
articles=[]
for stem,url in [('attal_pautrat_0311002v2','https://arxiv.org/abs/math-ph/0311002v2'),('attal_pautrat_0402064v1','https://arxiv.org/abs/math/0402064v1')]:
 p=HERE/'literature'/(stem+'.html');t=p.read_text(encoding='utf-8')
 title=html.unescape(re.search(r'<meta name="citation_title" content="([^"]*)"',t).group(1))
 block=next(i for i,l in enumerate(t.splitlines(),1) if '<blockquote class="abstract' in l)
 articles.append({'url':url,'title':title,'source':pin(p),'title_metadata_line':41,'abstract_lines':[block,block+3],
 'read_scope':'Título, autores e abstract apenas; texto integral e hipóteses dos teoremas não examinados.',
 'status':'KNOWN_ROUTE_FROM_ABSTRACT_NOT_A_SPECIALIZATION_PROOF',
 'use':('Cadeia de interações repetidas e limite Langevin; abstract anuncia três escalas e aproximação de geradores Lindblad por mapas CP.' if '0311002' in stem else 'Cadeia de átomos de n+1 níveis e limite em Gamma_s(L2(R;C^n)); operadores matriciais aproximam criação, aniquilação e gauge.'),
 'limit':'Não identifica automaticamente o banho do dispositivo, coeficientes bosônicos ilimitados ou circularSmear/H1 Maxwell.'})

supp={'schema':'r66-primary-semigroup-routes-v1','author':'/root/maxwell_covariance_review','created_utc':datetime.now(timezone.utc).isoformat(),
 'status':'DECLARADO_CANDIDATE_SOURCE_CHECK','requirement_satisfied':False,'mission_reference':str(REF),
 'book':{'url':fetch[0]['url'],'source':pin(book),'read_scope':'Somente os enunciados III.1.3 e III.5.8 e trecho adjacente; PDF inteiro custodiado, não lido integralmente.',
 'theorems':[
 {'number':'III.1.3','printed_page':158,'pdf_page_zero_based':173,'hypotheses':'A gera C0 em Banach X; ||T(t)||≤M exp(wt), M≥1; B∈L(X).','conclusion':'A+B em D(A) gera C0; ||S(t)||≤M exp((w+M||B||)t).'},
 {'number':'III.5.8','printed_page':227,'pdf_page_zero_based':242,'hypotheses':'T,S são C0; ||[T(t/n)S(t/n)]^n||≤M exp(wt); D=D(A)∩D(B) e (lambda0−A−B)D densos, lambda0>w.','conclusion':'C=closure(A+B) gera U(t); [T(t/n)S(t/n)]^n x→U(t)x uniformemente em t compacto.','visual_check':'A barra sobre A+B foi conferida na imagem da página; extração textual pode omiti-la.'}],
 'application_scope':'DERIVED condicional: se T0 é CPTP C0 em T1 e B=−i[Omega sigma_x,·], ||B||≤2|Omega|. III.1.3 dá A0+B fechado e resolvente para lambda>||B||. A estabilidade do produto vale com M=1,w=0. III.5.8 então aplica. CPTP requer passagem ao limite também nas amplificações finitas; não é conclusão isolada de III.1.3.',
 'not_proved_here':'Não é auditoria integral da construção bosônica, prova Lean, teorema HP ilimitado, troca dos limites de cortes/colisões ou identificação espacial.'},
 'articles':articles,'fetch_receipts':[pin(HERE/'PRIMARY_FETCH_R66.json'),pin(HERE/'PRIMARY_FETCH_R66_NETWORK.json')],
 'extraction_scope_note':'Os arquivos *_abstract.txt começam com o primeiro h1 da página (categoria disciplinar), não com o título do artigo. O título correto foi recuperado do campo citation_title e registrado acima; originais/extratos preservados.',
 'local_derivatives':[pin(p) for p in sorted((HERE/'literature').glob('*')) if p.suffix in {'.txt','.png'}],
 'network_note':'Primeira leitura direta recusada por DNS no sandbox; preservada. Segunda leitura pública autorizada retornou HTTP200 nas três fontes. Nenhum conteúdo local foi enviado.'}
sp=new('KNOWN_SEMIGROUPS_R66.json',supp)
note='R66 — fontes primárias e condições de uso\n\nEngel–Nagel: III.1.3, página impressa158/PDF173, e III.5.8, página227/PDF242. A soma no segundo enunciado recebe fecho; conferir as hipóteses completas no JSON ao lado. A aplicação ao bombeamento OH é condicional à extensão C0 em classe-traço e à passagem CPTP nas amplificações; nenhuma identificação temporal/espacial decorre desses teoremas.\n\nAttal–Pautrat: os dois abstracts fornecem rotas para colisões→ruído/Fock temporal. Texto integral não lido; nenhuma aplicação aos operadores ilimitados do dispositivo foi certificada aqui.\n\nFalha DNS inicial preservada e HTTP200 posterior custodiado. PDF integral pinado; leitura focal de duas páginas. Nenhum build, simulação, chamada de modelo, transição de missão ou original alterado.\n'
np=new('KNOWN_SEMIGROUPS_R66.txt',note)

checks=[]
def walk(o):
 if isinstance(o,dict):
  if isinstance(o.get('path'),str) and re.fullmatch('[0-9a-f]{64}',str(o.get('sha256',''))):
   a=pin(o['path']);assert a['sha256']==o['sha256'],o['path'];checks.append(a)
  for v in o.values():walk(v)
 elif isinstance(o,list):
  for v in o:walk(v)
for n in ['SOURCE_PINS_R66.json','REUSE_R66.json','KNOWN_SEMIGROUPS_R66.json']:
 walk(json.loads((HERE/n).read_text(encoding='utf-8')))
ip=new('INTEGRITY_FINAL_R66.json',{'status':'PASS_BYTES','verified_pin_occurrences':len(checks),'unique_paths':len({c['path'] for c in checks}),'pins':checks})
req={'operation':'project','reference':str(REF),'max_chars':400000}
cp=subprocess.run([r'C:\Python314\python.exe','-B','-X','utf8',r'C:\IALD\MEMORIA_IALD\mission_cli.py'],input=json.dumps(req),capture_output=True,text=True,encoding='utf-8')
d=json.loads(cp.stdout);assert cp.returncode==0 and d.get('ok'),cp.stderr
pr=new('PROJECT_FINAL_R66.json',d)
r=d['result'];revision=r['receipt']['revision']
delivery={'schema':'r66-source-reuse-delivery-v1','author':'/root/maxwell_covariance_review','status':'DECLARADO_AWAITING_INDEPENDENT_REVIEW','mission_reference':str(REF),'revision_final':revision,'requirement_satisfied':False,
 'artifacts':[pin(HERE/n) for n in ['REUSE_R66.json','REUSE_R66.txt','SOURCE_PINS_R66.json','FOCAL_SEARCH_R66.json','KNOWN_SEMIGROUPS_R66.json','KNOWN_SEMIGROUPS_R66.txt','INTEGRITY_FINAL_R66.json','PROJECT_START_R66.json','PROJECT_RESUME_R66.json','PROJECT_FINAL_R66.json']],
 'coverage':'24 fontes locais, busca focal anterior em12fontes,10 módulos F1.REDE/fock_construction; suplemento3fontes primárias públicas. Sem busca universal.',
 'material_results':['J inteiro preserva interferência de banho comum; canais independentes dentro de J alteram gerador.','R64 já fornece instrumento de saída temporal e discretização Kraus de primeira ordem.','Setores/Fock e pacotes densos/localizados/covariância são reutilizáveis; fi/fo de R63 são INPUT, não mapa físico demonstrado.','Perturbação limitada e Trotter localizados com hipóteses explícitas; abstracts de colisões não provam especialização ilimitada.'],
 'residual':'Mapa físico de modos/acoplamentos e igualdade de Gram com circularSmear, localização/causalidade e entrelaçamento do relógio/gerador continuam obrigações; não declarar R4/R5 integrais satisfeitos.',
 'mutations':'Somente novos artefatos desta pasta; nenhuma memória, missão, quadro, produção ou fonte científica alterada. Nenhuma simulação/build/provedor executado.'}
dp=new('DELIVERY_R66.json',delivery)
print(json.dumps({'delivery':dp,'main_report':pin(HERE/'REUSE_R66.json'),'supplement':sp,'revision':revision,'verified_pins':len(checks)},ensure_ascii=False))
