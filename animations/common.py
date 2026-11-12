"""Shared helpers for the 电磁场与电磁波 manim scenes (Manim Community + LaTeX).

公式统一用 LaTeX 排版：
  MT(r"...")  纯数学公式（MathTex，默认 LaTeX 模板）
  CT(r"...")  中文 + 行内公式（Tex + ctex 模板，xelatex 编译）
依赖：TeX 发行版（TinyTeX 即可）+ ctex、standalone、preview、dvisvgm 等宏包。
"""
from manim import *  # noqa: F401,F403

# ---------------------------------------------------------------- palette
C_E = YELLOW      # 电场
C_H = TEAL        # 磁场
C_POS = RED_C     # 正电荷
C_NEG = BLUE_C    # 负电荷
C_HL = ORANGE     # 强调
C_S = PURPLE_B    # 坡印廷 / 功率流

CTEX = TexTemplate(tex_compiler="xelatex", output_format=".xdv")
CTEX.add_to_preamble(r"\usepackage[UTF8]{ctex}" "\n" r"\usepackage{amsmath,amssymb,bm,xcolor}")
# 加宽行宽，避免长句被 TeX 自动折行（排版位置由 manim 控制）
MACROS = (r"\newcommand{\vv}[1]{\boldsymbol{#1}}\newcommand{\ax}{\boldsymbol{a}_x}\newcommand{\ay}{\boldsymbol{a}_y}"
          r"\newcommand{\az}{\boldsymbol{a}_z}\newcommand{\arho}{\boldsymbol{a}_\rho}\newcommand{\aphi}{\boldsymbol{a}_\phi}"
          r"\newcommand{\ar}{\boldsymbol{a}_r}\newcommand{\atheta}{\boldsymbol{a}_\theta}\newcommand{\an}{\boldsymbol{a}_n}"
          r"\newcommand{\dd}{\mathrm{d}}\newcommand{\je}{\mathrm{j}}")
CTEX.add_to_preamble(MACROS)
MTEX = TexTemplate()
MTEX.add_to_preamble(r"\usepackage{amsmath,amssymb,bm}" "\n" + MACROS)
CTEX.add_to_preamble(r"\setlength{\textwidth}{60cm}\setlength{\hsize}{60cm}\setlength{\linewidth}{60cm}")


def MT(tex: str, size: int = 32, color=WHITE, **kw) -> MathTex:
    return MathTex(tex, font_size=size, color=color, tex_template=MTEX, **kw)


def CT(tex: str, size: int = 30, color=WHITE, **kw) -> Tex:
    """Chinese text with inline $math$ (xelatex + ctex)."""
    return Tex(tex, tex_template=CTEX, font_size=size, color=color, **kw)


# backwards-compatible name
T = CT


def plane(x_range=(-4, 4, 1), y_range=(-3.5, 3.5, 1), unit=1.0, **kw) -> ComplexPlane:
    return ComplexPlane(
        x_range=list(x_range),
        y_range=list(y_range),
        x_length=(x_range[1] - x_range[0]) * unit,
        y_length=(y_range[1] - y_range[0]) * unit,
        background_line_style={"stroke_color": BLUE_E, "stroke_width": 1, "stroke_opacity": 0.6},
        axis_config={"stroke_width": 2},
        **kw,
    )


def axis_labels(p: ComplexPlane, re=r"\operatorname{Re}", im=r"\operatorname{Im}", size=24):
    a = MT(re, size, GREY_B).next_to(p.n2p(complex(p.x_range[1], 0)), DOWN + LEFT * 0.3, buff=0.12)
    b = MT(im, size, GREY_B).next_to(p.n2p(complex(0, p.y_range[1])), RIGHT, buff=0.12)
    return VGroup(a, b)


def tick_numbers(p: ComplexPlane, xs=(), ys=(), size=20):
    g = VGroup()
    for x in xs:
        g.add(MT(f"{x}", size, GREY_B).next_to(p.n2p(complex(x, 0)), DOWN, buff=0.08))
    for y in ys:
        lab = "i" if y == 1 else ("-i" if y == -1 else f"{y}i")
        g.add(MT(lab, size, GREY_B).next_to(p.n2p(complex(0, y)), LEFT, buff=0.08))
    return g


def panel(*lines, size=28, buff=0.22, color=WHITE):
    mobs = [CT(l, size, color) if isinstance(l, str) else l for l in lines]
    return VGroup(*mobs).arrange(DOWN, aligned_edge=LEFT, buff=buff)


def boxed(m, color=GREY_D):
    r = SurroundingRectangle(m, color=color, buff=0.2, corner_radius=0.1)
    r.set_fill(BLACK, opacity=0.75)
    return VGroup(r, m)


def title_bar(s: str, size=34):
    t = CT(s, size).to_edge(UP, buff=0.22)
    bg = BackgroundRectangle(t, fill_opacity=0.85, buff=0.08)
    return VGroup(bg, t)
