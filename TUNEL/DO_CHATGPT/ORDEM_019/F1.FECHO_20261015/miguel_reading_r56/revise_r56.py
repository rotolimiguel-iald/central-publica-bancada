"""Preserve the stopped broad-import attempt and produce a leaner candidate beside it."""
from support_r56 import *
preflight()
old=ROOT/'MiguelReadingTemporalCompositionR56.lean'
text=old.read_text(encoding='utf-8').replace('import TGLExt.TheSelectionIsTheBallast\n','')
text=text.replace('namespace ChatgptAudit.MiguelReadingR56','namespace ChatgptAudit.MiguelReadingR56R2')
text=text.replace('end ChatgptAudit.MiguelReadingR56','end ChatgptAudit.MiguelReadingR56R2')
text=text.replace('  exact ⟨(the_selection_opens_the_boundary h0 h1).1,\n    (the_selection_opens_the_boundary h0 h1).2.1⟩',
'''  constructor
  · rw [normSq_reflection, sin_thetaMiguel h0 h1, Real.sq_sqrt h0]
  · rw [normSq_transmission]
    have h := Real.sin_sq_add_cos_sq (thetaMiguel beta)
    rw [sin_thetaMiguel h0 h1, Real.sq_sqrt h0] at h
    linarith''')
new('MiguelReadingTemporalCompositionR56R2.lean',text)
script=(ROOT/'build_r56.py').read_text(encoding='utf-8').replace('MiguelReadingTemporalCompositionR56.','MiguelReadingTemporalCompositionR56R2.')
script=script.replace("command=[str(lean),str(source),'-o'", "command=[str(lean),'-M','4096',str(source),'-o'")
new('build_r56_r2.py',script)
new('ATTEMPT_R1_STOP_REASON.json',{'reason':'A tentativa com TheSelectionIsTheBallast importava a torre completa; processo medido em 7752847360 bytes privados e 317263872 de working set. Encerrado apenas PID229820 após conferir command line e parent237012. Nova candidata usa os lemas da fronteira já presentes em SelectionAngleReconstruction/TheVerbalCoupling.','status':'R1_STOPPED_NOT_A_THEOREM_FAILURE','old_source':pin(old),'new_source':pin(ROOT/'MiguelReadingTemporalCompositionR56R2.lean')})
print('R2 prepared; R1 and its failed execution receipt preserved.')
