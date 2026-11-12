# 电磁场与电磁波从零到精通

《电磁场与电磁波》讲义。章节结构与郭辉萍、刘学观编著《电磁场与电磁波》（第 6 版）一致，讲第 1–7 章和第 10 章：矢量分析与场论、静电场和恒定电场、边值问题、恒定磁场、时变电磁场、平面电磁波、传输线、无线信道与电磁兼容。每章都有直觉讲解、严格的定义与定理、手算例题、易错点、知识点归纳总结、练习题（答案可折叠），关键处嵌入 manim 动画。全书共 65 道例题、83 道练习、37 段动画、52 张配图。

**在线阅读：** <https://cockroach-f.github.io/em-fields-waves/>

姊妹站点：[复变函数从零到精通](https://cockroach-f.github.io/complex-functions/) · [量子力学从零到精通](https://cockroach-f.github.io/quantum-mechanics/) · [ISAR 目标识别入门与文献带读](https://cockroach-f.github.io/isar-tutorial/)

## 进度

- [x] 第 1 章 矢量分析与场论（9 道例题 + 9 道练习 + 4 段动画 + 3 张图）
- [x] 第 2 章 静电场和恒定电场（11 道例题 + 9 道练习 + 4 段动画 + 2 张图）
- [x] 第 3 章 边值问题的解法（6 道例题 + 10 道练习 + 3 段动画 + 3 张图）
- [x] 第 4 章 恒定电流的磁场（8 道例题 + 10 道练习 + 3 段动画 + 4 张图）
- [x] 第 5 章 时变电磁场与电磁波（6 道例题 + 12 道练习 + 4 段动画 + 3 张图）
- [x] 第 6 章 平面电磁波（4 道例题 + 12 道练习 + 6 段动画 + 2 张图）
- [x] 第 7 章 传输线（10 道例题 + 12 道练习 + 5 段动画 + 17 张图）
- [x] 第 10 章 无线信道、电磁干扰与电磁兼容（11 道例题 + 9 道练习 + 8 段动画 + 18 张图）
- [x] 全课程总结、公式速查

## 本地预览

```bash
pip install -r requirements.txt
mkdocs serve
```

## 目录结构

```
docs/
  index.md              # 绪论与知识地图
  ch1.md … ch7.md, ch10.md
  summary.md            # 全课程总结
  formulas.md           # 公式速查
  references.md         # 参考资料与致谢
  assets/videos/        # manim 渲染的 MP4（720p）
  assets/posters/       # 视频封面
  assets/img/           # 教材插图与参考资料配图
  javascripts/katex.js  # KaTeX 配置与矢量记号宏（\vv{E}、\ax 等）
animations/             # manim 场景源码（common.py、fieldtools.py、chN_scenes.py）
tools/
  render_videos.sh      # 渲染动画（720p）并压缩到 docs/assets/videos
  ql.sh                 # 低清预览渲染
```

## 重新渲染动画

依赖 [Manim Community](https://www.manim.community/)（≥0.18）、ffmpeg 和 TeX 发行版（xelatex + ctex）。

```bash
tools/render_videos.sh                          # 全部场景
tools/render_videos.sh ch2_scenes.py C2_Gauss   # 单个场景
```

## 部署

推送到 `main` 后，GitHub Actions（`.github/workflows/pages.yml`）自动执行 `mkdocs build --strict` 并发布到 GitHub Pages。

## 资料来源与版权

内容组织参考郭辉萍、刘学观编著《电磁场与电磁波》（第 6 版，西安电子科技大学出版社）。本仓库未包含教材正文，仅少量插图取自教材并注明来源；讲解文字、例题解答与动画均为本站编写，仅供学习交流。
