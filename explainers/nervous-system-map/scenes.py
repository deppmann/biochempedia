"""A map is not a verdict: the nervous-system map and what each kind of evidence licenses
(Biochemistrypedia explainer, Neuroscience course).

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.
The brain is drawn ONLY as regions in ONE standard view: the lateral view of the left side of the brain,
front at the viewer's left. No section of the brain is drawn. The lesion, recording, imaging and
stimulation panels are boxes, labelled chips and a firing sketch (labelled "in this sketch"); the only
numbers on screen are the lesson's own: 180 areas per hemisphere, 139 / 89 / 86 experiments, 1957.

COLOR MAP (one color per concept, whole video)
  BLUE   = the map: brain regions (lobes, brainstem, cerebellum), plain structures
  TEAL   = the region being talked about (the two gyri)
  RED    = lesion / damage / deficit
  YELLOW = recording: electrode, firing
  GREEN  = imaging: the BOLD signal
  ORANGE = stimulation: current pulses
  GREY   = labels, axes, de-emphasized, "not shown by this evidence"
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
MAP, HIL, LES, REC, IMG, STIM = BLUE, TEAL, RED, YELLOW, GREEN, ORANGE

# ---------------------------------------------------------------------------------------------
# The brain: lateral view, left side of the brain, front at the viewer's left (regions only)
# ---------------------------------------------------------------------------------------------
S_, OX, OY = 1.0, 0.2, 0.5


def A(x, y):
    return np.array([S_ * x + OX, S_ * (y - 0.275) + OY, 0.0])


_P = dict(
    A=(-4.0, 0.2), B=(-3.7, 1.2), C=(-2.8, 2.0), D=(-1.4, 2.5), E=(0.4, 2.62), F=(2.0, 2.35),
    G=(3.0, 1.6), H=(3.6, 0.6), I=(3.5, -0.4), J=(2.8, -1.0), K=(1.4, -1.5), L=(-0.3, -1.8),
    M=(-1.8, -1.6), N=(-2.3, -0.9), O=(-3.2, -0.5), Cb=(-0.7, -0.25), Pp=(1.2, 0.4), R=(2.3, -0.3),
)
_LOBES = dict(
    frontal=list("ABCDE") + ["Cb", "N", "O"],
    parietal=["E", "F", "R", "Pp", "Cb"],
    occipital=["F", "G", "H", "I", "J", "R"],
    temporal=["N", "Cb", "Pp", "R", "J", "K", "L", "M"],
)


def _poly(keys, rc=0.12, **style):
    pts = [A(*_P[k]) for k in keys]
    p = Polygon(*pts, **style)
    return p.round_corners(rc) if rc else p


def _raw(keys):
    return Polygon(*[A(*_P[k]) for k in keys], stroke_width=0)


def brain_parts():
    """dict of VMobjects: frontal, parietal, occipital, temporal, cerebellum, brainstem, pre, post."""
    d = {}
    for n, ks in _LOBES.items():
        d[n] = _poly(ks, fill_color=MAP, fill_opacity=0.30, stroke_color=BG, stroke_width=4)
    cb = Ellipse(width=2.1 * S_, height=1.2 * S_, fill_color=MAP, fill_opacity=0.30, stroke_color=BG,
                 stroke_width=4).move_to(A(2.5, -1.75))
    bs = Polygon(A(-0.3, -1.8), A(1.0, -1.57), A(1.3, -3.0), A(0.4, -3.1), fill_color=MAP, fill_opacity=0.30,
                 stroke_color=BG, stroke_width=4).round_corners(0.1)
    d["cerebellum"], d["brainstem"] = cb, bs
    # the two gyri: strips either side of the central sulcus (top E to the lateral fissure at Cb)
    d["pre"] = Polygon(A(0.4, 2.55), A(-0.7, -0.25), A(-1.2, -0.3), A(-0.1, 2.5), fill_color=HIL, fill_opacity=0.5,
                       stroke_width=0).round_corners(0.08)
    d["post"] = Polygon(A(0.45, 2.55), A(-0.65, -0.2), A(-0.25, -0.05), A(0.95, 2.5), fill_color=HIL, fill_opacity=0.5,
                        stroke_width=0).round_corners(0.08)
    return d


def mosaic():
    """schematic patches over the cerebrum (NOT the atlas): hexagon cells cut to the four lobes."""
    rng = np.random.default_rng(3)
    out = VGroup()
    raws = {n: _raw(ks) for n, ks in _LOBES.items()}
    r = 0.38
    dx, dy = 1.5 * r, np.sqrt(3) * r
    for i in range(-14, 14):
        for j in range(-12, 12):
            c = A(-0.2, 0.9) + np.array([i * dx, j * dy + (dy / 2 if i % 2 else 0), 0])
            if not (-4.4 < (c[0] - OX) / S_ < 3.9 and -2.2 < (c[1] - OY) / S_ + 0.275 < 2.9):
                continue
            hexa = RegularPolygon(6, radius=r * 0.98, start_angle=0).move_to(c)
            for lob in raws.values():
                try:
                    m = Intersection(hexa, lob, fill_color=MAP, fill_opacity=float(rng.uniform(0.12, 0.62)),
                                     stroke_color=BG, stroke_width=2.5)
                except Exception:
                    continue
                if len(m.points) > 6 and m.width > 0.06:
                    out.add(m)
    return out


def lab_in(text, pt, size=24, color=TEXT):
    return T(text, size=size, color=color).move_to(A(*pt))


def leader(text, label_pos, target, size=24, color=TEXT, anchor=LEFT, sub=None):
    """label with a leader line; `anchor` is the side of the label the line leaves from."""
    t = T(text, size=size, color=color)
    if sub:
        t = VGroup(t, T(sub, size=22, color=GREY)).arrange(DOWN, buff=0.08)
    t.move_to(np.array([*label_pos, 0.0]))
    tgt = np.array([*target, 0.0]) if len(target) == 2 else target
    start = t.get_edge_center(anchor) + anchor * 0.1
    ln = Line(start, tgt, color=GREY, stroke_width=2.5)
    dot = Dot(tgt, radius=0.05, color=GREY)
    return VGroup(ln, dot, t)


def view_label():
    a = T("Lateral view · left side of the brain", size=22, color=GREY)
    b = T("front is at the viewer's left", size=22, color=GREY)
    g = VGroup(a, b).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    return g.move_to(np.array([-6.2, -3.0, 0]), aligned_edge=LEFT)


def arrow(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, color=color, stroke_width=w, buff=0, max_tip_length_to_length_ratio=0.35,
                 max_stroke_width_to_length_ratio=12)


def neuron(color=MAP, scale=1.0):
    soma = Circle(radius=0.3, fill_color=color, fill_opacity=0.35, stroke_color=color, stroke_width=3)
    dens = VGroup(*[Line(soma.get_center() + 0.28 * np.array([np.cos(a), np.sin(a), 0]),
                         soma.get_center() + 0.62 * np.array([np.cos(a), np.sin(a), 0]), color=color, stroke_width=3)
                    for a in (np.pi * 0.75, np.pi * 0.5, np.pi * 0.25)])
    ax = Line(soma.get_center() + DOWN * 0.3, soma.get_center() + DOWN * 0.95, color=color, stroke_width=3)
    return VGroup(soma, dens, ax).scale(scale)


# =============================================================================================
class S00Title(TitleCard):
    LESSON = "The Map: How the Nervous System Is Organized"
    TITLE = "A Map Is Not a Verdict"


# ---------------------------------------------------------------------------------------------
class S01Map(SpokenScene):
    def construct(self):
        d = brain_parts()
        self.add(d["brainstem"], d["cerebellum"])
        d["brainstem"].set_opacity(0); d["cerebellum"].set_opacity(0)
        q = T("Where in the brain does a function live?", size=34).move_to(np.array([0, 3.2, 0]))
        lab = view_label()
        self.add(lab)
        self.at("Where in the brain")
        self.play(Write(q), run_time=1.2)
        self.at("Start with the map")
        self.play(*[FadeIn(d[k], scale=0.97) for k in ("frontal", "parietal", "temporal", "occipital")],
                  run_time=1.2)
        names = {}
        names["frontal"] = lab_in("Frontal", (-2.4, 0.9))
        names["parietal"] = lab_in("Parietal", (1.3, 1.1))
        names["temporal"] = lab_in("Temporal", (0.4, -1.0))
        names["occipital"] = leader("Occipital", (5.4, 1.2), A(3.1, 0.5))
        self.at("four lobes")
        self.play(FadeIn(names["frontal"]), run_time=0.4)
        self.at("parietal")
        self.play(FadeIn(names["parietal"]), run_time=0.4)
        self.at("temporal")
        self.play(FadeIn(names["temporal"]), run_time=0.4)
        self.at("occipital")
        self.play(FadeIn(names["occipital"]), run_time=0.4)
        self.at("The brainstem")
        names["brainstem"] = leader("Brainstem", (-2.4, -2.1), A(0.5, -2.4), anchor=RIGHT)
        self.play(d["brainstem"].animate.set_fill(MAP, 0.30).set_stroke(BG, 4, 1), FadeIn(names["brainstem"]), run_time=0.6)
        self.at("the cerebellum")
        names["cerebellum"] = leader("Cerebellum", (5.4, -1.9), A(3.2, -1.8))
        self.play(d["cerebellum"].animate.set_fill(MAP, 0.30).set_stroke(BG, 4, 1), FadeIn(names["cerebellum"]), run_time=0.6)
        self.at("A map names places")
        self.play(*[names[k].animate.set_opacity(0.0) for k in names], q.animate.set_opacity(0.0), run_time=0.7)
        qs = T("what lives in each one?", size=34, color=HIL).move_to(np.array([0, 3.2, 0]))
        marks = VGroup(*[T("?", size=64, color=HIL).move_to(A(*p)) for p in
                         [(-2.4, 0.9), (1.2, 1.1), (0.4, -1.0), (3.0, 0.5)]])
        self.at("It does not tell")
        self.play(FadeIn(qs), LaggedStart(*[FadeIn(m, scale=0.7) for m in marks], lag_ratio=0.15), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Literal(SpokenScene):
    def construct(self):
        d = brain_parts()
        lab = view_label()
        g = VGroup(*[d[k] for k in ("brainstem", "cerebellum", "frontal", "parietal", "temporal", "occipital")])
        self.add(lab, g)
        pre = leader("Precentral gyrus", (-5.0, 2.3), A(-0.75, 1.7), color=HIL, anchor=RIGHT, sub="primary motor cortex")
        post = leader("Postcentral gyrus", (4.85, 2.3), A(0.05, 1.7), color=HIL, anchor=LEFT, sub="primary somatosensory\ncortex")
        self.at("Read the map literally")
        self.wait(0.1)
        self.at("gyrus contains primary motor", lead=1.0)
        self.play(FadeIn(d["pre"]), FadeIn(pre), run_time=0.7)
        self.at("gyrus contains primary somatosensory", lead=1.0)
        self.play(FadeIn(d["post"]), FadeIn(post), run_time=0.7)
        self.at("No region here")
        one_a = chip("one region = one function", color=RED, size=24)
        one_b = chip("one function = one region", color=RED, size=24)
        row = VGroup(one_a, one_b).arrange(RIGHT, buff=0.5).move_to(np.array([0, 3.2, 0]))
        sa = Line(one_a.get_left(), one_a.get_right(), color=RED, stroke_width=5)
        sb = Line(one_b.get_left(), one_b.get_right(), color=RED, stroke_width=5)
        self.play(FadeIn(row), run_time=0.5)
        self.at("single function")
        self.play(Create(sa), run_time=0.4)
        self.at("single region")
        self.play(Create(sb), run_time=0.4)
        self.at("The cortex is a mosaic")
        mo = mosaic()
        self.play(FadeOut(pre), FadeOut(post), d["pre"].animate.set_opacity(0), d["post"].animate.set_opacity(0),
                  FadeOut(row), FadeOut(sa), FadeOut(sb), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(m) for m in mo], lag_ratio=0.004), run_time=1.3)
        self.at("One atlas")
        cap = VGroup(M("180", size=36, color=MAP), T("areas per hemisphere, one atlas", size=28)).arrange(RIGHT, buff=0.2)
        sub = T("healthy young adults · these patches are schematic, not the atlas", size=22, color=GREY)
        sub = VGroup(T("healthy young adults", size=22, color=GREY),
                     T("patches here are schematic, not the atlas", size=22, color=GREY)).arrange(DOWN, aligned_edge=RIGHT, buff=0.06)
        sub.move_to(np.array([6.2, 3.25, 0]), aligned_edge=RIGHT)
        cap.move_to(np.array([-6.2, 3.2, 0]), aligned_edge=LEFT)
        self.play(FadeIn(cap), FadeIn(sub), run_time=0.5)
        self.at("borders vary")
        self.play(mo.animate.shift(RIGHT * 0.1 + UP * 0.04), run_time=0.5)
        self.play(mo.animate.shift(LEFT * 0.2), run_time=0.5)
        self.play(mo.animate.shift(RIGHT * 0.1 + DOWN * 0.04), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Lesion(SpokenScene):
    def construct(self):
        tag = T("LESION", size=34, color=LES, weight=BOLD).move_to(np.array([-5.2, 3.1, 0]))
        before = chip("behaviour before", color=GREY, size=32)
        after = chip("behaviour after", color=GREY, size=32)
        row = VGroup(before, arrow(LEFT * 0.8, RIGHT * 0.8), after).arrange(RIGHT, buff=0.3)
        row.move_to(np.array([0, 2.05, 0]))
        boxes = VGroup(*[chip("structure", color=MAP, size=34, pad=0.38) for _ in range(3)]).arrange(RIGHT, buff=1.0)
        boxes.move_to(np.array([0, -0.2, 0]))
        cloud_small = Ellipse(width=boxes[1].width + 0.7, height=boxes[1].height + 0.9, color=LES, fill_opacity=0.28,
                              stroke_width=3).move_to(boxes[1])
        cloud_big = Ellipse(width=boxes.width + 1.4, height=boxes.height + 1.2, color=LES, fill_opacity=0.28,
                            stroke_width=3).move_to(boxes)
        dmg = T("damage", size=30, color=LES).next_to(cloud_big, UP, buff=0.12)
        self.at("So what kind")
        self.play(FadeIn(tag), run_time=0.5)
        self.at("The first is a lesion")
        self.play(FadeIn(boxes, lag_ratio=0.2), run_time=0.8)
        self.at("before and after")
        self.play(FadeIn(before), run_time=0.4)
        self.play(FadeIn(row[1]), FadeIn(after), run_time=0.5)
        self.at("after damage")
        self.play(FadeIn(cloud_small), boxes[1][0].animate.set_stroke(LES), run_time=0.6)
        self.at("A deficit")
        self.play(after[0].animate.set_stroke(LES).set_fill(LES, 0.2), after[1].animate.set_color(LES), run_time=0.6)
        self.at("contributes to the task")
        self.play(Indicate(cloud_small, color=LES, scale_factor=1.05), run_time=0.8)
        self.at("But damage spreads")
        self.play(Transform(cloud_small, cloud_big), FadeIn(dmg), run_time=1.0)
        self.at("In a 1957 report")
        yr = VGroup(M("1957", size=32, color=LES), T("report, human patients", size=30)).arrange(RIGHT, buff=0.25)
        yr.move_to(np.array([0, -2.0, 0]))
        self.play(FadeIn(yr), run_time=0.5)
        self.at("several medial temporal structures")
        sev = T("several medial temporal structures removed at once", size=30, color=LES).move_to(np.array([0, -2.85, 0]))
        self.play(FadeIn(sev), run_time=0.6)
        self.at("pinned to one")
        qs = VGroup(*[T("?", size=56, color=TEXT).move_to(b.get_center()) for b in boxes])
        self.play(*[b[1].animate.set_opacity(0.0) for b in boxes], FadeIn(qs, lag_ratio=0.2), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Record(SpokenScene):
    def construct(self):
        rng = np.random.default_rng(7)
        ln = Line(UP * 3.4, DOWN * 3.4, color=GREY, stroke_width=1.5, stroke_opacity=0.5)
        t_rec = T("RECORDING", size=34, color=REC, weight=BOLD).move_to(np.array([-3.2, 3.1, 0]))
        t_img = T("IMAGING", size=34, color=IMG, weight=BOLD).move_to(np.array([3.4, 3.1, 0]))
        x1, w0, w1 = -0.8, -3.8, -2.2
        lab_s = T("stimulus", size=24, color=GREY).move_to(np.array([-5.2, 2.0, 0]))
        base_s = Line(np.array([-4.3, 2.0, 0]), np.array([x1, 2.0, 0]), color=GREY, stroke_width=3)
        on = Rectangle(width=w1 - w0, height=0.45, fill_color=GREY, fill_opacity=0.6, stroke_width=0).move_to(
            np.array([(w0 + w1) / 2, 2.0, 0]))
        lab_f = T("firing", size=24, color=REC).move_to(np.array([-5.2, 0.8, 0]))
        base_f = Line(np.array([-4.3, 0.45, 0]), np.array([x1, 0.45, 0]), color=GREY, stroke_width=2)
        ticks = VGroup()
        xs = list(rng.uniform(-4.2, w0, 3)) + list(np.linspace(w0 + 0.05, w1 - 0.05, 15) + rng.uniform(-0.04, 0.04, 15)) \
            + list(rng.uniform(w1, x1, 2))
        for x in sorted(xs):
            ticks.add(Line(np.array([x, 0.45, 0]), np.array([x, 1.2, 0]), color=REC, stroke_width=4))
        sk = T("in this sketch", size=22, color=GREY).move_to(np.array([-1.7, 0.0, 0]))
        nrn = neuron(REC, 1.0).move_to(np.array([-5.3, -1.0, 0]))
        elec = Line(np.array([-4.4, -0.3, 0]), nrn[0].get_center() + np.array([0.28, 0.12, 0]), color=REC, stroke_width=3)
        elab = T("electrode", size=24, color=REC).move_to(np.array([-3.3, -0.4, 0]))
        goes = T("firing goes with the stimulus", size=26, color=REC).move_to(np.array([-2.2, -1.5, 0]))
        used = chip("used by the brain?", color=GREY, size=30).move_to(np.array([-2.9, -2.8, 0]))
        c_spk = chip("spiking", color=GREY, size=28).move_to(np.array([1.65, 1.8, 0]))
        c_lfp = chip("local field potential", color=IMG, size=28).move_to(np.array([4.55, 1.8, 0]))
        c_bold = chip("BOLD signal", color=IMG, size=32).move_to(np.array([3.3, -0.4, 0]))
        a_lfp = Arrow(c_lfp.get_bottom() + DOWN * 0.05, c_bold.get_top() + np.array([0.6, 0.05, 0]), color=IMG,
                      stroke_width=9, buff=0)
        a_spk = DashedLine(c_spk.get_bottom() + DOWN * 0.05, c_bold.get_top() + np.array([-0.6, 0.05, 0]),
                           color=GREY, stroke_width=3, dash_length=0.12)
        l_spk = T("less well", size=24, color=GREY).move_to(np.array([1.25, 0.65, 0]))
        l_lfp = T("better", size=26, color=IMG).move_to(np.array([5.35, 0.65, 0]))
        where = T("anaesthetized macaque · visual cortex", size=24, color=GREY).move_to(np.array([3.3, -1.4, 0]))
        seat = chip("an activation does not mark a seat", color=GREY, size=24).move_to(np.array([3.3, -2.6, 0]))
        self.add(ln)
        self.at("The second kind")
        self.play(FadeIn(t_rec), run_time=0.4)
        self.play(FadeIn(lab_s), Create(base_s), FadeIn(on), run_time=0.6)
        self.at("Firing goes")
        self.play(FadeIn(lab_f), Create(base_f), LaggedStart(*[Create(k) for k in ticks], lag_ratio=0.05),
                  FadeIn(sk), run_time=1.4)
        self.play(FadeIn(goes), run_time=0.4)
        self.at("does not show")
        self.play(FadeIn(nrn), Create(elec), FadeIn(elab), run_time=0.4)
        self.play(FadeIn(used), run_time=0.4)
        self.at("The third kind")
        self.play(FadeIn(t_img), run_time=0.4)
        self.at("oxygenation")
        self.play(FadeIn(c_bold), run_time=0.5)
        self.at("macaque visual cortex")
        self.play(FadeIn(where), run_time=0.4)
        self.at("local field potentials")
        self.play(FadeIn(c_lfp), run_time=0.4)
        self.at("better than spiking")
        self.play(FadeIn(c_spk), Create(a_spk), GrowArrow(a_lfp), FadeIn(l_spk), FadeIn(l_lfp), run_time=0.9)
        self.at("An activation")
        self.play(FadeIn(seat), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Stim(SpokenScene):
    def construct(self):
        tag = T("STIMULATION", size=34, color=STIM, weight=BOLD).move_to(np.array([-4.7, 3.2, 0]))
        box = RoundedRectangle(corner_radius=0.2, width=5.6, height=2.6, stroke_color=MAP, stroke_width=3,
                               fill_color=MAP, fill_opacity=0.08).move_to(np.array([-3.2, 1.35, 0]))
        cells = VGroup()
        for i in range(3):
            n = neuron(MAP, 0.9).move_to(box.get_center() + np.array([-1.6 + 1.6 * i, 0.2, 0]))
            cells.add(n)
        mt = T("area MT", size=26, color=TEXT).move_to(box.get_corner(UL) + np.array([0.85, -0.3, 0]))
        pref = VGroup(*[Arrow(c[0].get_center() + np.array([0.0, -0.12, 0]), c[0].get_center() + np.array([0.0, 0.14, 0]),
                              buff=0, color=HIL, stroke_width=4, max_tip_length_to_length_ratio=0.9) for c in cells])
        key = VGroup(Arrow(ORIGIN, UP * 0.5, buff=0, color=HIL, stroke_width=6), T("preferred direction", size=26, color=HIL)
                     ).arrange(RIGHT, buff=0.15).move_to(np.array([-3.2, -0.45, 0]))
        elec = Line(np.array([-1.5, 3.2, 0]), cells[2][0].get_center() + np.array([0.12, 0.25, 0]), color=STIM, stroke_width=3)
        pl = T("current pulses", size=26, color=STIM).move_to(np.array([0.05, 2.95, 0]))
        sc = Line(np.array([1.0, 1.3, 0]), np.array([6.1, 1.3, 0]), color=GREY, stroke_width=4)
        l1 = T("other direction", size=24, color=GREY).move_to(np.array([1.0, 0.7, 0]), aligned_edge=LEFT)
        l2 = T("preferred direction", size=24, color=HIL).move_to(np.array([6.1, 0.15, 0]), aligned_edge=RIGHT)
        cap = T("the monkey's choice", size=32).move_to(np.array([3.55, 2.3, 0]))
        dot = Dot(np.array([3.55, 1.3, 0]), radius=0.2, color=TEXT)
        tr = Arrow(np.array([3.55, 1.75, 0]), np.array([5.5, 1.75, 0]), buff=0, color=STIM, stroke_width=7)
        wmax = 7.6
        x0 = -6.0
        rows = [("139 experiments", 139, GREY, -1.4), ("89 significant effect", 89, STIM, -2.15), ("86 toward preferred", 86, HIL, -2.9)]
        bars = VGroup()
        for text, n, col, y in rows:
            wd = wmax * n / 139
            r = Rectangle(width=wd, height=0.6, fill_color=col, fill_opacity=0.35, stroke_color=col, stroke_width=2.5)
            r.move_to(np.array([x0 + wd / 2, y, 0]))
            tx = M(str(n), size=28, color=TEXT)
            tt = T(text.split(" ", 1)[1], size=26, color=TEXT)
            lab = VGroup(tx, tt).arrange(RIGHT, buff=0.15).move_to(r)
            bars.add(VGroup(r, lab))
        concl = T("a contribution, in that task,\nfrom the stimulated neurons,\nnot from one cell type", size=26, color=TEXT, line_spacing=0.9).move_to(np.array([4.0, -2.55, 0]))
        self.at("The fourth kind")
        self.play(FadeIn(tag), run_time=0.4)
        self.at("adds activity")
        self.play(FadeIn(sc), FadeIn(dot), FadeIn(cap), run_time=0.5)
        self.at("monkeys judged")
        self.play(FadeIn(l1), FadeIn(l2), run_time=0.5)
        self.at("stimulated neurons")
        self.play(FadeIn(box), FadeIn(cells, lag_ratio=0.2), run_time=0.7)
        self.play(Create(elec), FadeIn(pl), run_time=0.5)
        self.at("area")
        self.play(FadeIn(mt), run_time=0.4)
        self.at("shared a preferred")
        self.play(FadeIn(pref), FadeIn(key), run_time=0.6)
        self.at("experiments")
        self.play(FadeIn(bars[0]), run_time=0.4)
        self.at("significant effect")
        self.play(FadeIn(bars[1]), run_time=0.4)
        self.at("moved toward")
        self.play(FadeIn(bars[2]), run_time=0.3)
        self.play(dot.animate.move_to(np.array([5.3, 1.3, 0])), FadeIn(tr), run_time=0.8)
        self.at("That shows a contribution")
        self.play(FadeIn(concl), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        hdr_can = T("can show", size=26, color=GREY, weight=BOLD)
        hdr_not = T("cannot show alone", size=26, color=GREY, weight=BOLD)
        data = [
            ("Lesion", LES, "damaged tissue\ncontributes", "which part of the\ndamage mattered"),
            ("Recording", REC, "activity covaries with\na task or stimulus", "that the activity\nis used"),
            ("Imaging", IMG, "where a blood signal\ngoes with a task", "which neural signal,\nor necessity"),
            ("Stimulation", STIM, "adding activity\nchanges behaviour", "that the region\nis required"),
        ]
        xc, xn = -0.4, 4.1
        hdr_can.move_to(np.array([xc, 3.05, 0])); hdr_not.move_to(np.array([xn, 3.05, 0]))
        rows = []
        for i, (k, col, can, notc) in enumerate(data):
            y = 1.85 - i * 1.4
            kc = chip(k, color=col, size=30).move_to(np.array([-4.9, y, 0]))
            kc.align_to(np.array([-6.2, 0, 0]), LEFT)
            c1 = T(can, size=26, color=TEXT, line_spacing=0.9).move_to(np.array([xc, y, 0]))
            c2 = T(notc, size=26, color=GREY, line_spacing=0.9).move_to(np.array([xn, y, 0]))
            rows.append((kc, c1, c2))
        rule = T("Claim only what the evidence licenses.", size=36, color=GOLD, font=TITLE_FONT).move_to(np.array([0, -3.15, 0]))
        self.at("Here is the rule")
        self.play(FadeIn(hdr_can), FadeIn(hdr_not), run_time=0.5)
        self.at("A lesion shows")
        self.play(FadeIn(rows[0][0]), FadeIn(rows[0][1]), run_time=0.5)
        self.at("not which part")
        self.play(FadeIn(rows[0][2]), run_time=0.5)
        self.at("A recording shows")
        self.play(FadeIn(rows[1][0]), FadeIn(rows[1][1]), run_time=0.5)
        self.at("not use")
        self.play(FadeIn(rows[1][2]), run_time=0.5)
        self.at("Imaging shows")
        self.play(FadeIn(rows[2][0]), FadeIn(rows[2][1]), run_time=0.5)
        self.at("not which neural signal")
        self.play(FadeIn(rows[2][2]), run_time=0.5)
        self.at("Stimulation shows")
        self.play(FadeIn(rows[3][0]), FadeIn(rows[3][1]), run_time=0.5)
        self.at("not that the region")
        self.play(FadeIn(rows[3][2]), run_time=0.5)
        self.at("Claim only")
        self.play(FadeIn(rule, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "Claim only what the evidence licenses."
