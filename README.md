# GOAT Academy · Live Events Calendar

A live calendar for the GOAT Academy (The Money School) community showing every
upcoming session from the
**[Join Live Group Coaching](https://friends.goatacademy.org/spaces/16767656/events)**
space — colour-coded by **course level** and filterable by **level, coach, and
session** — styled after the Trading Roadmap (2026 edition).

## Files

| File | Purpose |
|---|---|
| `index.template.html` | The app source (design + logic) with a `__GA_DATA__` placeholder. Edit THIS file, never `index.html`. |
| `data/events.json` | The event snapshot baked into the page (also the file the daily refresh rewrites). |
| `scripts/build.py` | `python3 scripts/build.py` → regenerates `index.html` + `build/fragment.html` from the template + data. |
| `index.html` | Generated. The full standalone page — open it in any browser. |
| `build/fragment.html` | Generated. The same page without the document shell, used to publish the claude.ai Artifact. |

## How the data stays current

Two layers, so the calendar is never stale:

1. **Live, in the page.** The published Artifact declares the `mcp` capability.
   When a viewer has the GOAT Academy connector on claude.ai, the page calls
   `list_events` with the viewer's own credentials (fourteen 3-day windows,
   ~6 weeks around today, re-polled every 15 min while open) and swaps the
   baked snapshot for live data. Viewers without the connector — or any
   failure — fall back to the snapshot, with a status chip + fix hint.
2. **Daily snapshot refresh.** A scheduled Claude task re-fetches the events
   via the GOAT Academy MCP each morning, rewrites `data/events.json`, runs
   `scripts/build.py`, pushes to `main`, and republishes the same Artifact
   URL. So even snapshot-only viewers are at most a day behind.

### MCP fetch notes (for the refresh task)

- `list_events` wants the space **GlobalID**, not the numeric id:
  `Z2lkOi8vbWlnaHR5L0ZsZXhTcGFjZS8xNjc2NzY1Ng` (= `gid://mighty/FlexSpace/16767656`).
- The API returns at most **50 instances per call** with no cursor — fetch in
  3-day `startAt`/`endAt` windows and split any window that returns exactly 50.
- Instance rows in `data/events.json`:
  `[postResourceId, startsAt (ISO, original offset), durationMinutes, rsvpYes, rsvpMaybe, rsvpNo]`,
  deduped by `(postResourceId, startsAt)`; titles HTML-entity-decoded;
  `meta.generatedAt` = fetch time (UTC).

## Levels & coaches

Both are derived in `index.template.html` (`LEVEL_RULES` / `COACH_RULES`) from
the **Live Events Rubric** and **Coaches Guide** in the Trading Roadmap PDF:

- **Beginner** (Foundations) · **Intermediate** (Building consistency) ·
  **Advanced** (Refining and depth) · **All levels** — colours match the
  rubric; All-levels uses the brand teal instead of the rubric's mint so it
  stays distinguishable from Beginner green on a dense grid (contrast/CVD
  validated in both themes).
- Sessions not named in the rubric (onboarding/SSM, broker help, candlesticks,
  "Preparing for the Week Ahead"…) use documented fallback rules — adjust in
  `LEVEL_RULES` if the Academy classes them differently.
- Coaches are read from rubric annotations and title mentions (Jesús, BK ·
  Byung Kim, Patrick, Brett, Dominic, Carlos, CSM Team); everything else is
  "Coaching team".

## Design

Branding follows the Trading Roadmap app: teal→blue gradient band, blue
wordmark + tile, "2026 Edition" pill, lime live/next pill, tabbed nav, and a
rubric-style colour-key card. Dark and light themes with a 3-state toggle
(follow system / dark / light). Fonts: Archivo (display), Inter (UI),
IBM Plex Mono (times). All event times render in the viewer's timezone.
