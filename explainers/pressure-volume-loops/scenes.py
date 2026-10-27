"""Pressure-volume loops: where the two lines meet  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.
Every number on screen is the lesson's own: the made-up model adult left ventricle of worked problem
parts 1 and 3 (EDV 125 mL, V0 5 mL, Ees 3.0 mmHg per mL, Ea 1.5 mmHg per mL, heart rate not shown) and
its three moves (afterload up Ea 2.0; preload up EDV 140 mL; contractility up Ees 4.5). The lines are
computed from SV = (EDV - V0) / (1 + Ea / Ees), Pes = Ea x SV, ESV = EDV - SV. The loop's corner values
(80 mmHg aortic opening, 120 mmHg end-systolic pressure, about 10 mmHg mitral closure) are the lesson's;
the ejection and filling curves between corners are a sketch and are marked "shape not to scale".

COLOR MAP (one color per concept, whole video)
  BLUE   = the loop (one beat of the left ventricle)
  TEAL   = filling: end-diastolic volume, preload
  GREEN  = the end-systolic line (ESPVR), Ees, contractility
  ORANGE = the arterial line, Ea, afterload, the tightening arteries
  YELLOW = the end-systolic corner and the numbers read off it (ESV, Pes, SV), and what changes
  GREY   = axes, ghosts of the baseline, hedges
  TEXT   = labels and values that did not change
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"

# ---------------------------------------------------------------------------------------------
# geometry: x = volume (mL), y = pressure (mmHg); the plot sits left, a readout panel right
# ---------------------------------------------------------------------------------------------
X0, SX = -5.2, 0.052
Y0, SY = -2.5, 0.034
V0 = 5.0
PX_L, PX_R = 2.95, 6.2     # readout panel


def PT(v, p):
    return np.array([X0 + v * SX, Y0 + p * SY, 0.0])


A_ = (125, 10)   # mitral valve closes (end-diastolic volume)
B_ = (125, 80)   # aortic valve opens
C_ = (45, 120)   # aortic valve closes (end-systolic corner)
D_ = (45, 5)     # mitral valve opens


def _curve(f, n=48):
    m = VMobject()
    m.set_points_smoothly([f(i / (n - 1)) for i in range(n)])
    return m


def f_ab(s): return PT(125, 10 + 70 * s)
def f_bc(s): return PT(125 - 80 * s, 80 + 40 * (1 - (1 - s) ** 2))
def f_cd(s): return PT(45, 120 - 115 * s)
def f_da(s): return PT(45 + 80 * s, 5 + 5 * s ** 3)


def loop_segs():
    segs = [_curve(f_ab, 6), _curve(f_bc), _curve(f_cd, 6), _curve(f_da)]
    for s in segs:
        s.set_stroke(BLUE, 6)
        s.set_fill(opacity=0)
    return segs


def loop_fill():
    pts = []
    for f in (f_ab, f_bc, f_cd, f_da):
        pts += [f(i / 30) for i in range(31)]
    return Polygon(*pts, stroke_width=0, fill_color=BLUE, fill_opacity=0.25)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def btext(text, size=22, color=GREY, **kw):
    t = T(text, size, color, **kw)
    back = Rectangle(width=t.width + 0.16, height=t.height + 0.1, stroke_width=0, fill_color=BG, fill_opacity=0.85).move_to(t)
    return VGroup(back, t)


def caption_line():
    return T("model ventricle at rest: made-up numbers, shape not to scale", 22, GREY).move_to([0, 3.3, 0])


def axes_group():
    g = VGroup()
    g.add(Line(PT(0, 0), PT(150, 0), color=GREY, stroke_width=3))
    g.add(Line(PT(0, 0), PT(0, 160), color=GREY, stroke_width=3))
    g.add(T("left ventricular volume (mL)", 22, GREY).move_to([-1.2, -3.47, 0]))
    g.add(T("left ventricular pressure (mmHg)", 22, GREY).rotate(PI / 2).move_to([-6.12, 0.15, 0]))
    return g


# ---------------------------------------------------------------------------------------------
# the model and everything read off it
# ---------------------------------------------------------------------------------------------
def solve(edv, ees, ea):
    sv = (edv - V0) / (1 + ea / ees)
    pes = ea * sv
    esv = edv - sv
    return dict(edv=edv, ees=ees, ea=ea, sv=sv, pes=pes, esv=esv, ef=sv / edv)


BASE = (125, 3.0, 1.5)
AFT = (125, 3.0, 2.0)
PRE = (140, 3.0, 1.5)
CON = (125, 4.5, 1.5)


def state(edv, ees, ea):
    m = solve(edv, ees, ea)
    esv, pes = m["esv"], m["pes"]
    d = {}
    d["espvr"] = Line(PT(V0, 0), PT(V0 + 150 / ees, 150), color=GREEN, stroke_width=6)
    d["ealine"] = Line(PT(edv, 0), PT(esv, pes), color=ORANGE, stroke_width=6)
    d["gv"] = Line(PT(esv, pes), PT(esv, 0), color=YELLOW, stroke_width=3).set_opacity(0.7)
    d["gh"] = Line(PT(esv, pes), PT(0, pes), color=YELLOW, stroke_width=3).set_opacity(0.7)
    d["corner"] = Dot(PT(esv, pes), radius=0.15, color=YELLOW)
    d["edvdot"] = Dot(PT(edv, 0), radius=0.1, color=TEAL)
    d["edvlbl"] = M(f"{edv:g}", 22, TEAL).move_to(PT(edv, 0) + DOWN * 0.55)
    d["esvlbl"] = M(f"{esv:.0f}", 22, YELLOW).move_to(PT(esv, 0) + DOWN * 0.55)
    d["peslbl"] = M(f"{pes:.0f}", 22, YELLOW).move_to(PT(0, pes) + LEFT * 0.38)
    d["sv"] = DoubleArrow(PT(esv, 0) + DOWN * 0.17, PT(edv, 0) + DOWN * 0.17, buff=0, color=YELLOW, stroke_width=4,
                          tip_length=0.15, max_tip_length_to_length_ratio=0.5)
    return d


GEOM = ["espvr", "ealine", "gv", "gh", "corner", "edvdot", "sv"]
LBLS = ["edvlbl", "esvlbl", "peslbl"]


def dim_anims(m, o):
    return [m["loop"].animate.set_stroke(opacity=o), m["dots"].animate.set_opacity(o), m["y80"].animate.set_opacity(o)]


def morph(cur, new, keys=None, rt=1.4):
    """animations that carry the live objects in `cur` to the state `new` (labels are replaced)."""
    anims = []
    for k in (keys or GEOM + LBLS):
        if k in LBLS:
            anims.append(ReplacementTransform(cur[k], new[k]))
            cur[k] = new[k]
        else:
            anims.append(Transform(cur[k], new[k]))
    return anims


# ---------------------------------------------------------------------------------------------
# readout panel
# ---------------------------------------------------------------------------------------------
ROWS = [("EDV", TEAL, 2.2), ("Ees", GREEN, 1.65), ("Ea", ORANGE, 1.1),
        ("Pes", TEXT, 0.2), ("ESV", TEXT, -0.35), ("SV", TEXT, -0.9), ("EF", TEXT, -1.45)]


def strings(edv, ees, ea):
    m = solve(edv, ees, ea)
    ef = f"{m['ef'] * 100:.1f}".rstrip("0").rstrip(".")
    return dict(EDV=f"{edv:g} mL", Ees=f"{ees:.1f} mmHg/mL", Ea=f"{ea:.1f} mmHg/mL",
                Pes=f"{m['pes']:.0f} mmHg", ESV=f"{m['esv']:.0f} mL", SV=f"{m['sv']:.0f} mL", EF=f"{ef} %")


def panel_val(name, text, color, y):
    return M(text, 24, color).move_to([PX_R, y, 0], aligned_edge=RIGHT)


def panel_labels():
    g = VGroup()
    for name, col, y in ROWS:
        g.add(T(name, 24, col).move_to([PX_L, y, 0], aligned_edge=LEFT))
    g.add(Line([PX_L, 0.68, 0], [PX_R, 0.68, 0], color=GREY, stroke_width=2))
    return g


def row_color(name, base_txt, txt, col):
    if txt == base_txt:
        return TEXT
    return YELLOW if name in ("Pes", "ESV", "SV", "EF") else col


def panel_vals(s, base_s=None):
    base_s = base_s or strings(*BASE)
    vals = {}
    for name, col, y in ROWS:
        vals[name] = panel_val(name, s[name], row_color(name, base_s[name], s[name], col), y)
    return vals


def case_title(text, color):
    return T(text, 26, color).move_to([(PX_L + PX_R) / 2, 2.85, 0])


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "The cardiac cycle and pressure-volume loops"
    TITLE = "Where the two lines meet"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    """axes, a dot traces the loop, four corners with question marks, arteries tighten: which corner moves?"""

    def construct(self):
        cap = caption_line()
        ax = axes_group()
        self.play(FadeIn(cap), Create(ax[0]), Create(ax[1]), FadeIn(ax[2]), FadeIn(ax[3]), run_time=1.2)
        segs = loop_segs()
        dot = Dot(PT(*A_), radius=0.13, color=TEXT)
        self.at("closed loop")
        self.add(dot)
        for sg in segs:
            self.play(MoveAlongPath(dot, sg), Create(sg), run_time=0.7, rate_func=linear)
        self.play(FadeOut(dot), run_time=0.2)

        self.at("four corners")
        spots = [(A_, RIGHT * 0.42), (B_, RIGHT * 0.42), (C_, UP * 0.42), (D_, LEFT * 0.42)]
        dots, qs = [], []
        for (v, p), off in spots:
            dd = Dot(PT(v, p), radius=0.1, color=BLUE)
            q = T("?", 36, YELLOW, weight=BOLD).move_to(PT(v, p) + off)
            dots.append(dd)
            qs.append(q)
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.2),
                  LaggedStart(*[FadeIn(q, scale=0.5) for q in qs], lag_ratio=0.2), run_time=1.3)

        self.at("arteries tighten")
        tube = VGroup(Line([3.4, 0.45, 0], [6.1, 0.45, 0], color=ORANGE, stroke_width=6),
                      Line([3.4, -0.45, 0], [6.1, -0.45, 0], color=ORANGE, stroke_width=6))
        up = arr([4.75, 1.7, 0], [4.75, 0.62, 0], ORANGE, w=7)
        dn = arr([4.75, -1.7, 0], [4.75, -0.62, 0], ORANGE, w=7)
        lab = T("arteries tighten", 28, ORANGE).move_to([4.75, -2.3, 0])
        self.play(Create(tube), FadeIn(lab), GrowArrow(up), GrowArrow(dn), run_time=0.6)
        self.play(tube[0].animate.shift(DOWN * 0.18), tube[1].animate.shift(UP * 0.18), run_time=0.5)

        self.at("which corner")
        self.play(*[Indicate(q, color=YELLOW, scale_factor=1.5) for q in qs], run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Corners(SpokenScene):
    """a dot runs the loop counterclockwise; each corner's question mark becomes its valve event."""

    def construct(self):
        cap = caption_line()
        ax = axes_group()
        segs = loop_segs()
        loop = VGroup(*segs)
        spots = [(A_, RIGHT * 0.42), (B_, RIGHT * 0.42), (C_, UP * 0.42), (D_, LEFT * 0.42)]
        dots = VGroup(*[Dot(PT(v, p), radius=0.1, color=BLUE) for (v, p), _ in spots])
        qs = VGroup(*[T("?", 36, YELLOW, weight=BOLD).move_to(PT(v, p) + off) for (v, p), off in spots])
        tube = VGroup(Line([3.4, 0.27, 0], [6.1, 0.27, 0], color=ORANGE, stroke_width=6),
                      Line([3.4, -0.27, 0], [6.1, -0.27, 0], color=ORANGE, stroke_width=6))
        lab = T("arteries tighten", 28, ORANGE).move_to([4.75, -2.3, 0])
        self.add(cap, ax, loop, dots, qs, tube, lab)

        # the beat, counterclockwise
        self.at("counterclockwise")
        self.play(FadeOut(tube), FadeOut(lab), loop.animate.set_stroke(opacity=0.3), run_time=0.7)
        runner = Dot(PT(*D_), radius=0.14, color=TEXT)
        bright = [s.copy().set_stroke(BLUE, 8, opacity=1) for s in segs]
        # 1 -> 2: bottom right = mitral valve closes
        self.at("bottom right")
        runner.move_to(PT(*A_))
        self.play(FadeIn(runner, scale=0.5), run_time=0.4)
        lab_a = btext("mitral valve closes", 22, TEXT).move_to(PT(*A_) + RIGHT * 2.2)
        self.at("mitral valve closes")
        self.play(FadeOut(qs[0]), FadeIn(lab_a), run_time=0.4)
        edv_dot = Dot(PT(125, 0), radius=0.1, color=TEAL)
        edv_lbl = M("125", 22, TEAL).move_to(PT(125, 0) + DOWN * 0.55)
        self.at("end diastolic volume")
        self.play(FadeIn(edv_dot, scale=0.5), FadeIn(edv_lbl, shift=UP * 0.1), run_time=0.5)
        self.at("rises")
        self.play(MoveAlongPath(runner, segs[0]), Create(bright[0]), run_time=1.0, rate_func=linear)
        lab_b = btext("aortic valve opens", 22, TEXT).move_to(PT(*B_) + RIGHT * 2.2)
        y80 = M("80", 22, TEXT).move_to(PT(0, 80) + LEFT * 0.38)
        self.at("aortic valve opens")
        self.play(FadeOut(qs[1]), FadeIn(lab_b), FadeIn(y80), run_time=0.4)
        self.at("ejects")
        self.play(MoveAlongPath(runner, segs[1]), Create(bright[1]), run_time=1.3, rate_func=linear)
        lab_c = btext("aortic valve closes", 22, TEXT).move_to(PT(*C_) + RIGHT * 1.6 + DOWN * 0.9)
        self.at("aortic valve closes")
        self.play(FadeOut(qs[2]), FadeIn(lab_c), run_time=0.4)
        st = state(*BASE)
        self.at("end systolic volume")
        self.play(FadeIn(st["gv"]), FadeIn(st["esvlbl"], shift=UP * 0.1), FadeIn(st["corner"], scale=0.5), run_time=0.6)
        self.at("of mercury", nth=1)
        self.play(FadeIn(st["gh"]), FadeIn(st["peslbl"], shift=RIGHT * 0.1), run_time=0.5)
        self.at("then falls")
        self.play(MoveAlongPath(runner, segs[2]), Create(bright[2]), run_time=1.0, rate_func=linear)
        lab_d = btext("mitral valve opens", 22, TEXT).move_to(PT(*D_) + RIGHT * 1.6 + UP * 0.5)
        self.at("mitral valve opens")
        self.play(FadeOut(qs[3]), FadeIn(lab_d), run_time=0.4)
        self.at("fills")
        self.play(MoveAlongPath(runner, segs[3]), Create(bright[3]), run_time=1.2, rate_func=linear)
        self.play(FadeOut(runner), FadeOut(VGroup(*bright)), loop.animate.set_stroke(opacity=1),
                  FadeOut(VGroup(lab_a, lab_b, lab_c, lab_d)), run_time=0.8)
        self.finish()


def carried(scene, with_labels=True):
    """the model as it stands at the end of scene 2: loop, corner dots, markers; returns the live parts."""
    cap = caption_line()
    ax = axes_group()
    loop = VGroup(*loop_segs())
    dots = VGroup(*[Dot(PT(v, p), radius=0.1, color=BLUE) for (v, p) in (A_, B_, D_)])
    st = state(*BASE)
    y80 = M("80", 22, TEXT).move_to(PT(0, 80) + LEFT * 0.38)
    scene.add(cap, ax, loop, dots, st["gv"], st["gh"], st["corner"], st["edvdot"], st["edvlbl"], st["esvlbl"],
              st["peslbl"], y80)
    return dict(cap=cap, ax=ax, loop=loop, dots=dots, st=st, y80=y80)


# ---------------------------------------------------------------------------------------------
class S03Width(SpokenScene):
    """width = stroke volume (a yellow arrow under the axis), the sums, then the area fills as stroke work."""

    def construct(self):
        c = carried(self)
        st = c["st"]
        self.at("stroke volume")
        self.play(GrowFromCenter(st["sv"]), run_time=0.7)
        t1 = T("stroke volume", 26, YELLOW).move_to([4.6, 1.9, 0])
        e1 = M("125 - 45 = 80 mL", 25, TEXT).move_to([4.6, 1.35, 0])
        self.play(FadeIn(t1), run_time=0.4)
        self.at("minus")
        self.play(Write(e1), run_time=1.2)
        t2 = T("ejection fraction", 26, TEXT).move_to([4.6, 0.55, 0])
        e2 = M("80 / 125 = 64 %", 25, TEXT).move_to([4.6, 0.0, 0])
        self.at("Divide")
        self.play(FadeIn(t2), Write(e2), run_time=1.3)
        fill = loop_fill()
        t3 = T("area = stroke work", 26, BLUE).move_to([4.6, -1.1, 0])
        a3 = arr([2.95, -1.1, 0], [0.55, -0.55, 0], BLUE)
        self.at("area inside")
        self.play(FadeIn(fill), FadeIn(t3), GrowArrow(a3), run_time=0.9)
        self.wait(self.beat(0.08))
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Lines(SpokenScene):
    """a green line through the corner, an orange line from the end-diastolic volume, they meet; readouts."""

    def construct(self):
        c = carried(self)
        st = c["st"]
        self.add(st["sv"])
        fill = loop_fill()
        self.add(fill)
        t1 = T("stroke volume", 26, YELLOW).move_to([4.6, 1.9, 0])
        e1 = M("125 - 45 = 80 mL", 25, TEXT).move_to([4.6, 1.35, 0])
        t2 = T("ejection fraction", 26, TEXT).move_to([4.6, 0.55, 0])
        e2 = M("80 / 125 = 64 %", 25, TEXT).move_to([4.6, 0.0, 0])
        t3 = T("area = stroke work", 26, BLUE).move_to([4.6, -1.1, 0])
        a3 = arr([2.95, -1.1, 0], [0.55, -0.55, 0], BLUE)
        old = VGroup(t1, e1, t2, e2, t3, a3)
        self.add(old)
        self.play(FadeOut(old), FadeOut(fill), run_time=0.4)

        self.play(Indicate(st["corner"], color=YELLOW, scale_factor=1.8), run_time=0.9)
        espvr = Line(PT(V0, 0), PT(V0 + 150 / 3.0, 150), color=GREEN, stroke_width=6)
        esl = T("end-systolic line", 24, GREEN).move_to(PT(V0 + 50, 150) + RIGHT * 1.45 + UP * 0.0)
        self.at("pressure volume relation")
        self.play(Create(espvr), FadeIn(esl), run_time=1.5)
        st["espvr"] = espvr

        title = case_title("baseline", GREY)
        lbls = panel_labels()
        vals = panel_vals(strings(*BASE))
        self.at("Here")
        self.play(FadeIn(title), FadeIn(lbls[1]), FadeIn(vals["Ees"], shift=LEFT * 0.2), run_time=0.7)
        v0dot = Dot(PT(V0, 0), radius=0.1, color=GREEN)
        v0lbl = M("5", 22, GREEN).move_to(PT(V0, 0) + DOWN * 0.55)
        self.at("line meets the volume axis")
        self.play(FadeIn(v0dot, scale=0.5), FadeIn(v0lbl, shift=UP * 0.1), run_time=0.6)

        ealine = Line(PT(125, 0), PT(45, 120), color=ORANGE, stroke_width=6)
        self.at("second line starts")
        self.play(Indicate(st["edvdot"], color=TEAL, scale_factor=2.0), FadeIn(lbls[0]), FadeIn(vals["EDV"]), run_time=0.8)
        ea_tail = Line(PT(125, 0), PT(125, 0), color=ORANGE, stroke_width=6)
        self.add(ea_tail)
        self.play(Transform(ea_tail, ealine), run_time=1.4)
        st["ealine"] = ea_tail
        eal = T("arterial line", 24, ORANGE).move_to([-1.15, -1.5, 0])
        self.at("effective arterial")
        self.play(FadeIn(eal), FadeIn(lbls[2]), FadeIn(vals["Ea"], shift=LEFT * 0.2), run_time=0.7)
        self.at("where the two lines meet")
        self.play(Indicate(st["corner"], color=YELLOW, scale_factor=2.2), FadeIn(lbls[3:]), run_time=0.8)
        self.play(*[FadeIn(vals[k], shift=LEFT * 0.2) for k in ("Pes", "ESV", "SV", "EF")], run_time=0.9)
        self.wait(self.beat(0.05))
        self.finish()


# ---------------------------------------------------------------------------------------------
def full_model(scene, ghost=False):
    """the whole model as it stands after scene 4 (loop, both lines, corner, readouts); returns live parts."""
    cap = caption_line()
    ax = axes_group()
    loop = VGroup(*loop_segs())
    dots = VGroup(*[Dot(PT(v, p), radius=0.1, color=BLUE) for (v, p) in (A_, B_, D_)])
    y80 = M("80", 22, TEXT).move_to(PT(0, 80) + LEFT * 0.38)
    st = state(*BASE)
    v0dot = Dot(PT(V0, 0), radius=0.1, color=GREEN)
    v0lbl = M("5", 22, GREEN).move_to(PT(V0, 0) + DOWN * 0.55)
    lbls = panel_labels()
    vals = panel_vals(strings(*BASE))
    title = case_title("baseline", GREY)
    scene.add(cap, ax, loop, dots, y80, v0dot, v0lbl, lbls, title, *vals.values())
    for k in ("espvr", "ealine", "gv", "gh", "corner", "edvdot", "edvlbl", "esvlbl", "peslbl", "sv"):
        scene.add(st[k])
    return dict(loop=loop, dots=dots, y80=y80, st=st, vals=vals, title=title, lbls=lbls)


def update_panel(m, cfg, new_title, tcol):
    """animations: every panel value to the numbers of `cfg`, and the case title; changed ones in color."""
    s = strings(*cfg)
    new_vals = panel_vals(s)
    anims = []
    for name, _, _ in ROWS:
        anims.append(ReplacementTransform(m["vals"][name], new_vals[name]))
    m["vals"] = new_vals
    nt = case_title(new_title, tcol)
    anims.append(ReplacementTransform(m["title"], nt))
    m["title"] = nt
    return anims


class S05Afterload(SpokenScene):
    """arteries tighten: the orange line pivots steeper, the corner slides up the same green line."""

    def construct(self):
        m = full_model(self)
        st = m["st"]
        ring = Circle(radius=0.2, color=GREY, stroke_width=3).move_to(PT(*C_))
        rlbl = T("baseline loop", 22, GREY).move_to([-0.55, 1.95, 0])
        newst = state(*AFT)

        self.at("the arteries")
        self.play(*dim_anims(m, 0.3), FadeIn(ring), FadeIn(rlbl), run_time=0.8)
        self.at("filling")
        self.play(Indicate(m["st"]["edvdot"], color=TEAL, scale_factor=2.0),
                  Indicate(st["espvr"], color=GREEN, scale_factor=1.0), run_time=1.3)
        self.at("constriction")
        newt = case_title("afterload up", ORANGE)
        self.play(ReplacementTransform(m["title"], newt), run_time=0.5)
        m["title"] = newt
        self.at("raises")
        new_vals = panel_vals(strings(*AFT))
        self.play(Transform(st["ealine"], newst["ealine"]), ReplacementTransform(m["vals"]["Ea"], new_vals["Ea"]), run_time=1.4)
        m["vals"]["Ea"] = new_vals["Ea"]
        self.at("meets")
        self.play(Transform(st["corner"], newst["corner"]), Transform(st["gv"], newst["gv"]), Transform(st["gh"], newst["gh"]),
                  run_time=1.5)
        self.at("pressure rises")
        self.play(ReplacementTransform(st["peslbl"], newst["peslbl"]), ReplacementTransform(m["vals"]["Pes"], new_vals["Pes"]), run_time=0.7)
        st["peslbl"] = newst["peslbl"]
        m["vals"]["Pes"] = new_vals["Pes"]
        self.at("volume rises")
        self.play(ReplacementTransform(st["esvlbl"], newst["esvlbl"]), ReplacementTransform(m["vals"]["ESV"], new_vals["ESV"]), run_time=0.7)
        st["esvlbl"] = newst["esvlbl"]
        m["vals"]["ESV"] = new_vals["ESV"]
        self.at("falls to", nth=0)
        self.play(Transform(st["sv"], newst["sv"]), ReplacementTransform(m["vals"]["SV"], new_vals["SV"]), run_time=0.8)
        m["vals"]["SV"] = new_vals["SV"]
        self.at("ejection fraction")
        self.play(ReplacementTransform(m["vals"]["EF"], new_vals["EF"]), run_time=0.8)
        m["vals"]["EF"] = new_vals["EF"]
        self.play(Indicate(new_vals["EF"], color=YELLOW, scale_factor=1.25), run_time=0.9)
        self.finish()


class S06Rule(SpokenScene):
    """EF fell with Ees and filling unchanged; back to baseline; preload up; contractility up; the rule."""

    def construct(self):
        m = full_model(self)
        st = m["st"]
        ring = Circle(radius=0.2, color=GREY, stroke_width=3).move_to(PT(*C_))
        rlbl = T("baseline loop", 22, GREY).move_to([-0.55, 1.95, 0])
        m["loop"].set_stroke(opacity=0.3); m["dots"].set_opacity(0.3); m["y80"].set_opacity(0.3)
        self.add(ring, rlbl)
        # carry scene 5's end state: afterload up
        newst = state(*AFT)
        for k in GEOM:
            st[k].become(newst[k])
        for k in LBLS:
            self.remove(st[k])
            st[k] = newst[k]
            self.add(st[k])
        newt = case_title("afterload up", ORANGE)
        self.remove(m["title"])
        m["title"] = newt
        self.add(newt)
        new_vals = panel_vals(strings(*AFT))
        for k, v in m["vals"].items():
            self.remove(v)
        m["vals"] = new_vals
        self.add(*new_vals.values())

        self.at("did not change")
        self.play(Indicate(m["vals"]["EDV"], color=TEAL, scale_factor=1.15),
                  Indicate(m["vals"]["Ees"], color=GREEN, scale_factor=1.15),
                  Indicate(st["espvr"], color=GREEN, scale_factor=1.0), run_time=1.5)
        self.at("ejection fraction fell")
        self.play(Indicate(m["vals"]["EF"], color=YELLOW, scale_factor=1.25), run_time=1.0)
        self.at("with no change")
        self.play(Indicate(m["vals"]["Ees"], color=GREEN, scale_factor=1.15), run_time=0.9)

        # back to the first loop
        self.at("Go back")
        new = state(*BASE)
        self.play(*morph(st, new), *update_panel(m, BASE, "baseline", GREY),
                  *dim_anims(m, 1), FadeOut(ring), FadeOut(rlbl), run_time=1.5)

        # preload up: the corner slides up the same green line
        self.at("raise filling")
        new = state(*PRE)
        self.play(*morph(st, new), *update_panel(m, PRE, "preload up", TEAL), *dim_anims(m, 0.3), FadeIn(rlbl), run_time=1.8)
        self.at("corner slides")
        self.play(Indicate(st["corner"], color=YELLOW, scale_factor=2.0), run_time=1.0)
        self.at("volume rises")
        self.play(Indicate(m["vals"]["SV"], color=YELLOW, scale_factor=1.25), run_time=1.0)

        # contractility up: the green line steepens
        self.at("return filling")
        new = state(*BASE)
        self.play(*morph(st, new), *update_panel(m, BASE, "baseline", GREY), *dim_anims(m, 1), FadeOut(rlbl), run_time=1.4)
        self.at("and raise")
        new = state(*CON)
        self.play(*morph(st, new), *update_panel(m, CON, "contractility up", GREEN), *dim_anims(m, 0.3), FadeIn(rlbl), run_time=1.8)
        self.at("volume falls")
        self.play(Indicate(st["corner"], color=YELLOW, scale_factor=2.0), Indicate(m["vals"]["ESV"], color=YELLOW, scale_factor=1.25),
                  run_time=1.0)

        # the rule
        self.at("rule to keep")
        new = state(*BASE)
        panel_all = VGroup(m["lbls"], *m["vals"].values(), m["title"])
        self.play(*morph(st, new), *dim_anims(m, 1), FadeOut(panel_all), FadeOut(rlbl), run_time=0.9)
        self.play(FadeOut(st["gv"]), FadeOut(st["gh"]), FadeOut(st["peslbl"]), FadeOut(st["esvlbl"]), FadeOut(st["sv"]),
                  run_time=0.4)

        def chip3(head, sub, col, y):
            return VGroup(T(head, 28, col, weight=BOLD), T(sub, 24, TEXT)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([PX_L, y, 0], aligned_edge=LEFT)

        c1 = chip3("preload", "the bottom right corner", TEAL, 1.4)
        c2 = chip3("afterload", "the arterial line", ORANGE, 0.1)
        c3 = chip3("contractility", "the end-systolic line", GREEN, -1.2)
        self.at("preload")
        self.play(FadeIn(c1), Indicate(st["edvdot"], color=TEAL, scale_factor=2.2), run_time=0.5)
        self.at("afterload")
        self.play(FadeIn(c2), Indicate(st["ealine"], color=ORANGE, scale_factor=1.0), run_time=0.5)
        self.at("contractility", nth=2)
        self.play(FadeIn(c3), Indicate(st["espvr"], color=GREEN, scale_factor=1.0), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "Preload, afterload, contractility: each moves a different part of the loop."
