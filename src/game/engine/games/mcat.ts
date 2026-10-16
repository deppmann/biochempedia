import type { Shell } from '../shell';
import type {Pathway, QuizItem} from '../../types';
import type { LaunchRequest } from '../launch';
import {el} from "../dom.ts";
import '../../../styles/mcat.css';

interface ReviewQuestion extends QuizItem {
  pathwayName: string;
}

export function launchMCAT( shell: Shell, allPathways: Pathway[], req?: LaunchRequest): void {
  const title = 'MCAT Deep Review';

  const questions: ReviewQuestion[] = allPathways.flatMap(
    (pathway) => pathway.quiz.filter((q) => q.mcat !== false)
        .map((q) => ({...q, pathwayName: pathway.name,}))
    ).slice(0, 5);

  let index = 0;

  function renderQuestion(): void {
    shell.setCrumb(title, () => shell.goHome());
    shell.setMascot('Take your time. Focus on the reasoning.');

    const wrap = el('div.arc-home.');
    const q = questions[index];

    if (!q) {
      wrap.append(
        el('h1.arc-title', null, title),
        el('p.arc-lede', null, 'Review complete!')
      );
      shell.setStage(wrap);
      return;
    }

    wrap.append(
      el('p.arc-eyebrow', null, 'Untimed Learning Mode'),
      el('h1.arc-title', null, title),
      el('p.arc-lede', null,
        'Understand why every answer is right or wrong.'
      ),
      el('p.arc-blitz-count', null,
        `Question ${index + 1} of ${questions.length}`
      ),
      el('p.arc-blitz-stem', null,
        `${q.stem}`
      )
    );

    const options = el('div.arc-options.arc-blitz-opts');
    let selected = -1;
    const buttons: HTMLButtonElement[] = [];

    q.choices.forEach((choice, i) => {
      const button = el(
        'button.arc-opt.arc-opt-keyed',
        { type: 'button' },
        el('span.arc-optnum', null, String(i + 1)),
        el('span.arc-opttext', null, choice)
      ) as HTMLButtonElement;

      button.addEventListener('click', () => {
        selected = i;

        buttons.forEach((b, j) => {
          b.classList.toggle('is-selected', j === i);
        });
      });

      buttons.push(button);
      options.append(button);
    });

    wrap.append(options);

    wrap.append(
      el('h2', null, 'Explain your reasoning'),
      el('p', null,
        'Why did you select this answer? ' +
        'Why might the other choices be incorrect?'
      )
    );

    const reasoning = el('textarea.arc-textarea', {
      rows: '5',
      placeholder: 'Write your reasoning here...',
      'aria-label': 'Your reasoning'
    }) as HTMLTextAreaElement;

    wrap.append(reasoning);

    let confidence: 'high' | 'medium' | 'low' | null = null;
    const confidenceSection = el('div.arc-confidence');

    confidenceSection.append(
      el('h2', null, 'How confident are you?'),
      el('p', null, 'How certain are you about your selected answer?')
    );

    const confidenceButtons = el('div.arc-confidence-options');

    const levels = [
      { id: 'high', label: 'High' },
      { id: 'medium', label: 'Medium' },
      { id: 'low', label: 'Low' }
    ] as const;

    levels.forEach(({ id, label }) => {
      const button = el(
        'button.arc-confidence-btn',
        { type: 'button' },
        label
      ) as HTMLButtonElement;

      button.addEventListener('click', () => {
        confidence = id;

        confidenceButtons
          .querySelectorAll('.arc-confidence-btn')
          .forEach((btn) => {
            btn.classList.toggle('is-selected', btn === button);
            btn.setAttribute('aria-pressed', String(btn === button));
          });
      });

      button.setAttribute('aria-pressed', 'false');
      confidenceButtons.append(button);
    });

    confidenceSection.append(confidenceButtons);
    wrap.append(confidenceSection);


    const feedback = el('div.arc-teachbox');

    const submit = el(
      'button.arc-btn.is-primary',
      { type: 'button' },
      'Submit & Review'
    ) as HTMLButtonElement;

    submit.addEventListener('click', () => {
      if (selected === -1) {reasoning.focus(); return;}

      const correct = selected === q.answer;

      buttons.forEach((b, i) => {
        b.disabled = true;
        if (i === q.answer) {
          b.classList.add('is-correct');
        } else if (i === selected) {
          b.classList.add('is-wrong');
        }
      });

      reasoning.disabled = true;
      submit.disabled = true;

      feedback.className = `arc-teachbox is-shown card ${correct ? 'is-ok' : 'is-bad'}`;

      feedback.append(
        el('h2', null, correct ? 'Correct!' : 'Not quite!'),
        el('p.arc-teach-text', null, q.rationale)
      );

      const next = el(
        'button.arc-btn.is-primary',
        { type: 'button' }, index + 1 < questions.length ? 'Next Question →' : 'Finish Review →'
      );

      next.addEventListener('click', () => { index++; renderQuestion();});
      feedback.append(next);
    });
    wrap.append(submit, feedback);
    shell.setStage(wrap);
  }

  renderQuestion();
}