import json,sys
d=json.load(open("draws400.json"))["draws"]
def item(r,label,fmax,fix440=False):
    p=dict(r["parameters"]); p={k:p[k] for k in ('mass_1','mass_2','chi_1','chi_2','luminosity_distance','theta_jn','phase','geocent_time','dtau220','dtau440','domega220','domega440')}
    if fix440: p["dtau440"]=0.0; p["domega440"]=0.0
    return {"label":label,"fmax":fmax,"parameters":p}
# A: original config, 4 free, fmax 1024, draws 1..400 in bilby order
json.dump([item(r,"orig_d%d"%r["draw"],1024) for r in d],open("items_orig1024.json","w"))
# B: so-220 (440 fixed at GR), fmax 1024 and 2048, draws 1..120
json.dump([item(r,"s220_1024_d%d"%r["draw"],1024,True) for r in d[:120]],open("items_s220_1024.json","w"))
json.dump([item(r,"s220_2048_d%d"%r["draw"],2048,True) for r in d[:120]],open("items_s220_2048.json","w"))
# C: 220+440 free at fmax 2048, draws 1..120 (does the -6 abort recur beyond draw 8?)
json.dump([item(r,"both_2048_d%d"%r["draw"],2048) for r in d[:120]],open("items_both_2048.json","w"))
