"""Pin the independent runtime and Lean receipts; no production writes."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json
R=Path(__file__).resolve().parent
O=R.parent
def load(p):return json.loads(Path(p).read_bytes())
def pin(p):
    p=Path(p); b=p.read_bytes()
    return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
runtime_path=R/'runtime_20261014T143312_408279Z/REVIEW_RUNTIME_R1.json'
lean_path=R/'lean_20261014T143437_529032Z/REVIEW_LEAN_R1.json'
runtime=load(runtime_path); lean=load(lean_path)
assert runtime['passed'] and lean['passed']
dependencies=load(O/'attempts/20261014T143143_185233Z/DEPENDENCIES.json')
proof=load(O/'sources/tgl_kernel_proof_manifest.json')
verified=[]
for entry in dependencies:
    current=pin(entry['path'])
    assert current['sha256']==entry['sha256'] and current['bytes']==entry['bytes']
    normalized=entry['path'].replace('\\','/')
    if '/tgl_kernel/TGLExt/' in normalized:
        key='TGLExt/'+normalized.split('/tgl_kernel/TGLExt/',1)[1]
        assert proof['formal_files_sha256'][key]==current['sha256']
        current['matches_v392_proof_manifest']=True
    verified.append(current)
report='''# Revisão independente — F1.REGRA.MOTOR
**PASS_WITH_SCOPE**: nenhum achado material bloqueante; artefatos candidatos de sandbox.
Runtime: processo novo reproduziu 76 verificações e os 241 pontos byte a byte; 31 verificações adicionais independentes passaram.
Oráculo: canal de paridade com exponencial matricial por Taylor e scaling/squaring, espectro analítico e 48 estados/tempos; covariância por mudanças unitárias dentro dos blocos conferida.
Fontes: cinco funções e uma constante equivalentes por AST; selo/proof ligam o mesmo formal_source_hash; programa e selo coincidem com o estado consultado da Bancada.
Custódia: cadeia JSONL, arquivos congelados e dependências conferidos; nenhuma fonte mudou durante os testes.
Lean: dois módulos recompilados, EXIT 0, 42 teoremas novos e 22 reutilizados, somente o trio permitido; ambos os .olean idênticos aos do construtor.
Correspondência: E4 é o pinching em dois blocos 2×2; psi4, initial4 e target4 coincidem com o consumidor e o pré-registro. A ponte usa a frequência zero.
Tipos: eXe, pinching e motor vetorial recebem contratos separados. O testemunho M2 auxiliar não substitui a ligação M4, presente na seção ActualConsumerM4.
O alvo é fixado antes da execução; a leitura o satisfaz já em t=0. Uma inscrição incompatível permanece recusada.
O estado bruto converge e não coincide com o alvo em tempo finito, salvo se já fixo. Tolerância numérica não é igualdade Lean.
A grade usa u=Gamma*t: beta determina a escala temporal de referência; a curva versus u não mede beta nem fornece uma taxa física.
O espaço fixo tem dimensão complexa 8; não se demonstrou estado fixo único, infinitas dimensões ou confirmação física. Não há daemon ou implantação produtiva.
A regra de satisfação e a lei temporal são contratos explicitados. Traduções jurídico-ontológicas permanecem INPUT/ONTO.
Ferramenta de revisão: SciPy indisponível no runtime; o oráculo próprio usa Taylor de ordem 40 após redução da norma a no máximo 1/2, preservando o primeiro script como registro.
'''
report_path=R/'PARECER_R1.md'
with report_path.open('xb') as f:f.write(report.encode('utf-8'))
result={'passed':True,'verdict':'PASS_WITH_SCOPE','reviewed_utc':datetime.now(timezone.utc).isoformat(),'unit':'F1.REGRA.MOTOR','runtime_review':pin(runtime_path),'formal_review':pin(lean_path),'report':pin(report_path),'dependencies_verified':verified,'new_theorem_count':42,'reused_theorem_count':22,'formal_exit_codes':[m['exit_code'] for m in lean['modules']],'olean_matches_builder':[m['olean_matches_builder'] for m in lean['modules']],'runtime_replay_points':241,'runtime_original_checks':76,'runtime_independent_checks':runtime['checks_passed'],'material_findings':[],'scope_limits':runtime['scope_notes']+['Vector motor and corner reading are not identified with the actual M4 pinching.','The auxiliary M2 witness is distinct; the new ActualConsumerM4 section supplies the actual runtime correspondence.','The first reviewer script required unavailable SciPy and did not run science; immutable R1b uses an independent scaling-and-squaring Taylor exponential.'],'artifacts':[pin(p) for p in sorted(R.rglob('*')) if p.is_file() and p.name!='REVIEW_RESULT_R1.json']}
with (R/'REVIEW_RESULT_R1.json').open('xb') as f:f.write((json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps({'passed':True,'result':str(R/'REVIEW_RESULT_R1.json'),'sha256':pin(R/'REVIEW_RESULT_R1.json')['sha256']}))
