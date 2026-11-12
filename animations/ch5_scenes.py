"""第 5 章 时变电磁场与电磁波 —— manim 动画源码（LaTeX 排版）."""
import numpy as np

from common import *  # noqa: F401,F403
from fieldtools import *  # noqa: F401,F403
from ch4_scenes import wire_dot


def small_arrow(p, d, color, sw=4, tip=0.35):
    return Arrow(p, p + d, buff=0, color=color, stroke_width=sw, max_tip_length_to_length_ratio=tip,
                 max_stroke_width_to_length_ratio=12)


# --------------------------------------------------------------------------
# 5.1 法拉第电磁感应定律
# --------------------------------------------------------------------------
class C5_Faraday(Scene):
    def construct(self):
        title = title_bar(r"法拉第电磁感应定律：$\oint_C\vv E\cdot\dd\vv l=-\dfrac{\dd\Psi}{\dd t}$，变化的磁场激发涡旋电场")
        fitw(title, 13.6)
        self.play(FadeIn(title))
        O = LEFT * 3.6 + DOWN * 0.4
        R = 1.7
        t = ValueTracker(0.0)
        pts = [O + np.array([x, y, 0]) for x in np.linspace(-2.6, 2.6, 8) for y in np.linspace(-2.6, 2.6, 8)]

        def bfield():
            b = np.sin(t.get_value())
            g = VGroup()
            for p in pts:
                op = min(1, 0.12 + abs(b))
                g.add(wire_dot(p, out=b >= 0, r=0.09, color=C_H).set_opacity(op))
            return g

        B = always_redraw(bfield)
        loop = Circle(radius=R, color=WHITE, stroke_width=3).move_to(O)

        def efield():
            e = -np.cos(t.get_value())  # 环量 ∝ -dB/dt，正为逆时针
            g = VGroup()
            if abs(e) < 0.05:
                return g
            for k in range(8):
                a = k * TAU / 8
                p = O + R * np.array([np.cos(a), np.sin(a), 0])
                d = np.sign(e) * np.array([-np.sin(a), np.cos(a), 0]) * 0.75 * abs(e)
                g.add(small_arrow(p - d / 2, d, C_E, sw=5))
            return g

        E = always_redraw(efield)
        lb = CT(r"$\vv B(t)=\az B_0\sin\omega t$（$\odot$ 出纸面，$\otimes$ 入纸面）", 22, C_H).next_to(O + UP * 2.8, UP, buff=0.05)
        fitw(lb, 6.4)
        self.add(B)
        self.play(Create(loop), FadeIn(lb))
        self.add(E)
        # 右侧曲线
        ax = Axes(x_range=[0, TAU * 1.5, PI / 2], y_range=[-1.3, 1.3, 1], x_length=5.8, y_length=2.6,
                  axis_config={"stroke_width": 1.5, "include_ticks": False, "include_tip": False}).move_to(RIGHT * 3.5 + UP * 1.0)
        c1 = always_redraw(lambda: ax.plot(np.sin, x_range=[0, max(t.get_value(), 0.01), 0.02], color=C_H, stroke_width=3))
        c2 = always_redraw(lambda: ax.plot(lambda x: -np.cos(x), x_range=[0, max(t.get_value(), 0.01), 0.02], color=C_E, stroke_width=3))
        l1 = CT(r"$\Psi\propto\sin\omega t$", 22, C_H).next_to(ax, UP, buff=0.05).shift(LEFT * 1.6)
        l2 = CT(r"$\mathcal E=-\dfrac{\dd\Psi}{\dd t}\propto-\cos\omega t$", 22, C_E).next_to(ax, UP, buff=0.05).shift(RIGHT * 1.3)
        xl = MT(r"\omega t", 22, GREY_B).next_to(ax.x_axis, RIGHT, buff=0.05)
        self.play(Create(ax), FadeIn(l1), FadeIn(l2), FadeIn(xl))
        self.add(c1, c2)
        txt = VGroup(
            CT(r"磁通增大时，感应电场的环绕方向使其电流的磁场", 22),
            CT(r"\textbf{阻碍}磁通的变化（楞次定律）", 22),
            MT(r"\nabla\times\vv E=-\frac{\partial\vv B}{\partial t}", 34, C_HL),
            CT(r"感应电场是\textbf{涡旋场}：$\oint\vv E\cdot\dd\vv l\ne0$，不能再写成 $-\nabla\phi$", 22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        fitw(txt, 6.2).move_to(RIGHT * 3.5 + DOWN * 1.9)
        self.play(t.animate.set_value(TAU * 0.75), FadeIn(txt[0]), FadeIn(txt[1]), run_time=4, rate_func=linear)
        self.play(t.animate.set_value(TAU * 1.5), FadeIn(txt[2]), FadeIn(txt[3]), run_time=4, rate_func=linear)
        self.wait(1)
        B.clear_updaters(); E.clear_updaters(); c1.clear_updaters(); c2.clear_updaters()
        self.play(*[FadeOut(m) for m in [B, E, loop, lb, ax, c1, c2, l1, l2, xl, txt]])
        # ---------------- 动生电动势
        cap = CT(r"动生电动势：导体棒在磁场中运动，$\mathcal E=\oint(\vv v\times\vv B)\cdot\dd\vv l$", 26).next_to(title, DOWN, buff=0.3)
        fitw(cap, 13)
        self.play(FadeIn(cap))
        O2 = LEFT * 2.5 + DOWN * 0.6
        L = 2.6
        rails = VGroup(Line(O2 + LEFT * 2.5 + UP * L / 2, O2 + RIGHT * 4.0 + UP * L / 2, color=GREY_A, stroke_width=4),
                       Line(O2 + LEFT * 2.5 + DOWN * L / 2, O2 + RIGHT * 4.0 + DOWN * L / 2, color=GREY_A, stroke_width=4),
                       Line(O2 + LEFT * 2.5 + UP * L / 2, O2 + LEFT * 2.5 + DOWN * L / 2, color=GREY_A, stroke_width=4))
        res = Rectangle(width=0.3, height=0.9, color=GREY_A, fill_color=BLACK, fill_opacity=1).move_to(O2 + LEFT * 2.5)
        rl = MT("R", 26).next_to(res, LEFT, buff=0.1)
        bg = VGroup(*[wire_dot(O2 + np.array([x, y, 0]), out=False, r=0.08, color=C_H).set_opacity(0.6)
                      for x in np.linspace(-2.1, 3.7, 9) for y in np.linspace(-1.0, 1.0, 4)])
        x = ValueTracker(-0.8)
        bar = always_redraw(lambda: Line(O2 + RIGHT * x.get_value() + UP * (L / 2 + 0.15), O2 + RIGHT * x.get_value() + DOWN * (L / 2 + 0.15),
                                         color=C_HL, stroke_width=8))
        shade = always_redraw(lambda: Rectangle(width=x.get_value() + 2.5, height=L, stroke_width=0, fill_color=C_H, fill_opacity=0.12)
                              .move_to(O2 + RIGHT * (x.get_value() - 2.5) / 2))
        v = always_redraw(lambda: small_arrow(O2 + RIGHT * (x.get_value() + 0.15) + DOWN * 0.0, RIGHT * 0.8, WHITE))
        vl = always_redraw(lambda: MT(r"\vv v", 26).next_to(O2 + RIGHT * (x.get_value() + 0.95), UP, buff=0.05))
        cur = always_redraw(lambda: VGroup(small_arrow(O2 + RIGHT * x.get_value() + DOWN * 0.7, UP * 0.6, C_E, sw=6),
                                           small_arrow(O2 + RIGHT * (x.get_value() - 1.0) + UP * L / 2, LEFT * 0.6, C_E, sw=6),
                                           small_arrow(O2 + RIGHT * (x.get_value() - 1.0) + DOWN * L / 2, RIGHT * 0.6, C_E, sw=6)))
        Ll = MT("l", 26, GREY_A).next_to(O2 + RIGHT * 4.0, RIGHT, buff=0.15)
        bll = CT(r"$\vv B$ 均匀，指向纸内", 22, C_H).next_to(rails, DOWN, buff=0.15)
        self.play(FadeIn(bg), Create(rails), FadeIn(res), FadeIn(rl), FadeIn(bll), FadeIn(Ll))
        self.add(shade, bar, v, vl)
        self.play(FadeIn(cur))
        self.add(cur)
        expl = VGroup(
            CT(r"棒中电荷受力 $q\vv v\times\vv B$ 沿棒向上", 22, C_E),
            MT(r"\mathcal E=Blv=-\frac{\dd\Psi}{\dd t}", 32, C_HL),
            CT(r"回路面积（浅色）增大，磁通增大，感应电流逆时针", 22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        fitw(expl, 5.0).move_to(RIGHT * 4.4 + UP * 1.6)
        self.play(x.animate.set_value(2.6), FadeIn(expl), run_time=4, rate_func=linear)
        note = CT(r"一般情形：$\mathcal E=\displaystyle\oint_C\left(\vv v\times\vv B\right)\cdot\dd\vv l-\int_S\dfrac{\partial\vv B}{\partial t}\cdot\dd\vv S$（动生 + 感生）", 24).to_edge(DOWN, buff=0.25)
        fitw(note, 13)
        self.play(FadeIn(note))
        self.wait(3)


# --------------------------------------------------------------------------
# 5.2 位移电流
# --------------------------------------------------------------------------
class C5_Displacement(Scene):
    def construct(self):
        title = title_bar(r"位移电流：同一环路 $C$ 张两个曲面，$S$ 被导线穿过，$S'$ 从极板间穿过——$\vv J_d=\dfrac{\partial\vv D}{\partial t}$ 补上了缺口")
        fitw(title, 13.6)
        self.play(FadeIn(title))
        y0 = 0.2
        g = 0.7  # 半间距
        plL = Line([-g - 0.0, y0 - 1.3, 0], [-g, y0 + 1.3, 0], color=C_POS, stroke_width=8).shift(LEFT * 2.6)
        plR = Line([g, y0 - 1.3, 0], [g, y0 + 1.3, 0], color=C_NEG, stroke_width=8).shift(LEFT * 2.6)
        wL = Line([-6.8, y0, 0], [-g - 2.6, y0, 0], color=GREY_A, stroke_width=5)
        wR = Line([g - 2.6, y0, 0], [1.0, y0, 0], color=GREY_A, stroke_width=5)
        self.play(Create(wL), Create(wR), Create(plL), Create(plR))
        t = ValueTracker(0.0)
        # 传导电流箭头
        iarr = always_redraw(lambda: VGroup(*[small_arrow(np.array([xx, y0, 0]) + LEFT * 0.3 * np.sign(np.cos(t.get_value()) + 1e-9),
                                                          RIGHT * 0.6 * np.cos(t.get_value()), C_HL, sw=6)
                                              for xx in (-5.9, -4.6, 0.3)]) if abs(np.cos(t.get_value())) > 0.08 else VGroup())
        # 极板间电场（强度 ∝ q ∝ sin）
        def efield():
            q = np.sin(t.get_value())
            gg = VGroup()
            if abs(q) < 0.05:
                return gg
            for yy in np.linspace(y0 - 1.0, y0 + 1.0, 5):
                gg.add(Line([-g - 2.6 + 0.1, yy, 0], [g - 2.6 - 0.1, yy, 0], color=C_E, stroke_width=2 + 3 * abs(q),
                            stroke_opacity=0.3 + 0.7 * abs(q)))
                d = RIGHT * 0.25 * np.sign(q)
                gg.add(small_arrow(np.array([-2.6, yy, 0]) - d / 2, d, C_E, sw=3))
            return gg

        Ef = always_redraw(efield)
        # 环路 C 与两个曲面
        cx = -4.2
        C = Ellipse(width=0.55, height=2.0, color=WHITE, stroke_width=3).move_to([cx, y0, 0])
        Cl = MT("C", 28).next_to(C, UP, buff=0.05)
        S = Ellipse(width=0.55, height=2.0, stroke_width=0, fill_color=C_H, fill_opacity=0.25).move_to([cx, y0, 0])
        Sl = MT("S", 26, C_H).move_to([cx - 0.55, y0 - 1.2, 0])
        bag = VMobject(stroke_color=C_S, stroke_width=3, fill_color=C_S, fill_opacity=0.15)
        bag.set_points_smoothly([[cx, y0 + 1.0, 0], [cx + 1.2, y0 + 1.1, 0], [-2.6, y0 + 0.95, 0], [-2.35, y0, 0],
                                 [-2.6, y0 - 0.95, 0], [cx + 1.2, y0 - 1.1, 0], [cx, y0 - 1.0, 0]])
        Spl = MT("S'", 26, C_S).move_to([-3.0, y0 - 1.45, 0])
        self.add(Ef, iarr)
        self.play(Create(C), FadeIn(Cl), FadeIn(S), FadeIn(Sl))
        self.play(Create(bag), FadeIn(Spl))
        # 右侧曲线
        ax = Axes(x_range=[0, TAU * 1.25, PI / 2], y_range=[-1.3, 1.3, 1], x_length=5.0, y_length=2.4,
                  axis_config={"stroke_width": 1.5, "include_ticks": False, "include_tip": False}).move_to(RIGHT * 4.2 + UP * 1.2)
        cq = always_redraw(lambda: ax.plot(np.sin, x_range=[0, max(t.get_value(), 0.01), 0.02], color=C_E, stroke_width=3))
        ci = always_redraw(lambda: ax.plot(np.cos, x_range=[0, max(t.get_value(), 0.01), 0.02], color=C_HL, stroke_width=5))
        cd = always_redraw(lambda: DashedVMobject(ax.plot(np.cos, x_range=[0, max(t.get_value(), 0.02), 0.02], color=C_S, stroke_width=3), num_dashes=40))
        lg = VGroup(CT(r"极板电荷 $q$、板间 $D=q/A$", 20, C_E), CT(r"导线电流 $i=\dd q/\dd t$", 20, C_HL),
                    CT(r"位移电流 $\int_{S'}\frac{\partial\vv D}{\partial t}\cdot\dd\vv S=A\frac{\dd D}{\dd t}$（虚线）", 20, C_S)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        fitw(lg, 5.2).next_to(ax, DOWN, buff=0.15)
        self.play(Create(ax), FadeIn(lg))
        self.add(cq, ci, cd)
        self.play(t.animate.set_value(TAU * 1.25), run_time=7, rate_func=linear)
        for m in (cq, ci, cd, Ef, iarr):
            m.clear_updaters()
        conc = VGroup(
            CT(r"只算传导电流：$\oint_C\vv H\cdot\dd\vv l=\int_S\vv J\cdot\dd\vv S=i$，但 $\int_{S'}\vv J\cdot\dd\vv S=0$ —— 矛盾！", 22),
            CT(r"麦克斯韦：$\nabla\times\vv H=\vv J+\dfrac{\partial\vv D}{\partial t}$，于是 $\nabla\cdot\left(\vv J+\dfrac{\partial\vv D}{\partial t}\right)=0$，全电流处处连续", 22, C_HL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        fitw(conc, 13.2).to_edge(DOWN, buff=0.25)
        self.play(FadeIn(conc[0]))
        self.play(FadeIn(conc[1]))
        self.wait(3)


# --------------------------------------------------------------------------
# 5.4 坡印廷矢量：同轴线中的能流
# --------------------------------------------------------------------------
class C5_Poynting(Scene):
    def construct(self):
        title = title_bar(r"坡印廷矢量 $\vv S=\vv E\times\vv H$：能量在导体\textbf{之间}的场中流动，导线只是“导轨”")
        fitw(title, 13.6)
        self.play(FadeIn(title))
        x0, x1 = -5.6, 3.2
        yc = -0.2
        ri, ro = 0.35, 1.9
        outerT = Rectangle(width=x1 - x0, height=0.22, stroke_width=0, fill_color=GREY_B, fill_opacity=1).move_to([(x0 + x1) / 2, yc + ro + 0.11, 0])
        outerB = outerT.copy().move_to([(x0 + x1) / 2, yc - ro - 0.11, 0])
        inner = Rectangle(width=x1 - x0, height=2 * ri, stroke_width=0, fill_color=C_HL, fill_opacity=0.9).move_to([(x0 + x1) / 2, yc, 0])
        src = VGroup(Circle(radius=0.35, color=WHITE).move_to([x0 - 0.6, yc, 0]), MT("U", 26).move_to([x0 - 0.6, yc, 0]))
        load = VGroup(Rectangle(width=0.35, height=1.2, color=WHITE).move_to([x1 + 0.6, yc, 0]), MT("R_L", 24).move_to([x1 + 1.15, yc, 0]))
        lab = CT(r"同轴线纵剖面：内导体（橙）电流 $I$ 向右，外导体（灰）电流向左", 22).next_to(outerT, UP, buff=0.1)
        fitw(lab, 9)
        self.play(FadeIn(outerT), FadeIn(outerB), FadeIn(inner), FadeIn(src), FadeIn(load), FadeIn(lab))
        Ea = VGroup()
        Hs = VGroup()
        for xx in np.linspace(x0 + 0.6, x1 - 0.6, 7):
            Ea.add(small_arrow(np.array([xx, yc + ri + 0.05, 0]), UP * (ro - ri - 0.15), C_E, sw=3, tip=0.12))
            Ea.add(small_arrow(np.array([xx, yc - ri - 0.05, 0]), DOWN * (ro - ri - 0.15), C_E, sw=3, tip=0.12))
        for xx in np.linspace(x0 + 1.2, x1 - 1.2, 6):
            for yy in (0.75, 1.4):
                Hs.add(wire_dot(np.array([xx, yc + yy, 0]), out=True, r=0.09, color=C_H))
                Hs.add(wire_dot(np.array([xx, yc - yy, 0]), out=False, r=0.09, color=C_H))
        leg = VGroup(CT(r"$\vv E$：由内导体指向外导体（黄）", 22, C_E),
                     CT(r"$\vv H$：环绕内导体，上方出纸面、下方入纸面（青）", 22, C_H)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        fitw(leg, 7.5).to_edge(DOWN, buff=0.35).shift(LEFT * 2.6)
        self.play(FadeIn(Ea), FadeIn(leg[0]))
        self.play(FadeIn(Hs), FadeIn(leg[1]))
        # 能流
        Ss = VGroup()
        for yy in (0.6, 1.05, 1.5):
            for xx in np.linspace(x0 + 0.5, x1 - 1.0, 5):
                w = 0.9 * (0.6 / yy) ** 2 + 0.2
                Ss.add(small_arrow(np.array([xx, yc + yy, 0]), RIGHT * w, C_S, sw=5, tip=0.3))
                Ss.add(small_arrow(np.array([xx, yc - yy, 0]), RIGHT * w, C_S, sw=5, tip=0.3))
        res1 = VGroup(
            MT(r"\vv S=\vv E\times\vv H=\az\frac{UI}{2\pi\rho^2\ln(b/a)}", 30, C_S),
            MT(r"P=\int_a^b S\,2\pi\rho\,\dd\rho=UI", 30, C_S),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        fitw(res1, 4.6).to_corner(DR, buff=0.3)
        self.play(FadeOut(Hs), Ea.animate.set_opacity(0.35), LaggedStart(*[GrowArrow(a) for a in Ss], lag_ratio=0.02), run_time=2)
        self.play(FadeIn(res1))
        self.wait(2)
        # 有耗内导体：E 多了切向分量 → S 有径向分量流入导体
        cap2 = CT(r"内导体电导率有限：表面有 $E_z=\dfrac{J}{\sigma}$，$\vv S$ 倾斜，一部分能量\textbf{从侧面流入导体}变成焦耳热", 22, C_HL).next_to(title, DOWN, buff=0.12)
        fitw(cap2, 13)
        tilt = VGroup()
        for xx in np.linspace(x0 + 0.8, x1 - 1.0, 7):
            tilt.add(small_arrow(np.array([xx, yc + ri + 0.55, 0]), np.array([0.35, -0.42, 0]), RED_B, sw=5, tip=0.3))
            tilt.add(small_arrow(np.array([xx, yc - ri - 0.55, 0]), np.array([0.35, 0.42, 0]), RED_B, sw=5, tip=0.3))
        res2 = MT(r"-\oint\vv S\cdot\dd\vv S=\frac{I^2}{2\pi^2a^3\sigma}\cdot2\pi a=I^2R_0", 28, RED_B)
        fitw(res2, 4.6).next_to(res1, UP, buff=0.2).align_to(res1, LEFT)
        self.play(FadeOut(lab), FadeIn(cap2), Ss.animate.set_opacity(0.4), LaggedStart(*[GrowArrow(a) for a in tilt], lag_ratio=0.05), run_time=2)
        self.play(FadeIn(res2))
        self.wait(3)


# --------------------------------------------------------------------------
# 5.5 时谐场的相量表示
# --------------------------------------------------------------------------
class C5_Phasor(Scene):
    def construct(self):
        title = title_bar(r"相量：$\vv E(t)=\operatorname{Re}\left[\dot{\vv E}_m\mathrm e^{\mathrm j\omega t}\right]$，旋转矢量在实轴上的投影就是瞬时值")
        fitw(title, 13.6)
        self.play(FadeIn(title))
        O = LEFT * 4.3 + DOWN * 0.3
        s = 1.6
        axes = VGroup(Arrow(O + LEFT * 2.0, O + RIGHT * 2.1, buff=0, stroke_width=2, color=GREY_B),
                      Arrow(O + DOWN * 2.0, O + UP * 2.1, buff=0, stroke_width=2, color=GREY_B))
        re = MT(r"\operatorname{Re}", 22, GREY_B).next_to(axes[0], RIGHT, buff=0.05)
        im = MT(r"\operatorname{Im}", 22, GREY_B).next_to(axes[1], UP, buff=0.05)
        circ = Circle(radius=s, color=GREY_D, stroke_width=1.5).move_to(O)
        self.play(Create(axes), FadeIn(re), FadeIn(im), Create(circ))
        phi = PI / 6
        t = ValueTracker(0.0)

        def tip(off=0.0, r=1.0):
            a = t.get_value() + phi + off
            return O + s * r * np.array([np.cos(a), np.sin(a), 0])

        vecE = always_redraw(lambda: Arrow(O, tip(), buff=0, color=C_E, stroke_width=5))
        proj = always_redraw(lambda: DashedLine(tip(), [tip()[0], O[1], 0], color=C_E, stroke_width=2))
        pdot = always_redraw(lambda: Dot([tip()[0], O[1], 0], color=C_E, radius=0.07))
        lE = MT(r"E_m\mathrm e^{\mathrm j(\omega t+\varphi)}", 26, C_E).move_to(O + UP * 2.45 + RIGHT * 0.2)
        self.play(GrowArrow(vecE), FadeIn(lE))
        self.add(proj, pdot)
        # 右侧：瞬时值（时间轴向下画成波形）
        ax = Axes(x_range=[0, 4 * PI, PI], y_range=[-1.2, 1.2, 1], x_length=6.6, y_length=2.4,
                  axis_config={"stroke_width": 1.5, "include_ticks": False, "include_tip": False}).move_to(RIGHT * 2.9 + UP * 1.0)
        xl = MT(r"\omega t", 22, GREY_B).next_to(ax.x_axis, RIGHT, buff=0.05)
        cE = always_redraw(lambda: ax.plot(lambda x: np.cos(x + phi), x_range=[0, max(t.get_value(), 0.01), 0.03], color=C_E, stroke_width=3))
        lcE = MT(r"E(t)=E_m\cos(\omega t+\varphi)", 26, C_E).next_to(ax, UP, buff=0.05)
        self.play(Create(ax), FadeIn(xl), FadeIn(lcE))
        self.add(cE)
        self.play(t.animate.set_value(2 * PI), run_time=5, rate_func=linear)
        # 求导 = 乘 jω：超前 90°
        vecD = always_redraw(lambda: Arrow(O, tip(PI / 2, 0.8), buff=0, color=C_HL, stroke_width=5))
        cD = always_redraw(lambda: ax.plot(lambda x: 0.8 * np.cos(x + phi + PI / 2), x_range=[2 * PI, max(t.get_value(), 2 * PI + 0.01), 0.03],
                                           color=C_HL, stroke_width=3))
        lD = MT(r"\mathrm j\omega\,E_m\mathrm e^{\mathrm j(\omega t+\varphi)}", 26, C_HL).move_to(O + DOWN * 2.45 + RIGHT * 0.2)
        self.play(GrowArrow(vecD), FadeIn(lD))
        self.add(cD)
        self.play(t.animate.set_value(4 * PI), run_time=5, rate_func=linear)
        txt = VGroup(
            CT(r"$\dfrac{\partial}{\partial t}\ \longleftrightarrow\ \mathrm j\omega$：求导就是乘 $\mathrm j\omega$，相位超前 $90^\circ$（橙）", 22),
            MT(r"\nabla\times\dot{\vv H}=\dot{\vv J}+\mathrm j\omega\dot{\vv D},\qquad\nabla\times\dot{\vv E}=-\mathrm j\omega\dot{\vv B}", 28, C_HL),
            CT(r"时间变量消失，四维偏微分方程变成三维；复数运算见《复变函数》第 1 章", 22, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        fitw(txt, 7.0).move_to(RIGHT * 2.9 + DOWN * 1.9)
        for m in txt:
            self.play(FadeIn(m), run_time=0.7)
        self.wait(3)
