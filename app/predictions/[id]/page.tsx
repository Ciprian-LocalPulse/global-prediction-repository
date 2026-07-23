'use client';

import React, { useState } from 'react';
import {
  Globe,
  ArrowLeft,
  ShieldCheck,
  Calendar,
  Send,
  CheckCircle2,
  User,
  MessageSquare,
} from 'lucide-react';

export default function PredictionDetail() {
  const [userProbability, setUserProbability] = useState(45);
  const [rationale, setRationale] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const [comments, setComments] = useState([
    {
      id: 1,
      author: 'Dr. Elena Vance',
      score: '82.4 Brier',
      text: 'Based on current hardware scaling trends and benchmark saturation curves, 2028 is a very realistic timeline for ARC-AGI >90%.',
      time: '2 hours ago',
    },
    {
      id: 2,
      author: 'Marcus Aurelius',
      score: '79.1 Brier',
      text: 'Hardware is advancing fast, but algorithmic breakthroughs in reasoning architectures are hitting diminishing returns. I am leaning lower (30%).',
      time: '5 hours ago',
    },
  ]);

  const prediction = {
    id: '1',
    domain: 'AI & Technological Risk',
    hypothesis:
      'OpenAI or Google will release a verified AGI milestone model scoring >90% on ARC-AGI by end of 2028.',
    resolutionCriteria:
      'The model must be officially released for public or API evaluation and achieve an independently verified score strictly greater than 90.0% on the public evaluation split of ARC-AGI, confirmed by at least two independent AI safety research institutions before December 31, 2028.',
    resolutionDate: '2028-12-31',
    crowdProbability: 42,
    forecastersCount: 312,
    creator: 'AI Futures Initiative',
    status: 'Open',
  };

  const handleSubmitForecast = (e: React.FormEvent) => {
    e.preventDefault();

    setSubmitted(true);

    if (rationale.trim()) {
      setComments([
        {
          id: Date.now(),
          author: 'You (Forecaster)',
          score: 'New',
          text: rationale,
          time: 'Just now',
        },
        ...comments,
      ]);

      setRationale('');
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      {/* Header */}

      <header className="border-b border-slate-800 bg-slate-950/80 backdrop-blur">
        <div className="max-w-7xl mx-auto flex items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-cyan-500/20">
              <Globe className="h-6 w-6 text-cyan-400" />
            </div>

            <div>
              <h1 className="font-bold text-lg">GPR</h1>
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
            Back to Predictions
          </a>
        </div>
      </header>

      {/* Main */}

      <main className="max-w-5xl mx-auto px-4 py-10 sm:px-6 lg:px-8">
        <div className="mb-6 flex items-center justify-between">
          <span className="rounded-md border border-cyan-900 bg-cyan-950/80 px-3 py-1 text-xs font-semibold text-cyan-400">
            {prediction.domain}
          </span>

          <span className="flex items-center gap-1 text-xs text-slate-400">
            <Calendar className="h-3.5 w-3.5" />
            Resolves: {prediction.resolutionDate}
          </span>
        </div>

        <h1 className="mb-6 text-2xl font-extrabold leading-tight text-white sm:text-4xl">
          {prediction.hypothesis}
        </h1>

        {/* Stats */}

        <div className="mb-10 grid grid-cols-1 gap-6 md:grid-cols-3">
          <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-6 shadow-lg">
            <span className="text-xs font-medium uppercase tracking-wider text-slate-400">
              Crowd Consensus
            </span>

            <div className="my-4 flex items-baseline gap-3">
              <span className="text-4xl font-black text-emerald-400">
                {prediction.crowdProbability}%
              </span>

              <span className="text-xs text-slate-400">
                Probability of "Yes"
              </span>
            </div>

            <div className="h-2 w-full overflow-hidden rounded-full bg-slate-800">
              <div
                className="h-full rounded-full bg-gradient-to-r from-cyan-500 to-emerald-400"
                style={{
                  width: `${prediction.crowdProbability}%`,
                }}
              />
            </div>
          </div>

          <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-6 shadow-lg">
            <span className="text-xs font-medium uppercase tracking-wider text-slate-400">
              Active Forecasters
            </span>

            <div className="my-4 flex items-baseline gap-2">
              <span className="text-4xl font-black text-cyan-400">
                {prediction.forecastersCount}
              </span>

              <span className="text-xs text-slate-400">
                experts & researchers
              </span>
            </div>

            <span className="text-xs text-slate-400">
              Weighted by historical Brier accuracy
            </span>
          </div>

          <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-6 shadow-lg">
            <span className="text-xs font-medium uppercase tracking-wider text-slate-400">
              Status & Creator
            </span>

            <div className="my-4 flex items-center gap-2">
              <span className="rounded-full border border-emerald-800 bg-emerald-950 px-2.5 py-1 text-xs font-semibold text-emerald-400">
                {prediction.status}
              </span>

              <span className="text-xs text-slate-300">
                By {prediction.creator}
              </span>
            </div>

            <span className="text-xs text-slate-400">
              Strict cryptographic verification enabled
            </span>
          </div>
        </div>

        {/* Resolution */}

        <div className="mb-10 rounded-xl border border-cyan-950 bg-slate-900/40 p-6 shadow-inner">
          <h2 className="mb-2 flex items-center gap-2 text-sm font-bold uppercase tracking-wider text-cyan-400">
            <ShieldCheck className="h-4 w-4" />
            Objective Resolution Criteria
          </h2>

          <p className="text-sm leading-relaxed text-slate-300">
            {prediction.resolutionCriteria}
          </p>
        </div>

        {/* Forecast Form */}

        <div className="mb-12 rounded-2xl border border-slate-800 bg-gradient-to-br from-slate-900 to-slate-950 p-8 shadow-xl">
          <h2 className="mb-2 text-xl font-bold">
            Submit Your Forecast
          </h2>

          <p className="mb-6 text-xs text-slate-400">
            Adjust the probability slider and explain your reasoning.
          </p>

          <form
            onSubmit={handleSubmitForecast}
            className="space-y-6"
          >
            <div>
              <div className="mb-2 flex items-center justify-between">
                <label className="text-sm text-slate-300">
                  Your Probability Estimate
                </label>

                <span className="text-2xl font-black text-cyan-400">
                  {userProbability}%
                </span>
              </div>

              <input
                type="range"
                min={1}
                max={99}
                value={userProbability}
                onChange={(e) =>
                  setUserProbability(Number(e.target.value))
                }
                className="w-full accent-cyan-400"
              />
            </div>

            <textarea
              rows={5}
              value={rationale}
              onChange={(e) => setRationale(e.target.value)}
              placeholder="Explain your reasoning..."
              className="w-full rounded-xl border border-slate-800 bg-slate-900 p-4 text-sm text-slate-200 placeholder-slate-500 focus:border-cyan-500 focus:outline-none"
            />

            <div className="flex items-center justify-between">
              {submitted && (
                <div className="flex items-center gap-2 text-sm font-semibold text-emerald-400">
                  <CheckCircle2 className="h-5 w-5" />
                  Forecast submitted successfully.
                </div>
              )}

              <button
                type="submit"
                className="ml-auto flex items-center gap-2 rounded-xl bg-cyan-500 px-6 py-3 font-semibold text-slate-950 transition hover:bg-cyan-400"
              >
                <Send className="h-4 w-4" />
                Submit Forecast
              </button>
            </div>
          </form>
        </div>

        {/* Discussion */}

        <div>
          <div className="mb-6 flex items-center justify-between">
            <h2 className="flex items-center gap-2 text-lg font-bold">
              <MessageSquare className="h-5 w-5 text-cyan-400" />
              Discussion ({comments.length})
            </h2>

            <span className="text-xs text-slate-400">
              Sorted by reputation
            </span>
          </div>

          <div className="space-y-4">
            {comments.map((comment) => (
              <div
                key={comment.id}
                className="rounded-xl border border-slate-800 bg-slate-900/60 p-6"
              >
                <div className="mb-3 flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="flex h-8 w-8 items-center justify-center rounded-full bg-slate-800">
                      <User className="h-4 w-4 text-cyan-400" />
                    </div>

                    <div>
                      <p className="text-sm font-semibold">
                        {comment.author}
                      </p>

                      <p className="text-xs text-slate-500">
                        Score: {comment.score}
                      </p>
                    </div>
                  </div>

                  <span className="text-xs text-slate-500">
                    {comment.time}
                  </span>
                </div>

                <p className="text-sm leading-relaxed text-slate-300">
                  {comment.text}
                </p>
              </div>
            ))}
          </div>
        </div>
      </main>

      {/* Footer */}

      <footer className="mt-20 border-t border-slate-800 bg-slate-950 py-8 text-center text-xs text-slate-500">
        Global Prediction Repository (GPR) • Open Source Open-Access Forecasting
        Engine for Humanity.
      </footer>
    </div>
  );
}