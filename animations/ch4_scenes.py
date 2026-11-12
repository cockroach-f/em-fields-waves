"""第 4 章 恒定电流的磁场 —— manim 动画源码（LaTeX 排版）."""
import numpy as np
from scipy.special import ellipk, ellipe

from common import *  # noqa: F401,F403
from fieldtools import *  # noqa: F401,F403
from ch2_scenes import plain_axes


def wire_dot(pos, out=True, r=0.16, color=C_HL):
    c = Circle(radius=r, color=color, stroke_width=3, fill_color=BLACK, fill_opacity=1).move_to(pos)
    if out:
        s = Dot(pos, radius=0.045, color=color)
    else:
        s = VGroup(Line(pos + (UL * r * 0.65), pos + (DR * r * 0.65), color=color, stroke_width=3),
                   Line(pos + (UR * r * 0.65), pos + (DL * r * 0.65), color=color, stroke_width=3))
    return VGroup(c, s)


def loop_flux(X, Z, a=1.0):
    """圆电流环（半径 a，位于 z=0）的磁通函数 ψ=ρA_φ（任意单位），X 可为负（子午面左半）."""
    R = np.abs(X) + 1e-9
    m = 4 * a * R / ((a + R) ** 2 + Z ** 2)
    m = np.clip(m, 0, 1 - 1e-9)
    k = np.sqrt(m)
    A = np.sqrt(a / R) / k * ((1 - m / 2) * ellipk(m) - ellipe(m))
    return R * A


# --------------------------------------------------------------------------
# 4.1 毕奥–萨伐尔定律：有限长直导线 + 圆电流环
# --------------------------------------------------------------------------
class C4_BiotSavart(Scene):
    def construct(self):
        title = title_bar(r"毕奥–萨伐尔定律：$\dd\vv B=\dfrac{\mu_0}{4\pi}\dfrac{I\,\dd\vv l\times\ar}{R^2}$，把每段电流元的贡献叠加起来")
        fitw(title, 13.6)
        self.play(FadeIn(title))
        # ---------------- 有限长直导线
        ax = plain_axes(xr=(-1, 3), yr=(-2.4, 2.4), size=4.0).shift(LEFT * 4.3 + DOWN * 0.4)
        L1, L2, rho = -1.6, 2.0, 1.6
        wire = Line(ax.c2p(0, L1), ax.c2p(0, L2), color=C_HL, stroke_width=6)
        tip = Arrow(ax.c2p(0, 0.2), ax.c2p(0, 1.0), buff=0, color=C_HL, stroke_width=6)
        Ilab = MT("I", 30, C_HL).next_to(tip, LEFT, buff=0.1)
        Pd = Dot(ax.c2p(rho, 0), color=WHITE)
        Pl = MT("P", 28).next_to(Pd, RIGHT, buff=0.1)
        perp = DashedLine(ax.c2p(0, 0), ax.c2p(rho, 0), color=GREY_B)
        rl = MT(r"\rho", 26, GREY_B).next_to(perp, DOWN, buff=0.05)
        Bsym = wire_dot(ax.c2p(rho, 0) + RIGHT * 0.75 + UP * 0.35, out=False, r=0.13, color=C_H)
        Bl = CT(r"$\dd\vv B$ 垂直纸面向里", 20, C_H).next_to(Bsym, UP, buff=0.08)
        self.play(Create(wire), GrowArrow(tip), FadeIn(Ilab), FadeIn(Pd), FadeIn(Pl), Create(perp), FadeIn(rl))
        self.play(FadeIn(Bsym), FadeIn(Bl))
        # 积分曲线
        ax2 = Axes(x_range=[-2.5, 2.5, 1], y_range=[0, 1.2, 0.5], x_length=5.2, y_length=2.4,
                   axis_config={"stroke_width": 1.5, "include_ticks": False, "include_tip": False}).move_to(RIGHT * 3.3 + UP * 1.2)
        f = lambda z: rho ** 3 / (rho ** 2 + z ** 2) ** 1.5  # 归一化到 z=0 处为 1
        g = ax2.plot(f, x_range=[-2.5, 2.5], color=GREY_B, stroke_width=2)
        gl = CT(r"电流元 $I\dd z'$ 在 $P$ 点的贡献 $\propto\dfrac{\rho\,\dd z'}{(\rho^2+z'^2)^{3/2}}$", 22).next_to(ax2, UP, buff=0.1)
        xl = MT("z'", 24, GREY_B).next_to(ax2.x_axis, RIGHT, buff=0.05)
        self.play(Create(ax2), Create(g), FadeIn(gl), FadeIn(xl))
        zt = ValueTracker(L1)
        elem = always_redraw(lambda: Line(ax.c2p(0, zt.get_value() - 0.12), ax.c2p(0, zt.get_value() + 0.12), color=WHITE, stroke_width=10))
        Rline = always_redraw(lambda: DashedLine(ax.c2p(0, zt.get_value()), ax.c2p(rho, 0), color=C_E, stroke_width=2))
        area = always_redraw(lambda: ax2.get_area(g, x_range=[L1, max(zt.get_value(), L1 + 1e-3)], color=C_H, opacity=0.55))
        self.add(area, elem, Rline)
        self.play(zt.animate.set_value(L2), run_time=4, rate_func=linear)
        # 角度
        al1 = np.arctan2(L1, rho)
        al2 = np.arctan2(L2, rho)
        c1 = DashedLine(ax.c2p(rho, 0), ax.c2p(0, L1), color=GREY_A, stroke_width=2)
        c2 = DashedLine(ax.c2p(rho, 0), ax.c2p(0, L2), color=GREY_A, stroke_width=2)
        a1 = MT(r"\alpha_1", 24, GREY_A).move_to(ax.c2p(rho - 0.55, -0.32))
        a2 = MT(r"\alpha_2", 24, GREY_A).move_to(ax.c2p(rho - 0.55, 0.42))
        res = VGroup(
            MT(r"B=\frac{\mu_0I}{4\pi\rho}\left(\sin\alpha_2-\sin\alpha_1\right)", 32, C_H),
            CT(r"$\alpha$ 从垂线量起，向上为正（图中 $\alpha_1<0$）", 22, GREY_A),
            CT(r"无限长：$\alpha_1\to-\dfrac\pi2$，$\alpha_2\to\dfrac\pi2$，$\ B=\dfrac{\mu_0I}{2\pi\rho}$", 24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        fitw(res, 6.0).move_to(RIGHT * 3.3 + DOWN * 1.7)
        self.remove(Rline)
        self.play(Create(c1), Create(c2), FadeIn(a1), FadeIn(a2), FadeIn(res[0]), FadeIn(res[1]))
        self.play(FadeIn(res[2]))
        self.wait(2.5)
        left = VGroup(wire, tip, Ilab, Pd, Pl, perp, rl, Bsym, Bl, c1, c2, a1, a2)
        self.play(FadeOut(left), FadeOut(elem), FadeOut(area), FadeOut(ax2), FadeOut(g), FadeOut(gl), FadeOut(xl), FadeOut(res))
        # ---------------- 圆电流环（子午面）
        ax3 = plain_axes(xr=(-3, 3), yr=(-3, 3), size=5.8).shift(LEFT * 3.3 + DOWN * 0.45)
        levels = [0.04, 0.09, 0.16, 0.26, 0.4, 0.6, 0.9]
        cl = contour_lines(ax3, lambda X, Y: loop_flux(X, Y, 1.0), levels, [C_H] * len(levels),
                           xr=(-3, 3), yr=(-3, 3), n=150, sw=2.0)
        ring = DashedLine(ax3.c2p(-1, 0), ax3.c2p(1, 0), color=GREY_B, stroke_width=1.5)
        wl = wire_dot(ax3.c2p(-1, 0), out=True)
        wr = wire_dot(ax3.c2p(1, 0), out=False)
        zax = DashedLine(ax3.c2p(0, -3), ax3.c2p(0, 3), color=GREY_C, stroke_width=1.5)
        arrs = VGroup(*[Arrow(ax3.c2p(0, y - 0.25), ax3.c2p(0, y + 0.25), buff=0, color=C_H, stroke_width=4) for y in (-1.8, 0, 1.8)])
        arrs.add(Arrow(ax3.c2p(2.35, 0.3), ax3.c2p(2.35, -0.3), buff=0, color=C_H, stroke_width=4),
                 Arrow(ax3.c2p(-2.35, 0.3), ax3.c2p(-2.35, -0.3), buff=0, color=C_H, stroke_width=4))
        cap = CT(r"圆电流环的磁力线（过轴线的剖面）：$\odot$ 流出纸面，$\otimes$ 流入纸面", 22).next_to(ax3, UP, buff=0.0)
        fitw(cap, 6.2)
        self.play(Create(zax), Create(ring), FadeIn(wl), FadeIn(wr), FadeIn(cap))
        self.play(Create(cl), run_time=2.5)
        self.play(*[GrowArrow(a) for a in arrs])
        txt = VGroup(
            CT(r"轴线上（练习 1）：", 24),
            MT(r"\vv B=\az\frac{\mu_0Ia^2}{2\left(a^2+z^2\right)^{3/2}}", 32, C_H),
            CT(r"磁力线是闭合曲线，没有起点和终点：", 24),
            MT(r"\nabla\cdot\vv B=0", 32, C_HL),
            CT(r"远处（$r\gg a$）等效为磁偶极子 $\vv p_m=I\pi a^2\az$，", 24),
            CT(r"磁力线形状与电偶极子的电力线相同", 24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        fitw(txt, 6.0).move_to(RIGHT * 3.6 + DOWN * 0.3)
        for m in txt:
            self.play(FadeIn(m), run_time=0.7)
        self.wait(3)


# --------------------------------------------------------------------------
# 4.1.3 安培环路定律：同轴线的 H(ρ)
# --------------------------------------------------------------------------
class C4_Ampere(Scene):
    def construct(self):
        title = title_bar(r"安培环路定律 $\oint_C\vv H\cdot\dd\vv l=I$：同轴线截面上取半径 $\rho$ 的圆周，数一数穿过它的电流")
        fitw(title, 13.6)
        self.play(FadeIn(title))
        a, b, c = 0.6, 1.5, 1.85
        s = 1.45  # 单位 → 屏幕
        O = LEFT * 3.6 + DOWN * 0.4
        inner = Circle(radius=a * s, color=C_HL, fill_color=C_HL, fill_opacity=0.45, stroke_width=2).move_to(O)
        outer = Annulus(inner_radius=b * s, outer_radius=c * s, color=C_NEG, fill_opacity=0.45, stroke_width=0).move_to(O)
        ob = VGroup(Circle(radius=b * s, color=C_NEG, stroke_width=2).move_to(O), Circle(radius=c * s, color=C_NEG, stroke_width=2).move_to(O))
        l_in = CT(r"$I$（流出）", 22, C_HL).move_to(O)
        l_out = CT(r"$-I$（流入）", 22, C_NEG).move_to(O + UP * (b + c) / 2 * s)
        self.play(FadeIn(inner), FadeIn(outer), FadeIn(ob), FadeIn(l_in), FadeIn(l_out))
        dims = VGroup(MT("a", 22, GREY_A).move_to(O + (a * s + 0.15) * RIGHT + DOWN * 0.18),
                      MT("b", 22, GREY_A).move_to(O + (b * s - 0.15) * RIGHT + DOWN * 0.18),
                      MT("c", 22, GREY_A).move_to(O + (c * s + 0.18) * RIGHT + DOWN * 0.18))
        self.play(FadeIn(dims))

        def Henc(r):
            if r < a:
                return r * r / (a * a)
            if r < b:
                return 1.0
            if r < c:
                return (c * c - r * r) / (c * c - b * b)
            return 0.0

        def H(r):
            return Henc(r) / (2 * np.pi * max(r, 1e-6))

        rt = ValueTracker(0.05)
        circ = always_redraw(lambda: DashedVMobject(Circle(radius=rt.get_value() * s, color=C_H, stroke_width=3).move_to(O), num_dashes=40))
        harrows = always_redraw(lambda: VGroup(*[
            Arrow(O + rt.get_value() * s * np.array([np.cos(t), np.sin(t), 0]),
                  O + rt.get_value() * s * np.array([np.cos(t), np.sin(t), 0]) + 0.9 * H(rt.get_value()) / H(a) * np.array([-np.sin(t), np.cos(t), 0]),
                  buff=0, color=C_H, stroke_width=4, max_tip_length_to_length_ratio=0.35)
            for t in np.linspace(0, TAU, 8, endpoint=False)] if H(rt.get_value()) > 0.003 else []))
        # 右侧曲线
        ax = Axes(x_range=[0, 2.4, 0.5], y_range=[0, 0.3, 0.1], x_length=5.6, y_length=2.3,
                  axis_config={"stroke_width": 1.5, "include_ticks": False, "include_tip": False}).move_to(RIGHT * 3.4 + DOWN * 2.1)
        yl = MT(r"H(\rho)", 26, C_H).next_to(ax.y_axis, UP, buff=0.08)
        xl = MT(r"\rho", 26, GREY_B).next_to(ax.x_axis, RIGHT, buff=0.08)
        marks = VGroup(*[VGroup(DashedLine(ax.c2p(v, 0), ax.c2p(v, 0.3), color=GREY_D, stroke_width=1.5),
                                MT(n, 22, GREY_A).next_to(ax.c2p(v, 0), DOWN, buff=0.08)) for v, n in [(a, "a"), (b, "b"), (c, "c")]])
        self.play(Create(ax), FadeIn(yl), FadeIn(xl), FadeIn(marks))
        graph = always_redraw(lambda: ax.plot(H, x_range=[0.001, max(rt.get_value(), 0.0011), 0.004], color=C_H, stroke_width=3)
                              if rt.get_value() > 0.01 else VGroup())
        enc = always_redraw(lambda: CT(rf"$I_{{\text{{enc}}}}={Henc(rt.get_value()):.2f}\,I$", 26, C_E).move_to(O + UP * (c * s + 0.42)))
        self.add(circ, harrows, graph, enc)
        formulas = [
            (a, MT(r"\rho<a:\ H=\frac{I\rho}{2\pi a^2}", 26)),
            (b, MT(r"a<\rho<b:\ H=\frac{I}{2\pi\rho}", 28)),
            (c, MT(r"b<\rho<c:\ H=\frac{I}{2\pi\rho}\,\frac{c^2-\rho^2}{c^2-b^2}", 28)),
            (2.15, CT(r"$\rho>c:\ H=0$（屏蔽）", 28)),
        ]
        shown = VGroup()
        for stop, fm in formulas:
            self.play(rt.animate.set_value(stop), run_time=2.2, rate_func=linear)
            shown.add(fm)
            shown.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            fitw(shown, 6.2)
            shown.next_to(title, DOWN, buff=0.25).align_to(ax, LEFT)
            self.play(FadeIn(fm), run_time=0.5)
            self.wait(0.6)
        note = CT(r"外导体流回的 $-I$ 使外部 $I_{\text{enc}}=0$：同轴线的磁场被“关”在内外导体之间", 24, C_HL).to_edge(DOWN, buff=0.2)
        fitw(note, 13)
        self.play(FadeIn(note))
        self.wait(3)


# --------------------------------------------------------------------------
# 4.2 磁化：分子电流排列 → 内部抵消 → 表面束缚电流
# --------------------------------------------------------------------------
def square_loop(center, size, ccw=True, color=C_H, sw=2.5):
    h = size / 2
    corners = [center + np.array(v) * h for v in [(-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0)]]
    if not ccw:
        corners = corners[::-1]
    g = VGroup()
    for i in range(4):
        p, q = corners[i], corners[(i + 1) % 4]
        g.add(Line(p, q, color=color, stroke_width=sw))
        mid = (p + q) / 2
        d = (q - p) / np.linalg.norm(q - p) * 0.09
        g.add(Arrow(mid - d, mid + d, buff=0, color=color, stroke_width=sw, max_tip_length_to_length_ratio=0.9,
                    max_stroke_width_to_length_ratio=20))
    return g


class C4_Magnetization(Scene):
    def construct(self):
        title = title_bar(r"磁介质的磁化：分子电流环有序排列，内部相互抵消，表面剩下束缚电流 $\vv J_{Sb}=\vv M\times\an$")
        fitw(title, 13.6)
        self.play(FadeIn(title))
        nx, ny, sz = 7, 5, 0.62
        O = LEFT * 3.4 + DOWN * 0.3
        box = Rectangle(width=nx * sz + 0.1, height=ny * sz + 0.1, color=GREY_A, stroke_width=2,
                        fill_color="#14242e", fill_opacity=1).move_to(O)
        bl = CT(r"磁介质", 22, GREY_A).next_to(box, DOWN, buff=0.1)
        self.play(FadeIn(box), FadeIn(bl))
        rng = np.random.default_rng(3)
        centers = [O + np.array([(i - (nx - 1) / 2) * sz, (j - (ny - 1) / 2) * sz, 0]) for j in range(ny) for i in range(nx)]
        rand = VGroup()
        for cc in centers:
            r = 0.08 + 0.12 * rng.random()
            ccw = rng.random() < 0.5
            cc = cc + np.r_[(rng.random(2) - 0.5) * 0.12, 0]
            circ = Circle(radius=r, color=C_H, stroke_width=2).move_to(cc)
            ang = rng.random() * TAU
            p = cc + r * np.array([np.cos(ang), np.sin(ang), 0])
            t = np.array([-np.sin(ang), np.cos(ang), 0]) * (1 if ccw else -1) * 0.07
            rand.add(VGroup(circ, Arrow(p - t, p + t, buff=0, color=C_H, stroke_width=2, max_tip_length_to_length_ratio=0.9,
                                        max_stroke_width_to_length_ratio=20)))
        cap1 = CT(r"无外场：分子电流（磁偶极矩 $\vv p_m=I_a\vv S$）取向杂乱，$\vv M=0$", 24).move_to(RIGHT * 3.4 + UP * 2.0)
        fitw(cap1, 6.4)
        self.play(FadeIn(rand), FadeIn(cap1))
        self.wait(1.2)
        # 外场 B（指向纸外），全部变为逆时针方形环
        loops = VGroup(*[square_loop(cc, sz * 0.86) for cc in centers])
        bext = VGroup(*[wire_dot(O + np.array([x, 2.05, 0]), out=True, r=0.1, color=GREY_B) for x in np.linspace(-2.0, 2.0, 6)])
        bel = CT(r"外加 $\vv B$ 指向纸外", 20, GREY_B).next_to(bext, UP, buff=0.06)
        cap2 = CT(r"加外场：分子电流环转向，$\vv p_m$ 都沿 $\vv B$ 方向（纸外）", 24).move_to(cap1)
        fitw(cap2, 6.4)
        self.play(FadeIn(bext), FadeIn(bel), ReplacementTransform(rand, loops), ReplacementTransform(cap1, cap2), run_time=1.8)
        self.wait(1)
        # 相邻两环的公共边电流相反
        k = 2 * nx + 3
        e1 = loops[k][2].copy().set_color(C_HL).set_stroke(width=6)  # 右边
        e2 = loops[k + 1][6].copy().set_color(C_HL).set_stroke(width=6)  # 左边
        cap3 = VGroup(CT(r"相邻两环的公共边上电流方向相反，", 24), CT(r"内部处处抵消……", 24)).arrange(DOWN, aligned_edge=LEFT)
        fitw(cap3, 6.4).move_to(RIGHT * 3.4 + UP * 0.9)
        self.play(Create(e1), Create(e2), FadeIn(cap3))
        self.wait(1.2)
        # 只剩表面电流
        W, Hh = nx * sz, ny * sz
        rect = Rectangle(width=W * 0.97, height=Hh * 0.97, color=C_HL, stroke_width=5).move_to(O)
        sarrs = VGroup()
        for i in range(nx):
            x = O[0] + (i - (nx - 1) / 2) * sz
            sarrs.add(Arrow([x - 0.1, O[1] - Hh * 0.485, 0], [x + 0.1, O[1] - Hh * 0.485, 0], buff=0, color=C_HL, stroke_width=5,
                            max_tip_length_to_length_ratio=0.9, max_stroke_width_to_length_ratio=20))
            sarrs.add(Arrow([x + 0.1, O[1] + Hh * 0.485, 0], [x - 0.1, O[1] + Hh * 0.485, 0], buff=0, color=C_HL, stroke_width=5,
                            max_tip_length_to_length_ratio=0.9, max_stroke_width_to_length_ratio=20))
        for j in range(ny):
            y = O[1] + (j - (ny - 1) / 2) * sz
            sarrs.add(Arrow([O[0] + W * 0.485, y - 0.1, 0], [O[0] + W * 0.485, y + 0.1, 0], buff=0, color=C_HL, stroke_width=5,
                            max_tip_length_to_length_ratio=0.9, max_stroke_width_to_length_ratio=20))
            sarrs.add(Arrow([O[0] - W * 0.485, y + 0.1, 0], [O[0] - W * 0.485, y - 0.1, 0], buff=0, color=C_HL, stroke_width=5,
                            max_tip_length_to_length_ratio=0.9, max_stroke_width_to_length_ratio=20))
        cap4 = VGroup(
            CT(r"……只剩沿表面流动的\textbf{束缚面电流}：", 24).set_color(WHITE),
            MT(r"\vv J_{Sb}=\vv M\times\an,\qquad \vv J_b=\nabla\times\vv M", 30, C_HL),
            CT(r"（$\vv M$ 均匀时 $\vv J_b=0$；$\an$ 为介质表面外法线）", 22, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        fitw(cap4, 6.4).move_to(RIGHT * 3.4 + DOWN * 0.35)
        self.play(FadeOut(e1), FadeOut(e2), loops.animate.set_opacity(0.15), Create(rect), FadeIn(sarrs), FadeIn(cap4), run_time=1.6)
        self.wait(1.2)
        cap5 = VGroup(
            CT(r"把束缚电流也算进安培定律：$\nabla\times\dfrac{\vv B}{\mu_0}=\vv J+\nabla\times\vv M$", 24),
            MT(r"\vv H=\frac{\vv B}{\mu_0}-\vv M,\quad \nabla\times\vv H=\vv J,\quad \vv B=\mu_0(\vv H+\vv M)=\mu\vv H", 28, C_H),
            CT(r"与电介质完全对偶：$\vv D=\varepsilon_0\vv E+\vv P$，$\nabla\cdot\vv D=\rho_V$", 22, C_E),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        fitw(cap5, 6.4).move_to(RIGHT * 3.4 + DOWN * 2.35)
        for m in cap5:
            self.play(FadeIn(m), run_time=0.8)
        self.wait(3)
