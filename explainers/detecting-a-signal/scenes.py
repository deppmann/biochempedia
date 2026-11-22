"""Finding One Signal in a Crowd (detecting-a-signal)

COLOUR MAP (one colour per concept, used consistently across the entire film):
- BYSTANDER  (#7A8599) : slate grey — water, albumin, and background cell proteins (shapes only; never text)
- TARGET     (GOLD, #D4A843) : gold — insulin, sample hormone, and the target protein / peptides
- ANTIBODY   (#B388FF) : violet — Y-shaped antibodies and phosphospecific antibodies
- PHOSPHATE  (GREEN, #83C167) : emerald green — phosphate group (+80 Da)
- TRACER     (BLUE, #58C4DD) : cyan — radioactive tracer tag, computed RIA curve, and negative SDS charges
- BLIND_SPOT (RED, #FC6255) : coral red — blind-spot badges, missing fragment breaks, and missed sites
- TEXT       (#E8EAF0) : off-white — primary high-contrast labels

ONE PICTURE OF THE WORLD (carried across scenes):
Three persistent lab-bench zones spanning y in [-2.60, 2.70]:
  Left   ("Sample crowd", x in [-6.35, -2.45]) : molecules, extracts, and peptides entering the assay
  Center ("Selector",     x in [-2.20,  1.45]) : limiting antibodies, polyacrylamide gel, or MS/MS chamber
  Right  ("Readout",      x in [ 1.70,  6.35]) : dial/plot, western blot membrane, or fragment mass ladder
Top banner (y = 3.20) holds the active question, formula, or method title; bottom band (y = -3.10) holds
predict cards and schematic tags.

PER-SCENE CHANGES & COMPUTATIONS:
- s01_hook          : Bounded 2D random walk (rng(7)) of blood/cell molecules; log-ratio counters tick to 1:10^12 water & 1:10^7 albumin; cell protein receives one phosphate.
- s02_ria_setup     : Tracer and unlabelled hormone dynamically occupy/displace 8 limiting antibody tips while dial tracks exact bound tracer fraction (0% -> 100% -> 25%).
- s03_ria_math      : u_tracker (0 -> 100 pM) drives tight-binding mass-action RIA curve (R_tot=40, T=100, Kd=0.5 pM) to (100, 2010 cpm) as antibody sites split 4/8 tracer, 4/8 sample.
- s04_predict_q     : 3:1 crowd (300 pM sample : 100 pM tracer) streams in; dashed guide marks x = 300 pM and "?" on the computed curve.
- s05_pause         : PredictPause holds question card and x = 300 pM guide while countdown ring empties and molecules continue thermal drift.
- s06_ria_reveal    : u_tracker sweeps 100 -> 300 -> 500 pM through (300, 1007 cpm) as tips settle to 2/8 tracer, then flags antibody selectivity blind spot.
- s07_western       : Folded proteins straighten under SDS+heat with length-proportional "-" charges, migrate in gel by Rf = a - b*log10(MW), transfer to membrane, and bind phospho-antibody.
- s08_western_limits: Paired Resting/Stimulated blot strips step cleanly through equal vs rising total protein, then a second unsuspected phosphate appears while antibody misses it.
- s09_msms          : Trypsin snips protein into 5-bead peptides; MS1 peak shifts +80 Da (1,000 -> 1,080 Da); MS2 cuts bonds 1..4 so computed fragment ladder shifts +80 Da at residue 3.
- s10_close         : Removing cut between residues 2 & 3 drops fragment 1-2 and brackets 2 ambiguous residues; all three method readouts settle with blind-spot badges.
"""
from bp_parts import *

# ------------------------------------------------------------------ Colour map
BYSTANDER = "#7A8599"
TARGET = GOLD
ANTIBODY = "#B388FF"
PHOSPHATE = GREEN
TRACER = BLUE
BLIND_SPOT = RED
PANEL_FILL = "#161B27"
SLAB_FILL = "#202A3E"

# ------------------------------------------------------------------ Zone geometry
LEFT_X0, LEFT_X1 = -6.35, -2.45
CENT_X0, CENT_X1 = -2.20, 1.45
RIGHT_X0, RIGHT_X1 = 1.70, 6.35
ZONE_Y0, ZONE_Y1 = -2.60, 2.70
PREDICT_Y0 = -2.38

# ------------------------------------------------------------------ Physical models
# RIA tight-binding equilibrium: R_tot = 40 pM, T = 100 pM, Kd = 0.5 pM
R_TOT = 40.0
TRACER_PM = 100.0
KD_PM = 0.5


def _bound_total(L):
    s = R_TOT + L + KD_PM
    return 0.5 * (s - np.sqrt(s * s - 4.0 * R_TOT * L))


_B0 = _bound_total(TRACER_PM)


def ria_cpm(u):
    """Computed bound tracer counts (cpm) as a function of unlabelled hormone u (pM)."""
    L = TRACER_PM + u
    bt = _bound_total(L) * (TRACER_PM / L)
    return 4000.0 * bt / _B0


def sds_rf(mw_kda):
    """SDS-PAGE migration model: Rf = clip(a - b * log10(MW), 0.14, 0.88)."""
    return float(np.clip(2.22 - 0.92 * np.log10(mw_kda), 0.14, 0.88))


# MS/MS 5-bead peptide residue masses (Da), unphosphorylated total = 1,000 Da
BEAD_MASSES = np.array([190.0, 210.0, 185.0, 215.0, 200.0])
PHOS_MASS = 80.0
PHOS_IDX = 2  # 0-based index of phosphorylated residue (3rd residue)


def frag_masses(with_phos=True):
    cum = np.cumsum(BEAD_MASSES)
    if with_phos:
        cum[PHOS_IDX:] += PHOS_MASS
    return cum


# ------------------------------------------------------------------ Reusable picture builders
def make_zone(x0, x1, y0, y1, title, title_color=TEXT):
    w, h = x1 - x0, y1 - y0
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    box = RoundedRectangle(
        corner_radius=0.18, width=w, height=h,
        stroke_color=GREY, stroke_width=2.2,
        fill_color=PANEL_FILL, fill_opacity=0.65,
    ).move_to([cx, cy, 0])
    head = fit_text(title, max_w=w - 0.35, size=26, color=title_color, weight=BOLD).move_to([cx, y1 - 0.28, 0])
    rule = Line([x0 + 0.18, y1 - 0.54, 0], [x1 - 0.18, y1 - 0.54, 0], color=GREY, stroke_width=1.6).set_opacity(0.65)
    g = VGroup(box, rule, head)
    g.box, g.head, g.rule = box, head, rule
    return g


def make_three_zones(left_title="Sample crowd", cent_title="Selector", right_title="Readout"):
    lz = make_zone(LEFT_X0, LEFT_X1, ZONE_Y0, ZONE_Y1, left_title, TARGET)
    cz = make_zone(CENT_X0, CENT_X1, ZONE_Y0, ZONE_Y1, cent_title, ANTIBODY)
    rz = make_zone(RIGHT_X0, RIGHT_X1, ZONE_Y0, ZONE_Y1, right_title, TRACER)
    return lz, cz, rz


def add_brownian_walk(dots, bounds, rng, speed=0.25):
    """Attach a bounded 2D thermal random-walk updater to a list/VGroup of dots."""
    x0, x1, y0, y1 = bounds
    for d in dots:
        ang = rng.uniform(0, TAU)
        d._vx = speed * np.cos(ang)
        d._vy = speed * np.sin(ang)

        def step(mob, dt, x0=x0, x1=x1, y0=y0, y1=y1, rng=rng, speed=speed):
            if dt <= 0:
                return
            mob._vx += rng.normal(0, 0.35 * speed) * np.sqrt(dt)
            mob._vy += rng.normal(0, 0.35 * speed) * np.sqrt(dt)
            sp = np.hypot(mob._vx, mob._vy)
            if sp > 1.6 * speed:
                mob._vx *= 1.6 * speed / sp
                mob._vy *= 1.6 * speed / sp
            nx = mob.get_x() + mob._vx * dt
            ny = mob.get_y() + mob._vy * dt
            if nx < x0:
                nx = x0 + (x0 - nx)
                mob._vx = abs(mob._vx)
            elif nx > x1:
                nx = x1 - (nx - x1)
                mob._vx = -abs(mob._vx)
            if ny < y0:
                ny = y0 + (y0 - ny)
                mob._vy = abs(mob._vy)
            elif ny > y1:
                ny = y1 - (ny - y1)
                mob._vy = -abs(mob._vy)
            mob.move_to([nx, ny, 0])

        d.add_updater(step)


def make_tracer_dot(pos=ORIGIN, radius=0.135):
    core = Dot(pos, radius=radius * 0.65, color=TARGET)
    ring = Circle(radius=radius, color=TRACER, stroke_width=4.2).move_to(pos)
    return VGroup(ring, core)


def make_sample_dot(pos=ORIGIN, radius=0.13):
    return Dot(pos, radius=radius, color=TARGET)


def make_antibody(center, scale=1.0, color=ANTIBODY):
    """Y-shaped antibody cartoon; stores .tips = [left_tip, right_tip] for bound molecules."""
    c = np.array(center, dtype=float)
    s = scale
    stem = Line(c + DOWN * 0.56 * s, c + UP * 0.02 * s, color=color, stroke_width=8.5 * s)
    arm_l = Line(c + UP * 0.02 * s, c + np.array([-0.42 * s, 0.48 * s, 0]), color=color, stroke_width=8.0 * s)
    arm_r = Line(c + UP * 0.02 * s, c + np.array([0.42 * s, 0.48 * s, 0]), color=color, stroke_width=8.0 * s)
    cup_l = Arc(radius=0.14 * s, start_angle=0.45 * PI, angle=-1.15 * PI, arc_center=c + np.array([-0.48 * s, 0.54 * s, 0]),
                color=color, stroke_width=5.5 * s)
    cup_r = Arc(radius=0.14 * s, start_angle=0.55 * PI, angle=1.15 * PI, arc_center=c + np.array([0.48 * s, 0.54 * s, 0]),
                color=color, stroke_width=5.5 * s)
    g = VGroup(stem, arm_l, arm_r, cup_l, cup_r)
    g.tips = [c + np.array([-0.49 * s, 0.55 * s, 0]), c + np.array([0.49 * s, 0.55 * s, 0])]
    return g


def make_antibody_grid(cx=-0.375, cy=0.22):
    positions = [
        [cx - 0.85, cy + 0.90, 0],
        [cx + 0.85, cy + 0.90, 0],
        [cx - 0.85, cy - 0.62, 0],
        [cx + 0.85, cy - 0.62, 0],
    ]
    abs_list = [make_antibody(p, scale=0.96) for p in positions]
    tips = []
    for ab in abs_list:
        tips.extend(ab.tips)
    return VGroup(*abs_list), tips


def make_ria_plot():
    P = Plot(
        box=(2.90, 5.92, -1.42, 1.38),
        xr=(0, 500),
        yr=(0, 4000),
        xticks=[0, 100, 300, 500],
        yticks=[(0, "0"), (2000, "2,000"), (4000, "4,000")],
        xlabel="Sample hormone (pM)",
        ylabel="Bound counts (cpm)",
        color=TEXT,
        size=22,
        label_size=24,
        stroke=2.8,
    )
    # Give y-tick labels a tiny extra left margin from the curve start dot at (0, 4000)
    for tl in P.tick_labels:
        if tl.get_center()[0] < P.x0:
            tl.shift(LEFT * 0.06)
    return P


def live_ria_area(P, tracker, x0=0.0):
    """Shaded region under the computed RIA curve from x0 up to tracker."""
    def mk():
        x1 = tracker.get_value()
        if x1 - x0 <= 1e-3:
            return VMobject()
        xs = np.linspace(x0, x1, max(4, int(60 * (x1 - x0) / 500.0) + 2))
        pts = [P.pt(x0, 0)] + [P.pt(x, ria_cpm(x)) for x in xs] + [P.pt(x1, 0)]
        poly = Polygon(*pts, stroke_width=0, fill_color=TRACER, fill_opacity=0.22)
        return poly
    return always_redraw(mk)


def ria_area_static(P, x0, x1):
    xs = np.linspace(x0, x1, 40)
    pts = [P.pt(x0, 0)] + [P.pt(x, ria_cpm(x)) for x in xs] + [P.pt(x1, 0)]
    return Polygon(*pts, stroke_width=0, fill_color=TRACER, fill_opacity=0.22)


def populate_sample_crowd(rng, x0, x1, y0, y1, n_bystander=34, n_tracer=6, n_sample=6):
    bystanders = VGroup()
    for _ in range(n_bystander):
        p = [rng.uniform(x0, x1), rng.uniform(y0, y1), 0]
        bystanders.add(Dot(p, radius=rng.uniform(0.075, 0.11), color=BYSTANDER).set_opacity(0.90))
    tracers = VGroup()
    for _ in range(n_tracer):
        p = [rng.uniform(x0, x1), rng.uniform(y0, y1), 0]
        tracers.add(make_tracer_dot(p, radius=0.12))
    samples = VGroup()
    for _ in range(n_sample):
        p = [rng.uniform(x0, x1), rng.uniform(y0, y1), 0]
        samples.add(make_sample_dot(p, radius=0.12))
    add_brownian_walk(bystanders, (x0, x1, y0, y1), rng, speed=0.22)
    add_brownian_walk(tracers, (x0, x1, y0, y1), rng, speed=0.26)
    add_brownian_walk(samples, (x0, x1, y0, y1), rng, speed=0.26)
    return bystanders, tracers, samples


def make_predict_backdrop(u_val=100.0):
    """Exact world at the end of S04PredictQ, shared with S05Pause."""
    rng = np.random.default_rng(7)
    lz = make_zone(LEFT_X0, LEFT_X1, PREDICT_Y0, ZONE_Y1, "Sample crowd", TARGET)
    cz = make_zone(CENT_X0, CENT_X1, PREDICT_Y0, ZONE_Y1, "Selector", ANTIBODY)
    rz = make_zone(RIGHT_X0, RIGHT_X1, PREDICT_Y0, ZONE_Y1, "Computed model", TRACER)
    by, tr, sa = populate_sample_crowd(rng, LEFT_X0 + 0.25, LEFT_X1 - 0.25, PREDICT_Y0 + 0.65, ZONE_Y1 - 0.75,
                                       n_bystander=32, n_tracer=5, n_sample=15)
    left_sub = T("300 pM + 100 pM", size=24, color=TARGET).move_to([(LEFT_X0 + LEFT_X1) / 2, PREDICT_Y0 + 0.28, 0])

    abs_grp, _ = make_antibody_grid()
    cent_sub = T("Limiting antibody", size=24, color=ANTIBODY).move_to([(CENT_X0 + CENT_X1) / 2, PREDICT_Y0 + 0.28, 0])
    c_tr = VGroup(*[make_tracer_dot([rng.uniform(CENT_X0 + 0.35, CENT_X1 - 0.35),
                                     rng.uniform(-1.62, -1.12), 0], radius=0.105) for _ in range(4)])
    c_sa = VGroup(*[make_sample_dot([rng.uniform(CENT_X0 + 0.35, CENT_X1 - 0.35),
                                     rng.uniform(-1.62, -1.12), 0], radius=0.105) for _ in range(12)])
    add_brownian_walk(c_tr, (CENT_X0 + 0.30, CENT_X1 - 0.30, -1.65, -1.08), rng, speed=0.28)
    add_brownian_walk(c_sa, (CENT_X0 + 0.30, CENT_X1 - 0.30, -1.65, -1.08), rng, speed=0.28)
    q_marks = VGroup(*[T("?", size=26, color=GOLD, weight=BOLD).move_to(ab.get_center() + UP * 0.36) for ab in abs_grp])

    P = make_ria_plot()
    area = ria_area_static(P, 0, u_val)
    curve = P.curve(ria_cpm, x0=0, x1=u_val, color=TRACER, width=6.0)
    dot = Dot(P.pt(u_val, ria_cpm(u_val)), radius=0.10, color=TARGET, stroke_color=TRACER, stroke_width=3)
    guide = DashedLine(P.pt(300, 0), P.pt(300, 2100), color=GOLD, stroke_width=3, dash_length=0.14)
    q_pt = T("?", size=28, color=GOLD, weight=BOLD).next_to(P.pt(300, 1007), UR, buff=0.14)
    formula = M("100 / (100 + 300) = ?", size=32, color=TEXT).move_to([0, 3.22, 0])
    return VGroup(lz, cz, rz, by, tr, sa, left_sub, abs_grp, cent_sub, c_tr, c_sa, q_marks,
                  P, area, curve, dot, guide, q_pt, formula)


# ------------------------------------------------------------------ Scenes
class S00Title(TitleCard):
    LESSON = "How We Know: Detecting a Signal"
    TITLE = "Finding One Signal in a Crowd"


class S01Hook(SpokenScene):
    def construct(self):
        rng = np.random.default_rng(7)
        blood_box = RoundedRectangle(
            corner_radius=0.18, width=7.80, height=3.15,
            stroke_color=GREY, stroke_width=2.2, fill_color=PANEL_FILL, fill_opacity=0.65,
        ).move_to([-2.45, 1.05, 0])
        blood_head = T("Blood sample (schematic)", size=26, color=TEXT, weight=BOLD).move_to([-2.45, 2.34, 0])
        blood_rule = Line([-6.15, 2.08, 0], [1.25, 2.08, 0], color=GREY, stroke_width=1.6).set_opacity(0.65)
        rz = make_zone(RIGHT_X0, RIGHT_X1, -0.52, 2.62, "Signal vs crowd", TRACER)

        bx0, bx1, by0, by1 = -6.10, 1.20, -0.35, 1.42
        waters = VGroup(*[
            Dot([rng.uniform(bx0, bx1), rng.uniform(by0, by1), 0],
                radius=rng.uniform(0.065, 0.09), color=BYSTANDER).set_opacity(0.78)
            for _ in range(115)
        ])
        albumins = VGroup(*[
            Dot([rng.uniform(bx0, bx1), rng.uniform(by0, by1), 0],
                radius=rng.uniform(0.115, 0.145), color=BYSTANDER).set_opacity(0.92)
            for _ in range(28)
        ])
        insulin = Dot([-2.45, 0.55, 0], radius=0.16, color=TARGET)
        insulin_ring = always_redraw(lambda: Circle(radius=0.26, color=TARGET, stroke_width=3.2).move_to(insulin))
        insulin_legend = VGroup(
            Dot([-3.35, 1.76, 0], radius=0.11, color=TARGET),
            T("1 insulin", size=26, color=TARGET, weight=BOLD).move_to([-2.35, 1.76, 0]),
        )

        add_brownian_walk(waters, (bx0, bx1, by0, by1), rng, speed=0.28)
        add_brownian_walk(albumins, (bx0, bx1, by0, by1), rng, speed=0.22)
        add_brownian_walk([insulin], (-4.20, -0.60, -0.05, 1.15), rng, speed=0.24)

        water_exp = ValueTracker(0.0)
        alb_exp = ValueTracker(0.0)
        SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
        water_counter = always_redraw(lambda: M(
            f"1 : 10{str(int(round(water_exp.get_value()))).translate(SUP)} water",
            size=30, color=TEXT,
        ).move_to([4.02, 1.35, 0]))
        alb_counter = always_redraw(lambda: M(
            f"1 : 10{str(int(round(alb_exp.get_value()))).translate(SUP)} albumin",
            size=30, color=TEXT,
        ).move_to([4.02, 0.25, 0]))

        self.add(blood_box, blood_head, blood_rule, rz)
        self.play(FadeIn(waters), run_time=1.0)

        self.at("one insulin")
        self.add(insulin, insulin_ring, water_counter)
        self.play(
            FadeIn(insulin_legend),
            water_exp.animate(rate_func=linear).set_value(12.0),
            run_time=2.2,
        )

        self.at("How do you")
        q_banner = T("How do you find one signal in a crowd?", size=32, color=GOLD, weight=BOLD).move_to([0, 3.22, 0])
        self.play(FadeIn(q_banner), run_time=0.8)

        self.at("or locate")
        cell_box = RoundedRectangle(
            corner_radius=0.18, width=12.70, height=2.25,
            stroke_color=GREY, stroke_width=2.2, fill_color=PANEL_FILL, fill_opacity=0.65,
        ).move_to([0.0, -1.92, 0])
        cell_head = T("Inside a cell (schematic)", size=26, color=PHOSPHATE, weight=BOLD).move_to([-4.05, -1.12, 0])
        cx0, cx1, cy0, cy1 = -6.00, 1.80, -2.85, -1.58
        cell_prots = VGroup(*[
            RoundedRectangle(corner_radius=0.06, width=rng.uniform(0.40, 0.68), height=0.21,
                           stroke_color=BYSTANDER, stroke_width=2, fill_color=BYSTANDER, fill_opacity=0.75)
            .move_to([rng.uniform(cx0, cx1), rng.uniform(cy0, cy1), 0])
            for _ in range(32)
        ])
        target_prot = RoundedRectangle(
            corner_radius=0.08, width=1.40, height=0.36,
            stroke_color=TARGET, stroke_width=3.5, fill_color=TARGET, fill_opacity=0.55,
        ).move_to([3.10, -2.18, 0])
        phos_dot = Dot(target_prot.get_right() + LEFT * 0.16 + UP * 0.22, radius=0.13, color=PHOSPHATE)
        phos_lab = T("1 phosphate", size=24, color=PHOSPHATE, weight=BOLD).next_to(phos_dot, RIGHT, buff=0.20)
        self.play(FadeIn(cell_box), FadeIn(cell_head), FadeIn(target_prot), FadeIn(phos_dot), FadeIn(phos_lab), run_time=1.4)

        self.at("Albumin outnumbers")
        self.add(alb_counter)
        self.play(
            FadeIn(albumins),
            alb_exp.animate(rate_func=linear).set_value(7.0),
            run_time=1.2,
        )

        self.at("Inside cells")
        add_brownian_walk(cell_prots, (cx0, cx1, cy0, cy1), rng, speed=0.22)
        self.play(FadeIn(cell_prots), run_time=1.6)
        self.finish()


class S02RiaSetup(SpokenScene):
    def construct(self):
        rng = np.random.default_rng(7)
        lz, cz, rz = make_three_zones("Sample crowd", "Selector", "Readout")
        top_title = T("Competition for limiting antibody", size=30, color=TEXT, weight=BOLD).move_to([0, 3.22, 0])

        by, _, sa_left = populate_sample_crowd(
            rng, LEFT_X0 + 0.25, LEFT_X1 - 0.25, ZONE_Y0 + 0.55, ZONE_Y1 - 0.75,
            n_bystander=30, n_tracer=0, n_sample=10,
        )
        abs_grp, tips = make_antibody_grid()
        cent_sub = T("Limiting antibody", size=24, color=ANTIBODY).move_to([(CENT_X0 + CENT_X1) / 2, ZONE_Y0 + 0.28, 0])

        bound_frac = ValueTracker(0.0)
        gauge = dial(bound_frac, center=[4.02, 0.25, 0], radius=1.55, label="Bound radioactivity", color=TRACER, size=38)
        sites_tracker = ValueTracker(0.0)
        sites_note = counter("{:.0f} / 8 sites tracer", sites_tracker, at=[4.02, -1.75, 0], size=26, color=TRACER)
        tag = scope_tag("schematic")

        self.add(lz, cz, rz, top_title, by, sa_left, tag, gauge, sites_note)
        self.play(FadeIn(abs_grp, shift=UP * 0.2), FadeIn(cent_sub), run_time=1.6)

        self.at("Put the same")
        bound_tracers = [make_tracer_dot([LEFT_X1 + 0.1, rng.uniform(-1.5, 1.8), 0], radius=0.12) for _ in range(8)]
        bouncer1 = Dot([LEFT_X1 - 0.2, 1.1, 0], radius=0.12, color=BYSTANDER)
        bouncer2 = Dot([LEFT_X1 - 0.2, -0.5, 0], radius=0.12, color=BYSTANDER)
        self.add(*bound_tracers, bouncer1, bouncer2)
        self.play(
            *[t.animate.move_to(tip) for t, tip in zip(bound_tracers, tips)],
            Succession(bouncer1.animate.move_to(tips[0] + LEFT * 0.28), bouncer1.animate.move_to([LEFT_X1 - 0.3, 1.3, 0])),
            Succession(bouncer2.animate.move_to(tips[4] + LEFT * 0.28), bouncer2.animate.move_to([LEFT_X1 - 0.3, -0.7, 0])),
            bound_frac.animate.set_value(1.0),
            sites_tracker.animate.set_value(8.0),
            run_time=3.2,
        )
        self.remove(bouncer1, bouncer2)

        self.at("With few")
        site_rings = VGroup(*[Circle(radius=0.18, color=GOLD, stroke_width=3.0).move_to(tip) for tip in tips])
        self.play(FadeIn(site_rings), run_time=0.7)
        self.play(FadeOut(site_rings), run_time=0.6)

        self.at("sample hormone")
        replace_idx_1 = [0, 3, 5, 6]
        displaced_1 = [bound_tracers[i] for i in replace_idx_1]
        incoming_1 = [make_sample_dot([LEFT_X1 - 0.2, tips[i][1] + rng.uniform(-0.3, 0.3), 0], radius=0.12) for i in replace_idx_1]
        self.add(*incoming_1)
        self.play(
            *[m.animate.move_to(tips[i]) for m, i in zip(incoming_1, replace_idx_1)],
            *[d.animate.shift(RIGHT * 0.65 + UP * 0.45) for d in displaced_1],
            bound_frac.animate.set_value(0.50),
            sites_tracker.animate.set_value(4.0),
            run_time=3.0,
        )
        self.play(*[FadeOut(d) for d in displaced_1], run_time=0.5)

        self.at("more sample")
        replace_idx_2 = [1, 7]
        displaced_2 = [bound_tracers[i] for i in replace_idx_2]
        incoming_2 = [make_sample_dot([LEFT_X1 - 0.2, tips[i][1] + rng.uniform(-0.3, 0.3), 0], radius=0.12) for i in replace_idx_2]
        self.add(*incoming_2)
        self.play(
            *[m.animate.move_to(tips[i]) for m, i in zip(incoming_2, replace_idx_2)],
            *[d.animate.shift(RIGHT * 0.65 + DOWN * 0.45) for d in displaced_2],
            bound_frac.animate.set_value(0.25),
            sites_tracker.animate.set_value(2.0),
            run_time=2.6,
        )
        self.play(*[FadeOut(d) for d in displaced_2], run_time=0.5)
        self.finish()


class S03RiaMath(SpokenScene):
    def construct(self):
        rng = np.random.default_rng(7)
        lz, cz, rz = make_three_zones("Sample crowd", "Selector", "Computed binding model")
        by, tr, _ = populate_sample_crowd(
            rng, LEFT_X0 + 0.25, LEFT_X1 - 0.25, ZONE_Y0 + 0.65, ZONE_Y1 - 0.75,
            n_bystander=30, n_tracer=8, n_sample=0,
        )
        left_sub = T("100 pM tracer", size=24, color=TRACER).move_to([(LEFT_X0 + LEFT_X1) / 2, ZONE_Y0 + 0.28, 0])

        abs_grp, tips = make_antibody_grid()
        cent_sub = T("8 / 8 tracer", size=24, color=TRACER).move_to([(CENT_X0 + CENT_X1) / 2, ZONE_Y0 + 0.28, 0])
        tip_tracers = [make_tracer_dot(tip, radius=0.12) for tip in tips]

        P = make_ria_plot()
        u_tracker = ValueTracker(0.0)
        area = live_ria_area(P, u_tracker, x0=0.0)
        live = P.live_curve(ria_cpm, u_tracker, color=TRACER, width=6.0)
        dot = P.dot(lambda: u_tracker.get_value(), lambda: ria_cpm(u_tracker.get_value()), color=TARGET, ring=TRACER, radius=0.095)
        readout = always_redraw(lambda: M(
            f"{u_tracker.get_value():.0f} pM : {ria_cpm(u_tracker.get_value()):,.0f}",
            size=22, color=TEXT,
        ).move_to([4.95, 1.05, 0]))
        tag = scope_tag("computed model")

        self.add(lz, cz, rz, by, tr, abs_grp, *tip_tracers, tag)
        self.play(Create(P), run_time=1.5)

        self.at("Labeled fraction")
        formula = M("Labelled fraction = T / (T + U)", size=32, color=TEXT).move_to([0, 3.22, 0])
        self.play(FadeIn(formula), run_time=1.4)

        self.at("Put")
        self.add(area, live, dot, readout)
        glow = Dot(P.pt(0, 4000) + RIGHT * 0.08, radius=0.10, color=TRACER).set_opacity(0.65)
        self.play(FadeIn(left_sub), FadeIn(cent_sub), FadeIn(glow), run_time=0.6)
        self.play(FadeOut(glow), run_time=0.6)

        self.at("Add")
        sa = VGroup(*[
            make_sample_dot([rng.uniform(LEFT_X0 + 0.25, LEFT_X1 - 0.25),
                             rng.uniform(ZONE_Y0 + 0.65, ZONE_Y1 - 0.75), 0], radius=0.12)
            for _ in range(8)
        ])
        add_brownian_walk(sa, (LEFT_X0 + 0.25, LEFT_X1 - 0.25, ZONE_Y0 + 0.65, ZONE_Y1 - 0.75), rng, speed=0.26)
        new_left_sub = T("100 pM + 100 pM", size=24, color=TARGET).move_to(left_sub.get_center())
        new_cent_sub = T("4 / 8 tracer", size=24, color=TARGET).move_to(cent_sub.get_center())

        swap_idx = [1, 2, 5, 6]
        gold_at_tips = [make_sample_dot(tips[i], radius=0.12) for i in swap_idx]
        self.play(
            FadeIn(sa),
            swap(left_sub, new_left_sub, run_time=0.8),
            swap(cent_sub, new_cent_sub, run_time=0.8),
            *[FadeOut(tip_tracers[i]) for i in swap_idx],
            *[FadeIn(g) for g in gold_at_tips],
            u_tracker.animate(rate_func=linear).set_value(100.0),
            run_time=2.6,
        )

        self.at("100 over 200")
        formula_2 = M("100 / (100 + 100) = 1/2  ->  ~2,000 cpm", size=32, color=TRACER).move_to([0, 3.22, 0])
        self.play(swap(formula, formula_2, run_time=0.9), run_time=1.0)
        self.finish()


class S04PredictQ(SpokenScene):
    def construct(self):
        rng = np.random.default_rng(7)
        lz = make_zone(LEFT_X0, LEFT_X1, PREDICT_Y0, ZONE_Y1, "Sample crowd", TARGET)
        cz = make_zone(CENT_X0, CENT_X1, PREDICT_Y0, ZONE_Y1, "Selector", ANTIBODY)
        rz = make_zone(RIGHT_X0, RIGHT_X1, PREDICT_Y0, ZONE_Y1, "Computed model", TRACER)
        by, tr, sa = populate_sample_crowd(
            rng, LEFT_X0 + 0.25, LEFT_X1 - 0.25, PREDICT_Y0 + 0.65, ZONE_Y1 - 0.75,
            n_bystander=30, n_tracer=5, n_sample=5,
        )
        left_sub = T("100 pM + 100 pM", size=24, color=TARGET).move_to([(LEFT_X0 + LEFT_X1) / 2, PREDICT_Y0 + 0.28, 0])

        abs_grp, tips = make_antibody_grid()
        cent_sub = T("4 / 8 tracer", size=24, color=TARGET).move_to([(CENT_X0 + CENT_X1) / 2, PREDICT_Y0 + 0.28, 0])
        bound_mobs = VGroup(*[
            make_sample_dot(tips[i], radius=0.12) if i in (1, 2, 5, 6) else make_tracer_dot(tips[i], radius=0.12)
            for i in range(8)
        ])

        P = make_ria_plot()
        area = ria_area_static(P, 0, 100)
        curve = P.curve(ria_cpm, x0=0, x1=100, color=TRACER, width=6.0)
        dot = Dot(P.pt(100, ria_cpm(100)), radius=0.10, color=TARGET, stroke_color=TRACER, stroke_width=3)
        formula = M("100 / (100 + 100) = 1/2  ->  ~2,000 cpm", size=32, color=TRACER).move_to([0, 3.22, 0])
        self.add(lz, cz, rz, by, tr, sa, left_sub, abs_grp, cent_sub, bound_mobs, P, area, curve, dot, formula)

        self.at("Suppose the sample")
        extra_sa = VGroup(*[
            make_sample_dot([rng.uniform(LEFT_X0 + 0.25, LEFT_X1 - 0.25),
                             rng.uniform(PREDICT_Y0 + 0.65, ZONE_Y1 - 0.75), 0], radius=0.12)
            for _ in range(10)
        ])
        add_brownian_walk(extra_sa, (LEFT_X0 + 0.25, LEFT_X1 - 0.25, PREDICT_Y0 + 0.65, ZONE_Y1 - 0.75), rng, speed=0.26)
        new_left_sub = T("300 pM + 100 pM", size=24, color=TARGET).move_to(left_sub.get_center())
        new_cent_sub = T("Limiting antibody", size=24, color=ANTIBODY).move_to(cent_sub.get_center())

        c_tr = VGroup(*[make_tracer_dot([rng.uniform(CENT_X0 + 0.35, CENT_X1 - 0.35),
                                         rng.uniform(-1.62, -1.12), 0], radius=0.105) for _ in range(4)])
        c_sa = VGroup(*[make_sample_dot([rng.uniform(CENT_X0 + 0.35, CENT_X1 - 0.35),
                                         rng.uniform(-1.62, -1.12), 0], radius=0.105) for _ in range(12)])
        add_brownian_walk(c_tr, (CENT_X0 + 0.30, CENT_X1 - 0.30, -1.65, -1.08), rng, speed=0.28)
        add_brownian_walk(c_sa, (CENT_X0 + 0.30, CENT_X1 - 0.30, -1.65, -1.08), rng, speed=0.28)
        q_marks = VGroup(*[T("?", size=26, color=GOLD, weight=BOLD).move_to(ab.get_center() + UP * 0.36) for ab in abs_grp])
        formula_q = M("100 / (100 + 300) = ?", size=32, color=TEXT).move_to([0, 3.22, 0])

        self.play(
            FadeIn(extra_sa),
            swap(left_sub, new_left_sub, run_time=0.8),
            swap(cent_sub, new_cent_sub, run_time=0.8),
            swap(formula, formula_q, run_time=0.8),
            FadeOut(bound_mobs),
            FadeIn(c_tr), FadeIn(c_sa), FadeIn(q_marks),
            run_time=2.2,
        )

        self.at("Tracer over")
        guide = DashedLine(P.pt(300, 0), P.pt(300, 2100), color=GOLD, stroke_width=3, dash_length=0.14)
        q_pt = T("?", size=28, color=GOLD, weight=BOLD).next_to(P.pt(300, 1007), UR, buff=0.14)
        self.play(Create(guide), FadeIn(q_pt), run_time=1.3)

        self.at("What fraction")
        qcard = question_card(
            "300 pM sample + 100 pM tracer: fraction labelled & bound counts?",
            y=-3.10, size=28, max_w=10.6,
        )
        self.play(FadeIn(qcard), run_time=1.0)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = "300 pM sample + 100 pM tracer: fraction labelled & bound counts?"
    CARD = {"y": -3.10, "size": 28, "max_w": 10.6}
    SECONDS = 4.5

    def backdrop(self):
        return make_predict_backdrop(100.0)


class S06RiaReveal(SpokenScene):
    def construct(self):
        rng = np.random.default_rng(7)
        lz, cz, rz = make_three_zones("Sample crowd", "Selector", "Computed model")
        by, tr, sa = populate_sample_crowd(
            rng, LEFT_X0 + 0.25, LEFT_X1 - 0.25, ZONE_Y0 + 0.65, ZONE_Y1 - 0.75,
            n_bystander=30, n_tracer=5, n_sample=15,
        )
        left_sub = T("300 pM + 100 pM", size=24, color=TARGET).move_to([(LEFT_X0 + LEFT_X1) / 2, ZONE_Y0 + 0.28, 0])
        abs_grp, tips = make_antibody_grid()
        cent_sub = T("Limiting antibody", size=24, color=ANTIBODY).move_to([(CENT_X0 + CENT_X1) / 2, ZONE_Y0 + 0.28, 0])

        P = make_ria_plot()
        u_tracker = ValueTracker(100.0)
        base_area = ria_area_static(P, 0, 100)
        live_area = live_ria_area(P, u_tracker, x0=100.0)
        base_curve = P.curve(ria_cpm, x0=0, x1=100, color=TRACER, width=6.0)
        live = P.live_curve(ria_cpm, u_tracker, x0=100, color=TRACER, width=6.0)
        dot = P.dot(lambda: u_tracker.get_value(), lambda: ria_cpm(u_tracker.get_value()), color=TARGET, ring=TRACER, radius=0.095)
        readout = always_redraw(lambda: M(
            f"{u_tracker.get_value():.0f} pM : {ria_cpm(u_tracker.get_value()):,.0f}",
            size=22, color=TEXT,
        ).move_to([4.95, 1.05, 0]))
        guide = DashedLine(P.pt(300, 0), P.pt(300, 2100), color=GOLD, stroke_width=3, dash_length=0.14)
        formula = M("100 / (100 + 300) = ?", size=32, color=TEXT).move_to([0, 3.22, 0])
        tag = scope_tag("computed model")

        self.add(lz, cz, rz, by, tr, sa, left_sub, abs_grp, cent_sub, P,
                 base_area, live_area, base_curve, live, dot, readout, guide, formula, tag)

        formula_ans = M("100 / 400 = 1/4  ->  ~1,000 cpm", size=32, color=TRACER).move_to([0, 3.22, 0])
        bound_2_of_8 = VGroup(*[
            make_tracer_dot(tips[i], radius=0.12) if i in (0, 4) else make_sample_dot(tips[i], radius=0.12)
            for i in range(8)
        ])
        new_cent_sub = T("2 / 8 (1/4) tracer", size=24, color=TRACER).move_to(cent_sub.get_center())
        self.play(
            swap(formula, formula_ans, run_time=0.8),
            swap(cent_sub, new_cent_sub, run_time=0.8),
            FadeIn(bound_2_of_8),
            run_time=0.8,
        )
        self.play(
            u_tracker.animate(rate_func=linear).set_value(300.0),
            run_time=3.5,
        )

        self.at("Known standards")
        pt_300 = Dot(P.pt(300, ria_cpm(300)), radius=0.095, color=GOLD)
        self.add(pt_300)
        readout.clear_updaters()
        self.play(
            FadeOut(guide),
            FadeOut(readout),
            FadeOut(left_sub),
            FadeOut(new_cent_sub),
            FadeOut(formula_ans),
            run_time=0.6,
        )
        self.play(
            u_tracker.animate(rate_func=linear).set_value(500.0),
            run_time=2.5,
        )

        self.at("That is the")
        ria_title = T("Radioimmunoassay (RIA)", size=32, color=TEXT, weight=BOLD).move_to([0, 3.22, 0])
        self.play(FadeIn(ria_title), run_time=0.9)

        self.at("blind spot")
        hl_ring = Circle(radius=0.22, color=BLIND_SPOT, stroke_width=4.5).move_to(tips[7])
        blind_tag = boxed_label("Only as selective\nas the antibody", color=BLIND_SPOT, size=22, pad=0.16)
        blind_tag.move_to([-0.38, -2.02, 0])
        arr = Arrow(blind_tag.get_top() + RIGHT * 0.65, tips[7] + DOWN * 0.22, buff=0.08, color=BLIND_SPOT, stroke_width=3.8)
        self.play(Create(hl_ring), FadeIn(blind_tag), GrowArrow(arr), run_time=1.6)
        self.finish()


class S07Western(SpokenScene):
    def construct(self):
        lz, cz, rz = make_three_zones("Cell extract", "Polyacrylamide gel", "Western blot")
        title = T("SDS-PAGE & western blot", size=30, color=TEXT, weight=BOLD).move_to([0, 3.22, 0])
        tag = scope_tag("schematic")

        def folded_squiggle(center, w, color):
            c = np.array(center, dtype=float)
            pts = [c + np.array([(-0.5 + i / 6.0) * w, 0.22 * np.sin(i * 1.9), 0]) for i in range(7)]
            m = VMobject(color=color, stroke_width=9.5)
            m.set_points_as_corners(pts)
            return m

        fold_specs = [
            ("120", 120.0, 1.90, BYSTANDER, False),
            ("60_u", 60.0, 1.35, TARGET, False),
            ("60_p", 60.0, 1.35, TARGET, True),
            ("32", 32.0, 0.92, BYSTANDER, False),
        ]
        folded_y = [1.45, 0.55, -0.35, -1.25]
        folded_mobs = VGroup()
        for (_, _, w, col, has_p), y in zip(fold_specs, folded_y):
            sq = folded_squiggle([-4.40, y, 0], w, col)
            if has_p:
                pdot = Dot(sq.get_right() + UP * 0.16, radius=0.14, color=PHOSPHATE)
                folded_mobs.add(VGroup(sq, pdot))
            else:
                folded_mobs.add(sq)

        gel = RoundedRectangle(
            corner_radius=0.10, width=2.02, height=3.20,
            stroke_color=TRACER, stroke_width=2.8, fill_color=SLAB_FILL, fill_opacity=0.95,
        ).move_to([0.32, 0.18, 0])
        minus_sign = M("-", size=28, color=TRACER).next_to(gel, UP, buff=0.06)
        plus_sign = M("+", size=28, color=BLIND_SPOT).next_to(gel, DOWN, buff=0.06)
        lane_x = [-0.18, 0.80]
        well_y = 1.56
        wells = VGroup(*[
            Rectangle(width=0.76, height=0.16, stroke_color=GREY, stroke_width=2, fill_color=BG, fill_opacity=1.0)
            .move_to([lx, well_y, 0])
            for lx in lane_x
        ])

        membrane = RoundedRectangle(
            corner_radius=0.10, width=3.55, height=3.20,
            stroke_color=TEXT, stroke_width=2.8, fill_color=SLAB_FILL, fill_opacity=0.95,
        ).move_to([4.02, 0.18, 0])

        self.add(lz, cz, rz, title, tag, folded_mobs, gel, wells, minus_sign, plus_sign, membrane)

        self.at("Heating a cell")
        sds_badge = boxed_label("SDS + heat", color=TRACER, size=24).move_to([-4.40, -2.08, 0])
        heat_flash = RoundedRectangle(
            corner_radius=0.16, width=3.55, height=3.65,
            stroke_color=BLIND_SPOT, stroke_width=4, fill_color=BLIND_SPOT, fill_opacity=0.20,
        ).move_to([-4.40, 0.15, 0])
        self.play(FadeIn(sds_badge), FadeIn(heat_flash), run_time=1.0)
        self.play(FadeOut(heat_flash), run_time=0.8)

        self.at("unfolds")
        rods = VGroup()
        rod_widths = [2.45, 1.65, 1.65, 1.00]
        for (_, _, _, col, has_p), y, rw in zip(fold_specs, folded_y, rod_widths):
            rod = RoundedRectangle(
                corner_radius=0.06, width=rw, height=0.25,
                stroke_width=0, fill_color=col, fill_opacity=0.95,
            ).move_to([-4.40, y, 0])
            if has_p:
                pdot = Dot(rod.get_right() + UP * 0.18, radius=0.13, color=PHOSPHATE)
                rods.add(VGroup(rod, pdot))
            else:
                rods.add(rod)
        self.play(*[Transform(f, r) for f, r in zip(folded_mobs, rods)], run_time=2.2)

        self.at("negative charge")
        charges = VGroup()
        for mob, rw in zip(folded_mobs, rod_widths):
            n_ch = max(2, int(round(rw * 3.0)))
            xs = np.linspace(-rw / 2 + 0.14, rw / 2 - 0.14, n_ch)
            cy = mob.get_center()[1] if isinstance(mob, RoundedRectangle) else mob[0].get_center()[1]
            for dx in xs:
                charges.add(M("-", size=24, color=TRACER).move_to([-4.40 + dx, cy - 0.24, 0]))
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.12) for c in charges], lag_ratio=0.05), run_time=2.2)

        self.at("An electric field")
        gel_top, gel_bot = 1.38, -1.25
        def gel_y(mw):
            return gel_top - sds_rf(mw) * (gel_top - gel_bot)

        band_specs = [
            (lane_x[0], 120.0, 0.74, BYSTANDER, False),
            (lane_x[0], 60.0, 0.56, TARGET, False),
            (lane_x[0], 32.0, 0.38, BYSTANDER, False),
            (lane_x[1], 120.0, 0.74, BYSTANDER, False),
            (lane_x[1], 60.0, 0.56, TARGET, True),
            (lane_x[1], 32.0, 0.38, BYSTANDER, False),
        ]
        gel_bands = VGroup()
        gel_targets = []
        for lx, mw, bw, col, has_p in band_specs:
            start_b = RoundedRectangle(corner_radius=0.05, width=bw, height=0.26,
                                       stroke_width=0, fill_color=col, fill_opacity=0.95).move_to([-4.40, well_y, 0])
            end_y = gel_y(mw)
            if has_p:
                pdot = Dot([-4.40 + bw / 2 + 0.12, well_y, 0], radius=0.105, color=PHOSPHATE)
                gel_bands.add(VGroup(start_b, pdot))
            else:
                gel_bands.add(start_b)
            gel_targets.append((lx, end_y))

        field_arrow = Arrow([-2.06, 1.35, 0], [-2.06, -1.15, 0], color=TRACER, stroke_width=5.5, max_tip_length_to_length_ratio=0.12)
        self.play(
            GrowArrow(field_arrow),
            *[b.animate.move_to([lx + (0.06 if has_p else 0), well_y, 0]) for b, (lx, _), (_, _, _, _, has_p) in zip(gel_bands, gel_targets, band_specs)],
            run_time=1.8,
        )
        # Continuous migration down gel finishing as "smaller proteins travel farther" is spoken
        self.play(
            *[b.animate.shift(DOWN * (well_y - ty)) for b, (_, ty) in zip(gel_bands, gel_targets)],
            run_time=2.6,
            rate_func=linear,
        )
        size_labels = VGroup(
            T("120 kDa", size=22, color=TEXT).move_to([-0.79, gel_y(120.0), 0], aligned_edge=RIGHT),
            T("60 kDa", size=22, color=TARGET).move_to([-0.79, gel_y(60.0), 0], aligned_edge=RIGHT),
            T("32 kDa", size=22, color=TEXT).move_to([-0.79, gel_y(32.0), 0], aligned_edge=RIGHT),
        )
        self.play(FadeIn(size_labels), run_time=0.6)

        self.at("Transfer the bands")
        mem_lane_x = [3.10, 4.45]
        mem_bands = VGroup()
        for (lx, mw, bw, col, has_p), (_, ty) in zip(band_specs, gel_targets):
            mx = mem_lane_x[0] if lx == lane_x[0] else mem_lane_x[1]
            b = RoundedRectangle(corner_radius=0.05, width=bw, height=0.26,
                                 stroke_width=0, fill_color=col, fill_opacity=0.95).move_to([mx, ty, 0])
            if has_p:
                pdot = Dot([mx + bw / 2 + 0.12, ty, 0], radius=0.105, color=PHOSPHATE)
                mem_bands.add(VGroup(b, pdot))
            else:
                mem_bands.add(b)
        tx_arr1 = Arrow([1.40, 0.5, 0], [2.18, 0.5, 0], color=TEXT, stroke_width=4.5)
        tx_arr2 = Arrow([1.40, -0.3, 0], [2.18, -0.3, 0], color=TEXT, stroke_width=4.5)
        self.play(GrowArrow(tx_arr1), GrowArrow(tx_arr2), run_time=0.7)
        self.play(FadeIn(mem_bands, shift=RIGHT * 1.6), run_time=2.3)

        self.at("A phosphospecific")
        unphos_target = mem_bands[1].get_center()
        phos_band = mem_bands[4]
        phos_target = phos_band[0].get_center()

        ab_pass = make_antibody([2.55, unphos_target[1] - 0.55, 0], scale=0.40)
        ab_bind = make_antibody([5.40, phos_target[1], 0], scale=0.42).rotate(PI / 2)
        ab_note = boxed_label("Binds only with phosphate", color=ANTIBODY, size=22, pad=0.16).move_to([4.02, -2.08, 0])
        self.play(FadeIn(ab_pass), FadeIn(ab_bind), FadeIn(ab_note), run_time=1.0)

        glow_band = RoundedRectangle(
            corner_radius=0.09, width=0.90, height=0.44,
            stroke_color=PHOSPHATE, stroke_width=5.5, fill_color=PHOSPHATE, fill_opacity=0.68,
        ).move_to(phos_target)
        # Bind + light up phosphorylated band while unbinding antibody drifts past unphosphorylated band and fades
        self.play(
            ab_bind.animate.move_to([5.14, phos_target[1], 0]),
            ab_pass.animate(rate_func=linear).move_to([2.55, unphos_target[1] + 0.05, 0]),
            run_time=1.8,
        )
        self.play(
            ab_pass.animate(rate_func=linear).move_to([2.55, unphos_target[1] + 0.40, 0]).set_opacity(0),
            run_time=1.2,
        )
        self.remove(ab_pass)
        self.play(FadeIn(glow_band, scale=1.18), run_time=1.6)
        self.finish()


class S08WesternLimits(SpokenScene):
    def construct(self):
        title = T("Western blot: two pitfalls", size=30, color=TEXT, weight=BOLD).move_to([0, 3.22, 0])
        tag = scope_tag("schematic")

        mem = RoundedRectangle(
            corner_radius=0.18, width=10.8, height=4.6,
            stroke_color=TEXT, stroke_width=2.5, fill_color=SLAB_FILL, fill_opacity=0.92,
        ).move_to([0.0, -0.05, 0])
        lane_rest = T("Resting", size=28, color=TEXT, weight=BOLD).move_to([0.75, 1.78, 0])
        lane_stim = T("Stimulated", size=28, color=TEXT, weight=BOLD).move_to([3.55, 1.78, 0])

        p_strip = RoundedRectangle(
            corner_radius=0.10, width=5.25, height=0.88,
            stroke_color="#B4BDCB", stroke_width=2.0, fill_color="#E8ECF2", fill_opacity=0.96,
        ).move_to([2.15, 0.72, 0])
        t_strip = RoundedRectangle(
            corner_radius=0.10, width=5.25, height=0.88,
            stroke_color="#B4BDCB", stroke_width=2.0, fill_color="#E8ECF2", fill_opacity=0.96,
        ).move_to([2.15, -0.72, 0])

        p_lab = T("Phospho-specific", size=26, color=PHOSPHATE, weight=BOLD).move_to([-4.95, 0.72, 0], aligned_edge=LEFT)
        p_rest = RoundedRectangle(corner_radius=0.06, width=1.75, height=0.30, stroke_width=0, fill_color="#9BB892", fill_opacity=0.42).move_to([0.75, 0.72, 0])
        p_stim = RoundedRectangle(corner_radius=0.06, width=1.75, height=0.36, stroke_color="#143D1D", stroke_width=2.0, fill_color="#1D5A2A", fill_opacity=0.95).move_to([3.55, 0.72, 0])

        t_lab = T("Total protein", size=26, color=TARGET, weight=BOLD).move_to([-4.95, -0.72, 0], aligned_edge=LEFT)
        t_rest = RoundedRectangle(corner_radius=0.06, width=1.75, height=0.32, stroke_width=0, fill_color="#C9B27C", fill_opacity=0.48).move_to([0.75, -0.72, 0])
        t_stim_eq = RoundedRectangle(corner_radius=0.06, width=1.75, height=0.32, stroke_width=0, fill_color="#C9B27C", fill_opacity=0.48).move_to([3.55, -0.72, 0])
        t_stim_dark = RoundedRectangle(corner_radius=0.06, width=1.75, height=0.42, stroke_color="#3A2400", stroke_width=2.5, fill_color="#593805", fill_opacity=0.96).move_to([3.55, -0.72, 0])

        self.add(title, tag, mem, lane_rest, lane_stim, p_strip, p_lab, p_rest, p_stim)
        self.play(FadeIn(t_strip), FadeIn(t_lab), FadeIn(t_rest), FadeIn(t_stim_eq), run_time=1.8)

        self.at("Otherwise")
        case1 = boxed_label("Steady total  ->  More phosphate / protein", color=PHOSPHATE, size=24).move_to([0.0, -1.78, 0])
        self.play(FadeIn(case1), run_time=0.9)
        self.wait(0.7)

        self.at("from more protein")
        case2 = boxed_label("Darker total  ->  More protein", color=TARGET, size=24).move_to([0.0, -1.78, 0])
        self.play(FadeOut(case1), run_time=0.20)
        self.play(Transform(t_stim_eq, t_stim_dark), FadeIn(case2), run_time=0.25)

        self.at("An antibody also")
        blot_all = VGroup(mem, lane_rest, lane_stim, p_strip, p_lab, p_rest, p_stim, t_strip, t_lab, t_rest, t_stim_eq, case2)
        prot = RoundedRectangle(
            corner_radius=0.22, width=9.6, height=0.76,
            stroke_color=TARGET, stroke_width=3.5, fill_color=TARGET, fill_opacity=0.38,
        ).move_to([0.0, -0.05, 0])
        known_mark = DashedLine([-2.6, -0.48, 0], [-2.6, 0.38, 0], color=ANTIBODY, stroke_width=3.5)
        known_lab = T("Known site (empty)", size=26, color=ANTIBODY).move_to([-2.6, -1.05, 0])
        ab = make_antibody([-2.6, 1.45, 0], scale=1.00).rotate(PI)
        ab_lab = T("Phosphospecific antibody", size=26, color=ANTIBODY).next_to(ab, UP, buff=0.14)
        self.play(FadeOut(blot_all), FadeIn(prot), run_time=0.8)
        self.play(Create(known_mark), FadeIn(known_lab), FadeIn(ab), FadeIn(ab_lab), run_time=1.4)

        self.at("Raised against")
        new_p = Dot([2.4, 0.42, 0], radius=0.21, color=PHOSPHATE)
        new_p_ring = Circle(radius=0.34, color=PHOSPHATE, stroke_width=3.5).move_to(new_p)
        new_p_lab = T("Unsuspected phosphate", size=26, color=PHOSPHATE).move_to([2.4, -1.05, 0])
        missed = boxed_label("Unsuspected site missed", color=BLIND_SPOT, size=26).move_to([0.0, -3.10, 0])
        self.play(FadeIn(new_p), Create(new_p_ring), FadeIn(new_p_lab), run_time=1.0)
        ab_grp = VGroup(ab, ab_lab)
        self.play(
            ab_grp.animate(rate_func=linear).shift(RIGHT * 6.2 + UP * 0.36),
            FadeIn(missed, rate_func=lambda t: min(1.0, t / 0.45)),
            run_time=2.1,
        )
        self.play(
            FadeOut(ab_grp, shift=RIGHT * 1.2 + UP * 0.24, rate_func=linear),
            run_time=0.7,
        )
        self.remove(ab_grp)
        self.finish()


class S09Msms(SpokenScene):
    def construct(self):
        lz, cz, rz = make_three_zones("Trypsin digest", "MS/MS (schematic)", "Fragment ladder")
        title = T("Tandem mass spectrometry (MS/MS)", size=30, color=TEXT, weight=BOLD).move_to([0, 3.22, 0])
        tag = scope_tag("schematic")

        chain_beads = VGroup()
        for i in range(15):
            bx = -5.75 + (i % 5) * 0.56
            by = 1.45 - (i // 5) * 1.15
            dot = Circle(radius=0.22, color=TARGET, stroke_width=3.2, fill_color=TARGET, fill_opacity=0.65).move_to([bx, by, 0])
            if i == 7:
                p = Dot([bx, by + 0.33, 0], radius=0.125, color=PHOSPHATE)
                chain_beads.add(VGroup(dot, p))
            else:
                chain_beads.add(dot)
        links = VGroup()
        for i in range(14):
            p1 = chain_beads[i][0].get_center() if isinstance(chain_beads[i], VGroup) else chain_beads[i].get_center()
            p2 = chain_beads[i + 1][0].get_center() if isinstance(chain_beads[i + 1], VGroup) else chain_beads[i + 1].get_center()
            if (i + 1) % 5 != 0:
                links.add(Line(p1, p2, color=TARGET, stroke_width=4.5))
            else:
                links.add(DashedLine(p1, p2, color=GREY, stroke_width=2.5, dash_length=0.08))

        ms1 = Plot(
            box=(-1.62, 1.22, -0.75, 1.38),
            xr=(950, 1130), yr=(0, 1.2),
            xticks=[(1000, "1,000"), (1080, "1,080")],
            yticks=[],
            xlabel="Mass (Da)",
            ylabel="Stage 1",
            color=TEXT, size=22, label_size=22, stroke=2.5,
        )
        p1000_b, p1000_t = ms1.pt(1000, 0), ms1.pt(1000, 0.90)
        p1080_b, p1080_t = ms1.pt(1080, 0), ms1.pt(1080, 0.90)
        pk_1000 = Rectangle(width=0.30, height=p1000_t[1] - p1000_b[1], stroke_color=TARGET, stroke_width=2.5,
                            fill_color=TARGET, fill_opacity=0.88).move_to([(p1000_b[0] + p1000_t[0]) / 2, (p1000_b[1] + p1000_t[1]) / 2, 0])
        pk_1080 = Rectangle(width=0.30, height=p1080_t[1] - p1080_b[1], stroke_color=PHOSPHATE, stroke_width=2.5,
                            fill_color=PHOSPHATE, fill_opacity=0.92).move_to([(p1080_b[0] + p1080_t[0]) / 2, (p1080_b[1] + p1080_t[1]) / 2, 0])
        # Put shift arrow above the peaks (y_data=1.02) so "+80 Da" sits cleanly above both peaks
        shift_arr = Arrow(ms1.pt(1008, 1.02), ms1.pt(1072, 1.02), buff=0, color=PHOSPHATE, stroke_width=4.5)
        shift_lab = M("+80 Da", size=24, color=PHOSPHATE).next_to(shift_arr, UP, buff=0.14)

        self.add(lz, cz, rz, title, tag, links, chain_beads)
        self.wait(0.8)

        self.at("Cut the protein")
        cut_mark1 = VGroup(
            Line([-0.18, 0.09, 0], [0.18, -0.09, 0], color=TEXT, stroke_width=4.0),
            Line([-0.18, -0.09, 0], [0.18, 0.09, 0], color=TEXT, stroke_width=4.0),
        ).move_to(links[4].get_center())
        cut_mark2 = cut_mark1.copy().move_to(links[9].get_center())
        trypsin_lab = T("Trypsin", size=24, color=TEXT).move_to([-4.40, -1.90, 0])
        top_pep = VGroup(*[chain_beads[i] for i in range(0, 5)], *[links[i] for i in range(0, 4)])
        mid_pep = VGroup(*[chain_beads[i] for i in range(5, 10)], *[links[i] for i in range(5, 9)])
        bot_pep = VGroup(*[chain_beads[i] for i in range(10, 15)], *[links[i] for i in range(10, 14)])
        self.play(FadeIn(cut_mark1), FadeIn(cut_mark2), FadeIn(trypsin_lab), run_time=1.0)
        self.play(
            FadeOut(links[4]), FadeOut(links[9]),
            top_pep.animate.shift(UP * 0.25),
            bot_pep.animate.shift(DOWN * 0.25),
            run_time=1.4,
        )
        self.play(FadeOut(cut_mark1), FadeOut(cut_mark2), run_time=0.4)

        self.at("weigh each")
        fly_unphos = top_pep.copy()
        self.add(fly_unphos)
        self.play(
            fly_unphos.animate.scale(0.6).move_to(ms1.pt(1000, 1.05)).set_opacity(0),
            Create(ms1), GrowFromEdge(pk_1000, DOWN),
            run_time=1.8,
        )
        self.remove(fly_unphos)

        self.at("One phosphate adds")
        fly_phos = mid_pep.copy()
        self.add(fly_phos)
        self.play(
            fly_phos.animate.scale(0.6).move_to(ms1.pt(1080, 1.05)).set_opacity(0),
            pk_1000.animate.set_fill(opacity=0.30).set_stroke(opacity=0.45),
            GrowFromEdge(pk_1080, DOWN),
            GrowArrow(shift_arr),
            FadeIn(shift_lab),
            run_time=2.6,
        )
        self.remove(fly_phos)

        self.at("Tandem mass")
        stage1_all = VGroup(ms1, pk_1000, pk_1080, shift_arr, shift_lab)
        s2_head = M("1,080 Da peptide", size=24, color=PHOSPHATE).move_to([-0.38, 1.55, 0])
        frag_beads = VGroup()
        for idx in range(5):
            bx = -1.58 + idx * 0.60
            dot = Circle(radius=0.22, color=TARGET, stroke_width=3.2, fill_color=TARGET, fill_opacity=0.58).move_to([bx, 0.65, 0])
            num = M(str(idx + 1), size=22, color=TEXT).move_to(dot)
            if idx == PHOS_IDX:
                p = Dot([bx, 0.99, 0], radius=0.12, color=PHOSPHATE)
                frag_beads.add(VGroup(dot, num, p))
            else:
                frag_beads.add(VGroup(dot, num))
        frag_links = VGroup(*[
            Line([-1.36 + idx * 0.60, 0.65, 0], [-1.20 + idx * 0.60, 0.65, 0], color=TARGET, stroke_width=4.5)
            for idx in range(4)
        ])
        self.play(FadeOut(stage1_all), run_time=0.5)
        self.play(FadeIn(s2_head), FadeIn(frag_links), FadeIn(frag_beads), run_time=1.4)

        self.at("Break that heavier")
        cut_lines = VGroup(*[
            DashedLine([-1.28 + idx * 0.60, 1.05, 0], [-1.28 + idx * 0.60, 0.20, 0], color=TRACER, stroke_width=4.0, dash_length=0.08)
            for idx in range(4)
        ])
        break_lab = T("Backbone breaks", size=24, color=TRACER).move_to([-0.38, -0.35, 0])
        # Show fragment slices popping below the peptide as each bond breaks
        slice_bars = VGroup(*[
            Rectangle(width=(k + 1) * 0.56, height=0.16, stroke_color=PHOSPHATE if k >= PHOS_IDX else TARGET,
                      stroke_width=2, fill_color=PHOSPHATE if k >= PHOS_IDX else TARGET, fill_opacity=0.65)
            .move_to([-1.80 + (k + 1) * 0.28, -0.82 - k * 0.28, 0])
            for k in range(4)
        ])
        self.play(FadeIn(break_lab), run_time=0.5)
        self.play(
            LaggedStart(*[AnimationGroup(Create(cl), FadeIn(sb, shift=DOWN * 0.15)) for cl, sb in zip(cut_lines, slice_bars)], lag_ratio=0.45),
            run_time=3.8,
        )

        self.at("Fragments carrying")
        self.play(FadeOut(slice_bars), run_time=0.25)
        unmod_m = frag_masses(with_phos=False)
        phos_m = frag_masses(with_phos=True)
        ladder_x0 = 2.68
        ladder_w = 2.65
        max_m = 1120.0
        row_ys = [1.35, 0.58, -0.19, -0.96, -1.73]
        row_names = ["1", "1-2", "1-3", "1-4", "1-5"]

        row_anims = []
        for r_idx, (rn, um, pm, ry) in enumerate(zip(row_names, unmod_m, phos_m, row_ys)):
            r_lab = M(rn, size=22, color=TEXT).move_to([2.18, ry, 0])
            uw = ladder_w * (um / max_m)
            pw = ladder_w * (pm / max_m)
            u_bar = Rectangle(width=uw, height=0.36, stroke_color=GREY, stroke_width=2,
                              fill_color=TARGET, fill_opacity=0.38).move_to([ladder_x0 + uw / 2, ry, 0])
            if r_idx >= PHOS_IDX:
                p_bar = Rectangle(width=pw, height=0.36, stroke_color=PHOSPHATE, stroke_width=2.5,
                                  fill_color=PHOSPHATE, fill_opacity=0.88).move_to([ladder_x0 + pw / 2, ry, 0])
                plus_tag = M("+80", size=22, color=PHOSPHATE).next_to(p_bar, RIGHT, buff=0.10)
                # Animate bars separately from labels so bars never sweep across text in motion
                row_anims.append(AnimationGroup(FadeIn(r_lab), GrowFromEdge(u_bar, LEFT), GrowFromEdge(p_bar, LEFT), FadeIn(plus_tag)))
            else:
                row_anims.append(AnimationGroup(FadeIn(r_lab), GrowFromEdge(u_bar, LEFT)))

        res_ring = Circle(radius=0.32, color=PHOSPHATE, stroke_width=4.5).move_to(frag_beads[PHOS_IDX][0])
        res_lab = T("Residue 3: +80 Da", size=24, color=PHOSPHATE, weight=BOLD).move_to([-0.38, -1.35, 0])
        self.play(
            LaggedStart(*row_anims, lag_ratio=0.35),
            Create(res_ring),
            FadeIn(res_lab),
            run_time=2.3,
        )
        self.finish()


class S10Close(SpokenScene):
    def construct(self):
        lz, cz, rz = make_three_zones("Trypsin digest", "MS/MS (schematic)", "Fragment ladder")
        title = T("Mass spectrometry blind spot", size=30, color=TEXT, weight=BOLD).move_to([0, 3.22, 0])
        tag = scope_tag("schematic")

        s2_head = M("1,080 Da peptide", size=24, color=PHOSPHATE).move_to([-0.38, 1.55, 0])
        frag_beads = VGroup()
        for idx in range(5):
            bx = -1.58 + idx * 0.60
            dot = Circle(radius=0.22, color=TARGET, stroke_width=3.2, fill_color=TARGET, fill_opacity=0.58).move_to([bx, 0.65, 0])
            num = M(str(idx + 1), size=22, color=TEXT).move_to(dot)
            if idx == PHOS_IDX:
                p = Dot([bx, 0.99, 0], radius=0.12, color=PHOSPHATE)
                frag_beads.add(VGroup(dot, num, p))
            else:
                frag_beads.add(VGroup(dot, num))
        frag_links = VGroup(*[
            Line([-1.36 + idx * 0.60, 0.65, 0], [-1.20 + idx * 0.60, 0.65, 0], color=TARGET, stroke_width=4.5)
            for idx in range(4)
        ])
        cut_lines = VGroup(*[
            DashedLine([-1.28 + idx * 0.60, 1.05, 0], [-1.28 + idx * 0.60, 0.20, 0], color=TRACER, stroke_width=4.0, dash_length=0.08)
            for idx in range(4)
        ])

        unmod_m = frag_masses(with_phos=False)
        phos_m = frag_masses(with_phos=True)
        ladder_x0, ladder_w, max_m = 2.68, 2.65, 1120.0
        row_ys = [1.35, 0.58, -0.19, -0.96, -1.73]
        row_names = ["1", "1-2", "1-3", "1-4", "1-5"]
        ladder_rows = VGroup()
        for r_idx, (rn, um, pm, ry) in enumerate(zip(row_names, unmod_m, phos_m, row_ys)):
            r_lab = M(rn, size=22, color=TEXT).move_to([2.18, ry, 0])
            uw, pw = ladder_w * (um / max_m), ladder_w * (pm / max_m)
            u_bar = Rectangle(width=uw, height=0.36, stroke_color=GREY, stroke_width=2,
                              fill_color=TARGET, fill_opacity=0.38).move_to([ladder_x0 + uw / 2, ry, 0])
            if r_idx >= PHOS_IDX:
                p_bar = Rectangle(width=pw, height=0.36, stroke_color=PHOSPHATE, stroke_width=2.5,
                                  fill_color=PHOSPHATE, fill_opacity=0.88).move_to([ladder_x0 + pw / 2, ry, 0])
                plus_tag = M("+80", size=22, color=PHOSPHATE).next_to(p_bar, RIGHT, buff=0.10)
                ladder_rows.add(VGroup(r_lab, u_bar, p_bar, plus_tag))
            else:
                ladder_rows.add(VGroup(r_lab, u_bar))

        pep_note = T("5-residue peptide", size=24, color=TARGET).move_to([-4.40, 0.65, 0])
        self.add(lz, cz, rz, title, tag, s2_head, frag_links, frag_beads, cut_lines, ladder_rows, pep_note)

        # Substantial highlight sweeping onto cut 1-2 & row 1-2
        cut_ptr = Arrow([-0.68, -0.45, 0], [-0.68, 0.16, 0], buff=0, color=BLIND_SPOT, stroke_width=5.0)
        row_hl = RoundedRectangle(
            corner_radius=0.08, width=4.26, height=0.58,
            stroke_color=BLIND_SPOT, stroke_width=3.5, fill_color=BLIND_SPOT, fill_opacity=0.22,
        ).move_to([3.93, row_ys[1], 0])
        self.play(GrowArrow(cut_ptr), FadeIn(row_hl), run_time=1.8)

        self.at("If no break")
        self.play(FadeOut(cut_ptr), FadeOut(row_hl), FadeOut(cut_lines[1]), FadeOut(ladder_rows[1]), run_time=2.0)

        self.at("the site stays")
        b_left = frag_beads[1][0].get_left()[0] - 0.03
        b_right = frag_beads[2][0].get_right()[0] + 0.03
        ambig_box = RoundedRectangle(
            corner_radius=0.10, width=b_right - b_left + 0.02, height=1.12,
            stroke_color=BLIND_SPOT, stroke_width=3.5, fill_color=BLIND_SPOT, fill_opacity=0.25,
        ).move_to([(b_left + b_right) / 2, 0.75, 0])
        bracket = VGroup(
            Line([b_left, 0.12, 0], [b_left, -0.05, 0], color=BLIND_SPOT, stroke_width=4.5),
            Line([b_left, -0.05, 0], [b_right, -0.05, 0], color=BLIND_SPOT, stroke_width=4.5),
            Line([b_right, -0.05, 0], [b_right, 0.12, 0], color=BLIND_SPOT, stroke_width=4.5),
        )
        ambig = fit_text("No break here -> 2 residues possible", max_w=3.2, size=24, color=BLIND_SPOT, max_lines=2)
        ambig.move_to([-0.38, -0.75, 0])
        self.play(FadeIn(ambig_box), Create(bracket), FadeIn(ambig), run_time=0.9)

        self.at("Competition")
        work_mobs = VGroup(s2_head, frag_links, frag_beads, cut_lines[0], cut_lines[2], cut_lines[3],
                           ladder_rows[0], ladder_rows[2], ladder_rows[3], ladder_rows[4], pep_note,
                           ambig_box, bracket, ambig)
        summary_title = T("Three ways to find one signal", size=30, color=TEXT, weight=BOLD).move_to([0, 3.22, 0])

        c1_x = (LEFT_X0 + LEFT_X1) / 2
        c2_x = (CENT_X0 + CENT_X1) / 2
        c3_x = (RIGHT_X0 + RIGHT_X1) / 2
        h1_new = T("Competition (RIA)", size=26, color=TRACER, weight=BOLD).move_to(lz.head.get_center())
        h2_new = T("Antibodies (Blot)", size=26, color=ANTIBODY, weight=BOLD).move_to(cz.head.get_center())
        h3_new = T("Mass spectrometry", size=26, color=PHOSPHATE, weight=BOLD).move_to(rz.head.get_center())

        c1_plot = Plot(box=(LEFT_X0 + 0.65, LEFT_X1 - 0.35, -0.55, 1.45), xr=(0, 500), yr=(0, 4000),
                       xticks=[], yticks=[], color=GREY, stroke=2.5)
        c1_area = ria_area_static(c1_plot, 0, 500)
        c1_curve = c1_plot.curve(ria_cpm, color=TRACER, width=6.0)
        c1_badge = boxed_label("Antibody selectivity", color=BLIND_SPOT, size=24).move_to([c1_x, -1.65, 0])

        c2_mem = RoundedRectangle(corner_radius=0.12, width=2.8, height=2.0, stroke_color=GREY, stroke_width=2.2,
                                  fill_color=SLAB_FILL, fill_opacity=0.92).move_to([c2_x, 0.45, 0])
        c2_b1 = RoundedRectangle(corner_radius=0.05, width=0.90, height=0.22, stroke_width=0, fill_color=TARGET, fill_opacity=0.35).move_to([c2_x - 0.65, 0.85, 0])
        c2_b2 = RoundedRectangle(corner_radius=0.05, width=0.90, height=0.26, stroke_width=0, fill_color=PHOSPHATE, fill_opacity=0.95).move_to([c2_x + 0.65, 0.85, 0])
        c2_t1 = RoundedRectangle(corner_radius=0.05, width=0.90, height=0.22, stroke_width=0, fill_color=TARGET, fill_opacity=0.80).move_to([c2_x - 0.65, 0.05, 0])
        c2_t2 = RoundedRectangle(corner_radius=0.05, width=0.90, height=0.22, stroke_width=0, fill_color=TARGET, fill_opacity=0.80).move_to([c2_x + 0.65, 0.05, 0])
        c2_badge = boxed_label("Known site only", color=BLIND_SPOT, size=24).move_to([c2_x, -1.65, 0])

        c3_bars = VGroup(
            Rectangle(width=1.05, height=0.28, stroke_color=GREY, stroke_width=2, fill_color=TARGET, fill_opacity=0.38).move_to([c3_x - 0.65, 1.05, 0]),
            Rectangle(width=1.90, height=0.28, stroke_color=PHOSPHATE, stroke_width=2.5, fill_color=PHOSPHATE, fill_opacity=0.85).move_to([c3_x - 0.22, 0.45, 0]),
            Rectangle(width=2.60, height=0.28, stroke_color=PHOSPHATE, stroke_width=2.5, fill_color=PHOSPHATE, fill_opacity=0.85).move_to([c3_x + 0.12, -0.15, 0]),
        )
        c3_plus = M("+80 Da", size=24, color=PHOSPHATE).next_to(c3_bars[1], RIGHT, buff=0.12)
        c3_badge = boxed_label("Missing breaks", color=BLIND_SPOT, size=24).move_to([c3_x, -1.65, 0])

        self.play(
            FadeOut(work_mobs),
            swap(title, summary_title, run_time=0.5),
            swap(lz.head, h1_new, run_time=0.5),
            swap(cz.head, h2_new, run_time=0.5),
            swap(rz.head, h3_new, run_time=0.5),
            run_time=0.55,
        )
        self.play(
            LaggedStart(
                AnimationGroup(Create(c1_plot), FadeIn(c1_area), Create(c1_curve)),
                AnimationGroup(FadeIn(c2_mem), FadeIn(c2_b1), FadeIn(c2_b2), FadeIn(c2_t1), FadeIn(c2_t2)),
                AnimationGroup(FadeIn(c3_bars), FadeIn(c3_plus)),
                lag_ratio=0.35,
            ),
            run_time=1.5,
        )
        self.play(
            LaggedStart(FadeIn(c1_badge), FadeIn(c2_badge), FadeIn(c3_badge), lag_ratio=0.35),
            run_time=1.0,
        )
        self.finish()


class S11End(EndCard):
    LINE = "Competition, antibodies,\nand mass spectrometry detect scarce signals, each with blind spots."
