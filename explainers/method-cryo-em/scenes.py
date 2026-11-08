"""Cryo-electron microscopy: freezing molecules to see them  (Biochemistrypedia methods film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  PURPLE = the particles (the molecule or complex being studied; always a simple blob)
  BLUE   = the apparatus: grid, cold baths, microscope parts
  TEAL   = water and the glassy ice that holds the particles
  YELLOW = the electron beam, and the dose
  GREEN  = a good result: averages, maps, controls, the independent halves
  RED    = damage, noise made into a feature, the pitfalls, the crossed-out
  ORANGE = the extra protein in a complex
  GREY   = membranes, structure, de-emphasised text, the noise of an image
  GOLD   = people and dates, and the closing rule
Particles are three overlapping round blobs seen from different directions; the map is a
contour outline computed from the same blobs. Never a molecular structure.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"

# ---------------------------------------------------------------------------------------------
# a made-up particle: big blobs plus fine details, in 3D, so every view is a different flat shape
# ---------------------------------------------------------------------------------------------
BIG = [(-0.85, 0.05, 0.15, 0.72, 1.0), (0.85, 0.25, -0.2, 0.62, 1.0), (0.05, -0.85, 0.25, 0.58, 1.0)]
FINE = [(0.0, 0.55, 0.55, 0.26, 0.9), (-0.35, -0.45, -0.65, 0.24, 0.9), (1.0, -0.55, 0.3, 0.22, 0.9)]
BIG_B = [(-0.85, 0.05, 0.15, 0.72, 1.0), (0.55, 1.0, -0.2, 0.62, 1.0), (0.05, -0.85, 0.25, 0.58, 1.0)]
EXTRA = [(1.5, -1.0, 0.0, 0.34, 1.0)]
ALL = BIG + FINE


def rot(a, b, c):
    ca, sa, cb, sb, cc, sc = np.cos(a), np.sin(a), np.cos(b), np.sin(b), np.cos(c), np.sin(c)
    rx = np.array([[1, 0, 0], [0, ca, -sa], [0, sa, ca]])
    ry = np.array([[cb, 0, sb], [0, 1, 0], [-sb, 0, cb]])
    rz = np.array([[cc, -sc, 0], [sc, cc, 0], [0, 0, 1]])
    return rz @ ry @ rx


def project(R, spheres):
    """-> list of (x, y, sigma, amp) after rotating and dropping z."""
    out = []
    for x, y, z, s, a in spheres:
        p = R @ np.array([x, y, z])
        out.append((p[0], p[1], s, a))
    return out


def density(R, spheres=ALL, n=60, extent=2.5, blur=0.0):
    xs = np.linspace(-extent, extent, n)
    X, Y = np.meshgrid(xs, xs)
    Z = np.zeros_like(X)
    for x, y, s, a in project(R, spheres):
        s2 = s * s + blur * blur
        Z += a * (s * s / s2) * np.exp(-((X - x) ** 2 + (Y - y) ** 2) / (2 * s2))
    return X, Y, Z


# ---- contour outlines (marching squares, chained) --------------------------------------------
def contour_paths(Z, level, extent):
    n = Z.shape[0]
    step = 2 * extent / (n - 1)

    def pt(key):
        (i, j), d = key
        if d == 0:   # edge between (i,j) and (i,j+1)  -> along x
            za, zb = Z[i, j], Z[i, j + 1]
            t = (level - za) / (zb - za)
            return np.array([-extent + (j + t) * step, -extent + i * step])
        za, zb = Z[i, j], Z[i + 1, j]
        t = (level - za) / (zb - za)
        return np.array([-extent + j * step, -extent + (i + t) * step])

    segs = []
    for i in range(n - 1):
        for j in range(n - 1):
            c = [Z[i, j] >= level, Z[i, j + 1] >= level, Z[i + 1, j + 1] >= level, Z[i + 1, j] >= level]
            idx = c[0] + 2 * c[1] + 4 * c[2] + 8 * c[3]
            if idx in (0, 15):
                continue
            e = {"b": ((i, j), 0), "r": ((i, j + 1), 1), "t": ((i + 1, j), 0), "l": ((i, j), 1)}
            table = {1: [("l", "b")], 2: [("b", "r")], 3: [("l", "r")], 4: [("r", "t")],
                     5: [("l", "t"), ("b", "r")], 6: [("b", "t")], 7: [("l", "t")], 8: [("t", "l")],
                     9: [("t", "b")], 10: [("t", "r"), ("l", "b")], 11: [("t", "r")], 12: [("r", "l")],
                     13: [("r", "b")], 14: [("b", "l")]}[idx]
            for a, b in table:
                segs.append((e[a], e[b]))
    adj = {}
    for a, b in segs:
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)
    seen, paths = set(), []
    for a, b in segs:
        if (a, b) in seen or (b, a) in seen:
            continue
        path = [a, b]
        seen.add((a, b))
        for direction in (0, 1):
            while True:
                cur, prev = (path[-1], path[-2]) if direction == 0 else (path[0], path[1])
                nxt = [k for k in adj.get(cur, []) if k != prev and (cur, k) not in seen and (k, cur) not in seen]
                if not nxt:
                    break
                k = nxt[0]
                seen.add((cur, k))
                if direction == 0:
                    path.append(k)
                else:
                    path.insert(0, k)
                if path[0] == path[-1] and len(path) > 3:
                    break
        paths.append([pt(k) for k in path])
    return paths


def contour(R, center=(0, 0), scale=1.0, blur=0.0, levels=(0.45,), color=GREEN, spheres=ALL, w=3.5, extent=2.5, n=64):
    X, Y, Z = density(R, spheres, n=n, extent=extent, blur=blur)
    g = VGroup()
    for lv in levels:
        for p in contour_paths(Z, lv, extent):
            if len(p) < 3:
                continue
            m = VMobject()
            pts = [np.array([q[0] * scale + center[0], q[1] * scale + center[1], 0.0]) for q in p]
            m.set_points_as_corners(pts)
            m.set_stroke(color, w)
            g.add(m)
    return g


# ---- noisy images -------------------------------------------------------------------------------
BASE = np.array([40.0, 45.0, 56.0])
SIG = np.array([181.0, 140.0, 217.0])


def to_rgb(field):
    """field: 2D array, 0 = ice background, 1 = full particle signal."""
    img = BASE[None, None, :] + field[:, :, None] * (SIG - BASE)[None, None, :]
    return np.clip(img, 0, 255).astype(np.uint8)


def view_field(R, n=44, extent=2.5, spheres=ALL, blur=0.0, rot2=0.0):
    X, Y, Z = density(R, spheres, n=n, extent=extent, blur=blur)
    return Z


def noisy_tile(R, rng, sigma=0.9, amp=0.55, n=44, spheres=ALL):
    Z = view_field(R, n=n, spheres=spheres)
    return amp * np.clip(Z, 0, 1.2) + rng.randn(n, n) * sigma * amp * 0.5


def img(field, height=1.6):
    m = ImageMobject(to_rgb(field))
    m.height = height
    m.set_resampling_algorithm(RESAMPLING_ALGORITHMS["linear"])
    return m


def micrograph(rng, W=150, H=100, npart=14, amp=0.55, sigma=0.9, spheres=ALL, seed_pos=None, return_pos=False):
    """a faint, noisy field with particles in random positions and orientations."""
    field = np.zeros((H, W))
    pos = []
    k = 24
    tries = 0
    while len(pos) < npart and tries < 500:
        tries += 1
        cx, cy = rng.randint(k // 2 + 1, W - k // 2 - 1), rng.randint(k // 2 + 1, H - k // 2 - 1)
        if any((cx - a) ** 2 + (cy - b) ** 2 < (k * 1.05) ** 2 for a, b in pos):
            continue
        R = rot(rng.rand() * 6.28, rng.rand() * 6.28, rng.rand() * 6.28)
        Z = view_field(R, n=k, extent=2.5, spheres=spheres)
        field[cy - k // 2: cy - k // 2 + k, cx - k // 2: cx - k // 2 + k] += np.clip(Z, 0, 1.2)
        pos.append((cx, cy))
    field = amp * field + rng.randn(H, W) * sigma * amp * 0.5
    return (field, pos) if return_pos else field


# ---------------------------------------------------------------------------------------------
# drawing helpers
# ---------------------------------------------------------------------------------------------
def lab(text, size=24, color=GREY, **kw):
    return T(text, size, color, **kw)


def lines(*texts, size=24, color=TEXT, buff=0.12, align=LEFT, colors=None):
    g = VGroup(*[T(t, size, (colors[i] if colors else color)) for i, t in enumerate(texts)])
    return g.arrange(DOWN, aligned_edge=align, buff=buff)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow([a[0], a[1], 0], [b[0], b[1], 0], buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def poly(pts, color=YELLOW, w=5):
    m = VMobject()
    m.set_points_as_corners([np.array([p[0], p[1], 0.0]) for p in pts])
    m.set_stroke(color, w)
    return m


def blob(R, center=(0, 0), scale=1.0, color=PURPLE, op=0.85, spheres=BIG, stroke=2.0):
    """A particle as simple overlapping round blobs, seen from the direction given by R."""
    g = VGroup()
    for x, y, s, a in project(R, spheres):
        c = Circle(radius=s * 1.45 * scale, stroke_color=color, stroke_width=stroke, fill_color=color, fill_opacity=op)
        c.move_to([center[0] + x * scale, center[1] + y * scale, 0])
        g.add(c)
    return g


def cross(c, size=0.35, color=RED, w=7):
    return VGroup(Line([c[0] - size, c[1] - size, 0], [c[0] + size, c[1] + size, 0], color=color, stroke_width=w),
                  Line([c[0] - size, c[1] + size, 0], [c[0] + size, c[1] - size, 0], color=color, stroke_width=w))


def tagline(text, color=GOLD, size=24):
    return T(text, size, color)


def membrane(x0, x1, y, h=0.3, color=GREY):
    return RoundedRectangle(corner_radius=0.1, width=x1 - x0, height=h, stroke_color=color, stroke_width=2.5,
                            fill_color=color, fill_opacity=0.35).move_to([(x0 + x1) / 2, y, 0])


def axes_box(x0, x1, y0, y1, color=GREY):
    return VGroup(Line([x0, y0, 0], [x0, y1, 0], color=color, stroke_width=3),
                  Line([x0, y0, 0], [x1, y0, 0], color=color, stroke_width=3))


def fade_all(scene, *mobs, rt=0.5):
    scene.play(*[FadeOut(m) for m in mobs], run_time=rt)


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Methods library"
    TITLE = "Freezing Molecules to See Them"


# ---------------------------------------------------------------------------------------------
class S01Problem(SpokenScene):
    """the question; X-ray needs crystals, NMR small, membrane proteins clump; three obstacles for EM."""

    def construct(self):
        R0 = rot(0.4, 0.9, 0.2)
        big = blob(R0, (0, 0.2), 1.35)
        q = T("?", 80, YELLOW, weight=BOLD).move_to([0, 3.0, 0])
        ql = lab("a large protein: what shape?", 30, TEXT).move_to([0, -2.6, 0])
        self.at("How do you see")
        self.play(FadeIn(big, scale=0.9), FadeIn(q), FadeIn(ql), run_time=0.8)

        # ---- X-ray panel
        self.at("crystallography needs")
        self.play(FadeOut(big), FadeOut(q), FadeOut(ql), run_time=0.4)
        xr = chip("X-ray crystallography", BLUE, 26).move_to([-4.3, 2.9, 0])
        self.play(FadeIn(xr, shift=DOWN * 0.15), run_time=0.4)
        self.at("ordered crystals")
        cx, cy = -4.3, 0.2
        box = Rectangle(width=4.2, height=4.2, stroke_color=GREY, stroke_width=3).move_to([cx, cy, 0])
        lat = VGroup(*[blob(R0, (cx + (i - 1) * 1.3, cy + (j - 1) * 1.3), 0.43) for i in range(3) for j in range(3)])
        self.play(Create(box), FadeIn(lat, lag_ratio=0.08), run_time=1.2)
        cl = lab("a well-ordered crystal", 24, GREY).move_to([cx, -2.2, 0])
        self.play(FadeIn(cl), run_time=0.3)

        # ---- NMR panel
        self.at("in solution")
        nm = chip("NMR in solution", BLUE, 26).move_to([0, 2.9, 0])
        self.play(FadeIn(nm, shift=DOWN * 0.15), run_time=0.4)
        self.at("relatively small proteins")
        sm = blob(rot(0.2, 0.5, 0.9), (0, 0.5), 0.8)
        sl = lines("only relatively", "small proteins", size=26, color=TEXT, align=ORIGIN, buff=0.1).move_to([0, -1.5, 0])
        self.play(FadeIn(sm, scale=0.8), FadeIn(sl), run_time=0.6)

        # ---- membrane proteins clump
        self.at("Membrane proteins pulled out")
        mp = chip("membrane proteins", BLUE, 26).move_to([4.3, 2.9, 0])
        mem = membrane(2.4, 6.2, 1.5)
        pr = [blob(rot(0.3 * k, 0.8, 0.4), (3.0 + 1.3 * k, 1.5), 0.3) for k in range(3)]
        self.play(FadeIn(mp, shift=DOWN * 0.15), FadeIn(mem), *[FadeIn(p) for p in pr], run_time=0.6)
        self.play(*[p.animate.shift(DOWN * 1.9) for p in pr], run_time=0.8)
        self.at("tend to clump")
        tgt = [(3.8, -0.45), (4.35, -0.2), (4.8, -0.5)]
        self.play(*[p.animate.move_to([t[0], t[1], 0]) for p, t in zip(pr, tgt)], run_time=0.8)
        ring = Ellipse(width=2.6, height=1.7, stroke_color=RED, stroke_width=3).move_to([4.3, -0.4, 0])
        cll = lab("clump together", 26, RED).move_to([4.3, -1.7, 0])
        self.play(Create(ring), FadeIn(cll), run_time=0.5)

        # ---- the three obstacles
        self.at("Electron microscopy had")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        heads = [chip("The beam burns it", YELLOW, 26), chip("Low contrast", YELLOW, 26), chip("Vacuum dries it", YELLOW, 26)]
        xs = [-4.5, 0.0, 4.5]
        for h, x in zip(heads, xs):
            h.move_to([x, 2.9, 0])
        title = lab("electron microscopy: three obstacles", 28, TEXT).move_to([0, 3.7 - 0.0, 0])
        title.set_y(3.6)
        for h in heads:
            h.set_y(2.7)
        self.play(FadeIn(title), run_time=0.4)

        self.at("The beam burns")
        self.play(FadeIn(heads[0], shift=DOWN * 0.1), run_time=0.3)
        b1 = blob(R0, (xs[0], -0.1), 1.0)
        beams = VGroup(*[arr([xs[0] + d, 2.0, 0], [xs[0] + d, 1.3, 0], YELLOW, w=6, tip=0.2) for d in (-0.7, 0, 0.7)])
        self.play(FadeIn(b1), run_time=0.3)
        self.play(*[GrowArrow(a) for a in beams], run_time=0.5)
        self.play(b1.animate.set_color(RED).set_opacity(0.45), run_time=0.7)
        bl = lab("burns biological material", 24, RED).move_to([xs[0], -2.4, 0])
        self.play(FadeIn(bl), run_time=0.3)

        self.at("A weaker beam")
        self.play(FadeIn(heads[1], shift=DOWN * 0.1), run_time=0.3)
        rng = np.random.RandomState(4)
        tile = img(noisy_tile(R0, rng, sigma=1.5, amp=0.45, n=60), 3.2).move_to([xs[1], -0.2, 0])
        weak = arr([xs[1], 2.0, 0], [xs[1], 1.5, 0], YELLOW, w=3, tip=0.14).set_opacity(0.6)
        self.play(FadeIn(weak), FadeIn(tile), run_time=0.6)
        cl2 = lab("a weaker beam: faint image", 24, TEXT).move_to([xs[1], -2.4, 0])
        self.play(FadeIn(cl2), run_time=0.3)

        self.at("the vacuum dries")
        self.play(FadeIn(heads[2], shift=DOWN * 0.1), run_time=0.3)
        b3 = blob(R0, (xs[2], -0.1), 1.0)
        water = Circle(radius=1.85, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.18).move_to([xs[2], -0.1, 0])
        wl = lab("water", 26, TEXT).move_to([xs[2], 2.05, 0])
        self.play(FadeIn(water), FadeIn(b3), FadeIn(wl), run_time=0.5)
        self.play(water.animate.scale(0.1).set_opacity(0.0), FadeOut(wl),
                  b3.animate.set_color(GREY).set_opacity(0.5), run_time=1.0)
        dl = lab("dries out the sample", 24, RED).move_to([xs[2], -2.4, 0])
        self.play(FadeIn(dl), run_time=0.3)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Freeze(SpokenScene):
    """purify; thin film on a grid; blot; plunge in ethane; water becomes glass; particles held in water."""

    def construct(self):
        rng = np.random.RandomState(2)
        # ---- purify: a mixed set becomes identical
        mixed = VGroup()
        sets = [BIG, BIG_B, BIG, BIG_B, BIG, BIG_B]
        xs6 = [-5.9 + 1.5 * k for k in range(6)]
        for k in range(6):
            mixed.add(blob(rot(rng.rand() * 6, rng.rand() * 6, rng.rand() * 6), (xs6[k], 3.0), 0.34 + 0.08 * (k % 2),
                           spheres=sets[k], color=PURPLE if k % 2 else GREY))
        R0 = rot(0.4, 0.9, 0.2)
        same = VGroup(*[blob(R0, (xs6[k], 3.0), 0.38) for k in range(6)])
        self.at("Purify the molecule")
        self.play(FadeIn(mixed, lag_ratio=0.1), run_time=0.7)
        self.play(ReplacementTransform(mixed, same), run_time=0.8)
        idl = lab("identical particles", 26, PURPLE).move_to([4.9, 3.0, 0])
        self.at("identical particles")
        self.play(FadeIn(idl), run_time=0.3)

        # ---- the grid (top view), a drop, blotting
        self.at("Spread a small drop")
        gc = np.array([-3.4, -0.4, 0.0])
        gr = 1.9
        grid = VGroup(Circle(radius=gr, stroke_color=BLUE, stroke_width=4).move_to(gc))
        for t in np.linspace(-1.4, 1.4, 5):
            h = np.sqrt(max(0, gr ** 2 - t ** 2))
            grid.add(Line([gc[0] + t, gc[1] - h, 0], [gc[0] + t, gc[1] + h, 0], color=BLUE, stroke_width=1.5))
            grid.add(Line([gc[0] - h, gc[1] + t, 0], [gc[0] + h, gc[1] + t, 0], color=BLUE, stroke_width=1.5))
        gl = lab("fine metal mesh grid", 24, BLUE).move_to([gc[0], -2.75, 0])
        drop = Circle(radius=1.3, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.35).move_to(gc)
        dp = VGroup(*[blob(R0, (gc[0] + dx, gc[1] + dy), 0.17) for dx, dy in [(-0.6, 0.55), (0.4, 0.65), (-0.25, -0.1), (0.65, -0.15), (-0.65, -0.65), (0.2, -0.7)]])
        self.play(FadeIn(grid), FadeIn(gl), run_time=0.4)
        self.play(FadeIn(drop), FadeIn(dp), run_time=0.4)
        self.at("blot it")
        paper = Rectangle(width=1.4, height=3.4, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.35).move_to(gc + [3.4, 0, 0])
        pl = lab("blotting", 24, GREY).move_to(gc + [3.4, 2.1, 0])
        self.play(FadeIn(paper), FadeIn(pl), paper.animate.move_to(gc + [0.7, 0, 0]), run_time=0.3)
        film = Circle(radius=1.7, stroke_color=TEAL, stroke_width=1.5, fill_color=TEAL, fill_opacity=0.10).move_to(gc)
        self.play(ReplacementTransform(drop, film), paper.animate.move_to(gc + [3.4, 0, 0]), run_time=0.3)
        fl = lab("a thin film", 24, TEAL).move_to(gc + [0.0, 2.35, 0])
        self.play(FadeOut(paper), FadeOut(pl), FadeIn(fl), run_time=0.2)

        # ---- plunge into ethane
        self.at("plunge it into")
        bath = Rectangle(width=5.6, height=2.9, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.12).move_to([3.6, -1.6, 0])
        cup = Rectangle(width=3.6, height=1.9, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.25).move_to([3.6, -1.4, 0])
        bl1 = lab("liquid nitrogen", 24, BLUE).move_to([3.6, -3.25, 0])
        bl2 = lab("liquid ethane", 24, TEAL).move_to([3.6, -2.15, 0])
        self.play(FadeIn(bath), FadeIn(cup), FadeIn(bl1), FadeIn(bl2), run_time=0.4)
        bar = VGroup(Rectangle(width=1.7, height=0.14, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.6),
                     Rectangle(width=1.4, height=0.06, stroke_width=0, fill_color=TEAL, fill_opacity=0.9).shift(UP * 0.1),
                     Line([0, 0.07, 0], [0, 1.3, 0], color=GREY, stroke_width=4)).move_to([3.6, 1.4, 0])
        self.play(FadeOut(fl), FadeOut(gl), run_time=0.2)
        self.play(FadeOut(VGroup(grid, film, dp)), FadeIn(bar), run_time=0.4)
        self.play(bar.animate.shift(DOWN * 2.2), run_time=0.7)

        # ---- glass, not crystals
        self.at("Cooling this fast")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)
        fast = lab("cooling this fast", 30, BLUE).move_to([0, 3.2, 0])
        self.play(FadeIn(fast), run_time=0.3)
        self.at("turns the water into glass")
        gx, gy = 3.5, 0.2
        glass = Rectangle(width=5.8, height=3.2, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.12).move_to([gx, gy, 0])
        dots = VGroup(*[Dot([gx + rng.uniform(-2.7, 2.7), gy + rng.uniform(-1.45, 1.45), 0], radius=0.05, color=TEAL) for _ in range(60)])
        gparts = VGroup(*[blob(R0, (gx + dx, gy + dy), 0.2) for dx, dy in [(-1.5, 0.6), (0.2, -0.4), (1.6, 0.5)]])
        gtitle = lab("a glass: vitreous ice", 28, TEAL).move_to([gx, gy + 2.2, 0])
        self.play(FadeIn(glass), FadeIn(dots), FadeIn(gparts), FadeIn(gtitle), run_time=0.7)
        self.at("not crystals")
        cx0, cy0 = -3.5, 0.2
        cr = Rectangle(width=5.8, height=3.2, stroke_color=GREY, stroke_width=3).move_to([cx0, cy0, 0])
        lat = VGroup(*[Dot([cx0 - 2.4 + i * 0.48, cy0 - 1.3 + j * 0.43, 0], radius=0.055, color=GREY) for i in range(11) for j in range(7)])
        ct = lab("ice crystals", 28, GREY).move_to([cx0, cy0 + 2.2, 0])
        self.play(FadeIn(cr), FadeIn(lat), FadeIn(ct), run_time=0.6)
        x = cross([cx0, cy0], 1.0, RED, 10)
        self.play(Create(x), run_time=0.3)

        # ---- a glass scatters evenly
        self.at("A glass is disordered")
        self.play(FadeOut(cr), FadeOut(lat), FadeOut(ct), FadeOut(x), FadeOut(fast), FadeOut(gtitle), run_time=0.4)
        gg = VGroup(glass, dots, gparts)
        self.play(gg.animate.scale(1.3).move_to([0, 0.5, 0]), run_time=0.6)
        beams = VGroup(*[arr([bx, 3.55, 0], [bx, 2.7, 0], YELLOW, w=5, tip=0.18) for bx in (-2.2, 0, 2.2)])
        self.at("so the beam scatters evenly")
        self.play(*[GrowArrow(a) for a in beams], run_time=0.4)
        fan = VGroup()
        for bx in (-2.2, 0, 2.2):
            for ang in (-0.5, -0.25, 0, 0.25, 0.5):
                fan.add(arr([bx, -1.65, 0], [bx + 1.1 * np.sin(ang), -1.65 - 0.9 * np.cos(ang), 0], YELLOW, w=2, tip=0.1).set_opacity(0.5))
        self.play(FadeIn(fan), run_time=0.5)
        self.at("the background is uniform")
        uni = Rectangle(width=8.4, height=0.5, stroke_width=0, fill_color=GREEN, fill_opacity=0.35).move_to([0, -3.1, 0])
        ul = lab("a uniform background", 26, GREEN).move_to([0, -3.1, 0])
        self.play(FadeIn(uni), FadeIn(ul), run_time=0.4)

        # ---- the particles stay in water
        self.at("The molecules stay in water")
        self.play(FadeOut(beams), FadeOut(fan), FadeOut(uni), FadeOut(ul), run_time=0.4)
        wl = lab("held in water", 28, TEAL).move_to([0, -2.4, 0])
        self.play(FadeIn(wl), run_time=0.3)
        self.at("not dried or stained")
        n1 = chip("dried", RED, 26).move_to([-5.0, 0.5, 0])
        n2 = chip("stained", RED, 26).move_to([5.0, 0.5, 0])
        x1 = cross(n1.get_left() + [-0.5, 0, 0], 0.3, RED, 6)
        x2 = cross(n2.get_right() + [0.45, 0, 0], 0.3, RED, 6)
        self.play(FadeIn(n1), FadeIn(n2), run_time=0.3)
        self.play(Create(x1), Create(x2), run_time=0.3)

        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Image(SpokenScene):
    """image at LN2 temperature; random orientations; low contrast and the CTF; dose; movie alignment."""

    def construct(self):
        rng = np.random.RandomState(3)
        # ---- microscope column on the left
        sx = -5.0
        src = chip("electron beam", YELLOW, 26).move_to([sx, 3.1, 0])
        gridbar = Rectangle(width=2.2, height=0.14, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.5).move_to([sx, 0.7, 0])
        gl = lines("frozen grid", size=24, color=BLUE, buff=0.08).move_to([sx + 3.0, 0.7, 0]).align_to([sx + 1.35, 0, 0], LEFT)
        det = Rectangle(width=3.0, height=0.2, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.3).move_to([sx, -2.7, 0])
        dl = lab("detector", 24, GREY).move_to([sx, -3.2, 0])
        b_in = VGroup(*[arr([sx + d, 2.5, 0], [sx + d, 0.85, 0], YELLOW, w=5, tip=0.16) for d in (-0.7, 0, 0.7)])
        b_out = VGroup(*[arr([sx + d, 0.55, 0], [sx + d, -2.5, 0], YELLOW, w=3, tip=0.14).set_opacity(0.6) for d in (-0.7, 0, 0.7)])
        self.at("Image the frozen grid")
        self.play(FadeIn(src), FadeIn(gridbar), FadeIn(det), FadeIn(dl), run_time=0.5)
        self.play(FadeIn(gl), *[GrowArrow(a) for a in b_in], *[GrowArrow(a) for a in b_out], run_time=0.7)

        # ---- ice layer with particles at random orientations (flat projections)
        self.at("random orientations")
        ix, iy = 3.5, 1.35
        ice = Rectangle(width=5.6, height=2.9, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.10).move_to([ix, iy, 0])
        it = lab("particles in the ice", 24, TEAL).move_to([ix, iy + 1.75, 0])
        views = []
        for k in range(8):
            R = rot(rng.rand() * 6.28, rng.rand() * 6.28, rng.rand() * 6.28)
            views.append(R)
        parts = VGroup(*[blob(views[k], (ix - 2.15 + 1.25 * (k // 2), iy + (0.6 if k % 2 else -0.6)), 0.27) for k in range(8)])
        self.play(FadeIn(ice), FadeIn(it), FadeIn(parts, lag_ratio=0.1), run_time=0.9)
        self.at("a flat projection of a different view")
        vy = -1.3
        ez = VGroup()
        for k, R in enumerate([views[0], views[2], views[5], views[7]]):
            ez.add(blob(R, (ix - 2.1 + 1.4 * k, vy), 0.4, spheres=BIG + FINE, op=0.28, stroke=1.2))
        vl = lab("a different view each time", 24, TEXT).move_to([ix, -2.9, 0])
        vb = Rectangle(width=5.6, height=2.4, stroke_color=GREY, stroke_width=2).move_to([ix, vy - 0.15, 0])
        self.play(FadeIn(vb), FadeIn(ez, lag_ratio=0.15), FadeIn(vl), run_time=0.8)

        # ---- low contrast, out of focus, CTF
        self.at("Contrast is very low")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)
        col_x = [-4.5, 0.0, 4.5]
        cy = 0.8
        t1 = chip("contrast is very low", YELLOW, 24).move_to([col_x[0], 3.0, 0])
        faint = img(noisy_tile(views[0], rng, sigma=1.6, amp=0.45, n=60), 3.5).move_to([col_x[0], cy, 0])
        self.play(FadeIn(t1), FadeIn(faint), run_time=0.5)
        self.at("out of focus")
        uf = lab("so: taken out of focus", 24, TEXT).move_to([col_x[0], -1.5, 0])
        self.play(FadeIn(uf), run_time=0.3)
        self.at("contrast transfer function")
        xx = np.linspace(0.02, 1, 160)
        yy = np.sin(14 * xx ** 2) * np.exp(-2.0 * xx)
        crv = poly([[col_x[1] - 2.0 + 4.0 * xx[i], cy + 1.5 * yy[i]] for i in range(len(xx))], YELLOW, 4)
        base = DashedLine([col_x[1] - 2.0, cy, 0], [col_x[1] + 2.0, cy, 0], color=GREY, stroke_width=2)
        ax = axes_box(col_x[1] - 2.0, col_x[1] + 2.0, cy - 1.75, cy + 1.75)
        t2 = chip("contrast transfer function", YELLOW, 24).move_to([col_x[1], 3.0, 0])
        self.play(FadeIn(t2), Create(ax), FadeIn(base), Create(crv, run_time=1.0, rate_func=linear))
        cm = lab("modulates each image", 24, TEXT).move_to([col_x[1], -1.5, 0])
        self.play(FadeIn(cm), run_time=0.3)
        self.at("measured per image and corrected")
        ck = lab("measured per image, corrected", 24, GREEN).move_to([col_x[1], -2.15, 0])
        self.play(FadeIn(ck), run_time=0.4)

        # ---- dose limit
        self.at("Radiation damage limits")
        t3 = chip("radiation damage", RED, 24).move_to([col_x[2], 3.0, 0])
        bar_o = Rectangle(width=1.2, height=3.5, stroke_color=GREY, stroke_width=3).move_to([col_x[2], cy, 0])
        fill = Rectangle(width=1.16, height=0.05, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9).move_to([col_x[2], cy - 1.725, 0])
        limit = DashedLine([col_x[2] - 1.0, cy + 1.2, 0], [col_x[2] + 1.0, cy + 1.2, 0], color=RED, stroke_width=4)
        ll = lab("limits the dose", 24, RED).move_to([col_x[2], -1.5, 0])
        self.play(FadeIn(t3), Create(bar_o), FadeIn(fill), run_time=0.4)
        self.play(fill.animate.stretch_to_fit_height(2.85, about_edge=DOWN).move_to([col_x[2], cy - 1.75 + 1.425, 0]), run_time=0.9)
        self.play(Create(limit), FadeIn(ll), run_time=0.4)

        self.finish()


# ---------------------------------------------------------------------------------------------
VA = rot(0.4, 0.9, 0.2)
VB = rot(1.8, 0.3, 1.0)
VC = rot(2.6, 1.4, 0.5)
VD = rot(0.9, 2.2, 2.0)


def avg_tile(R, n, seed, sigma=1.5, amp=0.5, pix=60):
    r = np.random.RandomState(seed)
    return np.mean([noisy_tile(R, r, sigma=sigma, amp=amp, n=pix) for _ in range(n)], axis=0)


class S04Reconstruct(SpokenScene):
    """pick particles; align and sort into 2D classes; average; build and refine a 3D map; 3D classes."""

    def construct(self):
        rng = np.random.RandomState(8)
        W, H = 150, 100
        field, pos = micrograph(rng, W, H, npart=10, amp=0.5, sigma=1.1, return_pos=True)
        mg = img(field, 4.2).move_to([-3.9, 0.7, 0])
        sc = mg.width / W
        self.at("Software picks")
        self.play(FadeIn(mg), run_time=0.5)
        boxes = VGroup(*[Square(side_length=0.85, stroke_color=GREEN, stroke_width=3).move_to(
            [mg.get_center()[0] + (cx - W / 2) * sc, mg.get_center()[1] - (cy - H / 2) * sc, 0]) for cx, cy in pos])
        ml = lab("particles picked from the image", 24, GREEN).move_to([-3.9, -1.75, 0])
        self.play(Create(boxes, lag_ratio=0.05), FadeIn(ml), run_time=0.7)

        # tiles: two views, each with a random in-plane turn
        spots = [(1.7 + 1.1 * (k % 4), 2.2 - 1.2 * (k // 4)) for k in range(8)]
        kinds = [VA, VB, VA, VB, VB, VA, VA, VB]
        turns = [0.9, -1.2, 2.0, 0.5, -0.7, 1.6, -2.1, 1.1]
        tiles = Group()
        for k in range(8):
            t = img(noisy_tile(kinds[k], np.random.RandomState(40 + k), sigma=1.3, amp=0.55, n=44), 0.95).move_to([spots[k][0], spots[k][1], 0])
            t.rotate(turns[k])
            tiles.add(t)
        self.at("aligns them")
        self.play(FadeIn(tiles, lag_ratio=0.05), run_time=0.4)
        self.play(*[t.animate.rotate(-turns[k]) for k, t in enumerate(tiles)], run_time=0.5)
        self.at("sorts similar views")
        pa = [(1.8, 1.9), (2.8, 1.9), (1.8, 0.9), (2.8, 0.9)]
        pb = [(4.7, 1.9), (5.7, 1.9), (4.7, 0.9), (5.7, 0.9)]
        ia = [k for k in range(8) if kinds[k] is VA]
        ib = [k for k in range(8) if kinds[k] is VB]
        anims = [tiles[k].animate.move_to([pa[i][0], pa[i][1], 0]) for i, k in enumerate(ia)] + \
                [tiles[k].animate.move_to([pb[i][0], pb[i][1], 0]) for i, k in enumerate(ib)]
        self.play(*anims, run_time=0.9)
        self.at("2D classes")
        c1 = lab("class 1", 26, TEXT).move_to([2.3, 2.85, 0])
        c2 = lab("class 2", 26, TEXT).move_to([5.2, 2.85, 0])
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.4)
        self.at("Averaging a class")
        aA = img(avg_tile(VA, 40, 1), 2.0).move_to([2.3, -1.4, 0])
        aB = img(avg_tile(VB, 40, 2), 2.0).move_to([5.2, -1.4, 0])
        ar1 = arr([2.3, 0.2, 0], [2.3, -0.3, 0], GREEN, w=5, tip=0.15)
        ar2 = arr([5.2, 0.2, 0], [5.2, -0.3, 0], GREEN, w=5, tip=0.15)
        al = lab("average: sharper", 24, GREEN).move_to([3.75, -2.75, 0])
        self.play(GrowArrow(ar1), GrowArrow(ar2), FadeIn(aA), FadeIn(aB), FadeIn(al), run_time=0.9)

        # ---- 3D
        self.at("Then work out")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        imgs = Group(*[img(avg_tile(R, 40, 5 + i), 2.0).move_to(p) for i, (R, p) in enumerate(
            [(VA, [-5.2, 1.7, 0]), (VB, [-5.2, -1.7, 0]), (VC, [5.2, 1.7, 0]), (VD, [5.2, -1.7, 0])])])
        self.play(FadeIn(imgs, lag_ratio=0.15), run_time=0.8)
        self.at("build a starting model")
        m_lo = contour(VA, (0, 0.2), 1.25, blur=0.7, levels=(0.3, 0.85), color=GREEN, w=4)
        arrs = VGroup(*[arr([a * 3.9, b * 1.5, 0], [a * 1.9, b * 0.6, 0], GREY, w=4, tip=0.15) for a in (-1, 1) for b in (-1, 1)])
        ml1 = lab("3D starting model", 26, GREEN).move_to([0, -2.7, 0])
        self.play(*[GrowArrow(a) for a in arrs], Create(m_lo), FadeIn(ml1), run_time=1.0)
        self.at("refine it against")
        m_hi = contour(VA, (0, 0.2), 1.25, blur=0.0, levels=(0.3, 0.85), color=GREEN, w=4)
        ml2 = lab("refined against the particle images", 26, GREEN).move_to([0, -2.7, 0])
        self.play(FadeOut(m_lo), FadeIn(m_hi), ReplacementTransform(ml1, ml2), run_time=0.9)
        self.at("more than one shape")
        self.play(*[FadeOut(m) for m in (imgs, arrs, m_hi, ml2)], run_time=0.5)
        mA = contour(VA, (-3.2, 0.5), 1.3, levels=(0.3, 0.85), color=GREEN, w=4)
        mB = contour(VA, (3.2, 0.5), 1.3, levels=(0.3, 0.85), color=GREEN, spheres=BIG_B + FINE, w=4)
        la = lab("3D class 1", 28, TEXT).move_to([-3.2, -2.3, 0])
        lb = lab("3D class 2", 28, TEXT).move_to([3.2, -2.3, 0])
        self.at("separate 3D classes")
        self.play(Create(mA), Create(mB), FadeIn(la), FadeIn(lb), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Reading(SpokenScene):
    """example micrograph; class average sharpening; 3D map; half-map agreement curve; resolution is a guideline."""

    def construct(self):
        rng = np.random.RandomState(9)
        W, H = 150, 100
        field, pos0 = micrograph(rng, W, H, npart=14, amp=0.5, sigma=1.1, return_pos=True)
        mg = img(field, 4.4).move_to([-3.0, 0.3, 0])
        ex = lab("example, idealised", 24, GOLD).move_to([-3.0, 3.0, 0])
        self.at("The raw micrograph")
        self.play(FadeIn(mg), FadeIn(ex), run_time=0.6)
        ice = lab("grey ice", 26, GREY).move_to([-3.0, -2.2, 0])
        self.play(FadeIn(ice), run_time=0.3)
        self.at("faint, noisy shape")
        # point at one particle
        cx0, cy0 = pos0[0]
        tgt = [mg.get_center()[0] + (cx0 - W / 2) * mg.width / W, mg.get_center()[1] - (cy0 - H / 2) * mg.width / W]
        cl = lines("each particle:", "a faint, noisy shape", size=28, color=TEXT, align=LEFT).move_to([4.2, 1.6, 0])
        self.play(FadeIn(cl), run_time=0.4)
        a1 = arr([2.2, 1.6], [tgt[0] + 0.5, tgt[1] + 0.1], TEXT, w=4, tip=0.18)
        self.play(GrowArrow(a1), run_time=0.4)

        self.at("A class average sums")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)
        cx = [-4.3, 0.0, 4.3]
        tl = [img(avg_tile(VA, n, 3, pix=60), 3.2).move_to([x, 0.5, 0]) for n, x in zip((1, 8, 80), cx)]
        names = ["one image", "more images", "many aligned images"]
        for im, nm, x in zip(tl, names, cx):
            pass
        self.play(FadeIn(tl[0]), FadeIn(lab(names[0], 26, TEXT).move_to([cx[0], -1.6, 0])), run_time=0.4)
        self.play(FadeIn(tl[1]), FadeIn(lab(names[1], 26, TEXT).move_to([cx[1], -1.6, 0])), run_time=0.4)
        self.play(FadeIn(tl[2]), FadeIn(lab(names[2], 26, TEXT).move_to([cx[2], -1.6, 0])), run_time=0.4)
        exl = lab("example, idealised", 24, GOLD).move_to([0, 3.0, 0])
        self.play(FadeIn(exl), run_time=0.3)
        self.at("noise falls")
        nf = lab("noise falls, features appear", 28, GREEN).move_to([0, -2.6, 0])
        self.play(FadeIn(nf), run_time=0.4)

        self.at("The final output")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)
        R = VA
        mp = contour(R, (-3.8, 0.9), 1.1, levels=(0.3, 0.85), color=GREEN, w=4)
        mpl = lab("3D map", 30, GREEN).move_to([-3.8, -1.5, 0])
        self.play(Create(mp), FadeIn(mpl), run_time=0.8)
        self.at("stated resolution")
        rs = chip("a stated resolution", GREEN, 28).move_to([-3.8, -2.6, 0])
        self.play(FadeIn(rs), run_time=0.4)
        self.at("splitting the data in two")
        h1 = contour(R, (-5.3, 0.9), 0.6, levels=(0.3, 0.85), color=GREEN, w=3)
        h2 = contour(R, (-2.4, 0.9), 0.6, levels=(0.3, 0.85), color=GREEN, w=3, spheres=ALL)
        hl1 = lab("half 1", 24, TEXT).move_to([-5.3, -0.7, 0])
        hl2 = lab("half 2", 24, TEXT).move_to([-2.4, -0.7, 0])
        self.play(FadeOut(mp), FadeOut(mpl), FadeOut(rs), FadeIn(h1), FadeIn(h2), FadeIn(hl1), FadeIn(hl2), run_time=0.8)
        self.at("how well the halves agree")
        ox, oy = 1.4, -2.3
        axs = axes_box(ox, ox + 4.8, oy, oy + 4.6)
        xx = np.linspace(0, 1, 100)
        yy = 1.0 / (1.0 + np.exp((xx - 0.62) * 9))
        curve = poly([[ox + 4.8 * xx[i], oy + 0.2 + 4.2 * yy[i]] for i in range(100)], GREEN, 5)
        yl = lab("agreement", 24, TEXT).move_to([ox + 0.2, oy + 4.9, 0]).align_to([ox - 0.1, 0, 0], LEFT)
        xl = lab("finer detail", 24, TEXT).move_to([ox + 2.4, oy - 0.45, 0])
        ex2 = lab("example, idealised", 24, GOLD).move_to([ox + 3.4, oy + 4.95, 0])
        self.play(Create(axs), FadeIn(yl), FadeIn(xl), FadeIn(ex2), Create(curve, run_time=1.3, rate_func=linear))
        thr = DashedLine([ox, oy + 0.2 + 4.2 * 0.18, 0], [ox + 4.8, oy + 0.2 + 4.2 * 0.18, 0], color=GREY, stroke_width=3)
        tl_ = lab("cut-off", 24, GREY).move_to([ox + 4.3, oy + 0.2 + 4.2 * 0.18 + 0.35, 0])
        self.play(Create(thr), FadeIn(tl_), run_time=0.5)
        self.at("broad guideline")
        xc = ox + 4.8 * 0.73
        band = Rectangle(width=0.9, height=4.6, stroke_width=0, fill_color=YELLOW, fill_opacity=0.25).move_to([xc, oy + 2.3, 0])
        bl = lab("resolution: a broad guideline", 24, YELLOW).move_to([ox + 2.4, oy + 5.65, 0])
        self.play(FadeIn(band), FadeIn(bl), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Pitfalls(SpokenScene):
    """overfitting (noise aligned to a pattern; halves as control); air-water interface (stuck, one view)."""

    def construct(self):
        rng = np.random.RandomState(12)
        pix = 44
        tmpl = view_field(VA, n=pix)
        pool = [rng.randn(pix, pix) * 0.9 for _ in range(600)]
        corr = [float((p * tmpl).sum()) for p in pool]
        order = np.argsort(corr)[::-1]
        fake = np.mean([pool[i] for i in order[:60]], axis=0) * 0.5
        self.at("Overfitting")
        nt = Group(*[img(pool[k] * 0.5, 1.3).move_to([-5.4 + 1.5 * (k % 3), 1.9 - 1.5 * (k // 3), 0]) for k in range(6)])
        nl = lab("pure noise", 26, GREY).move_to([-4.0, -1.2, 0])
        self.play(FadeIn(nt, lag_ratio=0.1), FadeIn(nl), run_time=0.8)
        self.at("aligning noise")
        ft = img(fake * 2.2, 2.6).move_to([-0.3, 0.8, 0])
        ar = arr([-2.1, 0.8, 0], [-1.7, 0.8, 0], RED, w=5, tip=0.15)
        fl = lab("aligned to a reference", 24, RED).move_to([-0.3, -0.9, 0])
        fl2 = lab("a feature made from noise", 24, RED).move_to([-0.3, -1.4, 0])
        self.play(GrowArrow(ar), FadeIn(ft), FadeIn(fl), FadeIn(fl2), run_time=0.9)
        self.at("inflate the resolution")
        ox, oy = 2.6, -2.0
        axs = axes_box(ox, ox + 3.4, oy, oy + 3.6)
        xx = np.linspace(0, 1, 80)
        hi = poly([[ox + 3.4 * x, oy + 0.2 + 3.2 / (1 + np.exp((x - 0.8) * 9))] for x in xx], RED, 5)
        self.play(Create(axs), Create(hi, run_time=0.9, rate_func=linear), run_time=0.9)
        il = lab("inflated resolution", 24, RED).move_to([ox + 1.7, oy + 4.15, 0])
        sch = lab("schematic, not real data", 24, GOLD).move_to([ox + 1.7, oy + 4.8, 0])
        axl = lab("agreement", 22, TEXT).rotate(PI / 2).move_to([ox - 0.4, oy + 1.8, 0])
        self.play(FadeIn(il), FadeIn(sch), FadeIn(axl), run_time=0.3)
        self.at("refine halves of the data independently")
        lo = poly([[ox + 3.4 * x, oy + 0.2 + 3.2 / (1 + np.exp((x - 0.45) * 9))] for x in xx], GREEN, 5)
        gl = lab("independent halves", 24, GREEN).move_to([ox + 1.7, oy - 0.45, 0])
        xdl = lab("finer detail", 22, TEXT).move_to([ox + 1.7, oy - 0.9, 0])
        self.play(Create(lo, run_time=0.9, rate_func=linear), FadeIn(gl), FadeIn(xdl), run_time=0.9)

        # ---- air-water interface
        self.at("In one tomography survey")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        band = Rectangle(width=11.0, height=1.7, stroke_width=0, fill_color=TEAL, fill_opacity=0.15).move_to([0, 1.5, 0])
        top = Line([-5.5, 2.35, 0], [5.5, 2.35, 0], color=RED, stroke_width=4)
        bot = Line([-5.5, 0.65, 0], [5.5, 0.65, 0], color=RED, stroke_width=4)
        tl = lab("air-water interface", 24, RED).move_to([-4.2, 2.85, 0])
        bl = lab("air-water interface", 24, RED).move_to([-4.2, 0.2, 0])
        spots = [(-4.5, 1.2), (-3.2, 1.8), (-1.8, 1.0), (-0.6, 1.9), (0.8, 1.2), (2.0, 1.7), (3.2, 1.0), (-2.6, 1.5), (1.5, 1.4), (4.0, 1.8)]
        rr = np.random.RandomState(3)
        parts = VGroup(*[blob(rot(rr.rand() * 6, rr.rand() * 6, rr.rand() * 6), s, 0.2) for s in spots])
        self.play(FadeIn(band), Create(top), Create(bot), FadeIn(tl), FadeIn(bl), FadeIn(parts), run_time=1.0)
        self.at("stuck to")
        targets = []
        for k in range(10):
            if k == 4:
                targets.append(spots[k])
            elif k % 2 == 0:
                targets.append((spots[k][0], 2.1))
            else:
                targets.append((spots[k][0], 0.9))
        self.play(*[p.animate.move_to([t[0], t[1], 0]) for p, t in zip(parts, targets)], run_time=1.2)
        self.at("denature protein")
        self.play(*[p.animate.set_color(RED).set_opacity(0.6) for k, p in enumerate(parts) if k != 4], run_time=0.8)
        dl = lab("can denature protein", 26, RED).move_to([0, -0.5, 0])
        self.play(FadeIn(dl), run_time=0.3)
        self.at("too few views")
        same = [blob(VA, (t[0], t[1]), 0.2, color=RED, op=0.6) for k, t in enumerate(targets) if k != 4]
        self.play(*[ReplacementTransform(parts[k], same[i]) for i, k in enumerate([k for k in range(10) if k != 4])], run_time=0.8)
        vl = lab("often the same view: too few views", 26, TEXT).move_to([0, -1.2, 0])
        self.play(FadeIn(vl), run_time=0.4)
        self.at("Thicker ice")
        chs = [chip("thicker ice", GREEN, 26), chip("a little detergent", GREEN, 26), chip("a thin support film", GREEN, 26)]
        xs = [-4.4, 0.0, 4.4]
        grp = VGroup()
        for c, x in zip(chs, xs):
            c.move_to([x, -2.4, 0])
            t = lab("costs contrast" if x != 0.0 else " ", 24, RED).move_to([x, -3.1, 0])
            grp.add(c, t)
        self.play(FadeIn(grp[0], shift=UP * 0.1), run_time=0.4)
        self.at("detergent")
        self.play(FadeIn(grp[2], shift=UP * 0.1), run_time=0.4)
        self.at("thin support")
        self.play(FadeIn(grp[4], shift=UP * 0.1), run_time=0.4)
        self.at("cost contrast")
        self.play(FadeIn(grp[1]), FadeIn(grp[3]), FadeIn(grp[5]), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07Piezo(SpokenScene):
    """Piezo1: a large membrane protein that did not crystallise; domed membrane; tension and projected area."""

    def construct(self):
        R0 = rot(0.4, 0.9, 0.2)
        self.at("Mouse Piezo")
        mem = membrane(-5.0, 5.0, 0.0, h=0.3)
        pz = blob(R0, (0, 0.7), 1.1)
        pl = lab("mouse Piezo1: a large, flexible membrane protein", 28, TEXT).move_to([0, 3.0, 0])
        self.play(FadeIn(mem), FadeIn(pz), FadeIn(pl), run_time=0.8)
        self.at("In 2017")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        tag = lab("Guo and MacKinnon, 2017", 28, GOLD).move_to([0, 3.4, 0])
        self.play(FadeIn(tag), run_time=0.4)
        self.at("closed trimer")
        blades = VGroup()
        for k in range(3):
            e = Ellipse(width=2.4, height=0.85, stroke_color=GREEN, stroke_width=4, fill_color=GREEN, fill_opacity=0.15)
            e.shift(RIGHT * 1.15).rotate(k * 2 * np.pi / 3 + 0.5, about_point=ORIGIN)
            blades.add(e)
        hub = Circle(radius=0.45, stroke_color=GREEN, stroke_width=4, fill_color=GREEN, fill_opacity=0.15)
        prop = VGroup(blades, hub).move_to([-3.6, 1.0, 0])
        pl2 = lab("top view: three blades, closed state", 24, GREEN).move_to([-3.6, -2.3, 0])
        pl3 = lab("3.7 Å", 28, GREEN).move_to([-3.6, -2.9, 0])
        self.play(Create(prop, lag_ratio=0.2), FadeIn(pl2), FadeIn(pl3), run_time=1.0)
        self.at("bladed propeller")
        self.play(prop.animate.rotate(2 * np.pi / 3), run_time=1.2)
        self.at("forms a dome")
        xs = np.linspace(-3.0, 3.0, 90)
        flat = poly([[3.0 + x, 0.4] for x in xs], GREY, 7)
        dome_pts = lambda h, w: [[3.0 + x, 0.4 + h * np.exp(-(x / w) ** 2)] for x in xs]
        dome = poly(dome_pts(1.4, 1.2), GREY, 7)
        side = lab("side view: the detergent forms a dome", 24, GREY).move_to([3.0, -1.3, 0])
        self.play(Create(flat), run_time=0.5)
        self.play(Transform(flat, dome), FadeIn(side), run_time=1.0)
        self.at("tension changes")
        t1 = arr([0.2, 0.4, 0], [-0.6, 0.4, 0], TEXT, w=6, tip=0.2)
        t2 = arr([5.8, 0.4, 0], [6.6, 0.4, 0], TEXT, w=6, tip=0.2)
        tl = lab("proposed, in a membrane: tension", 24, TEXT).move_to([3.0, 2.0, 0])
        self.play(GrowArrow(t1), GrowArrow(t2), FadeIn(tl), run_time=0.5)
        self.at("projected area")
        br = DoubleArrow([3.0 - 1.6, -0.4, 0], [3.0 + 1.6, -0.4, 0], buff=0, color=YELLOW, stroke_width=5, tip_length=0.18)
        pa = lab("projected area under the dome", 24, YELLOW).move_to([3.0, -1.0, 0])
        self.play(FadeOut(side), Create(br), FadeIn(pa), run_time=0.6)
        self.at("under the dome")
        flat2 = poly(dome_pts(0.7, 1.8), GREY, 7)
        br2 = DoubleArrow([3.0 - 2.5, -0.4, 0], [3.0 + 2.5, -0.4, 0], buff=0, color=YELLOW, stroke_width=5, tip_length=0.18)
        self.play(Transform(flat, flat2), Transform(br, br2), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S08Tmc(SpokenScene):
    """native worm TMC-1 complex sorted with and without ARRD-6; then the rule: a structure is a still picture."""

    def construct(self):
        tag = lab("Jeong, Clark, Gouaux and colleagues, 2022", 26, GOLD).move_to([0, 3.4, 0])
        self.at("In 2022")
        self.play(FadeIn(tag), run_time=0.4)
        wn = chip("a worm (C. elegans) structure, not mammalian", BLUE, 24).move_to([0, 2.6, 0])
        self.play(FadeIn(wn, shift=DOWN * 0.1), run_time=0.4)
        names = ["TMC-1", "CALM-1", "TMIE"]
        chs = VGroup()
        for r in range(2):
            for c in range(3):
                chs.add(chip(names[c], PURPLE, 24).move_to([-5.0 + 1.75 * c, 1.35 - 0.95 * r - 0.2, 0]))
        cl = lab("two copies of each", 24, TEXT).move_to([-3.25, -1.3, 0])
        self.play(FadeIn(chs, lag_ratio=0.1), run_time=0.7)
        self.at("two copies each")
        self.play(FadeIn(cl), run_time=0.4)
        self.at("subset also carried")
        ex = chip("ARRD-6", ORANGE, 24).move_to([-4.3, -2.2, 0])
        exl = lab("in a subset", 24, ORANGE).move_to([-2.5, -2.2, 0])
        self.play(FadeIn(ex), FadeIn(exl), run_time=0.5)
        self.at("native extract")
        wc1 = chip("tagged worms", BLUE, 22).move_to([1.7, 1.7, 0])
        wc2 = chip("purified", BLUE, 22).move_to([5.2, 1.7, 0])
        wa = arr([2.9, 1.7], [4.3, 1.7], BLUE, w=4, tip=0.15)
        box = Rectangle(width=3.8, height=1.4, stroke_color=GREY, stroke_width=3).move_to([3.4, -0.1, 0])
        bx = lab("native extract", 22, GREY).move_to([3.4, 0.85, 0])
        R0 = rot(0.4, 0.9, 0.2)
        rr = np.random.RandomState(6)
        withx = [True, False, True, False, False, True]
        pp = []
        for k in range(6):
            p = blob(rot(rr.rand() * 6, rr.rand() * 6, rr.rand() * 6), (2.3 + 0.65 * (k % 3) * 1.0 + 0.3, -0.3 + 0.5 * (k // 3)), 0.17)
            if withx[k]:
                p.add(Circle(radius=0.1, stroke_color=ORANGE, stroke_width=2, fill_color=ORANGE, fill_opacity=0.95).move_to(p.get_right() + [0.0, 0.1, 0]))
            pp.append(p)
        self.play(FadeIn(wc1), GrowArrow(wa), FadeIn(wc2), run_time=0.7)
        self.play(FadeIn(box), FadeIn(bx), *[FadeIn(p) for p in pp], run_time=0.8)
        self.at("sorted by computer")
        wy, ny = -1.6, -1.6
        slots_w = [(1.9, -1.5), (2.7, -1.5), (2.3, -2.2)]
        slots_n = [(4.4, -1.5), (5.2, -1.5), (4.8, -2.2)]
        iw = [k for k in range(6) if withx[k]]
        inn = [k for k in range(6) if not withx[k]]
        self.play(*[pp[k].animate.move_to([slots_w[i][0], slots_w[i][1], 0]) for i, k in enumerate(iw)],
                  *[pp[k].animate.move_to([slots_n[i][0], slots_n[i][1], 0]) for i, k in enumerate(inn)], run_time=1.0)
        self.at("with and without")
        l1 = lab("with the extra protein", 24, ORANGE).move_to([2.3, -3.0, 0])
        sm = lab("simplified: the real result was three classes", 22, GOLD).move_to([3.0, -3.45, 0])
        l2 = lab("without", 24, TEXT).move_to([4.8, -3.0, 0])
        self.play(FadeIn(l1), FadeIn(l2), FadeIn(sm), run_time=0.4)

        self.at("static reconstruction")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        R = VA
        mp = contour(R, (-3.8, 0.9), 1.1, levels=(0.3, 0.85), color=GREEN, w=4)
        ml = lines("a still reconstruction", "of purified protein", size=26, color=GREEN, align=ORIGIN).move_to([-3.8, -1.7, 0])
        self.play(Create(mp), FadeIn(ml), run_time=0.9)
        self.at("time course")
        ax1 = axes_box(1.0, 5.6, -0.2, 2.6)
        tr = poly([[1.0 + 4.6 * x, 0.9 + 0.7 * np.sin(14 * x) * np.exp(-1.5 * x)] for x in np.linspace(0, 1, 120)], YELLOW, 4)
        tl = lab("time course, recording of function", 24, TEXT).move_to([3.3, 3.0, 0])
        self.play(Create(ax1), Create(tr, run_time=0.8, rate_func=linear), FadeIn(tl), run_time=0.8)
        self.at("recording of function")
        x = cross([3.3, 1.2], 1.2, RED, 9)
        nt = lab("not shown by a structure", 26, RED).move_to([3.3, -0.9, 0])
        self.play(Create(x), FadeIn(nt), run_time=0.5)
        self.at("Pair it with")
        c1 = chip("electrophysiology", BLUE, 26).move_to([-3.0, -3.0, 0])
        c2 = chip("mutants", BLUE, 26).move_to([0.9, -3.0, 0])
        self.play(FadeIn(c1, shift=UP * 0.1), FadeIn(c2, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S09End(EndCard):
    LINE = "A structure is static, not a recording of function."
