import json,sys,h5py
def plain(x):
    if isinstance(x,bytes): return x.decode('utf-8','replace')
    if hasattr(x,'tolist'): return plain(x.tolist())
    if isinstance(x,(list,tuple)): return [plain(a) for a in x[:20]]
    return x
with h5py.File(sys.argv[1],'r') as f:
    d=f['strain/Strain']
    print(json.dumps({'shape':d.shape,'dtype':str(d.dtype),'attrs':{k:plain(v) for k,v in d.attrs.items()},
                     'meta':{k:plain(f['meta'][k][()]) for k in f['meta'] if f['meta'][k].size<32},
                     'quality':list(f['quality'].keys()) if 'quality' in f else []},default=str))
