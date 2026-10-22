"""Append execution-state snapshot; never edit global memory or canonical artifacts."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
B=Path(__file__).resolve().parents[1];D=B.parent/'TUNEL/DO_CHATGPT';now=datetime.now(timezone.utc)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
deliveries={p.name:sha(p) for p in D.glob('ENTREGA_013_M[1-6]*.md')}
order=B.parent/'TUNEL/PARA_CHATGPT/ORDEM_013BIS_fechamento_e_ampliacao_dos_eventos_ate_5sigma.md'
data=dict(utc=now.isoformat(),active_order=str(order),order_sha256=sha(order),goal_status='ACTIVE_NOT_COMPLETE',
 part_a_status='M1_M2_M3_M4_M5_DELIVERED__M6_AND_CONTRACT_ERRATA_PENDING',formal_deliveries=deliveries,
 part_b_budget=dict(hours_authorized=40,started_utc=None,hours_charged=0,scope='All Part B machine wall time; Part A and old diagnostic jobs excluded'),
 current_package='C7_INDEPENDENT_v3_3',package_receipt='bis/C7_V3_3_DOCUMENTARY_VALIDATION.json',
 primary_replay='bis/C7_V3_2_C6_REPLAY.json',replay_scope='75 rows, zero difference; execution bytes identical in v3_3; scientific status INCONCLUSIVE_SYSTEMATICS',
 final_bundle_builder='refeito/build_final_bundle_v3_3_013bis.py',final_bundle_built=False,
 reviews_pending=['C7 v3_3 attribution residual R4','six supplemental replay wrappers','contract errata candidate','LVK injection descriptive calculation independent review'],
 agents=dict(Averroes='01a0ca10-c0e8-7c62-8ee8-4f153cd38299',Beauvoir='01a0ca1b-47e5-73c3-9c38-e334310b6c8c'),
 agent_assignments=dict(Averroes='Build only bis/contract_errata/CANDIDATE.md and receipt/scripts for eight prior notes; do not issue formal delivery',Beauvoir='Close C7 R4 and inspect new wrapper cleanup; LVK injection independent review later'),
 old_jobs='Two groups remain: phase_real_refined and continuous SEOB; continuous XPHM finished. Stop only own scripts when E3.1 begins; preserve snapshots/chunks and RAM.',
 latest_F0='bis/F0_SNAPSHOT_20260922T184601Z.json',
 next=['Read independent package/supplement closing reviews and apply corrections beside existing versions','Read contract errata candidate, verify and issue formal ENTREGA_013_ERRATA_contrato.md','Build final English bundle after all packages with clean verification','Create REAPROVEITAMENTO_C7.md and formal M6, F7 final scan and MA criteria','Start Part B budget and E0/E1, then E2 registration/tunnel witness before blind data PE','Continue E5/E4 then E3.1 stop old jobs, pilot and measured budget; no new C5 campaign'],
 restrictions=['Only Chatgpt writes; canonical/Atlas/memory/site untouched','No blind PE or new post-Sep22 posterior before E2 witness','No new heavy job while old groups run; no C5 reopening','No physical reading selected; NOT_FALSIFIED is not confirmation'],
 licence_manifest='cache/MANIFESTO_DOWNLOADS_013BIS_v2.json',licence_manifest_scope='1064 hashes verified, per-file licence declarations, old ledger preserved',
 supplemental_packages=['C7_POSTERIOR_REPRODUCTION_v3','C7_GWTC3_REPRODUCTION_v3','C7_INJECTION_REPRODUCTION_v3','C7_IMR_RECOVERY_REPRODUCTION_v3','C7_COHERENT_SOURCE_REPRODUCTION_v3','C7_NATIVE_SEOB_WAVEFORM_v3'])
p=B/'bis'/('EXECUTION_CHECKPOINT_'+now.strftime('%Y%m%dT%H%M%SZ')+'.json')
with p.open('xb') as f:f.write((json.dumps(data,indent=2,ensure_ascii=False)+'\n').encode())
print(p);print(sha(p))
