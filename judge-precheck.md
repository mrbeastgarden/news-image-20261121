# Local-judge layout pre-check — news-image-20261121

Date: 2026-11-21 ~08:45. Registered prompt (~/workspace/make-fun/local-judge/prompt.md),
adapted only for the day (21 Nov). Opponent: 20261120 S1 (9 stories, dev 12-0-0).
Layout pre-check only — never a placement predictor.

## Judgments

- Order 1 (A = 20261121, B = 20261120): WINNER: A, MARGIN: 2 — A covers far
  more of the day's news across regions with map and timeline, though B is
  cleaner to read.
- Order 2 (A = 20261120, B = 20261121): WINNER: B, MARGIN: 2 — same reason.
- Consistency: 2/2 agree (100%).

## Layout defects found and fixed

- Lead decks overflowed the lead boxes (v1) — fixed: shorter decks,
  lead_h 168 -> 178, headline 24 -> 23 pt, deck 14 -> 13 pt.
- Full-width map strip squashed continents beyond recognition (v1) — fixed:
  map moved to a left 480x150 block with proper aspect, timeline as a
  2-col list on the right.
- Timeline labels clipped at the edges (v1) — fixed by the 2-col list.
- Map labels LONDON/KYIV overlapped (v2), then GAZA/ANTALYA ran together
  (v3) — fixed: LONDON left of its dot, KYIV above, ANTALYA below KYIV.

## Remaining known nits (accepted)

- Lead 3 headline has an orphan "fuels" on line 3.
- List text is 14 pt — legible at 100%, not at thumbnail (leads read at
  256 px, verified with thumb256.png).
- Map is a rough hand-drawn outline, not a real map.

## Gates

- G1 size: entry.png 163,982 bytes (< 1,048,576).
- G2 determinism: two runs, identical sha256
  6a9eab2839685b2071e053918d7ccc7d3c32c7a180706cfad59b1109ee4586ef.
- G3 date/weekday: SATURDAY 21 NOVEMBER 2026, computed in code
  (datetime.date(2026,11,21).strftime('%A')).
- G4 legibility: 100% clean; 256 px thumbnail — masthead, band and the
  3 lead headlines read.
- G5: 45 stories, all with >= 2 sources or 1 wire, UTC evidence inside
  21 Nov UTC (research/20261121.json, validated by script).
- G6: every shipped file written in >= 2 messages (draw.py 4 passes,
  research JSON 3 passes, main.ts + README 2 passes each — see below).
