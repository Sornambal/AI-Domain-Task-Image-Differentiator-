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
    try {
      const response = await uploadAndCompare(fileA, fileB);
      setResult(response);
    } catch (err) {
      setError(err?.response?.data?.detail || 'Comparison failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 px-4 py-10 text-slate-100 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-7xl">
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-semibold tracking-tight">AI-Based CAD Drawing Difference Detection</h1>
          <p className="mt-3 text-lg text-slate-400">Upload two CAD drawings and receive aligned diff highlights, statistics, and an AI summary.</p>
        </div>

        <div className="grid gap-6 md:grid-cols-2">
          <UploadPanel label="Image A (Reference)" onFileSelect={setFileA} selectedFile={fileA} />
          <UploadPanel label="Image B (Comparison)" onFileSelect={setFileB} selectedFile={fileB} />
        </div>

        <div className="mt-6 flex justify-center">
          <button
            onClick={handleCompare}
            disabled={loading}
            className="rounded-full bg-cyan-600 px-6 py-3 font-medium text-white transition hover:bg-cyan-500 disabled:cursor-not-allowed disabled:bg-slate-700"
          >
            {loading ? 'Comparing…' : 'Compare'}
          </button>
        </div>

        {error ? <div className="mt-4 rounded-xl border border-red-700 bg-red-950/50 p-3 text-sm text-red-200">{error}</div> : null}

        {loading ? (
          <div className="mt-8 flex items-center justify-center rounded-2xl border border-slate-700 bg-slate-900/80 p-10">
            <div className="h-10 w-10 animate-spin rounded-full border-4 border-cyan-500 border-t-transparent" />
            <span className="ml-3 text-slate-300">Analyzing drawings…</span>
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
