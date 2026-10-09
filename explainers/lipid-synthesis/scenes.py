"""Lipid synthesis: from acetyl-CoA to cholesterol, and the dials that keep it in balance
(Biochemistrypedia explainer).  Every cue is a spoken phrase looked up in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = acetyl-CoA, the carbon bricks (the raw material)
  ORANGE = storage fat (triacylglycerol, fatty acid synthesis)
  BLUE   = membranes
  RED    = cholesterol / sterols, and SREBP (the cholesterol sensor)
  TEAL   = HMG-CoA reductase and the synthesis dial it sets (the enzyme)
  GREEN  = energy: AMPK, ATP, the AMP/ATP gauge, the phosphate tag
  PURPLE = mevalonate-derived products (translational feedback)
  GREY   = structure, axes, switched-off things
No molecular structures anywhere: chips, dots, gauges, flows.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

config.disable_caching = True

ORANGE = "#F2994A"
PURPLE = "#B58CD9"
GREY_D = "#3a3f4b"


# ------------------------------------------------------------------ helpers
def toggle(color, on=True, w=0.9, h=0.42):
    """A little switch: rounded track + knob. Knob right = on."""
    r = h / 2
    track = RoundedRectangle(corner_radius=r, width=w, height=h, stroke_color=color, stroke_width=3,
                             fill_color=interpolate_color(ManimColor(BG), ManimColor(color), 0.45 if on else 0.0),
                             fill_opacity=1)
    kx = (w / 2 - r) * (1 if on else -1)
    knob = Circle(radius=r * 0.72, fill_color=color if on else GREY, fill_opacity=1, stroke_width=0)
    knob.move_to(track.get_center() + RIGHT * kx)
    g = VGroup(track, knob)
    g.color_ = color
    g.w_, g.h_ = w, h
    return g


def flip(sw, on):
    track, knob = sw
    r = sw.h_ / 2
    kx = (sw.w_ / 2 - r) * (1 if on else -1)
    fill = interpolate_color(ManimColor(BG), ManimColor(sw.color_), 0.45 if on else 0.0)
    return [knob.animate.move_to(track.get_center() + RIGHT * kx).set_fill(sw.color_ if on else GREY),
            track.animate.set_fill(fill, opacity=1)]


def ptag(size=22, r=0.2):
    c = Circle(radius=r, fill_color=GREEN, fill_opacity=1, stroke_width=0)
    t = T("P", size, BG, weight=BOLD).move_to(c)
    return VGroup(c, t)


def bez(a, b, color, w=7):
    a, b = np.array(a, float), np.array(b, float)
    c = CubicBezier(a, a + RIGHT * 1.0, b - RIGHT * 1.0, b, stroke_color=color, stroke_width=w)
    tip = Triangle(fill_color=color, fill_opacity=1, stroke_width=0).scale(0.17).rotate(-PI / 2).move_to(b + LEFT * 0.1)
    c.tip_m = tip
    return c


# ------------------------------------------------------------------ title / end
class S00Title(TitleCard):
    LESSON = "Lipid synthesis"
    TITLE = "From acetyl-CoA to cholesterol"


class S06End(EndCard):
    LINE = "Four dials on one enzyme keep cholesterol in balance."


# ------------------------------------------------------------------ S01: one carbon unit, three destinations
class S01Fork(SpokenScene):
    def construct(self):
        head = T("One precursor, three destinies", 36, font=TITLE_FONT).to_edge(UP, buff=0.35)
        ac = chip("acetyl-CoA", YELLOW, 30).move_to([-4.9, 0, 0])
        ac_sub = T("2-carbon unit", 24, GREY).next_to(ac, DOWN, buff=0.18)
        F = np.array([-1.7, 0, 0])
        trunk = Line(ac.get_right(), F, color=YELLOW, stroke_width=7)

        dests = [
            ("Storage fat", "triacylglycerols", ORANGE, 1.95),
            ("Membranes", "phospholipids,\nsphingolipids", BLUE, 0.0),
            ("Hormones, signals", "cholesterol, steroids", RED, -1.95),
        ]
        boxes, icons, curves, labels = [], [], [], []
        tips = []
        for name, sub, col, y in dests:
            box = RoundedRectangle(corner_radius=0.18, width=5.35, height=1.55, stroke_color=col, stroke_width=3,
                                   fill_color=col, fill_opacity=0.10).move_to([3.55, y, 0])
            t1 = T(name, 28, col, weight=BOLD)
            t2 = T(sub, 24, TEXT, line_spacing=0.9)
            txt = VGroup(t1, t2).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
            txt.move_to(box.get_center() + RIGHT * 0.45)
            ic_c = box.get_left() + RIGHT * 0.85
            if col == ORANGE:       # lipid droplet
                icon = VGroup(Circle(0.42, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.35),
                              Circle(0.17, stroke_width=0, fill_color=ORANGE, fill_opacity=0.9).shift(UP * 0.12 + LEFT * 0.1))
            elif col == BLUE:       # a cell: a membrane ring around a nucleus-free interior
                icon = VGroup(Circle(0.42, stroke_color=BLUE, stroke_width=7), Circle(0.3, stroke_color=BLUE, stroke_width=2, stroke_opacity=0.5))
            else:                   # signal waves from a source
                icon = VGroup(Dot(radius=0.1, color=RED),
                              *[Arc(radius=r, start_angle=-PI / 3, angle=2 * PI / 3, stroke_color=RED, stroke_width=4) for r in (0.28, 0.46)]).shift(LEFT * 0.2)
            icon.move_to(ic_c)
            boxes.append(box); icons.append(icon); labels.append(txt)
            cv = bez(F, [box.get_left()[0] - 0.05, y, 0], col)
            curves.append(cv); tips.append(cv.tip_m)
        dest_groups = [VGroup(b, i, l) for b, i, l in zip(boxes, icons, labels)]

        # --- build
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.6)
        self.at("acetyl CoA")
        self.play(FadeIn(ac, scale=0.9), run_time=0.5)
        self.play(FadeIn(ac_sub), Create(trunk), run_time=0.6)
        self.at("the cell builds")
        self.play(*[Create(c) for c in curves], *[FadeIn(t) for t in tips], run_time=0.9)
        self.at("pour carbons into")
        self.play(FadeIn(dest_groups[0], shift=LEFT * 0.2), run_time=0.7)
        self.at("It can route them")
        self.play(FadeIn(dest_groups[1], shift=LEFT * 0.2), run_time=0.7)
        self.at("or it can elaborate")
        self.play(FadeIn(dest_groups[2], shift=LEFT * 0.2), run_time=0.7)
        self.at("The same carbons")
        dots = [Dot(radius=0.13, color=YELLOW).move_to(ac.get_right()) for _ in range(3)]
        self.add(*dots)
        self.play(*[MoveAlongPath(d, trunk) for d in dots], run_time=0.5, rate_func=linear)
        self.play(*[MoveAlongPath(d, c) for d, c in zip(dots, curves)], run_time=1.0, rate_func=linear)
        self.play(*[Indicate(g, scale_factor=1.04, color=c[2]) for g, c in zip(dest_groups, dests)], FadeOut(*dots), run_time=0.9)

        # --- the fate is decided by switches, not by the raw material
        self.at("What decides the fate")
        self.play(ac.animate.set_color(GREY), run_time=0.6)
        self.at("but the regulatory switches")
        sw_fed = toggle(ORANGE, True)
        sw_en = toggle(GREEN, True)
        sw_ch = toggle(RED, True)
        p_top = curves[0].point_from_proportion(0.45)
        p_bot = curves[2].point_from_proportion(0.62)
        sw_fed.move_to(p_top)
        sw_ch.move_to(p_bot)
        sw_en.move_to([-2.75, 0, 0])
        self.play(FadeIn(VGroup(sw_fed, sw_en, sw_ch), scale=0.5), run_time=0.7)
        lab_fed = T("fed or fasting", 24, ORANGE).next_to(sw_fed, LEFT, buff=0.2)
        lab_en = T("energy", 24, GREEN).next_to(sw_en, DOWN, buff=0.2)
        lab_ch = T("cholesterol held", 24, RED).next_to(sw_ch, LEFT, buff=0.2)
        self.at("fed or fasting")
        self.play(ac.animate.set_color(YELLOW), FadeIn(lab_fed), run_time=0.3)
        self.at("or fasting")
        self.play(*flip(sw_fed, False), curves[0].animate.set_stroke(opacity=0.25), tips[0].animate.set_fill(opacity=0.25), run_time=0.5)
        self.at("flush with energy")
        self.play(FadeIn(lab_en), run_time=0.4)
        self.at("or starving")
        self.play(*flip(sw_en, False), *[c.animate.set_stroke(opacity=0.25) for c in curves[1:]], *[t.animate.set_fill(opacity=0.25) for t in tips[1:]], trunk.animate.set_stroke(opacity=0.4), run_time=0.5)
        self.wait(0.6)
        self.play(*flip(sw_en, True), *flip(sw_fed, True), *[c.animate.set_stroke(opacity=1) for c in curves], *[t.animate.set_fill(opacity=1) for t in tips], trunk.animate.set_stroke(opacity=1), run_time=0.6)
        self.at("how much cholesterol")
        self.play(FadeIn(lab_ch), run_time=0.4)
        self.at("already hold")
        self.play(*flip(sw_ch, False), curves[2].animate.set_stroke(opacity=0.25), tips[2].animate.set_fill(opacity=0.25), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------ S02: 27 carbons from 18 acetyl-CoA
class S02Carbons(SpokenScene):
    def construct(self):
        # ---- phase A: the product, 27 carbons, all from acetyl-CoA
        chol = chip("cholesterol", RED, 40).move_to([0, 1.9, 0])
        grid = VGroup(*[Dot(radius=0.13, color=RED).move_to([(c - 4) * 0.42, (1 - r) * 0.42, 0]) for r in range(3) for c in range(9)])
        grid.move_to([1.6, 0.3, 0])
        big = T("27", 96, RED, weight=BOLD, font=TITLE_FONT).move_to([-2.4, 0.65, 0])
        carb = T("carbons", 30, TEXT).next_to(big, DOWN, buff=0.12)
        self.play(FadeIn(chol, shift=DOWN * 0.1), run_time=0.7)
        self.at("Every one of its")
        self.play(FadeIn(big, scale=0.8), FadeIn(carb), run_time=0.6)
        self.play(LaggedStartMap(FadeIn, grid, lag_ratio=0.05, scale=0.4), run_time=1.3)
        self.at("traces back to the same")
        self.play(*[d.animate.set_color(YELLOW) for d in grid], big.animate.set_color(YELLOW), run_time=0.9)
        ac = chip("acetyl-CoA", YELLOW, 34).move_to([1.6, -1.7, 0])
        up = Arrow(ac.get_top(), grid.get_bottom() + DOWN * 0.1, buff=0.12, stroke_width=5, color=YELLOW, max_tip_length_to_length_ratio=0.3)
        sub = T("a two-carbon unit", 26, GREY).next_to(ac, RIGHT, buff=0.3)
        self.at("acetyl CoA")
        self.play(FadeIn(ac, shift=UP * 0.15), FadeIn(sub), GrowArrow(up), run_time=0.7)
        self.play(Indicate(grid, color=YELLOW, scale_factor=1.05), run_time=0.8)

        # ---- phase B: 18 acetyl-CoA = 36 carbons; 27 are retained
        self.at("Eighteen acetyl CoA molecules")
        self.play(FadeOut(VGroup(chol, grid, big, carb, ac, sub, up)), run_time=0.4)
        pairs, sqs = [], []
        pitch = 0.68
        x0 = -(17 * pitch) / 2
        for i in range(18):
            o = RoundedRectangle(corner_radius=0.07, width=0.56, height=0.34, stroke_color=YELLOW, stroke_width=2.5,
                                 fill_color=YELLOW, fill_opacity=0.12)
            a = Square(0.2, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to(o.get_center() + LEFT * 0.12)
            b = Square(0.2, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to(o.get_center() + RIGHT * 0.12)
            g = VGroup(o, a, b).move_to([x0 + i * pitch, 1.6, 0])
            pairs.append(g); sqs += [a, b]
        row = VGroup(*pairs)
        row_lab = T("18 acetyl-CoA", 30, YELLOW).move_to([0, 2.55, 0])
        row_sub = T("2 carbons each = 36 carbons", 26, GREY).move_to([0, 0.85, 0])
        self.play(FadeIn(row_lab, shift=DOWN * 0.1), LaggedStartMap(FadeIn, row, lag_ratio=0.05, scale=0.6), run_time=1.5)
        self.at("pooled and condensed")
        self.play(FadeIn(row_sub), Indicate(row, color=YELLOW, scale_factor=1.03), run_time=0.9)
        self.at("27 of those carbons")
        lost = [i for i in range(36) if i % 4 == 3]
        keep = [i for i in range(36) if i % 4 != 3]
        ret = T("27 retained in the final sterol", 28, RED).move_to([0, 0.85, 0])
        self.play(*[sqs[i].animate.set_color(RED) for i in keep], *[sqs[i].animate.set_color(GREY_D) for i in lost],
                  FadeOut(row_sub), run_time=1.0)
        self.play(FadeIn(ret, shift=UP * 0.1), run_time=0.5)

        # ---- three stages
        self.at("The assembly happens in three broad stages")
        st = []
        names = [("stage 1", "activated\nisoprene units", YELLOW), ("stage 2", "squalene", PURPLE if False else YELLOW),
                 ("stage 3", "cholesterol", RED)]
        xs = [-4.4, 0.0, 4.4]
        chips = []
        for (lab, nm, col), x in zip(names, xs):
            c = chip(nm, GREY, 28).move_to([x, -1.55, 0])
            sl = T(lab, 24, GREY).move_to([x, -0.6, 0])
            chips.append((c, sl))
        arrs = [Arrow([xs[i] + 1.75, -1.55, 0], [xs[i + 1] - 1.4, -1.55, 0], buff=0, stroke_width=5, color=GREY, max_tip_length_to_length_ratio=0.3) for i in range(2)]
        self.play(LaggedStart(*[FadeIn(VGroup(c, sl), shift=UP * 0.1) for c, sl in chips], lag_ratio=0.35),
                  *[GrowArrow(a) for a in arrs], run_time=1.6)
        brace = Brace(VGroup(chips[0][0], chips[2][0]), DOWN, color=GREY, buff=0.25)
        steps = T("roughly 30 enzymatic steps", 28, TEXT).next_to(brace, DOWN, buff=0.15)
        self.at("roughly 30 enzymatic steps")
        self.play(GrowFromCenter(brace), FadeIn(steps), run_time=0.9)
        self.at("first building activated")
        self.play(chips[0][0].animate.set_color(YELLOW), run_time=0.6)
        self.at("then chaining them into")
        c2 = T("30 C", 30, YELLOW, weight=BOLD).next_to(chips[1][0], DOWN, buff=0.2).shift(DOWN * 0.0)
        # keep the 30 C label clear of the brace: sit above the chip instead
        c2.move_to([0, -0.05, 0])
        self.play(chips[1][0].animate.set_color(YELLOW), arrs[0].animate.set_color(YELLOW), FadeIn(c2, shift=DOWN * 0.1), run_time=0.7)
        self.at("then folding and trimming")
        c3 = T("27 C", 30, RED, weight=BOLD).move_to([4.4, -0.05, 0])
        self.play(chips[2][0].animate.set_color(RED), arrs[1].animate.set_color(RED), FadeIn(c3, shift=DOWN * 0.1), run_time=0.7)
        self.wait(0.5)

        # ---- the takeaway: small identical bricks, expensive and regulated
        self.at("The takeaway is conceptual")
        self.play(FadeOut(VGroup(*[c for c, _ in chips], *[s for _, s in chips], *arrs, brace, steps, c2, c3, row_lab, ret)), run_time=0.7)
        self.at("A molecule this structurally rich")
        slots = [[(c - 2.5) * 1.62, 1.5 - r * 0.98, 0] for r in range(3) for c in range(6)]
        self.play(*[s_.animate.set_color(YELLOW) for s_ in sqs], run_time=0.4)
        self.play(*[p.animate.scale(2.4).move_to(slots[i]) for i, p in enumerate(pairs)], run_time=1.6)
        brick_lab = T("small, identical bricks", 32, YELLOW).move_to([0, -1.4, 0])
        self.at("built entirely from small")
        self.play(FadeIn(brick_lab, shift=UP * 0.1), run_time=0.6)
        self.at("identical bricks")
        self.play(LaggedStart(*[Indicate(p, color=YELLOW, scale_factor=1.06) for p in pairs], lag_ratio=0.04), run_time=1.4)
        t1 = chip("energetically expensive", ORANGE, 28)
        t2 = chip("heavily regulated", TEAL, 28)
        tg = VGroup(t1, t2).arrange(RIGHT, buff=0.5).move_to([0, -2.5, 0])
        self.at("energetically expensive")
        self.play(FadeIn(t1, shift=UP * 0.1), run_time=0.5)
        self.at("heavily regulated")
        self.play(FadeIn(t2, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ------------------------------------------------------------------ S03: four dials on one enzyme
class S03Dials(SpokenScene):
    def construct(self):
        PY = 1.75   # pipe height
        pipe_top = Line([-6.2, PY + 0.2, 0], [6.2, PY + 0.2, 0], color=GREY, stroke_width=3)
        pipe_bot = Line([-6.2, PY - 0.2, 0], [6.2, PY - 0.2, 0], color=GREY, stroke_width=3)
        pipe_in = T("acetyl-CoA", 24, YELLOW).move_to([-4.3, PY + 0.65, 0])
        pipe_out = T("cholesterol", 24, RED).move_to([4.3, PY + 0.65, 0])
        zone = RoundedRectangle(corner_radius=0.18, width=3.7, height=1.9, stroke_color=TEAL, stroke_width=3.5,
                                fill_color=TEAL, fill_opacity=0.10).move_to([0, PY, 0])
        zlab = T("HMG-CoA reductase", 24, TEAL, weight=BOLD).move_to([0, PY + 0.72, 0])
        slots = [[(i - 3.5) * 0.4, PY - 0.68, 0] for i in range(8)]
        tokens = VGroup(*[RoundedRectangle(corner_radius=0.05, width=0.26, height=0.26, stroke_width=0, fill_color=TEAL, fill_opacity=1).move_to(slots[i]) for i in range(8)])
        active = VGroup(*tokens[:6])
        act = ValueTracker(1.0)

        flow = []
        L = 12.4
        for i in range(9):
            d = Dot(radius=0.11, color=YELLOW)
            d.u = i / 9.0
            flow.append(d)

        def upd(d, dt):
            d.u = (d.u + act.get_value() * 0.085 * dt) % 1.0
            x = -6.2 + L * d.u
            d.move_to([x, PY, 0])
            k = float(np.clip((x + 1.85) / 3.7, 0, 1))
            d.set_color(interpolate_color(ManimColor(YELLOW), ManimColor(RED), k))
            d.set_opacity(1.0 if act.get_value() > 0.02 else 0.0)

        for d in flow:
            d.add_updater(upd)

        # --- cue 1: the enzyme
        self.play(Create(pipe_top), Create(pipe_bot), FadeIn(pipe_in), FadeIn(pipe_out), run_time=0.8)
        self.at("reductase is the")
        self.add(*flow)
        self.play(FadeIn(zone), FadeIn(zlab), LaggedStartMap(FadeIn, active, lag_ratio=0.08, scale=0.5), run_time=1.2)
        self.at("rate limiting")
        self.play(Indicate(zone, color=TEAL, scale_factor=1.03), run_time=0.8)
        statin = T("statin target", 24, GREY).move_to([0, PY - 1.25, 0])
        self.at("the target of statins")
        self.play(FadeIn(statin, shift=UP * 0.1), run_time=0.6)

        # --- cue 2: four control layers (frames first)
        xs = [-4.6, -1.53, 1.53, 4.6]
        CY = -1.0
        frames, nums, conns = [], [], []
        cols = [GREEN, PURPLE, RED, RED]
        for i, (x, col) in enumerate(zip(xs, cols)):
            fr = RoundedRectangle(corner_radius=0.15, width=3.0, height=2.1, stroke_color=GREY, stroke_width=2.5,
                                  fill_color=GREY, fill_opacity=0.05).move_to([x, CY - 0.1, 0])
            nm = T(str(i + 1), 26, GREY, weight=BOLD).move_to(fr.get_corner(UL) + RIGHT * 0.32 + DOWN * 0.32)
            cn = DashedLine([0.0 + (x * 0.25), PY - 0.95, 0], [x, CY + 0.95, 0], color=GREY, stroke_width=2.5, dash_length=0.1)
            frames.append(fr); nums.append(nm); conns.append(cn)
        self.at("the cell guards it")
        self.play(FadeOut(statin), LaggedStart(*[Create(c) for c in conns], lag_ratio=0.1), run_time=0.9)
        self.at("four independent control layers")
        self.play(LaggedStart(*[FadeIn(VGroup(f, n)) for f, n in zip(frames, nums)], lag_ratio=0.15), run_time=1.2)
        axis = Arrow([-5.3, -2.7, 0], [5.3, -2.7, 0], buff=0, stroke_width=4, color=GREY, max_tip_length_to_length_ratio=0.05)
        fast = T("fast", 24, GREY).align_to([-6.3, 0, 0], LEFT).set_y(-2.7)
        slow = T("slow", 24, GREY).align_to([6.3, 0, 0], RIGHT).set_y(-2.7)
        tsc = T("time scale", 24, GREY).move_to([0, -3.2, 0])
        self.at("on different time scales")
        self.play(GrowArrow(axis), FadeIn(fast), FadeIn(slow), FadeIn(tsc), run_time=0.9)

        def fill_card(i, l1, l2, l3):
            fr = frames[i]
            t1 = T(l1, 24, cols[i], weight=BOLD)
            t2 = T(l2, 22, TEXT, line_spacing=0.85)
            t3 = T(l3, 22, GREY)
            g = VGroup(t1, t2, t3).arrange(DOWN, buff=0.07)
            if g.width > fr.width - 0.3:
                g.scale_to_fit_width(fr.width - 0.3)
            g.move_to(fr.get_center() + DOWN * 0.12)
            return [fr.animate.set_stroke(cols[i]).set_fill(cols[i], opacity=0.10), nums[i].animate.set_color(cols[i]),
                    conns[i].animate.set_color(cols[i]), FadeIn(g)], g

        # --- 1 phosphorylation
        a1, g1 = fill_card(0, "Phosphorylation", "AMPK, low energy", "seconds to minutes")
        self.at("Fastest is phosphorylation")
        self.play(*a1, run_time=0.8)
        self.at("switches the enzyme off")
        P = ptag().move_to(zone.get_corner(UR))
        self.play(FadeIn(P, scale=0.5), active.animate.set_color(GREY).set_opacity(0.4), act.animate.set_value(0.0), run_time=0.9)
        self.at("Slower is translational")
        self.play(FadeOut(P), active.animate.set_color(TEAL).set_opacity(1), act.animate.set_value(1.0), run_time=0.5)

        # --- 2 translation
        a2, g2 = fill_card(1, "Translation", "mevalonate\nproducts", "minutes to hours")
        self.play(*a2, run_time=0.8)
        self.at("derived products")
        self.play(Indicate(g2[1], color=PURPLE, scale_factor=1.08), run_time=0.7)
        self.at("suppress the messenger RNA")
        self.play(FadeOut(tokens[4]), FadeOut(tokens[5]), act.animate.set_value(4 / 6), run_time=0.8)
        active.remove(tokens[4], tokens[5])

        # --- 3 transcription
        a3, g3 = fill_card(2, "Transcription", "SREBP", "hours")
        self.at("Slower still is transcriptional")
        self.play(*a3, run_time=0.8)
        self.at("tuning enzyme amount")
        new = [tokens[4], tokens[5], tokens[6], tokens[7]]
        for t in new:
            t.set_opacity(1)
        self.play(LaggedStart(*[FadeIn(t, scale=0.4) for t in new], lag_ratio=0.12), act.animate.set_value(8 / 6), run_time=1.0)
        active.add(*new)

        # --- 4 degradation
        a4, g4 = fill_card(3, "Degradation", "sterol-induced", "hours")
        self.at("and finally")
        self.play(*a4, run_time=0.8)
        self.at("accelerates destruction")
        gone = list(active)[2:]
        self.play(LaggedStart(*[t.animate.shift(DOWN * 0.3).set_opacity(0) for t in gone], lag_ratio=0.08), act.animate.set_value(2 / 6), run_time=1.5)
        self.at("Four dials")
        flash = [f.animate.set_stroke(width=5) for f in frames]
        self.play(*flash, *[Indicate(g, color=WHITE, scale_factor=1.03) for g in (g1, g2, g3, g4)], run_time=0.9)
        self.play(*[f.animate.set_stroke(width=2.5) for f in frames], run_time=0.3)
        self.at("one enzyme")
        self.play(*[t.animate.shift(UP * 0.3).set_opacity(1) for t in gone], act.animate.set_value(1.0), Indicate(zone, color=TEAL, scale_factor=1.03), run_time=0.9)
        self.at("Cholesterol is essential")
        head = T("essential, but toxic in excess", 34, TEXT, font=TITLE_FONT).move_to([0, 3.2, 0])
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.7)
        self.finish()


# ------------------------------------------------------------------ S04: the thermostat
class S04Thermostat(SpokenScene):
    def construct(self):
        c = ValueTracker(0.5)    # membrane cholesterol level (the bar)
        e = ValueTracker(1.0)    # energy (ATP) level (the bar)
        ca = ValueTracker(0.5)   # the cholesterol signal as the dial sees it (lags the bar until the words say so)
        ea = ValueTracker(1.0)

        def s_of(cv, ev):
            return (1.0 / (1.0 + (cv / 0.45) ** 3)) * ev ** 1.2

        CX, CYD, R = 0.0, 0.2, 2.1
        arc = Arc(radius=R, start_angle=0, angle=PI, stroke_color=GREY, stroke_width=6).move_arc_center_to([CX, CYD, 0])
        ticks = VGroup(*[Line([CX + (R - 0.18) * np.cos(a), CYD + (R - 0.18) * np.sin(a), 0],
                              [CX + R * np.cos(a), CYD + R * np.sin(a), 0], color=GREY, stroke_width=4)
                         for a in np.linspace(0, PI, 9)])
        lo = T("less", 26, GREY).move_to([CX - R, CYD - 0.4, 0])
        hi = T("more", 26, GREY).move_to([CX + R, CYD - 0.4, 0])
        dial_lab = T("cholesterol synthesis", 30, TEAL, weight=BOLD).move_to([CX, CYD - 1.05, 0])
        hub = Dot(radius=0.14, color=TEAL).move_to([CX, CYD, 0])

        def needle():
            a = PI * (1 - s_of(ca.get_value(), ea.get_value()))
            return Line([CX, CYD, 0], [CX + (R - 0.35) * np.cos(a), CYD + (R - 0.35) * np.sin(a), 0], color=TEAL, stroke_width=8)
        nd = always_redraw(needle)
        dial = VGroup(arc, ticks, lo, hi, dial_lab)

        # --- sensors
        LX, RX = -4.8, 4.8
        BH, BW = 2.3, 0.55
        BY = 0.35
        l_title = T("SREBP", 32, RED, weight=BOLD).move_to([LX, 2.75, 0])
        l_sub = T("senses cholesterol", 24, RED).move_to([LX, 2.25, 0])
        l_frame = Rectangle(width=BW, height=BH, stroke_color=RED, stroke_width=3).move_to([LX, BY, 0])
        l_fill = always_redraw(lambda: Rectangle(width=BW, height=max(0.02, BH * c.get_value()), stroke_width=0, fill_color=RED, fill_opacity=0.85)
                               .move_to([LX, BY - BH / 2 + max(0.02, BH * c.get_value()) / 2, 0]))
        l_cap = T("membrane\ncholesterol", 24, GREY, line_spacing=0.9).move_to([LX, BY - BH / 2 - 0.65, 0])
        r_title = T("AMPK", 32, GREEN, weight=BOLD).move_to([RX, 2.75, 0])
        r_sub = T("senses energy", 24, GREEN).move_to([RX, 2.25, 0])
        ax_, bx_ = RX - 0.55, RX + 0.55
        r_f1 = Rectangle(width=BW, height=BH, stroke_color=GREEN, stroke_width=3).move_to([ax_, BY, 0])
        r_f2 = Rectangle(width=BW, height=BH, stroke_color=GREEN, stroke_width=3).move_to([bx_, BY, 0])
        r_atp = always_redraw(lambda: Rectangle(width=BW, height=max(0.02, BH * e.get_value()), stroke_width=0, fill_color=GREEN, fill_opacity=0.85)
                              .move_to([ax_, BY - BH / 2 + max(0.02, BH * e.get_value()) / 2, 0]))
        r_amp = always_redraw(lambda: Rectangle(width=BW, height=max(0.02, BH * (1 - e.get_value())), stroke_width=0, fill_color=interpolate_color(ManimColor(GREEN), ManimColor(WHITE), 0.45), fill_opacity=0.85)
                              .move_to([bx_, BY - BH / 2 + max(0.02, BH * (1 - e.get_value())) / 2, 0]))
        l_atp = T("ATP", 24, GREY).move_to([ax_, BY - BH / 2 - 0.35, 0])
        l_amp = T("AMP", 24, GREY).move_to([bx_, BY - BH / 2 - 0.35, 0])
        in_l = Arrow([LX + 1.0, 1.2, 0], [CX - R + 0.25, 1.2, 0], buff=0.05, stroke_width=5, color=RED, max_tip_length_to_length_ratio=0.2)
        in_r = Arrow([RX - 1.55, 1.2, 0], [CX + R - 0.25, 1.2, 0], buff=0.05, stroke_width=5, color=GREEN, max_tip_length_to_length_ratio=0.2)

        # --- build the dial
        self.play(Create(arc), Create(ticks), run_time=1.0)
        self.add(nd, hub)
        self.play(FadeIn(lo), FadeIn(hi), FadeIn(dial_lab), FadeIn(hub), run_time=0.7)
        self.at("with two sensors")
        self.play(FadeIn(VGroup(l_title, l_sub, l_frame, l_cap)), FadeIn(VGroup(r_title, r_sub, r_f1, r_f2, l_atp, l_amp)),
                  run_time=1.0)
        self.add(l_fill, r_atp, r_amp)
        self.at("feeding one dial")
        self.play(GrowArrow(in_l), GrowArrow(in_r), run_time=0.8)

        # --- SREBP
        self.at("SREBP senses cholesterol")
        self.play(Indicate(VGroup(l_title, l_sub), color=RED, scale_factor=1.08), run_time=0.8)
        self.at("low on cholesterol")
        self.play(c.animate.set_value(0.12), run_time=1.5)
        self.at("SREBP turns synthesis up")
        self.play(ca.animate.set_value(0.12), Indicate(in_l, color=RED, scale_factor=1.15), run_time=1.3)

        # --- AMPK
        self.at("AMPK senses energy")
        self.play(Indicate(VGroup(r_title, r_sub), color=GREEN, scale_factor=1.08), run_time=0.8)
        self.at("When ATP runs low")
        self.play(e.animate.set_value(0.12), run_time=1.6)
        self.at("AMPK turns synthesis down")
        self.play(ea.animate.set_value(0.12), Indicate(in_r, color=GREEN, scale_factor=1.15), run_time=1.3)
        famine = T("famine", 28, GREEN).move_to([CX, -2.35, 0])
        self.at("during a famine")
        self.play(FadeIn(famine, shift=UP * 0.1), run_time=0.5)

        # --- converge
        self.at("The two inputs converge")
        self.play(FadeOut(famine), e.animate.set_value(0.75), c.animate.set_value(0.4), ea.animate.set_value(0.75), ca.animate.set_value(0.4), run_time=1.0)
        self.play(Indicate(in_l, color=RED, scale_factor=1.12), Indicate(in_r, color=GREEN, scale_factor=1.12), run_time=0.9)
        t_dem = T("demand", 28, RED).move_to([LX, -2.35, 0])
        t_sup = T("supply", 28, TEAL).move_to([CX, -2.35, 0])
        t_aff = T("affordability", 28, GREEN).move_to([RX, -2.35, 0])
        self.at("balancing supply against")
        self.play(FadeIn(t_sup, shift=UP * 0.1), run_time=0.5)
        self.at("both demand")
        self.play(FadeIn(t_dem, shift=UP * 0.1), run_time=0.5)
        self.at("affordability")
        self.play(FadeIn(t_aff, shift=UP * 0.1), run_time=0.5)

        # --- high cholesterol
        self.at("High cholesterol pushes")
        self.play(e.animate.set_value(1.0), c.animate.set_value(0.9), ea.animate.set_value(1.0), ca.animate.set_value(0.9), run_time=1.4)
        self.at("Low energy does the same")
        self.play(c.animate.set_value(0.5), ca.animate.set_value(0.5), run_time=0.6)
        self.play(e.animate.set_value(0.12), ea.animate.set_value(0.12), run_time=1.4)

        # --- matched
        self.at("The cell is not maximizing")
        self.play(e.animate.set_value(0.9), c.animate.set_value(0.35), ea.animate.set_value(0.9), ca.animate.set_value(0.35), run_time=1.0)
        final = T("production matched to need", 34, TEXT, font=TITLE_FONT).move_to([0, -3.2, 0])
        self.at("matching production precisely")
        self.play(FadeIn(final, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ------------------------------------------------------------------ S05: AMPK triage
class S05Triage(SpokenScene):
    def construct(self):
        # --- gauge (AMP/ATP) on the left
        GX, GY, R = -4.75, 0.3, 1.4
        arc = Arc(radius=R, start_angle=0, angle=PI, stroke_color=GREEN, stroke_width=6).move_arc_center_to([GX, GY, 0])
        hot = Arc(radius=R, start_angle=0, angle=PI * 0.28, stroke_color=GREEN, stroke_width=14).move_arc_center_to([GX, GY, 0])
        ticks = VGroup(*[Line([GX + (R - 0.16) * np.cos(a), GY + (R - 0.16) * np.sin(a), 0],
                              [GX + R * np.cos(a), GY + R * np.sin(a), 0], color=GREEN, stroke_width=3)
                         for a in np.linspace(0, PI, 7)])
        g_lab = T("AMP / ATP", 28, GREEN, weight=BOLD).move_to([GX, GY - 0.65, 0])
        g_sub = T("ratio", 24, GREY).move_to([GX, GY - 1.1, 0])
        ang = ValueTracker(0.14)

        def nd():
            a = PI * (1 - ang.get_value())
            return Line([GX, GY, 0], [GX + (R - 0.3) * np.cos(a), GY + (R - 0.3) * np.sin(a), 0], color=GREEN, stroke_width=7)
        needle = always_redraw(nd)
        hub = Dot(radius=0.12, color=GREEN).move_to([GX, GY, 0])
        low_t = T("low energy state", 26, GREEN).move_to([GX, GY - 1.7, 0])

        # --- AMPK + lamp
        AX, AY = -1.35, 0.3
        ampk = chip("AMPK", GREEN, 34).move_to([AX, AY, 0])
        lamp = Circle(radius=0.24, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.0).move_to([AX, AY + 1.0, 0])
        lamp_t = T("low-fuel warning light", 22, GREY).next_to(lamp, UP, buff=0.12)
        a_in = Arrow([GX + R + 0.15, AY, 0], ampk.get_left() + LEFT * 0.05, buff=0, stroke_width=5, color=GREEN, max_tip_length_to_length_ratio=0.3)

        # --- targets
        rows = [(1.55, "HMG-CoA\nreductase", "cholesterol\nsynthesis", RED),
                (-0.95, "acetyl-CoA\ncarboxylase", "fatty acid\nsynthesis", ORANGE)]
        enz, outs, arrs, bars = [], [], [], []
        for y, en, out, col in rows:
            e_ = chip(en, TEAL, 24).move_to([1.95, y, 0])
            o_ = chip(out, col, 24).move_to([5.0, y, 0])
            ar = Arrow(e_.get_right(), o_.get_left(), buff=0.08, stroke_width=5, color=GREY, max_tip_length_to_length_ratio=0.3)
            enz.append(e_); outs.append(o_); arrs.append(ar)

        self.play(FadeIn(ampk, scale=0.9), run_time=0.6)
        self.play(FadeIn(lamp), FadeIn(lamp_t), run_time=0.6)
        self.at("reads the AMP")
        self.play(Create(arc), Create(ticks), FadeIn(g_lab), FadeIn(g_sub), FadeIn(hub), GrowArrow(a_in), run_time=1.2)
        self.add(needle)
        self.at("When that ratio climbs")
        self.play(ang.animate.set_value(0.8), run_time=1.6)
        self.at("signaling a low energy state")
        self.play(FadeIn(hot), FadeIn(low_t, shift=UP * 0.1), run_time=0.7)
        self.at("AMPK becomes active")
        glow = Circle(radius=0.5, stroke_color=GREEN, stroke_width=3).move_to(lamp)
        self.play(lamp.animate.set_fill(GREEN, opacity=0.95), ampk[0].animate.set_fill(GREEN, opacity=0.5), Flash(lamp, color=GREEN, flash_radius=0.6, line_length=0.18), run_time=0.9)
        self.at("starts phosphorylating")
        self.play(*[FadeIn(VGroup(e_, o_, ar), shift=LEFT * 0.15) for e_, o_, ar in zip(enz, outs, arrs)], run_time=0.7)
        self.at("the expensive biosynthetic enzymes")
        self.play(*[Indicate(e_, color=TEAL, scale_factor=1.08) for e_ in enz], run_time=0.9)

        def block(i):
            ar = arrs[i]
            mid = ar.get_center()
            tb = VGroup(Line(mid + UP * 0.32, mid + DOWN * 0.32, color=TEXT, stroke_width=8)).move_to(mid)
            return tb

        tags = []

        def shut(i, out_name_color):
            p = ptag().move_to(enz[i].get_corner(UL) + LEFT * 0.05 + UP * 0.05)
            fly = ptag().move_to(ampk.get_right())
            self.add(fly)
            self.play(fly.animate.move_to(p.get_center()), run_time=0.7)
            self.remove(fly)
            self.add(p)
            tags.append(p)
            self.play(enz[i].animate.set_color(GREY).set_opacity(0.55), run_time=0.5)

        self.at("It shuts down")
        shut(0, RED)
        bar0 = block(0)
        self.at("halting cholesterol synthesis")
        self.play(arrs[0].animate.set_opacity(0.3), GrowFromCenter(bar0), outs[0].animate.set_opacity(0.55), run_time=0.7)
        self.at("and it inactivates")
        shut(1, ORANGE)
        bar1 = block(1)
        self.at("halting fatty acid")
        self.play(arrs[1].animate.set_opacity(0.3), GrowFromCenter(bar1), outs[1].animate.set_opacity(0.55), run_time=0.7)

        # --- logic: don't spend ATP you don't have
        self.at("The logic is blunt")
        lg = T("no ATP to spare: don't build", 34, TEXT, font=TITLE_FONT).move_to([0.9, -2.45, 0])
        self.play(FadeIn(lg, shift=UP * 0.1), run_time=0.7)
        self.at("Do not spend ATP")
        self.play(Indicate(ampk, color=GREEN, scale_factor=1.08), run_time=0.7)
        self.at("storage and membrane molecules")
        self.play(*[Indicate(o_, color=c_, scale_factor=1.1) for o_, c_ in zip(outs, (RED, ORANGE))], run_time=1.0)
        self.at("do not have ATP to spare")
        self.play(Indicate(VGroup(arc, hot, g_lab, g_sub), color=GREEN, scale_factor=1.06), run_time=0.9)
        self.at("This is metabolic triage")
        self.play(Indicate(lg, color=GREEN, scale_factor=1.05), run_time=0.8)
        self.at("energy charge is monitored")
        self.play(ang.animate.set_value(0.84), run_time=0.5)
        self.play(ang.animate.set_value(0.76), run_time=0.5)
        self.play(ang.animate.set_value(0.82), run_time=0.5)
        self.at("the moment reserves dip")
        self.play(ang.animate.set_value(0.92), run_time=0.7)
        self.at("pulls the brake")
        brake = T("brake on anabolism", 30, GREEN, weight=BOLD).move_to([0.9, -3.05, 0])
        self.play(FadeIn(brake, shift=UP * 0.1), Indicate(ampk, color=GREEN, scale_factor=1.12), run_time=0.8)
        self.at("across multiple pathways")
        self.play(Indicate(VGroup(bar0, bar1), color=GREEN, scale_factor=1.15), run_time=0.9)
        self.finish()
