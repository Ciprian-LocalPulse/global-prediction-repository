'use client';

import React, { useState } from 'react';
import {
  Globe,
  ArrowLeft,
  Trophy,
  Search,
  User,
} from 'lucide-react';

export default function Leaderboard() {
  const [searchQuery, setSearchQuery] = useState('');

  const forecasters = [
    {
      rank: 1,
      name: 'Dr. Elena Vance',
      brierScore: 0.112,
      resolvedCount: 34,
      accuracy: '91.2%',
      role: 'Oracle / Lead AI Researcher',
    },
    {
      rank: 2,
      name: 'Marcus Aurelius',
      brierScore: 0.134,
      resolvedCount: 42,
      accuracy: '88.5%',
      role: 'Macro Economist',
    },
    {
      rank: 3,
      name: 'Satoshi_N_Clone',
      brierScore: 0.145,
      resolvedCount: 28,
      accuracy: '86.1%',
      role: 'Cryptographer & Risk Analyst',
    },
    {
      rank: 4,
      name: 'Climatologist_99',
      brierScore: 0.168,
      resolvedCount: 51,
      accuracy: '83.4%',
      role: 'Earth Sciences Professor',
    },
    {
      rank: 5,
      name: 'Aegis_Bot_v4',
      brierScore: 0.175,
      resolvedCount: 120,
      accuracy: '82.0%',
      role: 'Automated Forecasting AI',
    },
  ];

  const filteredForecasters = forecasters.filter(
    (forecaster) =>
      forecaster.name
        .toLowerCase()
        .includes(searchQuery.toLowerCase()) ||
      forecaster.role
        .toLowerCase()
        .includes(searchQuery.toLowerCase())
  );

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

      {/* Main */}

      <main className="mx-auto max-w-5xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="mx-auto mb-12 max-w-2xl text-center">
          <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-amber-800/50 bg-amber-950/60 px-3 py-1 text-xs font-semibold text-amber-400">
            <Trophy className="h-3.5 w-3.5" />
            Meritocratic Reputation Engine
          </div>

          <h1 className="mb-4 text-3xl font-extrabold tracking-tight text-white sm:text-5xl">
            Global Forecaster Leaderboard
          </h1>

          <p className="text-sm text-slate-400 sm:text-base">
            Rankings are determined by mathematical accuracy using the Brier
            score across resolved global predictions. Lower Brier scores indicate
            better calibration and forecasting performance.
          </p>
        </div>

        {/* Search */}

        <div className="relative mx-auto mb-8 max-w-md">
          <Search className="absolute left-4 top-3.5 h-5 w-5 text-slate-500" />

          <input
            type="text"
            placeholder="Search forecaster by name or role..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full rounded-xl border border-slate-800 bg-slate-900/80 py-3 pl-12 pr-4 text-sm text-slate-200 placeholder-slate-500 shadow-inner transition focus:border-cyan-500 focus:outline-none"
          />
        </div>

        {/* Table */}

        <div className="overflow-hidden rounded-2xl border border-slate-800 bg-slate-900/60 shadow-xl">
          <div className="overflow-x-auto">
            <table className="w-full border-collapse text-left">
              <thead>
                <tr className="border-b border-slate-800 bg-slate-950/50 text-xs uppercase tracking-wider text-slate-400">
                  <th className="px-6 py-4 font-semibold">Rank</th>
                  <th className="px-6 py-4 font-semibold">Forecaster</th>
                  <th className="px-6 py-4 font-semibold">Role</th>
                  <th className="px-6 py-4 text-right font-semibold">
                    Resolved
                  </th>
                  <th className="px-6 py-4 text-right font-semibold">
                    Accuracy
                  </th>
                  <th className="px-6 py-4 text-right font-semibold">
                    Brier Score
                  </th>
                </tr>
              </thead>

              <tbody className="divide-y divide-slate-800/60 text-sm">
                {filteredForecasters.map((forecaster) => (
                  <tr
                    key={forecaster.rank}
                    className="transition-colors hover:bg-slate-800/40"
                  >
                    <td className="px-6 py-4 font-bold text-white">
                      {forecaster.rank === 1 && (
                        <span className="flex h-6 w-6 items-center justify-center rounded-full border border-amber-500/40 bg-amber-500/20 text-xs text-amber-400">
                          1
                        </span>
                      )}

                      {forecaster.rank === 2 && (
                        <span className="flex h-6 w-6 items-center justify-center rounded-full border border-slate-300/40 bg-slate-300/20 text-xs text-slate-300">
                          2
                        </span>
                      )}

                      {forecaster.rank === 3 && (
                        <span className="flex h-6 w-6 items-center justify-center rounded-full border border-amber-700/40 bg-amber-700/20 text-xs text-amber-600">
                          3
                        </span>
                      )}

                      {forecaster.rank > 3 && (
                        <span className="pl-2 text-slate-400">
                          #{forecaster.rank}
                        </span>
                      )}
                    </td>

                    <td className="px-6 py-4">
                      <div className="flex items-center gap-3">
                        <div className="flex h-8 w-8 items-center justify-center rounded-full bg-slate-800">
                          <User className="h-4 w-4 text-cyan-400" />
                        </div>

                        <span className="font-semibold text-white">
                          {forecaster.name}
                        </span>
                      </div>
                    </td>

                    <td className="px-6 py-4 text-xs text-slate-400">
                      {forecaster.role}
                    </td>

                    <td className="px-6 py-4 text-right text-slate-300">
                      {forecaster.resolvedCount}
                    </td>

                    <td className="px-6 py-4 text-right font-semibold text-emerald-400">
                      {forecaster.accuracy}
                    </td>

                    <td className="px-6 py-4 text-right font-mono font-bold text-cyan-400">
                      {forecaster.brierScore.toFixed(3)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
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