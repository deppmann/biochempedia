import type {Shell} from '../shell';
import type {Pathway, QuizItem} from '../../types';
import type {LaunchRequest}  from '../launch';
import {el} from "../dom.ts";
import '../../../styles/mcat.css';

interface ReviewQuestion extends QuizItem {
  pathwayName: string;
  lessonSlug?: string;
}

type Confidence = 'high' | 'medium' | 'low' | 'new';

interface ReviewAnswer {
  selected: number;
  confidence: Confidence;
}

export function launchMCAT(
  shell: Shell,
  allPathways: Pathway[],
  req?: LaunchRequest
): void {
  const title = 'MCAT Deep Review';

  const questionBank: ReviewQuestion[] = allPathways.flatMap(
    (pathway) =>
      pathway.quiz
        .filter((q) => q.mcat !== false)
        .map((q) => ({
          ...q,
          pathwayName: pathway.name,
          lessonSlug: pathway.lessonSlug,
        }))
  );

  let questions: ReviewQuestion[] = [];
  let answers: ReviewAnswer[] = [];
  let index = 0;

  const confidenceLevels = [
    {
      id: 'high',
      label: 'Know It',
      description: 'I can explain my answer.',
    },
    {
      id: 'medium',
      label: 'Pretty Sure',
      description: 'I think I know the answer.',
    },
    {
      id: 'low',
      label: 'Educated Guess',
      description: 'I narrowed down the choices.',
    },
    {
      id: 'new',
      label: 'No Idea',
      description: 'I am guessing or unfamiliar.',
    },
  ] as const;

  function setHeader(message: string): void {
    shell.setCrumb(title, () => shell.goHome());
    shell.setMascot(message);
  }

  function createIntro(): HTMLElement {
    return el(
      'div.arc-home',
      null,
      el('p.arc-eyebrow', null, 'Untimed Learning Mode'),
      el('h1.arc-title', null, title),
    );
  }

  function shuffle<T>(items: T[]): T[] {
    const copy = [...items];

    for (let i = copy.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [copy[i], copy[j]] = [copy[j], copy[i]];
    }

    return copy;
  }

  function renderSetup(): void {
    setHeader('Choose your question count and begin.');

    const wrap = createIntro();

    if (questionBank.length === 0) {
      wrap.append(
        el('p', null, 'No MCAT review questions are available.')
      );
      shell.setStage(wrap);
      return;
    }

    const setup = el('div.arc-mcat-setup');

    setup.append(
      el('h2', null, 'Build Your Review'),
      el(
        'p',
        null,
        `${questionBank.length} questions available.`
      ),
      el('label', { for: 'mcat-count' }, 'Number of questions')
    );

    const countInput = el('input.arc-mcat-count', {
      id: 'mcat-count',
      type: 'number',
      min: '1',
      max: String(questionBank.length),
      value: String(Math.min(10, questionBank.length)),
      step: '1',
    }) as HTMLInputElement;

    const error = el('p.arc-mcat-error');
    error.setAttribute('role', 'alert');

    const start = el(
      'button.arc-btn.is-primary',
      { type: 'button' },
      'Start Review →'
    ) as HTMLButtonElement;

    function begin(): void {
      const count = Number(countInput.value);

      if (
        !Number.isInteger(count) ||
        count < 1 ||
        count > questionBank.length
      ) {
        error.textContent =
          `Enter a number between 1 and ${questionBank.length}.`;
        countInput.focus();
        return;
      }

      questions = shuffle(questionBank).slice(0, count);
      answers = [];
      index = 0;

      renderQuestion();
    }

    start.addEventListener('click', begin);

    countInput.addEventListener('keydown', (event) => {
      if (event.key === 'Enter') begin();
    });

    setup.append(countInput, error, start);
    wrap.append(setup);

    shell.setStage(wrap);
  }

  function renderQuestion(): void {
    setHeader('Focus on your reasoning. Results come later.');

    const q = questions[index];
    const wrap = createIntro();

    wrap.append(
      el(
        'p.arc-blitz-count',
        null,
        `Question ${index + 1} of ${questions.length}`
      ),
      el('p.arc-blitz-stem', null, q.stem)
    );

    const options = el('div.arc-options.arc-blitz-opts');
    const buttons: HTMLButtonElement[] = [];

    const saved = answers[index];

    let selected = saved?.selected ?? -1;
    let confidence: Confidence | null =
      saved?.confidence ?? null;

    q.choices.forEach((choice, i) => {
      const button = el(
        'button.arc-opt.arc-opt-keyed',
        {
          type: 'button',
          'aria-pressed': String(selected === i),
        },
        el('span.arc-optnum', null, String(i + 1)),
        el('span.arc-opttext', null, choice)
      ) as HTMLButtonElement;

      button.classList.toggle('is-selected', selected === i);

      button.addEventListener('click', () => {
        selected = i;

        buttons.forEach((b, j) => {
          b.classList.toggle('is-selected', j === i);
          b.setAttribute('aria-pressed', String(j === i));
        });
      });

      buttons.push(button);
      options.append(button);
    });

    wrap.append(options);

    const confidenceSection = el('div.arc-confidence');

    confidenceSection.append(
      el('h2', null, 'How well do you know this?'),
      el(
        'p',
        null,
        'Choose the statement that best describes your confidence.'
      )
    );

    const confidenceButtons = el(
      'div.arc-confidence-options'
    );

    confidenceLevels.forEach(({ id, label, description }) => {
      const button = el(
        'button.arc-confidence-btn',
        {
          type: 'button',
          'aria-pressed': String(confidence === id),
        },
        el('strong', null, label),
        el('span.arc-confidence-desc', null, description)
      ) as HTMLButtonElement;

      button.classList.toggle(
        'is-selected',
        confidence === id
      );

      button.addEventListener('click', () => {
        confidence = id;

        confidenceButtons
          .querySelectorAll<HTMLButtonElement>(
            '.arc-confidence-btn'
          )
          .forEach((btn) => {
            const active = btn === button;
            btn.classList.toggle('is-selected', active);
            btn.setAttribute(
              'aria-pressed',
              String(active)
            );
          });
      });

      confidenceButtons.append(button);
    });

    confidenceSection.append(confidenceButtons);
    wrap.append(confidenceSection);

    const error = el('p.arc-mcat-error');
    error.setAttribute('role', 'alert');

    const navigation = el('div.arc-mcat-navigation');

    function saveAnswer(): boolean {
      if (selected === -1) {
        error.textContent = 'Select an answer to continue.';
        return false;
      }

      if (confidence === null) {
        error.textContent =
          'Select your confidence level to continue.';
        return false;
      }

      answers[index] = { selected, confidence };
      error.textContent = '';
      return true;
    }

    if (index > 0) {
      const previous = el(
        'button.arc-btn',
        { type: 'button' },
        '← Previous'
      ) as HTMLButtonElement;

      previous.addEventListener('click', () => {
        // Preserve answers when navigating backward.
        if (!saveAnswer()) return;
        index--;
        renderQuestion();
      });

      navigation.append(previous);
    }

    const isLast = index === questions.length - 1;

    const next = el(
      'button.arc-btn.is-primary',
      { type: 'button' },
      isLast ? 'Finish & See Results →' : 'Next Question →'
    ) as HTMLButtonElement;

    next.addEventListener('click', () => {
      if (!saveAnswer()) return;

      if (isLast) {
        renderResults();
      } else {
        index++;
        renderQuestion();
      }
    });

    navigation.append(next);
    wrap.append(error, navigation);

    shell.setStage(wrap);
  }

  function renderResults(): void {
    setHeader('Review your results and learn from each answer.');

    const wrap = createIntro();

    const correctCount = questions.reduce(
      (total, q, i) =>
        total + (answers[i]?.selected === q.answer ? 1 : 0),
      0
    );

    const percent = Math.round(
      (correctCount / questions.length) * 100
    );

    const score = el('div.arc-mcat-results.card');

    score.append(
      el('h2', null, 'Review Complete!'),
      el('p.arc-mcat-score', null, `${percent}%`),
      el(
        'p',
        null,
        `${correctCount} of ${questions.length} correct`
      )
    );

    wrap.append(score);

    const overview = el('div.arc-mcat-overview');

    overview.append(
      el('h2', null, 'Your Question Breakdown')
    );

    questions.forEach((q, i) => {
      const answer = answers[i];
      const correct = answer.selected === q.answer;

      const row = el(
        'button.arc-mcat-review-row',
        { type: 'button' },
        el(
          'span',
          null,
          `Question ${i + 1} — ${q.pathwayName}`
        ),
        el(
          'span',
          null,
          correct ? 'Correct ✓' : 'Incorrect ✗'
        )
      ) as HTMLButtonElement;

      row.classList.add(
        correct ? 'is-correct' : 'is-wrong'
      );

      row.addEventListener('click', () => {
        renderReview(i);
      });

      overview.append(row);
    });

    wrap.append(overview);

    const reviewAll = el(
      'button.arc-btn.is-primary',
      { type: 'button' },
      'Review All Questions →'
    ) as HTMLButtonElement;

    reviewAll.addEventListener('click', () => {
      renderReview(0);
    });

    const restart = el(
      'button.arc-btn',
      { type: 'button' },
      'Start New Review'
    ) as HTMLButtonElement;

    restart.addEventListener('click', renderSetup);

    wrap.append(reviewAll, restart);
    shell.setStage(wrap);
  }

  function renderReview(reviewIndex: number): void {
    setHeader('Understand why each answer is right or wrong.');

    const q = questions[reviewIndex];
    const answer = answers[reviewIndex];
    const correct = answer.selected === q.answer;

    const wrap = createIntro();

    wrap.append(
      el(
        'p.arc-blitz-count',
        null,
        `Review ${reviewIndex + 1} of ${questions.length}`
      ),
      el('p.arc-blitz-stem', null, q.stem)
    );

    const options = el('div.arc-options.arc-blitz-opts');

    q.choices.forEach((choice, i) => {
      const option = el(
        'div.arc-opt.arc-opt-keyed',
        null,
        el('span.arc-optnum', null, String(i + 1)),
        el('span.arc-opttext', null, choice)
      );

      if (i === q.answer) {
        option.classList.add('is-correct');
      } else if (i === answer.selected) {
        option.classList.add('is-wrong');
      }

      options.append(option);
    });

    wrap.append(options);

    const confidenceLabel = confidenceLevels.find(
      (level) => level.id === answer.confidence
    )?.label ?? 'Unknown';

    const feedback = el(
      `div.arc-teachbox.is-shown.card.${
        correct ? 'is-ok' : 'is-bad'
      }`
    );

    feedback.append(
      el('h2', null, correct ? 'Correct!' : 'Not quite!'),
      el(
        'p',
        null,
        `Your confidence: ${confidenceLabel}`
      ),
      el(
        'p.arc-teach-text',
        null,
        q.rationale
      )
    );

    if (q.lessonSlug) {
      const lessonLink = el(
        'a.arc-lesson-link',
        {
          href:
            `/lessons/${encodeURIComponent(q.lessonSlug)}/`,
          target: '_blank',
          rel: 'noopener noreferrer',
        },
        `Review ${q.pathwayName} →`
      );

      feedback.append(lessonLink);
    }

    wrap.append(feedback);

    const navigation = el('div.arc-mcat-navigation');

    if (reviewIndex > 0) {
      const previous = el(
        'button.arc-btn',
        { type: 'button' },
        '← Previous'
      ) as HTMLButtonElement;

      previous.addEventListener('click', () => {
        renderReview(reviewIndex - 1);
      });

      navigation.append(previous);
    }

    const next = el(
      'button.arc-btn.is-primary',
      { type: 'button' },
      reviewIndex < questions.length - 1
        ? 'Next Review →'
        : 'Back to Results →'
    ) as HTMLButtonElement;

    next.addEventListener('click', () => {
      if (reviewIndex < questions.length - 1) {
        renderReview(reviewIndex + 1);
      } else {
        renderResults();
      }
    });

    navigation.append(next);
    wrap.append(navigation);

    shell.setStage(wrap);
  }

  renderSetup();
}
