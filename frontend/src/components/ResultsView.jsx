import React from 'react';

function ResultsView({ result }) {
  if (!result) {
    return null;
  }

  return (
    <div className="space-y-6">
      <div className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-2xl border border-slate-700 bg-slate-900/80 p-4 shadow-lg">
          <h3 className="mb-3 text-lg font-semibold">Original A</h3>
          <img src={result.original_a_url} alt="Original A" className="h-auto w-full rounded-xl border border-slate-800" />
        </div>
        <div className="rounded-2xl border border-slate-700 bg-slate-900/80 p-4 shadow-lg">
          <h3 className="mb-3 text-lg font-semibold">Original B</h3>
          <img src={result.original_b_url} alt="Original B" className="h-auto w-full rounded-xl border border-slate-800" />
        </div>
      </div>
      <div className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-2xl border border-slate-700 bg-slate-900/80 p-4 shadow-lg">
          <h3 className="mb-3 text-lg font-semibold">Diff Visualization</h3>
          <img src={result.diff_visualization_url} alt="Diff visualization" className="h-auto w-full rounded-xl border border-slate-800" />
        </div>
        <div className="rounded-2xl border border-slate-700 bg-slate-900/80 p-4 shadow-lg">
          <h3 className="mb-3 text-lg font-semibold">Heatmap</h3>
          <img src={result.heatmap_url} alt="Heatmap" className="h-auto w-full rounded-xl border border-slate-800" />
        </div>
      </div>
    </div>
  );
}

export default ResultsView;
