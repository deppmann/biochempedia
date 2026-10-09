"""The Calvin cycle: fixing carbon from air  (Biochemistrypedia explainer)

Four narrated slide clips, one arc: fixation counts the carbons (S01) -> what the cycle costs in ATP and NADPH
(S02) -> why a hot day makes Rubisco react with oxygen instead (S03) -> what that costs in carbon (S04).

COLOR MAP (one color per concept, whole video)
  BLUE   = carbon in sugar phosphates (RuBP, 3-PGA, G3P, the carbon pool)
  ORANGE = carbon that comes from CO2 (CO2 itself, a newly fixed carbon)
  TEAL   = Rubisco, the enzyme
  YELLOW = ATP            PURPLE = NADPH
  GREEN  = net gain: sugar leaving the cycle
  RED    = oxygen, oxygenase activity, carbon lost
  GOLD   = heat, and the one number to remember (3 ATP + 2 NADPH per CO2)
  TEXT   = plain words, totals       GREY = structure, de-emphasized
No molecular structures are drawn. A molecule is a labelled capsule or a block of dots, and each dot
is only a count of one carbon (no bonds, no atom geometry); phosphates are labelled tags.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F09A55"
PURPLE = "#B58CD9"
config.disable_caching = True


# ----------------------------------------------------------------------------- helpers
def capsule(colors, step=0.46, r=0.14, pl=False, pr=False, color=BLUE):
    """A molecule as a count of carbons: capsule + one dot per carbon + optional labelled phosphate tags."""
    n = len(colors)
    body = RoundedRectangle(corner_radius=0.2, width=n * step + 0.2, height=0.54, stroke_color=color,
                            stroke_width=2.5, fill_color=color, fill_opacity=0.12)
    dots = VGroup(*[Dot(radius=r, color=c).move_to(body.get_left() + RIGHT * (0.1 + step * (i + 0.5)))
                    for i, c in enumerate(colors)])

    def ptag():
        c = Circle(radius=0.2, stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.3)
        return VGroup(c, T("P", 22, TEXT, weight=BOLD).move_to(c))
    g = VGroup(body, dots)
    g.body, g.dots, g.pl, g.pr = body, dots, None, None
    if pl:
        g.pl = ptag().move_to(body.get_left() + LEFT * 0.22)
        g.add(g.pl)
    if pr:
        g.pr = ptag().move_to(body.get_right() + RIGHT * 0.22)
        g.add(g.pr)
    return g


def block(colors, cols=6, r=0.07, sp=0.19):
    """A block of dots, one per carbon, filled row by row."""
    n = len(colors)
    rows = -(-n // cols)
    g = VGroup()
    for i, c in enumerate(colors):
        rr, cc = divmod(i, cols)
        g.add(Dot(radius=r, color=c).move_to([(cc - (cols - 1) / 2) * sp, ((rows - 1) / 2 - rr) * sp, 0]))
    return g


def two_line(x, y, name, count=None, color=BLUE, size=24):
    parts = VGroup(T(name, size, color) if isinstance(name, str) else name)
    if count:
        parts.add(M(count, 22, GREY))
    return parts.arrange(DOWN, buff=0.06).move_to([x, y, 0])


def atp_tokens(n, per_row, r=0.12, sp=0.3):
    g = VGroup()
    for i in range(n):
        rr, cc = divmod(i, per_row)
        g.add(Circle(radius=r, stroke_width=0, fill_color=YELLOW, fill_opacity=0.95).move_to([cc * sp, -rr * sp, 0]))
    return g


def nadph_tokens(n, per_row, side=0.22, sp=0.3):
    g = VGroup()
    for i in range(n):
        rr, cc = divmod(i, per_row)
        g.add(Square(side_length=side, stroke_width=0, fill_color=PURPLE, fill_opacity=0.95)
              .move_to([cc * sp, -rr * sp, 0]))
    return g


def pop(group, run=0.7):
    return LaggedStart(*[FadeIn(m, scale=0.4) for m in group], lag_ratio=0.12, run_time=run)


# ============================================================================================
class S00Title(TitleCard):
    LESSON = "The Calvin cycle"
    TITLE = "Fixing carbon from air"


# ============================================================================================
class S01Fixation(SpokenScene):
    """RuBP (5 C) + CO2 (1 C) -> six-carbon intermediate -> two 3-PGA (3 C each): count the carbons."""

    def construct(self):
        head = T("Step 1: fixation", 34, font=TITLE_FONT).move_to([0, 3.4, 0])
        legend = VGroup(Dot(radius=0.14, color=BLUE), T("= one carbon", 24, GREY)).arrange(RIGHT, buff=0.15)
        legend.move_to([4.9, 3.4, 0])
        self.play(FadeIn(head), run_time=0.8)
        self.at("beads")
        self.play(FadeIn(legend), run_time=0.5)

        # --- RuBP: five carbons, a phosphate at each end -----------------------------------------------
        rubp = capsule([BLUE] * 5, pl=True, pr=True).move_to([-1.9, 2.55, 0])
        rubp_l = VGroup(T("RuBP", 28, BLUE), T("ribulose 1,5-bisphosphate", 22, GREY)).arrange(DOWN, buff=0.06)
        rubp_l.move_to([-1.9, 1.85, 0])
        self.at("Ribulose")
        self.play(FadeIn(rubp.body), FadeIn(rubp_l), run_time=0.8)
        self.at("5 carbon backbone")
        self.play(pop(rubp.dots, 1.0))
        self.at("capped")
        self.play(FadeIn(rubp.pl, scale=0.5), FadeIn(rubp.pr, scale=0.5), run_time=0.8)

        # --- Rubisco grabs CO2 ------------------------------------------------------------------------
        plus = T("+", 36, GREY).move_to([0.3, 2.55, 0])
        co2 = capsule([ORANGE]).move_to([1.7, 2.55, 0])
        co2_l = T("CO₂", 28, ORANGE).move_to([1.7, 1.95, 0])
        arrow = Arrow([-0.1, 1.35, 0], [-0.1, 0.78, 0], buff=0, stroke_width=7, color=GREY, tip_length=0.25)
        rub = chip("Rubisco", TEAL, size=28).move_to([1.5, 1.05, 0])
        self.at("enzyme")
        self.play(FadeIn(rub, shift=LEFT * 0.2), GrowArrow(arrow), run_time=0.9)
        self.at("single")
        self.play(FadeIn(plus), FadeIn(co2), FadeIn(co2_l), run_time=0.8)

        inter = capsule([BLUE, BLUE, ORANGE, BLUE, BLUE, BLUE], pl=True, pr=True).move_to([-0.1, 0.35, 0])
        self.at("attaches")
        self.play(FadeTransform(VGroup(rubp.copy(), co2.copy()), inter), run_time=1.3)
        inter_l = VGroup(T("six-carbon intermediate", 24, GREY), T("unstable", 24, TEXT)).arrange(DOWN, buff=0.08)
        inter_l.move_to([4.3, 0.35, 0])
        self.at("intermediate")
        self.play(FadeIn(inter_l[0]), run_time=0.6)
        self.at("unstable")
        self.play(FadeIn(inter_l[1]), run_time=0.5)

        # --- it splits down the middle -------------------------------------------------------------------
        xs = inter.body.get_center()[0]
        cut = DashedLine([xs, 0.0, 0], [xs, 0.72, 0], color=TEXT, stroke_width=3)
        dots = inter.dots
        bodyA = RoundedRectangle(corner_radius=0.2, width=1.58, height=0.54, stroke_color=BLUE, stroke_width=2.5,
                                 fill_color=BLUE, fill_opacity=0.12)
        bodyB = bodyA.copy()
        bodyA.move_to(inter.body.get_left() + RIGHT * 0.79)
        bodyB.move_to(inter.body.get_right() + LEFT * 0.79)
        self.at("splits")
        self.play(Create(cut), run_time=0.5)
        self.play(FadeOut(inter.body), FadeIn(bodyA), FadeIn(bodyB), run_time=0.2)
        pgaA = VGroup(bodyA, *dots[:3], inter.pl)
        pgaB = VGroup(bodyB, *dots[3:], inter.pr)
        tgtA, tgtB = np.array([-2.2, -1.0, 0]), np.array([2.0, -1.0, 0])
        self.play(FadeOut(cut), FadeOut(inter_l), pgaA.animate.shift(tgtA - pgaA.get_center()),
                  pgaB.animate.shift(tgtB - pgaB.get_center()), run_time=1.1)
        self.at("two identical")
        self.play(dots[2].animate.set_color(BLUE), run_time=0.6)
        labA = VGroup(T("3-PGA", 28, BLUE), T("3-phosphoglycerate", 22, GREY)).arrange(DOWN, buff=0.06)
        labA.move_to([-2.2, -1.72, 0])
        labB = labA.copy().move_to([2.0, -1.72, 0])
        self.at("3 phosphoglycerate")
        self.play(FadeIn(labA), FadeIn(labB), run_time=0.8)

        # --- the bookkeeping -----------------------------------------------------------------------------
        e5, ep, e1 = M("5", 44, BLUE), M("+", 44, GREY), M("1", 44, ORANGE)
        eq1, e6, eq2 = M("=", 44, GREY), M("6", 44, TEXT), M("=", 44, GREY)
        e3a, ep2, e3b = M("3", 44, BLUE), M("+", 44, GREY), M("3", 44, BLUE)
        ec = T("carbons", 30, GREY)
        eq = VGroup(e5, ep, e1, eq1, e6, eq2, e3a, ep2, e3b, ec).arrange(RIGHT, buff=0.22)
        eq.move_to([0, -3.1, 0])
        ec.align_to(e3b, DOWN)
        self.at("bookkeeping")
        self.play(FadeIn(T("carbon bookkeeping", 24, GREY).move_to([0, -2.6, 0])), run_time=0.5)
        self.at("sugar")
        self.play(FadeIn(e5, scale=0.6), Indicate(rubp.body, color=BLUE, scale_factor=1.06), run_time=0.35)
        self.at("plus")
        self.play(FadeIn(ep), FadeIn(e1, scale=0.6), Indicate(co2.body, color=ORANGE, scale_factor=1.15),
                  run_time=0.8)
        self.at("6 carbons total")
        self.play(FadeIn(eq1), FadeIn(e6, scale=0.6), run_time=0.7)
        self.at("cleanly")
        self.play(FadeIn(eq2), FadeIn(e3a, scale=0.6), FadeIn(ep2), FadeIn(e3b, scale=0.6), FadeIn(ec),
                  Indicate(bodyA, color=BLUE, scale_factor=1.08), Indicate(bodyB, color=BLUE, scale_factor=1.08),
                  run_time=1.0)
        self.finish()


# ============================================================================================
class S02Ledger(SpokenScene):
    """Pyramid of cost: 1 CO2 -> 3 CO2 (9 ATP + 6 NADPH, 1 net G3P) -> 6 CO2 (18 + 12, glucose);
    then the same bill by phase (per 3 CO2): fixation 0, reduction 6 ATP + 6 NADPH, regeneration 3 ATP."""

    def construct(self):
        head = T("The energy bill", 34, font=TITLE_FONT).move_to([0, 3.4, 0])
        PX = -3.0

        def tier(yc, wb, wt, h=1.4):
            pts = [[PX - wb / 2, yc - h / 2, 0], [PX + wb / 2, yc - h / 2, 0],
                   [PX + wt / 2, yc + h / 2, 0], [PX - wt / 2, yc + h / 2, 0]]
            return Polygon(*pts, stroke_color=GREY, stroke_width=2.5, fill_opacity=0)
        tb, tm, tt = tier(-1.5, 6.4, 4.95), tier(-0.05, 4.95, 3.5), tier(1.4, 3.5, 2.05)
        lab_b = T("1 CO₂", 28, ORANGE).move_to([PX, -1.5, 0])
        lab_m = T("3 CO₂", 28, ORANGE).move_to([PX, -0.05, 0])
        lab_m_sub = T("→ 1 net G3P", 22, BLUE).move_to([PX, -0.3, 0])
        lab_t0 = T("6 CO₂", 28, ORANGE).move_to([PX, 1.6, 0])
        lab_t_sub = T("→ 1 glucose", 22, GREEN).move_to([PX, 1.2, 0])

        self.play(FadeIn(head), run_time=0.8)
        self.at("pyramid")
        self.play(LaggedStart(Create(tb), Create(tm), Create(tt), lag_ratio=0.5, run_time=1.5))

        # --- base: 1 CO2 enters ----------------------------------------------------------------------------
        self.at("base")
        self.play(tb.animate.set_fill(ORANGE, 0.13), run_time=0.5)
        self.at("one carbon dioxide")
        self.play(FadeIn(lab_b), run_time=0.6)

        # --- middle tier: 3 turns -> 9 ATP + 6 NADPH -> 1 net G3P -------------------------------------------
        def place_ul(g, x, y):
            g.shift([x - g.get_left()[0], y - g.get_top()[1], 0])
            return g

        def cost(yc, na, nn, per_a, per_n):
            x0 = 0.95
            h_atp = T(f"{na} ATP", 28, YELLOW, weight=BOLD)
            h_plus = T("+", 28, GREY)
            h_nadph = T(f"{nn} NADPH", 28, PURPLE, weight=BOLD)
            hdr = VGroup(h_atp, h_plus, h_nadph).arrange(RIGHT, buff=0.2)
            hdr.move_to([x0 + hdr.width / 2, yc + 0.5, 0])
            ta = place_ul(atp_tokens(na, per_a), x0, yc + 0.18)
            tn = place_ul(nadph_tokens(nn, per_n), x0 + per_a * 0.3 + 0.3, yc + 0.18)
            return h_atp, h_plus, h_nadph, ta, tn
        a_mid = cost(-0.05, 9, 6, 9, 6)
        self.at("Three turns")
        self.play(tm.animate.set_fill(BLUE, 0.13), FadeIn(lab_m), run_time=0.6)
        self.at("nine")
        self.play(FadeIn(a_mid[0], shift=RIGHT * 0.15), pop(a_mid[3], 1.0))
        self.at("six NADPH")
        self.play(FadeIn(a_mid[1]), FadeIn(a_mid[2], shift=RIGHT * 0.15), pop(a_mid[4], 0.9))
        self.at("yield")
        self.play(lab_m.animate.shift(UP * 0.2), FadeIn(lab_m_sub, shift=UP * 0.1), run_time=0.6)

        # --- top tier: six turns doubles everything ---------------------------------------------------------
        a_top = cost(1.4, 18, 12, 9, 6)
        times2 = M("×2", 30, GOLD)
        self.at("assemble")
        self.play(tt.animate.set_fill(GREEN, 0.13), FadeIn(lab_t0), FadeIn(lab_t_sub), run_time=0.7)
        self.at("doubling")
        times2.next_to(a_top[0], LEFT, buff=0.2)
        self.play(FadeIn(times2, scale=0.6), run_time=0.5)
        self.at("18 ATP")
        self.play(FadeIn(a_top[0], shift=RIGHT * 0.15), pop(a_top[3], 1.0))
        self.at("12 NADPH")
        self.play(FadeIn(a_top[1]), FadeIn(a_top[2], shift=RIGHT * 0.15), pop(a_top[4], 0.9))
        self.at("per glucose")
        self.play(Indicate(tt, color=GREEN, scale_factor=1.03), run_time=0.8)

        # --- by phase ------------------------------------------------------------------------------------------
        A = VGroup(tb, tm, tt, lab_b, lab_m, lab_m_sub, lab_t0, lab_t_sub, times2, *a_mid, *a_top)
        head2 = VGroup(T("Where the energy goes", 34, font=TITLE_FONT), T("(per 3 CO₂)", 28, GREY)).arrange(RIGHT, buff=0.3)
        head2[1].align_to(head2[0], DOWN)
        head2.move_to([0, 3.4, 0])
        cols = [-4.15, 0.0, 4.15]
        panels = VGroup(*[RoundedRectangle(corner_radius=0.2, width=3.8, height=3.7, stroke_color=GREY, stroke_width=2.5,
                                           fill_color=GREY, fill_opacity=0.06).move_to([cx, 0.98, 0]) for cx in cols])
        h1, h2, h3 = [T(t, 30, TEXT, weight=BOLD).move_to([cx, 2.3, 0])
                      for t, cx in zip(["Fixation", "Reduction", "Regeneration"], cols)]
        s1, s2, s3 = [T(t, 22, GREY).move_to([cx, 1.8, 0])
                      for t, cx in zip(["Rubisco fixes CO₂", "acid → sugar", "RuBP rebuilt"], cols)]
        self.at("Breaking it down")
        self.play(FadeOut(A), ReplacementTransform(head, head2), run_time=1.0)
        self.play(FadeIn(panels), run_time=0.6)
        self.at("fixation")
        self.play(FadeIn(h1), FadeIn(s1), run_time=0.6)
        free = T("free", 44, GREEN).move_to([cols[0], 0.85, 0])
        free2 = M("0 ATP · 0 NADPH", 22, GREY).move_to([cols[0], 0.2, 0])
        self.at("energetically free")
        self.play(FadeIn(free, scale=0.7), FadeIn(free2), run_time=0.8)

        self.at("reduction")
        self.play(FadeIn(h2), FadeIn(s2), run_time=0.6)
        cx = cols[1]
        l2a = T("6 ATP", 28, YELLOW, weight=BOLD).move_to([cx, 1.05, 0])
        t2a = atp_tokens(6, 6).move_to([cx, 0.6, 0])
        l2n = T("6 NADPH", 28, PURPLE, weight=BOLD).move_to([cx, -0.05, 0])
        t2n = nadph_tokens(6, 6).move_to([cx, -0.5, 0])
        self.at("costs")
        self.play(FadeIn(l2a), pop(t2a, 0.9))
        self.at("NADPH", nth=2)
        self.play(FadeIn(l2n), pop(t2n, 0.9))

        self.at("regenerating")
        self.play(FadeIn(h3), FadeIn(s3), run_time=0.6)
        cx = cols[2]
        l3 = T("3 ATP", 28, YELLOW, weight=BOLD).move_to([cx, 1.05, 0])
        t3 = atp_tokens(3, 6).move_to([cx, 0.6, 0])
        self.at("additional")
        self.play(FadeIn(l3), pop(t3, 0.8))

        # --- the ledger totals -----------------------------------------------------------------------------------
        tot = VGroup(T("total", 26, GREY), T("9 ATP", 30, YELLOW, weight=BOLD), T("+", 30, GREY),
                     T("6 NADPH", 30, PURPLE, weight=BOLD), T("per 3 CO₂", 26, GREY)).arrange(RIGHT, buff=0.22)
        tot.move_to([0, -1.85, 0])
        one = VGroup(T("3 ATP", 36, YELLOW, weight=BOLD), T("+", 36, GREY),
                     T("2 NADPH", 36, PURPLE, weight=BOLD), T("per CO₂", 30, TEXT)).arrange(RIGHT, buff=0.25)
        box = RoundedRectangle(corner_radius=0.18, width=one.width + 0.7, height=one.height + 0.5, stroke_color=GOLD,
                               stroke_width=3).move_to([0, -2.85, 0])
        one.move_to(box)
        div = M("÷ 3", 30, GOLD).next_to(box, LEFT, buff=0.35)
        self.at("Sugar is expensive")
        self.play(FadeIn(tot, shift=UP * 0.1), run_time=0.8)
        self.at("ledger")
        self.play(FadeIn(div, scale=0.6), FadeIn(box), TransformFromCopy(tot[1], one[0]), FadeIn(one[1]),
                  TransformFromCopy(tot[3], one[2]), FadeIn(one[3]), run_time=1.1)
        self.finish()


# ============================================================================================
class DotField(VGroup):
    """Gas molecules wobbling in a fixed set of spots; `level` (0..1) sets how many are visible."""

    def __init__(self, pts, color, level, r=0.095, seed=0):
        super().__init__(*[Dot(radius=r, color=color) for _ in pts])
        self.pts = [np.array([p[0], p[1], 0.0]) for p in pts]
        self.level, self.t = level, 0.0
        self.ph = np.random.RandomState(seed).rand(len(pts), 2) * 6.28
        self.add_updater(self._u)
        self._u(self, 0)

    def _u(self, m, dt):
        self.t += dt
        L = self.level.get_value() * len(self.pts)
        for i, d in enumerate(self):
            off = np.array([np.sin(self.t * 1.3 + self.ph[i, 0]), np.cos(self.t * 1.1 + self.ph[i, 1]), 0]) * 0.05
            d.move_to(self.pts[i] + off)
            d.set_opacity(float(np.clip(L - i, 0, 1)))


class Inflow(VGroup):
    """CO2 molecules drifting down through the pore to Rubisco; pile up outside when the pore is shut."""

    def __init__(self, n, x, y_top, y_pore, y_end, open_t, speed=0.16, y_stop=1.98):
        super().__init__(*[Dot(radius=0.095, color=ORANGE) for _ in range(n)])
        self.n, self.x, self.open_t, self.speed = n, x, open_t, speed
        self.y_top, self.y_pore, self.y_end, self.y_stop = y_top, y_pore, y_end, y_stop
        self.s = 0.0
        self.blocked = [False] * n   # once the pore shuts, a molecule that reaches it stays outside
        self.piled = [False] * n
        self.jit = np.linspace(-0.55, 0.55, n)
        np.random.RandomState(4).shuffle(self.jit)
        self.add_updater(self._u)
        self._u(self, 0)

    def _u(self, m, dt):
        self.s = (self.s + dt * self.speed) % 1.0
        L = self.y_top - self.y_end
        u_pore = (self.y_top - self.y_pore) / L
        shut = self.open_t.get_value() < 0.5
        for k, d in enumerate(self):
            u = (k / self.n + self.s) % 1.0
            jx = self.jit[k]
            y = self.y_top - u * L
            if shut and u < u_pore:
                self.blocked[k] = True
            if not shut:
                self.blocked[k] = self.piled[k] = False
            if self.blocked[k]:
                pile = self.y_stop + 0.13 * (k % 3)
                if y <= pile or u >= u_pore:
                    self.piled[k] = True
                y = pile if self.piled[k] else max(y, pile)
                x = self.x + jx
                op = 1.0 if self.piled[k] else float(np.clip(u / 0.06, 0, 1))
            else:
                x = self.x + jx * float(np.clip((u_pore - u) / 0.1, 0, 1))
                op = float(np.clip((1 - u) / 0.1, 0, 1)) * float(np.clip(u / 0.06, 0, 1))
            d.move_to([x, y, 0])
            d.set_opacity(op)


def frac_o2(c_um, s=80.0, o_um=265.0):
    """Fraction of Rubisco events that take O2: v_o/v_c = (1/S)(O/C)  ->  f = 1 / (1 + S*C/O)."""
    return 1.0 / (1.0 + s * c_um / o_um)


class S03Hot(SpokenScene):
    """Heat -> stomata close -> internal CO2 drops -> O2 wins -> oxygenase -> carbon and energy lost."""

    def construct(self):
        head = T("The hot weather problem", 34, font=TITLE_FONT).move_to([-2.9, 3.4, 0])
        CX = -2.75
        BX0, BX1, BY0, BY1 = -5.0, -0.5, -1.9, 1.5

        # --- the leaf (a schematic, not a cross-section drawing) -----------------------------------------------
        box_sides = VGroup(Line([BX0, BY1, 0], [BX0, BY0, 0]), Line([BX0, BY0, 0], [BX1, BY0, 0]),
                           Line([BX1, BY0, 0], [BX1, BY1, 0]))
        wall = VGroup(Line([BX0, BY1, 0], [CX - 0.6, BY1, 0]), Line([CX + 0.6, BY1, 0], [BX1, BY1, 0]))
        leaf = VGroup(box_sides, wall).set_stroke(GREY, 3)
        open_t = ValueTracker(1.0)

        def guards():
            g = 0.26 * open_t.get_value()
            out = VGroup()
            for sgn in (-1, 1):
                e = Ellipse(width=0.52, height=0.62, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.35)
                e.move_to([CX + sgn * (g + 0.26), BY1, 0])
                out.add(e)
            return out
        guard_m = always_redraw(guards)
        stoma_lab = T("stomata", 22, GREY).move_to([BX1 - 0.65, BY1 + 0.35, 0])

        rub_box = RoundedRectangle(corner_radius=0.14, width=1.9, height=0.62, stroke_color=TEAL, stroke_width=2.5,
                                   fill_color=TEAL, fill_opacity=0.16)
        rub_txt = T("Rubisco", 26, TEAL)
        rub = VGroup(rub_box, rub_txt).move_to([CX, -1.0, 0])
        oxy_tag = T("oxygenase", 24, RED).move_to([CX, -1.55, 0])

        # --- gases ------------------------------------------------------------------------------------------------
        rs = np.random.RandomState(7)
        pts = []
        while len(pts) < 24:
            p = [rs.uniform(-4.75, -0.75), rs.uniform(-0.35, 1.2)]
            if abs(p[0] - CX) < 0.3:
                continue
            if all(np.hypot(p[0] - q[0], p[1] - q[1]) > 0.42 for q in pts):
                pts.append(p)
        co2_in, o2_in = ValueTracker(1.0), ValueTracker(0.3)
        co2_field = DotField(pts[:10], ORANGE, co2_in, seed=1)
        o2_field = DotField(pts[10:24], RED, o2_in, seed=2)
        inflow = Inflow(7, CX, 2.95, BY1, -0.7, open_t)
        leg = VGroup(VGroup(Dot(radius=0.09, color=ORANGE), T("CO₂", 24, ORANGE)).arrange(RIGHT, buff=0.1),
                     VGroup(Dot(radius=0.09, color=RED), T("O₂", 24, RED)).arrange(RIGHT, buff=0.1)
                     ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        leg.move_to([BX0 + 0.65, 2.25, 0])

        # --- thermometer (heat) -----------------------------------------------------------------------------------
        heat = ValueTracker(0.15)
        th_out = RoundedRectangle(corner_radius=0.12, width=0.3, height=3.0, stroke_color=GREY, stroke_width=3)
        th_out.move_to([-5.75, 0.0, 0])
        bulb = Circle(radius=0.26, stroke_color=GREY, stroke_width=3, fill_color=GOLD, fill_opacity=0.95)
        bulb.move_to([-5.75, -1.7, 0])

        def fill():
            h = 0.12 + 2.7 * heat.get_value()
            return Rectangle(width=0.16, height=h, stroke_width=0, fill_color=GOLD, fill_opacity=0.95).move_to(
                [-5.75, -1.5 + h / 2, 0])
        th_fill = always_redraw(fill)

        # --- who binds the active site ------------------------------------------------------------------------------
        c_um = ValueTracker(8.0)
        BAR_W = 4.5

        def bar():
            fo = frac_o2(c_um.get_value())
            wc, wo = BAR_W * (1 - fo), BAR_W * fo
            x0 = CX - BAR_W / 2
            a = Rectangle(width=wc, height=0.42, stroke_width=0, fill_color=ORANGE, fill_opacity=0.95).move_to([x0 + wc / 2, -3.0, 0])
            b = Rectangle(width=wo, height=0.42, stroke_width=0, fill_color=RED, fill_opacity=0.95).move_to([x0 + wc + wo / 2, -3.0, 0])
            la = T("CO₂", 22, BG, weight=BOLD).move_to(a)
            lb = T("O₂", 22, BG, weight=BOLD).move_to(b)
            return VGroup(a, b, la, lb)
        bar_m = always_redraw(bar)
        bar_cap = T("who binds Rubisco's active site", 22, GREY).move_to([CX, -2.5, 0])

        # --- the chain of dominoes ------------------------------------------------------------------------------------
        def link_chip(text, color, y):
            r = RoundedRectangle(corner_radius=0.14, width=5.7, height=0.72, stroke_color=color, stroke_width=2.5,
                                 fill_color=color, fill_opacity=0.16)
            t = T(text, 26, color).move_to(r)
            return VGroup(r, t).move_to([3.4, y, 0])
        ys = [2.5, 1.5, 0.5, -0.5, -1.5, -2.5]
        chips = [link_chip("Temperature rises", GOLD, ys[0]), link_chip("Stomata close", GREY, ys[1]),
                 link_chip("Internal CO₂ drops", ORANGE, ys[2]), link_chip("O₂ wins the competition", RED, ys[3]),
                 link_chip("Rubisco acts as an oxygenase", RED, ys[4]), link_chip("Carbon and energy lost", RED, ys[5])]
        arrows = [Arrow([3.4, ys[i] - 0.38, 0], [3.4, ys[i + 1] + 0.38, 0], buff=0, stroke_width=3, color=GREY,
                        tip_length=0.12, max_tip_length_to_length_ratio=0.5) for i in range(5)]

        # ------------------------------------------------------------------------------------------------------------
        self.add(co2_field, o2_field, inflow, guard_m)
        self.play(FadeIn(head), FadeIn(leaf), FadeIn(rub), FadeIn(stoma_lab), FadeIn(leg), run_time=1.2)
        self.at("plant gets too hot")
        self.add(th_fill)
        self.play(FadeIn(th_out), FadeIn(bulb), run_time=0.7)

        self.at("Temperature rises")
        self.play(FadeIn(chips[0], shift=DOWN * 0.15), heat.animate.set_value(1.0), run_time=1.5)
        self.at("closes")
        self.play(FadeIn(arrows[0]), FadeIn(chips[1], shift=DOWN * 0.15), open_t.animate.set_value(0.0), run_time=1.3)
        self.at("trap")
        self.play(Indicate(guard_m, color=RED, scale_factor=1.15), run_time=1.0)
        self.at("internal")
        self.play(FadeIn(arrows[1]), FadeIn(chips[2], shift=DOWN * 0.15), co2_in.animate.set_value(0.3), run_time=2.4)
        self.at("oxygen builds up")
        self.play(o2_in.animate.set_value(1.0), run_time=1.6)
        self.at("Now oxygen")
        self.play(FadeIn(arrows[2]), FadeIn(chips[3], shift=DOWN * 0.15), FadeIn(bar_cap), FadeIn(bar_m), run_time=0.8)
        self.play(c_um.animate.set_value(2.8), run_time=2.2)
        self.at("misfires")
        self.play(FadeIn(arrows[3]), FadeIn(chips[4], shift=DOWN * 0.15),
                  rub_box.animate.set_stroke(RED, 3).set_fill(RED, 0.2), rub_txt.animate.set_color(RED),
                  FadeIn(oxy_tag), run_time=0.9)
        self.at("burns carbon")
        loss_c = Dot(radius=0.08, color=ORANGE).move_to(rub.get_left() + LEFT * 0.3 + UP * 0.2)
        loss_a = VGroup(Circle(radius=0.2, stroke_width=0, fill_color=YELLOW, fill_opacity=0.95),
                        T("ATP", 18, BG, weight=BOLD)).move_to(rub.get_left() + LEFT * 0.35 + DOWN * 0.1)
        loss_a[1].move_to(loss_a[0])
        self.add(loss_c, loss_a)
        self.play(FadeIn(arrows[4]), FadeIn(chips[5], shift=DOWN * 0.15),
                  loss_c.animate.shift(LEFT * 1.0 + UP * 0.5).set_opacity(0),
                  loss_a.animate.shift(LEFT * 1.1 + DOWN * 0.1).set_opacity(0), run_time=1.6)
        self.at("Each step forces")
        self.play(LaggedStart(*[Indicate(c, color=TEXT, scale_factor=1.04) for c in chips], lag_ratio=0.25, run_time=2.6))
        self.at("lost productivity")
        self.play(chips[5][0].animate.set_fill(RED, 0.4).set_stroke(width=4), run_time=0.8)
        climate = T("hot, dry climates: hard on ordinary plants", 22, GOLD).move_to([3.4, -3.28, 0])
        self.at("hot dry climates")
        self.play(FadeIn(climate, shift=UP * 0.1), Indicate(VGroup(th_out, bulb), color=GOLD, scale_factor=1.08),
                  run_time=1.0)

        # --- the two fixes ---------------------------------------------------------------------------------------------
        spatial = chip("spatial", GOLD, size=44)
        temporal = chip("temporal", GOLD, size=44)
        spatial.move_to([-3.2, 0.3, 0])
        temporal.move_to([3.2, 0.3, 0])
        sp_sub = T("C₄ plants", 28, GREY).next_to(spatial, DOWN, buff=0.3)
        tp_sub = T("CAM plants", 28, GREY).next_to(temporal, DOWN, buff=0.3)
        fade_all = [head, leaf, rub, stoma_lab, leg, th_out, bulb, th_fill, guard_m, co2_field, o2_field,
                    inflow, bar_m, bar_cap, oxy_tag, climate, *chips, *arrows]
        two = T("two evolutionary fixes", 36, font=TITLE_FONT).move_to([0, 2.0, 0])
        self.at("evolutionary")
        self.play(*[FadeOut(m) for m in fade_all], FadeIn(two), run_time=1.0)
        self.at("spatial")
        self.play(FadeIn(spatial, shift=UP * 0.15), FadeIn(sp_sub), run_time=0.7)
        self.at("temporal")
        self.play(FadeIn(temporal, shift=UP * 0.15), FadeIn(tp_sub), run_time=0.7)
        self.finish()


# ============================================================================================
class S04Photoresp(SpokenScene):
    """Carbon count, normal cycle vs photorespiration. Each dot is one carbon."""

    def construct(self):
        SP = 0.19
        leg = VGroup(Dot(radius=0.07, color=BLUE), T("= one carbon", 22, GREY)).arrange(RIGHT, buff=0.12)
        leg.move_to([5.2, 3.35, 0])
        divider = Line([-6.3, -0.05, 0], [6.3, -0.05, 0], color=GREY, stroke_width=1.5).set_opacity(0.6)
        ytop, ybot = 1.95, -1.45
        X1, X2, X3, X4a, X4b = -5.1, -2.4, 0.1, 2.6, 5.2
        XB2a, XB2b, XB3, XB4 = -2.4, -0.1, 2.45, 5.0

        def arrow_between(xa, xb, y, color=GREY):
            return Arrow([xa + 0.62, y, 0], [xb - 0.62, y, 0], buff=0, stroke_width=4, color=color, tip_length=0.18)

        self.at("side by side")
        self.play(Create(divider), run_time=0.8)
        self.at("counting")
        self.play(FadeIn(leg), run_time=0.5)

        # ---- top: the normal cycle ------------------------------------------------------------------------------------
        t_top = T("Normal cycle", 30, TEXT, weight=BOLD).move_to([-5.0, 3.3, 0])
        self.at("On top")
        self.play(FadeIn(t_top), run_time=0.5)
        s1 = block([BLUE] * 30, sp=SP).move_to([X1, ytop + SP / 2, 0])
        lab1 = two_line(X1, 0.95, "6 RuBP", "30 C", BLUE, size=22)
        self.at("normal")
        self.play(pop(s1, 1.0), FadeIn(lab1), run_time=1.0)
        co2_dots = block([ORANGE] * 6, sp=SP).move_to([X1, ytop - 2.5 * SP, 0])
        lab1b = VGroup(T("6 RuBP", 22, BLUE), T("+ 6 CO₂", 22, ORANGE)).arrange(RIGHT, buff=0.12)
        lab1b = VGroup(lab1b, M("36 C", 22, GREY)).arrange(DOWN, buff=0.06).move_to([X1, 0.95, 0])
        self.at("six carbon")
        self.play(FadeIn(co2_dots, shift=DOWN * 0.5), ReplacementTransform(lab1[0], lab1b[0][0]),
                  FadeIn(lab1b[0][1], shift=LEFT * 0.1), ReplacementTransform(lab1[1], lab1b[1]), run_time=1.0)
        s1_all = VGroup(*s1, *co2_dots)

        s2 = block([BLUE] * 36, sp=SP).move_to([X2, ytop, 0])
        a12 = arrow_between(X1, X2, ytop)
        rub_lab = T("Rubisco", 22, TEAL).next_to(a12, UP, buff=0.12)
        lab2 = two_line(X2, 0.95, "12 3-PGA", "36 C", BLUE, size=22)
        self.at("Rubisco makes")
        self.play(GrowArrow(a12), FadeIn(rub_lab), run_time=0.7)
        self.at("12 molecules")
        self.play(TransformFromCopy(s1_all, s2), FadeIn(lab2), run_time=1.3)

        s3 = block([BLUE] * 36, sp=SP).move_to([X3, ytop, 0])
        a23 = arrow_between(X2, X3, ytop)
        lab3 = two_line(X3, 0.95, "12 G3P", "36 C", BLUE, size=22)
        self.at("which become")
        self.play(GrowArrow(a23), TransformFromCopy(s2, s3), FadeIn(lab3), run_time=1.3)

        s4a = block([BLUE] * 30, sp=SP).move_to([X4a, ytop + SP / 2, 0])
        s4b = block([GREEN] * 6, sp=SP).move_to([X4b, ytop, 0])
        lab4a = two_line(X4a, 0.95, "10 G3P", "30 C", BLUE, size=22)
        a34 = arrow_between(X3, X4a, ytop)
        self.at("10G3P")
        self.play(GrowArrow(a34), TransformFromCopy(VGroup(*s3[:30]), s4a), FadeIn(lab4a), run_time=1.2)
        loop = ArcBetweenPoints([X4a, ytop + 0.72, 0], [X1, ytop + 0.72, 0], angle=0.5, stroke_color=BLUE,
                                stroke_width=4)
        loop.add_tip(tip_length=0.2, tip_width=0.2)
        loop_lab = T("regenerates RuBP", 22, BLUE).move_to([(X1 + X4a) / 2, ytop + 0.95, 0])
        self.at("regenerate")
        self.play(Create(loop), FadeIn(loop_lab), run_time=1.2)

        lab4b = two_line(X4b, 0.95, "1 glucose", "6 C", GREEN, size=22)
        self.at("two exit")
        self.play(TransformFromCopy(VGroup(*s3[30:]), s4b), run_time=1.0)
        self.at("one glucose")
        self.play(FadeIn(lab4b), run_time=0.6)
        net_top = T("net: +6 fixed carbons", 28, GREEN).move_to([3.7, 0.35, 0])
        self.at("a gain of")
        self.play(FadeIn(net_top, shift=UP * 0.1), Indicate(s4b, color=GREEN, scale_factor=1.3), run_time=1.0)

        # ---- bottom: photorespiration ----------------------------------------------------------------------------------
        t_bot = T("Photorespiration", 30, TEXT, weight=BOLD).move_to([-4.6, -0.5, 0])
        self.at("On the bottom")
        self.play(FadeIn(t_bot), run_time=0.5)
        b1 = block([BLUE] * 30, sp=SP).move_to([X1, ybot, 0])
        lab_b1 = VGroup(VGroup(T("6 RuBP", 22, BLUE), T("+ 6 O₂", 22, RED)).arrange(RIGHT, buff=0.12),
                        M("30 C", 22, GREY)).arrange(DOWN, buff=0.06).move_to([X1, -2.3, 0])
        self.at("Rubisco grabs")
        self.play(pop(b1, 0.9), FadeIn(lab_b1), run_time=0.9)

        b2a = block([BLUE] * 18, sp=SP).move_to([XB2a, ybot, 0])
        b2b = block([BLUE] * 12, sp=SP).move_to([XB2b, ybot, 0])
        a_b = arrow_between(X1, XB2a, ybot)
        rub_lab2 = T("Rubisco", 22, TEAL).next_to(a_b, UP, buff=0.12)
        lab_b2a = two_line(XB2a, -2.3, "6 3-PGA", "18 C", BLUE, size=22)
        lab_b2b = two_line(XB2b, -2.3, "6 phosphoglycolate", "12 C", RED, size=22)
        self.at("producing")
        self.play(GrowArrow(a_b), FadeIn(rub_lab2), run_time=0.6)
        self.at("3PGA plus")
        self.play(TransformFromCopy(VGroup(*b1[:18]), b2a), FadeIn(lab_b2a), run_time=1.0)
        self.at("phosphoglycolate")
        self.play(TransformFromCopy(VGroup(*b1[18:]), b2b), FadeIn(lab_b2b), run_time=1.0)

        # salvage: 12 C -> 9 C back as 3-PGA, 3 C leave as CO2
        b3 = block([BLUE] * 9, cols=3, sp=SP).move_to([XB3, ybot, 0])
        lost = block([RED] * 3, cols=3, sp=SP)
        a_s = Arrow([XB2b + 0.62, ybot, 0], [XB3 - 0.4, ybot, 0], buff=0, stroke_width=4, color=GREY, tip_length=0.18)
        sal_lab = T("salvage", 22, GREY).next_to(a_s, UP, buff=0.12)
        lab_b3 = two_line(XB3, -2.3, "3 3-PGA", "9 C", BLUE, size=22)
        self.at("salvage")
        self.play(GrowArrow(a_s), FadeIn(sal_lab), run_time=0.7)
        self.at("recovers")
        self.play(TransformFromCopy(VGroup(*b2b[:9]), b3), FadeIn(lab_b3), run_time=1.0)
        self.at("releases")
        lost_lab = T("3 CO₂", 24, RED)
        VGroup(lost, lost_lab).arrange(RIGHT, buff=0.15).move_to([a_s.get_center()[0], -0.62, 0])
        self.play(TransformFromCopy(VGroup(*b2b[9:]), lost), FadeIn(lost_lab), run_time=0.9)
        net_bot = T("net: −3 fixed carbons", 28, RED).move_to([-1.0, -3.25, 0])
        self.at("lose three")
        self.play(FadeIn(net_bot, shift=UP * 0.1), Indicate(lost, color=RED, scale_factor=1.3), run_time=1.0)

        # not enough carbons to rebuild the 6 RuBP, so no glucose
        b4 = block([BLUE] * 27 + [BG] * 3, sp=SP).move_to([XB4, ybot, 0])
        hollow = VGroup(*[Circle(radius=0.07, stroke_color=RED, stroke_width=2.5, fill_opacity=0).move_to(d.get_center())
                          for d in b4[27:]])
        a_g = Arrow([XB3 + 0.4, ybot, 0], [XB4 - 0.7, ybot, 0], buff=0, stroke_width=4, color=GREY, tip_length=0.18)
        lab_b4 = two_line(XB4, -2.3, "9 G3P", "27 C", BLUE, size=22)
        need = T("30 C needed", 22, RED).move_to([XB4, -2.95, 0])
        self.at("There are not even enough")
        self.play(GrowArrow(a_g), TransformFromCopy(VGroup(*b2a, *b3), VGroup(*b4[:27])), FadeIn(lab_b4), run_time=0.9)
        self.at("carbons left")
        self.play(FadeIn(hollow, scale=1.6), FadeIn(need), run_time=0.9)
        self.at("no glucose")
        nog = T("no glucose made", 26, RED).move_to([XB4 - 0.25, -0.6, 0])
        self.play(FadeIn(nog, shift=DOWN * 0.1), run_time=0.7)
        self.at("contrast")
        self.play(Indicate(net_top, color=GREEN, scale_factor=1.08), Indicate(net_bot, color=RED, scale_factor=1.08),
                  run_time=1.2)
        self.finish()


# ============================================================================================
class S05End(EndCard):
    LINE = "Fixing carbon costs energy, and Rubisco's oxygen slip wastes it."
