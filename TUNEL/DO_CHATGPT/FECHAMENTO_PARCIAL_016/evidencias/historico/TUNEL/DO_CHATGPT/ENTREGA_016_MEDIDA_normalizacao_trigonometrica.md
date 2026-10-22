[REAL — falha de normalização simbólica preservada]
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`.
Comando A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/temporal_proposal_audit.py.
O subprocesso Python terminou por AssertionError; o shell da primeira chamada
retornou0 porque o Get-Content subsequente terminou normalmente. Não é rc0 do teste.
LogSHA2567819ed63b28394d34e92347eda8e0ae9f15e0920ae81f651dde894e22eff4732; scriptSHA256d0d6c769eb122c4bf8f2b15b1896669c870caaeee872b9763812597929bb09e6.
Causa e correção: simplificação comum deixou -4cos(r/2)^2/(cos r+1); expand/trigsimp
reduz a-2. Próximo passo executado em temporal_proposal_audit_v2.py com rcPython
propagado explicitamente pelo shell:0;10checks,CPU0.21875s.
V1 preservada; zero chamada remota. Não confundir essa falha CAS com uma física nova.
