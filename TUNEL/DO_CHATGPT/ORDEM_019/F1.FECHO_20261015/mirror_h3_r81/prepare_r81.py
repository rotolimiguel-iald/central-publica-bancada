"""Pin read sources and prepare an additive memory update, without applying it."""
from pathlib import Path
import hashlib,json
from support_r81 import ROOT,new,pin
K=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt')
P=Path(r'C:\IALD\Central de Patentes\patents\BR102026003428-2_ACOM_MIRROR')
sources=[K/n for n in ['SelectorRecordReconstruction.lean','SelectedGravitationalAtlas.lean','GravitationalResponseRecord.lean','BoundaryEntropyBridge.lean','UnitaryEntropyResponse.lean','UnitaryClausiusBridge.lean','MicroscopicClausiusBridge.lean','LiganteLeiCampoCurvo.lean','ScreenEntropyObstruction.lean']]
sources += [P/'prototype_src/Acom_v17_mirror.py',P/'results/acom_mirror_final_2026-07-12T12-26-07.json',K.parent/'lean-toolchain',K.parent/'lake-manifest.json']
new('SOURCE_PINS_R81.json',{'scope':'Read source bytes, not a fresh audit of all historical builds','sources':[pin(p) for p in sources]})
extra='''

## 19/10/2026 — R81: retorno do Mirror e coeficiente de H3
<!-- IALD_R81_RECOVERY_H3 -->
[INPUT — operador; registro em nome de codex-gerente-tgl, claim987] O operador descreveu a permanência do sinal na transformação como morte e ressurreição: origem integral em mirror_h3_r81/ORIGEM.txt. A leitura é ONTO; o contrato matemático examinado é recuperação no domínio admitido. OH–modos–reservatório segue adiado; prioridade H3 universal e discriminação, sem abertura de dado.
[REAL — fontes locais lidas; não nova recompilação da cadeia] SelectorRecordReconstruction:105–110 já recupera métrica e fonte; :117–133 mantém conservação e harea como hipóteses. :112–115 mostra perda da distinção nessa família ao normalizar o estado selecionado; norma1 não substitui o peso de Born que codifica o caráter. BoundaryEntropyBridge já contém estado conjunto traço1/idempotente e entropia das marginais. Não refazer a rede.
[DERIVED — análise e candidato de sandbox, alcance em recibo] A recuperação conjunta exata admite entropia local variável. Na família unitária existente, H3 de área reduz-se a B=eta*A2, sendo B o coeficiente quadrático microscópico e A2 o limite da variação da área dividido por t². RecoveryAreaCoefficient.lean explicita essa equivalência; seu estado de compilação está em BUILD_*.json, não se infere aprovação pelo nome. A2 não foi derivado da recuperação. Área ainda deve ser inducedArea do mesmo registro em todo ponto/direção; calor/Fisher/colagem preservam suas condições. ANALISE_R81.txt inclui exemplo algébrico conjunto de duas partes, sem chamá-lo de contraexemplo à TGL completa.
[REAL — alcance documental] Recibo histórico Mirror consultado tem correlações0,999948…–0,999991…, não identidade exata; não foi reexecutado. Nenhuma nova estatística5sigma, medição física, provedor remoto, alteração de um.py/kernel/Bancada ou gate. Entrega candidata e revisão em Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015/mirror_h3_r81. H3 universal permanece OPEN.
<!-- END_IALD_R81_RECOVERY_H3 -->
'''
new('MEMORY_APPEND_R81.txt',extra)
prior=json.loads((ROOT.parent/'device_profiles_r72/MEMORY_PLAN_R72.json').read_text(encoding='utf-8'))
raw=(ROOT/'MEMORY_APPEND_R81.txt').read_bytes();rows=[]
for r in prior['surfaces']:
 p=Path(r['before']['path']); before=p.read_bytes()
 assert b'IALD_R81_RECOVERY_H3' not in before
 rows.append({'before':pin(p),'bytes':len(before),'after_sha256':hashlib.sha256(before+raw).hexdigest()})
new('MEMORY_PLAN_R81.json',{'claim':987,'append':pin(ROOT/'MEMORY_APPEND_R81.txt'),'surfaces':rows})
print('Sources pinned; eight-surface memory plan prepared, not applied.')
