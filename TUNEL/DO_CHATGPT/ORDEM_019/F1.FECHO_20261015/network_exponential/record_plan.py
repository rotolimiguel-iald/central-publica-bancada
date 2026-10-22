from pathlib import Path
import hashlib,json,datetime,os
b=Path(__file__).resolve().parent
n=b.parent.parent/'F1.REDE'
k=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
m=k/'.lake/packages/mathlib/Mathlib'
def source(p,needles,role):
    data=p.read_bytes();lines=data.decode('utf8').splitlines()
    refs={s:[i+1 for i,line in enumerate(lines) if s in line] for s in needles}
    assert all(refs.values()),(p,refs)
    return dict(path=str(p),sha256=hashlib.sha256(data).hexdigest(),anchors=refs,role=role)
d=dict(unit='F1.FECHO_20261015',claim=845,created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
  status='DERIVED_SOURCE_PLAN_BEFORE_CONSTRUCTION',sources=[
  source(n/'fock_construction/BosonicSectors.lean',['def pureAlgebraic','def symmetricSpace','def pureTensor','theorem pureTensor_norm'],'Mesmos setores: fechamento do span diagonal; norma já construída.'),
  source(n/'fock_construction/BosonicFock.lean',['abbrev F :=','def vacuum','def gamma','def oneParticle'],'Mesmo lp dos setores; não definir outro Fock.'),
  source(m/'Analysis/InnerProductSpace/Completion.lean',['theorem inner_coe'],'Transporta a identidade do produto interno algébrico para o setor completo.'),
  source(m/'Analysis/InnerProductSpace/l2Space.lean',['theorem inner_eq_tsum','theorem hasSum_inner'],'Produto interno/série no lp.'),
  source(m/'Analysis/Normed/Lp/lpSpace.lean',['theorem memℓp_gen_iff'],'Memℓp pela somabilidade da norma quadrada.'),
  source(m/'Analysis/Normed/Algebra/Exponential.lean',['theorem expSeries_div_hasSum_exp (x : 𝔸)'],'Série inteira exp(z)=sum z^n/n! já existente.'),
  source(m/'Analysis/SpecialFunctions/Exponential.lean',['theorem Complex.exp_eq_exp_ℂ','theorem Real.exp_eq_exp_ℝ'],'Identifica a exponencial abstrata com Real/Complex exp.'),
  source(m/'Analysis/Analytic/Basic.lean',['theorem hasFPowerSeriesAt_iff :'],'Converte HasSum numa vizinhança em série analítica, sem postular raio.'),
  source(m/'Analysis/Analytic/Uniqueness.lean',['theorem HasFPowerSeriesAt.eq_zero '],'Extração de coeficientes pela unicidade da série da função zero.'),
  source(m/'Analysis/InnerProductSpace/Projection/Submodule.lean',['theorem topologicalClosure_eq_top_iff'],'Totalidade pela trivialidade do complemento ortogonal.')],
  construction='e(f)_n=(sqrt(n!))^{-1} • pureTensor n f no F existente.',
  steps=['Provar inner(pureTensor n f,pureTensor n g)=inner(f,g)^n por indução tensorial/completação.','Norma quadrada por componente = ||f||^(2n)/n!: exp fornece Memℓp.','lp.hasSum_inner fornece kernel exp(inner(f,g)) e norma.','Para totalidade: inner(psi,e(zf))=0 para todo z; usar hasFPowerSeriesAt_iff e HasFPowerSeriesAt.eq_zero para anular cada coeficiente.','Como Sector n é o fechamento do span diagonal, cada psi_n=0; complemento ortogonal do span de e(f) é zero.'],
  no_placeholder_hypothesis='Totalidade será provada ou ficará explicitamente pendente; nunca campo assumido para declarar construção.',
  provider_provenance='Alvo MiMo R3 já registrado; construção local autorizada, job preservado sem nova execução/cancelamento/substituição.',
  production_modified=False)
data=(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode()
with (b/'EXPONENTIAL_REUSE_PLAN_R1.json').open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
print(hashlib.sha256(data).hexdigest())
