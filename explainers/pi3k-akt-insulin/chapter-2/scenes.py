"""
COLOUR MAP (one colour per concept for the whole film)
- AMBER          (#F59E0B): insulin and insulin receptor (and growth-factor receptor)
- IRS_TEAL       (#2DD4BF): IRS-1 docking protein
- PI3K_BLUE      (#38BDF8): PI 3-kinase
- PIP2_SLATE     (#64748B): PIP2 lipid tiles
- PIP3_GOLD      (#FACC15): PIP3 lipid patch / tiles
- AKT_CORAL      (#F43F5E): active Akt (AKT_MUTED #9A4858 when inactive/detached)
- PHOS_YELLOW    (#FEF08A): 'P' phosphorylation badges (dark BG text on yellow-white fill)
- PTEN_MINT      (#34D399): PTEN and tyrosine phosphatases (erasers)
- TARGET_INDIGO  (#818CF8): resting inhibitory targets AS160, GSK3, FOXO1 (TARGET_OFF #94A3B8 when switched off)
- GLUT_EMERALD   (#10B981): GLUT4 channels, glucose dots, glycogen synthase and glycogen chains
- SER_FEEDBACK   (#D99B52): Ser-P negative feedback tags and feedback arc
- INHIB_RED      (#EF4444): inhibitory marks on GSK3-stalled glycogen synthase and mutant AS160 X

ONE CARRIED WORLD
A schematic cell-edge cross-section (plasma membrane bilayer at top when at the membrane,
zooming cleanly into the Muscle & fat zone, Glycogen zone, and Liver nucleus in the cytosol,
returning to the membrane cross-section for erasers/feedback, zooming back to Muscle & fat for
the AS160 mutant prediction, splitting into Stuck-on vs Turned-down membrane halves, and merging
back to one balanced membrane cross-section).

WHAT CHANGES IN EACH SCENE (computed / process-driven)
- s00_title: Standard TitleCard.
- s01_hook: PI 3-kinase converts slate PIP2 tiles to gold PIP3; Akt docks and gains two 'P' badges;
  three signal arrows fan downward to Muscle & fat, Glycogen, and Liver nucleus while a signal-load
  bar rises until PTEN and a feedback arc cap it.
- s02_glut4_as160: Active Akt stamps 'P' on indigo AS160, turning it grey and releasing 4 tethered
  GLUT4 vesicles; vesicles glide up and fuse into the membrane, opening GLUT4 channels through which
  seeded glucose dots (rng 7) stream continuously into the cytosol.
- s03_gsk3_glycogen: Indigo GSK3 holds emerald glycogen synthase stalled with red inhibitory marks
  and a live schematic synthase-rate gauge drops to slow; Akt stamps 'P' on GSK3, which greys and
  drifts off; marks clear, rate gauge rises to fast, and glycogen synthase builds a computed
  22-bead branched glycogen tree bead by bead.
- s04_foxo1_liver: FOXO1 sits on DNA inside the liver nucleus driving continuous gluconeogenic gene
  transcription pulses; Akt enters via the nuclear pore, stamps 'P', 14-3-3 clasps FOXO1 and exports
  it to the cytosol, and gene-transcription arrows and output dim over a live hours sweep.
- s05_guiding_rule: Three side-by-side tissue columns animate each outcome (AS160 off -> GLUT4 up,
  GSK3 off -> glycogen up, FOXO1 out -> liver genes down), reveal the Brake-off vs Driver-off
  summaries and guiding rule as spoken, and pull back up to the plasma membrane cross-section.
- s06_erasers_feedback: Tyrosine phosphatase strips receptor/IRS-1 phosphates and releases PI 3-kinase;
  mint-green PTEN sweeps the gold PIP3 patch back to slate PIP2; Akt detaches, sheds both 'P'
  badges, and dims to muted coral; feedback arc stamps Ser-P tags onto IRS-1 and PI 3-kinase fails
  to dock ('Ser-P IRS-1 ✕ PI3K').
- s07_predict_q: Muscle & fat zone returns with an X-marked 'AS160 mutant' blocking Akt's 'P' stamp;
  vesicles stay tethered below active Akt on PIP3 while the predict question appears.
- s08_pause: Deliberate 4.5 s PredictPause holding S07's exact state with the countdown ring.
- s09_predict_reveal: Only 1 of 5 vesicles bypasses mutant AS160 (slow glucose trickle, 'Uptake rises
  less'); 'push the whole relay both ways' splits into TwoPanel: Stuck on (cancer) with abundant
  PIP3/Akt and 'Growth factors: survival, growth' vs Turned down (insulin resistance) with Ser-P
  feedback, sparse PIP3, and 'Excess nutrients, inflammation → more serine feedback'.
- s10_closing: Merges to a single balanced membrane driven by an ODE PIP3 kinetic model (dp/dt):
  normal balance -> PTEN loss surge -> feedback drop -> steady healthy oscillation of PIP3 and Akt.
- s11_end: Standard EndCard with the exact take-home line.
"""

from bp_parts import *

# ---------------------------------------------------------------------------
# Concept colour palette (one colour per concept)
# ---------------------------------------------------------------------------
AMBER = "#F59E0B"        # insulin + receptor
IRS_TEAL = "#2DD4BF"     # IRS-1
PI3K_BLUE = "#38BDF8"    # PI 3-kinase
PIP2_SLATE = "#64748B"   # PIP2
PIP3_GOLD = "#FACC15"    # PIP3
AKT_CORAL = "#F43F5E"    # active Akt
AKT_MUTED = "#9A4858"    # inactive / cytosolic Akt
PHOS_YELLOW = "#FEF08A"  # 'P' badge fill
PTEN_MINT = "#34D399"    # PTEN / tyrosine phosphatases
TARGET_INDIGO = "#818CF8"  # resting AS160, GSK3, FOXO1
TARGET_OFF = "#94A3B8"   # switched-off target (high-contrast slate-grey)
GLUT_EMERALD = "#10B981"  # GLUT4, glucose, glycogen synthase, glycogen
SER_FEEDBACK = "#D99B52"  # Ser-P feedback tags
INHIB_RED = "#EF4444"    # inhibitory marks / mutant X
MEMB_STROKE = "#64748B"  # lipid bilayer lines
MEMB_FILL = "#2D3B55"    # lipid bilayer interior
VES_FILL = "#234036"     # vesicle interior fill


# ---------------------------------------------------------------------------
# Shared schematic builders
# ---------------------------------------------------------------------------
def p_badge(text="P", fill=PHOS_YELLOW, text_color=BG, size=22, radius=0.24):
    """High-contrast phosphate badge sized with comfortable border clearance."""
    if len(text) > 1:
        lab = T(text, size=size, color=text_color, weight=BOLD)
        w = max(0.92, lab.width + 0.24)
        h = max(0.44, lab.height + 0.18)
        box = RoundedRectangle(corner_radius=0.12, width=w, height=h,
                               fill_color=fill, fill_opacity=0.96,
                               stroke_color=text_color, stroke_width=1.5)
        return VGroup(box, lab.move_to(box))
    lab = T(text, size=size, color=text_color, weight=BOLD)
    c = Circle(radius=radius, fill_color=fill, fill_opacity=0.96,
               stroke_color=text_color, stroke_width=1.5)
    return VGroup(c, lab.move_to(c))


def x_badge(radius=0.23):
    """Red X badge placed outside a box so it never straddles or covers box letters."""
    c = Circle(radius=radius, fill_color=BG, fill_opacity=0.96,
               stroke_color=INHIB_RED, stroke_width=2.8)
    c1 = Line([-0.11, -0.11, 0], [0.11, 0.11, 0], color=INHIB_RED, stroke_width=4.0)
    c2 = Line([-0.11, 0.11, 0], [0.11, -0.11, 0], color=INHIB_RED, stroke_width=4.0)
    return VGroup(c, c1, c2)


def place_badge_above_right(badge, parent, dx=-0.10, gap=0.09):
    """Place a badge cleanly above the parent box without touching its stroke."""
    y = parent.get_top()[1] + gap + badge.height / 2
    x = parent.get_right()[0] + dx
    return badge.move_to([x, y, 0])


def place_badge_above_left(badge, parent, dx=0.10, gap=0.09):
    """Place a badge cleanly above the parent box on the left without touching its stroke."""
    y = parent.get_top()[1] + gap + badge.height / 2
    x = parent.get_left()[0] + dx
    return badge.move_to([x, y, 0])


def bilayer(y=1.98, x0=-6.3, x1=6.3, thickness=0.34):
    """Schematic plasma membrane bilayer bar with bold contrast."""
    w = x1 - x0
    cx = (x0 + x1) / 2
    band = Rectangle(width=w, height=thickness, fill_color=MEMB_FILL,
                     fill_opacity=0.95, stroke_width=0).move_to([cx, y, 0])
    top = Line([x0, y + thickness / 2, 0], [x1, y + thickness / 2, 0],
               color=MEMB_STROKE, stroke_width=3.6)
    bot = Line([x0, y - thickness / 2, 0], [x1, y - thickness / 2, 0],
               color=MEMB_STROKE, stroke_width=3.6)
    return VGroup(band, top, bot)


def pip_tiles(xs, y=1.68, active_mask=None, tile_w=0.44, tile_h=0.23):
    """Row of inner-leaflet lipid tiles (slate PIP2 or gold PIP3)."""
    if active_mask is None:
        active_mask = [False] * len(xs)
    tiles = VGroup()
    for x, act in zip(xs, active_mask):
        col = PIP3_GOLD if act else PIP2_SLATE
        r = RoundedRectangle(corner_radius=0.06, width=tile_w, height=tile_h,
                             fill_color=col, fill_opacity=0.94 if act else 0.85,
                             stroke_color=col, stroke_width=2.2).move_to([x, y, 0])
        tiles.add(r)
    return tiles


def insulin_receptor(x=-4.8, y=1.98, bound=True):
    """Schematic transmembrane receptor dimer with optional insulin pill on top."""
    leg_l = RoundedRectangle(corner_radius=0.08, width=0.30, height=1.35,
                             fill_color=AMBER, fill_opacity=0.38,
                             stroke_color=AMBER, stroke_width=3.0).move_to([x - 0.25, y - 0.06, 0])
    leg_r = RoundedRectangle(corner_radius=0.08, width=0.30, height=1.35,
                             fill_color=AMBER, fill_opacity=0.38,
                             stroke_color=AMBER, stroke_width=3.0).move_to([x + 0.25, y - 0.06, 0])
    cap = Arc(radius=0.44, start_angle=PI, angle=PI, arc_center=[x, y + 0.62, 0],
              color=AMBER, stroke_width=3.8)
    parts = [leg_l, leg_r, cap]
    if bound:
        ins = RoundedRectangle(corner_radius=0.14, width=0.52, height=0.30,
                               fill_color=AMBER, fill_opacity=0.95,
                               stroke_color=AMBER, stroke_width=2).move_to([x, y + 0.78, 0])
        parts.append(ins)
    return VGroup(*parts)


def akt_shape(pos=ORIGIN, active=True, with_p=True, width=1.50, height=0.68, text_size=28, p_size=22):
    """Coral-red Akt pill with two external 'P' badges cleanly above its top corners."""
    col = AKT_CORAL if active else AKT_MUTED
    op = 0.38 if active else 0.26
    body = RoundedRectangle(corner_radius=0.20, width=width, height=height,
                            fill_color=col, fill_opacity=op,
                            stroke_color=col, stroke_width=3.8 if active else 2.8).move_to(pos)
    lab = T("Akt", size=text_size, color=TEXT if active else TARGET_OFF, weight=BOLD).move_to(body)
    g = VGroup(body, lab)
    g.body = body
    g.lab = lab
    if with_p:
        p1 = place_badge_above_left(p_badge("P", size=p_size), body, dx=0.22, gap=0.08)
        p2 = place_badge_above_right(p_badge("P", size=p_size), body, dx=-0.22, gap=0.08)
        g.add(p1, p2)
        g.p1, g.p2 = p1, p2
    else:
        g.p1, g.p2 = None, None
    return g


def irs1_block(pos=(-3.0, 0.85, 0), tyr_p=True):
    """Teal IRS-1 docking platform with external P badge."""
    b = boxed_label("IRS-1", IRS_TEAL, size=26, box=(1.60, 0.58), fill_opacity=0.28).move_to(pos)
    if tyr_p:
        tp = place_badge_above_right(p_badge("P"), b.box, dx=-0.18, gap=0.09)
        b.add(tp)
        b.tp = tp
    else:
        b.tp = None
    return b


def pi3k_block(pos=(-0.95, 0.90, 0)):
    """Sky-blue PI 3-kinase."""
    return boxed_label("PI 3-kinase", PI3K_BLUE, size=24, box=(1.90, 0.58), fill_opacity=0.28).move_to(pos)


def pten_block(pos=(4.85, 0.85, 0)):
    """Mint-green PTEN eraser."""
    return boxed_label("PTEN", PTEN_MINT, size=26, box=(1.40, 0.58), fill_opacity=0.28).move_to(pos)


def clean_arrow(p0, p1, color=TEXT, stroke_width=3.4, buff=0.10):
    """Arrow trimmed cleanly by buff from both endpoints so it never straddles boxes."""
    v = np.array(p1, dtype=float) - np.array(p0, dtype=float)
    n = np.linalg.norm(v)
    if n < 2 * buff + 0.05:
        return Arrow(p0, p1, buff=0, color=color, stroke_width=stroke_width, max_tip_length_to_length_ratio=0.25)
    u = v / n
    return Arrow(np.array(p0) + u * buff, np.array(p1) - u * buff, buff=0,
                 color=color, stroke_width=stroke_width, tip_length=0.20)


def glut4_vesicle(pos, n_channels=2, radius=0.58):
    """Intracellular round vesicle carrying emerald GLUT4 channel bars."""
    ring = Circle(radius=radius, stroke_color=MEMB_STROKE, stroke_width=3.5,
                  fill_color=VES_FILL, fill_opacity=0.92).move_to(pos)
    bars = VGroup()
    angles = [PI / 2 - 0.45, PI / 2 + 0.45] if n_channels == 2 else [PI / 2]
    for ang in angles:
        c = pos + np.array([np.cos(ang), np.sin(ang), 0]) * radius
        ch = RoundedRectangle(corner_radius=0.05, width=0.18, height=0.36,
                              fill_color=GLUT_EMERALD, fill_opacity=0.96,
                              stroke_color=GLUT_EMERALD, stroke_width=2).move_to(c).rotate(ang - PI / 2)
        bars.add(ch)
    g = VGroup(ring, bars)
    g.ring = ring
    return g


def membrane_glut4_door(x, y=1.98):
    """Open emerald GLUT4 channel embedded in the plasma membrane bilayer."""
    left_wall = RoundedRectangle(corner_radius=0.04, width=0.16, height=0.48,
                                 fill_color=GLUT_EMERALD, fill_opacity=0.96,
                                 stroke_color=GLUT_EMERALD, stroke_width=2).move_to([x - 0.15, y, 0])
    right_wall = RoundedRectangle(corner_radius=0.04, width=0.16, height=0.48,
                                  fill_color=GLUT_EMERALD, fill_opacity=0.96,
                                  stroke_color=GLUT_EMERALD, stroke_width=2).move_to([x + 0.15, y, 0])
    pore = Rectangle(width=0.14, height=0.44, fill_color=BG, fill_opacity=1.0, stroke_width=0).move_to([x, y, 0])
    return VGroup(pore, left_wall, right_wall)


def build_muscle_fat_zone(mutated=False):
    """Rebuildable Muscle & fat schematic stage (shared by S02, S07, S08, S09)."""
    memb = bilayer(y=1.98, x0=-6.3, x1=6.3, thickness=0.34)
    memb_lab = T("plasma membrane", size=24, color=GREY).move_to([-5.15, 2.50, 0])
    xs = np.linspace(-0.7, 2.3, 8)
    tiles = pip_tiles(xs, y=1.68, active_mask=[True] * 8, tile_w=0.38, tile_h=0.22)
    pip_lab = T("PIP3", size=24, color=PIP3_GOLD).move_to([0.8, 2.50, 0])
    # Akt docked at y=0.52 -> P top = 0.52+0.34+0.08+0.48 = 1.42 < tiles bottom 1.57
    akt = akt_shape(pos=[0.8, 0.52, 0], active=True, with_p=True)

    # 5 intracellular vesicles with GLUT4 well below AS160
    ves_centers = [
        np.array([-4.0, -1.48, 0.0]),
        np.array([-2.0, -1.66, 0.0]),
        np.array([0.0, -1.48, 0.0]),
        np.array([2.0, -1.66, 0.0]),
        np.array([4.0, -1.48, 0.0]),
    ]
    vesicles = VGroup(*[glut4_vesicle(c) for c in ves_centers])
    glut_lab = T("GLUT4 vesicles", size=26, color=GLUT_EMERALD).move_to([-4.1, -2.42, 0])

    # AS160 brake block cleanly between Akt and vesicles
    as160_text = "AS160 mutant" if mutated else "AS160 (Rab GAP)"
    as160 = boxed_label(as160_text, TARGET_INDIGO, size=26, box=(2.75, 0.56), fill_opacity=0.28).move_to([0.0, -0.34, 0])
    tethers = VGroup(*[
        DashedLine(as160.get_bottom() + DOWN * 0.05, c + UP * 0.62,
                   color=TARGET_INDIGO, stroke_width=2.8, dash_length=0.10)
        for c in ves_centers[1:4]
    ])
    g = VGroup(memb, memb_lab, tiles, pip_lab, akt, vesicles, glut_lab, as160, tethers)
    g.memb = memb
    g.memb_lab = memb_lab
    g.tiles = tiles
    g.pip_lab = pip_lab
    g.akt = akt
    g.vesicles = vesicles
    g.ves_centers = ves_centers
    g.glut_lab = glut_lab
    g.as160 = as160
    g.tethers = tethers
    if mutated:
        xm = x_badge().next_to(as160.box, RIGHT, buff=0.14)
        g.add(xm)
        g.x_mark = xm
    return g


def branched_glycogen_positions(origin=(-0.15, -0.15, 0), seed=3):
    """Compute a deterministic 22-bead branched glycogen tree (first 4 = primer, 18 added)."""
    rng = np.random.default_rng(seed)
    pts = [np.array(origin, dtype=float)]
    edges = []
    for i in range(1, 12):
        step = np.array([0.46, 0.06 + rng.uniform(-0.07, 0.07), 0.0])
        pts.append(pts[-1] + step)
        edges.append((i - 1, i))
    b1_start = 3
    for k in range(5):
        parent = b1_start if k == 0 else len(pts) - 1
        step = np.array([0.38, 0.34 + rng.uniform(-0.04, 0.05), 0.0])
        pts.append(pts[parent] + step)
        edges.append((parent, len(pts) - 1))
    b2_start = 6
    for k in range(5):
        parent = b2_start if k == 0 else len(pts) - 1
        step = np.array([0.38, -0.34 + rng.uniform(-0.05, 0.04), 0.0])
        pts.append(pts[parent] + step)
        edges.append((parent, len(pts) - 1))
    return pts, edges


# ---------------------------------------------------------------------------
# Scenes
# ---------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "PI 3-Kinase, Akt and Insulin"
    TITLE = "One Kinase, Many Targets—and Its Brakes"


class S01Hook(SpokenScene):
    def construct(self):
        memb = bilayer(y=1.98, x0=-6.3, x1=6.3, thickness=0.34)
        rec = insulin_receptor(x=-5.1, y=1.98, bound=True)
        rec_lab = T("insulin + receptor", size=24, color=AMBER).move_to([-4.6, 3.15, 0])
        irs = irs1_block(pos=(-3.1, 0.82, 0), tyr_p=True)
        pi3k = pi3k_block(pos=(-1.05, 0.88, 0))
        a_rec_irs = clean_arrow(rec.get_bottom() + RIGHT * 0.25, irs.box.get_left(), color=AMBER, buff=0.06)

        xs = np.linspace(0.35, 3.45, 8)
        tiles = pip_tiles(xs, y=1.68, active_mask=[False] * 8, tile_w=0.38, tile_h=0.22)
        pip_lab = T("PIP2", size=24, color=PIP2_SLATE).move_to([1.9, 2.50, 0])

        akt = akt_shape(pos=[1.9, -0.15, 0], active=False, with_p=False)
        pten = pten_block(pos=(4.75, 0.82, 0))
        tag = scope_tag("schematic")

        zone_specs = [
            ("Muscle & fat", -4.25, "GLUT4 uptake"),
            ("Glycogen", -0.35, "storage chains"),
            ("Liver nucleus", 3.55, "gene control"),
        ]
        zones = VGroup()
        for name, zx, sub in zone_specs:
            box = RoundedRectangle(corner_radius=0.16, width=3.45, height=1.70,
                                   stroke_color=TARGET_INDIGO, stroke_width=2.4, stroke_opacity=0.60,
                                   fill_color=TARGET_INDIGO, fill_opacity=0.16).move_to([zx, -1.92, 0])
            hdr = T(name, size=26, color=TEXT, weight=BOLD).set_opacity(0.75).move_to([zx, -1.54, 0])
            sub_t = T(sub, size=24, color=TARGET_INDIGO).set_opacity(0.75).move_to([zx, -2.22, 0])
            zones.add(VGroup(box, hdr, sub_t))

        self.add(tag, memb, rec, rec_lab, irs, a_rec_irs, pi3k, tiles, pip_lab, akt, pten, zones)

        # Continuous lipid conversion before 'recruiting'
        gold_tiles = pip_tiles(xs, y=1.68, active_mask=[True] * 8, tile_w=0.38, tile_h=0.22)
        self.play(Transform(tiles[0], gold_tiles[0]), Transform(tiles[1], gold_tiles[1]), run_time=2.3)

        # Beat 1: PIP3 recruiting Akt to the membrane
        self.at("recruiting")
        new_pip_lab = T("PIP3", size=24, color=PIP3_GOLD).move_to([1.9, 2.50, 0])
        self.play(
            LaggedStart(*[Transform(tiles[i], gold_tiles[i]) for i in range(2, len(xs))], lag_ratio=0.14),
            swap(pip_lab, new_pip_lab, run_time=0.6),
            akt.animate.move_to([1.9, 0.52, 0]),
            run_time=2.0,
        )

        # Beat 2: Two phosphates activate it
        self.at("two phosphates")
        akt_on = akt_shape(pos=[1.9, 0.52, 0], active=True, with_p=True)
        self.play(
            akt.body.animate.set_stroke(AKT_CORAL, 4.0).set_fill(AKT_CORAL, 0.38),
            akt.lab.animate.set_color(TEXT),
            FadeIn(akt_on.p1, scale=0.6),
            FadeIn(akt_on.p2, scale=0.6),
            run_time=2.8,
        )
        self.remove(akt)
        akt = akt_on
        self.add(akt)

        # Beat 3: Akt turns on -> drives three tissue zones
        self.at("turns on")
        z_arrows = VGroup(*[
            clean_arrow(akt.body.get_bottom(), z[0].get_top(), color=AKT_CORAL, stroke_width=3.6, buff=0.08)
            for z in zones
        ])
        self.play(GrowArrow(z_arrows[0]), run_time=2.0)

        self.at("drive different tissue")
        self.play(
            GrowArrow(z_arrows[1]), GrowArrow(z_arrows[2]),
            *[z[0].animate.set_stroke(TARGET_INDIGO, 3.2, opacity=1.0).set_fill(TARGET_INDIGO, 0.28) for z in zones],
            *[z[1].animate.set_opacity(1.0) for z in zones],
            *[z[2].animate.set_opacity(1.0) for z in zones],
            run_time=1.6,
        )

        self.at("without running forever")
        runaway_bar_bg = RoundedRectangle(corner_radius=0.08, width=0.40, height=1.50,
                                          stroke_color=GREY, stroke_width=2.5, fill_opacity=0.18).move_to([5.85, -1.75, 0])
        sig_frac = ValueTracker(0.35)
        runaway_fill = always_redraw(lambda: Rectangle(
            width=0.30, height=max(0.05, 1.42 * sig_frac.get_value()),
            fill_color=AKT_CORAL if sig_frac.get_value() > 0.7 else PIP3_GOLD,
            fill_opacity=0.94, stroke_width=0
        ).move_to([5.85, -1.75 - 0.71 + max(0.05, 1.42 * sig_frac.get_value()) / 2, 0]))
        q_mark = T("?", size=32, color=AKT_CORAL, weight=BOLD).move_to([5.85, -0.68, 0])
        sig_lab = T("signal", size=22, color=GREY).next_to(runaway_bar_bg, DOWN, buff=0.10)
        self.play(FadeIn(runaway_bar_bg), FadeIn(sig_lab), FadeIn(q_mark), run_time=0.4)
        self.add(runaway_fill)
        self.play(sig_frac.animate.set_value(0.96), run_time=3.6, rate_func=linear)

        # Beat 4: Tissue targets + lipid erasers + negative feedback
        self.at("targets")
        self.play(*[z[0].animate.set_fill(TARGET_INDIGO, 0.34) for z in zones], run_time=0.6)

        self.at("with lipid erasers")
        pten_arrow = clean_arrow(pten.box.get_top() + LEFT * 0.25, tiles[-1].get_bottom(),
                                 color=PTEN_MINT, stroke_width=3.6, buff=0.08)
        self.play(
            GrowArrow(pten_arrow),
            pten.box.animate.set_stroke(PTEN_MINT, 4.0).set_fill(PTEN_MINT, 0.34),
            sig_frac.animate.set_value(0.62),
            FadeOut(q_mark),
            run_time=1.0,
        )

        self.at("and negative feedback")
        fb_arc = CurvedArrow(akt.body.get_left() + LEFT * 0.08 + DOWN * 0.10,
                             irs.box.get_bottom() + DOWN * 0.08,
                             angle=-0.42, color=SER_FEEDBACK, stroke_width=3.6)
        fb_lab = T("feedback", size=24, color=SER_FEEDBACK).move_to([-2.05, -0.18, 0])
        self.play(Create(fb_arc), FadeIn(fb_lab), sig_frac.animate.set_value(0.45), run_time=2.0)
        self.finish()


class S02Glut4As160(SpokenScene):
    def construct(self):
        title = T("Muscle & fat", size=30, color=TEXT, weight=BOLD).move_to([-4.6, 3.25, 0])
        tag = scope_tag("schematic")
        stage = build_muscle_fat_zone(mutated=False)
        xs = np.linspace(-0.7, 2.3, 8)
        pip2_tiles = pip_tiles(xs, y=1.68, active_mask=[False] * 8, tile_w=0.38, tile_h=0.22)
        pip2_lab = T("PIP2", size=24, color=PIP2_SLATE).move_to([0.8, 2.50, 0])
        self.add(title, tag, stage.memb, stage.memb_lab, pip2_tiles, pip2_lab)

        # Build resting vesicles continuously across 0..8.5s
        self.play(FadeIn(stage.vesicles[0], shift=UP * 0.10), FadeIn(stage.glut_lab), run_time=1.6)
        self.play(FadeIn(stage.vesicles[1], shift=UP * 0.10), FadeIn(stage.vesicles[2], shift=UP * 0.10), run_time=1.6)

        self.at("at rest")
        self.play(FadeIn(stage.vesicles[3], shift=UP * 0.10), FadeIn(stage.vesicles[4], shift=UP * 0.10), run_time=1.8)
        self.play(LaggedStart(*[v.ring.animate.set_stroke(GLUT_EMERALD, 3.5) for v in stage.vesicles], lag_ratio=0.18),
                  run_time=3.2)

        # Beat 2: A brake protein, AS160, holds those vesicles back
        self.at("a brake protein")
        self.play(FadeIn(stage.as160), run_time=1.8)
        self.at("holds those vesicles")
        tethers = VGroup(*[
            DashedLine(stage.as160.get_bottom() + DOWN * 0.05, v.get_top() + UP * 0.05,
                       color=TARGET_INDIGO, stroke_width=2.8, dash_length=0.10)
            for v in stage.vesicles[1:4]
        ])
        self.play(LaggedStart(*[Create(t) for t in tethers], lag_ratio=0.22), run_time=2.6)

        # Beat 3: Active Akt phosphorylates that brake and switches it off (move Akt horizontally clear of P!)
        self.at("phosphorylates that brake")
        self.play(
            LaggedStart(*[Transform(pip2_tiles[i], stage.tiles[i]) for i in range(len(xs))], lag_ratio=0.08),
            swap(pip2_lab, stage.pip_lab, run_time=0.5),
            FadeIn(stage.akt, shift=UP * 0.2),
            run_time=0.75,
        )
        self.remove(pip2_tiles)
        self.add(stage.tiles)
        self.play(stage.akt.animate.shift(RIGHT * 2.15), run_time=0.55)
        p_stamp = p_badge("P").next_to(stage.as160.box, RIGHT, buff=0.14)
        self.play(FadeIn(p_stamp, scale=0.5), run_time=0.45)

        self.at("switches it off")
        off_label = T("AS160 (off)", size=26, color=TARGET_OFF).move_to(stage.as160.label)
        self.play(
            stage.as160.box.animate.set_stroke(TARGET_OFF, 2.4).set_fill(TARGET_OFF, 0.22),
            swap(stage.as160.label, off_label, run_time=0.7),
            FadeOut(tethers),
            run_time=1.2,
        )

        # Beat 4: With help from other proteins, vesicles then fuse with the surface
        self.at("with help from")
        helpers = boxed_label("helper proteins", GREY, size=24, box=(2.35, 0.50), fill_opacity=0.26).move_to([-4.55, 0.25, 0])
        self.play(FadeIn(helpers), stage.akt.animate.shift(LEFT * 2.15), run_time=1.4)

        self.at("vesicles then fuse")
        door_xs = [-3.25, -1.85, 3.6, 5.1]
        gliding = [stage.vesicles[0], stage.vesicles[1], stage.vesicles[3], stage.vesicles[4]]
        self.play(
            FadeOut(helpers),
            FadeOut(stage.as160.box), FadeOut(off_label), FadeOut(p_stamp),
            FadeOut(stage.glut_lab),
            run_time=0.35,
        )
        self.play(
            *[v.animate.move_to([x, 1.32, 0]) for v, x in zip(gliding, door_xs)],
            run_time=1.45,
        )
        doors = VGroup(*[membrane_glut4_door(x, y=1.98) for x in door_xs])
        door_lab = T("GLUT4 channels at surface", size=24, color=GLUT_EMERALD).move_to([-0.5, 3.25, 0])
        self.play(
            *[FadeOut(v) for v in gliding],
            *[FadeIn(d) for d in doors],
            FadeIn(door_lab),
            run_time=0.9,
        )
        for v in gliding:
            self.remove(v)

        # Beat 5: Letting glucose stream in (computed seeded particle stream)
        self.at("letting glucose")
        rng = np.random.default_rng(7)
        ext_lab = T("glucose", size=26, color=GLUT_EMERALD).move_to([4.4, 3.25, 0])
        self.play(FadeIn(ext_lab), run_time=0.35)

        n_dots = 22
        stream_prog = ValueTracker(0.0)
        dot_specs = []
        for k in range(n_dots):
            dx = door_xs[k % len(door_xs)]
            phase = (k / n_dots) * 0.9
            x_jit = rng.uniform(-0.04, 0.04)
            spread = rng.uniform(-0.42, 0.42)
            dot_specs.append((dx, phase, x_jit, spread))

        def mk_glucose():
            g = VGroup()
            t = stream_prog.get_value()
            for dx, phase, xj, sp in dot_specs:
                u = t - phase
                if u < 0 or u > 1.05:
                    continue
                u_mod = min(u, 1.0)
                y = 2.75 - u_mod * 4.65
                x = dx + xj + (max(0.0, u_mod - 0.30) / 0.70) * sp
                g.add(Dot([x, y, 0], radius=0.11, color=GLUT_EMERALD))
            return g

        stream_mob = always_redraw(mk_glucose)
        self.add(stream_mob)
        rem = max(1.0, self.narration_s + 0.25 - self.elapsed())
        self.play(stream_prog.animate.set_value(1.95), run_time=rem, rate_func=linear)
        self.finish()


class S03Gsk3Glycogen(SpokenScene):
    def construct(self):
        title = T("Glycogen storage (muscle & liver)", size=30, color=TEXT, weight=BOLD).move_to([-3.2, 3.25, 0])
        tag = scope_tag("schematic")
        self.add(title, tag)

        # Left: emerald Glycogen synthase block + indigo GSK3 + live schematic synthase-rate bar
        gs_box = boxed_label("glycogen synthase", GLUT_EMERALD, size=26, box=(3.60, 0.96), fill_opacity=0.32).move_to([-3.65, -0.55, 0])
        gsk3 = boxed_label("GSK3", TARGET_INDIGO, size=28, box=(1.85, 0.68), fill_opacity=0.32).move_to([-3.65, 1.35, 0])
        inhib_marks = VGroup(*[
            p_badge("P", fill=INHIB_RED, text_color=TEXT).move_to(
                gs_box.box.get_top() + LEFT * 0.95 + RIGHT * (i * 0.95) + UP * 0.34
            )
            for i in range(3)
        ])
        state_slow = T("slow (inhibited)", size=26, color=INHIB_RED).move_to([-3.65, -1.70, 0])

        rate_val = ValueTracker(0.45)
        rate_lab = T("synthase rate", size=24, color=GREY).move_to([-4.65, -2.55, 0])
        rate_bg = RoundedRectangle(corner_radius=0.08, width=2.4, height=0.28,
                                   stroke_color=GREY, stroke_width=2.2, fill_opacity=0.18).move_to([-2.30, -2.55, 0])
        rate_fill = always_redraw(lambda: Rectangle(
            width=max(0.08, 2.30 * rate_val.get_value()), height=0.20,
            fill_color=INHIB_RED if rate_val.get_value() < 0.35 else GLUT_EMERALD,
            fill_opacity=0.94, stroke_width=0
        ).move_to([-2.30 - 1.15 + max(0.08, 2.30 * rate_val.get_value()) / 2, -2.55, 0]))

        pts, edges = branched_glycogen_positions(origin=(-0.15, -0.15, 0), seed=3)
        chain_lab = T("glycogen chain", size=26, color=GLUT_EMERALD).move_to([3.3, 2.25, 0])
        beads = [Dot(p, radius=0.18, color=GLUT_EMERALD) for p in pts]
        links = [Line(pts[a], pts[b], color=GLUT_EMERALD, stroke_width=5.2) for a, b in edges]
        primer_grp = VGroup(beads[0], links[0], beads[1], links[1], beads[2], links[2], beads[3])

        self.add(gs_box, primer_grp, chain_lab, rate_lab, rate_bg, rate_fill)
        self.play(Create(links[3]), FadeIn(beads[4], scale=0.6), rate_val.animate.set_value(0.55), run_time=2.2)
        self.play(Create(links[4]), FadeIn(beads[5], scale=0.6), run_time=2.2)

        # Beat 1: GSK3 normally phosphorylates glycogen synthase and keeps it slow
        self.at("an enzyme called")
        self.play(FadeIn(gsk3, shift=DOWN * 0.15), run_time=1.6)

        self.at("normally phosphorylates")
        gsk_arrow = clean_arrow(gsk3.box.get_bottom(), gs_box.box.get_top() + UP * 0.54, color=TARGET_INDIGO, buff=0.06)
        self.play(GrowArrow(gsk_arrow), LaggedStart(*[FadeIn(m, scale=0.6) for m in inhib_marks], lag_ratio=0.25),
                  rate_val.animate.set_value(0.18), run_time=2.8)

        self.at("keeps it slow")
        self.play(FadeIn(state_slow), rate_val.animate.set_value(0.10), run_time=2.0)

        # Beat 2: Active Akt phosphorylates GSK3 and shuts it down
        self.at("phosphorylates gsk3")
        akt = akt_shape(pos=[-0.85, 1.80, 0], active=True, with_p=True)
        self.play(FadeIn(akt), run_time=0.6)
        self.play(akt.animate.move_to([-1.25, 1.30, 0]), run_time=1.2)
        p_gsk = place_badge_above_right(p_badge("P"), gsk3.box, dx=-0.15, gap=0.09)
        self.play(FadeIn(p_gsk, scale=0.5), run_time=0.6)

        self.at("shuts it down")
        gsk_off_lab = T("GSK3 (off)", size=26, color=TARGET_OFF).move_to(gsk3.label)
        self.play(
            gsk3.box.animate.set_stroke(TARGET_OFF, 2.4).set_fill(TARGET_OFF, 0.22),
            swap(gsk3.label, gsk_off_lab, run_time=0.7),
            FadeOut(gsk_arrow),
            run_time=1.1,
        )

        # Beat 3: With that brake gone, GSK3 drifts away, inhibitory marks vanish
        self.at("with that")
        gsk_group = VGroup(gsk3.box, gsk_off_lab, p_gsk)
        state_fast = T("active (fast)", size=26, color=GLUT_EMERALD).move_to([-3.65, -1.70, 0])
        self.play(
            gsk_group.animate.move_to([-4.95, 1.85, 0]),
            FadeOut(inhib_marks),
            swap(state_slow, state_fast, run_time=0.7),
            rate_val.animate.set_value(0.95),
            run_time=2.0,
        )

        # Beat 4: Glycogen synthase speeds up and builds storage chains (beads 6..21)
        self.at("speeds up")
        link_arrow = clean_arrow(gs_box.box.get_right(), beads[0].get_center() + LEFT * 0.16, color=GLUT_EMERALD, buff=0.08)
        self.play(
            gs_box.box.animate.set_stroke(GLUT_EMERALD, 4.8).set_fill(GLUT_EMERALD, 0.38),
            GrowArrow(link_arrow),
            run_time=0.8,
        )

        rem_edges = edges[5:]
        rem_links = links[5:]
        n_steps = len(rem_edges)
        step_rt = max(0.08, (self.narration_s - self.elapsed() - 0.1) / n_steps)
        for idx, (a, b) in enumerate(rem_edges):
            self.play(Create(rem_links[idx]), FadeIn(beads[b], scale=0.6), run_time=step_rt)
        self.finish()


class S04Foxo1Liver(SpokenScene):
    def construct(self):
        title = T("Liver nucleus", size=30, color=TEXT, weight=BOLD).move_to([-4.6, 3.25, 0])
        tag = scope_tag("schematic")

        nuc_box = RoundedRectangle(corner_radius=1.1, width=7.5, height=5.1,
                                   fill_color="#1D2A46", fill_opacity=0.94,
                                   stroke_color=GREY, stroke_width=4.0).move_to([-2.15, -0.35, 0])
        pore_gap = Rectangle(width=0.45, height=1.20, fill_color=BG, fill_opacity=1.0,
                             stroke_width=0).move_to([1.60, -0.35, 0])
        pore_top = Circle(radius=0.11, fill_color=GREY, fill_opacity=0.95, stroke_width=0).move_to([1.60, 0.25, 0])
        pore_bot = Circle(radius=0.11, fill_color=GREY, fill_opacity=0.95, stroke_width=0).move_to([1.60, -0.95, 0])
        pore_lab = T("nuclear pore", size=24, color=GREY).move_to([2.65, -1.40, 0])
        cyto_lab = T("cytosol", size=26, color=GREY).move_to([4.5, 2.55, 0])

        dna_x = np.linspace(-5.1, 0.5, 40)
        pts1 = [[x, -1.45 + 0.16 * np.sin(2.5 * x), 0] for x in dna_x]
        pts2 = [[x, -1.45 - 0.16 * np.sin(2.5 * x), 0] for x in dna_x]
        dna1 = VMobject(color=IRS_TEAL, stroke_width=4.2).set_points_as_corners(pts1)
        dna2 = VMobject(color=PI3K_BLUE, stroke_width=4.2).set_points_as_corners(pts2)
        dna_lab = T("DNA", size=24, color=IRS_TEAL).move_to([-4.95, -2.02, 0])

        foxo = boxed_label("FOXO1", TARGET_INDIGO, size=28, box=(1.80, 0.62), fill_opacity=0.30).move_to([-2.4, -0.62, 0])
        gene_lab = T("Gluconeogenic genes", size=26, color=GLUT_EMERALD).move_to([-2.3, 1.35, 0])
        tx_arrows = VGroup(*[
            Arrow([-3.2 + i * 0.9, 0.15, 0], [-3.2 + i * 0.9, 0.98, 0],
                  buff=0, color=GLUT_EMERALD, stroke_width=4.2, tip_length=0.20)
            for i in range(3)
        ])

        self.add(title, tag, nuc_box, pore_gap, pore_top, pore_bot, pore_lab, cyto_lab)
        self.play(Create(dna1), Create(dna2), FadeIn(dna_lab), run_time=3.2)

        # Beat 1: Between meals, FOXO1 sits on DNA, driving genes that build new glucose
        self.at("between meals")
        self.play(FadeIn(foxo, shift=DOWN * 0.12), run_time=2.8)
        self.at("driving genes")
        self.play(FadeIn(gene_lab), LaggedStart(*[GrowArrow(a) for a in tx_arrows], lag_ratio=0.18),
                  run_time=1.4)

        tx_t = ValueTracker(0.0)
        tx_pulses = always_redraw(lambda: VGroup(*[
            Dot([-3.2 + i * 0.9, 0.18 + ((tx_t.get_value() + i * 0.25) % 1.0) * 0.80, 0],
                radius=0.09, color=GLUT_EMERALD)
            for i in range(3)
        ]))
        self.add(tx_pulses)
        self.play(tx_t.animate.set_value(2.0), run_time=2.8, rate_func=linear)
        self.remove(tx_pulses)

        # Beat 2: Active Akt enters briefly and stamps P onto FOXO1, then exits
        self.at("active")
        akt = akt_shape(pos=[4.2, 0.95, 0], active=True, with_p=True)
        self.play(FadeIn(akt), run_time=0.4)
        self.play(akt.animate.move_to([1.60, -0.35, 0]), run_time=0.7)
        self.play(akt.animate.move_to([-0.20, -0.55, 0]), run_time=0.7)
        p_foxo = place_badge_above_right(p_badge("P"), foxo.box, dx=-0.16, gap=0.08)
        self.play(FadeIn(p_foxo, scale=0.5), run_time=0.5)
        self.play(akt.animate.move_to([4.2, 1.55, 0]), run_time=0.8)
        self.play(FadeOut(akt), run_time=0.4)

        # Beat 3: Partner proteins (14-3-3) clasp phosphorylated FOXO1, move it out
        self.at("partner proteins")
        anchor = boxed_label("14-3-3", GOLD, size=24, box=(1.45, 0.50), fill_opacity=0.28).move_to([4.0, -0.35, 0])
        self.play(FadeIn(anchor), run_time=0.5)
        self.play(anchor.animate.move_to([-0.35, -0.62, 0]), run_time=0.9)

        self.at("move it out")
        foxo_bundle = VGroup(foxo, p_foxo, anchor)
        self.play(foxo_bundle.animate.move_to([1.60, -0.35, 0]), run_time=0.8)
        self.at("hold it in")
        self.play(foxo_bundle.animate.move_to([4.2, -0.25, 0]), run_time=1.8)

        # Beat 4: Over hours, those glucose-making genes quiet down
        self.at("over hours")
        hours_lab = T("hours later: genes quiet down", size=26, color=GOLD).move_to([-2.3, 2.82, 0])
        hrs_prog = ValueTracker(0.05)
        hrs_bar_bg = RoundedRectangle(corner_radius=0.06, width=3.4, height=0.22,
                                      stroke_color=GREY, stroke_width=2, fill_opacity=0.16).move_to([-2.3, 2.48, 0])
        hrs_bar_fill = always_redraw(lambda: Rectangle(
            width=max(0.08, 3.32 * hrs_prog.get_value()), height=0.14,
            fill_color=GOLD, fill_opacity=0.92, stroke_width=0
        ).move_to([-2.3 - 1.66 + max(0.08, 3.32 * hrs_prog.get_value()) / 2, 2.48, 0]))
        self.play(FadeIn(hours_lab), FadeIn(hrs_bar_bg), run_time=0.5)
        self.add(hrs_bar_fill)
        self.play(hrs_prog.animate.set_value(0.55), run_time=1.5, rate_func=linear)

        self.at("quiet down")
        self.play(
            hrs_prog.animate.set_value(1.0),
            *[a.animate.set_color(TARGET_OFF).set_opacity(0.42) for a in tx_arrows],
            gene_lab.animate.set_color(TARGET_OFF),
            foxo.box.animate.set_stroke(TARGET_OFF, 2.2).set_fill(TARGET_OFF, 0.20),
            run_time=1.8,
        )
        self.finish()


class S05GuidingRule(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic")
        self.add(tag)

        col_xs = [-4.2, 0.0, 4.2]
        cols = VGroup()

        c1_frame = RoundedRectangle(corner_radius=0.16, width=3.85, height=3.45,
                                    stroke_color=GLUT_EMERALD, stroke_width=3.0,
                                    fill_color=GLUT_EMERALD, fill_opacity=0.18).move_to([col_xs[0], 1.25, 0])
        c1_t = boxed_label("AS160", TARGET_OFF, size=26, box=(1.65, 0.56), fill_opacity=0.26).move_to([col_xs[0] - 0.35, 2.08, 0])
        c1_p = place_badge_above_right(p_badge("P", size=24), c1_t.box, dx=-0.16, gap=0.08)
        c1_off = T("off", size=26, color=TARGET_OFF).next_to(c1_t, RIGHT, buff=0.18)
        c1_arr = clean_arrow([col_xs[0], 1.68, 0], [col_xs[0], 0.96, 0], color=GLUT_EMERALD, buff=0.06)
        c1_out = T("GLUT4 up", size=28, color=GLUT_EMERALD, weight=BOLD).move_to([col_xs[0], 0.56, 0])
        c1_sub = T("glucose uptake", size=24, color=TEXT).move_to([col_xs[0], 0.05, 0])
        c1_icon = Dot([col_xs[0] - 0.8, -0.32, 0], radius=0.12, color=GLUT_EMERALD)
        cols.add(VGroup(c1_frame, c1_t, c1_p, c1_off, c1_arr, c1_out, c1_sub, c1_icon))

        c2_frame = RoundedRectangle(corner_radius=0.16, width=3.85, height=3.45,
                                    stroke_color=GLUT_EMERALD, stroke_width=3.0,
                                    fill_color=GLUT_EMERALD, fill_opacity=0.18).move_to([col_xs[1], 1.25, 0])
        c2_t = boxed_label("GSK3", TARGET_OFF, size=26, box=(1.55, 0.56), fill_opacity=0.26).move_to([col_xs[1] - 0.35, 2.08, 0])
        c2_p = place_badge_above_right(p_badge("P", size=24), c2_t.box, dx=-0.16, gap=0.08)
        c2_off = T("off", size=26, color=TARGET_OFF).next_to(c2_t, RIGHT, buff=0.18)
        c2_arr = clean_arrow([col_xs[1], 1.68, 0], [col_xs[1], 0.96, 0], color=GLUT_EMERALD, buff=0.06)
        c2_out = T("glycogen up", size=28, color=GLUT_EMERALD, weight=BOLD).move_to([col_xs[1], 0.56, 0])
        c2_sub = T("storage chains", size=24, color=TEXT).move_to([col_xs[1], 0.05, 0])
        c2_icon = VGroup(*[Dot([col_xs[1] - 0.6 + i * 0.4, -0.32, 0], radius=0.12, color=GLUT_EMERALD) for i in range(4)])
        cols.add(VGroup(c2_frame, c2_t, c2_p, c2_off, c2_arr, c2_out, c2_sub, c2_icon))

        c3_frame = RoundedRectangle(corner_radius=0.16, width=3.85, height=3.45,
                                    stroke_color=TARGET_INDIGO, stroke_width=3.0,
                                    fill_color=TARGET_INDIGO, fill_opacity=0.18).move_to([col_xs[2], 1.25, 0])
        c3_t = boxed_label("FOXO1", TARGET_OFF, size=26, box=(1.65, 0.56), fill_opacity=0.26).move_to([col_xs[2] - 0.35, 2.08, 0])
        c3_p = place_badge_above_right(p_badge("P", size=24), c3_t.box, dx=-0.16, gap=0.08)
        c3_off = T("out", size=26, color=TARGET_OFF).next_to(c3_t, RIGHT, buff=0.18)
        c3_arr = clean_arrow([col_xs[2], 1.68, 0], [col_xs[2], 0.96, 0], color=TARGET_INDIGO, buff=0.06)
        c3_out = T("liver genes down", size=28, color=TARGET_INDIGO, weight=BOLD).move_to([col_xs[2], 0.56, 0])
        c3_sub = T("new glucose slows", size=24, color=TEXT).move_to([col_xs[2], 0.05, 0])
        c3_icon = Line([col_xs[2] - 0.8, -0.32, 0], [col_xs[2] + 0.8, -0.32, 0], color=TARGET_INDIGO, stroke_width=4.2)
        cols.add(VGroup(c3_frame, c3_t, c3_p, c3_off, c3_arr, c3_out, c3_sub, c3_icon))

        self.play(FadeIn(cols[0], shift=UP * 0.15), run_time=0.8)
        self.play(FadeIn(cols[1], shift=UP * 0.15), run_time=0.8)
        self.at("all three jobs")
        self.play(FadeIn(cols[2], shift=UP * 0.15), run_time=1.6)

        self.at("switches each target")
        self.play(*[c[1].box.animate.set_stroke(TARGET_INDIGO, 3.2) for c in cols],
                  c1_icon.animate.shift(RIGHT * 1.6), run_time=1.8)

        self.at("removing a brake")
        brake_sum = boxed_label("Brake off (AS160, GSK3) → uptake, storage up",
                                GLUT_EMERALD, size=24, fill_opacity=0.22).move_to([-1.8, -1.08, 0])
        self.play(
            c1_frame.animate.set_stroke(GOLD, 3.4),
            c2_frame.animate.set_stroke(GOLD, 3.4),
            c1_out.animate.set_color(GOLD),
            c2_out.animate.set_color(GOLD),
            c2_icon.animate.scale(1.18),
            FadeIn(brake_sum, shift=UP * 0.10),
            run_time=2.2,
        )

        self.at("removing a driver")
        driver_sum = boxed_label("Driver off (FOXO1) → glucose-making genes down",
                                 TARGET_INDIGO, size=24, fill_opacity=0.22).move_to([1.6, -2.06, 0])
        self.play(
            c3_frame.animate.set_stroke(GOLD, 3.4),
            c3_out.animate.set_color(GOLD),
            c3_icon.animate.set_opacity(0.35),
            FadeIn(driver_sum, shift=UP * 0.10),
            run_time=2.2,
        )

        self.at("keep this second")
        rule_cap = caption("Akt phosphorylates tissue-specific targets, while erasers and feedback limit the signal.",
                           size=28, color=GOLD)
        self.play(FadeIn(rule_cap, shift=UP * 0.1), run_time=1.8)

        self.at("tissue specific targets")
        self.play(
            c1_frame.animate.set_stroke(GOLD, 3.8),
            c2_frame.animate.set_stroke(GOLD, 3.8),
            c3_frame.animate.set_stroke(GOLD, 3.8),
            run_time=1.2,
        )

        self.at("while erasers")
        memb = bilayer(y=1.98, x0=-6.3, x1=6.3, thickness=0.34)
        rec = insulin_receptor(x=-4.8, y=1.98, bound=True)
        irs = irs1_block(pos=(-3.0, 0.85, 0), tyr_p=True)
        pi3k = pi3k_block(pos=(-0.95, 0.90, 0))
        xs = np.linspace(0.45, 3.55, 8)
        tiles = pip_tiles(xs, y=1.68, active_mask=[True] * 8, tile_w=0.38, tile_h=0.22)
        pip_lab = T("PIP3", size=24, color=PIP3_GOLD).move_to([2.0, 2.50, 0])
        akt = akt_shape(pos=[2.0, 0.52, 0], active=True, with_p=True)
        pten = pten_block(pos=(4.95, 0.85, 0))
        self.play(FadeOut(cols), FadeOut(brake_sum), FadeOut(driver_sum), run_time=0.45)
        self.play(
            FadeIn(memb), FadeIn(rec), FadeIn(irs), FadeIn(pi3k),
            FadeIn(tiles), FadeIn(pip_lab), FadeIn(akt), FadeIn(pten),
            run_time=0.85,
        )
        self.at("limit the signal")
        self.play(pten.animate.shift(LEFT * 0.35), run_time=1.2)
        self.finish()


class S06ErasersFeedback(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic")
        memb = bilayer(y=1.98, x0=-6.3, x1=6.3, thickness=0.34)
        rec = insulin_receptor(x=-4.9, y=1.98, bound=True)
        rec_p = p_badge("P").move_to([-4.22, 1.38, 0])
        irs = irs1_block(pos=(-2.9, 0.85, 0), tyr_p=True)
        pi3k = pi3k_block(pos=(-0.70, 0.90, 0))
        a_dock = clean_arrow(irs.box.get_right(), pi3k.box.get_left(), color=IRS_TEAL, buff=0.06)

        xs = np.linspace(0.70, 3.80, 8)
        tiles = pip_tiles(xs, y=1.68, active_mask=[True] * 8, tile_w=0.38, tile_h=0.22)
        pip_lab = T("PIP3", size=24, color=PIP3_GOLD).move_to([2.25, 2.50, 0])
        akt = akt_shape(pos=[2.25, 0.52, 0], active=True, with_p=True)
        pten = pten_block(pos=(5.15, 1.15, 0))

        self.add(tag, memb, rec, rec_p, irs, pi3k, a_dock, tiles, pip_lab, akt, pten)

        # Beat 1: Every signal needs an off switch
        self.at("an off switch")
        ptase = boxed_label("Tyr phosphatase", PTEN_MINT, size=24, box=(2.35, 0.56), fill_opacity=0.28).move_to([-4.2, -0.65, 0])
        self.play(FadeIn(ptase, shift=UP * 0.15), run_time=2.2)

        # Beat 2: Tyrosine phosphatases reset the receptor and docking protein
        self.at("reset the receptor")
        self.play(ptase.animate.move_to([-4.2, 0.05, 0]), run_time=1.0)
        self.play(FadeOut(rec_p, shift=DOWN * 0.2), run_time=0.8)
        self.play(ptase.animate.move_to([-2.9, -0.10, 0]), run_time=1.0)
        self.play(
            FadeOut(irs.tp, shift=DOWN * 0.2),
            FadeOut(a_dock),
            pi3k.animate.move_to([-0.35, -0.45, 0]),
            ptase.animate.shift(DOWN * 1.1).set_opacity(0.0),
            run_time=2.2,
        )
        self.remove(ptase)

        # Beat 3: Mint-green PTEN sweeps above Akt at y=1.18, stripping PIP3 -> PIP2
        self.at("strips")
        self.play(
            akt.animate.move_to([2.25, -0.05, 0]),
            pten.animate.move_to([3.85, 1.18, 0]),
            run_time=0.8,
        )
        slate_tiles = pip_tiles(xs, y=1.68, active_mask=[False] * 8, tile_w=0.38, tile_h=0.22)
        self.play(
            pten.animate.move_to([0.65, 1.18, 0]),
            LaggedStart(*[Transform(tiles[len(xs) - 1 - i], slate_tiles[len(xs) - 1 - i])
                          for i in range(len(xs))], lag_ratio=0.14),
            run_time=2.6,
        )

        self.at("restoring slate")
        pip2_lab = T("PIP2", size=24, color=PIP2_SLATE).move_to([2.25, 2.50, 0])
        self.play(swap(pip_lab, pip2_lab, run_time=0.7), pten.animate.move_to([5.15, 1.15, 0]), run_time=1.4)

        # Beat 4: With its address gone, Akt leaves and loses both phosphates
        self.at("with its address")
        self.play(akt.animate.move_to([2.25, -0.60, 0]), run_time=1.4)
        self.at("leaves and loses")
        self.play(
            FadeOut(akt.p1, shift=UP * 0.15),
            FadeOut(akt.p2, shift=UP * 0.15),
            akt.body.animate.set_stroke(AKT_MUTED, 2.8).set_fill(AKT_MUTED, 0.26),
            akt.lab.animate.set_color(TARGET_OFF),
            run_time=2.4,
        )

        # Beat 5: Downstream kinases mark IRS-1 on serines, making it a poorer landing pad for PI 3-kinase
        self.at("downstream kinases")
        kin_box = boxed_label("downstream kinases", SER_FEEDBACK, size=24, box=(2.75, 0.56), fill_opacity=0.28).move_to([2.25, -2.15, 0])
        fb_arc = CurvedArrow(kin_box.get_left() + LEFT * 0.08,
                             irs.box.get_bottom() + DOWN * 0.12,
                             angle=-0.38, color=SER_FEEDBACK, stroke_width=3.6)
        self.play(FadeIn(kin_box), Create(fb_arc), run_time=1.6)

        ser1 = p_badge("Ser-P", fill=SER_FEEDBACK, text_color=BG, size=22).move_to([-3.45, 1.46, 0])
        ser2 = p_badge("Ser-P", fill=SER_FEEDBACK, text_color=BG, size=22).move_to([-2.35, 1.46, 0])
        self.play(
            FadeIn(ser1, scale=0.6), FadeIn(ser2, scale=0.6),
            irs.box.animate.set_stroke(TARGET_OFF, 2.2).set_fill(IRS_TEAL, 0.12),
            irs.label.animate.set_color(TARGET_OFF),
            run_time=1.4,
        )

        self.at("poorer landing pad")
        fail_x = x_badge().move_to([-1.78, 0.78, 0])
        fail_lab = boxed_label("Ser-P IRS-1 ✕ PI3K", SER_FEEDBACK, size=24, fill_opacity=0.22).move_to([-4.35, -0.85, 0])
        self.play(pi3k.animate.move_to([-0.55, 0.65, 0]), run_time=0.8)
        self.play(FadeIn(fail_x, scale=0.5), FadeIn(fail_lab), run_time=0.6)
        self.play(
            pi3k.animate.move_to([-0.25, -0.45, 0]),
            pi3k.box.animate.set_stroke(TARGET_OFF, 2.2).set_fill(PI3K_BLUE, 0.12),
            pi3k.label.animate.set_color(TARGET_OFF),
            run_time=1.4,
        )
        self.finish()


def build_predict_backdrop():
    """Shared backdrop for end of S07PredictQ and whole S08Pause."""
    title = T("Muscle & fat (test)", size=30, color=TEXT, weight=BOLD).move_to([-4.2, 3.25, 0])
    tag = T("schematic", size=24, color=GREY).move_to([5.5, 3.25, 0])
    stage = build_muscle_fat_zone(mutated=True)
    return VGroup(title, tag, stage)


class S07PredictQ(SpokenScene):
    def construct(self):
        title = T("Muscle & fat (test)", size=30, color=TEXT, weight=BOLD).move_to([-4.2, 3.25, 0])
        tag = T("schematic", size=24, color=GREY).move_to([5.5, 3.25, 0])
        stage = build_muscle_fat_zone(mutated=False)
        xs = np.linspace(-0.7, 2.3, 8)
        pip2_tiles = pip_tiles(xs, y=1.68, active_mask=[False] * 8, tile_w=0.38, tile_h=0.22)
        pip2_lab = T("PIP2", size=24, color=PIP2_SLATE).move_to([0.8, 2.50, 0])
        akt_rest = akt_shape(pos=[3.35, 0.05, 0], active=False, with_p=False)
        self.add(title, tag, stage.memb, stage.memb_lab, pip2_tiles, pip2_lab, akt_rest)

        self.at("test the pattern")
        self.play(LaggedStart(*[FadeIn(v, shift=UP * 0.10) for v in stage.vesicles], lag_ratio=0.14),
                  FadeIn(stage.glut_lab), run_time=2.0)
        self.play(FadeIn(stage.as160), Create(stage.tethers), run_time=2.0)

        # Beat 1: AS160 is mutated so Akt can no longer phosphorylate it
        self.at("is mutated")
        mut_lab = T("AS160 mutant", size=26, color=TARGET_INDIGO).move_to(stage.as160.label)
        xm = x_badge().next_to(stage.as160.box, RIGHT, buff=0.14)
        self.play(swap(stage.as160.label, mut_lab, run_time=0.7), FadeIn(xm, scale=0.5), run_time=1.2)

        self.at("can no longer")
        # Route probe_p cleanly right of AS160 mutant above xm
        probe_p = p_badge("P").move_to([2.05, 0.35, 0])
        self.play(FadeIn(probe_p), run_time=0.4)
        self.play(probe_p.animate.move_to(xm.get_top() + UP * 0.28), run_time=1.0)
        self.play(probe_p.animate.shift(UP * 0.28).set_opacity(0.0), run_time=1.0)
        self.remove(probe_p)

        # Beat 2: When insulin arrives, what happens to glucose uptake?
        self.at("when insulin arrives")
        self.play(
            LaggedStart(*[Transform(pip2_tiles[i], stage.tiles[i]) for i in range(len(xs))], lag_ratio=0.08),
            swap(pip2_lab, stage.pip_lab, run_time=0.5),
            akt_rest.body.animate.move_to([0.8, 0.52, 0]).set_stroke(AKT_CORAL, 3.8).set_fill(AKT_CORAL, 0.38),
            akt_rest.lab.animate.move_to([0.8, 0.52, 0]).set_color(TEXT),
            run_time=0.90,
        )
        self.play(FadeIn(stage.akt.p1, scale=0.6), FadeIn(stage.akt.p2, scale=0.6), run_time=0.45)
        self.remove(pip2_tiles, akt_rest)
        self.add(stage.tiles, stage.akt)

        self.at("what happens")
        q = question_card("Akt cannot mark AS160: what happens to glucose uptake?", y=-3.05, max_w=10.2)
        self.play(FadeIn(q.question, shift=UP * 0.1), run_time=1.8)
        self.finish()


class S08Pause(PredictPause):
    QUESTION = "Akt cannot mark AS160: what happens to glucose uptake?"
    CARD = {"y": -3.05, "max_w": 10.2}
    SECONDS = 4.5

    def backdrop(self):
        return build_predict_backdrop()


class S09PredictReveal(SpokenScene):
    def construct(self):
        bd = build_predict_backdrop()
        stage = bd[2]
        self.add(bd)

        # Beat 1: Fewer vesicles reach the surface, so uptake rises much less, though Akt itself is active
        self.at("fewer vesicles")
        fusor = stage.vesicles[4]
        self.play(fusor.animate.move_to([4.0, 1.32, 0]), run_time=1.4)
        door = membrane_glut4_door(4.0, y=1.98)
        self.play(FadeOut(fusor), FadeIn(door), run_time=0.5)
        stage.vesicles.remove(fusor)
        self.remove(fusor)

        self.at("rises much less")
        uptake_lab = boxed_label("Uptake rises less", GLUT_EMERALD, size=26, box=(2.85, 0.56), fill_opacity=0.28).move_to([4.25, -2.32, 0])
        akt_on_lab = T("Akt active", size=24, color=AKT_CORAL).move_to([-2.4, 0.52, 0])
        self.play(FadeIn(uptake_lab), FadeIn(akt_on_lab), run_time=0.4)

        trickle_t = ValueTracker(0.0)
        trickle = always_redraw(lambda: VGroup(*[
            Dot([4.0, 2.75 - ((trickle_t.get_value() + i * 0.35) % 1.0) * 3.8, 0], radius=0.10, color=GLUT_EMERALD)
            for i in range(3)
        ]))
        self.add(trickle)
        rem1 = max(0.8, self.t_of("push the whole relay") - 0.3 - self.elapsed())
        self.play(trickle_t.animate.set_value(1.2), run_time=rem1, rate_func=linear)
        self.remove(trickle)

        # Beat 2: Push the whole relay both ways -> introduce Stuck on / Turned down split
        self.at("push the whole relay")
        self.play(FadeOut(bd), FadeOut(door), FadeOut(uptake_lab), FadeOut(akt_on_lab), run_time=0.35)
        tp = TwoPanel("Stuck on (cancer)", "Turned down (insulin resistance)",
                      colors=(AKT_CORAL, SER_FEEDBACK), top=3.15, bottom=-2.95, gap=0.4, width=12.8, size=30)
        tag = scope_tag("schematic")

        l_cx = tp.area("left")[0][0]
        l_memb = bilayer(y=1.45, x0=l_cx - 2.65, x1=l_cx + 2.65, thickness=0.28)
        r_cx = tp.area("right")[0][0]
        r_memb = bilayer(y=1.45, x0=r_cx - 2.65, x1=r_cx + 2.65, thickness=0.28)
        self.play(FadeIn(tp), FadeIn(tag), FadeIn(l_memb), FadeIn(r_memb), run_time=1.3)

        # Beat 3: Lose the eraser PTEN, or mutate PI 3-kinase, and growth signals lock on in tumours
        self.at("lose the eraser")
        l_sub = T("PTEN lost / PIK3CA mutant", size=24, color=AKT_CORAL).move_to([l_cx, 2.05, 0])
        l_pi3k = boxed_label("PI 3-kinase (active)", PI3K_BLUE, size=24, box=(2.75, 0.52), fill_opacity=0.28).move_to([l_cx - 1.25, 0.44, 0])
        l_pten = boxed_label("PTEN lost", TARGET_OFF, size=24, box=(1.45, 0.52), fill_opacity=0.24).move_to([l_cx + 1.80, 0.44, 0])
        l_tiles = pip_tiles(np.linspace(l_cx - 2.1, l_cx + 2.1, 9), y=1.16, active_mask=[True] * 9, tile_w=0.42, tile_h=0.22)
        self.play(FadeIn(l_sub), FadeIn(l_pi3k), FadeIn(l_pten), FadeIn(l_tiles), run_time=1.6)

        self.at("mutate")
        l_akt1 = akt_shape(pos=[l_cx - 1.0, -0.75, 0], active=True, with_p=True, width=1.25, height=0.58, text_size=26, p_size=22)
        l_akt2 = akt_shape(pos=[l_cx + 1.0, -0.75, 0], active=True, with_p=True, width=1.25, height=0.58, text_size=26, p_size=22)
        l_arr1 = clean_arrow(l_akt1.body.get_bottom(), [l_cx - 1.0, -1.68, 0], color=AKT_CORAL, buff=0.06)
        l_arr2 = clean_arrow(l_akt2.body.get_bottom(), [l_cx + 1.0, -1.68, 0], color=AKT_CORAL, buff=0.06)
        l_grow = T("abundant PIP3 & active Akt", size=24, color=PIP3_GOLD).move_to([l_cx, -1.96, 0])
        self.play(FadeIn(l_akt1), FadeIn(l_akt2), FadeIn(l_arr1), FadeIn(l_arr2), FadeIn(l_grow), run_time=1.5)

        self.at("growth signals")
        l_side_note = T("Growth factors: survival, growth", size=24, color=TEXT).move_to([l_cx, -2.50, 0])
        self.play(
            l_arr1.animate.set_stroke(AKT_CORAL, 5.2), l_arr2.animate.set_stroke(AKT_CORAL, 5.2),
            l_akt1.body.animate.set_fill(AKT_CORAL, 0.48), l_akt2.body.animate.set_fill(AKT_CORAL, 0.48),
            FadeIn(l_side_note),
            run_time=1.6,
        )

        # Beat 4: Overdo serine feedback, and insulin resistance weakens the same relay
        self.at("serine feedback")
        r_irs = boxed_label("IRS-1", IRS_TEAL, size=24, box=(1.45, 0.52), fill_opacity=0.28).move_to([r_cx - 1.55, 0.05, 0])
        r_ser1 = p_badge("Ser-P", fill=SER_FEEDBACK, text_color=BG, size=22).move_to([r_cx - 2.05, 0.64, 0])
        r_ser2 = p_badge("Ser-P", fill=SER_FEEDBACK, text_color=BG, size=22).move_to([r_cx - 1.00, 0.64, 0])
        r_pi3k = boxed_label("PI 3-kinase", PI3K_BLUE, size=22, box=(1.65, 0.48), fill_opacity=0.16).move_to([r_cx + 1.05, 0.35, 0])
        r_tiles = pip_tiles(np.linspace(r_cx - 2.1, r_cx + 2.1, 9), y=1.16,
                            active_mask=[False, False, False, False, True, False, False, False, False],
                            tile_w=0.42, tile_h=0.22)
        r_akt = akt_shape(pos=[r_cx + 0.8, -0.82, 0], active=False, with_p=False, width=1.25, height=0.58, text_size=26)
        fb_arrow = clean_arrow([r_cx - 1.55, -0.95, 0], r_irs.box.get_bottom(), color=SER_FEEDBACK, buff=0.06)
        fb_src = T("serine feedback", size=22, color=SER_FEEDBACK).next_to(fb_arrow, DOWN, buff=0.08)
        r_side_note = fit_text("Excess nutrients, inflammation → more serine feedback",
                               max_w=5.7, size=22, color=SER_FEEDBACK, max_lines=2).move_to([r_cx, -2.50, 0])
        self.play(
            FadeIn(r_irs), FadeIn(r_pi3k), FadeIn(r_tiles), FadeIn(r_akt),
            FadeIn(r_ser1, scale=0.6), FadeIn(r_ser2, scale=0.6),
            GrowArrow(fb_arrow), FadeIn(fb_src), FadeIn(r_side_note),
            run_time=1.5,
        )

        self.at("insulin resistance")
        r_note = T("sparse PIP3, muted Akt", size=24, color=TARGET_OFF).move_to([r_cx, -1.85, 0])
        self.play(
            r_irs.box.animate.set_stroke(TARGET_OFF, 2.2).set_fill(IRS_TEAL, 0.12),
            r_irs.label.animate.set_color(TARGET_OFF),
            r_pi3k.box.animate.set_stroke(TARGET_OFF, 2.2).set_fill(PI3K_BLUE, 0.10),
            r_akt.animate.shift(DOWN * 0.25),
            FadeIn(r_note),
            run_time=2.2,
        )
        self.finish()


class S10Closing(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic")
        memb = bilayer(y=1.98, x0=-6.3, x1=6.3, thickness=0.34)
        rec = insulin_receptor(x=-4.9, y=1.98, bound=True)
        irs = irs1_block(pos=(-3.0, 0.85, 0), tyr_p=True)
        pi3k = pi3k_block(pos=(-0.95, 0.90, 0))
        pten = pten_block(pos=(4.95, 0.85, 0))

        # Computed ODE-driven PIP3 fraction: dp/dt = k_on*(1-p) - k_off*p
        pip3_level = ValueTracker(0.50)
        xs = np.linspace(0.45, 3.65, 8)

        def mk_tiles():
            n_on = int(round(np.clip(pip3_level.get_value(), 0.0, 1.0) * len(xs)))
            return pip_tiles(xs, y=1.68, active_mask=[i < n_on for i in range(len(xs))], tile_w=0.38, tile_h=0.22)

        tiles = always_redraw(mk_tiles)
        akt = akt_shape(pos=[2.05, 0.52, 0], active=True, with_p=True)
        akt_base = akt.get_center().copy()
        akt.add_updater(lambda m: m.move_to(akt_base + DOWN * (0.40 * max(0.0, 0.45 - pip3_level.get_value()))))

        targets = [
            ("Muscle: GLUT4", -4.75, 2.35, GLUT_EMERALD),
            ("Fat: GLUT4", -2.15, 2.05, GLUT_EMERALD),
            ("Liver: glycogen, FOXO1", 1.15, 3.65, TARGET_INDIGO),
            ("Growing cells", 4.55, 2.35, AKT_CORAL),
        ]
        t_chips = VGroup(*[boxed_label(txt, col, size=24, box=(bw, 0.56), fill_opacity=0.28).move_to([x, -1.78, 0])
                           for txt, x, bw, col in targets])
        arrow_op = ValueTracker(1.0)
        t_arrows_live = VGroup(*[
            always_redraw(lambda c=c: clean_arrow(
                akt.body.get_bottom(), c.box.get_top(), color=AKT_CORAL, stroke_width=2.8, buff=0.08
            ).set_opacity(arrow_op.get_value()))
            for c in t_chips
        ])

        bal_lab = T("PIP3 balance", size=24, color=PIP3_GOLD).move_to([5.05, 2.88, 0])
        bal_bg = RoundedRectangle(corner_radius=0.08, width=1.9, height=0.28,
                                  stroke_color=GREY, stroke_width=2.2, fill_opacity=0.16).move_to([5.05, 2.52, 0])
        bal_fill = always_redraw(lambda: Rectangle(
            width=max(0.06, 1.82 * np.clip(pip3_level.get_value(), 0.02, 1.0)), height=0.20,
            fill_color=AKT_CORAL if pip3_level.get_value() > 0.78 else (SER_FEEDBACK if pip3_level.get_value() < 0.25 else PIP3_GOLD),
            fill_opacity=0.94, stroke_width=0
        ).move_to([5.05 - 0.91 + max(0.06, 1.82 * np.clip(pip3_level.get_value(), 0.02, 1.0)) / 2, 2.52, 0]))

        self.add(tag, memb, rec, irs, pi3k, pten, tiles, akt, bal_lab, bal_bg, bal_fill)

        # Beat 1: One kinase directs muscle, fat, liver, and growing cells
        self.at("one kinase directs")
        static_arrows = []
        for idx, c in enumerate(t_chips):
            arr = clean_arrow(akt.body.get_bottom(), c.box.get_top(), color=AKT_CORAL, stroke_width=2.8, buff=0.08)
            static_arrows.append(arr)
            self.play(FadeIn(c, shift=UP * 0.12),
                      GrowArrow(arr),
                      pip3_level.animate.set_value(0.62 if idx % 2 == 0 else 0.48),
                      run_time=1.4)
        self.remove(*static_arrows)
        self.add(t_arrows_live)
        self.play(pip3_level.animate.set_value(0.56), run_time=2.2)

        # Beat 2: Lose an eraser and the signal locks on
        self.at("lose an eraser")
        status = T("PTEN lost: signal locks on", size=26, color=AKT_CORAL).move_to([0.0, -2.70, 0])
        self.play(
            pten.box.animate.set_stroke(opacity=0.28).set_fill(opacity=0.06),
            pten.label.animate.set_opacity(0.28),
            FadeIn(status),
            pip3_level.animate.set_value(1.0),
            run_time=2.8,
        )

        # Beat 3: Overdrive feedback and the cell responds weakly to insulin
        self.at("overdrive feedback")
        status_fb = T("Overdriven feedback: weak response", size=26, color=SER_FEEDBACK).move_to([0.0, -2.70, 0])
        fb_arc = CurvedArrow(akt.body.get_left() + LEFT * 0.10 + DOWN * 0.15,
                             irs.box.get_bottom() + DOWN * 0.10,
                             angle=-0.34, color=SER_FEEDBACK, stroke_width=3.6)
        ser_badge = place_badge_above_left(p_badge("Ser-P", fill=SER_FEEDBACK, text_color=BG, size=22),
                                           irs.box, dx=0.22, gap=0.09)
        self.play(
            pten.box.animate.set_stroke(opacity=1.0).set_fill(opacity=0.28),
            pten.label.animate.set_opacity(1.0),
            irs.box.animate.set_stroke(SER_FEEDBACK, 3),
            irs.tp.animate.set_opacity(0.25),
            akt.body.animate.set_stroke(AKT_MUTED, 2.8).set_fill(AKT_MUTED, 0.26),
            akt.lab.animate.set_color(TARGET_OFF),
            akt.p1.animate.set_opacity(0.25),
            akt.p2.animate.set_opacity(0.25),
            arrow_op.animate.set_value(0.28),
            Create(fb_arc),
            FadeIn(ser_badge, scale=0.6),
            swap(status, status_fb, run_time=0.6),
            pip3_level.animate.set_value(0.15),
            run_time=3.0,
        )

        # Beat 4: Healthy signaling pairs active Akt with reliable erasers and negative feedback
        self.at("healthy signaling")
        status_ok = T("Balanced: active Akt + erasers + feedback", size=26, color=PTEN_MINT).move_to([0.0, -2.70, 0])
        self.play(
            irs.box.animate.set_stroke(IRS_TEAL, 2.5),
            irs.tp.animate.set_opacity(1.0),
            fb_arc.animate.set_stroke(opacity=0.65),
            ser_badge.animate.set_opacity(0.65),
            akt.body.animate.set_stroke(AKT_CORAL, 3.8).set_fill(AKT_CORAL, 0.38),
            akt.lab.animate.set_color(TEXT),
            akt.p1.animate.set_opacity(1.0),
            akt.p2.animate.set_opacity(1.0),
            arrow_op.animate.set_value(1.0),
            swap(status_fb, status_ok, run_time=0.6),
            pip3_level.animate.set_value(0.55),
            run_time=2.8,
        )

        self.at("and negative feedback")
        self.play(pip3_level.animate.set_value(0.42), fb_arc.animate.set_stroke(opacity=0.85), run_time=0.9)
        self.play(pip3_level.animate.set_value(0.52), fb_arc.animate.set_stroke(opacity=0.65), run_time=0.8)
        self.finish()


class S11End(EndCard):
    LINE = "Akt phosphorylates tissue-specific targets, while erasers and feedback limit the signal."
