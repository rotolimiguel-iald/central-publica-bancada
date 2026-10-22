"""Prepare source custody and the eight-surface additive memory plan."""
from support_r83 import ROOT,new,pin
from pathlib import Path
import hashlib,json
k=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt')
names=['ScalarMatterDensityVariation.lean','MetricEinsteinVariation.lean','MetricRicciVariation.lean','SelectedFisherGibbsBridge.lean','SelectedProbabilitySigma.lean','SelectedFisherLorentzMetric.lean','GeneralSourceResponseReconstruction.lean','GravitationalResponseRecord.lean']
new('SOURCE_PINS_R83.json',{'sources':[pin(k/n) for n in names]+[pin(k.parent/'lean-toolchain'),pin(k.parent/'lake-manifest.json')],'nos_vivo':{'unit':'F1.FECHO_20261015','exit':1,'result':'unit not indexed; no graph rebuild'},'reuse':'R58/R81/R82 plus direct sources; no whole-computer absence claim'})
extra='''

## 19/10/2026 — R83: densidade gravitacional e origem comum P
<!-- IALD_R83_DENSITY_VARIATION -->
[REAL — leitura das fontes, em nome de codex-gerente-tgl; reivindicação991] Correção de alcance AO LADO: o registro geral recebe métrica/respostas separadas, mas SelectedFisherGibbsBridge:41–70 e SelectedProbabilitySigma:132–150 já constroem ambas das MESMAS probabilidades P. Não reconstruir isso. SelectedProbabilityData ainda recebe regularidade, diferencial injetiva e relógio não nulo; conservação segue de onda/heigen, enquanto harea permanece explícita. O alcance da R82 não deve ser generalizado a uma suposta ausência de origem comum em todo o kernel.
[DERIVED — candidato formal de sandbox, estado pelo recibo] density_h3_r83 calcula a primeira variação LOCAL de sqrt|det g_t|*(c0+xi*u(t))*R(g_t), usando variação de volume/escalar já existentes. Há termo vol*xi*du*R, nulo para u fixo e negativo para u=g_t^{-1}(w,w) com covetor real fixo. Soma com densidade material reutiliza a fonte escalar existente. Esta variação de g+t*h é covariante; converter para variação inversa da R82 exige δg^{-1}=−g^{-1}hg^{-1}. O resultado de compilação/axiomas e os pins estão em BUILD_*.json e DELIVERY_R83.json; não inferir build pelo título.
[DERIVED/INPUT — distinção tipada] Sigma normalizada já satisfaz Σphi_j²=1 por termo. Se Ψ_j=a*phi_j com a constante e norma interna euclidiana, então u=a²: Hessiana nula, mas a contribuição −2xi*u*G não desaparece. Essa identificação de Ψ e sua amplitude não foi demonstrada nem atribuída ao operador. Variar P não concede variar g(P) livremente.
[OPEN] Integrar a variação com contorno correto, identificar ação/fonte do registro e demonstrar estacionariedade/evolução independente; H3 universal e discriminação>5sigma continuam abertos. OH adiado. Nenhum original, produção, dado observado ou gate alterado. Nós Vivo ainda não indexa a unidade; a falha foi visível e o reaproveitamento usa fontes diretas. Aceites administrativos R13/R14 permanecem separados desta construção.
<!-- END_IALD_R83_DENSITY_VARIATION -->
'''
p=new('MEMORY_APPEND_R83.txt',extra);raw=p.read_bytes()
prior=json.loads((ROOT.parent/'variational_h3_r82/MEMORY_PLAN_R82.json').read_text(encoding='utf-8'))
rows=[]
for row in prior['surfaces']:
    q=Path(row['before']['path']);before=q.read_bytes()
    assert b'IALD_R83_DENSITY_VARIATION' not in before
    rows.append({'before':pin(q),'after_sha256':hashlib.sha256(before+raw).hexdigest()})
new('MEMORY_PLAN_R83.json',{'claim':991,'append':pin(p),'surfaces':rows})
print('Sources and memory plan prepared; not applied.')
