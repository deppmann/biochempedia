"""Neuron doctrine: a touch is not a fusion  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = neuron one (the branch and cell on the left)
  YELLOW = neuron two (the branch and cell on the right)
  RED    = the limit of the light microscope (the blind spot)
  ORANGE = Golgi's reading: the branches are joined
  GREEN  = Cajal's reading and the verdict: separate cells, each with its own membrane
  TEAL   = what passes through gap junctions (ions, small molecules, the signal)
  GREY   = tissue, outlines, stain tangle, de-emphasised things
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def smooth(points, color, w=9, opacity=1.0):
    m = VMobject()
    m.set_points_smoothly([np.array([x, y, 0.0]) for x, y in points])
    m.set_stroke(color, w, opacity=opacity)
    m.set_fill(opacity=0)
    return m


def branch(side, color):
    """a stylised nerve branch coming in from one side to the junction at the centre."""
    s = 1 if side == "R" else -1
    pts = [(-6.0, -2.3), (-4.5, -0.9), (-2.9, -1.1), (-1.5, 0.45), (-0.2, 0.04)]
    twigs = [[(-4.5, -0.9), (-5.2, 0.9), (-5.7, 1.9)],
             [(-2.9, -1.1), (-2.6, -1.9), (-2.4, -2.5)],
             [(-1.5, 0.45), (-1.9, 1.3), (-2.0, 2.2)]]
    g = VGroup(smooth(pts, color, 10))
    for t in twigs:
        g.add(smooth(t, color, 6))
    if s == 1:  # mirror through the origin
        g.apply_matrix(np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]]))
    return g


def tip(color, side, length=2.2, w=12, gap=0.3, y=0.0):
    """a blunt branch ending, for the close-up panels. side L comes from the left."""
    s = -1 if side == "L" else 1
    return Line([s * (gap / 2 + length), y, 0], [s * gap / 2, y, 0], color=color, stroke_width=w)


def disc(radius, center, fill=0.0, dashed=True):
    c = Circle(radius=radius, stroke_color=RED, stroke_width=4, fill_color=RED, fill_opacity=fill).move_to(center)
    return DashedVMobject(c, num_dashes=28) if dashed and fill == 0 else c


def cell_pair(gap, h=4.4, yc=0.35, w=4.9):
    """two big cell outlines facing each other across `gap`; returns left, right, left-edge, right-edge."""
    xl = -(gap / 2 + w / 2)
    xr = gap / 2 + w / 2
    L = RoundedRectangle(corner_radius=0.5, width=w, height=h, stroke_color=BLUE, stroke_width=4,
                         fill_color=BLUE, fill_opacity=0.12).move_to([xl, yc, 0])
    R = RoundedRectangle(corner_radius=0.5, width=w, height=h, stroke_color=YELLOW, stroke_width=4,
                         fill_color=YELLOW, fill_opacity=0.12).move_to([xr, yc, 0])
    el = Line([-gap / 2, yc - h / 2 + 0.5, 0], [-gap / 2, yc + h / 2 - 0.5, 0], color=GREEN, stroke_width=9)
    er = Line([gap / 2, yc - h / 2 + 0.5, 0], [gap / 2, yc + h / 2 - 0.5, 0], color=GREEN, stroke_width=9)
    return L, R, el, er


def channel(y, gap, color=TEAL):
    return RoundedRectangle(corner_radius=0.08, width=gap + 0.2, height=0.5, stroke_color=color, stroke_width=4,
                            fill_color=BG, fill_opacity=1).move_to([0, y, 0])


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def label(text, color=TEXT, size=26):
    return T(text, size, color)


class S00Title(TitleCard):
    LESSON = "Seeing neurons: Golgi, Cajal and the neuron doctrine"
    TITLE = "A touch is not a fusion"


# ---------------------------------------------------------------------------------------------
class S01Meet(SpokenScene):
    """two branches meet; touch or fuse; stain shows one branch; the junction gives no answer."""

    def construct(self):
        rng = np.random.default_rng(4)
        A, B = branch("L", BLUE), branch("R", YELLOW)

        # touch / fuse icons (bottom)
        t_l = Line([-4.1, -3.1, 0], [-3.55, -3.1, 0], color=BLUE, stroke_width=9)
        t_r = Line([-3.35, -3.1, 0], [-2.8, -3.1, 0], color=YELLOW, stroke_width=9)
        touch = VGroup(t_l, t_r, label("touch", TEXT, 30).next_to(t_r, RIGHT, buff=0.3))
        f_l = Line([2.3, -3.1, 0], [2.85, -3.1, 0], color=BLUE, stroke_width=9)
        f_r = Line([2.85, -3.1, 0], [3.4, -3.1, 0], color=YELLOW, stroke_width=9)
        fuse = VGroup(f_l, f_r, label("fuse", TEXT, 30).next_to(f_r, RIGHT, buff=0.3))

        self.at("Two fine nerve branches")
        self.play(Create(A), Create(B), run_time=2.0)
        self.at("touch, or do they fuse")
        self.play(FadeIn(touch, shift=UP * 0.1), FadeIn(fuse, shift=UP * 0.1), run_time=0.6)
        self.wait(0.1)

        # stain every cell: a tangle that hides the branches
        tangle = VGroup()
        for _ in range(46):
            tangle.add(Circle(radius=rng.uniform(0.25, 0.4), stroke_color=GREY, stroke_width=3, fill_color=GREY,
                              fill_opacity=0.45).move_to([rng.uniform(-5.8, 5.8), rng.uniform(-2.4, 2.4), 0]))
        self.at("marks every cell body")
        self.play(FadeIn(tangle), A.animate.set_stroke(opacity=0.15), B.animate.set_stroke(opacity=0.15),
                  run_time=1.2)
        stain = chip("Golgi stain: a few cells, completely", GREY, size=24).to_edge(UP, buff=0.4)
        self.at("black reaction")
        self.play(FadeOut(tangle), A.animate.set_stroke(opacity=1), B.animate.set_stroke(opacity=1),
                  FadeIn(stain), run_time=0.9)
        self.at("stay pale")
        pale = VGroup(*[Circle(radius=r, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.18).move_to([x, y, 0])
                        for x, y, r in [(-3.4, 1.9, 0.38), (1.6, 2.0, 0.32), (3.2, -2.3, 0.42), (-1.0, -2.3, 0.3), (5.3, -0.2, 0.34)]])
        self.play(FadeIn(pale), run_time=0.6)
        self.at("single branch")
        self.play(Indicate(A[0], color=BLUE, scale_factor=1.0), A[0].animate.set_stroke(width=14), run_time=1.2)
        self.at("no clear answer")
        q = T("?", 120, TEXT, weight=BOLD).move_to([0, 0.0, 0])
        back = Circle(radius=0.75, stroke_width=0, fill_color=BG, fill_opacity=0.85).move_to(q)
        self.play(FadeIn(back), FadeIn(q, scale=0.6), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Blur(SpokenScene):
    """the resolution limit hides the gap; branches at different depths project on each other."""

    def construct(self):
        # left panel: two tips that touch (top view)
        ctr = np.array([-3.2, 0.5, 0])
        tl = tip(BLUE, "L", 2.8, 16, 0.3).shift(ctr)
        tr = tip(YELLOW, "R", 2.8, 16, 0.3).shift(ctr)
        head_l = label("two branches that touch", TEXT, 28).move_to([-3.2, 3.2, 0])
        self.at("similar preparations")
        self.play(FadeIn(head_l), Create(tl), Create(tr), run_time=1.2)

        d = disc(1.9, ctr)
        lim = M("0.2 µm", 30, RED).next_to(d, DOWN, buff=0.15)
        self.at("cannot separate two points")
        self.play(Create(d), FadeIn(lim), run_time=1.2)
        dfill = disc(1.9, ctr, fill=0.32, dashed=False)
        same = label("looks like one", RED, 26).move_to(ctr + np.array([0, -2.75, 0]))
        self.at("fall inside that limit")
        self.play(FadeIn(dfill), FadeIn(same), run_time=0.8)

        # right panel: side view of a thick section, branches at different depths
        rc = np.array([3.4, 0.8, 0])
        slab = Rectangle(width=5.4, height=3.1, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                         fill_opacity=0.12).move_to(rc)
        a = Line(rc + [-2.5, 0.8, 0], rc + [0.4, 0.8, 0], color=BLUE, stroke_width=14)
        b = Line(rc + [-0.4, -0.8, 0], rc + [2.5, -0.8, 0], color=YELLOW, stroke_width=14)
        head_r = label("pass close at different depths", TEXT, 28).move_to([3.4, 3.1, 0])
        slab_lbl = label("thick section", GREY, 24).next_to(slab, UP, buff=0.12)
        head_r.move_to([3.4, 3.3, 0]); slab_lbl.move_to([3.4, 2.75, 0])
        self.at("different depths")
        self.play(FadeIn(head_r), FadeIn(slab), FadeIn(slab_lbl), Create(a), Create(b), run_time=1.4)
        # view from above: project onto a strip
        arrows = VGroup(*[arr([x, -0.9, 0], [x, -1.5, 0], GREY, 3, 0.15) for x in (2.0, 3.4, 4.8)])
        eye = label("seen from above", GREY, 24).move_to([3.4, -1.85, 0])
        pa = Line([1.0, -2.4, 0], [3.8, -2.4, 0], color=BLUE, stroke_width=12)
        pb = Line([3.0, -2.4, 0], [5.8, -2.4, 0], color=YELLOW, stroke_width=12)
        self.at("look the same")
        self.play(FadeIn(arrows), FadeIn(eye), Create(pa), Create(pb), run_time=1.2)
        glow = Ellipse(width=2.4, height=1.0, stroke_color=RED, stroke_width=3, fill_color=RED,
                       fill_opacity=0.32).move_to([3.4, -2.4, 0])
        self.play(FadeIn(glow), run_time=0.5)
        verdict = T("touch or fusion? The image cannot say.", 28, TEXT).move_to([0, -3.25, 0])
        self.at("contact from fusion")
        self.play(FadeIn(verdict, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Camps(SpokenScene):
    """same blurred junction, two readings: Golgi fills it with a join, Cajal with a gap."""

    def construct(self):
        cl, cr = np.array([-3.2, 0.5, 0]), np.array([3.2, 0.5, 0])

        def panel(ctr):
            tl = tip(BLUE, "L", 2.8, 16, 0.3).shift(ctr)
            tr = tip(YELLOW, "R", 2.8, 16, 0.3).shift(ctr)
            d = disc(1.9, ctr)
            f = disc(1.9, ctr, fill=0.22, dashed=False)
            return VGroup(tl, tr, d, f)

        pl, pr = panel(cl), panel(cr)
        mid = DashedLine([0, 2.7, 0], [0, -3.3, 0], color=GREY, stroke_width=2)
        spot = label("same blind spot", RED, 26).move_to([0, 3.35, 0])
        self.at("blind spot")
        self.play(FadeIn(pl), FadeIn(pr), Create(mid), FadeIn(spot), run_time=1.0)

        hg = chip("Golgi: joined", ORANGE, 28).move_to(cl + [0, 2.95, 0])
        self.at("Golgi saw no visible join")
        self.play(FadeIn(hg, shift=DOWN * 0.1), run_time=0.5)
        bridge = Line(cl + [-0.17, 0, 0], cl + [0.17, 0, 0], color=ORANGE, stroke_width=10)
        fine = label("too fine to see", ORANGE, 26).move_to(cl + [0, -2.35, 0])
        self.at("too fine to see")
        self.play(Create(bridge), FadeIn(fine), run_time=0.8)
        ax = chip("a network of axon branches", ORANGE, 24).move_to(cl + [0, -3.1, 0])
        self.at("axon branches")
        self.play(FadeIn(ax, shift=UP * 0.1), run_time=0.6)

        hc = chip("Cajal: separate", GREEN, 28).move_to(cr + [0, 2.95, 0])
        self.at("Cajal found")
        self.play(FadeIn(hc, shift=DOWN * 0.1), run_time=0.5)
        gapm = VGroup(Line(cr + [-0.15, -0.6, 0], cr + [-0.15, 0.6, 0], color=GREEN, stroke_width=6),
                      Line(cr + [0.15, -0.6, 0], cr + [0.15, 0.6, 0], color=GREEN, stroke_width=6))
        self.at("end close to other cells")
        self.play(Create(gapm), run_time=0.7)
        free = label("free endings: the evidence", GREEN, 26).move_to(cr + [0, -2.35, 0])
        self.at("free endings")
        self.play(FadeIn(free), Indicate(gapm, color=GREEN), run_time=0.9)
        sig = Arrow(cr + [-0.9, 1.3, 0], cr + [0.9, 1.3, 0], buff=0, color=TEAL, stroke_width=5, tip_length=0.22)
        siglbl = label("signals pass at contacts", TEAL, 24).move_to(cr + [0, -3.1, 0])
        self.at("signals pass between cells")
        self.play(GrowArrow(sig), FadeIn(siglbl), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Cleft(SpokenScene):
    """electron microscope: zoom into the blind spot and find two membranes with a cleft."""

    def construct(self):
        gap = 2.8
        L, R, el, er = cell_pair(gap, h=4.4, yc=0.5, w=4.4)
        blur = VGroup(tip(BLUE, "L", 1.0, 14, 0.3), tip(YELLOW, "R", 1.0, 14, 0.3),
                      disc(1.3, ORIGIN), disc(1.3, ORIGIN, fill=0.22, dashed=False)).move_to([0, 0.5, 0])
        blur_lbl = label("light microscope limit", RED, 28).next_to(blur, DOWN, buff=0.3)
        self.at("finer instrument")
        self.play(FadeIn(blur), FadeIn(blur_lbl), run_time=0.8)

        self.at("electron microscope")
        self.play(FadeIn(L), FadeIn(R), blur.animate.scale(4).set_opacity(0), FadeOut(blur_lbl), run_time=1.6)
        self.remove(blur)

        pre = label("neuron one: terminal", BLUE, 24).move_to([-3.6, 3.0, 0])
        post = label("neuron two", YELLOW, 24).move_to([3.6, 3.0, 0])
        self.play(FadeIn(pre), FadeIn(post), run_time=0.4)
        self.at("membranes of two cells stay separate")
        self.play(Create(el), Create(er), run_time=1.0)
        brace = DoubleArrow([-gap / 2, 0.5, 0], [gap / 2, 0.5, 0], buff=0, color=TEXT, stroke_width=4, tip_length=0.2)
        cl = label("cleft", TEXT, 28).move_to([0, 1.1, 0])
        self.at("narrow cleft")
        self.play(GrowFromCenter(brace), FadeIn(cl), run_time=0.7)

        ves = VGroup()
        for x, y in [(-2.1, 2.1), (-3.0, 1.7), (-2.3, 1.2), (-3.4, 0.7), (-2.0, 0.4), (-2.9, -0.1), (-2.2, -0.6), (-3.5, 2.3), (-3.6, -0.5)]:
            ves.add(Circle(radius=0.17, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.5).move_to([x, y, 0]))
        self.at("Small vesicles crowd")
        self.play(LaggedStart(*[GrowFromCenter(v) for v in ves], lag_ratio=0.12), run_time=1.4)

        nm = M("10 to 20 nm", 26, GREEN).move_to([0, -0.2, 0])
        self.at("10 to 20 nanometers")
        self.play(FadeIn(nm, shift=UP * 0.1), run_time=0.6)

        redbar = Line([-6.0, -2.35, 0], [-1.0, -2.35, 0], color=RED, stroke_width=10)
        redl = label("light microscope limit, 0.2 µm", RED, 26).next_to(redbar, RIGHT, buff=0.3)
        grbar = Line([-6.0, -3.05, 0], [-5.5, -3.05, 0], color=GREEN, stroke_width=10)
        grl = label("synaptic cleft", GREEN, 26).next_to(grbar, RIGHT, buff=0.3)
        self.at("times smaller")
        self.play(Create(redbar), FadeIn(redl), run_time=0.7)
        self.play(Create(grbar), FadeIn(grl), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Gap(SpokenScene):
    """gap junction channels cross; only small things pass; they close; the cells stay two cells."""

    def construct(self):
        gap = 0.8
        L, R, el, er = cell_pair(gap, h=4.9, yc=0.1, w=5.4)
        lab_l = label("neuron one", BLUE, 24).move_to([-3.6, 2.95, 0])
        lab_r = label("neuron two", YELLOW, 24).move_to([3.6, 2.95, 0])
        self.at("one real exception")
        self.play(FadeIn(L), FadeIn(R), Create(el), Create(er), run_time=1.2)

        ys = [1.3, 0.1, -1.1]
        chans = VGroup(*[channel(y, gap) for y in ys])
        self.at("Gap junctions join some neurons")
        self.play(LaggedStart(*[FadeIn(c, scale=0.7) for c in chans], lag_ratio=0.2), run_time=1.0)
        gj = label("gap junction channels", TEAL, 26).move_to([0, 3.05, 0])
        self.at("channels cross")
        self.play(FadeIn(gj), Indicate(chans, color=TEAL, scale_factor=1.08), run_time=1.0)

        dots = VGroup(*[Circle(radius=0.15, stroke_width=0, fill_color=TEAL, fill_opacity=1).move_to([-1.8 - 0.5 * k, y, 0])
                        for y in ys for k in (0, 1)])
        sm = label("ions and small molecules", TEAL, 26).move_to([-3.0, -2.95, 0])
        self.at("Ions and small molecules")
        self.play(FadeIn(dots), FadeIn(sm), run_time=0.5)
        self.play(*[d.animate.shift(RIGHT * 4.4) for d in dots], run_time=2.2, rate_func=linear)

        self.at("keeps its own membrane")
        self.play(Indicate(VGroup(el, er), color=GREEN, scale_factor=1.0), run_time=1.0)

        big = Circle(radius=0.4, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.55).move_to([-4.6, -2.95, 0])
        biglbl = label("larger than about 1 kDa", GREY, 24).next_to(big, RIGHT, buff=0.25)
        self.at("only molecules up to roughly")
        self.play(FadeOut(dots), FadeOut(sm), FadeIn(big), FadeIn(biglbl), run_time=0.5)
        self.play(big.animate.move_to([-1.0, 0.1, 0]).set_opacity(1), run_time=0.9)
        self.play(Indicate(chans[1], color=RED, scale_factor=1.0), run_time=0.4)
        self.play(big.animate.move_to([-2.4, -1.2, 0]), run_time=0.5)

        shut = VGroup(*[Line([-0.5, y, 0], [0.5, y, 0], color=RED, stroke_width=8) for y in ys])
        shutl = label("and they can close", RED, 26).move_to([3.2, -2.95, 0])
        self.at("they can close")
        self.play(FadeOut(big), FadeOut(biglbl), Create(shut), FadeIn(shutl), run_time=0.8)

        self.at("coupled")
        dots2 = VGroup(*[Circle(radius=0.15, stroke_width=0, fill_color=TEAL, fill_opacity=1).move_to([-1.3, y, 0]) for y in ys])
        self.play(FadeOut(shut), FadeOut(shutl), FadeIn(dots2), run_time=0.3)
        self.play(*[d.animate.shift(RIGHT * 2.6) for d in dots2], run_time=0.9, rate_func=linear)
        self.at("not one cell")
        self.play(FadeIn(lab_l), FadeIn(lab_r), FadeOut(gj), FadeOut(dots2), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """no network; coupling through regulated pores between separate cells; the rule."""

    def construct(self):
        gap = 0.8
        L, R, el, er = cell_pair(gap, h=4.9, yc=0.1, w=5.4)
        ys = [1.3, 0.1, -1.1]
        chans = VGroup(*[channel(y, gap) for y in ys])
        shut = VGroup(*[Line([-0.5, y, 0], [0.5, y, 0], color=RED, stroke_width=8) for y in ys])
        lab_l = label("neuron one", BLUE, 24).move_to([-3.6, 2.95, 0])
        lab_r = label("neuron two", YELLOW, 24).move_to([3.6, 2.95, 0])
        self.add(L, R, el, er, chans, lab_l, lab_r)

        net = chip("Golgi's network", ORANGE, 30).move_to([0, -3.05, 0])
        self.at("network")
        self.play(FadeIn(net, shift=UP * 0.1), run_time=0.5)
        self.at("does not exist")
        cross = Line(net.get_corner(DL) + [-0.1, -0.1, 0], net.get_corner(UR) + [0.1, 0.1, 0], color=RED, stroke_width=8)
        self.play(Create(cross), net.animate.set_opacity(0.5), run_time=0.6)

        self.at("coupling through regulated pores")
        pores = label("regulated pores", TEAL, 28).move_to([0, 3.05, 0])
        self.play(FadeIn(pores), Indicate(chans, color=TEAL, scale_factor=1.08), run_time=1.2)

        self.at("Keep this rule")
        self.play(FadeOut(net), FadeOut(cross), FadeOut(pores), run_time=0.5)
        own_l = label("its own membrane", GREEN, 26).move_to([-2.4, -3.05, 0])
        own_r = label("its own membrane", GREEN, 26).move_to([2.4, -3.05, 0])
        a_l = Arrow([-1.2, -2.65, 0], [-0.45, -2.1, 0], buff=0, color=GREEN, stroke_width=4, tip_length=0.2)
        a_r = Arrow([1.2, -2.65, 0], [0.45, -2.1, 0], buff=0, color=GREEN, stroke_width=4, tip_length=0.2)
        self.at("keeps its own membrane")
        self.play(FadeIn(own_l), FadeIn(own_r), GrowArrow(a_l), GrowArrow(a_r),
                  Indicate(VGroup(el, er), color=GREEN, scale_factor=1.0), run_time=1.2)
        self.finish()


class S07End(EndCard):
    LINE = "Each neuron keeps its own membrane, however closely it touches."
