# GOAT Academy · Live Events Calendar

A calendar app for the GOAT Academy (The Money School) community that shows every
upcoming session from the **[Join Live Group Coaching](https://friends.goatacademy.org/spaces/16767656/events)**
space, colour-coded so members can see at a glance what kind of session it is.

**Status: mockup.** This first version renders a real snapshot of the space's
events so the design can be reviewed with true data. It is a single
self-contained page — no build step, no dependencies.

## What's here

| File | Purpose |
|---|---|
| `index.html` | The whole app: month view, agenda view, filters, event drawer. Open it in a browser. |
| `data/events.json` | The event snapshot the page embeds (also kept separately for development). |

## The mockup

- **Month view** — Monday-first grid for August & September 2026, with the
  current day ringed, past days muted, weekends washed, and `+N more` overflow
  per day.
- **Agenda view** — upcoming sessions grouped by day.
- **Event drawer** — click any session: full local time + duration, RSVP counts
  (going / maybe / can't), recurrence note, and a link to the event post in the
  community.
- **Colour coding** — six *session types* inferred from titles (Market
  Briefings, Trading Skills, WSP Workshops, Investing, Onboarding & Brokers,
  Success Path). The legend chips double as filters. This grouping is a
  **placeholder for the course levels**: `classify()` in `index.html` is the
  single swap point — replace it with a `post → level` mapping when the levels
  are defined.
- **Timezones** — event times are stored with their original UTC offsets and
  rendered in the viewer's local timezone (shown in the toolbar chip).
- Light and dark themes, keyboard-accessible, responsive down to phone widths.

## Where the data comes from

Fetched 19 Aug 2026 with the community's MCP server (`list_events`), scoped to
the space and windowed by date to stay under the API's 50-instances-per-call cap:

- space resource id: `16767656`
- space GlobalID (what `list_events` expects as `spaceId`):
  `Z2lkOi8vbWlnaHR5L0ZsZXhTcGFjZS8xNjc2NzY1Ng` (= `gid://mighty/FlexSpace/16767656`)
- coverage: 2 Aug – 7 Sep 2026 · 307 event instances across 74 recurring series

`data/events.json` stores one row per occurrence:
`[postResourceId, startsAt, durationMinutes, rsvpYes, rsvpMaybe, rsvpNo]`,
plus a `series` dictionary with each post's title and URL slug.

## Roadmap

1. **Level-based colours** — swap the session-type classifier for the real
   course levels (needs the level definitions / post mapping).
2. **Live data** — refresh the snapshot automatically (scheduled MCP fetch that
   commits a new `events.json`, or a small backend) so the calendar stays
   current without manual updates.
3. **Embed** — publish and embed the calendar in the community.
4. Nice-to-haves: week view, "add to my calendar" (ICS) per event, search.
