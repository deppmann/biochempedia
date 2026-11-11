"""Chapter 2: what keeps a cell a stem cell (niche signals). Same look as chapter 1.

Extra colours: ORANGE Wnt, PURPLE BMP, PANETH pink, STROMA sand.

Chapter 1 header follows.


COLOR MAP
  BLUE   stem cells before lineage marking
  GREY   crypt, epithelium, differentiated daughters
  GREEN  permanent lineage mark / one Confetti clone
  YELLOW tamoxifen pulse / one Confetti clone
  RED    loss, short-lived outcome / one Confetti clone
  TEAL   niche-supported pool / cyan Confetti clone
  GOLD   questions and the chance spinner

All crypt scenes use the same geometry.  The picture is a simplified schematic;
no curve or quantitative readout is invented.
"""
from bp_style import *  # noqa: F401,F403


CX = -2.35
CRYPT_R = 2.15
CRYPT_CC = -1.0
CRYPT_TOP = 3.15
BASE_ANGLES = (200, 235, 270, 305, 340)
CONFETTI = [GREEN, YELLOW, RED, TEAL, GREEN]


def cell(color=BLUE, radius=0.38, opacity=0.68, stroke=3.5):
    return Circle(radius=radius, color=color, stroke_width=stroke,
                  fill_color=color, fill_opacity=opacity)


def base_positions():
    return [np.array([CX + 1.48 * np.cos(a * DEGREES),
                      CRYPT_CC + 1.48 * np.sin(a * DEGREES), 0])
            for a in BASE_ANGLES]


def crypt_shape():
    """Large, high-ink U-shaped pocket, open at the top."""
    back = VGroup(
        Rectangle(width=2 * CRYPT_R, height=CRYPT_TOP - CRYPT_CC,
                  stroke_width=0, fill_color=GREY, fill_opacity=0.20)
        .move_to([CX, (CRYPT_TOP + CRYPT_CC) / 2, 0]),
        Circle(radius=CRYPT_R, stroke_width=0, fill_color=GREY, fill_opacity=0.20)
        .move_to([CX, CRYPT_CC, 0]),
    ).set_z_index(-5)
    walls = VGroup(
        Line([CX - CRYPT_R, CRYPT_TOP, 0], [CX - CRYPT_R, CRYPT_CC, 0],
             color=GREY, stroke_width=6),
        Arc(radius=CRYPT_R, start_angle=PI, angle=PI,
            arc_center=[CX, CRYPT_CC, 0], color=GREY, stroke_width=6),
        Line([CX + CRYPT_R, CRYPT_CC, 0], [CX + CRYPT_R, CRYPT_TOP, 0],
             color=GREY, stroke_width=6),
    )
    return VGroup(back, walls)


def moving_stream(color=GREY, green_patch=False, speed=0.34):
    """A continuously renewing stream; the wrap makes every spoken hold alive."""
    xs = (-1.18, -0.38, 0.40, 1.15, -0.78, 0.05, 0.82)
    ys = (-0.20, 0.35, 0.86, 1.35, 1.82, 2.32, 2.78)
    dots = VGroup()
    for i, (dx, y) in enumerate(zip(xs, ys)):
        c = GREEN if green_patch and i in (1, 3, 5) else color
        d = cell(c, 0.29 if i % 2 else 0.32, 0.48, 2.8).move_to([CX + dx, y, 0])
        d.vy = speed * (0.82 + 0.08 * (i % 4))

        def rise(m, dt):
            m.shift(UP * m.vy * dt)
            if m.get_y() > CRYPT_TOP + 0.42:
                m.move_to([m.get_x(), -0.25, 0])

        d.add_updater(rise)
        dots.add(d)
    return dots


def simplified_label(text="simplified schematic"):
    return T(text, 28, TEXT, weight=BOLD).move_to([3.65, -3.42, 0])


def pool_bracket(label=True):
    y = -3.16
    line = VGroup(
        Line([CX - 1.92, y, 0], [CX + 1.92, y, 0], color=TEAL, stroke_width=6),
        Line([CX - 1.92, y, 0], [CX - 1.92, y + 0.24, 0], color=TEAL, stroke_width=6),
        Line([CX + 1.92, y, 0], [CX + 1.92, y + 0.24, 0], color=TEAL, stroke_width=6),
    )
    if label:
        line.add(T("stem-cell pool", 28, TEAL, weight=BOLD).next_to(line, DOWN, buff=0.08))
    return line


def niche_glow():
    return Ellipse(width=4.05, height=1.65, color=TEAL, stroke_width=3,
                   fill_color=TEAL, fill_opacity=0.12).move_to([CX, -2.25, 0]).set_z_index(-2)


def crypt_world(colors=None, stream_color=GREY, green_patch=False,
                show_simple=True, bracket=False, niche=False):
    colors = colors or [BLUE] * 5
    cr = crypt_shape()
    cells = VGroup(*[cell(c).move_to(p) for c, p in zip(colors, base_positions())])
    flow = moving_stream(stream_color, green_patch)
    items = [cr]
    if niche:
        items.append(niche_glow())
    items.extend([flow, cells])
    if bracket:
        items.append(pool_bracket())
    if show_simple:
        items.append(simplified_label())
    return VGroup(*items), cells, flow




# ---------------------------------------------------------------- chapter 2 additions
ORANGE = "#F08A3C"
PURPLE = "#9B6BD6"
PANETH = "#E58FB5"
STROMA = "#C9A27A"
PALE = "#D9C7A0"
LESSON_TITLE = "Stem Cells and Tissue Renewal"
WNT_POS = [4.35, -1.2, 0]
BMP_POS = [4.35, 2.5, 0]


def _u_shape(ytop):
    pts = [[CX + CRYPT_R * np.cos(a), CRYPT_CC + CRYPT_R * np.sin(a), 0]
           for a in np.linspace(PI, 2 * PI, 24)]
    pts += [[CX + CRYPT_R, ytop, 0], [CX - CRYPT_R, ytop, 0]]
    return Polygon(*pts, stroke_width=0)


def fields(vis=1.0):
    """Schematic Wnt (base) and BMP (top) colour fields that shimmer; not measured."""
    wnt = VGroup(*[_u_shape(yt).set_fill(ORANGE, 0.1) for yt in (-1.0, -0.3, 0.4, 1.1, 1.8)])
    bmp = VGroup(*[Rectangle(width=2 * CRYPT_R, height=CRYPT_TOP - yb, stroke_width=0)
                   .move_to([CX, (CRYPT_TOP + yb) / 2, 0]).set_fill(PURPLE, 0.1)
                   for yb in (2.2, 1.5, 0.8, 0.1, -0.6)])
    for g in (wnt, bmp):
        for k, l in enumerate(g):
            l.k = k
    f = VGroup(wnt, bmp)
    f.set_z_index(-4)
    f.wnt, f.bmp = wnt, bmp
    f.vis, f.wb, f.bb = ValueTracker(vis), ValueTracker(1), ValueTracker(1)
    st = [0.0]

    def up(m, dt):
        st[0] += dt
        for g, b in ((m.wnt, m.wb), (m.bmp, m.bb)):
            for l in g:
                l.set_fill(opacity=0.1 * m.vis.get_value() * b.get_value()
                           * (1 + 0.22 * np.sin(1.3 * st[0] + 1.1 * l.k)))
    f.add_updater(up)
    up(f, 0)
    return f


def pulse(m, base=0.12, amp=0.05, sp=2.0):
    st = [0.0]

    def up(mm, dt):
        st[0] += dt
        mm.set_fill(opacity=base + amp * np.sin(sp * st[0]))
    m.add_updater(up)


def ring_on(mob, color=GOLD, r=0.56):
    ring = Circle(radius=r, color=color, stroke_width=6)
    ring.add_updater(lambda m: m.move_to(mob))
    ring.move_to(mob)
    return ring


def ws_labels():
    return (T("Wnt", 40, ORANGE, weight=BOLD).move_to(WNT_POS),
            T("BMP", 40, PURPLE, weight=BOLD).move_to(BMP_POS))


def sil(color=GREY):
    return RoundedRectangle(width=0.42, height=0.66, corner_radius=0.12, color=color,
                            fill_color=color, fill_opacity=0.5, stroke_width=3)


P_DISP = np.array([CX + 0.45, 0.35, 0])


def after_displace(scene, vis=1.0, ring=True):
    """Carried state at the end of s05: one blue cell has been displaced up, a neighbour filled its place."""
    world, cells, flow = crypt_world()
    f = fields(vis)
    bp = base_positions()
    cells[3].move_to(P_DISP)
    cells[4].move_to(bp[3])
    scene.add(f, world)
    wl, bl = ws_labels()
    scene.add(wl, bl)
    rg = ring_on(cells[3]) if ring else None
    if rg is not None:
        scene.add(rg)
    return world, cells, flow, f, rg, wl, bl


class S01Link(SpokenScene, TitleCard):
    LESSON = LESSON_TITLE
    TITLE = "What Keeps a Cell a Stem Cell?"

    def construct(self):
        world, cells, flow = crypt_world()
        self.add(world)
        q = T("What keeps a cell\nin the stem-cell state?", 36, GOLD, weight=BOLD,
              line_spacing=0.9).move_to([3.5, 1.6, 0])
        self.at("what keeps a cell")
        self.play(FadeIn(q, shift=UP * 0.15), run_time=0.9)
        self.at("chapter 1 showed")
        self.play(LaggedStart(*[c.animate.set_color(YELLOW).set_fill(YELLOW, 0.72) for c in cells],
                              lag_ratio=0.25), run_time=1.8)
        self.at("come and go")
        self.play(LaggedStart(*[c.animate.set_color(BLUE).set_fill(BLUE, 0.68) for c in cells],
                              lag_ratio=0.2), run_time=1.4)
        self.at("but the crypt base held")
        br = pool_bracket()
        self.play(FadeIn(br), run_time=0.8)
        self.at("only a few positions")
        self.play(Indicate(cells, color=TEAL, scale_factor=1.06), run_time=1.2)
        self.at("what limits them")
        q2 = T("What limits\nthe positions?", 38, GOLD, weight=BOLD, line_spacing=0.9).move_to([3.5, 1.2, 0])
        self.play(FadeOut(q, shift=UP * 0.1), FadeIn(q2, shift=UP * 0.1), run_time=0.8)
        self.at("signals drawn in")
        self.play(Indicate(world[0], color=TEAL, scale_factor=1.02), run_time=1.0)
        self.finish()


class S02Title(TitleCard):
    LESSON = LESSON_TITLE
    TITLE = "What Keeps a Cell a Stem Cell?"

    def construct(self):
        world, cells, flow = crypt_world()
        self.add(world)
        title = T("What Keeps a Cell\na Stem Cell?", 38, font=TITLE_FONT, weight=BOLD,
                  line_spacing=0.92).move_to([3.4, 2.2, 0])
        panel = BackgroundRectangle(title, color=BG, fill_opacity=0.88, buff=0.22)
        self.play(FadeIn(panel), FadeIn(title), run_time=0.45)
        corner = T("NICHE SIGNALS", 28, TEAL, weight=BOLD).move_to([3.75, 3.28, 0])
        self.play(FadeOut(VGroup(panel, title), shift=UP * 0.08), run_time=0.28)
        self.play(FadeIn(corner, shift=UP * 0.08), run_time=0.32)
        self.finish()


class S03Niche(SpokenScene):
    def construct(self):
        world, cells, flow = crypt_world(niche=True)
        glow = world[1]
        self.add(world[0], flow, cells, world[-1])
        self.at("start with the neighborhood")
        self.play(FadeIn(glow), run_time=1.4)
        pulse(glow)
        self.at("a stem cell niche")
        niche = T("niche", 40, TEAL, weight=BOLD).move_to([3.7, 0.4, 0])
        la = Arrow([2.6, 0.3, 0], [-0.4, -1.45, 0], buff=0, color=TEAL, stroke_width=4, tip_length=0.2)
        self.play(FadeIn(niche), GrowArrow(la), run_time=0.9)
        self.at("in the mouse gut")
        pan = VGroup()
        for a in (217.5, 252.5, 287.5, 322.5):
            c = np.array([CX + 1.82 * np.cos(a * DEGREES), CRYPT_CC + 1.82 * np.sin(a * DEGREES), 0])
            sq = RoundedRectangle(width=0.46, height=0.46, corner_radius=0.08, color=PANETH,
                                  fill_color=PANETH, fill_opacity=0.55, stroke_width=3).move_to(c)
            gr = VGroup(*[Dot(c + np.array([dx, dy, 0]), radius=0.045, color=TEXT)
                          for dx, dy in ((-0.1, 0.08), (0.08, 0.1), (0.0, -0.1))])
            pan.add(VGroup(sq, gr))
        self.play(LaggedStart(*[FadeIn(p, scale=0.7) for p in pan], lag_ratio=0.2), run_time=1.1)
        self.at("paneth cells")
        pl = T("Paneth cells", 34, PANETH, weight=BOLD).move_to([3.9, -1.0, 0])
        pa = Arrow([2.1, -1.05, 0], [-0.7, -2.0, 0], buff=0, color=PANETH, stroke_width=4, tip_length=0.2)
        self.play(FadeIn(pl), GrowArrow(pa), Indicate(pan, color=PANETH, scale_factor=1.12), run_time=1.0)
        self.at("stromal cells")
        st = VGroup()
        for a in range(195, 346, 15):
            c = np.array([CX + 2.42 * np.cos(a * DEGREES), CRYPT_CC + 2.42 * np.sin(a * DEGREES), 0])
            st.add(Ellipse(width=0.72, height=0.28, color=STROMA, fill_color=STROMA, fill_opacity=0.55,
                           stroke_width=3).rotate((a + 90) * DEGREES).move_to(c))
        self.play(LaggedStart(*[FadeIn(s) for s in st], lag_ratio=0.1), run_time=1.0)
        sl = T("stromal cells", 34, STROMA, weight=BOLD).move_to([3.9, -2.3, 0])
        sa = Arrow([2.2, -2.3, 0], [0.0, -2.2, 0], buff=0, color=STROMA, stroke_width=4, tip_length=0.2)
        self.play(FadeIn(sl), GrowArrow(sa), run_time=0.7)
        self.at("both contribute")
        arrows = VGroup()
        for a in (235, 270, 305):
            d = np.array([np.cos(a * DEGREES), np.sin(a * DEGREES), 0])
            o = np.array([CX, CRYPT_CC, 0])
            arrows.add(Arrow(o + 2.3 * d, o + 1.9 * d, buff=0, color=TEAL, stroke_width=5, tip_length=0.16))
        self.play(FadeIn(arrows), run_time=0.5)
        arrows.add_updater(lambda m, dt, s=[0.0]: (s.__setitem__(0, s[0] + dt),
                                                   m.set_opacity(0.65 + 0.35 * np.sin(5 * s[0]))))
        self.wait(1.2)
        self.finish()


class S04Gradient(SpokenScene):
    def construct(self):
        world, cells, flow = crypt_world()
        f = fields(0.0)
        self.add(f, world)
        self.at("two kinds of signal")
        strips = VGroup(*[Rectangle(width=0.28, height=0.25, stroke_width=0,
                                    fill_color=interpolate_color(ManimColor(ORANGE), ManimColor(PURPLE), i / 23),
                                    fill_opacity=0.9).move_to([0.85, -2.9 + 0.2523 * i, 0]) for i in range(24)])
        gl = T("schematic gradient", 28, TEXT, weight=BOLD).rotate(PI / 2).move_to([1.5, 0.0, 0])
        self.play(f.vis.animate.set_value(1.0), FadeIn(strips), FadeIn(gl), run_time=2.6)
        self.at("w and t")
        wl = T("Wnt", 40, ORANGE, weight=BOLD).move_to(WNT_POS)
        self.play(FadeIn(wl), f.wb.animate.set_value(1.7), run_time=1.0)
        self.at("promotes self renewal")
        ws = T("promotes self-renewal", 28, ORANGE).move_to([4.35, -1.8, 0])
        self.play(FadeIn(ws), run_time=0.7)
        self.at("r spondin")
        also = T("also: R-spondin,\nEGF, Notch", 28, TEXT, line_spacing=0.9).move_to([4.1, -2.65, 0])
        self.play(FadeIn(also), f.wb.animate.set_value(1.0), run_time=0.9)
        self.at("bmp is strongest")
        bl = T("BMP", 40, PURPLE, weight=BOLD).move_to(BMP_POS)
        self.play(FadeIn(bl), f.bb.animate.set_value(1.7), run_time=1.0)
        self.at("among differentiated cells")
        self.play(Indicate(bl, color=PURPLE, scale_factor=1.08), run_time=0.9)
        self.at("suppresses self renewal")
        bs = T("suppresses self-renewal", 28, PURPLE).move_to([4.35, 1.85, 0])
        self.play(FadeIn(bs), f.bb.animate.set_value(1.0), run_time=0.8)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        world, cells, flow = crypt_world()
        f = fields()
        wl, bl = ws_labels()
        self.add(f, world, wl, bl)
        bp = base_positions()
        self.at("a blue stem cell is displaced")
        self.play(cells[3].animate.move_to(P_DISP), cells[4].animate.move_to(bp[3]), run_time=2.4)
        self.at("away from the strongest")
        rg = ring_on(cells[3])
        self.play(Create(rg), run_time=0.8)
        self.play(cells[3].animate.shift(UP * 0.12), run_time=1.5)
        self.at("what do you expect")
        q = T("What do you\nexpect it to do?", 38, GOLD, weight=BOLD, line_spacing=0.9).move_to([4.2, 0.6, 0])
        self.play(FadeIn(q, shift=UP * 0.15), run_time=0.9)
        self.finish()


class S06Pause(Scene):
    def construct(self):
        self.camera.background_color = BG
        world, cells, flow, f, rg, wl, bl = after_displace(self)
        cells[3].shift(UP * 0.12)
        q = T("What do you\nexpect it to do?", 38, GOLD, weight=BOLD, line_spacing=0.9).move_to([4.2, 0.6, 0])
        self.add(q)
        cells[3].add_updater(lambda m, dt: m.shift(UP * 0.06 * dt))
        self.wait(4.5)


class S07Reveal(SpokenScene):
    def construct(self):
        world, cells, flow, f, rg, wl, bl = after_displace(self)
        disp = cells[3]
        self.at("as cells move up")
        self.play(disp.animate.move_to([CX + 0.3, 1.9, 0]), run_time=3.2)
        self.at("leave the stem cell state")
        s = sil().move_to(disp)
        self.play(ReplacementTransform(disp, s), FadeOut(rg), run_time=1.1)

        def rise(m, dt):
            m.shift(UP * 0.34 * dt)
            if m.get_y() > CRYPT_TOP + 0.4:
                m.set_opacity(0)
        s.add_updater(rise)
        self.at("less wnt reaches them")
        lw = VGroup(Arrow(UP * 0.3, DOWN * 0.3, buff=0, color=ORANGE, stroke_width=6, tip_length=0.2),
                    T("less Wnt", 34, ORANGE, weight=BOLD)).arrange(RIGHT, buff=0.2).move_to([4.0, 0.9, 0])
        self.play(FadeIn(lw), f.wb.animate.set_value(0.6), run_time=0.8)
        self.at("more bmp")
        mb = VGroup(Arrow(DOWN * 0.3, UP * 0.3, buff=0, color=PURPLE, stroke_width=6, tip_length=0.2),
                    T("more BMP", 34, PURPLE, weight=BOLD)).arrange(RIGHT, buff=0.2).move_to([4.0, 0.1, 0])
        self.play(FadeIn(mb), f.bb.animate.set_value(1.6), run_time=0.8)
        self.at("the cell that remains")
        self.play(FadeOut(VGroup(lw, mb)), f.wb.animate.set_value(1.0), f.bb.animate.set_value(1.0), run_time=0.7)
        keep = T("keeps its support", 34, TEAL, weight=BOLD).move_to([4.3, 0.1, 0])
        self.play(Indicate(cells[2], color=TEAL, scale_factor=1.25), FadeIn(keep), run_time=1.2)
        self.at("so the positions")
        br = pool_bracket()
        self.play(FadeOut(keep), FadeIn(br), f.wb.animate.set_value(1.8), run_time=1.0)
        self.at("support is local")
        loc = T("local support", 38, TEAL, weight=BOLD).move_to([4.3, 0.4, 0])
        self.play(FadeIn(loc), Indicate(br, color=TEAL, scale_factor=1.03), run_time=1.0)
        self.finish()


class S08Idea(SpokenScene):
    def construct(self):
        world, cells, flow = crypt_world()
        f = fields()
        wl, bl = ws_labels()
        self.add(f, world, wl, bl)
        self.at("here is the key idea")
        zone = DashedVMobject(Ellipse(width=3.9, height=1.9, color=ORANGE, stroke_width=5)).move_to([CX, -2.1, 0])
        self.play(Create(zone), f.wb.animate.set_value(1.5), run_time=1.4)
        self.at("being a stem cell looks")
        halo = ring_on(cells[4], TEAL, 0.52)
        self.play(Create(halo), run_time=0.8)
        self.at("more like a state")
        st = T("state", 40, TEAL, weight=BOLD).move_to([3.9, -0.2, 0])
        a1 = Arrow([2.9, -0.3, 0], [-0.5, -1.3, 0], buff=0, color=TEAL, stroke_width=4, tip_length=0.2)
        self.play(FadeIn(st), GrowArrow(a1), run_time=0.9)
        self.at("local signals support")
        sup = T("supported by niche", 32, ORANGE, weight=BOLD).move_to([4.2, -2.3, 0])
        a2 = DashedLine([2.2, -2.1, 0], [-0.5, -1.6, 0], color=ORANGE, stroke_width=5).add_tip(tip_length=0.2)
        self.play(FadeIn(sup), Create(a2), run_time=1.0)
        self.at("chapter 1's clones")
        bp = base_positions()
        br = pool_bracket()
        self.play(FadeOut(VGroup(st, a1, sup, a2, halo)), f.wb.animate.set_value(1.0), FadeIn(br),
                  *[c.animate.set_color(col).set_fill(col, 0.72) for c, col in zip(cells, CONFETTI)], run_time=1.0)
        self.at("competed for places")
        self.play(*[cells[i].animate.move_to(bp[(i + 1) % 5]) for i in range(5)], run_time=1.1)
        self.at("inside that support")
        self.play(*[cells[i].animate.move_to(bp[(i + 2) % 5]) for i in range(5)], run_time=1.1)
        self.at("a winner holds")
        place = T("a place,\nnot a permanent title", 34, TEXT, weight=BOLD, line_spacing=0.9).move_to([4.2, 0.3, 0])
        pr = ring_on(cells[1], TEAL, 0.55)
        self.play(FadeIn(place), Create(pr), run_time=1.0)
        self.play(Indicate(cells[1], color=YELLOW, scale_factor=1.25), run_time=1.4)
        self.finish()


class S09Organoid(SpokenScene):
    def construct(self):
        world, cells, flow = crypt_world()
        f = fields()
        self.add(f, world)
        D = np.array([3.9, 0.35, 0])
        LBL = [3.9, -2.6, 0]
        dish = Circle(radius=1.95, color=TEXT, stroke_width=5, fill_color=TEXT, fill_opacity=0.05).move_to(D)
        self.at("a dish tests")
        self.play(Create(dish), run_time=1.0)
        self.at("single sorted")
        c0 = cells[1]
        path = ArcBetweenPoints(c0.get_center(), D, angle=-0.9)
        self.play(MoveAlongPath(c0, path), run_time=1.6)
        self.at("grew into organoids")
        b = c0.copy()
        self.add(b)
        self.play(c0.animate.scale(0.7).shift(LEFT * 0.25), b.animate.scale(0.7).shift(RIGHT * 0.25), run_time=0.7)
        c, d = c0.copy(), b.copy()
        self.add(c, d)
        self.play(c0.animate.shift(UP * 0.2), b.animate.shift(UP * 0.2), c.animate.shift(DOWN * 0.2),
                  d.animate.shift(DOWN * 0.2), run_time=0.7)
        self.at("matrix")
        gel = Circle(radius=1.82, color=PALE, stroke_width=0, fill_color=PALE, fill_opacity=0.16).move_to(D)
        gl = T("matrix", 32, PALE, weight=BOLD).move_to(LBL)
        self.play(FadeIn(gel), FadeIn(gl), run_time=0.8)
        self.at("added factors")
        drops = VGroup(*[Dot([x, 2.8, 0], radius=0.14, color=TEAL) for x in (3.0, 3.9, 4.8)])
        fl = T("added factors", 32, TEAL, weight=BOLD).move_to([3.9, 3.35, 0])
        self.play(FadeIn(drops), FadeIn(fl), run_time=0.5)
        self.play(drops.animate.shift(DOWN * 2.1).set_opacity(0), run_time=0.8)
        self.remove(drops)
        N = 10
        ringc = VGroup(*[cell(BLUE, 0.27, 0.6, 2.5).move_to(D + 1.0 * np.array([np.cos(2 * PI * i / N), np.sin(2 * PI * i / N), 0]))
                         for i in range(N)])
        lumen = Circle(radius=0.75, color=TEXT, stroke_width=0, fill_color=TEXT, fill_opacity=0.1).move_to(D)
        self.play(ReplacementTransform(VGroup(c0, b, c, d), ringc), FadeIn(lumen), FadeOut(fl), run_time=1.0)
        self.at("organoids are")
        ol = T("organoid (schematic)", 32, TEXT, weight=BOLD).move_to(LBL)
        self.play(FadeOut(gl), FadeIn(ol), run_time=0.6)
        buds = VGroup()
        glows = VGroup()
        for ang in (40, 160, 280):
            u = np.array([np.cos(ang * DEGREES), np.sin(ang * DEGREES), 0])
            glows.add(Circle(radius=0.42, stroke_width=0, fill_color=ORANGE, fill_opacity=0.3).move_to(D + 1.05 * u))
            for r, off in ((1.32, 0.14), (1.6, -0.12)):
                perp = np.array([-u[1], u[0], 0])
                buds.add(cell(BLUE, 0.27, 0.6, 2.5).move_to(D + r * u + off * perp))
        self.play(FadeIn(glows), LaggedStart(*[FadeIn(x, scale=0.6) for x in buds], lag_ratio=0.15), run_time=1.3)
        for g in glows:
            pulse(g, 0.3, 0.12, 2.5)
        org = VGroup(ringc, lumen, buds, glows)
        org.add_updater(lambda m, dt: m.rotate(0.12 * dt, about_point=D))
        self.at("they could be")
        arc = Arc(radius=2.3, start_angle=0.3, angle=1.7, arc_center=D, color=TEAL, stroke_width=6).add_tip(tip_length=0.25)
        rl = T("replated repeatedly", 32, TEAL, weight=BOLD).move_to(LBL)
        self.play(FadeOut(ol), FadeIn(rl), Create(arc), run_time=0.9)
        arc.add_updater(lambda m, dt: m.rotate(0.9 * dt, about_point=D))
        self.at("no stromal cells")
        self.play(FadeOut(arc), run_time=0.4)
        icon = VGroup(*[Ellipse(width=1.0, height=0.4, color=STROMA, fill_color=STROMA, fill_opacity=0.55,
                                stroke_width=3).move_to([1.0 + 1.15 * i, 3.0, 0]) for i in range(2)])
        il = T("stromal cells", 30, STROMA, weight=BOLD).move_to([1.6, 2.4, 0])
        self.play(FadeIn(icon), FadeIn(il), run_time=0.6)
        x = VGroup(Line(icon.get_corner(UL), icon.get_corner(DR), color=RED, stroke_width=7),
                   Line(icon.get_corner(DL), icon.get_corner(UR), color=RED, stroke_width=7))
        self.play(Create(x), run_time=0.6)
        self.at("the matrix and factors")
        self.play(Indicate(gel, color=PALE, scale_factor=1.04), FadeOut(rl), run_time=0.9)
        self.at("supplied a niche")
        nl = T("niche", 40, TEAL, weight=BOLD).move_to(LBL)
        self.play(FadeIn(nl), Indicate(glows, color=ORANGE, scale_factor=1.3), run_time=1.0)
        self.finish()


class S10Comeback(SpokenScene):
    def construct(self):
        world, cells, flow = crypt_world()
        f = fields()
        wl, bl = ws_labels()
        self.add(f, world, wl, bl)
        self.at("if the state depends")
        self.play(*[c.animate.set_fill(BLUE, 0.06) for c in cells], f.wb.animate.set_value(1.6), run_time=1.5)
        self.at("could a cell that")
        g = sil().move_to([CX + 0.35, 0.9, 0])
        g.add_updater(lambda m, dt, s=[0.0]: (s.__setitem__(0, s[0] + dt),
                                              m.move_to([CX + 0.35, 0.9 + 0.08 * np.sin(1.5 * s[0]), 0])))
        qm = T("?", 56, GOLD, weight=BOLD).move_to([CX + 1.0, 1.1, 0])
        self.play(FadeIn(g), FadeIn(qm), f.wb.animate.set_value(1.0), run_time=1.0)
        self.at("come back")
        da = DashedLine([CX + 0.2, 0.5, 0], [CX + 0.0, -1.6, 0], color=GOLD, stroke_width=5).add_tip(tip_length=0.22)
        cb = T("come back?", 36, GOLD, weight=BOLD).move_to([1.7, -0.3, 0])
        self.play(Create(da), FadeIn(cb), run_time=1.2)
        self.at("injury tests that")
        inj = T("injury:\nusual stem cells lost", 30, RED, weight=BOLD, line_spacing=0.9).move_to([4.4, -2.5, 0])
        self.play(FadeIn(inj), Indicate(cells, color=RED, scale_factor=1.08), run_time=1.2)
        self.at("reprogramming pushes")
        self.play(FadeOut(VGroup(inj, wl, bl, cb)), run_time=0.4)
        sc = Circle(radius=0.75, color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.35).move_to([4.2, 2.1, 0])
        nuc = Circle(radius=0.3, color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=0.5).move_to(sc)
        sl = T("specialized cell", 30, TEXT, weight=BOLD).move_to([4.2, 0.95, 0])
        self.play(FadeIn(sc), FadeIn(nuc), FadeIn(sl), run_time=1.0)
        self.play(Indicate(nuc, color=TEXT, scale_factor=1.3), run_time=1.0)
        self.at("whether a specialized nucleus")
        self.play(Indicate(nuc, color=TEAL, scale_factor=1.4), run_time=1.0)
        self.at("reset beyond its tissue")
        q2 = T("?", 80, GOLD, weight=BOLD).move_to([5.9, 2.1, 0])
        rl = T("reset beyond\nthe tissue?", 32, GOLD, weight=BOLD, line_spacing=0.9).move_to([4.5, -0.1, 0])
        self.play(FadeIn(q2, scale=1.3), FadeIn(rl), run_time=1.0)
        self.finish()


class S11Takeaway(SpokenScene):
    def construct(self):
        world, cells, flow = crypt_world(bracket=True)
        f = fields()
        wl, bl = ws_labels()
        for c in cells:
            c.set_fill(BLUE, 0.68)
        self.add(f, world, wl, bl)
        self.at("so when you ask")
        cl = T("the cell", 34, BLUE, weight=BOLD).move_to([4.0, 0.6, 0])
        a1 = Arrow([2.9, 0.5, 0], [-0.55, -1.35, 0], buff=0, color=BLUE, stroke_width=4, tip_length=0.2)
        self.play(FadeIn(cl), GrowArrow(a1), run_time=0.9)
        self.at("look at the place")
        pl = T("the place", 34, ORANGE, weight=BOLD).move_to([4.0, -0.5, 0])
        a2 = Arrow([2.9, -0.6, 0], [-0.8, -2.5, 0], buff=0, color=ORANGE, stroke_width=4, tip_length=0.2)
        self.play(FadeIn(pl), GrowArrow(a2), f.wb.animate.set_value(1.6), run_time=1.0)
        self.at("local niche signals")
        self.play(FadeOut(VGroup(cl, a1, pl, a2)), f.wb.animate.set_value(1.9), run_time=0.8)
        rule = T("Local niche signals\nhelp hold a cell in\nthe stem-cell state.", 34, TEXT,
                 weight=BOLD, line_spacing=0.95).move_to([4.2, 1.2, 0])
        self.play(FadeIn(rule, shift=UP * 0.1), run_time=1.0)
        self.at("whether a cell that left")
        self.play(f.wb.animate.set_value(1.0), FadeOut(VGroup(wl, bl)), run_time=0.6)
        g = sil().move_to([CX + 0.35, 0.9, 0])
        g.add_updater(lambda m, dt, s=[0.0]: (s.__setitem__(0, s[0] + dt),
                                              m.move_to([CX + 0.35, 0.9 + 0.08 * np.sin(1.5 * s[0]), 0])))
        da = DashedLine([CX + 0.2, 0.5, 0], [CX + 0.0, -1.6, 0], color=GOLD, stroke_width=5).add_tip(tip_length=0.22)
        nt = T("next test", 34, GOLD, weight=BOLD).move_to([4.2, -0.4, 0])
        self.play(FadeIn(g), Create(da), FadeIn(nt), run_time=1.0)
        self.finish()


class S12End(EndCard):
    LINE = "Local niche signals help hold a cell in the stem-cell state."
