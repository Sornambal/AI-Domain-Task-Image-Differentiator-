import React from 'react';

function ResultsView({ result }) {
  if (!result) {
    return null;
  }

  return (
    <div className="space-y-6">
      <div className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-4 shadow-xl shadow-slate-950/30">
          <h3 className="mb-3 text-lg font-semibold text-slate-100">Original A</h3>
          <img src={result.original_a_url} alt="Original A" className="h-auto w-full rounded-2xl border border-slate-800 object-contain" />
        </div>
        <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-4 shadow-xl shadow-slate-950/30">
          <h3 className="mb-3 text-lg font-semibold text-slate-100">Original B</h3>
          <img src={result.original_b_url} alt="Original B" className="h-auto w-full rounded-2xl border border-slate-800 object-contain" />
        </div>
      </div>
      <div className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-4 shadow-xl shadow-slate-950/30">
          <h3 className="mb-3 text-lg font-semibold text-slate-100">Diff Visualization</h3>
          <img src={result.diff_visualization_url} alt="Diff visualization" className="h-auto w-full rounded-2xl border border-slate-800 object-contain" />
        </div>
        <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-4 shadow-xl shadow-slate-950/30">
          <h3 className="mb-3 text-lg font-semibold text-slate-100">Heatmap</h3>
          <img src={result.heatmap_url} alt="Heatmap" className="h-auto w-full rounded-2xl border border-slate-800 object-contain" />
        </div>
      </div>
    </div>
  );
}

export default ResultsView;
