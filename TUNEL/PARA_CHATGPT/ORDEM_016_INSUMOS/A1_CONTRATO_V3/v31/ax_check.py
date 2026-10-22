import re,sys
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    items=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",s,re.S)
    noax=re.findall(r"'([^']+)' does not depend on any axioms",s)
    bad=[(n,a) for n,a in items if set(x.strip() for x in a.split(','))-{'propext','Classical.choice','Quot.sound'}]
    rc=re.findall(r"rc=(\d+)",s)
    print(f.split('/')[-1], 'rc=',rc[-1] if rc else '?', 'decls_trio=',len(items)-len(bad),'sem_axioma=',len(noax),'fora_do_trio=',bad,'errors=',s.count(': error'),'warnings=',s.count(': warning'))
