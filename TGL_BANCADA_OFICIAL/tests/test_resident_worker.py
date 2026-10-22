"""Scientific-runtime tests; run in the already installed h5py WSL environment."""
import sys
import tempfile
import time
import unittest
import shutil
from unittest.mock import patch
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'adapters'))
try:
    import h5py
    import numpy as np
    from resident_worker import ResidentDomain,model
    import resident_worker
    AVAILABLE=True
except ImportError:
    AVAILABLE=False

@unittest.skipUnless(AVAILABLE,'Requires the existing WSL scientific runtime')
class ResidentTests(unittest.TestCase):
    def fixture(self,folder,name='strain.h5',external=False):
        path=Path(folder)/name
        with h5py.File(path,'w') as f:
            values=np.ones(1024,dtype=float);values[257]=900;values[512:544]=np.nan
            d=f.create_dataset('strain/Strain',shape=(1024,),dtype='f8',external=[('missing.bin',0,8192)]) if external else f.create_dataset('strain/Strain',data=values)
            d.attrs['Xspacing']=.25;d.attrs['Xstart']=1234567890.;d.attrs['Xunits']='second'
            f.create_dataset('meta/Detector',data=np.bytes_('H1'))
            f.create_dataset('quality/simple/DQmask',data=np.ones(256,dtype=np.uint32))
        return {'id':name,'path':str(path),'source':str(path),'name':name}
    def wait(self,domain):
        for _ in range(200):
            s=domain.status()
            if s['status']!='LOADING':return s
            time.sleep(.01)
        self.fail('Load did not finish')
    def test_full_load_survives_source_removal_and_preserves_impulse_and_gap(self):
        with tempfile.TemporaryDirectory() as folder:
            item=self.fixture(folder);d=ResidentDomain()
            d.load({'domain':'test','sources':[item],'budget_bytes':1000000})
            s=self.wait(d);self.assertEqual(s['status'],'READY')
            self.assertEqual(s['resident_bytes'],1024*8+256*4)
            self.assertEqual(s['series'][0]['numeric_datasets'],2)
            Path(item['path']).unlink() # Own fixture: views must no longer read it.
            v=d.view({'id':item['id'],'start_s':0,'duration_s':256,'bins':32})
            self.assertEqual(v['window_rows'],1024)
            self.assertEqual(max(p[2] for p in v['points'] if p[2] is not None),900)
            self.assertTrue(any(p[1] is None for p in v['points']))
            self.assertEqual(v['data_reads_since_load'],0)
            self.assertEqual(d.release()['resident_bytes'],0)
    def test_external_storage_and_memory_overrun_are_visible_failures(self):
        with tempfile.TemporaryDirectory() as folder:
            item=self.fixture(folder,external=True);d=ResidentDomain()
            d.load({'domain':'test','sources':[item],'budget_bytes':1000000})
            s=self.wait(d);self.assertEqual(s['status'],'FAILED')
            self.assertIn('storage refused',s['errors'][0]['error'])
            item=self.fixture(folder,'ordinary.h5');e=ResidentDomain()
            e.load({'domain':'test','sources':[item],'budget_bytes':1})
            s=self.wait(e);self.assertEqual(s['status'],'FAILED');self.assertEqual(s['resident_bytes'],0)
    def test_partial_is_not_ready(self):
        with tempfile.TemporaryDirectory() as folder:
            good=self.fixture(folder,'good.h5');bad=self.fixture(folder,'bad.h5',external=True);d=ResidentDomain()
            d.load({'domain':'test','sources':[good,bad],'budget_bytes':1000000})
            s=self.wait(d);self.assertEqual(s['status'],'PARTIAL');self.assertEqual(s['loaded_files'],1)
            d.release()
    def test_existing_model_control_and_redshift(self):
        p={'mass_source_solar':65,'spin':.7,'redshift':.1,'reading':'R-GLOBAL','amplitude':1e-21,'duration_s':.08}
        a=model(p);np.testing.assert_array_equal(a['gr'],a['tgl'])
        self.assertAlmostEqual(a['mass_detector_solar'],71.5)
        b=model({**p,'reading':'R-B'})
        self.assertGreater(b['prediction']['gamma_per_s'],0)
        self.assertLess(np.linalg.norm(b['tgl']),np.linalg.norm(b['gr']))
        with self.assertRaises(ValueError):model({**p,'reading':'unselected'})

    def test_altered_scientific_copy_is_refused_before_use(self):
        with tempfile.TemporaryDirectory() as folder:
            target=Path(folder)
            shutil.copytree(resident_worker.HERE/'models',target/'models')
            source=target/'models'/'tgl_ringdown_prediction.py'
            source.write_bytes(source.read_bytes()+b'\n# altered own fixture\n')
            with patch.object(resident_worker,'HERE',target):
                with self.assertRaisesRegex(ValueError,'Scientific executor copy changed'):
                    model({'reading':'R-B'})

if __name__=='__main__':unittest.main()
