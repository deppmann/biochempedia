"""Water pays for order -- Biochemistrypedia explainer (lesson: water-weak-bonds).

COLOR MAP (kept for the whole video):
  BLUE   = water (capsule = one water molecule drawn as a dipole cartoon, never a structure)
  RED    = charged / polar things water loves (ions, lipid heads)
  YELLOW = nonpolar / greasy things water rejects (nonpolar blobs, lipid tails)
  GREEN  = entropy / freedom
  GREY   = structure, silhouettes, de-emphasised labels
No molecular structures are drawn: only labelled blobs, dipole capsules, dots and icons.
"""
import json
import math
import pathlib
import random

from bp_style import *  # noqa: F401,F403

HERE = pathlib.Path(__file__).parent
NARR = {s["id"]: s.get("narration", "") for s in json.load(open(HERE / "script.json"))["scenes"]}


class Base(NarratedScene):
    SID = None

    def cue(self, phrase, lead=0.0):
        """Wait until the narration reaches `phrase` (estimated from character position)."""
        txt = NARR[self.SID]
        i = txt.find(phrase)
        assert i >= 0, phrase
        target = i / len(txt) * self.narration_s - lead
        dt = target - self.elapsed()
        if dt > 0.02:
            self.wait(dt)


# ---------------------------------------------------------------- shared pieces
def water(pos=ORIGIN, ang=0.0, s=1.0, op=1.0):
    """One water molecule as a dipole capsule: filled dot = negative pole (left), hollow = positive (right)."""
    body = RoundedRectangle(corner_radius=0.15 * s, width=0.62 * s, height=0.30 * s, stroke_color=BLUE,
                            stroke_width=2.2, fill_color=BLUE, fill_opacity=0.22)
    neg = Dot(body.get_left() + RIGHT * 0.12 * s, radius=0.065 * s, color=BLUE)
    plus = Circle(radius=0.055 * s, stroke_color=BLUE, stroke_width=2).move_to(body.get_right() + LEFT * 0.12 * s)
    g = VGroup(body, neg, plus)
    g.rotate(ang).move_to(pos)
    g.ang = ang
    if op < 1:
        g.set_opacity(op)
    return g


def jiggle(m, amp=0.05, seed=0, spin=0.5):
    """Thermal wobble that composes with animations (applies position deltas, not absolute positions)."""
    r = random.Random(seed)
    ph = [r.uniform(0, 6.28) for _ in range(4)]
    fr = [r.uniform(1.5, 3.0) for _ in range(2)]
    m.jt = 0.0
    m.joff = np.zeros(3)
    m.jspin = r.uniform(-spin, spin)

    def upd(mob, dt):
        mob.jt += dt
        t = mob.jt
        new = np.array([amp * math.sin(fr[0] * t + ph[0]), amp * math.sin(fr[1] * t + ph[1]), 0.0])
        mob.shift(new - mob.joff)
        mob.joff = new
        mob.rotate(mob.jspin * dt)
        mob.ang += mob.jspin * dt

    m.add_updater(upd)
    return m


def unjiggle(m):
    m.clear_updaters()
    m.shift(-m.joff)
    m.joff = np.zeros(3)
    return m


def lipid(p, a, tails=2, L=0.4, hr=0.16, sw=4):
    """Lipid cartoon: red head dot at p; yellow tail line(s) pointing opposite to direction angle a.
    A schematic icon (head + tail lines), not a structure."""
    d = np.array([math.cos(a), math.sin(a), 0.0])
    n = np.array([-d[1], d[0], 0.0])
    p = np.array([p[0], p[1], 0.0])
    head = Circle(radius=hr, stroke_color=RED, stroke_width=2, fill_color=RED, fill_opacity=0.9).move_to(p)
    offs = [0.0] if tails == 1 else [-hr / 2, hr / 2]
    lines = []
    for o in offs:
        s0 = p - d * hr + n * o
        lines.append(Line(s0, s0 - d * L, color=YELLOW, stroke_width=sw))
    return VGroup(head, *lines)


def dim_tag(tag, on):
    o = 1.0 if on else 0.28
    return [tag[0].animate.set_stroke(opacity=o).set_fill(opacity=0.16 * o), tag[1].animate.set_opacity(o)]


def poisson(n, box, min_d, avoid=(), avoid_r=0.0, seed=1, existing=()):
    """Rejection-sample n points in box=(x0,x1,y0,y1) at least min_d apart and avoid_r from `avoid` points."""
    r = random.Random(seed)
    pts = list(existing)
    n += len(pts)
    tries = 0
    md = min_d
    while len(pts) < n:
        tries += 1
        if tries % 4000 == 0:
            md *= 0.93
        p = np.array([r.uniform(box[0], box[1]), r.uniform(box[2], box[3]), 0.0])
        if any(np.linalg.norm(p - a) < avoid_r for a in avoid):
            continue
        if any(np.linalg.norm(p - q) < md for q in pts):
            continue
        pts.append(p)
    return pts[len(existing):]


# ---------------------------------------------------------------- cards
class S00Title(TitleCard):
    LESSON = "Water & weak bonds"
    TITLE = "Water Pays for Order"


class S05End(EndCard):
    LINE = "Water's freedom pays for life's order."


# ---------------------------------------------------------------- s01: three jobs
def network(center, cols, rows, dx=1.0, dy=0.82, seed=2, jig=True):
    """A patch of water capsules with dashed hydrogen-bond links between neighbours."""
    r = random.Random(seed)
    caps, pos = [], []
    for j in range(rows):
        for i in range(cols):
            x = (i - (cols - 1) / 2) * dx + (0.5 * dx * 0.5 if j % 2 else -0.5 * dx * 0.5)
            y = (j - (rows - 1) / 2) * dy
            c = water(center + np.array([x, y, 0]), r.uniform(-0.9, 0.9))
            caps.append(c)
            pos.append(c.get_center())
    links = VGroup()
    for a in range(len(caps)):
        for b in range(a + 1, len(caps)):
            if np.linalg.norm(pos[a] - pos[b]) < dx * 1.12:
                ca, cb = caps[a], caps[b]
                links.add(always_redraw(lambda ca=ca, cb=cb: DashedLine(
                    ca.get_center(), cb.get_center(), color=BLUE, stroke_width=2.2, dash_length=0.07, dashed_ratio=0.5
                ).set_opacity(0.8)))
    if jig:
        for k, c in enumerate(caps):
            jiggle(c, amp=0.035, seed=seed * 100 + k, spin=0.25)
    return VGroup(*caps), links


class S01ThreeJobs(Base):
    SID = "s01_three_jobs"

    def construct(self):
        tags = VGroup(chip("1  Cohesion", BLUE, 26), chip("2  Dissolves ions", RED, 26),
                      chip("3  Rejects nonpolar", YELLOW, 26)).arrange(RIGHT, buff=0.3).to_edge(UP, buff=0.45)
        for t in tags:
            t[0].set_stroke(opacity=0.28).set_fill(opacity=0.045)
            t[1].set_opacity(0.28)
        sc = ORIGIN + DOWN * 0.45

        # intro: one polar water molecule
        big = water(sc + UP * 0.1, 0, s=5.0)
        lab = T("water is polar", 44).next_to(big, DOWN, buff=0.7)
        l_neg = T("negative end", 28, GREY).next_to(big, LEFT, buff=0.35)
        l_pos = T("positive end", 28, GREY).next_to(big, RIGHT, buff=0.35)
        self.play(FadeIn(big, scale=0.6), run_time=0.6)
        self.play(FadeIn(l_neg, shift=RIGHT * 0.1), FadeIn(l_pos, shift=LEFT * 0.1), Write(lab), run_time=0.9)
        self.cue("three jobs", lead=0.1)
        self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.15) for t in tags], lag_ratio=0.25), run_time=1.3)

        # job 1: cohesion
        self.cue("First,")
        self.play(FadeOut(VGroup(big, lab, l_neg, l_pos)), *dim_tag(tags[0], True), run_time=0.6)
        caps, links = network(sc + UP * 0.1, 6, 4, dx=1.25, dy=0.95)
        self.play(LaggedStart(*[FadeIn(c, scale=0.5) for c in caps], lag_ratio=0.05), run_time=1.1)
        self.cue("network of hydrogen", lead=0.2)
        self.add(links)
        self.play(LaggedStart(*[Create(l) for l in links], lag_ratio=0.04), run_time=1.5)
        hb = T("hydrogen bonds", 30, BLUE).move_to(sc + DOWN * 2.45)
        self.play(FadeIn(hb, shift=UP * 0.1), run_time=0.6)

        # job 2: dissolves charged things
        self.cue("Second,")
        for l in links:
            l.clear_updaters()
        self.play(FadeOut(caps), FadeOut(links), FadeOut(hb), *dim_tag(tags[0], False), *dim_tag(tags[1], True),
                  run_time=0.6)
        self.remove(links)
        ion_c = sc + UP * 0.1
        ion = VGroup(Circle(radius=0.5, stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.3),
                     T("Na⁺", 34, RED)).move_to(ion_c)
        self.play(GrowFromCenter(ion), run_time=0.5)
        shell = []
        for k in range(8):
            th = k * TAU / 8 + 0.2
            tgt = ion_c + 1.55 * np.array([math.cos(th), math.sin(th), 0])
            start = ion_c + 3.6 * np.array([math.cos(th), math.sin(th) * 0.9, 0])
            start[1] = np.clip(start[1], -3.0 - 0.0, 2.3)
            start[0] = np.clip(start[0], -6.0, 6.0)
            c = water(start, th + 0.9 * (k % 2 - 0.5) + 0.3, s=1.35)
            c.target_pos, c.target_ang = tgt, th
            shell.append(c)
        self.play(*[FadeIn(c) for c in shell], run_time=0.4)
        anims = []
        for c in shell:
            anims.append(c.animate.move_to(c.target_pos))
        self.play(LaggedStart(*anims, lag_ratio=0.1), run_time=1.5)
        # orient: negative pole (left end) turns toward the cation
        self.play(*[c.animate.rotate(c.target_ang - c.ang) for c in shell], run_time=0.9)
        for c in shell:
            c.ang = c.target_ang
        ring = DashedVMobject(Circle(radius=2.1, color=BLUE, stroke_width=3).move_to(ion_c), num_dashes=40)
        hs = T("hydration shell", 32, BLUE).move_to(sc + DOWN * 2.6)
        self.cue("hydration shell", lead=0.3)
        self.play(Create(ring), FadeIn(hs, shift=UP * 0.1), run_time=0.8)

        # job 3: rejects nonpolar
        self.cue("Third,")
        self.play(FadeOut(VGroup(ion, ring, hs, *shell)), *dim_tag(tags[1], False), *dim_tag(tags[2], True),
                  run_time=0.6)
        caps3, links3 = network(sc + np.array([1.9, 0.1, 0]), 5, 4, dx=1.25, dy=0.95, seed=5)
        blob = VGroup(RoundedRectangle(corner_radius=0.5, width=2.3, height=1.3, stroke_color=YELLOW,
                                       stroke_width=3, fill_color=YELLOW, fill_opacity=0.25),
                      T("nonpolar", 28, YELLOW)).move_to(sc + np.array([-4.3, 0.1, 0]))
        self.play(FadeIn(caps3), FadeIn(blob), run_time=0.7)
        self.add(links3)
        self.play(LaggedStart(*[Create(l) for l in links3], lag_ratio=0.03), run_time=0.9)
        self.cue("rejects nonpolar", lead=0.6)
        self.play(blob.animate.shift(RIGHT * 2.1), run_time=1.2, rate_func=smooth)
        arrows = VGroup(*[Arrow(sc + np.array([-0.45, y, 0]), sc + np.array([-1.35, y, 0]), buff=0, color=BLUE,
                                stroke_width=7, max_tip_length_to_length_ratio=0.5)
                          for y in (0.85, 0.1, -0.65)])
        self.play(FadeIn(arrows), blob.animate.shift(LEFT * 1.3), run_time=1.0, rate_func=rush_from)
        self.cue("hydrophobic effect", lead=0.8)
        eff = T("the hydrophobic effect", 34).move_to(sc + DOWN * 2.55)
        self.play(FadeIn(eff, shift=UP * 0.1), run_time=0.8)

        # close
        self.cue("Water is never")
        for l in links3:
            l.clear_updaters()
        self.play(FadeOut(VGroup(caps3, blob, arrows, eff)), FadeOut(links3),
                  *dim_tag(tags[0], True), *dim_tag(tags[1], True), *dim_tag(tags[2], True), run_time=0.8)
        self.remove(links3)
        solv = T("just the solvent", 44, GREY, font=TITLE_FONT).move_to(sc + UP * 0.2)
        x_s = Line(solv.get_left() + LEFT * 0.15, solv.get_right() + RIGHT * 0.15, color=TEXT, stroke_width=5)
        self.play(FadeIn(solv), run_time=0.5)
        self.play(Create(x_s), run_time=0.4)
        act = T("an active player", 52, font=TITLE_FONT).move_to(sc + UP * 0.2)
        self.cue("active player", lead=0.6)
        self.play(FadeOut(VGroup(solv, x_s), shift=UP * 0.3), run_time=0.3)
        self.play(FadeIn(act, shift=UP * 0.2), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------- s02: entropy
class S02Entropy(Base):
    SID = "s02_entropy"

    def construct(self):
        # A: entropy, not attraction
        hdr = T("the hydrophobic effect", 48, font=TITLE_FONT).move_to(UP * 2.0)
        by = T("driven by", 40)
        ent = chip("entropy", GREEN, 52, pad=0.3)
        nb = T("not by", 40, GREY)
        att = chip("attraction", GREY, 44, pad=0.28)
        row = VGroup(by, ent, nb, att).arrange(RIGHT, buff=0.35).move_to(DOWN * 0.3)
        self.play(Write(hdr), run_time=1.2)
        self.cue("driven by")
        self.play(FadeIn(by), run_time=0.6)
        self.cue("entropy,")
        self.play(GrowFromCenter(ent), run_time=0.8)
        self.cue("not by attraction")
        self.play(FadeIn(nb), FadeIn(att), run_time=0.5)
        strike = Line(att.get_left() + LEFT * 0.1, att.get_right() + RIGHT * 0.1, color=TEXT, stroke_width=5)
        self.play(Create(strike), run_time=0.4)
        self.cue("The second law", lead=0.3)
        self.play(FadeOut(VGroup(row, strike, hdr)), run_time=0.4)

        # B: second law -- order to disorder
        r = random.Random(11)
        sq = VGroup(*[Square(0.34, stroke_color=GREEN, stroke_width=2.5, fill_color=GREEN, fill_opacity=0.25)
                      for _ in range(20)]).arrange_in_grid(4, 5, buff=0.16).move_to(UP * 0.1)
        lab = T("the second law: disorder grows", 34, GREEN).move_to(DOWN * 2.5)
        self.play(FadeIn(sq, lag_ratio=0.03), run_time=0.5)
        tg = poisson(20, (-3.6, 3.6, -1.5, 1.8), 0.8, seed=4)
        self.play(FadeIn(lab, shift=UP * 0.1),
                  *[s.animate.move_to(p).rotate(r.uniform(-1.2, 1.2)) for s, p in zip(sq, tg)],
                  run_time=1.6, rate_func=smooth)
        self.cue("When nonpolar", lead=0.2)
        self.play(FadeOut(VGroup(sq, lab)), run_time=0.4)

        # C: caged water around lone nonpolar blobs
        cbox = np.array([-1.9, -0.25, 0])
        box = Rectangle(width=8.6, height=4.5, stroke_color=BLUE, stroke_width=2.5, fill_color=BLUE,
                        fill_opacity=0.05).move_to(cbox)
        bpos = [np.array(p + (0,)) for p in [(-4.2, 0.65), (-0.9, 0.7), (-4.0, -1.3), (-0.8, -1.3)]]
        blobs = VGroup(*[Circle(radius=0.32, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW,
                                fill_opacity=0.5).move_to(p) for p in bpos])
        cage, ringpos = [], []
        rr = random.Random(7)
        for b_i, bp in enumerate(bpos):
            for k in range(8):
                th = k * TAU / 8
                rp = bp + 0.78 * np.array([math.cos(th), math.sin(th), 0])
                ringpos.append((rp, th + PI / 2))
                jp = bp + (0.85 + rr.uniform(0, 0.45)) * np.array([math.cos(th + rr.uniform(-.25, .25)),
                                                                     math.sin(th + rr.uniform(-.25, .25)), 0])
                c = water(jp, rr.uniform(0, TAU))
                cage.append(c)
        freep = poisson(22, (-6.0, 2.2, -2.3, 1.8), 0.78, avoid=bpos + [cbox], avoid_r=1.55, seed=9)
        free = [water(p, rr.uniform(0, TAU)) for p in freep]
        for k, c in enumerate(cage + free):
            jiggle(c, amp=0.07 if c in cage else 0.05, seed=k, spin=0.7)
        # legend + entropy bar
        lg1 = VGroup(Circle(radius=0.14, stroke_color=YELLOW, fill_color=YELLOW, fill_opacity=0.5, stroke_width=3),
                     T("nonpolar", 24, YELLOW)).arrange(RIGHT, buff=0.2)
        lg2 = VGroup(water(ORIGIN, 0, 0.8), T("water", 24, BLUE)).arrange(RIGHT, buff=0.2)
        lg = VGroup(lg2, lg1).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(np.array([4.55, 1.7, 0]))
        base_y, hmax, bx = -2.45, 3.4, 4.55
        level = ValueTracker(0.6)
        bar = always_redraw(lambda: Rectangle(width=1.0, height=max(0.05, hmax * level.get_value()),
                                              stroke_color=GREEN, stroke_width=2.5, fill_color=GREEN, fill_opacity=0.45)
                            .move_to(np.array([bx, base_y, 0]), aligned_edge=DOWN))
        axis = Line(np.array([bx - 0.8, base_y, 0]), np.array([bx + 0.8, base_y, 0]), color=GREY, stroke_width=3)
        blab = T("water's entropy", 26, GREEN).move_to(np.array([bx, -2.9, 0]))
        head = T("lone nonpolar groups: water is caged", 32, BLUE).move_to(UP * 3.0 + LEFT * 1.9)
        self.play(FadeIn(box), FadeIn(blobs), FadeIn(VGroup(*free)), FadeIn(VGroup(*cage)), FadeIn(lg),
                  run_time=1.2)
        self.add(bar)
        self.play(FadeIn(axis), FadeIn(blab), FadeIn(head), run_time=0.8)
        self.cue("freeze into ordered cages")
        for c in cage:
            unjiggle(c)
        self.play(LaggedStart(*[c.animate.move_to(rp).rotate(((ang - c.ang + PI / 2) % PI) - PI / 2)
                                for c, (rp, ang) in zip(cage, ringpos)], lag_ratio=0.02),
                  level.animate.set_value(0.28), run_time=1.8)
        for c, (rp, ang) in zip(cage, ringpos):
            c.ang = ang
        self.cue("low entropy", lead=0.3)
        low = T("low entropy", 28, GREEN).move_to(np.array([bx, base_y + hmax * 0.28 + 0.4, 0]))
        self.play(FadeIn(low, shift=DOWN * 0.1), run_time=0.6)

        # D: cluster the blobs, release the water
        self.cue("Cluster the nonpolar")
        self.play(FadeOut(low), FadeOut(head), run_time=0.3)
        cl = [cbox + np.array(d + (0,)) for d in [(-0.34, 0.34), (0.34, 0.34), (-0.34, -0.34), (0.34, -0.34)]]
        NH = 10
        hull = []
        for k in range(NH):
            th = k * TAU / NH
            hull.append((cbox + 1.17 * np.array([math.cos(th), math.sin(th), 0]), th + PI / 2))
        relp = poisson(len(cage) - NH, (-6.0, 2.2, -2.3, 1.8), 0.78, avoid=[cbox], avoid_r=1.9, seed=21,
                       existing=freep)
        mv = [b.animate.move_to(p) for b, p in zip(blobs, cl)]
        # the NH cage capsules nearest the cluster centre form the hull; the rest are released
        order = sorted(range(len(cage)), key=lambda k: np.linalg.norm(cage[k].get_center() - cbox))
        hull_ids = set(order[:NH])
        cm, hi, ri = [], 0, 0
        for k, c in enumerate(cage):
            unjiggle(c) if hasattr(c, "joff") else None
            if k in hull_ids:
                hp, ha = hull[hi]
                hi += 1
                cm.append(c.animate.move_to(hp).rotate(((ha - c.ang + PI / 2) % PI) - PI / 2))
                c.ang_t = ha
            else:
                cm.append(c.animate.move_to(relp[ri]))
                ri += 1
        newhead = T("clustered: caged water is released", 32, GREEN).move_to(UP * 3.0 + LEFT * 1.9)
        self.play(*mv, *cm, level.animate.set_value(0.85), run_time=3.0, rate_func=smooth)
        for k, c in enumerate(cage):
            if k in hull_ids:
                c.ang = c.ang_t
            else:
                jiggle(c, amp=0.06, seed=100 + k, spin=0.7)
        high = T("high entropy", 28, GREEN).move_to(np.array([bx, base_y + hmax * 0.85 + 0.4, 0]))
        self.play(FadeIn(newhead, shift=DOWN * 0.1), FadeIn(high, shift=UP * 0.1), run_time=0.6)

        # E: consequences
        self.cue("The molecules huddle")
        push = VGroup(*[Arrow(cbox + 2.0 * np.array([math.cos(a), math.sin(a), 0]),
                              cbox + 1.35 * np.array([math.cos(a), math.sin(a), 0]), buff=0, color=GREEN,
                              stroke_width=7, max_tip_length_to_length_ratio=0.5)
                        for a in [0.0, PI / 2, PI, 3 * PI / 2]])
        newhead2 = T("water gains disorder by pushing them together", 30, GREEN).move_to(UP * 3.0 + LEFT * 1.9)
        self.play(FadeOut(newhead), run_time=0.3)
        self.play(FadeIn(push, lag_ratio=0.2), FadeIn(newhead2, shift=DOWN * 0.1), run_time=1.0)
        c1 = chip("protein folding", GREEN, 28)
        c2 = chip("membrane assembly", GREEN, 28)
        outs = VGroup(c1, c2).arrange(RIGHT, buff=0.4).move_to(np.array([-1.9, -3.05, 0]))
        self.cue("that drives", lead=0.2)
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.6)
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------- s03: dance floor
class S03DanceFloor(Base):
    SID = "s03_dance_floor"

    def construct(self):
        fl_c = np.array([0.0, -0.3, 0.0])
        X0, X1, Y0, Y1 = -5.2, 5.2, -2.8, 2.2
        floor = Rectangle(width=10.4, height=5.0, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                          fill_opacity=0.06).move_to(fl_c)
        rng = random.Random(5)
        N = 44
        pts = poisson(N, (X0 + 0.3, X1 - 0.3, Y0 + 0.3, Y1 - 0.3), 0.6, seed=3)
        dancers = []
        for p in pts:
            d = Dot(p, radius=0.15, color=BLUE)
            d.slot = None          # callable -> target position while "caged"
            d.goal = None          # open-floor point a newly freed dancer heads for
            d.hd = rng.uniform(0, TAU)
            dancers.append(d)
        wf_pos = [np.array(p + (0,)) for p in [(-3.6, 1.0), (-0.6, 1.2), (2.6, 0.4), (-1.9, -1.2), (3.4, -1.7)]]
        wf = [Circle(radius=0.3, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.5)
              .move_to(p) for p in wf_pos]
        state = {"wf_on": False}
        dg = VGroup(*dancers)

        def upd(g, dt):
            wfc = [w.get_center() for w in wf] if state["wf_on"] else []
            # soft personal space between free dancers, so the crowd spreads over whatever floor it has
            P = np.array([d.get_center() for d in dancers])
            push = np.zeros_like(P)
            for i in range(len(dancers)):
                if dancers[i].slot is not None:
                    continue
                dv = P[i] - P
                dist = np.linalg.norm(dv, axis=1)
                m = (dist > 1e-6) & (dist < 0.75)
                if m.any():
                    push[i] = (dv[m] / dist[m, None] * (0.75 - dist[m, None])).sum(axis=0)
            for d, pv in zip(dancers, push):
                if d.slot is None:
                    d.shift(pv * min(1.0, 2.5 * dt))
            for d in dancers:
                c = d.get_center()
                if d.slot is not None:
                    tgt = d.slot()
                    d.move_to(c + (tgt - c) * min(1.0, 3.5 * dt))
                    continue
                if d.goal is not None:
                    v = d.goal - c
                    dist = np.linalg.norm(v)
                    if dist < 0.12:
                        d.goal = None
                    else:
                        d.move_to(c + v / dist * min(dist, 2.6 * dt))
                        d.hd = math.atan2(v[1], v[0])
                        continue
                d.hd += rng.uniform(-6, 6) * dt
                n = c + dt * 1.2 * np.array([math.cos(d.hd), math.sin(d.hd), 0])
                if n[0] < X0 + 0.2 or n[0] > X1 - 0.2:
                    d.hd = PI - d.hd
                    n = c
                if n[1] < Y0 + 0.2 or n[1] > Y1 - 0.2:
                    d.hd = -d.hd
                    n = c
                n[0] = min(max(n[0], X0 + 0.2), X1 - 0.2)
                n[1] = min(max(n[1], Y0 + 0.2), Y1 - 0.2)
                for w in wfc:                      # navigate around the wallflowers
                    dd = np.linalg.norm(n - w)
                    if dd < 0.62:
                        n = w + (n - w) / max(dd, 1e-3) * 0.62
                        d.hd += 1.5
                d.move_to(n)

        def set_bound(d, on):
            if on:
                d.set_fill(BLUE, opacity=0.2).set_stroke(BLUE, width=2.5, opacity=1)
            else:
                d.set_fill(BLUE, opacity=1).set_stroke(width=0)

        dg.add_updater(upd)
        counter = always_redraw(lambda: M(f"free dancers  {sum(1 for d in dancers if d.slot is None):2d} / {N}", 32,
                                          GREEN).move_to(UP * 3.15))
        lg = VGroup(VGroup(Dot(radius=0.13, color=BLUE), T("dancers = water", 26, BLUE)).arrange(RIGHT, buff=0.2),
                    VGroup(Circle(radius=0.17, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW,
                                  fill_opacity=0.5), T("wallflowers = nonpolar molecules", 26, YELLOW))
                    .arrange(RIGHT, buff=0.2)).arrange(RIGHT, buff=0.7).move_to(DOWN * 3.3)
        lg[1].set_opacity(0)

        title = T("a crowded dance floor", 38).move_to(UP * 3.1)
        self.play(FadeIn(floor), FadeIn(title), run_time=0.8)
        self.add(dg)
        self.play(FadeIn(dg), FadeIn(lg[0]), run_time=1.0)
        self.wait(0.3)

        # wallflowers appear; dancers have to steer around them
        self.cue("Scattered wallflowers")
        self.play(FadeOut(title), run_time=0.4)
        self.add(counter)
        state["wf_on"] = True
        self.play(LaggedStart(*[GrowFromCenter(w) for w in wf], lag_ratio=0.2), lg[1].animate.set_opacity(1),
                  run_time=1.6)

        # the water locks into cages: the 6 nearest dancers bind to each wallflower
        self.cue("and the surrounding water locks")
        taken = set()
        for wi, w in enumerate(wf):
            wc = w.get_center()
            near = sorted([d for d in dancers if id(d) not in taken], key=lambda d: np.linalg.norm(d.get_center() - wc))[:6]
            a0 = rng.uniform(0, TAU)
            for k, d in enumerate(near):
                taken.add(id(d))
                ang = a0 + k * TAU / 6
                d.slot = (lambda w=w, ang=ang: w.get_center() + 0.68 * np.array([math.cos(ang), math.sin(ang), 0]))
                set_bound(d, True)
        cage_lbl = T("water locks into cages", 28, BLUE).move_to(DOWN * 3.3)
        self.play(FadeOut(lg), run_time=0.4)
        self.play(FadeIn(cage_lbl), run_time=0.5)

        # push wallflowers into a corner: only a few cages are left
        self.cue("Push the wallflowers")
        cl = [np.array(p + (0,)) for p in [(-3.82, -1.65), (-3.18, -1.65), (-3.82, -1.0), (-3.18, -1.0), (-3.5, -0.38)]]
        state["wf_on"] = False      # the wallflowers slide through; they do not sweep the crowd
        self.play(*[w.animate.move_to(p) for w, p in zip(wf, cl)], run_time=2.6, rate_func=smooth)
        state["wf_on"] = True
        ctr = np.mean(cl, axis=0)
        keep = [d for d in dancers if d.slot is not None]
        keep = sorted(keep, key=lambda d: np.linalg.norm(d.get_center() - ctr))
        freed = keep[8:]
        goals = poisson(len(freed), (X0 + 0.4, X1 - 0.4, Y0 + 0.4, Y1 - 0.4), 0.9, avoid=[ctr], avoid_r=2.4,
                        seed=17, existing=[d.get_center() for d in dancers if d.slot is None])
        goals.sort(key=lambda g: g[0])
        freed.sort(key=lambda d: d.get_center()[0])
        for k, d in enumerate(keep):
            if k < 8:
                ang = k * TAU / 8 + 0.3
                d.slot = (lambda ang=ang: ctr + np.array([math.cos(ang) * 1.1, math.sin(ang) * 1.42, 0]))
        for d, g in zip(freed, goals):
            d.slot = None
            d.goal = g
            set_bound(d, False)
        self.cue("and the dancers, the water")
        free_lbl = T("water is free to move", 28, GREEN).move_to(DOWN * 3.3)
        self.play(FadeOut(cage_lbl), FadeIn(free_lbl), run_time=0.6)

        # not attraction
        self.cue("The force isn't")
        att = chip("attraction", GREY, 28).move_to(DOWN * 3.3)
        x_att = Line(att.get_left() + LEFT * 0.1, att.get_right() + RIGHT * 0.1, color=TEXT, stroke_width=5)
        self.play(FadeOut(free_lbl), run_time=0.3)
        self.play(FadeIn(att), run_time=0.4)
        self.cue("attraction between", lead=-0.2)
        self.play(Create(x_att), run_time=0.4)
        self.cue("It's the system", lead=0.2)
        self.play(FadeOut(VGroup(att, x_att)), run_time=0.3)
        arrs = VGroup(*[Arrow(np.array(a + (0,)), np.array(b + (0,)), buff=0, color=BLUE, stroke_width=8,
                              max_tip_length_to_length_ratio=0.35)
                        for a, b in [((0.2, -2.2), (-1.8, -2.0)), ((0.3, -0.4), (-1.7, -1.0)),
                                     ((-0.8, 1.0), (-2.3, -0.1))]])
        ptxt = T("pushed together by the water's freedom", 30, GREEN).move_to(DOWN * 3.3)
        self.play(FadeIn(arrs, lag_ratio=0.25), FadeIn(ptxt, shift=UP * 0.1), run_time=1.4)
        self.finish()


# ---------------------------------------------------------------- s04: membranes
class S04Membranes(Base):
    SID = "s04_membranes"

    def construct(self):
        # A: same entropy
        ent = chip("water's entropy", GREEN, 40, pad=0.3).move_to(UP * 1.4)
        c1 = chip("protein folding", GREEN, 32).move_to(np.array([-3.6, -1.4, 0]))
        c2 = chip("membranes", GREEN, 32).move_to(np.array([3.6, -1.4, 0]))
        a1 = Arrow(ent.get_bottom() + LEFT * 0.4, c1.get_top(), buff=0.15, color=GREEN, stroke_width=6)
        a2 = Arrow(ent.get_bottom() + RIGHT * 0.4, c2.get_top(), buff=0.15, color=GREEN, stroke_width=6)
        self.play(FadeIn(ent, shift=DOWN * 0.1), run_time=0.6)
        self.play(GrowArrow(a1), FadeIn(c1), run_time=0.8)
        self.cue("builds your membranes")
        self.play(GrowArrow(a2), FadeIn(c2), run_time=0.8)
        self.cue("A phospholipid", lead=0.3)
        self.play(FadeOut(VGroup(ent, c1, c2, a1, a2)), run_time=0.5)

        # B: two greasy tails
        big = lipid(np.array([0.0, 0.9, 0]), PI / 2, 2, L=1.5, hr=0.45, sw=9)
        hd = T("polar head", 32, RED).next_to(big[0], RIGHT, buff=0.5)
        tl = T("two greasy tails", 32, YELLOW).move_to(np.array([2.9, -0.4, 0]))
        self.play(GrowFromCenter(big[0]), FadeIn(hd, shift=LEFT * 0.1), run_time=0.6)
        self.cue("two greasy", lead=0.2)
        self.play(Create(big[1]), Create(big[2]), FadeIn(tl, shift=LEFT * 0.1), run_time=0.7)
        # water molecules approach the tails and veer away
        drops = VGroup(*[water(np.array([x, y, 0]), 0.4, 0.8) for x, y in [(-2.8, -0.4), (-2.7, -1.3), (2.9, -1.5)]])
        wt = T("water won't wet them", 32, BLUE).move_to(DOWN * 2.8)
        self.cue("water won't wet", lead=0.3)
        self.play(FadeIn(drops), FadeIn(wt, shift=UP * 0.1), run_time=0.4)
        self.play(drops[0].animate.shift(RIGHT * 0.8), drops[1].animate.shift(RIGHT * 0.8),
                  drops[2].animate.shift(LEFT * 0.8), run_time=0.6)
        self.play(drops[0].animate.shift(LEFT * 0.6 + UP * 0.2), drops[1].animate.shift(LEFT * 0.6 + DOWN * 0.2),
                  drops[2].animate.shift(RIGHT * 0.6 + DOWN * 0.2), run_time=0.6)

        mc = np.array([0.0, -0.1, 0])

        def ring_member(th, tails, R, hr, L, sw, w_in, r_in, op=0.12):
            """One lipid icon on a ring (head out, tails in) plus its grey shape silhouette."""
            u = np.array([math.cos(th), math.sin(th), 0])
            n = np.array([-u[1], u[0], 0])
            pb = mc + (R - hr * 0.2) * u
            pe = mc + r_in * u
            if w_in == 0:
                sil = Polygon(pb + n * hr, pb - n * hr, pe, stroke_color=GREY, stroke_width=1.5,
                              fill_color=GREY, fill_opacity=0.12)
            else:
                sil = Polygon(pb + n * hr, pb - n * hr, pe - n * w_in, pe + n * w_in, stroke_color=GREY,
                              stroke_width=1.5, fill_color=GREY, fill_opacity=op)
            return VGroup(sil, lipid(mc + R * u, th, tails, L=L, hr=hr, sw=sw))

        # C: cone -> micelle (the single icon becomes the top member of the micelle)
        self.cue("A single-tailed", lead=0.2)
        self.play(FadeOut(VGroup(big, hd, tl, drops, wt)), run_time=0.4)
        one = lipid(np.array([0.0, 1.1, 0]), PI / 2, 1, L=1.5, hr=0.45, sw=9)
        cone = Polygon(np.array([-0.45, 1.1, 0]), np.array([0.45, 1.1, 0]), np.array([0.0, -0.85, 0]),
                       stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.12)
        cl = T("cone shape", 34, GREY).move_to(np.array([2.8, 0.2, 0]))
        self.play(FadeIn(one), FadeIn(cone), run_time=0.7)
        self.cue("cone-shaped", lead=0.2)
        self.play(FadeIn(cl, shift=LEFT * 0.1), cone.animate.set_fill(opacity=0.3), run_time=0.5)
        self.cue("packs into a sphere", lead=0.3)
        NM = 16
        mgrp = [ring_member(PI / 2 + k * TAU / NM, 1, 1.9, 0.3, 0.95, 6, 0, 0.6) for k in range(NM)]
        self.play(Transform(VGroup(cone, one), mgrp[0]), FadeOut(cl), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(g, scale=0.5) for g in mgrp[1:]], lag_ratio=0.06), run_time=1.0)
        ml = T("micelle", 40, TEXT).move_to(np.array([4.0, -0.1, 0]))
        self.play(FadeIn(ml, shift=LEFT * 0.1), run_time=0.4)

        # D: cylinder: same trick, but the shapes cannot close a sphere
        self.cue("But a bulky", lead=0.2)
        self.play(FadeOut(VGroup(cone, one, *mgrp[1:], ml)), run_time=0.4)
        two = lipid(np.array([0.0, 1.1, 0]), PI / 2, 2, L=1.5, hr=0.45, sw=9)
        cyl = Rectangle(width=0.9, height=2.4, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                        fill_opacity=0.12).move_to(np.array([0.0, 0.35, 0]))
        cll = T("cylinder shape", 34, GREY).move_to(np.array([3.0, 0.3, 0]))
        self.play(FadeIn(two), FadeIn(cyl), run_time=0.7)
        self.cue("cylindrical", lead=0.3)
        self.play(FadeIn(cll, shift=LEFT * 0.1), cyl.animate.set_fill(opacity=0.3), run_time=0.5)
        self.cue("so it can't form", lead=0.4)
        NC = 12
        # same head size and ring as the micelle, but parallel sides: the tails pile into the core
        rgrp = [ring_member(PI / 2 + k * TAU / NC, 2, 1.9, 0.3, 1.35, 6, 0.3, 0.2, op=0.2) for k in range(NC)]
        self.play(Transform(VGroup(cyl, two), rgrp[0]), FadeOut(cll), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(g, scale=0.5) for g in rgrp[1:]], lag_ratio=0.06), run_time=0.9)
        core = DashedVMobject(Circle(radius=0.62, stroke_color=TEXT, stroke_width=4).move_to(mc), num_dashes=18)
        nt = T("tails collide: no tidy sphere", 34, TEXT).move_to(np.array([0.0, -2.9, 0]))
        self.play(Create(core), FadeIn(nt, shift=UP * 0.1), run_time=0.5)

        # E: sheet tail to tail
        self.cue("instead it lines up", lead=0.1)
        self.play(FadeOut(VGroup(cyl, two, *rgrp[1:], core, nt)), run_time=0.4)
        L = 0.35
        wt_top = Rectangle(width=11.6, height=1.4, stroke_width=0, fill_color=BLUE, fill_opacity=0.14)\
            .move_to(np.array([0, 1.9, 0]))
        wt_bot = Rectangle(width=11.6, height=1.4, stroke_width=0, fill_color=BLUE, fill_opacity=0.14)\
            .move_to(np.array([0, -1.9, 0]))
        wl1 = T("water", 28, BLUE).move_to(wt_top)
        wl2 = T("water", 28, BLUE).move_to(wt_bot)
        NL = 18
        row_x = [(-4.675 + 0.55 * i) for i in range(NL)]
        top = [lipid(np.array([x, 0.6, 0]), PI / 2, 2, L=L) for x in row_x]
        bot = [lipid(np.array([x, -0.6, 0]), -PI / 2, 2, L=L) for x in row_x]
        self.play(FadeIn(wt_top), FadeIn(wt_bot), FadeIn(wl1), FadeIn(wl2),
                  LaggedStart(*[FadeIn(i, shift=DOWN * 0.3) for i in top], lag_ratio=0.04), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(i, shift=UP * 0.3) for i in bot], lag_ratio=0.04), run_time=1.0)
        sheet_lbl = T("tails meet tails; heads face the water", 32, YELLOW).move_to(np.array([0, -3.1, 0]))
        self.play(FadeIn(sheet_lbl), run_time=0.4)

        # F: sheet closes into a bilayer vesicle
        self.cue("and that sheet closes", lead=0.2)
        vc = np.array([0.0, -0.2, 0])
        outer_t = [lipid(vc + 2.1 * np.array([math.cos(k * TAU / NL + PI / 2), math.sin(k * TAU / NL + PI / 2), 0]),
                         k * TAU / NL + PI / 2, 2, L=L) for k in range(NL)]
        # inner leaflet: heads face the water inside, so each icon points toward the centre
        inner_t = [lipid(vc + 1.1 * np.array([math.cos(k * TAU / NL + PI / 2), math.sin(k * TAU / NL + PI / 2), 0]),
                         k * TAU / NL + PI / 2 + PI, 2, L=L) for k in range(NL)]
        ring_out = Annulus(inner_radius=2.35, outer_radius=3.2, stroke_width=0, fill_color=BLUE, fill_opacity=0.12).move_to(vc)
        disc_in = Circle(radius=0.9, stroke_width=0, fill_color=BLUE, fill_opacity=0.12).move_to(vc)
        win = T("water", 26, BLUE).move_to(vc)
        wout = T("water", 28, BLUE).move_to(vc + np.array([3.85, 0.0, 0]))
        self.play(FadeOut(sheet_lbl), FadeOut(wl1), FadeOut(wl2), FadeOut(wt_top), FadeOut(wt_bot), run_time=0.3)
        self.play(*[Transform(a, b) for a, b in zip(top, outer_t)],
                  *[Transform(a, b) for a, b in zip(bot, inner_t)],
                  FadeIn(ring_out), FadeIn(disc_in), run_time=2.2, rate_func=smooth)
        bl = T("sealed bilayer", 32, TEXT).move_to(np.array([4.6, 2.6, 0]))
        self.play(FadeIn(win), FadeIn(wout), FadeIn(bl, shift=LEFT * 0.1), run_time=0.4)

        # G: water does it
        self.cue("No enzyme", lead=0.1)
        enz = chip("enzyme", GREY, 30).move_to(np.array([-4.9, 2.6, 0]))
        x1 = Line(enz.get_left() + LEFT * 0.1, enz.get_right() + RIGHT * 0.1, color=TEXT, stroke_width=5)
        self.play(FadeIn(enz), run_time=0.4)
        self.play(Create(x1), run_time=0.4)
        self.cue("Water does", lead=0.1)
        pushes = VGroup(*[Arrow(vc + 3.25 * np.array([math.cos(a), math.sin(a), 0]),
                                vc + 2.55 * np.array([math.cos(a), math.sin(a), 0]), buff=0, color=BLUE,
                                stroke_width=7, max_tip_length_to_length_ratio=0.5)
                          for a in [0.5, 1.7, 2.7, 3.7, 4.6, 5.6]])
        self.play(FadeIn(pushes, lag_ratio=0.15), run_time=1.0)
        self.cue("touch the tails", lead=0.3)
        tails = VGroup(*[m[i] for m in top + bot for i in (1, 2)])
        self.play(Indicate(tails, color=YELLOW, scale_factor=1.0), run_time=1.0)
        self.finish()
