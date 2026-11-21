"""
Tail Codes: How One Receptor Branches and Ends Signaling
======================================================

COLOUR MAP (one colour per concept for the entire film):
- TEAL (#3FB8C0): Standard RTK receptor (EGFR, HER2, Insulin receptor)
- VIOLET (#B388FF): HER3 partner receptor
- GOLD (#D4A843): Kinase domains (active catalytic core)
- YELLOW (#F5D547): Phosphate groups (P) and phosphotyrosine badges (pY)
- GREEN (#83C167): +2 Asn motif, Grb2 SH2 adaptor, Ras -> MAP kinase branch
- BLUE (#58C4DD): PLC-gamma SH2 partner, IP3 + DAG branch
- MAGENTA (#EE6EB8): +3 Met (YXXM) motif, PI 3-kinase SH2 partner, Akt branch
- ORANGE (#F49342): Cbl docking site, Cbl ubiquitin ligase, Ub tags
- RED (#FC6255): Lysosome compartment, lost/mutated site X
- SILVER (#CBD4E1): Protein tyrosine phosphatases (PTPs)
- GREY (#8B93A1): Plasma membrane bilayer and inactive/resting outlines
- TEXT (#E8EAF0): Labels, schematic tags, titles

ONE PICTURE OF THE WORLD:
A cross-section of the plasma membrane (horizontal bilayer at the top) with the paired RTK
receptors extending downward into the cytosol—ectodomains above, single transmembrane helices
crossing the bilayer, paired gold kinases below, and long flexible tyrosine-carrying tails
filling most of the frame height.

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
- s01_hook: Separated resting receptors glide together across the membrane, kinases activate,
  the camera glides down so the parametric flexible tails fill ~65% of the frame, downstream
  branch paths and a shutoff loop grow, and sequential pY/branch highlights scan the tail.
- s02_phosphorylate_tails: Paired gold kinases transfer yellow P circles along clear outer arcs
  onto 8 parametric tail Y sites, converting each into a glowing pY docking site while
  three cytosolic SH2 partner cups move upward toward the tails.
- s03_sh2_reading: An emerald SH2 reading cup probes its two-part grip, approaches a
  mismatched +3 Met pY site, rebounds along a computed arc, and snaps onto the +2 Asn pY site.
- s04_branching: Phosphorylated tails unfold their motifs; emerald Grb2 docks onto pY1068
  (+2 Asn) and launches a multi-packet signal stream to Ras -> MAP kinase; sky-blue PLC-gamma
  docks onto pY992, shows PIP2 -> IP3 + DAG, and launches a signal stream to IP3 + DAG.
- s05_partner_mix: Left teal receptor swaps for violet HER3 paired with HER2; 6 pY (+3 Met)
  sites light up along a lengthened tail with a live 0->6 counter; 6 magenta PI 3-kinase cups
  dock while the Akt arrow stroke width grows proportionally (3.5 + 1.9 * n_docked) and shows
  PI3K -> Akt (growth, survival) with signal pulses.
- s06_beyond_the_tail: Highlights 'Just under membrane' (left) and 'Kinase insert loop' (right)
  pY sites with arrows on an RTK, then transitions to a pre-paired insulin receptor sweeping P
  circles onto a separate IRS proteins block whose outer pY badges recruit matching SH2 partners.
- s07_rule_and_predict: Shows Grb2 and PLC-gamma actively streaming signals, highlights the
  orange Cbl site with Cbl approaching, then crosses out the mutant Cbl site as Cbl rebounds
  and reveals the predict question banner cleanly above the receptor.
- s09_reveal_turnoff: Mutant receptor keeps streaming signals while a ValueTracker-driven
  schematic clock sweeps past; then intact Cbl docks and adds Ub tags, membrane pinches into
  a vesicle descending into the Lysosome compartment, while silver PTPs pluck P off a second pair.
- s10_close: Active receptor acts as a switchboard—kinases write P marks recruiting a growth
  branch (Grb2) and removal tagger (Cbl), then PTPs and lysosomal digestion clear the marks
  back to a quiet unphosphorylated resting receptor at the membrane.
"""

from bp_parts import *

# Concept palette extensions (strictly one colour per concept)
VIOLET = "#B388FF"
MAGENTA = "#EE6EB8"
ORANGE = "#F49342"
SILVER = "#CBD4E1"


# ---------------------------------------------------------------------------
# Parametric world geometry builders (shared across scenes for exact carry-over)
# ---------------------------------------------------------------------------

def make_membrane(y=2.2, x0=-6.25, x1=6.25, thickness=0.48):
    """Horizontal plasma membrane bilayer cross-section within the safe frame."""
    w = x1 - x0
    cx = (x0 + x1) / 2
    fill = Rectangle(
        width=w, height=thickness,
        stroke_width=0, fill_color=GREY, fill_opacity=0.38
    ).move_to([cx, y, 0])
    top = Line([x0, y + thickness / 2, 0], [x1, y + thickness / 2, 0], color=GREY, stroke_width=4.2)
    bot = Line([x0, y - thickness / 2, 0], [x1, y - thickness / 2, 0], color=GREY, stroke_width=4.2)
    g = VGroup(fill, top, bot)
    g.top_line = top
    g.bot_line = bot
    g.mem_y = y
    g.thickness = thickness
    return g


def tail_xy(u, x_base, y_top, length=3.4, side=-1, curve_amp=0.45):
    """Smooth parametric flexible tail point for u in [0, 1]."""
    y = y_top - u * length
    x = x_base + side * curve_amp * np.sin(u * PI * 1.15)
    return np.array([x, y, 0.0])


def make_tail_curve(x_base, y_top, length=3.4, side=-1, curve_amp=0.45, color=TEAL, width=10):
    """Parametric flexible tail VMobject."""
    pts = [tail_xy(u, x_base, y_top, length, side, curve_amp) for u in np.linspace(0, 1, 36)]
    m = VMobject(stroke_color=color, stroke_width=width, fill_opacity=0)
    m.set_points_smoothly(pts)
    return m


def make_monomer(x_center, mem_y=2.2, side=-1, color=TEAL, active=True, tail_len=3.4,
                 curve_amp=0.45, kinase_mode="active", tail_width=11, scale_geom=1.0):
    """Build one RTK monomer: ectodomain, TM helix, kinase domain, and parametric tail."""
    s = scale_geom
    ecto_y = mem_y + 0.60 * s
    ecto = RoundedRectangle(
        corner_radius=0.25 * s, width=1.10 * s, height=0.74 * s,
        stroke_color=color, stroke_width=4.0, fill_color=color, fill_opacity=0.46
    ).move_to([x_center, ecto_y, 0])

    tm = RoundedRectangle(
        corner_radius=0.06 * s, width=0.24 * s, height=0.60 * s,
        stroke_color=color, stroke_width=3.0, fill_color=color, fill_opacity=0.62
    ).move_to([x_center, mem_y, 0])

    kin_y = mem_y - 0.78 * s
    if kinase_mode == "active" and active:
        k_col, k_fill, k_sw = GOLD, 0.56, 4.4
    elif kinase_mode == "dim":
        k_col, k_fill, k_sw = color, 0.24, 3.4
    else:
        k_col, k_fill, k_sw = GREY, 0.26, 3.4
    kinase = RoundedRectangle(
        corner_radius=0.22 * s, width=1.20 * s, height=0.80 * s,
        stroke_color=k_col, stroke_width=k_sw, fill_color=k_col, fill_opacity=k_fill
    ).move_to([x_center, kin_y, 0])

    tail_top = kin_y - 0.40 * s
    tail = make_tail_curve(x_center, tail_top, length=tail_len, side=side,
                           curve_amp=curve_amp, color=color, width=tail_width)

    g = VGroup(tail, tm, ecto, kinase)
    g.ecto = ecto
    g.tm = tm
    g.kinase = kinase
    g.tail = tail
    g.x_center = x_center
    g.tail_top = tail_top
    g.tail_len = tail_len
    g.side = side
    g.curve_amp = curve_amp
    g.pt = lambda u, xb=x_center, yt=tail_top, ln=tail_len, sd=side, ca=curve_amp: tail_xy(u, xb, yt, ln, sd, ca)
    return g


def make_site_badge(tail_pt, side=-1, phosphorylated=False, motif=None, motif_color=GREEN,
                    stalk_len=0.26, text_size=24):
    """Build a roomy Y or pY badge on a short stalk offset cleanly from the tail."""
    stalk_end = tail_pt + np.array([side * stalk_len, 0.0, 0.0])
    stalk = Line(tail_pt, stalk_end, color=YELLOW if phosphorylated else GREY, stroke_width=4.2)

    txt_str = "pY" if phosphorylated else "Y"
    col = YELLOW if phosphorylated else TEXT
    b_col = YELLOW if phosphorylated else GREY
    fill_op = 0.30 if phosphorylated else 0.90
    fill_c = YELLOW if phosphorylated else BG

    lab = M(txt_str, size=text_size, color=col)
    pad_x, pad_y = 0.16, 0.15
    bw = max(0.70, lab.width + 2 * pad_x)
    bh = max(0.52, lab.height + 2 * pad_y)
    pill = RoundedRectangle(
        corner_radius=bh / 2, width=bw, height=bh,
        stroke_color=b_col, stroke_width=3.2, fill_color=fill_c, fill_opacity=fill_op
    )
    pill.move_to(stalk_end + np.array([side * (bw / 2 + 0.01), 0.0, 0.0]))
    lab.move_to(pill)
    g = VGroup(stalk, pill, lab)
    g.stalk = stalk
    g.pill = pill
    g.label = lab
    g.tab = None

    if motif is not None:
        tab_w, tab_h = 0.24, 0.30
        outer_x = pill.get_right()[0] if side > 0 else pill.get_left()[0]
        cy = pill.get_center()[1]
        if motif == "+3 Met":
            tab = Polygon(
                [outer_x, cy + tab_h / 2, 0],
                [outer_x + side * tab_w, cy, 0],
                [outer_x, cy - tab_h / 2, 0],
                stroke_color=motif_color, stroke_width=3.0,
                fill_color=motif_color, fill_opacity=0.75
            )
        else:
            tab = RoundedRectangle(
                corner_radius=0.06, width=tab_w, height=tab_h,
                stroke_color=motif_color, stroke_width=3.0,
                fill_color=motif_color, fill_opacity=0.75
            ).move_to([outer_x + side * (tab_w / 2 + 0.01), cy, 0])
        g.add(tab)
        g.tab = tab
    return g


def make_sh2_cup(name, color, facing=1, size=26, min_w=1.85, height=0.68):
    """Two-notch SH2 reading domain cup: jaw on `facing` side (+1 right, -1 left)."""
    lab = T(name, size=size, color=TEXT) if name else None
    body_w = max(min_w, (lab.width + 0.78) if lab else min_w)
    h = max(height, (lab.height + 0.32) if lab else height)
    notch = 0.28
    hw, hh = body_w / 2, h / 2
    pts = [
        [-hw, hh, 0],
        [hw, hh, 0],
        [hw - notch, hh * 0.45, 0],
        [hw - 0.06, 0.0, 0],
        [hw - notch, -hh * 0.45, 0],
        [hw, -hh, 0],
        [-hw, -hh, 0],
    ]
    if facing < 0:
        pts = [[-p[0], p[1], 0] for p in pts]
    cup = Polygon(
        *pts,
        stroke_color=color, stroke_width=3.6,
        fill_color=color, fill_opacity=0.46
    )
    g = VGroup(cup)
    if lab:
        lab.move_to(cup.get_center() + np.array([-facing * notch * 0.45, 0, 0]))
        g.add(lab)
    g.cup = cup
    g.label = lab
    g.facing = facing
    return g


def make_ptp_clipper():
    """Silver protein tyrosine phosphatase crescent clipper."""
    return AnnularSector(
        inner_radius=0.14, outer_radius=0.34,
        angle=TAU * 0.72, start_angle=PI * 0.14,
        stroke_color=SILVER, stroke_width=3.2,
        fill_color=SILVER, fill_opacity=0.52
    )


def make_arrow_between(p_start, p_end, color, width=6.0):
    return Arrow(
        p_start, p_end, buff=0.0,
        color=color, stroke_width=width,
        max_tip_length_to_length_ratio=0.16
    )


def add_signal_stream(arrow_start, arrow_end, color, progress_tracker, n_dots=3, radius=0.15):
    """Multi-packet glowing signal stream moving along an arrow."""
    def mk():
        t = progress_tracker.get_value()
        dots = VGroup()
        for k in range(n_dots):
            frac = (t + k / n_dots) % 1.0
            d = Dot(
                arrow_start + (arrow_end - arrow_start) * frac,
                radius=radius, color=color, stroke_color=TEXT, stroke_width=2.4
            )
            dots.add(d)
        return dots
    return always_redraw(mk)


# ---------------------------------------------------------------------------
# Scenes
# ---------------------------------------------------------------------------

class S00Title(TitleCard):
    LESSON = "Receptor Tyrosine Kinases"
    TITLE = "Tail Codes: How One Receptor Branches and Ends Signaling"


class S01Hook(SpokenScene):
    def construct(self):
        mem = make_membrane(y=1.65)
        left_r = make_monomer(-1.95, mem_y=1.65, side=-1, color=TEAL, active=False, tail_len=2.5, curve_amp=0.36)
        right_r = make_monomer(1.95, mem_y=1.65, side=1, color=TEAL, active=False, tail_len=2.5, curve_amp=0.36)
        tag = scope_tag("schematic", color=TEXT)
        world = VGroup(mem, left_r, right_r)

        self.play(FadeIn(world), FadeIn(tag), run_time=0.6)

        # Bring two receptor kinases together
        self.at("bringing two")
        self.play(
            left_r.animate.shift(RIGHT * 1.15),
            right_r.animate.shift(LEFT * 1.15),
            run_time=1.8
        )

        # Release brake & activate the pair -> gold kinases light up
        self.at("released their")
        self.play(
            left_r.kinase.animate.set_stroke(GOLD, 4.8).set_fill(GOLD, 0.56),
            right_r.kinase.animate.set_stroke(GOLD, 4.8).set_fill(GOLD, 0.56),
            run_time=1.1
        )

        # Glide smoothly down onto the long flexible tails (fill ~68% of frame height)
        mem_zoom = make_membrane(y=2.60)
        l_zoom = make_monomer(-0.80, mem_y=2.60, side=-1, color=TEAL, active=True, tail_len=3.25, curve_amp=0.52, tail_width=10)
        r_zoom = make_monomer(0.80, mem_y=2.60, side=1, color=TEAL, active=True, tail_len=3.25, curve_amp=0.52, tail_width=10)
        zoom_world = VGroup(mem_zoom, l_zoom, r_zoom)
        self.play(ReplacementTransform(world, zoom_world), run_time=1.8)

        # Unlabelled tyrosines (Y) along the flexible tails
        u_vals = [0.20, 0.44, 0.68, 0.90]
        l_sites = [make_site_badge(l_zoom.pt(u), side=-1, phosphorylated=False) for u in u_vals]
        r_sites = [make_site_badge(r_zoom.pt(u), side=1, phosphorylated=False) for u in u_vals]
        self.play(FadeIn(VGroup(*l_sites, *r_sites)), run_time=0.9)

        # Yet one active receptor starts several pathways at once
        self.at("starts several")
        b1_box = boxed_label("pathway ?", GREEN, size=26, fill_opacity=0.30).move_to([-4.2, -2.75, 0])
        b2_box = boxed_label("pathway ?", BLUE, size=26, fill_opacity=0.30).move_to([0.0, -2.95, 0])
        b3_box = boxed_label("pathway ?", MAGENTA, size=26, fill_opacity=0.30).move_to([4.0, -2.75, 0])
        a1 = DashedLine(l_zoom.pt(0.98) + LEFT * 0.1, b1_box.get_top() + UP * 0.12, color=GREEN, stroke_width=4.5)
        a2 = DashedLine(l_zoom.pt(1.0) + DOWN * 0.08, b2_box.get_top() + UP * 0.12, color=BLUE, stroke_width=4.5)
        a3 = DashedLine(r_zoom.pt(0.98) + RIGHT * 0.1, b3_box.get_top() + UP * 0.12, color=MAGENTA, stroke_width=4.5)
        self.play(
            Create(a1), Create(a2), Create(a3),
            FadeIn(b1_box), FadeIn(b2_box), FadeIn(b3_box),
            run_time=1.6
        )

        # And also schedules its own shut-off
        self.at("also schedules")
        shut_box = boxed_label("shutoff ?", ORANGE, size=26, fill_opacity=0.30).move_to([4.6, 0.45, 0])
        shut_arc = CurvedArrow(
            r_sites[0].pill.get_right() + RIGHT * 0.25,
            shut_box.get_top() + UP * 0.14,
            angle=-0.42, color=ORANGE, stroke_width=4.5
        )
        self.play(Create(shut_arc), FadeIn(shut_box), run_time=1.4)

        # Light up sample sites sequentially in yellow and highlight branches in sync
        self.at("how can")
        py_h1 = make_site_badge(l_zoom.pt(u_vals[1]), side=-1, phosphorylated=True)
        py_h2 = make_site_badge(l_zoom.pt(u_vals[2]), side=-1, phosphorylated=True)
        py_h3 = make_site_badge(r_zoom.pt(u_vals[0]), side=1, phosphorylated=True)
        self.play(
            ReplacementTransform(l_sites[1], py_h1),
            b1_box[0].animate.set_fill(GREEN, 0.48),
            run_time=1.3
        )
        self.play(
            ReplacementTransform(l_sites[2], py_h2),
            b2_box[0].animate.set_fill(BLUE, 0.48),
            b3_box[0].animate.set_fill(MAGENTA, 0.48),
            run_time=1.4
        )
        self.play(
            ReplacementTransform(r_sites[0], py_h3),
            shut_box[0].animate.set_fill(ORANGE, 0.48),
            run_time=1.4
        )
        self.finish()


class S02PhosphorylateTails(SpokenScene):
    def construct(self):
        mem = make_membrane(y=2.55)
        l_rec = make_monomer(-0.80, mem_y=2.55, side=-1, color=TEAL, active=True, tail_len=3.85, curve_amp=0.52, tail_width=10)
        r_rec = make_monomer(0.80, mem_y=2.55, side=1, color=TEAL, active=True, tail_len=3.85, curve_amp=0.52, tail_width=10)
        u_vals = [0.18, 0.42, 0.66, 0.90]
        l_sites = [make_site_badge(l_rec.pt(u), side=-1, phosphorylated=False) for u in u_vals]
        r_sites = [make_site_badge(r_rec.pt(u), side=1, phosphorylated=False) for u in u_vals]
        tag = scope_tag("schematic", color=TEXT)
        kin_lab = T("Kinase core", size=28, color=GOLD, weight=BOLD).move_to([3.5, 2.02, 0])
        kin_ptr = Arrow(kin_lab.get_left() + LEFT * 0.1, r_rec.kinase.get_right() + RIGHT * 0.08 + UP * 0.14,
                        buff=0.0, color=GOLD, stroke_width=4, max_tip_length_to_length_ratio=0.18)

        self.add(mem, l_rec, r_rec, *l_sites, *r_sites, tag)
        self.play(FadeIn(kin_lab), Create(kin_ptr), run_time=0.8)

        def sweep_pair(idx, run_t=0.95):
            """Simultaneously phosphorylate left and right tail site `idx` along clear outer paths."""
            pl_pt = l_rec.pt(u_vals[idx])
            pr_pt = r_rec.pt(u_vals[idx])
            new_l = make_site_badge(pl_pt, side=-1, phosphorylated=True)
            new_r = make_site_badge(pr_pt, side=1, phosphorylated=True)

            p_l = VGroup(
                Circle(radius=0.22, color=YELLOW, fill_color=YELLOW, fill_opacity=0.95, stroke_width=2),
                M("P", size=24, color=BG)
            ).move_to(l_rec.kinase.get_bottom() + LEFT * 0.35 + DOWN * 0.12)
            p_r = VGroup(
                Circle(radius=0.22, color=YELLOW, fill_color=YELLOW, fill_opacity=0.95, stroke_width=2),
                M("P", size=24, color=BG)
            ).move_to(r_rec.kinase.get_bottom() + RIGHT * 0.35 + DOWN * 0.12)

            rim_l = new_l.pill.get_left() + LEFT * 0.30
            rim_r = new_r.pill.get_right() + RIGHT * 0.30
            # Route cleanly outside all Y badges (x = +/-2.85) so P never passes over other Y/pY pills or kin_ptr
            path_l = CubicBezier(
                p_l.get_center(),
                np.array([-2.85, p_l.get_center()[1], 0]),
                np.array([-2.85, rim_l[1] + 0.1, 0]),
                rim_l
            )
            path_r = CubicBezier(
                p_r.get_center(),
                np.array([2.85, p_r.get_center()[1], 0]),
                np.array([2.85, rim_r[1] + 0.1, 0]),
                rim_r
            )
            self.add(p_l, p_r)
            self.play(
                MoveAlongPath(p_l, path_l),
                MoveAlongPath(p_r, path_r),
                l_rec.kinase.animate.set_fill(GOLD, 0.70),
                r_rec.kinase.animate.set_fill(GOLD, 0.70),
                run_time=run_t * 0.62
            )
            self.play(
                FadeOut(p_l, run_time=run_t * 0.28),
                FadeOut(p_r, run_time=run_t * 0.28),
                ReplacementTransform(l_sites[idx], new_l, run_time=run_t * 0.34),
                ReplacementTransform(r_sites[idx], new_r, run_time=run_t * 0.34),
                l_rec.kinase.animate.set_fill(GOLD, 0.52),
                r_rec.kinase.animate.set_fill(GOLD, 0.52),
            )
            l_sites[idx] = new_l
            r_sites[idx] = new_r

        # Paired kinases add phosphates to first pair of tyrosines outside the catalytic core
        self.at("the paired kinases")
        sweep_pair(0, run_t=1.25)

        # In EGFR, label receptor and tails
        self.at("in the epidermal")
        egfr_lab = T("EGFR", size=32, color=TEAL, weight=BOLD).move_to([-3.4, 3.22, 0])
        tails_lab = T("flexible tails", size=28, color=TEAL).move_to([4.1, 0.15, 0])
        self.play(FadeIn(egfr_lab), FadeIn(tails_lab), run_time=0.9)

        # Most of those tyrosines sit along its flexible tails -> phosphorylate remaining 3 pairs
        self.at("most of those")
        for idx in range(1, 4):
            sweep_pair(idx, run_t=0.90)

        # Each newly phosphorylated tyrosine turns into a docking site
        self.at("each newly")
        dock_lab = T("docking sites", size=28, color=YELLOW, weight=BOLD).move_to([4.1, -0.95, 0])
        self.play(FadeIn(dock_lab), run_time=0.6)
        glow_pills = [
            s.pill.animate.set_fill(YELLOW, 0.48).set_stroke(YELLOW, 4.4)
            for s in l_sites + r_sites
        ]
        self.play(LaggedStart(*glow_pills, lag_ratio=0.12), run_time=2.0)

        # For proteins floating in the cytosol -> 3 well-separated SH2 cups glide upward
        self.at("for proteins")
        p1 = make_sh2_cup("partner", GREEN, facing=1, size=24, min_w=1.7).move_to([-4.6, -2.95, 0])
        p2 = make_sh2_cup("partner", BLUE, facing=-1, size=24, min_w=1.7).move_to([4.6, -2.95, 0])
        p3 = make_sh2_cup("partner", ORANGE, facing=1, size=24, min_w=1.7).move_to([0.0, -3.22, 0])
        self.play(
            FadeIn(p1), FadeIn(p2), FadeIn(p3),
            p1.animate.shift(UP * 1.45),
            p2.animate.shift(UP * 1.35),
            p3.animate.shift(UP * 0.22),
            run_time=2.1
        )
        self.finish()


class S03Sh2Reading(SpokenScene):
    def construct(self):
        tail_pts = [
            np.array([-2.9, 3.2, 0.0]),
            np.array([-2.55, 1.35, 0.0]),
            np.array([-2.85, -1.25, 0.0]),
            np.array([-2.55, -3.2, 0.0]),
        ]
        tail = VMobject(stroke_color=TEAL, stroke_width=11, fill_opacity=0).set_points_smoothly(tail_pts)

        p_up = np.array([-2.65, 1.35, 0.0])
        p_dn = np.array([-2.78, -1.25, 0.0])

        def large_py_badge(pt, motif, m_col, label_dir):
            stalk = Line(pt, pt + RIGHT * 0.45, color=YELLOW, stroke_width=5)
            lab = M("pY", size=30, color=YELLOW)
            pill = RoundedRectangle(
                corner_radius=0.34, width=1.02, height=0.68,
                stroke_color=YELLOW, stroke_width=3.8, fill_color=YELLOW, fill_opacity=0.32
            ).move_to(pt + RIGHT * 0.98)
            lab.move_to(pill)
            rx = pill.get_right()[0]
            cy = pill.get_center()[1]
            if motif == "+3 Met":
                tab = Polygon(
                    [rx, cy + 0.26, 0], [rx + 0.44, cy, 0], [rx, cy - 0.26, 0],
                    stroke_color=m_col, stroke_width=3.2, fill_color=m_col, fill_opacity=0.78
                )
            else:
                tab = RoundedRectangle(
                    corner_radius=0.08, width=0.42, height=0.44,
                    stroke_color=m_col, stroke_width=3.2, fill_color=m_col, fill_opacity=0.78
                ).move_to([rx + 0.23, cy, 0])
            m_lab = T(motif, size=30, color=m_col, weight=BOLD).next_to(pill, label_dir, buff=0.54).shift(RIGHT * 0.25)
            return VGroup(stalk, pill, lab, tab, m_lab), pill, tab, m_lab

        site_up, pill_up, tab_up, lab_up = large_py_badge(p_up, "+3 Met", MAGENTA, UP)
        site_dn, pill_dn, tab_dn, lab_dn = large_py_badge(p_dn, "+2 Asn", GREEN, DOWN)
        tag = scope_tag("schematic", color=TEXT)

        self.play(FadeIn(tail), FadeIn(site_up), FadeIn(site_dn), FadeIn(tag), run_time=1.0)

        # Signaling proteins read those marks with pockets called SH2 domains
        self.at("read those marks")
        sh2_cup = make_sh2_cup("SH2 domain", GREEN, facing=-1, size=28, min_w=3.0, height=1.02).move_to([3.8, -0.1, 0])
        p_grip = Line(
            sh2_cup.cup.get_left() + UP * 0.28 + RIGHT * 0.05,
            sh2_cup.cup.get_left() + UP * 0.08 + RIGHT * 0.26,
            color=YELLOW, stroke_width=5.5
        )
        sh2 = VGroup(sh2_cup, p_grip)
        self.play(FadeIn(sh2, shift=LEFT * 0.6), run_time=1.5)

        self.play(p_grip.animate.set_stroke(YELLOW, 8.5), run_time=1.1)
        self.play(p_grip.animate.set_stroke(YELLOW, 5.5), run_time=1.0)

        self.at("such a pocket")
        self.play(sh2.animate.move_to([1.2, 1.35, 0]), run_time=2.0)

        # It grips the phosphate and checks the few amino acids right after it
        self.at("it grips")
        check_note = T("1. grip P   2. check +2/+3 residues", size=28, color=TEXT).move_to([2.0, 3.12, 0])
        self.play(FadeIn(check_note), run_time=0.8)

        self.at("and checks")
        self.play(sh2.animate.move_to([0.62, 1.35, 0]), run_time=0.9)
        mismatch = T("mismatch", size=26, color=RED, weight=BOLD).next_to(sh2, RIGHT, buff=0.30)
        self.play(FadeIn(mismatch), run_time=0.45)

        # Clear mismatch label before bouncing away so they never overlap in motion
        self.at("mismatched proteins")
        self.play(FadeOut(mismatch), run_time=0.20)
        bounce_path = CubicBezier(
            np.array([0.62, 1.35, 0]),
            np.array([2.9, 1.05, 0]),
            np.array([3.3, -0.45, 0]),
            np.array([1.8, -1.25, 0])
        )
        self.play(MoveAlongPath(sh2, bounce_path), run_time=1.25)

        self.at("while matching")
        # Stop cup jaw flush at outer edge of green +2 Asn tab without straddling its RoundedRectangle
        dock_x = tab_dn.get_right()[0] + sh2.width / 2 + 0.04
        self.play(sh2.animate.move_to([dock_x, -1.25, 0]), run_time=1.1)
        lock_ring = SurroundingRectangle(VGroup(pill_dn, tab_dn), color=GREEN, buff=0.10, stroke_width=4.5)
        lock_ring.layout_ok = True
        self.play(Create(lock_ring), run_time=0.7)
        self.finish()


class S04Branching(SpokenScene):
    def construct(self):
        mem = make_membrane(y=2.45)
        l_rec = make_monomer(-0.80, mem_y=2.45, side=-1, color=TEAL, active=True, tail_len=2.95, curve_amp=0.48, tail_width=10)
        r_rec = make_monomer(0.80, mem_y=2.45, side=1, color=TEAL, active=True, tail_len=2.95, curve_amp=0.48, tail_width=10)
        egfr_lab = T("EGFR", size=32, color=TEAL, weight=BOLD).move_to([-3.4, 3.20, 0])
        tag = scope_tag("schematic", color=TEXT)

        s_l1 = make_site_badge(l_rec.pt(0.42), side=-1, phosphorylated=True, motif="+2 Asn", motif_color=GREEN)
        s_l2 = make_site_badge(l_rec.pt(0.86), side=-1, phosphorylated=True)
        s_r1 = make_site_badge(r_rec.pt(0.18), side=1, phosphorylated=True)
        s_r2 = make_site_badge(r_rec.pt(0.56), side=1, phosphorylated=True, motif="+2", motif_color=BLUE)

        pair_grp = VGroup(mem, l_rec, r_rec, egfr_lab)
        pair_grp.scale(1.22)
        self.add(pair_grp, tag)
        self.play(pair_grp.animate.scale(1 / 1.22), run_time=1.6)
        self.play(LaggedStart(FadeIn(s_l1), FadeIn(s_r1), FadeIn(s_l2), FadeIn(s_r2), lag_ratio=0.25), run_time=2.2)

        self.at("epidermal growth factor")
        py1068_lab = T("pY1068 (+2 Asn)", size=28, color=GREEN, weight=BOLD).move_to([-3.7, 1.32, 0])
        hl_1068 = Circle(radius=0.46, color=GREEN, stroke_width=5.0).move_to(s_l1.pill)
        hl_1068.layout_ok = True
        self.play(
            Create(hl_1068), FadeIn(py1068_lab),
            r_rec.tail.animate.set_stroke(opacity=0.45),
            run_time=1.5
        )

        self.at("carries an asparagine")
        self.play(s_l1.tab.animate.scale(1.30), run_time=1.0)
        self.play(s_l1.tab.animate.scale(1 / 1.30), run_time=1.0)

        self.at("suits the adapter")
        grb2 = make_sh2_cup("Grb2", GREEN, facing=1, size=28, min_w=1.85, height=0.70)
        grb2.move_to([-5.2, s_l1.pill.get_center()[1], 0])
        dock_x_l = s_l1.tab.get_left()[0] - grb2.width / 2 - 0.04
        self.play(FadeIn(grb2), run_time=0.45)
        self.play(
            grb2.animate.move_to([dock_x_l, s_l1.pill.get_center()[1], 0]),
            r_rec.tail.animate.set_stroke(opacity=1.0),
            run_time=1.15
        )

        self.at("launching")
        ras_box = boxed_label("Ras → MAP kinase", GREEN, size=28, fill_opacity=0.30).move_to([-3.5, -2.55, 0])
        arr_start_l = grb2.get_bottom() + DOWN * 0.12
        arr_end_l = ras_box.get_top() + UP * 0.12
        arr_l = make_arrow_between(arr_start_l, arr_end_l, GREEN, width=6.5)
        pulse_l_t = ValueTracker(0.0)
        stream_l = add_signal_stream(arr_start_l, arr_end_l, GREEN, pulse_l_t, n_dots=3, radius=0.15)
        self.play(Create(arr_l), FadeIn(ras_box), run_time=0.9)
        self.add(stream_l)
        self.play(pulse_l_t.animate.set_value(1.2), run_time=1.5, rate_func=linear)

        self.at("another site")
        py992_lab = T("pY992", size=28, color=BLUE, weight=BOLD).move_to([4.1, 0.88, 0])
        hl_992 = Circle(radius=0.44, color=BLUE, stroke_width=4.5).move_to(s_r2.pill)
        hl_992.layout_ok = True
        plc = make_sh2_cup("PLC-gamma", BLUE, facing=-1, size=26, min_w=2.35, height=0.70)
        plc.move_to([5.2, s_r2.pill.get_center()[1], 0])
        dock_x_r = s_r2.tab.get_right()[0] + plc.width / 2 + 0.04
        ip3_box = boxed_label("IP3 + DAG", BLUE, size=28, fill_opacity=0.30).move_to([3.5, -2.55, 0])
        pip2_lhs = T("PIP2", size=24, color=TEXT, weight=BOLD)
        pip2_rhs = T("→ IP3 + DAG", size=24, color=BLUE, weight=BOLD)
        pip2_rxn = VGroup(pip2_lhs, pip2_rhs).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([5.25, -1.42, 0])
        self.play(
            Create(hl_992), FadeIn(py992_lab),
            FadeIn(plc),
            plc.animate.move_to([dock_x_r, s_r2.pill.get_center()[1], 0]),
            FadeIn(pip2_lhs),
            pulse_l_t.animate.set_value(2.4),
            run_time=1.6, rate_func=linear
        )

        # Keep left stream moving smoothly until "splits a membrane" is spoken
        wait_splits = max(0.0, self.t_of("splits a membrane") - 0.2 - self.elapsed())
        if wait_splits > 0.04:
            self.play(pulse_l_t.animate.set_value(2.4 + wait_splits * 0.8), run_time=wait_splits, rate_func=linear)

        self.at("splits a membrane")
        arr_start_r = plc.get_bottom() + DOWN * 0.12
        arr_end_r = ip3_box.get_top() + UP * 0.12
        arr_r = make_arrow_between(arr_start_r, arr_end_r, BLUE, width=6.5)
        pulse_r_t = ValueTracker(0.0)
        stream_r = add_signal_stream(arr_start_r, arr_end_r, BLUE, pulse_r_t, n_dots=3, radius=0.15)
        cur_l = pulse_l_t.get_value()
        self.play(
            FadeIn(pip2_rhs),
            Create(arr_r), FadeIn(ip3_box),
            pulse_l_t.animate.set_value(cur_l + 0.8),
            run_time=0.9, rate_func=linear
        )
        self.add(stream_r)
        self.play(
            pulse_l_t.animate.set_value(cur_l + 2.2),
            pulse_r_t.animate.set_value(1.5),
            run_time=1.7, rate_func=linear
        )
        self.finish()


class S05PartnerMix(SpokenScene):
    def construct(self):
        mem = make_membrane(y=2.65)
        l_egfr = make_monomer(-0.80, mem_y=2.65, side=-1, color=TEAL, active=True, tail_len=3.2, curve_amp=0.46, tail_width=10)
        r_her2 = make_monomer(0.80, mem_y=2.65, side=1, color=TEAL, active=True, tail_len=3.2, curve_amp=0.46, tail_width=10)
        l_her3 = make_monomer(-0.80, mem_y=2.65, side=-1, color=VIOLET, active=False, tail_len=4.05, curve_amp=0.55, kinase_mode="dim", tail_width=10)
        tag = scope_tag("schematic", color=TEXT)

        self.add(mem, l_egfr, r_her2, tag)
        self.play(
            l_egfr.animate.shift(LEFT * 4.5).set_opacity(0),
            FadeIn(l_her3, shift=RIGHT * 1.5),
            run_time=1.9
        )
        self.remove(l_egfr)

        self.at("remember violet")
        her3_lab = T("HER3", size=32, color=VIOLET, weight=BOLD).move_to([-3.0, 3.28, 0])
        her2_lab = T("HER2", size=32, color=TEAL, weight=BOLD).move_to([3.0, 3.28, 0])
        self.play(FadeIn(her3_lab), FadeIn(her2_lab), run_time=0.9)

        # Six tyrosines along HER3 tail, each +3 Met (YXXM)
        self.at("its tail carries", lead=0.30)
        n_sites = ValueTracker(0)
        site_counter = counter("{:.0f} × YXXM", n_sites, at=[3.9, 1.3, 0], size=34, color=MAGENTA)
        self.play(FadeIn(site_counter), run_time=0.25)

        u6 = np.linspace(0.08, 0.90, 6)
        her3_sites = []
        for idx, u in enumerate(u6, 1):
            s = make_site_badge(l_her3.pt(u), side=-1, phosphorylated=True, motif="+3 Met",
                                motif_color=MAGENTA, stalk_len=0.22, text_size=24)
            her3_sites.append(s)
            self.play(FadeIn(s), n_sites.animate.set_value(idx), run_time=0.16)

        self.at("each followed")
        met_note = T("+3 Met sites", size=28, color=MAGENTA).move_to([3.9, 0.58, 0])
        self.play(
            FadeIn(met_note),
            LaggedStart(*[s.tab.animate.scale(1.35) for s in her3_sites], lag_ratio=0.12),
            run_time=1.35
        )
        self.play(
            LaggedStart(*[s.tab.animate.scale(1 / 1.35) for s in her3_sites], lag_ratio=0.12),
            run_time=1.15
        )

        self.at("paired with")
        self.play(
            r_her2.kinase.animate.set_fill(GOLD, 0.80).set_stroke(GOLD, 6.0),
            her2_lab.animate.scale(1.12),
            run_time=0.55
        )
        self.play(
            r_her2.kinase.animate.set_fill(GOLD, 0.56).set_stroke(GOLD, 4.4),
            her2_lab.animate.scale(1 / 1.12),
            run_time=0.55
        )

        self.at("those sites recruit")
        n_docked = ValueTracker(0)
        akt_box = boxed_label("Akt", MAGENTA, size=34, fill_opacity=0.32).move_to([3.5, -2.55, 0])
        akt_full = boxed_label("PI3K → Akt (growth, survival)", MAGENTA, size=24, fill_opacity=0.32).move_to([3.45, -2.55, 0])
        arr_start = np.array([-0.55, -2.55, 0])
        arr_end_x = ValueTracker(akt_box.get_left()[0] - 0.14)
        akt_arrow = always_redraw(
            lambda: Arrow(
                arr_start, np.array([arr_end_x.get_value(), -2.55, 0]), buff=0.0,
                color=MAGENTA,
                stroke_width=3.5 + 1.9 * n_docked.get_value(),
                max_tip_length_to_length_ratio=0.14
            )
        )
        self.add(akt_arrow)
        self.play(FadeIn(akt_box), run_time=0.40)

        cups = []
        for idx, s in enumerate(her3_sites, 1):
            c = make_sh2_cup("", MAGENTA, facing=1, min_w=0.95, height=0.46)
            y_pos = s.pill.get_center()[1]
            c.move_to([-4.2, y_pos, 0])
            dock_x = s.tab.get_left()[0] - c.width / 2 - 0.04
            self.add(c)
            cups.append(c)
            self.play(
                c.animate.move_to([dock_x, y_pos, 0]),
                n_docked.animate.set_value(idx),
                run_time=0.20
            )

        cup_grp = VGroup(*cups)
        brace = Brace(cup_grp, LEFT, color=MAGENTA, buff=0.14)
        pi3k_lab = boxed_label("PI 3-kinase", MAGENTA, size=28, fill_opacity=0.28).next_to(brace, LEFT, buff=0.18)
        self.play(FadeIn(brace), FadeIn(pi3k_lab), run_time=0.40)

        self.at("which drives")
        self.play(
            swap(akt_box, akt_full, run_time=0.6),
            arr_end_x.animate(run_time=0.6).set_value(akt_full.get_left()[0] - 0.14),
        )
        pulse_t = ValueTracker(0.0)
        stream = add_signal_stream(arr_start, np.array([akt_full.get_left()[0] - 0.14, -2.55, 0]), MAGENTA, pulse_t, n_dots=3, radius=0.16)
        self.add(stream)
        self.play(pulse_t.animate.set_value(2.0), run_time=2.0, rate_func=linear)
        self.finish()


class S06BeyondTheTail(SpokenScene):
    def construct(self):
        mem = make_membrane(y=2.10)
        l_her3 = make_monomer(-0.80, mem_y=2.10, side=-1, color=VIOLET, active=False, tail_len=3.0, curve_amp=0.48, kinase_mode="dim")
        r_her2 = make_monomer(0.80, mem_y=2.10, side=1, color=TEAL, active=True, tail_len=3.0, curve_amp=0.48)
        pair_old = VGroup(l_her3, r_her2)
        tag = scope_tag("schematic", color=TEXT)
        self.add(mem, pair_old, tag)

        rtk = make_monomer(0.0, mem_y=2.10, side=-1, color=TEAL, active=True, tail_len=2.6, curve_amp=0.42, tail_width=10)
        self.play(
            pair_old.animate.shift(LEFT * 6.5).set_opacity(0),
            FadeIn(rtk, shift=LEFT * 1.5),
            run_time=1.9
        )
        self.remove(pair_old)

        # Stretch just under membrane (left) & kinase insert loop (right) with pointing arrows
        self.at("some use")
        jm_start = np.array([rtk.tm.get_left()[0], 1.79, 0])
        jm_end = np.array([-0.82, 1.42, 0])
        jm_tmp = make_site_badge(jm_end, side=-1, phosphorylated=True, stalk_len=0.0)
        jm_stalk = VMobject(color=YELLOW, stroke_width=4.2).set_points_as_corners([
            jm_start,
            np.array([-0.68, 1.74, 0]),
            jm_tmp.pill.get_right(),
        ])
        jm_badge = VGroup(jm_stalk, jm_tmp.pill, jm_tmp.label)
        jm_badge.stalk = jm_stalk
        jm_badge.pill = jm_tmp.pill
        jm_badge.label = jm_tmp.label
        jm_badge.tab = None
        jm_lab = T("Just under membrane", size=26, color=YELLOW, weight=BOLD).move_to([-4.25, 1.42, 0])
        jm_arr = Arrow(
            jm_lab.get_right() + RIGHT * 0.10,
            jm_badge.pill.get_left() + LEFT * 0.08,
            buff=0.0, color=YELLOW, stroke_width=4.0, max_tip_length_to_length_ratio=0.22
        )
        self.play(FadeIn(jm_badge), FadeIn(jm_lab), Create(jm_arr), run_time=1.2)

        self.at("or a loop")
        ins_pt = rtk.kinase.get_right() + DOWN * 0.1
        ins_badge = make_site_badge(ins_pt, side=1, phosphorylated=True, stalk_len=0.36)
        ins_lab = T("Kinase insert loop", size=26, color=YELLOW, weight=BOLD).move_to([4.15, 1.22, 0])
        ins_arr = Arrow(
            ins_lab.get_left() + LEFT * 0.10,
            ins_badge.pill.get_right() + RIGHT * 0.08,
            buff=0.0, color=YELLOW, stroke_width=4.0, max_tip_length_to_length_ratio=0.22
        )
        self.play(FadeIn(ins_badge), FadeIn(ins_lab), Create(ins_arr), run_time=1.2)

        # Cleanly fade out first RTK before bringing in Insulin receptor
        self.at("the insulin receptor")
        ins_l = make_monomer(-3.55, mem_y=2.10, side=-1, color=TEAL, active=True, tail_len=1.5, curve_amp=0.20, tail_width=10)
        ins_r = make_monomer(-2.05, mem_y=2.10, side=1, color=TEAL, active=True, tail_len=1.5, curve_amp=0.20, tail_width=10)
        ss_bond = Line(ins_l.ecto.get_right(), ins_r.ecto.get_left(), color=YELLOW, stroke_width=4.5)
        ins_title = T("Insulin receptor", size=30, color=TEAL, weight=BOLD).move_to([-2.8, 3.36, 0])
        ins_rec = VGroup(ins_l, ins_r, ss_bond, ins_title)

        self.play(
            FadeOut(rtk), FadeOut(jm_badge), FadeOut(jm_lab), FadeOut(jm_arr),
            FadeOut(ins_badge), FadeOut(ins_lab), FadeOut(ins_arr), run_time=0.45
        )
        self.play(FadeIn(ins_rec), run_time=0.95)

        self.at("on separate")
        irs_box = RoundedRectangle(
            corner_radius=0.26, width=2.9, height=3.1,
            stroke_color=TEAL, stroke_width=4.0, fill_color=TEAL, fill_opacity=0.28
        ).move_to([1.1, -0.55, 0])
        irs_lab = T("IRS proteins", size=28, color=TEXT, weight=BOLD).next_to(irs_box, UP, buff=0.22)
        self.play(FadeIn(irs_box), FadeIn(irs_lab), run_time=0.95)

        irs_sites = []
        ys = [0.48, -0.20, -0.88, -1.56]
        motifs = ["+2 Asn", "+3 Met", "+2 Asn", "+3 Met"]
        cols = [GREEN, MAGENTA, GREEN, MAGENTA]
        for y_p, mot, mc in zip(ys, motifs, cols):
            pt = np.array([irs_box.get_right()[0], y_p, 0])
            sb = make_site_badge(pt, side=1, phosphorylated=True, motif=mot, motif_color=mc, stalk_len=0.28)
            p_dot = Dot(ins_r.kinase.get_bottom(), radius=0.16, color=YELLOW)
            self.add(p_dot)
            self.play(
                MoveAlongPath(p_dot, ArcBetweenPoints(ins_r.kinase.get_bottom(), sb.pill.get_center(), angle=-0.35)),
                run_time=0.30
            )
            self.remove(p_dot)
            self.play(FadeIn(sb), run_time=0.12)
            irs_sites.append(sb)

        self.at("yet the same")
        c_grb = make_sh2_cup("SH2", GREEN, facing=-1, size=24, min_w=1.55, height=0.50).move_to([5.4, ys[0], 0])
        c_pi3 = make_sh2_cup("SH2", MAGENTA, facing=-1, size=24, min_w=1.55, height=0.50).move_to([5.4, ys[1], 0])
        self.play(FadeIn(c_grb), FadeIn(c_pi3), run_time=0.35)
        self.play(
            c_grb.animate.move_to([irs_sites[0].tab.get_right()[0] + c_grb.width / 2 + 0.04, ys[0], 0]),
            c_pi3.animate.move_to([irs_sites[1].tab.get_right()[0] + c_pi3.width / 2 + 0.04, ys[1], 0]),
            run_time=0.95
        )
        self.wait(1.9)
        self.finish()


def build_s07_world(mutant=True, with_cbl=True, show_cbl_site=True):
    """Shared picture for s07_rule_and_predict and s08_pause."""
    mem = make_membrane(y=1.85)
    l_rec = make_monomer(-0.80, mem_y=1.85, side=-1, color=TEAL, active=True, tail_len=2.85, curve_amp=0.46, tail_width=10)
    r_rec = make_monomer(0.80, mem_y=1.85, side=1, color=TEAL, active=True, tail_len=2.85, curve_amp=0.46, tail_width=10)

    l_site = make_site_badge(l_rec.pt(0.45), side=-1, phosphorylated=True, motif="+2 Asn", motif_color=GREEN)
    grb2 = make_sh2_cup("Grb2", GREEN, facing=1, size=26, min_w=1.75, height=0.64)
    grb2.move_to([l_site.tab.get_left()[0] - grb2.width / 2 - 0.04, l_site.pill.get_center()[1], 0])
    ras_box = boxed_label("Ras → MAP kinase", GREEN, size=26, fill_opacity=0.30).move_to([-3.5, -2.50, 0])
    arr_l = make_arrow_between(grb2.get_bottom() + DOWN * 0.12, ras_box.get_top() + UP * 0.12, GREEN, width=6.5)

    r_plc_site = make_site_badge(r_rec.pt(0.58), side=1, phosphorylated=True, motif="+2", motif_color=BLUE)
    plc = make_sh2_cup("PLC-gamma", BLUE, facing=-1, size=24, min_w=2.25, height=0.62)
    plc.move_to([r_plc_site.tab.get_right()[0] + plc.width / 2 + 0.04, r_plc_site.pill.get_center()[1], 0])
    ip3_box = boxed_label("IP3 + DAG", BLUE, size=26, fill_opacity=0.30).move_to([3.3, -2.70, 0])
    arr_r = make_arrow_between(plc.get_bottom() + DOWN * 0.12, ip3_box.get_top() + UP * 0.12, BLUE, width=6.5)

    g = VGroup(mem, l_rec, r_rec, l_site, grb2, ras_box, arr_l,
               r_plc_site, plc, ip3_box, arr_r)

    r_cbl_site = None
    cbl_lab = None
    if show_cbl_site:
        r_cbl_site = make_site_badge(r_rec.pt(0.24), side=1, phosphorylated=not mutant, motif="Cbl", motif_color=ORANGE)
        cbl_lab = T("Cbl site", size=26, color=ORANGE, weight=BOLD).next_to(r_cbl_site.pill, UP, buff=0.22).shift(RIGHT * 0.50)
        g.add(r_cbl_site, cbl_lab)

        if mutant:
            c = r_cbl_site.pill.get_center()
            x_mark = VGroup(
                Line(c + [-0.28, -0.24, 0], c + [0.28, 0.24, 0], color=RED, stroke_width=5),
                Line(c + [-0.28, 0.24, 0], c + [0.28, -0.24, 0], color=RED, stroke_width=5),
            )
            x_mark.layout_ok = True
            g.add(x_mark)

        if with_cbl:
            cbl_cup = make_sh2_cup("Cbl", ORANGE, facing=-1, size=26, min_w=1.60, height=0.62)
            cbl_cup.move_to([4.6 if mutant else r_cbl_site.tab.get_right()[0] + 1.15,
                             r_cbl_site.pill.get_center()[1], 0])
            g.add(cbl_cup)
            g.cbl_cup = cbl_cup

    tag = T("schematic", size=24, color=TEXT).move_to([-5.6, -3.3, 0])
    g.add(tag)

    g.l_rec = l_rec
    g.r_rec = r_rec
    g.ras_box = ras_box
    g.ip3_box = ip3_box
    g.l_site = l_site
    g.r_plc_site = r_plc_site
    g.r_cbl_site = r_cbl_site
    g.cbl_lab = cbl_lab
    g.grb2 = grb2
    g.plc = plc
    g.arr_l = arr_l
    g.arr_r = arr_r
    return g


class S07RuleAndPredict(SpokenScene):
    def construct(self):
        w = build_s07_world(mutant=False, with_cbl=False, show_cbl_site=False)
        self.add(w)

        p_t = ValueTracker(0.0)
        sl = add_signal_stream(w.arr_l.get_start(), w.arr_l.get_end(), GREEN, p_t, n_dots=2, radius=0.11)
        sr = add_signal_stream(w.arr_r.get_start(), w.arr_r.get_end(), BLUE, p_t, n_dots=2, radius=0.11)
        self.add(sl, sr)

        # Kinase and downstream box pulse tied to signal transmission so active signaling reads clearly
        self.play(
            p_t.animate.set_value(1.2),
            w.ras_box[0].animate.set_fill(GREEN, 0.52),
            w.ip3_box[0].animate.set_fill(BLUE, 0.52),
            run_time=1.8, rate_func=linear
        )
        self.play(
            p_t.animate.set_value(2.4),
            w.ras_box[0].animate.set_fill(GREEN, 0.28),
            w.ip3_box[0].animate.set_fill(BLUE, 0.28),
            run_time=1.7, rate_func=linear
        )

        self.at("recruit specific")
        rule_ban = VGroup(
            T("Phosphotyrosines recruit specific partners", size=25, color=GOLD),
            T("by sequence to branch and end signaling.", size=25, color=GOLD),
        ).arrange(DOWN, buff=0.08).move_to([0, 3.28, 0])
        self.play(
            FadeIn(rule_ban),
            p_t.animate.set_value(3.8),
            w.ras_box[0].animate.set_fill(GREEN, 0.48),
            w.ip3_box[0].animate.set_fill(BLUE, 0.48),
            run_time=2.2, rate_func=linear
        )
        self.play(
            p_t.animate.set_value(4.8),
            w.ras_box[0].animate.set_fill(GREEN, 0.30),
            w.ip3_box[0].animate.set_fill(BLUE, 0.30),
            run_time=1.4, rate_func=linear
        )

        # The tail even recruits its own removal tagger, Cbl
        self.at("the tail even")
        r_cbl_site = make_site_badge(w.r_rec.pt(0.24), side=1, phosphorylated=True, motif="Cbl", motif_color=ORANGE)
        cbl_lab = T("Cbl site", size=26, color=ORANGE, weight=BOLD).next_to(r_cbl_site.pill, UP, buff=0.22).shift(RIGHT * 0.50)
        self.play(
            FadeIn(r_cbl_site), FadeIn(cbl_lab),
            p_t.animate.set_value(5.6),
            run_time=1.4, rate_func=linear
        )

        self.at("the ubiquitin")
        cbl_cup = make_sh2_cup("Cbl", ORANGE, facing=-1, size=26, min_w=1.60, height=0.62)
        cbl_cup.move_to([5.2, r_cbl_site.pill.get_center()[1], 0])
        self.play(
            FadeIn(cbl_cup),
            cbl_cup.animate.move_to([3.95, r_cbl_site.pill.get_center()[1], 0]),
            p_t.animate.set_value(6.5),
            run_time=1.6, rate_func=linear
        )

        # Pause and predict
        self.at("pause and predict")
        q_card = question_card("Lost Cbl site: what happens to the receptor?", y=3.22, max_w=11.8)
        self.play(
            swap(rule_ban, q_card, run_time=0.9),
            p_t.animate.set_value(7.1),
            rate_func=linear
        )

        # Mutant loses that Cbl docking site
        self.at("if a mutant")
        mutant_site = make_site_badge(
            r_cbl_site.stalk.get_start(), side=1, phosphorylated=False, motif="Cbl", motif_color=ORANGE
        )
        c = mutant_site.pill.get_center()
        x_mark = VGroup(
            Line(c + [-0.28, -0.24, 0], c + [0.28, 0.24, 0], color=RED, stroke_width=5),
            Line(c + [-0.28, 0.24, 0], c + [0.28, -0.24, 0], color=RED, stroke_width=5),
        )
        x_mark.layout_ok = True
        self.play(
            ReplacementTransform(r_cbl_site, mutant_site),
            Create(x_mark),
            cbl_cup.animate.move_to([4.6, mutant_site.pill.get_center()[1], 0]),
            p_t.animate.set_value(9.6),
            run_time=4.0, rate_func=linear
        )
        self.remove(sl, sr)
        self.finish()


class S08Pause(PredictPause):
    QUESTION = "Lost Cbl site: what happens to the receptor?"
    CARD = {"y": 3.22, "max_w": 11.8}
    SECONDS = 4.5

    def backdrop(self):
        return build_s07_world(mutant=True, with_cbl=True, show_cbl_site=True)


class S09RevealTurnoff(SpokenScene):
    def construct(self):
        w = build_s07_world(mutant=True, with_cbl=True, show_cbl_site=True)
        q_card = question_card("Lost Cbl site: what happens to the receptor?", y=3.22, max_w=11.8)
        self.add(w, q_card)

        clk_c = np.array([4.6, 0.90, 0.0])
        clk_r = 0.62
        clk_face = Circle(radius=clk_r, color=TEXT, stroke_width=3.5, fill_color=BG, fill_opacity=0.88).move_to(clk_c)
        clk_ticks = VGroup(*[
            Line(
                clk_c + 0.80 * clk_r * np.array([np.cos(a), np.sin(a), 0]),
                clk_c + 0.96 * clk_r * np.array([np.cos(a), np.sin(a), 0]),
                color=GREY, stroke_width=2.5
            )
            for a in np.linspace(0, TAU, 12, endpoint=False)
        ])
        ang = ValueTracker(PI / 2)
        clk_hand = always_redraw(
            lambda: Line(
                clk_c,
                clk_c + 0.72 * clk_r * np.array([np.cos(ang.get_value()), np.sin(ang.get_value()), 0]),
                color=GOLD, stroke_width=4.5
            )
        )
        clk_lab = T("signals longer", size=26, color=GOLD, weight=BOLD).move_to([4.6, 2.75, 0])
        clock = VGroup(clk_face, clk_ticks, clk_hand, clk_lab)

        p_t = ValueTracker(0.0)
        sl = add_signal_stream(w.arr_l.get_start(), w.arr_l.get_end(), GREEN, p_t, n_dots=2, radius=0.11)
        sr = add_signal_stream(w.arr_r.get_start(), w.arr_r.get_end(), BLUE, p_t, n_dots=2, radius=0.11)

        self.play(
            FadeOut(q_card),
            w.cbl_cup.animate.move_to([4.6, -0.20, 0]),
            FadeIn(clock),
            run_time=0.6
        )
        self.add(sl, sr)

        self.at("so it keeps")
        self.play(
            ang.animate.set_value(PI / 2 - TAU * 0.90),
            p_t.animate.set_value(2.2),
            run_time=2.8, rate_func=linear
        )
        self.remove(sl, sr)

        # Normally, Cbl docks there and attaches ubiquitin tags
        self.at("normally")
        mem_l = make_membrane(y=2.35, x0=-6.2, x1=-0.2)
        l_pair_l = make_monomer(-3.65, mem_y=2.35, side=-1, color=TEAL, active=True, tail_len=1.55, curve_amp=0.20, scale_geom=0.74)
        l_pair_r = make_monomer(-2.65, mem_y=2.35, side=1, color=TEAL, active=True, tail_len=1.55, curve_amp=0.20, scale_geom=0.74)
        cbl_site = make_site_badge(l_pair_r.pt(0.32), side=1, phosphorylated=True, motif="Cbl", motif_color=ORANGE, stalk_len=0.08, text_size=29)
        cbl_site.pill.scale(1.12)
        cbl_site.tab.next_to(cbl_site.pill, RIGHT, buff=0.01)
        cbl_cup = make_sh2_cup("Cbl", ORANGE, facing=-1, size=29, min_w=1.18, height=0.56)
        cbl_cup.move_to([-0.75, cbl_site.pill.get_center()[1], 0])
        tag = scope_tag("schematic", color=TEXT)
        left_scene = VGroup(mem_l, l_pair_l, l_pair_r, cbl_site)

        self.play(
            FadeOut(w), FadeOut(clock),
            FadeIn(left_scene), FadeIn(cbl_cup), FadeIn(tag),
            run_time=0.9
        )
        self.play(
            cbl_cup.animate.move_to([cbl_site.tab.get_right()[0] + cbl_cup.width / 2 + 0.03,
                                     cbl_site.pill.get_center()[1], 0]),
            run_time=0.7
        )

        self.at("attaches ubiquitin")
        ub_tags = VGroup()
        for k, (u_ub, x_off, y_off) in enumerate([(0.16, -0.78, 0.08), (0.56, -0.46, 0.0), (0.98, -0.48, -0.06)]):
            ub = boxed_label("Ub", ORANGE, size=29, pad=0.13, fill_opacity=0.26).move_to(
                l_pair_l.pt(u_ub) + np.array([x_off, y_off, 0])
            )
            ub_tags.add(ub)
        self.play(LaggedStart(*[FadeIn(u, shift=RIGHT * 0.15) for u in ub_tags], lag_ratio=0.35), run_time=1.8)

        # Receptor taken in by endocytosis and routed to the lysosome for digestion
        self.at("the receptor is")
        lyso = Ellipse(width=4.2, height=1.55, stroke_color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.30).move_to([-3.15, -2.65, 0])
        lyso_lab = T("Lysosome", size=28, color=RED, weight=BOLD).move_to([-3.15, -2.95, 0])
        lyso_grp = VGroup(lyso, lyso_lab)

        self.at("by endocytosis")
        vesicle_ring = Circle(radius=1.96, stroke_color=GREY, stroke_width=4.5, fill_color=GREY, fill_opacity=0.16).move_to([-3.15, 0.14, 0])
        endo_lab = T("endocytosis", size=28, color=TEXT).move_to([-5.0, 2.95, 0])
        cargo = VGroup(l_pair_l, l_pair_r, cbl_site, cbl_cup, ub_tags)

        mem_l_healed = make_membrane(y=2.35, x0=-6.2, x1=-0.2)
        self.play(
            FadeIn(lyso_grp),
            FadeIn(endo_lab),
            cargo.animate.scale(0.76).move_to([-3.15, 0.14, 0]),
            Create(vesicle_ring),
            Transform(mem_l, mem_l_healed),
            run_time=1.8
        )

        self.at("to the lysosome")
        vesicle_full = VGroup(vesicle_ring, cargo)
        # Descend smoothly to just above Lysosome rim, then dissolve cleanly into Lysosome
        self.play(vesicle_full.animate.shift(DOWN * 0.50), run_time=0.9)
        self.play(FadeOut(vesicle_full, shift=DOWN * 0.45), run_time=1.1)

        # Meanwhile, protein tyrosine phosphatases strip phosphates off a second surface pair
        self.at("meanwhile")
        mem_r = make_membrane(y=2.35, x0=0.3, x1=6.2)
        r_pair_l = make_monomer(2.20, mem_y=2.35, side=-1, color=TEAL, active=True, tail_len=2.5, curve_amp=0.35, tail_width=10, scale_geom=0.80)
        r_pair_r = make_monomer(3.30, mem_y=2.35, side=1, color=TEAL, active=True, tail_len=2.5, curve_amp=0.35, tail_width=10, scale_geom=0.80)

        py_a = make_site_badge(r_pair_l.pt(0.45), side=-1, phosphorylated=True, motif="+2 Asn", motif_color=GREEN)
        py_b = make_site_badge(r_pair_r.pt(0.60), side=1, phosphorylated=True, motif="+2", motif_color=BLUE)
        grb_r = make_sh2_cup("Grb2", GREEN, facing=1, size=24, min_w=1.40, height=0.58)
        grb_r.move_to([py_a.tab.get_left()[0] - grb_r.width / 2 - 0.04, py_a.pill.get_center()[1], 0])
        plc_r = make_sh2_cup("PLC-g", BLUE, facing=-1, size=24, min_w=1.40, height=0.58)
        plc_r.move_to([py_b.tab.get_right()[0] + plc_r.width / 2 + 0.04, py_b.pill.get_center()[1], 0])

        ptp1 = make_ptp_clipper().move_to([0.75, 1.35, 0])
        ptp2 = make_ptp_clipper().flip(UP).move_to([5.15, 0.90, 0])
        ptp_lab = T("PTPs", size=28, color=SILVER, weight=BOLD).move_to([0.85, 3.05, 0])

        self.play(
            FadeIn(mem_r), FadeIn(r_pair_l), FadeIn(r_pair_r),
            FadeIn(py_a), FadeIn(py_b), FadeIn(grb_r), FadeIn(plc_r),
            FadeIn(ptp1), FadeIn(ptp2), FadeIn(ptp_lab),
            run_time=1.3
        )

        self.at("strip")
        y_a = make_site_badge(r_pair_l.pt(0.45), side=-1, phosphorylated=False)
        y_b = make_site_badge(r_pair_r.pt(0.60), side=1, phosphorylated=False)
        self.play(
            grb_r.animate.shift(LEFT * 0.8 + DOWN * 1.1).set_opacity(0),
            plc_r.animate.shift(RIGHT * 0.8 + DOWN * 1.1).set_opacity(0),
            ptp1.animate.move_to(py_a.tab.get_left() + LEFT * 0.36),
            ptp2.animate.move_to(py_b.tab.get_right() + RIGHT * 0.36),
            run_time=1.2
        )

        self.at("erasing docking")
        p_fly1 = VGroup(Circle(radius=0.16, color=YELLOW, fill_color=YELLOW, fill_opacity=0.95), M("P", 22, BG)).move_to(py_a.pill.get_bottom() + DOWN * 0.28)
        p_fly2 = VGroup(Circle(radius=0.16, color=YELLOW, fill_color=YELLOW, fill_opacity=0.95), M("P", 22, BG)).move_to(py_b.pill.get_bottom() + DOWN * 0.28)
        self.add(p_fly1, p_fly2)
        self.play(
            swap(py_a, y_a, run_time=0.7),
            swap(py_b, y_b, run_time=0.7),
            p_fly1.animate.shift(DOWN * 1.4).set_opacity(0),
            p_fly2.animate.shift(DOWN * 1.4).set_opacity(0),
            ptp1.animate.shift(LEFT * 0.5),
            ptp2.animate.shift(RIGHT * 0.5),
            run_time=1.6
        )
        self.finish()


class S10Close(SpokenScene):
    def construct(self):
        mem = make_membrane(y=1.90)
        l_rec = make_monomer(-0.80, mem_y=1.90, side=-1, color=TEAL, active=True, tail_len=2.85, curve_amp=0.45, tail_width=10)
        r_rec = make_monomer(0.80, mem_y=1.90, side=1, color=TEAL, active=True, tail_len=2.85, curve_amp=0.45, tail_width=10)
        tag = scope_tag("schematic", color=TEXT)
        sb_lab = T("sequence-coded switchboard", size=30, color=TEXT, weight=BOLD).move_to([0, 3.28, 0])

        l_y = make_site_badge(l_rec.pt(0.45), side=-1, phosphorylated=False)
        r_y = make_site_badge(r_rec.pt(0.45), side=1, phosphorylated=False)

        world = VGroup(mem, l_rec, r_rec, l_y, r_y)
        world.scale(0.92)
        self.add(world, tag)
        self.play(world.animate.scale(1 / 0.92), run_time=1.4)

        self.at("acts like")
        self.play(FadeIn(sb_lab), run_time=1.2)
        self.play(
            l_rec.kinase.animate.set_fill(GOLD, 0.72),
            r_rec.kinase.animate.set_fill(GOLD, 0.72),
            run_time=1.0
        )
        self.play(
            l_rec.kinase.animate.set_fill(GOLD, 0.52),
            r_rec.kinase.animate.set_fill(GOLD, 0.52),
            run_time=1.0
        )

        self.at("kinases write")
        l_py = make_site_badge(l_rec.pt(0.45), side=-1, phosphorylated=True, motif="+2 Asn", motif_color=GREEN)
        r_py = make_site_badge(r_rec.pt(0.45), side=1, phosphorylated=True, motif="Cbl", motif_color=ORANGE)
        p1 = Dot(l_rec.kinase.get_bottom() + LEFT * 0.25, radius=0.16, color=YELLOW)
        p2 = Dot(r_rec.kinase.get_bottom() + RIGHT * 0.25, radius=0.16, color=YELLOW)
        self.add(p1, p2)
        self.play(
            MoveAlongPath(p1, ArcBetweenPoints(p1.get_center(), l_py.pill.get_left() + LEFT * 0.28, angle=-0.45)),
            MoveAlongPath(p2, ArcBetweenPoints(p2.get_center(), r_py.pill.get_right() + RIGHT * 0.28, angle=0.45)),
            run_time=1.2
        )
        self.remove(p1, p2)
        self.play(ReplacementTransform(l_y, l_py), ReplacementTransform(r_y, r_py), run_time=0.6)

        self.at("neighboring amino")
        mot_l = T("+2 Asn", size=26, color=GREEN, weight=BOLD).move_to([-2.5, 0.45, 0])
        mot_r = T("Cbl site", size=26, color=ORANGE, weight=BOLD).move_to([2.5, 0.45, 0])
        self.play(FadeIn(mot_l), FadeIn(mot_r), run_time=0.9)

        self.at("growth branch")
        grb2 = make_sh2_cup("Grb2", GREEN, facing=1, size=26, min_w=1.75, height=0.64)
        grb2.move_to([-4.9, l_py.pill.get_center()[1], 0])
        ras_box = boxed_label("growth branch", GREEN, size=26, fill_opacity=0.30).move_to([-3.4, -2.45, 0])
        dock_l_x = l_py.tab.get_left()[0] - grb2.width / 2 - 0.04
        arr_l = make_arrow_between(
            np.array([dock_l_x, l_py.pill.get_center()[1] - 0.44, 0]),
            ras_box.get_top() + UP * 0.12, GREEN, width=6.0
        )
        self.play(
            FadeIn(grb2),
            grb2.animate.move_to([dock_l_x, l_py.pill.get_center()[1], 0]),
            Create(arr_l), FadeIn(ras_box),
            run_time=1.0
        )

        self.at("removal tagger")
        cbl = make_sh2_cup("Cbl", ORANGE, facing=-1, size=26, min_w=1.60, height=0.64)
        cbl.move_to([4.9, r_py.pill.get_center()[1], 0])
        lyso_box = boxed_label("Lysosome", RED, size=26, fill_opacity=0.30).move_to([3.4, -2.45, 0])
        dock_r_x = r_py.tab.get_right()[0] + cbl.width / 2 + 0.04
        arr_r = make_arrow_between(
            np.array([dock_r_x, r_py.pill.get_center()[1] - 0.44, 0]),
            lyso_box.get_top() + UP * 0.12, ORANGE, width=6.0
        )
        self.play(
            FadeIn(cbl),
            cbl.animate.move_to([dock_r_x, r_py.pill.get_center()[1], 0]),
            Create(arr_r), FadeIn(lyso_box),
            run_time=1.0
        )

        self.at("together")
        ptp = make_ptp_clipper().move_to([-5.0, -0.5, 0])
        ptp_lab = T("PTPs", size=26, color=SILVER, weight=BOLD).next_to(ptp, LEFT, buff=0.14)
        ptp_grp = VGroup(ptp, ptp_lab)
        self.play(
            FadeIn(ptp_grp),
            grb2.animate.shift(LEFT * 1.4 + DOWN * 0.8).set_opacity(0),
            FadeOut(arr_l), FadeOut(ras_box),
            run_time=1.0
        )
        self.play(
            ptp_grp.animate.move_to([l_py.tab.get_left()[0] - ptp_grp.width / 2 - 0.12, l_py.pill.get_center()[1], 0]),
            run_time=1.2
        )

        self.at("clear the board")
        rest_l = make_monomer(-1.90, mem_y=1.90, side=-1, color=TEAL, active=False, tail_len=2.5, curve_amp=0.36, tail_width=10)
        rest_r = make_monomer(1.90, mem_y=1.90, side=1, color=TEAL, active=False, tail_len=2.5, curve_amp=0.36, tail_width=10)
        rest_yl = make_site_badge(rest_l.pt(0.45), side=-1, phosphorylated=False)
        rest_yr = make_site_badge(rest_r.pt(0.45), side=1, phosphorylated=False)
        rest_lab = T("resting receptor", size=30, color=TEAL, weight=BOLD).move_to([0, 3.28, 0])

        self.play(
            FadeOut(l_py), FadeOut(r_py), FadeOut(mot_l), FadeOut(mot_r),
            FadeOut(cbl), FadeOut(arr_r), FadeOut(lyso_box), FadeOut(ptp_grp),
            ReplacementTransform(sb_lab, rest_lab),
            ReplacementTransform(l_rec, rest_l),
            ReplacementTransform(r_rec, rest_r),
            run_time=1.8
        )
        self.play(FadeIn(rest_yl), FadeIn(rest_yr), run_time=0.9)
        self.finish()


class S11End(EndCard):
    LINE = "Phosphotyrosines recruit specific partners by sequence to branch and end signaling."
