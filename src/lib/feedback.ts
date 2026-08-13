/**
 * The corrections / requests form.
 *
 * One Google Form serves both errors and feature requests. It is deliberately
 * anonymous: no email collection, no sign-in, and the email field is optional.
 * A student should be able to report a wrong bond without identifying
 * themselves.
 *
 * The "Which lesson?" field is prefilled from the page the reader is on, so a
 * report arrives already tagged and nobody has to remember which lesson they
 * were reading. Verified in a browser: the value lands in that field and no
 * other.
 *
 * NOTE: the share URL Google hands you carries `usp=sharing&ouid=…`. The ouid
 * is the form owner's Google account identifier — it is stripped here rather
 * than published on every page of a public site.
 */
const FORM_BASE =
  'https://docs.google.com/forms/d/e/1FAIpQLSe0MAoH7NWjTcKnp3fncbW1aNIzh4QsujDMkM4nm_n6mcfLig/viewform';

/** Entry id of the "Which lesson?" short-answer question. */
const ENTRY_LESSON = 'entry.532131771';

/**
 * Link to the feedback form, optionally prefilled with the lesson name.
 * Pass the lesson title; omit it for the general form (contact page, footer).
 */
export function feedbackUrl(lesson?: string): string {
  if (!lesson) return FORM_BASE;
  return `${FORM_BASE}?usp=pp_url&${ENTRY_LESSON}=${encodeURIComponent(lesson)}`;
}
