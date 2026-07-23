'use client';

import React, { useState } from 'react';
import {
  Globe,
  TrendingUp,
  ShieldCheck,
  ArrowUpRight,
  Search,
  PlusCircle,
} from 'lucide-react';

export default function Home() {
  const [searchQuery, setSearchQuery] = useState('');

  const predictions = [
    {
      id: '1',
      domain: 'AI & Technological Risk',
      hypothesis:
        'OpenAI or Google will release a verified AGI milestone model scoring >90% on ARC-AGI by end of 2028.',
      probability: 42,
      brierScorePending: true,
      status: 'Open',
      forecastersCount: 312,
      resolutionDate: '2028-12-31',
    },
    {
      id: '2',
      domain: 'Climate & Environment',
      hypothesis:
        'Global average surface temperature will exceed 1.5°C above pre-industrial levels for the entire calendar year 2027.',
      probability: 78,
      brierScorePending: true,
      status: 'Open',
      forecastersCount: 540,
      resolutionDate: '2027-12-31',
    },
    {
      id: '3',
      domain: 'Public Health & Pandemics',
      hypothesis:
        'An mRNA-based universal vaccine for influenza will receive FDA approval before Q3 2028.',
      probability: 65,
      brierScorePending: true,
      status: 'Open',
      forecastersCount: 189,
      resolutionDate: '2028-09-30',
    },
  ];

  const filteredPredictions = predictions.filter(
    (prediction) =>
      prediction.hypothesis
        .toLowerCase()
        .includes(searchQuery.toLowerCase()) ||
      prediction.domain
        .toLowerCase()
        .includes(searchQuery.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-950/80 backdrop-blur">
        <div className="max-w-7xl mx-auto flex items-center justify-between px-4 sm:px-6 lg:px-8 py-4">
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

          <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-slate-300">
            <a
              href="#"
              className="text-cyan-400 hover:text-cyan-300 transition-colors"
            >
              Predictions
            </a>

            <a href="#" className="hover:text-cyan-300 transition-colors">
              Leaderboard
            </a>

            <a href="#" className="hover:text-cyan-300 transition-colors">
              Methodology
            </a>

            <a href="#" className="hover:text-cyan-300 transition-colors">
              API Docs
            </a>
          </nav>

          <button className="flex items-center gap-2 rounded-lg bg-cyan-500 px-4 py-2 text-sm font-semibold text-slate-950 shadow-md shadow-cyan-500/20 transition hover:bg-cyan-400">
            <PlusCircle className="h-4 w-4" />
            New Prediction
          </button>
        </div>
      </header>

      {/* Hero */}
      <section className="relative overflow-hidden py-16 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto text-center">
        <div className="absolute inset-0 -z-10 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-cyan-900/20 via-slate-950/0 to-transparent" />

        <div className="inline-flex items-center gap-2 rounded-full border border-cyan-800/50 bg-cyan-950/60 px-3 py-1 text-xs font-semibold text-cyan-400">
          <ShieldCheck className="h-3.5 w-3.5" />
          Phase 1 MVP Active • Brier Scoring Engine Online
        </div>

        <h2 className="mx-auto mt-6 max-w-4xl text-4xl font-extrabold leading-tight tracking-tight sm:text-6xl">
          Anticipating Challenges. Mitigating Risks.
          <span className="bg-gradient-to-r from-cyan-400 to-emerald-400 bg-clip-text text-transparent">
            {' '}
            Building Tomorrow.
          </span>
        </h2>

        <p className="mx-auto mt-6 max-w-2xl text-lg text-slate-400 sm:text-xl">
          An open-access forecasting repository leveraging wisdom of the crowds
          and mathematical accountability to track critical global outcomes.
        </p>

        {/* Search */}
        <div className="relative mx-auto mt-10 max-w-xl">
          <Search className="absolute left-4 top-3.5 h-5 w-5 text-slate-500" />

          <input
            type="text"
            placeholder="Search by domain, keyword, or hypothesis..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full rounded-xl border border-slate-800 bg-slate-900/80 py-3 pl-12 pr-4 text-slate-200 placeholder-slate-500 shadow-inner transition focus:border-cyan-500 focus:outline-none"
          />
        </div>
      </section>

      {/* Predictions */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-20">
        <div className="mb-6 flex items-center justify-between">
          <h3 className="flex items-center gap-2 text-xl font-bold">
            <TrendingUp className="h-5 w-5 text-cyan-400" />
            Active Global Forecasts
          </h3>

          <span className="text-xs font-medium text-slate-400">
            Showing open verified hypotheses
          </span>
        </div>

        <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
          {filteredPredictions.map((prediction) => (
            <div
              key={prediction.id}
              className="group flex flex-col justify-between rounded-xl border border-slate-800 bg-slate-900/60 p-6 shadow-lg transition hover:border-cyan-500/50"
            >
              <div>
                <div className="mb-3 flex items-center justify-between">
                  <span className="rounded-md border border-cyan-900 bg-cyan-950/80 px-2.5 py-1 text-xs font-semibold text-cyan-400">
                    {prediction.domain}
                  </span>

                  <span className="text-xs text-slate-400">
                    Resolves: {prediction.resolutionDate}
                  </span>
                </div>

                <h4 className="line-clamp-3 text-base font-semibold transition group-hover:text-cyan-300">
                  {prediction.hypothesis}
                </h4>
              </div>

              <div className="mt-6 border-t border-slate-800/80 pt-4">
                <div className="mb-2 flex items-center justify-between">
                  <span className="text-xs font-medium text-slate-400">
                    Crowd Probability
                  </span>

                  <span className="text-2xl font-black text-emerald-400">
                    {prediction.probability}%
                  </span>
                </div>

                <div className="mb-4 h-2 w-full overflow-hidden rounded-full bg-slate-800">
                  <div
                    className="h-full rounded-full bg-gradient-to-r from-cyan-500 to-emerald-400 transition-all duration-500"
                    style={{
                      width: `${prediction.probability}%`,
                    }}
                  />
                </div>

                <div className="flex items-center justify-between text-xs text-slate-400">
                  <span>{prediction.forecastersCount} forecasters</span>

                  <button className="flex items-center gap-1 font-semibold text-cyan-400 hover:underline">
                    Forecast
                    <ArrowUpRight className="h-3.5 w-3.5" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800 bg-slate-950 py-8 text-center text-xs text-slate-500">
        <p>
          Global Prediction Repository (GPR) • Open Source Open-Access
          Forecasting Engine for Humanity.
        </p>
      </footer>
    </div>
  );
}