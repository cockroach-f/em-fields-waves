"""第 1 章 矢量分析与场论 —— manim 动画源码（LaTeX 排版）."""
import numpy as np

from common import *  # noqa: F401,F403


def fitw(m, w):
    if m.width > w:
        m.scale_to_fit_width(w)
    return m


def field_arrows(ax, F, xs, ys, scale=0.35, color=C_E, maxlen=0.55, sw=2.5):
    g = VGroup()
    for x in xs:
        for y in ys:
            v = np.array(F(x, y), dtype=float)
            n = np.linalg.norm(v)
            if n < 1e-9:
                continue
            L = min(scale * n, maxlen)
            d = v / n * L
            p = ax.c2p(x, y)
            q = ax.c2p(x + d[0], y + d[1])
            a = Arrow(p - (q - p) / 2, p + (q - p) / 2, buff=0, stroke_width=sw,
                      max_tip_length_to_length_ratio=0.35, color=color)
            a.set_opacity(min(0.35 + 0.5 * n, 1))
            g.add(a)
    return g


def small_axes(xr=(-3, 3), yr=(-3, 3), size=5.2):
    return Axes(x_range=[xr[0], xr[1], 1], y_range=[yr[0], yr[1], 1], x_length=size, y_length=size,
                axis_config={"stroke_width": 1.5, "stroke_opacity": 0.6, "include_ticks": False})


# --------------------------------------------------------------------------
# 1.2 圆柱坐标系与球坐标系：单位矢量随点而变
# --------------------------------------------------------------------------
class C1_Coordinates(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=68 * DEGREES, theta=-50 * DEGREES, zoom=0.9)
        axes = ThreeDAxes(x_range=[-3, 3, 1], y_range=[-3, 3, 1], z_range=[-2.5, 3, 1],
                          x_length=6, y_length=6, z_length=5.5, axis_config={"stroke_width": 2})
        lab = VGroup(MT("x", 30).move_to(axes.c2p(3.3, 0, 0)), MT("y", 30).move_to(axes.c2p(0, 3.3, 0)),
                     MT("z", 30).move_to(axes.c2p(0, 0, 3.3)))
        for l in lab:
            l.rotate(PI / 2, RIGHT)
        title = title_bar(r"圆柱坐标 $(\rho,\phi,z)$：单位矢量 $\arho,\aphi$ 随 $\phi$ 转动")
        self.add_fixed_in_frame_mobjects(title)
        self.play(Create(axes), FadeIn(lab), FadeIn(title))

        phi = ValueTracker(0.6)
        rho, zz = 2.0, 1.5

        def P():
            f = phi.get_value()
            return np.array([rho * np.cos(f), rho * np.sin(f), zz])

        cyl = Surface(lambda u, v: axes.c2p(rho * np.cos(u), rho * np.sin(u), v), u_range=[0, TAU], v_range=[-0.2, 2.6],
                      resolution=(24, 3), fill_opacity=0.12, stroke_width=0.4, checkerboard_colors=[BLUE_D, BLUE_E])
        dot = always_redraw(lambda: Dot(axes.c2p(*P()), radius=0.07, color=WHITE))
        drop = always_redraw(lambda: DashedLine(axes.c2p(*P()), axes.c2p(P()[0], P()[1], 0), color=GREY_B))
        rad = always_redraw(lambda: Line(axes.c2p(0, 0, 0), axes.c2p(P()[0], P()[1], 0), color=GREY_B))

        def uv(vec, col):
            p = axes.c2p(*P())
            return Arrow(p, p + 1.1 * np.array(vec), buff=0, color=col, stroke_width=5, max_tip_length_to_length_ratio=0.22)

        a_r = always_redraw(lambda: uv([np.cos(phi.get_value()), np.sin(phi.get_value()), 0], C_POS))
        a_p = always_redraw(lambda: uv([-np.sin(phi.get_value()), np.cos(phi.get_value()), 0], C_E))
        a_z = always_redraw(lambda: uv([0, 0, 1], C_H))
        self.play(FadeIn(cyl), FadeIn(dot), Create(drop), Create(rad))
        self.play(FadeIn(a_r), FadeIn(a_p), FadeIn(a_z))
        leg = panel(r"{\color[HTML]{FC6255}$\arho$}：沿 $\rho$ 增大（离开 $z$ 轴）",
                    r"{\color[HTML]{FFFF00}$\aphi$}：沿 $\phi$ 增大（绕 $z$ 轴）",
                    r"{\color[HTML]{5CD0B3}$\az$}：沿 $z$ 增大", size=24).to_corner(UL, buff=0.3).shift(DOWN * 0.8)
        self.add_fixed_in_frame_mobjects(leg)
        self.play(FadeIn(leg))
        self.begin_ambient_camera_rotation(rate=0.08)
        self.play(phi.animate.set_value(0.6 + 1.6 * PI), run_time=6, rate_func=linear)
        note = fitw(CT(r"$\arho=\ax\cos\phi+\ay\sin\phi$，$\aphi=-\ax\sin\phi+\ay\cos\phi$：不是常矢量，求导、积分时不能提出积分号", 24, C_HL), 13).to_edge(DOWN, buff=0.25)
        self.add_fixed_in_frame_mobjects(note)
        self.play(FadeIn(note))
        self.wait(1.5)
        self.stop_ambient_camera_rotation()

        # ---- spherical
        self.play(FadeOut(VGroup(cyl, dot, drop, rad, a_r, a_p, a_z)), FadeOut(leg), FadeOut(note), FadeOut(title))
        title2 = title_bar(r"球坐标 $(r,\theta,\phi)$：$\ar,\atheta,\aphi$ 构成右手正交系")
        self.add_fixed_in_frame_mobjects(title2)
        th = ValueTracker(0.8)
        R = 2.4

        def Q():
            t, f = th.get_value(), phi.get_value()
            return R * np.array([np.sin(t) * np.cos(f), np.sin(t) * np.sin(f), np.cos(t)])

        sph = Sphere(radius=R * axes.get_x_unit_size(), resolution=(18, 9), fill_opacity=0.10, stroke_width=0.3,
                     checkerboard_colors=[BLUE_D, BLUE_E]).move_to(axes.c2p(0, 0, 0))
        dot2 = always_redraw(lambda: Dot(axes.c2p(*Q()), radius=0.07, color=WHITE))
        rl = always_redraw(lambda: Line(axes.c2p(0, 0, 0), axes.c2p(*Q()), color=GREY_B))

        def uv2(vec, col):
            p = axes.c2p(*Q())
            return Arrow(p, p + 1.0 * np.array(vec), buff=0, color=col, stroke_width=5, max_tip_length_to_length_ratio=0.22)

        def basis():
            t, f = th.get_value(), phi.get_value()
            er = [np.sin(t) * np.cos(f), np.sin(t) * np.sin(f), np.cos(t)]
            et = [np.cos(t) * np.cos(f), np.cos(t) * np.sin(f), -np.sin(t)]
            ep = [-np.sin(f), np.cos(f), 0]
            return er, et, ep

        b_r = always_redraw(lambda: uv2(basis()[0], C_POS))
        b_t = always_redraw(lambda: uv2(basis()[1], PURPLE_B))
        b_p = always_redraw(lambda: uv2(basis()[2], C_E))
        self.play(FadeIn(title2), FadeIn(sph), FadeIn(dot2), Create(rl))
        self.play(FadeIn(b_r), FadeIn(b_t), FadeIn(b_p))
        leg2 = panel(r"{\color[HTML]{FC6255}$\ar$}：沿径向向外",
                     r"{\color[HTML]{CAA3E8}$\atheta$}：沿经线向“南”（$\theta$ 从 $0$ 到 $\pi$）",
                     r"{\color[HTML]{FFFF00}$\aphi$}：沿纬线向“东”", size=24).to_corner(UL, buff=0.3).shift(DOWN * 0.8)
        self.add_fixed_in_frame_mobjects(leg2)
        self.play(FadeIn(leg2))
        self.begin_ambient_camera_rotation(rate=0.08)
        self.play(th.animate.set_value(2.2), run_time=3)
        self.play(phi.animate.set_value(0.6 + 2.6 * PI), run_time=3)
        note2 = fitw(CT(r"度量系数：$\dd l_r=\dd r$，$\dd l_\theta=r\,\dd\theta$，$\dd l_\phi=r\sin\theta\,\dd\phi$；$\dd V=r^2\sin\theta\,\dd r\,\dd\theta\,\dd\phi$", 24, C_HL), 13).to_edge(DOWN, buff=0.25)
        self.add_fixed_in_frame_mobjects(note2)
        self.play(FadeIn(note2))
        self.wait(2.5)
        self.stop_ambient_camera_rotation()


# --------------------------------------------------------------------------
# 1.3.2 通量与散度：散度 = 单位体积净流出的通量
# --------------------------------------------------------------------------
class C1_Divergence(Scene):
    def construct(self):
        title = title_bar(r"散度 $\nabla\cdot\vv{F}=\lim\limits_{\Delta V\to0}\dfrac{1}{\Delta V}\oint_S\vv F\cdot\dd\vv S$：一点处“冒出”多少")
        self.play(FadeIn(title))
        cases = [
            (lambda x, y: (x, y), r"$\vv F=\ax x+\ay y$", r"$\nabla\cdot\vv F=2$（正源）", (0.6, 0.4), C_POS),
            (lambda x, y: (-x, -y), r"$\vv F=-\ax x-\ay y$", r"$\nabla\cdot\vv F=-2$（负源，汇）", (0.6, 0.4), C_NEG),
            (lambda x, y: (-y, x), r"$\vv F=-\ax y+\ay x$", r"$\nabla\cdot\vv F=0$（无散，转着走）", (0.6, 0.4), C_H),
        ]
        ax = small_axes(size=5.4).shift(LEFT * 3.4 + DOWN * 0.5)
        grid = np.arange(-2.5, 2.6, 0.5)
        self.play(Create(ax))
        old = None
        for F, ftex, dtex, c, col in cases:
            arr = field_arrows(ax, F, grid, grid, scale=0.18, maxlen=0.42)
            lab = VGroup(CT(ftex, 28), CT(dtex, 28, col)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(RIGHT * 3.2 + UP * 1.8)
            rv = ValueTracker(1.2)

            def circ(c=c, rv=rv, col=col):
                r = rv.get_value()
                return Circle(radius=r * ax.x_length / 6, color=col, stroke_width=3).move_to(ax.c2p(*c))

            def flux_arrows(F=F, c=c, rv=rv, col=col):
                r = rv.get_value()
                g = VGroup()
                for k in range(12):
                    t = k * TAU / 12
                    p = np.array(c) + r * np.array([np.cos(t), np.sin(t)])
                    n = np.array([np.cos(t), np.sin(t)])
                    fn = np.dot(F(*p), n)
                    L = 0.25 * fn
                    if abs(L) < 0.02:
                        continue
                    g.add(Arrow(ax.c2p(*p), ax.c2p(*(p + n * L)), buff=0, stroke_width=3,
                                max_tip_length_to_length_ratio=0.4, color=WHITE))
                return g

            def readout(F=F, c=c, rv=rv, col=col):
                r = rv.get_value()
                ts = np.linspace(0, TAU, 400, endpoint=False)
                flux = sum(np.dot(F(c[0] + r * np.cos(t), c[1] + r * np.sin(t)), [np.cos(t), np.sin(t)]) for t in ts) * r * TAU / 400
                area = PI * r * r
                return VGroup(
                    MT(rf"r={r:.2f}", 28),
                    MT(rf"\oint\vv F\cdot\vv a_n\,\dd l={flux:+.3f}", 28),
                    MT(rf"\frac{{1}}{{\Delta S}}\oint={flux / area:+.3f}", 30, col),
                ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(RIGHT * 3.2 + DOWN * 1.0)

            cc = always_redraw(circ)
            fa = always_redraw(flux_arrows)
            ro = always_redraw(readout)
            if old is not None:
                self.play(FadeOut(old))
            self.play(LaggedStart(*[GrowArrow(a) for a in arr], lag_ratio=0.01), FadeIn(lab), run_time=1.5)
            self.play(Create(cc), FadeIn(fa), FadeIn(ro))
            self.play(rv.animate.set_value(0.25), run_time=3)
            self.wait(0.8)
            old = VGroup(arr, lab, cc, fa, ro)
            cc.clear_updaters(); fa.clear_updaters(); ro.clear_updaters()
        self.play(FadeOut(old))
        box = boxed(VGroup(
            MT(r"\nabla\cdot\vv F=\frac{\partial F_x}{\partial x}+\frac{\partial F_y}{\partial y}+\frac{\partial F_z}{\partial z}", 38),
            CT(r"把小体积拼起来，内部公共面的通量两两抵消 $\Rightarrow$ 散度定理", 26, GREY_B),
            MT(r"\oint_S\vv F\cdot\dd\vv S=\int_V\nabla\cdot\vv F\,\dd V", 40, C_HL),
        ).arrange(DOWN, buff=0.3)).move_to(RIGHT * 3.2 + DOWN * 0.3)
        fitw(box, 6.6)
        self.play(FadeIn(box))
        self.wait(3)


# --------------------------------------------------------------------------
# 1.3.3 环量与旋度：放一个小桨轮
# --------------------------------------------------------------------------
class C1_Curl(Scene):
    def construct(self):
        title = title_bar(r"旋度 = 单位面积的环量：在场里放一个小桨轮，看它转不转")
        self.play(FadeIn(title))
        ax = small_axes(size=5.4).shift(LEFT * 3.4 + DOWN * 0.5)
        self.play(Create(ax))
        grid = np.arange(-2.5, 2.6, 0.5)

        def wheel(center, col):
            g = VGroup(Circle(radius=0.32, color=col, stroke_width=3))
            for k in range(4):
                t = k * PI / 2
                g.add(Line(ORIGIN, 0.32 * np.array([np.cos(t), np.sin(t), 0]), color=col, stroke_width=4))
            return g.move_to(ax.c2p(*center))

        cases = [
            (lambda x, y: (-y, x), r"$\vv F=-\ax y+\ay x$（刚体转动）", r"$\nabla\times\vv F=2\az$：桨轮逆时针转", [(0, 0), (1.5, 1.2), (-1.3, -1.4)], 2.0, C_POS),
            (lambda x, y: (y, 0), r"$\vv F=\ax y$（剪切流，矢量线是直线！）", r"$\nabla\times\vv F=-\az$：桨轮顺时针转", [(0, 0), (1.4, 1.4), (-1.4, -1.2)], -1.0, C_E),
            (lambda x, y: (-2 * y / (x * x + y * y), 2 * x / (x * x + y * y)), r"$\vv F=\aphi\dfrac2\rho$（涡旋，矢量线是圆！）", r"$\nabla\times\vv F=0\ (\rho\neq0)$：桨轮只公转不自转", [(1.4, 0)], 0.0, C_H),
        ]
        old = None
        for F, ftex, ctex, centers, curl, col in cases:
            arr = field_arrows(ax, lambda x, y: F(x, y) if x * x + y * y > 0.05 else (0, 0), grid, grid, scale=0.22, maxlen=0.42)
            lab = VGroup(CT(ftex, 26), CT(ctex, 26, col)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(RIGHT * 3.2 + UP * 1.6)
            fitw(lab, 6.6)
            if old is not None:
                self.play(FadeOut(old))
            self.play(LaggedStart(*[GrowArrow(a) for a in arr], lag_ratio=0.01), FadeIn(lab), run_time=1.5)
            wheels = VGroup(*[wheel(c, col) for c in centers])
            self.play(FadeIn(wheels))
            T = 4.0
            if curl == 0.0:
                # 跟着流体绕原点公转，但自身朝向不变（ω_自转 = curl/2 = 0）
                w = wheels[0]
                path = Circle(radius=1.4 * ax.x_length / 6).move_to(ax.c2p(0, 0))
                self.play(MoveAlongPath(w, path), run_time=T, rate_func=linear)
            else:
                self.play(*[Rotate(w, angle=curl / 2 * T * 0.8, about_point=w.get_center()) for w in wheels],
                          run_time=T, rate_func=linear)
            self.wait(0.5)
            old = VGroup(arr, lab, wheels)
        self.play(FadeOut(old))
        txt = VGroup(
            CT(r"桨轮的自转角速度 $=\tfrac12(\nabla\times\vv F)\cdot\az$：转不转与矢量线弯不弯无关", 26),
            MT(r"(\nabla\times\vv F)\cdot\an=\lim_{\Delta S\to0}\frac{1}{\Delta S}\oint_l\vv F\cdot\dd\vv l", 36, C_HL),
            CT(r"小回路拼成大回路，内部公共边的环量抵消 $\Rightarrow$ 斯托克斯定理", 26, GREY_B),
            MT(r"\oint_l\vv F\cdot\dd\vv l=\int_S(\nabla\times\vv F)\cdot\dd\vv S", 38, C_HL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 3.0 + DOWN * 0.2)
        fitw(txt, 6.8)
        # 小网格示意：相邻小方格的公共边环量抵消
        sq = VGroup()
        for i in range(3):
            for j in range(3):
                s = Square(side_length=0.85, color=GREY_B, stroke_width=2).move_to(ax.c2p(-1 + i, -1 + j))
                sq.add(s)
        arcs = VGroup()
        for s in sq:
            a = Arc(radius=0.24, start_angle=-PI / 2, angle=1.6 * PI, color=C_HL, stroke_width=2.5).move_arc_center_to(s.get_center())
            a.add_tip(tip_length=0.12, tip_width=0.12)
            arcs.add(a)
        outer = Square(side_length=0.85 * 3 + 0.0, color=C_HL, stroke_width=4).move_to(ax.c2p(0, 0))
        self.play(FadeIn(txt), Create(sq), FadeIn(arcs))
        self.play(Create(outer))
        self.wait(3)


# --------------------------------------------------------------------------
# 1.4 等值线与梯度；方向导数 = |∇u| cos α
# --------------------------------------------------------------------------
class C1_Gradient(Scene):
    def construct(self):
        title = title_bar(r"梯度 $\nabla u$：垂直于等值面，指向 $u$ 增加最快的方向")
        self.play(FadeIn(title))
        ax = small_axes((-3, 3), (-3, 3), size=5.6).shift(LEFT * 3.3 + DOWN * 0.45)

        def u(x, y):
            return np.exp(-((x - 0.8) ** 2 + (y - 0.6) ** 2) / 1.6) + 0.7 * np.exp(-((x + 1.2) ** 2 + (y + 1.0) ** 2) / 1.0)

        def gu(x, y, h=1e-4):
            return np.array([(u(x + h, y) - u(x - h, y)) / (2 * h), (u(x, y + h) - u(x, y - h)) / (2 * h)])

        # 等值线：用 marching squares 的简化版——取等值点集合画小点
        levels = [0.1, 0.2, 0.35, 0.5, 0.65, 0.8, 0.95]
        cols = color_gradient([BLUE_E, BLUE_B, GREEN_B, YELLOW, ORANGE, RED], len(levels))
        contours = VGroup()
        N = 140
        xs = np.linspace(-3, 3, N)
        ys = np.linspace(-3, 3, N)
        U = np.array([[u(x, y) for x in xs] for y in ys])
        for lev, c in zip(levels, cols):
            segs = VGroup()
            for i in range(N - 1):
                for j in range(N - 1):
                    q = [U[i, j], U[i, j + 1], U[i + 1, j + 1], U[i + 1, j]]
                    pts = []
                    corners = [(xs[j], ys[i]), (xs[j + 1], ys[i]), (xs[j + 1], ys[i + 1]), (xs[j], ys[i + 1])]
                    for k in range(4):
                        a, b = q[k], q[(k + 1) % 4]
                        if (a - lev) * (b - lev) < 0:
                            t = (lev - a) / (b - a)
                            pa, pb = np.array(corners[k]), np.array(corners[(k + 1) % 4])
                            pts.append(pa + t * (pb - pa))
                    if len(pts) == 2:
                        segs.add(Line(ax.c2p(*pts[0]), ax.c2p(*pts[1]), color=c, stroke_width=2.2))
            contours.add(segs)
        self.play(Create(ax), LaggedStart(*[FadeIn(s) for s in contours], lag_ratio=0.2), run_time=2.5)
        cl = CT(r"等值线 $u(x,y)=C$（暖色 = $u$ 大）", 24, GREY_A).next_to(ax, DOWN, buff=0.1)
        self.play(FadeIn(cl))
        grid = np.arange(-2.6, 2.7, 0.52)
        arr = field_arrows(ax, gu, grid, grid, scale=0.9, maxlen=0.45, color=WHITE, sw=2)
        self.play(LaggedStart(*[GrowArrow(a) for a in arr], lag_ratio=0.01), run_time=2)
        t1 = CT(r"白箭头 $=\nabla u$：处处与等值线垂直，越密处越长", 26).move_to(RIGHT * 3.2 + UP * 2.0)
        fitw(t1, 6.6)
        self.play(FadeIn(t1))
        self.wait(1)
        self.play(arr.animate.set_opacity(0.15))

        P = np.array([0.0, -0.6])
        g = gu(*P)
        gn = np.linalg.norm(g)
        pd = Dot(ax.c2p(*P), color=WHITE)
        garr = Arrow(ax.c2p(*P), ax.c2p(*(P + g / gn * 1.4)), buff=0, color=C_HL, stroke_width=5)
        glab = MT(r"\nabla u", 28, C_HL).next_to(garr.get_end(), UP, buff=0.08)
        self.play(FadeIn(pd), GrowArrow(garr), FadeIn(glab))
        ang = ValueTracker(0.0)
        g0 = np.arctan2(g[1], g[0])

        def ldir():
            a = g0 + ang.get_value()
            return np.array([np.cos(a), np.sin(a)])

        larr = always_redraw(lambda: Arrow(ax.c2p(*P), ax.c2p(*(P + ldir() * 1.1)), buff=0, color=C_H, stroke_width=4))
        llab = always_redraw(lambda: MT(r"\vv a_l", 28, C_H).next_to(ax.c2p(*(P + ldir() * 1.25)), ORIGIN))
        self.play(GrowArrow(larr), FadeIn(llab))
        # 右侧：方向导数随角度变化的曲线
        ax2 = Axes(x_range=[0, TAU, PI / 2], y_range=[-1.2, 1.2, 1], x_length=5.6, y_length=2.6,
                   axis_config={"stroke_width": 1.5, "include_ticks": False}).move_to(RIGHT * 3.3 + DOWN * 1.2)
        xl = MT(r"\alpha", 26, GREY_B).next_to(ax2.c2p(TAU, 0), RIGHT, buff=0.1)
        yl = MT(r"\frac{\partial u}{\partial l}=|\nabla u|\cos\alpha", 28, C_H).next_to(ax2, UP, buff=0.15)
        ticks = VGroup(*[MT(s, 22, GREY_B).next_to(ax2.c2p(v, 0), DOWN, buff=0.08) for s, v in
                         [(r"\pi/2", PI / 2), (r"\pi", PI), (r"3\pi/2", 3 * PI / 2)]])
        curve = always_redraw(lambda: ax2.plot(lambda a: np.cos(a), x_range=[0, max(ang.get_value(), 0.01)], color=C_H))
        dt = always_redraw(lambda: Dot(ax2.c2p(ang.get_value(), np.cos(ang.get_value())), color=C_H))
        self.play(FadeOut(t1), Create(ax2), FadeIn(xl), FadeIn(yl), FadeIn(ticks), FadeIn(curve), FadeIn(dt))
        self.play(ang.animate.set_value(TAU), run_time=6, rate_func=linear)
        notes = VGroup(
            CT(r"$\alpha=0$：沿 $\nabla u$，增长最快，最大值 $|\nabla u|$", 24, C_HL),
            CT(r"$\alpha=\pi/2$：沿等值线，$\partial u/\partial l=0$", 24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(RIGHT * 3.3 + UP * 1.6)
        fitw(notes, 6.6)
        self.play(FadeIn(notes))
        self.wait(3)
