"""第 3 章 边值问题的解法 —— manim 动画源码（LaTeX 排版）."""
import numpy as np

from common import *  # noqa: F401,F403
from fieldtools import *  # noqa: F401,F403
from ch2_scenes import plain_axes, charge_dot


def lines_from(ax, charges, src, n, stop, box=(-3.2, 3.2, -3.2, 3.2), color=C_E, angs=None):
    F = charges_field(charges)
    q, a, b = src
    L, A = VGroup(), VGroup()
    if angs is None:
        angs = [(k + 0.5) * TAU / n for k in range(n)]
    for t in angs:
        p0 = (a + 0.1 * np.cos(t), b + 0.1 * np.sin(t))
        pts = trace(F, p0, h=0.02, nmax=1200, box=box, stop=stop, sign=1.0 if q > 0 else -1.0)
        L.add(polyline(ax, pts, color, 2.2))
        A.add(mid_arrow(ax, pts, color, frac=0.4))
    return L, A


# --------------------------------------------------------------------------
# 3.3 镜像法：接地平面与接地导体球
# --------------------------------------------------------------------------
class C3_ImageMethod(Scene):
    def construct(self):
        title = title_bar(r"镜像法：用区域外的“假想电荷”代替导体上的感应电荷，满足同样的边界条件")
        fitw(title, 13.6)
        self.play(FadeIn(title))
        ax = plain_axes(size=6.2).shift(LEFT * 3.2 + DOWN * 0.45)
        d = 1.2
        gnd = Rectangle(width=6.2, height=3.1, stroke_width=0, fill_color=GREY_D, fill_opacity=0.85).move_to(ax.c2p(0, -1.55))
        gl = Line(ax.c2p(-3, 0), ax.c2p(3, 0), color=GREY_A, stroke_width=4)
        gt = CT(r"接地导体平面 $\phi=0$", 24, GREY_A).move_to(ax.c2p(-1.6, -0.35))
        q = charge_dot(ax, 1, 0, d)
        self.play(FadeIn(gnd), Create(gl), FadeIn(gt), FadeIn(q))
        charges = [(1, 0, d), (-1, 0, -d)]
        Lq, Aq = lines_from(ax, charges, (1, 0, d), 18, stop=lambda p: p[1] < 0)
        cap = VGroup(CT(r"点电荷 $q$ 距接地平面 $h$：", 26),
                     CT(r"平面上感应出负电荷，电力线垂直终止于导体表面", 24)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        fitw(cap, 6.0).move_to(RIGHT * 3.6 + UP * 2.0)
        self.play(LaggedStart(*[Create(l) for l in Lq], lag_ratio=0.03), FadeIn(cap), run_time=2.5)
        self.play(FadeIn(Aq))
        # 感应电荷分布
        xs = np.linspace(-3, 3, 200)
        rho = -d / (2 * np.pi * (xs ** 2 + d * d) ** 1.5)
        curve = VMobject(color=C_NEG, stroke_width=4)
        curve.set_points_as_corners([ax.c2p(x, 1.6 * r) for x, r in zip(xs, rho)])
        cl = CT(r"感应面电荷 $\rho_S=-\dfrac{qh}{2\pi(x^2+y^2+h^2)^{3/2}}$，总量 $-q$", 24, C_NEG)
        fitw(cl, 6.0).move_to(RIGHT * 3.6 + UP * 0.8)
        self.play(Create(curve), FadeIn(cl))
        self.wait(1)
        # 揭示镜像电荷
        self.play(gnd.animate.set_fill(opacity=0.15), FadeOut(gt), FadeOut(curve))
        qi = charge_dot(ax, -1, 0, -d).set_opacity(0.8)
        Li, Ai = lines_from(ax, charges, (1, 0, d), 18, stop=lambda p: p[1] < -d + 0.12 and abs(p[0]) < 0.12, color=C_E)
        for l in Li:
            l.set_stroke(opacity=0.35)
            l.set_stroke(width=2)
        dash = VGroup(*[DashedVMobject(l, num_dashes=40) for l in Li])
        cap2 = VGroup(
            CT(r"把导体换成镜像电荷 $-q$（位于 $-h$）：", 26, C_HL),
            CT(r"上半空间：只有源 $q$，满足同一个泊松方程", 24),
            CT(r"边界 $z=0$：$\dfrac{q}{R_+}-\dfrac{q}{R_-}=0$，电位仍为零", 24),
            CT(r"唯一性定理 $\Rightarrow$ 上半空间的场完全相同", 26, C_E),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        fitw(cap2, 6.0).move_to(RIGHT * 3.6 + DOWN * 0.6)
        self.play(FadeIn(qi), Create(dash), FadeIn(cap2), run_time=2)
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in [Lq, Aq, dash, qi, q, gnd, gl, cap, cl, cap2]])

        # ---- 接地导体球
        a, D = 1.0, 2.2
        b, qq = a * a / D, -a / D
        sph = Circle(radius=a * ax.x_length / 6, color=GREY_A, stroke_width=4, fill_color=GREY_D, fill_opacity=0.85).move_to(ax.c2p(0, 0))
        st = CT(r"接地导体球", 22, GREY_A).move_to(ax.c2p(0, 0))
        q1 = charge_dot(ax, 1, D, 0)
        self.play(FadeIn(sph), FadeIn(st), FadeIn(q1))
        ch = [(1, D, 0), (qq, b, 0)]
        Ls, As = lines_from(ax, ch, (1, D, 0), 20, stop=lambda p: p[0] ** 2 + p[1] ** 2 < a * a)
        cap3 = VGroup(
            CT(r"点电荷 $q$ 距球心 $d$，球半径 $a$：", 26),
            CT(r"镜像电荷 $q'=-\dfrac{a}{d}q$，位于 $b=\dfrac{a^2}{d}$", 28, C_HL),
            CT(r"（$q'$ 与 $q$ 关于球面互为“反演点”）", 22, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        fitw(cap3, 6.0).move_to(RIGHT * 3.6 + UP * 1.6)
        self.play(LaggedStart(*[Create(l) for l in Ls], lag_ratio=0.03), FadeIn(As), FadeIn(cap3), run_time=2.5)
        self.play(sph.animate.set_fill(opacity=0.12), FadeOut(st))
        qd = charge_dot(ax, -1, b, 0).scale(0.7)
        ql = MT(r"q'", 26, C_NEG).next_to(qd, DOWN, buff=0.08)
        P = charges_potential(ch)
        zero = contour_lines(ax, P, [0.0], [RED], n=160, sw=3)
        cap4 = VGroup(
            CT(r"$q$ 与 $q'$ 的零电位面恰好是球面 $r=a$（红）", 24, RED),
            CT(r"验证：球面上 $\dfrac{R_{q'}}{R_q}=\dfrac ad$，$\dfrac{q}{R_q}+\dfrac{q'}{R_{q'}}=0$", 24),
            CT(r"球不接地且不带电：再在球心加 $-q'$", 24, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        fitw(cap4, 6.0).move_to(RIGHT * 3.6 + DOWN * 1.1)
        self.play(FadeIn(qd), FadeIn(ql), Create(zero), FadeIn(cap4), run_time=2)
        self.wait(3)


# --------------------------------------------------------------------------
# 3.4 分离变量法：矩形槽的傅里叶级数解
# --------------------------------------------------------------------------
class C3_Separation(Scene):
    def construct(self):
        title = title_bar(r"分离变量法：盖板电位 $U_0$、其余三面接地的矩形槽，$\phi=\sum X_n(x)Y_n(y)$")
        fitw(title, 13.6)
        self.play(FadeIn(title))
        a, b = 2.0, 1.4
        W = 6.0
        H = W * b / a
        origin = np.array([-6.6 + 0.4, -2.6, 0])

        def P(x, y):
            return origin + np.array([x / a * W, y / b * H, 0])

        nx, ny = 220, 154
        X, Y = np.meshgrid(np.linspace(0, a, nx), np.linspace(0, b, ny))

        def partial(N):
            S = 0 * X
            for n in range(1, N + 1, 2):
                k = n * np.pi / a
                S = S + 4 / (n * np.pi) * np.sin(k * X) * np.sinh(k * Y) / np.sinh(k * b)
            return S

        walls = VGroup(Line(P(0, b), P(0, 0), color=GREY_A, stroke_width=5), Line(P(0, 0), P(a, 0), color=GREY_A, stroke_width=5),
                       Line(P(a, 0), P(a, b), color=GREY_A, stroke_width=5))
        lid = Line(P(0.03, b + 0.04), P(a - 0.03, b + 0.04), color=C_HL, stroke_width=6)
        labs = VGroup(CT(r"$\phi=U_0$", 24, C_HL).next_to(lid, UP, buff=0.08),
                      CT(r"$\phi=0$", 22, GREY_A).next_to(P(0, b / 2), LEFT, buff=0.1),
                      CT(r"$\phi=0$", 22, GREY_A).next_to(P(a, b / 2), RIGHT, buff=0.1),
                      CT(r"$\phi=0$", 22, GREY_A).next_to(P(a / 2, 0), DOWN, buff=0.1))
        self.play(Create(walls), Create(lid), FadeIn(labs))
        steps = VGroup(
            MT(r"\phi=X(x)Y(y),\ \ \frac{X''}{X}=-\frac{Y''}{Y}=-k^2", 30),
            MT(r"X_n=\sin\frac{n\pi x}{a},\quad Y_n=\sinh\frac{n\pi y}{a}", 30),
            MT(r"\phi=\sum_{n\ \text{odd}}\frac{4U_0}{n\pi}\,\frac{\sinh(n\pi y/a)}{\sinh(n\pi b/a)}\sin\frac{n\pi x}{a}", 32, C_HL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        fitw(steps, 6.0).move_to(RIGHT * 3.6 + UP * 1.9)
        self.play(FadeIn(steps[0]))
        self.play(FadeIn(steps[1]))
        self.play(FadeIn(steps[2]))
        ax2 = Axes(x_range=[0, a, 0.5], y_range=[-0.2, 1.3, 0.5], x_length=5.6, y_length=2.4,
                   axis_config={"stroke_width": 1.5, "include_ticks": False, "include_tip": False}).move_to(RIGHT * 3.6 + DOWN * 1.7)
        l0 = DashedLine(ax2.c2p(0, 1), ax2.c2p(a, 1), color=GREY_B)
        y1 = MT(r"U_0", 22, GREY_B).next_to(ax2.c2p(0, 1), LEFT, buff=0.08)
        al = CT(r"盖板处 $\phi(x,b)$ 的部分和", 22, GREY_A).next_to(ax2, UP, buff=0.08)
        self.play(Create(ax2), Create(l0), FadeIn(y1), FadeIn(al))
        old = None
        for N in [1, 3, 5, 9, 21, 61]:
            S = partial(N)
            img = heat_image(S, 0, 1.0, W).move_to((P(0, 0) + P(a, b)) / 2)
            cont = contour_lines(Axes(x_range=[0, a, 1], y_range=[0, b, 1], x_length=W, y_length=H).move_to((P(0, 0) + P(a, b)) / 2),
                                 lambda XX, YY: partial_eval(XX, YY, N, a, b), [0.1, 0.25, 0.5, 0.75, 0.9], [WHITE] * 5,
                                 xr=(0, a), yr=(0, b), n=90, sw=1.4, opacity=0.8)
            xs = np.linspace(0, a, 400)
            ys = [partial_eval(np.array(x), np.array(b), N, a, b) for x in xs]
            g = VMobject(color=C_E, stroke_width=3).set_points_as_corners([ax2.c2p(x, float(v)) for x, v in zip(xs, ys)])
            nl = MT(rf"N={N}", 30, C_E).next_to(al, RIGHT, buff=0.3)
            grp = Group(img, cont, g, nl)
            if old is None:
                self.play(FadeIn(img), FadeIn(cont), Create(g), FadeIn(nl))
            else:
                self.play(FadeOut(old), FadeIn(grp), run_time=0.8)
            self.bring_to_front(walls, lid)
            self.wait(1.0)
            old = grp
        note = VGroup(
            CT(r"高次项 $\propto e^{-n\pi(b-y)/a}$，离开盖板迅速衰减：槽内深处只剩 $n=1$", 22),
            CT(r"盖板两端电位跳变，部分和在角上振荡（吉布斯现象）", 22, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        fitw(note, 13).to_edge(DOWN, buff=0.12)
        self.play(FadeIn(note))
        self.wait(3)


def partial_eval(X, Y, N, a, b):
    S = 0 * X
    for n in range(1, N + 1, 2):
        k = n * np.pi / a
        S = S + 4 / (n * np.pi) * np.sin(k * X) * np.sinh(k * Y) / np.sinh(k * b)
    return S


# --------------------------------------------------------------------------
# 3.5 有限差分法：简单迭代与超松弛
# --------------------------------------------------------------------------
class C3_FiniteDifference(Scene):
    def construct(self):
        title = title_bar(r"有限差分法：$\phi_0=\tfrac14(\phi_1+\phi_2+\phi_3+\phi_4)$，反复迭代直到收敛")
        fitw(title, 13.6)
        self.play(FadeIn(title))
        M, N = 20, 14  # 内部网格 x、y 方向的节点数 +1

        def solve(omega, iters):
            U = np.zeros((N + 1, M + 1))
            U[N, 1:M] = 1.0
            hist, snaps = [], {}
            for k in range(1, iters + 1):
                mx = 0.0
                for i in range(1, N):
                    for j in range(1, M):
                        new = 0.25 * (U[i + 1, j] + U[i - 1, j] + U[i, j + 1] + U[i, j - 1])
                        r = new - U[i, j]
                        U[i, j] += omega * r
                        mx = max(mx, abs(r))
                hist.append(mx)
                snaps[k] = U.copy()
            return hist, snaps

        hist1, snaps1 = solve(1.0, 500)
        w_opt = 2 / (1 + np.sin(np.pi / max(M, N)))
        hist2, snaps2 = solve(w_opt, 500)

        W = 5.6
        center = np.array([-3.4, 0.1, 0])
        frame = Rectangle(width=W, height=W * N / M, color=GREY_A, stroke_width=3).move_to(center)
        lid = Line(frame.get_corner(UL), frame.get_corner(UR), color=C_HL, stroke_width=6)
        self.play(Create(frame), Create(lid))
        # 五点格式示意
        st = VGroup(Dot(ORIGIN, color=C_E, radius=0.09))
        for v, lab in [(RIGHT, "1"), (UP, "2"), (LEFT, "3"), (DOWN, "4")]:
            st.add(Line(ORIGIN, v * 0.6, color=GREY_B, stroke_width=2), Dot(v * 0.6, color=WHITE, radius=0.07),
                   MT(lab, 22).move_to(v * 0.85))
        st.add(MT("0", 22, C_E).move_to(UR * 0.22))
        st.move_to(RIGHT * 1.9 + UP * 2.0)
        ft = MT(r"\phi_0=\frac{\phi_1+\phi_2+\phi_3+\phi_4}{4}", 30).next_to(st, RIGHT, buff=0.3)
        self.play(FadeIn(st), FadeIn(ft))

        it = ValueTracker(1)

        def img():
            k = int(round(it.get_value()))
            U = snaps1[k]
            return heat_image(U, 0, 1, W).move_to(center)

        im = always_redraw(img)
        cnt = always_redraw(lambda: MT(rf"\text{{iter}}={int(round(it.get_value()))}", 30, C_E).next_to(frame, DOWN, buff=0.15))
        self.add(im, cnt)
        self.bring_to_front(frame, lid)
        cap = CT(r"简单迭代（高斯–赛德尔）：盖板的电位一圈圈“渗”进去", 24).next_to(frame, UP, buff=0.12)
        fitw(cap, 6.2)
        self.play(FadeIn(cap))
        self.play(it.animate.set_value(400), run_time=8, rate_func=lambda t: t ** 2)
        im.clear_updaters()
        self.wait(0.5)
        # 收敛曲线
        ax = Axes(x_range=[0, 500, 100], y_range=[-6, 0, 2], x_length=5.6, y_length=2.6,
                  axis_config={"stroke_width": 1.5, "include_ticks": False, "include_tip": False}).move_to(RIGHT * 3.6 + DOWN * 1.75)
        yl = MT(r"\log_{10}\max|\Delta\phi|", 24, GREY_B).next_to(ax, UP, buff=0.05).shift(LEFT * 1.6)
        xl = CT(r"迭代次数", 22, GREY_B).next_to(ax, DOWN, buff=0.08)
        ticks = VGroup(*[MT(str(v), 20, GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.06) for v in (0, -2, -4, -6)])

        def curve(h, col):
            pts = [ax.c2p(k + 1, max(np.log10(v + 1e-12), -6)) for k, v in enumerate(h)]
            return VMobject(color=col, stroke_width=3).set_points_as_corners(pts)

        c1, c2 = curve(hist1, C_E), curve(hist2, C_H)
        l1 = CT(r"简单迭代 $\omega=1$", 22, C_E).next_to(ax.c2p(500, -2.6), LEFT, buff=0.05)
        l2 = CT(rf"超松弛 $\omega={w_opt:.2f}$", 22, C_H).next_to(ax.c2p(40, -4.7), RIGHT, buff=0.05)
        self.play(Create(ax), FadeIn(yl), FadeIn(xl), FadeIn(ticks))
        self.play(Create(c1), FadeIn(l1), run_time=1.5)
        self.play(Create(c2), FadeIn(l2), run_time=1.5)
        k1 = next((k for k, v in enumerate(hist1) if v < 1e-5), len(hist1))
        k2 = next((k for k, v in enumerate(hist2) if v < 1e-5), len(hist2))
        sor = VGroup(
            MT(r"\phi_0^{(k+1)}=\phi_0^{(k)}+\omega\,R_0", 28),
            CT(rf"误差降到 $10^{{-5}}$：简单迭代 {k1 + 1} 次，超松弛 {k2 + 1} 次", 22, C_HL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        fitw(sor, 6.0).move_to(RIGHT * 3.6 + UP * 0.6)
        self.play(FadeIn(sor))
        self.wait(3)
