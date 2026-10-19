"""Patch clamp: watching one channel open and shut  (Biochemistrypedia methods film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the glass pipette and the amplifier (the apparatus)
  GREY   = membranes, cell outlines, structure, de-emphasised text
  PURPLE = ion channels (pores in the membrane)
  YELLOW = the current (arrows of current, the recorded trace, the unitary current i)
  GREEN  = a good seal, a control, the open probability
  RED    = leak, noise, the pitfall
  ORANGE = a solution you add or put in the pipette (agonist, ATP, serotonin, the pipette recipe)
  TEAL   = bath / chloride the cell owns
  GOLD   = dates and the closing rule
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def lab(text, size=24, color=GREY, **kw):
    return T(text, size, color, **kw)


def lines(*texts, size=24, color=TEXT, buff=0.14, align=LEFT, colors=None):
    g = VGroup(*[T(t, size, (colors[i] if colors else color)) for i, t in enumerate(texts)])
    return g.arrange(DOWN, aligned_edge=align, buff=buff)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def poly(pts, color=YELLOW, w=5):
    m = VMobject()
    m.set_points_as_corners([np.array([p[0], p[1], 0.0]) for p in pts])
    m.set_stroke(color, w)
    return m


def membrane(x0, x1, y, holes=(), h=0.3, hole_w=0.8, color=GREY):
    """Membrane bar with gaps (for channels) at the x positions in `holes`."""
    edges = [x0]
    segs = []
    for hx in sorted(holes):
        segs.append((edges[-1], hx - hole_w / 2))
        edges.append(hx + hole_w / 2)
    segs.append((edges[-1], x1))
    g = VGroup()
    for a, b in segs:
        if b - a > 0.02:
            g.add(RoundedRectangle(corner_radius=min(0.08, h / 2), width=b - a, height=h, stroke_color=color,
                                   stroke_width=2.5, fill_color=color, fill_opacity=0.35).move_to([(a + b) / 2, y, 0]))
    return g


class Chan(VGroup):
    """A channel: two posts through the membrane and a plug. Plug visible = closed, hidden = open."""

    def __init__(self, x, y, scale=1.0, closed=True):
        pw, h, gap = 0.3 * scale, 0.5 * scale, 0.2 * scale
        l = Rectangle(width=pw, height=h, stroke_color=PURPLE, stroke_width=2.5, fill_color=PURPLE, fill_opacity=0.55)
        r = l.copy()
        l.move_to([x - (gap + pw) / 2, y, 0])
        r.move_to([x + (gap + pw) / 2, y, 0])
        self.plug = Rectangle(width=gap + 0.02, height=h * 0.7, stroke_width=0, fill_color=PURPLE, fill_opacity=0.95)
        self.plug.move_to([x, y, 0])
        self.plug.set_opacity(1.0 if closed else 0.0)
        self.w = 2 * pw + gap
        self.cx, self.cy = x, y
        super().__init__(l, r, self.plug)

    def open(self):
        return self.plug.animate.set_opacity(0.0)

    def close(self):
        return self.plug.animate.set_opacity(1.0)


def pipette(tip, h=3.4, tip_w=1.1, top_w=2.2, solution=None):
    """Glass pipette as a trapezoid with an open tip. `solution` is a colour for its fill."""
    tx, ty = tip
    L = np.array([tx - tip_w / 2, ty, 0]); R = np.array([tx + tip_w / 2, ty, 0])
    UL = np.array([tx - top_w / 2, ty + h, 0]); UR = np.array([tx + top_w / 2, ty + h, 0])
    fill = Polygon(L, R, UR, UL, stroke_width=0, fill_color=solution or BLUE, fill_opacity=0.33 if solution else 0.10)
    wl = Line(UL, L, color=BLUE, stroke_width=5)
    wr = Line(UR, R, color=BLUE, stroke_width=5)
    g = VGroup(fill, wl, wr)
    g.tip = np.array([tx, ty, 0.0])
    return g


def cell_blob(c, r=0.9, color=GREY):
    return Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.10).move_to([c[0], c[1], 0])


def cur_arrows(x, y0, y1, n=1, color=YELLOW, spread=0.22):
    return VGroup(*[arr([x + (i - (n - 1) / 2) * spread, y0, 0], [x + (i - (n - 1) / 2) * spread, y1, 0], color, w=4, tip=0.16)
                    for i in range(n)])


def tag(text, color=GREY, size=24):
    return T(text, size, color)


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Methods library"
    TITLE = "Watching One Channel Open and Shut"


# ---------------------------------------------------------------------------------------------
class S01Problem(SpokenScene):
    """whole-cell current = sum of many pores; one pore's step hides in noise; one channel is inferred, never seen."""

    def construct(self):
        rng = np.random.RandomState(11)
        n = 11
        xs = np.linspace(-5.0, 5.0, n)
        my = 2.75
        mem = membrane(-6.3, 6.3, my, holes=xs, h=0.3, hole_w=0.46)
        chans = [Chan(x, my, 0.6, closed=True) for x in xs]
        mem_lbl = lab("many small pores", 26, PURPLE).move_to([0, 2.05, 0])

        # whole-cell sum trace (inward current drawn downwards)
        N = 140
        state = rng.rand(n) < 0.35
        counts = []
        for _ in range(N):
            flip = rng.rand(n) < 0.12
            state = np.where(flip, ~state, state)
            counts.append(int(state.sum()))
        x0, x1, y0 = -6.0, 6.0, 1.0
        pts = []
        for i, c in enumerate(counts):
            xa = x0 + (x1 - x0) * i / N
            xb = x0 + (x1 - x0) * (i + 1) / N
            pts += [[xa, y0 - 0.3 * c], [xb, y0 - 0.3 * c]]
        total = poly(pts, YELLOW, 5)
        base = DashedLine([x0, y0, 0], [x1, y0, 0], color=GREY, stroke_width=2)
        total_lbl = lab("current across the whole cell", 26, YELLOW).move_to([0, -2.1, 0])

        self.at("Membrane current")
        self.play(FadeIn(mem), *[FadeIn(c) for c in chans], FadeIn(mem_lbl), run_time=0.7)
        self.play(FadeIn(base), Create(total, run_time=2.0, rate_func=linear), FadeIn(total_lbl))
        # pores flicker
        self.at("opening and closing")
        flick = []
        for k in (1, 3, 4, 6, 8, 9):
            flick.append(chans[k].open())
        self.play(*flick, run_time=0.4)
        flick = [chans[k].close() for k in (1, 4, 8)] + [chans[k].open() for k in (0, 5, 10)]
        self.play(*flick, run_time=0.4)

        # one pore's step vs noise
        self.at("The steps of one pore")
        noise_y = -0.5
        tn = np.linspace(x0, x1, 260)
        nz = rng.randn(260) * 0.16
        step = np.where((tn > 1.2) & (tn < 3.0), -0.2, 0.0)
        nlin = poly([[a, noise_y + b + c] for a, b, c in zip(tn, nz, step)], RED, 3)
        nbase = DashedLine([x0, noise_y, 0], [x1, noise_y, 0], color=GREY, stroke_width=2)
        self.play(FadeOut(total), FadeOut(base), FadeOut(total_lbl), run_time=0.4)
        self.play(FadeIn(nbase), Create(nlin, run_time=1.2, rate_func=linear))
        noise_lbl = lab("noise of a large membrane", 26, RED).move_to([-3.0, -1.5, 0])
        box = DashedVMobject(Rectangle(width=1.8, height=0.9, stroke_color=YELLOW, stroke_width=3).move_to([2.1, noise_y - 0.1, 0]))
        q = T("?", 40, YELLOW, weight=BOLD).next_to(box, UP, buff=0.08)
        step_lbl = lab("one pore's step", 26, YELLOW).move_to([2.1, -1.5, 0])
        self.play(FadeIn(noise_lbl), Create(box), FadeIn(q), FadeIn(step_lbl), run_time=0.7)

        self.at("One open channel")
        self.play(FadeOut(noise_lbl), FadeOut(step_lbl), run_time=0.3)
        v = M("a few pA", 40, YELLOW).move_to([-2.2, -2.15, 0])
        v2 = lab("a few trillionths of an amp", 26, TEXT).move_to([2.6, -2.15, 0])
        v3 = lab("current of one open channel", 24, GREY).move_to([0, -3.0, 0])
        self.play(FadeIn(v, shift=UP * 0.15), run_time=0.4)
        self.at("a few trillionths")
        self.play(FadeIn(v2, shift=UP * 0.15), FadeIn(v3), run_time=0.5)

        self.at("Until single")
        keep = 5
        clear = VGroup(nlin, nbase, box, q, v, v2, v3)
        self.play(FadeOut(clear), *[c.animate.set_opacity(0.25) for k, c in enumerate(chans) if k != keep],
                  run_time=0.6)
        thousands = chip("thousands acting at once", PURPLE, 32).move_to([-3.0, -0.7, 0])
        one = chip("what one channel does", YELLOW, 32).move_to([3.6, -0.7, 0])
        qq = T("?", 56, YELLOW, weight=BOLD).next_to(one, DOWN, buff=0.2)
        inferred = lab("inferred, not seen", 28, GREY).move_to([0.3, -1.5, 0])
        a = arr(thousands.get_right() + [0.1, 0, 0], one.get_left() + [-0.1, 0, 0], GREY)
        self.at("had to be inferred")
        self.play(FadeIn(thousands, shift=RIGHT * 0.2), run_time=0.5)
        self.play(GrowArrow(a), FadeIn(one), FadeIn(qq), FadeIn(inferred), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def pow10(a, b, size=36, color=GREEN):
    """'10^a – 10^b Ω' with raised exponents, built from separate pieces (Menlo has no good superscripts)."""
    small = int(size * 0.58)
    parts = []
    x = M("10", size, color)
    ea = M(str(a), small, color).next_to(x, UR, buff=0.02).shift(DOWN * 0.12)
    dash = M("–", size, color).next_to(ea, RIGHT, buff=0.12).set_y(x.get_y())
    y = M("10", size, color).next_to(dash, RIGHT, buff=0.12).set_y(x.get_y())
    eb = M(str(b), small, color).next_to(y, UR, buff=0.02).shift(DOWN * 0.12)
    om = M("Ω", size, color).next_to(eb, RIGHT, buff=0.18).set_y(x.get_y())
    return VGroup(x, ea, dash, y, eb, om)


class S02Seal(SpokenScene):
    """pipette on membrane; seal resistance RISES on touch (leak, noise), jumps on suction (giga-seal, clean trace)."""

    def construct(self):
        my = -2.6
        px = -1.6
        tip0 = my + 0.15 + 0.22          # tip just above the membrane: leaky gap
        LX = -4.7                         # left label column
        mem = membrane(-6.3, 6.3, my, holes=[px], h=0.3, hole_w=0.8)
        ch = Chan(px, my, 1.0, closed=False)
        memlbl = lab("cell membrane", 24, GREY).move_to([-4.9, my - 0.55, 0])
        pip = pipette([px, tip0 + 3.0], h=5.0, tip_w=1.2, top_w=2.2)
        pip_lbl = lab("glass pipette", 26, BLUE).move_to([LX, 2.3, 0])

        self.at("A glass pipette")
        self.play(FadeIn(mem), FadeIn(ch), FadeIn(memlbl), FadeIn(pip), FadeIn(pip_lbl), run_time=0.5)
        self.at("a tip about")
        self.play(pip.animate.shift(DOWN * 3.0), FadeOut(pip_lbl), run_time=0.8)
        tipline = DoubleArrow([px - 0.62, tip0 + 0.5, 0], [px + 0.62, tip0 + 0.5, 0], buff=0, color=YELLOW,
                              stroke_width=3, tip_length=0.12)
        tip_lbl = lines("tip about", "1 µm across", size=24, color=YELLOW, buff=0.08, align=RIGHT).move_to([LX, -1.6, 0])
        self.play(Create(tipline), FadeIn(tip_lbl), run_time=0.4)

        self.at("slight suction")
        suc = arr([px, 0.2, 0], [px, 1.5, 0], BLUE, w=6, tip=0.25)
        suc_lbl = lab("slight suction", 24, BLUE).move_to([LX, 0.9, 0])
        self.play(GrowArrow(suc), FadeIn(suc_lbl), run_time=0.5)

        # --- what a seal must do (the target, not yet a measurement)
        self.at("The seal must resist")
        read_title = lab("seal resistance", 24, GREY).move_to([3.6, 3.15, 0])
        need = M("needed: above 1 GΩ", 28, GREEN).move_to([3.6, 2.5, 0])
        self.play(FadeOut(tipline), FadeOut(tip_lbl), FadeIn(read_title), FadeIn(need, shift=UP * 0.1), run_time=0.5)
        self.at("so current flows through the patch")
        flow = cur_arrows(px, my - 0.9, my + 1.4, n=2, spread=0.3)
        flow_lbl = lab("through the patch", 24, YELLOW).move_to([LX, -0.3, 0])
        self.play(*[GrowArrow(a) for a in flow], FadeIn(flow_lbl), run_time=0.6)
        self.at("and not around the rim")
        cross = VGroup(*[T("✕", 34, RED, weight=BOLD).move_to([px + s * 1.15, my + 0.6, 0]) for s in (-1, 1)])
        rim_lbl = lab("not around the rim", 24, RED).move_to([2.6, -1.5, 0])
        self.play(FadeIn(cross), FadeIn(rim_lbl), run_time=0.4)

        # --- early seals: the reading appears (rises from nothing) and leak is large
        self.at("earliest seals were")
        self.play(FadeOut(VGroup(suc, suc_lbl, flow, flow_lbl, cross, rim_lbl)), pip.animate.shift(DOWN * 0.12), run_time=0.5)
        gap_y = my + 0.27
        leak = VGroup(*[arr([px + s * 2.2, gap_y, 0], [px + s * 0.75, gap_y, 0], RED, w=6, tip=0.2) for s in (-1, 1)])
        read_new = M("10–20 MΩ", 38, RED).move_to([3.6, 1.7, 0])
        rng = np.random.RandomState(5)
        tx0, tx1, ty = 0.9, 6.2, -0.4
        tn = np.linspace(tx0, tx1, 200)
        nz = rng.randn(200) * 0.20
        step = np.where((tn > 3.0) & (tn < 4.3), -0.28, 0.0)
        noisy = poly([[a, ty + b + c] for a, b, c in zip(tn, nz, step)], RED, 3)
        trace_base = DashedLine([tx0, ty, 0], [tx1, ty, 0], color=GREY, stroke_width=2)
        self.play(FadeIn(read_new, shift=UP * 0.2), *[GrowArrow(a) for a in leak], run_time=0.5)
        leak_lbl = lab("leak around the rim", 24, RED).move_to([-4.7, my + 0.9, 0])
        self.play(FadeIn(leak_lbl), run_time=0.3)
        self.at("buried the signal")
        noise_lbl = lab("leak buries the signal in noise", 24, RED).move_to([3.55, -1.4, 0])
        self.play(FadeIn(trace_base), Create(noisy, run_time=0.9, rate_func=linear), FadeIn(noise_lbl))

        # --- slight suction closes the seal: leak shrinks, reading rises into the gigohm range
        self.at("describes seals of")
        suc2 = arr([px, 0.2, 0], [px, 1.5, 0], BLUE, w=6, tip=0.25)
        suc2_lbl = lab("slight suction", 24, BLUE).move_to([LX, 0.9, 0])
        small = VGroup(*[arr([px + s * 1.25, gap_y, 0], [px + s * 0.75, gap_y, 0], RED, w=3, tip=0.1) for s in (-1, 1)])
        self.play(pip.animate.shift(DOWN * 0.10), ReplacementTransform(leak, small), FadeOut(leak_lbl),
                  GrowArrow(suc2), FadeIn(suc2_lbl), run_time=0.6)
        rim2 = VGroup(Line([px - 0.6, my + 0.17, 0], [px - 1.0, my + 0.17, 0], color=GREEN, stroke_width=6),
                      Line([px + 0.6, my + 0.17, 0], [px + 1.0, my + 0.17, 0], color=GREEN, stroke_width=6))
        rng2 = np.random.RandomState(6)
        nz2 = rng2.randn(200) * 0.015
        step2 = np.where((tn > 2.2) & (tn < 3.3), -0.5, 0.0) + np.where((tn > 4.2) & (tn < 4.9), -0.5, 0.0)
        clean = poly([[a, ty + b + c] for a, b, c in zip(tn, nz2, step2)], YELLOW, 4)
        clean_lbl = lab("openings stand clear", 24, YELLOW).move_to([3.55, -1.4, 0])
        read_gig = pow10(9, 11, 36, GREEN).move_to([3.6, 1.7, 0])
        self.play(FadeOut(small), FadeIn(rim2), ReplacementTransform(noisy, clean), ReplacementTransform(noise_lbl, clean_lbl),
                  ReplacementTransform(read_new, read_gig), FadeOut(need), run_time=1.0)
        self.at("called giga")
        gl = lab("giga-seal", 32, GREEN, weight=BOLD).move_to([3.6, 0.9, 0])
        self.play(FadeIn(gl, scale=1.1), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Modes(SpokenScene):
    """voltage clamp on a cell-attached patch with square steps; then inside-out and outside-out patches."""

    def construct(self):
        my = -2.6
        px = -3.4
        mem = membrane(-6.3, 0.2, my, holes=[px], h=0.3, hole_w=0.8)
        ch = Chan(px, my, 1.0, closed=True)
        pip = pipette([px, my + 0.17], h=4.6, tip_w=1.2, top_w=2.2)
        amp = chip("amplifier", BLUE, 28).move_to([px + 0.3, 3.2, 0])
        wire = Line([px, amp.get_bottom()[1], 0], [px, my + 0.9, 0], color=BLUE, stroke_width=4)
        cellname = lab("cell membrane", 24, GREY).move_to([-4.9, my - 0.55, 0])
        self.add(mem, ch, cellname)

        self.at("An amplifier holds")
        self.play(FadeIn(pip), FadeIn(amp, shift=DOWN * 0.15), Create(wire), run_time=0.7)
        self.at("a voltage you choose")
        volt = chip("voltage you choose", YELLOW, 26).move_to([px + 3.5, 2.4, 0])
        va = arr(volt.get_left() + [-0.05, 0, 0], amp.get_right() + [0.05, 0, 0], YELLOW, w=4, tip=0.16)
        self.play(FadeIn(volt, shift=LEFT * 0.2), GrowArrow(va), run_time=0.5)
        self.at("That is voltage clamp")
        vc = lab("voltage clamp", 32, TEXT, weight=BOLD).move_to([px + 3.4, 1.4, 0])
        self.play(FadeIn(vc), run_time=0.4)

        self.at("In the cell attached form")
        ca = chip("cell-attached: the patch stays on the cell", GREY, 24).move_to([2.4, my - 0.7, 0])
        self.play(FadeIn(ca, shift=UP * 0.15), run_time=0.5)

        self.at("With an agonist")
        sol = pipette([px, my + 0.17], h=4.6, tip_w=1.2, top_w=2.2, solution=ORANGE)[0]
        ag = lines("agonist in", "the pipette", size=24, color=ORANGE, buff=0.08, align=RIGHT).move_to([-5.3, -0.6, 0])
        self.play(FadeIn(sol), FadeIn(ag), run_time=0.5)
        self.at("one channel's openings")
        tx0, tx1, ty = 0.9, 6.2, 0.9
        base = DashedLine([tx0, ty, 0], [tx1, ty, 0], color=GREY, stroke_width=2)
        steps = poly([[tx0, ty], [1.4, ty], [1.4, ty - 0.9], [2.3, ty - 0.9], [2.3, ty], [3.2, ty], [3.2, ty - 0.9],
                      [3.6, ty - 0.9], [3.6, ty], [4.4, ty], [4.4, ty - 0.9], [5.5, ty - 0.9], [5.5, ty], [tx1, ty]], YELLOW, 5)
        ex = lab("idealised example", 24, GREY).move_to([3.55, 1.75, 0])
        tl = lab("current through the patch", 24, YELLOW).move_to([3.55, -0.5, 0])
        flow = cur_arrows(px, my - 0.9, my + 1.2, n=2, spread=0.3)
        self.play(FadeIn(base), FadeIn(ex), FadeIn(tl), ch.open(), FadeIn(flow), run_time=0.3)
        self.play(Create(steps, run_time=1.3, rate_func=linear))
        self.at("square steps")
        sq = lab("square steps", 28, YELLOW, weight=BOLD).move_to([3.55, -1.1, 0])
        self.play(FadeIn(sq), run_time=0.3)

        # --- excised patches
        self.at("Pull the patch off")
        cyt = lab("cytoplasm", 24, GREEN).move_to([px + 1.6, my - 0.6, 0])
        self.play(FadeOut(VGroup(wire, amp, flow, volt, va, vc, ca, ag, base, steps, ex, tl, sq, cellname)), FadeIn(cyt), run_time=0.4)
        self.play(VGroup(pip, sol, ch).animate.shift(UP * 1.3), run_time=0.8)
        self.play(FadeOut(VGroup(mem, pip, sol, ch, cyt)), run_time=0.3)

        tip_y = -0.9
        bath_l = RoundedRectangle(corner_radius=0.1, width=5.6, height=2.7, stroke_color=TEAL, stroke_width=2,
                                  fill_color=TEAL, fill_opacity=0.12).move_to([-3.3, -1.95, 0])
        bath_r = bath_l.copy().move_to([3.3, -1.95, 0])
        bl = lab("bath", 24, TEAL).move_to([-5.55, -0.95, 0])
        br = lab("bath", 24, TEAL).move_to([1.05, -0.95, 0])
        pl = pipette([-3.3, tip_y], h=3.7, tip_w=1.2, top_w=2.0)
        pr = pipette([3.3, tip_y], h=3.7, tip_w=1.2, top_w=2.0)
        patch_l = VGroup(membrane(-3.3 - 0.6, -3.3 + 0.6, tip_y, holes=[-3.3], h=0.3, hole_w=0.8), Chan(-3.3, tip_y, 0.9, closed=True))
        patch_r = VGroup(membrane(3.3 - 0.6, 3.3 + 0.6, tip_y, holes=[3.3], h=0.3, hole_w=0.8), Chan(3.3, tip_y, 0.9, closed=True))
        t_l = lab("Inside-out patch", 30, TEXT, weight=BOLD).move_to([-3.3, 3.3, 0])
        t_r = lab("Outside-out patch", 30, TEXT, weight=BOLD).move_to([3.3, 3.3, 0])
        self.at("with its cytoplasmic face")
        self.play(FadeIn(VGroup(bath_l, bl, pl, patch_l)), FadeIn(t_l), run_time=0.5)
        f_l = lab("cytoplasmic face in the bath", 26, GREEN).move_to([-3.3, -1.75, 0])
        fa_l = arr([-3.3, -1.5, 0], [-3.3, tip_y - 0.3, 0], GREEN, w=4, tip=0.16)
        self.play(FadeIn(f_l), GrowArrow(fa_l), run_time=0.5)
        self.at("You can change the solution")
        chg = chip("change the solution here", ORANGE, 24).move_to([-3.3, -2.6, 0])
        self.play(FadeIn(chg), bath_l.animate.set_fill(ORANGE, 0.18).set_stroke(ORANGE), run_time=0.8)
        self.at("Start from whole cell mode")
        cell_o = cell_blob([3.3, -2.5], 0.7)
        pr2 = pipette([3.3, tip_y - 0.9], h=3.0, tip_w=0.8, top_w=1.8)
        opening = Line([3.3 - 0.38, -1.8, 0], [3.3 + 0.38, -1.8, 0], color=BG, stroke_width=7)
        wc_lbl = lab("whole-cell mode", 24, GREY).move_to([5.5, 0.7, 0])
        self.play(FadeIn(VGroup(bath_r, br)), FadeIn(t_r), FadeIn(cell_o), FadeIn(pr2), FadeIn(opening), FadeIn(wc_lbl), run_time=0.6)
        self.at("pull away instead")
        self.play(pr2.animate.shift(UP * 0.9), FadeOut(opening), FadeOut(wc_lbl), run_time=0.8)
        self.at("reseals with")
        patch_r2 = VGroup(membrane(3.3 - 0.6, 3.3 + 0.6, tip_y, holes=[3.3], h=0.3, hole_w=0.8), Chan(3.3, tip_y, 0.9, closed=True))
        self.play(FadeIn(patch_r2), run_time=0.4)
        self.at("extracellular face")
        f_r = lab("extracellular face in the bath", 24, GREEN).move_to([3.3, -1.4, 0])
        fa_r = arr([3.3, -1.2, 0], [3.3, tip_y - 0.2, 0], GREEN, w=4, tip=0.14)
        self.play(FadeIn(f_r), GrowArrow(fa_r), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Inside(SpokenScene):
    """whole-cell dialysis; perforated patch; current clamp plot."""

    def construct(self):
        cy, r = -0.6, 1.2
        top_y = cy + r
        cx0 = 0.0            # whole-cell starts centred, slides left when the perforated patch arrives
        cw = cell_blob([cx0, cy], r)
        pw = pipette([cx0, top_y - 0.05], h=2.4, tip_w=0.7, top_w=1.5)
        t_w = lab("Whole-cell", 30, TEXT, weight=BOLD).move_to([cx0, 3.3, 0])
        opening = Line([cx0 - 0.3, top_y, 0], [cx0 + 0.3, top_y, 0], color=BG, stroke_width=7)
        sol = pipette([cx0, top_y - 0.05], h=2.4, tip_w=0.7, top_w=1.5, solution=ORANGE)[0]
        dots = VGroup(*[Dot([cx0 + dx, cy + dy, 0], radius=0.09, color=ORANGE) for dx, dy in
                        [(-0.2, 0.8), (0.2, 0.7), (0.0, 0.4), (-0.4, 0.2), (0.4, 0.1), (-0.2, -0.2), (0.2, -0.3), (0.0, -0.6)]])
        own_w = VGroup(*[Dot([cx0 + dx, cy + dy, 0], radius=0.09, color=TEAL) for dx, dy in
                         [(-0.5, -0.2), (0.5, -0.1), (-0.3, -0.7), (0.3, -0.6)]])
        xch = DoubleArrow([cx0, top_y + 1.0, 0], [cx0, top_y - 0.45, 0], buff=0, color=TEXT, stroke_width=4, tip_length=0.16)
        dl = lab("pipette solution and cytoplasm exchange", 24, ORANGE)
        dl = fit(dl, max_w=6.0).move_to([cx0, cy - r - 0.45, 0])
        wc = VGroup(cw, pw, t_w, opening, sol, dots, dl, own_w, xch)

        self.at("In whole cell mode")
        self.play(FadeIn(cw), FadeIn(pw), FadeIn(t_w), FadeIn(own_w), run_time=0.6)
        self.at("gains access to the cell interior")
        self.play(FadeIn(opening), FadeIn(sol), run_time=0.4)
        self.at("ions and small molecules")
        self.play(FadeIn(xch), LaggedStart(*[FadeIn(d, shift=DOWN * 0.3) for d in dots[:5]], lag_ratio=0.1),
                  own_w[0].animate.move_to([cx0 - 0.2, top_y + 0.6, 0]), own_w[1].animate.move_to([cx0 + 0.2, top_y + 0.9, 0]),
                  FadeIn(dl), run_time=1.4)
        self.at("Perforated patch uses")
        cxp = 3.2
        self.play(wc.animate.shift(LEFT * 3.2), run_time=0.6)
        cp = cell_blob([cxp, cy], r)
        pp = pipette([cxp, top_y - 0.05], h=2.4, tip_w=0.7, top_w=1.5, solution=ORANGE)
        t_p = lab("Perforated patch", 30, TEXT, weight=BOLD).move_to([cxp, 3.3, 0])
        pores = VGroup(*[Dot([cxp + dx, top_y, 0], radius=0.07, color=PURPLE) for dx in (-0.2, 0.0, 0.2)])
        cont = VGroup(*[Dot([cxp + dx, cy + dy, 0], radius=0.09, color=TEAL) for dx, dy in
                        [(-0.5, 0.4), (0.4, 0.5), (0.0, 0.0), (-0.4, -0.4), (0.5, -0.3)]])
        pl = lab("pore-former: gramicidin or nystatin", 24, PURPLE).move_to([cxp, cy - r - 0.45, 0])
        keep = lab("the cell keeps most of its contents", 24, TEAL).move_to([cxp, cy - r - 1.05, 0])
        self.play(FadeIn(cp), FadeIn(pp), FadeIn(t_p), run_time=0.5)
        self.at("a pore former")
        self.play(FadeIn(pores), FadeIn(pl), run_time=0.5)
        self.at("while the cell keeps most")
        self.play(FadeIn(cont), FadeIn(keep), run_time=0.5)
        self.play(Indicate(cont, color=TEAL, scale_factor=1.2), run_time=0.5)

        # --- current clamp
        self.at("In current clamp")
        self.play(FadeOut(VGroup(wc, cp, pp, t_p, pores, cont, pl, keep)), run_time=0.5)
        title = lab("Current clamp", 32, TEXT, weight=BOLD).move_to([0, 3.3, 0])
        ex = lab("idealised", 24, GREY).move_to([5.2, 3.3, 0])
        x0, xe = -4.6, 2.6
        on, off = -3.2, 0.9
        yi, yv, H = 2.0, -1.9, 2.4
        cur = poly([[x0, yi], [on, yi], [on, yi + 0.9], [off, yi + 0.9], [off, yi], [xe, yi]], YELLOW, 5)
        cur_l = lab("current", 24, YELLOW).move_to([-5.5, yi + 0.5, 0])
        cur_l2 = lab("(set)", 22, GREY).next_to(cur_l, DOWN, buff=0.08)
        tau = 0.55
        ts = np.linspace(on, off, 80)
        vv = H * (1 - np.exp(-(ts - on) / tau))
        vend = H * (1 - np.exp(-(off - on) / tau))
        tdec = np.linspace(off, xe, 40)
        vd = vend * np.exp(-(tdec - off) / tau)
        vpts = [[x0, yv], [on, yv]] + [[a, yv + b] for a, b in zip(ts, vv)] + [[a, yv + b] for a, b in zip(tdec, vd)]
        volt = poly(vpts, GREEN, 5)
        volt_l = lab("voltage", 24, GREEN).move_to([-5.5, yv + 0.5, 0])
        volt_l2 = lab("(recorded)", 22, GREY).next_to(volt_l, DOWN, buff=0.08)
        self.play(FadeIn(title), FadeIn(ex), run_time=0.3)
        self.play(FadeIn(cur_l), FadeIn(cur_l2), Create(cur, run_time=1.0, rate_func=linear))
        self.play(FadeIn(volt_l), FadeIn(volt_l2), run_time=0.2)
        self.at("A current step")
        self.play(Create(volt, run_time=1.3, rate_func=linear))
        self.at("The steady voltage change")
        yp = yv + vend
        plateau = DashedLine([-0.3, yp, 0], [3.1, yp, 0], color=TEXT, stroke_width=3)
        basel = DashedLine([x0, yv, 0], [3.1, yv, 0], color=GREY, stroke_width=2)
        br = DoubleArrow([3.1, yv, 0], [3.1, yp, 0], buff=0, color=TEXT, stroke_width=3, tip_length=0.15)
        steady = lines("steady voltage", "change", size=24, color=TEXT, buff=0.06, align=ORIGIN).move_to([4.8, yv + vend / 2 + 0.7, 0])
        steady_n = lines("÷ current =", "input resistance", size=24, color=GREEN, buff=0.08, align=ORIGIN).move_to([4.8, yv + vend / 2 - 0.35, 0])
        self.play(Create(plateau), Create(basel), GrowFromCenter(br), FadeIn(steady), run_time=0.6)
        self.at("is the input resistance")
        self.play(FadeIn(steady_n), run_time=0.3)
        self.at("The charging curve")
        charge = poly([[a, yv + b] for a, b in zip(ts[:40], vv[:40])], YELLOW, 8)
        cl = lab("charging curve", 26, TEXT).move_to([-1.9, yv - 0.6, 0])
        self.play(Create(charge, run_time=0.7), FadeIn(cl), run_time=0.7)
        self.at("gives the time constant")
        cn = lab("time constant", 26, GREEN, weight=BOLD).move_to([-1.9, yv - 1.1, 0])
        self.play(FadeIn(cn), run_time=0.3)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Reading(SpokenScene):
    """read an idealised single-channel trace: level, step height, open fraction; control vs drug."""

    def construct(self):
        x0, x1 = -4.4, 3.4
        sx = x1 - x0
        d = -1.0
        RC = 5.0                      # right column centre

        def X(t):
            return x0 + t * sx

        y1 = 0.9
        g1 = VGroup()
        iv1 = [(0.08, 0.16), (0.37, 0.43), (0.71, 0.77)]
        a = poly([[X(0), y1], [X(0.08), y1]])
        b = poly([[X(0.08), y1], [X(0.08), y1 + d], [X(0.16), y1 + d]])
        c = poly([[X(0.16), y1 + d], [X(0.16), y1], [X(0.37), y1]])
        rest = poly([[X(0.37), y1], [X(0.37), y1 + d], [X(0.43), y1 + d], [X(0.43), y1], [X(0.71), y1], [X(0.71), y1 + d],
                     [X(0.77), y1 + d], [X(0.77), y1], [X(1.0), y1]])
        zero_l = lab("closed", 24, GREY).move_to([-5.45, y1, 0])
        open_l = lab("open", 24, GREY).move_to([-5.45, y1 + d, 0])
        zline = DashedLine([x0 - 0.1, y1, 0], [x1, y1, 0], color=GREY, stroke_width=2)

        self.at("The trace sits")
        hdr = lab("Reading one record", 32, TEXT, weight=BOLD).move_to([-2.6, 3.2, 0])
        self.play(FadeIn(zline), FadeIn(hdr), run_time=0.3)
        self.at("sits at zero")
        self.play(FadeIn(zero_l), Create(a, run_time=0.7, rate_func=linear))
        self.at("steps to a fixed level")
        self.play(FadeIn(open_l), Create(b, run_time=0.8, rate_func=linear))
        self.at("and steps back")
        self.play(Create(c, run_time=0.7, rate_func=linear))
        g1.add(zline, zero_l, open_l, a, b, c, rest)

        self.at("The step height")
        self.play(Create(rest, run_time=1.0, rate_func=linear))
        brace = DoubleArrow([X(0.08) - 0.28, y1, 0], [X(0.08) - 0.28, y1 + d, 0], buff=0, color=YELLOW, stroke_width=4, tip_length=0.15)
        i_l = lines("unitary", "current, i", size=26, color=YELLOW, buff=0.05, align=ORIGIN).move_to([X(0.57), y1 + d / 2, 0])
        self.play(GrowFromCenter(brace), FadeIn(i_l), run_time=0.5)
        g1.add(brace)

        self.at("The fraction of time")
        shades = VGroup(*[Rectangle(width=(b2 - a2) * sx, height=-d, stroke_width=0, fill_color=GREEN, fill_opacity=0.35)
                          .move_to([X((a2 + b2) / 2), y1 + d / 2, 0]) for a2, b2 in iv1])
        po = lab("open probability: fraction of time open", 26, GREEN, weight=BOLD).move_to([X(0.5), y1 + d - 0.55, 0])
        self.play(FadeOut(i_l), FadeIn(shades), FadeIn(po), run_time=0.6)
        g1.add(shades)

        self.at("In this idealized example")
        tagx = lab("IDEALISED EXAMPLE", 24, GOLD, weight=BOLD).move_to([4.5, 3.2, 0])
        lv = M("−2 pA", 28, YELLOW).move_to([-5.4, y1 + d - 0.55, 0])
        self.play(FadeIn(tagx), FadeIn(lv), run_time=0.4)
        g1.add(lv)
        self.at("milliseconds of one second")
        t200 = M("open 200 ms of 1 s", 26, GREEN).move_to([X(0.5), y1 + d - 0.55, 0])
        self.play(ReplacementTransform(po, t200), run_time=0.4)
        g1.add(t200)
        self.at("Open probability is")
        p1 = M("P_o = 0.2", 30, GREEN, weight=BOLD).move_to([RC, y1 + d / 2, 0])
        self.play(FadeIn(p1, scale=1.1), run_time=0.4)
        g1.add(p1)

        # --- after a drug
        self.at("After a drug")
        self.play(g1.animate.shift(UP * 1.0), run_time=0.5)
        y2 = -1.0
        iv2 = [(0.05, 0.20), (0.30, 0.45), (0.55, 0.70), (0.80, 0.85)]
        pts = [[X(0), y2]]
        for a2, b2 in iv2:
            pts += [[X(a2), y2], [X(a2), y2 + d], [X(b2), y2 + d], [X(b2), y2]]
        pts.append([X(1.0), y2])
        tr2 = poly(pts)
        zline2 = DashedLine([x0 - 0.1, y2, 0], [x1, y2, 0], color=GREY, stroke_width=2)
        drug = lab("after a drug", 26, ORANGE, weight=BOLD).move_to([-4.6, y2 + 0.5, 0])
        lv2 = M("−2 pA", 28, YELLOW).move_to([-5.4, y2 + d - 0.55, 0])
        self.play(FadeIn(zline2), FadeIn(drug), FadeIn(lv2), Create(tr2, run_time=1.6, rate_func=linear))
        shades2 = VGroup(*[Rectangle(width=(b2 - a2) * sx, height=-d, stroke_width=0, fill_color=GREEN, fill_opacity=0.35)
                           .move_to([X((a2 + b2) / 2), y2 + d / 2, 0]) for a2, b2 in iv2])
        self.play(FadeIn(shades2), run_time=0.3)
        self.at("milliseconds a second")
        t500 = M("open 500 ms of 1 s", 26, GREEN).move_to([X(0.5), y2 + d - 0.55, 0])
        self.play(FadeIn(t500), run_time=0.4)
        self.at("Open probability is", nth=1)
        p2 = M("P_o = 0.5", 30, GREEN, weight=BOLD).move_to([RC, y2 + d / 2, 0])
        self.play(FadeIn(p2, scale=1.1), run_time=0.4)

        self.at("The drug changed gating")
        c1 = chip("gating changed", GREEN, 26).move_to([-2.4, -3.2, 0])
        c2 = chip("level (i) unchanged", YELLOW, 26).move_to([2.3, -3.2, 0])
        self.play(FadeIn(c1, shift=UP * 0.15), run_time=0.5)
        self.at("not conduction")
        self.play(FadeIn(c2, shift=UP * 0.15), run_time=0.5)
        self.finish()

# ---------------------------------------------------------------------------------------------
class S06Pitfalls(SpokenScene):
    """brief closures vanish (control: report filter and sampling rate); whole-cell replaces chloride (control: perforated)."""

    def construct(self):
        # --- left panel: brief closures
        lx0, lx1 = -5.9, -0.9
        lsx = lx1 - lx0
        t1 = lab("Pitfall 1", 24, RED, weight=BOLD).move_to([-3.4, 3.3, 0])
        head1 = lab("Brief closures vanish", 28, TEXT, weight=BOLD).move_to([-3.4, 2.7, 0])
        d = -0.8

        def X(t):
            return lx0 + t * lsx

        ya = 1.5
        raw_pts = [[X(0), ya], [X(0.08), ya], [X(0.08), ya + d]]
        for t in (0.3, 0.5, 0.7):
            raw_pts += [[X(t), ya + d], [X(t), ya], [X(t + 0.025), ya], [X(t + 0.025), ya + d]]
        raw_pts += [[X(0.9), ya + d], [X(0.9), ya], [X(1.0), ya]]
        raw = poly(raw_pts, GREY, 4)
        raw_l = lab("what the channel did", 24, GREY).move_to([-3.4, ya + 0.55, 0])
        yb = -0.6
        shown = poly([[X(0), yb], [X(0.08), yb], [X(0.08), yb + d], [X(0.9), yb + d], [X(0.9), yb], [X(1.0), yb]], YELLOW, 5)
        shown_l = lab("what the recording shows", 24, YELLOW).move_to([-3.4, yb + 0.55, 0])
        ctrl1 = chip("report the filter and sampling rate", GREEN, 24)
        ctrl1 = fit(ctrl1, max_w=5.4).move_to([-3.4, -2.8, 0])

        self.at("Brief closures")
        self.play(FadeIn(t1), FadeIn(head1), run_time=0.5)
        self.at("Brief closures shorter")
        self.play(FadeIn(raw_l), Create(raw, run_time=1.4, rate_func=linear))
        self.at("vanish from the trace")
        self.play(FadeIn(shown_l), Create(shown, run_time=1.0, rate_func=linear))
        self.at("so report the filter")
        self.play(FadeIn(ctrl1, shift=UP * 0.15), run_time=0.5)

        # --- right panel: chloride
        sep = Line([0.0, 3.3, 0], [0.0, -3.3, 0], color=GREY, stroke_width=1.5)
        t2 = lab("Pitfall 2", 24, RED, weight=BOLD).move_to([3.3, 3.3, 0])
        head2 = lab("Chloride is replaced", 28, TEXT, weight=BOLD).move_to([3.3, 2.7, 0])
        cxa, cxb, cy = 1.7, 4.9, 0.0
        cell_a = cell_blob([cxa, cy], 0.95)
        cell_b = cell_blob([cxb, cy], 0.95)
        pa = pipette([cxa, cy + 0.95 - 0.05], h=1.5, tip_w=0.5, top_w=1.1, solution=ORANGE)
        pb = pipette([cxb, cy + 0.95 - 0.05], h=1.5, tip_w=0.5, top_w=1.1, solution=ORANGE)
        cl_a = chip("Cl⁻", TEAL, 26).move_to([cxa, cy - 0.05, 0])
        cl_b = chip("Cl⁻", TEAL, 26).move_to([cxb, cy - 0.05, 0])
        na = lab("whole-cell", 24, GREY).move_to([cxa, cy - 1.45, 0])
        nb = lab("perforated", 24, GREY).move_to([cxb, cy - 1.45, 0])
        self.at("And a conventional")
        self.play(FadeIn(sep), FadeIn(t2), FadeIn(head2), run_time=0.4)
        self.play(FadeIn(cell_a), FadeIn(pa), FadeIn(cl_a), FadeIn(na), run_time=0.6)
        self.at("replaces the cell's chloride")
        cl_a2 = chip("Cl⁻", ORANGE, 26).move_to([cxa, cy - 0.05, 0])
        self.play(ReplacementTransform(cl_a, cl_a2), run_time=0.8)
        self.at("reflects the experimenter's recipe")
        rec = lab("GABA reversal is", 24, ORANGE).move_to([cxa, cy - 2.05, 0])
        rec2 = lab("set by the recipe", 24, ORANGE).move_to([cxa, cy - 2.45, 0])
        self.play(FadeIn(rec), FadeIn(rec2), run_time=0.5)
        self.at("perforated patch leaves")
        self.play(FadeIn(cell_b), FadeIn(pb), FadeIn(cl_b), FadeIn(nb), run_time=0.6)
        self.at("leaves the cell's chloride alone")
        own = lab("the cell's own", 24, TEAL).move_to([cxb, cy - 2.05, 0])
        own2 = lab("chloride stays", 24, TEAL).move_to([cxb, cy - 2.45, 0])
        self.play(Indicate(cl_b, color=TEAL, scale_factor=1.2), FadeIn(own), FadeIn(own2), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07Origin(SpokenScene):
    """origin rows: 1976 and 1981."""

    def row(self, year, text_lines, tagtext, icon, y):
        yr = M(year, 44, GOLD, weight=BOLD).move_to([-5.0, y, 0])
        icon.scale(1.5).move_to([-2.4, y, 0])
        txt = lines(*text_lines, size=34, color=TEXT, buff=0.12)
        tg = tag(tagtext, size=26)
        grp = VGroup(txt, tg).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        grp = fit(grp, max_w=8.0, max_h=2.2)
        grp.move_to([-0.9 + grp.width / 2, y, 0])
        return yr, icon, grp

    def construct(self):
        ic76 = poly([[-0.9, 0.0], [-0.5, 0.0], [-0.5, -0.5], [-0.05, -0.5], [-0.05, 0.0], [0.25, 0.0], [0.25, -0.5], [0.55, -0.5],
                     [0.55, 0.0], [0.9, 0.0]], YELLOW, 4)
        pm = pipette([0, -0.45], h=0.9, tip_w=0.5, top_w=0.9)
        mm = membrane(-0.9, 0.9, -0.6, holes=[], h=0.2)
        gr = VGroup(Line([-0.25, -0.5, 0], [-0.55, -0.5, 0], color=GREEN, stroke_width=5),
                    Line([0.25, -0.5, 0], [0.55, -0.5, 0], color=GREEN, stroke_width=5))
        ic81 = VGroup(pm, mm, gr)
        ic81.shift(UP * 0.15)
        r76 = self.row("1976", ["Single-channel currents from", "denervated frog muscle"], "Neher & Sakmann, 1976", ic76, 1.6)
        r81 = self.row("1981", ["Gigaseal methods described, with", "excised patches and whole-cell recording"],
                       "Hamill, Marty, Neher, Sakmann & Sigworth, 1981", ic81, -1.5)

        self.at("recorded")
        yr, ic, tx = r76
        self.play(FadeIn(yr), FadeIn(tx[0]), run_time=0.6)
        self.at("Their records showed")
        self.play(Create(ic, run_time=1.2, rate_func=linear), FadeIn(tx[1]), run_time=1.2)
        self.at("described the")
        yr, ic, tx = r81
        self.play(FadeIn(yr), FadeIn(ic), FadeIn(tx), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S08Unlocked(SpokenScene):
    """three separate panels: cell-attached glucose, excised inside-out ATP, excised outside-out serotonin; then the rule."""

    def construct(self):
        CX = [-4.2, 0.0, 4.2]
        tipy = 1.2
        TY = -2.55
        AMP = 0.6

        def steps(x0, x1, ty, ivs, amp=AMP, color=YELLOW):
            pts = [[x0, ty]]
            for a, b in ivs:
                pts += [[a, ty], [a, ty - amp], [b, ty - amp], [b, ty]]
            pts.append([x1, ty])
            return poly(pts, color, 5)

        def panel(cx, header, tag_lines, closed=True):
            hd = fit(lab(header, 28, TEXT, weight=BOLD), max_w=3.95).move_to([cx, 3.35, 0])
            tg = lines(*tag_lines, size=22, color=GREY, buff=0.03, align=ORIGIN)
            tg.move_to([cx, 2.95 if len(tag_lines) == 1 else 2.82, 0])
            box = RoundedRectangle(corner_radius=0.1, width=3.9, height=1.95, stroke_color=TEAL, stroke_width=2,
                                   fill_color=TEAL, fill_opacity=0.12).move_to([cx, 0.225, 0])
            pip = pipette([cx, tipy], h=1.15, tip_w=1.3, top_w=2.0)
            ch = Chan(cx, tipy, 1.1, closed=closed)
            mem = membrane(cx - 0.8, cx + 0.8, tipy, holes=[cx], h=0.3, hole_w=0.9)
            return VGroup(hd, tg), box, pip, ch, mem

        def two(a, b, color, pos):
            return lines(a, b, size=22, color=color, buff=0.04, align=ORIGIN).move_to(pos)

        W2 = 1.9   # half-width of each trace
        # ---------------- column 1: cell-attached, glucose
        c1 = CX[0]
        hd1, box1, pip1, ch1, mem1 = panel(c1, "Cell-attached", ["Rorsman & Trube, 1985"], closed=False)
        in1 = lab("cell", 22, TEAL).move_to([c1 - 1.5, -0.55, 0])
        glu = chip("20 mM glucose", ORANGE, 24).move_to([c1, 0.15, 0])
        t1a = steps(c1 - W2, c1, TY, [(c1 - 1.6, c1 - 1.35), (c1 - 1.05, c1 - 0.7), (c1 - 0.5, c1 - 0.2)])
        t1b = steps(c1, c1 + W2, TY, [(c1 + 1.0, c1 + 1.12)])
        b1 = DashedLine([c1 - W2, TY, 0], [c1 + W2, TY, 0], color=GREY, stroke_width=2)
        l1a = lab("before glucose", 22, GREY).move_to([c1 - 0.95, -1.3, 0])
        l1b = two("with glucose:", "suppressed", YELLOW, [c1 + 0.95, -2.0, 0])
        ex1 = lab("example traces", 22, GREY).move_to([c1, -3.38, 0])
        # ---------------- column 2: excised inside-out, ATP
        c2 = CX[1]
        hd2, box2, pip2, ch2, mem2 = panel(c2, "Excised, inside-out", ["Rorsman & Trube, 1985"], closed=False)
        in2 = lab("bath", 22, TEAL).move_to([c2 - 1.5, -0.55, 0])
        face2 = lab("cytoplasmic face", 24, GREEN).move_to([c2, 0.72, 0])
        atp = chip("3 mM ATP", ORANGE, 24).move_to([c2, 0.15, 0])
        x1, x2, x3_ = c2 - 0.9, c2 + 0.1, c2 + W2
        t2a = steps(c2 - W2, x1, TY, [(c2 - 1.6, c2 - 1.3)])
        t2b = poly([[x1, TY], [x2, TY]], YELLOW, 5)
        t2c = steps(x2, x3_, TY, [(c2 + 0.4, c2 + 0.7), (c2 + 1.0, c2 + 1.3), (c2 + 1.55, c2 + 1.7)])
        b2 = DashedLine([c2 - W2, TY, 0], [c2 + W2, TY, 0], color=GREY, stroke_width=2)
        l2a = two("before", "ATP", GREY, [c2 - 1.4, -1.3, 0])
        l2b = two("with", "ATP", YELLOW, [c2 - 0.4, -2.0, 0])
        l2c = two("ATP washed out:", "openings return", GREEN, [c2 + 1.0, -1.3, 0])
        ex2 = lab("example traces", 22, GREY).move_to([c2, -3.38, 0])
        # ---------------- column 3: excised outside-out, serotonin
        c3 = CX[2]
        hd3, box3, pip3, ch3, mem3 = panel(c3, "Excised, outside-out", ["Derkach, Surprenant", "& North, 1989"], closed=True)
        in3 = lab("bath", 22, TEAL).move_to([c3 - 1.5, -0.55, 0])
        face3 = lab("extracellular face", 24, GREEN).move_to([c3, 0.72, 0])
        ser = chip("serotonin", ORANGE, 24).move_to([c3, 0.15, 0])
        t3 = steps(c3 - W2, c3 + W2, TY, [(c3 - 1.55, c3 - 1.25), (c3 - 0.8, c3 - 0.55), (c3 - 0.1, c3 + 0.45), (c3 + 0.95, c3 + 1.2)])
        b3 = DashedLine([c3 - W2, TY, 0], [c3 + W2, TY, 0], color=GREY, stroke_width=2)
        l3 = lab("5-HT3: unitary currents", 22, YELLOW).move_to([c3, -1.05, 0])
        ex3 = lab("example traces", 22, GREY).move_to([c3, -3.38, 0])
        x3 = lines("no cytoplasm in the patch:", "evidence that the receptor", "is itself a channel", size=22, color=TEXT, buff=0.04, align=ORIGIN)
        x3 = x3.move_to([c3, -1.85, 0])

        # ---- scene
        self.at("found that")
        self.play(FadeIn(hd1), FadeIn(box1), FadeIn(pip1), FadeIn(mem1), FadeIn(ch1), FadeIn(in1), FadeIn(b1), FadeIn(ex1),
                  FadeIn(t1a), FadeIn(l1a), run_time=0.7)
        self.at("millimolar glucose")
        self.play(FadeIn(glu, shift=UP * 0.1), run_time=0.4)
        self.at("suppressed potassium channel activity")
        self.play(Create(t1b, run_time=0.8, rate_func=linear), FadeIn(l1b), run_time=0.8)
        self.at("millimolar ATP")
        self.play(FadeIn(hd2), FadeIn(box2), FadeIn(pip2), FadeIn(mem2), FadeIn(ch2), FadeIn(in2), FadeIn(b2), FadeIn(ex2),
                  FadeIn(t2a), FadeIn(l2a), run_time=0.7)
        self.at("on the cytoplasmic face")
        self.play(FadeIn(face2), FadeIn(atp, shift=UP * 0.2), run_time=0.6)
        self.at("reversibly blocked")
        self.play(ch2.close(), Create(t2b, run_time=0.7, rate_func=linear), FadeIn(l2b), run_time=0.7)
        self.at("The excised patch")
        self.play(ch2.open(), FadeOut(atp), Create(t2c, run_time=0.8, rate_func=linear), FadeIn(l2c), run_time=0.8)

        self.at("recorded")
        self.play(FadeIn(hd3), FadeIn(box3), FadeIn(pip3), FadeIn(mem3), FadeIn(ch3), FadeIn(in3), FadeIn(b3), FadeIn(ex3),
                  run_time=0.7)
        self.at("unitary currents")
        self.play(FadeIn(face3), FadeIn(ser, shift=UP * 0.2), run_time=0.6)
        self.at("enteric neurons")
        self.play(ch3.open(), Create(t3, run_time=1.2, rate_func=linear), FadeIn(l3), run_time=1.2)
        self.at("Serotonin opening single channels")
        self.play(FadeIn(x3), run_time=0.6)

        # --- the rule
        self.at("Keep this rule")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.6)
        rule = lines("A current from cultured cells, or", "from cells engineered to make the", "channel, belongs to that preparation", "and protocol, not to a living animal.",
                     size=38, color=TEXT, buff=0.2, align=ORIGIN)
        rule_box = SurroundingRectangle(rule, color=GOLD, stroke_width=3, buff=0.45, corner_radius=0.2)
        head = lab("KEEP THIS RULE", 26, GOLD, weight=BOLD).next_to(rule_box, UP, buff=0.25)
        grp = VGroup(rule, rule_box, head).move_to([0, 0, 0])
        self.play(FadeIn(head), Create(rule_box), run_time=0.5)
        self.at("A current from cultured")
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S09End(EndCard):
    LINE = "Currents from cultured or engineered cells belong to that preparation and protocol."
