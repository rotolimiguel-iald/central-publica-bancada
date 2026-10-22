#!/usr/bin/env bash
set -euo pipefail
base='/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/t14_local_deps'
mkdir -p "$base/prefix"
count=0
for deb in "$base"/packages/*.deb; do
  dpkg-deb -x "$deb" "$base/prefix"
  count=$((count+1))
done
test "$count" -eq 6
test -x "$base/prefix/usr/bin/gsl-config"
test -x "$base/prefix/usr/bin/swig"
printf 'extracted_packages=%s\n' "$count"
