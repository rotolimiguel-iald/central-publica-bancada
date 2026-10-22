"""Apply the shared memory boundary without changing client authentication."""
from pathlib import Path
from iald_orchestrator.safe_files import replace_bytes
BASE=Path(__file__).resolve().parent

def edit(relative, replacements):
    path=BASE/relative
    raw=path.read_bytes()
    newline='\r\n' if b'\r\n' in raw else '\n'
    text=raw.decode().replace('\r\n','\n')
    for old,new in replacements:
        assert text.count(old)==1, (relative,old[:100])
        text=text.replace(old,new)
    replace_bytes(path,text.replace('\n',newline).encode())

edit('iald_orchestrator/providers.py', [
 ('def execute(name, prompt, workspace, *, cancel=None, process_callback=None):',
  'def execute(name, prompt, workspace, *, cancel=None, process_callback=None, memory_packet=None):'),
 ('    if name == "local":\n        payload =', '''    from . import canonical_memory
    from .policy import validate_prompt
    packet = memory_packet if memory_packet is not None else canonical_memory.prepare(prompt)
    if canonical_memory.digest(packet['prompt'].encode()) != packet['receipt']['packet_sha256']:
        raise ValueError("Pacote de memória alterado; envio bloqueado.")
    prompt = validate_prompt(packet['prompt'])
    if len((SYSTEM + prompt).encode()) > 39000:
        raise ValueError("Contexto comum excede o limite de transporte; dividir o pedido.")
    if name == "local":
        payload ='''),
 ('    result["elapsed_seconds"] =', '    result["canonical_memory"] = packet["receipt"]\n    result["elapsed_seconds"] =')])

edit('iald_orchestrator/runtime.py', [
 ('from . import VERSION, providers, jev', 'from . import VERSION, providers, jev, canonical_memory'),
 ('return {"version": VERSION, "providers": self.connections(), "jev": jev.availability(),',
  'return {"version": VERSION, "canonical_memory": canonical_memory.status(), "providers": self.connections(), "jev": jev.availability(),'),
 ('        decision = route(prompt, self.connections(), self.counts())', '''        packet = canonical_memory.prepare(prompt)
        classification = classify(prompt)
        classification['estimated_input_tokens'] = classify(providers.SYSTEM + packet['prompt'])['estimated_input_tokens']
        classification['estimate_status'] = 'INCLUDES_SHARED_MEMORY_AND_WRAPPER_EXCLUDES_CLIENT_INTERNALS'
        decision = route(prompt, self.connections(), self.counts(), classification=classification)
        decision['canonical_memory'] = packet['receipt']'''),
 ('            classification["estimated_input_tokens"] = classify(prompt)["estimated_input_tokens"]', '''            packet = canonical_memory.prepare(prompt)
            classification["estimated_input_tokens"] = classify(providers.SYSTEM + packet['prompt'])["estimated_input_tokens"]
            classification['estimate_status'] = 'INCLUDES_SHARED_MEMORY_AND_WRAPPER_EXCLUDES_CLIENT_INTERNALS' '''.rstrip()),
 ('            decision["jev"] = jev_status', '            decision["canonical_memory"] = packet["receipt"]\n            decision["jev"] = jev_status'),
 ('            result = providers.execute(decision["selected"], prompt, workspace, cancel=cancel,',
  '            result = providers.execute(decision["selected"], prompt, workspace, cancel=cancel, memory_packet=packet,')])

edit('iald_orchestrator/coordination.py', [
 ("        value['dispatch_prompt']=prompt", '''        value['dispatch_prompt']=prompt
        if value['stage'] not in TERMINAL:
            from .canonical_memory import prepare
            value['canonical_memory'] = prepare(value['prompt'])''')])
