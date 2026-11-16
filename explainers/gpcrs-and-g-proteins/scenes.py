"""How a Receptor Loads a Switch — one carried, schematic membrane world.

Colour map: receptor BLUE; agonist GOLD; G-alpha PURPLE; beta-gamma TEAL;
GDP GREY; GTP GREEN.  Proteins are labelled cartoons, never structures.
"""
from bp_parts import *


PURPLE = "#B58CD9"
MEM_Y = 0.45


def arrow_between(a, b, color=TEXT, width=5, buff=0.12):
    return Arrow(a, b, buff=buff, color=color, stroke_width=width,
                 tip_length=0.22, max_tip_length_to_length_ratio=0.35)


def flow_markers(paths, colors, per_path=3, speed=0.28, radius=0.11):
    """Dots that repeatedly traverse real pathway arrows, showing signal flow."""
    paths = list(paths)
    colors = list(colors) if isinstance(colors, (list, tuple)) else [colors] * len(paths)
    dots = VGroup()
    for i, (path, color) in enumerate(zip(paths, colors)):
        for j in range(per_path):
            d = Dot(path.point_from_proportion(j / per_path), radius=radius, color=color)
            d.path, d.phase = path, (j / per_path + i * 0.07) % 1.0
            dots.add(d)

    def advance(group, dt):
        for d in group:
            d.phase = (d.phase + speed * dt) % 1.0
            d.move_to(d.path.point_from_proportion(d.phase))
    dots.add_updater(advance)
    return dots


def wave_bars(bars, amp=0.08, speed=3.2):
    """A small travelling displacement through a receptor bundle."""
    for i, bar in enumerate(bars):
        base = bar.get_center().copy()
        bar._wave_t = i * 0.35

        def wave(mob, dt, base=base):
            mob._wave_t += dt
            mob.move_to(base + UP * amp * np.sin(speed * mob._wave_t))
        bar.add_updater(wave)
    return bars


def membrane():
    """The membrane used in every close view."""
    wash = Rectangle(width=13.0, height=1.52, stroke_width=0,
                     fill_color=GREY, fill_opacity=0.22).move_to([0, MEM_Y, 0])
    top = Line([-6.5, MEM_Y + 0.78, 0], [6.5, MEM_Y + 0.78, 0], color=GREY, stroke_width=4)
    bottom = Line([-6.5, MEM_Y - 0.78, 0], [6.5, MEM_Y - 0.78, 0], color=GREY, stroke_width=4)
    lipids = VGroup(*[Dot([x, MEM_Y + s * 0.55, 0], radius=0.035, color=GREY).set_opacity(0.45)
                      for x in np.linspace(-6.35, 6.35, 25) for s in (-1, 1)])
    return VGroup(wash, top, bottom, lipids)


def receptor_bundle(center=(-1.2, MEM_Y, 0), scale=1.0, active=False, labels=False):
    """Seven bars and one continuous path; helix 6 is the moving cytoplasmic bar."""
    cx, cy, _ = center
    xs = [cx + (i - 3) * 0.55 * scale for i in range(7)]
    bars = VGroup()
    for i, x in enumerate(xs):
        h = (2.35 if i not in (2, 3, 4) else 1.85) * scale
        y = cy - (0.15 * scale if i in (2, 3, 4) else 0)
        bar = RoundedRectangle(corner_radius=0.2 * scale, width=0.34 * scale, height=h,
                               stroke_color=BLUE, stroke_width=4,
                               fill_color=BLUE, fill_opacity=0.38).move_to([x, y, 0])
        bars.add(bar)
    if active:
        bars[5].rotate(23 * DEGREES, about_point=bars[5].get_top())
    pts = []
    for i, bar in enumerate(bars):
        pts.extend([bar.get_top(), bar.get_bottom()] if i % 2 == 0 else [bar.get_bottom(), bar.get_top()])
    chain = VMobject(color=BLUE, stroke_width=3, stroke_opacity=0.75).set_points_as_corners(pts)
    group = VGroup(bars) if labels else VGroup(chain, bars)
    group.bars, group.chain = bars, chain
    if labels:
        nums = VGroup(*[boxed_label(str(i + 1), BLUE, 24, box=(0.48, 0.48), pad=0.09)
                        .move_to([xs[i], 3.18, 0]) for i in range(7)])
        group.add(nums)
        group.nums = nums
    return group


def agonist(at=(-1.2, 2.55, 0), text="agonist"):
    g = boxed_label(text, GOLD, size=28, pad=0.2).move_to(at)
    return g


def nucleotide(text="GDP", color=GREY, at=(0, 0, 0)):
    g = boxed_label(text, color, size=26, box=(1.0, 0.52), pad=0.12).move_to(at)
    g.box.set_fill(BG, 1.0)
    return g


def gprotein(center=(-0.25, -2.05, 0), nucleotide_text="GDP", nucleotide_color=GREY,
             joined=True, tail=True):
    """A fitted alpha/nucleotide block and the adjacent beta-gamma unit."""
    cx, cy, _ = center
    body = Ellipse(width=2.45, height=1.35, stroke_width=0,
                   fill_color=PURPLE, fill_opacity=0.48).move_to([cx - 0.55, cy, 0])
    ga = T("G-alpha", 28, PURPLE, weight=BOLD).move_to(body.get_center() + UP * 0.16 + RIGHT * 0.22)
    nuc = nucleotide(nucleotide_text, nucleotide_color, body.get_center() + DOWN * 0.43)
    tail_m = Line([cx - 0.55, cy + 0.72, 0], [cx - 0.55, cy + 1.55, 0],
                  color=PURPLE, stroke_width=10)
    bx = cx + (1.95 if joined else 2.85)
    bg = RoundedRectangle(corner_radius=0.38, width=2.25, height=1.2,
                          stroke_color=TEAL, stroke_width=4,
                          fill_color=TEAL, fill_opacity=0.28).move_to([bx, cy, 0])
    bgl = T("beta-gamma", 24, TEAL, weight=BOLD).move_to(bg)
    group = VGroup(body, ga, nuc, bg, bgl)
    if tail:
        group.add(tail_m)
    group.body, group.ga, group.nuc, group.bg, group.bgl, group.tail = body, ga, nuc, bg, bgl, tail_m
    return group


def opening_world(question=True):
    """Exact carried frame for s01–s03."""
    mem = membrane()
    rec = receptor_bundle(center=(-1.55, MEM_Y, 0), scale=0.9)
    lig = agonist((-1.55, 2.62, 0))
    gp = gprotein(center=(-0.6, -2.25, 0), joined=True)
    rlab = T("7-pass GPCR", 28, BLUE).move_to([-4.6, 1.75, 0])
    lead = arrow_between(rlab.get_right() + RIGHT * 0.16, rec.get_left() + UP * 0.5,
                         BLUE, width=3, buff=0.02)
    qarr = DashedLine([-6.0, 2.5, 0], [-6.0, -1.85, 0], color=TEXT, stroke_width=5,
                      dash_length=0.18)
    qtip = Triangle(color=TEXT, fill_color=TEXT, fill_opacity=1).scale(0.13).rotate(PI).move_to(qarr.get_end())
    q = fit_text("How does binding outside load a switch inside?", max_w=7.0, size=34,
                 color=TEXT).move_to([3.0, 3.28, 0])
    g = VGroup(mem, rec, lig, gp, rlab, lead, qarr, qtip)
    if question:
        g.add(q)
    g.mem, g.rec, g.lig, g.gp, g.qarr, g.qtip, g.question = mem, rec, lig, gp, qarr, qtip, q
    return g


def active_receptor_world(with_trimer=False, nucleotide_text="GDP", nucleotide_color=GREY, labels=False):
    """Exact carried close view for s04–s06."""
    mem = membrane()
    rec = receptor_bundle(center=(-1.65, MEM_Y, 0), scale=1.25, active=True, labels=labels)
    lig = agonist((-1.65, 2.45, 0))
    cavity = DashedVMobject(Ellipse(width=1.2, height=0.72).move_to([0.12, -0.82, 0]),
                            num_dashes=24).set_color(TEXT).set_stroke(width=3)
    g = VGroup(mem, rec, lig, cavity)
    if with_trimer:
        gp = gprotein(center=(0.1, -2.15, 0), nucleotide_text=nucleotide_text,
                      nucleotide_color=nucleotide_color, joined=True)
        g.add(gp)
        g.gp = gp
    g.mem, g.rec, g.lig, g.cavity = mem, rec, lig, cavity
    return g


def family_chip(text, x, y, color=PURPLE):
    return boxed_label(text, color, size=25, box=(1.55, 0.58), pad=0.12).move_to([x, y, 0])


def pathway_hourglass(outputs=True):
    """Carried schematic for s08–s09."""
    receptors = VGroup(*[RoundedRectangle(corner_radius=0.15, width=0.45, height=1.0,
                                          stroke_color=BLUE, fill_color=BLUE, fill_opacity=0.3)
                         for _ in range(4)]).arrange(DOWN, buff=0.18).move_to([-5.25, 0.45, 0])
    fams = VGroup(family_chip("Gs", -1.5, 2.0), family_chip("Gi/o", -1.5, 0.85),
                  family_chip("Gq/11", -1.5, -0.3), family_chip("G12/13", -1.5, -1.45),
                  family_chip("beta-gamma", -1.5, -2.6, TEAL))
    in_arrows = VGroup(*[arrow_between(receptors.get_right(), f.get_left(), GREY, 3) for f in fams])
    group = VGroup(receptors, fams, in_arrows)
    if outputs:
        outs = VGroup(family_chip("cAMP up", 3.55, 2.0, GREEN),
                      family_chip("cAMP down", 3.55, 0.85, GOLD),
                      family_chip("calcium up", 3.55, -0.3, RED),
                      family_chip("Rho GEF", 3.55, -1.45, TEXT),
                      family_chip("K+ channel", 3.55, -2.6, TEAL))
        out_arrows = VGroup(*[arrow_between(f.get_right(), o.get_left(), f.box.get_color(), 3)
                              for f, o in zip(fams, outs)])
        group.add(outs, out_arrows)
        group.outs, group.out_arrows = outs, out_arrows
    group.receptors, group.fams, group.in_arrows = receptors, fams, in_arrows
    return group


class S01Hook(SpokenScene, TitleCard):
    LESSON = "GPCRs and G Proteins"
    TITLE = "How a Receptor Loads a Switch"

    def construct(self):
        w = opening_world()
        self.add(w.mem)
        self.at("How can binding")
        self.play(FadeIn(w.lig, shift=DOWN * 0.25), FadeIn(w.rec), run_time=1.0)
        bob(w.lig, amp=0.16, speed=3.0)
        self.play(FadeIn(w.gp, shift=UP * 0.2), run_time=0.8)
        self.play(Create(w.qarr), FadeIn(w.qtip), run_time=0.8)
        pulse(w.qarr, base=5, amp=1.5, speed=2.2)
        self.at("Follow one membrane")
        self.play(FadeIn(w.question), FadeIn(w[4]), GrowArrow(w[5]), run_time=0.8)
        self.play(Indicate(w.lig, color=GOLD, scale_factor=1.08), run_time=1.0)
        self.finish()


class S02Predict(Scene):
    def construct(self):
        w = opening_world()
        self.add(w)
        bob(w.lig, amp=0.16, speed=3.0)
        bob(w.gp, amp=0.15, speed=2.8, seed=2)
        pulse(w.qarr, base=5, amp=1.5, speed=2.2)
        self.wait(4.5)


class S03Title(Scene):
    def construct(self):
        w = opening_world(question=False).set_opacity(0.35)
        bob(w.lig, amp=0.04, speed=1.7)
        title = fit_text("How a Receptor Loads a Switch", max_w=11.0, size=50,
                         color=TEXT, font=TITLE_FONT).move_to([0, 0.25, 0])
        self.add(w)
        self.play(FadeIn(title), run_time=0.45)
        self.wait(1.1)
        self.play(FadeOut(title), run_time=0.45)


class S04Receptor(SpokenScene):
    def construct(self):
        w = active_receptor_world(labels=True)
        mem, rec, lig, cavity = w.mem, w.rec, w.lig, w.cavity
        rec0 = receptor_bundle(center=(-1.65, MEM_Y, 0), scale=1.25, active=False, labels=True)
        self.add(mem)
        self.at("A G protein")
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in rec0.bars], lag_ratio=0.12), run_time=1.5)
        self.play(Create(rec0.chain), run_time=1.0)
        pulse(rec0.bars, base=4, amp=1.0, speed=1.8)
        wave_bars(rec0.bars)
        self.at("one chain")
        self.play(Indicate(rec0.chain, color=TEXT, scale_factor=1.02), run_time=0.7)
        self.play(FadeOut(rec0.chain), FadeIn(rec0.nums), run_time=0.5)
        outer = T("outer pocket", 28, BLUE).move_to([3.6, 2.2, 0])
        inner = T("inner face", 28, BLUE).move_to([3.6, -0.62, 0])
        self.at("Its outer pocket")
        self.play(FadeIn(outer), FadeIn(inner), run_time=0.7)
        self.play(Indicate(rec0, color=BLUE, scale_factor=1.02), run_time=1.0)
        self.at("An agonist")
        self.play(FadeOut(VGroup(outer, inner)), FadeIn(lig, shift=DOWN * 0.3), run_time=0.8)
        bob(lig, amp=0.035, speed=2)
        self.at("It settles")
        lig.clear_updaters()
        pocket_lig = Circle(radius=0.22, stroke_color=GOLD, stroke_width=3,
                            fill_color=GOLD, fill_opacity=1).move_to([-1.65, 1.58, 0])
        pocket_lab = T("agonist", 28, GOLD).move_to([3.35, 2.2, 0])
        self.play(FadeOut(lig), FadeIn(pocket_lig, shift=DOWN * 0.2), FadeIn(pocket_lab), run_time=1.2)
        self.play(Indicate(rec0.bars[2:5], color=GOLD, scale_factor=1.05), run_time=0.8)
        self.at("One cytoplasmic")
        for b in rec0.bars:
            b.clear_updaters()
        self.play(Transform(rec0, rec), run_time=1.4)
        h6 = T("helix 6", 28, BLUE).move_to([3.45, -1.45, 0])
        h6a = arrow_between(h6.get_left(), rec.bars[5].get_bottom(), BLUE, 3)
        self.play(FadeIn(h6), GrowArrow(h6a), Create(cavity), run_time=0.8)
        pulse(cavity, base=3, amp=1.2, speed=2.4)
        self.finish()


class S05Resting(SpokenScene):
    def construct(self):
        w = active_receptor_world()
        self.add(w)
        pulse(w.cavity, base=3, amp=1.2, speed=2.6)
        bob(w.lig, amp=0.10, speed=2.4)
        gp = gprotein(center=(2.0, -2.25, 0), joined=True)
        self.at("A membrane bound")
        self.play(FadeIn(gp.body), FadeIn(gp.tail), run_time=0.8)
        bob(gp, amp=0.20, speed=3.0)
        self.at("Purple G alpha")
        self.play(FadeIn(gp.ga), FadeIn(gp.nuc), run_time=0.7)
        self.at("Teal beta gamma")
        self.play(FadeIn(gp.bg), FadeIn(gp.bgl), run_time=0.7)
        tether1 = Line([1.45, -1.55, 0], [1.45, -0.35, 0], color=GREY, stroke_width=3)
        tether2 = Line([3.25, -1.7, 0], [3.25, -0.35, 0], color=GREY, stroke_width=3)
        self.play(Create(tether1), Create(tether2), run_time=0.7)
        off = boxed_label("inactive", GREY, 28).move_to([4.9, -3.35, 0])
        self.at("In this resting")
        self.play(FadeIn(off), run_time=0.5)
        self.play(Indicate(gp.nuc, color=TEXT, scale_factor=1.12), run_time=0.8)
        self.at("The G alpha tail")
        gp.clear_updaters()
        self.play(FadeOut(VGroup(tether1, tether2, off)), gp.animate.shift(LEFT * 1.9 + UP * 0.55), run_time=1.6)
        self.play(Indicate(w.cavity, color=TEXT, scale_factor=1.12), run_time=0.8)
        pulse(w.cavity, base=3, amp=1.0, speed=2.2)
        self.finish()


class S06Exchange(SpokenScene):
    def construct(self):
        w = active_receptor_world(with_trimer=True)
        self.add(w)
        pulse(w.cavity, base=3, amp=1.0, speed=2.2)
        bob(w.gp, amp=0.18, speed=3.0)
        bob(w.lig, amp=0.13, speed=2.8)
        self.at("Docking changes")
        self.play(Indicate(w.gp.body, color=TEXT, scale_factor=1.04), run_time=0.9)
        self.at("The gray nucleotide")
        gdp = w.gp.nuc
        w.gp.clear_updaters()
        escape = CubicBezier(gdp.get_center(), gdp.get_center() + DOWN * 1.0,
                             [2.4, -3.2, 0], [3.6, -3.2, 0])
        self.play(MoveAlongPath(gdp, escape), run_time=1.1)
        self.play(FadeOut(gdp, shift=DOWN * 0.2), run_time=0.5)
        empty = DashedVMobject(RoundedRectangle(corner_radius=0.12, width=1.0, height=0.52),
                               num_dashes=18).set_color(TEXT).move_to(w.gp.body.get_center() + DOWN * 0.43)
        self.play(Create(empty), run_time=0.6)
        self.at("Green GTP")
        gtp = nucleotide("GTP", GREEN, at=(3.8, -2.75, 0))
        self.play(FadeIn(gtp), run_time=0.4)
        self.play(gtp.animate.move_to(empty), FadeOut(empty), run_time=1.1)
        bob(gtp, amp=0.10, speed=3.2)
        factor = boxed_label("exchange factor", BLUE, 28).move_to([4.35, 2.15, 0])
        fa = arrow_between(factor.get_left(), w.rec.get_right() + UP * 0.3, BLUE, 3)
        self.at("The receptor has acted")
        self.play(FadeIn(factor), GrowArrow(fa), run_time=0.7)
        source = T("not a GTP source", 28, GREY).move_to([4.2, 0.55, 0])
        self.play(FadeIn(source), run_time=0.6)
        self.at("It remains ready")
        second = VGroup(
            RoundedRectangle(corner_radius=0.3, width=1.25, height=0.85, stroke_color=PURPLE,
                             fill_color=PURPLE, fill_opacity=0.22),
            RoundedRectangle(corner_radius=0.3, width=0.9, height=0.75, stroke_color=TEAL,
                             fill_color=TEAL, fill_opacity=0.22).shift(RIGHT * 1.15),
        ).move_to([5.0, -2.25, 0])
        self.play(FadeOut(source), FadeIn(second, shift=LEFT * 0.4), run_time=0.8)
        bob(second, amp=0.04, speed=1.6)
        self.play(Indicate(w.lig, color=GOLD, scale_factor=1.08), run_time=0.8)
        self.finish()


class S07Outputs(SpokenScene):
    def construct(self):
        alpha = gprotein(center=(-1.5, 0.0, 0), nucleotide_text="GTP", nucleotide_color=GREEN,
                         joined=True, tail=False)
        self.add(alpha)
        self.at("GTP changes")
        self.play(Indicate(alpha.nuc, color=GREEN, scale_factor=1.15), run_time=0.8)
        canonical = T("textbook picture", 30, TEXT).move_to([0, 3.2, 0])
        self.at("The textbook picture")
        bg_unit = VGroup(alpha.bg, alpha.bgl)
        self.play(FadeIn(canonical), bg_unit.animate.shift(RIGHT * 3.4), run_time=1.4)
        alpha_unit = VGroup(alpha.body, alpha.ga, alpha.nuc)
        bob(alpha_unit, amp=0.18, speed=2.8)
        bob(bg_unit, amp=0.18, speed=2.8, seed=2)
        gi = T("Gi may rearrange", 30, GOLD).move_to([0, 3.2, 0])
        self.at("Activated G I")
        self.play(swap(canonical, gi), bg_unit.animate.shift(LEFT * 1.55), run_time=1.2)
        targets = VGroup(boxed_label("target A", TEXT, 28).move_to([-4.6, -2.45, 0]),
                         boxed_label("target B", TEXT, 28).move_to([4.6, -2.45, 0]))
        arrows = VGroup(arrow_between(alpha.body.get_bottom(), targets[0].get_top(), PURPLE, 4),
                        arrow_between(alpha.bg.get_bottom(), targets[1].get_top(), TEAL, 4))
        self.at("Either way")
        self.play(GrowArrow(arrows[0]), GrowArrow(arrows[1]), FadeIn(targets), run_time=1.0)
        self.play(Indicate(targets, color=TEXT, scale_factor=1.04), run_time=0.8)
        self.at("Hydrolysis later")
        gdp = nucleotide("GDP", GREY).move_to(alpha.nuc)
        self.play(swap(alpha.nuc, gdp), FadeOut(VGroup(arrows, targets, gi)), run_time=0.9)
        alpha_unit.clear_updaters(); bg_unit.clear_updaters()
        self.play(bg_unit.animate.shift(LEFT * 1.85), run_time=1.2)
        cycle = CurvedArrow([2.4, 1.0, 0], [1.5, 1.7, 0], angle=PI / 2, color=GREY)
        self.play(Create(cycle), run_time=0.7)
        self.finish()


class S08Paths(SpokenScene):
    def construct(self):
        h = pathway_hourglass(outputs=False)
        tag = scope_tag("schematic")
        self.at("Now the cell")
        self.play(FadeIn(h.receptors), run_time=0.7)
        bob(h.receptors, amp=0.025, speed=1.4)
        self.at("Follow the hourglass")
        waist = T("G-protein families", 30, PURPLE).move_to([-1.5, 3.15, 0])
        self.play(FadeIn(waist), LaggedStart(*[GrowArrow(a) for a in h.in_arrows], lag_ratio=0.12),
                  LaggedStart(*[FadeIn(f) for f in h.fams], lag_ratio=0.12), run_time=1.8)
        self.add(tag)
        outputs = pathway_hourglass(outputs=True)
        self.at("then widen")
        self.play(LaggedStart(*[GrowArrow(a) for a in outputs.out_arrows], lag_ratio=0.12),
                  LaggedStart(*[FadeIn(o) for o in outputs.outs], lag_ratio=0.12), run_time=1.8)
        pulse(outputs.out_arrows, base=3, amp=1.2, speed=1.8)
        flow = flow_markers(outputs.out_arrows, [GREEN, GOLD, RED, TEXT, TEAL], per_path=3)
        self.add(flow)
        self.at("One branch raises")
        self.play(Indicate(outputs.outs[0], color=GREEN, scale_factor=1.08), run_time=0.8)
        self.at("Another lowers")
        self.play(Indicate(outputs.outs[1], color=GOLD, scale_factor=1.08), run_time=0.8)
        self.at("Another raises calcium")
        self.play(Indicate(outputs.outs[2], color=RED, scale_factor=1.08), run_time=0.8)
        self.at("Beta gamma can open")
        self.play(Indicate(outputs.outs[4], color=TEAL, scale_factor=1.08), run_time=0.9)
        flow = Dot(outputs.out_arrows[4].get_start(), radius=0.09, color=TEAL)
        self.add(flow)
        self.play(MoveAlongPath(flow, outputs.out_arrows[4]), run_time=1.1)
        self.finish()


class S09Cells(SpokenScene):
    def construct(self):
        h = pathway_hourglass(outputs=True)
        heading = T("main targets, not exclusive", 30, GOLD).move_to([0, 3.25, 0])
        self.add(h, scope_tag("schematic"))
        pulse(h.in_arrows, base=3, amp=1.0, speed=1.7)
        pulse(h.out_arrows, base=3, amp=1.0, speed=1.9)
        flow = flow_markers(h.out_arrows, [GREEN, GOLD, RED, TEXT, TEAL], per_path=3)
        self.add(flow)
        self.at("Each family")
        self.play(FadeIn(heading), run_time=0.6)
        faint = CurvedArrow(h.fams[1].get_right(), h.outs[4].get_left(), angle=-0.4,
                            color=GREY, stroke_opacity=0.45, stroke_width=3)
        self.play(Create(faint), run_time=1.0)
        self.at("The receptor makes")
        self.play(Indicate(h.receptors, color=BLUE, scale_factor=1.08), run_time=0.9)
        cells = TwoPanel("cell A", "cell B", colors=(BLUE, TEAL), top=0.35, bottom=-3.0, width=8.6)
        cells.left_frame.set_fill(BLUE, 0.18)
        cells.right_frame.set_fill(TEAL, 0.18)
        a = VGroup(boxed_label("cAMP", GREEN, 28), boxed_label("protein A", BLUE, 26)).arrange(DOWN, buff=0.35)
        b = VGroup(boxed_label("cAMP", GREEN, 28), boxed_label("protein B", TEAL, 26)).arrange(DOWN, buff=0.35)
        cells.put(a, "left"); cells.put(b, "right")
        self.at("The cell then supplies")
        self.play(FadeOut(h), FadeOut(flow), FadeOut(faint), FadeOut(heading),
                  FadeIn(cells), FadeIn(a), FadeIn(b), run_time=1.2)
        bob(a[0], amp=0.22, speed=3.0); bob(b[0], amp=0.22, speed=3.2)
        pa = Line(a.get_right() + RIGHT * 0.22 + UP * 0.4, a.get_right() + RIGHT * 0.22 + DOWN * 0.4,
                  stroke_opacity=0)
        pb = Line(b.get_right() + RIGHT * 0.22 + UP * 0.4, b.get_right() + RIGHT * 0.22 + DOWN * 0.4,
                  stroke_opacity=0)
        self.add(flow_markers([pa, pb], [BLUE, TEAL], per_path=3, speed=0.38, radius=0.10))
        outa = Arrow(a.get_bottom(), a.get_bottom() + LEFT * 1.0 + DOWN * 0.55, color=BLUE, buff=0.05)
        outb = Arrow(b.get_bottom(), b.get_bottom() + RIGHT * 1.0 + DOWN * 0.55, color=TEAL, buff=0.05)
        self.at("So one messenger")
        self.play(GrowArrow(outa), GrowArrow(outb), run_time=1.0)
        pulse(outa, base=4, amp=1.5, speed=3.0); pulse(outb, base=4, amp=1.5, speed=3.0)
        pulse(cells.left_frame, base=3, amp=1.2, speed=2.0); pulse(cells.right_frame, base=3, amp=1.2, speed=2.0)
        self.add(flow_markers([outa, outb], [BLUE, TEAL], per_path=2, speed=0.45, radius=0.10))
        self.finish()


class S10Cells(SpokenScene):
    def construct(self):
        panels = TwoPanel("pacemaker cell", "airway muscle", colors=(BLUE, PURPLE), top=2.7, bottom=-2.55)
        panels.left_frame.set_fill(BLUE, 0.16)
        panels.right_frame.set_fill(PURPLE, 0.16)
        ach = boxed_label("acetylcholine", GOLD, 28).move_to([0, 3.25, 0])
        self.add(panels)
        self.at("The same acetylcholine")
        self.play(FadeIn(ach), run_time=0.8)
        bob(ach, amp=0.06, speed=1.6)
        pulse(ach.box, base=2.5, amp=1.0, speed=1.8)
        heart = VGroup(boxed_label("M2", BLUE, 28), boxed_label("Gi", PURPLE, 28),
                       boxed_label("beta-gamma", TEAL, 26), boxed_label("K+ channel", TEAL, 26)).arrange(DOWN, buff=0.24)
        airway = VGroup(boxed_label("M3", BLUE, 28), boxed_label("Gq", PURPLE, 28),
                        boxed_label("PLC-beta", TEAL, 26), boxed_label("calcium", RED, 26)).arrange(DOWN, buff=0.24)
        panels.put(heart, "left"); panels.put(airway, "right")
        self.at("In a pacemaker")
        self.play(LaggedStart(*[FadeIn(x) for x in heart], lag_ratio=0.18), run_time=1.6)
        pulse(VGroup(*[x.box for x in heart]), base=2.5, amp=1.0, speed=1.7)
        hp = Line(heart.get_right() + RIGHT * 0.22 + UP * 1.25,
                  heart.get_right() + RIGHT * 0.22 + DOWN * 1.25, stroke_opacity=0)
        self.add(flow_markers([hp], [TEAL], per_path=4, speed=0.34, radius=0.11))
        self.at("freed beta gamma")
        self.play(Indicate(heart[2], color=TEAL, scale_factor=1.08), Indicate(heart[3], color=TEAL, scale_factor=1.08), run_time=0.9)
        beats = VGroup(*[Line([x, -2.95, 0], [x, -2.6, 0], color=TEXT, stroke_width=6)
                         for x in (-5.2, -3.8, -2.2, -0.9)])
        self.at("Firing slows")
        self.play(LaggedStart(*[Create(b) for b in beats], lag_ratio=0.35), run_time=1.2)
        self.at("In airway muscle")
        self.play(LaggedStart(*[FadeIn(x) for x in airway], lag_ratio=0.18), run_time=1.6)
        pulse(VGroup(*[x.box for x in airway]), base=2.5, amp=1.0, speed=1.9)
        ap = Line(airway.get_left() + LEFT * 0.22 + UP * 1.25,
                  airway.get_left() + LEFT * 0.22 + DOWN * 1.25, stroke_opacity=0)
        self.add(flow_markers([ap], [RED], per_path=4, speed=0.34, radius=0.11))
        self.at("phospholipase C beta")
        self.play(Indicate(airway[2], color=TEAL, scale_factor=1.08), Indicate(airway[3], color=RED, scale_factor=1.08), run_time=0.9)
        band = RoundedRectangle(corner_radius=0.16, width=3.4, height=0.42, stroke_color=TEXT,
                                fill_color=GREY, fill_opacity=0.5).move_to([3.25, -2.78, 0])
        self.at("The muscle contracts")
        self.play(FadeIn(band), run_time=0.4)
        self.play(band.animate.stretch_to_fit_width(1.9).stretch_to_fit_height(0.65), run_time=1.0)
        self.at("The input matches")
        self.play(Indicate(ach, color=GOLD), run_time=0.8)
        self.add(scope_tag("schematic"))
        self.finish()


class S11Rule(SpokenScene):
    def construct(self):
        ligand = boxed_label("ligand", GOLD, 30).move_to([-5.7, 0.25, 0])
        rec = boxed_label("GPCR subtype", BLUE, 30).move_to([-2.75, 0.25, 0])
        gp = boxed_label("G protein", PURPLE, 30).move_to([0.35, 0.25, 0])
        targets = boxed_label("downstream proteins", TEAL, 30).move_to([4.25, 0.25, 0])
        a1 = arrow_between(ligand.get_right(), rec.get_left(), GOLD, 4)
        a2 = arrow_between(rec.get_right(), gp.get_left(), GREY, 4)
        a3 = arrow_between(gp.get_right(), targets.get_left(), GREY, 4)
        self.at("So do not predict")
        self.play(FadeIn(ligand), run_time=0.6)
        bob(ligand, amp=0.18, speed=3.0)
        wrong = T("ligand alone?", 32, GREY).move_to([0, 2.65, 0])
        cross = T("×", 58, RED, weight=BOLD).next_to(wrong, LEFT, buff=0.35)
        self.play(FadeIn(wrong), FadeIn(cross), run_time=0.8)
        self.at("Trace the receptor")
        self.play(FadeOut(VGroup(wrong, cross)), GrowArrow(a1), FadeIn(rec), run_time=0.7)
        self.play(GrowArrow(a2), FadeIn(gp), run_time=0.7)
        self.play(GrowArrow(a3), FadeIn(targets), run_time=0.7)
        pulse(VGroup(a1, a2, a3), base=4, amp=1.0, speed=1.8)
        pathflow = flow_markers([a1, a2, a3], [GOLD, BLUE, PURPLE], per_path=3, speed=0.32)
        self.add(pathflow)
        self.at("That path predicts")
        response = boxed_label("first response", TEXT, 30).move_to([4.25, -2.0, 0])
        ar = arrow_between(targets.get_bottom(), response.get_top(), TEXT, 4)
        self.play(GrowArrow(ar), FadeIn(response), run_time=0.9)
        tag = scope_tag("first response")
        self.add(tag)
        self.at("Dose and efficacy")
        strength = ValueTracker(0.25)
        gauge = dial(strength, center=[-1.8, -2.0, 0], radius=1.0, label="activation", color=GOLD, size=30)
        self.play(FadeIn(gauge), run_time=0.6)
        self.play(strength.animate.set_value(0.9), run_time=1.4)
        self.at("The wiring decides")
        self.play(Indicate(VGroup(rec, gp, targets), color=TEXT, scale_factor=1.03), run_time=1.0)
        self.play(FadeOut(VGroup(ligand, rec, gp, targets, a1, a2, a3, pathflow,
                                 response, ar, gauge, tag)), run_time=0.8)
        self.finish()


class S12End(EndCard):
    LINE = "GPCR subtype, G protein, and downstream proteins decide the first response."
