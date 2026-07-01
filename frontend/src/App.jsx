import React, { useState } from 'react';
import UploadPanel from './components/UploadPanel';
import ResultsView from './components/ResultsView';
import StatsCard from './components/StatsCard';
import SummaryBox from './components/SummaryBox';
import { uploadAndCompare } from './api/compareApi';

function App() {
  const [fileA, setFileA] = useState(null);
  const [fileB, setFileB] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleCompare = async () => {
    if (!fileA || !fileB) {
      setError('Please upload both drawings before comparing.');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);
    console.log('Starting compare', { fileA, fileB });

    try {
      const response = await uploadAndCompare(fileA, fileB);
      console.log('Compare response', response);
      setResult(response);
    } catch (err) {
      console.error('Compare error', err);
      setError(err?.response?.data?.detail || err?.message || 'Comparison failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top_left,_rgba(34,211,238,0.16),_transparent_24%),linear-gradient(135deg,_#020617_0%,_#07111f_100%)] px-4 py-8 text-slate-100 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-7xl">
        <div className="mb-8 rounded-3xl border border-slate-800/80 bg-slate-900/70 p-8 shadow-2xl shadow-cyan-950/20 backdrop-blur">
          <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
            <div>
              <p className="mb-2 text-sm font-semibold uppercase tracking-[0.3em] text-cyan-400">CAD Compare Studio</p>
              <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">AI-Based CAD Drawing Difference Detection</h1>
              <p className="mt-3 max-w-2xl text-lg text-slate-400">Upload two CAD drawings and get aligned difference highlights, detailed statistics, and an AI-generated summary in seconds.</p>
            </div>
            <div className="rounded-2xl border border-cyan-500/20 bg-cyan-500/10 px-4 py-3 text-sm text-cyan-200">
              Supports PNG, JPG, PDF, DXF, and DWG workflows
            </div>
          </div>
        </div>

        <div className="grid gap-6 md:grid-cols-2">
          <UploadPanel label="Image A (Reference)" onFileSelect={setFileA} selectedFile={fileA} />
          <UploadPanel label="Image B (Comparison)" onFileSelect={setFileB} selectedFile={fileB} />
        </div>

        <div className="mt-6 flex justify-center">
          <button
            onClick={handleCompare}
            disabled={loading}
            className="rounded-full bg-gradient-to-r from-cyan-500 to-blue-600 px-7 py-3.5 font-semibold text-white shadow-lg shadow-cyan-500/20 transition hover:scale-[1.01] hover:shadow-cyan-500/30 disabled:cursor-not-allowed disabled:from-slate-700 disabled:to-slate-700 disabled:shadow-none"
          >
            {loading ? 'Comparing…' : 'Compare Drawings'}
          </button>
        </div>

        {error ? <div className="mt-4 rounded-2xl border border-red-800/70 bg-red-950/70 p-4 text-sm text-red-200 shadow-lg">{error}</div> : null}

        {loading ? (
          <div className="mt-8 flex items-center justify-center rounded-3xl border border-slate-800 bg-slate-900/80 p-10 shadow-xl shadow-slate-950/30">
            <div className="h-10 w-10 animate-spin rounded-full border-4 border-cyan-500 border-t-transparent" />
            <span className="ml-3 text-lg text-slate-300">Analyzing drawings…</span>
          </div>
        ) : null}

        {result ? (
          <div className="mt-8 space-y-6">
            <ResultsView result={result} />
            <div className="grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
              <StatsCard statistics={result.statistics} />
              <SummaryBox summary={result.ai_summary} />
            </div>
          </div>
        ) : null}
      </div>
    </div>
  );
}

export default App;
