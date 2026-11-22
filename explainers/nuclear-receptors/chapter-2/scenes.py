"""
Helix 12 and Tissue Helpers: Turning the Switch
================================================

COLOUR MAP (one colour per concept across the whole film):
- TEAL   (#3FB8C0): Hormone-binding domain (HBD), DNA-binding domain (DBD), and new mRNA
- BLUE   (#58C4DD): Helix 12 (the moving lid / AF-2 plug)
- CREAM  (#EDE4CC): DNA strand and histone spools
- ORANGE (#F08C42): AF-1 front-end switching surface
- GOLD   (#D4A843): Agonist ligand (estradiol), hormone bar, and question/timer accents
- GREEN  (#83C167): Co-activators (LXXLL), acetyl tags, new protein, and ON state
- RED    (#FC6255): Antagonist ligand (4-hydroxytamoxifen), co-repressors, and OFF state
- YELLOW (#F5D547): Fast cyclic AMP relay curve (contrast against slow transcription)
- TEXT   (#E8EAF0): Primary labels and end-card text (full opacity)
- GREY   (#8B93A1): Plot axes, ticks, and schematic scope tag only

ONE WORLD CARRIED FROM SCENE TO SCENE:
A single modular nuclear receptor—orange AF-1 on the left, teal DNA-binding grip on pale cream DNA
in the middle, and a cutaway teal hormone-binding pocket on the right with hinged blue Helix 12—
carried from the full-receptor bridge into the zoomed pocket cutaway (s02-s07), back out to paired
receptors across Breast and Uterus cells (s08), and onto the computed timescale plot (s09-s10).

WHAT CHANGES ON SCREEN (every spoken scene, and what computes it):
- s01_bridge_hook: Receptor DBD grips DNA while gold ligand enters the pocket, zooms smoothly into
  the cutaway pocket, Helix 12 pivots to show the open switch, and Breast OFF / Uterus ON appear.
- s02_helix12_agonist: Bundled helices ripple to reveal the pocket, Helix 12 pivots through its
  hinge range, gold estradiol glides into the pocket, and Helix 12 rotates (+28 -> -90 deg) as a lid.
- s03_groove_coact: Helix 12 seats to complete the AF-2 groove, co-activator docks LXXLL, acetyl
  dots travel to 3 histones, loosen tracker (0->1) unwinds DNA, and rna_prog extends mRNA.
- s04_antagonist_setup: Gold estradiol and co-activator exit while Helix 12 rotates open (-90->+28 deg);
  tamoxifen converts into 4-hydroxytamoxifen with a growing side chain that enters the pocket mouth.
- s05_predict_q: Helix 12 rotates down (+28 deg toward -90 deg), collides with the protruding side
  chain at -44 deg and rebounds twice via a damped collision curve while the co-activator approaches.
- s07_reveal_groove_blocked: Helix 12 bounces off the arm once more, swings around (+28->+180 deg)
  into the AF-2 groove as a plug, co-activator rebounds off the plug, and histones tighten below.
- s08_af1_tissue_context: Full receptor dimer on DNA shows orange AF-1 open, then splits into Breast
  (co-repressors dock, histones stay tight, OFF) and Uterus (co-activators dock at AF-1, histones
  slide apart via loosen tracker, ON).
- s09_serm_timescale: A time ValueTracker (0->10) drives live_curve and dot on a computed Plot to draw
  the fast cAMP Gaussian spike (seconds), intermediate new mRNA curve (tens of min), and broad new
  protein plateau (hours).
- s10_closing: Gold hormone bar clears while a shaded protein plateau extends under a moving cursor;
  above, 3 target genes activate on DNA under the balance of ligand shape and cell helpers.
"""
import numpy as np
from bp_parts import *  # noqa: F401,F403

CREAM = "#EDE4CC"
ORANGE = "#F08C42"

# Shared geometry constants for the carried HBD cutaway (s02 - s07)
HINGE = np.array([1.34, 1.85, 0.0])
H12_LEN = 2.15
H12_OPEN = 28.0 * DEGREES
H12_LID = -90.0 * DEGREES
H12_COLLIDE = -44.0 * DEGREES
H12_PLUG = 180.0 * DEGREES
POCKET_CTR = np.array([-0.15, 0.30, 0.0])
GROOVE_CTR = np.array([0.20, 1.82, 0.0])


def make_helix12(angle_rad):
    """Helix 12 bar anchored at HINGE, rotated by angle_rad (0 = pointing +X)."""
    bar = RoundedRectangle(
        corner_radius=0.17,
        width=H12_LEN,
        height=0.36,
        color=BLUE,
        stroke_width=3.5,
        fill_color=BLUE,
        fill_opacity=0.48,
    )
    bar.move_to(HINGE + RIGHT * (H12_LEN / 2 - 0.12))
    bar.rotate(angle_rad, about_point=HINGE)
    pivot = Dot(HINGE, radius=0.075, color=TEXT, stroke_color=BLUE, stroke_width=2)
    return VGroup(bar, pivot)


def make_hbd_cutaway():
    """Cutaway schematic of ~12 bundled helices around the hydrophobic pocket and AF-2 groove."""
    tubes = VGroup()
    for i, x in enumerate([-3.40, -2.92, -2.44, -1.96, -1.48]):
        h = 3.25 if i in (0, 4) else 3.45
        op = 0.30 if i % 2 == 0 else 0.42
        t = RoundedRectangle(
            corner_radius=0.19,
            width=0.43,
            height=h,
            color=TEAL,
            stroke_width=2.6,
            fill_color=TEAL,
            fill_opacity=op,
        ).move_to([x, 0.42, 0])
        tubes.add(t)

    for i, x in enumerate([-1.00, -0.52, -0.04, 0.44, 0.92]):
        op = 0.40 if i % 2 == 0 else 0.30
        t = RoundedRectangle(
            corner_radius=0.17,
            width=0.43,
            height=0.95,
            color=TEAL,
            stroke_width=2.6,
            fill_color=TEAL,
            fill_opacity=op,
        ).move_to([x, -0.82, 0])
        tubes.add(t)

    shoulder = RoundedRectangle(
        corner_radius=0.17,
        width=0.43,
        height=1.28,
        color=TEAL,
        stroke_width=2.6,
        fill_color=TEAL,
        fill_opacity=0.42,
    ).move_to([-1.00, 1.54, 0])
    tubes.add(shoulder)

    for i, x in enumerate([-0.52, -0.04, 0.44, 0.92]):
        op = 0.30 if i % 2 == 0 else 0.40
        t = RoundedRectangle(
            corner_radius=0.15,
            width=0.43,
            height=0.60,
            color=TEAL,
            stroke_width=2.6,
            fill_color=TEAL,
            fill_opacity=op,
        ).move_to([x, 1.20, 0])
        tubes.add(t)

    pocket_bg = RoundedRectangle(
        corner_radius=0.22,
        width=2.36,
        height=1.18,
        stroke_width=0,
        fill_color=TEAL,
        fill_opacity=0.10,
    ).move_to(POCKET_CTR)
    g = VGroup(pocket_bg, tubes)
    g.tubes = tubes
    g.pocket_bg = pocket_bg
    return g


def make_estradiol(center=POCKET_CTR):
    """Gold sphere representing estradiol (no molecular structure)."""
    core = Circle(radius=0.40, color=GOLD, stroke_width=3.2, fill_color=GOLD, fill_opacity=0.62)
    halo = Circle(radius=0.50, color=GOLD, stroke_width=1.8, stroke_opacity=0.52, fill_opacity=0)
    return VGroup(halo, core).move_to(center)


def make_tamoxifen(center=POCKET_CTR, arm_len=2.15):
    """Coral-red 4-hydroxytamoxifen shape with bulky side chain jutting out of the pocket mouth."""
    body = RoundedRectangle(
        corner_radius=0.28,
        width=1.55,
        height=0.78,
        color=RED,
        stroke_width=3.2,
        fill_color=RED,
        fill_opacity=0.54,
    ).move_to(center + LEFT * 0.15)
    arm = RoundedRectangle(
        corner_radius=0.14,
        width=arm_len,
        height=0.32,
        color=RED,
        stroke_width=3.2,
        fill_color=RED,
        fill_opacity=0.70,
    ).move_to(center + RIGHT * (0.60 + arm_len / 2))
    g = VGroup(body, arm)
    g.body = body
    g.arm = arm
    return g


def make_coactivator(center=np.array([0.48, 2.58, 0.0])):
    """Emerald co-activator block carrying a short LXXLL helix rod underneath (clears shoulder)."""
    block = RoundedRectangle(
        corner_radius=0.18,
        width=2.28,
        height=0.66,
        color=GREEN,
        stroke_width=3.0,
        fill_color=GREEN,
        fill_opacity=0.28,
    ).move_to(center)
    rod = RoundedRectangle(
        corner_radius=0.12,
        width=1.32,
        height=0.28,
        color=GREEN,
        stroke_width=2.8,
        fill_color=GREEN,
        fill_opacity=0.68,
    ).move_to(center + DOWN * 0.76 + LEFT * 0.28)
    neck = Rectangle(
        width=0.32,
        height=0.28,
        stroke_width=0,
        fill_color=GREEN,
        fill_opacity=0.45,
    ).move_to(center + DOWN * 0.48 + LEFT * 0.28)
    lbl = T("Co-activator", size=25, color=GREEN).move_to(block)
    g = VGroup(neck, rod, block, lbl)
    g.block = block
    g.rod = rod
    g.lbl = lbl
    return g


def _spool_xs(loosen_u, x_left, x_right, shift_mid=-0.20):
    mid_x = (x_left + x_right) / 2.0 + shift_mid
    spread = 0.98 + 1.08 * loosen_u
    return [mid_x - spread, mid_x, mid_x + spread]


def make_dna_chromatin(loosen_tracker, y_center=-2.45, x_left=-5.3, x_right=2.5, shift_mid=-0.20):
    """Pale cream DNA wrapping 3 histone spools; spools slide apart as loosen_tracker goes 0->1."""
    def _build():
        u = float(np.clip(loosen_tracker.get_value(), 0.0, 1.0))
        spool_xs = _spool_xs(u, x_left, x_right, shift_mid=shift_mid)

        spools = VGroup()
        for sx in spool_xs:
            sp = Circle(
                radius=0.30,
                color=CREAM,
                stroke_width=2.4,
                fill_color=CREAM,
                fill_opacity=0.26,
            ).move_to([sx, y_center, 0])
            spools.add(sp)

        xs = np.linspace(x_left, x_right, 160)
        amp = 0.36 * (1.0 - 0.82 * u)
        pts_top, pts_bot = [], []
        for x in xs:
            bump = sum(np.exp(-((x - sx) / 0.34) ** 2) for sx in spool_xs)
            dy = amp * bump
            pts_top.append([x, y_center + 0.06 + dy, 0.0])
            pts_bot.append([x, y_center - 0.06 - 0.55 * dy, 0.0])
        strand1 = VMobject(stroke_color=CREAM, stroke_width=3.5).set_points_as_corners(pts_top)
        strand2 = VMobject(stroke_color=CREAM, stroke_width=2.2, stroke_opacity=0.75).set_points_as_corners(pts_bot)
        return VGroup(spools, strand1, strand2)

    return always_redraw(_build)


def make_dna_strand(x0=-5.4, x1=4.8, y=-1.95, amp=0.14):
    """Clean pale cream DNA double-strand bar for full-receptor views."""
    xs = np.linspace(x0, x1, 140)
    p1 = [[x, y + amp * np.sin(2.4 * (x - x0)), 0] for x in xs]
    p2 = [[x, y - amp * np.sin(2.4 * (x - x0)), 0] for x in xs]
    s1 = VMobject(stroke_color=CREAM, stroke_width=3.5).set_points_as_corners(p1)
    s2 = VMobject(stroke_color=CREAM, stroke_width=3.0, stroke_opacity=0.8).set_points_as_corners(p2)
    rungs = VGroup()
    for rx in np.arange(x0 + 0.25, x1 - 0.15, 0.45):
        dy = abs(amp * np.sin(2.4 * (rx - x0)))
        if dy > 0.04:
            rungs.add(Line([rx, y - dy, 0], [rx, y + dy, 0], color=CREAM, stroke_width=1.8, stroke_opacity=0.55))
    return VGroup(rungs, s1, s2)


def make_full_receptor(center=np.array([-0.5, -0.35, 0.0]), scale=1.0, show_tamoxifen=False, plugged=False):
    """Modular nuclear receptor sitting on DNA: AF-1 (orange) + DBD (teal) + HBD pocket (teal/blue)."""
    g = VGroup()
    af1 = RoundedRectangle(corner_radius=0.18, width=1.65, height=0.88, color=ORANGE, stroke_width=3.0,
                           fill_color=ORANGE, fill_opacity=0.36).move_to([-2.55, 0.35, 0])
    hinge1 = Line([-1.72, 0.20, 0], [-1.05, -0.30, 0], color=TEAL, stroke_width=5)
    dbd = RoundedRectangle(corner_radius=0.18, width=1.35, height=1.05, color=TEAL, stroke_width=3.0,
                           fill_color=TEAL, fill_opacity=0.36).move_to([-0.60, -0.78, 0])
    hinge2 = Line([0.08, -0.45, 0], [0.75, 0.20, 0], color=TEAL, stroke_width=5)

    hbd_body = VGroup(
        RoundedRectangle(corner_radius=0.22, width=1.85, height=1.50, color=TEAL, stroke_width=3.0,
                         fill_color=TEAL, fill_opacity=0.30).move_to([1.68, 0.55, 0]),
        RoundedRectangle(corner_radius=0.14, width=0.95, height=0.68, stroke_width=0,
                         fill_color=BG, fill_opacity=0.95).move_to([2.15, 0.50, 0]),
    )
    hbd_rim = Arc(radius=0.52, start_angle=PI / 2, angle=PI, arc_center=[1.95, 0.50, 0], color=TEAL, stroke_width=3.5)

    if plugged:
        h12 = RoundedRectangle(corner_radius=0.09, width=0.88, height=0.20, color=BLUE, stroke_width=2.8,
                               fill_color=BLUE, fill_opacity=0.55).move_to([1.68, 1.25, 0])
    else:
        h12 = RoundedRectangle(corner_radius=0.09, width=0.88, height=0.20, color=BLUE, stroke_width=2.8,
                               fill_color=BLUE, fill_opacity=0.55).move_to([2.65, 1.22, 0]).rotate(28 * DEGREES)

    g.add(hinge1, hinge2, af1, dbd, hbd_body, hbd_rim, h12)
    if show_tamoxifen:
        tam = RoundedRectangle(corner_radius=0.14, width=0.72, height=0.38, color=RED, stroke_width=2.4,
                               fill_color=RED, fill_opacity=0.55).move_to([2.05, 0.50, 0])
        arm = RoundedRectangle(corner_radius=0.07, width=0.78, height=0.16, color=RED, stroke_width=2.4,
                               fill_color=RED, fill_opacity=0.75).move_to([2.62, 0.50, 0])
        g.add(tam, arm)

    g.scale(scale).move_to(center)
    g.af1 = af1
    g.dbd = dbd
    g.hbd = hbd_body
    g.h12 = h12
    g.pocket_grp = VGroup(hbd_body, hbd_rim, h12)
    return g


def make_dimer_pair(y_dna=-1.90, scale=0.88):
    """Two face-to-face receptor monomers paired on DNA without overlapping HBDs."""
    left = make_full_receptor(center=[-2.85, y_dna + 1.48, 0], scale=scale, show_tamoxifen=True, plugged=True)
    right = make_full_receptor(center=[2.85, y_dna + 1.48, 0], scale=scale, show_tamoxifen=True, plugged=True)
    right.flip(UP)
    left.shift(LEFT * 0.25)
    right.shift(RIGHT * 0.25)
    return left, right


def make_timescale_plot():
    """Shared computed Plot for s09 and s10."""
    P = Plot(
        box=(-5.4, 5.4, -2.50, 0.50),
        xr=(0.0, 10.0),
        yr=(0.0, 1.15),
        xticks=[(0.7, "seconds"), (4.0, "tens of min"), (8.3, "hours")],
        yticks=[],
        ylabel="Response",
        color=GREY,
        size=24,
        label_size=26,
    )
    f_camp = lambda x: 0.92 * np.exp(-((x - 0.7) / 0.24) ** 2)
    f_mrna = lambda x: 0.0 if x < 1.3 else 0.78 * (1.0 - np.exp(-(x - 1.3) / 1.0)) * np.exp(-max(0.0, x - 3.6) / 9.5)
    f_prot = lambda x: 0.0 if x < 2.6 else 0.88 * (1.0 - np.exp(-((x - 2.6) / 2.2) ** 2))
    return P, f_camp, f_mrna, f_prot


def _shaded_area(P, fn, x0, tracker, color=GREEN, opacity=0.18):
    """Computed filled area under y=fn(x) from x0 up to tracker.get_value()."""
    def _mk():
        x1 = float(tracker.get_value())
        if x1 <= x0 + 0.05:
            return VMobject()
        xs = np.linspace(x0, x1, 60)
        pts = [P.pt(x0, 0.0)] + [P.pt(x, fn(x)) for x in xs] + [P.pt(x1, 0.0)]
        poly = Polygon(*pts, stroke_width=0, fill_color=color, fill_opacity=opacity)
        return poly
    return always_redraw(_mk)


# ------------------------------------------------------------------ Scenes
class S00Title(TitleCard):
    LESSON = "Nuclear Receptors: Receptors That Are Transcription Factors"
    TITLE = "Helix 12 and Tissue Helpers: Turning the Switch"


class S01BridgeHook(SpokenScene):
    def construct(self):
        dna = make_dna_strand(x0=-5.5, x1=4.8, y=-2.05)
        rec = make_full_receptor(center=[-0.5, -0.35, 0], scale=1.30)
        tag = scope_tag("schematic")

        lbl_af1 = T("AF-1", size=28, color=ORANGE).next_to(rec.af1, UP, buff=0.22)
        lbl_dbd = T("DBD", size=28, color=TEAL).next_to(rec.dbd, LEFT, buff=0.28)
        lbl_hbd = T("Pocket", size=28, color=TEAL).next_to(rec.hbd, UP, buff=0.35)
        lbl_dna = T("DNA", size=28, color=CREAM).next_to(dna, DOWN, buff=0.22)

        lig = Circle(radius=0.20, color=GOLD, stroke_width=2.5, fill_color=GOLD, fill_opacity=0.72).move_to(
            rec.hbd.get_center() + RIGHT * 2.6
        )
        lig.set_z_index(2)

        self.add(dna, rec, lbl_af1, lbl_dbd, lbl_hbd, lbl_dna, tag)
        # Receptor settles its DBD grip onto DNA while the first sentence introduces it
        self.play(
            rec.animate.shift(DOWN * 0.12),
            rec.dbd.animate.set_fill(TEAL, opacity=0.56),
            run_time=1.8,
        )

        self.at("binding both ligand")
        self.play(
            lig.animate.move_to(rec.hbd.get_center() + RIGHT * 0.28),
            rec.h12.animate.rotate(-18 * DEGREES),
            rec.hbd[0].animate.set_fill(TEAL, opacity=0.45),
            run_time=2.8,
        )

        self.at("tiny molecule inside")
        rest = VGroup(dna, rec[0], rec[1], rec[2], rec[3], lbl_af1, lbl_dbd, lbl_hbd, lbl_dna)
        target_pocket = make_hbd_cutaway()
        theta = ValueTracker(H12_OPEN)
        h12_open = always_redraw(lambda: make_helix12(theta.get_value()))
        estradiol = make_estradiol(POCKET_CTR)
        pocket_lbl = T("Hormone-binding pocket", size=30, color=TEAL).move_to([-1.2, 2.95, 0])

        self.play(FadeOut(rest), run_time=0.45)
        self.play(
            rec.pocket_grp.animate.scale(1.65).move_to([-0.2, 0.35, 0]),
            lig.animate.scale(1.65).move_to(POCKET_CTR),
            run_time=1.0,
        )
        self.play(
            FadeOut(VGroup(rec.pocket_grp, lig), run_time=0.35),
            FadeIn(target_pocket, run_time=0.55),
            FadeIn(h12_open, run_time=0.55),
            FadeIn(estradiol, run_time=0.55),
            FadeIn(pocket_lbl, run_time=0.55),
        )

        self.at("flip a gene")
        # Visual question: Helix 12 pivots part-way toward closing and back as the switch question is asked
        self.play(theta.animate.set_value(-18 * DEGREES), run_time=1.6)
        self.play(theta.animate.set_value(H12_OPEN), run_time=1.6)

        breast_badge = boxed_label("Breast: OFF", color=RED, size=28).move_to([4.55, 2.05, 0])
        uterus_badge = boxed_label("Uterus: ON", color=GREEN, size=28).move_to([4.55, 1.05, 0])

        self.at("in breast tissue")
        self.play(FadeIn(breast_badge, shift=LEFT * 0.2), run_time=1.0)

        self.at("in the uterus")
        self.play(FadeIn(uterus_badge, shift=LEFT * 0.2), run_time=1.0)
        self.finish()


class S02Helix12Agonist(SpokenScene):
    def construct(self):
        hbd = make_hbd_cutaway()
        theta = ValueTracker(H12_OPEN)
        h12 = always_redraw(lambda: make_helix12(theta.get_value()))
        tag = scope_tag("schematic")

        lbl_domain = T("Hormone-binding domain", size=30, color=TEAL).move_to([-1.4, 2.95, 0])
        lbl_helices = T("~12 helices + hydrophobic pocket", size=28, color=TEAL).move_to([-1.1, -2.05, 0])

        self.add(hbd, h12, tag)
        self.play(
            FadeIn(lbl_domain),
            LaggedStart(*[t.animate.set_fill(TEAL, opacity=0.52) for t in hbd.tubes], lag_ratio=0.06, run_time=2.2),
        )

        self.at("about 12 helices")
        pocket_outline = RoundedRectangle(
            corner_radius=0.22, width=2.36, height=1.18, color=GOLD, stroke_width=2.8, fill_opacity=0
        ).move_to(POCKET_CTR)
        self.play(
            FadeIn(lbl_helices, shift=UP * 0.15),
            LaggedStart(*[t.animate.set_fill(TEAL, opacity=0.34) for t in hbd.tubes], lag_ratio=0.05, run_time=2.4),
            Create(pocket_outline, run_time=1.8),
        )

        self.at("helix 12")
        lbl_h12 = T("Helix 12", size=30, color=BLUE).move_to([4.45, 2.45, 0])
        arrow_h12 = Arrow([3.65, 2.45, 0], [2.95, 2.55, 0], buff=0.05, color=BLUE, stroke_width=3.5, tip_length=0.22)
        self.play(
            FadeIn(lbl_h12),
            GrowArrow(arrow_h12),
            FadeOut(pocket_outline, run_time=0.6),
            theta.animate.set_value(42 * DEGREES),
            run_time=1.3,
        )
        self.play(theta.animate.set_value(H12_OPEN), run_time=1.2)

        self.at("agonist like estradiol enters")
        estradiol = make_estradiol(center=np.array([4.35, 0.30, 0.0]))
        lbl_est = T("Estradiol (agonist)", size=28, color=GOLD).next_to(estradiol, DOWN, buff=0.24)
        self.play(FadeIn(estradiol, shift=LEFT * 0.2), FadeIn(lbl_est), run_time=0.8)
        self.play(
            estradiol.animate.move_to(POCKET_CTR),
            lbl_est.animate.move_to([4.15, -0.75, 0]),
            FadeOut(lbl_helices, run_time=0.5),
            hbd.pocket_bg.animate.set_fill(GOLD, opacity=0.18),
            run_time=2.4,
        )

        self.at("helix 12 folds shut")
        self.play(FadeOut(arrow_h12, run_time=0.3), run_time=0.3)
        self.play(
            theta.animate.set_value(H12_LID),
            lbl_h12.animate.move_to([3.05, 0.70, 0]),
            run_time=2.2,
        )
        lid_note = T("Closed like a lid", size=28, color=BLUE).move_to([3.40, 1.35, 0])
        self.play(FadeIn(lid_note, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S03GrooveCoact(SpokenScene):
    def construct(self):
        hbd = make_hbd_cutaway()
        theta = ValueTracker(-65 * DEGREES)
        h12 = always_redraw(lambda: make_helix12(theta.get_value()))
        estradiol = make_estradiol(POCKET_CTR)
        tag = scope_tag("schematic")

        loosen = ValueTracker(0.0)
        chromatin = make_dna_chromatin(loosen, y_center=-2.45, x_left=-5.3, x_right=2.5, shift_mid=-0.20)

        self.add(hbd, h12, estradiol, tag)
        # Click Helix 12 shut into lid position to begin completing the AF-2 groove
        self.play(theta.animate.set_value(H12_LID), run_time=1.6)

        self.at("completes a shallow")
        groove_box = DashedVMobject(
            RoundedRectangle(corner_radius=0.12, width=1.80, height=0.58, color=GOLD, stroke_width=3.2).move_to(GROOVE_CTR),
            num_dashes=16,
        )
        lbl_groove = T("AF-2 groove", size=30, color=GOLD).move_to([-3.10, 2.65, 0])
        groove_arr = Arrow([-1.65, 2.48, 0], [-0.35, 1.98, 0], buff=0.05, color=GOLD, stroke_width=3.2, tip_length=0.20)
        self.play(Create(groove_box), FadeIn(lbl_groove), GrowArrow(groove_arr), run_time=2.2)

        coact = make_coactivator(center=np.array([4.35, 2.85, 0.0]))
        self.play(FadeIn(coact, shift=LEFT * 0.25), run_time=1.8)

        self.at("carry a short helix")
        lbl_lxx = T("LXXLL", size=28, color=GREEN).move_to([3.30, 2.55, 0])
        lxx_arr = CurvedArrow([2.65, 2.52, 0], [0.92, 1.88, 0], angle=0.52, color=GREEN, stroke_width=3.0, tip_length=0.18)
        self.play(
            coact.animate.shift(np.array([0.48, 2.58, 0.0]) - coact.block.get_center()),
            FadeOut(groove_box, run_time=0.4),
            FadeOut(groove_arr, run_time=0.4),
            FadeOut(lbl_groove, run_time=0.4),
            run_time=2.0,
        )
        self.play(FadeIn(lbl_lxx), Create(lxx_arr), run_time=0.9)

        self.at("add acetyl tags to histones")
        lbl_hist = T("Histones + DNA", size=26, color=CREAM).move_to([-4.65, -1.72, 0])
        self.play(FadeIn(chromatin), FadeIn(lbl_hist), run_time=1.2)

        # Acetyl dots fly along computed arcs to the bottom of each histone spool so top stays clear for mRNA
        init_xs = _spool_xs(0.0, -5.3, 2.5, shift_mid=-0.20)
        ac_dots_fly = VGroup()
        for idx, sx in enumerate(init_xs):
            d = Dot([1.75, 2.00, 0], radius=0.12, color=GREEN, stroke_color=TEXT, stroke_width=1.5)
            ac_dots_fly.add(d)
            path = ArcBetweenPoints(np.array([1.75, 2.00, 0.0]), np.array([sx, -2.82, 0.0]), angle=-0.45)
            tr = DashedVMobject(path.copy().set_stroke(GREEN, 2.5, opacity=0.65), num_dashes=14)
            self.add(d)
            self.play(Create(tr, run_time=0.45), MoveAlongPath(d, path, run_time=1.1))
            self.play(FadeOut(tr, run_time=0.25))

        ac_bound = always_redraw(
            lambda: VGroup(
                *[
                    VGroup(
                        Dot([sx, -2.82, 0], radius=0.11, color=GREEN, stroke_color=TEXT, stroke_width=1.5),
                        T("Ac", size=24, color=GREEN).move_to([sx, -3.14, 0]),
                    )
                    for sx in _spool_xs(float(loosen.get_value()), -5.3, 2.5, shift_mid=-0.20)
                ]
            )
        )
        self.remove(*ac_dots_fly)
        self.add(ac_bound)

        self.at("the dna loosens")
        self.play(loosen.animate.set_value(1.0), run_time=2.4)

        self.at("and rn")
        pol = RoundedRectangle(corner_radius=0.16, width=0.72, height=0.42, color=TEAL, stroke_width=2.8,
                               fill_color=TEAL, fill_opacity=0.68).move_to([-2.0, -2.42, 0])
        lbl_pol = T("RNA pol", size=26, color=TEAL).move_to([3.75, -2.42, 0])
        rna_prog = ValueTracker(0.0)
        rna_strand = always_redraw(
            lambda: VMobject(stroke_color=TEAL, stroke_width=5.5).set_points_as_corners(
                [
                    [-2.0 + 4.4 * s, -2.38 + 0.72 * s + 0.10 * np.sin(9.0 * s), 0.0]
                    for s in np.linspace(0.0, max(0.02, rna_prog.get_value()), 45)
                ]
            )
        )
        self.add(rna_strand, pol)
        self.play(FadeIn(lbl_pol), run_time=0.4)
        self.play(
            pol.animate.move_to([2.1, -2.42, 0]),
            rna_prog.animate.set_value(1.0),
            run_time=1.5,
        )
        self.finish()


class S04AntagonistSetup(SpokenScene):
    def construct(self):
        hbd = make_hbd_cutaway()
        theta = ValueTracker(H12_LID)
        h12 = always_redraw(lambda: make_helix12(theta.get_value()))
        estradiol = make_estradiol(POCKET_CTR)
        coact = make_coactivator(center=np.array([0.48, 2.58, 0.0]))
        tag = scope_tag("schematic")

        self.add(hbd, h12, estradiol, coact, tag)
        self.wait(0.3)

        self.at("without switching the receptor")
        self.play(
            estradiol.animate.shift(RIGHT * 4.2).set_opacity(0),
            coact.animate.shift(UP * 1.6).set_opacity(0),
            theta.animate.set_value(H12_OPEN),
            run_time=2.0,
        )
        self.remove(estradiol, coact)

        self.at("converts the breast")
        tam_pill = boxed_label("Tamoxifen", color=RED, size=28).move_to([4.15, 1.45, 0])
        liver_lbl = T("Liver", size=24, color=TEXT).move_to([4.85, 0.65, 0])
        conv_arr = Arrow([4.15, 0.98, 0], [4.15, 0.20, 0], buff=0.05, color=RED, stroke_width=3.2, tip_length=0.20)
        arm_tracker = ValueTracker(0.15)
        tam_live = always_redraw(lambda: make_tamoxifen(center=np.array([3.65, -0.40, 0.0]), arm_len=arm_tracker.get_value()))
        lbl_4oh = T("4-hydroxytamoxifen", size=28, color=RED).move_to([4.05, -1.25, 0])

        self.play(FadeIn(tam_pill), run_time=1.0)
        self.add(tam_live)
        self.play(GrowArrow(conv_arr), FadeIn(liver_lbl), arm_tracker.animate.set_value(2.15), run_time=3.5)
        self.play(FadeIn(lbl_4oh), run_time=1.2)
        tam = make_tamoxifen(center=np.array([3.65, -0.40, 0.0]), arm_len=2.15)
        self.remove(tam_live)
        self.add(tam)
        self.play(tam.animate.shift(LEFT * 1.35 + UP * 0.45), run_time=1.5)

        self.at("fits the pocket")
        target_tam = make_tamoxifen(center=POCKET_CTR + RIGHT * 0.65)
        self.play(
            FadeOut(tam_pill, run_time=0.45),
            FadeOut(conv_arr, run_time=0.45),
            FadeOut(liver_lbl, run_time=0.45),
            tam.animate.move_to(target_tam.get_center()),
            lbl_4oh.animate.move_to([3.95, -0.75, 0]),
            run_time=1.4,
        )

        self.at("long side chain sticks")
        arm_ring = DashedVMobject(
            RoundedRectangle(corner_radius=0.18, width=2.28, height=0.56, color=YELLOW, stroke_width=3.4).move_to(
                tam.arm.get_center()
            ),
            num_dashes=18,
        )
        lbl_chain = T("Side chain in pocket mouth", size=28, color=RED).move_to([3.75, -1.55, 0])
        self.play(Create(arm_ring), FadeIn(lbl_chain, shift=UP * 0.1), run_time=1.4)
        self.finish()


def build_predict_backdrop():
    """Shared world at end of s05 / throughout s06_pause."""
    hbd = make_hbd_cutaway()
    h12 = make_helix12(H12_OPEN)
    tam = make_tamoxifen(center=POCKET_CTR + RIGHT * 0.65)
    lbl_4oh = T("4-hydroxytamoxifen", size=28, color=RED).move_to([3.95, -0.75, 0])
    groove_ring = DashedVMobject(
        RoundedRectangle(corner_radius=0.14, width=1.80, height=0.58, color=GOLD, stroke_width=3.2).move_to(GROOVE_CTR),
        num_dashes=16,
    )
    lbl_groove = T("Co-activator groove", size=28, color=GOLD).move_to([-3.35, 2.65, 0])
    groove_arr = Arrow([-1.55, 2.50, 0], [-0.35, 1.98, 0], buff=0.05, color=GOLD, stroke_width=3.0, tip_length=0.18)
    coact = make_coactivator(center=np.array([4.85, 2.05, 0.0]))
    tag = scope_tag("schematic")
    return VGroup(hbd, h12, tam, lbl_4oh, groove_ring, lbl_groove, groove_arr, coact, tag)


class S05PredictQ(SpokenScene):
    def construct(self):
        hbd = make_hbd_cutaway()
        theta = ValueTracker(H12_OPEN)
        h12 = always_redraw(lambda: make_helix12(theta.get_value()))
        tam = make_tamoxifen(center=POCKET_CTR + RIGHT * 0.65)
        lbl_4oh = T("4-hydroxytamoxifen", size=28, color=RED).move_to([3.95, -0.75, 0])
        tag = scope_tag("schematic")

        self.add(hbd, h12, tam, lbl_4oh, tag)
        self.play(theta.animate.set_value(16 * DEGREES), run_time=1.8)

        self.at("wants to fold shut")
        for bounce in (H12_COLLIDE, 8 * DEGREES, H12_COLLIDE, H12_OPEN):
            self.play(theta.animate.set_value(bounce), run_time=0.7)

        self.at("nearby notch where")
        groove_ring = DashedVMobject(
            RoundedRectangle(corner_radius=0.14, width=1.80, height=0.58, color=GOLD, stroke_width=3.2).move_to(GROOVE_CTR),
            num_dashes=16,
        )
        lbl_groove = T("Co-activator groove", size=28, color=GOLD).move_to([-3.35, 2.65, 0])
        groove_arr = Arrow([-1.55, 2.50, 0], [-0.35, 1.98, 0], buff=0.05, color=GOLD, stroke_width=3.0, tip_length=0.18)
        coact = make_coactivator(center=np.array([6.05, 2.05, 0.0]))
        self.play(Create(groove_ring), FadeIn(lbl_groove), GrowArrow(groove_arr), run_time=2.0)
        self.play(FadeIn(coact), coact.animate.move_to([4.85, 2.05, 0.0]), run_time=2.4)

        self.at("what happens to that groove")
        q = question_card("Helix 12 cannot close. What happens to the groove?", size=30, y=-3.05)
        self.play(FadeIn(q, shift=UP * 0.15), run_time=0.8)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "Helix 12 cannot close. What happens to the groove?"
    SECONDS = 4.5
    CARD = {"size": 30, "y": -3.05}
    RING_AT = (5.85, -2.05, 0)

    def backdrop(self):
        return build_predict_backdrop()


class S07RevealGrooveBlocked(SpokenScene):
    def construct(self):
        hbd = make_hbd_cutaway()
        theta = ValueTracker(H12_OPEN)
        h12 = always_redraw(lambda: make_helix12(theta.get_value()))
        tam = make_tamoxifen(center=POCKET_CTR + RIGHT * 0.65)
        lbl_4oh = T("4-hydroxytamoxifen", size=28, color=RED).move_to([3.95, -0.75, 0])
        groove_ring = DashedVMobject(
            RoundedRectangle(corner_radius=0.14, width=1.80, height=0.58, color=GOLD, stroke_width=3.2).move_to(GROOVE_CTR),
            num_dashes=16,
        )
        coact = make_coactivator(center=np.array([4.85, 2.05, 0.0]))
        q = question_card("Helix 12 cannot close. What happens to the groove?", size=30, y=-3.05)
        tag = scope_tag("schematic")

        self.add(hbd, h12, tam, lbl_4oh, groove_ring, coact, q, tag)
        self.play(FadeOut(q, run_time=0.6), run_time=0.6)

        self.at("cannot close as a lid")
        # One more collision against the protruding side chain before swinging around
        self.play(theta.animate.set_value(H12_COLLIDE), run_time=1.4)
        self.play(theta.animate.set_value(H12_OPEN), run_time=1.2)

        self.at("swings around and lies")
        self.play(theta.animate.set_value(H12_PLUG), run_time=4.2)

        self.at("turns the lid into a plug")
        lbl_plug = T("Helix 12 blocks AF-2", size=30, color=BLUE).move_to([-3.45, 2.75, 0])
        plug_arr = Arrow([-1.58, 2.55, 0], [-0.35, 2.02, 0], buff=0.05, color=BLUE, stroke_width=3.2, tip_length=0.20)
        self.play(FadeOut(groove_ring, run_time=0.4), FadeIn(lbl_plug), GrowArrow(plug_arr), run_time=1.8)

        self.at("af2 groove occupied")
        self.play(coact.animate.move_to([2.40, 2.45, 0.0]), run_time=1.8)

        self.at("coactivators cannot bind")
        self.play(coact.animate.move_to([0.65, 2.78, 0.0]), run_time=0.85)
        self.play(coact.animate.move_to([0.65, 2.66, 0.0]), run_time=0.25)
        self.play(coact.animate.move_to([4.95, 3.00, 0.0]).set_opacity(0), run_time=1.1)
        self.remove(coact)

        self.at("keep the gene off")
        loosen = ValueTracker(0.75)
        chromatin = make_dna_chromatin(loosen, y_center=-2.45, x_left=-5.4, x_right=2.2, shift_mid=-0.20)
        breast_off = boxed_label("Breast: gene OFF", color=RED, size=28).move_to([4.55, -2.35, 0])
        self.play(FadeIn(chromatin), FadeIn(breast_off), run_time=0.5)
        self.play(loosen.animate.set_value(0.0), run_time=1.2)
        self.finish()


class S08Af1TissueContext(SpokenScene):
    def construct(self):
        dna = make_dna_strand(x0=-5.8, x1=5.8, y=-1.90)
        left_mon, right_mon = make_dimer_pair(y_dna=-1.90, scale=0.88)
        tag = scope_tag("schematic")

        pocket_zoom = make_hbd_cutaway().scale(0.85)
        h12_plug = make_helix12(H12_PLUG).scale(0.85)
        tam_zoom = make_tamoxifen(center=POCKET_CTR + RIGHT * 0.65).scale(0.85)
        zoom_grp = VGroup(pocket_zoom, h12_plug, tam_zoom).move_to(ORIGIN)

        self.add(zoom_grp, tag)
        self.play(FadeOut(zoom_grp, run_time=0.55))
        self.play(FadeIn(dna, run_time=0.9), FadeIn(left_mon, run_time=0.9), FadeIn(right_mon, run_time=0.9))

        self.at("second switching surface")
        af1_lbl = T("AF-1 still open", size=30, color=ORANGE).move_to([-4.6, 2.35, 0])
        af1_arr = Arrow([-4.6, 2.02, 0], [-4.8, 0.72, 0], buff=0.05, color=ORANGE, stroke_width=3.5, tip_length=0.22)
        af2_lbl = T("AF-2 plugged", size=28, color=BLUE).move_to([-0.25, 2.45, 0])
        self.play(
            FadeIn(af1_lbl),
            GrowArrow(af1_arr),
            FadeIn(af2_lbl),
            left_mon.af1.animate.set_fill(ORANGE, opacity=0.72),
            right_mon.af1.animate.set_fill(ORANGE, opacity=0.72),
            run_time=2.2,
        )

        self.at("front end surface")
        indep_lbl = T("AF-1 independent of Helix 12", size=28, color=ORANGE).move_to([3.65, 1.55, 0])
        self.play(
            Indicate(left_mon.af1, color=ORANGE, scale_factor=1.15),
            Indicate(right_mon.af1, color=ORANGE, scale_factor=1.15),
            FadeIn(indep_lbl),
            run_time=2.6,
        )

        self.at("outcome can depend")
        tp = TwoPanel("Breast", "Uterus", colors=(RED, GREEN), top=3.05, bottom=-2.55)
        self.play(
            FadeOut(VGroup(dna, left_mon, right_mon, af1_lbl, af1_arr, af2_lbl, indep_lbl), run_time=0.6),
            FadeIn(tp, run_time=0.8),
        )

        l_loosen = ValueTracker(0.0)
        l_dna = make_dna_chromatin(l_loosen, y_center=-1.35, x_left=-5.8, x_right=-0.8, shift_mid=0.0)
        l_rec = make_full_receptor(center=[-3.3, -0.15, 0], scale=0.58, show_tamoxifen=True, plugged=True)
        corep1 = boxed_label("Co-repressor", color=RED, size=24).move_to([-4.65, 1.85, 0])
        corep2 = boxed_label("Co-repressor", color=RED, size=24).move_to([-1.95, 1.85, 0])
        l_off = boxed_label("OFF", color=RED, size=28).move_to([-3.3, -2.08, 0])

        self.play(FadeIn(l_dna), FadeIn(l_rec), FadeIn(corep1), FadeIn(corep2), run_time=1.0)
        self.play(
            corep1.animate.move_to([-4.65, 1.15, 0]),
            corep2.animate.move_to([-1.95, 1.15, 0]),
            FadeIn(l_off),
            run_time=1.8,
        )

        self.at("rich in coactivators")
        r_loosen = ValueTracker(0.0)
        r_dna = make_dna_chromatin(r_loosen, y_center=-1.35, x_left=0.8, x_right=5.8, shift_mid=0.0)
        r_rec = make_full_receptor(center=[3.3, -0.15, 0], scale=0.58, show_tamoxifen=True, plugged=True)
        coact1 = boxed_label("Co-activator", color=GREEN, size=24).move_to([1.95, 1.82, 0])
        coact2 = boxed_label("Co-activator", color=GREEN, size=24).move_to([4.65, 1.82, 0])
        af1_dock_arr = Arrow([1.95, 0.72, 0], [1.95, 0.35, 0], buff=0.03, color=GREEN, stroke_width=3.0, tip_length=0.16)
        r_on = boxed_label("ON", color=GREEN, size=28).move_to([3.3, -2.08, 0])

        self.play(FadeIn(r_dna), FadeIn(r_rec), FadeIn(coact1), FadeIn(coact2), run_time=0.9)
        self.play(coact1.animate.move_to([1.95, 1.06, 0]), run_time=0.9)
        self.play(
            coact2.animate.move_to([1.95, 1.84, 0]),
            GrowArrow(af1_dock_arr),
            r_loosen.animate.set_value(1.0),
            FadeIn(r_on),
            run_time=2.2,
        )
        self.finish()


class S09SermTimescale(SpokenScene):
    def construct(self):
        left_card = RoundedRectangle(corner_radius=0.16, width=5.6, height=1.55, color=RED, stroke_width=2.5,
                                     fill_color=RED, fill_opacity=0.12).move_to([-3.15, 2.35, 0])
        right_card = RoundedRectangle(corner_radius=0.16, width=5.6, height=1.55, color=GREEN, stroke_width=2.5,
                                      fill_color=GREEN, fill_opacity=0.12).move_to([3.15, 2.35, 0])
        l_ttl = T("Breast: OFF", size=28, color=RED).move_to([-3.15, 2.72, 0])
        l_sub = T("AF-2 plugged, co-repressors", size=24, color=TEXT).move_to([-3.15, 2.02, 0])

        r_ttl = T("Uterus: ON", size=28, color=GREEN).move_to([3.15, 2.72, 0])
        r_ttl_bone = T("Uterus & Bone: ON", size=28, color=GREEN).move_to([3.15, 2.72, 0])
        r_sub = T("AF-1 co-activators dominate", size=24, color=TEXT).move_to([3.15, 2.02, 0])

        P, f_camp, f_mrna, f_prot = make_timescale_plot()
        title_tl = T("Schematic timeline", size=28, color=TEXT).move_to([0.0, 0.92, 0])
        tag = scope_tag("schematic")

        self.add(left_card, right_card, l_ttl, l_sub, r_ttl, r_sub, tag)
        self.at("opposes estrogen")
        self.play(left_card.animate.set_fill(RED, opacity=0.28), run_time=1.8)
        self.play(left_card.animate.set_fill(RED, opacity=0.12), run_time=1.4)

        self.at("uterus and bone")
        self.play(
            swap(r_ttl, r_ttl_bone, run_time=0.8),
            right_card.animate.set_fill(GREEN, opacity=0.28),
            run_time=1.8,
        )
        self.play(right_card.animate.set_fill(GREEN, opacity=0.12), run_time=1.4)

        self.at("new rna and protein")
        self.play(Create(P, run_time=1.8), FadeIn(title_tl, run_time=1.0))

        self.at("unlike fast")
        t_camp = ValueTracker(0.05)
        c_camp = P.live_curve(f_camp, t_camp, color=YELLOW, width=6)
        a_camp = _shaded_area(P, f_camp, 0.05, t_camp, color=YELLOW, opacity=0.22)
        d_camp = P.dot(lambda: t_camp.get_value(), lambda: f_camp(t_camp.get_value()), color=YELLOW, ring=TEXT, radius=0.09)
        lbl_camp = T("cAMP: seconds", size=26, color=YELLOW).move_to(P.pt(1.90, 1.06))
        self.add(a_camp, c_camp, d_camp)
        self.play(t_camp.animate.set_value(1.55), FadeIn(lbl_camp), run_time=2.8)

        self.at("the first new messenger")
        t_mrna = ValueTracker(1.30)
        c_mrna = P.live_curve(f_mrna, t_mrna, color=TEAL, width=5.5, x0=1.30)
        a_mrna = _shaded_area(P, f_mrna, 1.30, t_mrna, color=TEAL, opacity=0.15)
        d_mrna = P.dot(lambda: t_mrna.get_value(), lambda: f_mrna(t_mrna.get_value()), color=TEAL, ring=TEXT, radius=0.09)
        lbl_mrna = T("New mRNA: tens of min", size=26, color=TEAL).move_to(P.pt(3.75, 0.88))
        self.add(a_mrna, c_mrna, d_mrna)
        self.play(t_mrna.animate.set_value(5.6), FadeIn(lbl_mrna), run_time=3.5)

        self.at("protein changes build")
        t_prot = ValueTracker(2.60)
        c_prot = P.live_curve(f_prot, t_prot, color=GREEN, width=6, x0=2.60)
        a_prot = _shaded_area(P, f_prot, 2.60, t_prot, color=GREEN, opacity=0.18)
        d_prot = P.dot(lambda: t_prot.get_value(), lambda: f_prot(t_prot.get_value()), color=GREEN, ring=TEXT, radius=0.09)
        lbl_prot = T("New protein: hours", size=26, color=GREEN).move_to(P.pt(7.70, 1.04))
        self.add(a_prot, c_prot, d_prot)
        self.play(
            t_mrna.animate.set_value(9.9),
            t_prot.animate.set_value(9.9),
            FadeIn(lbl_prot, run_time=0.5),
            run_time=1.5,
        )
        self.finish()


class S10Closing(SpokenScene):
    def construct(self):
        P, _, f_mrna, f_prot = make_timescale_plot()
        c_mrna = P.curve(f_mrna, x0=1.30, x1=9.9, color=TEAL, width=4.5, opacity=0.75)
        c_prot = P.curve(f_prot, x0=2.60, x1=9.9, color=GREEN, width=6.0)

        t_cursor = ValueTracker(3.2)
        a_prot = _shaded_area(P, f_prot, 2.60, t_cursor, color=GREEN, opacity=0.22)
        d_prot = P.dot(lambda: t_cursor.get_value(), lambda: f_prot(t_cursor.get_value()), color=GREEN, ring=TEXT, radius=0.10)

        hormone_bar = RoundedRectangle(
            corner_radius=0.08,
            width=2.1,
            height=0.26,
            color=GOLD,
            stroke_width=2.5,
            fill_color=GOLD,
            fill_opacity=0.65,
        ).move_to(P.pt(1.2, 0.96))
        lbl_hormone = T("Hormone", size=24, color=GOLD).next_to(hormone_bar, UP, buff=0.10)
        lbl_outlast = T("Proteins outlast hormone", size=28, color=GREEN).move_to(P.pt(6.8, 1.04))

        dna = make_dna_strand(x0=-5.5, x1=5.5, y=1.30, amp=0.11)
        pocket_chip = boxed_label("Ligand shape (pocket)", color=TEAL, size=28).move_to([-2.7, 2.92, 0])
        helpers_chip = boxed_label("Cell helpers (co-act / co-rep)", color=GREEN, size=28).move_to([2.9, 2.92, 0])
        gene_arrows = VGroup(
            *[Arrow([gx, 1.44, 0], [gx + 0.55, 1.84, 0], buff=0, color=TEAL, stroke_width=3.4, tip_length=0.17) for gx in (-3.8, -0.3, 3.2)]
        )
        lbl_genes = T("Many target genes", size=26, color=CREAM).move_to([0.0, 0.88, 0])
        tag = scope_tag("schematic")

        self.add(P, a_prot, c_mrna, c_prot, d_prot, hormone_bar, lbl_hormone, dna, tag)
        self.play(t_cursor.animate.set_value(4.5), run_time=2.2)

        self.at("after the hormone clears")
        self.play(
            FadeOut(hormone_bar, run_time=1.0),
            FadeOut(lbl_hormone, run_time=1.0),
            t_cursor.animate.set_value(6.8),
            FadeIn(lbl_outlast, shift=UP * 0.1),
            run_time=2.6,
        )

        self.at("reset many genes")
        self.play(
            LaggedStart(*[GrowArrow(a) for a in gene_arrows], lag_ratio=0.35),
            FadeIn(lbl_genes),
            t_cursor.animate.set_value(8.2),
            run_time=2.4,
        )

        self.at("drug is not simply")
        off_on = T("Not simply ON or OFF", size=28, color=GOLD).move_to([0.0, 2.24, 0])
        self.play(FadeIn(off_on, run_time=0.7), t_cursor.animate.set_value(8.6), run_time=0.8)
        self.play(t_cursor.animate.set_value(9.2), run_time=2.2)

        self.at("shape")
        self.play(FadeIn(pocket_chip), FadeIn(helpers_chip), run_time=0.7)

        self.at("each cell's helpers decide")
        self.play(
            FadeOut(off_on, run_time=0.4),
            pocket_chip[0].animate.set_fill(TEAL, opacity=0.35),
            helpers_chip[0].animate.set_fill(GREEN, opacity=0.35),
            t_cursor.animate.set_value(9.9),
            run_time=2.6,
        )
        self.finish()


class S11End(EndCard):
    LINE = "Ligand shape and each cell’s helpers decide whether genes turn on."
