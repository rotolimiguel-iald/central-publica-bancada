"""Restricted public downloads under the witnessed E2/E3.2 job manifest.

No credentials. No posterior sample is opened by this module. Byte receipts
distinguish provider checksums from local hashes; an absent checksum stays open.
"""
import argparse,hashlib,json,os,time,urllib.request,urllib.parse
from datetime import datetime,timezone
from registration_guard import checked_registration,time_guard,authorize_event,output_path,sha,load_authorized_configuration,publish_new

ALLOWED_HOSTS={'gwosc.org','www.gwosc.org','zenodo.org'}

def validate_url(url):
    p=urllib.parse.urlsplit(url)
    if p.scheme!='https' or p.hostname not in ALLOWED_HOSTS or p.username or p.password or p.query or p.fragment:
        raise ValueError('Unregistered public download host or credential/query-bearing URL')
    return url

class PublicRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        validate_url(newurl)
        return super().redirect_request(req,fp,code,msg,headers,newurl)

def fetch(reg,digest,key,recipes):
    if key not in recipes:raise ValueError('Download not in witnessed recipe')
    cfg=recipes[key];authorize_event(reg,cfg['event'],cfg['mode']);time_guard(reg)
    if cfg['kind'] not in ('public_strain','public_posterior'):raise ValueError('Invalid science download kind')
    url=validate_url(cfg['url']);target=output_path(cfg['filename']);receipt=target.with_suffix(target.suffix+'.receipt.json')
    partial=target.with_suffix(target.suffix+'.partial')
    if any(p.exists() for p in (target,receipt,partial)):raise FileExistsError('Existing download/attempt; preserve it')
    size_limit=cfg['maximum_bytes']
    if type(size_limit) is not int or size_limit<=0 or size_limit>3_000_000_000:raise ValueError('Invalid download ceiling')
    if not cfg.get('license_source') or not cfg.get('license_status'):raise ValueError('Per-file license metadata required')
    expected=cfg.get('provider_checksum');algorithm=cfg.get('provider_checksum_algorithm')
    if expected is not None and algorithm not in ('md5','sha256'):raise ValueError('Unsupported provider checksum')
    h=hashlib.sha256();external=hashlib.new(algorithm) if expected is not None else None
    started=datetime.now(timezone.utc).isoformat();wall=time.perf_counter();count=0
    opener=urllib.request.build_opener(PublicRedirect())
    try:
        timeout=min(30.,time_guard(reg).timestamp()-time.time()-5.)
        if timeout<1:raise TimeoutError('Insufficient budget for download and receipt')
        with opener.open(urllib.request.Request(url,headers={'User-Agent':'IALD-013BIS-reproducibility/1'}),timeout=timeout) as response,partial.open('xb') as f:
            final_url=validate_url(response.geturl())
            while True:
                # A socket read is bounded by timeout; never begin one whose
                # bound extends beyond the reserved deadline margin.
                if time_guard(reg).timestamp()-time.time()<timeout+5:raise TimeoutError('Preserve partial before deadline')
                block=response.read(1024*1024)
                if not block:break
                count+=len(block)
                if count>size_limit:raise ValueError('Download exceeds witnessed ceiling')
                f.write(block);h.update(block)
                if external:external.update(block)
        if count==0:raise ValueError('Empty download')
        if external and external.hexdigest().lower()!=expected.lower():raise ValueError('Provider checksum mismatch; partial retained')
        time_guard(reg);os.link(partial,target);partial.unlink()
        value={'status':'PUBLIC_BYTES_DOWNLOADED_NOT_SAMPLES_READ','registration_sha256':digest,'recipe':key,
          'event':cfg['event'],'mode':cfg['mode'],'url':url,'final_url':final_url,'sha256':h.hexdigest(),'bytes':count,
          'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),'wall_seconds':time.perf_counter()-wall,
          'provider_checksum_verified':external is not None,'provider_checksum':expected,
          'license_status':cfg['license_status'],'license_source':cfg['license_source'],
          'downloader_sha256':sha(__file__),'posterior_values_read':False}
        time_guard(reg);publish_new(receipt,value)
        return {'receipt':str(receipt),'sha256':h.hexdigest(),'bytes':count}
    except Exception:
        # Failed bytes remain next to the uncreated target, never silently reused.
        raise

def main():
    p=argparse.ArgumentParser();p.add_argument('--recipe',required=True);args=p.parse_args()
    reg,digest=checked_registration()
    # New recipes require an E2 amendment or a separately witnessed E3.2
    # allocation read by the common registration guard; never ad-hoc URL input.
    view=load_authorized_configuration(reg,digest)
    recipes=view['downloads']
    print(json.dumps(fetch(reg,digest,args.recipe,recipes)))

if __name__=='__main__':main()
