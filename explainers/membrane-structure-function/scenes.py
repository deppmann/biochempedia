"""Crossing the Membrane  (Biochemistrypedia: Membranes: The Impermeable Sheet That Builds Itself)

COLOR MAP (one color per concept, whole video)
  GREY    = the lipid bilayer, axes, "inside / outside" labels
  BLUE    = Na+ and charged species (the thing that cannot dissolve in oil), the sodium gradient
  YELLOW  = K+ (the potassium channel story)
  TEAL    = water / the hydration shell
  GREEN   = passive, downhill: channels, simple + facilitated diffusion, uncharged indole
  ORANGE  = carriers, incl. symporters and antiporters (the secondary active carriers)
  RED     = ATP-powered pumps, the energy cost / uphill
  PURPLE  = cargo that gets driven UPHILL (glucose, Ca2+)
  GOLD    = call-outs, charge repulsion;  TEXT = neutral cargo and labels
NO molecular structures are drawn: only labelled chips, dots, blocks, arrows, schematic
energy profiles (no numbers) and a log-scale bar.
"""
import numpy as np

from bp_style import *

ORANGE = "#F2A65A"
PURPLE = "#B48EE0"


# ------------------------------------------------------------------ helpers
class Sp(SpokenScene):
    def at_s(self, t):
        r = t - self.elapsed()
        if r > 0.02:
            self.wait(r)


def sig(x):
    return 1.0 / (1.0 + np.exp(-x))


def mem(x0=-6.2, x1=6.2, y=0.0, th=0.8, gaps=()):
    """Schematic bilayer: a faint hydrophobic core slab with a row of head-group dots on each face.
    gaps = [(center_x, width)] leave room for transport proteins."""
    g = VGroup()
    segs, cur = [], x0
    for c, w in sorted(gaps):
        segs.append((cur, c - w / 2))
        cur = c + w / 2
    segs.append((cur, x1))
    for a, b in segs:
        if b - a < 0.2:
            continue
        g.add(Rectangle(width=b - a, height=th, stroke_width=0, fill_color=GREY, fill_opacity=0.22)
              .move_to([(a + b) / 2, y, 0]))
        for x in np.linspace(a + 0.15, b - 0.15, max(int((b - a) / 0.3), 1)):
            for s in (1, -1):
                g.add(Circle(radius=0.1, stroke_width=0, fill_color=GREY, fill_opacity=0.85)
                      .move_to([x, y + s * (th / 2 + 0.12), 0]))
    return g


def ion(label, color, r=0.32, size=24):
    c = Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=1)
    return VGroup(c, T(label, size, BG, weight=BOLD).move_to(c))


def dot(color=TEXT, r=0.13):
    return Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=1)


def zig(p, q, color=GOLD, amp=0.17, n=4):
    """A small lightning-bolt line between two points: the repulsion between like charges."""
    p, q = np.array(p, float), np.array(q, float)
    d = q - p
    nrm = np.array([-d[1], d[0], 0.0])
    nrm = nrm / (np.linalg.norm(nrm) + 1e-9)
    pts = [p]
    for i in range(1, 2 * n):
        pts.append(p + d * i / (2 * n) + nrm * amp * (1 if i % 2 else -1))
    pts.append(q)
    return VMobject(color=color, stroke_width=7).set_points_as_corners(pts)


# ------------------------------------------------------------------ cards
class S00Title(TitleCard):
    LESSON = "Membrane structure & function"
    TITLE = "Crossing the Membrane"


class S06End(EndCard):
    LINE = "Three questions sort every way across a membrane."


# ------------------------------------------------------------------ s01: the barrier
class S01Barrier(Sp):
    def construct(self):
        MY = -0.6
        mb = mem(-6.2, 6.2, y=MY, th=1.1)
        core = T("hydrophobic core", 24, GREY).move_to([0, MY, 0])
        out_l = T("outside", 24, GREY).move_to([-5.4, 1.3, 0])
        in_l = T("inside", 24, GREY).move_to([-5.5, -2.5, 0])
        self.play(FadeIn(mb), run_time=1.0)
        self.play(FadeIn(core), FadeIn(out_l), FadeIn(in_l), run_time=0.6)

        # ions and polar molecules bounce off the bilayer
        self.at("ions and most polar")
        na = ion("Na⁺", BLUE).move_to([-3.4, 2.7, 0])
        gl = chip("glucose", PURPLE, 24).move_to([0.2, 2.9, 0])
        k = ion("K⁺", YELLOW).move_to([3.4, 2.6, 0])
        cargo = [na, gl, k]
        self.play(*[FadeIn(c) for c in cargo], run_time=0.4)
        for _ in range(2):
            self.play(AnimationGroup(*[c.animate.set_y(0.62) for c in cargo], lag_ratio=0.2),
                      run_time=0.7, rate_func=rush_into)
            self.play(AnimationGroup(*[c.animate.set_y(1.75) for c in cargo], lag_ratio=0.2),
                      run_time=0.6, rate_func=rush_from)

        self.at("the reason is")
        call = T("the barrier is energy, not size", 30, GOLD).move_to([0, 3.3, 0])
        self.play(FadeIn(call, shift=DOWN * 0.1), run_time=0.6)

        # a naked ion has to give up its water to enter the oil
        self.at("crossing the hydrophobic core")
        self.play(FadeOut(VGroup(*cargo, call, out_l, in_l)), run_time=0.5)
        big = ion("Na⁺", BLUE, r=0.42, size=28).move_to([0, 2.35, 0])
        shell = VGroup(*[dot(TEAL, 0.17).move_to(big.get_center() + 0.85 * np.array([np.cos(a), np.sin(a), 0]))
                         for a in np.linspace(0, TAU, 7)[:-1] + 0.3])
        leg = T("shell of water", 24, TEAL).move_to([3.4, 2.35, 0])
        self.play(FadeIn(big), FadeIn(shell), FadeIn(leg), run_time=0.7)
        ionshell = VGroup(big, shell)
        self.play(ionshell.animate.shift(DOWN * 0.5), run_time=0.7)

        self.at("shedding the shell")
        self.play(*[d.animate.shift((d.get_center() - big.get_center()) * 0.55).set_opacity(0.3) for d in shell],
                  FadeOut(leg), FadeOut(core), run_time=1.0)
        self.play(big.animate.move_to([0, MY, 0]).scale(0.75), run_time=1.1)
        wall = T("an ion with no water, alone in oil", 28, RED).move_to([0, -2.3, 0])
        self.play(FadeIn(wall), run_time=0.5)

        # schematic energy profile
        self.at("stripping that water off")
        self.play(FadeOut(VGroup(mb, core, big, shell, wall)), run_time=0.6)
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 5.6, 1], x_length=10.2, y_length=4.4, tips=False,
                  axis_config={"include_numbers": False, "include_ticks": False, "color": GREY, "stroke_width": 3}
                  ).move_to([0.6, -0.2, 0])
        band = Rectangle(width=ax.c2p(6.5, 0)[0] - ax.c2p(3.5, 0)[0], height=ax.c2p(0, 5.6)[1] - ax.c2p(0, 0)[1],
                         stroke_width=0, fill_color=GREY, fill_opacity=0.14)
        band.move_to([(ax.c2p(3.5, 0)[0] + ax.c2p(6.5, 0)[0]) / 2, (ax.c2p(0, 5.6)[1] + ax.c2p(0, 0)[1]) / 2, 0])
        xl = VGroup(T("water", 24, GREY).move_to(ax.c2p(1.7, 0) + DOWN * 0.42),
                    T("membrane core", 24, GREY).move_to(ax.c2p(5, 0) + DOWN * 0.42),
                    T("water", 24, GREY).move_to(ax.c2p(8.3, 0) + DOWN * 0.42))
        yl = T("free energy", 26, GREY).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.3)
        self.play(Create(ax), FadeIn(band), FadeIn(xl), FadeIn(yl), run_time=1.0)

        def prof(A, col):
            return ax.plot(lambda x: A * (sig((x - 3.5) / 0.28) - sig((x - 6.5) / 0.28)),
                           x_range=[0.05, 9.95, 0.02], color=col, stroke_width=6)

        ion_c = prof(4.6, BLUE)
        self.at("costs a lot of")
        self.play(Create(ion_c), run_time=1.5)
        ion_l = T("ions", 28, BLUE).move_to(ax.c2p(7.7, 4.6), aligned_edge=LEFT)
        ion_d = DashedLine(ax.c2p(6.8, 4.6), ax.c2p(7.6, 4.6), color=BLUE, stroke_width=3)
        self.play(FadeIn(ion_l), FadeIn(ion_d), run_time=0.4)

        self.at("Hydrophobicity is the key")
        key = T("hydrophobicity is the key variable", 28, GOLD).move_to([0.6, 3.35, 0])
        self.play(FadeIn(key, shift=DOWN * 0.1), run_time=0.6)

        self.at("Indole")
        self.play(FadeOut(key), run_time=0.3)
        ind_c = prof(0.7, GREEN)
        ind_l = T("indole", 28, GREEN).move_to(ax.c2p(7.7, 0.7), aligned_edge=LEFT)
        ind_d = DashedLine(ax.c2p(6.8, 0.7), ax.c2p(7.6, 0.7), color=GREEN, stroke_width=3)
        self.play(Create(ind_c), FadeIn(ind_l), FadeIn(ind_d), run_time=1.0)
        self.at("slips through")
        d = Dot(radius=0.14, color=GREEN).move_to(ind_c.get_start())
        self.play(FadeIn(d), run_time=0.2)
        self.play(MoveAlongPath(d, ind_c), run_time=1.6, rate_func=linear)
        self.play(FadeOut(d), run_time=0.2)

        self.at("tryptophan itself")
        trp_c = prof(3.0, BLUE)
        trp_l = T("tryptophan", 28, BLUE).move_to(ax.c2p(7.7, 3.0), aligned_edge=LEFT)
        trp_d = DashedLine(ax.c2p(6.8, 3.0), ax.c2p(7.6, 3.0), color=BLUE, stroke_width=3)
        self.play(Create(trp_c), FadeIn(trp_l), FadeIn(trp_d), run_time=1.2)

        self.at("even though the ring")
        same = T("same ring, but tryptophan carries charges", 28, TEXT).move_to([0.6, 3.35, 0])
        self.play(FadeIn(same, shift=DOWN * 0.1), run_time=0.6)

        self.at("Charge is the")
        br = DoubleArrow([ax.c2p(4.2, 0.7)[0], ax.c2p(4.2, 0.7)[1] + 0.1, 0], [ax.c2p(4.2, 3.0)[0], ax.c2p(4.2, 3.0)[1] - 0.1, 0],
                         color=RED, buff=0, stroke_width=8, max_tip_length_to_length_ratio=0.2)
        brl = VGroup(T("charge is", 26, RED, weight=BOLD), T("the toll", 26, RED, weight=BOLD)).arrange(DOWN, buff=0.08).next_to(br, RIGHT, buff=0.2)
        self.play(GrowFromCenter(br), FadeIn(brl), run_time=0.8)

        # twelve decades of permeability
        self.at("Across the whole range")
        self.play(FadeOut(VGroup(ax, band, xl, yl, ion_c, ion_l, ion_d, ind_c, ind_l, ind_d, trp_c, trp_l, trp_d, same, br, brl)),
                  run_time=0.6)
        bar = Line([-5.2, -0.5, 0], [5.2, -0.5, 0], color=GREY, stroke_width=5)
        ticks = VGroup(*[Line([x, -0.5 - 0.2, 0], [x, -0.5 + 0.2, 0], color=GREY, stroke_width=4)
                         for x in np.linspace(-5.2, 5.2, 13)])
        lo = T("ions", 28, BLUE).move_to([-5.0, -1.2, 0])
        hi = T("small nonpolar molecules", 28, GREEN).move_to([3.9, -1.2, 0])
        ttl = T("permeability, log scale", 26, GREY).move_to([0, -2.2, 0])
        self.play(Create(bar), FadeIn(lo), FadeIn(hi), FadeIn(ttl), run_time=0.8)
        self.at("permeability spans")
        self.play(LaggedStart(*[GrowFromCenter(t) for t in ticks], lag_ratio=0.12), run_time=1.5)
        brace = BraceBetweenPoints([-5.2, -0.05, 0], [5.2, -0.05, 0], direction=UP, color=GOLD)
        bl = T("about 12 orders of magnitude", 30, GOLD).next_to(brace, UP, buff=0.12)
        self.at("orders of magnitude")
        self.play(GrowFromCenter(brace), FadeIn(bl), run_time=0.7)
        self.finish()


# ------------------------------------------------------------------ s02: channels, carriers, pumps
class S02Families(Sp):
    def construct(self):
        MY = 1.0
        CX = [-4.2, 0.0, 4.2]
        mb = mem(-6.3, 6.3, y=MY, th=0.8, gaps=[(c, 1.1) for c in CX])
        self.play(FadeIn(mb), run_time=0.9)
        PH = 1.6

        # channel: two blocks with a gap
        chL = Rectangle(width=0.42, height=PH, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.35)
        chR = chL.copy()
        chL.move_to([CX[0] - 0.36, MY, 0])
        chR.move_to([CX[0] + 0.36, MY, 0])
        channel = VGroup(chL, chR)
        # carrier: one block with a pocket on top
        cb = RoundedRectangle(corner_radius=0.2, width=1.0, height=PH, stroke_color=ORANGE, stroke_width=3,
                              fill_color=ORANGE, fill_opacity=0.3).move_to([CX[1], MY, 0])
        pocket = Circle(radius=0.26, stroke_width=0, fill_color=BG, fill_opacity=1).move_to([CX[1], MY + PH / 2, 0])
        carrier = VGroup(cb, pocket)
        # pump: block with a pocket on the bottom
        pb = RoundedRectangle(corner_radius=0.2, width=1.0, height=PH, stroke_color=RED, stroke_width=3,
                              fill_color=RED, fill_opacity=0.3).move_to([CX[2], MY, 0])
        ppocket = Circle(radius=0.26, stroke_width=0, fill_color=BG, fill_opacity=1).move_to([CX[2], MY - PH / 2, 0])
        pump = VGroup(pb, ppocket)

        self.at("three families")
        self.play(LaggedStart(GrowFromCenter(channel), GrowFromCenter(carrier), GrowFromCenter(pump), lag_ratio=0.5),
                  run_time=1.6)

        def title(txt, col, x):
            return T(txt, 34, col, weight=BOLD).move_to([x, 3.3, 0])

        def tags(lines, col, x):
            g = VGroup(*[T(s, 24, col) for s in lines]).arrange(DOWN, buff=0.1)
            return g.move_to([x, -1.5 - g.height / 2, 0])

        t1, t2, t3 = title("Channel", GREEN, CX[0]), title("Carrier", ORANGE, CX[1]), title("Pump", RED, CX[2])
        g1 = tags(["fastest", "~10 million ions/s", "passive", "selective by structure"], GREEN, CX[0])
        g2 = tags(["slower", "regulated", "changes shape"], ORANGE, CX[1])
        g3 = tags(["slowest", "~100 cycles/s", "spends ATP"], RED, CX[2])

        # ---- channels
        hi1 = VGroup(*[dot().move_to([CX[0] + dx, 2.0 + dy, 0]) for dx, dy in
                       [(-0.7, 0.2), (-0.1, 0.55), (0.6, 0.15), (-0.4, 0.8), (0.4, 0.75), (0.1, 0.1)]])
        lo1 = VGroup(*[dot().move_to([CX[0] + dx, -0.45, 0]) for dx in (-0.5, 0.45)])
        hl = T("high", 22, GREY).move_to([CX[0] + 1.95, 2.3, 0])
        ll = T("low", 22, GREY).move_to([CX[0] + 1.9, -0.5, 0])
        self.at("Channels are the fastest")
        self.play(FadeIn(t1), Indicate(channel, color=GREEN, scale_factor=1.12), run_time=0.8)
        self.play(FadeIn(g1[0]), run_time=0.4)
        self.at("10 million")
        self.play(FadeIn(g1[1]), FadeIn(hi1), FadeIn(lo1), FadeIn(hl), FadeIn(ll), run_time=0.7)
        self.at("but passive")
        self.play(FadeIn(g1[2]), run_time=0.4)
        self.at("They only let")
        stream = [dot(TEXT).move_to([CX[0], 2.1 + 0.45 * i, 0]) for i in range(3)]
        self.add(*stream)
        arrow1 = Arrow([CX[0] + 1.35, 2.1, 0], [CX[0] + 1.35, 0.0, 0], color=GREEN, buff=0, stroke_width=5)
        self.play(GrowArrow(arrow1), run_time=0.3)
        self.play(LaggedStart(*[d.animate.move_to([CX[0], -0.5, 0]) for i, d in enumerate(stream)],
                              lag_ratio=0.3), run_time=1.6, rate_func=linear)
        self.play(*[FadeOut(d) for d in stream], FadeOut(arrow1), run_time=0.2)
        self.at("selectivity built")
        odd = Square(side_length=0.26, stroke_color=TEXT, stroke_width=3, fill_opacity=0).move_to([CX[0] - 1.3, 2.5, 0])
        self.play(FadeIn(odd), FadeIn(g1[3]), run_time=0.3)
        self.play(odd.animate.move_to([CX[0] - 0.12, MY + PH / 2 + 0.3, 0]), run_time=0.5, rate_func=rush_into)
        self.play(odd.animate.move_to([CX[0] - 1.5, 2.9, 0]).set_opacity(0.0), run_time=0.6, rate_func=rush_from)

        # ---- carriers
        cargo2 = dot(TEXT, 0.15).move_to([CX[1] - 1.2, 1.9, 0])
        self.at("Carriers are slower")
        self.play(FadeIn(t2), Indicate(carrier, color=ORANGE, scale_factor=1.12), FadeIn(g2[0]), run_time=0.8)
        self.at("can be regulated")
        self.play(FadeIn(g2[1]), FadeIn(cargo2), run_time=0.4)
        self.play(cargo2.animate.move_to([CX[1], MY + PH / 2 - 0.02, 0]), run_time=0.6)
        self.at("They change shape")
        self.play(FadeIn(g2[2]), run_time=0.3)
        flip = VGroup(carrier, cargo2)
        self.play(Rotate(flip, angle=PI, about_point=[CX[1], MY, 0]), run_time=1.1)
        self.at("ferry their cargo")
        self.play(cargo2.animate.move_to([CX[1] + 1.2, -0.45, 0]), run_time=0.7)

        # ---- pumps
        hi3 = VGroup(*[dot().move_to([CX[2] + dx, 2.0 + dy, 0]) for dx, dy in
                       [(-0.7, 0.2), (-0.1, 0.55), (0.6, 0.15), (-0.4, 0.8), (0.4, 0.75), (0.1, 0.1)]])
        lo3 = VGroup(*[dot().move_to([CX[2] + dx, -0.45, 0]) for dx in (-0.5, 0.45)])
        cargo3 = dot(TEXT, 0.15).move_to([CX[2] - 0.55, -0.55, 0])
        self.at("Pumps are the slowest")
        self.play(FadeIn(t3), Indicate(pump, color=RED, scale_factor=1.12), FadeIn(g3[0]),
                  FadeIn(hi3), FadeIn(lo3), FadeIn(cargo3), run_time=0.8)
        self.at("100 cycles")
        self.play(FadeIn(g3[1]), run_time=0.4)
        self.at("they spend ATP")
        atp = chip("ATP", RED, 24).move_to([CX[2] + 1.3, -0.75, 0])
        self.play(FadeIn(g3[2]), FadeIn(atp), cargo3.animate.move_to([CX[2], MY - PH / 2 + 0.0, 0]), run_time=0.8)
        self.at("against their gradient")
        self.play(cargo3.animate.move_to([CX[2], MY + PH / 2 + 0.55, 0]), atp.animate.set_opacity(0.25), run_time=1.1)
        self.play(cargo3.animate.move_to([CX[2] + 0.95, 2.5, 0]), run_time=0.5)

        # ---- the three clues
        self.at("Speed regulation")
        self.play(*[Indicate(g[0], color=GOLD, scale_factor=1.15) for g in (g1, g2, g3)], run_time=0.9)
        self.at("regulation and energy")
        self.play(Indicate(g2[1], color=GOLD, scale_factor=1.2), run_time=0.8)
        self.at("energy source together")
        self.play(Indicate(g1[2], color=GOLD, scale_factor=1.2), Indicate(g3[2], color=GOLD, scale_factor=1.2),
                  run_time=0.8)
        self.at("which machine")
        self.play(*[Indicate(t, color=GOLD, scale_factor=1.2) for t in (t1, t2, t3)], run_time=1.0)
        self.finish()


# ------------------------------------------------------------------ s03: knock-on
class S03Knockon(Sp):
    SX = -2.9
    SITE = [1.65, 0.55, -0.55, -1.65]

    def construct(self):
        SX, SITE = self.SX, self.SITE
        wl = Rectangle(width=0.9, height=4.6, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                       fill_opacity=0.3).move_to([SX - 0.85, 0, 0])
        wr = wl.copy().move_to([SX + 0.85, 0, 0])
        pockets = VGroup(*[Circle(radius=0.38, stroke_color=GREY, stroke_width=3).move_to([SX, y, 0]) for y in SITE])
        labs = VGroup(*[T(f"S{i + 1}", 28, GREY).move_to([SX - 2.0, y, 0]) for i, y in enumerate(SITE)])
        outl = T("outside", 24, GREY).move_to([SX + 1.9, 3.0, 0])
        inl = T("inside", 24, GREY).move_to([SX + 1.9, -3.0, 0])
        filt = VGroup(T("K⁺ channel", 26, GREY), T("selectivity filter", 26, GREY)).arrange(DOWN, buff=0.08)
        filt.move_to([SX - 0.55, 2.95, 0], aligned_edge=RIGHT)

        self.play(FadeIn(wl), FadeIn(wr), FadeIn(outl), FadeIn(inl), FadeIn(filt), run_time=1.0)
        self.at("remarkable speed")
        zip1 = ion("K⁺", YELLOW, 0.3).move_to([SX, -3.0, 0])
        self.add(zip1)
        for _ in range(2):
            self.play(zip1.animate.move_to([SX, 3.0, 0]), run_time=0.55, rate_func=linear)
            self.play(zip1.animate.move_to([SX, -3.0, 0]).set_opacity(1), run_time=0.01)
        self.play(FadeOut(zip1), run_time=0.2)
        self.at("electrostatic")
        rep = T("electrostatic repulsion", 32, GOLD).move_to([3.3, 2.2, 0])
        self.play(FadeIn(rep, shift=DOWN * 0.1), run_time=0.7)
        pa = ion("K⁺", YELLOW, 0.3).move_to([2.7, 0.6, 0])
        pb = ion("K⁺", YELLOW, 0.3).move_to([3.9, 0.6, 0])
        pz = zig([3.05, 0.6, 0], [3.55, 0.6, 0])
        parr = VGroup(Arrow([2.3, 0.6, 0], [1.6, 0.6, 0], color=GOLD, buff=0, stroke_width=6),
                      Arrow([4.3, 0.6, 0], [5.0, 0.6, 0], color=GOLD, buff=0, stroke_width=6))
        self.play(FadeIn(pa), FadeIn(pb), run_time=0.4)
        self.play(Create(pz), GrowArrow(parr[0]), GrowArrow(parr[1]), run_time=0.6)

        self.at("Several potassium ions")
        A = ion("K⁺", YELLOW, 0.3).move_to([SX, SITE[0], 0])
        B = ion("K⁺", YELLOW, 0.3).move_to([SX, SITE[2], 0])
        self.play(FadeIn(A, scale=0.5), FadeIn(B, scale=0.5), run_time=0.8)
        self.at("four binding sites")
        self.play(Create(pockets), run_time=0.8)
        self.at("S1 through")
        self.play(LaggedStart(*[FadeIn(l) for l in labs], lag_ratio=0.35), run_time=1.5)

        # like charges repel
        self.at("Because like charges")
        z = zig([SX, SITE[2] + 0.34, 0], [SX, SITE[0] - 0.34, 0])
        self.play(Create(z), run_time=0.6)
        self.play(FadeOut(z), run_time=0.4)

        def cycle(a, b, t=1.0):
            """a at S1, b at S3. A new ion enters at S4 and the chain shifts: b to S2, a out the top."""
            c = ion("K⁺", YELLOW, 0.3).move_to([SX, -2.95, 0])
            self.play(FadeIn(c, shift=UP * 0.2), run_time=0.3 * t)
            self.play(c.animate.move_to([SX, SITE[3], 0]), run_time=0.5 * t)
            z1 = zig([SX, SITE[3] + 0.34, 0], [SX, SITE[2] - 0.34, 0])
            self.play(Create(z1), run_time=0.2 * t)
            self.play(b.animate.move_to([SX, SITE[1], 0]), FadeOut(z1), run_time=0.45 * t)
            z2 = zig([SX, SITE[1] + 0.34, 0], [SX, SITE[0] - 0.34, 0])
            self.play(Create(z2), run_time=0.2 * t)
            self.play(a.animate.move_to([SX, 3.0, 0]), FadeOut(z2), run_time=0.5 * t)
            self.play(a.animate.shift(UP * 0.5).set_opacity(0), run_time=0.3 * t)
            return c

        self.play(FadeOut(VGroup(rep, pa, pb, pz, parr)), run_time=0.3)
        self.at("the arrival of one")
        C = cycle(A, B)

        # analogy: balls in a row
        self.at("like balls knocking")
        ballx = [2.0 + 0.7 * i for i in range(5)]
        balls = VGroup(*[Circle(radius=0.3, stroke_color=TEXT, stroke_width=3, fill_color=GREY, fill_opacity=0.35)
                         .move_to([x, 0.3, 0]) for x in ballx])
        line = Line([1.2, 0.65, 0], [5.4, 0.65, 0], color=GREY, stroke_width=3)
        lab_a = T("balls on an assembly line", 28, TEXT).move_to([3.4, -0.7, 0])
        first = balls[0].copy().move_to([ballx[0] - 1.3, 0.3, 0])
        self.play(FadeIn(balls[1:]), FadeIn(line), FadeIn(lab_a), run_time=0.6)
        self.add(first)
        self.play(first.animate.move_to([ballx[0], 0.3, 0]), run_time=0.5, rate_func=rush_into)
        self.play(balls[4].animate.shift(RIGHT * 0.9), run_time=0.4, rate_func=rush_from)
        self.at_s(self.t_of("assembly line") + 0.9)
        self.play(Transform(lab_a, T("Newton's cradle", 28, TEXT).move_to([3.4, -0.7, 0])), run_time=0.5)

        # binding energy -> exit energy
        self.at("knock")
        self.play(FadeOut(VGroup(balls, first, line, lab_a)), run_time=0.5)
        e1 = chip("binding energy", YELLOW, 28).move_to([3.4, 1.7, 0])
        e2 = chip("exit energy", GREEN, 28).move_to([3.4, 0.0, 0])
        ea = Arrow(e1.get_bottom(), e2.get_top(), color=TEXT, buff=0.12, stroke_width=6)
        # the pair at S2/S4 steps up to S1/S3, ready for the next knock
        self.play(FadeIn(e1), B.animate.move_to([SX, SITE[0], 0]), C.animate.move_to([SX, SITE[2], 0]), run_time=0.5)
        self.at("directly into")
        self.play(GrowArrow(ea), FadeIn(e2), run_time=0.6)
        D = cycle(B, C, 0.55)

        self.at("so the channel is selective")
        sel = chip("selective", YELLOW, 30).move_to([2.3, -1.5, 0])
        fast = chip("fast", GREEN, 30).move_to([4.5, -1.5, 0])
        self.play(FadeIn(sel), run_time=0.5)
        self.at("and fast")
        self.play(FadeIn(fast), run_time=0.5)
        self.at("near the diffusion")
        dl = T("near the diffusion limit", 30, GREEN).move_to([3.4, -2.7, 0])
        self.play(FadeIn(dl), C.animate.move_to([SX, SITE[0], 0]), D.animate.move_to([SX, SITE[2], 0]), run_time=0.3)
        cycle(C, D, 0.5)
        self.finish()


# ------------------------------------------------------------------ s04: secondary active transport
class S04Secondary(Sp):
    def construct(self):
        MY = 0.0
        CXs, CXa, CXp = -3.6, 3.6, 0.0
        BW = 2.2
        mb = mem(-6.3, 6.3, y=MY, th=0.8, gaps=[(CXs, BW + 0.2), (CXa, BW + 0.2)])
        out_l = T("outside", 24, GREY).move_to([-5.45, 0.95, 0])
        in_l = T("inside", 24, GREY).move_to([-5.5, -0.95, 0])
        ttl = T("Secondary active transport", 38, TEXT, font=TITLE_FONT).move_to([0, 3.2, 0])
        self.play(FadeIn(mb), FadeIn(out_l), FadeIn(in_l), run_time=0.9)
        self.play(FadeIn(ttl), run_time=0.8)

        def blk(x, col, w=BW):
            return RoundedRectangle(corner_radius=0.2, width=w, height=1.7, stroke_color=col, stroke_width=3,
                                    fill_color=col, fill_opacity=0.3).move_to([x, MY, 0])

        sym, ant = blk(CXs, ORANGE), blk(CXa, ORANGE)
        slab = T("symporter", 30, ORANGE, weight=BOLD).move_to([CXs, 3.2, 0])
        alab = T("antiporter", 30, ORANGE, weight=BOLD).move_to([CXa, 3.2, 0])

        self.at("two flavors")
        self.play(GrowFromCenter(sym), GrowFromCenter(ant), run_time=0.8)

        # the sodium gradient the pump builds
        def na(x, y, r=0.27):
            return ion("Na⁺", BLUE, r, 22).move_to([x, y, 0])

        out_pos = [(-5.2, 2.2), (-5.0, 1.4), (-2.1, 1.5), (-1.5, 2.3), (-0.8, 1.4), (0.9, 1.6), (1.6, 2.3),
                   (2.2, 1.4), (5.0, 2.2), (5.3, 1.4)]
        out_na = VGroup(*[na(x, y) for x, y in out_pos])
        in_na = VGroup(na(-1.9, -1.4), na(1.9, -1.5))
        glab = T("sodium gradient: high outside, low inside", 26, BLUE).move_to([0, -3.1, 0])
        self.at("both spend the sodium")
        self.play(FadeIn(out_na, lag_ratio=0.12), FadeIn(in_na), FadeIn(glab), run_time=1.2)
        self.at("the pump builds")
        pback = Rectangle(width=1.3, height=1.0, stroke_width=0, fill_color=BG, fill_opacity=1).move_to([CXp, MY, 0])
        pmp = blk(CXp, RED, 1.2)
        pl = T("Na⁺–K⁺ pump", 26, RED).move_to([CXp, -1.6, 0])
        atp = chip("ATP", RED, 24).move_to([CXp, -2.3, 0])
        pna = na(CXp, -0.85)
        self.play(FadeIn(pback), GrowFromCenter(pmp), FadeIn(pl), FadeIn(atp), FadeIn(pna), run_time=0.6)
        self.play(pna.animate.move_to([CXp, 0.95, 0]), run_time=0.8)
        self.play(pna.animate.move_to([CXp + 0.3, 1.9, 0]), FadeOut(atp), run_time=0.4)

        # symporter
        self.at("simporters")
        self.play(FadeOut(VGroup(pl, pmp, pback, ttl, glab)), run_time=0.4)
        self.play(FadeIn(slab), Indicate(sym, color=ORANGE, scale_factor=1.08), run_time=0.7)
        self.at("same direction")
        sna = na(CXs - 0.75, 1.1)
        sgl = chip("glucose", PURPLE, 22).move_to([CXs + 0.45, 1.1, 0])
        self.play(FadeIn(sna), FadeIn(sgl), run_time=0.4)
        self.at("SGLT 1")
        sl = T("SGLT1, in the intestine", 24, ORANGE).move_to([CXs, -1.9, 0])
        self.play(FadeIn(sl), run_time=0.5)
        self.at("drags glucose uphill")
        gl_l = T("glucose moves uphill", 24, PURPLE).move_to([CXs, -2.5, 0])
        self.play(sgl.animate.move_to([CXs + 0.5, -1.1, 0]), sna.animate.move_to([CXs - 0.75, -1.1, 0]),
                  FadeIn(gl_l), run_time=1.5)
        self.at("riding sodium downhill")
        na_l = T("sodium moves downhill", 24, BLUE).move_to([CXs, -3.1, 0])
        self.play(FadeIn(na_l), Indicate(sna, color=BLUE, scale_factor=1.3), run_time=0.8)

        # antiporter
        self.at("anti porters")
        self.play(FadeIn(alab), run_time=0.4)
        self.play(Indicate(ant, color=ORANGE, scale_factor=1.08), run_time=0.6)
        self.at("opposite directions")
        ana = na(CXa - 0.65, 1.1)
        aca = ion("Ca²⁺", PURPLE, 0.34, 22).move_to([CXa + 0.65, -1.1, 0])
        self.play(FadeIn(ana), FadeIn(aca), run_time=0.4)
        self.at("the cardiac sodium")
        al = T("cardiac Na⁺–Ca²⁺ exchanger", 24, ORANGE).move_to([CXa, -1.9, 0])
        self.play(FadeIn(al), run_time=0.6)
        self.at("pushes calcium out")
        ca_l = T("calcium moves uphill", 24, PURPLE).move_to([CXa, -2.5, 0])
        self.play(ana.animate.move_to([CXa - 0.65, -1.1, 0]), aca.animate.move_to([CXa + 0.65, 1.1, 0]),
                  FadeIn(ca_l), run_time=1.6)
        self.at("the inward sodium flow")
        an_l = T("sodium moves downhill", 24, BLUE).move_to([CXa, -3.1, 0])
        self.play(FadeIn(an_l), Indicate(ana, color=BLUE, scale_factor=1.3), run_time=0.8)

        # no ATP here
        self.at("Neither one burns")
        self.play(FadeOut(VGroup(sl, gl_l, na_l, al, ca_l, an_l)), run_time=0.4)
        no1 = VGroup(chip("ATP", RED, 26).move_to([CXs, -2.2, 0]), chip("ATP", RED, 26).move_to([CXa, -2.2, 0]))
        crosses = VGroup(*[Cross(c, stroke_color=RED, stroke_width=7).scale(0.9) for c in no1])
        self.play(FadeIn(no1), run_time=0.3)
        self.play(Create(crosses), run_time=0.5)
        self.at("borrow the energy")
        self.play(FadeOut(VGroup(no1, crosses)), run_time=0.4)
        glab2 = T("energy stored in the sodium gradient", 28, BLUE).move_to([0, -3.0, 0])
        self.play(FadeIn(glab2), *[Indicate(m, color=BLUE, scale_factor=1.25) for m in out_na], run_time=1.0)

        # waterwheel
        self.at("like a waterwheel")
        everything = VGroup(mb, out_l, in_l, sym, ant, slab, alab, out_na, in_na, sna, sgl, ana, aca, glab2, pna)
        self.play(FadeOut(everything), run_time=0.6)
        WC = np.array([0.6, 0.1, 0])
        hub = Circle(radius=0.2, stroke_color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=1)
        angs = np.linspace(0, TAU, 9)[:-1]
        spokes = VGroup(*[Line(ORIGIN, 1.3 * np.array([np.cos(a), np.sin(a), 0]), color=GREY, stroke_width=6)
                          for a in angs])
        paddles = VGroup(*[Rectangle(width=0.6, height=0.24, stroke_width=0, fill_color=GREY, fill_opacity=1)
                           .rotate(a).move_to(1.3 * np.array([np.cos(a), np.sin(a), 0])) for a in angs])
        rim = Circle(radius=1.3, stroke_color=GREY, stroke_width=4)
        load = Circle(radius=0.26, stroke_width=0, fill_color=PURPLE, fill_opacity=1)
        load.move_to(1.68 * np.array([np.cos(-0.55), np.sin(-0.55), 0]))
        wheel = VGroup(rim, spokes, paddles, hub, load).move_to(WC)
        cur = VGroup(*[Arrow([-4.9, 3.1 - 0.55 * i, 0], [-1.35, 1.7 - 0.55 * i, 0], color=BLUE, buff=0,
                             stroke_width=6) for i in range(3)])
        cl = T("sodium flowing downhill", 28, BLUE).move_to([-3.6, -0.5, 0])
        ll = T("cargo lifted uphill", 28, PURPLE).move_to([4.3, 1.9, 0])
        self.at("waterwheel")
        self.play(FadeIn(wheel), run_time=0.5)
        self.play(FadeIn(cur, lag_ratio=0.3), FadeIn(cl), FadeIn(ll), run_time=0.8)
        self.play(Rotate(wheel, angle=PI / 2, about_point=WC, rate_func=linear), run_time=1.4)

        # everything depends on the pump
        self.at("Every one of them")
        self.play(FadeOut(VGroup(wheel, cur, cl, ll)), run_time=0.5)
        chain = VGroup(chip("Na⁺–K⁺ pump (spends ATP)", RED, 28),
                       chip("sodium gradient", BLUE, 28),
                       chip("symporters and antiporters", ORANGE, 28)).arrange(UP, buff=0.9).move_to([0, 0.0, 0])
        arrs = VGroup(*[Arrow(chain[i].get_top(), chain[i + 1].get_bottom(), color=TEXT, buff=0.1, stroke_width=6)
                        for i in range(2)])
        self.play(FadeIn(chain[0], shift=UP * 0.1), run_time=0.5)
        self.at("ultimately depends")
        self.play(GrowArrow(arrs[0]), FadeIn(chain[1]), run_time=0.6)
        self.play(GrowArrow(arrs[1]), FadeIn(chain[2]), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------ s05: decision tree
class S05Tree(Sp):
    def construct(self):
        QX = -3.9
        RX = 3.15

        def result(title, sub, col, y):
            t = T(title, 28, col, weight=BOLD)
            s = T(sub, 24, TEXT)
            g = VGroup(t, s).arrange(DOWN, buff=0.1)
            box = RoundedRectangle(corner_radius=0.16, width=6.2, height=g.height + 0.35, stroke_color=col,
                                   stroke_width=3, fill_color=col, fill_opacity=0.14)
            g.move_to(box)
            return VGroup(box, g).move_to([RX, y, 0])

        def q(text, y):
            return chip(text, TEXT, 28).move_to([QX, y, 0])

        def lab(txt, col, pos):
            return T(txt, 24, col).move_to(pos)

        y1, y2, y3 = 1.8, 0.2, -1.9
        top = T("a molecule that must cross", 26, GREY).move_to([QX, 2.95, 0])
        Q1 = q("small and nonpolar?", y1)
        Q2 = q("downhill or uphill?", y2)
        Q3 = q("what powers it?", y3)
        R1 = result("simple diffusion", "O₂ into a red blood cell", GREEN, y1)
        R2 = result("facilitated diffusion", "through a channel or carrier", GREEN, y2)
        R3 = result("primary active: a pump", "ATP, directly", RED, -1.15)
        R4 = result("secondary active", "symporter or antiporter", ORANGE, -2.75)

        def arr(a, b, col=TEXT):
            return Arrow(a, b, color=col, buff=0.08, stroke_width=5)

        a0 = arr(top.get_bottom(), Q1.get_top())
        a1 = arr(Q1.get_right(), R1.get_left(), GREEN)
        a1b = arr(Q1.get_bottom(), Q2.get_top())
        a2 = arr(Q2.get_right(), R2.get_left(), GREEN)
        a2b = arr(Q2.get_bottom(), Q3.get_top(), RED)
        a3 = arr(Q3.get_right() + UP * 0.1, R3.get_left(), RED)
        a3b = arr(Q3.get_right() + DOWN * 0.1, R4.get_left(), ORANGE)
        l1 = lab("yes", GREEN, (a1.get_center() + UP * 0.3))
        l1b = lab("no", TEXT, a1b.get_center() + RIGHT * 0.45)
        l2 = lab("downhill", GREEN, a2.get_center() + UP * 0.3 + LEFT * 0.2)
        l2b = lab("uphill", RED, a2b.get_center() + RIGHT * 0.65)
        l3 = lab("ATP", RED, a3.get_center() + UP * 0.32 + LEFT * 0.1)
        l3b = lab("ion gradient", ORANGE, a3b.get_center() + DOWN * 0.5 + LEFT * 0.55)

        head = T("A transport decision tree", 44, TEXT, font=TITLE_FONT).move_to([0, 0.3, 0])
        self.play(FadeIn(head, shift=UP * 0.15), run_time=0.9)
        self.at("First ask whether")
        self.play(FadeOut(head), run_time=0.4)
        self.play(FadeIn(top, shift=DOWN * 0.1), run_time=0.5)
        self.play(GrowArrow(a0), run_time=0.3)
        self.at("small and non polar")
        self.play(FadeIn(Q1), run_time=0.6)
        self.at("it simply diffuses")
        self.play(GrowArrow(a1), FadeIn(l1), FadeIn(R1[0]), FadeIn(R1[1][0]), run_time=0.7)
        self.at("like oxygen")
        self.play(FadeIn(R1[1][1]), run_time=0.6)

        self.at("If it needs help")
        self.play(GrowArrow(a1b), FadeIn(l1b), run_time=0.6)
        self.at("which direction")
        self.play(FadeIn(Q2), run_time=0.6)
        self.at("Downhill")
        self.play(GrowArrow(a2), FadeIn(l2), FadeIn(R2), run_time=0.9)
        self.at("Uphill")
        self.play(GrowArrow(a2b), FadeIn(l2b), run_time=0.6)
        self.at("active transport")
        self.play(FadeIn(Q3), run_time=0.6)
        self.at("directly by ATP")
        self.play(GrowArrow(a3), FadeIn(l3), FadeIn(R3), run_time=0.9)
        self.at("indirectly by")
        self.play(GrowArrow(a3b), FadeIn(l3b), FadeIn(R4), run_time=0.9)

        self.at("Three questions")
        nums = VGroup(*[Circle(radius=0.26, stroke_color=GOLD, stroke_width=3, fill_color=BG, fill_opacity=1)
                        .move_to(Q.get_left() + LEFT * 0.0) for Q in (Q1, Q2, Q3)])
        bx = min(Q.get_left()[0] for Q in (Q1, Q2, Q3)) - 0.42
        for n, Q, i in zip(nums, (Q1, Q2, Q3), "123"):
            n.move_to([bx, Q.get_center()[1], 0])
            n.add(T(i, 24, GOLD).move_to(n))
        self.play(LaggedStart(*[GrowFromCenter(n) for n in nums], lag_ratio=0.45), run_time=1.4)
        self.play(*[Indicate(Q, color=GOLD, scale_factor=1.08) for Q in (Q1, Q2, Q3)], run_time=0.9)
        self.finish()
