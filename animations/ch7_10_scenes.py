"""第 7 章 传输线 —— manim 动画源码（LaTeX 排版）。第 10 章场景已移至 ch10_scenes.py.

坐标约定与教材一致：传输线上的 z 从负载（z=0）指向电源，画面上负载在右端。
"""
import numpy as np

from common import *  # noqa: F401,F403
from fieldtools import fitw

C_U = YELLOW      # 电压
C_I = TEAL        # 电流
C_INC = GOLD    # 入射波
C_REF = BLUE_C    # 反射波
C_R = ORANGE      # 等电阻圆
C_X = TEAL_B      # 等电抗圆


def poly(points, color=WHITE, sw=3, opacity=1.0):
    m = VMobject(stroke_color=color, stroke_width=sw, stroke_opacity=opacity)
    m.set_points_as_corners(points)
    return m


def tline(x0, x1, y, gap=0.28, color=GREY_B, sw=4):
    """平行双线示意."""
    return VGroup(Line([x0, y + gap / 2, 0], [x1, y + gap / 2, 0], color=color, stroke_width=sw),
                  Line([x0, y - gap / 2, 0], [x1, y - gap / 2, 0], color=color, stroke_width=sw))


def load_box(x, y, gap=0.28, label="Z_L", color=C_HL, short=False):
    if short:
        b = Line([x, y + gap / 2, 0], [x, y - gap / 2, 0], color=color, stroke_width=6)
        return VGroup(b)
    r = Rectangle(width=0.22, height=gap * 1.6, color=color, stroke_width=3, fill_color=BLACK, fill_opacity=1).move_to([x + 0.18, y, 0])
    w1 = Line([x, y + gap / 2, 0], [x + 0.18, y + gap / 2, 0], color=GREY_B, stroke_width=4)
    w2 = Line([x, y - gap / 2, 0], [x + 0.18, y - gap / 2, 0], color=GREY_B, stroke_width=4)
    t = MT(label, 24, color).next_to(r, RIGHT, buff=0.08)
    return VGroup(w1, w2, r, t)


# ---------------------------------------------------------------- Smith chart helpers
def gmap(z):
    return (z - 1) / (z + 1)


def smith_point(c, R, G):
    return np.array([c[0] + R * G.real, c[1] + R * G.imag, 0.0])


def smith_chart(c, R, rs=(0.2, 0.5, 1, 2, 5), xs=(0.2, 0.5, 1, 2, 5), sw=1.6, labels=True, size=18,
                rlab=None, xlab=None):
    """Return VGroup(outer, real axis, r circles, x arcs, labels)."""
    c = np.array(c, dtype=float)
    g = VGroup()
    g.add(Circle(radius=R, color=GREY_A, stroke_width=2.2).move_to(c))
    g.add(Line(c + LEFT * R, c + RIGHT * R, color=GREY_B, stroke_width=1.4))
    th = np.linspace(-np.pi / 2 + 1e-3, np.pi / 2 - 1e-3, 400)
    rc = VGroup()
    for r in rs:
        pts = [smith_point(c, R, gmap(r + 1j * np.tan(t))) for t in th]
        rc.add(poly(pts, C_R, sw, 0.85))
    xc = VGroup()
    ph = np.linspace(0, np.pi / 2 - 1e-3, 300)
    for x in xs:
        for s in (1, -1):
            pts = [smith_point(c, R, gmap(np.tan(p) + 1j * s * x)) for p in ph]
            xc.add(poly(pts, C_X, sw, 0.85))
    g.add(rc, xc)
    lab = VGroup()
    if labels:
        for r in rs:
            p = smith_point(c, R, gmap(complex(r, 0)))
            lab.add(MT(rlab(r) if rlab else f"{r:g}", size, C_R).next_to(p, UP + LEFT * 0.4, buff=0.03))
        for x in xs:
            for s in (1, -1):
                G = gmap(complex(0, s * x))
                p = smith_point(c, R * 1.09, G)
                txt = (xlab(s * x) if xlab else (f"+{x:g}" if s > 0 else f"-{x:g}"))
                lab.add(MT(txt, size - 2, C_X).move_to(p))
    g.add(lab)
    return g


# --------------------------------------------------------------------------
# 7.1–7.2 行波、驻波、行驻波
# --------------------------------------------------------------------------
class C7_Waves(Scene):
    def construct(self):
        title = title_bar(r"传输线上的电压波：入射波 $+$ 反射波，负载决定反射多少（$z$ 从负载指向电源）")
        fitw(title, 13.6)
        self.play(FadeIn(title))
        XL, XS = 4.6, -5.6            # 负载、电源端屏幕横坐标
        lam = (XL - XS) / 1.25          # 屏幕上的一个波长
        ly = 2.25
        line = tline(XS, XL, ly)
        src = VGroup(Circle(radius=0.22, color=GREY_A, stroke_width=3).move_to([XS - 0.35, ly, 0]),
                     MT(r"\sim", 26, GREY_A).move_to([XS - 0.35, ly, 0]))
        Z0l = MT("Z_0", 24, GREY_A).move_to([(XS + XL) / 2, ly + 0.38, 0])
        self.play(Create(line), FadeIn(src), FadeIn(Z0l))
        load = load_box(XL, ly)
        self.play(FadeIn(load))
        # 坐标轴
        yb = -0.55
        su = 1.05                        # 电压单位 → 屏幕
        ax_line = Arrow([XL + 0.1, yb, 0], [XS - 0.3, yb, 0], buff=0, color=GREY_B, stroke_width=2, max_tip_length_to_length_ratio=0.02)
        zl = MT("z", 26, GREY_B).next_to(ax_line.get_end(), DOWN, buff=0.08)
        ticks = VGroup()
        for k, s in [(0, "0"), (0.25, r"\lambda/4"), (0.5, r"\lambda/2"), (0.75, r"3\lambda/4"), (1.0, r"\lambda")]:
            x = XL - k * lam
            ticks.add(Line([x, yb - 0.07, 0], [x, yb + 0.07, 0], color=GREY_B, stroke_width=2),
                      MT(s, 20, GREY_B).move_to([x, yb - 2.05, 0]),
                      DashedLine([x, yb - 1.85, 0], [x, yb + 1.85, 0], color=GREY_D, stroke_width=1, dash_length=0.06))
        self.play(Create(ax_line), FadeIn(zl), FadeIn(ticks))

        t = ValueTracker(0.0)
        gm = ValueTracker(0.0)    # |Γ_L|
        gp = ValueTracker(np.pi)  # φ_L
        show_parts = ValueTracker(0.0)
        zs = np.linspace(0, 1.25, 400)

        def sx(z):
            return XL - z * lam

        def u_inc(z, tt):
            return np.cos(TAU * tt + TAU * z)

        def u_ref(z, tt):
            return gm.get_value() * np.cos(TAU * tt - TAU * z + gp.get_value())

        def env(z):
            G = gm.get_value() * np.exp(1j * (gp.get_value() - 2 * TAU * z))
            return np.abs(1 + G)

        def envI(z):
            G = gm.get_value() * np.exp(1j * (gp.get_value() - 2 * TAU * z))
            return np.abs(1 - G)

        inc = always_redraw(lambda: poly([[sx(z), yb + su * u_inc(z, t.get_value()), 0] for z in zs], C_INC, 2.5, 0.8 * show_parts.get_value()))
        ref = always_redraw(lambda: poly([[sx(z), yb + su * u_ref(z, t.get_value()), 0] for z in zs], C_REF, 2.5, 0.8 * show_parts.get_value()))
        tot = always_redraw(lambda: poly([[sx(z), yb + su * (u_inc(z, t.get_value()) + u_ref(z, t.get_value())), 0] for z in zs], C_U, 4))
        envp = always_redraw(lambda: DashedVMobject(poly([[sx(z), yb + su * env(z), 0] for z in zs], WHITE, 2), num_dashes=70))
        envn = always_redraw(lambda: DashedVMobject(poly([[sx(z), yb - su * env(z), 0] for z in zs], WHITE, 2), num_dashes=70))
        envi = always_redraw(lambda: DashedVMobject(poly([[sx(z), yb + su * envI(z), 0] for z in zs], C_I, 2, 0.9), num_dashes=70))
        self.add(inc, ref, tot)
        leg = VGroup(CT(r"黄色实线：瞬时电压 $u(z,t)$", 22, C_U),
                     CT(r"白色虚线：振幅包络 $\pm|U(z)|$", 22, WHITE),
                     CT(r"青色虚线：电流振幅 $|I(z)|Z_0$", 22, C_I)).arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=0.12)
        fitw(leg, 13.4)
        # ---- 1. 匹配：行波
        cap = CT(r"(1)  $Z_L=Z_0$，$\Gamma_L=0$：只有入射行波，向负载“跑”去，振幅处处相同——\textbf{行波状态}", 24)
        fitw(cap, 13.4).next_to(title, DOWN, buff=0.2)
        self.play(FadeIn(cap), FadeIn(leg))
        self.play(t.animate.set_value(2.5), run_time=5, rate_func=linear)
        self.add(envp, envn, envi)
        self.play(t.animate.set_value(4.0), run_time=3, rate_func=linear)
        # ---- 2. 短路：纯驻波
        short = load_box(XL, ly, short=True)
        cap2 = CT(r"(2)  终端短路 $Z_L=0$，$\Gamma_L=-1$：全反射，入射波（金）与反射波（蓝）叠成\textbf{纯驻波}", 24)
        fitw(cap2, 13.4).move_to(cap)
        self.play(FadeOut(cap), FadeIn(cap2), FadeOut(load), FadeIn(short), show_parts.animate.set_value(1.0),
                  gm.animate.set_value(1.0), t.animate.set_value(5.0), run_time=2, rate_func=linear)
        self.play(t.animate.set_value(9.0), run_time=8, rate_func=linear)
        notes = VGroup(CT(r"电压波节在 $z=0,\ \lambda/2,\cdots$（短路点电压为零）", 22),
                       CT(r"电压波腹 $=$ 电流波节，相距 $\lambda/4$；能量只来回振荡，不传输", 22)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        fitw(notes, 13.0).to_edge(DOWN, buff=0.1)
        self.play(FadeOut(leg), FadeIn(notes), t.animate.set_value(11.0), run_time=4, rate_func=linear)
        self.play(t.animate.set_value(13.0), run_time=3, rate_func=linear)
        self.play(FadeOut(notes), FadeIn(leg), t.animate.set_value(14.0 - 2.0 + 0.0), run_time=1.5, rate_func=linear)
        # ---- 3. 一般负载：行驻波
        load2 = load_box(XL, ly, label=r"Z_L=3Z_0")
        cap3 = CT(r"(3)  $Z_L=3Z_0$，$\Gamma_L=0.5$：部分反射，\textbf{行驻波}——波节不为零，$\rho=\dfrac{|U|_{\max}}{|U|_{\min}}=\dfrac{1+|\Gamma_L|}{1-|\Gamma_L|}=3$", 24)
        fitw(cap3, 13.4).move_to(cap)
        self.play(FadeOut(cap2), FadeIn(cap3), FadeOut(short), FadeIn(load2),
                  gm.animate.set_value(0.5), gp.animate.set_value(0.0), t.animate.set_value(14.5), run_time=2.5, rate_func=linear)
        self.play(t.animate.set_value(19.5), run_time=10, rate_func=linear)
        mx = VGroup(MT(r"|U|_{\max}\propto1+|\Gamma_L|", 22, WHITE).move_to([sx(0.5), yb + su * 1.5 + 0.28, 0]),
                    MT(r"|U|_{\min}\propto1-|\Gamma_L|", 22, WHITE).move_to([sx(0.25), yb - su * 0.5 - 0.6, 0]))
        mxb = VGroup(*[BackgroundRectangle(m, fill_opacity=0.85, buff=0.05) for m in mx])
        self.play(FadeIn(mxb), FadeIn(mx), t.animate.set_value(21.5), run_time=4, rate_func=linear)
        self.wait(1)


# --------------------------------------------------------------------------
# 7.1.4 反射系数在圆上转圈 → 驻波包络、驻波比、波腹波节阻抗
# --------------------------------------------------------------------------
class C7_Gamma(Scene):
    def construct(self):
        title = title_bar(r"$\Gamma(z)=\Gamma_L\mathrm e^{-\mathrm j2\beta z}$：离负载越远，反射系数在圆上顺时针转，$\lambda/2$ 转一圈")
        fitw(title, 13.6)
        self.play(FadeIn(title))
        c = np.array([-3.7, -0.55, 0])
        R = 2.35
        circ = Circle(radius=R, color=GREY_A, stroke_width=2).move_to(c)
        xa = Line(c + LEFT * (R + 0.3), c + RIGHT * (R + 0.3), color=GREY_B, stroke_width=1.5)
        ya = Line(c + DOWN * (R + 0.2), c + UP * (R + 0.2), color=GREY_B, stroke_width=1.5)
        m1 = Dot(c + LEFT * R, color=C_U, radius=0.06)
        p1 = Dot(c + RIGHT * R, color=C_I, radius=0.06)
        l_m1 = MT("-1", 22, C_U).next_to(m1, DOWN + LEFT * 0.3, buff=0.06)
        l_p1 = MT("+1", 22, C_I).next_to(p1, DOWN + RIGHT * 0.3, buff=0.06)
        lab = CT(r"$\Gamma$ 平面（$|\Gamma|\le1$）", 22, GREY_A).next_to(circ, UP, buff=0.12).shift(LEFT * 1.2)
        self.play(Create(circ), Create(xa), Create(ya), FadeIn(m1), FadeIn(p1), FadeIn(l_m1), FadeIn(l_p1), FadeIn(lab))
        gL = 0.5 * np.exp(1j * np.deg2rad(60))
        rho = (1 + abs(gL)) / (1 - abs(gL))
        z = ValueTracker(0.0)

        def G():
            return gL * np.exp(-2j * TAU * z.get_value())

        vsw = DashedVMobject(Circle(radius=R * abs(gL), color=GREY_B, stroke_width=1.5).move_to(c), num_dashes=40)
        gdot = always_redraw(lambda: Dot(smith_point(c, R, G()), color=C_HL, radius=0.08))
        gvec = always_redraw(lambda: Arrow(c, smith_point(c, R, G()), buff=0, color=C_HL, stroke_width=4, max_tip_length_to_length_ratio=0.12))
        glab = always_redraw(lambda: MT(r"\Gamma(z)", 24, C_HL).next_to(smith_point(c, R, G()), UR, buff=0.05))
        uvec = always_redraw(lambda: Line(c + LEFT * R, smith_point(c, R, G()), color=C_U, stroke_width=4))
        ivec = always_redraw(lambda: Line(c + RIGHT * R, smith_point(c, R, G()), color=C_I, stroke_width=4))
        self.play(GrowArrow(gvec), FadeIn(gdot), FadeIn(glab), Create(vsw))
        expl = VGroup(CT(r"$U(z)=A_1\mathrm e^{\mathrm j\beta z}\,[1+\Gamma(z)]$：$|U|\propto$ 黄线长（到 $-1$ 的距离）", 22, C_U),
                      CT(r"$I(z)=\dfrac{A_1}{Z_0}\mathrm e^{\mathrm j\beta z}\,[1-\Gamma(z)]$：$|I|\propto$ 青线长（到 $+1$ 的距离）", 22, C_I))
        expl.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        fitw(expl, 6.6).move_to([3.4, 2.35, 0])
        self.play(Create(uvec), Create(ivec), FadeIn(expl))
        # 右侧包络图
        ax = Axes(x_range=[0, 0.75, 0.25], y_range=[0, 1.6, 0.5], x_length=6.0, y_length=2.6,
                  axis_config={"stroke_width": 1.5, "include_ticks": False, "include_tip": False}).move_to([3.4, -0.35, 0])
        # 让 z 轴向左增长：横轴翻转
        def P(zz, v):
            return ax.c2p(0.75 - zz, v)
        zt = VGroup(*[MT(s, 20, GREY_B).next_to(P(k, 0), DOWN, buff=0.1) for k, s in
                      [(0, "0"), (0.25, r"\lambda/4"), (0.5, r"\lambda/2"), (0.75, r"3\lambda/4")]])
        zarr = CT(r"$\leftarrow z$（向电源）", 20, GREY_B).next_to(P(0.375, 0), DOWN, buff=0.5)
        loadt = CT("负载", 20, GREY_B).next_to(P(0, 0), DOWN, buff=0.5)
        ul = MT(r"|U|/|A_1|", 22, C_U).next_to(ax.y_axis, UP, buff=0.05).shift(RIGHT * 4.4)
        self.play(Create(ax), FadeIn(zt), FadeIn(zarr), FadeIn(loadt))
        curveU = always_redraw(lambda: poly([P(q, abs(1 + gL * np.exp(-2j * TAU * q))) for q in np.linspace(0, max(z.get_value(), 1e-3), 200)], C_U, 3.5))
        curveI = always_redraw(lambda: poly([P(q, abs(1 - gL * np.exp(-2j * TAU * q))) for q in np.linspace(0, max(z.get_value(), 1e-3), 200)], C_I, 3.0))
        mark = always_redraw(lambda: DashedLine(P(z.get_value(), 0), P(z.get_value(), 1.6), color=C_HL, stroke_width=2))
        self.add(curveU, curveI, mark)
        self.play(z.animate.set_value(0.5), run_time=8, rate_func=linear)
        note = CT(r"转一整圈 $\Rightarrow$ 沿线移动 $\lambda/2$：$|\Gamma(z)|$ 不变，只有相位在变", 22).next_to(ax, DOWN, buff=0.55)
        fitw(note, 6.6)
        self.play(FadeOut(zarr), FadeOut(loadt), FadeIn(note))
        self.play(z.animate.set_value(0.75), run_time=4, rate_func=linear)
        self.play(FadeOut(note))
        # 波腹：Γ 落在正实轴（向负载方向移动 → 逆时针）
        curveU.clear_updaters()
        curveI.clear_updaters()
        zm1 = np.deg2rad(60) / (2 * TAU) + 0.5
        self.play(z.animate.set_value(zm1), run_time=2)
        t1 = VGroup(CT(r"$\Gamma$ 落在正实轴：电压波腹、电流波节", 22, C_U),
                    MT(r"z_{\max}=\frac{\phi_L}{4\pi}\lambda+n\frac{\lambda}{2},\quad |U|_{\max}=|A_1|(1+|\Gamma_L|),\quad R_{\max}=Z_0\rho", 26)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        fitw(t1, 6.6).next_to(ax, DOWN, buff=0.5)
        self.play(FadeIn(t1))
        self.wait(2)
        self.play(z.animate.set_value(zm1 - 0.25), run_time=2.5)
        t2 = VGroup(CT(r"再向负载走 $\lambda/4$，$\Gamma$ 逆时针转半圈到负实轴：电压波节", 22, C_I),
                    MT(r"|U|_{\min}=|A_1|(1-|\Gamma_L|),\quad R_{\min}=Z_0/\rho,\quad R_{\max}R_{\min}=Z_0^2", 26)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        fitw(t2, 6.6).move_to(t1)
        self.play(FadeOut(t1), FadeIn(t2))
        self.wait(2)
        t3 = MT(r"\rho=\frac{|U|_{\max}}{|U|_{\min}}=\frac{1+|\Gamma_L|}{1-|\Gamma_L|}=" + f"{rho:.0f}", 32, C_HL)
        t3.move_to(t2).shift(DOWN * 0.95)
        t3b = BackgroundRectangle(t3, fill_opacity=0.85, buff=0.1)
        self.play(FadeIn(t3b), FadeIn(t3))
        self.wait(3)


# --------------------------------------------------------------------------
# 7.2.2 短路线、开路线的输入阻抗：一段线就是电感、电容、谐振器
# --------------------------------------------------------------------------
class C7_Stub(Scene):
    def construct(self):
        title = title_bar(r"无耗短路线 $Z_{\mathrm{in}}=\mathrm jZ_0\tan\beta l$、开路线 $Z_{\mathrm{in}}=-\mathrm jZ_0\cot\beta l$：长度决定它是 $L$ 还是 $C$")
        fitw(title, 13.6)
        self.play(FadeIn(title))
        ax = Axes(x_range=[0, 1, 0.25], y_range=[-4, 4, 1], x_length=7.4, y_length=4.6,
                  axis_config={"stroke_width": 1.5, "include_ticks": False, "include_tip": False}).move_to([-2.9, -0.9, 0])
        xl = MT(r"l", 26, GREY_B).next_to(ax.x_axis, RIGHT, buff=0.1)
        yl = MT(r"X_{\mathrm{in}}/Z_0", 24, GREY_B).next_to(ax.y_axis, UP, buff=0.05)
        ticks = VGroup(*[MT(s, 20, GREY_B).next_to(ax.c2p(k, 0), DOWN + RIGHT * 0.4, buff=0.08) for k, s in
                         [(0.25, r"\frac{\lambda}{4}"), (0.5, r"\frac{\lambda}{2}"), (0.75, r"\frac{3\lambda}{4}"), (1, r"\lambda")]])
        vlines = VGroup(*[DashedLine(ax.c2p(k, -4), ax.c2p(k, 4), color=GREY_D, stroke_width=1.2) for k in (0.25, 0.5, 0.75, 1)])
        # 区域着色
        bands = VGroup()
        for k in range(4):
            col = C_HL if k % 2 == 0 else BLUE_C
            r = Rectangle(width=ax.c2p(0.25, 0)[0] - ax.c2p(0, 0)[0], height=4.6, stroke_width=0, fill_color=col, fill_opacity=0.10)
            r.move_to([(ax.c2p(k * 0.25, 0)[0] + ax.c2p((k + 1) * 0.25, 0)[0]) / 2, ax.c2p(0, 0)[1], 0])
            bands.add(r)
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(ticks), FadeIn(vlines))

        def branch(f, a, b):
            xs = np.linspace(a, b, 600)
            pts = [ax.c2p(x, f(x)) for x in xs if abs(f(x)) <= 4.0]
            return poly(pts, C_U, 3.5)

        tanf = lambda x: np.tan(TAU * x)
        cotf = lambda x: -1 / np.tan(TAU * x)
        eps = 0.012
        shortc = VGroup(*[branch(tanf, a + eps * (a > 0), b - eps) for a, b in [(0, 0.25), (0.25, 0.75), (0.75, 1.0)]])
        # 线的示意（右上）
        x0, y0 = 2.0, 2.0
        lt = ValueTracker(0.05)
        S = 5.6   # 屏幕长度 / λ
        stub = always_redraw(lambda: VGroup(tline(x0, x0 + S * lt.get_value(), y0, gap=0.26),
                                            Line([x0 + S * lt.get_value(), y0 + 0.13, 0], [x0 + S * lt.get_value(), y0 - 0.13, 0], color=C_HL, stroke_width=6)))
        ltxt = always_redraw(lambda: MT(rf"l={lt.get_value():.3f}\,\lambda", 24).next_to([x0 + 2.0, y0 - 0.25, 0], DOWN, buff=0.12))
        stit = CT("终端短路的一段线", 22, C_HL).next_to([x0 + 2.0, y0 + 0.2, 0], UP, buff=0.08)
        self.play(FadeIn(stub), FadeIn(ltxt), FadeIn(stit))
        self.play(FadeIn(bands), Create(shortc), run_time=2)
        dot = always_redraw(lambda: Dot(ax.c2p(lt.get_value(), np.clip(tanf(lt.get_value()), -4, 4)), color=WHITE, radius=0.07))
        self.add(dot)
        # 区域文字
        info = VGroup(
            CT(r"$0<l<\lambda/4$：$X>0$，\textbf{等效电感}", 22, C_HL),
            CT(r"$l=\lambda/4$：$|Z_{\mathrm{in}}|\to\infty$，并联谐振（相当于开路）", 22),
            CT(r"$\lambda/4<l<\lambda/2$：$X<0$，\textbf{等效电容}", 22, BLUE_B),
            CT(r"$l=\lambda/2$：$Z_{\mathrm{in}}=0$，串联谐振（相当于短路）", 22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        fitw(info, 5.6).move_to([4.0, -0.2, 0])
        self.play(lt.animate.set_value(0.2), FadeIn(info[0]), run_time=2.5, rate_func=linear)
        self.play(lt.animate.set_value(0.25 - 0.006), FadeIn(info[1]), run_time=1.5, rate_func=linear)
        self.play(lt.animate.set_value(0.25 + 0.006), run_time=0.3)
        self.play(lt.animate.set_value(0.45), FadeIn(info[2]), run_time=2.5, rate_func=linear)
        self.play(lt.animate.set_value(0.5), FadeIn(info[3]), run_time=1.0, rate_func=linear)
        self.play(lt.animate.set_value(0.74), run_time=2.5, rate_func=linear)
        rep = CT(r"每隔 $\lambda/2$ 重复（$\lambda/2$ 重复性）", 22, GREY_A).next_to(info, DOWN, buff=0.25)
        fitw(rep, 5.6)
        self.play(FadeIn(rep))
        self.wait(1)
        # 开路线
        openc = VGroup(*[branch(cotf, a + eps, b - eps) for a, b in [(0, 0.5), (0.5, 1.0)]]).set_color(C_I)
        o_lab = CT(r"开路线 $-\cot\beta l$ = 短路线曲线\textbf{平移} $\lambda/4$", 22, C_I)
        fitw(o_lab, 5.6).next_to(rep, DOWN, buff=0.25)
        self.play(Create(openc), FadeIn(o_lab), run_time=2)
        o2 = CT(r"$l<\lambda/4$ 的开路线是电容：$\lambda/4$ 线把“开路”变成“短路”", 22, C_I)
        fitw(o2, 5.6).next_to(o_lab, DOWN, buff=0.15)
        self.play(FadeIn(o2))
        self.wait(3)


# --------------------------------------------------------------------------
# 7.3 史密斯圆图：分式线性映射 Γ=(z−1)/(z+1)
# --------------------------------------------------------------------------
class C7_Smith(Scene):
    def construct(self):
        title = title_bar(r"史密斯圆图 $=$ 分式线性映射 $\Gamma=\dfrac{\bar Z-1}{\bar Z+1}$：把右半 $\bar Z$ 平面（$r\ge0$）映成单位圆盘")
        fitw(title, 13.6)
        self.play(FadeIn(title))
        # 左：归一化阻抗平面
        zc = np.array([-6.3, -0.7, 0])  # r=0, x=0 对应的屏幕点
        s = 0.95
        def ZP(z):
            return np.array([zc[0] + s * z.real, zc[1] + s * z.imag, 0.0])
        xa = Arrow(ZP(-0.2 + 0j), ZP(4.6 + 0j), buff=0, color=GREY_B, stroke_width=2, max_tip_length_to_length_ratio=0.03)
        ya = Arrow(ZP(-2.75j), ZP(2.75j), buff=0, color=GREY_B, stroke_width=2, max_tip_length_to_length_ratio=0.03)
        rl = MT("r", 24, GREY_B).next_to(xa.get_end(), DOWN, buff=0.05)
        xl = MT("x", 24, GREY_B).next_to(ya.get_end(), RIGHT, buff=0.05)
        ztit = CT(r"归一化阻抗 $\bar Z=r+\mathrm jx$", 22).move_to(ZP(2.2 + 3.15j))
        self.play(Create(xa), Create(ya), FadeIn(rl), FadeIn(xl), FadeIn(ztit))
        rs = (0, 0.2, 0.5, 1, 2, 5)
        xs = (0.2, 0.5, 1, 2)
        Xm, Rm = 2.6, 4.4
        tz = np.linspace(-Xm, Xm, 260)
        tr = np.linspace(0, Rm, 260)
        zr_lines, gr_lines, zx_lines, gx_lines = VGroup(), VGroup(), VGroup(), VGroup()
        c = np.array([3.3, -0.7, 0])
        R = 2.6
        for r in rs:
            if r > Rm:
                continue
            zr_lines.add(poly([ZP(r + 1j * x) for x in tz], C_R, 2.4))
            gr_lines.add(poly([smith_point(c, R, gmap(r + 1j * x)) for x in tz], C_R, 2.4))
        for x in xs:
            for sg in (1, -1):
                zx_lines.add(poly([ZP(q + 1j * sg * x) for q in tr], C_X, 2.4))
                gx_lines.add(poly([smith_point(c, R, gmap(q + 1j * sg * x)) for q in tr], C_X, 2.4))
        zr_lab = VGroup(*[MT(f"r={r:g}", 18, C_R).next_to(ZP(r + 2.6j), UP, buff=0.04) for r in (1, 2, 5) if r <= Rm])
        self.play(Create(zr_lines), Create(zx_lines), FadeIn(zr_lab), run_time=2)
        note = CT(r"等电阻线（竖线）与等电抗线（横线）", 22).move_to(ZP(2.2 - 3.05j))
        self.play(FadeIn(note))
        uc = Circle(radius=R, color=GREY_A, stroke_width=2.2).move_to(c)
        gtit = CT(r"反射系数平面 $\Gamma=\Gamma_u+\mathrm j\Gamma_v$", 22).move_to(c + UP * (R + 0.45))
        self.play(Create(uc), FadeIn(gtit))
        self.play(TransformFromCopy(zr_lines, gr_lines), TransformFromCopy(zx_lines, gx_lines), run_time=4)
        txt = CT(r"分式线性映射保圆：直线 $\to$ 圆。$r$ 线 $\to$ 等电阻圆，$x$ 线 $\to$ 等电抗圆弧", 22)
        fitw(txt, 13).to_edge(DOWN, buff=0.12)
        self.play(FadeOut(note), FadeIn(txt))
        self.wait(1.5)
        # 特殊点
        pts = [(0j, r"\bar Z=0", "短路", C_U, -1 + 0j), (1 + 0j, r"\bar Z=1", "匹配", WHITE, 0j)]
        anims = []
        for z, zl_, name, col, G in pts:
            d1 = Dot(ZP(z), color=col, radius=0.08)
            d2 = Dot(smith_point(c, R, G), color=col, radius=0.08)
            l2 = CT(name, 20, col).next_to(d2, DOWN, buff=0.08)
            anims += [FadeIn(d1), FadeIn(d2), FadeIn(l2)]
        dinf = Dot(smith_point(c, R, 1 + 0j), color=C_I, radius=0.08)
        linf = CT(r"$\bar Z=\infty$ 开路", 20, C_I).next_to(dinf, UP, buff=0.12).shift(LEFT * 0.3)
        up = CT(r"上半圆：$x>0$ 感性", 20, C_X).move_to(c + UP * 1.75 + LEFT * 0.3)
        dn = CT(r"下半圆：$x<0$ 容性", 20, C_X).move_to(c + DOWN * 1.75 + LEFT * 0.3)
        up.add_to_back(BackgroundRectangle(up, fill_opacity=0.85, buff=0.05))
        dn.add_to_back(BackgroundRectangle(dn, fill_opacity=0.85, buff=0.05))
        linf.add_to_back(BackgroundRectangle(linf, fill_opacity=0.85, buff=0.04))
        self.play(*anims, FadeIn(dinf), FadeIn(linf), FadeIn(up), FadeIn(dn))
        self.wait(2.5)
        # ---- 第二部分：圆图上走线（例 7-1）
        left = VGroup(xa, ya, rl, xl, ztit, zr_lines, zx_lines, zr_lab, note)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not title])
        c = np.array([-3.0, -0.55, 0])
        R = 2.85
        chart = smith_chart(c, R, rs=(0.2, 0.5, 1, 2, 5), xs=(0.2, 0.5, 1, 2, 5))
        self.play(FadeIn(chart))
        zL = 0.5 + 0.5j
        gL = gmap(zL)
        P1 = smith_point(c, R, gL)
        d1 = Dot(P1, color=C_HL, radius=0.09)
        l1 = MT("P_1", 24, C_HL).next_to(d1, UL, buff=0.04)
        steps = VGroup(
            CT(r"例 7-1：$Z_0=50\ \Omega$，$Z_L=(25+\mathrm j25)\ \Omega$，求 $z=0.2\lambda$ 处的阻抗", 22),
            CT(r"(1)  归一化 $\bar Z_L=0.5+\mathrm j0.5$：$r=0.5$ 圆与 $x=0.5$ 圆的交点 $P_1$", 22),
            CT(r"(2)  以 $|\Gamma_L|=" + f"{abs(gL):.3f}" + r"$ 为半径画等 $\rho$ 圆", 22),
            CT(r"(3)  向电源 $0.2\lambda$：顺时针转 $2\beta z=0.8\pi=144^\circ$ 到 $P_2$", 22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        fitw(steps, 6.3).move_to([3.65, 1.4, 0])
        self.play(FadeIn(steps[0]))
        self.play(FadeIn(steps[1]), FadeIn(d1), FadeIn(l1))
        rc = DashedVMobject(Circle(radius=R * abs(gL), color=WHITE, stroke_width=2).move_to(c), num_dashes=60)
        self.play(FadeIn(steps[2]), Create(rc))
        zt = ValueTracker(0.0)
        mv = always_redraw(lambda: Dot(smith_point(c, R, gL * np.exp(-2j * TAU * zt.get_value())), color=C_U, radius=0.08))
        arc = always_redraw(lambda: poly([smith_point(c, R, gL * np.exp(-2j * TAU * q)) for q in np.linspace(0, max(zt.get_value(), 1e-4), 120)], C_U, 5))
        self.add(arc, mv)
        self.play(FadeIn(steps[3]), zt.animate.set_value(0.2), run_time=3.5)
        z2 = (1 + gL * np.exp(-2j * TAU * 0.2)) / (1 - gL * np.exp(-2j * TAU * 0.2))
        l2 = MT("P_2", 24, C_U).next_to(smith_point(c, R, gL * np.exp(-2j * TAU * 0.2)), DR, buff=0.04)
        res = VGroup(CT(r"(4)  读出 $\bar Z_{\mathrm{in}}\approx" + f"{z2.real:.2f}-\\mathrm j{-z2.imag:.2f}" + r"$，乘 $Z_0$：", 22),
                     MT(r"Z_{\mathrm{in}}(0.2\lambda)\approx(98.5-\mathrm j50.7)\ \Omega", 28, C_U)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        fitw(res, 6.6).next_to(steps, DOWN, aligned_edge=LEFT, buff=0.3)
        self.play(FadeIn(l2), FadeIn(res))
        self.wait(1.5)
        rho = (1 + abs(gL)) / (1 - abs(gL))
        pr = Dot(smith_point(c, R, complex(abs(gL), 0)), color=C_HL, radius=0.07)
        tip = VGroup(CT(r"等 $\rho$ 圆与正实轴交点的 $r$ 值就是驻波比：$\rho=" + f"{rho:.2f}" + r"$", 22, C_HL),
                     CT(r"规则：向电源顺时针、向负载逆时针；转一圈 $=\lambda/2$", 22, GREY_A),
                     CT(r"整张图旋转 $180^\circ$（$\Gamma\to-\Gamma$）就变成导纳圆图", 22, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        fitw(tip, 6.6).next_to(res, DOWN, aligned_edge=LEFT, buff=0.3)
        self.play(FadeIn(pr), FadeIn(tip[0]))
        self.play(FadeIn(tip[1]))
        self.play(FadeIn(tip[2]))
        self.wait(3)


# --------------------------------------------------------------------------
# 7.7 阻抗匹配：λ/4 变换器的带宽 + 单支节匹配（导纳圆图）
# --------------------------------------------------------------------------
class C7_Match(Scene):
    def construct(self):
        title = title_bar(r"阻抗匹配：$\lambda/4$ 阻抗变换器（只在中心频率完全匹配）与短路支节匹配")
        fitw(title, 13.6)
        self.play(FadeIn(title))
        # ---------------- Part 1: λ/4 变换器
        y0 = 2.0
        l1 = tline(-6.4, -3.6, y0)
        l2 = tline(-3.6, -1.2, y0, gap=0.5, color=C_HL)
        ld = load_box(-1.2, y0, gap=0.5, label=r"R_L=100\,\Omega")
        t1 = MT(r"Z_0=50\,\Omega", 22, GREY_A).next_to(l1, UP, buff=0.12)
        t2 = MT(r"Z_{01}=\sqrt{Z_0R_L}=70.7\,\Omega", 22, C_HL).next_to(l2, UP, buff=0.12)
        t3 = MT(r"\lambda_0/4", 22, C_HL).next_to(l2, DOWN, buff=0.12)
        self.play(Create(l1), Create(l2), FadeIn(ld), FadeIn(t1), FadeIn(t2), FadeIn(t3))
        eq = MT(r"Z_{\mathrm{in}}=\frac{Z_{01}^2}{R_L}=Z_0\ \ (f=f_0)", 30).move_to([3.9, 2.0, 0])
        self.play(FadeIn(eq))
        ax = Axes(x_range=[0, 2, 0.5], y_range=[0, 0.4, 0.1], x_length=8.5, y_length=3.6,
                  axis_config={"stroke_width": 1.5, "include_ticks": False, "include_tip": False}).move_to([-1.6, -1.2, 0])
        xl = MT(r"f/f_0", 24, GREY_B).next_to(ax.x_axis, RIGHT, buff=0.1)
        yl = MT(r"|\Gamma_{\mathrm{in}}|", 24, GREY_B).next_to(ax.y_axis, UP, buff=0.05)
        tk = VGroup(*[MT(s, 20, GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.08) for v, s in [(0.5, "0.5"), (1, "1"), (1.5, "1.5"), (2, "2")]],
                    *[MT(s, 20, GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.08) for v, s in [(0.1, "0.1"), (0.2, "0.2"), (0.3, "0.3")]])
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(tk))
        Z0, RL = 50.0, 100.0

        def g1(x):
            t = np.tan(np.pi / 2 * x)
            Z1 = np.sqrt(Z0 * RL)
            Zi = Z1 * (RL + 1j * Z1 * t) / (Z1 + 1j * RL * t)
            return abs((Zi - Z0) / (Zi + Z0))

        def g2(x):
            t = np.tan(np.pi / 2 * x)
            Za, Zb = Z0 * 2 ** 0.25, Z0 * 2 ** 0.75
            Zi = Zb * (RL + 1j * Zb * t) / (Zb + 1j * RL * t)
            Zi = Za * (Zi + 1j * Za * t) / (Za + 1j * Zi * t)
            return abs((Zi - Z0) / (Zi + Z0))

        xs = np.linspace(0.001, 1.999, 500)
        c1 = poly([ax.c2p(x, g1(x)) for x in xs], C_HL, 3.5)
        tol = DashedLine(ax.c2p(0, 0.1), ax.c2p(2, 0.1), color=GREY_B, stroke_width=1.5)
        toll = CT(r"容许 $|\Gamma|\le0.1$（$\rho\le1.22$）", 20, GREY_B).next_to(ax.c2p(2, 0.1), UP, buff=0.05).shift(LEFT * 1.0)
        self.play(Create(c1), run_time=2.5)
        self.play(Create(tol), FadeIn(toll))
        band1 = Line(ax.c2p(0.817, 0.0), ax.c2p(1.183, 0.0), color=C_HL, stroke_width=10)
        b1t = CT(r"单节：相对带宽约 $37\%$", 22, C_HL).move_to([4.5, -0.2, 0]).align_to(np.array([3.05, 0, 0]), LEFT)
        self.play(Create(band1), FadeIn(b1t))
        why = VGroup(CT(r"偏离 $f_0$ 时，线长不再是 $\lambda/4$，", 22),
                     CT(r"$Z_{01}^2/R_L$ 的变换不成立：\textbf{窄带}", 22)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        fitw(why, 3.9).next_to(b1t, DOWN, aligned_edge=LEFT, buff=0.25)
        self.play(FadeIn(why))
        c2 = poly([ax.c2p(x, g2(x)) for x in xs], C_I, 3.5)
        band2 = Line(ax.c2p(0.643, 0.012), ax.c2p(1.357, 0.012), color=C_I, stroke_width=10)
        b2t = VGroup(CT(r"两节阶梯（$59.5\ \Omega$、$84.1\ \Omega$）：", 22, C_I),
                     CT(r"相对带宽约 $71\%$——多阶梯展宽频带", 22, C_I)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        fitw(b2t, 3.9).next_to(why, DOWN, aligned_edge=LEFT, buff=0.3)
        self.play(Create(c2), Create(band2), FadeIn(b2t), run_time=2.5)
        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not title])
        # ---------------- Part 2: 单支节匹配（导纳圆图）
        c = np.array([-3.0, -0.55, 0])
        R = 2.85
        chart = smith_chart(c, R, rs=(0.2, 0.5, 1, 2, 5), xs=(0.2, 0.5, 1, 2, 5))
        g1c = Circle(radius=R / 2, color=C_HL, stroke_width=4).move_to(c + RIGHT * R / 2)
        ctit = CT(r"导纳圆图（坐标读作 $\bar Y=g+\mathrm jb$）", 22).next_to(chart, UP, buff=0.05)
        self.play(FadeIn(chart), FadeIn(ctit))
        zL = 2 + 1j
        yL = 1 / zL
        W = lambda y: (y - 1) / (y + 1)   # 导纳圆图上的位置
        steps = VGroup(
            CT(r"例：$\bar Z_L=2+\mathrm j1$，在主线上并联一段短路支节匹配", 22),
            CT(r"(1)  $\bar Y_L=1/\bar Z_L=0.4-\mathrm j0.2$（阻抗点转 $180^\circ$）", 22),
            CT(r"(2)  向电源顺时针沿等 $\rho$ 圆走 $d$，碰到 $g=1$ 圆（橙色粗圆）", 22),
            CT(r"(3)  此处 $\bar Y=1+\mathrm j1$，支节提供 $-\mathrm j1$ 抵消电纳", 22),
            CT(r"(4)  短路支节 $\bar Y_s=-\mathrm j\cot\beta l=-\mathrm j1\Rightarrow l=\lambda/8$", 22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        fitw(steps, 6.6).move_to([3.75, 1.0, 0])
        self.play(FadeIn(steps[0]))
        pz = Dot(smith_point(c, R, gmap(zL)), color=GREY_A, radius=0.07)
        pzl = MT(r"\bar Z_L", 22, GREY_A).next_to(pz, UR, buff=0.04)
        self.play(FadeIn(pz), FadeIn(pzl))
        py = Dot(smith_point(c, R, W(yL)), color=C_U, radius=0.09)
        pyl = MT(r"\bar Y_L", 22, C_U).next_to(py, DL, buff=0.04)
        dia = DashedLine(pz.get_center(), py.get_center(), color=GREY_B, stroke_width=1.5)
        self.play(FadeIn(steps[1]), Create(dia), FadeIn(py), FadeIn(pyl))
        rc = DashedVMobject(Circle(radius=R * abs(W(yL)), color=WHITE, stroke_width=2).move_to(c), num_dashes=60)
        self.play(FadeIn(steps[2]), Create(rc), Create(g1c))
        dd = 0.19879
        zt = ValueTracker(0.0)
        arc = always_redraw(lambda: poly([smith_point(c, R, W(yL) * np.exp(-2j * TAU * q)) for q in np.linspace(0, max(zt.get_value(), 1e-4), 120)], C_U, 5))
        mv = always_redraw(lambda: Dot(smith_point(c, R, W(yL) * np.exp(-2j * TAU * zt.get_value())), color=C_U, radius=0.08))
        self.add(arc, mv)
        self.play(zt.animate.set_value(dd), run_time=3)
        dl = MT(r"d\approx0.199\lambda", 22, C_U).next_to(mv, UP, buff=0.08)
        self.play(FadeIn(dl), FadeIn(steps[3]))
        # 沿 g=1 圆移到圆心
        A = W(yL) * np.exp(-2j * TAU * dd)
        bt = ValueTracker(1.0)
        arc2 = always_redraw(lambda: poly([smith_point(c, R, W(1 + 1j * b)) for b in np.linspace(1.0, max(bt.get_value(), 1e-3), 80)], C_HL, 5))
        mv2 = always_redraw(lambda: Dot(smith_point(c, R, W(1 + 1j * bt.get_value())), color=C_HL, radius=0.08))
        self.add(arc2, mv2)
        self.play(bt.animate.set_value(0.0), run_time=2.5)
        ok = CT(r"到达圆心 $\bar Y=1$：匹配！", 24, C_HL).next_to(c, DOWN, buff=0.25)
        okb = BackgroundRectangle(ok, fill_opacity=0.85, buff=0.06)
        self.play(FadeIn(okb), FadeIn(ok), FadeIn(steps[4]))
        alt = CT(r"另一解：$d\approx0.375\lambda$ 处 $\bar Y=1-\mathrm j1$，支节 $l=3\lambda/8$", 22, GREY_A)
        fitw(alt, 6.6).next_to(steps, DOWN, aligned_edge=LEFT, buff=0.3)
        self.play(FadeIn(alt))
        self.wait(3)
