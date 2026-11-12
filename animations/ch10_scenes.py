"""第 10 章 无线信道、电磁干扰与电磁兼容 —— 补充 manim 动画源码（LaTeX 排版）.

渲染（输出 docs/assets/videos/C10_*.mp4，封面 docs/assets/posters/C10_*.jpg）：
    cd animations && manim -qm --disable_caching ch10_scenes.py C10_Friis（或 tools/render_videos.sh ch10_scenes.py）
场景：C10_TwoRay、C10_Ionosphere、C10_Multipath、C10_Shielding（原在 ch7_10_scenes.py），
      C10_Friis（自由空间损耗/弗里斯公式）、C10_Doppler（多普勒与快衰落）、
      C10_Fresnel（菲涅耳区与刃形绕射）、C10_Coupling（干扰的耦合途径与对策）。
"""
import numpy as np

from common import *  # noqa: F401,F403
from fieldtools import fitw

C_U = YELLOW
C_I = TEAL
C_INC = GOLD
C_REF = BLUE_C


def poly(points, color=WHITE, sw=3, opacity=1.0):
    m = VMobject(stroke_color=color, stroke_width=sw, stroke_opacity=opacity)
    m.set_points_as_corners(points)
    return m


def note(s, size=22, color=WHITE, w=13.2):
    t = fitw(CT(s, size, color), w)
    return t


# --------------------------------------------------------------------------
# 10.2.1 自由空间：能量按球面扩散，P_r ∝ 1/r^2，-20 dB/十倍程
# --------------------------------------------------------------------------
class C10_Friis(Scene):
    def construct(self):
        title = fitw(title_bar(r"自由空间传输损耗：功率在球面上摊薄，$S=\dfrac{P_{\mathrm{in}}G_t}{4\pi r^2}$"), 13.6)
        self.play(FadeIn(title))
        # 左：球面波前 + 固定有效面积的接收天线
        O = np.array([-5.6, -0.6, 0])
        tx = VGroup(Dot(O, color=C_HL, radius=0.09), CT("发射", 20, C_HL).next_to(O, DOWN, buff=0.12))
        self.play(FadeIn(tx))
        fronts = VGroup(*[Arc(radius=r, start_angle=-0.75, angle=1.5, arc_center=O, color=C_E, stroke_width=2,
                              stroke_opacity=0.8) for r in (0.8, 1.6, 2.4, 3.2, 4.0)])
        self.play(LaggedStart(*[Create(a) for a in fronts], lag_ratio=0.25), run_time=2.5)
        r = ValueTracker(1.6)
        ae = 0.7   # 接收天线口径（屏幕长度，固定）

        def rx():
            p = O + RIGHT * r.get_value()
            bar = Line(p + UP * ae / 2, p + DOWN * ae / 2, color=TEAL, stroke_width=7)
            cone = Polygon(O, p + UP * ae / 2, p + DOWN * ae / 2, stroke_width=0, fill_color=TEAL, fill_opacity=0.25)
            return VGroup(cone, bar)

        rxm = always_redraw(rx)
        ael = CT(r"接收天线有效面积 $A_e=\dfrac{\lambda^2G_r}{4\pi}$ 固定", 20, TEAL).move_to([-3.6, -3.0, 0])
        self.play(FadeIn(rxm), FadeIn(ael))
        fl = CT(r"截获的立体角 $\propto 1/r^2$：$P_r/P_r(r_0)=$", 20)
        fv = DecimalNumber(1.0, num_decimal_places=3, font_size=26)
        frac = VGroup(fl, fv).arrange(RIGHT, buff=0.12).move_to([-3.6, 2.35, 0])
        fv.add_updater(lambda m: m.set_value(1 / (r.get_value() / 0.8) ** 2))
        rl_ = MT(r"r/r_0=", 22, TEAL)
        rv = DecimalNumber(2.0, num_decimal_places=1, font_size=24, color=TEAL)
        rlab = VGroup(rl_, rv).arrange(RIGHT, buff=0.08)
        rlab.add_updater(lambda m: m.move_to(O + RIGHT * r.get_value() + UP * (ae / 2 + 0.3)))
        rv.add_updater(lambda m: m.set_value(r.get_value() / 0.8))
        self.play(FadeIn(frac), FadeIn(rlab))
        self.play(r.animate.set_value(4.0), run_time=4, rate_func=smooth)
        self.play(r.animate.set_value(0.8), run_time=2)
        self.play(r.animate.set_value(3.2), run_time=2)
        # 右：P_r (dBm) vs lg r
        ax0 = Axes(x_range=[0, 2, 1], y_range=[0, 60, 10], x_length=5.2, y_length=4.2,
                   axis_config={"stroke_width": 1.5, "include_tip": False}).move_to([3.6, -0.4, 0])

        class _A:   # 物理坐标 (lg r, P_r/dBm) -> 屏幕
            x_axis, y_axis = ax0.x_axis, ax0.y_axis

            @staticmethod
            def c2p(x, y):
                return ax0.c2p(x + 1, max(y, -90) + 90)

        ax = _A
        xt = VGroup(*[MT(s_, 18, GREY_B).next_to(ax.c2p(k, -90), DOWN, buff=0.1) for k, s_ in ((-1, "0.1"), (0, "1"), (1, "10"))])
        yt = VGroup(*[MT(str(v), 18, GREY_B).next_to(ax.c2p(-1, v), LEFT, buff=0.08) for v in (-90, -70, -50, -30)])
        xl = CT(r"$r$/km（对数）", 18, GREY_B).next_to(ax.x_axis, DOWN, buff=0.45)
        yl = CT(r"$P_r$/dBm", 18, GREY_B).next_to(ax.y_axis, UP, buff=0.1)
        cond = CT(r"$P_{\mathrm{in}}=1$ W，$G_t=G_r=1$，$f=900$ MHz", 18).next_to(ax0, UP, buff=0.55)
        self.play(Create(ax0), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), FadeIn(cond))

        def Pr(lgr):
            return 30 - (32.45 + 20 * np.log10(900) + 20 * lgr)

        fs = poly([ax.c2p(x, Pr(x)) for x in np.linspace(-1, 1, 60)], C_E, 4)
        self.play(Create(fs), run_time=2)
        p1 = Dot(ax.c2p(0, Pr(0)), color=C_HL)
        p1l = MT(r"-61.5\ \mathrm{dBm}", 20, C_HL).next_to(p1, RIGHT, buff=0.12)
        self.play(FadeIn(p1), FadeIn(p1l))
        slope = CT(r"距离 $\times10$：$-20$ dB", 20, C_E).next_to(ax.c2p(0.55, Pr(0.5)), UR, buff=0.2)
        self.play(FadeIn(slope))
        formula = MT(r"L_{bf}=\Big(\frac{4\pi r}{\lambda}\Big)^2\ \Rightarrow\ L_{bf}=32.45+20\lg f_{\mathrm{MHz}}+20\lg r_{\mathrm{km}}\ \mathrm{dB}", 28)
        fb = boxed(formula).move_to([0, -3.3, 0])
        self.play(FadeOut(ael), FadeIn(fb))
        self.wait(1)
        tworay = poly([ax.c2p(x, Pr(x) if x < 0.3 else Pr(0.3) - 40 * (x - 0.3)) for x in np.linspace(-1, 1, 80)], C_REF, 3)
        tl = CT(r"两径模型（10.3.3）远区：$-40$ dB/十倍程", 18, C_REF).next_to(ax.c2p(0.3, -88), UP, buff=0.05).shift(LEFT * 0.9)
        self.play(Create(DashedVMobject(tworay, num_dashes=40)), FadeIn(tl), run_time=2)
        msg = note(r"自由空间没有吸收：损耗只是能量扩散到更大的球面上，$A_e\propto\lambda^2$ 使 $L_{bf}$ 随 $f^2$ 增大", 22, C_HL)
        msg.next_to(title, DOWN, buff=0.12)
        self.play(FadeIn(msg))
        self.wait(3)


# --------------------------------------------------------------------------
# 10.2.2 衰落：多普勒频移 f_D=(v/λ)cosθ，以及驻波场中的“空间衰落→时间衰落”
# --------------------------------------------------------------------------
class C10_Doppler(Scene):
    def construct(self):
        title = fitw(title_bar(r"多普勒频移与快衰落：接收机穿过干涉图样，$f_D=\dfrac{v}{\lambda}\cos\theta$"), 13.6)
        self.play(FadeIn(title))
        # 第一段：平面波从斜方向入射，接收机向右运动
        lam = 1.0
        th = ValueTracker(50 * DEGREES)
        t = ValueTracker(0.0)
        box = Rectangle(width=7.0, height=4.2, color=GREY_D, stroke_width=1.5).move_to([-2.8, -0.3, 0])
        c = box.get_center()

        # 用裁剪方式简化：手工计算线段与矩形的交
        def clip(p, d, w=3.5, h=2.1):
            # 线 p + s d，求与 |x-cx|<=w, |y-cy|<=h 的交段
            s0, s1 = -1e9, 1e9
            for i, lim in ((0, w), (1, h)):
                if abs(d[i]) < 1e-9:
                    if abs(p[i] - c[i]) > lim:
                        return None
                    continue
                a = (c[i] - lim - p[i]) / d[i]
                b = (c[i] + lim - p[i]) / d[i]
                s0, s1 = max(s0, min(a, b)), min(s1, max(a, b))
            if s0 >= s1:
                return None
            return p + s0 * d, p + s1 * d

        def crests2():
            g = VGroup()
            a = th.get_value()
            k = np.array([-np.cos(a), -np.sin(a), 0])   # 波传播方向：从右上方射来
            n_ = np.array([-k[1], k[0], 0])
            ph = (t.get_value() * 0.8) % 0.8
            for m in range(-8, 9):
                p = c + k * (m * 0.8 + ph)
                r = clip(p, n_)
                if r is not None:
                    g.add(Line(r[0], r[1], color=C_E, stroke_width=2.5, stroke_opacity=0.7))
            return g

        waves = always_redraw(crests2)
        car_x = lambda: -5.6 + 0.7 * t.get_value()
        car = always_redraw(lambda: VGroup(
            RoundedRectangle(width=0.7, height=0.35, corner_radius=0.08, color=TEAL, fill_opacity=0.9).move_to([car_x(), -0.3, 0]),
            Arrow([car_x() + 0.35, -0.3, 0], [car_x() + 1.1, -0.3, 0], buff=0, color=TEAL, stroke_width=4)))
        kar = always_redraw(lambda: Arrow([0.3, 1.4, 0], [0.3 - 0.9 * np.cos(th.get_value()), 1.4 - 0.9 * np.sin(th.get_value()), 0],
                                          buff=0, color=C_HL, stroke_width=4))
        self.play(Create(box), FadeIn(waves), FadeIn(car), FadeIn(kar))
        eq = VGroup(MT(r"f'=f+\frac{v}{\lambda}\cos\theta", 32),
                    CT(r"$\theta$：运动方向与来波方向（反向）夹角", 20, GREY_B),
                    CT(r"迎着波走 $\cos\theta>0$：单位时间多碰到波峰，$f'$ 升高", 20),
                    CT(r"例：$v=30$ m/s，$f=900$ MHz", 20, C_HL),
                    MT(r"f_m=\frac{v}{\lambda}=\frac{30}{1/3}=90\ \mathrm{Hz}", 28, C_HL)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        eq.move_to([4.4, 0.2, 0])
        self.play(FadeIn(eq))
        self.play(t.animate.set_value(6), run_time=6, rate_func=linear)
        self.play(FadeOut(waves), FadeOut(car), FadeOut(kar), FadeOut(box), FadeOut(eq))

        # 第二段：直射 + 反射（相向两波）→ 驻波，移动接收机看到周期 1/(2 f_m) 的衰落
        sub = note(r"两列相向的波（如直射波与建筑物反射波）叠成驻波（第 6 章）：$|E|=2E_0|\cos kx|$，深谷间隔 $\lambda/2$", 22)
        sub.next_to(title, DOWN, buff=0.15)
        self.play(FadeIn(sub))
        ax = Axes(x_range=[0, 3, 0.5], y_range=[-2.2, 2.2, 1], x_length=11, y_length=2.4,
                  axis_config={"stroke_width": 1.2, "include_tip": False, "include_ticks": False}).move_to([0, 0.85, 0])
        xl = CT(r"$x/\lambda$", 18, GREY_B).next_to(ax.x_axis, RIGHT, buff=0.1)
        self.play(Create(ax), FadeIn(xl))
        tt = ValueTracker(0.0)
        k = 2 * np.pi
        inst = always_redraw(lambda: poly([ax.c2p(x, 2 * np.cos(k * x) * np.cos(2 * np.pi * tt.get_value())) for x in np.linspace(0, 3, 240)], C_E, 3))
        env = VGroup(poly([ax.c2p(x, 2 * abs(np.cos(k * x))) for x in np.linspace(0, 3, 240)], GREY_B, 2),
                     poly([ax.c2p(x, -2 * abs(np.cos(k * x))) for x in np.linspace(0, 3, 240)], GREY_B, 2))
        self.add(inst)
        self.play(tt.animate.set_value(2), run_time=3, rate_func=linear)
        self.play(Create(env))
        xr = ValueTracker(0.05)
        rxd = always_redraw(lambda: Dot(ax.c2p(xr.get_value(), 2 * abs(np.cos(k * xr.get_value()))), color=TEAL, radius=0.09))
        # 下方：接收电平 dB vs 时间
        ax2 = Axes(x_range=[0, 3, 0.5], y_range=[-30, 8, 10], x_length=11, y_length=1.9,
                   axis_config={"stroke_width": 1.2, "include_tip": False, "include_ticks": False}).move_to([0, -1.75, 0])
        yl2 = CT(r"接收电平/dB", 18, GREY_B).next_to(ax2.y_axis, UP, buff=0.05)
        xl2 = CT(r"时间 $t=x/v$", 18, GREY_B).next_to(ax2.x_axis, RIGHT, buff=0.1)
        zero = DashedLine(ax2.c2p(0, 0), ax2.c2p(3, 0), color=GREY_D, stroke_width=1)

        def lev(x):
            return max(20 * np.log10(max(2 * abs(np.cos(k * x)), 1e-3)), -30)

        trace = always_redraw(lambda: poly([ax2.c2p(x, lev(x)) for x in np.linspace(0.05, max(xr.get_value(), 0.06), 400)], TEAL, 3))
        self.play(Create(ax2), FadeIn(yl2), FadeIn(xl2), Create(zero), FadeIn(rxd))
        self.add(trace)
        self.play(xr.animate.set_value(2.95), tt.animate.set_value(30), run_time=9, rate_func=linear)
        res = note(r"空间上每走 $\lambda/2$ 一个深谷 $\Rightarrow$ 时间上衰落周期 $\dfrac{\lambda}{2v}=\dfrac{1}{2f_m}$；"
                   r"$f_m=90$ Hz 时约每 5.6 ms 一次", 22, C_HL)
        res.move_to([0, -3.35, 0])
        self.play(FadeIn(BackgroundRectangle(res, fill_opacity=0.85)), FadeIn(res))
        self.wait(3)


# --------------------------------------------------------------------------
# 10.3 视距传播的“余隙”：第一菲涅耳区与刃形绕射损耗
# --------------------------------------------------------------------------
def knife_loss(v):
    """ITU-R P.526 近似：刃形绕射损耗 J(ν)（dB），ν>-0.78 时有效，否则取 0。"""
    if v <= -0.78:
        return 0.0
    return 6.9 + 20 * np.log10(np.sqrt((v - 0.1) ** 2 + 1) + v - 0.1)


class C10_Fresnel(Scene):
    def construct(self):
        title = fitw(title_bar(r"第一菲涅耳区：$F_1=\sqrt{\dfrac{\lambda d_1d_2}{d}}$，保持 $0.6F_1$ 的余隙才算“视距”"), 13.6)
        self.play(FadeIn(title))
        T = np.array([-5.6, 0.8, 0])
        R = np.array([5.6, 0.8, 0])
        D = R[0] - T[0]
        tx = VGroup(Dot(T, color=C_HL, radius=0.09), CT("发射", 18, C_HL).next_to(T, LEFT, buff=0.1))
        rx = VGroup(Dot(R, color=TEAL, radius=0.09), CT("接收", 18, TEAL).next_to(R, RIGHT, buff=0.1))
        los = Line(T, R, color=C_E, stroke_width=3)
        self.play(FadeIn(tx), FadeIn(rx), Create(los))
        # 椭圆：r1+r2 = d + nλ/2（屏幕放大 λ 显示）
        lam_s = 0.25

        def zone(n, color, op):
            a = (D + n * lam_s / 2) / 2
            b = np.sqrt(a ** 2 - (D / 2) ** 2)
            e = Ellipse(width=2 * a, height=2 * b, color=color, stroke_width=2).move_to((T + R) / 2)
            e.set_fill(color, opacity=op)
            return e

        z1 = zone(1, BLUE_C, 0.18)
        z2 = zone(2, BLUE_E, 0.06)
        z3 = zone(3, BLUE_E, 0.03)
        # 经过椭圆上某点的折线：多走 λ/2
        a1 = (D + lam_s / 2) / 2
        b1 = np.sqrt(a1 ** 2 - (D / 2) ** 2)
        P = (T + R) / 2 + UP * b1
        bent = VGroup(Line(T, P, color=C_REF, stroke_width=3), Line(P, R, color=C_REF, stroke_width=3))
        bl = MT(r"r_1+r_2=d+\frac{\lambda}{2}", 26, C_REF).next_to(P, UP, buff=0.12)
        self.play(Create(bent), FadeIn(bl))
        self.play(FadeIn(z1), FadeIn(z2), FadeIn(z3))
        zl = CT(r"程差 $<\lambda/2$ 的次级波源所在区域 = 第一菲涅耳区（贡献主要能量）", 20).move_to([0, -0.6, 0])
        self.play(FadeIn(zl))
        self.wait(1.5)
        fr = MT(r"F_1=\sqrt{\frac{\lambda d_1d_2}{d}}\ \xrightarrow{\ d_1=d_2=d/2\ }\ \frac12\sqrt{\lambda d}", 28)
        ex = CT(r"例：$f=6$ GHz（$\lambda=5$ cm），$d=40$ km：路径中点 $F_1=22.4$ m", 20, C_HL)
        info = VGroup(fr, ex).arrange(DOWN, buff=0.2).move_to([0, -1.6, 0])
        self.play(FadeIn(info))
        self.wait(2)
        self.play(FadeOut(info), FadeOut(zl), FadeOut(bent), FadeOut(bl), FadeOut(z2), FadeOut(z3))
        # 刃形障碍升起
        h = ValueTracker(-2.0)   # 以 F1 为单位：障碍顶点相对视线的高度 h/F1
        mid = (T + R) / 2

        def knife():
            top = mid + UP * h.get_value() * b1
            base_y = -1.2
            tri = Polygon([mid[0] - 0.35, base_y, 0], [mid[0] + 0.35, base_y, 0], top, color=GREY_B, fill_color=GREY_D, fill_opacity=1, stroke_width=2)
            return tri

        kn = always_redraw(knife)
        ground = Line([-6.8, -1.2, 0], [6.8, -1.2, 0], color=GREY_A, stroke_width=3)
        self.play(FadeOut(los), Create(ground), FadeIn(kn))
        self.add(los)
        self.bring_to_front(los, tx, rx)
        # 右下：损耗曲线
        axf = Axes(x_range=[0, 4, 1], y_range=[0, 24, 6], x_length=5.4, y_length=2.1,
                   axis_config={"stroke_width": 1.2, "include_tip": False}).move_to([2.6, -2.75, 0])

        class _B:
            x_axis, y_axis = axf.x_axis, axf.y_axis

            @staticmethod
            def c2p(x, y):
                return axf.c2p(x + 2, y + 2)

        ax = _B
        xl = CT(r"$h/F_1$", 18, GREY_B).next_to(ax.x_axis, RIGHT, buff=0.1)
        yl = CT(r"附加损耗/dB", 18, GREY_B).next_to(ax.y_axis, UP, buff=0.05)
        xt = VGroup(*[MT(str(k_), 16, GREY_B).next_to(ax.c2p(k_, -2), DOWN, buff=0.06) for k_ in (-2, -1, 0, 1, 2)])
        yt = VGroup(*[MT(str(k_), 16, GREY_B).next_to(ax.c2p(-2, k_), LEFT, buff=0.06) for k_ in (0, 6, 12, 18)])
        self.play(Create(axf), FadeIn(xl), FadeIn(yl), FadeIn(xt), FadeIn(yt))
        sq2 = np.sqrt(2)   # ν = √2 h/F1

        cur = always_redraw(lambda: poly([ax.c2p(x, knife_loss(sq2 * x)) for x in np.linspace(-2, max(h.get_value(), -1.99), 200)], C_HL, 3))
        dot = always_redraw(lambda: Dot(ax.c2p(h.get_value(), knife_loss(sq2 * h.get_value())), color=C_HL))
        hv = DecimalNumber(-2.0, num_decimal_places=2, include_sign=True, font_size=26)
        jv = DecimalNumber(0.0, num_decimal_places=1, font_size=26, color=C_HL)
        rd = VGroup(MT(r"h/F_1=", 24), hv, MT(r"\quad J=", 24), jv, MT(r"\mathrm{dB}", 24)).arrange(RIGHT, buff=0.08).move_to([-3.6, -2.4, 0])
        hv.add_updater(lambda m: m.set_value(h.get_value()))
        jv.add_updater(lambda m: m.set_value(knife_loss(sq2 * h.get_value())))
        nu = MT(r"\nu=h\sqrt{\frac{2}{\lambda}\Big(\frac{1}{d_1}+\frac{1}{d_2}\Big)}=\sqrt2\,\frac{h}{F_1}", 24).move_to([-3.6, -3.4, 0])
        self.add(cur, dot)
        self.play(FadeIn(rd), FadeIn(nu))
        self.play(h.animate.set_value(-0.6), run_time=3, rate_func=linear)
        m1 = CT(r"余隙 $\ge0.6F_1$：几乎无附加损耗（可按自由空间计算）", 20, GREEN_B).next_to(title, DOWN, buff=0.15)
        self.play(FadeIn(m1))
        self.wait(1)
        self.play(h.animate.set_value(0.0), run_time=2.5, rate_func=linear)
        m2 = CT(r"刚好挡到视线（掠过）：损耗约 6 dB —— 能“看见”不等于“畅通”", 20, C_HL).move_to(m1)
        self.play(FadeOut(m1), FadeIn(m2))
        self.wait(1)
        self.play(h.animate.set_value(2.0), run_time=3.5, rate_func=linear)
        m3 = CT(r"视线被遮挡后仍有绕射波，但损耗迅速增大；频率越高 $F_1$ 越小，越难绕过障碍", 20, C_HL).move_to(m1)
        fitw(m3, 13.2)
        self.play(FadeOut(m2), FadeIn(m3))
        self.wait(3)


# --------------------------------------------------------------------------
# 10.7.4 干扰的三条途径与对策
# --------------------------------------------------------------------------
class C10_Coupling(Scene):
    def construct(self):
        title = fitw(title_bar(r"干扰三要素：干扰源 $\to$ 耦合途径 $\to$ 敏感电路"), 13.6)
        self.play(FadeIn(title))
        # 干扰源回路（左）与敏感回路（右），共用地线
        gy = -2.3
        src = Rectangle(width=2.6, height=2.0, color=C_POS, stroke_width=4).move_to([-3.6, -0.6, 0])
        vic = Rectangle(width=2.6, height=2.0, color=C_NEG, stroke_width=4).move_to([3.6, -0.6, 0])
        sl = CT(r"干扰源回路 $u_s,\ i_s$", 20, C_POS).next_to(src, UP, buff=0.15)
        vl = CT(r"敏感回路 $R$", 20, C_NEG).next_to(vic, UP, buff=0.15)
        gnd = Line([-5.6, gy, 0], [5.6, gy, 0], color=GREY_B, stroke_width=5)
        gl = CT(r"公共地线（阻抗 $Z_g$）", 18, GREY_B).next_to(gnd, DOWN, buff=0.1)
        legs = VGroup(Line(src.get_corner(DL), [src.get_left()[0], gy, 0], color=C_POS, stroke_width=3),
                      Line(vic.get_corner(DR), [vic.get_right()[0], gy, 0], color=C_NEG, stroke_width=3))
        zg = Rectangle(width=0.8, height=0.3, color=GREY_B, fill_color=BLACK, fill_opacity=1).move_to([0, gy, 0])
        self.play(Create(src), Create(vic), FadeIn(sl), FadeIn(vl), Create(gnd), Create(legs), FadeIn(zg), FadeIn(gl))
        cap_y = 0.2
        # 1 电容耦合
        ecap = VGroup(*[DashedLine([src.get_right()[0], cap_y + dy, 0], [vic.get_left()[0], cap_y + dy, 0], color=C_E, stroke_width=2)
                        for dy in (0.0, 0.2)])
        el = VGroup(CT(r"1. 电容耦合（电场）", 22, C_E), MT(r"u_n\approx \je\omega C_mR\,u_s", 26, C_E)).arrange(DOWN, buff=0.1)
        el.move_to([0, 1.45, 0])
        self.play(Create(ecap), FadeIn(el))
        self.play(*[ApplyMethod(l.set_stroke, {"opacity": 0.2}, rate_func=there_and_back) for l in ecap], run_time=1.5)
        self.wait(1)
        # 2 电感耦合
        loops = VGroup(*[Ellipse(width=w, height=w * 0.55, color=C_H, stroke_width=2).move_to([0, -0.9, 0]) for w in (4.2, 5.6)])
        ml = VGroup(CT(r"2. 电感耦合（磁场）", 22, C_H), MT(r"u_n=\je\omega M\,i_s", 26, C_H)).arrange(DOWN, buff=0.1).move_to([0, -0.9, 0])
        self.play(Create(loops), FadeIn(ml))
        self.wait(1.2)
        # 3 传导（公共阻抗）
        pulse = Dot([-5.0, gy, 0], color=C_HL, radius=0.11)
        cl = VGroup(CT(r"3. 传导（公共阻抗）", 22, C_HL), MT(r"u_n=Z_g\,i_s", 26, C_HL)).arrange(RIGHT, buff=0.3).move_to([0, gy - 0.85, 0])
        self.play(FadeOut(gl), FadeIn(cl))
        self.play(pulse.animate.move_to([0, gy, 0]), run_time=1.2)
        self.play(Flash(zg, color=C_HL), run_time=0.8)
        self.play(FadeOut(pulse))
        # 4 辐射
        waves = VGroup(*[Arc(radius=r, start_angle=0.25, angle=0.7, arc_center=src.get_corner(UR), color=PURPLE_B, stroke_width=3)
                         for r in (0.5, 0.9, 1.3)])
        rl = CT(r"4. 辐射（远场）", 22, PURPLE_B).move_to([-0.3, 2.35, 0])
        self.play(LaggedStart(*[Create(w) for w in waves], lag_ratio=0.3), FadeIn(rl))
        self.wait(1.5)
        # 对策
        fix = VGroup(
            CT(r"对策：1、2. 近场 $\to$ 屏蔽（静电屏蔽须接地；低频磁场用高 $\mu$）、拉开距离、减小回路面积/双绞", 20),
            CT(r"3. 传导 $\to$ 单点/混合接地，分开信号地与功率地，电源滤波", 20),
            CT(r"4. 辐射 $\to$ 良导体屏蔽体 + 处理孔缝；安全系数 $m=P_s-P_I>0$", 20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        fb = boxed(fitw(fix, 12.6))
        self.play(FadeOut(VGroup(ecap, el, loops, ml, waves, rl)))
        shield = DashedVMobject(SurroundingRectangle(vic, buff=0.25, color=GREEN_B, stroke_width=4), num_dashes=40)
        sh_l = CT("接地屏蔽盒", 18, GREEN_B).next_to(shield, RIGHT, buff=0.05).rotate(PI / 2)
        sgnd = Line(shield.get_bottom(), [shield.get_bottom()[0], gy, 0], color=GREEN_B, stroke_width=3)
        self.play(Create(shield), Create(sgnd), FadeIn(sh_l), vl.animate.next_to(shield, UP, buff=0.1))
        fb.move_to([0, 2.2, 0])
        self.play(FadeIn(fb))
        self.wait(4)


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

        pc = np.array([-4.0, -0.3, 0])
        S = 1.25

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
        x2 = CT(r"移动距离 $/\lambda$", 20, GREY_B).next_to(ax2.c2p(2.0, -30), DOWN, buff=0.42)
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
        sl = CT("良导体屏蔽板（厚 $t$）", 20).next_to(slab, UP, buff=0.4)
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
        l2 = CT(r"入射 $+$ 反射：表面处 $E\approx0$（$\Gamma\approx-1$，反射损耗 $\mathrm{SE}_r$）", 20, C_E).move_to([-3.4, yc - 2.45, 0])
        self.play(FadeIn(l2), t.animate.set_value(3.0), run_time=3, rate_func=linear)
        self.add(ins, out)
        l3 = CT(r"板内（放大显示）：每走 $\delta$ 衰减到 $1/\mathrm e$（吸收损耗 $\mathrm{SE}_a$）", 20, C_HL).move_to([2.6, yc - 2.95, 0])
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
        fitw(note, 13.0).move_to([0, 0.95, 0])
        self.play(FadeIn(note))
        self.wait(3.5)
