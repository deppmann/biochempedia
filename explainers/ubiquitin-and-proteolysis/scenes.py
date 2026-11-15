"""How a Signal Marks One Protein.

COLOR MAP (kept constant throughout)
  YELLOW = ubiquitin, the reusable tag
  GREY   = possible protein targets / HIF-1alpha
  BLUE   = E1
  TEAL   = E2
  GREEN  = E3, VHL, and recognition grips
  GOLD   = oxygen and the hydroxyl badge
  RED    = proteasome / destruction
  TEXT   = ARNT and neutral explanatory text

Proteins and enzymes are schematic labelled blocks.  No molecular structures are drawn.
"""
from bp_parts import *  # noqa: F401,F403


# ---------------------------------------------------------------------------
# Shared picture builders.  Continued scenes call these so landmarks do not drift.

def protein(text="HIF-1α", center=(0, 0, 0), feature="plain", width=3.25, height=1.45):
    """A grey target block with a proline notch and optional OH badge."""
    c = np.array(center, dtype=float)
    body = RoundedRectangle(corner_radius=0.18, width=width, height=height,
                            stroke_color=GREY, stroke_width=4,
                            fill_color=GREY, fill_opacity=0.38).move_to(c)
    lab = T(text, 34, TEXT, weight=BOLD).move_to(c + LEFT * 0.25)
    # Keep the site just outside the body: its label and badge must never sit on
    # the protein outline (the layout checker treats that as obscured text).
    notch = Circle(radius=0.23, stroke_color=GOLD if feature == "oh" else GREY,
                   stroke_width=4, fill_color=BG, fill_opacity=1).move_to(body.get_right() + RIGHT * 0.38)
    site = T("Pro", 24, GOLD if feature == "oh" else GREY).next_to(notch, DOWN, buff=0.26)
    parts = [body, lab, notch, site]
    if feature == "oh":
        badge = Circle(radius=0.29, stroke_width=0, fill_color=GOLD, fill_opacity=1).move_to(notch)
        badge_lab = T("OH", 22, BG, weight=BOLD).move_to(badge)
        parts += [badge, badge_lab]
    g = VGroup(*parts)
    g.body, g.notch, g.site = body, notch, site
    g.badge = VGroup(*parts[-2:]) if feature == "oh" else VGroup()
    return g


def ubiquitin(center=(0, 0, 0), small=False):
    return boxed_label("Ub", YELLOW, size=24 if small else 30,
                       box=(0.78, 0.68) if small else (1.02, 0.84),
                       fill_opacity=0.42).move_to(center)


def enzyme(text, color, center, width=1.65, height=1.2, size=34):
    return boxed_label(text, color, size=size, box=(width, height),
                       fill_opacity=0.42).move_to(center)


def grip(center=(2.5, 0, 0), label="E3", open_side="left", size=34):
    """A green C-shaped recognition grip beside its labelled receptor body."""
    c = np.array(center, dtype=float)
    angle = PI if open_side == "left" else 0
    jaws = AnnularSector(inner_radius=0.55, outer_radius=0.77, angle=1.45 * PI,
                         start_angle=angle + PI - 0.725 * PI,
                         color=GREEN, fill_opacity=1, stroke_width=0).move_to(c)
    body = enzyme(label, GREEN, c + (RIGHT if open_side == "left" else LEFT) * 1.48,
                  width=1.9, height=1.18, size=size)
    g = VGroup(jaws, body)
    g.jaws, g.body = jaws, body
    return g


def relay_world(with_target=True, attached=False):
    """The shared E1 -> E2 -> E3 relay used in scenes 2 and 3."""
    e1 = enzyme("E1", BLUE, (-4.9, 1.25, 0))
    e2 = enzyme("E2", TEAL, (-2.0, 1.25, 0))
    e3 = grip((1.35, 1.25, 0), "E3", "right")
    a1 = Arrow(e1.get_right(), e2.get_left(), buff=0.18, color=GREY,
               stroke_width=5, tip_length=0.18)
    a2 = Arrow(e2.get_right(), e3.body.get_left(), buff=0.22, color=GREY,
               stroke_width=5, tip_length=0.18)
    g = VGroup(e1, e2, e3, a1, a2)
    g.e1, g.e2, g.e3, g.arrows = e1, e2, e3, VGroup(a1, a2)
    if with_target:
        tgt = protein("target", (3.95, -0.55, 0), "plain", width=3.1)
        g.add(tgt)
        g.target = tgt
        if attached:
            u = ubiquitin((3.3, 0.35, 0), small=True)
            g.add(u)
            g.ub = u
    return g


def choice_world(question=True):
    """Exact final frame shared by the prediction and pause scenes."""
    left = protein("HIF-1α", (-3.15, 0.25, 0), "oh", width=3.45)
    right = protein("HIF-1α", (3.15, 0.25, 0), "plain", width=3.45)
    vhl = grip((0, 1.95, 0), "VHL", "left", size=30)
    labels = VGroup(T("hydroxyl badge", 28, GOLD).move_to([-3.15, -1.15, 0]),
                    T("plain proline", 28, GREY).move_to([3.15, -1.15, 0]))
    g = VGroup(left, right, vhl, labels)
    g.left_target, g.right_target, g.vhl = left, right, vhl
    if question:
        q = question_card("Which target will VHL grip?", y=-3.05, size=34)
        g.add(q)
        g.question = q
    return g


def conveyor_base(low_oxygen=False):
    """The shared HIF production line for oxygen-high and oxygen-low scenes."""
    rail = RoundedRectangle(corner_radius=0.16, width=11.9, height=0.46,
                            stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.30).move_to([-0.05, -1.25, 0])
    rollers = VGroup(*[Circle(radius=0.12, color=GREY, stroke_width=3).move_to([x, -1.25, 0])
                       for x in np.linspace(-5.6, 5.5, 10)])
    phd = enzyme("PHD", BLUE, (0, 1.45, 0), width=2.35, height=1.2, size=38)
    tag = T("schematic", 24, GREY).move_to([-5.45, -3.35, 0])
    g = VGroup(rail, rollers, phd, tag)
    g.rail, g.phd = rail, phd
    return g


def tiny_target(center, feature="plain"):
    body = RoundedRectangle(corner_radius=0.12, width=1.8, height=0.90,
                            stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.42).move_to(center)
    lab = T("HIF-1α", 24, TEXT).move_to(body)
    g = VGroup(body, lab)
    if feature == "oh":
        b = Circle(radius=0.22, fill_color=GOLD, fill_opacity=1, stroke_width=0).move_to(body.get_top() + UP * 0.24)
        g.add(b, T("OH", 22, BG, weight=BOLD).move_to(b))
    return g


def proteasome(center=(4.15, 0, 0), width=3.1, height=2.0):
    c = np.array(center, dtype=float)
    outer = RoundedRectangle(corner_radius=0.7, width=width, height=height,
                             stroke_color=RED, stroke_width=6,
                             fill_color=RED, fill_opacity=0.30).move_to(c)
    rings = VGroup(*[Line(c + [dx, -0.78, 0], c + [dx, 0.78, 0], color=RED, stroke_width=4)
                     for dx in (-0.65, 0, 0.65)])
    lab = T("proteasome", 30, RED, weight=BOLD).next_to(outer, DOWN, buff=0.22)
    return VGroup(outer, rings, lab)


# ---------------------------------------------------------------------------

class S00Hook(SpokenScene):
    def construct(self):
        targets = VGroup(*[tiny_target((x, y, 0)) for x, y in
                           [(-5.0, 1.7), (-2.6, 2.2), (2.8, 2.1), (5.0, 1.35),
                            (-4.6, -1.7), (-2.2, -2.05), (2.7, -2.0), (5.0, -1.5)]])
        hif = protein("HIF-1α", (0, 0, 0), "plain", width=3.7, height=1.35)
        self.play(LaggedStart(*[FadeIn(t, scale=0.8) for t in targets], lag_ratio=0.08),
                  FadeIn(hif, scale=0.85), run_time=1.4)
        for i, target in enumerate(targets):
            bob(target, amp=0.18, speed=2.8, seed=i % 3)

        self.at("How can oxygen")
        q = fit_text("How can oxygen select one protein?", max_w=9.8, size=42,
                     color=GOLD).move_to([0, 3.30, 0])
        self.play(Write(q), run_time=0.8)

        self.at("Watch the target")
        self.play(Indicate(hif.body, color=TEXT, scale_factor=1.06), run_time=0.8)

        ubs = VGroup(*[ubiquitin(p, small=True) for p in
                       [(-4.7, 0.1, 0), (-3.2, -0.25, 0), (3.0, 0.1, 0), (4.5, -0.25, 0)]])
        self.at("Yellow ubiquitin")
        self.play(LaggedStart(*[FadeIn(u, shift=UP * 0.15) for u in ubs], lag_ratio=0.14), run_time=0.8)
        bob(ubs, amp=0.10, speed=1.7, seed=2)

        self.at("Gray proteins")
        self.play(LaggedStart(*[Indicate(t, color=GREY, scale_factor=1.03) for t in targets], lag_ratio=0.04),
                  run_time=0.9)

        self.at("Green E3")
        e3 = grip((4.25, 0.15, 0), "E3", "left")
        self.play(FadeOut(ubs[2]), FadeOut(ubs[3]), FadeIn(e3, shift=LEFT * 0.25), run_time=0.8)
        self.play(Rotate(e3.jaws, angle=0.24, about_point=e3.jaws.get_center(), rate_func=there_and_back),
                  run_time=1.2)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Ubiquitin and Proteolysis"
    TITLE = "How a Signal Marks One Protein"


class S02Relay(SpokenScene):
    def construct(self):
        w = relay_world()
        self.play(FadeIn(w.target, shift=LEFT * 0.2), FadeIn(w.e1), run_time=0.8)
        bob(w.e1, amp=0.17, speed=2.8)
        atp = boxed_label("ATP", GOLD, 28, fill_opacity=0.24).move_to([-5.0, 2.7, 0])
        ub = ubiquitin((-5.0, -0.25, 0))
        self.at("spends a TP")
        self.play(FadeIn(atp), FadeIn(ub), run_time=0.5)
        self.play(ub.animate.move_to(w.e1.get_center() + DOWN * 1.42),
                  FadeOut(atp, shift=UP * 0.2), run_time=1.0)

        self.at("E2 receives")
        self.play(FadeIn(w.e2), GrowArrow(w.arrows[0]),
                  ub.animate.move_to(w.e2.get_center() + DOWN * 1.25), run_time=1.1)
        bob(w.e2, amp=0.17, speed=2.8, seed=2)

        self.at("E3 brings")
        self.play(FadeIn(w.e3), GrowArrow(w.arrows[1]),
                  ub.animate.move_to(w.e3.jaws.get_center() + UP * 1.0), run_time=1.1)
        self.play(w.target.animate.move_to([2.85, -0.45, 0]), run_time=1.0)

        self.at("target lysine")
        lys = T("lysine", 30, GOLD).next_to(w.target, DOWN, buff=0.2)
        self.play(FadeIn(lys), ub.animate.scale(0.75).move_to(w.target.get_top() + UP * 0.72 + LEFT * 0.45), run_time=0.9)

        self.at("tag is common")
        stream = VGroup(*[ubiquitin((-4.8 + i * 1.0, 2.75, 0), small=True) for i in range(5)])
        self.play(LaggedStart(*[FadeIn(x) for x in stream], lag_ratio=0.12), run_time=0.8)

        self.at("Recognition makes")
        self.play(Indicate(w.e3.jaws, color=GREEN, scale_factor=1.15),
                  Indicate(w.target.notch, color=GOLD, scale_factor=1.25), run_time=1.1)
        self.finish()


class S03Selection(SpokenScene):
    def construct(self):
        w = relay_world(with_target=False)
        self.add(w.e1, w.e2, w.arrows[0])
        bob(w.e1, amp=0.17, speed=2.8)
        bob(w.e2, amp=0.17, speed=2.8, seed=2)
        ub = ubiquitin((-4.8, 0.05, 0), small=True)
        self.add(ub)
        self.play(ub.animate.move_to([-1.95, 0.05, 0]), run_time=1.0)

        self.at("selector can change")
        g1 = grip((1.55, 1.35, 0), "E3-A", "right", size=28)
        g2 = grip((1.55, -1.25, 0), "E3-B", "right", size=28)
        self.play(FadeIn(g1), FadeIn(g2), run_time=0.8)

        a = protein("A", (4.65, 1.35, 0), "oh", width=2.5, height=1.0)
        b = protein("B", (4.65, -1.25, 0), "plain", width=2.5, height=1.0)
        self.at("Different E3 receptors")
        self.play(FadeIn(a, shift=LEFT * 0.25), FadeIn(b, shift=LEFT * 0.25), run_time=0.9)

        self.at("target features")
        feature = T("target features", 28, GOLD).move_to([4.45, -2.75, 0])
        self.play(FadeIn(feature), Indicate(a.notch, color=GOLD),
                  Indicate(b.notch, color=GREY), run_time=0.8)

        self.at("keep ubiquitin moving")
        self.play(ub.animate.move_to(g1.jaws.get_center() + UP * 1.0), run_time=1.0)

        self.at("which gray block")
        self.play(a.animate.shift(LEFT * 1.65), Indicate(g1.jaws, color=GREEN), run_time=1.0)
        self.play(Indicate(b, color=GREY, scale_factor=1.03), run_time=0.7)
        self.finish()


class S04Rule(SpokenScene):
    def construct(self):
        tgt = protein("target", (-1.5, 0, 0), "plain", width=4.0, height=1.5)
        g = grip((2.0, 0, 0), "E3", "left")
        self.play(FadeIn(tgt, scale=0.9), FadeIn(g), run_time=0.9)
        bob(g, amp=0.16, speed=2.7)
        self.at("target feature")
        degron = T("degron", 42, GOLD, weight=BOLD).move_to([-1.5, -1.55, 0])
        pointer = Line(degron.get_top(), tgt.notch.get_bottom(), color=GOLD, stroke_width=4)
        self.play(FadeIn(degron), Create(pointer), Indicate(tgt.notch, color=GOLD), run_time=0.9)

        self.at("short sequence")
        seq = VGroup(*[Square(0.28, stroke_color=GREY, stroke_width=3) for _ in range(4)]).arrange(RIGHT, buff=0.08)
        seq.move_to([-4.5, 2.15, 0])
        self.play(FadeIn(seq), run_time=0.6)
        self.at("chemical change")
        badge = VGroup(Circle(radius=0.31, fill_color=GOLD, fill_opacity=1, stroke_width=0),
                       T("OH", 22, BG, weight=BOLD)).move_to([0.1, 2.15, 0])
        self.play(FadeIn(badge, scale=0.5), run_time=0.6)

        self.at("Signals can create")
        self.play(badge.animate.move_to(tgt.notch), FadeOut(seq), run_time=1.0)
        self.at("strengthen its contact")
        self.play(FadeOut(tgt.site), tgt.animate.shift(RIGHT * 0.85),
                  Indicate(g.jaws, color=GREEN), run_time=1.0)

        self.at("Signals change protein fate")
        rule = caption("Signals change protein fate by changing what an E3 can recognize.",
                       size=32, color=TEXT, y=-3.05)
        self.play(FadeOut(degron), FadeOut(pointer), FadeIn(rule), run_time=0.8)
        self.play(Indicate(badge, color=GOLD), Indicate(g.jaws, color=GREEN), run_time=1.0)

        self.at("follow oxygen")
        g.clear_updaters()
        hif = T("HIF-1α", 34, TEXT, weight=BOLD).move_to(tgt[1])
        vhl = T("VHL", 34, GREEN, weight=BOLD).move_to(g.body[1])
        self.play(swap(tgt[1], hif), swap(g.body[1], vhl), run_time=0.9)
        self.finish()


class S05Write(SpokenScene):
    def construct(self):
        base = conveyor_base()
        self.play(Create(base.rail), FadeIn(base.phd), FadeIn(base[-1]), run_time=0.9)
        bob(base.phd, amp=0.18, speed=2.8)
        targets = [tiny_target((-5.0 + i * 2.2, -0.42, 0)) for i in range(5)]
        self.at("made continuously")
        self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 0.2) for t in targets], lag_ratio=0.14), run_time=1.2)

        self.at("oxygen is available")
        oxy = VGroup(*[VGroup(Circle(radius=0.36, fill_color=GOLD, fill_opacity=0.28,
                                    stroke_color=GOLD, stroke_width=3), T("O₂", 22, GOLD)).move_to(p)
                       for p in [(-4.5, 2.65, 0), (-2.6, 2.8, 0), (0, 2.9, 0), (2.7, 2.7, 0)]])
        self.play(LaggedStart(*[FadeIn(o, shift=DOWN * 0.2) for o in oxy], lag_ratio=0.12), run_time=0.8)

        self.at("uses it")
        self.play(FadeOut(oxy[2], shift=DOWN * 0.35), Indicate(base.phd, color=BLUE), run_time=0.9)

        self.at("adds a hydroxyl")
        badge = VGroup(Circle(radius=0.25, fill_color=GOLD, fill_opacity=1, stroke_width=0),
                       T("OH", 22, BG, weight=BOLD)).move_to(base.phd.get_bottom())
        self.play(FadeIn(badge, scale=0.4), badge.animate.move_to(targets[2].get_top() + UP * 0.28), run_time=1.0)

        self.at("proline on")
        pro = T("proline", 28, GOLD).move_to([0, -2.15, 0])
        line = Line(pro.get_top() + UP * 0.05, targets[2].get_bottom() + DOWN * 0.05, color=GOLD, stroke_width=3)
        self.play(FadeIn(pro), Create(line), run_time=0.7)

        self.at("small batch")
        degron = boxed_label("complete degron", GOLD, 30, fill_opacity=0.2).move_to([3.9, 1.65, 0])
        self.play(FadeIn(degron), Indicate(badge, color=GOLD, scale_factor=1.3), run_time=0.8)
        self.play(VGroup(*targets).animate.shift(RIGHT * 1.0), run_time=1.0)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        w = choice_world(question=False)
        self.play(FadeIn(w.left_target, shift=RIGHT * 0.2),
                  FadeIn(w.right_target, shift=LEFT * 0.2), run_time=0.9)
        bob(w.left_target, amp=0.16, speed=2.7)
        bob(w.right_target, amp=0.16, speed=2.7, seed=2)
        self.at("hydroxyl badge")
        self.play(Indicate(w.left_target.badge, color=GOLD, scale_factor=1.2), run_time=0.7)
        self.at("one does not")
        self.play(Indicate(w.right_target.notch, color=GREY, scale_factor=1.2), run_time=0.7)
        self.play(FadeIn(w[3]), run_time=0.5)
        self.at("Which target")
        self.play(FadeIn(w.vhl, shift=DOWN * 0.2), run_time=0.6)
        q = question_card("Which target will VHL grip?", y=-3.05, size=34)
        self.play(FadeIn(q), run_time=0.6)
        self.finish()


class S07Pause(PredictPause):
    QUESTION = "Which target will VHL grip?"
    SECONDS = 4.5
    CARD = {"y": -3.05, "size": 34}
    RING_AT = (5.95, -3.0, 0)

    def backdrop(self):
        return choice_world(question=False)


class S08Reveal(SpokenScene):
    def construct(self):
        w = choice_world(question=False)
        self.add(w.left_target, w.right_target, w[3])
        vhl = w.vhl
        self.play(FadeIn(vhl), run_time=0.5)
        self.at("closes around")
        shift = w.left_target.notch.get_center() - vhl.jaws.get_center()
        self.play(FadeOut(w.left_target.site), vhl.animate.shift(shift), run_time=1.0)
        bob(w.left_target, amp=0.16, speed=2.7, seed=1)
        bob(vhl, amp=0.16, speed=2.7, seed=1)
        self.play(Indicate(w.left_target.badge, color=GOLD), run_time=0.7)

        self.at("peptide with hydroxyproline")
        assay = Ledger([("hydroxyproline", "binds", GOLD),
                        ("ordinary proline", "no binding", GREY)],
                       top_left=(-5.7, -1.55), title="binding assay · schematic",
                       width=11.0, key_w=4.6, row_h=0.62, size=28)
        self.play(FadeOut(w[3]), FadeIn(assay), run_time=0.8)
        self.play(assay.reveal(0), run_time=0.7)

        self.at("ordinary proline")
        self.play(assay.reveal(1), w.right_target.animate.shift(RIGHT * 0.45), run_time=0.8)

        self.at("modification itself")
        self.play(Indicate(w.left_target.badge, color=GOLD, scale_factor=1.35),
                  Indicate(vhl.jaws, color=GREEN, scale_factor=1.12), run_time=1.1)
        self.finish()


class S09Destroy(SpokenScene):
    def construct(self):
        tgt = protein("HIF-1α", (-3.6, 0.7, 0), "oh", width=3.4)
        tgt.remove(tgt.site)
        vhl = grip((-0.55, 0.7, 0), "VHL", "left", size=30)
        self.add(tgt, vhl)
        bob(tgt, amp=0.16, speed=2.7, seed=1)
        bob(vhl, amp=0.16, speed=2.7, seed=1)
        self.at("ubiquitin chain")
        tgt.clear_updaters()
        vhl.clear_updaters()
        chain = VGroup(*[ubiquitin((-4.65 + 0.90 * i, 1.92 + 0.45 * i, 0), small=True) for i in range(4)])
        self.play(LaggedStart(*[FadeIn(u, scale=0.5) for u in chain], lag_ratio=0.18), run_time=1.3)

        self.at("red proteasome")
        pr = proteasome((4.25, 0.55, 0))
        pr[2].next_to(pr[0], UP, buff=0.22)
        self.play(FadeIn(pr, shift=LEFT * 0.25), run_time=0.8)

        self.at("breaks it down")
        marked = VGroup(tgt, chain)
        cargo = RoundedRectangle(corner_radius=0.16, width=2.5, height=0.72,
                                 stroke_color=GREY, stroke_width=4,
                                 fill_color=GREY, fill_opacity=0.35).move_to(tgt)
        self.play(FadeOut(marked), FadeOut(vhl), run_time=0.4)
        self.add(cargo)
        self.play(cargo.animate.move_to(pr[0]).set_opacity(0), run_time=0.7)
        pieces = VGroup(*[Square(0.2, stroke_width=0, fill_color=GREY, fill_opacity=1).move_to([5.8 + 0.2*i, 0.6-0.25*i, 0]) for i in range(4)])
        self.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.2) for p in pieces], lag_ratio=0.1), run_time=0.8)

        self.at("keeps entering")
        new = VGroup(*[tiny_target((-5.2 + 2.0*i, -1.65, 0)) for i in range(4)])
        rail = Line([-6.1, -2.25, 0], [2.1, -2.25, 0], color=GREY, stroke_width=6)
        self.play(Create(rail), LaggedStart(*[FadeIn(x, shift=RIGHT * 0.2) for x in new], lag_ratio=0.12), run_time=1.0)

        self.at("level low")
        level = ValueTracker(0.28)
        d = dial(level, center=[4.8, -1.75, 0], radius=0.9, label="HIF-1α level", color=GREY, size=30)
        self.play(FadeIn(d), run_time=0.7)
        self.play(level.animate.set_value(0.2), VGroup(*new).animate.shift(RIGHT * 1.0), run_time=1.2)
        self.add(scope_tag("schematic"))
        self.finish()


class S10LowOxygen(SpokenScene):
    def construct(self):
        base = conveyor_base(low_oxygen=True)
        self.add(base)
        bob(base.phd, amp=0.18, speed=2.8)
        oxygen = VGroup(*[VGroup(Circle(radius=0.36, fill_color=GOLD, fill_opacity=0.28,
                                       stroke_color=GOLD, stroke_width=3), T("O₂", 22, GOLD)).move_to(p)
                          for p in [(-4.6, 2.7, 0), (-2.4, 2.5, 0), (0, 2.8, 0), (2.4, 2.5, 0), (4.5, 2.7, 0)]])
        self.add(oxygen)
        self.at("oxygen falls")
        self.play(FadeOut(oxygen[1]), FadeOut(oxygen[3]), FadeOut(oxygen[4]),
                  oxygen[0].animate.shift(LEFT * 0.35), run_time=1.1)

        targets = VGroup(*[tiny_target((-5.1 + i * 1.9, -0.42, 0), "oh" if i == 2 else "plain") for i in range(6)])
        self.at("reaction less often")
        self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 0.2) for t in targets], lag_ratio=0.1), run_time=1.2)

        self.at("Fewer HIF")
        self.play(Indicate(targets[2], color=GOLD),
                  LaggedStart(*[Indicate(targets[i], color=GREY, scale_factor=1.02) for i in [0,1,3,4,5]], lag_ratio=0.05),
                  run_time=1.0)

        self.at("VHL finds fewer")
        vhl = grip((4.3, 1.1, 0), "VHL", "left", size=28)
        self.play(FadeIn(vhl), run_time=0.7)
        self.play(Rotate(vhl.jaws, 0.20, about_point=vhl.jaws.get_center(), rate_func=there_and_back), run_time=0.9)

        self.at("accumulates")
        pile = VGroup(*[tiny_target((-3.7 + 2.0*(i%4), -2.0 - 1.08*(i//4), 0)) for i in range(8)])
        self.play(FadeOut(targets), LaggedStart(*[FadeIn(t, shift=UP * 0.2) for t in pile], lag_ratio=0.08), run_time=1.2)

        self.at("pairs with a RNT")
        arnt = boxed_label("ARNT", TEXT, 30, fill_opacity=0.14).move_to([4.25, -0.15, 0])
        self.play(FadeOut(VGroup(*pile[:-1])), FadeIn(arnt),
                  pile[-1].animate.move_to([2.45, -0.15, 0]), run_time=0.9)

        self.at("switch on low")
        gene = RoundedRectangle(corner_radius=0.18, width=3.5, height=1.15,
                                stroke_color=GREEN, stroke_width=4,
                                fill_color=GREEN, fill_opacity=0.13).move_to([3.4, -2.1, 0])
        gene_lab = T("low-oxygen genes", 28, GREEN).move_to(gene)
        self.play(FadeIn(gene), FadeIn(gene_lab), Indicate(arnt, color=TEXT), run_time=0.9)
        self.finish()


class S12Return(SpokenScene):
    def construct(self):
        ub_stream = VGroup(*[ubiquitin((-5.4 + i * 0.85, 2.55, 0), small=True) for i in range(5)])
        pr = proteasome((4.65, 2.35, 0), width=2.6, height=1.35)
        self.play(FadeIn(ub_stream), FadeIn(pr), run_time=0.8)
        bob(ub_stream, amp=0.18, speed=2.8)
        self.at("what changed")
        hif = protein("HIF-1α", (-2.8, 0.15, 0), "oh", width=3.5)
        vhl = grip((0.15, 0.15, 0), "VHL", "left", size=30)
        self.play(FadeIn(hif), FadeIn(vhl), run_time=0.8)

        self.at("Oxygen changed")
        self.play(Indicate(hif.badge, color=GOLD, scale_factor=1.35),
                  Indicate(vhl.jaws, color=GREEN), run_time=1.0)

        self.at("did not invent")
        self.play(Indicate(ub_stream, color=YELLOW, scale_factor=1.04),
                  Indicate(pr[0], color=RED, scale_factor=1.04), run_time=1.0)

        self.at("Signals change protein fate")
        self.play(FadeOut(hif), FadeOut(vhl), FadeOut(ub_stream), FadeOut(pr), run_time=0.6)
        steps = VGroup(boxed_label("signal changes feature", GOLD, 30, fill_opacity=0.18),
                       boxed_label("E3 recognizes target", GREEN, 30, fill_opacity=0.18),
                       boxed_label("protein fate changes", RED, 30, fill_opacity=0.18)).arrange(DOWN, buff=0.55)
        steps.move_to([0, 0.55, 0])
        arrows = VGroup(Arrow(steps[0].get_bottom(), steps[1].get_top(), buff=0.12,
                              color=GREY, stroke_width=5, tip_length=0.18),
                        Arrow(steps[1].get_bottom(), steps[2].get_top(), buff=0.12,
                              color=GREY, stroke_width=5, tip_length=0.18))
        self.play(FadeIn(steps[0]), run_time=0.5)
        self.play(GrowArrow(arrows[0]), FadeIn(steps[1]), run_time=0.7)
        self.play(GrowArrow(arrows[1]), FadeIn(steps[2]), run_time=0.7)
        rule = caption("Signals change protein fate by changing what an E3 can recognize.",
                       size=32, y=-3.05)
        self.play(FadeIn(rule), run_time=0.7)
        self.finish()


class S13End(EndCard):
    LINE = "Signals change protein fate by changing what an E3 can recognize."
