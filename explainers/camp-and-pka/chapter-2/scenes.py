"""
PKA: The Target Sets the Response — camp-and-pka__chapter-2

COLOUR MAP (one colour per concept across the whole film):
- GREY   (#8B93A1): plasma membrane, cell boundaries, non-compatible targets, intracellular obstacles
- GOLD   (#D4A843): cyclic AMP (cAMP) tokens, cAMP level gauge, transferred phosphate (P) badges
- BLUE   (#58C4DD): adenylyl cyclase (cAMP synthesis / local source)
- RED    (#FC6255): phosphodiesterase (cAMP breakdown / local sink), OFF state
- TEAL   (#3FB8C0): PKA catalytic subunits (C) / active kinase & its substrate groove
- PURPLE (#B589D6): PKA regulatory subunits (R), blocking segments/tabs, cAMP-binding blocks
- GREEN  (#83C167): compatible PKA target proteins / substrates & cell-specific responses
- TEXT   (#E8EAF0): anchoring protein (AKAP) scaffold, ATP chip, primary labels & headings

ONE WORLD PICTURE:
A 16:9 dark cytosol cross-section beneath a horizontal GREY plasma membrane. Synthesis (BLUE
cyclase) makes GOLD cAMP and breakdown (RED phosphodiesterase) removes it; GOLD cAMP opens the
TEAL-PURPLE R2C2 PKA complex so TEAL catalytic grooves can phosphorylate reachable GREEN targets
in heart, fat, and liver cells or in local AKAP neighbourhoods within a single cell.

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
- s00_link_and_question: GOLD cAMP gauge settles via dc/dt = s - k*c (s=2, k=4), transforms into
  6 GOLD tokens moving to an R2C2 complex, then pulls back into heart and fat panels with distinct
  GREEN targets approaching PKA beside unanswered '?' outputs.
- s02_resting_complex: Four separated subunits (2 PURPLE R, 2 TEAL C) slide together into an R2C2
  tetramer; each C groove highlights, then each R blocking tab slides into its C groove and locks OFF.
- s03_blocked_groove: Magnified TEAL C block zooms in and receives ATP into its ATP pocket; PURPLE
  R tab slides from below-left into the substrate groove ahead of an approaching GREEN substrate,
  which collides and recoils via a damped collision curve while its phosphate badge stays empty.
- s04_camp_relieves: Four GOLD cAMP tokens move along curved paths into the 4 R sites; R subunits
  hinge outward and withdraw their tabs; C subunits slide free ('classical model'), rewind back to
  tethered reach ('anchored complexes may remain associated'), and targets approach beside '?'.
- s05_predict_targets: Two cell panels build step-by-step with identical GOLD cAMP and TEAL PKA;
  left gets round-ended GREEN strips and right gets forked GREEN strips, both advancing toward the
  grooves while the top equality question appears.
- s07_reveal: Equality question swaps to 'not necessarily'; round and forked GREEN strips dock into
  identical TEAL grooves, receive GOLD P badges, trigger matching output icons, while GREY
  incompatible strips drift past.
- s08_cell_examples: Left cell expands; in FAT, lipase and perilipin gain GOLD P and a fat droplet
  shrinks while releasing 5 fuel droplets; morphs to HEART where 3 targets drive output arrows and
  a contraction bar rises and relaxes; morphs to LIVER with glycogen-control enzymes phosphorylated.
- s09_addresses: One large cell builds a 5-part left neighbourhood (WHITE anchoring protein, TEAL
  PKA, GREEN substrate, BLUE cyclase emitting diffusing GOLD cAMP, RED PDE removing nearby tokens),
  then slides the whole 5-part assembly right leaving a faint site marker behind.
- s10_compartments: Computed 2D GOLD cAMP particle cloud diffuses from a membrane source; four
  unresolved candidate influences (BLUE source, RED sink, PURPLE transient binding, GREY tortuous
  obstacles) act on the live particles under 'candidate contributors ?' beside 'local responses observed'.
- s11_handoff: Opens on one exposed TEAL groove beside a waiting GREEN substrate and competing strip
  with a blank '?' result panel, then pulls back to observed diffusing local GOLD clouds with the four
  candidate '?' badges unresolved.
"""
from bp_parts import *

PURPLE = "#B589D6"
MEMBRANE_COL = GREY
CAMP_COL = GOLD
SYNTH_COL = BLUE
BREAK_COL = RED
PKA_COL = TEAL
REG_COL = PURPLE
TARGET_COL = GREEN
AKAP_COL = TEXT


# ------------------------------------------------------------------ shared shape builders
def make_c_block(w=1.85, h=2.4, groove_facing=LEFT, groove_w=0.68, groove_h=0.92,
                 color=PKA_COL, label="C", label_size=28):
    """Build a TEAL catalytic subunit block centered at (0,0) with an inward-facing substrate groove."""
    hw, hh = w / 2.0, h / 2.0
    gh2 = groove_h / 2.0
    if groove_facing is LEFT:
        pts = [
            [-hw, hh, 0], [hw, hh, 0], [hw, -hh, 0], [-hw, -hh, 0],
            [-hw, -gh2, 0], [-hw + groove_w, -gh2 * 0.78, 0],
            [-hw + groove_w, gh2 * 0.78, 0], [-hw, gh2, 0],
        ]
        lx = (-hw + groove_w + hw) * 0.5
    else:
        pts = [
            [hw, hh, 0], [-hw, hh, 0], [-hw, -hh, 0], [hw, -hh, 0],
            [hw, -gh2, 0], [hw - groove_w, -gh2 * 0.78, 0],
            [hw - groove_w, gh2 * 0.78, 0], [hw, gh2, 0],
        ]
        lx = (hw - groove_w - hw) * 0.5
    body = Polygon(*pts, color=color, stroke_width=3.5, fill_color=color, fill_opacity=0.22)
    body.round_corners(radius=0.08)
    g = VGroup(body)
    if label:
        lab = T(label, size=label_size, color=color, weight=BOLD).move_to([lx, 0, 0])
        g.add(lab)
        g.label = lab
    g.body = body
    gx = -hw + groove_w * 0.45 if groove_facing is LEFT else hw - groove_w * 0.45
    g.groove_offset = np.array([gx, 0.0, 0.0])
    return g


def make_r_block(w=1.25, h=2.2, tab_dir=LEFT, tab_len=0.58, tab_h=0.60,
                 color=REG_COL, label="R", label_size=28, camp_sites=True):
    """Build a PURPLE regulatory block whose rectangular body is at (0,0); use move_r() to position."""
    hw, hh = w / 2.0, h / 2.0
    th2 = tab_h / 2.0
    if tab_dir is LEFT:
        pts = [
            [-hw, hh, 0], [hw, hh, 0], [hw, -hh, 0], [-hw, -hh, 0],
            [-hw, -th2, 0], [-hw - tab_len, -th2 * 0.72, 0],
            [-hw - tab_len, th2 * 0.72, 0], [-hw, th2, 0],
        ]
        tab_cx = -hw - tab_len * 0.5
        sx = -hw * 0.20
        bbox_dx = -tab_len * 0.5
    else:
        pts = [
            [hw, hh, 0], [-hw, hh, 0], [-hw, -hh, 0], [hw, -hh, 0],
            [hw, -th2, 0], [hw + tab_len, -th2 * 0.72, 0],
            [hw + tab_len, th2 * 0.72, 0], [hw, th2, 0],
        ]
        tab_cx = hw + tab_len * 0.5
        sx = hw * 0.20
        bbox_dx = tab_len * 0.5
    body = Polygon(*pts, color=color, stroke_width=3.5, fill_color=color, fill_opacity=0.24)
    body.round_corners(radius=0.06)
    g = VGroup(body)
    sites = VGroup()
    if camp_sites:
        for sy in (hh - 0.36, -hh + 0.36):
            ring = Circle(radius=0.17, color=GOLD, stroke_width=2.5, fill_color=BG, fill_opacity=0.95)
            ring.move_to([sx, sy, 0])
            sites.add(ring)
        g.add(sites)
    g.sites = sites
    if label:
        lab = T(label, size=label_size, color=color, weight=BOLD).move_to([0, 0, 0])
        g.add(lab)
        g.label = lab
    g.body = body
    g.body_w = w
    g.bbox_offset = np.array([bbox_dx, 0.0, 0.0])
    g.tab_offset = np.array([tab_cx, 0.0, 0.0])
    return g


def move_r(r, body_pos):
    """Move an R block so its rectangular body center sits at `body_pos` (accounting for protruding tab)."""
    return r.move_to(np.array(body_pos, dtype=float) + r.bbox_offset)


def make_camp_token(radius=0.14):
    """A single GOLD cAMP messenger token (simple dot, no molecular structure)."""
    return Circle(radius=radius, color=CAMP_COL, stroke_width=2.5, fill_color=CAMP_COL, fill_opacity=0.90)


def make_phosphate_badge(filled=False, radius=0.26):
    """Empty dashed circle or filled GOLD 'P' phosphate badge with ample internal margin."""
    if filled:
        c = Circle(radius=radius, color=CAMP_COL, stroke_width=2.5, fill_color=CAMP_COL, fill_opacity=0.95)
        p = T("P", size=22, color=BG, weight=BOLD).move_to(c)
        return VGroup(c, p)
    c = DashedVMobject(Circle(radius=radius, color=TEXT, stroke_width=2.5), num_dashes=10)
    return VGroup(c)


def make_target_strip(tip="round", text="", color=TARGET_COL, w=2.2, h=0.66,
                      tip_dir=RIGHT, size=24, phosphate=None):
    """A target protein strip with round, forked, or blunt tip and phosphate badge clear of border."""
    hw, hh = w / 2.0, h / 2.0
    if tip == "round":
        base = RoundedRectangle(corner_radius=hh * 0.48, width=w, height=h,
                                stroke_color=color, stroke_width=3.0, fill_color=color, fill_opacity=0.20)
    elif tip == "forked":
        if tip_dir is RIGHT:
            pts = [
                [-hw, hh, 0], [hw * 0.65, hh, 0], [hw, hh * 0.72, 0],
                [hw * 0.42, 0, 0], [hw, -hh * 0.72, 0], [hw * 0.65, -hh, 0],
                [-hw, -hh, 0],
            ]
        else:
            pts = [
                [hw, hh, 0], [-hw * 0.65, hh, 0], [-hw, hh * 0.72, 0],
                [-hw * 0.42, 0, 0], [-hw, -hh * 0.72, 0], [-hw * 0.65, -hh, 0],
                [hw, -hh, 0],
            ]
        base = Polygon(*pts, color=color, stroke_width=3.0, fill_color=color, fill_opacity=0.20)
        base.round_corners(radius=0.05)
    else:
        base = Rectangle(width=w, height=h, stroke_color=color, stroke_width=2.5,
                         fill_color=color, fill_opacity=0.14)
    g = VGroup(base)
    g.body = base
    if text:
        lab = fit_text(text, max_w=w - 0.35, size=size, color=color, min_size=24, max_lines=1)
        shift_x = -0.14 if tip == "forked" and tip_dir is RIGHT else (0.14 if tip == "forked" and tip_dir is LEFT else 0.0)
        lab.move_to([shift_x, 0, 0])
        g.add(lab)
        g.label = lab
    if phosphate is not None:
        bx = -hw + 0.34 if tip_dir is RIGHT else hw - 0.34
        badge = make_phosphate_badge(filled=(phosphate == "full"), radius=0.25).move_to([bx, hh + 0.34, 0])
        g.add(badge)
        g.badge = badge
    return g


def make_cell_membrane(y=2.3, x0=-6.4, x1=6.4, thickness=0.26, gap_center=None, gap_w=0.0):
    """Horizontal GREY plasma membrane bilayer bar, with optional clean gap for embedded cyclase."""
    if gap_center is None or gap_w <= 0:
        segs = [(x0, x1)]
    else:
        segs = [(x0, gap_center - gap_w / 2.0), (gap_center + gap_w / 2.0, x1)]
    g = VGroup()
    for a, b in segs:
        if b - a <= 0.05:
            continue
        top = Line([a, y + thickness / 2, 0], [b, y + thickness / 2, 0], color=MEMBRANE_COL, stroke_width=5)
        bot = Line([a, y - thickness / 2, 0], [b, y - thickness / 2, 0], color=MEMBRANE_COL, stroke_width=5)
        band = Rectangle(width=b - a, height=thickness, stroke_width=0, fill_color=MEMBRANE_COL, fill_opacity=0.18)
        band.move_to([(a + b) / 2, y, 0])
        g.add(band, top, bot)
    return g


def build_predict_world(with_question=True):
    """Exact two-cell predict backdrop shared by s05_predict_targets, s06_predict_pause, and s07_reveal."""
    tp = TwoPanel("one cell", "other cell", colors=(PKA_COL, PKA_COL), top=2.65, bottom=-2.55, gap=0.45, width=12.6, size=28)
    tp.remove(tp.left_head, tp.right_head)
    lh = T("one cell", size=28, color=TEXT, weight=BOLD).move_to(tp.left_head)
    rh = T("other cell", size=28, color=TEXT, weight=BOLD).move_to(tp.right_head)
    tp.left_head = lh
    tp.right_head = rh
    tp.add(lh, rh)

    shared_items = {}
    for side, cx in (("left", -3.25), ("right", 3.25)):
        mem = make_cell_membrane(y=1.75, x0=cx - 2.75, x1=cx + 2.75, thickness=0.18)
        camp_pts = [
            [cx - 2.25, 1.15, 0], [cx - 1.72, 1.32, 0], [cx - 1.55, 0.85, 0], [cx - 2.15, 0.65, 0]
        ]
        camps = VGroup(*[make_camp_token(radius=0.12).move_to(p) for p in camp_pts])
        camp_lab = T("cAMP", size=24, color=CAMP_COL, weight=BOLD).move_to([cx - 1.9, 0.15, 0])
        pka = make_c_block(w=1.55, h=1.65, groove_facing=RIGHT, groove_w=0.52, groove_h=0.72,
                           label="PKA", label_size=24).move_to([cx - 0.35, 0.72, 0])
        out_box = RoundedRectangle(corner_radius=0.12, width=3.6, height=0.88,
                                   stroke_color=GREY, stroke_width=2.5, fill_color=BG, fill_opacity=0.85)
        out_box.move_to([cx, -1.88, 0])
        out_q = T("response: ?", size=24, color=TEXT).move_to(out_box)
        shared_items[side] = {
            "cx": cx, "mem": mem, "camps": camps, "camp_lab": camp_lab,
            "pka": pka, "out_box": out_box, "out_q": out_q,
        }

    left_strips = VGroup(
        make_target_strip("round", "", TARGET_COL, w=1.45, h=0.46, tip_dir=LEFT, phosphate="empty").move_to([-1.45, 0.72, 0]),
        make_target_strip("round", "", TARGET_COL, w=1.45, h=0.46, tip_dir=LEFT, phosphate="empty").move_to([-1.45, -0.52, 0]),
    )
    right_strips = VGroup(
        make_target_strip("forked", "", TARGET_COL, w=1.45, h=0.46, tip_dir=LEFT, phosphate="empty").move_to([5.05, 0.72, 0]),
        make_target_strip("forked", "", TARGET_COL, w=1.45, h=0.46, tip_dir=LEFT, phosphate="empty").move_to([5.05, -0.52, 0]),
    )
    shared_items["left"]["strips"] = left_strips
    shared_items["right"]["strips"] = right_strips

    world = VGroup(tp)
    for side in ("left", "right"):
        d = shared_items[side]
        world.add(d["mem"], d["camps"], d["camp_lab"], d["pka"], d["out_box"], d["out_q"], d["strips"])

    if with_question:
        q = question_card("Same cAMP + same PKA = same response?", y=3.25, left=-6.0, max_w=10.4, size=30).question
        world.add(q)
        shared_items["question"] = q
    return world, shared_items


# ------------------------------------------------------------------ scenes
class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        membrane = make_cell_membrane(y=2.25, x0=-6.1, x1=6.1, thickness=0.28, gap_center=-3.6, gap_w=2.05)
        mem_lab = T("plasma membrane", size=24, color=MEMBRANE_COL).move_to([3.85, 2.72, 0])
        cyt_lab = T("cytosol", size=24, color=MEMBRANE_COL).move_to([-5.0, -2.5, 0])

        cyclase = boxed_label("cyclase", SYNTH_COL, size=26, box=(1.8, 0.68)).move_to([-3.6, 2.25, 0])
        pde = boxed_label("PDE", BREAK_COL, size=26, box=(1.35, 0.68)).move_to([-1.05, -1.5, 0])

        c_val = ValueTracker(0.18)
        gauge_frame = RoundedRectangle(corner_radius=0.1, width=0.9, height=2.6,
                                       stroke_color=CAMP_COL, stroke_width=3, fill_color=BG, fill_opacity=0.9)
        gauge_frame.move_to([-2.4, 0.1, 0])
        gauge_fill = always_redraw(lambda: Rectangle(
            width=0.76,
            height=max(0.08, 2.4 * float(np.clip(c_val.get_value(), 0.02, 1.0))),
            stroke_width=0, fill_color=CAMP_COL, fill_opacity=0.85,
        ).align_to(gauge_frame.get_bottom() + UP * 0.08, DOWN).set_x(gauge_frame.get_x()))
        gauge_lab = T("cAMP", size=26, color=CAMP_COL, weight=BOLD).next_to(gauge_frame, LEFT, buff=0.24)

        synth_arr = Arrow([-3.5, 1.82, 0], [-2.78, 1.28, 0], color=SYNTH_COL, stroke_width=5, buff=0.05)
        break_arr = Arrow([-2.0, -0.75, 0], [-1.35, -1.12, 0], color=BREAK_COL, stroke_width=5, buff=0.05)
        stag = scope_tag("schematic")

        self.add(membrane, mem_lab, cyt_lab, cyclase, gauge_frame, gauge_fill, gauge_lab, stag)
        self.at("synthesis")
        self.play(GrowArrow(synth_arr), c_val.animate.set_value(0.84), run_time=self.beat(0.06))
        self.at("breakdown")
        # Computed exponential relaxation dc/dt = 2 - 4*c settling to steady state 0.50 over 4s
        self.play(FadeIn(pde), GrowArrow(break_arr), run_time=self.beat(0.04))
        self.play(c_val.animate.set_value(0.50), run_time=self.beat(0.18), rate_func=there_and_back_with_pause if False else rush_from)

        # Stage 2: Transform gauge into 6 GOLD tokens moving to a large TEAL-PURPLE PKA complex
        r_left = make_r_block(w=1.05, h=1.95, tab_dir=LEFT, tab_len=0.45, tab_h=0.50, label="R", label_size=26)
        r_right = make_r_block(w=1.05, h=1.95, tab_dir=RIGHT, tab_len=0.45, tab_h=0.50, label="R", label_size=26)
        move_r(r_left, [1.575, 0.05, 0])
        move_r(r_right, [2.625, 0.05, 0])
        c_left = make_c_block(w=1.55, h=2.15, groove_facing=RIGHT, groove_w=0.52, groove_h=0.72, label="C", label_size=28).move_to([0.28, 0.05, 0])
        c_right = make_c_block(w=1.55, h=2.15, groove_facing=LEFT, groove_w=0.52, groove_h=0.72, label="C", label_size=28).move_to([3.92, 0.05, 0])
        pka_group = VGroup(c_left, c_right, r_left, r_right)
        pka_lab = T("PKA", size=30, color=PKA_COL, weight=BOLD).next_to(pka_group, UP, buff=0.28)

        tokens = VGroup(*[
            make_camp_token(radius=0.14).move_to([-2.4 + (i % 2) * 0.25 - 0.12, -0.6 + (i // 2) * 0.55, 0])
            for i in range(6)
        ])

        self.at("activates")
        self.play(
            FadeOut(synth_arr), FadeOut(break_arr), FadeOut(pde), FadeOut(cyclase),
            FadeOut(gauge_fill), ReplacementTransform(gauge_frame, tokens),
            FadeIn(pka_group), FadeIn(pka_lab),
            run_time=self.beat(0.08),
        )
        token_targets = [
            r_left.sites[0].get_center(), r_left.sites[1].get_center(),
            r_right.sites[0].get_center(), r_right.sites[1].get_center(),
            [1.1, 1.32, 0], [3.1, 1.32, 0],
        ]
        self.play(
            *[tok.animate.move_to(pos) for tok, pos in zip(tokens, token_targets)],
            run_time=self.beat(0.09),
        )

        # Stage 3: Pull back into heart-cell panel and fat-cell panel, question across top
        self.at("why do heart")
        q_top = T("Why do heart and fat cells respond differently?", size=32, color=CAMP_COL, weight=BOLD).move_to([0, 3.25, 0])
        tp = TwoPanel("heart cell", "fat cell", colors=(PKA_COL, PKA_COL), top=2.65, bottom=-2.55, gap=0.45, width=12.6, size=30)

        h_c = make_c_block(w=1.45, h=1.55, groove_facing=RIGHT, groove_w=0.48, groove_h=0.64, label="PKA", label_size=24).move_to([-3.65, 0.78, 0])
        f_c = make_c_block(w=1.45, h=1.55, groove_facing=RIGHT, groove_w=0.48, groove_h=0.64, label="PKA", label_size=24).move_to([2.85, 0.78, 0])
        h_camps = VGroup(*[make_camp_token(0.11).move_to([-5.55 + (i % 2) * 0.42, 1.15 - (i // 2) * 0.45, 0]) for i in range(4)])
        f_camps = VGroup(*[make_camp_token(0.11).move_to([0.95 + (i % 2) * 0.42, 1.15 - (i // 2) * 0.45, 0]) for i in range(4)])

        h_out = RoundedRectangle(corner_radius=0.14, width=2.6, height=0.88, stroke_color=CAMP_COL, stroke_width=2.5).move_to([-3.25, -1.8, 0])
        h_q = T("response: ?", size=26, color=CAMP_COL, weight=BOLD).move_to(h_out)
        f_out = RoundedRectangle(corner_radius=0.14, width=2.6, height=0.88, stroke_color=CAMP_COL, stroke_width=2.5).move_to([3.25, -1.8, 0])
        f_q = T("response: ?", size=26, color=CAMP_COL, weight=BOLD).move_to(f_out)

        self.play(
            FadeOut(membrane), FadeOut(mem_lab), FadeOut(cyt_lab), FadeOut(gauge_lab),
            FadeOut(pka_group), FadeOut(pka_lab), FadeOut(tokens),
            FadeIn(q_top), FadeIn(tp),
            FadeIn(h_c), FadeIn(f_c), FadeIn(h_camps), FadeIn(f_camps),
            FadeIn(h_out), FadeIn(h_q), FadeIn(f_out), FadeIn(f_q),
            run_time=self.beat(0.10),
        )

        self.at("messenger is common")
        self.play(
            h_camps.animate.shift(RIGHT * 0.30),
            f_camps.animate.shift(RIGHT * 0.30),
            run_time=self.beat(0.12),
        )

        self.at("reachable machinery")
        h_targets = VGroup(
            make_target_strip("round", "", TARGET_COL, w=1.45, h=0.44, tip_dir=LEFT).move_to([-1.55, 1.05, 0]),
            make_target_strip("blunt", "", GREY, w=1.45, h=0.44, tip_dir=LEFT).move_to([-1.55, 0.20, 0]),
        )
        f_targets = VGroup(
            make_target_strip("forked", "", TARGET_COL, w=1.45, h=0.44, tip_dir=LEFT).move_to([4.95, 1.05, 0]),
            make_target_strip("blunt", "", GREY, w=1.45, h=0.44, tip_dir=LEFT).move_to([4.95, 0.20, 0]),
        )
        self.play(FadeIn(h_targets, shift=LEFT * 0.2), FadeIn(f_targets, shift=LEFT * 0.2), run_time=self.beat(0.10))
        self.play(h_targets[0].animate.shift(LEFT * 0.30), f_targets[0].animate.shift(LEFT * 0.30), run_time=self.beat(0.12))

        self.at("puzzle")
        self.play(Indicate(h_q, color=CAMP_COL, scale_factor=1.08), Indicate(f_q, color=CAMP_COL, scale_factor=1.08), run_time=self.beat(0.06))
        self.finish()


class S01Title(TitleCard):
    LESSON = "cAMP and Protein Kinase A"
    TITLE = "PKA: The Target Sets the Response"


class S02RestingComplex(SpokenScene):
    def construct(self):
        r_left = make_r_block(w=1.55, h=2.95, tab_dir=LEFT, tab_len=0.72, tab_h=0.82, label="R", label_size=34, camp_sites=False)
        r_right = make_r_block(w=1.55, h=2.95, tab_dir=RIGHT, tab_len=0.72, tab_h=0.82, label="R", label_size=34, camp_sites=False)
        c_left = make_c_block(w=2.35, h=3.25, groove_facing=RIGHT, groove_w=0.85, groove_h=1.18, label="C", label_size=36)
        c_right = make_c_block(w=2.35, h=3.25, groove_facing=LEFT, groove_w=0.85, groove_h=1.18, label="C", label_size=36)

        move_r(r_left, [-1.45, -0.15, 0])
        move_r(r_right, [1.45, -0.15, 0])
        c_left.move_to([-4.6, -0.15, 0])
        c_right.move_to([4.6, -0.15, 0])

        stag = scope_tag("schematic")
        self.add(c_left, c_right, r_left, r_right, stag)
        self.play(
            c_left.animate.move_to([-3.95, -0.15, 0]),
            c_right.animate.move_to([3.95, -0.15, 0]),
            run_time=self.beat(0.16),
        )

        self.at("paired")
        r2c2_lab = T("R2C2", size=40, color=TEXT, weight=BOLD).move_to([-1.6, 3.05, 0])
        four_lab = T("4 subunits", size=32, color=CAMP_COL, weight=BOLD).move_to([1.6, 3.05, 0])
        self.play(
            r_left.animate.shift(RIGHT * 0.675),
            r_right.animate.shift(LEFT * 0.675),
            FadeIn(r2c2_lab), FadeIn(four_lab),
            run_time=self.beat(0.14),
        )

        self.at("each catalytic")
        c_left_hi = c_left.body.copy().set_stroke(TEXT, width=6).set_fill(opacity=0)
        c_right_hi = c_right.body.copy().set_stroke(TEXT, width=6).set_fill(opacity=0)
        self.play(Create(c_left_hi), run_time=self.beat(0.08))
        self.play(FadeOut(c_left_hi), Create(c_right_hi), run_time=self.beat(0.08))
        self.play(FadeOut(c_right_hi), run_time=self.beat(0.04))

        self.at("each regulatory")
        self.play(c_left.animate.move_to([-2.73, -0.15, 0]), run_time=self.beat(0.08))
        self.at("keeps one")
        self.play(c_right.animate.move_to([2.73, -0.15, 0]), run_time=self.beat(0.09))

        self.at("inactive")
        off_l = boxed_label("OFF", BREAK_COL, size=26, box=(0.95, 0.50), fill_opacity=0.25).move_to([-1.95, 2.05, 0])
        off_r = boxed_label("OFF", BREAK_COL, size=26, box=(0.95, 0.50), fill_opacity=0.25).move_to([1.95, 2.05, 0])
        arr_l = Arrow(off_l.get_bottom() + DOWN * 0.06, [-1.95, 0.55, 0], color=BREAK_COL, stroke_width=4, buff=0.05)
        arr_r = Arrow(off_r.get_bottom() + DOWN * 0.06, [1.95, 0.55, 0], color=BREAK_COL, stroke_width=4, buff=0.05)
        self.play(FadeIn(off_l), FadeIn(off_r), run_time=self.beat(0.12))

        self.at("off switch")
        self.play(GrowArrow(arr_l), GrowArrow(arr_r), run_time=self.beat(0.10))
        self.finish()


class S03BlockedGroove(SpokenScene):
    def construct(self):
        c_big = make_c_block(w=5.8, h=4.9, groove_facing=LEFT, groove_w=2.1, groove_h=2.1, label="", color=PKA_COL)
        c_big.move_to([2.4, -0.15, 0])
        atp_pocket = RoundedRectangle(corner_radius=0.14, width=2.4, height=0.96,
                                      stroke_color=PKA_COL, stroke_width=3, fill_color=BG, fill_opacity=0.95)
        atp_pocket.move_to([2.25, 1.55, 0])
        atp_lab = T("ATP pocket", size=26, color=TEXT, weight=BOLD).move_to([2.25, 2.66, 0])
        groove_lab = T("substrate groove", size=28, color=PKA_COL, weight=BOLD).move_to([-2.35, -2.05, 0])
        stag = scope_tag("schematic")

        # Start zoomed slightly out and settle into full-frame magnification across 0..2.8s
        c_group = VGroup(c_big, atp_pocket)
        c_group.save_state()
        c_group.scale(0.84)
        self.add(c_group, atp_lab, groove_lab, stag)
        self.play(Restore(c_group), run_time=self.beat(0.14))

        atp_chip = boxed_label("ATP", TEXT, size=26, box=(1.1, 0.62), fill_opacity=0.18)
        atp_p = make_phosphate_badge(filled=True, radius=0.25).next_to(atp_chip, RIGHT, buff=0.18)
        atp_unit = VGroup(atp_chip, atp_p).move_to([-2.8, 2.0, 0])

        self.at("transferring phosphate")
        self.play(FadeIn(atp_unit), run_time=self.beat(0.06))
        self.play(atp_unit.animate.move_to(atp_pocket.get_center()), run_time=self.beat(0.12))

        sub = make_target_strip("round", "substrate", TARGET_COL, w=2.8, h=0.88, tip_dir=RIGHT, size=28, phosphate="empty")
        sub.move_to([-4.6, -0.15, 0])

        self.at("target must")
        self.play(FadeIn(sub, shift=RIGHT * 0.3), run_time=self.beat(0.06))
        self.play(sub.animate.move_to([-3.2, -0.15, 0]), run_time=self.beat(0.10))

        # PURPLE regulatory tab slides in from upper-left BELOW ATP pocket (y <= 0.45) to avoid straddling ATP!
        reg_tab = make_r_block(w=1.05, h=1.65, tab_dir=RIGHT, tab_len=1.35, tab_h=1.25,
                               color=REG_COL, label="R", label_size=30, camp_sites=False)
        move_r(reg_tab, [-2.2, 2.4, 0])
        reg_tab.set_opacity(0)

        self.at("regulatory segment")
        self.play(reg_tab.animate.set_opacity(1).shift(DOWN * 2.55 + RIGHT * 0.7), run_time=self.beat(0.08))
        self.at("occupies that groove")
        # Slide straight right into groove (y = -0.15, completely clear of ATP pocket at y = 1.55)
        self.play(reg_tab.animate.shift(RIGHT * 1.85), run_time=self.beat(0.11))

        self.at("blocking the groove")
        prog = ValueTracker(0.0)
        start_x = -3.2
        hit_x = -1.68

        def bump_pos(t):
            if t < 0.45:
                s = t / 0.45
                return start_x + (hit_x - start_x) * (1 - (1 - s) ** 2)
            s = (t - 0.45) / 0.55
            recoil = -0.82 * (1 - np.exp(-5.0 * s) * np.cos(1.8 * PI * s))
            return hit_x + recoil

        sub.add_updater(lambda m: m.set_x(bump_pos(prog.get_value())))
        self.play(prog.animate.set_value(1.0), run_time=self.beat(0.16), rate_func=linear)
        sub.clear_updaters()
        self.at("receiving phosphate")
        self.play(Indicate(sub.badge, color=TEXT, scale_factor=1.2), run_time=self.beat(0.08))
        self.finish()


class S04CampRelieves(SpokenScene):
    def construct(self):
        r_left = make_r_block(w=1.35, h=2.55, tab_dir=LEFT, tab_len=0.62, tab_h=0.68, label="R", label_size=30, camp_sites=True)
        r_right = make_r_block(w=1.35, h=2.55, tab_dir=RIGHT, tab_len=0.62, tab_h=0.68, label="R", label_size=30, camp_sites=True)
        c_left = make_c_block(w=2.05, h=2.75, groove_facing=RIGHT, groove_w=0.72, groove_h=0.98, label="C", label_size=32)
        c_right = make_c_block(w=2.05, h=2.75, groove_facing=LEFT, groove_w=0.72, groove_h=0.98, label="C", label_size=32)

        # Rectangular R bodies meet cleanly at x = 0 with zero overlap
        move_r(r_left, [-0.675, -0.25, 0])
        move_r(r_right, [0.675, -0.25, 0])
        c_left.move_to([-2.42, -0.25, 0])
        c_right.move_to([2.42, -0.25, 0])

        sites_lab = T("4 cAMP sites", size=28, color=CAMP_COL, weight=BOLD).move_to([0, 2.05, 0])
        stag = scope_tag("schematic")

        camp_starts = [[-4.8, 2.2, 0], [-4.8, -2.3, 0], [4.8, 2.2, 0], [4.8, -2.3, 0]]
        camps = VGroup(*[make_camp_token(0.15).move_to(p) for p in camp_starts])
        targets = [
            r_left.sites[0].get_center(), r_left.sites[1].get_center(),
            r_right.sites[0].get_center(), r_right.sites[1].get_center(),
        ]

        self.add(c_left, c_right, r_left, r_right, sites_lab, camps, stag)
        self.at("binds")
        self.play(*[c.animate.move_to(t) for c, t in zip(camps, targets)], run_time=self.beat(0.09))

        self.at("changes their shape")
        # Hinge TOPS OUTWARD cleanly around the inner bottom corners (0, -1.525)
        left_bound = VGroup(r_left, camps[0], camps[1])
        right_bound = VGroup(r_right, camps[2], camps[3])
        self.play(
            Rotate(left_bound, angle=0.16, about_point=[0.0, -1.525, 0]),
            Rotate(right_bound, angle=-0.16, about_point=[0.0, -1.525, 0]),
            run_time=self.beat(0.09),
        )
        self.at("release the grooves")
        self.play(
            c_left.animate.shift(LEFT * 0.72),
            c_right.animate.shift(RIGHT * 0.72),
            run_time=self.beat(0.09),
        )

        self.at("classical model")
        mod_lab = T("classical model", size=34, color=PKA_COL, weight=BOLD).move_to([0, 3.1, 0])
        self.play(FadeOut(sites_lab), FadeIn(mod_lab), run_time=self.beat(0.05))

        self.at("come away free")
        self.play(
            c_left.animate.move_to([-4.65, -0.25, 0]),
            c_right.animate.move_to([4.65, -0.25, 0]),
            run_time=self.beat(0.10),
        )

        self.at("evidence suggests")
        anch_lab = T("anchored complexes may remain associated", size=30, color=PKA_COL, weight=BOLD).move_to([0, 3.1, 0])
        tether_l = CurvedArrow([-1.45, -0.25, 0], [-2.55, -0.25, 0], angle=0.45, color=REG_COL, stroke_width=3, tip_length=0.01)
        tether_r = CurvedArrow([1.45, -0.25, 0], [2.55, -0.25, 0], angle=-0.45, color=REG_COL, stroke_width=3, tip_length=0.01)
        self.play(
            swap(mod_lab, anch_lab, run_time=self.beat(0.05)),
            c_left.animate.move_to([-3.55, -0.25, 0]).rotate(PI),
            c_right.animate.move_to([3.55, -0.25, 0]).rotate(PI),
            run_time=self.beat(0.11),
        )
        c_left.label.rotate(-PI)
        c_right.label.rotate(-PI)
        self.play(Create(tether_l), Create(tether_r), run_time=self.beat(0.08))

        self.at("either picture")
        both_lab = VGroup(
            T("classical model", size=26, color=PKA_COL),
            T("?", size=34, color=CAMP_COL, weight=BOLD),
            T("anchored complexes may remain associated", size=26, color=PKA_COL),
        ).arrange(RIGHT, buff=0.30).move_to([0, 3.1, 0])
        fit(both_lab, max_w=12.2)

        t_l = make_target_strip("round", "target", TARGET_COL, w=1.65, h=0.56, tip_dir=RIGHT, size=24).move_to([-5.6, -0.25, 0])
        t_r = make_target_strip("round", "target", TARGET_COL, w=1.65, h=0.56, tip_dir=LEFT, size=24).move_to([5.6, -0.25, 0])
        self.play(
            swap(anch_lab, both_lab, run_time=self.beat(0.05)),
            FadeIn(t_l, shift=RIGHT * 0.2), FadeIn(t_r, shift=LEFT * 0.2),
            run_time=self.beat(0.12),
        )
        self.play(t_l.animate.shift(RIGHT * 0.40), t_r.animate.shift(LEFT * 0.40), run_time=self.beat(0.13))
        self.finish()


class S05PredictTargets(SpokenScene):
    def construct(self):
        world, items = build_predict_world(with_question=False)
        stag = scope_tag("schematic")
        tp = world[0]
        left_strips = items["left"]["strips"]
        right_strips = items["right"]["strips"]
        left_strips.shift(RIGHT * 0.55).set_opacity(0)
        right_strips.shift(RIGHT * 0.55).set_opacity(0)

        l_mem, l_camps, l_clab, l_pka, l_ob, l_oq = (
            items["left"]["mem"], items["left"]["camps"], items["left"]["camp_lab"],
            items["left"]["pka"], items["left"]["out_box"], items["left"]["out_q"]
        )
        r_mem, r_camps, r_clab, r_pka, r_ob, r_oq = (
            items["right"]["mem"], items["right"]["camps"], items["right"]["camp_lab"],
            items["right"]["pka"], items["right"]["out_box"], items["right"]["out_q"]
        )
        self.add(tp, l_mem, r_mem, l_ob, l_oq, r_ob, r_oq, stag)
        self.play(
            FadeIn(l_pka, shift=DOWN * 0.2), FadeIn(r_pka, shift=DOWN * 0.2),
            run_time=self.beat(0.16),
        )
        self.play(
            FadeIn(l_camps, shift=RIGHT * 0.25), FadeIn(r_camps, shift=RIGHT * 0.25),
            FadeIn(l_clab), FadeIn(r_clab),
            run_time=self.beat(0.15),
        )

        self.at("same messenger")
        self.play(
            l_camps.animate.shift(RIGHT * 0.22),
            r_camps.animate.shift(RIGHT * 0.22),
            run_time=self.beat(0.14),
        )
        self.play(
            l_camps.animate.shift(LEFT * 0.22),
            r_camps.animate.shift(LEFT * 0.22),
            run_time=self.beat(0.10),
        )

        self.at("one cell")
        self.add(left_strips)
        self.play(left_strips.animate.set_opacity(1).shift(LEFT * 0.25), run_time=self.beat(0.10))

        self.at("different strips")
        self.add(right_strips)
        self.play(right_strips.animate.set_opacity(1).shift(LEFT * 0.25), run_time=self.beat(0.08))

        self.at("must their")
        q_card = question_card("Same cAMP + same PKA = same response?", y=3.25, left=-6.0, max_w=10.4, size=30).question
        self.play(
            FadeIn(q_card),
            left_strips.animate.shift(LEFT * 0.30),
            right_strips.animate.shift(LEFT * 0.30),
            run_time=self.beat(0.14),
        )
        self.finish()


class S06PredictPause(PredictPause):
    QUESTION = "Same cAMP + same PKA = same response?"
    OPTIONS = ()
    CARD = {"y": 3.25, "left": -6.0, "max_w": 10.4, "size": 30}
    RING_AT = (5.95, 3.25, 0)
    SECONDS = 4.5

    def backdrop(self):
        world, _ = build_predict_world(with_question=False)
        return VGroup(world, scope_tag("schematic"))


class S07Reveal(SpokenScene):
    def construct(self):
        world, items = build_predict_world(with_question=True)
        stag = scope_tag("schematic")
        self.add(world, stag)

        new_q = T("Same cAMP + same PKA  ->  not necessarily", size=30, color=CAMP_COL, weight=BOLD).move_to([0, 3.25, 0])
        self.play(swap(items["question"], new_q, run_time=self.beat(0.06)))

        self.at("active kinase")
        l_strip = items["left"]["strips"][0]
        l_out_icon = VGroup(
            Circle(radius=0.22, color=TARGET_COL, stroke_width=3, fill_color=TARGET_COL, fill_opacity=0.8),
            T("round output", size=24, color=TARGET_COL, weight=BOLD),
        ).arrange(RIGHT, buff=0.18).move_to(items["left"]["out_box"])

        self.play(l_strip.animate.move_to([-2.18, 0.72, 0]), run_time=self.beat(0.11))
        l_p = make_phosphate_badge(filled=True, radius=0.24).move_to(l_strip.badge)
        self.play(ReplacementTransform(l_strip.badge, l_p), run_time=self.beat(0.06))
        l_strip.badge = l_p
        self.play(
            swap(items["left"]["out_q"], l_out_icon, run_time=self.beat(0.06)),
            items["left"]["out_box"].animate.set_stroke(TARGET_COL),
        )

        self.at("different cells")
        r_strip = items["right"]["strips"][0]
        fork_sym = make_target_strip("forked", "", TARGET_COL, w=0.52, h=0.34, tip_dir=RIGHT)
        r_out_icon = VGroup(
            fork_sym,
            T("forked output", size=24, color=TARGET_COL, weight=BOLD),
        ).arrange(RIGHT, buff=0.18).move_to(items["right"]["out_box"])

        self.play(r_strip.animate.move_to([4.32, 0.72, 0]), run_time=self.beat(0.08))
        r_p = make_phosphate_badge(filled=True, radius=0.24).move_to(r_strip.badge)
        self.play(ReplacementTransform(r_strip.badge, r_p), run_time=self.beat(0.05))
        r_strip.badge = r_p
        self.play(
            swap(items["right"]["out_q"], r_out_icon, run_time=self.beat(0.05)),
            items["right"]["out_box"].animate.set_stroke(TARGET_COL),
        )

        self.at("identical messenger")
        grey_l = make_target_strip("blunt", "", GREY, w=1.4, h=0.40).move_to([-1.25, -1.05, 0])
        grey_r = make_target_strip("blunt", "", GREY, w=1.4, h=0.40).move_to([5.25, -1.05, 0])
        self.play(FadeIn(grey_l), FadeIn(grey_r), run_time=self.beat(0.04))
        self.play(
            grey_l.animate.move_to([-4.95, -1.05, 0]),
            grey_r.animate.move_to([1.55, -1.05, 0]),
            run_time=self.beat(0.18),
        )

        self.at("response follows")
        arr_l = Arrow(l_strip.get_bottom() + DOWN * 0.08, items["left"]["out_box"].get_top() + UP * 0.08,
                      color=TARGET_COL, stroke_width=4, buff=0.05)
        arr_r = Arrow(r_strip.get_bottom() + DOWN * 0.08, items["right"]["out_box"].get_top() + UP * 0.08,
                      color=TARGET_COL, stroke_width=4, buff=0.05)
        self.play(
            l_strip.animate.move_to([-2.4, -0.05, 0]),
            r_strip.animate.move_to([4.1, -0.05, 0]),
            FadeOut(items["left"]["strips"][1]), FadeOut(items["right"]["strips"][1]),
            FadeOut(grey_l), FadeOut(grey_r),
            run_time=self.beat(0.11),
        )
        self.play(GrowArrow(arr_l), GrowArrow(arr_r), run_time=self.beat(0.09))
        self.finish()


class S08CellExamples(SpokenScene):
    def construct(self):
        cell_box = RoundedRectangle(corner_radius=0.22, width=12.4, height=5.4,
                                    stroke_color=MEMBRANE_COL, stroke_width=3, fill_color=BG, fill_opacity=0.5).move_to([0, -0.1, 0])
        cell_head = T("FAT CELL", size=34, color=TARGET_COL, weight=BOLD).move_to([0, 3.05, 0])
        mem = make_cell_membrane(y=2.25, x0=-5.9, x1=5.9, thickness=0.20)
        camps = VGroup(*[make_camp_token(0.14).move_to([-5.3 + (i % 2) * 0.45, 1.15 - (i // 2) * 0.48, 0]) for i in range(4)])
        camp_lab = T("cAMP", size=24, color=CAMP_COL, weight=BOLD).move_to([-5.08, 0.05, 0])
        pka = make_c_block(w=1.65, h=1.85, groove_facing=RIGHT, groove_w=0.55, groove_h=0.78, label="PKA", label_size=28).move_to([-3.65, 0.45, 0])
        relay_tag = T("shared relay", size=24, color=PKA_COL).move_to([-4.3, -1.35, 0])
        stag = scope_tag("schematic")

        hsl = make_target_strip("round", "hormone-sensitive lipase", TARGET_COL, w=4.55, h=0.66, tip_dir=LEFT, size=24, phosphate="empty").move_to([0.2, 0.90, 0])
        peri = make_target_strip("round", "perilipin", TARGET_COL, w=4.55, h=0.66, tip_dir=LEFT, size=24, phosphate="empty").move_to([0.2, -0.70, 0])
        droplet = Circle(radius=0.80, color=CAMP_COL, stroke_width=3.5, fill_color=CAMP_COL, fill_opacity=0.22).move_to([4.25, 0.35, 0])
        drop_lab = T("fat droplet", size=24, color=CAMP_COL, weight=BOLD).move_to([4.25, -1.45, 0])

        self.add(cell_box, cell_head, mem, camps, camp_lab, pka, relay_tag, hsl, peri, droplet, drop_lab, stag)
        self.play(hsl.animate.shift(LEFT * 0.25), peri.animate.shift(LEFT * 0.25), run_time=self.beat(0.08))

        self.at("hormone")
        hsl_p = make_phosphate_badge(filled=True, radius=0.23).move_to(hsl.badge)
        peri_p = make_phosphate_badge(filled=True, radius=0.23).move_to(peri.badge)
        self.play(ReplacementTransform(hsl.badge, hsl_p), ReplacementTransform(peri.badge, peri_p), run_time=self.beat(0.11))
        hsl.badge = hsl_p
        peri.badge = peri_p

        self.at("fat breakdown")
        fuel = VGroup(*[
            Circle(radius=0.13, color=CAMP_COL, stroke_width=2, fill_color=CAMP_COL, fill_opacity=0.85).move_to(droplet.get_center())
            for _ in range(5)
        ])
        fuel_dirs = [UL * 0.95, UP * 1.15, UR * 0.95, RIGHT * 1.15, LEFT * 1.05]
        self.add(fuel)
        self.play(
            droplet.animate.scale(0.68),
            *[f.animate.shift(d) for f, d in zip(fuel, fuel_dirs)],
            run_time=self.beat(0.11),
        )

        # Morph to HEART CELL
        self.at("in heart")
        heart_head = T("HEART CELL", size=34, color=TARGET_COL, weight=BOLD).move_to([0, 3.05, 0])
        t_ca = make_target_strip("round", "L-type Ca²⁺ channel / Rad", TARGET_COL, w=4.35, h=0.60, tip_dir=LEFT, size=24, phosphate="full").move_to([-0.55, 1.35, 0])
        t_plb = make_target_strip("round", "phospholamban", TARGET_COL, w=4.35, h=0.60, tip_dir=LEFT, size=24, phosphate="full").move_to([-0.55, 0.00, 0])
        t_tni = make_target_strip("round", "troponin I", TARGET_COL, w=4.35, h=0.60, tip_dir=LEFT, size=24, phosphate="full").move_to([-0.55, -1.35, 0])

        o_ca = T("calcium entry", size=24, color=TEXT).move_to([2.65, 1.35, 0], aligned_edge=LEFT)
        o_plb = T("calcium cycling", size=24, color=TEXT).move_to([2.65, 0.00, 0], aligned_edge=LEFT)
        o_tni = T("contraction\n+ relaxation", size=24, color=TEXT, line_spacing=0.85).move_to([2.65, -1.35, 0], aligned_edge=LEFT)
        a_ca = Arrow(t_ca.get_right() + RIGHT * 0.08, o_ca.get_left() + LEFT * 0.08, color=TARGET_COL, stroke_width=3.5, buff=0.05)
        a_plb = Arrow(t_plb.get_right() + RIGHT * 0.08, o_plb.get_left() + LEFT * 0.08, color=TARGET_COL, stroke_width=3.5, buff=0.05)
        a_tni = Arrow(t_tni.get_right() + RIGHT * 0.08, o_tni.get_left() + LEFT * 0.08, color=TARGET_COL, stroke_width=3.5, buff=0.05)

        bar_h = ValueTracker(0.55)
        bar_bg = RoundedRectangle(corner_radius=0.08, width=0.52, height=2.2, stroke_color=GREY, stroke_width=2).move_to([5.65, 0.25, 0])
        bar_fill = always_redraw(lambda: Rectangle(
            width=0.40, height=bar_h.get_value(), stroke_width=0, fill_color=TARGET_COL, fill_opacity=0.85,
        ).align_to(bar_bg.get_bottom() + UP * 0.06, DOWN).set_x(bar_bg.get_x()))
        bar_lab = T("beat", size=24, color=TARGET_COL).next_to(bar_bg, DOWN, buff=0.18)

        self.play(
            FadeOut(hsl), FadeOut(peri), FadeOut(droplet), FadeOut(drop_lab), FadeOut(fuel),
            swap(cell_head, heart_head, run_time=self.beat(0.04)),
            FadeIn(t_ca), FadeIn(t_plb), FadeIn(t_tni), FadeIn(bar_bg), FadeIn(bar_fill), FadeIn(bar_lab),
            run_time=self.beat(0.06),
        )

        self.at("entry")
        self.play(GrowArrow(a_ca), FadeIn(o_ca), run_time=self.beat(0.04))
        self.at("cycling")
        self.play(GrowArrow(a_plb), FadeIn(o_plb), run_time=self.beat(0.04))
        self.at("contraction")
        self.play(GrowArrow(a_tni), FadeIn(o_tni), bar_h.animate.set_value(2.0), run_time=self.beat(0.05))
        self.at("relaxation")
        self.play(bar_h.animate.set_value(0.50), run_time=self.beat(0.07))

        # Morph to LIVER CELL
        self.at("liver")
        liver_head = T("LIVER CELL", size=34, color=TARGET_COL, weight=BOLD).move_to([0, 3.05, 0])
        t_gly = make_target_strip("round", "glycogen-control enzymes", TARGET_COL, w=4.55, h=0.80, tip_dir=LEFT, size=26, phosphate="empty").move_to([1.15, 0.45, 0])
        self.play(
            FadeOut(t_ca), FadeOut(t_plb), FadeOut(t_tni),
            FadeOut(a_ca), FadeOut(a_plb), FadeOut(a_tni),
            FadeOut(o_ca), FadeOut(o_plb), FadeOut(o_tni),
            FadeOut(bar_bg), FadeOut(bar_fill), FadeOut(bar_lab),
            swap(heart_head, liver_head, run_time=self.beat(0.04)),
            FadeIn(t_gly),
            run_time=self.beat(0.06),
        )
        self.play(t_gly.animate.move_to([0.7, 0.45, 0]), run_time=self.beat(0.08))

        self.at("glycogen")
        gly_p = make_phosphate_badge(filled=True, radius=0.23).move_to(t_gly.badge)
        self.play(ReplacementTransform(t_gly.badge, gly_p), run_time=self.beat(0.08))
        t_gly.badge = gly_p

        self.at("relay is shared")
        shared_box = SurroundingRectangle(VGroup(camps, pka, relay_tag), color=PKA_COL, buff=0.22, corner_radius=0.14)
        diff_lab = T("target set differs", size=28, color=TARGET_COL, weight=BOLD).move_to([0.7, -1.1, 0])
        self.play(Create(shared_box), FadeIn(diff_lab), run_time=self.beat(0.11))
        self.finish()


class S09Addresses(SpokenScene):
    def construct(self):
        cell_box = RoundedRectangle(corner_radius=0.22, width=12.6, height=5.8,
                                    stroke_color=MEMBRANE_COL, stroke_width=3, fill_color=BG, fill_opacity=0.45).move_to([0, -0.1, 0])
        mem = make_cell_membrane(y=2.3, x0=-6.1, x1=6.1, thickness=0.24)
        head = T("within one cell", size=32, color=TEXT, weight=BOLD).move_to([0, 3.15, 0])
        stag = scope_tag("schematic")

        self.add(cell_box, mem, stag)
        self.play(Create(cell_box), FadeIn(head, shift=DOWN * 0.1), run_time=self.beat(0.14))

        cx = -3.2
        akap = RoundedRectangle(corner_radius=0.14, width=3.9, height=0.72,
                                stroke_color=AKAP_COL, stroke_width=3.5, fill_color=AKAP_COL, fill_opacity=0.12).move_to([cx, -0.75, 0])
        akap_lab = T("anchoring protein", size=26, color=AKAP_COL, weight=BOLD).move_to(akap)

        self.at("anchoring protein")
        self.play(FadeIn(akap), FadeIn(akap_lab), run_time=self.beat(0.08))

        pka = make_c_block(w=1.45, h=1.45, groove_facing=RIGHT, groove_w=0.45, groove_h=0.62, label="PKA", label_size=24).move_to([cx - 1.0, 0.38, 0])
        sub = make_target_strip("round", "substrate", TARGET_COL, w=1.78, h=0.62, tip_dir=LEFT, size=24, phosphate="empty").move_to([cx + 0.95, 0.38, 0])
        other_sub = make_target_strip("round", "other target", GREY, w=2.1, h=0.58, tip_dir=LEFT, size=24).move_to([2.8, 0.38, 0])

        self.play(FadeIn(pka), run_time=self.beat(0.06))
        self.at("beside a selected")
        self.play(FadeIn(sub), run_time=self.beat(0.08))

        self.at("address narrows")
        self.play(FadeIn(other_sub), sub.animate.shift(LEFT * 0.25), run_time=self.beat(0.08))
        sub_p = make_phosphate_badge(filled=True, radius=0.23).move_to(sub.badge)
        self.play(ReplacementTransform(sub.badge, sub_p), run_time=self.beat(0.07))
        sub.badge = sub_p

        cyclase = boxed_label("cyclase", SYNTH_COL, size=26, box=(1.7, 0.56)).move_to([cx, 1.80, 0])
        pde = boxed_label("PDE", BREAK_COL, size=26, box=(1.3, 0.56)).move_to([cx, -1.80, 0])

        self.at("nearby cyclase")
        rng = np.random.default_rng(7)
        local_camps = VGroup(*[
            make_camp_token(0.10).move_to([cx + rng.uniform(-0.35, 0.95), rng.uniform(1.12, 1.44), 0])
            for _ in range(7)
        ])
        self.play(FadeIn(cyclase), *[FadeIn(t, shift=DOWN * 0.25) for t in local_camps], run_time=self.beat(0.09))

        self.at("phosphodiesterase")
        self.play(FadeIn(pde), run_time=self.beat(0.05))
        self.at("removes it")
        fading_camps = local_camps[:3]
        staying_camps = local_camps[3:]
        self.play(
            *[t.animate.move_to(pde.get_top() + UP * 0.12).set_opacity(0.0) for t in fading_camps],
            *[t.animate.shift(DOWN * 0.14) for t in staying_camps],
            FadeOut(other_sub),
            run_time=self.beat(0.07),
        )

        assembly = VGroup(akap, akap_lab, pka, sub, cyclase, pde, staying_camps)
        ghost = RoundedRectangle(corner_radius=0.14, width=3.9, height=0.72,
                                 stroke_color=AKAP_COL, stroke_width=2, stroke_opacity=0.35).move_to(akap)
        ghost_lab = T("site 1", size=24, color=GREY).move_to(ghost)
        self.play(
            FadeIn(ghost), FadeIn(ghost_lab),
            assembly.animate.shift(RIGHT * 6.4),
            run_time=self.beat(0.11),
        )
        self.finish()


class S10Compartments(SpokenScene):
    def construct(self):
        cell_box = RoundedRectangle(corner_radius=0.22, width=12.6, height=5.15,
                                    stroke_color=MEMBRANE_COL, stroke_width=3, fill_color=BG, fill_opacity=0.45).move_to([0, -0.35, 0])
        mem = make_cell_membrane(y=1.95, x0=-6.1, x1=6.1, thickness=0.22)
        obs_badge = boxed_label("local responses observed", CAMP_COL, size=26, fill_opacity=0.20).move_to([-3.2, 3.12, 0])
        cand_head = T("candidate contributors ?", size=28, color=TEXT, weight=BOLD).move_to([3.3, 3.12, 0])
        stag = scope_tag("schematic")

        src_pos = np.array([-2.9, 1.45, 0.0])
        sink_pos = np.array([-0.8, -1.65, 0.0])
        bind_pos = np.array([-4.4, -0.45, 0.0])
        obs_centers = [np.array([-2.2, 0.15, 0.0]), np.array([-3.3, -1.15, 0.0]), np.array([-1.4, -0.55, 0.0])]

        rng = np.random.default_rng(11)
        n_part = 22
        pos = np.zeros((n_part, 2))
        vel = np.zeros((n_part, 2))
        bound_timer = np.zeros(n_part)
        for i in range(n_part):
            ang = rng.uniform(-0.85 * PI, -0.15 * PI)
            r = rng.uniform(0.3, 1.6)
            pos[i] = src_pos[:2] + np.array([r * np.cos(ang), r * np.sin(ang)])
            vel[i] = rng.uniform(-0.45, 0.45, size=2)

        dots = VGroup(*[Circle(radius=0.085, color=CAMP_COL, stroke_width=0, fill_color=CAMP_COL, fill_opacity=0.88).move_to([p[0], p[1], 0]) for p in pos])
        flags = {"sink": False, "bind": False, "obs": False}

        def step_particles(mob, dt):
            dt = min(dt, 0.05)
            for i, d in enumerate(mob):
                if flags["bind"] and bound_timer[i] > 0:
                    bound_timer[i] -= dt
                    d.set_fill(opacity=0.95)
                    continue
                vel[i] += rng.normal(0, 0.6 * dt, size=2)
                speed = np.linalg.norm(vel[i])
                if speed > 0.72:
                    vel[i] = vel[i] / speed * 0.72
                nxt = pos[i] + vel[i] * dt
                if flags["obs"]:
                    for oc in obs_centers:
                        diff = nxt - oc[:2]
                        dist = np.linalg.norm(diff)
                        if dist < 0.46 and dist > 1e-4:
                            nvec = diff / dist
                            nxt = oc[:2] + nvec * 0.47
                            vel[i] -= 1.6 * np.dot(vel[i], nvec) * nvec
                if flags["bind"]:
                    bdiff = nxt - bind_pos[:2]
                    bdist = np.linalg.norm(bdiff)
                    if bdist < 0.78 and bdist > 1e-4:
                        nvec = bdiff / bdist
                        nxt = bind_pos[:2] + nvec * 0.79
                        if rng.random() < 0.12:
                            bound_timer[i] = 0.65
                        else:
                            vel[i] -= 1.5 * np.dot(vel[i], nvec) * nvec
                if nxt[0] < -5.8 or nxt[0] > 0.35:
                    vel[i][0] *= -1
                    nxt[0] = np.clip(nxt[0], -5.8, 0.35)
                if nxt[1] < -2.45 or nxt[1] > 1.72:
                    vel[i][1] *= -1
                    nxt[1] = np.clip(nxt[1], -2.45, 1.72)
                pos[i] = nxt
                if flags["sink"] and np.linalg.norm(pos[i] - sink_pos[:2]) < 0.62:
                    ang = rng.uniform(-0.8 * PI, -0.2 * PI)
                    pos[i] = src_pos[:2] + np.array([0.22 * np.cos(ang), 0.22 * np.sin(ang)])
                dist_src = np.linalg.norm(pos[i] - src_pos[:2])
                op = float(np.clip(1.0 - 0.16 * dist_src, 0.30, 0.95))
                d.move_to([pos[i][0], pos[i][1], 0]).set_fill(opacity=op)

        dots.add_updater(step_particles)

        rec_pka = make_c_block(w=1.48, h=1.38, groove_facing=RIGHT, groove_w=0.42, groove_h=0.58, label="PKA", label_size=24).move_to([-4.95, 0.95, 0])

        self.add(cell_box, mem, stag, dots)
        self.at("local cyclic")
        self.play(FadeIn(obs_badge), run_time=self.beat(0.06))
        self.at("receptor")
        self.play(FadeIn(rec_pka), run_time=self.beat(0.10))

        c1 = boxed_label("local production ?", SYNTH_COL, size=26, box=(4.2, 0.68)).move_to([3.3, 1.15, 0])
        c2 = boxed_label("local removal ?", BREAK_COL, size=26, box=(4.2, 0.68)).move_to([3.3, 0.20, 0])
        c3 = boxed_label("binding ?", REG_COL, size=26, box=(4.2, 0.68)).move_to([3.3, -0.75, 0])
        c4 = boxed_label("restricted movement ?", GREY, size=26, box=(4.2, 0.68)).move_to([3.3, -1.70, 0])

        src_chip = boxed_label("source ?", SYNTH_COL, size=24, box=(1.55, 0.52), fill_opacity=0.92).move_to(src_pos)
        src_chip[0].set_fill(BG, opacity=0.92)
        sink_chip = boxed_label("sink ?", BREAK_COL, size=24, box=(1.35, 0.52), fill_opacity=0.92).move_to(sink_pos)
        sink_chip[0].set_fill(BG, opacity=0.92)
        bind_chip = boxed_label("bind ?", REG_COL, size=24, box=(1.35, 0.52), fill_opacity=0.95).move_to(bind_pos)
        bind_chip[0].set_fill(BG, opacity=0.95)
        bind_chip.set_z_index(5)
        obs_shapes = VGroup(*[
            RoundedRectangle(corner_radius=0.14, width=0.66, height=0.46, stroke_color=GREY, stroke_width=2.5,
                             fill_color=GREY, fill_opacity=0.35).move_to(oc)
            for oc in obs_centers
        ])

        self.at("local production")
        self.play(FadeIn(cand_head), FadeIn(src_chip), FadeIn(c1), run_time=self.beat(0.06))

        self.at("local removal")
        flags["sink"] = True
        self.play(FadeIn(sink_chip), FadeIn(c2), run_time=self.beat(0.05))

        self.at("binding")
        flags["bind"] = True
        self.play(FadeIn(bind_chip), FadeIn(c3), run_time=self.beat(0.05))

        self.at("restricted movement")
        flags["obs"] = True
        self.play(FadeIn(obs_shapes), FadeIn(c4), run_time=self.beat(0.05))

        self.at("varies")
        for box in (c1, c2, c3, c4):
            self.play(Indicate(box, color=CAMP_COL, scale_factor=1.05), run_time=self.beat(0.06))

        self.at("observed")
        self.play(Indicate(obs_badge, color=CAMP_COL, scale_factor=1.06), run_time=self.beat(0.07))
        self.finish()


class S11Handoff(SpokenScene):
    def construct(self):
        bg_sites = VGroup(
            RoundedRectangle(corner_radius=0.14, width=2.8, height=0.50, stroke_color=GREY, stroke_width=2).move_to([-4.0, 2.55, 0]),
            RoundedRectangle(corner_radius=0.14, width=2.8, height=0.50, stroke_color=GREY, stroke_width=2).move_to([4.0, 2.55, 0]),
        ).set_opacity(0.28)
        bg_sites.layout_ok = True

        c_open = make_c_block(w=3.0, h=3.6, groove_facing=LEFT, groove_w=1.05, groove_h=1.4, label="PKA", label_size=32).move_to([1.6, 0.1, 0])
        sub_wait = make_target_strip("round", "target", TARGET_COL, w=2.4, h=0.72, tip_dir=RIGHT, size=26, phosphate="empty").move_to([-2.4, 0.55, 0])
        comp_wait = make_target_strip("round", "competitor", GREY, w=2.4, h=0.72, tip_dir=RIGHT, size=26).move_to([-2.4, -0.65, 0])

        res_box = RoundedRectangle(corner_radius=0.14, width=2.4, height=1.1, stroke_color=CAMP_COL, stroke_width=2.5).move_to([4.85, 0.1, 0])
        res_lab = T("result: ?", size=28, color=CAMP_COL, weight=BOLD).move_to(res_box)
        stag = scope_tag("schematic")

        self.add(bg_sites, c_open, stag)
        self.at("opens the catalytic")
        self.play(c_open.animate.scale(1.06), run_time=self.beat(0.11))
        self.at("access gives")
        self.play(FadeIn(sub_wait, shift=RIGHT * 0.25), run_time=self.beat(0.10))
        self.play(sub_wait.animate.shift(RIGHT * 0.40), run_time=self.beat(0.11))

        self.at("tests that groove")
        head_comp = T("groove competition", size=32, color=TEXT, weight=BOLD).move_to([0, 3.15, 0])
        self.play(FadeIn(head_comp), FadeIn(comp_wait, shift=RIGHT * 0.25), FadeIn(res_box), FadeIn(res_lab), run_time=self.beat(0.09))
        self.play(sub_wait.animate.shift(RIGHT * 0.45), comp_wait.animate.shift(RIGHT * 0.45), run_time=self.beat(0.12))

        self.at("evidence for local")
        cell_box = RoundedRectangle(corner_radius=0.22, width=12.4, height=5.0,
                                    stroke_color=MEMBRANE_COL, stroke_width=3, fill_color=BG, fill_opacity=0.45).move_to([0, -0.35, 0])
        mem = make_cell_membrane(y=1.80, x0=-5.9, x1=5.9, thickness=0.20)
        rng = np.random.default_rng(19)
        cloud_l = VGroup(*[make_camp_token(0.11).move_to([-3.5 + rng.uniform(-1.05, 1.05), rng.uniform(-0.15, 1.35), 0]) for _ in range(10)])
        cloud_r = VGroup(*[make_camp_token(0.11).move_to([3.5 + rng.uniform(-1.05, 1.05), rng.uniform(-0.15, 1.35), 0]) for _ in range(10)])
        obs_lab = boxed_label("established: local cAMP", CAMP_COL, size=26, fill_opacity=0.20).move_to([-3.1, 3.05, 0])
        prop_lab = boxed_label("proposed: 4 candidates ?", GREY, size=26, fill_opacity=0.16).move_to([3.1, 3.05, 0])

        q_badges = VGroup(
            boxed_label("source ?", SYNTH_COL, size=24, box=(2.0, 0.58)),
            boxed_label("sink ?", BREAK_COL, size=24, box=(2.0, 0.58)),
            boxed_label("binding ?", REG_COL, size=24, box=(2.0, 0.58)),
            boxed_label("obstacles ?", GREY, size=24, box=(2.0, 0.58)),
        ).arrange(RIGHT, buff=0.35).move_to([0, -1.75, 0])

        self.play(
            FadeOut(bg_sites), FadeOut(c_open), FadeOut(sub_wait), FadeOut(comp_wait),
            FadeOut(res_box), FadeOut(res_lab), FadeOut(head_comp),
            FadeIn(cell_box), FadeIn(mem), FadeIn(cloud_l), FadeIn(cloud_r),
            run_time=self.beat(0.08),
        )

        def drift_clouds(mob, dt):
            dt = min(dt, 0.05)
            for dot in mob:
                dot.shift([rng.normal(0, 0.35 * dt), rng.normal(0, 0.35 * dt), 0])

        cloud_l.add_updater(drift_clouds)
        cloud_r.add_updater(drift_clouds)

        self.at("separate")
        self.play(FadeIn(obs_lab), FadeIn(prop_lab), FadeIn(q_badges), run_time=self.beat(0.08))
        self.finish()


class S12End(EndCard):
    LINE = "PKA responses depend on which targets are nearby."
