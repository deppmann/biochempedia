# ==============================================================================
# mTORC1: Two Signals at the Lysosome — Animation Plan
# ==============================================================================
#
# COLOUR MAP (one colour per concept for the whole film):
#   EMERALD    = "#2ECC71"   Growth factor / Receptor / Akt / Active Rheb-GTP / Anabolic outputs
#   CRIMSON    = "#E05A47"   TSC brake / Inactive OFF badge / Autophagy block
#   CYAN       = "#38BDF8"   Amino acids / Rag GTPases (delivery track)
#   GOLD_MTOR  = "#F4B942"   mTORC1 complex (and notched Raptor tab)
#   LYSO_TEAL  = "#3FB8C0"   Lysosome membrane and lumen
#   MEMB_BLUE  = "#5B7399"   Plasma membrane bilayer
#   PHOS_YEL   = "#F5D547"   Phosphate (P) stamp / ATP fuel bar
#   TEXT       = "#E8EAF0"   Neutral labels and GDP badge (full opacity, never grey)
#
# CARRIED WORLD:
#   A cell cross-section with the plasma membrane and receptor at the top and the
#   teal lysosome in the lower center. Scenes s01-s02 and s10 show the whole cell;
#   scenes s03-s09 zoom in on the left-center plasma membrane and lysosome rim so
#   the physical switches (Rheb + TSC brake, Rags + notched mTORC1) fill the frame.
#
# WHAT CHANGES IN EACH SPOKEN SCENE (and what drives it):
#   s01_hook                Ribosomes translate an mRNA strand, assembling amino acids into
#                           a growing chain while a live ATP ValueTracker bar drops, then
#                           mTORC1 enters on a computed 2D random walk (rng seed 7).
#   s02_two_questions       Two independent signal lanes (emerald growth-factor track,
#                           cyan amino-acid stream) grow and carry signal tracers to the lysosome.
#   s03_growth_factor_track Growth factor docks at the receptor, Akt activates and glides
#                           to the lysosome, crimson TSC caliper clamps on Rheb and shows
#                           'TSC: Rheb-GTP → Rheb-GDP' word by word as Rheb cuts GTP to GDP,
#                           then Akt stamps a P onto TSC and TSC uncouples and drifts off.
#   s04_rheb_on             TSC clears; Rheb loads GTP and flexes on its lipid tether on
#                           the lysosome while mTORC1 executes a computed 2D random walk
#                           (rng seed 14) out in the cytoplasm across a clear gap.
#   s05_amino_acid_track    Cyan amino acids stream in around the lysosome; paired cyan
#                           Rags flip open into a gripping cup, latch onto mTORC1's
#                           notched Raptor tab, and reel mTORC1 beside Rheb-GTP.
#   s06_predict_setup       Amino acids stream as Rags hold mTORC1 on the lysosome; growth
#                           factor unbinds and leaves the cell, Akt dims, and the question
#                           banner + '?' pose the prediction.
#   s08_predict_reveal      Question clears to 'mTORC1 OFF'; crimson TSC glides back onto
#                           Rheb, drains GTP to GDP, and docked mTORC1 remains silent.
#   s09_both_yes_outputs    Growth factor returns, Akt clears TSC with P, Rheb loads GTP,
#                           mTORC1 fires to 'mTORC1 ON', driving animated Protein synthesis,
#                           Lipid synthesis, and an Autophagy inhibition bar.
#   s10_rule_and_scope      Pulls back to the full cell; both tracks carry synchronized
#                           signals to the lysosome AND gate, plus a schematic glutamine
#                           bypass note, holding the active balanced cell to the end.
# ==============================================================================

import numpy as np
from bp_parts import *

# ---- Film colour palette ----
EMERALD = "#2ECC71"
CRIMSON = "#E05A47"
CYAN = "#38BDF8"
GOLD_MTOR = "#F4B942"
LYSO_TEAL = "#3FB8C0"
MEMB_BLUE = "#5B7399"
PHOS_YEL = "#F5D547"


# ==============================================================================
# Shared builders (same geometry across carried scenes)
# ==============================================================================
def dark_chip(text, color=TEXT, size=28, pad=0.16, fill_opacity=0.22):
    """Boxed label with an opaque BG backing so particles/lines behind never bleed through text."""
    lab = T(text, size, color)
    w, h = lab.width + 2 * pad, lab.height + 2 * pad
    bg = RoundedRectangle(
        corner_radius=min(0.14, h / 2), width=w, height=h,
        stroke_width=0, fill_color=BG, fill_opacity=0.95,
    )
    box = RoundedRectangle(
        corner_radius=min(0.14, h / 2), width=w, height=h,
        stroke_color=color, stroke_width=2.8, fill_color=color, fill_opacity=fill_opacity,
    )
    g = VGroup(bg, box, lab.move_to(box))
    g.box = box
    g.label = lab
    return g


def make_plasma_membrane(y_mid=2.65, width=12.6, rec_x=-3.8):
    """Curved plasma membrane across the top with a receptor pocket at rec_x."""
    xs = np.linspace(-width / 2, width / 2, 120)
    ys_base = y_mid + 0.14 * np.cos(xs * np.pi / width)

    def _curve_with_pocket(dy):
        pts = []
        for x, y in zip(xs, ys_base):
            if abs(x - rec_x) < 0.36:
                t = (x - rec_x) / 0.36
                dip = 0.22 * (1.0 - t * t)
                pts.append([x, y + dy - dip, 0.0])
            else:
                pts.append([x, y + dy, 0.0])
        m = VMobject(stroke_color=MEMB_BLUE, stroke_width=5.0, fill_opacity=0)
        m.set_points_as_corners(pts)
        return m

    outer = _curve_with_pocket(+0.075)
    inner = _curve_with_pocket(-0.075)
    rec_y = y_mid + 0.14 * np.cos(rec_x * np.pi / width) - 0.16
    receptor = Polygon(
        [rec_x - 0.36, rec_y + 0.30, 0],
        [rec_x - 0.20, rec_y - 0.12, 0],
        [rec_x + 0.20, rec_y - 0.12, 0],
        [rec_x + 0.36, rec_y + 0.30, 0],
        [rec_x + 0.22, rec_y + 0.30, 0],
        [rec_x + 0.11, rec_y + 0.02, 0],
        [rec_x - 0.11, rec_y + 0.02, 0],
        [rec_x - 0.22, rec_y + 0.30, 0],
        stroke_color=EMERALD, stroke_width=3.2, fill_color=EMERALD, fill_opacity=0.28,
    )
    memb_lab = T("Plasma membrane", size=24, color=TEXT).move_to([3.7, y_mid + 0.42, 0])
    g = VGroup(outer, inner, receptor, memb_lab)
    g.receptor = receptor
    g.rec_pos = np.array([rec_x, rec_y + 0.16, 0.0])
    g.memb_lab = memb_lab
    return g


def make_gf_ligand(pos=ORIGIN):
    """Emerald growth-factor diamond."""
    return Polygon(
        [0, 0.28, 0], [0.26, 0, 0], [0, -0.28, 0], [-0.26, 0, 0],
        stroke_color=EMERALD, stroke_width=3.2, fill_color=EMERALD, fill_opacity=0.85,
    ).move_to(pos)


def make_lysosome(center=(0.0, -1.65, 0), width=5.6, height=2.1, label_size=28):
    """Teal double-walled lysosome oval with warm lumen fill and clear interior label."""
    c = np.array(center, dtype=float)
    outer = Ellipse(width=width, height=height, stroke_color=LYSO_TEAL, stroke_width=5.0,
                    fill_color=LYSO_TEAL, fill_opacity=0.24).move_to(c)
    inner = Ellipse(width=width - 0.22, height=height - 0.22, stroke_color=LYSO_TEAL,
                    stroke_width=2.2, fill_opacity=0).move_to(c)
    lab = T("Lysosome", size=label_size, color=LYSO_TEAL, weight=BOLD).move_to(c + DOWN * (height * 0.12))
    g = VGroup(outer, inner, lab)
    g.outer = outer
    g.lab = lab
    g.top_y = c[1] + height / 2.0
    return g


def make_mtorc1(pos=(0.0, 0.3, 0), active=False, dim=False):
    """Gold mTORC1 body with its notched Raptor side tab on the bottom-right."""
    col = GOLD_MTOR
    fill_op = 0.52 if active else (0.14 if dim else 0.26)
    sw = 4.8 if active else 3.2
    body = RoundedRectangle(
        corner_radius=0.28, width=2.05, height=0.86,
        stroke_width=0, fill_color=BG, fill_opacity=0.95,
    )
    tint = RoundedRectangle(
        corner_radius=0.28, width=2.05, height=0.86,
        stroke_color=col, stroke_width=sw, fill_color=col, fill_opacity=fill_op,
    )
    raptor = Polygon(
        [0.32, -0.43, 0], [0.85, -0.43, 0], [0.92, -0.70, 0],
        [0.68, -0.70, 0], [0.60, -0.56, 0], [0.52, -0.70, 0], [0.26, -0.70, 0],
        stroke_color=col, stroke_width=2.6, fill_color=col, fill_opacity=fill_op + 0.14,
    )
    lab = T("mTORC1", size=28, color=col, weight=BOLD).move_to(body.get_center())
    g = VGroup(body, tint, raptor, lab).move_to(pos)
    g.body = tint
    g.raptor = raptor
    g.lab = lab
    return g


def make_rheb(rim_x=-2.5, rim_y=-0.45, gtp=True, active=True):
    """Lipid-anchored Rheb on the lysosome rim with a wavy tail and GTP/GDP badge."""
    ts = np.linspace(0, 1, 24)
    pts = [[rim_x + 0.08 * np.sin(3 * np.pi * t), (rim_y - 0.17) + 0.61 * t, 0.0] for t in ts]
    tail = VMobject(stroke_color=EMERALD if active else TEXT, stroke_width=4.2)
    tail.set_points_as_corners(pts)

    col = EMERALD if active else TEXT
    fill_op = 0.28 if active else 0.14
    body_bg = RoundedRectangle(
        corner_radius=0.18, width=1.25, height=0.68,
        stroke_width=0, fill_color=BG, fill_opacity=0.95,
    ).move_to([rim_x, rim_y + 0.78, 0])
    body = RoundedRectangle(
        corner_radius=0.18, width=1.25, height=0.68,
        stroke_color=col, stroke_width=3.2, fill_color=col, fill_opacity=fill_op,
    ).move_to(body_bg.get_center())
    lab = T("Rheb", size=28, color=col, weight=BOLD).move_to(body.get_center())

    nuc_col = EMERALD if gtp else TEXT
    nuc_txt = "GTP" if gtp else "GDP"
    nuc_bg = RoundedRectangle(
        corner_radius=0.12, width=0.88, height=0.52,
        stroke_width=0, fill_color=BG, fill_opacity=0.95,
    ).move_to([rim_x + 1.32, rim_y + 0.78, 0])
    nuc_box = RoundedRectangle(
        corner_radius=0.12, width=0.88, height=0.52,
        stroke_color=nuc_col, stroke_width=2.6, fill_color=nuc_col, fill_opacity=0.24 if gtp else 0.12,
    ).move_to(nuc_bg.get_center())
    nuc_lab = T(nuc_txt, size=24, color=nuc_col, weight=BOLD).move_to(nuc_box.get_center())
    nuc = VGroup(nuc_bg, nuc_box, nuc_lab)

    g = VGroup(tail, body_bg, body, lab, nuc)
    g.tail = tail
    g.body = VGroup(body_bg, body, lab)
    g.nuc = nuc
    g.nuc_lab = nuc_lab
    g.anchor_pt = np.array([rim_x, rim_y, 0.0])
    return g


def make_tsc_brake(rheb_pos, clamped=True):
    """Crimson TSC caliper brake that clamps above Rheb, plus its 'TSC' label."""
    rx, ry = rheb_pos[0], rheb_pos[1]
    y_off = 0.42 if clamped else 0.95
    arch = Polygon(
        [rx - 0.85, ry + y_off - 0.34, 0],
        [rx - 0.85, ry + y_off + 0.24, 0],
        [rx + 0.85, ry + y_off + 0.24, 0],
        [rx + 0.85, ry + y_off - 0.34, 0],
        [rx + 0.68, ry + y_off - 0.34, 0],
        [rx + 0.68, ry + y_off + 0.04, 0],
        [rx - 0.68, ry + y_off + 0.04, 0],
        [rx - 0.68, ry + y_off - 0.34, 0],
        stroke_color=CRIMSON, stroke_width=3.2, fill_color=CRIMSON, fill_opacity=0.38,
    )
    lab = dark_chip("TSC", CRIMSON, size=28, pad=0.16, fill_opacity=0.24).move_to([rx, ry + y_off + 0.58, 0])
    g = VGroup(arch, lab)
    g.arch = arch
    g.lab = lab
    return g


def make_rags(rim_x=1.45, rim_y=-0.45, open_grip=False):
    """Paired cyan Rag proteins anchored on the lysosome rim; flips into gripping cup when open_grip=True."""
    stalk = Line([rim_x, rim_y, 0], [rim_x, rim_y + 0.28, 0], stroke_color=LYSO_TEAL, stroke_width=5.0)
    if open_grip:
        left_arm = Polygon(
            [rim_x - 0.04, rim_y + 0.28, 0], [rim_x - 0.58, rim_y + 0.32, 0],
            [rim_x - 0.62, rim_y + 0.58, 0], [rim_x - 0.38, rim_y + 0.58, 0],
            [rim_x - 0.36, rim_y + 0.48, 0], [rim_x - 0.04, rim_y + 0.48, 0],
            stroke_color=CYAN, stroke_width=3.2, fill_color=CYAN, fill_opacity=0.32,
        )
        right_arm = Polygon(
            [rim_x + 0.04, rim_y + 0.28, 0], [rim_x + 0.58, rim_y + 0.32, 0],
            [rim_x + 0.62, rim_y + 0.58, 0], [rim_x + 0.38, rim_y + 0.58, 0],
            [rim_x + 0.36, rim_y + 0.48, 0], [rim_x + 0.04, rim_y + 0.48, 0],
            stroke_color=CYAN, stroke_width=3.2, fill_color=CYAN, fill_opacity=0.32,
        )
    else:
        left_arm = RoundedRectangle(
            corner_radius=0.12, width=0.52, height=0.32,
            stroke_color=CYAN, stroke_width=2.8, fill_color=CYAN, fill_opacity=0.22,
        ).move_to([rim_x - 0.28, rim_y + 0.42, 0])
        right_arm = RoundedRectangle(
            corner_radius=0.12, width=0.52, height=0.32,
            stroke_color=CYAN, stroke_width=2.8, fill_color=CYAN, fill_opacity=0.22,
        ).move_to([rim_x + 0.28, rim_y + 0.42, 0])

    # Place 'Rags' cleanly outside the lysosome rim to the right-below the cup, away from output arrows
    lab = T("Rags", size=28, color=CYAN, weight=BOLD).move_to([rim_x + 1.10, rim_y + 0.12, 0])
    g = VGroup(stalk, left_arm, right_arm, lab)
    g.stalk = stalk
    g.arms = VGroup(left_arm, right_arm)
    g.lab = lab
    return g


def make_aa_stream(bounds=(3.2, 6.0, -1.8, 1.8), count=16, seed=21):
    """Cyan amino acid dots with computed flow trajectories toward the lysosome."""
    rng = np.random.default_rng(seed)
    x0, x1, y0, y1 = bounds
    dots = VGroup()
    for _ in range(count):
        x = rng.uniform(x0, x1)
        y = rng.uniform(y0, y1)
        d = Dot([x, y, 0], radius=0.11, color=CYAN, fill_opacity=0.90)
        d._vx = rng.uniform(-0.42, -0.18)
        d._vy = rng.uniform(-0.22, 0.18)
        d._bounds = bounds
        dots.add(d)
    dots.set_z_index(-5)
    return dots


def start_aa_flow(dots):
    """Attach computed continuous amino acid flow updater inside its bounding zone."""
    for d in dots:
        x0, x1, y0, y1 = d._bounds

        def _u(mob, dt, x0=x0, x1=x1, y0=y0, y1=y1):
            mob.shift([mob._vx * dt, mob._vy * dt, 0])
            p = mob.get_center()
            if p[0] < x0:
                mob.set_x(x1)
            elif p[0] > x1:
                mob.set_x(x0)
            if p[1] < y0:
                mob.set_y(y1)
            elif p[1] > y1:
                mob.set_y(y0)

        d.add_updater(_u)
    return dots


def start_random_walk(mob, center, rx=0.65, ry=0.35, seed=7, speed=1.4):
    """Computed smoothed 2D random walk around `center`."""
    rng = np.random.default_rng(seed)
    n_knots = 32
    angles = np.cumsum(rng.normal(0, 0.85, size=n_knots))
    xs = rx * np.sin(angles + rng.uniform(0, TAU))
    ys = ry * np.cos(angles * 0.7 + rng.uniform(0, TAU))
    c = np.array(center, dtype=float)
    mob._walk_t = 0.0

    def _u(m, dt):
        m._walk_t += dt * speed
        idx = m._walk_t % n_knots
        i0 = int(np.floor(idx))
        i1 = (i0 + 1) % n_knots
        f = idx - i0
        f = f * f * (3 - 2 * f)
        x = (1 - f) * xs[i0] + f * xs[i1]
        y = (1 - f) * ys[i0] + f * ys[i1]
        m.move_to(c + np.array([x, y, 0.0]))

    mob.add_updater(_u)
    return mob


def make_phos_badge(pos):
    """Yellow 'P' phosphate stamp with generous ring padding."""
    c = Circle(radius=0.28, stroke_color=PHOS_YEL, stroke_width=2.5, fill_color=PHOS_YEL, fill_opacity=0.95)
    t = T("P", size=24, color=BG, weight=BOLD).move_to(c)
    g = VGroup(c, t).move_to(pos)
    return g


def build_zoomed_stage(gf_present=True, akt_active=True, tsc_present=False,
                       rheb_gtp=True, rag_open=True, mtor_docked=True, mtor_active=False):
    """Rebuild the zoomed lysosome + plasma-membrane view cleanly at any state."""
    memb = make_plasma_membrane(y_mid=2.35, width=12.6, rec_x=-3.8)
    lyso = make_lysosome(center=(-0.2, -1.95, 0), width=9.4, height=3.1, label_size=30)
    rheb = make_rheb(rim_x=-2.5, rim_y=-0.45, gtp=rheb_gtp, active=rheb_gtp)
    rags = make_rags(rim_x=1.45, rim_y=-0.45, open_grip=rag_open)

    mtor_pos = (0.85, 0.58, 0) if mtor_docked else (3.3, 1.15, 0)
    mtor = make_mtorc1(mtor_pos, active=mtor_active)

    parts = VGroup(memb, lyso, rheb, rags, mtor)
    parts.memb = memb
    parts.lyso = lyso
    parts.rheb = rheb
    parts.rags = rags
    parts.mtor = mtor

    if gf_present:
        gf = make_gf_ligand(memb.rec_pos + UP * 0.14)
        parts.add(gf)
        parts.gf = gf
    else:
        parts.gf = None

    akt_col = EMERALD if akt_active else TEXT
    akt = dark_chip("Akt", akt_col, size=28, pad=0.16, fill_opacity=0.25 if akt_active else 0.10)
    akt.move_to([-3.8, 1.62, 0])
    parts.add(akt)
    parts.akt = akt

    if tsc_present:
        tsc = make_tsc_brake([-2.5, 0.33, 0], clamped=True)
        parts.add(tsc)
        parts.tsc = tsc
    else:
        parts.tsc = None

    return parts


# ==============================================================================
# Scenes
# ==============================================================================
class S00Title(TitleCard):
    LESSON = "mTOR and AMPK: Reading Nutrients and Energy"
    TITLE = "mTORC1: Two Signals at the Lysosome"


class S01Hook(SpokenScene):
    def construct(self):
        memb = make_plasma_membrane(y_mid=2.65, width=12.6, rec_x=-3.8)
        lyso = make_lysosome(center=(0.0, -1.65, 0), width=5.6, height=2.1, label_size=28)

        mrna = Line([2.1, 0.72, 0], [5.9, 0.72, 0], stroke_color=TEXT, stroke_width=4.0)
        ribo = RoundedRectangle(
            corner_radius=0.22, width=0.95, height=0.58,
            stroke_color=TEXT, stroke_width=3.0, fill_color=BG, fill_opacity=0.94,
        ).move_to([2.45, 0.72, 0])
        ribo_lab = T("New protein", size=28, color=TEXT).move_to([4.0, 1.78, 0])

        aa_dots = start_aa_flow(make_aa_stream(bounds=(3.1, 5.9, -2.0, 0.0), count=14, seed=11))
        aa_lab = T("Amino acids", size=28, color=CYAN).move_to([4.6, -2.50, 0])

        atp_level = ValueTracker(1.0)
        atp_bg = RoundedRectangle(
            corner_radius=0.08, width=2.5, height=0.38,
            stroke_color=PHOS_YEL, stroke_width=2.8, fill_opacity=0,
        ).move_to([-4.2, 0.65, 0])
        atp_fill = always_redraw(lambda: RoundedRectangle(
            corner_radius=0.06, width=max(0.08, 2.40 * atp_level.get_value()), height=0.30,
            stroke_width=0, fill_color=PHOS_YEL, fill_opacity=0.85,
        ).align_to(atp_bg.get_left() + RIGHT * 0.05, LEFT).set_y(atp_bg.get_y()))
        atp_lab = T("ATP", size=28, color=PHOS_YEL).next_to(atp_bg, UP, buff=0.18)

        self.add(memb, lyso, mrna, ribo, ribo_lab, aa_dots, aa_lab, atp_bg, atp_fill, atp_lab)

        # Beat 1: ribosome builds polypeptide chain from amino acids
        chain = VGroup()
        self.at("new protein")
        for i in range(6):
            bead = Dot([2.45 + i * 0.45, 0.30, 0], radius=0.11, color=CYAN)
            chain.add(bead)
            self.play(ribo.animate.shift(RIGHT * 0.45), FadeIn(bead, scale=0.7), run_time=0.48)

        # Beat 2: ATP burns down continuously while protein builds
        self.at("cellular energy")
        self.play(
            atp_level.animate.set_value(0.42),
            ribo.animate.shift(RIGHT * 0.45),
            run_time=2.6,
            rate_func=linear,
        )

        # Beat 3: Decision question while ATP keeps slipping
        self.at("decide it can")
        q_mark = T("?", size=56, color=GOLD_MTOR, weight=BOLD).move_to([0.0, 0.50, 0])
        self.play(
            FadeIn(q_mark, scale=0.8),
            atp_level.animate.set_value(0.30),
            run_time=2.2,
            rate_func=linear,
        )

        # Beat 4: Starting without permission wastes scarce supplies -> X above ribosome, ATP drops further
        self.at("without permission")
        stall = T("×", size=44, color=CRIMSON, weight=BOLD).move_to([ribo.get_x(), 1.25, 0])
        self.play(FadeIn(stall), atp_level.animate.set_value(0.18), run_time=2.8, rate_func=linear)
        self.play(FadeOut(stall), FadeOut(q_mark), run_time=0.8)

        # Beat 5: mTORC1 enters in center and runs computed random walk
        self.at("central kinase")
        mtor = make_mtorc1([0.0, 0.45, 0], active=False)
        self.play(FadeIn(mtor, scale=0.85), run_time=0.9)
        start_random_walk(mtor, center=(0.0, 0.45, 0), rx=0.55, ry=0.24, seed=7, speed=1.5)
        self.finish()


class S02TwoQuestions(SpokenScene):
    def construct(self):
        memb = make_plasma_membrane(y_mid=2.65, width=12.6, rec_x=-3.8)
        lyso = make_lysosome(center=(0.0, -1.65, 0), width=5.6, height=2.1, label_size=28)
        mtor = make_mtorc1([0.0, 0.45, 0], active=False)
        # Keep aa_dots strictly above q2_box and outside lysosome so lane_r1 starts from the cloud
        aa_dots = start_aa_flow(make_aa_stream(bounds=(2.8, 5.8, 1.40, 2.25), count=14, seed=21))

        self.add(memb, lyso, mtor, aa_dots)
        start_random_walk(mtor, center=(0.0, 0.45, 0), rx=0.35, ry=0.20, seed=9, speed=1.4)

        # Beat 1: mTORC1 checks two questions
        self.at("switches on")
        q1_box = dark_chip("Growth factor?", EMERALD, size=28, pad=0.18).move_to([-3.8, 0.72, 0])
        q2_box = dark_chip("Amino acids?", CYAN, size=28, pad=0.18).move_to([3.8, 0.72, 0])
        self.wait(1.5)

        # Beat 2: Left emerald track grows down to lysosome
        self.at("growth factor")
        lane_l1 = Arrow(memb.rec_pos + DOWN * 0.25, q1_box.get_top() + UP * 0.14,
                        color=EMERALD, stroke_width=4.5, buff=0)
        lane_l2 = Arrow(q1_box.get_bottom() + DOWN * 0.14, [-1.95, -0.75, 0],
                        color=EMERALD, stroke_width=4.5, buff=0)
        self.play(FadeIn(q1_box, shift=DOWN * 0.2), GrowArrow(lane_l1), run_time=1.3)
        self.play(GrowArrow(lane_l2), run_time=1.2)

        # Beat 3: Right cyan track grows from amino acids down to lysosome
        self.at("amino acids")
        lane_r1 = Arrow([3.8, 1.75, 0], q2_box.get_top() + UP * 0.14,
                        color=CYAN, stroke_width=4.5, buff=0)
        lane_r2 = Arrow(q2_box.get_bottom() + DOWN * 0.14, [1.95, -0.75, 0],
                        color=CYAN, stroke_width=4.5, buff=0)
        self.play(FadeIn(q2_box, shift=DOWN * 0.2), GrowArrow(lane_r1), run_time=1.3)
        self.play(GrowArrow(lane_r2), run_time=1.2)

        # Beat 4: Two signal tracers follow lane_l1->lane_l2 and lane_r1->lane_r2 behind the boxes
        self.at("two independent tracks")
        pulse_l = Dot(memb.rec_pos + DOWN * 0.25, radius=0.14, color=EMERALD).set_z_index(-2)
        pulse_r = Dot([3.8, 1.75, 0], radius=0.14, color=CYAN).set_z_index(-2)
        self.add(pulse_l, pulse_r, scope_tag("schematic", size=24, color=TEXT))
        self.play(
            pulse_l.animate.move_to(q1_box.get_bottom() + DOWN * 0.14),
            pulse_r.animate.move_to(q2_box.get_bottom() + DOWN * 0.14),
            run_time=1.3,
            rate_func=linear,
        )
        self.play(
            pulse_l.animate.move_to([-1.95, -0.75, 0]),
            pulse_r.animate.move_to([1.95, -0.75, 0]),
            run_time=1.7,
            rate_func=linear,
        )
        self.play(FadeOut(pulse_l), FadeOut(pulse_r), run_time=0.4)
        self.finish()


class S03GrowthFactorTrack(SpokenScene):
    def construct(self):
        memb = make_plasma_membrane(y_mid=2.35, width=12.6, rec_x=-3.8)
        lyso = make_lysosome(center=(-0.2, -1.95, 0), width=9.4, height=3.1, label_size=30)
        self.add(memb, lyso)

        # Beat 1: trace the growth factor track from receptor down toward the lysosome
        self.at("growth factor track")
        gf = make_gf_ligand([-3.8, 3.55, 0])
        gf_lab = T("Growth factor", size=28, color=EMERALD).next_to(gf, RIGHT, buff=0.25)
        track_lane = Arrow([-3.8, 2.15, 0], [-2.75, -0.25, 0], color=EMERALD, stroke_width=5.5, buff=0)
        self.play(FadeIn(gf), FadeIn(gf_lab), GrowArrow(track_lane), run_time=2.2)
        self.play(FadeOut(track_lane), run_time=0.8)

        # Beat 2: insulin binds receptor, activates Akt, Akt glides down beside Rheb
        self.at("activates the kinase")
        akt = dark_chip("Akt", EMERALD, size=28, pad=0.16, fill_opacity=0.25).move_to([-3.8, 1.65, 0])
        self.play(gf.animate.move_to(memb.rec_pos + UP * 0.14), FadeOut(gf_lab), run_time=1.0)
        self.play(FadeIn(akt, scale=0.85), run_time=0.9)
        self.play(akt.animate.move_to([-4.45, 0.90, 0]), run_time=2.0)

        # Beat 3: On the lysosome sits Rheb; crimson TSC caliper clamps onto Rheb and cuts GTP -> GDP
        self.at("on the lysosome")
        rheb_gtp = make_rheb(rim_x=-2.5, rim_y=-0.45, gtp=True, active=False)
        tsc = make_tsc_brake([-2.5, 0.33, 0], clamped=True)
        tsc_high = tsc.copy().shift(RIGHT * 1.6 + UP * 0.5).set_opacity(0)
        self.play(FadeIn(rheb_gtp), run_time=1.3)

        mech_tsc = T("TSC:", size=28, color=CRIMSON, weight=BOLD)
        mech_rheb = T("Rheb-", size=28, color=EMERALD, weight=BOLD)
        mech_gtp = T("GTP", size=28, color=EMERALD, weight=BOLD)
        mech_gtp_grp = VGroup(mech_rheb, mech_gtp).arrange(RIGHT, buff=0.06, aligned_edge=DOWN)
        mech_arr = T("→", size=28, color=CRIMSON, weight=BOLD)
        mech_gdp = T("Rheb-GDP", size=28, color=TEXT, weight=BOLD)
        mech_row = VGroup(mech_tsc, mech_gtp_grp, mech_arr, mech_gdp).arrange(RIGHT, buff=0.14, aligned_edge=DOWN)
        mech_arr.set_y(mech_gtp_grp.get_y())
        mech_row.move_to([3.0, 0.85, 0])

        self.at("the tsc complex")
        self.play(
            Transform(tsc_high, tsc),
            FadeIn(mech_tsc, shift=RIGHT * 0.1),
            run_time=1.4,
        )
        self.remove(tsc_high)
        self.add(tsc)

        self.at("making reb")
        self.play(FadeIn(mech_rheb, shift=RIGHT * 0.06), run_time=0.45)

        self.at("gtp")
        self.play(FadeIn(mech_gtp, shift=RIGHT * 0.06), run_time=0.45)

        self.at("to gdp")
        rheb_off = make_rheb(rim_x=-2.5, rim_y=-0.45, gtp=False, active=False)
        self.play(
            FadeIn(mech_arr, shift=RIGHT * 0.06),
            FadeIn(mech_gdp, shift=RIGHT * 0.06),
            swap(rheb_gtp.nuc, rheb_off.nuc, run_time=0.8),
            run_time=0.9,
        )

        # Beat 4: Akt stamps yellow P on TSC; TSC uncouples and drifts right-up into open cytoplasm
        self.at("phosphorylates")
        phos = make_phos_badge([-3.45, 1.33, 0])
        self.play(FadeIn(phos, scale=0.6), run_time=0.6)

        self.at("lifting that")
        tsc_with_p = VGroup(tsc, phos)
        self.play(
            tsc_with_p.animate.shift(RIGHT * 1.55 + UP * 0.45),
            FadeOut(mech_row),
            run_time=1.8,
        )
        self.finish()


class S04RhebOn(SpokenScene):
    def construct(self):
        memb = make_plasma_membrane(y_mid=2.35, width=12.6, rec_x=-3.8)
        lyso = make_lysosome(center=(-0.2, -1.95, 0), width=9.4, height=3.1, label_size=30)
        gf = make_gf_ligand(memb.rec_pos + UP * 0.14)
        akt = dark_chip("Akt", EMERALD, size=28, pad=0.16, fill_opacity=0.25).move_to([-4.45, 0.90, 0])
        rheb = make_rheb(rim_x=-2.5, rim_y=-0.45, gtp=False, active=False)
        tsc_prev = make_tsc_brake([-2.5, 0.33, 0], clamped=True)
        phos_prev = make_phos_badge([-3.45, 1.33, 0])
        tsc_leaving = VGroup(tsc_prev, phos_prev).shift(RIGHT * 1.55 + UP * 0.45)

        self.add(memb, lyso, gf, akt, rheb, tsc_leaving)

        # Beat 1: TSC finishes drifting away
        self.at("brake lifted")
        self.play(FadeOut(tsc_leaving, shift=RIGHT * 0.8 + UP * 0.2), run_time=1.4)

        # Beat 2: Rheb loads GTP and glows emerald
        self.at("loaded with")
        rheb_on = make_rheb(rim_x=-2.5, rim_y=-0.45, gtp=True, active=True)
        self.play(
            ReplacementTransform(rheb, rheb_on),
            akt.animate.move_to([-3.8, 1.62, 0]),
            run_time=1.8,
        )

        # Beat 3: mTORC1 appears across the cytoplasmic gap and immediately begins computed random walk
        self.at("direct activator")
        mtor = make_mtorc1([3.3, 1.15, 0], active=False)
        act_arc = Arrow([-0.60, 0.45, 0], [1.60, 0.85, 0], color=EMERALD, stroke_width=4.5, buff=0)
        self.play(FadeIn(mtor), GrowArrow(act_arc), run_time=1.2)
        start_random_walk(mtor, center=(3.3, 1.15, 0), rx=0.65, ry=0.35, seed=14, speed=1.4)
        self.wait(1.8)
        self.play(FadeOut(act_arc), run_time=0.8)

        # Beat 4: Lipid tail anchors Rheb to the lysosome membrane (flexes gently on tether)
        self.at("lipid tail anchors")
        tail_lab = T("Lipid tail", size=28, color=EMERALD).move_to([-4.45, -0.08, 0])
        tail_ptr = Arrow(tail_lab.get_right() + RIGHT * 0.1, [-2.68, -0.22, 0],
                         color=EMERALD, stroke_width=3.5, buff=0)
        self.play(FadeIn(tail_lab), GrowArrow(tail_ptr), run_time=1.2)
        for _ in range(2):
            self.play(rheb_on.animate.shift(RIGHT * 0.12), run_time=1.0, rate_func=there_and_back)

        # Beat 5: mTORC1 continues its computed random walk out in the cytoplasm
        self.at("drifts out in the cytoplasm")
        self.finish()


class S05AminoAcidTrack(SpokenScene):
    def construct(self):
        memb = make_plasma_membrane(y_mid=2.35, width=12.6, rec_x=-3.8)
        lyso = make_lysosome(center=(-0.2, -1.95, 0), width=9.4, height=3.1, label_size=30)
        gf = make_gf_ligand(memb.rec_pos + UP * 0.14)
        akt = dark_chip("Akt", EMERALD, size=28, pad=0.16, fill_opacity=0.25).move_to([-3.8, 1.62, 0])
        rheb = make_rheb(rim_x=-2.5, rim_y=-0.45, gtp=True, active=True)
        mtor = make_mtorc1([3.75, 1.25, 0], active=False)

        self.add(memb, lyso, gf, akt, rheb, mtor)
        start_random_walk(mtor, center=(3.75, 1.25, 0), rx=0.40, ry=0.22, seed=14, speed=1.4)

        # Beat 1: amino acid stream enters on the right (clean of lysosome and labels)
        self.at("amino acid track")
        aa_dots = start_aa_flow(make_aa_stream(bounds=(4.65, 6.1, -1.8, 1.8), count=12, seed=31))
        aa_lab = T("Amino acids", size=28, color=CYAN).move_to([5.45, -2.80, 0])
        self.play(FadeIn(aa_dots), FadeIn(aa_lab), run_time=1.1)

        # Beat 2: Rag proteins sit anchored on lysosome surface
        self.at("another pair of small switches")
        rags_closed = make_rags(rim_x=1.45, rim_y=-0.45, open_grip=False)
        self.play(FadeIn(rags_closed, shift=UP * 0.2), run_time=1.3)

        # Beat 3: Rags do not activate the kinase directly (cross placed cleanly above dashed line)
        self.at("do not activate")
        no_act = DashedLine([1.45, 0.15, 0], [2.45, 0.70, 0], color=CRIMSON, stroke_width=3.5)
        cross = T("×", size=34, color=CRIMSON, weight=BOLD).move_to([1.72, 0.72, 0])
        self.play(Create(no_act), FadeIn(cross), run_time=1.0)
        self.wait(1.6)
        self.play(FadeOut(no_act), FadeOut(cross), run_time=0.6)

        # Beat 4: Amino acids rise -> more dots flow in, Rags flip open into gripping cup
        self.at("when amino acids rise")
        more_aa = start_aa_flow(make_aa_stream(bounds=(4.65, 6.1, -1.8, 1.8), count=10, seed=37))
        rags_open = make_rags(rim_x=1.45, rim_y=-0.45, open_grip=True)
        self.play(FadeIn(more_aa), ReplacementTransform(rags_closed, rags_open), run_time=1.4)

        # Beat 5: Rags grab mTORC1 via its Raptor tab and pull it onto the lysosome beside Rheb-GTP
        self.at("grab")
        mtor.clear_updaters()
        self.play(mtor.animate.move_to([0.85, 0.58, 0]), run_time=2.5)
        self.finish()


class S06PredictSetup(SpokenScene):
    def construct(self):
        stage = build_zoomed_stage(
            gf_present=True, akt_active=True, tsc_present=False,
            rheb_gtp=True, rag_open=True, mtor_docked=True, mtor_active=False,
        )
        aa_dots = start_aa_flow(make_aa_stream(bounds=(4.65, 6.1, -1.8, 1.8), count=18, seed=41))
        aa_lab = T("Amino acids", size=28, color=CYAN).move_to([5.45, -2.80, 0])
        self.add(stage, aa_dots, aa_lab)

        # Beat 1: strict cellular gate
        self.at("strict cellular gate")
        gate_box = DashedVMobject(
            RoundedRectangle(corner_radius=0.25, width=6.8, height=2.24, stroke_color=GOLD_MTOR, stroke_width=2.5)
        ).move_to([-0.05, 0.38, 0])
        self.play(Create(gate_box), run_time=1.2)
        self.play(FadeOut(gate_box), run_time=0.8)

        # Beat 2: amino acids plentiful, Rags hold mTORC1 on lysosome
        self.at("amino acids are plentiful")
        self.play(stage.rags.animate.shift(UP * 0.05), stage.mtor.animate.shift(UP * 0.05),
                  run_time=1.0, rate_func=there_and_back)

        # Beat 3: remove the growth factor from outside the cell -> GF leaves cleanly below y=3.0, Akt dims
        self.at("remove the growth factor")
        akt_dim = dark_chip("Akt", TEXT, size=28, pad=0.16, fill_opacity=0.08).move_to(stage.akt.get_center())
        self.play(
            stage.gf.animate.shift(UP * 0.45).set_opacity(0),
            swap(stage.akt, akt_dim, run_time=1.0),
            run_time=1.6,
        )

        # Beat 4: Does the kinase switch on, or stay off? -> show top question banner + '?' after GF exits
        self.at("switch on or stay off")
        q_card = question_card(
            "Amino acids present, no growth factor: mTORC1 ON or OFF?",
            y=3.25, max_w=10.2, size=28,
        )
        q_mark = T("?", size=48, color=GOLD_MTOR, weight=BOLD).move_to([0.85, 1.50, 0])
        self.play(FadeIn(q_card), FadeIn(q_mark, scale=0.8), run_time=0.8)
        self.finish()


class S07Pause(PredictPause):
    QUESTION = "Amino acids present, no growth factor: mTORC1 ON or OFF?"
    CARD = {"y": 3.25, "max_w": 10.2, "size": 28}
    RING_AT = (5.9, 3.25, 0)
    SECONDS = 4.5

    def backdrop(self):
        stage = build_zoomed_stage(
            gf_present=False, akt_active=False, tsc_present=False,
            rheb_gtp=True, rag_open=True, mtor_docked=True, mtor_active=False,
        )
        aa_dots = start_aa_flow(make_aa_stream(bounds=(4.65, 6.1, -1.8, 1.8), count=18, seed=41))
        aa_lab = T("Amino acids", size=28, color=CYAN).move_to([5.45, -2.80, 0])
        q_mark = T("?", size=48, color=GOLD_MTOR, weight=BOLD).move_to([0.85, 1.50, 0])
        return VGroup(stage, aa_dots, aa_lab, q_mark)


class S08PredictReveal(SpokenScene):
    def construct(self):
        stage = build_zoomed_stage(
            gf_present=False, akt_active=False, tsc_present=False,
            rheb_gtp=True, rag_open=True, mtor_docked=True, mtor_active=False,
        )
        aa_dots = start_aa_flow(make_aa_stream(bounds=(4.65, 6.1, -1.8, 1.8), count=18, seed=41))
        aa_lab = T("Amino acids", size=28, color=CYAN).move_to([5.45, -2.80, 0])
        q_card = question_card(
            "Amino acids present, no growth factor: mTORC1 ON or OFF?",
            y=3.25, max_w=10.2, size=28,
        )
        q_mark = T("?", size=48, color=GOLD_MTOR, weight=BOLD).move_to([0.85, 1.50, 0])
        self.add(stage, aa_dots, aa_lab, q_card, q_mark)

        # Beat 1: It stays off — swap cleanly so '?' never overlaps 'mTORC1 OFF'
        self.at("it stays off")
        off_badge = dark_chip("mTORC1 OFF", CRIMSON, size=30, pad=0.18, fill_opacity=0.22).move_to([0.85, 1.68, 0])
        self.play(swap(VGroup(q_card, q_mark), off_badge, run_time=1.0))

        # Beat 2: Akt quiets down and TSC brake descends cleanly onto Rheb from open cytoplasm
        self.at("quiets down")
        tsc = make_tsc_brake([-2.5, 0.33, 0], clamped=True)
        tsc_start = tsc.copy().shift(UP * 0.58).set_opacity(0)
        self.play(
            FadeOut(stage.akt),
            Transform(tsc_start, tsc),
            run_time=2.2,
        )

        # Beat 3: TSC drains Rheb of GTP -> flips to GDP
        self.at("drains")
        rheb_off = make_rheb(rim_x=-2.5, rim_y=-0.45, gtp=False, active=False)
        self.play(ReplacementTransform(stage.rheb, rheb_off), run_time=1.8)

        # Beat 4: Even sitting right beside Rheb, docked mTORC1 stays silent
        self.at("sitting right beside")
        gap_line = DashedLine([-0.70, 0.42, 0], [-0.24, 0.42, 0], color=CRIMSON, stroke_width=4.0)
        self.play(Create(gap_line), run_time=1.0)
        self.finish()


class S09BothYesOutputs(SpokenScene):
    def construct(self):
        stage = build_zoomed_stage(
            gf_present=False, akt_active=False, tsc_present=True,
            rheb_gtp=False, rag_open=True, mtor_docked=True, mtor_active=False,
        )
        stage.remove(stage.akt)
        # Keep aa_dots cleanly in the lower-right cytoplasmic zone outside lysosome and below output boxes
        aa_dots = start_aa_flow(make_aa_stream(bounds=(4.65, 6.1, -2.05, -0.82), count=16, seed=41))
        aa_lab = T("Amino acids", size=28, color=CYAN).move_to([5.45, -2.80, 0])
        status = dark_chip("mTORC1 OFF", CRIMSON, size=30, pad=0.18, fill_opacity=0.22).move_to([0.85, 1.68, 0])
        self.add(stage, aa_dots, aa_lab, status)

        # Beat 1: Restore the growth factor
        self.at("restore the growth factor")
        gf = make_gf_ligand([-3.8, 3.35, 0])
        self.play(FadeIn(gf), run_time=0.5)
        self.play(gf.animate.move_to(stage.memb.rec_pos + UP * 0.14), run_time=1.1)

        # Beat 2: Akt clears the TSC brake (fast enough to finish before 'lights up with' at 8.34s)
        self.at("clears the")
        akt = dark_chip("Akt", EMERALD, size=28, pad=0.16, fill_opacity=0.25).move_to([-3.8, 1.62, 0])
        self.play(FadeIn(akt), run_time=0.4)
        self.play(akt.animate.move_to([-4.45, 0.90, 0]), run_time=0.6)
        phos = make_phos_badge([-3.45, 1.33, 0])
        self.play(FadeIn(phos, scale=0.7), run_time=0.3)
        self.play(VGroup(stage.tsc, phos).animate.shift(UP * 0.62 + RIGHT * 0.10).set_opacity(0), run_time=0.7)

        # Beat 3: Rheb lights up with GTP
        self.at("lights up with")
        rheb_on = make_rheb(rim_x=-2.5, rim_y=-0.45, gtp=True, active=True)
        self.play(ReplacementTransform(stage.rheb, rheb_on), run_time=1.0)

        # Beat 4: docked mTORC1 fires
        self.at("fires")
        fire_arc = Arrow([-0.74, 0.35, 0], [-0.24, 0.48, 0], color=EMERALD, stroke_width=5.0, buff=0)
        mtor_on = make_mtorc1([0.85, 0.58, 0], active=True)
        on_badge = dark_chip("mTORC1 ON", GOLD_MTOR, size=30, pad=0.18, fill_opacity=0.28).move_to([0.85, 1.68, 0])
        self.play(
            GrowArrow(fire_arc),
            ReplacementTransform(stage.mtor, mtor_on),
            swap(status, on_badge, run_time=0.7),
            run_time=1.0,
        )

        # Beat 5: Protein synthesis & Lipid synthesis outputs (clear of Rags at [2.55, -0.33])
        self.at("protein building")
        out_p = dark_chip("Protein synthesis", EMERALD, size=28, pad=0.16, fill_opacity=0.20).move_to([4.45, 1.82, 0])
        arr_p = Arrow([1.95, 0.80, 0], out_p.get_left() + LEFT * 0.14, color=EMERALD, stroke_width=4.0, buff=0)
        self.play(GrowArrow(arr_p), FadeIn(out_p, shift=RIGHT * 0.2), run_time=0.85)

        self.at("lipid synthesis")
        out_l = dark_chip("Lipid synthesis", EMERALD, size=28, pad=0.16, fill_opacity=0.20).move_to([4.45, 0.82, 0])
        arr_l = Arrow([1.95, 0.58, 0], out_l.get_left() + LEFT * 0.14, color=EMERALD, stroke_width=4.0, buff=0)
        self.play(GrowArrow(arr_l), FadeIn(out_l, shift=RIGHT * 0.2), run_time=0.9)

        # Beat 6: Holds off cellular self-digestion, autophagy (crimson flat-headed bar)
        self.at("self")
        out_a = dark_chip("Autophagy", CRIMSON, size=28, pad=0.16, fill_opacity=0.18).move_to([4.75, -0.18, 0])
        stem_a = Line([1.95, 0.38, 0], out_a.get_left() + LEFT * 0.12, color=CRIMSON, stroke_width=4.0)
        bar_head = Line(
            out_a.get_left() + LEFT * 0.12 + UP * 0.22,
            out_a.get_left() + LEFT * 0.12 + DOWN * 0.22,
            color=CRIMSON, stroke_width=5.0,
        )
        self.add(scope_tag("schematic", size=24, color=TEXT))
        self.play(Create(stem_a), Create(bar_head), FadeIn(out_a, shift=RIGHT * 0.2), run_time=1.3)
        self.finish()


class S10RuleAndScope(SpokenScene):
    def construct(self):
        memb = make_plasma_membrane(y_mid=2.65, width=12.6, rec_x=-3.8)
        lyso = make_lysosome(center=(0.0, -1.65, 0), width=5.6, height=2.1, label_size=28)
        gf = make_gf_ligand(memb.rec_pos + UP * 0.14)
        # Keep aa_dots strictly above deliv_box and outside lysosome so arr_r1 starts from the cloud
        aa_dots = start_aa_flow(make_aa_stream(bounds=(2.6, 5.8, 1.15, 2.25), count=14, seed=51))

        mtor = make_mtorc1([0.0, 0.18, 0], active=True)
        gate_lab = dark_chip("AND gate", GOLD_MTOR, size=28, pad=0.16, fill_opacity=0.25).move_to([0.0, 1.35, 0])

        rheb_box = dark_chip("Rheb ON", EMERALD, size=28, pad=0.16, fill_opacity=0.22).move_to([-3.8, 0.30, 0])
        deliv_box = dark_chip("mTORC1 delivered", CYAN, size=28, pad=0.16, fill_opacity=0.22).move_to([3.8, 0.30, 0])

        arr_l1 = Arrow(memb.rec_pos + DOWN * 0.25, rheb_box.get_top() + UP * 0.12,
                       color=EMERALD, stroke_width=4.5, buff=0)
        arr_l2 = Arrow(rheb_box.get_right() + RIGHT * 0.12, mtor.get_left() + LEFT * 0.14,
                       color=EMERALD, stroke_width=4.5, buff=0)
        arr_r1 = Arrow([3.8, 1.70, 0], deliv_box.get_top() + UP * 0.12,
                       color=CYAN, stroke_width=4.5, buff=0)
        arr_r2 = Arrow(deliv_box.get_left() + LEFT * 0.12, mtor.get_right() + RIGHT * 0.14,
                       color=CYAN, stroke_width=4.5, buff=0)

        self.add(memb, lyso, gf, aa_dots, mtor, gate_lab, rheb_box, deliv_box,
                 arr_l1, arr_l2, arr_r1, arr_r2, scope_tag("schematic", size=24, color=TEXT))

        # Beat 1: both growth factors and amino acids
        self.at("both growth factors")
        p1 = Dot(memb.rec_pos + DOWN * 0.25, radius=0.13, color=EMERALD).set_z_index(-2)
        p2 = Dot([3.8, 1.70, 0], radius=0.13, color=CYAN).set_z_index(-2)
        self.add(p1, p2)
        self.play(
            p1.animate.move_to(rheb_box.get_center()),
            p2.animate.move_to(deliv_box.get_center()),
            run_time=1.0,
            rate_func=linear,
        )
        self.play(
            p1.animate.move_to(mtor.get_left() + LEFT * 0.14),
            p2.animate.move_to(mtor.get_right() + RIGHT * 0.14),
            run_time=1.6,
            rate_func=linear,
        )
        self.play(FadeOut(p1), FadeOut(p2), run_time=0.3)

        # Beat 2: Growth factors activate Rheb, amino acids deliver the kinase
        self.at("activate")
        self.play(rheb_box.animate.scale(1.06), run_time=0.7, rate_func=there_and_back)
        self.play(deliv_box.animate.scale(1.06), run_time=0.7, rate_func=there_and_back)

        # Beat 3: Standard model & glutamine Rag-bypass caveat
        self.at("standard model")
        bypass_arc = CurvedArrow([4.6, -0.25, 0], [1.15, -0.35, 0], angle=-0.7, color=CYAN, stroke_width=3.2)
        bypass_dashed = DashedVMobject(bypass_arc)
        note = fit_text("Standard model (some Rag-independent routes, e.g. glutamine)",
                        max_w=10.2, size=26, color=TEXT).move_to([-0.8, -3.10, 0])
        self.play(Create(bypass_dashed), FadeIn(note), run_time=1.8)

        # Beat 4: Both signals agree -> synchronized arrival and steady hold (no fade to black!)
        self.at("until both signals agree")
        p3 = Dot(memb.rec_pos + DOWN * 0.25, radius=0.13, color=EMERALD).set_z_index(-2)
        p4 = Dot([3.8, 1.70, 0], radius=0.13, color=CYAN).set_z_index(-2)
        self.add(p3, p4)
        self.play(
            p3.animate.move_to(rheb_box.get_center()),
            p4.animate.move_to(deliv_box.get_center()),
            run_time=0.7,
            rate_func=linear,
        )
        self.play(
            p3.animate.move_to(mtor.get_left() + LEFT * 0.14),
            p4.animate.move_to(mtor.get_right() + RIGHT * 0.14),
            run_time=1.1,
            rate_func=linear,
        )
        self.play(FadeOut(p3), FadeOut(p4), run_time=0.3)
        self.finish()


class S11End(EndCard):
    LINE = "mTORC1 needs both growth factors and amino acids to switch on."
