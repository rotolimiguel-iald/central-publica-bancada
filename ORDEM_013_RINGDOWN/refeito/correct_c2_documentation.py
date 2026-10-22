"""Apply the independent C2 documentary correction beside the cited addendum."""
from pathlib import Path
import hashlib
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,s):
    if p.exists():raise FileExistsError(p)
    raw=s.encode();tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(raw)
    if tmp.read_bytes()!=raw:raise RuntimeError('Output mismatch')
    tmp.replace(p)
old=ROOT/'C2_ADENDO_OBSERVAVEL.md';s=old.read_text(encoding='utf-8')
wrong='Todas as trajetórias e ajustes estão no JSON; valores nas bordas são mantidos.'
if s.count(wrong)!=1:raise ValueError('Correction anchor missing')
s=s.replace(wrong,'Todos os ajustes individuais estão no JSON; as séries das trajetórias não foram arquivadas. Sua regeneração usa a semente, os índices de ruído, os insumos e o código identificados por hash, em ambiente numérico compatível. As versões das bibliotecas não foram registradas no ensaio original; o ambiente da revisão não certifica retrospectivamente esse runtime. Valores nas bordas são mantidos.')
s=s.replace('## Reprodução e custódia', '## Reprodução e custódia\n\nSupersedes: C2_ADENDO_OBSERVAVEL.md, SHA256 '+sha(old)+'. Correção ao lado em '+datetime.now(timezone.utc).isoformat()+'. Parecer independente: bis/C2_ADVERSARIAL_REVIEW.md, SHA256 '+sha(ROOT/'bis/C2_ADVERSARIAL_REVIEW.md')+'.\n\nA integração efetiva da largura de δf̂ na Parte B permanece NÃO PAGA nesta etapa; existe encaminhamento documental, não uma calibração executada. Os processos básicos e índices são pareados entre leituras: as células não fornecem evidências independentes. A revisão encontrou energia média branqueada reduzida de 0,90869 na biblioteca curta; não houve renormalização para forçar unidade.')
new(ROOT/'C2_ADENDO_OBSERVAVEL_v2.md',s)
fiche=(ROOT/'REAPROVEITAMENTO_C2.md').read_text(encoding='utf-8')
fiche += '\nAdendo documental vigente: C2_ADENDO_OBSERVAVEL_v2.md, SHA256 '+sha(ROOT/'C2_ADENDO_OBSERVAVEL_v2.md')+'. Supersedes da ficha: REAPROVEITAMENTO_C2.md, SHA256 '+sha(ROOT/'REAPROVEITAMENTO_C2.md')+'. Correção de armazenamento e encaminhamento B, sem nova simulação.\n'
new(ROOT/'REAPROVEITAMENTO_C2_v2.md',fiche)
print(sha(ROOT/'C2_ADENDO_OBSERVAVEL_v2.md'))
