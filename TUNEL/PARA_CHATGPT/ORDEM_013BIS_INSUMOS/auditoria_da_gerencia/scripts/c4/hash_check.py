import hashlib, json, os, sys
R = r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN"
man = json.load(open(os.path.join(R, "cache", "MANIFESTO_DOWNLOADS.json"), encoding="utf-8"))
want = {}
for f in man["files"]:
    want[f["path"].replace("/", "\\")] = f
targets = [
 r"cache\public\17018009\TGR_companion_S250114ax_results.tar.gz",
 r"cache\public\17018009\extracted\TGR_companion_S250114ax_results\gw250114_pseobnr\posterior_samples.h5",
 r"cache\public\21454847\pSEOB.tar.gz",
 r"cache\public\21454847\extracted\pSEOB\metafiles\pSEOB_GW250114_082203_Prod0.h5",
 r"cache\public\21454847\extracted\pSEOB\metafiles\pSEOB_GW150914_095045_Prod0.h5",
 r"cache\public\21454847\extracted\pSEOB\metafiles\pSEOB_GW231028_153006_Prod0.h5",
 r"cache\public\21454847\extracted\pSEOB\metafiles\pSEOB_GW190521_074359_Prod0.h5",
 r"cache\public\17461225\IGWN-GWTC3-TGR-v2-rin.zip",
 r"cache\public\17461225\extracted\rin\rin_S150914_pseobnrv4hm.h5",
 r"cache\public\17461225\extracted\rin\rin_S200129m_pseobnrv4hm.h5",
 r"cache\public\17018009\selected\3ec4616b581f990b.dat",
]
out = []
for t in targets:
    p = os.path.join(R, t)
    h = hashlib.sha256(); m5 = hashlib.md5(); n = 0
    with open(p, "rb") as fh:
        while True:
            b = fh.read(1 << 22)
            if not b: break
            h.update(b); m5.update(b); n += len(b)
    w = want.get(t)
    rec = dict(path=t, bytes=n, sha256=h.hexdigest(), md5=m5.hexdigest(),
               manifest_sha256=(w or {}).get("sha256"), manifest_bytes=(w or {}).get("bytes"),
               match=(w is not None and w["sha256"] == h.hexdigest() and w["bytes"] == n))
    out.append(rec); print(json.dumps(rec), flush=True)
json.dump(out, open("hash_check_result.json", "w"), indent=1)
