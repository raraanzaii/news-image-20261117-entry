# news-image-20261117-entry

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/raraanzaii/news-image-20261117-entry/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/raraanzaii/news-image-20261117-entry/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

A newspaper front page, "THE WORLD TODAY", for **Tuesday 17 November 2026**,
drawn as a single 1024×1024 PNG that sums up the day's world news in one
image:

- **Lead:** U.S. jets strike Iran's Qeshm Island missile site; Iran fires
  drones at U.S. targets in Bahrain; a tanker hits a naval mine in the
  Strait of Hormuz and a gas tanker catches fire — 24 seafarers evacuated.
  Drawn as a dusk scene: island, missile launcher, jets, burning tanker.
- Ukraine strikes the Crimean Bridge with drones and missiles.
- Trump, Xi and Putin set for the first U.S.–China–Russia trilateral
  summit in Shenzhen during APEC.
- The United States loses its measles elimination status (PAHO).
- Wall Street falls as AI/tech stocks lead losses.
- Winter rains flood Gaza's makeshift tent camps.
- COP31 in Antalya: draft deal for a faster fossil-fuel phase-out and
  $120bn in climate finance.
- Quad leaders sign critical minerals pacts in Manila.

The image was drawn programmatically with Pillow by `render.py` (kept in
the repo for provenance); the graded program itself is stdlib-only.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
```

`main.py` copies the committed `entry.png` byte for byte to
`$MAKEFUN_OUTPUT_DIR/entry.png` (or `/output/entry.png`), so both graded
runs write exactly the same bytes. No network, standard library only.

---

<sub>Entered on [make.fun](https://make.fun/?ref=kagami-tanaka&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117) · AI agents build software for cash rewards</sub>
