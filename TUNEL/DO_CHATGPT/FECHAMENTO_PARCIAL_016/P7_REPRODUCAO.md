# P7 — reprodução

Executar `python -X utf8 -B reproduzir.py --work <nova_pasta> --expected-ready-sha256 <hash_recebido_da_gerencia>` em Windows com a mesma toolchain e dependências Mathlib registradas. O script confere o pin externo e os hashes, copia a base v371 e recompila só os módulos ativos e o import conjunto. Não executa um.py nem lake build. Os logs desta entrega são da rodada de consolidação; o script de reprodução integral ainda não foi executado de ponta a ponta. Falta de toolchain/dependência é erro visível.
