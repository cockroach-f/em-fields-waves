"""第 6 章 平面电磁波 —— manim 动画源码（LaTeX 排版）.

三维场景的坐标约定：manim 的 X 轴 = 传播方向 z；manim 的 Z 轴（竖直）= x；manim 的 -Y 轴 = y，
于是 (a_x, a_y, a_z) = (Z_m, -Y_m, X_m) 仍为右手系。
"""
import numpy as np

from common import *  # noqa: F401,F403
from fieldtools import *  # noqa: F401,F403


def P3(x, y, z):
    """物理坐标 (x, y, z) -> manim 坐标."""
    return np.array([z, -y, x])


def axes3(L=6.0, h=1.6):
    g = VGroup(
        Line(P3(0, 0, -0.3), P3(0, 0, L), color=GREY_B, stroke_width=2),
        Line(P3(-h, 0, 0), P3(h, 0, 0), color=GREY_B, stroke_width=2),
        Line(P3(0, -h, 0), P3(0, h, 0), color=GREY_B, stroke_width=2),
    )
    return g


# --------------------------------------------------------------------------
# 6.1 均匀平面波：E、H 同相、互相垂直、都垂直于传播方向
# --------------------------------------------------------------------------
class C6_PlaneWave(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=68 * DEGREES, theta=-62 * DEGREES, zoom=0.95)
        title = CT(r"均匀平面波：$\vv E=\ax E_0\cos(\omega t-kz)$，$\vv H=\ay\dfrac{E_0}{\eta}\cos(\omega t-kz)$，$\vv E\times\vv H$ 沿 $+z$", 30)
        fitw(title, 13.4).to_edge(UP, buff=0.2)
        self.add_fixed_in_frame_mobjects(title)
        self.play(FadeIn(title))
        L = 6.4
        shift = np.array([-3.2, 0, 0])
        ax = axes3(L).shift(shift)
        lz = MT("z", 30).move_to(P3(0, 0, L + 0.35) + shift)
        lx = MT("x", 30, C_E).move_to(P3(1.85, 0, 0) + shift)
        ly = MT("y", 30, C_H).move_to(P3(0, 1.85, 0) + shift)
        for m in (lz, lx, ly):
            self.add_fixed_orientation_mobjects(m)
        self.play(Create(ax), FadeIn(lz), FadeIn(lx), FadeIn(ly))
        k = 2 * PI / 3.2
        t = ValueTracker(0.0)
        zs = np.linspace(0, L, 49)

        def wave(comp):
            ph = t.get_value()
            g = VGroup()
            pts = []
            for z in zs:
                a = np.cos(ph - k * z)
                if comp == "E":
                    p = P3(1.3 * a, 0, z) + shift
                    g.add(Line(P3(0, 0, z) + shift, p, color=C_E, stroke_width=2))
                else:
                    p = P3(0, 1.0 * a, z) + shift
                    g.add(Line(P3(0, 0, z) + shift, p, color=C_H, stroke_width=2))
                pts.append(p)
            curve = VMobject(stroke_color=C_E if comp == "E" else C_H, stroke_width=4).set_points_smoothly(pts)
            g.add(curve)
            return g

        Ew = always_redraw(lambda: wave("E"))
        Hw = always_redraw(lambda: wave("H"))
        self.add(Ew, Hw)
        Sarr = Arrow3D(P3(0, 0, L + 0.1) + shift, P3(0, 0, L + 1.0) + shift, color=C_S, thickness=0.03)
        self.play(FadeIn(Sarr))
        info = VGroup(
            CT(r"$k=\omega\sqrt{\mu\varepsilon}=\dfrac{2\pi}{\lambda}$，$v_p=\dfrac{\omega}{k}=\dfrac{1}{\sqrt{\mu\varepsilon}}$", 24),
            CT(r"$\eta=\dfrac{E_x}{H_y}=\sqrt{\dfrac\mu\varepsilon}$，真空 $\eta_0=120\pi\approx377\ \Omega$", 24),
            CT(r"$\vv E$、$\vv H$ 同相，$w_e=w_m$", 24),
            CT(r"$\vv S_{\text{av}}=\az\dfrac{E_0^2}{2\eta}$（紫色箭头）", 24, C_S),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        fitw(info, 4.6).to_corner(DL, buff=0.35)
        self.add_fixed_in_frame_mobjects(info)
        self.play(t.animate.set_value(2 * PI), FadeIn(info[0]), run_time=4, rate_func=linear)
        self.play(t.animate.set_value(4 * PI), FadeIn(info[1]), FadeIn(info[2]), run_time=4, rate_func=linear)
        self.move_camera(phi=75 * DEGREES, theta=-30 * DEGREES, run_time=2,
                         added_anims=[t.animate.set_value(5 * PI)])
        self.play(t.animate.set_value(7 * PI), FadeIn(info[3]), run_time=4, rate_func=linear)
        self.wait(1)


# --------------------------------------------------------------------------
# 6.4 电磁波的极化
# --------------------------------------------------------------------------
class C6_Polarization(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=-58 * DEGREES, zoom=0.9)
        title = CT(r"极化：迎着传播方向看，固定点上 $\vv E$ 矢端随时间画出的轨迹", 30)
        fitw(title, 13).to_edge(UP, buff=0.2)
        self.add_fixed_in_frame_mobjects(title)
        self.play(FadeIn(title))
        L = 6.0
        shift = np.array([-3.6, 0, 0])
        ax = axes3(L).shift(shift)
        lz = MT("z", 30).move_to(P3(0, 0, L + 0.35) + shift)
        lx = MT("x", 28).move_to(P3(1.8, 0, 0) + shift)
        ly = MT("y", 28).move_to(P3(0, 1.8, 0) + shift)
        for m in (lz, lx, ly):
            self.add_fixed_orientation_mobjects(m)
        self.add(ax, lz, lx, ly)
        k = 2 * PI / 3.0
        t = ValueTracker(0.0)
        zs = np.linspace(0, L, 121)
        # 2D 小窗：迎着波看（x 向右、y 向上，波朝观察者传来）
        C2 = np.array([4.3, -1.0, 0])
        R2 = 1.25
        box = Square(side_length=3.0, color=GREY_D, stroke_width=1.5).move_to(C2)
        cx = Line(C2 + LEFT * 1.4, C2 + RIGHT * 1.4, color=GREY_C, stroke_width=1.5)
        cy = Line(C2 + DOWN * 1.4, C2 + UP * 1.4, color=GREY_C, stroke_width=1.5)
        bl = CT(r"$z=0$ 处，迎着波看", 22, GREY_A).next_to(box, UP, buff=0.08)
        bx = MT("x", 22, GREY_B).next_to(cx, RIGHT, buff=0.04)
        by = MT("y", 22, GREY_B).next_to(cy, UP, buff=0.04)
        inset = VGroup(box, cx, cy, bl, bx, by)
        self.add_fixed_in_frame_mobjects(inset)
        self.play(FadeIn(inset))
        cases = [
            (1.0, 0.0, 0.0, r"线极化：$\vv E=(\ax+\ay)E_0\cos(\omega t-kz)$", r"两分量同相（或反相）"),
            (1.0, 1.0, -PI / 2, r"右旋圆极化：$\vv E=(\ax-\je\ay)E_0\mathrm e^{-\je kz}$", r"等幅、$E_y$ 滞后 $90^\circ$：拇指指向传播方向，四指为旋转方向"),
            (1.0, 1.0, PI / 2, r"左旋圆极化：$\vv E=(\ax+\je\ay)E_0\mathrm e^{-\je kz}$", r"等幅、$E_y$ 超前 $90^\circ$：旋转方向与右旋相反"),
            (1.0, 0.5, -PI / 3, r"椭圆极化：$E_{ym}/E_{xm}=0.5$，相差 $60^\circ$", r"一般情形：轨迹为椭圆，旋向由相位差的符号决定"),
        ]
        old = None
        for i, (ex, ey, dph, lab, sub) in enumerate(cases):
            if i == 0:
                ex, ey = 0.75, 0.75
            def Ef(z, ph, ex=ex, ey=ey, dph=dph):
                return ex * np.cos(ph - k * z), ey * np.cos(ph - k * z + dph)

            def helix(ex=ex, ey=ey, dph=dph):
                ph = t.get_value()
                pts = [P3(*(np.array(Ef(z, ph)) * 1.3), z) + shift for z in zs]
                g = VGroup(VMobject(stroke_color=C_E, stroke_width=3).set_points_smoothly(pts))
                for z in zs[::6]:
                    x, y = Ef(z, ph)
                    g.add(Line(P3(0, 0, z) + shift, P3(1.3 * x, 1.3 * y, z) + shift, color=C_E, stroke_width=1.5, stroke_opacity=0.6))
                x0, y0 = Ef(0, ph)
                g.add(Line(P3(0, 0, 0) + shift, P3(1.3 * x0, 1.3 * y0, 0) + shift, color=C_HL, stroke_width=6))
                return g

            def flat(ex=ex, ey=ey, dph=dph):
                ph = t.get_value()
                ts = np.linspace(0, TAU, 80)
                loc = VMobject(stroke_color=GREY_B, stroke_width=2).set_points_smoothly(
                    [C2 + R2 * np.array([ex * np.cos(s), ey * np.cos(s + dph), 0]) for s in ts])
                x0, y0 = Ef(0, ph)
                v = Arrow(C2, C2 + R2 * np.array([x0, y0, 0]), buff=0, color=C_HL, stroke_width=5, max_tip_length_to_length_ratio=0.2)
                return VGroup(loc, v)

            hx = always_redraw(helix)
            fl = always_redraw(flat)
            self.add_fixed_in_frame_mobjects(fl)
            txt = VGroup(CT(lab, 26, C_E), CT(sub, 22, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            fitw(txt, 8.0).to_corner(DL, buff=0.35)
            self.add_fixed_in_frame_mobjects(txt)
            if old is not None:
                for m in old:
                    m.clear_updaters()
                self.remove(*old)
            self.add(hx, fl)
            self.play(FadeIn(txt), run_time=0.5)
            self.play(t.animate.set_value(t.get_value() + 2 * TAU), run_time=5, rate_func=linear)
            old = (hx, fl, txt)
        self.wait(1)


# --------------------------------------------------------------------------
# 6.2–6.3 导电媒质：衰减、相位滞后、趋肤深度
# --------------------------------------------------------------------------
class C6_Lossy(Scene):
    def construct(self):
        title = title_bar(r"导电媒质中的平面波：$\vv E=\ax E_0\mathrm e^{-\alpha z}\cos(\omega t-\beta z)$，$\vv H$ 滞后 $\vv E$ 一个角度 $\psi$")
        fitw(title, 13.6)
        self.play(FadeIn(title))
        ax = Axes(x_range=[0, 3, 0.5], y_range=[-1.2, 1.2, 1], x_length=8.6, y_length=2.6,
                  axis_config={"stroke_width": 1.5, "include_ticks": False, "include_tip": False}).move_to(LEFT * 1.9 + UP * 0.7)
        zl = MT(r"z/\lambda", 24, GREY_B).next_to(ax.x_axis, RIGHT, buff=0.08)
        self.play(Create(ax), FadeIn(zl))
        t = ValueTracker(0.0)
        cases = [
            (0.05, 0.03, r"低损耗介质（$\sigma/\omega\varepsilon\ll1$）：$\alpha\approx\dfrac\sigma2\sqrt{\dfrac\mu\varepsilon}$，$\eta\approx\sqrt{\dfrac\mu\varepsilon}$，几乎不衰减"),
            (0.35, 0.25, r"一般导电媒质：$\gamma=\alpha+\je\beta=\je\omega\sqrt{\mu\varepsilon_c}$，$\varepsilon_c=\varepsilon-\je\dfrac\sigma\omega$"),
            (2 * PI / 1.0, PI / 4, r"良导体（$\sigma/\omega\varepsilon\gg1$）：$\alpha=\beta=\sqrt{\pi f\mu\sigma}$，$\psi=45^\circ$，一个波长内衰减到 $\mathrm e^{-2\pi}\approx0.2\%$"),
        ]
        old = None
        for i, (alpha, psi, txt) in enumerate(cases):
            # 以波长为单位：β=2π
            beta = 2 * PI
            a = alpha
            env = VGroup(ax.plot(lambda z: np.exp(-a * z), x_range=[0, 3, 0.01], color=GREY_B, stroke_width=1.5),
                         ax.plot(lambda z: -np.exp(-a * z), x_range=[0, 3, 0.01], color=GREY_B, stroke_width=1.5))
            env = DashedVMobject(env[0], num_dashes=50).add(*DashedVMobject(env[1], num_dashes=50))
            Ec = always_redraw(lambda a=a: ax.plot(lambda z: np.exp(-a * z) * np.cos(t.get_value() - beta * z), x_range=[0, 3, 0.005],
                                                   color=C_E, stroke_width=3))
            Hc = always_redraw(lambda a=a, psi=psi: ax.plot(lambda z: 0.7 * np.exp(-a * z) * np.cos(t.get_value() - beta * z - psi),
                                                            x_range=[0, 3, 0.005], color=C_H, stroke_width=3))
            parts = [env, Ec, Hc]
            dl = VGroup()
            if a > 0.2:
                d = 1 / a
                if d < 3:
                    dl = VGroup(DashedLine(ax.c2p(d, -1.2), ax.c2p(d, 1.2), color=C_HL, stroke_width=2),
                                MT(r"\delta=\frac1\alpha", 24, C_HL).next_to(ax.c2p(d, 1.2), UP, buff=0.05))
            cap = CT(txt, 24)
            fitw(cap, 13).move_to(DOWN * 1.35)
            if old is None:
                self.add(Ec, Hc)
                self.play(Create(env), FadeIn(cap), FadeIn(dl))
                leg = VGroup(CT(r"$E_x$", 24, C_E), CT(r"$\eta_0H_y$（缩放）", 24, C_H)).arrange(RIGHT, buff=0.4).next_to(ax, RIGHT, buff=0.2).shift(UP * 0.8)
                fitw(leg, 3.6)
                self.play(FadeIn(leg))
            else:
                for m in old[1:3]:
                    m.clear_updaters()
                self.remove(*old[1:3])
                self.add(Ec, Hc)
                self.play(ReplacementTransform(old[0], env), FadeOut(old[3]), FadeIn(cap), FadeOut(old[4]), FadeIn(dl))
            self.play(t.animate.set_value(t.get_value() + 2 * TAU), run_time=5, rate_func=linear)
            old = (env, Ec, Hc, cap, dl)
        tb = VGroup(
            CT(r"铜（$\sigma=5.8\times10^7$ S/m）：$\delta=\dfrac{1}{\sqrt{\pi f\mu_0\sigma}}\approx\dfrac{66\ \text{mm}}{\sqrt{f/\text{Hz}}}$", 24),
            CT(r"50 Hz：9.3 mm　　1 MHz：66 μm　　1 GHz：2.1 μm", 24, C_HL),
            CT(r"高频电流只在导体表面薄层内流动——\textbf{趋肤效应}；表面电阻 $R_S=\dfrac{1}{\sigma\delta}$", 24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        fitw(tb, 12.5).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(tb))
        self.wait(3)


# --------------------------------------------------------------------------
# 6.5 色散与群速
# --------------------------------------------------------------------------
class C6_GroupVelocity(Scene):
    def construct(self):
        title = title_bar(r"色散与群速：两个相近频率叠加，载波以 $v_p=\omega/\beta$ 前进，包络以 $v_g=\dd\omega/\dd\beta$ 前进")
        fitw(title, 13.6)
        self.play(FadeIn(title))
        ax = Axes(x_range=[0, 20, 5], y_range=[-2.3, 2.3, 1], x_length=12, y_length=3.2,
                  axis_config={"stroke_width": 1.5, "include_ticks": False, "include_tip": False}).move_to(UP * 0.4)
        zl = MT("z", 26, GREY_B).next_to(ax.x_axis, RIGHT, buff=0.08)
        self.play(Create(ax), FadeIn(zl))
        b0, db = 4.0, 0.35
        w0, dw = 4.0, 0.175   # v_p = 1, v_g = 0.5（正常色散）
        t = ValueTracker(0.0)
        f = lambda z, tt: np.cos((w0 + dw) * tt - (b0 + db) * z) + np.cos((w0 - dw) * tt - (b0 - db) * z)
        envf = lambda z, tt: 2 * np.cos(dw * tt - db * z)
        wave = always_redraw(lambda: ax.plot(lambda z: f(z, t.get_value()), x_range=[0, 20, 0.01], color=C_E, stroke_width=2.5))
        env = always_redraw(lambda: VGroup(
            DashedVMobject(ax.plot(lambda z: abs(envf(z, t.get_value())), x_range=[0, 20, 0.02], color=C_HL, stroke_width=2.5), num_dashes=80),
            DashedVMobject(ax.plot(lambda z: -abs(envf(z, t.get_value())), x_range=[0, 20, 0.02], color=C_HL, stroke_width=2.5), num_dashes=80)))
        # 跟踪点：一个载波波峰（v_p）与一个包络峰（v_g）
        zc0 = 2 * PI / b0 * 1
        crest = always_redraw(lambda: Dot(ax.c2p((zc0 + w0 / b0 * t.get_value()) % 20, 0), color=C_E, radius=0.09).shift(UP * 1.9))
        zp0 = 0.0 + 2 * PI / db / 2 * 0  # 包络峰在 z=0
        epk = always_redraw(lambda: Triangle(color=C_HL, fill_opacity=1).scale(0.12).rotate(PI)
                            .move_to(ax.c2p(((dw / db) * t.get_value()) % (PI / db) + PI / db * 0, 2.25)))
        self.add(wave, env, crest, epk)
        leg = VGroup(CT(r"合成波（黄）　包络（橙虚线，▼ 跟踪包络峰）　● 跟踪一个载波波峰", 22)).next_to(ax, DOWN, buff=0.15)
        fitw(leg, 12)
        self.play(FadeIn(leg))
        self.play(t.animate.set_value(14), run_time=8, rate_func=linear)
        txt = VGroup(
            MT(r"\cos(\omega_1t-\beta_1z)+\cos(\omega_2t-\beta_2z)=2\cos(\Delta\omega\,t-\Delta\beta\,z)\cos(\omega_0t-\beta_0z)", 28),
            CT(r"图中 $v_p=1$，$v_g=0.5$：载波波峰从包络中“穿过”。信号（能量、信息）以群速传播", 24),
            CT(r"无耗理想介质中 $\beta=\omega\sqrt{\mu\varepsilon}$，$v_g=v_p$，无色散；导电媒质、等离子体（电离层，第 10 章）中 $v_p$ 随频率变化，产生色散", 22, GREY_A),
        ).arrange(DOWN, buff=0.18)
        fitw(txt, 13).to_edge(DOWN, buff=0.25)
        self.play(FadeIn(txt), t.animate.set_value(20), run_time=4, rate_func=linear)
        self.wait(2)


# --------------------------------------------------------------------------
# 6.6 垂直入射：驻波与行驻波
# --------------------------------------------------------------------------
class C6_Standing(Scene):
    def construct(self):
        title = title_bar(r"垂直入射：入射波 + 反射波 = 驻波（理想导体）或行驻波（介质分界面）")
        fitw(title, 13.6)
        self.play(FadeIn(title))
        ax = Axes(x_range=[-2, 1, 0.5], y_range=[-2.2, 2.2, 1], x_length=10.5, y_length=3.4,
                  axis_config={"stroke_width": 1.5, "include_ticks": False, "include_tip": False}).move_to(UP * 0.35)
        zl = MT(r"z/\lambda_1", 24, GREY_B).next_to(ax.x_axis, RIGHT, buff=0.08)
        wall = Rectangle(width=ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0], height=3.4, stroke_width=0, fill_color=GREY_D, fill_opacity=0.9)
        wall.move_to((ax.c2p(0, 0) + ax.c2p(1, 0)) / 2)
        wl = CT(r"理想导体", 24, GREY_A).move_to(wall)
        self.play(Create(ax), FadeIn(zl), FadeIn(wall), FadeIn(wl))
        t = ValueTracker(0.0)
        b1 = 2 * PI
        Ec = always_redraw(lambda: ax.plot(lambda z: 2 * np.sin(b1 * z) * np.sin(t.get_value()), x_range=[-2, 0, 0.005], color=C_E, stroke_width=3))
        Hc = always_redraw(lambda: ax.plot(lambda z: 1.4 * np.cos(b1 * z) * np.cos(t.get_value()), x_range=[-2, 0, 0.005], color=C_H, stroke_width=3))
        envE = DashedVMobject(ax.plot(lambda z: 2 * abs(np.sin(b1 * z)), x_range=[-2, 0, 0.005], color=C_E, stroke_width=1.5, stroke_opacity=0.5), num_dashes=90)
        self.add(Ec, Hc)
        self.play(FadeIn(envE))
        cap = VGroup(
            CT(r"$\vv E_1=-\ax\je2E_0\sin\beta z$，$\vv H_1=\ay\dfrac{2E_0}{\eta_1}\cos\beta z$：$\vv E$ 与 $\vv H$ 在时间、空间上都差 $90^\circ$", 24),
            CT(r"电场波节在导体表面及 $z=-n\lambda/2$ 处（磁场波腹），$\vv S_{\text{av}}=0$：能量不传播，只在电、磁之间交换", 22, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        fitw(cap, 13).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(cap))
        self.play(t.animate.set_value(3 * TAU), run_time=7, rate_func=linear)
        # 介质分界面
        Ec.clear_updaters(); Hc.clear_updaters()
        R, T = -1 / 3, 2 / 3   # 媒质 2：εr=4
        b2 = 2 * b1
        wall2 = Rectangle(width=wall.width, height=3.4, stroke_width=0, fill_color=C_NEG, fill_opacity=0.18).move_to(wall)
        wl2 = CT(r"媒质 2：$\varepsilon_r=4$", 22, C_NEG).move_to(wall).shift(UP * 1.4)
        t.set_value(0)

        def E1(z, tt):
            return np.cos(tt - b1 * z) + R * np.cos(tt + b1 * z)

        def E2(z, tt):
            return T * np.cos(tt - b2 * z)

        Ec2 = always_redraw(lambda: VGroup(ax.plot(lambda z: E1(z, t.get_value()), x_range=[-2, 0, 0.005], color=C_E, stroke_width=3),
                                           ax.plot(lambda z: E2(z, t.get_value()), x_range=[0, 1, 0.005], color=C_E, stroke_width=3)))
        env2 = VGroup(
            DashedVMobject(ax.plot(lambda z: abs(1 + R * np.exp(2j * b1 * z)), x_range=[-2, 0, 0.005], color=C_HL, stroke_width=2), num_dashes=90),
            DashedVMobject(ax.plot(lambda z: -abs(1 + R * np.exp(2j * b1 * z)), x_range=[-2, 0, 0.005], color=C_HL, stroke_width=2), num_dashes=90),
            DashedVMobject(ax.plot(lambda z: T, x_range=[0, 1, 0.01], color=C_HL, stroke_width=2), num_dashes=20),
            DashedVMobject(ax.plot(lambda z: -T, x_range=[0, 1, 0.01], color=C_HL, stroke_width=2), num_dashes=20))
        cap2 = VGroup(
            CT(r"$R=\dfrac{\eta_2-\eta_1}{\eta_2+\eta_1}=-\dfrac13$，$T=\dfrac{2\eta_2}{\eta_2+\eta_1}=\dfrac23$：媒质 1 中为行驻波，包络（橙）在 $1\pm|R|$ 之间", 24),
            CT(r"驻波比 $S=\dfrac{1+|R|}{1-|R|}=2$；$R<0$，分界面处是电场波节（最小点）；媒质 2 中波长减半", 22, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        fitw(cap2, 13).to_edge(DOWN, buff=0.35)
        self.play(FadeOut(Ec), FadeOut(Hc), FadeOut(envE), FadeOut(wall), FadeOut(wl), FadeIn(wall2), FadeIn(wl2),
                  ReplacementTransform(cap, cap2))
        self.add(Ec2)
        self.play(FadeIn(env2))
        self.play(t.animate.set_value(3 * TAU), run_time=8, rate_func=linear)
        self.wait(1)


# --------------------------------------------------------------------------
# 6.7 斜入射：斯涅尔定律、布儒斯特角、全反射
# --------------------------------------------------------------------------
def fresnel(t1, e1, e2):
    """书中约定：R_par=(η1cosθi-η2cosθt)/(η1cosθi+η2cosθt)，R_perp=(η2cosθi-η1cosθt)/(η2cosθi+η1cosθt)."""
    n1, n2 = np.sqrt(e1), np.sqrt(e2)
    s = n1 * np.sin(t1) / n2
    ct = np.sqrt(1 - s * s + 0j)
    ct = np.where(np.imag(ct) < 0, np.conj(ct), ct)
    ci = np.cos(t1)
    h1, h2 = 1 / n1, 1 / n2
    Rpar = (h1 * ci - h2 * ct) / (h1 * ci + h2 * ct)
    Rper = (h2 * ci - h1 * ct) / (h2 * ci + h1 * ct)
    return np.abs(Rpar), np.abs(Rper)


class C6_Oblique(Scene):
    def construct(self):
        title = title_bar(r"斜入射：$k_1\sin\theta_i=k_2\sin\theta_t$（斯涅尔定律），反射系数随入射角变化")
        fitw(title, 13.6)
        self.play(FadeIn(title))
        O = LEFT * 3.7 + DOWN * 0.3
        Lr = 2.6
        iface = Line(O + LEFT * 3.0, O + RIGHT * 3.0, color=GREY_A, stroke_width=3)
        normal = DashedLine(O + UP * 2.6, O + DOWN * 2.6, color=GREY_C, stroke_width=1.5)
        m1 = CT(r"媒质 1", 22, GREY_A).move_to(O + LEFT * 2.3 + UP * 2.3)
        m2 = CT(r"媒质 2", 22, GREY_A).move_to(O + LEFT * 2.3 + DOWN * 2.3)
        lower = Rectangle(width=6, height=2.7, stroke_width=0, fill_color=C_NEG, fill_opacity=0.15).move_to(O + DOWN * 1.35)
        self.play(FadeIn(lower), Create(iface), Create(normal), FadeIn(m1), FadeIn(m2))
        th = ValueTracker(30 * DEGREES)
        eps = [1.0, 4.0]

        def rays():
            e1, e2 = eps
            ti = th.get_value()
            s = np.sqrt(e1 / e2) * np.sin(ti)
            g = VGroup()
            di = np.array([np.sin(ti), -np.cos(ti), 0])
            g.add(Arrow(O - di * Lr, O, buff=0, color=C_E, stroke_width=5, max_tip_length_to_length_ratio=0.08))
            Rpa, Rpe = fresnel(np.array([ti]), e1, e2)
            rr = float(max(Rpa[0], Rpe[0]))
            dr = np.array([np.sin(ti), np.cos(ti), 0])
            g.add(Arrow(O, O + dr * Lr, buff=0, color=C_E, stroke_width=2 + 4 * rr, stroke_opacity=0.25 + 0.75 * rr,
                        max_tip_length_to_length_ratio=0.08))
            if s < 1:
                tt = np.arcsin(s)
                dt = np.array([np.sin(tt), -np.cos(tt), 0])
                g.add(Arrow(O, O + dt * Lr, buff=0, color=C_HL, stroke_width=5, max_tip_length_to_length_ratio=0.08))
                g.add(MT(rf"\theta_t={np.degrees(tt):.1f}^\circ", 26, C_HL).move_to(RIGHT * 5.0 + DOWN * 2.05))
            else:
                g.add(CT(r"全反射（倏逝波贴着界面）", 22, C_HL).move_to(RIGHT * 5.0 + DOWN * 2.05))
            g.add(MT(rf"\theta_i={np.degrees(ti):.1f}^\circ", 26, C_E).move_to(RIGHT * 2.3 + DOWN * 2.05))
            return g

        rg = always_redraw(rays)
        self.add(rg)
        # 右侧：|R| 曲线
        ax = Axes(x_range=[0, 90, 15], y_range=[0, 1, 0.25], x_length=5.4, y_length=3.0,
                  axis_config={"stroke_width": 1.5, "include_ticks": False, "include_tip": False}).move_to(RIGHT * 3.6 + UP * 0.4)
        xl = MT(r"\theta_i\,(^\circ)", 22, GREY_B).next_to(ax.x_axis, DOWN, buff=0.1)
        yl = MT(r"|R|", 24, GREY_B).next_to(ax.y_axis, UP, buff=0.05)
        ticks = VGroup(*[MT(str(v), 18, GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.05) for v in (0, 30, 60, 90)])

        def curves():
            e1, e2 = eps
            xs = np.linspace(0, 89.9, 400)
            Rpa, Rpe = fresnel(np.radians(xs), e1, e2)
            c1 = VMobject(stroke_color=C_H, stroke_width=3).set_points_as_corners([ax.c2p(x, y) for x, y in zip(xs, Rpa)])
            c2 = VMobject(stroke_color=C_S, stroke_width=3).set_points_as_corners([ax.c2p(x, y) for x, y in zip(xs, Rpe)])
            return VGroup(c1, c2)

        cv = curves()
        mk = always_redraw(lambda: DashedLine(ax.c2p(np.degrees(th.get_value()), 0), ax.c2p(np.degrees(th.get_value()), 1), color=WHITE, stroke_width=1.5))
        lg = VGroup(CT(r"平行极化 $|R_{/\!/}|$", 20, C_H), CT(r"垂直极化 $|R_\perp|$", 20, C_S)).arrange(RIGHT, buff=0.4).next_to(ax, UP, buff=0.1)
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(ticks), Create(cv), FadeIn(lg))
        self.add(mk)
        cap = CT(r"由空气入射到 $\varepsilon_r=4$ 的介质：$\theta_B=\arctan\sqrt{\varepsilon_2/\varepsilon_1}=63.4^\circ$ 时 $R_{/\!/}=0$", 24)
        fitw(cap, 12.8).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(cap))
        self.play(th.animate.set_value(63.43 * DEGREES), run_time=3)
        bm = VGroup(Dot(ax.c2p(63.43, 0), color=C_H), MT(r"\theta_B", 22, C_H).next_to(ax.c2p(63.43, 0), UP, buff=0.12))
        self.play(FadeIn(bm))
        self.wait(1)
        self.play(th.animate.set_value(85 * DEGREES), run_time=2)
        self.wait(0.5)
        # 从光密到光疏
        eps[0], eps[1] = 4.0, 1.0
        cv2 = curves()
        cap2 = CT(r"由 $\varepsilon_r=4$ 入射到空气：$\theta_c=\arcsin\sqrt{\varepsilon_2/\varepsilon_1}=30^\circ$，$\theta_i\ge\theta_c$ 时 $|R|=1$（全反射）；$\theta_B=26.6^\circ$", 24)
        fitw(cap2, 12.8).to_edge(DOWN, buff=0.3)
        m1b = CT(r"媒质 1：$\varepsilon_r=4$", 22, GREY_A).move_to(m1)
        m2b = CT(r"媒质 2：空气", 22, GREY_A).move_to(m2)
        upper = Rectangle(width=6, height=2.7, stroke_width=0, fill_color=C_NEG, fill_opacity=0.15).move_to(O + UP * 1.35)
        th.set_value(10 * DEGREES)
        self.play(ReplacementTransform(cv, cv2), FadeOut(bm), ReplacementTransform(cap, cap2), ReplacementTransform(m1, m1b),
                  ReplacementTransform(m2, m2b), ReplacementTransform(lower, upper))
        bm2 = VGroup(Dot(ax.c2p(26.57, 0), color=C_H), MT(r"\theta_B", 22, C_H).next_to(ax.c2p(26.57, 0), UP, buff=0.12),
                     Dot(ax.c2p(30, 1), color=C_HL), MT(r"\theta_c", 22, C_HL).next_to(ax.c2p(30, 1), UP, buff=0.08))
        self.play(FadeIn(bm2))
        self.play(th.animate.set_value(26.57 * DEGREES), run_time=2)
        self.wait(0.5)
        self.play(th.animate.set_value(50 * DEGREES), run_time=3)
        self.wait(2)
