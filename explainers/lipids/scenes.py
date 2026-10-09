"""Shape is destiny: how tails set melting point and membrane fluidity  (Biochemistrypedia lipids explainer)

Four narrated slide clips, one arc: a fatty acid's shape sets its melting point (s01) -> the same rule
decides whether a fat is solid or liquid (s02) -> and whether a membrane is gel or fluid, which a cell
tunes (s03) -> with cholesterol as the two-way buffer (s04).

COLOR MAP (one color per concept, whole video)
  BLUE   = saturated tails: straight, tightly packed, solid / gel
  YELLOW = cis-unsaturated tails: kinked, loosely packed, liquid / fluid
  RED    = temperature: room / body lines, thermometers, "transition temperature" text
  GREEN  = cholesterol
  GREY   = axes, glycerol backbone, lipid heads, de-emphasized text
  GOLD   = one highlight frame only
Tails are drawn as thick schematic lines (straight or with a kink) - packing cartoons, never atom-level structures.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

config.disable_caching = True


# ---------------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------------
def tail(p0, length, direction=RIGHT, kink_at=(), amp=0.13, hump=0.34, color=BLUE, stroke=8):
    """Schematic acyl tail: a straight thick line, with one hump per cis double bond."""
    d = np.array(direction, float)
    n = np.array([-d[1], d[0], 0.0])
    p0 = np.array(p0, float)
    pts = [p0]
    for f in kink_at:
        a = max(0.0, min(length - hump, f * length - hump / 2))
        pts += [p0 + d * a, p0 + d * (a + hump / 2) + n * amp, p0 + d * (a + hump)]
    pts.append(p0 + d * length)
    m = VMobject(stroke_color=color, stroke_width=stroke, fill_opacity=0,
                 cap_style=CapStyleType.ROUND, joint_type=LineJointType.ROUND)
    m.set_points_as_corners(pts)
    return m


def wavy(p0, length, direction, A, cycles=2.5, phase=0.0, color=BLUE, stroke=8, N=36):
    d = np.array(direction, float)
    n = np.array([-d[1], d[0], 0.0])
    p0 = np.array(p0, float)
    pts = [p0 + d * (length * i / N) + n * A * np.sin(2 * np.pi * cycles * i / N + phase) for i in range(N + 1)]
    m = VMobject(stroke_color=color, stroke_width=stroke, fill_opacity=0,
                 cap_style=CapStyleType.ROUND, joint_type=LineJointType.ROUND)
    m.set_points_as_corners(pts)
    return m


def lab(text, size=22, color=GREY):
    return M(text, size, color)


def head_dot(p, r=0.13):
    return Circle(radius=r, stroke_width=0, fill_color=GREY, fill_opacity=1).move_to(p)


def lipid_v(x, yh, d, kind, i=0, L=1.0, spread=0.075, bend=1, stroke=6, r=0.13):
    """Two-tailed membrane lipid, head at (x, yh), tails running in direction d (DOWN or UP).
    kind: 'S' straight blue, 'U' kinked yellow (both tails kink the same way; bend = -1 left / +1 right on screen)."""
    head = head_dot([x, yh, 0], r)
    flip = 1 if d[1] < 0 else -1          # the tail's own normal points right for DOWN, left for UP
    tails = []
    for j, dx in enumerate((-spread, spread)):
        p0 = [x + dx, yh + d[1] * 0.1, 0]
        if kind == "S":
            tails.append(tail(p0, L, d, color=BLUE, stroke=stroke))
        else:
            f = 0.36 + 0.1 * (i % 2)
            tails.append(tail(p0, L, d, kink_at=[f], amp=0.17 * bend * flip, hump=0.42, color=YELLOW, stroke=stroke))
    return VGroup(head, *tails)


def bilayer(cx, kinds, spacing, ytop=1.45, ybot=-1.25, L=1.1):
    """Cross-section: top leaflet (tails down) and bottom leaflet (tails up). Returns (group, lipids)."""
    n = len(kinds)
    xs = [cx + (k - (n - 1) / 2) * spacing for k in range(n)]
    lips = []
    for k, (x, kd) in enumerate(zip(xs, kinds)):
        lips.append(lipid_v(x, ytop, DOWN, kd, i=k, L=L, bend=-1 if k % 2 == 0 else 1))
    for k, (x, kd) in enumerate(zip(xs, kinds)):
        lips.append(lipid_v(x, ybot, UP, kd, i=k + 1, L=L, bend=1 if k % 2 == 0 else -1))
    return VGroup(*lips), lips


def start_wiggle(scene, mobs, amp_x=0.05, amp_y=0.035):
    for k, m in enumerate(mobs):
        m._off = np.zeros(3)
        m._ph = 0.9 * k + 0.4 * (k % 3)

        def upd(mm, dt, scene=scene):
            t = scene.elapsed()
            off = np.array([amp_x * np.sin(2.6 * t + mm._ph), amp_y * np.sin(3.3 * t + 1.7 * mm._ph), 0.0])
            mm.shift(off - mm._off)
            mm._off = off
        m.add_updater(upd)


def stop_wiggle(mobs):
    for m in mobs:
        m.clear_updaters()
        if hasattr(m, "_off"):
            m.shift(-m._off)
            m._off = np.zeros(3)


def thermo(x, y0, h, tr, lo=0.0, hi=45.0):
    """Vertical thermometer driven by a ValueTracker (degrees C). Returns (outline, fill, label)."""
    tube = RoundedRectangle(width=0.34, height=h, corner_radius=0.17, stroke_color=GREY, stroke_width=3,
                            fill_opacity=0).move_to([x, y0 + h / 2, 0])
    bulb = Circle(radius=0.3, stroke_color=GREY, stroke_width=3, fill_color=RED, fill_opacity=0.9).move_to([x, y0 - 0.1, 0])

    def mk():
        hh = max(0.06, (h - 0.1) * (tr.get_value() - lo) / (hi - lo))
        return Rectangle(width=0.16, height=hh, stroke_width=0, fill_color=RED, fill_opacity=0.95).move_to([x, y0 + hh / 2, 0])

    fill = always_redraw(mk)
    label = always_redraw(lambda: M(f"{tr.get_value():.0f} °C", 28, RED).next_to(tube, RIGHT, buff=0.3))
    return VGroup(tube, bulb), fill, label


def label_row(*mobs, buff=0.3):
    return VGroup(*mobs).arrange(RIGHT, buff=buff)


# ---------------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Lipids"
    TITLE = "Shape is destiny"


# ---------------------------------------------------------------------------------------------------
class S01Melting(SpokenScene):
    """Melting point vs chain length (blue) and cis kinks (yellow), built row by row as each fatty acid is named."""

    def construct(self):
        X0, SC = 0.4, 0.048
        tx = lambda t: X0 + (t + 20) * SC
        AY = -2.3

        head = T("What makes a fat solid or liquid?", 38, font=TITLE_FONT).move_to([0, 3.4, 0])
        self.play(FadeIn(head, shift=UP * 0.1), run_time=0.7)

        # axis (melting point, deg C), drawn once, rows hang off it
        axis = Line([tx(-20), AY, 0], [tx(80), AY, 0], color=GREY, stroke_width=3)
        ticks = VGroup()
        for v in (-20, 0, 20, 40, 60, 80):
            ticks.add(Line([tx(v), AY, 0], [tx(v), AY - 0.1, 0], color=GREY, stroke_width=3))
            ticks.add(lab(str(v), 22).move_to([tx(v), AY - 0.38, 0]))
        axtitle = T("melting point (°C)", 24, GREY).move_to([tx(30), AY - 0.85, 0])
        zero = DashedLine([tx(0), 1.6, 0], [tx(0), AY, 0], color=GREY, stroke_width=2, dash_length=0.1).set_opacity(0.6)
        axisg = VGroup(axis, ticks, axtitle, zero)

        chip1 = chip("chain length", BLUE, 28)
        chip1.move_to([-6.0 + chip1.width / 2, 2.7, 0])
        cap1 = T("longer chains, higher melting point", 26, TEXT).next_to(chip1, RIGHT, buff=0.35)

        # rows
        specs = [("Lauric", "12:0", 12, [], 44, BLUE), ("Palmitic", "16:0", 16, [], 63, BLUE),
                 ("Stearic", "18:0", 18, [], 70, BLUE), ("Oleic", "18:1", 18, [0.5], 13, YELLOW),
                 ("Linolenic", "18:3", 18, [0.5, 0.67, 0.83], -11, YELLOW)]
        ys = [1.2, 0.5, -0.2, -0.9, -1.6]
        rows = []
        for (nm, code, n, kinks, v, col), y in zip(specs, ys):
            name = label_row(T(nm, 26, TEXT), lab(code, 22, GREY), buff=0.18)
            name.move_to([-6.0 + name.width / 2, y, 0])
            hd = head_dot([-3.2, y, 0], 0.1)
            tl = tail([-3.1, y, 0], n * 0.16, RIGHT, kink_at=kinks, amp=0.17, hump=0.5 if len(kinks) < 2 else 0.42, color=col, stroke=9)
            glyph = VGroup(hd, tl)
            bw = abs(v) * SC
            bar = Rectangle(width=bw, height=0.34, stroke_width=0, fill_color=col, fill_opacity=0.85)
            val = lab(f"{v} °C", 24, TEXT)
            if v >= 0:
                bar.move_to([tx(0) + bw / 2, y, 0])
            else:
                bar.move_to([tx(0) - bw / 2, y, 0])
            # left edge of the value label: just past the bar, or past the 20 °C room line for low melters
            xl = (tx(0) + bw + 0.2) if v > 25 else (tx(20) + 0.25)
            val.move_to([xl + val.width / 2, y, 0])
            val = VGroup(BackgroundRectangle(val, color=BG, fill_opacity=1, buff=0.06, stroke_width=0), val).set_z_index(6)
            rows.append(dict(name=name, glyph=glyph, bar=bar, val=val, v=v, y=y, col=col))

        # --- narration cues ---------------------------------------------------------------------
        self.at("First chain length")
        self.play(FadeIn(axisg), FadeIn(chip1, shift=RIGHT * 0.2), run_time=0.9)

        self.at("longer chains pack more tightly")
        self.play(LaggedStart(*[AnimationGroup(FadeIn(r["name"]), Create(r["glyph"])) for r in rows[:3]],
                              lag_ratio=0.35), run_time=1.5)

        self.at("melt higher")
        self.play(FadeIn(cap1, shift=RIGHT * 0.2), run_time=0.5)

        for key, r, edge in (("Loric acid at 12", rows[0], LEFT), ("palmitic at 16", rows[1], LEFT),
                             ("steric at 18", rows[2], LEFT)):
            self.at(key)
            self.play(GrowFromEdge(r["bar"], edge), FadeIn(r["val"]), run_time=0.7)

        # --- saturation: copy the straight stearic tail and kink it -----------------------------
        self.at("Second saturation")
        chip2 = chip("saturation", YELLOW, 28).move_to(chip1)
        chip2.move_to([-6.0 + chip2.width / 2, 2.7, 0])
        self.play(ReplacementTransform(chip1, chip2), FadeOut(cap1), run_time=0.7)

        self.at("One cis double bond")
        ghost = rows[2]["glyph"].copy()
        self.add(ghost)
        self.play(ReplacementTransform(ghost, rows[3]["glyph"]), run_time=1.3)
        cap2 = T("a kink breaks the packing", 26, TEXT).next_to(chip2, RIGHT, buff=0.35)
        self.at("breaks the packing")
        self.play(FadeIn(cap2, shift=RIGHT * 0.2), run_time=0.5)

        self.at("Steric acid is a solid")
        self.play(Indicate(rows[2]["bar"], color=BLUE, scale_factor=1.12), run_time=0.8)

        self.at("Oleic acid")
        self.play(FadeIn(rows[3]["name"]), run_time=0.4)
        self.at("melts at just 13")
        self.play(GrowFromEdge(rows[3]["bar"], LEFT), FadeIn(rows[3]["val"]), run_time=0.7)

        self.at("pours as an oil")
        room = DashedLine([tx(20), 1.55, 0], [tx(20), AY, 0], color=RED, stroke_width=3, dash_length=0.12)
        room_l = T("room temperature, 20 °C", 24, RED).move_to([tx(20) + 1.7, 1.78, 0])
        self.play(Create(room), FadeIn(room_l), run_time=0.8)

        self.at("More double bonds")
        ghost2 = rows[3]["glyph"].copy()
        self.add(ghost2)
        cap3 = T("more kinks, lower melting point", 26, TEXT).next_to(chip2, RIGHT, buff=0.35)
        self.play(ReplacementTransform(ghost2, rows[4]["glyph"]), FadeIn(rows[4]["name"]),
                  ReplacementTransform(cap2, cap3), run_time=0.9)
        self.at("drop it further")
        self.play(GrowFromEdge(rows[4]["bar"], RIGHT), FadeIn(rows[4]["val"]), run_time=0.8)

        self.at("whole chapter in one graph")
        frame = RoundedRectangle(corner_radius=0.2, width=12.5, height=5.75, stroke_color=GOLD, stroke_width=3)
        frame.move_to([0, -0.6, 0])
        head2 = T("Shape is destiny", 42, font=TITLE_FONT).move_to(head)
        self.play(Create(frame), ReplacementTransform(head, head2), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------------
class S02Tag(SpokenScene):
    """Three triacylglycerols: which tails hang off glycerol sets whether the fat is solid, semi-solid or liquid."""

    def construct(self):
        tx = lambda t: -5.5 + (t + 10) * 0.1375
        AY = -2.35
        ROWS = [2.2, 1.55, 0.9]
        PX = 1.3          # backbone offset left of card center
        U = 0.125         # tail length per carbon

        heading = T("Same glycerol, different tails", 36, font=TITLE_FONT).move_to([0, 3.4, 0])
        self.play(FadeIn(heading, shift=UP * 0.1), run_time=0.7)

        # axis
        axis = Line([tx(-10), AY, 0], [tx(70), AY, 0], color=GREY, stroke_width=3)
        ticks = VGroup()
        for v in range(-10, 71, 10):
            ticks.add(Line([tx(v), AY, 0], [tx(v), AY - 0.1, 0], color=GREY, stroke_width=3))
            ticks.add(lab(str(v), 22).move_to([tx(v), AY - 0.38, 0]))
        axtitle = T("melting point (°C)", 24, GREY).move_to([0, AY - 0.85, 0])
        axisg = VGroup(axis, ticks, axtitle)

        def make_card(cx, specs, name):
            back = Line([cx - PX, ROWS[0] + 0.28, 0], [cx - PX, ROWS[2] - 0.28, 0], color=GREY, stroke_width=11,
                        cap_style=CapStyleType.ROUND)
            tails, labs, grp = [], [], []
            for (n, kinks, col, code), y in zip(specs, ROWS):
                t = tail([cx - PX, y, 0], n * U, RIGHT, kink_at=kinks, amp=0.12, hump=0.34, color=col, stroke=9)
                l = lab(code, 22).move_to([cx - PX + n * U + 0.5, y, 0])
                tails.append(t)
                labs.append(l)
                grp.append(VGroup(t, l))
            nm = T(name, 28, TEXT).move_to([cx, 0.25, 0])
            return dict(back=back, tails=tails, labs=labs, grp=grp, name=nm, cx=cx)

        PAL = ("", 16, [], BLUE, "16:0")
        palm = make_card(4.2, [(16, [], BLUE, "16:0")] * 3, "Tripalmitin")
        olei = make_card(-4.2, [(18, [0.5], YELLOW, "18:1")] * 3, "Triolein")
        mixd = make_card(0.0, [(16, [], BLUE, "16:0"), (18, [0.5], YELLOW, "18:1"),
                               (18, [0.5, 0.67, 0.83], YELLOW, "18:3")], "mixed")

        # reference lines + markers
        body = DashedLine([tx(37), -1.3, 0], [tx(37), AY, 0], color=RED, stroke_width=3, dash_length=0.12)
        body_l = T("body 37 °C", 24, RED).move_to([tx(37) + 0.15 + 0.85, -1.0, 0])
        room = DashedLine([tx(20), -1.3, 0], [tx(20), AY, 0], color=RED, stroke_width=3, dash_length=0.12)
        room_l = T("room 20 °C", 24, RED).move_to([tx(20) - 0.1 - 0.85, -1.0, 0])

        def marker(v, col):
            dot = Dot([tx(v), AY, 0], radius=0.15, color=col)
            lb = lab(f"{v} °C", 24, TEXT).move_to([tx(v), AY + 0.5, 0])
            return VGroup(dot, lb)

        m_palm = marker(66, BLUE)
        m_olei = marker(5, YELLOW)
        rng = Rectangle(width=tx(40) - tx(25), height=0.3, stroke_width=0)
        rng.set_fill(color=[BLUE, YELLOW], opacity=0.9).move_to([(tx(25) + tx(40)) / 2, AY, 0])
        rng_l = T("melts over a range", 24, GREY).move_to([(tx(25) + tx(40)) / 2, AY + 0.5, 0])
        rng_l = VGroup(BackgroundRectangle(rng_l, color=BG, fill_opacity=1, buff=0.06, stroke_width=0), rng_l).set_z_index(6)

        chip_solid = chip("SOLID", BLUE, 26).move_to([palm["cx"], -0.4, 0])
        chip_liq = chip("LIQUID", YELLOW, 26).move_to([olei["cx"], -0.4, 0])
        chip_semi = chip("SEMI-SOLID", TEXT, 26).move_to([mixd["cx"], -0.4, 0])

        # --- cues -------------------------------------------------------------------------------
        self.at("which fatty acids hang off")
        gly = T("glycerol", 24, GREY).move_to([palm["cx"] - PX, ROWS[0] + 0.62, 0])
        self.play(Create(palm["back"]), FadeIn(axisg), run_time=0.8)
        self.at("glycerol.")
        self.play(FadeIn(gly), run_time=0.5)

        self.at("Trypalmitin")
        self.play(FadeIn(palm["name"]), run_time=0.5)
        self.at("three saturated")
        self.play(LaggedStart(*[Create(t) for t in palm["tails"]], lag_ratio=0.3),
                  LaggedStart(*[FadeIn(l) for l in palm["labs"]], lag_ratio=0.3), run_time=1.4)
        self.at("packs tightly")
        self.play(Indicate(VGroup(*palm["tails"]), color=BLUE, scale_factor=1.04), run_time=0.8)
        self.at("solid at body temperature")
        self.play(FadeIn(chip_solid), Create(body), FadeIn(body_l), run_time=0.8)
        self.play(FadeIn(m_palm, scale=0.5), run_time=0.6)

        self.at("Triolin")
        self.play(FadeOut(gly), Create(olei["back"]), FadeIn(olei["name"]), run_time=0.6)
        self.at("three unsaturated")
        self.play(LaggedStart(*[Create(t) for t in olei["tails"]], lag_ratio=0.3),
                  LaggedStart(*[FadeIn(l) for l in olei["labs"]], lag_ratio=0.3), run_time=1.4)
        self.at("stays liquid even")
        self.play(FadeIn(chip_liq), FadeIn(m_olei, scale=0.5), run_time=0.7)
        self.at("room temperature")
        self.play(Create(room), FadeIn(room_l), run_time=0.8)

        self.at("A mixed triacylglycerol")
        self.play(Create(mixd["back"]), FadeIn(mixd["name"]), run_time=0.6)
        self.at("one saturated chain")
        self.play(Create(mixd["tails"][0]), FadeIn(mixd["labs"][0]), run_time=0.7)
        self.at("two unsaturated")
        self.play(Create(mixd["tails"][1]), FadeIn(mixd["labs"][1]), run_time=0.6)
        self.play(Create(mixd["tails"][2]), FadeIn(mixd["labs"][2]), run_time=0.6)
        self.at("lands in between")
        self.play(GrowFromCenter(rng), FadeIn(rng_l), run_time=0.8)
        self.at("semi solid")
        self.play(FadeIn(chip_semi), run_time=0.5)
        self.at("around body temperature")
        self.play(Indicate(body, color=RED, scale_factor=1.0), Indicate(rng, color=TEXT, scale_factor=1.15), run_time=0.8)

        self.at("profile of most natural body fat")
        frame = RoundedRectangle(corner_radius=0.18, width=4.1, height=3.55, stroke_color=GOLD, stroke_width=3)
        frame.move_to([mixd["cx"] + 0.25, 0.95, 0])
        head2 = T("Most body fat is a mixture", 36, font=TITLE_FONT).move_to(heading)
        self.play(Create(frame), ReplacementTransform(heading, head2), run_time=0.9)

        self.at("fine tune the physical state")
        head3 = T("Cells choose which tail goes where", 36, font=TITLE_FONT).move_to(heading)
        self.play(FadeOut(frame), ReplacementTransform(head2, head3), run_time=0.7)

        self.at("choosing which fatty acid")
        g0, g1 = mixd["grp"][0], mixd["grp"][1]
        dy = ROWS[1] - ROWS[0]
        self.play(g0.animate.shift(UP * dy), g1.animate.shift(DOWN * dy), run_time=1.0)

        self.at("position on glycerol")
        sn = VGroup(*[T(f"sn-{i + 1}", 24, TEXT).move_to([mixd["cx"] - PX - 0.5, y, 0]) for i, y in enumerate(ROWS)])
        others = VGroup(palm["back"], *palm["tails"], *palm["labs"], palm["name"], chip_solid,
                        olei["back"], *olei["tails"], *olei["labs"], olei["name"], chip_liq)
        self.play(FadeIn(sn, shift=RIGHT * 0.15), FadeOut(others), m_palm.animate.set_opacity(0.3), m_olei.animate.set_opacity(0.3), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------------
class S03Fluidity(SpokenScene):
    """Saturation as the membrane's fluidity dial; E. coli retunes it when chilled (homeoviscous adaptation)."""

    def construct(self):
        # ---- dial (slider) -----------------------------------------------------------------------
        heading = T("Saturation is the membrane's fluidity dial", 34, font=TITLE_FONT).move_to([0, 3.4, 0])
        self.play(FadeIn(heading, shift=UP * 0.1), run_time=0.7)

        SY = 2.6
        track = Line([-2.6, SY, 0], [2.6, SY, 0], color=GREY, stroke_width=6, cap_style=CapStyleType.ROUND)
        end_l = T("saturated", 24, BLUE).next_to(track, LEFT, buff=0.55)
        end_r = T("unsaturated", 24, YELLOW).next_to(track, RIGHT, buff=0.55)
        knob = Circle(radius=0.2, stroke_color=TEXT, stroke_width=3, fill_color=BG, fill_opacity=1).move_to([0, SY, 0]).set_z_index(5)
        dial = VGroup(track, end_l, end_r, knob)
        self.at("main dial a cell turns")
        self.play(FadeIn(dial), run_time=0.7)

        # ---- left: saturated bilayer ---------------------------------------------------------------
        LX, RX = -3.45, 3.45
        sat_grp, sat_lips = bilayer(LX, ["S"] * 9, 0.62)
        uns_grp, uns_lips = bilayer(RX, ["U"] * 6, 0.95)

        self.at("Saturated tails pack tightly")
        l1 = T("saturated tails", 28, BLUE).move_to([LX, -1.95, 0])
        self.play(knob.animate.move_to([-2.35, SY, 0]), FadeIn(sat_grp), run_time=0.9)
        self.play(FadeIn(l1, shift=UP * 0.1), run_time=0.4)

        self.at("van der Waals' contacts")
        arrows = VGroup()
        for k in (1, 3, 5, 7):
            xa = LX + (k - 4 + 0.5) * 0.62
            for yy in (0.95, 0.6):
                arrows.add(DoubleArrow([xa - 0.15, yy, 0], [xa + 0.15, yy, 0], buff=0, color=TEXT, stroke_width=3,
                                       max_tip_length_to_length_ratio=0.5, tip_length=0.09))
        vdw = T("strong van der Waals contacts", 24, TEXT).move_to([LX, -2.5, 0])
        self.play(FadeIn(vdw, shift=UP * 0.1), LaggedStart(*[GrowFromCenter(a) for a in arrows], lag_ratio=0.1), run_time=1.0)

        self.at("raising the transition temperature")
        tm_hi = T("higher transition temperature", 24, RED).move_to([LX - 0.5, -3.1, 0])
        self.play(FadeIn(tm_hi, shift=UP * 0.1), run_time=0.6)
        self.at("toward a gel")
        gel = chip("gel", BLUE, 26).next_to(tm_hi, RIGHT, buff=0.3)
        self.play(FadeIn(gel, scale=0.8), run_time=0.5)

        # ---- right: unsaturated bilayer ------------------------------------------------------------
        self.at("Unsaturated tails kink")
        l2 = T("unsaturated (cis) tails", 28, YELLOW).move_to([RX, -1.95, 0])
        self.play(knob.animate.move_to([2.35, SY, 0]), FadeIn(uns_grp), run_time=0.9)
        self.play(FadeIn(l2, shift=UP * 0.1), run_time=0.4)

        self.at("packing defects")
        defects = VGroup()
        xs_u = [RX + (k - 2.5) * 0.95 for k in range(6)]
        for gx, gy in (((xs_u[0] + xs_u[1]) / 2, 0.8), ((xs_u[2] + xs_u[3]) / 2, 0.8), ((xs_u[4] + xs_u[5]) / 2, 0.8),
                       ((xs_u[1] + xs_u[2]) / 2, -0.6), ((xs_u[3] + xs_u[4]) / 2, -0.6)):
            defects.add(DashedVMobject(Ellipse(width=0.62, height=0.95, color=TEXT, stroke_width=3).move_to([gx, gy, 0]),
                                       num_dashes=16))
        dfx = T("packing defects", 24, TEXT).move_to([RX, -2.5, 0])
        self.play(FadeIn(dfx, shift=UP * 0.1), LaggedStart(*[Create(d) for d in defects], lag_ratio=0.25), run_time=1.0)

        self.at("keeping the membrane fluid")
        start_wiggle(self, uns_lips)
        tm_lo = T("lower transition temperature", 24, RED).move_to([RX - 0.5, -3.1, 0])
        self.play(FadeIn(tm_lo, shift=UP * 0.1), run_time=0.6)
        self.at("even when it is cold")
        fluid = chip("fluid", YELLOW, 26).next_to(tm_lo, RIGHT, buff=0.3)
        self.play(FadeIn(fluid, scale=0.8), run_time=0.5)

        # ---- E. coli ---------------------------------------------------------------------------------
        self.at("The E. coli")
        stop_wiggle(uns_lips)
        panels = VGroup(sat_grp, uns_grp, l1, l2, vdw, dfx, tm_hi, tm_lo, gel, fluid, arrows, defects)
        capsule = RoundedRectangle(corner_radius=0.6, width=2.6, height=1.3, stroke_color=GREY, stroke_width=4,
                                   fill_color=GREY, fill_opacity=0.1).move_to([-5.0, 0.2, 0])
        ec = T("E. coli", 28, TEXT).move_to(capsule)
        self.play(FadeOut(panels), FadeIn(VGroup(capsule, ec), shift=RIGHT * 0.2), run_time=0.6)

        kinds0 = ["S", "U", "S", "U", "S"]
        eb_grp, eb_lips = bilayer(-1.3, kinds0, 0.8, ytop=1.2, ybot=-1.05, L=0.95)
        mem_l = T("membrane", 24, GREY).move_to([-1.3, -1.7, 0])
        self.at("example")
        self.play(FadeIn(eb_grp), FadeIn(mem_l), knob.animate.move_to([0, SY, 0]), run_time=0.7)

        tr = ValueTracker(37)
        fl = ValueTracker(0.62)
        tube, tfill, tlab = thermo(1.6, -1.1, 3.0, tr)
        MX, MY0, MH = 4.7, -1.0, 2.8
        mtube = RoundedRectangle(width=0.45, height=MH, corner_radius=0.1, stroke_color=GREY, stroke_width=3,
                                 fill_opacity=0).move_to([MX, MY0 + MH / 2, 0])

        def mmk():
            hh = max(0.05, MH * fl.get_value())
            return Rectangle(width=0.33, height=hh, stroke_width=0, fill_color=TEXT, fill_opacity=0.85).move_to([MX, MY0 + 0.05 + hh / 2 - 0.0, 0])
        mfill = always_redraw(mmk)
        mlab = T("fluidity", 24, TEXT).move_to([MX, MY0 - 0.35, 0])
        ref = DashedLine([MX - 0.45, MY0 + 0.05 + MH * 0.62, 0], [MX + 0.45, MY0 + 0.05 + MH * 0.62, 0], color=GREY,
                         stroke_width=3, dash_length=0.1)
        self.at("is elegant")
        self.play(FadeIn(tube), FadeIn(tfill), FadeIn(tlab), FadeIn(mtube), FadeIn(mfill), FadeIn(mlab), FadeIn(ref), run_time=0.7)

        self.at("chilled to 20 degrees")
        self.play(tr.animate.set_value(20), fl.animate.set_value(0.24), run_time=1.5)

        self.at("makes more unsaturated")
        new_tails = []
        anims = []
        for k in (0, 2):                 # two saturated lipids switch to the kinked, unsaturated form
            for leaflet in (0, 1):
                idx = k + leaflet * 5
                old = eb_lips[idx]
                x = old[0].get_center()[0]
                yh = old[0].get_center()[1]
                d = DOWN if leaflet == 0 else UP
                new = lipid_v(x, yh, d, "U", i=k + 1 + leaflet, L=0.95, bend=-1 if (k + leaflet) % 2 == 0 else 1)
                anims.append(ReplacementTransform(old, new))
        self.play(*anims, knob.animate.move_to([1.5, SY, 0]), fl.animate.set_value(0.62), run_time=2.2)

        self.at("hold its fluidity steady")
        steady = T("held steady", 24, TEXT).move_to([MX, MY0 - 0.8, 0])
        self.play(FadeIn(steady, shift=UP * 0.1), Indicate(ref, color=TEXT, scale_factor=1.1), run_time=0.8)

        # ---- concept chain ---------------------------------------------------------------------------
        self.at("Tuning composition")
        c_env = chip("environment changes", RED, 24)
        c_mid = chip("lipid composition retuned", YELLOW, 24)
        c_vis = chip("viscosity constant", TEXT, 24)
        chain = VGroup(c_env, c_mid, c_vis).arrange(RIGHT, buff=0.85).move_to([0, -2.95, 0])
        fit(chain, max_w=12.2)
        a1 = Arrow(c_env.get_right(), c_mid.get_left(), buff=0.08, color=GREY, stroke_width=4, max_tip_length_to_length_ratio=0.4)
        a2 = Arrow(c_mid.get_right(), c_vis.get_left(), buff=0.08, color=GREY, stroke_width=4, max_tip_length_to_length_ratio=0.4)
        self.play(FadeIn(c_mid, shift=UP * 0.15), run_time=0.5)
        self.at("keep viscosity constant")
        self.play(FadeIn(c_vis, shift=UP * 0.15), GrowArrow(a2), run_time=0.6)
        self.at("as the environment changes")
        self.play(FadeIn(c_env, shift=UP * 0.15), GrowArrow(a1), run_time=0.6)

        self.at("homeoviscous adaptation")
        head2 = T("Homeoviscous adaptation", 40, font=TITLE_FONT).move_to(heading)
        rule = Line(LEFT * 2.2, RIGHT * 2.2, color=GOLD, stroke_width=4).next_to(head2, DOWN, buff=0.12)
        self.play(ReplacementTransform(heading, head2), GrowFromCenter(rule), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------------
class S04Cholesterol(SpokenScene):
    """Cholesterol loosens packed tails in the cold, restrains floppy tails in the heat, and flattens the transition."""

    def construct(self):
        heading = T("Cholesterol, the membrane's thermostat", 36, font=TITLE_FONT).move_to([0, 3.4, 0])

        def blob(x, y):
            return RoundedRectangle(width=0.3, height=1.3, corner_radius=0.15, stroke_width=0,
                                    fill_color=GREEN, fill_opacity=0.95).move_to([x, y, 0])

        # --- title chips ------------------------------------------------------------------------------
        chol = chip("cholesterol", GREEN, 34).move_to([-1.9, 1.0, 0])
        eq = T("=", 40, TEXT).move_to([0.0, 1.0, 0])
        thermo_c = chip("thermostat", RED, 34).move_to([1.95, 1.0, 0])
        self.play(FadeIn(heading, shift=UP * 0.1), FadeIn(chol, shift=RIGHT * 0.2), run_time=0.6)
        self.at("a thermostat")
        self.play(FadeIn(eq), FadeIn(thermo_c, shift=LEFT * 0.2), run_time=0.7)

        # --- cold: tight packed tails, cholesterol pries them apart -----------------------------------
        PY, L = 1.5, 1.8
        n_cold, sp = 8, 0.72
        xs = [(k - (n_cold - 1) / 2) * sp for k in range(n_cold)]

        def leaflet_lipids(xlist, color=BLUE, wave=None):
            out = []
            for k, x in enumerate(xlist):
                hd = head_dot([x, PY, 0], 0.17)
                if wave is None:
                    ts = [tail([x + dx, PY - 0.12, 0], L, DOWN, color=color, stroke=8) for dx in (-0.1, 0.1)]
                else:
                    ts = [wavy([x + dx, PY - 0.12, 0], L, DOWN, wave, cycles=3.0, phase=0.9 * k + 0.5 * j, color=color, stroke=8)
                          for j, dx in enumerate((-0.1, 0.1))]
                out.append(VGroup(hd, *ts))
            return out

        cold = leaflet_lipids(xs)
        cold_g = VGroup(*cold).shift(DOWN * 0.1)
        cold_tag = chip("low temperature", RED, 26).move_to([-4.7, 2.5, 0])

        self.at("At low temperature")
        self.play(FadeOut(VGroup(chol, eq, thermo_c)), run_time=0.5)
        self.play(FadeIn(cold_g), FadeIn(cold_tag, shift=RIGHT * 0.2), run_time=0.9)

        self.at("inserts between the tails")
        # open two gaps (between lipids 2|3 and 5|6) and drop a cholesterol into each
        shifts = [-0.28, -0.28, -0.28, 0.0, 0.0, 0.0, 0.28, 0.28]
        gx1 = (xs[2] + xs[3]) / 2
        gx2 = (xs[5] + xs[6]) / 2
        b1, b2 = blob(gx1 - 0.14, PY - 1.0), blob(gx2 + 0.14, PY - 1.0)
        self.play(*[cold[k].animate.shift(RIGHT * shifts[k]) for k in range(n_cold)],
                  FadeIn(b1, shift=DOWN * 0.3), FadeIn(b2, shift=DOWN * 0.3), run_time=1.0)
        chol_l = T("cholesterol", 26, GREEN).move_to([gx1 - 0.14, -0.95, 0])
        arr = Arrow(chol_l.get_top(), b1.get_bottom(), buff=0.08, color=GREEN, stroke_width=4,
                    max_tip_length_to_length_ratio=0.4)
        self.play(FadeIn(chol_l), GrowArrow(arr), run_time=0.4)

        self.at("disrupts tight packing")
        loose = T("tight packing disrupted", 30, TEXT).move_to([0, -1.75, 0])
        self.play(FadeIn(loose, shift=UP * 0.1), run_time=0.6)
        self.at("preventing the membrane from gelling")
        nogel = T("stays fluid in the cold", 32, BLUE).move_to([0, -2.6, 0])
        self.play(FadeIn(nogel, shift=UP * 0.1), run_time=0.7)

        # --- hot: floppy tails, cholesterol holds them --------------------------------------------------
        self.at("At high temperature")
        n_hot, sph = 6, 1.1
        xh = [(k - (n_hot - 1) / 2) * sph for k in range(n_hot)]
        hot = leaflet_lipids(xh, color=BLUE, wave=0.24)
        hot_g = VGroup(*hot).shift(DOWN * 0.1)
        hot_tag = chip("high temperature", RED, 26).move_to([-4.7, 2.5, 0])
        self.play(FadeOut(VGroup(cold_g, b1, b2, chol_l, arr, loose, nogel)), ReplacementTransform(cold_tag, hot_tag),
                  FadeIn(hot_g), run_time=0.9)
        floppy = T("floppy tails", 30, TEXT).move_to([0, -1.75, 0])
        held = T("held in check", 30, TEXT).move_to([0, -1.75, 0])
        self.play(FadeIn(floppy, shift=UP * 0.1), run_time=0.4)

        self.at("restrains the same tails")
        gh = [(xh[1] + xh[2]) / 2, (xh[3] + xh[4]) / 2]
        hb = [blob(g, PY - 1.0) for g in gh]
        calm = leaflet_lipids(xh, color=BLUE, wave=0.07)
        calm_g = VGroup(*calm).shift(DOWN * 0.1)
        self.play(ReplacementTransform(hot_g, calm_g), *[FadeIn(b, shift=DOWN * 0.3) for b in hb],
                  ReplacementTransform(floppy, held), run_time=1.3)
        self.at("too fluid")
        toofl = T("never too fluid", 32, YELLOW).move_to([0, -2.6, 0])
        self.play(FadeIn(toofl, shift=UP * 0.1), run_time=0.7)

        # --- the graph ----------------------------------------------------------------------------------
        self.at("On a graph")
        self.play(FadeOut(VGroup(calm_g, *hb, hot_tag, toofl, held)), run_time=0.4)

        OX, OY, AW, AH = -4.3, -2.2, 9.0, 4.0
        ax = Axes(x_range=[0, 70, 10], y_range=[0, 1.05, 0.25], x_length=AW, y_length=AH,
                  axis_config={"include_numbers": False, "include_ticks": False, "color": GREY, "stroke_width": 3,
                               "tip_width": 0.16, "tip_height": 0.16}, tips=True)
        ax.shift(np.array([OX, OY, 0]) - ax.c2p(0, 0))
        xt = VGroup(*[lab(str(v), 22).move_to(ax.c2p(v, 0) + DOWN * 0.35) for v in (0, 20, 40, 60)])
        xl = T("temperature (°C)", 26, GREY).move_to([ax.c2p(35, 0)[0], OY - 0.95, 0])
        yl = T("membrane fluidity", 26, GREY).rotate(PI / 2).move_to([OX - 0.5, OY + AH / 2, 0])
        self.play(Create(ax), FadeIn(xt), FadeIn(xl), FadeIn(yl), run_time=0.8)

        sharp_f = lambda x: 1 / (1 + np.exp(-(x - 41) / 1.4))
        broad_f = lambda x: 0.2 + 0.6 / (1 + np.exp(-(x - 38) / 16))
        sharp = ax.plot(sharp_f, x_range=[0, 70], color=BLUE, stroke_width=6, use_smoothing=False)
        broad = ax.plot(broad_f, x_range=[0, 70], color=GREEN, stroke_width=6)
        sharp_l = T("saturated lipid alone", 26, BLUE).move_to(ax.c2p(18, 0.12) + UP * 0.3)
        body = DashedLine(ax.c2p(37, 0), ax.c2p(37, 1.02), color=RED, stroke_width=3, dash_length=0.12)
        body_l = T("37 °C", 24, RED).move_to(ax.c2p(37, 1.02) + UP * 0.28)
        note = T("schematic curves", 22, GREY).move_to([ax.c2p(70, 0)[0] - 0.6, OY - 0.95, 0])
        self.at("against temperature")
        self.play(Create(sharp), FadeIn(sharp_l), Create(body), FadeIn(body_l), FadeIn(note), run_time=1.2)

        self.at("cholesterol flattens")
        ghost = sharp.copy()
        self.play(Transform(sharp, broad), FadeOut(sharp_l), run_time=1.9)
        broad_l = T("with cholesterol", 26, GREEN).move_to(ax.c2p(55, 0.62) + UP * 0.55)
        self.play(FadeIn(broad_l), run_time=0.4)

        self.at("stable operating range")
        band = Rectangle(width=ax.c2p(60, 0)[0] - ax.c2p(10, 0)[0], height=AH, stroke_width=0, fill_color=GREEN,
                         fill_opacity=0.10).move_to([(ax.c2p(10, 0)[0] + ax.c2p(60, 0)[0]) / 2, OY + AH / 2, 0])
        win = DoubleArrow(ax.c2p(10, 0.06), ax.c2p(60, 0.06), buff=0, color=GREEN, stroke_width=5,
                          max_tip_length_to_length_ratio=0.06)
        win_l = T("wide, stable window", 26, GREEN).next_to(win, UP, buff=0.1)
        win_l.set_x(ax.c2p(22, 0)[0])
        self.play(FadeIn(band), GrowFromCenter(win), FadeIn(win_l), run_time=1.1)

        self.at("One molecule")
        ghost.set_stroke(BLUE, opacity=0.4, width=4)
        self.play(FadeOut(VGroup(band, win, win_l, broad_l)), FadeIn(ghost), run_time=0.6)
        up = Arrow(ax.c2p(10, 0.0), ax.c2p(10, 0.27), buff=0.04, color=GREEN, stroke_width=6, max_tip_length_to_length_ratio=0.35)
        dn = Arrow(ax.c2p(64, 1.0), ax.c2p(64, 0.74), buff=0.04, color=GREEN, stroke_width=6, max_tip_length_to_length_ratio=0.35)
        up_l = T("more fluid in cold", 24, GREEN)
        up_l.move_to(ax.c2p(11.5, 0.12) + RIGHT * up_l.width / 2)
        dn_l = T("less fluid in the heat", 24, GREEN)
        dn_l.move_to(ax.c2p(70, 1.12) + LEFT * dn_l.width / 2)
        self.at("two opposite jobs")
        self.play(GrowArrow(up), GrowArrow(dn), FadeIn(up_l), FadeIn(dn_l), run_time=1.0)
        self.finish()


class S05End(EndCard):
    LINE = "Tail shape sets how fats and membranes behave."
