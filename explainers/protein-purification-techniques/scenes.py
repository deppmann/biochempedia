# COLOR MAP (kept for the whole video)
#   RED    = the protein you are hunting (target / "red marbles")
#   GREY   = everything else (contaminant proteins, structure, de-emphasis)
#   BLUE   = enzyme units (activity) / yield
#   GREEN  = specific activity, fold-purification, purity: the "it worked" numbers
#   TEAL   = resin beads and the MALDI matrix
#   YELLOW = what moves or is highlighted right now (laser, salt, current focus)
#   GOLD   = affinity ligand (and the title rule)
import json, math, os
from bp_style import *

_SCRIPT = {s["id"]: s for s in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "script.json")))["scenes"]}


class Nar(NarratedScene):
    ID = ""

    def setup(self):
        super().setup()
        self.narr = _SCRIPT[self.ID].get("narration", "")

    def tt(self, snippet):
        i = self.narr.find(snippet)
        assert i >= 0, snippet
        return i / len(self.narr) * self.narration_s

    def at(self, snippet, lead=0.25):
        d = self.tt(snippet) - lead - self.renderer.time
        if d > 0.05:
            self.wait(d)

    def log(self, tag):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "timing.log"), "a") as f:
            f.write(f"{self.ID} {tag} {self.renderer.time:.2f}\n")

    def until(self, snippet, lead=0.25):
        """seconds from now until just before `snippet` is spoken (for a run_time)"""
        return max(0.4, self.tt(snippet) - lead - self.renderer.time)


def blob(label, color=RED, w=1.0, h=0.7, size=30):
    e = Ellipse(width=w, height=h, color=color, fill_color=color, fill_opacity=0.85, stroke_width=2)
    t = T(label, size=size, color=BG if label else TEXT, weight=BOLD)
    return VGroup(e, t.move_to(e))


def bead(sign, r=0.36):
    c = Circle(radius=r, color=TEAL, fill_color=TEAL, fill_opacity=0.35, stroke_width=3)
    return VGroup(c, T(sign, size=30, color=TEXT, weight=BOLD).move_to(c))


def marble(color, r=0.2):
    return Circle(radius=r, color=color, fill_color=color, fill_opacity=0.9, stroke_width=1.5)


def beaker(cx, cy, w, h):
    pts = [[cx - w / 2, cy + h / 2, 0], [cx - w / 2, cy - h / 2, 0], [cx + w / 2, cy - h / 2, 0], [cx + w / 2, cy + h / 2, 0]]
    m = VMobject(color=GREY, stroke_width=4)
    m.set_points_as_corners(pts)
    return m


class S00Title(TitleCard):
    LESSON = "Techniques in protein biochemistry"
    TITLE = "Purify it, then prove it"


# ---------------------------------------------------------------- S01
class S01Specific(Nar):
    ID = "s01_specific"

    def construct(self):
        c1 = chip("specific activity", GREEN, size=32)
        c2 = chip("fold-purification", GREEN, size=32)
        c3 = chip("% yield", BLUE, size=32)
        row = VGroup(c1, c2, c3).arrange(RIGHT, buff=0.4).move_to(UP * 0.3)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in (c1, c2, c3)], lag_ratio=0.35), run_time=self.until("Specific activity is", 0.1))

        # the purification table
        colx = {"units": -0.1, "mg": 2.0, "sa": 5.0}
        hdr = VGroup(T("Step", 26, GREY).move_to([-5.0, 2.0, 0]),
                     T("Units", 26, BLUE).move_to([colx["units"], 2.0, 0]),
                     T("Protein (mg)", 26, GREY).move_to([colx["mg"], 2.0, 0]),
                     VGroup(T("Specific activity", 26, GREEN), T("(units/mg)", 24, GREEN)).arrange(DOWN, buff=0.06).move_to([colx["sa"] - 0.1, 2.0, 0]))
        rule = Line([-6.2, 1.55, 0], [6.4, 1.55, 0], color=GREY, stroke_width=2)
        rows_y = [0.8, -0.2, -1.2]
        data = [("Crude lysate", 1000, 500), ("Ion exchange", 800, 40), ("Affinity column", 400, 2)]
        step, units, mg, sa = VGroup(), VGroup(), VGroup(), VGroup()
        for (n, u, p), y in zip(data, rows_y):
            step.add(T(n, 28).move_to([-6.2, y, 0], aligned_edge=LEFT))
            units.add(M(f"{u}", 30, BLUE).move_to([colx["units"], y, 0]))
            mg.add(M(f"{p}", 30, GREY).move_to([colx["mg"], y, 0]))
            sa.add(M(f"{u / p:g}", 30, GREEN).move_to([colx["sa"], y, 0]))
        self.play(row.animate.scale(0.8).move_to(UP * 3.2), FadeIn(hdr[0]), FadeIn(rule), run_time=0.9)
        self.play(FadeIn(hdr[1]), FadeIn(hdr[2]), FadeIn(step), LaggedStart(*[FadeIn(x) for x in list(units) + list(mg)], lag_ratio=0.1), run_time=1.5)
        self.play(Indicate(c1, color=GREEN, scale_factor=1.08), FadeIn(hdr[3]), run_time=0.8)
        formula = M("specific activity = units ÷ mg protein", 28, GREEN).move_to(DOWN * 2.4)
        self.play(Write(formula), run_time=1.6)
        self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.15) for x in sa], lag_ratio=0.5), run_time=1.5)
        box = SurroundingRectangle(VGroup(hdr[3], sa), color=GREEN, buff=0.15, stroke_width=3)
        self.play(Create(box), run_time=0.8)
        rise = VGroup(T("rises at every good step", 26, GREEN), Arrow(DOWN * 0.3, UP * 0.3, color=GREEN, buff=0, stroke_width=6, max_tip_length_to_length_ratio=0.5)).arrange(RIGHT, buff=0.2).move_to([0, -3.15, 0])
        self.play(FadeIn(rise), run_time=0.8)

        # fold
        self.at("Fold-purification is")
        self.play(FadeOut(rise), run_time=0.4)
        fold = M("fold = 200 ÷ 2 = 100-fold", 28, GREEN).move_to(DOWN * 2.4)
        circ = VGroup(SurroundingRectangle(sa[0], color=YELLOW, buff=0.12), SurroundingRectangle(sa[2], color=YELLOW, buff=0.12))
        self.play(FadeOut(box), FadeTransform(formula, fold), Create(circ), run_time=1.2)
        # yield
        self.at("Percent yield is")
        yld = M("yield = 400 ÷ 1000 = 40 %", 28, BLUE).move_to(DOWN * 2.4)
        circ2 = VGroup(SurroundingRectangle(units[0], color=YELLOW, buff=0.12), SurroundingRectangle(units[2], color=YELLOW, buff=0.12))
        self.play(FadeOut(circ), FadeTransform(fold, yld), Create(circ2), run_time=1.2)

        # marbles
        self.at("Picture a beaker", 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        bl = beaker(-3.6, -0.3, 3.6, 2.4)
        br = beaker(3.6, -0.3, 3.6, 2.4)
        self.play(Create(bl), Create(br), run_time=0.5)
        def pile(cx, n_cols, items):
            out = []
            for i, col in enumerate(items):
                r, c = divmod(i, n_cols)
                out.append(marble(col, 0.25).move_to([cx - (n_cols - 1) * 0.26 + c * 0.52, -1.5 + 0.3 + r * 0.52, 0]))
            return out
        order = [GREY, RED, GREY, GREY, GREY, GREY, RED, GREY, GREY, GREY, RED, GREY]
        left = pile(-3.6, 6, order)
        self.play(LaggedStart(*[FadeIn(m, shift=DOWN * 0.8) for m in left], lag_ratio=0.08), run_time=1.2)
        lab1 = T("crude", 28, GREY).move_to([-3.6, 1.2 + 0.4, 0])
        cnt1 = M("3 red of 12", 28).move_to([-3.6, -2.35, 0])
        self.play(FadeIn(lab1), FadeIn(cnt1), run_time=0.4)
        right_items = [RED, GREY, RED, GREY, RED, GREY]
        slots = [m.get_center() for m in pile(3.6, 3, right_items)]
        arrow = Arrow([-1.2, 0.0, 0], [1.2, 0.0, 0], color=YELLOW, buff=0)
        arrow_lab = T("remove the rest", 26, YELLOW).next_to(arrow, UP, buff=0.15)
        self.play(GrowArrow(arrow), FadeIn(arrow_lab), run_time=0.5)
        reds = [m for m, c in zip(left, order) if c == RED]
        greys = [m for m, c in zip(left, order) if c == GREY]
        keep_g, drop_g = greys[:3], greys[3:]
        self.play(*[m.animate.set_opacity(0.25) for m in drop_g], run_time=0.5)
        cps = [m.copy() for m in reds + keep_g]
        moves = [m.animate.move_to(slots[k]) for m, k in zip(cps, (0, 2, 4, 1, 3, 5))]
        self.play(LaggedStart(*moves, lag_ratio=0.08), run_time=1.3)
        lab2 = T("purified", 28, GREEN).move_to([3.6, 1.2 + 0.4, 0])
        cnt2 = M("3 red of 6", 28).move_to([3.6, -2.35, 0])
        self.play(FadeIn(lab2), FadeIn(cnt2), run_time=0.4)
        hi = T("same red marbles, smaller pile: higher specific activity", 26, GREEN).move_to([0, -3.2, 0])
        self.play(FadeIn(hi), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------- S02
class S02Four(Nar):
    ID = "s02_four"

    def construct(self):
        W, H = 6.1, 3.25
        centers = [np.array([-3.15, 1.85, 0]), np.array([3.15, 1.85, 0]), np.array([-3.15, -1.6, 0]), np.array([3.15, -1.6, 0])]
        names = [("Solubility", "salting out"), ("Size", "gel filtration"), ("Charge", "ion exchange"), ("Affinity", "bound ligand")]
        panels = []
        for c, (a, b) in zip(centers, names):
            fr = RoundedRectangle(corner_radius=0.2, width=W, height=H, color=GREY, stroke_width=2.5).move_to(c)
            ti = T(a, 32, TEXT, weight=BOLD).move_to(c + np.array([-W / 2 + 0.3, H / 2 - 0.4, 0]), aligned_edge=LEFT)
            su = T(b, 26, GREY).move_to(c + np.array([W / 2 - 0.3, H / 2 - 0.4, 0]), aligned_edge=RIGHT)
            panels.append((fr, ti, su))
        self.play(LaggedStart(*[FadeIn(p[0]) for p in panels], lag_ratio=0.2), run_time=self.until("Solubility:", 0.2))

        # 1 solubility: precipitation curves
        self.at("Solubility:", 0.1)
        fr, ti, su = panels[0]
        self.play(FadeIn(ti), FadeIn(su), run_time=0.6)
        c = centers[0]
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 1, 0.5], x_length=4.0, y_length=1.4, tips=False,
                  axis_config={"include_numbers": False, "include_ticks": False, "color": GREY}).move_to(c + np.array([0.35, -0.2, 0]))
        xl = T("(NH₄)₂SO₄ (% saturation)", 24, GREY).next_to(ax, DOWN, buff=0.12)
        yl = T("% precip.", 24, GREY).rotate(PI / 2).next_to(ax, LEFT, buff=0.12)
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=0.8)
        sig = lambda x0: (lambda x: 1 / (1 + math.exp(-1.6 * (x - x0))))
        cg = ax.plot(sig(3.4), x_range=[0, 10], color=GREY, stroke_width=5)
        cr = ax.plot(sig(6.6), x_range=[0, 10], color=RED, stroke_width=5)
        self.play(Create(cg), run_time=1.3)
        self.play(Create(cr), run_time=1.3)

        # 2 gel filtration
        self.at("Size:", 0.1)
        fr, ti, su = panels[1]
        self.play(FadeIn(ti), FadeIn(su), run_time=0.6)
        c = centers[1]
        col = Rectangle(width=1.9, height=1.6, color=TEAL, stroke_width=3).move_to(c + np.array([-1.5, -0.2, 0]))
        beads = VGroup(*[Circle(radius=0.11, color=TEAL, fill_color=TEAL, fill_opacity=0.3, stroke_width=1.5).move_to(col.get_center() + np.array([-0.6 + (i % 3) * 0.5 + (0.25 if (i // 3) % 2 else 0), 0.58 - (i // 3) * 0.39, 0])) for i in range(12)])
        self.play(Create(col), FadeIn(beads), run_time=0.8)
        big = marble(RED, 0.2).move_to(col.get_top() + np.array([-0.25, 0.3, 0]))
        small = marble(GREY, 0.12).move_to(col.get_top() + np.array([0.25, 0.3, 0]))
        self.play(FadeIn(big), FadeIn(small), run_time=0.4)
        zig = VMobject()
        yb = col.get_bottom()[1]
        pts = [small.get_center()]
        x0 = col.get_center()[0] + 0.25
        for k in range(1, 7):
            pts.append([x0 + (0.3 if k % 2 else -0.3), small.get_center()[1] - k * 0.2, 0])
        zig.set_points_as_corners(pts)
        out_t = self.until("counterintuitively", 0.0) if False else 3.0
        self.play(big.animate.move_to([col.get_center()[0] - 0.25, yb - 0.4, 0]).set_rate_func(linear),
                  MoveAlongPath(small, zig, rate_func=linear), run_time=3.0)
        big_lab = T("large exits first", 28, RED).move_to(c + np.array([1.5, -0.2, 0]))
        self.play(FadeIn(big_lab), run_time=0.6)

        # 3 ion exchange
        self.at("Charge:", 0.1)
        fr, ti, su = panels[2]
        self.play(FadeIn(ti), FadeIn(su), run_time=0.6)
        c = centers[2]
        bds = VGroup(*[bead("−", 0.4).move_to(c + np.array([-1.9 + 1.0 * i, -0.8, 0])) for i in range(3)])
        self.play(LaggedStart(*[FadeIn(b) for b in bds], lag_ratio=0.2), run_time=0.8)
        pr = blob("+", RED, 1.0, 0.75, 34).move_to(c + np.array([-1.9, 0.45, 0]))
        pg = blob("−", GREY, 1.0, 0.75, 34).move_to(c + np.array([-0.4, 0.55, 0]))
        self.play(FadeIn(pr), FadeIn(pg), run_time=0.4)
        self.play(pr.animate.move_to(bds[0].get_top() + UP * 0.4), pg.animate.move_to(c + np.array([1.55, -0.85, 0])).set_rate_func(linear), run_time=2.0)
        opp = T("opposites\nstick", 28, RED).move_to(c + np.array([1.75, 0.35, 0]))
        self.play(FadeIn(opp), FadeOut(pg, shift=DOWN * 0.5), run_time=0.6)

        # 4 affinity
        self.at("Binding affinity:", 0.1)
        fr, ti, su = panels[3]
        self.play(FadeIn(ti), FadeIn(su), run_time=0.6)
        c = centers[3]
        b4 = Circle(radius=0.42, color=TEAL, fill_color=TEAL, fill_opacity=0.35, stroke_width=3).move_to(c + np.array([-1.5, -0.5, 0]))
        lig = Square(0.24, color=GOLD, fill_color=GOLD, fill_opacity=0.95).move_to(b4.get_top() + UP * 0.12)
        ll = T("ligand", 24, GOLD).next_to(lig, LEFT, buff=0.18).shift(DOWN * 0.12)
        bl4 = T("bead", 24, TEAL).next_to(b4, DOWN, buff=0.12)
        self.play(FadeIn(b4), FadeIn(lig), FadeIn(ll), FadeIn(bl4), run_time=0.8)
        pr4 = blob("", RED, 1.0, 0.75).move_to(c + np.array([-1.5, 0.5, 0]))
        pg4 = blob("", GREY, 1.0, 0.75).move_to(c + np.array([0.0, 0.5, 0]))
        self.play(FadeIn(pr4), FadeIn(pg4), run_time=0.4)
        self.play(pr4.animate.move_to(lig.get_top() + UP * 0.38), pg4.animate.move_to(c + np.array([0.0, -1.0, 0])).set_rate_func(linear), run_time=2.0)
        only = T("only yours\nsticks", 28, RED).move_to(c + np.array([1.7, 0.2, 0]))
        self.play(FadeIn(only), FadeOut(pg4, shift=DOWN * 0.5), run_time=0.6)

        # match
        self.at("Match the method", 0.1)
        self.play(LaggedStart(*[Indicate(p[0], color=YELLOW, scale_factor=1.03) for p in panels], lag_ratio=0.25), run_time=3.0)
        self.finish()


# ---------------------------------------------------------------- S03
class S03Ion(Nar):
    ID = "s03_ion"

    def construct(self):
        # opposites attract demo
        b = bead("−", 0.45).move_to(LEFT * 3.0)
        p = blob("+", RED, 1.3, 0.95, 40).move_to(RIGHT * 3.0)
        self.play(FadeIn(b), FadeIn(p), run_time=0.8)
        self.play(p.animate.next_to(b, RIGHT, buff=0.0), run_time=1.8)
        lab = T("opposites attract", 44).move_to(DOWN * 1.8)
        self.play(FadeIn(lab, shift=UP * 0.15), run_time=0.8)
        self.at("A cation exchanger", 0.4)

        PW = 6.1
        cL, cR = np.array([-3.15, 0, 0]), np.array([3.15, 0, 0])
        frL = RoundedRectangle(corner_radius=0.2, width=PW, height=6.7, color=GREY, stroke_width=2.5).move_to(cL)
        frR = RoundedRectangle(corner_radius=0.2, width=PW, height=6.7, color=GREY, stroke_width=2.5).move_to(cR)
        hL = T("Cation exchanger", 32, weight=BOLD).move_to(cL + UP * 2.85)
        hR = T("Anion exchanger", 32, weight=BOLD).move_to(cR + UP * 2.85)

        # left panel: shrink demo into bead 1
        beadsL = VGroup(*[bead("−", 0.45).move_to(cL + np.array([-1.9 + 1.9 * i, -0.9, 0])) for i in range(3)])
        proL = blob("+", RED, 1.2, 0.9, 40).move_to(beadsL[0].get_top() + UP * 0.45)
        self.play(FadeOut(lab), ReplacementTransform(b, beadsL[0]), ReplacementTransform(p, proL),
                  Create(frL), FadeIn(hL), run_time=1.5)
        self.play(FadeIn(beadsL[1]), FadeIn(beadsL[2]), run_time=0.6)
        negb = T("negative beads", 26, TEAL).move_to(cL + np.array([0, -2.5, 0]))
        self.play(FadeIn(negb), run_time=0.5)
        # second red docks, grey (negative) passes
        pro2 = blob("+", RED, 1.2, 0.9, 40).move_to(cL + np.array([1.9, 1.0, 0]))
        gre = blob("−", GREY, 1.2, 0.9, 40).move_to(cL + np.array([0.0, 1.0, 0]))
        self.play(FadeIn(pro2), FadeIn(gre), run_time=0.4)
        self.play(pro2.animate.move_to(beadsL[2].get_top() + UP * 0.45),
                  gre.animate.move_to(cL + np.array([0.95, -1.6, 0])).set_rate_func(linear), run_time=2.0)
        self.play(FadeOut(gre), run_time=0.5)
        cond = VGroup(M("pH < pI", 32, YELLOW), T("protein is +", 26, RED)).arrange(RIGHT, buff=0.35).move_to(cL + np.array([0, 1.8, 0]))
        self.at("use it when the buffer pH is below", 0.5)
        self.play(FadeIn(cond, shift=DOWN * 0.1), run_time=0.8)

        # right panel
        self.at("An anion exchanger", 0.3)
        beadsR = VGroup(*[bead("+", 0.45).move_to(cR + np.array([-1.9 + 1.9 * i, -0.9, 0])) for i in range(3)])
        self.play(Create(frR), FadeIn(hR), LaggedStart(*[FadeIn(x) for x in beadsR], lag_ratio=0.2), run_time=1.4)
        posb = T("positive beads", 26, TEAL).move_to(cR + np.array([0, -2.5, 0]))
        self.play(FadeIn(posb), run_time=0.5)
        proR1 = blob("−", RED, 1.2, 0.9, 40).move_to(cR + np.array([-1.9, 1.0, 0]))
        proR2 = blob("−", RED, 1.2, 0.9, 40).move_to(cR + np.array([1.9, 1.0, 0]))
        greR = blob("+", GREY, 1.2, 0.9, 40).move_to(cR + np.array([0.0, 1.0, 0]))
        self.play(FadeIn(proR1), FadeIn(proR2), FadeIn(greR), run_time=0.4)
        self.play(proR1.animate.move_to(beadsR[0].get_top() + UP * 0.45), proR2.animate.move_to(beadsR[2].get_top() + UP * 0.45),
                  greR.animate.move_to(cR + np.array([0.95, -1.6, 0])).set_rate_func(linear), run_time=2.2)
        self.play(FadeOut(greR), run_time=0.5)
        condR = VGroup(M("pH > pI", 32, YELLOW), T("protein is −", 26, RED)).arrange(RIGHT, buff=0.35).move_to(cR + np.array([0, 1.8, 0]))
        self.play(FadeIn(condR, shift=DOWN * 0.1), run_time=0.8)

        # release
        self.at("Once bound", 0.3)
        salt = []
        for cc, bds in ((cL, beadsL), (cR, beadsR)):
            for bi in range(3):
                for k in range(3):
                    ang = math.radians(-150 + 60 * k)
                    u = np.array([math.cos(ang), math.sin(ang), 0])
                    d = Dot(radius=0.09, color=YELLOW).move_to(bds[bi].get_center() + 0.95 * u)
                    salt.append((d, bds[bi].get_center() + 0.62 * u))
        lblL = VGroup(T("raise the salt", 30, YELLOW), T("(or shift the pH)", 24, YELLOW)).arrange(DOWN, buff=0.1).move_to(cL + np.array([0, -2.55, 0]))
        lblR = lblL.copy().move_to(cR + np.array([0, -2.55, 0]))
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d, _ in salt], lag_ratio=0.03), FadeOut(negb), FadeOut(posb), FadeIn(lblL), FadeIn(lblR), run_time=1.5)
        self.play(LaggedStart(*[d.animate.move_to(t) for d, t in salt], lag_ratio=0.02), run_time=1.5)
        self.play(proL.animate.shift(UP * 0.75), pro2.animate.shift(UP * 0.75),
                  proR1.animate.shift(UP * 0.75), proR2.animate.shift(UP * 0.75), run_time=2.0)
        self.finish()


# ---------------------------------------------------------------- S04
class S04Gel(Nar):
    ID = "s04_gel"

    def construct(self):
        cx = -1.2
        lane_x = [cx + (i - 2) * 1.1 for i in range(5)]
        gel = Rectangle(width=5.7, height=5.2, color=GREY, fill_color="#1a2233", fill_opacity=1, stroke_width=3).move_to([cx, 0.1, 0])
        wells = VGroup(*[Rectangle(width=0.8, height=0.14, color=GREY, fill_color=BG, fill_opacity=1, stroke_width=1.5).move_to([x, 2.55, 0]) for x in lane_x])
        names = ["ladder", "lysate", "step 1", "step 2", "final"]
        labs = VGroup(*[T(n, 24, GREY).move_to([x, 3.1, 0]) for n, x in zip(names, lane_x)])
        mw_y = lambda mw: 1.7 - (math.log10(150) - math.log10(mw)) * 3.6
        sign_top = M("−", 34, TEXT).move_to([cx + 3.35, 2.55, 0])
        sign_bot = M("+", 34, TEXT).move_to([cx + 3.35, -2.3, 0])
        self.play(FadeIn(gel), FadeIn(wells), FadeIn(labs[:2]), FadeIn(sign_top), FadeIn(sign_bot), run_time=1.2)
        # right callout: SDS coat
        prot = blob("", GREY, 1.3, 0.9).move_to([4.4, 1.7, 0])
        coat = VGroup(*[M("−", 36, YELLOW).move_to(prot.get_center() + np.array([1.05 * math.cos(a), 0.8 * math.sin(a), 0]))
                        for a in np.linspace(0, TAU, 8, endpoint=False)])
        cap = T("SDS coat:\nuniform − charge", 28).move_to([4.4, 0.35, 0])
        self.play(FadeIn(prot), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(c, scale=1.4) for c in coat], lag_ratio=0.08), FadeIn(cap), run_time=1.6)

        lad_mw = [150, 100, 75, 50, 37, 25, 15]
        lys = [(150, GREY, 0.10), (100, GREY, 0.10), (75, GREY, 0.10), (50, RED, 0.10), (37, GREY, 0.10), (25, GREY, 0.10), (20, GREY, 0.10), (15, GREY, 0.10)]
        def band(x, mw, col, h, op=0.9):
            return Rectangle(width=0.85, height=h, color=col, fill_color=col, fill_opacity=op, stroke_width=0).move_to([x, 2.4, 0])
        ladder = [band(lane_x[0], m, TEXT, 0.09, 0.75) for m in lad_mw]
        lysate = [band(lane_x[1], m, c, h) for m, c, h in lys]
        for b in ladder + lysate:
            self.add(b)
        self.at("small proteins migrate faster", 3.2)
        mv = [b.animate(rate_func=smooth).move_to([lane_x[0], mw_y(m), 0]) for b, m in zip(ladder, lad_mw)]
        mv += [b.animate(rate_func=smooth).move_to([lane_x[1], mw_y(m), 0]) for b, (m, _, _) in zip(lysate, lys)]
        arrow = Arrow([cx + 2.0 + 1.15, 1.9, 0], [cx + 2.0 + 1.15, -1.9, 0], color=YELLOW, buff=0, stroke_width=6) if False else None
        self.log("bands start")
        fast = T("small proteins\nrun farther", 28, YELLOW).move_to([4.9, 0.0, 0])
        dn = Arrow([3.0, 1.5, 0], [3.0, -1.5, 0], color=YELLOW, buff=0, stroke_width=6)
        self.play(*mv, FadeOut(coat), FadeOut(prot), FadeOut(cap), run_time=3.0)
        self.log("bands end")
        self.play(FadeIn(fast), GrowArrow(dn), run_time=0.6)
        self.at("Reading it", 1.1)
        self.log("reading")

        # purification lanes
        lanes = [
            [(100, GREY, 0.10), (50, RED, 0.14), (37, GREY, 0.10), (25, GREY, 0.10)],
            [(50, RED, 0.20), (37, GREY, 0.10)],
            [(50, RED, 0.30)],
        ]
        bs = []
        self.play(FadeIn(labs[2:]), FadeOut(fast), FadeOut(dn), run_time=0.4)
        allb = []
        for li, lane in enumerate(lanes):
            for m, c, h in lane:
                b = band(lane_x[2 + li], m, c, h)
                allb.append((b, lane_x[2 + li], m))
                self.add(b)
        self.play(*[b.animate.move_to([x, mw_y(m), 0]) for b, x, m in allb], run_time=1.6)
        cnts = VGroup(*[M(str(n), 30, GREEN).move_to([lane_x[1 + i], -2.85, 0]) for i, n in enumerate([8, 4, 2, 1])])
        fewer = T("fewer bands\n= purer sample", 28, GREEN).move_to([4.4, 0.0, 0])
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cnts], lag_ratio=0.35), FadeIn(fewer), run_time=1.0)

        # position -> molecular weight
        self.at("a band's position", 0.3)
        kd = VGroup(*[M(str(m), 24, TEXT).next_to([gel.get_left()[0], mw_y(m), 0], LEFT, buff=0.14) for m in lad_mw])
        kdh = M("kDa", 24, GREY).move_to([gel.get_left()[0] - 0.42, 3.1, 0])
        self.play(FadeOut(fewer), FadeIn(kd), FadeIn(kdh), run_time=0.8)
        tb = [b for b, x, m in [(lysate[3], 0, 50)]][0]
        guide = DashedLine([lane_x[0] - 0.5, mw_y(50), 0], [lane_x[1] + 0.45, mw_y(50), 0], color=YELLOW, stroke_width=5)
        pos = T("position\n= molecular weight", 28, YELLOW).move_to([4.4, 0.0, 0])
        self.play(Create(guide), FadeIn(pos), run_time=1.0)
        # intensity
        self.at("band intensity", 0.3)
        fin = [b for b, x, m in allb if x == lane_x[4]][0]
        self.play(FadeOut(guide), FadeOut(pos), run_time=0.4)
        inten = T("thicker band\n= more protein", 28, YELLOW).move_to([4.4, 0.0, 0])
        self.play(FadeIn(inten), Indicate(fin, color=YELLOW, scale_factor=1.3), run_time=1.4)
        # goal
        self.at("The goal of a purification", 0.3)
        others = ladder + lysate + [b for b, x, m in allb if x != lane_x[4]]
        goal = T("one band:\none protein", 34, GREEN).move_to([4.4, 0.0, 0])
        self.play(FadeOut(inten), *[o.animate.set_opacity(0.25) for o in others], *[c.animate.set_opacity(0.3) for c in cnts[:3]], FadeIn(goal), run_time=1.2)
        self.play(Indicate(fin, color=GREEN, scale_factor=1.35), SurroundingRectangle(fin, color=GREEN, buff=0.15).animate if False else Wait(0.1), run_time=1.5)
        self.finish()


# ---------------------------------------------------------------- S05
class S05Maldi(Nar):
    ID = "s05_maldi"

    def construct(self):
        tube = RoundedRectangle(corner_radius=0.2, width=7.8, height=1.3, color=GREY, stroke_width=3).move_to([0.1, 0.6, 0])
        plate = Rectangle(width=0.3, height=1.3, color=GREY, fill_color=GREY, fill_opacity=0.8, stroke_width=0).move_to([-3.95, 0.6, 0])
        matrix = Rectangle(width=0.12, height=1.1, color=TEAL, fill_color=TEAL, fill_opacity=0.9, stroke_width=0).next_to(plate, RIGHT, buff=0)
        det = Rectangle(width=0.3, height=1.3, color=GREY, fill_color=GREY, fill_opacity=0.8, stroke_width=0).move_to([4.15, 0.6, 0])
        l1 = T("matrix-coated plate", 24, TEAL).move_to([-3.9, -0.4, 0])
        l2 = T("evacuated flight tube", 24, GREY).move_to([0.1, -0.4, 0])
        l3 = T("detector", 24, GREY).move_to([4.2, -0.4, 0])
        t0 = T("Mass spectrometry weighs molecules", 34).move_to([0, 3.0, 0])
        self.play(FadeIn(t0, shift=DOWN * 0.1), run_time=1.0)
        self.play(FadeIn(plate), FadeIn(matrix), Create(tube), FadeIn(det), FadeIn(l1), FadeIn(l2), FadeIn(l3), run_time=2.0)
        # laser
        self.at("a laser blasts", 0.3)
        self.play(FadeOut(t0), run_time=0.4)
        samp = VGroup(*[marble(RED, 0.07).move_to([-3.8, 0.25 + 0.35 * i, 0]) for i in range(3)])
        self.play(FadeIn(samp), run_time=0.5)
        laser = Line([-5.8, 3.2, 0], [-3.85, 0.6, 0], color=YELLOW, stroke_width=8)
        ll = T("laser", 28, YELLOW).move_to([-4.6, 3.0, 0])
        self.play(Create(laser), FadeIn(ll), run_time=0.7)
        flash = Circle(radius=0.5, color=YELLOW, fill_color=YELLOW, fill_opacity=0.5, stroke_width=0).move_to([-3.8, 0.6, 0])
        self.play(FadeIn(flash, scale=0.4), run_time=0.3)
        self.play(FadeOut(flash, scale=2.0), run_time=0.4)
        ions = VGroup(marble(RED, 0.10).move_to([-3.7, 1.0, 0]), marble(RED, 0.15).move_to([-3.7, 0.6, 0]), marble(RED, 0.21).move_to([-3.7, 0.2, 0]))
        ion_lab = T("ions (bigger = heavier)", 26, RED).move_to([-3.6, 2.0, 0])
        self.play(FadeIn(ions), FadeOut(samp), FadeOut(laser), FadeOut(ll), FadeIn(ion_lab), run_time=0.6)
        # flight
        self.at("the ions fly down", 0.3)
        self.play(FadeOut(ion_lab), run_time=0.3)
        axis = Line([-3.6, -2.6, 0], [4.6, -2.6, 0], color=GREY, stroke_width=3)
        tl = T("time of flight (µs)", 24, GREY).move_to([0.5, -3.25, 0])
        arr = Arrow([4.3, -2.6, 0], [4.7, -2.6, 0], color=GREY, buff=0, stroke_width=3)
        self.play(Create(axis), FadeIn(tl), run_time=0.5)
        arr_x = [-3.5 + 6.5 * math.sqrt(m) / 1.732 for m in (1, 2, 3)]
        spikes = [Line([x, -2.6, 0], [x, -2.6 + h, 0], color=RED, stroke_width=7) for x, h in zip(arr_x, (1.0, 0.8, 0.6))]
        times = [4.4, 6.2, 7.6]
        ys = [1.0, 0.6, 0.2]
        anims = []
        for ion, tm, y, sp in zip(ions, times, ys, spikes):
            anims.append(ion.animate(run_time=tm, rate_func=linear).move_to([4.0, y, 0]))
            anims.append(Succession(Wait(tm), Create(sp, run_time=0.4)))
        heavy = T("heavier ions arrive later", 30, YELLOW).move_to([0.2, 2.0, 0])
        mz = M("m/z ∝ t²", 30, YELLOW).move_to([-2.2, -1.9, 0])
        anims.append(Succession(Wait(self.until("the time of flight", 0.3) if False else 4.0), FadeIn(mz)))
        anims.append(Succession(Wait(6.4), FadeIn(heavy)))
        self.play(AnimationGroup(*anims), run_time=max(times) + 0.4)
        self.play(FadeOut(ions), FadeOut(heavy), FadeOut(mz), run_time=0.4)
        self.at("It needs only", 0.3)
        c1 = chip("picomoles of sample", RED, 28).move_to([-3.2, 3.0, 0])
        c2 = chip("proteins above 10 kDa", RED, 28).move_to([3.0, 3.0, 0])
        self.play(FadeIn(c1, shift=DOWN * 0.1), run_time=0.8)
        self.at("can resolve proteins", 0.3)
        self.play(FadeIn(c2, shift=DOWN * 0.1), run_time=0.8)

        # spectrum
        self.at("Weigh a protein's tryptic", 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        ttl = T("weigh the tryptic peptides", 34).move_to([0, 3.2, 0])
        ax = Axes(x_range=[700, 2300, 200], y_range=[0, 1, 0.5], x_length=9.5, y_length=2.4, tips=False,
                  axis_config={"include_numbers": False, "include_ticks": False, "color": GREY}).move_to([0.3, 0.8, 0])
        xl = T("m/z  (peptide mass, Da)", 24, GREY).next_to(ax, DOWN, buff=0.12)
        yl = T("signal", 24, GREY).rotate(PI / 2).next_to(ax, LEFT, buff=0.12)
        peaks = [(842, 0.55), (1066, 0.9), (1305, 0.45), (1587, 0.75), (1840, 0.5), (2133, 0.65)]
        f = lambda x: sum(h * math.exp(-((x - m) / 9) ** 2) for m, h in peaks)
        curve = ax.plot(f, x_range=[700, 2300, 3], color=RED, stroke_width=4, use_smoothing=False)
        self.play(FadeIn(ttl), Create(ax), FadeIn(xl), FadeIn(yl), run_time=0.8)
        self.play(Create(curve), run_time=1.4)
        labs = VGroup(*[M(str(m), 24, TEXT).next_to(ax.c2p(m, h), UP, buff=0.1) for m, h in peaks])
        self.play(LaggedStart(*[FadeIn(l, shift=DOWN * 0.1) for l in labs], lag_ratio=0.1), run_time=0.8)
        self.at("you can identify it", 1.8)
        ch1 = chip("peptide masses", RED, 26)
        ch2 = chip("database of digests", GREY, 26)
        ch3 = chip("protein identified", GREEN, 26)
        a1 = Arrow(LEFT * 0.4, RIGHT * 0.4, color=YELLOW, buff=0)
        a2 = Arrow(LEFT * 0.4, RIGHT * 0.4, color=YELLOW, buff=0)
        strip = VGroup(ch1, a1, ch2, a2, ch3).arrange(RIGHT, buff=0.3).move_to([0, -2.8, 0])
        self.play(ReplacementTransform(labs.copy(), ch1), FadeIn(strip[1:3]), run_time=1.0)
        self.play(FadeIn(strip[3:]), run_time=0.9)
        self.finish()


class S06End(EndCard):
    LINE = "Run the purification simulator in the lesson yourself."
