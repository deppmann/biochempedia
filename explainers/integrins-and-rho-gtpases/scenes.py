"""
"A Grip That Signals and Feels Force" — Integrins and Rho GTPases (Part 1)

COLOUR MAP (one colour per concept across the whole film):
- Matrix / vessel wall      : #D4A359 (COL_MATRIX, warm amber)
- Ligand / RGD / Fibrinogen : #F5C542 (COL_LIGAND, bright gold)
- Plasma membrane           : #5C7A99 (COL_MEMB, slate-blue)
- Integrin alpha chain      : #2EC4B6 (COL_ALPHA, teal)
- Integrin beta chain       : #FF7A66 (COL_BETA, coral)
- Actin filaments           : #E2E8F0 (COL_ACTIN, silver-white)
- Talin                     : #A882E0 (COL_TALIN, violet)
- Kindlin                   : #7E8CE0 (COL_KINDLIN, violet-slate)
- Paxillin scaffold         : #83C167 (COL_PAXILLIN, green)
- Kinases (FAK & Src)       : #38BDF8 (COL_KINASE, cyan)
- Phosphate / Tyr397        : #FACC15 (COL_PHOS, bright yellow)
- Myosin motor              : #EF4444 (COL_MYOSIN, crimson)
- Vinculin                  : #E85D9E (COL_VINCULIN, magenta)

CARRIED WORLD:
A cross-section of the cell edge filling ~70% of the frame height: amber extracellular
matrix studded with gold handles along the bottom (y = -2.15..-2.95), slate-blue plasma
membrane bilayer across the middle (y = -0.28..+0.28), and silver-white actin filaments
in the cytoplasm above (y = +2.45..+2.61), with parametric two-chain integrins spanning
the membrane.

WHAT CHANGES IN EACH SCENE (and what drives it):
- s00_title: Standard TitleCard.
- s01_hook: White blood cell decelerates along a computed braking curve and arrests on the
  amber vessel wall while blood flow streams past; view zooms into its underside cross-section
  and bidirectional signal waves travel along the single enzyme-free receptor.
- s02_structure: Single carried integrin separates into highlighted teal alpha and coral beta
  chains, sweeps single-pass transmembrane markers down the bilayer, bends and straightens
  its outer legs toward the gold RGD handle (and tests a cell-protein target), and flexes
  its bare short tails toward actin.
- s03_predict: Hormone receptor binds a soluble ligand arriving from blood while continuous
  fibrinogen rods (deterministic RNG stream) drift past and deflect off the integrin as its
  outer legs fold at the knee and its head closes; question card enters at top.
- s04_pause: Standard PredictPause holding the question card while fibrinogen rods keep
  drifting past the bent, closed integrin and the 4.5 s ring empties.
- s05_inside_out: Question clears and matrix enters cleanly while fibrinogen rods drift past
  and deflect off the bent closed head; talin and kindlin glide down to dock on the coral
  beta tail, a separation tracker pries the tails and TM helices apart, a signal sweeps
  through the membrane, and knee-bend/head-open trackers straighten the legs onto the handle.
- s06_inside_out_payoff: Inside-out signal wave travels down through the locked integrin; two
  neighbouring bent integrins straighten and slide laterally along the membrane to cluster
  beside it on the matrix, reversing the signal wave upward as outside-in signalling.
- s07_focal_adhesion: Clustered tail zone highlights, talin rods extend upward to bridge to
  actin, paxillin docks beside them, folded FAK glides in and opens via a hinge-angle
  tracker, stamps yellow Tyr397 phosphate, docks Src onto Tyr397, and Src+FAK stamp
  phosphates onto neighbours.
- s08_mechanosensing: Driven by one tension tracker, crimson myosin crossbridges step along
  and pull actin leftward against the anchored matrix, a schematic tension gauge rises,
  talin's folded bundles unfold to expose three buried yellow pockets, and magenta vinculin
  clips snap onto the pockets and actin to thicken the mechanical bridge.
- s09_closing: Pulled-back live cross-section runs the three mechanisms in sequence (bent-to-
  extended integrin grip, FAK-Src phosphorylation on paxillin, myosin-driven talin stretch
  with vinculin clips), tests an open-question bracket on other proteins, and slides the
  actin filament rightward into movement.
- s10_end: Standard EndCard with exact take-home line.
"""
from bp_parts import *

# ------------------------------------------------------------------ Colour map
COL_MATRIX = "#D4A359"
COL_LIGAND = "#F5C542"
COL_MEMB = "#5C7A99"
COL_ALPHA = "#2EC4B6"
COL_BETA = "#FF7A66"
COL_ACTIN = "#E2E8F0"
COL_TALIN = "#A882E0"
COL_KINDLIN = "#7E8CE0"
COL_PAXILLIN = "#83C167"
COL_KINASE = "#38BDF8"
COL_PHOS = "#FACC15"
COL_MYOSIN = "#EF4444"
COL_VINCULIN = "#E85D9E"

Y_MEMB = 0.0
MEMB_HALF = 0.28
Y_MAT_TOP = -2.15
Y_MAT_BOT = -2.95
Y_ACTIN = 2.45


# ------------------------------------------------------------------ Carried world builders
def build_matrix(handles_x=(-3.2, -1.6, 0.0, 1.6, 3.2), y_top=Y_MAT_TOP, y_bot=Y_MAT_BOT,
                 label=True, label_text="matrix", label_x=-5.2):
    """Amber extracellular matrix bar with collagen mesh lines and gold RGD handles."""
    g = VGroup()
    bar = Rectangle(width=13.2, height=y_top - y_bot, stroke_color=COL_MATRIX, stroke_width=3,
                    fill_color=COL_MATRIX, fill_opacity=0.22).move_to([0, (y_top + y_bot) / 2, 0])
    g.add(bar)
    for yy in (y_top - 0.20, y_top - 0.44, y_bot + 0.16):
        ln = Line([-3.7, yy, 0], [6.4, yy, 0], color=COL_MATRIX, stroke_width=1.5, stroke_opacity=0.35)
        g.add(ln)
    handles = VGroup()
    for hx in handles_x:
        stalk = Line([hx, y_top, 0], [hx, y_top + 0.14, 0], color=COL_LIGAND, stroke_width=5)
        knob = RoundedRectangle(corner_radius=0.07, width=0.30, height=0.16, stroke_color=COL_LIGAND,
                                stroke_width=2.5, fill_color=COL_LIGAND, fill_opacity=0.90).move_to([hx, y_top + 0.22, 0])
        handles.add(VGroup(stalk, knob))
    g.add(handles)
    g.handles = handles
    g.bar = bar
    if label:
        lab = T(label_text, 28, COL_MATRIX).move_to([label_x, (y_top + y_bot) / 2, 0])
        g.add(lab)
        g.label = lab
    return g


def build_membrane(y_memb=Y_MEMB, half=MEMB_HALF, width=13.2):
    """Slate-blue plasma membrane bilayer across the middle."""
    g = VGroup()
    band = Rectangle(width=width, height=2 * half, stroke_width=0, fill_color=COL_MEMB,
                     fill_opacity=0.22).move_to([0, y_memb, 0])
    top_line = Line([-width / 2, y_memb + half, 0], [width / 2, y_memb + half, 0],
                    color=COL_MEMB, stroke_width=4)
    bot_line = Line([-width / 2, y_memb - half, 0], [width / 2, y_memb - half, 0],
                    color=COL_MEMB, stroke_width=4)
    g.add(band, top_line, bot_line)
    for x in np.linspace(-width / 2 + 0.25, width / 2 - 0.25, 42):
        tk = Line([x, y_memb - half + 0.07, 0], [x, y_memb + half - 0.07, 0],
                  color=COL_MEMB, stroke_width=1.4, stroke_opacity=0.4)
        tk.layout_ok = True
        g.add(tk)
    return g


def build_actin(y_base=Y_ACTIN, x0=-6.3, x1=6.3, label=True, label_at=(-5.2, 2.92, 0)):
    """Silver-white actin filament cables in the upper cytoplasm."""
    g = VGroup()
    for dy, sw in ((0.0, 6.0), (0.16, 4.0)):
        ln = Line([x0, y_base + dy, 0], [x1, y_base + dy, 0], color=COL_ACTIN, stroke_width=sw)
        g.add(ln)
    if label:
        lab = T("actin", 28, COL_ACTIN).move_to(label_at)
        g.add(lab)
        g.label = lab
    return g


def make_integrin(xc=0.0, y_memb=Y_MEMB, bend_t=0.0, open_t=1.0, sep_t=0.5, scale=1.0,
                  alpha_col=COL_ALPHA, beta_col=COL_BETA):
    """Parametric two-chain integrin (alpha teal, beta coral) with tail separation, knee bend, and head cleft."""
    g = VGroup()
    sep = (0.14 + 0.24 * sep_t) * scale
    tail_top = y_memb + (MEMB_HALF + 0.48) * scale
    memb_bot = y_memb - MEMB_HALF * scale
    l1 = 0.78 * scale
    l2 = 0.66 * scale
    theta = -PI / 2 + 2.20 * bend_t
    u = np.array([np.cos(theta), np.sin(theta), 0.0])
    n = np.array([-np.sin(theta), np.cos(theta), 0.0])

    chains = []
    for side, col in ((-1, alpha_col), (1, beta_col)):
        x_s = xc + side * sep
        tm = RoundedRectangle(
            corner_radius=0.07 * scale,
            width=0.17 * scale,
            height=(tail_top - memb_bot),
            stroke_color=col,
            stroke_width=2.5,
            fill_color=col,
            fill_opacity=0.72,
        ).move_to([x_s, (tail_top + memb_bot) / 2, 0])

        p0 = np.array([x_s, memb_bot, 0.0])
        p1 = p0 + np.array([-0.18 * bend_t * scale, -(l1 - 0.07 * bend_t) * scale, 0.0])
        p2 = p1 + l2 * u

        leg1 = Line(p0, p1, color=col, stroke_width=10 * scale)
        knee = Dot(p1, radius=0.065 * scale, color=col)
        leg2 = Line(p1, p2, color=col, stroke_width=9 * scale)

        jaw_shift = side * (0.04 + 0.11 * open_t) * scale * n
        tip_in = side * (0.02 + 0.04 * open_t) * scale * n
        tip_out = side * (0.20 + 0.08 * open_t) * scale * n
        pts = [
            p2 + jaw_shift * 0.4,
            p2 + tip_out + 0.08 * scale * u,
            p2 + tip_out + 0.28 * scale * u,
            p2 + tip_in + 0.32 * scale * u,
            p2 + jaw_shift * 0.2 + 0.14 * scale * u,
        ]
        head = Polygon(*pts, stroke_color=col, stroke_width=2.5, fill_color=col, fill_opacity=0.80)
        chain_g = VGroup(tm, leg1, knee, leg2, head)
        chain_g.tail_top = np.array([x_s, tail_top, 0.0])
        chain_g.tm = tm
        chain_g.knee = knee
        chain_g.head = head
        chains.append(chain_g)
        g.add(chain_g)

    g.alpha_chain, g.beta_chain = chains
    return g


def build_phosphate(pos, radius=0.18):
    """Bright yellow phosphate starburst badge with 'P'."""
    star = Star(n=8, outer_radius=radius * 1.35, inner_radius=radius * 1.02,
                color=COL_PHOS, fill_color=COL_PHOS, fill_opacity=0.95, stroke_width=1.5).move_to(pos)
    p_size = max(14, int(22 * radius / 0.18))
    p = T("P", p_size, "#0f1117", weight=BOLD).move_to(pos)
    p.layout_ok = "small"
    return VGroup(star, p)


def build_fak(pos, open_t=0.0, scale=1.0):
    """Hinged cyan FAK block: kinase body + hinged FERM cap that swings open as open_t goes 0 -> 1."""
    g = VGroup()
    kinase = RoundedRectangle(corner_radius=0.12, width=1.15 * scale, height=0.52 * scale,
                              stroke_color=COL_KINASE, stroke_width=2.5, fill_color=COL_KINASE,
                              fill_opacity=0.22).move_to(pos)
    hinge = kinase.get_left() + RIGHT * 0.12 * scale + UP * 0.24 * scale
    ferm_closed = RoundedRectangle(corner_radius=0.10, width=0.88 * scale, height=0.34 * scale,
                                   stroke_color=COL_KINASE, stroke_width=2.5, fill_color=COL_KINASE,
                                   fill_opacity=0.45)
    ferm_closed.move_to(pos + UP * 0.30 * scale + RIGHT * 0.08 * scale)
    ferm_closed.rotate(open_t * 1.45, about_point=hinge)
    dot_hinge = Dot(hinge, radius=0.055 * scale, color=TEXT)
    g.add(kinase, ferm_closed, dot_hinge)
    g.kinase = kinase
    g.ferm = ferm_closed
    return g


def build_talin_rod_bundles(p_bot, p_top, stretch_t, show_pockets=True):
    """Segmented talin rod between p_bot and p_top; unfolds from zig-zag bundles as stretch_t rises."""
    p0 = np.array(p_bot, dtype=float)
    p1 = np.array(p_top, dtype=float)
    vec = p1 - p0
    L = max(float(np.linalg.norm(vec)), 0.1)
    u = vec / L
    n = np.array([-u[1], u[0], 0.0])

    amp = 0.26 * (1.0 - 0.78 * stretch_t)
    pts = [p0]
    pockets = VGroup()
    n_seg = 3
    for i in range(n_seg):
        f_a = (i + 0.25) / n_seg
        f_m = (i + 0.50) / n_seg
        f_b = (i + 0.75) / n_seg
        sign = 1 if i % 2 == 0 else -1
        c_mid = p0 + vec * f_m
        pts.append(p0 + vec * f_a + sign * amp * n)
        pts.append(p0 + vec * f_b - sign * amp * n)
        if show_pockets and stretch_t > 0.55:
            alpha = float(np.clip((stretch_t - 0.55) / 0.35, 0.0, 1.0))
            pkt = RoundedRectangle(corner_radius=0.06, width=0.26, height=0.16,
                                   stroke_color="#FFE066", stroke_width=2.5,
                                   fill_color="#FFE066", fill_opacity=0.85 * alpha).move_to(c_mid)
            pkt.rotate(np.arctan2(u[1], u[0]) - PI / 2)
            pockets.add(pkt)
    pts.append(p1)

    rod = VMobject(color=COL_TALIN, stroke_width=8)
    rod.set_points_as_corners(pts)
    g = VGroup(rod, pockets)
    g.pockets = pockets
    return g


def build_vinculin_clip(pos, color=COL_VINCULIN):
    """Magenta C-clamp clip that bridges talin pocket to actin."""
    outer = Arc(radius=0.22, start_angle=PI * 0.25, angle=PI * 1.5, color=color, stroke_width=7).move_to(pos)
    return VGroup(outer)


def make_fibrinogen_stream(n_bars=12, seed=7, y_range=(-2.35, -1.25)):
    """Deterministic fibrinogen stream constrained to y_range and wrapped cleanly inside [-6.0, 6.0]."""
    rng = np.random.default_rng(seed)
    fib_group = VGroup()
    for i in range(n_bars):
        x0 = -5.6 + i * (11.2 / n_bars) + float(rng.uniform(-0.14, 0.14))
        y0 = float(rng.uniform(y_range[0], y_range[1]))
        spd = float(rng.uniform(1.15, 1.55))
        rod = RoundedRectangle(corner_radius=0.07, width=0.78, height=0.19,
                               stroke_color=COL_LIGAND, stroke_width=2,
                               fill_color=COL_LIGAND, fill_opacity=0.90).move_to([x0, y0, 0])
        rod.vx = spd
        rod.base_y = y0

        def make_upd():
            def upd(mob, dt):
                mob.shift(RIGHT * mob.vx * dt)
                if mob.get_x() > 6.0:
                    mob.set_x(-6.0)
                dx = mob.get_x() - 0.45
                if abs(dx) < 0.75 and abs(mob.get_y() - (-0.80)) < 0.50:
                    mob.shift(DOWN * 0.50 * dt)
                else:
                    mob.shift(UP * (mob.base_y - mob.get_y()) * 1.5 * dt)
            return upd

        rod.add_updater(make_upd())
        fib_group.add(rod)
    return fib_group


# ------------------------------------------------------------------ Scenes
class S00Title(TitleCard):
    LESSON = "Integrins and Rho GTPases"
    TITLE = "A Grip That Signals and Feels Force"


class S01Hook(SpokenScene):
    def construct(self):
        wall = build_matrix(handles_x=(-3.2, -1.6, 0.0, 1.6, 3.2), label=True, label_text="vessel wall", label_x=-4.9)

        flow_x = ValueTracker(0.0)
        flow_lines = always_redraw(lambda: VGroup(*[
            Arrow([-5.8 + (flow_x.get_value() % 1.4), fy, 0],
                  [-3.1 + (flow_x.get_value() % 1.4), fy, 0],
                  color=COL_MEMB, stroke_width=3.5, tip_length=0.22,
                  max_stroke_width_to_length_ratio=1.0).set_opacity(0.75)
            for fy in (0.65, 1.15, 1.65, 2.15)
        ]))
        flow_lab = T("blood flow", 26, COL_MEMB).move_to([-4.6, 2.65, 0])

        cell_x = ValueTracker(-4.6)

        def mk_wbc():
            x = cell_x.get_value()
            squash = float(np.clip((x + 1.5) / 2.0, 0.0, 1.0)) * 0.14
            body = Ellipse(width=2.1 + squash, height=1.9 - squash, stroke_color=COL_MEMB,
                           stroke_width=4.5, fill_color=COL_MEMB, fill_opacity=0.22).move_to([x, -0.95 - squash * 0.4, 0])
            nuc = Ellipse(width=0.95, height=0.68, stroke_color=COL_ACTIN, stroke_width=2.5,
                          fill_color=COL_ACTIN, fill_opacity=0.14).move_to(body.get_center() + UP * 0.15)
            pegs = VGroup()
            for dx in (-0.35, 0.0, 0.35):
                b = body.get_bottom() + np.array([dx, 0.06, 0])
                pegs.add(Line(b, b + DOWN * 0.25, color=COL_ALPHA, stroke_width=5))
            return VGroup(body, nuc, pegs)

        wbc = always_redraw(mk_wbc)
        wbc_lab = always_redraw(lambda: T("white blood cell", 28, TEXT).move_to(
            [np.clip(cell_x.get_value(), -4.5, 4.5), 0.50, 0]))

        self.add(wall, flow_lines, flow_lab, wbc, wbc_lab)
        self.play(
            cell_x.animate.set_value(-0.9),
            flow_x.animate.set_value(2.8),
            run_time=self.t_of("can stop on a") - 0.2,
            rate_func=linear,
        )
        self.at("can stop on a")
        self.play(
            cell_x.animate.set_value(0.0),
            flow_x.animate.set_value(4.5),
            run_time=1.3,
            rate_func=rush_from,
        )
        self.play(flow_x.animate.set_value(6.5), run_time=max(0.2, self.t_of("Its gripping receptor") - 0.2 - self.elapsed()), rate_func=linear)

        self.at("Its gripping receptor")
        matrix = build_matrix(handles_x=(-3.2, -1.6, 0.0, 1.6, 3.2), label=True)
        memb = build_membrane()
        actin = build_actin()
        open_t = ValueTracker(0.85)
        integ = always_redraw(lambda: make_integrin(xc=0.0, y_memb=Y_MEMB, bend_t=0.0, open_t=open_t.get_value(), sep_t=0.4))

        self.play(
            FadeOut(wbc), FadeOut(wbc_lab), FadeOut(flow_lines), FadeOut(flow_lab), FadeOut(wall),
            run_time=0.4,
        )
        self.play(
            FadeIn(matrix), FadeIn(memb), FadeIn(actin), FadeIn(integ),
            run_time=0.7,
        )

        self.at("has no enzyme")
        q_badge = boxed_label("no enzyme ?", COL_LIGAND, size=28).move_to([2.4, 0.95, 0])
        self.play(FadeIn(q_badge), open_t.animate.set_value(0.42), run_time=1.0)

        self.at("how does it switch on fast")
        arr_in = Arrow([0.65, 1.3, 0], [0.65, -1.35, 0], color=COL_LIGAND, stroke_width=6, tip_length=0.24)
        self.play(Create(arr_in), run_time=1.6)

        self.at("send signals inside")
        arr_out = Arrow([-0.65, -1.35, 0], [-0.65, 1.55, 0], color=COL_KINASE, stroke_width=6, tip_length=0.24)
        self.play(Create(arr_out), open_t.animate.set_value(0.75), run_time=2.0)
        self.finish()


class S02Structure(SpokenScene):
    def construct(self):
        matrix = build_matrix(handles_x=(-3.2, -1.6, 0.0, 1.6, 3.2), label=True)
        memb = build_membrane()
        actin = build_actin()
        tag = scope_tag("schematic")

        sep_t = ValueTracker(0.35)
        open_t = ValueTracker(0.85)
        bend_t = ValueTracker(0.0)
        integ = always_redraw(lambda: make_integrin(
            xc=0.0, y_memb=Y_MEMB, bend_t=bend_t.get_value(), open_t=open_t.get_value(), sep_t=sep_t.get_value()
        ))
        self.add(matrix, memb, actin, integ, tag)

        self.play(open_t.animate.set_value(0.45), run_time=1.4)
        self.at("is an integrin")
        title_chip = boxed_label("integrin", TEXT, size=30).move_to([0.0, 1.65, 0])
        self.play(FadeIn(title_chip), sep_t.animate.set_value(0.55), run_time=2.4)

        self.at("two different chains")
        # Raised to y = -0.68 so 'other cell protein' at -1.35 has huge clearance
        lab_a = T("α chain", 30, COL_ALPHA, weight=BOLD).move_to([-2.35, -0.68, 0])
        lab_b = T("β chain", 30, COL_BETA, weight=BOLD).move_to([2.35, -0.68, 0])
        arr_a = Arrow([-1.40, -0.68, 0], [-0.55, -0.68, 0], color=COL_ALPHA, stroke_width=3.5, tip_length=0.18)
        arr_b = Arrow([1.40, -0.68, 0], [0.55, -0.68, 0], color=COL_BETA, stroke_width=3.5, tip_length=0.18)
        self.play(
            sep_t.animate.set_value(0.85),
            FadeIn(lab_a), FadeIn(lab_b), Create(arr_a), Create(arr_b),
            run_time=2.4,
        )

        self.at("each crossing the membrane")
        tm_hi_a = RoundedRectangle(corner_radius=0.08, width=0.28, height=0.66, stroke_color=COL_PHOS,
                                   stroke_width=3.5).move_to([-0.34, 0.0, 0])
        tm_hi_b = RoundedRectangle(corner_radius=0.08, width=0.28, height=0.66, stroke_color=COL_PHOS,
                                   stroke_width=3.5).move_to([0.34, 0.0, 0])
        tm_lab = T("1× transmembrane", 26, TEXT).move_to([2.85, 0.58, 0])
        self.play(Create(tm_hi_a), Create(tm_hi_b), FadeIn(tm_lab), run_time=2.6)

        self.at("Outside")
        self.play(
            FadeOut(tm_hi_a), FadeOut(tm_hi_b), FadeOut(tm_lab),
            sep_t.animate.set_value(0.65), bend_t.animate.set_value(0.35),
            run_time=1.6,
        )

        self.at("grips the matrix")
        rgd_lab = T("RGD handle", 26, COL_LIGAND).move_to([3.05, -1.36, 0])
        rgd_arr = Arrow([2.35, -1.52, 0], [1.72, -1.85, 0], color=COL_LIGAND, stroke_width=3, tip_length=0.18, buff=0.06)
        self.play(bend_t.animate.set_value(0.0), open_t.animate.set_value(0.38), FadeIn(rgd_lab), Create(rgd_arr), run_time=3.0)

        self.at("proteins on other cells")
        other_chip = boxed_label("other cell protein", COL_LIGAND, size=24).move_to([-4.35, -1.35, 0])
        self.play(FadeIn(other_chip, shift=RIGHT * 0.5), run_time=1.2)
        self.play(FadeOut(other_chip, shift=LEFT * 0.5), run_time=1.1)

        self.at("Inside two short tails")
        tails_lab = T("short tails", 30, TEXT, weight=BOLD).move_to([-2.7, 1.05, 0])
        tails_arr = Arrow([-1.65, 0.92, 0], [-0.45, 0.60, 0], color=TEXT, stroke_width=3, tip_length=0.18)
        tail_box = RoundedRectangle(corner_radius=0.10, width=1.15, height=0.58, stroke_color=TEXT, stroke_width=3).move_to([0.0, 0.54, 0])
        self.play(FadeIn(tails_lab), Create(tails_arr), Create(tail_box), sep_t.animate.set_value(0.82), run_time=2.4)

        self.at("no kinase and no channel")
        no_enz = boxed_label("no enzyme", COL_BETA, size=28).move_to([3.0, 1.05, 0])
        self.play(FadeIn(no_enz), FadeOut(tail_box), sep_t.animate.set_value(0.65), run_time=0.8)
        self.finish()


class S03Predict(SpokenScene):
    def construct(self):
        memb = build_membrane()
        actin = build_actin(y_base=1.65, label_at=(-5.2, 2.08, 0))

        hr_cup = Arc(radius=0.35, start_angle=PI, angle=PI, color=GREY, stroke_width=6).move_to([-4.0, -0.35, 0])
        hr_stem = Line([-4.0, 0.35, 0], [-4.0, -0.35, 0], color=GREY, stroke_width=8)
        hr_lab = T("hormone receptor", 26, GREY).move_to([-4.0, 0.72, 0])
        sol_lig = VGroup(
            RoundedRectangle(corner_radius=0.10, width=0.55, height=0.28, stroke_color=COL_LIGAND,
                             stroke_width=2.5, fill_color=COL_LIGAND, fill_opacity=0.85),
        ).move_to([-4.0, -2.75, 0])
        sol_ring = Circle(radius=0.38, color=COL_LIGAND, stroke_width=3).move_to([-4.0, -2.75, 0])

        bend_t = ValueTracker(0.0)
        open_t = ValueTracker(0.75)
        integ = always_redraw(lambda: make_integrin(
            xc=0.4, y_memb=Y_MEMB, bend_t=bend_t.get_value(), open_t=open_t.get_value(), sep_t=0.25
        ))

        self.add(memb, actin, hr_stem, hr_cup, hr_lab, sol_lig, sol_ring, integ)
        self.play(
            sol_lig.animate.move_to([-4.0, -1.25, 0]),
            sol_ring.animate.move_to([-4.0, -1.25, 0]),
            run_time=self.t_of("soluble ligand arrives") - 0.2,
            rate_func=linear,
        )
        self.at("soluble ligand arrives")
        hr_sig = Arrow([-3.55, -0.30, 0], [-3.55, 0.55, 0], color=COL_LIGAND, stroke_width=4, tip_length=0.18)
        self.play(
            sol_lig.animate.move_to([-4.0, -0.58, 0]),
            FadeOut(sol_ring),
            Create(hr_sig),
            run_time=2.8,
            rate_func=smooth,
        )

        self.at("are bathed in ligand")
        fib_group = make_fibrinogen_stream(n_bars=12, seed=7)
        fib_lab = T("fibrinogen", 28, COL_LIGAND).move_to([-4.2, -2.85, 0])
        fib_sample = RoundedRectangle(corner_radius=0.07, width=0.68, height=0.18,
                                      stroke_color=COL_LIGAND, stroke_width=2,
                                      fill_color=COL_LIGAND, fill_opacity=0.90).next_to(fib_lab, RIGHT, buff=0.22)

        self.play(
            FadeOut(hr_cup), FadeOut(hr_stem), FadeOut(hr_lab), FadeOut(sol_lig), FadeOut(hr_sig),
            FadeIn(fib_group), FadeIn(fib_lab), FadeIn(fib_sample),
            run_time=2.6,
        )

        self.at("Think of a platelet")

        self.at("Why does that platelet")
        q = question_card("Platelets float in fibrinogen. Why do they not clump right away?", y=3.05, size=29)
        self.play(FadeIn(q), run_time=0.8)
        self.finish()


class S04Pause(PredictPause):
    QUESTION = "Platelets float in fibrinogen. Why do they not clump right away?"
    CARD = {"y": 3.05, "size": 29}
    RING_AT = (6.0, -3.0, 0)
    SECONDS = 4.5

    def backdrop(self):
        memb = build_membrane()
        actin = build_actin(y_base=1.65, label_at=(-5.2, 2.08, 0))
        integ = make_integrin(xc=0.4, y_memb=Y_MEMB, bend_t=0.0, open_t=0.75, sep_t=0.25)
        fib_group = make_fibrinogen_stream(n_bars=12, seed=7)
        fib_lab = T("fibrinogen", 28, COL_LIGAND).move_to([-4.2, -2.85, 0])
        fib_sample = RoundedRectangle(corner_radius=0.07, width=0.68, height=0.18,
                                      stroke_color=COL_LIGAND, stroke_width=2,
                                      fill_color=COL_LIGAND, fill_opacity=0.90).next_to(fib_lab, RIGHT, buff=0.22)
        return VGroup(memb, actin, integ, fib_group, fib_lab, fib_sample)


class S05InsideOut(SpokenScene):
    def construct(self):
        memb = build_membrane()
        actin = build_actin(y_base=1.65, label_at=(-5.2, 2.08, 0))
        q = question_card("Platelets float in fibrinogen. Why do they not clump right away?", y=3.05, size=29)
        matrix = build_matrix(handles_x=(-3.2, -1.6, 0.0, 1.6, 3.2), label=True)

        bend_t = ValueTracker(0.0)
        open_t = ValueTracker(0.75)
        sep_t = ValueTracker(0.0)
        integ = always_redraw(lambda: make_integrin(
            xc=0.0, y_memb=Y_MEMB, bend_t=bend_t.get_value(),
            open_t=open_t.get_value(), sep_t=sep_t.get_value()
        ))

        self.add(memb, actin, integ, q)
        self.play(FadeOut(q), run_time=0.6)
        self.play(actin.animate.shift(UP * 0.80), FadeIn(matrix, shift=UP * 0.4), run_time=2.8)

        # Continuous ligand bars passing and deflecting off head through 12s
        probes = make_fibrinogen_stream(n_bars=5, seed=11, y_range=(-1.60, -0.95))
        self.add(probes)

        self.at("outer legs fold at a knee")
        knee_ring = Circle(radius=0.22, color=COL_PHOS, stroke_width=4).move_to([-0.15, -1.00, 0])
        knee_lab = T("folded knee", 28, COL_PHOS).move_to([-2.4, -1.00, 0])
        knee_arr = Arrow([-1.35, -1.00, 0], [-0.42, -1.00, 0], color=COL_PHOS, stroke_width=3, tip_length=0.18)
        self.play(
            Create(knee_ring), FadeIn(knee_lab), Create(knee_arr),
            bend_t.animate.set_value(1.0), open_t.animate.set_value(0.0),
            run_time=2.4,
        )

        self.at("Bent with the head closed")
        weak_lab = T("weak grip", 28, GREY).move_to([2.6, -0.72, 0])
        self.play(FadeIn(weak_lab), run_time=2.4)

        self.at("An inside signal")
        talin = boxed_label("talin", COL_TALIN, size=26).move_to([1.95, 1.85, 0])
        kindlin = boxed_label("kindlin", COL_KINDLIN, size=24).move_to([3.35, 1.85, 0])
        self.play(
            FadeOut(probes),
            FadeOut(knee_ring), FadeOut(knee_lab), FadeOut(knee_arr), FadeOut(weak_lab),
            FadeIn(talin), FadeIn(kindlin),
            run_time=1.4,
        )

        self.at("to the beta tail")
        self.play(
            talin.animate.move_to([0.92, 0.72, 0]),
            kindlin.animate.move_to([2.25, 0.72, 0]),
            run_time=1.4,
        )

        self.at("the two tails separate")
        sep_lab = T("tails separate", 28, TEXT).move_to([-2.4, 0.78, 0])
        self.play(
            sep_t.animate.set_value(1.0),
            talin.animate.shift(RIGHT * 0.24),
            kindlin.animate.shift(RIGHT * 0.24),
            FadeIn(sep_lab),
            run_time=2.5,
        )

        self.at("passes through the membrane")
        wave_y = ValueTracker(0.55)
        wave = always_redraw(lambda: RoundedRectangle(
            corner_radius=0.12, width=1.15, height=0.24,
            stroke_color=COL_TALIN, stroke_width=5
        ).move_to([0.0, wave_y.get_value(), 0]))
        self.add(wave)
        self.play(wave_y.animate.set_value(-0.95), run_time=1.7, rate_func=linear)
        self.remove(wave)

        self.at("the legs straighten")
        self.play(bend_t.animate.set_value(0.0), run_time=1.3, rate_func=smooth)

        self.at("the head opens tight")
        firm_lab = T("tight grip", 28, COL_LIGAND, weight=BOLD).move_to([2.4, -1.55, 0])
        self.play(open_t.animate.set_value(1.0), FadeIn(firm_lab), run_time=1.2)
        self.finish()


class S06InsideOutPayoff(SpokenScene):
    def construct(self):
        matrix = build_matrix(handles_x=(-3.2, -1.6, 0.0, 1.6, 3.2), label=True)
        memb = build_membrane()
        actin = build_actin()

        c_integ = make_integrin(xc=0.0, y_memb=Y_MEMB, bend_t=0.0, open_t=1.0, sep_t=1.0)
        c_talin = boxed_label("talin", COL_TALIN, size=24).move_to([0.55, 1.12, 0])
        c_kindlin = boxed_label("kindlin", COL_KINDLIN, size=24).move_to([1.95, 1.12, 0])

        lx_t = ValueTracker(-3.6)
        lb_t = ValueTracker(1.0)
        lo_t = ValueTracker(0.0)
        ls_t = ValueTracker(0.0)

        rx_t = ValueTracker(3.6)
        rb_t = ValueTracker(1.0)
        ro_t = ValueTracker(0.0)
        rs_t = ValueTracker(0.0)

        l_integ = always_redraw(lambda: make_integrin(
            xc=lx_t.get_value(), y_memb=Y_MEMB, bend_t=lb_t.get_value(),
            open_t=lo_t.get_value(), sep_t=ls_t.get_value()
        ))
        r_integ = always_redraw(lambda: make_integrin(
            xc=rx_t.get_value(), y_memb=Y_MEMB, bend_t=rb_t.get_value(),
            open_t=ro_t.get_value(), sep_t=rs_t.get_value()
        ))

        self.add(matrix, memb, actin, c_integ, c_talin, c_kindlin, l_integ, r_integ)

        ready_ring = Circle(radius=0.60, color=COL_ALPHA, stroke_width=4).move_to([-3.6, -0.65, 0])
        self.play(Create(ready_ring), run_time=0.8)
        self.play(ready_ring.animate.move_to([3.6, -0.65, 0]), run_time=2.6, rate_func=smooth)
        self.play(FadeOut(ready_ring), run_time=0.4)

        self.at("grab hold fast")
        fast_tag = boxed_label("ready on surface — no new protein", TEXT, size=24).move_to([0.0, 1.96, 0])
        self.play(FadeIn(fast_tag), run_time=2.2)

        self.at("starts in the cytoplasm")
        io_arrow = Arrow([-1.35, 1.35, 0], [-1.35, -1.65, 0], color=COL_TALIN, stroke_width=7, tip_length=0.28)
        io_lab = boxed_label("inside-out", COL_TALIN, size=28).move_to([-3.15, 1.55, 0])
        self.play(FadeOut(fast_tag), run_time=0.4)
        self.play(Create(io_arrow), FadeIn(io_lab), run_time=1.0)

        self.at("changes grip outside")
        grip_ring = Circle(radius=0.45, color=COL_LIGAND, stroke_width=5).move_to([0.0, -1.93, 0])
        sig_wave = RoundedRectangle(corner_radius=0.10, width=0.80, height=0.26,
                                    stroke_color=COL_TALIN, stroke_width=5).move_to([-1.35, 1.25, 0])
        self.add(sig_wave)
        self.play(
            sig_wave.animate.move_to([-1.35, -1.55, 0]),
            Create(grip_ring),
            lx_t.animate.set_value(-3.1), rx_t.animate.set_value(3.1),
            run_time=3.8, rate_func=linear,
        )
        self.remove(sig_wave)

        self.at("Once bound integrins cluster")
        l_talin = boxed_label("talin", COL_TALIN, size=22).move_to([-1.22, 1.12, 0])
        r_talin = boxed_label("talin", COL_TALIN, size=22).move_to([1.98, 1.12, 0])
        self.play(
            FadeOut(io_arrow), FadeOut(io_lab),
            FadeOut(grip_ring), FadeOut(c_kindlin),
            c_talin.animate.move_to([0.38, 1.12, 0]),
            lb_t.animate.set_value(0.0), ls_t.animate.set_value(1.0), lo_t.animate.set_value(1.0),
            rb_t.animate.set_value(0.0), rs_t.animate.set_value(1.0), ro_t.animate.set_value(1.0),
            lx_t.animate.set_value(-1.6), rx_t.animate.set_value(1.6),
            run_time=2.6,
        )
        self.play(FadeIn(l_talin), FadeIn(r_talin), run_time=0.6)

        self.at("the message reverses")
        oi_arrow = Arrow([3.1, -1.65, 0], [3.1, 1.45, 0], color=COL_KINASE, stroke_width=7, tip_length=0.28)
        oi_lab = boxed_label("outside-in", COL_KINASE, size=28).move_to([4.75, 1.15, 0])
        up_wave = RoundedRectangle(corner_radius=0.10, width=0.80, height=0.26,
                                   stroke_color=COL_KINASE, stroke_width=5).move_to([3.1, -1.45, 0])
        self.play(Create(oi_arrow), FadeIn(oi_lab), run_time=1.0)
        self.add(up_wave)
        self.play(up_wave.animate.move_to([3.1, 1.30, 0]), run_time=2.1, rate_func=linear)
        self.remove(up_wave)
        self.finish()


class S07FocalAdhesion(SpokenScene):
    def construct(self):
        matrix = build_matrix(handles_x=(-4.0, -2.4, -0.8, 0.8, 2.4, 4.0), label=True)
        memb = build_membrane()
        actin = build_actin()
        tag = scope_tag("schematic")

        clusters = VGroup(*[
            make_integrin(xc=x, y_memb=Y_MEMB, bend_t=0.0, open_t=1.0, sep_t=1.0)
            for x in (-2.4, -0.8, 0.8)
        ])
        self.add(matrix, memb, actin, clusters, tag)

        self.at("assemble a focal adhesion")
        fa_head = boxed_label("focal adhesion", TEXT, size=28).move_to([-4.6, 1.85, 0])
        tail_scan = RoundedRectangle(corner_radius=0.12, width=4.0, height=0.68,
                                     stroke_color=COL_TALIN, stroke_width=4).move_to([-0.4, 0.56, 0])
        self.play(FadeIn(fa_head), Create(tail_scan), run_time=2.6)
        self.play(tail_scan.animate.set_stroke(opacity=0.2), run_time=1.4)
        self.remove(tail_scan)

        self.at("links the")
        talin_t = ValueTracker(0.0)
        rods = always_redraw(lambda: VGroup(*[
            Line(
                [bx, 0.72, 0],
                [bx, 0.72 + talin_t.get_value() * (Y_ACTIN - 0.72), 0],
                color=COL_TALIN, stroke_width=10,
            )
            for bx in (-2.02, -0.42)
        ]))
        talin_lab = T("talin", 28, COL_TALIN, weight=BOLD).move_to([-3.2, 1.20, 0])
        self.add(rods)
        self.play(talin_t.animate.set_value(1.0), FadeIn(talin_lab), run_time=2.5)

        self.at("forms a docking scaffold")
        pax = RoundedRectangle(corner_radius=0.12, width=2.45, height=0.56, stroke_color=COL_PAXILLIN,
                               stroke_width=3.5, fill_color=COL_PAXILLIN, fill_opacity=0.24).move_to([4.45, 0.78, 0])
        pax_lab = T("paxillin", 26, COL_PAXILLIN, weight=BOLD).move_to(pax)
        pax_g = VGroup(pax, pax_lab).shift(RIGHT * 1.4)
        self.play(pax_g.animate.shift(LEFT * 1.4), run_time=2.8)

        self.at("borrows focal adhesion kinase")
        fak_open = ValueTracker(0.0)
        fak_x = ValueTracker(5.3)
        fak_y = ValueTracker(1.95)
        fak_mob = always_redraw(lambda: build_fak([fak_x.get_value(), fak_y.get_value(), 0], open_t=fak_open.get_value(), scale=0.90))
        fak_lab = always_redraw(lambda: T("FAK", 26, COL_KINASE, weight=BOLD).move_to(
            [fak_x.get_value(), fak_y.get_value() - 0.48, 0]
        ))
        self.add(fak_mob, fak_lab)
        self.play(fak_x.animate.set_value(2.25), run_time=1.6)
        self.play(fak_y.animate.set_value(1.05), run_time=1.6)

        self.at("Folded shut at rest")
        self.play(fak_open.animate.set_value(0.10), run_time=0.6)
        self.play(fak_open.animate.set_value(0.0), run_time=0.6)

        self.at("it opens")
        self.play(fak_open.animate.set_value(1.0), run_time=1.0)

        self.at("phosphorylates one of its own")
        p_tyr = build_phosphate([2.35, 1.55, 0], radius=0.17)
        tyr_lab = T("Tyr397", 24, COL_PHOS, weight=BOLD).move_to([2.82, 2.16, 0])
        tyr_arr = Arrow([2.64, 2.00, 0], [2.44, 1.78, 0], color=COL_PHOS, stroke_width=3, tip_length=0.15, buff=0.04)
        flash_ring = Circle(radius=0.35, color=COL_PHOS, stroke_width=4).move_to([2.35, 1.55, 0])
        self.play(FadeIn(p_tyr, scale=1.5), FadeIn(tyr_lab), Create(tyr_arr), Create(flash_ring), run_time=2.0)
        self.play(FadeOut(flash_ring), run_time=0.6)

        self.at("That phosphate docks")
        src_g = boxed_label("Src", COL_KINASE, size=26).move_to([5.3, 1.60, 0])
        self.play(FadeIn(src_g), run_time=0.6)
        self.play(src_g.animate.move_to([3.20, 1.56, 0]), run_time=2.6)

        self.at("the pair phosphorylates")
        p1 = build_phosphate([2.98, 0.95, 0], radius=0.14)
        p2 = build_phosphate([4.05, 1.34, 0], radius=0.14)
        p3 = build_phosphate([5.05, 1.34, 0], radius=0.14)
        self.play(FadeIn(p1, scale=1.4), run_time=0.4)
        self.play(FadeIn(p2, scale=1.4), FadeIn(p3, scale=1.4), run_time=0.6)
        self.finish()


class S08Mechanosensing(SpokenScene):
    def construct(self):
        matrix = build_matrix(handles_x=(-3.8, -2.2, -0.6, 1.0, 2.6), label=True)
        memb = build_membrane()
        tag = scope_tag("schematic")

        hero_x = -0.6
        integ = make_integrin(xc=hero_x, y_memb=Y_MEMB, bend_t=0.0, open_t=1.0, sep_t=1.0)
        tail_pt = integ.beta_chain.tail_top

        pull_t = ValueTracker(0.0)
        head_phase = ValueTracker(0.0)

        actin = always_redraw(lambda: build_actin(
            y_base=Y_ACTIN, x0=-5.55, x1=3.0, label=True, label_at=(1.6, 2.95, 0)
        ).shift(LEFT * (1.0 * pull_t.get_value())))

        talin_rod = always_redraw(lambda: build_talin_rod_bundles(
            tail_pt,
            [tail_pt[0] - 1.0 * pull_t.get_value(), Y_ACTIN, 0],
            stretch_t=pull_t.get_value(),
            show_pockets=True,
        ))

        g_center = np.array([4.35, 1.15, 0.0])
        g_track = Arc(radius=1.20, start_angle=PI, angle=-PI, arc_center=g_center, stroke_color=GREY, stroke_width=12)
        g_fill = always_redraw(lambda: Arc(
            radius=1.20, start_angle=PI, angle=-PI * max(0.02, pull_t.get_value()),
            arc_center=g_center, stroke_color=COL_MYOSIN, stroke_width=12
        ))
        g_needle = always_redraw(lambda: Line(
            g_center,
            g_center + 0.95 * np.array([np.cos(PI - PI * pull_t.get_value()), np.sin(PI - PI * pull_t.get_value()), 0]),
            color=TEXT, stroke_width=5,
        ))
        g_low = T("low", 22, GREY).move_to(g_center + LEFT * 1.45 + DOWN * 0.24)
        g_high = T("high", 22, COL_MYOSIN).move_to(g_center + RIGHT * 1.45 + DOWN * 0.24)
        g_title = T("tension", 28, TEXT, weight=BOLD).move_to(g_center + DOWN * 0.56)
        gauge = VGroup(g_track, g_fill, g_needle, g_low, g_high, g_title)

        talin_lab = T("talin rod", 28, COL_TALIN, weight=BOLD).move_to([-2.4, 1.35, 0])

        self.add(matrix, memb, actin, integ, talin_rod, talin_lab, gauge, tag)

        # Gentle initial tension test showing adhesion feels pull right away
        self.play(pull_t.animate.set_value(0.22), run_time=1.9, rate_func=smooth)
        self.play(pull_t.animate.set_value(0.0), run_time=1.9, rate_func=smooth)

        self.at("motor protein myosin")
        myosin_box = boxed_label("myosin", COL_MYOSIN, size=26).move_to([-4.6, 1.78, 0])
        top_myo = myosin_box.get_top()[1]
        myosin_heads = always_redraw(lambda: VGroup(
            Line([-4.95, top_myo, 0], [-5.15 - 0.22 * np.sin(head_phase.get_value() * TAU), 2.42, 0],
                 color=COL_MYOSIN, stroke_width=5),
            Line([-4.25, top_myo, 0], [-4.45 + 0.22 * np.sin(head_phase.get_value() * TAU), 2.42, 0],
                 color=COL_MYOSIN, stroke_width=5),
        ))
        pull_arr = Arrow([-3.1, 2.95, 0], [-4.7, 2.95, 0], color=COL_MYOSIN, stroke_width=5, tip_length=0.24)
        self.play(FadeIn(myosin_box), FadeIn(myosin_heads), Create(pull_arr), run_time=1.2)
        self.play(pull_t.animate.set_value(0.32), head_phase.animate.set_value(2.0), run_time=4.8, rate_func=linear)

        self.at("hides binding sites")
        vinc_c1 = build_vinculin_clip([1.7, 1.45, 0])
        vinc_c2 = build_vinculin_clip([2.25, 1.45, 0])
        vinc_lab = T("vinculin", 28, COL_VINCULIN, weight=BOLD).move_to([1.95, 2.15, 0])
        self.play(
            FadeIn(vinc_c1), FadeIn(vinc_c2), FadeIn(vinc_lab),
            pull_t.animate.set_value(0.45), head_phase.animate.set_value(3.5),
            run_time=4.0, rate_func=linear,
        )

        self.at("Tension stretches the rod")
        self.play(pull_t.animate.set_value(1.0), head_phase.animate.set_value(5.0), run_time=2.0, rate_func=smooth)

        self.at("uncovers those buried sites")
        # Placed below at y = 0.70 so it clears vinc_c1 glide path (y = 1.65) and gauge 'low' (x = 2.90)
        pock_lab = fit_text("buried sites\nexposed", max_w=1.8, size=24, color="#FFE066", max_lines=2).move_to([1.15, 0.72, 0])
        pock_arr = Arrow([0.25, 0.85, 0], [-0.30, 1.15, 0], color="#FFE066", stroke_width=3, tip_length=0.16, buff=0.06)
        self.play(FadeIn(pock_lab), Create(pock_arr), head_phase.animate.set_value(5.8), run_time=1.4)

        self.at("Vinculin then clips talin")
        top_pt = np.array([tail_pt[0] - 1.0, Y_ACTIN, 0.0])
        c_mid = tail_pt + (top_pt - tail_pt) * 0.50
        c_top = tail_pt + (top_pt - tail_pt) * 0.83
        bridge_1 = Line(c_mid, top_pt + RIGHT * 0.25, color=COL_VINCULIN, stroke_width=7)
        bridge_2 = Line(c_top, top_pt + LEFT * 0.22, color=COL_VINCULIN, stroke_width=7)
        self.play(
            FadeOut(pock_lab), FadeOut(pock_arr),
            vinc_c1.animate.move_to(c_mid),
            vinc_c2.animate.move_to(c_top),
            vinc_lab.animate.move_to([0.95, 2.20, 0]),
            Create(bridge_1), Create(bridge_2),
            run_time=2.8,
        )
        # Keep motor pulling firmly against the reinforced bridge
        self.play(head_phase.animate.set_value(7.2), run_time=2.4, rate_func=linear)
        self.finish()


class S09Closing(SpokenScene):
    def construct(self):
        matrix = build_matrix(handles_x=(-3.6, 0.0, 3.6), label=True)
        memb = build_membrane()
        actin_shift = ValueTracker(0.0)
        actin = always_redraw(lambda: build_actin(x0=-5.9, x1=5.4).shift(RIGHT * actin_shift.get_value()))

        l_bend = ValueTracker(1.0)
        l_open = ValueTracker(0.0)
        l_sep = ValueTracker(0.0)
        l_integ = always_redraw(lambda: make_integrin(
            xc=-3.6, y_memb=Y_MEMB, bend_t=l_bend.get_value(),
            open_t=l_open.get_value(), sep_t=l_sep.get_value(), scale=0.88
        ))
        c_integ = make_integrin(xc=0.0, y_memb=Y_MEMB, bend_t=0.0, open_t=1.0, sep_t=1.0, scale=0.88)
        r_integ = make_integrin(xc=3.6, y_memb=Y_MEMB, bend_t=0.0, open_t=1.0, sep_t=1.0, scale=0.88)

        # Separated cleanly: c_fak at [0.72, 1.24], pax_g at [1.95, 0.78], Src at [2.15, 1.52]
        pax_g = boxed_label("paxillin", COL_PAXILLIN, size=24).move_to([1.95, 0.78, 0])
        c_fak_open = ValueTracker(0.0)
        c_fak = always_redraw(lambda: build_fak([0.72, 1.24, 0], open_t=c_fak_open.get_value(), scale=0.68))

        r_pull = ValueTracker(0.0)
        r_tail = r_integ.beta_chain.tail_top
        r_talin = always_redraw(lambda: build_talin_rod_bundles(
            r_tail, [r_tail[0] - 0.55 * r_pull.get_value(), Y_ACTIN, 0], stretch_t=r_pull.get_value()
        ))

        self.add(matrix, memb, actin, l_integ, c_integ, r_integ, pax_g, c_fak, r_talin)

        # Preview sweep across all 3 mechanisms
        scan_box = RoundedRectangle(corner_radius=0.14, width=2.2, height=1.7, stroke_color=COL_LIGAND, stroke_width=3.5).move_to([-3.6, -0.95, 0])
        self.play(Create(scan_box), run_time=0.8)
        self.play(scan_box.animate.move_to([3.6, -0.95, 0]), run_time=4.0, rate_func=linear)
        self.play(FadeOut(scan_box), run_time=0.6)

        self.at("Inside cues straighten")
        l_tal = boxed_label("talin", COL_TALIN, size=24).move_to([-2.45, 0.78, 0])
        l_tag = boxed_label("inside-out", COL_TALIN, size=26).move_to([-3.6, 1.85, 0])
        self.play(
            FadeIn(l_tal), FadeIn(l_tag),
            l_sep.animate.set_value(1.0), l_bend.animate.set_value(0.0), l_open.animate.set_value(1.0),
            run_time=4.2,
        )

        self.at("borrows kinases")
        c_tag = boxed_label("outside-in", COL_KINASE, size=26).move_to([-1.10, 2.02, 0])
        p_tyr = build_phosphate([0.82, 1.62, 0], radius=0.14)
        src_b = boxed_label("Src", COL_KINASE, size=24).move_to([2.15, 1.64, 0])
        self.play(c_fak_open.animate.set_value(1.0), FadeIn(c_tag), run_time=0.8)
        self.play(FadeIn(p_tyr), FadeIn(src_b), run_time=0.7)

        self.at("adds extra links under load")
        r_tag = boxed_label("force sensing", COL_VINCULIN, size=24).move_to([5.45, 1.65, 0])
        self.play(r_pull.animate.set_value(1.0), FadeIn(r_tag), run_time=1.4)
        v1 = build_vinculin_clip([r_tail[0] - 0.28, 1.55, 0])
        v2 = build_vinculin_clip([r_tail[0] - 0.45, 2.15, 0])
        self.play(FadeIn(v1), FadeIn(v2), run_time=0.9)

        self.at("Whether other adhesion proteins")
        open_q = T("other proteins?\nopen question", size=22, color=COL_LIGAND, line_spacing=0.8).move_to([1.80, -1.05, 0])
        q_box = RoundedRectangle(corner_radius=0.12, width=2.36, height=0.95, stroke_color=COL_LIGAND, stroke_width=2.5).move_to([1.80, -1.05, 0])
        self.play(FadeIn(open_q), Create(q_box), run_time=3.5)

        self.at("Next actin switches")
        act_arr = Arrow([-2.0, 2.92, 0], [1.3, 2.92, 0], color=COL_ACTIN, stroke_width=6, tip_length=0.25)
        act_next = T("actin switches -> movement", 26, TEXT).move_to([3.95, 2.92, 0])
        self.play(FadeOut(open_q), FadeOut(q_box), Create(act_arr), FadeIn(act_next), actin_shift.animate.set_value(0.85), run_time=3.4)
        self.finish()


class S10End(EndCard):
    LINE = "Integrin grip switches from inside, and focal adhesions signal and sense force."
