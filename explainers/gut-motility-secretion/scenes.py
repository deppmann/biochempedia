"""Gut motility: the gut keeps its own time  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = ICC and the slow wave they make (the beat, the timing)
  BLUE   = smooth muscle and its contraction
  GREEN  = enteric nerves, neurons and hormones (what sets strength)
  PURPLE = the ANO1 chloride channel
  RED    = absent or lost (no rhythm, nerve cut or blocked, no response)
  ORANGE = the gut contents
  GREY   = outlines, axes, thresholds, labels
  GOLD   = the open question mark
All slow-wave traces and contraction bars are schematic sketches ("in this sketch"), not recordings.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def smooth(x):
    x = float(np.clip(x, 0, 1))
    return x * x * (3 - 2 * x)


def sw_shape(p):
    """schematic slow wave over one period: quick rise, plateau, fall (relative units, 0..1)."""
    p = p % 1.0
    if p < 0.12:
        return smooth(p / 0.12)
    if p < 0.55:
        return 1 - 0.18 * (p - 0.12) / 0.43
    if p < 0.8:
        return 0.82 * (1 - smooth((p - 0.55) / 0.25))
    return 0.0


def trace(x0, x1, ybase, amp, n, color=YELLOW, stroke=5, phase0=0.0, npts=360):
    xs = np.linspace(x0, x1, npts)
    pts = [[x, ybase + amp * sw_shape(phase0 + (x - x0) / (x1 - x0) * n), 0] for x in xs]
    m = VMobject(color=color, stroke_width=stroke)
    m.set_points_as_corners(pts)
    return m


def wave_x(x0, x1, n, k, p=0.3):
    """x of phase p in wave k."""
    return x0 + (k + p) / n * (x1 - x0)


def axes(x0, x1, ybase, ytop, color=GREY):
    return VGroup(Line([x0 - 0.15, ybase, 0], [x1 + 0.15, ybase, 0], color=color, stroke_width=2.5),
                  Line([x0 - 0.15, ybase, 0], [x0 - 0.15, ytop, 0], color=color, stroke_width=2.5))


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def cross(center, color=RED, s=0.32):
    c = np.array(center, float)
    return VGroup(Line(c + [-s, -s, 0], c + [s, s, 0], color=color, stroke_width=7),
                  Line(c + [-s, s, 0], c + [s, -s, 0], color=color, stroke_width=7))


def icc_cell(color=YELLOW, scale=1.0):
    """a branched pacemaker cell, drawn as a labelled-schematic blob with arms."""
    body = Circle(radius=0.2, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.55)
    arms = VGroup(*[Line(0.2 * np.array([np.cos(a), np.sin(a), 0]), 0.5 * np.array([np.cos(a), np.sin(a), 0]), color=color, stroke_width=3)
                    for a in (0.35, 1.75, 3.5, 5.0)])
    g = VGroup(arms, body)
    g.scale(scale)
    return g


def icc_row(center, xs, scale=1.0, color=YELLOW, link=True):
    cx, cy = center
    cells = [icc_cell(color, scale).move_to([cx + x, cy, 0]) for x in xs]
    links = VGroup(*[Line(cells[i].get_center(), cells[i + 1].get_center(), color=color, stroke_width=2, stroke_opacity=0.55)
                     for i in range(len(cells) - 1)]) if link else VGroup()
    return VGroup(links, *cells)


def bar(cx, cy, w, h, color=BLUE, text=None, size=24, op=0.3):
    r = RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=color, stroke_width=3,
                         fill_color=color, fill_opacity=op).move_to([cx, cy, 0])
    if text is None:
        return r
    t = T(text, size, color).move_to(r)
    return VGroup(r, t)


class S00Title(TitleCard):
    LESSON = "Gut motility, secretion and gut hormones"
    TITLE = "The gut keeps its own time"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    """a gut wall with pacemaker cells present, a flat rhythm trace, a crossed-out channel, and a question."""

    def construct(self):
        # wall: muscle / ICC network / muscle
        top = bar(-3.2, 2.7, 6.4, 1.0, BLUE, "smooth muscle", 26)
        bot = bar(-3.2, -0.3, 6.4, 1.0, BLUE, "smooth muscle", 26)
        net = icc_row((-3.2, 1.2), [-2.55, -0.85, 0.85, 2.55], 1.3)
        wall = VGroup(top, bot, net)
        lbl = T("pacemaker cells: present", 28, YELLOW).move_to([-3.2, -1.3, 0])

        chan = chip("one chloride channel", PURPLE, size=28).move_to([-2.9, -2.8, 0])
        x = cross(chan.get_left() + [-0.5, 0, 0], RED, 0.32)
        # rhythm panel
        ax = axes(1.6, 6.3, 0.5, 3.3)
        head = T("slow waves", 28, GREY).move_to([4.0, 3.5, 0])
        flat = Line([1.6, 0.5, 0], [6.3, 0.5, 0], color=RED, stroke_width=6)
        norhy = T("no waves", 32, RED, weight=BOLD).move_to([4.0, 1.9, 0])
        q = T("?", 140, GOLD, weight=BOLD).move_to([4.3, -1.6, 0])
        what = T("what does it do?", 28, GOLD).move_to([4.3, -2.9, 0])

        self.at("without one chloride")
        self.play(FadeIn(chan, shift=UP * 0.2), run_time=0.6)
        self.play(Create(x), run_time=0.4)
        self.at("pacemaker cells")
        self.play(FadeIn(wall, lag_ratio=0.2), run_time=1.0)
        self.play(FadeIn(lbl), run_time=0.4)
        self.at("no electrical")
        self.play(FadeIn(ax), FadeIn(head), Create(flat), run_time=0.7)
        self.play(FadeIn(norhy), run_time=0.4)
        self.at("What does that channel do")
        self.play(FadeIn(q, scale=0.5), FadeIn(what), run_time=0.6)
        self.at("keeps its own time")
        self.play(Indicate(net, color=YELLOW, scale_factor=1.08), run_time=0.9)
        self.at("branched cells")
        self.play(*[Indicate(m, color=YELLOW, scale_factor=1.35) for m in net[1:]], run_time=0.9)
        newlbl = T("interstitial cells of Cajal (ICC)", 28, YELLOW).move_to([-3.2, -1.3, 0])
        self.at("interstitial cells")
        self.play(Transform(lbl, newlbl), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Slowwave(SpokenScene):
    """slow wave trace; isolated ICC beat, isolated muscle does not; in a pair the wave shrinks passively."""

    def construct(self):
        X0, X1, N = -2.4, 5.8, 3
        # --- first: one muscle-cell recording, big, centred -------------------------------------
        yb0, amp0 = -1.3, 2.6
        ax0 = axes(X0, X1, yb0, yb0 + 3.0)
        tr0 = trace(X0, X1, yb0, amp0, N)
        chip0 = chip("smooth muscle cell", BLUE, size=26).move_to([-4.6, yb0 + 1.2, 0])
        xl0 = T("1 minute, in this sketch", 24, GREY).move_to([(X0 + X1) / 2, yb0 - 0.55, 0])
        yl0 = T("membrane potential, relative units", 22, GREY).move_to([-0.7, yb0 + 3.35, 0])
        self.at("Record from")
        self.play(FadeIn(chip0), FadeIn(ax0), FadeIn(xl0), FadeIn(yl0), run_time=0.7)
        self.at("slow waves")
        self.play(Create(tr0, rate_func=linear), run_time=3.0)
        lasts = T("each lasts seconds", 24, YELLOW).move_to([wave_x(X0, X1, N, 3, 0.34), yb0 + amp0 + 0.5, 0])
        self.at("last seconds")
        self.play(FadeIn(lasts), run_time=0.4)
        rate = T("about 3 per minute", 28, YELLOW).move_to([0.2, 3.3, 0])
        rate2 = T("human stomach", 24, GREY).move_to([0.2, 2.85, 0])
        self.at("human stomach")
        self.play(FadeOut(lasts), FadeIn(rate), run_time=0.5)
        self.at("pacemaker cells")
        self.play(FadeIn(rate2), run_time=0.5)

        # --- isolated cells ---------------------------------------------------------------------
        yA, yB, ampR = 1.1, -2.0, 1.15
        axA = axes(X0, X1, yA, yA + 1.7)
        trA = trace(X0, X1, yA, ampR, N)
        chipA = chip("ICC", YELLOW, size=26).move_to([-4.6, yA + 0.6, 0])
        axB = axes(X0, X1, yB, yB + 1.7)
        trB_flat = trace(X0, X1, yB, 0.0, N, color=BLUE)
        chipB = chip("smooth muscle", BLUE, size=26).move_to([-4.6, yB + 0.6, 0])
        isoA = T("isolated ICC: rhythmic", 24, YELLOW).move_to([4.1, yA + 2.05, 0])
        isoB = T("isolated muscle cell: typically no rhythm", 24, BLUE).move_to([2.6, yB + 1.3, 0])
        self.at("Isolated")
        self.play(FadeOut(rate), FadeOut(rate2), FadeOut(xl0), FadeOut(yl0),
                  ReplacementTransform(tr0, trB_flat), ReplacementTransform(ax0, axB), ReplacementTransform(chip0, chipB),
                  run_time=1.0)
        self.play(FadeIn(axA), FadeIn(chipA), Create(trA, rate_func=linear), run_time=2.0)
        self.play(FadeIn(isoA), FadeIn(isoB), run_time=0.5)

        # --- paired recording: passive spread, shrinking ---------------------------------------
        trB_small = trace(X0, X1, yB, 0.6, N, color=BLUE)
        self.at("In paired recordings")
        self.play(FadeOut(isoA), FadeOut(isoB), run_time=0.4)
        self.at("larger in")
        self.play(Indicate(trA, color=YELLOW, scale_factor=1.0), run_time=0.8)
        arrs = VGroup(*[arr([wave_x(X0, X1, N, k, 0.3) + 0.2, yA - 0.2, 0], [wave_x(X0, X1, N, k, 0.3) + 0.2, yB + 0.95, 0], YELLOW, 4, 0.2)
                        for k in (0, 1, 2, 3)])
        shr = T("passive spread,\nshrinking", 24, GREY).move_to([-4.6, -0.45, 0])
        self.at("They reached the muscle")
        self.play(LaggedStart(*[GrowArrow(a) for a in arrs], lag_ratio=0.15), Transform(trB_flat, trB_small), run_time=1.6)
        self.at("shrinking as they spread")
        self.play(FadeIn(shr), run_time=0.5)
        nore = T("smooth muscle cannot regenerate them", 26, RED).move_to([1.7, yB - 0.65, 0])
        self.at("cannot regenerate")
        self.play(FadeIn(nore), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Metronome(SpokenScene):
    """the beat fixes timing; the plateau must pass threshold for contraction; neurons and hormones lift it."""

    def construct(self):
        X0, X1, N = -3.2, 5.8, 4
        yb, amp = 0.55, 1.0
        thr_y = yb + 1.35
        yc = -2.8   # contraction baseline
        ax = axes(X0, X1, yb - 0.1, yb + 2.9)
        tr = trace(X0, X1, yb, amp, N)
        sw = T("slow wave", 28, YELLOW).move_to([-4.9, yb + 0.45, 0])
        notap = T("not an action\npotential", 22, GREY).move_to([-4.9, yb - 0.25, 0])
        note = T("relative units, in this sketch", 22, GREY).move_to([1.6, 3.45, 0])
        # contraction row
        cax = Line([X0 - 0.15, yc, 0], [X1 + 0.15, yc, 0], color=GREY, stroke_width=2.5)
        cl = T("contraction", 28, BLUE).move_to([-4.9, yc + 0.7, 0])
        # beat marks
        xs = [wave_x(X0, X1, N, k, 0.3) for k in range(N)]
        ticks = VGroup(*[DashedLine([x, yb - 0.1, 0], [x, yc, 0], color=YELLOW, stroke_width=3, dash_length=0.12).set_opacity(0.7) for x in xs])
        when = T("when", 28, YELLOW, weight=BOLD).move_to([-4.9, -0.7, 0])
        thr = DashedLine([X0 - 0.15, thr_y, 0], [X1 + 0.15, thr_y, 0], color=GREY, stroke_width=3, dash_length=0.15)
        thr_t = T("threshold for\ncalcium entry", 22, GREY).move_to([-4.9, thr_y + 0.25, 0])

        self.play(FadeIn(ax), FadeIn(sw), FadeIn(note), FadeIn(cax), FadeIn(cl), run_time=0.4)
        self.at("not an action potential")
        self.play(FadeIn(notap), Create(tr, rate_func=linear), run_time=2.2)
        self.at("sets when")
        self.play(Create(ticks, lag_ratio=0.2), FadeIn(when), run_time=1.2)
        self.at("past threshold")
        self.play(Create(thr), FadeIn(thr_t), run_time=0.7)

        # metronome and pianist tags
        met = T("metronome: the beat", 26, YELLOW).move_to([-1.2, -3.3, 0])
        pia = T("pianist: how loud", 26, GREEN).move_to([3.7, -3.3, 0])
        self.at("metronome")
        self.play(FadeIn(met), Indicate(ticks, color=YELLOW, scale_factor=1.0), run_time=0.8)
        self.at("pianist")
        self.play(FadeIn(pia), run_time=0.5)

        # neurons and hormones lift the plateau over threshold; bars appear at the same beats
        nh = T("neurons and\nhormones", 26, GREEN, weight=BOLD).move_to([-4.9, 3.12, 0])
        nh_arr = arr([-4.0, 3.0, 0], [-2.8, 2.55, 0], GREEN, 4, 0.2)
        bars = VGroup(*[Rectangle(width=0.7, height=1.6, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.55)
                        .move_to([x, yc + 0.8, 0]) for x in xs])
        tr_hi = trace(X0, X1, yb + 0.8, amp, N)   # same wave height, plateau lifted over the threshold
        self.at("and inhibitory neurons")
        self.play(FadeIn(nh, shift=UP * 0.2), GrowArrow(nh_arr), run_time=0.5)
        self.at("how strongly")
        self.play(Transform(tr, tr_hi), run_time=1.0)
        self.play(*[GrowFromEdge(b, DOWN) for b in bars], run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Mice(SpokenScene):
    """three mouse panels: wild-type, Kit-mutant (few ICC), ANO1-null (ICC look normal): both lack slow waves."""

    PW = 4.0

    def panel(self, cx, title, ncells, wave):
        yTop, yBot = 3.45, -1.9
        rect = RoundedRectangle(corner_radius=0.15, width=self.PW, height=yTop - yBot, stroke_color=GREY, stroke_width=2.5) \
            .move_to([cx, (yTop + yBot) / 2, 0])
        head = T(title, 24, TEXT, weight=BOLD).move_to([cx, 3.0, 0])
        offs = [-1.35, -0.45, 0.45, 1.35] if ncells == 4 else [0.0]
        row = icc_row((cx, 2.2), offs, 0.95, link=(ncells == 4))
        tx0, tx1 = cx - 1.7, cx + 1.7
        ax = axes(tx0, tx1, -0.95, 0.9)
        tr = trace(tx0, tx1, -0.95, 1.6, 3, YELLOW) if wave else Line([tx0, -0.95, 0], [tx1, -0.95, 0], color=RED, stroke_width=6)
        return rect, head, row, ax, tr

    def construct(self):
        cxs = [-4.45, 0.0, 4.45]
        # panel 1: wild type; panel 2: Kit-mutant; panel 3: ANO1-null. (revealed in narration order 2, 1, 3)
        p1 = self.panel(cxs[0], "wild-type siblings", 4, True)
        p2 = self.panel(cxs[1], "Kit-mutant mice", 1, False)
        p3 = self.panel(cxs[2], "A N O 1 null mice".replace("A N O 1", "ANO1"), 4, False)
        s1 = T("ICC present", 22, YELLOW).move_to([cxs[0], 1.5, 0])
        s2 = T("few myenteric ICC", 22, YELLOW).move_to([cxs[1], 1.5, 0])
        s3 = T("ICC networks look normal", 22, YELLOW).move_to([cxs[2], 1.5, 0])
        r1 = T("slow waves", 24, YELLOW).move_to([cxs[0], -1.5, 0])
        r2 = T("no slow waves", 24, RED).move_to([cxs[1], -1.5, 0])
        r3 = T("no slow waves", 24, RED).move_to([cxs[2], -1.5, 0])
        ano = chip("ANO1 channel", PURPLE, size=24).move_to([cxs[2] + 0.2, 0.75, 0])
        anox = cross(ano.get_left() + [-0.4, 0, 0], RED, 0.25)

        self.at("Small intestinal muscle")
        self.play(FadeIn(p2[0]), FadeIn(p2[1]), run_time=0.5)
        self.play(FadeIn(p2[2]), FadeIn(s2), FadeIn(p2[3]), run_time=0.7)
        self.at("lacked the slow waves")
        self.play(Create(p2[4]), FadeIn(r2), run_time=0.7)
        self.at("wild type")
        self.play(FadeIn(p1[0]), FadeIn(p1[1]), FadeIn(p1[2]), FadeIn(s1), FadeIn(p1[3]), FadeIn(r1), run_time=0.4)
        self.play(Create(p1[4], rate_func=linear), run_time=1.0)
        self.at("Mice lacking")
        self.play(FadeIn(p3[0]), FadeIn(p3[1]), FadeIn(p3[3]), run_time=0.5)
        self.play(FadeIn(ano), Create(anox), run_time=0.7)
        self.at("failed to develop")
        self.play(Create(p3[4]), FadeIn(r3), run_time=0.7)
        self.at("networks looked normal")
        self.play(FadeIn(p3[2]), FadeIn(s3), run_time=0.8)

        concl = T("a calcium-activated chloride current is necessary for the rhythm,", 28, PURPLE).move_to([0, -2.55, 0])
        concl2 = T("separately from building the network", 28, PURPLE).move_to([0, -3.05, 0])
        self.at("So a calcium")
        self.play(FadeIn(concl), run_time=0.6)
        self.play(FadeIn(concl2), run_time=0.5)
        h1 = T("not shown: that ANO1 is the whole pacemaker", 28, GREY).move_to([0, -2.55, 0])
        h2 = T("neonatal mice, not adults or any human disorder", 28, GREY).move_to([0, -3.1, 0])
        self.at("does not show")
        self.play(FadeOut(concl), FadeOut(concl2), FadeIn(h1), run_time=0.7)
        self.at("neonatal mice")
        self.play(FadeIn(h2), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Wall(SpokenScene):
    """the myenteric plexus between the muscle layers, then the oral-contraction / anal-relaxation reflex."""

    def construct(self):
        # --- wall layers --------------------------------------------------------------------
        circ = bar(0, 1.75, 9.0, 1.3, BLUE, "circular muscle layer", 30)
        lon = bar(0, -0.85, 9.0, 1.3, BLUE, "longitudinal muscle layer", 30)
        head = T("enteric nervous system: neurons in the gut wall", 32, GREEN).move_to([0, 3.15, 0])
        mv = T("mainly controls movement", 28, GREEN).move_to([0, -2.4, 0])
        plex = bar(0, 0.45, 9.0, 1.0, GREEN, None, op=0.3)
        nodes = VGroup()
        for xs_ in ([-4.0, -3.4, -2.8], [2.8, 3.4, 4.0]):
            pts = [[x, 0.45 + dy, 0] for x, dy in zip(xs_, (0.14, -0.14, 0.14))]
            nodes.add(*[Line(pts[i], pts[i + 1], color=GREEN, stroke_width=3) for i in range(2)])
            nodes.add(*[Dot(p, radius=0.1, color=GREEN) for p in pts])
        plabel = T("myenteric plexus", 30, GREEN).move_to([0, 0.45, 0])
        self.at("nervous system")
        self.play(FadeIn(head), run_time=0.6)
        self.at("network of neurons")
        self.play(FadeIn(plex), FadeIn(nodes), run_time=0.7)
        self.at("myenteric plexus")
        self.play(FadeIn(plabel), run_time=0.4)
        self.at("circular and longitudinal")
        self.play(FadeIn(circ, shift=DOWN * 0.2), FadeIn(lon, shift=UP * 0.2), run_time=0.7)
        self.at("mainly controls movement")
        self.play(FadeIn(mv), Indicate(plex, color=GREEN, scale_factor=1.03), run_time=0.9)

        # --- the reflex in a loop of gut: three blocks ---------------------------------------------
        cxs = [-4.2, 0.0, 4.2]
        H0 = 3.0
        YC = 0.2

        def blk(cx, h, color=GREY, op=0.25):
            return RoundedRectangle(corner_radius=0.12, width=3.9, height=h, stroke_color=color, stroke_width=3,
                                    fill_color=color, fill_opacity=op).move_to([cx, YC, 0])

        oral, mid, anal = blk(cxs[0], H0), blk(cxs[1], H0), blk(cxs[2], H0)
        l_oral = T("oral side", 28, GREY).move_to([cxs[0], 2.35, 0])
        l_anal = T("anal side", 28, GREY).move_to([cxs[2], 2.35, 0])
        ball = Circle(radius=0.6, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.8).move_to([cxs[1], YC + 0.3, 0])
        l_ball = T("contents", 26, ORANGE).move_to([cxs[1], YC - 0.75, 0])
        dog = T("loop of small intestine, anesthetized dog (1899)", 26, GREY).move_to([0, 3.2, 0])
        self.at("and Starling")
        self.play(FadeOut(VGroup(circ, plex, plabel, nodes, lon, head, mv)), run_time=0.6)
        self.play(FadeIn(oral), FadeIn(mid), FadeIn(anal), FadeIn(l_oral), FadeIn(l_anal), FadeIn(dog), run_time=0.8)
        self.play(FadeIn(ball), FadeIn(l_ball), run_time=0.5)

        oral2 = blk(cxs[0], 1.2, BLUE, 0.55)
        anal2 = blk(cxs[2], 4.4, GREY, 0.12)
        mid2 = blk(cxs[1], 3.8, GREY, 0.25)
        dist = T("distension", 28, ORANGE).move_to([cxs[1], 2.5, 0])
        self.at("Distension of the wall")
        self.play(Transform(mid, mid2), FadeIn(dist), run_time=0.7)
        t_oral = T("contraction", 28, BLUE).move_to([cxs[0], 1.1, 0])
        t_anal = T("relaxation", 28, GREY).move_to([cxs[2], 2.8, 0])
        self.at("contraction on the oral")
        self.play(Transform(oral, oral2), FadeIn(t_oral), FadeOut(l_oral), run_time=0.9)
        self.at("relaxation on the anal")
        self.play(Transform(anal, anal2), FadeIn(t_anal), FadeOut(l_anal), run_time=0.9)
        drive = arr([-1.6, -2.1, 0], [2.0, -2.1, 0], ORANGE, 6)
        self.at("driving contents anally")
        self.play(ball.animate.move_to([cxs[2], YC + 0.3, 0]), l_ball.animate.move_to([cxs[2], YC - 0.75, 0]),
                  FadeOut(dist), Transform(mid, blk(cxs[1], H0)), GrowArrow(drive), run_time=1.3)

        # --- the two tests ---------------------------------------------------------------------
        cut = chip("extrinsic nerves cut", GREEN, size=26).move_to([-1.4, -3.15, 0])
        cutx = cross(cut.get_left() + [-0.45, 0, 0], RED, 0.28)
        kept = T("response persisted", 28, GREEN, weight=BOLD).move_to([3.6, -3.15, 0])
        self.at("persisted after the extrinsic")
        self.play(FadeOut(drive), FadeIn(cut), Create(cutx), run_time=0.6)
        self.play(FadeIn(kept), run_time=0.4)
        blocked = chip("conduction in the wall blocked", GREEN, size=26).move_to([-1.0, -3.15, 0])
        blx = cross(blocked.get_left() + [-0.45, 0, 0], RED, 0.28)
        lost = T("response lost", 28, RED, weight=BOLD).move_to([4.3, -3.15, 0])
        self.at("lost when conduction")
        self.play(FadeOut(cut), FadeOut(cutx), FadeOut(kept),
                  Transform(oral, blk(cxs[0], H0)), Transform(anal, blk(cxs[2], H0)),
                  Transform(mid, blk(cxs[1], 3.8, GREY, 0.25)), FadeIn(dist),
                  FadeOut(t_oral), FadeOut(t_anal), FadeIn(l_oral), FadeIn(l_anal),
                  ball.animate.move_to([cxs[1], YC + 0.3, 0]), l_ball.animate.move_to([cxs[1], YC - 0.75, 0]),
                  run_time=0.8)
        self.play(FadeIn(blocked), Create(blx), run_time=0.5)
        self.at("was blocked")
        self.play(FadeIn(lost), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """fixed beat marks on top, contraction bars below that change height while the beat stays put."""

    def construct(self):
        X0, X1, N = -2.4, 5.6, 5
        xs = [X0 + (X1 - X0) * (k + 0.5) / N for k in range(N)]
        yt = 2.7     # beat row
        yb = -1.2    # bar baseline
        hA = [1.4, 1.4, 1.4, 1.4, 1.4]
        hB = [0.6, 2.3, 1.1, 2.0, 0.8]
        hC = [2.2, 0.7, 1.8, 0.6, 1.5]
        lab1 = T("when", 36, YELLOW, weight=BOLD).move_to([-4.9, yt + 0.15, 0])
        sub1 = T("ICC slow waves", 24, YELLOW).move_to([-4.9, yt - 0.4, 0])
        lab2 = T("how strongly", 36, GREEN, weight=BOLD).move_to([-4.9, 0.5, 0])
        sub2 = T("neurons and\nhormones", 24, GREEN).move_to([-4.9, -0.2, 0])
        beat = Line([X0 - 0.2, yt, 0], [X1 + 0.2, yt, 0], color=GREY, stroke_width=2.5)
        ticks = [Line([x, yt - 0.28, 0], [x, yt + 0.28, 0], color=YELLOW, stroke_width=7) for x in xs]
        base = Line([X0 - 0.2, yb, 0], [X1 + 0.2, yb, 0], color=GREY, stroke_width=2.5)
        guides = VGroup(*[DashedLine([x, yt - 0.3, 0], [x, yb, 0], color=YELLOW, stroke_width=2.5, dash_length=0.12).set_opacity(0.5) for x in xs])

        def bars(hs):
            return VGroup(*[Rectangle(width=0.8, height=h, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.55)
                            .move_to([x, yb + h / 2, 0]) for x, h in zip(xs, hs)])

        bA = bars(hA)
        skn = T("schematic, relative units", 22, GREY).move_to([1.6, yb - 0.4, 0])
        rule = T("Slow waves mainly set the timing.", 38, font=TITLE_FONT)
        fit(rule, max_w=12.0)
        rule.move_to([0, -2.8, 0])

        self.at("splits the work")
        self.play(FadeIn(lab1), FadeIn(sub1), FadeIn(lab2), FadeIn(sub2), FadeIn(beat), FadeIn(base), FadeIn(skn), run_time=0.8)
        self.at("keep the beat")
        self.play(LaggedStart(*[GrowFromCenter(t) for t in ticks], lag_ratio=0.25), run_time=1.6)
        self.at("sets when the muscle")
        self.play(Create(guides), run_time=0.6)
        self.play(*[GrowFromEdge(b, DOWN) for b in bA], run_time=0.9)
        self.at("Neurons and hormones set")
        self.play(Indicate(sub2, color=GREEN, scale_factor=1.1), run_time=0.7)
        self.play(Transform(bA, bars(hB)), run_time=1.1)
        self.play(Transform(bA, bars(hC)), run_time=1.0)
        self.at("Keep this rule")
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "Slow waves mainly set the timing."
