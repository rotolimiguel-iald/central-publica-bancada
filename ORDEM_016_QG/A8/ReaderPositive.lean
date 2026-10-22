import ExactTypeReader
set_option autoImplicit false
namespace ChatgptAudit.ReaderControl
def identityWitness : Nat := 1
#assert_exact_type identityWitness : Nat
def preserve (n : Nat) : n = n := rfl
#assert_exact_type preserve : (n : Nat) → n = n
#print axioms identityWitness
#print axioms preserve
end ChatgptAudit.ReaderControl
