"""Memory consolidation: sufficient is not necessary  (Biochemistrypedia neuroscience explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = a cell that is active (firing)
  BLUE   = blue light, and the opsin tag (the ring round a tagged cell)
  GREEN  = the behaviour or recall is present (freezing, intact recall, more recall)
  RED    = silenced cells, recall that fails
  ORANGE = likely engram candidate region (Roy and colleagues 2022)
  PURPLE = a control group
  GOLD   = the open question
  GREY   = cells at rest, boxes, outlines, de-emphasized
All drawings are boxes, cells, rings, arrows and counts. No brain section, no slice, no molecule.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def bar_end(a, b, color=RED, w=5):
    """inhibition: a line ending in a bar"""
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.06
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w), Line(b + perp * 0.22, b - perp * 0.22, color=color, stroke_width=w + 1))


def box(w, h, center, label=None, color=GREY, size=24, label_pos="out"):
    r = RoundedRectangle(corner_radius=0.18, width=w, height=h, stroke_color=color, stroke_width=3,
                         fill_color=color, fill_opacity=0.06).move_to(center)
    g = VGroup(r)
    if label:
        t = T(label, size, color)
        if label_pos == "out":
            t.next_to(r, UP, buff=0.14).align_to(r, LEFT)
        else:
            t.move_to(r.get_top() + DOWN * 0.3)
        g.add(t)
    g.rect = r
    return g


def cell(p, r=0.26):
    p = np.array([p[0], p[1], 0.0])
    soma = Circle(radius=r, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.25).move_to(p)
    stubs = VGroup()
    for ang in (100, 215, 325):
        d = np.array([np.cos(np.radians(ang)), np.sin(np.radians(ang)), 0])
        stubs.add(Line(p + d * r, p + d * (r + 0.17), stroke_color=GREY, stroke_width=3))
    g = VGroup(soma, stubs)
    g.soma, g.stubs, g.p = soma, stubs, p
    return g


def ring(c, color=BLUE, k=1.62):
    return Circle(radius=c.soma.width / 2 * k, stroke_color=color, stroke_width=4, fill_opacity=0).move_to(c.p)


def st(c, s):
    """animations that put a cell in a state: idle, active, silent"""
    col, fo = {"idle": (GREY, 0.25), "active": (YELLOW, 0.85), "silent": (RED, 0.1)}[s]
    return [c.soma.animate.set_stroke(col).set_fill(col, fo), c.stubs.animate.set_stroke(col, opacity=1.0 if s != "silent" else 0.5)]


def setst(c, s):
    col, fo = {"idle": (GREY, 0.25), "active": (YELLOW, 0.85), "silent": (RED, 0.1)}[s]
    c.soma.set_stroke(col).set_fill(col, fo)
    c.stubs.set_stroke(col, opacity=1.0 if s != "silent" else 0.5)


def scatter(n, x0, x1, y0, y1, seed, dmin, rows=2):
    """n cells on a jittered, staggered grid inside the rectangle (rows x cols)"""
    rs = np.random.RandomState(seed)
    cols = -(-n // rows)
    pts = []
    for r in range(rows):
        for c in range(cols):
            if len(pts) == n:
                break
            fx = (c + (0.5 if r % 2 else 0.0)) / max(cols - 0.5, 1)
            fy = r / max(rows - 1, 1)
            q = np.array([x0 + fx * (x1 - x0) + rs.uniform(-0.12, 0.12), y0 + fy * (y1 - y0) + rs.uniform(-0.1, 0.1)])
            pts.append(q)
    return pts


def lighten(m):
    return m

# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Plasticity, networks and consolidation"
    TITLE = "Sufficient is not necessary"


# ---------------------------------------------------------------------------------------------
class S01Freeze(SpokenScene):
    """cells in the dentate gyrus lit by blue light -> mouse freezes in a different box -> was the memory found?"""

    def construct(self):
        dg = box(9.0, 3.4, [0, 1.15, 0], "dentate gyrus of the mouse")
        pts = scatter(12, -3.7, 3.4, 0.15, 2.1, 7, 1.0, rows=2)
        cells = [cell(p, 0.3) for p in pts]
        tagged = [0, 2, 5, 7, 10]
        rings = [ring(cells[i], BLUE, 1.55) for i in tagged]
        self.at("Shine blue light")
        self.play(FadeIn(dg), *[FadeIn(c) for c in cells], run_time=0.8)
        self.play(*[Create(r) for r in rings], run_time=0.5)
        light = arr([6.25, 1.15, 0], [4.65, 1.15, 0], BLUE, 7)
        light_l = T("blue light", 24, BLUE).next_to(light, UP, buff=0.12)
        self.play(GrowArrow(light), FadeIn(light_l), run_time=0.4)
        state = chip("mouse: moving", GREY, 28).move_to([0, -2.4, 0])
        self.play(FadeIn(state), *sum([st(cells[i], "active") for i in tagged], []), run_time=0.4)
        self.at("freezes")
        frz = chip("mouse: FREEZING", GREEN, 28).move_to(state)
        self.play(ReplacementTransform(state, frz), run_time=0.5)
        self.at("tagged while")
        self.play(FadeOut(light), FadeOut(light_l), *sum([st(cells[i], "idle") for i in tagged], []), run_time=0.4)
        bxa = box(4.6, 1.8, [-3.9, -2.4, 0])
        la = T("Box A: fear learned here", 24, GREY).move_to(bxa.rect.get_top() + DOWN * 0.4)
        self.play(FadeOut(frz), FadeIn(bxa), FadeIn(la), run_time=0.5)
        tg = T("tagged while it learned", 24, BLUE).move_to([0.6, -1.15, 0])
        ar = arr([-3.2, -1.5, 0], [-2.7, -0.6, 0], BLUE)
        self.play(GrowArrow(ar), FadeIn(tg), *sum([st(cells[i], "active") for i in tagged], []), run_time=0.5)
        self.at("different box")
        self.play(FadeOut(ar), FadeOut(tg), *sum([st(cells[i], "idle") for i in tagged], []), run_time=0.3)
        bxb = box(4.6, 1.8, [3.9, -2.4, 0])
        lb = T("Box B: a different box", 24, GREY).move_to(bxb.rect.get_top() + DOWN * 0.4)
        mouse_b = chip("mouse: FREEZING", GREEN, 24).move_to([3.9, -2.75, 0])
        light2 = arr([6.25, 1.15, 0], [4.65, 1.15, 0], BLUE, 7)
        light2_l = T("blue light", 24, BLUE).next_to(light2, UP, buff=0.12)
        self.play(FadeIn(bxb), FadeIn(lb), FadeIn(light2), FadeIn(light2_l), run_time=0.4)
        self.play(FadeIn(mouse_b), *sum([st(cells[i], "active") for i in tagged], []), run_time=0.4)
        self.at("found where the memory")
        q = T("Was the memory found?", 40, GOLD, font=TITLE_FONT).move_to([0, -2.4, 0])
        self.play(FadeOut(bxa), FadeOut(la), FadeOut(bxb), FadeOut(lb), FadeOut(mouse_b), FadeOut(light2), FadeOut(light2_l), run_time=0.4)
        self.play(FadeIn(q, shift=UP * 0.15), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Tag(SpokenScene):
    """active cells -> c-fos on -> opsin ring -> doxycycline window -> light lights only the ringed cells."""

    def construct(self):
        dg = box(11.6, 4.3, [0, 0.2, 0], "dentate gyrus of the mouse")
        pts = scatter(20, -4.8, 4.2, -1.45, 1.45, 11, 1.4, rows=4)
        cells = [cell(p, 0.3) for p in pts]
        tagged = [1, 3, 6, 9, 12, 15, 18]
        self.play(FadeIn(dg), *[FadeIn(c) for c in cells], run_time=0.8)
        self.at("recently active neurons")
        fos = chip("c-fos switched on", YELLOW, 24).move_to([4.2, 2.75, 0])
        self.play(FadeIn(fos), *sum([st(cells[i], "active") for i in tagged], []), run_time=0.6)
        self.at("put an opsin")
        rings = [ring(cells[i], BLUE, 1.6) for i in tagged]
        ops = chip("opsin in these cells", BLUE, 24).move_to([4.2, 2.75, 0])
        self.play(ReplacementTransform(fos, ops), *[Create(r) for r in rings], run_time=0.7)
        self.at("active during learning")
        self.wait(0.3)
        self.play(*sum([st(cells[i], "idle") for i in tagged], []), run_time=0.4)
        self.at("off a drug")
        seg = []
        spec = [("on", 3.0, GREY), ("off: tagging window", 4.4, YELLOW), ("on again", 3.0, GREY)]
        x = -5.4
        for lab, w, col in spec:
            r = RoundedRectangle(corner_radius=0.1, width=w - 0.1, height=0.5, stroke_color=col, stroke_width=3,
                                 fill_color=col, fill_opacity=0.18).move_to([x + w / 2, -3.3, 0])
            t = T(lab, 22, col).move_to(r)
            seg.append(VGroup(r, t))
            x += w
        dlab = T("doxycycline", 22, GREY).move_to([-4.4, -2.7, 0])
        self.play(*[FadeIn(s) for s in seg], FadeIn(dlab), run_time=0.7)
        self.at("restricted the tagging")
        self.play(Indicate(seg[1][0], color=YELLOW, scale_factor=1.05), run_time=0.8)
        self.at("switches on just those cells")
        lt = chip("blue light", BLUE, 24).move_to([0.2, 2.75, 0])
        glow = Rectangle(width=11.6, height=4.3, stroke_color=BLUE, stroke_width=5, fill_opacity=0).move_to(dg.rect)
        self.play(FadeIn(lt), Create(glow), run_time=0.5)
        self.play(*sum([st(cells[i], "active") for i in tagged], []), run_time=0.5)
        only = T("only the tagged cells", 24, YELLOW).move_to([4.0, -2.7, 0])
        self.play(FadeIn(only), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Enough(SpokenScene):
    """test row and two control rows; 20 Hz note; sufficiency."""

    def construct(self):
        ys = [2.2, 0.6, -1.0]
        conds = [("fear-tagged, with opsin", BLUE), ("tagged in a neutral context", PURPLE),
                 ("fluorescent protein, no opsin", PURPLE)]
        res = [("FREEZING in a different context", GREEN), ("no fear freezing", GREY), ("no freezing to light", GREY)]
        rows = []
        for y, (ct, cc), (rt, rc) in zip(ys, conds, res):
            c = chip(ct, cc, 24).move_to([0, y, 0]).align_to([-6.2, 0, 0], LEFT)
            a = arr([-0.6, y, 0], [0.7, y, 0], BLUE, 6)
            al = T("light", 22, BLUE).next_to(a, UP, buff=0.06)
            r = chip(rt, rc, 24).move_to([0, y, 0]).align_to([1.0, 0, 0], LEFT)
            rows.append((c, a, al, r))
        self.at("light on those cells")
        self.play(FadeIn(rows[0][0]), GrowArrow(rows[0][1]), FadeIn(rows[0][2]), run_time=0.7)
        self.at("freeze")
        self.play(FadeIn(rows[0][3]), run_time=0.5)
        self.at("Two controls")
        ctl = T("controls", 24, PURPLE).move_to([-5.45, 1.4, 0])
        self.play(FadeIn(ctl), run_time=0.3)
        self.at("neutral context")
        self.play(FadeIn(rows[1][0]), GrowArrow(rows[1][1]), FadeIn(rows[1][2]), run_time=0.5)
        self.play(FadeIn(rows[1][3]), run_time=0.4)
        self.at("fluorescent protein")
        self.play(FadeIn(rows[2][0]), GrowArrow(rows[2][1]), FadeIn(rows[2][2]), run_time=0.5)
        self.play(FadeIn(rows[2][3]), run_time=0.4)
        self.at("pulses were")
        note = T("20 Hz pulses: the tool, not the cells' natural firing", 24, GREY).move_to([0, -2.2, 0])
        self.play(FadeIn(note), run_time=0.5)
        self.at("enough to produce")
        self.play(FadeOut(ctl), Indicate(rows[0][3], color=GREEN, scale_factor=1.06), run_time=0.8)
        self.at("sufficiency")
        suf = T("SUFFICIENCY, in this preparation", 38, GREEN, weight=BOLD).move_to([0, -3.1, 0])
        self.play(FadeIn(suf, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Needed(SpokenScene):
    """sufficient (cells ON) vs needed (cells OFF at natural recall); prefrontal cells silenced on day 2 and day 12."""

    def construct(self):
        suf = chip("cells ON gives freezing:\nsufficient", GREEN, 30).move_to([-3.4, 0.5, 0])
        self.at("not the same")
        self.play(FadeIn(suf), run_time=0.5)
        self.at("Necessity needs")
        nec = chip("cells OFF at natural recall:\nneeded?", GOLD, 30).move_to([3.4, 0.5, 0])
        self.play(FadeIn(nec), run_time=0.5)
        pans, cl, rg, lbl = [], {}, {}, {}
        X = {0: -3.2, 1: 3.2}
        for k, day in ((0, "Day 2"), (1, "Day 12")):
            x = X[k]
            b = box(5.8, 4.5, [x, -0.65, 0])
            t = T(day, 34, TEXT, weight=BOLD).move_to([x, 1.15, 0])
            sub = T("prefrontal cells in mice", 22, GREY).move_to([x, 0.62, 0])
            pans.append(VGroup(b, t, sub))
            cl[k] = [cell([x - 2.0 + 1.0 * i, -0.5 + (0.26 if i % 2 else -0.06)], 0.36) for i in range(5)]
        self.at("colleagues tagged")
        self.play(suf.animate.scale(0.75).move_to([-3.2, 3.05, 0]), nec.animate.scale(0.75).move_to([3.2, 3.05, 0]), run_time=0.5)
        self.play(*[FadeIn(p) for p in pans], *[FadeIn(c) for k in cl for c in cl[k]], run_time=0.7)
        for k in cl:
            rg[k] = [ring(c, BLUE, 1.5) for c in cl[k]]
            lbl[k] = T("tagged at learning", 24, BLUE).move_to([X[k], -1.5, 0])
        self.at("in mice at learning")
        self.play(*[Create(r) for k in rg for r in rg[k]], *[FadeIn(lbl[k]) for k in lbl], run_time=0.6)
        self.at("them later")
        sils = {k: T("silenced", 24, RED).move_to([X[k], -1.5, 0]) for k in cl}
        self.play(*[r.animate.set_stroke(RED) for k in rg for r in rg[k]],
                  *sum([st(c, "silent") for k in cl for c in cl[k]], []),
                  *[ReplacementTransform(lbl[k], sils[k]) for k in lbl], run_time=0.7)
        self.at("failed on")
        r12 = chip("natural cue recall fails", RED, 24).move_to([3.2, -2.4, 0])
        self.play(FadeIn(r12, shift=UP * 0.1), run_time=0.5)
        self.at("did not fail")
        r2 = chip("natural cue recall intact", GREEN, 24).move_to([-3.2, -2.4, 0])
        self.play(FadeIn(r2, shift=UP * 0.1), run_time=0.5)
        self.at("the later delay")
        self.play(Indicate(r12, color=RED, scale_factor=1.08), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Where(SpokenScene):
    """247 squares, one per region; 117 turn orange; one ensemble versus several together."""

    def construct(self):
        cols, rows_, pitch, side = 19, 13, 0.38, 0.3
        x0, y0 = -6.1 + side / 2, 2.35
        sq = []
        for j in range(rows_):
            for i in range(cols):
                s = Square(side_length=side, stroke_color=GREY, stroke_width=1.5, fill_color=GREY, fill_opacity=0.18)
                s.move_to([x0 + i * pitch, y0 - j * pitch, 0])
                sq.append(s)
        assert len(sq) == 247
        hdr = T("each square is one mouse brain region (not a map)", 22, GREY).move_to([-2.5, 3.0, 0])
        self.at("mapped learning activated cells")
        self.play(LaggedStart(*[FadeIn(s) for s in sq], lag_ratio=0.004), FadeIn(hdr), run_time=1.6)
        n247 = T("247 regions", 40, TEXT, weight=BOLD).move_to([3.95, 2.2, 0])
        self.play(FadeIn(n247), run_time=0.4)
        self.at("flagged")
        rs = np.random.RandomState(3)
        pick = set(rs.choice(247, 117, replace=False).tolist())
        assert len(pick) == 117
        n117 = T("117", 64, ORANGE, weight=BOLD).move_to([2.7, 0.9, 0])
        txt = T("likely engram\ncandidates", 24, ORANGE).move_to([5.1, 0.9, 0])
        self.play(*[sq[i].animate.set_stroke(ORANGE).set_fill(ORANGE, 0.8) for i in sorted(pick)], run_time=1.0)
        self.play(FadeIn(n117), FadeIn(txt), run_time=0.5)
        self.at("Reactivating several")
        one = chip("one\nensemble", GREY, 24).move_to([2.85, -0.75, 0])
        a1 = arr([2.85, -1.3, 0], [2.85, -1.75, 0], GREY)
        r1 = chip("recall", GREEN, 24).move_to([2.85, -2.3, 0])
        self.play(FadeIn(one), FadeIn(a1), FadeIn(r1), run_time=0.6)
        sev = chip("several\ntogether", GREY, 24).move_to([5.25, -0.75, 0])
        a2 = arr([5.25, -1.3, 0], [5.25, -1.75, 0], GREEN, 8)
        r2 = chip("more recall", GREEN, 24).move_to([5.25, -2.3, 0])
        self.at("together gave")
        self.play(FadeIn(sev), GrowArrow(a2), FadeIn(r2), run_time=0.6)
        self.at("more than one answer")
        ans = T("Where is the memory? More than one answer?", 28, GOLD).move_to([-1.6, -3.1, 0])
        self.play(FadeIn(ans, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """sufficient (light drives freezing) is not needed (silence breaks recall); the bounds of the claim."""

    def construct(self):
        X = (-3.5, 3.5)
        hl = T("Sufficient?", 36, GREEN, weight=BOLD).move_to([X[0], 3.05, 0])
        hr = T("Needed?", 36, RED, weight=BOLD).move_to([X[1], 3.05, 0])
        cl = cell([X[0], 0.55], 0.4)
        rl = ring(cl, BLUE, 1.5)
        cr = cell([X[1], 0.55], 0.4)
        rr = ring(cr, BLUE, 1.5)
        lt = chip("light on", BLUE, 28).move_to([X[0], 2.15, 0])
        la = arr([X[0], 1.75, 0], [X[0], 1.15, 0], BLUE, 6)
        lfa = arr([X[0], -0.05, 0], [X[0], -0.65, 0], YELLOW, 6)
        lf = chip("freezing", GREEN, 28).move_to([X[0], -1.1, 0])
        sl = chip("silenced during natural recall", RED, 24).move_to([X[1], 2.15, 0])
        sa = bar_end([X[1], 1.78, 0], [X[1], 1.15, 0], RED, 6)
        rfa = arr([X[1], -0.05, 0], [X[1], -0.65, 0], RED, 6)
        rf = chip("recall fails", RED, 28).move_to([X[1], -1.1, 0])
        setst(cl, "idle")
        self.at("triggers freezing")
        self.play(FadeIn(hl), FadeIn(cl), FadeIn(rl), FadeIn(lt), GrowArrow(la), run_time=0.7)
        self.play(*st(cl, "active"), GrowArrow(lfa), FadeIn(lf), run_time=0.6)
        self.at("sufficiency")
        self.play(Indicate(lf, color=GREEN, scale_factor=1.08), run_time=0.7)
        self.at("Necessity needs silencing")
        setst(cr, "idle")
        self.play(FadeIn(hr), FadeIn(cr), FadeIn(rr), FadeIn(sl), Create(sa), run_time=0.7)
        self.play(*st(cr, "silent"), rr.animate.set_stroke(RED), GrowArrow(rfa), FadeIn(rf), run_time=0.6)
        self.at("not human memory")
        neq = T("\u2260", 64, TEXT, weight=BOLD).move_to([0, 0.55, 0])
        bnd = chip("mouse contextual fear, over days", GREY, 26).move_to([0, -2.35, 0])
        self.play(FadeIn(neq), run_time=0.4)
        self.play(FadeIn(bnd, shift=UP * 0.1), run_time=0.5)
        self.at("Ask which control")
        c1 = chip("control: fluorescent protein only", PURPLE, 22).move_to([-3.4, -3.25, 0])
        c2 = chip("control: neutral-context tag", PURPLE, 22).move_to([3.6, -3.25, 0])
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "Sufficiency is not necessity. Ask which control each claim needs."
