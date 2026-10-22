"""Arithmetic audit of nominal source scales; not a field solve or experiment."""
from decimal import Decimal as D
import json
from support_r72 import ROOT,new,pin
src=ROOT.parent.parent.parent.parent.parent.parent/'Patentes'
p=__import__('pathlib').Path(r'C:\IALD\Central de Patentes\Patentes\PATENTE_SUPERCONDUTOR_HOLOGRAFICO_TGL_v2_BLINDAGEM.tex')
lines=p.read_text(encoding='utf-8').splitlines()
assert '3\\times10^8' in lines[696]
assert 'L = 9' in lines[685]
assert '1.667,359' in lines[779]
assert '780' in lines[799]
c=D('3e8');L=D('.09');laser=D('780e-9');oh=D('1667.359e6')
f=c/(2*L);opt=c/laser
new('DIMENSIONAL_RESULT_R72.json',{'scope':'DERIVED from nominal documentary numbers; c=3e8 is source approximation, not CODATA precision or measured mode','source':pin(p),'anchors':[{'line':n,'text':lines[n-1]} for n in [686,688,691,697,698,780,800]],'input':{'c_source_m_s':str(c),'side_m':str(L),'lambda_laser_m':str(laser),'oh_Hz':str(oh)},'derived':{'nominal_c_over_2L_Hz':str(f),'oh_minus_nominal_Hz':str(oh-f),'optical_carrier_Hz':str(opt),'optical_to_oh_ratio':str(opt/oh)},'limitation':'No constitutive/EM solve. Nominal RF scale and optical carrier cannot be equated by label; sideband/conversion/rotating frame must be explicit. Nominal length rounded, not a falsification.'})
print('documentary arithmetic saved')
