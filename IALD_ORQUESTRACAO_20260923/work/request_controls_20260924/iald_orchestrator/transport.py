"""Small persistent inbox for the official Codex app's unattended coordinator."""
from .coordination import Coordination
from .runtime import BASE, now
from .safe_files import save_json
import json

CONFIG = BASE / 'transport.json'

def configuration():
    # Invalid/missing configuration must not silently enable automation.
    if not CONFIG.is_file():
        return {'enabled': False, 'new_project_tasks_authorized': False}
    return json.loads(CONFIG.read_bytes())

class Transport:
    def __init__(self, coordination=None):
        self.coordination = coordination or Coordination()

    def next_job(self):
        config = configuration()
        with self.coordination.runtime.db() as db:
            # Finish an existing handoff before opening another project task.
            row = db.execute("""SELECT id,stage FROM coordination_jobs
                WHERE stage NOT IN ('completed','failed','cancelled')
                ORDER BY CASE WHEN stage='awaiting_dispatch' THEN 1 ELSE 0 END,
                created_at,id LIMIT 1""").fetchone()
        if row is None:
            return {'state': 'idle', 'pending': False, 'provider_calls': 0}
        if not config.get('enabled'):
            return {'state': 'paused', 'pending': True, 'job_id': row['id']}
        if row['stage'] == 'awaiting_dispatch' and not config.get('new_project_tasks_authorized'):
            return {'state': 'needs_project_task_authorization', 'pending': True, 'job_id': row['id']}
        job = self.coordination.get(row['id'])
        return {'state': 'work', 'pending': True, 'job': job,
                'handoff_markers': {'draft': f'IALD_JOB:{row["id"]}:DRAFT',
                                    'synthesis': f'IALD_JOB:{row["id"]}:SYNTHESIS'}}

    def submit(self, prompt, request_id, execution_constraints=None):
        # Only explicit operator requests may enter here; model output is not authority.
        return self.coordination.create(prompt, request_id, execution_constraints)

    def receipt(self, state, job_id=None):
        if state not in ('idle','progress','needs_attention','completed'):
            raise ValueError('Estado de transporte inválido.')
        if job_id:
            self.coordination.get(job_id)
        value = {'checked_at': now(), 'state': state, 'job_id': job_id}
        save_json(self.coordination.runtime.state_dir/'transport_last_check.json', value)
        return value
