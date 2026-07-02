import React, { useState } from 'react';
import UploadPanel from './components/UploadPanel';
import ResultsView from './components/ResultsView';
import StatsCard from './components/StatsCard';
import SummaryBox from './components/SummaryBox';
import { uploadAndCompare } from './api/compareApi';

function App() {
  const [fileA, setFileA] = useState(null);
  const [fileB, setFileB] = useState(null);
  const [sensitivity, setSensitivity] = useState(50);
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
      const response = await uploadAndCompare(fileA, fileB, sensitivity);
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
    <div className="min-h-screen bg-[#030712] bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(34,211,238,0.15),rgba(255,255,255,0))] px-4 py-12 text-slate-100 sm:px-6 lg:px-8 selection:bg-cyan-500/30">
      <div className="mx-auto max-w-7xl">
        <div className="mb-12 relative overflow-hidden rounded-3xl border border-slate-800/60 bg-slate-900/40 p-8 shadow-2xl shadow-cyan-900/20 backdrop-blur-xl print:hidden">
          <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/5 to-purple-500/5" />
          <div className="relative flex flex-col gap-6 md:flex-row md:items-end md:justify-between">
            <div>
              <p className="mb-3 text-xs font-bold uppercase tracking-[0.3em] text-cyan-400">CAD Compare Studio</p>
              <h1 className="font-display text-4xl font-bold tracking-tight sm:text-5xl bg-gradient-to-r from-white via-slate-200 to-cyan-200 bg-clip-text text-transparent">AI-Based CAD Difference Detection</h1>
              <p className="mt-4 max-w-2xl text-lg leading-relaxed text-slate-400">Upload two CAD drawings and get aligned difference highlights, detailed statistics, and an AI-generated summary in seconds.</p>
            </div>
            <div className="rounded-2xl border border-cyan-500/30 bg-cyan-500/10 px-5 py-3 text-sm font-medium text-cyan-200 shadow-[0_0_15px_rgba(34,211,238,0.1)]">
              Supports PNG, JPG, PDF, DXF, and DWG
            </div>
          </div>
        </div>

        <div className="grid gap-6 md:grid-cols-2 print:hidden">
          <UploadPanel label="Image A (Reference)" onFileSelect={setFileA} selectedFile={fileA} />
          <UploadPanel label="Image B (Comparison)" onFileSelect={setFileB} selectedFile={fileB} />
        </div>

        <div className="mt-12 flex flex-col items-center justify-center space-y-8 print:hidden">
          <div className="flex w-full max-w-md flex-col items-center space-y-4 rounded-3xl border border-slate-800/60 bg-slate-900/40 p-6 backdrop-blur-md shadow-xl shadow-black/50">
            <label htmlFor="sensitivity" className="text-sm font-semibold text-slate-300 tracking-wide uppercase">
              Sensitivity: <span className="text-cyan-400">{sensitivity}%</span>
            </label>
            <input
              type="range"
              id="sensitivity"
              min="0"
              max="100"
              value={sensitivity}
              onChange={(e) => setSensitivity(Number(e.target.value))}
              className="w-full h-2 rounded-lg appearance-none cursor-pointer bg-slate-800 accent-cyan-400 outline-none"
            />
            <p className="text-xs text-slate-500 text-center font-medium">Lower = Ignore small defects | Higher = Precision detail</p>
          </div>

          <button
            onClick={handleCompare}
            disabled={loading}
            className="group relative inline-flex items-center justify-center overflow-hidden rounded-full p-4 px-10 font-semibold text-white transition-all duration-300 ease-out hover:scale-[1.02] hover:shadow-[0_0_40px_-10px_rgba(34,211,238,0.5)] disabled:cursor-not-allowed disabled:opacity-50 disabled:hover:scale-100 disabled:hover:shadow-none"
          >
            <span className="absolute inset-0 bg-gradient-to-r from-cyan-600 via-blue-600 to-cyan-600 bg-[length:200%_100%] transition-all duration-500 group-hover:bg-[100%_0]" />
            <span className="relative flex items-center gap-3 tracking-wide">
              {loading ? (
                <>
                  <div className="h-5 w-5 animate-spin rounded-full border-2 border-white border-t-transparent" />
                  Processing...
                </>
              ) : 'Run Analysis'}
            </span>
          </button>
        </div>

        {error ? <div className="mt-8 rounded-2xl border border-red-800/50 bg-red-950/40 p-4 text-center text-sm font-medium text-red-300 shadow-lg backdrop-blur-md print:hidden">{error}</div> : null}

        {loading ? (
          <div className="mt-12 flex items-center justify-center rounded-3xl border border-slate-800/60 bg-slate-900/40 p-12 shadow-2xl backdrop-blur-md animate-pulse-slow print:hidden">
            <div className="h-12 w-12 animate-spin rounded-full border-4 border-cyan-500/30 border-t-cyan-400" />
            <span className="ml-4 font-display text-xl text-slate-300 tracking-wide">Analyzing geometry...</span>
          </div>
        ) : null}

        {result ? (
          <div className="mt-8 space-y-6">
            <div className="flex items-center justify-between print:hidden">
              <h2 className="text-2xl font-bold text-white">Analysis Results</h2>
              <button
                onClick={() => window.print()}
                className="rounded-xl border border-cyan-500/30 bg-cyan-500/10 px-5 py-2.5 font-semibold text-cyan-200 transition-all hover:bg-cyan-500/20 hover:shadow-[0_0_20px_rgba(34,211,238,0.2)] flex items-center gap-2 cursor-pointer"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
                Download Report (PDF)
              </button>
            </div>
            <div className="hidden print:block mb-8">
              <h1 className="text-3xl font-bold text-black">CAD Comparison Report</h1>
              <p className="text-sm text-gray-600 mt-2">Generated on {new Date().toLocaleDateString()}</p>
            </div>
            <ResultsView result={result} />
            <div className="grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
              <StatsCard statistics={result.statistics} />
              <SummaryBox summary={result.ai_summary} regions={result.statistics.regions} />
            </div>
          </div>
        ) : null}
      </div>
    </div>
  );
}

export default App;
