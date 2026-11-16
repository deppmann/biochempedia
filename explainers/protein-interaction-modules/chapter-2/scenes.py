"""Two grips, one decision.

COLOR MAP (shared with chapter 1)
  BLUE  = proteins and receptor outlines
  GOLD  = phosphates
  TEAL  = binding domains
  GREEN = matching motifs and lipids
  RED   = failed contacts
  GREY  = neutral structure and secondary labels

All cartoons are schematic.  The Src clamp and detector are rebuilt by the same
builder functions whenever they carry across a cut.
"""
import numpy as np
from bp_parts import *  # noqa: F401,F403


# ---------------------------------------------------------------------------
# Shared drawing vocabulary

def phosphate(r=0.25):
    disk = Circle(radius=r, stroke_color=GOLD, stroke_width=3,
                  fill_color=GOLD, fill_opacity=1)
    return VGroup(disk, T("P", 24, BG, weight=BOLD).move_to(disk))


def module(label, width=1.35, height=0.85, notch="round"):
    """A labelled teal binding module; the small notch makes it an acting grip."""
    box = RoundedRectangle(corner_radius=0.2, width=width, height=height,
                           stroke_color=TEAL, stroke_width=5,
                           fill_color=TEAL, fill_opacity=0.16)
    grip_center = box.get_right() + RIGHT * 0.22
    if notch == "round":
        grip = Arc(radius=0.19, start_angle=-PI / 2, angle=PI,
                   color=TEAL, stroke_width=6).move_arc_center_to(grip_center)
    else:
        grip = VGroup(Line(box.get_right() + RIGHT * 0.12 + UP * 0.22,
                           box.get_right() + RIGHT * 0.34,
                           color=TEAL, stroke_width=6),
                      Line(box.get_right() + RIGHT * 0.12 + DOWN * 0.22,
                           box.get_right() + RIGHT * 0.34,
                           color=TEAL, stroke_width=6))
    return VGroup(box, grip, T(label, 28, TEAL, weight=BOLD).move_to(box))


def flexible_line(points, color=BLUE, width=7):
    line = VMobject(stroke_color=color, stroke_width=width, fill_opacity=0)
    line.set_points_smoothly([np.array([x, y, 0.0]) for x, y in points])
    return line


def kinase(center=(1.15, 0, 0), active=False, scale=1.0):
    box = RoundedRectangle(corner_radius=0.34, width=3.1 * scale, height=2.05 * scale,
                           stroke_color=BLUE, stroke_width=5,
                           fill_color=BLUE, fill_opacity=0.34 if active else 0.11).move_to(center)
    label = T("kinase", 32 * scale, BLUE, weight=BOLD).move_to(box)
    return VGroup(box, label)


def open_src(y=0.1):
    """The carried open Src strip used at the start of the clamp story."""
    body = RoundedRectangle(corner_radius=0.42, width=11.4, height=2.25,
                            stroke_width=0, fill_color=BLUE, fill_opacity=0.20).move_to([0.15, y, 0])
    body.set_z_index(-2)
    sh3 = module("SH3", 1.35, 0.9, "angle").move_to([-4.75, y, 0])
    sh2 = module("SH2", 1.35, 0.9, "round").move_to([-2.85, y, 0])
    link = flexible_line([(-2.15, y), (-1.72, y + 0.12), (-1.3, y)], GREEN, 7)
    kin = RoundedRectangle(corner_radius=0.24, width=3.05, height=1.25,
                           stroke_color=BLUE, stroke_width=5, fill_color=BLUE,
                           fill_opacity=0.18).move_to([0.35, y, 0])
    kl = T("kinase", 32, BLUE, weight=BOLD).move_to(kin)
    tail = flexible_line([(1.9, y), (2.65, y + 0.18), (3.45, y - 0.18),
                          (4.35, y + 0.14), (5.25, y)], BLUE, 7)
    end = Dot([5.25, y, 0], radius=0.18, color=BLUE)
    group = VGroup(body, sh3, sh2, link, kin, kl, tail, end)
    return dict(group=group, sh3=sh3, sh2=sh2, linker=link,
                kinase=VGroup(kin, kl), tail=tail, end=end, body=body)


def compact_src(active=False, scale=1.0, shift=ORIGIN, include_status=True):
    """The one canonical compact Src clamp, reused through the prediction."""
    sh = np.array(shift, dtype=float)
    kin = kinase((1.15, -0.15, 0), active=active, scale=1.0)
    sh2 = module("SH2", 1.45, 0.92, "round").move_to([-2.05, 0.78, 0])
    sh3 = module("SH3", 1.45, 0.92, "angle").move_to([-2.05, -1.12, 0])
    linker = flexible_line([(-1.15, -1.12), (-0.55, -0.9), (-0.35, -0.45)], GREEN, 8)
    tail = flexible_line([(2.7, 0.2), (3.45, 0.7), (3.0, 1.72),
                          (1.25, 2.15), (-0.2, 1.95), (-0.63, 1.47)], BLUE, 8)
    p = phosphate(0.25).move_to([-0.9, 1.47, 0])
    contact2 = Line([-1.22, 1.03, 0], [-1.08, 1.28, 0], color=TEAL, stroke_width=8)
    contact3 = Line([-1.18, -1.12, 0], [-0.92, -1.12, 0], color=TEAL, stroke_width=8)
    body = RoundedRectangle(corner_radius=0.48, width=7.4, height=4.75,
                            stroke_width=0, fill_color=BLUE, fill_opacity=0.20).move_to([0.2, 0.05, 0])
    body.set_z_index(-2)
    pieces = [body, kin, sh2, sh3, linker, tail, p, contact2, contact3]
    status = None
    if include_status:
        status = boxed_label("inactive shape", BLUE, 28, fill_opacity=0.12).move_to([4.8, -1.65, 0])
        pieces.append(status)
    group = VGroup(*pieces).scale(scale).shift(sh)
    return dict(group=group, kinase=kin, sh2=sh2, sh3=sh3, linker=linker,
                tail=tail, phosphate=p, c2=contact2, c3=contact3, status=status, body=body)


def external_target(at=(4.55, 1.45, 0), scale=1.0):
    bar = RoundedRectangle(corner_radius=0.22, width=2.7 * scale, height=0.82 * scale,
                           stroke_color=BLUE, stroke_width=5,
                           fill_color=BLUE, fill_opacity=0.15).move_to(at)
    p = phosphate(0.23 * scale).move_to(bar.get_left() + RIGHT * 0.62 * scale)
    motifs = VGroup(*[Square(side_length=0.24 * scale, stroke_color=GREEN, stroke_width=3,
                              fill_color=GREEN, fill_opacity=0.65) for _ in range(3)])
    motifs.arrange(RIGHT, buff=0.09 * scale).move_to(bar.get_center() + RIGHT * 0.55 * scale)
    return VGroup(bar, p, motifs)


def detector_world(detector_at=(0.35, 1.25, 0), both=True, receptor=True, lipid=True, scale=1.0):
    """The canonical two-input detector world used in scenes 10--12."""
    mem = RoundedRectangle(corner_radius=0.12, width=11.6 * scale, height=0.38 * scale,
                           stroke_color=BLUE, stroke_width=4,
                           fill_color=BLUE, fill_opacity=0.16).move_to([0, -2.0, 0])
    parts = [mem]
    rec = p = lip = None
    if receptor:
        rec = RoundedRectangle(corner_radius=0.18, width=0.62 * scale, height=3.2 * scale,
                               stroke_color=BLUE, stroke_width=5,
                               fill_color=BLUE, fill_opacity=0.18).move_to([-2.25, -0.55, 0])
        p = phosphate(0.25 * scale).move_to([-2.25, 0.82, 0])
        parts += [rec, p]
    if lipid:
        lip = VGroup(Circle(radius=0.25 * scale, stroke_color=GREEN, stroke_width=4,
                            fill_color=GREEN, fill_opacity=0.55).move_to([2.25, -1.7, 0]),
                     Line([2.25, -1.88, 0], [2.25, -2.25, 0], color=GREEN, stroke_width=5))
        parts.append(lip)
    sh2 = module("SH2", 1.32 * scale, 0.82 * scale, "round").move_to([-1.0, 0, 0])
    ph = module("PH", 1.32 * scale, 0.82 * scale, "angle").move_to([1.0, 0, 0])
    link = flexible_line([(-0.28, 0), (0, 0.18), (0.28, 0)], BLUE, 6 * scale)
    host = RoundedRectangle(corner_radius=0.34, width=4.7, height=1.55,
                            stroke_width=0, fill_color=BLUE, fill_opacity=0.22)
    host.set_z_index(-2)
    detector = VGroup(host, sh2, link, ph).move_to(detector_at)
    parts.append(detector)
    group = VGroup(*parts)
    return dict(group=group, membrane=mem, receptor=rec, phosphate=p, lipid=lip,
                detector=detector, sh2=sh2, ph=ph, linker=link, host=host)


def prediction_world(drift=False):
    src = compact_src(include_status=False)
    target = external_target()
    glow(src["body"], seed=1)
    if drift:
        bob(target, amp=0.08, speed=1.2, seed=2)
    return VGroup(src["group"], target)


def gentle(mob, amp=0.11, speed=1.45, seed=0):
    bob(mob, amp=amp, speed=speed, seed=seed)
    return mob


def glow(mob, color=BLUE, lo=0.17, hi=0.27, speed=1.15, seed=0):
    """Slow fill breathing for a large narrated host shape."""
    mob._glow_t = seed * 0.8

    def update(shape, dt):
        shape._glow_t += dt
        opacity = lo + (hi - lo) * (0.5 + 0.5 * np.sin(speed * shape._glow_t))
        shape.set_fill(color, opacity)
    return mob.add_updater(update)


def panel_src(center=(-3.25, -0.05, 0), tail=True):
    """Readable Src shorthand for a half-frame; labels stay at 24 pt."""
    c = np.array(center, dtype=float)
    sh3 = module("SH3", 1.25, 0.78, "angle").move_to(c + [-1.55, -0.72, 0])
    sh2 = module("SH2", 1.25, 0.78, "round").move_to(c + [-1.55, 0.55, 0])
    kin = RoundedRectangle(corner_radius=0.25, width=2.55, height=1.75,
                           stroke_color=BLUE, stroke_width=5, fill_color=BLUE,
                           fill_opacity=0.18).move_to(c + [0.65, -0.05, 0])
    kl = T("kinase", 26, BLUE, weight=BOLD).move_to(kin)
    body = RoundedRectangle(corner_radius=0.32, width=5.35, height=3.75,
                            stroke_width=0, fill_color=BLUE, fill_opacity=0.18).move_to(c + [0, 0.05, 0])
    body.set_z_index(-2)
    pieces = [body, sh3, sh2, kin, kl]
    tail_line = badge = None
    if tail:
        tail_line = flexible_line([(c[0] + 1.9, c[1] + 0.25), (c[0] + 2.25, c[1] + 1.1),
                                   (c[0] + 0.7, c[1] + 1.62), (c[0] - 0.72, c[1] + 1.22)], BLUE, 7)
        badge = phosphate(0.24).move_to(c + [-0.95, 1.22, 0])
        pieces += [tail_line, badge]
    return dict(group=VGroup(*pieces), sh2=sh2, sh3=sh3, kinase=VGroup(kin, kl),
                tail=tail_line, phosphate=badge, body=body)


def panel_detector(center=(3.25, -0.1, 0), receptor=True, lipid=True):
    """Readable detector shorthand for a half-frame; no scaled text."""
    c = np.array(center, dtype=float)
    mem = RoundedRectangle(corner_radius=0.1, width=5.45, height=0.48,
                           stroke_color=BLUE, stroke_width=4, fill_color=BLUE,
                           fill_opacity=0.16).move_to(c + [0, -1.58, 0])
    sh2 = module("SH2", 1.25, 0.78, "round").move_to(c + [-0.78, 0.65, 0])
    ph = module("PH", 1.25, 0.78, "angle").move_to(c + [0.78, 0.65, 0])
    link = flexible_line([(c[0] - 0.08, c[1] + 0.65), (c[0], c[1] + 0.82),
                          (c[0] + 0.08, c[1] + 0.65)], BLUE, 6)
    host = RoundedRectangle(corner_radius=0.3, width=3.65, height=1.35,
                            stroke_width=0, fill_color=BLUE, fill_opacity=0.22).move_to(c + [0, 0.65, 0])
    host.set_z_index(-2)
    detector = VGroup(host, sh2, link, ph)
    pieces = [mem, detector]
    rec = p = lip = None
    if receptor:
        rec = RoundedRectangle(corner_radius=0.15, width=0.52, height=2.55,
                               stroke_color=BLUE, stroke_width=5, fill_color=BLUE,
                               fill_opacity=0.18).move_to(c + [-2.15, -0.35, 0])
        p = phosphate(0.24).move_to(c + [-2.15, 0.62, 0])
        pieces += [rec, p]
    if lipid:
        lip = VGroup(Circle(radius=0.24, stroke_color=GREEN, stroke_width=4,
                            fill_color=GREEN, fill_opacity=0.55).move_to(c + [1.65, -1.28, 0]),
                     Line(c + [1.65, -1.48, 0], c + [1.65, -1.78, 0], color=GREEN, stroke_width=5))
        pieces.append(lip)
    return dict(group=VGroup(*pieces), detector=detector, sh2=sh2, ph=ph,
                receptor=rec, phosphate=p, lipid=lip, membrane=mem, host=host)


# ---------------------------------------------------------------------------
# Film

class S01Hook(SpokenScene):
    def construct(self):
        host = RoundedRectangle(corner_radius=0.28, width=8.5, height=1.3,
                                stroke_color=BLUE, stroke_width=5,
                                fill_color=BLUE, fill_opacity=0.14).move_to([0, -0.15, 0])
        one = module("reader", 1.6, 0.95).move_to(host)
        self.play(FadeIn(host), FadeIn(one, scale=0.8), run_time=0.8)
        glow(host, lo=0.12, hi=0.22, seed=1)
        self.add(scope_tag("schematic"))
        self.at("what changes")
        q = T("?", 68, GOLD, weight=BOLD).move_to([0, 2.35, 0])
        self.play(FadeIn(q, scale=0.5), run_time=0.55)
        self.at("one protein carries")
        sh3 = module("SH3", 1.55, 0.95, "angle").move_to([-1.65, -0.15, 0])
        sh2 = module("SH2", 1.55, 0.95, "round").move_to([1.65, -0.15, 0])
        self.play(ReplacementTransform(one, sh3), FadeIn(sh2, shift=RIGHT * 0.35),
                  FadeOut(q), run_time=1.15)
        self.at("influence one another")
        arcs = VGroup(ArcBetweenPoints(sh3.get_top(), sh2.get_top(), angle=-0.65,
                                      color=TEAL, stroke_width=5),
                      ArcBetweenPoints(sh2.get_bottom(), sh3.get_bottom(), angle=-0.65,
                                      color=TEAL, stroke_width=5))
        self.play(Create(arcs), run_time=0.8)
        pulse(arcs, base=5, amp=1.5, speed=2)
        gentle(VGroup(host, sh3, sh2), amp=0.035, speed=1.1)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Protein Modules: SH2, SH3, PTB, PDZ and PH"
    TITLE = "Two Grips, One Decision"


class S03SrcOpen(SpokenScene):
    def construct(self):
        title = T("cellular Src", 38, TEXT, weight=BOLD).move_to([0, 2.85, 0])
        self.play(FadeIn(title), run_time=0.45)
        src = open_src()
        self.play(FadeIn(src["body"]), run_time=0.4)
        glow(src["body"], seed=1)
        self.at("open strip")
        self.play(Create(src["tail"]), FadeIn(src["end"]), run_time=0.8)
        self.at("it carries")
        self.play(FadeIn(src["sh3"], shift=UP * 0.15), run_time=0.55)
        self.play(FadeIn(src["sh2"], shift=UP * 0.15), run_time=0.55)
        self.at("a kinase")
        self.play(FadeIn(src["kinase"]), run_time=0.65)
        self.at("short tail")
        tail_lab = T("tail", 28, BLUE).next_to(src["tail"], DOWN, buff=0.45)
        self.play(FadeIn(tail_lab), run_time=0.45)
        self.at("distinct job")
        self.play(Indicate(src["sh3"], color=TEAL), Indicate(src["sh2"], color=TEAL),
                  Indicate(src["kinase"], color=BLUE), run_time=1.2)
        self.at("flexible connections")
        self.play(Create(src["linker"]), src["tail"].animate.shift(UP * 0.08), run_time=0.8)
        gentle(src["tail"], amp=0.05, speed=1.15)
        self.add(scope_tag("schematic"))
        self.finish()


class S04TailGrip(SpokenScene):
    def construct(self):
        src = open_src()
        self.add(src["group"], scope_tag("schematic"))
        glow(src["body"], seed=2)
        csk = boxed_label("Csk", TEAL, 30).move_to([4.9, 2.3, 0])
        self.at("kinase called")
        self.play(FadeIn(csk, shift=DOWN * 0.2), run_time=0.55)
        self.at("places")
        p = phosphate().move_to(src["end"].get_center() + UP * 0.38)
        arrow = Arrow(csk.get_bottom(), p.get_top(), buff=0.12, color=TEAL,
                      stroke_width=5, tip_length=0.18)
        self.play(GrowArrow(arrow), FadeIn(p, scale=0.4), run_time=0.7)
        self.play(FadeOut(VGroup(csk, arrow)), run_time=0.35)
        self.at("tail bends back")
        folded = flexible_line([(1.9, 0.1), (3.0, 0.55), (2.8, 1.7),
                                (1.15, 2.15), (-0.7, 1.95), (-2.25, 0.78)], BLUE, 7)
        self.play(Transform(src["tail"], folded),
                  src["end"].animate.move_to([-2.25, 0.78, 0]),
                  p.animate.move_to([-2.25, 1.22, 0]), run_time=1.35)
        self.at("own")
        self.play(Indicate(src["sh2"], color=TEAL, scale_factor=1.12), run_time=0.55)
        self.at("bringing the tail")
        contact = Line([-2.08, 0.45, 0], [-2.25, 0.91, 0], color=TEAL, stroke_width=8)
        self.play(Create(contact), run_time=0.55)
        pulse(contact, base=8, amp=2, speed=2)
        self.at("uses the reader internally")
        lab = boxed_label("internal grip", TEAL, 28).move_to([-4.65, 2.2, 0])
        self.play(FadeIn(lab), run_time=0.45)
        self.finish()


class S05LinkerGrip(SpokenScene):
    def construct(self):
        src = compact_src(include_status=False)
        # Build the clamp one contact at a time.
        self.add(src["body"], src["kinase"], src["sh2"], src["tail"], src["phosphate"], src["c2"],
                 scope_tag("schematic"))
        glow(src["body"], seed=3)
        gentle(src["tail"], amp=0.09, speed=1.35)
        self.at("catches the linker")
        self.play(FadeIn(src["linker"]), FadeIn(src["sh3"], shift=RIGHT * 0.25), run_time=0.8)
        self.play(Create(src["c3"]), run_time=0.5)
        self.at("internal contacts settle")
        self.play(Indicate(src["c2"], color=TEAL), Indicate(src["c3"], color=TEAL), run_time=1.0)
        self.at("together they stabilize")
        status = boxed_label("inactive shape", BLUE, 30).move_to([4.65, -1.65, 0])
        self.play(Indicate(src["sh2"], color=TEAL), Indicate(src["sh3"], color=TEAL),
                  FadeIn(status), src["kinase"][0].animate.set_fill(BLUE, 0.07),
                  run_time=0.9)
        pulse(src["kinase"][0], base=5, amp=1.2, speed=1.8)
        self.at("neither module")
        note = T("binding modules", 30, TEAL).move_to([-4.4, -2.45, 0])
        self.play(FadeIn(note), Indicate(src["kinase"], color=BLUE), run_time=0.75)
        self.finish()


class S06Predict(SpokenScene):
    QUESTION = "Can the tail keep the same grip?"

    def construct(self):
        src = compact_src(include_status=False)
        self.add(src["group"], scope_tag("schematic"))
        glow(src["body"], seed=1)
        self.at("better external")
        target = external_target()
        self.play(FadeIn(target, shift=LEFT * 0.45), run_time=0.85)
        gentle(target, amp=0.13, speed=1.45, seed=2)
        self.at("predict what happens")
        q = question_card(self.QUESTION, y=-3.15, max_w=8.8)
        self.play(FadeIn(q.question), run_time=0.55)
        self.at("own tail")
        self.play(Indicate(src["phosphate"], color=GOLD, scale_factor=1.2), run_time=0.55)
        self.at("compare the two targets")
        self.play(Indicate(target[1], color=GOLD, scale_factor=1.2),
                  Indicate(src["phosphate"], color=GOLD, scale_factor=1.2), run_time=0.9)
        self.finish()


class S07Pause(PredictPause):
    QUESTION = "Can the tail keep the same grip?"
    SECONDS = 4.5
    CARD = {"y": -3.15, "max_w": 8.8}

    def backdrop(self):
        return prediction_world(drift=True)


class S08Reveal(SpokenScene):
    def construct(self):
        src = compact_src(include_status=False)
        target = external_target()
        self.add(src["group"], target, scope_tag("schematic"))
        glow(src["body"], seed=2)
        self.at("external target")
        self.play(target.animate.move_to([-0.05, 2.65, 0]), FadeOut(src["c2"]), run_time=1.0)
        self.at("pull it from the tail")
        free_tail = flexible_line([(2.45, 0.2), (3.15, 0.65), (3.9, 1.25),
                                   (4.55, 1.9), (5.15, 2.45)], BLUE, 7)
        self.play(Transform(src["tail"], free_tail),
                  VGroup(src["phosphate"]).animate.move_to([5.15, 2.85, 0]), run_time=1.05)
        self.at("losing one internal")
        self.play(src["sh2"].animate.shift(LEFT * 0.65 + UP * 0.25),
                  src["kinase"][0].animate.set_fill(BLUE, 0.22), run_time=0.85)
        loosened = boxed_label("clamp loosened", TEAL, 30).move_to([3.95, -1.65, 0])
        self.play(FadeIn(loosened), run_time=0.4)
        self.at("other inputs")
        motif = VGroup(*[Square(side_length=0.3, stroke_color=GREEN, stroke_width=3,
                                fill_color=GREEN, fill_opacity=0.65) for _ in range(3)])
        motif.arrange(RIGHT, buff=0.1).move_to([-4.7, -1.65, 0])
        self.play(FadeIn(motif, shift=RIGHT * 0.25), src["sh3"].animate.shift(UP * 0.22), run_time=0.75)
        self.at("opening makes")
        self.play(Indicate(src["kinase"], color=BLUE, scale_factor=1.05),
                  src["kinase"][0].animate.set_fill(BLUE, 0.34), run_time=0.85)
        pulse(src["kinase"][0], base=5, amp=1.2, speed=2)
        self.finish()


class S09Viral(SpokenScene):
    def construct(self):
        panels = TwoPanel("cellular Src", "viral Src", colors=(TEAL, BLUE), top=3.05, bottom=-2.35)
        self.add(panels, scope_tag("schematic"))
        panels.left_frame.set_fill(TEAL, 0.08)
        panels.right_frame.set_fill(BLUE, 0.08)
        cell = panel_src(center=(-3.25, -0.2, 0), tail=True)
        viral = panel_src(center=(3.25, -0.2, 0), tail=True)
        self.play(FadeIn(cell["group"]), FadeIn(viral["group"]), run_time=0.75)
        glow(cell["body"], seed=1)
        glow(viral["body"], seed=3)
        pulse(panels.left_frame, base=2.5, amp=1.0, speed=1.3)
        pulse(panels.right_frame, base=2.5, amp=1.0, speed=1.5)
        self.at("lost the tail")
        self.play(FadeOut(VGroup(viral["tail"], viral["phosphate"])), run_time=0.75)
        self.at("other mutations")
        ticks = VGroup(*[Line([-0.16, 0, 0], [0.16, 0, 0], color=GREY, stroke_width=4)
                         for _ in range(3)]).arrange(RIGHT, buff=0.38).move_to([3.25, 1.6, 0])
        self.play(Create(ticks), run_time=0.55)
        self.at("full internal clamp")
        self.play(Indicate(cell["sh2"], color=TEAL), Indicate(cell["sh3"], color=TEAL), run_time=0.8)
        self.at("always on")
        on = boxed_label("always on", BLUE, 30).move_to([3.25, -1.7, 0])
        self.play(FadeIn(on), viral["kinase"][0].animate.set_fill(BLUE, 0.38), run_time=0.75)
        pulse(viral["kinase"][0], base=5, amp=1.4, speed=2)
        self.at("removes an off switch")
        missing = T("tail target missing", 28, GREY).move_to([3.25, 2.2, 0])
        self.play(FadeIn(missing), run_time=0.45)
        self.finish()


class S10Detector(SpokenScene):
    def construct(self):
        title = T("conditional detector", 38, TEXT, weight=BOLD).move_to([0, 3.0, 0])
        self.at("same modular logic")
        self.play(FadeIn(title), run_time=0.5)
        world = detector_world()
        # Show the host first, then add its modules as named.
        self.play(FadeIn(world["membrane"]), FadeIn(world["host"]), run_time=0.7)
        glow(world["host"], seed=2)
        self.at("one protein")
        self.play(FadeIn(world["sh2"]), FadeIn(world["receptor"]), FadeIn(world["phosphate"]), run_time=0.8)
        gentle(world["receptor"], amp=0.13, speed=2.0, seed=1)
        gentle(world["phosphate"], amp=0.13, speed=2.0, seed=1)
        self.at("add a pH")
        self.play(FadeIn(world["ph"]), FadeIn(world["lipid"]), run_time=0.8)
        self.at("join them")
        self.play(Create(world["linker"]), run_time=0.55)
        gentle(world["detector"], amp=0.055, speed=1.2)
        self.add(scope_tag("schematic"))
        self.finish()


def one_grip_case(kind="receptor", center=ORIGIN):
    receptor = kind == "receptor"
    return panel_detector(center=center, receptor=receptor, lipid=not receptor)


class S11OneGrip(SpokenScene):
    def construct(self):
        panels = TwoPanel("receptor mark only", "lipid only", colors=(GOLD, GREEN), top=3.05, bottom=-2.4)
        self.add(panels, scope_tag("schematic"))
        left = one_grip_case("receptor", [-3.25, -0.05, 0])
        right = one_grip_case("lipid", [3.25, -0.05, 0])
        panels.left_frame.set_fill(GOLD, 0.07)
        panels.right_frame.set_fill(GREEN, 0.07)
        self.play(FadeIn(left["group"]), FadeIn(right["group"]), run_time=0.75)
        glow(left["host"], seed=1)
        glow(right["host"], seed=3)
        self.at("either contact alone")
        self.play(Indicate(left["detector"], color=TEAL),
                  Indicate(right["detector"], color=TEAL), run_time=0.8)
        pulse(panels.left_frame, base=2.5, amp=1.0, speed=1.3)
        pulse(panels.right_frame, base=2.5, amp=1.0, speed=1.5)
        self.at("only the receptor")
        start_l = left["detector"].get_center().copy()
        self.play(left["detector"].animate.shift(DOWN * 0.55), run_time=0.7)
        self.play(left["detector"].animate.move_to(start_l), run_time=0.65)
        self.at("only the lipid")
        start_r = right["detector"].get_center().copy()
        self.play(right["detector"].animate.shift(DOWN * 0.55), run_time=0.7)
        self.play(right["detector"].animate.move_to(start_r), run_time=0.65)
        self.at("brief encounter")
        weak_l = boxed_label("weak grip", GOLD, 27).move_to([-3.25, 1.85, 0])
        weak_r = boxed_label("weak grip", GREEN, 27).move_to([3.25, 1.85, 0])
        self.play(FadeIn(weak_l), FadeIn(weak_r), run_time=0.55)
        gentle(left["detector"], seed=1)
        gentle(right["detector"], seed=3)
        self.finish()


class S12Together(SpokenScene):
    def construct(self):
        world = detector_world(detector_at=(0, 1.3, 0))
        self.add(world["group"], scope_tag("schematic"))
        glow(world["host"], seed=2)
        gentle(world["receptor"], amp=0.13, speed=2.0, seed=1)
        gentle(world["phosphate"], amp=0.13, speed=2.0, seed=1)
        self.at("both domains bind")
        bound = world["detector"].copy().move_to([0, 0.0, 0])
        self.play(Transform(world["detector"], bound), run_time=0.85)
        c1 = Line(world["sh2"].get_left(), world["phosphate"].get_center() + RIGHT * 0.32,
                  color=TEAL, stroke_width=9)
        c1.add_updater(lambda line: line.put_start_and_end_on(
            world["sh2"].get_left(), world["phosphate"].get_center() + RIGHT * 0.32))
        c2 = Line(world["ph"].get_bottom(), world["lipid"][0].get_center(), color=TEAL, stroke_width=9)
        self.play(Create(c1), Create(c2), run_time=0.7)
        pulse(c1, base=9, amp=3, speed=1.7)
        pulse(c2, base=9, amp=3, speed=1.9)
        self.at("each contact helps")
        self.play(Indicate(c1, color=TEAL), Indicate(c2, color=TEAL), run_time=0.9)
        self.at("remains recruited")
        anchor = SurroundingRectangle(VGroup(c1, c2), color=TEAL, buff=0.62,
                                      corner_radius=0.25, stroke_width=4)
        self.play(Create(anchor), run_time=0.65)
        pulse(anchor, base=4, amp=1.2, speed=1.8)
        self.at("removing either")
        self.play(FadeOut(c1), world["detector"].animate.shift(UP * 0.35), run_time=0.65)
        self.play(FadeIn(c1), world["detector"].animate.shift(DOWN * 0.35), run_time=0.55)
        self.at("joint retention")
        brace = Brace(VGroup(c1, c2), RIGHT, color=TEAL)
        avid = T("avidity", 34, TEAL, weight=BOLD).next_to(brace, RIGHT, buff=0.28)
        self.play(FadeIn(brace), FadeIn(avid), run_time=0.6)
        self.at("two weak contacts together")
        self.play(c1.animate.set_stroke(width=13), c2.animate.set_stroke(width=13), run_time=0.85)
        self.finish()


class S13Rule(SpokenScene):
    def construct(self):
        rule = fit_text("Combining modules can make binding conditional on more than one signal.",
                        max_w=8.6, size=38, color=TEXT, max_lines=2).move_to([0, 3.05, 0])
        self.at("second rule")
        self.play(FadeIn(rule), run_time=0.65)
        panels = TwoPanel("two internal contacts", "two external contacts",
                          colors=(TEAL, GREEN), top=2.45, bottom=-2.5, size=29)
        self.at("combining modules")
        self.play(FadeIn(panels), run_time=0.55)
        panels.left_frame.set_fill(TEAL, 0.08)
        panels.right_frame.set_fill(GREEN, 0.08)
        src = panel_src(center=(-3.25, -0.2, 0), tail=True)
        det = panel_detector(center=(3.25, -0.35, 0), receptor=True, lipid=True)
        self.play(FadeIn(src["group"]), FadeIn(det["group"]), run_time=0.75)
        glow(src["body"], seed=1)
        glow(det["host"], seed=3)
        self.at("in SARC")
        lbrace = Brace(VGroup(src["sh2"], src["sh3"]), DOWN, color=TEAL)
        loff = T("holds off", 28, TEAL).next_to(lbrace, DOWN, buff=0.06)
        self.play(FadeIn(lbrace), FadeIn(loff), run_time=0.6)
        self.at("in the detector")
        rbrace = Brace(det["detector"], DOWN, color=GREEN)
        rplace = T("holds in place", 28, GREEN).next_to(rbrace, DOWN, buff=0.08)
        self.play(FadeIn(rbrace), FadeIn(rplace), run_time=0.6)
        self.add(scope_tag("schematic"))
        self.finish()


class S14End(EndCard):
    LINE = "Combining modules can make binding conditional on more than one signal."
