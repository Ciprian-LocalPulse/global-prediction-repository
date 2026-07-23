'use client';

import React from 'react';
import {
  Globe,
  ArrowLeft,
  BookOpen,
  Calculator,
  ShieldCheck,
  CheckCircle2,
} from 'lucide-react';

export default function Methodology() {
  return (
    <div className="min-h-screen bg-slate-950 text-white">
      {/* Header */}

      <header className="border-b border-slate-800 bg-slate-950/80 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-cyan-500/20">
              <Globe className="h-6 w-6 text-cyan-400" />
            </div>

            <div>
              <h1 className="text-lg font-bold">GPR</h1>
              <p className="text-xs text-slate-400">
                Global Prediction Repository
              </p>
            </div>
          </div>

          <a
            href="/"
            className="flex items-center gap-2 text-sm font-medium text-slate-300 transition-colors hover:text-cyan-400"
          >
            <ArrowLeft className="h-4 w-4" />
            Back to Home
          </a>
        </div>
      </header>

      {/* Main Content */}

      <main className="mx-auto max-w-4xl space-y-12 px-4 py-12 sm:px-6 lg:px-8">
        {/* Hero */}

        <div className="mx-auto max-w-2xl text-center">
          <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-cyan-800/50 bg-cyan-950/60 px-3 py-1 text-xs font-semibold text-cyan-400">
            <BookOpen className="h-3.5 w-3.5" />
            Scientific &amp; Mathematical Framework
          </div>

          <h1 className="mb-4 text-3xl font-extrabold tracking-tight text-white sm:text-5xl">
            Forecasting Methodology
          </h1>

          <p className="text-sm text-slate-400 sm:text-base">
            Learn how the Global Prediction Repository separates noise from
            genuine forecasting skill through mathematical accountability,
            objective resolution criteria, and reputation-weighted consensus.
          </p>
        </div>

        {/* Section 1 */}

        <section className="space-y-6 rounded-2xl border border-slate-800 bg-slate-900/60 p-8 shadow-xl">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl border border-cyan-800 bg-cyan-950 text-cyan-400">
              <Calculator className="h-5 w-5" />
            </div>

            <h2 className="text-xl font-bold text-white">
              1. The Brier Scoring Engine
            </h2>
          </div>

          <p className="text-sm leading-relaxed text-slate-300">
            To evaluate forecasting performance objectively, the Global
            Prediction Repository relies on the{' '}
            <strong>Brier Score</strong>, one of the most widely accepted
            scoring rules in forecasting research. Rather than rewarding bold
            guesses, it rewards calibration—assigning probabilities that match
            reality over time.
          </p>

          <p className="text-sm leading-relaxed text-slate-300">
            The score ranges from <strong>0</strong> (perfect prediction) to{' '}
            <strong>1</strong> (worst possible prediction). Lower scores always
            indicate better forecasting performance.
          </p>

          <div className="rounded-xl border border-slate-800 bg-slate-950/80 p-6 text-center">
            <p className="mb-2 font-mono text-xs uppercase text-slate-400">
              Mathematical Formulation
            </p>

            <div className="my-4 rounded-lg border border-cyan-900/40 bg-slate-900 p-4 font-mono text-lg text-cyan-400 sm:text-2xl">
              BS = (1 / N) × Σ(ft − ot)²
            </div>

            <p className="text-xs leading-relaxed text-slate-400">
              <strong>ft</strong> represents the forecast probability (0–1),
              while <strong>ot</strong> is the observed outcome (0 = false,
              1 = true). The average squared error across all resolved
              predictions becomes the forecaster's Brier Score.
            </p>
          </div>

          <div className="grid gap-4 md:grid-cols-3">
            <div className="rounded-xl border border-emerald-900/40 bg-emerald-950/20 p-5">
              <h3 className="mb-2 font-semibold text-emerald-400">
                Excellent
              </h3>

              <p className="text-sm text-slate-300">
                Brier Score below <strong>0.10</strong>. Exceptional calibration
                maintained over many resolved forecasts.
              </p>
            </div>

            <div className="rounded-xl border border-cyan-900/40 bg-cyan-950/20 p-5">
              <h3 className="mb-2 font-semibold text-cyan-400">
                Strong
              </h3>

              <p className="text-sm text-slate-300">
                Between <strong>0.10</strong> and <strong>0.20</strong>. High
                forecasting quality with consistently reliable probabilities.
              </p>
            </div>

            <div className="rounded-xl border border-amber-900/40 bg-amber-950/20 p-5">
              <h3 className="mb-2 font-semibold text-amber-400">
                Needs Improvement
              </h3>

              <p className="text-sm text-slate-300">
                Above <strong>0.20</strong>. Indicates overconfidence,
                underconfidence, or poor calibration.
              </p>
            </div>
          </div>
        </section>

        {/* Section 2 */}

        <section className="space-y-6 rounded-2xl border border-slate-800 bg-slate-900/60 p-8 shadow-xl">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl border border-emerald-800 bg-emerald-950 text-emerald-400">
              <ShieldCheck className="h-5 w-5" />
            </div>

            <h2 className="text-xl font-bold text-white">
              2. Wisdom of the Crowds & Reputation Weighting
            </h2>
          </div>

          <p className="text-sm leading-relaxed text-slate-300">
            Individual experts can make remarkable forecasts, but research has
            repeatedly shown that properly aggregated forecasts outperform most
            individuals. GPR combines crowd intelligence with historical
            forecasting performance to produce a calibrated consensus.
          </p>

          <ul className="space-y-4 text-sm text-slate-300">
            <li className="flex items-start gap-3">
              <CheckCircle2 className="mt-0.5 h-5 w-5 shrink-0 text-emerald-400" />

              <span>
                <strong>Reputation Weighting:</strong> Forecasters with lower
                historical Brier Scores receive greater influence in the
                aggregate probability.
              </span>
            </li>

            <li className="flex items-start gap-3">
              <CheckCircle2 className="mt-0.5 h-5 w-5 shrink-0 text-emerald-400" />

              <span>
                <strong>Continuous Learning:</strong> Reputation changes after
                every resolved prediction, rewarding consistent long-term
                accuracy instead of isolated successes.
              </span>
            </li>

            <li className="flex items-start gap-3">
              <CheckCircle2 className="mt-0.5 h-5 w-5 shrink-0 text-emerald-400" />

              <span>
                <strong>Anti-Manipulation:</strong> Identity verification,
                Sybil resistance, audit trails, and cryptographic integrity
                reduce coordinated manipulation attempts.
              </span>
            </li>
          </ul>
        </section>
                {/* Section 3 */}

        <section className="space-y-6 rounded-2xl border border-slate-800 bg-slate-900/60 p-8 shadow-xl">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl border border-cyan-800 bg-cyan-950 text-cyan-400">
              <Globe className="h-5 w-5" />
            </div>

            <h2 className="text-xl font-bold text-white">
              3. Resolution Criteria Verification
            </h2>
          </div>

          <p className="text-sm leading-relaxed text-slate-300">
            Every prediction published within the Global Prediction Repository
            must include clear, measurable, and objective resolution criteria.
            Forecasts cannot rely on subjective interpretation or ambiguous
            wording. Each hypothesis is accompanied by a fixed resolution date
            and publicly documented criteria before forecasting begins.
          </p>

          <p className="text-sm leading-relaxed text-slate-300">
            Once the resolution deadline is reached, the outcome is verified
            using trusted sources such as government publications, scientific
            journals, benchmark repositories, regulatory agencies, and other
            authoritative datasets. Every resolution is permanently recorded to
            ensure transparency and reproducibility.
          </p>

          <div className="grid gap-4 md:grid-cols-3">
            <div className="rounded-xl border border-slate-800 bg-slate-950/70 p-5">
              <h3 className="mb-2 font-semibold text-cyan-400">
                Objective
              </h3>

              <p className="text-sm text-slate-300">
                Resolution criteria must be binary and independently
                verifiable.
              </p>
            </div>

            <div className="rounded-xl border border-slate-800 bg-slate-950/70 p-5">
              <h3 className="mb-2 font-semibold text-cyan-400">
                Transparent
              </h3>

              <p className="text-sm text-slate-300">
                Every decision is documented together with supporting evidence
                and official references.
              </p>
            </div>

            <div className="rounded-xl border border-slate-800 bg-slate-950/70 p-5">
              <h3 className="mb-2 font-semibold text-cyan-400">
                Immutable
              </h3>

              <p className="text-sm text-slate-300">
                Resolved outcomes cannot be altered once verification has been
                completed.
              </p>
            </div>
          </div>
        </section>

        {/* Section 4 */}

        <section className="space-y-6 rounded-2xl border border-slate-800 bg-slate-900/60 p-8 shadow-xl">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl border border-emerald-800 bg-emerald-950 text-emerald-400">
              <BookOpen className="h-5 w-5" />
            </div>

            <h2 className="text-xl font-bold text-white">
              4. Open Science Principles
            </h2>
          </div>

          <p className="text-sm leading-relaxed text-slate-300">
            The Global Prediction Repository is designed around the principles
            of transparency, reproducibility, and scientific integrity.
            Forecasts, methodologies, aggregate probabilities, historical
            performance, and scoring algorithms remain publicly inspectable
            whenever possible.
          </p>

          <div className="space-y-4">
            <div className="flex items-start gap-3">
              <CheckCircle2 className="mt-1 h-5 w-5 shrink-0 text-emerald-400" />

              <div>
                <h3 className="font-semibold text-white">
                  Open Methodology
                </h3>

                <p className="text-sm text-slate-400">
                  Every scoring mechanism and aggregation method is documented
                  and available for independent review.
                </p>
              </div>
            </div>

            <div className="flex items-start gap-3">
              <CheckCircle2 className="mt-1 h-5 w-5 shrink-0 text-emerald-400" />

              <div>
                <h3 className="font-semibold text-white">
                  Reproducible Results
                </h3>

                <p className="text-sm text-slate-400">
                  Historical forecasts and outcomes remain accessible for
                  independent verification and research.
                </p>
              </div>
            </div>

            <div className="flex items-start gap-3">
              <CheckCircle2 className="mt-1 h-5 w-5 shrink-0 text-emerald-400" />

              <div>
                <h3 className="font-semibold text-white">
                  Community Driven
                </h3>

                <p className="text-sm text-slate-400">
                  Improvements to forecasting methodology can be proposed,
                  discussed, and audited by the wider research community.
                </p>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}

      <footer className="mt-20 border-t border-slate-800 bg-slate-950 py-8 text-center text-xs text-slate-500">
        <p>
          Global Prediction Repository (GPR) • Open Source Open-Access
          Forecasting Engine for Humanity.
        </p>
      </footer>
    </div>
  );
}