"""The organizer, chapter 3: Dead Tissue That Still Induces  (Biochemistrypedia chaptered film)

COLOR MAP (one colour per concept, same as chapters 1 and 2)
  BLUE   = ectoderm that is on its way to skin
  PURPLE = neural fate
  CREAM  = organizer tissue (dashed-look grey fill + cream outline = killed organizer)
  YELLOW = the signal / what is highlighted
  GREY   = outlines, labels, dishes
  RED    = the open question, the brake, a cross
  GREEN  = a tick, "yes", "sufficient" (this chapter only)
  TEAL   = an organized second axis, "necessary", next-lesson cue (this chapter only)
  AMBER  = injuring agents (injury, chemicals) (this chapter only)
  HEAT   = heat treatment (this chapter only)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
CREAM = "#F2EBD3"
AMBER = "#E39A3C"
HEAT = "#E8743B"
ICE = "#CFE9F5"


# ------------------------------------------------------------------ small helpers
def lab(text, color=GREY, size=26, **kw):
    return T(text, size, color, **kw)


def arr(a, b, color=GREY, w=6, tip=0.25):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def circ(x, y, color=BLUE, r=0.33, fo=0.5):
    return Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=fo).move_to([x, y, 0])


def recolor(cells, color, fo=0.5):
    return [c.animate.set_stroke(color).set_fill(color, fo) for c in cells]


def hexsheet(cx, cy, cols, rows, r=0.34, color=BLUE, gap=1.06):
    dx = 2 * r * gap
    dy = dx * 0.866
    g = VGroup()
    for j in range(rows):
        for i in range(cols):
            x = cx + (i - (cols - 1) / 2) * dx + (dx / 4 if j % 2 else -dx / 4)
            y = cy + ((rows - 1) / 2 - j) * dy
            g.add(circ(x, y, color, r))
    return g


def flatsheet(cx, cy, cols, rows, w=0.9, h=0.3, color=BLUE, dx=0.98, dy=0.38):
    g = VGroup()
    for j in range(rows):
        for i in range(cols):
            x = cx + (i - (cols - 1) / 2) * dx + (dx / 4 if j % 2 else -dx / 4)
            y = cy + ((rows - 1) / 2 - j) * dy
            e = Ellipse(width=w, height=h, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.5)
            g.add(e.move_to([x, y, 0]))
    return g


def piece(cx, cy, r=0.26, dead=False):
    """a small cluster of organizer cells: living (solid cream) or killed (grey fill, faint cream outline)."""
    d = r * 2.1
    pts = [(0, 0)] + [(d * np.cos(a), d * np.sin(a)) for a in np.arange(6) * PI / 3]
    g = VGroup()
    for px, py in pts:
        c = Circle(radius=r, stroke_width=3)
        if dead:
            c.set_stroke(CREAM, opacity=0.7).set_fill(GREY, 0.35)
        else:
            c.set_stroke(CREAM).set_fill(CREAM, 0.85)
        g.add(c.move_to([cx + px, cy + py, 0]))
    return g


def kill(g):
    return [c.animate.set_stroke(CREAM, opacity=0.7).set_fill(GREY, 0.35) for c in g]


def tick(x, y, s=0.3, color=GREEN):
    return VGroup(Line([x - s, y, 0], [x - s * 0.35, y - s * 0.75, 0]),
                  Line([x - s * 0.35, y - s * 0.75, 0], [x + s, y + s * 0.8, 0])).set_stroke(color, 9)


def cross(x, y, s=0.28, color=RED):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0]),
                  Line([x - s, y + s, 0], [x + s, y - s, 0])).set_stroke(color, 9)


def dish(cx, cy, w=6.5, h=4.7):
    return RoundedRectangle(corner_radius=0.55, width=w, height=h, stroke_color=GREY, stroke_width=4,
                            fill_color=GREY, fill_opacity=0.07).move_to([cx, cy, 0])



LIGHT = "#C3C9D3"


def fitw(mob, max_w):
    if mob.width > max_w:
        mob.scale(max_w / mob.width)
    return mob


def hdr_with_x(text, color, y=3.62, size=28, cross_color=RED, with_x=True):
    """one heading; the cross (if any) sits inside it, right before the words."""
    t = lab(text, color, size)
    if not with_x:
        return t.move_to([0, y, 0])
    x = cross(0, 0, 0.2, cross_color)
    g = VGroup(x, t).arrange(RIGHT, buff=0.25).move_to([0, y, 0])
    return g


# ------------------------------------------------------------------ the two-dish stage (s03 to s08)
D1X, D2X, DY = -3.55, 3.55, 0.55
SHEET2X = 4.55
MK, CHX, CHY1, CHY2 = 0.75, 1.3, -1.25, -2.1
CR = 0.38            # cell radius in the dishes


def ones(n):
    return [i for i in range(n) if i % 4 != 3]


def schematic(cx, cy):
    """a tiny second axis: neural tube over a rod, with a row of blocks beside (teal outline = organized axis)."""
    tube = RoundedRectangle(corner_radius=0.12, width=1.9, height=0.3, stroke_color=PURPLE, stroke_width=3,
                            fill_color=PURPLE, fill_opacity=0.55).move_to([cx, cy + 0.26, 0])
    rod = RoundedRectangle(corner_radius=0.07, width=1.9, height=0.14, stroke_color=TEAL, stroke_width=3,
                           fill_color=TEAL, fill_opacity=0.5).move_to([cx, cy - 0.02, 0])
    blocks = VGroup(*[Square(0.26, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.25)
                      .move_to([cx - 0.75 + 0.5 * i, cy - 0.33, 0]) for i in range(4)])
    return VGroup(tube, rod, blocks)


def stage(d2="blue", chips="q", header="early-gastrula ectoderm", header_color=BLUE, hdr_x=False,
          frac=False, axis_done=False):
    """Rebuild the s03 picture exactly; returns a dict of mobjects (not added to the scene)."""
    S = {}
    S["hdr"] = hdr_with_x(header, header_color, with_x=hdr_x)
    S["dish1"], S["dish2"] = dish(D1X, 0.05, h=5.5), dish(D2X, 0.05, h=5.5)
    S["l1"] = lab("ectoderm alone", BLUE, 28).move_to([D1X, 3.08, 0])
    S["l2"] = lab("ectoderm + killed organizer", CREAM, 28).move_to([D2X, 3.08, 0])
    S["skin"] = flatsheet(D1X, DY, 5, 4, w=1.0, h=0.4, dx=1.1, dy=0.55)
    S["res1"] = lab("skin", BLUE, 38, weight=BOLD).move_to([D1X, -1.65, 0])
    sh = hexsheet(SHEET2X, DY + 0.15, 5, 4, CR, BLUE)
    if d2 == "neural":
        for i, c in enumerate(sh):
            if (not frac) or i % 4 != 3:
                c.set_stroke(PURPLE).set_fill(PURPLE, 0.5)
    S["sheet2"] = sh
    S["piece"] = piece(1.3, DY, 0.32, dead=True)
    if chips:
        txt1 = "neural?" if chips == "q" else ("often neural" if frac else "neural")
        S["c_neural"] = chip(txt1, PURPLE, 30)
        S["c_axis"] = chip("no organized second axis" if axis_done else "second axis?", TEAL, 30)
        S["c_neural"].move_to([CHX + S["c_neural"].width / 2, CHY1, 0])
        S["c_axis"].move_to([CHX + S["c_axis"].width / 2, CHY2, 0])
        if chips in ("tick", "cross"):
            S["t_neural"] = tick(MK, CHY1)
        if chips == "cross":
            S["t_axis"] = cross(MK, CHY2)
    return S


def stage_group(S):
    return VGroup(*[v for v in S.values()])


# ------------------------------------------------------------------ the results table (s10 to s15)
TY = [2.8 - 1.05 * i for i in range(6)]
TL, TR = -6.4, 6.4
ROWS = [
    ("ectoderm alone (control)", "early gastrula, no tissue added", "no (skin)", RED),
    ("killed organizer", "neural tissue, but no organized axis", "often", GREEN),
    ("other killed tissues", None, "yes, many", GREEN),
    ("ether extracts of amphibian tissue", "Waddington, Needham and Needham, by 1934", "in some tests", GREEN),
    ("unrelated materials", "from adult tissues to synthetic chemicals", "in some cases", GREEN),
    ("salamander: no organizer / brief damage", "Barth, then Holtfreter, 1940s", "in some cultures", GREEN),
]


def tparts(i):
    label, detail, ans, col = ROWS[i]
    y = TY[i]
    C = chip(ans, col, 28)
    C.move_to([TR - C.width / 2, y, 0])
    maxw = (TR - C.width - 0.3) - TL
    L = fitw(lab(label, TEXT, 32), maxw)
    L.move_to([TL + L.width / 2, y + (0.23 if detail else 0), 0])
    D = None
    if detail:
        D = fitw(lab(detail, LIGHT, 32), maxw)
        D.move_to([TL + D.width / 2, y - 0.26, 0])
    rule = Line([TL, y - 0.54, 0], [TR, y - 0.54, 0], stroke_color=GREY, stroke_width=1.5, stroke_opacity=0.5)
    return L, D, C, rule


def table_title():
    t = lab("Scores neural?", TEXT, 38, weight=BOLD)
    return t.move_to([TL + t.width / 2, 3.55, 0])


def table_static(n):
    """title + the first n rows, complete."""
    g = VGroup(table_title())
    for i in range(n):
        L, D, C, rule = tparts(i)
        g.add(L, C, rule)
        if D:
            g.add(D)
    return g


NOTE_TXT = "examples from different labs and species, not matched trials"
MORAL_TXT = "When almost everything scores yes, a yes cannot name the signal."


def moral_parts():
    note = fitw(lab(NOTE_TXT, LIGHT, 26), 12.0).move_to([0, -3.2, 0])
    moral = fitw(lab(MORAL_TXT, YELLOW, 32), 12.4).move_to([0, -3.6, 0])
    return note, moral


# ------------------------------------------------------------------ the hidden-tendency sheet (s16, s17, s19)
TSX, TSY = 0.0, -0.2
TR_ = 0.47


def tend_sheet(cx, cy, cols=12, rows=5, r=TR_):
    sh = hexsheet(cx, cy, cols, rows, r)
    dots = VGroup(*[Dot(c.get_center(), radius=0.13, color=PURPLE).set_opacity(0.45) for c in sh])
    return sh, dots


# =============================================================================================
class S00Title(TitleCard):
    LESSON = "The organizer: Spemann and Mangold"
    TITLE = "Dead Tissue That Still Induces"


# ---------------------------------------------------------------------------------------------
class S01Q(SpokenScene):
    def construct(self):
        dsh = dish(3.4, 0.3)
        sheet = hexsheet(3.4, 0.3, 5, 4, CR, BLUE)
        l_d = lab("ectoderm in a dish", BLUE, 30).move_to([3.4, 3.05, 0])
        self.play(FadeIn(dsh), FadeIn(sheet, lag_ratio=0.02), FadeIn(l_d), run_time=0.35)
        pc = piece(-4.9, 0.3, 0.42)
        l_o = lab("organizer", CREAM, 36, weight=BOLD).move_to([-4.9, 2.3, 0])
        self.at("organizer sends")
        self.play(FadeIn(pc, scale=0.6), FadeIn(l_o), run_time=0.5)
        a = arr([-3.2, 0.3, 0], [0.0, 0.3, 0], YELLOW, 9)
        self.at("sends a signal")
        self.play(GrowArrow(a), run_time=0.6)
        sub = chip("a substance?", YELLOW, 30).move_to([-1.6, 1.15, 0])
        self.at("should be a substance")
        self.play(FadeIn(sub, shift=DOWN * 0.15), run_time=0.6)
        l_k = lab("killed", GREY, 36).move_to([-4.9, 2.3, 0])
        self.at("kill the cells")
        self.play(*kill(pc), FadeOut(l_o), FadeIn(l_k), run_time=1.0)
        q = T("?", 150, RED, weight=BOLD).move_to([3.4, 0.3, 0])
        self.at("Does it still work")
        self.play(sheet.animate.set_opacity(0.3), FadeIn(q, scale=0.4), run_time=0.7)
        self.play(Indicate(a, color=YELLOW, scale_factor=1.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02H(SpokenScene):
    def construct(self):
        xs = [-4.4, 0.0, 4.4]
        PY = -0.1
        pcs = [piece(x, PY, 0.42) for x in xs]
        cred = lab("Johannes Holtfreter, from 1933", TEXT, 36).move_to([0, 3.5, 0])
        self.play(FadeIn(cred, shift=DOWN * 0.1), run_time=0.5)
        self.at("from 1933")
        lp = lab("organizer pieces", CREAM, 32).move_to([0, -3.3, 0])
        self.play(*[FadeIn(p, scale=0.7) for p in pcs], FadeIn(lp), run_time=0.6)
        self.at("Holt")
        self.play(*[Indicate(p, color=CREAM, scale_factor=1.08) for p in pcs], run_time=0.8)
        # frozen
        flake = VGroup(*[Line(np.array([np.cos(a), np.sin(a), 0]) * -0.6, np.array([np.cos(a), np.sin(a), 0]) * 0.6)
                         for a in (0, PI / 3, 2 * PI / 3)]).set_stroke(ICE, 8).move_to([xs[0], 2.25, 0])
        l1 = lab("frozen", ICE, 36).move_to([xs[0], -1.95, 0])
        self.at("froze")
        self.play(FadeIn(flake, scale=0.4), FadeIn(l1), *kill(pcs[0]), run_time=0.8)
        # dried
        sun = VGroup(Circle(radius=0.26, stroke_color=AMBER, fill_color=AMBER, fill_opacity=0.9),
                     *[Line(np.array([np.cos(a), np.sin(a), 0]) * 0.42, np.array([np.cos(a), np.sin(a), 0]) * 0.66).set_stroke(AMBER, 7)
                       for a in np.arange(8) * PI / 4]).move_to([xs[1], 2.25, 0])
        l2 = lab("dried", AMBER, 36).move_to([xs[1], -1.95, 0])
        self.at("dried")
        self.play(FadeIn(sun, scale=0.4), FadeIn(l2), *kill(pcs[1]), run_time=0.8)
        # heated
        waves = VGroup(*[ParametricFunction(lambda t, x0=x0: np.array([x0 + 0.14 * np.sin(5 * t), t, 0]), t_range=[0, 1.1])
                         .set_stroke(HEAT, 7) for x0 in (-0.4, 0, 0.4)]).move_to([xs[2], 2.25, 0])
        l3 = lab("heated", HEAT, 36).move_to([xs[2], -1.95, 0])
        self.at("heated")
        self.play(FadeIn(waves, shift=UP * 0.2), FadeIn(l3), *kill(pcs[2]), run_time=0.8)
        # boiling
        bub = VGroup(*[Circle(radius=r, stroke_color=HEAT, stroke_width=4).move_to([xs[2] + dx, PY + dy, 0])
                       for r, dx, dy in ((0.26, -0.7, -0.9), (0.34, 0.55, -0.95), (0.22, 1.05, -0.2), (0.3, -0.2, 1.1))])
        l3b = lab("heated to boiling", HEAT, 36).move_to([xs[2], -1.95, 0])
        self.at("to boiling")
        self.play(FadeIn(bub, scale=0.5), FadeOut(l3), FadeIn(l3b), run_time=0.8)
        self.play(*[b.animate.shift(UP * 0.25) for b in bub], run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Ecto(SpokenScene):
    def construct(self):
        S = stage(chips=None)
        pc = piece(0.0, DY, 0.32, dead=True)
        raw1 = hexsheet(D1X, DY, 5, 4, CR, BLUE)
        self.play(FadeIn(S["dish1"]), FadeIn(raw1, lag_ratio=0.02), FadeIn(S["dish2"]),
                  FadeIn(S["sheet2"], lag_ratio=0.02), FadeIn(pc), run_time=0.6)
        l2a = lab("ectoderm", BLUE, 28).move_to([D2X, 3.08, 0])
        self.play(FadeIn(l2a), run_time=0.3)
        self.at("against early")
        self.play(pc.animate.move_to(S["piece"].get_center()), FadeOut(l2a), FadeIn(S["l2"]), run_time=0.8)
        self.at("gastrula ectoderm")
        self.play(FadeIn(S["hdr"], shift=DOWN * 0.1), run_time=0.4)
        self.at("On its own")
        self.play(FadeIn(S["l1"]), Indicate(raw1, color=BLUE, scale_factor=1.04), run_time=0.8)
        self.at("became skin")
        self.play(ReplacementTransform(raw1, S["skin"]), run_time=1.0)
        self.play(FadeIn(S["res1"], shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Q(SpokenScene):
    def construct(self):
        S = stage(chips="q")
        base = [S[k] for k in ("hdr", "dish1", "dish2", "l1", "l2", "skin", "res1", "sheet2", "piece")]
        self.add(*base)
        self.at("dead organizer")
        self.play(Indicate(S["piece"], color=CREAM, scale_factor=1.15), run_time=0.8)
        self.at("become neural")
        self.play(FadeIn(S["c_neural"], shift=UP * 0.15), run_time=0.6)
        self.play(*[Indicate(c, color=PURPLE, scale_factor=1.12) for c in S["sheet2"]], run_time=0.9)
        self.at("second axis")
        self.play(FadeIn(S["c_axis"], shift=UP * 0.15), run_time=0.6)
        self.finish()


class S05Pause(NarratedScene):
    def construct(self):
        S = stage(chips="q")
        self.add(*S.values())
        pr = T("Predict", 44, YELLOW, weight=BOLD).move_to([D1X, -3.45, 0])
        self.play(FadeIn(pr, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rev1(SpokenScene):
    def construct(self):
        S = stage(chips="q")
        self.add(*S.values())
        self.at("often became neural")
        sh = S["sheet2"]
        pur = [c for i, c in enumerate(sh) if i % 4 != 3]
        self.play(*recolor(pur, PURPLE), run_time=1.1)
        new_chip = stage(chips="tick", frac=True)["c_neural"]
        tk = tick(MK, CHY1)
        self.remove(S["c_neural"])
        self.add(new_chip)
        self.play(Create(tk), run_time=0.7)
        hdr2 = hdr_with_x("living organizer: not needed", CREAM, size=28)
        self.at("living organizer was not")
        self.play(FadeOut(S["hdr"]), FadeIn(hdr2), run_time=0.8)
        self.finish()


class S07Rev2(SpokenScene):
    def construct(self):
        S = stage(d2="neural", chips="tick", header="living organizer: not needed", header_color=CREAM,
                  hdr_x=True, frac=True)
        self.add(*S.values())
        hdr2 = lab("organizing did not survive", RED, 30).move_to([0, 3.62, 0])
        self.at("organizing did not survive")
        self.play(FadeOut(S["hdr"]), FadeIn(hdr2), Indicate(S["piece"], color=GREY, scale_factor=1.15), run_time=0.9)
        self.at("Killed tissue")
        self.play(Indicate(S["piece"], color=CREAM, scale_factor=1.2), run_time=0.7)
        self.at("made ectoderm neural")
        pur = [c for i, c in enumerate(S["sheet2"]) if i % 4 != 3]
        self.play(*[Indicate(c, color=PURPLE, scale_factor=1.15) for c in pur], run_time=1.0)
        self.at("without building")
        self.play(Indicate(S["c_axis"], color=TEAL, scale_factor=1.1), run_time=0.8)
        sch = schematic(-1.2, -3.25).scale(1.1)
        self.at("organized second axis")
        self.play(FadeIn(sch, shift=UP * 0.1), run_time=0.5)
        newc = stage(chips="tick", frac=True, axis_done=True)["c_axis"]
        self.play(FadeOut(S["c_axis"]), FadeIn(newc), Create(cross(MK, CHY2)), run_time=0.6)
        self.play(Indicate(newc, color=RED, scale_factor=1.05), run_time=0.6)
        self.finish()


class S08Beat(NarratedScene):
    def construct(self):
        S = stage(d2="neural", chips="cross", header="organizing did not survive", header_color=RED,
                  frac=True, axis_done=True)
        self.add(*S.values(), schematic(-1.2, -3.25).scale(1.1))
        self.finish()


# ---------------------------------------------------------------------------------------------
class S09Suff(SpokenScene):
    def construct(self):
        cards = [RoundedRectangle(corner_radius=0.3, width=6.5, height=6.8, stroke_color=GREY, stroke_width=3,
                                  fill_color=GREY, fill_opacity=0.06).move_to([x, 0, 0]) for x in (-3.5, 3.5)]
        h1 = lab("sufficient", GREEN, 58, weight=BOLD, font=TITLE_FONT).move_to([-3.5, 2.65, 0])
        h2 = lab("necessary", TEAL, 58, weight=BOLD, font=TITLE_FONT).move_to([3.5, 2.65, 0])
        fa = chip("with factor", YELLOW, 34).move_to([1.85, 1.25, 0])
        ea = chip("effect", PURPLE, 36).move_to([5.4, 1.25, 0])
        aa = arr([3.35, 1.25, 0], [4.35, 1.25, 0], GREEN, 8)
        fb = chip("without factor", GREY, 32).move_to([2.0, -0.55, 0])
        eb = chip("effect", PURPLE, 36, fill_opacity=0.05).move_to([5.4, -0.55, 0])
        eb.set_opacity(0.45)
        ab = DashedLine([3.65, -0.55, 0], [4.35, -0.55, 0], color=GREY, stroke_width=7)
        xb = cross(5.4, -0.55, 0.45)
        t2 = lab("no effect without it", TEXT, 42).move_to([3.5, -2.45, 0])
        necessary = VGroup(h2, fa, ea, aa, fb, eb, ab, xb, t2)
        # Both cards are populated early; the narration then highlights each definition.
        self.play(*[FadeIn(c) for c in cards], FadeIn(necessary), run_time=0.5)
        f1 = chip("factor", YELLOW, 38).move_to([-5.15, 1.25, 0])
        e1 = chip("effect", PURPLE, 38).move_to([-1.8, 1.25, 0])
        a1 = arr([-4.2, 1.25, 0], [-2.85, 1.25, 0], GREEN, 9)
        self.at("is sufficient")
        self.play(FadeIn(h1), FadeIn(f1), run_time=0.5)
        self.at("enough")
        self.play(GrowArrow(a1), FadeIn(e1), run_time=0.5)
        t1 = lab("enough, by itself", TEXT, 42).move_to([-3.5, -0.45, 0])
        self.at("by itself")
        self.play(FadeIn(t1), run_time=0.5)
        f1b = chip("dead organizer", CREAM, 30)
        fitw(f1b, 3.0).move_to([-4.95, -2.45, 0])
        e1b = chip("neural", PURPLE, 34).move_to([-1.65, -2.45, 0])
        a1b = arr(f1b.get_right() + RIGHT * 0.15, e1b.get_left() - RIGHT * 0.15, GREEN, 8)
        self.at("to produce")
        self.play(FadeIn(f1b), GrowArrow(a1b), FadeIn(e1b), run_time=0.7)
        self.at("is necessary")
        self.play(Indicate(h2, color=TEAL, scale_factor=1.04), run_time=0.5)
        self.at("that effect")
        self.play(Indicate(VGroup(fa, aa, ea), color=TEAL, scale_factor=1.03), run_time=0.6)
        self.at("does not")
        self.play(Indicate(VGroup(fb, ab, eb, xb), color=TEAL, scale_factor=1.03), run_time=0.6)
        self.finish()


class S10Soff(SpokenScene):
    def construct(self):
        d = piece(-4.3, 0.7, 0.65, dead=True)
        ld = lab("dead organizer", CREAM, 36).move_to([-4.3, -1.8, 0])
        self.play(FadeIn(d, scale=0.7), FadeIn(ld), run_time=0.5)
        a = arr([-2.0, 0.7, 0], [0.4, 0.7, 0], YELLOW, 9)
        en = hexsheet(3.5, 0.7, 4, 3, 0.676, BLUE)
        len_ = lab("ectoderm", BLUE, 36).move_to([3.5, -1.8, 0])
        self.at("was sufficient")
        self.play(GrowArrow(a), FadeIn(en), FadeIn(len_), run_time=0.7)
        self.at("make ectoderm neural")
        lneu = lab("neural", PURPLE, 36, weight=BOLD).move_to([3.5, -1.8, 0])
        self.play(*recolor(en, PURPLE), FadeOut(len_), FadeIn(lneu), run_time=0.8)
        suff = lab("sufficient", GREEN, 58, weight=BOLD, font=TITLE_FONT).move_to([-3.3, -2.9, 0])
        self.at("sufficient does")
        self.play(FadeIn(suff, shift=UP * 0.1), run_time=0.5)
        eq = VGroup(lab("=", TEXT, 80), Line([-0.34, -0.58, 0], [0.34, 0.58, 0], stroke_color=RED, stroke_width=10)).move_to([0.0, -2.9, 0])
        self.at("not mean")
        self.play(FadeIn(eq, scale=0.6), run_time=0.5)
        nat = lab("natural", TEXT, 58, weight=BOLD, font=TITLE_FONT).move_to([3.3, -2.9, 0])
        self.at("natural")
        self.play(FadeIn(nat, shift=UP * 0.1), run_time=0.5)
        title = table_title()
        L0, D0, C0, r0 = tparts(0)
        L1, D1, C1, r1 = tparts(1)
        self.at("Then the controls")
        self.play(FadeOut(VGroup(d, ld, a, en, lneu, suff, eq, nat)), FadeIn(title), run_time=0.45)
        self.at("controls were")
        self.play(FadeIn(r0), FadeIn(L0, shift=RIGHT * 0.2), FadeIn(D0), FadeIn(C0, scale=0.6), run_time=0.5)
        self.at("run")
        self.play(FadeIn(r1), FadeIn(L1, shift=RIGHT * 0.2), FadeIn(D1), FadeIn(C1, scale=0.6), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S11Other(SpokenScene):
    def construct(self):
        self.add(table_static(2))
        L, D, C, rule = tparts(2)
        self.at("many other killed")
        self.play(FadeIn(rule), FadeIn(L, shift=RIGHT * 0.2), run_time=0.6)
        self.at("induced too")
        self.play(FadeIn(C, scale=0.6), run_time=0.5)
        L3, D3, C3, rule3 = tparts(3)
        self.at("did ether extracts")
        self.play(FadeIn(rule3), FadeIn(L3, shift=RIGHT * 0.2), run_time=0.6)
        self.at("in the 1930s")
        self.play(FadeIn(D3, shift=UP * 0.1), FadeIn(C3, scale=0.6), run_time=0.6)
        self.finish()


class S12Unrel(SpokenScene):
    def construct(self):
        self.add(table_static(4))
        L, D, C, rule = tparts(4)
        self.at("unrelated materials")
        self.play(FadeIn(rule), FadeIn(L, shift=RIGHT * 0.2), run_time=0.6)
        self.at("from adult tissues")
        self.play(FadeIn(D, shift=UP * 0.1), run_time=0.6)
        self.at("induced in some")
        self.play(FadeIn(C, scale=0.6), run_time=0.6)
        self.finish()


class S13Amb(SpokenScene):
    def construct(self):
        self.add(table_static(5))
        L, D, C, rule = tparts(5)
        self.at("in the 1940s")
        self.play(FadeIn(rule), FadeIn(L, shift=RIGHT * 0.2), FadeIn(D, shift=UP * 0.1), run_time=0.7)
        self.at("became neural")
        self.play(FadeIn(C, scale=0.6), run_time=0.6)
        self.at("no organizer at all")
        self.play(Indicate(L, color=YELLOW, scale_factor=1.03), run_time=0.9)
        self.finish()


class S14Moral(SpokenScene):
    def construct(self):
        tab = table_static(6)
        self.add(tab)
        note, moral = moral_parts()
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.5)
        chips_ = [tparts(i)[2] for i in range(1, 6)]
        self.at("scores yes")
        self.play(*[Indicate(c, color=GREEN, scale_factor=1.12) for c in chips_], run_time=1.0)
        self.at("a yes cannot")
        self.play(FadeIn(moral, shift=UP * 0.15), run_time=0.7)
        self.finish()


class S15Beat(NarratedScene):
    def construct(self):
        note, moral = moral_parts()
        self.add(table_static(6), note, moral)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S16Trap(SpokenScene):
    def construct(self):
        sh, dots = tend_sheet(TSX, TSY)
        cred = lab("C. H. Waddington", TEXT, 38).move_to([0, 3.45, 0])
        self.at("Waddington described")
        self.play(FadeIn(sh, lag_ratio=0.01), FadeIn(cred, shift=DOWN * 0.1), run_time=0.7)
        lc = lab("competent ectoderm", BLUE, 38).move_to([0, 2.55, 0])
        self.at("competent ectoderm")
        self.play(FadeIn(lc, shift=DOWN * 0.1), run_time=0.6)
        lh = lab("a hidden tendency to become neural", PURPLE, 36).move_to([0, -3.1, 0])
        self.at("hidden tendency")
        self.play(FadeIn(dots, lag_ratio=0.02), FadeIn(lh, shift=UP * 0.1), run_time=1.0)
        self.at("to become neural")
        picks = [sh[3], sh[19], sh[28], sh[44], sh[55]]
        self.play(*recolor(picks, PURPLE), run_time=0.5)
        self.play(*recolor(picks, BLUE), run_time=0.5)
        self.finish()


class S17Inj(SpokenScene):
    def construct(self):
        left, ldots = tend_sheet(-3.5, 0, cols=6, rows=5, r=0.43)
        right, rdots = tend_sheet(3.5, 0, cols=6, rows=5, r=0.43)
        self.add(left, ldots, right, rdots)
        cl = chip("natural signal", YELLOW, 36).move_to([-3.5, 3.15, 0])
        cr = chip("injury", AMBER, 36).move_to([3.5, 3.15, 0])
        al = VGroup(*[arr([x, cl.get_bottom()[1] - 0.18, 0], [x, 2.05, 0], YELLOW, 8, 0.22)
                     for x in (-4.7, -3.5, -2.3)])
        ar = VGroup(*[arr([x, cr.get_bottom()[1] - 0.18, 0], [x, 2.05, 0], AMBER, 8, 0.22)
                     for x in (2.3, 3.5, 4.7)])
        self.at("a substance might")
        self.play(FadeIn(cl), *[GrowArrow(a) for a in al], run_time=0.8)
        c1 = lab("switches neural on", PURPLE, 32).move_to([-3.5, -2.35, 0])
        self.at("natural signal")
        self.play(*recolor(left, PURPLE), FadeOut(ldots), FadeIn(c1), run_time=0.9)
        self.at("or it might")
        self.play(Indicate(right, color=BLUE, scale_factor=1.02), run_time=0.5)
        self.at("merely injure")
        self.play(FadeIn(cr), *[GrowArrow(a) for a in ar], run_time=0.8)
        lr = fitw(lab("releases the hidden tendency", PURPLE, 32), 6.2).move_to([3.5, -2.35, 0])
        self.at("release that tendency")
        self.play(*recolor(right, PURPLE), FadeOut(rdots), FadeIn(lr), run_time=1.0)
        same = chip("same result either way", GREEN, 30).move_to([0, -3.2, 0])
        self.play(FadeIn(same), run_time=0.5)
        self.finish()


class S18Stall(SpokenScene):
    def construct(self):
        X30, X40, DEC = -5.2, -1.4, 3.0
        axis = arr([-6.4, -0.3, 0], [6.5, -0.3, 0], LIGHT, 7)
        ticks = [Line([x, -0.45, 0], [x, -0.15, 0], stroke_color=LIGHT, stroke_width=7) for x in (X30, X40, X40 + DEC, X40 + 2 * DEC)]
        l30 = lab("1930s", LIGHT, 38).move_to([X30, -0.85, 0])
        l40 = lab("1940s", LIGHT, 38).move_to([X40, -0.85, 0])
        c30 = chip("dead tissue induces", TEXT, 30).move_to([-4.7, 1.9, 0])
        s30 = Line([X30, 1.45, 0], [X30, -0.15, 0], stroke_color=GREY, stroke_width=3)
        self.play(Create(axis), *[FadeIn(t) for t in ticks], FadeIn(l30), FadeIn(l40), FadeIn(c30), Create(s30), run_time=0.3)
        c40 = chip("salamander ectoderm", YELLOW, 32, fill_opacity=0.3).move_to([0.6, 1.9, 0])
        s40 = Line([X40, 1.45, 0], [X40, -0.15, 0], stroke_color=YELLOW, stroke_width=4)
        tag = lab("one explanation", YELLOW, 28).move_to([0.6, 2.75, 0])
        self.at("salamander result", lead=0.0)
        self.play(FadeIn(c40, shift=DOWN * 0.1), Create(s40), run_time=0.7)
        self.at("one explanation")
        self.play(FadeIn(tag, shift=DOWN * 0.1), run_time=0.5)
        bar = Arrow([X40, -2.0, 0], [6.5, -2.0, 0], buff=0, color="#FF7F88", stroke_width=16, tip_length=0.35)
        lb = lab("no molecule identified", "#FF9DA5", 44, weight=BOLD).move_to([2.2, -1.25, 0])
        self.at("chemical hunt")
        self.play(GrowArrow(bar), FadeIn(lb), run_time=1.0)
        br = Brace(Line([X40, -2.0, 0], [6.0, -2.0, 0]), DOWN, color=TEXT, buff=0.15)
        ld = lab("decades ...", TEXT, 46, weight=BOLD, font=TITLE_FONT).next_to(br, DOWN, buff=0.15)
        self.at("for decades")
        self.play(FadeIn(br), FadeIn(ld, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
PX = [-3.5, 3.5]
PY_ = -0.8
PCOLS, PROWS, PR = 6, 5, 0.4


def panel_sheet(x):
    sh = hexsheet(x, PY_, PCOLS, PROWS, PR, BLUE)
    dots = VGroup(*[Dot(c.get_center(), radius=0.12, color=PURPLE).set_opacity(0.45) for c in sh])
    return sh, dots


def brake_bar(x, op=1.0):
    yb = PY_ + 2.35
    bar = Line([x - 2.7, yb, 0], [x + 2.7, yb, 0], stroke_color=RED, stroke_width=12)
    lbl = lab("brake", RED, 28).move_to([x - 1.9, yb + 0.35, 0])
    g = VGroup(bar, lbl)
    g.set_opacity(op)
    return g


SUPPOSE = "Suppose: neural is the default, held back by a brake"
FINAL_LINE = "many agents loosen the brake, so many induce"


class S19Brake(SpokenScene):
    def construct(self):
        sh, dots = tend_sheet(TSX, TSY)
        self.add(sh, dots)
        sup = fitw(lab(SUPPOSE, RED, 30), 12.4).move_to([0, -3.4, 0])
        suppose_tag = lab("Suppose", RED, 32, weight=BOLD).move_to([0, 2.5, 0])
        bar = Line([-5.9, 2.4, 0], [5.9, 2.4, 0], stroke_color=RED, stroke_width=14)
        stem = Line([0, 2.4, 0], [0, 2.95, 0], stroke_color=RED, stroke_width=7)
        cb = chip("brake", RED, 36).move_to([0, 3.4, 0])
        brake = VGroup(bar, stem, cb)
        self.play(FadeIn(sup, shift=UP * 0.1), run_time=0.4)
        self.at("neural is what")
        self.play(FadeIn(brake, shift=DOWN * 0.2), run_time=0.8)
        self.at("is released")
        self.play(brake.animate.shift(UP * 0.2).set_opacity(0.5), *recolor(sh, PURPLE), FadeOut(dots), run_time=1.0)
        panels = []
        for x in PX:
            s_, d_ = panel_sheet(x)
            panels.append((s_, d_, brake_bar(x)))
        self.at("Then", lead=0.6)
        self.play(FadeOut(brake), FadeOut(sh), FadeOut(sup), run_time=0.25)
        self.add(suppose_tag)
        self.play(*[FadeIn(VGroup(s_, d_, b_)) for s_, d_, b_ in panels], run_time=0.35)
        names = [("injury", AMBER), ("chemical", AMBER)]
        chips_, arrows = [], []
        for x, (nm, col) in zip(PX, names):
            chips_.append(chip(nm, col, 34).move_to([x, 3.4, 0]))
            arrows.append(arr([x, 3.0, 0], [x, PY_ + 2.4, 0], col, 9, 0.22))
        self.at("many injuries")
        self.play(FadeIn(chips_[0], shift=DOWN * 0.1), GrowArrow(arrows[0]), run_time=0.5)
        self.at("and chemicals")
        self.play(FadeIn(chips_[1], shift=DOWN * 0.1), GrowArrow(arrows[1]), run_time=0.5)
        self.at("weaken it")
        self.play(*[b_.animate.set_opacity(0.5) for _, _, b_ in panels], run_time=0.8)
        fl = fitw(lab(FINAL_LINE, YELLOW, 34), 12.4).move_to([0, -3.4, 0])
        self.at("be expected")
        self.play(*[a for s_, d_, _ in panels for a in recolor(s_, PURPLE)], *[FadeOut(d_) for _, d_, _ in panels],
                  run_time=0.65)
        self.play(FadeOut(suppose_tag), run_time=0.15)
        self.play(FadeIn(fl, shift=UP * 0.1), run_time=0.3)
        self.finish()


class S19bBeat(NarratedScene):
    def construct(self):
        names = [("injury", AMBER), ("chemical", AMBER)]
        for x, (nm, col) in zip(PX, names):
            s_, d_ = panel_sheet(x)
            for c in s_:
                c.set_stroke(PURPLE).set_fill(PURPLE, 0.5)
            b_ = brake_bar(x, 0.5)
            self.add(s_, b_, chip(nm, col, 34).move_to([x, 3.4, 0]), arr([x, 3.0, 0], [x, PY_ + 2.4, 0], col, 9, 0.22))
        self.add(fitw(lab(FINAL_LINE, YELLOW, 34), 12.4).move_to([0, -3.4, 0]))
        self.finish()


# ---------------------------------------------------------------------------------------------
class S20Next(SpokenScene):
    def construct(self):
        card = RoundedRectangle(corner_radius=0.4, width=12.6, height=7.0, stroke_color=TEAL, stroke_width=4,
                                fill_color=TEAL, fill_opacity=0.05).move_to([0, 0, 0])
        hd = lab("NEXT LESSON", TEAL, 32, weight=BOLD).move_to([0, 3.0, 0])
        self.at("The next lesson")
        self.play(FadeIn(card), FadeIn(hd), run_time=0.6)
        cols, rows, r = 10, 4, 0.34
        sh = hexsheet(0, 0.3, cols, rows, r, BLUE)
        lf = lab("frog ectoderm", BLUE, 36).move_to([0, 2.3, 0])
        self.at("frog ectoderm")
        self.play(FadeIn(sh, lag_ratio=0.01), FadeIn(lf), run_time=0.9)
        rng = np.random.RandomState(7)
        tgt = []
        for j in range(rows):
            for i in range(cols):
                tgt.append([-4.9 + i * 1.09 + rng.uniform(-0.18, 0.18), 1.5 - j * 0.95 + rng.uniform(-0.15, 0.15), 0])
        ls = lab("cells separated", GREY, 32).move_to([0, -2.1, 0])
        self.at("cells separated")
        self.play(*[c.animate.move_to(p) for c, p in zip(sh, tgt)], FadeIn(ls), run_time=1.3)
        ln = lab("neural", PURPLE, 36, weight=BOLD).move_to([0, 2.3, 0])
        self.at("becoming neural")
        self.play(*recolor(sh, PURPLE), ReplacementTransform(lf, ln), run_time=0.7)
        ni = chip("no inducer", RED, 36).move_to([0, -2.9, 0])
        self.at("no inducer")
        self.play(FadeOut(ls), FadeIn(ni, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S21Take(SpokenScene):
    def construct(self):
        nb = piece(-4.2, 0.6, 0.55)
        lnb = lab("neighbours", CREAM, 38, weight=BOLD).move_to([-4.2, -2.1, 0])
        self.play(FadeIn(nb, scale=0.7), FadeIn(lnb), run_time=0.5)
        cell_ = Circle(radius=1.4, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.5).move_to([4.0, 0.6, 0])
        lcell = lab("a cell that can still answer", BLUE, 32).move_to([3.4, -2.1, 0])
        a = arr([-2.3, 0.6, 0], [2.3, 0.6, 0], YELLOW, 10)
        self.at("can set")
        self.play(GrowArrow(a), FadeIn(cell_, scale=0.6), run_time=0.5)
        self.at("a cell's fate")
        self.play(cell_.animate.set_stroke(PURPLE).set_fill(PURPLE, 0.55), run_time=0.6)
        self.at("while it can still")
        self.play(FadeIn(lcell, shift=UP * 0.1), run_time=0.6)
        self.play(Indicate(cell_, color=PURPLE, scale_factor=1.08), run_time=0.8)
        q = T("?", 140, RED, weight=BOLD).move_to([0.0, 2.2, 0])
        lq = lab("what is the signal?", RED, 46, font=TITLE_FONT).move_to([0, -3.2, 0])
        self.at("What the signal")
        self.play(FadeIn(q, scale=0.4), FadeIn(lq, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S22End(EndCard):
    LINE = "A yes cannot name the signal."
    LINE2 = "Neighbours can set a cell's fate, while it can still answer."

    def construct(self):
        line = fitw(T(self.LINE, size=56, font=TITLE_FONT), 12.0)
        l2 = fitw(T(self.LINE2, size=34, font=TITLE_FONT, color=GREY), 12.0)
        sub = T("biochemistrypedia.com", size=26, color=TEAL)
        g = VGroup(line, l2, sub).arrange(DOWN, buff=0.5)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.25))
        self.play(FadeIn(l2, shift=UP * 0.1), run_time=self.beat(0.2))
        self.play(FadeIn(sub), run_time=self.beat(0.1))
        self.finish()
