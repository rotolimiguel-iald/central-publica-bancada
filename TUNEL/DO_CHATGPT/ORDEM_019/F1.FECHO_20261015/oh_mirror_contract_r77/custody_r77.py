"""Pin consulted immutable sources and exact line excerpts; no scientific execution."""
from pathlib import Path
from support_r77 import ROOT,new,pin
P=ROOT.parent
sources=[
 (Path(r'C:\IALD\Central de Patentes\Patentes\PATENTE_SUPERCONDUTOR_HOLOGRAFICO_TGL_v2_BLINDAGEM.tex'),[(246,267),(290,298),(343,370),(474,517)]),
 (Path(r'C:\IALD\papers_latex\luz\luz.tex'),[(70,108),(200,219)]),
 (P/'device_clock_r57/MiguelFixedBoundaryScalarReadingR57R2.lean',[(1,90)]),
 (P/'device_clock_r57/DERIVACAO_R57.md',[(132,221)]),
 (P/'instrument_phase_r74/PHASE_INSTRUMENT_BRIDGE_R74.md',[(1,110)]),
 (P/'instrument_phase_r74/RELATORIO_R74.md',None),
 (P/'reservoir_bridge_r66/RELATORIO_R66.txt',None),
 (P/'device_profiles_r72/sources/BOUNDARY_DATA_TABLE_R72.md',None),
 (P/'recognition_reuse_r73/CORRECAO_REAPROVEITAMENTO_R73.md',None),
 (P/'output_observability_r76/RELATORIO_R76.md',None),
 (ROOT/'ORIGEM_R77.txt',None),
]
if __name__=='__main__':
 rows=[];texts=[]
 for path,ranges in sources:
  lines=path.read_text(encoding='utf-8').splitlines()
  ranges=ranges or [(1,len(lines))]
  ranges=[(a,min(b,len(lines))) for a,b in ranges]
  rows.append({**pin(path),'lines':len(lines),'consulted_ranges':ranges})
  texts.append(str(path)+'\n'+'\n'.join(f'{i+1}: {lines[i]}' for a,b in ranges for i in range(a-1,b)))
 new('SOURCE_PINS_R77.json',{'sources':rows,'scope':'documentary and analytic only; no scientific execution'})
 new('SOURCE_EXCERPTS_R77.txt','\n\n'.join(texts))
 print(f'{len(rows)} sources pinned')
