[REAL] Errata de custódia, 27/09/2026.

O campo `official_package_unchanged: false` em `T14_B_PATCH_RECEIPT.json` (SHA-256 `f6cbd52778f5e470fdbdc6b2ce9e94fc7a8a297417e8a280729804115e7fa766`) está incorreto. O tarball oficial `cache/t14_local_deps/src/pygsl_lite-0.1.8.tar.gz` foi relido após a instalação: SHA-256 `3213755c71da61e9629551e088530130d28e27048cd5f3ba48deb8165e6df6de`, idêntico ao hash fixado no recibo. A única mudança foi na cópia extraída local, `gsl_dist/swig_extension.py`: `spawn(cmd, 1, 1)` passou a `spawn(cmd)` para compatibilidade do build com Python 3.12/setuptools. O pacote externo e os originais científicos permanecem sem alteração.

Este adendo corrige o campo, sem sobrescrever o recibo histórico nem afetar o resultado da API ou o gate.
