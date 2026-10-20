"""Each stage changes the place  (Biochemistrypedia explainer, high school Biology: succession in Virginia)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  LIME   = weeds and grasses (horseweed, asters, broomsedge): the early plants
  GREEN  = pines
  ORANGE = oaks and hickories (hardwoods): the late plants
  YELLOW = sunlight (the sun and light arrows)
  SOIL   = soil (brown bar)
  BLUE   = a term being defined (community, succession, abiotic factors, climax community)
  RED    = disturbance (fire, flood, plowing, a reset)
  PURPLE = people mowing (first scene only)
  GREY   = bare rock, axes, outlines, neutral labels
Plants are simple schematic shapes (tufts, triangles, circles on sticks), not drawings of species.
Dots in the community boxes are an illustration, not counts. The only times on screen are the
lesson's own words for the published Piedmont old-field path: first years, about year 3, a few
decades, a century or more. No Glacier Bay figure and no data-table number is shown.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

LIME = "#B5D86A"
SOIL = "#A67C52"
ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
PINE = GREEN
HARD = ORANGE

GY = -1.3          # ground top (strip scenes)
XS = [-4.6, -1.55, 1.55, 4.6]
WOBBLE = [0.9, 1.0, 0.8, 1.0, 0.85, 0.95, 0.9, 1.0]


# ------------------------------------------------------------------------------------ helpers
def tufts(cx, base, n, h, color=LIME, gap=0.28, w=4):
    g = VGroup()
    for i in range(n):
        x = cx + (i - (n - 1) / 2) * gap
        tilt = 0.06 * (1 if i % 2 else -1)
        g.add(Line([x, base, 0], [x + tilt, base + h * WOBBLE[i % 8], 0], color=color, stroke_width=w))
    return g


def pine(cx, base, h, w, tr=0.25, color=PINE):
    trunk = Line([cx, base, 0], [cx, base + h * tr + 0.05, 0], color=color, stroke_width=5)
    can = Polygon([cx - w / 2, base + h * tr, 0], [cx + w / 2, base + h * tr, 0], [cx, base + h, 0],
                  stroke_color=color, stroke_width=3.5, fill_color=color, fill_opacity=0.28)
    return VGroup(trunk, can)


def oak(cx, base, h, r, color=HARD):
    trunk = Line([cx, base, 0], [cx, base + h, 0], color=color, stroke_width=5)
    crown = Circle(radius=r, stroke_color=color, stroke_width=3.5, fill_color=color, fill_opacity=0.28)
    crown.move_to([cx, base + h + r * 0.55, 0])
    return VGroup(trunk, crown)


def ground(y, x0=-6.3, x1=6.3, h=0.3, color=SOIL):
    return Rectangle(width=x1 - x0, height=h, stroke_color=color, stroke_width=2.5, fill_color=color,
                     fill_opacity=0.5).move_to([(x0 + x1) / 2, y - h / 2, 0])


def lab2(a, b, ca=TEXT, cb=GREY, sa=24, sb=22, w=2.95):
    ta, tb = T(a, sa, ca), T(b, sb, cb)
    g = VGroup(ta, tb).arrange(DOWN, buff=0.1)
    return fit(g, max_w=w)


def col_plants(i, lime_h=(0.5, 1.2)):
    x, b = XS[i], GY
    if i == 0:
        return tufts(x, b, 6, 0.8)
    if i == 1:
        return tufts(x, b, 8, 2.0, w=3.5)
    if i == 2:
        return VGroup(pine(x - 0.8, b, 3.0, 1.45), pine(x + 0.8, b, 2.7, 1.3))
    return VGroup(oak(x - 0.8, b, 1.3, 0.8), oak(x + 0.8, b, 1.1, 0.75))


COLLAB = [("weeds", "first years"), ("broomsedge", "about year 3"), ("young pines", "a few decades"),
          ("oaks and hickories", "a century or more")]
COLCOL = [LIME, LIME, PINE, HARD]


def col_label(i):
    g = lab2(*COLLAB[i], ca=COLCOL[i])
    return g.move_to([XS[i], -2.2, 0])


def sun(x=-5.9, y=2.8, r=0.3):
    c = Circle(radius=r, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW, fill_opacity=0.9).move_to([x, y, 0])
    rays = VGroup(*[Line(c.get_center() + r * 1.35 * np.array([np.cos(a), np.sin(a), 0]),
                         c.get_center() + r * 1.9 * np.array([np.cos(a), np.sin(a), 0]), color=YELLOW, stroke_width=4)
                    for a in np.linspace(0, 2 * np.pi, 8, endpoint=False)])
    return VGroup(c, rays)


def larrow(x, y0, y1, w=4, op=1.0):
    a = Arrow([x, y0, 0], [x, y1, 0], color=YELLOW, stroke_width=w, buff=0, tip_length=0.2,
              max_tip_length_to_length_ratio=0.5)
    a.set_opacity(op)
    return a


def arr(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=w, tip_length=0.22, max_tip_length_to_length_ratio=0.4)


def time_arrow(y=-3.15):
    a = arr([-6.1, y, 0], [6.1, y, 0], GREY, 4)
    t = T("years after mowing stops", 22, GREY).move_to([0, y - 0.35, 0])
    return VGroup(a, t)


def dots_box(cx, cy, mix, w=3.5, h=2.9, seed=0):
    """mix = (n_lime, n_green, n_orange). Dots are an illustration, not counts."""
    box = RoundedRectangle(corner_radius=0.15, width=w, height=h, stroke_color=GREY, stroke_width=3)
    box.move_to([cx, cy, 0])
    rng = np.random.RandomState(seed)
    cols = [LIME] * mix[0] + [PINE] * mix[1] + [HARD] * mix[2]
    n = len(cols)
    cells = [(i, j) for i in range(4) for j in range(3)]
    rng.shuffle(cells)
    rng.shuffle(cols)
    dots = VGroup()
    for (i, j), c in zip(cells[:n], cols):
        p = [cx - w / 2 + 0.4 + i * (w - 0.8) / 3 + rng.uniform(-0.07, 0.07),
             cy - h / 2 + 0.4 + j * (h - 0.8) / 2 + rng.uniform(-0.07, 0.07), 0]
        dots.add(Circle(radius=0.18, stroke_color=c, stroke_width=2, fill_color=c, fill_opacity=0.85).move_to(p))
    out = VGroup(box, dots)
    out.cols = cols[:n]
    return out


def strip(upto=4, labels=True, sunlight=False):
    g = VGroup(ground(GY))
    for i in range(upto):
        g.add(col_plants(i))
        if labels:
            g.add(col_label(i))
    return g


class S00Title(TitleCard):
    LESSON = "Succession in Virginia"
    TITLE = "Each stage changes the place"


# ------------------------------------------------------------------------------------ 1
class S01Stop(SpokenScene):
    """A mowed field, then a timeline from a few years to a century or more, with the question."""

    def construct(self):
        g = ground(GY)
        mown = tufts(-4.6, GY, 7, 0.25, color=LIME, gap=0.3, w=3)
        mown_l = lab2("mowed field", "kept short by people", ca=PURPLE, w=3.2).move_to([-4.6, -2.2, 0])
        self.add(g)
        self.at("stop mowing")
        self.play(FadeIn(mown, lag_ratio=0.1), FadeIn(mown_l), run_time=0.8)
        tl = time_arrow()
        self.play(Create(tl[0]), FadeIn(tl[1]), run_time=0.7)
        self.at("nobody plants anything")
        stop = chip("mowing stops", PURPLE, size=26).move_to([-4.6, 0.2, 0])
        self.play(FadeIn(stop, shift=DOWN * 0.1), run_time=0.5)
        self.at("seeds blow in")
        seeds = VGroup(*[Circle(radius=0.07, stroke_width=0, fill_color=LIME, fill_opacity=1).move_to([x, 1.0 + 0.3 * (k % 2), 0])
                         for k, x in enumerate([-1.9, -1.4, -0.9, -0.4, 0.1, 0.6])])
        sl = T("seeds", 24, LIME).move_to([-0.9, 1.9, 0])
        self.play(FadeIn(seeds), FadeIn(sl), run_time=0.4)
        self.play(*[s.animate.move_to([s.get_x(), GY - 0.12 * (k % 3) - 0.04, 0]) for k, s in enumerate(seeds)],
                  run_time=0.9)
        self.at("within a few years")
        few = VGroup(tufts(XS[1], GY, 8, 2.0, w=3.5), pine(XS[1] + 1.32, GY, 1.3, 0.75))
        few_l = lab2("a few years", "broomsedge, blackberry, small pines", ca=LIME, w=4.4).move_to([XS[1], -2.2, 0])
        self.play(FadeOut(mown), FadeOut(mown_l), FadeOut(stop), FadeOut(sl), FadeOut(seeds), FadeIn(few, shift=UP * 0.2),
                  FadeIn(few_l), run_time=0.9)
        self.at("after a century or more")
        qb = RoundedRectangle(corner_radius=0.15, width=3.0, height=3.2, stroke_color=GREY, stroke_width=3, stroke_opacity=0.8)
        qb.move_to([XS[3], GY + 1.6, 0])
        q = T("?", 80, YELLOW, weight=BOLD).move_to(qb)
        far = T("a century or more", 24, GREY).move_to([XS[3], -2.2, 0])
        self.play(Create(qb), FadeIn(q), FadeIn(far), run_time=0.7)
        self.at("oaks and hickories")
        oaks = col_plants(3)
        self.play(FadeOut(q), FadeOut(qb), FadeIn(oaks, shift=UP * 0.2), run_time=0.9)
        far2 = T("oaks and hickories", 24, HARD).move_to([XS[3], -2.2, 0])
        self.play(Transform(far, far2), run_time=0.4)
        self.at("what happens to a field")
        ques = T("What happens to a field after people or fire leave it alone?", 32, font=TITLE_FONT)
        fit(ques, max_w=12.2)
        ques.move_to([0, 3.0, 0])
        self.play(Write(ques), run_time=1.6)
        self.finish()


# ------------------------------------------------------------------------------------ 2
class S02Name(SpokenScene):
    """Community boxes along a time arrow: the mix of plants moves from early to late."""

    def construct(self):
        title = T("ecological succession", 44, BLUE, font=TITLE_FONT).move_to([0, 2.9, 0])
        self.at("this change has a name")
        self.play(Write(title), run_time=1.2)
        b1 = dots_box(-4.45, 0.2, (9, 3, 0), seed=3)
        b2 = dots_box(0.0, 0.2, (5, 5, 2), seed=5)
        b3 = dots_box(4.45, 0.2, (2, 3, 7), seed=8)
        self.at("a community is")
        self.play(Create(b1[0]), FadeIn(b1[1], lag_ratio=0.08), run_time=1.0)
        cl = T("community", 28, BLUE).next_to(b1, UP, buff=0.2)
        cl2 = T("all the species in one area", 24, GREY).next_to(b1, DOWN, buff=0.25)
        self.play(FadeIn(cl), FadeIn(cl2), run_time=0.5)
        self.at("succession is the change")
        a1 = arr([-2.6, 0.2, 0], [-1.95, 0.2, 0], GREY, 5)
        a2 = arr([1.95, 0.2, 0], [2.6, 0.2, 0], GREY, 5)
        tl = T("years to centuries", 24, GREY).move_to([0, -1.9, 0])
        self.play(GrowArrow(a1), Create(b2[0]), FadeIn(b2[1], lag_ratio=0.08), run_time=1.0)
        self.play(GrowArrow(a2), Create(b3[0]), FadeIn(b3[1], lag_ratio=0.08), FadeIn(tl), run_time=1.0)
        self.at("predictable in a general way")
        gen = T("predictable in a general way", 30, TEXT).move_to([0, -2.75, 0])
        self.play(FadeIn(gen), run_time=0.5)
        self.at("come early")
        e = T("early", 26, LIME).next_to(b1, DOWN, buff=0.25)
        self.play(FadeOut(cl2), FadeIn(e), *[Indicate(d, color=LIME, scale_factor=1.35) for d, c in zip(b1[1], b1.cols) if c == LIME][:4],
                  run_time=0.9)
        self.at("others late")
        l = T("late", 26, HARD).next_to(b3, DOWN, buff=0.25)
        self.play(FadeIn(l), *[Indicate(d, color=HARD, scale_factor=1.35) for d, c in zip(b3[1], b3.cols) if c == HARD][:4],
                  run_time=0.9)
        note = T("dots: an illustration, not counts", 22, GREY).move_to([0, -3.4, 0])
        self.play(FadeIn(note), run_time=0.4)
        self.finish()


# ------------------------------------------------------------------------------------ 3
class S03Start(SpokenScene):
    """Disturbance hits a community; soil stays (secondary) or bare rock (primary)."""

    def construct(self):
        box = dots_box(0.0, 2.35, (4, 4, 4), w=3.4, h=1.5, seed=11)
        cl = T("community", 24, BLUE).next_to(box, LEFT, buff=0.3)
        self.play(Create(box[0]), FadeIn(box[1]), FadeIn(cl), run_time=0.8)
        self.at("starts after a disturbance")
        dch = chip("disturbance", RED, size=28).move_to([4.9, 2.35, 0])
        da = arr(dch.get_left() + LEFT * 0.0, box.get_right() + RIGHT * 0.05, RED, 6)
        self.play(FadeIn(dch), GrowArrow(da), run_time=0.7)
        keep = VGroup(*list(box[1])[:3])
        gone = VGroup(*list(box[1])[3:])
        self.play(FadeOut(gone), box[0].animate.set_stroke(RED), run_time=0.7)
        self.at("a disturbance is an event")
        ex = T("fire, flood, plowing", 26, RED).move_to([4.9, 1.45, 0])
        self.play(FadeIn(ex), run_time=0.5)
        self.at("if the soil stays")
        s_g = ground(-0.2, -6.2, -0.5, 0.45)
        s_seed = VGroup(*[Circle(radius=0.07, stroke_width=0, fill_color=LIME, fill_opacity=1).move_to([x, -0.35, 0])
                          for x in [-5.4, -4.5, -3.6, -2.7, -1.8]])
        s_t = T("soil stays", 26, SOIL).move_to([-3.35, 0.35, 0])
        s_a = arr([-1.3, 1.9, 0], [-3.0, 0.75, 0], GREY, 4)
        s_n = chip("secondary succession", BLUE, size=26).move_to([-3.35, -1.1, 0])
        self.play(FadeOut(da), FadeOut(dch), FadeOut(ex), GrowArrow(s_a), FadeIn(s_g), FadeIn(s_t), FadeIn(s_seed), run_time=0.9)
        self.play(FadeIn(s_n), run_time=0.5)
        self.at("on bare rock")
        r_g = ground(-0.2, 0.5, 6.2, 0.45, GREY)
        r_t = T("bare rock, no soil", 26, GREY).move_to([3.35, 0.35, 0])
        r_a = arr([1.3, 1.9, 0], [3.0, 0.75, 0], GREY, 4)
        self.play(GrowArrow(r_a), FadeIn(r_g), FadeIn(r_t), run_time=0.9)
        self.at("that is primary succession")
        r_n = chip("primary succession", BLUE, size=26).move_to([3.35, -1.1, 0])
        self.play(FadeIn(r_n), run_time=0.5)
        self.at("lichens and mosses")
        blobs = VGroup(*[Ellipse(width=0.42, height=0.2, stroke_color=LIME, stroke_width=2, fill_color=LIME, fill_opacity=0.5)
                         .move_to([x, -0.1 + 0.0, 0]) for x in [2.2, 3.0, 3.8, 4.5]])
        bl = T("lichens and mosses first", 24, LIME).move_to([3.35, -1.75, 0])
        self.play(FadeIn(blobs, lag_ratio=0.2), FadeIn(bl), run_time=0.9)
        self.at("usually reaches forest")
        fb = Rectangle(width=2.4, height=0.28, stroke_width=0, fill_color=GREEN, fill_opacity=0.7).move_to([-4.15, -2.8, 0])
        rb = Rectangle(width=5.2, height=0.28, stroke_width=0, fill_color=GREY, fill_opacity=0.7).move_to([3.6, -2.8, 0])
        ft = T("usually faster", 24, GREEN).next_to(fb, DOWN, buff=0.18)
        rt = T("usually slower", 24, GREY).next_to(rb, DOWN, buff=0.18).align_to(rb, LEFT)
        self.play(GrowFromEdge(fb, LEFT), GrowFromEdge(rb, LEFT), FadeIn(ft), FadeIn(rt), run_time=1.3)
        self.finish()


# ------------------------------------------------------------------------------------ 4
class S04Path(SpokenScene):
    """The published Piedmont old-field path in full sun: weeds, broomsedge, young pines."""

    def construct(self):
        g = ground(GY)
        tl = time_arrow()
        sn = sun()
        sl = T("full sun", 24, YELLOW).next_to(sn, DOWN, buff=0.15)
        self.at("here is the usual path")
        self.play(FadeIn(g), Create(tl[0]), FadeIn(tl[1]), FadeIn(sn), FadeIn(sl), run_time=1.0)
        self.at("in the first years")
        p0 = col_plants(0)
        l0 = col_label(0)
        a0 = larrow(XS[0], 2.9, -0.3)
        self.play(FadeIn(p0, shift=UP * 0.15), FadeIn(l0), GrowArrow(a0), run_time=0.8)
        self.at("weeds such as")
        self.play(Indicate(p0, color=LIME, scale_factor=1.2), run_time=0.8)
        self.at("by about the third year")
        p1 = col_plants(1)
        l1 = col_label(1)
        a1 = larrow(XS[1], 2.9, 0.9)
        self.play(FadeIn(p1, shift=UP * 0.2), FadeIn(l1), GrowArrow(a1), run_time=0.9)
        self.at("a tall grass")
        self.play(Indicate(p1, color=LIME, scale_factor=1.12), run_time=0.8)
        self.at("pines grow fast")
        p2 = col_plants(2)
        l2 = col_label(2)
        a2 = larrow(XS[2], 2.9, 1.9)
        self.play(FadeIn(p2, shift=UP * 0.3), FadeIn(l2), GrowArrow(a2), run_time=1.0)
        self.at("young pine forest")
        self.play(Indicate(p2, color=PINE, scale_factor=1.1), run_time=0.9)
        self.finish()


# ------------------------------------------------------------------------------------ 5
class S05Shade(SpokenScene):
    """Zoom on the pine stand: the canopy shades the ground, hardwoods cope, pines die, hardwoods fill in."""

    def construct(self):
        # carry over the last state of scene 4 in the same place
        g = ground(GY)
        tl = time_arrow()
        old = VGroup(g, tl, sun(), larrow(XS[0], 2.9, -0.3), larrow(XS[1], 2.9, 0.9), larrow(XS[2], 2.9, 1.9))
        old.add(*[col_plants(i) for i in range(3)], *[col_label(i) for i in range(3)])
        self.add(old)
        self.at("each stage changes")
        B = -2.0
        ground2 = ground(B)
        pines = VGroup(*[pine(x, B, 3.6, 2.5, tr=0.5) for x in [-3.9, -1.3, 1.3, 3.9]])
        sn = sun(-5.9, 2.3)
        sl = T("sunlight", 24, YELLOW).next_to(sn, DOWN, buff=0.15)
        self.play(FadeOut(old), run_time=0.5)
        self.play(FadeIn(ground2), FadeIn(pines, lag_ratio=0.1), FadeIn(sn), FadeIn(sl), run_time=1.0)
        self.at("abiotic factors")
        ab = chip("abiotic factors: light and soil", BLUE, size=28).move_to([0, 3.1, 0])
        self.play(FadeIn(ab, shift=DOWN * 0.1), run_time=0.6)
        self.at("a closed pine canopy")
        arrows = VGroup(*[larrow(x, 2.65, 1.75, 5) for x in [-3.9, -1.3, 1.3, 3.9]])
        shade = Rectangle(width=11.6, height=1.55, stroke_width=0, fill_color=GREY, fill_opacity=0.18).move_to([0, B + 0.78, 0])
        dim = VGroup(*[larrow(x, -0.35, -1.0, 3, 0.35) for x in [-2.6, 0, 2.6]])
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15), run_time=1.0)
        self.play(FadeIn(shade), FadeIn(dim), run_time=0.7)
        shl = T("shade", 26, GREY).move_to([-5.3, -1.3, 0])
        self.play(FadeIn(shl), run_time=0.3)
        self.at("pine seedlings grow poorly")
        seed = pine(-2.6, B, 0.45, 0.32, tr=0.3)
        sl1 = lab2("pine seedling", "grows poorly in shade", ca=PINE, cb=PINE, w=3.4).move_to([-2.6, -2.85, 0])
        self.play(FadeIn(seed, shift=UP * 0.1), FadeIn(sl1), run_time=0.7)
        self.play(seed.animate.scale(0.8, about_point=seed.get_bottom()), run_time=0.8)
        self.at("young hardwoods")
        sap = oak(2.6, B, 0.4, 0.22)
        sl2 = lab2("oak or hickory sapling", "copes better, grows slowly", ca=HARD, cb=HARD, w=3.8).move_to([2.6, -2.85, 0])
        self.play(FadeIn(sap, shift=UP * 0.1), FadeIn(sl2), run_time=0.7)
        self.at("as the old pines die")
        dead = [p.animate.set_opacity(0.15) for p in pines]
        self.play(*dead, FadeOut(arrows), FadeOut(dim), FadeOut(shade), FadeOut(shl), run_time=1.0)
        big = oak(2.6, B, 1.8, 0.9)
        o2 = oak(-1.3, B, 1.6, 0.85)
        o4 = oak(-4.0, B, 1.5, 0.8)
        fl = T("hardwoods fill the gaps", 30, HARD).move_to([0, -2.85, 0])
        self.play(FadeOut(sl2), FadeOut(sl1), FadeOut(pines), run_time=0.6)
        self.play(Transform(sap, big), GrowFromEdge(o2, DOWN), GrowFromEdge(o4, DOWN), FadeIn(fl), run_time=1.6)
        self.finish()


# ------------------------------------------------------------------------------------ 6
class S06Answer(SpokenScene):
    """Whole path again: each stage changes light and soil; climax community; a reset patch; the rule."""

    def construct(self):
        s = strip(4)
        tl = time_arrow()
        self.add(s, tl)
        q = T("Why do plants arrive in this order?", 32, font=TITLE_FONT).move_to([0, 3.35, 0])
        self.at("so why do plants arrive")
        self.play(Write(q), run_time=1.3)
        self.at("each stage changes light")
        ars = VGroup(*[arr([XS[i] + 0.7, 2.3, 0], [XS[i + 1] - 0.7, 2.3, 0], BLUE, 6) for i in range(3)])
        cl = T("light and soil change", 26, BLUE).move_to([0, 2.75, 0])
        self.play(LaggedStart(*[GrowArrow(a) for a in ars], lag_ratio=0.4), FadeIn(cl), run_time=1.4)
        self.at("favor the next plants")
        self.play(*[a.animate.set_color(GREEN) for a in ars], cl.animate.set_color(GREEN), run_time=0.7)
        fav = T("and favor the next plants", 26, GREEN).move_to([0, 2.75, 0])
        self.play(Transform(cl, fav), run_time=0.5)
        self.at("in most of virginia")
        box = RoundedRectangle(corner_radius=0.15, width=3.0, height=3.1, stroke_color=BLUE, stroke_width=3.5).move_to([XS[3], GY + 1.55, 0])
        self.play(FadeOut(ars), FadeOut(cl), Create(box), run_time=0.7)
        self.at("climax community")
        cc = T("climax community", 28, BLUE).move_to([XS[3], 2.15, 0])
        self.play(FadeIn(cc, shift=DOWN * 0.1), run_time=0.6)
        self.at("fire storms and people")
        oaks = s[-2]
        patch = VGroup(oaks[0])
        newt = tufts(XS[3] - 0.8, GY, 5, 0.8)
        rd = arr([XS[3] - 0.8, 1.95, 0], [XS[3] - 0.8, 1.0, 0], RED, 6)
        rl = T("disturbance", 26, RED).move_to([XS[3], 2.15, 0])
        self.play(FadeOut(cc), FadeIn(rl), GrowArrow(rd), run_time=0.7)
        self.play(FadeOut(oaks[0]), FadeOut(rd), FadeIn(newt, shift=UP * 0.1), run_time=0.8)
        self.at("path and timing vary")
        pt = T("the path and timing vary", 30, TEXT).move_to([-2.5, 2.6, 0])
        self.play(FadeIn(pt), run_time=0.6)
        self.at("changes the place")
        everything = Group(*self.mobjects)
        self.play(FadeOut(everything), run_time=0.8)
        rule = T("Each stage changes the place,", 42, font=TITLE_FONT)
        rule2 = T("and that favors the next plants.", 42, GREEN, font=TITLE_FONT)
        rr = VGroup(rule, rule2).arrange(DOWN, buff=0.35).move_to([0, 0.2, 0])
        fit(rr, max_w=12)
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=0.8)
        self.play(FadeIn(rule2, shift=UP * 0.15), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Each stage changes the place and favors the next plants."
