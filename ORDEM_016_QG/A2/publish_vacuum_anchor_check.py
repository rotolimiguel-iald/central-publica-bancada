from pathlib import Path
from datetime import datetime, timezone
import hashlib, json

root=Path(__file__).resolve().parents[1]
out=root.parent/'TUNEL/DO_CHATGPT'
inputs=root.parent/'TUNEL/PARA_CHATGPT/ORDEM_016_INSUMOS'
kernel=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
now=datetime.now(timezone.utc)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def create(p,b):
    assert not p.exists(),p
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b
    t.rename(p)
def append(p,b):
    old=p.read_bytes()
    create(p.with_name(p.name+'.bak_'+now.strftime('%Y%m%d_%H%M%S_%f')),old)
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(old+b)
    assert t.read_bytes()==old+b
    t.replace(p)
anchors=[]
for p,needle in [
 (inputs/'A1_CONTRATO_V3/v31/ContratoQG_v31_Teoremas.lean','theorem Δit_vac'),
 (inputs/'A1_CONTRATO_V3/v31/ContratoQG_v31.lean','  bw :'),
 (inputs/'A1_CONTRATO_V3/v31/ContratoQG_v31.lean','  V_vac :'),
 (kernel/'TGLExt/ModularPower.lean','theorem modularFlow_fixes_omega'),
 (kernel/'TGLExt/V354BoundedPolar.lean','theorem boundedAbsolute_ker')]:
    lines=p.read_text(encoding='utf-8').splitlines()
    hits=[i for i,l in enumerate(lines,1) if needle in l]
    assert len(hits)==1,(needle,hits)
    anchors.append({'source':str(p),'sha256':sha(p),'line':hits[0],
                    'excerpt':'\n'.join(lines[hits[0]-1:hits[0]+4])})
receipt={'utc':now.isoformat(),'status':'SOURCE_ANCHORS_VERIFIED_NOT_NEW_COMPILATION',
         'anchors':anchors,'next':'A-2.5.a finite bounded transform; inspect V354BoundedPolar existing kernel identity before implementation'}
create(root/'A2/vacuum_anchor_check.json',(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n').encode())
body=f'''[REAL — conferência de fontes; nenhuma nova prova ou compilação neste alvo]

# A-2.4 — vácuo e camada de uma partícula

Data UTC: {now.isoformat()}. ABERTURA sha256: `{sha(out/'ENTREGA_016_ABERTURA_operador.md')}`.

O contrato já deriva `Δit_vac` de `C.bw` e `C.boost.V_vac`.
Portanto é uma conclusão condicionada a um habitante de ContratoH2: não constrói esse
habitante, nem demonstra BW independentemente das hipóteses.
Na torre, `modularFlow_fixes_omega` demonstra a fixação de hOmega pela ação nos níveis.
As duas âncoras foram conferidas diretamente; não são teoremas novos desta bancada.

A construção da reta de luz desta bancada está na camada de uma partícula.
Não foi adicionado um vetor de vácuo a essa camada. O vácuo da segunda quantização
pertence a uma construção posterior; a torre existente não fornece automaticamente
o vácuo do novo par físico. Essa ponte permanece explicitamente distinta.

Âncoras e hashes:
'''
for a in anchors[:4]:
    body+=f"\n- `{a['source']}:{a['line']}` — sha256 `{a['sha256']}`.\n"
body+='''
Consulta: leitura dos enunciados e corpos com Get-Content/rg. Sem execução de um.py,
sem escrita no kernel e sem chamada de modelo. A aceitação deste alvo era a conferência
das âncoras e a identificação da camada sem vácuo, agora realizada. Custo de consultas:
aproximadamente 4 s parede (ferramentas); nenhuma compilação adicional.
Não move o gate. Próximo ramo A-2.5.a: transformada limitada na face finita.
A busca prévia encontrou `boundedAbsolute_ker` em V354BoundedPolar.lean: a igualdade
do núcleo do valor absoluto será reutilizada quando aplicável, sem repetir o lema.
'''
create(out/'ENTREGA_016_MEDIDA_A2_4_vacuo_ancoras.md',body.encode())
append(out/'ENTREGA_016_PROGRESSO.md',f'\n- {now.isoformat()} — A-2.4 PAGO como conferência das âncoras Δit_vac e modularFlow_fixes_omega; camada de uma partícula sem vácuo registrada. Consultas aproximadamente 0,0011 h parede; nenhuma nova compilação/chamada. Próximo A-2.5.a.\n'.encode())
print(json.dumps(receipt,ensure_ascii=False))
