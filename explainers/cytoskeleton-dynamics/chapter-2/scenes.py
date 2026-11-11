"""When a Drug Becomes a Test -- chapter 2 of the cytoskeleton pair.

COLOR MAP (same as chapter 1, plus one colour for the drug)
  GOLD     fresh ATP/GTP-bearing subunits
  BLUE     old ADP/GDP-bearing subunits (the lattice)
  GREEN    a tight end
  RED      a loose end / a catastrophe counter
  TEAL     the free-subunit gauge
  MAGENTA  the drug and everything it does (this chapter)
  TEXT     labels and neutral structure

Every picture is schematic; subunits are blocks, never molecular structures.
"""
import numpy as np
from types import SimpleNamespace
from bp_style import *  # noqa: F401,F403

GOLD_FRESH = GOLD
MAGENTA = "#E05CCB"

Y0 = -0.2          # the assembly-line lane
POOL_X = -5.9
LAT_X0 = 0.15
LAT_DX = 0.66
BW, BH = 0.60, 1.20


def until(scene, phrase, margin=0.25, floor=0.35, nth=0):
    return max(floor, scene.t_of(phrase, nth) - 0.2 - scene.elapsed() - margin)


def label(text, color=TEXT, size=30, weight=NORMAL):
    return T(text, size=size, color=color, weight=weight)


def subunit(x, y=Y0, color=BLUE, w=BW, h=BH):
    return RoundedRectangle(corner_radius=0.07, width=w, height=h, stroke_color=color, stroke_width=2.4,
                            fill_color=color, fill_opacity=0.42).move_to([x, y, 0])


def drifting_field(seed=1, n=34, opacity=0.55, speed=1.0):
    rng = np.random.RandomState(seed)
    dots = VGroup()
    n = int(round(n * 1.2))
    for _ in range(n):
        d = Dot([rng.uniform(-6.55, 6.55), rng.uniform(-3.55, 3.55), 0], radius=rng.uniform(0.08, 0.14), color=GOLD_FRESH)
        d.set_opacity(opacity)
        d.v = np.array([rng.uniform(-0.16, 0.18), rng.uniform(0.10, 0.24), 0]) * speed

        def drift(m, dt):
            m.shift(m.v * dt)
            if m.get_y() > 3.72:
                m.shift(DOWN * 7.35)
            if m.get_x() > 6.92:
                m.shift(LEFT * 13.75)
            elif m.get_x() < -6.92:
                m.shift(RIGHT * 13.75)
        d.add_updater(drift)
        dots.add(d)
    dots.set_z_index(-8)
    return dots


def bob(m, ax=0.0, ay=0.0, period=3.0, phase=0.0):
    """Slow oscillation of a mobject about where it was built."""
    m._bt = phase
    m._boff = np.zeros(3)

    def up(mm, dt):
        mm._bt += dt
        s = np.sin(2 * PI * mm._bt / period)
        off = np.array([ax * s, ay * s, 0.0])
        mm.shift(off - mm._boff)
        mm._boff = off
    m.add_updater(up)
    return m


def flow(x0, x1, y=Y0, n=6, speed=0.9, w=0.36, h=0.5):
    """Free gold subunits streaming left to right and being used up at the end."""
    L = x1 - x0
    g = VGroup(*[subunit(x0 + L * (i + 0.5) / n, y, GOLD_FRESH, w=w, h=h) for i in range(n)])
    g.spd = ValueTracker(speed)
    g.clock = 0.0

    def up(m, dt):
        m.clock += dt
        for i, b in enumerate(m):
            b.shift(RIGHT * m.spd.get_value() * dt)
            if b.get_x() > x1:
                b.shift(LEFT * L)
            f = (b.get_x() - x0) / L
            a = max(0.0, min(1.0, f * 5, (1 - f) * 6))
            b.set_fill(GOLD_FRESH, opacity=0.42 * a)
            b.set_stroke(GOLD_FRESH, opacity=a)
            b.set_y(y + 0.07 * np.sin(2.2 * m.clock + i))
    g.add_updater(up)
    return g


def lattice(n=10, color=BLUE, x0=LAT_X0, y=Y0, h=BH, w=BW, dx=LAT_DX):
    return VGroup(*[subunit(x0 + dx * i, y, color, w, h) for i in range(n)])


def pool_gauge(lvl):
    box = RoundedRectangle(corner_radius=0.12, width=1.0, height=4.2, stroke_color=TEAL, stroke_width=3,
                           fill_color=TEAL, fill_opacity=0.08).move_to([POOL_X, 0.0, 0])

    def mk():
        hh = max(0.05, 3.8 * lvl.get_value())
        return Rectangle(width=0.7, height=hh, stroke_width=0, fill_color=TEAL, fill_opacity=0.4).move_to([POOL_X, -1.9 + hh / 2, 0])
    fill = always_redraw(mk)
    lab = label("free pool", TEAL, 30, BOLD).move_to([POOL_X + 0.1, 2.5, 0])
    g = VGroup(box, fill, lab)
    g.lab = lab
    return g


def actin_world(level=0.85, n=10):
    w = SimpleNamespace()
    w.lvl = ValueTracker(level)
    w.pool = pool_gauge(w.lvl)
    w.flow = flow(-4.85, -0.5, Y0, 6, 0.9)
    w.lat = lattice(n)
    w.schem = label("schematic", TEXT, 24).set_opacity(0.8).move_to([5.3, -3.45, 0])
    return w


def spot(cx, cy, w, h):
    return RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=MAGENTA, stroke_width=5,
                            fill_color=MAGENTA, fill_opacity=0.10).move_to([cx, cy, 0])


def bracket(x0, x1, y, color=TEXT):
    return VGroup(Line([x0, y, 0], [x1, y, 0]), Line([x0, y, 0], [x0, y + 0.22, 0]),
                  Line([x1, y, 0], [x1, y + 0.22, 0])).set_stroke(color, 5)


# ---------------------------------------------------------------- icons and tags
def icon(kind):
    if kind == "target":
        return VGroup(Circle(radius=0.27, color=MAGENTA, stroke_width=4),
                      Line([-0.4, 0, 0], [0.4, 0, 0], color=MAGENTA, stroke_width=4),
                      Line([0, -0.4, 0], [0, 0.4, 0], color=MAGENTA, stroke_width=4))
    if kind == "dose":
        return VGroup(RoundedRectangle(corner_radius=0.08, width=0.38, height=0.85, stroke_color=MAGENTA, stroke_width=3),
                      Rectangle(width=0.26, height=0.5, stroke_width=0, fill_color=MAGENTA, fill_opacity=0.8).move_to([0, -0.14, 0]))
    return VGroup(RoundedRectangle(corner_radius=0.22, width=0.95, height=0.5, stroke_color=TEXT, stroke_width=3),
                  Dot([-0.15, 0.0, 0], radius=0.06, color=GOLD_FRESH), Dot([0.12, -0.05, 0], radius=0.06, color=GOLD_FRESH))


def tag(name, kind, w=3.5, h=1.1, size=34):
    box = RoundedRectangle(corner_radius=0.16, width=w, height=h, stroke_color=TEXT, stroke_width=3,
                           fill_color=TEXT, fill_opacity=0.06)
    t = label(name, TEXT, size, BOLD).move_to(box.get_center() + LEFT * (w * 0.2))
    ic = icon(kind).move_to(box.get_center() + RIGHT * (w * 0.30))
    g = VGroup(box, t, ic)
    g.box, g.icon = box, ic
    return g


# ---------------------------------------------------------------- the carried hook world (actin above, microtubule below)
AY = 2.3
MY = (-2.0, -2.5, -3.0)


def hook_world():
    w = SimpleNamespace()
    w.aflow = flow(-6.3, -0.45, AY, 6, 0.8, w=0.32, h=0.4)
    w.alat = VGroup(*[subunit(-0.05 + 0.5 * i, AY, BLUE, w=0.46, h=0.62) for i in range(12)])
    w.aend = SurroundingRectangle(w.alat[0], color=GREEN, buff=0.08, stroke_width=3)
    w.mflow = flow(-6.3, -0.45, MY[1], 6, 0.8, w=0.32, h=0.4)
    cols = VGroup()
    for i in range(12):
        c = GOLD_FRESH if i < 2 else BLUE
        cols.add(VGroup(*[subunit(-0.05 + 0.5 * i, y, c, w=0.46, h=0.44) for y in MY]))
    w.mt = cols
    bob(VGroup(cols[0], cols[1]), ax=0.14, period=3.2)
    w.alab = label("actin, schematic", TEXT, 28).move_to([-3.2, 3.3, 0])
    w.mlab = label("microtubule, schematic", TEXT, 26).move_to([-3.3, -3.55, 0])
    w.all = VGroup(w.aflow, w.alat, w.aend, w.mflow, w.mt, w.alab, w.mlab)
    return w


def bead_rows(r, ys, h, x_end, dx, n=10, bead_r=0.3):
    """n blocks split over r rows, each row ending at a bead on the right (barbed ends face left)."""
    k = n // r
    blocks, beads = VGroup(), VGroup()
    for ri in range(r):
        for j in range(k):
            blocks.add(subunit(x_end - dx * (k - 1 - j), ys[ri], BLUE, w=dx * 0.9, h=h))
        beads.add(Circle(radius=bead_r, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.5)
                  .move_to([x_end + dx * 0.5 + bead_r, ys[ri], 0]))
    return blocks, beads


# ================================================================ scenes
class S00Hook(SpokenScene):
    def construct(self):
        dots = drifting_field(2, 30, 0.5, 1.0)
        w = hook_world()
        self.add(dots, w.all)
        qs = [label("?", MAGENTA, 90, BOLD).set_opacity(0.6).move_to([x, 0.1, 0]) for x in (-4.0, -0.1, 3.4)]
        self.at("free subunits")
        self.play(FadeIn(qs[0], scale=1.3), run_time=0.6)
        self.at("Ns")
        self.play(FadeIn(qs[1], scale=1.3), qs[0].animate.set_opacity(0.3), run_time=0.6)
        self.at("and their")
        self.play(FadeIn(qs[2], scale=1.3), qs[1].animate.set_opacity(0.3), run_time=0.6)
        self.at("How can a drug")
        drug = chip("drug", MAGENTA, 34).move_to([0, 4.3, 0])
        self.play(drug.animate.move_to([0, 0.1, 0]), run_time=1.0)
        self.at("turn that rule")
        ghosts = [drug.copy() for _ in range(3)]
        self.remove(drug)
        self.add(*ghosts)
        self.play(*[g.animate.move_to([x, 0.1, 0]).set_opacity(0.6) for g, x in zip(ghosts, (-4.0, -0.1, 3.4))],
                  FadeOut(VGroup(*qs)), run_time=1.0)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Cytoskeletal Polymers and Dynamics"
    TITLE = "When a Drug Becomes a Test"

    def construct(self):
        dots = drifting_field(3, 38, 0.3, 0.9)
        self.add(dots)
        super().construct()


class S02Rule(SpokenScene):
    def construct(self):
        dots = drifting_field(4, 28, 0.4, 1.0)
        w = hook_world()
        self.add(dots, w.all)
        card = RoundedRectangle(corner_radius=0.3, width=12.4, height=3.4, stroke_color=TEXT, stroke_width=2.5,
                                fill_color=BG, fill_opacity=0.6).move_to([0, 0, 0])
        drug = chip("drug", MAGENTA, 34).move_to([0, 1.2, 0])
        tags = [tag("target", "target").move_to([-4.3, 0.05, 0]), tag("dose", "dose").move_to([0, 0.05, 0]),
                tag("system", "system").move_to([4.3, 0.05, 0])]
        links = [Line(drug.get_bottom(), t.get_top(), color=MAGENTA, stroke_width=5) for t in tags]
        oa = chip("conclusion A", TEXT, 26).move_to([-4.2, -1.3, 0])
        ob = chip("conclusion B", TEXT, 26).move_to([4.2, -1.3, 0])
        arrow = Arrow([1.9, -1.3, 0], [-1.9, -1.3, 0], buff=0, color=TEXT, stroke_width=8)
        arrow_l = arrow.copy()
        arrow_r = Arrow([-1.9, -1.3, 0], [1.9, -1.3, 0], buff=0, color=TEXT, stroke_width=8)
        for m in [drug, *tags, *links, oa, ob, arrow]:
            m.set_z_index(2)

        self.at("A drug")
        drug.move_to([0, 3.9, 0])
        self.play(FadeIn(card), drug.animate.move_to([0, 1.2, 0]), run_time=1.0)
        self.at("three labels")
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.2) for t in tags], lag_ratio=0.4), run_time=1.0)
        self.at("stay attached")
        self.play(*[Create(l) for l in links], FadeIn(oa), FadeIn(ob), FadeIn(arrow), run_time=0.9)
        self.at("target")
        self.play(Indicate(tags[0], color=MAGENTA, scale_factor=1.06), run_time=0.7)
        self.at("dose")
        self.play(Indicate(tags[1], color=MAGENTA, scale_factor=1.06), run_time=0.7)
        self.at("test system")
        self.play(Indicate(tags[2], color=MAGENTA, scale_factor=1.06), run_time=0.7)
        offs = [UP * 0.85, UP * 0.85 + RIGHT * 0.35, UP * 0.85]
        for k, cue in enumerate(("Remove any", "and the same", "can support")):
            self.at(cue)
            self.play(tags[k].icon.animate.shift(offs[k]), links[k].animate.set_opacity(0.12),
                      Transform(arrow, arrow_r.copy()), run_time=0.5)
            self.wait(0.2)
            self.play(tags[k].icon.animate.shift(-offs[k]), links[k].animate.set_opacity(1.0),
                      Transform(arrow, arrow_l.copy()), run_time=0.5)
        self.play(Indicate(drug, color=MAGENTA, scale_factor=1.12), run_time=0.8)
        self.finish()


def world_labels_s03(w):
    pl = w.pool.lab
    el = label("end", GREEN, 30, BOLD).move_to([LAT_X0, 0.95, 0])
    ll = label("lattice", BLUE, 30, BOLD).move_to([3.1, 0.95, 0])
    return pl, el, ll


class S03Sites(SpokenScene):
    def construct(self):
        dots = drifting_field(5, 26, 0.4, 1.0)
        w = actin_world()
        pl, el, ll = world_labels_s03(w)
        self.add(dots)
        box, fill = w.pool[0], w.pool[1]
        self.play(FadeIn(box), FadeIn(fill), FadeIn(w.flow), FadeIn(w.lat), FadeIn(w.schem), run_time=1.2)
        hero = subunit(-5.4, Y0, GOLD_FRESH, w=0.46, h=0.7).set_stroke(TEXT, 4)

        self.at("Free subunits")
        self.play(FadeIn(pl), FadeIn(hero), run_time=0.5)
        self.play(hero.animate.move_to([LAT_X0 - LAT_DX, Y0, 0]), run_time=1.0, rate_func=smooth)
        self.at("feed an end")
        self.play(FadeIn(el, shift=DOWN * 0.1), run_time=0.5)
        self.at("adds to")
        self.play(Indicate(hero, color=GOLD_FRESH, scale_factor=1.25), run_time=0.8)
        self.at("removes from")
        self.play(w.lat[9].animate.shift(RIGHT * 0.9).set_opacity(0), run_time=1.0)
        self.at("from a lattice")
        self.play(FadeIn(ll, shift=DOWN * 0.1), run_time=0.5)
        r1 = spot(POOL_X, 0.3, 1.75, 5.4)
        r2 = spot(0.0, 0.15, 2.0, 2.8)
        r3 = spot(3.1, 0.15, 6.9, 2.8)
        self.at("perturbation")
        self.play(FadeIn(r1), run_time=0.5)
        self.at("any of those")
        self.play(Transform(r1, r2), run_time=0.7)
        self.at("three places")
        self.play(Transform(r1, r3), run_time=0.8)
        self.finish()


def cup(x, y):
    u = VMobject().set_points_as_corners([[x - 0.4, y + 0.35, 0], [x - 0.4, y - 0.35, 0], [x + 0.4, y - 0.35, 0],
                                          [x + 0.4, y + 0.35, 0]]).set_stroke(MAGENTA, 7)
    b = subunit(x, y, GOLD_FRESH, w=0.4, h=0.5)
    return VGroup(u, b)


class S04Latrunculin(SpokenScene):
    def construct(self):
        dots = drifting_field(6, 26, 0.4, 1.0)
        w = actin_world(0.85)
        self.add(dots, w.pool, w.flow, w.lat, w.schem)
        lab = label("latrunculin A", MAGENTA, 32, BOLD).move_to([-2.7, 2.75, 0])
        n = ValueTracker(0)
        cnt = always_redraw(lambda: M(f"pairs: {int(round(n.get_value()))}", 30, MAGENTA).move_to([1.3, 2.75, 0]))
        self.play(FadeIn(lab, shift=DOWN * 0.1), FadeIn(cnt), run_time=0.7)
        cups = VGroup(*[cup(x, 1.55) for x in (-4.5, -3.5, -2.5, -1.5)])

        self.at("binds actin monomers")
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.3) for c in cups], lag_ratio=0.7), n.animate.set_value(4),
                  run_time=2.4, rate_func=linear)
        self.at("cannot join")
        self.play(Indicate(cups, color=MAGENTA, scale_factor=1.08), run_time=0.8)
        self.at("pool falls")
        self.play(w.lvl.animate.set_value(0.3), w.flow.spd.animate.set_value(0.4), run_time=1.8)
        self.at("less actin enters")
        self.play(Indicate(w.lat[0], color=BLUE, scale_factor=1.15), run_time=0.8)
        self.at("also speed loss")
        a1 = Arrow([0.9, 1.0, 0], [-0.1, 1.0, 0], buff=0, color=MAGENTA, stroke_width=7, tip_length=0.25)
        a2 = Arrow([5.4, 1.0, 0], [6.4, 1.0, 0], buff=0, color=MAGENTA, stroke_width=7, tip_length=0.25)
        self.play(FadeIn(a1), FadeIn(a2), run_time=0.6)
        self.at("freshly built")
        fl = label("fresh filament", GOLD_FRESH, 26, BOLD).move_to([0.8, -1.45, 0])
        fr = label("fresh filament", GOLD_FRESH, 26, BOLD).move_to([5.3, -1.45, 0])
        self.play(*[w.lat[i].animate.set_fill(GOLD_FRESH, 0.42).set_stroke(GOLD_FRESH) for i in (0, 1, 8, 9)],
                  FadeIn(fl), FadeIn(fr), run_time=0.7)
        self.play(w.lat[0].animate.shift(LEFT * 0.8).set_opacity(0), w.lat[9].animate.shift(RIGHT * 0.8).set_opacity(0),
                  run_time=0.9)
        self.play(w.lat[1].animate.shift(LEFT * 0.8).set_opacity(0), w.lat[8].animate.shift(RIGHT * 0.8).set_opacity(0),
                  run_time=0.9)
        self.at("Sequestration")
        br = bracket(-6.4, -1.0, -2.85, MAGENTA)
        bl = label("sequestration", MAGENTA, 32, BOLD).move_to([-3.7, -3.3, 0])
        self.play(Create(br), FadeIn(bl), run_time=0.8)
        self.at("not the whole")
        br2 = bracket(-6.4, 6.4, -2.85, MAGENTA)
        bl2 = label("more than sequestration", MAGENTA, 32, BOLD).move_to([0, -3.3, 0])
        self.play(Transform(br, br2), Transform(bl, bl2), run_time=1.2)
        self.finish()


class S05EndAndLattice(SpokenScene):
    def construct(self):
        dots = drifting_field(7, 26, 0.4, 1.0)
        w = actin_world(0.85)
        self.add(dots, w.pool, w.flow, w.lat, w.schem)
        e = ValueTracker(1)
        ends_lab = label("ends", TEXT, 32, BOLD).move_to([-5.5, 2.1, 0])
        ends_num = always_redraw(lambda: M(str(int(round(e.get_value()))), 70, MAGENTA).move_to([-3.5, 2.1, 0]))
        tot_lab = label("total actin", BLUE, 32, BOLD).move_to([-5.2, 0.8, 0])
        tot_bar = Rectangle(width=4.0, height=0.42, stroke_width=0, fill_color=BLUE, fill_opacity=0.5).move_to([-4.6, 0.15, 0])
        tot_frm = Rectangle(width=4.0, height=0.42, stroke_color=BLUE, stroke_width=2).move_to([-4.6, 0.15, 0])
        bind_lab = label("drug binding", MAGENTA, 32, BOLD).move_to([-4.9, -0.95, 0])
        bind_frm = Rectangle(width=4.0, height=0.42, stroke_color=MAGENTA, stroke_width=2).move_to([-4.6, -1.55, 0])

        def mkbind():
            wd = max(0.05, 0.8 * e.get_value())
            return Rectangle(width=wd, height=0.42, stroke_width=0, fill_color=MAGENTA, fill_opacity=0.7).move_to([-6.6 + wd / 2, -1.55, 0])
        bind_bar = always_redraw(mkbind)
        readouts = VGroup(ends_lab, ends_num, tot_lab, tot_bar, tot_frm, bind_lab, bind_frm, bind_bar)
        cb = label("cytochalasin B", MAGENTA, 32, BOLD).move_to([-1.0, 2.75, 0])
        self.play(FadeIn(cb, shift=DOWN * 0.1), run_time=0.7)

        s1 = bead_rows(1, [Y0], 0.9, 5.6, 0.62)
        s2 = bead_rows(2, [0.5, -0.9], 0.7, 5.6, 0.62)
        s5 = bead_rows(5, [1.5, 0.7, -0.1, -0.9, -1.7], 0.6, 5.6, 0.62)

        def marks(blocks, k):
            m = VGroup()
            for i in range(0, len(blocks), k):
                x, y = blocks[i].get_x(), blocks[i].get_y()
                m.add(Rectangle(width=0.1, height=0.55, stroke_width=0, fill_color=GREEN, fill_opacity=1).move_to([x - 0.4, y, 0]))
                m.add(Dot([x - 0.78, y, 0], radius=0.2, color=MAGENTA))
            return m
        m2, m5 = marks(s2[0], 5), marks(s5[0], 2)

        self.at("acts elsewhere")
        self.play(FadeOut(w.pool), FadeOut(w.flow), FadeIn(readouts), run_time=1.2)
        self.at("Its binding follows")
        self.play(Transform(w.lat, s2[0]), FadeIn(s2[1]), FadeIn(m2), e.animate.set_value(2), run_time=1.4)
        self.at("number")
        self.play(Transform(w.lat, s5[0]), Transform(s2[1], s5[1]), Transform(m2, m5), e.animate.set_value(5), run_time=1.4)
        self.at("not total actin")
        self.play(Indicate(VGroup(tot_bar, tot_frm), color=BLUE, scale_factor=1.05), run_time=0.8)
        self.at("it inhibits addition")
        gold = VGroup(*[subunit(0.8, y, GOLD_FRESH, w=0.4, h=0.45) for y in (1.5, 0.7, -0.1, -0.9, -1.7)])
        self.play(FadeIn(gold), run_time=0.3)
        self.play(gold.animate.shift(RIGHT * 2.3), run_time=1.1)
        self.at("at barbed ends")
        self.play(gold.animate.shift(LEFT * 1.6).set_opacity(0), run_time=0.9)
        self.at("instead binds")
        s1b = s1[0]
        loss = ValueTracker(1.0)
        loss_lab = label("loss rate", TEXT, 34, BOLD).move_to([-5.3, 0.8, 0])
        loss_frm = Rectangle(width=4.0, height=0.42, stroke_color=TEXT, stroke_width=2).move_to([-4.6, 0.15, 0])

        def mkloss():
            wd = max(0.05, 4.0 * loss.get_value())
            return Rectangle(width=wd, height=0.42, stroke_width=0, fill_color=TEXT, fill_opacity=0.6).move_to([-6.6 + wd / 2, 0.15, 0])
        loss_bar = always_redraw(mkloss)
        clips = VGroup()
        for i in range(0, 10, 2):
            x = 5.6 - 0.62 * (9 - i)
            clips.add(Rectangle(width=0.4, height=0.16, stroke_width=0, fill_color=MAGENTA, fill_opacity=0.95).move_to([x, Y0 + 0.52, 0]))
            clips.add(Rectangle(width=0.4, height=0.16, stroke_width=0, fill_color=MAGENTA, fill_opacity=0.95).move_to([x, Y0 - 0.52, 0]))
        cb2 = label("phalloidin", MAGENTA, 32, BOLD).move_to([-1.0, 2.75, 0])
        self.play(Transform(w.lat, s1b), FadeOut(s2[1]), FadeOut(m2), FadeOut(readouts), FadeOut(cb),
                  FadeIn(cb2), FadeIn(loss_lab), FadeIn(loss_frm), FadeIn(loss_bar), run_time=1.3)
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.15) for c in clips], lag_ratio=0.15), run_time=1.0)
        ghost = subunit(5.6, Y0, BLUE).set_opacity(0)
        ghost.phase = 0.0

        def gu(m, dt):
            m.phase += dt * loss.get_value() / 1.3
            f = m.phase % 1.0
            m.set_x(5.6 + 0.9 * f)
            m.set_fill(BLUE, opacity=0.42 * (1 - f))
            m.set_stroke(BLUE, opacity=1 - f)
        ghost.add_updater(gu)
        self.add(ghost)
        self.at("purified muscle actin")
        dish = RoundedRectangle(corner_radius=0.4, width=7.4, height=2.8, stroke_color=TEXT, stroke_width=3).move_to([2.75, Y0, 0])
        dl = label("purified muscle actin", TEXT, 30, BOLD).move_to([2.75, -2.15, 0])
        self.play(FadeIn(dish), FadeIn(dl), run_time=0.8)
        self.at("slows disassembly")
        self.play(loss.animate.set_value(0.25), run_time=1.4)
        self.finish()


def predict_parts():
    p = SimpleNamespace()
    p.title = label("polymer amount, schematic", TEXT, 32).move_to([0, 3.4, 0])
    p.frame = Rectangle(width=8.2, height=0.9, stroke_color=TEXT, stroke_width=3).move_to([0, 2.65, 0])
    p.blocks = VGroup(*[subunit(-3.51 + 0.78 * i, 2.65, BLUE, w=0.7, h=0.62) for i in range(10)])
    p.doors, p.qs, p.names = VGroup(), VGroup(), VGroup()
    for x, nm, col in zip((-4.4, 0.0, 4.4), ("subunits", "ends", "lattice"), (GOLD_FRESH, GREEN, BLUE)):
        p.doors.add(RoundedRectangle(corner_radius=0.2, width=3.4, height=3.0, stroke_color=MAGENTA, stroke_width=4,
                                     fill_color=MAGENTA, fill_opacity=0.07).move_to([x, -0.15, 0]))
        p.qs.add(label("?", MAGENTA, 96, BOLD).move_to([x, -0.2, 0]))
        p.names.add(label(nm, col, 34, BOLD).move_to([x, -2.1, 0]))
    p.question = label("Where did the drug act?", TEXT, 36, BOLD).move_to([0, -3.15, 0])
    return p


class S06Predict(SpokenScene):
    def construct(self):
        dots = drifting_field(8, 26, 0.4, 1.0)
        w = actin_world(0.85)
        p = predict_parts()
        self.add(dots, w.pool, w.flow, w.lat)
        self.at("Now predict")
        self.play(FadeOut(w.pool), FadeOut(w.flow), Transform(w.lat, p.blocks), FadeIn(p.frame), FadeIn(p.title), run_time=1.5)
        self.at("lowers the amount")
        self.play(LaggedStart(*[w.lat[i].animate.shift(RIGHT * 0.3).set_opacity(0) for i in range(9, 2, -1)], lag_ratio=0.15),
                  run_time=1.3)
        self.at("Does that observation")
        self.play(LaggedStart(*[FadeIn(VGroup(d, q, n)) for d, q, n in zip(p.doors, p.qs, p.names)], lag_ratio=0.3),
                  FadeIn(p.question), run_time=1.4)
        self.at("trapped subunits")
        self.play(Indicate(p.doors[0], color=MAGENTA, scale_factor=1.07), run_time=0.8)
        self.at("blocked ends")
        self.play(Indicate(p.doors[1], color=MAGENTA, scale_factor=1.07), run_time=0.8)
        self.at("changed the lattice")
        self.play(Indicate(p.doors[2], color=MAGENTA, scale_factor=1.07), run_time=0.8)
        self.finish()


class S07Think(NarratedScene):
    def construct(self):
        dots = drifting_field(8, 26, 0.4, 1.0)
        p = predict_parts()
        low = VGroup(*p.blocks[:3])
        self.add(dots, p.frame, p.title, low, p.doors, p.qs, p.names, p.question)
        for k, d in enumerate(p.doors):
            d.t = 0.0

            def f(m, dt, k=k):
                m.t += dt
                m.set_fill(MAGENTA, opacity=0.07 + 0.07 * (1 + np.sin(2.4 * m.t + k)) / 2)
            d.add_updater(f)
        for k, q in enumerate(p.qs):
            bob(q, ay=0.12, period=2.4, phase=k * 0.8)
        self.wait(4.5)


# ---------------------------------------------------------------- plots shared by scenes 8 and 9
PL1 = dict(x0=-6.2, x1=-0.9, y0=-0.55, y1=3.0)
PL2 = dict(x0=1.2, x1=6.5, y0=-0.55, y1=3.0)


def px(P, e):
    return P["x0"] + (P["x1"] - P["x0"]) * (e / 6.0)


def py_bind(P, e):
    return P["y0"] + (P["y1"] - P["y0"]) * (0.05 + 0.17 * e)


def py_flat(P, e):
    return P["y0"] + (P["y1"] - P["y0"]) * 0.62


def plot_frame(P):
    ax = VGroup(Line([P["x0"], P["y0"], 0], [P["x1"], P["y0"], 0]), Line([P["x0"], P["y0"], 0], [P["x0"], P["y1"], 0])).set_stroke(TEXT, 4)
    ticks = VGroup()
    for e in (1, 2, 5):
        ticks.add(Line([px(P, e), P["y0"] - 0.08, 0], [px(P, e), P["y0"] + 0.08, 0]).set_stroke(TEXT, 3))
        ticks.add(M(str(e), 24, TEXT).move_to([px(P, e), P["y0"] - 0.36, 0]))
    xl = label("end number", TEXT, 28).move_to([(P["x0"] + P["x1"]) / 2, P["y0"] - 0.78, 0])
    return VGroup(ax, ticks, xl)


def plot_title(P, text, color):
    return label(text, color, 34, BOLD).move_to([(P["x0"] + P["x1"]) / 2, 3.45, 0])


def pt(P, e, fn, color):
    return Dot([px(P, e), fn(P, e), 0], radius=0.14, color=color)


def strip_stage(k):
    ys = {1: [-2.65], 2: [-2.3, -3.0], 5: [-1.95, -2.3, -2.65, -3.0, -3.35]}[k]
    return bead_rows(k, ys, 0.26, 2.0, 0.3, bead_r=0.17)


class S08Measure(SpokenScene):
    def construct(self):
        dots = drifting_field(9, 26, 0.4, 1.0)
        p = predict_parts()
        low = VGroup(*p.blocks[:3])
        self.add(dots, p.frame, p.title, low, p.doors, p.qs, p.names, p.question)
        for q in p.qs:
            bob(q, ay=0.12, period=2.4)

        # the three doors open onto three mechanisms that all end in the same low bar
        def mech(i):
            x = (-4.4, 0.0, 4.4)[i]
            if i == 0:
                return VGroup(cup(x, -0.15)).scale(1.4)
            if i == 1:
                bl = VGroup(*[subunit(x - 0.2 + 0.5 * j, -0.15, BLUE, w=0.44, h=0.7) for j in range(3)])
                return VGroup(bl, Rectangle(width=0.2, height=0.95, stroke_width=0, fill_color=MAGENTA, fill_opacity=1).move_to([x - 0.55, -0.15, 0]))
            bl = VGroup(*[subunit(x - 0.5 + 0.5 * j, -0.15, BLUE, w=0.44, h=0.7) for j in range(3)])
            cl = VGroup(*[Rectangle(width=0.4, height=0.16, stroke_width=0, fill_color=MAGENTA, fill_opacity=1).move_to([x - 0.5 + 0.5 * j, -0.15 + s * 0.5, 0])
                          for j in range(3) for s in (1, -1)])
            return VGroup(bl, cl)
        mechs = [mech(i) for i in range(3)]
        arrows = VGroup(*[Arrow([x, 1.45, 0], [x * 0.55, 2.15, 0], buff=0, color=TEXT, stroke_width=6, tip_length=0.22)
                          for x in (-4.4, 0.0, 4.4)])
        self.at("Now")
        self.play(FadeOut(p.qs), LaggedStart(*[FadeIn(m, scale=0.8) for m in mechs], lag_ratio=0.3),
                  FadeIn(arrows), run_time=1.5)
        self.at("Add a second")
        self.play(FadeOut(VGroup(p.doors, p.names, p.question, arrows, p.frame, p.title, low, *mechs)), run_time=0.7)
        f1, f2 = plot_frame(PL1), plot_frame(PL2)
        t1, t2 = plot_title(PL1, "drug binding", MAGENTA), plot_title(PL2, "total actin", BLUE)
        sch = label("schematic", TEXT, 24).set_opacity(0.8).move_to([5.3, -3.45, 0])
        self.play(Create(f1), Create(f2), FadeIn(t1), FadeIn(t2), FadeIn(sch), run_time=1.2)
        d1 = [pt(PL1, e, py_bind, MAGENTA) for e in (1, 2, 5)]
        d2 = [pt(PL2, e, py_flat, BLUE) for e in (1, 2, 5)]
        s1, s2, s5 = strip_stage(1), strip_stage(2), strip_stage(5)
        strip = s1[0].copy()
        sbead = s1[1].copy()
        self.at("Holding total actin")
        self.play(FadeIn(strip), FadeIn(sbead), FadeIn(d1[0]), FadeIn(d2[0]), run_time=0.9)
        self.at("constant")
        flat = Line([px(PL2, 1), py_flat(PL2, 1), 0], [px(PL2, 5), py_flat(PL2, 5), 0]).set_stroke(BLUE, 6)
        self.play(Create(flat), run_time=0.8)
        self.at("changing end")
        self.play(Transform(strip, s2[0]), Transform(sbead, s2[1]), FadeIn(d1[1]), FadeIn(d2[1]), run_time=1.0)
        self.at("can reveal")
        self.play(Transform(strip, s5[0]), Transform(sbead, s5[1]), FadeIn(d1[2]), FadeIn(d2[2]), run_time=1.0)
        self.at("binding that follows")
        line1 = Line([px(PL1, 1), py_bind(PL1, 1), 0], [px(PL1, 5), py_bind(PL1, 5), 0]).set_stroke(MAGENTA, 6)
        self.play(Create(line1), run_time=1.0)
        self.play(Indicate(VGroup(*d1), color=MAGENTA, scale_factor=1.2), run_time=0.8)
        self.finish()


class S09Inference(SpokenScene):
    def construct(self):
        dots = drifting_field(10, 26, 0.4, 1.0)
        f1, f2 = plot_frame(PL1), plot_frame(PL2)
        t1, t2 = plot_title(PL1, "drug binding", MAGENTA), plot_title(PL2, "total actin", BLUE)
        sch = label("schematic", TEXT, 24).set_opacity(0.8).move_to([5.3, -3.45, 0])
        d1 = VGroup(*[pt(PL1, e, py_bind, MAGENTA) for e in (1, 2, 5)])
        d2 = VGroup(*[pt(PL2, e, py_flat, BLUE) for e in (1, 2, 5)])
        flat = Line([px(PL2, 1), py_flat(PL2, 1), 0], [px(PL2, 5), py_flat(PL2, 5), 0]).set_stroke(BLUE, 6)
        line1 = Line([px(PL1, 1), py_bind(PL1, 1), 0], [px(PL1, 5), py_bind(PL1, 5), 0]).set_stroke(MAGENTA, 6)
        s5 = strip_stage(5)
        for b in s5[1]:
            b.set_opacity(0.5)
        plot1 = VGroup(f1, d1, line1, t1)
        plot2 = VGroup(f2, d2, flat, t2)
        self.add(dots, plot1, plot2, s5[0], s5[1], sch)
        # shrink the second plot and the beads away, bring the binding plot down into its box
        mech_box = RoundedRectangle(corner_radius=0.25, width=7.2, height=6.9, stroke_color=TEXT, stroke_width=3).move_to([-3.0, 0.1, 0])
        mech_ttl = label("mechanism test", TEXT, 32, BOLD).move_to([-3.0, 3.15, 0])
        eff_box = RoundedRectangle(corner_radius=0.25, width=5.6, height=6.9, stroke_color=TEXT, stroke_width=3).move_to([3.8, 0.1, 0])
        eff_ttl = label("effect: less polymer", TEXT, 32, BOLD).move_to([3.8, 3.1, 0])
        bar_f = Rectangle(width=4.6, height=1.0, stroke_color=TEXT, stroke_width=3).move_to([3.8, 0.9, 0])
        bar_b = VGroup(*[subunit(1.9 + 0.44 * i, 0.9, BLUE, w=0.4, h=0.8) for i in range(3)])
        self.play(FadeOut(plot2), FadeOut(s5[0]), FadeOut(s5[1]), plot1.animate.shift(DOWN * 1.0), run_time=1.2)
        self.at("effect")
        self.play(FadeIn(eff_box), FadeIn(eff_ttl), FadeIn(bar_f), FadeIn(bar_b), run_time=1.0)
        self.at("mechanism")
        self.play(FadeIn(mech_box), FadeIn(mech_ttl), run_time=0.9)
        self.at("Polymer amount")
        self.play(Indicate(VGroup(bar_f, bar_b), color=TEXT, scale_factor=1.06), run_time=0.9)
        self.at("A measurement tied")
        c1 = chip("end number", TEXT, 24).move_to([-4.9, -2.95, 0])
        c2 = chip("binding", MAGENTA, 24).move_to([-1.7, -2.95, 0])
        ar1 = Arrow([-3.7, -2.95, 0], [-2.8, -2.95, 0], buff=0, color=TEXT, stroke_width=6, tip_length=0.22)
        ar2 = Arrow([-0.9, -2.95, 0], [1.0, -2.95, 0], buff=0, color=TEXT, stroke_width=6, tip_length=0.22)
        self.play(FadeIn(c1), Create(ar1), run_time=0.7)
        self.play(FadeIn(c2), Create(ar2), run_time=0.8)
        self.at("proposed target")
        ring = SurroundingRectangle(d1, color=MAGENTA, buff=0.2, stroke_width=5)
        alts = VGroup(chip("free pool", TEXT, 26).move_to([3.8, -1.2, 0]), chip("lattice", TEXT, 26).move_to([3.8, -2.1, 0]))
        self.play(Create(ring), FadeIn(alts), run_time=0.9)
        self.play(alts.animate.set_opacity(0.25), run_time=0.8)
        self.at("how that outcome")
        self.play(Indicate(ar2, color=MAGENTA, scale_factor=1.2), Indicate(bar_f, color=TEXT, scale_factor=1.04), run_time=1.0)
        self.finish()


class S10Dose(SpokenScene):
    def construct(self):
        dots = drifting_field(11, 24, 0.4, 1.0)
        nb, amp, dose = ValueTracker(13.0), ValueTracker(1.6), ValueTracker(0.0)
        mt_cols = VGroup()
        for i in range(16):
            mt_cols.add(VGroup(*[subunit(-5.3 + 0.5 * i, y, BLUE, w=0.44, h=0.42) for y in (2.35, 1.85, 1.35, 0.85)]))
        seed = RoundedRectangle(corner_radius=0.12, width=0.5, height=2.2, stroke_color=GREY, fill_color=GREY, fill_opacity=0.45).move_to([-5.85, 1.6, 0])
        mt_cols.t = 0.0

        def mtup(m, dt):
            m.t += dt
            nv = nb.get_value() + amp.get_value() * np.sin(1.2 * m.t)
            for i, c in enumerate(m):
                a = max(0.0, min(1.0, nv - i))
                col = GOLD_FRESH if i >= nv - 2 else BLUE
                for b in c:
                    b.set_fill(col, opacity=0.42 * a)
                    b.set_stroke(col, opacity=a)
        mt_cols.add_updater(mtup)
        mt_lab = label("microtubule, schematic", TEXT, 28).move_to([-2.6, 3.3, 0])
        # growth and shortening arrows
        gl = ValueTracker(1.4)
        g_lab = label("growth", TEXT, 28).move_to([-4.6, 0.0, 0])
        s_lab = label("shortening", TEXT, 28).move_to([-4.3, -0.6, 0])
        g_arr = always_redraw(lambda: Arrow([-3.1, 0.0, 0], [-3.1 + gl.get_value(), 0.0, 0], buff=0, color=TEXT, stroke_width=7, tip_length=0.22))
        s_arr = always_redraw(lambda: Arrow([-3.1 + gl.get_value(), -0.6, 0], [-3.1, -0.6, 0], buff=0, color=TEXT, stroke_width=7, tip_length=0.22))
        # dose gauge
        gf = Rectangle(width=7.5, height=0.42, stroke_color=MAGENTA, stroke_width=3).move_to([-1.75, -1.75, 0])

        def mkd():
            wd = max(0.02, 7.5 * dose.get_value())
            return Rectangle(width=wd, height=0.42, stroke_width=0, fill_color=MAGENTA, fill_opacity=0.65).move_to([-5.5 + wd / 2, -1.75, 0])
        gfill = always_redraw(mkd)
        glab = label("nocodazole dose", MAGENTA, 30, BOLD).move_to([-3.9, -1.15, 0])
        # cultured cell
        cell = Circle(radius=1.85, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.04).move_to([4.55, 0.9, 0])
        clab = label("cultured cells", TEXT, 28).move_to([4.55, 3.2, 0])
        rays = VGroup()
        rng = np.random.RandomState(3)
        for k in range(9):
            ang = 2 * PI * k / 9 + 0.2
            ln = rng.uniform(1.15, 1.6)
            rays.add(Line([4.55, 0.9, 0], [4.55 + ln * np.cos(ang), 0.9 + ln * np.sin(ang), 0]).set_stroke(BLUE, 5))
        rays.thr = [0.15 + 0.07 * k for k in range(9)]
        rays.add_updater(lambda m, dt: [r.set_stroke(BLUE, 5, opacity=1.0 if dose.get_value() < 0.2 else
                                                     float(np.clip(1.0 - (dose.get_value() - 0.2 - 0.05 * k) / 0.5, 0.0, 1.0)))
                                        for k, r in enumerate(m)])
        sch = label("schematic", TEXT, 24).set_opacity(0.8).move_to([5.6, -3.45, 0])
        self.add(dots, seed, mt_cols, mt_lab, sch)
        self.play(FadeIn(g_lab), FadeIn(s_lab), FadeIn(g_arr), FadeIn(s_arr), run_time=1.0)
        self.at("Dose changes")
        self.play(FadeIn(gf), FadeIn(gfill), FadeIn(glab), run_time=0.8)
        self.at("In tested cultured cells")
        self.play(FadeIn(cell), FadeIn(rays), FadeIn(clab), run_time=0.9)
        ticks = VGroup(*[Line([-5.5 + 7.5 * d, -1.98, 0], [-5.5 + 7.5 * d, -1.52, 0]).set_stroke(TEXT, 3) for d in (0.12, 0.4, 0.65, 0.9)])
        nano = label("nanomolar", MAGENTA, 30, BOLD).move_to([-4.6, -2.45, 0])
        micro = label("micromolar", MAGENTA, 30, BOLD).move_to([0.8, -2.45, 0])
        out1 = label("paused, slower", TEXT, 28).move_to([-4.6, -3.15, 0])
        out2 = label("most microtubules gone", TEXT, 28).move_to([0.2, -3.15, 0])
        self.at("nanomolar nocodazole")
        self.play(dose.animate.set_value(0.12), FadeIn(nano), run_time=1.0)
        self.at("can pause")
        self.play(amp.animate.set_value(0.35), gl.animate.set_value(0.6), run_time=1.2)
        self.at("and slow growth")
        self.play(Indicate(VGroup(g_arr, s_arr), color=TEXT, scale_factor=1.1), run_time=0.8)
        self.at("shortening")
        self.play(FadeIn(out1, shift=UP * 0.1), run_time=0.6)
        self.at("Micromolar doses")
        self.play(FadeIn(micro), run_time=0.5)
        self.add(ticks)
        for d in (0.4, 0.65, 0.9):
            self.play(dose.animate.set_value(d), run_time=0.9)
        self.play(nb.animate.set_value(3.5), amp.animate.set_value(0.3), run_time=2.0)
        self.at("remove most")
        self.play(FadeIn(out2, shift=UP * 0.1), run_time=0.6)
        self.finish()


class Dish(VGroup):
    pass


def mt_dish(cx, rate, seed):
    """A dish with five identical microtubules growing slowly and collapsing quickly."""
    rng = np.random.RandomState(seed)
    g = VGroup()
    circle = Circle(radius=1.75, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.05).move_to([cx, 0, 0])
    g.add(circle)
    lines, tips = [], []
    for k in range(5):
        ang = 2 * PI * k / 5 + 0.4
        l = Line([cx, 0, 0], [cx + 0.3 * np.cos(ang), 0.3 * np.sin(ang), 0]).set_stroke(BLUE, 6)
        t = Dot([cx, 0, 0], radius=0.1, color=GOLD_FRESH)
        lines.append((l, ang))
        tips.append(t)
        g.add(l, t)
    g.fr = [0.19 * k for k in range(5)]
    g.prev = list(g.fr)
    g.count = ValueTracker(0)
    g.rate = rate

    def up(m, dt):
        for k, (l, ang) in enumerate(lines):
            m.prev[k] = m.fr[k]
            m.fr[k] = (m.fr[k] + dt * m.rate.get_value()) % 1.0
            if m.prev[k] < 0.8 <= m.fr[k]:
                m.count.set_value(m.count.get_value() + 1)
            f = m.fr[k]
            ln = 0.3 + 1.3 * (f / 0.8 if f < 0.8 else 1 - (f - 0.8) / 0.2)
            end = np.array([cx + ln * np.cos(ang), ln * np.sin(ang), 0])
            l.put_start_and_end_on(np.array([cx, 0, 0]), end)
            tips[k].move_to(end)
    g.add_updater(up)
    return g


class S11System(SpokenScene):
    def construct(self):
        dots = drifting_field(12, 24, 0.35, 1.0)
        rl, rr = ValueTracker(0.22), ValueTracker(0.22)
        dl, dr = mt_dish(-4.35, rl, 1), mt_dish(4.35, rr, 2)
        cl = always_redraw(lambda: M(f"catastrophes: {int(dl.count.get_value())}", 28, RED).move_to([-4.35, -2.4, 0]))
        cr = always_redraw(lambda: M(f"catastrophes: {int(dr.count.get_value())}", 28, RED).move_to([4.35, -2.4, 0]))
        sch = label("schematic", TEXT, 24).set_opacity(0.8).move_to([0, -3.45, 0])
        chp = chip("nocodazole", MAGENTA, 34).move_to([0, 2.3, 0])
        self.add(dots)
        self.play(FadeIn(dl), FadeIn(dr), FadeIn(cl), FadeIn(cr), FadeIn(sch), run_time=1.2)
        self.at("With nocodazole")
        self.play(FadeIn(chp, shift=DOWN * 0.4), run_time=0.8)
        self.at("catastrophe became more")
        arl = Arrow([-0.3, 1.9, 0], [-1.2, 1.0, 0], buff=0, color=MAGENTA, stroke_width=6, tip_length=0.22)
        txl = label("more\ncatastrophes", RED, 26, BOLD).move_to([-1.15, 0.35, 0])
        self.play(rl.animate.set_value(0.8), Create(arl), FadeIn(txl), run_time=1.0)
        self.play(Indicate(txl, color=RED, scale_factor=1.12), run_time=0.8)
        self.at("newt lung")
        nl = label("newt lung cells", TEXT, 30, BOLD).move_to([-4.35, 2.6, 0])
        self.play(FadeIn(nl, shift=DOWN * 0.1), run_time=0.5)
        self.at("In BSC-1")
        nr = label("BSC-1 cells, 1 hour", TEXT, 30, BOLD).move_to([4.35, 2.6, 0])
        self.play(FadeIn(nr, shift=DOWN * 0.1), run_time=0.6)
        self.at("catastrophe became less")
        arr = Arrow([0.3, 1.9, 0], [1.2, 1.0, 0], buff=0, color=MAGENTA, stroke_width=6, tip_length=0.22)
        txr = label("fewer\ncatastrophes", RED, 26, BOLD).move_to([1.15, 0.35, 0])
        self.play(rr.animate.set_value(0.07), Create(arr), FadeIn(txr), run_time=1.0)
        self.play(Indicate(txr, color=RED, scale_factor=1.12), run_time=0.8)
        self.finish()


class S12PhalloidinBoundary(SpokenScene):
    def construct(self):
        dots = drifting_field(13, 24, 0.35, 1.0)
        loss_l, loss_r = ValueTracker(1.0), ValueTracker(1.0)

        def fil(x0, n=7):
            return VGroup(*[subunit(x0 + 0.7 * i, 0.0, BLUE, w=0.62, h=0.85) for i in range(n)])

        def leaver(xend, loss):
            gh = subunit(xend, 0.0, BLUE, w=0.62, h=0.85).set_opacity(0)
            gh.phase = 0.0

            def gu(m, dt):
                m.phase += dt * loss.get_value() / 1.3
                f = m.phase % 1.0
                m.set_x(xend + 0.9 * f)
                m.set_fill(BLUE, opacity=0.42 * (1 - f))
                m.set_stroke(BLUE, opacity=1 - f)
            gh.add_updater(gu)
            return gh

        dish = RoundedRectangle(corner_radius=0.4, width=6.0, height=4.2, stroke_color=TEXT, stroke_width=3).move_to([-3.4, 0, 0])
        fl = fil(-5.4)
        cell = Ellipse(width=5.8, height=4.2, stroke_color=TEXT, stroke_width=5, fill_color=TEXT, fill_opacity=0.04).move_to([3.55, 0, 0])
        fr = fil(1.0)
        lab_l = label("purified muscle actin", TEXT, 30, BOLD).move_to([-3.4, 2.55, 0])
        lab_r = label("living cell", TEXT, 30, BOLD).move_to([3.55, 2.55, 0])
        sch = label("schematic", TEXT, 24).set_opacity(0.8).move_to([0, -3.45, 0])
        ghl, ghr = leaver(-1.2, loss_l), leaver(5.2, loss_r)
        self.add(dots)
        self.at("shows another system")
        self.play(FadeIn(dish), FadeIn(fl), FadeIn(cell), FadeIn(fr), FadeIn(lab_l), FadeIn(lab_r), FadeIn(sch), run_time=1.2)
        self.add(ghl, ghr)
        self.at("It slows")
        clips = VGroup()
        for i in range(0, 7, 2):
            for s in (1, -1):
                clips.add(Rectangle(width=0.5, height=0.18, stroke_width=0, fill_color=MAGENTA, fill_opacity=0.95).move_to([-5.4 + 0.7 * i, s * 0.52, 0]))
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.1) for c in clips], lag_ratio=0.15), run_time=1.0)
        self.play(loss_l.animate.set_value(0.12), run_time=1.0)
        self.at("but enters living")
        out = VGroup(*[Rectangle(width=0.4, height=0.16, stroke_width=0, fill_color=MAGENTA, fill_opacity=0.95).move_to([-0.1 + 0.15 * (i % 2), 1.4 - 0.55 * i, 0])
                       for i in range(6)])
        self.play(FadeIn(out), run_time=0.5)
        self.play(*[c.animate.move_to([0.45 + 0.06 * (i % 2), 1.4 - 0.55 * i, 0]) for i, c in enumerate(out)], run_time=1.4)
        self.play(Indicate(out, color=MAGENTA, scale_factor=1.15), run_time=0.8)
        self.at("Fluorescent")
        fixed = Ellipse(width=8.0, height=4.4, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.12).move_to([0, 0.1, 0])
        ffil = VGroup(*[subunit(-3.6 + 0.6 * i, 0.1, BLUE, w=0.54, h=0.8) for i in range(13)])
        self.play(FadeOut(VGroup(dish, fl, cell, fr, lab_l, lab_r, clips, out, ghl, ghr)), FadeIn(fixed), FadeIn(ffil), run_time=1.2)
        self.at("stains filaments")
        glow = VGroup(*[Rectangle(width=0.5, height=0.18, stroke_width=0, fill_color=MAGENTA, fill_opacity=1).move_to([-3.6 + 0.6 * i, 0.1 + s * 0.55, 0])
                        for i in range(0, 13) for s in (1, -1)])
        self.play(LaggedStart(*[FadeIn(g) for g in glow], lag_ratio=0.03), run_time=1.4)
        self.at("after cells are fixed")
        fl_lab = label("fixed-cell stain", MAGENTA, 36, BOLD).move_to([0, 2.95, 0])
        self.play(FadeIn(fl_lab, shift=DOWN * 0.1), Indicate(glow, color=MAGENTA, scale_factor=1.1), run_time=1.0)
        self.finish()


def rope_pts(g, x0=-4.6, x1=4.6, y_off=0.0, n=50, amp=0.9, kind="spread"):
    xs = np.linspace(x0, x1, n)
    spread = np.stack([xs, y_off + amp * np.sin(1.3 * xs) - 0.1, np.zeros(n)], 1)
    gath = np.stack([-2.1 + 0.3 * np.sin(1.9 * xs), -0.2 + 1.5 * (xs / 4.6) + 0.3 * y_off, np.zeros(n)], 1)
    return (1 - g) * spread + g * gath


class S13CleanerTest(SpokenScene):
    def construct(self):
        dots = drifting_field(14, 22, 0.3, 1.0)
        gv = ValueTracker(0.0)
        cell = Ellipse(width=12.4, height=5.8, stroke_color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=0.04).move_to([0.1, 0, 0])
        nuc = Circle(radius=0.95, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.12).move_to([-3.6, -0.2, 0])

        def mk_rope():
            m = VMobject().set_stroke(GREY, 14)
            m.set_points_smoothly(rope_pts(gv.get_value()))
            return m
        rope = always_redraw(mk_rope)

        def mk_other(off):
            def f():
                m = VMobject().set_stroke(BLUE, 5)
                m.set_points_smoothly(rope_pts(0.45 * gv.get_value(), -4.2, 4.2, off, amp=0.4))
                return m
            return always_redraw(f)
        others = VGroup(mk_other(1.1), mk_other(-1.2), mk_other(-1.9))
        vlab = label("vimentin", TEXT, 34, BOLD).move_to([4.4, 3.4, 0])
        flab = label("human fibroblast", TEXT, 28).move_to([-4.0, 3.4, 0])
        sch = label("schematic", TEXT, 24).set_opacity(0.8).move_to([5.3, -3.45, 0])
        self.add(dots)
        self.play(FadeIn(cell), FadeIn(nuc), FadeIn(rope), FadeIn(others), FadeIn(vlab), FadeIn(flab), FadeIn(sch), run_time=1.5)
        self.at("With Afrin")
        chp = chip("withaferin A", MAGENTA, 28).move_to([0, 4.6, 0])
        self.play(chp.animate.move_to([0.2, 3.3, 0]), run_time=1.0)
        self.at("redistributes vimentin")
        self.play(gv.animate.set_value(1.0), run_time=2.2)
        warn = chip("not selective", RED, 28).move_to([1.0, -2.3, 0])
        self.play(FadeIn(warn, shift=UP * 0.1), run_time=0.6)
        self.at("did not alter")
        self.play(FadeOut(VGroup(cell, nuc, rope, others, vlab, flab, chp, warn)), run_time=0.7)
        top = label("purified vimentin", TEXT, 34, BOLD).move_to([0, 3.25, 0])
        dA = RoundedRectangle(corner_radius=0.3, width=5.8, height=3.4, stroke_color=TEXT, stroke_width=3).move_to([-3.4, 0.2, 0])
        dB = RoundedRectangle(corner_radius=0.3, width=5.8, height=3.4, stroke_color=TEXT, stroke_width=3).move_to([3.4, 0.2, 0])
        lA = label("no drug", TEXT, 30, BOLD).move_to([-3.4, -2.0, 0])
        lB = label("with withaferin A", MAGENTA, 30, BOLD).move_to([3.4, -2.0, 0])
        cB = chip("withaferin A", MAGENTA, 26).move_to([3.4, 1.2, 0])
        av = ValueTracker(0.02)

        def mk_assem(cx):
            def f():
                a = max(0.02, av.get_value())
                xs = np.linspace(cx - 2.3, cx - 2.3 + 4.6 * a, 30)
                pts = np.stack([xs, 0.2 + 0.4 * np.sin(2.0 * xs), np.zeros(30)], 1)
                m = VMobject().set_stroke(GREY, 14)
                m.set_points_smoothly(pts)
                return m
            return always_redraw(f)
        self.play(FadeIn(top), FadeIn(dA), FadeIn(dB), FadeIn(lA), FadeIn(lB), FadeIn(cB), run_time=0.8)
        asm = VGroup(mk_assem(-3.4), mk_assem(3.4))
        self.add(asm)
        self.play(av.animate.set_value(1.0), run_time=2.6, rate_func=linear)
        self.at("Removing vimentin genetically")
        self.play(FadeOut(VGroup(top, dA, dB, lA, lB, cB, asm)), run_time=0.7)
        cA = Ellipse(width=5.6, height=4.0, stroke_color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=0.04).move_to([-3.4, 0.0, 0])
        cBb = Ellipse(width=5.6, height=4.0, stroke_color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=0.04).move_to([3.4, 0.0, 0])
        nA = Circle(radius=0.6, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.12).move_to([-4.3, 0.0, 0])
        nB = Circle(radius=0.6, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.12).move_to([2.5, 0.0, 0])
        tA = label("no vimentin", TEXT, 30, BOLD).move_to([-3.4, 2.5, 0])
        tB = label("no vimentin", TEXT, 30, BOLD).move_to([3.4, 2.5, 0])
        self.play(FadeIn(cA), FadeIn(cBb), FadeIn(nA), FadeIn(nB), FadeIn(tA), FadeIn(tB), run_time=1.0)
        self.at("then adding it back")
        blk = chip("vimentin add-back", MAGENTA, 28).move_to([3.4, -3.5, 0])
        self.play(FadeIn(blk, shift=UP * 0.2), blk.animate.move_to([3.4, -2.75, 0]), run_time=0.6)
        rb = VMobject().set_stroke(GREY, 14)
        pts_full = np.stack([np.linspace(3.4 - 1.0, 3.4 + 2.0, 30), 0.0 + 0.5 * np.sin(np.linspace(0, 9, 30)), np.zeros(30)], 1)
        rb.set_points_smoothly(pts_full)
        self.play(Create(rb), Transform(tB, label("vimentin back", TEXT, 30, BOLD).move_to([3.4, 2.5, 0])), run_time=0.9)
        self.at("cleaner test")
        ck = VGroup(Line([-0.5, 3.1, 0], [-0.1, 2.6, 0]), Line([-0.1, 2.6, 0], [0.7, 3.5, 0])).set_stroke(GREEN, 14)
        self.play(Create(ck), run_time=0.8)
        self.finish()


class S14ReadResult(SpokenScene):
    def construct(self):
        dots = drifting_field(15, 24, 0.35, 1.0)
        xs = (-4.95, -1.65, 1.65, 4.95)
        e = ValueTracker(2)

        def card(cy):
            frm = RoundedRectangle(corner_radius=0.3, width=13.0, height=2.9, stroke_color=TEXT, stroke_width=3,
                                   fill_color=TEXT, fill_opacity=0.04).move_to([0, cy, 0])
            txt = [label("this target", TEXT, 28, BOLD), label("at this dose", TEXT, 28, BOLD),
                   label("in this system", TEXT, 28, BOLD), label("changed this\nmeasurement", TEXT, 28, BOLD)]
            for t, x in zip(txt, xs):
                t.move_to([x, cy - 0.85, 0])
            return frm, txt

        f1, t1 = card(1.3)
        f2, t2 = card(-2.0)

        def icons(cy, addback=False):
            i1 = (chip("add-back", MAGENTA, 24) if addback else icon("target")).move_to([xs[0], cy + 0.4, 0])
            i2 = icon("dose").move_to([xs[1], cy + 0.4, 0])
            i3 = icon("system").move_to([xs[2], cy + 0.4, 0])
            return [i1, i2, i3]
        ic1 = icons(1.3)
        ic2 = icons(-2.0, True)
        cnt1 = always_redraw(lambda: M(f"ends {int(round(e.get_value()))}", 34, MAGENTA).move_to([xs[3], 1.7, 0]))
        cnt2 = always_redraw(lambda: M(f"ends {int(round(e.get_value()))}", 34, MAGENTA).move_to([xs[3], -1.45, 0]))
        self.add(dots)
        self.play(FadeIn(f1), run_time=0.8)
        self.at("This target")
        self.play(FadeIn(ic1[0], shift=DOWN * 0.3), FadeIn(t1[0]), run_time=0.6)
        self.at("at this dose")
        self.play(FadeIn(ic1[1], shift=DOWN * 0.3), FadeIn(t1[1]), run_time=0.6)
        self.at("in this system")
        self.play(FadeIn(ic1[2], shift=DOWN * 0.3), FadeIn(t1[2]), run_time=0.6)
        self.at("changed this")
        self.play(FadeIn(cnt1), FadeIn(t1[3]), e.animate.set_value(5), run_time=1.2)
        self.at("compare another")
        self.play(FadeIn(f2), *[FadeIn(i) for i in ic2], *[FadeIn(t) for t in t2], FadeIn(cnt2), run_time=1.2)
        self.at("aimed at")
        self.play(Indicate(ic2[0], color=MAGENTA, scale_factor=1.25), Indicate(ic1[0], color=MAGENTA, scale_factor=1.25), run_time=1.0)
        self.finish()


class S15Return(SpokenScene):
    def construct(self):
        dots = drifting_field(16, 28, 0.4, 1.0)
        w = hook_world()
        self.add(dots, w.all)
        tags = [tag("target", "target", w=3.4, h=1.0, size=32).move_to([-3.7, 0.55, 0]),
                tag("dose", "dose", w=3.4, h=1.0, size=32).move_to([0.0, 0.55, 0]),
                tag("system", "system", w=3.4, h=1.0, size=32).move_to([3.7, 0.55, 0])]
        drug = chip("drug", MAGENTA, 34).move_to([-5.2, -1.2, 0])
        links = [always_redraw(lambda t=t: Line(drug.get_top(), t.get_bottom(), color=MAGENTA, stroke_width=5)) for t in tags]
        oarr = Arrow([3.2, -1.2, 0], [4.9, -1.2, 0], buff=0, color=TEXT, stroke_width=8)
        olab = label("outcome", TEXT, 28).move_to([6.0, -1.2, 0])
        self.at("This chapter adds")
        self.play(FadeIn(drug), *[FadeIn(t, shift=DOWN * 0.2) for t in tags], *[FadeIn(l) for l in links], run_time=0.6)
        self.play(drug.animate.move_to([-0.05, -1.25, 0]), FadeIn(oarr), FadeIn(olab), run_time=0.9)
        self.at("rule for testing")
        frame = RoundedRectangle(corner_radius=0.25, width=11.6, height=1.8, stroke_color=MAGENTA, stroke_width=5).move_to([0, 0.55, 0])
        self.play(Create(frame), run_time=0.9)
        self.at("If target")
        newgauge = icon("dose").move_to(tags[1].icon.get_center())
        newgauge[1].stretch_to_fit_height(0.75).align_to(newgauge[0], DOWN).shift(UP * 0.05)
        self.play(Transform(tags[1].icon, newgauge), Rotate(oarr, 0.45, about_point=oarr.get_start()), run_time=1.0)
        self.at("or system")
        newdish = Circle(radius=0.3, stroke_color=TEXT, stroke_width=3).move_to(tags[2].icon.get_center())
        self.play(Transform(tags[2].icon, newdish), Rotate(oarr, -0.9, about_point=oarr.get_start()), run_time=1.0)
        self.at("the conclusion may")
        self.play(Rotate(oarr, 0.5, about_point=oarr.get_start()), Indicate(frame, color=MAGENTA, scale_factor=1.03), run_time=1.0)
        self.finish()


class S16End(EndCard):
    LINE = "A drug tests mechanism only with target, dose, and system."
