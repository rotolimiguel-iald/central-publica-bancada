import ExactTypeReader_v2
set_option autoImplicit false
namespace ChatgptAudit.ReaderControl
def otherIndex : Fin 2 := ⟨0, by decide⟩
#assert_exact_type otherIndex : Fin 3
#print axioms otherIndex
end ChatgptAudit.ReaderControl
