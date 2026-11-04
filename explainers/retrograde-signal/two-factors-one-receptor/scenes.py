"""Chapter 3 of "The Signal from the Target Travels Home": Two Factors, One Receptor

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, shared with every chapter of this lesson; from scenes.old.py)
  YELLOW = NGF, the final target's factor (and the target that makes it)
  ORANGE = NT-3, the intermediate target's factor (the blood vessel that makes it, a factor that acts only locally)
  BLUE   = TrkA, the receptor
  TEAL   = the carried signal: the signaling endosome, trafficking
  PINK   = dynein, the motor
  PURPLE = the nucleus (dim = no signal has arrived, bright = a signal has arrived)
  INDIGO = p75, the second receptor (drawn as a stalk with a round head, so it is not read as TrkA)
  GREEN  = supported / switched on / yes
  RED    = fails: not carried, not kept alive, no
  GREY   = the neuron's outline, axes, labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58FB8"
INDIGO = "#8A7FFF"
SOLID = interpolate_color(ManimColor(BG), ManimColor(GREY), 0.17)
TIP = 4.4          # x of the axon tip, in neuron units
LESSON = "The Signal from the Target Travels Home"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
class Neuron:
    """A straight neuron: cell body (left), axon, tip (right). p(x, y) maps neuron units to the frame."""

    def __init__(self, cx=0.0, cy=0.0, sc=1.0, tube=1.7, body_r=1.3):
        self.cx, self.cy, self.sc, self.tube = cx, cy, sc, tube
        h = tube * sc
        body = Circle(radius=body_r * sc).move_to(self.p(-4.95, 0))
        axon = RoundedRectangle(corner_radius=h / 2, width=(TIP + 4.9) * sc, height=h).move_to(self.p((TIP - 4.9) / 2, 0))
        self.cell = Union(body, axon).set_stroke(GREY, 3).set_fill(SOLID, 1)
        self.nuc = Circle(radius=0.46 * body_r * sc, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE,
                          fill_opacity=0.35).move_to(self.p(-5.0, 0))
        self.group = VGroup(self.cell, self.nuc)

    def p(self, x, y=0.0):
        return np.array([self.cx + x * self.sc, self.cy + y * self.sc, 0.0])


def rec_bar(pos, sc=1.0, angle=0.0, color=BLUE):
    return RoundedRectangle(corner_radius=0.09 * sc, width=0.26 * sc, height=0.7 * sc, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.85).move_to(pos).rotate(angle)


def p75_stalk(center, angle_deg, r=1.0, length=0.5):
    """A p75 receptor: a stalk with a round head, sticking out of a circle of radius r at the given angle."""
    a = np.deg2rad(angle_deg)
    d = np.array([np.cos(a), np.sin(a), 0.0])
    base = np.array(center) + d * r
    head = base + d * length
    return VGroup(Line(base - d * 0.05, head, color=INDIGO, stroke_width=7),
                  Circle(radius=0.13, stroke_color=INDIGO, stroke_width=3, fill_color=INDIGO, fill_opacity=1).move_to(head))


def dot(pos, color, r=0.17):
    return Circle(radius=r, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=1).move_to(pos)


def endo(pos, sc=1.0, dot_color=YELLOW):
    """Signaling endosome: a teal bubble holding the factor and the receptor. Returns VGroup(bubble, bar, dot)."""
    pos = np.array(pos, float)
    bubble = Circle(radius=0.45 * sc, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.18).move_to(pos)
    bar = rec_bar(pos + np.array([-0.12, 0, 0]) * sc, sc * 0.75)
    d = dot(pos + np.array([0.14, 0.02, 0]) * sc, dot_color, 0.12 * sc)
    return VGroup(bubble, bar, d)


def legs(pos, sc=1.0):
    """Two pink motor feet reaching from an endosome down to the microtubule."""
    pos = np.array(pos, float)
    out = VGroup()
    for s_ in (-1, 1):
        top = pos + np.array([0.12 * s_, -0.42, 0]) * sc
        bot = pos + np.array([0.36 * s_, -0.87, 0]) * sc
        out.add(Line(top, bot, color=PINK, stroke_width=6), dot(bot, PINK, 0.09 * sc))
    return out


def glide(mob, dx, dur):
    """Move mob left by dx over dur seconds of scene time, whatever else the scene is doing (an updater)."""
    st = {"moved": 0.0}
    v = dx / max(dur, 0.3)

    def upd(m, dt):
        step = min(v * dt, dx - st["moved"])
        if step > 0:
            m.shift(LEFT * step)
            st["moved"] += step
    mob.add_updater(upd)


def barred(a, b, color=RED, w=6, frac=0.35):
    """An arrow that is blocked part-way (a bar across it)."""
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    perp = np.array([-d[1], d[0], 0])
    mid = a + (b - a) * frac
    return VGroup(Arrow(a, b, buff=0, color=color, stroke_width=w, tip_length=0.28),
                  Line(mid + perp * 0.38, mid - perp * 0.38, color=color, stroke_width=w + 4))


def tag(text, color, size=26, **kw):
    return T(text, max(size, 26) if size < 26 else size, color, **kw)


def leader(a, b, color=GREY, w=2.5):
    return Line(np.array(a, float), np.array(b, float), color=color, stroke_width=w, stroke_opacity=0.85)


def halo(pos, r=0.6, color=GREEN):
    return Circle(radius=r, stroke_color=color, stroke_width=5).move_to(pos)


# ---- the curved "route" stage: cell body, axon along a blood vessel, organ -----------------------
def f_path(x):
    return -1.5 + 3.0 / (1 + np.exp(-1.1 * (x + 1.0)))


def path_pt(x):
    return np.array([x, f_path(x), 0.0])


ORGAN_X = 6.0
BODY_C = np.array([-5.0, -1.45, 0.0])
AX_END = 5.55          # the axon tip touches the organ's left edge
TIP_X = 5.33


def route_curve(x0, x1, **kw):
    return ParametricFunction(lambda t: path_pt(t), t_range=[x0, x1], **kw)


def stage_body():
    body = Circle(radius=1.2, stroke_color=GREY, stroke_width=3, fill_color=SOLID, fill_opacity=1).move_to(BODY_C)
    nuc = Circle(radius=0.55, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.35).move_to(BODY_C + LEFT * 0.05)
    return body, nuc


def stage_axon(x0=-4.2, x1=AX_END):
    ax = route_curve(x0, x1, stroke_width=10, color=GREY)
    ax.set_cap_style(CapStyleType.ROUND)
    return ax


def stage_tip():
    return Circle(radius=0.22, stroke_color=GREY, stroke_width=3, fill_color=SOLID, fill_opacity=1).move_to(path_pt(TIP_X))


def stage_vessel(op=0.22):
    v = route_curve(-3.6, 1.6, stroke_width=80, color=ORANGE, stroke_opacity=op)
    v.set_cap_style(CapStyleType.ROUND)
    return v


def stage_organ(op=0.14):
    return RoundedRectangle(corner_radius=0.15, width=0.9, height=3.0, stroke_color=YELLOW, stroke_width=3,
                            fill_color=YELLOW, fill_opacity=op).move_to([ORGAN_X, f_path(4.4), 0])


ORGAN_LBL = np.array([ORGAN_X, -0.75, 0])
VESSEL_TXT = np.array([-3.3, 0.6, 0])
VESSEL_ANCH = np.array([-3.0, f_path(-3.0) + 0.42, 0])


def vessel_label(text, color=ORANGE):
    """A label above the vessel with a short leader line to its edge."""
    lab = tag(text, color, 28).move_to(VESSEL_TXT)
    ld = leader(lab.get_bottom() + DOWN * 0.04, VESSEL_ANCH, color)
    return VGroup(lab, ld)


def organ_label(text="final\ntarget", color=YELLOW):
    return tag(text, color, 28, line_spacing=0.8).move_to(ORGAN_LBL)


NT3_DOTS_X = (-2.5, -1.7, -0.9, -0.1, 0.7, 1.4)


def nt3_dots():
    return VGroup(*[dot([x, f_path(x) - 0.22, 0], ORANGE, 0.11) for x in NT3_DOTS_X])


def ngf_dots():
    return VGroup(*[dot([6.1 + (0.0 if k % 2 else 0.1), f_path(4.4) + y, 0], YELLOW, 0.13)
                    for k, y in enumerate((-1.1, -0.5, 0.55, 1.1))])


# ---- the question/answer table ------------------------------------------------------------------
BIG = dict(hdr_y=2.1, hdr_h=1.25, row_y={"NT-3": 0.3, "NGF": -1.75}, row_h=2.0,
           col={"label": (-4.0, 3.2), "growth": (-0.7, 4.2), "survival": (3.5, 4.2)}, fs_hdr=34, fs_row=46, fs_cell=62,
           hdr={"growth": "axon\ngrowth", "survival": "cell-body\nsurvival", "carried": "carried back\nto cell body"})
COMPACT = dict(hdr_y=3.4, hdr_h=0.58, row_y={"NT-3": 2.8, "NGF": 2.22}, row_h=0.56,
               col={"label": (-5.3, 1.6), "growth": (-3.3, 2.4), "survival": (-0.4, 3.4), "carried": (3.7, 4.8)},
               fs_hdr=24, fs_row=26, fs_cell=26,
               hdr={"growth": "axon growth", "survival": "cell-body survival", "carried": "carried back to cell body"})
ROWCOL = {"NT-3": ORANGE, "NGF": YELLOW}


class Table:
    """Rows NT-3 and NGF; columns growth, survival (and later carried back). Cells are '?', 'yes', 'no' or 'nost'."""

    def __init__(self, geom, cols, cells):
        self.g, self.cols, self.cells = geom, list(cols), dict(cells)
        self.m = self._build(geom, self.cols)

    def _cell(self, g, row, col, val):
        x = g["col"][col][0]
        y = g["row_y"][row]
        fs = g["fs_cell"]
        if val == "?":
            return T("?", fs, TEXT, weight=BOLD).move_to([x, y, 0])
        txt = {"yes": "yes", "no": "no", "nost": "no (not stably)"}[val]
        t = T(txt, fs, GREEN if val == "yes" else RED, weight=BOLD)
        ref = T("no", fs, weight=BOLD)
        t.move_to([x, y, 0])
        glyph = t[1] if val == "yes" else t[0]          # a letter with no descender: its bottom is the baseline
        t.shift(UP * ((y - ref.height / 2) - glyph.get_bottom()[1]))
        return t

    def _build(self, g, cols):
        m = {}
        left = g["col"]["label"][0] - g["col"]["label"][1] / 2
        right = g["col"][cols[-1]][0] + g["col"][cols[-1]][1] / 2
        w = right - left
        cx = (left + right) / 2
        m["hdrband"] = Rectangle(width=w, height=g["hdr_h"] - 0.06, stroke_width=0, fill_color=GREY,
                                 fill_opacity=0.14).move_to([cx, g["hdr_y"], 0])
        for r, c in ROWCOL.items():
            m["band_" + r] = RoundedRectangle(corner_radius=0.12, width=w, height=g["row_h"] - 0.08, stroke_color=c,
                                              stroke_width=2, stroke_opacity=0.55, fill_color=c,
                                              fill_opacity=0.10).move_to([cx, g["row_y"][r], 0])
        for c in cols:
            colr = TEAL if c == "carried" else TEXT
            lines = [T(ln, g["fs_hdr"], colr, weight=BOLD) for ln in g["hdr"][c].split("\n")]
            h = lines[0] if len(lines) == 1 else VGroup(*lines).arrange(DOWN, buff=0.06)
            m["hdr_" + c] = h.move_to([g["col"][c][0], g["hdr_y"], 0])
        for r, c in ROWCOL.items():
            m["lbl_" + r] = T(r, g["fs_row"], c, weight=BOLD).move_to([g["col"]["label"][0], g["row_y"][r], 0])
        for (r, c), v in self.cells.items():
            if c in cols and v:
                m[f"cell_{r}_{c}"] = self._cell(g, r, c, v)
        return m

    def group(self):
        return VGroup(*self.m.values())

    def keys(self, *prefixes):
        return [self.m[k] for k in self.m if any(k.startswith(p) for p in prefixes)]

    def set(self, row, col, val):
        key = f"cell_{row}_{col}"
        new = self._cell(self.g, row, col, val)
        old = self.m.get(key)
        self.cells[(row, col)] = val
        self.m[key] = new
        if old is None:
            return FadeIn(new, scale=0.6)
        return ReplacementTransform(old, new)

    def morph(self, geom, cols):
        new = self._build(geom, list(cols))
        anims = []
        for k, v in new.items():
            if k in self.m:
                anims.append(Transform(self.m[k], v))
            else:
                anims.append(FadeIn(v))
                self.m[k] = v
        self.g, self.cols = geom, list(cols)
        return anims

    def hl(self, row, on=True):
        """Animation that thickens a row's outline (on) or resets it."""
        return self.m["band_" + row].animate.set_stroke(width=6 if on else 2, opacity=1.0 if on else 0.55)


def table_state(stage):
    """Cell contents at each point of the chapter."""
    c = {}
    for r in ROWCOL:
        for k in ("growth", "survival"):
            c[(r, k)] = "?"
    if stage >= 1:   # after s08
        c[("NT-3", "growth")] = "yes"
        c[("NT-3", "survival")] = "no"
    if stage >= 2:   # after s09
        c[("NGF", "growth")] = "yes"
        c[("NGF", "survival")] = "yes"
    if stage >= 3:   # carried-back column opens (s11)
        c[("NT-3", "carried")] = "?"
        c[("NGF", "carried")] = "?"
    if stage >= 4:   # after s12
        c[("NGF", "carried")] = "yes"
    if stage >= 5:   # after s13
        c[("NT-3", "carried")] = "nost"
    return c


def big_table(stage):
    return Table(BIG, ["growth", "survival"], table_state(stage))


def compact_table(stage):
    return Table(COMPACT, ["growth", "survival", "carried"], table_state(stage))


def add_table(scene, tbl, skip_prefixes=()):
    for k, v in tbl.m.items():
        if not any(k.startswith(p) for p in skip_prefixes):
            scene.add(v)


def table_caption():
    return T("Factor on distal axons only. Predict each cell.", 28, TEXT).move_to([0, 3.3, 0])


# ---- the neuron strip under the compact table (s11 to s14) ----------------------------------------
STRIP = dict(cx=0.2, cy=-1.2, sc=1.0, tube=2.8, body_r=1.65)
CY = STRIP["cy"]
CH_X = 5.975
ES = 1.3            # endosome scale in the strip
MT_Y = CY - 0.9    # the microtubule


def strip_neuron(nuc_op=0.12):
    n = Neuron(**STRIP)
    n.nuc.set_fill(PURPLE, nuc_op)
    rec = rec_bar(n.p(TIP, 0), 1.8)
    return n, rec


def strip_chamber(color, name):
    """A neutral culture chamber on the axon tips: a labelled box with the factor as a dot cloud."""
    ch = RoundedRectangle(corner_radius=0.15, width=1.55, height=3.4, stroke_color=color, stroke_width=3,
                          fill_color=color, fill_opacity=0.10).move_to([CH_X, CY, 0])
    pts = ((5.62, 1.0), (6.4, 0.6), (5.62, 0.0), (6.42, -0.45), (5.72, -0.95), (6.4, -1.2), (5.7, 1.3))
    dots = VGroup(*[dot([x, CY + y, 0], color, 0.13) for x, y in pts])
    nm = tag(f"{name} in\nchamber", color, 26, weight=BOLD, line_spacing=0.8).move_to([CH_X, CY + 2.3, 0])
    cap = T("factor on axon tips only (culture)", 26, GREY).move_to([4.1, CY - 2.2, 0])
    return ch, dots, nm, cap


def strip_endosome(n, color, x_off=1.0):
    pos = n.p(TIP - x_off, 0.3)
    return endo(pos, ES, color), pos


# =============================================================================================
class S00Title(TitleCard):
    LESSON = LESSON
    TITLE = "Two Factors, One Receptor"


# ---------------------------------------------------------------------------------------------
class S01Q(SpokenScene):
    """Two factors converge on one TrkA receptor at the axon tip; why both?"""

    def construct(self):
        tipbody = RoundedRectangle(corner_radius=0.6, width=11.0, height=2.8, stroke_color=GREY, stroke_width=3,
                                   fill_color=SOLID, fill_opacity=1).move_to([0, -2.3, 0])
        rec = rec_bar([0, -0.65, 0], 3.8)
        d1 = dot([-5.0, 2.2, 0], ORANGE, 0.4)
        d2 = dot([5.0, 2.2, 0], YELLOW, 0.4)
        n1 = tag("NT-3", ORANGE, 34, weight=BOLD).next_to(d1, UP, buff=0.15)
        n2 = tag("NGF", YELLOW, 34, weight=BOLD).next_to(d2, UP, buff=0.15)
        self.at("two factors", lead=0.0)
        self.play(FadeIn(tipbody), FadeIn(rec), FadeIn(d1, scale=0.5), FadeIn(d2, scale=0.5), FadeIn(n1), FadeIn(n2),
                  run_time=0.5)

        self.at("switch on")
        self.play(d1.animate.move_to([-1.0, 1.6, 0]), d2.animate.move_to([1.0, 1.6, 0]),
                  n1.animate.move_to([-1.0, 2.55, 0]), n2.animate.move_to([1.0, 2.55, 0]), run_time=0.8)
        self.at("same receptor")
        ring = halo([0, -0.65, 0], 1.65)
        trk = tag("TrkA", BLUE, 40, weight=BOLD).move_to([3.2, -0.65, 0])
        self.play(Create(ring), FadeIn(trk, shift=LEFT * 0.1), run_time=0.6)
        self.at("axon tip")
        lbl = tag("axon tip", GREY, 32).move_to([3.0, -2.55, 0])
        self.play(FadeIn(lbl), run_time=0.4)

        self.at("why does")
        q = T("?", 110, TEXT, weight=BOLD).move_to([0, 1.6, 0])
        self.play(d1.animate.move_to([-3.4, 1.6, 0]), d2.animate.move_to([3.4, 1.6, 0]),
                  n1.animate.move_to([-3.4, 2.55, 0]), n2.animate.move_to([3.4, 2.55, 0]), FadeOut(ring),
                  FadeIn(q, scale=0.6), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Route(SpokenScene):
    """A sympathetic axon grows along a blood vessel toward an organ."""

    def construct(self):
        body, nuc = stage_body()
        stub = route_curve(-4.2, -3.2, stroke_width=10, color=GREY)
        seg1 = route_curve(-3.2, 1.0, stroke_width=10, color=GREY)
        seg2 = route_curve(1.0, AX_END, stroke_width=10, color=GREY)
        for a in (stub, seg1, seg2):
            a.set_cap_style(CapStyleType.ROUND)
        vessel = stage_vessel(0.10)
        organ = stage_organ(0.05)
        self.add(vessel, organ, body, nuc, stub)
        self.bring_to_front(stub)

        self.at("sympathetic axons", lead=0.1)
        sl = tag("sympathetic neuron", GREY, 28).move_to([-4.6, -3.2, 0])
        self.play(FadeIn(sl), Create(seg1), run_time=1.5, rate_func=linear)
        self.at("blood vessels", lead=0.1)
        vl = vessel_label("blood vessel")
        self.play(vessel.animate.set_stroke(opacity=0.3), FadeIn(vl), run_time=0.5)
        self.play(Create(seg2), run_time=1.1, rate_func=linear)
        tipc = stage_tip()
        self.add(tipc)
        self.at("the organs", lead=0.1)
        ol = organ_label("organ", YELLOW)
        self.play(organ.animate.set_fill(YELLOW, 0.2), FadeIn(ol), run_time=0.6)
        self.at("innervate")
        self.play(Indicate(organ, color=YELLOW, scale_factor=1.06), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def build_stage_full(vessel_op=0.3, organ_op=0.2):
    body, nuc = stage_body()
    vessel = stage_vessel(vessel_op)
    ax = stage_axon()
    tipc = stage_tip()
    organ = stage_organ(organ_op)
    return body, nuc, vessel, ax, tipc, organ


class S03Two(SpokenScene):
    """The vessel makes NT-3 (orange); the organ makes NGF (yellow)."""

    def construct(self):
        body, nuc, vessel, ax, tipc, organ = build_stage_full(0.3, 0.2)
        vl = vessel_label("blood vessel")
        ol = organ_label("organ", YELLOW)
        self.add(vessel, body, nuc, ax, tipc, organ, vl, ol)

        self.at("vessels", lead=0.1)
        self.play(vessel.animate.set_stroke(opacity=0.5), run_time=0.5)
        self.at("intermediate target")
        vl2 = vessel_label("intermediate target")
        self.play(ReplacementTransform(vl, vl2), run_time=0.5)
        self.at("make nt3")
        nd = nt3_dots()
        nt = tag("NT-3", ORANGE, 38, weight=BOLD).move_to([-0.9, f_path(-0.9) - 1.25, 0])
        nl = leader([-0.9, f_path(-0.9) - 1.0, 0], [-0.9, f_path(-0.9) - 0.5, 0], ORANGE)
        self.play(FadeIn(nd, scale=0.5, lag_ratio=0.25), FadeIn(nt), FadeIn(nl), run_time=0.9)

        self.at("final targets")
        ol2 = organ_label("final\ntarget", YELLOW)
        self.play(organ.animate.set_fill(YELLOW, 0.34), ReplacementTransform(ol, ol2), run_time=0.5)
        self.at("make ngf")
        gd = ngf_dots()
        ngf = tag("NGF", YELLOW, 38, weight=BOLD).move_to([ORGAN_X, 3.52, 0])
        gl = leader([ORGAN_X, 3.24, 0], [ORGAN_X, f_path(4.4) + 1.5, 0], YELLOW)
        self.play(FadeIn(gd, scale=0.5, lag_ratio=0.25), FadeIn(ngf), FadeIn(gl), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Both(SpokenScene):
    """NT-3 and NGF each switch on TrkA: the receptor lights up either way."""

    def construct(self):
        xs = (-3.4, 3.4)
        parts = []
        for cx, col, nm in ((xs[0], ORANGE, "NT-3"), (xs[1], YELLOW, "NGF")):
            body = RoundedRectangle(corner_radius=0.5, width=6.2, height=2.6, stroke_color=GREY, stroke_width=3,
                                    fill_color=SOLID, fill_opacity=1).move_to([cx, -2.5, 0])
            rec = rec_bar([cx, -1.0, 0], 3.4).set_opacity(0.45)
            d = dot([cx, 2.3, 0], col, 0.38)
            n = tag(nm, col, 42, weight=BOLD).move_to([cx, 3.3, 0])
            trk = tag("TrkA", BLUE, 34, weight=BOLD).move_to([cx + 1.9, -0.45, 0])
            glow = RoundedRectangle(corner_radius=0.2, width=1.3, height=2.75, stroke_color=GREEN, stroke_width=6).move_to([cx, -1.0, 0])
            on = tag("on", GREEN, 38, weight=BOLD).move_to([cx - 1.4, -0.45, 0])
            parts.append((body, rec, d, n, trk, glow, on, cx))
        self.at("both factors", lead=0.0)
        self.play(*[FadeIn(p[0]) for p in parts], *[FadeIn(p[1]) for p in parts], *[FadeIn(p[2], scale=0.5) for p in parts],
                  *[FadeIn(p[3]) for p in parts], *[FadeIn(p[4]) for p in parts], run_time=0.7)
        self.at("can", lead=0.1)
        self.play(*[p[2].animate.move_to([p[7], 0.9, 0]) for p in parts], run_time=0.3)
        self.at("activate", lead=0.1)
        self.play(*[Create(p[5]) for p in parts], *[p[1].animate.set_opacity(1.0) for p in parts],
                  *[FadeIn(p[6], scale=0.6) for p in parts], run_time=0.5)
        self.play(*[Indicate(p[4], color=BLUE, scale_factor=1.15) for p in parts], run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
def dish_row(cy, color, name):
    """One compartmented dish: neuron cell bodies on the left, the factor only in the right (distal) chamber."""
    outline = RoundedRectangle(corner_radius=0.25, width=12.2, height=2.8, stroke_color=GREY, stroke_width=3).move_to([0, cy, 0])
    wall = Line([-0.2, cy - 1.4, 0], [-0.2, cy + 1.4, 0], color=GREY, stroke_width=8)
    chamber = RoundedRectangle(corner_radius=0.2, width=6.0, height=2.6, stroke_width=0, fill_color=color,
                               fill_opacity=0.12).move_to([2.85, cy, 0])
    bodies = VGroup()
    axons = VGroup()
    for dy in (0.42, -0.42):
        b = Circle(radius=0.3, stroke_color=GREY, stroke_width=3, fill_color=SOLID, fill_opacity=1).move_to([-5.0, cy + dy, 0])
        a = Line([-4.7, cy + dy, 0], [3.6, cy + dy * 0.5, 0], color=GREY, stroke_width=6)
        a.set_cap_style(CapStyleType.ROUND)
        bodies.add(b)
        axons.add(a)
    dots = VGroup(*[dot([x, cy + y, 0], color, 0.12) for x, y in
                    ((1.0, 0.72), (2.0, 0.78), (3.0, 0.72), (3.95, 0.02), (4.5, -0.45), (5.35, -0.2), (5.3, 0.45), (4.4, 0.5))])
    nm = tag(name, color, 32, weight=BOLD).move_to([5.1, cy + 1.05, 0])
    return outline, wall, chamber, bodies, axons, dots, nm


class S05Test(SpokenScene):
    """Compartmented dish: each factor only on the distal axons; none at the cell bodies."""

    def construct(self):
        A = dish_row(1.75, ORANGE, "NT-3")
        B = dish_row(-1.45, YELLOW, "NGF")
        credit = tag("Kuruvilla, Ginty and colleagues, 2004", GREY, 26).move_to([0, -3.45, 0])
        sn = [tag("sympathetic neurons", GREY, 26).move_to([-3.0, cy + 1.05, 0]) for cy in (1.75, -1.45)]
        self.play(*[FadeIn(m) for r in (A, B) for m in (r[0], r[1], r[3], r[4])], FadeIn(credit), run_time=0.8)

        self.at("colleagues", lead=0.2)
        self.play(*[FadeIn(t) for t in sn], run_time=0.5)
        self.at("each factor")
        self.play(*[FadeIn(m) for r in (A, B) for m in (r[2], r[5], r[6])], run_time=0.8)
        self.at("only to")
        nofac = [tag("no factor here", GREY, 26).move_to([-3.0, cy - 1.05, 0]) for cy in (1.75, -1.45)]
        self.play(*[FadeIn(t) for t in nofac], run_time=0.5)
        self.at("distal axons")
        dl = [tag("distal axons", TEXT, 26).move_to([2.2, cy - 1.05, 0]) for cy in (1.75, -1.45)]
        self.play(*[FadeIn(t) for t in dl], *[Indicate(r[4], color=TEXT, scale_factor=1.03) for r in (A, B)], run_time=0.8)
        self.at("sympathetic neurons")
        self.play(*[Indicate(r[3], color=TEXT, scale_factor=1.15) for r in (A, B)], run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Ask(SpokenScene):
    """A table of questions: with NT-3 on the axon tips, do the axons grow? Do the cell bodies survive?"""

    def construct(self):
        tbl = big_table(0)
        cap = table_caption()
        self.at("with", lead=0.0)
        self.play(*[FadeIn(m) for m in tbl.keys("hdrband", "band_", "lbl_")], FadeIn(cap), run_time=0.4)
        self.at("nt3")
        self.play(tbl.hl("NT-3"), Indicate(tbl.m["lbl_NT-3"], color=ORANGE, scale_factor=1.15), run_time=0.7)
        self.at("axons grow")
        self.play(FadeIn(tbl.m["hdr_growth"], shift=DOWN * 0.1), *[FadeIn(tbl.m[f"cell_{r}_growth"], scale=0.6) for r in ROWCOL],
                  run_time=0.6)
        self.play(Indicate(tbl.m["cell_NT-3_growth"], color=TEXT, scale_factor=1.3), run_time=0.6)
        self.at("cell bodies")
        self.play(FadeIn(tbl.m["hdr_survival"], shift=DOWN * 0.1), *[FadeIn(tbl.m[f"cell_{r}_survival"], scale=0.6) for r in ROWCOL],
                  run_time=0.6)
        self.play(Indicate(tbl.m["cell_NT-3_survival"], color=TEXT, scale_factor=1.3), run_time=0.6)
        self.finish()


class S07Pause(NarratedScene):
    def construct(self):
        tbl = big_table(0)
        add_table(self, tbl)
        tbl.m["band_NT-3"].set_stroke(width=6, opacity=1.0)
        self.add(table_caption())
        pp = T("Pause and predict", 28, GREY).move_to([0.6, -3.45, 0])
        ring = Circle(radius=0.28, stroke_color=GREY, stroke_width=5).move_to([-2.0, -3.45, 0])
        self.add(pp, ring)
        self.play(Uncreate(ring), run_time=self.narration_s - 0.3, rate_func=linear)
        self.finish()


class S08Nt3(SpokenScene):
    def construct(self):
        tbl = big_table(0)
        add_table(self, tbl)
        self.add(table_caption())
        tbl.m["band_NT-3"].set_stroke(width=6, opacity=1.0)
        self.at("growth", lead=0.1)
        self.play(tbl.set("NT-3", "growth", "yes"), run_time=0.6)
        self.at("not survive", lead=0.0)
        self.play(tbl.set("NT-3", "survival", "no"), run_time=0.6)
        self.finish()


class S09Ngf(SpokenScene):
    def construct(self):
        tbl = big_table(1)
        add_table(self, tbl)
        self.add(table_caption())
        tbl.m["band_NT-3"].set_stroke(width=6, opacity=1.0)
        self.at("ngf", lead=0.0)
        self.play(tbl.hl("NT-3", False), tbl.hl("NGF", True), Indicate(tbl.m["lbl_NGF"], color=YELLOW, scale_factor=1.15),
                  run_time=0.6)
        self.at("growth", lead=0.1)
        self.play(tbl.set("NGF", "growth", "yes"), run_time=0.6)
        self.at("survival", lead=0.1)
        self.play(tbl.set("NGF", "survival", "yes"), run_time=0.6)
        self.finish()


class S10Beat(NarratedScene):
    def construct(self):
        tbl = big_table(2)
        add_table(self, tbl)
        self.add(table_caption())
        tbl.m["band_NGF"].set_stroke(width=6, opacity=1.0)
        self.wait(self.beat(1.0))
        self.finish()


class S11Why(SpokenScene):
    """The table makes room and a new column opens: carried back to the cell body."""

    def construct(self):
        tbl = big_table(2)
        add_table(self, tbl)
        cap = table_caption()
        self.add(cap)
        tbl.m["band_NGF"].set_stroke(width=6, opacity=1.0)
        self.at("why", lead=0.0)
        self.at("difference", lead=0.1)
        self.play(Indicate(tbl.m["cell_NT-3_survival"], color=RED, scale_factor=1.3),
                  Indicate(tbl.m["cell_NGF_survival"], color=GREEN, scale_factor=1.3), run_time=0.9)
        self.at("trafficking", lead=0.1)
        tbl.cells.update({("NT-3", "carried"): "?", ("NGF", "carried"): "?"})
        self.play(*tbl.morph(COMPACT, ["growth", "survival", "carried"]), FadeOut(cap), run_time=1.0)
        n, rec = strip_neuron()
        self.play(FadeIn(n.group), FadeIn(rec), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S12Ngf(SpokenScene):
    """An NGF-TrkA endosome rides dynein to the cell body."""

    def construct(self):
        tbl = compact_table(3)
        add_table(self, tbl)
        tbl.m["band_NGF"].set_stroke(width=6, opacity=1.0)
        n, rec = strip_neuron()
        self.add(n.group, rec)
        ch, dots, nm, cap = strip_chamber(YELLOW, "NGF")
        mt = Line(n.p(-3.7, 0) + np.array([0, MT_Y - CY, 0]), n.p(TIP - 0.5, 0) + np.array([0, MT_Y - CY, 0]), color=GREY,
                  stroke_width=6)
        self.at("ngf", lead=0.0)
        self.play(FadeIn(ch), FadeIn(dots), FadeIn(nm), FadeIn(cap), run_time=0.8)
        self.bring_to_front(rec)

        self.at("track a", lead=0.3)
        rec_l = tag("TrkA", BLUE, 30, weight=BOLD).move_to([3.3, 0.6, 0])
        rl = leader([3.75, 0.38, 0], n.p(TIP - 0.05, 0) + UP * 0.55, BLUE)
        d0 = dots[2]
        self.play(d0.animate.move_to(n.p(TIP + 0.36, 0)), FadeIn(rec_l), FadeIn(rl), run_time=0.6)
        self.play(Indicate(rec, color=BLUE, scale_factor=1.3), run_time=0.5)

        self.at("taken into")
        ev, pos = strip_endosome(n, YELLOW, 1.0)
        self.play(FadeOut(rec_l), FadeOut(rl), FadeIn(ev, scale=0.4), run_time=0.7)
        self.bring_to_front(ev)

        self.at("carried back", lead=0.1)
        lg = legs(pos, ES)
        dyn = tag("dynein", PINK, 28, weight=BOLD).move_to(pos + UP * 1.6)
        dl = leader(pos + UP * 1.35, pos + UP * 0.62, PINK)
        self.play(FadeIn(mt), FadeIn(lg, shift=UP * 0.1), FadeIn(dyn), FadeIn(dl), run_time=0.5)
        mover = VGroup(ev, lg, dyn, dl)
        self.add(mover)
        dur = self.narration_s - self.elapsed() - 1.0
        glide(mover, (TIP - 1.0 - (-3.55)) * STRIP["sc"], dur)
        self.at("cell body", lead=0.2)
        self.play(FadeOut(dyn), FadeOut(dl), run_time=0.3)
        cb = tag("cell body", GREY, 28).move_to(n.p(-4.95, 0) + UP * 2.0)
        self.play(FadeIn(cb), tbl.set("NGF", "carried", "yes"), run_time=0.6)
        rest = self.narration_s - 0.05 - self.elapsed()
        if rest > 0:
            self.wait(rest)
        self.play(n.nuc.animate.set_fill(PURPLE, 0.75), run_time=0.4)
        self.finish()


class S13Nt3(SpokenScene):
    """NT-3 lights TrkA at the tip, the complex goes into a local endosome that does not make the trip."""

    def construct(self):
        tbl = compact_table(4)
        add_table(self, tbl)
        tbl.m["band_NT-3"].set_stroke(width=6, opacity=1.0)
        n, rec = strip_neuron()
        self.add(n.group, rec)
        ch, dots, nm, cap = strip_chamber(ORANGE, "NT-3")
        self.at("nt3", lead=0.0)
        self.play(FadeIn(ch), FadeIn(dots), FadeIn(nm), FadeIn(cap), run_time=0.5)
        self.bring_to_front(rec)
        d0 = dots[2]
        self.play(d0.animate.move_to(n.p(TIP + 0.36, 0)), run_time=0.4)
        ring = halo(n.p(TIP, 0), 0.8)
        rec_l = tag("TrkA", BLUE, 30, weight=BOLD).move_to([3.3, 0.6, 0])
        rl = leader([3.75, 0.38, 0], n.p(TIP - 0.05, 0) + UP * 0.75, BLUE)
        self.play(Create(ring), FadeIn(rec_l), FadeIn(rl), run_time=0.4)

        self.at("complexes", lead=0.3)
        ev, pos = strip_endosome(n, ORANGE, 0.95)
        self.play(FadeOut(rec_l), FadeOut(rl), FadeOut(ring), FadeIn(ev, scale=0.4), run_time=0.5)
        self.bring_to_front(ev)
        self.play(ev.animate.shift(LEFT * 0.9), run_time=0.6, rate_func=rush_from)

        self.at("not stably", lead=0.2)
        bl = barred(pos + LEFT * 1.35 + DOWN * 0.0, pos + LEFT * 4.2, frac=0.25)
        self.play(ev.animate.set_opacity(0.25), Create(bl), run_time=0.5)
        self.at("carried back", lead=0.0)
        self.play(tbl.set("NT-3", "carried", "nost"), run_time=0.5)
        self.finish()


class S14Link(SpokenScene):
    """NT-3 switches the receptor on at the tip; the signal is not carried home (the cell body stays dim)."""

    def construct(self):
        tbl = compact_table(5)
        add_table(self, tbl)
        tbl.m["band_NT-3"].set_stroke(width=6, opacity=1.0)
        n, rec = strip_neuron()
        ch, dots, nm, cap = strip_chamber(ORANGE, "NT-3")
        self.add(n.group, rec, ch, dots, nm, cap)
        self.bring_to_front(rec)
        self.at("nt3", lead=0.1)
        d0 = dots[2]
        self.play(d0.animate.move_to(n.p(TIP + 0.36, 0)), run_time=0.7)
        self.at("receptor on", lead=0.1)
        ring = halo(n.p(TIP, 0), 0.8)
        on = tag("TrkA on", GREEN, 32, weight=BOLD).move_to([3.3, 0.6, 0])
        ol = leader([3.85, 0.38, 0], n.p(TIP - 0.05, 0) + UP * 0.75, GREEN)
        self.play(Create(ring), FadeIn(on, scale=0.7), FadeIn(ol), run_time=0.7)

        self.at("that signal", lead=0.1)
        y = CY + 0.3
        arr = DashedLine(n.p(TIP - 0.9, 0.3), n.p(TIP - 3.4, 0.3), color=TEAL, stroke_width=6, dash_length=0.2)
        arr.add_tip(tip_length=0.28)
        self.play(Create(arr), run_time=0.7, rate_func=linear)
        self.at("not carried", lead=0.1)
        bar = Line(n.p(TIP - 3.55, 0.3) + UP * 0.45, n.p(TIP - 3.55, 0.3) + DOWN * 0.45, color=RED, stroke_width=11)
        self.play(Create(bar), run_time=0.4)
        self.at("home", lead=0.1)
        cb = tag("cell body: dim", GREY, 28).move_to(n.p(-4.95, 0) + UP * 2.0)
        self.play(FadeIn(cb), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
KO_Y0 = 0.0
Y_START = (-0.5, -0.25, 0.0, 0.25, 0.5)
Y_END = (-1.6, -0.8, 0.0, 0.8, 1.6)
KO_END = 2.15


def ko_panel(cx, label, color):
    frame = RoundedRectangle(corner_radius=0.2, width=6.5, height=5.6, stroke_color=GREY, stroke_width=2,
                             stroke_opacity=0.6).move_to([cx, -0.1, 0])
    vessel = Line([cx - 2.3, KO_Y0, 0], [cx + 1.7, KO_Y0, 0], stroke_width=120, color=ORANGE, stroke_opacity=0.2)
    vessel.set_cap_style(CapStyleType.ROUND)
    organ = RoundedRectangle(corner_radius=0.12, width=0.8, height=4.0, stroke_color=YELLOW, stroke_width=3,
                             fill_color=YELLOW, fill_opacity=0.14).move_to([cx + 2.5, KO_Y0, 0])
    lbl = tag(label, color, 32, weight=BOLD).move_to([cx, 3.25, 0])
    vl = tag("vessel", ORANGE, 26).move_to([cx - 2.0, 1.15, 0])
    ol = tag("organ", YELLOW, 26).move_to([cx + 2.5, 2.38, 0])
    return frame, vessel, organ, lbl, vl, ol


def ko_axon(cx, i, frac, seed=0.0):
    n = 70
    xs = np.linspace(cx - 2.7, cx + KO_END, n)[: max(4, int(n * frac))]
    u = (xs - (cx - 2.7)) / (KO_END + 2.7)
    ss = u * u * (3 - 2 * u)
    ys = KO_Y0 + Y_START[i] + (Y_END[i] - Y_START[i]) * ss + 0.05 * np.sin(3.3 * xs + seed + i)
    a = VMobject(color=GREY, stroke_width=6).set_points_smoothly([np.array([x, y, 0.0]) for x, y in zip(xs, ys)])
    a.set_cap_style(CapStyleType.ROUND)
    return a


class S15Useful(SpokenScene):
    """Control mouse versus NT-3 knockout: fewer, shorter axons along the vessel, less of the organ innervated."""

    def construct(self):
        cxL, cxR = -3.4, 3.4
        PL = ko_panel(cxL, "control", TEXT)
        PR = ko_panel(cxR, "NT-3 knockout", ORANGE)
        self.add(*PL, *PR)
        self.at("it is", lead=0.0)
        self.wait(0.3)
        self.at("lacking", lead=0.3)
        self.play(Indicate(PR[3], color=ORANGE, scale_factor=1.15), PR[1].animate.set_stroke(opacity=0.06), run_time=0.8)
        self.at("sympathetic axon", lead=0.2)
        axL = [ko_axon(cxL, i, 1.0) for i in range(5)]
        axR = [ko_axon(cxR, 4, 1.0), ko_axon(cxR, 2, 0.5), ko_axon(cxR, 0, 0.32)]
        self.play(*[Create(a) for a in axL + axR], run_time=1.8, rate_func=linear)
        self.at("target innervation", lead=0.1)
        endL = VGroup(*[dot([cxL + KO_END, KO_Y0 + Y_END[i], 0], GREEN, 0.11) for i in range(5)])
        dR = dot([cxR + KO_END, KO_Y0 + Y_END[4], 0], GREEN, 0.11)
        self.play(FadeIn(endL, scale=0.5), FadeIn(dR, scale=0.5), Indicate(PR[2], color=YELLOW, scale_factor=1.04),
                  run_time=0.7)
        self.at("impaired", lead=0.4)
        res = tag("NT-3 knockout: growth and innervation impaired", RED, 30, weight=BOLD).move_to([0, -3.45, 0])
        self.play(FadeIn(res, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
GHOST = 0.09


class S16Handoff(SpokenScene):
    """The axon reaches the organ; the vessel fades behind it."""

    def construct(self):
        body, nuc = stage_body()
        vessel = stage_vessel(0.40)
        ax1 = route_curve(-4.2, 4.0, stroke_width=10, color=GREY)
        ax2 = route_curve(4.0, AX_END, stroke_width=10, color=GREY)
        for a in (ax1, ax2):
            a.set_cap_style(CapStyleType.ROUND)
        organ = stage_organ(0.30)
        vl = vessel_label("intermediate target")
        ol = organ_label()
        pr = tag("proposed", TEXT, 32)
        ho = tag("handoff", TEXT, 40, weight=BOLD)
        row = VGroup(pr, ho).arrange(RIGHT, buff=0.25, aligned_edge=DOWN).move_to([-0.6, -2.05, 0])
        tipc = stage_tip().move_to(path_pt(4.0))
        self.add(vessel, body, nuc, ax1, tipc, organ, vl, ol, pr)
        self.bring_to_front(ax1)
        self.play(Create(ax2), MoveAlongPath(tipc, route_curve(4.0, TIP_X)),
                  vessel.animate.set_stroke(opacity=GHOST), FadeOut(vl), run_time=0.85, rate_func=linear)
        self.at("handoff", lead=0.1)
        self.play(FadeIn(ho, shift=UP * 0.1), run_time=0.5)
        self.finish()


def p75_set(n_extra=False):
    angs = (140, 112, 84, 56) if not n_extra else (154, 140, 126, 112, 98, 84, 70, 56, 42)
    return VGroup(*[p75_stalk(BODY_C, a, r=1.2, length=0.5) for a in angs])


P75_LBL = BODY_C + UP * 2.5 + RIGHT * 0.35


class S17P75(SpokenScene):
    """Retrograde NGF signaling raises a second neurotrophin receptor, p75."""

    def construct(self):
        body, nuc = stage_body()
        vessel = stage_vessel(GHOST)
        ax = stage_axon()
        tipc = stage_tip()
        organ = stage_organ(0.30)
        ol = organ_label()
        self.add(vessel, body, nuc, ax, tipc, organ, ol)
        self.bring_to_front(ax, tipc)
        ev = endo(path_pt(TIP_X - 0.5), 1.1)
        el = tag("retrograde NGF signal", TEAL, 28, weight=BOLD)
        el.add_updater(lambda m: m.move_to(ev.get_center() + UP * 0.95 + LEFT * 1.5))
        self.at("retrograde", lead=0.0)
        self.play(FadeIn(ev, scale=0.5), FadeIn(el), run_time=0.4)
        seg = ParametricFunction(lambda t: path_pt(TIP_X - 0.5 - t), t_range=[0, TIP_X - 0.5 + 3.6])
        self.play(MoveAlongPath(ev, seg), run_time=1.3, rate_func=linear)
        el.clear_updaters()
        self.play(nuc.animate.set_fill(PURPLE, 0.75), FadeOut(ev), FadeOut(el), run_time=0.3)

        self.at("raises", lead=0.1)
        stalks = p75_set()
        lbl = tag("p75", INDIGO, 38, weight=BOLD).move_to(P75_LBL)
        self.play(LaggedStart(*[FadeIn(s, scale=0.4) for s in stalks], lag_ratio=0.4), FadeIn(lbl, shift=DOWN * 0.1),
                  run_time=1.8)
        self.finish()


def s18_objects(final):
    body, nuc = stage_body()
    vessel = stage_vessel(0.08 if final else 0.40)
    ax = stage_axon()
    tipc = stage_tip()
    organ = stage_organ(0.30)
    ol = organ_label()
    stalks = p75_set(True)
    lbl = tag("p75", INDIGO, 38, weight=BOLD).move_to(P75_LBL)
    cx_ = -2.5  # actual vessel/axon contact, well away from the organ
    contact = path_pt(cx_)
    rec = rec_bar(contact, 1.3)
    od = dot(contact + np.array([0.0, -0.8, 0]), ORANGE, 0.16)
    ring = halo(contact, 0.62)
    rl = tag("NT-3 response", GREEN, 26, weight=BOLD).move_to(contact + np.array([0.0, 1.25, 0]))
    rld = leader(contact + np.array([0.0, 1.0, 0]), contact + np.array([0.0, 0.68, 0]), GREEN)
    vlab = tag("NT-3", ORANGE, 26, weight=BOLD).move_to(contact + np.array([0.0, -1.5, 0]))
    if final:
        for m_, o_ in ((rec, 0.4), (od, 0.3), (ring, 0.15)):
            m_.set_opacity(o_)
        rl.set_opacity(0.4)
        rld.set_opacity(0.3)
        vlab.set_opacity(0.55)
    return dict(body=body, nuc=nuc, vessel=vessel, ax=ax, tipc=tipc, organ=organ, ol=ol, stalks=stalks, lbl=lbl, rec=rec,
                od=od, ring=ring, rl=rl, rld=rld, vlab=vlab)


class S18Less(SpokenScene):
    """As p75 rises, the neuron responds less to NT-3; the vessel's colour fades, the organ's stays."""

    def construct(self):
        o = s18_objects(False)
        o["nuc"].set_fill(PURPLE, 0.75)
        stalks = o["stalks"]
        # start from the four stalks of the previous scene; the rest appear as p75 rises
        first = [stalks[i] for i in (1, 3, 5, 7)]
        rest = [stalks[i] for i in (0, 2, 4, 6, 8)]
        self.add(o["vessel"], o["body"], o["nuc"], o["ax"], o["tipc"], o["organ"], o["ol"], o["lbl"], *first, o["rec"], o["od"],
                 o["ring"], o["rl"], o["rld"], o["vlab"])
        self.bring_to_front(o["ax"], o["rec"])
        up = Arrow(BODY_C + UP * 2.2 + RIGHT * 1.65, BODY_C + UP * 3.0 + RIGHT * 1.65, buff=0, color=INDIGO, stroke_width=7,
                   tip_length=0.25)
        self.at("p75", lead=0.2)
        self.play(*[FadeIn(s, scale=0.4) for s in rest], GrowArrow(up), run_time=1.0)
        self.at("responds less", lead=0.1)
        self.play(o["ring"].animate.set_opacity(0.15), o["rec"].animate.set_opacity(0.4), o["od"].animate.set_opacity(0.3),
                  o["rl"].animate.set_opacity(0.4), o["rld"].animate.set_opacity(0.3), o["vlab"].animate.set_opacity(0.55),
                  o["vessel"].animate.set_stroke(opacity=0.08), run_time=0.8)
        self.at("less", lead=0.0)
        lab = tag("less responsive to the intermediate target\nonce at the final one", TEXT, 26, line_spacing=0.9)
        lab.move_to([0.4, -3.35, 0])
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S19Beat(NarratedScene):
    def construct(self):
        o = s18_objects(True)
        o["nuc"].set_fill(PURPLE, 0.75)
        lab = tag("less responsive to the intermediate target\nonce at the final one", TEXT, 26, line_spacing=0.9)
        lab.move_to([0.4, -3.35, 0])
        up = Arrow(BODY_C + UP * 2.2 + RIGHT * 1.65, BODY_C + UP * 3.0 + RIGHT * 1.65, buff=0, color=INDIGO, stroke_width=7,
                   tip_length=0.25)
        self.add(o["vessel"], o["body"], o["nuc"], o["ax"], o["tipc"], o["organ"], o["ol"], o["stalks"], o["lbl"], o["rec"],
                 o["od"], o["ring"], o["rl"], o["rld"], o["vlab"], lab, up)
        self.bring_to_front(o["ax"], o["rec"])
        self.wait(self.beat(1.0))
        self.finish()


# ---------------------------------------------------------------------------------------------
class S20Scope(SpokenScene):
    """Two panels: NT-3 steering an axon along the vessel; NGF signal arriving at the cell body."""

    def construct(self):
        fl = RoundedRectangle(corner_radius=0.2, width=6.4, height=6.4, stroke_color=GREY, stroke_width=2,
                              stroke_opacity=0.6).move_to([-3.4, 0.1, 0])
        fr = RoundedRectangle(corner_radius=0.2, width=6.4, height=6.4, stroke_color=GREY, stroke_width=2,
                              stroke_opacity=0.6).move_to([3.4, 0.1, 0])
        # left panel: a fork; the vessel branch is chosen
        F = np.array([-3.5, -0.9, 0.0])

        def ssm(u):
            return u * u * (3 - 2 * u)

        def pa(u):   # branch A along the vessel (up)
            return np.array([F[0] + 2.6 * u, F[1] + 2.9 * ssm(u), 0])

        def pb(u):   # branch B (no vessel, down)
            return np.array([F[0] + 2.6 * u, F[1] - 1.0 * ssm(u), 0])

        vessel = ParametricFunction(pa, t_range=[0.12, 1.0], stroke_width=70, color=ORANGE, stroke_opacity=0.25)
        vessel.set_cap_style(CapStyleType.ROUND)
        branch_b = DashedVMobject(ParametricFunction(pb, t_range=[0, 1], stroke_width=5, color=GREY, stroke_opacity=0.5),
                                  num_dashes=14)
        dts = VGroup(*[dot(pa(u) + np.array([0.0, -0.3, 0]), ORANGE, 0.14) for u in (0.3, 0.5, 0.7, 0.9)])
        lbody = Circle(radius=0.85, stroke_color=GREY, stroke_width=3, fill_color=SOLID, fill_opacity=1).move_to([-5.5, -0.9, 0])
        lnuc = Circle(radius=0.4, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.12).move_to([-5.5, -0.9, 0])
        stub = Line([-4.8, -0.9, 0], F, color=GREY, stroke_width=12)
        grow = ParametricFunction(pa, t_range=[0, 1], stroke_width=12, color=GREY)
        for a in (stub, grow):
            a.set_cap_style(CapStyleType.ROUND)
        lrec = rec_bar(pa(1.0) + np.array([0.0, 0.1, 0]), 1.4, angle=PI / 2)
        ld = dot(pa(1.0) + np.array([0.0, 0.5, 0]), ORANGE, 0.15)
        # right panel: the NGF neuron
        tube = RoundedRectangle(corner_radius=0.7, width=4.4, height=1.4, stroke_color=GREY, stroke_width=3,
                                fill_color=SOLID, fill_opacity=1).move_to([3.95, 0.1, 0])
        rbody = Circle(radius=1.4, stroke_color=GREY, stroke_width=3, fill_color=SOLID, fill_opacity=1).move_to([1.5, 0.1, 0])
        rnuc = Circle(radius=0.65, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.12).move_to([1.5, 0.1, 0])
        rb = rec_bar([5.95, 0.1, 0], 2.0)
        yd = dot([6.4, 0.1, 0], YELLOW, 0.15)
        ngf_l = tag("NGF", YELLOW, 28, weight=BOLD).move_to([6.05, 1.25, 0])
        self.add(fl, fr, vessel, branch_b, stub, lbody, lnuc, tube, rbody, rnuc, rb, yd, ngf_l)
        self.at("a factor", lead=0.0)
        self.at("acts only locally", lead=0.1)
        ll = tag("NT-3: acts only locally", ORANGE, 30, weight=BOLD).move_to([-3.4, 2.85, 0])
        self.play(FadeIn(ll), FadeIn(dts, lag_ratio=0.2), run_time=0.7)
        self.at("steer an axon", lead=0.1)
        steer = tag("steers the axon", TEXT, 28).move_to([-4.6, 0.7, 0])
        sld = leader([-4.1, 0.45, 0], F + np.array([-0.12, 0.12, 0]), TEXT)
        self.play(Create(grow), FadeIn(steer), FadeIn(sld), run_time=1.2, rate_func=linear)
        self.play(FadeIn(lrec), FadeIn(ld), run_time=0.3)
        self.bring_to_front(stub, grow, lrec)

        self.at("it cannot", lead=0.2)
        badge = chip("not kept alive by this alone", RED, 26)
        badge.move_to([-3.9, -2.65, 0])
        rl = tag("NGF signal at the cell body", TEAL, 28, weight=BOLD).move_to([3.4, 2.85, 0])
        ev = endo([5.0, 0.1, 0], 1.4)
        self.play(FadeIn(badge, shift=UP * 0.1), FadeIn(rl), FadeIn(ev, scale=0.5), run_time=0.6)
        glide(ev, 2.2, 1.5)
        self.at("keep the neuron alive", lead=0.0)
        self.wait(0.2)
        alive = chip("alive", GREEN, 28).move_to([1.5, 2.2, 0])
        self.play(rnuc.animate.set_fill(PURPLE, 0.8), FadeIn(alive, scale=0.6), run_time=0.5)
        self.finish()


class S21Comp(SpokenScene):
    """Several axons converge on one organ: every tip has NGF bound, but only some receptors are trafficked home."""

    def construct(self):
        ys = (2.3, 0.8, -0.8, -2.3)
        tips = (2.0, 0.7, -0.7, -2.0)
        bodies, nucs, axons, recs, bound = VGroup(), VGroup(), VGroup(), VGroup(), VGroup()
        for y, ty in zip(ys, tips):
            b = Circle(radius=0.45, stroke_color=GREY, stroke_width=3, fill_color=SOLID, fill_opacity=1).move_to([-5.9, y, 0])
            nu = Circle(radius=0.2, stroke_color=PURPLE, stroke_width=2, fill_color=PURPLE, fill_opacity=0.12).move_to([-5.9, y, 0])
            a = VMobject(color=GREY, stroke_width=8).set_points_smoothly(
                [np.array([-5.4, y, 0]), np.array([-0.3, (y + ty) / 2, 0]), np.array([4.7, ty, 0])])
            a.set_cap_style(CapStyleType.ROUND)
            bodies.add(b), nucs.add(nu), axons.add(a)
            recs.add(rec_bar([4.95, ty, 0], 0.9))
            bound.add(dot([5.33, ty, 0], YELLOW, 0.13))
        organ = RoundedRectangle(corner_radius=0.15, width=0.9, height=5.2, stroke_color=YELLOW, stroke_width=3,
                                 fill_color=YELLOW, fill_opacity=0.14).move_to([6.0, 0, 0])
        self.add(bodies, nucs)
        self.play(LaggedStart(*[Create(a) for a in axons], lag_ratio=0.15), run_time=0.7)
        self.bring_to_front(bodies, nucs)
        self.at("competition", lead=0.2)
        bl = tag("NGF bound at every tip", YELLOW, 28, weight=BOLD).move_to([-0.4, 3.4, 0])
        self.play(FadeIn(recs), FadeIn(bound, scale=0.5), FadeIn(bl), run_time=0.5)
        self.at("final target", lead=0.2)
        ol = tag("final\ntarget", YELLOW, 28, line_spacing=0.8).move_to([5.95, -3.3, 0])
        self.play(FadeIn(organ), FadeIn(ol), run_time=0.5)

        self.at("depends", lead=0.5)
        carried, stays = (0, 2), (1, 3)
        starts = {0: 0.86, 2: 0.68}
        runs = {0: 1.8, 2: 1.5}
        evs, anims = VGroup(), []
        for i in carried:
            ev = endo(axons[i].point_from_proportion(starts[i]), 0.75)
            evs.add(ev)
            p0 = starts[i]
            # Continue through the soma to its nucleus; brighten on arrival and hold.
            path = VMobject().set_points_as_corners(
                [axons[i].point_from_proportion(p) for p in np.linspace(p0, 0, 45)] + [nucs[i].get_center()])
            anims.append(Succession(
                MoveAlongPath(ev, path, run_time=runs[i], rate_func=linear),
                AnimationGroup(nucs[i].animate.set_fill(PURPLE, 1.0), FadeOut(ev), run_time=0.25)))
        stay_tags = [tag("stays at the tip", GREY, 26).move_to([3.3, tips[i] + (0.42 if i == 1 else -0.5), 0]) for i in stays]
        self.play(FadeIn(evs, scale=0.5), *[FadeIn(t) for t in stay_tags], run_time=0.3)
        t1 = tag("trafficking", TEAL, 36, weight=BOLD)
        t2 = tag(", not only binding", GREY, 36)
        row = VGroup(t1, t2).arrange(RIGHT, buff=0.04, aligned_edge=DOWN).move_to([-0.4, -3.4, 0])
        wait_t = max(0.05, self.t_of("trafficking") - 0.2 - self.elapsed())
        self.play(*anims, Succession(Wait(wait_t), FadeIn(t1, shift=UP * 0.1, run_time=0.4)))
        self.at("not only", lead=0.2)
        self.play(FadeIn(t2, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S22Take(SpokenScene):
    """Closing card: survival needs a signal that reaches home still able to signal."""

    def construct(self):
        top = tag("TAKEAWAY", GOLD, 28, weight=BOLD).move_to([0, 3.4, 0])
        l1 = T("Binding at the tip is not enough.", 44, TEXT, font=TITLE_FONT).move_to([0, 2.4, 0])
        l2a = T("Survival needs a signal that makes it home", 44, TEAL, font=TITLE_FONT)
        l2b = T("still able to signal.", 44, TEAL, font=TITLE_FONT)
        l2 = VGroup(l2a, l2b).arrange(DOWN, buff=0.2).move_to([0, 0.95, 0])
        fit(l2, max_w=12.4)
        nuc = Circle(radius=0.95, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.12).move_to([-5.3, -2.0, 0])
        line = Line([-4.3, -2.0, 0], [4.4, -2.0, 0], color=GREY, stroke_width=10)
        rb = rec_bar([4.7, -2.0, 0], 1.9)
        yd = dot([5.2, -2.0, 0], YELLOW, 0.2)
        tl = tag("tip: bound", YELLOW, 28).move_to([4.9, -3.15, 0])
        cb = tag("cell body: dim", GREY, 28).move_to([-5.0, -3.4, 0])
        self.at("take away", lead=0.0)
        self.play(FadeIn(top), run_time=0.4)
        self.at("binding at the tip", lead=0.2)
        self.play(FadeIn(l1, shift=UP * 0.15), FadeIn(line), FadeIn(rb), FadeIn(yd), FadeIn(nuc), FadeIn(tl), FadeIn(cb),
                  run_time=0.8)
        self.at("survival needs", lead=0.1)
        self.play(FadeIn(l2, shift=UP * 0.15), run_time=0.8)
        self.at("makes it home", lead=0.2)
        ev = endo([3.6, -2.0, 0], 0.9)
        self.play(FadeIn(ev, scale=0.5), run_time=0.3)
        glide(ev, 7.9, max(1.8, self.narration_s - self.elapsed() - 0.2))
        rest = self.narration_s - 0.1 - self.elapsed()
        if rest > 0:
            self.wait(rest)
        cb2 = tag("cell body: signal arrived", TEAL, 28).move_to([-4.3, -3.4, 0])
        self.play(nuc.animate.set_fill(PURPLE, 0.75), ReplacementTransform(cb, cb2), FadeOut(ev), run_time=0.4)
        self.finish()


class S23End(EndCard):
    LINE = "Survival needs a signal that reaches home still able to signal."
