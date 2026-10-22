from pathlib import Path
import json,hashlib,re,datetime,os
b=Path(__file__).resolve().parent
n=b.parent.parent/'F1.REDE'
k=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
m=k/'.lake/packages/mathlib/Mathlib'
def record(p,needles,role):
    data=p.read_bytes();lines=data.decode('utf8').splitlines()
    refs={a:[i+1 for i,s in enumerate(lines) if a in s] for a in needles}
    assert all(refs.values()),(p,refs)
    return dict(path=str(p),sha256=hashlib.sha256(data).hexdigest(),anchors=refs,role=role)
sources=[
record(n/'modular_wedge/CanonicalWedge.lean',['def Jcandidate','theorem Jcandidate_involutive'],'Antiunitária involutiva já concreta em H1; não reconstruir.'),
record(n/'modular_wedge/CanonicalOutput.lean',['J := Jcandidate','J_involutive := Jcandidate_involutive'],'A MESMA J do contrato D1a3 habitado.'),
record(n/'fock_construction/BosonicSectors.lean',['def powerData','def algebraicGamma','def symmetricSpace','def gammaSector','def oneParticleEmbedding'],'Mesmos tensores e setores: span diagonal fechado, sem impor uma nova realização.'),
record(n/'fock_construction/BosonicTwoParticle.lean',['def completionEquiv','theorem completionEquiv_coe'],'Adaptador linear existente; a API de extensão subjacente já é semilinear.'),
record(n/'fock_construction/SectorDirectSum.lean',['def diagonalFun','def diagonal','def sectorEmbedding'],'Soma Hilbert existente; novo adaptador semilinear componente a componente.'),
record(n/'fock_construction/BosonicFock.lean',['abbrev F :=','def vacuum','def gamma','def oneParticle'],'Fock concreto mantido definição por definição.'),
record(k/'TGLExt/GenericAntilinearAdjoint.lean',['theorem antiunitary_inner_conj'],'Identidade do produto interno antiunitário já genérica em H.'),
record(m/'LinearAlgebra/TensorProduct/Map.lean',['def congr (f : M ≃ₛₗ[σ₁₂]','theorem congr_tmul'],'Transporte algébrico já semilinear; falta apenas empacotar sua isometria.'),
record(m/'Analysis/Normed/Operator/Extend.lean',['def extendOfIsometry','theorem extendOfIsometry_eq'],'Extensão semilinear isométrica existente, reutilizada diretamente.'),
record(m/'Analysis/InnerProductSpace/TensorProduct.lean',['noncomputable def congrIsometry','theorem inner_tmul'],'Wrapper de isometria tensorial é linear; identidade de produto interno permite adaptador antiunitário.')]
handoff=n/'orchestration_r3/HANDOFF_SUBMITTED_R3_20261014.json'
doc=dict(unit='F1.FECHO_20261015',claim=845,created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
status='DERIVED_LOCAL_IMPLEMENTATION_PLAN',sources=sources,
preexisting_jobs=dict(path=str(handoff),sha256=hashlib.sha256(handoff.read_bytes()).hexdigest(),data=json.loads(handoff.read_bytes())),
provenance='Construção local Codex autorizada pela gerência delegante; nenhum provedor executado, substituído, cancelado ou reaberto. Conciliação futura com os pedidos registrados cabe à coordenação.',
scope=['Pagar J, J_invol, J_vac no mesmo Fock do assembly R1 por Gamma(Jcandidate).','Preservar a aplicação ao setor1 e o vácuo por termos, não campos.','Tomita, KMS, CCR, Weyl, positividade espectral no Fock e core modular permanecem explicitamente importados.'],
steps=['TensorProduct.congr com starRingEnd, norma pela identidade de produto interno já existente.','Extensão por extendOfIsometry ao MESMO Completion.','Invariância do span diagonal e do seu fechamento; restrição aos mesmos Sector n.','Soma lp componente a componente preserva norma; inversa dada pela involução.','Especialização em Jcandidate; Gamma(J)^2=1, vácuo fixo, entrelaçamento de oneParticle.','Novo adaptador do certificado elimina três campos pagos e conserva os demais como hipóteses nomeadas.'],
falsifiers=['Primeiro setor precisa reproduzir Jcandidate; conjugação arbitrária do Fock não paga o alvo.','Vácuo deve ser o existente, não outro por equivalência abstrata.','J/J_invol/J_vac não podem reaparecer como hipóteses no consumidor.'],
not_claimed=['Identificação Gamma(J) com o Tomita de uma álgebra CCR ainda não construída.','Construção de Maxwell/Wick, Takesaki para a mesma álgebra, H3 ou rede global por esse único adaptador.'])
data=(json.dumps(doc,ensure_ascii=False,indent=2)+'\n').encode()
with (b/'GAMMA_J_REUSE_PLAN_R1.json').open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
print(hashlib.sha256(data).hexdigest())
