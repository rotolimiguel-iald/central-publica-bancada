"""Only F3 chronology regressions. No numerical diagnostics or real data."""
from datetime import datetime,timezone,timedelta
from pathlib import Path
import copy
import sys
import types
import unittest
from unittest.mock import patch
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'producer'))
import tgl_ringdown_ampliacao as m


class AuthorizationChronology(unittest.TestCase):
    def call(self, stamp, valid=False):
        now=datetime.now(timezone.utc)
        spec=dict(plan_path='plan.json',nuisance_path='nuisance.json',plan_sha256='a'*64,
                  producer_tree_sha256={'synthetic.py':'b'*64})
        reg=dict(e7=spec,registered_utc=(now-timedelta(days=1)).isoformat())
        auth=dict(status='AUTHORIZED_BY_PRINCIPAL_AFTER_E2',registration_sha256='c'*64,
                  plan_sha256=spec['plan_sha256'],producer_tree_sha256=spec['producer_tree_sha256'],registered_utc=stamp)
        # Use strict stdlib parsing; checked_authorization itself also requires timezone.
        guard=types.SimpleNamespace(utc=lambda s:datetime.fromisoformat(s.replace('Z','+00:00')))
        reads=[]
        class PayloadReached(Exception):pass
        def reader(path):
            name=Path(path).name;reads.append(name)
            if name=='plan.json':return {'events':[{'role':'calibration'}]}
            if name=='nuisance.json':return {'gate':{}}
            if name=='auth.json':return copy.deepcopy(auth)
            if name=='payload.json':raise PayloadReached('no payload read; boundary sentinel')
            raise AssertionError(name)
        with patch.object(m,'checked_context',return_value=(reg,guard)),patch.object(m,'require_pin'),\
             patch.object(m,'read_json',side_effect=reader),\
             patch.object(m,'fullsample_diagnostics',side_effect=AssertionError('diagnostics forbidden')):
            if valid:
                with self.assertRaises(PayloadReached):m.run(Path(__file__).parent,'reg','c'*64,'payload.json','d'*64,'auth.json','e'*64)
                self.assertIn('payload.json',reads)
            else:
                with self.assertRaises(ValueError):m.run(Path(__file__).parent,'reg','c'*64,'payload.json','d'*64,'auth.json','e'*64)
                self.assertNotIn('payload.json',reads)

    def test_future_refused_before_payload(self):
        self.call((datetime.now(timezone.utc)+timedelta(days=1)).isoformat())

    def test_naive_refused_before_payload(self):
        self.call(datetime.now(timezone.utc).replace(tzinfo=None).isoformat())

    def test_malformed_refused_before_payload(self):
        self.call('not-a-date')

    def test_nontext_refused_before_payload(self):
        self.call(None)

    def test_before_E2_refused_before_payload(self):
        self.call((datetime.now(timezone.utc)-timedelta(days=2)).isoformat())

    def test_current_aware_positive_control(self):
        self.call(datetime.now(timezone.utc).isoformat(),True)

    def test_current_aware_offset_positive_control(self):
        self.call(datetime.now(timezone(timedelta(hours=-3))).isoformat(),True)


if __name__=='__main__':unittest.main(verbosity=2)
