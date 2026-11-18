"""The Mark and the Reader (turning-signals-off) — animation scenes.

COLOUR MAP (one colour per concept across the whole film):
  YELLOW : agonist (adrenaline) & active receptor
  GREEN  : G protein & ON signaling output
  GOLD   : phosphate marks (P) & predict question / emphasis
  RED    : arrestin (the reader / clamp) & blocked state
  BLUE   : second messenger / cyclic nucleotide pool
  TEAL   : GRK (the kinase writer) & downstream removal machinery
  GREY   : membrane, lipid vesicles, neutral controls, axes
  TEXT   : primary labels and headings

ONE CARRIED WORLD:
  A plasma membrane bilayer with a yellow receptor holding yellow adrenaline in its
  extracellular pocket, a green G-protein docking bay on its cytoplasmic core, and a
  cytoplasmic tail that receives gold phosphate marks (P) from teal GRK and is clamped
  over the docking bay by red arrestin.

WHAT CHANGES PER SPOKEN SCENE (and what computes it):
  s01_hook        : G proteins dock and depart carrying ON at a rate driven by a
                    monotonic phase integrator as response drops (1.0 -> 0.18, non-zero)
                    while the response meter drops and the yellow agonist stays locked.
  s03_active      : Zoomed cytoplasmic face; green G protein docks and leaves with ON;
                    teal GRK approaches along the same route and settles at the tail.
  s04_mark        : GRK stamps 4 gold P badges onto the tail while G proteins still dock;
                    the world transforms into a reconstitution tray with an active
                    G-protein activation meter.
  s04_rebuild     : Enlarged tray; vesicle + receptor, G protein, and GRK are added one
                    at a time; coupling and phosphate meters respond as distinct readouts.
  s05_purify      : TwoPanel comparison ('partly purified' vs 'highly purified'); both
                    phosphate meters rise identically (0 -> 0.90), while coupling drops
                    strongly on the left (1.0 -> 0.20) and slightly on the right (1.0 -> 0.88).
  s06_predict     : Trays merge to the purified marked receptor with active G-protein
                    cycling and high coupling; an empty red clamp outline ('missing part?')
                    and the predict question card appear.
  s08_reader      : Retinal arrestin enters from an eye icon, clamps the marked receptor
                    and drops coupling (0.88 -> 0.59), then fails to latch onto an
                    unmarked receptor where coupling stays high (0.98).
  s08_controls    : Three test lanes reset neutral then run sequentially: grey unrelated
                    protein bounces off, heat-damaged red block collapses, intact red
                    arrestin clamps the marked receptor and drops its coupling bar.
  s09_two_parts   : Full-frame receptor + 2-row Ledger (WRITER / READER); GRK writes P
                    marks, arrestin clamps the green docking bay, and approaching G
                    proteins physically deflect off the occupied core.
  s10_rule        : Balance bar tips toward removal as mark+reader shut off production;
                    departing green ON blocks dwindle according to pool_n (1.0 -> 0.15).
  s10_consequence : Agonist remains locked ('agonist still bound'); outside-signal meter
                    holds steady while arrestin clamps the bay and drives
                    G-protein activation sharply down (0.92 -> 0.16, not to zero).
  s11_handoff     : Pulled-back blocked receptor feeds a 3-layer downstream cascade while
                    a live Plot computes exponential persistence curves y_i(t)=exp(-k_i*t)
                    after coupling falls, until removal processes bring each layer down.
"""
from bp_parts import *


# ------------------------------------------------------------------ concept colours
AG_COL = YELLOW
GP_COL = GREEN
PHOS_COL = GOLD
ARR_COL = RED
CN_COL = BLUE
REM_COL = TEAL
MEM_COL = GREY


class FilmScene(SpokenScene):
    """SpokenScene without bp_style's decorative ambient motes; all motion comes from the subject."""

    def setup(self):
        NarratedScene.setup(self)


# ------------------------------------------------------------------ reusable world parts
def make_membrane(x0=-6.5, x1=6.5, y=1.35, thickness=0.38):
    """Horizontal lipid bilayer bar spanning the scene."""
    band = Rectangle(width=x1 - x0, height=thickness, stroke_width=0, fill_color=MEM_COL, fill_opacity=0.22).move_to([(x0 + x1) / 2, y, 0])
    top = Line([x0, y + thickness / 2, 0], [x1, y + thickness / 2, 0], color=MEM_COL, stroke_width=3)
    bot = Line([x0, y - thickness / 2, 0], [x1, y - thickness / 2, 0], color=MEM_COL, stroke_width=3)
    return VGroup(band, top, bot)


def make_p_badge(pos=ORIGIN, radius=0.26, with_letter=True):
    """Gold phosphate mark badge (P)."""
    c = Circle(radius=radius, stroke_color=TEXT, stroke_width=2, fill_color=PHOS_COL, fill_opacity=0.95).move_to(pos)
    if with_letter:
        p = T("P", size=24, color=BG, weight=BOLD).move_to(c)
        return VGroup(c, p)
    return VGroup(c)


def make_receptor(center=ORIGIN, scale=1.0, n_phosphates=0, show_agonist=True, show_dock=True, p_letters=True):
    """Active yellow receptor with top agonist pocket, bottom G-protein docking bay, and cytoplasmic tail.

    Geometry is built directly with `scale` so text sizes are controlled independently.
    """
    cx, cy = center[0], center[1]
    pts = [
        [-0.95, 1.15], [-0.42, 1.15], [-0.36, 0.55], [0.36, 0.55], [0.42, 1.15], [0.95, 1.15],
        [0.95, -0.75], [2.75, -0.75], [2.75, -1.08], [0.60, -1.08],
        [0.52, -1.25], [0.35, -1.25], [0.30, -0.72], [-0.55, -0.72], [-0.60, -1.25], [-0.95, -1.25],
    ]
    scaled_pts = [np.array([cx + x * scale, cy + y * scale, 0.0]) for x, y in pts]
    body = Polygon(*scaled_pts, stroke_color=AG_COL, stroke_width=3.5, fill_color=AG_COL, fill_opacity=0.18)

    g = VGroup(body)
    g.body = body
    g.rec_center = np.array([cx, cy, 0.0])
    g.rec_scale = scale
    g.pocket_center = np.array([cx, cy + 0.86 * scale, 0.0])
    g.dock_center = np.array([cx - 0.12 * scale, cy - 0.98 * scale, 0.0])
    p_rad = 0.26 if p_letters else 0.14
    y_drop = 0.34 if p_letters else 0.20 * scale
    g.tail_slots = [np.array([cx + (0.95 + 0.55 * i) * scale, cy - 1.08 * scale - y_drop, 0.0]) for i in range(4)]

    agonist = None
    if show_agonist:
        agonist = RoundedRectangle(corner_radius=0.16 * scale, width=0.58 * scale, height=0.44 * scale,
                                   stroke_color=TEXT, stroke_width=2.5, fill_color=AG_COL, fill_opacity=0.92)
        agonist.move_to(g.pocket_center)
        g.add(agonist)
    g.agonist = agonist

    dock = None
    if show_dock:
        dock_rect = RoundedRectangle(corner_radius=0.10 * scale, width=0.80 * scale, height=0.44 * scale,
                                     stroke_color=GP_COL, stroke_width=2.5, fill_color=GP_COL, fill_opacity=0.12)
        dock = DashedVMobject(dock_rect, num_dashes=14).move_to(g.dock_center)
        g.add(dock)
    g.dock = dock

    phosphates = VGroup()
    for i in range(min(n_phosphates, 4)):
        phosphates.add(make_p_badge(g.tail_slots[i], radius=p_rad, with_letter=p_letters))
    g.add(phosphates)
    g.phosphates = phosphates
    return g


def make_g_protein(pos=ORIGIN, on=False, label="G protein", scale=1.0):
    """Green G-protein block, optionally carrying a properly padded ON badge."""
    sz = max(24, int(round(28 * scale)))
    box = boxed_label(label, GP_COL, size=sz, pad=max(0.16, 0.18 * scale), fill_opacity=0.20)
    box.move_to(pos)
    if on:
        on_txt = T("ON", size=24, color=BG, weight=BOLD)
        on_bg = RoundedRectangle(corner_radius=0.10, width=on_txt.width + 0.34, height=on_txt.height + 0.24,
                                 stroke_color=TEXT, stroke_width=2, fill_color=GP_COL, fill_opacity=0.95)
        badge = VGroup(on_bg, on_txt.move_to(on_bg)).next_to(box, RIGHT, buff=0.12)
        out = VGroup(box, badge)
        out.box, out.badge = box, badge
        return out
    out = VGroup(box)
    out.box, out.badge = box, None
    return out


def set_gp_vis(gp, vis):
    """Show/hide a make_g_protein VGroup without altering its translucent box fill_opacity."""
    s = 1.0 if vis else 0.0
    gp.box.box.set_stroke(opacity=s).set_fill(opacity=0.20 * s)
    gp.box.label.set_opacity(s)
    if gp.badge is not None:
        gp.badge[0].set_stroke(opacity=s).set_fill(opacity=0.95 * s)
        gp.badge[1].set_opacity(s)
    return gp


def make_grk(pos=ORIGIN, label="GRK"):
    """Teal kinase block with a small catalytic tip."""
    card = boxed_label(label, REM_COL, size=28, pad=0.20, fill_opacity=0.20).move_to(pos)
    tip = Triangle(stroke_color=REM_COL, stroke_width=2.5, fill_color=REM_COL, fill_opacity=0.35).scale(0.16)
    tip.rotate(-PI / 2).next_to(card, LEFT, buff=-0.02)
    g = VGroup(tip, card)
    g.card, g.tip = card, tip
    return g


def make_arrestin_clamp(rec_center=ORIGIN, scale=1.0, label="arrestin", outline_only=False, faded=False, p_letters=True):
    """Red C-shaped reader clamp built around a receptor's coordinates so it covers the G-protein bay
    and cradles the tail without overlapping the yellow receptor body or any P badge."""
    cx, cy = rec_center[0], rec_center[1]
    s = scale
    # Top of main clamp body clears the bottom of the P badges cleanly
    p_bottom_rel = -1.08 * s - (0.68 if p_letters else 0.40 * s)
    y_top = p_bottom_rel - 0.12
    body_h = max(0.56, 0.62 * s)
    y_bot = y_top - body_h
    y_mid = (y_top + y_bot) / 2.0

    # Left plug sits strictly inside the G-protein recess [-0.55s, +0.30s], y <= -0.72s
    lx0, lx1 = -0.46 * s, 0.22 * s
    plug_top = -0.82 * s

    # Ensure body is wide enough for the label
    lbl = None
    lbl_w = 0.0
    if label:
        sz = max(24, int(round(26 * s)))
        lbl = T(label, size=sz, color=ARR_COL).set_opacity(0.55 if faded else 1.0)
        lbl_w = lbl.width

    rx_outer = max(3.18 * s, -0.75 * s + lbl_w + 0.85)
    rx_inner = rx_outer - 0.28 * s
    hook_top = -1.16 * s

    pts = [
        [-0.75 * s, y_top],
        [lx0, y_top],
        [lx0, plug_top],
        [lx1, plug_top],
        [lx1, y_top],
        [rx_inner, y_top],
        [rx_inner, hook_top],
        [rx_outer, hook_top],
        [rx_outer, y_bot],
        [-0.75 * s, y_bot],
    ]
    spts = [np.array([cx + x, cy + y, 0.0]) for x, y in pts]
    op = 0.0 if outline_only else (0.10 if faded else 0.24)
    st_op = 0.55 if faded else 1.0
    shape = Polygon(*spts, stroke_color=ARR_COL, stroke_width=3.5, stroke_opacity=st_op,
                    fill_color=ARR_COL, fill_opacity=op)
    if outline_only:
        shape = DashedVMobject(shape, num_dashes=32)
    g = VGroup(shape)
    g.shape = shape
    if lbl is not None:
        lbl.move_to([cx + (-0.75 * s + rx_inner) / 2.0, cy + y_mid, 0.0])
        g.add(lbl)
    g.label = lbl
    return g


def make_meter(title, tracker, center, width=0.68, height=2.5, color=GP_COL, low_lbl="low", high_lbl="high",
               title_size=26, lbl_size=24):
    """Qualitative vertical meter bar driven by a ValueTracker (0..1), no invented numbers."""
    cx, cy = center[0], center[1]
    track = RoundedRectangle(corner_radius=0.10, width=width, height=height, stroke_color=MEM_COL,
                             stroke_width=2.5, fill_color=BG, fill_opacity=0.85).move_to(center)
    pad = 0.05
    max_h = height - 2 * pad
    inner_w = width - 2 * pad

    def mk_bar():
        v = float(np.clip(tracker.get_value(), 0.02, 1.0))
        bh = max(0.08, v * max_h)
        r = RoundedRectangle(corner_radius=0.06, width=inner_w, height=bh, stroke_width=0,
                             fill_color=color, fill_opacity=0.88)
        r.move_to([cx, cy - max_h / 2 + bh / 2, 0.0])
        return r

    bar = always_redraw(mk_bar)
    ttl = T(title, size=title_size, color=color, line_spacing=0.85).next_to(track, UP, buff=0.18)
    hi = T(high_lbl, size=lbl_size, color=TEXT).next_to(track, RIGHT, buff=0.16).align_to(track, UP)
    lo = T(low_lbl, size=lbl_size, color=TEXT).next_to(track, RIGHT, buff=0.16).align_to(track, DOWN)
    g = VGroup(track, bar, ttl, hi, lo)
    g.track, g.bar, g.ttl = track, bar, ttl
    return g


def make_eye_icon(center=ORIGIN, scale=0.8):
    """Simple geometric eye schematic (arcs + iris + label) for the retina clue."""
    cx, cy = center[0], center[1]
    top = ArcBetweenPoints([cx - 0.8 * scale, cy, 0], [cx + 0.8 * scale, cy, 0], angle=-1.2,
                           color=TEXT, stroke_width=3)
    bot = ArcBetweenPoints([cx - 0.8 * scale, cy, 0], [cx + 0.8 * scale, cy, 0], angle=1.2,
                           color=TEXT, stroke_width=3)
    iris = Circle(radius=0.25 * scale, stroke_color=CN_COL, stroke_width=3, fill_color=CN_COL, fill_opacity=0.30).move_to(center)
    pupil = Dot(center, radius=0.09 * scale, color=TEXT)
    lbl = T("retina", size=26, color=TEXT).next_to(bot, DOWN, buff=0.18)
    return VGroup(top, bot, iris, pupil, lbl)


# ------------------------------------------------------------------ shared s06/s07 world
def world_predict():
    """Shared picture for end of s06_predict and all of s07_pause."""
    mem = make_membrane(x0=-6.4, x1=0.6, y=1.35)
    rec = make_receptor(center=[-3.2, 1.0, 0], scale=1.0, n_phosphates=4, show_agonist=True, show_dock=True, p_letters=True)
    ag_lbl = T("agonist", size=26, color=AG_COL).next_to(rec.agonist, UP, buff=0.38)
    p_lbl = T("phosphate marks", size=26, color=PHOS_COL).move_to([-0.65, 2.28, 0])
    grk = make_grk(pos=[-5.2, -0.35, 0], label="GRK")
    gap_box = make_arrestin_clamp(rec_center=rec.rec_center, scale=1.0, label="missing part?", outline_only=True, p_letters=True)

    p_val = ValueTracker(0.90)
    c_val = ValueTracker(0.88)
    m_phos = make_meter("phosphate", p_val, center=[2.7, 0.65, 0], height=2.1, color=PHOS_COL)
    m_coup = make_meter("coupling", c_val, center=[4.9, 0.65, 0], height=2.1, color=GP_COL)

    tag = scope_tag("schematic")
    return VGroup(mem, rec, ag_lbl, p_lbl, grk, gap_box, m_phos, m_coup, tag)


# ================================================================== SCENES
class S01Hook(FilmScene):
    """Hook: adrenaline stays locked, G-protein departures slow down sharply (not to zero), '?' grows."""

    def construct(self):
        mem = make_membrane(x0=-6.6, x1=6.6, y=1.45)
        rec = make_receptor(center=[-1.3, 1.10, 0], scale=1.15, n_phosphates=0, show_agonist=True, show_dock=True)
        ag_lbl = T("adrenaline", size=28, color=AG_COL).next_to(rec.agonist, UP, buff=0.38)
        rec_lbl = T("receptor", size=28, color=AG_COL).next_to(rec.body, LEFT, buff=0.30).shift(DOWN * 0.25)

        resp_t = ValueTracker(1.0)
        resp_meter = make_meter("cell response", resp_t, center=[-5.1, -1.0, 0], height=2.2, color=GP_COL)

        # Monotonic phase integrator driven by response rate; pre-built off/on mobjects avoid VGroup.become() font scaling
        phase_tr = ValueTracker(0.0)
        phase_tr.add_updater(lambda m, dt: m.increment_value((0.36 + 0.95 * resp_t.get_value()) * dt))
        dock_pt = rec.dock_center + DOWN * 0.72
        gp_off = make_g_protein(pos=dock_pt, on=False, label="G protein", scale=0.92)
        gp_on = set_gp_vis(make_g_protein(pos=dock_pt, on=True, label="G protein", scale=0.92), False)

        def upd_off(m):
            phase = phase_tr.get_value() % 1.0
            if phase < 0.44:
                u = phase / 0.44
                set_gp_vis(m.move_to(dock_pt + DOWN * (1.45 * (1.0 - u))), True)
            else:
                set_gp_vis(m, False)

        def upd_on(m):
            phase = phase_tr.get_value() % 1.0
            if phase >= 0.44:
                u = (phase - 0.44) / 0.56
                set_gp_vis(m.move_to(dock_pt + DOWN * (0.45 * min(1.0, u * 2.0)) + RIGHT * (2.9 * u) + DOWN * (0.55 * u)), True)
            else:
                set_gp_vis(m, False)

        gp_off.add_updater(upd_off)
        gp_on.add_updater(upd_on)
        qmark = T("?", size=120, color=PHOS_COL, weight=BOLD).move_to([3.9, 0.35, 0])
        q_sub = T("still occupied", size=28, color=AG_COL).next_to(qmark, DOWN, buff=0.25)
        tag = scope_tag("schematic")

        self.add(mem, rec, ag_lbl, rec_lbl, resp_meter, phase_tr, gp_off, gp_on, tag)
        self.wait(3.0)

        self.at("cell's response")
        self.play(resp_t.animate(run_time=2.5, rate_func=smooth).set_value(0.18))

        self.at("How can")
        self.play(FadeIn(qmark, scale=0.6, run_time=0.6), FadeIn(q_sub, run_time=0.6))
        rem = max(0.5, self.narration_s + 0.3 - self.elapsed())
        self.wait(rem)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Turning the Signal Off: Arrestins, RGS Proteins and Phosphodiesterases"
    TITLE = "The Mark and the Reader"


class S03Active(FilmScene):
    """Zoomed cytoplasmic face: green G protein docks & leaves ON; teal GRK approaches & settles."""

    def construct(self):
        mem = make_membrane(x0=-6.6, x1=6.6, y=1.85)
        rec = make_receptor(center=[-1.5, 1.35, 0], scale=1.30, n_phosphates=0, show_agonist=True, show_dock=True)
        rec_lbl = T("active receptor", size=30, color=AG_COL).next_to(rec.body, LEFT, buff=0.35).shift(DOWN * 0.25)
        ag_lbl = T("agonist", size=28, color=AG_COL).next_to(rec.agonist, UP, buff=0.36)
        bay_lbl = T("G-protein site", size=26, color=GP_COL).move_to([-4.5, -0.35, 0])
        bay_ptr = Arrow(bay_lbl.get_right() + RIGHT * 0.08, rec.dock_center + LEFT * 0.60,
                        color=GP_COL, stroke_width=2.5, buff=0.04, max_tip_length_to_length_ratio=0.18)
        tag = scope_tag("schematic")

        self.play(FadeIn(mem, rec, rec_lbl, ag_lbl, bay_lbl, bay_ptr, tag), run_time=0.7)

        # Receptor is visibly active: first G-protein round runs while active receptor is introduced
        dock_pt = rec.dock_center + DOWN * 0.72
        gp0 = make_g_protein(pos=dock_pt + DOWN * 1.5, on=False, label="G protein")
        self.play(FadeIn(gp0, shift=UP * 0.2), run_time=0.35)
        self.play(gp0.animate.move_to(dock_pt), run_time=0.8)
        gp0_on = make_g_protein(pos=dock_pt, on=True, label="G protein")
        self.play(FadeOut(gp0, run_time=0.15), FadeIn(gp0_on, run_time=0.2))
        self.play(gp0_on.animate.move_to([3.5, -2.15, 0]), run_time=1.3)
        self.play(FadeOut(gp0_on), run_time=0.25)

        # Second round of signaling on "Its interface..."
        self.at("Its interface")
        gp = make_g_protein(pos=dock_pt + DOWN * 1.5, on=False, label="G protein")
        self.play(FadeIn(gp, shift=UP * 0.2), run_time=0.4)
        self.play(gp.animate.move_to(dock_pt), run_time=1.2)
        gp_on = make_g_protein(pos=dock_pt, on=True, label="G protein")
        self.play(FadeOut(gp, run_time=0.15), FadeIn(gp_on, run_time=0.2))
        self.play(gp_on.animate.move_to([3.5, -2.15, 0]), run_time=2.3)
        self.play(FadeOut(gp_on), run_time=0.3)

        # Dedicated receptor kinase approaches that active shape
        self.at("dedicated receptor kinase")
        grk_start = [4.2, -2.15, 0]
        grk_dock = [rec.tail_slots[2][0] + 0.65, rec.tail_slots[2][1] - 0.72, 0]
        grk = make_grk(pos=grk_start, label="receptor kinase")
        self.play(FadeIn(grk, shift=LEFT * 0.3), run_time=0.5)
        gpx_on = make_g_protein(pos=dock_pt + DOWN * 1.5, on=True, label="G protein")
        gp_cycle = Succession(
            FadeIn(gpx_on, shift=UP * 0.2, run_time=0.4),
            gpx_on.animate(run_time=1.0).move_to(dock_pt),
            gpx_on.animate(run_time=1.9).move_to([-3.0, -2.2, 0]),
            FadeOut(gpx_on, run_time=0.3),
        )
        self.play(grk.animate.move_to(grk_dock), gp_cycle, run_time=4.6)

        self.at("The kinase is called")
        grk_short = make_grk(pos=grk_dock, label="GRK")
        gp2 = make_g_protein(pos=dock_pt + DOWN * 1.5, on=False, label="G protein")
        self.play(swap(grk, grk_short, run_time=0.7), FadeIn(gp2, run_time=0.4))
        self.play(gp2.animate.move_to(dock_pt), run_time=1.4)
        gp2_on = make_g_protein(pos=dock_pt, on=True, label="G protein")
        self.play(FadeOut(gp2, run_time=0.15), FadeIn(gp2_on, run_time=0.2))
        self.at("or GRK")
        self.play(gp2_on.animate.move_to([1.2, -2.25, 0]), run_time=1.2)
        self.finish()


class S04Mark(FilmScene):
    """GRK adds gold P marks on tail; G protein still docks; transforms into reconstitution tray."""

    def construct(self):
        mem = make_membrane(x0=-6.6, x1=6.6, y=1.85)
        rec = make_receptor(center=[-1.5, 1.35, 0], scale=1.30, n_phosphates=0, show_agonist=True, show_dock=True)
        rec_lbl = T("active receptor", size=30, color=AG_COL).next_to(rec.body, LEFT, buff=0.35).shift(DOWN * 0.25)
        ag_lbl = T("agonist", size=28, color=AG_COL).next_to(rec.agonist, UP, buff=0.36)
        grk_pos = [rec.tail_slots[2][0] + 0.65, rec.tail_slots[2][1] - 0.72, 0]
        grk = make_grk(pos=grk_pos, label="GRK")
        tag = scope_tag("schematic")
        self.add(mem, rec, rec_lbl, ag_lbl, grk, tag)

        # Gold phosphate badges appear one at a time along the cytoplasmic tail
        self.at("adds phosphate marks")
        p_badges = VGroup()
        for slot in rec.tail_slots:
            badge = make_p_badge(slot, radius=0.26, with_letter=True)
            p_badges.add(badge)
            self.play(
                grk.animate.move_to([slot[0] + 0.55, slot[1] - 0.72, 0]),
                FadeIn(badge, scale=0.5),
                run_time=0.65,
            )
        p_lbl = T("phosphate marks", size=28, color=PHOS_COL).move_to([2.05, 0.95, 0])
        self.play(FadeIn(p_lbl), run_time=0.4)

        # But a mark is not an off switch: G protein still docks and leaves ON
        self.at("But a mark")
        dock_pt = rec.dock_center + DOWN * 0.85
        gp = make_g_protein(pos=dock_pt + DOWN * 1.4, on=False, label="G protein")
        self.play(FadeIn(gp), run_time=0.3)
        self.play(gp.animate.move_to(dock_pt), run_time=0.8)
        gp_on = make_g_protein(pos=dock_pt + DOWN * 0.45, on=True, label="G protein")
        self.play(FadeOut(gp, run_time=0.15), FadeIn(gp_on, run_time=0.2))
        self.play(gp_on.animate.move_to([-1.2, -2.35, 0]), run_time=0.7)
        self.play(gp_on.animate.move_to([3.5, -2.35, 0]), run_time=0.9)

        # Transform membrane scene into reconstitution tray + G-protein activation gauge
        self.at("purified the kinase")
        tray = RoundedRectangle(corner_radius=0.22, width=7.6, height=5.0, stroke_color=MEM_COL, stroke_width=3,
                                fill_color=MEM_COL, fill_opacity=0.08).move_to([-2.0, 0.1, 0])
        tray_ttl = T("reconstitution tray", size=28, color=TEXT).next_to(tray, UP, buff=0.18)

        b_rec = boxed_label("receptor", AG_COL, size=28, pad=0.22).move_to([-4.2, 1.3, 0])
        b_gp = boxed_label("G protein", GP_COL, size=28, pad=0.22).move_to([-0.3, 1.3, 0])
        b_grk = boxed_label("kinase (GRK)", REM_COL, size=28, pad=0.22).move_to([-4.2, -0.7, 0])
        b_atp = boxed_label("ATP", PHOS_COL, size=28, pad=0.22).move_to([-0.3, -0.7, 0])
        blocks = VGroup(b_rec, b_gp, b_grk, b_atp)

        act_t = ValueTracker(0.15)
        act_meter = make_meter("G-protein\nactivation", act_t, center=[3.9, 0.1, 0], height=3.0, color=GP_COL)

        old_world = VGroup(mem, rec, rec_lbl, ag_lbl, grk, p_badges, p_lbl, gp_on)
        self.play(
            FadeOut(old_world, run_time=0.5),
            FadeIn(tray, tray_ttl, blocks, act_meter, run_time=0.7),
        )
        self.at("rebuilt signaling")
        self.play(act_t.animate(run_time=1.8).set_value(0.90))
        self.finish()


class S04Rebuild(FilmScene):
    """Enlarged tray: receptor in lipid vesicle, add G protein & kinase separately; two distinct gauges."""

    def construct(self):
        tray = RoundedRectangle(corner_radius=0.22, width=7.6, height=5.3, stroke_color=MEM_COL, stroke_width=3,
                                fill_color=MEM_COL, fill_opacity=0.08).move_to([-2.3, 0.0, 0])
        tray_ttl = T("reconstitution tray", size=28, color=TEXT).next_to(tray, UP, buff=0.18)

        coup_t = ValueTracker(0.05)
        phos_t = ValueTracker(0.05)
        m_coup = make_meter("coupling", coup_t, center=[2.7, 0.0, 0], height=2.9, color=GP_COL)
        m_phos = make_meter("phosphate", phos_t, center=[4.9, 0.0, 0], height=2.9, color=PHOS_COL)
        tag = scope_tag("schematic")

        self.play(Create(tray), FadeIn(tray_ttl, m_coup, m_phos, tag), run_time=1.4)

        # Vesicle enters smoothly as pathway reconstruction is introduced, then receptor sits inside
        vesicle = Circle(radius=1.85, stroke_color=MEM_COL, stroke_width=3.5, fill_color=MEM_COL, fill_opacity=0.10).move_to([-3.7, 0.1, 0])
        ves_lbl = T("lipid vesicle", size=26, color=TEXT).next_to(vesicle, DOWN, buff=0.18)
        self.play(Create(vesicle), FadeIn(ves_lbl), run_time=1.8)

        self.at("The receptor sat")
        rec = make_receptor(center=[-4.0, 0.15, 0], scale=0.68, n_phosphates=0, show_agonist=True, show_dock=True, p_letters=False)
        rec_lbl = T("receptor", size=26, color=AG_COL).next_to(rec.body, UP, buff=0.18)
        self.play(FadeIn(rec, rec_lbl), run_time=1.1)

        # Purified G protein added beside it -> coupling readout rises
        self.at("beside purified")
        gp = make_g_protein(pos=[-0.4, 2.0, 0], on=False, label="G protein", scale=0.95)
        self.play(FadeIn(gp), run_time=0.4)
        self.play(gp.animate.move_to([-0.5, 0.85, 0]), coup_t.animate.set_value(0.95), run_time=1.4)

        # Candidate proteins added one at a time -> kinase adds phosphate
        self.at("added candidate proteins")
        grk = make_grk(pos=[-0.4, -2.0, 0], label="kinase")
        self.play(FadeIn(grk), run_time=0.4)
        self.play(grk.animate.move_to([-0.6, -1.05, 0]), run_time=1.2)
        p_marks = VGroup(*[make_p_badge(s, radius=0.14, with_letter=False) for s in rec.tail_slots])
        self.play(FadeIn(p_marks), phos_t.animate.set_value(0.90), run_time=1.2)

        # Receptor coupling became the readout, not phosphate alone
        self.at("Receptor coupling became")
        hl_box = SurroundingRectangle(m_coup, color=GP_COL, buff=0.14, stroke_width=3, corner_radius=0.12)
        self.play(Create(hl_box), coup_t.animate.set_value(0.88), run_time=1.2)
        self.finish()


class S05Purify(FilmScene):
    """TwoPanel: partly purified (phosphate high, coupling drops strongly) vs highly purified (phosphate high, coupling falls slightly)."""

    def construct(self):
        tp = TwoPanel("partly purified", "highly purified", colors=(PHOS_COL, REM_COL), top=3.15, bottom=-2.55)
        tag = scope_tag("schematic")

        def panel_contents(cx, p_init=0.05, c_init=0.95):
            ves = Circle(radius=1.08, stroke_color=MEM_COL, stroke_width=3, fill_color=MEM_COL, fill_opacity=0.10).move_to([cx - 1.78, 0.35, 0])
            rec = make_receptor(center=[cx - 2.16, 0.45, 0], scale=0.40, n_phosphates=0, show_agonist=True, show_dock=False, p_letters=False)
            p_tr = ValueTracker(p_init)
            c_tr = ValueTracker(c_init)
            mp = make_meter("phosphate", p_tr, center=[cx + 0.12, 0.20, 0], width=0.48, height=1.90, color=PHOS_COL,
                            title_size=24, lbl_size=24)
            mc = make_meter("coupling", c_tr, center=[cx + 1.82, 0.20, 0], width=0.48, height=1.90, color=GP_COL,
                            title_size=24, lbl_size=24)
            # Live G-protein coupling stream below the vesicle driven directly by c_tr
            ph = ValueTracker(0.0)
            ph.add_updater(lambda m, dt, ct=c_tr: m.increment_value((0.12 + 0.68 * ct.get_value()) * dt))
            gp = make_g_protein(pos=[cx - 2.1, -1.65, 0], on=True, label="G", scale=0.72)
            gp.add_updater(lambda m, p=ph, c=cx: m.move_to([c - 2.1 + 3.2 * (p.get_value() % 1.0), -1.65, 0]))
            return ves, rec, p_tr, c_tr, mp, mc, ph, gp

        l_ves, l_rec, lp_tr, lc_tr, l_mp, l_mc, l_ph, l_gp = panel_contents(-3.3)
        r_ves, r_rec, rp_tr, rc_tr, r_mp, r_mc, r_ph, r_gp = panel_contents(3.3)
        self.add(tp, tag, l_ves, l_rec, l_mp, l_mc, l_ph, l_gp, r_ves, r_rec, r_mp, r_mc, r_ph, r_gp)

        # Left: partly purified adds phosphate & strongly reduces coupling
        self.at("added phosphate")
        l_p = VGroup(*[make_p_badge(s, radius=0.12, with_letter=False) for s in l_rec.tail_slots])
        self.play(FadeIn(l_p), lp_tr.animate.set_value(0.90), run_time=1.3)

        self.at("strongly reduced")
        self.play(lc_tr.animate.set_value(0.20), run_time=1.4)

        # Right: highly purified kinase adds phosphate too, yet coupling falls only a little
        self.at("highly purified")
        r_p = VGroup(*[make_p_badge(s, radius=0.12, with_letter=False) for s in r_rec.tail_slots])
        self.play(FadeIn(r_p), rp_tr.animate.set_value(0.90), run_time=1.4)

        self.at("yet coupling fell")
        self.play(rc_tr.animate.set_value(0.88), run_time=1.2)

        # Highlight equal phosphate signals
        self.at("phosphate signal remained")
        hl_p = VGroup(
            SurroundingRectangle(l_mp.track, color=PHOS_COL, buff=0.08, stroke_width=3),
            SurroundingRectangle(r_mp.track, color=PHOS_COL, buff=0.08, stroke_width=3),
        )
        self.play(Create(hl_p), run_time=0.8)

        # Highlight unequal functional effect
        self.at("functional effect vanished")
        hl_c = VGroup(
            SurroundingRectangle(l_mc.track, color=GP_COL, buff=0.08, stroke_width=3),
            SurroundingRectangle(r_mc.track, color=GP_COL, buff=0.08, stroke_width=3),
        )
        self.play(FadeOut(hl_p, run_time=0.25), Create(hl_c, run_time=0.8))
        self.finish()


class S06Predict(FilmScene):
    """Merge to purified marked receptor; active G-protein cycling continues; empty red outline + question card."""

    def construct(self):
        p_left = ValueTracker(0.90)
        c_left = ValueTracker(0.20)
        p_right = ValueTracker(0.90)
        c_right = ValueTracker(0.88)

        g_left = VGroup(
            T("partly purified", size=28, color=PHOS_COL).move_to([-3.3, 2.5, 0]),
            make_meter("phosphate", p_left, center=[-4.3, 0.2, 0], height=2.2, color=PHOS_COL),
            make_meter("coupling", c_left, center=[-2.2, 0.2, 0], height=2.2, color=GP_COL),
        )
        g_right = VGroup(
            T("highly purified", size=28, color=REM_COL).move_to([3.3, 2.5, 0]),
            make_meter("phosphate", p_right, center=[2.3, 0.2, 0], height=2.2, color=PHOS_COL),
            make_meter("coupling", c_right, center=[4.4, 0.2, 0], height=2.2, color=GP_COL),
        )
        self.add(g_left, g_right, scope_tag("schematic"))
        self.wait(0.8)

        self.at("switching off")
        wp = world_predict()
        mem, rec, ag_lbl, p_lbl, grk, gap_box, m_phos, m_coup, tag = wp
        self.play(
            FadeOut(g_left, run_time=0.45),
            FadeOut(g_right, run_time=0.45),
            FadeIn(mem, rec, ag_lbl, p_lbl, grk, m_phos, m_coup, run_time=0.8),
        )

        # Animate a G protein still docking below the bay while the missing part is asked
        dock_pt = rec.dock_center + DOWN * 0.96
        gp = make_g_protein(pos=dock_pt + DOWN * 1.0, on=False, label="G protein", scale=0.88)
        self.play(FadeIn(gp), run_time=0.3)
        self.play(gp.animate.move_to(dock_pt), run_time=0.8)

        self.at("What missing part")
        q = question_card("What missing part would make the phosphate mark matter?")
        self.play(FadeOut(gp, run_time=0.25), FadeIn(gap_box, run_time=0.5), FadeIn(q.question, run_time=0.6))
        self.finish()


class S07Pause(PredictPause):
    QUESTION = "What missing part would make the phosphate mark matter?"
    RING_AT = (5.9, -2.05, 0)
    SECONDS = 4.5

    def backdrop(self):
        wp = world_predict()
        gap_box = wp[5]
        pulse(gap_box.shape, base=3.5, amp=1.5, speed=3.5)
        return wp


class S08Reader(FilmScene):
    """Retinal arrestin enters from eye icon, clamps marked receptor & drops coupling; fails on unmarked receptor."""

    def construct(self):
        wp = world_predict()
        mem, rec, ag_lbl, p_lbl, grk, gap_box, m_phos_init, m_coup_init, tag = wp
        q = question_card("What missing part would make the phosphate mark matter?")
        self.add(mem, rec, ag_lbl, p_lbl, grk, gap_box, m_phos_init, m_coup_init, tag, q.question)

        # Clue from the retina
        self.at("from the retina")
        eye = make_eye_icon(center=[5.0, 2.45, 0], scale=0.78)
        self.play(
            FadeOut(q.question, m_phos_init, m_coup_init, run_time=0.4),
            FadeIn(eye, run_time=0.6),
        )

        # Live coupling meter for the marked receptor
        c_val = ValueTracker(0.88)
        m_coup = make_meter("coupling", c_val, center=[4.6, -1.05, 0], height=1.85, color=GP_COL)
        self.play(FadeIn(m_coup), run_time=0.5)

        self.at("second protein")
        arr = make_arrestin_clamp(rec_center=[1.35, 2.55, 0], scale=0.70, label="second protein", p_letters=True)
        self.play(FadeIn(arr, shift=LEFT * 0.3), run_time=0.6)

        self.at("called arrestin")
        arr_named = make_arrestin_clamp(rec_center=[1.35, 2.55, 0], scale=0.70, label="arrestin", p_letters=True)
        self.play(swap(arr.label, arr_named.label, run_time=0.6))
        arr = VGroup(arr.shape, arr_named.label)

        # Adding retinal arrestin fills the empty outline, clamps the core, and drops coupling
        self.at("Adding retinal arrestin")
        target_arr = make_arrestin_clamp(rec_center=rec.rec_center, scale=1.0, label="arrestin", p_letters=True)
        self.play(
            FadeOut(gap_box, run_time=0.3),
            Transform(arr, target_arr),
            run_time=1.6,
        )
        self.at("brought back part")
        self.play(c_val.animate.set_value(0.59), run_time=1.4)

        # Arrestin alone could not act on an unmarked receptor
        self.at("Arrestin alone")
        l_rec = make_receptor(center=[-4.65, 1.05, 0], scale=0.72, n_phosphates=4, show_agonist=True, show_dock=True, p_letters=False)
        l_arr = make_arrestin_clamp(rec_center=l_rec.rec_center, scale=0.72, label="arrestin", p_letters=False)
        left_sys = VGroup(
            T("marked receptor", size=28, color=PHOS_COL).move_to([-3.3, 2.85, 0]),
            make_membrane(x0=-6.2, x1=-0.4, y=1.35),
            l_rec,
            l_arr,
            make_meter("coupling", ValueTracker(0.59), center=[-1.25, -0.55, 0], width=0.48, height=1.85, color=GP_COL),
        )
        r_c = ValueTracker(0.98)
        r_rec = make_receptor(center=[1.55, 1.05, 0], scale=0.72, n_phosphates=0, show_agonist=True, show_dock=True, p_letters=False)
        r_arr_dock = make_arrestin_clamp(rec_center=r_rec.rec_center, scale=0.72, label="arrestin", p_letters=False)
        r_arr = r_arr_dock.copy().shift(DOWN * 1.4)
        right_sys = VGroup(
            T("unmarked receptor", size=28, color=TEXT).move_to([3.3, 2.85, 0]),
            make_membrane(x0=0.4, x1=6.2, y=1.35),
            r_rec,
            make_meter("coupling", r_c, center=[4.95, -0.55, 0], width=0.48, height=1.85, color=GP_COL),
        )
        self.play(
            FadeOut(mem, rec, ag_lbl, p_lbl, grk, arr, eye, m_coup, run_time=0.45),
            FadeIn(left_sys, right_sys, r_arr, run_time=0.65),
        )
        # Arrestin approaches unmarked receptor, fails to latch, and drifts away
        self.play(r_arr.animate.shift(UP * 0.9), run_time=0.8)
        self.play(r_arr.animate.shift(DOWN * 1.1), run_time=1.2)
        self.finish()


class S08Controls(FilmScene):
    """Three carried test lanes: unrelated grey bounces, heat-damaged collapses, intact arrestin clamps."""

    def construct(self):
        lane_x = [-4.2, 0.0, 4.2]
        titles = ["unrelated protein", "heat-damaged", "intact arrestin"]
        tcols = [MEM_COL, ARR_COL, ARR_COL]

        lanes, c_trackers, recs = [], [], []
        for x, ttl, col in zip(lane_x, titles, tcols):
            hd = T(ttl, size=26, color=col).move_to([x, 3.0, 0])
            mem = make_membrane(x0=x - 1.75, x1=x + 1.75, y=1.80)
            rec = make_receptor(center=[x - 0.75, 1.65, 0], scale=0.55, n_phosphates=4, show_agonist=True, show_dock=True, p_letters=False)
            ct = ValueTracker(0.95)
            cm = make_meter("coupling", ct, center=[x + 1.00, -1.95, 0], width=0.44, height=1.15, color=GP_COL,
                            title_size=24, lbl_size=24)
            lanes.append(VGroup(hd, mem, rec, cm))
            c_trackers.append(ct)
            recs.append(rec)

        tag = scope_tag("schematic")
        self.play(FadeIn(*lanes, tag), run_time=0.8)

        # Show active G-protein turnover across the 3 starting lanes before testing candidate proteins
        gp_init = VGroup(*[make_g_protein(pos=[lx - 0.75, -0.45, 0], on=True, label="G", scale=0.72) for lx in lane_x])
        self.play(FadeIn(gp_init), run_time=0.3)
        self.play(gp_init.animate.shift(UP * 0.85), run_time=0.9)
        self.play(gp_init.animate.shift(DOWN * 0.85), run_time=0.7)
        self.play(FadeOut(gp_init), run_time=0.25)

        # Lane 1: unrelated grey block approaches below receptor and bounces away
        self.at("unrelated protein")
        grey_blk = boxed_label("control", MEM_COL, size=24, pad=0.16).move_to([lane_x[0] - 0.75, -0.55, 0])
        self.play(FadeIn(grey_blk), run_time=0.35)
        self.play(grey_blk.animate.move_to([lane_x[0] - 0.75, 0.35, 0]), run_time=0.9)
        self.play(grey_blk.animate.move_to([lane_x[0] - 0.75, -0.80, 0]), run_time=1.0)
        # G-protein turnover carries on in every lane while the narrator finishes the claim
        gp_a = VGroup(*[make_g_protein(pos=[lx + 0.55, -0.45, 0], on=True, label="G", scale=0.72) for lx in lane_x])
        self.play(FadeIn(gp_a), run_time=0.2)
        self.play(gp_a.animate.shift(UP * 0.85), run_time=0.8)
        self.play(gp_a.animate.shift(DOWN * 0.85), run_time=0.7)
        self.play(FadeOut(gp_a), run_time=0.2)

        # Lane 2: heat-damaged arrestin collapses (shape flattens while label drops cleanly below it)
        self.at("Heat")
        bad_dock = make_arrestin_clamp(rec_center=recs[1].rec_center, scale=0.55, label="damaged", faded=True, p_letters=False)
        bad_arr = bad_dock.copy().shift(DOWN * 0.60)
        self.play(FadeIn(bad_arr), run_time=0.35)
        self.play(bad_arr.animate.shift(UP * 0.35), run_time=0.8)
        self.play(
            bad_arr.shape.animate.stretch(0.35, 1, about_edge=UP).set_opacity(0.35),
            bad_arr.label.animate.shift(DOWN * 0.45).set_opacity(0.65),
            run_time=1.0,
        )
        gp_b = VGroup(*[make_g_protein(pos=[lx + 0.55, -0.45, 0], on=True, label="G", scale=0.72) for lx in (lane_x[0], lane_x[2])])
        self.play(FadeIn(gp_b), run_time=0.2)
        self.play(gp_b.animate.shift(UP * 0.85), run_time=0.8)
        self.play(gp_b.animate.shift(DOWN * 0.85), run_time=0.7)
        self.play(FadeOut(gp_b), run_time=0.2)

        # Lane 3: intact red arrestin clamps marked receptor and drops coupling cleanly before "intact reader"
        self.at("The effect required")
        good_dock = make_arrestin_clamp(rec_center=recs[2].rec_center, scale=0.55, label="arrestin", p_letters=False)
        good_arr = good_dock.copy().shift(DOWN * 0.60)
        self.play(FadeIn(good_arr), run_time=0.25)
        self.play(good_arr.animate.move_to(good_dock), run_time=0.55)
        self.play(c_trackers[2].animate.set_value(0.50), run_time=0.45)

        # Two highlighted requirements at the bottom
        self.at("intact reader")
        req1 = boxed_label("intact reader", ARR_COL, size=26, pad=0.18).move_to([-2.7, -3.05, 0])
        self.play(FadeIn(req1), run_time=0.5)
        self.at("carrying the kinase's mark")
        req2 = boxed_label("marked receptor", PHOS_COL, size=26, pad=0.18).move_to([1.8, -3.05, 0])
        self.play(FadeIn(req2), run_time=0.5)
        self.finish()


class S09TwoParts(FilmScene):
    """Full-frame receptor + 2-step Ledger (WRITER / READER); G protein approaches and deflects off occupied core."""

    def construct(self):
        mem = make_membrane(x0=-6.4, x1=0.2, y=1.35)
        rec = make_receptor(center=[-3.5, 1.0, 0], scale=1.0, n_phosphates=0, show_agonist=True, show_dock=True, p_letters=True)
        ag_lbl = T("active receptor", size=28, color=AG_COL).next_to(rec.body, UP, buff=0.22)
        tag = scope_tag("schematic")

        L = Ledger(
            [
                ("WRITER", "GRK adds P mark", REM_COL),
                ("READER", "arrestin blocks G site", ARR_COL),
            ],
            top_left=(0.7, 2.0),
            title="two jobs",
            row_h=0.95,
            key_w=1.55,
            width=5.6,
            size=26,
        )
        self.play(FadeIn(mem, rec, ag_lbl, L, tag), run_time=0.8)

        # Step 1: GRK writes the mark on the active receptor
        self.at("GRK writes")
        grk = make_grk(pos=[-0.3, -1.9, 0], label="GRK")
        self.play(L.reveal(0), FadeIn(grk), run_time=0.6)
        p_marks = VGroup(*[make_p_badge(s, radius=0.26, with_letter=True) for s in rec.tail_slots])
        self.play(grk.animate.move_to([-0.2, -1.25, 0]), FadeIn(p_marks), run_time=1.3)
        self.play(FadeOut(grk), run_time=0.4)

        # Step 2: Arrestin reads that mark and covers the surface needed by G protein
        self.at("reads that mark")
        arr_dock = make_arrestin_clamp(rec_center=rec.rec_center, scale=1.0, label="arrestin", p_letters=True)
        arr = arr_dock.copy().shift(DOWN * 1.45)
        self.play(L.reveal(1), FadeIn(arr), run_time=0.6)

        self.at("covers the surface")
        self.play(arr.animate.move_to(arr_dock), run_time=1.3)

        # Writer identifies target; Reader produces the block -> G protein approaches and turns away
        self.at("The writer identifies")
        self.play(L.mark(0, color=REM_COL), run_time=0.6)

        gp_try = make_g_protein(pos=[-3.65, -3.15, 0], on=False, label="G protein", scale=0.90)
        self.play(FadeIn(gp_try), run_time=0.2)
        self.play(gp_try.animate.move_to([-3.65, -2.25, 0]), run_time=0.6)
        self.play(gp_try.animate.move_to([-5.2, -3.15, 0]), run_time=0.7)
        self.play(FadeOut(gp_try), run_time=0.2)

        self.at("The reader produces")
        self.play(L.mark(1, color=ARR_COL), run_time=0.5)

        for _ in range(2):
            gp = make_g_protein(pos=[-3.65, -3.15, 0], on=False, label="G protein", scale=0.90)
            self.play(FadeIn(gp), run_time=0.2)
            self.play(gp.animate.move_to([-3.65, -2.25, 0]), run_time=0.55)
            self.play(gp.animate.move_to([-5.2, -3.15, 0]), run_time=0.65)
            self.play(FadeOut(gp), run_time=0.15)
        self.finish()


class S10Rule(FilmScene):
    """Blocked receptor + schematic balance bar tipping toward removal + dwindling ON stream."""

    def construct(self):
        mem = make_membrane(x0=-6.4, x1=0.2, y=1.35)
        rec = make_receptor(center=[-3.5, 1.0, 0], scale=1.0, n_phosphates=4, show_agonist=True, show_dock=True, p_letters=True)
        arr_dock = make_arrestin_clamp(rec_center=rec.rec_center, scale=1.0, label="arrestin", p_letters=True)
        arr = arr_dock.copy().shift(DOWN * 1.15)
        tag = scope_tag("schematic")

        # Schematic balance beam on the right (tilt: 0 = level, +1 = tipped toward removal)
        tilt = ValueTracker(0.0)
        pivot_pt = np.array([3.3, 1.65, 0.0])
        fulcrum = Triangle(stroke_color=TEXT, stroke_width=2.5, fill_color=MEM_COL, fill_opacity=0.4).scale(0.28).move_to(pivot_pt + DOWN * 0.25)

        def mk_beam():
            ang = -0.32 * tilt.get_value()
            dx, dy = 1.95 * np.cos(ang), 1.95 * np.sin(ang)
            left_end = pivot_pt + np.array([-dx, -dy, 0])
            right_end = pivot_pt + np.array([dx, dy, 0])
            bar = Line(left_end, right_end, color=TEXT, stroke_width=5)
            l_lbl = boxed_label("new activation", GP_COL, size=24, pad=0.14).next_to(left_end, UP, buff=0.18)
            r_lbl = boxed_label("removal", REM_COL, size=24, pad=0.14).next_to(right_end, UP, buff=0.18)
            return VGroup(bar, l_lbl, r_lbl)

        beam = always_redraw(mk_beam)

        # Fixed-phase pre-built ON blocks: dropping slots by index prevents teleporting or low-contrast fading
        pool_n = ValueTracker(1.0)
        phase_tr = ValueTracker(0.0)
        phase_tr.add_updater(lambda m, dt: m.increment_value(0.45 * dt))

        stream_blocks = []
        for i in range(4):
            blk = make_g_protein(pos=[-1.8, -2.25, 0], on=True, label="G", scale=0.82)

            def mk_upd(idx):
                def upd(m):
                    n_active = max(1, int(round(4.0 * np.clip(pool_n.get_value(), 0.0, 1.0))))
                    if idx >= n_active:
                        set_gp_vis(m, False)
                        return
                    phase = (phase_tr.get_value() + idx * 0.25) % 1.0
                    pos = np.array([-1.8 + 7.2 * phase, -2.25 + 0.14 * np.sin(PI * phase), 0.0])
                    set_gp_vis(m.move_to(pos), True)
                return upd

            blk.add_updater(mk_upd(i))
            stream_blocks.append(blk)

        stream_lbl = T("departing ON G proteins", size=26, color=GP_COL).move_to([0.6, -3.05, 0])

        self.add(mem, rec, fulcrum, beam, phase_tr, *stream_blocks, stream_lbl, tag)
        self.wait(6.4)

        # Active layer fades when removal outruns production
        self.at("each active layer fades")
        self.play(
            tilt.animate(run_time=2.5).set_value(0.55),
            pool_n.animate(run_time=2.5).set_value(0.55),
        )

        # Mark and reader together prevent new G-protein activation
        self.at("new receptor signaling falls")
        self.play(FadeIn(arr, shift=UP * 0.3, run_time=0.5))
        self.play(arr.animate(run_time=0.9).move_to(arr_dock))
        self.at("mark and reader")
        self.play(
            tilt.animate(run_time=2.4).set_value(1.0),
            pool_n.animate(run_time=2.4).set_value(0.20),
        )
        rem = max(0.4, self.narration_s + 0.3 - self.elapsed())
        self.wait(rem)
        self.finish()


class S10Consequence(FilmScene):
    """Agonist stays firmly bound; outside signal holds steady while G-protein activation drops sharply (not to zero)."""

    def construct(self):
        mem = make_membrane(x0=-6.4, x1=0.2, y=1.35)
        rec = make_receptor(center=[-3.5, 1.0, 0], scale=1.0, n_phosphates=4, show_agonist=True, show_dock=True, p_letters=True)
        ag_lbl = T("agonist still bound", size=28, color=AG_COL).next_to(rec.agonist, UP, buff=0.38)
        arr_dock = make_arrestin_clamp(rec_center=rec.rec_center, scale=1.0, label="arrestin", p_letters=True)
        arr = arr_dock.copy().shift(DOWN * 1.15)

        out_t = ValueTracker(1.0)
        gp_t = ValueTracker(0.92)
        m_out = make_meter("outside signal", out_t, center=[1.6, 0.35, 0], height=2.5, color=AG_COL)
        m_gp = make_meter("G-protein\nactivation", gp_t, center=[4.5, 0.35, 0], height=2.5, color=GP_COL)

        # Monotonic phase integrator on a single pre-built ON block clear of arrestin & meters
        phase_tr = ValueTracker(0.0)
        phase_tr.add_updater(lambda m, dt: m.increment_value((0.32 + 0.80 * gp_t.get_value()) * dt))

        stream_mob = make_g_protein(pos=[0.5, -2.45, 0], on=True, label="G", scale=0.80)
        stream_mob.add_updater(lambda m: m.move_to([0.5 + 4.0 * (phase_tr.get_value() % 1.0), -2.45, 0.0]))
        tag = scope_tag("schematic")

        self.add(mem, rec, ag_lbl, arr, m_out, m_gp, phase_tr, stream_mob, tag)
        self.wait(3.8)

        # Agonist need not leave first -> highlight bound agonist
        self.at("The agonist need")
        lock_ring = SurroundingRectangle(rec.agonist, color=AG_COL, buff=0.10, stroke_width=3, corner_radius=0.10)
        self.play(Create(lock_ring, run_time=0.6))

        # Receptor remains occupied while access changes
        self.at("access changes")
        self.play(arr.animate(run_time=1.3).move_to(arr_dock))

        # Desensitization records regulation inside the cell, not disappearance of outside signal
        self.at("Desensitization therefore")
        reg_lbl = T("inside regulation", size=28, color=ARR_COL).move_to([-3.5, -3.15, 0])
        self.play(
            FadeIn(reg_lbl, run_time=0.5),
            gp_t.animate(run_time=2.5).set_value(0.16),
        )
        rem = max(0.4, self.narration_s + 0.3 - self.elapsed())
        self.wait(rem)
        self.finish()


class S11Handoff(FilmScene):
    """Pull back from blocked receptor; extend 3 downstream layers + live computed persistence Plot."""

    def construct(self):
        # Upper-left: pulled-back blocked receptor with arrestin clamped
        mem = make_membrane(x0=-6.4, x1=-0.8, y=2.55, thickness=0.28)
        rec = make_receptor(center=[-4.4, 2.35, 0], scale=0.60, n_phosphates=4, show_agonist=True, show_dock=False, p_letters=False)
        arr = make_arrestin_clamp(rec_center=rec.rec_center, scale=0.60, label="arrestin", p_letters=False)
        rec_lbl = T("receptor blocked", size=26, color=ARR_COL).move_to([-3.7, 3.35, 0])

        # Downstream chain extending downward on left
        g_node = boxed_label("active G proteins", GP_COL, size=26, pad=0.16).move_to([-4.1, -0.15, 0])
        m_node = boxed_label("second messengers", CN_COL, size=26, pad=0.16).move_to([-4.1, -1.45, 0])
        t_box = boxed_label("target", TEXT, size=26, pad=0.16).move_to([-4.4, -2.75, 0])
        t_p = make_p_badge([t_box.get_right()[0] + 0.40, t_box.get_center()[1], 0], radius=0.25, with_letter=True)
        t_node = VGroup(t_box, t_p)

        a1 = Arrow([g_node.get_center()[0], arr.get_bottom()[1], 0], g_node.get_top(), color=GP_COL, stroke_width=3, buff=0.10)
        a2 = Arrow(g_node.get_bottom(), m_node.get_top(), color=CN_COL, stroke_width=3, buff=0.10)
        a3 = Arrow(m_node.get_bottom(), t_box.get_top(), color=PHOS_COL, stroke_width=3, buff=0.10)

        # Right side: computed Plot showing downstream layers persisting after receptor coupling falls
        P = Plot(
            box=(0.4, 5.9, -2.0, 2.3),
            xr=(0, 10),
            yr=(0, 1.1),
            xticks=[0, 5, 10],
            yticks=[(0, "0"), (1, "1")],
            xlabel="time (schematic)",
            ylabel="active pool",
            size=24,
            label_size=26,
        )
        t_tr = ValueTracker(0.0)
        fn_rec = lambda x: np.exp(-1.1 * x)
        fn_gp = lambda x: np.exp(-0.50 * x)
        fn_cn = lambda x: np.exp(-0.28 * x)
        fn_tgt = lambda x: np.exp(-0.14 * x)

        c_rec = P.live_curve(fn_rec, t_tr, color=ARR_COL, width=4)
        c_gp = P.live_curve(fn_gp, t_tr, color=GP_COL, width=5)
        c_cn = P.live_curve(fn_cn, t_tr, color=CN_COL, width=5)
        c_tgt = P.live_curve(fn_tgt, t_tr, color=PHOS_COL, width=5)

        # Live pool bars beside each downstream node driven by the exact same exp(-k_i * t_tr)
        def mk_pool_bar(y_pos, fn, col):
            x_left, max_w, h = -2.15, 1.55, 0.28
            track = RoundedRectangle(corner_radius=0.06, width=max_w, height=h, stroke_color=MEM_COL,
                                     stroke_width=2, fill_color=BG, fill_opacity=0.85).move_to([x_left + max_w / 2, y_pos, 0])

            def mk_fill():
                v = float(np.clip(fn(t_tr.get_value()), 0.02, 1.0))
                w = max(0.05, v * (max_w - 0.06))
                return RoundedRectangle(corner_radius=0.04, width=w, height=h - 0.06, stroke_width=0,
                                        fill_color=col, fill_opacity=0.88).move_to([x_left + 0.03 + w / 2, y_pos, 0])

            return track, always_redraw(mk_fill).set_z_index(2)

        trk_gp, fill_gp = mk_pool_bar(-0.15, fn_gp, GP_COL)
        trk_cn, fill_cn = mk_pool_bar(-1.45, fn_cn, CN_COL)
        trk_tgt, fill_tgt = mk_pool_bar(-2.75, fn_tgt, PHOS_COL)

        # Moving downstream carrier beads along the arrows while pools persist
        flow_t = ValueTracker(0.0)
        flow_t.add_updater(lambda m, dt: m.increment_value(1.2 * dt))

        def mk_flow_dot(arrow, fn, col):
            p0, p1 = arrow.get_start(), arrow.get_end()
            return always_redraw(lambda: Dot(
                p0 + (p1 - p0) * (flow_t.get_value() % 1.0),
                radius=0.07,
                color=col,
            ).set_opacity(float(np.clip(fn(t_tr.get_value()), 0.15, 1.0))))

        d1 = mk_flow_dot(a1, fn_gp, GP_COL)
        d2 = mk_flow_dot(a2, fn_cn, CN_COL)
        d3 = mk_flow_dot(a3, fn_tgt, PHOS_COL)

        legend = VGroup(
            T("receptor", size=24, color=ARR_COL),
            T("G protein", size=24, color=GP_COL),
            T("messenger", size=24, color=CN_COL),
            T("target", size=24, color=PHOS_COL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([4.9, 1.45, 0])

        tag = scope_tag("schematic")

        self.play(FadeIn(mem, rec, arr, rec_lbl, P, legend, tag), run_time=0.8)
        self.add(c_rec, c_gp, c_cn, c_tgt, flow_t)

        self.at("Active G proteins")
        self.add(fill_gp)
        self.play(FadeIn(a1, g_node, trk_gp, run_time=0.5), t_tr.animate(run_time=1.3, rate_func=linear).set_value(2.0))
        self.add(d1)

        self.at("second messengers")
        self.add(fill_cn)
        self.play(FadeIn(a2, m_node, trk_cn, run_time=0.5), t_tr.animate(run_time=1.2, rate_func=linear).set_value(3.4))
        self.add(d2)

        self.at("phosphorylated targets")
        self.add(fill_tgt)
        self.play(FadeIn(a3, t_node, trk_tgt, run_time=0.5), t_tr.animate(run_time=1.4, rate_func=linear).set_value(5.0))
        self.add(d3)

        self.at("persist after")
        self.play(t_tr.animate(run_time=3.2, rate_func=linear).set_value(7.5))

        self.at("Their removal processes")
        rem_tag = T("removal processes", size=26, color=REM_COL).move_to([4.3, 2.95, 0])
        self.play(FadeIn(rem_tag, run_time=0.5), t_tr.animate(run_time=3.4, rate_func=linear).set_value(10.0))
        self.finish()


class S12End(EndCard):
    LINE = "A GRK mark does little until arrestin reads it."
