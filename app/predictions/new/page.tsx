'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import {
  Globe,
  ArrowLeft,
  ShieldCheck,
  PlusCircle,
  Calendar,
  Send,
} from 'lucide-react';

export default function NewPrediction() {
  const router = useRouter();

  const [domain, setDomain] = useState(
    'AI & Technological Risk'
  );

  const [hypothesis, setHypothesis] = useState('');

  const [resolutionCriteria, setResolutionCriteria] =
    useState('');

  const [resolutionDate, setResolutionDate] =
    useState('');

  const [probability, setProbability] =
    useState(50);

  const [rationale, setRationale] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    alert(
      'Prediction successfully created and broadcasted to the GPR network!'
    );

    router.push('/');
  };

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
              <h1 className="text-lg font-bold">
                GPR
              </h1>

              <p className="text-xs text-slate-400">
                Global Prediction Repository
              </p>
            </div>
          </div>

          <Link
            href="/"
            className="flex items-center gap-2 text-sm font-medium text-slate-300 transition-colors hover:text-cyan-400"
          >
            <ArrowLeft className="h-4 w-4" />
            Back to Home
          </Link>
        </div>
      </header>

      {/* Main */}

      <main className="mx-auto max-w-3xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="mx-auto mb-10 max-w-xl text-center">
          <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-cyan-800/50 bg-cyan-950/60 px-3 py-1 text-xs font-semibold text-cyan-400">
            <PlusCircle className="h-3.5 w-3.5" />
            Decentralized Hypothesis Submission
          </div>

          <h1 className="mb-3 text-3xl font-extrabold tracking-tight text-white sm:text-4xl">
            Create New Prediction
          </h1>

          <p className="text-sm text-slate-400">
            Formulate a clear, measurable hypothesis with
            objective resolution criteria and contribute
            to the Global Prediction Repository.
          </p>
        </div>

        <form
          onSubmit={handleSubmit}
          className="space-y-6 rounded-2xl border border-slate-800 bg-slate-900/60 p-8 shadow-xl"
        >
          {/* Domain */}

          <div>
            <label className="mb-2 block text-sm font-medium text-slate-300">
              Prediction Domain
            </label>

            <select
              value={domain}
              onChange={(e) =>
                setDomain(e.target.value)
              }
              className="w-full rounded-xl border border-slate-800 bg-slate-950 px-4 py-3 text-sm text-slate-200 transition focus:border-cyan-500 focus:outline-none"
            >
              <option>
                AI & Technological Risk
              </option>

              <option>
                Climate & Environment
              </option>

              <option>
                Public Health & Pandemics
              </option>

              <option>
                Global Resource Management
              </option>

              <option>
                Geopolitical Stability
              </option>
            </select>
          </div>

          {/* Hypothesis */}

          <div>
            <label className="mb-2 block text-sm font-medium text-slate-300">
              Hypothesis Statement
            </label>

            <input
              required
              type="text"
              value={hypothesis}
              onChange={(e) =>
                setHypothesis(e.target.value)
              }
              placeholder="Example: Global average temperature will exceed..."
              className="w-full rounded-xl border border-slate-800 bg-slate-950 px-4 py-3 text-sm text-slate-200 placeholder-slate-600 transition focus:border-cyan-500 focus:outline-none"
            />
          </div>

          {/* Resolution Criteria */}

          <div>
            <label className="mb-2 flex items-center gap-2 text-sm font-medium text-slate-300">
              <ShieldCheck className="h-4 w-4 text-cyan-400" />
              Objective Resolution Criteria
            </label>

            <textarea
              required
              rows={4}
              value={resolutionCriteria}
              onChange={(e) =>
                setResolutionCriteria(
                  e.target.value
                )
              }
              placeholder="Describe exactly how the prediction will be resolved..."
              className="w-full rounded-xl border border-slate-800 bg-slate-950 p-4 text-sm text-slate-200 placeholder-slate-600 transition focus:border-cyan-500 focus:outline-none"
            />
          </div>

          {/* Resolution Date */}

          <div>
            <label className="mb-2 flex items-center gap-2 text-sm font-medium text-slate-300">
              <Calendar className="h-4 w-4 text-cyan-400" />
              Resolution Date
            </label>

            <input
              required
              type="date"
              value={resolutionDate}
              onChange={(e) =>
                setResolutionDate(
                  e.target.value
                )
              }
              className="w-full rounded-xl border border-slate-800 bg-slate-950 px-4 py-3 text-sm text-slate-200 transition focus:border-cyan-500 focus:outline-none"
            />
          </div>

          {/* Probability */}

          <div>
            <div className="mb-2 flex items-center justify-between">
              <label className="text-sm font-medium text-slate-300">
                Initial Probability Estimate
              </label>

              <span className="text-2xl font-extrabold text-cyan-400">
                {probability}%
              </span>
            </div>

            <input
              type="range"
              min={1}
              max={99}
              value={probability}
              onChange={(e) =>
                setProbability(
                  Number(e.target.value)
                )
              }
              className="w-full accent-cyan-400"
            />

            <div className="mt-2 flex justify-between text-[11px] text-slate-500">
              <span>1%</span>
              <span>50%</span>
              <span>99%</span>
            </div>
          </div>
          {/* Initial Rationale */}

          <div>
            <label className="mb-2 block text-sm font-medium text-slate-300">
              Initial Rationale / Thesis
            </label>

            <textarea
              rows={4}
              value={rationale}
              onChange={(e) => setRationale(e.target.value)}
              placeholder="Provide the evidence, assumptions, datasets, research papers, or logical reasoning supporting your initial probability estimate..."
              className="w-full rounded-xl border border-slate-800 bg-slate-950 p-4 text-sm text-slate-200 placeholder-slate-600 transition focus:border-cyan-500 focus:outline-none"
            />
          </div>

          {/* Information Box */}

          <div className="rounded-xl border border-cyan-900/40 bg-cyan-950/20 p-5">
            <h3 className="mb-2 font-semibold text-cyan-400">
              Submission Guidelines
            </h3>

            <ul className="space-y-2 text-sm text-slate-300">
              <li>
                • Write a prediction that can be objectively verified.
              </li>

              <li>
                • Define clear and measurable resolution criteria.
              </li>

              <li>
                • Select a fixed resolution date.
              </li>

              <li>
                • Provide an honest probability estimate between 1% and 99%.
              </li>

              <li>
                • Explain your reasoning with supporting evidence whenever
                possible.
              </li>
            </ul>
          </div>

          {/* Submit */}

          <button
            type="submit"
            className="flex w-full items-center justify-center gap-2 rounded-xl bg-cyan-500 py-3.5 font-semibold text-slate-950 shadow-lg shadow-cyan-500/20 transition hover:bg-cyan-400"
          >
            <Send className="h-4 w-4" />
            Broadcast Prediction
          </button>
        </form>
      </main>

      {/* Footer */}

      <footer className="mt-20 border-t border-slate-800 bg-slate-950 py-8 text-center text-xs text-slate-500">
        <div className="mx-auto max-w-5xl px-4">
          <p>
            Global Prediction Repository (GPR) • Open Source • Open Access
            Forecasting Engine for Humanity.
          </p>
        </div>
      </footer>
    </div>
  );
}