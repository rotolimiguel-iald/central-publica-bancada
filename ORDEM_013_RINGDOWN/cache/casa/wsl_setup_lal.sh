#!/bin/bash
# Configura o Ubuntu do WSL para o lalsuite: DNS publico (a resolucao do Windows passa por um DNS do Tailscale que reescreve
# files.pythonhosted.org para 100.127.127.77), Python 3.12 + venv, e instalacao OFFLINE dos wheels ja conferidos contra a PyPI.
set -e
echo "== 1. DNS proprio (nao herdar o do Windows)"
cat > /etc/wsl.conf <<'EOF'
[network]
generateResolvConf = false
[boot]
systemd = false
EOF
rm -f /etc/resolv.conf; printf 'nameserver 1.1.1.1\nnameserver 8.8.8.8\n' > /etc/resolv.conf; chattr +i /etc/resolv.conf 2>/dev/null || true
getent hosts files.pythonhosted.org | head -2
echo "== 2. pacotes"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq && apt-get install -y -qq python3 python3-venv python3-pip ca-certificates curl > /tmp/apt.log 2>&1 && echo "apt ok: $(python3 --version)"
echo "== 3. venv + wheels conferidos (offline)"
python3 -m venv /opt/lal_env
/opt/lal_env/bin/pip install --quiet --upgrade pip 2>/dev/null || true
/opt/lal_env/bin/pip install --quiet --no-index --find-links /mnt/c/tmp/whl_lal lalsuite && echo "lalsuite instalado"
/opt/lal_env/bin/python - <<'EOF'
import lal, lalsimulation as ls, numpy as np
print('lal', lal.__version__, '| lalsimulation ok')
m1, m2 = 36.0 * lal.MSUN_SI, 29.0 * lal.MSUN_SI
for name in ('IMRPhenomXPHM', 'SEOBNRv4', 'IMRPhenomD', 'SEOBNRv5_ROM' if hasattr(ls, 'SEOBNRv5_ROM') else 'SEOBNRv4_ROM'):
    try:
        appr = ls.GetApproximantFromString(name)
        hp, hc = ls.SimInspiralChooseTDWaveform(m1, m2, 0, 0, 0.3, 0, 0, 0.1, 400e6 * lal.PC_SI, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0 / 4096, 20.0, 20.0, lal.CreateDict(), appr)
        print('  %-16s ok: %d amostras, |h| max %.2e' % (name, hp.data.length, np.abs(hp.data.data).max()))
    except Exception as e:
        print('  %-16s ERRO %s: %s' % (name, type(e).__name__, str(e)[:100]))
EOF
echo "== FIM"
