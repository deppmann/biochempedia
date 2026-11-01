"""A survival factor has a ceiling  (Developmental Neuroscience, neurotrophic hypothesis)

COLOR MAP (one color per concept, whole video)
  BLUE   = a neuron (made, status not yet decided)
  GREEN  = a neuron that survives / the survival curve
  RED    = a neuron that dies or is lost / blocked / antiserum
  YELLOW = nerve growth factor (NGF) and "what the factor can support"
  TEAL   = the number of neurons made (the ceiling)
  PURPLE = the receptor TrkA (the knockout)
  GREY   = target tissue, axes, structure, empty slots
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
GA = 2.399963


def disk_pts(n, sp, center):
    """phyllotaxis points: the first k are the same for any n."""
    return [np.array([center[0] + sp * np.sqrt(k + 0.5) * np.cos(k * GA),
                      center[1] + sp * np.sqrt(k + 0.5) * np.sin(k * GA), 0]) for k in range(n)]


def dot(p, color=BLUE, r=0.16, op=0.95):
    return Circle(radius=r, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=op).move_to(p)


def slot(p, r=0.16):
    return DashedVMobject(Circle(radius=r, stroke_color=GREY, stroke_width=2, stroke_opacity=0.7).move_to(p), num_dashes=10)


def to_state(d, color, op):
    return d.animate.set_stroke(color, opacity=op).set_fill(color, opacity=op * 0.95)


def status(text, color=GREY, y=-3.3, x=0.0):
    return T(text, 26, color).move_to([x, y, 0])


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def inhib(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b + perp * 0.26, b - perp * 0.26, color=color, stroke_width=w + 1))


def cross(center, s=0.4, color=RED):
    c = np.array(center, float)
    return VGroup(Line(c + [-s, -s, 0], c + [s, s, 0], color=color, stroke_width=7),
                  Line(c + [-s, s, 0], c + [s, -s, 0], color=color, stroke_width=7))


def grid_pts(center, cols=4, rows=3, sp=0.95):
    out = []
    for r in range(rows):
        for c in range(cols):
            out.append(np.array([center[0] + (c - (cols - 1) / 2) * sp, center[1] + ((rows - 1) / 2 - r) * sp, 0]))
    return out


def axes_at(origin, w, h, xlabel, ylabel):
    o = np.array(origin, float)
    xa = Arrow(o, o + [w, 0, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.2)
    ya = Arrow(o, o + [0, h, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.2)
    xl = T(xlabel, 26, GREY).move_to(o + [w - (1.6 if len(xlabel) < 20 else 2.8), -0.5, 0])
    yl = T(ylabel, 26, GREY).rotate(PI / 2).move_to(o + [-0.55, h / 2, 0])
    return VGroup(xa, ya, xl, yl)


class S00Title(TitleCard):
    LESSON = "The neurotrophic hypothesis tested"
    TITLE = "Neurons Compete for Limited Support"

# Six schematic neurons: no numerical experimental claims are encoded in these counts.
NY = [2.0 - 0.8 * i for i in range(6)]
NX = -5.3
TX0 = 1.8
WIN = [0, 2, 4]
FACT_PTS = [np.array([3.0 + i * 0.7, 0.25, 0]) for i in range(3)]


def build_race():
    neu = VGroup(*[dot([NX, y, 0], BLUE, r=0.22) for y in NY])
    axs = VGroup(*[Line([NX + 0.22, y, 0], [TX0, y, 0], color=BLUE,
                       stroke_width=3, stroke_opacity=0.8) for y in NY])
    tgt = RoundedRectangle(corner_radius=0.25, width=3.4, height=5.2,
                           stroke_color=GREY, stroke_width=3,
                           fill_color=GREY, fill_opacity=0.15).move_to([3.5, 0, 0])
    tlbl = T("target tissue", 28, GREY).move_to([3.5, 2.95, 0])
    return neu, axs, tgt, tlbl


def ganglion(center, n=6, sp=0.63, radius=0.25):
    return VGroup(*[dot(p, r=radius) for p in disk_pts(n, sp, center)])


def fibres(neurons, length=1.3):
    return VGroup(*[Line(d.get_right(), d.get_right() + RIGHT * length,
                        color=BLUE, stroke_width=3) for d in neurons])


def heading(text, color=TEXT):
    return T(text, 32, color, font=TITLE_FONT).move_to([0, 3.15, 0])


class S03Limit(SpokenScene):
    def construct(self):
        neu, axs, tgt, tlbl = build_race()
        self.at("Developing neurons")
        self.play(FadeIn(neu), Create(axs), FadeIn(tgt), FadeIn(tlbl), run_time=1.1)
        fd = VGroup(*[dot(p, YELLOW, r=0.2) for p in FACT_PTS])
        fc = chip("limited factor", YELLOW, 26).move_to([3.5, -1.5, 0])
        self.at("limited supply")
        self.play(FadeIn(fd), FadeIn(fc), run_time=0.7)
        idea = status("Competition for limited target-derived support", TEXT)
        self.at("That is the neurotrophic hypothesis")
        self.play(FadeIn(idea), run_time=0.7)
        self.at("Neurons are made in excess")
        self.play(Indicate(neu, color=BLUE, scale_factor=1.12), run_time=0.8)
        self.at("The target is the tissue")
        self.play(Indicate(tgt, color=GREY, scale_factor=1.03), run_time=0.7)
        self.at("an axon grows")
        self.play(ShowPassingFlash(axs.copy().set_color(TEXT), time_width=0.5), run_time=1.0)
        self.at("It supplies the factor")
        self.play(*[fd[k].animate.move_to([TX0, NY[i], 0]) for k, i in enumerate(WIN)], run_time=1.0)
        self.play(*[to_state(neu[i], GREEN, 0.95) for i in WIN],
                  *[axs[i].animate.set_color(GREEN) for i in WIN], FadeOut(fd), run_time=0.5)
        lose = [i for i in range(6) if i not in WIN]
        death = status("Too little support → apoptosis", RED)
        self.at("Neurons that get too little")
        self.play(FadeOut(idea), run_time=0.2)
        self.play(*[to_state(neu[i], RED, 0.95) for i in lose],
                  *[axs[i].animate.set_color(RED) for i in lose], FadeIn(death), run_time=0.4)
        self.at("die by apoptosis")
        self.play(*[FadeOut(neu[i]) for i in lose], *[FadeOut(axs[i]) for i in lose], run_time=1.0)
        self.at("Competition lets")
        self.play(FadeOut(death), run_time=0.25)
        self.play(FadeIn(idea), FadeOut(fc),
                  Indicate(tgt, color=YELLOW, scale_factor=1.02), run_time=0.55)
        self.finish()


class S02Two(SpokenScene):
    def construct(self):
        left = ganglion([-3.7, 0, 0], sp=0.52)
        right = ganglion([2.4, 0, 0], sp=0.52)
        target_l = chip("target", GREY, 26).move_to([-1.5, 0, 0])
        target_r = chip("target", GREY, 26).move_to([4.7, 0, 0])
        label_l = T("Remove target", 30, RED).move_to([-3.3, 2.5, 0])
        label_r = T("Add target", 30, YELLOW).move_to([3.3, 2.5, 0])
        self.at("Remove a target")
        self.add(left, target_l)
        self.play(FadeIn(label_l), target_l.animate.shift(RIGHT * 0.5).set_opacity(0), run_time=0.6)
        self.at("more neurons die")
        self.play(*[to_state(d, RED, 0.05) for d in left[:4]], run_time=0.8)
        self.at("Add target")
        self.play(FadeIn(right), FadeIn(label_r), FadeIn(target_r), run_time=0.5)
        self.at("fewer die")
        self.play(to_state(right[0], RED, 0.05), *[to_state(d, GREEN, 0.95) for d in right[1:]], run_time=0.6)
        head = heading("Chick spinal ganglia")
        early = ganglion([-3.8, 0, 0], sp=0.58)
        late = ganglion([2.8, 0, 0], sp=0.58)
        f_early, f_late = fibres(early, 0.8), fibres(late, 0.8)
        labels = VGroup(T("Formed", 28, BLUE).move_to([-3.5, -2.1, 0]),
                        T("Later", 28, GREY).move_to([3.1, -2.1, 0]))
        timeline = arr([-1.1, 0, 0], [0.7, 0, 0])
        self.at("In chick spinal ganglia")
        self.play(FadeOut(VGroup(left, right, target_l, target_r, label_l, label_r)), FadeIn(head), run_time=0.5)
        self.at("many neurons formed")
        self.play(FadeIn(early), FadeIn(labels[0]), run_time=0.6)
        self.at("grew fibers")
        self.play(Create(f_early), run_time=0.5)
        self.at("dying cells")
        self.play(GrowArrow(timeline), FadeIn(late), FadeIn(f_late), FadeIn(labels[1]), run_time=0.5)
        self.play(*[to_state(late[i], RED, 0.15) for i in [0, 2, 4]],
                  *[f_late[i].animate.set_stroke(RED, opacity=0.15) for i in [0, 2, 4]], run_time=0.6)
        self.at("The neurons were made")
        self.play(FadeIn(status("Made first → lost later", TEXT)), run_time=0.6)
        self.finish()


class S01Swell(SpokenScene):
    def construct(self):
        base = ganglion([1.1, 0, 0], sp=0.7, radius=0.3)
        lbl = T("sympathetic ganglion", 28, GREY).move_to([1.1, -2.65, 0])
        ngf = chip("NGF", YELLOW, 34).move_to([-4.6, 0, 0])
        arrow = arr([-3.5, 0, 0], [-1.8, 0, 0], YELLOW)
        head = heading("Nerve growth factor", YELLOW)
        self.at("Nerve growth factor")
        self.play(FadeIn(head), FadeIn(ngf), FadeIn(base), FadeIn(lbl), run_time=0.8)
        add = T("Addition · young mammals", 28, YELLOW).move_to([0, 2.3, 0])
        self.at("Give young mammals")
        self.play(FadeIn(add), GrowArrow(arrow), run_time=0.6)
        self.at("ganglia enlarge")
        self.play(base.animate.scale(1.45), run_time=0.9)
        anti = chip("anti-NGF serum", RED, 28).move_to([-4.6, 0, 0])
        block = T("Blockade · newborn mice", 28, RED).move_to([0, 2.3, 0])
        self.at("Block it with")
        self.play(base.animate.scale(1 / 1.45), ReplacementTransform(ngf, anti),
                  ReplacementTransform(add, block),
                  Transform(arrow, arr([-2.75, 0, 0], [-1.8, 0, 0], RED)), run_time=0.7)
        self.at("ganglia waste away")
        self.play(*[to_state(d, RED, 0.08) for d in base[1:]], base[0].animate.scale(0.7), run_time=0.9)
        question = chip("Antibodies: bind something else?", RED, 30).move_to([0, 0.6, 0])
        ngf_test = chip("NGF", YELLOW, 30).move_to([-2.4, -1.0, 0])
        unknown = chip("other target?", GREY, 30).move_to([2.4, -1.0, 0])
        self.at("But antibodies")
        self.play(FadeOut(VGroup(base, lbl, anti, arrow, block)), FadeIn(question), run_time=0.6)
        self.at("something other than")
        self.play(FadeIn(ngf_test), FadeIn(unknown), run_time=0.6)
        self.finish()


class S04Trka(SpokenScene):
    def construct(self):
        head = heading("Independent genetic tests")
        ngf = chip("No NGF", YELLOW, 30).move_to([-3.2, 2.1, 0])
        trka = chip("No TrkA receptor", PURPLE, 30).move_to([3.2, 2.1, 0])
        # Two populations for each independent disruption; schematic, not quantitative.
        groups = [ganglion([x, y, 0], n=4, sp=0.4, radius=0.19)
                  for x in [-3.2, 3.2] for y in [0.7, -1.0]]
        labels = VGroup(T("Sympathetic", 26, GREY).move_to([0, 0.7, 0]),
                        T("Many sensory", 26, GREY).move_to([0, -1.0, 0]))
        self.at("Genetics tests that doubt")
        self.play(FadeIn(head), run_time=0.5)
        self.at("Mice lacking NGF")
        self.play(FadeIn(ngf), FadeIn(VGroup(*groups[:2])), FadeIn(labels), run_time=0.6)
        self.at("its receptor")
        self.play(FadeIn(trka), FadeIn(VGroup(*groups[2:])), run_time=0.6)
        self.at("lose sympathetic neurons")
        self.play(*[to_state(d, RED, 0.08) for g in [groups[0], groups[2]] for d in g[:3]], run_time=0.7)
        self.at("many sensory neurons")
        self.play(*[to_state(d, RED, 0.08) for g in [groups[1], groups[3]] for d in g[:3]], run_time=0.7)
        null = heading("TrkA-null sympathetic ganglion", PURPLE)
        gang = ganglion([-2.2, 0, 0], sp=0.75, radius=0.3)
        axons = fibres(gang, 3.7)
        state = status("Initial formation", BLUE)
        self.at("Without TRKA")
        self.play(FadeOut(VGroup(head, ngf, trka, *groups, labels)), run_time=0.3)
        self.play(FadeIn(null), run_time=0.3)
        self.at("ganglion still forms")
        self.play(FadeIn(gang), FadeIn(state), run_time=0.6)
        self.at("axons start growing")
        self.play(Create(axons), run_time=0.9)
        self.at("Later the neurons die")
        self.play(*[to_state(d, RED, 0.06) for d in gang], axons.animate.set_stroke(RED, opacity=0.06),
                  FadeOut(state), run_time=1.0)
        self.at("What failed was survival")
        self.play(FadeIn(status("Survival failure", RED)), run_time=0.6)
        self.finish()


class S05Excess(SpokenScene):
    def construct(self):
        head = heading("Chick embryos · death period")
        untreated = ganglion([-3.2, 0.25, 0], sp=0.67, radius=0.3)
        treated = ganglion([3.2, 0.25, 0], sp=0.67, radius=0.3)
        labels = VGroup(T("Untreated", 28, GREY).move_to([-3.2, 2.15, 0]),
                        chip("Extra NGF", YELLOW, 28).move_to([3.2, 2.15, 0]))
        self.at("Add excess NGF")
        self.play(FadeIn(head), FadeIn(labels), FadeIn(untreated), FadeIn(treated), run_time=0.8)
        self.at("more neurons escape")
        self.play(*[to_state(d, RED, 0.9) for d in untreated[:3]], to_state(treated[0], RED, 0.9),
                  *[to_state(d, GREEN, 0.95) for d in untreated[3:]],
                  *[to_state(d, GREEN, 0.95) for d in treated[1:]], run_time=0.6)
        self.play(*[FadeOut(d) for d in untreated[:3]], FadeOut(treated[0]), run_time=0.7)
        readouts = VGroup(chip("Neuron count", TEAL, 24), chip("Dying cells", RED, 24),
                         chip("Division marker", TEAL, 24)).arrange(RIGHT, buff=0.45).move_to([0, -2.8, 0])
        self.at("Count neurons")
        self.play(FadeIn(readouts[0]), run_time=0.4)
        self.at("dying cells")
        self.play(FadeIn(readouts[1]), run_time=0.4)
        self.at("mark dividing cells")
        self.play(FadeIn(readouts[2]), run_time=0.5)
        early = heading("Early exposure is a different condition", YELLOW)
        cell = dot([-0.6, 0, 0], BLUE, r=0.45)
        pair = VGroup(dot([-1.0, 0, 0], BLUE, r=0.4), dot([1.0, 0, 0], BLUE, r=0.4))
        self.at("Early NGF")
        self.play(FadeOut(VGroup(head, labels, untreated, treated, readouts)), run_time=0.25)
        self.play(FadeIn(early), FadeIn(cell), run_time=0.25)
        self.at("can also increase division")
        self.play(ReplacementTransform(cell, pair), FadeIn(status("Can increase division", TEAL)), run_time=0.9)
        self.finish()


class S08Return(SpokenScene):
    def construct(self):
        head = heading("Support across a distance")
        body = dot([-5.0, 0, 0], BLUE, r=0.65)
        axon = Line([-4.35, 0, 0], [3.5, 0, 0], color=BLUE, stroke_width=6)
        target = RoundedRectangle(corner_radius=0.22, width=2.1, height=3.8,
                                  color=GREY, fill_color=GREY, fill_opacity=0.15).move_to([4.55, 0, 0])
        labels = VGroup(T("cell body", 28, BLUE).move_to([-5, -1.35, 0]),
                        T("axon", 28, BLUE).move_to([-0.5, -0.6, 0]),
                        T("target", 28, GREY).move_to([4.55, 2.35, 0]))
        self.at("How does a target")
        self.play(FadeIn(head), FadeIn(body), Create(axon), FadeIn(target), FadeIn(labels), run_time=0.8)
        factor = dot([4.6, 0.7, 0], YELLOW, r=0.24)
        ending = Circle(radius=0.43, color=YELLOW, stroke_width=3).move_to([3.5, 0, 0])
        self.at("The factor acts")
        self.play(FadeIn(factor), run_time=0.4)
        self.at("at the axon ending")
        self.play(factor.animate.move_to([3.5, 0, 0]), Create(ending), run_time=0.6)
        signal = dot([3.5, 0, 0], YELLOW, r=0.2)
        direction = arr([3.4, 1.3, 0], [-4.2, 1.3, 0], YELLOW)
        self.at("A signal returns")
        self.play(FadeOut(factor), FadeOut(ending), FadeIn(signal), GrowArrow(direction), run_time=0.5)
        self.at("along the axon")
        self.play(signal.animate.move_to([-5, 0, 0]), run_time=1.5, rate_func=linear)
        self.at("to support survival")
        self.play(FadeOut(signal), to_state(body, GREEN, 0.95),
                  FadeIn(status("Target → cell body", YELLOW)), run_time=0.6)
        self.finish()


class S09Dependence(SpokenScene):
    def construct(self):
        head = heading("Dependence varies with population and age")
        young = ganglion([-3.2, 0, 0], sp=0.6, radius=0.28)
        older = ganglion([3.2, 0, 0], sp=0.6, radius=0.28)
        labels = VGroup(T("Newborn", 30, GREY).move_to([-3.2, 2, 0]),
                        T("Older", 30, GREY).move_to([3.2, 2, 0]))
        serum = chip("Same anti-NGF serum", RED, 28).move_to([0, -2.7, 0])
        self.at("Dependence varies")
        self.play(FadeIn(head), FadeIn(young), FadeIn(older), FadeIn(labels), run_time=0.8)
        self.at("has much less effect")
        self.play(FadeIn(serum), *[to_state(d, RED, 0.07) for d in young[:5]],
                  to_state(older[0], RED, 0.2), run_time=0.9)
        pophead = heading("Different populations, different requirements")
        dependent = chip("NGF-dependent neurons", BLUE, 26).move_to([-2.4, 1.7, 0])
        ngf = chip("NGF", YELLOW, 26).move_to([4.2, 1.7, 0])
        a1 = arr([3.4, 1.7, 0], [0.9, 1.7, 0], YELLOW)
        motor = chip("Limb motor neurons", BLUE, 26).move_to([-2.4, 0.15, 0])
        no = T("Do not depend on NGF", 26, GREY).move_to([3.3, 0.15, 0])
        sensory = VGroup(T("Large sensory neurons", 26, BLUE), T("sense muscle stretch", 24, GREY)).arrange(DOWN, buff=0.15).move_to([-2.4, -1.8, 0])
        other = chip("Different neurotrophin", GREY, 24).move_to([3.6, -1.8, 0])
        a2 = arr([1.7, -1.8, 0], [0.1, -1.8, 0], GREY)
        self.at("Limb motor neurons")
        self.play(FadeOut(VGroup(head, young, older, labels, serum)), run_time=0.25)
        self.play(FadeIn(pophead), FadeIn(dependent), FadeIn(ngf),
                  GrowArrow(a1), FadeIn(motor), run_time=0.35)
        self.at("do not depend")
        self.play(FadeIn(no), run_time=0.5)
        self.at("Large sensory neurons")
        self.play(FadeIn(sensory), run_time=0.6)
        self.at("a different neurotrophin")
        self.play(FadeIn(other), GrowArrow(a2), run_time=0.6)
        self.finish()


class S10Wiring(SpokenScene):
    def construct(self):
        head = heading("Survival and wiring are different readouts")
        body_l = dot([-5.3, 0, 0], GREEN, r=0.44)
        body_r = dot([1.0, 0, 0], GREEN, r=0.44)
        target_l = RoundedRectangle(corner_radius=0.2, width=2.5, height=3.4, color=GREY,
                                    fill_color=GREY, fill_opacity=0.12).move_to([-1.7, 0, 0])
        target_r = target_l.copy().move_to([4.6, 0, 0])
        label_l = T("Target supplies NGF", 26, YELLOW).move_to([-3.3, 2.25, 0])
        label_r = T("Neuron makes NGF", 26, YELLOW).move_to([3.0, 2.25, 0])
        ax_l = Line([-4.86, 0, 0], [-2.5, 0, 0], color=BLUE, stroke_width=4)
        ax_r = Line([1.44, 0, 0], [3.8, 0, 0], color=BLUE, stroke_width=4)
        dense = VGroup(*[Line([-2.5, 0, 0], [-1.0, y, 0], color=BLUE, stroke_width=3)
                         for y in [-1.2, -0.6, 0, 0.6, 1.2]])
        sparse = VGroup(*[Line([3.8, 0, 0], [5.3, y, 0], color=BLUE, stroke_width=3)
                          for y in [-0.45, 0.45]])
        ngf_l = dot([-1.7, 1.2, 0], YELLOW, r=0.16)
        ngf_r = dot([1.0, 0.9, 0], YELLOW, r=0.16)
        normal = VGroup(body_l, target_l, label_l, ngf_l)
        altered = VGroup(body_r, target_r, label_r, ngf_r)
        self.at("Survival is only part")
        self.play(FadeIn(head), FadeIn(body_l), run_time=0.6)
        self.at("NGF also promotes")
        self.play(FadeIn(VGroup(target_l, label_l, ngf_l)), Create(ax_l), run_time=0.6)
        self.at("growth and branching")
        self.play(Create(dense), run_time=0.8)
        self.at("When sympathetic neurons")
        self.play(FadeIn(altered), run_time=0.7)
        self.at("axons still reach")
        self.play(Create(ax_r), run_time=0.7)
        self.at("but branch sparsely")
        self.play(Create(sparse), run_time=0.9)
        survived = VGroup(T("Alive", 26, GREEN).move_to([-5.3, -1.2, 0]),
                          T("Alive", 26, GREEN).move_to([1.0, -1.2, 0]))
        self.at("Keeping neurons alive")
        self.play(FadeIn(survived), run_time=0.5)
        self.at("does not explain their wiring")
        self.play(FadeIn(status("Survival ≠ pattern of innervation", TEXT)), run_time=0.6)
        self.finish()


class S06Ceiling(SpokenScene):
    def construct(self):
        head = heading("Smaller point: the survival ceiling")
        early = ganglion([-3.4, 0.25, 0], sp=0.65, radius=0.28)
        later = ganglion([3.4, 0.25, 0], sp=0.65, radius=0.28)
        # Empty slots mark the same starting population, not additional neurons.
        slots = VGroup(*[slot(d.get_center(), r=0.28) for d in later])
        labels = VGroup(T("Already made", 30, TEAL).move_to([-3.4, 2.15, 0]),
                        T("Survivors", 30, GREEN).move_to([3.4, 2.15, 0]))
        arrow = arr([-1.15, 0, 0], [1.15, 0, 0])
        self.at("A smaller closing point")
        self.play(FadeIn(head), run_time=0.6)
        self.at("For a fixed population")
        self.play(FadeIn(early), FadeIn(slots), FadeIn(labels), GrowArrow(arrow), run_time=0.7)
        self.at("survival alone cannot save more")
        # Only part of the population is initially supported; none has died here.
        self.play(FadeIn(VGroup(*later[:3])), run_time=0.7)
        cap = T("Survivors ≤ neurons already made", 30, TEAL).move_to([0, -2.7, 0])
        self.at("than were made")
        self.play(FadeIn(cap), run_time=0.6)
        ngf = chip("Extra factor", YELLOW, 26).move_to([0, 1.7, 0])
        self.at("Extra factor can spare")
        self.play(FadeIn(ngf), FadeIn(VGroup(*later[3:])),
                  *[to_state(d, GREEN, 0.95) for d in later[:3]], run_time=0.7)
        self.at("would otherwise die")
        self.play(*[to_state(d, GREEN, 0.95) for d in later[3:]],
                  Indicate(cap, color=TEAL, scale_factor=1.02), run_time=0.7)
        self.finish()



class S07End(EndCard):
    LINE = "Neurons compete for limited target-derived survival support."
