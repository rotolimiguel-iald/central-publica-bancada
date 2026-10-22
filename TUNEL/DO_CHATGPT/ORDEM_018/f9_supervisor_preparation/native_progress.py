"""Prepared acknowledged native-call progress channel. Never starts a solver.

This protocol is not yet wired into the stdlib worker or 39f88; its actual
checkpoint names are sourced from background_supplier.py. A reviewed future
science bootstrap must bind the two preopened pipes and the real parent loop.
"""
import math
import os
import select
import time
from posix_protocol import canonical, document, exact, need, positive_integer, sha

PHASES=('BEFORE_NATIVE_BACKGROUND','AFTER_NATIVE_BACKGROUND')

class NativeProgressWindow:
    """Parent-side state. Persist ENTER before ACK; never issue a retry grant."""
    def __init__(self, *, run_directory, execution_unit_id, launch_nonce,
                 work_deadline, nominal_native_seconds, max_attempts, record_cap):
        positive_integer(max_attempts,'max_attempts')
        need(type(nominal_native_seconds) in (int,float) and math.isfinite(nominal_native_seconds)
             and nominal_native_seconds>0,'POSITIVE_FINITE_NATIVE_SECONDS')
        positive_integer(record_cap,'record_cap')
        need(type(launch_nonce) is str and len(launch_nonce)==32,'LAUNCH_NONCE')
        need(time.monotonic()<work_deadline,'PROGRESS_ALREADY_EXPIRED')
        self.run=run_directory
        self.unit=execution_unit_id;self.nonce=launch_nonce
        self.work_deadline=work_deadline;self.native_seconds=nominal_native_seconds
        self.maximum=max_attempts;self.cap=record_cap
        self.sequence=self.attempts=self.returns=0
        self.active=None;self.failed=False;self.seen_call_nonces=set()

    def next_deadline(self):
        return min(self.work_deadline,self.active['deadline']) if self.active else self.work_deadline

    def receive(self, raw):
        # Caller reads one bounded newline-delimited frame on the dedicated pipe.
        # Parent monotonic time controls the budget, never a child-provided clock.
        need(not self.failed,'PROGRESS_LATCHED')
        try:
            need(len(raw)<=self.cap and time.monotonic()<self.next_deadline(),'PROGRESS_CAP_OR_DEADLINE')
            msg=document(raw)
            exact(msg,('schema','execution_unit_id','launch_nonce','sequence','phase','call_nonce'))
            need(msg['schema']=='F9_NATIVE_PROGRESS_V1' and msg['execution_unit_id']==self.unit and
                 msg['launch_nonce']==self.nonce,'PROGRESS_IDENTITY')
            need(type(msg['sequence']) is int and msg['sequence']==self.sequence+1,'PROGRESS_SEQUENCE')
            need(msg['phase'] in PHASES and type(msg['call_nonce']) is str and
                 len(msg['call_nonce'])==32 and all(c in '0123456789abcdef' for c in msg['call_nonce']),
                 'PROGRESS_PHASE_OR_NONCE')
            now=time.monotonic()
            if msg['phase']=='BEFORE_NATIVE_BACKGROUND':
                need(self.active is None and self.attempts<self.maximum and
                     msg['call_nonce'] not in self.seen_call_nonces,'OVERLAP_OR_ATTEMPT_CAP_OR_REUSED_NONCE')
                self.seen_call_nonces.add(msg['call_nonce'])
                self.attempts+=1
                self.active={'call_nonce':msg['call_nonce'],'attempt':self.attempts,
                             'deadline':min(self.work_deadline,now+self.native_seconds)}
            else:
                need(self.active is not None and msg['call_nonce']==self.active['call_nonce'],
                     'RETURN_WITHOUT_OWNED_ENTER')
                self.returns+=1;self.active=None
            self.sequence=msg['sequence']
            row={**msg,'schema':'F9_NATIVE_PROGRESS_CONSUMPTION_V1','parent_monotonic':now,
                 'attempts':self.attempts,'returns':self.returns,'active':self.active,
                 'automatic_retry':False,'grant_scope':'PINNED_TRUSTED_PYTHON_CHECKPOINT_ONLY'}
            self.run.publish('progress_'+str(self.sequence).zfill(12)+'.json',canonical(row),self.cap)
            need(time.monotonic()<self.next_deadline(),'EXPIRED_DURING_PROGRESS_PERSISTENCE')
            return canonical({'schema':'F9_NATIVE_PROGRESS_ACK_V1','execution_unit_id':self.unit,
                'launch_nonce':self.nonce,'sequence':self.sequence,'phase':msg['phase'],
                'call_nonce':msg['call_nonce'],'progress_record_sha256':sha(canonical(row))})
        except BaseException:
            self.failed=True
            raise

    def terminal(self):
        need(not self.failed and self.active is None and self.attempts==self.returns,
             'PROGRESS_NOT_TERMINAL')
        need(time.monotonic()<self.work_deadline,'PROGRESS_TERMINAL_DEADLINE')
        return {'evidence_scope':'ACKNOWLEDGED_TRUSTED_PYTHON_CHECKPOINTS',
                'attempts':self.attempts,'returns':self.returns,'sequence':self.sequence,
                'unreported_native_calls_detected':None,'automatic_retry':False}


def exchange(*, request_fd, ack_fd, execution_unit_id, launch_nonce, sequence,
             phase, call_nonce, deadline, max_frame_bytes):
    """Child sends one checkpoint and waits for matching parent ACK.

    FDs are preopened pipes, nonblocking, owned/pinned by future bootstrap.
    Caller performs the native call ONLY after BEFORE returns, then sends AFTER.
    A missing ACK, partial frame, denial or timeout fails without repetition.
    """
    positive_integer(max_frame_bytes,'max_frame_bytes')
    need(phase in PHASES,'FIXED_NATIVE_CHECKPOINT')
    msg={'schema':'F9_NATIVE_PROGRESS_V1','execution_unit_id':execution_unit_id,
         'launch_nonce':launch_nonce,'sequence':sequence,'phase':phase,'call_nonce':call_nonce}
    raw=canonical(msg)+b'\n';need(len(raw)<=max_frame_bytes,'FRAME_TOO_LARGE')
    for fd in (request_fd,ack_fd):need(not os.get_blocking(fd),'NONBLOCKING_PROGRESS_PIPE_REQUIRED')
    view=memoryview(raw)
    while view:
        remaining=deadline-time.monotonic();need(remaining>0,'PROGRESS_SEND_DEADLINE')
        _,writable,_=select.select([], [request_fd], [], remaining)
        need(writable,'PROGRESS_SEND_TIMEOUT')
        try:n=os.write(request_fd,view)
        except BlockingIOError:continue
        need(n>0,'PROGRESS_PIPE_WRITE');view=view[n:]
    data=bytearray()
    while not data.endswith(b'\n'):
        remaining=deadline-time.monotonic();need(remaining>0,'PROGRESS_ACK_DEADLINE')
        readable,_,_=select.select([ack_fd], [], [], remaining)
        need(readable,'PROGRESS_ACK_TIMEOUT')
        try:chunk=os.read(ack_fd,1)
        except BlockingIOError:continue
        need(chunk,'PROGRESS_ACK_EOF');data.extend(chunk)
        need(len(data)<=max_frame_bytes,'PROGRESS_ACK_OVERFLOW')
    ack=document(bytes(data))
    exact(ack,('schema','execution_unit_id','launch_nonce','sequence','phase','call_nonce','progress_record_sha256'))
    need(ack['schema']=='F9_NATIVE_PROGRESS_ACK_V1' and
         all(ack[k]==msg[k] for k in ('execution_unit_id','launch_nonce','sequence','phase','call_nonce')),
         'PROGRESS_ACK_MISMATCH')
    need(time.monotonic()<deadline,'PROGRESS_ACK_EXPIRED')
    return ack
