"""Too costly to throw away: build it, recycle it, or pay in uric acid  (Biochemistrypedia nucleotide-metabolism explainer)

One through-line: a nucleotide is expensive, so the cell recycles (salvage) instead of building (de novo);
break the recycling (Lesch-Nyhan) or reach the human end of the road (no uricase) and the bill arrives as uric acid.

COLOR MAP (one color per concept, whole video)
  GREEN  = a finished nucleotide (IMP, AMP, GMP, "nucleotide")
  YELLOW = a free purine base / ring (hypoxanthine, guanine, adenine, xanthine)
  BLUE   = an enzyme (HGPRT, APRT, xanthine oxidase, uricase)
  PURPLE = PRPP, the activated ribose
  ORANGE = ATP, the cost (coins)
  RED    = uric acid / urate crystals, and every "broken" X
  TEAL   = allopurinol, the drug
  GREY   = axes, structure, de-emphasized text, nucleosides (adenosine, inosine)
  GOLD   = one highlight frame only
No molecular structures: chips, coins, tiles, arrows, a gauge. Nothing here is a drawn molecule.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

config.disable_caching = True

PURPLE = "#B58CD9"
ORANGE = "#E8913A"


# ---------------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------------
def solid(mob, pad=0.03):
    """Opaque backing so a line passing behind a chip does not show through it."""
    return VGroup(BackgroundRectangle(mob, color=BG, fill_opacity=1, buff=pad, stroke_width=0), mob)


def xmark(target, size=0.42, w=9):
    c = target.get_center()
    return VGroup(Line(c + np.array([-size, -size, 0]), c + np.array([size, size, 0]), color=RED, stroke_width=w),
                  Line(c + np.array([-size, size, 0]), c + np.array([size, -size, 0]), color=RED, stroke_width=w))


def arr(a, b, color=GREY, w=4):
    return Arrow(np.array(a, float), np.array(b, float), buff=0, color=color, stroke_width=w,
                 max_tip_length_to_length_ratio=0.3)


def link(a, b, color=GREY, gap=0.1, w=4):
    """Arrow from the edge of chip a to the edge of chip b."""
    d = b.get_center() - a.get_center()
    d = d / np.linalg.norm(d)
    return arr(a.get_boundary_point(d) + d * gap, b.get_boundary_point(-d) - d * gap, color, w)


def use_chip(top, bottom, color=GREY):
    lines = VGroup(T(top, 28, TEXT, weight=BOLD), T(bottom, 24, GREY)).arrange(DOWN, buff=0.08)
    box = RoundedRectangle(corner_radius=0.14, width=lines.width + 0.55, height=lines.height + 0.36,
                           stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.12)
    return VGroup(box, lines.move_to(box))


def dim(c, k):
    """Fade a chip without its fill turning into a solid slab (set_opacity would)."""
    return AnimationGroup(c[0].animate.set_stroke(opacity=k).set_fill(opacity=0.16 * k), c[1].animate.set_opacity(k))


def coin(r=0.31):
    return Circle(radius=r, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.85)


def poly_path(*pts):
    m = VMobject()
    m.set_points_as_corners([np.array(p, float) for p in pts])
    return m


def dot(color=YELLOW, r=0.11):
    return Dot(radius=r, color=color)


# ---------------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Nucleotide metabolism"
    TITLE = "Too costly to throw away"


# ---------------------------------------------------------------------------------------------------
class S01Cost(SpokenScene):
    """A nucleotide is expensive: what it is used for, what it costs (a pile of ATP), and that the cell keeps it."""

    def construct(self):
        hub = chip("nucleotide", GREEN, 40).move_to([0, 0.9, 0])
        self.play(FadeIn(hub, scale=0.9), run_time=0.8)

        self.at("most expensive")
        self.play(Circumscribe(hub, color=ORANGE, time_width=0.6, run_time=1.2))

        specs = [("DNA and RNA", "the letters", [-4.3, 2.6, 0], "Nucleotides are the letters"),
                 ("ATP, GTP", "carriers of energy", [4.3, 2.6, 0], "carriers of energy"),
                 ("cyclic AMP", "signaling cores", [-4.3, -0.8, 0], "cores of signaling"),
                 ("NAD⁺, FAD, CoA", "cofactor backbones", [4.3, -0.8, 0], "backbones of cofactors")]
        uses, links = [], []
        for top, bot, pos, cue in specs:
            u = use_chip(top, bot).move_to(pos)
            ln = link(hub, u, GREY, gap=0.12)
            self.at(cue)
            self.play(GrowArrow(ln), FadeIn(u, shift=ln.get_vector() * 0.15), run_time=0.8)
            uses.append(u)
            links.append(ln)

        # --- cost: building the ring from scratch burns a pile of ATP -------------------------------
        self.at("Building their rings")
        ring = chip("purine ring", YELLOW, 30).move_to([-5.0, 1.2, 0])
        self.play(FadeOut(VGroup(*uses, *links)), hub.animate.move_to([0.5, 1.2, 0]), run_time=0.9)
        a1 = arr([-3.55, 1.2, 0], [-1.35, 1.2, 0], GREY)
        scratch = T("built from scratch", 24, GREY).move_to([-2.45, 0.55, 0])
        self.play(FadeIn(ring, shift=RIGHT * 0.2), GrowArrow(a1), FadeIn(scratch), run_time=0.9)

        self.at("costs a small fortune")
        coins = []
        for r in range(3):
            for c in range(3 - r):
                k = coin(0.4)
                k.move_to([4.2 + (c - (2 - r) / 2) * 0.9, -0.05 + r * 0.8, 0])
                coins.append(k)
        self.play(LaggedStart(*[FadeIn(k, shift=DOWN * 0.5) for k in coins], lag_ratio=0.25), run_time=2.0)
        atp = T("ATP", 32, ORANGE, weight=BOLD).move_to([4.2, -0.85, 0])
        self.play(FadeIn(atp), run_time=0.4)

        # --- the cell almost never throws one away -------------------------------------------------
        self.at("almost never throws")
        bin_ = chip("thrown away", GREY, 28).move_to([0.5, -2.5, 0])
        down = arr([0.5, 0.7, 0], [0.5, -2.0, 0], GREY)
        self.play(GrowArrow(down), FadeIn(bin_), run_time=0.8)
        xm = xmark(VGroup(down), 0.4).move_to([0.5, -0.65, 0])
        self.play(Create(xm), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------------
class S02Denovo(SpokenScene):
    """De novo: ring built piece by piece onto PRPP, about ten enzymatic steps, about six ATP, out comes IMP -> AMP, GMP."""

    def construct(self):
        head = T("Two routes to a purine nucleotide", 38, font=TITLE_FONT).move_to([0, 3.1, 0])
        self.play(FadeIn(head, shift=UP * 0.1), run_time=0.8)

        self.at("the difference is mostly")
        c_dn = chip("de novo", GREY, 32).move_to([-2.4, 1.5, 0])
        c_sv = chip("salvage", GREY, 32).move_to([2.4, 1.5, 0])
        self.play(FadeIn(c_dn, shift=UP * 0.1), FadeIn(c_sv, shift=UP * 0.1), run_time=0.8)
        self.at("cost")
        k_dn = VGroup(*[coin(0.2) for _ in range(6)]).arrange(RIGHT, buff=0.1).next_to(c_dn, DOWN, buff=0.35)
        k_sv = coin(0.2).next_to(c_sv, DOWN, buff=0.35)
        k = VGroup(k_dn, k_sv)
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.2) for c in k_dn], lag_ratio=0.15),
                  FadeIn(k_sv, shift=DOWN * 0.2), run_time=0.7)

        # --- de novo only ----------------------------------------------------------------------------
        self.at("de novo synthesis builds")
        title2 = T("De novo synthesis", 38, font=TITLE_FONT, color=TEXT).move_to([0, 3.1, 0])
        self.play(FadeOut(VGroup(c_sv, k, c_dn)), FadeOut(head, shift=UP * 0.2), FadeIn(title2, shift=UP * 0.2), run_time=0.9)

        # ten tiles = the ring being built piece by piece (floating), then they land on PRPP
        tiles = VGroup(*[RoundedRectangle(corner_radius=0.1, width=0.6, height=0.6, stroke_width=0,
                                          fill_color=YELLOW, fill_opacity=0.9) for _ in range(10)])
        tiles.arrange(RIGHT, buff=0.12).move_to([-1.0, 1.65, 0])
        self.at("atom by atom")
        ring_lbl = T("the purine ring, piece by piece", 26, YELLOW).next_to(tiles, UP, buff=0.3)
        self.play(LaggedStart(*[FadeIn(t, scale=0.4) for t in tiles], lag_ratio=0.12), FadeIn(ring_lbl, run_time=0.6),
                  run_time=1.3)

        self.at("directly onto")
        prpp = chip("PRPP", PURPLE, 38).move_to([-5.2, 0.9, 0])
        self.play(FadeIn(prpp, shift=RIGHT * 0.3), FadeOut(ring_lbl),
                  tiles.animate.move_to([-4.2 + tiles.width / 2, 0.9, 0]), run_time=0.9)
        self.at("activated ribose")
        rib = T("activated ribose", 26, GREY).next_to(prpp, DOWN, buff=0.25)
        self.play(FadeIn(rib), run_time=0.5)

        # --- ten steps, six ATP -------------------------------------------------------------------------
        self.at("about 10 enzymatic steps")
        steps = T("about ten enzymatic steps", 30, BLUE).move_to([-0.6, 0.0, 0])
        self.play(LaggedStart(*[t.animate.set_stroke(BLUE, 4) for t in tiles], lag_ratio=0.1),
                  FadeIn(steps), run_time=1.3)
        self.at("spends roughly")
        n = ValueTracker(1)
        counter = always_redraw(lambda: M(f"{int(round(n.get_value()))} ATP", 44, ORANGE).move_to([2.6, -1.9, 0]))
        coins = [coin(0.38).move_to([-5.4 + 0.92 * i, -1.9, 0]) for i in range(6)]
        for i, cn in enumerate(coins):
            if i == 0:
                self.play(FadeIn(cn, shift=DOWN * 0.4), FadeIn(counter), run_time=0.35, rate_func=linear)
            else:
                self.play(FadeIn(cn, shift=DOWN * 0.4), n.animate.set_value(i + 1), run_time=0.35, rate_func=linear)
        approx = M("~6 ATP", 44, ORANGE).move_to([2.6, -1.9, 0])
        self.remove(counter)
        self.add(approx)
        # --- out comes IMP -------------------------------------------------------------------------------
        self.at("finished purine nucleotide")
        nuc = chip("nucleotide", GREEN, 40).move_to([-0.9, 0.9, 0])
        self.play(FadeOut(rib), FadeOut(steps),
                  ReplacementTransform(VGroup(prpp, tiles), nuc), run_time=1.1)
        self.at("IMP")
        imp = chip("IMP", GREEN, 44).move_to(nuc)
        self.play(ReplacementTransform(nuc, imp), run_time=0.5)
        self.at("Both AMP")
        amp = chip("AMP", GREEN, 44).move_to([3.4, 2.2, 0])
        gmp = chip("GMP", GREEN, 44).move_to([3.4, -0.3, 0])
        l1, l2 = link(imp, amp, GREY), link(imp, gmp, GREY)
        self.play(GrowArrow(l1), FadeIn(amp, shift=l1.get_vector() * 0.1), run_time=0.7)
        self.at("GMP")
        self.play(GrowArrow(l2), FadeIn(gmp, shift=l2.get_vector() * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------------
class S03Salvage(SpokenScene):
    """Salvage: free base + PRPP -> nucleotide in one step (HGPRT, APRT); ~90% recovered; the default."""

    def construct(self):
        rows = [("hypoxanthine", "IMP", "HGPRT", 1.9), ("guanine", "GMP", "HGPRT", 0.6), ("adenine", "AMP", "APRT", -0.7)]
        XB, XN = -3.4, 4.6
        bases, nucs, arrows, plabels, enz = [], [], [], [], []
        title = T("Salvage", 40, font=TITLE_FONT).move_to([-5.2, 3.15, 0])
        self.play(FadeIn(title, shift=UP * 0.1), run_time=0.7)

        self.at("a free base")
        for (b, nm, e, y), cue in zip(rows, ("hypoxanthine", "guanine", "adenine")):
            ch = chip(b, YELLOW, 30).move_to([XB, y, 0])
            bases.append(ch)
        # right-align every base chip to a common right edge so the arrows start from one column
        right_edge = max(c.get_right()[0] for c in bases)
        for c in bases:
            c.shift(RIGHT * (right_edge - c.get_right()[0]))
        for c, cue in zip(bases, ("hypoxanthine", "guanine", "adenine")):
            self.at(cue)
            self.play(FadeIn(c, shift=RIGHT * 0.2), run_time=0.6)

        self.at("reattaches it to")
        for (b, nm, e, y), c in zip(rows, bases):
            a = arr([right_edge + 0.2, y, 0], [XN - 0.85, y, 0], GREY)
            pl = T("+ PRPP", 24, PURPLE).move_to([right_edge + 1.4, y + 0.38, 0])
            n = chip(nm, GREEN, 32).move_to([XN, y, 0])
            arrows.append(a)
            plabels.append(pl)
            nucs.append(n)
        self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(pl)) for a, pl in zip(arrows, plabels)],
                              lag_ratio=0.25), run_time=1.2)
        self.play(LaggedStart(*[FadeIn(n, scale=0.8) for n in nucs], lag_ratio=0.25), run_time=0.9)
        self.at("single step")
        step = T("one step", 30, TEXT, weight=BOLD).move_to([(right_edge + XN) / 2 - 0.2, 2.95, 0])
        self.play(FadeIn(step), Indicate(VGroup(*arrows), color=TEXT, scale_factor=1.04), run_time=1.0)

        # --- the two enzymes ------------------------------------------------------------------------
        xm = (right_edge + 0.2 + XN - 0.85) / 2 + 0.5
        self.at("The enzyme HGPRT")
        e1 = solid(chip("HGPRT", BLUE, 26).move_to([xm, 1.9, 0]))
        e2 = solid(chip("HGPRT", BLUE, 26).move_to([xm, 0.6, 0]))
        self.play(FadeIn(e1, scale=0.8), FadeIn(e2, scale=0.8), run_time=0.7)
        self.at("salvages hypoxanthine")
        self.play(Indicate(bases[0], color=YELLOW, scale_factor=1.1), run_time=0.8)
        self.at("guanine", nth=1)
        self.play(Indicate(bases[1], color=YELLOW, scale_factor=1.1), run_time=0.8)
        self.at("a PRT")
        e3 = solid(chip("APRT", BLUE, 26).move_to([xm, -0.7, 0]))
        self.play(FadeIn(e3, scale=0.8), run_time=0.6)
        self.at("salvages adenine")
        self.play(Indicate(bases[2], color=YELLOW, scale_factor=1.1), run_time=0.8)

        # --- ~90% recovered -----------------------------------------------------------------------------
        self.at("Recycling is so much cheaper")
        lbl = T("free purines recovered", 28, GREY).move_to([-3.45, -2.2, 0])
        track = Rectangle(width=6.0, height=0.5, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to([-0.1, -2.9, 0])
        track.align_to([-5.9, 0, 0], LEFT)
        self.play(FadeIn(lbl), Create(track), run_time=0.8)
        self.at("something like 90")
        fill = Rectangle(width=6.0 * 0.9, height=0.5, stroke_width=0, fill_color=GREEN, fill_opacity=0.9)
        fill.align_to(track, LEFT).align_to(track, DOWN)
        pct = M("~90%", 36, GREEN).next_to(track, RIGHT, buff=0.3)
        self.play(GrowFromEdge(fill, LEFT), FadeIn(pct), run_time=1.5)

        self.at("Salvage is the default")
        frame = SurroundingRectangle(VGroup(*bases, *nucs, e1, e2, e3), color=GOLD, buff=0.3, stroke_width=3,
                                     corner_radius=0.2)
        self.play(Create(frame), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------------
class S04Lesch(SpokenScene):
    """Lesch-Nyhan: HGPRT missing -> bases spill into catabolism -> uric acid; PRPP piles up -> more de novo -> more to degrade."""

    def construct(self):
        B = chip("free bases", YELLOW, 28).move_to([-3.2, 1.6, 0])
        H = chip("HGPRT", BLUE, 28).move_to([0.3, 1.6, 0])
        N = chip("nucleotides", GREEN, 28).move_to([3.9, 1.6, 0])
        a1 = link(B, H)
        a2 = link(H, N)
        self.play(FadeIn(B), FadeIn(H), FadeIn(N), GrowArrow(a1), GrowArrow(a2), run_time=0.6)

        self.at("recycling is gone")
        x = xmark(H, 0.33, 7)
        self.play(Create(x), dim(H, 0.55), a1.animate.set_opacity(0.3), a2.animate.set_opacity(0.3),
                  dim(N, 0.3), run_time=0.8)

        self.at("In Lesch")
        ln = T("Lesch-Nyhan syndrome", 34, font=TITLE_FONT).move_to([0, 3.05, 0])
        self.play(FadeIn(ln, shift=DOWN * 0.1), run_time=0.7)
        self.at("X linked")
        xl = T("X-linked defect", 26, GREY).next_to(ln, DOWN, buff=0.12)
        self.play(FadeIn(xl), run_time=0.5)
        self.at("is missing")
        miss = T("HGPRT missing", 26, RED).next_to(H, DOWN, buff=0.22)
        self.play(FadeIn(miss), run_time=0.5)

        # --- bases spill into the catabolic lane -----------------------------------------------------------
        U = chip("uric acid", RED, 30).move_to([3.9, -0.7, 0])
        lane_pts = [[-3.2, 1.2, 0], [-3.2, -0.7, 0], [U.get_left()[0] - 0.1, -0.7, 0]]
        self.at("Free bases")
        self.play(Indicate(B, color=YELLOW, scale_factor=1.08), run_time=0.8)
        self.at("dumped into")
        lane1 = Line(lane_pts[0], lane_pts[1], color=GREY, stroke_width=4)
        lane2 = arr(lane_pts[1], lane_pts[2], GREY)
        lane_lbl = T("catabolism", 24, GREY).move_to([0.3, -0.33, 0])
        path = poly_path(*lane_pts)
        dots = [dot() for _ in range(5)]
        self.play(Create(lane1), GrowArrow(lane2), FadeIn(lane_lbl), run_time=0.5)
        self.add(*dots)
        for d in dots:
            d.move_to(path.get_start())
        self.play(LaggedStart(*[MoveAlongPath(d, path, rate_func=linear) for d in dots], lag_ratio=0.22),
                  run_time=2.1)
        self.remove(*dots)
        self.at("turned into uric acid")
        self.play(FadeIn(U, scale=0.85), run_time=0.4)
        self.play(Indicate(U, color=RED, scale_factor=1.12), run_time=0.5)

        # --- PRPP piles up, pushes de novo ---------------------------------------------------------------------
        self.at("The PRPP")
        tank_box = Rectangle(width=0.9, height=1.9, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to([-5.6, -2.3, 0])
        lvl = ValueTracker(0.22)

        def mk_fill():
            h = 1.9 * lvl.get_value()
            r = Rectangle(width=0.9, height=max(h, 0.02), stroke_width=0, fill_color=PURPLE, fill_opacity=0.85)
            r.move_to([-5.6, tank_box.get_bottom()[1] + max(h, 0.02) / 2, 0])
            return r

        fill = always_redraw(mk_fill)
        tank_lbl = T("PRPP", 28, PURPLE, weight=BOLD).next_to(tank_box, UP, buff=0.14)
        self.play(Create(tank_box), FadeIn(tank_lbl), run_time=0.7)
        self.add(fill)
        self.at("piles up")
        self.play(lvl.animate.set_value(0.95), run_time=0.9, rate_func=smooth)
        self.at("pushes de novo")
        D = chip("de novo synthesis", GREY, 24).move_to([-2.35, -2.3, 0])
        a_t = arr([-5.1, -2.3, 0], [D.get_left()[0] - 0.1, -2.3, 0], PURPLE)
        self.play(GrowArrow(a_t), FadeIn(D), run_time=0.8)
        self.at("even higher")
        pts2 = [[D.get_right()[0] + 0.1, -2.3, 0], [1.5, -2.3, 0], [1.5, -0.7, 0], lane_pts[2]]
        l_a = Line(pts2[0], pts2[1], color=GREY, stroke_width=4)
        l_b = Line(pts2[1], pts2[2], color=GREY, stroke_width=4)
        path2 = poly_path(*pts2)
        self.play(Create(l_a), Create(l_b), run_time=0.7)
        self.at("still more purines")
        more = T("more purines", 24, GREY).move_to([0.3, -1.9, 0])
        dots2 = [dot() for _ in range(6)]
        for d in dots2:
            d.move_to(path2.get_start())
        self.add(*dots2)
        self.play(FadeIn(more),
                  LaggedStart(*[MoveAlongPath(d, path2, rate_func=linear) for d in dots2], lag_ratio=0.22),
                  run_time=3.4)
        self.remove(*dots2)

        # --- the bill ----------------------------------------------------------------------------------------------
        self.at("hyperuricemia")
        hu = T("hyperuricemia", 26, RED).move_to([4.2, -1.65, 0])
        self.play(U.animate.scale(1.35).move_to([4.2, -0.7, 0]), FadeIn(hu), run_time=0.9)
        self.at("neurological disease")
        nd = chip("neurological disease", GREY, 28).move_to([4.3, -2.75, 0])
        self.play(FadeIn(nd, shift=UP * 0.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------------
class S05Uric(SpokenScene):
    """Catabolism chain to uric acid; xanthine oxidase; uricase turns it to soluble allantoin in most mammals, not in us."""

    def construct(self):
        names = [("adenosine", GREY), ("inosine", GREY), ("hypoxanthine", YELLOW), ("xanthine", YELLOW),
                 ("uric acid", RED)]
        chips = VGroup(*[chip(n, c, 26, pad=0.18) for n, c in names]).arrange(RIGHT, buff=0.8)
        fit(chips, max_w=12.4)
        chips.move_to([0, 1.0, 0])
        ad, ino, hyp, xan, uri = chips
        arrows = [link(chips[i], chips[i + 1], GREY, gap=0.08) for i in range(4)]

        self.at("taken apart")
        t = T("a purine is retired", 32, font=TITLE_FONT).move_to([0, 3.15, 0])
        self.play(FadeIn(t, shift=UP * 0.1), run_time=0.8)
        self.at("AMP and adenosine")
        amp = chip("AMP", GREEN, 26, pad=0.18).move_to([ad.get_center()[0], 2.35, 0])
        la = arr([amp.get_center()[0], amp.get_bottom()[1] - 0.05, 0], [ad.get_center()[0], ad.get_top()[1] + 0.05, 0])
        self.play(FadeOut(t), FadeIn(amp), GrowArrow(la), FadeIn(ad), run_time=0.9)
        self.at("funnel through")
        self.play(GrowArrow(arrows[0]), FadeIn(ino), run_time=0.8)
        self.at("hypoxanthine")
        self.play(GrowArrow(arrows[1]), FadeIn(hyp), run_time=0.8)

        # --- xanthine oxidase -----------------------------------------------------------------------------
        self.at("xanthine oxidase")
        mid2, mid3 = arrows[2].get_center(), arrows[3].get_center()
        xo = solid(chip("xanthine oxidase", BLUE, 26)).move_to([(mid2[0] + mid3[0]) / 2, -0.35, 0])
        k2 = Line(xo.get_top() + LEFT * 0.7, mid2 + DOWN * 0.1, color=BLUE, stroke_width=3)
        k3 = Line(xo.get_top() + RIGHT * 0.7, mid3 + DOWN * 0.1, color=BLUE, stroke_width=3)
        self.play(FadeIn(xo, shift=UP * 0.15), run_time=0.7)
        self.at("oxidizes hypoxanthine to")
        self.play(GrowArrow(arrows[2]), Create(k2), FadeIn(xan), run_time=0.8)
        self.at("xanthine to uric acid")
        self.play(GrowArrow(arrows[3]), Create(k3), FadeIn(uri), run_time=0.8)
        self.at("Guanine joins")
        gu = chip("guanine", YELLOW, 26, pad=0.18).move_to([xan.get_center()[0], 2.35, 0])
        lg = arr([gu.get_center()[0], gu.get_bottom()[1] - 0.05, 0], [xan.get_center()[0], xan.get_top()[1] + 0.05, 0])
        self.play(FadeIn(gu), GrowArrow(lg), run_time=0.8)

        # --- uricase ---------------------------------------------------------------------------------------------
        xu = uri.get_center()[0]
        self.at("Most mammals")
        uc = chip("uricase", BLUE, 26).move_to([xu, -1.6, 0])
        al = chip("allantoin", GREY, 26).move_to([xu, -2.9, 0])
        d1 = arr([xu, uri.get_bottom()[1] - 0.05, 0], [xu, uc.get_top()[1] + 0.05, 0])
        d2 = arr([xu, uc.get_bottom()[1] - 0.05, 0], [xu, al.get_top()[1] + 0.05, 0])
        sol = T("highly soluble", 24, GREY).next_to(al, LEFT, buff=0.3)
        self.play(GrowArrow(d1), FadeIn(uc), run_time=0.7)
        self.at("highly soluble")
        self.play(GrowArrow(d2), FadeIn(al), FadeIn(sol), run_time=0.8)

        self.at("Humans and the other")
        mam = VGroup(uc, al, d1, d2, sol)
        self.play(FadeOut(VGroup(xo, k2, k3)), run_time=0.6)
        self.at("lost a working")
        x = xmark(uc, 0.33, 7)
        self.play(Create(x), dim(uc, 0.45), dim(al, 0.45), d1.animate.set_opacity(0.45), d2.animate.set_opacity(0.45),
                  sol.animate.set_opacity(0.45), run_time=0.8)

        self.at("For us")
        chain = VGroup(chips, *arrows, amp, la, gu, lg)
        self.play(FadeOut(VGroup(mam, x)), chain.animate.shift(DOWN * 0.9), run_time=0.9)
        self.at("end product")
        box = SurroundingRectangle(uri, color=RED, buff=0.16, stroke_width=4, corner_radius=0.2)
        endl = T("end product", 30, RED, weight=BOLD).next_to(uri, DOWN, buff=0.45).align_to([6.2, 0, 0], RIGHT)
        self.play(Create(box), FadeIn(endl), run_time=0.8)
        self.at("sparingly soluble")
        spar = T("sparingly soluble", 28, GREY).next_to(endl, DOWN, buff=0.18).align_to([6.2, 0, 0], RIGHT)
        self.play(FadeIn(spar), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------------
class S06Gout(SpokenScene):
    """No uricase -> urate climbs past ~6.8 mg/dL -> needle crystals in a joint; allopurinol blocks xanthine oxidase -> urate falls."""

    def construct(self):
        # opener: the missing enzyme
        uc = chip("uricase", BLUE, 34).move_to([0, 0.6, 0])
        self.play(FadeIn(uc), run_time=0.5)
        uc_x = xmark(uc, 0.5)
        self.play(Create(uc_x), dim(uc, 0.35), run_time=0.7)
        gout = T("gout", 60, font=TITLE_FONT).move_to([0, -1.1, 0])
        self.at("gout")
        self.play(FadeIn(gout, shift=UP * 0.15), run_time=0.7)

        # --- gauge ---------------------------------------------------------------------------------------------------
        GX, GY0, GH = -5.0, -2.5, 5.0
        sy = lambda v: GY0 + v / 10 * GH
        gauge = Rectangle(width=0.9, height=GH, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to([GX, GY0 + GH / 2, 0])
        ticks = VGroup()
        for v in (0, 2, 4, 6, 8, 10):
            ticks.add(Line([GX - 0.45, sy(v), 0], [GX - 0.58, sy(v), 0], color=GREY, stroke_width=3))
            ticks.add(M(str(v), 22, GREY).move_to([GX - 0.95, sy(v), 0]))
        gtitle = T("serum urate (mg/dL)", 24, TEXT).move_to([-4.3, 3.05, 0])
        lv = ValueTracker(3.5)

        def mk_lvl():
            h = max(sy(lv.get_value()) - GY0, 0.02)
            r = Rectangle(width=0.9, height=h, stroke_width=0, fill_color=RED, fill_opacity=0.8)
            r.move_to([GX, GY0 + h / 2, 0])
            return r

        level = always_redraw(mk_lvl)
        self.at("Once serum urate")
        self.play(FadeOut(VGroup(uc, gout, uc_x)), run_time=0.6)
        self.play(Create(gauge), FadeIn(ticks), FadeIn(gtitle), run_time=0.9)
        self.add(level)
        limit = DashedLine([GX - 0.45, sy(6.8), 0], [-3.1, sy(6.8), 0], color=RED, stroke_width=3, dash_length=0.12)
        lim_lbl = M("6.8 mg/dL", 24, RED).move_to([-1.85, sy(6.8), 0])
        self.at("climbs")
        self.play(lv.animate(run_time=3.4, rate_func=smooth).set_value(9.0),
                  Succession(Wait(0.45), AnimationGroup(Create(limit), FadeIn(lim_lbl), run_time=0.6)))

        # --- crystals in a joint -------------------------------------------------------------------------------------
        self.at("begins to crystallize")
        joint = RoundedRectangle(corner_radius=0.25, width=6.2, height=2.7, stroke_color=GREY, stroke_width=3,
                                 fill_opacity=0).move_to([2.9, 1.65, 0])
        jl = T("joint", 24, GREY).move_to(joint.get_corner(UL) + np.array([0.55, -0.32, 0]))
        rng = np.random.default_rng(7)
        crystals = VGroup()
        for i in range(16):
            ang = rng.uniform(0, PI)
            L = rng.uniform(0.5, 0.85)
            cx = rng.uniform(joint.get_left()[0] + 0.7, joint.get_right()[0] - 0.7)
            cy = rng.uniform(joint.get_bottom()[1] + 0.4, joint.get_top()[1] - 0.45)
            if cx < joint.get_left()[0] + 1.4 and cy > joint.get_top()[1] - 0.9:
                cx += 1.4
            d = np.array([np.cos(ang), np.sin(ang), 0])
            n = np.array([-np.sin(ang), np.cos(ang), 0])
            c = np.array([cx, cy, 0])
            pts = [c - d * L / 2, c + n * 0.045, c + d * L / 2, c - n * 0.045]
            crystals.add(Polygon(*pts, stroke_width=0, fill_color=RED, fill_opacity=0.95))
        self.play(Create(joint, run_time=0.4), FadeIn(jl),
                  Succession(Wait(0.3), LaggedStart(*[FadeIn(c, scale=0.3) for c in crystals], lag_ratio=0.07, run_time=1.2)))
        self.at("monosodium urate")
        msu = T("monosodium urate crystals", 24, RED).next_to(joint, DOWN, buff=0.18)
        self.play(FadeIn(msu), run_time=0.5)
        self.at("needle sharp crystals")
        self.play(Indicate(crystals, color=RED, scale_factor=1.1), run_time=1.0)
        self.at("flare")
        self.play(joint.animate.set_stroke(RED, 6), run_time=0.7)

        # --- allopurinol -------------------------------------------------------------------------------------------------
        self.at("The fix")
        self.play(FadeOut(msu), run_time=0.4)
        row = VGroup(chip("hypoxanthine", YELLOW, 24, pad=0.18), chip("xanthine", YELLOW, 24, pad=0.18),
                     chip("uric acid", RED, 24, pad=0.18)).arrange(RIGHT, buff=0.75).move_to([2.9, -0.85, 0])
        hyp, xan, uri = row
        ar = [link(row[0], row[1], GREY, 0.08), link(row[1], row[2], GREY, 0.08)]
        m1, m2 = ar[0].get_center(), ar[1].get_center()
        xo = solid(chip("xanthine oxidase", BLUE, 24)).move_to([(m1[0] + m2[0]) / 2, -2.1, 0])
        k1 = Line(xo.get_top() + LEFT * 0.7, m1 + DOWN * 0.1, color=BLUE, stroke_width=3)
        k2 = Line(xo.get_top() + RIGHT * 0.7, m2 + DOWN * 0.1, color=BLUE, stroke_width=3)
        self.play(FadeIn(row), GrowArrow(ar[0]), GrowArrow(ar[1]), FadeIn(xo), Create(k1), Create(k2), run_time=1.1)
        self.at("Allopurinol")
        allo = chip("allopurinol", TEAL, 26).move_to([-0.2, -2.1, 0])
        self.play(FadeIn(allo, shift=RIGHT * 0.2), run_time=0.6)
        self.at("look alike")
        self.play(Indicate(hyp, color=YELLOW, scale_factor=1.12), Indicate(allo, color=TEAL, scale_factor=1.12), run_time=1.0)
        self.at("inhibits xanthine oxidase")
        bar = Line(xo.get_left() + np.array([-0.12, -0.2, 0]), xo.get_left() + np.array([-0.12, 0.2, 0]),
                   color=TEAL, stroke_width=8)
        blk = arr(allo.get_right() + RIGHT * 0.05, bar.get_center() + LEFT * 0.3, TEAL)
        self.play(GrowArrow(blk), Create(bar), dim(xo[1], 0.55),
                  ar[0].animate.set_opacity(0.25), ar[1].animate.set_opacity(0.25), k1.animate.set_opacity(0.25), k2.animate.set_opacity(0.25),
                  run_time=0.9)
        self.at("urate production falls")
        self.play(lv.animate.set_value(4.2), run_time=1.5, rate_func=smooth)
        self.at("crystals can dissolve")
        self.play(LaggedStart(*[FadeOut(c, scale=0.3) for c in crystals], lag_ratio=0.07),
                  joint.animate.set_stroke(GREY, 3), run_time=1.8)
        self.at("Gertrude")
        who = T("designed by Gertrude Elion and George Hitchings", 24, GREY).move_to([1.9, -3.15, 0])
        self.play(FadeIn(who), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------------
class S07End(EndCard):
    LINE = "Nucleotides are too expensive to throw away."
