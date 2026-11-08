"""Sensitive periods in behavior, chapter 1: One Input, Many Ages  (Biochemistrypedia chaptered film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.
Same look and colour map as the other chapters of this lesson (taken from scenes.old.py).

COLOR MAP (one color per concept, whole series)
  TEAL   = the window: how open the young nervous system is to experience (curves, "window" labels)
  YELLOW = experience that arrives: song heard, the tape, a tutor
  PURPLE = the memory of the tutor song (the template)
  BLUE   = the young bird and its own practice singing
  GREEN  = a normal or good outcome (wild song, a good copy, a check mark)
  RED    = an abnormal or impaired outcome, or something crossed out
  GREY   = structure, axes, the door, de-emphasized things
  GOLD   = the one idea to carry (card edge only), and the one summary number

Every curve is computed: song spectrograms from note-by-note pitch sweeps, practice waves from the
same wave functions the old film used (rich / rambling), the window curves from two sigmoids.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
PANEL = "#151823"
BRIGHT = "#F2C94C"      # the one summary number (a bright gold so it reads on the dark ground)
DOORC = "#DDE2EC"       # the door: a light grey


# ---------------------------------------------------------------------------------------------
# small drawing helpers
# ---------------------------------------------------------------------------------------------
def bird(scale=1.0, color=BLUE):
    """A sparrow from simple shapes, facing right. Parts: [0] tail [1] body [2] head [3] beak [4] eye [5] legs."""
    body = Ellipse(width=1.5, height=0.95, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.28)
    head = Circle(radius=0.34, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.28).move_to([0.62, 0.42, 0])
    beak = Polygon([0.93, 0.5, 0], [1.28, 0.4, 0], [0.93, 0.32, 0], stroke_color=YELLOW, stroke_width=3,
                   fill_color=YELLOW, fill_opacity=0.9)
    tail = Polygon([-0.65, 0.1, 0], [-1.4, 0.35, 0], [-1.3, -0.05, 0], stroke_color=color, stroke_width=4,
                   fill_color=color, fill_opacity=0.28)
    eye = Dot([0.72, 0.48, 0], radius=0.05, color=TEXT)
    legs = VGroup(Line([-0.1, -0.45, 0], [-0.1, -0.8, 0], color=color, stroke_width=4),
                  Line([0.2, -0.45, 0], [0.2, -0.8, 0], color=color, stroke_width=4))
    return VGroup(tail, body, head, beak, eye, legs).scale(scale)


def tape(s=1.0, color=YELLOW, fill=0.25):
    """A small cassette tape: the recorded song."""
    body = RoundedRectangle(corner_radius=0.08, width=0.9, height=0.58, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=fill)
    r1 = Circle(radius=0.11, stroke_color=color, stroke_width=3).move_to([-0.2, 0.06, 0])
    r2 = Circle(radius=0.11, stroke_color=color, stroke_width=3).move_to([0.2, 0.06, 0])
    strip = Rectangle(width=0.5, height=0.09, stroke_width=0, fill_color=color, fill_opacity=0.8).move_to([0, -0.17, 0])
    return VGroup(body, r1, r2, strip).scale(s)


def no_tape(at, s=0.9):
    """The crossed-out tape chip: this bird heard no tape."""
    return VGroup(tape(s, GREY, 0.05).set_opacity(0.55), cross([0, 0, 0], RED, 0.2 * s, 6)).move_to([at[0], at[1], 0])


def ear(s=1.0, color=GREY, w=5):
    """A plain ear: a tall rim open at the bottom, an inner fold and the canal (always labelled 'ear' on screen)."""
    rim = ParametricFunction(lambda t: np.array([0.38 * np.cos(np.radians(-60 + 300 * t)), 0.55 * np.sin(np.radians(-60 + 300 * t)), 0]),
                             t_range=[0, 1], color=color, stroke_width=w)
    fold = ParametricFunction(lambda t: np.array([-0.02 + 0.19 * np.cos(np.radians(30 + 250 * t)), 0.06 + 0.30 * np.sin(np.radians(30 + 250 * t)), 0]),
                              t_range=[0, 1], color=color, stroke_width=w)
    canal = Dot([0.02, -0.12, 0], radius=0.045, color=color)
    return VGroup(rim, fold, canal).scale(s).set_fill(opacity=0)


def speaker(s=1.0, color=GREY):
    box = Rectangle(width=0.4, height=0.5, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.5)
    cone = Polygon([0.2, 0.25, 0], [0.7, 0.62, 0], [0.7, -0.62, 0], [0.2, -0.25, 0], stroke_color=color,
                   stroke_width=3, fill_color=color, fill_opacity=0.3)
    return VGroup(box, cone).scale(s)


def check(at, color=GREEN, s=0.2):
    c = VMobject(stroke_color=color, stroke_width=11)
    c.set_points_as_corners([[-s, 0, 0], [-s * 0.3, -s * 0.75, 0], [s * 1.1, s * 0.9, 0]])
    return c.move_to(at)


def cross(at, color=RED, s=0.2, w=7):
    return VGroup(Line([-s, -s, 0], [s, s, 0], color=color, stroke_width=w),
                  Line([-s, s, 0], [s, -s, 0], color=color, stroke_width=w)).move_to(at)


def link(a, b, color=GREY, w=4):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=0.2)


def wave(x0, y, L, fn, color, amp=0.4, w=4, n=220, t_scale=1.0):
    """A wave drawn over width L from fn(t), t in [0, 5]; the same sample count everywhere so waves can Transform."""
    pts = [[x0 + L * i / n, y + amp * fn(t_scale * 5.0 * i / n), 0] for i in range(n + 1)]
    return VMobject(stroke_color=color, stroke_width=w).set_points_as_corners(pts)


def ghost(mob, opacity=0.5, dashes=90):
    """A dashed, dimmed copy of an open curve (a target seen behind a moving trace)."""
    return DashedVMobject(mob.copy().set_stroke(opacity=opacity), num_dashes=dashes, dashed_ratio=0.55)


def rich(t):
    return (0.55 + 0.45 * np.sin(2.1 * t)) * np.sin(9.0 * t) + 0.25 * np.sin(23 * t + 1)


def rambling(t):
    return 0.8 * np.sin(5.0 * t + 0.8) * np.cos(17 * t) + 0.35 * np.sin(31 * t + 2) + 0.2 * np.sin(2.3 * t)


def mixed(a):
    """A practice wave a fraction `a` of the way from rambling to the rich target."""
    return lambda t: (1 - a) * rambling(t) + a * rich(t)


def wander(k):
    """A practice wave that wanders: a different rambling shape each time."""
    return lambda t: rambling(t + 1.7 * k) * (0.85 + 0.15 * np.sin(1.3 * k + t))


# ---------------------------------------------------------------------------------------------
# song spectrograms: pitch (up) over time (right), built from note-by-note sweeps
# ---------------------------------------------------------------------------------------------
def _sweep(t0, t1, f0, f1, curve=0.0, n=20):
    u = np.linspace(0, 1, n)
    return np.stack([t0 + (t1 - t0) * u, f0 + (f1 - f0) * u + curve * np.sin(np.pi * u)], 1)


def song_notes(kind, seed=0):
    """Return a list of (points in [0,1]x[0,1], weight) for one song."""
    notes = []
    if kind == "wild":            # rich, detailed: whistles, a trill of short down-sweeps, three closing notes
        notes += [(_sweep(0.04, 0.20, 0.74, 0.70, 0.02), 1.0), (_sweep(0.23, 0.33, 0.66, 0.52, -0.03), 1.0)]
        for k in range(7):
            s = 0.37 + 0.032 * k
            notes.append((_sweep(s, s + 0.022, 0.62, 0.40, 0.03, 8), 1.0))
        notes += [(_sweep(0.63, 0.72, 0.35, 0.55, 0.10), 1.0), (_sweep(0.75, 0.84, 0.55, 0.30, -0.10), 1.0),
                  (_sweep(0.87, 0.95, 0.30, 0.50, 0.10), 1.0)]
        harm = [(np.stack([p[:, 0], np.clip(p[:, 1] * 1.32, 0, 0.93)], 1), 0.45) for p, _ in notes[:2] + notes[9:]]
        notes += harm
    elif kind == "simple":        # an isolate: a few flat, plain notes
        notes += [(_sweep(0.06, 0.24, 0.50, 0.50, 0.02), 1.0), (_sweep(0.33, 0.50, 0.42, 0.42, -0.02), 1.0),
                  (_sweep(0.60, 0.80, 0.47, 0.47, 0.025), 1.0)]
    elif kind == "poor":          # tutored too late: still plain, a little rough
        notes += [(_sweep(0.05, 0.20, 0.55, 0.55, 0.02), 1.0), (_sweep(0.29, 0.40, 0.50, 0.38, 0.0), 1.0),
                  (_sweep(0.50, 0.53, 0.46, 0.46, 0), 1.0), (_sweep(0.58, 0.61, 0.46, 0.46, 0), 1.0),
                  (_sweep(0.66, 0.69, 0.46, 0.46, 0), 1.0), (_sweep(0.76, 0.90, 0.44, 0.52, 0.0), 1.0)]
    elif kind == "disorder":      # disordered: irregular lengths, gaps and jumps in pitch
        rng = np.random.RandomState(seed)
        t = 0.03
        while t < 0.9:
            d = rng.uniform(0.02, 0.11)
            notes.append((_sweep(t, t + d, rng.uniform(0.15, 0.85), rng.uniform(0.15, 0.85), rng.uniform(-0.12, 0.12), 12), 1.0))
            t += d + rng.uniform(0.0, 0.07)
    return notes


def spectrogram(kind, center, w=5.4, h=2.8, color=GREEN, seed=0, sw=9.0, with_traces=True, axes=False):
    """A dark panel. [0] is the frame, [1] the group of traces, [2] the axis marks (empty unless axes=True)."""
    cx, cy = center[0], center[1]
    frame = RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_color=GREY, stroke_width=2.5,
                             fill_color=PANEL, fill_opacity=1).move_to([cx, cy, 0])
    extras = VGroup()
    if axes:
        x0, y0 = cx - w / 2 + 0.95, cy - h / 2 + 0.85
        ww, hh = w - 1.3, h - 1.45
        extras.add(Arrow([x0 - 0.2, y0 - 0.15, 0], [x0 - 0.2, cy + h / 2 - 0.3, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.16),
                   Arrow([x0 - 0.2, y0 - 0.15, 0], [cx + w / 2 - 0.25, y0 - 0.15, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.16),
                   T("pitch", 26, GREY).rotate(PI / 2).move_to([cx - w / 2 + 0.38, cy + 0.1, 0]),
                   T("time", 26, GREY).move_to([cx + 0.3, cy - h / 2 + 0.35, 0]),
                   T("schematic", 26, GREY).move_to([cx + w / 2 - 1.05, cy + h / 2 - 0.33, 0]))
    else:
        x0, y0 = cx - w / 2 + 0.25, cy - h / 2 + 0.2
        ww, hh = w - 0.5, h - 0.4
    traces = VGroup()
    if with_traces:
        for pts, wt in song_notes(kind, seed):
            m = VMobject(stroke_color=color, stroke_width=sw * wt, stroke_opacity=min(1.0, 0.35 + wt * 0.65))
            m.set_points_as_corners([[x0 + t * ww, y0 + float(np.clip((f - 0.2) / 0.62, 0.0, 1.0)) * hh, 0] for t, f in pts])
            traces.add(m)
    return VGroup(frame, traces, extras)


def p_in(p):
    """FadeIn for a spectrogram's frame and its axis marks (not the traces)."""
    parts = [FadeIn(p[0])] + ([FadeIn(p[2])] if len(p[2]) else [])
    return AnimationGroup(*parts)


def draw_song(panel, run_time=1.2):
    return LaggedStart(*[Create(m) for m in panel[1]], lag_ratio=0.12, run_time=run_time)


def lab(text, size=26, color=GREY, pos=(0, 0), font=FONT, weight=NORMAL):
    return T(text, max(size, 26), color, font=font, weight=weight).move_to([pos[0], pos[1], 0])


def lab_top(text, size, color, x, ytop, weight=NORMAL):
    """A label whose TOP edge sits at ytop, so a row of labels shares one line whatever their descenders."""
    m = T(text, max(size, 26), color, weight=weight).move_to([x, 0, 0])
    m.align_to([0, ytop, 0], UP)
    return m


# ---------------------------------------------------------------------------------------------
# the window-versus-age plot used by the last scenes
# ---------------------------------------------------------------------------------------------
PX0, PX1, PY0, PY1 = -4.7, 6.0, -2.8, 3.3


def pt(u, v):
    return [PX0 + u * (PX1 - PX0), PY0 + 0.1 + v * (PY1 - PY0 - 0.3), 0]


def _sig(x):
    return 1.0 / (1.0 + np.exp(-x))


def step_val(u):
    return 0.05 + 0.95 * _sig((0.45 - u) / 0.012)


def ramp_val(u):
    return 0.05 + 0.95 * _sig((0.45 - u) / 0.2)


def curve(fn, color=TEAL, sw=7, dashed=False, opacity=1.0, n=240):
    m = VMobject(stroke_color=color, stroke_width=sw, stroke_opacity=opacity)
    m.set_points_as_corners([pt(i / n, fn(i / n)) for i in range(n + 1)])
    return DashedVMobject(m, num_dashes=70, dashed_ratio=0.6) if dashed else m


def plot_axes():
    """Returns the two arrows, the y labels (title, little, much) and the x labels (title, early, late)."""
    ax = VGroup(Arrow([PX0, PY0, 0], [PX1 + 0.3, PY0, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.22),
                Arrow([PX0, PY0, 0], [PX0, PY1 + 0.15, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.22))
    ylab = VGroup(T("copy of tutor song (what lasts)", 26, GREY).rotate(PI / 2).move_to([PX0 - 1.4, (PY0 + PY1) / 2 + 0.1, 0]),
                  T("little", 26, GREY).move_to([PX0 - 0.6, PY0 + 0.55, 0]),
                  T("much", 26, GREY).move_to([PX0 - 0.6, PY1 - 0.45, 0]))
    ybase = PY0 - 0.45
    xlab = VGroup(T("age at tutoring", 26, GREY).move_to([(PX0 + PX1) / 2 + 0.2, ybase, 0]),
                  T("early", 26, GREY).move_to([PX0 + 0.55, ybase, 0]),
                  T("late", 26, GREY).move_to([PX1 - 0.4, ybase, 0]))
    return ax, ylab, xlab


# ---------------------------------------------------------------------------------------------
# shared frames carried from scene to scene
# ---------------------------------------------------------------------------------------------
def s01_objects():
    b = bird(3.2).move_to([-2.2, 0.3, 0])
    by = b.get_bottom()[1] - 0.08
    branch = VGroup(Line([-6.6, by, 0], [2.4, by + 0.1, 0], color=GREY, stroke_width=9),
                    Line([-5.2, by + 0.03, 0], [-5.9, by + 0.7, 0], color=GREY, stroke_width=5),
                    Line([0.6, by + 0.08, 0], [1.4, by + 0.7, 0], color=GREY, stroke_width=5))
    q = T("?", 360, YELLOW, font=TITLE_FONT).move_to([4.9, 0.3, 0])
    return b, branch, q


def chamber(center, w=1.9, h=1.35, color=BLUE, bscale=0.5, foam=False):
    """A sound-isolated chamber: a thick, filled wall (with foam ticks when large) around a dark room."""
    t = 0.3 if foam else 0.17
    outer = RoundedRectangle(corner_radius=0.18, width=w, height=h, stroke_color=GREY, stroke_width=3.5,
                             fill_color=GREY, fill_opacity=0.4)
    inner = RoundedRectangle(corner_radius=0.1, width=w - 2 * t, height=h - 2 * t, stroke_color=GREY, stroke_width=1.5,
                             fill_color=PANEL, fill_opacity=1)
    b = bird(bscale, color).move_to(outer.get_center())
    parts = [outer, inner, b]
    if foam:
        ticks = VGroup()
        for xx in np.linspace(-w / 2 + 0.45, w / 2 - 0.45, 9):
            ticks.add(Line([xx, h / 2 - t + 0.04, 0], [xx + 0.18, h / 2 - 0.04, 0], color=GREY, stroke_width=2.5),
                      Line([xx, -h / 2 + t - 0.04, 0], [xx + 0.18, -h / 2 + 0.04, 0], color=GREY, stroke_width=2.5))
        for yy in np.linspace(-h / 2 + 0.45, h / 2 - 0.45, 7):
            ticks.add(Line([-w / 2 + t - 0.04, yy, 0], [-w / 2 + 0.04, yy + 0.18, 0], color=GREY, stroke_width=2.5),
                      Line([w / 2 - t + 0.04, yy, 0], [w / 2 - 0.04, yy + 0.18, 0], color=GREY, stroke_width=2.5))
        parts.insert(2, ticks)
        grp = VGroup(outer, inner, ticks, b)
    else:
        grp = VGroup(outer, inner, b)
    return grp.move_to([center[0], center[1], 0])


def big_chambers():
    return [chamber([x, -0.1], w=4.0, h=4.2, bscale=1.25, foam=True) for x in (-4.4, 0.0, 4.4)]


ROW_Y = [2.1, 0.45, -1.2]
CH_X = -5.2          # chamber centres in the rows layout
TL0, TL1 = -3.9, 3.0  # each row's age line
AD_X = 4.95          # adult spectrogram panels
TAPE_EARLY, TAPE_LATE = -3.0, 0.4
NONE_X = -0.8


def row_line(y):
    return link([TL0, y, 0], [TL1, y, 0], GREY, 4)


def rows_layout():
    """Three chambers with their age lines and empty adult panels (no tapes)."""
    chs = [chamber([CH_X, y], w=2.1, h=1.45, bscale=0.55) for y in ROW_Y]
    lines = [row_line(y) for y in ROW_Y]
    ads = [spectrogram("simple", [AD_X, y], w=2.7, h=1.4, with_traces=False) for y in ROW_Y]
    return chs, lines, ads


def age_axis():
    """One shared age axis under the three rows: ticks at hatching and adult."""
    y = -2.3
    line = link([TL0, y, 0], [TL1 + 0.05, y, 0], GREY, 3)
    t0 = Line([TL0, y - 0.1, 0], [TL0, y + 0.1, 0], color=GREY, stroke_width=3)
    t1 = Line([TL1, y - 0.1, 0], [TL1, y + 0.1, 0], color=GREY, stroke_width=3)
    l0 = T("hatching", 26, GREY).move_to([TL0, y - 0.45, 0])
    l1 = T("adult", 26, GREY).move_to([TL1, y - 0.45, 0])
    mid = T("age (days after hatching)", 26, GREY).move_to([(TL0 + TL1) / 2 + 0.1, y - 0.45, 0])
    return VGroup(line, t0, t1, l0, l1, mid)


def tape_on(x, y, s=0.9):
    return tape(s).move_to([x, y + 0.32, 0])


def fwd_arrows():
    return [link([TL1 + 0.05, y, 0], [AD_X - 1.45, y, 0], GREY, 4) for y in ROW_Y]


def pq_objects():
    """Everything on screen at the end of the predict scene (rebuilt by the pause and the reveal)."""
    chs, lines, ads = rows_layout()
    tapes = [tape_on(TAPE_EARLY, ROW_Y[0]), tape_on(TAPE_LATE, ROW_Y[1])]
    none_mark = no_tape([NONE_X, ROW_Y[2] + 0.32])
    names = [lab("early tape", 26, YELLOW, (TL0 + 0.9, ROW_Y[0] - 0.42)),
             lab("later tape", 26, YELLOW, (TL0 + 0.9, ROW_Y[1] - 0.42)),
             lab("no tape", 26, GREY, (TL0 + 0.8, ROW_Y[2] - 0.42))]
    qs = [T("?", 60, YELLOW, font=TITLE_FONT).move_to(a[0].get_center()) for a in ads]
    axis = age_axis()
    adlab = lab("adult song", 26, GREEN, (AD_X, ROW_Y[0] + 0.95))
    pred = lab("Predict", 36, GOLD, (0, 3.3), font=TITLE_FONT)
    question = lab("Which ones sing a good copy?", 30, TEXT, (0, -3.4), font=TITLE_FONT)
    return chs, lines, ads, tapes, none_mark, names, qs, axis, adlab, pred, question


def phase_axis():
    return VGroup(link([-6.5, -2.6, 0], [6.5, -2.6, 0], GREY, 3), lab("age", 26, GREY, (6.0, -3.0)))


def band(x0, x1, color, y0=-1.9, y1=3.2, dashed=False, fill=0.1):
    r = Rectangle(width=x1 - x0, height=y1 - y0, stroke_color=color, stroke_width=3, fill_color=color,
                  fill_opacity=fill).move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])
    return DashedVMobject(r, num_dashes=44, dashed_ratio=0.55) if dashed else r


def lstage_content():
    """Sensory-phase band content: ear (labelled), the tutor song heard (yellow), the memory kept (purple)."""
    e = ear(1.6, YELLOW).move_to([-5.55, 0.7, 0])
    e_lab = lab("ear", 26, YELLOW, (-5.55, -0.45))
    heard = wave(-4.65, 0.55, 2.1, rich, YELLOW, 0.5, 5)
    mem = wave(-2.35, 0.55, 1.75, rich, PURPLE, 0.5, 5)
    mem_lab = lab("memory", 26, PURPLE, (-1.5, -0.45))
    return VGroup(e, e_lab), heard, mem, mem_lab


# =============================================================================================
# scenes
# =============================================================================================
class S00Title(TitleCard):
    LESSON = "Sensitive Periods in Behavior: Song, Language and Sight"
    TITLE = "One Input, Many Ages"


class S01Q(SpokenScene):
    def construct(self):
        b, branch, q = s01_objects()
        self.play(FadeIn(b, shift=DOWN * 0.3), Create(branch), run_time=0.9)
        self.at("catch up")
        self.play(GrowFromCenter(q), run_time=0.6)
        self.at("never heard")
        self.play(Indicate(q, color=YELLOW, scale_factor=1.08), run_time=0.7)
        self.finish()


class S02Hook(SpokenScene):
    def construct(self):
        b, branch, q = s01_objects()
        self.add(b, branch, q)
        name = lab("male white-crowned sparrow", 30, BLUE, (-1.9, b.get_bottom()[1] - 0.6))
        self.at("A male")
        self.play(FadeIn(name), run_time=0.5)
        # the isolate panel arrives centred; it slides right when the wild panel enters
        iso = spectrogram("simple", [0, 0.55], w=6.2, h=4.5, color=BLUE, with_traces=True, axes=True)
        iso_lab = lab("raised without adult song", 30, BLUE, (0, -2.1))
        iso_all = VGroup(iso, iso_lab)
        self.at("raised without adult song")
        self.play(FadeOut(name), FadeOut(q), FadeOut(branch), FadeOut(b), p_in(iso), FadeIn(iso_lab), run_time=0.9)
        self.at("still sings")
        self.play(draw_song(iso, 1.3))
        wild = spectrogram("wild", [-3.55, 0.55], w=6.2, h=4.5, color=GREEN, axes=True)
        wild_lab = lab("wild song", 30, GREEN, (-3.55, -2.1))
        self.at("But its song")
        self.play(iso_all.animate.shift(RIGHT * 3.55), p_in(wild), FadeIn(wild_lab), draw_song(wild, 0.8), run_time=0.75)
        simple_lab = lab("simple, abnormal", 30, RED, (3.55, -2.75))
        self.at("simple and abnormal")
        self.play(iso[1].animate.set_color(RED), FadeIn(simple_lab), run_time=0.7)
        self.finish()


def bird_points(b, sc):
    """The ear patch and the throat (syrinx) on a bird built with bird(sc)."""
    hc = b[2].get_center()
    return hc + np.array([-0.1, -0.03, 0]) * sc, hc + np.array([-0.04, -0.66, 0]) * sc


class S03Notdeaf(SpokenScene):
    def construct(self):
        iso = spectrogram("simple", [4.1, 0.45], w=4.4, h=4.2, color=RED)
        iso_lab = lab("still simple", 30, RED, (4.1, -2.0))
        b = bird(2.1).move_to([-1.9, 0.45, 0])
        ear_pt, syr_pt = bird_points(b, 2.1)
        self.add(iso, b)
        spk = speaker(1.0, GREY).move_to([-6.3, 0.45, 0])
        arcs = VGroup(*[Arc(radius=r, start_angle=-PI / 5, angle=2 * PI / 5, color=YELLOW, stroke_width=6).move_arc_center_to([-5.75, 0.45, 0])
                        for r in (0.5, 0.85, 1.2)])
        tp = tape(0.8).move_to([-6.3, 1.5, 0])
        self.at("The right song played later")
        self.play(FadeIn(spk), FadeIn(tp), LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.4), run_time=1.2)
        self.at("does little")
        self.play(Indicate(iso[1], color=RED, scale_factor=1.03), FadeIn(iso_lab), run_time=0.8)
        # hearing works: ring on the ear, arrow from the label above, check
        ear_ring = Circle(radius=0.2, stroke_color=GREEN, stroke_width=5).move_to(ear_pt)
        ear_txt = lab("hearing works", 30, TEXT, (-2.2, 3.0))
        ear_ck = check([ear_txt.get_left()[0] - 0.45, 3.0, 0], GREEN, 0.28)
        ear_ar = link([ear_pt[0] - 0.1, 2.65, 0], [ear_pt[0] - 0.05, ear_pt[1] + 0.3, 0], GREEN, 5)
        self.at("not deaf")
        self.play(Create(ear_ring), FadeIn(ear_txt), GrowArrow(ear_ar), Create(ear_ck), run_time=0.7)
        syr_ring = Circle(radius=0.2, stroke_color=GREEN, stroke_width=5).move_to(syr_pt)
        syr_txt = lab("vocal organ (syrinx) works", 30, TEXT, (-1.6, -2.45))
        syr_ck = check([syr_txt.get_left()[0] - 0.45, -2.45, 0], GREEN, 0.28)
        syr_ar = link([syr_pt[0] + 0.05, -2.05, 0], [syr_pt[0] + 0.02, syr_pt[1] - 0.3, 0], GREEN, 5)
        self.at("its voice works")
        self.play(Create(syr_ring), FadeIn(syr_txt), GrowArrow(syr_ar), Create(syr_ck), run_time=0.7)
        # Both completed checks remain visible for at least two seconds.
        self.wait(2.0)
        self.finish()


class S04Missed(SpokenScene):
    def construct(self):
        base = -0.9
        axis = link([-6.3, base, 0], [6.4, base, 0], GREY, 5)
        axl = lab("the bird's life", 30, GREY, (4.6, base - 0.6))
        box = band(-6.3, 0.3, YELLOW, y0=base, y1=3.0, dashed=True, fill=0.0)
        block = Rectangle(width=6.6, height=0.34, stroke_width=0, fill_color=YELLOW, fill_opacity=1.0).move_to([-3.0, base, 0])
        miss_tape = VGroup(tape(2.6, YELLOW, 0.25), cross([0, 0, 0], RED, 0.65, 8)).move_to([-3.0, 0.8, 0])
        miss = lab("the experience: missed", 36, YELLOW, (-3.0, 2.4), weight=BOLD)
        # The complete missed early interval is visible from the first frame.
        self.add(axis, axl, box, block, miss, miss_tape)
        right = lab("at the right age", 34, YELLOW, (-3.0, base - 0.6), weight=BOLD)
        self.at("at the right age")
        self.play(FadeIn(right), Indicate(block, color=YELLOW, scale_factor=1.04), run_time=0.5)
        self.finish()


class S05Marler(SpokenScene):
    def construct(self):
        name = T("Peter Marler", 66, TEXT, font=TITLE_FONT)
        yrs = T("1960s and 1970s", 34, GREY)
        credit = VGroup(name, yrs).arrange(DOWN, buff=0.25).move_to([0, 1.2, 0])
        self.play(FadeIn(credit, shift=DOWN * 0.15), run_time=0.7)
        when = T("when?", 130, YELLOW, font=TITLE_FONT).move_to([0, -1.5, 0])
        self.at("when it must come")
        self.play(FadeIn(when, shift=UP * 0.1), run_time=0.5)
        chs = big_chambers()
        self.at("He raised young sparrows")
        self.play(credit.animate.scale(0.6).move_to([-3.6, 3.15, 0]), when.animate.scale(0.38).move_to([3.0, 3.1, 0]),
                  LaggedStart(*[FadeIn(c) for c in chs], lag_ratio=0.3), run_time=1.3)
        walls = lab("sound-isolated chambers", 36, GREY, (0, -2.85))
        self.at("sound isolated chambers")
        self.play(FadeIn(walls), *[Indicate(c[0], color=GREY, scale_factor=1.02) for c in chs], run_time=0.6)
        self.finish()


class S06Design(SpokenScene):
    def construct(self):
        big = big_chambers()
        self.add(*big)
        chs, lines, ads = rows_layout()
        axis = age_axis()
        self.play(*[ReplacementTransform(big[i], chs[i]) for i in range(3)],
                  *[GrowArrow(l) for l in lines], FadeIn(axis), run_time=0.7)
        t1 = tape(0.9).move_to([TAPE_EARLY, ROW_Y[0] + 2.4, 0])
        t2 = tape(0.9).move_to([TAPE_LATE, ROW_Y[1] + 1.8, 0])
        song = lab("recorded song", 26, YELLOW, (TAPE_EARLY + 0.2, ROW_Y[0] + 0.98))
        self.at("recorded song")
        self.play(FadeIn(t1), run_time=0.1)
        self.play(t1.animate.move_to([TAPE_EARLY, ROW_Y[0] + 0.32, 0]), FadeIn(song), run_time=0.45)
        self.at("at chosen ages")
        self.play(FadeIn(t2), run_time=0.1)
        none = no_tape([NONE_X, ROW_Y[2] + 0.32])
        none_lab = lab("no tape", 26, GREY, (TL0 + 0.8, ROW_Y[2] - 0.42))
        self.play(t2.animate.move_to([TAPE_LATE, ROW_Y[1] + 0.32, 0]), FadeIn(none), FadeIn(none_lab), run_time=0.5)
        fwd = fwd_arrows()
        self.at("Then he waited")
        self.play(*[GrowArrow(f) for f in fwd], run_time=0.9)
        adlab = lab("adult song", 26, GREEN, (AD_X, ROW_Y[0] + 0.95))
        self.at("recorded what they sang")
        self.play(*[FadeIn(a) for a in ads], FadeIn(adlab), run_time=0.8)
        self.finish()


class S07Pq(SpokenScene):
    def construct(self):
        chs, lines, ads, tapes, none_mark, names, qs, axis, adlab, pred, question = pq_objects()
        # carried from the design scene: chambers, age lines, tapes, crossed-out chip, empty adult panels (rebuilt in place)
        self.add(*chs, *lines, *ads, *tapes, *fwd_arrows(), axis, none_mark, adlab)
        self.play(FadeIn(pred), run_time=0.4)
        hl = [SurroundingRectangle(VGroup(chs[i], lines[i], ads[i]), buff=0.06, color=YELLOW, stroke_width=3, corner_radius=0.1)
              for i in range(3)]
        self.at("heard the tape early")
        self.play(FadeIn(names[0]), FadeIn(hl[0]), run_time=0.5)
        self.at("some later")
        self.play(FadeOut(hl[0]), FadeIn(names[1]), FadeIn(hl[1]), run_time=0.5)
        self.at("some never")
        self.play(FadeOut(hl[1]), FadeIn(names[2]), FadeIn(hl[2]), run_time=0.5)
        self.at("Which ones sing a good copy")
        self.play(FadeOut(hl[2]), FadeIn(question), *[FadeIn(q) for q in qs], run_time=0.8)
        self.finish()


class S08Pause(NarratedScene):
    def construct(self):
        chs, lines, ads, tapes, none_mark, names, qs, axis, adlab, pred, question = pq_objects()
        self.add(*chs, *lines, *ads, *tapes, *fwd_arrows(), axis, *names, none_mark, *qs, adlab, pred, question)
        self.finish()


class S09Rev(SpokenScene):
    def construct(self):
        chs, lines, ads, tapes, none_mark, names, qs, axis, adlab, pred, question = pq_objects()
        old = VGroup(*chs, *lines, *ads, *tapes, *fwd_arrows(), axis, *names, none_mark, *qs, adlab, pred, question)
        self.add(old)
        py, ph = 1.2, 3.5
        tut = spectrogram("wild", [-3.4, py], w=6.0, h=ph, color=YELLOW)
        adult = spectrogram("wild", [3.4, py], w=6.0, h=ph, color=GREEN, with_traces=True)
        slot = DashedVMobject(RoundedRectangle(corner_radius=0.14, width=6.0, height=ph, stroke_color=GREEN, stroke_width=3,
                                               stroke_opacity=0.6).move_to([3.4, py, 0]), num_dashes=46, dashed_ratio=0.55)
        slot_lab = lab("adult song: ?", 30, GREEN, (3.4, py)).set_opacity(0.7)
        tut_lab = lab("tutor song on the tape", 30, YELLOW, (-3.4, 3.3))
        ad_lab = lab("adult song: a good copy", 30, GREEN, (3.4, 3.3))
        arr = link([-0.2, py, 0], [0.2, py, 0], GREY, 5)
        tl = link([-6.3, -2.2, 0], [6.3, -2.2, 0], GREY, 4)
        tp = tape(0.9).move_to([-5.4, -1.88, 0])
        first = Dot([3.9, -2.2, 0], radius=0.14, color=BLUE)
        heard_lab = lab("heard the tape early", 26, YELLOW, (-4.2, -2.78))
        sang_lab = lab("first sang", 26, BLUE, (3.9, -2.78))
        mon = DoubleArrow([-4.7, -1.4, 0], [3.6, -1.4, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.2)
        mon_lab = lab("months pass", 30, GREY, (-0.5, -0.95))
        self.at("Birds that heard song early")
        self.play(FadeOut(old), FadeIn(tut[0]), draw_song(tut, 0.9), FadeIn(tut_lab), Create(tl), FadeIn(tp),
                  FadeIn(heard_lab), FadeIn(slot), FadeIn(slot_lab), run_time=0.9)
        self.at("sang good copies")
        self.play(FadeOut(slot), FadeOut(slot_lab), GrowArrow(arr), FadeIn(adult[0]), FadeIn(ad_lab), draw_song(adult, 1.2), run_time=1.2)
        self.at("though months passed")
        self.play(GrowArrow(mon), FadeIn(mon_lab), run_time=0.7)
        self.at("before they first sang")
        self.play(FadeIn(first, scale=2.0), FadeIn(sang_lab), run_time=0.5)
        self.finish()


class S10Rev2(SpokenScene):
    def construct(self):
        cxl, cxr = -3.4, 3.4
        ph, py = 4.0, -0.35
        lead_l = lab("tape played to older birds", 30, YELLOW, (cxl, 3.15))
        tl_l = link([cxl - 2.7, 2.1, 0], [cxl + 2.7, 2.1, 0], GREY, 4)
        tp = tape(0.9).move_to([cxl + 1.2, 2.42, 0])
        pl = spectrogram("poor", [cxl, py], w=5.8, h=ph, color=RED)
        lead_r = lab("no adult song heard", 30, GREY, (cxr, 3.15))
        tl_r = link([cxr - 2.7, 2.1, 0], [cxr + 2.7, 2.1, 0], GREY, 4)
        nt = no_tape([cxr, 2.42])
        pr = spectrogram("simple", [cxr, py], w=5.8, h=ph, color=RED)
        slot = DashedVMobject(RoundedRectangle(corner_radius=0.14, width=5.8, height=ph, stroke_color=GREY, stroke_width=3,
                                               stroke_opacity=0.5).move_to([cxr, py, 0]), num_dashes=46, dashed_ratio=0.55)
        little = lab("little effect", 36, RED, (cxl, -2.75), weight=BOLD)
        abn = lab("abnormal", 36, RED, (cxr, -2.75), weight=BOLD)
        # the older-bird column is on screen from the first word, with its empty panel
        self.play(FadeIn(lead_l), GrowArrow(tl_l), FadeIn(tp, shift=DOWN * 0.4), FadeIn(pl[0]), FadeIn(slot), run_time=0.8)
        self.at("had little effect")
        self.play(draw_song(pl, 0.9), FadeIn(little), run_time=0.9)
        self.at("Birds that heard no adult song")
        self.play(FadeIn(lead_r), GrowArrow(tl_r), FadeIn(nt), FadeOut(slot), FadeIn(pr[0]), run_time=0.8)
        self.at("sang simple")
        self.play(draw_song(pr, 1.2), run_time=1.2)
        self.at("abnormal songs")
        self.play(FadeIn(abn), Indicate(pr[1], color=RED, scale_factor=1.03), run_time=0.6)
        self.finish()


MK_XS = [-4.3, 0.0, 4.3]
MK_PY, MK_PH, MK_PW = 0.0, 4.0, 4.1


def marks_objects():
    tp = tape(1.1).move_to([0, 3.1, 0])
    same = lab("the same tape", 30, YELLOW, (2.4, 3.1))
    ytop = 2.55
    labs = [lab_top("tutored early", 30, YELLOW, MK_XS[0], ytop), lab_top("tutored later", 30, YELLOW, MK_XS[1], ytop),
            lab_top("never tutored", 30, YELLOW, MK_XS[2], ytop)]
    arrs = [link([x * 0.2, 2.95, 0], [x, 2.72, 0], YELLOW, 3) for x in MK_XS]
    panels = [spectrogram("wild", [MK_XS[0], MK_PY], w=MK_PW, h=MK_PH, color=GREEN, sw=7.5),
              spectrogram("poor", [MK_XS[1], MK_PY], w=MK_PW, h=MK_PH, color=RED, sw=7.5),
              spectrogram("simple", [MK_XS[2], MK_PY], w=MK_PW, h=MK_PH, color=RED, sw=7.5)]
    return tp, same, labs, arrs, panels


class S12Marks(SpokenScene):
    def construct(self):
        tp, same, labs, arrs, panels = marks_objects()
        self.play(FadeIn(tp, shift=DOWN * 0.3), FadeIn(same), run_time=0.5)
        self.at("at different ages")
        self.play(*[GrowArrow(a) for a in arrs], *[FadeIn(l) for l in labs], *[FadeIn(p[0]) for p in panels], run_time=0.6)
        self.at("left very different marks")
        self.play(*[draw_song(p, 0.8) for p in panels], run_time=0.8)
        self.finish()


class S13Beat(NarratedScene):
    def construct(self):
        tp, same, labs, arrs, panels = marks_objects()
        self.add(tp, same, *labs, *arrs, *panels)
        self.finish()


class S14aPhases(SpokenScene):
    def construct(self):
        axis = phase_axis()
        self.play(Create(axis), run_time=0.6)
        whole = band(-6.4, 6.4, GREY, dashed=True, fill=0.0)
        learn = lab("learning", 48, GREY, (0, 0.65), font=TITLE_FONT)
        self.at("splits learning")
        self.play(Create(whole), FadeIn(learn), run_time=0.7)
        bl = band(-6.4, -0.2, GREY, dashed=True, fill=0.0)
        br = band(0.2, 6.4, GREY, dashed=True, fill=0.0)
        self.at("into two phases")
        self.play(FadeOut(learn), ReplacementTransform(whole, VGroup(bl, br)), run_time=0.8)
        bl_f = band(-6.4, -0.2, YELLOW)
        title = lab("sensory phase", 38, YELLOW, (-3.3, 2.6), weight=BOLD)
        self.at("First a sensory phase")
        self.play(ReplacementTransform(bl, bl_f), FadeIn(title), run_time=0.8)
        e, heard, mem, mem_lab = lstage_content()
        sub = lab("listen and memorize", 30, TEXT, (-3.3, 2.0))
        self.at("The bird listens")
        self.play(FadeIn(sub), FadeIn(e, shift=RIGHT * 0.2), Create(heard), run_time=0.9)
        self.at("memorizes")
        self.play(TransformFromCopy(heard, mem), FadeIn(mem_lab), run_time=1.0)
        self.finish()


def dim_anims(group, f):
    """Dim every piece by factor f without turning open curves into filled shapes."""
    out = []
    for m in group.family_members_with_points():
        out.append(m.animate.set_fill(opacity=m.get_fill_opacity() * f).set_stroke(opacity=m.get_stroke_opacity() * f))
    return out


def sensory_band_static():
    bl_f = band(-6.4, -0.2, YELLOW)
    title = lab("sensory phase", 38, YELLOW, (-3.3, 2.6), weight=BOLD)
    sub = lab("listen and memorize", 30, TEXT, (-3.3, 2.0))
    e, heard, mem, mem_lab = lstage_content()
    return VGroup(bl_f, title, sub, e, heard, mem, mem_lab)


BW_X0, BW_L = 2.1, 4.1      # the right band's waves: labels at the left, waves across the rest of the band
BW_TY, BW_PY, BW_A = 0.85, -0.95, 0.55


class S14bPhases2(SpokenScene):
    def construct(self):
        axis = phase_axis()
        left = sensory_band_static()
        br = band(0.2, 6.4, GREY, dashed=True, fill=0.0)
        self.add(axis, left, br)
        br_f = band(0.2, 6.4, BLUE)
        title = lab("sensorimotor phase", 38, BLUE, (3.3, 2.6), weight=BOLD)
        self.at("Then a sensory motor phase")
        self.play(ReplacementTransform(br, br_f), FadeIn(title), *dim_anims(left, 0.4), run_time=0.9)
        sub = lab("practice and match", 30, TEXT, (3.3, 2.0))
        pr_lab = lab("practice", 28, BLUE, (1.2, BW_PY))
        tgt_lab = lab("memory", 28, PURPLE, (1.2, BW_TY))
        prac = wave(BW_X0, BW_PY, BW_L, rambling, BLUE, BW_A, 5)
        self.at("It practices")
        self.play(FadeIn(sub), Create(prac), FadeIn(pr_lab), run_time=0.9)
        target = wave(BW_X0, BW_TY, BW_L, rich, PURPLE, BW_A, 5)
        self.at("shaping rambling sounds")
        self.play(Create(target), FadeIn(tgt_lab), run_time=0.7)
        self.at("until they match the memory")
        # a dashed copy of the memory sits behind the practice row, so the tightening is visible against it
        self.play(FadeIn(ghost(wave(BW_X0, BW_PY, BW_L, rich, PURPLE, BW_A, 5), 0.6)), run_time=0.3)
        for a in (0.4, 0.75, 1.0):
            self.play(Transform(prac, wave(BW_X0, BW_PY, BW_L, mixed(a), BLUE, BW_A, 5)), run_time=0.45)
            self.wait(0.12)
        self.finish()


def konishi_frame():
    bl = band(-6.4, -2.1, YELLOW, y0=-1.7, y1=2.2)
    br = band(2.1, 6.4, BLUE, y0=-1.7, y1=2.2, dashed=True, fill=0.0)
    tl = lab("hears a tutor", 32, YELLOW, (-4.25, 1.6), weight=BOLD)
    hw = wave(-5.9, 0.0, 3.3, rich, YELLOW, 0.5, 5)
    tr = lab("practice phase", 32, BLUE, (4.25, 1.6), weight=BOLD)
    return bl, br, tl, hw, tr


class S14cKonishi(SpokenScene):
    def construct(self):
        bl, br, tl, hw, tr = konishi_frame()
        ax = link([-6.5, -2.55, 0], [6.5, -2.55, 0], GREY, 3)
        age = lab("age", 26, GREY, (6.0, -3.0))
        q = lab("What does practice need?", 40, TEXT, (0, 3.05), font=TITLE_FONT)
        self.play(FadeIn(q), FadeIn(bl), FadeIn(tl), Create(hw), FadeIn(br), FadeIn(tr), Create(ax), FadeIn(age), run_time=0.4)
        qm = T("?", 120, BLUE, font=TITLE_FONT).move_to([4.25, 0.0, 0])
        self.at("practice need")
        self.play(GrowFromCenter(qm), run_time=0.5)
        credit = VGroup(T("Masakazu Konishi", 40, TEXT, font=TITLE_FONT)).move_to([0, 3.05, 0])
        self.at("Masakazu")
        self.play(FadeOut(q), FadeIn(credit, shift=DOWN * 0.1), run_time=0.6)
        deaf = VGroup(ear(2.0, RED), cross([0.0, 0.0, 0], RED, 0.8, 8)).move_to([0, 0.45, 0])
        deaf_lab = lab("deafened ear", 34, RED, (0, -1.0), weight=BOLD)
        self.at("deafened young sparrows")
        self.play(FadeIn(deaf, scale=1.4), FadeIn(deaf_lab), run_time=0.8)
        a1 = link([-2.0, 0.3, 0], [-1.2, 0.3, 0], GREY, 4)
        a2 = link([1.2, 0.3, 0], [2.0, 0.3, 0], GREY, 4)
        self.at("after they heard a tutor")
        self.play(Indicate(hw, color=YELLOW, scale_factor=1.03), GrowArrow(a1), run_time=0.8)
        self.at("but before they practiced")
        self.play(GrowArrow(a2), Indicate(tr, color=BLUE, scale_factor=1.08), run_time=0.8)
        self.finish()


class S14dKonishi2(SpokenScene):
    def construct(self):
        pw, ph, py = 6.0, 4.4, -0.1
        pl = spectrogram("disorder", [-3.4, py], w=pw, h=ph, color=RED, seed=3)
        pr = spectrogram("disorder", [3.4, py], w=pw, h=ph, color=RED, seed=11)
        ll = lab("heard a tutor,\nthen deafened", 28, RED, (-3.4, 3.0))
        lr = lab("deafened before\never hearing a tutor", 28, RED, (3.4, 3.0))
        both = lab("extremely abnormal, alike", 34, TEXT, (0, -2.85), weight=BOLD)
        # both panels are on screen at once: the right one is an empty box until its song is drawn
        self.play(FadeIn(ll), FadeIn(pl[0]), FadeIn(pr[0]), draw_song(pl, 1.3), run_time=1.3)
        self.at("no better than those of birds")
        self.play(FadeIn(lr), draw_song(pr, 1.3), run_time=1.3)
        self.at("deafened before ever hearing a tutor")
        self.play(FadeIn(both), Indicate(pr[1], color=RED, scale_factor=1.02), run_time=0.6)
        self.finish()


TP_X0, TP_L, TP_A = -4.6, 10.4, 0.6
TP_YS = (2.15, 0.1, -1.95)


def tmpl_row_marks():
    ys = TP_YS
    e = VGroup(ear(1.3, BLUE).move_to([-5.9, ys[1] + 0.15, 0]), lab("ear", 26, BLUE, (-5.9, ys[1] - 0.7)))
    de = VGroup(VGroup(ear(1.3, RED), cross([0, 0, 0], RED, 0.6, 7)).move_to([-5.9, ys[2] + 0.15, 0]),
                T("deafened\near", 26, RED).move_to([-5.9, ys[2] - 1.05, 0]))
    return e, de


class S14eTemplate(SpokenScene):
    def construct(self):
        ys = TP_YS
        tmpl = wave(TP_X0, ys[0], TP_L, rich, PURPLE, TP_A, 5)
        hear = wave(TP_X0, ys[1], TP_L, rambling, BLUE, TP_A, 5)
        deaf = wave(TP_X0, ys[2], TP_L, wander(0), RED, TP_A, 5)
        e, de = tmpl_row_marks()
        hear_lab = lab("hears itself", 28, BLUE, (-3.2, ys[1] + 0.9))
        deaf_lab = lab("deafened", 28, RED, (-3.7, ys[2] + 0.9))
        gh1 = ghost(wave(TP_X0, ys[1], TP_L, rich, PURPLE, TP_A, 5), 0.55, 120)
        gh2 = ghost(wave(TP_X0, ys[2], TP_L, rich, PURPLE, TP_A, 5), 0.55, 120)
        self.play(Create(tmpl), run_time=0.3)
        self.at("bird must hear")
        self.play(Create(hear), FadeIn(e), FadeIn(hear_lab), run_time=0.7)
        self.at("to match its practice")
        self.play(Create(deaf), FadeIn(de), FadeIn(deaf_lab), FadeIn(gh1), FadeIn(gh2), run_time=0.5)
        rest = 1.85 - self.elapsed()
        if rest > 0.02:
            self.wait(rest)
        # three overlays of the practice wave: rambling (above), closer, matched; the deafened one only wanders
        self.play(Transform(hear, wave(TP_X0, ys[1], TP_L, mixed(0.5), BLUE, TP_A, 5)),
                  Transform(deaf, wave(TP_X0, ys[2], TP_L, wander(1), RED, TP_A, 5)), run_time=0.35)
        tl = lab("stored memory", 30, PURPLE, (-3.3, ys[0] + 0.95))
        self.at("stored memory")
        self.play(FadeIn(tl),
                  Transform(hear, wave(TP_X0, ys[1], TP_L, mixed(1.0), BLUE, TP_A, 5)),
                  Transform(deaf, wave(TP_X0, ys[2], TP_L, wander(2), RED, TP_A, 5)), run_time=0.4)
        tl2 = lab("template", 36, PURPLE, (-3.9, ys[0] + 0.95), weight=BOLD)
        self.at("a template")
        self.play(ReplacementTransform(tl, tl2), Indicate(tmpl, color=PURPLE, scale_factor=1.02), run_time=0.7)
        self.finish()


class S14fBeat(NarratedScene):
    def construct(self):
        ys = TP_YS
        tmpl = wave(TP_X0, ys[0], TP_L, rich, PURPLE, TP_A, 5)
        hear = wave(TP_X0, ys[1], TP_L, mixed(1.0), BLUE, TP_A, 5)
        deaf = wave(TP_X0, ys[2], TP_L, wander(2), RED, TP_A, 5)
        e, de = tmpl_row_marks()
        self.add(tmpl, ghost(wave(TP_X0, ys[1], TP_L, rich, PURPLE, TP_A, 5), 0.55, 120),
                 ghost(wave(TP_X0, ys[2], TP_L, rich, PURPLE, TP_A, 5), 0.55, 120), hear, deaf, e, de,
                 lab("hears itself", 28, BLUE, (-3.2, ys[1] + 0.9)), lab("deafened", 28, RED, (-3.7, ys[2] + 0.9)),
                 lab("template", 36, PURPLE, (-3.9, ys[0] + 0.95), weight=BOLD))
        self.finish()


class S15Plot(SpokenScene):
    def construct(self):
        ax, ylab, xlab = plot_axes()
        self.play(Create(ax), run_time=0.8)
        self.at("Plot what lasts")
        self.play(FadeIn(ylab), run_time=0.6)
        self.at("against the age")
        self.play(FadeIn(xlab), run_time=0.6)
        c_step = curve(step_val, TEAL, 6, dashed=True, opacity=0.5)
        c_ramp = curve(ramp_val, TEAL, 6, dashed=True, opacity=0.5)
        self.at("the input was given")
        self.play(Create(c_step), Create(c_ramp), run_time=1.4)
        self.finish()


def plot_static(step_style="ghost", ramp_style="ghost"):
    ax, ylab, xlab = plot_axes()
    objs = [ax, ylab, xlab]
    c_step = curve(step_val, TEAL, 7 if step_style == "bold" else 6, dashed=(step_style != "bold"), opacity=1 if step_style == "bold" else 0.5)
    c_ramp = curve(ramp_val, TEAL, 7 if ramp_style == "bold" else 6, dashed=(ramp_style != "bold"), opacity=1 if ramp_style == "bold" else 0.5)
    return objs, c_step, c_ramp


STEP_X = pt(0.45, 0)[0]
DOOR_TOP = pt(0, 1.0)[1]
DOOR_BOT = pt(0, 0.05)[1] + 0.12


def door_mob(c):
    """Bright door beside the top of the drop, hinged along its left jamb."""
    xh, yb, H, W = STEP_X - 2.0, 0.9, 1.85, 1.4
    skew = 0.5 * (1 - c)
    leaf = Polygon([xh, yb, 0], [xh + W * c, yb + skew, 0],
                   [xh + W * c, yb + H + skew, 0], [xh, yb + H, 0],
                   stroke_color=DOORC, stroke_width=6,
                   fill_color=DOORC, fill_opacity=0.8)
    hinge = Line([xh, yb - 0.1, 0], [xh, yb + H + 0.1, 0], color=TEXT, stroke_width=10)
    pins = VGroup(*[Dot([xh, yb + H * f, 0], radius=0.08, color=GREY) for f in (0.2, 0.8)])
    knob = Dot([xh + W * c * 0.83, yb + H * 0.45, 0], radius=0.08, color=PANEL)
    return VGroup(leaf, hinge, pins, knob)


class S16Door(SpokenScene):
    def construct(self):
        objs, c_step, c_ramp = plot_static("ghost", "ghost")
        self.add(*objs, c_step, c_ramp)
        bold = curve(step_val, TEAL, 8)
        self.at("that ends abruptly")
        self.play(Create(bold), FadeOut(c_ramp), run_time=1.0)
        t1 = lab("critical period", 38, TEAL, (4.1, 1.9), weight=BOLD)
        t2 = lab("(this course's usage)", 26, GREY, (4.1, 1.3))
        cv = ValueTracker(0.12)
        door = always_redraw(lambda: door_mob(cv.get_value()))
        self.at("a critical period")
        self.add(door)
        self.play(FadeIn(t1), FadeIn(t2), run_time=0.6)
        self.at("like a door")
        self.play(cv.animate.set_value(1.0), run_time=1.1, rate_func=smooth)
        self.wait(1.0)
        self.finish()


def tide_icon(level):
    """A tide gauge: sea in a box, a dashed line at the old high-water mark; level in [0, 1]."""
    cx, cy, w, h = 4.35, 1.95, 3.6, 2.5
    x0, x1, yb = cx - w / 2, cx + w / 2, cy - h / 2
    top = yb + 0.1 + level * (h - 0.35)
    xs = np.linspace(x0, x1, 40)
    wave_top = [[x, top + 0.07 * np.sin(5 * x + 3 * level), 0] for x in xs]
    water = Polygon(*([[x0, yb, 0]] + wave_top + [[x1, yb, 0]]), stroke_width=0, fill_color=TEAL, fill_opacity=0.5)
    topline = VMobject(stroke_color=TEAL, stroke_width=4).set_points_as_corners(wave_top)
    frame = Rectangle(width=w, height=h, stroke_color=GREY, stroke_width=3).move_to([cx, cy, 0])
    mark = DashedLine([x0, yb + 0.1 + (h - 0.35), 0], [x1, yb + 0.1 + (h - 0.35), 0], color=GREY, stroke_width=3)
    return VGroup(water, topline, frame, mark)


class S17Tide(SpokenScene):
    def construct(self):
        objs, c_step, c_ramp = plot_static("ghost", "ghost")
        self.add(*objs, c_step, c_ramp)
        bold = curve(ramp_val, TEAL, 8)
        self.at("A window that fades gradually")
        self.play(Create(bold), FadeOut(c_step), run_time=1.5)
        t1 = lab("sensitive period", 36, TEAL, (4.1, 0.2), weight=BOLD)
        t2 = lab("(this course's usage)", 26, GREY, (4.1, -0.4))
        u = ValueTracker(0.0)
        lv = lambda: (ramp_val(u.get_value()) - 0.05) / 0.95
        tide = always_redraw(lambda: tide_icon(lv()))
        rider = always_redraw(lambda: Dot(pt(u.get_value(), ramp_val(u.get_value())), radius=0.15, color=TEXT))
        self.at("it calls a sensitive period")
        self.add(tide, rider)
        self.play(FadeIn(t1), FadeIn(t2), run_time=0.6)
        self.at("like a tide")
        self.play(u.animate.set_value(1.0), run_time=1.8, rate_func=linear)
        note = VGroup(T("schematic, not data.", 28, TEXT), T("Other authors use", 28, TEXT),
                      T("these terms differently.", 28, TEXT)).arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to([-2.2, -0.75, 0])
        self.at("Researchers also use these terms")
        self.play(FadeIn(note), run_time=0.6)
        self.finish()


class S18Most(SpokenScene):
    def construct(self):
        objs, c_step, c_ramp = plot_static("ghost", "bold")
        self.add(*objs, c_ramp, c_step)
        self.at("The clearest human case")
        self.play(Indicate(c_ramp, color=TEAL, scale_factor=1.02), run_time=0.8)
        gl = VGroup(T("second-language grammar", 28, TEAL, weight=BOLD),
                    T("looks like a tide in the outcome", 26, TEXT),
                    T("schematic; shape remains a question", 26, GREY)).arrange(DOWN, buff=0.1).move_to([3.4, 2.35, 0])
        g_lead = DashedLine([1.6, 1.85, 0], pt(0.52, ramp_val(0.52)), color=TEAL, stroke_width=3)
        self.at("second language grammar")
        self.play(FadeIn(gl), Create(g_lead), run_time=0.6)
        self.at("is a tide in the outcome")
        self.play(Indicate(c_ramp, color=TEAL, scale_factor=1.02), run_time=0.8)
        stepc = curve(step_val, TEAL, 7, dashed=True, opacity=0.9)
        dot_at = pt(0.45, 0.5 * (step_val(0.45) + ramp_val(0.45)))
        dot = Dot(dot_at, radius=0.2, color=BRIGHT)
        dot_ring = Circle(radius=0.34, stroke_color=BRIGHT, stroke_width=4).move_to(dot_at)
        dl_t = T("one summary number", 30, BRIGHT, weight=BOLD)
        dl_bg = RoundedRectangle(corner_radius=0.12, width=dl_t.width + 0.4, height=dl_t.height + 0.3, stroke_color=BRIGHT,
                                 stroke_width=2.5, fill_color=PANEL, fill_opacity=0.95)
        dl = VGroup(dl_bg, dl_t.move_to(dl_bg)).move_to([-2.4, -0.85, 0])
        lead = DashedLine([dl.get_right()[0], dl.get_right()[1] + 0.05, 0], [dot_at[0] - 0.3, dot_at[1] - 0.12, 0], color=BRIGHT, stroke_width=4)
        self.at("Telling them apart")
        self.play(ReplacementTransform(c_step, stepc), run_time=0.5)
        self.play(FadeIn(dot, scale=2.0), Create(dot_ring), Create(lead), FadeIn(dl), run_time=0.5)
        self.at("takes the whole curve")
        self.play(Indicate(c_ramp, color=TEAL, scale_factor=1.02), Indicate(stepc, color=TEAL, scale_factor=1.02), run_time=0.5)
        # Explicit still hold after the final emphasis, including dot and label.
        self.wait(1.5)
        self.finish()


def idea_card():
    return RoundedRectangle(corner_radius=0.3, width=12.4, height=5.6, stroke_color=GOLD, stroke_width=4,
                            fill_color=PANEL, fill_opacity=1).move_to([0, 0, 0])


class S19Idea(SpokenScene):
    def construct(self):
        card = idea_card()
        tag = lab("THE ONE IDEA TO CARRY", 30, GOLD, (0, 2.0), weight=BOLD)
        l1 = lab("Same input,", 66, TEXT, (0, 0.85), font=TITLE_FONT)
        l2 = lab("different ages:", 66, YELLOW, (0, -0.2), font=TITLE_FONT)
        l3 = lab("measure what lasts.", 66, TEAL, (0, -1.25), font=TITLE_FONT)
        self.play(FadeIn(card), FadeIn(tag), run_time=0.6)
        self.at("Same input")
        self.play(FadeIn(l1, shift=UP * 0.1), run_time=0.5)
        self.at("different ages")
        self.play(FadeIn(l2, shift=UP * 0.1), run_time=0.5)
        self.at("measure what lasts")
        self.play(FadeIn(l3, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S20Idea2(SpokenScene):
    def construct(self):
        card = idea_card()
        top = VGroup(lab("Same input, different ages:", 42, TEXT, (0, 0), font=TITLE_FONT),
                     lab("measure what lasts.", 42, TEAL, (0, 0), font=TITLE_FONT)).arrange(DOWN, buff=0.1).move_to([0, 2.05, 0])
        div = Line([-5.6, 1.2, 0], [5.6, 1.2, 0], color=GREY, stroke_width=2)
        b = bird(0.75, BLUE).move_to([-4.8, 0.15, 0])
        a_ = lab("In zebra finches,", 38, YELLOW, (-2.0, 0.55), weight=BOLD)
        a_.align_to([-3.4, 0, 0], LEFT)
        b_ = lab("expected input seems to help end the window.", 30, TEXT, (0, -0.2))
        b_.align_to([-3.4, 0, 0], LEFT)
        tp = tape(1.2).move_to([-4.6, -1.7, 0])
        tp_lab = lab("expected input", 28, YELLOW, (-4.6, -2.3))
        ar = link([-3.6, -1.7, 0], [-2.3, -1.7, 0], YELLOW, 5)
        endc = VMobject(stroke_color=TEAL, stroke_width=7).set_points_as_corners(
            [[-2.0 + 2.4 * i / 40, -1.2 - 0.9 * _sig((i / 40 - 0.55) / 0.08), 0] for i in range(41)])
        endl = lab("window closes", 34, TEAL, (3.1, -1.7), weight=BOLD)
        # Establish the whole causal picture immediately; spoken cues highlight its parts.
        self.add(card, top, div, b, a_, b_, tp, tp_lab, ar, endc, endl)
        self.at("In zebra finches")
        self.play(Indicate(b, color=BLUE, scale_factor=1.08), run_time=0.5)
        self.at("the expected input")
        self.play(Indicate(tp, color=YELLOW, scale_factor=1.1), run_time=0.6)
        self.at("help end the window")
        self.play(ShowPassingFlash(endc.copy().set_stroke(width=12)), Indicate(endl, color=TEAL, scale_factor=1.03), run_time=0.8)
        self.finish()


TK_OFF = 0.45


class S23Take(SpokenScene):
    def construct(self):
        base_y = -2.25
        xs = [-4.4 + TK_OFF, 0.0 + TK_OFF, 4.4 + TK_OFF]
        yax_x = -5.35 + TK_OFF
        axis = link([yax_x, base_y, 0], [6.5, base_y, 0], GREY, 4)
        yaxis = link([yax_x, base_y, 0], [yax_x, 3.2, 0], GREY, 4)
        ylab = T("the mark it leaves", 28, TEXT).rotate(PI / 2).move_to([yax_x - 0.5, 0.45, 0])
        axl = lab("age", 26, GREY, (6.2, base_y + 0.4))
        win = Rectangle(width=3.6, height=4.2, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.12).move_to([xs[1], base_y + 2.1, 0])
        wl = lab("window", 30, TEAL, (xs[1], base_y - 0.45), weight=BOLD)
        o1 = lab("other ages", 26, GREY, (xs[0], base_y - 0.45))
        o2 = lab("other ages", 26, GREY, (xs[2], base_y - 0.45))
        self.play(GrowArrow(axis), GrowArrow(yaxis), FadeIn(ylab), run_time=0.6)
        self.at("range of ages")
        self.play(FadeIn(axl), FadeIn(win), FadeIn(wl), FadeIn(o1), FadeIn(o2), run_time=0.8)
        tps = [tape(1.0).move_to([x, 2.35, 0]) for x in xs]
        arrs = [link([x, 2.0, 0], [x, 1.6, 0], YELLOW, 4) for x in xs]
        self.at("when the same experience")
        self.play(LaggedStart(*[AnimationGroup(FadeIn(t, shift=DOWN * 0.3), GrowArrow(a)) for t, a in zip(tps, arrs)],
                              lag_ratio=0.3), run_time=1.0)
        hs = [0.7, 3.0, 0.55]
        cols = [RED, GREEN, RED]
        bars = [Rectangle(width=1.5, height=h, stroke_width=0, fill_color=c, fill_opacity=0.9).move_to([x, base_y + h / 2, 0])
                for x, h, c in zip(xs, hs, cols)]
        self.at("unusually strong")
        self.play(*[GrowFromEdge(b, DOWN) for b in bars], run_time=1.1)
        strong = lab("strong, lasting", 28, GREEN, (xs[1], base_y + 3.0 + 0.4), weight=BOLD)
        weak = lab("weak", 26, RED, (xs[0], base_y + 0.7 + 0.4))
        weak2 = lab("weak", 26, RED, (xs[2], base_y + 0.55 + 0.4))
        self.play(FadeIn(strong), FadeIn(weak), FadeIn(weak2), run_time=0.4)
        self.finish()


class S24End(EndCard):
    LINE = "A window: ages when one experience leaves an unusually strong, lasting mark."

    def construct(self):
        # the same line, broken in two so it can be set large and centred
        l1 = T("A window: ages when one experience", 44, font=TITLE_FONT)
        l2 = T("leaves an unusually strong, lasting mark.", 44, font=TITLE_FONT)
        line = VGroup(l1, l2).arrange(DOWN, buff=0.25)
        sub = T("biochemistrypedia.com", 26, TEAL)
        g = VGroup(line, sub).arrange(DOWN, buff=0.6)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
