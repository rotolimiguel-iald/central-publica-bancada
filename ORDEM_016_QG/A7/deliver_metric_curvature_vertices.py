"""Deliver the fixed-background potential vertices and explicitly partial loops."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,uuid
H=Path(__file__).resolve().parent;O=H.parents[1]/'TUNEL/DO_CHATGPT'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):
 b=v if isinstance(v,bytes) else (v if isinstance(v,str) else json.dumps(v,ensure_ascii=False,indent=2)).encode()
 if p.exists():
  old=p.read_bytes()
  if old==b:return
  bk=p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'));bk.write_bytes(old);assert bk.read_bytes()==old
 tmp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);tmp.write_bytes(b);assert b and tmp.read_bytes()==b;tmp.replace(p)
now=datetime.now(timezone.utc).isoformat();opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
r=json.loads((H/'metric_curvature_vertices/results.json').read_bytes())
report=f'''[DERIVED — vértices de curvatura; REAL — CAS exato; OPEN — soma métrica curva]
# A7.b — potencial métrico, duas bolhas e um tadpole delimitado
Abertura SHA256 `{opening}`. UTC {now}.

**Ação e limite da decomposição.** Com G=g+h, M=I+g^-1h e
C^rho_mu,nu=Gamma(G)^rho_mu,nu-Gamma(g)^rho_mu,nu,
a densidade Einstein–Hilbert integra-se, módulo divergência, como

    sqrt(G)[G^mu,nu Ric(g)_mu,nu
      +G^mu,nu(C^rho_mu,sigma C^sigma_nu,rho
               -C^rho_mu,nu C^sigma_rho,sigma)-2Lambda].

Na integração por partes usa-se
nabla_rho(sqrt(G)G^mu,nu)=sqrt(G)[C^lambda_rho,lambda G^mu,nu
-C^mu_rho,lambda G^lambda,nu-C^nu_rho,lambda G^mu,lambda].
Assim se recupera a mesma parte Gamma-Gamma principal já calculada,
com derivadas de fundo, e o potencial abaixo. O cutoff precisa ser constante
para descartar a divergência; seus contatos não são apagados da missão.

Ric(g)=3K g,Lambda=3K. O potencial de ação é

    S_pot=-(3K/(2kappa)) integral sqrt(g) P(h),
    P(h)=sqrt(det M)(tr M^-1-2).

Escrevendo t=trh,s_j=tr(h^j), os polinômios homogêneos são

    P2=s2/2-t²/4,
    P3=-t³/12+t s2/2-2s3/3,
    P4=-t⁴/64+3t²s2/16-3s2²/16-t s3/2+3s4/4.

O termo linear é zero. A expansão foi conferida independentemente por
autovalores de uma matriz simétrica: polinômios invariantes, não uma
hipótese de comutação entre polarizações diferentes.

Com h0=h-g trh/4, P3=-2tr(h0³)/3. A polarização cúbica fornece

    16kappa V3_pot(A,B,C)/K = 96 tr(A0 B0 C0).

Logo uma perna g anula V3_pot. Também D_g P4=-(3/2)P3, D_gP3=0,
e V4_pot(g,g,A,B)=0. A polarização usada inclui os fatores combinatórios;
não se divide outra vez por3! ou4!. C_g(h) linear não acrescenta vértices
cúbicos/quárticos de gauge fixing.

**Contribuições calculadas.** Mantendo o mesmo S0 e a contração transposta
de metric_bubble_v2, a bolha com UM vértice de potencial e UM principal,
somadas as duas posições, tem coeficiente log/A0

    K[-32p² trAB+20p² trA trB
       -34(pAp trB+pBp trA)+80pABp].

A bolha com DOIS vértices de potencial dá

    K²[576trAB-144trA trB].

São numeradores métricos **sem** o peso -1/2 da Hessiana efetiva.
Usam propagadores principais nas duas linhas. Não incluem correções de
conexão/transporte/endomorfismo dos demais diagramas; portanto não são
o coeficiente métrico curvo total. Em e12/e12,p=e0, dão -64K e1152K²:
não podem ser simplesmente descartados.

O tadpole do POTENCIAL quartico com o coeficiente log universal coincidente
do propagador métrico, proporcional a (K/2)g_ab g_cd nas convenções já
derivadas, é zero por V4_pot(g,g,A,B)=0. Isso não elimina tadpoles do
vértice quartico com derivadas, termos de potência, W suave ou contatos.

**Verificação.** {r['checks']} checks,2 negativos,rc0,CPU {r['cpu_seconds']}s.
Inclui55 pares bilineares para cada bolha, polarização por diferenças finitas
exatas, simetrias de Bose, expansão determinante/inversa e interpolação dos
vértices principais conferida fora dos nós. A avaliação das15 parcelas de
momento usa o extrator radial já verificado, sem impor Ward=0.

Reprodução: A4/symbolic_runtime/Scripts/python.exe -X utf8 -B
A7/metric_curvature_vertices_check.py. Fontes, plano, log e resultados no
manifesto. Próximo elo: quartico com derivadas e seus jatos coincidentes;
depois os demais termos da bolha curva e fontes BV. Q2 permanece aberta.
Nenhum original, kernel, gate ou arquivo canônico foi alterado.
'''
rp=O/'ENTREGA_016_A7b_vertices_potencial_metrico_curvo.md';save(rp,report);save(H/'metric_curvature_vertices/DERIVACAO.md',report)
files=[H/p for p in ['metric_curvature_vertices.py','metric_curvature_vertices_check.py','metric_curvature_vertices_run.log',
 'metric_curvature_vertices/PRE_REGISTER.json','metric_curvature_vertices/results.json','metric_curvature_vertices/manifest.json',
 'metric_curvature_vertices/DERIVACAO.md']]+[Path(__file__),rp]
save(H/'metric_curvature_vertices/delivery_manifest.json',dict(at=now,opening_sha256=opening,
 artifacts=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in files]))
ledger=O/'LEDGER_016.jsonl';raw=ledger.read_bytes();marker='A7_METRIC_CURVATURE_POTENTIAL_VERTICES'
if marker.encode() not in raw:save(ledger,raw+(json.dumps(dict(event=marker,at=now,provider='local',target='A-7.b',
 checks=r['checks'],cpu_seconds=r['cpu_seconds'],report_sha256=sha(rp),full_Q2=False,new_external_execution=False))+'\n').encode())
cont=H/'CONTINUIDADE.json';d=json.loads(cont.read_bytes())
d.update(at=now,status='ACTIVE',previous_goal_turn='PROGRESS',
 completed_this_turn=['Curvature potential cubic/quartic vertices derived from fixed-background action',
 'Two explicit metric bubble contributions computed;potential quartic logarithmic tadpole zero with restricted scope',
 'Kimi curvature review completed;MiMo independent log audit started per coordinator'],
 metric_potential_manifest=str(H/'metric_curvature_vertices/delivery_manifest.json'),
 next=['Derivative quartic metric vertex and coincident propagator jets; remaining curved metric bubble',
 'Recover Kimi curvature result by API;review before incorporating; no repeat',
 'Full Q2 open;A7.c onlyafter24h;A7.d,A8,PartB and finalaudit remain'])
save(cont,d)
progress=O/'ENTREGA_016_PROGRESSO.md';cost=json.loads((H/'ghost_curved_hessian/COST_SNAPSHOT.json').read_bytes())['total_known_partial']
save(progress,progress.read_bytes()+f'\n- {now} — A7.b PROGRESSO: verticespotencialcurvo,bolhas K[-32,20,-34,80] eK²[576,-144],273checks CPU{r["cpu_seconds"]}s. Tadpolepotenciallogzero;derivativosOPEN. Custo parcialUS${cost},desconhecidosnãozero. Abertura{opening};ledger{sha(ledger)}.\n'.encode())
for a in json.loads((H/'metric_curvature_vertices/delivery_manifest.json').read_bytes())['artifacts']:assert sha(Path(a['path']))==a['sha256']
print(json.dumps(dict(report=str(rp),verified_artifacts=len(files),status='ACTIVE_PROGRESS')))
