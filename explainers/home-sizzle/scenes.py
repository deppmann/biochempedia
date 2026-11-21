"""
COLOUR MAP ("What is here, in about a minute" — home-sizzle)
- TEAL (#3FB8C0): STEMhop brand address (stemhop.com), ladder "Simpler"/"Deeper" labels & rung highlight outline
- GOLD / MARK (#D4A843): highlight outline round named parts of captures, Hex inner bonds & feet, active ladder rung
- TEXT (#E8EAF0): body text (tagline, ladder titles & notes), capture borders

SCENES
- s01_name: STEMhop wordmark with hop arc and still Hex beside it; tagline fades in under wordmark.
- s02_here: Cross-fade to homepage lede (upper) with outline on age range, then homepage subjects (lower) with outline on Coming pill.
- s03_lesson: Three lesson captures in sequence (lesson_top with hook then film outline, lesson_sim with slider outline, lesson_question with explanation outline).
- s04_hop: Cross-fade to four-rung HopLadder for osmosis; Hex starts on High school, hops down to Grade 7 with outline, holds, then hops back up.
- s05_parents: Cross-fade to Parents section capture with outline on 30 activities line.
- s06_teachers: Cross-fade to match_private, then match_result with heading outline, then back to match_private with never sent outline.
- s07_honest: Cross-fade to about_review with human review outline, then report_button with button outline.
- s08_start: Cross-fade to plain STEMhop wordmark; stemhop.com fades in underneath in TEAL.
"""
from pathlib import Path
import json
import numpy as np

from bp_parts import *  # noqa: F401,F403
from bp_ladder import HopLadder

RNG = np.random.default_rng(7)

SHOTS = Path(__file__).resolve().parent / "shots"
META = json.loads((SHOTS / "shots.json").read_text())
MARK = "#D4A843"  # the outline round what the narrator is naming (gold reads on the light captures)


def screen(name, max_w=11.4, max_h=6.1, center=ORIGIN):
    """One capture as a still 'screen': the image, fitted, with a thin pale border. Returns a Group; .img is the image."""
    img = ImageMobject(str(SHOTS / f"{name}.png"))
    img.scale(min(max_w / img.width, max_h / img.height)).move_to(center)
    frame = Rectangle(width=img.width + 0.06, height=img.height + 0.06, stroke_color=TEXT, stroke_width=2).move_to(img)
    frame.layout_ok = True
    g = Group(img, frame)
    g.img = img
    return g


def mark(scr, name, key, pad=0.04):
    """The outline for mark `key` of capture `name`, placed on the screen `scr`: a VGroup with one rounded rectangle per rectangle in the mark's list."""
    rs = META[name]["marks"][key]
    img = scr.img
    outlines = VGroup()
    for x0, y0, rw, rh in rs:
        w, h = rw * img.width + 2 * pad, rh * img.height + 2 * pad
        cx = img.get_left()[0] + (x0 + rw / 2) * img.width
        cy = img.get_top()[1] - (y0 + rh / 2) * img.height
        r = RoundedRectangle(width=w, height=h, corner_radius=0.08, stroke_color=MARK, stroke_width=6).move_to([cx, cy, 0])
        r.layout_ok = True
        outlines.add(r)
    return outlines


def _build_s01():
    wm = ImageMobject(str(SHOTS / "wordmark.png"))
    wm.set_width(7.5).move_to([-0.55, 0.55, 0])
    hx = hex_mascot(1.5)
    baseline_y = wm.get_bottom()[1] + 0.164 * wm.height + 0.04
    hx.move_to([wm.get_right()[0] + 0.05, baseline_y, 0], aligned_edge=DL)
    tagline = T("STEM, one short lesson at a time.", size=34)
    tagline.move_to([0, wm.get_bottom()[1] - 0.35 - tagline.height / 2, 0])
    return wm, hx, tagline


def _build_s02_end():
    scr1 = screen("home_lede", max_h=2.6, center=[0, 1.9, 0])
    m1 = mark(scr1, "home_lede", "age")
    scr2 = screen("home_subjects", max_h=3.6, center=[0, -1.55, 0])
    m2 = mark(scr2, "home_subjects", "coming")
    return scr1, m1, scr2, m2


def _build_s03_end():
    scr = screen("lesson_question")
    m = mark(scr, "lesson_question", "why")
    return scr, m


def _build_s04_ladder():
    rungs = [
        dict(
            level="Grade 7",
            title="Diffusion and Osmosis",
            adds="Water drifts to the saltier side: weigh cucumber slices and see.",
        ),
        dict(
            level="High school",
            title="Crossing the Membrane",
            adds="In distilled water a red blood cell may burst; a plant cell's wall holds.",
        ),
        dict(
            level="College, a first course",
            title="Osmoregulation",
            adds="Count dissolved particles, then ask how a sea fish keeps its water.",
        ),
        dict(
            level="College, upper level",
            title="Body Fluid Compartments",
            adds="Where a litre of water goes in your body, and why saline differs.",
        ),
    ]
    return HopLadder(rungs, here=1, x=-5.1, text_w=10.2)


def _build_s05_end():
    scr = screen("parents")
    m = mark(scr, "parents", "thirty")
    return scr, m


def _build_s06_end():
    scr = screen("match_private")
    m = mark(scr, "match_private", "never_sent")
    return scr, m


def _build_s07_end():
    scr = screen("report_button")
    m = mark(scr, "report_button", "button")
    return scr, m


class S01Name(SpokenScene):
    def construct(self):
        wm, hx, tagline = _build_s01()
        self.play(FadeIn(wm), FadeIn(hx), run_time=0.5)
        self.at("one short lesson")
        self.play(FadeIn(tagline), run_time=0.4)
        self.finish()


class S02Here(SpokenScene):
    def construct(self):
        prev = Group(*_build_s01())
        self.add(prev)

        scr1 = screen("home_lede", max_h=2.6, center=[0, 1.9, 0])
        self.play(FadeOut(prev), FadeIn(scr1), run_time=0.4)

        self.at("from age")
        m1 = mark(scr1, "home_lede", "age")
        self.play(Create(m1), run_time=0.5)

        self.at("with more sciences")
        scr2 = screen("home_subjects", max_h=3.6, center=[0, -1.55, 0])
        self.play(FadeIn(scr2), run_time=0.4)
        m2 = mark(scr2, "home_subjects", "coming")
        self.play(Create(m2), run_time=0.5)
        self.finish()


class S03Lesson(SpokenScene):
    def construct(self):
        prev = Group(*_build_s02_end())
        self.add(prev)

        scr_top = screen("lesson_top")
        self.play(FadeOut(prev), FadeIn(scr_top), run_time=0.4)

        self.at("short reading")
        m_hook = mark(scr_top, "lesson_top", "hook")
        self.play(Create(m_hook), run_time=0.5)

        self.at("nearly")
        m_film = mark(scr_top, "lesson_top", "film")
        self.play(FadeOut(m_hook), Create(m_film), run_time=0.5)

        self.at("most have a simulation")
        scr_sim = screen("lesson_sim")
        self.play(FadeOut(scr_top), FadeOut(m_film), FadeIn(scr_sim), run_time=0.4)

        self.at("you can change")
        m_slider = mark(scr_sim, "lesson_sim", "slider")
        self.play(Create(m_slider), run_time=0.5)

        self.at("practice questions")
        scr_q = screen("lesson_question")
        self.play(FadeOut(scr_sim), FadeOut(m_slider), FadeIn(scr_q), run_time=0.4)

        self.at("explain their answers")
        m_why = mark(scr_q, "lesson_question", "why")
        self.play(Create(m_why), run_time=0.5)
        self.finish()


class S04Hop(SpokenScene):
    def construct(self):
        prev = Group(*_build_s03_end())
        self.add(prev)

        lad = _build_s04_ladder()
        self.play(FadeOut(prev), FadeIn(lad), run_time=0.5)

        self.at("hop down")
        lad.hop(self, 0, run_time=0.55)
        out0 = lad.outline(0)
        self.play(Create(out0), run_time=0.35)

        self.at("hop back up", lead=0.1)
        self.play(FadeOut(out0), run_time=0.2)
        lad.hop(self, 1, run_time=0.6)
        self.finish()


class S05Parents(SpokenScene):
    def construct(self):
        prev = _build_s04_ladder()
        self.add(prev)

        scr = screen("parents")
        self.play(FadeOut(prev), FadeIn(scr), run_time=0.4)

        self.at("start with")
        m_thirty = mark(scr, "parents", "thirty")
        self.play(Create(m_thirty), run_time=0.5)
        self.finish()


class S06Teachers(SpokenScene):
    def construct(self):
        prev = Group(*_build_s05_end())
        self.add(prev)

        scr_priv = screen("match_private")
        self.play(FadeOut(prev), FadeIn(scr_priv), run_time=0.4)

        self.at("see matching lessons", lead=0.35)
        scr_res = screen("match_result")
        self.play(FadeOut(scr_priv), FadeIn(scr_res), run_time=0.3)
        m_head = mark(scr_res, "match_result", "heading")
        self.play(Create(m_head), run_time=0.4)

        self.at("sending", lead=0.35)
        scr_priv2 = screen("match_private")
        self.play(FadeOut(scr_res), FadeOut(m_head), FadeIn(scr_priv2), run_time=0.3)
        m_never = mark(scr_priv2, "match_private", "never_sent")
        self.play(Create(m_never), run_time=0.4)
        self.finish()


class S07Honest(SpokenScene):
    def construct(self):
        prev = Group(*_build_s06_end())
        self.add(prev)

        scr_rev = screen("about_review")
        self.play(FadeOut(prev), FadeIn(scr_rev), run_time=0.4)

        self.at("a person has not")
        m_human = mark(scr_rev, "about_review", "human")
        self.play(Create(m_human), run_time=0.5)

        self.at("so each has")
        scr_btn = screen("report_button")
        self.play(FadeOut(scr_rev), FadeOut(m_human), FadeIn(scr_btn), run_time=0.4)

        self.at("a button")
        m_btn = mark(scr_btn, "report_button", "button")
        self.play(Create(m_btn), run_time=0.5)
        self.finish()


class S08Start(SpokenScene):
    def construct(self):
        prev = Group(*_build_s07_end())
        self.add(prev)

        wm = ImageMobject(str(SHOTS / "wordmark_plain.png"))
        wm.set_width(7.0).move_to([0, 0.5, 0])
        self.play(FadeOut(prev), FadeIn(wm), run_time=0.4)

        self.at("at stemhop")
        addr = T("stemhop.com", size=44, color=TEAL)
        addr.next_to(wm, DOWN, buff=0.35)
        self.play(FadeIn(addr), run_time=0.4)
        self.finish()


class S09End(EndCard):
    LINE = "Every lesson explains its idea at more than one level."
