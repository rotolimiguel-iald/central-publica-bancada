from pathlib import Path
p=Path(__file__).parent
s=(p/'compile_pdf_offline_r1.py').read_text(encoding='utf-8')
s=s.replace('means the output PDF exists.', 'means both engine passes returned zero and the output PDF exists.')
s=s.replace('            subprocess.run(\n                [eng] + offline_options +','            compiled = subprocess.run(\n                [eng] + offline_options +')
s=s.replace('                timeout=180)\n        ok', '''                timeout=180)
            if compiled.returncode != 0:
                print("   [PDF] motor terminou com codigo %s (ver %s.log)" %
                      (compiled.returncode, texname))
                return False
        ok''')
with (p/'compile_pdf_offline_r2.py').open('x',encoding='utf-8') as f:f.write(s)
s=(p/'test_compile_pdf_offline_r1.py').read_text(encoding='utf-8')
s=s.replace("pdf_patch_r1'","pdf_patch_r2'").replace("compile_pdf_offline_r1.py","compile_pdf_offline_r2.py")
s=s.replace('PDF_PATCH_RECEIPT_R1','PDF_PATCH_RECEIPT_R2')
s=s.replace(" ('missing_package',", """ ('stale_pdf_then_failure',r'\\documentclass{article}\\usepackage{iald_unavailable_package_negative_control_20261015}\\begin{document}Failure must override stale PDF.\\end{document}',False),
 ('missing_package',""")
s=s.replace("    namespace['OUT']=str(dest)", """    if name=='stale_pdf_then_failure':
        with (dest/'fixture.pdf').open('xb') as f:f.write((OUT/'local_ok/fixture.pdf').read_bytes())
    namespace['OUT']=str(dest)""")
s=s.replace("      'Existing compile_pdf PDF-existence tri-state is preserved, including its preexisting handling of engine exit codes.',",
"      'Both engine exit codes must be zero; a stale PDF cannot override failure.',")
with (p/'test_compile_pdf_offline_r2.py').open('x',encoding='utf-8') as f:f.write(s)
