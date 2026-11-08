"""Synapse elimination, chapter 3: The Focal Block  (Biochemistrypedia chaptered explainer)

COLOR MAP (one color per concept, shared with the other chapters; taken from scenes.old.py)
  BLUE   = motor axon A and its terminals (also neuron 1 in the culture)
  ORANGE = motor axon B and its terminals (also neuron 2 in the culture)
  TEAL   = acetylcholine receptor sites on the muscle
  YELLOW = activity (impulses, bursts, an active site, a muscle response)
  RED    = blocked by toxin, lost, removed, punished
  GREEN  = kept, nothing lost, protected
  GREY   = muscle fiber, outlines, de-emphasized, "silent" site outline
  PURPLE = Rule 1 card (silence)         (new in this chapter)
  GOLD   = Rule 2 card (less active than neighbours)
  PINK   = the candidate-signal mutant mice (PKC, BDNF, p75) in the last plot
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CE0"
PINK = "#E58FC0"
WHITE = TEXT

# ----------------------------------------------------------------------------------------------
# geometry helpers
# ----------------------------------------------------------------------------------------------
EP = dict(n=8, sp=0.62, top=-0.9, mh=1.35, bh=1.35, gap=1.2, stem_top=3.5)      # one of two endplates
EPT = dict(n=8, sp=0.62, top=-1.25, mh=1.8, bh=1.5, gap=1.35, stem_top=3.6)     # the same, taller (no cards below)
BIG = dict(n=8, sp=1.3, top=-1.0, mh=1.5, bh=0.7, gap=0.6, stem_top=3.5)       # one big endplate
LRED = "#FF8F85"   # lighter tint of RED, for red text on the dark ground


def junction(cx, top, n, sp, mh=1.2, bh=0.6, gap=0.5, stem_top=3.4, color=BLUE, rw=0.62, groups=None):
    xs = [cx + (i - (n - 1) / 2) * sp for i in range(n)]
    groups = groups or [(color, list(range(n)))]
    gcol = {}
    for c, idx in groups:
        for i in idx:
            gcol[i] = c
    width = n * sp + 0.5
    muscle = RoundedRectangle(corner_radius=0.2, width=width, height=mh, stroke_color=GREY, stroke_width=3,
                              fill_color=GREY, fill_opacity=0.22).move_to([cx, top - mh / 2, 0])
    rec = [RoundedRectangle(corner_radius=0.06, width=sp * rw, height=0.3, stroke_color=TEAL, stroke_width=3,
                            fill_color=TEAL, fill_opacity=0.6).move_to([x, top + 0.15, 0]) for x in xs]
    yb = top + 0.3 + gap + bh / 2
    bw = sp * 0.8
    bout = [RoundedRectangle(corner_radius=0.12, width=bw, height=bh, stroke_color=gcol[i], stroke_width=3,
                             fill_color=gcol[i], fill_opacity=0.55).move_to([x, yb, 0]) for i, x in enumerate(xs)]
    # short connectors only between neighbouring boxes of one axon (no bar through the boxes)
    segs = []
    for i in range(n - 1):
        same = gcol[i] == gcol[i + 1]
        segs.append(Line([xs[i] + bw / 2, yb, 0], [xs[i + 1] - bw / 2, yb, 0], color=gcol[i],
                         stroke_width=8 if same else 0))
    stems = []
    for c, idx in groups:
        gx = float(np.mean([xs[i] for i in idx]))
        on_box = any(abs(xs[i] - gx) < 1e-6 for i in idx)
        stems.append(Line([gx, stem_top, 0], [gx, yb + (bh / 2 if on_box else 0), 0], color=c, stroke_width=8))
    return dict(xs=xs, cx=cx, top=top, n=n, sp=sp, yb=yb, yr=top + 0.15, muscle=muscle, rec=rec, bout=bout,
                segs=segs, stem=stems[0], stems=stems, width=width, mh=mh, stem_top=stem_top)


def jgroup(J, lost=()):
    """All parts of a junction; `lost` sites are left out (receptors and terminal gone)."""
    lost = set(lost)
    parts = [J["muscle"]] + list(J["stems"])
    parts += [s for k, s in enumerate(J["segs"]) if k not in lost and k + 1 not in lost]
    parts += [b for i, b in enumerate(J["bout"]) if i not in lost]
    parts += [r for i, r in enumerate(J["rec"]) if i not in lost]
    return VGroup(*parts)


def block_now(J, idxs):
    for i in idxs:
        J["rec"][i].set_stroke(RED).set_fill(RED, 0.8)


def block_anims(J, idxs):
    return [J["rec"][i].animate.set_stroke(RED).set_fill(RED, 0.8) for i in idxs]


def wash(J, idxs, opacity=0.28):
    x0, x1 = J["xs"][min(idxs)], J["xs"][max(idxs)]
    w = (x1 - x0) + J["sp"] * 0.95
    return Rectangle(width=w, height=0.62, stroke_color=RED, stroke_width=3, fill_color=RED,
                     fill_opacity=opacity).move_to([(x0 + x1) / 2, J["yr"], 0])


def withdraw(J, idxs, up=0.5):
    a = []
    for i in idxs:
        a.append(J["bout"][i].animate.shift(UP * up).set_opacity(0))
        a.append(FadeOut(J["rec"][i], scale=0.3))
    for k, s in enumerate(J["segs"]):
        if k in idxs or k + 1 in idxs:
            a.append(FadeOut(s))
    return a


def bracket_under(x0, x1, y, color, tick=0.12, w=3):
    return VGroup(Line([x0, y + tick, 0], [x0, y, 0], color=color, stroke_width=w),
                  Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=w),
                  Line([x1, y, 0], [x1, y + tick, 0], color=color, stroke_width=w))


def fire(scene, J, idxs, blocked=(), rt=0.9, stem=True):
    """An impulse runs down the stem, then the terminals at idxs and their free receptors flash."""
    dot = Dot(radius=0.15, color=YELLOW).move_to([J["cx"], J["stem_top"], 0])
    scene.add(dot)
    scene.play(dot.animate.move_to([J["cx"], J["yb"], 0]), run_time=rt * 0.55, rate_func=linear)
    anims = [FadeOut(dot, scale=0.5)]
    anims += [Indicate(J["bout"][i], color=YELLOW, scale_factor=1.15) for i in idxs]
    anims += [Indicate(J["rec"][i], color=YELLOW, scale_factor=1.25) for i in idxs if i not in blocked]
    scene.play(*anims, run_time=rt * 0.45)


def inhib(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    perp = np.array([-d[1], d[0], 0])
    mid = (a + b) / 2
    return VGroup(Line(a, b, color=color, stroke_width=w + 1),
                  Line(mid + perp * 0.0 + d * 0, mid, color=color, stroke_width=w))


def fire_multi(scene, jobs, rt=0.9):
    """jobs: list of (J, idxs, blocked). All junctions fire at once."""
    dots = []
    for J, idxs, blocked in jobs:
        d = Dot(radius=0.15, color=YELLOW).move_to([J["cx"], J["stem_top"], 0])
        dots.append(d)
    scene.add(*dots)
    scene.play(*[d.animate.move_to([J["cx"], J["yb"], 0]) for d, (J, _, _) in zip(dots, jobs)],
               run_time=rt * 0.55, rate_func=linear)
    anims = [FadeOut(d, scale=0.5) for d in dots]
    for J, idxs, blocked in jobs:
        anims += [Indicate(J["bout"][i], color=YELLOW, scale_factor=1.15) for i in idxs]
        anims += [Indicate(J["rec"][i], color=YELLOW, scale_factor=1.25) for i in idxs if i not in blocked]
    scene.play(*anims, run_time=rt * 0.45)


def cross_on(mob, color=RED, w=6, s=0.9):
    return Cross(mob, stroke_color=color, stroke_width=w).scale(s)


def flash(scene, J, idxs, blocked=(), rt=0.6):
    """Terminals and their free receptors light up (no travelling dot)."""
    anims = [Indicate(J["bout"][i], color=YELLOW, scale_factor=1.12) for i in idxs]
    anims += [Indicate(J["rec"][i], color=YELLOW, scale_factor=1.25) for i in idxs if i not in blocked]
    scene.play(*anims, run_time=rt)


def tag(text, color=TEXT, size=24, **kw):
    return T(text, size, color, **kw)


def pathdot(points, color=YELLOW, r=0.14):
    d = Dot(radius=r, color=color).move_to(points[0])
    p = VMobject().set_points_as_corners([np.array(q, float) for q in points])
    return d, p


# ----------------------------------------------------------------------------------------------
# activity icons and the two rule cards
# ----------------------------------------------------------------------------------------------
def site_icon(kind, r=0.26):
    if kind == "silent":
        return Circle(radius=r, stroke_color=GREY, stroke_width=3.5, fill_color=BG, fill_opacity=1)
    if kind == "weak":
        return Circle(radius=r, stroke_color=YELLOW, stroke_width=3.5, fill_color=YELLOW, fill_opacity=0.25)
    return Circle(radius=r, stroke_color=YELLOW, stroke_width=3.5, fill_color=YELLOW, fill_opacity=0.95)


class RuleCard(VGroup):
    pass


def rule_icon(n, scale=1.0, spacing=1.0):
    kinds = ["silent"] if n == 1 else ["active", "weak", "active", "active"]
    sites = [site_icon(k, 0.28 * scale) for k in kinds]
    g = VGroup(*sites).arrange(RIGHT, buff=spacing - 0.56 * scale)
    g.target = sites[0] if n == 1 else sites[1]
    g.sites = sites
    return g


def rule_card(n, cx, cy, big=True, dim=False, body=True, icon=True, crossed=False):
    color = PURPLE if n == 1 else GOLD
    w, h = (6.1, 4.0) if big else (6.1, 1.45)
    frame = RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=color,
                             stroke_width=3 if dim else 4.5, fill_color=color,
                             fill_opacity=0.05 if dim else 0.12).move_to([cx, cy, 0])
    if dim:
        frame.set_stroke(opacity=0.55)
    tg = T(f"RULE {n}", 28 if big else 24, color, weight=BOLD)
    if big:
        tg.move_to([cx, cy + h / 2 - 0.45, 0])
        texts = (["A silent synapse", "is removed."] if n == 1 else
                 ["A synapse is removed when it is", "less active than nearby synapses,", "if enough of them are active."])
        lines = [T(t, 26) for t in texts]
        bg = VGroup(*lines).arrange(DOWN, buff=0.14).move_to([cx, cy + 0.45, 0])
    else:
        tg.move_to([cx - w / 2 + 0.25 + tg.width / 2, cy + h / 2 - 0.34, 0])
        texts = (["A silent synapse is removed."] if n == 1 else
                 ["Removed when less active than nearby", "synapses, if enough of them are active."])
        lines = [T(t, 22) for t in texts]
        bg = VGroup(*lines).arrange(DOWN, buff=0.1).move_to([cx, cy - 0.22, 0])
    ic = rule_icon(n, 1.2, 1.15).move_to([cx, cy - h / 2 + 0.85, 0]) if (big and icon) else VGroup()
    card = RuleCard(frame, tg)
    card.frame, card.tag, card.lines, card.icon, card.n, card.color = frame, tg, lines, ic, n, color
    card.cross = None
    if body:
        card.add(*lines)          # when body is False the sentence is left out; a scene fades it in on its cue
    if icon and big:
        card.add(ic)
        if crossed:
            card.cross = cross_on(ic.target, s=1.0)
            card.add(card.cross)
    if dim:
        tg.set_opacity(0.6)
        if body:
            for ln in lines:
                ln.set_opacity(0.6)
        if ic:
            ic.set_opacity(0.6)
        if card.cross is not None:
            card.cross.set_opacity(0.6)
    return card


def card_off(card):
    """Animations that grey a lit card out (still readable)."""
    a = [card.frame.animate.set_stroke(opacity=0.55, width=3).set_fill(opacity=0.05), card.tag.animate.set_opacity(0.6)]
    a += [ln.animate.set_opacity(0.6) for ln in card.lines]
    if card.icon:
        a.append(card.icon.animate.set_opacity(0.6))
    if card.cross is not None:
        a.append(card.cross.animate.set_opacity(0.6))
    return a


def card_on(card):
    a = [card.frame.animate.set_stroke(opacity=1, width=5).set_fill(card.color, 0.2), card.tag.animate.set_opacity(1)]
    a += [ln.animate.set_opacity(1) for ln in card.lines]
    return a


BIGX = (-3.3, 3.3)


def big_cards(dim=(False, False), body=(True, True), icon=True, crossed=(False, False), cy=-0.15):
    return (rule_card(1, BIGX[0], cy, True, dim[0], body[0], icon, crossed[0]),
            rule_card(2, BIGX[1], cy, True, dim[1], body[1], icon, crossed[1]))


def small_cards(dim=(False, False), cy=-3.1):
    return rule_card(1, -3.25, cy, False, dim[0]), rule_card(2, 3.25, cy, False, dim[1])


# ----------------------------------------------------------------------------------------------
# whole-muscle schematic (chapter opening: TTX and stimulation)
# ----------------------------------------------------------------------------------------------
TRUNK_X = -3.2
JY, EY = 1.9, -0.4
BR_X = [-5.7, -4.4, -2.0, -0.7]   # where the four branches reach the muscle


def whole_muscle():
    muscle = RoundedRectangle(corner_radius=0.25, width=7.0, height=3.0, stroke_color=GREY, stroke_width=3,
                              fill_color=GREY, fill_opacity=0.22).move_to([-3.2, -1.9, 0])
    stripes = VGroup(*[Line([-6.5, y, 0], [0.1, y, 0], color=GREY, stroke_width=2).set_opacity(0.5)
                       for y in (-1.2, -1.7, -2.2)])
    lbl = T("newborn rat muscle", 28, GREY).move_to([-3.2, -2.85, 0])
    trunk = Line([TRUNK_X, 3.5, 0], [TRUNK_X, JY, 0], color=BLUE, stroke_width=10)
    brs = VGroup(*[Line([TRUNK_X, JY, 0], [x, EY, 0], color=BLUE, stroke_width=7) for x in BR_X])
    ends = VGroup(*[Dot(radius=0.14, color=BLUE).move_to([x, EY, 0]) for x in BR_X])
    return VGroup(muscle, stripes, lbl, trunk, brs, ends), lbl


def gauge(cx=4.05, y=-1.45):
    """Elimination speed: a track with a 'normal' reference tick and a marker that moves along it."""
    half = 2.1
    track = Line([cx - half, y, 0], [cx + half, y, 0], color=GREY, stroke_width=8)
    t_mid = Line([cx, y - 0.3, 0], [cx, y + 0.3, 0], color=TEXT, stroke_width=5)
    t_l = Line([cx - half, y - 0.18, 0], [cx - half, y + 0.18, 0], color=GREY, stroke_width=5)
    t_r = Line([cx + half, y - 0.18, 0], [cx + half, y + 0.18, 0], color=GREY, stroke_width=5)
    title = T("elimination speed", 30, TEXT).move_to([cx, y + 1.05, 0])
    normal = T("normal", 26, TEXT).move_to([cx, y - 0.65, 0])
    marker = Dot(radius=0.3, color=TEXT).move_to([cx, y, 0])
    base = VGroup(track, t_mid, t_l, t_r, title, normal)
    return dict(base=base, marker=marker, c=np.array([cx, y, 0.0]), left=np.array([cx - half, y, 0.0]),
                right=np.array([cx + half, y, 0.0]), y=y, cx=cx, half=half)


def spin(hand, c, rate):
    pass


def impulse_down(scene, rt=1.1, stop_y=None, color=YELLOW):
    """A dot runs down the trunk; if stop_y is None it fans out to the four fibres."""
    d = Dot(radius=0.16, color=color).move_to([TRUNK_X, 3.5, 0])
    scene.add(d)
    if stop_y is not None:
        scene.play(d.animate.move_to([TRUNK_X, stop_y, 0]), run_time=rt, rate_func=linear)
        return d
    scene.play(d.animate.move_to([TRUNK_X, JY, 0]), run_time=rt * 0.4, rate_func=linear)
    ds = [Dot(radius=0.14, color=color).move_to([TRUNK_X, JY, 0]) for _ in BR_X]
    scene.remove(d)
    scene.add(*ds)
    scene.play(*[q.animate.move_to([x, EY, 0]) for q, x in zip(ds, BR_X)], run_time=rt * 0.6, rate_func=linear)
    scene.play(*[FadeOut(q, scale=0.4) for q in ds], run_time=0.2)
    return None


# ----------------------------------------------------------------------------------------------
# culture schematic (Lo and Poo)
# ----------------------------------------------------------------------------------------------
NX = (-4.0, 4.0)
BUX = (NX[0] + 0.8, NX[1] - 0.8)      # where the burst icons sit


def culture(labels=False):
    muscle = RoundedRectangle(corner_radius=0.3, width=11.8, height=1.3, stroke_color=GREY, stroke_width=3,
                              fill_color=GREY, fill_opacity=0.22).move_to([0, -2.3, 0])
    mlab = T("muscle cell", 26, GREY).move_to([0, -2.45, 0])
    n1 = Circle(radius=0.7, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.4).move_to([NX[0], 2.7, 0])
    n2 = Circle(radius=0.7, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE, fill_opacity=0.4).move_to([NX[1], 2.7, 0])
    ax1 = Line([NX[0], 2.0, 0], [NX[0], -0.9, 0], color=BLUE, stroke_width=8)
    ax2 = Line([NX[1], 2.0, 0], [NX[1], -0.9, 0], color=ORANGE, stroke_width=8)
    b1 = RoundedRectangle(corner_radius=0.12, width=1.3, height=0.45, stroke_color=BLUE, stroke_width=3,
                          fill_color=BLUE, fill_opacity=0.55).move_to([NX[0], -0.95, 0])
    b2 = RoundedRectangle(corner_radius=0.12, width=1.3, height=0.45, stroke_color=ORANGE, stroke_width=3,
                          fill_color=ORANGE, fill_opacity=0.55).move_to([NX[1], -0.95, 0])
    r1 = RoundedRectangle(corner_radius=0.06, width=1.0, height=0.28, stroke_color=TEAL, stroke_width=3,
                          fill_color=TEAL, fill_opacity=0.6).move_to([NX[0], -1.5, 0])
    r2 = RoundedRectangle(corner_radius=0.06, width=1.0, height=0.28, stroke_color=TEAL, stroke_width=3,
                          fill_color=TEAL, fill_opacity=0.6).move_to([NX[1], -1.5, 0])
    d = dict(muscle=muscle, mlab=mlab, n1=n1, n2=n2, ax1=ax1, ax2=ax2, b1=b1, b2=b2, r1=r1, r2=r2)
    d["l1"] = T("neuron 1", 28, BLUE)
    d["l1"].move_to([NX[0] - 0.95 - d["l1"].width / 2, 2.7, 0])
    d["l2"] = T("neuron 2", 28, ORANGE)
    d["l2"].move_to([NX[1] + 0.95 + d["l2"].width / 2, 2.7, 0])
    d["all"] = VGroup(muscle, mlab, ax1, ax2, n1, n2, b1, b2, r1, r2)
    return d


def burst_icon(x, y, color=YELLOW):
    hs = [0.25, 0.5, 0.35, 0.55, 0.3, 0.5, 0.25]
    g = VGroup(*[Line([x + (i - 3) * 0.13, y - h / 2, 0], [x + (i - 3) * 0.13, y + h / 2, 0], color=color, stroke_width=5)
                 for i, h in enumerate(hs)])
    return g


def resp_panel(cy, rows, title, title_color=TEXT):
    """A recording panel centred on x=0 with axis labels: bars before the burst, a marker, bars after.
    rows: list of (color, before_heights, after_heights)."""
    h = 2.7 if len(rows) == 1 else 3.4
    W = 4.5
    frame = RoundedRectangle(corner_radius=0.15, width=W, height=h, stroke_color=GREY, stroke_width=2.5,
                             fill_color=GREY, fill_opacity=0.08).move_to([0, cy, 0])
    ttl = T(title, 24, title_color).move_to([0, cy + h / 2 + 0.28, 0])
    xs_b, xs_a = [-1.7, -1.3, -0.9], [0.0, 0.4, 0.8, 1.2]
    y0s = [cy - h / 2 + 0.65] if len(rows) == 1 else [cy - h / 2 + 0.65, cy + 0.1]
    mark = DashedLine([-0.45, cy - h / 2 + 0.5, 0], [-0.45, cy + h / 2 - 0.55, 0], color=YELLOW, stroke_width=3)
    blab = T("burst", 24, YELLOW).move_to([-0.45, cy + h / 2 - 0.3, 0])
    ylab = T("response", 24, GREY).rotate(PI / 2).move_to([-W / 2 - 0.25, cy, 0])
    tlab = T("time (minutes)", 24, GREY).move_to([0, cy - h / 2 + 0.25, 0])
    befores, afters = [], []
    for (col, hb, ha), y0 in zip(rows, y0s):
        base = Line([-W / 2 + 0.2, y0, 0], [W / 2 - 0.2, y0, 0], color=GREY, stroke_width=2).set_opacity(0.6)
        befores.append(VGroup(base, *[Rectangle(width=0.26, height=hh * 0.95, stroke_width=0, fill_color=col, fill_opacity=0.9)
                                      .move_to([x, y0 + hh * 0.475, 0]) for x, hh in zip(xs_b, hb)]))
        afters.append([Rectangle(width=0.26, height=hh * 0.95, stroke_width=0, fill_color=col, fill_opacity=0.9)
                       .move_to([x, y0 + hh * 0.475, 0]) for x, hh in zip(xs_a, ha)])
    return dict(frame=frame, title=ttl, mark=mark, blab=blab, ylab=ylab, tlab=tlab, before=befores, after=afters, h=h,
                xs_a=xs_a, y0s=y0s, W=W)


# ----------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Synapse Elimination: One Muscle Fiber, One Axon"
    TITLE = "The Focal Block"


# ----------------------------------------------------------------------------------------------
class S01Q(SpokenScene):
    def construct(self):
        top = T("Starting size alone does not decide.", 36).move_to([0, 3.05, 0])
        f1 = RoundedRectangle(corner_radius=0.2, width=6.1, height=4.0, stroke_color=PURPLE, stroke_width=4.5,
                              fill_color=PURPLE, fill_opacity=0.1).move_to([-3.3, -0.35, 0])
        f2 = RoundedRectangle(corner_radius=0.2, width=6.1, height=4.0, stroke_color=GOLD, stroke_width=4.5,
                              fill_color=GOLD, fill_opacity=0.1).move_to([3.3, -0.35, 0])
        q1 = T("?", 110, GREY, weight=BOLD).move_to(f1)
        q2 = T("?", 110, GREY, weight=BOLD).move_to(f2)
        self.add(top, f1, f2, q1, q2)
        self.at("what does")
        top2 = T("So what does?", 40, YELLOW).move_to([0, 3.05, 0])
        self.play(ReplacementTransform(top, top2), run_time=0.5)
        self.at("silence")
        h1 = T("Silence?", 40, PURPLE, weight=BOLD).move_to([-3.3, 0.9, 0])
        i1 = rule_icon(1, 1.7, 1.2).move_to([-3.3, -0.65, 0])
        self.play(FadeOut(q1), FadeIn(h1, shift=UP * 0.15), FadeIn(i1, scale=0.7), run_time=0.7)
        self.at("being quieter")
        h2 = T("Quieter than a neighbour?", 30, GOLD, weight=BOLD).move_to([3.3, 0.9, 0])
        i2 = rule_icon(2, 1.3, 1.1).move_to([3.3, -0.65, 0])
        self.play(FadeOut(q2), FadeIn(h2, shift=UP * 0.15), FadeIn(i2, scale=0.7), run_time=0.7)
        self.play(Indicate(i2.sites[1], color=YELLOW, scale_factor=1.3), run_time=0.8)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S02Ttx(SpokenScene):
    def construct(self):
        wm, lbl = whole_muscle()
        g = gauge()
        mk = g["marker"]
        self.add(wm, g["base"], mk)
        self.wait(0.3)
        self.at("blocking nerve")
        impulse_down(self, 1.1)
        self.at("tetrodotoxin")
        blk = Line([TRUNK_X - 0.55, 2.75, 0], [TRUNK_X + 0.55, 2.75, 0], color=RED, stroke_width=12)
        chp = chip("tetrodotoxin", LRED, size=30).move_to([-0.35, 2.75, 0])
        lead = Line([TRUNK_X + 0.6, 2.75, 0], [chp.get_left()[0], 2.75, 0], color=RED, stroke_width=3)
        self.play(Create(blk), FadeIn(chp, shift=LEFT * 0.2), Create(lead), run_time=0.35)
        d = impulse_down(self, 0.5, stop_y=3.0)
        self.play(FadeOut(d, scale=0.4), run_time=0.12)
        self.at("slows elimination")
        bar = Line(g["c"], g["c"] + 0.001 * RIGHT, color=RED, stroke_width=12)
        self.add(bar)
        sl = T("slower", 30, LRED, weight=BOLD).move_to(g["left"] + DOWN * 0.65)
        self.play(mk.animate.move_to(g["left"]).set_color(RED),
                  Transform(bar, Line(g["c"], g["left"], color=RED, stroke_width=12)),
                  FadeIn(sl, shift=DOWN * 0.1), run_time=1.6)
        self.play(Indicate(mk, color=RED, scale_factor=1.3), run_time=0.6)
        self.finish()


class S03Stim(SpokenScene):
    def construct(self):
        wm, lbl = whole_muscle()
        g = gauge()
        mk = g["marker"]
        self.add(wm, g["base"], mk)
        self.at("electrical stimulation")
        tip = Polygon([TRUNK_X + 0.1, 2.6, 0], [-1.9, 2.85, 0], [-1.9, 2.35, 0], stroke_color=YELLOW, stroke_width=3,
                      fill_color=YELLOW, fill_opacity=0.6)
        body = RoundedRectangle(corner_radius=0.08, width=0.75, height=0.5, stroke_color=YELLOW, stroke_width=3,
                                fill_color=YELLOW, fill_opacity=0.3).move_to([-1.55, 2.6, 0])
        el = T("electrode", 28, YELLOW).move_to([-1.55, 3.2, 0])
        self.play(FadeIn(tip, shift=LEFT * 0.2), FadeIn(body, shift=LEFT * 0.2), FadeIn(el), run_time=0.6)
        impulse_down(self, 0.9)
        self.at("some patterns")

        def train_a(x0, y):
            return VGroup(*[Line([x0 + g_ * 0.62 + k * 0.1, y - 0.2, 0], [x0 + g_ * 0.62 + k * 0.1, y + 0.2, 0],
                                 color=YELLOW, stroke_width=5) for g_ in range(3) for k in range(4)])

        def train_b(x0, y):
            return VGroup(*[Line([x0 + k * 0.36, y - 0.2, 0], [x0 + k * 0.36, y + 0.2, 0], color=YELLOW, stroke_width=5)
                            for k in range(6)])

        pa, pb = train_a(0.2, 3.25), train_b(0.2, 2.15)
        la = Line([-1.15, 2.7, 0], [0.0, 3.25, 0], color=YELLOW, stroke_width=3)
        lb = Line([-1.15, 2.5, 0], [0.0, 2.15, 0], color=YELLOW, stroke_width=3)
        self.play(Create(la), Create(lb), LaggedStart(*[FadeIn(t) for t in list(pa) + list(pb)], lag_ratio=0.05),
                  run_time=0.9)
        self.at("speeds it up")
        ta = T("speeds it up", 28, GREEN, weight=BOLD).move_to([4.5, 3.25, 0])
        tb = T("no change", 28, GREY).move_to([4.5, 2.15, 0])
        bar = Line(g["c"], g["c"] + 0.001 * RIGHT, color=GREEN, stroke_width=12)
        self.add(bar)
        sf = T("faster", 30, GREEN, weight=BOLD).move_to(g["right"] + DOWN * 0.65)
        self.play(pb.animate.set_opacity(0.3), lb.animate.set_opacity(0.3), FadeIn(ta, shift=LEFT * 0.1), FadeIn(tb),
                  mk.animate.move_to(g["right"]).set_color(GREEN),
                  Transform(bar, Line(g["c"], g["right"], color=GREEN, stroke_width=12)),
                  FadeIn(sf, shift=DOWN * 0.1), run_time=1.6)
        self.at("activity sets the pace")
        c = chip("activity sets the pace", YELLOW, size=32).move_to([4.05, -3.0, 0])
        self.play(FadeIn(c, shift=UP * 0.2), run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S04Both(SpokenScene):
    def construct(self):
        J = junction(0, groups=[(BLUE, list(range(4))), (ORANGE, list(range(4, 8)))], **BIG)
        jg = jgroup(J)
        mlab = T("muscle fiber", 28, GREY).move_to([0, -1.75, 0])
        a1 = T("axon", 28, BLUE).move_to([-4.3, 3.1, 0])
        a2 = T("axon", 28, ORANGE).move_to([4.3, 3.1, 0])
        self.play(FadeIn(jg), FadeIn(mlab), FadeIn(a1), FadeIn(a2), run_time=0.7)
        self.at("every input")
        ins = VGroup(*J["stems"], *J["segs"], *J["bout"])
        self.play(ins.animate.set_opacity(0.2), run_time=0.6)
        self.at("at once")
        self.play(ins.animate.set_opacity(1), run_time=0.5)
        self.wait(0.2)
        self.play(ins.animate.set_opacity(0.2), run_time=0.45)
        self.play(ins.animate.set_opacity(1), run_time=0.45)
        self.at("quiet input")
        b = J["bout"][2]
        self.play(b.animate.set_stroke(opacity=0.25).set_fill(opacity=0.1), run_time=0.5)
        self.at("its neighbors")
        q = T("?", 70, YELLOW, weight=BOLD).move_to([J["xs"][2], 1.35, 0])
        nb = [J["bout"][i] for i in (1, 3)]
        self.play(FadeIn(q, scale=0.6), *[Indicate(x, color=YELLOW, scale_factor=1.2) for x in nb], run_time=1.1)
        self.at("two rules")
        c1, c2 = big_cards(body=(False, False))
        self.play(FadeOut(VGroup(jg, mlab, q, a1, a2)), run_time=0.5)
        self.play(FadeIn(c1, shift=UP * 0.2), FadeIn(c2, shift=UP * 0.2), run_time=0.8)
        self.finish()


class S05R1(SpokenScene):
    def construct(self):
        c1, c2 = big_cards(dim=(False, True), body=(False, False))
        self.add(c1, c2)
        self.at("a silent synapse")
        self.play(FadeIn(VGroup(*c1.lines), shift=UP * 0.1), Indicate(c1.icon.target, color=GREY, scale_factor=1.3),
                  run_time=0.6)
        self.at("is removed")
        x = cross_on(c1.icon.target, s=1.0)
        self.play(Create(x), run_time=0.6)
        self.finish()


class S06R2(SpokenScene):
    def construct(self):
        c1, c2 = big_cards(dim=(True, False), body=(True, False), crossed=(True, False))
        self.add(c1, c2)
        self.at("a synapse is removed")
        self.play(FadeIn(c2.lines[0], shift=UP * 0.1), run_time=0.5)
        self.at("less active")
        self.play(FadeIn(c2.lines[1], shift=UP * 0.1), Indicate(c2.icon.sites[1], color=YELLOW, scale_factor=1.4),
                  run_time=0.7)
        self.at("nearby synapses")
        self.play(*[Indicate(c2.icon.sites[i], color=YELLOW, scale_factor=1.25) for i in (0, 2, 3)], run_time=0.8)
        self.at("enough of them")
        self.play(FadeIn(c2.lines[2], shift=UP * 0.1),
                  *[Indicate(c2.icon.sites[i], color=YELLOW, scale_factor=1.25) for i in (0, 2, 3)], run_time=0.6)
        self.at("are active")
        x = cross_on(c2.icon.target, s=1.0)
        self.play(Create(x), run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S07Test(SpokenScene):
    def construct(self):
        J = junction(0, **BIG)
        mlab = T("muscle fiber", 28, GREY).move_to([0, -1.75, 0])
        self.add(jgroup(J), mlab)
        self.at("silence part")
        w = wash(J, (0, 1), 0.3)
        w.stretch_to_fit_height(0.75)
        sil = T("silenced", 30, LRED, weight=BOLD).move_to([(J["xs"][0] + J["xs"][1]) / 2, -3.2, 0])
        self.play(FadeIn(w), *block_anims(J, (0, 1)), FadeIn(sil, shift=UP * 0.15), run_time=0.6)
        self.at("one junction")
        jl = T("one junction", 30, TEXT).move_to([2.4, 3.1, 0])
        self.play(FadeIn(jl), run_time=0.4)
        self.at("leave the rest")
        wk = T("working", 30, YELLOW, weight=BOLD).move_to([(J["xs"][2] + J["xs"][7]) / 2, -3.2, 0])
        br = bracket_under(J["xs"][2] - 0.5, J["xs"][7] + 0.5, -2.75, YELLOW)
        self.play(FadeIn(wk, shift=UP * 0.15), Create(br), run_time=0.5)
        fire(self, J, range(2, 8), blocked=(0, 1), rt=1.0)
        self.finish()


def tox_pill(rec, y, solid=False):
    return RoundedRectangle(corner_radius=0.18, width=rec.width + 0.12, height=0.42, stroke_color=RED, stroke_width=3,
                            fill_color=RED, fill_opacity=0.95 if solid else 0.3).move_to([rec.get_center()[0], y, 0])


ZOOM = dict(n=8, sp=1.3, top=-1.0, mh=1.5, bh=0.8, gap=1.5, stem_top=3.6, rw=0.62)


class S08Tox(SpokenScene):
    def construct(self):
        J = junction(0, **ZOOM)
        bound = (0, 1)
        self.add(jgroup(J))
        self.at("alpha")
        hov = -0.35
        pills = [tox_pill(J["rec"][i], hov) for i in bound]
        mx = (J["xs"][0] + J["xs"][1]) / 2
        tl = T("alpha-bungarotoxin", 30, LRED, weight=BOLD).move_to([mx, 0.3, 0])
        self.play(*[FadeIn(p, shift=DOWN * 0.3) for p in pills], FadeIn(tl), run_time=0.8)
        self.at("snake toxin")
        self.wait(0.3)
        self.at("binds acetylcholine")
        self.play(*[p.animate.move_to([J["xs"][i], J["yr"], 0]).set_fill(RED, 0.95) for p, i in zip(pills, bound)],
                  run_time=1.0)
        self.at("receptors")
        rl = T("acetylcholine receptors", 28, TEAL).move_to([1.6, J["top"] - 0.6, 0])
        self.play(FadeIn(rl, shift=UP * 0.1), *[Indicate(J["rec"][i], color=TEAL, scale_factor=1.15) for i in range(2, 8)],
                  run_time=0.8)
        self.at("almost irreversibly")
        ch = chip("almost irreversible", LRED, size=30).move_to([2.9, -3.1, 0])
        self.play(FadeIn(ch, shift=UP * 0.2), run_time=0.5)
        self.at("blocks each one")
        self.play(*block_anims(J, bound), *[Indicate(p, color=RED, scale_factor=1.15) for p in pills], run_time=0.6)
        bl = T("blocked", 30, LRED, weight=BOLD).move_to([mx, -3.1, 0])
        self.play(FadeIn(bl, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S09Muscle(SpokenScene):
    def construct(self):
        J = junction(0, **ZOOM)
        bound = (0, 1)
        block_now(J, bound)
        pills = [tox_pill(J["rec"][i], J["yr"], True) for i in bound]
        self.add(jgroup(J), *pills)
        mx = (J["xs"][0] + J["xs"][1]) / 2
        ox = (J["xs"][2] + J["xs"][7]) / 2
        self.at("where it sits")
        tl = T("toxin here", 28, LRED).move_to([mx, -3.1, 0])
        fl = T("no toxin", 28, TEAL).move_to([ox, -3.1, 0])
        self.play(FadeIn(tl), FadeIn(fl), run_time=0.5)

        def release():
            dots, tgt = [], []
            for i in range(8):
                for dx in (-0.15, 0.15):
                    dots.append(Dot(radius=0.09, color=WHITE).move_to([J["xs"][i] + dx, J["yb"] - 0.45, 0]))
                    y = J["yr"] + 0.36 if i in bound else J["yr"] + 0.2
                    tgt.append([J["xs"][i] + dx, y, 0])
            self.add(*dots)
            self.play(*[d.animate.move_to(p) for d, p in zip(dots, tgt)], run_time=0.9, rate_func=linear)
            opens = [i for i in range(8) if i not in bound]
            glow = [Rectangle(width=1.1, height=0.7, stroke_width=0, fill_color=YELLOW, fill_opacity=0.5)
                    .move_to([J["xs"][i], J["top"] - 0.4, 0]) for i in opens]
            self.add(*glow)
            self.play(*[Indicate(J["rec"][i], color=YELLOW, scale_factor=1.3) for i in opens],
                      *[FadeOut(d, scale=0.5) for d in dots], run_time=0.8)
            return glow

        self.at("muscle stops responding")
        glow = release()
        rn = T("no response", 30, LRED, weight=BOLD).move_to([mx, -1.9, 0])
        rr = T("responds", 30, YELLOW, weight=BOLD).move_to([ox, -1.9, 0])
        self.play(FadeIn(rn), FadeIn(rr), *[g.animate.set_opacity(0.0) for g in glow], run_time=0.5)
        self.remove(*glow)
        self.at("axon above")
        al = T("axon: untouched", 30, BLUE).move_to([3.3, 3.1, 0])
        self.play(FadeIn(al, shift=LEFT * 0.2), run_time=0.4)
        fire(self, J, range(8), blocked=bound, rt=0.8)
        fire(self, J, range(8), blocked=bound, rt=0.8)
        self.at("quieter here")
        ch = chip("quieter here:\nthe muscle responds less", YELLOW, size=28).move_to([-3.4, 2.5, 0])
        self.play(FadeIn(ch, shift=DOWN * 0.2), Indicate(rn, color=RED, scale_factor=1.15), run_time=0.7)
        self.at("muscle responds less")
        self.play(Indicate(ch, color=YELLOW, scale_factor=1.05), run_time=0.8)
        self.finish()


def two_endplates(washed=True, patch=(0, 1), ep=EP):
    JL = junction(-3.55, **ep)
    JR = junction(3.55, **ep)
    wl = wash(JL, patch) if washed else None
    wr = wash(JR, range(8)) if washed else None
    if washed:
        block_now(JL, patch)
        block_now(JR, range(8))
    return JL, JR, wl, wr


class S10Setup(SpokenScene):
    def construct(self):
        JL, JR, _, _ = two_endplates(False, ep=EPT)
        wl = wash(JL, (0, 1))
        wr = wash(JR, range(8))
        mouse = chip("in a living mouse", TEXT, size=30).move_to([0, 3.35, 0])
        self.play(FadeIn(jgroup(JL)), FadeIn(jgroup(JR)), FadeIn(mouse), run_time=0.8)
        self.at("one small patch")
        e1 = T("endplate 1", 28, TEXT).move_to([-5.4, 2.4, 0])
        self.play(FadeIn(e1), FadeIn(wl), *block_anims(JL, (0, 1)), run_time=0.7)
        sp = T("one small patch", 28, LRED).move_to([-4.9, -2.55, 0])
        self.play(FadeIn(sp, shift=UP * 0.1), run_time=0.4)
        self.at("second end plate")
        e2 = T("endplate 2", 28, TEXT).move_to([5.4, 2.4, 0])
        self.play(FadeIn(e2), run_time=0.4)
        self.at("cover every receptor")
        self.play(FadeIn(wr), *block_anims(JR, range(8)), run_time=0.8)
        ev = T("every receptor", 28, LRED).move_to([3.55, -2.55, 0])
        self.play(FadeIn(ev, shift=UP * 0.1), run_time=0.4)
        self.finish()


def ep_scene(scene, lost_left=(), nodim=True):
    JL, JR, wl, wr = two_endplates(True)
    scene.add(jgroup(JL, lost_left), wl, jgroup(JR), wr)
    return JL, JR, wl, wr


class S11Predict(SpokenScene):
    def construct(self):
        JL, JR, wl, wr = ep_scene(self)
        c1, c2 = small_cards()
        self.add(c1, c2)
        top = T("Predict.", 40, YELLOW, weight=BOLD).move_to([0, 3.4, 0])
        self.add(top)
        self.at("over the following weeks")
        qb = RoundedRectangle(corner_radius=0.2, width=1.3, height=2.0, stroke_color=YELLOW, stroke_width=4,
                              fill_color=YELLOW, fill_opacity=0.1).move_to([0, 0.3, 0])
        qm = T("?", 100, YELLOW, weight=BOLD).move_to(qb)
        self.play(FadeIn(qb, scale=0.8), FadeIn(qm, scale=0.7), run_time=0.7)
        self.at("each rule")
        self.play(Indicate(c1.frame, color=PURPLE, scale_factor=1.03), Indicate(c2.frame, color=GOLD, scale_factor=1.03),
                  run_time=0.9)
        self.finish()


class S12Pause(NarratedScene):
    def construct(self):
        JL, JR, wl, wr = ep_scene(self)
        c1, c2 = small_cards()
        qb = RoundedRectangle(corner_radius=0.2, width=1.3, height=2.0, stroke_color=YELLOW, stroke_width=4,
                              fill_color=YELLOW, fill_opacity=0.1).move_to([0, 0.3, 0])
        qm = T("?", 100, YELLOW, weight=BOLD).move_to(qb)
        top = T("Predict.", 40, YELLOW, weight=BOLD).move_to([0, 3.4, 0])
        self.add(c1, c2, qb, qm, top)
        self.finish()


def x_on_bouts(J, idxs):
    return [cross_on(J["bout"][i], RED, 5, 0.8) for i in idxs]


class S13R1(SpokenScene):
    def construct(self):
        JL, JR, wl, wr = ep_scene(self)
        c1, c2 = small_cards(dim=(False, True))
        self.add(c1, c2)
        self.at("predicts loss")
        xl = x_on_bouts(JL, (0, 1))
        xr = x_on_bouts(JR, range(8))
        ll = T("loss", 30, LRED, weight=BOLD).move_to([-5.4, -2.05, 0])
        lr = T("loss", 30, LRED, weight=BOLD).move_to([3.55, -2.05, 0])
        self.play(*[Create(x) for x in xl], FadeIn(ll, shift=UP * 0.1), run_time=0.7)
        self.at("both junctions")
        self.play(*[Create(x) for x in xr], FadeIn(lr, shift=UP * 0.1), run_time=0.8)
        self.at("silent sites")
        self.play(Indicate(wl, color=RED, scale_factor=1.1), Indicate(wr, color=RED, scale_factor=1.05), run_time=0.9)
        self.finish()


class S14R2(SpokenScene):
    def construct(self):
        JL, JR, wl, wr = ep_scene(self)
        c1, c2 = small_cards(dim=(True, False))
        self.add(c1, c2)
        self.at("predicts loss only")
        xl = x_on_bouts(JL, (0, 1))
        ll = T("loss", 30, LRED, weight=BOLD).move_to([-5.4, -2.05, 0])
        self.play(*[Create(x) for x in xl], FadeIn(ll, shift=UP * 0.1), run_time=0.7)
        self.at("partial block")
        self.play(Indicate(wl, color=RED, scale_factor=1.1), run_time=0.7)
        self.at("small silent patch")
        sp = T("silent patch", 24, LRED).move_to([-5.4, -2.05, 0])
        self.play(ReplacementTransform(ll, sp), run_time=0.5)
        self.at("larger working area")
        br = bracket_under(JL["xs"][2] - 0.3, JL["xs"][7] + 0.3, -1.87, YELLOW, tick=0.1)
        wk = T("larger working area", 24, YELLOW).move_to([-2.75, -2.12, 0])
        self.play(Create(br), FadeIn(wk, shift=UP * 0.1), run_time=0.6)
        self.play(*[Indicate(JL["bout"][i], color=YELLOW, scale_factor=1.12) for i in range(2, 8)], run_time=0.8)
        self.finish()


class S15Bgl(SpokenScene):
    def construct(self):
        card = RoundedRectangle(corner_radius=0.25, width=10.6, height=4.6, stroke_color=GOLD, stroke_width=4,
                                fill_color=GOLD, fill_opacity=0.07).move_to([0, 0.1, 0])
        yr = T("1994", 96, GOLD, font=TITLE_FONT).move_to([0, 1.25, 0])
        nm1 = T("Rita Balice-Gordon", 44, TEXT, font=TITLE_FONT)
        nm2 = T("and Lichtman", 44, TEXT, font=TITLE_FONT)
        nm = VGroup(nm1, nm2).arrange(DOWN, buff=0.12).move_to([0, -0.55, 0])
        liv = T("living mice", 32, GREY).move_to([0, -1.75, 0])
        self.play(FadeIn(card), run_time=0.4)
        self.play(Write(yr), run_time=0.8)
        self.at("rita")
        self.play(FadeIn(nm1, shift=UP * 0.1), run_time=0.5)
        self.at("lichtman")
        self.play(FadeIn(nm2, shift=UP * 0.1), run_time=0.5)
        self.at("reported the result")
        self.play(FadeIn(liv, shift=UP * 0.1), run_time=0.5)
        self.finish()


def timebar(y=-3.15):
    x0, x1 = -3.0, 5.0
    line = Line([x0, y, 0], [x1, y, 0], color=GREY, stroke_width=5)
    ticks = VGroup(*[Line([x, y - 0.12, 0], [x, y + 0.12, 0], color=GREY, stroke_width=3) for x in np.linspace(x0, x1, 5)])
    lab = T("weeks (schematic)", 26, GREY)
    lab.move_to([-6.3 + lab.width / 2, y, 0])
    mark = Dot(radius=0.18, color=TEXT).move_to([x0, y, 0])
    return line, ticks, lab, mark


class S16Res(SpokenScene):
    def construct(self):
        JL, JR, wl, wr = ep_scene(self)
        line, ticks, lab, mark = timebar()
        self.add(line, ticks, lab, mark)
        mark.add_updater(lambda m, dt: m.shift(RIGHT * min(dt * 1.4, max(0, 5.0 - m.get_center()[0]))))
        self.at("partial block")
        self.play(Indicate(wl, color=RED, scale_factor=1.12), run_time=0.6)
        self.at("lost its receptors")
        lt = T("receptors lost", 26, LRED)
        lt.move_to([-6.3 + lt.width / 2, -1.85, 0])
        self.play(*[FadeOut(JL["rec"][i], scale=0.3) for i in (0, 1)], FadeIn(lt, shift=UP * 0.1), run_time=0.8)
        self.at("nerve terminal withdrew")
        anims = []
        for i in (0, 1):
            anims.append(JL["bout"][i].animate.shift(UP * 0.5).set_opacity(0))
        for k, s in enumerate(JL["segs"]):
            if k in (0, 1):
                anims.append(FadeOut(s))
        wt = T("terminal withdrew", 26, LRED)
        wt.move_to([-6.3 + wt.width / 2, -2.6, 0])
        self.play(*anims, run_time=1.2)
        self.play(FadeIn(wt, shift=UP * 0.1), run_time=0.4)
        self.finish()


class S17Res2(SpokenScene):
    def construct(self):
        JL, JR, wl, wr = two_endplates(True)
        gl = VGroup(jgroup(JL, (0, 1)), wl)
        gl.set_opacity(0.4)
        self.add(gl, jgroup(JR), wr)
        c1, c2 = small_cards()
        lt = T("patch lost", 26, LRED).move_to([-5.3, -2.05, 0])
        self.add(c1, c2, lt)
        self.at("full block")
        self.play(Indicate(wr, color=RED, scale_factor=1.03), run_time=0.6)
        self.at("nothing was eliminated")
        ok = T("nothing lost", 30, GREEN, weight=BOLD).move_to([3.55, -2.05, 0])
        self.play(FadeIn(ok, shift=UP * 0.1), *[Indicate(b, color=GREEN, scale_factor=1.12) for b in JR["bout"]],
                  *card_off(c1), run_time=1.0)
        self.finish()


class S18Beat(NarratedScene):
    def construct(self):
        JL, JR, wl, wr = two_endplates(True)
        gl = VGroup(jgroup(JL, (0, 1)), wl)
        gl.set_opacity(0.4)
        self.add(gl, jgroup(JR), wr)
        c1, c2 = small_cards(dim=(True, False))
        lt = T("patch lost", 26, LRED).move_to([-5.3, -2.05, 0])
        ok = T("nothing lost", 30, GREEN, weight=BOLD).move_to([3.55, -2.05, 0])
        self.add(c1, c2, lt, ok)
        self.finish()


# ----------------------------------------------------------------------------------------------
ZW = dict(n=8, sp=1.3, top=0.65, mh=1.2, bh=0.7, gap=0.6, stem_top=3.7)


class S19Why(SpokenScene):
    def construct(self):
        J = junction(0, **ZW)
        block_now(J, range(8))
        w = wash(J, range(8))
        w.stretch_to_fit_width(J["width"] - 0.1)
        icons = [site_icon("silent", 0.27).move_to([x, 0.1, 0]) for x in J["xs"]]
        c1, c2 = small_cards(dim=(True, True))
        self.add(jgroup(J), w, c1, c2)
        self.at("full block")
        self.play(Indicate(w, color=RED, scale_factor=1.02), run_time=0.5)
        fire(self, J, range(8), blocked=range(8), rt=0.8)
        self.at("equally silent")
        br = bracket_under(J["xs"][0] - 0.3, J["xs"][7] + 0.3, -0.75, TEXT, tick=0.15)
        lab = T("equal: every site equally silent", 30, TEXT).move_to([0, -1.3, 0])
        self.play(*[FadeIn(i, scale=0.6) for i in icons], Create(br), FadeIn(lab, shift=UP * 0.1), run_time=0.8)
        self.at("no site is quieter")
        eq = VGroup(*[T("=", 36, TEXT, weight=BOLD).move_to([(a + b) / 2, 0.1, 0])
                      for a, b in zip(J["xs"], J["xs"][1:])])
        self.play(Indicate(icons[3], color=TEXT, scale_factor=1.4), Indicate(icons[4], color=TEXT, scale_factor=1.4),
                  FadeIn(eq, scale=0.6), run_time=1.0)
        self.play(Indicate(icons[6], color=TEXT, scale_factor=1.4), Indicate(icons[7], color=TEXT, scale_factor=1.4),
                  run_time=0.8)
        self.at("rule two wins")
        self.play(*card_on(c2), run_time=0.7)
        self.play(Indicate(c2.frame, color=GOLD, scale_factor=1.04), run_time=0.7)
        self.finish()


ZL = dict(n=8, sp=1.3, top=-0.9, mh=1.6, bh=0.9, gap=1.0, stem_top=3.6)


def lost_state_junction():
    return junction(0, **ZL)


class S20Local(SpokenScene):
    def construct(self):
        J = junction(0, **{**ZL, "top": -1.1, "mh": 1.85, "bh": 1.15, "gap": 1.25})
        block_now(J, (0, 1))
        w = wash(J, (0, 1), 0.3)
        w.stretch_to_fit_height(0.62)
        mlab = T("muscle fiber", 28, GREY).move_to([3.6, -2.65, 0])
        self.add(jgroup(J), w, mlab)
        tc = chip("toxin on the receptors", LRED, size=28).move_to([-3.2, -3.1, 0])
        ar = Arrow(tc.get_top() + UP * 0.02, [J["xs"][0] + 0.2, J["yr"] - 0.3, 0], buff=0.05, color=RED, stroke_width=6,
                   max_tip_length_to_length_ratio=0.3)
        self.add(tc, ar)
        self.at("loss stayed")
        anims = []
        for i in (0, 1):
            anims += [FadeOut(J["rec"][i], scale=0.3), J["bout"][i].animate.shift(UP * 0.5).set_opacity(0)]
        for k in (0, 1):
            anims.append(FadeOut(J["segs"][k]))
        self.play(*anims, FadeOut(tc), FadeOut(ar), run_time=0.5)
        x0, x1 = J["xs"][0] - 0.64, J["xs"][1] + 0.64
        y0, y1 = J["yr"] - 0.4, J["yr"] + 0.4
        out = Rectangle(width=x1 - x0, height=y1 - y0, stroke_color=RED, stroke_width=5).move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])
        out2 = DashedVMobject(out, num_dashes=44)
        self.at("stayed inside")
        self.play(Create(out2), run_time=0.5)
        self.at("signal behind it")
        tg = chip("signal and its range: unknown", YELLOW, size=30).move_to([2.2, -1.85, 0])
        a1 = DashedLine([x1 + 0.2, -1.85, 0], [-1.7, -1.85, 0], color=YELLOW, stroke_width=5)
        a1.add_tip(tip_length=0.25)
        self.play(Create(a1), FadeIn(tg, shift=UP * 0.2), run_time=0.7)
        self.at("how far it travels")
        qm = T("?", 70, YELLOW, weight=BOLD).move_to([-2.05, -2.5, 0])
        self.play(FadeIn(qm, scale=0.6), run_time=0.5)
        self.finish()


PANEL = dict(n=8, sp=0.62, top=-1.15, mh=1.45, bh=1.5, gap=1.35, stem_top=3.15)


class S20bArea(SpokenScene):
    def construct(self):
        JL = junction(-3.55, **PANEL)
        JR = junction(3.55, **PANEL)
        block_now(JL, (0, 1))
        block_now(JR, range(6))
        wl, wr = wash(JL, (0, 1)), wash(JR, range(6))
        cred = T("Barber and Lichtman, 1999 (same lab)", 28, GOLD).move_to([0, 3.45, 0])
        sch = T("schematic", 30, TEXT).move_to([0, 2.8, 0])
        self.add(jgroup(JL), jgroup(JR), wl, wr, cred, sch)
        self.at("active territory")
        bl = bracket_under(JL["xs"][2] - 0.3, JL["xs"][7] + 0.3, -2.75, YELLOW)
        br = bracket_under(JR["xs"][6] - 0.3, JR["xs"][7] + 0.3, -2.75, YELLOW)
        la = T("large active area", 24, YELLOW).move_to([(JL["xs"][2] + JL["xs"][7]) / 2, -3.15, 0])
        sa = T("small active area", 24, YELLOW).move_to([5.2, -3.15, 0])
        self.play(Create(bl), Create(br), FadeIn(la), FadeIn(sa), run_time=0.5)
        flash(self, JL, range(2, 8), (0, 1))
        flash(self, JR, (6, 7), range(6))
        self.at("a large active area")
        self.play(Indicate(la, color=YELLOW, scale_factor=1.1), run_time=0.5)
        self.at("small silent one")
        self.play(*withdraw(JL, (0, 1)), run_time=1.1)
        lost = T("2 of 8 sites lost", 26, LRED, weight=BOLD).move_to([-3.55, -1.75, 0])
        # Retain dashed footprints of the two withdrawn boutons: both panels began with eight.
        footprints = VGroup(*[DashedVMobject(RoundedRectangle(
            corner_radius=0.12, width=JL["sp"] * 0.8, height=PANEL["bh"],
            stroke_color=LRED, stroke_width=2).move_to([JL["xs"][i], JL["yb"], 0]),
            num_dashes=16) for i in (0, 1)])
        self.play(FadeIn(footprints), FadeIn(lost, shift=UP * 0.1), run_time=0.4)
        self.at("a small active area")
        self.play(Indicate(sa, color=YELLOW, scale_factor=1.1), run_time=0.5)
        flash(self, JR, (6, 7), range(6), rt=0.8)
        kept = T("large blocked area stays", 26, GREEN, weight=BOLD).move_to([3.55, -1.75, 0])
        self.play(FadeIn(kept, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S21Decide(SpokenScene):
    def construct(self):
        J = junction(0, **{**ZL, "stem_top": 3.0})
        pl = (0, 1)
        block_now(J, pl)
        w = wash(J, pl)
        sch = T("schematic of the 1994 result", 28, GREY).move_to([-3.6, 2.35, 0])
        self.add(jgroup(J), w, sch)
        self.at("toxin was put")
        self.play(Indicate(w, color=RED, scale_factor=1.1), run_time=0.6)
        self.play(*withdraw(J, pl), run_time=1.0)
        lt = T("lost here", 28, LRED, weight=BOLD).move_to([(J["xs"][0] + J["xs"][1]) / 2, -3.05, 0])
        self.play(FadeIn(lt, shift=UP * 0.1), run_time=0.3)
        self.at("local difference in activity")
        bl = bracket_under(J["xs"][2] - 0.4, J["xs"][7] + 0.4, -2.75, YELLOW)
        wk = T("working area", 28, YELLOW).move_to([(J["xs"][2] + J["xs"][7]) / 2, -3.15, 0])
        self.play(Create(bl), FadeIn(wk, shift=UP * 0.1), run_time=0.4)
        flash(self, J, range(2, 8), pl, rt=0.8)
        self.at("directs which sites go")
        ch = chip("a local difference in activity biases which sites go", YELLOW, size=28).move_to([0, 3.4, 0])
        self.play(FadeIn(ch, shift=DOWN * 0.2), run_time=0.6)
        self.finish()


class S22Lopoo(SpokenScene):
    def construct(self):
        d = culture()
        cr = T("Lo and Poo, 1991", 64, GOLD, font=TITLE_FONT)
        sub = T("Xenopus culture", 40, TEXT)
        cg = VGroup(cr, sub).arrange(DOWN, buff=0.25).move_to([0, 0.3, 0])
        self.play(FadeIn(cg, shift=DOWN * 0.1), run_time=0.5)
        self.at("smallest contest")
        self.play(cg.animate.scale(0.6).move_to([0, 3.2, 0]), FadeIn(d["muscle"]), FadeIn(d["mlab"]), run_time=0.4)
        self.play(FadeIn(d["n1"], scale=0.7), FadeIn(d["n2"], scale=0.7), run_time=0.3)
        self.play(Create(d["ax1"]), Create(d["ax2"]), run_time=0.4)
        self.play(FadeIn(d["b1"]), FadeIn(d["b2"]), FadeIn(d["r1"]), FadeIn(d["r2"]), run_time=0.3)
        sc = chip("the smallest contest:\ntwo inputs, one target", TEXT, size=30).move_to([0, 0.5, 0])
        self.play(FadeIn(sc, shift=UP * 0.1), run_time=0.4)
        self.at("cultures")
        self.play(Indicate(sub, color=YELLOW, scale_factor=1.15), run_time=0.8)
        self.finish()


def shown_culture(scene, labels=True):
    d = culture()
    scene.add(d["all"])
    if labels:
        scene.add(d["l1"], d["l2"])
    return d


class S23Cells(SpokenScene):
    def construct(self):
        d = culture()
        self.add(d["all"])
        self.at("two spinal neurons")
        self.play(FadeIn(d["l1"]), FadeIn(d["l2"]), Indicate(d["n1"], color=BLUE, scale_factor=1.2),
                  Indicate(d["n2"], color=ORANGE, scale_factor=1.2), run_time=0.7)
        self.at("one muscle cell")
        pn = resp_panel(0.8, [(ORANGE, [1.0, 1.0, 1.0], [0.42, 0.38, 0.4, 0.4])], "neuron 2's response (schematic)", ORANGE)
        self.play(Indicate(d["muscle"], color=GREY, scale_factor=1.03), FadeIn(pn["frame"]), FadeIn(pn["title"]),
                  FadeIn(pn["ylab"]), FadeIn(pn["tlab"]), FadeIn(pn["before"][0]), run_time=0.7)
        self.at("a burst")
        bi = burst_icon(BUX[0], 0.2)
        bl = T("burst", 24, YELLOW).next_to(bi, DOWN, buff=0.1)
        self.play(FadeIn(bi, scale=0.6), FadeIn(bl), run_time=0.35)
        for k in range(3):
            dd = Dot(radius=0.12, color=YELLOW).move_to([NX[0], 2.0, 0])
            self.add(dd)
            self.play(dd.animate.move_to([NX[0], -0.7, 0]), run_time=0.2, rate_func=linear)
            self.remove(dd)
        self.add(pn["mark"], pn["blab"])
        self.at("immediately weakened")
        self.play(Create(pn["mark"]), FadeIn(pn["blab"]), *[FadeIn(b) for b in pn["after"][0]],
                  d["b2"].animate.set_stroke(opacity=0.35).set_fill(opacity=0.2), run_time=0.6)
        self.at("other synapse")
        wk = T("weaker", 30, LRED, weight=BOLD).move_to([NX[1] + 1.75, -0.95, 0])
        self.play(FadeIn(wk, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S24Predict(SpokenScene):
    def construct(self):
        d = culture()
        self.add(d["all"], d["l1"], d["l2"])
        card = RoundedRectangle(corner_radius=0.2, width=3.6, height=2.6, stroke_color=YELLOW, stroke_width=4,
                                fill_color=YELLOW, fill_opacity=0.1).move_to([0, 1.0, 0])
        pr = T("Predict.", 34, YELLOW, weight=BOLD).move_to([0, 1.85, 0])
        qm = T("?", 90, YELLOW, weight=BOLD).move_to([0, 0.75, 0])
        self.play(FadeIn(card), FadeIn(pr), FadeIn(qm, scale=0.7), run_time=0.6)
        self.at("both neurons")
        b1 = burst_icon(BUX[0], 0.2)
        b2 = burst_icon(BUX[1], 0.2)
        l1 = T("burst", 24, YELLOW).next_to(b1, DOWN, buff=0.1)
        l2 = T("burst", 24, YELLOW).next_to(b2, DOWN, buff=0.1)
        self.play(FadeIn(b1, scale=0.6), FadeIn(b2, scale=0.6), FadeIn(l1), FadeIn(l2), run_time=0.5)
        self.at("burst together")
        for k in range(3):
            a = Dot(radius=0.12, color=YELLOW).move_to([NX[0], 2.0, 0])
            b = Dot(radius=0.12, color=YELLOW).move_to([NX[1], 2.0, 0])
            self.add(a, b)
            self.play(a.animate.move_to([NX[0], -0.7, 0]), b.animate.move_to([NX[1], -0.7, 0]), run_time=0.22, rate_func=linear)
            self.remove(a, b)
        self.finish()


class S25Pause(NarratedScene):
    def construct(self):
        d = culture()
        self.add(d["all"], d["l1"], d["l2"])
        card = RoundedRectangle(corner_radius=0.2, width=3.6, height=2.6, stroke_color=YELLOW, stroke_width=4,
                                fill_color=YELLOW, fill_opacity=0.1).move_to([0, 1.0, 0])
        pr = T("Predict.", 34, YELLOW, weight=BOLD).move_to([0, 1.85, 0])
        qm = T("?", 90, YELLOW, weight=BOLD).move_to([0, 0.75, 0])
        b1 = burst_icon(BUX[0], 0.2)
        b2 = burst_icon(BUX[1], 0.2)
        l1 = T("burst", 24, YELLOW).next_to(b1, DOWN, buff=0.1)
        l2 = T("burst", 24, YELLOW).next_to(b2, DOWN, buff=0.1)
        self.add(card, pr, qm, b1, b2, l1, l2)
        self.finish()


class S26Reveal(SpokenScene):
    def construct(self):
        d = culture()
        self.add(d["all"], d["l1"], d["l2"])
        b1 = burst_icon(BUX[0], 0.2)
        b2 = burst_icon(BUX[1], 0.2)
        l1 = T("burst", 24, YELLOW).next_to(b1, DOWN, buff=0.1)
        l2 = T("burst", 24, YELLOW).next_to(b2, DOWN, buff=0.1)
        self.add(b1, b2, l1, l2)
        pn = resp_panel(1.05, [(BLUE, [1.0, 1.0, 1.0], [0.97, 1.0, 0.98, 1.0]),
                               (ORANGE, [1.0, 1.0, 1.0], [0.96, 0.98, 1.0, 0.97])], "responses (schematic)", TEXT)
        self.add(pn["frame"], pn["title"], pn["ylab"], pn["tlab"], *pn["before"], pn["mark"], pn["blab"])
        self.at("largely absent")
        self.play(*[FadeIn(b) for row in pn["after"] for b in row], run_time=0.6)
        st = T("steady", 30, GREEN, weight=BOLD).move_to([1.4, pn["y0s"][1] + 1.25, 0])
        self.play(FadeIn(st, shift=LEFT * 0.1), run_time=0.4)
        self.at("neither input")
        ch = chip("activity at the same time seems to protect both", GREEN, size=28).move_to([0, -2.3, 0])
        self.play(FadeOut(d["mlab"]), FadeIn(ch, shift=UP * 0.2), run_time=0.6)
        self.finish()


class S27Hd(SpokenScene):
    def construct(self):
        d = culture()
        self.add(d["all"], d["l1"], d["l2"])
        self.at("heterosynaptic depression")
        a = chip("heterosynaptic depression", YELLOW, size=34).move_to([0, 3.3, 0])
        self.play(FadeIn(a, shift=DOWN * 0.2), d["b2"].animate.set_stroke(opacity=0.4).set_fill(opacity=0.2),
                  run_time=0.6)
        self.at("weakening within minutes")
        b = chip("weakening within minutes", TEXT, size=28).move_to([0, 2.35, 0])
        self.play(FadeIn(b, shift=DOWN * 0.2), run_time=0.6)
        self.at("fits rule 2")
        c2 = rule_card(2, 0, 0.8, False, False)
        self.play(FadeIn(c2, shift=UP * 0.2), run_time=0.7)
        self.at("it is not")
        # Opaque backing and high-contrast text remain through the final frame.
        row = T("functional weakening in culture, not structural removal", 26, TEXT, weight=BOLD)
        row.move_to([0, -0.43, 0])
        backing = RoundedRectangle(corner_radius=0.14, width=row.width + 0.4, height=row.height + 0.18,
                                    stroke_color=LRED, stroke_width=3,
                                    fill_color=BG, fill_opacity=1).move_to(row)
        badge = VGroup(backing, row).set_z_index(10)
        self.play(FadeIn(badge), run_time=0.25)
        self.play(Indicate(d["b2"], color=ORANGE, scale_factor=1.15), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------------------------
BX = [-3.25, -1.95, -0.65, 0.65, 1.95, 3.25]


def two_axons(weak_alpha=1.0):
    yb, top = 1.7, 0.5
    muscle = RoundedRectangle(corner_radius=0.2, width=8.6, height=1.5, stroke_color=GREY, stroke_width=3,
                              fill_color=GREY, fill_opacity=0.22).move_to([0, top - 0.75, 0])
    stemA = Line([-1.95, 3.5, 0], [-1.95, yb + 0.275, 0], color=BLUE, stroke_width=9)
    stemB = Line([1.95, 3.5, 0], [1.95, yb + 0.275, 0], color=ORANGE, stroke_width=9)
    sg = lambda a, b, c: Line([a + 0.475, yb, 0], [b - 0.475, yb, 0], color=c, stroke_width=9)
    segA = [sg(BX[0], BX[1], BLUE), sg(BX[1], BX[2], BLUE)]
    segB = [sg(BX[3], BX[4], ORANGE), sg(BX[4], BX[5], ORANGE)]
    bA = [RoundedRectangle(corner_radius=0.12, width=0.95, height=0.55, stroke_color=BLUE, stroke_width=3,
                           fill_color=BLUE, fill_opacity=0.55).move_to([x, yb, 0]) for x in BX[:3]]
    bB = [RoundedRectangle(corner_radius=0.12, width=0.95, height=0.55, stroke_color=ORANGE, stroke_width=3,
                           fill_color=ORANGE, fill_opacity=0.55).move_to([x, yb, 0]) for x in BX[3:]]
    rec = [RoundedRectangle(corner_radius=0.06, width=0.7, height=0.28, stroke_color=TEAL, stroke_width=3,
                            fill_color=TEAL, fill_opacity=0.6).move_to([x, top + 0.14, 0]) for x in BX]
    return dict(muscle=muscle, stemA=stemA, stemB=stemB, segA=segA, segB=segB, bA=bA, bB=bB, rec=rec, yb=yb, top=top)


class S28Buff(SpokenScene):
    def construct(self):
        d = two_axons()
        allm = VGroup(d["muscle"], d["stemA"], d["stemB"], *d["segA"], *d["segB"], *d["bA"], *d["bB"], *d["rec"])
        la = T("axon", 28, BLUE).move_to([-1.2, 3.3, 0])
        lb = T("axon", 28, ORANGE).move_to([2.7, 3.3, 0])
        mf = T("muscle fiber", 26, GREY).move_to([-3.0, -0.65, 0])
        self.add(allm, la, lb, mf)
        self.at("mice had one of two inputs")
        self.wait(0.1)
        self.at("made weaker")
        rl = T("reduced\ntransmitter release", 26, ORANGE).move_to([4.9, 2.75, 0])
        self.play(FadeIn(rl, shift=DOWN * 0.1), run_time=0.4)
        dots, tg = [], []
        for x in BX[:3]:
            for dx in (-0.25, 0, 0.25):
                dots.append(Dot(radius=0.08, color=WHITE).move_to([x + dx, d["yb"] - 0.4, 0]))
                tg.append([x + dx, d["top"] + 0.5, 0])
        for x in BX[3:]:
            dots.append(Dot(radius=0.08, color=WHITE).move_to([x, d["yb"] - 0.4, 0]))
            tg.append([x, d["top"] + 0.5, 0])
        self.add(*dots)
        self.play(*[dd.animate.move_to(p) for dd, p in zip(dots, tg)], run_time=0.7, rate_func=linear)
        big = [Rectangle(width=0.9, height=0.7, stroke_width=0, fill_color=YELLOW, fill_opacity=0.6).move_to([x, 0.1, 0])
               for x in BX[:3]]
        small = [Rectangle(width=0.9, height=0.22, stroke_width=0, fill_color=YELLOW, fill_opacity=0.6).move_to([x, 0.34, 0])
                 for x in BX[3:]]
        rs = T("smaller muscle response", 26, YELLOW).move_to([2.0, -1.4, 0])
        rb = T("larger response", 26, YELLOW).move_to([-1.95, -1.4, 0])
        self.play(*[FadeIn(b) for b in big + small], *[FadeOut(dd, scale=0.5) for dd in dots], FadeIn(rs), FadeIn(rb),
                  run_time=0.6)
        self.at("more powerful inputs")
        self.play(*[Indicate(b, color=GREEN, scale_factor=1.12) for b in d["bA"]], run_time=0.9)
        self.at("strongly favored")
        kp = T("the more powerful inputs were strongly favoured", 32, GREEN, weight=BOLD).move_to([0, -2.5, 0])
        sch = T("schematic", 28, GREY).move_to([0, -3.2, 0])
        self.play(FadeIn(kp, shift=DOWN * 0.1), FadeIn(sch), *[Indicate(b, color=GREEN, scale_factor=1.12) for b in d["bA"]],
                  run_time=0.8)
        self.finish()


class Balance(VGroup):
    pass


BAL_L, BAL_DROP, BAL_PAN = 4.3, 1.7, 3.8


def make_balance(cx=0.0, cy=0.4):
    pole = Line([cx, cy - 3.2, 0], [cx, cy, 0], color=GREY, stroke_width=9)
    base = Polygon([cx - 1.3, cy - 3.2, 0], [cx + 1.3, cy - 3.2, 0], [cx, cy - 2.4, 0], stroke_color=GREY,
                   stroke_width=4, fill_color=GREY, fill_opacity=0.35)
    beam = Line([cx - BAL_L, cy, 0], [cx + BAL_L, cy, 0], color=TEXT, stroke_width=9)
    pl = RoundedRectangle(corner_radius=0.1, width=BAL_PAN, height=0.2, stroke_color=GREY, stroke_width=3,
                          fill_color=GREY, fill_opacity=0.6)
    pr = RoundedRectangle(corner_radius=0.1, width=BAL_PAN, height=0.2, stroke_color=GREY, stroke_width=3,
                          fill_color=GREY, fill_opacity=0.6)
    strs = [Line(ORIGIN, ORIGIN, color=GREY, stroke_width=3) for _ in range(4)]
    return dict(pole=pole, base=base, beam=beam, pl=pl, pr=pr, strings=strs, cx=cx, cy=cy)


def layout_balance(B, a, left_items, right_items):
    """a > 0: left side down.  Items are (mobject, dx, h) resting on the pan."""
    cx, cy, L = B["cx"], B["cy"], BAL_L
    pl_end = np.array([cx - L * np.cos(a), cy - L * np.sin(a), 0])
    pr_end = np.array([cx + L * np.cos(a), cy + L * np.sin(a), 0])
    B["beam"].put_start_and_end_on(pl_end, pr_end)
    hw = BAL_PAN / 2 - 0.05
    for pan, end, strs in ((B["pl"], pl_end, B["strings"][:2]), (B["pr"], pr_end, B["strings"][2:])):
        ctr = end + np.array([0, -BAL_DROP, 0])
        pan.move_to(ctr)
        strs[0].put_start_and_end_on(end, ctr + np.array([-hw, 0, 0]))
        strs[1].put_start_and_end_on(end, ctr + np.array([hw, 0, 0]))
    for items, pan in ((left_items, B["pl"]), (right_items, B["pr"])):
        for m, dx, h in items:
            m.move_to(pan.get_center() + np.array([dx, 0.1 + h / 2, 0]))
    if "lab" in B:
        B["lab"].move_to(B["pr"].get_center() + np.array([0, -0.55, 0]))


def blk(w, h, color, op, text, size):
    under = Rectangle(width=w, height=h, stroke_width=0, fill_color=BG, fill_opacity=1)
    box = RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=op)
    g = VGroup(under, box)
    if text:
        g.add(T(text, size, TEXT).move_to(box))
    return g


class S29Bias(SpokenScene):
    def construct(self):
        B = make_balance(0.0, 1.0)
        strong = blk(2.8, 1.1, BLUE, 0.6, "stronger", 32)
        weak = blk(1.8, 0.9, ORANGE, 0.5, "weaker", 28)
        oth = [blk(0.75, 0.75, GREY, 0.5, "?", 30) for _ in range(3)]
        B["lab"] = T("other factors, unresolved", 28, GREY)
        left_items = [(strong, 0.0, 1.1)]
        right_items = [(weak, -1.0, 0.9), (oth[0], 0.45, 0.75), (oth[1], 1.3, 0.75), (oth[2], 0.88, 2.2)]
        a = ValueTracker(0.0)
        parts = VGroup(*B["strings"], B["pole"], B["base"], B["beam"], B["pl"], B["pr"], strong, weak, *oth)
        layout_balance(B, 0.0, left_items, right_items)
        parts.add_updater(lambda m: layout_balance(B, a.get_value(), left_items, right_items))
        self.add(parts, B["lab"])
        self.at("a bias")
        self.play(a.animate.set_value(0.2), run_time=0.6, rate_func=smooth)
        self.at("not a verdict")
        self.play(a.animate.set_value(0.0), run_time=0.5, rate_func=smooth)
        self.play(a.animate.set_value(0.13), run_time=0.5, rate_func=smooth)
        self.wait(3.5)
        self.finish()


def signal_group():
    """Active terminal (left) and quiet terminal (right) over one muscle; returns parts."""
    muscle = RoundedRectangle(corner_radius=0.25, width=11.4, height=1.4, stroke_color=GREY, stroke_width=3,
                              fill_color=GREY, fill_opacity=0.22).move_to([0, -2.45, 0])
    mlab = T("muscle", 28, GREY).move_to([0, -2.6, 0])
    rA = [RoundedRectangle(corner_radius=0.06, width=0.9, height=0.3, stroke_color=TEAL, stroke_width=3,
                           fill_color=TEAL, fill_opacity=0.6).move_to([x, -1.65, 0]) for x in (-3.9, -2.5)]
    rQ = [RoundedRectangle(corner_radius=0.06, width=0.9, height=0.3, stroke_color=TEAL, stroke_width=3,
                           fill_color=TEAL, fill_opacity=0.6).move_to([x, -1.65, 0]) for x in (2.5, 3.9)]
    stA = Line([-3.2, 3.4, 0], [-3.2, 1.0, 0], color=BLUE, stroke_width=9)
    stQ = Line([3.2, 3.4, 0], [3.2, 1.0, 0], color=BLUE, stroke_width=9)
    tA = RoundedRectangle(corner_radius=0.2, width=3.4, height=1.2, stroke_color=BLUE, stroke_width=3,
                          fill_color=BLUE, fill_opacity=0.55).move_to([-3.2, 0.5, 0])
    tQ = RoundedRectangle(corner_radius=0.2, width=3.4, height=1.2, stroke_color=BLUE, stroke_width=3,
                          fill_color=BLUE, fill_opacity=0.55).move_to([3.2, 0.5, 0])
    return dict(muscle=muscle, mlab=mlab, rA=rA, rQ=rQ, stA=stA, stQ=stQ, tA=tA, tQ=tQ)


def sig_all(d):
    return VGroup(d["muscle"], d["mlab"], *d["rA"], *d["rQ"], d["stA"], d["stQ"], d["tA"], d["tQ"])


class S30Signal(SpokenScene):
    def construct(self):
        d = signal_group()
        ta = T("active terminal", 28, YELLOW).move_to(d["tA"])
        tq = T("quiet terminal", 28, GREY).move_to(d["tQ"])
        d["tQ"].set_stroke(opacity=0.45).set_fill(opacity=0.25)
        d["stQ"].set_opacity(0.45)
        self.add(sig_all(d), ta, tq)
        self.at("what carries")
        qd = DashedLine([-0.4, -1.35, 0], [-0.4, 0.2, 0], color=YELLOW, stroke_width=5)
        q = T("?", 100, YELLOW, weight=BOLD).move_to([0.0, -0.55, 0])
        self.play(Create(qd), FadeIn(q, scale=0.6), run_time=0.7)
        self.at("in one model")
        cand = chip("one model: a candidate", TEXT, size=32, fill_opacity=0.3).move_to([0, 2.6, 0])
        self.play(FadeOut(qd), FadeOut(q), FadeIn(cand, shift=DOWN * 0.15), run_time=0.5)
        self.at("punishes inactive")
        pa = Arrow([3.2, -1.3, 0], [3.2, -0.2, 0], buff=0.0, color=RED, stroke_width=8, max_tip_length_to_length_ratio=0.35)
        pl = T("punish", 30, LRED, weight=BOLD).move_to([4.9, -0.75, 0])
        self.play(GrowArrow(pa), FadeIn(pl, shift=LEFT * 0.1), d["tQ"].animate.set_stroke(RED, opacity=0.8), run_time=0.5)
        self.at("protects")
        ga = Arrow([-3.2, -1.3, 0], [-3.2, -0.2, 0], buff=0.0, color=GREEN, stroke_width=8, max_tip_length_to_length_ratio=0.35)
        gl = T("protect", 30, GREEN, weight=BOLD).move_to([-4.95, -0.75, 0])
        self.play(GrowArrow(ga), FadeIn(gl, shift=RIGHT * 0.1), d["tA"].animate.set_stroke(GREEN), run_time=0.5)
        self.finish()


class S31Signal2(SpokenScene):
    def construct(self):
        d = signal_group()
        ta = T("active terminal", 28, YELLOW).move_to(d["tA"])
        tq = T("quiet terminal", 28, GREY).move_to(d["tQ"])
        d["tQ"].set_stroke(RED, opacity=0.8).set_fill(opacity=0.25)
        d["tA"].set_stroke(GREEN)
        d["stQ"].set_opacity(0.45)
        pa = Arrow([3.2, -1.3, 0], [3.2, -0.2, 0], buff=0.0, color=RED, stroke_width=8, max_tip_length_to_length_ratio=0.35)
        pl = T("punish", 30, LRED, weight=BOLD).move_to([4.9, -0.75, 0])
        ga = Arrow([-3.2, -1.3, 0], [-3.2, -0.2, 0], buff=0.0, color=GREEN, stroke_width=8, max_tip_length_to_length_ratio=0.35)
        gl = T("protect", 30, GREEN, weight=BOLD).move_to([-4.95, -0.75, 0])
        cand = chip("one model: a candidate", TEXT, size=32, fill_opacity=0.3).move_to([0, 2.6, 0])
        shapes = VGroup(d["muscle"], *d["rA"], *d["rQ"], d["stA"], d["stQ"], d["tA"], d["tQ"], ga, pa)
        texts = VGroup(d["mlab"], ta, tq, pl, gl, cand)
        self.add(shapes, texts)

        # the same model, redrawn smaller in the right half (arrows faded: only a candidate) so the plot can take the left
        cx = 3.9
        xa, xq = cx - 1.3, cx + 1.3
        s_mus = RoundedRectangle(corner_radius=0.2, width=5.4, height=0.9, stroke_color=GREY, stroke_width=3,
                                 fill_color=GREY, fill_opacity=0.22).move_to([cx, -0.55, 0])
        s_rec = [RoundedRectangle(corner_radius=0.06, width=0.7, height=0.26, stroke_color=TEAL, stroke_width=3,
                                  fill_color=TEAL, fill_opacity=0.6).move_to([x, -0.1 + 0.13, 0])
                 for x in (xa - 0.45, xa + 0.45, xq - 0.45, xq + 0.45)]
        s_stA = Line([xa, 3.3, 0], [xa, 1.9, 0], color=BLUE, stroke_width=8)
        s_stQ = Line([xq, 3.3, 0], [xq, 1.9, 0], color=BLUE, stroke_width=8).set_opacity(0.45)
        s_tA = RoundedRectangle(corner_radius=0.16, width=2.1, height=0.8, stroke_color=GREEN, stroke_width=3,
                                fill_color=BLUE, fill_opacity=0.55).move_to([xa, 1.5, 0])
        s_tQ = RoundedRectangle(corner_radius=0.16, width=2.1, height=0.8, stroke_color=RED, stroke_width=3,
                                fill_color=BLUE, fill_opacity=0.25).move_to([xq, 1.5, 0])
        s_tQ.set_stroke(opacity=0.8)
        s_ga = Arrow([xa, 0.2, 0], [xa, 1.0, 0], buff=0.0, color=GREEN, stroke_width=7, max_tip_length_to_length_ratio=0.35)
        s_pa = Arrow([xq, 0.2, 0], [xq, 1.0, 0], buff=0.0, color=RED, stroke_width=7, max_tip_length_to_length_ratio=0.35)
        s_ga.set_opacity(0.3)
        s_pa.set_opacity(0.3)
        small = VGroup(s_mus, *s_rec, s_stA, s_stQ, s_tA, s_tQ, s_ga, s_pa)
        c_a = T("active", 24, YELLOW).move_to(s_tA)
        c_q = T("quiet", 24, GREY).move_to(s_tQ)
        c_pr = T("protect", 24, GREEN).set_opacity(0.4).move_to([xa - 0.95, 0.6, 0])
        c_pu = T("punish", 24, LRED).set_opacity(0.4).move_to([xq + 0.95, 0.6, 0])
        c_cand = T("one model: a candidate", 26, TEXT, weight=BOLD).move_to([cx, -1.55, 0])
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 1.1, 0.5], x_length=6.2, y_length=4.4, tips=False,
                  axis_config={"include_numbers": False, "stroke_color": GREY, "stroke_width": 3}).move_to([-2.9, 0.6, 0])
        xl = T("time", 26, GREY).next_to(ax, DOWN, buff=0.12).align_to(ax, RIGHT)
        yl = T("synapses eliminated", 26, GREY).rotate(PI / 2).next_to(ax, LEFT, buff=0.15)
        sch = T("schematic", 30, TEXT).move_to([-2.9, 3.35, 0])

        def logi(t0, w=0.7):
            return lambda t: 1.0 / (1.0 + np.exp(-(t - t0) / w))

        wt = ax.plot(logi(3.4), x_range=[0, 10], color=GREY, stroke_width=7)
        pk = ax.plot(logi(5.8), x_range=[0, 10], color=PINK, stroke_width=7)
        bd = DashedVMobject(ax.plot(logi(3.4), x_range=[0, 10], color=PINK, stroke_width=7), num_dashes=40)

        def legend(row, color, text, dashed=False):
            y = -2.5 - 0.42 * row
            ln = Line([-6.2, y, 0], [-5.5, y, 0], color=color, stroke_width=7)
            if dashed:
                ln = DashedVMobject(ln, num_dashes=5)
            tx = T(text, 24, color).next_to(ln, RIGHT, buff=0.2)
            return VGroup(ln, tx)

        l0 = legend(0, GREY, "normal mice")
        l1 = legend(1, PINK, "without one form of PKC")
        l2 = legend(2, PINK, "without BDNF, or without p75", dashed=True)
        self.play(ReplacementTransform(shapes, small), FadeOut(texts), FadeIn(VGroup(c_a, c_q, c_pr, c_pu, c_cand)),
                  FadeIn(ax), FadeIn(xl), FadeIn(yl), FadeIn(sch), Create(wt), FadeIn(l0), run_time=0.9)
        self.at("pkc")
        self.play(FadeIn(l1), run_time=0.3)
        self.at("elimination in mice is delayed")
        self.play(Create(pk), run_time=1.3)
        pkl = T("PKC", 26, PINK, weight=BOLD).move_to(ax.c2p(8.2, 0.35))
        self.play(FadeIn(pkl), run_time=0.3)
        self.at("still completes")
        top = DashedLine(ax.c2p(0, 1.0), ax.c2p(10, 1.0), color=GREY, stroke_width=2).set_opacity(0.6)
        done = T("still completes", 28, GREEN, weight=BOLD).move_to(ax.c2p(7.6, 1.0) + UP * 0.32)
        self.play(Create(top), FadeIn(done), run_time=0.6)
        self.at("mice lacking")
        self.play(FadeOut(done), FadeIn(l2), run_time=0.4)
        self.at("eliminates synapses on schedule")
        self.play(Create(bd), run_time=1.2)
        self.at("on schedule")
        os_ = T("on schedule", 28, GREEN, weight=BOLD).move_to(ax.c2p(2.3, 0.82))
        bl = T("BDNF, p75", 24, PINK, weight=BOLD).move_to(ax.c2p(2.0, 0.65))
        self.play(FadeIn(os_), FadeIn(bl), run_time=0.4)
        self.at("none of these")
        qq = T("signal?", 28, YELLOW, weight=BOLD).move_to([cx, 0.6, 0])
        unproven = T("none shown to be the signal", 26, YELLOW, weight=BOLD).move_to([cx, -1.55, 0])
        self.play(FadeOut(os_), FadeIn(qq), ReplacementTransform(c_cand, unproven), run_time=0.5)
        self.at("indispensable signal")
        tg2 = chip("affecting the pace and being\nrequired are different tests", YELLOW, size=26).move_to([cx, -2.75, 0])
        self.play(FadeIn(tg2, shift=UP * 0.2), run_time=0.6)
        self.finish()


def closing_cards(dim=False):
    f1 = RoundedRectangle(corner_radius=0.2, width=6.1, height=4.0, stroke_color=PURPLE, stroke_width=4.5,
                          fill_color=PURPLE, fill_opacity=0.1).move_to([-3.3, -0.3, 0])
    f2 = RoundedRectangle(corner_radius=0.2, width=6.1, height=4.0, stroke_color=GOLD, stroke_width=4.5,
                          fill_color=GOLD, fill_opacity=0.1).move_to([3.3, -0.3, 0])
    return f1, f2


class S32Take(SpokenScene):
    def construct(self):
        f1, f2 = closing_cards()
        t1 = [T("Silence alone does", 32, TEXT), T("not remove a synapse.", 32, TEXT)]
        t2 = [T("Being quieter than its", 32, TEXT), T("neighbours puts it at risk.", 32, TEXT)]
        g1 = VGroup(*t1).arrange(DOWN, buff=0.16).move_to([-3.3, 0.85, 0])
        g2 = VGroup(*t2).arrange(DOWN, buff=0.16).move_to([3.3, 0.85, 0])
        i1 = rule_icon(1, 1.7, 1.2).move_to([-3.3, -0.75, 0])
        i2 = rule_icon(2, 1.3, 1.1).move_to([3.3, -0.75, 0])
        self.add(f1, f2, i1, i2)
        self.at("silence alone")
        ring = Circle(radius=0.55, stroke_color=GREEN, stroke_width=6).move_to(i1.target)
        stay = T("stays", 30, GREEN, weight=BOLD).move_to([-3.3, -1.7, 0])
        self.play(FadeIn(g1, shift=UP * 0.1), Create(ring), FadeIn(stay, shift=UP * 0.1), run_time=0.8)
        self.at("being quieter")
        self.play(FadeIn(g2, shift=UP * 0.1), run_time=0.7)
        self.play(Indicate(i2.sites[1], color=YELLOW, scale_factor=1.3), run_time=0.7)
        self.at("puts it at risk", lead=0.1)
        risk = Circle(radius=0.5, stroke_color=RED, stroke_width=9).move_to(i2.target)
        rl = T("at risk", 30, LRED, weight=BOLD).move_to([3.3, -1.7, 0])
        self.play(FadeIn(risk), FadeIn(rl), i2.target.animate.set_stroke(RED), run_time=0.25)
        self.finish()


class S33End(EndCard):
    LINE = "Being quieter than neighbours, not silence alone, puts a synapse at risk."
