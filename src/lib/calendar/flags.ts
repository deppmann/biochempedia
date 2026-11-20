/* The calendar's one switch.

   EMAIL_OPT_IN is OFF. While it is off, no "Email me" button and no email dialog is put on any
   page, and no code path asks for an address. Nothing in the site sends calendar email yet: there
   is no sending code, no scheduler and no table. Turning this on is the LAST step, after the
   steps listed in docs/CALENDAR_EMAIL.md and after the site's owner has seen a test email. */
export const EMAIL_OPT_IN = false;
