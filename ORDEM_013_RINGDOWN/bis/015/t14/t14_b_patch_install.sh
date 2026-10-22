#!/usr/bin/env bash
set -euo pipefail
root='/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN'
deps="$root/cache/t14_local_deps"
env_dir="$root/cache/t14_pyseobnr_venv"
report="$root/bis/015/t14"
export PATH="$deps/prefix/bin:$deps/prefix/usr/bin:$PATH"
export LD_LIBRARY_PATH="$deps/prefix/usr/lib/x86_64-linux-gnu:${LD_LIBRARY_PATH:-}"
export LIBRARY_PATH="$deps/prefix/usr/lib/x86_64-linux-gnu:${LIBRARY_PATH:-}"
export CPATH="$deps/prefix/usr/include:${CPATH:-}"
export SWIG_LIB="$deps/prefix/usr/share/swig4.0"
export PIP_DISABLE_PIP_VERSION_CHECK=1
export PYTHONDONTWRITEBYTECODE=1
set +e
timeout --signal=TERM --kill-after=10s 1200s "$env_dir/bin/python" -m pip install --no-input --no-cache-dir --no-deps --no-build-isolation "$deps/src/pygsl_lite-0.1.8" > "$report/T14_B_PATCHED_PYGSL.log" 2>&1
first=$?
set -e
printf '%s\n' "$first" > "$report/T14_B_PATCHED_PYGSL.rc"
if [ "$first" -ne 0 ]; then
  printf 'T14_B_PATCHED_PYGSL_RC=%s\n' "$first"
  exit 0
fi
set +e
timeout --signal=TERM --kill-after=10s 1800s "$env_dir/bin/python" -m pip install --no-input --no-cache-dir pyseobnr==0.3.7 > "$report/T14_B_FINAL_PIP.log" 2>&1
second=$?
set -e
printf '%s\n' "$second" > "$report/T14_B_FINAL_PIP.rc"
printf 'T14_B_FINAL_PIP_RC=%s\n' "$second"
