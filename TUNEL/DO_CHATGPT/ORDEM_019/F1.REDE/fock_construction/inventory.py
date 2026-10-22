"""Produce a new, byte-pinned directed inventory; canonical inputs are read only."""
from pathlib import Path
import hashlib,json,re,datetime
B=Path(__file__).resolve().parent
K=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
M=K/'.lake/packages/mathlib'
def pin(p):
    raw=p.read_bytes()
    return {'path':str(p),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
def ref(p,needle):
    d=pin(p); lines=p.read_text(encoding='utf-8').splitlines()
    d['line']=next(i for i,s in enumerate(lines,1) if needle in s); d['anchor']=needle
    return d
sq=K/'TGLExt/TheImportedSecondQuantization.lean'
br=K/'TGLExt/MaxwellLiteratureBridge.lean'
tp=M/'Mathlib/Analysis/InnerProductSpace/TensorProduct.lean'
entries=[
('Fock.F, Ω, Ω_norm, F_infinite, ι','OPEN_FULL_CERTIFICATE','Construção concreta em curso: setores simétricos reais sobre o H1 v392; soma Hilbert e vácuo pela peça SectorDirectSum da raiz. Não usar soma de cópias de H1 como substituto da potência simétrica.',ref(sq,'structure FockCertificate')),
('Γ, Γ_refl, Γ_trans, Γ_vac, Γ_one_particle','CONSTRUCTED_SECTOR2_AND_SECTORS_IN_PROGRESS','Setor 2 implementado por completação do tensor quadrado e fixos do flip; todos n em arquivo novo por clausura do span dos poderes diagonais. Só promover estado mediante recibo de build.',ref(sq,'Γ :')),
('Γ_strong, Γ_strong4, Γ_positive, Γ_no_fixed','OPEN_CONCRETE_PROOFS','Continuidade forte, positividade espectral e unicidade do vácuo não seguem só de leis algébricas da representação; exigem teoremas sobre a soma e potências.',ref(sq,'Γ_strong :')),
('R, R_mono, R_local, R_cov','OPEN_CONSTRUCTION','Faltam operadores Weyl/CCR e álgebra de von Neumann concreta no Fock construído. A interface atual não contém Weyl nem CCR como campos.',ref(sq,'R :')),
('wedge_cyclic, wedge_separating, wedge_nonabelian','KNOWN_NOT_CONSTRUCTED_HERE','Literatura de segunda quantização de subespaços padrão fornece rota; estes campos fortes impedem confundir o modelo com álgebra escalar ou rede zero.',ref(sq,'wedge_cyclic :')),
('bw_kms, J, J_invol, J_vac, tomita, flow','OPEN_SECOND_QUANTIZATION_LINK','Peças modulares concretas H1 foram construídas em modular_wedge; transportar via Γ e provar realização modular em Fock continua obrigação.',ref(sq,'bw_kms :')),
('Core, embedding, dualAction, trace, PF, Pp, Pm','OPEN_SAME_FOCK_CORE','A série V350/V351 existe; identificar o core do fluxo do Fock concreto, embedding e projeções nesta interface requer ponte. O registro não codifica normalidade/semifinitude do traço em domínio positivo e sua aditividade só é exigida no split.',ref(sq,'Core : Type')),
('Maxwell.Dom, Dom_vac, Dom_translate','OPEN_CONCRETE_DOMAIN','Dom é Set, sem linearidade/densidade tipada. O domínio regular Maxwell não é construído aqui.',ref(sq,'structure MaxwellCertificate')),
('StressTensorDataLocalV32: simetria/conservação/covariância boost','EXISTS_TYPED','Não classificar simetria ou conservação como ausentes: já são campos de T. Covariância completa de Lorentz, F_ab e equações de Maxwell não estão nesses campos.',ref(K/'TGLExt/ContratoQG_v32.lean','structure StressTensorDataLocalV32')),
('MaxwellQuadraticForm → toStress (extensão por zero)','EXISTS_TERM','A ponte de domínio está pronta desde v375: Dom_translate/boost iff permitem extensão por zero total, idêntica a Q no domínio e sem interpretação física fora. A construção de Q real permanece aberta.',ref(br,'def toStress')),
('Maxwell.charge_link, nontrivial','OPEN_CONCRETE_PROOFS','A ponte toCertificate apenas recebe estes dois fatos. Na sonda Lean, zeroQuadraticForm habita a interface parcial; maxwell_stress_not_everywhere_zero prova que o certificado completo exclui T universalmente zero.',ref(br,'def toCertificate')),
('TensorProduct inner, commIsometry, congrIsometry','EXISTS_MATHLIB','Máquina usada literalmente no candidato. O arquivo declara TODO para completar o produto; a nova peça efetua UniformSpace.Completion explicitamente.',ref(tp,'noncomputable def congrIsometry')),
('InnerProductSpace Completion + LinearEquiv.extendOfIsometry','EXISTS_MATHLIB','Completude, produto interno e extensão de isometria de faixa densa usados para prolongar os operadores tensoriais.',ref(M/'Mathlib/Analysis/Normed/Operator/Extend.lean','def extendOfIsometry')),
('lp G 2 / soma Hilbert','EXISTS_MATHLIB','InnerProductSpace e CompleteSpace já existem; a raiz está construindo a ação diagonal em arquivo novo.',ref(M/'Mathlib/Analysis/InnerProductSpace/l2Space.lean','instance instInnerProductSpace')),
]
d={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'unit':'F1.REDE','claim_event':747,'status':'DIRECTED_INVENTORY_NOT_COMPLETE_CERTIFICATE','same_H1':ref(sq,'abbrev H1'),'entries':[{'fields':a,'status':b,'reading':c,'source':d} for a,b,c,d in entries], 'negative_probe':{'claim':'A interface parcial de forma de tensão admite Q=0; o certificado Maxwell inteiro não admite T universalmente zero. Nenhum habitante degenerado de FockCertificate foi fabricado ou alegado.','source':pin(B/'CertificateNegativeProbe.lean'),'build':pin(B/'attempts/20261013T222311_332225Z/RECEIPT.json')},'non_claims':['FockCertificate construído','campo Maxwell construído','rede 4D demonstrada por estes arquivos','dispositivo físico identificado com Fock','creditação física']}
p=B/'INVENTORY_R1.json'
with p.open('x',encoding='utf-8') as f:json.dump(d,f,ensure_ascii=False,indent=2)
print(json.dumps(pin(p),ensure_ascii=False))
