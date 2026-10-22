"""Prepare a pinned candidate without importing um.py or evaluating observed data."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, re, shutil
BASE=Path(__file__).resolve().parent
ROOT=BASE/'candidate'
BENCH=Path(r'C:/IALD/Bancada_Um')
NOS=Path(r'C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós')
def sha(b):return hashlib.sha256(b).hexdigest()
def entry(p, relative=False):
 b=p.read_bytes()
 return dict(path=p.relative_to(ROOT).as_posix() if relative else str(p),bytes=len(b),sha256=sha(b))
def copy_same(src,dst,data=None):
 b=src.read_bytes() if data is None else data;dst.parent.mkdir(parents=True,exist_ok=True)
 if dst.exists():
  if dst.read_bytes()!=b:raise ValueError('candidate conflict '+str(dst))
 else:
  with dst.open('xb') as f:f.write(b)
 return dst
for rel in ['tabelas/camb_lcdm_v1.npz','tabelas/camb_lcdm_v1.json','tabelas/pantheon_cov_v1.npy.json','fontes_externas/moresco_2022_cc.json','fontes_externas/moresco_2020_cov.json','fontes_externas/chen_huang_wang_2019_1808.05724.pdf']:
 copy_same(BENCH/rel,ROOT/rel)
nu=BASE.parent/'F8.2.NU3/archive_contracts'
nu_raw=(nu/'CONTRACTS_API_R2.json').read_bytes()
nu_contract=json.loads(nu_raw)
copy_same(nu/'CONTRACTS_API_R2.json',ROOT/'fontes_externas/NU3/CONTRACTS_API_R2.json',nu_raw)
for item in nu_contract['sources']:
 src=Path(item['extraction_path'])
 data=src.read_bytes()
 if sha(data)!=item['extraction_sha256']:raise ValueError('NU extraction changed')
 copy_same(src,ROOT/'fontes_externas/NU3'/src.name,data)
external=[]
d1=NOS.parent/'cache/d1_camb/v3'
external += [d1/'d1_v3_pipeline.py',d1/'MANIFESTO_D1_V3.json',d1/'saida/D1_CAMB_V3_REAL_RESULT.json']
external += [Path(r'C:/IALD/observaveis_tgl/tgl_data_cache/pantheon/Pantheon+SH0ES.dat'), Path(r'C:/IALD/projetos_pyhton/acom/tgl_data_cache/pantheon_covariance.dat')]
for directory in [Path(r'C:/IALD/Artigo/teste_acustico_beta_tgl_v1/_originais'),Path(r'C:/IALD/Artigo/frente_alpha'),NOS.parent/'TETELESTAI/BANCADA_OFICIAL/data/cosmology']:
 for name in ['desi_gaussian_bao_ALL_GCcomb_mean.txt','desi_gaussian_bao_ALL_GCcomb_cov.txt']:
  if (directory/name).is_file():external.append(directory/name)
sources=[entry(p) for p in external]
sources += [entry(p,True) for parent in ['fontes_externas','tabelas'] for p in sorted((ROOT/parent).rglob('*')) if p.is_file()]
for e in sources:e.update(statute='PINNED_CUSTODY_NOT_OPERATOR_ADMISSION',check_each_call=True)
code=[entry(p,True) for p in sorted(ROOT.rglob('*')) if p.is_file() and (p.suffix=='.py' or p.name=='CONTRATO_CANONICO_B2.md' or p.parent==ROOT/'ui' or (p.parent==ROOT/'bancada' and p.suffix=='.json'))]
raw=(NOS/'um.py').read_bytes();seal=(NOS/'um_absoluto_selo.json').read_bytes()
version=re.search(r'^UM_VERSION\s*=\s*["\']([^"\']+)',raw.decode('utf-8-sig'),re.M).group(1)
m=dict(schema=1,deployment_id='B2-NU3-20261009-R2',created_utc=datetime.now(timezone.utc).isoformat(),canonical=dict(version=version,script=dict(path=str(NOS/'um.py'),bytes=len(raw),sha256=sha(raw)),seal=dict(path=str(NOS/'um_absoluto_selo.json'),bytes=len(seal),sha256=sha(seal))),code=code,sources=sources,contracts=dict(cosmology='TGL/eff default; historical modes explicit; finite CAMB support; diagnostic likelihood',neff='Two Yp branches; X16/D8 selection unresolved',neutrino='Recovered author contracts; conditional synthetic channels; no absolute Ia yield',gw='Historical ECO consultation; pinned rite launch separate; ringdown not implemented',phase9='sealed opening not exposed; no promotion of draft',identity_policy='every operation; drift refuses until tested deployment',beta_policy='alpha_CODATA_2018*sqrt(e); bulk scale distinct',admission='custody is not operator source admission'))
assert json.loads(seal)['sha256']['um.py']==sha(raw)
assert json.loads(seal)['um_version']==version
path=ROOT/'canonical_contracts.json'
if path.exists():raise FileExistsError(path)
with path.open('x',encoding='utf-8') as f:json.dump(m,f,ensure_ascii=False,indent=2)
print(json.dumps(dict(manifest=entry(path,True),code=len(code),sources=len(sources),canonical=version),ensure_ascii=False))
