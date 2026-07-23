# Methodology

This document lays out the statistical reasoning behind the scoring and
aggregation choices in the GPR, and is aimed at anyone evaluating whether
the platform's numbers mean what they claim to mean.

## Why Brier scores, and not something else

There are several ways to grade a probabilistic forecast against a binary
outcome. The GPR uses the Brier score, introduced by Glenn W. Brier in
1950 for evaluating weather forecasts, for a few concrete reasons:

- **It's a proper scoring rule.** A forecaster who wants to minimize their
  expected Brier score has no incentive to report anything other than
  their true belief. Reporting 70% when you genuinely believe 70% is
  always at least as good, in expectation, as reporting 60% or 90%
  instead. This matters a lot for a public reputation system, where
  people would otherwise have an incentive to game their stated
  probabilities.
- **It's simple enough to explain in one sentence**: squared difference
  between your stated probability and the eventual outcome (1 or 0).
  Log-loss (the other common proper scoring rule) is also proper, but
  penalizes extreme wrong answers far more harshly — a 99% confident
  wrong call scores far worse under log-loss than under Brier. For a
  public platform where the goal is encouraging participation rather
  than punishing confident outliers into silence, Brier's gentler
  penalty curve is the better fit.
- **It has an established track record in exactly this domain.** Philip
  Tetlock's Good Judgment Project, probably the most well-known
  large-scale forecasting tournament, used Brier scores as its primary
  accuracy metric, which makes GPR scores at least loosely comparable to
  a body of published forecasting research.

## Reading a Brier score

Brier scores range from 0 (perfect) to 1 (perfectly wrong). Some
reference points that make raw numbers easier to interpret:

| Score | What it represents |
|-------|---------------------|
| 0.00  | Stated 100% and was right, or 0% and was right |
| 0.25  | What you get from guessing 50% every time, regardless of outcome |
| 0.50  | Roughly what an anti-correlated forecaster (confidently wrong more often than right) produces |
| 1.00  | Stated 100% and was wrong, or 0% and was wrong |

A score below 0.25 means a forecaster is, on average, doing better than a
coin flip — which sounds like a low bar, but on genuinely uncertain
questions (the kind the GPR is built around), beating 0.25 consistently
is a meaningful signal of skill, not a given.

## Why the reputation score is `(1 - mean Brier) * 100`

This transformation exists purely for readability. Brier scores are
"lower is better" and live on a 0–1 scale, which is an unusual convention
for anything displayed on a public leaderboard — most people expect
higher numbers to mean better performance. Inverting and rescaling to
0–100 makes the leaderboard intuitive without changing the underlying
math: a user with a mean Brier score of 0.15 gets a global accuracy score
of 85, and everyone sorts the way you'd expect.

New users start at exactly 50, matching what a mean Brier score of 0.50
would convert to. This is a deliberately neutral starting point — it
doesn't reward or punish someone for not having a track record yet — and
it's specifically not a claim that a brand-new user is "as good as a coin
flip," just that there isn't yet enough data to say anything else.

## Why the leaderboard has a minimum resolved-forecast threshold

A user who has made one forecast and happened to be right sits at the
best possible score (100) with a sample size of exactly one. Left
unfiltered, the leaderboard would spend its first weeks dominated by
people who got lucky once, which defeats the purpose of a track-record
based system. The `min_resolved` parameter (default 3) on the
`/leaderboard` endpoint exists to keep the default view meaningful; it's
configurable per-request for anyone who wants to look at newer
forecasters anyway.

Three is not a statistically rigorous cutoff — it's a pragmatic one for
an early-stage platform with limited resolved history. As the GPR
accumulates more resolved predictions, this threshold is a reasonable
first thing to revisit, ideally alongside a confidence-interval-based
approach (e.g., only ranking users whose score is statistically
distinguishable from 50 at some confidence level) rather than a flat
count.

## Why crowd consensus switches from simple to weighted averaging at n=3

See `docs/ARCHITECTURE.md` for the mechanical explanation. The
statistical reasoning underneath it: weighted averaging is only more
accurate than simple averaging once the weights themselves are
meaningfully informative, and a weight derived from someone's resolved
history means very little when that person has resolved zero or one
prior predictions (which describes most users on most predictions in a
young platform). Below three forecasts, a straight average is not just
simpler — it is very likely also the more accurate choice, since it
doesn't let one user's largely-uninformative weight dominate the result.

## Known limitations, stated plainly

- **Resolution criteria quality varies.** The consensus probability and
  the resulting Brier scores are only as good as the resolution criteria
  written at prediction-creation time. A vaguely worded criterion
  produces an Ambiguous resolution, which is the honest outcome, but it
  also means that prediction contributes nothing to anyone's track
  record. Better criteria-writing guidance for creators is a good
  candidate for a Phase 2 improvement.
- **No correction for question difficulty.** A user's global accuracy
  score currently treats every resolved prediction as equally
  informative, regardless of whether it was a near-certain outcome or a
  genuine toss-up. A more sophisticated version of the reputation engine
  might weight by the entropy of the eventual crowd consensus at
  resolution time, but that adds real complexity for a benefit that's
  hard to justify before there's enough resolved history to test it
  against.
- **Selection effects in who forecasts what.** Users self-select which
  predictions to forecast on, which means accuracy scores aren't
  necessarily comparable across users who specialize in different
  domains with different inherent difficulty. This is a known limitation
  of essentially every public forecasting platform, not something unique
  to the GPR, and it's worth being upfront about rather than implying the
  leaderboard is a clean apples-to-apples ranking.
