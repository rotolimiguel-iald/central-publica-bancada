#!/usr/bin/env bash
set -euo pipefail
root='/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN'
env_dir="$root/cache/t14_pyseobnr_venv"
report="$root/bis/015/t14"
export PIP_DISABLE_PIP_VERSION_CHECK=1
set +e
timeout --signal=TERM --kill-after=10s 300s "$env_dir/bin/python" -m pip install --no-input --no-cache-dir 'numpy==2.5.3' > "$report/T14_B_NUMPY.log" 2>&1
rc=$?
set -e
printf '%s\n' "$rc" > "$report/T14_B_NUMPY.rc"
printf 'T14_B_NUMPY_RC=%s\n' "$rc"
