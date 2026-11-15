# Booking form exploration

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
