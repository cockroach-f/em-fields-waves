"""数值工具：等值线（marching squares）、矢量线追踪、二维点电荷场。"""
import numpy as np
from manim import VGroup, Line, VMobject, Arrow, WHITE


def fitw(m, w):
    if m.width > w:
        m.scale_to_fit_width(w)
    return m


def contour_lines(ax, f, levels, colors, xr=(-3, 3), yr=(-3, 3), n=120, sw=2.0, opacity=1.0):
    """返回 VGroup(每个等值一个 VGroup 的小线段)."""
    xs = np.linspace(*xr, n)
    ys = np.linspace(*yr, n)
    X, Y = np.meshgrid(xs, ys)
    U = f(X, Y)
    out = VGroup()
    for lev, c in zip(levels, colors):
        segs = VGroup()
        for i in range(n - 1):
            for j in range(n - 1):
                q = [U[i, j], U[i, j + 1], U[i + 1, j + 1], U[i + 1, j]]
                if not np.all(np.isfinite(q)):
                    continue
                corners = [(xs[j], ys[i]), (xs[j + 1], ys[i]), (xs[j + 1], ys[i + 1]), (xs[j], ys[i + 1])]
                pts = []
                for k in range(4):
                    a, b = q[k], q[(k + 1) % 4]
                    if (a - lev) * (b - lev) < 0:
                        t = (lev - a) / (b - a)
                        pa, pb = np.array(corners[k]), np.array(corners[(k + 1) % 4])
                        pts.append(pa + t * (pb - pa))
                if len(pts) >= 2:
                    segs.add(Line(ax.c2p(*pts[0]), ax.c2p(*pts[1]), color=c, stroke_width=sw, stroke_opacity=opacity))
                if len(pts) == 4:
                    segs.add(Line(ax.c2p(*pts[2]), ax.c2p(*pts[3]), color=c, stroke_width=sw, stroke_opacity=opacity))
        out.add(segs)
    return out


def trace(F, p0, h=0.02, nmax=1200, box=(-3.2, 3.2, -3.2, 3.2), stop=None, sign=1.0):
    """RK4 沿归一化场方向追踪矢量线."""
    pts = [np.array(p0, dtype=float)]
    p = pts[0].copy()

    def d(q):
        v = np.array(F(*q), dtype=float) * sign
        n = np.linalg.norm(v)
        return v / n if n > 1e-12 else v * 0

    for _ in range(nmax):
        k1 = d(p); k2 = d(p + h / 2 * k1); k3 = d(p + h / 2 * k2); k4 = d(p + h * k3)
        p = p + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        pts.append(p.copy())
        if not (box[0] < p[0] < box[1] and box[2] < p[1] < box[3]):
            break
        if stop is not None and stop(p):
            break
    return np.array(pts)


def polyline(ax, pts, color=WHITE, sw=2.5, opacity=1.0):
    m = VMobject(stroke_color=color, stroke_width=sw, stroke_opacity=opacity)
    m.set_points_as_corners([ax.c2p(*q) for q in pts])
    return m


def mid_arrow(ax, pts, color=WHITE, frac=0.5, size=0.18):
    """在折线中部放一个方向箭头."""
    k = max(1, min(len(pts) - 2, int(len(pts) * frac)))
    a, b = ax.c2p(*pts[k - 1]), ax.c2p(*pts[k + 1])
    d = b - a
    n = np.linalg.norm(d)
    if n < 1e-9:
        return VGroup()
    d = d / n * size
    c = ax.c2p(*pts[k])
    return Arrow(c - d / 2, c + d / 2, buff=0, color=color, stroke_width=3, max_tip_length_to_length_ratio=0.9,
                 max_stroke_width_to_length_ratio=20)


def charges_field(charges, soft=1e-3):
    """charges: [(q, x, y)] -> 2D 截面中的 3D 点电荷场 E ∝ q R/R^3."""
    def F(x, y):
        ex = ey = 0.0
        for q, a, b in charges:
            dx, dy = x - a, y - b
            r3 = (dx * dx + dy * dy + soft) ** 1.5
            ex += q * dx / r3
            ey += q * dy / r3
        return ex, ey
    return F


def charges_potential(charges, soft=1e-4):
    def P(X, Y):
        V = 0 * X
        for q, a, b in charges:
            V = V + q / np.sqrt((X - a) ** 2 + (Y - b) ** 2 + soft)
        return V
    return P


def colormap(v, stops=None):
    """v in [0,1] (ndarray) -> uint8 RGB，类似 inferno 的配色."""
    if stops is None:
        stops = [(0.0, (0, 0, 4)), (0.25, (87, 16, 110)), (0.5, (188, 55, 84)), (0.75, (249, 142, 9)), (1.0, (252, 255, 164))]
    v = np.clip(v, 0, 1)
    out = np.zeros(v.shape + (3,))
    for (a, ca), (b, cb) in zip(stops[:-1], stops[1:]):
        m = (v >= a) & (v <= b)
        t = ((v - a) / (b - a))[m]
        for k in range(3):
            out[..., k][m] = ca[k] + t * (cb[k] - ca[k])
    return out.astype(np.uint8)


def heat_image(U, vmin, vmax, width, stops=None):
    """U[row=y, col=x]，y 向上为正；返回宽度为 width 的 ImageMobject."""
    from manim import ImageMobject
    arr = colormap((np.asarray(U) - vmin) / (vmax - vmin), stops)[::-1]
    im = ImageMobject(arr)
    im.set_resampling_algorithm(0)  # nearest
    im.scale_to_fit_width(width)
    return im
