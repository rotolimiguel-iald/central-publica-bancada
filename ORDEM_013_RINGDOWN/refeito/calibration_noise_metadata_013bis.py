"""Inspect only HDF metadata/quality masks of existing calibration noise."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, time
import h5py
import numpy as np

B = Path(__file__).resolve().parents[1]
R = B.parent

def sha(path):
    value=hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda:stream.read(1024*1024),b''): value.update(chunk)
    return value.hexdigest()

def main():
    started=time.perf_counter()
    regpath=B/'RINGDOWN_5SIGMA_V1.json'
    reg=json.loads(regpath.read_bytes()); cfg=reg['pe_jobs']['GW250114_PILOT']
    results=[]
    first_slot=1420874240
    for detector in cfg['detectors']:
        entry=cfg['data'][detector]
        path=(R/entry['offsource_path']).resolve()
        if not path.is_relative_to(B/'cache'): raise ValueError('Outside cache')
        actual=sha(path)
        if actual!=entry['offsource_sha256']: raise ValueError('Changed noise source')
        with h5py.File(path,'r') as handle:
            raw=handle['strain/Strain'] # shape/attributes only, never indexed
            gps=float(handle['meta/GPSstart'][()]); fs=1/float(raw.attrs['Xspacing'])
            masks=[]; descriptions=[]
            for group,field,namesfield,required in (
                ('quality/simple','DQmask','DQShortnames',cfg['quality_required']),
                ('quality/injections','Injmask','InjShortnames',cfg['injection_flags_required'])):
                names=[x.decode() if isinstance(x,bytes) else str(x) for x in handle[group+'/'+namesfield][()]]
                if not set(required)<=set(names): raise ValueError('Required flags missing')
                bits=sum(1<<names.index(x) for x in required)
                values=handle[group+'/'+field][()]
                if values.ndim!=1 or values.dtype.kind not in 'iu': raise ValueError('Invalid mask')
                masks.append((values&bits)==bits)
                descriptions.append({'group':group,'names':names,'required':required})
            if masks[0].shape!=masks[1].shape: raise ValueError('Mask cadence mismatch')
            good=masks[0]&masks[1]
            if not np.isfinite([gps,fs]).all() or fs!=4096 or len(good)!=raw.shape[0]/fs: raise ValueError('Metadata extent mismatch')
            length=int(cfg['psd_duration_s']); psd=None
            for offset in range(len(good)-length+1):
                if gps+offset+length>first_slot: break
                if bool(good[offset:offset+length].all()):
                    psd=[gps+offset,gps+offset+length]; break
            slots=[]
            for index in range(112):
                start=first_slot+32*index; off=int(start-gps)
                inside=off>=0 and off+16<=len(good)
                slots.append({'index':index,'start_GPS':start,'end_GPS':start+16,
                              'within_file':inside,'passes_flags':bool(good[off:off+16].all()) if inside else False})
            results.append({'detector':detector,'file_sha256':actual,'file':entry['offsource_path'],
                'GPS_start':gps,'duration_seconds':len(good),'sample_rate_hz':fs,
                'strain_shape':list(raw.shape),'flags':descriptions,'first_flag_valid_PSD_interval_before_candidate_slots':psd,
                'candidate_slots':slots})
    common=[i for i in range(112) if all(row['candidate_slots'][i]['passes_flags'] for row in results)]
    value={'status':'CALIBRATION_NOISE_FLAGS_REVIEWED_NOT_STRAIN_OR_PSD_FINITENESS',
        'created_utc':datetime.now(timezone.utc).isoformat(),'registration_sha256':sha(regpath),
        'script_sha256':sha(Path(__file__)),'wall_seconds':time.perf_counter()-started,
        'results':results,'common_flag_valid_slot_indices':common,
        'scope':'Existing known-event noise files only. Hashes read raw bytes for integrity; no strain samples decoded. Candidate slot geometry from injection preparation, not an allocation or selection by noise level. PSD positivity/stationarity/finiteness, waveform support, achieved injection SNR and population transfer remain OPEN.'}
    target=B/'bis/E3_CALIBRATION_NOISE_METADATA_V1.json'; tmp=target.with_name(target.name+'.pending')
    data=(json.dumps(value,indent=2,allow_nan=False)+'\n').encode()
    with tmp.open('xb') as stream: stream.write(data);stream.flush();os.fsync(stream.fileno())
    if tmp.stat().st_size!=len(data): raise IOError('Incomplete receipt')
    os.link(tmp,target);tmp.unlink()
    print(json.dumps({'path':str(target),'sha256':sha(target),'common_flag_valid_slots':len(common),
        'first_flag_valid_PSDs':{v['detector']:v['first_flag_valid_PSD_interval_before_candidate_slots'] for v in results},'status':value['status']}))

if __name__=='__main__':main()
