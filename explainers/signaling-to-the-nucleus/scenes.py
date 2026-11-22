"""
COLOUR MAP (one colour per concept for the whole film):
    PHOSPHATE    = "#F59E0B"  # amber-gold phosphate dots ('P')
    CAMP_PKA     = "#FB7185"  # coral-orange cAMP / PKA
    CA_CALC      = "#22D3EE"  # cyan-teal calcium / CaM / CaMKIV / calcineurin
    CREB_COL     = "#A78BFA"  # violet-purple CREB
    CBP_COL      = "#34D399"  # emerald-green CBP (KIX) & acetyl marks
    NFAT_COL     = "#38BDF8"  # sky-blue NFAT
    IMPORT_COL   = "#84CC16"  # lime-green nuclear entry tag
    DRUG_COL     = "#EF4444"  # crimson transplant drugs & helper protein clamp
    MRNA_COL     = "#6EE7B7"  # mint c-fos / target mRNA ribbon
    MEMBRANE_COL = "#64748B"  # slate-blue plasma membrane & nuclear envelope
    DNA_COL      = "#E2E8F0"  # bright white DNA bar
    RNAP_COL     = "#D4A843"  # gold RNA polymerase & question prompt highlight

CARRIED WORLD:
    2D cross-section of one living cell: slate-blue plasma membrane arc on the left,
    warm dark cytosol in the center, dashed nuclear envelope with an open nuclear pore
    opening into a deep-indigo nucleus on the right, and a horizontal white DNA bar
    along the lower nucleus. Scenes zoom smoothly between the full cell and the
    nuclear compartment, rebuilding carried objects in the same coordinates.

WHAT CHANGES IN EACH SPOKEN SCENE:
    s01_hook:             Ribosome gets crossed out; signal strikes membrane receptor and
                          computed mint c-fos mRNA ribbons grow continuously off DNA while
                          a '?' switch flips to ON.
    s02_creb_waiting:     View zooms into nucleus; generic factor binds DNA; slow transcription+
                          translation bar fills then transforms into fast pre-made CREB dimer on CRE.
    s03_camp_pka_cbp:     Coral cAMP dots rise, free PKA blocks that glide through the pore and
                          snap 'P' onto CREB Ser 133; CBP KIX crescent glides over, cups 'P',
                          uncoils computed histone loops, and recruits RNA pol to grow mRNA.
    s04_calcium_converge: Cyan Ca2+ streams through membrane channel, binds CaM ring, activates
                          nuclear CaMKIV to put 'P' on CREB Ser 133; ERK and PKA signal pulses
                          converge on 'P' before CBP docks onto 'P'.
    s05_nfat_setup:       View pans out to full cell; 12 amber 'P' dots shield sky-blue NFAT's
                          lime Import tag, and NFAT drifts to the nuclear envelope and bounces off.
    s06_predict_prompt:   T-cell receptor fires; continuous Ca2+ stream flows as cyan Calcineurin
                          approaches NFAT and the predict question card enters below.
    s08_nfat_reveal:      Calcineurin sweeps NFAT, popping 12 'P' dots off; exposed Import tag
                          glows as NFAT glides through the pore onto DNA to grow mRNA, then exits
                          when kinases restore 'P' dots after Ca2+ drops.
    s09_drugs:            Crimson Drug pill fails to block Calcineurin alone, joins Helper wedge
                          into a clamp beside the open active notch, and physically blocks grey
                          Protein substrate from reaching the notch.
    s10_return_cfos:      Full cell shows both switches active side by side (CREB +1 P with CBP,
                          NFAT -12 P entering through pore) as mint c-fos mRNA surges off DNA
                          beside the stopped ribosome.
"""
from bp_parts import *

# Film colour map
PHOSPHATE = "#F59E0B"
CAMP_PKA = "#FB7185"
CA_CALC = "#22D3EE"
CREB_COL = "#A78BFA"
CBP_COL = "#34D399"
NFAT_COL = "#38BDF8"
IMPORT_COL = "#84CC16"
DRUG_COL = "#EF4444"
MRNA_COL = "#6EE7B7"
MEMBRANE_COL = "#64748B"
CYTOSOL_FILL = "#141822"
NUCLEUS_FILL = "#262C60"
DNA_COL = "#E2E8F0"
RNAP_COL = GOLD


# ------------------------------------------------------------------ shared builders
def make_dashed_envelope(x, y_top, y_bot, pore_y=0.0, pore_half=0.78):
    """Dashed nuclear envelope with an open pore gap around pore_y so moving shapes pass clear."""
    parts = VGroup()
    if y_top > pore_y + pore_half + 0.15:
        parts.add(DashedLine([x, y_top, 0], [x, pore_y + pore_half, 0],
                             color=MEMBRANE_COL, stroke_width=5.5, dash_length=0.24, dashed_ratio=0.58))
    if pore_y - pore_half - 0.15 > y_bot:
        parts.add(DashedLine([x, pore_y - pore_half, 0], [x, y_bot, 0],
                             color=MEMBRANE_COL, stroke_width=5.5, dash_length=0.24, dashed_ratio=0.58))
    for dy in (pore_half, -pore_half):
        parts.add(Line([x - 0.16, pore_y + dy, 0], [x + 0.16, pore_y + dy, 0],
                       color=MEMBRANE_COL, stroke_width=5.5))
    return parts


def make_dna_bar(x0, x1, y, cre_x=None):
    """Bright white double-rail DNA bar with schematic base-pair rungs and optional CRE highlight."""
    g = VGroup()
    r1 = Line([x0, y + 0.09, 0], [x1, y + 0.09, 0], color=DNA_COL, stroke_width=5)
    r2 = Line([x0, y - 0.09, 0], [x1, y - 0.09, 0], color=DNA_COL, stroke_width=5)
    g.add(r1, r2)
    rx = x0 + 0.25
    while rx < x1 - 0.2:
        g.add(Line([rx, y - 0.09, 0], [rx, y + 0.09, 0], color=DNA_COL, stroke_width=2.2))
        rx += 0.36
    if cre_x is not None:
        cre_bar = Line([cre_x - 0.90, y, 0], [cre_x + 0.90, y, 0], color=RNAP_COL, stroke_width=8)
        g.add(cre_bar)
        g.cre_bar = cre_bar
    return g


def build_full_cell(y_top=3.30, y_bot=-2.45, env_x=0.65, pore_y=-0.1, dna_y=-1.55,
                    show_labels=True, dna_cre=False):
    """Carried 2D cell cross-section: plasma membrane left, cytosol center, nucleus right."""
    h = y_top - y_bot
    cy = (y_top + y_bot) / 2
    mem_x = -5.75
    right_x = 6.30

    cyto_bg = Rectangle(width=env_x - mem_x, height=h, stroke_width=0,
                        fill_color=CYTOSOL_FILL, fill_opacity=0.85).move_to([(mem_x + env_x) / 2, cy, 0])
    nuc_bg = RoundedRectangle(corner_radius=0.35, width=right_x - env_x, height=h,
                              stroke_width=0,
                              fill_color=NUCLEUS_FILL, fill_opacity=0.95).move_to([(env_x + right_x) / 2, cy, 0])
    p_top = np.array([mem_x + 0.35, y_top, 0])
    p_bot = np.array([mem_x + 0.35, y_bot, 0])
    membrane = ArcBetweenPoints(p_bot, p_top, angle=-0.36, color=MEMBRANE_COL, stroke_width=8.5)
    envelope = make_dashed_envelope(env_x, y_top - 0.1, y_bot + 0.1, pore_y=pore_y, pore_half=0.78)
    dna = make_dna_bar(env_x + 0.45, right_x - 0.3, dna_y, cre_x=(env_x + 1.85 if dna_cre else None))

    g = VGroup(cyto_bg, nuc_bg, membrane, envelope, dna)
    g.membrane = membrane
    g.envelope = envelope
    g.dna = dna
    g.env_x = env_x
    g.pore_y = pore_y
    g.dna_y = dna_y
    g.mem_x = mem_x
    if show_labels:
        lbl_cyto = T("Cytosol", 28, TEXT).move_to([(mem_x + env_x) / 2, y_top - 0.34, 0])
        lbl_nuc = T("Nucleus", 28, TEXT).move_to([(env_x + right_x) / 2, y_top - 0.34, 0])
        g.add(lbl_cyto, lbl_nuc)
        g.lbl_cyto = lbl_cyto
        g.lbl_nuc = lbl_nuc
    return g


def build_nuclear_view(env_x=-2.3, mem_x=None, y_top=3.30, y_bot=-2.65, dna_y=-1.60,
                       cre_x=0.35, show_labels=True):
    """Carried zoomed-in nuclear view: nuclear envelope on left, deep-indigo nucleus filling right."""
    h = y_top - y_bot
    cy = (y_top + y_bot) / 2
    right_x = 6.30
    left_x = -6.30

    cyto_bg = Rectangle(width=env_x - left_x, height=h, stroke_width=0,
                        fill_color=CYTOSOL_FILL, fill_opacity=0.85).move_to([(left_x + env_x) / 2, cy, 0])
    nuc_bg = RoundedRectangle(corner_radius=0.32, width=right_x - env_x, height=h,
                              stroke_width=0,
                              fill_color=NUCLEUS_FILL, fill_opacity=0.95).move_to([(env_x + right_x) / 2, cy, 0])
    envelope = make_dashed_envelope(env_x, y_top - 0.1, y_bot + 0.1, pore_y=0.0, pore_half=0.82)
    dna = make_dna_bar(env_x + 0.45, right_x - 0.3, dna_y, cre_x=cre_x)

    g = VGroup(cyto_bg, nuc_bg, envelope, dna)
    if mem_x is not None:
        mem_top = Line([mem_x, y_top, 0], [mem_x, 0.48, 0], color=MEMBRANE_COL, stroke_width=8)
        mem_bot = Line([mem_x, -0.48, 0], [mem_x, y_bot, 0], color=MEMBRANE_COL, stroke_width=8)
        chan_top = Line([mem_x - 0.20, 0.48, 0], [mem_x + 0.20, 0.48, 0], color=CA_CALC, stroke_width=6)
        chan_bot = Line([mem_x - 0.20, -0.48, 0], [mem_x + 0.20, -0.48, 0], color=CA_CALC, stroke_width=6)
        channel = VGroup(mem_top, mem_bot, chan_top, chan_bot)
        g.add(channel)
        g.channel = channel
    if show_labels:
        lbl_cyto = T("Cytosol", 28, TEXT).move_to([((mem_x or left_x) + env_x) / 2, y_top - 0.34, 0])
        lbl_nuc = T("Nucleus", 28, TEXT).move_to([(env_x + right_x) / 2, y_top - 0.34, 0])
        g.add(lbl_cyto, lbl_nuc)
        g.lbl_cyto = lbl_cyto
        g.lbl_nuc = lbl_nuc
    g.envelope = envelope
    g.dna = dna
    g.env_x = env_x
    g.dna_y = dna_y
    return g


def make_receptor(pos):
    """Y-shaped membrane receptor on plasma membrane."""
    x, y, _ = pos
    stem = Line([x - 0.28, y, 0], [x + 0.34, y, 0], color=MEMBRANE_COL, stroke_width=7)
    arm_u = Line([x - 0.28, y, 0], [x - 0.56, y + 0.32, 0], color=MEMBRANE_COL, stroke_width=7)
    arm_d = Line([x - 0.28, y, 0], [x - 0.56, y - 0.32, 0], color=MEMBRANE_COL, stroke_width=7)
    return VGroup(stem, arm_u, arm_d)


def make_ribosome_stopped(pos):
    """Schematic two-subunit ribosome with a bold crimson X and clear label below."""
    x, y, _ = pos
    large = RoundedRectangle(corner_radius=0.22, width=1.15, height=0.54,
                             stroke_color=TEXT, stroke_width=3.5, fill_color=TEXT, fill_opacity=0.20).move_to([x, y + 0.23, 0])
    small = RoundedRectangle(corner_radius=0.16, width=0.86, height=0.36,
                             stroke_color=TEXT, stroke_width=3.5, fill_color=TEXT, fill_opacity=0.20).move_to([x, y - 0.25, 0])
    strand = Line([x - 0.85, y - 0.02, 0], [x + 0.85, y - 0.02, 0], color=TEXT, stroke_width=3)
    x1 = Line([x - 0.56, y - 0.46, 0], [x + 0.56, y + 0.52, 0], color=DRUG_COL, stroke_width=7)
    x2 = Line([x - 0.56, y + 0.52, 0], [x + 0.56, y - 0.46, 0], color=DRUG_COL, stroke_width=7)
    cross = VGroup(x1, x2)
    cross.layout_ok = True
    icon = VGroup(strand, large, small, cross)
    lbl = T("Ribosomes stopped", 28, DRUG_COL, weight=BOLD).next_to(icon, DOWN, buff=0.22)
    g = VGroup(icon, lbl)
    g.icon = icon
    g.cross = cross
    g.label = lbl
    return g


def make_p_dot(radius=0.22, font_size=22):
    """Amber-gold phosphate badge ('P') with comfortable padding."""
    c = Circle(radius=radius, stroke_color=PHOSPHATE, stroke_width=3.5,
               fill_color=PHOSPHATE, fill_opacity=0.30)
    t = T("P", font_size, PHOSPHATE, weight=BOLD).move_to(c)
    return VGroup(c, t)


def make_creb_pair(pos):
    """Two-lobed violet CREB dimer block parked on DNA, with seam ticks clear of letters."""
    x, y, _ = pos
    body = RoundedRectangle(corner_radius=0.24, width=2.05, height=1.00,
                            stroke_color=CREB_COL, stroke_width=4,
                            fill_color=CREB_COL, fill_opacity=0.28).move_to([x, y, 0])
    tick_top = Line([x, y + 0.50, 0], [x, y + 0.30, 0], color=CREB_COL, stroke_width=3.5)
    tick_bot = Line([x, y - 0.50, 0], [x, y - 0.30, 0], color=CREB_COL, stroke_width=3.5)
    lbl = T("CREB", 28, CREB_COL, weight=BOLD).move_to(body)
    g = VGroup(body, tick_top, tick_bot, lbl)
    g.body = body
    g.p_spot = body.get_top() + UP * 0.34
    g.lbl = lbl
    return g


def make_cbp_crescent(size=28):
    """Single-polygon emerald-green CBP with a concave bottom KIX pocket and VectorizedPoint anchor."""
    pts = [
        [-1.35, 1.24, 0],
        [1.35, 1.24, 0],
        [1.35, 0.00, 0],
        [0.48, 0.00, 0],
        [0.40, 0.62, 0],
        [-0.40, 0.62, 0],
        [-0.48, 0.00, 0],
        [-1.35, 0.00, 0],
    ]
    poly = Polygon(*pts, stroke_color=CBP_COL, stroke_width=4,
                   fill_color=CBP_COL, fill_opacity=0.28)
    lbl = T("CBP (KIX)", size, CBP_COL, weight=BOLD).move_to([0.0, 0.92, 0])
    cup_anchor = VectorizedPoint([0.0, 0.26, 0.0])
    g = VGroup(poly, lbl, cup_anchor)
    g.poly = poly
    g.cup_anchor = cup_anchor
    return g


def make_nfat_block(pos, body_w=1.70, body_h=1.18, font_size=28, tag_size=24):
    """Sky-blue NFAT block with an adjacent lime-green 'Import tag' badge (non-overlapping)."""
    x, y, _ = pos
    body = RoundedRectangle(corner_radius=0.18, width=body_w, height=body_h,
                            stroke_color=NFAT_COL, stroke_width=4,
                            fill_color=NFAT_COL, fill_opacity=0.28).move_to([x, y, 0])
    lbl = T("NFAT", font_size, NFAT_COL, weight=BOLD).move_to(body)
    tag = boxed_label("Import tag", IMPORT_COL, size=tag_size, pad=0.14).next_to(body, RIGHT, buff=0.14)
    g = VGroup(body, lbl, tag)
    g.body = body
    g.tag = tag
    return g


def make_nfat_phosphates(nfat_group):
    """Twelve amber-gold 'P' circles forming a non-overlapping outer shield around 'Import tag'."""
    c = nfat_group.tag.get_center()
    offsets = [
        (-0.66, 0.67), (-0.14, 0.67), (0.38, 0.67), (0.90, 0.67),
        (-0.66, -0.67), (-0.14, -0.67), (0.38, -0.67), (0.90, -0.67),
        (1.24, 0.27), (1.24, -0.27), (1.76, 0.50), (1.76, -0.50),
    ]
    dots = VGroup()
    for dx, dy in offsets:
        p = make_p_dot(radius=0.22, font_size=22).move_to(c + np.array([dx, dy, 0]))
        dots.add(p)
    return dots


def make_calcineurin(pos, scale=1.0, font_size=24):
    """Cyan-teal Calcineurin with a carved active-site notch on the right and clear label on left."""
    x, y, _ = pos
    pts = [
        [-1.85, 0.85, 0],
        [1.05, 0.85, 0],
        [1.05, 0.36, 0],
        [0.42, 0.00, 0],
        [1.05, -0.36, 0],
        [1.05, -0.85, 0],
        [-1.85, -0.85, 0],
    ]
    shell = Polygon(*pts, stroke_color=CA_CALC, stroke_width=4,
                    fill_color=CA_CALC, fill_opacity=0.28).scale(scale).move_to([x, y, 0])
    lbl = T("Calcineurin", font_size, CA_CALC, weight=BOLD).move_to(
        shell.get_center() + LEFT * 0.34 * scale)
    g = VGroup(shell, lbl)
    g.shell = shell
    g.notch_point = shell.get_right() + LEFT * 0.63 * scale
    return g


def make_mrna_ribbon(origin, tracker, max_len=2.5, height=1.35, phase_offset=0.0, stroke_w=6.5):
    """Computed mint mRNA ribbon that grows from origin as tracker goes 0 -> 1."""
    ox, oy, _ = origin

    def mk():
        p = float(np.clip(tracker.get_value(), 0.0, 1.0))
        m = VMobject(stroke_color=MRNA_COL, stroke_width=stroke_w, fill_opacity=0)
        if p < 0.03:
            return m
        n = max(6, int(64 * p))
        s = np.linspace(0.0, p, n)
        xs = ox + s * max_len
        ys = oy + s * height + 0.15 * np.sin(phase_offset + 18.0 * s - 4.0 * p)
        pts = [np.array([xi, yi, 0.0]) for xi, yi in zip(xs, ys)]
        m.set_points_as_corners(pts)
        return m

    return always_redraw(mk)


def make_histone_spools(x_start, y, uncoil_tracker):
    """Three computed histone spools whose spacing and DNA coil loops loosen with uncoil_tracker."""
    def mk():
        u = float(np.clip(uncoil_tracker.get_value(), 0.0, 1.0))
        g = VGroup()
        spacing = 0.78 + 0.44 * u
        for i in range(3):
            cx = x_start + i * spacing
            spool = Circle(radius=0.25, stroke_color=TEXT, stroke_width=3.5,
                           fill_color=TEXT, fill_opacity=0.20).move_to([cx, y + 0.33, 0])
            loop_r = 0.33 - 0.08 * u
            coil = Arc(radius=loop_r, start_angle=-0.2 * PI, angle=(1.45 - 0.65 * u) * PI,
                       arc_center=spool.get_center(), stroke_color=DNA_COL, stroke_width=4.5)
            g.add(spool, coil)
            if u > 0.35:
                ac = T("Ac", 24, CBP_COL, weight=BOLD).move_to([cx, y + 0.80, 0])
                g.add(ac)
        return g

    return always_redraw(mk)


def make_ca_stream(x0, x1, y0, phase_tracker, n=7, radius=0.13):
    """Computed continuous stream of Ca2+ ions drifting horizontally from x0 to x1."""
    def mk():
        ph = phase_tracker.get_value()
        g = VGroup()
        for i in range(n):
            frac = (ph + i / n) % 1.0
            xi = x0 + frac * (x1 - x0)
            yi = y0 + 0.16 * np.sin(2.5 * i + 6.0 * frac)
            g.add(Dot([xi, yi, 0], radius=radius, color=CA_CALC))
        return g

    return always_redraw(mk)


# ------------------------------------------------------------------ scenes
class S00Title(TitleCard):
    LESSON = "Signaling to the Nucleus: CREB, AP-1 and Immediate Early Genes"
    TITLE = "Two Phosphate Switches That Flip Waiting Factors"


class S01Hook(SpokenScene):
    def construct(self):
        cell = build_full_cell(y_top=3.30, y_bot=-2.45, env_x=0.45, pore_y=-0.1, dna_y=-1.55, show_labels=True)
        receptor = make_receptor(np.array([-5.88, -0.1, 0.0]))
        ribo = make_ribosome_stopped(np.array([-2.65, 1.35, 0.0]))

        q_box = boxed_label("? switch", RNAP_COL, size=28).move_to([2.25, cell.dna_y + 0.72, 0])
        q_prompt = T("What was waiting?", 36, RNAP_COL, weight=BOLD).move_to([0.0, -3.12, 0])

        mrna_t = ValueTracker(0.0)
        mrna_1 = make_mrna_ribbon(np.array([3.35, cell.dna_y + 0.25, 0.0]), mrna_t, max_len=2.15, height=1.75)
        mrna_2 = make_mrna_ribbon(np.array([3.70, cell.dna_y + 0.25, 0.0]), mrna_t, max_len=2.0, height=1.25, phase_offset=1.8)
        mrna_lbl = T("c-fos mRNA", 28, MRNA_COL, weight=BOLD).move_to([4.65, 1.15, 0])

        self.add(cell, receptor)

        self.at("resting cell")
        self.play(FadeIn(ribo[0][0:3]), FadeIn(q_box), run_time=1.4)

        self.at("every ribosome stopped")
        self.play(Create(ribo.cross), FadeIn(ribo.label), run_time=1.8)

        self.at("Add a growth factor")
        pulse_dot = Dot([-6.35, -0.1, 0], radius=0.18, color=RNAP_COL)
        self.play(FadeIn(pulse_dot, scale=0.8), run_time=0.3)
        self.play(pulse_dot.animate.move_to([-5.95, -0.1, 0]), run_time=0.7)
        relay = Arrow([-5.35, -0.1, 0], [q_box.get_left()[0] - 0.14, q_box.get_center()[1], 0],
                      color=RNAP_COL, stroke_width=5, buff=0.08)
        relay.layout_ok = True
        self.play(GrowArrow(relay), FadeOut(pulse_dot), run_time=0.9)

        self.at("transcripts still surge")
        self.add(mrna_1, mrna_2)
        self.play(mrna_t.animate.set_value(0.68), FadeIn(mrna_lbl), run_time=3.4, rate_func=linear)

        self.at("already built and waiting")
        self.play(Indicate(q_box, color=RNAP_COL, scale_factor=1.12),
                  FadeIn(q_prompt, shift=UP * 0.15),
                  mrna_t.animate.set_value(0.84), run_time=2.4, rate_func=linear)

        self.at("only had to flip it")
        flipped = boxed_label("ON switch", MRNA_COL, size=28).move_to(q_box)
        self.play(swap(q_box, flipped, run_time=0.8),
                  mrna_t.animate.set_value(1.0), run_time=1.8, rate_func=linear)
        self.finish()


class S02CrebWaiting(SpokenScene):
    def construct(self):
        full_cell = build_full_cell(y_top=3.30, y_bot=-2.45, env_x=0.45, pore_y=-0.1, dna_y=-1.55, show_labels=True)
        nuc_view = build_nuclear_view(env_x=-2.3, y_top=3.30, y_bot=-2.65, dna_y=-1.60, cre_x=0.35, show_labels=True)
        cre_lbl = T("CRE", 28, RNAP_COL, weight=BOLD).move_to([0.35, -2.20, 0])
        gene_lbl = T("Gene", 28, MRNA_COL).move_to([4.0, -2.20, 0])

        self.add(*full_cell)
        self.play(
            ReplacementTransform(full_cell[0], nuc_view[0]),
            ReplacementTransform(full_cell[1], nuc_view[1]),
            FadeOut(full_cell.membrane),
            ReplacementTransform(full_cell.envelope, nuc_view.envelope),
            FadeTransform(full_cell.dna, nuc_view.dna),
            ReplacementTransform(full_cell.lbl_cyto, nuc_view.lbl_cyto),
            ReplacementTransform(full_cell.lbl_nuc, nuc_view.lbl_nuc),
            FadeIn(cre_lbl),
            FadeIn(gene_lbl),
            run_time=1.2,
        )

        self.at("binds a short DNA site")
        generic_tf = boxed_label("Factor", TEXT, size=28).move_to([0.35, 0.85, 0])
        self.play(FadeIn(generic_tf), run_time=0.5)
        self.play(generic_tf.animate.move_to([0.35, -0.90, 0]), run_time=2.8)

        self.at("Making a new factor is slow")
        slow_t = ValueTracker(0.0)
        slow_txt = T("Slow: transcribe + translate", 28, DRUG_COL, weight=BOLD).move_to([1.65, 2.05, 0])
        bar_bg = RoundedRectangle(corner_radius=0.12, width=6.0, height=0.42,
                                  stroke_color=DRUG_COL, stroke_width=3, fill_opacity=0.14).move_to([1.65, 1.38, 0])
        bar_fill = always_redraw(lambda: Rectangle(
            width=max(0.05, 5.9 * slow_t.get_value()), height=0.32, stroke_width=0,
            fill_color=DRUG_COL, fill_opacity=0.72
        ).align_to(bar_bg, LEFT).shift(RIGHT * 0.05).set_y(bar_bg.get_y()))
        self.play(FadeIn(slow_txt), FadeIn(bar_bg), run_time=0.5)
        self.add(bar_fill)
        self.play(slow_t.animate.set_value(0.60), run_time=2.3, rate_func=linear)

        self.at("transcribed and translated")
        self.play(slow_t.animate.set_value(1.0), run_time=2.4, rate_func=linear)

        self.at("Fast pathways modify")
        fast_txt = T("Fast: modify pre-made factor", 28, CREB_COL, weight=BOLD).move_to([1.65, 2.05, 0])
        self.play(FadeOut(bar_bg), FadeOut(bar_fill), FadeOut(slow_txt), run_time=0.5)
        self.play(FadeIn(fast_txt, shift=DOWN * 0.1), run_time=1.8)

        self.at("One waiting factor is CREB")
        creb = make_creb_pair(np.array([0.35, -0.90, 0.0]))
        self.play(ReplacementTransform(generic_tf, creb), run_time=2.2)

        self.at("sits on DNA as a pair")
        rnap_box = RoundedRectangle(corner_radius=0.14, width=1.70, height=0.72,
                                    stroke_color=RNAP_COL, stroke_width=3, stroke_opacity=0.60,
                                    fill_color=RNAP_COL, fill_opacity=0.08).move_to([4.15, 0.72, 0])
        rnap_txt = T("RNA pol", 26, RNAP_COL).set_opacity(0.78).move_to(rnap_box)
        rnap = VGroup(rnap_box, rnap_txt)
        self.play(FadeIn(rnap), creb.animate.move_to([0.35, -0.98, 0]), run_time=2.5)

        self.at("yet stays quiet")
        quiet_lbl = T("Waiting (gene off)", 28, TEXT).move_to([4.15, -0.25, 0])
        self.play(FadeIn(quiet_lbl), rnap.animate.shift(UP * 0.45), run_time=1.8)
        self.finish()


class S03CampPkaCbp(SpokenScene):
    def construct(self):
        nuc_view = build_nuclear_view(env_x=-2.3, y_top=3.30, y_bot=-2.65, dna_y=-1.60, cre_x=-0.15, show_labels=True)
        cre_lbl = T("CRE", 28, RNAP_COL, weight=BOLD).move_to([-0.15, -2.20, 0])
        creb = make_creb_pair(np.array([-0.15, -0.98, 0.0]))
        uncoil_t = ValueTracker(0.0)
        histones = make_histone_spools(3.55, nuc_view.dna_y, uncoil_t)

        rnap_box = RoundedRectangle(corner_radius=0.14, width=1.70, height=0.72,
                                    stroke_color=RNAP_COL, stroke_width=3, stroke_opacity=0.60,
                                    fill_color=RNAP_COL, fill_opacity=0.08).move_to([4.65, 1.55, 0])
        rnap_txt = T("RNA pol", 26, RNAP_COL).set_opacity(0.78).move_to(rnap_box)
        rnap = VGroup(rnap_box, rnap_txt)

        pka_reg = RoundedRectangle(corner_radius=0.18, width=1.65, height=1.22,
                                   stroke_color=CAMP_PKA, stroke_width=3.5,
                                   fill_color=CAMP_PKA, fill_opacity=0.14).move_to([-4.65, 0.15, 0])
        pka_cat = boxed_label("PKA", CAMP_PKA, size=28, box=(1.20, 0.74)).move_to([-4.65, 0.15, 0])
        pka_cat.set_z_index(2)
        camp_lbl = T("cAMP", 28, CAMP_PKA, weight=BOLD).move_to([-4.65, -2.35, 0])

        rng = np.random.default_rng(7)
        camp_dots = VGroup(*[
            Dot([-5.75 + rng.uniform(0.0, 2.2), -1.95 + rng.uniform(0.0, 0.55), 0],
                radius=0.14, color=CAMP_PKA)
            for _ in range(12)
        ])
        camp_dots.set_z_index(1)

        self.add(nuc_view, cre_lbl, creb, histones, rnap, pka_reg, pka_cat)

        self.at("rises")
        self.play(FadeIn(camp_dots), FadeIn(camp_lbl), run_time=0.5)
        self.play(camp_dots.animate.shift(UP * 0.50), run_time=1.0, rate_func=linear)

        self.at("frees")
        self.play(FadeOut(pka_reg), camp_dots.animate.shift(UP * 0.25), run_time=0.8)
        self.play(pka_cat.animate.move_to([-3.25, 0.0, 0]), run_time=1.4)
        self.play(FadeOut(camp_dots), FadeOut(camp_lbl), run_time=0.9)

        self.at("enter the nucleus")
        self.play(pka_cat.animate.move_to([-1.65, 0.0, 0]), run_time=1.3)

        self.at("attach one phosphate")
        p_dot = make_p_dot(radius=0.23, font_size=24).move_to(pka_cat.get_right() + RIGHT * 0.25)
        self.play(pka_cat.animate.move_to([-1.88, -0.25, 0]), FadeIn(p_dot), run_time=0.9)
        self.play(p_dot.animate.move_to(creb.p_spot), run_time=1.1)

        self.at("serine 133")
        ser_lbl = T("Ser 133", 28, PHOSPHATE, weight=BOLD).move_to([2.05, -0.14, 0])
        self.play(pka_cat.animate.move_to([-4.2, 1.5, 0]).set_opacity(0), FadeIn(ser_lbl),
                  Indicate(p_dot, color=PHOSPHATE, scale_factor=1.2), run_time=2.4)
        self.remove(pka_cat)

        self.at("docking handle")
        ring = Circle(radius=0.38, color=PHOSPHATE, stroke_width=4.5).move_to(p_dot)
        cbp = make_cbp_crescent().move_to([1.65, 2.00, 0])
        self.play(Create(ring), FadeIn(cbp), run_time=1.2)
        self.play(FadeOut(ring), cbp.animate.move_to([0.95, 1.75, 0]), run_time=3.2)

        self.at("cannot bind DNA")
        self.play(cbp.animate.move_to([-0.15, 1.75, 0]), run_time=1.9)

        self.at("grips it")
        shift_vec = p_dot.get_center() - cbp.cup_anchor.get_center()
        self.play(cbp.animate.shift(shift_vec), run_time=2.8)

        self.at("adds acetyl groups")
        self.play(uncoil_t.animate.set_value(0.55), run_time=1.4, rate_func=linear)

        self.at("loosen packaged DNA")
        self.play(uncoil_t.animate.set_value(1.0), run_time=1.7, rate_func=linear)

        self.at("calls in RNA polymerase")
        mrna_t = ValueTracker(0.0)
        mrna = make_mrna_ribbon(np.array([2.85, nuc_view.dna_y + 1.05, 0.0]), mrna_t, max_len=2.15, height=1.25)
        self.play(
            rnap_box.animate.set_stroke(opacity=1.0).set_fill(opacity=0.28),
            rnap_txt.animate.set_opacity(1.0),
            rnap.animate.move_to([2.25, nuc_view.dna_y + 0.50, 0]),
            run_time=1.1,
        )
        self.add(mrna)
        self.play(mrna_t.animate.set_value(1.0), run_time=1.6, rate_func=linear)
        self.finish()


class S04CalciumConverge(SpokenScene):
    def construct(self):
        nuc_view = build_nuclear_view(env_x=-2.3, mem_x=-5.9, y_top=3.30, y_bot=-2.65, dna_y=-1.60,
                                      cre_x=1.65, show_labels=True)
        cre_lbl = T("CRE", 28, RNAP_COL, weight=BOLD).move_to([1.65, -2.20, 0])
        creb = make_creb_pair(np.array([1.65, -0.98, 0.0]))

        cam_ring = Circle(radius=0.56, stroke_color=CA_CALC, stroke_width=5.5,
                          fill_color=CA_CALC, fill_opacity=0.18).move_to([-3.85, 0.0, 0])
        cam_lbl = T("CaM", 26, CA_CALC, weight=BOLD).move_to(cam_ring)

        camk_box_rect = RoundedRectangle(corner_radius=0.14, width=1.70, height=0.74,
                                         stroke_color=CA_CALC, stroke_width=3.5, stroke_opacity=0.50,
                                         fill_color=CA_CALC, fill_opacity=0.08).move_to([-0.55, 0.15, 0])
        camk_txt = T("CaMKIV", 28, CA_CALC, weight=BOLD).set_opacity(0.70).move_to(camk_box_rect)
        camk_box = VGroup(camk_box_rect, camk_txt)

        phase = ValueTracker(0.0)
        ca_stream = make_ca_stream(-5.95, -4.35, 0.0, phase, n=9, radius=0.16)
        ca_lbl = T("Ca²⁺", 28, CA_CALC, weight=BOLD).move_to([-4.6, -1.25, 0])

        self.add(nuc_view, cre_lbl, creb, cam_ring, cam_lbl, camk_box)

        self.at("different messenger")
        self.add(ca_stream)
        self.play(FadeIn(ca_lbl), phase.animate.set_value(2.0), run_time=2.6, rate_func=linear)

        self.at("Calcium binds calmodulin")
        bound_dots = VGroup(*[
            Dot(cam_ring.point_at_angle(i * TAU / 6), radius=0.13, color=CA_CALC)
            for i in range(6)
        ])
        self.play(FadeIn(bound_dots, lag_ratio=0.12), phase.animate.set_value(4.0), run_time=2.8, rate_func=linear)

        self.at("nuclear kinase")
        self.remove(ca_stream)
        cam_group = VGroup(cam_ring, cam_lbl, bound_dots)
        self.play(
            cam_group.animate.move_to([-2.45, 0.0, 0]),
            camk_box_rect.animate.set_stroke(opacity=1.0).set_fill(opacity=0.28),
            camk_txt.animate.set_opacity(1.0),
            run_time=2.6,
        )

        self.at("puts a phosphate")
        p_dot = make_p_dot(radius=0.23, font_size=24).move_to([0.90, 0.15, 0])
        self.play(FadeOut(cam_group), FadeOut(ca_lbl), camk_box.animate.move_to([-0.35, 0.15, 0]),
                  FadeIn(p_dot), run_time=0.8)
        self.play(p_dot.animate.move_to(creb.p_spot), run_time=0.8)

        self.at("exact same serine")
        ser_lbl = T("Ser 133", 28, PHOSPHATE, weight=BOLD).move_to([3.85, -0.14, 0])
        self.play(FadeIn(ser_lbl), Indicate(p_dot, color=PHOSPHATE, scale_factor=1.25),
                  camk_box.animate.move_to([-0.85, -0.20, 0]), run_time=2.2)

        self.at("Growth factors")
        erk_lbl = T("kinases ERK switches on", 26, TEXT).move_to([0.45, 2.25, 0])
        erk_arrow = Arrow(erk_lbl.get_bottom() + DOWN * 0.14 + RIGHT * 0.25, p_dot.get_top() + UP * 0.14,
                          color=TEXT, stroke_width=4, buff=0.08)
        erk_arrow.layout_ok = True
        self.play(FadeIn(erk_lbl, shift=RIGHT * 0.2), run_time=2.0)

        self.at("kinases that ERK")
        erk_pulse = Dot(erk_arrow.get_start(), radius=0.12, color=TEXT)
        self.play(GrowArrow(erk_arrow), run_time=1.3)
        self.play(MoveAlongPath(erk_pulse, erk_arrow), run_time=1.5)
        self.remove(erk_pulse)

        self.at("separate signals")
        pka_tag = T("PKA (cAMP)", 26, CAMP_PKA, weight=BOLD).move_to([-0.85, 1.15, 0])
        pka_arrow = Arrow(pka_tag.get_right() + RIGHT * 0.14, p_dot.get_left() + UL * 0.22,
                          color=CAMP_PKA, stroke_width=4, buff=0.08)
        pka_arrow.layout_ok = True
        camk_arrow = Arrow(camk_box.get_right() + RIGHT * 0.10, p_dot.get_left() + LEFT * 0.12,
                           color=CA_CALC, stroke_width=4, buff=0.08)
        camk_arrow.layout_ok = True
        cbp = make_cbp_crescent().move_to([4.55, 1.95, 0])
        self.play(FadeIn(pka_tag), GrowArrow(pka_arrow), GrowArrow(camk_arrow), FadeIn(cbp), run_time=0.7)
        self.wait(0.35)
        # Clear top arrows/labels before gliding CBP above P and descending so it clears ERK label and Ser 133
        cup_offset = cbp.cup_anchor.get_center() - cbp.get_center()
        dock_center = p_dot.get_center() - cup_offset
        above_center = np.array([dock_center[0], 1.75, 0.0])
        self.play(FadeOut(erk_arrow), FadeOut(pka_arrow), FadeOut(camk_arrow),
                  FadeOut(erk_lbl), FadeOut(pka_tag), run_time=0.25)
        self.play(cbp.animate.move_to(above_center), run_time=0.25)
        self.play(cbp.animate.move_to(dock_center), run_time=0.25)
        self.finish()


class S05NfatSetup(SpokenScene):
    def construct(self):
        nuc_start = build_nuclear_view(env_x=-2.3, y_top=3.30, y_bot=-2.65, dna_y=-1.60, cre_x=0.35, show_labels=True)
        creb_start = make_creb_pair(np.array([0.35, -0.98, 0.0]))
        p_start = make_p_dot(radius=0.23, font_size=24).move_to(creb_start.p_spot)

        cell = build_full_cell(y_top=3.30, y_bot=-2.45, env_x=0.65, pore_y=-0.1, dna_y=-1.55, show_labels=True)
        creb_small = make_creb_pair(np.array([3.65, -0.98, 0.0]))
        p_small = make_p_dot(radius=0.23, font_size=24).move_to(creb_small.p_spot)

        self.add(*nuc_start, creb_start, p_start)

        self.at("Adding a phosphate")
        self.play(
            ReplacementTransform(nuc_start[0], cell[0]),
            ReplacementTransform(nuc_start[1], cell[1]),
            FadeIn(cell.membrane),
            ReplacementTransform(nuc_start.envelope, cell.envelope),
            FadeTransform(nuc_start.dna, cell.dna),
            ReplacementTransform(nuc_start.lbl_cyto, cell.lbl_cyto),
            ReplacementTransform(nuc_start.lbl_nuc, cell.lbl_nuc),
            ReplacementTransform(creb_start, creb_small),
            ReplacementTransform(p_start, p_small),
            run_time=2.5,
        )

        self.at("second premade factor")
        nfat = make_nfat_block(np.array([-4.15, -0.1, 0.0]))
        p_ring = make_nfat_phosphates(nfat)
        nfat_all = VGroup(nfat, p_ring)
        self.play(FadeIn(nfat_all, shift=RIGHT * 0.2), run_time=2.0)

        self.at("resting in the cytoplasm")
        self.play(nfat_all.animate.shift(RIGHT * 0.55), run_time=2.6)

        self.at("dozen phosphates")
        self.play(*[Indicate(p, color=PHOSPHATE, scale_factor=1.2) for p in p_ring], run_time=1.8)

        self.at("nuclear entry tag")
        self.play(Indicate(nfat.tag, color=IMPORT_COL, scale_factor=1.15), run_time=2.0)

        self.at("removing phosphates")
        self.play(nfat_all.animate.move_to([-2.05, -0.1, 0]), run_time=2.8)

        self.at("locking it outside")
        self.play(nfat_all.animate.move_to([-1.45, -0.1, 0]), run_time=0.9)
        self.play(nfat_all.animate.move_to([-2.45, -0.1, 0]), run_time=1.3)
        self.finish()


def world_nfat_predict(ca_phase=0.0):
    """Shared builder for end of s06_predict_prompt and s07_pause."""
    cell = build_full_cell(y_top=3.30, y_bot=-2.25, env_x=0.75, pore_y=-0.1, dna_y=-1.45, show_labels=True)
    nfat = make_nfat_block(np.array([-3.35, -0.1, 0.0]))
    p_ring = make_nfat_phosphates(nfat)
    calc = make_calcineurin(np.array([-3.25, 1.80, 0.0]), font_size=24)
    receptor = make_receptor(np.array([-5.88, -0.1, 0.0]))
    ca_dots = VGroup(*[
        Dot([-5.45 + 0.24 * ((i + ca_phase) % 4), -0.1 + 0.14 * np.sin(2.0 * i + ca_phase), 0.0],
            radius=0.10, color=CA_CALC)
        for i in range(4)
    ])
    ca_lbl = T("Ca²⁺", 28, CA_CALC, weight=BOLD).move_to([-4.95, -1.25, 0])
    return VGroup(cell, receptor, nfat, p_ring, calc, ca_dots, ca_lbl)


class S06PredictPrompt(SpokenScene):
    def construct(self):
        cell = build_full_cell(y_top=3.30, y_bot=-2.25, env_x=0.75, pore_y=-0.1, dna_y=-1.45, show_labels=True)
        nfat = make_nfat_block(np.array([-3.35, -0.1, 0.0]))
        p_ring = make_nfat_phosphates(nfat)
        receptor = make_receptor(np.array([-5.88, -0.1, 0.0]))

        self.add(cell, receptor, nfat, p_ring)

        self.at("T cell receptor")
        sig = Dot([-6.35, -0.1, 0], radius=0.17, color=CA_CALC)
        self.play(FadeIn(sig), run_time=0.4)
        self.play(sig.animate.move_to([-5.95, -0.1, 0]), run_time=1.3)

        self.at("sustained calcium")
        ca_phase = ValueTracker(0.0)
        ca_stream = make_ca_stream(-5.55, -4.45, -0.1, ca_phase, n=4, radius=0.10)
        ca_lbl = T("Ca²⁺", 28, CA_CALC, weight=BOLD).move_to([-4.95, -1.25, 0])
        calc = make_calcineurin(np.array([-3.85, 1.80, 0.0]), font_size=24)
        self.play(FadeOut(sig), FadeIn(ca_lbl), FadeIn(calc), run_time=0.6)
        self.add(ca_stream)
        self.play(ca_phase.animate.set_value(2.0), run_time=2.2, rate_func=linear)

        self.at("removes phosphates")
        self.play(calc.animate.move_to([-3.25, 1.80, 0]), ca_phase.animate.set_value(3.5), run_time=1.8, rate_func=linear)

        self.at("Pause and predict")
        q = question_card("Calcineurin removes phosphates -> Where does NFAT go?", max_w=10.5)
        self.play(FadeIn(q, shift=UP * 0.15), ca_phase.animate.set_value(3.92), run_time=0.8, rate_func=linear)
        self.play(ca_phase.animate.set_value(6.0), run_time=4.0, rate_func=linear)
        self.finish()


class S07Pause(PredictPause):
    QUESTION = "Calcineurin removes phosphates -> Where does NFAT go?"
    SECONDS = 4.5

    def backdrop(self):
        return world_nfat_predict()


class S08NfatReveal(SpokenScene):
    def construct(self):
        world = world_nfat_predict()
        cell, receptor, nfat, p_ring, calc, ca_dots, ca_lbl = world
        q = question_card("Calcineurin removes phosphates -> Where does NFAT go?", max_w=10.5)
        self.add(world, q)

        self.play(FadeOut(q), run_time=0.6)

        self.at("strips the phosphates")
        self.play(calc.animate.move_to([-2.05, 1.80, 0]), run_time=1.2)
        self.play(
            calc.animate.move_to([-3.25, 1.80, 0]),
            *[p.animate.shift(UP * 0.45 + RIGHT * 0.25).set_opacity(0) for p in p_ring],
            run_time=2.4,
        )
        self.remove(p_ring)

        self.at("tag exposed")
        tag_lbl = T("Import tag exposed", 28, IMPORT_COL, weight=BOLD).move_to([-2.05, -1.35, 0])
        self.play(Indicate(nfat.tag, color=IMPORT_COL, scale_factor=1.15), FadeIn(tag_lbl), run_time=1.1)

        self.at("glides through a pore")
        self.play(FadeOut(tag_lbl), nfat.animate.move_to([3.05, -0.35, 0]), run_time=1.1)

        self.at("switches on target genes")
        mrna_t = ValueTracker(0.0)
        mrna = make_mrna_ribbon(np.array([4.55, cell.dna_y + 0.25, 0.0]), mrna_t, max_len=1.55, height=1.55)
        gene_lbl = T("Target gene ON", 28, MRNA_COL, weight=BOLD).move_to([4.55, 1.35, 0])
        self.add(mrna)
        self.play(mrna_t.animate.set_value(1.0), FadeIn(gene_lbl), run_time=2.2, rate_func=linear)

        self.at("calcium drops")
        self.play(FadeOut(ca_dots), FadeOut(ca_lbl), FadeOut(calc),
                  FadeOut(mrna), FadeOut(gene_lbl), run_time=1.3)

        self.at("restore those phosphates")
        kinase_lbl = T("Kinases", 28, PHOSPHATE, weight=BOLD).move_to([3.05, 1.30, 0])
        p_back = make_nfat_phosphates(nfat)
        self.play(FadeIn(kinase_lbl), FadeIn(p_back, lag_ratio=0.05), run_time=1.2)

        self.at("send it back out")
        nfat_back = VGroup(nfat, p_back)
        self.play(FadeOut(kinase_lbl), nfat_back.animate.move_to([-1.95, -0.1, 0]), run_time=1.4)
        self.finish()


class S09Drugs(SpokenScene):
    def construct(self):
        cell = build_full_cell(y_top=3.30, y_bot=-2.50, env_x=4.5, pore_y=-0.1, dna_y=-1.55, show_labels=False)
        lbl_cyto = T("Cytosol", 28, TEXT).move_to([-0.5, 2.90, 0])
        lbl_nuc = T("Nucleus", 28, TEXT).move_to([5.35, 2.90, 0])

        calc = make_calcineurin(np.array([-1.55, -0.15, 0.0]), scale=1.18, font_size=26)
        notch_lbl = T("Active site", 26, CA_CALC, weight=BOLD).move_to([-0.65, -1.78, 0])
        notch_arr = Arrow(notch_lbl.get_top() + UP * 0.06, calc.notch_point + DOWN * 0.14,
                          color=CA_CALC, stroke_width=3.5, buff=0.05)
        notch_arr.layout_ok = True

        self.add(cell, lbl_cyto, lbl_nuc, calc, notch_lbl, notch_arr)

        self.at("Two transplant drugs")
        csa = boxed_label("Cyclosporin A", DRUG_COL, size=26).move_to([-4.05, 2.15, 0])
        fk = boxed_label("FK506", DRUG_COL, size=26).move_to([-4.05, 1.30, 0])
        self.play(FadeIn(csa, shift=RIGHT * 0.2), FadeIn(fk, shift=RIGHT * 0.2), run_time=2.5)

        self.at("jamming the switch")
        self.play(Indicate(notch_lbl, color=DRUG_COL, scale_factor=1.18), run_time=1.4)

        self.at("Neither drug blocks")
        drug = boxed_label("Drug", DRUG_COL, size=26).move_to([2.05, 1.45, 0])
        self.play(FadeIn(drug), run_time=0.6)
        self.play(drug.animate.move_to([0.75, -0.15, 0]), run_time=1.3)
        self.play(drug.animate.move_to([2.05, 1.45, 0]), run_time=1.3)

        self.at("small helper protein")
        helper = boxed_label("Helper protein", DRUG_COL, size=26).move_to([2.05, 2.35, 0])
        self.play(FadeIn(helper, shift=DOWN * 0.15), run_time=0.8)
        self.play(helper.animate.next_to(drug, UP, buff=0.08), run_time=0.9)
        jaw = RoundedRectangle(corner_radius=0.08, width=0.34, height=1.10,
                               stroke_color=DRUG_COL, stroke_width=3.5,
                               fill_color=DRUG_COL, fill_opacity=0.35).next_to(drug, DOWN, buff=0.06).align_to(drug, LEFT)
        self.play(FadeIn(jaw), run_time=0.4)
        clamp = VGroup(helper, drug, jaw)

        self.at("That pair sits beside")
        # Dock clamp beside the active notch mouth: jaw hangs right in front of the notch entrance
        self.play(clamp.animate.move_to([0.75, 1.02, 0]), run_time=2.2)

        self.at("keeps protein substrates")
        sub = boxed_label("Protein substrate", TEXT, size=26).move_to([2.80, -0.15, 0])
        self.play(FadeIn(sub, shift=LEFT * 0.12), run_time=0.35)
        self.play(sub.animate.move_to([2.22, -0.15, 0]), run_time=1.1)
        self.play(sub.animate.move_to([2.90, -0.15, 0]), run_time=1.0)
        self.finish()


class S10ReturnCfos(SpokenScene):
    def construct(self):
        cell = build_full_cell(y_top=3.30, y_bot=-2.45, env_x=0.45, pore_y=1.55, dna_y=-1.65,
                               show_labels=True, dna_cre=True)
        ribo = make_ribosome_stopped(np.array([-3.1, -1.25, 0.0]))
        creb = make_creb_pair(np.array([2.15, -1.04, 0.0]))
        p_creb = make_p_dot(radius=0.23, font_size=24).move_to(creb.p_spot)
        cbp = make_cbp_crescent(size=26).move_to([2.15, 1.75, 0])

        nfat = make_nfat_block(np.array([-3.5, 1.55, 0.0]), body_w=1.45, body_h=0.96,
                               font_size=26, tag_size=22)
        p_nfat = make_nfat_phosphates(nfat)

        # Start immediately with full carried cell on screen (no blank frame!)
        self.add(cell, ribo, creb, nfat, p_nfat)

        self.at("adds one phosphate")
        self.play(FadeIn(p_creb, scale=1.25), FadeIn(cbp), run_time=0.6)
        shift_vec = p_creb.get_center() - cbp.cup_anchor.get_center()
        self.play(cbp.animate.shift(shift_vec), run_time=0.8)

        self.at("removes many")
        self.play(FadeOut(p_nfat, shift=UP * 0.2), run_time=0.9)
        self.play(nfat.animate.move_to([-1.25, 1.55, 0]), run_time=0.8)
        self.play(nfat.animate.move_to([2.85, 1.55, 0]), run_time=1.3)

        self.at("Fast signals flip")
        mrna_t = ValueTracker(0.0)
        m1 = make_mrna_ribbon(np.array([3.65, cell.dna_y + 0.25, 0.0]), mrna_t, max_len=2.15, height=1.55)
        m2 = make_mrna_ribbon(np.array([3.95, cell.dna_y + 0.25, 0.0]), mrna_t, max_len=1.95, height=1.10, phase_offset=1.7)
        cfos_lbl = T("c-fos mRNA", 28, MRNA_COL, weight=BOLD).move_to([4.95, 0.75, 0])
        self.add(m1, m2)
        self.play(mrna_t.animate.set_value(0.65), FadeIn(cfos_lbl), run_time=3.5, rate_func=linear)

        self.at("within minutes")
        self.play(mrna_t.animate.set_value(0.90), run_time=1.8, rate_func=linear)

        self.at("Stopped ribosomes")
        self.play(Indicate(ribo, color=DRUG_COL, scale_factor=1.08),
                  Indicate(cfos_lbl, color=MRNA_COL, scale_factor=1.08),
                  mrna_t.animate.set_value(1.0), run_time=2.2, rate_func=linear)
        self.finish()


class S11End(EndCard):
    LINE = "Fast signals flip pre-made factors to switch on first-wave genes."
