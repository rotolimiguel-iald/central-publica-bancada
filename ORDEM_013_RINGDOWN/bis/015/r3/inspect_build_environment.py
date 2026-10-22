"""Read-only build-tool inventory for the scheduled, isolated R3 build."""
import json,shutil,subprocess,sys,sysconfig,hashlib
from pathlib import Path
from datetime import datetime,timezone
root=Path(__file__).resolve().parents[4]
out={"at":datetime.now(timezone.utc).isoformat(),"scope":"READ_ONLY_PREPARATION_NOT_BUILD_OR_SCIENCE", "tools":{},"pkgconfig":{},"native_installations":0}
for name in ('gcc','g++','make','cmake','autoconf','automake','libtoolize','pkg-config','git','swig','bison','flex'):
    out['tools'][name]=shutil.which(name)
pc=out['tools']['pkg-config']
if pc:
    for name in ('gsl','fftw3','fftw3f','hdf5','zlib','lal','lalsimulation'):
        p=subprocess.run([pc,'--modversion',name],capture_output=True,text=True,timeout=5)
        out['pkgconfig'][name]=dict(returncode=p.returncode,version=p.stdout.strip() if p.returncode==0 else None)
out['python']=dict(executable=sys.executable,version=sys.version,include=sysconfig.get_path('include'))
out['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
print(json.dumps(out))
