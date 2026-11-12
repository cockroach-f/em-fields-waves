#!/usr/bin/env bash
# 低清预览渲染：tools/ql.sh chN_scenes.py Scene1 Scene2 ...
export PATH=/workspace/tools/.TinyTeX/bin/x86_64-linux:/workspace/tools/mamba/envs/manim/bin:$PATH
cd "$(dirname "$0")/../animations"
f=$1; shift
for s in "$@"; do manim -ql --disable_caching "$f" "$s" > "/tmp/ql_$s.log" 2>&1; echo "$s $?"; done
echo QLDONE
