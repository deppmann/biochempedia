"""
COLOUR MAP (one colour per concept for the entire film):
- BLUE (#58C4DD): fatty-acid chain tiles (16-tile chain, 3-tile odd-chain tail) and fat droplet
- ORANGE (#FF862F): coenzyme A (CoA) handles and CoA-handle slot
- YELLOW (#F5D547): attention cues and the carnitine gate
- PINK (#D147BD): electron carriers (FADH2, NADH / NAD+)
- GREEN (#83C167): acetyl-CoA carts (2 blocks each), citric acid cycle ring, ATP earned, "can use" glow
- RED (#FC6255): activation cost (-2 ATP), blood-lane rails, red blood cell disc, "cannot use"
- PURPLE (#9A72AC): beta-oxidation workshop wheel
- GREY (#8B93A1): membranes, liver outline, human silhouette, CO2 puffs, glycerol, protein chips, schematic tag
- GOLD (#D4A843): 106 ATP total gauge, title rule, question card
- TEAL (#3FB8C0): ketone bodies (acetoacetate / D-3-hydroxybutyrate capsules) ONLY
- WHITE / TEXT (#FFFFFF / #E8EAF0): glucose hexagon tokens, brain outline, primary labels

CARRIED WORLD:
One continuous body-to-liver world:
- Full view: faint generic human silhouette behind; liver cell at LEFT (x -5.15..-1.35) housing spinning PURPLE
  workshop wheel + GREEN citric acid cycle ring; RED blood-lane rails across middle branching RIGHT to brain
  (top), heart/muscle/kidney (middle), and red blood cell (bottom); day counter top-centre; schematic tag bottom-right.
- Zoomed liver view (s03-s06): liver boundary fills ~70% of frame with left/right blood-lane stubs, PURPLE wheel,
  GREEN citric acid cycle ring, surplus queue, and repackaging press.

WHAT CHANGES PER SPOKEN SCENE (and what it is computed from):
- s00_link_and_question: 16-tile BLUE chain feeds PURPLE wheel -> 8 GREEN acetyl-CoA carts roll out as GOLD ATP gauge
  computes 0..106 ATP; pulls back to liver/blood-lane/brain world; day counter + fast progress bar race 1..382 and brain flickers.
- s02_the_fast: day counter resets 1..382 while BLUE fat droplet area scales proportionally to weight (456 -> 180 lb,
  r = r0 * sqrt(w/456)) beside live readout; WHITE glucose hexagons flow along blood lane then thin to a trickle + '?'.
- s03_no_net_glucose: zoomed liver; GREEN acetyl-CoA cart delivers 2 BLUE carbons into turning GREEN citric acid cycle ring,
  carbon wedge orbits ring, 2 GREY CO2 puffs leave, computed balance tally updates in:2 -> out:2 -> net:0 while 'to glucose' hex stays hollow.
- s04_exceptions: GREY glycerol token and BLUE 3-tile odd-chain tail each enter and yield 1 WHITE glucose hexagon out;
  even-chain exit dims as YELLOW cue circles growing pile of GREEN acetyl-CoA carts.
- s05_flood: insulin gauge ValueTracker drops to low, BLUE chains flood through opening YELLOW carnitine gate, PURPLE wheel
  spins faster (omega 1.1->2.8) making carts faster (2.2/s) than ring consumes (0.6/s), stacking 'surplus' queue.
- s06_repackage: 2 GREEN carts enter press, ORANGE CoA handles return to wheel, 2 GREEN blocks fuse into TEAL acetoacetate
  capsule; PINK NADH docks -> NAD+ leaves as capsule relabels D-3-hydroxybutyrate and lines up at exit.
- s07_idea: pulls back to full world; hollow liver hex flashes & fades; stream of TEAL capsules (2 GREEN blocks each)
  ships along blood lane toward all three right-side tissue icons.
- s08_ledger: GOLD 106 ATP bar splits strictly to scale (26/106 = 24.5% GREEN at liver; 80/106 = 75.5% upper segment rides
  blood lane with 4 TEAL capsules = 8 GREEN blocks) while PINK carriers stay at liver.
- s09_predict: right tissues dim; 3 TEAL capsules peel back to hover/bob at rim of liver's GREEN ring; question card rises.
- s11_answer: question dissolves to 'No'; empty ORANGE CoA slot ('no thiophorase') bounces capsules into blood lane, red blood
  cell bounces capsules ('no mitochondria'), muscle clips ORANGE handle and splits capsule to 2 GREEN blocks + glows GREEN,
  brain adapts slower and glows GREEN.
- s12_cahill: day counter runs 1..40 while computed decay bar/readout 'protein broken down (g/day)' falls 75 -> 20, muscle
  protein chip trickle slows proportionally, and brain shifts from WHITE hexagons to TEAL capsules.
- s13_return: pulls back to silhouette world; day counter runs 1..382 as BLUE droplet area & weight roll 456 -> 180 lb;
  broad TEAL capsule stream + thin WHITE gluconeogenesis hexagon trickle both feed brain.
- s14_close: hollow WHITE liver hex flashes and vanishes; empty ORANGE CoA slot glows; TEAL blood stream brightens and
  brain + heart/muscle/kidney glow GREEN together while red blood cell stays dim.
"""

from bp_parts import *

# ------------------------------------------------------------------ shared geometry & helpers
LIVER_CENTER = np.array([-3.25, -0.10, 0.0])
LIVER_W = 3.80
LIVER_H = 4.60
WHEEL_POS = np.array([-4.25, 0.25, 0.0])
RING_POS = np.array([-2.25, 0.25, 0.0])

TISSUE_X = 3.75
BRAIN_POS = np.array([TISSUE_X, 1.85, 0.0])
MUSCLE_POS = np.array([TISSUE_X, 0.10, 0.0])
RBC_POS = np.array([TISSUE_X, -1.75, 0.0])

LANE_X0 = -1.35
LANE_XJ = 1.50
LANE_Y = -0.15


def make_wheel(radius=0.68, color=PURPLE, omega=1.5, spokes=6):
    """Spinning beta-oxidation workshop wheel with bold spokes and rotating rim pocket."""
    outer = Circle(radius=radius, color=color, stroke_width=4.8, fill_color=color, fill_opacity=0.22)
    inner = Circle(radius=radius * 0.26, color=color, stroke_width=3.5, fill_color=BG, fill_opacity=1.0)
    sp = VGroup(*[
        Line(
            [radius * 0.26 * np.cos(a), radius * 0.26 * np.sin(a), 0],
            [radius * 0.96 * np.cos(a), radius * 0.96 * np.sin(a), 0],
            color=color, stroke_width=4.0,
        )
        for a in np.linspace(0, TAU, spokes, endpoint=False)
    ])
    wedge = AnnularSector(inner_radius=radius * 0.35, outer_radius=radius * 0.92, angle=TAU / spokes,
                          start_angle=0.0, color=color, fill_opacity=0.45, stroke_width=0)
    marker = Dot([radius * 0.82, 0, 0], radius=0.10, color=YELLOW)
    g = VGroup(outer, wedge, sp, inner, marker)
    g._omega = omega
    g.add_updater(lambda m, dt: m.rotate(-m._omega * dt))
    return g


def make_cac_ring(radius=0.62, color=GREEN, omega=1.2):
    """Spinning citric acid cycle ring with directional beads and glowing active arc."""
    ring = Circle(radius=radius, color=color, stroke_width=5.2, fill_color=color, fill_opacity=0.15)
    arc = Arc(radius=radius, start_angle=0.0, angle=1.35, stroke_color=YELLOW, stroke_width=6.5)
    beads = VGroup(*[
        Dot([radius * np.cos(a), radius * np.sin(a), 0], radius=0.09, color=color)
        for a in np.linspace(0, TAU, 4, endpoint=False)
    ])
    g = VGroup(ring, arc, beads)
    g._omega = omega
    g.add_updater(lambda m, dt: m.rotate(-m._omega * dt))
    return g


def make_acetyl_cart(scale=1.0):
    """Two GREEN carbon blocks clamped to one ORANGE CoA handle."""
    b1 = RoundedRectangle(corner_radius=0.05, width=0.22, height=0.22, color=GREEN, stroke_width=2, fill_color=GREEN, fill_opacity=0.88)
    b2 = b1.copy().next_to(b1, RIGHT, buff=0.04)
    blocks = VGroup(b1, b2)
    coa = RoundedRectangle(corner_radius=0.07, width=0.18, height=0.28, color=ORANGE, stroke_width=2, fill_color=ORANGE, fill_opacity=0.88)
    coa.next_to(blocks, LEFT, buff=0.04)
    g = VGroup(coa, blocks)
    g.coa = coa
    g.blocks = blocks
    return g.scale(scale)


def make_ketone_capsule(scale=1.0):
    """TEAL capsule enclosing two GREEN 2-carbon blocks (acetoacetate / D-3-hydroxybutyrate)."""
    b1 = RoundedRectangle(corner_radius=0.04, width=0.18, height=0.18, color=GREEN, stroke_width=1.5, fill_color=GREEN, fill_opacity=0.92)
    b2 = b1.copy().next_to(b1, RIGHT, buff=0.05)
    blocks = VGroup(b1, b2)
    shell = RoundedRectangle(corner_radius=0.18, width=0.62, height=0.34, color=TEAL, stroke_width=3.2, fill_color=TEAL, fill_opacity=0.28)
    blocks.move_to(shell)
    g = VGroup(shell, blocks)
    g.shell = shell
    g.blocks = blocks
    return g.scale(scale)


def make_glucose_hex(radius=0.15, hollow=False):
    """WHITE hexagon token representing glucose."""
    return RegularPolygon(6, radius=radius, color=WHITE, stroke_width=3.0, fill_color=WHITE, fill_opacity=0.0 if hollow else 0.90)


def make_fat_chain(n_tiles=16, tile_w=0.16, gap=0.03):
    """BLUE fatty-acid chain made of n_tiles squares."""
    return VGroup(*[
        RoundedRectangle(corner_radius=0.03, width=tile_w, height=tile_w, color=BLUE, stroke_width=1.8, fill_color=BLUE, fill_opacity=0.88)
        for _ in range(n_tiles)
    ]).arrange(RIGHT, buff=gap)


def make_silhouette():
    """Faint generic human torso + head outline behind full-world scenes (kept low opacity)."""
    head = Circle(radius=0.52, color=GREY, stroke_width=1.8, stroke_opacity=0.20, fill_color=GREY, fill_opacity=0.07).move_to([0.2, 2.55, 0])
    torso = RoundedRectangle(corner_radius=0.75, width=3.1, height=4.5, color=GREY, stroke_width=1.8, stroke_opacity=0.20, fill_color=GREY, fill_opacity=0.07).move_to([0.2, -0.35, 0])
    return VGroup(torso, head)


def make_brain_icon(scale=1.0, color=TEXT):
    """Schematic brain outline (two rounded lobes + sulcus indent)."""
    pts = [
        [-0.85, -0.25, 0], [-0.95, 0.20, 0], [-0.55, 0.55, 0], [-0.05, 0.58, 0],
        [0.02, 0.42, 0], [0.10, 0.58, 0], [0.62, 0.52, 0], [0.95, 0.15, 0],
        [0.85, -0.30, 0], [0.35, -0.45, 0], [0.0, -0.35, 0], [-0.45, -0.45, 0],
    ]
    outline = Polygon(*pts, color=color, stroke_width=3.8, fill_color=color, fill_opacity=0.18).round_corners(0.28)
    fold = ArcBetweenPoints([-0.35, 0.05, 0], [0.35, 0.02, 0], angle=-0.5).set_stroke(color, 2.4)
    g = VGroup(outline, fold).scale(scale)
    g.outline = outline
    return g


def make_muscle_icon(scale=1.0, color=TEXT):
    """Schematic combined heart, muscle, kidney tissue badge."""
    body = RoundedRectangle(corner_radius=0.38, width=1.65, height=0.88, color=color, stroke_width=3.5, fill_color=color, fill_opacity=0.18)
    fibers = VGroup(*[
        Line([-0.55, y, 0], [0.55, y, 0], color=color, stroke_width=2.2)
        for y in (-0.18, 0.0, 0.18)
    ])
    g = VGroup(body, fibers).scale(scale)
    g.outline = body
    return g


def make_rbc_icon(scale=1.0):
    """RED biconcave disc icon for red blood cell."""
    outer = Ellipse(width=1.15, height=0.72, color=RED, stroke_width=3.5, fill_color=RED, fill_opacity=0.32)
    inner = Ellipse(width=0.52, height=0.28, color=RED, stroke_width=2.2, fill_color=BG, fill_opacity=0.90)
    g = VGroup(outer, inner).scale(scale)
    g.outline = outer
    return g


def make_blood_rails(branches=3):
    """Two parallel RED blood-lane rails from liver exit to 1 (brain) or 3 (brain/muscle/rbc) targets."""
    rails = VGroup()
    dy = 0.22
    if branches == 1:
        p0 = np.array([LANE_X0, LANE_Y, 0.0])
        p1 = np.array([0.8, LANE_Y, 0.0])
        p2 = np.array([TISSUE_X - 1.05, BRAIN_POS[1], 0.0])
        for off in (dy, -dy):
            top_path = VMobject(color=RED, stroke_width=2.8)
            top_path.set_points_smoothly([p0 + UP * off, p1 + UP * off, [1.85, 0.85 + off * 0.6, 0], p2 + UP * off * 0.7])
            rails.add(top_path)
    else:
        for off in (dy, -dy):
            rails.add(Line([LANE_X0, LANE_Y + off, 0], [LANE_XJ, LANE_Y + off, 0], color=RED, stroke_width=2.8))
        for ty in (BRAIN_POS[1], MUSCLE_POS[1], RBC_POS[1]):
            for off in (0.14, -0.14):
                p = VMobject(color=RED, stroke_width=2.4)
                p.set_points_smoothly([[LANE_XJ, LANE_Y + off, 0], [2.15, 0.55 * ty + 0.45 * LANE_Y + off, 0], [TISSUE_X - 0.95, ty + off, 0]])
                rails.add(p)
    return rails


def make_day_counter(tracker, at=(0.45, 2.75, 0), max_days=382.0, bar=True):
    """Top-centre live counter labelled 'days without food' with optional computed progress bar."""
    lab = T("days without food", 26, TEXT).move_to(at)
    num = always_redraw(lambda: M(f"{int(round(tracker.get_value())):3d}", 34, GOLD).next_to(lab, DOWN, buff=0.12))
    g = VGroup(lab, num)
    if bar:
        bw = 2.4
        bg = RoundedRectangle(corner_radius=0.05, width=bw, height=0.18, color=GREY, stroke_width=1.8, fill_opacity=0.18).next_to(lab, DOWN, buff=0.56)
        fill = always_redraw(lambda: RoundedRectangle(
            corner_radius=0.04, width=max(0.06, bw * min(1.0, tracker.get_value() / max_days)),
            height=0.13, color=GOLD, stroke_width=0, fill_color=GOLD, fill_opacity=0.90,
        ).align_to(bg.get_left() + RIGHT * 0.02, LEFT).set_y(bg.get_y()))
        g.add(bg, fill)
    return g


def make_full_world(branches=3, show_tissues=True, wheel_omega=1.5, ring_omega=1.2):
    """Build the carried full-body world at identical coordinates across scenes."""
    sil = make_silhouette()
    liver_box = RoundedRectangle(corner_radius=0.35, width=LIVER_W, height=LIVER_H, color=GREY, stroke_width=3.8, fill_color=GREY, fill_opacity=0.16).move_to(LIVER_CENTER)
    liver_lab = T("liver", 30, TEXT).next_to(liver_box, UP, buff=0.18)
    wheel = make_wheel(radius=0.64, omega=wheel_omega).move_to(WHEEL_POS)
    ring = make_cac_ring(radius=0.60, omega=ring_omega).move_to(RING_POS)
    rails = make_blood_rails(branches=branches)
    g = VGroup(sil, liver_box, liver_lab, wheel, ring, rails)
    g.sil = sil
    g.liver_box = liver_box
    g.liver_lab = liver_lab
    g.wheel = wheel
    g.ring = ring
    g.rails = rails
    if show_tissues:
        brain = make_brain_icon(0.95).move_to(BRAIN_POS)
        brain_lab = T("brain", 28, TEXT).next_to(brain, UP, buff=0.16)
        g.add(brain, brain_lab)
        g.brain = brain
        g.brain_lab = brain_lab
        if branches == 3:
            muscle = make_muscle_icon(0.95).move_to(MUSCLE_POS)
            muscle_lab = T("heart, muscle, kidney", 24, TEXT).next_to(muscle, DOWN, buff=0.18)
            rbc = make_rbc_icon(0.95).move_to(RBC_POS)
            rbc_lab = T("red blood cell", 26, TEXT).next_to(rbc, DOWN, buff=0.16)
            g.add(muscle, muscle_lab, rbc, rbc_lab)
            g.muscle, g.muscle_lab = muscle, muscle_lab
            g.rbc, g.rbc_lab = rbc, rbc_lab
    return g


def make_liver_zoom(wheel_pos=(-3.4, 0.0, 0), ring_pos=(1.45, -0.05, 0), ring_r=1.28, wheel_omega=1.4, ring_omega=1.2):
    """Zoomed liver cell (~70% of frame) carrying the same internal elements."""
    box = RoundedRectangle(corner_radius=0.42, width=10.5, height=5.15, color=GREY, stroke_width=4.0, fill_color=GREY, fill_opacity=0.15).move_to([-0.4, -0.05, 0])
    lab = T("liver", 30, TEXT).move_to([0.0, 2.84, 0])
    left_rails = VGroup(
        Line([-6.4, 0.12, 0], [-5.65, 0.12, 0], color=RED, stroke_width=2.8),
        Line([-6.4, -0.38, 0], [-5.65, -0.38, 0], color=RED, stroke_width=2.8),
    )
    right_rails = VGroup(
        Line([4.85, 0.12, 0], [6.4, 0.12, 0], color=RED, stroke_width=2.8),
        Line([4.85, -0.38, 0], [6.4, -0.38, 0], color=RED, stroke_width=2.8),
    )
    wheel = make_wheel(radius=0.98, omega=wheel_omega).move_to(wheel_pos)
    ring = make_cac_ring(radius=ring_r, omega=ring_omega).move_to(ring_pos)
    g = VGroup(box, lab, left_rails, right_rails, wheel, ring)
    g.box, g.lab = box, lab
    g.left_rails, g.right_rails = left_rails, right_rails
    g.wheel, g.ring = wheel, ring
    return g


def stream_along_path(factory, points, n_items=6, speed=0.35, active_fn=None):
    """Create `n_items` moving smoothly along polyline `points` driven by elapsed time."""
    pts = [np.array(p, dtype=float) for p in points]
    segs = [pts[i + 1] - pts[i] for i in range(len(pts) - 1)]
    lens = [float(np.linalg.norm(s)) for s in segs]
    tot = sum(lens) or 1.0
    cum = np.cumsum([0.0] + lens)

    def pos_at(u):
        u = u % 1.0
        d = u * tot
        for i, L in enumerate(lens):
            if d <= cum[i + 1] or i == len(lens) - 1:
                f = (d - cum[i]) / max(L, 1e-6)
                return pts[i] + f * segs[i]
        return pts[-1]

    group = VGroup()
    t_clock = ValueTracker(0.0)
    group._clock = t_clock
    group.add_updater(lambda m, dt: t_clock.increment_value(dt))
    for k in range(n_items):
        mob = factory(k)
        phase = k / n_items

        def upd(m, ph=phase):
            u = (ph + t_clock.get_value() * speed) % 1.0
            m.move_to(pos_at(u))
            if active_fn is not None:
                m.set_opacity(active_fn(u, t_clock.get_value()))
        mob.add_updater(upd)
        mob.move_to(pos_at(phase))
        group.add(mob)
    return group


# ------------------------------------------------------------------ scenes
class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic"))
        # 0..5.3s: link-back mitochondrial workshop
        ws_box = RoundedRectangle(corner_radius=0.35, width=11.8, height=6.1, color=GREY, stroke_width=3.8, fill_color=GREY, fill_opacity=0.15).move_to([0.0, 0.0, 0])
        ws_wheel = make_wheel(radius=1.15, omega=1.7).move_to([-2.4, 0.1, 0])
        chain = make_fat_chain(16, tile_w=0.18, gap=0.03).move_to([-4.6, 1.85, 0])
        atp_val = ValueTracker(0.0)
        atp_bar_bg = RoundedRectangle(corner_radius=0.08, width=0.58, height=3.1, color=GREY, stroke_width=2.5, fill_opacity=0.15).move_to([4.25, -0.15, 0])
        atp_fill = always_redraw(lambda: RoundedRectangle(
            corner_radius=0.05, width=0.48, height=max(0.06, 3.0 * min(1.0, atp_val.get_value() / 106.0)),
            color=GOLD, stroke_width=0, fill_color=GOLD, fill_opacity=0.90
        ).align_to(atp_bar_bg.get_bottom() + UP * 0.05, DOWN).set_x(atp_bar_bg.get_x()))
        atp_num = always_redraw(lambda: M(f"roughly {int(round(atp_val.get_value()))} ATP", 26, GOLD).next_to(atp_bar_bg, UP, buff=0.22))
        act_tag = T("-2 ATP", 24, RED).next_to(atp_bar_bg, DOWN, buff=0.18)
        ws_grp = VGroup(ws_box, ws_wheel, chain, atp_bar_bg, atp_fill, atp_num, act_tag)
        self.add(ws_grp)

        carts = VGroup(*[make_acetyl_cart(0.85) for _ in range(8)])
        for idx, c in enumerate(carts):
            c.move_to([-0.7 + (idx % 4) * 1.10, 0.7 - (idx // 4) * 0.85, 0])
            c.set_opacity(0)
        self.add(carts)

        self.play(
            chain.animate.shift(RIGHT * 1.5),
            atp_val.animate.set_value(54),
            LaggedStart(*[c.animate.set_opacity(1) for c in carts[:4]], lag_ratio=0.2),
            run_time=2.4,
        )
        self.at("acetyl coenzyme")
        self.play(
            atp_val.animate.set_value(106),
            LaggedStart(*[c.animate.set_opacity(1) for c in carts[4:]], lag_ratio=0.2),
            chain.animate.scale(0.35).move_to(ws_wheel.get_center()),
            run_time=1.8,
        )

        # 5.68s: pullback into full carried world
        self.at("stretch that")
        world = make_full_world(branches=1, show_tissues=True, wheel_omega=1.6, ring_omega=1.3)
        world.brain.outline.set_stroke(opacity=0.55)
        self.play(
            FadeOut(VGroup(chain, carts, atp_bar_bg, atp_fill, atp_num, act_tag), run_time=0.5),
            ReplacementTransform(ws_box, world.liver_box, run_time=1.5),
            ReplacementTransform(ws_wheel, world.wheel, run_time=1.5),
            FadeIn(VGroup(world.sil, world.liver_lab, world.ring, world.rails, world.brain, world.brain_lab), run_time=1.5),
        )

        # 8.54s: 1965 -> day counter + progress bar starts at 1
        self.at("In 1965")
        day_t = ValueTracker(1.0)
        day_cnt = make_day_counter(day_t, at=(0.45, 2.48, 0), bar=True)
        self.play(FadeIn(day_cnt), run_time=0.5)
        self.play(day_t.animate.set_value(35.0), run_time=1.5, rate_func=linear)

        # 11.10s: stopped eating -> races to 382 and stops
        self.at("stopped eating")
        self.play(day_t.animate.set_value(382.0), run_time=2.8, rate_func=rush_into)

        # 14.92s: brain flickers + question at top
        self.at("How did his")
        q_txt = T("How did the brain keep running?", 34, TEXT).move_to([0.0, 3.30, 0])
        self.play(
            FadeIn(q_txt),
            world.brain.outline.animate.set_stroke(color=YELLOW, width=5, opacity=1.0),
            run_time=0.5,
        )
        self.play(world.brain.outline.animate.set_stroke(color=TEXT, width=3.8, opacity=0.90), run_time=0.5)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        self.add(scope_tag("schematic"))
        world = make_full_world(branches=1, show_tissues=True, wheel_omega=1.6, ring_omega=1.3)
        pulse(world.brain.outline, base=3.8, amp=1.8, speed=3.5)
        day_t = ValueTracker(382.0)
        day_cnt = make_day_counter(day_t, at=(0.45, 2.48, 0), bar=True)
        q_txt = T("How did the brain keep running?", 34, TEXT).move_to([0.0, 3.30, 0])
        self.add(world, day_cnt, q_txt)

        # Cleanly in lower middle (x -0.6..2.9, y -2.3..-1.1), 100% clear of liver (-1.35) and blood rails
        lesson = T("Fatty Acid Degradation", 24, GREY)
        title = T("Fuel the Liver Ships", 34, TEXT, font=TITLE_FONT)
        rule = Line(LEFT * 1.1, RIGHT * 1.1, color=GOLD, stroke_width=3.5)
        t_grp = VGroup(lesson, title, rule).arrange(DOWN, buff=0.14).move_to([1.15, -1.75, 0])

        self.play(FadeOut(q_txt, run_time=0.35), FadeIn(t_grp, run_time=0.5))
        self.wait(0.8)
        self.play(FadeOut(t_grp, run_time=0.3))
        self.finish()


class S02TheFast(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic"))
        world = make_full_world(branches=1, show_tissues=True, wheel_omega=1.6, ring_omega=1.3)
        day_t = ValueTracker(1.0)
        day_cnt = make_day_counter(day_t, at=(0.45, 2.75, 0), bar=True)
        self.add(world, day_cnt)

        # Start glucose flow early (brain depends on glucose early in a fast) and run day_t smoothly
        flow_rate = ValueTracker(0.55)
        hex_stream = stream_along_path(
            lambda _: make_glucose_hex(0.15),
            [[LANE_X0 + 0.1, LANE_Y, 0], [0.8, LANE_Y, 0], [1.85, 0.85, 0], [TISSUE_X - 0.95, BRAIN_POS[1], 0]],
            n_items=6,
            speed=0.40,
            active_fn=lambda u, t: flow_rate.get_value(),
        )
        self.add(hex_stream)

        # 2.64s: water, tea, coffee icons
        self.at("water")
        cups = VGroup()
        for col in (BLUE, GOLD, ORANGE):
            cup = VGroup(
                RoundedRectangle(corner_radius=0.06, width=0.28, height=0.30, color=col, stroke_width=2.5, fill_color=col, fill_opacity=0.25),
                Arc(radius=0.08, start_angle=-PI / 2, angle=PI, stroke_color=col, stroke_width=2.2).shift(RIGHT * 0.14),
            )
            cups.add(cup)
        cups.arrange(RIGHT, buff=0.28)
        cups_lab = T("water, tea, coffee", 24, TEXT).next_to(cups, DOWN, buff=0.12)
        cups_grp = VGroup(cups, cups_lab).move_to([0.35, 1.38, 0])
        self.play(FadeIn(cups_grp), day_t.animate.set_value(95.0), run_time=1.8, rate_func=linear)

        # 6.80s: 456 lb -> 180 lb with area-scaled BLUE fat droplet
        self.at("456")
        w_t = ValueTracker(456.0)
        r0 = 0.76
        droplet_anchor = np.array([-0.30, -1.55, 0.0])
        droplet = always_redraw(lambda: Circle(
            radius=r0 * np.sqrt(max(w_t.get_value(), 10.0) / 456.0),
            color=BLUE, stroke_width=3.2, fill_color=BLUE, fill_opacity=0.50,
        ).move_to(droplet_anchor))
        w_readout = always_redraw(lambda: M(f"{int(round(w_t.get_value())):3d} lb", 30, BLUE).move_to([1.45, -1.55, 0]))
        self.play(FadeIn(droplet), FadeIn(w_readout), run_time=0.45)
        self.play(
            w_t.animate.set_value(180.0),
            day_t.animate.set_value(382.0),
            run_time=3.1,
            rate_func=linear,
        )

        # 11.02s: Early in a fast, brain depends on glucose
        self.at("Early in a fast")
        self.play(flow_rate.animate.set_value(1.0), run_time=0.6)

        self.at("depends on glucose")
        self.play(world.brain.outline.animate.set_stroke(color=WHITE, width=5.2), run_time=0.9)

        # 15.24s: stream thins to trickle + '?'
        self.at("where could")
        q_mark = T("?", 46, WHITE, weight=BOLD).move_to([0.50, 0.48, 0])
        self.play(
            flow_rate.animate.set_value(0.22),
            world.brain.outline.animate.set_stroke(color=TEXT, width=3.8),
            FadeIn(q_mark),
            run_time=0.9,
        )
        self.finish()


class S03NoNetGlucose(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic"))
        liver = make_liver_zoom(wheel_pos=(-3.3, -0.05, 0), ring_pos=(1.15, -0.05, 0), ring_r=1.25, wheel_omega=1.8, ring_omega=1.5)
        ring_lab = T("citric acid cycle", 28, GREEN).next_to(liver.ring, UP, buff=0.22)

        exit_arr = Arrow([2.40, 0.25, 0], [3.85, 0.55, 0], color=GREY, stroke_width=3.5, buff=0.05)
        exit_lab = T("to glucose", 26, TEXT).next_to(exit_arr, UP, buff=0.14)
        hollow_hex = make_glucose_hex(0.24, hollow=True).move_to([4.28, 0.65, 0])

        tally_in = T("in: 2 C", 26, BLUE).move_to([-0.15, -1.85, 0])
        tally_out = T("out: 2 C", 26, GREY).move_to([1.35, -1.85, 0])
        tally_net = T("net: 0", 28, YELLOW).move_to([2.85, -1.85, 0])

        # Live fatty-acid feed + circulating 2-carbon packets so process is visibly continuous
        fa_feed = stream_along_path(
            lambda _: make_fat_chain(4, tile_w=0.14, gap=0.02),
            [[-5.6, -0.10, 0], [-4.1, -0.10, 0]],
            n_items=3, speed=0.45,
        )
        # Orbiting 2-carbon markers around the citric acid cycle ring
        orbit_grp = VGroup()
        ang_t = ValueTracker(0.0)
        orbit_grp.add_updater(lambda m, dt: ang_t.increment_value(-1.5 * dt))
        for k in range(3):
            b = RoundedRectangle(corner_radius=0.04, width=0.22, height=0.22, color=GREEN, stroke_width=2, fill_color=GREEN, fill_opacity=0.88)
            ph = k * TAU / 3
            b.add_updater(lambda m, p=ph: m.move_to(liver.ring.get_center() + 1.25 * np.array([np.cos(ang_t.get_value() + p), np.sin(ang_t.get_value() + p), 0])))
            orbit_grp.add(b)

        self.play(FadeIn(liver), FadeIn(ring_lab), FadeIn(exit_arr), FadeIn(exit_lab), FadeIn(hollow_hex), run_time=1.0)
        self.add(fa_feed, orbit_grp)

        self.at("citric")
        self.play(liver.ring.animate.scale(1.06), run_time=0.5)
        self.play(liver.ring.animate.scale(1 / 1.06), run_time=0.4)

        # 6.14s: takes in 2 carbons
        self.at("takes in")
        cart = make_acetyl_cart(1.15).move_to([-1.7, -0.05, 0])
        self.play(FadeIn(cart), run_time=0.4)
        self.play(cart.animate.move_to([-0.25, -0.05, 0]), run_time=0.9)
        c_tiles = cart.blocks.copy()
        self.add(c_tiles)
        self.play(
            c_tiles.animate.move_to(liver.ring.get_center() + LEFT * 0.50),
            cart.coa.animate.shift(LEFT * 1.4),
            FadeOut(cart),
            FadeIn(tally_in),
            run_time=1.0,
        )

        # 10.78s: loses two as CO2
        self.at("loses two")
        puff1 = chip("CO2", GREY, 24, pad=0.12).move_to([2.95, -0.75, 0])
        puff2 = chip("CO2", GREY, 24, pad=0.12).move_to([2.95, -1.35, 0])
        self.play(FadeOut(c_tiles, run_time=0.4), FadeIn(puff1), FadeIn(puff2), run_time=0.5)
        self.play(
            puff1.animate.shift(RIGHT * 1.35 + DOWN * 0.15),
            puff2.animate.shift(RIGHT * 1.35 + DOWN * 0.15),
            FadeIn(tally_out),
            run_time=1.4,
        )
        self.play(FadeOut(puff1), FadeOut(puff2), FadeIn(tally_net), run_time=0.6)

        # 15.32s: No oxaloacetate left over
        self.at("is left over")
        self.play(hollow_hex.animate.set_stroke(color=YELLOW, width=5.0), run_time=0.5)
        self.play(hollow_hex.animate.set_stroke(color=WHITE, width=3.0), run_time=0.5)
        self.finish()


class S04Exceptions(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic"))
        liver = make_liver_zoom(wheel_pos=(-3.3, -0.05, 0), ring_pos=(1.15, -0.05, 0), ring_r=1.25, wheel_omega=1.6, ring_omega=1.4)
        ring_lab = T("citric acid cycle", 28, GREEN).next_to(liver.ring, UP, buff=0.22)
        exit_arr = Arrow([2.40, 0.25, 0], [3.85, 0.55, 0], color=GREY, stroke_width=3.5, buff=0.05)
        exit_lab = T("to glucose", 26, TEXT).next_to(exit_arr, UP, buff=0.14)
        hollow_hex = make_glucose_hex(0.24, hollow=True).move_to([4.28, 0.65, 0])
        self.add(liver, ring_lab, exit_arr, exit_lab, hollow_hex)

        # 0.78s: glycerol backbone -> 1 WHITE hexagon out (finishes before 2.18s)
        self.at("glycerol")
        glyc = chip("glycerol", GREY, 24).move_to([-4.3, 1.70, 0])
        g_hex = make_glucose_hex(0.22).move_to([-0.8, 1.70, 0])
        self.play(FadeIn(glyc), run_time=0.20)
        self.play(glyc.animate.move_to([-1.2, 1.70, 0]), run_time=0.40)
        self.play(ReplacementTransform(glyc, g_hex), run_time=0.25)
        self.play(g_hex.animate.move_to([5.8, -0.13, 0]), run_time=0.40)

        # 2.18s: odd-chain tail (3 BLUE tiles) -> 1 WHITE hexagon out
        self.at("tail of odd")
        stub_tiles = make_fat_chain(3, tile_w=0.24, gap=0.04).move_to([-4.2, -1.75, 0])
        stub_lab = T("odd-chain tail", 24, BLUE).next_to(stub_tiles, DOWN, buff=0.14)
        o_hex = make_glucose_hex(0.22).move_to([2.6, -0.25, 0])
        self.play(FadeIn(stub_tiles), FadeIn(stub_lab), run_time=0.40)
        self.play(FadeOut(stub_lab, run_time=0.30), stub_tiles.animate.move_to([0.2, -1.65, 0]), run_time=0.90)
        self.play(ReplacementTransform(stub_tiles, o_hex), run_time=0.45)
        self.play(o_hex.animate.move_to([5.8, -0.13, 0]), run_time=0.80)
        self.play(FadeOut(g_hex), FadeOut(o_hex), run_time=0.30)

        # 7.34s: Most of fat's carbon needs another route
        self.at("needs another")
        pile = VGroup(*[make_acetyl_cart(1.05) for _ in range(4)]).arrange(UP, buff=0.14).scale(0.90).move_to([-1.21, -0.15, 0])
        cue = Circle(radius=0.95, color=YELLOW, stroke_width=4.5).move_to(pile)
        self.play(
            VGroup(exit_arr, exit_lab, hollow_hex).animate.set_opacity(0.35),
            LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in pile], lag_ratio=0.18),
            Create(cue),
            run_time=1.2,
        )
        self.finish()


class S05Flood(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic"))
        liver = make_liver_zoom(wheel_pos=(-2.95, -0.10, 0), ring_pos=(2.35, 0.05, 0), ring_r=1.15, wheel_omega=1.1, ring_omega=0.9)
        ring_lab = T("citric acid cycle", 26, GREEN).next_to(liver.ring, UP, buff=0.20)
        mito_wall = Line([-4.55, -1.65, 0], [-4.55, 1.55, 0], color=GREY, stroke_width=3.8)
        gate_hinge = np.array([-4.55, 0.25, 0.0])
        gate = Line(gate_hinge, [-4.55, -0.55, 0], color=YELLOW, stroke_width=6.5)
        gate_lab = T("carnitine gate", 24, YELLOW).move_to([-3.85, -2.05, 0])

        # Insulin gauge on far left top; swap cleanly between 'high' and 'low' (avoids become() height quirk)
        ins_t = ValueTracker(0.85)
        ins_bg = RoundedRectangle(corner_radius=0.06, width=0.38, height=1.35, color=GREY, stroke_width=2.4).move_to([-6.12, 1.65, 0])
        ins_fill = always_redraw(lambda: RoundedRectangle(
            corner_radius=0.04, width=0.30, height=max(0.06, 1.27 * ins_t.get_value()),
            color=RED if ins_t.get_value() < 0.35 else GREEN, stroke_width=0,
            fill_color=RED if ins_t.get_value() < 0.35 else GREEN, fill_opacity=0.88,
        ).align_to(ins_bg.get_bottom() + UP * 0.04, DOWN).set_x(ins_bg.get_x()))
        ins_lab = T("insulin", 24, TEXT).next_to(ins_bg, UP, buff=0.14)
        ins_high = T("high", 24, GREEN).next_to(ins_bg, DOWN, buff=0.14)
        ins_low = T("low", 24, RED).next_to(ins_bg, DOWN, buff=0.14)

        self.add(liver, ring_lab, mito_wall, gate, gate_lab, ins_bg, ins_fill, ins_lab, ins_high)

        # 1.98s: low insulin + fatty acid flood
        self.at("low insulin")
        fa_chains = stream_along_path(
            lambda _: make_fat_chain(6, tile_w=0.13, gap=0.02),
            [[-6.2, -0.15, 0], [-4.8, -0.15, 0]],
            n_items=4, speed=0.55,
        )
        self.add(fa_chains)
        self.play(ins_t.animate.set_value(0.15), swap(ins_high, ins_low, run_time=0.6), run_time=1.8)

        # 5.82s: carnitine gate swings open; chains pour through
        self.at("opens")
        self.play(Rotate(gate, angle=PI / 2, about_point=gate_hinge), run_time=0.9)
        self.remove(fa_chains)
        fa_pour = stream_along_path(
            lambda _: make_fat_chain(6, tile_w=0.13, gap=0.02),
            [[-6.2, -0.15, 0], [-3.15, -0.10, 0]],
            n_items=5, speed=0.65,
        )
        self.add(fa_pour)

        # 8.84s: beta-oxidation wheel speeds up
        self.at("Beta")
        liver.wheel._omega = 2.8
        fast_carts = stream_along_path(
            lambda _: make_acetyl_cart(0.85),
            [[-2.00, -0.1, 0], [-1.28, -0.1, 0]],
            n_items=2, speed=1.1,
        )
        slow_carts = stream_along_path(
            lambda _: make_acetyl_cart(0.85),
            [[0.08, 0.05, 0], [1.15, 0.05, 0]],
            n_items=2, speed=0.35,
        )
        self.add(fast_carts, slow_carts)

        # 11.96s: queue grows taller -> 'surplus'
        self.at("faster than")
        surplus_lab = T("surplus", 28, YELLOW).move_to([-0.60, 2.05, 0])
        self.play(FadeIn(surplus_lab), run_time=0.4)
        q_carts = VGroup(*[make_acetyl_cart(0.95) for _ in range(6)]).arrange(UP, buff=0.12).move_to([-0.60, -0.15, 0])
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in q_carts], lag_ratio=0.22), run_time=2.5)
        self.finish()


class S06Repackage(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic"))
        liver = make_liver_zoom(wheel_pos=(-4.1, -0.1, 0), ring_pos=(3.15, 1.15, 0), ring_r=0.68, wheel_omega=1.8, ring_omega=1.2)
        ring_lab = T("citric acid cycle", 24, GREEN).next_to(liver.ring, UP, buff=0.14)
        q_carts = VGroup(*[make_acetyl_cart(0.90) for _ in range(5)]).arrange(UP, buff=0.10).move_to([-2.35, -0.20, 0])
        q_lab = T("surplus", 26, YELLOW).next_to(q_carts, UP, buff=0.18)

        # Live fatty-acid stream feeding wheel so workshop visibly keeps running
        fa_feed = stream_along_path(
            lambda _: make_fat_chain(4, tile_w=0.12, gap=0.02),
            [[-6.2, -0.12, 0], [-4.9, -0.12, 0]],
            n_items=3, speed=0.55,
        )

        press_top = RoundedRectangle(corner_radius=0.06, width=0.90, height=0.20, color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.35).move_to([-0.65, 0.55, 0])
        press_bot = press_top.copy().move_to([-0.65, -0.85, 0])
        press = VGroup(press_top, press_bot)

        self.add(liver, ring_lab, fa_feed, q_carts, q_lab, press)

        # 0.72s: press draws 2 GREEN carts from surplus
        self.at("repackages")
        c1, c2 = q_carts[-1], q_carts[-2]
        self.play(
            c1.animate.move_to([-0.65, 0.05, 0]),
            c2.animate.move_to([-0.65, -0.40, 0]),
            run_time=1.5,
        )

        # 3.58s: Two acetyl-CoA -> CoA handles return left
        self.at("Two acetyl")
        self.play(
            press_top.animate.shift(DOWN * 0.16),
            press_bot.animate.shift(UP * 0.16),
            c1.coa.animate.move_to(liver.wheel.get_center() + UP * 0.3),
            c2.coa.animate.move_to(liver.wheel.get_center() + DOWN * 0.3),
            run_time=1.1,
        )
        self.play(FadeOut(c1.coa), FadeOut(c2.coa), run_time=0.25)

        # 5.16s: become one acetoacetate capsule
        self.at("become one")
        cap = make_ketone_capsule(1.30).move_to([1.65, -0.15, 0])
        ac_lab = T("acetoacetate", 26, TEAL).next_to(cap, DOWN, buff=0.22)
        kb_lab = T("ketone body", 24, TEXT).next_to(ac_lab, DOWN, buff=0.14)
        self.play(
            ReplacementTransform(VGroup(c1.blocks, c2.blocks), cap),
            press_top.animate.shift(UP * 0.16),
            press_bot.animate.shift(DOWN * 0.16),
            run_time=1.2,
        )
        self.play(FadeIn(ac_lab), FadeIn(kb_lab), run_time=0.6)

        # 9.78s: reduced by NADH -> NAD+ -> D-3-hydroxybutyrate
        self.at("reduced")
        nadh = chip("NADH", PINK, 24).move_to([1.65, 1.35, 0])
        nadp = chip("NAD+", PINK, 24).move_to([0.35, 1.35, 0])
        self.play(FadeIn(nadh), run_time=0.35)
        self.play(nadh.animate.next_to(cap, UP, buff=0.14), run_time=0.7)
        hb_lab = T("D-3-hydroxybutyrate", 26, TEAL).move_to([1.65, -0.95, 0])
        self.play(
            ReplacementTransform(nadh, nadp),
            FadeOut(kb_lab),
            swap(ac_lab, hb_lab, run_time=0.6),
            run_time=0.9,
        )
        self.play(FadeOut(nadp, shift=LEFT * 0.5), run_time=0.5)

        # 12.58s: line up TEAL capsules at liver edge
        self.at("dominant form")
        lineup = VGroup(*[make_ketone_capsule(1.05) for _ in range(3)]).arrange(DOWN, buff=0.20).move_to([4.05, -0.15, 0])
        self.play(
            cap.animate.scale(1.05 / 1.30).move_to(lineup[0]),
            hb_lab.animate.move_to([2.95, -1.85, 0]),
            FadeIn(lineup[1]),
            FadeIn(lineup[2]),
            run_time=1.2,
        )
        self.finish()


class S07Idea(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic"))
        world = make_full_world(branches=3, show_tissues=True, wheel_omega=1.8, ring_omega=1.4)
        world.muscle_lab.shift(RIGHT * 0.25)
        hollow_hex = make_glucose_hex(0.22, hollow=True).move_to([-1.65, 1.55, 0])
        # Capsules already exiting liver along blood trunk from t=0
        trunk_stream = stream_along_path(
            lambda _: make_ketone_capsule(0.75),
            [[-2.10, -0.15, 0], [LANE_XJ, LANE_Y, 0]],
            n_items=5, speed=0.55,
        )
        self.add(world, hollow_hex, trunk_stream)

        # 3.62s: cannot become net glucose -> hex flashes & fades, then streams extend to branches
        self.at("cannot become")
        self.play(hollow_hex.animate.scale(1.3).set_stroke(color=YELLOW, width=5.5), run_time=0.5)
        self.play(FadeOut(hollow_hex), run_time=0.6)

        # Start branched flow as fast/ships sentence begins
        self.at("liver ships")
        self.remove(trunk_stream)
        ship_lab = T("ships ketones", 28, TEAL).move_to([0.10, -0.82, 0])
        top_stream = stream_along_path(
            lambda _: make_ketone_capsule(0.70),
            [[LANE_X0 + 0.15, LANE_Y, 0], [LANE_XJ, LANE_Y, 0], [2.15, 0.55 * BRAIN_POS[1] + 0.45 * LANE_Y, 0], [TISSUE_X - 0.95, BRAIN_POS[1], 0]],
            n_items=5, speed=0.35,
        )
        mid_stream = stream_along_path(
            lambda _: make_ketone_capsule(0.70),
            [[LANE_X0 + 0.15, LANE_Y, 0], [LANE_XJ, LANE_Y, 0], [TISSUE_X - 0.95, MUSCLE_POS[1], 0]],
            n_items=5, speed=0.35,
        )
        bot_stream = stream_along_path(
            lambda _: make_ketone_capsule(0.70),
            [[LANE_X0 + 0.15, LANE_Y, 0], [LANE_XJ, LANE_Y, 0], [2.15, 0.55 * RBC_POS[1] + 0.45 * LANE_Y, 0], [TISSUE_X - 0.95, RBC_POS[1], 0]],
            n_items=5, speed=0.35,
        )
        self.play(FadeIn(ship_lab), run_time=0.5)
        self.add(top_stream, mid_stream, bot_stream)

        # 11.66s: capsules hover at tissues without entering
        self.at("other tissues")
        self.wait(1.0)
        self.finish()


class S08Ledger(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic"))
        world = make_full_world(branches=3, show_tissues=True, wheel_omega=1.6, ring_omega=1.3)
        fadh_chip = chip("FADH2", PINK, 22, pad=0.12).move_to([-4.25, -1.25, 0])
        nadh_chip = chip("NADH", PINK, 22, pad=0.12).move_to([-2.45, -1.25, 0])
        carriers = VGroup(fadh_chip, nadh_chip)

        # GOLD 106 ATP gauge at far left (x = -5.75), animated filling 0->106 early so scene is active
        bar_h = 4.24
        bar_w = 0.56
        bar_x = -5.75
        atp_fill_t = ValueTracker(20.0)
        bar_bg = RoundedRectangle(corner_radius=0.06, width=bar_w, height=bar_h, color=GREY, stroke_width=2.2).move_to([bar_x, -0.1, 0])
        full_gold = always_redraw(lambda: Rectangle(
            width=bar_w - 0.06, height=max(0.08, (bar_h - 0.06) * (atp_fill_t.get_value() / 106.0)),
            color=GOLD, stroke_width=0, fill_color=GOLD, fill_opacity=0.90,
        ).align_to(bar_bg.get_bottom() + UP * 0.03, DOWN).set_x(bar_x))
        top_num = T("roughly 106 ATP", 24, GOLD).move_to([-5.35, 2.42, 0])
        self.add(world, carriers, bar_bg, full_gold, top_num)
        self.play(atp_fill_t.animate.set_value(106.0), run_time=2.5, rate_func=linear)

        # 3.04s: 4 acetoacetate (2 GREEN blocks each = 8 blocks) at liver exit
        self.at("exports palmitate")
        four_caps = VGroup(*[make_ketone_capsule(0.75) for _ in range(4)]).arrange(DOWN, buff=0.18).move_to([-0.75, -0.15, 0])
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in four_caps], lag_ratio=0.18), run_time=1.8)

        # 6.32s: split bar to exact scale 26/106 vs 80/106
        self.at("keeps")
        h_low = (bar_h - 0.06) * (26.0 / 106.0)
        h_high = (bar_h - 0.06) * (80.0 / 106.0)
        seg_low = Rectangle(width=bar_w - 0.06, height=h_low, color=GREEN, stroke_width=0, fill_color=GREEN, fill_opacity=0.90)
        seg_low.align_to(bar_bg.get_bottom() + UP * 0.03, DOWN).set_x(bar_x)
        seg_high = Rectangle(width=bar_w - 0.06, height=h_high, color=TEAL, stroke_width=0, fill_color=TEAL, fill_opacity=0.88)
        seg_high.align_to(bar_bg.get_top() - UP * 0.03, UP).set_x(bar_x)
        low_lab = T("liver keeps 26", 24, GREEN).move_to([-5.10, -2.72, 0])
        self.remove(full_gold)
        self.play(
            FadeIn(seg_low, run_time=0.4),
            FadeIn(seg_high, run_time=0.4),
            FadeIn(low_lab, run_time=0.5),
        )

        # 10.76s: upper segment leaves gauge cleanly upward/right (never crossing purple wheel!) to blood lane
        self.at("tissues that burn")
        high_lab = T("tissues: most of rest", 24, TEAL).move_to([0.25, 1.50, 0])
        seg_target = Rectangle(width=2.1, height=0.35, color=TEAL, stroke_width=0, fill_color=TEAL, fill_opacity=0.88).move_to([0.25, 0.95, 0])
        self.play(
            FadeOut(seg_high, shift=RIGHT * 0.4),
            FadeIn(seg_target, shift=RIGHT * 1.2),
            four_caps.animate.move_to([1.35, -0.30, 0]),
            run_time=1.8,
        )
        self.play(FadeIn(high_lab), run_time=0.5)
        self.finish()


class S09Predict(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic"))
        world = make_full_world(branches=3, show_tissues=True, wheel_omega=1.5, ring_omega=1.2)
        for m in (world.brain, world.brain_lab, world.muscle, world.muscle_lab, world.rbc, world.rbc_lab):
            m.set_opacity(0.42)
        lane_caps = stream_along_path(
            lambda _: make_ketone_capsule(0.62),
            [[LANE_X0 + 0.15, LANE_Y, 0], [LANE_XJ, LANE_Y, 0], [TISSUE_X - 0.95, MUSCLE_POS[1], 0]],
            n_items=4, speed=0.25,
        )
        self.add(world, lane_caps)

        # 3.48s: capsules peel back toward liver's GREEN ring and bob at its rim
        self.at("liver made")
        hover_caps = VGroup(*[make_ketone_capsule(0.70) for _ in range(3)])
        targets = [
            RING_POS + np.array([0.85, 0.55, 0]),
            RING_POS + np.array([0.92, 0.0, 0]),
            RING_POS + np.array([0.85, -0.55, 0]),
        ]
        for c in hover_caps:
            c.move_to([-0.8, -0.15, 0])
        self.play(LaggedStart(*[c.animate.move_to(t) for c, t in zip(hover_caps, targets)], lag_ratio=0.15), run_time=1.3)
        for i, c in enumerate(hover_caps):
            bob(c, amp=0.12, speed=3.2, seed=i)

        # 5.84s: question card
        self.at("Will the liver")
        q = question_card("Will the liver burn them?", y=-2.95)
        self.play(FadeIn(q.question), run_time=0.8)
        self.finish()


class S10Pause(PredictPause):
    QUESTION = "Will the liver burn them?"
    SECONDS = 4.5
    CARD = {"y": -2.95}

    def backdrop(self):
        world = make_full_world(branches=3, show_tissues=True, wheel_omega=1.5, ring_omega=1.2)
        for m in (world.brain, world.brain_lab, world.muscle, world.muscle_lab, world.rbc, world.rbc_lab):
            m.set_opacity(0.42)
        hover_caps = VGroup(*[make_ketone_capsule(0.70) for _ in range(3)])
        targets = [
            RING_POS + np.array([0.85, 0.55, 0]),
            RING_POS + np.array([0.92, 0.0, 0]),
            RING_POS + np.array([0.85, -0.55, 0]),
        ]
        for i, (c, t) in enumerate(zip(hover_caps, targets)):
            c.move_to(t)
            bob(c, amp=0.12, speed=3.2, seed=i)
        lane_caps = stream_along_path(
            lambda _: make_ketone_capsule(0.62),
            [[LANE_X0 + 0.15, LANE_Y, 0], [LANE_XJ, LANE_Y, 0], [TISSUE_X - 0.95, MUSCLE_POS[1], 0]],
            n_items=4, speed=0.25,
        )
        return VGroup(world, hover_caps, lane_caps)


class S11Answer(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic"))
        world = make_full_world(branches=3, show_tissues=True, wheel_omega=1.5, ring_omega=1.2)
        hover_caps = VGroup(*[make_ketone_capsule(0.70) for _ in range(3)])
        for c, t in zip(hover_caps, [RING_POS + [0.85, 0.55, 0], RING_POS + [0.92, 0.0, 0], RING_POS + [0.85, -0.55, 0]]):
            c.move_to(t)
        q = question_card("Will the liver burn them?", y=-2.95)
        self.add(world, hover_caps, q)

        # 0.00s: question dissolves into white 'No'
        no_txt = T("No", 38, WHITE, weight=BOLD).move_to([0.0, -3.0, 0])
        self.play(swap(q.question, no_txt, run_time=0.7), run_time=0.8)

        # 2.22s: liver lacks thiophorase -> empty ORANGE slot (No fades out cleanly)
        self.at("liver lacks")
        coa_slot = RoundedRectangle(corner_radius=0.08, width=0.26, height=0.40, color=ORANGE, stroke_width=3, fill_opacity=0.0).move_to(RING_POS + RIGHT * 0.72)
        no_thio = T("no thiophorase", 24, ORANGE).move_to([-2.95, -1.15, 0])
        self.play(FadeOut(no_txt, run_time=0.4), FadeIn(coa_slot), FadeIn(no_thio), run_time=0.6)

        # 5.00s: capsules bounce off and join blood lane
        self.at("reloads")
        liver_no = T("cannot use", 26, RED).move_to([-3.25, -2.75, 0])
        self.play(
            hover_caps.animate.move_to([0.2, LANE_Y, 0]),
            FadeIn(liver_no),
            run_time=1.3,
        )
        self.remove(hover_caps)
        top_stream = stream_along_path(lambda _: make_ketone_capsule(0.62), [[LANE_X0 + 0.15, LANE_Y, 0], [LANE_XJ, LANE_Y, 0], [2.15, 0.55 * BRAIN_POS[1] + 0.45 * LANE_Y, 0], [TISSUE_X - 0.95, BRAIN_POS[1], 0]], n_items=3, speed=0.28)
        mid_stream = stream_along_path(lambda _: make_ketone_capsule(0.62), [[LANE_X0 + 0.15, LANE_Y, 0], [LANE_XJ, LANE_Y, 0], [TISSUE_X - 0.95, MUSCLE_POS[1], 0]], n_items=3, speed=0.28)
        self.add(top_stream, mid_stream)

        # 8.80s: red blood cell bounces capsules
        self.at("Red blood")
        rbc_cap = make_ketone_capsule(0.65).move_to([2.45, RBC_POS[1] + 0.15, 0])
        self.add(rbc_cap)
        self.play(rbc_cap.animate.move_to([2.95, RBC_POS[1], 0]), run_time=0.6)
        self.play(rbc_cap.animate.move_to([2.25, RBC_POS[1] - 0.35, 0]), run_time=0.5)

        self.at("no mitochondria")
        no_mito = T("no mitochondria", 24, TEXT).move_to([0.95, -2.18, 0])
        rbc_no = T("cannot use", 24, RED).move_to([TISSUE_X, -2.95, 0])
        self.play(FadeOut(rbc_cap), FadeIn(no_mito), FadeIn(rbc_no), run_time=0.8)

        # 14.40s: heart, muscle, kidney -> ORANGE handle clips, splits to 2 GREEN blocks, glows GREEN
        self.at("Heart")
        m_cap = make_ketone_capsule(0.68).move_to([2.85, MUSCLE_POS[1], 0])
        m_coa = RoundedRectangle(corner_radius=0.05, width=0.14, height=0.24, color=ORANGE, stroke_width=2, fill_color=ORANGE, fill_opacity=0.85).move_to([3.25, MUSCLE_POS[1], 0])
        m_can = T("can use", 24, GREEN).next_to(world.muscle, RIGHT, buff=0.18)
        self.play(FadeIn(m_cap), run_time=0.2)
        self.play(
            m_cap.animate.move_to(MUSCLE_POS),
            FadeIn(m_coa),
            world.muscle.outline.animate.set_stroke(color=GREEN, width=5).set_fill(color=GREEN, opacity=0.24),
            FadeIn(m_can),
            run_time=0.9,
        )
        self.play(FadeOut(m_cap), FadeOut(m_coa), run_time=0.2)

        # 15.96s: after adaptation, brain glows GREEN more slowly
        self.at("after adaptation")
        b_can = T("can use", 24, GREEN).next_to(world.brain, RIGHT, buff=0.18)
        self.play(
            world.brain.outline.animate.set_stroke(color=GREEN, width=5).set_fill(color=GREEN, opacity=0.22),
            FadeIn(b_can),
            run_time=1.8,
        )
        self.finish()


class S12Cahill(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic"))
        world = make_full_world(branches=3, show_tissues=True, wheel_omega=1.5, ring_omega=1.2)
        day_t = ValueTracker(1.0)
        day_cnt = make_day_counter(day_t, at=(0.45, 2.75, 0), max_days=40.0, bar=True)
        ketone_stream = stream_along_path(
            lambda _: make_ketone_capsule(0.65),
            [[LANE_X0 + 0.15, LANE_Y, 0], [LANE_XJ, LANE_Y, 0], [2.15, 0.55 * BRAIN_POS[1] + 0.45 * LANE_Y, 0], [TISSUE_X - 0.95, BRAIN_POS[1], 0]],
            n_items=5, speed=0.30,
        )
        self.add(world, day_cnt, ketone_stream)

        # Vertical bar on far right lower (x = 5.82, y = -1.25) so label clears both 'muscle spared' and prot_chips
        prot_t = ValueTracker(75.0)
        bar_h = 1.75
        bar_bg = RoundedRectangle(corner_radius=0.06, width=0.44, height=bar_h, color=GREY, stroke_width=2.2).move_to([5.82, -1.25, 0])
        bar_fill = always_redraw(lambda: RoundedRectangle(
            corner_radius=0.04, width=0.36, height=max(0.08, (bar_h - 0.08) * (prot_t.get_value() / 80.0)),
            color=YELLOW, stroke_width=0, fill_color=YELLOW, fill_opacity=0.88,
        ).align_to(bar_bg.get_bottom() + UP * 0.04, DOWN).set_x(bar_bg.get_x()))
        bar_lab = T("protein\nbroken down\n(g/day)", 22, TEXT, line_spacing=0.85).next_to(bar_bg, UP, buff=0.28)
        bar_num = always_redraw(lambda: M(f"{int(round(prot_t.get_value())):2d}", 30, YELLOW).next_to(bar_bg, DOWN, buff=0.14))

        prot_chips = stream_along_path(
            lambda _: RoundedRectangle(corner_radius=0.03, width=0.18, height=0.12, color=GREY, stroke_width=1.5, fill_color=GREY, fill_opacity=0.85),
            [[MUSCLE_POS[0] + 0.85, MUSCLE_POS[1] - 0.15, 0], [5.45, -0.50, 0]],
            n_items=4, speed=0.45,
            active_fn=lambda u, t: np.clip((prot_t.get_value() - 10.0) / 65.0, 0.18, 1.0),
        )

        self.at("By day")
        self.play(FadeIn(bar_bg), FadeIn(bar_fill), FadeIn(bar_lab), FadeIn(bar_num), run_time=0.6)
        self.add(prot_chips)

        self.at("protein breakdown")
        decay_rf = lambda a: (1.0 - np.exp(-3.0 * a)) / (1.0 - np.exp(-3.0))
        self.play(
            day_t.animate.set_value(40.0),
            prot_t.animate.set_value(20.0),
            run_time=4.8,
            rate_func=decay_rf,
        )

        self.at("shifted onto")
        brain_ket = make_ketone_capsule(0.65).move_to(BRAIN_POS)
        self.play(
            FadeIn(brain_ket),
            world.brain.outline.animate.set_stroke(color=TEAL, width=4.8),
            run_time=1.0,
        )

        self.at("sparing muscle")
        spared = T("muscle spared", 24, GREEN).next_to(world.muscle, UP, buff=0.16).shift(LEFT * 0.20)
        self.play(
            world.muscle.outline.animate.set_stroke(color=GREEN, width=4.8),
            FadeIn(spared),
            run_time=1.0,
        )
        self.finish()


class S13Return(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic"))
        world = make_full_world(branches=1, show_tissues=True, wheel_omega=1.6, ring_omega=1.3)
        day_t = ValueTracker(1.0)
        day_cnt = make_day_counter(day_t, at=(0.45, 2.75, 0), bar=True)
        w_t = ValueTracker(456.0)
        r0 = 0.76
        droplet_anchor = np.array([-0.30, -1.55, 0.0])
        droplet = always_redraw(lambda: Circle(
            radius=r0 * np.sqrt(max(w_t.get_value(), 10.0) / 456.0),
            color=BLUE, stroke_width=3.2, fill_color=BLUE, fill_opacity=0.50,
        ).move_to(droplet_anchor))
        w_readout = always_redraw(lambda: M(f"{int(round(w_t.get_value())):3d} lb", 30, BLUE).move_to([1.45, -1.55, 0]))
        self.add(world, day_cnt, droplet, w_readout)

        ket_stream = stream_along_path(
            lambda _: make_ketone_capsule(0.70),
            [[LANE_X0 + 0.15, LANE_Y, 0], [0.8, LANE_Y, 0], [1.85, 0.85, 0], [TISSUE_X - 0.95, BRAIN_POS[1], 0]],
            n_items=6, speed=0.35,
        )
        self.add(ket_stream)

        self.at("a year of fat")
        self.play(day_t.animate.set_value(180.0), w_t.animate.set_value(320.0), run_time=4.5, rate_func=linear)

        self.at("would have run")
        hedge = T("would have\n(not measured)", 22, TEXT).next_to(world.brain, DOWN, buff=0.22)
        self.play(
            FadeIn(hedge),
            day_t.animate.set_value(310.0),
            w_t.animate.set_value(225.0),
            run_time=3.5,
            rate_func=linear,
        )

        # 10.56s: thin WHITE glucose hexagon trickle above top rail
        self.at("Gluconeogenesis")
        gluco_stream = stream_along_path(
            lambda _: make_glucose_hex(0.12),
            [[LANE_X0 + 0.15, LANE_Y + 0.34, 0], [0.7, LANE_Y + 0.34, 0], [1.75, 1.15, 0], [TISSUE_X - 0.95, BRAIN_POS[1] + 0.25, 0]],
            n_items=2, speed=0.22,
        )
        gluco_lab = T("gluconeogenesis", 24, WHITE).move_to([0.30, 1.35, 0])
        self.add(gluco_stream)
        self.play(FadeIn(gluco_lab, run_time=0.4), day_t.animate.set_value(382.0), w_t.animate.set_value(180.0), run_time=2.5, rate_func=linear)
        self.finish()


class S14Close(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic"))
        world = make_full_world(branches=3, show_tissues=True, wheel_omega=1.6, ring_omega=1.3)
        hollow_hex = make_glucose_hex(0.20, hollow=True).move_to([-1.65, 1.55, 0])
        coa_slot = RoundedRectangle(corner_radius=0.08, width=0.26, height=0.40, color=ORANGE, stroke_width=3, fill_opacity=0.0).move_to(RING_POS + RIGHT * 0.72)
        top_stream = stream_along_path(lambda _: make_ketone_capsule(0.65), [[LANE_X0 + 0.15, LANE_Y, 0], [LANE_XJ, LANE_Y, 0], [2.15, 0.55 * BRAIN_POS[1] + 0.45 * LANE_Y, 0], [TISSUE_X - 0.95, BRAIN_POS[1], 0]], n_items=4, speed=0.30)
        mid_stream = stream_along_path(lambda _: make_ketone_capsule(0.65), [[LANE_X0 + 0.15, LANE_Y, 0], [LANE_XJ, LANE_Y, 0], [TISSUE_X - 0.95, MUSCLE_POS[1], 0]], n_items=4, speed=0.30)
        self.add(world, hollow_hex, coa_slot, top_stream, mid_stream)

        # 1.80s: hollow hex flashes once and fades for good
        self.at("no net sugar")
        self.play(hollow_hex.animate.set_stroke(color=YELLOW, width=5), run_time=0.4)
        self.play(FadeOut(hollow_hex), run_time=0.6)

        # 5.70s: empty CoA slot glows
        self.at("cannot burn")
        self.play(coa_slot.animate.set_stroke(color=YELLOW, width=5).set_fill(color=ORANGE, opacity=0.40), run_time=0.9)

        # 7.46s: brain + heart/muscle/kidney glow GREEN together; red blood cell stays dim
        self.at("tissues that can")
        self.play(
            world.brain.outline.animate.set_stroke(color=GREEN, width=5).set_fill(color=GREEN, opacity=0.24),
            world.muscle.outline.animate.set_stroke(color=GREEN, width=5).set_fill(color=GREEN, opacity=0.24),
            VGroup(world.rbc, world.rbc_lab).animate.set_opacity(0.32),
            run_time=1.1,
        )
        self.finish()


class S15End(EndCard):
    LINE = "Even-chain fat makes no net glucose, so the liver ships ketones."
