"""Steering Blood Toward Air — Ventilation, Perfusion and Gas Exchange (Chapter 2)

COLOUR MAP (one colour per concept, kept all film):
  BLUE   (#58C4DD) : air, ventilation (alveolus boxes, air arrows, inspired gas chips)
  RED    (#FC6255) : blood, perfusion (arterial inflow trunk, branches, outflow vein, blood dots)
  YELLOW (#F5D547) : oxygen carried in blood leaving units, and predict/question highlights
  ORANGE (#FF862F) : pulmonary artery smooth muscle ring (narrowing) and smooth muscle cell
  GREY   (#8B93A1) : lung outline, inactive/relaxed state, nerves, structural labels, schematic tag
  TEXT   (#E8EAF0) : pressure gauge, voltage meter, primary labels, active test checks
  PURPLE (#9A72AC) : calcium ions and voltage-gated calcium channels
  CYAN   (#3FB8C0) : hypothesized mitochondrial oxygen sensor (Cox4i2)
  PINK   (#D147BD) : systemic working muscle block (S02 contrast only)

ONE WORLD CARRIED ALL FILM:
  A rounded grey lung outline filling ~70% of frame height, containing three lung units in a row
  (rounded BLUE alveolus boxes, BLUE air arrows entering from above, a shared RED inflow trunk
  below branching through ORANGE smooth-muscle rings into each unit, and three RED outflow
  streams joining above into one vein leaving at the right with YELLOW oxygen dots).

WHAT CHANGES IN EACH SPOKEN SCENE (and what computes it):
  s00_link_and_question : LEFT unit ventilation tracker drops 1.0 -> 0.18; computed O2 dot loading
                          drops in LEFT outflow and dilutes the shared vein mix; question appears.
  s02_opposite          : Systemic muscle arteriole ring widens (flow fraction up) vs lung LEFT
                          ORANGE ring narrows (conductance drops 1.0 -> 0.14, computed flow diverts
                          to middle & right units).
  s03_ratio_up          : LEFT perfusion tracker drops further; computed V/Q bar ratio and vertical
                          ratio pointer rise modestly on low-high scale; blood shifts to right units.
  s04_cat               : Pressure ValueTracker swings from baseline (0.50) to high (0.88) on 10.5% O2
                          and slightly below baseline (0.38) on 100% O2, driving dial needle & arc.
  s05_predict           : Vagus nerve snaps & falls; stellate ganglion fades; 10.5% O2 returns with
                          gauge covered by '?' and YELLOW question card at top.
  s07_answer            : Gauge cover lifts revealing needle still high (0.88); all three rings turn
                          ORANGE and tighten slightly; flow?/outflow? uncertainty tags appear.
  s08_idea              : Experiment props clear; LEFT unit dims, LEFT ring tightens (conductance down),
                          computed blood dots reroute to middle & right; summary banner appears.
  s09_mechanism         : Zoom into smooth muscle cell; K+ door closes (outward dot rate 1.0 -> 0.15),
                          membrane voltage tracker rises, Ca2+ doors open (inward PURPLE dots), cell
                          geometry shortens & thickens dynamically.
  s10_sensor            : CYAN mitochondrion fades in; pullback to isolated mouse lung (Cox4i2 removed);
                          hypoxia test leaves ring open (0.0), KCl test tightens same ring (1.0).
  s11_upstream          : Test buttons fold into 3-step chain (sensing -> signaling -> contraction);
                          contraction gets tick, upstream bracket highlights sensing+signaling.
  s12_when              : Healthy lung at rest shows even flow; uneven ventilation narrows LEFT ring and
                          diverts flow; altitude pales all three air arrows slightly.
  s13_return            : LEFT ring tightens from open to narrowed; computed blood flow diverts to
                          middle & right units while ratio pointer climbs modestly; O2 dots unchanged.
"""
from bp_parts import *

CYAN = TEAL
SEED = 7


# ------------------------------------------------------------------ shared icons & helpers
def tick_mark(color=TEXT, size=0.34, stroke=5):
    return VGroup(
        Line([-0.4 * size, 0.0, 0], [-0.1 * size, -0.35 * size, 0], color=color, stroke_width=stroke),
        Line([-0.1 * size, -0.35 * size, 0], [0.45 * size, 0.4 * size, 0], color=color, stroke_width=stroke),
    )


def cross_mark(color=TEXT, size=0.30, stroke=5):
    return VGroup(
        Line([-0.38 * size, -0.38 * size, 0], [0.38 * size, 0.38 * size, 0], color=color, stroke_width=stroke),
        Line([-0.38 * size, 0.38 * size, 0], [0.38 * size, -0.38 * size, 0], color=color, stroke_width=stroke),
    )


def ratio_scale(ratio_tracker, pos, height=2.2, show_label=True):
    """Vertical low-to-high scale with a moving pointer driven by ratio_tracker (0..1)."""
    pos = np.array(pos, dtype=float)
    bar = Line(pos + DOWN * (height / 2), pos + UP * (height / 2), color=GREY, stroke_width=5)
    t_low = T("low", 24, GREY).next_to(bar, DOWN, buff=0.14)
    t_high = T("high", 24, GREY).next_to(bar, UP, buff=0.14)

    def mk_ptr():
        v = float(np.clip(ratio_tracker.get_value(), 0.05, 0.95))
        y = pos[1] - height / 2 + v * height
        tri = Triangle(color=YELLOW, fill_color=YELLOW, fill_opacity=1, stroke_width=0).scale(0.15)
        tri.rotate(-PI / 2).move_to([pos[0] - 0.24, y, 0])
        return tri

    ptr = always_redraw(mk_ptr)
    g = VGroup(bar, t_low, t_high, ptr)
    if show_label:
        tag = T("ratio", 26, YELLOW).next_to([pos[0] - 0.38, pos[1], 0], LEFT, buff=0.14)
        g.add(tag)
    return g


def pressure_gauge(p_tracker, center, radius=0.78):
    """Schematic WHITE pressure dial gauge (no numbers, baseline tick at middle)."""
    c = np.array(center, dtype=float)
    face = Circle(radius=radius, color=TEXT, stroke_width=3.5, fill_color=BG, fill_opacity=0.92).move_to(c)
    track = Arc(radius=radius * 0.78, start_angle=PI * 1.15, angle=-PI * 1.3, arc_center=c,
                stroke_color=GREY, stroke_width=6)
    b_in = c + radius * 0.62 * UP
    b_out = c + radius * 0.94 * UP
    base_tick = Line(b_in, b_out, color=TEXT, stroke_width=3.5)
    base_lab = T("baseline", 22, GREY).next_to(face, UP, buff=0.10)

    def mk_arc():
        v = float(np.clip(p_tracker.get_value(), 0.02, 1.0))
        return Arc(radius=radius * 0.78, start_angle=PI * 1.15, angle=-PI * 1.3 * v, arc_center=c,
                   stroke_color=TEXT, stroke_width=6)

    def mk_needle():
        v = float(np.clip(p_tracker.get_value(), 0.02, 1.0))
        ang = PI * 1.15 - PI * 1.3 * v
        tip = c + radius * 0.68 * np.array([np.cos(ang), np.sin(ang), 0.0])
        return VGroup(
            Line(c, tip, color=TEXT, stroke_width=4.5),
            Dot(c, radius=0.065, color=TEXT),
        )

    val_arc = always_redraw(mk_arc)
    needle = always_redraw(mk_needle)
    return VGroup(face, track, base_tick, base_lab, val_arc, needle), face


# ------------------------------------------------------------------ carried lung world
class LungWorld:
    """Three-unit lung model with computed flow diversion and oxygen content loading."""

    UX = (-2.3, 0.0, 2.3)

    def __init__(self, center=(0.0, -0.05), scale=1.0, vent=(1.0, 1.0, 1.0),
                 constrict=(0.0, 0.0, 0.0), dim=(0.0, 0.0, 0.0),
                 o2_level=1.0, show_o2_dots=True, rings_grey=False,
                 show_air_manifold=False, trunk_left_local=-5.1, seed=SEED):
        self.center = np.array([center[0], center[1], 0.0], dtype=float)
        self.scale = scale
        self.vent = [ValueTracker(v) for v in vent]
        self.constrict = [ValueTracker(c) for c in constrict]
        self.dim = [ValueTracker(d) for d in dim]
        self.o2_level = ValueTracker(o2_level)
        self.show_o2_dots = show_o2_dots
        self.rings_grey = rings_grey
        self.show_air_manifold = show_air_manifold
        self.trunk_left_local = trunk_left_local
        self.t = 0.0
        self.rng = np.random.default_rng(seed)

        self.root = VGroup()
        self._build()

    def _to_world(self, x, y):
        return self.center + self.scale * np.array([x, y, 0.0])

    def _flow_shares(self):
        g = np.array([max(0.14, 1.0 - 0.86 * self.constrict[i].get_value()) for i in range(3)])
        return g / g.sum()

    def _o2_prob(self, i, shares):
        v = self.vent[i].get_value() * self.o2_level.get_value()
        q = shares[i] * 3.0
        vq = v / max(q, 0.12)
        return float(np.clip(vq / (vq + 0.28), 0.15, 0.98))

    def _build(self):
        s = self.scale
        # 1. Outer rounded lung contour (~70% frame height when scale=1.0)
        outline = RoundedRectangle(
            corner_radius=0.85 * s, width=8.8 * s, height=5.3 * s,
            stroke_color=GREY, stroke_width=4.2, fill_color=GREY, fill_opacity=0.07,
        ).move_to(self._to_world(0.05, 0.12))
        self.outline = outline
        self.root.add(outline)

        # 2. Static vessel backbone
        trunk_y = -1.88
        vein_y = 2.18
        tx0 = self.trunk_left_local
        trunk = Line(self._to_world(tx0, trunk_y), self._to_world(2.3, trunk_y),
                     color=RED, stroke_width=10 * s, stroke_opacity=0.45)
        trunk_tip = Arrow(
            self._to_world(tx0 - 0.25, trunk_y), self._to_world(tx0 + 0.75, trunk_y),
            buff=0, color=RED, stroke_width=9 * s, max_tip_length_to_length_ratio=0.28,
        )
        vein = Line(self._to_world(-1.45, vein_y), self._to_world(5.15, vein_y),
                    color=RED, stroke_width=10 * s, stroke_opacity=0.45)
        vein_tip = Arrow(
            self._to_world(4.4, vein_y), self._to_world(5.45, vein_y),
            buff=0, color=RED, stroke_width=9 * s, max_tip_length_to_length_ratio=0.28,
        )
        self.trunk, self.vein = trunk, vein
        self.root.add(trunk, trunk_tip, vein, vein_tip)

        # Optional air manifold for cat/pump experiment (s04-s07)
        if self.show_air_manifold:
            man_y = 1.84
            man_bar = Line(self._to_world(-2.45, man_y), self._to_world(2.15, man_y),
                           color=BLUE, stroke_width=5.0 * s)
            self.air_manifold = man_bar
            self.root.add(self.air_manifold)

        # 3. Three lung units: alveolus boxes, air arrows, vessel branches, orange muscle rings
        self.alveoli = []
        self.air_arrows = []
        self.rings = []
        self.branches = []

        for i, ux in enumerate(self.UX):
            alv = RoundedRectangle(
                corner_radius=0.26 * s, width=1.36 * s, height=1.24 * s,
                stroke_color=BLUE, stroke_width=4.5, fill_color=BLUE, fill_opacity=0.18,
            ).move_to(self._to_world(ux, 0.20))
            self.alveoli.append(alv)
            self.root.add(alv)

            # Breathing pulse on alveolus fill & subtle breath glow
            def make_alv_up(idx):
                def u(m):
                    d = self.dim[idx].get_value()
                    v = self.vent[idx].get_value()
                    o2 = float(np.clip(self.o2_level.get_value(), 0.45, 1.25))
                    breath = 1.0 + 0.14 * v * np.sin(2.4 * self.t + idx * 0.15)
                    op_s = max(0.32, 1.0 - 0.56 * d) * min(1.0, 0.55 + 0.45 * o2)
                    op_f = max(0.03, 0.18 * (1.0 - 0.72 * d)) * min(1.2, o2) * breath
                    m.set_stroke(opacity=op_s)
                    m.set_fill(opacity=op_f)
                return u
            alv.add_updater(make_alv_up(i))

            def make_air(idx, xpos):
                def mk():
                    v = float(np.clip(self.vent[idx].get_value(), 0.12, 1.0))
                    o2 = float(np.clip(self.o2_level.get_value(), 0.4, 1.2))
                    breath = np.sin(2.4 * self.t + idx * 0.15)
                    top_y = 1.80 if self.show_air_manifold else 1.84
                    bot_y = 0.88 - 0.05 * v * breath
                    shaft_w = max(2.4, 9.0 * v) * self.scale
                    col = interpolate_color(ManimColor(GREY), ManimColor(BLUE), float(np.clip(0.35 + 0.65 * o2, 0.35, 1.0)))
                    op = float(np.clip(0.45 + 0.55 * v, 0.4, 1.0)) * float(np.clip(0.5 + 0.5 * o2, 0.45, 1.0))
                    p0 = self._to_world(xpos - 0.15, top_y)
                    p1 = self._to_world(xpos - 0.15, bot_y)
                    a = Arrow(p0, p1, buff=0, color=col, stroke_width=shaft_w,
                              tip_length=0.24 * self.scale * (0.65 + 0.35 * v))
                    a.set_opacity(op)
                    return a
                return always_redraw(mk)

            air_mob = make_air(i, ux)
            self.air_arrows.append(air_mob)
            self.root.add(air_mob)

            # Outflow routed neatly outside the alveolus box (no corner crossing)
            def make_branch(idx, xpos):
                def mk():
                    c = float(np.clip(self.constrict[idx].get_value(), 0.0, 1.0))
                    w_in = max(3.0, 9.5 * (1.0 - 0.65 * c)) * self.scale
                    p_trunk = self._to_world(xpos, -1.88)
                    p_ring = self._to_world(xpos, -0.60)
                    in_line = Line(p_trunk, p_ring, color=RED, stroke_width=w_in, stroke_opacity=0.55)
                    pts = [
                        self._to_world(xpos, -0.60),
                        self._to_world(xpos + 0.85, -0.60),
                        self._to_world(xpos + 0.85, 0.72),
                        self._to_world(xpos + 0.85, 2.18),
                    ]
                    out_line = VMobject(stroke_color=RED, stroke_width=max(3.0, w_in * 0.92), stroke_opacity=0.48)
                    out_line.set_points_as_corners(pts)
                    return VGroup(in_line, out_line)
                return always_redraw(mk)

            br = make_branch(i, ux)
            self.branches.append(br)
            self.root.add(br)

            def make_ring(idx, xpos):
                def mk():
                    c = float(np.clip(self.constrict[idx].get_value(), 0.0, 1.0))
                    w = (0.68 - 0.36 * c) * self.scale
                    h = (0.32 + 0.06 * c) * self.scale
                    col = GREY if self.rings_grey else ORANGE
                    sw = (4.5 if self.rings_grey else 6.0 + 3.0 * c) * self.scale
                    fo = 0.10 if self.rings_grey else (0.20 + 0.25 * c)
                    return Ellipse(width=w, height=h, stroke_color=col, stroke_width=sw,
                                   fill_color=col, fill_opacity=fo).move_to(self._to_world(xpos, -1.20))
                return always_redraw(mk)

            rg = make_ring(i, ux)
            self.rings.append(rg)
            self.root.add(rg)

        # 4. Computed blood & oxygen particles (persistent pool)
        self.n_dots = 30
        self.particles = []
        self._accum = np.zeros(3)
        self.blood_dots = VGroup()
        self.o2_dots = VGroup()

        for k in range(self.n_dots):
            b = k % 3
            s_init = (k / self.n_dots) * 15.8
            bd = Dot(radius=0.088 * s, color=RED)
            od = Dot(radius=0.056 * s, color=YELLOW)
            if not self.show_o2_dots:
                od.set_opacity(0)
            self.particles.append({
                "branch": b,
                "s": s_init,
                "o2_on": self.rng.random() < self._o2_prob(b, self._flow_shares()),
                "passed_junction": False,
            })
            self.blood_dots.add(bd)
            self.o2_dots.add(od)

        self.root.add(self.blood_dots, self.o2_dots)
        self._step_particles(0.0)
        self.root.add_updater(self._updater)

    def _pick_branch(self, shares):
        self._accum += shares
        idx = int(np.argmax(self._accum))
        self._accum[idx] -= 1.0
        return idx

    def _path_point(self, branch, s_dist):
        ux = self.UX[branch]
        tx0 = self.trunk_left_local
        segs = [
            ((tx0, -1.88), (ux, -1.88)),
            ((ux, -1.88), (ux, -0.60)),
            ((ux, -0.60), (ux + 0.85, -0.60)),
            ((ux + 0.85, -0.60), (ux + 0.85, 0.72)),
            ((ux + 0.85, 0.72), (ux + 0.85, 2.18)),
            ((ux + 0.85, 2.18), (5.15, 2.18)),
        ]
        rem = s_dist
        for a, b in segs:
            ax, ay = a
            bx, by = b
            L = float(np.hypot(bx - ax, by - ay))
            if rem <= L or b == segs[-1][1]:
                f = float(np.clip(rem / max(L, 1e-6), 0.0, 1.0))
                return self._to_world(ax + f * (bx - ax), ay + f * (by - ay)), L
            rem -= L
        return self._to_world(5.15, 2.18), 1.0

    def _total_len(self, branch):
        ux = self.UX[branch]
        return (ux - self.trunk_left_local) + 1.28 + 0.85 + 1.32 + 1.46 + (5.15 - (ux + 0.85))

    def _step_particles(self, dt):
        shares = self._flow_shares()
        base_speed = 2.45
        for k, p in enumerate(self.particles):
            b = p["branch"]
            ux = self.UX[b]
            trunk_len = ux - self.trunk_left_local
            old_s = p["s"]
            in_branch = trunk_len < old_s < (trunk_len + 4.91)
            spd = base_speed * (0.65 + 1.1 * shares[b] if in_branch else 1.0)
            p["s"] += spd * dt

            if not p["passed_junction"] and old_s <= (self.UX[0] - self.trunk_left_local) < p["s"]:
                p["passed_junction"] = True
                new_b = self._pick_branch(shares)
                if new_b != b:
                    p["branch"] = new_b
                    b = new_b
                    p["o2_on"] = self.rng.random() < self._o2_prob(b, shares)

            tot = self._total_len(b)
            if p["s"] >= tot:
                p["s"] -= tot
                p["branch"] = self._pick_branch(shares)
                b = p["branch"]
                p["passed_junction"] = False
                p["o2_on"] = self.rng.random() < self._o2_prob(b, shares)

            pos, _ = self._path_point(b, p["s"])
            bd = self.blood_dots[k]
            od = self.o2_dots[k]
            bd.move_to(pos)
            trunk_l = self.UX[b] - self.trunk_left_local
            if self.show_o2_dots and p["o2_on"] and p["s"] > trunk_l + 2.13:
                od.move_to(pos + UP * 0.06 * self.scale + RIGHT * 0.05 * self.scale)
                od.set_opacity(1.0)
            else:
                od.move_to(pos)
                od.set_opacity(0.0)

    def _updater(self, mob, dt):
        self.t += dt
        self._step_particles(dt)


# ------------------------------------------------------------------ scenes
class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        self.world = LungWorld(center=(0.0, -0.05), scale=1.0, show_o2_dots=True)
        tag = scope_tag("schematic")
        self.add(tag)
        self.play(FadeIn(self.world.root), run_time=0.8)

        self.at("unit short of air")
        self.play(
            self.world.vent[0].animate.set_value(0.18),
            self.world.dim[0].animate.set_value(0.75),
            run_time=1.3,
        )

        self.at("the mix pays")
        vein_hl = SurroundingRectangle(
            Line(self.world._to_world(2.8, 2.18), self.world._to_world(5.2, 2.18)),
            buff=0.22, color=YELLOW, stroke_width=3, corner_radius=0.14,
        )
        self.play(FadeIn(vein_hl), run_time=0.4)
        self.play(FadeOut(vein_hl), run_time=0.6)

        self.at("can the lung")
        q_txt = T("Can the lung fight back?", size=36, color=TEXT).move_to([0.0, HEAD_Y, 0])
        self.play(
            FadeIn(q_txt, shift=DOWN * 0.1),
            Indicate(self.world.alveoli[0], color=YELLOW, scale_factor=1.06),
            run_time=0.9,
        )
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        self.world = LungWorld(center=(0.0, -0.05), scale=1.0, vent=(0.18, 1.0, 1.0),
                               dim=(0.75, 0.0, 0.0), show_o2_dots=True)
        q_txt = T("Can the lung fight back?", size=36, color=TEXT).move_to([0.0, HEAD_Y, 0])
        tag = scope_tag("schematic")
        self.add(self.world.root, q_txt, tag)

        title = T("Steering Blood Toward Air", size=44, font=TITLE_FONT, color=TEXT).move_to([0.0, HEAD_Y, 0])
        rule = Line(LEFT * 2.1, RIGHT * 2.1, color=GOLD, stroke_width=3.5).next_to(title, DOWN, buff=0.12)
        self.play(FadeOut(q_txt, run_time=0.45))
        self.play(FadeIn(title, shift=DOWN * 0.08), Create(rule), run_time=0.85)
        self.finish()


class S02Opposite(SpokenScene):
    def construct(self):
        self.world = LungWorld(center=(0.0, -0.05), scale=1.0, vent=(0.18, 1.0, 1.0),
                               dim=(0.75, 0.0, 0.0), show_o2_dots=False)
        tag = scope_tag("schematic")
        self.add(self.world.root, tag)
        self.wait(0.25)

        self.at("working muscle")
        lung_right = LungWorld(center=(2.4, -0.05), scale=0.72, vent=(0.18, 1.0, 1.0),
                               dim=(0.75, 0.0, 0.0), show_o2_dots=False)

        muscle_box = RoundedRectangle(corner_radius=0.3, width=3.1, height=2.2,
                                      stroke_color=PINK, stroke_width=4, fill_color=PINK, fill_opacity=0.14)
        muscle_box.move_to([-3.6, 0.2, 0])
        muscle_lab = T("muscle", size=30, color=PINK).next_to(muscle_box, UP, buff=0.2)

        m_w = ValueTracker(0.50)
        m_vessel = always_redraw(lambda: Line(
            [-3.6, -1.65, 0], [-3.6, 1.25, 0], color=RED,
            stroke_width=8 + 10 * (m_w.get_value() - 0.5), stroke_opacity=0.55,
        ))
        m_ring = always_redraw(lambda: Ellipse(
            width=0.58 + 0.55 * (m_w.get_value() - 0.5), height=0.30,
            stroke_color=ORANGE, stroke_width=6, fill_color=ORANGE, fill_opacity=0.22,
        ).move_to([-3.6, -0.95, 0]))

        m_dots = VGroup(*[Dot(radius=0.072, color=RED) for _ in range(7)])
        m_s = np.linspace(0.0, 2.9, 7, endpoint=False)

        def m_dot_up(mob, dt):
            spd = 1.6 + 2.4 * (m_w.get_value() - 0.5)
            for idx, d in enumerate(mob):
                m_s[idx] = (m_s[idx] + spd * dt) % 2.9
                x_off = (0.12 * np.sin(idx * 2.1)) * (1.0 + 0.9 * (m_w.get_value() - 0.5))
                d.move_to([-3.6 + x_off, -1.65 + m_s[idx], 0])

        m_dots.add_updater(m_dot_up)
        m_grp = VGroup(muscle_box, muscle_lab, m_vessel, m_ring, m_dots)

        self.play(FadeOut(self.world.root, run_time=0.35))
        self.world = lung_right
        self.play(FadeIn(self.world.root), FadeIn(m_grp), run_time=0.65)

        self.at("widens")
        widen_tag = chip("low oxygen: widens", ORANGE, size=26).next_to(m_vessel, DOWN, buff=0.24)
        self.play(m_w.animate.set_value(1.25), FadeIn(widen_tag), run_time=1.0)

        self.at("the opposite")
        lung_full = LungWorld(center=(0.0, -0.05), scale=1.0, vent=(0.18, 1.0, 1.0),
                              dim=(0.75, 0.0, 0.0), show_o2_dots=False)
        self.play(FadeOut(m_grp), FadeOut(widen_tag), FadeOut(self.world.root), run_time=0.45)
        self.world = lung_full
        self.play(FadeIn(self.world.root), run_time=0.55)

        self.at("they narrow")
        # Placed cleanly BELOW the lung outline under the LEFT unit so it never touches the outline
        narrow_tag = chip("low oxygen: narrows", ORANGE, size=26).move_to([-2.3, -3.05, 0])
        self.play(
            self.world.constrict[0].animate.set_value(0.95),
            FadeIn(narrow_tag),
            run_time=1.0,
        )

        self.at("blood leaves")
        self.play(self.world.constrict[0].animate.set_value(1.0), run_time=0.5)
        self.finish()


class S03RatioUp(SpokenScene):
    def construct(self):
        self.world = LungWorld(center=(0.0, -0.05), scale=1.0, vent=(0.18, 1.0, 1.0),
                               constrict=(0.65, 0.0, 0.0), dim=(0.75, 0.0, 0.0), show_o2_dots=False)
        tag = scope_tag("schematic")
        self.add(self.world.root, tag)

        self.at("follow the poorly")
        self.play(FadeOut(self.world.root, run_time=0.35))
        self.world = LungWorld(center=(-2.15, -0.05), scale=0.85, vent=(0.18, 1.0, 1.0),
                               constrict=(0.65, 0.0, 0.0), dim=(0.75, 0.0, 0.0), show_o2_dots=False)
        focus_box = SurroundingRectangle(
            VGroup(self.world.alveoli[0], self.world.rings[0]),
            buff=0.38, color=YELLOW, stroke_width=2.5, corner_radius=0.22,
        )
        self.play(FadeIn(self.world.root), FadeIn(focus_box), run_time=0.6)

        q_val = ValueTracker(0.68)
        r_val = ValueTracker(0.24)

        v_bar = RoundedRectangle(corner_radius=0.08, width=0.95, height=0.42,
                                 stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.8)
        v_bar.move_to([3.20, 0.85, 0])
        v_lab = T("ventilation", 28, BLUE).next_to(v_bar, UP, buff=0.14)
        frac_line = Line([2.10, 0.35, 0], [4.30, 0.35, 0], color=TEXT, stroke_width=4)

        q_bar = always_redraw(lambda: RoundedRectangle(
            corner_radius=0.08, width=max(0.32, 2.1 * q_val.get_value()), height=0.42,
            stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.8,
        ).move_to([3.20, -0.15, 0]))
        q_lab = T("perfusion", 28, RED).move_to([3.20, -0.70, 0])

        r_scale = ratio_scale(r_val, pos=[5.95, 0.35, 0], height=2.2, show_label=False)
        r_tag = T("ratio", 28, YELLOW).move_to([4.95, 0.35, 0])
        frac_grp = VGroup(v_bar, v_lab, frac_line, q_bar, q_lab, r_scale, r_tag)
        self.play(FadeIn(frac_grp), run_time=0.7)

        self.at("air is unchanged")
        self.play(
            Indicate(v_bar, color=BLUE, scale_factor=1.08),
            Indicate(self.world.air_arrows[0], color=BLUE, scale_factor=1.08),
            run_time=0.9,
        )

        self.at("less blood")
        self.play(
            self.world.constrict[0].animate.set_value(1.0),
            q_val.animate.set_value(0.24),
            run_time=1.3,
        )

        self.at("ventilation over")
        self.play(Indicate(v_bar, color=BLUE, scale_factor=1.06), run_time=0.6)

        self.at("less perfusion")
        self.play(Indicate(q_bar, color=RED, scale_factor=1.08), run_time=0.6)

        self.at("larger ratio")
        self.play(r_val.animate.set_value(0.56), run_time=1.2)

        self.at("pushed back up")
        self.play(Indicate(r_scale, color=YELLOW, scale_factor=1.06), run_time=0.8)

        self.at("better ventilated units")
        lung_out = LungWorld(center=(0.0, -0.05), scale=1.0, vent=(0.18, 1.0, 1.0),
                             constrict=(1.0, 0.0, 0.0), dim=(0.75, 0.0, 0.0), show_o2_dots=False)
        self.play(FadeOut(frac_grp), FadeOut(focus_box), FadeOut(self.world.root), run_time=0.45)
        self.world = lung_out
        self.play(FadeIn(self.world.root), run_time=0.55)
        self.finish()


def _s04_layout_params():
    return dict(center=(1.65, -0.15), scale=0.82, show_o2_dots=False,
                rings_grey=True, show_air_manifold=True, trunk_left_local=-8.6)


class S04Cat(SpokenScene):
    def construct(self):
        self.world = LungWorld(**_s04_layout_params())
        tag = scope_tag("schematic")
        cat_tag = chip("cat, 1946", TEXT, size=26).move_to([-5.35, 3.20, 0])
        ring_q = T("?", 28, TEXT).move_to(self.world._to_world(0.0, -1.20) + RIGHT * 0.48)

        # Left column at x=-5.15 leaves x=-4.0..-1.92 completely clear for nerves
        man_world_y = self.world._to_world(-2.45, 1.84)[1]
        pump_box = RoundedRectangle(corner_radius=0.14, width=1.40, height=0.72,
                                    stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.16)
        pump_box.move_to([-5.15, man_world_y, 0])
        pump_lab = T("pump", 26, TEXT).move_to(pump_box)
        pump_feed = Line(pump_box.get_right(), self.world._to_world(-2.45, 1.84),
                         color=BLUE, stroke_width=5.0 * 0.82)
        pump_grp = VGroup(pump_box, pump_lab, pump_feed)
        bob(pump_box, amp=0.04, speed=2.4)
        bob(pump_lab, amp=0.04, speed=2.4)

        gas_air = chip("air", BLUE, size=26).move_to([-5.15, man_world_y + 0.92, 0])

        p_val = ValueTracker(0.50)
        gauge_grp, gauge_face = pressure_gauge(p_val, center=[-5.15, -0.35, 0], radius=0.76)
        trunk_world_y = self.world._to_world(0.0, -1.88)[1]
        gauge_stem = Line(gauge_face.get_bottom(), [-5.15, trunk_world_y, 0], color=TEXT, stroke_width=4)
        gauge_title = fit_text("pulmonary artery pressure", max_w=2.8, size=26, color=TEXT, max_lines=2)
        gauge_title.move_to([-5.05, trunk_world_y - 0.58, 0])

        self.add(self.world.root, tag)
        self.play(FadeIn(cat_tag), FadeIn(ring_q), run_time=0.7)

        self.at("ventilated")
        self.play(FadeIn(pump_grp), FadeIn(gas_air), run_time=0.7)

        self.at("pulmonary arterial pressure")
        self.play(FadeIn(gauge_stem), FadeIn(gauge_grp), FadeIn(gauge_title), run_time=0.8)

        self.at("ten and a half")
        gas_low = chip("10.5% oxygen", BLUE, size=26).move_to(gas_air)
        self.play(
            swap(gas_air, gas_low, run_time=0.55),
            self.world.o2_level.animate.set_value(0.52),
        )

        self.at("strongly raised")
        self.play(p_val.animate.set_value(0.88), run_time=1.1)

        self.at("pure oxygen")
        gas_pure = chip("100% oxygen", BLUE, size=26).move_to(gas_air)
        self.play(
            swap(gas_low, gas_pure, run_time=0.55),
            self.world.o2_level.animate.set_value(1.15),
            p_val.animate.set_value(0.38),
        )
        self.finish()


def _s05_base(o2_level=1.15, cover=False, cut_vagus=False, remove_stellate=False):
    world = LungWorld(**_s04_layout_params())
    world.o2_level.set_value(o2_level)
    cat_tag = chip("cat, 1946", TEXT, size=26).move_to([-5.35, 3.20, 0])
    ring_q = T("?", 28, TEXT).move_to(world._to_world(0.0, -1.20) + RIGHT * 0.48)

    man_world_y = world._to_world(-2.45, 1.84)[1]
    pump_box = RoundedRectangle(corner_radius=0.14, width=1.40, height=0.72,
                                stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.16)
    pump_box.move_to([-5.15, man_world_y, 0])
    pump_lab = T("pump", 26, TEXT).move_to(pump_box)
    pump_feed = Line(pump_box.get_right(), world._to_world(-2.45, 1.84),
                     color=BLUE, stroke_width=5.0 * 0.82)
    pump_grp = VGroup(pump_box, pump_lab, pump_feed)
    bob(pump_box, amp=0.04, speed=2.4)
    bob(pump_lab, amp=0.04, speed=2.4)

    gas_chip = chip("10.5% oxygen" if o2_level < 0.7 else "100% oxygen", BLUE, size=26).move_to(
        [-5.15, man_world_y + 0.92, 0]
    )
    p_val = ValueTracker(0.38 if o2_level >= 0.7 else 0.88)
    gauge_grp, gauge_face = pressure_gauge(p_val, center=[-5.15, -0.35, 0], radius=0.76)
    trunk_world_y = world._to_world(0.0, -1.88)[1]
    gauge_stem = Line(gauge_face.get_bottom(), [-5.15, trunk_world_y, 0], color=TEXT, stroke_width=4)
    gauge_title = fit_text("pulmonary artery pressure", max_w=2.8, size=26, color=TEXT, max_lines=2)
    gauge_title.move_to([-5.05, trunk_world_y - 0.58, 0])

    cov = VGroup()
    if cover:
        c_disc = Circle(radius=0.74, color=GREY, stroke_width=3.5, fill_color=BG, fill_opacity=0.96).move_to(gauge_face)
        c_q = T("?", 48, YELLOW).move_to(c_disc)
        cov = VGroup(c_disc, c_q)

    # Vagus & stellate nerves cleanly in clear band above lung (y=2.58, lung top=2.12, question y=3.25)
    vagus_lab = T("vagus nerves", 26, TEXT).move_to([-2.40, 2.58, 0])
    v_start = vagus_lab.get_bottom() + DOWN * 0.08
    v_mid = np.array([-1.95, 1.85, 0])
    v_end = world._to_world(-1.5, 0.9)
    vagus_top = Line(v_start, v_mid, color=GREY, stroke_width=3.5)
    vagus_bot = Line(v_mid, v_end, color=GREY, stroke_width=3.5)
    if cut_vagus:
        vagus_top.shift(LEFT * 0.04 + UP * 0.04)
        vagus_bot.set_opacity(0.0)
        snip = cross_mark(YELLOW, size=0.25, stroke=4).move_to(v_mid)
        vagus_grp = VGroup(vagus_top, snip, vagus_lab)
    else:
        vagus_grp = VGroup(vagus_top, vagus_bot, vagus_lab)

    stellate_grp = VGroup()
    if not remove_stellate:
        s_lab = T("stellate ganglia", 26, TEXT).move_to([0.55, 2.58, 0])
        s_start = s_lab.get_bottom() + DOWN * 0.08
        s_end = world._to_world(-0.8, 0.65)
        s_line = Line(s_start, s_end, color=GREY, stroke_width=3.5)
        s_knot = Dot(s_start + DOWN * 0.35 + RIGHT * 0.03, radius=0.10, color=GREY)
        stellate_grp = VGroup(s_line, s_knot, s_lab)

    return world, cat_tag, ring_q, pump_grp, gas_chip, p_val, gauge_grp, gauge_stem, gauge_title, cov, vagus_grp, stellate_grp


class S05Predict(SpokenScene):
    def construct(self):
        world, cat_tag, ring_q, pump_grp, gas_pure, p_val, gauge_grp, gauge_stem, gauge_title, _, _, _ = _s05_base(o2_level=1.15)
        tag = scope_tag("schematic")
        self.add(world.root, cat_tag, ring_q, pump_grp, gas_pure, gauge_stem, gauge_grp, gauge_title, tag)

        self.at("nerves")
        vagus_lab = T("vagus nerves", 26, TEXT).move_to([-2.40, 2.58, 0])
        v_start = vagus_lab.get_bottom() + DOWN * 0.08
        v_mid = np.array([-1.95, 1.85, 0])
        v_end = world._to_world(-1.5, 0.9)
        vagus_top = Line(v_start, v_mid, color=GREY, stroke_width=3.5)
        vagus_bot = Line(v_mid, v_end, color=GREY, stroke_width=3.5)

        s_lab = T("stellate ganglia", 26, TEXT).move_to([0.55, 2.58, 0])
        s_start = s_lab.get_bottom() + DOWN * 0.08
        s_end = world._to_world(-0.8, 0.65)
        s_line = Line(s_start, s_end, color=GREY, stroke_width=3.5)
        s_knot = Dot(s_start + DOWN * 0.35 + RIGHT * 0.03, radius=0.10, color=GREY)

        vp = Dot(radius=0.06, color=TEXT)
        sp = Dot(radius=0.06, color=TEXT)
        vp.t_p = 0.0
        sp.t_p = 0.0
        vp.add_updater(lambda m, dt: (setattr(m, "t_p", (m.t_p + dt * 0.9) % 1.0), m.move_to(interpolate(v_start, v_end, m.t_p))))
        sp.add_updater(lambda m, dt: (setattr(m, "t_p", (m.t_p + dt * 0.8) % 1.0), m.move_to(interpolate(s_start, s_end, m.t_p))))

        self.play(
            Create(vagus_top), Create(vagus_bot), FadeIn(vagus_lab),
            Create(s_line), FadeIn(s_knot), FadeIn(s_lab),
            FadeIn(vp), FadeIn(sp),
            run_time=1.0,
        )

        self.at("cut the vagus")
        vp.clear_updaters()
        snip = cross_mark(YELLOW, size=0.25, stroke=4).move_to(v_mid)
        self.play(
            FadeOut(vp),
            FadeIn(snip),
            vagus_top.animate.shift(LEFT * 0.04 + UP * 0.04),
            vagus_bot.animate.shift(DOWN * 0.35).set_opacity(0.0),
            run_time=0.8,
        )

        self.at("removed the stellate")
        sp.clear_updaters()
        self.play(FadeOut(sp), FadeOut(s_line), FadeOut(s_knot), FadeOut(s_lab), run_time=0.8)

        self.at("if nerves carried")
        gas_low = chip("10.5% oxygen", BLUE, size=26).move_to(gas_pure)
        c_disc = Circle(radius=0.74, color=GREY, stroke_width=3.5, fill_color=BG, fill_opacity=0.96).move_to(gauge_grp[0])
        c_q = T("?", 48, YELLOW).move_to(c_disc)
        cov = VGroup(c_disc, c_q)
        self.play(
            swap(gas_pure, gas_low, run_time=0.5),
            world.o2_level.animate.set_value(0.52),
            FadeIn(cov),
        )

        self.at("did it")
        q_card = question_card("Does the rise vanish?", y=3.25, color=YELLOW, size=34)
        q_card.move_to([0.7, 3.25, 0])
        self.play(FadeIn(q_card, shift=DOWN * 0.1), run_time=0.6)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "Does the rise vanish?"
    CARD = {"y": 3.25, "color": YELLOW, "size": 34}
    RING_AT = (5.85, 3.15, 0)
    SECONDS = 4.5

    def backdrop(self):
        world, cat_tag, ring_q, pump_grp, gas_chip, _, gauge_grp, gauge_stem, gauge_title, cov, vagus_grp, _ = _s05_base(
            o2_level=0.52, cover=True, cut_vagus=True, remove_stellate=True,
        )
        return VGroup(world.root, cat_tag, ring_q, pump_grp, gas_chip, gauge_stem, gauge_grp, gauge_title, cov, vagus_grp, scope_tag("schematic"))

    def construct(self):
        self.add(self.backdrop())
        qc = question_card(self.QUESTION, self.OPTIONS, chips_at=self.CHIPS_AT, **self.CARD)
        qc.move_to([0.7, 3.25, 0])
        self.add(qc)
        ring, run = countdown(self.SECONDS, center=self.RING_AT)
        self.add(ring)
        self.play(run)
        self.finish()


class S07Answer(SpokenScene):
    def construct(self):
        world, cat_tag, ring_q, pump_grp, gas_chip, p_val, gauge_grp, gauge_stem, gauge_title, cov, vagus_grp, _ = _s05_base(
            o2_level=0.52, cover=True, cut_vagus=True, remove_stellate=True,
        )
        q_card = question_card("Does the rise vanish?", y=3.25, color=YELLOW, size=34)
        q_card.move_to([0.7, 3.25, 0])
        tag = scope_tag("schematic")
        self.add(world.root, cat_tag, ring_q, pump_grp, gas_chip, gauge_stem, gauge_grp, gauge_title, cov, vagus_grp, q_card, tag)

        self.at("the rise survived")
        self.play(FadeOut(q_card), FadeOut(cov), run_time=0.7)

        self.at("acting directly on")
        world.rings_grey = False
        direct_tag = chip("in part: direct", ORANGE, size=26).move_to([1.65, -2.95, 0])
        self.play(
            FadeOut(ring_q),
            *[world.constrict[i].animate.set_value(0.45) for i in range(3)],
            FadeIn(direct_tag),
            run_time=1.0,
        )

        self.at("keep that hedge")
        self.play(Indicate(direct_tag, color=YELLOW, scale_factor=1.08), run_time=0.8)

        self.at("not a resistance")
        p_note = chip("pressure is not resistance", TEXT, size=26).move_to([-4.25, -3.15, 0])
        self.play(FadeIn(p_note), run_time=0.7)

        self.at("flow and outflow")
        trunk_world_y = world._to_world(0.0, -1.88)[1]
        flow_q = T("flow?", 26, TEXT).move_to([-2.75, trunk_world_y - 0.40, 0])
        out_q = T("outflow pressure?", 26, TEXT).move_to([4.15, 2.52, 0])
        self.play(FadeIn(flow_q), FadeIn(out_q), run_time=0.8)

        self.at("hypoxia test")
        whole_tag = chip("whole lung, not regions", TEXT, size=26).move_to([1.65, 3.20, 0])
        self.play(
            *[world.dim[i].animate.set_value(0.55) for i in range(3)],
            FadeIn(whole_tag),
            run_time=0.9,
        )
        self.finish()


class S08Idea(SpokenScene):
    def construct(self):
        world_exp, cat_tag, _, pump_grp, gas_chip, _, gauge_grp, gauge_stem, gauge_title, _, vagus_grp, _ = _s05_base(
            o2_level=0.52, cover=False, cut_vagus=True, remove_stellate=True,
        )
        world_exp.rings_grey = False
        for i in range(3):
            world_exp.constrict[i].set_value(0.45)
            world_exp.dim[i].set_value(0.55)
        direct_tag = chip("in part: direct", ORANGE, size=26).move_to([1.65, -2.95, 0])
        p_note = chip("pressure is not resistance", TEXT, size=26).move_to([-4.25, -3.15, 0])
        whole_tag = chip("whole lung, not regions", TEXT, size=26).move_to([1.65, 3.20, 0])
        props = VGroup(cat_tag, pump_grp, gas_chip, gauge_grp, gauge_stem, gauge_title, vagus_grp, direct_tag, p_note, whole_tag)
        tag = scope_tag("schematic")

        self.add(world_exp.root, props, tag)
        self.world = LungWorld(center=(0.0, -0.05), scale=1.0, vent=(0.18, 1.0, 1.0),
                               constrict=(0.0, 0.0, 0.0), dim=(0.0, 0.0, 0.0), show_o2_dots=False)
        self.play(FadeOut(props), FadeOut(world_exp.root), run_time=0.55)
        self.play(FadeIn(self.world.root), run_time=0.55)

        self.at("runs short of")
        self.play(self.world.dim[0].animate.set_value(0.75), run_time=0.8)

        self.at("small arteries narrow")
        self.play(self.world.constrict[0].animate.set_value(1.0), run_time=1.0)

        self.at("blood shifts")
        self.play(Indicate(self.world.alveoli[1], color=BLUE, scale_factor=1.04),
                  Indicate(self.world.alveoli[2], color=BLUE, scale_factor=1.04), run_time=0.8)

        self.at("local correction")
        banner = T("less oxygen here, less blood", size=34, color=YELLOW).move_to([0.0, HEAD_Y, 0])
        arr = Arrow(banner.get_bottom() + LEFT * 2.2 + DOWN * 0.05,
                    self.world._to_world(-2.3, 1.95),
                    buff=0, color=YELLOW, stroke_width=3.5, tip_length=0.2)
        self.play(FadeIn(banner), Create(arr), run_time=0.65)
        self.finish()


def _build_muscle_cell(squeeze, k_open, vm_val, ca_open, label_pos=(-2.15, -0.10), seed=SEED):
    """Smooth muscle cell cartoon (no molecular structures) driven by ValueTrackers."""
    rng = np.random.default_rng(seed)

    cell_body = always_redraw(lambda: RoundedRectangle(
        corner_radius=1.05,
        width=7.6 - 1.3 * squeeze.get_value(),
        height=3.2 + 0.7 * squeeze.get_value(),
        stroke_color=ORANGE, stroke_width=5, fill_color=ORANGE, fill_opacity=0.16,
    ).move_to([-0.3, -0.05, 0]))

    cell_lab = T("smooth\nmuscle cell", 28, ORANGE, line_spacing=0.9).move_to([label_pos[0], label_pos[1], 0])

    # Potassium door on upper edge (center x=-0.15)
    def _mk_k_gate():
        ky = -0.05 + (3.2 + 0.7 * squeeze.get_value()) / 2
        ko = k_open.get_value()
        return VGroup(
            Line([-0.60, ky, 0], [-0.60 + 0.42 * (1.0 - ko), ky + 0.35 * ko, 0],
                 color=TEXT, stroke_width=6),
            Line([0.30, ky, 0], [0.30 - 0.42 * (1.0 - ko), ky + 0.35 * ko, 0],
                 color=TEXT, stroke_width=6),
        )

    k_gate = always_redraw(_mk_k_gate)
    k_lab = T("potassium current", 28, TEXT).move_to([-0.15, 2.55, 0])

    # Computed outward grey K+ dots in central ion lane (x ~ -0.15)
    k_dots = VGroup(*[Dot(radius=0.085, color=GREY) for _ in range(14)])
    k_phase = np.linspace(0.0, 1.0, 14, endpoint=False)

    def k_up(mob, dt):
        ko = k_open.get_value()
        rate = 0.45 + 0.65 * ko
        for idx, d in enumerate(mob):
            k_phase[idx] = (k_phase[idx] + rate * dt) % 1.0
            active = idx < max(6, int(round(14 * ko)))
            x = -0.15 + 0.28 * np.sin(idx * 1.9 + k_phase[idx] * 2.0)
            # When open, stream up through gate to y=2.25; when shut, circulate inside below gate
            if ko < 0.35 and idx >= 2:
                y = -0.4 + 1.65 * np.sin(PI * k_phase[idx])
            else:
                top_y = 1.45 + 0.80 * ko
                y = 0.05 + (top_y - 0.05) * k_phase[idx]
            d.move_to([x, y, 0])
            d.set_opacity(0.95 if active else 0.0)

    k_dots.add_updater(k_up)

    # Membrane voltage meter safely inside right half of cell (well clear of walls & dots)
    m_base = np.array([1.55, 0.08, 0])
    m_box = RoundedRectangle(corner_radius=0.1, width=0.52, height=1.45,
                             stroke_color=TEXT, stroke_width=3.5, fill_color=BG, fill_opacity=0.88).move_to(m_base)
    m_fill = always_redraw(lambda: Rectangle(
        width=0.38, height=max(0.14, 1.30 * vm_val.get_value()),
        stroke_width=0, fill_color=TEXT, fill_opacity=0.92,
    ).align_to(m_box.get_bottom() + UP * 0.07, DOWN).set_x(m_base[0]))
    m_lab = T("membrane\nvoltage", 24, TEXT, line_spacing=0.85).move_to([1.55, -1.10, 0])
    m_state = always_redraw(lambda: T(
        "less negative" if vm_val.get_value() > 0.5 else "resting",
        22, YELLOW if vm_val.get_value() > 0.5 else GREY,
    ).move_to([1.55, 1.02, 0]))

    # Two calcium channel doors in central ion lane (x = -0.60, +0.30)
    ca_xs = [-0.60, 0.30]

    def _mk_ca_gates():
        cy = -0.05 - (3.2 + 0.7 * squeeze.get_value()) / 2
        co = ca_open.get_value()
        return VGroup(*[
            VGroup(
                Line([cx - 0.32, cy, 0], [cx - 0.32 * (1.0 - 0.85 * co), cy - 0.32 * co, 0],
                     color=PURPLE, stroke_width=6),
                Line([cx + 0.32, cy, 0], [cx + 0.32 * (1.0 - 0.85 * co), cy - 0.32 * co, 0],
                     color=PURPLE, stroke_width=6),
            )
            for cx in ca_xs
        ])

    ca_gates = always_redraw(_mk_ca_gates)
    ca_lab = T("calcium channels", 28, PURPLE).move_to([-0.15, -2.65, 0])

    # Computed inward PURPLE Ca2+ dots strictly in central ion lane (-0.85..+0.55)
    ca_dots = VGroup(*[Dot(radius=0.095, color=PURPLE) for _ in range(18)])
    ca_phase = rng.random(18)

    def ca_up(mob, dt):
        op = ca_open.get_value()
        for idx, d in enumerate(mob):
            ca_phase[idx] = (ca_phase[idx] + 1.05 * dt) % 1.0
            cx = ca_xs[idx % 2]
            x = cx + 0.20 * np.cos(idx * 2.3)
            y = -2.25 + 3.15 * ca_phase[idx]
            d.move_to([x, y, 0])
            d.set_opacity(0.95 * op)

    ca_dots.add_updater(ca_up)

    return VGroup(cell_body, k_dots, ca_dots, k_gate, ca_gates, m_box, m_fill, cell_lab, k_lab, m_lab, m_state, ca_lab)


class S09Mechanism(SpokenScene):
    def construct(self):
        self.world = LungWorld(center=(0.0, -0.05), scale=1.0, vent=(0.18, 1.0, 1.0),
                               constrict=(1.0, 0.0, 0.0), dim=(0.75, 0.0, 0.0), show_o2_dots=False)
        tag = scope_tag("schematic")
        self.add(self.world.root, tag)

        squeeze = ValueTracker(0.0)
        k_open = ValueTracker(1.0)
        vm_val = ValueTracker(0.22)
        ca_open = ValueTracker(0.0)
        cell_grp = _build_muscle_cell(squeeze, k_open, vm_val, ca_open)

        self.play(Indicate(self.world.rings[0], color=ORANGE, scale_factor=1.3), run_time=0.8)
        self.play(FadeOut(self.world.root), FadeIn(cell_grp), run_time=1.0)

        self.at("inhibits")
        self.play(k_open.animate.set_value(0.15), vm_val.animate.set_value(0.38), run_time=2.0)

        self.at("smooth muscle")
        self.play(Indicate(cell_grp[7], color=ORANGE, scale_factor=1.06), run_time=1.0)

        self.at("depolarizes")
        self.play(vm_val.animate.set_value(0.82), run_time=1.4)

        self.at("calcium channels open")
        self.play(ca_open.animate.set_value(1.0), run_time=0.8)
        self.play(squeeze.animate.set_value(1.0), run_time=1.8)

        self.at("one route among")
        other_tag = T("one route of several", 28, TEXT).move_to([0.0, HEAD_Y, 0])
        side_a1 = Arrow([-5.2, 0.4, 0], [-3.6, 0.4, 0], buff=0, color=GREY, stroke_width=3.5, tip_length=0.2)
        side_a2 = Arrow([-5.2, -0.5, 0], [-3.6, -0.5, 0], buff=0, color=GREY, stroke_width=3.5, tip_length=0.2)
        self.play(FadeIn(other_tag), Create(side_a1), Create(side_a2), run_time=0.8)
        self.finish()


def _mito_icon(scale=1.0):
    bean = RoundedRectangle(corner_radius=0.35 * scale, width=1.15 * scale, height=0.62 * scale,
                            stroke_color=CYAN, stroke_width=3.5, fill_color=CYAN, fill_opacity=0.22)
    wave = VMobject(stroke_color=CYAN, stroke_width=2.5).set_points_as_corners([
        [-0.36 * scale, 0.0, 0], [-0.18 * scale, 0.14 * scale, 0],
        [0.0, -0.14 * scale, 0], [0.18 * scale, 0.14 * scale, 0], [0.36 * scale, 0.0, 0],
    ])
    return VGroup(bean, wave)


class S10Sensor(SpokenScene):
    def construct(self):
        squeeze = ValueTracker(1.0)
        k_open = ValueTracker(0.15)
        vm_val = ValueTracker(0.78)
        ca_open = ValueTracker(1.0)
        cell_grp = _build_muscle_cell(squeeze, k_open, vm_val, ca_open, label_pos=(-1.95, -0.80))
        tag = scope_tag("schematic")
        self.add(cell_grp, tag)

        mito = _mito_icon(1.00).move_to([-1.95, 1.05, 0])
        mito_q = T("?", 34, CYAN).next_to(mito, RIGHT, buff=0.12)
        mito_lab = T("sensor?\n(hypothesized)", 24, CYAN, line_spacing=0.85).move_to([-1.95, 0.26, 0])
        mito_grp = VGroup(mito, mito_q, mito_lab)

        self.at("mitochondria")
        self.play(FadeIn(mito_grp), run_time=1.0)

        self.at("in mice")
        self.world = LungWorld(center=(0.6, 0.35), scale=0.86, vent=(1.0, 1.0, 1.0),
                               constrict=(0.0, 0.0, 0.0), dim=(0.0, 0.0, 0.0), show_o2_dots=False)
        mouse_tag = chip("isolated mouse lung", TEXT, size=26).move_to([-4.6, 3.15, 0])

        # Cleanly OUTSIDE left lung border (lung left = 0.6 - 4.35*0.86 = -3.14)
        sm_bean = _mito_icon(0.55).move_to([-3.65, 0.15, 0])
        sm_x = cross_mark(TEXT, size=0.35, stroke=4).move_to(sm_bean)
        cox_lab = T("Cox4i2 removed", 26, CYAN).move_to([-4.95, -0.45, 0])
        cox_grp = VGroup(sm_bean, sm_x, cox_lab)

        btn_hyp = boxed_label("hypoxia", BLUE, size=28, box=(2.5, 0.68)).move_to([-2.0, -2.85, 0])
        btn_kcl = boxed_label("potassium chloride", ORANGE, size=28, box=(3.6, 0.68)).move_to([1.8, -2.85, 0])

        self.play(FadeOut(cell_grp), FadeOut(mito_grp), run_time=0.5)
        self.play(
            FadeIn(self.world.root), FadeIn(mouse_tag), FadeIn(cox_grp),
            FadeIn(btn_hyp), FadeIn(btn_kcl),
            run_time=0.9,
        )

        self.at("did not constrict")
        ring_x = cross_mark(TEXT, size=0.4, stroke=5).move_to(self.world._to_world(-2.3, -1.20) + RIGHT * 0.56)
        hl_hyp = SurroundingRectangle(btn_hyp, buff=0.06, color=YELLOW, stroke_width=3.5, corner_radius=0.18)
        self.play(
            btn_hyp.box.animate.set_fill(opacity=0.48).set_stroke(width=5),
            btn_kcl.box.animate.set_fill(opacity=0.05).set_stroke(opacity=0.35),
            btn_kcl.label.animate.set_opacity(0.45),
            FadeIn(hl_hyp),
            self.world.o2_level.animate.set_value(0.50),
            FadeIn(ring_x),
            run_time=1.0,
        )

        self.at("potassium chloride")
        ring_tick = tick_mark(TEXT, size=0.42, stroke=5).move_to(ring_x)
        hl_kcl = SurroundingRectangle(btn_kcl, buff=0.06, color=YELLOW, stroke_width=3.5, corner_radius=0.18)
        self.play(
            FadeOut(hl_hyp),
            FadeIn(hl_kcl),
            btn_hyp.box.animate.set_fill(opacity=0.05).set_stroke(width=2.5, opacity=0.35),
            btn_hyp.label.animate.set_opacity(0.45),
            btn_kcl.box.animate.set_fill(opacity=0.48).set_stroke(width=5, opacity=1.0),
            btn_kcl.label.animate.set_opacity(1.0),
            self.world.o2_level.animate.set_value(1.0),
            FadeOut(ring_x),
            FadeIn(ring_tick),
            self.world.constrict[0].animate.set_value(1.0),
            run_time=1.0,
        )
        self.finish()


class S11Upstream(SpokenScene):
    def construct(self):
        self.world = LungWorld(center=(0.6, 0.35), scale=0.86, vent=(1.0, 1.0, 1.0),
                               constrict=(1.0, 0.0, 0.0), dim=(0.0, 0.0, 0.0), show_o2_dots=False)
        mouse_tag = chip("isolated mouse lung", TEXT, size=26).move_to([-4.6, 3.15, 0])
        sm_bean = _mito_icon(0.55).move_to([-3.65, 0.15, 0])
        sm_x = cross_mark(TEXT, size=0.35, stroke=4).move_to(sm_bean)
        cox_lab = T("Cox4i2 removed", 26, CYAN).move_to([-4.95, -0.45, 0])
        ring_tick = tick_mark(TEXT, size=0.42, stroke=5).move_to(self.world._to_world(-2.3, -1.20) + RIGHT * 0.56)
        btn_hyp = boxed_label("hypoxia", BLUE, size=28, box=(2.5, 0.68)).move_to([-2.0, -2.85, 0])
        btn_kcl = boxed_label("potassium chloride", ORANGE, size=28, box=(3.6, 0.68)).move_to([1.8, -2.85, 0])
        btn_kcl.box.set_fill(opacity=0.48)
        tag = scope_tag("schematic")

        self.add(self.world.root, mouse_tag, sm_bean, sm_x, cox_lab, ring_tick, btn_hyp, btn_kcl, tag)

        b_sense = boxed_label("sensing", CYAN, size=30, box=(2.5, 0.85)).move_to([-3.8, -1.75, 0])
        b_sig = boxed_label("signaling", TEXT, size=30, box=(2.6, 0.85)).move_to([0.0, -1.75, 0])
        b_con = boxed_label("contraction", ORANGE, size=30, box=(2.8, 0.85)).move_to([3.9, -1.75, 0])
        a1 = Arrow(b_sense.get_right() + RIGHT * 0.08, b_sig.get_left() + LEFT * 0.08,
                   buff=0, color=GREY, stroke_width=4, tip_length=0.22)
        a2 = Arrow(b_sig.get_right() + RIGHT * 0.08, b_con.get_left() + LEFT * 0.08,
                   buff=0, color=GREY, stroke_width=4, tip_length=0.22)
        chain = VGroup(b_sense, b_sig, b_con, a1, a2)

        lung_hi = LungWorld(center=(0.0, 1.05), scale=0.68, vent=(1.0, 1.0, 1.0),
                            constrict=(1.0, 0.0, 0.0), dim=(0.0, 0.0, 0.0), show_o2_dots=False)

        self.play(
            FadeOut(btn_hyp), FadeOut(btn_kcl),
            FadeOut(self.world.root), FadeOut(sm_bean), FadeOut(sm_x), FadeOut(cox_lab), FadeOut(ring_tick),
            FadeIn(lung_hi.root), FadeIn(chain),
            run_time=0.8,
        )
        self.world = lung_hi

        self.at("machinery works")
        c_tick = tick_mark(TEXT, size=0.42, stroke=5).next_to(b_con, UP, buff=0.14)
        self.play(FadeIn(c_tick), Indicate(b_con, color=ORANGE, scale_factor=1.05), run_time=0.8)

        self.at("defect sits upstream")
        up_pair = VGroup(b_sense, b_sig)
        br = Brace(up_pair, DOWN, buff=0.14, color=TEXT)
        br_lab1 = T("defect here (mouse)", 26, TEXT).next_to(br, DOWN, buff=0.12)
        self.play(GrowFromCenter(br), FadeIn(br_lab1), run_time=0.9)

        self.at("in humans")
        br_lab2 = VGroup(
            T("defect here (mouse)", 26, TEXT),
            T("humans: open question", 26, YELLOW),
        ).arrange(DOWN, buff=0.08).next_to(br, DOWN, buff=0.10)
        sense_q = T("?", 40, CYAN).next_to(b_sense, UP, buff=0.12)
        self.play(swap(br_lab1, br_lab2, run_time=0.6), FadeIn(sense_q))
        self.finish()


class S12When(SpokenScene):
    def construct(self):
        self.world = LungWorld(center=(0.0, -0.05), scale=1.0, vent=(1.0, 1.0, 1.0),
                               constrict=(0.0, 0.0, 0.0), dim=(0.0, 0.0, 0.0), show_o2_dots=False)
        tag = scope_tag("schematic")
        self.add(self.world.root, tag)

        self.at("healthy lungs at rest")
        rest_tag = T("healthy, rest, sea level: little", 30, TEXT).move_to([0.0, HEAD_Y, 0])
        self.play(FadeIn(rest_tag), run_time=0.7)

        self.at("uneven between regions")
        uneven_tag = T("uneven ventilation", 30, YELLOW).move_to([0.0, HEAD_Y, 0])
        self.play(
            swap(rest_tag, uneven_tag, run_time=0.5),
            self.world.vent[0].animate.set_value(0.18),
            self.world.dim[0].animate.set_value(0.75),
            self.world.constrict[0].animate.set_value(1.0),
        )

        self.at("at altitude")
        # Placed cleanly above the outflow vein (vein y=2.13, mountain bottom y=2.40)
        mtn = Polygon(
            [4.55, 2.40, 0], [5.00, 3.05, 0], [5.32, 2.65, 0],
            [5.65, 3.12, 0], [6.10, 2.40, 0],
            stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.25,
        )
        alt_lab = T("altitude", 28, TEXT).next_to(mtn, UP, buff=0.10)
        mtn_grp = VGroup(mtn, alt_lab)
        self.play(
            FadeIn(mtn_grp),
            self.world.o2_level.animate.set_value(0.62),
            run_time=0.9,
        )
        self.finish()


class S13Return(SpokenScene):
    def construct(self):
        self.world = LungWorld(center=(0.0, -0.05), scale=1.0, vent=(0.18, 1.0, 1.0),
                               constrict=(0.25, 0.0, 0.0), dim=(0.75, 0.0, 0.0),
                               o2_level=1.0, show_o2_dots=True)
        tag = scope_tag("schematic")
        self.add(self.world.root, tag)

        r_val = ValueTracker(0.24)
        r_scale = ratio_scale(r_val, pos=[-5.05, 0.25, 0], height=2.2)

        self.at("gives up part")
        self.play(
            self.world.constrict[0].animate.set_value(1.0),
            FadeIn(r_scale),
            run_time=1.0,
        )

        self.at("ratio rises")
        self.play(r_val.animate.set_value(0.56), run_time=1.1)

        self.at("steered toward units")
        self.play(
            Indicate(self.world.air_arrows[1], color=BLUE, scale_factor=1.08),
            Indicate(self.world.air_arrows[2], color=BLUE, scale_factor=1.08),
            run_time=0.9,
        )
        self.finish()


class S14End(EndCard):
    LINE = "Where air runs short, lung arteries narrow,\nsending blood to better-ventilated units."
