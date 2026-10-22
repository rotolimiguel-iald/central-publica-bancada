import sys,json,tempfile,time,threading,uuid,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from iald_orchestrator.runtime import Runtime,now
from iald_orchestrator.process_lock import process_lock
class Probe(Runtime):
    guard=threading.Lock()
    lanes={}; peak=0; calls=[]; finishes=[]
    def _perform(self,task_id,prompt,routing_prompt=None):
        lane=self.task(task_id)['execution_constraints']['required_provider']
        with self.guard:
            self.lanes[lane]=self.lanes.get(lane,0)+1
            assert self.lanes[lane]==1
            self.__class__.peak=max(self.peak,sum(self.lanes.values()))
            self.calls.append(task_id)
        time.sleep(.18 if lane=='kimi' else .04)
        self._update(task_id,status='failed' if prompt=='fail' else 'result_ready')
        with self.guard:
            self.lanes[lane]-=1;self.finishes.append(task_id)
class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.r=Probe(self.tmp.name,recover=False)
        Probe.lanes={};Probe.calls=[];Probe.finishes=[];Probe.peak=0
    def tearDown(self):self.tmp.cleanup()
    def add(self,provider,prompt='ok',status='queued'):
        i=str(uuid.uuid4())
        with self.r.db() as db:
            db.execute('INSERT INTO tasks(id,request_id,prompt,created_at,updated_at,status,execution_constraints) VALUES(?,?,?,?,?,?,?)',(i,i,prompt,now(),now(),status,json.dumps({'required_provider':provider})))
        return i
    def test_parallel_exclusion_order_and_failure(self):
        ids=[self.add('kimi'),self.add('kimi'),self.add('mimo','fail'),self.add('deepseek'),self.add('mimo')]
        other=Probe(self.tmp.name,recover=False)
        ts=[threading.Thread(target=r._drain) for r in [self.r,other]]
        [t.start() for t in ts];[t.join(5) for t in ts]
        self.assertFalse(any(t.is_alive() for t in ts));self.assertEqual(Probe.peak,3)
        self.assertEqual(len(Probe.calls),5);self.assertEqual(len(set(Probe.calls)),5)
        self.assertLess(Probe.calls.index(ids[0]),Probe.calls.index(ids[1]))
        self.assertLess(Probe.finishes.index(ids[2]),Probe.finishes.index(ids[0]))
        self.assertEqual(self.r.task(ids[2])['status'],'failed')
        self.r._drain();self.assertEqual(len(Probe.calls),5)
    def test_uncertain_not_retried(self):
        i=self.add('kimi',status='running');self.add('mimo');self.r._drain()
        self.assertEqual(Probe.calls,[]);self.assertEqual(self.r.task(i)['status'],'running')
    def test_legacy_lock_and_recovery(self):
        i=self.add('kimi',status='running')
        with process_lock(self.r.db_path):
            Probe(self.tmp.name,recover=True)
            self.assertEqual(self.r.task(i)['status'],'running')
        Probe(self.tmp.name,recover=True)
        self.assertEqual(self.r.task(i)['status'],'interrupted')
        self.r._drain();self.assertEqual(Probe.calls,[])
class SelectionTests(unittest.TestCase):
    def test_free_provider_and_ready_result(self):
        from iald_orchestrator.coordination import Coordination
        from iald_orchestrator.transport import Transport
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as tmp:
            r=Runtime(tmp,recover=False);c=Coordination(r);t=Transport(c)
            ids=[str(uuid.uuid4()) for _ in range(3)]
            with r.db() as db:
                for i,provider in zip(ids,['kimi','kimi','mimo']):
                    db.execute('INSERT INTO coordination_jobs(id,request_id,prompt,created_at,updated_at,stage,execution_constraints) VALUES(?,?,?,?,?,?,?)',(i,i,'test',str(ids.index(i)),now(),'awaiting_dispatch',json.dumps({'required_provider':provider})))
                db.execute("UPDATE coordination_jobs SET stage='execution_waiting',execution_task_id=? WHERE id=?",(ids[0],ids[0]))
                db.execute('INSERT INTO tasks(id,request_id,prompt,created_at,updated_at,status) VALUES(?,?,?,?,?,?)',(ids[0],ids[0],'test',now(),now(),'running'))
            with patch('iald_orchestrator.transport.configuration',return_value={'enabled':True,'new_project_tasks_authorized':True}),patch.object(c,'get',side_effect=lambda i:{'id':i}):
                self.assertEqual(t.next_job()['job']['id'],ids[2])
                with r.db() as db:db.execute("UPDATE tasks SET status='result_ready' WHERE id=?",(ids[0],))
                self.assertEqual(t.next_job()['job']['id'],ids[0])

if __name__=='__main__':unittest.main()
