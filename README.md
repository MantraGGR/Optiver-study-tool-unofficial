# Optiver-study-tool-unofficial
This is the UNOFFIAL OPTIVER study tool which is made by claude to help me practice the simulations that may come up on the OA, I have not taken the OA yet and don't know what will be on it so yeah ,


# Optiver OA Trainer

Free, open-source practice for the [Optiver](https://optiver.com) online assessment. Five browser-based games covering probability, numerical reasoning, likelihood ranking, interval estimation, and orderbook arbitrage. No login, no tracking, no build step — just open `index.html`.

> **Disclaimer:** This is an unofficial study tool and is **not affiliated with or endorsed by Optiver.** The *Beat the Odds* probability format closely follows publicly available descriptions of the assessment. The reasoning games are reconstructions built to train the same underlying skills — the real assessment's UI, exact question counts, and timings vary by role and hiring cycle. Use this to build speed and intuition, not as a leaked replica.

## Games

| Game | What it trains | Format |
|------|----------------|--------|
| **Beat the Odds** | Probability & expected value under a clock | 15 × 90s, +1 / −1, pass at 7 |
| **Orderbooks** | Finding riskless arbitrage across bundled instruments | 10 × 75s |
| **NumberLogic** | Number sequences, grids, hidden operations | 12 × 45s |
| **Likelihood List** | Ranking outcomes by probability from charts/tables | 10 × 60s, +1 / −1 / skip 0 |
| **Intervals** | Estimation & calibration (bounding your uncertainty) | 12 × 25s |

### Beat the Odds
The most developed game: **141 questions** across 11 categories — Dice, Coins, Cards, Expected Value, Gambler's Ruin & Walks, Bayes, Streaks, Classics, Hard Mix (multi-concept), Recursion ("the game resets" family), and an Expert set. Includes:

- **Timed test** — real conditions: 15 questions, 90s each, 15-minute overall cap, +1/−1 scoring, no going back, category breakdown and worked solutions at the end.
- **Drill mode** — untimed, filter by category, instant feedback with explanations.
- **Cheat sheet** — the ~15 formulas and reflexes (1/p, coupon collector, gambler's ruin, order statistics, normal approximation, Bayes counting, symmetry) that cover most questions.

**Every answer is verified by Monte-Carlo simulation** — see `verify/`.

### The reasoning games
Orderbooks, NumberLogic, Likelihood, and Intervals are **procedurally generated**, so the question supply is effectively infinite and you can't overfit to a fixed bank. NumberLogic sequences include the reported hard types: fractions left unsimplified, interleaved series, second differences, and Fibonacci-style operations.

## Running it

No dependencies. Either:

```bash
# just open the file
open index.html          # macOS
xdg-open index.html      # Linux

# or serve it (nicer for hash deep-links)
python3 -m http.server 8000
# then visit http://localhost:8000
```

Or use the live version via GitHub Pages (see below).

## Deploying to GitHub Pages

1. Push this repo to GitHub.
2. Repo **Settings → Pages → Source → Deploy from branch → `main` / root**.
3. Your trainer is live at `https://<your-username>.github.io/<repo-name>/`.

## Contributing

PRs welcome. The most useful contributions:

- **More questions** for Beat the Odds — add to the `BANK` array in `beat-the-odds.html`. Please include a verification (exact fraction or a Monte-Carlo check) in your PR description.
- **New generator types** for the reasoning games.
- **Bug fixes** and accessibility improvements.

Ground rule: **no unverified answers.** If you add a probability question, prove the answer.

## Project structure

```
index.html            landing hub, links to all games
beat-the-odds.html    probability trainer (self-contained)
reasoning-games.html  Orderbooks / NumberLogic / Likelihood / Intervals
verify/verify.py      Monte-Carlo + exact checks for the question bank
LICENSE               MIT
```

## License

MIT — see [LICENSE](LICENSE). Free to use, modify, and share.

---

*Built as a study aid. Good luck on your assessment.*
