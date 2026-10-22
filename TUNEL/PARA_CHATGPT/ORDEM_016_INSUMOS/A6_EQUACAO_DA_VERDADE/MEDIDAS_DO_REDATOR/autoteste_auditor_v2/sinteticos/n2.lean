namespace A
axiom fake : False
theorem u : 1 = 2 := fake.elim
end A
#print axioms A.u
