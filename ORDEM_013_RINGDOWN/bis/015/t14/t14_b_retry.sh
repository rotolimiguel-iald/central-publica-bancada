#!/usr/bin/env bash
set -euo pipefail
root='/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN'
local_deps="$root/cache/t14_local_deps"
env_dir="$root/cache/t14_pyseobnr_venv"
report="$root/bis/015/t14"
export PATH="$local_deps/prefix/bin:$local_deps/prefix/usr/bin:$PATH"
export LD_LIBRARY_PATH="$local_deps/prefix/usr/lib/x86_64-linux-gnu:${LD_LIBRARY_PATH:-}"
export LIBRARY_PATH="$local_deps/prefix/usr/lib/x86_64-linux-gnu:${LIBRARY_PATH:-}"
export CPATH="$local_deps/prefix/usr/include:${CPATH:-}"
export SWIG_LIB="$local_deps/prefix/usr/share/swig4.0"
export PIP_DISABLE_PIP_VERSION_CHECK=1
export PYTHONDONTWRITEBYTECODE=1
test -x "$env_dir/bin/python"
test -x "$local_deps/prefix/usr/bin/swig"
"$local_deps/prefix/usr/bin/swig" -version > "$report/T14_B_SWIG_VERSION.log" 2>&1
gsl-config --version > "$report/T14_B_GSL_VERSION.log" 2>&1
set +e
timeout --signal=TERM --kill-after=10s 1800s "$env_dir/bin/python" -m pip install --no-input --no-cache-dir pyseobnr==0.3.7 > "$report/T14_B_PIP.log" 2>&1
rc=$?
set -e
printf '%s\n' "$rc" > "$report/T14_B_PIP.rc"
printf 'T14_B_PIP_RC=%s\n' "$rc"
