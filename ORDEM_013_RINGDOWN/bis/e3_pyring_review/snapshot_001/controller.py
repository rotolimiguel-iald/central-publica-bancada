"""Future-only calibration launcher with a single shared two-hour envelope."""
import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
import argparse,sys,time,subprocess,signal,resource
from pathlib import Path
from datetime import datetime,timezone
from custody import HERE,ROOT,verify,contained,sha,publish_new


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--authorization',required=True);args=parser.parse_args()
    started=time.time();mono=time.monotonic()
    cfg,manifest,auth,limit=verify(args.authorization)
    from run_controlled import cleanup_group
    # One exclusive directory for the complete calibration, including variants.
    root=contained(ROOT,cfg['output_relative_to_Chatgpt']);root.mkdir(mode=0o700)
    end=min(started+cfg['wall_envelope_seconds'],limit.timestamp())
    if end-time.time()<30:raise TimeoutError('No time after custody checks')
    mono_end=mono+end-started
    publish_new(root/'ENVELOPE.json',dict(started_utc=datetime.now(timezone.utc).isoformat(),
      stop_utc=datetime.fromtimestamp(end,timezone.utc).isoformat(),manifest_sha256=sha(HERE/'MANIFEST.json'),
      authorization_sha256=sha(contained(ROOT,args.authorization)),scope='NONBLIND_CALIBRATION_ONLY_MAX_2H'))
    runs=[];child=None;cleanup=None
    def interrupted(sig,frame):raise InterruptedError('Calibration controller interrupted')
    previous={s:signal.signal(s,interrupted) for s in (signal.SIGTERM,signal.SIGINT)}
    before=resource.getrusage(resource.RUSAGE_CHILDREN)
    try:
        for variant in cfg['variants']:
            if variant not in ('welch','public_psd'):raise ValueError('Invalid branch')
            if variant=='public_psd' and set(cfg['public_psd'])!=set(cfg['detectors']):
                raise ValueError('Public PSD branch requires pinned files before manifest/authorization')
            stop=min(end,time.time()+cfg['variant_wall_seconds'][variant])
            if stop-time.time()<30 or mono_end-time.monotonic()<30:raise TimeoutError('Insufficient envelope')
            out=root/variant;out.mkdir();child=None;cleanup=None
            ctx=dict(controller_pid=os.getpid(),
              controller_start_ticks=Path(f'/proc/{os.getpid()}/stat').read_text().rsplit(')',1)[1].split()[19],
              stop_utc=datetime.fromtimestamp(stop,timezone.utc).isoformat(),manifest_sha256=sha(HERE/'MANIFEST.json'))
            publish_new(out/'CONTEXT.json',ctx)
            command=[sys.executable,'-B',str(HERE/'runner.py'),'--authorization',str(contained(ROOT,args.authorization)),
              '--context',str(out/'CONTEXT.json')]
            local_mono_stop=time.monotonic()+stop-time.time()-15
            cutoff=False;begin=time.perf_counter()
            try:
                with (out/'RUN.log').open('xb') as log:
                    child=subprocess.Popen(command,stdout=log,stderr=subprocess.STDOUT,start_new_session=True,env=os.environ.copy())
                    while child.poll() is None:
                        if time.time()>=stop-15 or time.monotonic()>=min(local_mono_stop,mono_end-15):
                            cutoff=True;break
                        time.sleep(.2)
            finally:
                if child is not None:cleanup=cleanup_group(child)
            info=dict(variant=variant,wall_seconds=time.perf_counter()-begin,returncode=child.returncode,
              cutoff=cutoff,cleanup=cleanup,status='PARTIAL' if cutoff or child.returncode else 'COMPLETED_REQUIRES_REVIEW')
            runs.append(info);publish_new(out/'CONTROLLER.json',info)
            if not cleanup['group_absent']:raise RuntimeError('Calibration process group remains')
    finally:
        if child is not None and cleanup is None:cleanup=cleanup_group(child)
        for sig,handler in previous.items():signal.signal(sig,handler)
        after=resource.getrusage(resource.RUSAGE_CHILDREN)
        publish_new(root/'COST.json',dict(wall_seconds=time.monotonic()-mono,ceiling_seconds=cfg['wall_envelope_seconds'],
          children_cpu_seconds=(after.ru_utime+after.ru_stime)-(before.ru_utime+before.ru_stime),
          runs=runs,cleanup=cleanup,manifest_sha256=sha(HERE/'MANIFEST.json'),
          cost_scope='Includes initialization, conditioning, sampling and cleanup; one process/one BLAS thread; no physical claim'))


if __name__=='__main__':main()
