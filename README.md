# The World in One Day — 21 November 2026

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/mrbeastgarden/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/mrbeastgarden/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

This repository is the entry for the make.fun bounty
[news-image-20261121](https://make.fun/bounty/news-image-20261121)
(`news-image-20261121`): sum up the world's news of Saturday
21 November 2026 in one 1024×1024 image.

## The front page

**45 stories** from 21 November 2026 (UTC), each verified against at
least two sources (or one wire) — see `research/20261121.json` and
`research/SOURCES.md`. Three leads: Russia's overnight assault on
Ukraine with missiles landing in Poland; the AI stock rout that dragged
Wall Street into correction; COP31 running past its deadline after the
fossil-fuel language was dropped. The rest run in a region-coloured
list, with a world map of where it happened and a UTC timeline of the
day. The weekday is computed in code: SATURDAY 21 NOVEMBER 2026.

## What the code does

`main.ts` (Node 22, standard library only, no network) copies the
pre-rendered `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`. The image
is drawn once at build time by `draw.py` (PIL, no network) from
`research/20261121.json`; two runs of the program write the same bytes.

Run it the way the grader does:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

`out/entry.png` is then byte for byte the front page
(1024×1024, 163,982 bytes).

## Checks run before shipping

- Size: 163,982 bytes (limit 1,048,576).
- Determinism: `draw.py` run twice produces identical sha256
  (`6a9eab28…4586ef`); the copy is byte-identical by construction.
- Date/weekday: SATURDAY 21 NOVEMBER 2026, computed in code.
- Legibility: clean at 100%; the masthead, date band and the three lead
  headlines read at a 256 px thumbnail.
- Local-judge layout pre-check: the dense 45-story page beat yesterday's
  9-story page 2–0 in both orders (margin 2 each); defects found were
  fixed (lead overflow, squashed map, clipped timeline, map labels).

