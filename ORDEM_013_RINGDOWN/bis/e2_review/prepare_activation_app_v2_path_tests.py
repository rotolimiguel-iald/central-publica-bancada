"""Additive path-only regression fixtures. No real sealer or activation."""
from pathlib import Path
import ast
HERE=Path(__file__).resolve().parent;B=HERE.parents[1]
old=(HERE/'activation_app_v2_path_snapshot/registration_guard.py').read_bytes()
current=(B/'bis/e2_code/registration_guard.py').read_bytes()
before=b'ORDEM_013_RINGDOWN/bis/E2_REVIEW_APPLICATION_V1.json'
after=b'ORDEM_013_RINGDOWN/bis/E2_REVIEW_APPLICATION_V2.json'
if old.count(before)!=1 or old.replace(before,after)!=current:
    raise ValueError('Guard delta is not exactly the single authorized byte-string replacement')
text=(HERE/'test_activation_marker_v2.py').read_text()
text=text.replace('E2_REVIEW_APPLICATION_V1.json','E2_REVIEW_APPLICATION_V2.json')
text=text.replace('activation_mock_v2','activation_app_v2_path_mock')
text=text.replace('ACTIVATION_MARKER_MOCKS_V2.json','ACTIVATION_APP_V2_PATH_TESTS.json')
anchor="    checks.append('application_equal_registration_positive')"
if text.count(anchor)!=1:raise ValueError('Ambiguous test insertion')
text=text.replace(anchor,anchor+'''
    for rejected_name in ('E2_REVIEW_APPLICATION_V1.json','E2_REVIEW_APPLICATION_V3.json'):
        wrong=copy.deepcopy(reg)
        wrong['activation']['review_application_relative_to_Chatgpt']='ORDEM_013_RINGDOWN/bis/'+rejected_name
        try:g.check_activation(wrong,digest,note)
        except ValueError as error:
            if str(error)!='Activation artifact paths differ':raise
            checks.append('fixed_path_rejects_'+rejected_name)
        else:raise RuntimeError('Wrong fixed application path accepted')
''')
ast.parse(text)
with (HERE/'test_activation_app_v2_path.py').open('x',encoding='utf-8',newline='\n') as f:f.write(text)
print('Single byte-string source delta confirmed; additive fixtures prepared')
