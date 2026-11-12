#!/usr/bin/env bash
# 渲染 animations/ 下的 manim 场景为 720p30 MP4，并复制到 docs/assets/videos/，同时截取封面图。
# 用法：tools/render_videos.sh [scene_file.py] [Scene ...]
#   不带参数：渲染所有 animations/ch*_scenes.py 中的全部场景
# 依赖：manim (Community, >=0.18)、ffmpeg、TeX 发行版（xelatex + ctex，公式用 MathTex/Tex 排版）。
#   若存在 TINYTEX_BIN（默认 /workspace/tools/.TinyTeX/bin/x86_64-linux）会自动加入 PATH。
set -euo pipefail
TINYTEX_BIN="${TINYTEX_BIN:-/workspace/tools/.TinyTeX/bin/x86_64-linux}"
[[ -d "$TINYTEX_BIN" ]] && export PATH="$TINYTEX_BIN:$PATH"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/animations"
OUT="$ROOT/docs/assets/videos"; POS="$ROOT/docs/assets/posters"
mkdir -p "$OUT" "$POS"
files=("${1:-}")
if [[ -z "${files[0]}" ]]; then files=(ch*_scenes.py); fi
shift || true
for f in "${files[@]}"; do
  mod="${f%.py}"
  if [[ $# -gt 0 ]]; then scenes=("$@"); else
    scenes=($(python3 - "$f" <<'PY'
import ast, sys
tree = ast.parse(open(sys.argv[1], encoding="utf-8").read())
for n in tree.body:
    if isinstance(n, ast.ClassDef) and n.name[:1] == "C":
        print(n.name)
PY
))
  fi
  for s in "${scenes[@]}"; do
    echo ">> $f :: $s"
    manim -qm --disable_caching "$f" "$s" >/dev/null
    src="media/videos/$mod/720p30/$s.mp4"
    # 再压一遍，减小体积（H.264, CRF 28, faststart 便于网页边下边播）
    ffmpeg -v error -y -i "$src" -c:v libx264 -preset slow -crf 28 -pix_fmt yuv420p -movflags +faststart -an "$OUT/$s.mp4"
    d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT/$s.mp4")
    ffmpeg -v error -y -ss "$(python3 -c "print(float('$d')*0.55)")" -i "$OUT/$s.mp4" -frames:v 1 -vf scale=640:-1 "$POS/$s.jpg"
    ls -lh "$OUT/$s.mp4" | awk '{print "   size:", $5}'
  done
done
