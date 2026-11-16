# Booking form exploration

## Playwright MCP (Brave)

Explored on 2026-11-16 with Playwright MCP driving Brave, opening `http://localhost:8000/booking_form.html`, filling the fields, clicking the submit button and reading `#result`.

| # | name | email | date | Selectors used | Message shown |
|---|---|---|---|---|---|
| 1 | S | sara@mail.com | 2026-11-17 (tomorrow) | `#name`, `#email`, `#date`, `#submit`, `#result` | Patient name must be at least 2 characters |
| 2 | Sara | sara@mail.com | 2026-11-17 (tomorrow) | `#name`, `#email`, `#date`, `#submit`, `#result` | Booking confirmed |
| 3 | (empty) | sara@mail.com | 2026-11-17 (tomorrow) | `#name`, `#submit`, `#result` | Patient name is required |
| 4 | Sara | sara.mail | 2026-11-17 (tomorrow) | `#name`, `#email`, `#submit`, `#result` | Enter a valid email |
| 5 | Sara | sara@mail.com | 2026-11-15 (yesterday) | `#email`, `#date`, `#submit`, `#result` | Appointment date cannot be in the past |
| 6 | Sara | sara@mail.com | (empty) | `#date`, `#submit`, `#result` | Appointment date is required |

Inputs 2 to 6 ran one after another on the same page, so the selectors column lists only the fields that were changed for that input; the other fields kept their values from the input before.

Playwright code that Playwright MCP ran for input 1:

```js
await page.goto('http://localhost:8000/booking_form.html');
await page.locator('#name').fill('S');
await page.locator('#email').fill('sara@mail.com');
await page.locator('#date').fill('2026-11-17');
await page.locator('#submit').click();
```

Each input was read back with:

```js
await page.evaluate('() => document.querySelector(\'#result\').textContent');
```

## Earlier check (Claude Code's built-in browser)

Explored on 2026-11-15 by opening `booking_form.html` (served at `http://localhost:8765/booking_form.html`) in a browser driven by an AI assistant (Claude Code's built-in browser, not Playwright MCP), filling the fields, clicking the submit button and reading the result.

Selectors used for every input: `#name`, `#email`, `#date` to fill, `#submit` to click, `#result` to read the message.

| # | name | email | date | Message shown |
|---|---|---|---|---|
| 1 | Sara | sara@mail.com | 2026-11-16 (tomorrow) | Booking confirmed |
| 2 | (empty) | sara@mail.com | 2026-11-16 (tomorrow) | Patient name is required |
| 3 | S | sara@mail.com | 2026-11-16 (tomorrow) | Patient name must be at least 2 characters |
| 4 | Sara | sara.mail | 2026-11-16 (tomorrow) | Enter a valid email |
| 5 | Sara | sara@mail.com | 2026-11-14 (yesterday) | Appointment date cannot be in the past |
| 6 | Sara | sara@mail.com | (empty) | Appointment date is required |
| 7 | Sara | (empty) | 2026-11-15 (today) | Email is required |
| 8 | Sara | sara@mail.com | 2026-11-15 (today) | Booking confirmed |

## What I learned

- The form checks name, then email, then date, and shows only the first error.
- Today's date is accepted; only dates before today are rejected.
- Only `Booking confirmed` means the booking is valid, so the workflow checks whether `#result` starts with that text.
