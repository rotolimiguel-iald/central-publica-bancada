"""Discover public GWOSC frame metadata for the 33 registered calibration events."""
import hashlib, json, time, urllib.request, urllib.parse, urllib.error
from datetime import datetime, timezone
from pathlib import Path
B=Path(r"C:\IALD\Central de Patentes\Chatgpt")
R=B/"ORDEM_013_RINGDOWN"; D=R/"bis/015/t07/metadata"
D.mkdir(parents=True,exist_ok=True)
def sha(raw):return hashlib.sha256(raw).hexdigest()
catalog=R/"C4_CATALOG_220.json"
catalog_sha=sha(catalog.read_bytes())
events=[row["event"] for row in json.loads(catalog.read_bytes())["rows"]]
assert len(events)==33 and len(set(events))==33
def get(url,p):
    if p.exists():
        raw=p.read_bytes()
    else:
        req=urllib.request.Request(url,headers={"Accept":"application/json","User-Agent":"IALD-T07-calibration-metadata/1.0"})
        with urllib.request.urlopen(req,timeout=20) as response:
            raw=response.read()
        with p.open("xb") as f:f.write(raw)
    return json.loads(raw),sha(raw)
rows=[]
for name in events:
    line={"event":name}
    try:
        api_name=name
        try:
            info,h=get("https://gwosc.org/api/v2/events/"+urllib.parse.quote(api_name,safe="")+"?format=json",D/(name+"_event.json"))
        except urllib.error.HTTPError as exc:
            if exc.code!=404 or "_" not in name: raise
            api_name=name.split("_",1)[0]
            info,h=get("https://gwosc.org/api/v2/events/"+urllib.parse.quote(api_name,safe="")+"?format=json",D/(name+"_event.json"))
        line["event_api_name"]=api_name
        line["event_api_sha256"]=h
        versions=info["versions"]
        latest=max(versions,key=lambda v:v["version"])
        detail,h=get(latest["detail_url"],D/(name+"_detail.json"))
        line.update(version=latest["version"],catalog=latest["catalog"],detail_api_sha256=h,gps=detail["gps"],detectors=detail["detectors"])
        gps=int(detail["gps"])
        query=urllib.parse.urlencode({"format":"json","start":gps-16,"stop":gps+16,"sample-rate":4,"pagesize":100})
        files,h=get("https://gwosc.org/api/v2/strain-files?"+query,D/(name+"_frames.json"))
        line["frame_api_sha256"]=h
        line["frames"]=[{"detector":f["detector"],"gps_start":f["gps_start"],"hdf5_url":f["hdf5_url"]} for f in files["results"] if f["detector"] in detail["detectors"]]
        line["status"]="METADATA_FOUND" if line["frames"] else "NO_4KHZ_FRAMES"
    except Exception as exc:
        line["status"]="API_ERROR"
        line["error"]=type(exc).__name__+":"+str(exc)[:200]
    rows.append(line)
    print(json.dumps({"event":name,"status":line["status"],"frames":len(line.get("frames",[]))}),flush=True)
    time.sleep(.05)
out={"status":"T07_METADATA_ONLY_NO_STRAIN_DOWNLOADED","created_utc":datetime.now(timezone.utc).isoformat(),"catalog_sha256":catalog_sha,"event_count":len(events),"rows":rows,"license":"GWOSC API public data CC BY 4.0; individual file licenses to be verified before download","no_gate_change":True}
p=D/"DISCOVERY_v2.json"
raw=(json.dumps(out,ensure_ascii=False,indent=2)+"\n").encode()
with p.open("xb") as f:f.write(raw)
print(json.dumps({"discovery_sha256":sha(raw),"found":sum(r["status"]=="METADATA_FOUND" for r in rows),"errors":sum(r["status"]=="API_ERROR" for r in rows)}))
