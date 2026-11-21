"""
Film: "Why ATP works as money" (metabolism-basic-concepts__chapter-2)

COLOUR MAP (one colour per concept for the whole film):
- YELLOW (#F5D547): ATP, phosphoryl groups, activated carriers (NADH, FADH2)
- GOLD (#D4A843): phosphoryl transfer badges (~P), acetyl-CoA hub highlight, title rule
- BLUE (#58C4DD): glucose, fuel carbon (food streams, carbon tokens, fat savings vault)
- GREEN (#83C167): favourable flow / phosphorylated cell-work targets
- TEAL (#3FB8C0): electrons (electron sparks and electron spark meters)
- RED (#FC6255): heat/losses and oxygen-bonded tag on glucose
- ORANGE (#FF862F): fuel combustion glow at the base of the fuel lift
- GREY (#8B93A1): schematic hill, terraces, citric acid cycle wheel structure, dimmed ADP, schematic tag
- TEXT (#E8EAF0): ordinary labels, headlines, work icons (move, pump, build), hydrogen tags

ONE CARRIED WORLD:
A broad schematic hill with a mid-height ATP wallet tray on a flat ledge transforms in place into three
stacked phosphoryl-transfer terraces, gains a fuel-powered lift shaft on the left fed by converging fuel
highways and the citric acid cycle wheel, and pulls back at the end to show the whole loop of ATP cash
spent on work and remade by burning fuel.

SCENE MOTION PLAN (what changes on screen and what computes it):
- s00_link_and_question: Ghost ATP/glucose carts roll along the hill profile; ATP beads continuously circulate out of the mid-height tray and back in while a ValueTracker clock runs 06:00 -> 24:00 and a tally stack grows to 40 kg/day.
- s01_title: Dimmed hill, tray, and circulating ATP beads continue moving behind the centred title card as it lifts away and the world brightens.
- s02_cash: Zoomed view tracks one bead rolling down from the tray to a lower ledge (turning grey ADP), riding an unlabelled lift back up (brightening to yellow ATP) while background beads follow the same path and a loop counter ticks 1, 2, 3 up to hundreds a day.
- s03_ladder: Hill profile morphs in place into three terraces; GOLD phosphoryl badges slide strictly downward from richer donors to recharge ADP->ATP and from ATP to acceptors below (lighting GREEN), repeating continuously.
- s04_idea: Transfer arrows pulse into and out of the middle ATP tray as downward badges drop; work icons (move, pump, build) light in turn; the left fuel lift shaft rises with an ORANGE glow at its base.
- s05_converge: Pan left to show food icons (steak, potato, olive oil) breaking into continuous streams of BLUE carbon beads flowing along three curved highways (and a dashed amino-acid branch) into the central GOLD acetyl-CoA block.
- s06_electrons: Acetyl-CoA feeds a continuously rotating citric acid cycle wheel that emits grey CO2 puffs and TEAL electron sparks onto YELLOW NADH/FADH2 trucks, which drive to O2 at the lift base and start the fuel lift raising ADP -> ATP to the tray.
- s07_predict: Slowly turning wheel and lift remain active behind two rising BLUE carbon tokens (fatty acid vs glucose) with empty TEAL spark meters.
- s08_predict_hold: PredictPause holds the question over the two carbon tokens while the wheel/lift continue slowly turning, empty meters flicker faintly, and the 4.5 s countdown ring runs.
- s09_answer: Hydrogen tags attach to the fatty-acid carbon as its TEAL meter fills high (0.90) and sparks start streaming, an oxygen tag attaches to glucose as its meter fills partway (0.40), bars rise to exact 2.25:1 heights (~9 vs ~4 kcal/g), and TEAL sparks stream continuously from both meters to YELLOW carrier trucks.
- s10_return: Pull back to the full world; BLUE fat vault settles at bottom left, ATP tray glows, BLUE fuel streams feed the lift, and YELLOW ATP beads loop continuously out to move/pump/build work icons and back up the running fuel lift.
- s11_end: Standard EndCard with the take-home line and waving Hex mascot.
"""

from bp_parts import *

# ------------------------------------------------------------------ shared constants & builders
TRAY_X = 0.0
TRAY_Y = 0.30


def _hill_y(x):
    """Broad schematic hillside with a flat mid-height wallet ledge centred at x=0."""
    if x < -2.0:
        if x <= -3.5:
            t = (x + 6.3) / 2.8
            return -2.1 + 4.1 * (0.5 - 0.5 * np.cos(PI * np.clip(t, 0.0, 1.0)))
        t = (x + 3.5) / 1.5
        return 2.0 - 1.95 * (0.5 - 0.5 * np.cos(PI * np.clip(t, 0.0, 1.0)))
    elif x <= 2.0:
        return 0.05
    else:
        t = (x - 2.0) / 4.3
        return 0.05 - 2.35 * (0.5 - 0.5 * np.cos(PI * np.clip(t, 0.0, 1.0)))


def make_hill(fill_op=0.16, stroke_op=0.85):
    """Broad schematic grey hill filling ~70% of the frame height, flat at the wallet ledge."""
    xs = np.linspace(-6.3, 6.3, 180)
    top_pts = [np.array([x, _hill_y(x), 0.0]) for x in xs]
    outline = VMobject(stroke_color=GREY, stroke_width=4.5, stroke_opacity=stroke_op)
    outline.set_points_as_corners(top_pts)
    poly_pts = top_pts + [np.array([6.3, -3.1, 0.0]), np.array([-6.3, -3.1, 0.0])]
    fill = Polygon(*poly_pts, stroke_width=0, fill_color=GREY, fill_opacity=fill_op)
    return VGroup(fill, outline)


def make_bead(label="ATP", color=YELLOW, radius=0.41, opacity=1.0, font_size=22, show_text=True):
    """A single ATP or ADP bead with text centred inside, large enough for clean clearance."""
    ring = Circle(
        radius=radius,
        stroke_color=color,
        stroke_width=3.2,
        stroke_opacity=opacity,
        fill_color=BG,
        fill_opacity=0.92,
    )
    glow = Circle(
        radius=radius,
        stroke_width=0,
        fill_color=color,
        fill_opacity=0.20 * opacity,
    )
    if show_text and label:
        txt = T(label, size=font_size, color=color, weight=BOLD).set_opacity(opacity)
        txt.move_to(ring)
        return VGroup(glow, ring, txt)
    return VGroup(glow, ring)


def make_tray(center=(TRAY_X, TRAY_Y, 0), n_beads=4, opacity=1.0, show_label=True,
              label_text="ATP in body", show_bead_text=True, bead_radius=0.41, width=3.85):
    """Open U-shaped tray holding four YELLOW ATP beads."""
    cx, cy, _ = center
    h = bead_radius * 2.45
    pts = [
        np.array([cx - width / 2, cy + h * 0.45, 0.0]),
        np.array([cx - width / 2, cy - h * 0.45, 0.0]),
        np.array([cx + width / 2, cy - h * 0.45, 0.0]),
        np.array([cx + width / 2, cy + h * 0.45, 0.0]),
    ]
    u_wall = VMobject(stroke_color=YELLOW, stroke_width=4, stroke_opacity=0.9 * opacity)
    u_wall.set_points_as_corners(pts)
    backing = RoundedRectangle(
        corner_radius=0.08, width=width - 0.06, height=h * 0.85,
        stroke_width=0, fill_color=BG, fill_opacity=0.88 * opacity,
    ).move_to([cx, cy - 0.03, 0.0])
    beads = VGroup(*[
        make_bead("ATP", YELLOW, radius=bead_radius, opacity=opacity, font_size=22, show_text=show_bead_text)
        for _ in range(n_beads)
    ])
    beads.arrange(RIGHT, buff=0.08).move_to([cx, cy - 0.03, 0.0])
    g = VGroup(backing, u_wall, beads)
    g.wall = u_wall
    g.backing = backing
    g.beads = beads
    if show_label:
        lbl = T(label_text, size=26, color=YELLOW).next_to(u_wall, UP, buff=0.16).set_opacity(opacity)
        g.add(lbl)
        g.label = lbl
    return g


def make_cart(text, color, width=1.45, height=0.64, opacity=0.55):
    """Ghost cart for opening recap."""
    box = RoundedRectangle(
        corner_radius=0.12, width=width, height=height,
        stroke_color=color, stroke_width=2.8, stroke_opacity=opacity,
        fill_color=color, fill_opacity=0.14 * opacity,
    )
    lbl = T(text, size=24, color=color).set_opacity(opacity).move_to(box)
    w1 = Circle(radius=0.10, stroke_color=color, stroke_width=2.5, stroke_opacity=opacity, fill_color=BG, fill_opacity=0.9)
    w2 = w1.copy()
    w1.next_to(box, DOWN, buff=0.02).shift(LEFT * (width * 0.28))
    w2.next_to(box, DOWN, buff=0.02).shift(RIGHT * (width * 0.28))
    return VGroup(box, lbl, w1, w2)


def make_terrace_system(x_left=-3.1, x_right=5.6, ys=(1.90, 0.0, -1.85), with_axis=True):
    """Three broad phosphoryl-transfer terraces stacked like rungs."""
    g = VGroup()
    rungs = VGroup()
    for y in ys:
        line = Line([x_left, y, 0], [x_right, y, 0], color=GREY, stroke_width=5)
        shelf = Rectangle(
            width=x_right - x_left, height=0.24,
            stroke_width=0, fill_color=GREY, fill_opacity=0.28,
        ).move_to([(x_left + x_right) / 2, y - 0.12, 0])
        rungs.add(VGroup(shelf, line))
    g.add(rungs)
    g.rungs = rungs
    g.ys = ys
    g.x_left = x_left
    g.x_right = x_right
    if with_axis:
        ax_x = x_left - 0.35
        ax = Arrow([ax_x, ys[2] - 0.20, 0], [ax_x, ys[0] + 0.55, 0], color=GREY, stroke_width=4, buff=0, max_tip_length_to_length_ratio=0.08)
        ax_lbl = T("transfer potential\n(schematic)", size=24, color=GREY, line_spacing=0.85)
        ax_lbl.next_to(ax.get_end(), LEFT, buff=0.18).shift(DOWN * 0.15)
        if ax_lbl.get_left()[0] < -6.25:
            ax_lbl.align_to([-6.25, 0, 0], LEFT)
        g.add(ax, ax_lbl)
        g.axis = ax
        g.axis_label = ax_lbl
    return g


def make_p_badge(color=GOLD, radius=0.24):
    """Small phosphoryl badge 'P'."""
    c = Circle(radius=radius, stroke_color=color, stroke_width=3.2, fill_color=BG, fill_opacity=0.95)
    f = Circle(radius=radius, stroke_width=0, fill_color=color, fill_opacity=0.28)
    t = T("P", size=22, color=color, weight=BOLD).move_to(c)
    return VGroup(f, c, t)


def make_work_icons(y=-1.85, xs=(-1.3, 0.7, 2.7), size=24, with_labels=True):
    """Three small TEXT work icons on the bottom terrace: move, pump, build."""
    specs = [("move", 0), ("pump", 1), ("build", 2)]
    out = VGroup()
    for name, kind in specs:
        x = xs[kind]
        if kind == 0:
            glyph = VGroup(
                Circle(radius=0.19, color=TEXT, stroke_width=3),
                Dot([0, 0, 0], radius=0.05, color=TEXT),
                Line([-0.23, 0, 0], [0.23, 0, 0], color=TEXT, stroke_width=2.5),
                Line([0, -0.23, 0], [0, 0.23, 0], color=TEXT, stroke_width=2.5),
            )
        elif kind == 1:
            glyph = VGroup(
                Line([-0.15, -0.19, 0], [-0.15, 0.19, 0], color=TEXT, stroke_width=3),
                Line([0.15, -0.19, 0], [0.15, 0.19, 0], color=TEXT, stroke_width=3),
                Arrow([0, -0.21, 0], [0, 0.23, 0], color=TEXT, stroke_width=3, buff=0, max_tip_length_to_length_ratio=0.35),
            )
        else:
            b1 = Rectangle(width=0.21, height=0.13, stroke_color=TEXT, stroke_width=2.5, fill_color=TEXT, fill_opacity=0.18).move_to([-0.12, -0.09, 0])
            b2 = b1.copy().move_to([0.12, -0.09, 0])
            b3 = b1.copy().move_to([0.0, 0.08, 0])
            glyph = VGroup(b1, b2, b3)
        glyph.move_to([x, y + 0.34, 0])
        if with_labels:
            lbl = T(name, size=size, color=TEXT).next_to(glyph, UP, buff=0.10)
            item = VGroup(glyph, lbl)
            item.glyph = glyph
            item.label = lbl
        else:
            item = VGroup(glyph)
            item.glyph = glyph
            item.label = None
        out.add(item)
    return out


def make_fuel_lift(x=-4.4, y_bot=-1.85, y_top=0.0, width=0.92, show_label=True, glow_opacity=0.60):
    """Empty fuel-driven lift shaft reaching from bottom terrace to middle terrace."""
    h = y_top - y_bot
    shaft = Rectangle(
        width=width, height=h,
        stroke_color=GREY, stroke_width=3.2,
        fill_color=BG, fill_opacity=0.58,
    ).move_to([x, (y_bot + y_top) / 2, 0])
    rails = VGroup(
        DashedLine([x - width * 0.26, y_bot + 0.08, 0], [x - width * 0.26, y_top - 0.08, 0], color=GREY, stroke_width=2, dash_length=0.12),
        DashedLine([x + width * 0.26, y_bot + 0.08, 0], [x + width * 0.26, y_top - 0.08, 0], color=GREY, stroke_width=2, dash_length=0.12),
    )
    glow = Ellipse(
        width=width * 1.15, height=0.42,
        stroke_color=ORANGE, stroke_width=2.5, stroke_opacity=glow_opacity,
        fill_color=ORANGE, fill_opacity=0.40 * glow_opacity,
    ).move_to([x, y_bot - 0.26, 0])
    g = VGroup(shaft, rails, glow)
    g.shaft = shaft
    g.glow = glow
    if show_label:
        lbl = T("fuel", size=24, color=ORANGE).next_to(glow, DOWN, buff=0.12)
        g.add(lbl)
        g.label = lbl
    return g


def make_compact_right_world(x0=2.65, x1=6.18, ys=(1.60, 0.05, -1.50), show_labels=True, glow_op=0.80):
    """Build compact terraces + tray + fuel lift at final size (all text >= 22 pt, strictly inside frame)."""
    terraces = make_terrace_system(x_left=x0 + 0.55, x_right=x1, ys=ys, with_axis=False)
    tray_x = (x0 + 0.55 + x1) / 2
    tray = make_tray(center=(tray_x, ys[1] + 0.34, 0), n_beads=4, show_label=False,
                     show_bead_text=False, bead_radius=0.18, width=1.85)
    atp_lbl = T("ATP", size=24, color=YELLOW, weight=BOLD).next_to(tray.wall, UP, buff=0.10)
    icon_xs = (x0 + 1.00, tray_x, x1 - 0.42)
    work_icons = make_work_icons(y=ys[2], xs=icon_xs, size=22, with_labels=show_labels)
    lift = make_fuel_lift(x=x0, y_bot=ys[2], y_top=ys[1], width=0.68, show_label=show_labels, glow_opacity=glow_op)
    g = VGroup(terraces, tray, atp_lbl, work_icons, lift)
    g.terraces = terraces
    g.tray = tray
    g.atp_lbl = atp_lbl
    g.work_icons = work_icons
    g.lift = lift
    return g


def make_wheel(center=(-2.6, 0.20, 0), radius=1.72, opacity=1.0):
    """Large citric acid cycle wheel with spokes (label placed cleanly below)."""
    cx, cy, _ = center
    outer = Circle(radius=radius, stroke_color=GREY, stroke_width=5, stroke_opacity=opacity, fill_color=GREY, fill_opacity=0.14 * opacity).move_to(center)
    inner = Circle(radius=radius * 0.62, stroke_color=GREY, stroke_width=3, stroke_opacity=0.75 * opacity).move_to(center)
    spokes = VGroup()
    for k in range(6):
        ang = k * PI / 3
        p1 = np.array([cx + 0.25 * radius * np.cos(ang), cy + 0.25 * radius * np.sin(ang), 0.0])
        p2 = np.array([cx + radius * np.cos(ang), cy + radius * np.sin(ang), 0.0])
        spokes.add(Line(p1, p2, color=GREY, stroke_width=3.0, stroke_opacity=0.80 * opacity))
    hub = Circle(radius=0.25 * radius, stroke_color=GOLD, stroke_width=3.5, stroke_opacity=opacity, fill_color=BG, fill_opacity=0.95).move_to(center)
    arrows = VGroup()
    for ang in (PI * 0.25, PI * 0.92, PI * 1.58):
        p = np.array([cx + radius * np.cos(ang), cy + radius * np.sin(ang), 0.0])
        tangent = np.array([np.sin(ang), -np.cos(ang), 0.0])
        arrows.add(Triangle(color=GOLD, fill_color=GOLD, fill_opacity=opacity, stroke_width=0).scale(0.12).rotate(np.arctan2(tangent[1], tangent[0]) - PI / 2).move_to(p))
    rot_group = VGroup(spokes, arrows)
    wheel = VGroup(outer, inner, rot_group, hub)
    wheel.rot = rot_group
    wheel.center_pt = np.array(center, dtype=float)
    wheel.radius = radius
    return wheel


def make_truck(text, center, color=YELLOW):
    """Small delivery truck representing an activated electron carrier (NADH / FADH₂)."""
    box = boxed_label(text, color=color, size=24, pad=0.16, fill_opacity=0.24)
    box.move_to(center)
    w1 = Circle(radius=0.09, stroke_color=color, stroke_width=2.5, fill_color=BG, fill_opacity=0.95)
    w2 = w1.copy()
    w1.next_to(box, DOWN, buff=0.02).shift(LEFT * (box.width * 0.28))
    w2.next_to(box, DOWN, buff=0.02).shift(RIGHT * (box.width * 0.28))
    g = VGroup(box, w1, w2)
    g.box = box
    return g


def make_carbon_token(label_text, center, radius=0.84):
    """Large BLUE carbon token ('C') with label cleanly below."""
    ring = Circle(radius=radius, stroke_color=BLUE, stroke_width=4.5, fill_color=BLUE, fill_opacity=0.25).move_to(center)
    c_sym = T("C", size=48, color=BLUE, weight=BOLD).move_to(ring)
    lbl = T(label_text, size=26, color=BLUE).next_to(ring, DOWN, buff=0.18)
    g = VGroup(ring, c_sym, lbl)
    g.ring = ring
    g.c_sym = c_sym
    g.label = lbl
    return g


def make_spark_meter(center, fill_frac=0.0, width=2.45, height=0.44, flicker=False):
    """TEAL electron spark meter beneath a carbon token."""
    bg = RoundedRectangle(corner_radius=0.08, width=width, height=height, stroke_color=TEAL, stroke_width=3, fill_color=BG, fill_opacity=0.85).move_to(center)
    tracker = ValueTracker(fill_frac)

    def _mk_bar():
        f = float(np.clip(tracker.get_value(), 0.0, 1.0))
        if f < 0.02:
            if flicker:
                return RoundedRectangle(
                    corner_radius=0.06, width=width - 0.10, height=height - 0.10,
                    stroke_width=0, fill_color=TEAL, fill_opacity=0.12,
                ).move_to(bg)
            return VMobject()
        w = max(0.08, (width - 0.10) * f)
        r = RoundedRectangle(
            corner_radius=0.05, width=w, height=height - 0.10,
            stroke_width=0, fill_color=TEAL, fill_opacity=0.85,
        )
        r.align_to(bg.get_left() + RIGHT * 0.05, LEFT)
        r.set_y(bg.get_center()[1])
        return r

    bar = always_redraw(_mk_bar)
    g = VGroup(bg, bar)
    g.bg = bg
    g.tracker = tracker
    return g


def _bead_circulation_updater(beads, path_fn, speed=0.22):
    """Attach phase-offset path circulation updater to a group of beads/dots."""
    state = {"t": 0.0}

    def _u(mob, dt):
        state["t"] += dt * speed
        for i, b in enumerate(mob):
            u = (state["t"] + i / len(mob)) % 1.0
            pos, op, col = path_fn(u)
            b.move_to(pos)
            if col is not None:
                if len(b.submobjects) >= 3:
                    b[1].set_stroke(color=col, opacity=op)
                    b[0].set_fill(color=col, opacity=0.20 * op)
                    b[2].set_color(col).set_opacity(op)
                else:
                    b.set_color(col).set_opacity(op)
            else:
                b.set_opacity(op)
    beads.add_updater(_u)
    return beads


# ------------------------------------------------------------------ Scene 0
class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        hill = make_hill()
        tag = scope_tag("schematic")
        self.add(hill, tag)

        # Ghost joined carts crossing the crest (lifted cleanly above hill outline)
        cart_prog = ValueTracker(0.0)
        g_cart = make_cart("glucose", BLUE, width=1.45, opacity=0.55)
        a_cart = make_cart("ATP", YELLOW, width=1.15, opacity=0.55)

        def _g_pos():
            x = -4.8 + 1.8 * cart_prog.get_value()
            y = max(_hill_y(x - 0.75), _hill_y(x), _hill_y(x + 0.75)) + 0.65
            return np.array([x, y, 0.0])

        def _a_pos():
            x = -2.2 + 2.4 * cart_prog.get_value()
            return np.array([x, _hill_y(x) + 1.05, 0.0])

        g_cart.add_updater(lambda m: m.move_to(_g_pos()))
        a_cart.add_updater(lambda m: m.move_to(_a_pos()))
        rope = always_redraw(
            lambda: DashedLine(
                _g_pos() + RIGHT * 0.78,
                _a_pos() + LEFT * 0.62,
                color=GREY, stroke_width=2.5, dash_length=0.12,
            ).set_opacity(0.55)
        )
        self.add(rope, g_cart, a_cart)
        self.play(cart_prog.animate.set_value(1.0), run_time=self.beat(0.22), rate_func=linear)
        g_cart.clear_updaters()
        a_cart.clear_updaters()
        self.play(FadeOut(rope), FadeOut(g_cart), FadeOut(a_cart), run_time=0.40)

        # Beat 2: "Now look at the wallet"
        self.at("look at the wallet")
        tray = make_tray(center=(TRAY_X, TRAY_Y + 0.34, 0), width=3.85)
        self.play(FadeIn(tray, shift=DOWN * 0.15), run_time=0.65)

        # Beat 3: "well under a kilogram"
        self.at("well under a kilogram")
        under_lbl = T("under 1 kg", size=28, color=YELLOW, weight=BOLD).next_to(tray.wall, DOWN, buff=0.22)
        self.play(FadeIn(under_lbl, shift=UP * 0.1), run_time=0.55)

        # Beat 4: "roughly 40 kilograms"
        self.at("roughly 40 kilograms")
        hour = ValueTracker(6.0)
        clock = always_redraw(
            lambda: M(f"{int(hour.get_value()):02d}:00", size=34, color=TEXT).move_to([5.45, 3.05, 0])
        )

        tally_base = np.array([5.15, -0.85, 0.0])

        def _mk_tally():
            frac = np.clip((hour.get_value() - 6.0) / 18.0, 0.0, 1.0)
            n_bars = max(1, int(round(frac * 10)))
            bars = VGroup()
            for k in range(n_bars):
                bar = RoundedRectangle(
                    corner_radius=0.04, width=1.20, height=0.15,
                    stroke_color=YELLOW, stroke_width=1.5, fill_color=YELLOW, fill_opacity=0.70,
                ).move_to([tally_base[0], tally_base[1] + 0.10 + k * 0.18, 0])
                bars.add(bar)
            return bars

        tally_stack = always_redraw(_mk_tally)
        tally_val = always_redraw(
            lambda: M(f"{40.0 * np.clip((hour.get_value() - 6.0) / 18.0, 0.0, 1.0):.0f} kg", size=28, color=YELLOW).move_to([5.15, -2.55, 0])
        )
        tally_tag = T("about 40 kg a day", size=26, color=YELLOW).move_to([tally_base[0] - 0.15, tally_base[1] + 2.20, 0])

        flow_beads = VGroup(*[Dot(radius=0.18, color=YELLOW) for _ in range(6)])
        flow_beads.layout_ok = True

        def _bead_path(u):
            if u < 0.55:
                s = u / 0.55
                x = 2.15 + s * 3.85
                y = _hill_y(x) + 0.24
                return np.array([x, y, 0.0]), 0.95 * (1.0 - 0.45 * s), YELLOW
            else:
                s = (u - 0.55) / 0.45
                x = -2.45 + s * 0.60
                y = 2.55 - s * 1.95
                return np.array([x, y, 0.0]), 0.95 * np.sin(PI * s), YELLOW

        _bead_circulation_updater(flow_beads, _bead_path, speed=0.35)
        self.add(clock, tally_stack, tally_val, flow_beads)
        self.play(hour.animate.set_value(24.0), FadeIn(tally_tag), run_time=3.2, rate_func=linear)

        # Beat 5: "How can so small"
        self.at("How can so small")
        q_top = T("How does a tiny pool keep up?", size=38, color=TEXT, weight=BOLD).move_to([-0.8, 3.05, 0])
        self.play(FadeIn(q_top, shift=DOWN * 0.1), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------ Scene 1
class S01Title(NarratedScene):
    def construct(self):
        hill = make_hill(fill_op=0.06, stroke_op=0.30)
        tray = make_tray(center=(TRAY_X, TRAY_Y + 0.34, 0), opacity=0.32, show_label=False, show_bead_text=False, width=3.85)
        tag = scope_tag("schematic").set_opacity(0.45)

        flow_beads = VGroup(*[Dot(radius=0.18, color=YELLOW).set_opacity(0.35) for _ in range(6)])
        flow_beads.layout_ok = True

        def _bead_path(u):
            if u < 0.55:
                s = u / 0.55
                x = 2.15 + s * 3.85
                y = _hill_y(x) + 0.24
                return np.array([x, y, 0.0]), 0.35, None
            else:
                s = (u - 0.55) / 0.45
                x = -2.45 + s * 0.60
                y = 2.55 - s * 1.95
                return np.array([x, y, 0.0]), 0.35 * np.sin(PI * s), None

        _bead_circulation_updater(flow_beads, _bead_path, speed=0.35)
        self.add(hill, tray, flow_beads, tag)

        brand = T(SITE_NAME, size=22, color=TEAL, weight=BOLD).set_opacity(0.9)
        brand.layout_ok = True
        lesson = T("METABOLISM: BASIC CONCEPTS AND DESIGN", size=22, color=GREY)
        title = T("Why ATP works as money", size=52, font=TITLE_FONT, color=TEXT)
        fit(title, max_w=11.5)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.28).move_to([0, 0.2, 0])
        card_bg = RoundedRectangle(
            corner_radius=0.22, width=g.width + 1.0, height=g.height + 0.7,
            stroke_width=0, fill_color=BG, fill_opacity=0.86,
        ).move_to(g)

        self.play(FadeIn(card_bg), FadeIn(g), run_time=0.40)
        self.wait(1.0)
        self.play(
            FadeOut(g, shift=UP * 0.6),
            FadeOut(card_bg),
            hill[0].animate.set_fill(opacity=0.16),
            hill[1].animate.set_stroke(opacity=0.85),
            tray.wall.animate.set_stroke(opacity=0.95),
            tray.backing.animate.set_fill(opacity=0.88),
            *[b[0].animate.set_fill(opacity=0.20) for b in tray.beads],
            *[b[1].animate.set_stroke(opacity=1.0) for b in tray.beads],
            run_time=0.55,
        )
        self.finish()


# ------------------------------------------------------------------ Scene 2
class S02Cash(SpokenScene):
    def construct(self):
        tray_pos = np.array([0.0, 1.70, 0.0])
        lift_x = -4.2

        slope = VMobject(stroke_color=GREY, stroke_width=4.5)
        slope.set_points_as_corners([
            np.array([lift_x - 0.8, 1.35, 0.0]),
            np.array([1.95, 1.35, 0.0]),
            np.array([3.05, -2.05, 0.0]),
            np.array([5.8, -2.05, 0.0]),
        ])
        slope_fill = Polygon(
            np.array([lift_x - 0.8, 1.35, 0.0]),
            np.array([1.95, 1.35, 0.0]),
            np.array([3.05, -2.05, 0.0]),
            np.array([5.8, -2.05, 0.0]),
            np.array([5.8, -3.1, 0.0]),
            np.array([lift_x - 0.8, -3.1, 0.0]),
            stroke_width=0, fill_color=GREY, fill_opacity=0.17,
        )
        lift_track = Rectangle(
            width=0.95, height=3.40,
            stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=0.6,
        ).move_to([lift_x, -0.35, 0.0])
        lift_rails = DashedLine([lift_x, -1.90, 0], [lift_x, 1.25, 0], color=GREY, stroke_width=2, dash_length=0.14)
        tray = make_tray(center=tray_pos, n_beads=4, show_label=True, label_text="ATP in body", width=3.85)
        tag = scope_tag("schematic")

        world = VGroup(slope_fill, slope, lift_track, lift_rails, tray)
        world.scale(0.84)
        self.add(world, tag)
        self.play(world.animate.scale(1.0 / 0.84), run_time=2.4)

        bg_beads = VGroup(*[Dot(radius=0.18, color=YELLOW) for _ in range(5)])
        bg_beads.layout_ok = True

        def _loop_pt(u):
            if u < 0.30:
                s = u / 0.30
                p = np.array([2.35 + s * 1.75, 1.75 - s * 3.30, 0.0])
                col = YELLOW if s < 0.82 else GREY
                return p, 0.85, col
            elif u < 0.58:
                s = (u - 0.30) / 0.28
                p = np.array([4.1 - s * (4.1 - lift_x), -1.55, 0.0])
                return p, 0.65, GREY
            elif u < 0.85:
                s = (u - 0.58) / 0.27
                p = np.array([lift_x, -1.55 + s * 3.30, 0.0])
                col = GREY if s < 0.85 else YELLOW
                return p, 0.75 + 0.20 * s, col
            else:
                s = (u - 0.85) / 0.15
                p = np.array([lift_x + s * (-2.45 - lift_x), 1.75, 0.0])
                return p, 0.90, YELLOW

        _bead_circulation_updater(bg_beads, _loop_pt, speed=0.22)
        self.add(bg_beads)

        self.at("Each molecule is spent")
        tracked = make_bead("ATP", YELLOW, radius=0.41, font_size=22).move_to([2.45, 1.80, 0.0])
        tracked_adp = make_bead("ADP", GREY, radius=0.41, opacity=0.85, font_size=22).move_to([4.1, -1.55, 0.0])
        tracked_lift_top = make_bead("ATP", YELLOW, radius=0.41, font_size=22).move_to([lift_x, 1.80, 0.0])

        loop_n = ValueTracker(1.0)
        loop_txt = counter("loop {:.0f}", loop_n, at=[4.3, 2.75, 0], size=32, color=YELLOW)
        self.add(tracked, loop_txt)

        self.play(tracked.animate.move_to([4.1, -1.55, 0.0]), run_time=1.3, rate_func=linear)
        self.play(swap(tracked, tracked_adp, run_time=0.35))
        self.play(tracked_adp.animate.move_to([lift_x, -1.55, 0.0]), run_time=1.0, rate_func=linear)
        self.play(tracked_adp.animate.move_to([lift_x, 1.80, 0.0]), run_time=1.05, rate_func=linear)
        self.play(swap(tracked_adp, tracked_lift_top, run_time=0.35))
        self.play(tracked_lift_top.animate.move_to([-2.55, 1.80, 0.0]), run_time=0.65, rate_func=linear)
        self.play(FadeOut(tracked_lift_top), run_time=0.25)
        loop_n.set_value(2)
        self.wait(0.25)
        loop_n.set_value(3)

        self.play(loop_n.animate.set_value(180), run_time=1.8, rate_func=rush_into)
        hundreds_lbl = T("hundreds a day", size=30, color=YELLOW, weight=BOLD).move_to([4.3, 2.75, 0])
        self.play(swap(loop_txt, hundreds_lbl, run_time=0.45))

        self.at("good money")
        q1 = T("good money?", size=30, color=TEXT, weight=BOLD).move_to([4.55, 1.65, 0])
        self.play(FadeIn(q1, shift=LEFT * 0.15), run_time=0.55)

        self.at("what keeps remaking")
        q2 = T("what remakes it?", size=30, color=TEXT, weight=BOLD).next_to(lift_track, RIGHT, buff=0.45).shift(DOWN * 0.30)
        self.play(FadeIn(q2, shift=LEFT * 0.15), run_time=0.55)
        self.finish()


# ------------------------------------------------------------------ Scene 3
class S03Ladder(SpokenScene):
    def construct(self):
        hill = make_hill()
        tray = make_tray(center=(0.0, 0.44, 0), n_beads=4, show_label=False, width=3.85)
        atp_lbl = T("ATP", size=28, color=YELLOW, weight=BOLD).next_to(tray.wall, UP, buff=0.14)
        tag = scope_tag("schematic")
        self.add(hill, tray, atp_lbl, tag)

        terraces = make_terrace_system(x_left=-3.1, x_right=5.15, ys=(1.90, 0.0, -1.85), with_axis=True)
        self.play(
            ReplacementTransform(hill, terraces.rungs),
            tray.animate.move_to([0.55, 0.48, 0.0]),
            atp_lbl.animate.move_to([0.55, 1.18, 0.0]),
            FadeIn(terraces.axis),
            FadeIn(terraces.axis_label),
            run_time=1.5,
        )

        # Beat 2: Rank phosphorylated compounds
        self.at("Rank phosphorylated compounds")
        d1 = RoundedRectangle(corner_radius=0.12, width=1.65, height=0.68, stroke_color=YELLOW, stroke_width=3.2, fill_color=YELLOW, fill_opacity=0.22).move_to([-1.25, 2.32, 0])
        d2 = d1.copy().move_to([0.65, 2.32, 0])
        donors_lbl = T("richer donors", size=28, color=YELLOW).next_to(d2, RIGHT, buff=0.30)

        a1 = RoundedRectangle(corner_radius=0.12, width=1.65, height=0.68, stroke_color=BLUE, stroke_width=3.2, fill_color=BLUE, fill_opacity=0.22).move_to([-1.25, -1.44, 0])
        a2 = a1.copy().move_to([0.65, -1.44, 0])
        acceptors_lbl = T("acceptors below", size=28, color=BLUE).next_to(a2, RIGHT, buff=0.30)

        self.play(FadeIn(d1), FadeIn(d2), FadeIn(donors_lbl), FadeIn(a1), FadeIn(a2), FadeIn(acceptors_lbl), run_time=0.95)

        # Continuous downward transfer-potential badges outside x_right=5.15 (never touching terraces or labels)
        down_arr = Arrow([6.05, 1.90, 0], [6.05, -1.80, 0], color=GOLD, stroke_width=5.5, buff=0, max_tip_length_to_length_ratio=0.10)
        flow_p = VGroup(*[make_p_badge(GOLD, radius=0.27) for _ in range(5)])
        fp_t = {"t": 0.0}

        def _slide_down(mob, dt):
            fp_t["t"] = (fp_t["t"] + dt * 0.52) % 1.0
            for idx, b in enumerate(mob):
                s = (fp_t["t"] + idx * 0.20) % 1.0
                b.move_to([5.55, 2.15 - s * 3.80, 0.0]).set_opacity(np.sin(PI * s))

        flow_p.add_updater(_slide_down)
        self.add(flow_p)

        # Mid-beat highlight on axis and top/bottom blocks during "free energy each releases"
        self.at("free energy each releases")
        self.play(
            terraces.axis.animate.set_color(GOLD),
            d1.animate.set_stroke(width=5.5).set_fill(opacity=0.38),
            d2.animate.set_stroke(width=5.5).set_fill(opacity=0.38),
            run_time=0.85,
        )
        self.play(
            a1.animate.set_stroke(width=5.5).set_fill(opacity=0.38),
            a2.animate.set_stroke(width=5.5).set_fill(opacity=0.38),
            d1.animate.set_stroke(width=3.2).set_fill(opacity=0.22),
            d2.animate.set_stroke(width=3.2).set_fill(opacity=0.22),
            run_time=0.85,
        )
        self.play(
            terraces.axis.animate.set_color(GREY),
            a1.animate.set_stroke(width=3.2).set_fill(opacity=0.22),
            a2.animate.set_stroke(width=3.2).set_fill(opacity=0.22),
            run_time=0.85,
        )

        # Beat 3: Under standard conditions, transfers run downhill
        self.at("transfers run downhill")
        self.play(GrowArrow(down_arr), run_time=0.7)

        # Beat 4: ATP sits in the middle
        self.at("sits in the middle")
        mid_glow = RoundedRectangle(
            corner_radius=0.14, width=4.20, height=1.40,
            stroke_color=YELLOW, stroke_width=3.5,
        ).move_to([0.55, 0.76, 0.0])
        self.play(Create(mid_glow), run_time=0.55)

        # Beat 5: Compounds above it can recharge ADP
        self.at("Compounds above it")
        adp_bead = make_bead("ADP", GREY, radius=0.41, opacity=0.88, font_size=22).move_to([-2.15, 0.48, 0])
        self.play(FadeOut(mid_glow), FadeIn(adp_bead), run_time=0.45)
        b_top = make_p_badge(GOLD).move_to([-1.25, 2.25, 0])
        self.play(FadeIn(b_top), run_time=0.2)
        self.play(b_top.animate.move_to([-2.15, 1.15, 0]), run_time=0.85)
        atp_recharged = make_bead("ATP", YELLOW, radius=0.41, font_size=22).move_to([-2.15, 0.48, 0])
        self.play(FadeOut(b_top), run_time=0.2)
        self.play(swap(adp_bead, atp_recharged, run_time=0.4))

        # Beat 6: ATP, in turn, phosphorylates compounds below it
        self.at("phosphorylates compounds below")
        b_mid = make_p_badge(GOLD).move_to([0.65, -0.25, 0])
        self.play(FadeIn(b_mid), run_time=0.2)
        self.play(b_mid.animate.move_to([0.65, -0.92, 0]), run_time=0.8)
        self.play(
            FadeOut(b_mid),
            a2.animate.set_stroke(GREEN, width=4).set_fill(GREEN, opacity=0.35),
            run_time=0.4,
        )

        drop_badges = VGroup(make_p_badge(GOLD, radius=0.22), make_p_badge(GOLD, radius=0.22))
        drop_state = {"t": 0.0}

        def _drop_loop(mob, dt):
            drop_state["t"] = (drop_state["t"] + dt * 0.45) % 1.0
            s = drop_state["t"]
            mob[0].move_to([-2.15, 1.65 - s * 0.50, 0.0]).set_opacity(np.sin(PI * s))
            mob[1].move_to([0.65, -0.22 - s * 0.80, 0.0]).set_opacity(np.sin(PI * s))

        drop_badges.add_updater(_drop_loop)
        self.add(drop_badges)
        self.finish()


# ------------------------------------------------------------------ Scene 4
class S04Idea(SpokenScene):
    def construct(self):
        terraces = make_terrace_system(x_left=-3.1, x_right=5.15, ys=(1.90, 0.0, -1.85), with_axis=True)
        tray = make_tray(center=(0.55, 0.48, 0), n_beads=4, show_label=False, width=3.85)
        atp_lbl = T("ATP", size=28, color=YELLOW, weight=BOLD).move_to([0.55, 1.18, 0.0])

        d1 = RoundedRectangle(corner_radius=0.12, width=1.65, height=0.68, stroke_color=YELLOW, stroke_width=3.2, fill_color=YELLOW, fill_opacity=0.22).move_to([-1.25, 2.32, 0])
        d2 = d1.copy().move_to([0.65, 2.32, 0])
        donors_lbl = T("richer donors", size=28, color=YELLOW).next_to(d2, RIGHT, buff=0.30)

        a1 = RoundedRectangle(corner_radius=0.12, width=1.65, height=0.68, stroke_color=BLUE, stroke_width=3.2, fill_color=BLUE, fill_opacity=0.22).move_to([-1.25, -1.44, 0])
        a2 = a1.copy().move_to([0.65, -1.44, 0])
        acceptors_lbl = T("acceptors below", size=28, color=BLUE).next_to(a2, RIGHT, buff=0.30)

        arr_top = Arrow([-1.85, 1.85, 0], [-1.85, 0.55, 0], color=GOLD, stroke_width=5, buff=0)
        arr_bot = Arrow([1.85, -0.05, 0], [1.85, -1.15, 0], color=GREEN, stroke_width=5, buff=0)
        tag = scope_tag("schematic")

        # 4 continuous downward P badges (2 per drop lane, spaced 0.50 in phase), clear of all labels
        drop_badges = VGroup(*[make_p_badge(GOLD, radius=0.22) for _ in range(4)])
        drop_state = {"t": 0.0}

        def _drop_loop(mob, dt):
            drop_state["t"] = (drop_state["t"] + dt * 0.52) % 1.0
            for idx, b in enumerate(mob):
                s = (drop_state["t"] + (idx // 2) * 0.50) % 1.0
                if idx % 2 == 0:
                    b.move_to([-2.45, 1.65 - s * 1.15, 0.0]).set_opacity(np.sin(PI * s))
                else:
                    b.move_to([5.55, -0.20 - s * 1.25, 0.0]).set_opacity(np.sin(PI * s))

        drop_badges.add_updater(_drop_loop)
        terraces.rungs[1][1].set_color(YELLOW).set_stroke(width=7)

        self.add(terraces, tray, atp_lbl, d1, d2, donors_lbl, a1, a2, acceptors_lbl, arr_top, arr_bot, drop_badges, tag)

        # Beat 2: refilled from above
        self.at("refilled from above")
        self.play(
            arr_top.animate.set_stroke(width=10).set_color(YELLOW),
            tray.wall.animate.set_stroke(width=7),
            terraces.rungs[1][1].animate.set_stroke(width=10),
            run_time=0.5,
        )
        self.play(
            arr_top.animate.set_stroke(width=5).set_color(GOLD),
            tray.wall.animate.set_stroke(width=4),
            terraces.rungs[1][1].animate.set_stroke(width=7),
            run_time=0.5,
        )

        # Beat 3: pay for jobs below
        self.at("pay for jobs below")
        self.play(
            arr_bot.animate.set_stroke(width=10),
            tray.wall.animate.set_stroke(width=7),
            terraces.rungs[1][1].animate.set_stroke(width=10),
            run_time=0.5,
        )
        self.play(
            arr_bot.animate.set_stroke(width=5),
            tray.wall.animate.set_stroke(width=4),
            terraces.rungs[1][1].animate.set_stroke(width=7),
            run_time=0.5,
        )

        # Beat 4: Here is the idea to hold -> swap bottom blocks for work icons cleanly
        self.at("Here is the idea")
        work_icons = make_work_icons(y=-1.85, xs=(-1.3, 0.7, 2.7), size=26)
        self.play(
            Succession(
                FadeOut(VGroup(a1, a2, acceptors_lbl), run_time=0.35),
                FadeIn(work_icons, run_time=0.45),
            )
        )

        # Beat 5: ATP is cash, not savings
        self.at("cash not savings")
        headline = T("ATP: cash, not savings", size=38, color=TEXT, weight=BOLD).move_to([0.95, 3.08, 0])
        self.play(FadeIn(headline, shift=DOWN * 0.1), run_time=0.55)

        # Beat 6: spent on the cell's work -> three work icons light in turn
        self.at("cell's work")
        for item in work_icons:
            item.glyph.set_color(GREEN)
            item.label.set_color(GREEN)
            self.wait(0.28)

        # Beat 7: remade by burning fuel
        self.at("burning fuel")
        lift = make_fuel_lift(x=-4.45, y_bot=-1.85, y_top=0.0, width=0.92, show_label=True, glow_opacity=0.85)
        self.play(FadeIn(lift, shift=UP * 0.2), run_time=0.70)
        g_t = {"v": 0.0}
        lift.glow.add_updater(lambda m, dt: (g_t.update(v=g_t["v"] + dt * 3.5), m.set_fill(opacity=0.35 + 0.28 * np.sin(g_t["v"]))))
        self.finish()


# ------------------------------------------------------------------ Scene 5
class S05Converge(SpokenScene):
    def construct(self):
        right_world = make_compact_right_world(x0=2.65, x1=6.18, ys=(1.60, 0.05, -1.50), show_labels=True, glow_op=0.8)
        right_world.shift(LEFT * 1.3)
        tag = scope_tag("schematic")
        self.add(right_world, tag)

        self.play(right_world.animate.shift(RIGHT * 1.3), run_time=1.2)

        g_t = {"v": 0.0}
        right_world.lift.glow.add_updater(lambda m, dt: (g_t.update(v=g_t["v"] + dt * 3.5), m.set_fill(opacity=0.35 + 0.28 * np.sin(g_t["v"]))))

        self.at("in three stages")
        steak_icon = VGroup(
            RoundedRectangle(corner_radius=0.20, width=1.45, height=0.70, stroke_color=TEXT, stroke_width=2.5, fill_color=RED, fill_opacity=0.24),
            T("steak", size=24, color=TEXT),
        )
        steak_icon[1].move_to(steak_icon[0])
        steak_icon.move_to([-5.25, 2.25, 0])

        potato_icon = VGroup(
            Ellipse(width=1.54, height=0.74, stroke_color=TEXT, stroke_width=2.5, fill_color=GOLD, fill_opacity=0.22),
            T("potato", size=24, color=TEXT),
        )
        potato_icon[1].move_to(potato_icon[0])
        potato_icon.move_to([-5.25, 0.55, 0])

        oil_icon = VGroup(
            RoundedRectangle(corner_radius=0.18, width=1.58, height=0.70, stroke_color=TEXT, stroke_width=2.5, fill_color=YELLOW, fill_opacity=0.20),
            T("olive oil", size=24, color=TEXT),
        )
        oil_icon[1].move_to(oil_icon[0])
        oil_icon.move_to([-5.25, -1.15, 0])

        plaza = boxed_label("acetyl-CoA", color=GOLD, size=30, pad=0.28, stroke=4, fill_opacity=0.24).move_to([0.90, 0.55, 0])
        self.play(FadeIn(steak_icon), FadeIn(potato_icon), FadeIn(oil_icon), FadeIn(plaza), run_time=0.95)

        self.at("Digestion breaks")
        p_top = CubicBezier([-4.40, 2.25, 0], [-2.5, 2.25, 0], [-1.3, 1.35, 0], [-0.25, 0.80, 0], color=BLUE, stroke_width=4.5)
        p_mid = CubicBezier([-4.40, 0.55, 0], [-2.5, 0.55, 0], [-1.3, 0.55, 0], [-0.25, 0.55, 0], color=BLUE, stroke_width=4.5)
        p_bot = CubicBezier([-4.40, -1.15, 0], [-2.5, -1.15, 0], [-1.3, -0.25, 0], [-0.25, 0.30, 0], color=BLUE, stroke_width=4.5)

        lbl_aa = T("amino acids", size=26, color=BLUE).move_to([-2.75, 2.75, 0])
        lbl_sug = T("sugars", size=26, color=BLUE).move_to([-2.75, 0.98, 0])
        lbl_fa = T("fatty acids", size=26, color=BLUE).move_to([-2.75, -1.68, 0])

        stream_beads = VGroup(*[Dot(radius=0.15, color=BLUE) for _ in range(15)])
        stream_beads.layout_ok = True
        paths = [p_top, p_mid, p_bot]
        st = {"t": 0.0}

        def _stream_upd(mob, dt):
            st["t"] += dt * 0.45
            for i, d in enumerate(mob):
                p = paths[i % 3]
                u = (st["t"] + (i // 3) * 0.20) % 1.0
                d.move_to(p.point_from_proportion(u))

        stream_beads.add_updater(_stream_upd)
        self.play(Create(p_top), Create(p_mid), Create(p_bot), FadeIn(lbl_aa), FadeIn(lbl_sug), FadeIn(lbl_fa), run_time=1.2)
        self.add(stream_beads)

        self.at("funnels into one")
        branch_curve = CubicBezier([-1.05, 1.38, 0], [-0.85, -0.95, 0], [-0.40, -1.85, 0], [1.10, -1.85, 0])
        branch = DashedVMobject(branch_curve.copy().set_stroke(BLUE, 3.0), num_dashes=16)
        branch_lbl = T("some enter elsewhere", size=24, color=BLUE).move_to([-1.2, -2.42, 0])
        branch_dots = VGroup(*[Dot(radius=0.11, color=BLUE) for _ in range(3)])
        branch_dots.layout_ok = True
        bt = {"t": 0.0}
        branch_dots.add_updater(lambda m, dt: (bt.update(t=bt["t"] + dt * 0.35), [d.move_to(branch_curve.point_from_proportion((bt["t"] + i / 3) % 1.0)) for i, d in enumerate(m)]))

        self.play(Create(branch), FadeIn(branch_lbl), plaza.box.animate.set_stroke(width=6), run_time=0.95)
        self.add(branch_dots)

        self.at("Different highways")
        self.finish()


# ------------------------------------------------------------------ Scene 6
class S06Electrons(SpokenScene):
    def construct(self):
        right_world = make_compact_right_world(x0=2.65, x1=6.18, ys=(1.60, 0.05, -1.50), show_labels=True, glow_op=0.25)
        tag = scope_tag("schematic")

        acetyl = boxed_label("acetyl-CoA", color=GOLD, size=28, pad=0.22).move_to([-4.65, 2.55, 0])
        wheel = make_wheel(center=(-2.8, 0.15, 0), radius=1.70)
        wheel_lbl = T("citric acid cycle", size=28, color=TEXT, weight=BOLD).move_to([-2.8, -2.02, 0])
        feed_arr = Arrow([-4.15, 2.12, 0], [-3.55, 1.55, 0], color=GOLD, stroke_width=4, buff=0)

        wheel.rot.add_updater(lambda m, dt: m.rotate(-0.65 * dt, about_point=wheel.center_pt))
        self.add(right_world, acetyl, feed_arr, wheel, wheel_lbl, tag)

        # Beat 2: carbon dioxide -> two small grey-outlined dark-filled CO2 puffs
        self.at("carbon dioxide")
        co2_1 = VGroup(Circle(radius=0.48, stroke_color=GREY, stroke_width=2.5, fill_color=BG, fill_opacity=0.92), T("CO₂", size=24, color=TEXT)).move_to([-1.6, 2.05, 0])
        co2_1[1].move_to(co2_1[0])
        co2_2 = co2_1.copy().move_to([-0.55, 2.25, 0])
        self.play(FadeIn(co2_1, shift=UP * 0.25), FadeIn(co2_2, shift=UP * 0.35), run_time=0.75)
        self.play(co2_1.animate.shift(UP * 0.55), co2_2.animate.shift(UP * 0.60), run_time=0.85)

        # Beat 3: electrons stripped -> TEAL sparks jump from wheel to YELLOW NADH & FADH2 trucks
        self.at("The electrons it strips")
        nadh = make_truck("NADH", center=(0.45, 1.25, 0), color=YELLOW)
        fadh = make_truck("FADH₂", center=(0.45, -0.15, 0), color=YELLOW)
        self.play(FadeIn(nadh), FadeIn(fadh), run_time=0.65)

        self.at("NADH and FADH2")
        sparks = VGroup(*[Dot(radius=0.12, color=TEAL) for _ in range(6)])
        sparks.layout_ok = True
        sp_t = {"t": 0.0}

        def _spark_jump(mob, dt):
            sp_t["t"] += dt * 0.9
            for i, d in enumerate(mob):
                s = (sp_t["t"] + i / 3) % 1.0
                tgt = nadh.get_left() if i % 2 == 0 else fadh.get_left()
                src = np.array([-1.15, 0.85 if i % 2 == 0 else -0.25, 0.0])
                d.move_to(src + s * (tgt - src) + UP * 0.22 * np.sin(PI * s))

        sparks.add_updater(_spark_jump)
        self.add(sparks)

        # Beat 4: Handing those electrons onto oxygen -> trucks drive to O2 block at lift base
        self.at("Handing those electrons")
        o2_block = boxed_label("O₂", color=RED, size=26, pad=0.18).move_to([1.65, -2.0, 0])
        self.play(FadeIn(o2_block), run_time=0.4)
        sparks.clear_updaters()
        self.play(FadeOut(sparks), nadh.animate.move_to([0.20, -1.35, 0]), fadh.animate.move_to([0.20, -2.45, 0]), run_time=0.8)

        # Beat 5: drives ATP synthesis
        self.at("drives")
        right_world.lift.glow.set_fill(ORANGE, opacity=0.65).set_stroke(ORANGE, opacity=0.95)
        o2_sparks = VGroup(*[Dot(radius=0.12, color=TEAL) for _ in range(4)])
        o2_sparks.layout_ok = True
        os_t = {"t": 0.0}

        def _to_o2(mob, dt):
            os_t["t"] += dt * 1.1
            for i, d in enumerate(mob):
                s = (os_t["t"] + (i // 2) * 0.5) % 1.0
                src = nadh.get_right() if i % 2 == 0 else fadh.get_right()
                d.move_to(src + s * (o2_block.get_left() - src))

        o2_sparks.add_updater(_to_o2)
        self.add(o2_sparks)

        lift_x_world = right_world.lift.shaft.get_center()[0]
        lift_yb = right_world.lift.shaft.get_bottom()[1] + 0.1
        lift_yt = right_world.lift.shaft.get_top()[1] - 0.1
        tray_pt = right_world.tray.get_center()

        lifted_beads = VGroup(*[Dot(radius=0.13, color=GREY) for _ in range(4)])
        lifted_beads.layout_ok = True
        lb_t = {"t": 0.0}

        def _lift_run(mob, dt):
            lb_t["t"] += dt * 0.45
            for i, d in enumerate(mob):
                u = (lb_t["t"] + i * 0.25) % 1.0
                if u < 0.65:
                    s = u / 0.65
                    d.move_to([lift_x_world, lift_yb + s * (lift_yt - lift_yb), 0.0])
                    d.set_color(GREY if s < 0.75 else YELLOW)
                else:
                    s = (u - 0.65) / 0.35
                    d.move_to([lift_x_world + s * (tray_pt[0] - lift_x_world), lift_yt + s * (tray_pt[1] - lift_yt), 0.0])
                    d.set_color(YELLOW)

        lifted_beads.add_updater(_lift_run)
        self.add(lifted_beads)
        self.finish()


# ------------------------------------------------------------------ Predict backdrop helper
def _predict_backdrop():
    """Shared moving world + two carbon tokens + empty spark meters for s07, s08, s09."""
    wheel = make_wheel(center=(-4.95, -0.10, 0), radius=1.10, opacity=0.45)
    wheel_lbl = T("citric acid cycle", size=22, color=GREY).move_to([-4.95, -1.65, 0]).set_opacity(0.65)
    wheel.rot.add_updater(lambda m, dt: m.rotate(-0.45 * dt, about_point=wheel.center_pt))

    right_world = make_compact_right_world(x0=3.75, x1=6.18, ys=(1.25, 0.05, -1.15), show_labels=False, glow_op=0.45)
    # Spread the 3 compact icons cleanly across x = 4.60 .. 5.85
    for idx, x_new in enumerate((4.60, 5.22, 5.84)):
        right_world.work_icons[idx].set_x(x_new)
    right_world.atp_lbl.set_opacity(0.50)
    right_world.terraces.set_opacity(0.45)
    right_world.tray.wall.set_stroke(opacity=0.45)
    right_world.lift.shaft.set_stroke(opacity=0.45)

    fa_tok = make_carbon_token("fatty acid carbon", center=(-1.65, 1.10, 0), radius=0.82)
    gl_tok = make_carbon_token("glucose carbon", center=(1.65, 1.10, 0), radius=0.82)

    m_fa = make_spark_meter(center=(-1.65, -0.62, 0), fill_frac=0.0, width=2.45, height=0.44, flicker=True)
    m_gl = make_spark_meter(center=(1.65, -0.62, 0), fill_frac=0.0, width=2.45, height=0.44, flicker=True)
    tag = scope_tag("schematic")
    return VGroup(wheel, wheel_lbl, right_world, tag), fa_tok, gl_tok, m_fa, m_gl


# ------------------------------------------------------------------ Scene 7
class S07Predict(SpokenScene):
    def construct(self):
        bg_world, fa_tok, gl_tok, m_fa, m_gl = _predict_backdrop()
        self.add(bg_world)

        self.at("Take one carbon")
        self.play(FadeIn(fa_tok, shift=UP * 0.4), FadeIn(m_fa), run_time=0.9)

        self.at("one carbon from glucose")
        self.play(FadeIn(gl_tok, shift=UP * 0.4), FadeIn(m_gl), run_time=0.9)

        self.at("Which one has more")
        q = question_card("Which carbon has more to give?", y=3.08, color=TEXT, size=38)
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------ Scene 8
class S08PredictHold(PredictPause):
    QUESTION = "Which carbon has more to give?"
    CARD = {"y": 3.08, "color": TEXT, "size": 38}
    RING_AT = (5.85, -2.30, 0)
    SECONDS = 4.5

    def backdrop(self):
        bg_world, fa_tok, gl_tok, m_fa, m_gl = _predict_backdrop()
        fl = {"t": 0.0}

        def _flicker(m, dt):
            fl["t"] += dt * 4.5
            m.bg.set_stroke(opacity=0.6 + 0.35 * np.sin(fl["t"]))

        m_fa.add_updater(_flicker)
        m_gl.add_updater(lambda m, dt: m.bg.set_stroke(opacity=0.6 + 0.35 * np.sin(fl["t"] + 1.2)))
        return VGroup(bg_world, fa_tok, gl_tok, m_fa, m_gl)


# ------------------------------------------------------------------ Scene 9
class S09Answer(SpokenScene):
    def construct(self):
        bg_world, fa_tok, gl_tok, m_fa, m_gl = _predict_backdrop()
        self.add(bg_world, fa_tok, gl_tok, m_fa, m_gl)

        fa_hi = Circle(radius=0.94, stroke_color=TEAL, stroke_width=3.5).move_to(fa_tok.ring)
        self.play(Create(fa_hi), run_time=0.5)

        self.at("loaded with hydrogens")
        h_offsets = [UP * 1.12, LEFT * 1.12, UL * 0.86 + UP * 0.1]
        h_tags = VGroup()
        for off in h_offsets:
            hb = boxed_label("H", color=TEXT, size=24, pad=0.10, corner_radius=0.14).move_to(fa_tok.ring.get_center() + off)
            h_tags.add(hb)

        carrier = make_truck("NADH / FADH₂", center=(0.0, -1.65, 0), color=YELLOW)
        self.play(
            FadeOut(fa_hi),
            FadeIn(h_tags, lag_ratio=0.15),
            m_fa.tracker.animate.set_value(0.90),
            FadeIn(carrier),
            run_time=1.25,
        )

        # Start streaming TEAL sparks immediately from fatty acid to carrier truck
        sp_mode = {"gl_on": False}
        sparks = VGroup(*[Dot(radius=0.12, color=TEAL) for _ in range(8)])
        sparks.layout_ok = True
        sp_t = {"t": 0.0}

        def _stream(mob, dt):
            sp_t["t"] += dt * 0.90
            for i, d in enumerate(mob):
                if i < 5 or not sp_mode["gl_on"]:
                    s = (sp_t["t"] + (i % 5) * 0.20) % 1.0
                    src = m_fa.bg.get_bottom() + RIGHT * 0.45
                    tgt = carrier.get_top() + LEFT * 0.40
                else:
                    s = (sp_t["t"] + (i - 5) * 0.33) % 1.0
                    src = m_gl.bg.get_bottom() + LEFT * 0.45
                    tgt = carrier.get_top() + RIGHT * 0.40
                d.move_to(src + s * (tgt - src))
                d.set_opacity(np.sin(PI * s))

        sparks.add_updater(_stream)
        self.add(sparks)

        self.at("bonded to oxygen")
        o_tag = boxed_label("O", color=RED, size=24, pad=0.10, corner_radius=0.14).move_to(gl_tok.ring.get_center() + RIGHT * 1.12)
        self.play(FadeIn(o_tag, shift=LEFT * 0.15), m_gl.tracker.animate.set_value(0.40), run_time=1.05)
        sp_mode["gl_on"] = True

        # Beat 4: fat ~9 kcal/g, carbohydrate ~4 kcal/g (exact 2.25 : 1 height ratio, clear of center truck)
        self.at("fat yields about 9")
        base_y = -2.42
        bar_scale = 0.14  # 9 * 0.14 = 1.26, 4 * 0.14 = 0.56 -> exact 2.25 ratio
        val_fat = ValueTracker(0.0)
        val_carb = ValueTracker(0.0)

        bar_fat = always_redraw(
            lambda: Rectangle(
                width=1.10, height=max(0.04, val_fat.get_value() * bar_scale),
                stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.68,
            ).align_to([0, base_y, 0], DOWN).set_x(-2.70)
        )
        bar_carb = always_redraw(
            lambda: Rectangle(
                width=1.10, height=max(0.04, val_carb.get_value() * bar_scale),
                stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.42,
            ).align_to([0, base_y, 0], DOWN).set_x(2.70)
        )
        lbl_fat = always_redraw(
            lambda: T(f"fat ~{val_fat.get_value():.0f} kcal/g", size=24, color=BLUE).move_to([-2.70, base_y - 0.34, 0])
        )
        lbl_carb = always_redraw(
            lambda: T(f"carbohydrate ~{val_carb.get_value():.0f} kcal/g", size=24, color=BLUE).move_to([2.70, base_y - 0.34, 0])
        )

        self.add(bar_fat, lbl_fat)
        self.play(val_fat.animate.set_value(9.0), run_time=1.2)

        self.at("carbohydrate about 4")
        self.add(bar_carb, lbl_carb)
        self.play(val_carb.animate.set_value(4.0), run_time=1.0)
        self.finish()


# ------------------------------------------------------------------ Scene 10
class S10Return(SpokenScene):
    def construct(self):
        terraces = make_terrace_system(x_left=-0.1, x_right=5.95, ys=(1.95, 0.20, -1.65), with_axis=False)
        tray = make_tray(center=(2.95, 0.70, 0.0), n_beads=4, show_label=True, label_text="ATP in body", width=3.85)
        under_lbl = T("under 1 kg", size=26, color=YELLOW).move_to([2.95, -0.22, 0])
        work_icons = make_work_icons(y=-1.65, xs=(1.1, 2.95, 4.8), size=24)
        for item in work_icons:
            item.glyph.set_color(GREEN)
            item.label.set_color(GREEN)
            item.label.move_to([item.glyph.get_center()[0], -2.10, 0])

        lift = make_fuel_lift(x=-1.05, y_bot=-1.65, y_top=0.20, width=0.92, show_label=True, glow_opacity=0.8)

        s1 = CubicBezier([-5.8, 2.0, 0], [-4.0, 1.9, 0], [-2.8, 0.9, 0], [-1.55, 0.45, 0], color=BLUE, stroke_width=4)
        s2 = CubicBezier([-5.8, 1.0, 0], [-4.0, 1.0, 0], [-2.8, 0.6, 0], [-1.55, 0.25, 0], color=BLUE, stroke_width=4)
        fuel_lbl = T("fuel streams", size=26, color=BLUE).move_to([-4.1, 2.45, 0])
        tag = scope_tag("schematic")

        fuel_dots = VGroup(*[Dot(radius=0.14, color=BLUE) for _ in range(8)])
        fuel_dots.layout_ok = True
        ft = {"t": 0.0}
        fpaths = [s1, s2]

        def _fuel_upd(mob, dt):
            ft["t"] += dt * 0.42
            for i, d in enumerate(mob):
                p = fpaths[i % 2]
                d.move_to(p.point_from_proportion((ft["t"] + (i // 2) * 0.25) % 1.0))

        fuel_dots.add_updater(_fuel_upd)
        self.add(terraces, tray, under_lbl, work_icons, lift, s1, s2, fuel_lbl, fuel_dots, tag)

        # Beat 2: Fat -> wide BLUE-outlined vault cleanly enclosing 'fat: long-term store'
        self.at("Fat is its main")
        vault_box = RoundedRectangle(corner_radius=0.16, width=4.45, height=1.75, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.22).move_to([-3.95, -1.40, 0])
        vault_ring = Circle(radius=0.26, stroke_color=BLUE, stroke_width=3).move_to([-5.62, -1.40, 0])
        vault_spoke = Line([-5.80, -1.40, 0], [-5.44, -1.40, 0], color=BLUE, stroke_width=2.5)
        vault_lbl = T("fat: long-term store", size=24, color=BLUE, weight=BOLD).move_to([-3.55, -1.12, 0])
        savings_lbl = T("savings", size=24, color=TEXT).move_to([-3.55, -1.65, 0])
        vault = VGroup(vault_box, vault_ring, vault_spoke, vault_lbl, savings_lbl)
        self.play(FadeIn(vault, shift=UP * 0.25), run_time=0.9)

        # Beat 3: small pool of cash -> tray glows YELLOW
        self.at("small pool of cash")
        tray_glow = SurroundingRectangle(tray, color=YELLOW, buff=0.12, corner_radius=0.14, stroke_width=4)
        self.play(Create(tray_glow), run_time=0.55)
        self.play(FadeOut(tray_glow), run_time=0.45)

        # Beat 4: Work keeps spending it, and burning fuel keeps paying it back -> continuous ATP/ADP loop
        self.at("Work keeps spending")
        loop_beads = VGroup(*[Dot(radius=0.14, color=YELLOW) for _ in range(6)])
        loop_beads.layout_ok = True
        lp_t = {"t": 0.0}

        def _full_loop(mob, dt):
            lp_t["t"] += dt * 0.26
            for i, d in enumerate(mob):
                u = (lp_t["t"] + i / len(mob)) % 1.0
                if u < 0.32:
                    s = u / 0.32
                    tgt_x = [1.1, 2.95, 4.8][i % 3]
                    start_x = 4.90 if i % 3 != 0 else 1.00
                    p = np.array([start_x + s * (tgt_x - start_x), 0.55 - s * 1.90, 0.0])
                    d.move_to(p).set_color(YELLOW if s < 0.85 else GREY)
                elif u < 0.62:
                    s = (u - 0.32) / 0.30
                    src_x = [1.1, 2.95, 4.8][i % 3]
                    p = np.array([src_x + s * (-1.05 - src_x), -1.40 - 0.12 * np.sin(PI * s), 0.0])
                    d.move_to(p).set_color(GREY)
                elif u < 0.85:
                    s = (u - 0.62) / 0.23
                    p = np.array([-1.05, -1.55 + s * 1.95, 0.0])
                    d.move_to(p).set_color(GREY if s < 0.75 else YELLOW)
                else:
                    s = (u - 0.85) / 0.15
                    p = np.array([-1.05 + s * (1.00 + 1.05), 0.48 + 0.15 * np.sin(PI * s), 0.0])
                    d.move_to(p).set_color(YELLOW)

        loop_beads.add_updater(_full_loop)
        self.add(loop_beads)
        self.finish()


# ------------------------------------------------------------------ Scene 11
class S11End(EndCard):
    LINE = "ATP is cash, not savings: spent by work, remade by fuel."
