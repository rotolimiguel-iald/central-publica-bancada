from pathlib import Path
p=Path(__file__).parent
s=(p/'RegularCovariantCoreR1.lean').read_text(encoding='utf-8')
for a,b in [
 ('rw [boostCLM B,','rw [boostCLM,'),
 (',boostCLM B,',',boostCLM,'),
 ('[regularUnitary B,','[regularUnitary,'),
 ('unfold regularUnitary B','unfold regularUnitary'),
 (',boostCLM B]',',boostCLM]'),
 ('boostIso_strong B\n','(boostIso_strong B)\n'),
 ('Set.range regularUnitary B','Set.range (regularUnitary B)'),
 ('amplification B M','amplification M'),
 ('rcases hA with ⟨B,hB,rfl⟩','rcases hA with ⟨A0,hA0,rfl⟩'),
 ('exact hM B hB','exact hM A0 hA0'),
 ('exact fibre_mem B M B hB','exact fibre_mem B M A0 hA0'),
]: s=s.replace(a,b)
with (p/'RegularCovariantCoreR2.lean').open('x',encoding='utf-8',newline='\n') as f:f.write(s)
