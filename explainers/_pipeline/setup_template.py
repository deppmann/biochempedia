"""Setup films for Biology Together (ages 5-10 activity guides): one shared template.

A setup film is the grown-up's quick start, 45-75 seconds: what to gather, how to set it up, what to
watch for, and the one safety point. Every film has the same six scenes, and all of its content lives
in script.json, so a film needs no scenes.py code of its own:

    (scenes.py of a setup film is the fixed stub SCENES_STUB below; render.py finds classes by reading it)

script.json scenes, in this order (ids fixed):
  s00_title    {"silent": 2.5}
  s00_idea     optional, same shape as s01_gather: the big idea (scenes.py then adds S00Idea(BigIdea))
  s01_gather   {"tts": ..., "items": [{"text": "on screen", "cue": "words spoken"}], "image": "img/x.png"?}
  s02_setup    {"tts": ..., "items": [...numbered steps...], "image": ...?}
  s03_watch    {"tts": ..., "items": [...], "image": ...?}
  s04_safety   {"tts": ..., "items": [...]}
  s05_end      {"silent": 3.0, "line": "the end-card line, 12 words or fewer"}
Top level: "lesson" (slug), "title" (film title), "pageTitle" (the activity's title).
Each item appears when the narrator says its cue (word-level sync, see SpokenScene.at); "image"
is a path relative to script.json (an approved figure from the activity page, converted to PNG).
"""
import json
import os
from pathlib import Path

from bp_style import *  # noqa: F401,F403

HEAD = {"s00_idea": ("The big idea", BLUE), "s01_gather": ("What you need", TEAL), "s02_setup": ("Set it up", GOLD),
        "s03_watch": ("What to watch for", GREEN), "s04_safety": ("Safety", RED)}


def _script():
    return json.loads(Path(os.environ["KX_SCRIPT"]).read_text())


def _scene(sid):
    return next(s for s in _script()["scenes"] if s["id"] == sid)


class SetupTitle(TitleCard):
    def construct(self):
        d = _script()
        self.LESSON = "Biology Together · " + d.get("pageTitle", "")
        self.TITLE = d["title"]
        super().construct()


class _Steps(SpokenScene):
    SID = ""

    def construct(self):
        sc = _scene(self.SID)
        label, color = HEAD[self.SID]
        head = T(label, size=48, font=TITLE_FONT, color=color).to_corner(UL, buff=0.6)
        rule = Line(LEFT, RIGHT, color=color, stroke_width=3).set_width(head.width).next_to(head, DOWN, buff=0.12, aligned_edge=LEFT)
        img = None
        if sc.get("image"):
            p = Path(os.environ["KX_SCRIPT"]).parent / sc["image"]
            if p.exists():
                img = ImageMobject(str(p))
                img.height = 5.6
                if img.width > 6.0:
                    img.width = 6.0
                img.to_edge(RIGHT, buff=0.55).shift(DOWN * 0.35)
        col_w = 6.6 if img is not None else 11.6
        rows = []
        numbered = self.SID == "s02_setup"
        for i, it in enumerate(sc["items"]):
            txt = T(it["text"], size=38)
            if txt.width > col_w - 0.8:
                txt = Paragraph(*_wrap(it["text"], col_w - 0.8, 38), font=FONT, font_size=38, color=TEXT, line_spacing=0.9)
            mark = (T(str(i + 1), size=32, color=BG, weight=BOLD) if numbered else Dot(radius=0.1, color=color))
            if numbered:
                disc = Circle(radius=0.3, color=color, fill_color=color, fill_opacity=1, stroke_width=0)
                mark = VGroup(disc, mark.move_to(disc))
            row = VGroup(mark, txt).arrange(RIGHT, buff=0.3, aligned_edge=UP if txt.height > 0.6 else ORIGIN)
            rows.append(row)
        col = VGroup(*rows).arrange(DOWN, buff=0.55, aligned_edge=LEFT)
        fit(col, max_w=col_w, max_h=5.6)
        col.next_to(rule, DOWN, buff=0.45, aligned_edge=LEFT)
        if col.get_bottom()[1] < -3.6:
            col.shift(UP * (-3.6 - col.get_bottom()[1]))
        self.play(FadeIn(head, shift=RIGHT * 0.15), Create(rule), run_time=0.5)
        if img is not None:
            frame = SurroundingRectangle(img, buff=0.05, color=GREY, stroke_width=1.5, corner_radius=0.08)
            self.play(FadeIn(img), Create(frame), run_time=0.6)
        for it, row in zip(sc["items"], rows):
            self.at(it["cue"])
            self.play(FadeIn(row, shift=RIGHT * 0.15), run_time=0.45)
        self.finish()


def _wrap(text, width_units, size=30):
    """Greedy wrap by measured width (Manim units)."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if T(trial, size=size).width > width_units and cur:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


class BigIdea(_Steps):
    """Optional scene after the title: the activity's big idea in a child's words (2026-11-01)."""
    SID = "s00_idea"


class Gather(_Steps):
    SID = "s01_gather"


class Setup(_Steps):
    SID = "s02_setup"


class Watch(_Steps):
    SID = "s03_watch"


class Safety(_Steps):
    SID = "s04_safety"


class SetupEnd(EndCard):
    def construct(self):
        self.LINE = _scene("s05_end").get("line", "The full guide is on this page.")
        super().construct()


SCENES_STUB = """from setup_template import *


class S00Title(SetupTitle):
    pass


class S01Gather(Gather):
    pass


class S02Setup(Setup):
    pass


class S03Watch(Watch):
    pass


class S04Safety(Safety):
    pass


class S05End(SetupEnd):
    pass
"""
