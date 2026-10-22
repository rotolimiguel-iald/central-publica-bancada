import sys,os,json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import probe
OUT=probe.OUT
rows=json.load(open(OUT+"/replay24.json"))
base=dict(rows[15])
res=[]
for a in [-0.8,0.0,0.5,1.0,2.0]:
    first=None
    for b in [1.0+0.25*k for k in range(13)]:
        p=dict(base);p['dtau220']=a;p['dtau440']=b
        x=probe.run(p,1024,f"l_{a}_{b}");x['dtau220']=a;x['dtau440']=b;res.append(x)
        if x['rc']!=0 and first is None:first=b
    print("dtau220",a,"first crash dtau440 >=",first,flush=True)
json.dump(res,open(OUT+"/line_draw16_fmax1024.json","w"),indent=1)
# QNM freqs of the remnant for draw 16 (SEOBNRv4 fit)
import lal,lalsimulation as ls
m1,m2=base['mass_1'],base['mass_2'];c1,c2=base['chi_1'],base['chi_2']
v=lal.CreateCOMPLEX16Vector(1)
out={}
for (l,m) in [(2,2),(4,4)]:
    ls.SimIMREOBGenerateQNMFreqV2(v,m1,m2,[0,0,c1],[0,0,c2],l,m,1,ls.SEOBNRv4)
    out[f"{l}{m}"]={"re":v.data[0].real,"im":v.data[0].imag}
print("QNM",json.dumps(out))
print("Im440/Im220",out["44"]["im"]/out["22"]["im"])
