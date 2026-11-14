"""Scene components for the explainer films: the pieces animators rebuilt in every film, laid out
safely by construction (inside the frame, labels clear of each other, text 24 pt or more).

    from bp_parts import *      # everything in bp_style, plus the components below

Read this list first and build from these where one fits; draw by hand only the lesson's own picture.

    fit_text      text that shrinks (not below 24) and then wraps to a width
    boxed_label   a label in a box sized to it (or fitted into a fixed box), never spilling past the border
    Plot          axes with ticks that never collide, computed curves, a growing curve, a tracker dot
    counter       a live number tied to a ValueTracker, at a fixed spot
    Readout       a boxed panel of live numbers ("N = 512", "rate = +0.12 /day"), sized for the widest value
    dial          a half-circle gauge with needle and percent, tied to a ValueTracker
    countdown     the predict beat's 5 s ring (returns the ring and the animation)
    TwoPanel      two framed side-by-side panels with headings; .put(mob, "left") fits a picture in a panel
    Ledger        a table whose rows are revealed, changed and marked one at a time
    question_card the predict question with optional answer chips, in the bottom band
    PredictPause  the silent 5 s pause scene: rebuild the picture, hold the question, run the ring
    place_label   put a label next to a target on the first side that is free and inside the frame
    scope_tag     "schematic" / "in this model" tag in the fixed bottom-right safe zone
    caption       one line in the bottom band (not a subtitle: a stated rule or a summary line)
    swap          replace one label by another with no moment where both overlap
    bob, pulse    small idle motion so a held frame is never dead

Zones (16:9 frame 14.22 x 8): main picture y -2.5..3.0; heading band y 3.0..3.55; bottom band
y -3.55..-2.6 (question card, caption, scope tag on the right). The layout check (layout_check.py)
runs on every render; these components pass it by default.

What the check reports (2026-11-14) and the usual fix:
    covered / straddle   a line or outline through a label or through its chip: move the label (the hint
                         says which way and how far), route the line around it, or end the arrow at the
                         chip's edge (chip.get_right() + RIGHT * 0.1), never inside it
    box_overlap / near   chips touching or overlapping: arrange(..., buff=0.3) or place_label(avoid=[...])
    overflow             letters past their own box: boxed_label(...) sizes the box to the text
    outside              a bar or fill past its panel: TwoPanel.put / fit the picture to the panel area
    small                under 22 pt after a group scale: scale the picture, add the label after
    in motion            old and new text visible together in a cross-fade: swap(old, new)
Do not hide a finding with `layout_ok`: it is for deliberate designs only, and opted-out findings are
still listed under "suppressed" in layout_report.json for the frame checker.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403
from bp_style import T, M, chip, fit, FONT, MONO, TEAL, GOLD, SAFE_W, SAFE_H, NarratedScene, TEXT, GREY, BG

MIN_SIZE = 24
FRAME_X = 6.75        # usable half-width (layout check: 2% of the width from each side)
FRAME_Y = 3.75        # usable half-height
HEAD_Y = 3.3          # centre of the heading band
BOTTOM_Y = -3.1       # centre of the bottom band


# ------------------------------------------------------------------ text
def fit_text(text, max_w=11.0, size=30, color=TEXT, min_size=MIN_SIZE, max_lines=3, font=FONT, weight=NORMAL, **kw):
    """Text that fits `max_w`: first shrinks toward `min_size`, then wraps at spaces (up to `max_lines`).

        t = fit_text("each new gram of tissue needs more oxygen than the surface brings in", max_w=5, size=30)
        t.move_to(LEFT * 3)
    """
    t = T(text, size, color, font=font, weight=weight, **kw)
    if t.width <= max_w:
        return t
    s = max(min_size, size * max_w / t.width)
    t = T(text, s, color, font=font, weight=weight, **kw)
    if t.width <= max_w:
        return t
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if cur and T(trial, min_size, font=font, weight=weight).width > max_w:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    lines.append(cur)
    lines = lines[:max_lines - 1] + [" ".join(lines[max_lines - 1:])] if len(lines) > max_lines else lines
    t = T("\n".join(lines), min_size, color, font=font, weight=weight, line_spacing=0.8, **kw)
    return fit(t, max_w=max_w)


def boxed_label(text, color=TEXT, size=28, box=None, pad=0.22, min_size=MIN_SIZE, stroke=2.5, fill_opacity=0.16,
                corner_radius=0.14):
    """A label in a rounded box. Without `box`, the box is sized to the text plus `pad` (like chip()). With
    `box=(w, h)`, the text is shrunk to fit that fixed size, but not below `min_size`; if it still does not
    fit, the box grows to hold it and a note is printed, so the letters never cross the border.

        g = boxed_label("people choose", TEAL, box=(2.4, 0.52))   # prints a note; box widened to fit
        g.box, g.label
    """
    lab = T(text, size, color)
    if box is None:
        w, h = lab.width + 2 * pad, lab.height + 2 * pad
    else:
        w, h = box
        s = min(1.0, (w - 2 * pad) / lab.width, (h - pad) / lab.height)   # half the padding above and below
        if s < 1.0:
            lab = T(text, max(min_size, size * s), color)
        if lab.width > w - 2 * pad + 1e-6 or lab.height > h - pad + 1e-6:
            nw, nh = max(w, lab.width + 2 * pad), max(h, lab.height + pad)
            print(f"[boxed_label] {text!r} does not fit a {w:g} x {h:g} box at {min_size} pt: box enlarged to "
                  f"{nw:.2f} x {nh:.2f}")
            w, h = nw, nh
    rect = RoundedRectangle(corner_radius=min(corner_radius, h / 2), width=w, height=h, stroke_color=color,
                            stroke_width=stroke, fill_color=color, fill_opacity=fill_opacity)
    g = VGroup(rect, lab.move_to(rect))
    g.box, g.label = rect, lab
    return g


# ------------------------------------------------------------------ plots
class Plot(VGroup):
    """Hand-built axes (no LaTeX) mapping data to a box in scene units, with tick labels that cannot collide.

        P = Plot(box=(-5.6, 0.0, -2.2, 2.4), xr=(0, 30), yr=(0, 1200),
                 xticks=[0, 10, 20, 30], yticks=[(0, "0"), (500, "500"), (1000, "1000")],
                 xlabel="time (days)", ylabel="N")
        curve = P.curve(lambda t: 1000 / (1 + 9 * np.exp(-0.3 * t)), color=WHITE)
        t = ValueTracker(0)
        live = P.live_curve(lambda t: 1000 / (1 + 9 * np.exp(-0.3 * t)), t)   # draws up to t
        dot = P.dot(lambda: t.get_value(), lambda: 1000 / (1 + 9 * np.exp(-0.3 * t.get_value())))
        self.play(Create(P)); self.add(live, dot); self.play(t.animate.set_value(30), run_time=6)

    P.pt(x, y) gives the scene point for data (x, y). Curves are clipped to the y-range, so a steep
    curve never runs off the plot. Ticks: values or (value, "label"); a label that would touch its
    neighbour is dropped (the tick stays). The y label sits above the y axis, left-aligned.
    """

    def __init__(self, box, xr, yr, xticks=(), yticks=(), xlabel="", ylabel="", color=GREY, size=24, label_size=26,
                 stroke=3):
        super().__init__()
        self.x0, self.x1, self.y0, self.y1 = box
        self.xr, self.yr = xr, yr
        self.axes = VGroup(Line([self.x0, self.y0, 0], [self.x1, self.y0, 0], color=color, stroke_width=stroke),
                           Line([self.x0, self.y0, 0], [self.x0, self.y1, 0], color=color, stroke_width=stroke))
        self.ticks, self.tick_labels = VGroup(), VGroup()
        for axis, ticks in (("x", xticks), ("y", yticks)):
            placed = []
            for tk in ticks:
                v, lab = tk if isinstance(tk, (tuple, list)) else (tk, f"{tk:g}")
                p = self.pt(v, yr[0]) if axis == "x" else self.pt(xr[0], v)
                d = DOWN if axis == "x" else LEFT
                self.ticks.add(Line(p, p + d * 0.1, color=color, stroke_width=stroke))
                t = T(lab, size, color).next_to(p, d, buff=0.14)
                if any(_touch(t, q, 0.12) for q in placed):
                    continue
                placed.append(t)
                self.tick_labels.add(t)
        self.add(self.axes, self.ticks, self.tick_labels)
        self.xlabel = self.ylabel = None
        if xlabel:
            below = self.tick_labels[0].get_bottom()[1] if len(xticks) else self.y0
            self.xlabel = T(xlabel, label_size, color).move_to([(self.x0 + self.x1) / 2, min(below, self.y0) - 0.35, 0])
            self.add(self.xlabel)
        if ylabel:
            self.ylabel = T(ylabel, label_size, color).next_to([self.x0, self.y1, 0], UP, buff=0.18)
            self.ylabel.align_to([self.x0 - 0.3, 0, 0], LEFT)
            self.add(self.ylabel)

    def pt(self, x, y):
        fx = (x - self.xr[0]) / (self.xr[1] - self.xr[0])
        fy = (y - self.yr[0]) / (self.yr[1] - self.yr[0])
        return np.array([self.x0 + fx * (self.x1 - self.x0), self.y0 + fy * (self.y1 - self.y0), 0.0])

    def _pts(self, fn, x0, x1, n):
        xs = np.linspace(x0, x1, n)
        ys = np.array([fn(x) for x in xs], dtype=float)
        ok = (ys >= self.yr[0] - 1e-9) & (ys <= self.yr[1] + 1e-9)
        return [self.pt(x, y) for x, y in zip(xs[ok], ys[ok])]

    def curve(self, fn, x0=None, x1=None, color=TEXT, width=6, n=160, opacity=1.0):
        """A computed curve y = fn(x) over [x0, x1] (default: the whole x range), clipped to the plot."""
        x0 = self.xr[0] if x0 is None else x0
        x1 = self.xr[1] if x1 is None else x1
        m = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity, fill_opacity=0)
        pts = self._pts(fn, x0, x1, n)
        if len(pts) >= 2:
            m.set_points_as_corners(pts)
        return m

    def live_curve(self, fn, tracker, color=TEXT, width=6, x0=None):
        """The curve drawn from x0 up to tracker's value, redrawn every frame (always_redraw)."""
        x0 = self.xr[0] if x0 is None else x0

        def mk():
            x1 = tracker.get_value()
            m = VMobject(stroke_color=color, stroke_width=width, fill_opacity=0)
            if x1 - x0 > 1e-6:
                pts = self._pts(fn, x0, x1, max(3, int(160 * (x1 - x0) / (self.xr[1] - self.xr[0])) + 2))
                if len(pts) >= 2:
                    m.set_points_as_corners(pts)
            return m
        return always_redraw(mk)

    def dot(self, xf, yf, color=TEXT, ring=TEAL, radius=0.12):
        """A tracker dot at (xf(), yf()) in data units, redrawn every frame."""
        return always_redraw(lambda: Dot(self.pt(xf(), yf()), radius=radius, color=color, stroke_color=ring, stroke_width=3))

    def hline(self, y, label=None, color=GREY, size=26, dashed=True):
        """A horizontal reference line (e.g. K) with its label at the right end, above the line."""
        a, b = self.pt(self.xr[0], y), self.pt(self.xr[1], y)
        ln = DashedLine(a, b, color=color, stroke_width=3, dash_length=0.14) if dashed else Line(a, b, color=color, stroke_width=3)
        g = VGroup(ln)
        if label:
            g.add(T(label, size, color).next_to(b, UP, buff=0.12).align_to(b, RIGHT))
        return g

    def vline(self, x, label=None, color=GREY, size=26, dashed=True):
        """A vertical reference line with its label above the plot's top."""
        a, b = self.pt(x, self.yr[0]), self.pt(x, self.yr[1])
        ln = DashedLine(a, b, color=color, stroke_width=3, dash_length=0.14) if dashed else Line(a, b, color=color, stroke_width=3)
        g = VGroup(ln)
        if label:
            g.add(T(label, size, color).next_to(b, UP, buff=0.12))
        return g


def _touch(a, b, buff=0.0):
    return not (a.get_right()[0] + buff < b.get_left()[0] or b.get_right()[0] + buff < a.get_left()[0]
                or a.get_top()[1] + buff < b.get_bottom()[1] or b.get_top()[1] + buff < a.get_bottom()[1])


# ------------------------------------------------------------------ live numbers
def counter(fmt, tracker, at, size=32, color=TEXT, mono=True):
    """A live number at a fixed spot: fmt.format(tracker value). Centre stays put as the digits change.

        n = ValueTracker(1)
        c = counter("volume × {:.0f}", n, at=[4.5, 2.6, 0], color=GOLD)
        self.add(c); self.play(n.animate.set_value(8), run_time=3)
    """
    mk = M if mono else T
    return always_redraw(lambda: mk(fmt.format(tracker.get_value()), size, color).move_to(at))


class Readout(VGroup):
    """A boxed panel of live numbers, one row each, sized once for the widest value so nothing touches the border.

        N = ValueTracker(100)
        r = Readout([("N", lambda: N.get_value(), "{:6.0f}", TEXT),
                     ("rate", lambda: 0.2 * (1 - N.get_value() / 1000), "{:+6.2f} /day", TEAL)],
                    at=[4.2, -1.8, 0], widest=[1000, -0.25])
        self.play(FadeIn(r)); self.play(N.animate.set_value(900), run_time=4)

    rows: (label, value function, format, colour). widest: the values that print widest (default: the
    values at build time). Values are monospace; labels are left-aligned and padded to the same width.
    """

    def __init__(self, rows, at=ORIGIN, size=28, widest=None, title=None, pad=0.3, color=GREY):
        super().__init__()
        n = max(len(r[0]) for r in rows)
        widest = widest or [r[1]() for r in rows]
        sample = VGroup(*[M(f"{r[0]:<{n}} = " + r[2].format(w), size) for r, w in zip(rows, widest)]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        w, h = sample.width + 2 * pad + 0.2, sample.height + 2 * pad
        ttl = None
        if title:
            ttl = T(title, 24, GREY)
            w = max(w, ttl.width + 2 * pad)
            h += ttl.height + 0.15
        self.box = RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_color=color, stroke_width=2.5,
                                    fill_color=BG, fill_opacity=0.9).move_to(at)
        self.add(self.box)
        top = self.box.get_top()[1] - pad
        if ttl:
            ttl.move_to([self.box.get_center()[0], top - ttl.height / 2, 0])
            self.add(ttl)
            top -= ttl.height + 0.15
        left = self.box.get_left()[0] + pad
        rows_h = sample.height

        def mk():
            g = VGroup(*[M(f"{r[0]:<{n}} = " + r[2].format(r[1]()), size, r[3]) for r in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
            g.move_to([left + g.width / 2, top - rows_h / 2, 0])
            return g
        self.rows = always_redraw(mk)
        self.add(self.rows)


def dial(tracker, center, radius=1.4, label="", color=BLUE, fmt="{:.0f}%", scale=100.0, size=40):
    """A half-circle gauge: grey track, coloured arc and needle at tracker's value (0..1), number inside, label below.

        f = ValueTracker(0.2)
        d = dial(f, center=[3.5, 0.5, 0], label="take-back")
        self.play(FadeIn(d)); self.play(f.animate.set_value(0.99), run_time=3)
    """
    c = np.array(center, dtype=float)
    track = Arc(radius=radius, start_angle=PI, angle=-PI, arc_center=c, stroke_color=GREY, stroke_width=10)
    v = lambda: float(np.clip(tracker.get_value(), 0.001, 1.0))
    val = always_redraw(lambda: Arc(radius=radius, start_angle=PI, angle=-PI * v(), arc_center=c, stroke_color=color, stroke_width=10))
    needle = always_redraw(lambda: Line(c, c + 0.8 * radius * np.array([np.cos(PI - PI * v()), np.sin(PI - PI * v()), 0]),
                                        color=TEXT, stroke_width=5))
    num = always_redraw(lambda: M(fmt.format(tracker.get_value() * scale), size, TEXT).move_to(c + DOWN * 0.45))
    g = VGroup(track, val, needle, num)
    if label:
        g.add(T(label, 28, color).move_to(c + DOWN * (0.45 + 0.65)))
    return g


def countdown(seconds=5.0, center=(6.0, -3.0, 0), radius=0.45, color=GOLD):
    """The predict beat's ring that empties over `seconds`. Returns (ring, animation).

        ring, run = countdown(5, center=[5.9, -3.0, 0])
        self.add(ring); self.play(run); self.finish()
    """
    c = np.array(center, dtype=float)
    pr = ValueTracker(1.0)
    bg = Circle(radius=radius, color=GREY, stroke_width=4).move_to(c).set_opacity(0.5)
    arc = always_redraw(lambda: Arc(radius=radius, start_angle=PI / 2, angle=max(pr.get_value(), 0.001) * TAU,
                                    color=color, stroke_width=8, arc_center=c))
    return VGroup(bg, arc), pr.animate(run_time=seconds, rate_func=linear).set_value(0.0)


# ------------------------------------------------------------------ layouts
class TwoPanel(VGroup):
    """Two framed panels side by side with headings: the standard before/after or this/that comparison.

        tp = TwoPanel("small population", "large population", colors=(GOLD, BLUE))
        self.play(FadeIn(tp))
        tp.put(left_picture, "left")      # scales down (never up) to fit the panel, and centres it
        tp.put(right_picture, "right")
        self.play(FadeIn(left_picture), FadeIn(right_picture))

    The panels fill y -2.5..3.0 by default, leaving the bottom band free for a caption or question.
    """

    def __init__(self, left, right, colors=(BLUE, GOLD), top=3.0, bottom=-2.5, gap=0.4, width=12.8, size=32):
        super().__init__()
        w = (width - gap) / 2
        h = top - bottom
        self.areas = {}
        for side, title, col, x in (("left", left, colors[0], -(w + gap) / 2), ("right", right, colors[1], (w + gap) / 2)):
            frame = RoundedRectangle(corner_radius=0.18, width=w, height=h, stroke_color=col, stroke_width=2.5).move_to([x, (top + bottom) / 2, 0])
            head = fit_text(title, max_w=w - 0.5, size=size, color=col).move_to([x, top - 0.45, 0])
            self.add(frame, head)
            inner_top = head.get_bottom()[1] - 0.2
            self.areas[side] = (np.array([x, (inner_top + bottom + 0.2) / 2, 0]), w - 0.5, inner_top - bottom - 0.4)
            setattr(self, side + "_frame", frame)
            setattr(self, side + "_head", head)

    def area(self, side):
        """(centre, width, height) of the free area under a panel's heading."""
        return self.areas[side]

    def put(self, mob, side):
        c, w, h = self.areas[side]
        fit(mob, max_w=w, max_h=h)
        return mob.move_to(c)


class Ledger(VGroup):
    """A table whose rows appear one at a time and can be updated or marked: a tally, a balance, a summary.

        L = Ledger([("glucose", "nearly all taken back", GREEN),
                    ("sodium", "most taken back", ORANGE),
                    ("water", "about 99% taken back", BLUE)], top_left=[-6.4, -1.0], title="what leaves")
        self.play(FadeIn(L))                       # title (and rule) only
        self.play(L.reveal(0)); self.play(L.reveal(1))
        self.play(L.change(1, "a small share excreted"))
        self.play(L.mark(2))                       # a gold underline, not a scale-up
        self.play(FadeOut(L.everything()))

    Rows sit on a fixed grid (row_h apart); values are fitted to the value column so they cannot spill.
    """

    def __init__(self, rows, top_left=(-6.4, 1.0), title=None, row_h=0.5, key_w=2.6, width=8.0, size=28):
        super().__init__()
        x0, y0 = top_left
        self.size, self.row_h, self.val_x, self.val_w = size, row_h, x0 + key_w, width - key_w
        y = y0
        if title:
            t = T(title, size, GREY).move_to([x0, y, 0], aligned_edge=LEFT)
            rule = Line([x0, y - 0.3, 0], [x0 + width, y - 0.3, 0], color=GREY, stroke_width=2)
            self.add(t, rule)
            y -= 0.3 + row_h * 0.8
        self.rows, self.revealed = [], []
        for k, v, col in rows:
            key = fit_text(k, max_w=key_w - 0.2, size=size, color=col).move_to([x0, y, 0], aligned_edge=LEFT)
            val = self._val(v, y)
            self.rows.append(VGroup(key, val))
            y -= row_h

    def _val(self, text, y):
        return fit_text(text, max_w=self.val_w, size=self.size, color=TEXT, max_lines=1).move_to([self.val_x, y, 0], aligned_edge=LEFT)

    def reveal(self, i, shift=RIGHT * 0.15):
        self.revealed.append(self.rows[i])
        return FadeIn(self.rows[i], shift=shift)

    def change(self, i, text):
        old = self.rows[i][1]
        new = self._val(text, old.get_center()[1])
        self.rows[i].submobjects[1] = new
        return AnimationGroup(FadeOut(old), FadeIn(new))

    def mark(self, i, color=GOLD):
        r = self.rows[i]
        u = Line(r.get_corner(DL) + DOWN * 0.08, r.get_corner(DR) + DOWN * 0.08, color=color, stroke_width=4)
        self.revealed.append(u)
        return Create(u)

    def everything(self):
        return VGroup(self, *self.revealed)


def question_card(question, options=(), y=BOTTOM_Y + 0.15, color=GOLD, size=30, chip_size=26, chips_at=None, left=None, max_w=10.2):
    """The predict question in the bottom band, with optional answer chips.

        q = question_card("Where is it adding the most per day?", ["when N is small", "halfway to K", "at K"],
                          chips_at=[4.3, 0.5, 0])      # a column in free space beside the picture
        self.play(FadeIn(q.chips)); self.play(FadeIn(q.question))

    Without chips_at the chips sit in a row just above the question (y about -2.3): use that only when
    the picture stops above y = -1.9. Sized to leave room for the countdown ring at the bottom right.
    left: x of the question's left edge (default: centred at x = -0.5); max_w: its width limit, for a
    bottom band shared with a plot's axis labels.
    """
    g = VGroup()
    q = fit_text(question, max_w=max_w, size=size, color=color, max_lines=2).move_to([-0.5, y, 0])
    if left is not None:
        q.align_to([left, 0, 0], LEFT)
    g.add(q)
    if options:
        row = VGroup(*[chip(o, TEXT, chip_size) for o in options])
        if chips_at is not None:
            row.arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(chips_at)
        else:
            row.arrange(RIGHT, buff=0.3)
            fit(row, max_w=11.5)
            row.next_to(q, UP, buff=0.3)
        g.add(row)
        g.chips = row
    g.question = q
    return g


class PredictPause(NarratedScene):
    """The silent predict pause: the previous picture, the question held still, and a 5 s ring.

        class S08Pause(PredictPause):
            QUESTION = "Where is it adding the most per day?"
            OPTIONS = ["when N is small", "halfway to K", "right at K"]
            def backdrop(self):
                return world_after_s07()        # the same builder the spoken scene used

    Set SECONDS to change the hold. The spoken predict scene before it should show question_card(...)
    with the same words, so the pause starts on the exact same frame.
    """
    QUESTION = "Pause and predict."
    OPTIONS = ()
    CHIPS_AT = None
    CARD = {}           # extra question_card arguments, e.g. {"left": -6.6, "y": -3.5, "size": 26}
    RING_AT = (6.0, -3.0, 0)
    SECONDS = 5.0

    def backdrop(self):
        return VGroup()

    def construct(self):
        self.add(self.backdrop())
        self.add(question_card(self.QUESTION, self.OPTIONS, chips_at=self.CHIPS_AT, **self.CARD))
        ring, run = countdown(self.SECONDS, center=self.RING_AT)
        self.add(ring)
        self.play(run)
        self.finish()


# ------------------------------------------------------------------ labels
def place_label(label, target, avoid=(), dirs=(UP, RIGHT, DOWN, LEFT, UR, UL, DR, DL), buff=0.18):
    """Put `label` beside `target` on the first side where it stays inside the frame and clear of `avoid`.

        lab = place_label(T("surface", 28, GOLD), cube, avoid=[title, other_label])
        self.play(FadeIn(lab))

    Falls back to the first side if none is free (and the layout check will then report it).
    """
    for d in dirs:
        label.next_to(target, d, buff=buff)
        inside = (label.get_left()[0] > -FRAME_X and label.get_right()[0] < FRAME_X
                  and label.get_bottom()[1] > -FRAME_Y and label.get_top()[1] < FRAME_Y)
        if inside and not any(_touch(label, a, 0.08) for a in avoid):
            return label
    return label.next_to(target, dirs[0], buff=buff)


def scope_tag(text="schematic", size=24, color=GREY):
    """The scope tag ("schematic", "in this model", "not to scale") in the bottom-right safe corner.

        self.add(scope_tag("in this model"))
    """
    t = T(text, size, color)
    return t.move_to([FRAME_X - 0.2 - t.width / 2, -FRAME_Y + 0.3 + t.height / 2, 0])


def caption(text, size=30, color=TEXT, y=BOTTOM_Y):
    """One stated line in the bottom band (fitted to 10.5 units so the scope tag still fits beside it)."""
    return fit_text(text, max_w=10.5, size=size, color=color, max_lines=2).move_to([-0.9, y, 0])


def swap(old, new, run_time=0.8):
    """Replace one label by another without the two ever overlapping half-faded (a common leftover).

        self.play(swap(old_label, new_label))
    """
    return Succession(FadeOut(old, run_time=run_time * 0.45), FadeIn(new, run_time=run_time * 0.55))


# ------------------------------------------------------------------ idle motion
def bob(m, amp=0.04, speed=2.0, seed=0):
    """Gentle up-and-down drift (an animal breathing, a bead resting). Returns m with an updater."""
    m._bob_t, base = seed * 0.7, m.get_center().copy()

    def u(mob, dt):
        mob._bob_t += dt
        mob.move_to(base + UP * amp * np.sin(speed * mob._bob_t))
    return m.add_updater(u)


def pulse(m, base=6.0, amp=2.5, speed=4.0):
    """A curve or outline whose stroke width breathes, to keep the subject alive while a sentence lands."""
    m._pt = 0.0

    def u(mob, dt):
        mob._pt += dt
        mob.set_stroke(width=base + amp * np.sin(speed * mob._pt))
    return m.add_updater(u)


__all__ = [n for n in dir() if not n.startswith("_")]
