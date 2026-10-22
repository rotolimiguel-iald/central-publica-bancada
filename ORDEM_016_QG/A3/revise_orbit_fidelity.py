from pathlib import Path
import hashlib,json
here=Path(__file__).resolve().parent
old=here/'OrbitTranslationFaithfulness.lean'
new=here/'OrbitTranslationFaithfulness_v2.lean'
raw=old.read_bytes(); text=raw.decode()
text=text.replace('Fin.cons energy (fun i => if i=j then q else 0)',
                  '![energy, if j=0 then q else 0, if j=1 then q else 0, if j=2 then q else 0]')
text=text.replace(', Fin.cons]', ']')
text=text.replace('    simp only [hs1, zero_mul, sub_zero] at hh',
                  '    simp only [Fin.succ_zero_eq_one, hs1, zero_mul, sub_zero] at hh')
assert not new.exists()
with new.open('xb') as f:f.write(text.encode())
print(json.dumps(dict(predecessor_sha256=hashlib.sha256(raw).hexdigest(),output=str(new))))
