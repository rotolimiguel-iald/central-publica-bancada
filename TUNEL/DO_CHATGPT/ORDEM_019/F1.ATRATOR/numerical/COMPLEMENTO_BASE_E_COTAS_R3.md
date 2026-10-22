# Complemento numérico — ligação à face Hilbert

Autor: codex-gerente-tgl / atrator_sources. Complemento documental aos resultados R3, sem rodada ampliada.

Na base populacional, e=(1,1)/√2 e f=(1,−1)/√2. A matriz ortogonal Q=(1/√2)[[1,1],[1,−1]] tem colunas e,f. Então Q* T_pop Q=diag(1,λ), Q* R_pop Q=diag(1,0), pois T_pop e=e e T_pop f=(1−2β)f. Esta é precisamente a faceFamily=P+λ(I−P) da implementação Lean, transportada pela equivalência ortogonal Q. A tipagem do transporte evita identificar vetores de bases diferentes pelo mesmo nome.

Para n=4096, a cota analítica registrada λ^4096 é 4.702756306259857e-44. O erro numérico medido ||T^4096−R|| foi 5.335181422738092e-13; a diferença é o piso de arredondamento acumulado, dentro da tolerância 1e−10 fixada antes. Não se interpreta o piso de ponto flutuante como taxa física residual.

Para N=4096, a distância Cesàro medida foi 0.01014606139265087, com cota 0.01014606139265306; a fórmula exata foi conferida com resíduo 6.597631825361452e-14. A convergência média O(1/N) não recebe a tolerância de distância final da convergência forte.

FONTES_ANTES_DEPOIS_R3.json registra os pins conferidos antes/depois no código que saiu EXIT 0 e uma releitura final independente dos arquivos. Os digests intermediários por arquivo não foram gravados separadamente; sua igualdade resulta das duas guardas integrais concluídas. R1/R2 e suas erratas permanecem preservadas.
