"""How codons become a chain (Biochemistrypedia explainer, chapter 2).

COLOR MAP (shared with chapter 1, with the chapter-2 action colours required by the script)
  BLUE   = mRNA and codons
  GOLD   = start and fixed reading register
  TEAL   = reading window, ribosome, and synthetase action
  GREEN  = amino acids and the growing peptide
  RED    = stop and release
  YELLOW = tRNA adaptors
  GREY   = unresolved states and quiet structure
"""
from bp_parts import *  # noqa: F401,F403


CODON_W = 1.48
RIBO_Y = -1.45
SLOT_X = {"E": -2.65, "P": 0.0, "A": 2.65}


def codon_ribbon(y=-1.35, center=0.0, n=7, start=True, stop=False):
    """The carried blue message, rebuilt at one fixed scale throughout the film."""
    boxes = VGroup()
    for i in range(n):
        x = center + (i - (n - 1) / 2) * CODON_W
        col = GOLD if start and i == 0 else (RED if stop and i == n - 1 else BLUE)
        box = RoundedRectangle(corner_radius=0.1, width=CODON_W - 0.08, height=0.74,
                               stroke_color=col, stroke_width=3, fill_color=col,
                               fill_opacity=0.13).move_to([x, y, 0])
        bases = M("AUG" if i == 0 else ("UAG" if stop and i == n - 1 else "GCU"),
                  28, col).move_to(box)
        boxes.add(VGroup(box, bases))
    return boxes


def reading_window(x=-2.96, y=-1.35):
    return RoundedRectangle(corner_radius=0.17, width=CODON_W + 0.02, height=1.06,
                            stroke_color=TEAL, stroke_width=7).move_to([x, y, 0])


def cargo_block(text="amino acid", color=GREEN, width=1.55, size=28):
    if not text:
        return RoundedRectangle(corner_radius=0.14, width=width, height=0.68,
                                stroke_color=color, stroke_width=2.5,
                                fill_color=color, fill_opacity=0.22)
    return boxed_label(text, color, size=size, box=(width, 0.68), fill_opacity=0.22)


def trna_cartoon(center=ORIGIN, scale=1.0, cargo=True, cargo_text="amino acid",
                  wrong=False, labels=False):
    """One schematic L-shaped adaptor; every continuation calls this builder."""
    c = np.array(center, dtype=float)
    stem = VMobject(stroke_color=YELLOW, stroke_width=14, fill_opacity=0)
    stem.set_points_as_corners([c + [-0.75, -1.65, 0], c + [-0.15, -1.65, 0],
                                c + [-0.15, 0.85, 0], c + [0.9, 0.85, 0]])
    anticodon = VGroup(*[RoundedRectangle(corner_radius=0.07, width=0.42, height=0.42,
                                         stroke_color=YELLOW, stroke_width=3,
                                         fill_color=YELLOW, fill_opacity=0.22)
                        for _ in range(3)]).arrange(RIGHT, buff=0.08)
    anticodon.move_to(c + [-0.75, -1.65, 0])
    top = Dot(c + [0.9, 0.85, 0], radius=0.13, color=YELLOW)
    g = VGroup(stem, anticodon, top)
    if cargo:
        block = cargo_block(cargo_text, GREEN,
                            width=4.1 if wrong else (1.0 if not cargo_text else 1.55),
                            size=36 if wrong else 28)
        block.next_to(top, UP, buff=0.18)
        g.add(block)
        g.cargo = block
    g.anticodon = anticodon
    g.tip = top
    if labels:
        low = T("anticodon", 30, YELLOW).next_to(anticodon, DOWN, buff=0.22)
        high = T("amino-acid end", 30, YELLOW).next_to(top, RIGHT, buff=0.35)
        g.add(low, high)
        g.low_label, g.high_label = low, high
    return g.scale(scale, about_point=c)


def link_world(with_trna=False):
    ribbon = codon_ribbon(y=-1.35)
    window = reading_window()
    start = T("start", 28, GOLD).next_to(ribbon[0], DOWN, buff=0.2)
    aa = cargo_block("amino acid", GREEN).move_to([-2.22, 1.55, 0])
    question = T("?", 54, GREY).move_to([-2.22, 0.05, 0])
    g = VGroup(ribbon, window, start, aa, question)
    if with_trna:
        t = trna_cartoon(center=[-2.2, 0.4, 0], scale=0.7, cargo=False)
        g.remove(question)
        g.add(t)
    return g


def ribosome_world(chain_len=3, a_trna=True, stop=False, ribbon_n=7):
    """The single carried E/P/A world for scenes 8--12."""
    ribbon = codon_ribbon(y=RIBO_Y, center=0, n=ribbon_n, stop=stop)
    upper = RoundedRectangle(corner_radius=0.45, width=9.5, height=2.8,
                             stroke_color=TEAL, stroke_width=6, fill_color=TEAL,
                             fill_opacity=0.10).move_to([0, 1.0, 0])
    lower = RoundedRectangle(corner_radius=0.32, width=13.3, height=1.2,
                             stroke_color=TEAL, stroke_width=5, fill_color=TEAL,
                             fill_opacity=0.08).move_to([0, RIBO_Y, 0])
    sites = VGroup(*[T(k, 38, TEAL, weight=BOLD).move_to([x, 2.75, 0])
                     for k, x in SLOT_X.items()])
    p = trna_cartoon(center=[SLOT_X["P"], 0.12, 0], scale=0.56, cargo=False)
    chain = VGroup(*[cargo_block("", GREEN, width=0.62, size=24) for _ in range(chain_len)])
    chain.arrange(RIGHT, buff=0.11).move_to([SLOT_X["P"], 1.82, 0])
    g = VGroup(upper, lower, ribbon, sites, p, chain)
    g.upper, g.lower, g.ribbon, g.sites, g.p_trna, g.chain = upper, lower, ribbon, sites, p, chain
    if a_trna:
        a = trna_cartoon(center=[SLOT_X["A"], 0.12, 0], scale=0.56, cargo=True,
                          cargo_text="")
        g.add(a)
        g.a_trna = a
    return g


def predict_picture(include_choices=True):
    ribbon = codon_ribbon(y=-1.65, center=1.9, n=4, start=False)
    window = RoundedRectangle(corner_radius=0.35, width=1.9, height=3.0,
                              stroke_color=TEAL, stroke_width=6, fill_color=TEAL,
                              fill_opacity=0.10).move_to([2.65, 0.45, 0])
    t = trna_cartoon(center=[-0.5, 0.25, 0], scale=0.72, cargo=True,
                     cargo_text="wrong amino acid", wrong=True)
    pair = VGroup(*[Line([-1.25 + i * 0.28, -1.2, 0], [-1.25 + i * 0.28, -1.4, 0],
                              color=GOLD, stroke_width=5) for i in range(3)])
    g = VGroup(ribbon, window, t, pair)
    g.trna, g.pair, g.window, g.ribbon = t, pair, window, ribbon
    if include_choices:
        reject = boxed_label("reject?", GREY, 30).move_to([-4.9, 1.7, 0])
        accept = boxed_label("accept?", GOLD, 30).move_to([5.55, 1.7, 0])
        g.add(reject, accept)
        g.reject, g.accept = reject, accept
    return g


def checkpoint_world():
    left_title = T("charge", 30, GOLD).move_to([-3.7, 2.8, 0])
    right_title = T("pair", 30, GOLD).move_to([3.75, 2.8, 0])
    t = trna_cartoon(center=[-3.7, 0.15, 0], scale=0.68, cargo=True, cargo_text="")
    clamp_l = Arc(radius=1.1, start_angle=-PI / 2, angle=PI, color=TEAL,
                  stroke_width=8, arc_center=[-3.9, 0.8, 0])
    ribbon = codon_ribbon(y=-1.65, center=3.75, n=3, start=False)
    window = RoundedRectangle(corner_radius=0.08, width=2.0, height=3.0,
                              stroke_color=TEAL, stroke_width=6, fill_color=TEAL,
                              fill_opacity=0.09).move_to([3.75, 0.45, 0])
    path = CurvedArrow([-2.6, 0.5, 0], [2.25, 0.5, 0], angle=-0.4,
                       color=GOLD, stroke_width=4)
    g = VGroup(left_title, right_title, t, clamp_l, ribbon, window, path)
    g.trna, g.clamp, g.ribbon, g.window, g.path = t, clamp_l, ribbon, window, path
    return g


class S00LinkQuestion(SpokenScene):
    def construct(self):
        ribbon = codon_ribbon(y=-1.35)
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.12) for c in ribbon], lag_ratio=0.08), run_time=1.0)
        self.at("How does each box")
        window = reading_window()
        aa = cargo_block("amino acid", GREEN).move_to([-2.22, 1.55, 0])
        q = T("?", 54, GREY).move_to([-2.22, 0.05, 0])
        self.play(Create(window), FadeIn(aa, shift=DOWN * 0.2), FadeIn(q), run_time=0.8)
        self.at("Keep the same blue")
        start = T("start", 28, GOLD).next_to(ribbon[0], DOWN, buff=0.2)
        self.play(FadeIn(start), Indicate(ribbon, color=BLUE, scale_factor=1.02), run_time=0.8)
        self.at("and teal reading")
        self.play(Indicate(window, color=TEAL, scale_factor=1.08), run_time=0.6)
        self.at("Now add the adapter")
        trna = trna_cartoon(center=[-2.2, 0.4, 0], scale=0.7, cargo=False)
        self.play(FadeOut(q), FadeIn(trna, shift=LEFT * 0.3), run_time=0.9)
        bob(aa, amp=0.05)
        self.add(scope_tag("schematic"))
        self.finish()


class S01Title(TitleCard):
    LESSON = "The Genetic Code and Translation"
    TITLE = "How Codons Become a Chain"

    def construct(self):
        world = link_world(with_trna=True).set_opacity(0.42).shift(DOWN * 0.6)
        title = T(self.TITLE, 52, TEXT, font=TITLE_FONT)
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4)
        card = VGroup(title, rule).arrange(DOWN, buff=0.3).move_to([0, 1.65, 0])
        self.add(world, scope_tag("schematic"))
        self.play(FadeIn(card), run_time=0.55)
        self.play(world[1].animate.shift(RIGHT * 0.45), rate_func=there_and_back, run_time=0.9)
        self.finish()


class S02Adaptor(SpokenScene):
    def construct(self):
        t = trna_cartoon(center=[0, 0.15, 0], scale=1.25, cargo=False)
        self.play(Create(t[0]), FadeIn(t[1]), FadeIn(t[2]), run_time=1.0)
        self.at("Its anticodin")
        low = T("anticodon", 32, YELLOW).move_to([-3.5, -1.9, 0])
        codon = codon_ribbon(y=-2.65, center=-0.94, n=1, start=False)
        self.play(FadeIn(low), codon.animate.shift(RIGHT * 0.5), run_time=0.8)
        self.at("Its other end")
        high = T("amino-acid end", 32, YELLOW).next_to(t.tip, RIGHT, buff=0.35)
        cargo = cargo_block("amino acid", GREEN).next_to(t.tip, UP, buff=0.25)
        self.play(FadeIn(high), FadeIn(cargo, shift=DOWN * 0.35), run_time=0.8)
        self.at("The adapter keeps")
        self.play(Rotate(VGroup(t, cargo, low, high), angle=0.08, about_point=ORIGIN,
                         rate_func=there_and_back), run_time=1.4)
        self.at("as it moves")
        self.play(VGroup(t, cargo, low, high).animate.shift(RIGHT * 0.35),
                  codon.animate.shift(RIGHT * 0.35), rate_func=there_and_back, run_time=1.1)
        self.finish()


class S03Charging(SpokenScene):
    def construct(self):
        t = trna_cartoon(center=[0, -0.2, 0], scale=0.95, cargo=False)
        self.play(FadeIn(t, shift=UP * 0.2), run_time=0.8)
        self.at("an aminosil")
        clamp = VGroup(Arc(radius=1.35, start_angle=-PI / 2, angle=PI, color=TEAL,
                           stroke_width=10, arc_center=[0.45, 0.9, 0]),
                       Arc(radius=1.05, start_angle=PI / 2, angle=PI, color=TEAL,
                           stroke_width=10, arc_center=[0.55, 0.9, 0]))
        enzyme = T("synthetase", 32, TEAL).move_to([0.4, 3.0, 0])
        self.play(Create(clamp), FadeIn(enzyme), run_time=0.9)
        pulse(clamp, base=10, amp=3, speed=3.0)
        bob(enzyme, amp=0.1, speed=2.0)
        self.at("The enzyme selects")
        choices = VGroup(*[cargo_block("", GREEN, width=0.72) for _ in range(4)])
        choices.arrange(DOWN, buff=0.22).move_to([-4.0, 0.7, 0])
        self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.35) for b in choices], lag_ratio=0.12), run_time=0.8)
        self.at("and the transfer")
        selected = choices[1]
        self.play(selected.animate.move_to([1.15, 2.0, 0]),
                  *[b.animate.shift(LEFT * 0.8).set_opacity(0.25) for b in choices if b is not selected],
                  run_time=1.0)
        self.at("Some synthetases")
        path = CurvedArrow([1.7, 0.5, 0], [4.4, -1.0, 0], angle=0.5,
                           color=GREY, stroke_width=4)
        edit = T("editing may remove errors", 29, GREY).next_to(path, DOWN, buff=0.18)
        self.play(Create(path), FadeIn(edit), run_time=0.8)
        self.at("remove mistakes")
        self.play(FadeOut(choices[0]), FadeOut(choices[2]), FadeOut(choices[3]),
                  selected.animate.next_to(t.tip, UP, buff=0.18), run_time=0.9)
        self.finish()


class S04Checks(SpokenScene):
    def construct(self):
        w = checkpoint_world()
        self.play(FadeIn(w.clamp), FadeIn(w.trna), run_time=0.9)
        self.at("The synthetase chooses")
        self.play(Indicate(w.trna.cargo, color=GREEN, scale_factor=1.12), FadeIn(w[0]), run_time=0.7)
        self.at("At the ribosome")
        self.play(Create(w.path), FadeIn(w.ribbon), FadeIn(w.window), FadeIn(w[1]), run_time=1.0)
        travel = trna_cartoon(center=[-3.7, 0.15, 0], scale=0.68, cargo=True, cargo_text="")
        self.add(travel)
        self.remove(w.trna)
        self.play(travel.animate.move_to([3.75, 0.2, 0]), run_time=2.0, rate_func=smooth)
        self.at("The growing chain")
        chain = VGroup(*[cargo_block("", GREEN, width=0.62) for _ in range(4)])
        chain.arrange(RIGHT, buff=0.1).move_to([3.75, 2.2, 0])
        self.play(FadeIn(chain, shift=RIGHT * 0.2), run_time=0.8)
        self.at("whatever cargo arrived")
        self.play(Indicate(travel.cargo, color=GREEN), travel.cargo.animate.shift(UP * 0.25), run_time=0.8)
        self.at("Charge -transfer")
        cap = caption("Charged tRNAs connect codons to the growing protein.", color=GOLD)
        self.play(FadeIn(cap, shift=UP * 0.15), run_time=0.8)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        p = predict_picture(include_choices=False)
        self.play(FadeIn(p.trna, shift=RIGHT * 0.3), FadeIn(p.ribbon), FadeIn(p.window), run_time=0.9)
        pulse(p.window, base=6, amp=2.5, speed=2.5)
        bob(p.trna.cargo, amp=0.12, speed=2.4)
        scan = Dot([2.65, 1.2, 0], radius=0.14, color=GOLD)
        scan._st = 0.0

        def _scan(mob, dt):
            mob._st += dt
            mob.move_to([2.65 + 0.6 * np.sin(1.6 * mob._st), 1.2 + 0.3 * np.cos(3.2 * mob._st), 0])
        scan.add_updater(_scan)
        self.add(scan)
        self.at("carries the wrong")
        self.play(Indicate(p.trna.cargo, color=GREEN, scale_factor=1.08), run_time=0.7)
        self.at("but its anticodin")
        self.play(Create(p.pair), run_time=0.6)
        pulse(p.pair, base=5, amp=2, speed=3)
        self.at("Will the ribosome")
        choices = VGroup(boxed_label("reject?", GREY, 30).move_to([-4.9, 1.7, 0]),
                         boxed_label("accept?", GOLD, 30).move_to([5.55, 1.7, 0]))
        self.play(FadeIn(choices[0], shift=RIGHT * 0.2), FadeIn(choices[1], shift=LEFT * 0.2), run_time=0.8)
        bob(choices[0], amp=0.12, speed=2.2, seed=1)
        bob(choices[1], amp=0.12, speed=2.2, seed=2)
        self.at("or accept")
        q = question_card("Will the ribosome reject the adaptor, or accept it?")
        self.play(FadeIn(q.question), run_time=0.6)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "Will the ribosome reject the adaptor, or accept it?"
    SECONDS = 4.5

    def backdrop(self):
        return predict_picture(include_choices=True)


class S07Reveal(SpokenScene):
    def construct(self):
        p = predict_picture(include_choices=True)
        self.add(p)
        self.at("pairing check passes")
        self.play(p.trna.animate.shift(RIGHT * 2.7), p.window.animate.set_stroke(opacity=0.0),
                  p.accept.animate.set_color(GOLD), run_time=1.1)
        self.at("does not inspect")
        self.play(p.trna.cargo.animate.shift(UP * 0.3), Indicate(p.pair, color=GOLD), run_time=0.8)
        self.at("wrong cargo can")
        chain = VGroup(*[cargo_block("", GREEN, width=0.62) for _ in range(3)])
        chain.arrange(RIGHT, buff=0.1).move_to([3.5, 2.35, 0])
        added = cargo_block("", GREEN, width=0.62).next_to(chain, RIGHT, buff=0.1)
        self.play(FadeIn(chain), Transform(p.trna.cargo, added),
                  FadeOut(p.reject), FadeOut(p.accept), run_time=1.0)
        self.at("Accuracy therefore")
        w = checkpoint_world()
        self.play(FadeOut(VGroup(p, chain)), FadeIn(w), run_time=1.0)
        self.at("charging before")
        self.play(Indicate(VGroup(w.clamp, w.trna), color=TEAL, scale_factor=1.03), run_time=0.8)
        self.at("pairing at")
        self.play(Indicate(VGroup(w.ribbon, w.window), color=TEAL, scale_factor=1.03), run_time=0.8)
        self.finish()


class S08Sites(SpokenScene):
    def construct(self):
        r = ribosome_world(chain_len=3, a_trna=False)
        self.play(FadeIn(r.upper, shift=DOWN * 0.2), FadeIn(r.lower, shift=UP * 0.2),
                  FadeIn(r.ribbon), run_time=0.9)
        self.at("The P site")
        self.play(FadeIn(r.sites[1]), FadeIn(r.p_trna, shift=UP * 0.2), FadeIn(r.chain), run_time=0.8)
        self.at("carrying the growing")
        self.play(r.chain.animate.shift(RIGHT * 0.2), rate_func=there_and_back, run_time=0.9)
        self.at("The I site")
        a = trna_cartoon(center=[5.4, 0.12, 0], scale=0.56, cargo=True, cargo_text="")
        self.play(FadeIn(r.sites[2]), FadeIn(a), run_time=0.6)
        self.play(a.animate.move_to([SLOT_X["A"], 0.12, 0]), run_time=1.3)
        self.at("matches the next")
        self.play(Indicate(a.anticodon, color=GOLD), Indicate(r.ribbon[5], color=BLUE), run_time=0.8)
        self.at("The E site")
        self.play(FadeIn(r.sites[0]), run_time=0.5)
        self.at("is the exit")
        exit_arrow = Arrow([-3.0, 0.7, 0], [-5.3, 0.7, 0], buff=0,
                           color=GREY, stroke_width=5)
        self.play(GrowArrow(exit_arrow), run_time=0.8)
        self.finish()


class S09Transfer(SpokenScene):
    def construct(self):
        r = ribosome_world(chain_len=3, a_trna=True)
        self.add(r)
        self.at("transfers the chain")
        self.play(r.chain.animate.move_to([SLOT_X["A"], 2.1, 0]), run_time=1.5,
                  path_arc=-0.45)
        self.at("amino acid in")
        self.play(r.a_trna.cargo.animate.next_to(r.chain, RIGHT, buff=0.1), run_time=0.8)
        self.at("Then the ribosome")
        self.play(r.ribbon.animate.shift(LEFT * CODON_W), run_time=1.5, rate_func=smooth)
        self.at("chain -bearing")
        empty = r.p_trna
        charged = r.a_trna
        self.play(charged.animate.shift(LEFT * (SLOT_X["A"] - SLOT_X["P"])),
                  r.chain.animate.shift(LEFT * (SLOT_X["A"] - SLOT_X["P"])),
                  empty.animate.shift(LEFT * (SLOT_X["P"] - SLOT_X["E"])), run_time=1.6)
        self.at("empty adapter")
        self.play(empty.animate.shift(LEFT * 3.2).set_opacity(0.0), run_time=1.4)
        self.finish()


class S10Ribozyme(SpokenScene):
    def construct(self):
        r = ribosome_world(chain_len=2, a_trna=True)
        self.add(r)
        self.at("not merely a track")
        self.play(Indicate(r.upper, color=TEAL, scale_factor=1.03), run_time=0.8)
        self.at("large subunit RNA")
        pocket = Ellipse(width=4.6, height=1.45, color=GOLD, stroke_width=0,
                         fill_color=GOLD, fill_opacity=0.08).move_to([1.3, 1.35, 0])
        lab = T("RNA-lined pocket", 32, GOLD).move_to([-2.7, 3.25, 0])
        self.play(Create(pocket), FadeIn(lab), run_time=0.9)
        self.at("positions")
        left_end = cargo_block("growing end", GREEN, width=1.9, size=25).move_to([-1.2, 1.15, 0])
        right_end = cargo_block("next amino acid", GREEN, width=2.6, size=25).move_to([2.2, 1.15, 0])
        self.play(FadeOut(r.chain), FadeOut(r.a_trna.cargo),
                  FadeIn(left_end), FadeIn(right_end), run_time=0.7)
        self.at("catalyzes peptide")
        self.play(left_end.animate.move_to([-0.9, 1.15, 0]),
                  right_end.animate.move_to([1.9, 1.15, 0]), run_time=1.1)
        self.at("reaction occurs")
        self.play(Indicate(pocket, color=GOLD, scale_factor=1.03), run_time=0.8)
        self.at("That is why")
        ribozyme = boxed_label("ribozyme", TEAL, 38).move_to([0, 3.05, 0])
        self.play(FadeOut(r.sites), swap(lab, ribozyme), run_time=0.8)
        pulse(ribozyme.box, base=3, amp=1.5, speed=3)
        self.at("called a ribosome")
        self.play(FadeOut(VGroup(pocket, left_end, right_end)),
                  r.chain.animate.move_to([0, 1.82, 0]), run_time=0.9)
        self.finish()


class S11Repeat(SpokenScene):
    def construct(self):
        r = ribosome_world(chain_len=2, a_trna=False, ribbon_n=5)
        self.add(r)
        self.at("blue ribbon moves")
        self.play(r.ribbon.animate.shift(LEFT * CODON_W), run_time=1.8, rate_func=linear)
        self.at("Each accepted adapter")
        a1 = trna_cartoon(center=[5.3, 0.12, 0], scale=0.56, cargo=True, cargo_text="")
        self.play(FadeIn(a1), a1.animate.move_to([SLOT_X["A"], 0.12, 0]), run_time=1.3)
        self.at("adds a green")
        new1 = cargo_block("", GREEN, width=0.62).move_to([2.65, 2.1, 0])
        self.play(FadeIn(new1), a1.animate.shift(LEFT * 2.65),
                  r.p_trna.animate.shift(LEFT * 2.65), run_time=1.4)
        self.at("chain grows")
        self.play(new1.animate.next_to(r.chain, RIGHT, buff=0.11),
                  r.ribbon.animate.shift(LEFT * CODON_W), run_time=1.2)
        self.at("ribosome repeats")
        a2 = trna_cartoon(center=[5.3, 0.12, 0], scale=0.56, cargo=True, cargo_text="")
        self.play(FadeIn(a2), a2.animate.move_to([SLOT_X["A"], 0.12, 0]), run_time=1.2)
        self.at("without changing")
        new2 = cargo_block("", GREEN, width=0.62).move_to([2.65, 2.1, 0])
        self.play(FadeIn(new2), a2.animate.shift(LEFT * 2.65),
                  new2.animate.next_to(new1, RIGHT, buff=0.11), run_time=1.2)
        self.finish()


class S12Stop(SpokenScene):
    def construct(self):
        r = ribosome_world(chain_len=5, a_trna=False, stop=True)
        self.add(r)
        self.at("stop enters")
        self.play(r.ribbon.animate.shift(LEFT * CODON_W), Indicate(r.ribbon[-1], color=RED), run_time=1.2)
        self.at("release factor")
        factor = cargo_block("release factor", RED, width=2.15, size=27).move_to([5.0, 0.5, 0])
        self.play(FadeIn(factor), factor.animate.move_to([SLOT_X["A"], 0.5, 0]), run_time=1.1)
        self.at("completed chain")
        self.play(r.chain.animate.shift(UP * 1.25), FadeOut(r.sites), run_time=1.0)
        self.at("ribosome can")
        self.play(r.upper.animate.shift(UP * 0.8), r.lower.animate.shift(DOWN * 0.55),
                  FadeOut(VGroup(r.p_trna, factor, r.ribbon)), run_time=1.2)
        self.at("stop adds no")
        no_add = T("no amino acid added", 34, RED).move_to([0, 0.1, 0])
        self.play(FadeIn(no_add), run_time=0.7)
        self.finish()


class S13Rule(SpokenScene):
    def construct(self):
        ribbon = codon_ribbon(y=-1.55, center=-3.9, n=2, start=False)
        t = trna_cartoon(center=[-1.1, 0.05, 0], scale=0.72, cargo=True, cargo_text="")
        window = RoundedRectangle(corner_radius=0.45, width=12.0, height=4.9,
                                  stroke_color=TEAL, stroke_width=6, fill_color=TEAL,
                                  fill_opacity=0.07).move_to([0.5, 0.25, 0])
        chain = VGroup(*[cargo_block("", GREEN, width=0.7) for _ in range(5)])
        chain.arrange(RIGHT, buff=0.12).move_to([3.7, 1.8, 0])
        self.play(FadeIn(window), FadeIn(ribbon), run_time=0.8)
        self.at("never touches")
        gap = DoubleArrow(ribbon.get_right() + RIGHT * 0.2, t.anticodon.get_left() + LEFT * 0.15,
                          color=GREY, stroke_width=4, buff=0)
        self.play(GrowArrow(gap), run_time=0.7)
        self.at("charged adapter")
        self.play(FadeIn(t, shift=RIGHT * 0.3), run_time=0.8)
        self.at("makes the connection")
        self.play(FadeOut(gap), FadeIn(chain, shift=RIGHT * 0.2), run_time=0.8)
        self.at("ribosome preserves")
        self.play(Indicate(window, color=TEAL, scale_factor=1.02), run_time=0.7)
        self.at("adapter carries identity")
        pulse_dot = Dot(ribbon[0].get_center(), radius=0.14, color=GOLD)
        self.add(pulse_dot)
        path = VMobject().set_points_smoothly([ribbon[0].get_center(), t.anticodon.get_center(),
                                               t.tip.get_center(), chain.get_left()])
        self.play(MoveAlongPath(pulse_dot, path), run_time=2.0, rate_func=linear)
        self.at("code to the chain")
        self.play(FadeOut(VGroup(ribbon, t, window, chain, pulse_dot)), run_time=0.9)
        self.finish()


class S14End(EndCard):
    LINE = "Charged tRNAs connect codons to the growing protein."
