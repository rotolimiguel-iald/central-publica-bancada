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
export XDG_CACHE_HOME="$root/cache/t14_xdg_cache"
export NUMBA_CACHE_DIR="$root/cache/t14_numba_cache"
export MPLCONFIGDIR="$root/cache/t14_mpl_cache"
export PYTHONDONTWRITEBYTECODE=1
set +e
timeout --signal=TERM --kill-after=10s 900s "$env_dir/bin/python" "$report/t14_effect_probe.py" > "$report/T14_B_EFFECT_PROBE.log" 2>&1
rc=$?
set -e
printf '%s\n' "$rc" > "$report/T14_B_EFFECT_PROBE.rc"
printf 'T14_B_EFFECT_PROBE_RC=%s\n' "$rc"
