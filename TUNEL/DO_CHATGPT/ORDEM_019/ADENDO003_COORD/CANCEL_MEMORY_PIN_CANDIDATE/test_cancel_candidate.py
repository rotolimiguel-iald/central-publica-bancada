import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
import uuid
from unittest.mock import patch

BASE = Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
OUT = Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\ADENDO003_COORD\CANCEL_MEMORY_PIN_CANDIDATE')
sys.path.insert(0, str(BASE))
from iald_orchestrator import canonical_memory, request_controls
from iald_orchestrator.runtime import Runtime, now

spec = importlib.util.spec_from_file_location('iald_orchestrator.coord_cancel_candidate', OUT / 'coordination.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class CancelMemoryPinTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.runtime = Runtime(self.tmp.name, recover=False)
        self.coordination = module.Coordination(self.runtime)
        self.job_id = str(uuid.uuid4())
        self.constraints = request_controls.normalize({
            'mission_id': 'ORDEM_016', 'branch_id': 'A2.3',
            'lemma_id': 'cancel_pin_regression', 'role': 'draft',
            'required_provider': 'local', 'max_calls': 1,
            'memory_generation': 'a' * 64,
        })
        stamp = now()
        with self.runtime.db() as db:
            db.execute('INSERT INTO coordination_jobs(id,request_id,prompt,created_at,updated_at,stage,execution_constraints) VALUES(?,?,?,?,?,?,?)',
                       (self.job_id,str(uuid.uuid4()),'Teste local de cancelamento.',stamp,stamp,'awaiting_dispatch',request_controls.encode(self.constraints)))

    def tearDown(self):
        self.tmp.cleanup()

    def test_old_pin_blocks_read_but_not_public_cancel(self):
        packet = {'prompt': 'Teste local de cancelamento.', 'receipt': {'generation': 'b' * 64, 'sources': []}}
        with patch.object(canonical_memory, 'prepare', return_value=packet) as prepare, patch.object(self.runtime, 'cancel') as cancel_runtime:
            with self.assertRaisesRegex(ValueError, 'Geração canônica diferente'):
                self.coordination.get(self.job_id)
            with self.assertRaisesRegex(ValueError, 'Geração canônica diferente'):
                self.coordination.act(self.job_id, 'begin_draft')
            calls_before = prepare.call_count
            result = self.coordination.act(self.job_id, 'cancel')
            self.assertEqual(result['stage'], 'cancelled')
            self.assertEqual(prepare.call_count, calls_before)
            self.assertEqual(cancel_runtime.call_count, 0)
            again = self.coordination.act(self.job_id, 'cancel')
            self.assertEqual(again['stage'], 'cancelled')
            self.assertEqual(prepare.call_count, calls_before)
        with self.runtime.db() as db:
            row = db.execute('SELECT stage,version,execution_constraints FROM coordination_jobs WHERE id=?',(self.job_id,)).fetchone()
            events = db.execute('SELECT action,from_stage,to_stage FROM coordination_events WHERE job_id=?',(self.job_id,)).fetchall()
        self.assertEqual((row['stage'],row['version']), ('cancelled',1))
        self.assertEqual(json.loads(row['execution_constraints'])['memory_generation'], 'a' * 64)
        self.assertEqual([tuple(e) for e in events], [('cancel','awaiting_dispatch','cancelled')])

    def test_invalid_payload_and_unknown_job_fail_closed(self):
        with self.assertRaises(ValueError):
            self.coordination.act(self.job_id, 'cancel', 'invalid')
        with self.assertRaisesRegex(ValueError, 'não encontrada'):
            self.coordination.act(str(uuid.uuid4()), 'cancel')

if __name__ == '__main__':
    unittest.main(verbosity=2)
