/* The help words on /start/ and /start/help/, in one place.

   Wording approved by the site's owner on 2026-11-22 in its calmer form: the line under the box
   names no harm, and the help page's headings name the help, not the harm. /start/ is linked from
   /ideas/, /courses/ and the nothing-found state of the site search; /start/help/ stays noindex.
   Change the words here and nowhere else.

   Why the page has them at all: children use the box, and a search box cannot tell when a
   sentence is a call for help. So the help does not depend on detecting one: `line` is on the page
   always, under the box. `urgent` is shown first, and no lessons, when the words are plainly about
   self-harm, abuse or danger (needsHelp() in syllabus-match.mjs), which is a small extra and will
   miss things. Rules for these words: written for a ten-year-old; never suggest the child did
   something wrong by typing; never name a parent as the only adult; say plainly which numbers are
   for the United States. */
export const HELP = {
  href: '/start/help/',
  /** Always on the page, quiet, under the box. */
  line: 'This is a search box, not a person. It can\'t talk with you. If you ever need help with something, ask an adult you trust.',
  linkText: 'Ways to get help',
  /** Shown first when the words are plainly about self-harm, abuse or danger. */
  urgent: {
    heading: 'This sounds hard, and it matters.',
    lines: [
      'Please tell an adult you trust today: a teacher, a school counselor or nurse, a coach, or someone in your family you feel safe with.',
      'If you are in danger right now, call 911 (in the United States).',
      'In the United States you can also call or text 988 at any time, day or night. It is free, and a person will answer and listen.',
      'This box only finds biology lessons, so it cannot help with this. Those people can.',
    ],
    status: 'This sounds hard, and it matters. Please tell an adult you trust today. In the United States you can call or text 988 at any time.',
  },
  /** The help page. */
  page: {
    title: 'Ways to get help',
    intro: 'STEMhop is a place to learn science. It cannot talk with you, and nobody here reads what you type. People can help, though, and you deserve that help.',
    steps: [
      ['Tell an adult you trust', 'A teacher, a school counselor or nurse, a coach, a grandparent, or someone else in your family you feel safe with. If the first person does not help, tell another one.'],
      ['If you need help right away', 'In the United States, call 911.'],
      ['If you feel very sad or worried', 'In the United States you can call or text 988 at any time, day or night. It is free. A person will answer and listen.'],
      ['If someone is not treating you well', 'It is not your fault. In the United States you can call 1-800-422-4453 at any time to talk with someone whose job is to help children.'],
      ['If you are not in the United States', 'Ask an adult you trust to help you find the number for children where you live.'],
    ],
    numbers: [['911', 'tel:911'], ['988', 'tel:988'], ['1-800-422-4453', 'tel:18004224453']],
    foot: 'Asking for help is a brave and good thing to do.',
  },
};

/** The text with its phone numbers made into links a phone can dial. `esc` escapes HTML. */
export function withNumbers(text, esc = (s) => s) {
  // "call or text 988": one link to call and one to text, so a phone can do either.
  const both = '<a href="tel:988">call</a> or <a href="sms:988">text</a> 988';
  let out = esc(text).split('call or text 988').join('\u0001');
  for (const [n, href] of HELP.page.numbers) out = out.split(n).join(`<a href="${href}">${n}</a>`);
  return out.split('\u0001').join(both);
}
