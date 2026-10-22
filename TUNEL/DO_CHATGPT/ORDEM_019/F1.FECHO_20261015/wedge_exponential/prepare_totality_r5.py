from pathlib import Path
b=Path(__file__).resolve().parent
s=(b/'RealSubspaceTotalityR4.lean').read_text(encoding='utf8')
a=s.index('open ClosedSubmodule\n\ntheorem standard_complex_span_dense')
z=s.index('\ntheorem standard_exponential_total',a)
s=s[:a]+'''theorem standard_complex_span_dense (K : StandardSubspace H1) :
    (Submodule.span ℂ (K.toClosedSubmodule : Set H1)).topologicalClosure = ⊤ :=
  F1Fecho.StandardComplexSpan.dense K
''' + s[z:]
s=s.replace('import WedgeAnalyticR2','import WedgeAnalyticR2\nimport StandardComplexSpanR1')
with (b/'RealSubspaceTotalityR5.lean').open('x',encoding='utf8',newline='\n') as f:f.write(s)
