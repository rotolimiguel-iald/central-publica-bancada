[REAL — inventário somente leitura; MEDIDA provisória, não qualificação R3]

27/09/2026. Abertura016SHA256: `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. ORDEM 015 SHA256 `c903681d01eec5ed8d55b7fe69e061a79b3a7b73eecede8f895cfb2d127f75a3`; contrato R3 SHA256 `b03c0df8d2061da21a44fcb3cb9ceca440a1049fdec8981b90a6e9a6efff3e5c`; LOCATION.json SHA256 `cbd9767da8845b61e12936c25d71f8b13c8c4234ae61a6f06a0a02bab308a8c5`.

A pasta R3 ainda não contém árvore LALSuite compilável, `configure`, `configure.ac`, `CMakeLists.txt`, headers ou venv. As duas fontes C custodiadas estão em `bis/e3_pilot_failure_diagnostic/sources/`; elas são insuficientes para compilar o pacote. Este inventário usou nomes e metadados para o ambiente, sem executar build ou patch.

Toolchain observada: Windows tem CMake 4.2.3, mas não foram encontrados ali GCC, Make, Autoconf, Automake ou pkg-config. WSL tem GCC 13.3, GNU Make 4.3 e Python 3.12.3 com `venv`; a auditoria não encontrou CMake, Autotools, pkg-config, SWIG nem dependências de desenvolvimento GSL/FFTW/HDF5 no ambiente examinado. Ausência nesta busca limitada é pré-condição a verificar na tentativa; não prova impossibilidade global.

R3, PASSO 12b, permanece **não executado**. Após encerrar a árvore T04, o contrato exige patch em cópia, build em venv próprio fora de `/opt`, guardas de índice/overflow, 122 pontos finitos e comparação da forma de onda nos pontos onde o original é finito. A reserva é 2 h, enquanto 1–3 h era estimativa não testada da ordem. Sem árvore fonte completa pinada e dependências, o risco de não qualificar R3 nesse envelope é alto. Se a tentativa não couber, registrar MEDIDA/NÃO PAGO com custo e seguir a ordem; nenhum uso científico do patch ocorre por esta nota.
