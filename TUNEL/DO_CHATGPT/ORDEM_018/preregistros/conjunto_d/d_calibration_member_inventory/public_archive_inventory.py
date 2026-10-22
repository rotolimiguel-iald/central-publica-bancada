"""Bounded public calibration-archive header inventory. No numerical member reader."""
import argparse
import datetime as dt
import hashlib
from html.parser import HTMLParser
import io
import json
import os
from pathlib import Path
import re
import tarfile
import gzip
import urllib.parse
import urllib.request

BASE = Path(__file__).resolve().parent
DROOT = BASE.parent
ROOT = DROOT.parent.parent
PAGE = 'https://dcc.ligo-wa.caltech.edu/LIGO-T2500288/public'
HOSTS = {'dcc.ligo-wa.caltech.edu', 'dcc.ligo.org'}
NAMES = ('LIGO_O4a_cal_uncertainty.tgz', 'LIGO_O4b_cal_uncertainty.tgz')
EACH = 50 * 1024 * 1024
TOTAL = 100 * 1024 * 1024
EXPANDED = 8 * 1024 * 1024 * 1024
MAX_MEMBERS = 100000

def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def sha(data):
    return hashlib.sha256(data).hexdigest()

def new_bytes(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() or path.with_suffix(path.suffix+'.tmp').exists():
        raise FileExistsError('Refusing repeat/overwrite: '+str(path))
    tmp = path.with_suffix(path.suffix+'.tmp')
    with tmp.open('xb') as f:
        f.write(data)
    if tmp.stat().st_size != len(data):
        raise RuntimeError('Incomplete atomic write')
    os.replace(tmp, path)

def new_json(name, value):
    new_bytes(BASE/name, (json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))

def allowed(url, archive=None):
    p=urllib.parse.urlsplit(url)
    if p.scheme!='https' or p.hostname not in HOSTS or p.username or p.password:
        raise ValueError('Nonofficial URL refused')
    if archive:
        if urllib.parse.unquote(p.path).rsplit('/',1)[-1] != archive or '/T2500288/' not in p.path or not p.path.startswith('/public/'):
            raise ValueError('Archive URL identity mismatch')
    elif not (p.path.startswith('/LIGO-T2500288') or '/T2500288/' in p.path):
        raise ValueError('Document identity mismatch')

class Redirect(urllib.request.HTTPRedirectHandler):
    def __init__(self, archive=None):
        super().__init__(); self.archive=archive; self.hops=[]
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        allowed(newurl,self.archive)
        if len(self.hops)>=3: raise RuntimeError('Redirect limit')
        self.hops.append({'from':req.full_url,'to':newurl,'http_status':code})
        return super().redirect_request(req,fp,code,msg,headers,newurl)

def open_once(url, method='GET', archive=None):
    allowed(url,archive)
    handler=Redirect(archive)
    opener=urllib.request.build_opener(handler)
    request=urllib.request.Request(url, method=method, headers={'User-Agent':'IALD-D-calibration-documentary/1.0','Accept-Encoding':'identity'})
    return opener.open(request,timeout=40), handler

class Links(HTMLParser):
    def __init__(self):
        super().__init__();self.links=[];self.active=None
    def handle_starttag(self,tag,attrs):
        if tag=='a':
            self.active={'href':dict(attrs).get('href',''),'label':''}
    def handle_data(self,data):
        if self.active is not None:self.active['label']+=data
    def handle_endtag(self,tag):
        if tag=='a' and self.active is not None:
            self.links.append(self.active);self.active=None

def discover():
    new_json('DISCOVERY_ATTEMPT_STARTED.json',{'at':now(),'request_id':'a178d269-5b24-443a-b59b-4060aebe9a4c','page':PAGE,'automatic_retries':0})
    req_path=ROOT/'D_CALIBRATION_MEMBER_INVENTORY_REQUEST.json'
    request=json.loads(req_path.read_bytes())
    for p in [req_path,Path(request['source_receipt']['path']),DROOT/'PROPOSTA_MANIFESTO_METADATA_D.json',DROOT/'d_metadata_semantics'/'MANIFESTO_ENTREGA.json']:
        data=p.read_bytes()
        if p.name==Path(request['source_receipt']['path']).name:
            pin=request['source_receipt']
            if len(data)!=pin['bytes'] or sha(data)!=pin['sha256']:raise ValueError('ROOT receipt pin mismatch')
        new_bytes(BASE/'sources_local'/p.name,data)
    try:
        response,handler=open_once(PAGE)
        with response as r:
            kind=r.headers.get_content_type()
            if kind!='text/html':raise ValueError('Expected official HTML')
            data=r.read(1_000_001)
            if len(data)>1_000_000:raise ValueError('Document size limit')
            final=r.url
        text=data.decode('utf-8')
        if 'T2500288-v5' not in text:raise ValueError('Document not confirmed v5')
        new_bytes(BASE/'sources_public'/'DCC_T2500288_v5.html',data)
        parser=Links();parser.feed(text)
        rows=[]
        for name in NAMES:
            candidates={urllib.parse.urljoin(final,l['href']) for l in parser.links if name in l['label'] or urllib.parse.unquote(l['href']).rsplit('/',1)[-1]==name}
            if len(candidates)!=1:raise ValueError('Ambiguous/missing published URL: '+name)
            url=candidates.pop();allowed(url,name)
            row={'archive':name,'url_as_published':url,'source_page':final,'source_page_sha256':sha(data)}
            try:
                response,h=open_once(url,'HEAD',name)
                with response as r:
                    length=r.headers.get('Content-Length')
                    n=int(length) if length is not None else None
                    if n is not None and (n<0 or n>EACH):raise ValueError('Declared archive size exceeds cap')
                    row.update(head_status='OK',head_http_status=r.status,head_final_url=r.url,
                        declared_bytes=n,content_type=r.headers.get_content_type(),etag=r.headers.get('ETag'),
                        last_modified=r.headers.get('Last-Modified'),redirects=h.hops)
            except Exception as exc:
                row.update(head_status='FAILED_NO_RETRY',error=f'{type(exc).__name__}: {exc}')
            rows.append(row)
        ready=all(x['head_status']=='OK' for x in rows) and sum(x.get('declared_bytes') or 0 for x in rows)<=TOTAL
        new_json('DISCOVERY.json',{'at':now(),'page':final,'page_sha256':sha(data),'page_bytes':len(data),'archives':rows,
            'ready_for_bounded_download':ready,'per_archive_cap':EACH,'total_cap':TOTAL,
            'unknown_length_rule':'Only stream with hard byte limit; HEAD failure stops, no retry.',
            'public_member_index_candidates':[l for l in parser.links if re.search(r'manifest|inventory|member.?list|index.*cal',l['label'],re.I)],
            'page_redirects':handler.hops})
        print(json.dumps({'ready_for_bounded_download':ready,'archives':rows},ensure_ascii=False),flush=True)
    except Exception as exc:
        new_json('DISCOVERY_FAILED.json',{'at':now(),'error':f'{type(exc).__name__}: {exc}','automatic_retry':False})
        raise

def download():
    info=json.loads((BASE/'DISCOVERY.json').read_bytes())
    if info['ready_for_bounded_download'] is not True:raise RuntimeError('Discovery not qualified')
    new_json('DOWNLOAD_ATTEMPT_STARTED.json',{'at':now(),'automatic_retries':0,'archives':list(NAMES),'cap_each':EACH,'cap_total':TOTAL})
    total=0;rows=[]
    for meta in info['archives']:
        name=meta['archive'];url=meta['url_as_published'];part=BASE/'archives'/(name+'.part')
        part.parent.mkdir(exist_ok=True)
        row={'archive':name,'url_as_published':url,'started_at':now(),'status':'STARTED','member_content_interpreted':False}
        new_json(name+'.attempt.json',row)
        h=hashlib.sha256();n=0
        try:
            response,redirect=open_once(url,'GET',name)
            with response as r, part.open('xb') as out:
                reported=r.headers.get('Content-Length')
                declared=int(reported) if reported is not None else None
                if declared is not None and (declared<0 or declared>EACH or declared+total>TOTAL):raise RuntimeError('GET size exceeds cap')
                if declared is not None and meta['declared_bytes'] is not None and declared!=meta['declared_bytes']:raise RuntimeError('HEAD/GET length changed before body read')
                if r.headers.get('Content-Encoding','identity')!='identity':raise RuntimeError('Unexpected transport encoding')
                while True:
                    room=min(EACH-n,TOTAL-total)
                    if room<=0:
                        if declared is not None and n==declared:break
                        raise RuntimeError('Byte cap reached before verifiable end; partial preserved')
                    chunk=r.read(min(262144,room))
                    if not chunk:break
                    if len(chunk)>room:raise RuntimeError('Hard streaming limit reached; partial file preserved')
                    out.write(chunk);h.update(chunk);n+=len(chunk);total+=len(chunk)
                if declared is not None and n!=declared:raise RuntimeError('GET length mismatch')
                if meta['declared_bytes'] is not None and n!=meta['declared_bytes']:raise RuntimeError('HEAD length mismatch; identity uncertain')
                final_url=r.url;etag=r.headers.get('ETag')
                if meta['etag'] and etag and meta['etag']!=etag:raise RuntimeError('ETag changed since HEAD')
            dest=BASE/'archives'/name
            if dest.exists():raise RuntimeError('Destination exists')
            os.replace(part,dest)
            row.update(status='DOWNLOADED_WITHIN_CAP',bytes=n,sha256=h.hexdigest(),path=str(dest),final_url=final_url,etag=etag,redirects=redirect.hops,completed_at=now())
        except Exception as exc:
            row.update(status='FAILED_NO_RETRY',bytes_written=n,partial_sha256=h.hexdigest(),partial_path=str(part),error=f'{type(exc).__name__}: {exc}',stopped_at=now())
            rows.append(row);new_json('DOWNLOAD_RECEIPT.json',{'archives':rows,'total_bytes_written':total,'status':'STOPPED_NO_RETRY','automatic_retries':0})
            print(json.dumps(row,ensure_ascii=False),flush=True);raise
        rows.append(row);print(json.dumps({k:row[k] for k in ('archive','status','bytes','sha256')},ensure_ascii=False),flush=True)
    new_json('DOWNLOAD_RECEIPT.json',{'at':now(),'archives':rows,'total_bytes_written':total,'status':'COMPLETE','automatic_retries':0})

class CappedStream(io.RawIOBase):
    def __init__(self,src,limit):self.src=src;self.limit=limit;self.count=0
    def readable(self):return True
    def read(self,n=-1):
        room=self.limit-self.count
        if n<0:n=room+1
        data=self.src.read(min(n,room+1))
        if len(data)>room:raise RuntimeError('Expanded stream cap exceeded')
        self.count+=len(data);return data

def inventory():
    receipt=json.loads((BASE/'DOWNLOAD_RECEIPT.json').read_bytes())
    if receipt['status']!='COMPLETE':raise RuntimeError('No complete pinned download')
    new_json('INVENTORY_ATTEMPT_STARTED.json',{'at':now(),'reads':'TAR headers only; gzip bodies skipped by tar stream; no extraction/numerical parsing','expanded_cap_each':EXPANDED,'member_cap_each':MAX_MEMBERS})
    outputs=[]
    try:
        for source in receipt['archives']:
            path=Path(source['path']);hashobj=hashlib.sha256()
            with path.open('rb') as f:
                for buf in iter(lambda:f.read(262144),b''):hashobj.update(buf)
            if path.stat().st_size!=source['bytes'] or hashobj.hexdigest()!=source['sha256']:raise ValueError('Archive pin mismatch')
            members=[]
            with gzip.open(path,'rb') as gz:
                stream=CappedStream(gz,EXPANDED)
                with tarfile.open(fileobj=stream,mode='r|') as tf:
                    for entry in tf:
                        if len(members)>=MAX_MEMBERS:raise RuntimeError('Member count cap exceeded')
                        if entry.size<0 or entry.size>EXPANDED:raise ValueError('Invalid member size')
                        member={'name':entry.name,'size_from_header':entry.size,'mtime_from_header':entry.mtime,
                            'type':entry.type.decode('ascii',errors='backslashreplace'),'is_regular_file':entry.isfile(),
                            'is_directory':entry.isdir(),'linkname':entry.linkname,'pax_headers':entry.pax_headers,
                            'member_body_read_via_extractfile':False,'numerical_rows_parsed':False}
                        match=re.fullmatch(r'calibration_uncertainty_(H1|L1)_(\d+)\.txt',entry.name.rsplit('/',1)[-1])
                        member['detector_from_name']=match.group(1) if match and entry.isfile() else None
                        member['GPS_from_name']=int(match.group(2)) if match and entry.isfile() else None
                        members.append(member)
                # Verify gzip trailer/EOF without interpreting member bodies.
                while stream.read(262144):pass
            row={'archive':source['archive'],'archive_sha256':source['sha256'],'members':members,
                'header_count':len(members),'expanded_bytes_traversed':stream.count,'extracted_members':0,
                'numerical_member_content_interpreted':False,'calibration_validity_or_C00_C01_inferred':False}
            out_name=source['archive']+'.members.json';new_json(out_name,row)
            outputs.append({'file':out_name,'header_count':len(members),'matched_names':sum(m['GPS_from_name'] is not None for m in members),'expanded_bytes_traversed':stream.count})
            print(json.dumps(outputs[-1]),flush=True)
        new_json('INVENTORY_RECEIPT.json',{'at':now(),'status':'COMPLETE_HEADER_INVENTORY_ONLY','outputs':outputs,'numerical_rows_parsed':False,'extracted_members':0})
    except Exception as exc:
        new_json('INVENTORY_FAILED.json',{'at':now(),'completed_outputs':outputs,'error':f'{type(exc).__name__}: {exc}','no_automatic_retry':True})
        raise

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['discover','download','inventory'])
    globals()[ap.parse_args().phase]()
