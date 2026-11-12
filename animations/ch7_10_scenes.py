"""第 7 章 传输线 / 第 10 章 无线信道、电磁干扰与电磁兼容 —— manim 动画源码（LaTeX 排版）.

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


# ==========================================================================
# 第 10 章
# ==========================================================================
# --------------------------------------------------------------------------
# 10.3.3 视距信道的直射波 + 地面反射波：路径因子 |F|
# --------------------------------------------------------------------------
class C10_TwoRay(Scene):
    def construct(self):
        title = title_bar(r"视距传播：直射波 $+$ 地面反射波（$R\approx-1$），路径因子 $|F|=2\left|\sin\dfrac{2\pi h_1h_2}{\lambda d}\right|$")
        fitw(title, 13.6)
        self.play(FadeIn(title))
        lam, h1, h2 = 1.0, 40.0, 40.0            # m
        gy = 0.55
        X0 = -6.2
        sxk = 1.2                                # 屏幕 / km
        hs = 0.022                               # 屏幕 / m（高度放大显示）
        ground = VGroup(Line([X0 - 0.4, gy, 0], [6.9, gy, 0], color=GREY_A, stroke_width=3),
                        *[Line([x, gy, 0], [x - 0.18, gy - 0.18, 0], color=GREY_C, stroke_width=1.5) for x in np.arange(X0 - 0.2, 6.9, 0.3)])
        T = np.array([X0, gy + h1 * hs, 0])
        tx = VGroup(Line([X0, gy, 0], T, color=C_HL, stroke_width=4), Dot(T, color=C_HL, radius=0.07))
        txl = MT("h_1", 22, C_HL).next_to(tx, LEFT, buff=0.08)
        img = DashedLine([X0, gy, 0], [X0, gy - h1 * hs, 0], color=GREY_B, stroke_width=2)
        imgl = CT("镜像", 18, GREY_B).next_to(img, LEFT, buff=0.08)
        self.play(Create(ground), FadeIn(tx), FadeIn(txl))
        d = ValueTracker(1.2)

        def Rp():
            return np.array([X0 + sxk * d.get_value(), gy + h2 * hs, 0])

        rx = always_redraw(lambda: VGroup(Line([Rp()[0], gy, 0], Rp(), color=C_I, stroke_width=4), Dot(Rp(), color=C_I, radius=0.07),
                                          MT("h_2", 22, C_I).next_to(Rp(), RIGHT, buff=0.08)))
        direct = always_redraw(lambda: Line(T, Rp(), color=C_E, stroke_width=3))

        def refl_pt():
            x = X0 + sxk * d.get_value() * h1 / (h1 + h2)
            return np.array([x, gy, 0])

        reflected = always_redraw(lambda: VGroup(Line(T, refl_pt(), color=C_REF, stroke_width=3), Line(refl_pt(), Rp(), color=C_REF, stroke_width=3)))
        imgray = always_redraw(lambda: DashedLine(refl_pt(), [X0, gy - h1 * hs, 0], color=GREY_B, stroke_width=1.5))
        self.play(FadeIn(rx), Create(direct), Create(reflected))
        self.play(Create(img), FadeIn(imgl), Create(imgray))
        lg = VGroup(CT(r"直射波 $r$", 20, C_E), CT(r"反射波 $r'$（相当于来自镜像天线）", 20, C_REF)).arrange(RIGHT, buff=0.4)
        lg.move_to([0.5, gy + 1.45, 0])
        dr = MT(r"r'-r\approx\frac{2h_1h_2}{d}", 26).move_to([-3.2, gy + 1.45, 0])
        self.play(FadeIn(lg), FadeIn(dr))
        # 下方 |F|(d)
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 2, 1], x_length=10.2, y_length=2.4,
                  axis_config={"stroke_width": 1.5, "include_ticks": False, "include_tip": False}).move_to([-1.0, -2.25, 0])
        xl = CT(r"$d$/km", 20, GREY_B).next_to(ax.x_axis, RIGHT, buff=0.1)
        yl = MT(r"|F|", 24, GREY_B).next_to(ax.y_axis, UP, buff=0.05)
        tks = VGroup(*[MT(str(k), 18, GREY_B).next_to(ax.c2p(k, 0), DOWN, buff=0.06) for k in (2, 4, 6, 8, 10)],
                     *[MT(str(k), 18, GREY_B).next_to(ax.c2p(0, k), LEFT, buff=0.06) for k in (1, 2)])
        one = DashedLine(ax.c2p(0, 1), ax.c2p(10, 1), color=GREY_D, stroke_width=1.2)
        onel = CT("自由空间", 16, GREY_C).next_to(ax.c2p(10, 1), UP, buff=0.04).shift(LEFT * 0.4)
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(tks), Create(one), FadeIn(onel))

        def F(dkm):
            return 2 * abs(np.sin(2 * np.pi * h1 * h2 / (lam * dkm * 1000)))

        curve = always_redraw(lambda: poly([ax.c2p(q, F(q)) for q in np.linspace(0.3, max(d.get_value(), 0.31), int(80 + 260 * (d.get_value() / 10)) + 400)], C_U, 3))
        # 相量图
        pc = np.array([5.6, -2.0, 0])
        ps = 0.55
        ph = lambda: 4 * np.pi * h1 * h2 / (lam * d.get_value() * 1000)   # kΔr
        v1 = Arrow(pc, pc + RIGHT * ps * 1.0, buff=0, color=C_E, stroke_width=4, max_tip_length_to_length_ratio=0.25)
        v2 = always_redraw(lambda: Arrow(pc + RIGHT * ps, pc + RIGHT * ps + ps * np.array([-np.cos(ph()), np.sin(ph()), 0]), buff=0,
                                         color=C_REF, stroke_width=4, max_tip_length_to_length_ratio=0.25))
        vs = always_redraw(lambda: Arrow(pc, pc + RIGHT * ps + ps * np.array([-np.cos(ph()), np.sin(ph()), 0]), buff=0,
                                         color=C_U, stroke_width=5, max_tip_length_to_length_ratio=0.2))
        ptit = CT(r"相量：$1+R\,\mathrm e^{-\mathrm jk(r'-r)}$", 18).move_to(pc + UP * 1.35)
        pcirc = Circle(radius=ps, color=GREY_D, stroke_width=1).move_to(pc + RIGHT * ps)
        dlab = always_redraw(lambda: MT(rf"d={d.get_value():.1f}\ \mathrm{{km}}", 22).move_to(pc + DOWN * 1.05))
        self.play(FadeIn(ptit), Create(pcirc), GrowArrow(v1), FadeIn(v2), FadeIn(vs), FadeIn(dlab))
        self.add(curve)
        cap = CT(r"$h_1=h_2=40\lambda$，$\lambda=1$ m：$d$ 增大时两路程差减小，合成场强起伏（干涉）", 22).next_to(title, DOWN, buff=0.15)
        fitw(cap, 13)
        self.play(FadeIn(cap))
        self.play(d.animate.set_value(3.2), run_time=6, rate_func=linear)
        n1 = CT(r"程差 $=\lambda/2$ 的奇数倍$\pm$：反相相消（考虑 $R=-1$ 后为同相相加）", 20)
        self.play(d.animate.set_value(6.4), run_time=4, rate_func=linear)
        mx = CT(r"最后一个极大：$\dfrac{2\pi h_1h_2}{\lambda d}=\dfrac\pi2\Rightarrow d=\dfrac{4h_1h_2}{\lambda}=6.4$ km", 20, C_HL)
        mx.next_to(ax.c2p(6.4, 2), UP, buff=0.05).shift(LEFT * 0.6)
        mxb = BackgroundRectangle(mx, fill_opacity=0.85, buff=0.05)
        self.play(FadeIn(mxb), FadeIn(mx))
        self.play(d.animate.set_value(10.0), run_time=4, rate_func=linear)
        far = CT(r"更远处 $|F|\approx\dfrac{4\pi h_1h_2}{\lambda d}$：场强 $\propto1/d^2$，功率 $\propto1/d^4$（比自由空间的 $1/d^2$ 衰减得快）", 22, C_HL)
        fitw(far, 13).move_to(cap)
        self.play(FadeOut(cap), FadeIn(far))
        self.wait(3)


# --------------------------------------------------------------------------
# 10.4 电离层的连续折射：最高可用频率与天波静区
# --------------------------------------------------------------------------
def iono_ray(th0, f, hm=300.0, ym=100.0, fc=8.0, ds=2.0, hmax=470.0, xmax=1900.0):
    def dn2(h):
        if abs(h - hm) >= ym:
            return 0.0
        return 2 * (fc / f) ** 2 * (h - hm) / ym ** 2
    th = np.radians(th0)
    x, h = 0.0, 0.0
    kx, kh = np.sin(th), np.cos(th)
    pts = [(x, h)]
    for _ in range(6000):
        k1 = np.array([kx, kh, 0.5 * dn2(h)])
        s2 = np.array([x, h, kh]) + ds / 2 * k1
        k2 = np.array([kx, s2[2], 0.5 * dn2(s2[1])])
        x, h, kh = np.array([x, h, kh]) + ds * k2
        pts.append((x, h))
        if h < 0 or h > hmax or x > xmax:
            break
    return np.array(pts)


class C10_Ionosphere(Scene):
    def construct(self):
        title = title_bar(r"电离层“反射”是连续折射：$n=\sqrt{1-80.8N/f^2}$ 随高度减小，射线逐渐弯回地面")
        fitw(title, 13.6)
        self.play(FadeIn(title))
        GX, GY = -6.3, -3.1
        sx, sy = 6.6e-3, 9.8e-3

        def P(x, h):
            return np.array([GX + sx * x, GY + sy * h, 0])

        ground = Line(P(-30, 0), P(1950, 0), color=GREY_A, stroke_width=3)
        # 电子密度着色
        layers = VGroup()
        for hh in np.arange(200, 400, 8):
            Nrel = 1 - ((hh + 4 - 300) / 100) ** 2
            r = Rectangle(width=sx * 1980, height=sy * 8, stroke_width=0, fill_color=BLUE_D, fill_opacity=0.08 + 0.5 * Nrel)
            r.move_to(P(960, hh + 4))
            layers.add(r)
        lt = CT(r"电离层（电子密度在 $300$ km 处最大）", 20, BLUE_B).move_to(P(1450, 420))
        # 电子密度剖面小图
        prof = poly([P(1880 - 260 * (1 - ((h - 300) / 100) ** 2), h) for h in np.linspace(200, 400, 60)], BLUE_B, 2.5)
        profl = MT("N(h)", 20, BLUE_B).next_to(P(1700, 300), LEFT, buff=0.05)
        tx = Dot(P(0, 0), color=C_HL, radius=0.08)
        self.play(Create(ground), FadeIn(layers), FadeIn(lt), Create(prof), FadeIn(profl), FadeIn(tx))
        # ---- A. 入射角一定，频率不同
        capA = CT(r"(1) 入射角 $\theta_0=60^\circ$ 一定：频率越高，要到电子密度越大处才折回，落地越远；高于 $f_{\max}$ 就穿出", 22)
        fitw(capA, 13.4).next_to(title, DOWN, buff=0.12)
        self.play(FadeIn(capA))
        rays = VGroup()
        cols = [C_E, C_HL, RED_C]
        labs = VGroup()
        for f, col in zip([12, 15, 18], cols):
            pts = iono_ray(60, f)
            r = poly([P(*q) for q in pts], col, 3)
            rays.add(r)
            self.play(Create(r), run_time=2.0)
            end = pts[-1]
            lb = MT(f"{f}\\,\\mathrm{{MHz}}", 20, col)
            if end[1] > 400:
                lb.next_to(P(*end), RIGHT, buff=0.08)
            else:
                lb.next_to(P(*end), UP, buff=0.12)
            labs.add(lb)
            self.play(FadeIn(lb), run_time=0.4)
        muf = VGroup(MT(r"f_{\max}=\sqrt{80.8N_{\max}}\sec\theta_0", 28, C_HL),
                     CT(r"本例 $\sqrt{80.8N_{\max}}=8$ MHz，$\theta_0=60^\circ$：$f_{\max}=16$ MHz", 20)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        muf.move_to(P(560, 120))
        mb = BackgroundRectangle(muf, fill_opacity=0.85, buff=0.08)
        self.play(FadeIn(mb), FadeIn(muf))
        self.wait(2.5)
        self.play(FadeOut(rays), FadeOut(labs), FadeOut(muf), FadeOut(mb), FadeOut(capA))
        # ---- B. 频率一定，入射角不同 → 静区
        capB = CT(r"(2) 频率 $f=12$ MHz 一定：减小入射角，落地点先变近、后变远；$\theta_0<\theta_{0\min}$ 时穿出电离层", 22)
        fitw(capB, 13.4).next_to(title, DOWN, buff=0.12)
        self.play(FadeIn(capB))
        angs = [75, 68, 62, 56, 52, 49.5, 48.6, 46]
        raysB = VGroup()
        lands = []
        for i, a in enumerate(angs):
            pts = iono_ray(a, 12)
            col = interpolate_color(YELLOW, RED, i / (len(angs) - 1))
            r = poly([P(*q) for q in pts], col, 2.6)
            raysB.add(r)
            if pts[-1][1] < 10:
                lands.append(pts[-1][0])
            self.play(Create(r), run_time=1.0)
        skip = min(lands)
        zone = Rectangle(width=sx * (skip - 60), height=0.22, stroke_width=0, fill_color=RED_E, fill_opacity=0.75)
        zone.move_to(P(60 + (skip - 60) / 2, 0) + DOWN * 0.13)
        zl = CT(r"静区：天波到不了，地波又已衰减殆尽", 20, RED_B).next_to(zone, UP, buff=0.08)
        zlb = BackgroundRectangle(zl, fill_opacity=0.85, buff=0.04)
        gw = Rectangle(width=sx * 60, height=0.22, stroke_width=0, fill_color=GREEN_D, fill_opacity=0.8).move_to(P(30, 0) + DOWN * 0.13)
        gwl = CT("地波", 16, GREEN_B).next_to(gw, DOWN, buff=0.04)
        self.play(FadeIn(zone), FadeIn(gw), FadeIn(gwl), FadeIn(zlb), FadeIn(zl))
        th = VGroup(MT(r"\theta_{0\min}=\arcsin\sqrt{1-\frac{80.8N_{\max}}{f^2}}", 26, C_HL),
                    CT(r"本例 $\theta_{0\min}\approx48^\circ$，静区半径约 $" + f"{skip:.0f}" + r"$ km", 20),
                    CT(r"最佳工作频率 $f_{\mathrm{opt}}=0.85f_{\max}$", 20)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        th.move_to(P(1450, 120))
        thb = BackgroundRectangle(th, fill_opacity=0.85, buff=0.08)
        self.play(FadeIn(thb), FadeIn(th))
        self.wait(3.5)


# --------------------------------------------------------------------------
# 10.2.2 多径：频率选择性衰落与快衰落
# --------------------------------------------------------------------------
class C10_Multipath(Scene):
    def construct(self):
        title = title_bar(r"多径传输：同一时延差 $\tau$ 对不同频率造成不同相差 $\varphi=\omega\tau$——频率选择性衰落")
        fitw(title, 13.6)
        self.play(FadeIn(title))
        a = 0.8
        ax = Axes(x_range=[0, 4, 1], y_range=[0, 2, 1], x_length=8.2, y_length=3.0,
                  axis_config={"stroke_width": 1.5, "include_ticks": False, "include_tip": False}).move_to([-2.2, 0.35, 0])
        xl = MT(r"f\tau", 22, GREY_B).next_to(ax.x_axis, RIGHT, buff=0.1)
        yl = CT(r"合成场强 $|1+a\,\mathrm e^{-\mathrm j2\pi f\tau}|$（$a=0.8$）", 20, GREY_B).next_to(ax.y_axis, UP, buff=0.08).shift(RIGHT * 1.8)
        tks = VGroup(*[MT(s, 18, GREY_B).next_to(ax.c2p(k, 0), DOWN, buff=0.06) for k, s in [(0.5, r"\tfrac12"), (1, "1"), (1.5, r"\tfrac32"), (2, "2"), (3, "3"), (4, "4")]])
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(tks))
        ft = ValueTracker(0.0)
        H = lambda x: abs(1 + a * np.exp(-2j * np.pi * x))
        curve = always_redraw(lambda: poly([ax.c2p(q, H(q)) for q in np.linspace(0, max(ft.get_value(), 1e-3), 300)], C_U, 3.5))
        pc = np.array([4.6, 0.3, 0])
        ps = 0.85
        v1 = Arrow(pc, pc + RIGHT * ps, buff=0, color=C_E, stroke_width=4, max_tip_length_to_length_ratio=0.2)
        endp = lambda: pc + RIGHT * ps + a * ps * np.array([np.cos(-2 * np.pi * ft.get_value()), np.sin(-2 * np.pi * ft.get_value()), 0])
        v2 = always_redraw(lambda: Arrow(pc + RIGHT * ps, endp(), buff=0, color=C_REF, stroke_width=4, max_tip_length_to_length_ratio=0.2))
        vs = always_redraw(lambda: Arrow(pc, endp(), buff=0, color=C_U, stroke_width=5, max_tip_length_to_length_ratio=0.15))
        pl = VGroup(CT("路径 1", 18, C_E), CT("路径 2（迟到 $\\tau$）", 18, C_REF), CT("合成", 18, C_U)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to(pc + UP * 1.6 + RIGHT * 0.5)
        self.play(GrowArrow(v1), FadeIn(v2), FadeIn(vs), FadeIn(pl))
        self.add(curve)
        self.play(ft.animate.set_value(4.0), run_time=8, rate_func=linear)
        n1 = CT(r"$f\tau=\frac12,\frac32,\cdots$：两路反相，合成场强极小；相邻极小间隔 $\Delta f=1/\tau$", 22)
        fitw(n1, 13).next_to(ax, DOWN, buff=0.45)
        self.play(FadeIn(n1))
        # 信号频谱窗口
        nb = Rectangle(width=ax.c2p(0.25, 0)[0] - ax.c2p(0, 0)[0], height=3.0, stroke_width=0, fill_color=GREEN, fill_opacity=0.25).move_to(ax.c2p(1.0, 1.0))
        nbl = CT(r"窄带信号 $B\ll1/\tau$：带内近似平坦，不失真", 20, GREEN_B)
        wb = Rectangle(width=ax.c2p(1.6, 0)[0] - ax.c2p(0, 0)[0], height=3.0, stroke_width=0, fill_color=RED, fill_opacity=0.22).move_to(ax.c2p(2.4, 1.0))
        wbl = CT(r"宽带信号 $B>1/\tau$：不同频率分量衰落不同，波形失真", 20, RED_B)
        g = VGroup(nbl, wbl).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        fitw(g, 13).next_to(n1, DOWN, buff=0.2)
        self.play(FadeIn(nb), FadeIn(nbl))
        self.play(FadeIn(wb), FadeIn(wbl))
        rule = CT(r"容许带宽 $\Delta f=\dfrac1\tau$", 28, C_HL).move_to(pc + DOWN * 1.7)
        self.play(FadeIn(rule))
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not title])
        # ---- 快衰落：很多散射波随机相位叠加
        title2 = title_bar(r"移动台周围许多散射波随机相位叠加：走动半个波长，合成场强就可能从峰值跌入深谷——快衰落")
        fitw(title2, 13.6)
        self.play(FadeOut(title), FadeIn(title2))
        rng = np.random.default_rng(7)
        N = 10
        amp = rng.uniform(0.4, 1.0, N)
        alpha = rng.uniform(0, 2 * np.pi, N)
        phi0 = rng.uniform(0, 2 * np.pi, N)
        amp /= np.sqrt((amp ** 2).sum())
        xt = ValueTracker(0.0)   # 移动距离 / λ

        def phasors(x):
            return amp * np.exp(1j * (phi0 + 2 * np.pi * x * np.cos(alpha)))

        pc = np.array([-4.4, -0.5, 0])
        S = 2.2

        def chain():
            g = VGroup()
            p = pc.copy()
            for z in phasors(xt.get_value()):
                q = p + S * np.array([z.real, z.imag, 0])
                g.add(Arrow(p, q, buff=0, color=C_REF, stroke_width=3, max_tip_length_to_length_ratio=0.25))
                p = q
            g.add(Arrow(pc, p, buff=0, color=C_U, stroke_width=5, max_tip_length_to_length_ratio=0.12))
            return g

        ch = always_redraw(chain)
        circ = Circle(radius=S, color=GREY_D, stroke_width=1).move_to(pc)
        cl = CT(r"$N=10$ 条路径的相量首尾相接", 20).next_to(circ, DOWN, buff=0.15)
        self.play(Create(circ), FadeIn(ch), FadeIn(cl))
        ax2 = Axes(x_range=[0, 3, 0.5], y_range=[-30, 8, 10], x_length=6.6, y_length=3.6,
                   axis_config={"stroke_width": 1.5, "include_ticks": False, "include_tip": False}).move_to([3.2, -0.5, 0])
        x2 = CT(r"移动距离 $/\lambda$", 20, GREY_B).next_to(ax2.x_axis, DOWN, buff=0.15).shift(RIGHT * 2.5)
        y2 = CT(r"合成场强 / dB", 20, GREY_B).next_to(ax2.y_axis, UP, buff=0.08)
        t2 = VGroup(*[MT(str(k), 18, GREY_B).next_to(ax2.c2p(k, -30), DOWN, buff=0.06) for k in (1, 2, 3)],
                    *[MT(str(k), 18, GREY_B).next_to(ax2.c2p(0, k), LEFT, buff=0.06) for k in (0, -10, -20, -30)])
        z0 = DashedLine(ax2.c2p(0, 0), ax2.c2p(3, 0), color=GREY_D, stroke_width=1.2)
        self.play(Create(ax2), FadeIn(x2), FadeIn(y2), FadeIn(t2), Create(z0))
        db = lambda x: np.clip(20 * np.log10(abs(phasors(x).sum()) + 1e-6), -30, 8)
        env = always_redraw(lambda: poly([ax2.c2p(q, db(q)) for q in np.linspace(0, max(xt.get_value(), 1e-3), 400)], C_U, 3))
        self.add(env)
        self.play(xt.animate.set_value(3.0), run_time=12, rate_func=linear)
        fin = CT(r"深衰落相距约 $\lambda/2$；对策：分集接收（空间、频率、极化分集）、均衡、交织编码", 22, C_HL).to_edge(DOWN, buff=0.2)
        fitw(fin, 13.2)
        self.play(FadeIn(fin))
        self.wait(3)


# --------------------------------------------------------------------------
# 10.8.2 电磁屏蔽：反射 + 趋肤衰减
# --------------------------------------------------------------------------
class C10_Shielding(Scene):
    def construct(self):
        title = title_bar(r"电磁屏蔽：入射波在金属表面大部分被反射，透入的部分按 $\mathrm e^{-x/\delta}$ 迅速衰减")
        fitw(title, 13.6)
        self.play(FadeIn(title))
        X1, X2 = 0.0, 3.0      # 金属板屏幕位置
        yc = 0.4
        slab = Rectangle(width=X2 - X1, height=4.2, stroke_color=GREY_A, stroke_width=2, fill_color=GREY_D, fill_opacity=0.55).move_to([(X1 + X2) / 2, yc, 0])
        sl = CT("良导体屏蔽板（厚 $t$）", 20).next_to(slab, UP, buff=0.08)
        self.play(FadeIn(slab), FadeIn(sl))
        t = ValueTracker(0.0)
        lam_s = 2.4                # 空气中屏幕波长
        dlt = 0.6                  # 屏幕上的趋肤深度
        A0 = 1.1

        def air(x, tt):            # 入射 + 反射（Γ≈−1）
            k = TAU / lam_s
            return A0 * (np.cos(TAU * tt - k * (x - X1)) - np.cos(TAU * tt + k * (x - X1)))

        def inside(x, tt):         # 归一化到表面值（放大显示）
            u = (x - X1) / dlt
            return 0.9 * np.exp(-u) * np.cos(TAU * tt - u)

        xa = np.linspace(-6.6, X1, 300)
        xi = np.linspace(X1, X2, 200)
        inc = always_redraw(lambda: poly([[x, yc + A0 * np.cos(TAU * t.get_value() - TAU / lam_s * (x - X1)), 0] for x in xa], C_INC, 2, 0.6))
        tot = always_redraw(lambda: poly([[x, yc + air(x, t.get_value()), 0] for x in xa], C_E, 3.5))
        ins = always_redraw(lambda: poly([[x, yc + inside(x, t.get_value()), 0] for x in xi], C_HL, 3.5))
        envi = VGroup(DashedVMobject(poly([[x, yc + 0.9 * np.exp(-(x - X1) / dlt), 0] for x in xi], WHITE, 2), num_dashes=20),
                      DashedVMobject(poly([[x, yc - 0.9 * np.exp(-(x - X1) / dlt), 0] for x in xi], WHITE, 2), num_dashes=20))
        out = always_redraw(lambda: poly([[x, yc + 0.9 * np.exp(-(X2 - X1) / dlt) * 30 * np.cos(TAU * t.get_value() - (X2 - X1) / dlt - TAU / lam_s * (x - X2)), 0]
                                          for x in np.linspace(X2, 6.8, 200)], C_I, 3))
        self.add(inc)
        l1 = CT(r"入射波", 20, C_INC).move_to([-5.0, yc + 1.6, 0])
        self.play(FadeIn(l1), t.animate.set_value(1.5), run_time=3, rate_func=linear)
        self.add(tot)
        l2 = CT(r"入射 $+$ 反射：表面处 $E\approx0$（$\Gamma\approx-1$，反射损耗 $\mathrm{SE}_r$）", 20, C_E).move_to([-3.3, yc - 2.0, 0])
        self.play(FadeIn(l2), t.animate.set_value(3.0), run_time=3, rate_func=linear)
        self.add(ins, out)
        l3 = CT(r"板内（放大显示）：每走 $\delta$ 衰减到 $1/\mathrm e$（吸收损耗 $\mathrm{SE}_a$）", 20, C_HL).move_to([1.5, yc - 2.45, 0])
        fitw(l3, 7.0)
        l4 = CT(r"透出的波（再放大 30 倍）", 18, C_I).move_to([5.0, yc + 1.0, 0])
        dm = VGroup(*[DashedLine([X1 + k * dlt, yc - 1.9, 0], [X1 + k * dlt, yc + 1.9, 0], color=GREY_B, stroke_width=1) for k in (1, 2, 3, 4)],
                    *[MT(s, 18, GREY_B).move_to([X1 + k * dlt, yc + 2.15, 0]) for k, s in [(1, r"\delta"), (2, r"2\delta"), (3, r"3\delta"), (4, r"4\delta")]])
        self.play(FadeIn(l3), FadeIn(l4), Create(envi), FadeIn(dm), t.animate.set_value(5.0), run_time=3, rate_func=linear)
        self.play(t.animate.set_value(8.0), run_time=5, rate_func=linear)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not title])
        # ---- 频率越高 δ 越小：吸收损耗表
        f1 = VGroup(MT(r"\delta=\frac{1}{\sqrt{\pi f\mu\sigma}},\qquad \mathrm{SE}_a=20\lg\mathrm e^{t/\delta}=8.686\,\frac{t}{\delta}\ \mathrm{dB}", 32),
                    CT(r"铜（$\sigma=5.8\times10^7$ S/m，$\mu=\mu_0$），板厚 $t=0.5$ mm：", 24)).arrange(DOWN, buff=0.3).next_to(title, DOWN, buff=0.35)
        self.play(FadeIn(f1))
        rows = [("50 Hz", 9.35e-3), ("1 kHz", 2.09e-3), ("100 kHz", 2.09e-4), ("1 MHz", 6.61e-5), ("100 MHz", 6.61e-6)]
        ax = Axes(x_range=[0, 5, 1], y_range=[0, 4, 1], x_length=9.0, y_length=3.2,
                  axis_config={"stroke_width": 1.5, "include_ticks": False, "include_tip": False}).move_to([-0.8, -1.6, 0])
        yl = CT(r"$\mathrm{SE}_a$（dB，对数刻度）", 20, GREY_B).next_to(ax.y_axis, UP, buff=0.06)
        ytk = VGroup(*[MT(s, 18, GREY_B).next_to(ax.c2p(0, k), LEFT, buff=0.06) for k, s in [(0, "0.1"), (1, "1"), (2, "10"), (3, "100"), (4, "1000")]])
        self.play(Create(ax), FadeIn(yl), FadeIn(ytk))
        bars = VGroup()
        for i, (name, d) in enumerate(rows):
            A = 8.686 * 0.5e-3 / d
            hgt = np.clip(np.log10(A) + 1, 0.02, 4)
            b = Rectangle(width=1.0, height=ax.c2p(0, hgt)[1] - ax.c2p(0, 0)[1], stroke_width=0,
                          fill_color=interpolate_color(BLUE_C, ORANGE, i / 4), fill_opacity=0.85)
            b.move_to(ax.c2p(i + 0.6, hgt / 2))
            lab = MT(name.replace(" ", r"\,").replace("Hz", r"\mathrm{Hz}").replace("k", r"\mathrm{k}").replace("M", r"\mathrm{M}"), 20).next_to(ax.c2p(i + 0.6, 0), DOWN, buff=0.08)
            dl = MT(rf"\delta={d * 1e3:.3g}\,\mathrm{{mm}}" if d >= 1e-4 else rf"\delta={d * 1e6:.3g}\,\mu\mathrm{{m}}", 16, GREY_A).next_to(lab, DOWN, buff=0.05)
            val = MT(f"{A:.3g}" + r"\,\mathrm{dB}", 18).next_to(b, UP, buff=0.05)
            bars.add(VGroup(b, lab, dl, val))
            self.play(GrowFromEdge(b, DOWN), FadeIn(lab), FadeIn(dl), FadeIn(val), run_time=0.8)
        note = VGroup(CT(r"高频：薄薄一层良导体（非铁磁）就有很大的吸收损耗；", 22, C_HL),
                      CT(r"低频（$<10$ kHz）：$\delta$ 比板厚还大，磁场要靠高 $\mu$ 材料“分流”——磁屏蔽", 22, C_HL)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        fitw(note, 4.4).move_to([5.0, -1.2, 0])
        self.play(FadeIn(note))
        self.wait(3.5)
