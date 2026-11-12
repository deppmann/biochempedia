"""The Size Test (Cells Are Everywhere, film 1)

COLOUR MAP (one colour per concept, whole film)
  BLUE   = the eye line (the limit of the eye, 100 um) and water
  BROWN  = frog egg      PINK = human egg      GREEN = green alga
  RED    = red blood cell  AMBER = bacterium   TEAL = Paramecium
  YELLOW = vocabulary, counters, the dial
  The size ladder is computed: y = Y0 + DEC * (log10(size in um) + 1).
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

BROWN = "#B9784A"
PINK = "#F2B8CC"
AMBER = "#F2A93B"
PAPER = "#F2F2F2"
STEEL = "#B8C0CC"

AX = -4.6          # x of the ladder axis
Y0 = -3.0          # y of 0.1 um
DEC = 1.24         # height of one decade (one rung)
EYE_X1 = 6.4       # right end of the eye line


def Y(v):
    """y on screen of a size v in micrometres (log ladder)."""
    return Y0 + DEC * (np.log10(v) + 1)


RUNGS = [(0.1, "0.1 µm"), (1, "1 µm"), (10, "10 µm"), (100, "100 µm"), (1000, "1,000 µm"), (10000, "10 mm")]
CELLS = {  # kind: (column x, real size in um, colour)
    "frog": (-3.4, 1000, BROWN),
    "human": (-2.0, 100, PINK),
    "alga": (-0.2, 20, GREEN),
    "rbc": (1.4, 7.7, RED),
    "bact": (3.0, 2, AMBER),
}


def icon(kind, s=1.0):
    """Cartoon cell icon, always the same colour. Not drawn to scale (the ladder carries the size)."""
    if kind == "frog":
        g = VGroup(Circle(0.38 * s, stroke_color="#7A4A2A", stroke_width=3, fill_color=BROWN, fill_opacity=1),
                   Circle(0.13 * s, stroke_width=0, fill_color="#D9A27A", fill_opacity=0.8).shift(UL * 0.15 * s))
    elif kind == "human":
        g = VGroup(Circle(0.3 * s, stroke_color="#C97A9A", stroke_width=3, fill_color=PINK, fill_opacity=1),
                   Circle(0.1 * s, stroke_width=0, fill_color="#E58FB0", fill_opacity=0.9))
    elif kind == "alga":
        g = VGroup(Circle(0.3 * s, stroke_color="#2E7D32", stroke_width=3, fill_color=GREEN, fill_opacity=1),
                   Circle(0.09 * s, stroke_width=0, fill_color="#B7E4A0", fill_opacity=0.9).shift(UL * 0.1 * s))
    elif kind == "rbc":
        g = VGroup(Ellipse(width=0.66 * s, height=0.5 * s, stroke_color="#9E2A2A", stroke_width=3, fill_color=RED, fill_opacity=1),
                   Ellipse(width=0.26 * s, height=0.18 * s, stroke_width=0, fill_color="#9E2A2A", fill_opacity=0.65))
    elif kind == "bact":
        g = VGroup(RoundedRectangle(corner_radius=0.1 * s, width=0.6 * s, height=0.22 * s, stroke_color="#A86A10",
                                    stroke_width=3, fill_color=AMBER, fill_opacity=1))
    elif kind == "para":
        body = Ellipse(width=1.0 * s, height=0.42 * s, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.55)
        hairs = VGroup()
        for th in np.linspace(0, 2 * np.pi, 26, endpoint=False):
            p = np.array([0.5 * s * np.cos(th), 0.21 * s * np.sin(th), 0])
            n = np.array([np.cos(th) * 0.5, np.sin(th) * 0.21, 0])
            n = n / np.linalg.norm(n)
            hairs.add(Line(p, p + n * 0.09 * s, color=TEAL, stroke_width=2))
        g = VGroup(body, hairs)
    else:
        raise ValueError(kind)
    return g


def wobble(m, amp=0.04, w=1.3, ph=0.0):
    """Slow ambient drift on a static object so a held frame is never dead."""
    base = m.get_center().copy()
    t = [ph]

    def u(mm, dt):
        t[0] += dt
        mm.move_to(base + np.array([amp * np.sin(w * t[0] + ph), amp * np.cos(1.3 * w * t[0] + ph), 0]))
    m.add_updater(u)
    return m


def make_ladder():
    axis = Line([AX, Y(0.1), 0], [AX, Y(10000), 0], color=STEEL, stroke_width=5)
    ticks = [Line([AX - 0.14, Y(v), 0], [AX + 0.14, Y(v), 0], color=STEEL, stroke_width=4) for v, _ in RUNGS]
    labs = []
    for v, t in RUNGS:
        lab = T(t, 28)
        lab.move_to([AX - 0.22 - lab.width / 2, Y(v), 0])
        labs.append(lab)
    return axis, ticks, labs


def grid(short=False):
    x1 = -2.2 if short else EYE_X1
    return VGroup(*[Line([AX, Y(v), 0], [x1, Y(v), 0], color="#2B3345", stroke_width=3) for v, _ in RUNGS if v != 100]).set_z_index(-3)


def eye_line(short=False):
    x1 = -2.2 if short else EYE_X1
    ln = Line([AX, Y(100), 0], [x1, Y(100), 0], color=BLUE, stroke_width=8)
    lab = T("eye line" if short else "eye line, 100 µm", 28, BLUE, weight=BOLD)
    lab.move_to([x1 - lab.width / 2 + 0.25, Y(100) + 0.3, 0])
    return ln, lab


def microscope(h=2.8):
    s = h / 2.8
    col = STEEL
    base = RoundedRectangle(corner_radius=0.08, width=1.7, height=0.2, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.8).move_to([0, -1.4, 0])
    arm = VMobject(color=col, stroke_width=14)
    arm.set_points_smoothly([[0.55, -1.3, 0], [0.9, -0.6, 0], [0.85, 0.3, 0], [0.4, 0.95, 0]])
    tube = Line([0.18, 1.2, 0], [-0.12, -0.05, 0], color=col, stroke_width=30)
    eyep = Line([0.2, 1.25, 0], [0.26, 1.55, 0], color=col, stroke_width=16)
    obj = Line([-0.13, -0.05, 0], [-0.16, -0.3, 0], color=TEAL, stroke_width=12)
    stage = Line([-0.75, -0.7, 0], [0.6, -0.7, 0], color=col, stroke_width=9)
    slide = Rectangle(width=0.7, height=0.07, stroke_width=0, fill_color=PAPER, fill_opacity=0.9).move_to([-0.2, -0.62, 0])
    g = VGroup(base, arm, stage, slide, tube, eyep, obj)
    g.scale(s)
    g.lens = obj
    return g


def gauge(lm, center=(6.2, -0.2)):
    """Dial gauge + readout, driven by a ValueTracker holding log10(magnification)."""
    c = np.array([center[0], center[1], 0])
    ring = Circle(0.46, stroke_color=STEEL, stroke_width=5, fill_color=BG, fill_opacity=1).move_to(c)

    def ang():
        return np.radians(-130 + lm.get_value() * 100)
    ptr = always_redraw(lambda: Line(c, c + 0.36 * np.array([np.sin(ang()), np.cos(ang()), 0]), color=YELLOW, stroke_width=7))
    hub = Dot(c, radius=0.06, color=YELLOW)
    rd = always_redraw(lambda: M(f"{int(round(10 ** lm.get_value()))}x", 34, YELLOW, weight=BOLD).move_to([center[0] - 0.05, center[1] - 0.95, 0]))
    return VGroup(ring, ptr, hub, rd)


def make_card(kind, lm):
    x, real, col = CELLS[kind]

    def yy():
        return Y(real * 10 ** lm.get_value())
    box = RoundedRectangle(corner_radius=0.1, width=0.95, height=0.95, stroke_color=col, stroke_width=3, fill_color=PAPER, fill_opacity=1)
    card = VGroup(box, icon(kind, 0.9))
    card.move_to([x, yy(), 0])
    card.add_updater(lambda m: m.move_to([x, yy(), 0]))
    ptr = always_redraw(lambda: Line([AX, yy(), 0], [x - 0.48, yy(), 0], color=col, stroke_width=3).set_opacity(0.8))
    return card, ptr


def rule_text():
    r = M("picture size = real size × magnification", 34, TEXT, weight=BOLD)
    fit(r, max_w=10.6)
    return r.move_to([1.0, -3.4, 0])


def callout(lines, y, color=YELLOW, x=5.2):
    g = VGroup(*[M(t, 28, color if i == len(lines) - 1 else TEXT, weight=BOLD) for i, t in enumerate(lines)]).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
    g.move_to([x, y, 0])
    return g


def schem():
    return T("schematic", 22, STEEL).move_to([6.1, 3.62, 0])


def ripples(center, r, n=3, period=3.0, color=BLUE):
    rings = VGroup(*[Circle(radius=r * 0.3).move_to(center) for _ in range(n)])
    clock = [0.0]

    def upd(g, dt):
        clock[0] += dt
        for i, ring in enumerate(g):
            ph = ((clock[0] / period) + i / n) % 1
            ring.become(Circle(radius=r * (0.3 + 0.7 * ph), stroke_color=color, stroke_width=3, stroke_opacity=0.55 * (1 - ph)).move_to(center))
    rings.add_updater(upd)
    return rings


class LS(SpokenScene):
    def add_ladder(self, labels=True, short=False):
        self.add(grid(short))
        axis, ticks, labs = make_ladder()
        self.axis, self.ticks, self.labs = axis, ticks, labs
        self.ladder = VGroup(axis, *ticks, *labs)
        self.add(self.ladder)
        return self.ladder

    def add_eye(self, short=False):
        self.eye, self.eyelab = eye_line(short)
        self.eyelab.set_z_index(20)
        self.add(self.eye, self.eyelab)

    def add_icons(self, kinds, wob=True):
        self.icons = {}
        for i, k in enumerate(kinds):
            x, real, col = CELLS[k]
            ic = icon(k, 1.35).move_to([x, Y(real), 0])
            if wob:
                wobble(ic, 0.06, 1.1 + 0.2 * i, i)
            self.icons[k] = ic
            self.add(ic)

    def add_scope(self):
        self.scope = microscope().move_to([4.45, -1.15, 0])
        self.add(self.scope)
        wobble(self.scope.lens, 0.0)  # placeholder, keeps lens in the same place
        self.scope.lens.clear_updaters()
        g = self.scope.lens
        g.t = 0.0

        def glow(m, dt):
            m.t += dt
            m.set_stroke(opacity=0.65 + 0.35 * np.sin(2.2 * m.t))
        g.add_updater(glow)


# ---------------------------------------------------------------- scenes

class S00Title(TitleCard):
    LESSON = "Cells Are Everywhere"
    TITLE = "The Size Test"


class S01Question(LS):
    def construct(self):
        jar = VGroup(
            RoundedRectangle(corner_radius=0.3, width=2.2, height=2.7, stroke_color="#9FD3E6", stroke_width=5,
                             fill_color=BLUE, fill_opacity=0.12),
            Rectangle(width=1.5, height=0.28, stroke_color=STEEL, stroke_width=3, fill_color=STEEL, fill_opacity=0.7).shift(UP * 1.45),
        ).move_to([-2.6, 1.2, 0])
        slide = Rectangle(width=4.6, height=0.2, stroke_color="#9FD3E6", stroke_width=3, fill_color="#9FD3E6", fill_opacity=0.3).move_to([-2.6, -1.9, 0])
        drop = Circle(0.2, stroke_color="#BFE6F2", stroke_width=3, fill_color=BLUE, fill_opacity=0.35).move_to([-2.6, -0.2, 0])
        self.at("This drop")
        self.play(FadeIn(jar, shift=DOWN * 0.3), FadeIn(slide), run_time=0.9)
        self.play(FadeIn(drop, scale=0.5), run_time=0.3)
        self.play(drop.animate.move_to([-2.6, -1.7, 0]), rate_func=rush_into, run_time=0.9)
        flat = Ellipse(width=1.7, height=0.3, stroke_color="#BFE6F2", stroke_width=3, fill_color=BLUE, fill_opacity=0.3).move_to([-2.6, -1.68, 0])
        self.play(Transform(drop, flat), run_time=0.6)
        self.at("Is it")
        q = T("?", 190, TEXT, weight=BOLD).move_to([4.5, 0.4, 0])
        self.play(FadeIn(q, scale=0.4), run_time=0.7)
        self.at("And if tiny living things")
        big = Circle(2.5, stroke_color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.14).move_to([0.3, 0.2, 0])
        rip = ripples([0.3, 0.2, 0], 2.5)
        self.play(FadeOut(jar), FadeOut(slide), ReplacementTransform(drop, big), run_time=1.4)
        self.add(rip)
        self.at("why can't your eyes")
        self.play(big.animate.scale(1.12), q.animate.shift(RIGHT * 0.3), run_time=2.3, rate_func=linear)
        self.at("To answer")
        self.play(Indicate(q, color=YELLOW, scale_factor=1.12), run_time=1.0)
        self.add(schem())
        self.finish()


class S02Ruler(LS):
    def construct(self):
        ruler = VGroup(Rectangle(width=12.6, height=1.7, stroke_color="#8A6D3B", stroke_width=4, fill_color="#D9B98A", fill_opacity=0.95))
        ticks = VGroup(*[Line([x, 0.85, 0], [x, 0.3, 0], color="#4B3716", stroke_width=3) for x in np.arange(-6.3 + 0.35, 6.3, 0.7)])
        ruler = VGroup(ruler, ticks).move_to([0, -0.4, 0])
        ruler.shift(LEFT * 14)
        self.add(ruler)
        self.play(ruler.animate.shift(RIGHT * 14), run_time=1.3, rate_func=rush_from)
        # two neighbouring marks
        i = 9
        t1, t2 = ticks[i], ticks[i + 1]
        x1, x2 = t1.get_x(), t2.get_x()
        self.at("Its smallest marks")
        self.play(t1.animate.set_stroke(YELLOW, 7), t2.animate.set_stroke(YELLOW, 7), run_time=0.5)
        br = Brace(Line([x1, 0.9, 0], [x2, 0.9, 0]), direction=UP, color=YELLOW)
        lab = T("1 mm", 40, YELLOW, weight=BOLD).next_to(br, UP, buff=0.1)
        self.play(GrowFromCenter(br), FadeIn(lab, shift=UP * 0.1), run_time=0.8)
        self.at("Now split")
        bar = Rectangle(width=11, height=1.5, stroke_color="#8A6D3B", stroke_width=4, fill_color="#D9B98A", fill_opacity=0.95).move_to([0, -0.2, 0])
        br2 = Brace(Line([-5.5, 0.55, 0], [5.5, 0.55, 0]), direction=UP, color=YELLOW)
        lab2 = T("1 mm", 40, YELLOW, weight=BOLD).next_to(br2, UP, buff=0.1)
        self.play(FadeOut(ruler), ReplacementTransform(br, br2), ReplacementTransform(lab, lab2), FadeIn(bar), run_time=1.3)
        self.at("into a thousand")
        cnt = M("10", 48, YELLOW, weight=BOLD).move_to([0, -1.6, 0])
        l10 = VGroup(*[Line([x, 0.55, 0], [x, -0.95, 0], color="#4B3716", stroke_width=3) for x in np.linspace(-5.5, 5.5, 11)[1:-1]])
        self.play(Create(l10), FadeIn(cnt), run_time=0.8)
        cnt2 = M("100", 48, YELLOW, weight=BOLD).move_to(cnt)
        l100 = VGroup(*[Line([x, 0.55, 0], [x, -0.95, 0], color="#4B3716", stroke_width=1.5) for x in np.linspace(-5.5, 5.5, 101)[1:-1]])
        self.play(FadeIn(l100), Transform(cnt, cnt2), run_time=0.7)
        cnt3 = M("1,000", 48, YELLOW, weight=BOLD).move_to(cnt)
        l1000 = VGroup(*[Line([x, 0.55, 0], [x, -0.95, 0], color="#4B3716", stroke_width=0.6) for x in np.linspace(-5.5, 5.5, 1001)[1:-1]])
        self.play(FadeIn(l1000), Transform(cnt, cnt3), run_time=0.7)
        self.at("Each tiny part")
        sliver = Rectangle(width=0.02, height=1.5, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to([-5.5 + 0.01, -0.2, 0])
        arrow = Arrow([-4.4, -2.2, 0], [-5.45, -1.05, 0], color=YELLOW, buff=0.05, stroke_width=6)
        self.play(FadeIn(sliver), GrowArrow(arrow), run_time=0.8)
        self.at("one micrometer")
        l1 = T("1 µm", 40, YELLOW, weight=BOLD).move_to([-3.6, -2.4, 0])
        self.play(FadeIn(l1, shift=UP * 0.1), run_time=0.6)
        eq = M("1 mm = 1,000 µm", 44, TEXT, weight=BOLD).move_to([2.2, -2.7, 0])
        self.play(FadeIn(eq, shift=UP * 0.1), Indicate(sliver, color=YELLOW, scale_factor=1.0), run_time=0.8)
        self.finish()


class S03Eye(LS):
    def construct(self):
        bar = Rectangle(width=11, height=1.5, stroke_color="#8A6D3B", stroke_width=4, fill_color="#D9B98A", fill_opacity=0.95).move_to([0, -0.2, 0])
        br = Brace(Line([-5.5, 0.55, 0], [5.5, 0.55, 0]), direction=UP, color=YELLOW)
        lab = T("1 mm", 40, YELLOW, weight=BOLD).next_to(br, UP, buff=0.1)
        self.play(FadeIn(bar), FadeIn(br), FadeIn(lab), run_time=0.6)
        # cartoon eye
        eye = VGroup(Ellipse(width=1.7, height=0.9, stroke_color=TEXT, stroke_width=4, fill_color=PAPER, fill_opacity=1),
                     Circle(0.3, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.9),
                     Dot(radius=0.13, color=BG)).move_to([-4.8, 2.7, 0])
        self.play(FadeIn(eye, scale=0.6), run_time=0.8)
        self.at("Most people")
        pup = VGroup(eye[1], eye[2])
        self.play(pup.animate.shift(DOWN * 0.12 + RIGHT * 0.12), run_time=0.7)
        tenth = Rectangle(width=1.1, height=1.5, stroke_width=0, fill_color=BLUE, fill_opacity=0.9).move_to([-5.5 + 0.55, -0.2, 0])
        self.at("smaller than about 100")
        self.play(FadeIn(tenth), run_time=0.5)
        brb = Brace(Line([-5.5, -0.95, 0], [-4.4, -0.95, 0]), direction=DOWN, color=BLUE)
        blab = T("0.1 mm = 100 µm", 34, BLUE, weight=BOLD).move_to([-2.4, -1.75, 0])
        self.play(GrowFromCenter(brb), FadeIn(blab, shift=UP * 0.1), run_time=0.8)
        self.at("a tenth of a millimeter")
        div = VGroup(*[Line([x, 0.55, 0], [x, -0.95, 0], color="#4B3716", stroke_width=3) for x in np.linspace(-5.5, 5.5, 11)[1:-1]])
        self.play(Create(div), run_time=1.0)
        self.play(Indicate(tenth, color=BLUE, scale_factor=1.05), run_time=0.8)
        self.at("We will draw that limit")
        ln, lnlab = eye_line()
        axis, ticks, labs = make_ladder()
        self.play(FadeOut(bar), FadeOut(br), FadeOut(lab), FadeOut(div), FadeOut(brb), FadeOut(blab), FadeOut(eye),
                  FadeIn(axis), run_time=0.7)
        self.play(ReplacementTransform(tenth, ln), run_time=1.5)
        self.at("the eye line")
        self.play(FadeIn(lnlab, shift=UP * 0.1), run_time=0.6)
        self.play(Indicate(ln, color=BLUE, scale_factor=1.0), run_time=0.8)
        self.finish()


class S04Ladder(LS):
    def construct(self):
        self.add_eye()
        axis, ticks, labs = make_ladder()
        gl = {v: Line([AX, Y(v), 0], [EYE_X1, Y(v), 0], color="#2B3345", stroke_width=3).set_z_index(-3) for v, _ in RUNGS if v != 100}
        self.play(Create(axis), run_time=0.6)
        for (v, _), tk, lb in zip(RUNGS, ticks, labs):
            anims = [FadeIn(tk), FadeIn(lb, shift=RIGHT * 0.1)]
            if v in gl:
                anims.append(Create(gl[v]))
            self.play(*anims, run_time=0.35)
        self.at("Each rung is ten times")
        tags = VGroup()
        climber = Dot(radius=0.14, color=YELLOW).move_to([AX, Y(0.1), 0])
        trail = Line([AX, Y(0.1), 0], [AX, Y(0.1), 0], color=YELLOW, stroke_width=9)
        self.add(trail, climber)
        for i in range(5):
            a, b = RUNGS[i][0], RUNGS[i + 1][0]
            t = chip("× 10", YELLOW, 30, pad=0.14).move_to([AX + 0.95, (Y(a) + Y(b)) / 2, 0])
            tags.add(t)
            self.play(climber.animate.move_to([AX, Y(b), 0]),
                      trail.animate.put_start_and_end_on([AX, Y(0.1), 0], [AX, Y(b), 0]),
                      FadeIn(t, shift=UP * 0.15), run_time=0.55)
            self.wait(0.1)
        self.at("We place real cells")
        self.play(FadeOut(tags), FadeOut(climber), FadeOut(trail), run_time=0.3)
        slots = VGroup()
        for k in ["frog", "human", "alga", "rbc", "bact"]:
            x, real, col = CELLS[k]
            s = DashedVMobject(Circle(0.5, stroke_color=col, stroke_width=3.5), num_dashes=14).move_to([x, Y(real), 0])
            slots.add(s)
            s.add_updater(lambda m, dt: m.rotate(0.6 * dt))
            self.play(GrowFromCenter(s), run_time=0.3)
        self.at("at their real sizes")
        self.play(*[Indicate(s, color=STEEL, scale_factor=1.15) for s in slots], run_time=1.0)
        self.finish()


class S05Cells(LS):
    def construct(self):
        self.add_ladder()
        self.add_eye()
        slots = {}
        for k in CELLS:
            x, real, col = CELLS[k]
            s = DashedVMobject(Circle(0.5, stroke_color=col, stroke_width=3.5), num_dashes=14).move_to([x, Y(real), 0])
            slots[k] = s
            s.add_updater(lambda m, dt: m.rotate(0.6 * dt))
            self.add(s)

        def drop_in(k, dur=0.9):
            x, real, col = CELLS[k]
            ic = icon(k, 1.35).move_to([x, 3.6, 0])
            self.add(ic)
            self.play(ic.animate.move_to([x, Y(real), 0]), FadeOut(slots[k]), rate_func=rush_into, run_time=dur)
            wobble(ic, 0.06, 1.2 + 0.15 * len(slots), len(slots))
            return ic

        self.at("A frog egg")
        frog = drop_in("frog")
        self.at("often about a millimeter")
        ftag = T("often about 1,000 µm", 28, TEXT).move_to([-3.4 + 0.55 + 2.0 + 1.25, Y(1000) + 0.32, 0])
        self.play(FadeIn(ftag, shift=RIGHT * 0.1), run_time=0.6)
        self.at("It sits above")
        self.play(Indicate(self.eye, color=BLUE, scale_factor=1.0), run_time=1.0)
        self.at("so you can see it")
        tick = VMobject(color=GREEN, stroke_width=8)
        tick.set_points_as_corners([[-0.15, 0, 0], [0, -0.18, 0], [0.28, 0.2, 0]])
        see = T("you can see it", 28, GREEN, weight=BOLD)
        seeg = VGroup(tick, see).arrange(RIGHT, buff=0.2).move_to([-0.9, Y(1000) - 0.55, 0])
        self.play(Create(tick), FadeIn(see, shift=RIGHT * 0.1), run_time=0.8)
        self.at("A human egg")
        human = drop_in("human")
        self.at("about 100")
        htag = T("about 100 µm", 28, TEXT).move_to([-2.4, Y(100) - 0.72, 0])
        self.play(FadeIn(htag, shift=UP * 0.1), run_time=0.6)
        self.at("sits right on")
        self.play(Indicate(self.eye, color=BLUE, scale_factor=1.0), Indicate(human, color=PINK, scale_factor=1.3), run_time=1.0)
        self.at("A green alga")
        alga = drop_in("alga", 0.8)
        atag = T("20 µm", 28, TEXT).move_to([-0.2, Y(20) - 0.55, 0])
        self.play(FadeIn(atag, shift=UP * 0.1), run_time=0.4)
        self.at("a red blood cell")
        rbc = drop_in("rbc", 0.7)
        rtag = T("7.7 µm", 28, TEXT).move_to([1.4, Y(7.7) - 0.5, 0])
        self.play(FadeIn(rtag, shift=UP * 0.1), run_time=0.4)
        self.at("a bacterium")
        bact = drop_in("bact", 0.6)
        btag = T("2 µm", 28, TEXT).move_to([3.0, Y(2) - 0.45, 0])
        self.play(FadeIn(btag, shift=UP * 0.1), run_time=0.4)
        self.at("all sit below it")
        hid = T("hidden", 34, YELLOW, weight=BOLD).move_to([1.4, 0.42, 0])
        self.play(FadeIn(hid, shift=DOWN * 0.15), run_time=0.7)
        self.play(*[Indicate(m, scale_factor=1.25) for m in (alga, rbc, bact)], run_time=1.0)
        self.finish()


class S06Most(LS):
    def construct(self):
        self.add_ladder()
        self.add_eye()
        self.add_icons(["frog", "human", "alga", "rbc", "bact"])
        band = Rectangle(width=EYE_X1 - AX, height=Y(100) - Y(1), stroke_width=0, fill_color=YELLOW, fill_opacity=0.16)
        band.move_to([(AX + EYE_X1) / 2, (Y(100) + Y(1)) / 2, 0])
        band.set_z_index(-1)
        self.at("Most cells")
        self.play(GrowFromEdge(band, DOWN), run_time=1.3)
        blab = T("most cells", 34, YELLOW, weight=BOLD).move_to([-0.9, Y(1) + 0.35, 0])
        self.play(FadeIn(blab, shift=UP * 0.1), run_time=0.6)
        self.at("about 1 and 100")
        self.play(Indicate(self.labs[1], color=YELLOW, scale_factor=1.25), run_time=0.8)
        self.play(Indicate(self.labs[3], color=YELLOW, scale_factor=1.25), run_time=0.8)
        self.at("That puts most")
        self.play(Indicate(self.eye, color=BLUE, scale_factor=1.0),
                  *[Indicate(self.icons[k], scale_factor=1.3) for k in ("alga", "rbc", "bact")], run_time=1.4)
        self.at("too small to see")
        hid = T("hidden", 34, TEXT, weight=BOLD).move_to([1.4, 0.42, 0])
        self.play(FadeIn(hid, shift=DOWN * 0.15), run_time=0.7)
        self.play(Indicate(band, color=YELLOW, scale_factor=1.0), run_time=1.0)
        self.finish()


class S07Mag(LS):
    def construct(self):
        self.add_ladder()
        self.add_eye()
        self.add_icons(["frog", "human", "alga", "rbc", "bact"])
        scope = microscope().move_to([4.45 + 8, -1.45, 0])
        self.add(scope)
        self.at("A microscope uses")
        self.play(scope.animate.move_to([4.45, -1.45, 0]), run_time=1.3, rate_func=rush_from)
        g = scope.lens
        g.t = 0.0

        def glow(m, dt):
            m.t += dt
            m.set_stroke(opacity=0.65 + 0.35 * np.sin(2.2 * m.t))
        g.add_updater(glow)
        self.at("make small things")
        small = icon("rbc", 0.9).move_to([3.7, 2.75, 0])
        arrow = Arrow([4.15, 2.75, 0], [4.85, 2.75, 0], color=STEEL, buff=0.0, stroke_width=6)
        self.play(FadeIn(small, scale=0.5), run_time=0.5)
        big = icon("rbc", 2.2).move_to([5.7, 2.75, 0])
        self.play(GrowArrow(arrow), FadeIn(big, scale=0.3), run_time=1.0)
        lm = ValueTracker(0)
        self.at("Magnification is")
        gz = gauge(lm, center=(6.2, -0.45))
        mlab = T("magnification", 24, YELLOW, weight=BOLD).move_to([5.65, 0.4, 0])
        self.play(FadeIn(gz), FadeIn(mlab, shift=DOWN * 0.1), run_time=0.8)
        self.at("larger the picture")
        self.play(Indicate(big, scale_factor=1.15), run_time=0.8)
        self.at("picture looks")
        plab = T("picture", 30, TEXT, weight=BOLD).move_to([5.7, 1.95, 0])
        self.play(FadeIn(plab, shift=UP * 0.1), run_time=0.4)
        self.at("real thing")
        rlab = T("real", 30, TEXT, weight=BOLD).move_to([3.7, 2.2, 0])
        self.play(FadeIn(rlab, shift=UP * 0.1), run_time=0.4)
        self.play(FadeOut(self.icons["frog"]), FadeOut(self.icons["human"]), run_time=0.6)
        self.at("So the picture")
        self.play(FadeOut(VGroup(small, big, arrow, plab, rlab, mlab)), run_time=0.5)
        rule = rule_text()
        self.play(Write(rule), run_time=3.6, rate_func=linear)
        self.play(Indicate(rule, color=YELLOW, scale_factor=1.04), run_time=0.9)
        self.finish()


class S08Dial(LS):
    def construct(self):
        self.add_ladder()
        self.add_eye()
        self.add_icons(["alga", "rbc", "bact"])
        self.add_scope()
        self.add(rule_text())
        lm = ValueTracker(0)
        gz = gauge(lm)
        self.add(gz)
        cards = {}
        ptrs = {}
        for k in ("alga", "rbc", "bact"):
            c, p = make_card(k, lm)
            cards[k], ptrs[k] = c, p
        self.at("Turn the dial up")
        self.play(*[FadeIn(cards[k], scale=0.7) for k in cards], *[FadeIn(ptrs[k]) for k in ptrs], run_time=0.8)
        self.at("every picture slides")
        self.play(lm.animate.set_value(1.0), run_time=2.6, rate_func=smooth)
        self.at("The cells do not change")
        self.play(*[Indicate(self.icons[k], scale_factor=1.5) for k in self.icons], run_time=1.6)
        self.at("Only their pictures")
        self.play(*[Indicate(cards[k], color=PAPER, scale_factor=1.25) for k in cards], run_time=1.4)
        self.wait(0.3)
        self.at("Watch the red blood cell")
        self.play(FadeOut(cards["alga"]), FadeOut(ptrs["alga"]), FadeOut(cards["bact"]), FadeOut(ptrs["bact"]),
                  Indicate(cards["rbc"], color=PAPER, scale_factor=1.3), run_time=1.2)
        self.at("At 40 times")
        self.play(lm.animate.set_value(np.log10(40)), run_time=1.6, rate_func=smooth)
        self.at("its picture is already")
        co = callout(["7.7 µm × 40", "= 308 µm"], 2.6)
        self.play(Write(co), run_time=1.6)
        self.at("It has crossed")
        self.play(Indicate(self.eye, color=BLUE, scale_factor=1.0), Indicate(cards["rbc"], color=PAPER, scale_factor=1.3), run_time=1.4)
        self.finish()


class S09Predict(LS):
    def construct(self):
        self.add_ladder()
        self.add_eye()
        self.add_icons(["alga", "rbc"])
        self.add_scope()
        self.add(rule_text())
        lm = ValueTracker(np.log10(40))
        dl = ValueTracker(np.log10(40))
        gz = gauge(dl)
        self.add(gz)
        crbc, prbc = make_card("rbc", lm)
        co = callout(["7.7 µm × 40", "= 308 µm"], 2.6)
        self.add(crbc, prbc, co)
        self.play(lm.animate.set_value(0), dl.animate.set_value(0), FadeOut(co), run_time=0.45)
        self.play(FadeOut(crbc), FadeOut(prbc), run_time=0.15)
        self.at("green alga")
        lm_a = ValueTracker(0)
        calg, palg = make_card("alga", lm_a)
        halo = Circle(0.62, stroke_color=GREEN, stroke_width=6).move_to(calg)
        self.play(FadeIn(calg, scale=0.7), FadeIn(palg), Create(halo), run_time=0.8)
        halo.t = 0.0

        def pulse(m, dt):
            m.t += dt
            m.set_stroke(opacity=0.5 + 0.5 * np.sin(3 * m.t))
        halo.add_updater(pulse)
        self.at("about 20")
        alab = T("20 µm", 28, TEXT).move_to([-0.2, Y(20) - 0.88, 0])
        self.play(FadeIn(alab, shift=UP * 0.1), run_time=0.5)
        self.at("Set the dial")
        self.play(dl.animate.set_value(1.0), run_time=1.0)
        self.at("just 10 times")
        self.play(Indicate(gz, color=YELLOW, scale_factor=1.2), run_time=1.0)
        self.at("Will its picture")
        q = T("?", 130, TEXT, weight=BOLD).move_to([5.2, 2.85, 0])
        pp = T("Pause and predict", 30, YELLOW, weight=BOLD).move_to([4.9, 1.9, 0])
        self.play(FadeIn(q, scale=0.4), FadeIn(pp, shift=UP * 0.1), run_time=0.8)
        self.finish()


class S10Pause(LS):
    def construct(self):
        self.add_ladder()
        self.add_eye()
        self.add_icons(["alga", "rbc"])
        self.add_scope()
        self.add(rule_text())
        dl = ValueTracker(1.0)
        self.add(gauge(dl))
        lm = ValueTracker(0)
        calg, palg = make_card("alga", lm)
        halo = Circle(0.62, stroke_color=GREEN, stroke_width=6).move_to(calg)
        halo.t = 0.0

        def pulse(m, dt):
            m.t += dt
            m.set_stroke(opacity=0.5 + 0.5 * np.sin(3 * m.t))
        halo.add_updater(pulse)
        alab = T("20 µm", 28, TEXT).move_to([-0.2, Y(20) - 0.88, 0])
        q = T("?", 130, TEXT, weight=BOLD).move_to([5.2, 2.85, 0])
        pp = T("Pause and predict", 30, YELLOW, weight=BOLD).move_to([4.9, 1.9, 0])
        q.t = 0.0

        def qpulse(m, dt):
            m.t += dt
            m.set_opacity(0.65 + 0.35 * np.sin(3.5 * m.t))
        q.add_updater(qpulse)
        self.add(calg, palg, halo, alab, q, pp)
        bar = Line([-4.2, -3.74, 0], [6.4, -3.74, 0], color=YELLOW, stroke_width=8)
        self.add(bar)
        self.play(Transform(bar, Line([6.4, -3.74, 0], [6.4, -3.74, 0], color=YELLOW, stroke_width=8)),
                  run_time=self.narration_s - 0.3, rate_func=linear)
        self.finish()


class S11Reveal(LS):
    def construct(self):
        self.add_ladder()
        self.add_eye()
        self.add_icons(["alga", "rbc"])
        self.add_scope()
        self.add(rule_text())
        dl = ValueTracker(1.0)
        self.add(gauge(dl))
        lm_a = ValueTracker(0)
        lm_r = ValueTracker(0)
        calg, palg = make_card("alga", lm_a)
        alab = T("20 µm", 28, TEXT).move_to([-0.2, Y(20) - 0.88, 0])
        q = T("?", 130, TEXT, weight=BOLD).move_to([5.2, 2.85, 0])
        self.add(calg, palg, alab, q)
        self.play(FadeOut(alab), FadeOut(q), lm_a.animate.set_value(1.0), run_time=1.8, rate_func=smooth)
        self.at("Its picture is 200")
        co = callout(["20 µm × 10", "= 200 µm"], 3.0)
        self.play(Write(co), run_time=1.4)
        self.at("twice the eye line")
        self.play(Indicate(self.eye, color=BLUE, scale_factor=1.0), Indicate(calg, color=PAPER, scale_factor=1.3), run_time=1.6)
        self.at("The red blood cell")
        crbc, prbc = make_card("rbc", lm_r)
        self.play(FadeIn(crbc, scale=0.7), FadeIn(prbc), Indicate(self.icons["rbc"], scale_factor=1.4), run_time=0.8)
        self.at("at the same 10 times")
        self.play(lm_r.animate.set_value(1.0), run_time=1.4, rate_func=smooth)
        self.at("still sits below")
        co2 = callout(["7.7 µm × 10", "= 77 µm: not yet"], 1.9, x=4.6)
        self.play(Write(co2), run_time=1.2)
        self.play(Indicate(crbc, color=PAPER, scale_factor=1.25), run_time=0.8)
        self.finish()


class S12School(LS):
    def construct(self):
        self.add_ladder()
        self.add_eye()
        self.add_icons(["alga", "rbc", "bact"])
        self.add_scope()
        self.add(rule_text())
        lm = ValueTracker(0)
        gz = gauge(lm)
        self.add(gz)
        cards, ptrs = {}, {}
        for k in ("alga", "rbc", "bact"):
            cards[k], ptrs[k] = make_card(k, lm)
        self.play(*[FadeIn(cards[k], scale=0.7) for k in cards], *[FadeIn(ptrs[k]) for k in ptrs], run_time=0.8)
        self.at("magnifies 40")
        self.play(lm.animate.set_value(np.log10(40)), run_time=1.2)
        self.at("100 or 400")
        self.play(lm.animate.set_value(2.0), run_time=0.8)
        self.at("400 times")
        self.play(lm.animate.set_value(np.log10(400)), run_time=1.0)
        self.at("At 400 times")
        self.play(Indicate(self.eye, color=BLUE, scale_factor=1.0), run_time=1.0)
        self.at("most cells pass")
        labs = VGroup(*[M(f"{n} {t}", 26, c, weight=BOLD) for n, t, c in (("alga", "8,000 µm", GREEN), ("RBC ", "3,080 µm", RED), ("bact", "800 µm", AMBER))]).arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to([5.2, 2.5, 0])
        self.play(FadeIn(labs, shift=UP * 0.1), *[Indicate(cards[k], color=PAPER, scale_factor=1.25) for k in cards], run_time=1.4)
        self.at("Then you can see")
        view = VGroup(Circle(2.15, stroke_color=TEXT, stroke_width=8, fill_color=PAPER, fill_opacity=0.96)).move_to([0.9, 0.5, 0])
        self.play(FadeOut(labs), *[FadeOut(cards[k]) for k in cards], *[FadeOut(ptrs[k]) for k in ptrs], FadeIn(view, scale=0.6), *[FadeOut(self.icons[k]) for k in self.icons], run_time=0.8)
        content = VGroup()
        rng = np.random.default_rng(4)
        specs = ([("alga", 0.8)] * 4) + ([("rbc", 0.75)] * 6) + ([("bact", 0.85)] * 8)
        pts = []
        while len(pts) < len(specs):
            p = rng.uniform(-1.7, 1.7, 2)
            if np.hypot(*p) < 1.7 and all(np.hypot(*(p - q)) > 0.55 for q in pts):
                pts.append(p)
        for (k, s), p in zip(specs, pts):
            ic = icon(k, s * 1.2).move_to([0.9 + p[0], 0.5 + p[1], 0])
            if k == "bact":
                ic.rotate(rng.uniform(0, np.pi))
            ic.scale(0.001)
            content.add(ic)
        self.add(content)
        self.play(*[c.animate.scale(1000) for c in content], run_time=0.9, lag_ratio=0.05)
        for i, c in enumerate(content):
            wobble(c, 0.05, 0.9 + 0.1 * (i % 5), i)
        self.at("shows them clearly")
        note = VGroup(T("shapes need a clear lens", 26, TEXT), T("and a sample that stands out", 26, TEXT)).arrange(DOWN, buff=0.1)
        note.move_to([0.9, -2.45, 0])
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.8)
        self.add(schem())
        self.finish()


class S13Close(LS):
    def construct(self):
        self.add_ladder(short=True)
        self.add_eye(short=True)
        c = np.array([2.6, 0.2, 0])
        drop = Circle(2.55, stroke_color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.14).move_to(c)
        self.add(rule_text())
        self.add(schem())
        band = Rectangle(width=-2.2 - AX, height=Y(100) - Y(1), stroke_width=0, fill_color=YELLOW, fill_opacity=0.16)
        band.move_to([(AX - 2.2) / 2, (Y(100) + Y(1)) / 2, 0])
        band.set_z_index(-1)
        blab = T("most cells", 28, YELLOW, weight=BOLD).move_to([-3.45, Y(10) - 0.2, 0])
        self.add(band, blab)
        rip = ripples(c, 2.55)
        self.at("So a clear drop")
        self.play(FadeIn(drop, scale=0.8), run_time=0.9)
        self.add(rip)
        # hidden residents
        rng = np.random.default_rng(11)
        res = []
        for k, n, s in (("alga", 4, 1.4), ("bact", 6, 1.6)):
            for _ in range(n):
                a = rng.uniform(0, 2 * np.pi)
                r = rng.uniform(0.2, 1.9)
                ic = icon(k, s).move_to(c + np.array([r * np.cos(a), r * np.sin(a) * 0.9, 0]))
                if k == "bact":
                    ic.rotate(rng.uniform(0, np.pi))
                ic.base = ic.get_center().copy()
                ic.ph = rng.uniform(0, 6)
                res.append(ic)
        para = icon("para", 1.7).move_to(c)
        para.ph = 0.0
        lens = VGroup(Circle(1.35, stroke_color=TEXT, stroke_width=7, fill_color=PAPER, fill_opacity=0.9))
        lens_c = c.copy()
        st = {"t": 0.0, "R": 1.35}

        def lens_pos(t):
            return c + np.array([1.3 * np.sin(0.55 * t), 0.75 * np.sin(0.9 * t + 1.0), 0])

        def drive(m, dt):
            st["t"] += dt
            t = st["t"]
            m.move_to(lens_pos(t))
            m.set_width(2 * st["R"])

        lens.add_updater(drive)
        for ic in res:
            def vis(m, dt):
                t = st["t"]
                m.move_to(m.base + 0.06 * np.array([np.sin(1.3 * t + m.ph), np.cos(1.1 * t + m.ph), 0]))
                d = np.linalg.norm(m.get_center() - lens_pos(t))
                m.set_opacity(1.0 if d < st["R"] - 0.25 else 0.0)
            ic.add_updater(vis)

        def pvis(m, dt):
            t = st["t"]
            m.move_to(c + np.array([1.3 * np.sin(0.4 * t + 2.0), 0.7 * np.cos(0.6 * t), 0]))
            m.set_opacity(1.0 if np.linalg.norm(m.get_center() - lens_pos(t)) < st["R"] - 0.3 else 0.0)
        para.add_updater(pvis)
        self.at("is not always empty")
        lens.move_to(lens_pos(0))
        self.add(*res, para)
        self.play(FadeIn(lens, scale=0.7), run_time=0.8)
        self.at("Most living things")
        self.play(Indicate(band, color=YELLOW, scale_factor=1.0), run_time=1.2)
        self.at("below the eye line")
        self.play(Indicate(self.eye, color=BLUE, scale_factor=1.0), run_time=1.2)
        self.at("where our eyes cannot reach")
        self.wait(1.6)
        self.at("That is why most cells")
        self.play(Indicate(band, color=YELLOW, scale_factor=1.0), run_time=1.0)
        self.at("until microscopes")
        self.play(Indicate(lens, color=TEXT, scale_factor=1.08), run_time=1.2)
        self.finish()


class S14End(EndCard):
    LINE = "Picture size = real size × magnification. Past 100 µm, it can show."
