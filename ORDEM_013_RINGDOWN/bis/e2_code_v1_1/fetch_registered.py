"""Restricted public downloads under the witnessed E2/E3.2 job manifest.

No credentials. No posterior sample is opened by this module. Byte receipts
distinguish provider checksums from local hashes; an absent checksum stays open.
"""
import argparse,hashlib,json,os,time,signal,threading,urllib.request,urllib.parse
from datetime import datetime,timezone
from registration_guard import checked_registration,time_guard,authorize_event,output_path,sha,load_authorized_configuration,publish_new,contained

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
    """Bound the whole own-process operation, including slow streaming reads."""
    if not hasattr(signal,'setitimer') or threading.current_thread() is not threading.main_thread():
        raise RuntimeError('Download wall deadline requires Unix main-thread signal timer')
    if signal.getitimer(signal.ITIMER_REAL)!=(0.,0.):
        raise RuntimeError('Refuse to replace an existing wall timer')
    remaining=time_guard(reg).timestamp()-time.time()-3.
    if remaining<=0:raise TimeoutError('No download budget remains')
    previous=signal.getsignal(signal.SIGALRM)
    def expired(signum,frame):raise TimeoutError('Registered download wall deadline reached')
    signal.signal(signal.SIGALRM,expired)
    signal.setitimer(signal.ITIMER_REAL,remaining)
    try:return _fetch(reg,digest,key,recipes)
    finally:
        signal.setitimer(signal.ITIMER_REAL,0.)
        signal.signal(signal.SIGALRM,previous)


def _fetch(reg,digest,key,recipes):
    if key not in recipes:raise ValueError('Download not in witnessed recipe')
    cfg=recipes[key];authorize_event(reg,cfg['event'],cfg['mode']);time_guard(reg)
    canonical=lambda value:hashlib.sha256(json.dumps(value,sort_keys=True,allow_nan=False).encode()).hexdigest()
    view=load_authorized_configuration(reg,digest)
    if canonical(view['downloads'].get(key))!=canonical(cfg):raise ValueError('Recipe does not match active witnessed configuration')
    allocation_sha=view['_allocation_sha256'];config_sha=None
    if allocation_sha is not None:
        allocation=json.loads(contained(reg['allocation_policy']['relative_to_Chatgpt']).read_bytes())
        config_sha=allocation['jobs_sha256']
    recipe_sha=canonical(cfg)
    if cfg['kind'] not in ('public_strain','public_posterior'):raise ValueError('Invalid science download kind')
    url=validate_url(cfg['url']);target=output_path(cfg['filename']);receipt=target.with_suffix(target.suffix+'.receipt.json')
    partial=target.with_suffix(target.suffix+'.partial')
    if any(p.exists() for p in (target,receipt,partial)):raise FileExistsError('Existing download/attempt; preserve it')
    size_limit=cfg['maximum_bytes']
    if type(size_limit) is not int or size_limit<=0 or size_limit>3_000_000_000:raise ValueError('Invalid download ceiling')
    if not cfg.get('license_source') or not cfg.get('license_status'):raise ValueError('Per-file license metadata required')
    expected=cfg.get('provider_checksum');algorithm=cfg.get('provider_checksum_algorithm')
    if expected is not None and algorithm not in ('md5','sha256'):raise ValueError('Unsupported provider checksum')
    expected_size=cfg.get('expected_bytes')
    if expected_size is not None and (type(expected_size) is not int or not 0<expected_size<=size_limit):raise ValueError('Invalid declared provider size')
    h=hashlib.sha256();external=hashlib.new(algorithm) if expected is not None else None
    started=datetime.now(timezone.utc).isoformat();wall=time.perf_counter();count=0
    opener=urllib.request.build_opener(PublicRedirect())
    try:
        timeout=min(30.,time_guard(reg).timestamp()-time.time()-5.)
        if timeout<1:raise TimeoutError('Insufficient budget for download and receipt')
        with opener.open(urllib.request.Request(url,headers={'User-Agent':'IALD-013BIS-reproducibility/1','Accept-Encoding':'identity'}),timeout=timeout) as response,partial.open('xb') as f:
            final_url=validate_url(response.geturl())
            if response.headers.get('Content-Encoding') not in (None,'identity'):raise ValueError('Unexpected encoded response')
            length=response.headers.get('Content-Length');http_length=int(length) if length is not None else None
            if http_length is not None and not 0<http_length<=size_limit:raise ValueError('Invalid HTTP length')
            while True:
                # Socket timeout bounds inactivity, not total streaming time.
                # The outer signal timer enforces the whole-operation deadline.
                if time_guard(reg).timestamp()-time.time()<timeout+5:raise TimeoutError('Preserve partial before deadline')
                block=response.read(1024*1024)
                if not block:break
                count+=len(block)
                if count>size_limit:raise ValueError('Download exceeds witnessed ceiling')
                f.write(block);h.update(block)
                if external:external.update(block)
        if count==0:raise ValueError('Empty download')
        if http_length is not None and count!=http_length:raise ValueError('Truncated or oversized HTTP response; partial retained')
        if expected_size is not None and count!=expected_size:raise ValueError('Provider metadata size mismatch; partial retained')
        if expected_size is None and http_length is None and external is None:raise ValueError('No provider completeness check; retain unvalidated partial')
        if external and external.hexdigest().lower()!=expected.lower():raise ValueError('Provider checksum mismatch; partial retained')
        fresh=load_authorized_configuration(reg,digest)
        if fresh['_allocation_sha256']!=allocation_sha or canonical(fresh['downloads'].get(key))!=recipe_sha:
            raise ValueError('Download authorization changed before promotion')
        time_guard(reg);os.link(partial,target);partial.unlink()
        value={'status':'PUBLIC_BYTES_DOWNLOADED_NOT_SAMPLES_READ','registration_sha256':digest,'recipe':key,
          'event':cfg['event'],'mode':cfg['mode'],'url':url,'final_url':final_url,'sha256':h.hexdigest(),'bytes':count,
          'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),'wall_seconds':time.perf_counter()-wall,
          'provider_checksum_verified':external is not None,'provider_checksum':expected,
          'HTTP_content_length':http_length,'provider_expected_bytes':expected_size,'size_checks_passed':True,
          'allocation_sha256':allocation_sha,'jobs_configuration_sha256':config_sha,'recipe_sha256':recipe_sha,
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
