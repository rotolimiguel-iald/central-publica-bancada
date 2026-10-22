"""F2 conditional algebra and forecast; no data fitting, no canonical imports."""
from pathlib import Path
import datetime, hashlib, json, math, os, re, time, urllib.request

ROOT = Path(__file__).resolve().parent
def sha(b): return hashlib.sha256(b).hexdigest()
def write(name, data):
    p=ROOT/name; p.parent.mkdir(parents=True,exist_ok=True)
    b=data if isinstance(data,bytes) else data.encode("utf-8")
    if p.exists():
        stamp=datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        p.with_name(p.name+".bak_"+stamp).write_bytes(p.read_bytes())
    t=p.with_name(p.name+".tmp")
    t.write_bytes(b)
    assert t.stat().st_size==len(b)
    os.replace(t,p)
    assert p.read_bytes()==b
def dump(name,obj):write(name,json.dumps(obj,ensure_ascii=False,indent=2)+"\n")
T0=time.perf_counter()
SOURCE=Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py")
raw=SOURCE.read_bytes()
lines=raw.decode("utf-8").splitlines()
m=re.search(r"^ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)",raw.decode("utf-8"),re.M)
assert m
alpha=float(m.group(1)); beta=alpha*math.sqrt(math.e)
local_sources=[]
def capture(path, spans=None):
    p=Path(path); b=p.read_bytes()
    record={"path":str(p),"sha256":sha(b),"bytes":len(b),"role":"scientific reference read only"}
    if spans:
        ll=b.decode("utf-8").splitlines()
        excerpts=[{"first_line":a,"last_line":z,"text":"\n".join(ll[a-1:z])} for a,z in spans]
        name="source_excerpts/"+p.name+".json"
        dump(name,{"source":record,"excerpts":excerpts})
        record["excerpts_file"]=name
    local_sources.append(record)
capture(SOURCE,[(2879,2959),(4215,4283),(4584,4641),(193616,193650),(199223,199289)])
capture(r"C:\IALD\Bancada_Um\bancada\motor.py",[(180,219)])
capture(r"C:\IALD\Bancada_Um\bancada\fundo_gpu.py",[(130,159)])
capture(r"C:\IALD\Central de Patentes\memory\TGL_ATLAS.md",[(31800,31803),(31842,31843),(32061,32066)])
base=Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT")
for p in [base/"ORDEM_018_o_discriminante.md",base/"ORDEM_015_INSUMOS/PROTOCOLO_ANTI_PAREDE.md",base/"ORDEM_018_INSUMOS/VERBO_operador_05out.txt",ROOT/"mapas_consultados.json",ROOT/"PLANO_F2_ANTES_DOS_CALCULOS.md",Path(__file__)]:
    capture(p)

def E(z,om):return math.sqrt(om*(1+z)**3+1-om)
def k(z,om,b):return E(z,om)**(2*b/3)
def simpson(fn,z,n):
    h=z/n
    return h/3*(fn(0)+fn(z)+4*sum(fn(i*h) for i in range(1,n,2))+2*sum(fn(i*h) for i in range(2,n,2)))
def Q(z,om,b,n):return simpson(lambda u:k(u,om,b)/E(u,om),z,n)/simpson(lambda u:1/E(u,om),z,n)
rows=[]
checks=[]
for om in [.25,.3,.35]:
    for z in [.1,.5,1.,1.5,2.3,3.]:
        q=Q(z,om,beta,4000); q2=Q(z,om,beta,2000); kz=k(z,om,beta)
        checks.extend([abs(q-q2)<1e-10,1<=q<=kz,abs(Q(z,om,0.,2000)-1)<1e-14])
        rows.append({"om":om,"z":z,"endpoint_k_minus_1":kz-1,
                     "distance_ratio_Q_minus_1":q-1,"magnitude_shift_vs_shadow":5*math.log10(q),
                     "refinement_absolute":abs(q-q2),
                     "conditional_lens_endpoint_proxy_sigma":70*(kz-1)/3.9})
gamma=.5*beta*math.sqrt((6.62607015e-34/(2*math.pi))*6.67430e-11/299792458.**5)*(2*math.pi*100)**2
s8_ratio=math.sqrt(1+beta)-1
m2=beta*math.sin(math.pi/4)
result={
 "status":"DERIVED_CONDITIONAL_ALGEBRA__NO_NEW_OBSERVATIONAL_VERDICT",
 "at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "protocol_sha256":sha((ROOT/"PLANO_F2_ANTES_DOS_CALCULOS.md").read_bytes()),
 "scientific_source_sha256":sha(raw),"alpha_fine_codata_2018_from_source":alpha,"beta_runtime":beta,
 "fiducial":{"H0":70,"Omega_m":.3,"Omega_r":0,"domain_z_max":3,
             "statute":"INPUT illustrative flat matter+Lambda, no fitted target"},
 "distance_rows":rows,
 "S8":{"algebraic_ratio_minus_1_at_fixed_sigma8":s8_ratio,"reference_input_S8":.8,
       "conditional_delta":.8*s8_ratio,"published_larger_sigma":.021,
       "optimistic_conditional_proxy_sigma":.8*s8_ratio/.021,
       "prediction_status":"OPEN full perturbation dynamics required"},
 "clock":{"Gamma_at_100_Hz_per_s_identity_only":gamma,"required_sigma_Gamma_5sigma":gamma/5,
          "measurement_repeated":False,"tau_star_status":"tP identification, c cubed alone supplies no new scale"},
 "neutrino":{"m2_eV":m2,"dm21_eV2_given_m1_zero":m2*m2,
             "m1_zero_NO_scale_angle_are_conditions":True,
             "JUNO_sigma_dm21_eV2":.12e-5,
             "rival_discrimination_sigma":None,"reason":"LCDM does not predict a unique dm21",
             "sum_reopened":False,"sum_supersession_source_lines":[4275,4277]},
 "validation":{"all_checks_passed":all(checks),"checks":len(checks),
               "beta_zero_limit":True,"quadrature_refinement_abs_tolerance":1e-10},
 "provider_request_ids":[], "provider_response_status":"No external model call in this subtask",
 "elapsed_seconds":time.perf_counter()-T0
}
assert result["validation"]["all_checks_passed"]
dump("F2_CALCULOS_CONDICIONAIS.json",result)
sources=[
 ("tdcosmo","https://arxiv.org/abs/2506.03023v4"),
 ("kids","https://arxiv.org/abs/2503.19441"),
 ("temperature_direct","https://arxiv.org/abs/1502.07858"),
 ("temperature_joint","https://arxiv.org/abs/1511.04335"),
 ("temperature_duality","https://arxiv.org/abs/1112.1862"),
 ("juno","https://arxiv.org/abs/2511.14593v1")]
remote=[]
for name,url in sources:
    rec={"name":name,"url":url,"purpose":"primary published sigma and definition; centres not used for verdict"}
    try:
        req=urllib.request.Request(url,headers={"User-Agent":"IALD-research/1.0"})
        with urllib.request.urlopen(req,timeout=20) as r:
            data=r.read(); rec["resolved_url"]=r.url
        write("public_sources/"+name+".html",data)
        rec.update(sha256=sha(data),bytes=len(data),path="public_sources/"+name+".html",status="READ_BY_HASH")
    except Exception as e:
        rec.update(status="READ_FAILED",error=repr(e))
    remote.append(rec)
dump("F2_FONTES_SHA256.json",{"at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"local":local_sources,"primary_web":remote,
     "caveat":"Web abstracts contain known central values; no central was used in forecasts or new verdict."})
print(json.dumps({"calculation_seconds":result["elapsed_seconds"],"beta":beta,"z1":[r for r in rows if r["om"]==.3 and r["z"]==1],"z23":[r for r in rows if r["om"]==.3 and r["z"]==2.3],"S8":result["S8"],"clock":result["clock"],"neutrino":result["neutrino"],"web":[{"name":r["name"],"status":r["status"]}for r in remote]},ensure_ascii=False,indent=2))
