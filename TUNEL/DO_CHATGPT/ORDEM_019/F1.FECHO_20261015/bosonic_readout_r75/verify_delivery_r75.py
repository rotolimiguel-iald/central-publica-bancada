"""Read-only verification of the delivered R75 append and mission state."""
from support_r75 import *
def main():
    applied=json.loads((ROOT/'MEMORY_APPLIED_R75.json').read_text(encoding='utf-8'))
    extra=(ROOT/'MEMORY_APPEND_R75.txt').read_bytes(); rows=[]
    for r in applied['surfaces']:
        backup=Path(r['backup']['path']); current=Path(r['after']['path'])
        assert pin(backup)==r['backup'] and pin(current)==r['after']
        assert current.read_bytes()==backup.read_bytes()+extra
        rows.append({'path':str(current),'pure_append':True,'backup_sha256':r['backup']['sha256'],'after_sha256':r['after']['sha256']})
    m=project('POST_DELIVERY_PROJECT')
    tasks=[x for x in m['projection']['active'] if x['id'] in ['R4','R5']]
    assert len(tasks)==2 and all(not x.get('lease') for x in tasks)
    out={'memory_verified':rows,'mission_receipt':m['receipt'],'R4_R5':tasks,'map':json.loads((ROOT/'MAP_REGISTER_RESULT.json').read_text(encoding='utf-8')),'board':json.loads((ROOT/'BOARD_REGISTER_RESULT.json').read_text(encoding='utf-8')),'scientific_rerun':False}
    new('POST_DELIVERY_VERIFIED_R75.json',out)
    print(json.dumps({'memory_surfaces':len(rows),'revision':m['receipt']['revision'],'map':out['map'],'board':out['board']},ensure_ascii=False))
if __name__=='__main__':main()

