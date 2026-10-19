"""Sensory prostheses: a contact is not a channel  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = implant hardware: cochlear contacts, retinal electrodes, native implant resolution
  YELLOW = electric current and its fields (a model sketch, not a measurement)
  TEAL   = a channel (a band of frequency information)
  PURPLE = ganglion cells and their axons of passage
  GREEN  = a participant who met the endpoint
  ORANGE = zoom (implant plus a magnifier)
  RED    = serious events, and the "is not" sign
  TEXT   = what the person perceives (percepts), people in general
  GREY   = outlines, unassessed people, labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def contact(x, y, size=0.36, color=BLUE):
    return Square(side_length=size, stroke_color=color, stroke_width=3, fill_color=color,
                  fill_opacity=0.55).move_to([x, y, 0])


def poly(points, color, fill=0.0, w=3, fill_color=None):
    m = VMobject()
    m.set_points_as_corners([np.array([x, y, 0.0]) for x, y in points])
    m.set_stroke(color, w)
    m.set_fill(fill_color or color, fill)
    return m


def bell(c, base, amp, s, x0, x1, n=60):
    xs = np.linspace(x0, x1, n)
    return xs, base + amp * np.exp(-0.5 * ((xs - c) / s) ** 2)


class S00Title(TitleCard):
    LESSON = "Restoring senses: implants and prostheses"
    TITLE = "A contact is not a channel"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        n, pitch, y = 22, 0.5, 0.7
        x0 = -(n - 1) * pitch / 2
        bar = RoundedRectangle(corner_radius=0.2, width=n * pitch + 0.3, height=0.75, stroke_color=GREY,
                               stroke_width=3, fill_color=GREY, fill_opacity=0.25).move_to([0, y, 0])
        cs = VGroup(*[contact(x0 + i * pitch, y) for i in range(n)])
        lab = T("cochlear implant array", 30, GREY).move_to([0, y + 1.3, 0])
        self.play(FadeIn(bar), FadeIn(lab), run_time=0.8)
        self.at("contacts")
        self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in cs], lag_ratio=0.06), run_time=2.0)
        cnt = T("up to 22 contacts", 32, BLUE).move_to([0, y - 1.0, 0])
        self.play(FadeIn(cnt), run_time=0.5)
        self.at("stopped improving")
        ch = bchip("8 to 10 channels", TEAL, 34).move_to([0, -1.9, 0])
        sub = T("speech scores stopped improving: one study of 18 adult implant users", 24, GREY).move_to([0, -2.9, 0])
        a = arr([0, y - 1.4, 0], [0, -1.35, 0], TEAL)
        self.play(GrowArrow(a), FadeIn(ch, shift=UP * 0.15), FadeIn(sub), run_time=1.0)
        self.at("what is a channel")
        q = T("?", 56, YELLOW, weight=BOLD).next_to(ch, RIGHT, buff=0.4)
        self.play(FadeIn(q, scale=1.4), run_time=0.5)
        self.at("electrode in the eye")
        self.play(*[FadeOut(m) for m in (bar, cs, lab, cnt, a, ch, sub, q)], run_time=0.6)
        eye = T("in the eye", 32, GREY).move_to([0, 2.6, 0])
        el = contact(-3.5, 0, 1.0)
        ell = T("one electrode", 30, BLUE).next_to(el, DOWN, buff=0.4)
        box = DashedVMobject(Square(side_length=2.2, stroke_color=TEXT, stroke_width=3)).move_to([3.5, 0, 0])
        qq = T("?", 80, YELLOW, weight=BOLD).move_to(box)
        bl = T("one pixel?", 30, TEXT).next_to(box, DOWN, buff=0.4)
        ar = arr([-2.5, 0, 0], [2.2, 0, 0], GREY)
        self.play(FadeIn(eye), FadeIn(el), FadeIn(ell), run_time=0.6)
        self.play(GrowArrow(ar), FadeIn(box), FadeIn(qq), FadeIn(bl), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Overlap(SpokenScene):
    def construct(self):
        n, pitch, yc = 7, 1.65, -1.1
        xs = [-(n - 1) * pitch / 2 + i * pitch for i in range(n)]
        sig, amp, base = 0.78, 2.3, -0.65
        head = T("a few contacts, enlarged", 28, GREY).to_edge(UP, buff=0.35)
        bar = RoundedRectangle(corner_radius=0.2, width=xs[-1] - xs[0] + 1.6, height=0.8, stroke_color=GREY,
                               stroke_width=3, fill_color=GREY, fill_opacity=0.25).move_to([0, yc, 0])
        cs = VGroup(*[contact(x, yc, 0.55) for x in xs])
        self.play(FadeIn(head), FadeIn(bar), FadeIn(cs), run_time=0.5)
        cl = T("contact: hardware", 28, BLUE).move_to([-3.3, -2.2, 0])
        cla = arr([-3.3, -1.9, 0], [xs[1] - 0.05, yc - 0.4, 0], BLUE, w=4)
        self.at("hardware")
        self.play(FadeIn(cl), GrowArrow(cla), run_time=0.8)
        # channel = a band of frequency information
        bx = xs[3]
        band = Rectangle(width=pitch * 0.95, height=3.1, stroke_color=TEAL, stroke_width=3, fill_color=TEAL,
                         fill_opacity=0.18).move_to([bx, 0.7, 0])
        bl = T("channel: a band of frequency information", 28, TEAL).move_to([2.2, 2.95, 0])
        bla = arr([bx + 0.7, 2.8, 0], [bx + 0.15, 2.3, 0], TEAL, w=4)
        self.at("band of frequency")
        self.play(FadeIn(band), FadeIn(bl), GrowArrow(bla), run_time=0.9)
        # clinical map
        axis = arr([-5.9, -2.5, 0], [5.9, -2.5, 0], GREY, w=4)
        hi = T("base: higher frequencies", 26, GREY).move_to([-3.9, -3.0, 0])
        lo = T("apex: lower frequencies", 26, GREY).move_to([3.9, -3.0, 0])
        self.at("clinical maps")
        self.play(FadeOut(cl), FadeOut(cla), FadeOut(bl), FadeOut(bla), FadeOut(band), FadeOut(head), run_time=0.4)
        self.play(GrowArrow(axis), FadeIn(hi), FadeIn(lo), run_time=1.0)
        # overlapping fields (a sketch)
        fields, overlaps = [], []
        for x in xs:
            gx, gy = bell(x, base, amp, sig, x - 1.9, x + 1.9)
            fields.append(poly(list(zip(gx, gy)), YELLOW, 0.14, w=3))
        for i in range(n - 1):
            gx = np.linspace(xs[i] - 0.6, xs[i + 1] + 0.6, 60)
            g1 = base + amp * np.exp(-0.5 * ((gx - xs[i]) / sig) ** 2)
            g2 = base + amp * np.exp(-0.5 * ((gx - xs[i + 1]) / sig) ** 2)
            ym = np.minimum(g1, g2)
            pts = list(zip(gx, ym)) + [(gx[-1], base), (gx[0], base)]
            overlaps.append(poly(pts, YELLOW, 0.6, w=0))
        tag = T("electric fields, in this sketch", 26, YELLOW).move_to([0, 2.55, 0])
        self.at("Neighboring contacts")
        self.play(LaggedStart(*[FadeIn(f) for f in fields], lag_ratio=0.1), FadeIn(tag), run_time=1.2)
        self.at("overlapping electric fields")
        ov = VGroup(*overlaps)
        self.play(FadeIn(ov), run_time=0.8)
        ci = bchip("overlap = channel interaction", YELLOW, 28).move_to([0, 2.55, 0])
        self.at("channel interaction")
        self.play(FadeOut(tag), FadeIn(ci, shift=DOWN * 0.1), run_time=0.6)
        self.at("So many contacts")
        neq = VGroup(T("many contacts", 30, BLUE), T("≠", 40, RED, weight=BOLD),
                     T("as many independent channels", 30, TEAL)).arrange(RIGHT, buff=0.3).move_to([0, 3.25, 0])
        self.play(FadeOut(ci), FadeIn(neq), run_time=0.7)
        self.at("The plateau depends")
        pl = bchip("plateau depends on array type and placement", GREY, 26).move_to([0, 2.3, 0])
        self.play(FadeIn(pl, shift=DOWN * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Streak(SpokenScene):
    def construct(self):
        # retina, schematic surface view (left); percept panel (right)
        head = T("retina, schematic", 26, GREY).move_to([-3.1, 3.2, 0])
        panel = RoundedRectangle(corner_radius=0.15, width=3.8, height=4.2, stroke_color=GREY, stroke_width=3,
                                 fill_color=GREY, fill_opacity=0.12).move_to([4.4, 0.2, 0])
        plab = T("what the person sees", 26, TEXT).move_to([4.4, 2.8, 0])
        ey0 = 0.2
        el = contact(-3.4, ey0, 0.7)
        ell = T("epiretinal electrode over the macular retina (schematic)".replace(" over", "\nover"), 24, BLUE).move_to([-3.1, -2.95, 0])
        elr = arr([-3.4, -2.6, 0], [-3.4, ey0 - 0.45, 0], BLUE, w=4)
        dot = Circle(radius=0.22, stroke_width=0, fill_color=TEXT, fill_opacity=1).move_to([4.4, 0.2, 0])
        dl = T("expected: one dot", 26, TEXT).move_to([4.4, -1.4, 0])
        self.play(FadeIn(head), FadeIn(panel), FadeIn(plab), run_time=0.6)
        self.at("camera")
        offs = [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (dx, dy) != (0, 0)]
        gel = VGroup(*[contact(-3.4 + dx * 1.0, ey0 + dy * 1.0, 0.5) for dx, dy in offs])
        gdt = VGroup(*[Circle(radius=0.2, stroke_width=0, fill_color=TEXT, fill_opacity=1).move_to([4.4 + dx * 0.9, 0.5 + dy * 0.9, 0]) for dx, dy in offs])
        dot.move_to([4.4, 0.5, 0])
        dl.move_to([4.4, -1.5, 0])
        dl_grid = T("expected:\na grid of dots", 26, TEXT).move_to([4.4, -1.35, 0])
        self.play(FadeIn(el), FadeIn(gel), FadeIn(dot), FadeIn(gdt), FadeIn(dl_grid), run_time=0.9)
        self.at("But an electrode")
        self.play(FadeOut(gel), FadeOut(gdt), FadeOut(dl_grid), FadeOut(head), run_time=0.6)
        self.play(GrowArrow(elr), FadeIn(ell), dot.animate.move_to([4.4, 0.2, 0]), FadeIn(dl), run_time=0.7)
        # ganglion cells and axons
        ys = [1.9, 1.3, 0.7, 0.2, -0.4, -1.0, -1.6]
        disk_c = np.array([1.2, 0.2, 0])
        disk = Circle(radius=0.55, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.3).move_to(disk_c)
        dlab = T("optic disk", 26, GREY).next_to(disk, UP, buff=0.5)
        cells, axons = [], []
        for y in ys:
            c = Circle(radius=0.14, stroke_color=PURPLE, stroke_width=2.5, fill_color=PURPLE, fill_opacity=0.7).move_to([-5.5, y, 0])
            ax = Line([-5.36, y, 0], [disk_c[0] - 0.5, 0.2 + (y - 0.2) * 0.15, 0], color=PURPLE, stroke_width=3)
            cells.append(c); axons.append(ax)
        grp = VGroup(*cells, *axons)
        axl = T("ganglion-cell axons", 26, PURPLE).move_to([-3.1, 2.75, 0])
        self.at("axons running")
        self.play(FadeIn(disk), FadeIn(dlab), LaggedStart(*[Create(a) for a in axons], lag_ratio=0.1),
                  FadeIn(VGroup(*cells)), FadeIn(axl), run_time=1.6)
        # the axons passing the electrode: those whose line passes y near 0.2 at x=-3.4
        def ay(i, x):
            y = ys[i]; yend = 0.2 + (y - 0.2) * 0.15
            t = (x + 5.36) / (disk_c[0] - 0.5 + 5.36)
            return y + (yend - y) * t
        pass_idx = [i for i in range(len(ys)) if abs(ay(i, -3.4) - ey0) < 0.45]
        self.at("axons of passage")
        hl = [axons[i].animate.set_color(YELLOW).set_stroke(width=6) for i in pass_idx]
        cur = Circle(radius=0.75, stroke_color=YELLOW, stroke_width=3).move_to(el)
        self.play(Create(cur), *hl, run_time=0.9)
        self.play(*[cells[i].animate.set_color(YELLOW) for i in pass_idx], FadeOut(cur), run_time=0.6)
        self.at("follows the places")
        cy = [ys[i] for i in pass_idx]
        top, bot = max(cy), min(cy)
        streak = Ellipse(width=0.6, height=2.0, stroke_width=0, fill_color=TEXT, fill_opacity=1).move_to([4.4, 0.7, 0])
        streak.rotate(PI / 2 * 0.0)
        sl = T("one example of an\nelongated or distorted\npercept", 24, TEXT).move_to([4.4, -1.15, 0])
        self.play(ReplacementTransform(dot, streak), ReplacementTransform(dl, sl), run_time=1.0)
        self.at("Four adults")
        note = T("4 adults with Argus implants drew single-electrode percepts", 24, TEXT).move_to([0, -3.45, 0])
        self.play(FadeOut(ell), FadeOut(elr), FadeIn(note), run_time=0.7)
        self.at("an axon model")
        mod = bchip("axon-pathway model", PURPLE, 26).move_to([-3.1, -2.75, 0])
        self.play(FadeIn(mod, shift=UP * 0.1), run_time=0.6)
        self.at("direct recording")
        ms = bchip("model-supported explanation, not a recording", GREY, 24).move_to([-0.0, -2.75, 0]).shift(LEFT * 0)
        self.play(FadeOut(mod), FadeOut(note), FadeIn(ms.move_to([-1.6, -2.95, 0])), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Count(SpokenScene):
    def construct(self):
        head = T("PRIMAvera: open-label, single-arm; adults with geographic atrophy", 26, GREY).move_to([0, 3.2, 0])
        cols, rows, pitch, r = 10, 4, 1.0, 0.38
        gx0, gy0 = -4.5, 2.5
        dots = []
        for k in range(38):
            rr, cc = divmod(k, cols)
            d = Circle(radius=r, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.9)
            d.move_to([gx0 + cc * pitch, gy0 - rr * pitch, 0])
            dots.append(d)
        grid = VGroup(*dots)
        self.play(FadeIn(head), run_time=0.7)
        self.at("were implanted")
        cnt1 = T("38 implanted", 32, GREY).move_to([0, -1.4, 0])
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.03), FadeIn(cnt1), run_time=1.6)
        self.at("were assessed")
        un = dots[32:]
        asd = dots[:32]
        cnt2 = T("32 assessed at twelve months", 32, TEXT).move_to([0, -1.4, 0])
        self.play(*[d.animate.set_stroke(TEXT).set_fill(TEXT, 0.9) for d in asd],
                  *[d.animate.set_fill(BG, 1).set_stroke(GREY) for d in un],
                  ReplacementTransform(cnt1, cnt2), run_time=1.0)
        self.at("met the endpoint")
        cnt3 = T("26 met the endpoint", 32, GREEN).move_to([0, -1.4, 0])
        self.play(*[d.animate.set_stroke(GREEN).set_fill(GREEN, 0.95) for d in dots[:26]],
                  ReplacementTransform(cnt2, cnt3), run_time=1.0)
        def key(col, fill, text):
            d = Circle(radius=0.16, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=fill)
            return VGroup(d, T(text, 24, TEXT)).arrange(RIGHT, buff=0.15)
        legend = VGroup(key(GREEN, 0.95, "met the endpoint"), key(TEXT, 0.9, "assessed, not met"),
                        key(GREY, 0.0, "not assessed")).arrange(RIGHT, buff=0.6).move_to([0, -3.2, 0])
        self.play(FadeIn(legend), run_time=0.6)
        # fraction 1
        br1 = Brace(VGroup(*asd[:10]), UP, color=TEXT)  # placeholder, replaced below
        self.remove(br1)
        f1 = VGroup(T("26 / 32 = 81.3%", 36, GREEN, weight=BOLD), T("of those assessed", 26, TEXT)).arrange(DOWN, buff=0.15)
        f1.move_to([-3.1, -2.2, 0])
        self.at("of those assessed")
        self.play(FadeIn(f1, shift=LEFT * 0.2), FadeOut(cnt3), run_time=0.8)
        self.at("Count the")
        unbox = SurroundingRectangle(VGroup(*un), color=GREY, buff=0.12, corner_radius=0.1)
        unl = T("6 not assessed", 26, GREY).next_to(unbox, DOWN, buff=0.15)
        self.play(Create(unbox), FadeIn(unl), run_time=0.8)
        f2 = VGroup(T("26 / 38 = 68.4%", 36, GREEN, weight=BOLD), T("of those implanted", 26, GREY)).arrange(DOWN, buff=0.15)
        f2.move_to([3.1, -2.2, 0])
        self.at("of those implanted")
        self.play(FadeIn(f2, shift=LEFT * 0.2), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Native(SpokenScene):
    def construct(self):
        # left: with the PRIMA glasses and zoom; right: native implant resolution
        divider = DashedLine([0.15, 3.3, 0], [0.15, -2.4, 0], color=GREY, stroke_width=3)
        lh = T("with the PRIMA glasses", 32, ORANGE, weight=BOLD).move_to([-3.3, 3.0, 0])
        rh = T("native implant", 32, BLUE, weight=BOLD).move_to([3.5, 3.0, 0])
        ep = bchip("endpoint:\ngain of at least 0.2 logMAR", ORANGE, 26).move_to([-3.3, 1.75, 0])
        self.at("The endpoint")
        self.play(FadeIn(lh), FadeIn(ep, shift=DOWN * 0.1), Create(divider), run_time=1.0)
        self.at("adjust zoom")
        sl_line = Line([-5.6, -0.1, 0], [-1.0, -0.1, 0], color=ORANGE, stroke_width=5)
        t1 = T("1×", 30, ORANGE).move_to([-5.6, -0.75, 0])
        t12 = T("12×", 30, ORANGE).move_to([-1.0, -0.75, 0])
        knob = Circle(radius=0.2, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=1).move_to([-5.6, -0.1, 0])
        zl = T("zoom", 30, ORANGE).move_to([-3.3, 0.6, 0])
        self.play(Create(sl_line), FadeIn(t1), FadeIn(t12), FadeIn(knob), FadeIn(zl), run_time=0.8)
        self.play(knob.animate.move_to([-1.0, -0.1, 0]), run_time=1.5)
        self.at("implant plus a magnifier")
        zsum = bchip("implant + magnifier", ORANGE, 28).move_to([-3.3, -1.7, 0])
        self.play(FadeIn(zsum, shift=UP * 0.1), run_time=0.7)
        self.at("Without zoom or image processing")
        nz = bchip("no zoom, no image processing", BLUE, 26).move_to([3.5, 1.75, 0])
        self.play(FadeIn(rh), FadeIn(nz, shift=DOWN * 0.1), run_time=0.8)
        self.at("mean implant resolution")
        nat = T("1.32 logMAR", 46, BLUE, weight=BOLD).move_to([3.5, 0.55, 0])
        self.play(FadeIn(nat, scale=0.9), run_time=0.8)
        self.at("to the power")
        w = M("20 × 10^1.32 ≈ 417", 30, BLUE).move_to([3.5, -0.6, 0])
        self.play(FadeIn(w), run_time=0.7)
        self.at("so 20 over")
        sn = T("= 20/417", 50, BLUE, weight=BOLD).move_to([3.5, -1.7, 0])
        self.play(FadeIn(sn, shift=UP * 0.1), run_time=0.7)
        self.at("separate measurements")
        sep = bchip("separate measurements", RED, 32).move_to([0.15, -3.05, 0])
        self.play(FadeIn(sep, scale=0.9), divider.animate.set_color(RED).set_stroke(width=6), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        ev = VGroup(T("19 participants", 40, RED, weight=BOLD),
                    T("26 serious device- or procedure-related events", 32, RED)).arrange(DOWN, buff=0.25)
        evb = RoundedRectangle(corner_radius=0.2, width=ev.width + 0.8, height=ev.height + 0.7, stroke_color=RED,
                               stroke_width=3, fill_color=RED, fill_opacity=0.12).move_to(ev)
        evg = VGroup(evb, ev).move_to([0, 0.3, 0])
        self.at("Serious events")
        self.play(FadeIn(evg, scale=0.95), run_time=0.9)
        ask = T("ask what was counted", 38, TEXT, weight=BOLD).move_to([0, 1.8, 0])
        self.at("ask what was counted")
        small = VGroup(T("19 participants", 26, RED, weight=BOLD),
                       T("26 serious device- or procedure-related events", 24, RED)).arrange(DOWN, buff=0.12)
        sb = RoundedRectangle(corner_radius=0.15, width=small.width + 0.6, height=small.height + 0.4, stroke_color=RED,
                              stroke_width=3, fill_color=RED, fill_opacity=0.12).move_to(small)
        sg = VGroup(sb, small).move_to([0, 3.0, 0])
        self.play(ReplacementTransform(evg, sg), run_time=0.7)
        self.play(FadeIn(ask, scale=0.95), run_time=0.5)
        pairs = [("contacts", BLUE, "channels", TEAL, "Contacts are not channels"),
                 ("electrodes", BLUE, "pixels", TEXT, "electrodes are not pixels"),
                 ("people assessed", TEXT, "people implanted", GREY, "people assessed"),
                 ("native", BLUE, "zoomed", ORANGE, "Native resolution")]
        ys = [0.6, -0.5, -1.6, -2.7]
        for (a, ca, b, cb, cue), y in zip(pairs, ys):
            ca_c = bchip(a, ca, 30)
            cb_c = bchip(b, cb, 30)
            ne = T("\u2260", 44, RED, weight=BOLD)
            row = VGroup(ca_c, ne, cb_c).arrange(RIGHT, buff=0.5).move_to([0, y, 0])
            self.at(cue)
            self.play(FadeIn(row, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "Ask what was counted. Native resolution is not zoomed reading."
