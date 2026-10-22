# R70 — erro causal da aproximação ao gerador efetivo

18/10/2026, codex-gerente-tgl. [DERIVED — demonstração analítica, não compilação Lean]. Reuso: LOCALITY_BRIDGE_R69.md e BOSONIC_CONTINUUM_R66.txt. Mesmos espaços e mesmos observáveis precisam ser identificados antes de aplicar estas cotas.

## 1. Defeito causal de um gerador limitado

Para h=h*, família finita L_j e B limitado, escreva

G*(B)=i[h,B]+(1/2)Σ(L_j*[B,L_j]+[L_j*,B]L_j).

Logo d_B=||[h,B]||+(1/2)Σ||L_j||(||[B,L_j]||+||[L_j*,B]||) satisfaz ||G*B||≤d_B. A derivada do semigrupo uniformemente contínuo e a contração da aplicação unital completamente positiva dão

||T_t*B−B||=||∫_0^t T_s*(G*B)ds||≤t d_B.

Se os coeficientes são locais e B pertence ao comutante, d_B=0. Se são apenas aproximados, a cota quantifica o defeito; ela não prova que o defeito real seja diferente de zero. Nenhuma norma de operador ilimitado é inserida nesta fórmula.

## 2. Comparação entre dois geradores

Para geradores limitados G e G~ na MESMA álgebra, com coeficientes pareados h,L_j e h~,M_j (completar a lista por zeros se necessário), defina

ε_G=2||h−h~||+2Σ||L_j−M_j||(||L_j||+||M_j||).

Expandir o termo de salto e o anticomutador prova ||G−G~||_{1→1}≤ε_G. A identidade de Duhamel, usando contração dos dois semigrupos, implica ||T_t−T~_t||_{1→1}≤t ε_G. Se T~ é localizado e ρ é estado normal,

|Tr[(T_tρ−ρ)B]|≤t ε_G ||B||.

O pareamento dos saltos não é único; a cota é suficiente e pode ser frouxa. Não se afirma minimalidade, nem se infere ε_G=0 da ausência de medida. A norma é a usual em traço-classe, não uma norma diamante implicitamente assumida.

## 3. Como ligar esta cota à R66 sem trocar de espaço

R66 fornece, para X suportado em N≤m0 e m≥m0, δ_cut=2||X||_1 Σ_{k=m−m0+1}∞(2|Ω|t)^k/k!, em norma-traço após inclusão no espaço comum. Se existir uma realização local T_loc no espaço da rede e um mapa isométrico V, a decomposição triangular é

||V T_R66(t)X V* − T_loc(t)(VXV*)||_1
≤δ_cut + ||V E_m T_m(t)X V* − T_loc(t)(VXV*)||_1.

O segundo termo é δ_loc, uma OBRIGAÇÃO nova com peso. Só pode ser substituído por t ε_G se as duas dinâmicas comparadas forem semigrupos limitados definidos no mesmo espaço, com os coeficientes e normas acima verificados. A extensão do corte por zeros não se torna local por essa escolha. A inclusão R66 por si não fornece δ_loc.

Para observável B limitado, o erro de expectativa é ≤||B||(δ_cut+δ_loc). Uma incerteza instrumental independente δ_inst pode ser somada em unidades do MESMO observável, depois de transportar a calibração R69. Não usar esta cota para quadraturas ilimitadas sem estimativas de momentos. Não comparar δ_inst dimensional com norma-traço adimensional.

Assim o próximo contrato verificável é uma cota δ_loc(t,classe de estados,m) efetiva. A construção R70 de campos locais pode fornecer candidatos, mas não os identifica por nome aos modos R66. Nenhum valor desconhecido recebe zero por padrão.

## 4. Controles e alcance

O script causal_budget_r70.py testa a identidade causal e as cotas por exponenciais de superoperadores em dois qubits sintéticos. A primeira álgebra é B(C²)⊗I e o observável externo é I⊗Z. O controle perturbado tem acoplamento não local explícito. Não é um modelo do aparelho nem confirmação da rede relativística. Plano e script são pinados antes da execução única; o resultado fica em recibo separado.
