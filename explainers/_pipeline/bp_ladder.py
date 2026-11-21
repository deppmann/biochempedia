"""The hop ladder for films: the site's ladder (src/components/hop/Ladder.astro, src/styles/hop.css) drawn
for a film's dark ground. One drawing, so every film that shows hopping shows the same ladder.

    from bp_ladder import HopLadder

    lad = HopLadder([dict(level="Grade 7", title="Diffusion and Osmosis", adds="Water drifts to the saltier side."),
                     dict(level="High school")], here=1)          # simplest level FIRST; here = Hex's rung
    self.add(lad)                       # rails, rungs, level labels, "Deeper"/"Simpler", Hex on its rung
    self.play(FadeIn(lad.fill(1, "Crossing the Membrane", "A plant cell's wall holds.")))   # a rung's lesson, later
    self.play(Create(lad.outline(0)))   # a thin teal outline round one rung's row
    lad.hop(self, 0)                    # Hex hops to rung 0 and lands (only when the narration says a reader hops)

The site's rules hold here too: up is deeper, down is simpler; the words are "Deeper" and "Simpler";
Hex marks "you are here" and nothing else; no rung is locked, greyed, filled or counted.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403


class HopLadder(VGroup):
    def __init__(self, rungs, here=None, x=-5.7, y_bottom=-3.0, spacing=1.6, text_w=6.0, hex_h=0.9,
                 level_size=22, title_size=26, note_size=22, **kw):
        super().__init__(**kw)
        self.x, self.y_bottom, self.spacing, self.text_w = x, y_bottom, spacing, text_w
        self.title_size, self.note_size = title_size, note_size
        self.n, self.here, self.half = len(rungs), here, 0.42
        top = self.rung_y(self.n - 1)
        self.rails = VGroup(*[Line([x + s * self.half, y_bottom - 0.2, 0], [x + s * self.half, top + 1.15, 0],
                                   color=TEXT, stroke_width=4) for s in (-1, 1)])
        self.rung_lines = VGroup(*[Line([x - self.half, self.rung_y(i), 0], [x + self.half, self.rung_y(i), 0],
                                        color=TEXT, stroke_width=6) for i in range(self.n)])
        for m in (*self.rails, *self.rung_lines):
            m.set_cap_style(CapStyleType.ROUND)
        self.deeper = T("Deeper", size=22, color=TEAL, weight=BOLD).move_to([x, top + 1.45, 0])
        self.simpler = T("Simpler", size=22, color=TEAL, weight=BOLD).move_to([x, y_bottom - 0.42, 0])
        self.levels = VGroup(*[T(r["level"], size=level_size, color=GOLD, weight=BOLD) for r in rungs])
        self.texts = [None] * self.n          # each rung's title + note, once filled
        for i in range(self.n):
            self._stack(i)
        # the reader's rung: gold laid on it, and Hex standing on it
        self.gold = Line([x - self.half * 0.8, 0, 0], [x + self.half * 0.8, 0, 0], color=GOLD, stroke_width=4)
        self.hex = hex_mascot(hex_h)
        self.hex.layout_ok = True
        self.gold.layout_ok = True
        self.add(self.rails, self.rung_lines, self.deeper, self.simpler, self.levels)
        if here is not None:
            self.gold.move_to([x, self.rung_y(here), 0])
            self.hex.move_to(self.stand(here))
            self.add(self.gold, self.hex)
        for i, r in enumerate(rungs):
            if r.get("title"):
                self.add(self.fill(i, r["title"], r.get("adds")))

    @property
    def text_x(self):
        return self.x + self.half + 0.4

    def rung_y(self, i):
        return self.y_bottom + i * self.spacing

    def stand(self, i):
        """Centre of Hex when its feet are on rung i."""
        return np.array([self.x, self.rung_y(i) + self.hex.height / 2 + 0.04, 0])

    def fill(self, i, title, adds=None):
        """Rung i's lesson title and the note on what that level adds, placed between the rung and its level label.
        Returns the group (not yet on screen): FadeIn it when the narration reaches that level."""
        t = fit_width(T(title, size=self.title_size, weight=BOLD), self.text_w)
        g = VGroup(t)
        if adds:
            g.add(wrap(adds, self.text_w, self.note_size))
        self.texts[i] = g
        self._stack(i)
        return g

    def _stack(self, i):
        """Rung i's words sit just above its rung and grow upward: note, title, level label."""
        parts = [*reversed(self.texts[i] or []), self.levels[i]]
        y = self.rung_y(i) + 0.12
        for m in parts:
            m.move_to([self.text_x, y, 0], aligned_edge=DL)
            y = m.get_top()[1] + 0.06

    def row(self, i):
        """Everything written on rung i (level label, and title and note if filled)."""
        return VGroup(self.levels[i], *(self.texts[i] or []))

    def outline(self, i, color=TEAL):
        """A thin outline round rung i's row of text: 'the narration is on this level'. It never moves Hex."""
        r = SurroundingRectangle(self.row(i), color=color, stroke_width=3, buff=0.07, corner_radius=0.1)
        r.layout_ok = True
        return r

    def hop(self, scene, i, run_time=0.7):
        """Hex hops from its rung to rung i in one arc and lands; the gold moves with it."""
        up = i > self.here
        self.here = i
        scene.play(self.hex.animate(path_arc=(-1.1 if up else 1.1)).move_to(self.stand(i)),
                   self.gold.animate.move_to([self.x, self.rung_y(i), 0]), run_time=run_time, rate_func=smooth)
        scene.play(self.hex.animate.shift(DOWN * 0.05), rate_func=there_and_back, run_time=0.18)


def fit_width(m, max_w):
    if m.width > max_w:
        m.scale(max_w / m.width)
    return m


def wrap(text, max_w, size, color=TEXT):
    """Left-aligned text wrapped to max_w (word wrap by measured width), at one size."""
    words, lines, cur = text.split(), [], ""
    probe = lambda s: T(s, size=size).width
    for w in words:
        if cur and probe(cur + " " + w) > max_w:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    lines.append(cur)
    return VGroup(*[T(l, size=size, color=color) for l in lines]).arrange(DOWN, buff=0.05, aligned_edge=LEFT)
