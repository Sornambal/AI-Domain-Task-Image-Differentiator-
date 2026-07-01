import React from 'react';

function SummaryBox({ summary }) {
  return (
    <div className="rounded-3xl border border-cyan-800/70 bg-cyan-950/40 p-6 shadow-xl shadow-cyan-950/20">
      <h3 className="mb-2 text-lg font-semibold text-cyan-200">AI Summary</h3>
      <p className="leading-7 text-slate-200">{summary || 'The AI summary will appear here once the comparison finishes.'}</p>
    </div>
  );
}

export default SummaryBox;
