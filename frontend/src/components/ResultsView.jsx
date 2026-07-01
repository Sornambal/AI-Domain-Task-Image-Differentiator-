import React from 'react';

function ResultsView({ result }) {
  if (!result) {
    return null;
  }

  return (
    <div className="space-y-8">
      <div className="grid gap-8 lg:grid-cols-2">
        <div className="group relative overflow-hidden rounded-3xl border border-slate-700/50 bg-slate-800/20 p-2 shadow-2xl backdrop-blur-xl transition-all hover:border-cyan-500/30">
          <div className="absolute inset-x-0 top-0 z-10 bg-gradient-to-b from-slate-900/90 to-transparent p-6 pt-5">
            <h3 className="font-display text-lg font-semibold tracking-wide text-slate-100">Reference Drawing</h3>
          </div>
          <div className="relative overflow-hidden rounded-2xl bg-slate-950/50">
            <img src={result.original_a_url} alt="Original A" className="h-auto w-full object-contain transition-transform duration-700 group-hover:scale-[1.02]" />
          </div>
        </div>
        <div className="group relative overflow-hidden rounded-3xl border border-slate-700/50 bg-slate-800/20 p-2 shadow-2xl backdrop-blur-xl transition-all hover:border-cyan-500/30">
          <div className="absolute inset-x-0 top-0 z-10 bg-gradient-to-b from-slate-900/90 to-transparent p-6 pt-5">
            <h3 className="font-display text-lg font-semibold tracking-wide text-slate-100">Comparison Drawing</h3>
          </div>
          <div className="relative overflow-hidden rounded-2xl bg-slate-950/50">
            <img src={result.original_b_url} alt="Original B" className="h-auto w-full object-contain transition-transform duration-700 group-hover:scale-[1.02]" />
          </div>
        </div>
      </div>
      <div className="grid gap-8 lg:grid-cols-2">
        <div className="group relative overflow-hidden rounded-3xl border border-purple-900/30 bg-slate-800/20 p-2 shadow-2xl backdrop-blur-xl transition-all hover:border-purple-500/50 hover:shadow-[0_0_30px_-5px_rgba(168,85,247,0.2)]">
          <div className="absolute inset-x-0 top-0 z-10 bg-gradient-to-b from-slate-900/90 to-transparent p-6 pt-5">
            <h3 className="font-display text-lg font-semibold tracking-wide text-purple-400">Heatmap Analysis</h3>
          </div>
          <div className="relative overflow-hidden rounded-2xl bg-slate-950/50">
            <img src={result.heatmap_url} alt="Heatmap" className="h-auto w-full object-contain transition-transform duration-700 group-hover:scale-[1.03]" />
          </div>
        </div>
        <div className="group relative overflow-hidden rounded-3xl border border-red-900/30 bg-slate-800/20 p-2 shadow-2xl backdrop-blur-xl transition-all hover:border-red-500/50 hover:shadow-[0_0_30px_-5px_rgba(239,68,68,0.2)]">
          <div className="absolute inset-x-0 top-0 z-10 flex items-center justify-between bg-gradient-to-b from-slate-900/90 to-transparent p-6 pt-5">
            <h3 className="font-display text-lg font-semibold tracking-wide text-red-400">Difference Overlay</h3>
            <span className="flex h-3 w-3 relative">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-red-500"></span>
            </span>
          </div>
          <div className="relative overflow-hidden rounded-2xl bg-slate-950/50">
            <img src={result.diff_visualization_url} alt="Diff visualization" className="h-auto w-full object-contain transition-transform duration-700 group-hover:scale-[1.03]" />
          </div>
        </div>
      </div>
    </div>
  );
}

export default ResultsView;
