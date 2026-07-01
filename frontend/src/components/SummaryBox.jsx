import React from 'react';

function SummaryBox({ summary }) {
  return (
    <div className="relative overflow-hidden rounded-3xl border border-cyan-500/30 bg-cyan-950/30 p-8 shadow-2xl shadow-cyan-900/20 backdrop-blur-xl">
      <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/10 to-transparent" />
      <div className="relative">
        <div className="mb-4 flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-cyan-500/20 text-cyan-400">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path d="M10.394 2.08a1 1 0 00-.788 0l-7 3a1 1 0 000 1.84L5.25 8.051a.999.999 0 01.356-.257l4-1.714a1 1 0 11.788 1.838L7.667 9.088l1.94.831a1 1 0 00.787 0l7-3a1 1 0 000-1.838l-7-3zM3.31 9.397L5 10.12v4.102a8.969 8.969 0 00-1.05-.174 1 1 0 01-.89-.89 11.115 11.115 0 01.25-3.762zM9.3 16.573A9.026 9.026 0 007 14.935v-3.957l1.818.78a3 3 0 002.364 0l5.508-2.361a11.026 11.026 0 01.25 3.762 1 1 0 01-.89.89 8.968 8.968 0 00-5.35 2.524 1 1 0 01-1.4 0zM6 18a1 1 0 001-1v-2.065a8.935 8.935 0 00-2-.712V17a1 1 0 001 1z" />
            </svg>
          </div>
          <h3 className="font-display text-xl font-semibold tracking-wide text-cyan-200">AI Analysis</h3>
        </div>
        <div className="rounded-2xl border border-cyan-500/20 bg-slate-950/50 p-6">
          <p className="leading-relaxed text-slate-300 font-medium">
            {summary || 'The AI summary will appear here once the comparison finishes.'}
          </p>
        </div>
      </div>
    </div>
  );
}

export default SummaryBox;
