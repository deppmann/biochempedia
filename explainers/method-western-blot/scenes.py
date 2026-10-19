"""Gel electrophoresis, SDS-PAGE and the western blot: one protein out of thousands
(Biochemistrypedia methods film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the gel, the electrodes (the apparatus)
  GREY   = other proteins, membranes, structure, de-emphasised text
  YELLOW = the target protein and its band
  ORANGE = SDS and the negative charge it gives
  PURPLE = the primary antibody
  TEAL   = the second antibody and its enzyme
  WHITE  = the light or colour the enzyme makes
  GREEN  = the standard of known weights, and controls
  RED    = pitfalls and limits
  GOLD   = dates and the closing rule
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
WHITE_L = "#FFFFFF"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def lab(text, size=24, color=GREY, **kw):
    return T(text, size, color, **kw)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def minus(x, y, size=24, color=ORANGE):
    """A negative-charge badge: a small ring with a bar. size sets the ring radius."""
    r = size / 24 * 0.15
    ring = Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.15)
    bar_ = Line([-r * 0.55, 0, 0], [r * 0.55, 0, 0], color=color, stroke_width=4)
    return VGroup(ring, bar_).move_to([x, y, 0])


def bar(cx, cy, w, h, color, op=1.0, stroke=0):
    r = Rectangle(width=w, height=h, stroke_width=stroke, stroke_color=color, fill_color=color, fill_opacity=op)
    return r.move_to([cx, cy, 0])


def slab(cx, cy, w, h, nl, color=BLUE):
    """A gel as a slab with wells at the top. Returns (group, lane_xs, well_y)."""
    body = RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.12).move_to([cx, cy, 0])
    xs = [cx - w / 2 + w * (i + 0.5) / nl for i in range(nl)]
    wy = cy + h / 2 - 0.2
    wells = VGroup(*[Rectangle(width=w / nl * 0.62, height=0.14, stroke_color=color, stroke_width=2.5,
                               fill_color=BG, fill_opacity=1).move_to([x, wy, 0]) for x in xs])
    return VGroup(body, wells), xs, wy


def memb(cx, cy, w, h, nl=None, color=GREY):
    body = Rectangle(width=w, height=h, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.16)
    body.move_to([cx, cy, 0])
    xs = [cx - w / 2 + w * (i + 0.5) / nl for i in range(nl)] if nl else []
    return body, xs


def band(x, y, w, color=GREY, op=0.85, h=0.14):
    return bar(x, y, w, h, color, op)


def ab(x, y, color, s=1.0):
    """Antibody as a plain Y: arm tips at (x, y), stem going up. A labelled shape, not a structure."""
    tl = np.array([x - 0.28 * s, y, 0.0]); tr = np.array([x + 0.28 * s, y, 0.0])
    j = np.array([x, y + 0.5 * s, 0.0]); top = np.array([x, y + 1.0 * s, 0.0])
    g = VGroup(Line(tl, j, color=color, stroke_width=7), Line(tr, j, color=color, stroke_width=7),
               Line(j, top, color=color, stroke_width=7))
    for ln in g:
        ln.set_cap_style(CapStyleType.ROUND)
    g.tip = np.array([x, y, 0.0]); g.top = top
    return g


def title_at(text, x, y, size=26, color=TEXT):
    return T(text, size, color).move_to([x, y, 0])


def example_tag(text="example data, idealised", x=0.0, y=3.2, size=22):
    t = T(text, size, GREY)
    box = RoundedRectangle(corner_radius=0.1, width=t.width + 0.4, height=t.height + 0.28,
                           stroke_color=GREY, stroke_width=2).move_to(t)
    g = VGroup(box, t).move_to([x, y, 0])
    return g


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Methods library"
    TITLE = "One Protein Out of Thousands"


def electrodes(cx, cy, w, h):
    etop = bar(cx, cy + h / 2 + 0.3, w + 0.3, 0.1, BLUE, 1)
    ebot = bar(cx, cy - h / 2 - 0.3, w + 0.3, 0.1, BLUE, 1)
    emin = T("−", 44, ORANGE, weight=BOLD).move_to([cx - w / 2 - 0.5, cy + h / 2 + 0.3, 0])
    eplu = T("+", 44, TEXT, weight=BOLD).move_to([cx - w / 2 - 0.5, cy - h / 2 - 0.3, 0])
    return VGroup(etop, ebot, emin, eplu)


# ---------------------------------------------------------------------------------------------
class S01Problem(SpokenScene):
    """A mixture of thousands of proteins; one is wanted; an antibody cannot find it until the mixture is sorted."""

    def construct(self):
        rng = np.random.RandomState(5)
        tube = RoundedRectangle(corner_radius=0.35, width=4.4, height=5.6, stroke_color=GREY, stroke_width=4,
                                fill_color=GREY, fill_opacity=0.06).move_to([-3.6, -0.3, 0])
        tlab = lab("cell extract", 30, GREY).move_to([-3.6, 2.9, 0])
        dots = VGroup()
        pts = []
        while len(pts) < 70:
            p = (rng.uniform(-5.5, -1.7), rng.uniform(-2.9, 2.1))
            if all((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 > 0.16 for q in pts) and not (abs(p[0] + 3.6) < 0.4 and abs(p[1] + 0.2) < 0.4):
                pts.append(p)
        for i, p in enumerate(pts):
            r = rng.uniform(0.08, 0.2)
            if i % 3 == 0:
                m = Square(side_length=r * 2, stroke_width=0, fill_color=GREY, fill_opacity=0.7)
            elif i % 3 == 1:
                m = Triangle(stroke_width=0, fill_color=GREY, fill_opacity=0.7).scale(r * 1.2)
            else:
                m = Circle(radius=r, stroke_width=0, fill_color=GREY, fill_opacity=0.7)
            dots.add(m.move_to([p[0], p[1], 0]))
        target = Circle(radius=0.24, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to([-3.6, -0.2, 0])
        ring = Circle(radius=0.55, stroke_color=YELLOW, stroke_width=3).move_to(target)

        self.at("A cell extract")
        self.play(FadeIn(tube), FadeIn(tlab), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.02), FadeIn(target), run_time=1.6)

        c1 = chip("Is the protein there?", YELLOW, 32).move_to([3.3, 2.3, 0])
        c2 = chip("In which form?", YELLOW, 32).move_to([3.3, 1.0, 0])
        c3 = chip("How big is it?", YELLOW, 32).move_to([3.3, -0.3, 0])
        self.at("Is one protein there")
        self.play(Create(ring), FadeIn(c1, shift=LEFT * 0.2), run_time=0.7)
        self.at("in which form")
        self.play(FadeIn(c2, shift=LEFT * 0.2), run_time=0.6)
        self.at("And how big")
        self.play(FadeIn(c3, shift=LEFT * 0.2), run_time=0.6)

        self.at("An antibody binds")
        a = ab(-0.2, -2.7, PURPLE, 1.6)
        alab = lab("antibody: binds one protein", 26, PURPLE).move_to([3.3, -1.5, 0])
        self.play(FadeIn(a, shift=UP * 0.3), FadeIn(alab), run_time=0.7)
        self.at("cannot show size")
        q = T("?", 72, RED, weight=BOLD).move_to([-0.2, -0.45, 0])
        nofind = lab("cannot show size or form\nin a mixture", 26, RED, line_spacing=0.8).move_to([3.6, -2.5, 0])
        self.play(FadeIn(q, scale=1.3), FadeIn(nofind), run_time=0.8)

        self.at("The mixture must be sorted")
        self.play(FadeOut(VGroup(c1, c2, c3, alab, nofind, q, ring)), run_time=0.5)
        s1 = chip("1  sort the mixture", BLUE, 36).move_to([3.3, 1.8, 0])
        s2 = chip("2  hold the protein still", BLUE, 36).move_to([3.3, 0.4, 0])
        self.play(FadeIn(s1, shift=LEFT * 0.2), run_time=0.6)
        self.at("and the protein held still")
        self.play(FadeIn(s2, shift=LEFT * 0.2), run_time=0.6)

        self.at("Western blotting detects")
        self.play(FadeOut(VGroup(s1, s2)), FadeOut(a), run_time=0.4)
        wb = chip("western blot", BLUE, 48).move_to([3.3, 1.5, 0])
        wb2 = lab("detects selected proteins", 32, TEXT).move_to([3.3, 0.3, 0])
        wb3 = lab("in a mixture", 32, TEXT).move_to([3.3, -0.4, 0])
        self.play(FadeIn(wb, scale=0.9), run_time=0.5)
        self.play(FadeIn(wb2), FadeIn(wb3), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Charge(SpokenScene):
    """DNA runs to the + electrode in agarose; SDS gives proteins charge in proportion to length."""

    def construct(self):
        cx, cy, w, h = -3.6, -0.1, 3.8, 4.5
        g, xs, wy = slab(cx, cy, w, h, 3)
        el = electrodes(cx, cy, w, h)
        ttl = lab("DNA in an agarose gel", 28, TEXT).move_to([cx, 3.2, 0])

        self.at("Sorting starts")
        self.play(FadeIn(g), FadeIn(el), FadeIn(ttl), run_time=0.9)

        sizes = [0.8, 0.54, 0.3]
        frag, finals, mins = [], [], VGroup()
        final_y = [wy - 1.2, wy - 2.0, wy - 2.9]
        for x in xs:
            for k, s_ in enumerate(sizes):
                f = bar(x, wy - 0.05 - 0.12 * k, s_, 0.1, TEXT, 0.95)
                frag.append(f)
                finals.append((f, x, final_y[k]))
        self.at("DNA has a negatively")
        self.play(*[FadeIn(f) for f in frag], run_time=0.6)
        for x in xs:
            mins.add(minus(x - 0.6, wy - 0.45, 20), minus(x + 0.6, wy - 0.45, 20))
        lbl1 = lab("negatively charged backbone", 24, ORANGE).move_to([cx, cy + h / 2 + 0.85, 0])
        self.play(FadeIn(mins), FadeOut(ttl), FadeIn(lbl1), run_time=0.5)
        self.at("runs toward the positive")
        self.play(FadeOut(mins), FadeOut(lbl1), FadeIn(ttl), *[f.animate.move_to([x, y, 0]) for f, x, y in finals],
                  run_time=2.2, rate_func=smooth)
        self.at("Agarose sorts fragments")
        srt = lab("sorted by size", 26, TEXT).move_to([cx, cy - h / 2 - 0.85, 0])
        self.play(FadeIn(srt), run_time=0.4)

        self.at("For proteins")
        left = VGroup(g, el, ttl, srt, *frag)
        self.play(left.animate.set_opacity(0.2), run_time=0.7)
        blob = Circle(radius=0.6, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.35).move_to([1.6, 1.3, 0])
        blab = lab("protein", 24, GREY).next_to(blob, DOWN, buff=0.15)
        self.play(FadeIn(blob), FadeIn(blab), run_time=0.6)
        self.at("heated in")
        sds = chip("SDS: a detergent", ORANGE, 30).move_to([4.2, 3.0, 0])
        heat = lab("heat", 28, TEXT).move_to([1.6, 2.4, 0])
        self.play(FadeIn(sds, shift=DOWN * 0.2), FadeIn(heat), run_time=0.6)
        self.at("It unfolds each protein")
        xsz = np.linspace(1.0, 5.2, 16)
        line = VMobject()
        line.set_points_as_corners([np.array([x, 1.3 + (0.3 if i % 2 else -0.3), 0.0]) for i, x in enumerate(xsz)])
        line.set_stroke(GREY, 6)
        self.play(FadeOut(heat), FadeOut(blab), Transform(blob, line), run_time=1.2)
        self.at("coats it with negative charge")
        ms = VGroup(*[minus(1.1 + 0.55 * i, 2.15, 24) for i in range(8)])
        self.play(LaggedStart(*[FadeIn(m, scale=1.6) for m in ms], lag_ratio=0.12), run_time=1.2)
        self.at("roughly in proportion")
        self.play(FadeOut(VGroup(blob, ms, sds)), run_time=0.4)
        short = VMobject(); short.set_points_as_corners([np.array([x, 1.1 + (0.22 if i % 2 else -0.22), 0.0]) for i, x in enumerate(np.linspace(1.0, 2.6, 7))])
        short.set_stroke(GREY, 6)
        longp = VMobject(); longp.set_points_as_corners([np.array([x, -0.7 + (0.22 if i % 2 else -0.22), 0.0]) for i, x in enumerate(np.linspace(1.0, 5.8, 21))])
        longp.set_stroke(GREY, 6)
        sm = VGroup(*[minus(1.1 + 0.55 * i, 1.75, 24) for i in range(3)])
        lm = VGroup(*[minus(1.1 + 0.55 * i, -0.05, 24) for i in range(9)])
        sl = lab("short: less charge", 26, TEXT).move_to([4.5, 1.25, 0])
        ll = lab("long: more charge", 26, TEXT).move_to([3.5, -1.3, 0])
        self.play(Create(short), FadeIn(sm), FadeIn(sl), run_time=0.8)
        self.play(Create(longp), FadeIn(lm), FadeIn(ll), run_time=1.0)
        self.at("So charge scales with weight")
        cw = chip("charge scales with weight", ORANGE, 30).move_to([3.5, -2.3, 0])
        self.play(FadeIn(cw, shift=UP * 0.2), run_time=0.6)
        self.at("separates by size")
        sz = lab("so the protein separates by size", 28, TEXT).move_to([3.5, -3.1, 0])
        self.play(FadeIn(sz), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
LANE_NL = 6


def make_gel(cx=0.0, cy=-0.15, w=8.0, h=4.6):
    g, xs, wy = slab(cx, cy, w, h, LANE_NL)
    lane_w = w / LANE_NL
    bw = lane_w * 0.66
    ladder_y = [1.55, 1.15, 0.75, 0.38, -0.1, -0.75, -1.55]
    grey_y = [1.35, 0.85, -0.5, -1.25, -1.95]
    target_y = 0.2
    bands = VGroup()
    start = []
    for i, x in enumerate(xs):
        if i in (0, LANE_NL - 1):
            for y in ladder_y:
                b = band(x, wy - 0.12, bw, GREEN, 0.9)
                bands.add(b); start.append((b, x, y))
        else:
            for j, y in enumerate(grey_y):
                if (i + j) % 4 == 3:
                    continue
                b = band(x, wy - 0.12, bw, GREY, 0.7, 0.13)
                bands.add(b); start.append((b, x, y + 0.04 * (i - 2)))
            t = band(x, wy - 0.12, bw, YELLOW, 1.0, 0.15)
            bands.add(t); start.append((t, x, target_y))
    return g, xs, wy, bands, start, bw


class S03Run(SpokenScene):
    """Bands run to different depths by size; the standard turns position into size; transfer to a membrane."""

    def construct(self):
        cx, cy, w, h = 0.0, -0.15, 8.0, 4.6
        g, xs, wy, bands, start, bw = make_gel(cx, cy, w, h)
        el = electrodes(cx, cy, w, h)
        ttl = lab("polyacrylamide gel", 28, TEXT).move_to([cx, 3.2, 0])

        self.at("Load the proteins")
        self.play(FadeIn(g), FadeIn(el), FadeIn(ttl), run_time=0.6)
        self.play(FadeIn(bands), run_time=0.4)
        self.play(*[b.animate.move_to([x, y, 0]) for b, x, y in start], run_time=2.2, rate_func=smooth)
        self.at("Small proteins travel farther")
        big = lab("large", 28, GREY).move_to([5.3, 1.4, 0])
        small = lab("small", 28, GREY).move_to([5.3, -1.9, 0])
        a = arr([5.3, 0.9, 0], [5.3, -1.4, 0], YELLOW, 5)
        self.play(FadeIn(big), FadeIn(small), GrowArrow(a), run_time=0.8)

        self.at("A standard of proteins")
        boxes = VGroup(*[Rectangle(width=w / LANE_NL * 0.9, height=h - 0.5, stroke_color=GREEN, stroke_width=3).move_to([xs[i], cy - 0.1, 0]) for i in (0, LANE_NL - 1)])
        std = lab("standard: proteins of known weight", 26, GREEN).move_to([0, -3.4, 0])
        self.play(FadeOut(VGroup(big, small, a)), Create(boxes), FadeIn(std), run_time=0.8)
        self.at("turns band position into size")
        ty = 0.2
        ln = DashedLine([xs[0], ty, 0], [xs[-1], ty, 0], color=YELLOW, stroke_width=3)
        szl = chip("position gives size", YELLOW, 28).move_to([0, 3.25, 0])
        self.play(Create(ln), FadeOut(ttl), FadeIn(szl), run_time=1.0)

        self.at("Then the sorted proteins")
        self.play(FadeOut(VGroup(boxes, std, ln, szl, el)), run_time=0.4)
        gel = VGroup(g, bands)
        sc = 0.68
        gx, mx = -3.4, 3.4
        self.play(gel.animate.scale(sc).move_to([gx, cy, 0]), run_time=0.9)
        mem2, _ = memb(mx, cy, w * sc, h * sc, LANE_NL)
        mlab = lab("membrane", 28, GREY).move_to([mx, cy + h * sc / 2 + 0.45, 0])
        glab = lab("gel", 28, BLUE).move_to([gx, cy + h * sc / 2 + 0.45, 0])
        self.play(FadeIn(mem2), FadeIn(mlab), FadeIn(glab), run_time=0.5)
        self.at("electrophoretic transfer")
        copy = bands.copy()
        ar = arr([-0.5, cy, 0], [0.5, cy, 0], BLUE, 6)
        tl = lab("electrophoretic\ntransfer", 26, BLUE, line_spacing=0.8).move_to([0, cy + 2.2, 0])
        self.play(GrowArrow(ar), FadeIn(tl), run_time=0.5)
        copy.shift(RIGHT * (mx - gx))
        self.play(FadeIn(copy), run_time=1.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Probe(SpokenScene):
    """Block the membrane; primary antibody on the target; wash; secondary antibodies carry an enzyme and make light."""

    def construct(self):
        ym = -2.7
        memrane = Rectangle(width=12.0, height=0.6, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.2).move_to([0, ym, 0])
        mlab = lab("membrane", 24, GREY).move_to([-5.2, ym - 0.7, 0])
        xs = [-5.2, -4.0, -2.8, -1.6, -0.4, 0.5, 1.7, 2.9, 4.1, 5.3]
        bumps = VGroup()
        bh = 0.5
        for x in xs:
            col = YELLOW if abs(x - 0.5) < 1e-6 else GREY
            b = RoundedRectangle(corner_radius=0.2, width=0.6, height=bh, stroke_width=0, fill_color=col, fill_opacity=1.0 if col == YELLOW else 0.7)
            b.move_to([x, ym + 0.3 + bh / 2, 0])
            bumps.add(b)
        tx = 0.5
        ttop = ym + 0.3 + bh
        stage = VGroup(memrane, bumps, mlab)
        stage.shift(UP * 2.2)
        self.play(FadeIn(stage), run_time=0.6)

        self.at("Leftover binding sites")
        blocks = VGroup()
        for x in np.arange(-5.7, 5.8, 0.2):
            if any(abs(x - bx) < 0.4 for bx in xs):
                continue
            blocks.add(Square(side_length=0.16, stroke_width=0, fill_color=TEXT, fill_opacity=0.65).move_to([x, ym + 0.3 + 0.1, 0]))
        blocks.shift(UP * 2.2)
        stage.add(blocks)
        blab = lab("blocking protein covers leftover sites", 32, TEXT).move_to([-0.2, ym + 1.7 + 2.2 + 0.3, 0])
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.3) for b in blocks], lag_ratio=0.03), FadeIn(blab), run_time=2.0)

        self.at("A primary antibody")
        self.play(FadeOut(blab), stage.animate.shift(DOWN * 2.2), run_time=0.8)
        s = 2.0
        prim = ab(tx, ttop + 0.02, PURPLE, s)
        prim.shift(UP * 2.0)
        floaters = VGroup(ab(-4.6, -0.9, PURPLE, 1.5), ab(-3.1, -0.2, PURPLE, 1.5), ab(-1.7, -0.8, PURPLE, 1.5))
        plab = lab("primary antibody", 26, PURPLE).move_to([4.2, -0.5, 0])
        self.play(FadeIn(floaters, shift=DOWN * 0.3), FadeIn(prim), run_time=0.7)
        self.play(prim.animate.shift(DOWN * 2.0), run_time=1.0)
        self.play(FadeIn(plab), run_time=0.4)
        self.at("Washing removes")
        wash = lab("wash", 32, BLUE).move_to([-3.1, 2.3, 0])
        self.play(FadeIn(wash), floaters.animate.shift(UP * 1.6).set_opacity(0.0), run_time=1.3)
        self.play(FadeOut(wash), run_time=0.3)

        self.at("A second antibody")
        s2 = 1.5
        stop = np.array([tx, ttop + s + 0.02, 0.0])
        sec = ab(stop[0], stop[1], TEAL, s2)
        sec.shift(UP * 1.4)
        self.play(FadeIn(sec), run_time=0.5)
        self.play(sec.animate.shift(DOWN * 1.4), run_time=0.8)
        slab_ = lab("second antibody", 26, TEAL).move_to([4.2, 0.8, 0])
        self.play(FadeIn(slab_), run_time=0.4)
        self.at("It carries an enzyme")
        enz = Square(side_length=0.38, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.85)
        enz.move_to(np.array([stop[0], stop[1] + s2 + 0.25, 0.0]))
        self.play(FadeIn(enz, scale=0.5), run_time=0.5)
        elab = lab("enzyme", 26, TEAL).move_to([0.5, 3.35, 0])
        self.play(FadeIn(elab), run_time=0.4)
        self.at("makes light or")
        cen = enz.get_center()
        rays = VGroup()
        for k in range(8):
            ang = k * PI / 4
            d = np.array([np.cos(ang), np.sin(ang), 0.0])
            rays.add(Line(cen + d * 0.36, cen + d * 0.66, color=WHITE_L, stroke_width=4))
        halo = Circle(radius=0.6, stroke_width=0, fill_color=WHITE_L, fill_opacity=0.18).move_to(cen)
        glow = RoundedRectangle(corner_radius=0.26, width=0.95, height=0.78, stroke_color=WHITE_L, stroke_width=4, fill_opacity=0).move_to(bumps[5])
        self.play(FadeIn(rays, scale=0.7), FadeIn(halo), Create(glow), FadeOut(elab), run_time=0.8)
        self.at("Several can bind")
        extra = VGroup(); extra_e = VGroup()
        for ang in (-50, 50):
            sx = ab(stop[0], stop[1], TEAL, s2)
            sx.rotate(ang * DEGREES, about_point=stop)
            e2 = Square(side_length=0.38, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.85)
            e2.move_to(stop + np.array([-np.sin(ang * DEGREES) * (s2 + 0.25), np.cos(ang * DEGREES) * (s2 + 0.25), 0.0]))
            extra.add(sx); extra_e.add(e2)
        self.play(FadeIn(extra), FadeIn(extra_e), run_time=0.8)
        self.at("which amplifies a weak signal")
        amp = lab("more enzymes:\nstronger signal", 30, WHITE_L, line_spacing=0.8).move_to([-3.6, 1.6, 0])
        rays2 = VGroup()
        for e2 in extra_e:
            c2 = e2.get_center()
            for k in range(6):
                ang = k * PI / 3 + 0.3
                d = np.array([np.cos(ang), np.sin(ang), 0.0])
                rays2.add(Line(c2 + d * 0.32, c2 + d * 0.56, color=WHITE_L, stroke_width=4))
        self.play(FadeIn(rays2), FadeIn(amp), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Read(SpokenScene):
    """Reading one made-up blot: position gives size, intensity gives amount; phospho-Akt then total Akt."""

    def construct(self):
        sx, sy, sw, sh = -2.9, 1.45, 6.0, 3.0
        m1, xs1 = memb(sx, sy, sw, sh, 3)
        lane_names = ["standard", "control", "insulin"]
        lnames = VGroup(*[lab(n, 26, GREEN if i == 0 else TEXT).move_to([xs1[i], sy + sh / 2 + 0.35, 0]) for i, n in enumerate(lane_names)])
        std_y = [sy + 1.15, sy + 0.7, sy + 0.1, sy - 0.45, sy - 1.05]
        std_b = VGroup(*[band(xs1[0], y, 0.9, GREEN, 0.9) for y in std_y])
        ty = sy + 0.0 + 0.05
        b_ctl = band(xs1[1], ty, 1.0, YELLOW, 0.35, 0.22)
        b_ins = band(xs1[2], ty, 1.0, YELLOW, 1.0, 0.22)

        self.at("The result is a membrane")
        self.play(FadeIn(m1), FadeIn(lnames), run_time=0.7)
        self.play(FadeIn(std_b), FadeIn(b_ctl), FadeIn(b_ins), run_time=0.7)
        tag = example_tag("example data, idealised", 3.6, 3.2, 24)
        self.play(FadeIn(tag), run_time=0.5)

        self.at("Read the band's position")
        ln = DashedLine([xs1[0] + 0.45, ty, 0], [xs1[2] - 0.5, ty, 0], color=YELLOW, stroke_width=3)
        pos = chip("position: size estimate", YELLOW, 28).move_to([3.6, 2.1, 0])
        self.play(Create(ln), FadeIn(pos), run_time=0.9)
        self.at("Its intensity gives amount")
        inten = chip("intensity: amount", YELLOW, 28).move_to([3.6, 1.1, 0])
        self.play(FadeOut(ln), FadeIn(inten), run_time=0.6)
        self.at("but uncalibrated intensity")
        nos = chip("not an absolute mass", RED, 28).move_to([3.6, 0.1, 0])
        self.play(FadeIn(nos, shift=UP * 0.15), run_time=0.6)

        self.at("Say insulin")
        self.play(FadeOut(VGroup(pos, inten, nos)), run_time=0.4)
        row1 = lab("antibody to one phosphorylated\nserine of Akt", 26, TEXT, line_spacing=0.8).move_to([3.6, 1.9, 0])
        self.play(FadeIn(row1), run_time=0.6)
        row1b = lab("insulin: darker band", 26, YELLOW).move_to([3.6, 0.9, 0])
        self.play(FadeIn(row1b), run_time=0.5)

        self.at("Blot the same samples")
        m2, xs2 = memb(sx, -1.8, sw, 1.5, 3)
        row2 = lab("total Akt, same samples", 26, TEXT).move_to([3.6, -1.1, 0])
        self.play(FadeIn(m2), FadeIn(row2), run_time=0.7)
        self.at("whether darker meant more phosphate")
        t_ctl = band(xs2[1], -1.8, 1.0, YELLOW, 0.8, 0.22)
        t_ins = band(xs2[2], -1.8, 1.0, YELLOW, 0.8, 0.22)
        ca = chip("total equal: more phosphate", GREEN, 26).move_to([3.6, -2.1, 0])
        il = lab("illustration", 22, GREY).move_to([3.6, -2.8, 0])
        self.play(FadeIn(t_ctl), FadeIn(t_ins), FadeIn(ca), FadeIn(il), run_time=0.7)
        self.at("or more protein")
        cb = chip("total darker too: more protein", RED, 26).move_to([3.6, -2.1, 0])
        self.play(FadeOut(ca), t_ctl.animate.set_fill(YELLOW, opacity=0.35), FadeIn(cb), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Pitfalls(SpokenScene):
    """Three pitfalls and their controls: identity, loading, linear range (all idealised)."""

    def construct(self):
        cxs = [-4.3, 0.0, 4.3]
        tag = example_tag("idealised examples", 0.0, -3.25, 22)
        t1 = lab("identity", 32, TEXT).move_to([cxs[0], 3.1, 0])
        t2 = lab("loading", 32, TEXT).move_to([cxs[1], 3.1, 0])
        t3 = lab("amount", 32, TEXT).move_to([cxs[2], 3.1, 0])
        self.play(FadeIn(tag), run_time=0.4)

        # column 1
        m, xs = memb(cxs[0], 1.3, 3.9, 3.0, 3)
        names = VGroup(*[lab(n, 22, GREEN if i else TEXT, line_spacing=0.8).move_to([xs[i], -0.8, 0]) for i, n in enumerate(["sample", "known\npositive", "no\ntarget"])])
        b0 = band(xs[0], 1.3, 1.0, YELLOW, 1.0, 0.22)
        b1 = band(xs[1], 1.3, 1.0, YELLOW, 1.0, 0.22)
        self.at("A band of the right size")
        idl1 = lab("idealised", 22, GREY).move_to([xs[2] - 0.2, 2.5, 0])
        self.play(FadeIn(t1), FadeIn(m), FadeIn(b0), FadeIn(names[0]), FadeIn(idl1), run_time=0.8)
        q = T("?", 64, RED, weight=BOLD).move_to([cxs[0], -1.7, 0])
        self.play(FadeIn(q, scale=1.3), run_time=0.4)
        self.at("Include a")
        self.play(FadeIn(b1), FadeIn(names[1]), FadeOut(q), run_time=0.7)
        self.at("and a sample lacking the target")
        self.play(FadeIn(names[2]), run_time=0.6)
        self.at("for example a knockout")
        ko = lab("knockout or knockdown", 24, GREEN).move_to([cxs[0], -1.85, 0])
        self.play(FadeIn(ko), run_time=0.6)

        # column 2
        m2, xs2 = memb(cxs[1], 1.95, 3.9, 1.6, 3)
        vals = [0.4, 0.95, 0.65]
        top = VGroup(*[band(xs2[i], 1.95, 1.0, YELLOW, v, 0.22) for i, v in enumerate(vals)])
        self.at("Lanes differ")
        idl2 = lab("idealised", 22, GREY).move_to([cxs[1] + 1.2, 2.55, 0])
        self.play(FadeIn(t2), FadeIn(m2), FadeIn(top), FadeIn(idl2), run_time=0.8)
        fold = lab("uneven transfer:\nsignal can change 2 to 4 fold", 24, RED, line_spacing=0.8).move_to([cxs[1], 0.75, 0])
        self.play(FadeIn(fold), run_time=0.5)
        self.at("Add a loading control")
        m3, xs3 = memb(cxs[1], -0.6, 3.9, 1.1, 3)
        low = VGroup(*[band(xs3[i], -0.6, 1.0, GREEN, v, 0.22) for i, v in enumerate(vals)])
        ll = lab("loading control", 26, GREEN).move_to([cxs[1], -1.4, 0])
        idl3 = lab("idealised", 22, GREY).move_to([cxs[1] + 1.2, -0.3, 0])
        self.play(FadeIn(m3), FadeIn(low), FadeIn(ll), FadeIn(idl3), run_time=0.8)
        self.at("a stable protein or the total protein")
        ll2 = lab("a stable protein, or total protein", 24, GREEN).move_to([cxs[1], -1.85, 0])
        self.play(FadeIn(ll2), run_time=0.5)

        # column 3
        ox, oy = cxs[2] - 1.7, -0.6
        ax = VGroup(Line([ox, oy, 0], [ox + 3.4, oy, 0], color=GREY, stroke_width=3),
                    Line([ox, oy, 0], [ox, oy + 3.3, 0], color=GREY, stroke_width=3))
        xl = lab("amount of protein", 24, GREY).move_to([cxs[2], oy - 0.4, 0])
        yl = lab("signal", 24, GREY).move_to([ox + 0.65, oy + 2.95, 0])

        def f(x):
            return 1 - np.exp(-x * 1.7)
        xs_ = np.linspace(0, 1.0, 40)
        W, Hh = 3.2, 2.9
        curve = VMobject()
        curve.set_points_as_corners([np.array([ox + 0.1 + W * x, oy + 0.05 + Hh * f(x * 3.0), 0.0]) for x in xs_])
        curve.set_stroke(YELLOW, 5)
        lin = Rectangle(width=W * 0.2, height=3.1, stroke_width=0, fill_color=GREEN, fill_opacity=0.22).move_to(
            [ox + 0.1 + W * 0.1, oy + 1.55, 0])
        sat = Rectangle(width=W * 0.5, height=3.1, stroke_width=0, fill_color=RED, fill_opacity=0.16).move_to(
            [ox + 0.1 + W * 0.75, oy + 1.55, 0])
        self.at("And stay in the linear range")
        self.play(FadeIn(t3), FadeIn(ax), FadeIn(xl), FadeIn(yl), Create(curve), run_time=1.2)
        idl4 = lab("idealised", 22, GREY).move_to([cxs[2] + 0.9, oy + 1.4, 0])
        self.play(FadeIn(lin), FadeIn(idl4), run_time=0.5)
        llin = lab("linear range", 24, GREEN).move_to([ox + 1.75, oy + 0.55, 0])
        self.play(FadeIn(llin), run_time=0.3)
        self.at("Overloaded abundant targets saturate")
        p1 = Dot([ox + 0.1 + W * 0.62, oy + 0.05 + Hh * f(0.62 * 3.0), 0], color=RED, radius=0.1)
        p2 = Dot([ox + 0.1 + W * 0.95, oy + 0.05 + Hh * f(0.95 * 3.0), 0], color=RED, radius=0.1)
        self.play(FadeOut(llin), FadeIn(sat), FadeIn(p1), FadeIn(p2), run_time=0.7)
        self.at("so equal bands may hide")
        eq = lab("unequal amounts,\nequal bands", 24, RED, line_spacing=0.8).move_to([cxs[2], -1.75, 0])
        self.play(FadeIn(eq), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
def source_tag(text, x, y):
    return T(text, 24, GOLD).move_to([x, y, 0])


class S07Origin(SpokenScene):
    """1979 transfer, 1987 dystrophin."""

    def construct(self):
        cxs = [-3.7, 4.0]
        years = ["1979", "1987"]
        line = Line([-6.2, 2.75, 0], [6.2, 2.75, 0], color=GOLD, stroke_width=3)
        ys = [T(y, 40, GOLD, weight=BOLD).move_to([cxs[i], 3.2, 0]) for i, y in enumerate(years)]
        dots = [Dot([cxs[i], 2.75, 0], color=GOLD, radius=0.1) for i in range(2)]
        self.play(Create(line), run_time=0.4)

        # 1979
        self.at("In 1979")
        self.play(FadeIn(ys[0], shift=DOWN * 0.1), FadeIn(dots[0]), run_time=0.5)
        who1 = lab("Towbin, Staehelin and Gordon", 26, TEXT).move_to([cxs[0], 2.25, 0])
        g, xg, wy = slab(-5.0, 0.45, 2.1, 2.9, 2)
        gb = VGroup(*[band(xg[0], 0.45 + d, 0.8, GREY, 0.7, 0.13) for d in (0.6, -0.8)], band(xg[0], 0.45 - 0.05, 0.8, YELLOW, 1.0, 0.16),
                    *[band(xg[1], 0.45 + d, 0.8, GREY, 0.7, 0.13) for d in (0.6, -0.8)], band(xg[1], 0.45 - 0.05, 0.8, YELLOW, 1.0, 0.16))
        mm, mxs = memb(-2.4, 0.45, 2.1, 2.9, 2)
        mb = gb.copy().shift(RIGHT * 2.6)
        ar = arr([-3.85, 0.45, 0], [-3.55, 0.45, 0], BLUE, 5, 0.15)
        tr = lab("transfer to nitrocellulose", 24, GREY).move_to([cxs[0], -1.3, 0])
        self.play(FadeIn(who1), FadeIn(g), FadeIn(gb), run_time=0.7)
        self.play(FadeIn(mm), GrowArrow(ar), FadeIn(tr), run_time=0.6)
        self.play(FadeIn(mb), run_time=0.5)
        self.at("In their SDS gels")
        keep = lab("band pattern kept", 26, TEXT).move_to([cxs[0], -1.85, 0])
        nq = lab("transfer not quantitative", 26, RED).move_to([cxs[0], -2.35, 0])
        self.play(FadeIn(keep), run_time=0.5)
        self.play(FadeIn(nq), run_time=0.5)
        tg1 = source_tag("Towbin et al., 1979", cxs[0], -3.0)
        self.play(FadeIn(tg1), run_time=0.4)

        # 1987
        self.at("In 1987")
        self.play(FadeIn(ys[1], shift=DOWN * 0.1), FadeIn(dots[1]), run_time=0.5)
        who3 = lab("Hoffman, Brown and Kunkel", 26, TEXT).move_to([cxs[1], 2.25, 0])
        m3, x3 = memb(cxs[1], 0.45, 4.0, 2.9, 3)
        n3 = VGroup(*[lab(n, 24, GREY).move_to([x3[i], -1.25, 0]) for i, n in enumerate(["normal", "DMD", "mdx"])])
        self.play(FadeIn(who3), FadeIn(m3), FadeIn(n3), run_time=0.7)
        self.at("a protein of roughly")
        b3 = band(x3[0], 0.45, 1.1, YELLOW, 1.0, 0.25)
        kd = chip("roughly 400 kd", YELLOW, 26).move_to([cxs[1], -1.85, 0])
        self.play(FadeIn(b3), FadeIn(kd), run_time=0.7)
        self.at("They saw none detectable")
        none = lab("none detectable in DMD or mdx", 24, RED).move_to([cxs[1], -2.4, 0])
        sc = lab("schematic", 22, GREY).move_to([x3[2], 1.8, 0])
        tg3 = source_tag("Hoffman, Brown and Kunkel, 1987", cxs[1], -3.15)
        self.play(FadeIn(none), FadeIn(sc), FadeIn(tg3), run_time=0.8)
        self.finish()


class S08Switch(SpokenScene):
    """Ferrell and Machleder 1998 (one oocyte per lane), Deppmann et al. 2003 (gel shift), then the rule."""

    def construct(self):
        lx, rx = 0.0, 4.1
        m1, xs1 = memb(lx, 1.2, 8.0, 2.8, 8)
        states = [0, 1, 0, 0, 1, 1, 0, None]
        bs = VGroup()
        for i, s_ in enumerate(states):
            if s_ is None:
                continue
            y = 1.2 + (0.4 if s_ else -0.4)
            bs.add(band(xs1[i], y, 0.7, YELLOW, 1.0, 0.2))
        pooled = VGroup(band(xs1[7], 1.6, 0.7, YELLOW, 0.5, 0.2), band(xs1[7], 0.8, 0.7, YELLOW, 0.5, 0.2))
        t1 = lab("individual oocytes", 28, TEXT).move_to([lx, 3.1, 0])
        pl = lab("pooled", 24, GREY).move_to([xs1[7] - 0.35, -0.5, 0])
        tg1 = source_tag("Ferrell and Machleder, 1998", lx, -3.2)
        sc1 = lab("schematic", 22, GREY).move_to([lx, -2.65, 0])

        self.at("In 1998")
        self.play(FadeIn(m1), FadeIn(t1), run_time=0.7)
        self.play(FadeIn(bs), FadeIn(tg1), run_time=0.7)
        self.at("The response was an")
        aon = lab("each oocyte: on or off", 32, YELLOW).move_to([lx, -1.2, 0])
        self.play(FadeIn(aon), FadeIn(sc1), run_time=0.6)
        self.at("Pooled eggs would hide")
        self.play(FadeIn(pl), FadeIn(pooled), run_time=0.6)
        hide = lab("pooled: the switch is hidden", 30, RED).move_to([lx, -2.0, 0])
        self.play(FadeIn(hide), run_time=0.5)

        self.at("Rule")
        allm = VGroup(m1, t1, bs, pooled, pl, tg1, aon, sc1, hide)
        self.play(FadeOut(allm), run_time=0.6)
        r1 = chip("A band gives size,", GOLD, 40).move_to([0, 1.4, 0])
        r1b = chip("and amount only within the linear range", GOLD, 40).move_to([0, 0.2, 0])
        self.at("A band gives size")
        self.play(FadeIn(r1, shift=UP * 0.15), run_time=0.5)
        self.play(FadeIn(r1b, shift=UP * 0.15), run_time=0.6)
        r2 = chip("A band of the right size is not proof of identity", RED, 36).move_to([0, -1.6, 0])
        self.at("A band of the right size")
        self.play(FadeIn(r2, shift=UP * 0.15), run_time=0.6)
        self.finish()


class S09End(EndCard):
    LINE = "A band of the right size is not proof of identity."
