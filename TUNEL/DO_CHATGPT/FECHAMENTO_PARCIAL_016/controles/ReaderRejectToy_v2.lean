import ExactTypeReader_v2
set_option autoImplicit false
namespace ChatgptAudit.ReaderControl
def toy : Unit := ()
#assert_exact_type toy : Nat
#print axioms toy
end ChatgptAudit.ReaderControl
