"""Demo of every component in bp_parts.py (silent). Render: see FILM_COMPONENTS notes; needs silent wavs."""
from bp_parts import *

R, K, N0 = 0.3, 1000, 50
logistic = lambda t: K / (1 + (K / N0 - 1) * np.exp(-R * t))


def growth_plot():
    """The carried-over picture: built by one function so s01, s05 and s06 match exactly."""
    P = Plot(box=(-5.9, 1.2, -1.3, 2.6), xr=(0, 30), yr=(0, 1200), xticks=[0, 10, 20, 30],
             yticks=[(0, "0"), (500, "500"), (1000, "1000")], xlabel="time (days)", ylabel="N (computed)")
    return P, P.hline(K, "K = 1,000", GOLD)


class S00Title(TitleCard):
    LESSON = "Pipeline"
    TITLE = "Scene Components Demo"


class S01Plot(NarratedScene):
    def construct(self):
        P, k = growth_plot()
        t = ValueTracker(0)
        live = P.live_curve(logistic, t, color=WHITE)
        dot = P.dot(lambda: t.get_value(), lambda: logistic(t.get_value()))
        ro = Readout([("day", lambda: t.get_value(), "{:5.1f}", TEXT),
                      ("N", lambda: logistic(t.get_value()), "{:5.0f}", WHITE),
                      ("growth", lambda: R * logistic(t.get_value()) * (1 - logistic(t.get_value()) / K), "{:+5.0f} /day", ORANGE)],
                     at=[4.2, 0.6, 0], widest=[30.0, 1000, -75], title="readout")
        self.play(Create(P), run_time=self.beat(0.15))
        self.play(FadeIn(k), FadeIn(ro), run_time=self.beat(0.1))
        self.add(live, dot, scope_tag("in this model"))
        self.play(t.animate.set_value(30), run_time=self.beat(0.6), rate_func=linear)
        self.finish()


class S02Panels(NarratedScene):
    def construct(self):
        tp = TwoPanel("small bag: 20 beads", "big bag: 200 beads", colors=(GOLD, BLUE))
        self.play(FadeIn(tp), run_time=self.beat(0.15))
        a = VGroup(*[Dot(radius=0.16, color=GOLD if i % 2 else BLUE) for i in range(20)]).arrange_in_grid(4, 5, buff=0.18)
        b = VGroup(*[Dot(radius=0.08, color=GOLD if i % 2 else BLUE) for i in range(200)]).arrange_in_grid(10, 20, buff=0.07)
        tp.put(a, "left"), tp.put(b, "right")
        a.scale(0.8), b.scale(0.8)
        self.play(FadeIn(a), FadeIn(b), run_time=self.beat(0.15))
        la = place_label(T("swings far", 28, GOLD), a, avoid=[tp.left_head], dirs=(DOWN, UP))
        lb = place_label(T("barely moves", 28, BLUE), b, avoid=[tp.right_head], dirs=(DOWN, UP))
        n = ValueTracker(0)
        c = counter("generation {:.0f}", n, at=[0, 3.5, 0], size=28, color=GREY)
        self.play(FadeIn(la), FadeIn(lb), run_time=self.beat(0.15))
        bob(a, amp=0.05), bob(b, amp=0.02, seed=2)
        self.add(c)
        self.play(n.animate.set_value(12), run_time=self.beat(0.4), rate_func=linear)
        self.finish()


class S03Ledger(NarratedScene):
    def construct(self):
        L = Ledger([("glucose", "nearly all taken back", GREEN), ("sodium", "most taken back", ORANGE),
                    ("water", "about 99% taken back", BLUE)], top_left=(-5.8, 2.3), title="what the kidney keeps")
        self.play(FadeIn(L), run_time=self.beat(0.1))
        for i in range(3):
            self.play(L.reveal(i), run_time=self.beat(0.08))
        self.play(L.change(1, "a small share excreted"), run_time=self.beat(0.1))
        self.play(L.mark(2), run_time=self.beat(0.08))
        cap = caption("The take-back, not the filter, sets how much urine leaves.")
        self.play(FadeIn(cap), run_time=self.beat(0.1))
        old = T("filter: 180 L a day", 30, GREY).move_to([3.0, -0.9, 0])
        new = T("urine: about 1.5 L a day", 30, YELLOW).move_to([3.0, -0.9, 0])
        self.play(FadeIn(old), run_time=self.beat(0.08))
        self.play(swap(old, new), run_time=self.beat(0.12))
        self.finish()


class S04Dial(NarratedScene):
    def construct(self):
        f = ValueTracker(0.1)
        d = dial(f, center=[0, 0.4, 0], radius=1.8, label="take-back")
        kept = ValueTracker(18)
        c = counter("{:.0f} of 180 L kept", kept, at=[0, 3.1, 0], size=30)
        self.play(FadeIn(d), FadeIn(c), run_time=self.beat(0.15))
        self.play(f.animate.set_value(0.99), kept.animate.set_value(178), run_time=self.beat(0.55))
        self.add(scope_tag("schematic"))
        self.finish()


class S05Predict(NarratedScene):
    def construct(self):
        P, k = growth_plot()
        self.add(P, k, P.curve(logistic, color=WHITE))
        q = question_card("Where is it adding the most per day?", ["when N is small", "halfway to K", "right at K"],
                          chips_at=[3.6, 0.6, 0])
        self.play(FadeIn(q.chips), run_time=self.beat(0.2))
        self.play(FadeIn(q.question), run_time=self.beat(0.2))
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "Where is it adding the most per day?"
    OPTIONS = ["when N is small", "halfway to K", "right at K"]
    CHIPS_AT = [3.6, 0.6, 0]

    def backdrop(self):
        P, k = growth_plot()
        return VGroup(P, k, P.curve(logistic, color=WHITE))


class S07End(EndCard):
    LINE = "Build from parts; draw only the lesson's own picture."
