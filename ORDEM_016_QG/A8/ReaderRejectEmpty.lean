import ExactTypeReader
set_option autoImplicit false
namespace ChatgptAudit.ReaderControl
def fromEmpty (h : False) : Nat := False.elim h
#assert_exact_type fromEmpty : Nat
#print axioms fromEmpty
end ChatgptAudit.ReaderControl
