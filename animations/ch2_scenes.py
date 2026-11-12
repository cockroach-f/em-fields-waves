"""第 2 章 静电场和恒定电场 —— manim 动画源码（LaTeX 排版）."""
import numpy as np

from common import *  # noqa: F401,F403
from fieldtools import *  # noqa: F401,F403


def plain_axes(xr=(-3, 3), yr=(-3, 3), size=6.0, show=False):
    ax = Axes(x_range=[xr[0], xr[1], 1], y_range=[yr[0], yr[1], 1], x_length=size,
              y_length=size * (yr[1] - yr[0]) / (xr[1] - xr[0]),
              axis_config={"stroke_width": 1, "stroke_opacity": 0.35 if show else 0.0, "include_ticks": False, "include_tip": False})
    return ax


def charge_dot(ax, q, x, y):
    col = C_POS if q > 0 else C_NEG
    r = 0.13 + 0.03 * abs(q)
    d = Circle(radius=r, color=col, fill_opacity=1, stroke_width=0).move_to(ax.c2p(x, y))
    s = MT("+" if q > 0 else "-", 30, WHITE).move_to(d)
    return VGroup(d, s)


def field_line_set(ax, charges, n_per=14, color=C_E, box=(-3.2, 3.2, -3.2, 3.2)):
    F = charges_field(charges)

    def near(p, tol=0.09):
        return any((p[0] - a) ** 2 + (p[1] - b) ** 2 < tol * tol for _, a, b in charges)

    lines = VGroup()
    arrows = VGroup()
    for q, a, b in charges:
        n = int(round(n_per * abs(q)))
        for k in range(n):
            t = (k + 0.5) * TAU / n
            p0 = (a + 0.1 * np.cos(t), b + 0.1 * np.sin(t))
            sign = 1.0 if q > 0 else -1.0
            pts = trace(F, p0, h=0.025, nmax=900, box=box, stop=lambda p: near(p), sign=sign)
            if q < 0 and near(pts[-1]):
                continue
            lines.add(polyline(ax, pts, color, 2.2))
            arrows.add(mid_arrow(ax, pts if q > 0 else pts[::-1], color, frac=0.45 if q > 0 else 0.55))
    return lines, arrows


# --------------------------------------------------------------------------
# 2.1 电力线与等位线
# --------------------------------------------------------------------------
class C2_FieldLines(Scene):
    def construct(self):
        title = title_bar(r"电力线（黄）与等位线（蓝）：处处正交，电力线从正电荷出发、终止于负电荷")
        fitw(title, 13.6)
        self.play(FadeIn(title))
        ax = plain_axes(size=6.2).shift(LEFT * 3.2 + DOWN * 0.45)
        configs = [
            ([(1, 0, 0)], r"单个点电荷 $+q$", r"$\vv E=\dfrac{q}{4\pi\varepsilon_0r^2}\ar$，等位面是球面"),
            ([(1, -1, 0), (-1, 1, 0)], r"电偶极子 $+q,-q$", r"远处 $\phi\approx\dfrac{p\cos\theta}{4\pi\varepsilon_0r^2}$，$\vv p=q\vv d$ 由 $-q$ 指向 $+q$"),
            ([(1, -1, 0), (1, 1, 0)], r"两个等量正电荷", r"中点处 $\vv E=0$（鞍点），电力线互相“排斥”"),
            ([(1, -1, 0), (-2, 1, 0)], r"$+q$ 与 $-2q$", r"零电位面是一个球面（图中红圈）：$\dfrac{q}{R_1}=\dfrac{2q}{R_2}$"),
        ]
        old = None
        for charges, name, note in configs:
            lines, arrows = field_line_set(ax, charges)
            P = charges_potential(charges)
            vmax = 3.0
            levels = [v for v in np.linspace(-vmax, vmax, 13) if abs(v) > 1e-6]
            cols = [interpolate_color(BLUE_B, BLUE_E, abs(v) / vmax) for v in levels]
            eq = contour_lines(ax, P, levels, cols, n=110, sw=1.6, opacity=0.9)
            dots = VGroup(*[charge_dot(ax, *c) for c in charges])
            txt = VGroup(CT(name, 30, C_HL), CT(note, 24)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
            fitw(txt, 6.0).move_to(RIGHT * 3.6 + UP * 0.6)
            if old is not None:
                self.play(FadeOut(old), run_time=0.6)
            self.play(FadeIn(dots), FadeIn(txt))
            self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.03), run_time=2.2)
            self.play(FadeIn(arrows), FadeIn(eq), run_time=1.0)
            extra = VGroup()
            if len(charges) == 2 and charges[1][0] == -2:
                # +q 在 (-1,0)，-2q 在 (1,0)：零电位圆心 (-5/3,0)，半径 4/3
                c0 = Circle(radius=4 / 3 * ax.x_length / 6, color=RED, stroke_width=4).move_to(ax.c2p(-5 / 3, 0))
                lab = CT(r"$\phi=0$", 24, RED).next_to(c0, DOWN, buff=0.05)
                extra.add(c0, lab)
                self.play(Create(c0), FadeIn(lab))
            self.wait(1.6)
            old = VGroup(lines, arrows, eq, dots, txt, extra)
        rule = VGroup(
            CT(r"电力线密度 $\propto|\vv E|$；电力线 $\perp$ 等位面", 26),
            CT(r"$\vv E=-\nabla\phi$：指向电位降低最快的方向", 26, C_E),
            CT(r"电力线不闭合、不相交（$\nabla\times\vv E=0$）", 26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        fitw(rule, 6.0).move_to(RIGHT * 3.6 + DOWN * 2.0)
        self.play(FadeIn(rule))
        self.wait(2.5)


# --------------------------------------------------------------------------
# 2.2 高斯定律：通量只数包围的电荷
# --------------------------------------------------------------------------
class C2_Gauss(Scene):
    def construct(self):
        title = title_bar(r"高斯定律 $\oint_S\vv D\cdot\dd\vv S=q$：与闭合面的形状无关，只看面内电荷")
        fitw(title, 13.6)
        self.play(FadeIn(title))
        ax = plain_axes(size=6.4).shift(LEFT * 3.1 + DOWN * 0.45)
        N = 16
        rays = VGroup()
        angs = [(k + 0.5) * TAU / N for k in range(N)]
        for t in angs:
            rays.add(Line(ax.c2p(0.12 * np.cos(t), 0.12 * np.sin(t)), ax.c2p(3.1 * np.cos(t), 3.1 * np.sin(t)),
                          color=C_E, stroke_width=2))
        q = charge_dot(ax, 1, 0, 0)
        self.play(FadeIn(q), LaggedStart(*[Create(r) for r in rays], lag_ratio=0.03))
        cap0 = CT(r"每条电力线代表同样多的电通量，点电荷 $q$ 共发出 $N=16$ 条", 24).move_to(RIGHT * 3.5 + UP * 2.2)
        fitw(cap0, 6.2)
        self.play(FadeIn(cap0))

        def blob(t, kind):
            if kind == 0:
                return 1.3 * np.cos(t), 1.3 * np.sin(t)
            if kind == 1:
                r = 1.75 + 0.45 * np.sin(3 * t) + 0.3 * np.cos(5 * t)
                return r * np.cos(t), r * np.sin(t)
            return 2.0 + 0.75 * np.cos(t), 0.9 + 0.75 * np.sin(t)

        def inside(x, y, kind):
            if kind == 0:
                return x * x + y * y < 1.69
            if kind == 1:
                t = np.arctan2(y, x)
                return np.hypot(x, y) < 1.75 + 0.45 * np.sin(3 * t) + 0.3 * np.cos(5 * t)
            return (x - 2.0) ** 2 + (y - 0.9) ** 2 < 0.5625

        names = [r"球面（圆）", r"任意形状的闭合面", r"不包围电荷的闭合面"]
        old = None
        for kind in range(3):
            ts = np.linspace(0, TAU, 300)
            curve = VMobject(color=WHITE, stroke_width=3.5)
            curve.set_points_as_corners([ax.c2p(*blob(t, kind)) for t in ts])
            outs, ins = VGroup(), VGroup()
            for t in angs:
                rs = np.linspace(0.12, 3.1, 1500)
                st = [inside(r * np.cos(t), r * np.sin(t), kind) for r in rs]
                for i in range(1, len(rs)):
                    if st[i] != st[i - 1]:
                        p = ax.c2p(rs[i] * np.cos(t), rs[i] * np.sin(t))
                        if st[i - 1] and not st[i]:
                            outs.add(Dot(p, radius=0.07, color=GREEN))
                        else:
                            ins.add(Dot(p, radius=0.07, color=RED))
            n_out, n_in = len(outs), len(ins)
            info = VGroup(
                CT(names[kind], 28, C_HL),
                CT(rf"穿出（绿）：{n_out}　穿入（红）：{n_in}", 26),
                CT(rf"净通量 $\propto {n_out}-{n_in}={n_out - n_in}$", 28, GREEN if n_out - n_in else GREY_B),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
            fitw(info, 6.0).move_to(RIGHT * 3.5 + UP * 0.3)
            if old is not None:
                self.play(FadeOut(old), run_time=0.6)
            self.play(Create(curve), FadeIn(info))
            anims = [FadeIn(d, scale=1.5) for d in outs] + [FadeIn(d, scale=1.5) for d in ins]
            self.play(LaggedStart(*anims, lag_ratio=0.05), run_time=1.5)
            self.wait(1.4)
            old = VGroup(curve, outs, ins, info)
        self.play(FadeOut(old), FadeOut(cap0))
        box = boxed(VGroup(
            MT(r"\oint_S\vv D\cdot\dd\vv S=\sum q_{\text{in}}", 40, C_HL),
            CT(r"面外电荷的电力线“进一次、出一次”，贡献为零", 24, GREY_B),
            CT(r"散度定理 $\Rightarrow$ 微分形式 $\nabla\cdot\vv D=\rho_V$", 26),
            CT(r"对称性好时（球、柱、面）选高斯面使 $D$ 在面上为常数", 24, GREY_B),
        ).arrange(DOWN, buff=0.25)).move_to(RIGHT * 3.4 + DOWN * 0.3)
        fitw(box, 6.4)
        self.play(FadeIn(box))
        self.wait(3)


# --------------------------------------------------------------------------
# 2.3 电介质的极化：束缚电荷削弱介质内的电场
# --------------------------------------------------------------------------
class C2_Polarization(Scene):
    def construct(self):
        title = title_bar(r"电介质的极化：电偶极子转向排列，表面出现束缚电荷 $\rho_{Sb}=\vv P\cdot\an$")
        fitw(title, 13.6)
        self.play(FadeIn(title))
        X0, W = -2.6, 6.4
        top = Rectangle(width=W, height=0.18, color=C_POS, fill_opacity=1).move_to([X0, 2.25, 0])
        bot = Rectangle(width=W, height=0.18, color=C_NEG, fill_opacity=1).move_to([X0, -2.85, 0])
        tl = VGroup(*[MT("+", 26, C_POS).move_to([X0 - W / 2 + 0.4 + 0.8 * k, 2.55, 0]) for k in range(8)])
        bl = VGroup(*[MT("-", 26, C_NEG).move_to([X0 - W / 2 + 0.4 + 0.8 * k, -3.15, 0]) for k in range(8)])
        self.play(FadeIn(top), FadeIn(bot), FadeIn(tl), FadeIn(bl))
        slab = Rectangle(width=W, height=2.4, color=GREY_B, stroke_width=2, fill_color=BLUE_E, fill_opacity=0.35).move_to([X0, -0.3, 0])
        sl = CT(r"电介质 $\varepsilon$", 24, GREY_A).next_to(slab, RIGHT, buff=0.1)
        self.play(FadeIn(slab), FadeIn(sl))
        rng = np.random.default_rng(3)
        dips = VGroup()
        pos = []
        for i in range(8):
            for j in range(3):
                pos.append(np.array([X0 - W / 2 + 0.4 + 0.8 * i, -0.3 - 0.75 + 0.75 * j, 0]))

        def dipole(c, ang):
            d = 0.22 * np.array([np.cos(ang), np.sin(ang), 0])
            body = Line(c - d, c + d, color=GREY_B, stroke_width=3)
            pq = Dot(c + d, radius=0.07, color=C_POS)
            nq = Dot(c - d, radius=0.07, color=C_NEG)
            return VGroup(body, pq, nq)

        angs0 = rng.uniform(0, TAU, len(pos))
        for c, a in zip(pos, angs0):
            dips.add(dipole(c, a))
        cap = CT(r"无外场：分子电偶极矩取向杂乱，宏观 $\vv P=0$", 26)
        fitw(cap, 4.9).move_to(RIGHT * 4.45 + UP * 1.5)
        self.play(FadeIn(dips), FadeIn(cap))
        self.wait(0.8)
        lines_vac = VGroup()
        xs = [X0 - W / 2 + 0.4 + 0.8 * k for k in range(8)]
        for x in xs:
            lines_vac.add(Arrow([x, 2.1, 0], [x, -2.7, 0], buff=0, color=C_E, stroke_width=2, max_tip_length_to_length_ratio=0.04))
        cap2 = CT(r"加外场 $\vv E_0$（自由电荷产生）：偶极子转向，沿 $\vv E$ 排列", 26).move_to(cap)
        fitw(cap2, 4.9).move_to(RIGHT * 4.45 + UP * 1.5)
        self.play(FadeIn(lines_vac), ReplacementTransform(cap, cap2))
        self.play(*[Rotate(d, angle=(-PI / 2 - a + PI) % TAU - PI, about_point=c) for d, c, a in zip(dips, pos, angs0)], run_time=2.5)
        self.wait(0.5)
        sb_top = VGroup(*[MT("-", 30, C_NEG).move_to([x + 0.4, 0.75, 0]) for x in xs[:-1]])
        sb_bot = VGroup(*[MT("+", 30, C_POS).move_to([x + 0.4, -1.35, 0]) for x in xs[:-1]])
        cap3 = VGroup(
            CT(r"内部相邻偶极子的 $\pm$ 抵消，只在表面剩下", 24),
            CT(r"束缚面电荷 $\rho_{Sb}=\vv P\cdot\an$", 26, C_HL),
            CT(r"（上表面 $\an=\ay$：$-$；下表面 $\an=-\ay$：$+$）", 22, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(cap2).shift(DOWN * 0.3)
        fitw(cap3, 4.9).move_to(RIGHT * 4.45 + UP * 1.3)
        self.play(FadeIn(sb_top), FadeIn(sb_bot), ReplacementTransform(cap2, cap3))
        self.wait(0.8)
        new_lines = VGroup()
        for k, x in enumerate(xs):
            if k % 2 == 0:
                new_lines.add(Arrow([x, 2.1, 0], [x, -2.7, 0], buff=0, color=C_E, stroke_width=2, max_tip_length_to_length_ratio=0.04))
            else:
                new_lines.add(VGroup(Line([x, 2.1, 0], [x, 0.9, 0], color=C_E, stroke_width=2),
                                     Arrow([x, -1.5, 0], [x, -2.7, 0], buff=0, color=C_E, stroke_width=2, max_tip_length_to_length_ratio=0.2)))
        cap4 = VGroup(
            CT(r"部分 $\vv E$ 线终止于束缚电荷：介质内 $E$ 变小", 24, C_E),
            MT(r"\vv E=\frac{\vv E_0}{\varepsilon_r}", 34, C_E),
            CT(r"但 $\vv D=\varepsilon_0\vv E+\vv P$ 只认自由电荷：", 24),
            CT(r"$\nabla\cdot\vv D=\rho_V$，$\vv D=\varepsilon\vv E$，$D$ 线穿过介质不中断", 24, C_HL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        fitw(cap4, 4.9).move_to(RIGHT * 4.45 + DOWN * 1.45)
        self.play(ReplacementTransform(lines_vac, new_lines), FadeIn(cap4))
        self.wait(3)


# --------------------------------------------------------------------------
# 2.5 边界条件：电力线在介质分界面上“折射”
# --------------------------------------------------------------------------
class C2_Refraction(Scene):
    def construct(self):
        title = title_bar(r"分界面上 $E_{1t}=E_{2t}$，$D_{1n}=D_{2n}$ $\Rightarrow$ $\dfrac{\tan\theta_1}{\tan\theta_2}=\dfrac{\varepsilon_1}{\varepsilon_2}$")
        self.play(FadeIn(title))
        L = 7.0
        cx = -2.6
        y0 = -0.45
        up = Rectangle(width=L, height=2.9, stroke_width=0, fill_color=BLUE_E, fill_opacity=0.15).move_to([cx, y0 + 1.45, 0])
        dn = Rectangle(width=L, height=2.9, stroke_width=0, fill_color=TEAL_E, fill_opacity=0.35).move_to([cx, y0 - 1.45, 0])
        iface = Line([cx - L / 2, y0, 0], [cx + L / 2, y0, 0], color=WHITE, stroke_width=3)
        l1 = CT(r"媒质 1：$\varepsilon_1$", 26).move_to([cx - L / 2 + 1.1, 2.15, 0])
        l1.add_to_back(BackgroundRectangle(l1, fill_opacity=0.8, buff=0.06))
        ratio = ValueTracker(1.0)
        def mk_l2():
            m = CT(rf"媒质 2：$\varepsilon_2={ratio.get_value():.2f}\,\varepsilon_1$", 26).move_to([cx - L / 2 + 1.6, -3.05, 0])
            m.add_to_back(BackgroundRectangle(m, fill_opacity=0.8, buff=0.06))
            return m

        l2 = always_redraw(mk_l2)
        self.play(FadeIn(up), FadeIn(dn), Create(iface), FadeIn(l1), FadeIn(l2))
        th1 = 40 * DEGREES

        def th2():
            return np.arctan(ratio.get_value() * np.tan(th1))

        xl, xr = cx - L / 2, cx + L / 2

        def clip(a, b):
            d = b - a
            t0, t1 = 0.0, 1.0
            if abs(d[0]) > 1e-9:
                ta, tb = (xl - a[0]) / d[0], (xr - a[0]) / d[0]
                t0 = max(t0, min(ta, tb))
                t1 = min(t1, max(ta, tb))
            elif not (xl <= a[0] <= xr):
                return None
            if t1 <= t0:
                return None
            return Line(a + t0 * d, a + t1 * d, color=C_E, stroke_width=2.5)

        def dlines():
            g = VGroup()
            t2 = th2()
            for k in range(-8, 9):
                b = np.array([cx + 0.75 * k, y0, 0])
                a = b + 2.8 * np.array([-np.tan(th1), 1, 0])
                c = b + 2.7 * np.array([np.tan(t2), -1, 0])
                for seg in (clip(a, b), clip(b, c)):
                    if seg is not None:
                        g.add(seg)
            return g

        lines = always_redraw(dlines)
        self.play(FadeIn(lines))
        self.bring_to_front(l1, l2)
        P = np.array([cx + 0.75, y0, 0])
        nrm = DashedLine(P + UP * 2.4, P + DOWN * 2.4, color=GREY_B)

        def angle_marks():
            t2 = th2()
            a1 = Arc(radius=0.9, start_angle=PI / 2, angle=th1, arc_center=P, color=C_HL)
            a2 = Arc(radius=0.9, start_angle=-PI / 2, angle=t2, arc_center=P, color=C_HL)
            t1l = MT(r"\theta_1", 26, C_HL).move_to(P + 1.2 * np.array([-np.sin(th1 / 2), np.cos(th1 / 2), 0]))
            t2l = MT(r"\theta_2", 26, C_HL).move_to(P + 1.25 * np.array([np.sin(t2 / 2), -np.cos(t2 / 2), 0]))
            return VGroup(a1, a2, t1l, t2l)

        am = always_redraw(angle_marks)
        self.play(Create(nrm), FadeIn(am))

        def readout():
            t2 = th2()
            return VGroup(
                MT(rf"\theta_1={np.degrees(th1):.1f}^\circ", 30),
                MT(rf"\theta_2={np.degrees(t2):.1f}^\circ", 30, C_HL),
                MT(rf"\frac{{\tan\theta_1}}{{\tan\theta_2}}={np.tan(th1) / np.tan(t2):.3f}=\frac{{\varepsilon_1}}{{\varepsilon_2}}", 30),
                MT(rf"\frac{{E_2}}{{E_1}}=\frac{{\sin\theta_1}}{{\sin\theta_2}}={np.sin(th1) / np.sin(t2):.3f}", 30, C_E),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(RIGHT * 4.3 + UP * 0.9)

        ro = always_redraw(readout)
        self.play(FadeIn(ro))
        self.play(ratio.animate.set_value(4.0), run_time=3)
        self.wait(0.6)
        self.play(ratio.animate.set_value(0.25), run_time=3.5)
        self.wait(0.6)
        self.play(ratio.animate.set_value(2.0), run_time=2)
        notes = VGroup(
            CT(r"黄线画的是 $\vv D$ 线：法向分量连续，在分界面上不中断", 22),
            CT(r"$\varepsilon_2>\varepsilon_1$：进入高介电常数媒质后偏离法线", 22),
            CT(r"导体表面（$E_t=0$）：电力线垂直于导体表面", 22, C_HL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(RIGHT * 4.1 + DOWN * 2.1)
        fitw(notes, 5.6)
        self.play(FadeIn(notes))
        self.wait(3)
