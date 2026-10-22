"""Correct only the unregistered map input; keep the original pinned."""
import hashlib
import json
from pathlib import Path
root=Path(__file__).resolve().parent
old=root/"MAPA_F43_R5_20261008.json"
new=root/"MAPA_F43_R5_VALIDADO_20261008.json"
obj=json.loads(old.read_text(encoding="utf-8"))
for artifact in obj["artefatos"]:
    artifact["caminho"]=artifact.pop("path")
obj["nota"]="O primeiro input falhou na validação do mapa por usar path em lugar de caminho; não foi registrado. SHA-256 do input preservado: "+hashlib.sha256(old.read_bytes()).hexdigest()
raw=(json.dumps(obj,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
with new.open("xb") as stream:
    stream.write(raw)
print(hashlib.sha256(raw).hexdigest())