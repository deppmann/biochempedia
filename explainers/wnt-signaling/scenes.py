"""Wnt Slows the Drain — animation scenes for the STEMhop lesson "Wnt: β-Catenin and Planar Polarity".

COLOUR MAP (one colour per concept for the whole film):
  CATENIN   = "#FF6E5A"   coral-orange : β-catenin (free cytoplasmic, junctional, nuclear)
  DESTRUCT  = "#A78BFA"   violet       : destruction complex (Axin, APC, CK1, GSK3), SCF (β-TrCP), proteasome, drain
  TEAL      = "#3FB8C0"   teal         : Frizzled seven-pass receptor (from bp_style)
  LRP_BLUE  = "#5B8DEF"   slate-blue   : LRP5/6 single-pass co-receptor
  WNT_GOLD  = "#F5D547"   gold         : Wnt ligand + fatty-acid lipid tail + phosphate tags (P)
  DVL_AMBER = "#F29F38"   amber        : Dishevelled (Dvl)
  EMERALD   = "#34D399"   emerald      : TCF on target DNA and active transcription ("ON")
  GROUCHO   = "#94A3B8"   cool grey    : Groucho co-repressor ("OFF")
  MEMBRANE  = "#64748B"   slate        : plasma membrane, nuclear envelope, DNA backbone
  MUTATION  = "#EC4899"   magenta      : broken APC / mutated phosphate site crack & mutation inset
  TEXT      = "#E8EAF0"   off-white    : primary labels & headings
  GREY      = "#8B93A1"   grey         : scope tags & axis ticks

ONE CARRIED WORLD:
  Left/centre: cross-section of one dark-slate cell (plasma membrane at top with Frizzled and LRP5/6,
  cadherin junction on the left edge, cytoplasm in the middle with synthesis tap -> destruction
  complex / proteasome drain, and rounded nucleus at bottom with pores, DNA and TCF).
  Right: live schematic β-catenin level tank (0..150 units) governed by first-order turnover
  dC/dt = s - k*C with s = 12 / min, k_off = 0.4 / min (steady 30), k_on = 0.1 / min (steady 120).

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
  s01_hook            : Free β-catenin blocks spawn continuously from the tap (rate s=12/min), drift across
                        cytoplasm and are shredded in the violet drain while the tank stays steady at 30.
  s02_off_complex     : Cadherin junction pool is highlighted and dimmed; free β-catenin docks into the
                        assembling violet destruction complex (Axin, APC, CK1, GSK3) while receptors sit empty.
  s03_off_tag_destroy : CK1 adds 1 gold phosphate then GSK3 adds 3 more sequentially; tagged β-catenin slides
                        to SCF (β-TrCP), grows a ubiquitin chain, and spirals into the turning proteasome.
  s04_predict_setup   : Schematic tank expands to fill focus with tap (12/min) and drain (k=0.4/min -> 30);
                        valve narrows drain to 1/4 (k=0.1/min) and three prediction choice chips appear.
  s06_predict_reveal  : "Rises 4x" highlights; tank fluid, live readout, and computed curve C(t)=120-90*exp(-0.1*t)
                        climb simultaneously from t_min (30 -> 120 units) while "Level = synthesis ÷ destruction rate",
                        "12 ÷ 0.4 = 30", and "12 ÷ 0.1 = 120 (4×)" build word by word in time with speech.
  s07_wnt_receptor    : Gold Wnt with its curved lipid tail drifts down, inserts the lipid into teal Frizzled's
                        groove, and pulls slate-blue LRP5/6 beside Frizzled.
  s08_complex_pulled  : Amber Dishevelled docks beneath Frizzled, gold phosphates appear on LRP5/6's tail, and
                        the violet destruction complex glides up to tether there while the shredder idles.
  s09_nucleus_tcf     : Surviving coral β-catenin blocks accumulate across cytoplasm, stream through nuclear
                        pores to TCF/Groucho on DNA, while the tank gauge climbs along C(t)=120-90*exp(-0.1*t).
  s10_genes_and_cancer: β-Catenin displaces Groucho from TCF to launch transcription waves along DNA; then an
                        inset with empty receptors ("No Wnt") and cracked APC/missing P sites stays stuck ON.
  s11_wrap            : Side-by-side comparison ("No Wnt" vs "+ Wnt") runs live particle turnover and tank
                        levels (30 OFF vs 120 ON) simultaneously to show slowing destruction switches genes on.
"""

from bp_parts import *

# ------------------------------------------------------------------ concept palette
CATENIN = "#FF6E5A"
DESTRUCT = "#A78BFA"
LRP_BLUE = "#5B8DEF"
WNT_GOLD = "#F5D547"
DVL_AMBER = "#F29F38"
EMERALD = "#34D399"
GROUCHO = "#94A3B8"
MEMBRANE = "#64748B"
MUTATION = "#EC4899"
CYTO_BG = "#1B2433"
NUC_BG = "#233044"

# ------------------------------------------------------------------ turnover math (lesson numbers)
SYN_RATE = 12.0       # units / min
K_OFF = 0.4           # / min  -> steady = 30
K_ON = 0.1            # / min  -> steady = 120 (1/4 rate)
STEADY_OFF = SYN_RATE / K_OFF   # 30.0
STEADY_ON = SYN_RATE / K_ON     # 120.0


def c_climb(t_min):
    """Exact ODE solution for free β-catenin after k drops from 0.4 to 0.1 / min at t = 0."""
    return STEADY_ON - (STEADY_ON - STEADY_OFF) * np.exp(-K_ON * t_min)


# ------------------------------------------------------------------ shared geometry builders
def make_frizzled(center, scale=1.0):
    """Schematic 7-pass receptor (bars + outer binding cup with lipid groove; no molecular structure)."""
    g = VGroup()
    cup = Arc(radius=0.34, start_angle=PI * 1.08, angle=PI * 0.84, color=TEAL, stroke_width=4.5)
    cup.move_arc_center_to([0, 0.34, 0])
    helices = VGroup(*[
        RoundedRectangle(corner_radius=0.04, width=0.08, height=0.58,
                         stroke_color=TEAL, stroke_width=1.8, fill_color=TEAL, fill_opacity=0.40)
        .move_to([-0.24 + i * 0.08, -0.05, 0])
        for i in range(7)
    ])
    g.add(helices, cup)
    g.scale(scale).move_to(center)
    return g


def make_lrp(center, scale=1.0, tall=1.0):
    """Schematic single-pass LRP5/6 co-receptor with outer head and inner cytoplasmic tail."""
    head = RoundedRectangle(corner_radius=0.1, width=0.32, height=0.34,
                            stroke_color=LRP_BLUE, stroke_width=2.5, fill_color=LRP_BLUE, fill_opacity=0.36).move_to([0, 0.38, 0])
    stalk = Line([0, 0.21, 0], [0, -0.45 * tall, 0], color=LRP_BLUE, stroke_width=5.5)
    g = VGroup(stalk, head).scale(scale).move_to(center)
    return g


def make_wnt(center, scale=1.0, font_size=26):
    """Gold Wnt ligand block with curved fatty-acid lipid tail pointing down-left."""
    body = RoundedRectangle(corner_radius=0.14, width=1.24, height=0.54,
                            stroke_color=WNT_GOLD, stroke_width=2.5, fill_color=WNT_GOLD, fill_opacity=0.28)
    tail = CubicBezier(
        body.get_bottom() + LEFT * 0.22,
        body.get_bottom() + LEFT * 0.38 + DOWN * 0.20,
        body.get_bottom() + LEFT * 0.16 + DOWN * 0.35,
        body.get_bottom() + LEFT * 0.28 + DOWN * 0.52,
        color=WNT_GOLD, stroke_width=5,
    )
    shapes = VGroup(body, tail).scale(scale).move_to(center)
    lab = T("Wnt", font_size, WNT_GOLD, weight=BOLD).move_to(shapes[0])
    g = VGroup(shapes, lab)
    g.tail = shapes[1]
    g.body = shapes[0]
    return g


def make_catenin_block(pos=ORIGIN, size=0.34, w_ratio=1.35, label=False, font_size=22, min_w=0.0):
    """Coral-orange β-catenin block (sized to hold 'β-cat' without overflow when label=True)."""
    if label:
        t = T("β-cat", font_size, BG, weight=BOLD)
        w = max(size * w_ratio, t.width + 0.30, min_w)
        h = max(size, t.height + 0.20)
        rect = RoundedRectangle(corner_radius=0.08, width=w, height=h,
                                stroke_color=CATENIN, stroke_width=2.2, fill_color=CATENIN, fill_opacity=0.88).move_to(pos)
        return VGroup(rect, t.move_to(rect))
    w, h = size * w_ratio, size
    return RoundedRectangle(corner_radius=0.07, width=w, height=h,
                            stroke_color=CATENIN, stroke_width=2.2, fill_color=CATENIN, fill_opacity=0.80).move_to(pos)


def make_tap(pos, scale=1.0):
    """Synthesis tap nozzle on the left wall of the cytoplasm."""
    pipe = RoundedRectangle(corner_radius=0.06, width=0.65, height=0.26,
                            stroke_color=CATENIN, stroke_width=2.5, fill_color=CATENIN, fill_opacity=0.28)
    spout = Polygon([-0.12, -0.13, 0], [0.12, -0.13, 0], [0.18, -0.34, 0], [-0.18, -0.34, 0],
                    stroke_color=CATENIN, stroke_width=2.2, fill_color=CATENIN, fill_opacity=0.40).next_to(pipe, DOWN, buff=0).shift(RIGHT * 0.16)
    return VGroup(pipe, spout).scale(scale).move_to(pos)


def make_proteasome(pos, scale=1.0):
    """Turning violet proteasome shredder barrel (4 stacked rings + inner teeth)."""
    rings = VGroup(*[
        RoundedRectangle(corner_radius=0.1, width=0.86, height=0.20,
                         stroke_color=DESTRUCT, stroke_width=2.5, fill_color=DESTRUCT, fill_opacity=0.24 + 0.08 * (i % 2))
        for i in range(4)
    ]).arrange(DOWN, buff=0.03)
    blades = VGroup(
        Line([-0.24, 0.18, 0], [0.24, -0.18, 0], color=DESTRUCT, stroke_width=2.5),
        Line([-0.24, -0.18, 0], [0.24, 0.18, 0], color=DESTRUCT, stroke_width=2.5),
    ).move_to(rings)
    g = VGroup(rings, blades).scale(scale).move_to(pos)
    g.blades = blades
    return g


def make_cell_shell(x0=-6.1, x1=2.45, mem_y=2.45, nuc_top=-1.15, nuc_bot=-3.25):
    """Carried dark-slate cell cross-section: plasma membrane across top, cytoplasm, rounded nucleus at bottom."""
    w = x1 - x0
    cx = (x0 + x1) / 2
    cyto_h = mem_y - (nuc_bot + 0.15)
    cyto_bg = RoundedRectangle(corner_radius=0.18, width=w, height=cyto_h,
                               stroke_width=0, fill_color=CYTO_BG, fill_opacity=0.72).move_to([cx, (mem_y + nuc_bot + 0.15) / 2, 0])
    wall_l = Line([x0, mem_y, 0], [x0, nuc_bot + 0.35, 0], color=MEMBRANE, stroke_width=3.5)
    wall_r = Line([x1, mem_y, 0], [x1, nuc_bot + 0.35, 0], color=MEMBRANE, stroke_width=3.5)
    mem_top = Line([x0, mem_y + 0.08, 0], [x1, mem_y + 0.08, 0], color=MEMBRANE, stroke_width=3.5)
    mem_bot = Line([x0, mem_y - 0.08, 0], [x1, mem_y - 0.08, 0], color=MEMBRANE, stroke_width=3.5)

    pore1, pore2 = cx - 1.15, cx + 1.15
    pw = 0.34
    nuc_w = w - 0.8
    nx0, nx1 = cx - nuc_w / 2, cx + nuc_w / 2
    nuc_bg = RoundedRectangle(corner_radius=0.45, width=nuc_w, height=nuc_top - nuc_bot,
                              stroke_width=0, fill_color=NUC_BG, fill_opacity=0.85).move_to([cx, (nuc_top + nuc_bot) / 2, 0])
    nt1 = Line([nx0 + 0.35, nuc_top, 0], [pore1 - pw, nuc_top, 0], color=MEMBRANE, stroke_width=3.5)
    nt2 = Line([pore1 + pw, nuc_top, 0], [pore2 - pw, nuc_top, 0], color=MEMBRANE, stroke_width=3.5)
    nt3 = Line([pore2 + pw, nuc_top, 0], [nx1 - 0.35, nuc_top, 0], color=MEMBRANE, stroke_width=3.5)
    ns_l = ArcBetweenPoints([nx0 + 0.35, nuc_top, 0], [nx0 + 0.35, nuc_bot, 0], angle=0.55, color=MEMBRANE, stroke_width=3.5)
    ns_r = ArcBetweenPoints([nx1 - 0.35, nuc_top, 0], [nx1 - 0.35, nuc_bot, 0], angle=-0.55, color=MEMBRANE, stroke_width=3.5)
    nb = Line([nx0 + 0.35, nuc_bot, 0], [nx1 - 0.35, nuc_bot, 0], color=MEMBRANE, stroke_width=3.5)

    dna_y = nuc_bot + 0.50
    dna1 = Line([nx0 + 0.7, dna_y + 0.04, 0], [nx1 - 0.7, dna_y + 0.04, 0], color=MEMBRANE, stroke_width=3)
    dna2 = Line([nx0 + 0.7, dna_y - 0.04, 0], [nx1 - 0.7, dna_y - 0.04, 0], color=MEMBRANE, stroke_width=3)
    dna_ticks = VGroup(*[
        Line([nx0 + 0.9 + i * 0.45, dna_y - 0.04, 0], [nx0 + 0.9 + i * 0.45, dna_y + 0.04, 0],
             color=MEMBRANE, stroke_width=2)
        for i in range(int((nuc_w - 1.8) / 0.45) + 1)
    ])
    g = VGroup(cyto_bg, nuc_bg, wall_l, wall_r, mem_top, mem_bot, nt1, nt2, nt3, ns_l, ns_r, nb, dna1, dna2, dna_ticks)
    g.cx = cx
    g.dna_y = dna_y
    g.pores = [pore1, pore2]
    g.mem_y = mem_y
    g.nuc_top = nuc_top
    return g


def make_side_tank(level_tracker, phase_tracker=None, drain_rate_tracker=None, x=4.75, y_bot=-1.95, y_top=2.25, w=1.80, show_target=False):
    """Carried right-side schematic level tank (0..150 units) with live tap inflow & drain outflow."""
    h = y_top - y_bot
    frame = RoundedRectangle(corner_radius=0.10, width=w, height=h,
                             stroke_color=GREY, stroke_width=3, fill_color=CYTO_BG, fill_opacity=0.65).move_to([x, (y_bot + y_top) / 2, 0])
    ticks = VGroup()
    for val in (0, 30, 60, 90, 120):
        yy = y_bot + (val / 150.0) * h
        ticks.add(Line([x - w / 2 - 0.10, yy, 0], [x - w / 2, yy, 0], color=GREY, stroke_width=2.5))
    y30 = y_bot + (30.0 / 150.0) * h
    y120 = y_bot + (120.0 / 150.0) * h
    ref30 = DashedLine([x - w / 2 + 0.05, y30, 0], [x + w / 2 - 0.05, y30, 0], color=GREY, stroke_width=2, dash_length=0.10)
    lbl30 = M("30", 24, GREY).next_to([x - w / 2 - 0.12, y30, 0], LEFT, buff=0.10)
    extras = VGroup()
    if show_target:
        ref120 = DashedLine([x - w / 2 + 0.05, y120, 0], [x + w / 2 - 0.05, y120, 0], color=WNT_GOLD, stroke_width=2, dash_length=0.10)
        lbl120 = M("120", 24, WNT_GOLD).next_to([x - w / 2 - 0.12, y120, 0], LEFT, buff=0.10)
        extras.add(ref120, lbl120)

    def fluid_mk():
        val = float(np.clip(level_tracker.get_value(), 2.0, 148.0))
        fh = (val / 150.0) * (h - 0.06)
        r = Rectangle(width=w - 0.08, height=fh, stroke_width=0, fill_color=CATENIN, fill_opacity=0.72)
        r.move_to([x, y_bot + 0.03 + fh / 2, 0])
        surf = Line([x - w / 2 + 0.05, y_bot + 0.03 + fh, 0], [x + w / 2 - 0.05, y_bot + 0.03 + fh, 0],
                    color=CATENIN, stroke_width=3.5)
        g = VGroup(r, surf)
        if phase_tracker is not None:
            ph = phase_tracker.get_value()
            in_x = x - w * 0.22
            surf_y = y_bot + 0.03 + fh
            g.add(Line([in_x, y_top - 0.04, 0], [in_x, surf_y, 0], color=CATENIN, stroke_width=3.5, stroke_opacity=0.45))
            for i in range(4):
                u = (ph * 0.95 + i * 0.25) % 1.0
                dy = (y_top - 0.06) - u * max(0.15, (y_top - 0.06) - surf_y)
                g.add(Dot([in_x, dy, 0], radius=0.065, color=CATENIN))
            dr = drain_rate_tracker.get_value() if drain_rate_tracker is not None else 1.0
            for i in range(3):
                u = (ph * (0.45 + 0.70 * dr) + i / 3.0) % 1.0
                dx = x + w / 2 + 0.05 + u * 0.34
                dy = y_bot + 0.16 - 0.36 * (u ** 1.6)
                g.add(Dot([dx, dy, 0], radius=0.055 + 0.025 * dr, color=DESTRUCT))
        return g

    fluid = always_redraw(fluid_mk)
    title = T("Free β-cat", 26, CATENIN).move_to([x, y_top + 0.35, 0])
    num = always_redraw(lambda: M(f"{level_tracker.get_value():.0f}", 30, CATENIN).move_to([x, y_bot - 0.38, 0]))
    return VGroup(frame, fluid, ref30, extras, ticks, lbl30, title, num)


def make_destruction_complex(center, scale=1.0, show_labels=True):
    """Violet destruction complex: Axin arc with CK1, GSK3, APC placed well CLEAR of the arc."""
    cx, cy = center[0], center[1]
    r = 0.74 * scale
    axin = Arc(radius=r, start_angle=PI * 0.55, angle=PI * 1.10, color=DESTRUCT, stroke_width=8 * max(0.7, scale),
               arc_center=[cx, cy, 0])
    if show_labels:
        # Placed well outside arc radius so neither box nor text ever touches Axin or each other
        ck1 = boxed_label("CK1", DESTRUCT, size=24, box=(0.94, 0.48), pad=0.08, fill_opacity=0.26).move_to([cx - 0.24 * scale, cy + 1.28 * scale, 0])
        gsk3 = boxed_label("GSK3", DESTRUCT, size=24, box=(1.08, 0.48), pad=0.08, fill_opacity=0.26).move_to([cx + 1.42 * scale, cy + 0.88 * scale, 0])
        apc = boxed_label("APC", DESTRUCT, size=26, box=(1.12, 0.54), pad=0.08, fill_opacity=0.28).move_to([cx + 1.35 * scale, cy - 0.88 * scale, 0])
        axin_lab = T("Axin", 24, DESTRUCT).move_to([cx - 1.28 * scale, cy - 0.65 * scale, 0])
        g = VGroup(axin, ck1, gsk3, apc, axin_lab)
        g.axin, g.ck1, g.gsk3, g.apc, g.axin_lab = axin, ck1, gsk3, apc, axin_lab
    else:
        ck1 = RoundedRectangle(corner_radius=0.08, width=0.58 * scale, height=0.34 * scale,
                               stroke_color=DESTRUCT, stroke_width=2, fill_color=DESTRUCT, fill_opacity=0.35).move_to([cx + 0.05 * scale, cy + 1.05 * scale, 0])
        gsk3 = RoundedRectangle(corner_radius=0.08, width=0.64 * scale, height=0.34 * scale,
                                stroke_color=DESTRUCT, stroke_width=2, fill_color=DESTRUCT, fill_opacity=0.35).move_to([cx + 0.98 * scale, cy + 0.55 * scale, 0])
        apc = RoundedRectangle(corner_radius=0.08, width=0.72 * scale, height=0.40 * scale,
                               stroke_color=DESTRUCT, stroke_width=2, fill_color=DESTRUCT, fill_opacity=0.35).move_to([cx + 0.92 * scale, cy - 0.52 * scale, 0])
        g = VGroup(axin, ck1, gsk3, apc)
        g.axin, g.ck1, g.gsk3, g.apc = axin, ck1, gsk3, apc
    return g


def make_big_tank(level_t, drain_open_t, tap_phase_t, box=(-5.4, 0.1, -1.45, 2.35), show_target=False):
    """Expanded schematic tank for S04/S05/S06, computed from s=12/min and k=0.4 or 0.1/min."""
    x0, x1, y0, y1 = box
    cx = (x0 + x1) / 2
    w = x1 - x0
    h = y1 - y0
    wall_l = Line([x0, y1, 0], [x0, y0, 0], color=GREY, stroke_width=4)
    wall_b = Line([x0, y0, 0], [x1, y0, 0], color=GREY, stroke_width=4)
    wall_r_top = Line([x1, y1, 0], [x1, y0 + 0.34, 0], color=GREY, stroke_width=4)
    drain_top = Line([x1, y0 + 0.34, 0], [x1 + 0.72, y0 + 0.34, 0], color=DESTRUCT, stroke_width=4)
    drain_bot = Line([x1, y0, 0], [x1 + 0.72, y0, 0], color=DESTRUCT, stroke_width=4)

    ticks = VGroup()
    lbl120 = None
    for val in (0, 30, 60, 90, 120, 150):
        yy = y0 + (val / 150.0) * h
        ticks.add(Line([x0 - 0.12, yy, 0], [x0, yy, 0], color=GREY, stroke_width=2.5))
        if show_target:
            if val in (0, 30, 120):
                col = WNT_GOLD if val == 120 else GREY
                t_lbl = M(str(val), 24, col).next_to([x0 - 0.14, yy, 0], LEFT, buff=0.08)
                ticks.add(t_lbl)
                if val == 120:
                    lbl120 = t_lbl
        else:
            t_lbl = M(str(val), 24, GREY).next_to([x0 - 0.14, yy, 0], LEFT, buff=0.08)
            ticks.add(t_lbl)
            if val == 120:
                lbl120 = t_lbl

    y30 = y0 + (30.0 / 150.0) * h
    y120 = y0 + (120.0 / 150.0) * h
    ref30 = DashedLine([x0 + 0.06, y30, 0], [x1 - 0.06, y30, 0], color=GREY, stroke_width=2, dash_length=0.14)
    ref120 = DashedLine([x0 + 0.06, y120, 0], [x1 - 0.06, y120, 0], color=WNT_GOLD, stroke_width=2, dash_length=0.14)

    def mk_fluid():
        val = float(np.clip(level_t.get_value(), 2.0, 148.0))
        fh = (val / 150.0) * (h - 0.05)
        fill = Rectangle(width=w - 0.06, height=fh, stroke_width=0, fill_color=CATENIN, fill_opacity=0.66)
        fill.move_to([cx, y0 + 0.025 + fh / 2, 0])
        ph = tap_phase_t.get_value()
        pts = [[x0 + 0.04 + (w - 0.08) * (i / 18.0),
                y0 + 0.025 + fh + 0.055 * np.sin(i * 0.85 - ph * 5.2), 0]
               for i in range(19)]
        surf = VMobject(color=CATENIN, stroke_width=5).set_points_as_corners(pts)
        return VGroup(fill, surf)

    fluid = always_redraw(mk_fluid)

    tap_x = x0 + 1.05
    tap_pipe = RoundedRectangle(corner_radius=0.06, width=0.95, height=0.28,
                                stroke_color=CATENIN, stroke_width=2.5, fill_color=CATENIN, fill_opacity=0.28).move_to([tap_x - 0.35, y1 + 0.62, 0])
    tap_spout = Polygon([tap_x - 0.10, y1 + 0.48, 0], [tap_x + 0.10, y1 + 0.48, 0],
                        [tap_x + 0.14, y1 + 0.25, 0], [tap_x - 0.14, y1 + 0.25, 0],
                        stroke_color=CATENIN, stroke_width=2.2, fill_color=CATENIN, fill_opacity=0.40)

    def mk_streams():
        ph = tap_phase_t.get_value()
        val = float(np.clip(level_t.get_value(), 2.0, 148.0))
        surf_y = y0 + 0.025 + (val / 150.0) * (h - 0.05)
        stream = VGroup(Line([tap_x, y1 + 0.24, 0], [tap_x, surf_y, 0], color=CATENIN, stroke_width=7, stroke_opacity=0.55))
        for i in range(5):
            frac = (ph * 1.15 + i * 0.20) % 1.0
            dy = (y1 + 0.22) - frac * max(0.2, (y1 + 0.22) - surf_y)
            stream.add(RoundedRectangle(corner_radius=0.04, width=0.26, height=0.16,
                                        stroke_width=0, fill_color=CATENIN, fill_opacity=0.92).move_to([tap_x, dy, 0]))
        open_f = float(np.clip(drain_open_t.get_value(), 0.15, 1.0))
        out_thick = float(np.clip(3.0 + 6.0 * open_f * (val / 30.0) * 0.5, 2.5, 10.0))
        out_y = y0 + 0.17
        stream.add(Line([x1 + 0.05, out_y, 0], [x1 + 0.92, out_y, 0], color=DESTRUCT, stroke_width=out_thick, stroke_opacity=0.72))
        for i in range(4):
            frac = (ph * (0.75 + 1.0 * open_f) + i * 0.25) % 1.0
            dx = x1 + 0.72 + frac * 0.72
            dy = out_y - 0.55 * (frac ** 1.6)
            stream.add(Dot([dx, dy, 0], radius=0.085 + 0.05 * open_f, color=DESTRUCT))
        gate_h = 0.30 * (1.0 - open_f)
        if gate_h > 0.02:
            gate = Rectangle(width=0.14, height=gate_h, stroke_color=WNT_GOLD, stroke_width=2,
                             fill_color=WNT_GOLD, fill_opacity=0.88).move_to([x1 + 0.36, y0 + 0.34 - gate_h / 2, 0])
            stream.add(gate)
        return stream

    streams = always_redraw(mk_streams)
    g = VGroup(fluid, ref30)
    if show_target:
        g.add(ref120)
    g.add(wall_l, wall_b, wall_r_top, drain_top, drain_bot, ticks, tap_pipe, tap_spout, streams)
    g.ref120 = ref120
    g.lbl120 = lbl120
    g.box = box
    g.tap_pos = [tap_x, y1 + 0.62, 0]
    g.drain_pos = [x1 + 0.36, y0 + 0.17, 0]
    return g


# ================================================================== SCENES
class S00Title(TitleCard):
    LESSON = "Wnt: β-Catenin and Planar Polarity"
    TITLE = "Wnt Slows the Drain"


class S01Hook(SpokenScene):
    """Synthesis tap pours coral β-catenin continuously into cytoplasm and violet drain shreds it."""

    def construct(self):
        cell = make_cell_shell()
        fzd = make_frizzled([cell.cx - 1.5, cell.mem_y - 0.02, 0])
        lrp = make_lrp([cell.cx + 0.2, cell.mem_y - 0.04, 0])
        tap = make_tap([-5.15, 1.35, 0])
        prot = make_proteasome([1.35, 0.35, 0])

        sim_t = ValueTracker(0.0)
        sim_t.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(sim_t)

        level = ValueTracker(STEADY_OFF)
        tank = make_side_tank(level, phase_tracker=sim_t)

        prot.blades.add_updater(lambda m, dt: m.rotate(1.4 * dt))

        def mk_stream():
            t = sim_t.get_value()
            g = VGroup()
            n = 6
            for i in range(n):
                u = (t * 0.28 + i / n) % 1.0
                if u < 0.80:
                    p = u / 0.80
                    x = -4.75 + p * 5.55
                    y = 0.78 - 0.38 * p + 0.14 * np.sin(p * PI + i)
                    blk = make_catenin_block([x, y, 0], size=0.30)
                    blk.set_opacity(min(1.0, u * 10.0))
                    g.add(blk)
                else:
                    p = (u - 0.80) / 0.20
                    for k, dx in enumerate((-0.16, 0.0, 0.16)):
                        dot = Dot([1.35 + dx * (1 + p), -0.22 - p * 0.34 - 0.04 * k, 0],
                                  radius=0.05, color=CATENIN).set_opacity(1.0 - p)
                        g.add(dot)
            return g

        stream = always_redraw(mk_stream)
        tap_lbl = T("Synthesis tap", 24, CATENIN).next_to(tap, UP, buff=0.22).shift(RIGHT * 0.35)
        prot_lbl = T("Drain (proteasome)", 24, DESTRUCT).next_to(prot, UP, buff=0.28).shift(LEFT * 0.55)
        cat_lbl = T("Free β-catenin", 28, CATENIN).move_to([-2.0, 1.52, 0])

        self.add(cell, fzd, lrp, tap, prot, tank, stream, scope_tag("schematic"))
        self.play(FadeIn(tap_lbl), run_time=0.8)

        self.at("only to destroy it")
        self.play(FadeIn(prot_lbl), run_time=0.9)

        self.at("free beta catenin")
        self.play(FadeIn(cat_lbl), run_time=0.9)

        self.at("fast responsive control switch")
        switch_tag = boxed_label("Always made, always drained", CATENIN, size=24, fill_opacity=0.18).move_to([-2.0, -0.52, 0])
        self.play(FadeIn(switch_tag), run_time=0.9)
        self.finish()


class S02OffComplex(SpokenScene):
    """No Wnt: stable junction pool is distinct; free β-catenin docks into Axin/APC/CK1/GSK3."""

    def construct(self):
        cell = make_cell_shell()
        fzd = make_frizzled([cell.cx - 1.55, cell.mem_y - 0.02, 0])
        lrp = make_lrp([cell.cx + 0.85, cell.mem_y - 0.04, 0])
        fzd_lbl = T("Frizzled", 24, TEAL).next_to(fzd, UP, buff=0.34)
        lrp_lbl = T("LRP5/6", 24, LRP_BLUE).next_to(lrp, UP, buff=0.24)
        no_wnt = boxed_label("No Wnt signal", GREY, size=24, fill_opacity=0.16).move_to([1.35, 3.22, 0])

        tap = make_tap([-5.15, 1.35, 0])
        prot = make_proteasome([1.65, -0.25, 0], scale=0.88)
        prot.blades.add_updater(lambda m, dt: m.rotate(2.4 * dt))

        sim_t = ValueTracker(0.0)
        sim_t.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(sim_t)

        level = ValueTracker(STEADY_OFF)
        tank = make_side_tank(level, phase_tracker=sim_t)

        cadherins = VGroup(*[
            Line([-6.10, 0.25 - i * 0.42, 0], [-5.80, 0.25 - i * 0.42, 0], color=TEAL, stroke_width=5)
            for i in range(3)
        ])
        junc_blocks = VGroup(*[
            make_catenin_block([-5.54, 0.25 - i * 0.42, 0], size=0.28)
            for i in range(3)
        ])
        junc_grp = VGroup(cadherins, junc_blocks)
        junc_lbl = T("Junction pool:\nstable", 24, CATENIN).next_to(junc_blocks, RIGHT, buff=0.20)

        comp = make_destruction_complex([-1.55, 0.15, 0], scale=0.84)
        docked_cat = make_catenin_block([-1.32, 0.15, 0], size=0.38, label=True, font_size=22)

        def mk_flow():
            t = sim_t.get_value()
            g = VGroup()
            for i in range(5):
                u = (t * 0.62 + i / 5.0) % 1.0
                x = -4.75 + u * 2.40
                y = 0.92 - 0.20 * u
                g.add(make_catenin_block([x, y, 0], size=0.30).set_opacity(1.0 - 0.65 * max(0, u - 0.75) / 0.25))
            return g

        flow = always_redraw(mk_flow)

        self.add(cell, fzd, lrp, fzd_lbl, lrp_lbl, no_wnt, tap, prot, tank, flow, scope_tag("schematic"))

        self.at("Stable beta")
        self.play(FadeIn(junc_grp), FadeIn(junc_lbl), run_time=1.0)

        self.at("untouched here")
        self.play(junc_grp.animate.set_opacity(0.45), junc_lbl.animate.set_opacity(0.70), run_time=0.9)

        self.at("Every free copy")
        comp_lbl = T("Destruction complex", 26, DESTRUCT).move_to([-2.75, 1.80, 0])
        self.play(Create(comp.axin), FadeIn(docked_cat, shift=LEFT * 0.4), FadeIn(comp_lbl), run_time=1.4)

        self.at("A violet scaffold")
        self.play(FadeIn(comp.axin_lab), run_time=0.9)

        self.at("holds two kinases")
        self.play(FadeIn(comp.ck1), FadeIn(comp.gsk3), run_time=1.1)

        self.at("A large partner")
        self.play(FadeIn(comp.apc), run_time=1.1)
        self.finish()


class S03OffTagDestroy(SpokenScene):
    """CK1 primes 1 phosphate, GSK3 adds 3 more, SCF (β-TrCP) adds Ub, proteasome shreds it; TCF OFF."""

    def construct(self):
        cell = make_cell_shell()
        fzd = make_frizzled([cell.cx - 1.55, cell.mem_y - 0.02, 0])
        lrp = make_lrp([cell.cx + 0.85, cell.mem_y - 0.04, 0])
        tap = make_tap([-5.15, 1.35, 0])

        comp = make_destruction_complex([-3.75, 0.22, 0], scale=0.85)
        comp.apc.shift(DOWN * 0.14)
        comp.gsk3.shift(UP * 0.06)
        cat = make_catenin_block([-3.08, -0.05, 0], size=0.40, label=True, font_size=22, min_w=1.82)

        scf_clamp = Arc(radius=1.02, start_angle=-PI * 0.72, angle=PI * 1.44, color=DESTRUCT, stroke_width=6).move_to([-0.38, 0.20, 0])
        scf_lbl = T("SCF (β-TrCP)", 24, DESTRUCT).next_to(scf_clamp, UP, buff=0.18)
        prot = make_proteasome([1.62, -0.20, 0], scale=0.88)
        prot.blades.add_updater(lambda m, dt: m.rotate(2.6 * dt))
        prot_lbl = T("Proteasome", 24, DESTRUCT).next_to(prot, UP, buff=0.26).shift(LEFT * 0.22)

        tcf = boxed_label("TCF", EMERALD, size=24, pad=0.14, fill_opacity=0.25).move_to([cell.cx - 1.85, cell.dna_y + 0.40, 0])
        groucho = boxed_label("Groucho", GROUCHO, size=24, pad=0.14, fill_opacity=0.25).next_to(tcf, RIGHT, buff=0.16)
        off_badge = boxed_label("Target genes: OFF", GROUCHO, size=24, pad=0.16, fill_opacity=0.18).move_to([cell.cx + 2.05, -1.78, 0])

        sim_t = ValueTracker(0.0)
        sim_t.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(sim_t)

        level = ValueTracker(STEADY_OFF)
        tank = make_side_tank(level, phase_tracker=sim_t)

        def mk_cyto_flow():
            t = sim_t.get_value()
            g = VGroup()
            for i in range(3):
                u = (t * 0.55 + i / 3.0) % 1.0
                x = -5.12 + u * 0.55
                y = 0.90 - 0.65 * u
                g.add(make_catenin_block([x, y, 0], size=0.18).set_opacity(1.0 - 0.7 * max(0, u - 0.7) / 0.3))
            return g

        cyto_flow = always_redraw(mk_cyto_flow)

        def p_badge(pos):
            c = Circle(radius=0.22, stroke_color=WNT_GOLD, stroke_width=2, fill_color=WNT_GOLD, fill_opacity=0.92).move_to(pos)
            l = T("P", 22, BG, weight=BOLD).move_to(c)
            return VGroup(c, l)

        # Space 4 P badges cleanly above cat (y=0.51), clear of cyto_flow & GSK3
        p_xs = [-3.72, -3.30, -2.88, -2.46]
        p1 = p_badge([p_xs[0], 0.51, 0])
        p234 = [p_badge([x, 0.51, 0]) for x in p_xs[1:]]

        self.add(cell, fzd, lrp, tap, comp, cat, scf_clamp, scf_lbl, prot, prot_lbl,
                 tcf, groucho, off_badge, tank, cyto_flow, scope_tag("schematic"))

        self.at("adds a priming phosphate")
        self.play(comp.ck1.animate.shift(UP * 0.08), run_time=0.35)
        self.play(FadeIn(p1, scale=1.25), comp.ck1.animate.shift(DOWN * 0.08), run_time=0.65)

        self.at("That lets")
        self.play(comp.gsk3.animate.shift(UP * 0.08), run_time=0.35)
        for p in p234:
            self.play(FadeIn(p, scale=1.25), run_time=0.65)
        self.play(comp.gsk3.animate.shift(DOWN * 0.08), run_time=0.35)

        self.at("Next")
        tagged = VGroup(cat, p1, *p234)
        self.play(tagged.animate.move_to([-0.65, 0.22, 0]), run_time=1.4)

        self.at("inside an SCF")
        ub_chain = VGroup(*[
            Dot([-1.15 + i * 0.13, -0.51, 0], radius=0.075, color=DESTRUCT)
            for i in range(4)
        ])
        ub_lbl = T("Ub", 22, DESTRUCT, weight=BOLD).next_to(ub_chain, RIGHT, buff=0.08)
        self.play(LaggedStart(*[FadeIn(u, scale=1.2) for u in ub_chain], lag_ratio=0.15), FadeIn(ub_lbl), run_time=0.7)

        self.at("proteasome")
        all_cargo = VGroup(tagged, ub_chain, ub_lbl)
        self.play(FadeOut(all_cargo, target_position=prot.get_center(), scale=0.35), run_time=1.1)
        frags = VGroup(*[
            Dot([1.55 + (i - 1.5) * 0.22, -0.82 - (i % 2) * 0.12, 0], radius=0.055, color=CATENIN)
            for i in range(4)
        ])
        self.play(FadeIn(frags), frags.animate.shift(DOWN * 0.22).set_opacity(0.15), run_time=0.9)
        self.finish()


def build_predict_backdrop():
    """Exact shared backdrop for S04PredictSetup end frame and S05Pause."""
    level_t = ValueTracker(STEADY_OFF)
    drain_open_t = ValueTracker(0.25)
    tap_phase_t = ValueTracker(0.0)
    tap_phase_t.add_updater(lambda m, dt: m.increment_value(dt))
    tank = make_big_tank(level_t, drain_open_t, tap_phase_t)
    syn_lbl = T("Synthesis: 12 / min", 26, CATENIN).next_to(tank.tap_pos, RIGHT, buff=0.55).shift(UP * 0.08)
    drain_lbl = T("k: 0.1 / min (1/4 rate)", 26, DESTRUCT).move_to([-2.65, -2.02, 0])
    lvl_lbl = M("30 units", 28, CATENIN).move_to([-2.65, -0.35, 0])
    return VGroup(tank, syn_lbl, drain_lbl, lvl_lbl, scope_tag("schematic")), tap_phase_t


class S04PredictSetup(SpokenScene):
    """Tank analogy: synthesis 12/min, open drain k=0.4/min -> 30; valve narrows drain to 1/4."""

    def construct(self):
        level_t = ValueTracker(STEADY_OFF)
        drain_open_t = ValueTracker(1.0)
        tap_phase_t = ValueTracker(0.0)
        tap_phase_t.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(tap_phase_t)

        tank = make_big_tank(level_t, drain_open_t, tap_phase_t)
        syn_lbl = T("Synthesis: 12 / min", 26, CATENIN).next_to(tank.tap_pos, RIGHT, buff=0.55).shift(UP * 0.08)
        drain_lbl_open = T("Destruction k: 0.4 / min", 26, DESTRUCT).move_to([-2.65, -2.02, 0])
        drain_lbl_narrow = T("k: 0.1 / min (1/4 rate)", 26, DESTRUCT).move_to([-2.65, -2.02, 0])
        lvl_lbl = M("30 units", 28, CATENIN).move_to([-2.65, -0.35, 0])

        q = question_card(
            "Destruction cut to 1/4, synthesis steady: steady level?",
            ["Stays flat", "Drops to 1/4", "Rises 4x"],
            chips_at=[4.2, 0.8, 0],
        )

        self.play(FadeIn(tank), FadeIn(lvl_lbl), FadeIn(scope_tag("schematic")), run_time=1.0)

        self.at("A running tap")
        self.play(FadeIn(syn_lbl), run_time=0.9)

        self.at("open drain")
        self.play(FadeIn(drain_lbl_open), run_time=0.9)

        self.at("If a signal slows destruction")
        self.play(
            drain_open_t.animate.set_value(0.25),
            swap(drain_lbl_open, drain_lbl_narrow, run_time=0.8),
            run_time=2.2,
        )

        self.at("how does the level change")
        self.play(FadeIn(q.chips), FadeIn(q.question), run_time=1.0)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = "Destruction cut to 1/4, synthesis steady: steady level?"
    OPTIONS = ["Stays flat", "Drops to 1/4", "Rises 4x"]
    CHIPS_AT = [4.2, 0.8, 0]
    RING_AT = (6.0, -2.15, 0)
    SECONDS = 4.5

    def backdrop(self):
        bg, tap_phase_t = build_predict_backdrop()
        self.add(tap_phase_t)
        return bg


class S06PredictReveal(SpokenScene):
    """Rises 4x highlights; tank, live counter, and computed curve climb while rule and both cases build."""

    def construct(self):
        level_t = ValueTracker(STEADY_OFF)
        drain_open_t = ValueTracker(0.25)
        tap_phase_t = ValueTracker(0.0)
        tap_phase_t.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(tap_phase_t)

        t_min = ValueTracker(0.0)
        climb_active = [False]

        def _climb(m, dt):
            if climb_active[0] and m.get_value() < 60.0:
                m.set_value(min(60.0, m.get_value() + 5.5 * dt))

        def _level_now():
            val = c_climb(t_min.get_value())
            return STEADY_ON if STEADY_ON - val <= 0.5 else val

        t_min.add_updater(_climb)
        self.add(t_min)
        level_t.add_updater(lambda m: m.set_value(_level_now()))
        self.add(level_t)

        tank = make_big_tank(level_t, drain_open_t, tap_phase_t)
        syn_lbl = T("Synthesis: 12 / min", 26, CATENIN).next_to(tank.tap_pos, RIGHT, buff=0.55).shift(UP * 0.08)
        drain_lbl = T("k: 0.1 / min (1/4 rate)", 26, DESTRUCT).move_to([-2.65, -2.02, 0])
        live_num = always_redraw(lambda: M(f"{_level_now():.0f} units", 28, CATENIN).move_to([-2.65, 2.65, 0]))

        q = question_card(
            "Destruction cut to 1/4, synthesis steady: steady level?",
            ["Stays flat", "Drops to 1/4", "Rises 4x"],
            chips_at=[4.2, 0.8, 0],
        )

        P = Plot(
            box=(1.85, 5.65, 0.25, 2.25),
            xr=(0, 60),
            yr=(0, 150),
            xticks=[0, 15, 30, 45, 60],
            yticks=[(0, "0"), (30, "30"), (120, "120")],
            xlabel="time (min)",
            ylabel="free β-catenin",
        )
        h120 = P.hline(120, "120 (4×)", WNT_GOLD, size=24)
        h120[1].shift(UP * 0.08)
        live_c = P.live_curve(c_climb, t_min, color=CATENIN, width=5)
        dot_c = P.dot(lambda: t_min.get_value(), lambda: c_climb(t_min.get_value()), color=CATENIN, ring=WNT_GOLD)

        rule_level = T("Level", 24, TEXT)
        rule_eq = M("=", 24, TEXT)
        rule_syn = T("synthesis", 24, CATENIN)
        rule_div = M("÷", 24, TEXT)
        rule_des = T("destruction rate", 24, DESTRUCT)
        rule_grp = VGroup(rule_level, rule_eq, rule_syn, rule_div, rule_des).arrange(RIGHT, buff=0.06).move_to([4.22, -1.56, 0])

        c1_12 = M("12", 26, CATENIN)
        c1_div = M("÷", 26, TEXT)
        c1_k = M("0.4", 26, DESTRUCT)
        c1_eq = M("=", 26, TEXT)
        c1_res = M("30", 26, GREY)
        c1_grp = VGroup(c1_12, c1_div, c1_k, c1_eq, c1_res).arrange(RIGHT, buff=0.14).move_to([4.05, -2.10, 0])

        c2_12 = M("12", 26, CATENIN)
        c2_div = M("÷", 26, TEXT)
        c2_k = M("0.1", 26, DESTRUCT)
        c2_eq = M("=", 26, TEXT)
        c2_res = M("120", 26, WNT_GOLD)
        c2_4x = M("(4×)", 26, WNT_GOLD)
        c2_grp = VGroup(c2_12, c2_div, c2_k, c2_eq, c2_res, c2_4x).arrange(RIGHT, buff=0.14).next_to(c1_grp, DOWN, buff=0.16).align_to(c1_grp, LEFT)

        self.add(tank, syn_lbl, drain_lbl, q, scope_tag("schematic"))

        self.at("The level rises")
        win_chip = q.chips[2]
        losers = VGroup(q.chips[0], q.chips[1], q.question)
        self.play(
            win_chip[0].animate.set_stroke(EMERALD, 3.5).set_fill(EMERALD, 0.28),
            win_chip[1].animate.set_color(EMERALD),
            win_chip.animate.move_to([4.90, 2.95, 0]),
            FadeOut(losers),
            run_time=0.55,
        )
        self.play(
            Create(P),
            FadeIn(tank.ref120),
            tank.lbl120.animate.set_color(WNT_GOLD),
            FadeIn(h120),
            FadeIn(live_num),
            run_time=0.75,
        )
        self.add(live_c, dot_c)
        climb_active[0] = True

        self.at("level equals")
        self.play(FadeIn(rule_level), run_time=0.22)
        self.play(FadeIn(rule_eq), run_time=0.18)

        self.at("synthesis")
        self.play(FadeIn(rule_syn), run_time=0.35)

        self.at("divided by")
        self.play(FadeIn(rule_div), run_time=0.35)

        self.at("destruction rate")
        self.play(FadeIn(rule_des), run_time=0.45)

        self.at("Twelve over point four")
        self.play(FadeIn(c1_12), run_time=0.22)
        self.play(FadeIn(c1_div), run_time=0.20)
        self.play(FadeIn(c1_k), run_time=0.32)

        self.at("gives thirty")
        self.play(FadeIn(c1_eq), run_time=0.20)
        self.play(FadeIn(c1_res), run_time=0.35)

        self.at("twelve over point one")
        self.play(FadeIn(c2_12), run_time=0.22)
        self.play(FadeIn(c2_div), run_time=0.20)
        self.play(FadeIn(c2_k), run_time=0.32)

        self.at("gives one hundred twenty")
        self.play(FadeIn(c2_eq), run_time=0.20)
        self.play(FadeIn(c2_res), run_time=0.35)
        self.play(FadeIn(c2_4x), run_time=0.30)

        self.at("Synthesis never changed")
        self.play(
            Indicate(syn_lbl, color=CATENIN, scale_factor=1.06),
            Indicate(c1_12, color=CATENIN, scale_factor=1.12),
            Indicate(c2_12, color=CATENIN, scale_factor=1.12),
            run_time=1.4,
        )

        self.at("That is how")
        self.play(
            Indicate(win_chip, color=EMERALD, scale_factor=1.06),
            Indicate(h120, color=WNT_GOLD, scale_factor=1.06),
            run_time=1.5,
        )

        self.at("by slowing its constant destruction")
        self.play(
            Indicate(drain_lbl, color=WNT_GOLD, scale_factor=1.06),
            Indicate(c2_k, color=WNT_GOLD, scale_factor=1.12),
            Indicate(c2_res, color=WNT_GOLD, scale_factor=1.10),
            run_time=1.8,
        )
        self.finish()


class S07WntReceptor(SpokenScene):
    """Gold Wnt with curved lipid tail grips teal Frizzled's groove and pulls slate-blue LRP5/6 snug."""

    def construct(self):
        cell = make_cell_shell(x0=-6.1, x1=2.45, mem_y=0.65, nuc_top=-2.15, nuc_bot=-3.40)
        fzd = make_frizzled([cell.cx - 1.35, cell.mem_y - 0.02, 0], scale=1.30)
        lrp = make_lrp([cell.cx + 1.35, cell.mem_y - 0.18, 0], scale=1.30, tall=1.25)
        fzd_lbl = T("Frizzled", 28, TEAL).next_to(fzd, DOWN, buff=0.25)
        lrp_lbl = T("LRP5/6", 28, LRP_BLUE).next_to(lrp, RIGHT, buff=0.38).shift(UP * 0.68)

        wnt = make_wnt([-4.8, 2.55, 0], scale=1.10)
        lipid_lbl = T("lipid tail", 24, WNT_GOLD).next_to(wnt.tail, LEFT, buff=0.18)

        sim_t = ValueTracker(0.0)
        sim_t.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(sim_t)

        level = ValueTracker(STEADY_OFF)
        tank = make_side_tank(level, phase_tracker=sim_t, show_target=True)
        tap = make_tap([-5.15, -0.35, 0])
        prot = make_proteasome([1.60, -1.15, 0], scale=0.85)
        prot.blades.add_updater(lambda m, dt: m.rotate(1.4 * dt))

        def mk_flow():
            t = sim_t.get_value()
            g = VGroup()
            for i in range(4):
                u = (t * 0.25 + i / 4.0) % 1.0
                x = -4.75 + u * 5.8
                y = -0.95 - 0.22 * u
                g.add(make_catenin_block([x, y, 0], size=0.25).set_opacity(1.0 - 0.7 * max(0, u - 0.75) / 0.25))
            return g

        flow = always_redraw(mk_flow)

        self.add(cell, fzd, lrp, fzd_lbl, lrp_lbl, tap, prot, tank, flow, scope_tag("schematic"))
        self.play(FadeIn(wnt, shift=DOWN * 0.25), FadeIn(lipid_lbl), run_time=1.4)

        self.at("Outside the cell")
        target_wnt_pos = fzd.get_top() + UP * 0.42 + RIGHT * 0.28
        self.play(wnt.animate.move_to(target_wnt_pos), FadeOut(lipid_lbl), run_time=2.8)
        lipid_in_lbl = T("lipid in groove", 24, WNT_GOLD).next_to(wnt, UP, buff=0.16)
        self.play(FadeIn(lipid_in_lbl), run_time=0.8)

        self.at("At the same time")
        new_lrp_x = fzd.get_right()[0] + 0.55
        self.play(lrp.animate.set_x(new_lrp_x), lrp_lbl.animate.set_x(new_lrp_x + 1.10), run_time=2.8)
        self.finish()


class S08ComplexPulled(SpokenScene):
    """Dishevelled docks beneath Frizzled, LRP6 tail gains phosphates, complex glides up; shredder idles."""

    def construct(self):
        cell = make_cell_shell(x0=-6.1, x1=2.45, mem_y=1.15, nuc_top=-2.15, nuc_bot=-3.40)
        fzd = make_frizzled([cell.cx - 1.55, cell.mem_y - 0.02, 0], scale=1.22)
        lrp = make_lrp([fzd.get_right()[0] + 0.65, cell.mem_y - 0.67, 0], scale=1.22, tall=3.1)
        lrp[0].layout_ok = True  # blue intracellular stalk intentionally passes behind the P phosphate badges
        wnt = make_wnt(fzd.get_top() + UP * 0.40 + RIGHT * 0.28, scale=1.05)
        fzd_lbl = T("Frizzled", 24, TEAL).next_to(fzd, LEFT, buff=0.22).shift(UP * 0.35)
        lrp_lbl = T("LRP5/6", 24, LRP_BLUE).next_to(lrp[1], RIGHT, buff=0.22)

        dvl = boxed_label("Dishevelled", DVL_AMBER, size=24, fill_opacity=0.26).move_to([fzd.get_center()[0] - 0.10, -1.25, 0])
        comp = make_destruction_complex([-0.35, -0.88, 0], scale=0.72)
        prot = make_proteasome([1.68, -1.05, 0], scale=0.85)
        tap = make_tap([-5.15, -1.45, 0])

        sim_t = ValueTracker(0.0)
        sim_t.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(sim_t)

        shred_speed = ValueTracker(1.0)
        prot.blades.add_updater(lambda m, dt: m.rotate(2.4 * shred_speed.get_value() * dt))

        level = ValueTracker(STEADY_OFF)
        tank = make_side_tank(level, phase_tracker=sim_t, drain_rate_tracker=shred_speed, show_target=True)

        def mk_flow():
            t = sim_t.get_value()
            escape = float(np.clip((1.0 - shred_speed.get_value()) / 0.9, 0.0, 1.0))
            g = VGroup()
            for i in range(5):
                u = (t * 0.34 + i / 5.0) % 1.0
                x = -4.98 + u * (6.60 + 0.38 * escape)
                drop = min(1.0, u / 0.16)
                base_y = -1.76 - 0.18 * drop + 0.02 * np.sin(u * PI * 2.0)
                pull = (1.0 - escape) * (max(0.0, (u - 0.92) / 0.08) ** 1.2)
                y = base_y * (1.0 - pull) + (-1.42) * pull
                op = min(1.0, u * 12.0) * (1.0 - (1.0 - escape) * max(0.0, (u - 0.90) / 0.10))
                if escape > 0.05 and u > 0.92:
                    op *= max(0.0, 1.0 - (u - 0.92) / 0.08 * escape)
                g.add(make_catenin_block([x, y, 0], size=0.25).set_opacity(float(np.clip(op, 0.0, 1.0))))
            if escape > 0.05:
                pool_spots = [(-1.35, -1.80), (0.05, -1.86), (1.05, -1.92), (1.88, -1.82)]
                for k, (px, py) in enumerate(pool_spots):
                    by = py + 0.03 * np.sin(t * 2.0 + k * 1.4)
                    g.add(make_catenin_block([px, by, 0], size=0.25).set_opacity(0.92 * escape))
            return g

        flow = always_redraw(mk_flow)

        self.add(cell, fzd, lrp, wnt, fzd_lbl, lrp_lbl, comp, prot, tap, tank, flow, scope_tag("schematic"))

        self.at("Inside the cell")
        dvl_target = [fzd.get_center()[0] - 0.25, fzd.get_bottom()[1] - 0.45, 0]
        self.play(FadeIn(dvl, shift=UP * 0.35), dvl.animate.move_to(dvl_target), run_time=2.5)

        self.at("Meanwhile")
        tail_x = lrp.get_center()[0]
        p_dots = VGroup(*[
            VGroup(Dot([tail_x, 0.22 - i * 0.38, 0], radius=0.145, color=WNT_GOLD),
                   T("P", 22, BG, weight=BOLD).move_to([tail_x, 0.22 - i * 0.38, 0]))
            for i in range(3)
        ])
        self.play(LaggedStart(*[FadeIn(p, scale=1.25) for p in p_dots], lag_ratio=0.35), run_time=2.8)

        self.at("The destruction complex moves up")
        delta = np.array([tail_x + 1.28, -0.15, 0]) - comp.axin.get_center()
        tether = Line([tail_x + 0.16, -0.16, 0], [tail_x + 0.93, -0.16, 0], color=WNT_GOLD, stroke_width=3.5)
        self.play(comp.animate.shift(delta), run_time=2.0)
        self.play(Create(tether), run_time=0.4)

        self.at("where it stops")
        debate_note = boxed_label("How complex stops: debated", WNT_GOLD, size=24, fill_opacity=0.18).move_to([-4.35, 2.95, 0])
        idle_lbl = T("Drain idling", 24, GREY).next_to(prot, UP, buff=0.22).shift(LEFT * 0.20)
        self.play(
            FadeIn(debate_note),
            FadeIn(idle_lbl),
            shred_speed.animate.set_value(0.1),
            level.animate.set_value(45.0),
            run_time=2.5,
        )
        self.finish()


class S09NucleusTcf(SpokenScene):
    """Coral β-catenin survives, fills cytoplasm, climbs tank (30->120), enters nucleus to TCF+Groucho."""

    def construct(self):
        cell = make_cell_shell(x0=-6.1, x1=2.45, mem_y=2.25, nuc_top=-0.95, nuc_bot=-3.25)
        fzd = make_frizzled([cell.cx - 0.85, cell.mem_y - 0.02, 0])
        lrp = make_lrp([fzd.get_right()[0] + 0.55, cell.mem_y - 0.14, 0])
        wnt = make_wnt(fzd.get_top() + UP * 0.36 + RIGHT * 0.22, scale=0.90, font_size=24)
        dvl = boxed_label("Dishevelled", DVL_AMBER, size=22, fill_opacity=0.24).move_to([fzd.get_center()[0] - 0.72, cell.mem_y - 0.76, 0])
        comp = make_destruction_complex([lrp.get_center()[0] + 0.40, 1.38, 0], scale=0.55, show_labels=False)
        comp_tag = T("Complex tethered", 24, DESTRUCT).move_to([0.85, 0.80, 0])
        debate = T("How stopped: debated", 24, WNT_GOLD).move_to([0.75, 2.95, 0])

        tap = make_tap([-5.15, 0.85, 0])
        tcf = boxed_label("TCF", EMERALD, size=26, pad=0.14, fill_opacity=0.26).move_to([cell.cx - 0.45, cell.dna_y + 0.36, 0])
        groucho = boxed_label("Groucho", GROUCHO, size=26, pad=0.14, fill_opacity=0.26).next_to(tcf, RIGHT, buff=0.14)
        dna_lbl = T("Target DNA", 24, GREY).next_to([cell.cx - 2.3, cell.dna_y, 0], UP, buff=0.14)

        sim_t = ValueTracker(0.0)
        sim_t.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(sim_t)

        t_min = ValueTracker(5.0)
        level = ValueTracker(c_climb(5.0))
        level.add_updater(lambda m: m.set_value(c_climb(t_min.get_value())))
        self.add(level)
        tank = make_side_tank(level, phase_tracker=sim_t, drain_rate_tracker=ValueTracker(0.25), show_target=True)

        rng = np.random.default_rng(7)
        seeds = rng.uniform(0, 1, size=(12, 3))

        def mk_accumulation():
            t = sim_t.get_value()
            frac = float(np.clip((t - 2.5) / 10.5, 0.18, 1.0))
            n_vis = max(2, int(round(12 * frac)))
            g = VGroup()
            for i in range(n_vis):
                s0, s1, s2 = seeds[i]
                if i < 7:
                    px = -4.65 + ((s0 + t * 0.06) % 1.0) * 6.0
                    py = -0.22 + s1 * 0.58
                    g.add(make_catenin_block([px, py, 0], size=0.24))
                else:
                    pore_x = cell.pores[i % 2]
                    u = (s2 + t * 0.14) % 1.0
                    py = 0.02 - u * 1.80
                    px = pore_x
                    g.add(make_catenin_block([px, py, 0], size=0.22))
            return g

        cloud = always_redraw(mk_accumulation)

        self.add(cell, fzd, lrp, wnt, dvl, comp, comp_tag, debate, tap, tcf, groucho, dna_lbl, tank, cloud, scope_tag("schematic"))
        self.play(t_min.animate.set_value(12.0), run_time=5.0, rate_func=linear)

        self.at("Newly made")
        self.play(FadeOut(debate), t_min.animate.set_value(26.0), run_time=4.2, rate_func=linear)

        self.at("enters the nucleus")
        pore_lbl = T("Nuclear\npores", 22, GREY, line_spacing=0.58).move_to([cell.cx, -0.52, 0])
        self.play(FadeIn(pore_lbl), t_min.animate.set_value(35.0), run_time=2.2, rate_func=linear)

        self.at("There it finds")
        self.play(FadeOut(pore_lbl), t_min.animate.set_value(45.0), run_time=4.2, rate_func=linear)
        self.finish()


class S10GenesAndCancer(SpokenScene):
    """β-Catenin displaces Groucho to switch genes ON; then broken APC / P-site inset stays ON with no Wnt."""

    def construct(self):
        dna_y = -1.25
        dna1 = Line([-5.8, dna_y + 0.05, 0], [1.2, dna_y + 0.05, 0], color=MEMBRANE, stroke_width=3.5)
        dna2 = Line([-5.8, dna_y - 0.05, 0], [1.2, dna_y - 0.05, 0], color=MEMBRANE, stroke_width=3.5)
        nuc_arc = RoundedRectangle(corner_radius=0.35, width=7.5, height=5.0,
                                   stroke_color=MEMBRANE, stroke_width=3, fill_color=NUC_BG, fill_opacity=0.80).move_to([-2.3, -0.35, 0])

        tcf = boxed_label("TCF", EMERALD, size=28, box=(1.20, 0.56), pad=0.08, fill_opacity=0.28).move_to([-3.3, dna_y + 0.36, 0])
        groucho = boxed_label("Groucho", GROUCHO, size=26, box=(1.55, 0.52), pad=0.08, fill_opacity=0.28).next_to(tcf, RIGHT, buff=0.10)
        cat_nucl = make_catenin_block([-4.9, 1.05, 0], size=0.52, label=True, font_size=24)
        coact = boxed_label("Coactivators", EMERALD, size=24, fill_opacity=0.24).move_to([-2.1, 1.05, 0])
        simple_lbl = T("Simple model", 24, GREY).move_to([-4.6, 1.68, 0])

        status_off = boxed_label("Target genes: OFF", GROUCHO, size=26, fill_opacity=0.18).move_to([-2.3, -2.20, 0])
        status_on = boxed_label("Target genes: ON", EMERALD, size=26, fill_opacity=0.25).move_to([-2.3, -2.20, 0])

        wave_on = ValueTracker(0.0)
        phase = ValueTracker(0.0)
        phase.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(phase)

        def mk_waves():
            active = wave_on.get_value()
            ph = phase.get_value()
            g = VGroup()
            if active > 0.2:
                # Moving emerald transcription pulse wave along DNA
                pts = [[-1.3 + 2.3 * (j / 24.0), dna_y + 0.36 + 0.14 * np.sin(j * 0.65 - ph * 5.0), 0] for j in range(25)]
                wline = VMobject(stroke_color=EMERALD, stroke_width=4.5, stroke_opacity=active, fill_opacity=0).set_points_as_corners(pts)
                g.add(wline)
                for k in range(4):
                    u = (ph * 0.65 + k / 4.0) % 1.0
                    wx = -1.3 + u * 2.2
                    wy = dna_y + 0.36 + 0.14 * np.sin((u * 24.0) * 0.65 - ph * 5.0)
                    g.add(Dot([wx, wy, 0], radius=0.09, color=EMERALD).set_opacity(active * (1.0 - 0.3 * u)))
                # Surviving β-catenin blocks drifting through nucleus above TCF
                for k in range(3):
                    u = (ph * 0.40 + k / 3.0) % 1.0
                    bx = -5.2 + u * 1.4
                    by = 0.65 - 0.25 * u
                    g.add(make_catenin_block([bx, by, 0], size=0.22).set_opacity(active * (1.0 - 0.4 * u)))
            return g

        waves = always_redraw(mk_waves)

        level = ValueTracker(STEADY_ON)
        tank = make_side_tank(level, phase_tracker=phase, drain_rate_tracker=ValueTracker(0.25), show_target=True)

        self.add(nuc_arc, dna1, dna2, tcf, groucho, cat_nucl, simple_lbl, status_off, waves, tank, scope_tag("schematic"))

        self.play(
            cat_nucl.animate.move_to(tcf.get_top() + UP * 0.32),
            groucho.animate.shift(RIGHT * 1.3 + UP * 1.2).set_opacity(0.0),
            run_time=2.0,
        )
        self.remove(groucho)

        self.at("brings in")
        self.play(FadeIn(coact, shift=DOWN * 0.15), run_time=0.45)
        self.play(coact.animate.next_to(cat_nucl, RIGHT, buff=0.14), run_time=0.85)

        self.at("switch target genes")
        self.play(
            swap(status_off, status_on, run_time=0.7),
            wave_on.animate.set_value(1.0),
            run_time=1.4,
        )
        self.remove(status_off)

        self.at("Notice what happens")
        inset = RoundedRectangle(corner_radius=0.18, width=4.65, height=5.8,
                                 stroke_color=MUTATION, stroke_width=2.8, fill_color=CYTO_BG, fill_opacity=0.95).move_to([3.95, 0.1, 0])
        inset_hdr = T("Mutation", 26, MUTATION, weight=BOLD).move_to([3.95, 2.65, 0])
        no_wnt_m = T("No Wnt", 22, GREY).move_to([3.95, 2.22, 0])
        fzd_m = make_frizzled([3.20, 1.55, 0], scale=0.70)
        lrp_m = make_lrp([4.65, 1.50, 0], scale=0.70)

        apc_l = RoundedRectangle(corner_radius=0.06, width=0.66, height=0.44,
                                 stroke_color=DESTRUCT, stroke_width=2.5, fill_color=DESTRUCT, fill_opacity=0.25).move_to([2.45, 0.45, 0])
        apc_r = RoundedRectangle(corner_radius=0.06, width=0.66, height=0.44,
                                 stroke_color=DESTRUCT, stroke_width=2.5, fill_color=DESTRUCT, fill_opacity=0.25).move_to([3.25, 0.40, 0])
        crack = Line([2.82, 0.72, 0], [2.88, 0.12, 0], color=MUTATION, stroke_width=3.5)
        apc_lbl = T("Broken APC", 22, MUTATION).move_to([2.85, -0.10, 0])

        cat_mut = make_catenin_block([5.05, 0.45, 0], size=0.42, label=True, font_size=22)
        no_p_lbl = T("or no P sites", 22, MUTATION).move_to([5.05, -0.10, 0])

        inset_bar_bg = RoundedRectangle(corner_radius=0.08, width=3.6, height=0.42,
                                        stroke_color=GREY, stroke_width=2.2, fill_color=BG, fill_opacity=0.8).move_to([3.95, -0.95, 0])
        inset_bar_fill = Rectangle(width=2.88, height=0.34, stroke_width=0, fill_color=CATENIN, fill_opacity=0.78).move_to([3.61, -0.95, 0])
        inset_bar_lbl = M("Free β-cat: 120", 24, CATENIN).move_to([3.95, -1.48, 0])
        stuck_lbl = boxed_label("Broken drain: stuck ON", EMERALD, size=24, fill_opacity=0.25).move_to([3.95, -2.25, 0])

        self.play(FadeOut(tank), run_time=0.35)
        self.remove(tank)
        self.play(
            FadeIn(VGroup(inset, inset_hdr, no_wnt_m, fzd_m, lrp_m, apc_l, apc_r, crack, apc_lbl, cat_mut, no_p_lbl)),
            run_time=2.1,
        )

        self.at("Destruction slows")
        self.play(FadeIn(VGroup(inset_bar_bg, inset_bar_fill, inset_bar_lbl, stuck_lbl)), run_time=2.2)
        self.finish()


class S11Wrap(SpokenScene):
    """Side-by-side comparison: 'No Wnt' (open drain, 30, OFF) vs '+ Wnt' (slowed drain, 120, ON)."""

    def construct(self):
        tp = TwoPanel("No Wnt", "+ Wnt", colors=(DESTRUCT, CATENIN), top=3.20, bottom=-2.40, gap=0.45, width=12.6, size=32)
        sim_t = ValueTracker(0.0)
        sim_t.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(sim_t)

        lc = tp.area("left")[0]
        rc = tp.area("right")[0]

        def build_half(cx, wnt_on):
            g = VGroup()
            mem_y = 1.32
            mem = Line([cx - 2.6, mem_y, 0], [cx + 2.6, mem_y, 0], color=MEMBRANE, stroke_width=3)
            fzd = make_frizzled([cx - 0.85, mem_y, 0], scale=0.72)
            lrp = make_lrp([cx + 0.25 if wnt_on else cx + 0.75, mem_y - 0.08, 0], scale=0.72)
            g.add(mem, fzd, lrp)

            syn = T("Synthesis: 12 / min", 24, CATENIN).move_to([cx - 1.25, 0.44, 0])
            g.add(syn)

            tx = cx + 1.90
            t_bg = RoundedRectangle(corner_radius=0.06, width=0.82, height=1.75,
                                    stroke_color=GREY, stroke_width=2.5, fill_color=CYTO_BG, fill_opacity=0.65).move_to([tx, -0.25, 0])
            fh = 1.36 if wnt_on else 0.35
            t_fill = Rectangle(width=0.74, height=fh, stroke_width=0, fill_color=CATENIN, fill_opacity=0.76)
            t_fill.move_to([tx, -1.12 + 0.03 + fh / 2, 0])
            t_num = M("120" if wnt_on else "30", 24, CATENIN).move_to([tx, -1.38, 0])
            g.add(t_bg, t_fill, t_num)

            if not wnt_on:
                comp = make_destruction_complex([cx + 0.55, -0.18, 0], scale=0.40, show_labels=False)
                drain_lbl = T("Open drain: k = 0.4", 24, DESTRUCT).move_to([cx - 0.55, -0.88, 0])
                dna = Line([cx - 2.3, -1.42, 0], [cx + 1.0, -1.42, 0], color=MEMBRANE, stroke_width=3)
                badge = boxed_label("Genes: OFF", GROUCHO, size=24, pad=0.20, fill_opacity=0.20).move_to([cx - 0.55, -1.94, 0])
                g.add(comp, drain_lbl, dna, badge)
            else:
                wnt = make_wnt([cx - 0.45, mem_y + 0.48, 0], scale=0.72, font_size=22)
                dvl = RoundedRectangle(corner_radius=0.06, width=0.70, height=0.22,
                                       stroke_color=DVL_AMBER, stroke_width=2, fill_color=DVL_AMBER, fill_opacity=0.50).move_to([cx - 0.85, mem_y - 0.42, 0])
                comp = make_destruction_complex([cx + 0.72, mem_y - 0.65, 0], scale=0.38, show_labels=False)
                drain_lbl = T("Slowed drain: k = 0.1", 24, DESTRUCT).move_to([cx - 0.55, -0.88, 0])
                dna = Line([cx - 2.3, -1.42, 0], [cx + 1.0, -1.42, 0], color=EMERALD, stroke_width=3.5)
                badge = boxed_label("Genes: ON", EMERALD, size=24, pad=0.20, fill_opacity=0.25).move_to([cx - 0.55, -1.94, 0])
                g.add(wnt, dvl, comp, drain_lbl, dna, badge)
            return g

        left_half = build_half(lc[0], wnt_on=False)
        right_half = build_half(rc[0], wnt_on=True)

        def mk_particles():
            t = sim_t.get_value()
            g = VGroup()
            for i in range(4):
                u = (t * 0.68 + i / 4.0) % 1.0
                px = (lc[0] - 2.1) + u * 1.5
                py = 0.05 - 0.25 * u
                g.add(make_catenin_block([px, py, 0], size=0.21).set_opacity(1.0 - u))
            for i in range(6):
                u = (t * 0.52 + i / 6.0) % 1.0
                px = (rc[0] - 2.1) + u * 2.3
                py = 0.05 - 0.45 * u
                g.add(make_catenin_block([px, py, 0], size=0.22))
            return g

        particles = always_redraw(mk_particles)
        cap = caption("The cell turns the pathway on by slowing constant destruction.", size=28, color=TEXT, y=-3.05)

        self.add(tp, scope_tag("schematic"))
        self.play(FadeIn(left_half[0:4]), FadeIn(right_half[0:4]), run_time=1.0)
        self.add(particles)

        self.at("Keep the drain open")
        self.play(FadeIn(left_half[4:]), run_time=1.4)

        self.at("Slow the drain")
        self.play(FadeIn(right_half[4:]), run_time=1.6)

        self.at("The cell turns the pathway on")
        self.play(FadeIn(cap), run_time=1.2)
        self.finish()


class S12End(EndCard):
    LINE = "Wnt raises free β-catenin by slowing its constant destruction."
