import sys
BS=chr(92)
a=open(sys.argv[1],encoding='utf-8').read().replace('cetico_final'+BS,'')
b=open(sys.argv[2],encoding='utf-8').read()
strip=lambda s:[l for l in s.splitlines() if not l.startswith('rc=') and not l.startswith('kernel_files')]
print('equal_mod_rc_and_path:',strip(a)==strip(b), '| axioms lines', a.count('depends on axioms'), b.count('depends on axioms'), '| sorryAx', a.count('sorryAx'))
