import React from 'react';

function SummaryBox({ summary }) {
  return (
    <div className="rounded-2xl border border-cyan-700 bg-cyan-950/40 p-6 shadow-lg">
      <h3 className="mb-2 text-lg font-semibold">AI Summary</h3>
      <p className="leading-7 text-slate-200">{summary || 'The AI summary will appear here once the comparison finishes.'}</p>
    </div>
  );
}

export default SummaryBox;
