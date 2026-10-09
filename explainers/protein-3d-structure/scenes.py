# COLOR MAP (kept for the whole video; one color per concept)
#   BLUE    the protein / polypeptide chain / candidate conformations still alive
#   ORANGE  backbone geometry constraints: the rigid peptide plane, the phi/psi hinges, planarity, trans, Ramachandran
#   YELLOW  nonpolar (hydrophobic) side chains, lipid tails, the hydrophobic effect
#   PURPLE  polar / charged residues
#   TEAL    water (and the interactive cue on cards)
#   GREEN   the native fold, allowed / surviving, healthy
#   RED     forbidden, eliminated, misfolded, disease
#   GOLD    elastase (the protease in the alpha-1 antitrypsin story)
#   GREY    labels, frames, structure
# NOTHING here draws a molecular structure: chains are smooth curves, residues are beads/chips,
# the peptide "plane" is a rounded plate on two hinges, and the plots are computed.
import numpy as np
from bp_style import *

ORANGE = "#F29E4C"
PURPLE = "#B58CE0"


class Clock(NarratedScene):
    """NarratedScene with absolute-time scheduling: self.at(t) waits until t seconds into the narration."""

    def at(self, t):
        d = t - self.elapsed()
        if d > 0.01:
            self.wait(d)

    def to(self, t, *anims, **kw):
        """Start the animations at time t, running until t+dur (dur defaults to 1.0)."""
        self.at(t)
        dur = kw.pop("dur", 1.0)
        self.play(*anims, run_time=dur, **kw)


def heading(text, color=TEXT, size=36):
    h = T(text, size=size, color=color, font=TITLE_FONT)
    return h.to_edge(UP, buff=0.45)


def tag(txt, color=TEXT, size=24, pos=None):
    """A label with a dark backing so it stays readable over dots and plots."""
    t = T(txt, size=size, color=color)
    bk = Rectangle(width=t.width + 0.24, height=t.height + 0.16, stroke_width=0, fill_color=BG, fill_opacity=0.85).move_to(t)
    g = VGroup(bk, t)
    if pos is not None:
        g.move_to(pos)
    return g.set_z_index(8)


def wipe(scene, *extra, run_time=0.6):
    """Clear everything (except mobjects listed in `extra`) with one FadeOut."""
    keep = set(extra)
    gone = [m for m in scene.mobjects if m not in keep]
    if gone:
        scene.play(*[FadeOut(m) for m in gone], run_time=run_time)


def squiggle(seed, n=34, w=7.0, h=3.0, color=BLUE, width=7):
    """A random chain-like curve (a schematic polypeptide, not a structure)."""
    k = seed * 101
    while True:
        rng = np.random.RandomState(k)
        k += 1
        ang = 0.0
        pts = [np.array([0.0, 0.0])]
        for _ in range(n - 1):
            ang += rng.choice([-1.25, 0.0, 1.25]) + rng.normal(0, 0.25)
            pts.append(pts[-1] + np.array([np.cos(ang), np.sin(ang)]))
        P = np.array(pts)
        ratio = np.ptp(P[:, 0]) / max(np.ptp(P[:, 1]), 1e-6)
        if 0.9 * w / h < ratio < 1.4 * w / h:
            break
    P -= (P.max(0) + P.min(0)) / 2
    P *= min(w / np.ptp(P[:, 0]), h / np.ptp(P[:, 1]))
    m = VMobject(stroke_color=color, stroke_width=width)
    m.set_points_smoothly([np.array([x, y, 0.0]) for x, y in P])
    return m


class S00Title(TitleCard):
    LESSON = "Protein three-dimensional structure"
    TITLE = "How a sequence finds its fold"


# ------------------------------------------------------------------ 1. Levinthal
class S01Levinthal(Clock):
    def construct(self):
        top = T("Levinthal, 1969", size=30, color=GREY).to_edge(UP, buff=0.5)
        chain = squiggle(0, w=6.5, h=2.4)
        chain.shift(UP * 0.4)
        lab = T("a small protein: 100 residues", size=28, color=GREY).next_to(chain, DOWN, buff=0.7)
        self.to(0.3, FadeIn(top, shift=DOWN * 0.1), dur=0.8)
        self.to(0.7, Create(chain), dur=1.8)
        self.to(4.1, FadeIn(lab, shift=UP * 0.1), dur=0.6)
        # 4.1-7.8 "astronomically many conformations": the chain flickers through random shapes
        self.at(5.0)
        for s in range(1, 8):
            self.play(Transform(chain, squiggle(s, w=6.5, h=2.4).shift(UP * 0.4)), run_time=0.38)
        count = M("3 shapes per residue, 100 residues: 3¹⁰⁰", size=30, color=TEXT)
        count2 = M("≈ 5 × 10⁴⁷ shapes", size=44, color=TEXT)
        VGroup(count, count2).arrange(DOWN, buff=0.25).next_to(lab, DOWN, buff=0.4)
        self.to(7.7, FadeIn(count, shift=UP * 0.1), dur=0.5)
        self.to(8.2, FadeIn(count2, shift=UP * 0.1), dur=0.6)
        # 9.3 random sampling: chart of search time vs the age of the universe
        self.at(9.0)
        self.play(FadeOut(lab), FadeOut(count), FadeOut(count2), FadeOut(chain), FadeOut(top), run_time=0.5)
        ax = Axes(x_range=[0, 3, 1], y_range=[0, 30, 10], x_length=3.6, y_length=4.3,
                  axis_config={"include_numbers": False, "include_ticks": False, "stroke_color": GREY, "stroke_width": 3},
                  tips=False).move_to([-2.6, -0.85, 0])
        ticks = VGroup(*[M(str(v), size=24, color=GREY).next_to(ax.c2p(0, v), LEFT, buff=0.2) for v in (0, 10, 20, 30)])
        ylab = T("log₁₀ (years)", size=26, color=GREY).next_to(ax, UP, buff=0.25).align_to(ax, LEFT)
        head = heading("Sampling every shape, one by one", size=34)
        self.to(9.2, FadeIn(head), Create(ax), FadeIn(ticks), FadeIn(ylab), dur=0.9)
        rate = M("1 shape per 10⁻¹³ s", size=30, color=TEXT)
        rate_sub = T("the speed of bond rotation", size=26, color=GREY)
        VGroup(rate, rate_sub).arrange(RIGHT, buff=0.35).move_to([0.6, 2.65, 0])
        self.to(11.0, FadeIn(rate, shift=LEFT * 0.1), FadeIn(rate_sub), dur=0.8)
        # random-search bar: 5e47 shapes x 1e-13 s = 5e34 s = 1.6e27 years
        tr = ValueTracker(0)
        bar = always_redraw(lambda: Rectangle(width=0.9, height=max(0.001, ax.c2p(0, tr.get_value())[1] - ax.c2p(0, 0)[1]),
                                              stroke_width=0, fill_color=RED, fill_opacity=0.9)
                            .move_to(ax.c2p(1.1, 0), aligned_edge=DOWN))
        self.add(bar)
        self.at(12.5)
        self.play(tr.animate.set_value(27.2), run_time=1.5, rate_func=rush_from)
        r_lab = VGroup(T("random search", size=26, color=RED), M("≈ 10²⁷ years", size=36, color=RED)).arrange(DOWN, buff=0.1, aligned_edge=LEFT).next_to(ax.c2p(1.1, 27.2), RIGHT, buff=0.7).shift(DOWN*0.25)
        self.play(FadeIn(r_lab, shift=LEFT * 0.1), run_time=0.4)
        uni = DashedLine(ax.c2p(0, 10.14), ax.c2p(3, 10.14), color=TEXT, stroke_width=3)
        uni_lab = VGroup(T("age of the universe", size=26, color=TEXT), M("≈ 10¹⁰ years", size=30, color=TEXT)) \
            .arrange(DOWN, buff=0.1, aligned_edge=LEFT).next_to(ax.c2p(3, 10.14), RIGHT, buff=0.25)
        self.to(14.4, Create(uni), FadeIn(uni_lab), dur=0.8)
        # 16.4 the escape: not a random search
        self.at(16.4)
        self.play(*[FadeOut(m) for m in [ax, ticks, ylab, bar, r_lab, uni, uni_lab, rate, rate_sub, head]], run_time=0.5)
        chain2 = squiggle(20, w=6.0, h=2.4).shift(UP * 0.3)
        self.add(chain2)
        self.at(16.95)
        for s in range(21, 27):
            self.play(Transform(chain2, squiggle(s, w=6.0, h=2.4).shift(UP * 0.3)), run_time=0.42)
        rl = T("random search", size=34, color=RED).next_to(chain2, DOWN, buff=0.6)
        cross = Cross(chain2, stroke_color=RED, stroke_width=10).scale(1.08)
        self.to(19.5, FadeIn(rl), Create(cross), dur=0.7)
        self.at(21.0)
        self.play(*[FadeOut(m) for m in [chain2, rl, cross]], run_time=0.4)
        # 21.4 biased pathways -> funnel
        xs = np.linspace(-4.3, 4.3, 860)

        def E(x):
            return (-3.0 * np.exp(-x ** 2 / 10) - 0.7 * np.exp(-x ** 2 / 0.2)
                    + 0.7 * np.cos(2.6 * x) * (1 - np.exp(-x ** 2 / 1.2)) * np.exp(-x ** 2 / 25))
        cx, cy, sx, sy = 0.2, 1.83, 1.0, 0.9      # curve placement on screen
        P = lambda x, y: np.array([cx + sx * x, cy + sy * y, 0.0])
        funnel = ParametricFunction(lambda t: P(t, E(t)), t_range=[-4.3, 4.3, 0.02], color=BLUE, stroke_width=6)
        base_y = -2.75
        ax_y = Line([-5.4, base_y, 0], [5.4, base_y, 0], color=GREY, stroke_width=3)
        ax_x = Line([-5.4, base_y, 0], [-5.4, 1.9, 0], color=GREY, stroke_width=3)
        el = T("free energy", size=26, color=GREY).rotate(PI / 2).next_to(ax_x, LEFT, buff=0.2)
        xl = T("conformation", size=26, color=GREY).next_to(ax_y, DOWN, buff=0.15)
        fh = heading("Folding funnels downhill", size=34)
        self.to(21.4, Create(ax_x), Create(ax_y), FadeIn(el), FadeIn(xl), FadeIn(fh), dur=0.5)
        self.to(21.9, Create(funnel), dur=0.9)
        d = np.gradient(E(xs), xs)
        mins = [xs[i] for i in range(1, len(xs) - 1) if d[i - 1] < 0 <= d[i] and xs[i] < -0.5]
        m1, m2 = mins[0], mins[1]                    # two intermediates on the left slope
        start = -4.0
        tx = ValueTracker(start)
        ball = Dot(radius=0.18, color=YELLOW).set_z_index(5)
        ball.add_updater(lambda b: b.move_to(P(tx.get_value(), E(tx.get_value())) + UP * 0.18))
        ball.update()
        self.add(ball)
        self.at(22.9)
        self.play(tx.animate.set_value(m1), run_time=1.2, rate_func=smooth)           # biased pathway
        i1 = chip("partly correct intermediates", YELLOW, size=24, pad=0.14).move_to([-2.9, 2.2, 0])
        i1_arrow = Arrow(i1.get_bottom(), P(m1, E(m1)) + UP * 0.45, buff=0.05, color=YELLOW, stroke_width=4, max_tip_length_to_length_ratio=0.3)
        i2_arrow = Arrow(i1.get_bottom() + RIGHT * 0.6, P(m2, E(m2)) + UP * 0.45, buff=0.05, color=YELLOW, stroke_width=4, max_tip_length_to_length_ratio=0.15)
        self.to(24.9, FadeIn(i1, shift=UP * 0.1), GrowArrow(i1_arrow), Indicate(ball, color=YELLOW, scale_factor=1.6), dur=0.7)
        self.play(tx.animate.set_value(m2), run_time=1.0, rate_func=smooth)
        self.play(GrowArrow(i2_arrow), Indicate(ball, color=YELLOW, scale_factor=1.6), run_time=0.5)
        self.at(27.1)
        self.play(FadeOut(i1), FadeOut(i1_arrow), FadeOut(i2_arrow), tx.animate.set_value(0.0), run_time=1.5, rate_func=smooth)
        ball.clear_updaters()
        nat = Dot(P(0, E(0)) + UP * 0.22, radius=0.22, color=GREEN).set_z_index(6)
        nl = chip("native state", GREEN, size=28).next_to(P(0, E(0)), DOWN, buff=0.45)
        self.play(Transform(ball, nat), FadeIn(nl, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------ 2. planarity -> phi/psi -> Ramachandran
def _ell(phi, psi, c, a, b):
    out = False
    for dp in (0,):
        for dq in (0,):
            out = out or (((phi - c[0] + dp) / a) ** 2 + ((psi - c[1] + dq) / b) ** 2 <= 1)
    return out


def allowed(phi, psi):
    """Schematic Ramachandran 'allowed' regions (degrees): beta, bridge, alpha-R, alpha-L."""
    return (_ell(phi, psi, (-120, 130), 62, 52) or _ell(phi, psi, (-75, 40), 22, 55)
            or _ell(phi, psi, (-62, -42), 32, 28) or _ell(phi, psi, (58, 45), 24, 32))


def mask_image(px=360):
    arr = np.zeros((px, px, 4), dtype=np.uint8)
    g = np.array([0x83, 0xC1, 0x67, 150], dtype=np.uint8)
    for r in range(px):
        psi = 180 - (r + 0.5) * 360 / px
        for c in range(px):
            phi = -180 + (c + 0.5) * 360 / px
            if allowed(phi, psi):
                arr[r, c] = g
    return arr


class S02Planar(Clock):
    def construct(self):
        # ---------- A (0.2-3.9): the peptide bond is the root of every constraint
        head = heading("Every constraint starts at the peptide bond", size=34)
        big = RoundedRectangle(corner_radius=0.25, width=3.9, height=1.8, stroke_color=BLUE, stroke_width=5,
                               fill_color=BLUE, fill_opacity=0.22).shift(UP * 0.55)
        xs_ = [-4.8, -2.4, 0.0, 2.4, 4.8]
        smalls = [RoundedRectangle(corner_radius=0.15, width=1.3, height=0.7, stroke_color=BLUE, stroke_width=4,
                                   fill_color=BLUE, fill_opacity=0.25).move_to([x, 0.55, 0]) for x in xs_]
        links_ = [VGroup(Line(smalls[i].get_right(), smalls[i + 1].get_left(), color=GREY, stroke_width=4),
                         Dot(smalls[i].get_right() * 0.5 + smalls[i + 1].get_left() * 0.5, radius=0.1, color=GREY))
                  for i in range(4)]
        self.to(0.2, FadeIn(head, shift=DOWN * 0.1), dur=0.6)
        self.to(0.5, LaggedStart(*[FadeIn(p) for p in smalls], *[FadeIn(l) for l in links_], lag_ratio=0.12), dur=1.8)
        plate = smalls[2]
        others = [p for i, p in enumerate(smalls) if i != 2] + links_
        plab = T("peptide bond", size=34, color=BLUE).move_to(big)
        self.at(2.6)
        self.play(*[FadeOut(o) for o in others], Transform(plate, big), run_time=1.0)
        self.play(FadeIn(plab), run_time=0.4)
        # ---------- B (4.9-7.8): resonance -> partial double bond
        gx0, gx1, gy = -3.0, 3.0, -1.75
        gline = Line([gx0, gy, 0], [gx1, gy, 0], color=GREY, stroke_width=6)
        gl = T("single", size=26, color=GREY).next_to(gline.get_start(), DOWN, buff=0.3)
        gr = T("double", size=26, color=GREY).next_to(gline.get_end(), DOWN, buff=0.3)
        gt = T("partial double-bond character (resonance)", size=28, color=ORANGE).next_to(gline, UP, buff=0.55)
        gtr = ValueTracker(0.0)
        gfill = always_redraw(lambda: Line([gx0, gy, 0], [gx0 + (gx1 - gx0) * gtr.get_value(), gy, 0],
                                           color=ORANGE, stroke_width=12))
        gdot = always_redraw(lambda: Dot([gx0 + (gx1 - gx0) * gtr.get_value(), gy, 0], radius=0.17, color=ORANGE))
        self.to(4.9, Create(gline), FadeIn(gl), FadeIn(gr), FadeIn(gt, shift=UP * 0.1), dur=0.8)
        self.add(gfill, gdot)
        self.at(5.9)
        self.play(gtr.animate.set_value(0.42), run_time=1.6, rate_func=smooth)
        pct = M("≈ 40 % double", size=26, color=ORANGE).next_to(gdot, DOWN, buff=0.3)
        self.play(FadeIn(pct, shift=UP * 0.1), run_time=0.4)
        # ---------- C (8.6-11.2): six atoms locked flat
        self.at(8.4)
        self.play(FadeOut(gline), FadeOut(gl), FadeOut(gr), FadeOut(gt), FadeOut(gfill), FadeOut(gdot), FadeOut(pct), run_time=0.4)
        six = T("six atoms around it", size=30, color=GREY).next_to(plate, DOWN, buff=0.55)
        self.to(8.7, FadeIn(six, shift=UP * 0.1), dur=0.4)
        self.at(9.2)
        pg = VGroup(plate, plab)
        for _ in range(2):       # it tries to twist out of plane ...
            self.play(pg.animate.stretch(0.35, 1), run_time=0.22)
            self.play(pg.animate.stretch(1 / 0.35, 1), run_time=0.22)
        # ... and cannot: it locks flat
        flat_top = DashedLine(plate.get_corner(UL) + LEFT * 0.7, plate.get_corner(UR) + RIGHT * 0.7, color=ORANGE, stroke_width=3)
        flat_bot = DashedLine(plate.get_corner(DL) + LEFT * 0.7, plate.get_corner(DR) + RIGHT * 0.7, color=ORANGE, stroke_width=3)
        self.play(plate.animate.set_stroke(ORANGE).set_fill(ORANGE, 0.28), plab.animate.set_color(ORANGE),
                  Create(flat_top), Create(flat_bot), run_time=0.6)
        self.at(10.9)
        pl_chip = chip("planarity", ORANGE, size=36).next_to(six, DOWN, buff=0.35)
        self.play(FadeIn(pl_chip, shift=UP * 0.15), run_time=0.5)
        # ---------- D (12.6-16.1): only phi and psi are free
        self.at(12.5)
        self.play(*[FadeOut(m) for m in [six, pl_chip, flat_top, flat_bot, plab, plate, head]], run_time=0.5)
        sc = ValueTracker(1.0)
        ox = ValueTracker(-1.7)
        phi_t = ValueTracker(0.0)
        psi_t = ValueTracker(0.0)
        judge = ValueTracker(0.0)
        ph_deg = ValueTracker(0.0)    # the dot's phi/psi in degrees drive judging
        ps_deg = ValueTracker(0.0)

        def u(a):
            return np.array([np.cos(a), np.sin(a), 0.0])

        def pose():
            S, X, Y = sc.get_value(), ox.get_value(), 0.1
            t1 = phi_t.get_value()
            t2 = t1 + psi_t.get_value()
            org = lambda v: np.array([X, Y, 0.0]) + v * S
            c0 = np.array([X, Y, 0.0])
            h1 = org(np.array([0.85, 0, 0]))
            node = h1 + 0.75 * S * u(t1)
            h2 = node + 0.75 * S * u(t1)
            c1 = h2 + 1.0 * S * u(t2)
            return c0, h1, node, h2, c1, t2

        def plate_at(c, ang):
            S = sc.get_value()
            r = RoundedRectangle(corner_radius=0.2 * S, width=1.7 * S, height=0.9 * S, stroke_color=BLUE, stroke_width=4,
                                 fill_color=BLUE, fill_opacity=0.28)
            return r.rotate(ang).move_to(c)

        def build():
            c0, h1, node, h2, c1, t2 = pose()
            S = sc.get_value()
            col = GREY
            if judge.get_value() > 0.5:
                col = GREEN if allowed(ph_deg.get_value(), ps_deg.get_value()) else RED
            link1 = Line(h1, node, color=GREY, stroke_width=4)
            link2 = Line(node, h2, color=GREY, stroke_width=4)
            nd = Dot(node, radius=0.13 * S + 0.03, color=col)
            ring = Circle(radius=0.3 * S + 0.1, color=col, stroke_width=4).move_to(node) if col == RED else VGroup()
            hh1 = Dot(h1, radius=0.15 * S, color=ORANGE)
            hh2 = Dot(h2, radius=0.15 * S, color=ORANGE)
            return VGroup(plate_at(c0, 0), plate_at(c1, t2), link1, link2, hh1, hh2, nd, ring)

        chain = always_redraw(build)
        c_in = build()
        self.play(LaggedStart(*[FadeIn(p) for p in c_in], lag_ratio=0.25), run_time=0.9)
        self.remove(*c_in)
        self.add(chain)
        lphi = M("φ", size=36, color=ORANGE)
        lpsi = M("ψ", size=36, color=ORANGE)
        lphi.add_updater(lambda m: m.move_to(pose()[1] + UP * 0.55 * sc.get_value() ** 0.5 + LEFT * 0.0))
        lpsi.add_updater(lambda m: m.move_to(pose()[3] + UP * 0.55 * sc.get_value() ** 0.5))
        self.at(13.3)
        free = T("only two bonds can rotate", size=32, color=ORANGE).to_edge(UP, buff=0.5)
        self.play(FadeIn(free, shift=DOWN * 0.1), run_time=0.5)
        # swing phi, then psi
        self.at(13.8)
        self.play(phi_t.animate.set_value(0.55), run_time=0.4)
        self.play(phi_t.animate.set_value(-0.45), run_time=0.4)
        self.play(psi_t.animate.set_value(0.8), run_time=0.4)
        self.play(psi_t.animate.set_value(-0.6), run_time=0.4)
        self.play(phi_t.animate.set_value(0.0), psi_t.animate.set_value(0.0), run_time=0.2)
        self.at(15.6)
        self.play(FadeIn(lphi, scale=1.3), run_time=0.35)
        self.at(16.1)
        self.play(FadeIn(lpsi, scale=1.3), run_time=0.35)
        # ---------- E (17.0-22.4): most of those combinations clash
        self.at(16.9)
        sx0 = 3.35
        plot_c = np.array([sx0, -0.15, 0.0])
        PW = 4.7
        frame = Square(PW, color=GREY, stroke_width=3).move_to(plot_c)
        hl = Line(frame.get_left(), frame.get_right(), color=GREY, stroke_width=1.5).set_opacity(0.5)
        vl = Line(frame.get_bottom(), frame.get_top(), color=GREY, stroke_width=1.5).set_opacity(0.5)
        xt = VGroup(*[M(v, size=22, color=GREY).next_to(frame.get_bottom() + RIGHT * dx, DOWN, buff=0.12)
                      for v, dx in (("-180°", -PW / 2 + 0.2), ("0°", 0), ("180°", PW / 2 - 0.2))])
        yt = VGroup(*[M(v, size=22, color=GREY).next_to(frame.get_left() + UP * dy, LEFT, buff=0.12)
                      for v, dy in (("180°", PW / 2 - 0.15), ("0°", 0), ("-180°", -PW / 2 + 0.15))])
        xa = M("φ", size=34, color=ORANGE).next_to(xt, DOWN, buff=0.05).shift(RIGHT * 0.0)
        ya = M("ψ", size=34, color=ORANGE).next_to(yt, LEFT, buff=0.15).set_y(plot_c[1])
        c2p = lambda phi, psi: plot_c + np.array([phi / 360 * PW, psi / 360 * PW, 0.0])
        self.play(sc.animate.set_value(0.62), ox.animate.set_value(-4.55),
                  lphi.animate.scale(0.85), lpsi.animate.scale(0.85), FadeOut(free),
                  FadeIn(frame), FadeIn(hl), FadeIn(vl), FadeIn(xt), FadeIn(yt), FadeIn(xa), FadeIn(ya), run_time=1.0)
        # "not unrestricted": swing freely while the plot waits
        self.play(phi_t.animate.set_value(1.1), psi_t.animate.set_value(-0.9), run_time=0.6)
        self.play(phi_t.animate.set_value(-1.0), psi_t.animate.set_value(0.8), run_time=0.7)
        # sampling begins at 19.3
        self.at(19.2)
        judge.set_value(1.0)
        rng = np.random.RandomState(7)
        samples = [(rng.uniform(-180, 180), rng.uniform(-180, 180)) for _ in range(26)]
        good = [(-62, -42), (-125, 135), (-80, 90), (58, 45)]
        for i, g in enumerate(good):
            samples[3 + i * 6] = (g[0] + rng.uniform(-8, 8), g[1] + rng.uniform(-8, 8))
        dots = VGroup()
        for (a, b) in samples:
            ok = allowed(a, b)
            ph_deg.set_value(a)
            ps_deg.set_value(b)
            d = Dot(c2p(a, b), radius=0.075, color=GREEN if ok else RED).set_z_index(6)
            dots.add(d)
            self.play(phi_t.animate.set_value(np.radians(a) * 0.5), psi_t.animate.set_value(np.radians(b) * 0.5),
                      FadeIn(d, scale=2.0), run_time=0.11, rate_func=linear)
        # ---------- F (23.7-30.2): the plot is the map of what survives
        self.at(23.6)
        judge.set_value(0.0)
        self.play(phi_t.animate.set_value(0.0), psi_t.animate.set_value(0.0), run_time=0.3)
        rtitle = T("Ramachandran plot", size=30, color=TEXT).next_to(frame, UP, buff=0.15)
        self.play(FadeIn(rtitle, shift=DOWN * 0.1), run_time=0.5)
        img = ImageMobject(mask_image()).set_height(PW).move_to(plot_c)
        img.set_z_index(2)
        self.add(img)
        self.play(FadeIn(img), run_time=1.6)
        def tag(txt, pos):
            t = T(txt, size=24, color=TEXT)
            bk = Rectangle(width=t.width + 0.2, height=t.height + 0.14, stroke_width=0, fill_color=BG, fill_opacity=0.8).move_to(t)
            return VGroup(bk, t).move_to(pos).set_z_index(8)
        la = tag("α-helix", c2p(-62, -108))
        lb = tag("β-sheet", c2p(-100, 160))
        self.play(FadeIn(la), FadeIn(lb), run_time=0.5)
        big = M("≈ 15%", size=64, color=GREEN)
        sub = T("of φ–ψ space survives", size=30, color=TEXT)
        VGroup(big, sub).arrange(DOWN, buff=0.25).move_to([-3.6, -2.0, 0])
        self.to(27.3, FadeIn(big, shift=UP * 0.15), FadeIn(sub, shift=UP * 0.1), dur=0.8)
        self.finish()


# ------------------------------------------------------------------ 3. the hydrophobic effect
class S03Water(Clock):
    def construct(self):
        rng = np.random.RandomState(11)
        N = 12
        types = ["P", "N", "N", "P", "N", "P", "N", "N", "P", "N", "P", "P"]   # N = nonpolar, P = polar
        unf = [np.array([-4.5 + 0.8 * i, 0.95 * np.sin(1.25 * i) * (1 if i % 2 == 0 else 1), 0]) for i in range(N)]
        fold = []
        ni = pi = 0
        for i, t_ in enumerate(types):
            if t_ == "N":
                a = 2 * PI * ni / 6 + 0.4
                fold.append(np.array([0.55 * np.cos(a), 0.55 * np.sin(a), 0]))
                ni += 1
            else:
                a = 2 * PI * pi / 6 + 0.9
                fold.append(np.array([1.45 * np.cos(a), 1.45 * np.sin(a), 0]))
                pi += 1
        col = {"N": YELLOW, "P": PURPLE}
        beads = [Dot(unf[i], radius=0.2, color=col[types[i]]).set_z_index(5) for i in range(N)]
        chain = VMobject(stroke_color=BLUE, stroke_width=5).set_z_index(3)
        tt = ValueTracker(0.0)         # 0 = unfolded, 1 = folded
        rel = ValueTracker(0.0)        # release of caged water
        # cage dots: 8 per nonpolar bead
        cages = []
        for i, t_ in enumerate(types):
            if t_ != "N":
                continue
            for k in range(8):
                a = 2 * PI * k / 8
                tgt = None
                while tgt is None:
                    r_ = rng.uniform(2.2, 4.6)
                    an = rng.uniform(0, 2 * PI)
                    p = np.array([r_ * np.cos(an) * 1.2, r_ * np.sin(an) * 0.62, 0])
                    if abs(p[0]) < 5.0 and abs(p[1]) < 2.6 and np.linalg.norm(p) > 2.1:
                        tgt = p
                cages.append((i, a, tgt, rng.uniform(0, 0.5), Dot(radius=0.065, color=TEAL).set_z_index(2)))
        # bulk water
        bulk = []
        while len(bulk) < 70:
            p = np.array([rng.uniform(-5.0, 5.0), rng.uniform(-2.6, 2.6), 0])
            if min(np.linalg.norm(p - u_) for u_ in unf) < 0.75:
                continue
            q = p.copy()
            if np.linalg.norm(p) < 2.1:
                q = p / max(np.linalg.norm(p), 1e-3) * rng.uniform(2.2, 2.7)
                q[0] *= 1.0
            bulk.append((p, q, Dot(p, radius=0.06, color=TEAL).set_opacity(0.7).set_z_index(1)))
        BR = 0.46

        def bpos(i):
            return (1 - tt.get_value()) * unf[i] + tt.get_value() * fold[i]

        dummy = Mobject()

        def upd(_):
            for i, b in enumerate(beads):
                b.move_to(bpos(i))
            chain.set_points_smoothly([bpos(i) for i in range(N)])
            R = rel.get_value()
            for (i, a, tgt, dl, d) in cages:
                loc = float(np.clip((R - dl) / 0.5, 0, 1))
                att = bpos(i) + BR * np.array([np.cos(a), np.sin(a), 0])
                d.move_to((1 - loc) * att + loc * tgt)
            for (p, q, d) in bulk:
                d.move_to((1 - tt.get_value()) * p + tt.get_value() * q)
        dummy.add_updater(upd)
        upd(None)
        self.add(dummy)
        # legend (bottom row)
        def leg(c, txt):
            return VGroup(Dot(radius=0.12, color=c), T(txt, size=24, color=TEXT)).arrange(RIGHT, buff=0.15)
        legend = VGroup(leg(YELLOW, "nonpolar side chain"), leg(PURPLE, "polar / charged"), leg(TEAL, "water")).arrange(RIGHT, buff=0.7).move_to([0, -3.35, 0])
        # entropy gauge
        eg_x = 6.0
        eg_frame = Rectangle(width=0.45, height=3.0, stroke_color=GREY, stroke_width=3).move_to([eg_x, -0.2, 0])
        ent = ValueTracker(0.12)
        eg_fill = always_redraw(lambda: Rectangle(width=0.45, height=3.0 * ent.get_value(), stroke_width=0, fill_color=TEAL, fill_opacity=0.9)
                                .move_to(eg_frame.get_bottom(), aligned_edge=DOWN))
        eg_lab = VGroup(T("water", size=24, color=TEAL), T("entropy", size=24, color=TEAL)).arrange(DOWN, buff=0.16).next_to(eg_frame, UP, buff=0.2)
        # --- 0.1 setup
        water_all = VGroup(*[c[4] for c in cages], *[b[2] for b in bulk])
        self.to(0.1, FadeIn(chain), *[FadeIn(b, scale=0.5) for b in beads], FadeIn(legend), FadeIn(water_all), dur=1.0)
        # --- 0.8 the water ordered around each nonpolar side chain
        ow = tag("ordered water", TEAL, 26, [3.3, 2.3, 0])
        self.to(0.8, FadeIn(ow, shift=LEFT * 0.1), dur=0.5)
        # --- 1.4-3.4 water pushes the nonpolar side chains together (partial collapse, cages still on)
        self.at(1.4)
        self.play(tt.animate.set_value(0.5), run_time=2.0, rate_func=smooth)
        # --- 4.1-6.5 burying them in a core releases the ordered water (cages fly off as the core closes)
        core = tag("hydrophobic core", YELLOW, 26, [-3.3, 2.3, 0])
        arr = Arrow(core.get_right(), [-0.55, 0.5, 0], buff=0.08, color=YELLOW, stroke_width=4, max_tip_length_to_length_ratio=0.25)
        self.at(4.1)
        self.play(tt.animate.set_value(1.0), rel.animate(rate_func=lambda t: smooth(min(1.0, max(0.0, (t - 0.15) / 0.85)))).set_value(1.0),
                  FadeIn(core, shift=RIGHT * 0.1, rate_func=lambda t: smooth(min(1.0, t * 2.5))),
                  GrowArrow(arr, rate_func=lambda t: smooth(min(1.0, t * 2.5))), run_time=2.3)
        fw = tag("ordered water released", TEAL, 26, [3.0, 2.3, 0])
        self.play(Transform(ow, fw), FadeIn(eg_frame), FadeIn(eg_fill), FadeIn(eg_lab), run_time=0.5)
        # --- 7.2 entropically favorable
        self.at(7.2)
        self.play(ent.animate.set_value(0.85), run_time=1.0, rate_func=smooth)
        # --- 9.3 polar residues sit on the surface
        self.at(9.0)
        self.play(FadeOut(core), FadeOut(arr), FadeOut(ow), FadeOut(eg_frame), FadeOut(eg_fill), FadeOut(eg_lab), run_time=0.4)
        surf = tag("polar and charged residues on the surface", PURPLE, 26, [0, 2.5, 0])
        self.at(9.5)
        self.play(FadeIn(surf, shift=DOWN * 0.1), run_time=0.4)
        for i, t_ in enumerate(types):
            if t_ == "P":
                self.play(Indicate(beads[i], color=PURPLE, scale_factor=1.6), run_time=0.45)
        # --- 13.8 membrane porin
        self.at(13.2)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not legend], run_time=0.5)
        dummy.clear_updaters()
        top = heading("A membrane porin", size=34)
        wat1 = Rectangle(width=9.6, height=1.9, stroke_width=0, fill_color=TEAL, fill_opacity=0.12).move_to([0, 1.75, 0])
        wat2 = Rectangle(width=9.6, height=1.9, stroke_width=0, fill_color=TEAL, fill_opacity=0.12).move_to([0, -1.75, 0])
        lip = Rectangle(width=9.6, height=1.6, stroke_width=0, fill_color=YELLOW, fill_opacity=0.2).move_to([0, 0, 0])
        lw1 = T("water", size=24, color=TEAL).move_to([-4.0, 2.2, 0])
        lw2 = T("water", size=24, color=TEAL).move_to([-4.0, -2.2, 0])
        ll = T("lipid bilayer", size=26, color=YELLOW).move_to([-3.6, 0, 0])
        self.to(13.8, FadeIn(top), FadeIn(wat1), FadeIn(wat2), FadeIn(lip), FadeIn(lw1), FadeIn(lw2), FadeIn(ll), dur=0.8)
        wallL = Rectangle(width=0.5, height=3.0, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.45).move_to([-0.85, 0, 0])
        wallR = Rectangle(width=0.5, height=3.0, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.45).move_to([0.85, 0, 0])
        plab2 = T("porin", size=26, color=BLUE).move_to([2.3, 1.35, 0])
        self.to(14.9, DrawBorderThenFill(wallL), DrawBorderThenFill(wallR), FadeIn(plab2), dur=1.0)
        # hydrophobic residues face the lipid (outer faces)
        outL = Rectangle(width=0.12, height=1.6, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to([-1.16, 0, 0])
        outR = Rectangle(width=0.12, height=1.6, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to([1.16, 0, 0])
        hy = tag("hydrophobic residues\nface the lipid", YELLOW, 26, [3.9, 0.0, 0])
        hy_arr = Arrow(hy.get_left(), [1.4, 0, 0], buff=0.08, color=YELLOW, stroke_width=4, max_tip_length_to_length_ratio=0.25)
        self.at(16.7)
        self.play(FadeIn(outL), FadeIn(outR), FadeIn(hy), GrowArrow(hy_arr), FadeOut(ll), FadeOut(plab2), run_time=0.8)
        # polar channel through the middle
        inL = Rectangle(width=0.12, height=3.0, stroke_width=0, fill_color=PURPLE, fill_opacity=1).move_to([-0.54, 0, 0])
        inR = Rectangle(width=0.12, height=3.0, stroke_width=0, fill_color=PURPLE, fill_opacity=1).move_to([0.54, 0, 0])
        po = tag("a polar channel", PURPLE, 26, [0, 2.2, 0])
        po_arr = Arrow(po.get_bottom(), [0, 1.35, 0], buff=0.05, color=PURPLE, stroke_width=4, max_tip_length_to_length_ratio=0.25)
        flow = ValueTracker(0.0)
        wdots = VGroup(*[Dot(radius=0.075, color=TEAL) for _ in range(7)])

        def fl(_):
            for k, d in enumerate(wdots):
                y = 1.5 - ((flow.get_value() * 3.0 + k * 3.0 / 7) % 3.0)
                d.move_to([0.18 * np.sin(3 * y + k), y, 0])
        wdots.add_updater(fl)
        fl(None)
        self.at(19.7)
        self.play(FadeOut(hy), FadeOut(hy_arr), FadeIn(inL), FadeIn(inR), FadeIn(po), GrowArrow(po_arr), FadeIn(wdots), run_time=0.8)
        self.play(flow.animate.set_value(0.9), run_time=1.6, rate_func=linear)
        # --- 22.1 negotiation
        self.at(21.8)
        wdots.clear_updaters()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        cp = chip("protein", BLUE, size=44, pad=0.35).move_to([-2.9, 0.4, 0])
        cw = chip("water", TEAL, size=44, pad=0.35).move_to([2.9, 0.4, 0])
        da = DoubleArrow(cp.get_right() + RIGHT * 0.15, cw.get_left() + LEFT * 0.15, buff=0.0, color=TEXT, stroke_width=5)
        neg = T("a negotiation", size=40, font=TITLE_FONT).move_to([0, -1.5, 0])
        self.to(22.2, FadeIn(cp, shift=RIGHT * 0.2), FadeIn(cw, shift=LEFT * 0.2), dur=0.7)
        self.to(23.5, GrowArrow(da), dur=0.6)
        self.to(24.5, FadeIn(neg, shift=UP * 0.1), dur=0.7)
        self.finish()


# ------------------------------------------------------------------ 4. the constraint filter
class S04Filter(Clock):
    def construct(self):
        rng = np.random.RandomState(5)
        FC = np.array([-3.1, -0.05, 0.0])
        frame = Rectangle(width=6.3, height=4.5, stroke_color=GREY, stroke_width=3).move_to(FC)
        flab = T("every possible conformation", size=26, color=GREY).next_to(frame, DOWN, buff=0.3)
        NN = 360
        pos = [FC + np.array([rng.uniform(-2.9, 2.9), rng.uniform(-2.0, 2.0), 0]) for _ in range(NN)]
        rank = rng.uniform(0, 1, NN)
        rank[int(np.argmin(rank))] = 0.0
        dots = [Dot(p, radius=0.055, color=BLUE) for p in pos]
        allg = VGroup(*dots)
        names = [("peptide planarity", ORANGE), ("trans preference", ORANGE), ("Ramachandran φ–ψ", ORANGE), ("hydrophobic effect", YELLOW)]
        chips = [chip(t_, c_, size=28) for t_, c_ in names]
        col = VGroup(*chips).arrange(DOWN, buff=0.5).move_to([3.9, -0.05, 0])
        def dim(c_, lvl=0.0):
            c_[0].set_fill(opacity=0.06 + 0.1 * lvl).set_stroke(opacity=0.4 + 0.3 * lvl)
            c_[1].set_opacity(0.45 + 0.3 * lvl)
        for c_ in chips:
            dim(c_)
        head = heading("Four layers of constraint", size=34)
        self.to(0.3, FadeIn(frame), LaggedStart(*[FadeIn(d, scale=0.3) for d in dots], lag_ratio=0.004), dur=2.6)
        self.to(2.6, FadeIn(flab, shift=UP * 0.1), dur=0.6)
        self.to(4.0, FadeIn(head, shift=DOWN * 0.1), LaggedStart(*[FadeIn(c_, shift=LEFT * 0.2) for c_ in chips], lag_ratio=0.3), dur=2.4)
        thr = [0.25, 0.075, 0.02]       # survivors after planarity / trans / phi-psi (schematic)
        shrink = [0.85, 0.65, 0.4]
        alive = list(range(NN))

        def light(i, t_):
            self.at(t_)
            anims = [chips[i][0].animate.set_fill(names[i][1], 0.4).set_stroke(opacity=1), chips[i][1].animate.set_opacity(1.0)]
            if i > 0:
                anims += [chips[i - 1][0].animate.set_fill(opacity=0.2).set_stroke(opacity=0.7), chips[i - 1][1].animate.set_opacity(0.7)]
            self.play(*anims, run_time=0.6)

        def eliminate(k, t_, dur):
            nonlocal alive
            self.at(t_)
            keep = [i for i in alive if rank[i] < thr[k]]
            gone = [i for i in alive if rank[i] >= thr[k]]
            self.play(*[dots[i].animate.set_color(RED) for i in gone], run_time=0.3)
            anims = [FadeOut(dots[i], scale=0.2) for i in gone]
            if k == 0:
                nf = T("conformations still allowed", size=26, color=GREY).move_to(flab)
                anims.append(Transform(flab, nf))
            for i in keep:
                pos[i] = FC + (pos[i] - FC) * (shrink[k] / (shrink[k - 1] if k else 1.0))
                anims.append(dots[i].animate.move_to(pos[i]))
            self.play(*anims, run_time=dur)
            alive = keep
            return len(keep)

        light(0, 8.3)
        eliminate(0, 9.3, 1.3)
        light(1, 12.3)
        eliminate(1, 13.3, 1.0)
        light(2, 15.2)
        eliminate(2, 17.1, 1.4)
        light(3, 20.0)
        # hydrophobic effect collapses the chain onto one fold
        self.at(21.7)
        best = int(np.argmin(rank))
        others = [i for i in alive if i != best]
        self.play(*[dots[i].animate.set_color(RED) for i in others], run_time=0.3)
        self.play(*[FadeOut(dots[i], scale=0.2) for i in others], dots[best].animate.move_to(FC).set_color(GREEN).scale(3.2),
                  run_time=1.6)
        one = chip("one stable fold", GREEN, size=28).next_to(dots[best], DOWN, buff=0.5)
        self.to(23.4, FadeIn(one, shift=UP * 0.1), dur=0.6)
        # not limitations -> the mechanism
        self.at(24.9)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        nl = T("constraints are not limitations", size=42, font=TITLE_FONT).move_to([0, 0.3, 0])
        self.to(25.4, FadeIn(nl, shift=UP * 0.1), dur=0.7)
        self.at(26.8)
        self.play(FadeOut(nl), run_time=0.4)
        gate = VGroup(*[chip(t_, c_, size=24, pad=0.14) for t_, c_ in names]).arrange(DOWN, buff=0.12).move_to([-0.7, 0.2, 0])
        seq = chip("sequence", BLUE, size=34, pad=0.26).next_to(gate, LEFT, buff=1.1)
        fold = VGroup(T("one unique", size=34, color=GREEN), T("structure", size=34, color=GREEN)).arrange(DOWN, buff=0.1)
        fbox = RoundedRectangle(corner_radius=0.14, width=fold.width + 0.52, height=fold.height + 0.44, stroke_color=GREEN,
                                stroke_width=2.5, fill_color=GREEN, fill_opacity=0.16).move_to(fold)
        fold = VGroup(fbox, fold).next_to(gate, RIGHT, buff=1.1)
        a1 = Arrow(seq.get_right(), gate.get_left() + LEFT * 0.05, buff=0.1, color=TEXT, stroke_width=5)
        a2 = Arrow(gate.get_right() + RIGHT * 0.05, fold.get_left(), buff=0.1, color=TEXT, stroke_width=5)
        self.to(27.1, FadeIn(seq, shift=RIGHT * 0.2), dur=0.5)
        self.to(27.7, GrowArrow(a1), FadeIn(gate, scale=0.9), dur=0.9)
        self.to(29.3, GrowArrow(a2), FadeIn(fold, shift=LEFT * 0.2), dur=0.9)
        self.finish()


# ------------------------------------------------------------------ 5. alpha-1 antitrypsin
def blob(r0=1.2, noise=0.06, seed=0, color=BLUE, fill=0.3, n=26, width=5):
    """A schematic protein blob (not a structure): a closed smooth wobbly outline."""
    rng = np.random.RandomState(seed)
    k = rng.uniform(-1, 1, n)
    pts = []
    for j in range(n):
        a = 2 * PI * j / n
        r = r0 * (1 + noise * k[j] + 0.5 * noise * np.sin(3 * a + seed))
        pts.append(np.array([r * np.cos(a), r * np.sin(a), 0.0]))
    m = VMobject(stroke_color=color, stroke_width=width, fill_color=color, fill_opacity=fill)
    m.set_points_smoothly(pts + [pts[0]])
    return m


class S05A1at(Clock):
    def construct(self):
        head = heading("Alpha-1 antitrypsin", size=34)
        prot = blob(1.15, 0.05, 1, BLUE).move_to([0, -0.7, 0])
        plab = T("the protein", size=28, color=BLUE).move_to([0, -2.75, 0])
        self.to(0.2, FadeIn(head, shift=DOWN * 0.1), DrawBorderThenFill(prot), FadeIn(plab), dur=1.6)
        # sequence strip: five residues, one highlighted
        boxes = VGroup(*[Square(0.7, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.1) for _ in range(5)]).arrange(RIGHT, buff=0.12).move_to([0, 2.05, 0])
        nums = VGroup(*[M(str(340 + i), size=22, color=GREY).next_to(boxes[i], DOWN, buff=0.12) for i in range(5)])
        seqlab = T("amino acid sequence", size=24, color=GREY).next_to(boxes, LEFT, buff=0.45)
        self.to(3.0, FadeIn(boxes, shift=DOWN * 0.1), FadeIn(nums), FadeIn(seqlab), dur=0.9)
        glu = T("Glu", size=28, color=PURPLE).move_to(boxes[2])
        self.to(4.8, boxes[2].animate.set_stroke(PURPLE).set_fill(PURPLE, 0.25), FadeIn(glu), Indicate(boxes[2], color=PURPLE), dur=0.9)
        lys = T("Lys", size=28, color=RED).move_to(boxes[2])
        self.at(6.2)
        self.play(Transform(glu, lys), boxes[2].animate.set_stroke(RED).set_fill(RED, 0.25), run_time=0.6)
        # misfolding
        mis = blob(1.3, 0.3, 4, RED).move_to(prot)
        mlab = T("misfolded", size=28, color=RED).move_to([0, -2.75, 0])
        self.at(7.4)
        self.play(Transform(prot, mis), Transform(plab, mlab), run_time=1.3)
        # two organs
        liver = chip("liver", RED, size=32).move_to([-4.3, -0.7, 0])
        lung = chip("lungs", RED, size=32).move_to([4.3, -0.7, 0])
        aL = Arrow(prot.get_left() + LEFT * 0.1, liver.get_right(), buff=0.12, color=RED, stroke_width=5)
        aR = Arrow(prot.get_right() + RIGHT * 0.1, lung.get_left(), buff=0.12, color=RED, stroke_width=5)
        self.at(9.4)
        self.play(GrowArrow(aL), GrowArrow(aR), FadeIn(liver, shift=RIGHT * 0.2), FadeIn(lung, shift=LEFT * 0.2), run_time=0.9)
        # ---------------- liver (11.5-18.5)
        self.at(11.2)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not head], run_time=0.5)
        cell = Ellipse(width=5.2, height=3.7, stroke_color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=0.1).move_to([-2.4, -0.1, 0])
        clab = T("liver cell", size=28, color=GREY).next_to(cell, DOWN, buff=0.3)
        blood = RoundedRectangle(corner_radius=0.2, width=3.0, height=3.7, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.05).move_to([4.5, -0.1, 0])
        blab = T("blood", size=28, color=GREY).next_to(blood, DOWN, buff=0.3)
        self.to(11.6, FadeIn(cell), FadeIn(clab), FadeIn(blood), FadeIn(blab), dur=0.7)
        centers = [np.array([-2.4 + dx, -0.1 + dy, 0]) for dx, dy in [(-1.3, 0.7), (-0.5, -0.9), (0.9, 0.6), (-0.9, -0.1), (0.3, 0.1), (1.2, -0.6)]]
        smalls = [blob(0.3, 0.3, 10 + i, RED, 0.5, width=4).move_to(c) for i, c in enumerate(centers)]
        self.to(12.4, LaggedStart(*[FadeIn(b, scale=0.3) for b in smalls], lag_ratio=0.25), dur=1.5)
        clump = blob(0.95, 0.28, 21, RED, 0.55).move_to([-2.4, -0.1, 0])
        self.at(13.7)
        self.play(*[b.animate.move_to([-2.4, -0.1, 0]).scale(0.7) for b in smalls], run_time=1.0)
        self.play(*[FadeOut(b) for b in smalls], FadeIn(clump), run_time=0.3)
        agg = tag("aggregates inside the cell", RED, 26, [-2.4, 2.35, 0])
        self.to(14.4, FadeIn(agg, shift=DOWN * 0.1), dur=0.5)
        sec = DashedLine(cell.get_right() + LEFT * 0.1, blood.get_left() + RIGHT * 0.1, color=GREY, stroke_width=5)
        sx = Cross(Square(0.5), stroke_color=RED, stroke_width=8).move_to(sec.get_center())
        slab = T("not secreted", size=26, color=RED).next_to(sx, UP, buff=0.3)
        self.at(15.3)
        self.play(Create(sec), run_time=0.5)
        self.play(Create(sx), FadeIn(slab), run_time=0.5)
        dam = T("damaged liver", size=28, color=RED).move_to(clab)
        self.at(17.0)
        self.play(cell.animate.set_stroke(RED).set_fill(RED, 0.12), Transform(clab, dam), run_time=0.7)
        # ---------------- lungs (18.6-27)
        self.at(18.3)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not head], run_time=0.5)
        band = Rectangle(width=11.6, height=1.1, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.08).move_to([0, 1.95, 0])
        bl = T("blood", size=24, color=GREY).move_to([-5.0, 2.75, 0])
        alv = VGroup(*[Circle(0.42, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.18).move_to([-4.6 + 1.15 * i, -1.0, 0]) for i in range(9)])
        tl = T("lung tissue", size=26, color=GREY).move_to([0, -2.5, 0])
        self.to(18.7, FadeIn(band), FadeIn(bl), FadeIn(alv), FadeIn(tl), dur=0.6)
        ghost = blob(0.42, 0.05, 1, BLUE, 0.0, width=4).move_to([-4.2, 1.95, 0])
        ghost.set_stroke(BLUE, 4, 0.8)
        gc = Cross(Square(0.9), stroke_color=RED, stroke_width=7).move_to(ghost)
        gl = T("antitrypsin missing", size=24, color=BLUE).next_to(ghost, RIGHT, buff=0.35)
        self.to(19.6, Create(ghost), FadeIn(gl), dur=0.5)
        self.play(Create(gc), run_time=0.4)
        els = VGroup(*[chip("elastase", GOLD, size=24, pad=0.14) for _ in range(3)])
        els.arrange(RIGHT, buff=0.35).move_to([3.1, 0.75, 0])
        self.to(21.6, LaggedStart(*[FadeIn(e, shift=DOWN * 0.15) for e in els], lag_ratio=0.3), dur=1.0)
        arrs = VGroup(*[Arrow(els[i].get_bottom(), alv[5 + i].get_top() + UP * 0.1, buff=0.08, color=GOLD, stroke_width=5, max_tip_length_to_length_ratio=0.2) for i in range(3)])
        unc = T("unchecked", size=26, color=GOLD).move_to([-0.8, 0.75, 0])
        self.to(23.1, LaggedStart(*[GrowArrow(a) for a in arrs], lag_ratio=0.25), FadeIn(unc), dur=1.2)
        # tissue destroyed
        self.at(24.5)
        self.play(*[a.animate.set_stroke(RED).set_fill(RED, 0.15) for a in alv[4:]], run_time=0.5)
        hole = Circle(1.05, stroke_color=RED, stroke_width=5, fill_color=RED, fill_opacity=0.08).move_to([2.3, -1.0, 0])
        self.play(*[FadeOut(a, scale=0.3) for a in alv[4:]], FadeIn(hole, scale=0.5), FadeOut(unc), FadeOut(tl), run_time=1.3)
        em = T("emphysema", size=34, color=RED).move_to([2.3, -2.5, 0])
        self.to(26.3, FadeIn(em, shift=UP * 0.1), dur=0.6)
        # ---------------- summary (27.7-34)
        self.at(27.5)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not head], run_time=0.5)
        one = chip("one amino acid change", RED, size=36, pad=0.28).move_to([0, 1.7, 0])
        o1 = chip("liver: aggregation", RED, size=30).move_to([-3.4, -0.7, 0])
        o2 = chip("lungs: elastase unchecked", RED, size=30).move_to([3.4, -0.7, 0])
        a1 = Arrow(one.get_bottom() + LEFT * 0.6, o1.get_top(), buff=0.12, color=RED, stroke_width=5)
        a2 = Arrow(one.get_bottom() + RIGHT * 0.6, o2.get_top(), buff=0.12, color=RED, stroke_width=5)
        self.to(27.8, FadeIn(one, shift=DOWN * 0.15), dur=0.7)
        self.to(28.7, GrowArrow(a1), GrowArrow(a2), FadeIn(o1, shift=UP * 0.1), FadeIn(o2, shift=UP * 0.1), dur=0.9)
        fid = T("folding fidelity matters", size=42, font=TITLE_FONT).move_to([0, -2.6, 0])
        self.to(32.0, FadeIn(fid, shift=UP * 0.1), dur=0.9)
        self.finish()


class S06End(EndCard):
    LINE = "Now explore the Ramachandran map yourself in the lesson."
