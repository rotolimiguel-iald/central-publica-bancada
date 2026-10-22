"""Preparation controls only: no Bilby/LAL/Dynesty imports, sampler or waveform."""
from pathlib import Path
import ast,hashlib,json,math,random,os,sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from prior_transform import transform,parameters,FREE,FIXED,MASS_AREA
checks=[]
def check(name,condition):
    checks.append({"name":name,"passed":bool(condition)})
    if not condition:raise AssertionError(name)
for rel in ("prior_transform.py","driver_p3.py","launch_p3.py"):
    ast.parse((ROOT/rel).read_text());check("syntax:"+rel,True)
c=json.loads((ROOT/"CONTRATO_P3.json").read_text())
for rel,pin in c["inputs"].items():
    raw=(ROOT/rel).read_bytes()
    check("input_pin:"+rel,len(raw)==pin["bytes"] and hashlib.sha256(raw).hexdigest()==pin["sha256"])
check("no_execution_dir",not (ROOT/"EXECUTION_001").exists())
check("no_actual_authorization_receipt",not (ROOT/"AUTORIZACAO_COORDENACAO.json").exists())
check("exact_free_coordinate_order",list(FREE)==c["free_parameters"])
# Independent midpoint quadrature over allowed rectangle strips.
n=30000;dx=75/n
area=sum((min(80,35+(i+.5)*dx)-max(20,.2*(35+(i+.5)*dx)))*dx for i in range(n))
check("normalized_conditioned_mass_area",abs(area-MASS_AREA)<1e-6)
rng=random.Random(902018);max_jac_err=0.
for i in range(10000):
    u=[rng.random() for _ in range(12)];v=transform(u);p=parameters(v)
    assert 35<=p["mass_1"]<=110 and 20<=p["mass_2"]<=80 and .2<=p["mass_ratio"]<=1
    assert -.8<=p["dtau220"]<=2 and all(p[k]==x for k,x in FIXED.items())
    assert all(math.isfinite(x) for x in v)
    if i<1000 and 1e-5<u[0]<1-1e-5 and min(abs(v[0]-80),abs(v[0]-100))>1e-3:
        h=1e-7;ul=u.copy();ur=u.copy();ul[0]-=h;ur[0]+=h
        deriv=(transform(ur)[0]-transform(ul)[0])/(2*h)
        jac=deriv*(min(80,v[0])-max(20,.2*v[0]))
        max_jac_err=max(max_jac_err,abs(jac/MASS_AREA-1))
check("10000_prior_points_support_and_fixed_zeros",True)
check("joint_mass_jacobian_constant",max_jac_err<1e-6)
for a in (0.,1687.5/MASS_AREA,2887.5/MASS_AREA,1.):
    for b in (0.,1.):
        u=[.5]*12;u[0]=a;u[1]=b;p=parameters(transform(u))
        check("mass_piece_endpoint:%s:%s"%(a,b),.2-1e-14<=p["mass_ratio"]<=1+1e-14)
for u in ([.5]*11,[-.1]+[.5]*11,[1.1]+[.5]*11,[float("nan")]+[.5]*11):
    try:transform(u)
    except ValueError:pass
    else:raise AssertionError("Invalid cube accepted")
check("invalid_cube_fail_closed",True)
for j in c["jobs"]:
    p=j["truth"]
    check("exact_fixed_deformations:"+j["id"],all(p[k]==x for k,x in FIXED.items()))
check("only_two_paired_synthetic_targets",[j["label"] for j in c["jobs"]]==["GR_GAUSS","RB_GAUSS"] and c["noise"]["paired_between_jobs"])
check("hard_budget_includes_initialization",c["limits"]["max_likelihood_calls"]==10000)
check("no_native_modules_imported",not any(x in sys.modules for x in ("bilby","lal","lalsimulation","dynesty","numpy")))
result={"status":"PREPARATION_CONTROLS_PASS","checks":checks,"count":len(checks),
        "mass_area_quadrature":area,"maximum_relative_mass_jacobian_error":max_jac_err,
        "PE_jobs":0,"native_waveforms":0,"D_read":False,
        "scope":"Syntax, pins and independent normalized-prior arithmetic only; no scientific runtime wiring or likelihood evaluated."}
path=ROOT/"CONTROLES_PREPARACAO_V2_FINAL.json";assert not path.exists()
raw=(json.dumps(result,indent=2)+"\n").encode();tmp=path.with_name(path.name+".tmp")
tmp.write_bytes(raw);assert tmp.read_bytes()==raw;os.replace(tmp,path)
print(json.dumps({k:v for k,v in result.items() if k!="checks"}))
